"""seed Ahli Komputer requirements: seven required items, and one pick from two

Revision ID: 9e4b1d7a6c02
Revises: a7f2c5d9b318
Create Date: 2026-10-26 00:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e4b1d7a6c02"
down_revision: str | Sequence[str] | None = "a7f2c5d9b318"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Komputer"

PILIH_GROUP = "Pilih SATU: pembentangan atau pemprosesan perkataan"

# (position, group title, text, detail)
REQUIREMENTS = [
    (
        1,
        None,
        "Mempunyai komputer atau menggunakannya 12 bulan",
        "Mempunyai sebuah komputer (Personal Computer) atau telah menggunakan komputer di sekolah sekurang-kurangnya 12 bulan.",
    ),
    (
        2,
        None,
        "Terangkan komputer dan komponen asas",
        "Menerangkan apa itu komputer dan komponen asasnya.",
    ),
    (
        3,
        None,
        "Sejarah ringkas komputer",
        "Mengetahui sejarah ringkas komputer.",
    ),
    (
        4,
        None,
        "Jenis komputer dan penyimpanan data",
        "Menerangkan pelbagai jenis komputer dan bagaimana data disimpan.",
    ),
    (
        5,
        None,
        "Sistem pengoperasian (OS)",
        "Mengetahui sistem pengoperasian (Operating System - OS) dan kegunaannya, misalnya Windows, Macintosh, Linux dan sebagainya.",
    ),
    (
        6,
        None,
        "Virus komputer dan cara mencegahnya",
        "Mengetahui apa itu virus komputer dan cara mencegahnya.",
    ),
    (
        7,
        None,
        "Kegunaan komputer di rumah, pejabat dan industri",
        "Mengetahui 6 jenis kegunaan komputer di rumah, pejabat dan industri.",
    ),
    (
        8,
        PILIH_GROUP,
        "Pembentangan MS PowerPoint",
        "Menyediakan satu pembentangan komputer MS PowerPoint dan sebagainya.",
    ),
    (
        9,
        PILIH_GROUP,
        "Pemprosesan perkataan (MS Word)",
        "Mempunyai kemahiran dalam pemprosesan perkataan seperti MS Word dan sebagainya.",
    ),
]


def upgrade() -> None:
    # 1. The pick-one group for items 8 and 9
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position)
            select b.id, :title, 1, 1
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and b.stream_id is null
        """).bindparams(title=PILIH_GROUP, badge_name=BADGE_NAME)
    )
    # 2. The requirements, each in its group when it has one
    for position, group_title, text, detail in REQUIREMENTS:
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
