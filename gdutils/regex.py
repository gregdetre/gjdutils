import re
from typing import Iterable

# Based on:
#   https://github.com/gregdetre/emacs-freex/blob/63523bf3b9032cc75b55ee28929dcdaf7714a419/freex_sqlalchemy.py#L653
#   https://github.com/gregdetre/emacs-freex/blob/63523bf3b9032cc75b55ee28929dcdaf7714a419/freex_sqlalchemy.py#L713
# That code has faster versions for much bigger lists of aliases, but this is fine for now.


def compile_regex_for_matching_aliases(aliases: Iterable[str]):
    """
    Builds and compiles the implicit link regular expression.
    """
    # add .lower() here and elsewhere if you want case-insensitive
    aliases = [re.escape(a) for a in aliases]

    # ensure that 'jubba wubba' comes before 'jubba'
    aliases.sort(reverse=True)

    # build the regexp string to be single words
    #
    # it used to look like this, which worked nicely, unless
    # there was a carriage return
    alias_regex_str = "\\b" + "\\b|\\b".join(aliases) + "\\b"

    # we want to deal with the possibility that there are 0
    # or 1 spaces after a word, followed by 0 or 1 carriage
    # returns, followed by zero or more spaces, which is
    # what might happen if an implicit link was to span two
    # lines in an indented paragraph. that's what ' ?\n? *' does
    #
    # the \\b that gets
    # added later will ensure that there's a word boundary
    # of *some* kind.
    alias_regex_str = alias_regex_str.replace("\\ ", " ?\\\n? *")

    # for ages, it wasn't matching things like 'Smith &
    # Jones (2006)', because there was some problem with the
    # parentheses. i eventually realized that it matched the
    # first, but not the second parenthesis, because (i
    # think) the parenthesis was screwing with the \b (bare
    # word) separator. if you remove all the bare word
    # separators that follow closing parentheses, the sun
    # comes back out again
    alias_regex_str = alias_regex_str.replace(")\\b", ")")

    # compile the regexp
    # impLinkRegexp = re.compile(aliasRegexpStr, re.IGNORECASE|re.MULTILINE)
    compiled_regex = re.compile(alias_regex_str, re.MULTILINE)
    return compiled_regex


def find_matchranges_for_aliases(
    compiled_regex_of_aliases: re.Pattern, txt_to_search: str
):
    """
    Return a list of (beg,end) tuples for all the matching implicit
    links in the provided string.
    """
    # get the start and endpoints for the matchranges
    matchranges = [
        list(match.span())
        for match in compiled_regex_of_aliases.finditer(txt_to_search)
    ]

    # return the matchranges
    return matchranges


# txt = """There was a young European man called Friedrich Nietzsche, who most went by just "Nietzsche" (and but never 'Friedrich'). He was a friend of Little Hans and Little Richard but he was not little or Little."""

# aliasRegexpStr, impLinkRegexp = update_implicit_link_regexp_original(all_aliases)
# match_ranges = get_all_matching_implicit_links_original(impLinkRegexp, txt)

# for match_range in match_ranges:
#     match_txt = txt[match_range[0]:match_range[1]]
#     matched_name = name_from_alias[match_txt]
#     print('MATCHED: ', match_txt, ' <- NAME: ', matched_name, sep='')
