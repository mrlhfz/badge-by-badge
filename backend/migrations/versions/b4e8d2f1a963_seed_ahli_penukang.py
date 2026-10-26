"""seed Ahli Penukang requirements: pick three of five parts (A to E)

Revision ID: b4e8d2f1a963
Revises: f9a3c6e1b852
Create Date: 2026-10-26 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4e8d2f1a963"
down_revision: str | Sequence[str] | None = "f9a3c6e1b852"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Penukang"

PARENT = "Pilih TIGA bahagian: A, B, C, D atau E"

# (title, pick_count, position, parent title)
GROUPS = [
    (PARENT, 3, 1, None),
    ("Bahagian A: Pembuat Bakul", 2, 2, PARENT),
    ("Bahagian B: Penjilid Buku", 5, 3, PARENT),
    ("Bahagian C: Ahli Penyambung", 6, 4, PARENT),
    ("Bahagian D: Tukang Kulit", 3, 5, PARENT),
    ("Bahagian E: Percetakan", 3, 6, PARENT),
]

# (group title, position, text, detail)
REQUIREMENTS = [
    (
        "Bahagian A: Pembuat Bakul",
        1,
        "Membuat bakul daripada rotan, rumput atau jerami",
        "Membuat sendiri benda yang boleh digunakan sebagai bakul daripada rotan, rumput atau jerami.",
    ),
    (
        "Bahagian A: Pembuat Bakul",
        2,
        "Bahan mentah bakul dan prosesnya",
        "Mengetahui di mana boleh didapati bahan mentah yang digunakan untuk membuat bakul dan bagaimana ia diproses.",
    ),
    (
        "Bahagian B: Penjilid Buku",
        3,
        "Tugas memelihara bahan bacaan",
        "Memelihara berbagai bahan bacaan seperti buku, majalah dan nota.",
    ),
    (
        "Bahagian B: Penjilid Buku",
        4,
        "Teknik, media dan proses penjilidan",
        "Teknik, media dan proses.",
    ),
    (
        "Bahagian B: Penjilid Buku",
        5,
        "Kemasan dan persembahan",
        "Ketepatan dan kebersihan bekerja; hiasan pada kertas rusuk.",
    ),
    (
        "Bahagian B: Penjilid Buku",
        6,
        "Penilaian penjilidan buku",
        "a) Pengetahuan: konsep, prinsip dan aplikasinya. b) Proses atau tatacara. c) Hasil kerja: kemasan, ketahanan, kebersihan.",
    ),
    (
        "Bahagian B: Penjilid Buku",
        7,
        "Pemeliharaan dan penjagaan buku",
        "a) Cara menyimpan buku. b) Cara menggunakan buku.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        8,
        "Memasukkan skru sedalam 3.5 cm",
        "Memasukkan skru sedalam 3.5 cm tanpa merosakkan kayu atau skru itu.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        9,
        "Memaku penutup peti (ensel)",
        "Memaku penutup peti (ensel) dengan betul, menggunakan papan tebal 2 cm dan paku panjang 3.5 cm.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        10,
        "Membentuk sekeping papan",
        "Membentuk sekeping papan 2.5 cm tebal dan 60 cm panjang dengan gergaji biasa; pembelahan hendaklah lurus dan serongnya tidak boleh lebih daripada 1.6 mm.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        11,
        "Mengasah pahat dan ketam",
        "Mengasah pahat dan ketam, membuat lubang tanggam dan sambungan separuh.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        12,
        "Membuat bangku (stool) atau kerusi",
        "Membuat sebuah bangku (stool) atau kerusi.",
    ),
    (
        "Bahagian C: Ahli Penyambung",
        13,
        "Mengetahui jenis kayu",
        "2 jenis kayu lembut, 2 jenis kayu sederhana keras dan 3 jenis kayu keras.",
    ),
    (
        "Bahagian D: Tukang Kulit",
        14,
        "Membuat tumit sepatu atau barang kulit",
        "Membuat tumit sepatu dengan bahan kulit, dijahit atau dipakukan; ATAU mengadakan satu barang sahaja yang dibuat sendiri: rantai kunci, wogel, sarung kapak/pisau atau dompet wang yang dihiasi corak berwarna.",
    ),
    (
        "Bahagian D: Tukang Kulit",
        15,
        "Alatan dan bahan kulit",
        "Mengetahui alatan dan bahan yang digunakan untuk membuat barang yang dipilihnya itu.",
    ),
    (
        "Bahagian D: Tukang Kulit",
        16,
        "Jenis kulit dan cara memilihnya",
        "Mengetahui jenis kulit yang biasa digunakan dan cara memilihnya.",
    ),
    (
        "Bahagian E: Percetakan",
        17,
        "Rangka dan cetakan surat sebaran",
        "Mengatur satu rangka surat sebaran, menaip dan mencetak surat sebaran itu.",
    ),
    (
        "Bahagian E: Percetakan",
        18,
        "Jenis huruf percetakan",
        "Mengenali jenis huruf percetakan mengikut saiz (point-system) dan namakan enam jenis.",
    ),
    (
        "Bahagian E: Percetakan",
        19,
        "Tanda pembetulan dan jenis kertas",
        "Mengetahui semua tanda pembetulan dalam percetakan serta nama berbagai bentuk kertas yang berlainan jenis dan ukurannya.",
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


def _insert_requirement(group_title: str, position: int, text: str, detail: str) -> None:
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
