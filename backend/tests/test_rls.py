import os

import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import engine

# Alembic's own version table is exempt from RLS (R4).
EXEMPT_TABLES = {"alembic_version"}
# pins has RLS on with no policies on purpose, so only the backend's service role can use it.
TABLES_WITHOUT_POLICIES = {"pins"}


def _skip_or_fail(message):
    # On CI a missing database is a failure, so a skipped check cannot pass unnoticed.
    if os.getenv("CI"):
        pytest.fail(message)
    pytest.skip(message)


def test_every_public_table_has_rls():
    query = text("""
        select c.relname, c.relrowsecurity
        from pg_class c
        join pg_namespace n on n.oid = c.relnamespace
        where n.nspname = 'public'
          and c.relkind = 'r'
    """)
    try:
        with engine.connect() as conn:
            tables = conn.execute(query).all()
    except OperationalError:
        _skip_or_fail("database is not reachable, so the RLS check did not run")

    # An empty database would pass the RLS check without checking anything, so fail instead.
    assert tables, "no public tables found, so the RLS check did not test anything"

    tables_without_rls = {name for name, has_rls in tables if not has_rls}
    assert tables_without_rls <= EXEMPT_TABLES, (
        f"tables without RLS: {sorted(tables_without_rls - EXEMPT_TABLES)}"
    )


def test_every_public_table_has_a_policy():
    # RLS on with no policy blocks every row, so a table can pass the flag check and still be unusable.
    query = text("""
        select c.relname
        from pg_class c
        join pg_namespace n on n.oid = c.relnamespace
        where n.nspname = 'public'
          and c.relkind = 'r'
          and c.relname not in (
              select tablename from pg_policies where schemaname = 'public'
          )
    """)
    try:
        with engine.connect() as conn:
            tables_without_policy = set(conn.execute(query).scalars().all())
    except OperationalError:
        _skip_or_fail("database is not reachable, so the RLS policy check did not run")

    tables_without_policy -= EXEMPT_TABLES | TABLES_WITHOUT_POLICIES
    assert not tables_without_policy, (
        f"tables with RLS but no policy: {sorted(tables_without_policy)}"
    )
