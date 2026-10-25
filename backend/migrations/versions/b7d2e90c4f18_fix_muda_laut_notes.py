"""fix Muda Laut notes to match the book

Revision ID: b7d2e90c4f18
Revises: a1f4c9e27d13
Create Date: 2026-10-25 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7d2e90c4f18"
down_revision: str | Sequence[str] | None = "a1f4c9e27d13"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (badge name, position, new detail)
NEW_DETAILS = [
    (
        "Lencana Jaya",
        16,
        "Simpulan dan ikatan (Abah-Abah (manharness knot), Rolling Hitch, Middleman's Knot, Water Bowline, Fisherman's Knot, Eye Splice, Floor/Snake Lashing, Tripod/Figure-8 Lashing); mendirikan pondok sementara; projek perintis.",
    ),
    ("Lencana Maju", 12, "Menghidupkan api; Roti Liat; Ikan."),
    (
        "Lencana Maju",
        23,
        "Mengembara 16 km berjalan kaki dalam patrol dan bermalam di luar dengan mendirikan khemah. Menyediakan laporan bertulis dalam Buku log.",
    ),
    (
        "Lencana Juragan",
        2,
        "Membincangkan Beaufort wind and sea scales, dan mengetahui sekurang-kurangnya dua tanda keadaan cuaca, sama ada dalam keadaan baik atau buruk di kawasan perairan tempatan.",
    ),
    (
        "Lencana Juragan",
        11,
        "Menguruskan satu patrol sekurang-kurangnya tujuh orang untuk perjalanan di air sejauh 5 km (kenderaan sendiri) atau 10 km (kenderaan air awam), termasuk membuat persediaan dan persiapan menentukan keselamatan ahli-ahli serta kenderaan airnya dalam semua keadaan.",
    ),
]

# (badge name, position, old detail), the values before this migration
OLD_DETAILS = [
    (
        "Lencana Jaya",
        16,
        "Simpulan dan ikatan (Abah-Abah, Rolling Hitch, Middleman's Knot, Water Bowline, Fisherman's Knot, Eye Splice, Floor/Snake Lashing, Tripod/Figure-8 Lashing); mendirikan pondok sementara; projek perintis.",
    ),
    ("Lencana Maju", 12, None),
    ("Lencana Maju", 23, None),
    (
        "Lencana Juragan",
        2,
        "Membincangkan Beaufort wind and sea scales, dan mengetahui sekurang-kurangnya dua tanda keadaan laut.",
    ),
    (
        "Lencana Juragan",
        11,
        "Menguruskan satu patrol sekurang-kurangnya tujuh orang untuk perjalanan di air sejauh 5 km (kenderaan sendiri) atau 10 km (kenderaan air awam).",
    ),
]


def _set_detail(badge_name: str, position: int, detail: str | None) -> None:
    # Bind values as parameters, so quotes in the text cannot break the SQL.
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
    for badge_name, position, detail in NEW_DETAILS:
        _set_detail(badge_name, position, detail)


def downgrade() -> None:
    for badge_name, position, detail in OLD_DETAILS:
        _set_detail(badge_name, position, detail)
