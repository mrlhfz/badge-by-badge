import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import EntryStatus


# What a Scout sends to mark a requirement done
class EntryCreate(BaseModel):
    requirement_id: uuid.UUID
    entry_date: date
    note: str | None = Field(default=None, max_length=500)


# What a Scout sends to change an entry; only the fields that are sent are changed
class EntryUpdate(BaseModel):
    entry_date: date | None = None
    note: str | None = Field(default=None, max_length=500)


# What the API returns for an entry
class EntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    scout_id: uuid.UUID
    requirement_id: uuid.UUID
    entry_date: date
    note: str | None
    status: EntryStatus
    confirmed_at: datetime | None
