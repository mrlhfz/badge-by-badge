import uuid

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import get_current_role, get_current_user_id, require_role
from app.enums import Role


# Stands in for a database session that returns a fixed role
class FakeSession:
    def __init__(self, role):
        self.role = role

    def scalar(self, statement):
        return self.role


# A token that isn't a real JWT must be refused with 401
def test_garbage_token_is_rejected():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="not-a-token"
    )
    with pytest.raises(HTTPException) as error:
        get_current_user_id(credentials)
    assert error.value.status_code == 401


# A Scout is refused by a check that only allows Admins
def test_scout_is_refused_by_admin_only():
    check = require_role(Role.Admin)
    with pytest.raises(HTTPException) as error:
        check(role=Role.Scout)
    assert error.value.status_code == 403


# An Admin passes the same check
def test_admin_is_allowed():
    check = require_role(Role.Admin)
    assert check(role=Role.Admin) == Role.Admin


# A found profile returns its role
def test_profile_role_is_returned():
    db = FakeSession(Role.Leader)
    assert get_current_role(user_id=str(uuid.uuid4()), db=db) == Role.Leader


# A user ID that isn't a UUID is refused with 401
def test_non_uuid_user_id_is_refused():
    db = FakeSession(Role.Admin)
    with pytest.raises(HTTPException) as error:
        get_current_role(user_id="not-a-uuid", db=db)
    assert error.value.status_code == 401


# A signed-in user with no profile row is refused with 403
def test_missing_profile_is_refused():
    db = FakeSession(None)
    with pytest.raises(HTTPException) as error:
        get_current_role(user_id=str(uuid.uuid4()), db=db)
    assert error.value.status_code == 403
