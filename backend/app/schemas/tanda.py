from datetime import date

from pydantic import BaseModel

from app.enums import TandaState


# The Scout's standing for the Tanda Cemerlang, for the card on the home page
class TandaOut(BaseModel):
    state: TandaState
    required: list[str]
    missing: list[str]
    held_since: date | None
    eligible_on: date | None
    months_required: int
