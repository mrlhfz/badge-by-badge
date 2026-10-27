import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.enums import EntryStatus
from app.services.entries import assert_requirement_applies, assert_scout_can_change

LEVEL = uuid.uuid4()
OTHER_LEVEL = uuid.uuid4()
STREAM = uuid.uuid4()
OTHER_STREAM = uuid.uuid4()


def scout_with(scout_id):
    return SimpleNamespace(id=scout_id)


def entry_for(scout_id, entry_status=EntryStatus.Pending):
    return SimpleNamespace(scout_id=scout_id, status=entry_status)


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
