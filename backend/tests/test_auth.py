import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import get_current_user_id, require_role
from app.enums import Role


# A token that isn't a real JWT must be refused with 401
def test_garbage_token_is_rejected():
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="not-a-token")
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
