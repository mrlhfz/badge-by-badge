import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, UUIDPk


class Level(UUIDPk, Base):
    __tablename__ = "levels"

    name: Mapped[str] = mapped_column(unique=True)
    sort_order: Mapped[int] = mapped_column(unique=True)
    top_award: Mapped[str]


class Stream(UUIDPk, Base):
    __tablename__ = "streams"

    name: Mapped[str] = mapped_column(unique=True)


class LevelStream(Base):
    __tablename__ = "level_streams"

    level_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("levels.id"), primary_key=True
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("streams.id"), primary_key=True
    )
