from typing import Sequence


def trunc(s, n):
    """
    Truncate a string to N characters, appending '...' if truncated.

      trunc('1234567890', 10) -> '1234567890'
      trunc('12345678901', 10) -> '1234567890...'
    """
    if not s:
        return s
    return s[:n] + "..." if len(s) > n else s


def longest_substring_multi(strs: Sequence[str]) -> str:
    """
    Find the longest common substring for multiple strings in list DATA.

    https://stackoverflow.com/questions/2892931/longest-common-substring-from-more-than-two-strings-python
    """
    substr = ""
    if len(strs) > 1 and len(strs[0]) > 0:
        for i in range(len(strs[0])):
            for j in range(len(strs[0]) - i + 1):
                if j > len(substr) and all(strs[0][i : i + j] in x for x in strs):
                    substr = strs[0][i : i + j]
    return substr
