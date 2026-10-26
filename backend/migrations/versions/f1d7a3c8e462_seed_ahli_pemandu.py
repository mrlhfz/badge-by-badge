"""seed Ahli Pemandu requirements: four required items, no groups

Revision ID: f1d7a3c8e462
Revises: e8c2f5a9d031
Create Date: 2026-10-26 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1d7a3c8e462"
down_revision: str | Sequence[str] | None = "e8c2f5a9d031"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Pemandu"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Arah jalan ke tempat yang ditentukan",
        "Menunjukkan kepada Penilai arah jalan yang mudah diikuti ke tempat yang ditentukan.",
    ),
    (
        2,
        "Peta kasar tempat penting",
        "Membuat sebuah peta kasar dengan menandakan tempat-tempat penting dan utama: a) kediaman doktor, doktor haiwan, doktor gigi, hospital, klinik dan ambulan; b) Balai Bomba, Balai Polis, Pejabat Pos, pondok telefon dan bengkel motokar; c) perhentian bas, stesen keretapi, jalan bas dan keretapi ke tempat yang berhampiran, serta jadual perjalanannya; d) Ibu Pejabat Pengakap, tempat perhimpunan awam, kebun bunga, pawagam, tempat beribadat, muzium dan tempat menarik dan bersejarah; e) kediaman Pesuruhjaya Pengakap Daerah, penolong-penolongnya, pemimpin dan penolong pemimpin kumpulan, serta ahli patrolnya.",
    ),
    (
        3,
        "Menggunakan peta",
        "Menggunakan peta untuk pergi ke tempat yang diarahkan oleh Penilai.",
    ),
    (
        4,
        "Arah jalan ke tapak perkhemahan",
        "Mengarahkan dengan jelas arah jalan yang mudah diikuti oleh pelawat ke tempat perkhemahan yang jauhnya lebih kurang 8 kilometer, dengan kenderaan awam, berbasikal atau berkereta.",
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
