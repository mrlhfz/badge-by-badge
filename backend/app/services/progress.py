import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.enums import AnimalKind, EntryStatus, ProgressStatus
from app.models.people import Scout
from app.models.progress import Badge, Entry, Requirement, RequirementGroup, ScoutLevel
from app.services.badge_rules import RuleGroup, RuleRequirement, badge_is_complete
from app.services.path_rules import PathBadge


# The level a Scout is on right now, or None if they have no current level
def current_level_id(db: Session, scout: Scout) -> uuid.UUID | None:
    return db.scalar(
        select(ScoutLevel.level_id).where(
            ScoutLevel.scout_id == scout.id,
            ScoutLevel.ended_at.is_(None),
        )
    )


# Does this Scout keep poultry? An entry for this badge marked poultry says so
def keeps_poultry(db: Session, scout_id: uuid.UUID, badge_id: uuid.UUID) -> bool:
    found = db.scalar(
        select(Entry.id)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .where(
            Entry.scout_id == scout_id,
            Requirement.badge_id == badge_id,
            Entry.animal_kind == AnimalKind.Poultry,
        )
        .limit(1)
    )
    return found is not None


# Loads a badge's requirements and groups in the shape the completion rule expects
def rule_inputs(
    db: Session, badge_id: uuid.UUID
) -> tuple[list[RuleRequirement], list[RuleGroup]]:
    requirements = db.scalars(
        select(Requirement).where(Requirement.badge_id == badge_id)
    ).all()
    groups = db.scalars(
        select(RequirementGroup).where(RequirementGroup.badge_id == badge_id)
    ).all()
    return (
        [RuleRequirement(r.id, r.group_id, r.stream_id) for r in requirements],
        [
            RuleGroup(g.id, g.parent_group_id, g.pick_count, g.applies_when_poultry)
            for g in groups
        ],
    )


# Works out one badge's progress status for one Scout
def badge_status(db: Session, scout: Scout, badge_id: uuid.UUID) -> ProgressStatus:
    # Any entry, pending or confirmed, means the Scout has started
    entries = db.scalars(
        select(Entry)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .where(Entry.scout_id == scout.id, Requirement.badge_id == badge_id)
    ).all()
    if not entries:
        return ProgressStatus.NotStarted

    # Only confirmed entries count toward completion
    confirmed = {e.requirement_id for e in entries if e.status == EntryStatus.Confirmed}
    requirements, groups = rule_inputs(db, badge_id)
    complete = badge_is_complete(
        requirements,
        groups,
        confirmed,
        scout.stream_id,
        keeps_poultry(db, scout.id, badge_id),
    )
    return ProgressStatus.Complete if complete else ProgressStatus.InProgress


# The requirements a Scout sees on a badge: general ones and ones for their stream
def requirements_for_scout(
    db: Session, scout: Scout, badge_id: uuid.UUID
) -> list[Requirement]:
    return list(
        db.scalars(
            select(Requirement)
            .where(
                Requirement.badge_id == badge_id,
                Requirement.deleted_at.is_(None),
                or_(
                    Requirement.stream_id.is_(None),
                    Requirement.stream_id == scout.stream_id,
                ),
            )
            .order_by(Requirement.position)
        ).all()
    )


# The Scout's own entries for a badge, keyed by requirement, so the detail page can show them
def entries_by_requirement(
    db: Session, scout: Scout, badge_id: uuid.UUID
) -> dict[uuid.UUID, Entry]:
    entries = db.scalars(
        select(Entry)
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .where(Entry.scout_id == scout.id, Requirement.badge_id == badge_id)
    ).all()
    return {e.requirement_id: e for e in entries}


# Loads a badge's groups, for the checklist sections
def groups_for_badge(db: Session, badge_id: uuid.UUID) -> list[RequirementGroup]:
    return list(
        db.scalars(
            select(RequirementGroup)
            .where(RequirementGroup.badge_id == badge_id)
            .order_by(RequirementGroup.position)
        ).all()
    )


# Loads a badge, or None if it's missing or deleted
def live_badge(db: Session, badge_id: uuid.UUID) -> Badge | None:
    badge = db.get(Badge, badge_id)
    if badge is None or badge.deleted_at is not None:
        return None
    return badge


# The badges on a level that this Scout can see, in display order
def visible_badges(db: Session, scout: Scout, level_id: uuid.UUID) -> list[Badge]:
    return list(
        db.scalars(
            select(Badge)
            .where(
                Badge.level_id == level_id,
                Badge.deleted_at.is_(None),
                or_(Badge.stream_id.is_(None), Badge.stream_id == scout.stream_id),
            )
            .order_by(Badge.sort_order)
        ).all()
    )


# Each badge's status for this Scout, worked out once per badge
def badge_statuses(
    db: Session, scout: Scout, badges: list[Badge]
) -> dict[uuid.UUID, ProgressStatus]:
    return {badge.id: badge_status(db, scout, badge.id) for badge in badges}


# The path the Scout sees, built from badges whose statuses are already known
def path_from(
    badges: list[Badge], statuses: dict[uuid.UUID, ProgressStatus]
) -> list[PathBadge]:
    return [
        PathBadge(
            id=badge.id,
            name=badge.name,
            row=badge.path_row,
            complete=statuses[badge.id] == ProgressStatus.Complete,
        )
        for badge in badges
        if badge.path_row is not None
    ]
