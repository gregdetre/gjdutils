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


def is_same_sign(x1, x2):
    if x1 > 0 and x2 > 0:
        return True
    if x1 < 0 and x2 < 0:
        return True


def isiterable(x):
    """
    from http://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-a-variable-is-iterable
    """
    import collections

    return isinstance(x, collections.Iterable)
