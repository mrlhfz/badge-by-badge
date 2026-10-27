import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums import EntryStatus


# What a Scout sends to mark a requirement done
class EntryCreate(BaseModel):
    requirement_id: uuid.UUID
    entry_date: date
    note: str | None = Field(default=None, max_length=500)


# What a Scout sends to change an entry; only the fields that are sent are changed.
# The date can be left out, but it can't be sent as null, because an entry always has a date.
class EntryUpdate(BaseModel):
    entry_date: date | None = None
    note: str | None = Field(default=None, max_length=500)

    @field_validator("entry_date")
    @classmethod
    def date_is_not_null(cls, value: date | None) -> date | None:
        if value is None:
            raise ValueError("entry_date cannot be null")
        return value


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
