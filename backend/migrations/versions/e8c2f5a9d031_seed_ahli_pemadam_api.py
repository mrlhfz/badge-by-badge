"""seed Ahli Pemadam Api requirements: seven required items, no groups

Revision ID: e8c2f5a9d031
Revises: d6e1b8f4a270
Create Date: 2026-10-26 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e8c2f5a9d031"
down_revision: str | Sequence[str] | None = "d6e1b8f4a270"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Pemadam Api"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Tugas Pasukan Bomba",
        "Mengetahui tugas Pasukan Bomba dan Penyelamat Tempatan.",
    ),
    (
        2,
        "Bahaya api dan pencegahan di rumah",
        "Memahami bahaya api dan mengetahui tindakan mencegah kebakaran di rumah mengenai semua jenis alat pemanas, khususnya pemanas yang menggunakan minyak dan bahan pembakar terbuka, pemanas elektrik, mancis, wayar elektrik, fius dan lain-lain alat; penggunaan alat gas dan minyak petrol; pengawasan bunga api, lilin, unggun api dan perhiasan rumah.",
    ),
    (
        3,
        "Persediaan mencegah kebakaran di perhimpunan",
        "Merancang persediaan mencegah kebakaran bagi sesuatu perhimpunan Pengakap atau acara, termasuk peraturan tempat duduk, dan mengetahui sebab persediaan sedemikian perlu.",
    ),
    (
        4,
        "Bahaya api dalam perkhemahan",
        "Mengetahui bahaya api dalam perkhemahan dan persediaan mencegah kebakaran, mengetahui punca kebakaran belukar dan lalang, serta tahu bagaimana mengawal kejadian itu.",
    ),
    (
        5,
        "Tindakan semasa kebakaran",
        "Menerangkan apa dan mengapa tindakan mesti diambil apabila berlaku kebakaran di dalam dan di luar rumah, termasuk cara memanggil pihak Bomba dan peraturan yang sepatutnya dilakukan sehingga pihak Bomba menerima panggilan itu.",
    ),
    (
        6,
        "Peralatan memadam kebakaran",
        "Mengetahui: a) kerja mencegah kebakaran dengan menggunakan baldi berderet; b) cara menggunakan pam kaki (stirrup pump) dan pam tangan; c) cara menggunakan pemadam api seperti air, asid soda, gas cartridge, karbon tetraklorida dan buih, serta jenis pemadam yang sesuai bagi setiap jenis api.",
    ),
    (
        7,
        "Mengendalikan orang yang terbakar",
        "Mengendalikan seorang yang terbakar pakaian di badannya.",
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
