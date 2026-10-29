import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.enums import Role
from app.schemas.admin_requirements import (
    RequirementAdminOut,
    RequirementCreate,
    RequirementUpdate,
)
from app.services import admin_requirements as requirement_service

# One guard on the router covers every route, so a route added later can't forget it
router = APIRouter(
    prefix="/admin/badges",
    tags=["admin requirements"],
    dependencies=[Depends(require_role(Role.Admin))],
)


# Admin: every requirement on a badge, in order, including removed ones
@router.get("/{badge_id}/requirements", response_model=list[RequirementAdminOut])
def list_requirements(badge_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    return requirement_service.list_requirements(db, badge_id)


# Admin: add a requirement to the end of a badge's list
@router.post(
    "/{badge_id}/requirements",
    response_model=RequirementAdminOut,
    status_code=status.HTTP_201_CREATED,
)
def create_requirement(
    badge_id: uuid.UUID,
    body: RequirementCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.create_requirement(db, badge_id, body)


# Admin: change a requirement's text, detail, group or stream
@router.patch("/requirements/{requirement_id}", response_model=RequirementAdminOut)
def update_requirement(
    requirement_id: uuid.UUID,
    body: RequirementUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    requirement = requirement_service.get_requirement_or_404(db, requirement_id)
    return requirement_service.update_requirement(db, requirement, body)


# Admin: remove a requirement from Scouts' checklists, keeping its entries
@router.delete("/requirements/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(
    requirement_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
):
    requirement = requirement_service.get_requirement_or_404(db, requirement_id)
    requirement_service.soft_delete_requirement(db, requirement)
