"""seed Ahli Jurubahasa requirements: four required items, and pick one letter in item 4b

Revision ID: d6e1b8f4a270
Revises: c4a9e7b3d215
Create Date: 2026-10-26 17:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d6e1b8f4a270"
down_revision: str | Sequence[str] | None = "c4a9e7b3d215"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Jurubahasa"

PILIH_GROUP = "Pilih SATU surat"

# (title, pick_count, position)
GROUPS = [
    (PILIH_GROUP, 1, 1),
]

# (position, group title or None, text, detail)
REQUIREMENTS = [
    (
        1,
        None,
        "Berceramah dengan Pengakap",
        "Berceramah dengan Pengakap atas tajuk yang diberi oleh Penilai selama sekurang-kurangnya 5 minit.",
    ),
    (
        2,
        None,
        "Karangan dalam bahasa lain",
        "Menulis satu karangan sekurang-kurangnya 150 patah perkataan atas tajuk yang diberi oleh Penilai.",
    ),
    (
        3,
        None,
        "Terjemahan petikan",
        "Menterjemahkan satu petikan daripada surat khabar atau majalah, lebih kurang 100 patah perkataan. Pengakap diberi masa 10 minit untuk membaca dan menterjemah.",
    ),
    (
        4,
        None,
        "Jurubahasa kepada pelawat luar negeri",
        "Menjadi jurubahasa kepada seorang pelawat luar negeri.",
    ),
    (
        5,
        PILIH_GROUP,
        "Menulis surat kepada kumpulan atau sekolah",
        "Menulis sepucuk surat kepada satu Kumpulan Pengakap, sekolah atau pertubuhan berkenaan dengan suatu lawatan.",
    ),
    (
        6,
        PILIH_GROUP,
        "Berkirim surat dengan sahabat luar negeri",
        "Berkirim-kiriman surat dalam jangka masa tidak kurang enam bulan dengan seorang Pengakap atau sahabat luar negeri yang sebaya.",
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
