from typing import Literal, Sequence, TypeVar

T = TypeVar("T")


def found_one(lst: Sequence[T]) -> T | Literal[False]:
    """
    e.g.
    >>> found_one([])
    False
    >>> found_one([10])
    10
    >>> found_one([10, 20])
    False
    """
    if len(lst) == 0:
        return False
    elif len(lst) == 1:
        found = lst[0]
        assert found is not False, "Too confusing - we found something, but it's False"
        return found
    else:
        return False


def find_duplicates(lst: Sequence[T]) -> list[T]:
    return [item for item in set(lst) if lst.count(item) > 1]


# def uniquify(items: Sequence[T], key: Callable[[T], Any] | None = None) -> list[T]:
# this would be useful if you wanted to uniquify something non-hashable, but I couldn't get it to work
# https://www.perplexity.ai/search/in-python-unique-version-of-a-5r0iCRlBSjm2Dv6HGLu_6g
# return list(OrderedDict.fromkeys(map(key, items) if key else items))


def uniquify(items: Sequence[T]) -> list[T]:
    # https://www.perplexity.ai/search/unique-version-of-a-list-prese-qYpae.JBRDedvHdmEyOqfA
    # seen = set()
    # return [x for x in lst if not (x in seen or seen.add(x))]

    # https://www.w3resource.com/python-exercises/list-advanced/python-list-advanced-exercise-8.php
    return list(dict.fromkeys(items))
