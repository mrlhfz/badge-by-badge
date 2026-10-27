import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.enums import EntryStatus, ProgressStatus
from app.schemas.comments import CommentOut


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
    comments: list[CommentOut]


# One Scout's progress: the count of complete badges, each badge, and every entry
class ScoutProgressOut(BaseModel):
    scout_id: uuid.UUID
    full_name: str
    complete: int
    total: int
    badges: list[ScoutBadgeProgress]
    entries: list[ScoutEntryOut]


# The Leader's home summary: how many Scouts they lead, and how many entries await confirmation
class LeaderSummaryOut(BaseModel):
    full_name: str | None
    scout_count: int
    pending_entries: int


# One entry the Leader confirmed, with its comments, for the Leader's log
class LogEntryOut(BaseModel):
    id: uuid.UUID
    scout_id: uuid.UUID
    scout_name: str
    badge_name: str
    requirement_text: str
    entry_date: date
    note: str | None
    confirmed_at: datetime | None


# One entry waiting for the Leader's confirmation, with the Scout's name so the Leader knows whose it is
class PendingEntryOut(BaseModel):
    id: uuid.UUID
    scout_id: uuid.UUID
    scout_name: str
    badge_name: str
    requirement_text: str
    entry_date: date
    note: str | None
    comments: list[CommentOut]
