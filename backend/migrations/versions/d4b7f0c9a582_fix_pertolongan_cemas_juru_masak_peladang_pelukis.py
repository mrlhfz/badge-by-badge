"""match the Pertolongan Cemas, Juru Masak di Khemah, Peladang Muda and Pelukis rows to the book

Revision ID: d4b7f0c9a582
Revises: c5d2e9f1a376
Create Date: 2026-10-26 23:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4b7f0c9a582"
down_revision: str | Sequence[str] | None = "c5d2e9f1a376"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PELADANG = "Peladang Muda"
UNGGAS_GROUP = "Kumpulan C: unggas (ujian 3)"

# (badge name, position, old detail, new detail)
DETAIL_CHANGES = [
    (
        "Ahli Pertolongan Cemas",
        2,
        "Mengetahui kedudukan urat nadi dan cara memberhentikan keluaran darah.",
        "Mengetahui kedudukan urat nadi dan tahu bagaimana memberhentikan keluaran darah.",
    ),
    (
        "Ahli Pertolongan Cemas",
        5,
        "Menunjukkan cara mengendali tulang selangka patah dan cara menjaga supaya yang patah tidak disyaki patah.",
        "Menunjukkan cara mengendalikan tulang selangka patah dan cara menjaga supaya yang patah tidak disyaki patah.",
    ),
    (
        "Juru Masak di Khemah",
        1,
        "Memasak DUA jenis makanan dengan tidak menggunakan perkakas dapur, untuk diri sendiri dan seorang lagi. Ingatan: semua hidangan hendaklah dimasak dalam keadaan berkhemah.",
        "Memasak DUA jenis makanan dengan tidak menggunakan perkakas dapur, untuk diri sendiri dan seorang lagi.",
    ),
    (
        "Juru Masak di Khemah",
        13,
        "Menyediakan DUA jenis menu dengan sukatan sekali untuk satu patrol seramai 6 orang; tidak semuanya makanan itu perlu dimasak.",
        "Menyediakan DUA jenis menu dengan sukatan sekali untuk satu patrol seramai 6 orang; tidak semuanya makanan itu perlu dimasak. Ingatan: semua hidangan hendaklah dimasak dalam keadaan berkhemah.",
    ),
    (
        PELADANG,
        1,
        "Menunjuk cara pengelolaan harian bagi sesuatu pusat ternakan. Menghuraikan kepada Penilai perubahan yang berlaku di pusat ternakan di kawasan serta beri sebab perubahan itu dibuat. Melakukan latihan praktik di suatu pusat ternakan yang baru ditubuhkan.",
        "Menunjukkan cara pengelolaan harian bagi sesuatu pusat ternakan. Menghuraikan kepada Penilai perubahan yang berlaku di pusat ternakan di kawasan serta beri sebab perubahan itu dibuat. Melakukan latihan praktik di suatu pusat ternakan yang baru ditubuhkan.",
    ),
    (
        PELADANG,
        5,
        "Menerangkan kepada Penilai berbagai kerja yang telah dijalankan dalam kebun itu dan hasil yang diperolehi.",
        "Menerangkan kepada Penilai berbagai kerja yang telah dijalankan dalam kebun itu dan hasil yang diperoleh.",
    ),
    (
        "Pelukis",
        7,
        "Melukis lambang Pengakap pada apa-apa bahan seperti kadbod, papan lapis, polystrene dan sebagainya.",
        "Melukis lambang Pengakap pada apa-apa bahan seperti kadbod, papan lapis, polystyrene dan sebagainya.",
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


def _set_applies_when_poultry(flag: bool) -> None:
    op.execute(
        sa.text("""
            update requirement_groups g
            set applies_when_poultry = :flag
            from badges b
            where b.id = g.badge_id
              and b.name = :badge_name
              and g.title = :title
        """).bindparams(flag=flag, badge_name=PELADANG, title=UNGGAS_GROUP)
    )


def upgrade() -> None:
    for badge_name, position, _, new_detail in DETAIL_CHANGES:
        _set_detail(badge_name, position, new_detail)
    _set_applies_when_poultry(True)


def downgrade() -> None:
    _set_applies_when_poultry(False)
    for badge_name, position, old_detail, _ in DETAIL_CHANGES:
        _set_detail(badge_name, position, old_detail)
