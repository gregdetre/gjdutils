from functools import update_wrapper
import inspect
import re

from gjdutils.typ import isiterable


# from abracadjabra.utils
def generate_mckey(prefix, d):
    """
    Should generate a legal, human-readable, unique and
    predictable string Memcached key from dictionary
    D. N.B. we're using 'mckey' to distinguish Memcached
    'keys' from dictionary 'keys'.

    Designed to be called at the top of your function with
    locals(), so it ignores any REQUEST and SELF keys - but
    you can always add {'user': request.user} if needed.

    Notes:

    - Prepends PREFIX + '__' to the MCKEY generated from D.

    - For dictionaries, concatenates the keys+values, sorted
      by key.

    - Converts lists and querysets to lists of IDs, hashing
      the result if too long.

    - Hashes the MCKEY if it's non-ascii or too long. Removes spaces etc.

    Keys are separated from their value by '::', and the
    key/value pairs are separated from one another by '__'.

    e.g.

       {'a': 100, 'b': 'blah'} -> u'a::100__b::blah'

    xxx - should be moved to utils.caching, along with Evan's cmcd
    """

    def sorted_dict_by_keys(d):
        """
        Returns a SortedDict, with the keys sorted alphabetically.

        This might not be necessary, since I think the order
        of a Python 3 dict's keys() is deterministic, but by
        sorting by dictionary keys, it's easier to know in
        advance what the generated MCKEY should look like.
        The idea is to ensure that no matter how D was
        created, you'll know what the key should be.
        """
        sorted_d = dict()
        for k in sorted(d.keys()):
            sorted_d[k] = d[k]
        return sorted_d

    def to_str_or_hash(s):
        """
        Tries to convert S to a STR. If it doesn't work,
        just return the hash.
        """
        try:
            s = str(s)
        except UnicodeEncodeError:
            s = str(hash(s))
        return s

    def hash_if_too_long(s):
        """
        Return the HASH of S rather than S if it's too long
        (since the hash is only 10 characters).

        We call this on each component and then once more at
        the end because we want to keep the overall result
        as human-readable as possible, while still being
        unique.
        """
        if len(s) > MAX_MEMCACHED_KEY_LEN:
            s = str(hash(s))
        return s

    def iterable_to_string(seq):
        """
        If the items in SEQ are Django Models,
        store a comma-separated list of ids.

        Otherwise, just join the items in SEQ.

        e.g. [Thing.objects.get(id=1), Thing.objects.get(id=2)] -> 'Thing:1,2'
        """
        if not seq:
            return ""
        pieces = [to_str_or_hash(x) for x in seq]
        model_prefix = ""
        s = model_prefix + ",".join(pieces)
        s = hash_if_too_long(s)
        return s

    def sanitize_val(v):
        """
        If V is an iterable, turn it into a comma-separated
        string (of IDs, if Models).

        Even though (empirically) it appears that Django's
        cache.set and cache.get use Memcached's binary
        protocol (so they can deal with non-ascii keys), it
        seems safer to require the key to be ascii.
        """
        if isinstance(v, str):
            pass
        elif isinstance(v, unicode):
            v = to_str_or_hash(v)
        elif hasattr(v, "pk"):
            # for instances, i decided not to separate the
            # modelname from the id with a colon to
            # distinguish them from querysets
            v = v._meta.object_name + str(v.pk)
        elif isinstance(v, dict):
            # we might decide that even if we *can* deal
            # with dicts like this, it's too crazy to be worth it...
            v = generate_mckey("", v)
        elif isiterable(v):
            v = iterable_to_string(v)
        else:
            v = to_str_or_hash(v)
        v = v.strip()
        return hash_if_too_long(v)

    # 250 bytes, minus global KEY_PREFIX, plus leave extra room in case
    MAX_MEMCACHED_KEY_LEN = 200

    prefix = to_str_or_hash(prefix).upper()

    assert isinstance(d, dict)
    # ignore REQUEST and SELF, so you can easily pass in locals() for D
    if "request" in d:
        del d["request"]
    if "self" in d:
        del d["self"]
    d = sorted_dict_by_keys(d)

    # require everything to be a nice ascii string
    pieces = "__".join(
        [
            "%s::%s"
            % (
                sanitize_val(k),
                sanitize_val(v),
            )
            for k, v in d.items()
        ]
    )

    prefix_pieces = prefix + "__" + pieces
    # replace all whitespace with underscores
    prefix_pieces = re.sub("[ \t\r\n]+", "_", prefix_pieces)
    # not too long
    prefix_pieces = hash_if_too_long(prefix_pieces)
    # make sure it's ascii-friendly
    prefix_pieces = str(prefix_pieces)
    return prefix_pieces


def cmcd(prefix=None, arg_names=(), expiry=None):
    """Caches the return value of func based on the cache key generated by
    generate_mckey. The prefix argument to the `generate_mckey` is
    determined from the module and the name of the function if `prefix` is
    `None`. `arg_names` should be a sequence of strings that will be
    pulled from the kwargs dict and passed to `generate_mckey` to generate
    a key.

    Unfortunately we don't have access to the same locals() as the
    function itself, so the functions we're wrapping with this need to
    take keyword arguments, and the arguments we're generating the cache
    from must be specified.

    NOTE: prefix must be defined in settings.CACHE_EXPIRY, OR set expiry=EXPIRY_TIME, e.g.

    See utils.tests for usage.
    """

    def dec(func, prefix=prefix, arg_names=arg_names, expiry=expiry):
        if expiry is None:
            if prefix == None:
                prefix = ".".join((func.__module__, func.__name__))

            prefix = prefix.upper()
            if prefix not in sett.CACHE_EXPIRY:
                raise Exception(
                    "Prefix %s must be defined in settings.CACHE_EXPIRY if expiry is not specified"
                    % prefix
                )

            expiry = sett.CACHE_EXPIRY[prefix]

        fspec = inspect.getargspec(func)
        pos_args = fspec.args
        defaults = fspec.defaults
        defaults = defaults if defaults else ()

        if pos_args or defaults:
            if not arg_names:
                raise Exception(
                    "arg_names must be specified for functions that take arguments."
                )

            default_args = dict(
                (k, v) for k, v in zip(reversed(pos_args), reversed(defaults))
            )
            noargs = False
        else:
            noargs = True

        def f(*args, **kwargs):
            if not noargs:
                all_args = dict(default_args)
                all_args.update(dict((n, v) for n, v in zip(pos_args, args)))
                all_args.update(kwargs)
                d = dict((k, all_args.get(k, None)) for k in arg_names)
            else:
                all_args = {}
                d = {}

            mckey = generate_mckey(prefix, d)
            cached = cache.get(mckey)

            if cached:
                return cached

            val = func(*args, **kwargs)

            cache.set(mckey, val, expiry)

            return val

        return update_wrapper(f, func)

    return dec
