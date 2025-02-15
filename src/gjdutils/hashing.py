import base64
import hashlib


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
    hashed = hashlib.sha1(s).digest()
    b32 = base64.b32encode(hashed)[:n]
    return b32.decode("utf-8").lower()


def hash_consistent(obj):
    """
    Supposedly gives the same response every time you call it, even after restarting the kernel.

    N.B. This is based on output from GitHub Copilot, and I haven't tried it.
    """
    obj_str = str(obj)
    hash_obj = hashlib.sha256(obj_str.encode()).hexdigest()
    return hash_obj
