from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.people import Scout
from app.models.progress import Badge, VerificationEvent
from app.schemas.admin_home import AdminHomeOut, RecentVerificationOut

# How many recent verification changes the Admin home lists
RECENT_LIMIT = 5


# Counts for the Admin home, plus the latest verify and unverify actions
def get_admin_home(db: Session) -> AdminHomeOut:
    # Scouts who are not verified yet
    unverified_scouts = db.scalar(
        select(func.count()).select_from(Scout).where(Scout.is_verified.is_(False))
    )
    # Badges that have not been removed (soft-deleted ones don't count)
    badge_count = db.scalar(
        select(func.count()).select_from(Badge).where(Badge.deleted_at.is_(None))
    )
    # The newest events first, with the Scout's name joined in
    rows = db.execute(
        select(Scout.full_name, VerificationEvent.action, VerificationEvent.created_at)
        .join(Scout, Scout.id == VerificationEvent.scout_id)
        .order_by(VerificationEvent.created_at.desc())
        .limit(RECENT_LIMIT)
    ).all()
    return AdminHomeOut(
        unverified_scouts=unverified_scouts,
        badge_count=badge_count,
        recent_verifications=[
            RecentVerificationOut(scout_name=name, action=action, created_at=created_at)
            for name, action, created_at in rows
        ],
    )
