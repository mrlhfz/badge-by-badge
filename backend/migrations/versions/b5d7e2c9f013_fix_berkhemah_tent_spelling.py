"""fix the tent take-down word in Ahli Berkhemah: merobek becomes merobohkan

Revision ID: b5d7e2c9f013
Revises: f4c1a8d2e907
Create Date: 2026-10-25 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b5d7e2c9f013"
down_revision: str | Sequence[str] | None = "f4c1a8d2e907"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Berkhemah"

# (position, new text, old text, old detail, new detail)
ROWS = [
    (
        2,
        "Mendirikan dan merobohkan khemah pengembara",
        "Mendirikan dan menggulung khemah pengembara",
        "Mendirikan, merobek dan menggulungkan khemah pengembara (hike tent).",
        "Mendirikan, merobohkan dan menggulungkan khemah pengembara (hike tent).",
    ),
    (
        3,
        "Mengarah kerja khemah patrol",
        "Mengarah kerja khemah patrol",
        "Mengarah dengan jayanya kerja mendirikan, merobek dan menggulungkan sebuah khemah patrol.",
        "Mengarah dengan jayanya kerja mendirikan, merobohkan dan menggulungkan sebuah khemah patrol.",
    ),
]


def _set(position: int, text: str, detail: str) -> None:
    op.execute(
        sa.text("""
            update requirements r
            set text = :text, detail = :detail
            from badges b
            where b.id = r.badge_id
              and b.name = :badge_name
              and r.position = :position
        """).bindparams(
            text=text, detail=detail, position=position, badge_name=BADGE_NAME
        )
    )


def upgrade() -> None:
    for position, new_text, _, _, new_detail in ROWS:
        _set(position, new_text, new_detail)


def downgrade() -> None:
    for position, _, old_text, old_detail, _ in ROWS:
        _set(position, old_text, old_detail)
