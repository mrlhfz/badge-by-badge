from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.people import Scout
from app.schemas.tanda import TandaOut
from app.services import progress, tanda
from app.services.scouts import get_current_scout

router = APIRouter(prefix="/tanda", tags=["tanda"])


# Scout: where they stand for the Tanda Cemerlang
@router.get("/current", response_model=TandaOut)
def get_current_tanda(
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    level_id = progress.current_level_id(db, scout)
    result = tanda.tanda_for_scout(db, scout, level_id, date.today())
    return TandaOut(
        state=result.state,
        required=result.required,
        missing=result.missing,
        held_since=result.held_since,
        eligible_on=result.eligible_on,
        months_required=tanda.TANDA_MONTHS,
    )
