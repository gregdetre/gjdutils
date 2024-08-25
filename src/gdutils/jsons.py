import json
from typing import Optional


def jsonify(x):
    def json_dumper_robust(obj):
        try:
            return obj.toJSON()
        except:
            try:
                return str(obj)
            except:
                return None

    return json.dumps(x, sort_keys=True, indent=4, default=json_dumper_robust)


def to_json(
    inps: list,
    fields: Optional[list] = None,
    skip_if_missing: bool = False,
    skip_empties: bool = True,
    max_str_len: Optional[int] = 1000,
) -> str:
    """
    Convert a list of dicts to a JSON string, with only the fields we want,
    and in the same order as FIELDS.
    """
    outs = []
    for inp in inps:
        if fields is None:
            fields = inp.keys()
        # we want to make sure to return a dict with only the fields we want,
        # and in the same order as FIELDS
        out = {}
        for k in fields:
            if skip_if_missing and (k not in inp):
                continue
            v = inp[k]  # will error if missing and !SKIP_IF_MISSING
            if skip_empties and (v is None or v == ""):
                continue
            if max_str_len and isinstance(v, str) and len(v) > max_str_len:
                v = v[:max_str_len] + "..."
            out[k] = v
        outs.append(out)
    outs_j = json.dumps(outs, indent=2)
    return outs_j
