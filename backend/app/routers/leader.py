import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user_id, require_role
from app.database import get_db
from app.enums import Role
from app.models.people import Scout
from app.schemas.comments import CommentCreate, CommentOut
from app.schemas.leader import (
    LeaderScoutOut,
    LeaderSummaryOut,
    LogEntryOut,
    PendingEntryOut,
    ScoutProgressOut,
)
from app.services import comments as comment_service
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


# Leader: how many Scouts they lead, and how many entries wait for confirmation
@router.get("/summary", response_model=LeaderSummaryOut)
def get_summary(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return leader_service.troop_summary(db, uuid.UUID(user_id))


# Leader: every pending entry in the troop, so they can confirm them in one place
@router.get("/entries/pending", response_model=list[PendingEntryOut])
def list_pending_entries(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return leader_service.pending_entries(db, uuid.UUID(user_id))


# Leader: the entries they confirmed, with their comments
@router.get("/log", response_model=list[LogEntryOut])
def list_log(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return leader_service.leader_log(db, uuid.UUID(user_id))


# Leader: add a comment to an entry, only for a Scout in their troop
@router.post(
    "/entries/{entry_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def add_entry_comment(
    entry_id: uuid.UUID,
    body: CommentCreate,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    entry = entry_service.get_entry_or_404(db, entry_id)
    return comment_service.add_comment(db, entry, uuid.UUID(user_id), body.body)


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
