from typing import Optional
from bs4 import BeautifulSoup


# see also: prettyhtml() in blocks/decorators.py


def remove_html_tags(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def contents_of_body(soup):
    """
    e.g.
      BeautifulSoup('<p>hello</p><p>world</world>', features='lxml')
        =>
          <p>hello</p>
          <p>world</p>

    N.B. for html.parser, you might just be able to do: str(soup)
    """
    # it might be better to prettify with body hidden=True???
    return "\n".join([str(t) for t in soup.body.contents])


def compare_html(h1, h2):
    h1p = BeautifulSoup(h1, features="html.parser").prettify().strip()
    h2p = BeautifulSoup(h2, features="html.parser").prettify().strip()
    assert h1p == h2p


def simplify_html(h):
    soup = BeautifulSoup(h, features="lxml")
    for t in soup.recursiveChildGenerator():
        t.attrs = {}
    # whitespace_from_linebreaks(
    # contents_of_body(soup)
    # )
    return contents_of_body(soup)
