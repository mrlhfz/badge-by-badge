"""seed Ahli Pengembara requirements: four required items, no groups

Revision ID: f5b9e2d7a4c1
Revises: e3a7d1c5f902
Create Date: 2026-10-26 13:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f5b9e2d7a4c1"
down_revision: str | Sequence[str] | None = "e3a7d1c5f902"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Pengembara"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Mengembara bersama dua Pengakap",
        "Mengembara dengan berjalan kaki, berbasikal, berperahu atau berakit bersama-sama dua orang Pengakap dalam masa sekurang-kurangnya 2 hari 1 malam ke suatu tempat yang belum pernah dilawati, dengan membawa alatan dan bekalan yang cukup.",
    ),
    (
        2,
        "Persediaan pengembaraan",
        "Mengetahui persediaan suatu pengembaraan serta menyusun alatan berkenaan dengan rapi.",
    ),
    (
        3,
        "Projek dan peta pengembaraan",
        "Merancang satu projek berhubung dengan pengembaraan tersebut dan membuat peta yang mengandungi semua jalan kampung dan taliair dalam lingkungan dua kilometer daripada satu tanda. Rancangan itu ditunjukkan kepada Penilai bagi kelulusannya, kemudian pengembaraan dijalankan seorang diri atau bersama seorang Pengakap lain.",
    ),
    (
        4,
        "Mengembara 10 km dengan kompas",
        "Mengembara dengan seorang Pengakap lain sejauh 10 km dengan berpandukan kompas dan peta sahaja.",
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
