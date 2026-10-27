import uuid
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.auth import get_current_user_id
from app.database import get_db
from app.enums import Role
from app.services import admin_scouts as scout_service
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


# A Scout is refused by the Admin scout routes
def test_scout_is_refused_on_scout_list(client_as):
    response = client_as(Role.Scout).get("/admin/scouts")
    assert response.status_code == 403


# A Leader is refused by the Admin scout routes too
def test_leader_is_refused_on_verification(client_as):
    response = client_as(Role.Leader).post(
        f"/admin/scouts/{uuid.uuid4()}/verification", json={"action": "verify"}
    )
    assert response.status_code == 403


# An action that isn't verify or unverify is rejected before anything changes
def test_unknown_action_is_rejected(client_as):
    response = client_as(Role.Admin).post(
        f"/admin/scouts/{uuid.uuid4()}/verification", json={"action": "delete"}
    )
    assert response.status_code == 422


# An Admin gets the Scout list from the service, as JSON
def test_admin_gets_scout_list(client_as, monkeypatch):
    monkeypatch.setattr(
        scout_service,
        "list_scouts",
        lambda db: [
            SimpleNamespace(id=uuid.uuid4(), full_name="Test Scout", is_verified=False)
        ],
    )
    response = client_as(Role.Admin).get("/admin/scouts")
    assert response.status_code == 200
    assert response.json()[0]["full_name"] == "Test Scout"
    assert response.json()[0]["is_verified"] is False
