"""move Remaja Jayadiri, Ekspedisi and Perkhidmatan to general and seed their requirements

Revision ID: d5e0b38a1c94
Revises: b7d2e90c4f18
Create Date: 2026-10-25 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5e0b38a1c94"
down_revision: str | Sequence[str] | None = "b7d2e90c4f18"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

GENERAL_BADGES = ["Lencana Jayadiri", "Lencana Ekspedisi", "Lencana Perkhidmatan"]

EKSPEDISI_GROUP = "Ekspedisi: pilih SATU"

# (badge name, position, group title, text, detail)
REQUIREMENTS = [
    (
        "Lencana Jayadiri",
        1,
        None,
        "Fungsi Parlimen",
        "Mengetahui fungsi-fungsi Parlimen.",
    ),
    (
        "Lencana Jayadiri",
        2,
        None,
        "Bendera dan Lambang Negeri",
        "Melukis dan menerangkan rupabentuk bendera semua Negeri dalam Malaysia dan mengetahui Lambang Malaysia dan Lambang Negeri masing-masing.",
    ),
    (
        "Lencana Jayadiri",
        3,
        None,
        "Fungsi agensi Kerajaan",
        "Menerangkan fungsi satu daripada agensi Kerajaan atau badan berkanun seperti UDA, MARDI, MARA, FELDA, LPN, PETRONAS dan lain-lain.",
    ),
    (
        "Lencana Jayadiri",
        4,
        None,
        "Peta negeri dan kawasan Parlimen",
        "Melukis peta negeri masing-masing dan menunjukkan kawasan Parlimen serta nama Ahli Parlimen yang berkenaan.",
    ),
    (
        "Lencana Jayadiri",
        5,
        None,
        "Buku Log Pengakap",
        "Mempunyai Buku Log Pengakap yang kemas kini.",
    ),
    (
        "Lencana Perkhidmatan",
        1,
        None,
        "Menyelamatkan nyawa",
        "Lulus dan mempunyai SATU sijil daripada: Pertolongan Cemas (Sijil Peringkat Asas, Pegawai Perubatan / St John / Bulan Sabit Merah / JPAM); Pemadam Api (Sijil Asas Kebombaan, Jabatan Bomba); Penyelamat Nyawa (Bronze Medallion).",
    ),
    (
        "Lencana Perkhidmatan",
        2,
        None,
        "Perkhidmatan masyarakat",
        "Membuat kerja amal yang diakui kepada masyarakat berjumlah 24 jam dalam tempoh 9 hingga 12 bulan (dalam Perkhemahan Daerah, Negeri, Kebangsaan, banjir, bencana, rumah ibadat, rumah kebajikan, dll.).",
    ),
    (
        "Lencana Ekspedisi",
        1,
        None,
        "Latihan ekspedisi",
        "Keperluan peribadi dan patrol; beg membawa tidak lebih 15 kg termasuk 10 kg makanan (haversack).",
    ),
    (
        "Lencana Ekspedisi",
        2,
        EKSPEDISI_GROUP,
        "Berjalan kaki 4 hari 3 malam (80 km) atau berbasikal 150 km",
        "Mengambil bahagian dalam satu ekspedisi berpatrol (4 hingga 7 orang) dengan berjalan kaki selama 4 hari 3 malam sejauh 80 km ATAU 150 km berbasikal dengan melaksanakan tugasan.",
    ),
    (
        "Lencana Ekspedisi",
        3,
        EKSPEDISI_GROUP,
        "Perjalanan meliputi jalan raya, jalan desa dan hutan berbukit-bukau",
        "Perjalanan hendaklah meliputi jalan raya, jalan desa, hutan berbukit-bukau.",
    ),
    (
        "Lencana Ekspedisi",
        4,
        EKSPEDISI_GROUP,
        "Bermalam di satu lokasi dengan khemah",
        "Bermalam di satu lokasi, mendirikan khemah dan menyediakan makan malam dan sarapan secara 'backwoods' atau seumpamanya.",
    ),
    (
        "Lencana Ekspedisi",
        5,
        EKSPEDISI_GROUP,
        "Pengembaraan malam 3 jam",
        "Perjalanan meliputi pengembaraan malam tidak kurang 3 jam.",
    ),
    (
        "Lencana Ekspedisi",
        6,
        EKSPEDISI_GROUP,
        "Berjalan kaki bersama patrol 40 km dalam 24 jam",
        "Berjalan kaki bersama patrol (4-7 orang) tidak kurang 40 km dalam masa 24 jam terus-menerus dengan melaksanakan tugasan.",
    ),
    (
        "Lencana Ekspedisi",
        7,
        EKSPEDISI_GROUP,
        "Perjalanan di pinggiran bandar, desa atau luar bandar",
        "Perjalanan hendaklah meliputi pinggiran bandar, desa atau luar bandar.",
    ),
    (
        "Lencana Ekspedisi",
        8,
        EKSPEDISI_GROUP,
        "Masa rehat 2 jam untuk memasak",
        "Masa rehat diberikan selama 2 jam bagi menyediakan makanan yang disediakan secara 'backwoods' atau seumpamanya.",
    ),
    (
        "Lencana Ekspedisi",
        9,
        EKSPEDISI_GROUP,
        "Ekspedisi diakhiri dengan pengembaraan malam 10 jam",
        "Ekspedisi ini diakhiri dengan pengembaraan malam selama 10 jam.",
    ),
    (
        "Lencana Ekspedisi",
        10,
        EKSPEDISI_GROUP,
        "Berakit, berkayak atau berdayung 50 km",
        "Berakit, berkayak atau berdayung sejauh 50 km selama 4 hari 3 malam di sungai atau persisiran pantai.",
    ),
    (
        "Lencana Ekspedisi",
        11,
        EKSPEDISI_GROUP,
        "Mendaki gunung 3 hari 2 malam",
        "Mendaki gunung selama 3 hari 2 malam (mengikut keadaan tempatan) tidak kurang 4,500 kaki dari aras laut.",
    ),
    (
        "Lencana Ekspedisi",
        12,
        None,
        "Laporan Log Ekspedisi",
        "Menyediakan laporan bertulis Log Ekspedisi mengikut format yang disediakan oleh Persekutuan Pengakap Malaysia.",
    ),
    (
        "Lencana Ekspedisi",
        13,
        None,
        "Tugasan perjalanan",
        "Tugasan tertentu yang berkait dengan perjalanan ekspedisi.",
    ),
    (
        "Lencana Ekspedisi",
        14,
        None,
        "Laporan dengan gambar atau video",
        "Laporan perjalanan dan tugasan hendaklah disokong dengan gambar, rakaman atau video.",
    ),
    (
        "Lencana Ekspedisi",
        15,
        None,
        "Hantar Log kepada Pemimpin Kumpulan",
        "Log Ekspedisi hendaklah dihantar untuk disemak oleh Pemimpin Kumpulan tidak lewat 10 hari selepas ekspedisi.",
    ),
]


def upgrade() -> None:
    # 1. Stop these badges being Laut-only. They become general (stream_id null).
    op.execute(
        sa.text("""
            update badges
            set stream_id = null
            where name in :names
              and level_id = (select id from levels where name = 'Pengakap Remaja')
              and stream_id = (select id from streams where name = 'Pengakap Laut')
        """).bindparams(sa.bindparam("names", value=GENERAL_BADGES, expanding=True))
    )
    # 2. The Ekspedisi pick-one group (option 2 in the book)
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position)
            select b.id, :title, 1, 2
            from badges b
            join levels l on l.id = b.level_id
            where b.name = 'Lencana Ekspedisi'
              and l.name = 'Pengakap Remaja'
              and b.stream_id is null
        """).bindparams(title=EKSPEDISI_GROUP)
    )
    # 3. The requirements, each attached to its group when it has one
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
                  and b.stream_id is null
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
                where b.name in :names and l.name = 'Pengakap Remaja' and b.stream_id is null
            )
        """).bindparams(sa.bindparam("names", value=GENERAL_BADGES, expanding=True))
    )
    op.execute(
        sa.text("""
            delete from requirement_groups
            where badge_id in (
                select b.id from badges b
                join levels l on l.id = b.level_id
                where b.name = 'Lencana Ekspedisi' and l.name = 'Pengakap Remaja' and b.stream_id is null
            )
        """)
    )
    op.execute(
        sa.text("""
            update badges
            set stream_id = (select id from streams where name = 'Pengakap Laut')
            where name in :names
              and level_id = (select id from levels where name = 'Pengakap Remaja')
              and stream_id is null
        """).bindparams(sa.bindparam("names", value=GENERAL_BADGES, expanding=True))
    )
