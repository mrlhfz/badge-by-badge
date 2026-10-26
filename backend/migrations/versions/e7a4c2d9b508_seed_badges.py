"""seed the 57 badges (levels, streams, kinds, descriptions and sort order) so a fresh database has the catalogue

Revision ID: e7a4c2d9b508
Revises: d4b7f0c9a582
Create Date: 2026-10-27 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7a4c2d9b508"
down_revision: str | Sequence[str] | None = "a1f4c9e27d13"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (name, level name, stream name or None, kind, sort order, description)
BADGES = [
    (
        "Ahli Koleksi Hobi",
        "Pengakap Muda",
        None,
        "skill",
        1,
        "Kepandaian Kegemaran (am)",
    ),
    (
        "Ahli Renang",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        1,
        "Kepandaian Kegemaran (Laut)",
    ),
    (
        "Lencana Keahlian",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        1,
        "Lencana Keahlian untuk Pengakap Muda Laut",
    ),
    ("Ahli Muzik", "Pengakap Muda", None, "skill", 2, "Kepandaian Kegemaran (am)"),
    (
        "Lencana Usaha",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        2,
        "Lencana Usaha untuk Pengakap Muda Laut",
    ),
    (
        "Pengail Muda",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        2,
        "Kepandaian Kegemaran (Laut)",
    ),
    (
        "Ahli Pertahanan Diri",
        "Pengakap Muda",
        None,
        "skill",
        3,
        "Kepandaian Kegemaran (am)",
    ),
    (
        "Eksplorasi Marin",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        3,
        "Kepandaian Kegemaran (Laut)",
    ),
    (
        "Lencana Ahli Bot",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        3,
        "Lencana Ahli Bot untuk Pengakap Muda Laut",
    ),
    ("Ahli Sukan", "Pengakap Muda", None, "skill", 4, "Kepandaian Kegemaran (am)"),
    (
        "Lencana Maju",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        4,
        "Lencana Maju untuk Pengakap Muda Laut",
    ),
    (
        "Pewaris Maritim",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        4,
        "Kepandaian Kegemaran (Laut)",
    ),
    (
        "Ahli Snorkel",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        5,
        "Kepandaian Kegemaran (Laut)",
    ),
    (
        "Juru Masak di Khemah",
        "Pengakap Muda",
        None,
        "skill",
        5,
        "Kepandaian Kegemaran (am)",
    ),
    (
        "Lencana Juragan Muda",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        5,
        "Lencana Juragan Muda untuk Pengakap Muda Laut",
    ),
    (
        "Ahli Perahu Dayung",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        6,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Lencana Juragan",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        6,
        "Lencana Juragan untuk Pengakap Muda Laut",
    ),
    ("Pustakawan", "Pengakap Muda", None, "skill", 6, "Kepandaian Kegemaran (am)"),
    (
        "Ahli Komunikasi Marin",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        7,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Lencana Jaya",
        "Pengakap Muda",
        "Pengakap Laut",
        "compulsory",
        7,
        "Lencana Jaya untuk Pengakap Muda Laut",
    ),
    ("Peladang Muda", "Pengakap Muda", None, "skill", 7, "Kepandaian Kegemaran (am)"),
    (
        "Ahli Perahu Layar",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        8,
        "Kepandaian Pengetahuan (Laut)",
    ),
    ("Pelukis", "Pengakap Muda", None, "skill", 8, "Kepandaian Kegemaran (am)"),
    (
        "Ahli Survival Laut",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        9,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Penunggang Basikal",
        "Pengakap Muda",
        None,
        "skill",
        9,
        "Kepandaian Kegemaran (am)",
    ),
    (
        "Ahli Berkhemah",
        "Pengakap Muda",
        None,
        "skill",
        10,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Ahli Oseanografi",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        10,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Ahli Astronomi",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        11,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Ahli Elektronik",
        "Pengakap Muda",
        None,
        "skill",
        11,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Ahli Akuakultur",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        12,
        "Kepandaian Pengetahuan (Laut)",
    ),
    (
        "Ahli Ilmu Perintis",
        "Pengakap Muda",
        None,
        "skill",
        12,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Ahli Komputer",
        "Pengakap Muda",
        None,
        "skill",
        13,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Ahli Penyelamat Nyawa",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        13,
        "Kepandaian Perkhidmatan (Laut)",
    ),
    ("Ahli Mekanik", "Pengakap Muda", None, "skill", 14, "Kepandaian Pengetahuan (am)"),
    (
        "Kuartermaster",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        14,
        "Kepandaian Perkhidmatan (Laut)",
    ),
    (
        "Ahli Penukang",
        "Pengakap Muda",
        None,
        "skill",
        15,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Pemelihara Ekologi Marin",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        15,
        "Kepandaian Perkhidmatan (Laut)",
    ),
    (
        "Ahli Perhutanan",
        "Pengakap Muda",
        None,
        "skill",
        16,
        "Kepandaian Pengetahuan (am)",
    ),
    (
        "Pembantu Regatta",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        16,
        "Kepandaian Perkhidmatan (Laut)",
    ),
    ("Ahli Pelihat", "Pengakap Muda", None, "skill", 17, "Kepandaian Pengetahuan (am)"),
    (
        "Koordinator Pameran Pengakap Laut",
        "Pengakap Muda",
        "Pengakap Laut",
        "skill",
        17,
        "Kepandaian Perkhidmatan (Laut)",
    ),
    ("Pengembara", "Pengakap Muda", None, "skill", 18, "Kepandaian Pengetahuan (am)"),
    ("Tukang Masak", "Pengakap Muda", None, "skill", 19, "Kepandaian Pengetahuan (am)"),
    (
        "Ahli Pertolongan Cemas",
        "Pengakap Muda",
        None,
        "skill",
        20,
        "Kepandaian Perkhidmatan (am)",
    ),
    (
        "Ahli Anti-Dadah",
        "Pengakap Muda",
        None,
        "skill",
        21,
        "Kepandaian Perkhidmatan (am)",
    ),
    (
        "Ahli Komuniti",
        "Pengakap Muda",
        None,
        "skill",
        22,
        "Kepandaian Perkhidmatan (am)",
    ),
    ("Jurubahasa", "Pengakap Muda", None, "skill", 23, "Kepandaian Perkhidmatan (am)"),
    ("Pemadam Api", "Pengakap Muda", None, "skill", 24, "Kepandaian Perkhidmatan (am)"),
    ("Pemandu", "Pengakap Muda", None, "skill", 25, "Kepandaian Perkhidmatan (am)"),
    ("Pemelihara", "Pengakap Muda", None, "skill", 26, "Kepandaian Perkhidmatan (am)"),
    (
        "Pengawal Perkhemahan",
        "Pengakap Muda",
        None,
        "skill",
        27,
        "Kepandaian Perkhidmatan (am)",
    ),
    ("Setiausaha", "Pengakap Muda", None, "skill", 28, "Kepandaian Perkhidmatan (am)"),
    (
        "Lencana Jayadiri",
        "Pengakap Remaja",
        None,
        "compulsory",
        1,
        "Lencana Tertinggi Pengakap Remaja Laut",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        "Pengakap Remaja",
        "Pengakap Laut",
        "compulsory",
        2,
        "Lencana Tertinggi Pengakap Remaja Laut",
    ),
    (
        "Lencana Pengail",
        "Pengakap Remaja",
        "Pengakap Laut",
        "compulsory",
        3,
        "Lencana Tertinggi Pengakap Remaja Laut",
    ),
    (
        "Lencana Ekspedisi",
        "Pengakap Remaja",
        None,
        "compulsory",
        4,
        "Lencana Tertinggi Pengakap Remaja Laut",
    ),
    (
        "Lencana Perkhidmatan",
        "Pengakap Remaja",
        None,
        "compulsory",
        5,
        "Lencana Tertinggi Pengakap Remaja Laut",
    ),
]


def upgrade() -> None:
    # Skips a badge that already exists, so running this on the dev database adds nothing.
    for name, level_name, stream_name, kind, sort_order, description in BADGES:
        op.execute(
            sa.text("""
                insert into badges (level_id, stream_id, name, description, sort_order, kind)
                select l.id, s.id, :name, :description, :sort_order, cast(:kind as badge_kind)
                from levels l
                left join streams s on s.name = :stream_name
                where l.name = :level_name
                  and not exists (
                      select 1 from badges b
                      where b.name = :name
                        and b.level_id = l.id
                        and b.stream_id is not distinct from s.id
                  )
            """).bindparams(
                name=name,
                description=description,
                sort_order=sort_order,
                kind=kind,
                stream_name=stream_name,
                level_name=level_name,
            )
        )


def downgrade() -> None:
    # Nothing is removed. The dev database had these badges before this migration, so deleting
    # them here would delete real data. A fresh database can be rebuilt by upgrading from the start.
    pass
