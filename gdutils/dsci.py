import numpy as np
import pandas as pd
import random
import sys


def init_random_seeds():
    # always use the same seed, always initialise before you do anything else
    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    # faker.Faker.seed(RANDOM_SEED)


def init_display_options():
    # so that it's easier to see things in the terminal
    pd.set_option("display.max_rows", 10000)
    pd.set_option("display.max_columns", 1000)
    pd.set_option("display.max_colwidth", 100)
    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)


def jaccard_similarity(list1, list2) -> float:
    """
    For comparing how much overlap there is between two sets.

    Returns a normalised 0-1 similarity score, where higher = more similar.

    USAGE:
        a = ['hello', 'foo', 'foo', 'tux']
        b = ['blah', 'hello', 'foo']
        jaccard_similarity(a, b)

    from https://stackoverflow.com/a/56774335
    """
    intersection = len(set(list1).intersection(list2))
    union = len(set(list1)) + len(set(list2)) - intersection
    return intersection / union


def calc_proportion_longest_common_substring(descriptions: Sequence[str]) -> float:
    # find length of longest string
    longest = max([len(description) for description in descriptions])
    if longest == 0:
        return 0.0

    if len(descriptions) == 2:
        # TODO try this out instead (both behaviour and speed)
        # return fwfuzz.partial_ratio(descriptions[0], descriptions[1]) / 100
        # this would be faster, but I can't install pylcs on my machine
        # len_substring = pylcs.lcs2(descriptions[0], descriptions[1])
        # so fall back on the original implementation
        len_substring = len(longest_substring_multi(descriptions))
    else:
        len_substring = len(longest_substring_multi(descriptions))

    if len_substring <= 1:
        # decided to count a single letter as a 0
        return 0.0
    val = len_substring / longest
    assert 0 <= val <= 1
    return val


def calc_proportion_identical(lst: Any) -> float:
    """
    Returns a value between 0 and 1 for the uniformity of the values
    in LST, i.e. higher if they're all the same.
    """

    def count_most_common(lst):
        """
        Find the most common item in LST, and count how many times it occurs.
        """
        # Counter(['a', 'b', 'a']).most_common(2) -> [
        #   ('a', 2),
        #   ('b', 1),
        # ]
        # so this gives the count of the most common (in this case 2 occurrences of 'a')
        return Counter(lst).most_common(1)[0][1]

    most_common = count_most_common(lst)
    if most_common == 1:
        return 0
    else:
        return most_common / len(lst)


def calc_normalised_std_tightness(vals) -> float:
    """
    The standard deviation STD is in the same units as VALS, i.e.
    it's unnormalised. We normalise by the (absolute) mean,
    subtract from 1, and truncate.

    This gives us a unbounded 'tightness' score,
    i.e. 1 means no variability, 0 means a lot of variability, e.g.

    [19, 21, 20, 20] -> 0.96
    [19,  1, 40, 20] -> 0.31
    [ 9,  1, 70,  0] -> 0
    """
    if len(vals) == 1:
        return 1.0
    average = abs(sum(vals) / len(vals))
    if average < 0.01:
        # e.g. mean([-50, 50]) -> 0
        # risking a divide-by-zero, which could produce unstable results.
        # better to default to treating as not part of the cluster?
        return 0

    if len(vals) == 2:
        deviation = abs(vals[0] - vals[1])
    else:
        deviation = np.std(vals)
    normalised_std = deviation / average
    tightness = 1 - min(1, normalised_std)
    assert 0 <= tightness <= 1
    return tightness


def is_same_sign(x1, x2):
    if x1 > 0 and x2 > 0:
        return True
    if x1 < 0 and x2 < 0:
        return True


def calc_pair_amounts_closeness(amounts: Sequence[float]) -> float:
    """
    Returns higher the closer the two numbers.

    Returns 0 if one number is zero but the other isn't,
    or if they're of different signs.
    """
    assert len(amounts) == 2
    amount1, amount2 = max(amounts), min(amounts)
    if amount1 == 0.0 and amount2 == 0.0:
        # avoid divide-by-zero
        return 1.0
    if amount1 > 0 and amount2 < 0:
        # because a debit and a credit are never similar, no matter what their values
        return 0.0
    if amount1 < 0:
        # if it's negative, they're both negative, and this only works
        # for positive numbers, so swap sign (and therefore max/min
        # will be swapped too)
        amount1, amount2 = abs(amount2), abs(amount1)
    val = 1 - (amount1 - amount2) / (amount1 + amount2)
    assert 0 <= val <= 1
    return val


def convert_sim_dist_reciprocal(val: float) -> float:
    """
    Convert from similarity to distance with 1/x, dealing with divide-by-zero.
    """
    assert 0 <= val <= 1
    out = sys.maxsize if val == 0 else (1 / val)
    assert 0 <= out <= 1
    return out


def convert_sim_dist_oneminus(val: float) -> float:
    """
    Convert from similarity to distance with 1 - x.
    """
    assert 0 <= val <= 1
    out = 1 - val
    assert 0 <= out <= 1
    return out
