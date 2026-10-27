import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums import BadgeKind


# What an Admin sends to create a badge
class BadgeCreate(BaseModel):
    level_id: uuid.UUID
    stream_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(max_length=1000)
    sort_order: int
    kind: BadgeKind
    path_row: int | None = Field(default=None, ge=1, le=7)


# What an Admin sends to change a badge; only the fields that are sent are changed
class BadgeUpdate(BaseModel):
    level_id: uuid.UUID | None = None
    stream_id: uuid.UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    sort_order: int | None = None
    kind: BadgeKind | None = None
    path_row: int | None = Field(default=None, ge=1, le=7)

    # These fields can be left out, but never sent as null: the database needs a value
    @field_validator("level_id", "name", "description", "sort_order", "kind")
    @classmethod
    def required_fields_are_not_null(cls, value):
        if value is None:
            raise ValueError("this field cannot be null")
        return value


# What the Admin API returns for a badge, including soft-deleted ones
class BadgeAdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    level_id: uuid.UUID
    stream_id: uuid.UUID | None
    name: str
    description: str
    sort_order: int
    kind: BadgeKind
    path_row: int | None
    deleted_at: datetime | None
