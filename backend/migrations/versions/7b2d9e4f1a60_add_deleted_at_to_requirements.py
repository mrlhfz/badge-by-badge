"""add deleted_at to requirements, so removed requirements are hidden but keep their entries

Revision ID: 7b2d9e4f1a60
Revises: f3a8b2c1d9e4
Create Date: 2026-10-27 18:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "7b2d9e4f1a60"
down_revision: str | Sequence[str] | None = "f3a8b2c1d9e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Null means the requirement is live; a timestamp means it was removed
    op.add_column(
        "requirements",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("requirements", "deleted_at")
