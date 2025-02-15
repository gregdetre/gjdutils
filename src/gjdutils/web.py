from pathlib import Path
from urllib import parse as urlparse
import webbrowser

from gjdutils.strings import PathOrStr


def webbrowser_open(filen: PathOrStr, browser=None):
    """
    For some reason, the default webbrowser.open() doesn't work for me, so you may want to set browser to 'chrome'
    """
    # I had an issue where it refused to open a non .html file
    assert filen.endswith(".html"), "File must end with .html"
    if browser:
        browser = webbrowser.get(browser)
    else:
        browser = webbrowser
    full_filen = f"file://{Path.cwd() / filen}"
    return browser.open(full_filen)


def trunc_url(url):
    """
    e.g. 'http://www.guardian.co.uk/blah/ -> /blah

    Based on dev/guardian/data/data/greg/sharedwisdom/sharedwisdom/models.py
    """
    # URLPARSE returns ParseResult(scheme='http',
    #                              netloc='memrise.com',
    #                              path='/blah.png',
    #                              params='',
    #                              query='q1=x&q2=y',
    #                              fragment='')
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    # ditch the SCHEME and NETLOC
    # PARAMS are an arcane part that comes after a semi-colon
    return path  # + params


def validate_request_args(args, defaults):
    """
    DEFAULTS = dict of allowed query parameters, with the keys
    being the allowed query-string-parameter-keys and values
    as their defaults.
    """
    if args:
        unexpecteds = set(args.keys()) - set(defaults.keys())
        assert not unexpecteds, "Unexpected key(s): %s" % unexpecteds
    # params = {key: args.get(key, default)
    #           for key, default in defaults.items()}
    params = defaults | args
    return params


def query_string_from_dict(d):
    return "?" + "&".join(["%s=%s" % (k, v) for k, v in d.items()])


def params_from_request(request):
    try:
        if request.json:
            params_in = request.json.get("params", {})
        else:
            params_in = dict(request.values)
        return params_in
    except:
        print("Error in PARAMS_FROM_REQUEST")
        return {}
