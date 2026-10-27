import uuid
from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import EntryStatus
from app.models.people import Scout
from app.models.progress import Entry, EntryComment
from app.services import entries as entry_service


# Adds a Leader's comment to a pending entry, only for a Scout in the troop they lead
def add_comment(
    db: Session, entry: Entry, leader_profile_id: uuid.UUID, body: str
) -> EntryComment:
    scout = db.get(Scout, entry.scout_id)
    entry_service.assert_leader_leads_scout(db, leader_profile_id, scout)
    # A confirmed entry is settled, so it takes no new comments
    if entry.status != EntryStatus.Pending:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending entries can be commented on",
        )
    comment = EntryComment(entry_id=entry.id, author_id=leader_profile_id, body=body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# All comments for a set of entries, oldest first, grouped by entry ID
def comments_by_entry(
    db: Session, entry_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[EntryComment]]:
    grouped: dict[uuid.UUID, list[EntryComment]] = defaultdict(list)
    if not entry_ids:
        return grouped
    comments = db.scalars(
        select(EntryComment)
        .where(EntryComment.entry_id.in_(entry_ids))
        .order_by(EntryComment.created_at)
    ).all()
    for comment in comments:
        grouped[comment.entry_id].append(comment)
    return grouped
