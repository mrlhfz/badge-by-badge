"""seed Ahli Sukan requirements: pick 5 events, one from each of Kumpulan A, B and C

Revision ID: c6e2a9f4b71d
Revises: b3d8f0a6c17e
Create Date: 2026-10-25 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c6e2a9f4b71d"
down_revision: str | Sequence[str] | None = "b3d8f0a6c17e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Sukan"

SUKAN_GROUP = "Pilih LIMA acara: sekurang-kurangnya SATU daripada tiap Kumpulan A, B dan C"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Berlari 100 meter (Kumpulan A)",
        "Berlari 100 meter. Darjah minima: di bawah 14 tahun 15 saat; di bawah 15 tahun 15 saat.",
    ),
    (
        2,
        "Berlari 200 meter (Kumpulan A)",
        "Berlari 200 meter. Darjah minima: di bawah 14 tahun 34 saat; di bawah 15 tahun 30 saat.",
    ),
    (
        3,
        "Berlari 400 meter (Kumpulan A)",
        "Berlari 400 meter. Darjah minima: di bawah 14 tahun 80 saat; di bawah 15 tahun 70 saat.",
    ),
    (
        4,
        "Berlari 800 meter (Kumpulan A)",
        "Berlari 800 meter. Darjah minima: di bawah 14 tahun 3 minit 10 saat; di bawah 15 tahun 2 minit 45 saat.",
    ),
    (
        5,
        "Berlari 1500 meter (Kumpulan A)",
        "Berlari 1500 meter. Darjah minima: di bawah 14 tahun 6 minit 10 saat; di bawah 15 tahun 5 minit 50 saat.",
    ),
    (
        6,
        "Lompat tinggi (Kumpulan B)",
        "Lompat tinggi. Darjah minima: di bawah 14 tahun 1.10 meter; di bawah 15 tahun 1.23 meter.",
    ),
    (
        7,
        "Lompat jauh (Kumpulan B)",
        "Lompat jauh. Darjah minima: di bawah 14 tahun 3.65 meter; di bawah 15 tahun 4.26 meter.",
    ),
    (
        8,
        "Lontar cakera (Kumpulan C)",
        "Lontar cakera. Darjah minima: di bawah 14 tahun 16.5 meter; di bawah 15 tahun 22.00 meter.",
    ),
    (
        9,
        "Lontar peluru (Kumpulan C)",
        "Lontar peluru. Darjah minima: di bawah 14 tahun 7.30 meter; di bawah 15 tahun 8.85 meter.",
    ),
    (
        10,
        "Lontar bola kriket (Kumpulan C)",
        "Lontar bola kriket. Darjah minima: di bawah 14 tahun 41.20 meter; di bawah 15 tahun 46.60 meter.",
    ),
]


def upgrade() -> None:
    # 1. The pick-five group. It does not yet check "one from each of A, B and C"; that is for #15.
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position)
            select b.id, :title, 5, 1
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and b.stream_id is null
        """).bindparams(title=SUKAN_GROUP, badge_name=BADGE_NAME)
    )
    # 2. The ten events, each one row, all inside the group
    for position, text, detail in REQUIREMENTS:
        op.execute(
            sa.text("""
                insert into requirements (badge_id, stream_id, group_id, position, text, detail)
                select b.id, null,
                       (select g.id from requirement_groups g
                        where g.badge_id = b.id and g.title = :group_title),
                       :position, :text, :detail
                from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name
                  and l.name = 'Pengakap Muda'
                  and b.stream_id is null
            """).bindparams(
                group_title=SUKAN_GROUP,
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
    op.execute(
        sa.text("""
            delete from requirement_groups
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name and l.name = 'Pengakap Muda' and b.stream_id is null
            )
        """).bindparams(badge_name=BADGE_NAME)
    )
