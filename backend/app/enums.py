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


class AnimalKind(Enum):
    Poultry = "poultry"
    Other = "other"


# How far a Scout has got with one badge; computed, not stored
class ProgressStatus(Enum):
    NotStarted = "not_started"
    InProgress = "in_progress"
    Complete = "complete"


# Where a Scout stands for the Tanda Cemerlang; computed, and the award itself happens outside the app
class TandaState(Enum):
    NotYet = "not_yet"
    Waiting = "waiting"
    Eligible = "eligible"
