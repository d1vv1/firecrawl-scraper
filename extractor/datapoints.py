"""Every data point for a list of companies, one row per value, with the exact place
each value came from.

    python -m extractor.datapoints data/golden_test_sample_5_per_segment_country_all.csv
        [--workers 3] [--only ID,ID] [--limit N] [--retry-failed] [--redo] [--no-docs]
        [--fields pay|company|revenue,headcount...] [--ignore-run-required] [--dry-run]

--fields collects only those data points and replaces only them in the saved rows; the
input's run_required ("Pay Data", "Company Data") limits a company the same way unless
--ignore-run-required (fields.py, issue 16).

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
     report on the site, the annual report's remuneration section; amounts in a pay
     table of a PDF come from the table itself (pay_tables.py);
  5. document fallback: data points still missing are looked for in the company's
     other documents (governance and sustainability reports, "The share" and
     shareholder pages, legal notice, year-end report...; see documents.py), in
     rounds, at most --doc-credits Firecrawl credits per company.
See docs/pipeline_flow.html for the whole flow.

Output:
  <--out>.csv                  one row per company and data point, and per role and pay
                               field (18 columns, COLUMNS)
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
  scraper_version  the scraper version that extracted it (config.SCRAPER_VERSION; 0 for
              values saved before versioning). --outdated re-runs companies below it
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from urllib.parse import quote as urlquote, urlparse

import httpx
import openai
from firecrawl import PaymentRequiredError

from . import apis, edgar, fx, listing, llm, pay, pay_tables, requote, sector
from . import fields as selection
from .apis import Found
from .batch import FATAL, Company, _KeepAwake, _setup_logging, _worker_init, process_company
from .config import CACHE_DIR, OUTPUT_DIR, SCRAPER_VERSION, fold, load_settings
from .documents import (DP_DOC_TYPES, Candidate, DocType, Document, Library, _stem as doc_stem,
                        title_year)
from .extract import full_value, full_value_quoted, printed_figure
from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from .pipeline import find_official_website, identify_lei, run as run_report
from .report_finder import extract_year, is_pdf_url
from .schemas import DataPointFacts, Holder, NumberFact, TextFact
from .scraper import Page, cache_stem, local_file, markdown_to_pages, pages_to_markdown
from .sections import DATAPOINT_TOPICS, Chunk, select_chunks, split_chunks
from .validate import figure_in_quote, iso_currency, lone_cell, quote_in_text, source_row
from .website import WebsiteNotFoundError

log = logging.getLogger("extractor.datapoints")

COLUMNS = ["company_id", "company_name", "segment", "country", "lei", "grain", "role_row",
           "data_point", "value", "unit", "period_end", "source", "endpoint", "method",
           "retrieved_at", "confidence", "note", "scraper_version"]

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
API_ONLY = {"lei"}
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
# A report up to this long is read whole. The keyword pick below showed the AI a median 14%
# of a report (12 Nov 2026, 407 reports), and values stated in the rest stayed empty: of 83
# such values in 8 reports, the whole report gave 32. Longer reports share this budget
# between the topics. 200,000 words is about 300,000 tokens; set REPORT_WORDS=0 for a
# model with a small context window or token quota (the keyword pick alone).
REPORT_WORDS = int(os.getenv("REPORT_WORDS", "200000"))
DOC_WORDS = int(os.getenv("DOC_WORDS", "60000"))     # the same for each fallback document
TOPIC_WORDS = 2_500                  # report words sent per topic at least (7 topics)
DOC_TOPIC_WORDS = 1_500              # words per needed topic at least, from a long fallback document
DOC_ROUNDS = 3                       # AI calls over fallback documents, at most
DOCS_PER_ROUND = 3                   # documents read per round
DEFAULT_DOC_CREDITS = 10             # maps and page scrapes; PDFs are downloaded for free
DEFAULT_PIPELINE_CREDITS = 8           # website (2), map (1), web search (2), page (1), maps

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
    # The tracker's run_required ("Pay Data", "Company Data", "Company and Pay Data")
    run_required: str | None = None
    # The data points this run collects (fields.py); None: all of them
    fields: frozenset[str] | None = None


FILINGS_SEARCH = re.compile(
    r"filings\.xbrl\.org/api/filings\?.*entity\.identifier(?:\]|%5D)?=([A-Z0-9]{20})\b", re.I)


def known_ids() -> dict[str, str]:
    """ISIN -> company_id of every company in the runs saved in output/ (their isin rows),
    so a company list without ids reuses a company's id and a merge doesn't add it twice."""
    out: dict[str, str] = {}
    for f in sorted(OUTPUT_DIR.glob("*_datapoints.csv")):
        try:
            with open(f, encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    if r.get("data_point") == "isin" and r.get("value"):
                        for code in re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", r["value"].upper()):
                            out.setdefault(code, r["company_id"])
        except (OSError, csv.Error, KeyError):
            continue
    return out


def new_id(name: str, isin: str) -> str:
    """'STABILUS SE INH. EO-,01', DE000STAB1L8 -> 'stabilus-se-1f0c2a9e': the name without
    its listing line, and a hash of the ISIN so two companies never share an id."""
    from .config import slugify, without_share_class
    tail = hashlib.sha1((isin or name).encode()).hexdigest()[:8]
    return f"{slugify(without_share_class(name))[:50]}-{tail}"


def read_targets(path: Path) -> list[Target]:
    """One Target per company_id, in first-seen order. The country "(none)" (and any
    value that isn't a 2-letter code) means unknown.

    Also reads the company tracker saved as a UTF-8 CSV ("Company Name", "ISIN", "Run
    required", "Company URL", "Link" = remuneration report, "Annual Link", "Link3" as
    "Additional Files_1" says): without a company_id column, a company's id is the one it
    has in earlier runs (by ISIN), else a new one from its name and ISIN."""
    text = path.read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t")
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    low = {h: (h or "").strip().lower() for h in rows[0]} if rows else {}

    def col(*names):
        return next((h for h, l in low.items() if l in names), None)
    c_id = col("company_id", "id")
    c_name = col("company_name", "name", "legal_name", "company name")
    c_country, c_seg = col("country", "country_code"), col("segment", "tier")
    c_lei, c_bid = col("lei"), col("business_id", "registration_id", "org_number")
    tracker = col("remuneration files") is not None
    c_rem = col("remuneration_report_url") or (col("link") if tracker else None)
    c_ar = col("annual_report_url", "annual link")
    c_extra_type, c_extra = col("additional files_1"), col("link3")
    c_isin, c_req = col("isin"), col("run_required", "run required")
    c_site = col("website", "company url", "company_url")
    if not c_name or not (c_id or c_isin):
        raise ValueError(f"{path} needs company_id (or ISIN) and company_name columns")
    ids = known_ids() if not c_id else {}
    if not c_id:
        for r in rows:
            name = (r.get(c_name) or "").strip()
            isin = (r.get(c_isin) or "").strip().upper()
            r["_id"] = ids.get(isin) or new_id(name, isin) if name else ""
        c_id = "_id"
    for r in rows:
        # the tracker's extra file goes where its type says, when that column is empty
        kind = (r.get(c_extra_type) or "").lower() if c_extra_type else ""
        url = (r.get(c_extra) or "").strip() if c_extra else ""
        if url and "remuneration" in kind and c_rem and not (r.get(c_rem) or "").strip():
            r[c_rem] = url
        elif url and "annual" in kind and c_ar and not (r.get(c_ar) or "").strip():
            r[c_ar] = url
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
        site = (r.get(c_site) or "").strip() if c_site else ""
        if site and not t.company.website:
            t.company.website = site if site.startswith("http") else f"https://{site}"
        isin = (r.get(c_isin) or "").strip().upper() if c_isin else ""
        if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin) and not t.isin:
            t.isin = isin
        required = (r.get(c_req) or "").strip() if c_req else ""
        if required and not t.run_required:
            t.run_required = required
        for attr, column in (("remuneration_report_url", c_rem), ("annual_report_url", c_ar)):
            url = (r.get(column) or "").strip() if column else ""
            searched = FILINGS_SEARCH.search(url)
            if searched:
                # a filings.xbrl.org search, not a report (K2A, SED Energy): its LEI lets the
                # report step find the filing itself
                if not t.company.lei:
                    t.company.lei = searched.group(1).upper()
                continue
            if url.startswith(("http", "file:")) and not getattr(t, attr):
                setattr(t, attr, url)
        # a report supplied on disk is the one the report step reads (from_reports.py)
        if t.annual_report_url and t.annual_report_url.startswith("file:"):
            t.company.report_url = t.annual_report_url
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


# A quote is kept whole in the note, up to this length: a clipped quote can't be looked
# up again in the source text (96 failed quote checks in the FY2025 file were clipped).
QUOTE_CHARS = 1000


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

# note on a value whose quote is the source line the code found, not the AI's (source_row)
REPLACED = " (the source row; the AI's quote pieced table cells together)"
# ... or the figure's own cell of a table drawn cell by cell (validate.lone_cell)
LONE_CELL = " (the figure's own cell; the table is drawn cell by cell and the quote's words are on this page)"


def find_source_row(quote: str, figure: float, near: list[tuple], texts: list[tuple]):
    """(line, key, note) of validate.source_row in the (key, text) pairs `near` the quote's
    place, else in all `texts`, else the figure's own cell (validate.lone_cell); None when
    no line or more than one qualifies."""
    for group in (near, texts):
        hits = [(row, key) for key, text in group if (row := source_row(quote, figure, text))]
        if len(hits) == 1:
            return (*hits[0], REPLACED)
        if len(hits) > 1:
            return None
    cell = lone_cell(quote, figure, texts)
    return (*cell, LONE_CELL) if cell else None


_NOT_FOUND = re.compile(r'(PDF page (\d+)|report text|web page): "(.*?)…?" \(quote not found verbatim\)')


def repair_quotes(rows: list[dict], pages_of) -> None:
    """Saved values whose quote was not in the text get the source row as their quote, as
    Origin.where now does during a run (no source asked again; `pages_of(endpoint)` gives
    the cached text by page). Only figures: the printed figure must be on the row."""
    for r in rows:
        m = _NOT_FOUND.search(r["note"]) if r["value"] else None
        if not m:
            continue
        printed = re.search(r"printed (-?[\d.]+(?:e[+-]?\d+)?)", r["note"])
        try:
            figure = float(printed.group(1) if printed else r["value"])
        except ValueError:
            continue
        pages = pages_of(r["endpoint"])
        if not pages:
            continue
        texts = sorted(pages.items())
        page = int(m.group(2)) if m.group(2) else None
        near = [t for t in texts if page and t[0] in (page, page - 1, page + 1)]
        found = find_source_row(m.group(3), figure, near, texts)
        if not found:
            continue
        row, key, tail = found
        base = r["endpoint"].split("#")[0]
        if m.group(2):
            where, r["endpoint"] = f"PDF page {key}", f"{base}#page={key}"
        else:
            where, r["endpoint"] = m.group(1), text_fragment(base, row)
        note = r["note"].replace(m.group(0), f'{where}: "{clip(row, QUOTE_CHARS)}"{tail}')
        r["note"] = re.sub(r"; the figure \S+ is not in the quote", "", note)
        if r["confidence"] == "C":
            r["confidence"] = "B"


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
    pdf: Path | None = None  # the cached PDF, for page images of pay tables

    def page_text(self) -> dict[int, str]:
        return {p.number: p.text for p in self.pages}

    def place(self, quote: str | None, chunk_id: int | None,
              figure: float | None = None) -> tuple["Origin", str, str, str, str | None]:
        return (self, *self.where(quote, chunk_id, figure))

    def source_row(self, quote: str, chunk_id: int | None, figure: float) -> tuple[str, int | None, str] | None:
        """(the source line, its page or chunk id) for a quote not in the text: the one line
        printing the figure with the quote's words (validate.source_row), looked for in the
        quote's chunk first, then in the whole document, where it must be the only one."""
        if self.kind == "web":
            texts = [(cid, ch.text) for cid, ch in self.chunks.items()]
            near = [t for t in texts if t[0] == chunk_id]
        else:
            texts = [(p.number, p.text) for p in self.pages]
            chunk = self.chunks.get(chunk_id) if chunk_id is not None else None
            near = [t for t in texts if chunk and t[0] in chunk.pages]
        return find_source_row(quote, figure, near, texts)
        return None

    def where(self, quote: str | None, chunk_id: int | None,
              figure: float | None = None) -> tuple[str, str, str, str | None]:
        """(endpoint, confidence, location note, the quote used) for a value with this quote.
        A quote not in the text, for a value with a figure, is replaced by the source line
        that prints the figure, when one line clearly is the one meant (source_row)."""
        if self.kind == "web":
            url = (self.page_urls or {}).get(chunk_id, self.url)
            chunk = self.chunks.get(chunk_id)
            ok = bool(quote and chunk and quote_in_text(quote, chunk.text))
            if not ok and quote:          # wrong chunk id: look in every page
                for cid, ch in self.chunks.items():
                    if quote_in_text(quote, ch.text):
                        url, ok = (self.page_urls or {}).get(cid, url), True
                        break
            fixed = None
            if not ok and quote and figure is not None:
                fixed = self.source_row(quote, chunk_id, figure)
                if fixed:
                    quote, ok = fixed[0], True
                    url = (self.page_urls or {}).get(fixed[1], url)
            return (text_fragment(url, quote) if ok else url, "B" if ok else "C",
                    f'web page: "{clip(quote, QUOTE_CHARS)}"' + (fixed[2] if fixed else "" if ok
                                                    else " (quote not found verbatim)"), quote)
        loc = locate(quote, chunk_id, self.chunks, self.pages)
        fixed = None
        if not loc.verified and quote and figure is not None:
            fixed = self.source_row(quote, chunk_id, figure)
            if fixed:
                quote, loc = fixed[0], Located(fixed[1], True)
        conf = "B" if loc.verified else "C"
        tail = fixed[2] if fixed else "" if loc.verified else " (quote not found verbatim)"
        if self.kind == "pdf":
            page = loc.page
            return (f"{self.url}#page={page}" if page else self.url, conf,
                    f'PDF page {page}: "{clip(quote, QUOTE_CHARS)}"{tail}' if page else f'"{clip(quote, QUOTE_CHARS)}"{tail}',
                    quote)
        # Filed XHTML / HTML report text has no fixed pages: link to the quote itself.
        return (text_fragment(self.url, quote) if loc.verified else self.url, conf,
                f'report text: "{clip(quote, QUOTE_CHARS)}"{tail}', quote)


@dataclass
class Bundle:
    """Several documents read in one AI call. Chunk ids are unique across them, so a
    value is placed in the document its chunk came from; if its quote isn't there (the
    model gave the wrong chunk id), in whichever document has it."""
    origins: list[Origin]

    def place(self, quote: str | None, chunk_id: int | None,
              figure: float | None = None) -> tuple[Origin, str, str, str, str | None]:
        first = next((o for o in self.origins if chunk_id in o.chunks), self.origins[0])
        placed = first.place(quote, chunk_id)
        if placed[2] == "B" or not quote:
            return placed
        for o in self.origins:
            if o is not first:
                other = o.place(quote, None)
                if other[2] == "B":
                    return other
        # in no document as quoted: the source row, in the chunk's document first
        if figure is not None:
            for o in [first] + [o for o in self.origins if o is not first]:
                other = o.place(quote, chunk_id if o is first else None, figure)
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
                  + (f" {filing.get('form')}" if filing.get("type") == "edgar" else "")
                  # issue 6: a holding company's group figures, from its parent's accounts
                  + (f": {PARENT_ACCOUNTS}" if "parent company" in (filing.get("form") or "") else ""))
    else:
        source = "Annual report (PDF)" if kind == "pdf" else "Annual report (web page)"
    pdf = (CACHE_DIR / md_name).with_suffix(".pdf")
    return Origin(kind, result["report_url"], source, "PARSE", result.get("extracted_at") or _now(),
                  pages, chunks, pdf=pdf if kind == "pdf" and pdf.exists() else None)


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
                     confidence="C", note=f'"{clip(m.get("quote"), QUOTE_CHARS)}"', retrieved_at=at)
    endpoint, conf, where, _ = origin.where(m.get("quote"), m.get("chunk_id"),
                                            m["value"] if isinstance(m["value"], (int, float)) else None)
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
    if money is None and origin is not None:
        # no revenue or total assets read (a pre-revenue company, a bank): the year and its
        # end are still the report's (Chesterfield's FY2025 report had no fiscal year row)
        money = Found("_report", None, source=origin.source, endpoint=origin.url, method="PARSE",
                      confidence="B")
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
    # said again after the text: a whole report is 100,000 words between the two
    return (f"Company legal name: {name}\nSource: {url}\n\n{only}"
            f"Excerpts from {what} (tables are in markdown):\n\n{body}"
            + (f"\n\n{only.strip()}" if only else ""))


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


def report_chunks(origin: Origin, gaps: list[str] | None = None) -> list[Chunk]:
    """What the AI reads of the report: all of it when it is no longer than REPORT_WORDS;
    of a longer one the best chunks per topic, the topics sharing that budget: every
    topic, or only those of `gaps` (plus the profile, for the identity check)."""
    chunks = list(origin.chunks.values())
    if chunks and sum(c.words for c in chunks) <= REPORT_WORDS:
        return chunks
    topics = list(DATAPOINT_TOPICS) if gaps is None else sorted(
        {"profile"} | {FACT_TOPIC[g] for g in gaps if FACT_TOPIC.get(g) in DATAPOINT_TOPICS}
        | ({"keyfigures"} if any(FACT_TOPIC.get(g) == "financials" for g in gaps) else set()))
    words = max(TOPIC_WORDS, REPORT_WORDS // len(topics))
    picked: dict[int, Chunk] = {}
    for topic in topics:
        for c in select_chunks(chunks, topic, words):
            picked[c.id] = c
    return [picked[i] for i in sorted(picked)]


def _breakdown(b) -> str:
    return "; ".join(f"{getattr(i, 'country', None) or i.segment}: {fmt_number(i.value)}"
                     for i in b.items)


# A line of profit, not of income, is never the revenue ("Operating profit 1,234",
# "Rörelseresultat", "Betriebsergebnis"). A label that also names revenue or the
# statement ("Statement of Profit or Loss ... management fees") is not one.
PROFIT_LABEL = re.compile(r"\b(profit|result|ebit|ebitda|resultat|rörelseresultat|driftsresultat|"
                          r"ergebnis|betriebsergebnis|liiketulos|tulos|overskudd)\b", re.I)
REVENUE_WORDS = re.compile(r"profit (or|and) loss|revenue|sales|turnover|fees|umsatz|erlöse|"
                           r"omsättning|omsætning|omsetning|inntekter|intäkter|liikevaihto", re.I)
SAME_AS_PROFIT = "same figure as the operating profit read: check it is not a profit line"


def _label(quote: str | None) -> str:
    """The words before a quote's first figure: the line label of a table row."""
    return re.split(r"\d", quote or "", maxsplit=1)[0]


def not_a_profit_line(found: list[Found], revenue_quote: str | None) -> list[Found]:
    """A revenue read off a profit line is dropped. A revenue and an EBITDA of the same
    figure can't both be right: "Operating income" is a bank's total income (ProCredit)
    but an investment company's result (Industrivärden), and the label can't tell which.
    The EBITDA goes, and the revenue is kept graded C for a look."""
    rev = next((f for f in found if f.data_point == "revenue"), None)
    if rev is None:
        return found
    label = _label(revenue_quote)
    if PROFIT_LABEL.search(label) and not REVENUE_WORDS.search(label):
        log.info("Revenue %s dropped: read off a profit line (%r)", rev.value, label.strip())
        return [f for f in found if f is not rev]
    ebitda = next((f for f in found if f.data_point == "ebitda"), None)
    if (ebitda is not None and ebitda.value and rev.value
            and abs(float(ebitda.value) - float(rev.value)) <= 0.001 * abs(float(rev.value))):
        log.info("EBITDA %s dropped: it is the revenue figure", ebitda.value)
        rev.confidence = "C"
        rev.note = f"{rev.note}; {SAME_AS_PROFIT}" if rev.note else SAME_AS_PROFIT
        return [f for f in found if f is not ebitda]
    return found


def from_facts(facts: DataPointFacts, origin: Origin | Bundle, country: str | None = None) -> list[Found]:
    """The AI's facts as Found values, each placed by its quote (in its document, when
    several documents were read together). `country` picks the MIC of a growth market
    named in several countries ("First North")."""
    out: list[Found] = []

    def add(name: str, value, fact, unit: str = "", period: str = "", extra: str = "",
            figure=None, method: str = ""):
        if value in (None, "", []) or not getattr(fact, "quote", None):
            return                      # no quote, no value: the prompt demands one
        doc, endpoint, conf, where, quote = origin.place(fact.quote, fact.chunk_id, figure)
        if figure is not None and not figure_in_quote(figure, quote):
            # worked out by the AI or taken from the wrong place
            conf, where = "C", f"{where}; the figure {fmt_number(figure)} is not in the quote"
        dated = f"document dated {doc.date}" if doc.date else ""
        out.append(Found(name, value, unit=unit, period_end=period or "", source=doc.source,
                         endpoint=endpoint, method=method or doc.method, confidence=conf,
                         note="; ".join(x for x in (extra, where, dated) if x),
                         retrieved_at=doc.retrieved_at))

    for name in ("revenue", "total_assets"):
        n: NumberFact = getattr(facts, name)
        if n.value is not None and n.unit:
            shown = printed_figure(n.value, n.unit, n.quote)
            add(name, full_value_quoted(n.value, n.unit, n.quote), n, unit=n.currency or "",
                period=n.period_end, figure=shown,
                extra=f"printed {fmt_number(shown)} {n.unit}")
    e = facts.ebitda
    if e.value is not None and e.unit and e.measure:
        what = e.measure.replace("_", " ") + (" (company-defined)" if e.company_defined else "")
        shown = printed_figure(e.value, e.unit, e.quote)
        add("ebitda", full_value_quoted(e.value, e.unit, e.quote), e, unit=e.currency or "",
            figure=shown, extra=f"{what}; printed {fmt_number(shown)} {e.unit}"
                  + (f" ({e.label_in_report})" if e.label_in_report else ""))
    out[:] = not_a_profit_line(out, facts.revenue.quote)
    for name in ("fte", "headcount"):
        n = getattr(facts, name)
        # "Average employees [A] Thousand ... 88" (Shell): scaled like any printed unit
        scaled = n.unit not in (None, "units")
        shown = printed_figure(n.value, n.unit or "units", n.quote)
        add(name, full_value_quoted(n.value, n.unit or "units", n.quote), n, unit="employees",
            period=n.period_end, figure=shown, extra=f"printed {fmt_number(shown)} {n.unit}" if scaled else "")
    n, t = facts.shares_outstanding, facts.treasury_shares
    if n.value is not None:
        shares = full_value_quoted(n.value, n.unit or "units", n.quote)
        held = (full_value_quoted(t.value, t.unit or "units", t.quote)
                if t.value and t.quote and figure_in_quote(t.value, t.quote) else None)
        if held and not OUTSTANDING_WORDS.search(n.quote or "") and 0 < held < shares:
            # Bang & Olufsen: 147,326,503 issued, 4,719,497 in treasury
            add("shares_outstanding", shares - held, n, unit="shares", period=n.period_end,
                figure=n.value, method="DERIVED",
                extra=f"derived: {fmt_number(shares)} issued - {fmt_number(held)} treasury shares "
                      f"(treasury: \"{clip(t.quote, 80)}\")")
        else:
            add("shares_outstanding", shares, n, unit="shares", period=n.period_end, figure=n.value)
    p = facts.share_price
    if p.value is not None and p.currency:
        add("share_price", p.value, p, unit=p.currency, period=p.date or "", figure=p.value,
            extra=f"closing price {p.date}" if p.date else "closing price at year end")
    for name in ("legal_name", "business_id", "other_names", "head_office_city", "ticker",
                 "isin", "exchange", "exchange_segment", "listing_date", "sub_sector",
                 "fiscal_year_end", "reporting_currency", "accounting_basis", "pension_type",
                 "benefits", "shareholding_requirement"):
        t: TextFact = getattr(facts, name)
        if name == "exchange_segment" and STOCK_INDEX.search(t.value or ""):
            continue                    # "FTSE 250": index membership is not a segment
        mic = listing.mic_for_name(t.value, country) if name == "exchange" and t.value else None
        add(name, t.value, t, extra=f"MIC {mic}" if mic else "")
    site = website_domain(facts.website.value)
    if site and site in (facts.website.quote or "").lower():
        add("website", site, facts.website)       # not from "available at Marimekko's website"
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
        if b.items and not percent_items(b):
            unit = " ".join(x for x in (b.currency, b.unit if b.unit != "units" else "") if x) \
                or ("employees" if name.startswith("staff") else "")
            add(name, _breakdown(b), b, unit=unit, extra=b.basis or "")
    return out


# Stock indices the AI gives as an exchange segment, though the prompt rules them out.
STOCK_INDEX = re.compile(r"\b(FTSE|M?DAX|SDAX|TecDAX|OBX|OMX\w*|SMI|SPI|CAC|AEX|STOXX|S&P|"
                         r"index|indices)\b", re.I)

# A share count that already excludes treasury shares.
OUTSTANDING_WORDS = re.compile(r"outstanding|excluding|excl\.|net of|in circulation|utestående|"
                               r"utestaende|udestående|ulkona olev|exkl", re.I)


def percent_items(b) -> bool:
    """A breakdown whose figures the quote prints as percentages ("69 percent work in R&D")."""
    q = b.quote or ""
    return any(re.search(rf"(?<![\d.,]){re.escape(fmt_number(i.value))}\s*(%|percent|per cent|"
                         rf"procent|prosent|prosenttia)", q, re.I) for i in b.items)


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
    fields = {FACT_FIELD.get(g, g) for g in gaps}
    if "shares_outstanding" in gaps:
        fields.add("treasury_shares")         # code subtracts them from shares issued
    return sorted(fields & set(DataPointFacts.model_fields))


# Always read from the report, even when an API gave them: identity_check compares the
# legal name and country; the report's ticker keeps the exchange's spelling ("VOLV B",
# where OpenFIGI gives "VOLVB").
IDENTITY_FIELDS = ("legal_name", "country_code", "ticker")


def report_gaps(chosen: dict[str, Found]) -> list[str]:
    """What the annual report's AI pass should look for: data points no API or tag
    gave, plus those with only a C-graded value (a FIRDS listing date)."""
    weak = [n for n, f in chosen.items() if f.confidence == "C" and n in DP_DOC_TYPES]
    return [n for n in NAMES if n in gap_list(chosen) or n in weak]


def doc_origin(doc: Document, first_id: int) -> Origin:
    """A fallback document as an Origin, its chunk ids starting at first_id."""
    chunks = {first_id + i: Chunk(first_id + i, c.text, c.pages)
              for i, c in enumerate(split_chunks(doc.pages))}
    date = str(doc.year) if doc.year else ""
    if doc.kind == "pdf":
        return Origin("pdf", doc.url, doc.source, "PARSE", doc.retrieved_at, doc.pages, chunks,
                      date=date, pdf=doc.path)
    return Origin("web", doc.url, doc.source, "SCRAPE", doc.retrieved_at, doc.pages, chunks,
                  {cid: doc.url for cid in chunks}, date=date)


def doc_chunks(origins: list[Origin], gaps: list[str]) -> list[Chunk]:
    """What the AI reads of each document: all of it when it is no longer than DOC_WORDS,
    of a longer one the best chunks per needed topic, the topics sharing that budget."""
    topics = sorted({FACT_TOPIC[g] for g in gaps})
    words = max(DOC_TOPIC_WORDS, DOC_WORDS // max(len(topics), 1))
    picked: dict[int, Chunk] = {}
    for o in origins:
        chunks = list(o.chunks.values())
        if sum(c.words for c in chunks) <= max(DOC_WORDS, DOC_TOPIC_WORDS):
            picked |= {c.id: c for c in chunks}
            continue
        for topic in topics:
            picked |= {c.id: c for c in select_chunks(chunks, topic, words)}
    return [picked[i] for i in sorted(picked)]


def from_documents(name: str, slug: str, site: str, gaps: list[str], lib: Library,
                   fc: FirecrawlClient, country: str | None = None) -> tuple[list[Found], list[str]]:
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
        requote.repair(facts, Bundle(origins), name, f"{slug}_docs_{key}")
        got = [f for f in from_facts(facts, Bundle(origins), country) if f.data_point in gaps]
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
        try:
            f = pay.ask_pay(name, o.url, chunks, what, key, o.pdf, o.page_text())
        except openai.LengthFinishReasonError:
            # the model's reasoning ran to the output limit (TWMA's parent accounts, which
            # have no executive pay table): this source gives no answer, the run goes on
            log.warning("Pay: the AI's answer about %s ran out of length; skipped", o.url)
            read.append(f"{o.source} (no usable AI answer)")
            continue
        read.append(o.source)
        year = fiscal_end_year(f.fiscal_year)
        if year and report_year and year < report_year and not given:
            # Shell: an investor-roadshow deck with the previous year's outcomes; Equinor:
            # the FY2024 remuneration report when the annual report is FY2025
            log.info("Pay: %s gives FY%s pay, the report is FY%s; skipped", o.url, year,
                     report_year)
            continue
        if pay.has_pay(f):
            # the amounts of roles found in a checked pay table come from the table
            facts = pay_tables.from_tables(name, f, o.pdf, chunks, o.page_text())
            origin = o
            requote.repair(facts, origin, name, f"{key}_pay")
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
                                     f"{slug}_pay_{hashlib.sha1(pdoc.url.encode()).hexdigest()[:12]}",
                                     policy_origin.pdf, policy_origin.page_text())
                requote.repair(policy, policy_origin, name,
                               f"{slug}_pay_{hashlib.sha1(pdoc.url.encode()).hexdigest()[:12]}_pay")
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
                     "the remuneration section of the company's annual report", report_key,
                     report.pdf, report.page_text())
    have = {pay._norm_title(r.role_title) for r in facts.roles}
    extra = [r for r in ar.roles
             if r.executive and r.is_aggregate and pay._norm_title(r.role_title) not in have]
    more = ar.model_copy(update={"roles": extra})
    if not extra or not pay.has_pay(more):
        return []
    requote.repair(more, report, name, f"{report_key}_pay_aggregates")
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


# Values that hold for a date or period: the yearly figures, plus who owns the company.
PERIODIC = YEARLY | {"largest_holders", "controlling_owner", "controlling_owner_name",
                     "ownership_type", "pe_stake_5pct"}


def with_report_period(values: list[Found], period_end: str | None) -> None:
    """A periodic value read from the annual report without its own date holds for the
    report's period end (EBITDA, the segment note, the shareholder table)."""
    for f in values:
        if period_end and not f.period_end and f.data_point in PERIODIC:
            f.period_end = period_end
            f.note += "; period end: the report's (no other date stated)"


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


OTHER_COMPANY = "possibly another company's report"


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
    why = "check: " + " and ".join(reasons) + f": {OTHER_COMPANY}"
    log.warning("Identity check: %s", why)
    for f in values:
        if f.source == source and f.method != "XBRL":
            f.confidence = "C"
            f.note = "; ".join(x for x in (f.note, why) if x)


PARENT_ACCOUNTS = "the parent company's consolidated accounts"
OWN_IDENTITY = {"legal_name", "business_id", "other_names", "country_code", "listing_status"}


def parent_group(values: list[Found]) -> list[Found]:
    """Values read from the parent's consolidated accounts that a holding company files
    (issue 6): its name and number are the parent's, so they are dropped; the figures
    are the parent's group, which holds this company, and the note says so."""
    parent = next((str(f.value) for f in values if f.data_point == "legal_name" and f.value), "")
    why = "group figures from the parent company's consolidated accounts" + (
        f" ({clip(parent, 60)})" if parent else "")
    kept = [f for f in values if f.data_point not in OWN_IDENTITY]
    for f in kept:
        if f.value not in (None, ""):
            f.note = "; ".join(x for x in (f.note, why) if x)
    return kept


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


# --- 1b. an annual report found outside the report step (issue 15) -------------------------

def sought_year(today: dt.date | None = None) -> int:
    """The fiscal year a run looks for: the last full year (FY2025 during 2026), as for
    ESEF filings (esef.is_recent)."""
    return (today or dt.date.today()).year - 1


def report_year(result: dict | None) -> int | None:
    return fiscal_end_year(str((result or {}).get("fiscal_year") or ""))


def lacks_report(result: dict | None) -> bool:
    """The report step read no annual report, or one for a year before the one sought."""
    year = report_year(result)
    return result is None or (year is not None and year < sought_year())


def share_conversion(slug: str, url: str) -> None:
    """A PDF converts once: the report step (scraper.fetch_report) and the document
    library (documents.Library) cache it under different names; copy whichever exists to
    the other (a 177-page report takes minutes to convert)."""
    report, doc = CACHE_DIR / cache_stem(slug, url), CACHE_DIR / doc_stem(slug, url)
    for src, dst in ((doc, report), (report, doc)):
        if src.with_suffix(".md").exists() and not dst.with_suffix(".md").exists():
            if src.with_suffix(".pdf").exists():
                shutil.copyfile(src.with_suffix(".pdf"), dst.with_suffix(".pdf"))
            shutil.copyfile(src.with_suffix(".md"), dst.with_suffix(".md"))


def use_as_report(t: Target, url: str, site: str | None, fc: FirecrawlClient,
                  how: str) -> dict | None:
    """Run the report step on a document found outside it: it reads the fiscal year, its
    end and the core figures as for any report, and its result replaces the report
    step's (a failure, or an older year's report). None when the document gives no
    usable report, or no newer year than the result it would replace."""
    c = t.company
    old = json.loads(c.result_path.read_text(encoding="utf-8")) if c.result_path.exists() else None
    share_conversion(c.slug, url)
    log.info("Report step on %s (%s)", url, how)
    try:
        result = run_report(c.name, website=site, report_url=url, use_cache=True, lei=c.lei,
                            company_id=c.company_id, country=c.country, fc=fc,
                            qualitative=False)
    except FATAL:
        raise
    except Exception as e:  # noqa: BLE001 - the run goes on as without this document
        log.warning("Report step on %s failed: %s", url, str(e)[:200])
        return None
    share_conversion(c.slug, url)
    new_year, old_year = report_year(result), report_year(old)
    if old and old_year and (new_year is None or new_year <= old_year):
        log.info("%s is FY%s, not newer than the report read before (FY%s); kept that one",
                 url, new_year, old_year)
        c.result_path.write_text(json.dumps(old, indent=2, ensure_ascii=False), encoding="utf-8")
        return None
    result.pop("_output_path", None)
    if not site:
        # run() takes the report's host for the website (image.tallink.com): unknown instead
        result["website"], result["website_source"] = None, None
    result["report_source"] = how
    c.result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    c.error_path.unlink(missing_ok=True)
    log.info("Annual report: FY%s from %s (%s)", result.get("fiscal_year"), url, how)
    return result


def report_files(c: Company) -> dict[Path, str | None]:
    """The report step's result and error files as they are, for restore_files."""
    return {p: p.read_text(encoding="utf-8") if p.exists() else None
            for p in (c.result_path, c.error_path)}


def restore_files(saved: dict[Path, str | None]) -> None:
    for p, text in saved.items():
        if text is None:
            p.unlink(missing_ok=True)
        else:
            p.write_text(text, encoding="utf-8")


def find_annual_report(lib: Library, year: int) -> Document | None:
    """The company's annual report for `year` among its documents: a candidate dated
    `year` or later (or undated), fetched, and plainly that report (documents.title_year:
    tens of pages, "Annual report 2025" on its cover). A web page that isn't (a reports
    page) still adds its links, so the second try can be the PDF it links to."""
    def recent(cand: Candidate) -> bool:
        return cand.year is None or cand.year >= year
    for _ in range(2):
        doc = lib.find("annual_report", accept=recent)
        if doc is None:
            return None
        found = title_year(doc.pages)
        if found and found >= year:
            return doc
        log.info("Documents: %s is not the FY%s annual report (%s)", doc.url, year,
                 f"FY{found}" if found else "no annual-report title with a year on its cover")
    return None


def known_website(result: dict | None, slug: str) -> str | None:
    """The website found before (the report step's or its search cache), no lookup."""
    if result and result.get("website"):
        return result["website"]
    disc = CACHE_DIR / f"{slug}_discovery.json"
    if disc.exists():
        return json.loads(disc.read_text(encoding="utf-8")).get("website")
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
        elif name == "sector_code":
            # classified from the business description (sector.py), else a register's code
            why = ("not found: no business description to classify, and no register code"
                   + (f" (tried: {', '.join(tried)})" if tried else ""))
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
    in_eur, at = cap, ""
    # a year-end price read without its date: the report's fiscal year end dates it
    fye = getattr(chosen.get("fiscal_year_end"), "value", "") or ""
    date = price.period_end or (str(fye) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fye)) else "")
    if price.unit != "EUR":
        # The ECB's euro rate on the price's date (the last working day before it)
        rate = fx.eur_rate(price.unit, date)
        if not rate:
            return None, (f"not derived: market cap {cap:,.0f} {price.unit}; no ECB euro rate "
                          f"for {price.unit} on {date or 'an unknown date'}")
        in_eur = cap / rate[0]
        at = f", {cap:,.0f} {price.unit} at {rate[0]:g} {price.unit} per EUR ({fx.SOURCE}, {rate[1]})"
        if not price.period_end:
            at += f"; the price has no date: the rate of the fiscal year end {date}"
    band = next(name for floor, name in MARKET_CAP_BANDS_EUR if in_eur >= floor)
    worst = min((shares, price), key=lambda f: CONFIDENCE_RANK[f.confidence])
    return Found("market_cap_band", band, unit="", period_end=price.period_end or date,
                 source="derived", endpoint=price.endpoint, method="DERIVED",
                 confidence=worst.confidence,
                 note=f"market cap {in_eur:,.0f} EUR = shares outstanding x share price{at} "
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


def read_report(t: Target, result: dict, lei_record: dict | None, values: list[Found],
                sel: frozenset[str] | None = None) -> tuple[Origin | None, list[Found]]:
    """Step 2: the figures the report step read (tags or the report), then one AI pass over
    the report for what they and the APIs (`values`) left open, and a C-graded value,
    which a quoted one beats; only for the selected data points (`sel`). The report's own
    legal name and country are always asked for, for the identity check. Returns the
    report and its values."""
    c = t.company
    origin = report_origin(result)
    tagged = from_result(result, origin)
    out = parent_group(tagged) if origin and PARENT_ACCOUNTS in origin.source else tagged
    gaps = [g for g in report_gaps(best(values + out)) if selection.wants(sel, g)]
    chunks = report_chunks(origin, gaps) if origin and gaps else []
    if not chunks:
        return origin, out + year_of_report(result, origin, out)
    log.info("Data points: asking the AI about %d report chunks for %d open data point(s)",
             len(chunks), len(gaps))
    facts = ask(c.name, origin.url, chunks, "the company's annual report",
                Path(result["debug"]["markdown_file"]).stem,
                wanted_fields(gaps + list(IDENTITY_FIELDS)))
    requote.repair(facts, origin, c.name, Path(result["debug"]["markdown_file"]).stem)
    report_values = from_facts(facts, origin, (lei_record or {}).get("country") or c.country)
    if not result.get("period_end_date"):
        # the report step gave no period end: the fiscal year end the report states
        # dates its values (and the pay rows) instead
        result["period_end_date"] = next(
            (f.value for f in report_values if f.data_point == "fiscal_year_end"
             and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(f.value or ""))), None)
    with_report_period(report_values, result.get("period_end_date"))
    if PARENT_ACCOUNTS in origin.source:
        report_values = parent_group(report_values)
    else:
        # The LEI record's legal country first: the input's country can be the listing
        # market (2020 Bulkers: listed in Norway, registered in Bermuda).
        identity_check(report_values + values + out,
                       (lei_record or {}).get("country") or c.country,
                       [c.name, (lei_record or {}).get("legal_name") or ""], origin.source)
    return origin, out + report_values + year_of_report(result, origin, out + report_values)


def year_of_report(result: dict, origin: Origin | None, have: list[Found]) -> list[Found]:
    """The fiscal year when the report step gave none (Commerzbank's report: no figures read,
    no year): from the year end the report states (2025-12-31 -> 2025; 2026-03-31 -> 2025/26),
    else from the title on its cover ("Geschäftsbericht 2025"). Sets it in `result` too, for
    the pay step. [] when the year is known or not to be found."""
    if result.get("fiscal_year") or origin is None or any(f.data_point == "fiscal_year" for f in have):
        return []
    end = str(result.get("period_end_date") or "")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", end):
        day = dt.date.fromisoformat(end)
        year = str(day.year) if day.month > 6 else f"{day.year - 1}/{str(day.year)[2:]}"
        how = f"derived: the fiscal year ending {end}, the year end the report states"
    elif title := title_year(origin.pages):
        year, how = str(title), f"derived: the year in the report's title ({origin.source})"
    else:
        return []
    result["fiscal_year"] = year
    return [Found("fiscal_year", year, period_end=end, source=origin.source,
                  endpoint=origin.url.split("#")[0], method="DERIVED", confidence="B", note=how,
                  retrieved_at=result.get("extracted_at") or "")]


def collect(t: Target, docs: bool = True, doc_credits: int = DEFAULT_DOC_CREDITS,
            error: str | None = None, flags: set | None = None,
            meter: dict | None = None, use_apis: bool = True) -> list[Found]:
    """`error`: why the annual-report pipeline has no result (if not in its error file).
    `flags` gets "no_credits" when Firecrawl refused for lack of credits; `meter`
    gets "credits", the Firecrawl credits spent here. Only the data points of
    `t.fields` are looked for (None: all); the rows of the others are not for saving."""
    c = t.company
    sel = t.fields
    flags = flags if flags is not None else set()
    meter = meter if meter is not None else {}
    result = json.loads(c.result_path.read_text(encoding="utf-8")) if c.result_path.exists() else None
    if result is None and c.error_path.exists():
        e = json.loads(c.error_path.read_text(encoding="utf-8"))
        error = f"{e.get('error_type')}: {e.get('error')}"
    values: list[Found] = []
    tried: list[str] = []
    want_report = selection.needs_report(sel)

    # 1. the annual-report pipeline
    lei_record = (result or {}).get("lei_record")
    if result is None:
        try:
            lei_record = identify_lei(c.name, c.slug, c.lei, True, c.country)["record"]
        except Exception as e:  # noqa: BLE001
            log.warning("LEI lookup failed: %s", e)
    if not c.lei and (lei_record or {}).get("lei"):
        c.lei = lei_record["lei"]

    # 1b. the report step found no report of the year, but the input names one (issue 15:
    # Tallink's report step chose an AGM board report; its annual report was in the input)
    supplied = readable(t.annual_report_url)
    if want_report and supplied and not local_file(supplied) and lacks_report(result):
        pfc = FirecrawlClient(load_settings(), max_credits=1)    # a PDF downloads for free
        found = use_as_report(t, supplied, known_website(result, c.slug), pfc,
                              "annual_report_url in the input")
        meter["pipeline"] = meter.get("pipeline", 0) + pfc.credits.total
        if found:
            result, error = found, None
            lei_record = result.get("lei_record") or lei_record

    gleif_isins: list[str] = []
    if use_apis:
        # 0. the official APIs first; the documents below fill what they leave empty
        api_values, answered, gleif_isins = from_apis(t, result, lei_record)
        values += api_values
        tried += answered

    # 2. the report: its figures, then the AI pass for what the APIs and tags left open
    origin, from_report = (read_report(t, result, lei_record, values, sel)
                           if result and want_report else (None, []))
    values += from_report
    report_label = None
    if result and want_report:
        report_label = origin.source if origin else "annual report"
        tried.append(report_label)

    fc = lib = site = None
    roles: list[Found] = []
    roles_why = ""
    try:
        if docs and selection.needs_documents(sel):
            fc = FirecrawlClient(load_settings(), max_credits=doc_credits)
            site = website_for(t, result, lei_record, fc)
            if site:
                year = str((result or {}).get("fiscal_year") or "")
                lib = Library(c.slug, site, int(year) if year.isdigit() else None, fc,
                              skip_urls=[(result or {}).get("report_url")])

        # 2b. still no report of the year: look for it among the company's documents (a
        # report the search missed, linked elsewhere on the site), and read it as the report
        if lib and want_report and lacks_report(result):
            doc = find_annual_report(lib, sought_year())
            saved = report_files(c)
            found = use_as_report(t, doc.url, site, fc, "found among the company's documents") \
                if doc else None
            if found:
                # the older year's report gives way: its values and its place in `tried`
                stale = {id(f) for f in from_report}
                others = [f for f in values if id(f) not in stale]
                new_origin, new_values = read_report(t, found, lei_record, others, sel)
                if any(OTHER_COMPANY in f.note for f in new_values):
                    # a report on the company's site by another company (Jinhui Shipping's
                    # site has its Hong Kong parent's): not used; a supplied one is trusted
                    log.warning("Annual report %s fails the identity check; not used", doc.url)
                    restore_files(saved)
                else:
                    if report_label in tried:
                        tried.remove(report_label)
                    result, error, origin, from_report = found, None, new_origin, new_values
                    values = others + from_report
                    lib.report_year = report_year(result)
                    tried.append(origin.source if origin else "annual report")

        chosen = best(values)
        listed = chosen.get("listing_status")
        unlisted = bool(listed and listed.value == "unlisted")
        roles_why = ("not applicable: the company is not listed" if unlisted
                     else "" if selection.needs_pay(sel)
                     else selection.NOT_COLLECTED + selection.label(sel))

        # 3. executive pay (role grain) and the company-level pay terms
        if not unlisted and selection.needs_pay(sel):
            fy = fiscal_end_year(str((result or {}).get("fiscal_year") or ""))
            roles, terms, read = from_pay(
                c.name, c.slug, lib, origin,
                Path(result["debug"]["markdown_file"]).stem if origin else "",
                (result or {}).get("period_end_date") or "",
                (lei_record or {}).get("country") or c.country, fy,
                tuple((u, label) for u, label in ((readable(t.remuneration_report_url), "Remuneration report"),
                                                  (readable(t.annual_report_url), "Annual report")) if u),
                next((int(f.value) for f in values if f.data_point == "cik" and f.value), None))
            values += terms
            tried += [r for r in read if r not in tried]
            if not roles:
                roles_why = ("not found in: " + ", ".join(read) if read
                             else "no remuneration report found")

        # 4. document fallback for the company-grain data points still missing
        chosen = best(values)
        gaps = [g for g in gap_list(chosen) if selection.wants(sel, g)]
        if lib and gaps:
            log.info("Document fallback on %s for: %s", site, ", ".join(gaps))
            found, read = from_documents(c.name, c.slug, site, gaps, lib, fc,
                                         (lei_record or {}).get("country") or c.country)
            values += found
            tried += list(dict.fromkeys(read)) or ["company documents (none usable found)"]
    except PaymentRequiredError:
        flags.add("no_credits")
        tried.append(f"company documents (skipped: {NO_CREDITS})")
        roles_why = roles_why or f"remuneration report not searched: {NO_CREDITS}"
    if fc:
        log.info("Documents used %d Firecrawl credit(s)", fc.credits.total)
        meter["credits"] = fc.credits.total
    chosen = best(values)
    parent = chosen.get("ultimate_parent")
    if parent and any(same_company(parent.value, n) for n in
                      (c.name, getattr(chosen.get("legal_name"), "value", ""))):
        del chosen["ultimate_parent"]          # the company itself: it is the top of its group
    # The sector from the business description, the client's route (issue 7); the
    # register's code, often the holding company's, stays in the note.
    classified = sector.from_description(chosen, c.name) \
        if selection.wants(sel, "sector_code") else None
    if classified:
        chosen["sector_code"] = classified
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
                     else "", "confidence": f.confidence, "note": f.note,
                     "scraper_version": str(SCRAPER_VERSION)})
    return refresh(rows)


def dp_path(c: Company) -> Path:
    return DP_DIR / f"{c.slug}.json"


def saved_version(c: Company) -> int:
    """The scraper version a company's saved values were extracted with (0: before versioning)."""
    try:
        rows = json.loads(dp_path(c).read_text(encoding="utf-8"))
        return min(int(r.get("scraper_version") or 0) for r in rows) if rows else 0
    except (OSError, ValueError):
        return 0


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
    if selection.needs_report(t.fields) and needs_pipeline(c, opts):
        res = process_company(c, False, opts["pipeline_credits"], qualitative=False)
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
    rows = save_rows(t, rows_for(t, found))
    if "no_credits" in flags:
        no_credits_path(c).write_text(NO_CREDITS, encoding="utf-8")
    else:
        no_credits_path(c).unlink(missing_ok=True)
    mine = [r for r in rows if t.fields is None or r["data_point"] in t.fields]
    return {"kind": "done", "no_credits": "no_credits" in flags,
            "found": sum(1 for r in mine if r["value"]), "total": len(mine),
            "fields": selection.label(t.fields),
            "seconds": time.monotonic() - started, "credits": spent(meter)}


def save_rows(t: Target, rows: list[dict]) -> list[dict]:
    """Write a company's rows; a run limited to some data points (t.fields) replaces only
    those in the rows saved before (fields.merge). Returns the rows saved."""
    path = dp_path(t.company)
    if t.fields is not None:
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        rows = selection.merge(old, rows, t.fields)
    DP_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    return rows


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
    if c.report_url and c.result_path.exists():
        # a supplied report replaces the one found before (from_reports.py): the new
        # run overwrites the result
        done = json.loads(c.result_path.read_text(encoding="utf-8")).get("report_url")
        if done != c.report_url:
            return True
    return not c.result_path.exists() and (not c.error_path.exists() or opts["retry_failed"]
                                           or no_credits_path(c).exists())


def worst_case(t: Target, opts: dict) -> int:
    """The most Firecrawl credits one company can spend (both caps hold per company), for
    the steps its selected data points need (t.fields)."""
    return sum(credits for _, credits in plan(t, opts))


def plan(t: Target, opts: dict) -> list[tuple[str, int]]:
    """The steps a company's run takes, each with its worst-case Firecrawl credits."""
    c, sel = t.company, t.fields
    steps = [("official APIs", 0)] if opts.get("apis", True) else []
    if selection.needs_report(sel):
        if needs_pipeline(c, opts):
            # a report supplied on disk needs no search: the report step spends nothing
            local = bool(c.report_url and local_file(c.report_url))
            steps.append(("report step (file given)" if local else "report search",
                          0 if local else opts["pipeline_credits"]))
        elif c.result_path.exists():
            steps.append(("report (found before)", 0))
        else:
            steps.append(("report (failed before; --retry-failed searches again)", 0))
        url = readable(t.annual_report_url)
        if url and not local_file(url) and lacks_report(_saved_result(c)):
            steps.append(("annual_report_url as the report", 0 if is_pdf_url(url) else 1))
        steps.append(("report AI pass", 0))
    docs = opts["docs"] and selection.needs_documents(sel)
    if selection.needs_pay(sel):
        steps.append(("executive pay", 0))
    if docs:
        steps.append(("company documents (pay, fallback)", opts["doc_credits"]))
    return steps


def _saved_result(c: Company) -> dict | None:
    try:
        return json.loads(c.result_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# --- outputs --------------------------------------------------------------------------------

# Facts that hold until they change: their date is the one they were read for.
OWNERSHIP = {"largest_holders", "controlling_owner", "controlling_owner_name", "ownership_type",
             "pe_stake_5pct", "ultimate_parent"}
REPORT_SOURCES = ("Annual report", "ESEF filing")


def _fy_label_fits(label: str, end: dt.date) -> bool:
    """Does a fiscal-year label name the year that ends on `end`? "2025" for a year ending
    31 Dec 2025; "2025/26" or "2025/2026" for one ending in 2026; "2025" also for a year
    ending in the first half of 2026 (Burckhardt names its year after the year it starts)."""
    years = [int(y) for y in re.findall(r"(?<!\d)(\d{4})(?!\d)", label)]
    m = re.search(r"(\d{4})\s*[/-]\s*(\d{2})(?!\d)", label)
    if m:
        years.append(int(m.group(1)[:2] + m.group(2)))
    if not years:
        return True                     # nothing to compare
    last = max(years)
    return last == end.year or (len(set(years)) == 1 and end.month <= 6 and last == end.year - 1)


def fiscal_year_from_its_end(rows: list[dict]) -> None:
    """The fiscal year the AI named, put right where the report's own fiscal year end says
    another year (Basler Kantonalbank: "2023" for the 2025 report, figures dated 2025-12-31).
    Values that took the wrong year's end as their date get the right one: those dated
    "the report's (no other date stated)", and pay rows from that report or whose quote
    names the new year, unless the quote names the old one."""
    co = [r for r in rows if r["grain"] == "company"]
    fy = next((r for r in co if r["data_point"] == "fiscal_year" and r["value"]), None)
    fye = next((r for r in co if r["data_point"] == "fiscal_year_end"
                and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["value"])), None)
    if not fy or not fye:
        return
    end = dt.date.fromisoformat(fye["value"])
    if _fy_label_fits(fy["value"], end):
        return
    old, old_end = fy["value"], fy["period_end"]
    new = str(end.year) if end.month > 6 else f"{end.year - 1}/{str(end.year)[2:]}"
    fy.update(value=new, period_end=fye["value"],
              note=f"{fy['note']}; the AI said {old}, the report's fiscal year ends {fye['value']}")
    if not old_end or old_end == fye["value"]:
        return
    old_year, new_year = old_end[:4], str(end.year)
    report = fye["endpoint"].split("#")[0]
    for r in rows:
        if r is fy or r["period_end"] != old_end or not r["value"]:
            continue
        m = re.search(r'(?:PDF page \d+|report text|web page): "([^"]*)', r["note"])
        quote = m.group(1) if m else ""
        if "period end: the report's (no other date stated)" in r["note"] or (
                r["grain"] == "role" and old_year not in quote
                and (new_year in quote or (report and r["endpoint"].split("#")[0] == report))):
            r["period_end"] = fye["value"]
            r["note"] += f"; dated {fye['value']}, the report's fiscal year end (was {old_end})"


def iso_codes(rows: list[dict]) -> None:
    """Currencies as ISO 4217 codes: "US$" -> "USD" in a currency field and at the start of
    a unit ("US$ millions"). A share price in pence (GBp, GBX) becomes pounds, the printed
    pence kept in the note for the quote check."""
    for r in rows:
        country = r.get("country", "")
        if r["data_point"] in ("pay_currency", "reporting_currency") and r["value"]:
            r["value"] = iso_currency(r["value"], country)
        if r["data_point"] == "share_price" and r["unit"] in ("GBp", "GBX") \
                and re.fullmatch(r"-?[\d.]+", r["value"]):
            pence = r["value"]
            r["value"], r["unit"] = fmt_number(float(pence) / 100), "GBP"
            r["note"] = f"{r['note']}; printed {pence} pence" if r["note"] else f"printed {pence} pence"
        if r["unit"]:
            head, _, rest = r["unit"].partition(" ")
            code = iso_currency(head, country)
            if code != head:
                r["unit"] = f"{code} {rest}".strip()


FROM_FTE = "derived: full-time equivalents (no headcount stated)"


def headcount_from_fte(by: dict[str, dict]) -> None:
    """No headcount but an FTE count: the FTE count, rounded, is the headcount (the closest
    size measure the company states; decided 11 Nov 2026), method DERIVED, its note
    saying so. `by`: a company's rows by data point."""
    hc, fte = by.get("headcount"), by.get("fte")
    if not hc or hc["value"] or not fte or not fte["value"] or hc["note"].startswith(selection.NOT_COLLECTED):
        return
    try:
        n = float(fte["value"])
    except ValueError:
        return
    whole = int(n + 0.5)                 # half up (round() gives 1234 for 1234.5)
    if whole < 1:
        return
    how = FROM_FTE if whole == n else f"{FROM_FTE}, rounded from {fte['value']}"
    printed = "" if whole == n or "printed " in fte["note"] else f"printed {fte['value']}; "
    hc.update({k: fte[k] for k in ("unit", "period_end", "source", "endpoint", "retrieved_at",
                                   "confidence", "scraper_version")},
              value=str(whole), method="DERIVED", note=f"{how}; {printed}{fte['note']}")


VARIABLE_PAY = ("sti_paid", "sti_target", "sti_max", *pay.LTIS, "lti_target", "lti_max")
NO_VARIABLE_PAY = "not applicable: no variable pay (the total is fixed pay only)"


def no_variable_pay(mine: dict[str, dict]) -> None:
    """A role paid only fixed pay (2invest's sole board member: 72,000 salary, total 72,000):
    its total is base salary + benefits + pension, and no bonus figure was read. Then the
    empty STI and LTI rows say so instead of "not found". `mine`: a role's rows by data point."""
    def amount(k):
        r = mine.get(k)
        try:
            return float(r["value"]) if r and r["value"] else None
        except ValueError:
            return None
    base, total = amount("base_salary"), amount("total_remuneration")
    if not base or not total or any(mine.get(k, {}).get("value") for k in VARIABLE_PAY):
        return
    fixed = base + (amount("benefits_value") or 0) + (amount("pension_contribution") or 0)
    if not (base <= total and abs(total - fixed) <= 0.01 * total):
        return
    for k in VARIABLE_PAY:
        r = mine.get(k)
        if r and not r["value"] and r["note"].startswith("not found"):
            r["note"] = NO_VARIABLE_PAY


def refresh(rows: list[dict]) -> list[dict]:
    """A company's saved rows under the current rules, without asking any source again:
    the market-cap band where only the euro rate was missing, and a date for a pay term
    or an ownership fact read without one. Rows that already have them are unchanged."""
    for r in rows:
        r.setdefault("scraper_version", "0")    # saved before versioning
    iso_codes(rows)
    fiscal_year_from_its_end(rows)
    by = {r["data_point"]: r for r in rows if r["grain"] == "company"}
    headcount_from_fte(by)
    band = by.get("market_cap_band")
    if band and not band["value"] and band["note"].startswith("not derived: market cap"):
        names = [f.name for f in fields(Found)]
        chosen = {k: Found(**{n: by[k][n] for n in names if n in by[k]})
                  for k in ("shares_outstanding", "share_price", "fiscal_year_end")
                  if by.get(k, {}).get("value")}
        new, why = market_cap_band(chosen)
        if new:
            band.update({k: v for k, v in asdict(new).items() if k in band}, retrieved_at=_now())
        else:
            band["note"] = why
    names = [f.name for f in fields(Found)]
    for role in dict.fromkeys(r["role_row"] for r in rows if r["grain"] == "role"):
        no_variable_pay({r["data_point"]: r for r in rows
                         if r["grain"] == "role" and r["role_row"] == role})
        mine = {r["data_point"]: r for r in rows if r["grain"] == "role" and r["role_row"] == role
                and r["data_point"] in pay.TARGETS}
        have = {k: Found(**{n: r[n] for n in names if n in r}) for k, r in mine.items() if r["value"]}
        if not have:
            continue
        for k, r in mine.items():
            if isinstance(have.get(k), Found):
                have[k].value = float(r["value"]) if re.fullmatch(r"-?[\d.]+", r["value"]) else r["value"]
        before = {k: id(v) for k, v in have.items()}
        pay.misread_targets(have)
        for k, r in mine.items():
            if k in have and before.get(k) != id(have[k]):
                r.update({**{n: v for n, v in asdict(have[k]).items() if n in r},
                          "value": pay._num(have[k].value)})
            elif k not in have and r["value"]:
                r.update(value="", unit="", method="", confidence="", retrieved_at="",
                         note="dropped: a target read from its maximum's quote, or above the maximum")
    pay_end = next((r["period_end"] for r in rows if r["grain"] == "role" and r["period_end"]), "")
    report_end = (by.get("fiscal_year_end") or {}).get("value") or ""
    for r in rows:
        if r["grain"] != "company" or not r["value"] or r["period_end"]:
            continue
        if r["data_point"] in LISTED_REPORTS_ONLY and pay_end:
            r["period_end"], why = pay_end, "the pay year's"
        elif r["data_point"] in OWNERSHIP and report_end and r["source"].startswith(REPORT_SOURCES):
            r["period_end"], why = report_end, "the report's"
        elif r["data_point"] in OWNERSHIP and r["retrieved_at"]:
            r["period_end"], why = r["retrieved_at"][:10], "the day it was read"
        else:
            continue
        r["note"] += f"; period end: {why} (no other date stated)"
    return rows


def write_csv(targets: list[Target], out: Path) -> int:
    from .output_checks import Sources          # imports this module
    sources = Sources(CACHE_DIR, OUTPUT_DIR)
    n = 0
    tmp = out.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for t in targets:
            p = dp_path(t.company)
            if p.exists():
                rows = refresh(json.loads(p.read_text(encoding="utf-8")))
                repair_quotes(rows, sources.pages)
                for row in rows:
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
    p.add_argument("--outdated", action="store_true",
                   help=f"Also redo companies whose values came from an older scraper version "
                        f"(now {SCRAPER_VERSION}; column scraper_version)")
    p.add_argument("--no-dashboard", action="store_true",
                   help="Don't run the output checks and update the dashboard at the end")
    p.add_argument("--fields",
                   help="Only these data points, comma-separated: names (revenue,headcount) or "
                        f"groups ({', '.join(selection.GROUPS)}). Only they are replaced in the "
                        "company's saved rows. Companies done before run again when one of "
                        "them has no value (or with --redo)")
    p.add_argument("--ignore-run-required", action="store_true",
                   help="Collect every data point whatever the input's run_required says "
                        "('Pay Data': the pay fields only; 'Company Data': the company fields only)")
    p.add_argument("--dry-run", action="store_true",
                   help="Show each company's steps and worst-case Firecrawl credits; run nothing")
    args = p.parse_args(argv)

    OUTPUT_DIR.mkdir(exist_ok=True)
    _setup_logging()
    try:
        everyone = read_targets(args.csv)
        cli_fields = selection.parse(args.fields)
    except (OSError, ValueError, csv.Error) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    targets = everyone
    if args.only:
        wanted = {x.strip() for x in args.only.split(",")}
        targets = [t for t in targets if t.company.company_id in wanted]
    if args.limit:
        targets = targets[:args.limit]
    nothing = []
    for t in targets:
        required = None if args.ignore_run_required else selection.from_run_required(t.run_required)
        t.fields = selection.combine(cli_fields, required)
        if t.fields is not None and not t.fields:
            nothing.append(t)
    if nothing:
        print(f"{len(nothing)} companies skipped: --fields asks for nothing their run_required "
              f"needs ({', '.join(t.company.company_id for t in nothing[:5])}"
              f"{', ...' if len(nothing) > 5 else ''})")
        targets = [t for t in targets if t not in nothing]

    def due(t: Target) -> bool:
        c = t.company
        if (args.redo or not dp_path(c).exists() or no_credits_path(c).exists()
                or (args.outdated and saved_version(c) < SCRAPER_VERSION)):
            return True
        # --fields tops up: a company runs again when a field asked for has no value
        return cli_fields is not None and bool(selection.missing(
            json.loads(dp_path(c).read_text(encoding="utf-8")), t.fields))
    todo = [t for t in targets if due(t)]
    print(f"{len(targets)} companies from {args.csv}; {len(targets) - len(todo)} done before"
          + (f" with scraper version {SCRAPER_VERSION}" if args.outdated else "")
          + (f" with {selection.label(cli_fields)}" if cli_fields is not None else ""))
    opts = {"docs": not args.no_docs, "doc_credits": args.doc_credits, "apis": not args.no_apis,
            "pipeline_credits": args.pipeline_credits, "retry_failed": args.retry_failed}
    problems = {t.company.company_id: input_problems(t) for t in todo}
    if args.dry_run:
        dry_run(todo, opts, problems)
        return 0
    flagged = sum(1 for p in problems.values() if p)
    if flagged:
        print(f"Input: {flagged} companies with a problem in the input (--dry-run lists them)")
    worst = sum(worst_case(t, opts) for t in todo)
    if args.max_run_credits is None and worst:
        print(f"No --max-run-credits cap: this run could use up to {worst} Firecrawl credits")
    code_at_start = code_fingerprint()

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
                code_at_start = warn_if_code_changed(code_at_start)
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
                        code_at_start = warn_if_code_changed(code_at_start)
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
    if not args.no_dashboard and code != 2:
        from . import dashboard          # imports output_checks, which imports this module
        try:
            print(f"Checks and dashboard updated: {dashboard.build(args.out)}")
        except Exception as e:  # noqa: BLE001 - a report problem must not hide the run's result
            log.warning("Could not update the checks report and dashboard: %s", e)
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


def dry_run(todo: list[Target], opts: dict, problems: dict | None = None) -> None:
    """--dry-run: per company, the fields asked for, the steps and their worst case, and
    any problem in its input."""
    total = 0
    problems = problems or {}
    for i, t in enumerate(todo, 1):
        steps = plan(t, opts)
        credits = sum(n for _, n in steps)
        total += credits
        print(f"[{i}/{len(todo)}] {t.company.company_id} {t.company.name}: "
              f"fields {selection.label(t.fields)}"
              + (f" (run_required: {t.run_required})" if t.run_required else ""))
        print("    " + "; ".join(f"{s} ({n} credits)" if n else s for s, n in steps)
              + f"; worst case {credits} credits")
        for p in problems.get(t.company.company_id, []):
            print(f"    INPUT: {p}")
    flagged = sum(1 for p in problems.values() if p)
    print(f"\nDry run: {len(todo)} companies, at most {total} Firecrawl credits "
          f"(caps per company; most companies spend far less)"
          + (f"; {flagged} with an input problem (INPUT lines)" if flagged else ""))


# Hosts whose links need a login: the tool can't open them and searches instead (Wave 1's
# Google Drive links)
LOGIN_HOSTS = ("drive.google.com", "docs.google.com", "sharepoint.com", "onedrive.live.com",
               "1drv.ms", "dropbox.com", "box.com")


def needs_login(url: str | None) -> bool:
    host = urlparse(url or "").netloc.lower()
    return bool(url) and any(host == h or host.endswith("." + h) for h in LOGIN_HOSTS)


def readable(url: str | None) -> str | None:
    """A supplied link, unless it needs a login: a Google Drive link gives a sign-in or
    viewer page, never the file (DACH Set 2: Edisun's viewer page was read as its "FY2023
    report"). The document is then searched for instead."""
    return None if needs_login(url) else url


def input_problems(t: Target) -> list[str]:
    """What in a company's input row will cost it: a report link the tool can't open, or no
    LEI and no ISIN (the company is then found by name only, and an official filing can't
    be looked up by its LEI)."""
    out = []
    for label, url in (("annual_report_url", t.annual_report_url),
                       ("remuneration_report_url", t.remuneration_report_url)):
        host = urlparse(url or "").netloc.lower()
        if needs_login(url):
            out.append(f"{label} needs a login ({host}): searched for instead; give a direct link to the PDF")
    if not t.company.lei and not t.isin:
        out.append("no LEI and no ISIN: found by name only")
    return out


def code_fingerprint() -> str:
    """The code and prompts a run started with (their files' sizes and times)."""
    root = Path(__file__).resolve().parent
    files = sorted(list(root.glob("*.py")) + list((root.parent / "prompts").glob("*.md")))
    return hashlib.sha1("|".join(f"{f.name}:{f.stat().st_size}:{f.stat().st_mtime_ns}"
                                 for f in files).encode()).hexdigest()


def warn_if_code_changed(at_start: str) -> str:
    """A run whose code or prompts change while it runs mixes versions: companies after the
    change ran (partly) with the new code, and a worker can load a half-edited module (FY2025
    run 5: two companies failed on an import error). Warn once; returns the new fingerprint."""
    now = code_fingerprint()
    if now != at_start:
        msg = ("WARNING: the code or prompts changed while this run is going; the companies "
               "that follow run with the changed code. Don't edit during a run.")
        print(msg, flush=True)
        log.warning(msg)
    return now


def _report(i: int, n: int, t: Target, res: dict) -> int:
    prefix = f"[{i}/{n}] {t.company.company_id} {t.company.name}"
    if res["kind"] == "done":
        fields = f" of {res['fields']}" if res.get("fields", "all") != "all" else ""
        print(f"{prefix}: {res['found']}/{res['total']} data points{fields} ({res['seconds']:.0f}s)"
              + (f" [{NO_CREDITS}: free sources only]" if res.get("no_credits") else ""), flush=True)
        return 0
    print(f"{prefix}: {res['kind'].upper()} {res.get('error', '')}", flush=True)
    return 2 if res["kind"] in ("fatal", "offline") else 0


if __name__ == "__main__":
    sys.exit(main())
