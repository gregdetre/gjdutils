import json
from typing import Optional


def jsonify(x):
    def json_dumper_robust(obj):
        try:
            return obj.toJSON()
        except AttributeError:
            # Object doesn't have toJSON method, try string conversion
            try:
                return str(obj)
            except (ValueError, TypeError):
                # If string conversion fails, return None to skip this field
                return None

    return json.dumps(x, sort_keys=True, indent=4, default=json_dumper_robust)


# from o-1
# class RobustJSONEncoder(json.JSONEncoder):
#     def __init__(self, *args, **kwargs):
#         self.seen = set()
#         super().__init__(*args, **kwargs)

#     def default(self, obj):
#         if id(obj) in self.seen:
#             return None  # Replace circular references with None or a placeholder
#         self.seen.add(id(obj))
#         try:
#             return obj.toJSON()
#         except:
#             try:
#                 return str(obj)
#             except:
#                 return None


# def jsonify(x):
#     return json.dumps(x, cls=RobustJSONEncoder, sort_keys=True, indent=4)


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
    if fields is None:
        fields = []
    outs = []
    for inp in inps:
        if fields is None:
            fields = inp.keys()
        # we want to make sure to return a dict with only the fields we want,
        # and in the same order as FIELDS
        out = {}
        for k in fields:  # type: ignore
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
