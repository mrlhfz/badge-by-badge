"""seed Ahli Anti-Dadah requirements: Tahap 1 (all units) and Tahap 2 (units with a pick count)

Revision ID: e2b9d4f6a3c8
Revises: c6e2a9f4b71d
Create Date: 2026-10-25 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e2b9d4f6a3c8"
down_revision: str | Sequence[str] | None = "c6e2a9f4b71d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Anti-Dadah"

# (title, pick_count, position, parent title)
GROUPS = [
    ("Tahap 1 (lulus semua unit)", 4, 1, None),
    ("Tahap 1 Unit I: Remaja", 4, 2, "Tahap 1 (lulus semua unit)"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 5, 3, "Tahap 1 (lulus semua unit)"),
    ("Tahap 1 Unit III: Tekanan dan masalah hidup", 2, 4, "Tahap 1 (lulus semua unit)"),
    (
        "Tahap 1 Unit IV: Dasar negara mengenai dadah",
        2,
        5,
        "Tahap 1 (lulus semua unit)",
    ),
    ("Tahap 2 (lulus kedua-dua unit)", 2, 6, None),
    ("Tahap 2 Unit I: Amali (pilih DUA)", 2, 7, "Tahap 2 (lulus kedua-dua unit)"),
    (
        "Tahap 2 Unit II: Kerja luar (pilih SATU)",
        1,
        8,
        "Tahap 2 (lulus kedua-dua unit)",
    ),
]

# (group title, position, text)
REQUIREMENTS = [
    ("Tahap 1 Unit I: Remaja", 1, "Perubahan"),
    ("Tahap 1 Unit I: Remaja", 2, "Masalah"),
    ("Tahap 1 Unit I: Remaja", 3, "Penyelesaian"),
    ("Tahap 1 Unit I: Remaja", 4, "Perhubungan"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 5, "Sebab merokok"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 6, "Akibat merokok"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 7, "Akibat dadah"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 8, "Akibat alkohol"),
    ("Tahap 1 Unit II: Tingkahlaku negatif", 9, "Sikap masyarakat"),
    (
        "Tahap 1 Unit III: Tekanan dan masalah hidup",
        10,
        "Cabaran di dalam dan luar sekolah",
    ),
    ("Tahap 1 Unit III: Tekanan dan masalah hidup", 11, "Khidmat bantu"),
    ("Tahap 1 Unit IV: Dasar negara mengenai dadah", 12, "Akta keselamatan"),
    ("Tahap 1 Unit IV: Dasar negara mengenai dadah", 13, "Akta Dadah Berbahaya"),
    ("Tahap 2 Unit I: Amali (pilih DUA)", 14, "Menyimpan buku skrap"),
    ("Tahap 2 Unit I: Amali (pilih DUA)", 15, "Melukis poster"),
    ("Tahap 2 Unit I: Amali (pilih DUA)", 16, "Menulis esei"),
    ("Tahap 2 Unit I: Amali (pilih DUA)", 17, "Menyertai pertandingan"),
    ("Tahap 2 Unit II: Kerja luar (pilih SATU)", 18, "Menyampaikan mesej anti dadah"),
    ("Tahap 2 Unit II: Kerja luar (pilih SATU)", 19, "Membuat lawatan"),
    ("Tahap 2 Unit II: Kerja luar (pilih SATU)", 20, "Menghadiri ceramah"),
]


def _insert_group(
    title: str, pick_count: int, position: int, parent_title: str | None
) -> None:
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position, parent_group_id)
            select b.id, :title, :pick_count, :position,
                   (select p.id from requirement_groups p
                    where p.badge_id = b.id and p.title = :parent_title)
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and b.stream_id is null
        """).bindparams(
            title=title,
            pick_count=pick_count,
            position=position,
            parent_title=parent_title,
            badge_name=BADGE_NAME,
        )
    )


def _insert_requirement(group_title: str, position: int, text: str) -> None:
    op.execute(
        sa.text("""
            insert into requirements (badge_id, stream_id, group_id, position, text, detail)
            select b.id, null,
                   (select g.id from requirement_groups g
                    where g.badge_id = b.id and g.title = :group_title),
                   :position, :text, :text
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and b.stream_id is null
        """).bindparams(
            group_title=group_title,
            position=position,
            text=text,
            badge_name=BADGE_NAME,
        )
    )


def upgrade() -> None:
    # Parents are listed before children, so each parent exists when its children are inserted.
    for title, pick_count, position, parent_title in GROUPS:
        _insert_group(title, pick_count, position, parent_title)
    for group_title, position, text in REQUIREMENTS:
        _insert_requirement(group_title, position, text)


def downgrade() -> None:
    badge_groups = """
        select g.id from requirement_groups g
        join badges b on b.id = g.badge_id
        join levels l on l.id = b.level_id
        where b.name = :badge_name and l.name = 'Pengakap Muda' and b.stream_id is null
    """
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
    # Child groups first, then parents
    op.execute(
        sa.text(f"""
            delete from requirement_groups
            where id in ({badge_groups}) and parent_group_id is not null
        """).bindparams(badge_name=BADGE_NAME)
    )
    op.execute(
        sa.text(f"""
            delete from requirement_groups
            where id in ({badge_groups})
        """).bindparams(badge_name=BADGE_NAME)
    )
