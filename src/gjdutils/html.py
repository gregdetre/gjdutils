from bs4 import BeautifulSoup
from lxml.html import tostring
from lxml.etree import _Element as ElementType
from typing import Optional, Union


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


def remove_attrs_from_html(h):
    """
    Gets rid of all the attrs in the html.
    """
    soup = BeautifulSoup(h, features="lxml")
    for t in soup.recursiveChildGenerator():
        t.attrs = {}  # type: ignore
    # whitespace_from_linebreaks(
    # contents_of_body(soup)
    # )
    return contents_of_body(soup)


def adjust_indentation(pretty_html, indent: int):
    # from https://www.perplexity.ai/search/can-you-customise-the-beautifu-225tf.pISaiggsL5tNL.gA
    lines = pretty_html.split("\n")
    adjusted_lines = []
    for line in lines:
        line_lstrip = line.lstrip(" ")
        leading_spaces = len(line) - len(line_lstrip)
        indent_level = leading_spaces // 1  # default indent is 1 space
        adjusted_lines.append(" " * (indent_level * indent) + line_lstrip)
    return "\n".join(adjusted_lines)


def prettify_html(
    html: Union[str, ElementType, list[ElementType]],  # BeautifulSoup
    indent: int = 2,
    n: Optional[int] = None,  # number of chars to show
):
    # if isinstance(html, pq):
    #     html = html.outer_html()  # type: ignore
    if isinstance(html, list):
        # then we'll handle it as a string in a moment
        html = "".join(
            [tostring(e, method="html").decode() for e in html]  # type: ignore
        )  #  type: ignore
    if isinstance(html, ElementType):
        # this will do some cleaning and fixing. but
        # you need document_fromstring() if you want to make sure
        # that it's a full html doc, e.g. with html, body
        html = tostring(html, method="html").decode()  # type: ignore

    soup = BeautifulSoup(html, "html.parser")  # type: ignore
    # html2 = tostring(html, pretty_print=True, method="html").decode()  # type: ignore
    # the lxml pretty_print just isn't as good as BS4, e.g. with a list of elements
    # it wraps things in a div fragment, but the pretty-print of that isn't right
    html2 = soup.prettify()
    prettified = adjust_indentation(html2, indent=indent)[:n]  # type: ignore
    return prettified


def pprettify_html(*args, **kwargs) -> None:
    html = prettify_html(*args, **kwargs)
    print(html)
