from inspect import isfunction


def isint(f, tol=0.00000001):
    """
    Takes in a float F, and checks that it's within TOL of floor(f).
    """
    # we're casting to float before the comparison with TOL
    # so that decimal Fs work
    return abs(float(f) - int(f)) <= 0.00000001


def isnum(n):
    try:
        float(n)
        return True
    except:
        return False


def isiterable(x):
    """
    from http://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-a-variable-is-iterable
    """
    import collections
    return isinstance(x, collections.Iterable)


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


def print_dict(d: dict):
    print "\n".join(['%s: %s' % (k, d[k]) for k in sorted(d.keys())])

