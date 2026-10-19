"""Every data point for a list of companies, one row per value, with the exact place
each value came from.

    python -m extractor.datapoints golden_test_sample_5_per_segment_country_all.csv
        [--workers 3] [--only ID,ID] [--limit N] [--retry-failed] [--redo] [--no-web]

Input: any CSV with company_id, company_name and (optional) segment, country, lei,
business_id. Several rows per company are fine (the golden sample has one row per
golden value); each company is processed once.

For each company, cheapest and most exact first:
  1. the annual-report pipeline (python -m extractor.batch): LEI, revenue and total
     assets (XBRL tags or the report), revenue model, business structure;
  2. official APIs: GLEIF (+ parents, ISINs), SEC EDGAR, Brønnøysund (NO),
     Companies House (UK), PRH (FI);
  3. one more LLM pass over the same report for the remaining facts (employees,
     owners, listing, pay, revenue and staff by country), each with a quote that is
     looked up in the report to find its page;
  4. HTML backup: data points still missing are looked for on the company's own web
     pages (Firecrawl map + scrape, at most --web-credits credits per company).

Output:
  output/datapoints.csv        one row per company and data point (15 columns)
  output/datapoints/<id>.json  the same rows per company (re-runs skip done companies)
  output/golden_test_filled.csv  the input CSV with build_value filled in, when the
                               input is the golden sample

Where a value came from:
  source      who published it (GLEIF, SEC EDGAR, Annual report (PDF), Company website...)
  endpoint    the exact URL: the API request, the filing, the PDF with #page=N, or the
              web page with a #:~:text= fragment that browsers scroll to
  method      API (register field), XBRL (tagged figure), PARSE (read from a filed
              document), SCRAPE (read from a web page), BUY (market data, not collected)
  confidence  A exact (register field or XBRL tag); B read by the AI, quote found in
              the source; C read by the AI, quote not found verbatim (check it)
  note        the page and quote, the tag name, or why there is no value
"""

import argparse
import csv
import datetime as dt
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

from . import apis, edgar, llm
from .apis import Found
from .batch import FATAL, Company, _KeepAwake, _setup_logging, _worker_init, process_company
from .config import CACHE_DIR, OUTPUT_DIR, load_settings
from .extract import full_value
from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from .pipeline import find_official_website, identify_lei
from .schemas import DataPointFacts, Holder, NumberFact, TextFact
from .scraper import Page, markdown_to_pages
from .sections import DATAPOINT_TOPICS, Chunk, select_chunks, split_chunks
from .validate import quote_in_text
from .website import WebsiteNotFoundError, registered_domain

log = logging.getLogger("extractor.datapoints")

COLUMNS = ["company_id", "company_name", "segment", "country", "lei", "data_point", "value",
           "unit", "period_end", "source", "endpoint", "method", "retrieved_at", "confidence",
           "note"]

# (data point, level) in output order. Names match the golden dataset's `field`.
DATA_POINTS = [
    ("legal_name", "reference"), ("lei", "reference"), ("business_id", "reference"),
    ("cik", "reference"), ("other_names", "reference"), ("country_code", "reference"),
    ("head_office_city", "reference"), ("legal_form", "reference"),
    ("listing_status", "reference"), ("ticker", "reference"), ("isin", "reference"),
    ("exchange", "reference"), ("exchange_segment", "reference"), ("listing_date", "reference"),
    ("sector_code", "reference"), ("sub_sector", "reference"), ("reporting_currency", "reference"),
    ("shares_outstanding", "market"), ("share_price", "market"), ("market_cap", "market"),
    ("market_cap_band", "market"),
    ("fiscal_year", "financials"), ("revenue", "financials"), ("total_assets", "financials"),
    ("fte", "financials"), ("headcount", "financials"),
    ("controlling_owner", "other"), ("controlling_owner_name", "other"),
    ("ownership_type", "other"), ("pe_stake_5pct", "other"), ("ultimate_parent", "other"),
    ("revenue_model", "other"), ("business_structure", "other"), ("segments", "other"),
    ("revenue_by_country", "other"), ("staff_by_country", "other"), ("pension_type", "other"),
    ("shareholding_requirement", "other"),
]
NAMES = [d for d, _ in DATA_POINTS]
BUY_ONLY = {"share_price", "market_cap", "market_cap_band"}
LISTED_ONLY = {"ticker", "isin", "exchange", "exchange_segment", "listing_date",
               "shares_outstanding", "share_price", "market_cap", "market_cap_band", "cik"}
# Pay facts are only published by listed companies (remuneration reports).
LISTED_REPORTS_ONLY = {"pension_type", "shareholding_requirement"}

CONFIDENCE_RANK = {"A": 3, "B": 2, "C": 1, "": 0}
METHOD_RANK = {"API": 4, "XBRL": 4, "PARSE": 3, "SCRAPE": 2, "BUY": 0, "": 0}

DP_DIR = OUTPUT_DIR / "datapoints"
TOPIC_WORDS = 2_500                  # report words sent per topic (5 topics)
WEB_PAGE_WORDS = 3_000               # words kept per scraped web page
DEFAULT_WEB_CREDITS = 4              # map 1 + scrape 3
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


def from_result(result: dict, origin: Origin | None) -> list[Found]:
    """The figures and identifiers the pipeline found."""
    out: list[Found] = []
    for name in ("revenue", "total_assets"):
        f = _money_found(name, result.get(name) or {}, result, origin)
        if f:
            out.append(f)
    period = result.get("period_end_date") or ""
    at = result.get("extracted_at") or ""
    money = next((f for f in out), None)
    if result.get("fiscal_year") and money:
        out.append(Found("fiscal_year", result["fiscal_year"], period_end=period, source=money.source,
                         endpoint=money.endpoint.split("#")[0], method=money.method,
                         confidence=money.confidence, note="the year the figures are for",
                         retrieved_at=at))
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


def described_in_result(result: dict, origin: Origin | None) -> list[Found]:
    """The pipeline's revenue model and business structure. They share one quote for
    several facts, so a fact with its own quote (the data-point pass) wins a tie."""
    out: list[Found] = []
    if origin is None:
        return out
    period = result.get("period_end_date") or ""
    at = result.get("extracted_at") or ""

    def described(name: str, value, d: dict, extra: str = ""):
        if value in (None, "", []):
            return
        endpoint, conf, where = origin.where(d.get("quote"), d.get("chunk_id"))
        out.append(Found(name, value, period_end=period, source=origin.source, endpoint=endpoint,
                         method=origin.method, confidence=conf,
                         note="; ".join(x for x in (extra, where) if x), retrieved_at=at))

    rm = result.get("revenue_model") or {}
    if rm.get("description") or rm.get("categories"):
        described("revenue_model", " | ".join(x for x in (", ".join(rm.get("categories") or []),
                                                          rm.get("description")) if x), rm)
    bs = result.get("business_structure") or {}
    described("business_structure", bs.get("description"), bs)
    described("segments", "; ".join(bs.get("segments") or []), bs)
    described("legal_form", bs.get("legal_form"), bs)
    if bs.get("is_listed") is not None:
        described("listing_status", "listed" if bs["is_listed"] else "unlisted", bs)
    if bs.get("ultimate_parent"):
        described("ultimate_parent", bs["ultimate_parent"], bs)
    return out


# --- 3. the AI pass over the report, and 4. over web pages ------------------------------

def _user_prompt(name: str, url: str, chunks: list[Chunk], what: str) -> str:
    body = "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)
    return (f"Company legal name: {name}\nSource: {url}\n\n"
            f"Excerpts from {what} (tables are in markdown):\n\n{body}")


def ask(name: str, url: str, chunks: list[Chunk], what: str, cache_key: str) -> DataPointFacts:
    """The data-point LLM call, cached by the document and chunks it was given."""
    path = CACHE_DIR / f"{cache_key}_datapoints_llm.json"
    ids = [c.id for c in chunks]
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if saved.get("chunk_ids") == ids and saved.get("prompt") == llm.load_prompt("datapoints_system"):
            return DataPointFacts.model_validate(saved["facts"])
    facts = llm.call_llm(llm.load_prompt("datapoints_system"), _user_prompt(name, url, chunks, what),
                         DataPointFacts)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"chunk_ids": ids, "prompt": llm.load_prompt("datapoints_system"),
                                "model": llm.model_name(), "facts": facts.model_dump()},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return facts


def report_chunks(origin: Origin) -> list[Chunk]:
    picked: dict[int, Chunk] = {}
    for topic in DATAPOINT_TOPICS:
        for c in select_chunks(list(origin.chunks.values()), topic, TOPIC_WORDS):
            picked[c.id] = c
    return [picked[i] for i in sorted(picked)]


def _country_list(b) -> str:
    return "; ".join(f"{i.country}: {fmt_number(i.value)}" for i in b.items)


def from_facts(facts: DataPointFacts, origin: Origin) -> list[Found]:
    """The AI's facts as Found values, each placed by its quote."""
    out: list[Found] = []

    def add(name: str, value, fact, unit: str = "", period: str = "", extra: str = ""):
        if value in (None, "", []) or not getattr(fact, "quote", None):
            return                      # no quote, no value: the prompt demands one
        endpoint, conf, where = origin.where(fact.quote, fact.chunk_id)
        out.append(Found(name, value, unit=unit, period_end=period or "", source=origin.source,
                         endpoint=endpoint, method=origin.method, confidence=conf,
                         note="; ".join(x for x in (extra, where) if x),
                         retrieved_at=origin.retrieved_at))

    for name in ("revenue", "total_assets"):
        n: NumberFact = getattr(facts, name)
        if n.value is not None and n.unit:
            add(name, full_value(n.value, n.unit), n, unit=n.currency or "", period=n.period_end,
                extra=f"printed {fmt_number(n.value)} {n.unit}")
    for name in ("fte", "headcount"):
        n = getattr(facts, name)
        add(name, n.value, n, unit="employees", period=n.period_end)
    n = facts.shares_outstanding
    if n.value is not None:
        add("shares_outstanding", full_value(n.value, n.unit or "units"), n, unit="shares",
            period=n.period_end)
    for name in ("head_office_city", "ticker", "isin", "exchange", "exchange_segment",
                 "listing_date", "sub_sector", "reporting_currency", "pension_type",
                 "shareholding_requirement"):
        t: TextFact = getattr(facts, name)
        add(name, t.value, t)
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
            if owner.holder_type in ("listed_company", "other_company"):
                add("ultimate_parent", owner.name, owner, extra="controlling company (immediate parent)")
    elif owner.quote:
        add("controlling_owner", "none", owner, extra="no controlling shareholder")
        add("ownership_type", "widely_held", owner, extra="no controlling shareholder")

    holders = [h for h in facts.major_shareholders if h.name and h.quote]
    pe = [h for h in holders + ([owner] if owner.name and owner.quote else [])
          if h.holder_type == "private_equity" and (h.stake_pct is None or h.stake_pct >= 5)]
    if pe:
        h = pe[0]
        add("pe_stake_5pct", "yes", h, extra=f"{h.name}"
            + (f" {fmt_number(h.stake_pct)}%" if h.stake_pct is not None else ""))
    elif holders:
        add("pe_stake_5pct", "no", holders[0], extra="shareholders of 5% or more: " + "; ".join(
            f"{h.name} {fmt_number(h.stake_pct)}%" if h.stake_pct is not None else h.name
            for h in holders))

    for name in ("revenue_by_country", "staff_by_country"):
        b = getattr(facts, name)
        if b.items:
            unit = " ".join(x for x in (b.currency, b.unit if b.unit != "units" else "") if x) \
                or ("employees" if name == "staff_by_country" else "")
            add(name, _country_list(b), b, unit=unit, extra=b.basis or "")
    return out


# --- 4. HTML backup: the company's own web pages ---------------------------------------------

PAGE_HINTS = {
    "ownership": ["shareholder", "ownership", "owner", "aksjonaer", "aktieagare", "aktionaer",
                  "osakkeenomistaj", "eier", "eigar", "agare", "ejer", "omistaj", "investor",
                  "governance", "about", "om-oss", "om-os"],
    "profile": ["about", "about-us", "company", "who-we-are", "om-oss", "om-os", "meista",
                "ueber-uns", "uber-uns", "a-propos", "chi-siamo", "quienes-somos", "facts",
                "key-figures", "contact", "kontakt", "history", "organisation", "organization"],
    "listing": ["investor", "share", "stock", "aksjen", "aktien", "osake", "listing"],
    "pay": ["remuneration", "governance", "compensation"],
    "financials": ["key-figures", "financial", "results", "annual", "nokkeltall", "nyckeltal"],
}
TOPIC_OF = {"controlling_owner": "ownership", "controlling_owner_name": "ownership",
            "ownership_type": "ownership", "pe_stake_5pct": "ownership", "ultimate_parent": "ownership",
            "head_office_city": "profile", "fte": "profile", "headcount": "profile",
            "sub_sector": "profile", "listing_status": "listing", "ticker": "listing",
            "isin": "listing", "exchange": "listing", "exchange_segment": "listing",
            "listing_date": "listing", "shares_outstanding": "listing",
            "pension_type": "pay", "shareholding_requirement": "pay",
            "revenue": "financials", "total_assets": "financials",
            "revenue_by_country": "financials", "staff_by_country": "financials",
            "reporting_currency": "financials"}
SKIP_URL = re.compile(r"\.(pdf|jpe?g|png|gif|svg|zip|xlsx?|docx?|mp4)(\?|$)|/(news|press|blog|jobs?|"
                      r"vacanc|career|product|shop|cart|login|cookie|privacy|terms)", re.I)


def rank_pages(site: str, links: list[dict], missing: list[str], n: int) -> list[str]:
    """The site's pages most likely to hold the missing data points, by URL words."""
    topics = {TOPIC_OF[m] for m in missing if m in TOPIC_OF}
    home = registered_domain(urlparse(site).netloc)
    scored = []
    for link in links:
        url = (link.get("url") or "").split("#")[0]
        p = urlparse(url)
        if not url or registered_domain(p.netloc) != home or SKIP_URL.search(url):
            continue
        path = p.path.lower()
        text = f"{path} {(link.get('title') or '').lower()}"
        score = sum(2 if any(h in path for h in PAGE_HINTS[t]) else
                    1 if any(h in text for h in PAGE_HINTS[t]) else 0 for t in topics)
        if score:
            score -= path.count("/") * 0.1 + len(path) / 500     # short, top-level pages first
            scored.append((score, url))
    seen, out = set(), []
    for _, url in sorted(scored, key=lambda s: -s[0]):
        key = urlparse(url).path.rstrip("/").lower()
        if key not in seen:
            seen.add(key)
            out.append(url)
    return out[:n]


def _web_markdown(url: str, slug: str, fc: FirecrawlClient) -> str:
    """A page as markdown via Firecrawl (cached: re-runs cost nothing)."""
    import hashlib
    path = CACHE_DIR / f"{slug}_web_{hashlib.sha1(url.encode()).hexdigest()[:16]}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    md = fc.scrape(url, formats=["markdown"])["markdown"]
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(md, encoding="utf-8")
    return md


def _trim_words(text: str, n: int) -> str:
    words = text.split(" ")
    return text if len(words) <= n else " ".join(words[:n])


def web_origin(name: str, slug: str, site: str, missing: list[str], fc: FirecrawlClient
               ) -> Origin | None:
    """Map the site (1 credit), scrape the home page and the best pages for what is
    missing (1 credit each), as one document for the AI."""
    try:
        links = fc.map(site, search=None, limit=300)
    except CreditBudgetExceeded:
        return None
    budget = (fc.max_credits or 99) - fc.credits.total
    urls = [site] + [u for u in rank_pages(site, links, missing, 4)
                     if u.rstrip("/") != site.rstrip("/")]
    chunks, page_urls, pages = {}, {}, []
    for url in urls[:max(budget, 0)]:
        try:
            md = _web_markdown(url, slug, fc)
        except CreditBudgetExceeded:
            break
        except Exception as e:  # noqa: BLE001 - one page failing must not stop the others
            log.warning("Scrape of %s failed: %s", url, str(e)[:150])
            continue
        if len(md.strip()) < 200:
            continue
        cid = len(chunks)
        chunks[cid] = Chunk(cid, _trim_words(md, WEB_PAGE_WORDS), [cid + 1])
        page_urls[cid] = url
        pages.append(Page(cid + 1, chunks[cid].text))
    if not chunks:
        return None
    return Origin("web", site, "Company website", "SCRAPE", _now(), pages, chunks, page_urls)


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


def finish(t: Target, chosen: dict[str, Found], tried: list[str], gleif_isins: list[str],
           error: str | None) -> list[Found]:
    """One Found per data point, in DATA_POINTS order, with a reason for each gap."""
    us = t.company.country == "US" or t.company.segment == "us_listed"
    isin = chosen.get("isin")
    if isin and gleif_isins:
        codes = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", str(isin.value).upper())
        if codes and all(c in gleif_isins for c in codes):
            chosen["isin"] = Found(**{**asdict(isin), "confidence": "A",
                                      "note": isin.note + "; confirmed in the GLEIF ISIN map"})
    listed = (chosen.get("listing_status").value == "listed") if chosen.get("listing_status") else None
    if listed is None and any(k in chosen for k in ("ticker", "exchange", "isin")):
        src = next(chosen[k] for k in ("ticker", "exchange", "isin") if k in chosen)
        chosen["listing_status"] = Found(**{**asdict(src), "data_point": "listing_status",
                                            "value": "listed", "unit": "",
                                            "note": f"has a {src.data_point}: {clip(str(src.value), 60)}"})
        listed = True
    rows = []
    for name in NAMES:
        if name in chosen:
            rows.append(chosen[name])
            continue
        if name in BUY_ONLY:
            why, method = "not collected: market data changes daily and is bought (vendor quote)", "BUY"
        elif name == "cik" and not us:
            why, method = "not applicable: no SEC filing found and not US-listed", ""
        elif listed is False and (name in LISTED_ONLY or name in LISTED_REPORTS_ONLY):
            why, method = "not applicable: the company is not listed", ""
        else:
            why = "not found in: " + ", ".join(tried) if tried else "no source reached"
            method = ""
        if error and name not in BUY_ONLY:
            why += f" (annual-report route failed: {clip(error, 140)})"
        rows.append(Found(name, None, method=method, note=why))
    return rows


# --- one company ------------------------------------------------------------------------------

NO_CREDITS = "Firecrawl is out of credits"


def collect(t: Target, web: bool = True, web_credits: int = DEFAULT_WEB_CREDITS,
            error: str | None = None, flags: set | None = None) -> list[Found]:
    """`error`: why the annual-report pipeline has no result (if not in its error file).
    `flags` gets "no_credits" when Firecrawl refused for lack of credits."""
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
    origin = report_origin(result) if result else None
    if result:
        values += from_result(result, origin)
        tried.append(origin.source if origin else "annual report")

    # 2. official APIs
    lei = (lei_record or {}).get("lei") or c.lei
    gleif_isins: list[str] = []
    if lei:
        try:
            g = apis.gleif_values(lei)
            gleif_isins = next((f.value.split(";") for f in g if f.data_point == "_gleif_isins"), [])
            values += g
            tried.append("GLEIF")
        except httpx.HTTPError as e:
            log.warning("GLEIF failed: %s", e)
    home = (lei_record or {}).get("country") or c.country
    number = t.business_id or (lei_record or {}).get("registered_as") \
        or ((result or {}).get("filing") or {}).get("registration_number")
    reg = apis.registry_values(home, number)
    if reg:
        values += reg
        tried.append(reg[0].source)
    cik = ((result or {}).get("filing") or {}).get("cik")
    if not cik and (c.country == "US" or c.segment == "us_listed" or home == "US"):
        try:
            cik, why = edgar.find_cik(c.name)
            log.info("SEC CIK: %s (%s)", cik, why)
        except (httpx.HTTPError, edgar.SecContactMissing) as e:
            log.warning("SEC lookup failed: %s", e)
    if cik:
        try:
            values += apis.edgar_values(int(cik))
            tried.append("SEC EDGAR")
        except (httpx.HTTPError, edgar.SecContactMissing) as e:
            log.warning("SEC EDGAR failed: %s", e)

    # 3. the AI pass over the report
    if origin:
        chunks = report_chunks(origin)
        if chunks:
            log.info("Data points: asking the AI about %d report chunks", len(chunks))
            facts = ask(c.name, origin.url, chunks, "the company's annual report",
                        Path(result["debug"]["markdown_file"]).stem)
            values += from_facts(facts, origin)
        values += described_in_result(result, origin)

    # 4. HTML backup for whatever is still missing
    chosen = best(values)
    listed = chosen.get("listing_status")
    missing = [n for n in NAMES if n not in chosen and n in TOPIC_OF
               and not (listed and listed.value == "unlisted"
                        and (n in LISTED_ONLY or n in LISTED_REPORTS_ONLY))]
    if web and missing:
        fc = FirecrawlClient(load_settings(), max_credits=web_credits)
        try:
            site = website_for(t, result, lei_record, fc)
        except PaymentRequiredError:
            site = None
            flags.add("no_credits")
        if "no_credits" in flags:
            tried.append(f"company website (skipped: {NO_CREDITS})")
        elif site:
            log.info("HTML backup on %s for: %s", site, ", ".join(missing))
            try:
                w = web_origin(c.name, c.slug, site, missing, fc)
            except PaymentRequiredError:
                w = None
                flags.add("no_credits")
                tried.append(f"company website (skipped: {NO_CREDITS})")
            if w:
                tried.append(f"company website ({len(w.chunks)} pages)")
                facts = ask(c.name, site, list(w.chunks.values()), "the company's web pages",
                            f"{c.slug}_web")
                values += [f for f in from_facts(facts, w) if f.data_point in missing]
            log.info("HTML backup used %d Firecrawl credit(s)", fc.credits.total)
        chosen = best(values)
    return finish(t, chosen, tried, gleif_isins, error)


def rows_for(t: Target, found: list[Found]) -> list[dict]:
    c = t.company
    lei = next((str(f.value) for f in found if f.data_point == "lei" and f.value), c.lei or "")
    rows = []
    for f in found:
        value = fmt_number(f.value) if isinstance(f.value, (int, float)) else (f.value or "")
        rows.append({"company_id": c.company_id, "company_name": c.name,
                     "segment": c.segment or "", "country": c.country or "", "lei": lei,
                     "data_point": f.data_point, "value": value, "unit": f.unit,
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
    error = None
    if not c.result_path.exists() and (not c.error_path.exists() or opts["retry_failed"]
                                       or no_credits_path(c).exists()):
        res = process_company(c, False, opts["pipeline_credits"])
        if res["kind"] == "fatal" and "PaymentRequired" in res.get("error", ""):
            # The free routes (filings, registers, APIs) still work: carry on without
            # Firecrawl; the company is redone on the next run.
            flags.add("no_credits")
            error = f"{NO_CREDITS}: the website report search was skipped"
        elif res["kind"] in ("fatal", "offline"):
            return res
    handler = logging.FileHandler(OUTPUT_DIR / f"{c.slug}.log", mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    try:
        found = collect(t, web=opts["web"] and "no_credits" not in flags,
                        web_credits=opts["web_credits"], error=error, flags=flags)
    except FATAL as e:
        return {"kind": "fatal", "error": f"{type(e).__name__}: {e}"}
    except Exception as e:  # noqa: BLE001 - record and continue with the next company
        log.exception("Data points for %s failed", c.company_id)
        return {"kind": "error", "error": f"{type(e).__name__}: {str(e)[:200]}"}
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
    return {"kind": "done", "no_credits": "no_credits" in flags, "found": sum(1 for r in rows if r["value"]), "total": len(rows),
            "seconds": time.monotonic() - started}


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
    p.add_argument("--no-web", action="store_true", help="No HTML backup (no Firecrawl credits for it)")
    p.add_argument("--web-credits", type=int, default=DEFAULT_WEB_CREDITS,
                   help=f"Firecrawl credits per company for the HTML backup (default {DEFAULT_WEB_CREDITS})")
    p.add_argument("--pipeline-credits", type=int, default=DEFAULT_PIPELINE_CREDITS,
                   help=f"Firecrawl credits per company for finding the report (default {DEFAULT_PIPELINE_CREDITS})")
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
    opts = {"web": not args.no_web, "web_credits": args.web_credits,
            "pipeline_credits": args.pipeline_credits, "retry_failed": args.retry_failed}

    workers = max(1, args.workers)
    code = 0
    with _KeepAwake():
        if workers == 1:
            for i, t in enumerate(todo, 1):
                res = process(t, opts)
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
                        code = _report(i, len(todo), t, res) or code
                        write_csv(everyone, args.out)
    n = write_csv(everyone, args.out)
    print(f"\n{n} rows: {args.out}")
    filled = write_golden_filled(args.csv, everyone, OUTPUT_DIR / "golden_test_filled.csv")
    if filled:
        print(f"Golden sample with build_value: {filled}")
    return code


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
