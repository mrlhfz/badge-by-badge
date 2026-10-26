"""seed Penunggang Basikal requirements: five required items, no groups

Revision ID: c4a9e7b3d215
Revises: b8f3d6a2c941
Create Date: 2026-10-26 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4a9e7b3d215"
down_revision: str | Sequence[str] | None = "b8f3d6a2c941"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Penunggang Basikal"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Memiliki dan menggunakan basikal",
        "Mempunyai dan menggunakan dengan jayanya selama sekurang-kurangnya 6 bulan sebuah basikal yang cukup lengkap dan berkeadaan baik.",
    ),
    (
        2,
        "Memperbaiki kerosakan basikal",
        "Memperbaiki kerosakan seperti menukar tayar dan tiub, menampal tiub bocor, serta mengganti alat brek atau bahagian lain pada basikal mengikut arahan Penilai.",
    ),
    (
        3,
        "Peraturan lalu lintas dan peta",
        "Mengetahui peraturan lalu lintas dan keselamatan jalan raya serta boleh membaca peta jalan raya.",
    ),
    (
        4,
        "Pengembaraan basikal 10 km",
        "Mengambil bahagian dalam kegiatan pengembaraan basikal sekurang-kurangnya sejauh 10 kilometer.",
    ),
    (
        5,
        "Mengulangi berita secara lisan",
        "Mengulangi kata-kata satu berita yang diberi secara lisan dan mesti disampaikan kepada pihak tertentu setelah menunggang basikal selama satu jam.",
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
