import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


# One requirement on a badge, as the Admin sees it; removed ones are included, with their time
class RequirementAdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    badge_id: uuid.UUID
    position: int
    text: str
    detail: str | None
    group_id: uuid.UUID | None
    stream_id: uuid.UUID | None
    deleted_at: datetime | None


# What the Admin sends to add a requirement to a badge
class RequirementCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    detail: str | None = Field(default=None, max_length=1000)
    group_id: uuid.UUID | None = None
    stream_id: uuid.UUID | None = None


# What the Admin sends to change a requirement; only the fields that are sent are changed
class RequirementUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=500)
    detail: str | None = Field(default=None, max_length=1000)
    group_id: uuid.UUID | None = None
    stream_id: uuid.UUID | None = None

    # The text can be left out, but it can't be sent as null: a requirement always has its text
    @field_validator("text")
    @classmethod
    def text_is_not_null(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("text cannot be null")
        return value
