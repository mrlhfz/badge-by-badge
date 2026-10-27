import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.auth import get_current_user_id
from app.database import get_db
from app.enums import Role
from app.services import admin_requirements as requirement_service
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


# A Scout is refused by the Admin requirement routes
def test_scout_is_refused_on_requirement_list(client_as):
    response = client_as(Role.Scout).get(f"/admin/badges/{uuid.uuid4()}/requirements")
    assert response.status_code == 403


# A Leader is refused when trying to add a requirement
def test_leader_is_refused_on_create(client_as):
    response = client_as(Role.Leader).post(
        f"/admin/badges/{uuid.uuid4()}/requirements", json={"text": "Renang 50 meter"}
    )
    assert response.status_code == 403


# A requirement with no text is rejected before anything is saved
def test_empty_text_is_rejected(client_as):
    response = client_as(Role.Admin).post(
        f"/admin/badges/{uuid.uuid4()}/requirements", json={"text": ""}
    )
    assert response.status_code == 422


# The text can be left out of an update, but it can't be sent as null
def test_null_text_is_rejected_on_update(client_as):
    response = client_as(Role.Admin).patch(
        f"/admin/badges/requirements/{uuid.uuid4()}", json={"text": None}
    )
    assert response.status_code == 422


# An Admin gets the list from the service, removed requirements included
def test_admin_gets_requirement_list(client_as, monkeypatch):
    monkeypatch.setattr(
        requirement_service,
        "list_requirements",
        lambda db, badge_id: [
            SimpleNamespace(
                id=uuid.uuid4(),
                badge_id=badge_id,
                position=1,
                text="Renang 50 meter",
                detail=None,
                group_id=None,
                stream_id=None,
                deleted_at=datetime(2026, 10, 27, tzinfo=UTC),
            )
        ],
    )
    response = client_as(Role.Admin).get(f"/admin/badges/{uuid.uuid4()}/requirements")
    assert response.status_code == 200
    assert response.json()[0]["text"] == "Renang 50 meter"
    assert response.json()[0]["deleted_at"] is not None
