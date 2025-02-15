from decimal import Decimal
from typing import Optional

from gjdutils.indexing import (
    loc_between,
    loc_for_insert_at,
    loc_for_insert_at2,
)


def test_loc_for_insert_at():
    # Test inserting at the beginning
    locs = [Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]
    position = 0
    loc = loc_for_insert_at(locs, position)
    assert loc == Decimal("0.1")
    assert locs == [Decimal("0.1"), Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]

    # Test inserting at the end
    locs = [Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]
    position = 3
    loc = loc_for_insert_at(locs, position)
    assert loc == Decimal("0.8")
    assert locs == [Decimal("0.2"), Decimal("0.4"), Decimal("0.6"), Decimal("0.8")]

    # Test inserting between two items
    locs = [Decimal("0.2"), Decimal("0.6")]
    position = 1
    loc = loc_for_insert_at(locs, position)
    assert loc == Decimal("0.4")
    assert locs == [Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]

    # Test inserting into an empty list
    locs = []
    position = 0
    loc = loc_for_insert_at(locs, position)
    assert loc == Decimal("0.5")
    assert locs == [Decimal("0.5")]

    # Test inserting into a list with one item
    locs = [Decimal("0.2")]
    position = 1
    loc = loc_for_insert_at(locs, position)
    assert loc == Decimal("0.6")
    assert locs == [Decimal("0.2"), Decimal("0.6")]


def test_loc_for_insert_at2():
    # Test inserting at the beginning
    locs = [Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]
    position = 0
    locs_copy = locs.copy()
    locs_copy.sort()
    loc = loc_for_insert_at2(locs, position)
    assert loc == Decimal("0.1")
    assert locs == sorted(locs_copy + [Decimal("0.1")])

    # Test inserting at the end
    locs = [Decimal("0.2"), Decimal("0.4"), Decimal("0.6")]
    position = 3
    locs_copy = locs.copy()
    locs_copy.sort()
    loc = loc_for_insert_at2(locs, position)
    assert loc == Decimal("0.8")
    assert locs == sorted(locs_copy + [Decimal("0.8")])

    # Test inserting between two items
    locs = [Decimal("0.2"), Decimal("0.6")]
    position = 1
    locs_copy = locs.copy()
    locs_copy.sort()
    loc = loc_for_insert_at2(locs, position)
    assert loc == Decimal("0.4")
    assert locs == sorted(locs_copy + [Decimal("0.4")])

    # Test inserting into an empty list
    locs = []
    position = 0
    locs_copy = locs.copy()
    locs_copy.sort()
    loc = loc_for_insert_at2(locs, position)
    assert loc == Decimal("0.5")
    assert locs == sorted(locs_copy + [Decimal("0.5")])

    # Test inserting into a list with one item
    locs = [Decimal("0.2")]
    position = 1
    locs_copy = locs.copy()
    locs_copy.sort()
    loc = loc_for_insert_at2(locs, position)
    assert loc == Decimal("0.6")
    assert locs == sorted(locs_copy + [Decimal("0.6")])


def test_loc_between():
    # Test when both loc1 and loc2 are not None
    loc1 = Decimal("0.2")
    loc2 = Decimal("0.6")
    result = loc_between(loc1, loc2)
    assert result == Decimal("0.4")

    # Test when loc1 is None and loc2 is not None
    loc1 = None
    loc2 = Decimal("0.6")
    result = loc_between(loc1, loc2)
    assert result == Decimal("0.3")

    # Test when loc1 is not None and loc2 is None
    loc1 = Decimal("0.2")
    loc2 = None
    result = loc_between(loc1, loc2)
    assert result == Decimal("0.6")

    # Test when both loc1 and loc2 are None
    loc1 = None
    loc2 = None
    result = loc_between(loc1, loc2)
    assert result == Decimal("0.5")
