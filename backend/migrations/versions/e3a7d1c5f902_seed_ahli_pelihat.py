"""seed Ahli Pelihat requirements: five required items, no groups

Revision ID: e3a7d1c5f902
Revises: d9f2b6a0c318
Create Date: 2026-10-26 12:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e3a7d1c5f902"
down_revision: str | Sequence[str] | None = "d9f2b6a0c318"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Pelihat"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Permainan Kim: mengingati benda",
        "Dalam Permainan Kim, mengingati 20 daripada 25 jenis benda selepas melihatnya selama satu minit.",
    ),
    (
        2,
        "Mengenali bunyi",
        "Mengenali 8 daripada 10 jenis bunyi yang senang dengan mendengarnya sahaja.",
    ),
    (
        3,
        "Laporan lisan",
        "Membuat laporan lisan kurang daripada satu minit berkenaan dengan satu kejadian yang dilakonkan.",
    ),
    (
        4,
        "Acuan plaster jejak",
        "Membuat enam acuan plaster jejak burung, binatang (dua daripadanya binatang liar) dan kesan tayar motokar atau basikal. Semua acuan hendaklah dibuat oleh Pengakap sendiri dengan menaruh label tarikh dan tempat diambilnya dengan betul dan terang.",
    ),
    (
        5,
        "Mengikuti jejak",
        "Mengikuti satu jejak sejauh 1.5 km di kawasan yang belum pernah dilalui, yang mengandungi sekurang-kurangnya 25 jenis kesan binatang, kenderaan dan lain-lain.",
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
