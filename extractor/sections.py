"""Step 5: cut the report into chunks and keep only the relevant ones.

Annual reports are 100-300+ pages; we send the LLM ~6,000 words per question.
"""

import logging
import math
import re
from dataclasses import dataclass, field

from functools import lru_cache

from .config import CHUNK_OVERLAP_WORDS, CHUNK_WORDS, WORD_BUDGET_PER_GROUP, fold
from .scraper import Page

log = logging.getLogger(__name__)

FINANCIALS = [
    "consolidated income statement", "consolidated statement of profit or loss",
    "turnover", "revenue", "net sales", "consolidated balance sheet",
    "statement of financial position", "total assets", "total equity and liabilities",
    # common wording variants
    "total liabilities and equity",
    # Nordic-language reports (matched accent-insensitively)
    "koncernens resultaträkning", "koncernens rapport över totalresultat", "nettoomsättning",
    "intäkter", "koncernens balansräkning", "koncernens rapport över finansiell ställning",
    "summa tillgångar", "summa eget kapital och skulder",
    "konsernets resultatregnskap", "resultatregnskap", "driftsinntekter", "salgsinntekter",
    "konsernets balanse", "oppstilling av finansiell stilling", "sum eiendeler",
    "sum egenkapital og gjeld",
    "koncernens resultatopgørelse", "resultatopgørelse", "nettoomsætning", "omsætning",
    "koncernens balance", "aktiver i alt", "passiver i alt", "egenkapital og forpligtelser i alt",
    "konsernin tuloslaskelma", "liikevaihto", "konsernin tase", "vastaavaa yhteensä",
    "vastattavaa yhteensä", "taseen loppusumma",
    "rekstrarreikningur", "rekstrartekjur", "efnahagsreikningur", "eignir samtals",
]
QUALITATIVE = [
    "business model", "our strategy", "how we create value", "segment information",
    "operating segments", "business groups", "group structure",
    "principal subsidiaries", "related undertakings", "parent company",
    # common wording variants
    "business group", "at a glance", "significant subsidiaries", "'s structure",
    "corporate structure",
    # Nordic-language reports
    "affärsmodell", "vår strategi", "rörelsesegment", "segmentsinformation",
    "koncernstruktur", "dotterföretag", "dotterbolag", "moderbolaget",
    "forretningsmodell", "driftssegmenter", "segmentinformasjon", "konsernstruktur",
    "datterselskaper", "morselskapet",
    "forretningsmodel", "vores strategi", "segmentoplysninger", "dattervirksomheder",
    "modervirksomhed", "moderselskab",
    "liiketoimintamalli", "strategiamme", "toimintasegmentit", "segmenttitiedot",
    "konsernirakenne", "tytäryhtiöt", "emoyhtiö",
]
# Data points beyond the core figures (python -m extractor.datapoints), one group
# per topic so that each topic gets its own share of the word budget.
OWNERSHIP = [
    "shareholders", "largest shareholders", "major shareholders", "principal shareholders",
    "ownership structure", "share capital", "number of shares", "controlling shareholder",
    "ultimate parent", "parent company", "owned by", "isin", "ticker", "listed on",
    "stock exchange", "nasdaq", "euronext", "large cap", "mid cap", "small cap", "first north",
    "största aktieägare", "aktieägare", "ägarstruktur", "aktiekapital",
    "største aksjonærer", "aksjonærer", "eierstruktur", "aksjekapital",
    "største aktionærer", "aktionærer", "ejerforhold", "aktiekapital",
    "suurimmat osakkeenomistajat", "osakkeenomistajat", "omistusrakenne", "osakepääoma",
]
EMPLOYEES = [
    "number of employees", "average number of employees", "full-time equivalents", "fte",
    "headcount", "employees", "staff costs", "personnel",
    "medelantal anställda", "antal anställda", "medarbetare",
    "årsverk", "antall ansatte", "ansatte",
    "gennemsnitligt antal", "antal ansatte", "medarbejdere",
    "henkilöstön määrä", "henkilöstö", "keskimäärin",
]
REMUNERATION = [
    "remuneration", "pension", "defined contribution", "defined benefit",
    "shareholding requirement", "share ownership guideline", "shareholding guideline",
    "chief executive officer", "executive management", "group management",
    "ersättning", "ersättningar till ledande befattningshavare", "pensionsavsättning",
    "godtgjørelse", "lederlønn", "vederlag", "lønn til ledende ansatte",
    "palkitseminen", "palkitsemisraportti", "eläke", "toimitusjohtaja",
    # pay tables (role grain)
    "base salary", "fixed salary", "fixed pay", "short-term incentive", "long-term incentive",
    "annual bonus", "variable remuneration", "total remuneration", "benefits", "target bonus",
    "grundgehalt", "festvergütung", "kurzfristige variable vergütung", "langfristige variable",
    "gesamtvergütung", "rémunération fixe", "rémunération variable", "vaste beloning",
    "variabele beloning", "retribución fija", "retribución variable", "retribuzione fissa",
    "compensi", "remuneração fixa", "grundlön", "rörlig ersättning", "fastlønn", "grundløn",
    "peruspalkka", "lyhyen aikavälin kannustin",
]
GEOGRAPHY = [
    "geographical information", "geographic information", "geographical areas",
    "revenue by country", "revenue by geography", "by geographical market", "by country",
    "domestic", "rest of the world", "rest of world", "non-current assets by country",
    "geografiska", "geografisk", "geografiske", "maantieteellinen", "maantieteelliset",
]
PROFILE = [
    "registered office", "headquarters", "head office", "domicile", "corporate information",
    "general information", "reporting entity", "presentation currency", "functional currency",
    "säte", "huvudkontor", "hovedkontor", "forretningskontor", "hjemsted", "kotipaikka",
    "registration number", "registered number", "corporate identity number", "legal form",
    "public limited company", "formerly", "domiciled", "incorporated",
    "organisationsnummer", "org.nr", "organisasjonsnummer", "cvr", "y-tunnus",
    "handelsregister", "amtsgericht", "sitz der gesellschaft", "www.",
]
SEGMENTS = [
    "segment information", "operating segments", "reportable segments", "segment reporting",
    "ifrs 8", "by segment", "segment revenue",
    "rörelsesegment", "segmentsinformation", "segmentinformasjon", "driftssegmenter",
    "segmentoplysninger", "segmenttitiedot", "segmentberichterstattung", "segmentinformationen",
    "gesegmenteerde informatie", "information sectorielle", "información por segmentos",
    "informativa di settore", "informação por segmentos",
]
KEYFIGURES = [
    "ebitda", "adjusted ebitda", "operating profit", "operating result", "ebit",
    "key figures", "financial highlights", "five-year summary", "alternative performance measures",
    "share price", "closing price", "market capitalisation", "market capitalization",
    "basis of preparation", "accounting policies", "financial year", "fiscal year",
    "rörelseresultat", "driftsresultat", "liiketulos", "betriebsergebnis", "nyckeltal",
    "nøkkeltall", "hoved- og nøgletal", "tunnusluvut", "kennzahlen", "aktiekurs",
    "aksjekurs", "osakekurssi", "schlusskurs", "börsvärde", "markedsverdi",
]
DATAPOINT_TOPICS = {"ownership": OWNERSHIP, "employees": EMPLOYEES,
                    "remuneration": REMUNERATION, "geography": GEOGRAPHY, "profile": PROFILE,
                    "segments": SEGMENTS, "keyfigures": KEYFIGURES}
KEYWORD_GROUPS = {"financials": FINANCIALS, "qualitative": QUALITATIVE, **DATAPOINT_TOPICS}

# Headings of the primary statements. A chunk with one of these AND lots of
# numbers is almost certainly the statement itself.
STATEMENT_HEADINGS = [
    "consolidated income statement", "consolidated statement of profit or loss",
    "consolidated statement of comprehensive income", "consolidated balance sheet",
    "consolidated statement of financial position", "statement of financial position",
    "income statement", "balance sheet",
    "koncernens resultaträkning", "koncernens balansräkning", "resultaträkning",
    "balansräkning", "koncernens rapport över finansiell ställning",
    "konsernets resultatregnskap", "resultatregnskap", "konsernets balanse",
    "oppstilling av finansiell stilling",
    "koncernens resultatopgørelse", "resultatopgørelse", "koncernens balance",
    "konsernin tuloslaskelma", "konsernin tase", "tuloslaskelma",
    "rekstrarreikningur", "efnahagsreikningur",
]
STATEMENT_BOOST = 50.0
HEADING_BONUS = 8.0      # per keyword that appears in one of the chunk's headings
LENGTH_NORM_WORDS = 300  # keyword score is divided by sqrt(words / this) for longer chunks
MIN_SECTION_WORDS = 60   # shorter heading sections are merged into the next one
HEADINGS_PER_PAGE_MIN = 0.3

_HEADING_RE = re.compile(r"^#{1,6}\s+\S")
_NUMBER_RE = re.compile(r"\(?-?\d{1,3}(?:[,.  ]\d{3})+(?:\.\d+)?\)?|\(?-?\d+(?:\.\d+)?\)?")
_WORD_RE = re.compile(r"[^\s|]+")


@dataclass
class Chunk:
    id: int
    text: str
    pages: list[int] = field(default_factory=list)

    @property
    def words(self) -> int:
        # Text with few spaces (codes, run-together tags) is far more tokens than its
        # word count says; count every 8 characters as at least one word.
        return max(count_words(self.text), len(self.text) // 8)


def strip_markup(text: str) -> str:
    """Remove markdown/HTML formatting so keyword and quote matching see plain text."""
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"</?[a-z][^>]*>", " ", text, flags=re.I)
    text = re.sub(r"^\|?\s*:?-{3,}.*$", " ", text, flags=re.M)   # table separator rows
    text = text.replace("|", " ")
    text = re.sub(r"[*_`#]+", "", text)
    return text


def count_words(text: str) -> int:
    return len(_WORD_RE.findall(strip_markup(text)))


# --- chunking -------------------------------------------------------------------

def _lines_with_pages(pages: list[Page]):
    for p in pages:
        for line in p.text.splitlines():
            yield p.number, line


def _split_long(text: str, pages: list[int]) -> list[tuple[str, list[int]]]:
    """Split by lines into ~CHUNK_WORDS windows with CHUNK_OVERLAP_WORDS overlap.
    Works on lines (not words) so markdown table rows stay intact."""
    lines = text.splitlines()
    out, start = [], 0
    while start < len(lines):
        words, end = 0, start
        while end < len(lines) and (words < CHUNK_WORDS or end == start):
            words += count_words(lines[end])
            end += 1
        out.append(("\n".join(lines[start:end]), pages))
        if end >= len(lines):
            break
        back, overlap = end, 0
        while back > start + 1 and overlap < CHUNK_OVERLAP_WORDS:
            back -= 1
            overlap += count_words(lines[back])
        start = back
    return out


def _sections_by_heading(pages: list[Page]) -> list[tuple[str, list[int]]]:
    sections: list[tuple[list[str], list[int]]] = []
    lines, spans = [], []
    for number, line in _lines_with_pages(pages):
        if _HEADING_RE.match(line) and count_words("\n".join(lines)) >= MIN_SECTION_WORDS:
            sections.append((lines, spans))
            lines, spans = [], []
        lines.append(line)
        if not spans or spans[-1] != number:
            spans.append(number)
    if lines:
        sections.append((lines, spans))
    return [("\n".join(l), s) for l, s in sections]


def _sections_by_page_windows(pages: list[Page]) -> list[tuple[str, list[int]]]:
    """No headings: concatenate pages, then fixed-size windows over it."""
    out: list[tuple[str, list[int]]] = []
    buf, buf_pages, words = [], [], 0
    for p in pages:
        buf.append(p.text)
        buf_pages.append(p.number)
        words += count_words(p.text)
        if words >= CHUNK_WORDS:
            out.append(("\n".join(buf), buf_pages))
            buf, buf_pages, words = [], [], 0
    if buf:
        out.append(("\n".join(buf), buf_pages))
    return out


def split_chunks(pages: list[Page]) -> list[Chunk]:
    n_headings = sum(1 for _, line in _lines_with_pages(pages) if _HEADING_RE.match(line))
    use_headings = n_headings >= HEADINGS_PER_PAGE_MIN * len(pages)
    log.info("Chunking %d pages by %s (%d headings)", len(pages),
             "headings" if use_headings else "fixed-size windows", n_headings)
    sections = _sections_by_heading(pages) if use_headings else _sections_by_page_windows(pages)

    chunks: list[Chunk] = []
    for text, sec_pages in sections:
        if not text.strip():
            continue
        parts = _split_long(text, sec_pages) if count_words(text) > CHUNK_WORDS else [(text, sec_pages)]
        for part, part_pages in parts:
            chunks.append(Chunk(len(chunks), part, list(part_pages)))
    return chunks


# --- table-of-contents detection -----------------------------------------------

_TOC_LINE_RE = re.compile(r"^[A-Za-z][^\d]{2,80}?\s+\d{1,3}$")


def is_toc_line(line: str) -> bool:
    """A short line of words ending in a page number, with no other numbers
    (financial table rows have several number cells; ToC lines have one)."""
    plain = re.sub(r"\s+", " ", strip_markup(line)).strip()
    return bool(_TOC_LINE_RE.match(plain))


def is_toc(text: str, min_lines: int = 5, min_ratio: float = 0.35) -> bool:
    lines = [l for l in (re.sub(r"\s+", " ", strip_markup(x)).strip()
                         for x in text.splitlines()) if l]
    if not lines:
        return False
    toc = sum(is_toc_line(l) for l in lines)
    ratio = toc / len(lines)
    if re.search(r"^\s*(table of )?contents\s*$", strip_markup(text), re.I | re.M):
        min_ratio *= 0.6
    return toc >= min_lines and ratio >= min_ratio


# --- scoring and selection -----------------------------------------------------

def number_density(text: str) -> tuple[int, float]:
    plain = strip_markup(text)
    nums = len(_NUMBER_RE.findall(plain))
    words = max(len(_WORD_RE.findall(plain)), 1)
    return nums, nums / words


def _plain_lower(text: str) -> str:
    """Plain text for keyword matching: no markup, accents folded ("omsætning" and
    "omsaetning" both become "omsatning"); keywords are folded the same way."""
    return re.sub(r"\s+", " ", fold(strip_markup(text).replace("’", "'")))


@lru_cache(maxsize=None)
def _folded(words: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(fold(w) for w in words)


def score_chunk(text: str, keywords: list[str], boost_statements: bool) -> float:
    """Keyword score (length-normalized, so a long section that mentions a keyword
    once doesn't beat a short section about it), plus a bonus for keywords in
    headings, plus a big boost for real statement tables."""
    low = _plain_lower(text)
    headings = _plain_lower("\n".join(l for l in text.splitlines() if _HEADING_RE.match(l)))
    score = 0.0
    keywords = _folded(tuple(keywords))
    for kw in keywords:
        n = low.count(kw)
        if n:
            score += 2 + math.log1p(n)     # distinct keywords matter more than repeats
    words = max(len(_WORD_RE.findall(low)), 1)
    score /= math.sqrt(max(words, LENGTH_NORM_WORDS) / LENGTH_NORM_WORDS)
    score += HEADING_BONUS * sum(kw in headings for kw in keywords)
    if boost_statements and score and is_statement_table(text):
        score += STATEMENT_BOOST
    return round(score, 2)


def is_statement_table(text: str) -> bool:
    """A primary-statement heading plus lots of numbers: the actual statement table."""
    low = _plain_lower(text)
    n_nums, density = number_density(text)
    return (any(h in low for h in _folded(tuple(STATEMENT_HEADINGS)))
            and n_nums >= 30 and density >= 0.2)


def select_chunks(chunks: list[Chunk], group: str,
                  word_budget: int = WORD_BUDGET_PER_GROUP) -> list[Chunk]:
    keywords = KEYWORD_GROUPS[group]
    scored = []
    for c in chunks:
        if is_toc(c.text):
            log.debug("[%s] chunk %d skipped: table of contents", group, c.id)
            continue
        s = score_chunk(c.text, keywords, boost_statements=(group == "financials"))
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda sc: (-sc[0], sc[1].id))

    picked, used = [], 0
    for s, c in scored:
        if used + c.words > word_budget:
            continue  # try smaller chunks further down the list
        picked.append(c)
        used += c.words
        log.info("[%s] picked chunk %d (pages %s, score %.1f, %d words)",
                 group, c.id, _page_range(c.pages), s, c.words)
    picked.sort(key=lambda c: c.id)
    log.info("[%s] %d chunk(s), %d words", group, len(picked), used)
    return picked


def _page_range(pages: list[int]) -> str:
    if not pages:
        return "?"
    return str(pages[0]) if len(pages) == 1 else f"{pages[0]}-{pages[-1]}"
