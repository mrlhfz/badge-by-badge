from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.people import Scout
from app.schemas.me import MeOut
from app.services import me as me_service
from app.services.scouts import get_current_scout

router = APIRouter(prefix="/me", tags=["me"])


# Scout: the signed-in Scout's own details
@router.get("", response_model=MeOut)
def get_me(
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    return me_service.my_profile(db, scout)
