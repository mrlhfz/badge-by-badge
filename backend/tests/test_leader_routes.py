import uuid
from datetime import date, datetime
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.auth import get_current_user_id
from app.database import get_db
from app.enums import EntryStatus, Role
from app.schemas.leader import LeaderSummaryOut, LogEntryOut, PendingEntryOut
from app.services import comments as comment_service
from app.services import entries as entry_service
from app.services import leader as leader_service
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


# A Scout is refused by the Leader routes
def test_scout_is_refused_on_leader_routes(client_as):
    response = client_as(Role.Scout).get("/leader/troop/scouts")
    assert response.status_code == 403


# An Admin is refused by the Leader routes too, since they don't lead a troop
def test_admin_is_refused_on_leader_routes(client_as):
    response = client_as(Role.Admin).get("/leader/troop/scouts")
    assert response.status_code == 403


# A Scout is refused by the summary route too
def test_scout_is_refused_on_summary(client_as):
    response = client_as(Role.Scout).get("/leader/summary")
    assert response.status_code == 403


# A Leader gets the counts from the service, as JSON
def test_leader_gets_troop_summary(client_as, monkeypatch):
    monkeypatch.setattr(
        leader_service,
        "troop_summary",
        lambda db, profile_id: LeaderSummaryOut(
            full_name="Test Leader", scout_count=3, pending_entries=2
        ),
    )
    response = client_as(Role.Leader).get("/leader/summary")
    assert response.status_code == 200
    assert response.json() == {
        "full_name": "Test Leader",
        "scout_count": 3,
        "pending_entries": 2,
    }


# A Scout is refused by the pending-entries route
def test_scout_is_refused_on_pending_entries(client_as):
    response = client_as(Role.Scout).get("/leader/entries/pending")
    assert response.status_code == 403


# A Leader gets the pending entries from the service, as JSON
def test_leader_gets_pending_entries(client_as, monkeypatch):
    entry_id = uuid.uuid4()
    scout_id = uuid.uuid4()
    monkeypatch.setattr(
        leader_service,
        "pending_entries",
        lambda db, profile_id: [
            PendingEntryOut(
                id=entry_id,
                scout_id=scout_id,
                scout_name="Test Scout",
                badge_name="Ahli Renang",
                requirement_text="Renang 50 meter",
                entry_date=date(2026, 10, 1),
                note=None,
                comments=[],
            )
        ],
    )
    response = client_as(Role.Leader).get("/leader/entries/pending")
    assert response.status_code == 200
    assert response.json()[0]["scout_name"] == "Test Scout"
    assert response.json()[0]["entry_date"] == "2026-10-01"


# A Scout is refused by the log route
def test_scout_is_refused_on_log(client_as):
    response = client_as(Role.Scout).get("/leader/log")
    assert response.status_code == 403


# A Scout is refused when trying to comment
def test_scout_is_refused_on_comment(client_as):
    response = client_as(Role.Scout).post(
        f"/leader/entries/{uuid.uuid4()}/comments", json={"body": "Well done"}
    )
    assert response.status_code == 403


# An empty comment is rejected before anything is saved
def test_empty_comment_is_rejected(client_as):
    response = client_as(Role.Leader).post(
        f"/leader/entries/{uuid.uuid4()}/comments", json={"body": ""}
    )
    assert response.status_code == 422


# A Leader gets the log from the service, one row per confirmed entry
def test_leader_gets_log(client_as, monkeypatch):
    monkeypatch.setattr(
        leader_service,
        "leader_log",
        lambda db, profile_id: [
            LogEntryOut(
                id=uuid.uuid4(),
                scout_id=uuid.uuid4(),
                scout_name="Test Scout",
                badge_name="Ahli Renang",
                requirement_text="Renang 50 meter",
                entry_date=date(2026, 10, 1),
                note=None,
                confirmed_at=datetime(2026, 10, 1, 9, 0),
            )
        ],
    )
    response = client_as(Role.Leader).get("/leader/log")
    assert response.status_code == 200
    assert response.json()[0]["scout_name"] == "Test Scout"


# Stands in for a database session: the Scout lookup returns a stub Scout
class CommentFakeDb:
    def get(self, model, key):
        return SimpleNamespace(id=key, troop_id=uuid.uuid4())


# A comment on a confirmed entry is refused, since the entry is already settled
def test_comment_on_confirmed_entry_is_refused(monkeypatch):
    # Skip the troop check here, so the test reaches the confirmed-entry rule
    monkeypatch.setattr(entry_service, "assert_leader_leads_scout", lambda db, leader_id, scout: None)
    entry = SimpleNamespace(
        id=uuid.uuid4(), scout_id=uuid.uuid4(), status=EntryStatus.Confirmed
    )
    with pytest.raises(HTTPException) as error:
        comment_service.add_comment(CommentFakeDb(), entry, uuid.uuid4(), "Well done")
    assert error.value.status_code == 409
