import base64
import hashlib
import sys
import traceback
import uuid


def gen_uuid():
    # e.g. '161b58a4d8'
    return str(uuid.uuid4()).replace("-", "")[:10]


def hash_readable(s, n=10):
    """
    Returns a string hash that contains base32 characters instead of a number,
    to make it more readable (and still low risk of collisions if you truncate it).

    e.g. hash_readable('hello') => 'vl2mmho4yx'

    Unlike Python's default hash function, this should be deterministic
    across sessions (because we're using 'hashlib').

    I'm using this for anonymising email addresses if I don't have a user UUID.
    """
    if isinstance(s, str):
        s = bytes(s, "utf-8")
    hasher = hashlib.sha1(s)
    b32 = base64.b32encode(hasher.digest())[:n]
    return b32.decode("utf-8").lower()


def semicolon_str_as_list(s):
    """
    see utils.tests.MiscTests.test_semicolon_str_as_list().
    """
    if not s:
        return []
    return [x.strip() for x in s.split(";") if len(x.strip()) > 0]


def whittle_dict(d, keys):
    """
    Returns D2, containing just the KEYS from dictionary D,
    e.g.

    whittle_dict({'a': 100, 'b': 200}, ['a']) -> {'a': 100}

    Will raise an exception if any of KEYS aren't keys in D.

    xxx - maybe this should instead do a copy, and delete any not needed???
    """
    d2 = {}
    for k in keys:
        d2[k] = d[k]
    return d2


def str_from_exception(name=None):
    return {
        "name": name,
        "msg": "".join(traceback.format_exception(*sys.exc_info())),
    }
