from random import shuffle
from typing import Callable, Iterable
from sorteddict import SortedDict

SAMPLE_TUPLES = [
    (1, {"id": 1, "name": "C"}),
    (2, {"id": 2, "name": "B"}),
    (3, {"id": 3, "name": "A"}),
]
SORTFUNC_ID = lambda x: x["id"]
SORTFUNC_NAME = lambda x: x["name"]


def check_keys_values_items(d: dict, sortfunc: Callable):
    actual_items = list(d.items())
    actual_keys = list(d.keys())
    actual_values = list(d.values())
    desired_items = sorted(actual_items, key=lambda kv: sortfunc(kv[1]))
    desired_keys = [k for k, v in desired_items]
    desired_values = [v for k, v in desired_items]
    assert actual_items == desired_items
    assert actual_keys == desired_keys
    assert actual_values == desired_values


def test_sorteddict():
    d = SortedDict[int, dict](SORTFUNC_ID)  # initialise with *args
    for k, v in SAMPLE_TUPLES:
        d[k] = v
    assert list(d.keys()) == [1, 2, 3]
    check_keys_values_items(d, SORTFUNC_ID)

    d = SortedDict[int, dict](SORTFUNC_NAME)  # initialise with *args
    for k, v in SAMPLE_TUPLES:
        d[k] = v
    assert list(d.keys()) == [3, 2, 1]

    shuffle(items)
    d = SortedDict[int, dict](sortfunc=SORTFUNC_ID)  # try initialising with **kwargs
    for k, v in SAMPLE_TUPLES:
        d[k] = v
    check_keys_values_items(d, SORTFUNC_ID)
    d[20] = {"id": 100}
    d[0] = {"id": 0}
    d[10] = {"id": 1}
    assert list(d.keys()) == [0, 1, 10, 2, 3, 20]
    check_keys_values_items(d, SORTFUNC_ID)

    del d[10]
    assert list(d.keys()) == [0, 1, 2, 3, 20]
    check_keys_values_items(d, SORTFUNC_ID)
