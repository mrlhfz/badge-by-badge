"""rename the Muda general badge Juru Perpustakaan to Pustakawan

Revision ID: a9c3e7d1f25b
Revises: f1a7c4e95d32
Create Date: 2026-10-25 17:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a9c3e7d1f25b"
down_revision: str | Sequence[str] | None = "f1a7c4e95d32"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _rename(old_name: str, new_name: str) -> None:
    op.execute(
        sa.text("""
            update badges
            set name = :new_name
            where name = :old_name
              and level_id = (select id from levels where name = 'Pengakap Muda')
              and stream_id is null
        """).bindparams(old_name=old_name, new_name=new_name)
    )


def upgrade() -> None:
    _rename("Juru Perpustakaan", "Pustakawan")


def downgrade() -> None:
    _rename("Pustakawan", "Juru Perpustakaan")
