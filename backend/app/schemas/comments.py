import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# What a Leader sends to comment on an entry
class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=500)


# One comment on an entry, as the API returns it
class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    entry_id: uuid.UUID
    body: str
    created_at: datetime
