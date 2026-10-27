import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catalog import Level, Stream
from app.models.progress import Badge
from app.schemas.admin_badges import BadgeCreate, BadgeUpdate


# Loads a badge, deleted or not, or returns 404
def get_badge_or_404(db: Session, badge_id: uuid.UUID) -> Badge:
    badge = db.get(Badge, badge_id)
    if badge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return badge


# The level and stream must exist; a missing one is a 404
def assert_level_and_stream_exist(
    db: Session, level_id: uuid.UUID, stream_id: uuid.UUID | None
) -> None:
    if db.get(Level, level_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    if stream_id is not None and db.get(Stream, stream_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")


# The 409 for a name already in use. A deleted badge still holds its name, so say so when it's the cause.
def duplicate_name_error(
    db: Session, level_id: uuid.UUID, stream_id: uuid.UUID | None, name: str
) -> HTTPException:
    deleted_holder = db.scalar(
        select(Badge.id)
        .where(
            Badge.level_id == level_id,
            Badge.stream_id == stream_id,
            Badge.name == name,
            Badge.deleted_at.is_not(None),
        )
        .limit(1)
    )
    detail = (
        "A deleted badge already uses this name here"
        if deleted_holder
        else "A badge with this name already exists here"
    )
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


# Every badge on a level, including soft-deleted ones, in display order
def list_badges(db: Session, level_id: uuid.UUID) -> list[Badge]:
    return list(
        db.scalars(
            select(Badge).where(Badge.level_id == level_id).order_by(Badge.sort_order)
        ).all()
    )


# Creates a badge; a duplicate name at the same level and stream is a 409
def create_badge(db: Session, body: BadgeCreate) -> Badge:
    assert_level_and_stream_exist(db, body.level_id, body.stream_id)
    badge = Badge(**body.model_dump())
    db.add(badge)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise duplicate_name_error(db, body.level_id, body.stream_id, body.name)
    db.refresh(badge)
    return badge


# Changes a badge; only the fields that were sent are changed. A deleted badge can't be changed.
def update_badge(db: Session, badge: Badge, body: BadgeUpdate) -> Badge:
    if badge.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This badge is deleted, so it can't be changed",
        )
    changes = body.model_dump(exclude_unset=True)
    target_level = changes.get("level_id", badge.level_id)
    target_stream = changes.get("stream_id", badge.stream_id)
    target_name = changes.get("name", badge.name)
    assert_level_and_stream_exist(db, target_level, target_stream)
    for field, value in changes.items():
        setattr(badge, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise duplicate_name_error(db, target_level, target_stream, target_name)
    db.refresh(badge)
    return badge


# Every level and stream, for the Admin's dropdowns
def catalog(db: Session) -> dict:
    levels = db.scalars(select(Level).order_by(Level.name)).all()
    streams = db.scalars(select(Stream).order_by(Stream.name)).all()
    return {"levels": list(levels), "streams": list(streams)}


# Soft-deletes a badge: it's hidden from Scouts, but its entries and history stay
def soft_delete_badge(db: Session, badge: Badge) -> None:
    badge.deleted_at = datetime.now(UTC)
    db.commit()
