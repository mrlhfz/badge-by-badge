"""seed Ahli Berkhemah requirements: nine required items, no groups

Revision ID: f4c1a8d2e907
Revises: e2b9d4f6a3c8
Create Date: 2026-10-25 21:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f4c1a8d2e907"
down_revision: str | Sequence[str] | None = "e2b9d4f6a3c8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Berkhemah"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Berkhemah dalam patrol 12 malam",
        "Telah berkhemah dalam patrol sejumlah sekurang-kurangnya 12 malam.",
    ),
    (
        2,
        "Mendirikan dan menggulung khemah pengembara",
        "Mendirikan, merobek dan menggulungkan khemah pengembara (hike tent).",
    ),
    (
        3,
        "Mengarah kerja khemah patrol",
        "Mengarah dengan jayanya kerja mendirikan, merobek dan menggulungkan sebuah khemah patrol.",
    ),
    (
        4,
        "Pilih tapak perkhemahan",
        "Mengetahui perkara mustahak yang perlu dipertimbangkan apabila memilih tempat untuk tapak perkhemahan.",
    ),
    (
        5,
        "Kebersihan dan keselamatan perkhemahan",
        "Mengetahui prinsip mengenai kebersihan dan keselamatan dalam perkhemahan.",
    ),
    (
        6,
        "Simpan bahan makanan di khemah kuartermaster",
        "Menunjukkan cara menyimpan bahan makanan di khemah kuartermaster.",
    ),
    (
        7,
        "Buat tempat simpan makanan dan dapur pelantar",
        "Membuat sendiri tempat menyimpan bahan makanan, dapur pelantar dan dua gejet lain yang dipilih sendiri dalam perkhemahan.",
    ),
    (
        8,
        "Masak untuk 2 orang dewasa",
        "Memasak untuk 2 orang dewasa sama ada masakan panas untuk sarapan pagi atau satu hidangan biasa termasuk sejenis sayur-sayuran.",
    ),
    (
        9,
        "Pengetahuan darjah perkhemahan tertinggi",
        "Mempunyai pengetahuan untuk mencapai darjah perkhemahan paling tinggi.",
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
