import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user_id, require_role
from app.database import get_db
from app.enums import Role
from app.schemas.admin_scouts import AdminScoutOut, VerificationIn
from app.services import admin_scouts as scout_service

# One guard on the router covers every route, so a route added later can't forget it
router = APIRouter(
    prefix="/admin/scouts",
    tags=["admin scouts"],
    dependencies=[Depends(require_role(Role.Admin))],
)


# Admin: every Scout, with whether they are verified
@router.get("", response_model=list[AdminScoutOut])
def list_scouts(db: Annotated[Session, Depends(get_db)]):
    return scout_service.list_scouts(db)


# Admin: verify or unverify a Scout
@router.post("/{scout_id}/verification", response_model=AdminScoutOut)
def change_verification(
    scout_id: uuid.UUID,
    body: VerificationIn,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return scout_service.set_verified(db, scout_id, body.action, uuid.UUID(user_id))
