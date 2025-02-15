from pathlib import Path
from six import string_types
from string import punctuation
import textwrap
from typing import Optional, Sequence, Union

PathOrStr = Union[str, Path]


def is_string(x):
    """
    Based on https://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility
    """
    return isinstance(x, string_types)


def remove_punctuation(txt: str) -> str:
    """Removes characters that are in string.punctuation."""
    return txt.translate(str.maketrans("", "", punctuation))


def remove_first_line(s):
    return "\n".join(s.splitlines()[1:])


def truncate_chars(s: str, n: Optional[int] = None):
    """
    Truncate a string to N characters, appending '...' if truncated.

      trunc('1234567890', 10) -> '1234567890'
      trunc('12345678901', 10) -> '1234567890...'
    """
    if not s:
        return s
    if n is None:
        return s
    return s[:n] + "..." if len(s) > n else s


def truncate_words(txt: str, n: Optional[int] = None):
    if n is None:
        return txt
    words = txt.split(" ")
    return " ".join(words[:n])


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


def jinja_get_template_variables(template: str) -> set[str]:
    """
    Extract all variables expected by a Jinja2 template.

    Args:
        template_string (str): The Jinja2 template string to analyze

    Returns:
        set: A set of variable names found in the template

    Example:
        >>> template = "Hello {{ name }}! Your age is {{ age }}"
        >>> get_template_variables(template)
        {'name', 'age'}
    """
    # https://claude.ai/chat/3a2e9e93-c9cd-4b19-8313-ef7640e5971f
    from jinja2 import Environment, meta

    env = Environment()
    ast = env.parse(template)
    variables = meta.find_undeclared_variables(ast)
    return variables


def jinja_render(
    prompt_template: str,
    context: dict,
    filesystem_loader: Optional[PathOrStr] = None,
    check_surplus_context: bool = True,
    strip=True,
):
    """
    Render a Jinja template with the given dictionary, e.g.

        jinja_render("{{name}} is {{age}} years old", {'name': 'Bob', 'age': 42}) -> "Bob is 42 years old"

    Will raise an error if CONTEXT is missing any variables.
    """
    from jinja2 import Environment, FileSystemLoader, StrictUndefined

    loader = None if filesystem_loader is None else FileSystemLoader(filesystem_loader)
    env = Environment(loader=loader, undefined=StrictUndefined)
    template = env.from_string(prompt_template)
    rendered = template.render(context)
    if strip:
        rendered = rendered.strip()
    if check_surplus_context:
        # should it be an error if we have been provided more keys in the context
        # than are used in the template? e.g. this is useful for noticing when the
        # template has e.g. {myvar} with single instead of double braces
        jinja_variables = jinja_get_template_variables(prompt_template)
        surplus_context = set(context.keys()) - jinja_variables
        if surplus_context:
            raise ValueError(f"Surplus context: {surplus_context}")

    return rendered


# probably better off using slugify from the slugify package
# import codecs
# import translitcodec
# def slugify(text, delim=u'-'):
#     """
#     Generates an ASCII-only slug

#     Based on http://flask.pocoo.org/snippets/5/
#     """
#     if not text or not text.strip():
#         return ''
#     _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
#     result = []
#     for word in _punct_re.split(text.lower()):
#         # https://pypi.org/project/translitcodec/
#         word = codecs.encode(word, 'translit/long')
#         if word:
#             result.append(word)
#     return str(delim.join(result))


def display_compare_strings(s1, s2):
    if len(s2) > len(s1):
        # e.g. s1='abc', s2='abcd', => s2[3:], i.e. 'd'
        print("Truncated: %s" % s2[len(s1) :])
    print("\n".join(["%s %s" % (pair[0], pair[1]) for pair in zip(s1, s2)]))


def wrap_indent(s: str, indent_level: int = 0, sep="  "):
    spaces = sep * indent_level
    return "\n".join(textwrap.wrap(s, initial_indent=spaces, subsequent_indent=spaces))


def indent_without_wrap(s: str, indent_txt: Optional[str] = None):
    if indent_txt is None:
        indent_txt = "    "
    return (
        textwrap.fill(s, initial_indent=indent_txt, subsequent_indent=indent_txt)
        if s and isinstance(s, str)
        else str(s)
    )


def append_fullstop(s: str):
    """
    Appends a fullstop if there isn't already punctuation at the end of S.
    """
    if not isinstance(s, str):
        return ""
    s_orig = s[:]
    s = s.strip()
    if not s:
        return s
    if s[-1] in punctuation:
        return s
    return f"{s}."


def str_from_num(x):
    try:
        import numpy as np

        bools = (bool, np.bool_)
    except ImportError:
        bools = (bool,)

    # todo, find a better way of doing this, e.g.
    # if isinstance(Iterable), recur. otherwise try str(x)
    if x is None:
        return str(x)
    elif isinstance(x, bools):
        return str(x)
    elif isinstance(x, str):
        return x
    elif isinstance(x, (int, float)):
        # return f"{x:.2f}"
        return str(round(x * 100))
    elif isinstance(x, (list, tuple)):
        # e.g. [0.20,0.10,-5.00]
        return "[" + ",".join([str_from_num(item) for item in x]) + "]"  # type: ignore
    else:
        raise Exception(f"Unknown NUM_STR type: {type(x)}, {x}")
