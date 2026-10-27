import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.people import Scout
from app.models.progress import Badge
from app.schemas.badges import (
    BadgeDetailOut,
    BadgeListItem,
    GroupOut,
    RequirementOut,
)
from app.schemas.entries import EntryOut
from app.services import progress
from app.services.scouts import get_current_scout

router = APIRouter(prefix="/badges", tags=["badges"])


# Scout: the badges on their current level, each with its progress status
@router.get("/current", response_model=list[BadgeListItem])
def list_current_badges(
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    level_id = progress.current_level_id(db, scout)
    if level_id is None:
        return []
    badges = db.scalars(
        select(Badge)
        .where(
            Badge.level_id == level_id,
            Badge.deleted_at.is_(None),
            or_(Badge.stream_id.is_(None), Badge.stream_id == scout.stream_id),
        )
        .order_by(Badge.sort_order)
    ).all()
    return [
        BadgeListItem(
            id=badge.id,
            name=badge.name,
            status=progress.badge_status(db, scout, badge.id),
        )
        for badge in badges
    ]


# Scout: one badge with its checklist and the Scout's own entries
@router.get("/{badge_id}", response_model=BadgeDetailOut)
def get_badge_detail(
    badge_id: uuid.UUID,
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    badge = progress.live_badge(db, badge_id)
    # A badge off the Scout's current level is treated as missing
    if badge is None or badge.level_id != progress.current_level_id(db, scout):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )

    entries = progress.entries_by_requirement(db, scout, badge_id)
    requirements = [
        RequirementOut(
            id=req.id,
            text=req.text,
            detail=req.detail,
            group_id=req.group_id,
            entry=EntryOut.model_validate(entries[req.id]) if req.id in entries else None,
        )
        for req in progress.requirements_for_scout(db, scout, badge_id)
    ]
    groups = [
        GroupOut(
            id=group.id,
            title=group.title,
            pick_count=group.pick_count,
            parent_group_id=group.parent_group_id,
        )
        for group in progress.groups_for_badge(db, badge_id)
    ]
    return BadgeDetailOut(
        id=badge.id,
        name=badge.name,
        description=badge.description,
        status=progress.badge_status(db, scout, badge_id),
        groups=groups,
        requirements=requirements,
    )
