"""seed Ahli Perhutanan requirements: six required items, no groups

Revision ID: c7d1a5e9b204
Revises: b4e8d2f1a963
Create Date: 2026-10-26 11:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7d1a5e9b204"
down_revision: str | Sequence[str] | None = "b4e8d2f1a963"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BADGE_NAME = "Ahli Perhutanan"

# (position, text, detail)
REQUIREMENTS = [
    (
        1,
        "Mengenali pokok tempatan",
        "Mengenali 15 jenis pokok tempatan dan juga mengenali pokok-pokok yang lain dengan berpandukan bahan rujukan.",
    ),
    (
        2,
        "Menanam dan memelihara pokok",
        "Mengetahui menanam dan memelihara pokok dan tumbuh-tumbuhan dengan teratur, dengan menerangkan tiap-tiap peringkat yang mustahak seperti membatas, merumput, membaja dan lain-lain sebab berbuat demikian; memahami akibat yang berlaku kepada pokok dan tumbuhan disebabkan kena api, masalah cuaca dan dibinasakan oleh binatang atau serangga.",
    ),
    (
        3,
        "Tapak semaian",
        "Menyediakan tapak semaian dengan baja yang sesuai bagi pokok yang ditanam dan mengetahui mengahwin atau mencantum pokok.",
    ),
    (
        4,
        "Kapak dan keselamatan",
        "Mengetahui cara memilih dan menggunakan kapak, menjaganya serta mengetahui peraturan keselamatan berkenaan dengan menggunakan dan menyimpan kapak.",
    ),
    (
        5,
        "Menebang pokok",
        "Menebang sebatang pokok, memotong dahan dan ranting serta menyusunnya dengan kemas potongan itu.",
    ),
    (
        6,
        "Kajian tumbuh-tumbuhan",
        "Membuat kajian tumbuh-tumbuhan di Hutan Simpanan Kerajaan / Hutan Lipur.",
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
