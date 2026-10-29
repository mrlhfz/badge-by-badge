import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.database import get_db
from app.enums import EntryStatus
from app.services import entries as entry_service
from app.services.entries import (
    assert_requirement_applies,
    assert_scout_can_change,
    delete_entry,
)
from app.services.scouts import get_current_scout
from main import app

LEVEL = uuid.uuid4()
OTHER_LEVEL = uuid.uuid4()
STREAM = uuid.uuid4()
OTHER_STREAM = uuid.uuid4()


def scout_with(scout_id):
    return SimpleNamespace(id=scout_id)


def entry_for(scout_id, entry_status=EntryStatus.Pending):
    return SimpleNamespace(scout_id=scout_id, status=entry_status)


# Stands in for a database session and records the order of its calls
class DeleteFakeDb:
    def __init__(self, comment_rows=1):
        self.calls = []
        self.statements = []
        self.comment_rows = comment_rows

    def execute(self, statement):
        self.calls.append("delete comments")
        self.statements.append(statement)
        return SimpleNamespace(rowcount=self.comment_rows)

    def delete(self, entry):
        self.calls.append("delete entry")

    def commit(self):
        self.calls.append("commit")


# Another Scout's entry looks the same as a missing one: 404
def test_scout_cannot_change_someone_elses_entry():
    scout = scout_with(uuid.uuid4())
    entry = entry_for(uuid.uuid4())
    with pytest.raises(HTTPException) as error:
        assert_scout_can_change(entry, scout)
    assert error.value.status_code == 404


# Confirmed entries are locked for the Scout
def test_confirmed_entry_cannot_be_changed():
    scout_id = uuid.uuid4()
    entry = entry_for(scout_id, EntryStatus.Confirmed)
    with pytest.raises(HTTPException) as error:
        assert_scout_can_change(entry, scout_with(scout_id))
    assert error.value.status_code == 409


# A Scout may change their own pending entry
def test_scout_can_change_own_pending_entry():
    scout_id = uuid.uuid4()
    # Passing without an error is the result; no HTTPException means allowed
    assert_scout_can_change(entry_for(scout_id), scout_with(scout_id))


# Deleting a pending entry with a comment removes the comment first, then the entry, in one commit
def test_delete_entry_with_comment_removes_comment_first():
    scout_id = uuid.uuid4()
    db = DeleteFakeDb(comment_rows=1)
    entry = SimpleNamespace(id=uuid.uuid4(), scout_id=scout_id, status=EntryStatus.Pending)
    delete_entry(db, entry, scout_with(scout_id))
    assert db.calls == ["delete comments", "delete entry", "commit"]
    # The comment delete must target only this entry's comments
    assert entry.id in db.statements[0].compile().params.values()


# Deleting a pending entry with no comments still goes ahead
def test_delete_entry_without_comments_still_deletes():
    scout_id = uuid.uuid4()
    db = DeleteFakeDb(comment_rows=0)
    entry = SimpleNamespace(id=uuid.uuid4(), scout_id=scout_id, status=EntryStatus.Pending)
    delete_entry(db, entry, scout_with(scout_id))
    assert db.calls == ["delete comments", "delete entry", "commit"]


# Deleting a pending entry through the route answers 204 with no body
def test_delete_route_returns_204_for_pending_entry_with_comment(monkeypatch):
    scout_id = uuid.uuid4()
    entry = SimpleNamespace(id=uuid.uuid4(), scout_id=scout_id, status=EntryStatus.Pending)
    monkeypatch.setattr(entry_service, "get_entry_or_404", lambda db, entry_id: entry)
    app.dependency_overrides[get_current_scout] = lambda: scout_with(scout_id)
    app.dependency_overrides[get_db] = lambda: DeleteFakeDb()
    try:
        response = TestClient(app).delete(f"/entries/{entry.id}")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 204


# A requirement on the Scout's level and stream is allowed
def test_requirement_on_current_level_and_stream_applies():
    assert_requirement_applies(None, LEVEL, STREAM, LEVEL)
    assert_requirement_applies(STREAM, LEVEL, STREAM, LEVEL)


# A requirement from another level is refused with 422
def test_requirement_from_other_level_is_refused():
    with pytest.raises(HTTPException) as error:
        assert_requirement_applies(None, OTHER_LEVEL, STREAM, LEVEL)
    assert error.value.status_code == 422


# A requirement from another stream is refused with 422
def test_requirement_from_other_stream_is_refused():
    with pytest.raises(HTTPException) as error:
        assert_requirement_applies(OTHER_STREAM, LEVEL, STREAM, LEVEL)
    assert error.value.status_code == 422


# A Scout with no current level is refused, rather than allowed by accident
def test_scout_without_current_level_is_refused():
    with pytest.raises(HTTPException) as error:
        assert_requirement_applies(None, LEVEL, STREAM, None)
    assert error.value.status_code == 422
