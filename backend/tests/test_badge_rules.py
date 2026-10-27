import uuid

from app.services.badge_rules import RuleGroup, RuleRequirement, badge_is_complete

SCOUT_STREAM = uuid.uuid4()
OTHER_STREAM = uuid.uuid4()


def requirement(group=None, stream=None):
    return RuleRequirement(id=uuid.uuid4(), group_id=group, stream_id=stream)


def group(pick_count, parent=None, poultry=False):
    return RuleGroup(
        id=uuid.uuid4(),
        parent_group_id=parent,
        pick_count=pick_count,
        applies_when_poultry=poultry,
    )


# Every ungrouped requirement must be confirmed
def test_ungrouped_requirement_must_be_confirmed():
    r = requirement()
    assert not badge_is_complete([r], [], set(), SCOUT_STREAM, keeps_poultry=False)
    assert badge_is_complete([r], [], {r.id}, SCOUT_STREAM, keeps_poultry=False)


# A group with pick_count 2 needs two confirmed picks, not all four
def test_group_needs_pick_count_confirmed():
    g = group(pick_count=2)
    picks = [requirement(group=g.id) for _ in range(4)]
    assert not badge_is_complete(
        picks, [g], {picks[0].id}, SCOUT_STREAM, keeps_poultry=False
    )
    assert badge_is_complete(
        picks, [g], {picks[0].id, picks[1].id}, SCOUT_STREAM, keeps_poultry=False
    )


# Requirements for another stream do not count
def test_other_stream_requirements_are_ignored():
    mine = requirement()
    theirs = requirement(stream=OTHER_STREAM)
    assert badge_is_complete(
        [mine, theirs], [], {mine.id}, SCOUT_STREAM, keeps_poultry=False
    )


# A poultry-only group is skipped for a Scout who doesn't keep poultry
def test_poultry_group_skipped_for_non_poultry_scout():
    g = group(pick_count=1, poultry=True)
    picks = [requirement(group=g.id)]
    assert badge_is_complete(picks, [g], set(), SCOUT_STREAM, keeps_poultry=False)


# A poultry-only group is required for a Scout who keeps poultry
def test_poultry_group_required_for_poultry_scout():
    g = group(pick_count=1, poultry=True)
    picks = [requirement(group=g.id)]
    assert not badge_is_complete(picks, [g], set(), SCOUT_STREAM, keeps_poultry=True)
    assert badge_is_complete(
        picks, [g], {picks[0].id}, SCOUT_STREAM, keeps_poultry=True
    )


# A parent group can count a subgroup as one of its picks
def test_parent_counts_a_satisfied_subgroup():
    parent = group(pick_count=1)
    child = group(pick_count=1, parent=parent.id)
    inside = requirement(group=child.id)
    groups = [parent, child]
    assert not badge_is_complete(
        [inside], groups, set(), SCOUT_STREAM, keeps_poultry=False
    )
    assert badge_is_complete(
        [inside], groups, {inside.id}, SCOUT_STREAM, keeps_poultry=False
    )


# A parent can mix its own requirements with satisfied subgroups
def test_parent_mixes_direct_picks_and_subgroups():
    parent = group(pick_count=2)
    child = group(pick_count=1, parent=parent.id)
    direct = requirement(group=parent.id)
    inside = requirement(group=child.id)
    groups = [parent, child]
    assert badge_is_complete(
        [direct, inside],
        groups,
        {direct.id, inside.id},
        SCOUT_STREAM,
        keeps_poultry=False,
    )
    assert not badge_is_complete(
        [direct, inside], groups, {direct.id}, SCOUT_STREAM, keeps_poultry=False
    )
