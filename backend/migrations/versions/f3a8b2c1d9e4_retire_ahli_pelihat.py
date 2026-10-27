"""retire duplicate Ahli Pelihat badge

Revision ID: f3a8b2c1d9e4
Revises: e4d1c7a9b2f3
Create Date: 2026-10-27 13:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3a8b2c1d9e4"
down_revision: str | Sequence[str] | None = "e4d1c7a9b2f3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# The book lists "Pelihat", so the extra "Ahli Pelihat" row is soft-deleted, not removed
LEVEL_NAME = "Pengakap Muda"


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            update badges set deleted_at = now()
            where name = 'Ahli Pelihat'
              and level_id = (select id from levels where name = :level)
            """
        ).bindparams(level=LEVEL_NAME)
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            update badges set deleted_at = null
            where name = 'Ahli Pelihat'
              and level_id = (select id from levels where name = :level)
            """
        ).bindparams(level=LEVEL_NAME)
    )
