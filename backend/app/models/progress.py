import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..enums import BadgeKind, EntryStatus, VerificationAction
from .base import Base, CreatedAt, UUIDPk


class ScoutLevel(UUIDPk, Base):
    __tablename__ = "scout_levels"
    __table_args__ = (
        Index(
            "uq_scout_levels_current",
            "scout_id",
            unique=True,
            postgresql_where=text("ended_at is null"),
        ),
    )

    scout_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scouts.id"))
    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("levels.id"))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    set_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))


class Badge(UUIDPk, Base):
    __tablename__ = "badges"

    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("levels.id"))
    stream_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("streams.id"))
    name: Mapped[str]
    description: Mapped[str]
    sort_order: Mapped[int]
    kind: Mapped[BadgeKind] = mapped_column(
        Enum(
            BadgeKind, name="badge_kind", values_callable=lambda e: [m.value for m in e]
        )
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RequirementGroup(UUIDPk, Base):
    __tablename__ = "requirement_groups"
    __table_args__ = (
        UniqueConstraint("badge_id", "position", name="uq_requirement_groups_badge_position"),
        CheckConstraint("pick_count >= 1", name="ck_requirement_groups_pick_count"),
    )

    badge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("badges.id"))
    title: Mapped[str]
    pick_count: Mapped[int]
    position: Mapped[int]


class Requirement(UUIDPk, Base):
    __tablename__ = "requirements"
    __table_args__ = (
        UniqueConstraint("badge_id", "position", name="uq_requirements_badge_position"),
    )

    badge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("badges.id"))
    stream_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("streams.id"))
    group_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("requirement_groups.id")
    )
    position: Mapped[int]
    text: Mapped[str]
    detail: Mapped[str | None]

class RequiredSkillCount(Base):
    __tablename__ = "required_skill_counts"
    __table_args__ = (
        CheckConstraint(
            "required_count >= 0", name="ck_required_skill_counts_required_count"
        ),
    )

    level_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("levels.id"), primary_key=True
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("streams.id"), primary_key=True
    )
    required_count: Mapped[int]


class Entry(UUIDPk, CreatedAt, Base):
    __tablename__ = "entries"
    __table_args__ = (
        UniqueConstraint(
            "scout_id", "requirement_id", name="uq_entries_scout_requirement"
        ),
    )

    scout_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scouts.id"))
    requirement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("requirements.id"))
    entry_date: Mapped[Date] = mapped_column(Date)
    note: Mapped[str | None]
    status: Mapped[EntryStatus] = mapped_column(
        Enum(
            EntryStatus,
            name="entry_status",
            values_callable=lambda e: [m.value for m in e],
        ),
        server_default="pending",
    )
    confirmed_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("profiles.id"))
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class EntryComment(UUIDPk, CreatedAt, Base):
    __tablename__ = "entry_comments"

    entry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entries.id"))
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))
    body: Mapped[str]


class VerificationEvent(UUIDPk, CreatedAt, Base):
    __tablename__ = "verification_events"

    scout_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scouts.id"))
    action: Mapped[VerificationAction] = mapped_column(
        Enum(
            VerificationAction,
            name="verification_action",
            values_callable=lambda e: [m.value for m in e],
        )
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.id"))
