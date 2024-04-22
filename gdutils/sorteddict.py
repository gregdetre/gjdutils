# This dict is always sorted by `sortfunc` when you iterate over it.
#
# For example, if you have a dict of str -> Nodes, and you want to iterate over them in
# order of their `idx` attribute, you can do:
#
#   d = SortedDict[str,Node](lambda node: node.idx)
#   [insert, remove, Nodes]
#   d.values()  # this will always be sorted by idx
#
# based on code from ChatGPT

from typing import Any, Callable, Dict, Generic, TypeVar


# Define type variables for keys and values
K = TypeVar("K")
V = TypeVar("V")


class SortedDict(Dict[K, V], Generic[K, V]):
    def __init__(self, sortfunc: Callable[[V], Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sortfunc = sortfunc
        self._reorder()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._reorder()

    def _reorder(self):
        sorted_items = sorted(self.items(), key=lambda item: self.sortfunc(item[1]))
        super().clear()
        for key, value in sorted_items:
            super().__setitem__(key, value)
