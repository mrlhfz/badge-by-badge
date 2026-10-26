"""stop duplicate badge names: unique per level and stream, with stream-less badges checked separately

Revision ID: a3d6e1f9c482
Revises: f2c8a6e4d917
Create Date: 2026-10-27 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3d6e1f9c482"
down_revision: str | Sequence[str] | None = "f2c8a6e4d917"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Stop before creating the indexes if any duplicate names already exist, so the list can be fixed first.
    duplicates = (
        op.get_bind()
        .execute(
            sa.text("""
            select count(*) from (
                select level_id, stream_id, name
                from badges
                group by level_id, stream_id, name
                having count(*) > 1
            ) d
        """)
        )
        .scalar()
    )
    if duplicates:
        raise RuntimeError(
            f"{duplicates} duplicate badge name(s) found; fix them before this migration runs"
        )

    # A plain unique constraint treats two NULL stream ids as different, so stream-less badges get their own index.
    op.execute("""
        create unique index uq_badges_level_name
        on badges (level_id, name)
        where stream_id is null
    """)
    op.execute("""
        create unique index uq_badges_level_stream_name
        on badges (level_id, stream_id, name)
        where stream_id is not null
    """)


def downgrade() -> None:
    op.execute("drop index if exists uq_badges_level_stream_name")
    op.execute("drop index if exists uq_badges_level_name")
