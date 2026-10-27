import uuid

import pytest
from fastapi.testclient import TestClient

from app.auth import get_current_user_id
from app.database import get_db
from app.enums import Role
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
