"""match the Ahli Penyelamat Nyawa rescue rope and rescue details to the book

Revision ID: d9f2b6a0c318
Revises: c7d1a5e9b204
Create Date: 2026-10-26 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d9f2b6a0c318"
down_revision: str | Sequence[str] | None = "c7d1a5e9b204"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Penyelamat Nyawa"

# (position, old detail, new detail)
CHANGES = [
    (
        4,
        "Melemparkan tali penyelamat 10 meter sejauh 1 meter daripada 2 pacak jaraknya 2 kali daripada 3 kali.",
        "Melemparkan tali penyelamat sepanjang 10 meter di antara 2 pancang, jaraknya 1 meter, dengan kejayaan 2 kali daripada 3 kali lemparan.",
    ),
    (
        5,
        "Menunjukkan cara menyelamatkan mangsa dari rumah terbakar, gas racun, jalan raya, kena kejutan elektrik.",
        "Menunjukkan cara menyelamatkan mangsa dari rumah terbakar, gas racun, jalan raya dan kena kejutan elektrik.",
    ),
]


def _set_detail(position: int, detail: str) -> None:
    op.execute(
        sa.text("""
            update requirements r
            set detail = :detail
            from badges b
            where b.id = r.badge_id
              and b.name = :badge_name
              and r.position = :position
        """).bindparams(detail=detail, badge_name=BADGE_NAME, position=position)
    )


def upgrade() -> None:
    for position, _, new_detail in CHANGES:
        _set_detail(position, new_detail)


def downgrade() -> None:
    for position, old_detail, _ in CHANGES:
        _set_detail(position, old_detail)
