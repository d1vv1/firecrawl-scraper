"""ESEF filings: exact figures from XBRL tags, and the report text, by LEI.

EU/EEA (and UK) companies listed on a regulated market file their annual report in
ESEF format: an .xhtml report with the financial statements tagged as data.
filings.xbrl.org indexes these filings by LEI, free and without a key. Germany and
Ireland are missing from the index, and companies only on growth markets (First
North, Euronext Growth) don't file ESEF; those go through the website route.

From one filing we take:
  - revenue, total assets, total equity and liabilities: tagged numbers, no AI;
  - the period end (so the fiscal year is certain);
  - the full report text, for the facts that aren't tagged (revenue model, ...).
"""

import datetime as dt
import logging
import re
from dataclasses import asdict, dataclass, field

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

log = logging.getLogger(__name__)

BASE = "https://filings.xbrl.org"
HEADERS = {"User-Agent": "annual-report-extractor/0.1"}
TIMEOUT_S = 120
MAX_FILINGS_TO_TRY = 4     # the newest filings can be quarterly; look a little further back

# Revenue is tagged with one of these (Volvo: Revenue; Nokia: RevenueFromContractsWithCustomers).
REVENUE_CONCEPTS = ["ifrs-full:Revenue", "ifrs-full:RevenueFromContractsWithCustomers",
                    "ifrs-full:RevenueFromSaleOfGoods"]
# A broader line some companies tag as well (CTT: revenue plus other operating income).
# Kept next to revenue, never instead of it (see datapoints.REVENUE_RULE).
BROAD_REVENUE_CONCEPT = "ifrs-full:RevenueAndOperatingIncome"
ASSETS_CONCEPT = "ifrs-full:Assets"
EQUITY_AND_LIABILITIES_CONCEPT = "ifrs-full:EquityAndLiabilities"
# A fact with any other dimension (segment, geography, ...) is a breakdown, not the total.
_PLAIN_DIMENSIONS = {"concept", "entity", "period", "unit", "language"}


@dataclass
class TaggedFigure:
    value: float              # full value in currency units (tags hold full numbers)
    currency: str             # ISO 4217
    concept: str              # e.g. "ifrs-full:Revenue"
    period: str               # e.g. "2025-01-01/2025-12-31" or "2025-12-31"
    scope: str = "consolidated"   # registries also file parent-only accounts


@dataclass
class EsefFiling:
    lei: str
    filing_id: str
    period_end: str           # YYYY-MM-DD
    country: str | None
    report_url: str           # the full annual report (.xhtml)
    viewer_url: str | None
    package_url: str | None
    figures: dict[str, TaggedFigure] = field(default_factory=dict)
    language: str | None = None   # report language from the file name: "en", "fi", "sv", ...

    @property
    def fiscal_year(self) -> str:
        return self.period_end[:4]

    def as_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "EsefFiling":
        figs = {k: TaggedFigure(**v) for k, v in (d.get("figures") or {}).items()}
        return EsefFiling(**{**d, "figures": figs})


class _Retryable(Exception):
    pass


@retry(retry=retry_if_exception_type((httpx.TransportError, _Retryable)),
       stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20), reraise=True)
def _get(url: str, params: dict | None = None, api: bool = False) -> httpx.Response:
    headers = HEADERS | ({"Accept": "application/vnd.api+json"} if api else {})
    r = httpx.get(url, params=params, headers=headers, timeout=TIMEOUT_S, follow_redirects=True)
    if r.status_code == 429 or r.status_code >= 500:
        raise _Retryable(f"HTTP {r.status_code} for {url}")
    r.raise_for_status()
    return r


def list_filings(lei: str) -> list[dict]:
    """Filings for an LEI, newest period first (attributes only)."""
    data = _get(f"{BASE}/api/filings", {"filter[entity.identifier]": lei, "sort": "-period_end",
                                         "page[size]": 10}, api=True).json().get("data", [])
    return [f["attributes"] for f in data]


def _day(s: str) -> dt.date:
    return dt.date.fromisoformat(s[:10])


def annual_figures(facts: dict, period_end: str) -> dict[str, TaggedFigure]:
    """Revenue for a ~12-month period ending at period_end, and assets/equity+liabilities
    at period_end. Empty when the filing isn't an annual one. XBRL periods end at
    midnight *after* the last day, e.g. 2025-01-01/2026-01-01 for calendar 2025."""
    end = _day(period_end) + dt.timedelta(days=1)
    durations: dict[str, TaggedFigure] = {}
    instants: dict[str, TaggedFigure] = {}
    full_year = False          # any 12-month money figure ending at period_end
    for f in facts.values():
        d = f.get("dimensions", {})
        if not set(d) <= _PLAIN_DIMENSIONS:
            continue
        concept, period, unit = d.get("concept"), d.get("period") or "", d.get("unit") or ""
        if unit.startswith("iso4217:") and "/" in period:
            try:
                start, stop = (_day(x) for x in period.split("/"))
                full_year = full_year or (stop == end and 350 <= (stop - start).days <= 380)
            except ValueError:
                pass
        if not unit.startswith("iso4217:") or concept not in (
                *REVENUE_CONCEPTS, BROAD_REVENUE_CONCEPT, ASSETS_CONCEPT,
                EQUITY_AND_LIABILITIES_CONCEPT):
            continue
        try:
            value = float(f["value"])
        except (TypeError, ValueError):
            continue
        currency = unit.split(":", 1)[1]
        if "/" in period:
            start, stop = (_day(x) for x in period.split("/"))
            if stop == end and 350 <= (stop - start).days <= 380:
                durations.setdefault(concept, TaggedFigure(
                    value, currency, concept, f"{start}/{stop - dt.timedelta(days=1)}"))
        elif _day(period) in (end, end - dt.timedelta(days=1)):
            instants.setdefault(concept, TaggedFigure(value, currency, concept, period_end))
    out = {}
    revenue = next((durations[c] for c in REVENUE_CONCEPTS if c in durations), None)
    if revenue:
        out["revenue"] = revenue
    if BROAD_REVENUE_CONCEPT in durations:
        out["revenue_and_operating_income"] = durations[BROAD_REVENUE_CONCEPT]
    if ASSETS_CONCEPT in instants:
        out["total_assets"] = instants[ASSETS_CONCEPT]
    if EQUITY_AND_LIABILITIES_CONCEPT in instants:
        out["total_equity_and_liabilities"] = instants[EQUITY_AND_LIABILITIES_CONCEPT]
    # An annual filing has full-year figures; a half-year one only 6 months (its balance
    # sheet date alone isn't enough: Bavarian Nordic's H1 2026 filing has total assets too).
    return out if full_year and ("revenue" in out or "total_assets" in out) else {}


def latest_annual_filing(lei: str) -> EsefFiling | None:
    """The newest annual ESEF filing for this LEI, with its tagged figures."""
    tried = set()
    for attrs in list_filings(lei):
        period_end = attrs.get("period_end")
        if not period_end or period_end in tried or not attrs.get("json_url"):
            continue
        tried.add(period_end)
        if len(tried) > MAX_FILINGS_TO_TRY:
            break
        try:
            facts = _get(BASE + attrs["json_url"]).json().get("facts", {})
        except (httpx.HTTPError, _Retryable, ValueError) as e:
            log.warning("ESEF facts for %s %s unreadable: %s", lei, period_end, str(e)[:120])
            continue
        figures = annual_figures(facts, period_end)
        if not figures:
            log.info("ESEF filing %s %s is not an annual report; trying an older one", lei, period_end)
            continue
        def url(key):
            return BASE + attrs[key] if attrs.get(key) else None
        filing = EsefFiling(lei=lei, filing_id=attrs.get("fxo_id") or f"{lei}-{period_end}",
                            period_end=period_end, country=attrs.get("country"),
                            report_url=url("report_url"), viewer_url=url("viewer_url"),
                            package_url=url("package_url"), figures=figures,
                            language=report_language(attrs.get("report_url") or attrs["json_url"]))
        log.info("ESEF: annual filing %s (FY%s), tagged %s", filing.filing_id,
                 filing.fiscal_year, sorted(figures))
        return filing
    return None


def report_language(path: str) -> str | None:
    """Language from the ESEF file name: bava-2025-12-31-en.xhtml -> "en",
    ...-2025-12-31-1-fi.json -> "fi". None if the name doesn't say."""
    m = re.search(r"-([a-z]{2})(?:\.[a-z]+)?(?:/|$)", path.rsplit("/reports/", 1)[-1].lower())
    return m.group(1) if m else None


def is_recent(filing: EsefFiling | None, today: dt.date | None = None) -> bool:
    """Recent enough to use instead of the website: last full year or newer (FY2025
    during 2026). Otherwise the website likely has a newer report."""
    return bool(filing) and int(filing.fiscal_year) >= (today or dt.date.today()).year - 1


def download_report(filing: EsefFiling) -> str:
    """The full annual report (.xhtml) as text."""
    r = _get(filing.report_url)
    r.encoding = r.encoding or "utf-8"
    return r.text
