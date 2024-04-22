from decimal import Decimal, getcontext
from typing import Optional

"""
For manual ordering and reording in a database:
- every item gets a Decimal location (LOC) between 0 and 1
- the LOCs of all items are sorted
- the LOC of a new item is calculated as the average of the LOCs of the items before and after it
- the LOC won't ever be 0 or 1, so there will always be a gap for you to insert afterwards
- if you insert at the beginning or end, the LOC will be half of the first or last item's LOC

I think Figma used this.
"""

# Set precision high enough to handle many divisions
getcontext().prec = 28


def locs_for(n: int) -> list[Decimal]:
    # Assign initial idx values with buffers at both ends
    locs = []
    for i in range(n):
        loc = Decimal(i + 1) / Decimal(n + 1)
        locs.append(loc)
    assert len(locs) == n
    return locs


def loc_for_insert_at(locs: list[Decimal], position: int, do_insert: bool = True):
    """
    TODO: rewrite in terms of LOC_BETWEEN
    """
    assert locs == sorted(
        locs
    ), f"Input LOCS are unsorted, so things are already broken - {locs}"
    list_length = len(locs)
    if position == 0:  # Insert at the beginning
        newloc = locs[0] / 2 if list_length > 0 else Decimal("0.5")
    elif position >= list_length:  # Insert at the end
        newloc = locs[-1] + (1 - locs[-1]) / 2 if list_length > 0 else Decimal("0.5")
    elif position < 0:
        raise Exception(f"Position must be non-negative, but got {position}")
    else:  # Insert between two items
        newloc = (locs[position - 1] + locs[position]) / 2
    if do_insert:
        locs.insert(position, newloc)
        assert locs == sorted(locs), f"Somehow we've broken the LOCS sorting: {locs}"
    return newloc


def loc_for_insert_at2(locs: list[Decimal], position: int, do_insert: bool = True):
    """
    Functional version of LOC_FOR_INSERT_AT that returns a new list instead of
    modifying the input list.

    Uses LOC_BETWEEN.
    """
    assert locs == sorted(
        locs
    ), f"Input LOCS are unsorted, so things are already broken - {locs}"
    list_length = len(locs)
    if position < 0:
        raise Exception(f"Position must be non-negative, but got {position}")
    elif position == 0:  # Insert at the beginning
        loc1 = None
        loc2 = locs[0] if list_length > 0 else None
    elif position >= list_length:  # Insert at the end
        loc1 = locs[-1] if list_length > 0 else None
        loc2 = None
    else:  # Insert between two items
        loc1 = locs[position - 1]
        loc2 = locs[position]
    newloc = loc_between(loc1, loc2)
    if do_insert:
        locs.insert(position, newloc)
        assert locs == sorted(locs), f"Somehow we've broken the LOCS sorting: {locs}"
    return newloc


def loc_between(loc1: Optional[Decimal], loc2: Optional[Decimal]) -> Decimal:
    if loc1 is not None and loc2 is not None:
        assert (
            loc1 >= 0 and loc2 <= 1
        ), f"LOCs must be between 0 and 1, but got {loc1} and {loc2}"
        return (loc1 + loc2) / 2
    elif loc1 is None and loc2 is not None:
        return loc2 / 2
    elif loc1 is not None and loc2 is None:
        return loc1 + (1 - loc1) / 2
    elif loc1 is None and loc2 is None:
        return Decimal("0.5")
    else:
        raise Exception(f"This should never happen: {loc1}, {loc2}")


def disp(locs: list[Decimal]):
    print(", ".join(["%.3f" % loc for loc in locs]))
