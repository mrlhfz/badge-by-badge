"""seed Ahli Mekanik requirements: pick one part (A, B or C); Part C has two options

Revision ID: f9a3c6e1b852
Revises: e5c9a2f8d741
Create Date: 2026-10-26 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9a3c6e1b852"
down_revision: str | Sequence[str] | None = "e5c9a2f8d741"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Mekanik"

# (title, pick_count, position, parent title)
GROUPS = [
    ("Pilih SATU bahagian: A, B atau C", 1, 1, None),
    ("Bahagian A", 9, 2, "Pilih SATU bahagian: A, B atau C"),
    ("Bahagian B", 5, 3, "Pilih SATU bahagian: A, B atau C"),
    ("Bahagian C", 1, 4, "Pilih SATU bahagian: A, B atau C"),
    ("Bahagian C Pilihan 1: item 1 dan 2", 2, 5, "Bahagian C"),
    ("Bahagian C Pilihan 2: item 3", 1, 6, "Bahagian C"),
]

# (group title, position, text, detail)
REQUIREMENTS = [
    (
        "Bahagian A",
        1,
        "Enjin 2 lejang dan 4 lejang",
        "Mengetahui perbezaan di antara enjin jenis 2 lejang dengan 4 lejang.",
    ),
    ("Bahagian A", 2, "Bahagian asas motosikal", "Mengetahui bahagian asas motosikal."),
    (
        "Bahagian A",
        3,
        "Ukuran celah plag motosikal",
        "Membuka, mencuci dan memeriksa ukuran celah plag motosikal.",
    ),
    (
        "Bahagian A",
        4,
        "Minyak pelincir motosikal",
        "Menukar minyak pelincir motosikal; mengetahui cara memeriksa paras minyak pelincir itu.",
    ),
    (
        "Bahagian A",
        5,
        "Tayar motosikal tiub yang bocor",
        "Tahu membuka tayar motosikal tiub yang bocor dan memasangnya semula.",
    ),
    (
        "Bahagian A",
        6,
        "Clutch dan brek motosikal",
        "Mengetahui cara membetulkan 'clutch' dan brek motosikal.",
    ),
    (
        "Bahagian A",
        7,
        "Mentol motosikal",
        "Menukar mentol motosikal yang terbakar atau pecah.",
    ),
    (
        "Bahagian A",
        8,
        "Rantai motosikal yang kendur",
        "Mengetahui cara menangani rantai motosikal yang kendur.",
    ),
    (
        "Bahagian A",
        9,
        "Air bateri motosikal",
        "Mengetahui cara menambahkan air bateri motosikal.",
    ),
    (
        "Bahagian B",
        10,
        "Alat penerima radio",
        "Membuat alat penerima radio (radio receiver) yang menggunakan dua injap (valves) atau transistor, di atas sekeping papan. Jika dikehendaki, fon telinga (headphone) boleh juga dipasang. Melukis litar elektrik (circuit) penerima radio itu dan terangkan kepada Penilai fungsi tiap-tiap satu bahagian alat yang digunakan itu.",
    ),
    (
        "Bahagian B",
        11,
        "Alat pateri (soldering iron)",
        "Menunjukkan kebolehan menggunakan alat pateri (soldering iron) dan tahu berjaga-jaga apabila menggunakan pateri pada transistor dan litar elektrik.",
    ),
    (
        "Bahagian B",
        12,
        "Keselamatan memperbaiki peti radio AC/DC",
        "Mengetahui betapa mustahaknya berjaga-jaga tentang keselamatan apabila memperbaiki peti radio yang memakai tenaga elektrik AC/DC, seperti memasang sambungan pembesar suara atau memperbaiki bahagian yang kecil-kecil sebelum menutup suis memotong tenaga elektrik itu.",
    ),
    (
        "Bahagian B",
        13,
        "Memperbaiki kerosakan kecil pada peti radio",
        "Memperbaiki kerosakan yang kecil-kecil pada peti radio seperti suis dan wayar longgar, bunyi bising atau bateri lemah.",
    ),
    (
        "Bahagian B",
        14,
        "Syarat Lesen Radio Amatur",
        "Terangkan dengan ringkas syarat utama untuk mendapatkan Lesen Radio Amatur (transceiver).",
    ),
    (
        "Bahagian C Pilihan 1: item 1 dan 2",
        15,
        "Prinsip dan perjalanan motobot lebih 2 kuda",
        "Menerangkan prinsip dan perjalanan 2 jenis jentera motobot yang lebih dari 2 kuda kuasanya dan mengetahui cara menyelenggarakannya.",
    ),
    (
        "Bahagian C Pilihan 1: item 1 dan 2",
        16,
        "Motobot 4 kuda dan enjin laut diesel",
        "Mengetahui cara menjalankan jentera motobot yang berkuasa 4 kuda dan juga cara menyelenggarakan enjin laut diesel.",
    ),
    (
        "Bahagian C Pilihan 2: item 3",
        17,
        "Enjin sangkut (outboard engine)",
        "Dengan bantuan minima, membuka, mencuci dan memasang balik enjin sangkut (outboard engine) serta memasangkannya pada bot dengan betul. Menerangkan cara mengetahui kerosakan kecil pada masa mula menjalankan enjin dan masa berlayar.",
    ),
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


def _insert_requirement(
    group_title: str, position: int, text: str, detail: str
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
    # Parents are listed before children, so each parent exists when its children are inserted.
    for title, pick_count, position, parent_title in GROUPS:
        _insert_group(title, pick_count, position, parent_title)
    for group_title, position, text, detail in REQUIREMENTS:
        _insert_requirement(group_title, position, text, detail)


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
