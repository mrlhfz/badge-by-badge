from enum import Enum


class Role(Enum):
    Admin = "admin"
    Leader = "leader"
    Scout = "scout"


class PinKind(Enum):
    Leader = "leader"
    Scout = "scout"


class EntryStatus(Enum):
    Pending = "pending"
    Confirmed = "confirmed"


class VerificationAction(Enum):
    Verify = "verify"
    Unverify = "unverify"


class BadgeKind(Enum):
    Compulsory = "compulsory"
    Skill = "skill"
