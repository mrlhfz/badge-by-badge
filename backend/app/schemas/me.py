from pydantic import BaseModel


# The signed-in Scout's own details, for the greeting on the My Badges screen
class MeOut(BaseModel):
    full_name: str
    level_name: str | None
    stream_name: str | None
    is_verified: bool
