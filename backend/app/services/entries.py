import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.enums import EntryStatus
from app.models.people import Scout, TroopLeader
from app.models.progress import Entry, Requirement
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


# A Scout may change only their own entry, and only while it is still pending
def assert_scout_can_change(entry: Entry, scout: Scout) -> None:
    if entry.scout_id != scout.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This entry is not yours",
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
        select(TroopLeader.troop_id).where(
            TroopLeader.profile_id == leader_profile_id
        )
    )
    if led_troop != scout.troop_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This scout is not in your troop",
        )


# Creates a pending entry for the signed-in Scout
def create_entry(db: Session, scout: Scout, body: EntryCreate) -> Entry:
    if db.get(Requirement, body.requirement_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found",
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


# Changes a pending entry; only the fields that were sent are changed
def update_entry(
    db: Session, entry: Entry, scout: Scout, body: EntryUpdate
) -> Entry:
    assert_scout_can_change(entry, scout)
    changes = body.model_dump(exclude_unset=True)
    if changes.get("entry_date") is not None:
        entry.entry_date = changes["entry_date"]
    if "note" in changes:
        entry.note = changes["note"]
    db.commit()
    db.refresh(entry)
    return entry


# Deletes a pending entry
def delete_entry(db: Session, entry: Entry, scout: Scout) -> None:
    assert_scout_can_change(entry, scout)
    db.delete(entry)
    db.commit()


# Marks an entry confirmed by a Leader from the same troop as the Scout
def confirm_entry(db: Session, entry: Entry, leader_profile_id: uuid.UUID) -> Entry:
    scout = db.get(Scout, entry.scout_id)
    assert_leader_leads_scout(db, leader_profile_id, scout)
    entry.status = EntryStatus.Confirmed
    entry.confirmed_by = leader_profile_id
    entry.confirmed_at = datetime.now(UTC)
    db.commit()
    db.refresh(entry)
    return entry
