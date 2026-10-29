import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import VerificationAction
from app.models.people import Scout
from app.models.progress import VerificationEvent


# Every Scout, by name, for the Admin's list
def list_scouts(db: Session) -> list[Scout]:
    return list(db.scalars(select(Scout).order_by(Scout.full_name)).all())


# Sets a Scout's verified flag and records which Admin did it, so every change leaves a trail
def set_verified(
    db: Session,
    scout_id: uuid.UUID,
    action: VerificationAction,
    admin_profile_id: uuid.UUID,
) -> Scout:
    scout = db.get(Scout, scout_id)
    if scout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found",
        )
    scout.is_verified = action == VerificationAction.Verify
    db.add(
        VerificationEvent(scout_id=scout.id, action=action, actor_id=admin_profile_id)
    )
    db.commit()
    db.refresh(scout)
    return scout
