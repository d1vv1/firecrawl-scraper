"""Every data point for a list of companies, one row per value, with the exact place
each value came from.

    python -m extractor.datapoints data/golden_test_sample_5_per_segment_country_all.csv
        [--workers 3] [--only ID,ID] [--limit N] [--retry-failed] [--redo] [--no-docs]

Input: any CSV with company_id, company_name and (optional) segment, country, lei,
business_id, isin, annual_report_url, remuneration_report_url. Several rows per company
are fine (the golden sample has one row per golden value); each company is processed once.

For each company, in order of precedence (most exact first). In run order, the
annual-report pipeline (2) runs first (process_company), then collect() does the rest:
  1. the official APIs (from_apis): GLEIF, ESMA FIRDS + OpenFIGI (listing.py), the home
     register (NO, FI, UK) and SEC EDGAR;
  2. the annual-report pipeline (python -m extractor.batch): an ESEF/SEC/register filing
     or the website's report; revenue and total assets from XBRL tags or the report;
  3. one LLM pass over the same report for the remaining facts, each with a quote that
     is looked up in the report to find its page;
  4. executive pay per role (from_pay): a supplied URL, SEC exhibits, the remuneration
     report on the site, the annual report's remuneration section;
  5. document fallback: data points still missing are looked for in the company's
     other documents (governance and sustainability reports, "The share" and
     shareholder pages, legal notice, year-end report...; see documents.py), in
     rounds, at most --doc-credits Firecrawl credits per company.
See docs/pipeline_flow.html for the whole flow.

Output:
  <--out>.csv                  one row per company and data point, and per role and pay
                               field (17 columns, COLUMNS)
  output/datapoints/<id>.json  the same rows per company (re-runs skip done companies)
  output/golden_test_filled.csv  the input CSV with build_value filled in, when the
                               input is the golden sample

Where a value came from:
  source      who published it (Annual report (PDF), SEC EDGAR filing, Remuneration
              report (PDF), Share information (web page)...)
  endpoint    the exact URL: the API request, the filing, the PDF with #page=N, or the
              web page with a #:~:text= fragment that browsers scroll to
  method      API (register field), XBRL (tagged figure), PARSE (read from a filed
              document), SCRAPE (read from a web page), DERIVED (computed from other values)
  confidence  A exact (register field or XBRL tag); B read by the AI, quote found in
              the source; C read by the AI, quote not found verbatim (check it)
  note        the page and quote, the tag name, or why there is no value
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
import logging
import re
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import quote as urlquote, urlparse

import httpx
from firecrawl import PaymentRequiredError

from . import apis, edgar, listing, llm, pay
from .apis import Found
from .batch import FATAL, Company, _KeepAwake, _setup_logging, _worker_init, process_company
from .config import CACHE_DIR, OUTPUT_DIR, fold, load_settings
from .documents import DP_DOC_TYPES, Candidate, DocType, Document, Library
from .extract import full_value, full_value_quoted
from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from .pipeline import find_official_website, identify_lei
from .report_finder import extract_year, is_pdf_url
from .schemas import DataPointFacts, Holder, NumberFact, TextFact
from .scraper import Page, markdown_to_pages, pages_to_markdown
from .sections import DATAPOINT_TOPICS, Chunk, select_chunks, split_chunks
from .validate import quote_in_text
from .website import WebsiteNotFoundError

log = logging.getLogger("extractor.datapoints")

COLUMNS = ["company_id", "company_name", "segment", "country", "lei", "grain", "role_row",
           "data_point", "value", "unit", "period_end", "source", "endpoint", "method",
           "retrieved_at", "confidence", "note"]

# Company-grain data points in output order (protocol field in the comment). Names
# match the golden dataset's `field`. Role grain (R01-R11): pay.ROLE_POINTS.
DATA_POINTS = [
    "legal_name", "other_names",                        # C01
    "lei",                                              # C02
    "business_id",                                      # C03
    "cik",                                              # SEC registrants (golden dataset)
    "isin",                                             # C04
    "ticker", "exchange",                               # C05
    "exchange_segment",                                 # C06
    "listing_status", "listing_date",                   # C07
    "country_code", "head_office_city",                 # C08
    "website",                                          # C09
    "sector_code",                                      # C10
    "sub_sector",                                       # C11
    "revenue",                                          # C12
    "total_assets",                                     # C13
    "ebitda",                                           # C14
    "fiscal_year", "fiscal_year_end", "reporting_currency", "accounting_basis",   # C15
    "headcount", "fte",                                 # C16
    "shares_outstanding",                               # C17
    "share_price",                                      # C18
    "market_cap_band",                                  # derived from C17 x C18
    "largest_holders",                                  # C19
    "controlling_owner", "controlling_owner_name", "ownership_type", "pe_stake_5pct",   # C20
    "ultimate_parent",                                  # C21
    "revenue_by_segment", "staff_by_segment",           # C22
    "revenue_by_country", "staff_by_country",           # C22
    "pension_type", "benefits", "shareholding_requirement",   # C23
]
NAMES = DATA_POINTS
# Only an official API gives these (GLEIF, the registers, SEC EDGAR).
API_ONLY = {"lei", "sector_code"}
LISTED_ONLY = {"ticker", "isin", "exchange", "exchange_segment", "listing_date", "share_price",
               "market_cap_band", "cik"}
# Pay facts are only published by listed companies (remuneration reports).
LISTED_REPORTS_ONLY = {"pension_type", "benefits", "shareholding_requirement"}
# Market cap bands in EUR (Nasdaq Nordic's cap segments; confirm against the CDP band
# definition). Other currencies need a year-end EUR rate: an API step, not done here.
MARKET_CAP_BANDS_EUR = [(1_000_000_000, "large"), (150_000_000, "mid"), (0, "small")]

CONFIDENCE_RANK = {"A": 3, "B": 2, "C": 1, "": 0}
METHOD_RANK = {"API": 4, "XBRL": 4, "PARSE": 3, "SCRAPE": 2, "DERIVED": 1, "": 0}

DP_DIR = OUTPUT_DIR / "datapoints"
TOPIC_WORDS = 2_500                  # report words sent per topic (7 topics)
DOC_TOPIC_WORDS = 1_500              # words per needed topic from each fallback document
DOC_ROUNDS = 3                       # AI calls over fallback documents, at most
DOCS_PER_ROUND = 3                   # documents read per round
DEFAULT_DOC_CREDITS = 10             # maps and page scrapes; PDFs are downloaded for free
DEFAULT_PIPELINE_CREDITS = 6

OWNER_CATEGORY = {"private_equity": "private_equity", "family_or_individual": "family",
                  "state": "state", "listed_company": "corporate", "other_company": "corporate",
                  "foundation": "foundation", "institutional_investor": "institutional",
                  "employees": "employees", "other": "other"}
OWNERSHIP_TYPE = {"private_equity": "pe_backed", "family_or_individual": "family_owned",
                  "state": "state_owned", "listed_company": "subsidiary",
                  "other_company": "subsidiary", "foundation": "foundation_owned",
                  "institutional_investor": "other", "employees": "employee_owned",
                  "other": "other"}


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


# --- input ----------------------------------------------------------------------------

@dataclass
class Target:
    company: Company
    business_id: str | None = None
    isin: str | None = None          # optional: finds the LEI when the name doesn't
    # Documents found by hand, read first in the pay step (no search, no year check):
    # for reports no search reaches (Equinor's FY2025 report on a CDN under a hash).
    remuneration_report_url: str | None = None
    annual_report_url: str | None = None


def read_targets(path: Path) -> list[Target]:
    """One Target per company_id, in first-seen order. The country "(none)" (and any
    value that isn't a 2-letter code) means unknown."""
    text = path.read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t")
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    low = {h: (h or "").strip().lower() for h in rows[0]} if rows else {}

    def col(*names):
        return next((h for h, l in low.items() if l in names), None)
    c_id, c_name = col("company_id", "id"), col("company_name", "name", "legal_name")
    c_country, c_seg = col("country", "country_code"), col("segment")
    c_lei, c_bid = col("lei"), col("business_id", "registration_id", "org_number")
    c_rem, c_ar = col("remuneration_report_url"), col("annual_report_url")
    c_isin = col("isin")
    if not c_id or not c_name:
        raise ValueError(f"{path} needs company_id and company_name columns")
    out: dict[str, Target] = {}
    for r in rows:
        cid = (r.get(c_id) or "").strip()
        if not cid:
            continue
        country = (r.get(c_country) or "").strip().upper() if c_country else ""
        lei = (r.get(c_lei) or "").strip().upper() if c_lei else ""
        bid = (r.get(c_bid) or "").strip() if c_bid else ""
        t = out.get(cid)
        if t is None:
            out[cid] = t = Target(Company(cid, (r.get(c_name) or "").strip(),
                                          country if re.fullmatch(r"[A-Z]{2}", country) else None,
                                          (r.get(c_seg) or "").strip() or None if c_seg else None,
                                          lei if len(lei) == 20 else None))
        if bid and not t.business_id:
            t.business_id = bid
        isin = (r.get(c_isin) or "").strip().upper() if c_isin else ""
        if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin) and not t.isin:
            t.isin = isin
        for attr, column in (("remuneration_report_url", c_rem), ("annual_report_url", c_ar)):
            url = (r.get(column) or "").strip() if column else ""
            if url.startswith("http") and not getattr(t, attr):
                setattr(t, attr, url)
        if len(lei) == 20 and not t.company.lei:
            t.company.lei = lei
    return list(out.values())


# --- formatting -------------------------------------------------------------------------

def fmt_number(v: float | int | None) -> str:
    if v is None:
        return ""
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.6f}".rstrip("0").rstrip(".")


def clip(text: str | None, n: int = 160) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return text if len(text) <= n else text[:n - 1] + "…"


def text_fragment(url: str, quote: str | None) -> str:
    """url#:~:text=... so a browser scrolls to the quote (Chrome, Edge, Safari). Only
    for running text: table rows ("Revenue|3|1,234") never match the rendered page."""
    if not quote or "|" in quote:
        return url
    words = re.sub(r"\s+", " ", quote).strip().split(" ")
    if len(words) < 3:
        return url
    start = " ".join(words[:5])
    end = " ".join(words[-3:]) if len(words) > 8 else None
    frag = urlquote(start, safe="") + (f",{urlquote(end, safe='')}" if end else "")
    return f"{url.split('#')[0]}#:~:text={frag}"


# --- where a quote is ---------------------------------------------------------------------

@dataclass
class Located:
    page: int | None        # page of the document (PDF page) the quote is on
    verified: bool          # the quote was found in the text


def locate(quote: str | None, chunk_id: int | None, chunks: dict[int, Chunk],
           pages: list[Page]) -> Located:
    """Find the page a quote is on: first among the pages of its chunk, then anywhere
    in the document (the model sometimes gives the wrong chunk id)."""
    if not quote:
        return Located(None, False)
    chunk = chunks.get(chunk_id) if chunk_id is not None else None
    by_number = {p.number: p for p in pages}
    candidates = [by_number[n] for n in (chunk.pages if chunk else []) if n in by_number]
    for mode in ("exact", "loose"):
        for group in (candidates, pages):
            for p in group:
                if quote_in_text(quote, p.text) == mode:
                    return Located(p.number, True)
    # The quote spans a page break: it is in the chunk, though on no single page.
    if chunk and quote_in_text(quote, chunk.text):
        return Located(chunk.pages[0] if chunk.pages else None, True)
    return Located(chunk.pages[0] if chunk and chunk.pages else None, False)


@dataclass
class Origin:
    """A document the AI read: a filed report, a PDF, or a web page."""
    kind: str               # pdf / html / xhtml / registry / web
    url: str
    source: str             # e.g. "Annual report (PDF)"
    method: str             # PARSE or SCRAPE
    retrieved_at: str
    pages: list[Page]
    chunks: dict[int, Chunk]
    page_urls: dict[int, str] | None = None     # web: chunk id -> page URL
    date: str = ""          # the document's date, for fallback documents ("2025")

    def place(self, quote: str | None, chunk_id: int | None) -> tuple["Origin", str, str, str]:
        return (self, *self.where(quote, chunk_id))

    def where(self, quote: str | None, chunk_id: int | None) -> tuple[str, str, str]:
        """(endpoint, confidence, location note) for a value with this quote."""
        if self.kind == "web":
            url = (self.page_urls or {}).get(chunk_id, self.url)
            chunk = self.chunks.get(chunk_id)
            ok = bool(quote and chunk and quote_in_text(quote, chunk.text))
            if not ok and quote:          # wrong chunk id: look in every page
                for cid, ch in self.chunks.items():
                    if quote_in_text(quote, ch.text):
                        url, ok = (self.page_urls or {}).get(cid, url), True
                        break
            return (text_fragment(url, quote) if ok else url, "B" if ok else "C",
                    f'web page: "{clip(quote)}"' + ("" if ok else " (quote not found verbatim)"))
        loc = locate(quote, chunk_id, self.chunks, self.pages)
        conf = "B" if loc.verified else "C"
        tail = "" if loc.verified else " (quote not found verbatim)"
        if self.kind == "pdf":
            page = loc.page
            return (f"{self.url}#page={page}" if page else self.url, conf,
                    f'PDF page {page}: "{clip(quote)}"{tail}' if page else f'"{clip(quote)}"{tail}')
        # Filed XHTML / HTML report text has no fixed pages: link to the quote itself.
        return (text_fragment(self.url, quote) if loc.verified else self.url, conf,
                f'report text: "{clip(quote)}"{tail}')


@dataclass
class Bundle:
    """Several documents read in one AI call. Chunk ids are unique across them, so a
    value is placed in the document its chunk came from; if its quote isn't there (the
    model gave the wrong chunk id), in whichever document has it."""
    origins: list[Origin]

    def place(self, quote: str | None, chunk_id: int | None) -> tuple[Origin, str, str, str]:
        first = next((o for o in self.origins if chunk_id in o.chunks), self.origins[0])
        placed = first.place(quote, chunk_id)
        if placed[2] == "B" or not quote:
            return placed
        for o in self.origins:
            if o is not first:
                other = o.place(quote, None)
                if other[2] == "B":
                    return other
        return placed


# --- 1. the annual-report pipeline's result -----------------------------------------------

FILING_SOURCE = {"esef": "ESEF filing (filings.xbrl.org)", "edgar": "SEC EDGAR filing",
                 "registry": "Company register filing"}
REGISTRY_NAMES = {"brreg": "Brønnøysund accounts register", "virk": "Danish Business Authority (virk.dk)",
                  "companies_house": "Companies House filing"}


def report_origin(result: dict) -> Origin | None:
    """The document the pipeline read, from its cached page-tagged markdown."""
    md_name = ((result.get("debug") or {}).get("markdown_file"))
    if not md_name or not (CACHE_DIR / md_name).exists():
        return None
    pages = markdown_to_pages((CACHE_DIR / md_name).read_text(encoding="utf-8"))
    chunks = {c.id: c for c in split_chunks(pages)}
    kind = result.get("report_type") or "pdf"
    filing = result.get("filing") or {}
    if result.get("report_url") == filing.get("report_url"):
        source = (REGISTRY_NAMES.get(filing.get("registry"), FILING_SOURCE.get(filing.get("type"), "Filing"))
                  + (f" {filing.get('form')}" if filing.get("type") == "edgar" else ""))
    else:
        source = "Annual report (PDF)" if kind == "pdf" else "Annual report (web page)"
    return Origin(kind, result["report_url"], source, "PARSE", result.get("extracted_at") or _now(),
                  pages, chunks)


def _money_found(name: str, m: dict, result: dict, origin: Origin | None) -> Found | None:
    if not m or m.get("value") is None:
        return None
    filing = result.get("filing") or {}
    value = m.get("value_full") if m.get("value_full") is not None else full_value(m["value"], m.get("unit"))
    at = result.get("extracted_at") or ""
    period = result.get("period_end_date") or ""
    scope = f"{m.get('scope')} figures" if m.get("scope") and m.get("scope") != "consolidated" else ""
    if m.get("method") == "xbrl_tag":
        if filing.get("type") == "edgar":
            endpoint, source = edgar.FACTS_URL.format(cik=int(filing["cik"])), "SEC EDGAR XBRL"
        else:
            endpoint = filing.get("report_url") or result.get("report_url")
            source = (REGISTRY_NAMES.get(filing.get("registry"), "Company register") + " (XBRL)"
                      if filing.get("type") == "registry" else "ESEF filing (filings.xbrl.org)")
        note = f"tag {m.get('xbrl_concept')}; {clip(m.get('quote'), 120)}"
        if filing.get("viewer_url"):
            note += f"; viewer {filing['viewer_url']}"
        return Found(name, value, unit=m.get("currency") or "", period_end=period, source=source,
                     endpoint=endpoint, method="XBRL", confidence="A",
                     note="; ".join(x for x in (note, scope) if x), retrieved_at=at)
    if origin is None:
        return Found(name, value, unit=m.get("currency") or "", period_end=period,
                     source="Annual report", endpoint=result.get("report_url") or "", method="PARSE",
                     confidence="C", note=f'"{clip(m.get("quote"))}"', retrieved_at=at)
    endpoint, conf, where = origin.where(m.get("quote"), m.get("chunk_id"))
    printed = f"printed {fmt_number(m['value'])} {m.get('unit')} ({m.get('label_in_report')})"
    return Found(name, value, unit=m.get("currency") or "", period_end=period, source=origin.source,
                 endpoint=endpoint, method="PARSE", confidence=conf,
                 note="; ".join(x for x in (where, printed, scope) if x), retrieved_at=at)


# Which line is "revenue" when a filing tags two (CTT: revenue from contracts with
# customers 1,129m; revenue and operating income 1,292m). "ifrs": the IFRS revenue line,
# the broader one in the note; "broad": the broader line, IFRS revenue in the note.
REVENUE_RULE = "ifrs"


def from_result(result: dict, origin: Origin | None) -> list[Found]:
    """The figures and identifiers the pipeline found."""
    out: list[Found] = []
    for name in ("revenue", "total_assets"):
        f = _money_found(name, result.get(name) or {}, result, origin)
        if f:
            out.append(f)
    broad = (result.get("filing") or {}).get("revenue_and_operating_income")
    rev = next((f for f in out if f.data_point == "revenue"), None)
    if rev and broad is not None and _norm(broad) != _norm(rev.value):
        if REVENUE_RULE == "broad":
            rev.note = (f"revenue and operating income (ifrs-full:RevenueAndOperatingIncome); "
                        f"IFRS revenue {fmt_number(rev.value)} {rev.unit}")
            rev.value = broad
        else:
            rev.note += (f"; the filing also tags revenue and operating income "
                         f"{fmt_number(broad)} {rev.unit} (ifrs-full:RevenueAndOperatingIncome)")
    period = result.get("period_end_date") or ""
    at = result.get("extracted_at") or ""
    money = next((f for f in out), None)
    if result.get("fiscal_year") and money:
        out.append(Found("fiscal_year", result["fiscal_year"], period_end=period, source=money.source,
                         endpoint=money.endpoint.split("#")[0], method=money.method,
                         confidence=money.confidence, note="the year the figures are for",
                         retrieved_at=at))
    if result.get("period_end_date") and money:
        out.append(Found("fiscal_year_end", result["period_end_date"], period_end=period,
                         source=money.source, endpoint=money.endpoint.split("#")[0],
                         method=money.method, confidence=money.confidence,
                         note="period end of the figures", retrieved_at=at))
    if money and money.unit:
        out.append(Found("reporting_currency", money.unit, period_end=period, source=money.source,
                         endpoint=money.endpoint, method=money.method, confidence=money.confidence,
                         note=f"currency of {money.data_point}", retrieved_at=at))
    filing = result.get("filing") or {}
    if filing.get("employees_in_filing") is not None:
        out.append(Found("headcount", filing["employees_in_filing"], unit="employees",
                         period_end=filing.get("period_end") or period,
                         source=REGISTRY_NAMES.get(filing.get("registry"), "Company register"),
                         endpoint=filing.get("report_url") or "", method="XBRL"
                         if filing.get("registry") != "brreg" else "API", confidence="A",
                         note="employees stated in the filed accounts", retrieved_at=at))
    if filing.get("cik"):
        out.append(Found("cik", str(filing["cik"]), source="SEC EDGAR",
                         endpoint=edgar.SUBMISSIONS_URL.format(cik=int(filing["cik"])), method="API",
                         confidence="A", retrieved_at=at))
    return out


# --- 2. the AI pass over the report (and over fallback documents) ------------------------------

def _user_prompt(name: str, url: str, chunks: list[Chunk], what: str,
                 wanted: list[str] | None = None) -> str:
    body = "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)
    only = (f"Only these facts are needed: {', '.join(wanted)}. Set every other fact to "
            f"null (empty list / empty items).\n\n" if wanted else "")
    return (f"Company legal name: {name}\nSource: {url}\n\n{only}"
            f"Excerpts from {what} (tables are in markdown):\n\n{body}")


def ask(name: str, url: str, chunks: list[Chunk], what: str, cache_key: str,
        wanted: list[str] | None = None) -> DataPointFacts:
    """The data-point LLM call, cached by the document, the chunks it was given and the
    facts asked for (`wanted`: DataPointFacts fields; None asks for all)."""
    path = CACHE_DIR / f"{cache_key}_datapoints_llm.json"
    ids = [c.id for c in chunks]
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if (saved.get("chunk_ids") == ids and saved.get("wanted") == wanted
                and saved.get("prompt") == llm.load_prompt("datapoints_system")):
            return DataPointFacts.model_validate(saved["facts"])
    facts = llm.call_llm(llm.load_prompt("datapoints_system"),
                         _user_prompt(name, url, chunks, what, wanted), DataPointFacts)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"chunk_ids": ids, "wanted": wanted,
                                "prompt": llm.load_prompt("datapoints_system"),
                                "model": llm.model_name(), "facts": facts.model_dump()},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return facts


def report_chunks(origin: Origin) -> list[Chunk]:
    picked: dict[int, Chunk] = {}
    for topic in DATAPOINT_TOPICS:
        for c in select_chunks(list(origin.chunks.values()), topic, TOPIC_WORDS):
            picked[c.id] = c
    return [picked[i] for i in sorted(picked)]


def _breakdown(b) -> str:
    return "; ".join(f"{getattr(i, 'country', None) or i.segment}: {fmt_number(i.value)}"
                     for i in b.items)


def from_facts(facts: DataPointFacts, origin: Origin | Bundle) -> list[Found]:
    """The AI's facts as Found values, each placed by its quote (in its document, when
    several documents were read together)."""
    out: list[Found] = []

    def add(name: str, value, fact, unit: str = "", period: str = "", extra: str = ""):
        if value in (None, "", []) or not getattr(fact, "quote", None):
            return                      # no quote, no value: the prompt demands one
        doc, endpoint, conf, where = origin.place(fact.quote, fact.chunk_id)
        dated = f"document dated {doc.date}" if doc.date else ""
        out.append(Found(name, value, unit=unit, period_end=period or "", source=doc.source,
                         endpoint=endpoint, method=doc.method, confidence=conf,
                         note="; ".join(x for x in (extra, where, dated) if x),
                         retrieved_at=doc.retrieved_at))

    for name in ("revenue", "total_assets"):
        n: NumberFact = getattr(facts, name)
        if n.value is not None and n.unit:
            add(name, full_value_quoted(n.value, n.unit, n.quote), n, unit=n.currency or "",
                period=n.period_end,
                extra=f"printed {fmt_number(n.value)} {n.unit}")
    e = facts.ebitda
    if e.value is not None and e.unit and e.measure:
        what = e.measure.replace("_", " ") + (" (company-defined)" if e.company_defined else "")
        add("ebitda", full_value_quoted(e.value, e.unit, e.quote), e, unit=e.currency or "",
            extra=f"{what}; printed {fmt_number(e.value)} {e.unit}"
                  + (f" ({e.label_in_report})" if e.label_in_report else ""))
    for name in ("fte", "headcount"):
        n = getattr(facts, name)
        add(name, n.value, n, unit="employees", period=n.period_end)
    n = facts.shares_outstanding
    if n.value is not None:
        add("shares_outstanding", full_value_quoted(n.value, n.unit or "units", n.quote), n,
            unit="shares",
            period=n.period_end)
    p = facts.share_price
    if p.value is not None and p.currency:
        add("share_price", p.value, p, unit=p.currency, period=p.date or "",
            extra=f"closing price {p.date}" if p.date else "closing price at year end")
    for name in ("legal_name", "business_id", "other_names", "head_office_city", "ticker",
                 "isin", "exchange", "exchange_segment", "listing_date", "sub_sector",
                 "fiscal_year_end", "reporting_currency", "accounting_basis", "pension_type",
                 "benefits", "shareholding_requirement"):
        t: TextFact = getattr(facts, name)
        add(name, t.value, t)
    site = website_domain(facts.website.value)
    if site:
        add("website", site, facts.website)
    cc = (facts.country_code.value or "").strip().upper()
    if re.fullmatch(r"[A-Z]{2}", cc):
        add("country_code", cc, facts.country_code)
    if facts.ultimate_parent.value:
        add("ultimate_parent", facts.ultimate_parent.value, facts.ultimate_parent,
            extra="top company of the group")
    if facts.is_listed.value in ("listed", "unlisted"):
        add("listing_status", facts.is_listed.value, facts.is_listed)

    owner: Holder = facts.controlling_owner
    if owner.name:
        stake = f"{fmt_number(owner.stake_pct)}%" if owner.stake_pct is not None else ""
        add("controlling_owner_name", owner.name, owner, extra=" ".join(
            x for x in (owner.holder_type or "", stake) if x))
        if owner.holder_type:
            add("controlling_owner", OWNER_CATEGORY[owner.holder_type], owner, extra=owner.name)
            add("ownership_type", OWNERSHIP_TYPE[owner.holder_type], owner,
                extra=f"derived from the controlling owner ({owner.name})")
            if owner.holder_type in ("listed_company", "other_company") and (owner.stake_pct or 0) > 50:
                add("ultimate_parent", owner.name, owner, extra="majority owner (immediate parent)")
    elif owner.quote:
        add("controlling_owner", "none", owner, extra="no shareholder with 20% of the votes")
        add("ownership_type", "widely_held", owner, extra="no shareholder with 20% of the votes")

    holders = [h for h in facts.major_shareholders if h.name and h.quote]
    if holders:
        add("largest_holders", "; ".join(
            f"{h.name} {fmt_number(h.stake_pct)}%" if h.stake_pct is not None else h.name
            for h in holders), holders[0], extra=f"{len(holders)} holder(s) as listed")
    big = [h for h in holders if h.stake_pct is not None and h.stake_pct >= 5]
    pe = [h for h in big + ([owner] if owner.name and owner.quote else [])
          if h.holder_type == "private_equity" and (h.stake_pct is None or h.stake_pct >= 5)]
    if pe:
        h = pe[0]
        add("pe_stake_5pct", "yes", h, extra=f"{h.name}"
            + (f" {fmt_number(h.stake_pct)}%" if h.stake_pct is not None else ""))
    elif big:
        add("pe_stake_5pct", "no", big[0], extra="no private equity among the holders of 5% or more")

    for name in ("revenue_by_country", "staff_by_country", "revenue_by_segment", "staff_by_segment"):
        b = getattr(facts, name)
        if b.items:
            unit = " ".join(x for x in (b.currency, b.unit if b.unit != "units" else "") if x) \
                or ("employees" if name.startswith("staff") else "")
            add(name, _breakdown(b), b, unit=unit, extra=b.basis or "")
    return out


def website_domain(text: str | None) -> str:
    """'https://www.Yubico.com/investors' -> 'yubico.com'."""
    m = re.search(r"(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)", (text or "").lower())
    return m.group(1) if m else ""


# --- 3. document fallback: the company's other documents ------------------------------------

# Data points the AI pass can answer -> the DataPointFacts field asked for, and the
# report topic (sections.DATAPOINT_TOPICS) whose chunks are sent for it.
FACT_FIELD = {"controlling_owner_name": "controlling_owner", "ownership_type": "controlling_owner",
              "pe_stake_5pct": "major_shareholders", "largest_holders": "major_shareholders",
              "listing_status": "is_listed"}
FACT_TOPIC = {
    "controlling_owner": "ownership", "controlling_owner_name": "ownership",
    "ownership_type": "ownership", "pe_stake_5pct": "ownership", "ultimate_parent": "ownership",
    "largest_holders": "ownership",
    "isin": "ownership", "ticker": "ownership", "exchange": "ownership",
    "exchange_segment": "ownership", "listing_date": "ownership", "listing_status": "ownership",
    "shares_outstanding": "ownership", "share_price": "keyfigures",
    "fte": "employees", "headcount": "employees", "staff_by_country": "employees",
    "staff_by_segment": "segments", "revenue_by_segment": "segments",
    "pension_type": "remuneration", "benefits": "remuneration",
    "shareholding_requirement": "remuneration",
    "revenue_by_country": "geography", "revenue": "financials", "total_assets": "financials",
    "ebitda": "keyfigures", "reporting_currency": "financials", "fiscal_year_end": "keyfigures",
    "accounting_basis": "keyfigures", "legal_name": "profile", "website": "profile",
    "business_id": "profile", "country_code": "profile", "head_office_city": "profile",
    "other_names": "profile", "sub_sector": "profile"}
assert set(FACT_TOPIC) == set(DP_DOC_TYPES)


def gap_list(chosen: dict[str, Found]) -> list[str]:
    """The data points still empty that a document can fill (not those of listed
    companies when the company is known to be unlisted)."""
    listed = chosen.get("listing_status")
    unlisted = bool(listed and listed.value == "unlisted")
    return [n for n in NAMES if n not in chosen and n in DP_DOC_TYPES
            and not (unlisted and (n in LISTED_ONLY or n in LISTED_REPORTS_ONLY))]


def wanted_fields(gaps: list[str]) -> list[str]:
    return sorted({FACT_FIELD.get(g, g) for g in gaps})


def doc_origin(doc: Document, first_id: int) -> Origin:
    """A fallback document as an Origin, its chunk ids starting at first_id."""
    chunks = {first_id + i: Chunk(first_id + i, c.text, c.pages)
              for i, c in enumerate(split_chunks(doc.pages))}
    date = str(doc.year) if doc.year else ""
    if doc.kind == "pdf":
        return Origin("pdf", doc.url, doc.source, "PARSE", doc.retrieved_at, doc.pages, chunks,
                      date=date)
    return Origin("web", doc.url, doc.source, "SCRAPE", doc.retrieved_at, doc.pages, chunks,
                  {cid: doc.url for cid in chunks}, date=date)


def doc_chunks(origins: list[Origin], gaps: list[str]) -> list[Chunk]:
    """Only the parts relevant to the gaps: a short document whole, of a long one the
    best chunks per needed topic."""
    topics = sorted({FACT_TOPIC[g] for g in gaps})
    picked: dict[int, Chunk] = {}
    for o in origins:
        chunks = list(o.chunks.values())
        if sum(c.words for c in chunks) <= DOC_TOPIC_WORDS:
            picked |= {c.id: c for c in chunks}
            continue
        for topic in topics:
            picked |= {c.id: c for c in select_chunks(chunks, topic, DOC_TOPIC_WORDS)}
    return [picked[i] for i in sorted(picked)]


def from_documents(name: str, slug: str, site: str, gaps: list[str], lib: Library,
                   fc: FirecrawlClient) -> tuple[list[Found], list[str]]:
    """Rounds of: pick the most promising documents for the gaps, read them, ask the AI
    only for the gaps; stop when the gaps are filled, nothing is left to read, or after
    DOC_ROUNDS. Returns the values and the documents read (for "not found in")."""
    values: list[Found] = []
    read: list[str] = []
    next_id = 0
    for _ in range(DOC_ROUNDS):
        if not gaps:
            break
        origins = []
        for cand in lib.pick(gaps, DOCS_PER_ROUND):
            doc = lib.fetch(cand)
            if doc:
                origins.append(doc_origin(doc, next_id))
                next_id += len(origins[-1].chunks)
        if not origins:
            if lib.out_of_credits:
                break
            continue                     # every pick was unusable: try the next ones
        read += [o.source for o in origins]
        chunks = doc_chunks(origins, gaps)
        if not chunks:
            continue
        wanted = wanted_fields(gaps)
        log.info("Documents: asking the AI about %d chunk(s) of %d document(s) for: %s",
                 len(chunks), len(origins), ", ".join(gaps))
        key = hashlib.sha1("|".join(o.url for o in origins).encode()).hexdigest()[:12]
        facts = ask(name, origins[0].url if len(origins) == 1 else site, chunks,
                    "the company's documents: " + "; ".join(f"{o.source} {o.url}" for o in origins),
                    f"{slug}_docs_{key}", wanted)
        got = [f for f in from_facts(facts, Bundle(origins)) if f.data_point in gaps]
        for f in got:
            year_check(f, lib.report_year)
        values += got
        gaps = [g for g in gaps if g not in {f.data_point for f in got}]
    log.info("Documents: %d value(s) from %d document(s), %d Firecrawl credit(s)",
             len(values), len(read), fc.credits.total)
    return values, read


# --- 4. executive pay, role grain -------------------------------------------------------------

AR_PAY_WORDS = 8_000             # words of the annual report's remuneration section


def _pay_chunks(origin: Origin, words: int) -> list[Chunk]:
    chunks = list(origin.chunks.values())
    if sum(c.words for c in chunks) <= words:
        return chunks
    return select_chunks(chunks, "remuneration", words)


def fiscal_end_year(text: str | None) -> int | None:
    """The year a fiscal year ends in: '2025' -> 2025, '2025/26' and '2025-2026' -> 2026."""
    m = re.search(r"(20\d{2})(?:\s*[/-]\s*(\d{4}|\d{2}))?", text or "")
    if not m:
        return None
    if not m.group(2):
        return int(m.group(1))
    end = m.group(2)
    return int(end) if len(end) == 4 else int(m.group(1)[:2] + end)


# Where the directors' remuneration report is a statutory part of the annual report.
AR_PAY_FIRST = {"GB", "IE"}


def sec_doc(slug: str, url: str, label: str, year: int | None) -> Document | None:
    """An SEC document (a 20-F exhibit, a proxy statement) as page-like text, cached.
    The SEC wants its own User-Agent, so it is fetched through edgar, not Firecrawl."""
    from .xhtml_text import html_to_text, text_to_pages
    path = CACHE_DIR / f"{slug}_sec_{hashlib.sha1(url.encode()).hexdigest()[:16]}.md"
    try:
        if path.exists():
            pages = markdown_to_pages(path.read_text(encoding="utf-8"))
        else:
            pages = text_to_pages(html_to_text(edgar._get(url).text))
            CACHE_DIR.mkdir(exist_ok=True)
            path.write_text(pages_to_markdown(pages), encoding="utf-8")
    except (httpx.HTTPError, edgar.SecContactMissing) as e:
        log.warning("SEC document %s unreadable: %s", url, str(e)[:150])
        return None
    return Document(url, DocType("sec", label, "", ()), "web", pages, year, _now())


def supplied_doc(slug: str, url: str, label: str, lib: Library | None) -> Document | None:
    """A document given in the input (remuneration_report_url / annual_report_url),
    fetched like any other: a PDF is downloaded and converted (no credits)."""
    lib = lib or Library(slug, f"{urlparse(url).scheme}://{urlparse(url).netloc}", None, None)
    return lib.fetch(Candidate(url, DocType("supplied", label, "", ()), 9, extract_year(url),
                               is_pdf_url(url), 0))


def from_pay(name: str, slug: str, lib: Library | None, report: Origin | None,
             report_key: str, period_end: str, country: str | None = None,
             report_year: int | None = None, supplied: tuple = (),
             cik: int | None = None) -> tuple[list[Found], list[Found], list[str]]:
    """Role rows and the company-level pay terms, from the remuneration report (or the
    annual report's remuneration section), plus the remuneration policy for target and
    maximum percentages the report lacks. Returns (role rows, company values, sources)."""
    read: list[str] = []

    def sources():
        """Up to two remuneration documents, then the annual report's section. The
        second one comes from the first's links (a governance page linking the PDF) or
        from a map search for the type (Jumbo's report sits in an AGM folder)."""
        for url, label in supplied:
            doc = supplied_doc(slug, url, label, lib)
            if doc is None:
                log.warning("Pay: the supplied %s %s could not be read", label.lower(), url)
                continue
            o = doc_origin(doc, 0)
            yield (o, _pay_chunks(o, pay.PAY_WORDS), f"the company's {label.lower()}",
                   f"{slug}_pay_{hashlib.sha1(doc.url.encode()).hexdigest()[:12]}", True)
        if cik:
            # SEC filings: free, no bot checks (a 20-F attaches the home-country report)
            try:
                found = edgar.pay_documents(int(cik))
            except (httpx.HTTPError, edgar.SecContactMissing) as e:
                log.warning("SEC pay documents: %s", str(e)[:150])
                found = []
            for url, label in found:
                doc = sec_doc(slug, url, label, report_year)
                if doc:
                    o = doc_origin(doc, 0)
                    yield (o, _pay_chunks(o, pay.PAY_WORDS), f"the company's {label}",
                           f"{slug}_pay_{hashlib.sha1(url.encode()).hexdigest()[:12]}", False)
        ar = ((report, _pay_chunks(report, AR_PAY_WORDS),
               "the remuneration section of the company's annual report", report_key, False)
              if report else None)
        if ar and country in AR_PAY_FIRST:
            yield ar
        for attempt in range(2 if lib else 0):
            if attempt == 1:
                # before searching again: open the site's report downloads page, whose
                # files (also those behind download buttons) join the URL pool
                lib.find("report_hub")
            doc = lib.find("remuneration", search=attempt > 0)
            if doc is None:
                continue
            o = doc_origin(doc, 0)
            yield (o, _pay_chunks(o, pay.PAY_WORDS), "the company's remuneration report",
                   f"{slug}_pay_{hashlib.sha1(doc.url.encode()).hexdigest()[:12]}", False)
        if ar and country not in AR_PAY_FIRST:
            yield ar

    facts = origin = None
    for o, chunks, what, key, given in sources():
        if not chunks:
            continue
        log.info("Pay: asking the AI about %d chunk(s) of %s", len(chunks), o.source)
        f = pay.ask_pay(name, o.url, chunks, what, key)
        read.append(o.source)
        year = fiscal_end_year(f.fiscal_year)
        if year and report_year and year < report_year and not given:
            # Shell: an investor-roadshow deck with the previous year's outcomes; Equinor:
            # the FY2024 remuneration report when the annual report is FY2025
            log.info("Pay: %s gives FY%s pay, the report is FY%s; skipped", o.url, year,
                     report_year)
            continue
        if pay.has_pay(f):
            facts, origin = f, o
            break
        log.info("Pay: no executive pay figures in %s", o.url)
    if facts is None:
        return [], [], read
    policy = policy_origin = None
    if lib and pay.needs_policy(facts):
        pdoc = lib.find("remuneration_policy")
        if pdoc:
            policy_origin = doc_origin(pdoc, 0)
            chunks = _pay_chunks(policy_origin, pay.PAY_WORDS)
            if chunks:
                policy = pay.ask_pay(name, pdoc.url, chunks, "the company's remuneration policy",
                                     f"{slug}_pay_{hashlib.sha1(pdoc.url.encode()).hexdigest()[:12]}")
                read.append(policy_origin.source)
    roles = pay.role_found(facts, origin, policy, policy_origin, period_end)
    roles += _aggregates_from_report(name, facts, origin, report, report_key, period_end, read)
    terms = pay.company_terms(facts, origin)
    if policy:
        terms += pay.company_terms(policy, policy_origin)
    return roles, terms, read


def _aggregates_from_report(name: str, facts, origin: Origin, report: Origin | None,
                            report_key: str, period_end: str, read: list[str]) -> list[Found]:
    """Swedish and Finnish remuneration reports cover the CEO only; the total for the
    other executives is in the annual report (Volvo: 'Övriga medlemmar i
    koncernledningen'). Add the annual report's aggregate executive rows that the
    remuneration report lacks. Only aggregates: the CEO would otherwise appear twice
    under two spellings of the title."""
    if report is None or origin is report:
        return []
    chunks = _pay_chunks(report, AR_PAY_WORDS)
    if not chunks:
        return []
    ar = pay.ask_pay(name, report.url, chunks,
                     "the remuneration section of the company's annual report", report_key)
    have = {pay._norm_title(r.role_title) for r in facts.roles}
    extra = [r for r in ar.roles
             if r.executive and r.is_aggregate and pay._norm_title(r.role_title) not in have]
    more = ar.model_copy(update={"roles": extra})
    if not extra or not pay.has_pay(more):
        return []
    read.append(report.source)
    log.info("Pay: %d aggregate role(s) added from %s", len(extra), report.source)
    return pay.role_found(more, report, period_end=period_end)


def no_roles(why: str) -> list[Found]:
    """The one role row of a company with no pay disclosure found."""
    return [Found("role_disclosure", None, note=why, grain="role")]


# Figures that change every year: from a fallback document they must be for the
# report's fiscal year (a web page can hold an old year's figure).
YEARLY = {"revenue", "total_assets", "ebitda", "revenue_by_segment", "staff_by_segment",
          "revenue_by_country", "staff_by_country", "headcount", "fte", "shares_outstanding",
          "share_price"}


def year_check(f: Found, report_year: int | None) -> None:
    """Grade C a yearly figure whose document isn't dated the report's year or later."""
    if f.data_point not in YEARLY or not report_year:
        return
    dated = re.search(r"document dated (\d{4})", f.note)
    period = re.match(r"(\d{4})", f.period_end or "")
    year = int(period.group(1)) if period else int(dated.group(1)) if dated else None
    if year is None or year < report_year:
        f.confidence = "C"
        f.note += (f"; check the year: the report is FY{report_year}, this document is "
                   + (f"from {year}" if year else "undated"))


# Words that don't tell two companies apart: legal forms and generic name parts.
_NAME_NOISE = {"ab", "ag", "as", "asa", "nv", "bv", "sa", "se", "spa", "plc", "ltd", "limited",
               "oyj", "oy", "abp", "gmbh", "kgaa", "inc", "corp", "corporation", "llc", "publ",
               "aktiengesellschaft", "aktiebolag", "aktiebolaget", "allmennaksjeselskap",
               "aksjeselskap", "osakeyhtio", "sgps", "sarl", "srl", "holding", "holdings", "group",
               "groupe", "gruppe", "gruppo", "grupo", "company", "the", "and", "international"}


def name_core(name: str | None) -> frozenset[str]:
    """The distinctive words of a company name: 'Siemens Aktiengesellschaft' -> {siemens}."""
    words = re.findall(r"[a-z0-9]+", fold(name or ""))
    return frozenset(w for w in words if len(w) > 2 and w not in _NAME_NOISE)


def identity_check(values: list[Found], country: str | None, names: list[str], source: str) -> None:
    """Is the report really this company's? Two signals from the report's own text: the
    country it says the company is registered in, and its legal name (the Siemens run
    read 'Siemens Financieringsmaatschappij N.V.', a Dutch subsidiary). On either
    mismatch, every value read from that report is graded C with the reason; XBRL tags of
    a filing found by the company's LEI are left alone."""
    reasons = []
    stated = next((f.value for f in values if f.data_point == "country_code"
                   and f.source == source and f.value), None)
    if country and stated and stated != country:
        reasons.append(f"the report says the company is in {stated}, the company list says {country}")
    legal = next((f.value for f in values if f.data_point == "legal_name"
                  and f.source == source and f.value), None)
    wanted = [name_core(n) for n in names if name_core(n)]
    if legal and name_core(legal) and wanted and name_core(legal) not in wanted:
        reasons.append(f"the report is by '{clip(str(legal), 60)}', not {names[0]}")
    if not reasons:
        return
    why = "check: " + " and ".join(reasons) + ": possibly another company's report"
    log.warning("Identity check: %s", why)
    for f in values:
        if f.source == source and f.method != "XBRL":
            f.confidence = "C"
            f.note = "; ".join(x for x in (f.note, why) if x)


def same_company(a: str, b: str) -> bool:
    def key(s):
        words = re.sub(r"[^a-z0-9]+", " ", (s or "").lower())       # "N.V." -> "n v"
        return re.sub(r"\b(n v|nv|s a|sa|ag|ab|asa|oyj|plc|se|spa|gmbh|publ|holding)\b| ", "", words)
    return bool(key(a)) and key(a) == key(b)


def website_for(t: Target, result: dict | None, lei_record: dict | None,
                fc: FirecrawlClient) -> str | None:
    c = t.company
    if result and result.get("website"):
        return result["website"]
    disc = CACHE_DIR / f"{c.slug}_discovery.json"
    if disc.exists():
        site = json.loads(disc.read_text(encoding="utf-8")).get("website")
        if site:
            return site
    try:
        return find_official_website(c.name, fc, lei_record, c.country)["website"]
    except (WebsiteNotFoundError, CreditBudgetExceeded) as e:
        log.info("No website for the HTML backup: %s", str(e)[:150])
    except httpx.HTTPError as e:
        log.warning("Website lookup failed: %s", str(e)[:150])
    return None


# --- choosing one value per data point ------------------------------------------------------

def best(values: list[Found]) -> dict[str, Found]:
    """Per data point: the most exact value (A > B > C, then API/XBRL > PARSE > SCRAPE).
    A differing runner-up is mentioned in the note, for review."""
    by: dict[str, list[Found]] = {}
    for f in values:
        if f.data_point.startswith("_") or f.value in (None, ""):
            continue
        by.setdefault(f.data_point, []).append(f)
    out = {}
    for name, fs in by.items():
        fs.sort(key=lambda f: (-CONFIDENCE_RANK[f.confidence], -METHOD_RANK[f.method]))
        top = fs[0]
        if name == "ticker" and top.source == "OpenFIGI":
            # OpenFIGI drops the space of the share class ("VOLVB"); a document that
            # gives the same ticker has the exchange's own spelling ("VOLV B").
            same = next((f for f in fs[1:] if _norm(f.value) == _norm(top.value)
                         and f.value != top.value), None)
            if same:
                top = Found(**{**asdict(top), "value": same.value,
                               "note": f"OpenFIGI {top.value}; spelling from {same.source}"})
        other = next((f for f in fs[1:] if _norm(f.value) != _norm(top.value)), None)
        if other:
            top = Found(**{**asdict(top), "note": "; ".join(x for x in (
                top.note, f"other source says {clip(str(other.value), 80)} ({other.source})") if x)})
        out[name] = top
    return out


def _norm(v) -> str:
    if isinstance(v, (int, float)):
        return fmt_number(round(float(v), -3) if abs(v) >= 1e6 else v)
    return re.sub(r"[^a-z0-9]", "", str(v).lower())


def finish(t: Target, chosen: dict[str, Found], tried: list[str],
           error: str | None, gleif_isins=()) -> list[Found]:
    """One Found per data point, in DATA_POINTS order, with a reason for each gap."""
    us = t.company.country == "US" or t.company.segment == "us_listed"
    isin = chosen.get("isin")
    if isin and gleif_isins and isin.confidence != "A":
        codes = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", str(isin.value).upper())
        if codes and all(code in gleif_isins for code in codes):
            chosen["isin"] = Found(**{**asdict(isin), "confidence": "A",
                                      "note": isin.note + "; confirmed in the GLEIF ISIN map"})
    listed = (chosen.get("listing_status").value == "listed") if chosen.get("listing_status") else None
    if listed is None and any(k in chosen for k in ("ticker", "exchange", "isin")):
        src = next(chosen[k] for k in ("ticker", "exchange", "isin") if k in chosen)
        chosen["listing_status"] = Found(**{**asdict(src), "data_point": "listing_status",
                                            "value": "listed", "unit": "",
                                            "note": f"has a {src.data_point}: {clip(str(src.value), 60)}"})
        listed = True
    band, band_why = market_cap_band(chosen)
    if band:
        chosen["market_cap_band"] = band
    rows = []
    for name in NAMES:
        if name in chosen:
            rows.append(chosen[name])
            continue
        method = ""
        if name == "market_cap_band" and band_why and listed is not False:
            why = band_why
        elif name in API_ONLY and not any(s in ", ".join(tried) for s in apis.API_SOURCES):
            why, method = "not found: only an official API gives it (API step off or no LEI)", ""
        elif name == "cik" and not us:
            why, method = "not applicable: no SEC filing found and not US-listed", ""
        elif listed is False and (name in LISTED_ONLY or name in LISTED_REPORTS_ONLY):
            why, method = "not applicable: the company is not listed", ""
        else:
            why = "not found in: " + ", ".join(tried) if tried else "no source reached"
        if error and name not in API_ONLY:
            why += f" (annual-report route failed: {clip(error, 140)})"
        rows.append(Found(name, None, method=method, note=why))
    return rows


def market_cap_band(chosen: dict[str, Found]) -> tuple[Found | None, str]:
    """Shares outstanding x year-end share price, banded in EUR (MARKET_CAP_BANDS_EUR).
    Returns (the band, or None with the reason)."""
    shares, price = chosen.get("shares_outstanding"), chosen.get("share_price")
    if not shares or not price:
        missing = " and ".join(n for n, f in (("shares outstanding", shares), ("share price", price))
                               if not f)
        return None, f"not derived: no {missing}"
    cap = float(shares.value) * float(price.value)
    if price.unit != "EUR":
        return None, (f"not derived: market cap {cap:,.0f} {price.unit}; the EUR band needs the "
                      f"year-end exchange rate (API step)")
    band = next(name for floor, name in MARKET_CAP_BANDS_EUR if cap >= floor)
    worst = min((shares, price), key=lambda f: CONFIDENCE_RANK[f.confidence])
    return Found("market_cap_band", band, unit="", period_end=price.period_end,
                 source="derived", endpoint=price.endpoint, method="DERIVED",
                 confidence=worst.confidence,
                 note=f"market cap {cap:,.0f} EUR = shares outstanding x share price "
                      f"({shares.source}; {price.source})"), ""


# --- one company ------------------------------------------------------------------------------

NO_CREDITS = "Firecrawl is out of credits"


def from_apis(t: Target, result: dict | None, lei_record: dict | None
              ) -> tuple[list[Found], list[str], list[str]]:
    """The official APIs, before any document: GLEIF (by LEI), ESMA FIRDS and OpenFIGI
    (exchange data, by LEI), the home register (NO, FI, UK; by register number) and
    SEC EDGAR (SEC registrants). Free; responses cached
    for a week. Returns (values, sources answered, GLEIF's ISINs). A failing API is
    logged and skipped: documents still fill its fields."""
    c = t.company
    values: list[Found] = []
    answered: list[str] = []
    isins: list[str] = []
    lei = (lei_record or {}).get("lei") or c.lei
    if lei:
        try:
            g = apis.gleif_values(lei)
            isins = next((f.value.split(";") for f in g if f.data_point == "_gleif_isins"), [])
            values += g
            answered.append("GLEIF")
        except httpx.HTTPError as e:
            log.warning("GLEIF failed: %s", str(e)[:150])
    home = (lei_record or {}).get("country") or c.country
    if lei:
        try:
            ex = listing.listing_values(lei, home, isins)
            values += ex
            answered += list(dict.fromkeys(f.source for f in ex))
        except (httpx.HTTPError, ValueError, KeyError) as e:
            log.warning("Exchange lists (FIRDS/OpenFIGI) failed: %s", str(e)[:150])
    number = (t.business_id or (lei_record or {}).get("registered_as")
              or ((result or {}).get("filing") or {}).get("registration_number")
              or next((str(f.value) for f in values if f.data_point == "business_id"), None))
    reg = apis.registry_values(home, number, (lei_record or {}).get("legal_name") or c.name)
    if reg:
        values += reg
        answered.append(reg[0].source)
    cik = ((result or {}).get("filing") or {}).get("cik")
    us = c.country == "US" or c.segment == "us_listed" or home == "US"
    if not cik:
        # Foreign companies with US-listed shares file 20-Fs too (Equinor: CIK 1140625).
        # The input name first, then the LEI's legal name ("Nokia Oyj" in GLEIF).
        for name in dict.fromkeys(n for n in (c.name, (lei_record or {}).get("legal_name")) if n):
            try:
                cik, why = edgar.find_cik(name)
                log.info("SEC CIK for %r: %s (%s)", name, cik, why)
            except (httpx.HTTPError, edgar.SecContactMissing) as e:
                log.warning("SEC lookup failed: %s", str(e)[:150])
                break
            if cik:
                break
    if cik:
        try:
            sec = apis.edgar_values(int(cik))
            # For a foreign issuer the SEC's ticker and exchange are its US listing (an
            # ADR on the NYSE), not its home market: keep only the identifiers.
            values += sec if us else [f for f in sec if f.data_point in ("cik", "other_names")]
            answered.append("SEC EDGAR")
        except (httpx.HTTPError, edgar.SecContactMissing) as e:
            log.warning("SEC EDGAR failed: %s", str(e)[:150])
    log.info("API step: %d value(s) from %s", len(values), ", ".join(answered) or "no API")
    return values, answered, isins


def collect(t: Target, docs: bool = True, doc_credits: int = DEFAULT_DOC_CREDITS,
            error: str | None = None, flags: set | None = None,
            meter: dict | None = None, use_apis: bool = True) -> list[Found]:
    """`error`: why the annual-report pipeline has no result (if not in its error file).
    `flags` gets "no_credits" when Firecrawl refused for lack of credits; `meter`
    gets "credits", the Firecrawl credits spent here."""
    c = t.company
    flags = flags if flags is not None else set()
    result = json.loads(c.result_path.read_text(encoding="utf-8")) if c.result_path.exists() else None
    if result is None and c.error_path.exists():
        e = json.loads(c.error_path.read_text(encoding="utf-8"))
        error = f"{e.get('error_type')}: {e.get('error')}"
    values: list[Found] = []
    tried: list[str] = []

    # 1. the annual-report pipeline
    lei_record = (result or {}).get("lei_record")
    if result is None:
        try:
            lei_record = identify_lei(c.name, c.slug, c.lei, True, c.country)["record"]
        except Exception as e:  # noqa: BLE001
            log.warning("LEI lookup failed: %s", e)
    if not c.lei and (lei_record or {}).get("lei"):
        c.lei = lei_record["lei"]
    gleif_isins: list[str] = []
    if use_apis:
        # 0. the official APIs first; the documents below fill what they leave empty
        api_values, answered, gleif_isins = from_apis(t, result, lei_record)
        values += api_values
        tried += answered
    origin = report_origin(result) if result else None
    if result:
        values += from_result(result, origin)
        tried.append(origin.source if origin else "annual report")

    # 2. the AI pass over the report
    if origin:
        chunks = report_chunks(origin)
        if chunks:
            log.info("Data points: asking the AI about %d report chunks", len(chunks))
            facts = ask(c.name, origin.url, chunks, "the company's annual report",
                        Path(result["debug"]["markdown_file"]).stem)
            report_values = from_facts(facts, origin)
            # The LEI record's legal country first: the input's country can be the
            # listing market (2020 Bulkers: listed in Norway, registered in Bermuda).
            identity_check(report_values + values,
                           (lei_record or {}).get("country") or c.country,
                           [c.name, (lei_record or {}).get("legal_name") or ""], origin.source)
            values += report_values

    chosen = best(values)
    listed = chosen.get("listing_status")
    unlisted = bool(listed and listed.value == "unlisted")
    fc = lib = site = None
    roles: list[Found] = []
    roles_why = "not applicable: the company is not listed" if unlisted else ""
    try:
        if docs:
            fc = FirecrawlClient(load_settings(), max_credits=doc_credits)
            site = website_for(t, result, lei_record, fc)
            if site:
                year = str((result or {}).get("fiscal_year") or "")
                lib = Library(c.slug, site, int(year) if year.isdigit() else None, fc,
                              skip_urls=[(result or {}).get("report_url")])

        # 3. executive pay (role grain) and the company-level pay terms
        if not unlisted:
            fy = fiscal_end_year(str((result or {}).get("fiscal_year") or ""))
            roles, terms, read = from_pay(
                c.name, c.slug, lib, origin,
                Path(result["debug"]["markdown_file"]).stem if origin else "",
                (result or {}).get("period_end_date") or "",
                (lei_record or {}).get("country") or c.country, fy,
                tuple((u, label) for u, label in ((t.remuneration_report_url, "Remuneration report"),
                                                  (t.annual_report_url, "Annual report")) if u),
                next((int(f.value) for f in values if f.data_point == "cik" and f.value), None))
            values += terms
            tried += [r for r in read if r not in tried]
            if not roles:
                roles_why = ("not found in: " + ", ".join(read) if read
                             else "no remuneration report found")

        # 4. document fallback for the company-grain data points still missing
        chosen = best(values)
        gaps = gap_list(chosen)
        if lib and gaps:
            log.info("Document fallback on %s for: %s", site, ", ".join(gaps))
            found, read = from_documents(c.name, c.slug, site, gaps, lib, fc)
            values += found
            tried += list(dict.fromkeys(read)) or ["company documents (none usable found)"]
    except PaymentRequiredError:
        flags.add("no_credits")
        tried.append(f"company documents (skipped: {NO_CREDITS})")
        roles_why = roles_why or f"remuneration report not searched: {NO_CREDITS}"
    if fc:
        log.info("Documents used %d Firecrawl credit(s)", fc.credits.total)
        if meter is not None:
            meter["credits"] = fc.credits.total
    chosen = best(values)
    parent = chosen.get("ultimate_parent")
    if parent and any(same_company(parent.value, n) for n in
                      (c.name, getattr(chosen.get("legal_name"), "value", ""))):
        del chosen["ultimate_parent"]          # the company itself: it is the top of its group
    return finish(t, chosen, tried, error, gleif_isins) + (roles or no_roles(roles_why))


def rows_for(t: Target, found: list[Found]) -> list[dict]:
    c = t.company
    lei = next((str(f.value) for f in found if f.data_point == "lei" and f.value), c.lei or "")
    rows = []
    for f in found:
        value = fmt_number(f.value) if isinstance(f.value, (int, float)) else (f.value or "")
        rows.append({"company_id": c.company_id, "company_name": c.name,
                     "segment": c.segment or "", "country": c.country or "", "lei": lei,
                     "grain": f.grain, "role_row": f.role_row, "data_point": f.data_point, "value": value, "unit": f.unit,
                     "period_end": f.period_end, "source": f.source, "endpoint": f.endpoint,
                     "method": f.method, "retrieved_at": f.retrieved_at if f.value not in (None, "")
                     else "", "confidence": f.confidence, "note": f.note})
    return rows


def dp_path(c: Company) -> Path:
    return DP_DIR / f"{c.slug}.json"


def no_credits_path(c: Company) -> Path:
    """Marks a company done without Firecrawl (out of credits): redone on the next run."""
    return DP_DIR / f"{c.slug}.nocredits"


def process(t: Target, opts: dict) -> dict:
    """Runs in a worker process. The pipeline first (unless done before), then the data
    points. Returns {"kind": "done"|"fatal"|"error", ...}."""
    c = t.company
    started = time.monotonic()
    flags: set = set()
    meter = {"credits": 0}
    error = None
    resolve_lei(t)
    if needs_pipeline(c, opts):
        res = process_company(c, False, opts["pipeline_credits"])
        meter["pipeline"] = res.get("credits", 0)
        if res["kind"] == "fatal" and "PaymentRequired" in res.get("error", ""):
            # The free routes (filings, registers, APIs) still work: carry on without
            # Firecrawl; the company is redone on the next run.
            flags.add("no_credits")
            error = f"{NO_CREDITS}: the website report search was skipped"
        elif res["kind"] in ("fatal", "offline"):
            return res | {"credits": meter["pipeline"]}
    handler = logging.FileHandler(OUTPUT_DIR / f"{c.slug}.log", mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    try:
        found = collect(t, docs=opts["docs"] and "no_credits" not in flags,
                        doc_credits=opts["doc_credits"], error=error, flags=flags, meter=meter,
                        use_apis=opts.get("apis", True))
    except FATAL as e:
        return {"kind": "fatal", "error": f"{type(e).__name__}: {e}", "credits": spent(meter)}
    except Exception as e:  # noqa: BLE001 - record and continue with the next company
        log.exception("Data points for %s failed", c.company_id)
        return {"kind": "error", "error": f"{type(e).__name__}: {str(e)[:200]}",
                "credits": spent(meter)}
    finally:
        logging.getLogger().removeHandler(handler)
        handler.close()
    rows = rows_for(t, found)
    DP_DIR.mkdir(parents=True, exist_ok=True)
    dp_path(c).write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    if "no_credits" in flags:
        no_credits_path(c).write_text(NO_CREDITS, encoding="utf-8")
    else:
        no_credits_path(c).unlink(missing_ok=True)
    return {"kind": "done", "no_credits": "no_credits" in flags,
            "found": sum(1 for r in rows if r["value"]), "total": len(rows),
            "seconds": time.monotonic() - started, "credits": spent(meter)}


def resolve_lei(t: Target) -> None:
    """No LEI in the input: try the ISIN or register number in GLEIF before the
    pipeline's name search, which misses companies listed under another name."""
    c = t.company
    if c.lei or not (t.isin or t.business_id):
        return
    from .lei import find_lei_by_id
    try:
        rec, how = find_lei_by_id(t.business_id, c.country, t.isin)
    except Exception as e:  # noqa: BLE001 - GLEIF down: the name search still runs
        log.warning("LEI lookup by identifier failed: %s", str(e)[:150])
        return
    if rec:
        log.info("LEI %s for %s (%s)", rec.lei, c.name, how)
        c.lei = rec.lei


def spent(meter: dict) -> int:
    return meter.get("pipeline", 0) + meter.get("credits", 0)


def needs_pipeline(c: Company, opts: dict) -> bool:
    return not c.result_path.exists() and (not c.error_path.exists() or opts["retry_failed"]
                                           or no_credits_path(c).exists())


def worst_case(t: Target, opts: dict) -> int:
    """The most Firecrawl credits one company can spend (both caps hold per company)."""
    return ((opts["pipeline_credits"] if needs_pipeline(t.company, opts) else 0)
            + (opts["doc_credits"] if opts["docs"] else 0))


# --- outputs --------------------------------------------------------------------------------

def write_csv(targets: list[Target], out: Path) -> int:
    n = 0
    tmp = out.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for t in targets:
            p = dp_path(t.company)
            if p.exists():
                for row in json.loads(p.read_text(encoding="utf-8")):
                    w.writerow(row)
                    n += 1
    for attempt in range(5):
        try:
            tmp.replace(out)
            break
        except PermissionError:           # open in Excel
            time.sleep(1 + attempt)
    return n


SCALE = {"millions": 1e6, "thousands": 1e3, "billions": 1e9, "": 1}


def build_value(golden: dict, row: dict) -> str:
    """Our value in the golden row's unit (money in millions, codes as they are)."""
    v = row["value"]
    if not v:
        return ""
    unit = (golden.get("unit") or "").strip().lower()
    if unit in SCALE and unit and re.fullmatch(r"-?\d+(\.\d+)?", v):
        cur = (golden.get("currency") or "").strip()
        if cur and row["unit"] and cur != row["unit"]:
            return f"{fmt_number(round(float(v) / SCALE[unit], 3))} ({row['unit']}, golden in {cur})"
        return fmt_number(round(float(v) / SCALE[unit], 3))
    return v


def write_golden_filled(src: Path, targets: list[Target], out: Path) -> Path | None:
    """The golden sample with build_value filled from our rows (same rows, same columns)."""
    text = src.read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    if not rows or "field" not in rows[0] or "build_value" not in rows[0]:
        return None
    ours: dict[tuple[str, str], dict] = {}
    for t in targets:
        p = dp_path(t.company)
        if p.exists():
            for r in json.loads(p.read_text(encoding="utf-8")):
                if r.get("grain", "company") == "company":
                    ours[(r["company_id"], r["data_point"])] = r
    alias = {"fte": "fte", "headcount": "headcount"}
    for r in rows:
        mine = ours.get((r["company_id"], alias.get(r["field"], r["field"])))
        if mine:
            r["build_value"] = build_value(r, mine)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return out


# --- CLI --------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.datapoints",
                                description="Every data point, with its exact source, for a CSV of companies.")
    p.add_argument("csv", type=Path, help="CSV with company_id, company_name (+ segment, country, lei, business_id)")
    p.add_argument("--out", type=Path, default=OUTPUT_DIR / "datapoints.csv")
    p.add_argument("--only", help="Comma-separated company_ids")
    p.add_argument("--limit", type=int, help="Only the first N companies")
    p.add_argument("--workers", type=int, default=1, help="Companies at the same time (3 is a good choice)")
    p.add_argument("--redo", action="store_true", help="Redo the data points of companies done before")
    p.add_argument("--retry-failed", action="store_true",
                   help="Re-run the annual-report pipeline for companies where it failed before")
    p.add_argument("--no-apis", action="store_true",
                   help="Skip the official APIs (GLEIF, registers, SEC EDGAR)")
    p.add_argument("--no-docs", "--no-web", dest="no_docs", action="store_true",
                   help="No document fallback (no Firecrawl credits for it)")
    p.add_argument("--doc-credits", "--web-credits", dest="doc_credits", type=int,
                   default=DEFAULT_DOC_CREDITS,
                   help=f"Firecrawl credits per company for the document fallback (default {DEFAULT_DOC_CREDITS})")
    p.add_argument("--pipeline-credits", type=int, default=DEFAULT_PIPELINE_CREDITS,
                   help=f"Firecrawl credits per company for finding the report (default {DEFAULT_PIPELINE_CREDITS})")
    p.add_argument("--max-run-credits", type=int,
                   help="Firecrawl credits for the whole run. A company only starts if the credits "
                        "spent plus the worst case of every company still running stay within it")
    args = p.parse_args(argv)

    OUTPUT_DIR.mkdir(exist_ok=True)
    _setup_logging()
    try:
        everyone = read_targets(args.csv)
    except (OSError, ValueError, csv.Error) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    targets = everyone
    if args.only:
        wanted = {x.strip() for x in args.only.split(",")}
        targets = [t for t in targets if t.company.company_id in wanted]
    if args.limit:
        targets = targets[:args.limit]
    todo = [t for t in targets if args.redo or not dp_path(t.company).exists()
            or no_credits_path(t.company).exists()]
    print(f"{len(targets)} companies from {args.csv}; {len(targets) - len(todo)} done before")
    opts = {"docs": not args.no_docs, "doc_credits": args.doc_credits, "apis": not args.no_apis,
            "pipeline_credits": args.pipeline_credits, "retry_failed": args.retry_failed}

    workers = max(1, args.workers)
    code = 0
    budget = Budget(args.max_run_credits)
    with _KeepAwake():
        if workers == 1:
            for i, t in enumerate(todo, 1):
                if not budget.allows(t, opts, []):
                    budget.skipped = len(todo) - i + 1
                    break
                res = process(t, opts)
                budget.spent += res.get("credits", 0)
                code = _report(i, len(todo), t, res) or code
                if res["kind"] in ("fatal", "offline"):
                    break
                write_csv(everyone, args.out)
        else:
            with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init,
                                     initargs=(workers,)) as ex:
                queue, running, i = list(todo), {}, 0
                while queue or running:
                    while queue and len(running) < workers and not code:
                        if not budget.allows(queue[0], opts, list(running.values())):
                            if not running:                 # nothing will free up credits
                                budget.skipped, queue = len(queue), []
                            break
                        t = queue.pop(0)
                        running[ex.submit(process, t, opts)] = t
                    if not running:
                        break
                    done, _ = wait(list(running), return_when=FIRST_COMPLETED)
                    for fut in done:
                        t = running.pop(fut)
                        i += 1
                        try:
                            res = fut.result()
                        except Exception as e:  # noqa: BLE001
                            res = {"kind": "error", "error": f"worker crashed: {e}"}
                        budget.spent += res.get("credits", 0)
                        code = _report(i, len(todo), t, res) or code
                        write_csv(everyone, args.out)
    n = write_csv(everyone, args.out)
    print(f"\n{n} rows: {args.out}")
    print(f"Firecrawl credits used: {budget.spent}"
          + (f" of the run's {budget.cap}" if budget.cap is not None else ""))
    if budget.skipped:
        print(f"{budget.skipped} companies not started: they could exceed --max-run-credits")
    filled = write_golden_filled(args.csv, everyone, OUTPUT_DIR / "golden_test_filled.csv")
    if filled:
        print(f"Golden sample with build_value: {filled}")
    return code


@dataclass
class Budget:
    """--max-run-credits: a company starts only if the credits spent so far, plus the
    worst case of every company still running and of this one, stay within the cap."""
    cap: int | None
    spent: int = 0
    skipped: int = 0

    def allows(self, t: Target, opts: dict, running: list[Target]) -> bool:
        if self.cap is None:
            return True
        reserved = sum(worst_case(r, opts) for r in running)
        return self.spent + reserved + worst_case(t, opts) <= self.cap


def _report(i: int, n: int, t: Target, res: dict) -> int:
    prefix = f"[{i}/{n}] {t.company.company_id} {t.company.name}"
    if res["kind"] == "done":
        print(f"{prefix}: {res['found']}/{res['total']} data points ({res['seconds']:.0f}s)"
              + (f" [{NO_CREDITS}: free sources only]" if res.get("no_credits") else ""), flush=True)
        return 0
    print(f"{prefix}: {res['kind'].upper()} {res.get('error', '')}", flush=True)
    return 2 if res["kind"] in ("fatal", "offline") else 0


if __name__ == "__main__":
    sys.exit(main())
