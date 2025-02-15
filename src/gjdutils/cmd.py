import subprocess
import sys


def run_cmd(cmd: str):
    stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    stdout = stdout.decode(sys.stdout.encoding or "UTF-8")
    return stdout


def run_cmd2(cmd: str, raise_error: bool = False, verbose: int = 0):
    process = subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout = process.stdout
    stderr = process.stderr
    if stderr and raise_error:
        raise Exception(stderr)
    if verbose > 1:
        print(f"{cmd=}")
    if verbose > 0:
        # print(f"{stdout=}")
        print(stdout)
        # print(error)
    return stdout, stderr


def subproc(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    verbose=True,
    throw_exception=True,
):
    """
    Why can't python have a subproc function like this (like
    matlab's 'unix')? Takes in a CMD, returns a RETCODE,
    OUT_STR and ERR_STR strings, and the SUBPOPEN
    subprocess.Popen object.

    RETCODE = 0 (all is well)
    RETCODE = -1 (caught an exception of some kind)
    RETCODE = non-zero (the command ran, but the shell didn't like it)

    If VERBOSE, then it will print CMD before running it,
    and the OUT_STR and ERR_STR after running (if they're
    non-empty).

    If THROW_EXCEPTION, will throw an exception if RETCODE is
    non-zero. If not THROW_EXCEPTION, it'll just return the RETCODE
    and it's up to you to check it.

    Returns: RETCODE, OUT_STR, ERR_STR, SUBPOPEN

    N.B. this is more cautious than matlab's 'unix' command,
    because its default is to throw an exception if there's
    any kind of problem.

    Update: this sucks if you want to use pipes (e.g. 'cat *
    > blah'). In that case, I ended up just using
    os.system().

    Usage e.g.:

        retcode, out_str, err_str, subpopen = subproc('ls')

    N.B. This was written for Python 2 - there may be a better way now.
    """
    # from freex_sqlalchemy.py

    if verbose > 0:
        print(cmd)

    # it's ugly having two different routes for
    # throw_exception, but i don't know how to store and
    # return the exception traceback
    if throw_exception:
        # call subprocess.Popen nakedly, without bothering to catch exceptions
        subpopen = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
        retcode = subpopen.wait()
        out_str = subpopen.stdout.read()
        err_str = subpopen.stderr.read()

        if retcode != 0:
            # xxx need to return proper exception classes
            # rather than just strings
            raise Exception("Non-zero retcode: %i" % retcode)

        if len(err_str) > 0:
            print(out_str)
            print(err_str)
            raise Exception("Non-empty error string")

    else:
        # wrap any exception, and let the user know with the retcode = -1
        try:
            subpopen = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
            retcode = subpopen.wait()
            out_str = subpopen.stdout.read()
            err_str = subpopen.stderr.read()
        except:
            out_str = ""
            err_str = ""
            subpopen = ""
            retcode = -1

    if verbose & len(out_str) > 0:
        print(out_str)
    if verbose & len(err_str) > 0:
        print(err_str)

    return retcode, out_str, err_str, subpopen
