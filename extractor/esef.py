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
import json
import logging
import re
import time
from dataclasses import asdict, dataclass, field

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import CACHE_DIR

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


# Tags read for the gaps the AI left (docs/not_found_reduction_plan.md, B3 and B4).
OPERATING_PROFIT_CONCEPT = "ifrs-full:ProfitLossFromOperatingActivities"
SHARES_OUTSTANDING_CONCEPT = "ifrs-full:NumberOfSharesOutstanding"
SHARES_ISSUED_CONCEPT = "ifrs-full:NumberOfSharesIssued"
# The ultimate parent only: "NameOfParentEntity" is the immediate parent.
PARENT_CONCEPTS = ("ifrs-full:NameOfUltimateParentOfEntity",)
# A company's own EBITDA tag (an extension: "austriacard:Ebitda"); not "...Ebitda" lines
# that only feed it (depreciation "recognised in profit or loss Ebitda").
_EBITDA_LOCAL = re.compile(r"(adjusted)?ebitda", re.I)
EXTRAS_PAUSE_S = 1.0
_last_ask = 0.0


@dataclass
class ExtraFigures:
    """What one annual filing tags beyond revenue and assets, for its fiscal year."""
    period_end: str
    report_url: str
    viewer_url: str | None
    ebitda: TaggedFigure | None = None             # the company's own EBITDA tag
    operating_profit: TaggedFigure | None = None
    shares: TaggedFigure | None = None             # outstanding, else issued (concept says which)
    parent: tuple[str, str] | None = None          # (name, concept)


def extra_figures(facts: dict, period_end: str) -> dict:
    """EBITDA (a company extension tag named "Ebitda"), operating profit, the share count
    at period_end (outstanding, else issued) and the parent's name, from one filing's
    facts, without dimensions. Money and counts must be for the fiscal year ending at
    period_end (12 months, or at that date)."""
    end = _day(period_end) + dt.timedelta(days=1)
    out: dict = {}
    for f in facts.values():
        d = f.get("dimensions", {})
        if not set(d) <= _PLAIN_DIMENSIONS:
            continue
        concept, period, unit = d.get("concept") or "", d.get("period") or "", d.get("unit") or ""
        if concept in PARENT_CONCEPTS:
            name = re.sub(r"<[^>]+>", " ", str(f.get("value") or "")).strip()
            if 1 < len(name) < 200:
                out.setdefault(concept, (re.sub(r"\s+", " ", name), concept))
            continue
        try:
            value = float(f["value"])
        except (TypeError, ValueError, KeyError):
            continue
        local = concept.split(":", 1)[-1]
        is_ebitda = not concept.startswith("ifrs-full:") and _EBITDA_LOCAL.fullmatch(local)
        if unit.startswith("iso4217:") and "/" in period and (
                concept == OPERATING_PROFIT_CONCEPT or is_ebitda):
            start, stop = (_day(x) for x in period.split("/"))
            if stop == end and 350 <= (stop - start).days <= 380:
                key = "ebitda" if is_ebitda else "operating_profit"
                if key == "ebitda" and local.lower().startswith("adjusted") and "ebitda" in out:
                    continue                # the plain EBITDA tag first
                out.setdefault(key, TaggedFigure(value, unit.split(":", 1)[1], concept,
                                                 f"{start}/{stop - dt.timedelta(days=1)}"))
        elif unit == "xbrli:shares" and "/" not in period and concept in (
                SHARES_OUTSTANDING_CONCEPT, SHARES_ISSUED_CONCEPT):
            if _day(period) in (end, end - dt.timedelta(days=1)) and value > 0:
                out.setdefault(concept, TaggedFigure(value, "shares", concept, period_end))
    return out


def extras_for(lei: str, period_end: str) -> ExtraFigures | None:
    """The tags beyond revenue and assets from the annual filing for the fiscal year that
    ends on period_end (YYYY-MM-DD), or None when filings.xbrl.org has no such filing.
    Cached in cache/esef_extra_<lei>_<date>.json (a "none" answer for a week)."""
    path = CACHE_DIR / f"esef_extra_{lei}_{period_end[:10]}.json"
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if saved.get("extras"):
            e = saved["extras"]
            for k in ("ebitda", "operating_profit", "shares"):
                e[k] = TaggedFigure(**e[k]) if e.get(k) else None
            e["parent"] = tuple(e["parent"]) if e.get("parent") else None
            return ExtraFigures(**e)
        if dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(saved["checked_at"])                 < dt.timedelta(days=7):
            return None
    got = _extras_for(lei, period_end)
    if got is not False:
        CACHE_DIR.mkdir(exist_ok=True)
        path.write_text(json.dumps({"extras": asdict(got) if got else None,
                                    "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()}),
                        encoding="utf-8")
    return got or None


def _extras_for(lei: str, period_end: str) -> ExtraFigures | None | bool:
    """extras_for without the cache; False when the index could not be read (not cached).
    One company a second at most: the index answers 429 to a faster run."""
    global _last_ask
    time.sleep(max(0.0, EXTRAS_PAUSE_S - (time.monotonic() - _last_ask)))
    _last_ask = time.monotonic()
    try:
        filings = list_filings(lei)
    except (httpx.HTTPError, _Retryable) as e:
        log.warning("ESEF filings for %s: %s", lei, str(e)[:120])
        return False
    attrs = next((a for a in filings if (a.get("period_end") or "")[:10] == period_end[:10]
                  and a.get("json_url")), None)
    if not attrs:
        return None
    try:
        facts = _get(BASE + attrs["json_url"]).json().get("facts", {})
    except (httpx.HTTPError, _Retryable, ValueError) as e:
        log.warning("ESEF facts for %s %s unreadable: %s", lei, period_end, str(e)[:120])
        return False
    got = extra_figures(facts, period_end[:10])
    return ExtraFigures(
        period_end=period_end[:10],
        report_url=BASE + attrs["report_url"] if attrs.get("report_url") else BASE + attrs["json_url"],
        viewer_url=BASE + attrs["viewer_url"] if attrs.get("viewer_url") else None,
        ebitda=got.get("ebitda"), operating_profit=got.get("operating_profit"),
        shares=got.get(SHARES_OUTSTANDING_CONCEPT) or got.get(SHARES_ISSUED_CONCEPT),
        parent=next((got[c] for c in PARENT_CONCEPTS if c in got), None))


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
    from . import source_policy
    source_policy.gate(filing.report_url)      # filings.xbrl.org: allowed until legal answers
    r = _get(filing.report_url)
    r.encoding = r.encoding or "utf-8"
    return r.text
