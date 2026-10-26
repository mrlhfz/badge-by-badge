"""seed Tukang Masak requirements: terma, pick two of eight dishes, cooking for guests, and cutting meat

Revision ID: a2c6f8d1e537
Revises: f5b9e2d7a4c1
Create Date: 2026-10-26 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2c6f8d1e537"
down_revision: str | Sequence[str] | None = "f5b9e2d7a4c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Tukang Masak"

PILIH_GROUP = "Pilih DUA masakan daripada senarai"

# (title, pick_count, position)
GROUPS = [
    (PILIH_GROUP, 2, 1),
]

# (position, group title or None, text, detail)
REQUIREMENTS = [
    (
        1,
        None,
        "Terma masakan umum",
        "Mengetahui terma masakan umum: tumis, cincang, parut, seram kuku, manis-manis buah dan sebagainya.",
    ),
    (2, PILIH_GROUP, "Telur goreng", "Menyediakan bahan dan memasak telur goreng."),
    (3, PILIH_GROUP, "Pisang goreng", "Menyediakan bahan dan memasak pisang goreng."),
    (4, PILIH_GROUP, "Bubur kacang", "Menyediakan bahan dan memasak bubur kacang."),
    (5, PILIH_GROUP, "Sambal tumis", "Menyediakan bahan dan memasak sambal tumis."),
    (6, PILIH_GROUP, "Sup", "Menyediakan bahan dan memasak sup."),
    (7, PILIH_GROUP, "Masak kicap", "Menyediakan bahan dan memasak masak kicap."),
    (8, PILIH_GROUP, "Asam pedas", "Menyediakan bahan dan memasak asam pedas."),
    (9, PILIH_GROUP, "Sayur campur", "Menyediakan bahan dan memasak sayur campur."),
    (
        10,
        None,
        "Nasi putih",
        "Memasak dan menghidangkan dengan sempurna nasi putih untuk dua hingga empat orang tetamu.",
    ),
    (
        11,
        None,
        "Kari daging",
        "Memasak dan menghidangkan dengan sempurna kari daging untuk dua hingga empat orang tetamu.",
    ),
    (
        12,
        None,
        "Sejenis masakan daripada sayur",
        "Memasak dan menghidangkan dengan sempurna sejenis masakan daripada sayur untuk dua hingga empat orang tetamu.",
    ),
    (
        13,
        None,
        "Manisan",
        "Memasak dan menghidangkan dengan sempurna manisan untuk dua hingga empat orang tetamu.",
    ),
    (
        14,
        None,
        "Kopi atau teh",
        "Memasak dan menghidangkan dengan sempurna kopi atau teh untuk dua hingga empat orang tetamu.",
    ),
    (
        15,
        None,
        "Memotong dan menghiris daging",
        "Mengetahui prinsip memotong dan menghiris daging lembu, kambing dan daging ayam, sebelum dan selepas dimasak.",
    ),
]


def _insert_group(title: str, pick_count: int, position: int) -> None:
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position)
            select b.id, :title, :pick_count, :position
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and b.stream_id is null
        """).bindparams(
            title=title,
            pick_count=pick_count,
            position=position,
            badge_name=BADGE_NAME,
        )
    )


def _insert_requirement(
    position: int, group_title: str | None, text: str, detail: str
) -> None:
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
            group_title=group_title,
            position=position,
            text=text,
            detail=detail,
            badge_name=BADGE_NAME,
        )
    )


def upgrade() -> None:
    # The group exists before the rows that belong to it are inserted.
    for title, pick_count, position in GROUPS:
        _insert_group(title, pick_count, position)
    for position, group_title, text, detail in REQUIREMENTS:
        _insert_requirement(position, group_title, text, detail)


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
