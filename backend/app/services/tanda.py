import calendar
import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import ProgressStatus, TandaState
from app.models.catalog import Stream
from app.models.people import Scout
from app.models.progress import Badge, Entry, Requirement
from app.services.progress import badge_status

# How long the badges must be held before the Tanda can be awarded
TANDA_MONTHS = 3

# The Laut stream must hold Jaya and Juragan; the Darat path needs only Jaya
LAUT_REQUIRED = ["Lencana Jaya", "Lencana Juragan"]
DARAT_REQUIRED = ["Lencana Jaya"]


# Adds whole months to a date, keeping the day if the month is long enough
def add_months(start: date, months: int) -> date:
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


@dataclass(frozen=True)
class TandaResult:
    state: TandaState
    required: list[str]
    missing: list[str]
    held_since: date | None
    eligible_on: date | None


# Decides the Tanda state from the completion date of each required badge (None if not complete)
def evaluate(completed_on: dict[str, date | None], today: date) -> TandaResult:
    required = list(completed_on)
    missing = [name for name in required if completed_on[name] is None]
    if missing:
        return TandaResult(TandaState.NotYet, required, missing, None, None)

    # Every required badge must be held for the full time, so the last one to complete sets the start
    held_since = max(d for d in completed_on.values() if d is not None)
    eligible_on = add_months(held_since, TANDA_MONTHS)
    state = TandaState.Eligible if today >= eligible_on else TandaState.Waiting
    return TandaResult(state, required, [], held_since, eligible_on)


# The date a badge was completed: the latest confirmation on its entries, if it's complete now
def completed_on(db: Session, scout: Scout, badge_id: uuid.UUID) -> date | None:
    if badge_status(db, scout, badge_id) != ProgressStatus.Complete:
        return None
    latest = db.scalar(
        select(func.max(Entry.confirmed_at))
        .join(Requirement, Requirement.id == Entry.requirement_id)
        .where(Entry.scout_id == scout.id, Requirement.badge_id == badge_id)
    )
    return latest.date() if latest else None


# The Tanda state for one Scout, using their stream and their current level
def tanda_for_scout(
    db: Session, scout: Scout, level_id: uuid.UUID | None, today: date
) -> TandaResult:
    stream = db.get(Stream, scout.stream_id)
    is_laut = stream is not None and stream.name == "Pengakap Laut"
    names = LAUT_REQUIRED if is_laut else DARAT_REQUIRED

    dates: dict[str, date | None] = {}
    for name in names:
        badge = None
        if level_id is not None:
            badge = db.scalar(
                select(Badge).where(
                    Badge.level_id == level_id,
                    Badge.name == name,
                    Badge.deleted_at.is_(None),
                )
            )
        dates[name] = completed_on(db, scout, badge.id) if badge else None
    return evaluate(dates, today)
