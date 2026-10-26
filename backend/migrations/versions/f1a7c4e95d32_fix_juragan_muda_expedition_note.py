"""add the log book note to Juragan Muda expedition requirement

Revision ID: f1a7c4e95d32
Revises: e8f3a6c2b019
Create Date: 2026-10-25 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1a7c4e95d32"
down_revision: str | Sequence[str] | None = "e8f3a6c2b019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

NEW_DETAIL = (
    "Mengikuti satu ekspedisi memancing 2 hari 1 malam di bawah pengawasan orang dewasa "
    "dengan menyimpan rekod dan gambar ke dalam buku log."
)
OLD_DETAIL = "Mengikuti satu ekspedisi memancing 2 hari 1 malam di bawah pengawasan orang dewasa."


def _set_detail(detail: str) -> None:
    op.execute(
        sa.text("""
            update requirements r
            set detail = :detail
            from badges b
            where b.id = r.badge_id
              and b.name = 'Lencana Juragan Muda'
              and r.position = 7
        """).bindparams(detail=detail)
    )


def upgrade() -> None:
    _set_detail(NEW_DETAIL)


def downgrade() -> None:
    _set_detail(OLD_DETAIL)
