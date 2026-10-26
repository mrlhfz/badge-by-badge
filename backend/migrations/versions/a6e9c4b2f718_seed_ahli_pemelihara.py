"""seed Ahli Pemelihara requirements: six required items, no groups

Revision ID: a6e9c4b2f718
Revises: f1d7a3c8e462
Create Date: 2026-10-26 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a6e9c4b2f718"
down_revision: str | Sequence[str] | None = "f1d7a3c8e462"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Pemelihara"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Tujuan pemeliharaan dan tanah",
        "Mengetahui: a) tujuan pemeliharaan termasuk usaha pertubuhan pemeliharaan di negara ini; b) 5 jenis tanah dan sebab utama tanah boleh terhakis; c) membandingkan akibat hujan yang terlalu banyak dengan akibat kemarau yang berpanjangan.",
    ),
    (
        2,
        "Pencemaran udara dan air",
        "Mengetahui sebab utama udara dan air tercemar dan akibatnya, serta cara mengawal pencemaran itu.",
    ),
    (
        3,
        "Hubungan tumbuhan, binatang dan manusia",
        "Mengetahui bagaimana tumbuhan, binatang dan manusia ada hubungan antara satu sama lain.",
    ),
    (
        4,
        "Kerosakan alam semula jadi",
        "Memberi empat contoh bagaimana alam semula jadi boleh rosak dan musnah, dua daripadanya dalam kawasan Pengakap itu sendiri, serta menyatakan cara pemeliharaan bagi mengelakkan atau mencegah kerosakan dan kemusnahan itu.",
    ),
    (
        5,
        "Kajian dua kawasan",
        "Membuat: a) satu kajian bagi dua kawasan yang berlainan, satu daripadanya kawasan yang selalu digunakan oleh orang ramai, sekurang-kurangnya dua hari bagi setiap kawasan dan boleh dibuat pada hujung minggu; b) dengan lukisan, menerangkan kepada Penilai hasil kajian: i) penggunaan tanah pada masa lampau dan sekarang; ii) penilaian penggunaan tanah dari segi kemudahan, kemunduran dan kepulihan alam; iii) pemeliharaan hidupan liar (binatang atau tumbuhan); iv) perselisihan antara berbagai-bagai pengguna. Kajian boleh dibuat seorang diri atau bersama seorang Pengakap lain, dengan laporan yang berasingan.",
    ),
    (
        6,
        "Projek pemeliharaan alam sekitar",
        "Mengambil bahagian dalam satu projek pemeliharaan alam sekitar selama sekurang-kurangnya tiga bulan.",
    ),
]


def upgrade() -> None:
    for position, text, detail in REQUIREMENTS:
        op.execute(
            sa.text("""
                insert into requirements (badge_id, stream_id, group_id, position, text, detail)
                select b.id, null, null, :position, :text, :detail
                from badges b
                join levels l on l.id = b.level_id
                where b.name = :badge_name
                  and l.name = 'Pengakap Muda'
                  and b.stream_id is null
            """).bindparams(
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
