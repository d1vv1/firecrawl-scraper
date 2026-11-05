"""Turn an HTML / iXBRL (.xhtml) annual report into page-like text, stdlib only.

ESEF reports are usually PDF pages re-drawn as HTML: every word or line sits in its
own positioned box. Read in document order that gives one word per line, so lines
are joined back into sentences. Real tables become "| cell | cell |" rows, the same
shape pymupdf4llm gives for PDFs, so the rest of the pipeline treats both alike.
"""

import re
import unicodedata
from collections import Counter
from html.parser import HTMLParser

from .scraper import Page

_BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "section", "table"}
_SKIP = {"style", "script", "head", "title", "ix:header"}
_POSITIONED = re.compile(r"position\s*:\s*absolute", re.I)
_TOP = re.compile(r"top\s*:\s*(-?[\d.]+)px")
ROW_PX = 4                     # boxes this close in height are one row
_FIGURE_END = re.compile(r"\d[\d,.]*\)?%?$|[–—-]$")
# Converted text changes when this does, so cached conversions are made again
# (pipeline.esef_document). 3: positioned boxes are lines, boxes at one height one
# line; private-font text decoded.
VERSION = 3

# Some reports' fonts give glyphs private codes (U+E000-U+F8FF) instead of letters.
# Two kinds are seen, and both are decoded with the words the same document spells
# out in plain text:
# - a whole font shifted: Bang & Olufsen's U+E644 is "a" and U+E603 a space (every
#   code = letter + 0xE5E3), its digits another font (U+E8DC is "0");
# - single ligature glyphs: AO World's U+E61F is "fi" ("_nancial", "pro_t").
_PRIVATE = re.compile("[\ue000-\uf8ff]")
_PRIVATE_RUN = re.compile("[\ue000-\uf8ff]+")
LIGATURES = ("fi", "fl", "ff", "ffi", "ffl", "ft", "st", "tt", "Th")
_FIGURES = re.compile(r"[\d.,/%()\-– ]*\d[\d.,/%()\-– ]*")
_YEAR = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)")


def _vocabulary(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[^\W\d_]{3,}", _PRIVATE.sub(" ", text))}


def _shifted(text: str, vocab: set[str]) -> dict[str, str]:
    """Private code -> character, for fonts whose codes are printable characters
    moved by one offset. An offset is kept when most of the words it decodes are
    words of the document; for a font of figures only, when they read as years."""
    runs = _PRIVATE_RUN.findall(text)
    common = Counter(c for run in runs for c in run).most_common(12)
    offsets = {ord(c) - ord(x) for c, _ in common for x in " etaoinsr0123456789"}
    scored, figures = [], []
    for off in offsets:
        hits = tries = years = 0
        for run in runs:
            if not all(0x20 <= ord(c) - off <= 0x7E for c in run):
                continue
            plain = "".join(chr(ord(c) - off) for c in run)
            words = re.findall(r"[^\W\d_]{3,}", plain)
            tries += len(words)
            hits += sum(w.lower() in vocab for w in words)
            # a font of figures only: any shift gives digits, so only years prove it
            years += not words and bool(_FIGURES.fullmatch(plain) and _YEAR.search(plain))
        if hits >= 5 and hits >= tries / 2:
            scored.append((hits, off))
        elif not tries and years:
            figures.append((years, off))
    # a digits font: the shift with the most years (2026/27), if clearly the most
    figures.sort(reverse=True)
    if figures and figures[0][0] >= 2 and (len(figures) == 1 or figures[0][0] > figures[1][0]):
        scored.append(figures[0])
    table: dict[str, str] = {}
    for _, off in sorted(scored, reverse=True):
        for run in runs:
            if all(0x20 <= ord(c) - off <= 0x7E for c in run):
                for c in run:
                    table.setdefault(c, chr(ord(c) - off))
    return table


def private_glyphs(text: str) -> str:
    """Private-code glyphs replaced by the text they draw: shifted fonts first, then
    ligatures; a glyph that spells nothing known (an icon, a bullet) becomes a space."""
    if not _PRIVATE.search(text):
        return text
    vocab = _vocabulary(text)
    for _ in range(3):              # a second font (digits) is found once the first is decoded
        table = _shifted(text, vocab)
        if not table:
            break
        text = text.translate(str.maketrans(table))
        vocab = _vocabulary(text)
    for code in set(_PRIVATE.findall(text)):
        words = re.findall(rf"[^\W\d_]*{code}[^\W\d_]*", text)
        best, hits = "", 0
        for lig in LIGATURES:
            n = sum(w.replace(code, lig).lower() in vocab for w in words)
            if n > hits:
                best, hits = lig, n
        text = text.replace(code, best if hits >= max(2, len(words) // 3) else " ")
    return text


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
        self.top = None       # height of the last positioned box

    def handle_starttag(self, tag, attrs):
        tag = _local(tag)
        if tag in _SKIP:
            self.skip += 1
        elif _POSITIONED.search(style := dict(attrs).get("style") or ""):
            # a box placed on the page starts a line, even a <span> (AO World's notes:
            # "3,133Directors" ran the staff table's rows together), unless it sits at
            # the height of the box before it: a cell of the same row (Bang & Olufsen
            # draws each cell as its own box)
            top = _TOP.search(style)
            top = float(top.group(1)) if top else None
            same_row = top is not None and self.top is not None and abs(top - self.top) < ROW_PX
            self.out.append(" " if self.cell or same_row else "\n")
            self.top = top
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
    raw = private_glyphs(unicodedata.normalize("NFKC", "".join(p.out)).replace(" ", " "))
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
        # a line ending in a figure is a table row of a drawn table: its own line
        if re.search(r"[.!?:;]$", line) or _FIGURE_END.search(line) or len(" ".join(current)) > 1200:
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
