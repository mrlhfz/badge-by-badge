import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..enums import PinKind, Role
from .base import Base, CreatedAt, UUIDPk


class Profile(CreatedAt, Base):
    __tablename__ = "profiles"

    # FK to auth.users.id is added by hand in the migration (Alembic can't see the auth schema)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role", values_callable=lambda e: [m.value for m in e])
    )
    username: Mapped[str | None] = mapped_column(unique=True)
    full_name: Mapped[str | None]


class Pin(UUIDPk, CreatedAt, Base):
    __tablename__ = "pins"

    kind: Mapped[PinKind] = mapped_column(
        Enum(PinKind, name="pin_kind", values_callable=lambda e: [m.value for m in e])
    )
    code_hash: Mapped[str] = mapped_column(unique=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))
    scout_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("scouts.id"))
    claimed_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("profiles.id"))
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Troop(UUIDPk, CreatedAt, Base):
    __tablename__ = "troops"
    __table_args__ = (
        CheckConstraint("leaders_required >= 1", name="ck_troops_leaders_required"),
    )

    name: Mapped[str] = mapped_column(unique=True)
    leaders_required: Mapped[int]


class TroopLeader(UUIDPk, Base):
    __tablename__ = "troop_leaders"

    troop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("troops.id"), index=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id"), unique=True
    )
    assigned_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Scout(UUIDPk, CreatedAt, Base):
    __tablename__ = "scouts"

    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profiles.id"), unique=True
    )
    troop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("troops.id"), index=True)
    stream_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("streams.id"))
    full_name: Mapped[str]
    ppm_number: Mapped[str | None] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    is_verified: Mapped[bool] = mapped_column(server_default=text("false"))
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))
