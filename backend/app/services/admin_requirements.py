import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.catalog import Stream
from app.models.progress import Requirement, RequirementGroup
from app.schemas.admin_requirements import RequirementCreate, RequirementUpdate
from app.services.admin_badges import get_badge_or_404


# Loads a requirement, or returns 404 if it doesn't exist
def get_requirement_or_404(db: Session, requirement_id: uuid.UUID) -> Requirement:
    requirement = db.get(Requirement, requirement_id)
    if requirement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found",
        )
    return requirement


# Every requirement on a badge in order, including removed ones so the Admin can see them
def list_requirements(db: Session, badge_id: uuid.UUID) -> list[Requirement]:
    get_badge_or_404(db, badge_id)
    return list(
        db.scalars(
            select(Requirement)
            .where(Requirement.badge_id == badge_id)
            .order_by(Requirement.position)
        ).all()
    )


# A group must belong to the same badge as the requirement it's given to
def assert_group_on_badge(db: Session, group_id: uuid.UUID, badge_id: uuid.UUID) -> None:
    group = db.get(RequirementGroup, group_id)
    if group is None or group.badge_id != badge_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="That group is not on this badge",
        )


# A stream must exist, so a bad ID gets a clear message instead of a database error
def assert_stream_exists(db: Session, stream_id: uuid.UUID) -> None:
    if db.get(Stream, stream_id) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="That stream does not exist",
        )


# Adds a requirement at the end of a badge's list
def create_requirement(db: Session, badge_id: uuid.UUID, body: RequirementCreate) -> Requirement:
    get_badge_or_404(db, badge_id)
    if body.group_id is not None:
        assert_group_on_badge(db, body.group_id, badge_id)
    if body.stream_id is not None:
        assert_stream_exists(db, body.stream_id)
    # Positions must stay unique per badge, and removed rows still hold theirs, so take the next free one
    last = db.scalar(select(func.max(Requirement.position)).where(Requirement.badge_id == badge_id))
    requirement = Requirement(
        badge_id=badge_id,
        position=(last or 0) + 1,
        text=body.text,
        detail=body.detail,
        group_id=body.group_id,
        stream_id=body.stream_id,
    )
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return requirement


# Changes only the fields the Admin sent
def update_requirement(db: Session, requirement: Requirement, body: RequirementUpdate) -> Requirement:
    changes = body.model_dump(exclude_unset=True)
    if changes.get("group_id") is not None:
        assert_group_on_badge(db, changes["group_id"], requirement.badge_id)
    if changes.get("stream_id") is not None:
        assert_stream_exists(db, changes["stream_id"])
    for field, value in changes.items():
        setattr(requirement, field, value)
    db.commit()
    db.refresh(requirement)
    return requirement


# Removes a requirement from Scouts' checklists, but keeps it and its entries in the records
def soft_delete_requirement(db: Session, requirement: Requirement) -> None:
    requirement.deleted_at = datetime.now(UTC)
    db.commit()
