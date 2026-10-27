import re
from pathlib import Path

from app.enums import (
    AnimalKind,
    BadgeKind,
    EntryStatus,
    PinKind,
    ProgressStatus,
    Role,
    TandaState,
    VerificationAction,
)

FRONTEND_ENUMS = Path(__file__).resolve().parents[2] / "frontend" / "src" / "enums.ts"
MIRRORED_ENUMS = [
    Role,
    PinKind,
    EntryStatus,
    VerificationAction,
    BadgeKind,
    AnimalKind,
    ProgressStatus,
    TandaState,
]


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


def test_progress_status_values():
    assert [m.value for m in ProgressStatus] == ["not_started", "in_progress", "complete"]


def test_models_import():
    import app.models  # noqa: F401


def test_frontend_mirror_matches_backend():
    # Each enum in enums.ts is an `export const Name = { Key: "value", ... } as const;` block.
    source = FRONTEND_ENUMS.read_text(encoding="utf-8")
    blocks = dict(
        re.findall(r"export const (\w+) = \{(.*?)\} as const;", source, re.DOTALL)
    )

    for enum_class in MIRRORED_ENUMS:
        frontend_members = dict(
            re.findall(r'(\w+):\s*"([^"]*)"', blocks[enum_class.__name__])
        )
        assert frontend_members == {m.name: m.value for m in enum_class}, (
            enum_class.__name__
        )
