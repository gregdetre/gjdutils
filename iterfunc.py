import itertools
import random


def flatten(lol):
    """
    See http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python

    e.g. [['image00', 'image01'], ['image10'], []] -> ['image00', 'image01', 'image10']
    """

    chain = list(itertools.chain(*lol))
    return chain


def update_d(d1, d2):
    d1_copy = d1.copy()
    d1_copy.update(d2)
    return d1_copy


def shuffle_copy(lst):
    lst2 = lst.copy()
    random.shuffle(lst2)
    return lst2
