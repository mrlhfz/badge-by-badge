from app.enums import (
    AnimalKind,
    BadgeKind,
    EntryStatus,
    PinKind,
    Role,
    VerificationAction,
)


def test_role_values():
    assert [m.value for m in Role] == ["admin", "leader", "scout"]


def test_pin_kind_values():
    assert [m.value for m in PinKind] == ["leader", "scout"]


def test_entry_status_values():
    assert [m.value for m in EntryStatus] == ["pending", "confirmed"]


def test_verification_action_values():
    assert [m.value for m in VerificationAction] == ["verify", "unverify"]


def test_badge_kind_values():
    assert [m.value for m in BadgeKind] == ["compulsory", "skill"]


def test_animal_kind_values():
    assert [m.value for m in AnimalKind] == ["poultry", "other"]


def test_models_import():
    import app.models  # noqa: F401
