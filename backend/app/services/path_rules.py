import uuid
from dataclasses import dataclass

from app.services.badge_names import LENCANA_AHLI_BOT, LENCANA_USAHA

# Skill rows where a set number of picks completes the row. Other rows need every badge done.
PICKS_PER_ROW: dict[int, int] = {3: 2, 5: 3, 6: 3}

# A badge that waits for another badge in the same row (the book: Ahli Bot after Usaha)
WAITS_FOR: dict[str, str] = {LENCANA_AHLI_BOT: LENCANA_USAHA}


# One badge on the path, as the lock rule sees it
@dataclass(frozen=True)
class PathBadge:
    id: uuid.UUID
    name: str
    row: int
    complete: bool


# A row is complete when its required picks are done
def row_complete(row: int, badges_in_row: list[PathBadge]) -> bool:
    picks = PICKS_PER_ROW.get(row)
    if picks is None:
        return all(b.complete for b in badges_in_row)
    return sum(1 for b in badges_in_row if b.complete) >= picks


# A badge is locked until every earlier row is complete, and until the badge it waits for is done
def is_locked(badge: PathBadge, path: list[PathBadge]) -> bool:
    earlier_rows = {b.row for b in path if b.row < badge.row}
    for row in earlier_rows:
        if not row_complete(row, [b for b in path if b.row == row]):
            return True

    waits_for = WAITS_FOR.get(badge.name)
    if waits_for is not None:
        waited = [b for b in path if b.name == waits_for]
        if waited and not all(b.complete for b in waited):
            return True

    return False
