"""match the Ahli Ilmu Perintis and Ahli Komputer details to the book

Revision ID: e5c9a2f8d741
Revises: d1e7b9a3f604
Create Date: 2026-10-26 02:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5c9a2f8d741"
down_revision: str | Sequence[str] | None = "d1e7b9a3f604"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (badge name, position, old detail, new detail)
CHANGES = [
    (
        "Ahli Ilmu Perintis",
        1,
        "Mengetahui ciri utama dalam berbagai jenis dan ukuran tali yang dibuat daripada serabut biasa. Menunjukkan bagaimana menggulung dan menjaga tali.",
        "Mengetahui ciri utama dalam berbagai jenis dan ukuran tali yang dibuat daripada serabut biasa. Menunjukkan bagaimana menggulung dan menjaga tali serta menjaga ketegangannya.",
    ),
    (
        "Ahli Ilmu Perintis",
        3,
        "Mengerti serta menunjukkan kegunaan pancang dogang (anchorage) untuk peneroka yang boleh digunakan bagi berbagai-bagai projek, tempat dan keadaan tanah.",
        "Mengerti serta menunjukkan kegunaan pancang dogang (anchorage) untuk peneroka yang boleh digunakan bagi berbagai-bagai projek, tempat dan keadaan tanah termasuk tanah yang gembur dan lembab.",
    ),
    (
        "Ahli Ilmu Perintis",
        5,
        "Mengetuai patrol membuat satu projek yang dipilih oleh Penilai.",
        "Mengetuai patrol membuat satu projek yang dipilih oleh Penilai dengan jayanya.",
    ),
    (
        "Ahli Ilmu Perintis",
        6,
        "Dengan jayanya mengetuai patrol membuat projek yang direka sendiri dengan terlebih dahulu berbincang dengan Penilai tentang rangka, model, cara membuatnya, alatan yang digunakan dan jangka masa menyiapkan projek itu.",
        "Dengan jayanya mengetuai patrol membuat projek yang direka sendiri dengan terlebih dahulu berbincang dengan Penilai tentang rangka-rangka, model, cara membuatnya, alatan yang digunakan dan jangka masa bagi menyiapkan projek itu.",
    ),
    (
        "Ahli Komputer",
        6,
        "Mengetahui apa itu virus komputer dan cara mencegahnya.",
        "Mengetahui mengenai virus komputer dan cara mencegahnya.",
    ),
    (
        "Ahli Komputer",
        8,
        "Menyediakan satu pembentangan komputer MS PowerPoint dan sebagainya.",
        "Menyediakan satu pengaturcaraan persembahan komputer MS PowerPoint dan sebagainya.",
    ),
]


def _set_detail(badge_name: str, position: int, detail: str) -> None:
    op.execute(
        sa.text("""
            update requirements r
            set detail = :detail
            from badges b
            where b.id = r.badge_id
              and b.name = :badge_name
              and r.position = :position
        """).bindparams(detail=detail, badge_name=badge_name, position=position)
    )


def upgrade() -> None:
    for badge_name, position, _, new_detail in CHANGES:
        _set_detail(badge_name, position, new_detail)


def downgrade() -> None:
    for badge_name, position, old_detail, _ in CHANGES:
        _set_detail(badge_name, position, old_detail)
