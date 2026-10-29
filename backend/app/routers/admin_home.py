from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.enums import Role
from app.schemas.admin_home import AdminHomeOut
from app.services import admin_home as home_service

# One guard on the router covers every route, so a route added later can't forget it
router = APIRouter(
    prefix="/admin/home",
    tags=["admin home"],
    dependencies=[Depends(require_role(Role.Admin))],
)


# Admin: the counts and recent verification changes for the Admin home page
@router.get("", response_model=AdminHomeOut)
def get_admin_home(db: Annotated[Session, Depends(get_db)]):
    return home_service.get_admin_home(db)
