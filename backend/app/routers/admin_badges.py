import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.enums import Role
from app.schemas.admin_badges import BadgeAdminOut, BadgeCreate, BadgeUpdate
from app.services import admin_badges as badge_service

# One guard on the router covers every route, so a route added later can't forget it
router = APIRouter(
    prefix="/admin/badges",
    tags=["admin badges"],
    dependencies=[Depends(require_role(Role.Admin))],
)


# Admin: every badge on a level, including deleted ones
@router.get("", response_model=list[BadgeAdminOut])
def list_badges(
    level_id: Annotated[uuid.UUID, Query()],
    db: Annotated[Session, Depends(get_db)],
):
    return badge_service.list_badges(db, level_id)


# Admin: create a badge on a level, with an optional stream
@router.post("", response_model=BadgeAdminOut, status_code=status.HTTP_201_CREATED)
def create_badge(body: BadgeCreate, db: Annotated[Session, Depends(get_db)]):
    return badge_service.create_badge(db, body)


# Admin: change a badge's level, stream, name, description, order, kind or path row
@router.patch("/{badge_id}", response_model=BadgeAdminOut)
def update_badge(
    badge_id: uuid.UUID,
    body: BadgeUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    badge = badge_service.get_badge_or_404(db, badge_id)
    return badge_service.update_badge(db, badge, body)


# Admin: soft-delete a badge
@router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(badge_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    badge = badge_service.get_badge_or_404(db, badge_id)
    badge_service.soft_delete_badge(db, badge)
