import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.enums import EntryStatus
from app.models.people import Scout, TroopLeader
from app.models.progress import Badge, Entry, EntryComment, Requirement, ScoutLevel
from app.schemas.entries import EntryCreate, EntryUpdate


# Loads an entry, or returns 404 if it doesn't exist
def get_entry_or_404(db: Session, entry_id: uuid.UUID) -> Entry:
    entry = db.get(Entry, entry_id)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    return entry


# A Scout may change only their own entry, and only while it is still pending.
# Another Scout's entry gets the same 404 as a missing one, so IDs can't be probed.
def assert_scout_can_change(entry: Entry, scout: Scout) -> None:
    if entry.scout_id != scout.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    if entry.status != EntryStatus.Pending:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Confirmed entries can't be changed",
        )


# A Leader may act only on scouts in the troop they lead
def assert_leader_leads_scout(
    db: Session, leader_profile_id: uuid.UUID, scout: Scout
) -> None:
    led_troop = db.scalar(
        select(TroopLeader.troop_id).where(TroopLeader.profile_id == leader_profile_id)
    )
    if led_troop != scout.troop_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This scout is not in your troop",
        )


# A requirement must match the Scout's current level and stream.
# A missing current level (None) never matches, so the Scout is refused.
def assert_requirement_applies(
    requirement_stream_id: uuid.UUID | None,
    badge_level_id: uuid.UUID,
    scout_stream_id: uuid.UUID,
    scout_level_id: uuid.UUID | None,
) -> None:
    on_level = badge_level_id == scout_level_id
    on_stream = requirement_stream_id in (None, scout_stream_id)
    if not (on_level and on_stream):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="This requirement is not on your current level or stream",
        )


# Creates a pending entry for the signed-in Scout
def create_entry(db: Session, scout: Scout, body: EntryCreate) -> Entry:
    requirement = db.get(Requirement, body.requirement_id)
    if requirement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found",
        )
    badge = db.get(Badge, requirement.badge_id)
    scout_level_id = db.scalar(
        select(ScoutLevel.level_id).where(
            ScoutLevel.scout_id == scout.id,
            ScoutLevel.ended_at.is_(None),
        )
    )
    assert_requirement_applies(
        requirement.stream_id, badge.level_id, scout.stream_id, scout_level_id
    )
    entry = Entry(
        scout_id=scout.id,
        requirement_id=body.requirement_id,
        entry_date=body.entry_date,
        note=body.note,
        status=EntryStatus.Pending,
    )
    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        # The database allows one entry per scout and requirement
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This requirement already has an entry",
        )
    db.refresh(entry)
    return entry


# Lists a Scout's entries, oldest first, one page at a time
def list_entries_for_scout(
    db: Session, scout_id: uuid.UUID, limit: int, offset: int
) -> list[Entry]:
    query = (
        select(Entry)
        .where(Entry.scout_id == scout_id)
        .order_by(Entry.entry_date)
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(query).all())


# Changes a pending entry; only the fields that were sent are changed
def update_entry(db: Session, entry: Entry, scout: Scout, body: EntryUpdate) -> Entry:
    assert_scout_can_change(entry, scout)
    changes = body.model_dump(exclude_unset=True)
    if changes.get("entry_date") is not None:
        entry.entry_date = changes["entry_date"]
    if "note" in changes:
        entry.note = changes["note"]
    db.commit()
    db.refresh(entry)
    return entry


# Deletes a pending entry and its comments in one transaction
def delete_entry(db: Session, entry: Entry, scout: Scout) -> None:
    assert_scout_can_change(entry, scout)
    # Comments point at the entry with no cascade, so they must go first
    db.execute(delete(EntryComment).where(EntryComment.entry_id == entry.id))
    db.delete(entry)
    db.commit()


# Marks an entry confirmed by a Leader from the same troop as the Scout
def confirm_entry(db: Session, entry: Entry, leader_profile_id: uuid.UUID) -> Entry:
    scout = db.get(Scout, entry.scout_id)
    assert_leader_leads_scout(db, leader_profile_id, scout)
    # Confirming twice would overwrite who confirmed the entry and when
    if entry.status == EntryStatus.Confirmed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Entry is already confirmed",
        )
    entry.status = EntryStatus.Confirmed
    entry.confirmed_by = leader_profile_id
    entry.confirmed_at = datetime.now(UTC)
    db.commit()
    db.refresh(entry)
    return entry
