"""Step 3: find the latest annual report URL on the company's website.

Strategy: Firecrawl map (with a search term) -> filter URLs -> pick the best:
PDF first, newest year, English version, keywords in the file name. If no PDF
turns up, scrape one investor/results page and look for PDF links in it.

Keywords cover English plus German, the Nordic languages (sv, no, da, fi, is),
Dutch, French, Spanish and Italian, because many European companies use native
words in their file names even for the English report.
"""

import datetime as dt
import logging
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from urllib.parse import unquote, urljoin, urlparse

from .config import MAP_LIMIT, fold
from firecrawl import FirecrawlError

from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient

log = logging.getLogger(__name__)

# English first (we prefer English reports); the native term for the company's
# country (from its LEI) is tried next, before the broader fallbacks.
MAP_SEARCH_TERMS = ["annual report", "integrated report", "investors"]
NATIVE_SEARCH_TERM = {
    "DE": "geschäftsbericht", "AT": "geschäftsbericht", "CH": "geschäftsbericht",
    "SE": "årsredovisning", "NO": "årsrapport", "DK": "årsrapport",
    "FI": "vuosikertomus", "IS": "ársskýrsla", "NL": "jaarverslag", "BE": "jaarverslag",
    "FR": "rapport annuel", "LU": "rapport annuel", "ES": "informe anual",
    "IT": "relazione finanziaria annuale",
}

# (keyword, language, weight). Weight 2 = the annual report itself; 1 = weaker
# signals (a narrative "annual review", a directors' report, ...).
KEEP_KEYWORDS = [
    ("annual-report", "en", 2), ("annualreport", "en", 2), ("integrated-report", "en", 2),
    ("10-k", "en", 1), ("form-10-k", "en", 1), ("20-f", "en", 1),   # US filings: below "annual report"
    ("universal-registration", "en", 2), ("report-and-accounts", "en", 2),
    ("annual-financial-report", "en", 2), ("financial-statements", "en", 2),
    ("annual-and-sustainability", "en", 2),
    ("annual-review", "en", 1),
    ("geschäftsbericht", "de", 2), ("konzernabschluss", "de", 2),
    ("jahresbericht", "de", 1), ("konzernbericht", "de", 1),
    ("årsredovisning", "sv", 2), ("års-och-hållbarhetsredovisning", "sv", 2),
    ("årsrapport", "no/da", 2), ("årsberetning", "no", 1),
    ("årsregnskap", "no", 1), ("årsregnskab", "da", 1),
    ("vuosikertomus", "fi", 2), ("tilinpäätös", "fi", 2), ("toimintakertomus", "fi", 1),
    ("ársskýrsla", "is", 2), ("ársreikningur", "is", 2),
    ("jaarverslag", "nl", 2), ("jaarrapport", "nl", 2),
    ("rapport-annuel", "fr", 2), ("document-d-enregistrement-universel", "fr", 2),
    ("informe-anual", "es", 2), ("cuentas-anuales", "es", 2),
    ("relazione-finanziaria-annuale", "it", 2), ("relazione-annuale", "it", 2),
]
# German companies often abbreviate Geschäftsbericht as "GB" in the file name:
# "GB_1u1_2025_ENG.pdf", "1und1-AG_GB-2024_EN.pdf". Only trusted in the file name
# and next to a year, because "/gb/" is also a UK locale folder.
_GB_FILE_RE = re.compile(r"(?<![a-z0-9])gb-(?:[a-z0-9]+-)?20\d{2}(?![0-9])")

# Documents that are never the annual report.
TYPE_EXCLUDES = [
    "half-year", "halfyear", "interim", "quarter", "q1", "q2", "q3", "q4", "h1", "9m",
    "summary", "presentation", "factsheet", "capital-markets", "tax-report",
    "impact-report", "green-bond", "modern-slavery", "bulletin", "release",
    "parent-company",
    # not reports themselves, but often newer than the report and keyword-matching
    "press-release", "news",
    "halbjahr", "quartal", "zwischenbericht", "zwischenmitteilung", "präsentation",
    "jahresabschluss", "einzelabschluss",           # German parent-only accounts
    "delårsrapport", "kvartal", "halvår", "bokslutskommuniké",
    "osavuosikatsaus", "puolivuosikatsaus", "liiketoimintakatsaus", "tilinpäätöstiedote",
    "árshlutauppgjör", "árshlutareikningur",
    "halfjaar", "kwartaal", "semestriel", "trimestriel", "semestral", "trimestral",
    "semestrale", "trimestrale",
    # Pages *about* the report, not the report (seen in a 96-company Nordic run):
    # calendar entries, events, press releases and news, notices, bond documents.
    "calendar", "kalender", "kalenteri", "event", "events", "begivenhed", "evenemang",
    "tapahtuma", "webcast", "publishes", "published", "pressmeddelande", "pressemelding",
    "pressemeddelelse", "tiedote", "nyheder", "nyheter", "uutiset", "tidindi", "invitation",
    "kallelse", "innkalling", "indkaldelse", "bond", "joukkovelkakirja", "prospectus",
    "prospekt", "publicerar", "publiserer", "offentliggor", "offentliggjort", "julkaisee",
    "now-available", "aktuelles", "pressemitteilung", "verschiebung", "postpone",
]
# Only these file types can be a report (an .ics calendar entry once won as "the report").
_REPORT_EXTENSIONS = {"", ".pdf", ".html", ".htm", ".aspx", ".php", ".jsp"}

# A file named after another country is usually a subsidiary's or region's report
# ("ABB India Limited Integrated Annual Report 2025" on abb.com). Words that are part
# of the company's own name or its own country are allowed.
_COUNTRY_WORDS = {
    "SE": ["sweden", "sverige", "swedish"], "NO": ["norway", "norge", "norwegian"],
    "DK": ["denmark", "danmark", "danish"], "FI": ["finland", "suomi", "finnish"],
    "IS": ["iceland", "island"], "FO": ["faroe", "foroyar"],
    "DE": ["germany", "deutschland"], "GB": ["uk", "united-kingdom"], "US": ["usa", "america"],
    "CH": ["switzerland", "schweiz", "suisse"], "NL": ["netherlands", "nederland"],
    "PL": ["poland", "polska"], "EE": ["estonia", "eesti"], "LV": ["latvia"], "LT": ["lithuania"],
    "IN": ["india", "indian"], "CN": ["china", "chinese"], "BR": ["brazil", "brasil"],
    "MX": ["mexico"], "JP": ["japan"], "KR": ["korea"], "AU": ["australia"], "CA": ["canada"],
    "FR": ["france"], "IT": ["italy", "italia"], "ES": ["spain", "espana"],
    "ZA": ["south-africa"], "NG": ["nigeria"], "GH": ["ghana"], "BD": ["bangladesh"],
    "PK": ["pakistan"], "ID": ["indonesia"], "TR": ["turkey", "turkiye"], "RU": ["russia"],
}

# Freshness: stop early only on a recent report; never return an ancient one.
FRESH_MIN_AGE_YEARS = 1      # FY2025 counts as fresh during 2026
MAX_AGE_YEARS = 3            # older than this -> "not found" instead of a stale report
# Short pages mean a listing or teaser page, not an HTML annual report.
MIN_HTML_REPORT_CHARS = 20_000
MAX_ALTERNATIVES = 2         # candidates to try if the chosen file is unusable
# Credits kept back while searching, so a report found as a web page can still be
# fetched (1 scrape). Solstad Maritime spent its whole cap searching, then couldn't.
SEARCH_RESERVE_CREDITS = 1


def _reserve_left(fc, cost: int) -> None:
    """Stop searching when the next call would eat into the fetch reserve."""
    cap = getattr(fc, "max_credits", None)
    meter = getattr(fc, "credits", None)
    if cap is not None and meter is not None and meter.total + cost + SEARCH_RESERVE_CREDITS > cap:
        raise CreditBudgetExceeded(
            f"Stopping the search at {meter.total} of {cap} credits to keep "
            f"{SEARCH_RESERVE_CREDITS} for fetching the report")
# Separate topical reports. These don't exclude a COMBINED report, e.g. "annual report
# incl. sustainability report" or "års- och hållbarhetsredovisning".
TOPIC_EXCLUDES = [
    "sustainability", "esg", "remuneration", "governance-report", "corporate-governance",
    "people-and-planet",
    "nachhaltigkeit", "vergütungsbericht",
    "hållbarhet", "ersättningsrapport", "bolagsstyrning",
    "bærekraft", "godtgjørelse", "eierstyring", "bæredygtighed", "vederlagsrapport",
    "vastuullisuus", "palkitsemisraportti", "hallinnointi", "sjálfbærni",
    "duurzaamheid", "développement-durable", "sostenibilidad", "sostenibilità",
]
_COMBINE_WORDS = r"(?:incl|including|inkl|inklusive|and|och|og|ja|und|with|med)"

EN_MARKERS = {"en", "eng", "english"}
NATIVE_MARKERS = {"de", "deu", "ger", "deutsch", "sv", "swe", "svenska", "no", "nor", "nb",
                  "norsk", "da", "dan", "dk", "dansk", "fi", "fin", "suomi", "isl", "nl",
                  "nld", "fr", "fra", "es", "esp", "ita"}

# A year must stand alone: "2025.pdf" yes, the "2059" inside hash "205966bf" no. A
# fiscal-year prefix is allowed: "Annual-Financial-Report-FY2025.pdf" (Siemens), "GJ2025".
_YEAR_RE = re.compile(r"(?<![0-9a-z])(?:fy|gj)?(20\d{2})(?![0-9])")
# A year inside a date written without separators: "jumboannualreport_31122025_en.pdf"
# (ddmmyyyy) and "report_20251231.pdf" (yyyymmdd).
_DATE_RE = re.compile(r"(?<![0-9a-z])(?:[0-3]\d[01]\d(20\d{2})|(20\d{2})[01]\d[0-3]\d)(?![0-9a-z])")
_IR_PAGE_HINTS = ["annual-report", "report-and-accounts", "reports", "results", "berichte",
                  "rapporter", "raportit", "publications", "investor", "sijoittaj"]


def _norm(url: str) -> str:
    """Folded URL with '-' as the only word separator."""
    t = fold(unquote(unquote(url)))
    t = re.sub(r"[\s_+]+", "-", t)
    return re.sub(r"-{2,}", "-", t)


def _word_re(word: str) -> re.Pattern:
    # Short tokens ("q1", "esg", "h1") must stand alone, so "faq1" doesn't match.
    # Longer words only need a word start, so compounds like "kvartalsrapport" match
    # but "headquarters" doesn't trip "quarter".
    tail = r"(?![a-z0-9])" if len(word) <= 3 else ""
    return re.compile(rf"(?<![a-z0-9]){re.escape(word)}{tail}")


_KEEP = [(fold(k).replace(" ", "-"), lang, w) for k, lang, w in KEEP_KEYWORDS]
_TYPE = [(w, _word_re(fold(w))) for w in TYPE_EXCLUDES]
_FILE_NAME_ONLY = {"presentation", "präsentation", "summary", "factsheet"}
_TOPIC = [(w, _word_re(fold(w)),
           re.compile(rf"{_COMBINE_WORDS}-(?:[a-z0-9]+-){{0,2}}{re.escape(fold(w))}"))
          for w in TOPIC_EXCLUDES]


@dataclass
class ReportCandidate:
    url: str
    kept: bool
    reason: str
    year: int | None = None
    is_pdf: bool = False
    english: int = 0           # +1 English version, -1 another language, 0 unknown
    file_weight: int = 0       # keyword weight found in the file name
    path_weight: int = 0       # keyword weight found elsewhere in the URL
    unexplained: int = 0       # file-name words that aren't the company, a keyword or a year


@dataclass
class ReportResult:
    url: str
    year: int | None
    is_pdf: bool
    candidates: list[ReportCandidate] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)   # next best, if the first is unusable


class ReportNotFoundError(RuntimeError):
    pass


def is_pdf_url(url: str) -> bool:
    return urlparse(url).path.lower().endswith(".pdf")


def _split(url: str) -> tuple[str, str]:
    """(normalized path without file name, normalized file name)"""
    n = _norm(urlparse(url).path)
    path, _, name = n.rpartition("/")
    return path, name


def extract_year(url: str) -> int | None:
    """Year from the file name if it has one (folders are often the publication
    year, e.g. /2026/...-annual-report-2025.pdf), else from the whole URL."""
    max_year = dt.date.today().year + 1
    for part in (_split(url)[1], _norm(url)):
        found = _YEAR_RE.findall(part) + [a or b for a, b in _DATE_RE.findall(part)]
        years = [int(y) for y in found if int(y) <= max_year]
        if years:
            return max(years)
    return None


def _keywords(text: str) -> list[tuple[str, str, int]]:
    found = [(k, lang, w) for k, lang, w in _KEEP if k in text]
    if _GB_FILE_RE.search(text):
        found.append(("gb-<year>", "de", 2))
    return found


def _language(url: str, keywords: list[tuple[str, str, int]]) -> int:
    path, name = _split(url)
    for part in (name, path):
        tokens = set(re.split(r"[^a-z0-9]+", part))
        if tokens & EN_MARKERS:
            return 1
        if tokens & NATIVE_MARKERS:
            return -1
    langs = {lang for _, lang, _ in keywords}
    if langs == {"en"}:
        return 1
    return -1 if langs and "en" not in langs else 0


def allowed_place_words(company_name: str | None, countries) -> frozenset[str]:
    """Country words that may appear in this company's report URLs: its own
    countries' names and any word of its own name ("Norwegian Air Shuttle")."""
    words = set()
    for c in countries:
        words.update(fold(w) for w in _COUNTRY_WORDS.get((c or "").upper(), []))
    if company_name:
        words.update(re.findall(r"[a-z0-9]+", fold(company_name)))
    return frozenset(words)


_FOREIGN = [(w, re.compile(rf"(?<![a-z0-9]){re.escape(fold(w))}(?![a-z0-9])"))
            for ws in _COUNTRY_WORDS.values() for w in ws]


# Legal forms in a file name. One the company doesn't have marks another entity's report.
_LEGAL_FORMS = {"plc", "ltd", "limited", "oyj", "nv", "bv", "spa", "gmbh", "inc", "llc", "ag",
                "asa", "sarl", "srl", "kgaa"}
# File-name words that say nothing about whose report it is.
_NEUTRAL_WORDS = ({w for k, _, _ in _KEEP for w in k.split("-")} | EN_MARKERS | NATIVE_MARKERS | {
    "annual", "report", "reports", "financial", "statements", "statement", "and", "the", "of",
    "group", "consolidated", "integrated", "combined", "management", "final", "web", "print",
    "online", "version", "spread", "spreads", "original", "single", "pages", "full", "digital",
    "interactive", "accounts", "review", "year", "fy", "gj", "ar", "ir", "doc", "document",
    "download", "file", "media", "secured", "sec", "esef", "low", "high", "res", "book",
    "accessible", "updated", "new", "copy", "pdf", "ua", "en", "gb", "eng", "incl", "inkl",
    "csrd", "esrs", "esef", "courtesy", "draft", "signed", "audited"})


def _unexplained(tokens: set[str], allowed_words: frozenset[str]) -> int:
    """Short alphabetic file-name words that are neither the company's name nor a
    keyword, year or language marker: 'sfm' in 'sfm-annual-report-2025.pdf' (a
    subsidiary). Hash-like and numeric parts don't count."""
    return sum(1 for t in tokens if t.isalpha() and 2 <= len(t) <= 6
               and t not in _NEUTRAL_WORDS and t not in allowed_words)


def classify(url: str, allowed_words: frozenset[str] = frozenset()) -> ReportCandidate:
    """Apply the keep/exclude filters to one URL and say why. `allowed_words`
    (see allowed_place_words) are country words that don't mark a subsidiary."""
    ext = PurePosixPath(urlparse(url).path).suffix.lower()
    if ext not in _REPORT_EXTENSIONS:
        return ReportCandidate(url, False, f"excluded: not a report file ({ext})")
    u = _norm(url)
    file_name = ([s for s in _norm(urlparse(url).path).split("/") if s] or [""])[-1]
    for word, rx in _TYPE:
        # "presentation" etc. only count in the file name: IR folders are often called
        # "report-and-presentations" (Aker, Ørsted) and hold the annual report too.
        if rx.search(file_name if word in _FILE_NAME_ONLY else u):
            return ReportCandidate(url, False, f"excluded: contains '{word}'")
    for word, rx, combined in _TOPIC:
        if rx.search(u) and not combined.search(u):
            return ReportCandidate(url, False, f"excluded: contains '{word}'")
    path_only = _norm(urlparse(url).path)
    for word, rx in _FOREIGN:
        if fold(word) not in allowed_words and rx.search(path_only):
            return ReportCandidate(url, False, f"excluded: names another country ('{word}'), "
                                               f"probably a subsidiary's or region's report")

    path, name = _split(url)
    tokens = set(re.split(r"[^a-z0-9]+", name.rsplit(".", 1)[0]))
    other_form = (tokens & _LEGAL_FORMS) - allowed_words
    if allowed_words and other_form and not (tokens & _LEGAL_FORMS & allowed_words):
        # "siemens-plc-annual-report-2025.pdf" on siemens.com, for Siemens AG
        return ReportCandidate(url, False, f"excluded: names another legal entity "
                                           f"('{sorted(other_form)[0]}'), probably a subsidiary's report")
    in_name = _keywords(name)
    # The GB abbreviation only counts in the file name; drop it from the path check.
    in_path = [k for k in _keywords(path) if k[0] != "gb-<year>"]
    if not in_name and not in_path:
        return ReportCandidate(url, False, "no annual-report keyword")
    words = sorted({k for k, _, _ in in_name + in_path})
    return ReportCandidate(
        url, True, f"keyword {words}", extract_year(url), is_pdf_url(url),
        english=_language(url, in_name + in_path),
        file_weight=sum(w for _, _, w in in_name), path_weight=sum(w for _, _, w in in_path),
        unexplained=_unexplained(tokens, allowed_words))


def _is_doc(c: ReportCandidate) -> bool:
    """A document that can be the report: a PDF, or an HTML page for one report year."""
    return c.is_pdf or _looks_like_report_page(c.url)


def _rank(c: ReportCandidate, today: dt.date | None = None) -> tuple:
    """Documents before listing pages. Among recent reports (FY last year or newer)
    PDF wins, then the newest year; among older ones the newest year wins (so AAK's
    current HTML report beats its 2021 PDF). Then English, keywords in the file name,
    keywords in the path, shortest URL."""
    year = c.year or 0
    fresh = year >= (today or dt.date.today()).year - FRESH_MIN_AGE_YEARS
    head = (c.is_pdf, year) if fresh else (year, c.is_pdf)
    return (_is_doc(c), fresh, *head, c.english, -c.unexplained, c.file_weight, c.path_weight,
            -len(c.url))


def pick_best(candidates: list[ReportCandidate]) -> ReportCandidate | None:
    """The best kept candidate by _rank (e.g. 'annual-report-and-accounts' beats
    'annual-report-on-form-20-f', and an annual report beats a tax report in the
    same 'annual_report' folder)."""
    kept = [c for c in candidates if c.kept]
    return max(kept, key=_rank) if kept else None


def _dedupe(urls) -> list[str]:
    seen, out = set(), []
    for u in urls:
        u = u.split("#")[0]
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _log_candidates(cands: list[ReportCandidate], source: str) -> None:
    for c in cands:
        if c.kept:
            log.info("[%s] KEEP %s (year=%s, pdf=%s, english=%+d, %s)",
                     source, c.url, c.year, c.is_pdf, c.english, c.reason)
        else:
            log.debug("[%s] drop %s (%s)", source, c.url, c.reason)
    log.info("[%s] %d URL(s), %d kept", source, len(cands), sum(c.kept for c in cands))


def search_terms(country: str | None) -> list[str]:
    terms = list(MAP_SEARCH_TERMS)
    native = NATIVE_SEARCH_TERM.get((country or "").upper())
    if native:
        terms.insert(1, native)
    return terms


def _result(best: ReportCandidate, cands: list[ReportCandidate]) -> ReportResult:
    if best.english < 0:
        log.warning("Chosen report looks non-English (%s); extracting from it anyway.", best.url)
    oldest_ok = dt.date.today().year - MAX_AGE_YEARS
    others = sorted((c for c in cands if c.kept and c.url != best.url and _is_doc(c)
                     and (c.year is None or c.year >= oldest_ok)), key=_rank, reverse=True)
    alternatives = list(dict.fromkeys(c.url for c in others))[:MAX_ALTERNATIVES]
    return ReportResult(best.url, best.year, best.is_pdf, cands, alternatives)


def is_fresh(c: ReportCandidate | None, today: dt.date | None = None) -> bool:
    """A recent PDF: good enough to stop searching."""
    year = (today or dt.date.today()).year
    return bool(c and c.is_pdf and (c.year or 0) >= year - FRESH_MIN_AGE_YEARS)


def _looks_like_report_page(url: str) -> bool:
    """An HTML annual report (one page per report year), not a listing/archive page."""
    segments = [s for s in _norm(urlparse(url).path).split("/") if s]
    name = segments[-1] if segments else ""
    return bool(_YEAR_RE.search(name) and _keywords(name)
                and not re.search(r"(?<![a-z])(reports|archive|arkiv|arkisto)(?![a-z])", name))


def find_report(website_url: str, fc: FirecrawlClient, country: str | None = None,
                company_name: str | None = None, other_countries=()) -> ReportResult:
    """Cheapest first, stopping as soon as a recent PDF turns up:
    1. map "annual report";
    2. scrape the investor "annual reports" page for PDF links (finds current reports
       hosted elsewhere, e.g. storage.mfn.se, that the map doesn't know yet);
    3. map the native term (e.g. "årsredovisning"), then "integrated report", "investors".
    Stops early when the per-company credit cap is reached. Never returns a report
    older than MAX_AGE_YEARS, and never a listing/calendar page."""
    allowed = allowed_place_words(company_name, [country, *other_countries])
    all_cands: list[ReportCandidate] = []
    all_urls: list[str] = []
    scraped: set[str] = set()

    def add(urls: list[str], source: str) -> ReportCandidate | None:
        cands = [classify(u, allowed) for u in urls]
        _log_candidates(cands, source)
        all_cands.extend(cands)
        return pick_best(all_cands)

    def scrape_ir_page() -> ReportCandidate | None:
        ir_page = _pick_ir_page(all_cands, _dedupe(all_urls), website_url, exclude=scraped)
        if ir_page is None:
            return pick_best(all_cands)
        scraped.add(ir_page)
        log.info("Scraping IR page %s for report links", ir_page)
        try:
            _reserve_left(fc, 1)
            page = fc.scrape(ir_page, formats=["markdown", "links"])
        except FirecrawlError as e:          # e.g. "all scraping engines failed"
            log.warning("Could not scrape %s: %s", ir_page, str(e)[:150])
            return pick_best(all_cands)
        found = page["links"] + re.findall(r"\((https?://[^)\s]+\.pdf[^)\s]*)\)", page["markdown"])
        # PDFs, and also links to report *pages* (some companies publish the annual
        # report as a web page, or link the PDF only through script).
        linked = _dedupe(urljoin(ir_page, u) for u in found)
        titles = _link_titles(page["markdown"], ir_page)
        cands = []
        for u in linked:
            if not (is_pdf_url(u) or _looks_like_report_page(u)):
                continue
            title = titles.get(u)
            if title and not rf_keywords_in(u):
                # "[2025 Annual Report](https://s202.q4cdn.com/.../8769e063.pdf)": the
                # file name says nothing, so judge it by its link text instead.
                ext = ".pdf" if is_pdf_url(u) else ""
                c = classify(f"{u.split('?')[0].rsplit('/', 1)[0]}/{title}{ext}", allowed)
                c.url, c.is_pdf = u, is_pdf_url(u)
            else:
                c = classify(u, allowed)
            cands.append(c)
        _log_candidates(cands, f"scrape {ir_page}")
        all_cands.extend(cands)
        return pick_best(all_cands)

    try:
        for i, term in enumerate(search_terms(country)):
            _reserve_left(fc, 1)
            links = fc.map(website_url, search=term, limit=MAP_LIMIT)
            urls = _dedupe(l["url"] for l in links if l.get("url"))
            all_urls += urls
            if is_fresh(add(urls, f"map '{term}'")):
                break
            if i == 0 and is_fresh(scrape_ir_page()):
                break
        else:
            scrape_ir_page()                 # a better IR page may have turned up since
    except CreditBudgetExceeded as e:
        log.warning("%s; choosing from what was found so far", e)

    best = pick_best(all_cands)
    if not best:
        raise ReportNotFoundError(
            f"No annual report found on {website_url} "
            f"({len(all_cands)} URLs checked). Pass --report-url URL.")
    oldest_ok = dt.date.today().year - MAX_AGE_YEARS
    if best.year and best.year < oldest_ok:
        raise ReportNotFoundError(
            f"Only old reports found on {website_url} (newest: FY{best.year}, {best.url}). "
            f"Pass --report-url URL.")
    if not best.is_pdf and not _looks_like_report_page(best.url):
        raise ReportNotFoundError(
            f"No annual report PDF found on {website_url}; best match is a listing page "
            f"({best.url}). Pass --report-url URL.")
    return _result(best, all_cands)


# Pages not worth scraping for report links. Narrower than TYPE_EXCLUDES: a
# "reports-and-presentations" page is exactly the page we want.
_NOT_IR_PAGE = [_word_re(fold(w)) for w in (
    "calendar", "kalender", "kalenteri", "event", "events", "begivenhed", "evenemang",
    "tapahtuma", "webcast", "news", "nyheder", "nyheter", "uutiset", "press", "tidindi",
    "release", "published", "publishes")]


_MD_LINK = re.compile(r"\[([^\]]{3,200})\]\((https?://[^)\s]+|/[^)\s]*)\)")


def _link_titles(markdown: str, base: str) -> dict[str, str]:
    """URL -> link text, from markdown links (inner images and markup removed)."""
    out = {}
    for text, href in _MD_LINK.findall(markdown or ""):
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)|[*_`#]", " ", text)
        text = re.sub(r"\s+", "-", text.strip())
        if text:
            out.setdefault(urljoin(base, href), text)
    return out


def reports_linked_from(markdown: str, page_url: str) -> list[str]:
    """Annual-report PDFs linked from a page we already scraped (a teaser page:
    "Annual report 2025 now available"), best first. When no link names a report but
    the page links exactly one PDF, that PDF is the one the page is about."""
    found = [href for _, href in _MD_LINK.findall(markdown or "")]
    found += re.findall(r"(https?://[^)\s\]\"'<>]+\.pdf[^)\s\]\"'<>]*)", markdown or "")
    pdfs = [u for u in _dedupe(urljoin(page_url, u) for u in found) if is_pdf_url(u)]
    titles = _link_titles(markdown, page_url)
    cands = []
    for u in pdfs:
        title = titles.get(u)
        if title and not rf_keywords_in(u):
            c = classify(f"{u.split('?')[0].rsplit('/', 1)[0]}/{title}.pdf")
            c.url, c.is_pdf = u, True
        else:
            c = classify(u)
        cands.append(c)
    kept = sorted((c for c in cands if c.kept), key=_rank, reverse=True)
    if kept:
        return [c.url for c in kept]
    return pdfs if len(pdfs) == 1 else []


def rf_keywords_in(url: str) -> bool:
    """Does the URL itself carry an annual-report keyword?"""
    path, name = _split(url)
    return bool(_keywords(name) or _keywords(path))


def _parent(url: str) -> str:
    p = urlparse(url)
    path = p.path.rstrip("/")
    return f"{p.scheme}://{p.netloc}{path.rsplit('/', 1)[0]}/" if "/" in path.strip("/") else ""


def _pick_ir_page(cands: list[ReportCandidate], urls: list[str], website_url: str,
                  exclude: set[str] = frozenset()) -> str | None:
    """The page most likely to link the *current* report, not yet scraped. Candidates:
    HTML pages about annual reports, the parent listing of an HTML report page
    (reports.aak.com/reports/Annual_Report_2021 -> reports.aak.com/reports/), and
    reports/investor pages. Pages with an old year in the URL rank last; then pages
    with no year; then the shortest. Never calendar/event/news/press pages."""
    html = [u for u in urls if not is_pdf_url(u)
            and PurePosixPath(urlparse(u).path).suffix.lower() in _REPORT_EXTENSIONS]
    known = [c.url for c in cands if c.kept and not c.is_pdf]       # pages about annual reports
    known += [_parent(u) for u in known if _looks_like_report_page(u)]
    pages = list(known)
    for hint in _IR_PAGE_HINTS:
        # the path only: on investor.firstsolar.com every page contains "investor"
        pages += [u for u in html if hint in _norm(urlparse(u).path)]
    pages = [u for u in dict.fromkeys(pages) if u and u not in exclude
             and not any(rx.search(_norm(u)) for rx in _NOT_IR_PAGE)
             and "ical" not in _norm(urlparse(u).path)]      # DownloadICal.aspx = calendar file
    fresh_year = dt.date.today().year - FRESH_MIN_AGE_YEARS

    def rank(u: str) -> tuple:
        year = extract_year(u)
        return (u not in known, year is not None and year < fresh_year, year is not None, len(u))
    if pages:
        return min(pages, key=rank)
    fallback = urljoin(website_url, "/investors/")
    return None if fallback in exclude else fallback
