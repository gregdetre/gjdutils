from typing import Union

# this doesn't support numpy's numeric types, but it's a good stopgap for now.
# there doesn't appear to be a perfect, agreed solution
#
# https://stackoverflow.com/questions/60616802/how-to-type-hint-a-generic-numeric-type-in-python
Numeric = Union[int, float]


def percent(num, denom):
    return (100 * (num / float(denom))) if denom else 0


def percent_str(num, denom):
    return str(percent) + "%"


def discretise(
    val,
    increment: Union[int, float] = 0.1,
    lower: Union[int, float] = 0.0,
    upper: Union[int, float] = 1.0,
    enforce_range: bool = True,
):
    """
    You will probably want to cache this.
    """
    import numpy as np
    import pandas as pd

    def calc_increments(increment, lower, upper):
        assert (
            lower <= increment <= upper
        ), f"Required: {lower:.2f} < {increment:.2f} <= {upper:.2f}"
        # e.g. for lower=0, upper=1, increment_size=0.05, nincrements=21
        nincrements = int((upper - lower) / increment) + 1
        # e.g. for lower=0, upper=1, increment_size=0.05, increments = [0., 0.05, 0.1, ..., 0.95, 1. ]
        increments = np.linspace(lower, upper, nincrements)
        return increments

    if pd.isnull(val):
        return upper
    if enforce_range and (val < lower or val > upper):
        raise ValueError(
            f"Value {val:.2f} is outside the valid range [{lower:.2f}, {upper:.2f}]"
        )
    increments = calc_increments(increment, lower, upper)
    if val < lower:
        return increments[0]
    if val > upper:
        return increments[-1]
    idx = np.digitize(val, increments)
    # e.g.
    #   0.00 -> 0.0
    #   0.01 -> 0.0
    #   0.06 -> 0.05
    #   0.99 -> 0.95
    #   1.00 -> 1.0
    discretised = increments[idx - 1]
    return discretised


def ordinal(n: int):
    """
    e.g 1 -> "1st", 103 -> "103rd"
    """
    # from https://claude.ai/chat/87fad336-e0fa-4074-aed4-f4e57ed20bb7

    # TESTED:
    # for i in [0, 1, 2, 3, 4, 10, 11, 12, 13, 22, 78, 103, 103231, 103235]:
    #     print(i, ordinal(i))
    assert n >= 0
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
