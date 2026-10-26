"""remove the Jaya Kumpulan IV (Masyarakat) requirement, which the book does not print

Revision ID: b3d8f0a6c17e
Revises: a9c3e7d1f25b
Create Date: 2026-10-25 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3d8f0a6c17e"
down_revision: str | Sequence[str] | None = "a9c3e7d1f25b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

MASYARAKAT_TEXT = "Kumpulan IV: Masyarakat"
MASYARAKAT_DETAIL = (
    "Menyedia, memasak dan melayan; pertunjukkan hiburan amatur; "
    "perkhidmatan dan menjalankan malam pengakap."
)


def upgrade() -> None:
    op.execute(
        sa.text("""
            delete from requirements r
            using badges b
            where b.id = r.badge_id
              and b.name = 'Lencana Jaya'
              and r.text = :text
        """).bindparams(text=MASYARAKAT_TEXT)
    )


def downgrade() -> None:
    # Put the row back in the same group as the Kemahiran row (position 16), at position 15.
    op.execute(
        sa.text("""
            insert into requirements (badge_id, stream_id, group_id, position, text, detail)
            select b.id, null, kemahiran.group_id, 15, :text, :detail
            from badges b
            join requirements kemahiran
              on kemahiran.badge_id = b.id and kemahiran.position = 16
            where b.name = 'Lencana Jaya'
        """).bindparams(text=MASYARAKAT_TEXT, detail=MASYARAKAT_DETAIL)
    )
