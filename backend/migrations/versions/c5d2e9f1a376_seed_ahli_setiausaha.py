"""seed Ahli Setiausaha requirements: seven required items and pick one of two in item 2

Revision ID: c5d2e9f1a376
Revises: b3f8d2a6e104
Create Date: 2026-10-26 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5d2e9f1a376"
down_revision: str | Sequence[str] | None = "b3f8d2a6e104"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Setiausaha"

PILIH_GROUP = "Pilih SATU: karangan atau menaip"

# (title, pick_count, position)
GROUPS = [
    (PILIH_GROUP, 1, 1),
]

# (position, group title or None, text, detail)
REQUIREMENTS = [
    (
        1,
        None,
        "Peraturan susunan pentadbiran",
        "Mengetahui peraturan susunan pentadbiran Persekutuan Pengakap peringkat Kumpulan dan Daerah, serta boleh menyediakan surat-menyurat untuk Majlis Ketua Patrol dan Pemimpin Kumpulan Pengakap.",
    ),
    (
        2,
        PILIH_GROUP,
        "Menulis karangan 250 patah perkataan",
        "Di hadapan Penilai, menulis sebuah karangan dengan baik, panjangnya 250 patah perkataan.",
    ),
    (
        3,
        PILIH_GROUP,
        "Menaip 100 patah perkataan",
        "Di hadapan Penilai, menaip 100 patah perkataan dengan mesin taip atau komputer, dengan tidak lebih daripada 5 kesalahan (jika ada); menunjukkan cara membersihkan mesin taip dan menggantikan riben mesin taip atau mesin mencetak.",
    ),
    (
        4,
        None,
        "Peraturan mesyuarat jawatankuasa",
        "Mengetahui peraturan mesyuarat jawatankuasa dan boleh menyediakan aturcara dan minit mesyuarat itu.",
    ),
    (
        5,
        None,
        "Pengurusan kewangan Kumpulan",
        "Mengetahui hal ehwal pengurusan kewangan Kumpulan Pengakap, menyediakan dan menyimpan dengan mudah kira-kira penerimaan dan perbelanjaan bagi Kumpulan atau Patrol, serta mengetahui cara menyimpan wang persendirian dalam bank.",
    ),
    (
        6,
        None,
        "Surat dan kad jemputan",
        "Menulis sepucuk surat mengikut tajuk yang diberi oleh Penilai, dan membuat draf kad jemputan kepada orang ramai berhubung dengan suatu upacara yang akan diadakan oleh Kumpulan, Unit atau Patrol.",
    ),
    (
        7,
        None,
        "Perkhidmatan Pejabat Pos",
        "Mengetahui penggunaan perkhidmatan Pejabat Pos bagi mendapatkan senarai bayaran kiriman pos dalam Malaysia dan berhubung dengan kiriman bungkusan, pos berdaftar, pos laju dan perkhidmatan pengiriman ke luar negeri.",
    ),
    (
        8,
        None,
        "Berita untuk Majalah Pengakap",
        "Menyediakan keluaran berita berkenaan dengan satu upacara Kumpulan atau Unit yang dihadiri oleh Penilai, untuk Majalah Pengakap melaporkan sesuatu peristiwa Kumpulan atau Daerah.",
    ),
    (
        9,
        None,
        "Pengurusan fail",
        "Mengendalikan pengurusan fail.",
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
