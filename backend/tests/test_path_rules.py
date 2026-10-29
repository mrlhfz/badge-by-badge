import uuid

from app.services.path_rules import PathBadge, is_locked, row_complete


def badge(name, row, complete=False):
    return PathBadge(id=uuid.uuid4(), name=name, row=row, complete=complete)


# The first row is always open
def test_first_row_is_never_locked():
    keahlian = badge("Lencana Keahlian", 1)
    assert not is_locked(keahlian, [keahlian])


# A badge in row 2 stays locked until row 1 is complete
def test_row_two_waits_for_row_one():
    usaha = badge("Lencana Usaha", 2)
    assert is_locked(usaha, [badge("Lencana Keahlian", 1), usaha])
    assert not is_locked(usaha, [badge("Lencana Keahlian", 1, complete=True), usaha])


# Ahli Bot waits for Usaha, even though both are in row 2
def test_ahli_bot_waits_for_usaha_in_same_row():
    usaha = badge("Lencana Usaha", 2, complete=False)
    ahli_bot = badge("Lencana Ahli Bot", 2)
    path = [badge("Lencana Keahlian", 1, complete=True), usaha, ahli_bot]
    assert is_locked(ahli_bot, path)
    usaha_done = badge("Lencana Usaha", 2, complete=True)
    path = [badge("Lencana Keahlian", 1, complete=True), usaha_done, ahli_bot]
    assert not is_locked(ahli_bot, path)


# A skill row needs its picks, so one of two Kegemaran picks is not enough
def test_skill_row_needs_its_picks():
    one_pick = [badge("Ahli Renang", 3, complete=True), badge("Ahli Muzik", 3)]
    assert not row_complete(3, one_pick)
    two_picks = [
        badge("Ahli Renang", 3, complete=True),
        badge("Ahli Muzik", 3, complete=True),
    ]
    assert row_complete(3, two_picks)


# Row 4 stays locked until the two Kegemaran picks in row 3 are done
def test_row_four_waits_for_kegemaran_picks():
    renang = badge("Ahli Renang", 3, complete=True)
    muzik = badge("Ahli Muzik", 3)
    maju = badge("Lencana Maju", 4)
    assert is_locked(maju, [renang, muzik, maju])
    muzik_done = badge("Ahli Muzik", 3, complete=True)
    assert not is_locked(maju, [renang, muzik_done, maju])


# A compulsory row needs every badge done, not just some
def test_compulsory_row_needs_every_badge():
    maju = badge("Lencana Maju", 4, complete=True)
    juragan_muda = badge("Lencana Juragan Muda", 4, complete=False)
    assert not row_complete(4, [maju, juragan_muda])


# Juragan (row 7) stays locked until row 6 is complete
def test_row_seven_waits_for_row_six():
    perkhidmatan = [
        badge("Ahli Pertolongan Cemas", 6, complete=True),
        badge("Setiausaha", 6),
    ]
    juragan = badge("Lencana Juragan", 7)
    path = perkhidmatan + [juragan]
    assert is_locked(juragan, path)
