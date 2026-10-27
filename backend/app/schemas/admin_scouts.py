import uuid

from pydantic import BaseModel, ConfigDict

from app.enums import VerificationAction


# One Scout, as the Admin sees them, with whether they are verified
class AdminScoutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    is_verified: bool


# What the Admin sends to verify or unverify a Scout
class VerificationIn(BaseModel):
    action: VerificationAction
