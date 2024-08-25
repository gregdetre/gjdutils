from .dicts import print_dict
from .typ import isfunction


def print_locals(
    d: dict, ignore_functions: bool = True, ignore_underscores: bool = True
):
    """
    e.g. print_locals(locals())
    """

    def del_robust(k):
        if k in d:
            del d[k]

    assert isinstance(d, dict)
    for k in d.keys():
        if ignore_functions and isfunction(d[k]):
            del_robust(k)
        if ignore_underscores and k.startswith("_"):
            del_robust(k)
    return print_dict(d)


def identity_func(x):
    return x


def empty_func(*args, **kwargs):
    return None
