from datetime import date

from app.enums import TandaState
from app.services.tanda import add_months, evaluate


# Three months after a date keeps the day, and short months stop at their last day
def test_add_months_keeps_day_and_handles_short_months():
    assert add_months(date(2026, 1, 15), 3) == date(2026, 4, 15)
    assert add_months(date(2026, 11, 30), 3) == date(2027, 2, 28)
    assert add_months(date(2028, 11, 30), 3) == date(2029, 2, 28)


# A badge still missing means the Scout isn't there yet
def test_missing_badge_is_not_yet():
    result = evaluate({"Lencana Jaya": None, "Lencana Juragan": date(2026, 1, 1)}, date(2026, 6, 1))
    assert result.state == TandaState.NotYet
    assert result.missing == ["Lencana Jaya"]


# Badges held, but less than three months, is waiting
def test_held_less_than_three_months_is_waiting():
    result = evaluate({"Lencana Jaya": date(2026, 1, 1)}, date(2026, 2, 1))
    assert result.state == TandaState.Waiting
    assert result.eligible_on == date(2026, 4, 1)


# Three months held is eligible
def test_held_three_months_is_eligible():
    result = evaluate({"Lencana Jaya": date(2026, 1, 1)}, date(2026, 4, 1))
    assert result.state == TandaState.Eligible


# For Laut, the later badge sets the start, so both must be held three months
def test_later_badge_sets_the_start_date():
    dates = {"Lencana Jaya": date(2026, 1, 1), "Lencana Juragan": date(2026, 3, 1)}
    result = evaluate(dates, date(2026, 5, 1))
    assert result.held_since == date(2026, 3, 1)
    assert result.state == TandaState.Waiting
    assert evaluate(dates, date(2026, 6, 1)).state == TandaState.Eligible
