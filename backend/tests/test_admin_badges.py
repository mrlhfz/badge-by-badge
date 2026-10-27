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


# A Scout is refused by the Admin badge routes
def test_scout_is_refused_on_admin_badges(client_as):
    response = client_as(Role.Scout).get(f"/admin/badges?level_id={uuid.uuid4()}")
    assert response.status_code == 403


# A Leader is refused by the Admin badge routes too
def test_leader_is_refused_on_admin_badges(client_as):
    response = client_as(Role.Leader).get(f"/admin/badges?level_id={uuid.uuid4()}")
    assert response.status_code == 403
