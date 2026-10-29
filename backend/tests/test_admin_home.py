import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

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
