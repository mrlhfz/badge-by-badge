import uuid
from datetime import datetime

from pydantic import BaseModel

from app.enums import VerificationAction


# One recent verify or unverify, with the Scout's name so the Admin can see who it was.
# The event id is unique, so the frontend can use it as a list key.
class RecentVerificationOut(BaseModel):
    id: uuid.UUID
    scout_name: str
    action: VerificationAction
    created_at: datetime


# What the Admin home shows: how many Scouts wait, how many badges exist, and the latest changes
class AdminHomeOut(BaseModel):
    unverified_scouts: int
    badge_count: int
    recent_verifications: list[RecentVerificationOut]
