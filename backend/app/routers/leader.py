import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user_id, require_role
from app.database import get_db
from app.enums import Role
from app.models.people import Scout
from app.schemas.leader import LeaderScoutOut, ScoutProgressOut
from app.services import entries as entry_service
from app.services import leader as leader_service

# One guard on the router covers every route, so a route added later can't forget it
router = APIRouter(
    prefix="/leader",
    tags=["leader"],
    dependencies=[Depends(require_role(Role.Leader))],
)


# Leader: the Scouts in the troop they lead
@router.get("/troop/scouts", response_model=list[LeaderScoutOut])
def list_troop_scouts(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return leader_service.troop_scouts(db, uuid.UUID(user_id))


# Leader: one Scout's progress and entries, only for a Scout in their troop
@router.get("/scouts/{scout_id}/progress", response_model=ScoutProgressOut)
def get_scout_progress(
    scout_id: uuid.UUID,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    scout = db.get(Scout, scout_id)
    if scout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found",
        )
    entry_service.assert_leader_leads_scout(db, uuid.UUID(user_id), scout)
    return leader_service.scout_progress(db, scout)
