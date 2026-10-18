"""Turn an HTML / iXBRL (.xhtml) annual report into page-like text, stdlib only.

ESEF reports are usually PDF pages re-drawn as HTML: every word or line sits in its
own positioned box. Read in document order that gives one word per line, so lines
are joined back into sentences. Real tables become "| cell | cell |" rows, the same
shape pymupdf4llm gives for PDFs, so the rest of the pipeline treats both alike.
"""

import re
from html.parser import HTMLParser

from .scraper import Page

_BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "section", "table"}
_SKIP = {"style", "script", "head", "title", "ix:header"}


def _local(tag: str) -> str:
    """Tag name without its namespace prefix, except ix:header: the hidden inline-XBRL
    block (contexts, units, hidden facts) that came out as one 167,000-character run
    of tag names in Merck's 10-K and blew the LLM's token limit."""
    tag = tag.lower()
    return tag if tag == "ix:header" else tag.rsplit(":", 1)[-1]
WORDS_PER_PAGE = 450          # pseudo-pages: the report has no page breaks we can rely on


class _Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.cell = 0         # inside a table cell: block tags become spaces

    def handle_starttag(self, tag, attrs):
        tag = _local(tag)
        if tag in _SKIP:
            self.skip += 1
        elif tag in ("td", "th"):
            self.cell += 1
            self.out.append(" | ")
        elif tag == "tr":
            self.out.append("\n")
        elif tag in _BLOCK:
            self.out.append(" " if self.cell else "\n")

    def handle_endtag(self, tag):
        tag = _local(tag)
        if tag in _SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in ("td", "th"):
            self.cell = max(0, self.cell - 1)
        elif tag == "tr":
            self.out.append(" |\n")
        elif tag in _BLOCK and not self.cell:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(html: str) -> str:
    """Plain text: sentences joined, table rows kept one per line."""
    html = re.sub(r'(?i)src="data:[^"]*"', 'src=""', html)      # embedded images are huge
    p = _Extractor()
    p.feed(html)
    raw = "".join(p.out).replace(" ", " ")
    paragraphs, current = [], []
    for line in raw.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        if line.startswith("|"):                    # table row: its own line
            if current:
                paragraphs.append(" ".join(current))
                current = []
            if re.search(r"[^|\s]", line):
                paragraphs.append(re.sub(r"(\|\s*){2,}", "| ", line))
            continue
        current.append(line)
        if re.search(r"[.!?:;]$", line) or len(" ".join(current)) > 1200:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs)


def text_to_pages(text: str, words_per_page: int = WORDS_PER_PAGE) -> list[Page]:
    """Split into numbered pseudo-pages at paragraph boundaries ("page" = section N)."""
    pages, buf, words = [], [], 0
    for para in text.split("\n"):
        buf.append(para)
        words += len(para.split())
        if words >= words_per_page:
            pages.append(Page(len(pages) + 1, "\n".join(buf)))
            buf, words = [], 0
    if buf:
        pages.append(Page(len(pages) + 1, "\n".join(buf)))
    return pages
