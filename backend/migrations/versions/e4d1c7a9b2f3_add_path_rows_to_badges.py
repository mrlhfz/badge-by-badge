"""add path rows to Pengakap Muda badges

Revision ID: e4d1c7a9b2f3
Revises: b9e4f2a7c136
Create Date: 2026-10-27 12:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e4d1c7a9b2f3"
down_revision: str | Sequence[str] | None = "b9e4f2a7c136"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# The compulsory badges. Every Pengakap Muda Scout needs them, so they have no stream.
COMPULSORY = [
    "Lencana Keahlian",
    "Lencana Usaha",
    "Lencana Ahli Bot",
    "Lencana Maju",
    "Lencana Juragan Muda",
    "Lencana Jaya",
    "Lencana Juragan",
]

# Which row of the path each Pengakap Muda badge sits in, from the book's chart
ROWS: dict[int, list[str]] = {
    1: ["Lencana Keahlian"],
    2: ["Lencana Usaha", "Lencana Ahli Bot"],
    3: [
        # Kegemaran: kepelautan
        "Ahli Renang",
        "Pengail Muda",
        "Eksplorasi Marin",
        "Pewaris Maritim",
        "Ahli Snorkel",
        # Kegemaran: am
        "Ahli Koleksi Hobi",
        "Ahli Muzik",
        "Ahli Pertahanan Diri",
        "Ahli Sukan",
        "Juru Masak di Khemah",
        "Peladang Muda",
        "Pelukis",
        "Penunggang Basikal",
        "Pustakawan",
    ],
    4: ["Lencana Maju", "Lencana Juragan Muda"],
    5: [
        # Pengetahuan: kepelautan
        "Ahli Perahu Dayung",
        "Ahli Komunikasi Marin",
        "Ahli Perahu Layar",
        "Ahli Survival Laut",
        "Ahli Oseanografi",
        "Ahli Astronomi",
        "Ahli Akuakultur",
        # Pengetahuan: am
        "Ahli Berkhemah",
        "Ahli Elektronik",
        "Ahli Ilmu Perintis",
        "Ahli Komputer",
        "Ahli Mekanik",
        "Ahli Penukang",
        "Ahli Perhutanan",
        "Pelihat",
        "Pengembara",
        "Tukang Masak",
    ],
    6: [
        # Perkhidmatan: kepelautan
        "Ahli Penyelamat Nyawa",
        "Kuartermaster",
        "Pemelihara Ekologi Marin",
        "Pembantu Regatta",
        "Koordinator Pameran Pengakap Laut",
        # Perkhidmatan: am
        "Ahli Pertolongan Cemas",
        "Ahli Anti-Dadah",
        "Ahli Komuniti",
        "Jurubahasa",
        "Pemadam Api",
        "Pemandu",
        "Pemelihara",
        "Pengawal Perkhemahan",
        "Setiausaha",
    ],
    7: ["Lencana Jaya", "Lencana Juragan"],
}

# The level these badges belong to
LEVEL_NAME = "Pengakap Muda"


def upgrade() -> None:
    op.add_column("badges", sa.Column("path_row", sa.Integer(), nullable=True))

    # Put each badge in its row
    for row, names in ROWS.items():
        for name in names:
            op.execute(
                sa.text(
                    """
                    update badges set path_row = :row
                    where name = :name
                      and level_id = (select id from levels where name = :level)
                    """
                ).bindparams(row=row, name=name, level=LEVEL_NAME)
            )

    # Compulsory badges apply to every Scout, so they lose their stream
    for name in COMPULSORY:
        op.execute(
            sa.text(
                """
                update badges set stream_id = null
                where name = :name
                  and level_id = (select id from levels where name = :level)
                """
            ).bindparams(name=name, level=LEVEL_NAME)
        )


def downgrade() -> None:
    # The old streams on the compulsory badges are not restored here
    op.drop_column("badges", "path_row")
