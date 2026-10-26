"""Document fallback: the company's other documents, for the data points still empty
after the annual report (python -m extractor.datapoints).

The report finder keeps only *the* annual report and drops remuneration, governance and
sustainability reports, year-end reports and the like. Those hold exactly the data
points the annual report often lacks, so this module finds them again:

  1. the site URLs the report search already listed (cache/<slug>_discovery.json; free);
  2. one plain Firecrawl map of the site, then a map search per document type
     ("remuneration report", "shareholders"...), 1 credit each, cached;
  3. links on the pages already fetched (free).

Only the company's own documents: its site and subdomains, plus PDFs it links to on
document hosts (e.g. storage.mfn.se). Never a domain on the blocked list. PDFs are
downloaded and converted locally (free); web pages are scraped by Firecrawl (1 credit).
Everything is cached, so re-runs cost nothing.
"""

import datetime as dt
import hashlib
import html
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin, urlparse

import httpx
from firecrawl import PaymentRequiredError

from .config import CACHE_DIR, MAP_LIMIT, fold
from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from .report_finder import EN_MARKERS, NATIVE_MARKERS, _link_titles, _norm, extract_year, is_pdf_url
from .scraper import (DownloadError, NeedsOCRError, Page, check_not_scanned, download,
                      looks_like_pdf, markdown_to_pages, pages_to_markdown, pdf_to_pages)
from .website import is_blocked, registered_domain

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DocType:
    key: str
    label: str              # for `source`, e.g. "Remuneration report (PDF)"
    search: str             # Firecrawl map search term
    words: tuple[str, ...]  # URL / link-text keywords, about 10 languages
    avoid: tuple[str, ...] = ()   # words of a neighbouring type: rank lower, don't exclude
    pdf_first: bool = False       # a report: its PDF beats a web page about it


_POLICY_WORDS = ("policy", "guidelines", "riktlinjer", "retningslinjer", "politik", "politikk",
                 "politiikka", "vergütungssystem", "beleid", "politique", "política", "politica")

DOC_TYPES = {d.key: d for d in [
    DocType("remuneration", "Remuneration report", "remuneration report", (
        "remuneration", "compensation-report", "vergütungsbericht", "vergütung",
        "ersättningsrapport", "ersättning", "godtgjørelse", "lederlønn", "lederløn",
        "vederlagsrapport", "palkitsemisraportti", "palkitseminen", "bezoldiging",
        "remuneratie", "rémunération", "remuneraciones", "remunerazione", "iarc",
        "starfskjarastefna"), avoid=_POLICY_WORDS, pdf_first=True),
    DocType("remuneration_policy", "Remuneration policy", "remuneration policy", (
        "remuneration-policy", "compensation-policy", "pay-policy", "vergütungssystem",
        "vergütungspolitik", "riktlinjer-för-ersättning", "ersättningspolicy",
        "retningslinjer-for-lederlønn", "retningslinjer-for-fastsettelse",
        "godtgjørelsespolitikk", "vederlagspolitik", "lønpolitik", "palkitsemispolitiikka",
        "bezoldigingsbeleid", "remuneratiebeleid", "politique-de-rémunération",
        "política-de-remuneraciones", "politica-di-remunerazione", "politica-sulla-remunerazione",
        "política-de-remuneração"), pdf_first=True),
    DocType("agm_notice", "AGM notice", "annual general meeting", (
        "notice-of-annual-general-meeting", "notice-of-agm", "agm-notice", "notice-of-meeting",
        "annual-general-meeting", "agm", "kallelse", "årsstämma", "innkalling",
        "generalforsamling", "indkaldelse", "kokouskutsu", "yhtiökokous", "hauptversammlung",
        "oproeping", "algemene-vergadering", "convocation", "assemblée-générale",
        "junta-general", "convocatoria", "assemblea", "aðalfundur"), pdf_first=True),
    DocType("governance", "Corporate governance report", "corporate governance", (
        "corporate-governance", "governance-report", "governance-statement", "governance",
        "bolagsstyrning", "eierstyring", "foretaksstyring", "selskabsledelse", "hallinnointi",
        "hallinto", "unternehmensführung", "deugdelijk-bestuur", "gouvernement-d-entreprise",
        "gobierno-corporativo", "governo-societario", "stjórnarhættir"), pdf_first=True),
    DocType("sustainability", "Sustainability report", "sustainability report", (
        "sustainability", "esg", "gri", "csrd", "hållbarhet", "bærekraft", "bæredygtighed",
        "ansvarlighed", "vastuullisuus", "yritysvastuu", "nachhaltigkeit", "duurzaamheid",
        "développement-durable", "sostenibilidad", "sostenibilità", "sjálfbærni"), pdf_first=True),
    DocType("share", "Share information", "share", (
        "the-share", "share-information", "share-data", "shareinformation", "share-capital",
        "stock-information", "share", "shares", "aktien", "aktie", "aksjen", "aksje",
        "osake", "osakkeet", "aandeel", "l-action", "accion", "azioni", "hlutabréf")),
    DocType("shareholders", "Shareholder information", "shareholders", (
        "largest-shareholders", "major-shareholders", "shareholders", "shareholder-structure",
        "ownership", "owners", "aktieägare", "ägarstruktur", "ägare", "aksjonærer",
        "eierstruktur", "eiere", "aktionærer", "ejerforhold", "ejere", "osakkeenomistajat",
        "omistajat", "aktionäre", "aktionärsstruktur", "aandeelhouders", "actionnariat",
        "accionistas", "azionisti", "azionariato", "hluthafar")),
    DocType("legal_notice", "Legal notice", "legal notice", (
        "impressum", "imprint", "legal-notice", "legal-information", "legal",
        "company-information", "corporate-information", "juridisk", "mentions-légales",
        "aviso-legal", "note-legali", "colofon", "contact", "kontakt", "yhteystiedot")),
    DocType("year_end", "Year-end report", "year-end report", (
        "year-end-report", "full-year-report", "full-year", "fourth-quarter", "q4",
        "annual-results", "preliminary-results", "bokslutskommuniké", "tilinpäätöstiedote",
        "jahresfinanzbericht"), pdf_first=True),
    DocType("listing", "Listing notice", "listing", (
        "ipo", "initial-public-offering", "listing", "first-day-of-trading",
        "admission-to-trading", "notering", "börsnotering", "börsintroduktion",
        "första-dag-för-handel", "børsnotering", "listautuminen", "listautumisanti",
        "börsengang", "introduction-en-bourse")),
    DocType("history", "Company history", "history", (
        "history", "our-history", "milestones", "historia", "historie", "historik",
        "geschichte", "histoire", "storia", "geschiedenis")),
    DocType("report_hub", "Report downloads page", "reports", (
        "annual-reports", "reports", "reports-and-presentations", "downloads", "publications",
        "download-centre", "download-center", "reporting-centre", "rapporter", "berichte",
        "publikationen", "julkaisut", "publicaties", "rapports", "informes", "relazioni")),
    DocType("about", "Company profile", "about us", (
        "about-us", "about", "who-we-are", "at-a-glance", "in-brief", "om-oss", "om-os",
        "über-uns", "unternehmen", "à-propos", "qui-sommes-nous", "chi-siamo",
        "quienes-somos", "over-ons", "meistä", "yritys")),
]}

# Data point -> document types, most likely first (docs/document_fallback_plan.md).
# Covers every data point the data-point AI pass can answer.
DP_DOC_TYPES = {
    "pension_type": ["remuneration_policy", "remuneration", "agm_notice"],
    "benefits": ["remuneration_policy", "remuneration"],
    "shareholding_requirement": ["remuneration_policy", "remuneration", "agm_notice"],
    "largest_holders": ["shareholders", "governance"],
    "controlling_owner": ["shareholders", "governance"],
    "controlling_owner_name": ["shareholders", "governance"],
    "ownership_type": ["shareholders", "governance"],
    "pe_stake_5pct": ["shareholders", "governance"],
    "ultimate_parent": ["shareholders", "legal_notice", "about"],
    "isin": ["share"],
    "share_price": ["share"],
    "ticker": ["share"],
    "exchange": ["share", "governance"],
    "exchange_segment": ["share", "governance"],
    "listing_date": ["listing", "share", "history"],
    "listing_status": ["share", "governance"],
    "shares_outstanding": ["share", "shareholders"],
    "fte": ["sustainability", "year_end"],
    "headcount": ["sustainability", "year_end", "about"],
    "staff_by_country": ["sustainability"],
    "staff_by_segment": ["sustainability", "year_end"],
    "revenue_by_country": ["year_end"],
    "revenue_by_segment": ["year_end"],
    "revenue": ["year_end"],
    "total_assets": ["year_end"],
    "ebitda": ["year_end"],
    "reporting_currency": ["year_end"],
    "fiscal_year_end": ["year_end"],
    "accounting_basis": ["year_end"],
    "website": ["legal_notice", "about"],
    "legal_name": ["legal_notice", "about"],
    "business_id": ["legal_notice"],
    "country_code": ["legal_notice", "about"],
    "head_office_city": ["legal_notice", "about"],
    "other_names": ["history", "legal_notice"],
    "sub_sector": ["about"],
}

DOC_EXTENSIONS = {"", ".pdf", ".html", ".htm", ".aspx", ".php", ".jsp"}   # Excel/Word: phase 2
# Never worth fetching for any document type.
_SKIP = [re.compile(rf"(?<![a-z0-9]){w}(?![a-z0-9])") for w in (
    "privacy", "cookies?", "login", "careers?", "jobs?", "vacanc[a-z]*", "webcast",
    "calendar", "kalender", "kalenteri", "ical", "shop", "cart", "products?")]
# News and blog pages are about an event, not the page or document itself (a merger post
# once passed as "Shareholder information"). Only the listing notice is news by nature.
_NEWS_PAGE = re.compile(r"(?<![a-z0-9])(news|blog|press|media|announcements?|releases?|"
                        r"nyheter|nyheder|uutiset|tiedotteet|meddelelser|borsmeddelelser|"
                        r"pressmeddelanden?|pressemitteilungen?|aktuelles)(?![a-z0-9])")
STALE_YEARS = 2              # a dated document older than the report year - this is skipped
MAX_DOCS_PER_TYPE = 2        # documents tried per type over all rounds
MIN_TEXT_CHARS = 200         # shorter pages hold nothing


def _keyword_re(word: str) -> re.Pattern:
    # Short words ("esg", "q4", "agm") stand alone; longer ones need a word start only,
    # so compounds like "ersättningsrapport" still match "ersättning".
    w = re.escape(fold(word).replace(" ", "-"))
    tail = r"(?![a-z0-9])" if len(word) <= 3 else ""
    return re.compile(rf"(?<![a-z0-9]){w}{tail}")


_WORDS = {k: [_keyword_re(w) for w in d.words] for k, d in DOC_TYPES.items()}
_AVOID = {k: [_keyword_re(w) for w in d.avoid] for k, d in DOC_TYPES.items()}


def gap_types(gaps: list[str]) -> list[DocType]:
    """Document types worth trying for these gaps, by expected yield: a type scores 2
    per gap it is the first choice for, 1 per gap it is a later choice for."""
    score: dict[str, int] = {}
    for g in gaps:
        for i, key in enumerate(DP_DOC_TYPES.get(g, [])):
            score[key] = score.get(key, 0) + (2 if i == 0 else 1)
    return [DOC_TYPES[k] for k in sorted(score, key=lambda k: -score[k])]


@dataclass
class Candidate:
    url: str
    doc_type: DocType
    score: float            # keyword match: 2 file name, 1 path, +1 link text
    year: int | None
    is_pdf: bool
    english: int            # +1 English, -1 another language, 0 unknown


def classify(url: str, doc_type: DocType, title: str = "",
             report_year: int | None = None) -> Candidate | None:
    """Is this URL (with its link text, if known) a document of this type?"""
    p = urlparse(url)
    ext = PurePosixPath(p.path).suffix.lower()
    if p.scheme not in ("http", "https") or ext not in DOC_EXTENSIONS or is_blocked(p.netloc):
        return None
    path = _norm(p.path)
    if any(rx.search(path) for rx in _SKIP):
        return None
    if doc_type.key != "listing" and not is_pdf_url(url) and _NEWS_PAGE.search(path):
        return None
    folder, _, name = path.rpartition("/")
    text = _norm(title) if title else ""
    rxs = _WORDS[doc_type.key]
    score = (2 if any(rx.search(name) for rx in rxs) else 1 if any(rx.search(folder) for rx in rxs)
             else 0) + (1 if text and any(rx.search(text) for rx in rxs) else 0)
    if not score:
        return None
    if any(rx.search(f"{path} {text}") for rx in _AVOID[doc_type.key]):
        score -= 1.5          # a policy is not the report: kept, but ranked below it
    year = extract_year(url) or (extract_year("/" + text) if text else None)
    if year and report_year and year < report_year - STALE_YEARS:
        return None
    tokens = set(re.split(r"[^a-z0-9]+", path))
    english = 1 if tokens & EN_MARKERS else -1 if tokens & NATIVE_MARKERS else 0
    return Candidate(url, doc_type, score, year, is_pdf_url(url), english)


def _rank(c: Candidate, report_year: int | None) -> tuple:
    """Best keyword match in the URL first (link text only breaks ties after the year: a
    2024 report whose link says "Remuneration report 2024" must not beat the 2025 one);
    for report types a PDF before a web page about it; then the report's year or newer,
    then the newest; then English; then the shortest URL (top-level pages first)."""
    current = bool(c.year and report_year and c.year >= report_year)
    return (min(c.score, 2), c.is_pdf and c.doc_type.pdf_first, current, c.year or 0, c.score,
            c.english, -len(c.url))


@dataclass
class Document:
    url: str
    doc_type: DocType
    kind: str                    # "pdf" or "web"
    pages: list[Page]
    year: int | None
    retrieved_at: str
    links: dict[str, str] = field(default_factory=dict)    # url -> link text
    path: Path | None = None     # the cached PDF (kind "pdf"), for page images

    @property
    def source(self) -> str:
        return f"{self.doc_type.label} ({'PDF' if self.kind == 'pdf' else 'web page'})"


def _canonical(url: str) -> str:
    """One spelling per page: no fragment, no trailing slash ("/owners/" = "/owners")."""
    url = url.split("#")[0]
    return url.rstrip("/") if urlparse(url).path not in ("", "/") else url


def _stem(slug: str, url: str) -> str:
    return f"{slug}_doc_{hashlib.sha1(url.encode()).hexdigest()[:16]}"


def _mtime(path) -> str:
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(timespec="seconds")


_PDF_LINK = re.compile(r"(https?://[^)\s\]\"'<>]+\.pdf[^)\s\]\"'<>]*)", re.I)


_FILE_FIELD = re.compile(
    r'"(?:originalFilename|fileName|filename|title|label|name)"\s*:\s*"([^"]{3,200})"'
    r'[^{}]{0,400}?"(?:url|href|src|downloadUrl)"\s*:\s*"(https?://[^"]+\.pdf[^"]*)"'
    r'|"(?:url|href|src|downloadUrl)"\s*:\s*"(https?://[^"]+\.pdf[^"]*)"'
    r'[^{}]{0,400}?"(?:originalFilename|fileName|filename|title|label|name)"\s*:\s*"([^"]{3,200})"')
_ANY_PDF = re.compile(r'(https?://[^"\'\s<>()]+\.pdf)(?![a-z])', re.I)


def embedded_files(raw_html: str) -> dict[str, str]:
    """PDF addresses kept in a page's data rather than in links: download buttons whose
    file URL sits in the page's embedded JSON (Equinor's reports page:
    "originalFilename":"equinor-2025-remuneration-report.pdf","url":"https://cdn...").
    url -> label (the file name or title given next to it, else the URL's file name)."""
    text = html.unescape(raw_html or "").replace("\\/", "/").replace("\\", "")
    out: dict[str, str] = {}
    for m in _FILE_FIELD.finditer(text):
        label, url = (m.group(1), m.group(2)) if m.group(2) else (m.group(4), m.group(3))
        out.setdefault(url, label.replace("-", " ").replace("_", " "))
    for url in _ANY_PDF.findall(text):
        out.setdefault(url, urlparse(url).path.rsplit("/", 1)[-1].replace("-", " ")
                       .replace("_", " "))
    return out


def links_in(markdown: str, base: str) -> dict[str, str]:
    """Every link on a page: url -> link text ("" if none)."""
    out = {u: t.replace("-", " ") for u, t in _link_titles(markdown, base).items()}
    for u in _PDF_LINK.findall(markdown or ""):
        out.setdefault(urljoin(base, u), "")
    return {u.split("#")[0]: t for u, t in out.items()}


class Library:
    """The company's own documents, found and fetched cheapest first."""

    def __init__(self, slug: str, site: str, report_year: int | None, fc: FirecrawlClient,
                 skip_urls=()):
        self.slug, self.site, self.report_year, self.fc = slug, site, report_year, fc
        self.home = registered_domain(urlparse(site).netloc)
        self.pool: dict[str, str] = {}          # url -> link text
        self.mapped: set[str | None] = set()    # map searches done (None: plain map)
        self.used: set[str] = {_canonical(u) for u in skip_urls if u}
        self.tries: dict[str, int] = {}         # doc type -> documents tried
        self.out_of_credits = False
        self._load_discovery()

    # --- discovery ---------------------------------------------------------------------

    def _add(self, links: dict[str, str], own_page: bool = False) -> None:
        """Site URLs always; other hosts only for PDFs linked from the company's pages."""
        for url, title in links.items():
            url = _canonical(url)
            if not url:
                continue
            same = registered_domain(urlparse(url).netloc) == self.home
            if same or (own_page and is_pdf_url(url)):
                if title or url not in self.pool:
                    self.pool[url] = title

    def _load_discovery(self) -> None:
        path = CACHE_DIR / f"{self.slug}_discovery.json"
        if not path.exists():
            return
        d = json.loads(path.read_text(encoding="utf-8"))
        # Map results and links on the IR page the report search already found.
        self._add({c["url"]: "" for c in d.get("report_candidates") or [] if c.get("url")},
                  own_page=True)
        log.info("Documents: %d site URLs from the report search", len(self.pool))

    def _map(self, term: str | None) -> None:
        """A Firecrawl map (1 credit; cached by site and term)."""
        if term in self.mapped or self.out_of_credits:
            return
        self.mapped.add(term)
        path = CACHE_DIR / f"{self.slug}_map_{hashlib.sha1(f'{self.site}|{term}'.encode()).hexdigest()[:12]}.json"
        if path.exists():
            links = json.loads(path.read_text(encoding="utf-8"))
        else:
            try:
                links = self.fc.map(self.site, search=term, limit=MAP_LIMIT)
            except CreditBudgetExceeded as e:
                log.info("Documents: %s", e)
                self.out_of_credits = True
                return
            CACHE_DIR.mkdir(exist_ok=True)
            path.write_text(json.dumps(links), encoding="utf-8")
        self._add({l["url"]: l.get("title") or "" for l in links if l.get("url")})

    def candidates(self, doc_type: DocType) -> list[Candidate]:
        found = [classify(u, doc_type, t, self.report_year)
                 for u, t in self.pool.items() if u not in self.used]
        return sorted((c for c in found if c), key=lambda c: _rank(c, self.report_year),
                      reverse=True)

    def _best(self, dt_: DocType) -> Candidate | None:
        """The best unread candidate of a type: cached URL lists first, then a plain
        map, then a map search for the type (each map only once per company)."""
        if self.tries.get(dt_.key, 0) >= MAX_DOCS_PER_TYPE:
            return None
        cands = self.candidates(dt_)
        for term in (None, dt_.search):
            if cands:
                break
            self._map(term)
            cands = self.candidates(dt_)
        if self.out_of_credits:
            cands = [c for c in cands if c.is_pdf]      # PDFs are downloaded for free
        if not cands:
            return None
        self.used.add(cands[0].url)
        self.tries[dt_.key] = self.tries.get(dt_.key, 0) + 1
        return cands[0]

    def find(self, key: str, search: bool = False) -> Document | None:
        """The best document of one type, fetched; the next candidate if one is unusable.
        `search`: run the type's map search first even if cached URLs have candidates
        (the first document found was the wrong kind, e.g. a committee page, and the
        real report sits in a folder no cached list reaches; 1 credit)."""
        if search:
            self._map(DOC_TYPES[key].search)
        for _ in range(MAX_DOCS_PER_TYPE):
            c = self._best(DOC_TYPES[key])
            if c is None:
                return None
            doc = self.fetch(c)
            if doc:
                return doc
        return None

    def pick(self, gaps: list[str], n: int) -> list[Candidate]:
        """The best unread document for each of the most promising types, at most n.
        Cached URL lists first; a plain map, then a map search per type, only when
        a type has no candidate yet. A later-choice type is skipped when the documents
        already picked cover all its gaps (it gets its turn next round if they don't
        fill them)."""
        picked, covered = [], set()
        for dt_ in gap_types(gaps):
            if len(picked) >= n:
                break
            serves = {g for g in gaps if dt_.key in DP_DOC_TYPES.get(g, [])}
            if serves <= covered:
                continue
            c = self._best(dt_)
            if c:
                picked.append(c)
                covered |= serves
        return picked

    # --- fetching -------------------------------------------------------------------------

    def fetch(self, c: Candidate) -> Document | None:
        """PDFs are downloaded and converted locally; pages are scraped (1 credit). A URL
        that doesn't end in .pdf is tried as a download first: some are PDFs, and
        Firecrawl charges per page for those."""
        md_path = CACHE_DIR / f"{_stem(self.slug, c.url)}.md"
        pdf_path = md_path.with_suffix(".pdf")
        try:
            files_path = md_path.with_suffix(".files.json")
            if md_path.exists():
                pages = markdown_to_pages(md_path.read_text(encoding="utf-8"))
                kind, at = ("pdf" if pdf_path.exists() else "web"), _mtime(md_path)
                files = json.loads(files_path.read_text(encoding="utf-8")) \
                    if files_path.exists() else {}
            else:
                pages, kind, files = self._download(c, pdf_path)
                at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
                CACHE_DIR.mkdir(exist_ok=True)
                md_path.write_text(pages_to_markdown(pages), encoding="utf-8")
                if files:
                    files_path.write_text(json.dumps(files), encoding="utf-8")
        except CreditBudgetExceeded as e:
            log.info("Documents: %s", e)
            self.out_of_credits = True
            return None
        except (DownloadError, NeedsOCRError, httpx.HTTPError, OSError) as e:
            log.warning("Documents: %s unusable: %s", c.url, str(e)[:150])
            return None
        except PaymentRequiredError:
            raise
        except Exception as e:  # noqa: BLE001 - Firecrawl errors: one document must not stop the rest
            log.warning("Documents: %s failed: %s", c.url, str(e)[:150])
            return None
        if sum(len(p.text.strip()) for p in pages) < MIN_TEXT_CHARS:
            return None
        doc = Document(c.url, c.doc_type, kind, pages, c.year, at,
                       path=pdf_path if kind == "pdf" and pdf_path.exists() else None)
        if kind == "web":
            doc.links = links_in("\n".join(p.text for p in pages), c.url)
            for url, label in files.items():           # download buttons (page data)
                doc.links.setdefault(url, label)
            self._add(doc.links, own_page=True)       # step 3: follow its links
        log.info("Documents: read %s %s (%d page(s))", doc.source, c.url, len(pages))
        return doc

    def _download(self, c: Candidate, pdf_path) -> tuple[list[Page], str, dict[str, str]]:
        """(pages, kind, files): files are PDF addresses found in a web page's data."""
        body, ct = None, None
        if c.is_pdf:
            body, ct = download(c.url)
        else:
            try:
                body, ct = download(c.url)
            except (DownloadError, httpx.HTTPError):
                body = None
        if body is not None and looks_like_pdf(body, ct):
            pdf_path.write_bytes(body)
            pages = pdf_to_pages(pdf_path)
            check_not_scanned(pages)
            return pages, "pdf", {}
        if c.is_pdf:
            raise DownloadError(f"Expected a PDF from {c.url} but got {ct!r}")
        # The raw HTML from the plain download holds file addresses kept in the page's
        # data (download buttons); the readable text comes from Firecrawl.
        files = embedded_files(body.decode("utf-8", "replace")) if body else {}
        md = self.fc.scrape(c.url, formats=["markdown"])["markdown"]
        return [Page(1, md)], "web", files
