import uuid
from dataclasses import dataclass


# One requirement, as the completion rule sees it
@dataclass(frozen=True)
class RuleRequirement:
    id: uuid.UUID
    group_id: uuid.UUID | None
    stream_id: uuid.UUID | None


# One requirement group, as the completion rule sees it
@dataclass(frozen=True)
class RuleGroup:
    id: uuid.UUID
    parent_group_id: uuid.UUID | None
    pick_count: int
    applies_when_poultry: bool


# A badge is complete when every ungrouped requirement is confirmed and every top-level group is satisfied.
# Only requirements for the Scout's stream count. A poultry-only group counts only for a Scout who keeps poultry.
def badge_is_complete(
    requirements: list[RuleRequirement],
    groups: list[RuleGroup],
    confirmed_ids: set[uuid.UUID],
    scout_stream_id: uuid.UUID,
    keeps_poultry: bool,
) -> bool:
    applies = [r for r in requirements if r.stream_id in (None, scout_stream_id)]
    active = [g for g in groups if keeps_poultry or not g.applies_when_poultry]

    # Requirements outside any group must all be confirmed
    for requirement in applies:
        if requirement.group_id is None and requirement.id not in confirmed_ids:
            return False

    # Each top-level group that has something to do for this Scout must be satisfied
    return all(
        _group_satisfied(group, applies, active, confirmed_ids)
        for group in active
        if group.parent_group_id is None and _has_items(group, applies, active)
    )


# A group is satisfied when its confirmed requirements plus its satisfied subgroups reach pick_count.
# Subgroups with nothing to do for this Scout are skipped, so they don't block the parent.
def _group_satisfied(
    group: RuleGroup,
    applies: list[RuleRequirement],
    active: list[RuleGroup],
    confirmed_ids: set[uuid.UUID],
) -> bool:
    direct_done = sum(
        1 for r in applies if r.group_id == group.id and r.id in confirmed_ids
    )
    subgroups_done = sum(
        1
        for child in active
        if child.parent_group_id == group.id
        and _has_items(child, applies, active)
        and _group_satisfied(child, applies, active, confirmed_ids)
    )
    return direct_done + subgroups_done >= group.pick_count


# True when a group has at least one requirement for this Scout, directly or in a subgroup
def _has_items(
    group: RuleGroup,
    applies: list[RuleRequirement],
    active: list[RuleGroup],
) -> bool:
    if any(r.group_id == group.id for r in applies):
        return True
    return any(
        _has_items(child, applies, active)
        for child in active
        if child.parent_group_id == group.id
    )
