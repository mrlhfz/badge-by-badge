"""seed Ahli Pengawal Perkhemahan requirements: required items, pick three of five camp tasks, and pick three of four tools

Revision ID: b3f8d2a6e104
Revises: a6e9c4b2f718
Create Date: 2026-10-26 21:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3f8d2a6e104"
down_revision: str | Sequence[str] | None = "a6e9c4b2f718"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Pengawal Perkhemahan"

PILIH_LIMA = "Pilih TIGA daripada lima perkara"
PILIH_EMPAT = "Pilih TIGA daripada empat alat"

# (title, pick_count, position)
GROUPS = [
    (PILIH_LIMA, 3, 1),
    (PILIH_EMPAT, 3, 2),
]

# (position, group title or None, text, detail)
REQUIREMENTS = [
    (
        1,
        None,
        "Berkhemah sekurang-kurangnya 10 malam",
        "Telah berkhemah tidak kurang daripada 10 malam pada sekurang-kurangnya empat tapak perkhemahan yang berlainan.",
    ),
    (
        2,
        None,
        "Bertugas di tapak perkhemahan tetap",
        "Telah bertugas sekurang-kurangnya 7 hari di tapak perkhemahan tetap (daerah, negeri atau kebangsaan) membantu Pengawal Perkhemahan dengan memuaskan.",
    ),
    (
        3,
        PILIH_LIMA,
        "Menggunakan kayu arang untuk memasak",
        "Menunjukkan cara menggunakan kayu arang untuk memasak.",
    ),
    (
        4,
        PILIH_LIMA,
        "Membuat unggun api",
        "Menunjukkan cara membuat unggun api.",
    ),
    (
        5,
        PILIH_LIMA,
        "Memasang khemah patrol",
        "Menunjukkan cara memasang khemah patrol.",
    ),
    (
        6,
        PILIH_LIMA,
        "Menyidai kain basah dan menganginkan alat tidur",
        "Menyidai kain basah dan menganginkan alat tempat tidur dan lain-lain di perkhemahan.",
    ),
    (
        7,
        PILIH_LIMA,
        "Mencegah kebakaran di perkhemahan",
        "Mencegah kebakaran di perkhemahan.",
    ),
    (
        8,
        None,
        "Cara guna perkakas di perkhemahan",
        "Menerangkan dan, mana yang boleh, menunjukkan cara digunakan dalam perkhemahan untuk: a) membuat meja makanan; b) membuat tandas; c) menjaga alat memasak; d) menjaga air minuman dan makanan; e) menjaga alatan perkhemahan.",
    ),
    (
        9,
        None,
        "Taraf perkhemahan yang tinggi",
        "Mengetahui betapa mustahaknya menjaga taraf perkhemahan yang tinggi dan baik.",
    ),
    (
        10,
        None,
        "Peti pertolongan cemas",
        "Menyediakan dengan lengkap sebuah peti pertolongan cemas untuk kegunaan satu patrol yang berjalan selama 7 hari.",
    ),
    (
        11,
        PILIH_EMPAT,
        "Kapak penebang",
        "Menggunakan kapak penebang.",
    ),
    (
        12,
        PILIH_EMPAT,
        "Gergaji",
        "Menggunakan gergaji.",
    ),
    (
        13,
        PILIH_EMPAT,
        "Alat-alat ketuk (tukul)",
        "Menggunakan alat-alat ketuk seperti tukul.",
    ),
    (
        14,
        PILIH_EMPAT,
        "Alat mesin ringan",
        "Menggunakan alat mesin ringan seperti mesin pemotong rumput, gergaji rantai dan sebagainya.",
    ),
    (
        15,
        None,
        "Membincangkan tapak perkhemahan",
        "Membincangkan dengan Penilai bagaimana sebuah tapak perkhemahan yang tidak asing bagi Pengakap boleh diperbaiki dan dimajukan lagi.",
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
    # The groups exist before the rows that belong to them are inserted.
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
