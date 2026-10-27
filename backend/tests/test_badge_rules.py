import uuid

from app.services.badge_rules import RuleGroup, RuleRequirement, badge_is_complete

SCOUT_STREAM = uuid.uuid4()
OTHER_STREAM = uuid.uuid4()


def requirement(group=None, stream=None):
    return RuleRequirement(id=uuid.uuid4(), group_id=group, stream_id=stream)


# Every ungrouped requirement must be confirmed
def test_ungrouped_requirement_must_be_confirmed():
    r = requirement()
    assert not badge_is_complete([r], [], set(), SCOUT_STREAM)
    assert badge_is_complete([r], [], {r.id}, SCOUT_STREAM)


# A group with pick_count 2 needs two confirmed picks, not all four
def test_group_needs_pick_count_confirmed():
    group = RuleGroup(id=uuid.uuid4(), pick_count=2)
    picks = [requirement(group=group.id) for _ in range(4)]
    assert not badge_is_complete(picks, [group], {picks[0].id}, SCOUT_STREAM)
    assert badge_is_complete(picks, [group], {picks[0].id, picks[1].id}, SCOUT_STREAM)


# Requirements for another stream do not count
def test_other_stream_requirements_are_ignored():
    mine = requirement()
    theirs = requirement(stream=OTHER_STREAM)
    assert badge_is_complete([mine, theirs], [], {mine.id}, SCOUT_STREAM)
