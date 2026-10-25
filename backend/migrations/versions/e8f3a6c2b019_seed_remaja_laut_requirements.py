"""seed Remaja Laut requirements for Jurumudi and Pengail

Revision ID: e8f3a6c2b019
Revises: d5e0b38a1c94
Create Date: 2026-10-25 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e8f3a6c2b019"
down_revision: str | Sequence[str] | None = "d5e0b38a1c94"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LAUT_BADGES = ["Lencana Jurumudi (Helmsman)", "Lencana Pengail"]

PENGAIL_GROUP = "Casting atau labuh: pilih SATU"

# (badge name, position, group title, text, detail)
REQUIREMENTS = [
    (
        "Lencana Jurumudi (Helmsman)",
        1,
        None,
        "Pendayung buatan sendiri",
        "Membuat sebuah pendayung yang boleh digunakan dan diterima oleh Penguji daripada bahan-bahan yang terbuang, serta boleh menamakan bahagian pendayung tersebut.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        2,
        None,
        "Kain layar dan ikatan",
        "Menamakan bahagian kain layar dan kegunaannya; mengetahui perbezaan ikat hidup dan ikat mati (running and standing rigging).",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        3,
        None,
        "Mendayung atau melayarkan bot",
        "Berkemahiran mendayung ATAU melayarkan bot, dan tahu menggunakan sauh.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        4,
        None,
        "Istilah pelayaran",
        "Tahu dan memahami istilah dan syarat-syarat arahan yang digunakan dalam pelayaran (contoh: man over board, colors, sunset).",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        5,
        None,
        "Enjin sangkut (OBM)",
        "Boleh menyenggara, membaiki kerosakan enjin sangkut (OBM) yang ringan.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        6,
        None,
        "Menyimpan dan membaiki tali",
        "Menunjukkan cara menyimpan, menggulung dan membaiki kerosakan pada tali.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        7,
        None,
        "Carta dan kompas",
        "Boleh memahami dan membaca carta dengan pelbagai simbol (Buoyage, Wreck Marking System); mengetahui Steering Compass dan Compass Error; menentukan 'Transit Bearing' dan 'Cross Bearing'; arah sebenar dan arah kompas; menentukan arah yang dituju (course charting).",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        8,
        None,
        "Morse dan semaphore",
        "Boleh membaca Morse sekurang-kurangnya 6 perkataan seminit dan Semaphore sekurang-kurangnya 3 perkataan seminit.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        9,
        None,
        "Perahu layar Laser",
        "Memasang (assemble) sebuah perahu layar Laser dan menamakan bahagian-bahagiannya.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        10,
        None,
        "Mengesan jenis hujan",
        "Menghuraikan kaedah mengesan jenis hujan yang bakal turun sama ada lebat, ribut atau angin sahaja berdasarkan tiupan angin, arus dan keadaan awan.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        11,
        None,
        "Laut bergelora dan arus",
        "Menerangkan kepada Penguji tentang bila laut akan bergelora dan arah arus pada waktu tertentu.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        12,
        None,
        "Kesan letih akibat cuaca",
        "Mengetahui kesan-kesan buruk yang menyebabkan seseorang itu menjadi letih, penat, disebabkan oleh angin, udara yang sejuk dan angin.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        13,
        None,
        "Iklim Khatulistiwa dan monsun",
        "Menerangkan secara ringkas kepada Penguji tentang iklim Khatulistiwa dan jenis-jenis angin monsun yang bertiup di Malaysia.",
    ),
    (
        "Lencana Jurumudi (Helmsman)",
        14,
        None,
        "Rekod cuaca",
        "Menyimpan satu rekod berdasarkan pemerhatiannya setiap tiga hari sekali selama sekurang-kurangnya satu bulan: kekuatan angin (anemometer); jenis awan dan jumlah; udara dan tanda Beaufort; suhu (jangka suhu).",
    ),
    (
        "Lencana Pengail",
        1,
        None,
        "Keselamatan dalam air",
        "Mengetahui peraturan keselamatan dalam air, memahami bahaya air dan tindakan sebelum mengharunginya.",
    ),
    (
        "Lencana Pengail",
        2,
        None,
        "Mengail 6 kali",
        "Mengail di air tawar atau masin sekurang-kurangnya 6 kali dalam tempoh 3 bulan dengan rekod (ikan, ukuran, berat, cara tangkapan, umpan, cuaca).",
    ),
    (
        "Lencana Pengail",
        3,
        None,
        "Mengenali 20 jenis ikan",
        "Mengenali 20 jenis ikan air tawar atau air masin yang direkodkan dalam buku log.",
    ),
    (
        "Lencana Pengail",
        4,
        None,
        "Arah lubuk, umpan dan mata kail",
        "Mengetahui arah lubuk, umpan, saiz mata kail dan batu ladung yang sesuai.",
    ),
    (
        "Lencana Pengail",
        5,
        PENGAIL_GROUP,
        "Casting 6 kali",
        "Mengetahui cara mematikan lilit (casting) sekurang-kurangnya 6 kali berturut-turut sejauh 5 meter.",
    ),
    (
        "Lencana Pengail",
        6,
        PENGAIL_GROUP,
        "Labuh mata kail dengan batu ladung",
        "Melabuhkan mata kail dengan batu ladung ke dalam air sedalam 1 meter.",
    ),
    (
        "Lencana Pengail",
        7,
        None,
        "Alat mengail",
        "Mengenali sekurang-kurangnya 6 jenis alat mengail (joran, batu ladung, takal, tali kail, mata kail dll.).",
    ),
    (
        "Lencana Pengail",
        8,
        None,
        "Sotong dan ketam",
        "Mengenali ikan dan kehidupan laut yang lain (sotong dan ketam).",
    ),
    (
        "Lencana Pengail",
        9,
        None,
        "Kaedah yang tidak dibenarkan",
        "Menerangkan kepada Penguji tentang kaedah menangkap ikan yang tidak dibenarkan di Malaysia dan faktor-faktor pengharamannya.",
    ),
    (
        "Lencana Pengail",
        10,
        None,
        "Tangkap dan lepas",
        "Menerangkan kepada Penguji tentang kaedah tangkap dan lepas (catch and release) dan cara ia dilakukan.",
    ),
    (
        "Lencana Pengail",
        11,
        None,
        "Dua masakan hidupan laut",
        "Menyediakan dua masakan menggunakan hidupan laut, satu dengan kaedah biasa dan satu dengan kaedah survival.",
    ),
]


def upgrade() -> None:
    # 1. The pick-one group for Pengail items 5a and 5b
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position)
            select b.id, :title, 1, 5
            from badges b
            join levels l on l.id = b.level_id
            where b.name = 'Lencana Pengail'
              and l.name = 'Pengakap Remaja'
        """).bindparams(title=PENGAIL_GROUP)
    )
    # 2. The requirements, each attached to its group when it has one
    for badge_name, position, group_title, text, detail in REQUIREMENTS:
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
                  and l.name = 'Pengakap Remaja'
            """).bindparams(
                group_title=group_title,
                position=position,
                text=text,
                detail=detail,
                badge_name=badge_name,
            )
        )


def downgrade() -> None:
    op.execute(
        sa.text("""
            delete from requirements
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name in :names and l.name = 'Pengakap Remaja'
            )
        """).bindparams(sa.bindparam("names", value=LAUT_BADGES, expanding=True))
    )
    op.execute(
        sa.text("""
            delete from requirement_groups
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name = 'Lencana Pengail' and l.name = 'Pengakap Remaja'
            )
        """)
    )
