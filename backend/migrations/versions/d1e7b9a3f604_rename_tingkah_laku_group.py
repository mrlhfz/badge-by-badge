"""rename the Ahli Anti-Dadah group Tingkahlaku to the standard spelling Tingkah laku

Revision ID: d1e7b9a3f604
Revises: 9e4b1d7a6c02
Create Date: 2026-10-26 01:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1e7b9a3f604"
down_revision: str | Sequence[str] | None = "9e4b1d7a6c02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

OLD_TITLE = "Tahap 1 Unit II: Tingkahlaku negatif"
NEW_TITLE = "Tahap 1 Unit II: Tingkah laku negatif"


def _rename(old_title: str, new_title: str) -> None:
    op.execute(
        sa.text("""
            update requirement_groups g
            set title = :new_title
            from badges b
            where b.id = g.badge_id
              and b.name = 'Ahli Anti-Dadah'
              and g.title = :old_title
        """).bindparams(old_title=old_title, new_title=new_title)
    )


def upgrade() -> None:
    _rename(OLD_TITLE, NEW_TITLE)


def downgrade() -> None:
    _rename(NEW_TITLE, OLD_TITLE)
