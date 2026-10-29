import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import EntryStatus, ProgressStatus
from app.models.people import Profile, Scout, TroopLeader
from app.models.progress import Badge, Entry, Requirement
from app.schemas.comments import CommentOut
from app.schemas.leader import (
    LeaderSummaryOut,
    LogEntryOut,
    PendingEntryOut,
    ScoutBadgeProgress,
    ScoutEntryOut,
    ScoutProgressOut,
)
from app.services import progress
from app.services.comments import comments_by_entry


# The Scouts in the troop this Leader leads; an empty list if they lead no troop
def troop_scouts(db: Session, leader_profile_id: uuid.UUID) -> list[Scout]:
    troop_id = _troop_id_for(db, leader_profile_id)
    if troop_id is None:
        return []
    return list(
        db.scalars(
            select(Scout).where(Scout.troop_id == troop_id).order_by(Scout.full_name)
        ).all()
    )


# The troop this Leader leads, or None if they lead no troop
def _troop_id_for(db: Session, leader_profile_id: uuid.UUID) -> uuid.UUID | None:
    return db.scalar(
        select(TroopLeader.troop_id).where(TroopLeader.profile_id == leader_profile_id)
    )


# How many Scouts the Leader leads, and how many of their entries await confirmation
def troop_summary(db: Session, leader_profile_id: uuid.UUID) -> LeaderSummaryOut:
    profile = db.get(Profile, leader_profile_id)
    full_name = profile.full_name if profile else None
    troop_id = _troop_id_for(db, leader_profile_id)
    if troop_id is None:
        return LeaderSummaryOut(full_name=full_name, scout_count=0, pending_entries=0)
    scout_count = db.scalar(
        select(func.count(Scout.id)).where(Scout.troop_id == troop_id)
    )
    pending_entries = db.scalar(
        select(func.count(Entry.id))
        .join(Scout, Scout.id == Entry.scout_id)
        .where(Scout.troop_id == troop_id, Entry.status == EntryStatus.Pending)
    )
    return LeaderSummaryOut(
        full_name=full_name, scout_count=scout_count, pending_entries=pending_entries
    )


# The entries this Leader confirmed, newest first, each with its comments
def leader_log(db: Session, leader_profile_id: uuid.UUID) -> list[LogEntryOut]:
    rows = db.execute(
        select(Entry, Scout.full_name, Requirement.text, Badge.name)
        .join(Scout, Scout.id == Entry.scout_id)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .join(Badge, Badge.id == Requirement.badge_id)
        .where(
            Entry.confirmed_by == leader_profile_id,
            Entry.status == EntryStatus.Confirmed,
        )
        .order_by(Entry.confirmed_at.desc())
    ).all()
    return [
        LogEntryOut(
            id=entry.id,
            scout_id=entry.scout_id,
            scout_name=scout_name,
            badge_name=badge_name,
            requirement_text=requirement_text,
            entry_date=entry.entry_date,
            note=entry.note,
            confirmed_at=entry.confirmed_at,
        )
        for entry, scout_name, requirement_text, badge_name in rows
    ]


# Every pending entry in the Leader's troop, oldest first, so they can confirm them in one place
def pending_entries(db: Session, leader_profile_id: uuid.UUID) -> list[PendingEntryOut]:
    troop_id = _troop_id_for(db, leader_profile_id)
    if troop_id is None:
        return []
    rows = db.execute(
        select(Entry, Scout.full_name, Requirement.text, Badge.name)
        .join(Scout, Scout.id == Entry.scout_id)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .join(Badge, Badge.id == Requirement.badge_id)
        .where(Scout.troop_id == troop_id, Entry.status == EntryStatus.Pending)
        .order_by(Entry.entry_date)
    ).all()
    comments = comments_by_entry(db, [entry.id for entry, *_ in rows])
    return [
        PendingEntryOut(
            id=entry.id,
            scout_id=entry.scout_id,
            scout_name=scout_name,
            badge_name=badge_name,
            requirement_text=requirement_text,
            entry_date=entry.entry_date,
            note=entry.note,
            comments=[CommentOut.model_validate(c) for c in comments.get(entry.id, [])],
        )
        for entry, scout_name, requirement_text, badge_name in rows
    ]


# One Scout's badge progress on their current level, and every entry they have made
def scout_progress(db: Session, scout: Scout) -> ScoutProgressOut:
    level_id = progress.current_level_id(db, scout)
    badges = (
        progress.visible_badges(db, scout, level_id) if level_id is not None else []
    )
    statuses = progress.badge_statuses(db, scout, badges)

    rows = db.execute(
        select(Entry, Requirement.text, Badge.name)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .join(Badge, Badge.id == Requirement.badge_id)
        .where(Entry.scout_id == scout.id)
        .order_by(Entry.entry_date)
    ).all()

    comments = comments_by_entry(db, [entry.id for entry, *_ in rows])
    return ScoutProgressOut(
        scout_id=scout.id,
        full_name=scout.full_name,
        complete=sum(1 for s in statuses.values() if s == ProgressStatus.Complete),
        total=len(badges),
        badges=[
            ScoutBadgeProgress(id=b.id, name=b.name, status=statuses[b.id])
            for b in badges
        ],
        entries=[
            ScoutEntryOut(
                id=entry.id,
                badge_name=badge_name,
                requirement_text=requirement_text,
                entry_date=entry.entry_date,
                note=entry.note,
                status=entry.status,
                comments=[
                    CommentOut.model_validate(c) for c in comments.get(entry.id, [])
                ],
            )
            for entry, requirement_text, badge_name in rows
        ],
    )
