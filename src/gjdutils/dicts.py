import json
from typing import Iterable, Optional

from gjdutils.strings import is_string, jinja_render


def compare_dict(d1, d2, ignore_underscores=True):
    """
    Returns None if they're the same, else returns the first
    key that differs.
    """
    for k, v in d1.items():
        if ignore_underscores and k.startswith("_"):
            continue
        if v != d2[k]:
            return k
    return None


def dict_from_module(mod):
    """
    e.g.
      import config
      config.BLAH
      cfg = dict_from_module(config)
      cfg['BLAH']
      # OR
      cfg = dict_from_module('config')
    """
    if is_string(mod):
        mod = __import__(mod)
    else:
        raise ValueError("Expected a string, got %s" % type(mod))
    return {k: v for k, v in mod.__dict__.items() if not k.startswith("__")}


def pop_copy(d, k):
    """
    A non-destructive version of POP that returns both the
    updated copy of the dictionary and the popped value,
    e.g.

      pop_copy({'a': 100, 'b': 200}, 'a') -> {'b': 200}, 100
    """
    out = d.copy()
    v = out.pop(k)
    return out, v


def pop_safe(d, k, default=None):
    """
    Destructive, like the default pop, but returns DEFAULT
    if K is not a key in D.
    """
    return d.pop(k) if k in d else default


def whittle_dict(d, keys):
    d2 = {}
    for k in keys:
        d2[k] = d[k]
    return d2


def these_fields_only(d: dict, fields: Iterable[str], required=True):
    """
    Returns D2, containing just the KEYS from dictionary D, e.g.

      these_fields_only({'a': 100, 'b': 200}, ['a']) -> {'a': 100}

    If REQUIRED, will raise an exception if any of KEYS aren't keys in D.
    """
    # used to be called WHITTLE_DICT
    if required:
        # will fail if any of the fields in FIELDS are missing from D
        d2 = {k: d[k] for k in fields}
    else:
        d2 = {k: d[k] for k in fields if k in d}
    return d2


def print_dict(d: dict):
    print("\n".join(["%s: %s" % (k, d[k]) for k in sorted(d.keys())]))


def truncate_dict(d: dict, n: Optional[int], reverse=False) -> dict:
    l = list(d.items())
    if reverse:
        l = list(reversed(l))
    l_trunc = l[:n]
    d_trunc = dict(l_trunc)
    return d_trunc


# this is no longer needed. if you want to update a dict in an expression:
#   d_both = {**d1, **d2}
# or
#   d_both = d1 | d2
# def update_d(d1, d2): ...


def combine_dicts(d1: dict, d2: dict, require_unique: bool = True) -> dict:
    """
    UPDATE: you can now do the simple version of this with `d1 | d2`
    """
    if require_unique:
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        overlapping_k = set.intersection(d1_keys, d2_keys)
        assert not overlapping_k, "Overlapping keys: %s" % overlapping_k
    # d = d1.copy()
    # d.update(d2)
    d = d1 | d2
    # check we've maintained ordering. only makes sense if REQUIRE_UNIQUE is False
    # assert list(d1.keys()) + list(d2.keys()) == list(d.keys())
    return d


def update_params_from_defaults(defaults: dict, params_in: dict):
    for param_k in params_in.keys():
        assert param_k in defaults.keys(), "Unexpected param '%s'" % param_k
    params_out = combine_dicts(defaults, params_in, require_unique=False)
    return params_out


def reverse_dict(d):
    """
    Returns a dictionary with values as keys and vice versa.

    Will fail if the values aren't unique or aren't
    hashable.
    """
    vals = d.values()
    # confirm that all the values are unique
    assert len(vals) == len(set(vals))
    d2 = {}
    for k, v in d.items():
        d2[v] = k
    return d2


class HashableDict(dict):
    # http://code.activestate.com/recipes/414283-frozen-dictionaries/
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def rename_fields(d: dict, renames: dict):
    """
    Renames multiple fields in a dictionary at the same time,
    returning a new one, and preserving the order, e.g.

    D = {'a': 100, 'b': 200}
    RENAMES = {'a': 'c'}
    ->
    D2 = {'c': 100, 'b': 200}
    """
    d2 = {}
    for k, v in d.items():
        if k in renames.keys():
            k2 = renames[k]
            d2[k2] = v
        else:
            d2[k] = v
    return d2


def dict_from_list(lst: list[dict], key, skip_duplicates: bool = False):
    """
    Given a list of dicts LST, return a dict DIC where D[v] = an item IT in LST where lst[key]=v.

    For example, given a list of EVENTS, return a dict where D[event_id] = event:

        events_d = dict_from_list(events_l, key="id")
    """
    dic = {}
    for it in lst:
        assert key in it, f"Key {key} not found in {it}"
        v = it[key]
        if skip_duplicates and (v in dic):
            continue
        assert v not in dic, f"Found duplicate key {v}"
        dic[v] = it
    return dic


def pprint_dict(d: dict):
    return print(json.dumps(d, indent=4))


def dict_as_html(d: dict) -> str:
    return jinja_render(
        """
<div class="dict-view">
    <ul>
    {% for key, value in d.items() %}
        <li>
            <strong>{{ key }}</strong>: 
            {% if value is mapping %}
                {{ dict_as_html(value) | safe }}
            {% elif value is sequence and value is not string %}
                <ul>
                {% for item in value %}
                    <li>{{ item }}</li>
                {% endfor %}
                </ul>
            {% else %}
                {{ value }}
            {% endif %}
        </li>
    {% endfor %}
    </ul>
</div>
""",
        context={"d": d, "dict_as_html": dict_as_html},
    )
