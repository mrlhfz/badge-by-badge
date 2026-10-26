import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import engine

# Alembic's own version table is exempt from RLS (R4).
EXEMPT_TABLES = {"alembic_version"}


def test_every_public_table_has_rls():
    query = text("""
        select c.relname
        from pg_class c
        join pg_namespace n on n.oid = c.relnamespace
        where n.nspname = 'public'
          and c.relkind = 'r'
          and not c.relrowsecurity
    """)
    try:
        with engine.connect() as conn:
            tables_without_rls = set(conn.execute(query).scalars().all())
    except OperationalError:
        pytest.skip("database is not reachable, so the RLS check did not run")

    assert tables_without_rls <= EXEMPT_TABLES, (
        f"tables without RLS: {sorted(tables_without_rls - EXEMPT_TABLES)}"
    )
