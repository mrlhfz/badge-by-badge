import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.dialects import postgresql

from app.auth import get_current_user_id
from app.database import get_db
from app.enums import Role, VerificationAction
from app.schemas.admin_home import AdminHomeOut, RecentVerificationOut
from app.services import admin_home as home_service
from main import app


# Stands in for a database session whose role lookup returns a fixed role
class FakeSession:
    def __init__(self, role):
        self.role = role

    def scalar(self, statement):
        return self.role


@pytest.fixture
def client_as():
    # Returns a test client that is logged in with the given role
    def make(role):
        app.dependency_overrides[get_current_user_id] = lambda: str(uuid.uuid4())
        app.dependency_overrides[get_db] = lambda: FakeSession(role)
        return TestClient(app)

    yield make
    app.dependency_overrides.clear()


# A Scout is refused by the Admin home route
def test_scout_is_refused_on_admin_home(client_as):
    response = client_as(Role.Scout).get("/admin/home")
    assert response.status_code == 403


# A Leader is refused by the Admin home route too
def test_leader_is_refused_on_admin_home(client_as):
    response = client_as(Role.Leader).get("/admin/home")
    assert response.status_code == 403


# An Admin gets the counts and recent changes from the service, as JSON
def test_admin_gets_home_summary(client_as, monkeypatch):
    monkeypatch.setattr(
        home_service,
        "get_admin_home",
        lambda db: AdminHomeOut(
            unverified_scouts=3,
            badge_count=12,
            recent_verifications=[
                RecentVerificationOut(
                    id=uuid.uuid4(),
                    scout_name="Test Scout",
                    action=VerificationAction.Verify,
                    created_at=datetime(2026, 10, 29, 9, 0, tzinfo=UTC),
                )
            ],
        ),
    )
    response = client_as(Role.Admin).get("/admin/home")
    assert response.status_code == 200
    body = response.json()
    assert body["unverified_scouts"] == 3
    assert body["badge_count"] == 12
    assert body["recent_verifications"][0]["scout_name"] == "Test Scout"
    assert body["recent_verifications"][0]["action"] == "verify"


# Records each query the service runs, and returns empty results, so the SQL can be checked
class RecordingSession:
    def __init__(self):
        self.statements = []

    def scalar(self, statement):
        self.statements.append(statement)
        return 0

    def execute(self, statement):
        self.statements.append(statement)
        return SimpleNamespace(all=list)


# Runs the service and returns the three queries as Postgres SQL text, in the order they run
def compiled_queries():
    session = RecordingSession()
    home_service.get_admin_home(session)
    return [
        str(
            statement.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        for statement in session.statements
    ]


# The unverified count only counts Scouts who are not verified
def test_unverified_count_skips_verified_scouts():
    unverified_sql, _, _ = compiled_queries()
    assert "scouts.is_verified IS false" in unverified_sql


# The badge count skips badges that were removed (soft-deleted)
def test_badge_count_skips_removed_badges():
    _, badge_sql, _ = compiled_queries()
    assert "badges.deleted_at IS NULL" in badge_sql


# The recent list is newest first and holds only the latest five
def test_recent_list_is_newest_five():
    _, _, recent_sql = compiled_queries()
    assert "ORDER BY verification_events.created_at DESC" in recent_sql
    assert "LIMIT 5" in recent_sql
