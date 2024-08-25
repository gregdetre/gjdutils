from typing import Literal, Sequence, TypeVar

T = TypeVar("T")


def found_one(lst: Sequence[T]) -> T | Literal[False]:
    if len(lst) == 0:
        return False
    elif len(lst) == 1:
        found = lst[0]
        assert found is not False, "Too confusing - we found something, but it's False"
        return found
    else:
        return False
