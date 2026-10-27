import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user_id, require_role
from app.database import get_db
from app.enums import Role
from app.models.people import Scout
from app.schemas.entries import EntryCreate, EntryOut, EntryUpdate
from app.services import entries as entry_service
from app.services.scouts import get_current_scout

router = APIRouter(prefix="/entries", tags=["entries"])

# Paging for list endpoints: at most 100 rows per page, 50 by default
LimitParam = Annotated[int, Query(ge=1, le=100)]
OffsetParam = Annotated[int, Query(ge=0)]


# Scout: list their own entries, one page at a time
@router.get("/mine", response_model=list[EntryOut])
def list_my_entries(
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
    limit: LimitParam = 50,
    offset: OffsetParam = 0,
):
    return entry_service.list_entries_for_scout(db, scout.id, limit, offset)


# Leader: list one scout's entries, only for a scout in their troop
@router.get(
    "/scout/{scout_id}",
    response_model=list[EntryOut],
    dependencies=[Depends(require_role(Role.Leader))],
)
def list_scout_entries(
    scout_id: uuid.UUID,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    limit: LimitParam = 50,
    offset: OffsetParam = 0,
):
    scout = db.get(Scout, scout_id)
    if scout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found",
        )
    entry_service.assert_leader_leads_scout(db, uuid.UUID(user_id), scout)
    return entry_service.list_entries_for_scout(db, scout.id, limit, offset)


# Scout: mark a requirement done with a date and a note
@router.post("", response_model=EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(
    body: EntryCreate,
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    return entry_service.create_entry(db, scout, body)


# Scout: edit their own pending entry
@router.patch("/{entry_id}", response_model=EntryOut)
def update_entry(
    entry_id: uuid.UUID,
    body: EntryUpdate,
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    entry = entry_service.get_entry_or_404(db, entry_id)
    return entry_service.update_entry(db, entry, scout, body)


# Scout: delete their own pending entry
@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: uuid.UUID,
    scout: Annotated[Scout, Depends(get_current_scout)],
    db: Annotated[Session, Depends(get_db)],
):
    entry = entry_service.get_entry_or_404(db, entry_id)
    entry_service.delete_entry(db, entry, scout)


# Leader: confirm an entry for a scout in their troop
@router.post(
    "/{entry_id}/confirm",
    response_model=EntryOut,
    dependencies=[Depends(require_role(Role.Leader))],
)
def confirm_entry(
    entry_id: uuid.UUID,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    entry = entry_service.get_entry_or_404(db, entry_id)
    return entry_service.confirm_entry(db, entry, uuid.UUID(user_id))
