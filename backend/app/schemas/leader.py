import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.enums import EntryStatus, ProgressStatus


# A Scout in the Leader's troop
class LeaderScoutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    stream_id: uuid.UUID


# One badge on the Scout's current level, with its status
class ScoutBadgeProgress(BaseModel):
    id: uuid.UUID
    name: str
    status: ProgressStatus


# One entry the Scout has made, with the words the Leader needs to judge it
class ScoutEntryOut(BaseModel):
    id: uuid.UUID
    badge_name: str
    requirement_text: str
    entry_date: date
    note: str | None
    status: EntryStatus


# One Scout's progress: the count of complete badges, each badge, and every entry
class ScoutProgressOut(BaseModel):
    scout_id: uuid.UUID
    full_name: str
    complete: int
    total: int
    badges: list[ScoutBadgeProgress]
    entries: list[ScoutEntryOut]
