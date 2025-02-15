import itertools
from typing import Sequence


def contiguous_pairs(lst: Sequence):
    """
    Given a list LST, return the contiguous pairs, e.g.

    [10, 20, 30, 40, 50]
    ->
    [(10, 20), (20, 30), (30, 40), (40, 50)]

    (from GitHub Copilot)
    """
    pairs = [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]
    return pairs


def flatten(lol):
    """
    See http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python

    e.g. [['image00', 'image01'], ['image10'], []] -> ['image00', 'image01', 'image10']
    """

    chain = list(itertools.chain(*lol))
    return chain


# def flatten(list_of_lists):
#     """
#     Flatten one level of nesting

#     from https://docs.python.org/3/library/itertools.html#itertools-recipes
#     """
#     return list(chain.from_iterable(list_of_lists))


def unique(items):
    """
    Returns KEEP, a list based on ITEMS, but with duplicates
    removed (preserving order, based on first new example).

    http://stackoverflow.com/questions/89178/in-python-what-is-the-fastest-algorithm-for-removing-duplicates-from-a-list-so-t

    unique([1, 1, 2, 'a', 'a', 3]) -> [1, 2, 'a', 3]
    """
    found = set([])
    keep = []
    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)
    return keep


def uniquify_list(lst):
    """Return a list of the elements in s, but without duplicates, preserving order.

    from comment in http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560

      Lightweight and fast ..., Raymond Hettinger, 2002/03/17

    """

    set = {}
    return [set.setdefault(e, e) for e in lst if e not in set]


def grouper(iterable, n):
    """
    Collect data into fixed-length chunks or blocks. If
    the last block is too small, returns a truncated block.

    e.g. grouper('ABCDEFG', 3) --> ABC DEF G

    From http://stackoverflow.com/a/8991553/230523
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def grouper_ragged(iterable, n):
    """
    Collect data into non-overlapping chunks - the last one might be shorter than the others

    >>> print(list(grouper('ABCDEFG', 3)))  # [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]

    from https://stackoverflow.com/a/41333827/230523
    """
    it = iter(iterable)
    group = tuple(itertools.islice(it, n))
    while group:
        yield group
        group = tuple(itertools.islice(it, n))
