"""seed Ahli Komuniti requirements: pick one part (A, B or C), with sub-choices in Part B

Revision ID: b8f3d6a2c941
Revises: a2c6f8d1e537
Create Date: 2026-10-26 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8f3d6a2c941"
down_revision: str | Sequence[str] | None = "a2c6f8d1e537"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Komuniti"

PARENT = "Pilih SATU bahagian: A, B atau C"
PART_B = "Bahagian B"
PART_B_ITEM_1 = "Bahagian B item 1: pilih TIGA daripada enam perkara"
PART_B_ITEM_5 = "Bahagian B item 5: pilih SATU kemahiran"
PART_B_ITEM_6 = "Bahagian B item 6: pilih SATU perkara"

# (title, pick_count, position, parent title)
GROUPS = [
    (PARENT, 1, 1, None),
    ("Bahagian A", 3, 2, PARENT),
    (PART_B, 6, 3, PARENT),
    (PART_B_ITEM_1, 3, 4, PART_B),
    (PART_B_ITEM_5, 1, 5, PART_B),
    (PART_B_ITEM_6, 1, 6, PART_B),
    ("Bahagian C", 1, 7, PARENT),
]

# (position, group title, text, detail)
REQUIREMENTS = [
    (
        1,
        "Bahagian A",
        "Mengkaji perkhidmatan kemasyarakatan setempat",
        "Mengkaji perkhidmatan kemasyarakatan setempat seperti pendidikan, kesihatan, rekreasi dan sosial dengan menggunakan sumber Majlis Daerah, pegawai belia dan perpustakaan awam; membincang dengan Majlis Ketua Patrol bagaimana perkhidmatan itu dapat membantu keperluan masyarakat.",
    ),
    (
        2,
        "Bahagian A",
        "Kajian aspek masyarakat setempat",
        "Menjalankan kajian berkenaan satu aspek masyarakat setempat selepas mengemukakan kepada Majlis Ketua Patrol dan Pemimpin Pengakap; kajian sekurang-kurangnya 6 bulan, dengan kumpulan yang dikaji ialah orang dewasa, kanak-kanak, orang cacat, yatim piatu dan penganggur.",
    ),
    (
        3,
        "Bahagian A",
        "Perkhidmatan masyarakat 2 bulan",
        "Mengambil bahagian dalam perkhidmatan masyarakat selama sekurang-kurangnya 2 bulan dan menerangkan kepada Penilai segala pengalaman semasa menjalankan aktiviti itu.",
    ),
    (
        4,
        PART_B,
        "Cara membantu orang cacat",
        "Menunjukkan kesedaran dan menerangkan 4 cara membantu orang cacat dalam kehidupan harian.",
    ),
    (
        5,
        PART_B,
        "Agensi perkhidmatan orang cacat",
        "Menyenaraikan agensi dan penganjur yang memberi perkhidmatan kepada orang cacat, termasuk perkhidmatan sosial.",
    ),
    (
        6,
        PART_B,
        "Berhubung giat dengan orang cacat",
        "Berhubung giat dengan orang cacat dalam tempoh 3 bulan.",
    ),
    (
        7,
        PART_B_ITEM_1,
        "Deria",
        "Mengetahui 3 perkara tentang kelemahan deria orang cacat.",
    ),
    (
        8,
        PART_B_ITEM_1,
        "Intelek",
        "Mengetahui 3 perkara tentang kelemahan intelek orang cacat.",
    ),
    (
        9,
        PART_B_ITEM_1,
        "Sistem saraf",
        "Mengetahui 3 perkara tentang kelemahan sistem saraf orang cacat.",
    ),
    (
        10,
        PART_B_ITEM_1,
        "Paru-paru dan jantung",
        "Mengetahui 3 perkara tentang kelemahan paru-paru dan jantung orang cacat.",
    ),
    (
        11,
        PART_B_ITEM_1,
        "Perkembangan fizikal",
        "Mengetahui 3 perkara tentang kelemahan perkembangan fizikal orang cacat.",
    ),
    (
        12,
        PART_B_ITEM_1,
        "Tahap bahasa",
        "Mengetahui 3 perkara tentang kelemahan tahap bahasa orang cacat.",
    ),
    (
        13,
        PART_B_ITEM_5,
        "Bahasa isyarat untuk orang pekak",
        "Menunjukkan kemahiran bahasa isyarat untuk orang pekak.",
    ),
    (
        14,
        PART_B_ITEM_5,
        "Braille untuk orang buta",
        "Menunjukkan kemahiran braille untuk orang buta.",
    ),
    (
        15,
        PART_B_ITEM_5,
        "Pengurusan kerusi roda",
        "Menunjukkan kemahiran pengurusan dan penjagaan kerusi roda.",
    ),
    (
        16,
        PART_B_ITEM_5,
        "Teknik pengendalian orang cacat",
        "Menunjukkan teknik pengendalian orang cacat, misalnya mengangkat atau mengusung.",
    ),
    (
        17,
        PART_B_ITEM_6,
        "Cerpen atau sajak untuk orang buta",
        "Merakamkan sebuah cerpen atau sajak untuk orang buta.",
    ),
    (
        18,
        PART_B_ITEM_6,
        "Bangunan awam di bandar",
        "Mengkaji berkenaan bangunan awam di bandar.",
    ),
    (
        19,
        PART_B_ITEM_6,
        "Menemani orang buta",
        "Menemani seorang orang buta untuk membeli-belah atau bersiar-siar.",
    ),
    (
        20,
        "Bahagian C",
        "Melawat balai polis tempatan",
        "Melawat balai polis tempatan dan membuat kajian mengenai: a) organisasi jabatan polis dan struktur jawatan atau pangkat; b) bahagian yang terdapat di Jabatan Polis; c) jenis perhubungan (seperti radio dan walkie-talkie), sistem kecemasan dan kod fonetik yang digunakan; d) tugas anggota polis amnya dan pembenterasan jenayah khasnya.",
    ),
]


def _insert_group(title: str, pick_count: int, position: int, parent_title: str | None) -> None:
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


def _insert_requirement(position: int, group_title: str, text: str, detail: str) -> None:
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
    # Parents are listed before children, so each parent exists when its children are inserted.
    for title, pick_count, position, parent_title in GROUPS:
        _insert_group(title, pick_count, position, parent_title)
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
    # Child groups first, then parents
    op.execute(
        sa.text("""
            delete from requirement_groups
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name and l.name = 'Pengakap Muda' and b.stream_id is null
            )
            and parent_group_id is not null
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
