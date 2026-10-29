from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalog import Level, Stream
from app.models.people import Scout
from app.schemas.me import MeOut
from app.services import progress


# The Scout's name, current level, stream and verification state
def my_profile(db: Session, scout: Scout) -> MeOut:
    level_id = progress.current_level_id(db, scout)
    level_name = (
        db.scalar(select(Level.name).where(Level.id == level_id)) if level_id else None
    )
    stream_name = db.scalar(select(Stream.name).where(Stream.id == scout.stream_id))
    return MeOut(
        full_name=scout.full_name,
        level_name=level_name,
        stream_name=stream_name,
        is_verified=scout.is_verified,
    )
