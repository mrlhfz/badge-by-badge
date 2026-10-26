"""seed required_skill_counts

Revision ID: a1f4c9e27d13
Revises: 3c8e1f5a9b72
Create Date: 2026-10-25 10:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1f4c9e27d13"
down_revision: str | Sequence[str] | None = "3c8e1f5a9b72"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (level name, stream name, required skill badges)
REQUIRED_SKILL_COUNTS = [
    ("Pengakap Muda", "Pengakap", 8),
    ("Pengakap Muda", "Pengakap Laut", 8),
    ("Pengakap Remaja", "Pengakap", 0),
    ("Pengakap Remaja", "Pengakap Laut", 0),
]


def _values(rows: list[tuple]) -> str:
    """Turn Python tuples into a SQL VALUES list, with quotes doubled."""
    return ", ".join(
        "(" + ", ".join("'" + str(v).replace("'", "''") + "'" for v in row) + ")"
        for row in rows
    )


def upgrade() -> None:
    op.execute(f"""
        insert into required_skill_counts (level_id, stream_id, required_count)
        select l.id, s.id, v.required_count::int
        from (values {_values(REQUIRED_SKILL_COUNTS)}) as v(level_name, stream_name, required_count)
        join levels l on l.name = v.level_name
        join streams s on s.name = v.stream_name
    """)


def downgrade() -> None:
    op.execute("""
        delete from required_skill_counts
        where level_id in (
            select id from levels where name in ('Pengakap Muda', 'Pengakap Remaja')
        )
    """)
