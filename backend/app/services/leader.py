import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import ProgressStatus
from app.models.people import Scout, TroopLeader
from app.models.progress import Badge, Entry, Requirement
from app.schemas.leader import ScoutBadgeProgress, ScoutEntryOut, ScoutProgressOut
from app.services import progress


# The Scouts in the troop this Leader leads; an empty list if they lead no troop
def troop_scouts(db: Session, leader_profile_id: uuid.UUID) -> list[Scout]:
    troop_id = db.scalar(
        select(TroopLeader.troop_id).where(TroopLeader.profile_id == leader_profile_id)
    )
    if troop_id is None:
        return []
    return list(
        db.scalars(
            select(Scout).where(Scout.troop_id == troop_id).order_by(Scout.full_name)
        ).all()
    )


# One Scout's badge progress on their current level, and every entry they have made
def scout_progress(db: Session, scout: Scout) -> ScoutProgressOut:
    level_id = progress.current_level_id(db, scout)
    badges = progress.visible_badges(db, scout, level_id) if level_id is not None else []
    statuses = progress.badge_statuses(db, scout, badges)

    rows = db.execute(
        select(Entry, Requirement.text, Badge.name)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .join(Badge, Badge.id == Requirement.badge_id)
        .where(Entry.scout_id == scout.id)
        .order_by(Entry.entry_date)
    ).all()

    return ScoutProgressOut(
        scout_id=scout.id,
        full_name=scout.full_name,
        complete=sum(1 for s in statuses.values() if s == ProgressStatus.Complete),
        total=len(badges),
        badges=[
            ScoutBadgeProgress(id=b.id, name=b.name, status=statuses[b.id]) for b in badges
        ],
        entries=[
            ScoutEntryOut(
                id=entry.id,
                badge_name=badge_name,
                requirement_text=requirement_text,
                entry_date=entry.entry_date,
                note=entry.note,
                status=entry.status,
            )
            for entry, requirement_text, badge_name in rows
        ],
    )
