import os
from pathlib import Path
from typing import Sequence

from .cmd import run_cmd

# keep this, because it makes sense for the user to be able to import from here
from .strings import is_string, PathOrStr


def split_filen(filen: Path | str):
    """
    Splits a filename into its path, stem, and extension (without dot), e.g.

        split_filen('data/blah.mp4') -> ('data', 'blah', 'mp4')
    """
    filen = Path(filen)
    return filen.parent, filen.stem, filen.suffix[1:] if filen.suffix else ""


def create_dir_if_not_exists(dirn: str):
    if not os.path.exists(dirn):
        os.makedirs(dirn)


def validate_ext(ext):
    assert is_string(ext)
    assert ext.lower() == ext
    assert ext
    assert ext[0] != "."


def validate_dir(dirn):
    dirn_path = Path(dirn)
    assert dirn_path.exists() and dirn_path.is_dir()
    return dirn_path


def fulltext(
    filens: Sequence[str],
    patterns: list[str],
    dirn: str,
    file_ext: str,
    case_sensitive=False,
):
    """
    Returns: FOUND_FILES (list of filename strings)

    Feed in a list of filenames (complete with extensions),
    which will be fed to agrep for full-text
    searching. Returns a list of files.

    FILENS is a list of strings. If its non-empty, then
    these will be fed in to agrep. If it's empty, then we'll
    just feed in a '*.[freex_extension]'. Spaces in
    filenames are escaped with backslashes, but this is the
    only thing we're escaping.

    PATTERNS is a list of strings, which will be ANDed
    together in the agrep regex. Currently, this doesn't
    escape the pattern regex at all, though it does surround it in
    quotes, so the usual agrep rules apply.

    Unless case_sensitive==True, will append a -i flag.
    """
    # from freex_sqlalchemy.py

    # xxx this should check that all the files have extensions

    if case_sensitive:
        case_flag = ""
    else:
        case_flag = "-i"

    # xxx should check that all the items in the pattern
    # list are strings...
    #
    # first strip each of the pattern strings of whitespace,
    # and remove the surrounding quotes - we'll add them
    # back to the whole pattern_str when we create the CMD
    #
    # then AND together multiple patterns with agrep,
    # using semicolons
    for pat in patterns:
        if pat[0] == '"':
            pat = pat[1:]
        if pat[-1] == '"':
            pat = pat[0:-1]

    pattern_str = ";".join([x.strip() for x in patterns])

    if len(filens) > 0:
        # escape all the spaces with back-slashes
        filens = [x.replace(" ", "\\ ") for x in filens]

        # convert to a space-delimited string (with spaces
        # escaped by backslashes), and each file prepended by the
        # database_dir, e.g.
        # /blah/test0.freex /blah/hello\ world.freex
        fnames_str = " ".join([os.path.join(dirn, filen) for filen in filens])

        # the -l says to just return filenames only (no text
        # context)
        #
        # put the pattern in quotes
        #
        # and then just list the files at the end
        cmd = 'agrep -l %s "%s" %s' % (case_flag, pattern_str, fnames_str)

    else:
        # if we're not restricting the files we're looking
        # through, then there could be too many files to run
        # agrep on directly, so we have to pipe it from a
        # find
        #
        # this is to avoid the '/usr/local/bin/agrep:
        # Argument list too long' error
        cmd = 'find %s -name "*.%s" -print0 | xargs -0 agrep -l %s "%s"' % (
            dirn,
            file_ext,
            case_flag,
            pattern_str,
        )

    # Run command with minimal output unless there's an error
    retcode, out_str, _ = run_cmd(
        cmd,
        verbose=0,
        check=False,  # Don't raise exception if no matches found (agrep returns 1)
    )

    if len(out_str) > 0:
        # strip away the path to yield just the filename for
        # each of the files in out_str
        found_files = [os.path.basename(x) for x in out_str.strip().split("\n")]
    else:
        # if you run the above on an empty string, you get
        # [''], whereas we really want to return an empty
        # list if we didn't find anything
        found_files = []

    return found_files
