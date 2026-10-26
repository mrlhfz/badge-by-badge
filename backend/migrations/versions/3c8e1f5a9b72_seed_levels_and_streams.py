"""seed levels, streams and level_streams

Revision ID: 3c8e1f5a9b72
Revises: 579a51626f80
Create Date: 2026-10-25 09:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3c8e1f5a9b72"
down_revision: str | Sequence[str] | None = "579a51626f80"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LEVELS = [
    ("Pengakap Lebah", 1, "Lencana Lebah"),
    ("Pengakap Kanak-Kanak", 2, "Anugerah Rambu Pengakap Kanak-Kanak"),
    ("Pengakap Muda", 3, "Anugerah Rambu Pengakap Muda"),
    ("Pengakap Remaja", 4, "Anugerah Pengakap Raja"),
    ("Pengakap Kelana", 5, "Anugerah BP Award"),
]

STREAMS = ["Pengakap", "Pengakap Laut", "Pengakap Udara", "Pengakap Khas"]

# Which streams are open at each level (docs/mvp-spec.md, Streams table).
LEVEL_STREAMS = [
    ("Pengakap Lebah", "Pengakap"),
    ("Pengakap Lebah", "Pengakap Khas"),
    ("Pengakap Kanak-Kanak", "Pengakap"),
    ("Pengakap Kanak-Kanak", "Pengakap Laut"),
    ("Pengakap Kanak-Kanak", "Pengakap Khas"),
    ("Pengakap Muda", "Pengakap"),
    ("Pengakap Muda", "Pengakap Laut"),
    ("Pengakap Muda", "Pengakap Udara"),
    ("Pengakap Muda", "Pengakap Khas"),
    ("Pengakap Remaja", "Pengakap"),
    ("Pengakap Remaja", "Pengakap Laut"),
    ("Pengakap Remaja", "Pengakap Udara"),
    ("Pengakap Remaja", "Pengakap Khas"),
    ("Pengakap Kelana", "Pengakap"),
    ("Pengakap Kelana", "Pengakap Laut"),
    ("Pengakap Kelana", "Pengakap Udara"),
    ("Pengakap Kelana", "Pengakap Khas"),
]


def _values(rows: list[tuple]) -> str:
    """Turn Python tuples into a SQL VALUES list, with quotes doubled."""
    return ", ".join(
        "(" + ", ".join("'" + str(v).replace("'", "''") + "'" for v in row) + ")"
        for row in rows
    )


def upgrade() -> None:
    op.execute(
        f"insert into levels (name, sort_order, top_award) values {_values(LEVELS)}"
    )
    op.execute(f"insert into streams (name) values {_values([(s,) for s in STREAMS])}")
    op.execute(f"""
        insert into level_streams (level_id, stream_id)
        select l.id, s.id
        from (values {_values(LEVEL_STREAMS)}) as pairs(level_name, stream_name)
        join levels l on l.name = pairs.level_name
        join streams s on s.name = pairs.stream_name
    """)


def downgrade() -> None:
    op.execute(f"""
        delete from level_streams
        where level_id in (
            select id from levels where name in ({", ".join(f"'{n}'" for n, _, _ in LEVELS)})
        )
    """)
    op.execute(f"""
        delete from levels
        where name in ({", ".join(f"'{n}'" for n, _, _ in LEVELS)})
    """)
    op.execute(f"""
        delete from streams
        where name in ({", ".join(f"'{s}'" for s in STREAMS)})
    """)
