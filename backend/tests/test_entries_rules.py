import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.enums import EntryStatus
from app.services.entries import assert_scout_can_change


def scout_with(scout_id):
    return SimpleNamespace(id=scout_id)


def entry_for(scout_id, entry_status=EntryStatus.Pending):
    return SimpleNamespace(scout_id=scout_id, status=entry_status)


# A Scout may not change another Scout's entry
def test_scout_cannot_change_someone_elses_entry():
    scout = scout_with(uuid.uuid4())
    entry = entry_for(uuid.uuid4())
    with pytest.raises(HTTPException) as error:
        assert_scout_can_change(entry, scout)
    assert error.value.status_code == 403


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
