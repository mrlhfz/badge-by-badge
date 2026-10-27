import uuid

from pydantic import BaseModel

from app.enums import ProgressStatus
from app.schemas.comments import CommentOut
from app.schemas.entries import EntryOut


# One badge on the Scout's current level, with its progress status and place on the path
class BadgeListItem(BaseModel):
    id: uuid.UUID
    name: str
    status: ProgressStatus
    row: int | None = None
    locked: bool = False


# One requirement on a badge, with the Scout's own entry for it if there is one
class RequirementOut(BaseModel):
    id: uuid.UUID
    text: str
    detail: str | None
    group_id: uuid.UUID | None
    entry: EntryOut | None
    # The Leader's comments on the Scout's entry, oldest first
    comments: list[CommentOut] = []


# A checklist section, such as "pick 2 of these 4"
class GroupOut(BaseModel):
    id: uuid.UUID
    title: str
    pick_count: int
    parent_group_id: uuid.UUID | None


# One badge with everything the detail page needs
class BadgeDetailOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    status: ProgressStatus
    groups: list[GroupOut]
    requirements: list[RequirementOut]
