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
def as_scout():
    app.dependency_overrides[get_current_user_id] = lambda: str(uuid.uuid4())
    app.dependency_overrides[get_db] = lambda: FakeSession(Role.Scout)
    yield TestClient(app)
    app.dependency_overrides.clear()


# A Scout is refused by the Admin badge routes
def test_scout_is_refused_on_admin_badges(as_scout):
    response = as_scout.get(f"/admin/badges?level_id={uuid.uuid4()}")
    assert response.status_code == 403
