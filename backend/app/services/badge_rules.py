import uuid
from dataclasses import dataclass


# One requirement, as the completion rule sees it
@dataclass(frozen=True)
class RuleRequirement:
    id: uuid.UUID
    group_id: uuid.UUID | None
    stream_id: uuid.UUID | None


# One requirement group and how many of its requirements must be done
@dataclass(frozen=True)
class RuleGroup:
    id: uuid.UUID
    pick_count: int


# A badge is complete when every ungrouped requirement is confirmed and each group
# has enough confirmed picks. Only requirements for the Scout's stream count.
def badge_is_complete(
    requirements: list[RuleRequirement],
    groups: list[RuleGroup],
    confirmed_ids: set[uuid.UUID],
    scout_stream_id: uuid.UUID,
) -> bool:
    applies = [r for r in requirements if r.stream_id in (None, scout_stream_id)]

    # Requirements outside any group must all be confirmed
    for requirement in applies:
        if requirement.group_id is None and requirement.id not in confirmed_ids:
            return False

    # Each group needs at least pick_count confirmed requirements
    for group in groups:
        in_group = [r for r in applies if r.group_id == group.id]
        if not in_group:
            continue
        done = sum(1 for r in in_group if r.id in confirmed_ids)
        if done < group.pick_count:
            return False

    return True
