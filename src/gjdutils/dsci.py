from collections import Counter
import itertools
import sys
from typing import Any, Sequence

# keep this, because it makes sense for the user to be able to import from here
from .rand import set_seeds


def init_display_options():
    import numpy as np
    import pandas as pd

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


def calc_normalised_std_tightness(vals: Sequence[float]) -> float:
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
    import numpy as np

    n = len(vals)
    if n == 0:
        raise Exception("Empty")
    elif n == 1:
        return 1.0
    if n == 2:
        deviation = abs(vals[0] - vals[1])
    else:
        deviation = float(np.std(vals))

    average = abs(sum(vals) / n)
    if average < 0.01:
        # e.g. mean([-50, 50]) -> 0
        # risking a divide-by-zero, which could produce unstable results.
        # better to default to treating as not part of the cluster?
        return 0

    normalised_std = deviation / average
    tightness = 1 - min(1, normalised_std)
    assert 0 <= tightness <= 1
    return tightness


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


def square_df_from_square(sq, features):
    import pandas as pd

    df = pd.DataFrame(sq)
    # create a 'Feature' column
    df["Feature"] = features
    rename_dict = dict(zip(range(len(features)), features))
    df.rename(columns=rename_dict, inplace=True)
    # df = df.reindex_axis(['Feature'] + features, axis=1)
    df = df.set_index("Feature")
    return df


def long_df_from_flat(dists_flat, features):
    import pandas as pd

    combos = [(f1, f2) for f1, f2 in itertools.permutations(features, 2)]
    assert len(combos) == len(dists_flat)
    dists_triplet = [
        (combo[0], combo[1], dist) for combo, dist in zip(combos, dists_flat)
    ]
    dists_long_df = pd.DataFrame(dists_triplet, columns=["Feature", "Brand", "Score"])
    return dists_long_df


def square_df_from_flat(dists_flat, features):
    from scipy import spatial

    nFeatures = len(features)
    dists_sq = spatial.distance.squareform(np.array(dists_flat))
    assert dists_sq.shape == (nFeatures, nFeatures)
    return square_df_from_square(dists_sq, features)


def pairwise_local(data, distance_func, format="long"):
    """
    Returns squareform pairwise distances DataFrame (run symmetrically).

    DATA should be a iterable of arrays (e.g. a list of bitarrays).
    Pairs of rows from DATA will be passed into DISTANCE_FUNC, which
    should return a float.

    If format 'square' (default), returns an (nFeatures x nFeatures)
    square distances matrix.

    If format 'flat', returns a vector of distances (that could be fed
    into scipy squareform to produce the 'square' version).

    If format 'long', returns recs weighted-sum model format.
    """
    features = sorted(data.keys())
    dists_flat = [
        distance_func(data[f1], data[f2])
        for f1, f2 in itertools.permutations(features, 2)
    ]
    if format == "flat":
        return dists_flat
    if format == "long":
        return long_df_from_flat(dists_flat, features)
    elif format == "square":
        dists_sq_df = square_df_from_flat(dists_flat, features)
        return dists_sq_df
    else:
        raise Exception("Unknown FORMAT %s" % format)
