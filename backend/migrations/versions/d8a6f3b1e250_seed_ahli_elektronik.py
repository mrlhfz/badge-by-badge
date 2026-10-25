"""seed Ahli Elektronik requirements: four required items, no groups

Revision ID: d8a6f3b1e250
Revises: b5d7e2c9f013
Create Date: 2026-10-25 23:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8a6f3b1e250"
down_revision: str | Sequence[str] | None = "b5d7e2c9f013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Elektronik"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Menunjukkan 4 jenis litar elektrik",
        "Menunjukkan sekurang-kurangnya 4 jenis litar elektrik yang telah dipasang, satu daripadanya mestilah pada set radio yang mudah difahami.",
    ),
    (
        2,
        "Senaraikan 4 jenis alat elektronik",
        "Senaraikan sekurang-kurangnya 4 jenis alat elektronik untuk kegunaan rumah tangga dan perindustrian serta terangkan bagaimana tiap-tiap satu itu berfungsi.",
    ),
    (
        3,
        "Teori transistor",
        "Mengetahui teori yang mudah bagi transistor dan bagaimana alat itu boleh digunakan untuk dirangkaikan kepada alat-alat 'resistor', 'capacitors' dan 'coils' bagi membuat satu litar elektronik yang mudah.",
    ),
    (
        4,
        "Litar untuk lampu LED",
        "Membuat litar elektrik bagi menyalakan lampu LED.",
    ),
]


def upgrade() -> None:
    for position, text, detail in REQUIREMENTS:
        op.execute(
            sa.text("""
                insert into requirements (badge_id, stream_id, group_id, position, text, detail)
                select b.id, null, null, :position, :text, :detail
                from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name
                  and l.name = 'Pengakap Muda'
                  and b.stream_id is null
            """).bindparams(
                position=position,
                text=text,
                detail=detail,
                badge_name=BADGE_NAME,
            )
        )


def downgrade() -> None:
    op.execute(
        sa.text("""
            delete from requirements
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name and l.name = 'Pengakap Muda' and b.stream_id is null
            )
        """).bindparams(badge_name=BADGE_NAME)
    )
