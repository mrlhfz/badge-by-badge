import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user_id
from app.database import get_db
from app.models.people import Scout


# Finds the Scout record linked to the signed-in user; 403 if there is none
def get_current_scout(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> Scout:
    try:
        profile_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    scout = db.scalar(select(Scout).where(Scout.profile_id == profile_id))
    if scout is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No scout record for this user",
        )
    return scout
