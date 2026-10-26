"""index troop_id columns, restrict RLS helper functions, and trigger entries.updated_at

Revision ID: b9e4f2a7c136
Revises: a3d6e1f9c482
Create Date: 2026-10-26 10:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b9e4f2a7c136"
down_revision: str | Sequence[str] | None = "a3d6e1f9c482"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # RLS policies filter these columns on every leader read.
    op.create_index("ix_scouts_troop_id", "scouts", ["troop_id"])
    op.create_index("ix_troop_leaders_troop_id", "troop_leaders", ["troop_id"])

    # Security-definer helpers are reachable through the API by default. Only signed-in users need them.
    op.execute("revoke execute on function app_role() from public, anon")
    op.execute("grant execute on function app_role() to authenticated")
    op.execute("revoke execute on function leader_troop_ids() from public, anon")
    op.execute("grant execute on function leader_troop_ids() to authenticated")

    # The trigger sets updated_at for every writer, including raw SQL and the dashboard.
    op.execute("""
        create or replace function set_entries_updated_at() returns trigger
        language plpgsql set search_path = ''
        as $$
        begin
            new.updated_at = now();
            return new;
        end;
        $$;
    """)
    op.execute("""
        create trigger entries_set_updated_at
        before update on entries
        for each row execute function set_entries_updated_at();
    """)


def downgrade() -> None:
    op.execute("drop trigger if exists entries_set_updated_at on entries")
    op.execute("drop function if exists set_entries_updated_at()")

    op.execute("grant execute on function leader_troop_ids() to public, anon")
    op.execute("grant execute on function app_role() to public, anon")

    op.drop_index("ix_troop_leaders_troop_id", table_name="troop_leaders")
    op.drop_index("ix_scouts_troop_id", table_name="scouts")
