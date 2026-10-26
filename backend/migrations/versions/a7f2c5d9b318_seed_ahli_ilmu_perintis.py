"""seed Ahli Ilmu Perintis requirements: six required items, no groups

Revision ID: a7f2c5d9b318
Revises: d8a6f3b1e250
Create Date: 2026-10-25 23:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7f2c5d9b318"
down_revision: str | Sequence[str] | None = "d8a6f3b1e250"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Ilmu Perintis"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Ciri tali dan cara menggulung",
        "Mengetahui ciri utama dalam berbagai jenis dan ukuran tali yang dibuat daripada serabut biasa. Menunjukkan bagaimana menggulung dan menjaga tali.",
    ),
    (
        2,
        "Keselamatan penggunaan tali",
        "Boleh menentukan dan mengawasi keselamatan penggunaan tali.",
    ),
    (
        3,
        "Kegunaan pancang dogang (anchorage)",
        "Mengerti serta menunjukkan kegunaan pancang dogang (anchorage) untuk peneroka yang boleh digunakan bagi berbagai-bagai projek, tempat dan keadaan tanah.",
    ),
    (
        4,
        "Simpulan, ikatan dan cara mematikan tali",
        "Menunjukkan kegunaan semua simpulan, ikatan dan cara mematikan tali yang digunakan dalam kegiatan peneroka.",
    ),
    (
        5,
        "Mengetuai patrol membuat projek",
        "Mengetuai patrol membuat satu projek yang dipilih oleh Penilai.",
    ),
    (
        6,
        "Projek perintis sendiri",
        "Dengan jayanya mengetuai patrol membuat projek yang direka sendiri dengan terlebih dahulu berbincang dengan Penilai tentang rangka, model, cara membuatnya, alatan yang digunakan dan jangka masa menyiapkan projek itu.",
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
