import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.people import Scout
from app.schemas.badges import (
    BadgeDetailOut,
    BadgeListItem,
    GroupOut,
    RequirementOut,
)
from app.schemas.entries import EntryOut
from app.services import progress
from app.services.path_rules import is_locked
from app.services.scouts import get_current_scout

router = APIRouter(prefix="/badges", tags=["badges"])


# Scout: the badges on their current level, with status, path row and whether each is locked
@router.get("/current", response_model=list[BadgeListItem])
def list_current_badges(
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    level_id = progress.current_level_id(db, scout)
    if level_id is None:
        return []

    path = progress.path_badges(db, scout, level_id)
    on_path = {p.id: p for p in path}
    items = []
    for badge in progress.visible_badges(db, scout, level_id):
        placed = on_path.get(badge.id)
        items.append(
            BadgeListItem(
                id=badge.id,
                name=badge.name,
                status=progress.badge_status(db, scout, badge.id),
                row=placed.row if placed else None,
                locked=is_locked(placed, path) if placed else False,
            )
        )
    return items


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

    # A locked badge can't be opened until the rows before it are complete
    path = progress.path_badges(db, scout, badge.level_id)
    placed = next((p for p in path if p.id == badge_id), None)
    if placed is not None and is_locked(placed, path):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Finish the earlier rows before opening this badge",
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
