"""SEC EDGAR: US annual reports (Form 10-K, or 20-F / 40-F for foreign issuers).

Every company registered with the SEC files its annual report on EDGAR, free and with
no scraping: we find the company's CIK by name, take its latest annual filing, read
revenue / total assets / total liabilities and equity from that filing's XBRL tags
(the SEC's company-facts API, filtered to that filing), and download the filing
itself (inline-XBRL HTML) for the text-based facts.

This also covers companies outside the US that file with the SEC (Chubb, NXP,
Smurfit WestRock, Johnson Controls...), whose own websites often have no annual
report PDF.

The SEC requires a User-Agent with a contact: set SEC_CONTACT in .env.
"""

import datetime as dt
import json
import logging
import os
import re
import time
from dataclasses import asdict, dataclass, field

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import CACHE_DIR, ConfigError, load_settings
from .esef import TaggedFigure
from .lei import match_level, name_key

log = logging.getLogger(__name__)

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
ANNUAL_FORMS = ("10-K", "20-F", "40-F", "10-K/A", "20-F/A")
TICKERS_MAX_AGE = dt.timedelta(days=7)
_MIN_INTERVAL_S = 0.15          # the SEC allows 10 requests/second
_last_call = 0.0

REVENUE_CONCEPTS = [
    ("us-gaap", "Revenues"),
    ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
    ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax"),
    ("us-gaap", "SalesRevenueNet"),
    ("ifrs-full", "Revenue"),
    ("ifrs-full", "RevenueFromContractsWithCustomers"),
]
ASSETS_CONCEPTS = [("us-gaap", "Assets"), ("ifrs-full", "Assets")]
EQUITY_AND_LIABILITIES_CONCEPTS = [("us-gaap", "LiabilitiesAndStockholdersEquity"),
                                   ("ifrs-full", "EquityAndLiabilities")]


class SecContactMissing(ConfigError):
    pass


@dataclass
class EdgarFiling:
    cik: int
    company: str              # SEC's name for the registrant
    form: str                 # 10-K, 20-F, ...
    filing_id: str            # accession number
    period_end: str           # YYYY-MM-DD (the report date)
    filed: str
    report_url: str           # the filing's main document (inline-XBRL HTML)
    figures: dict[str, TaggedFigure] = field(default_factory=dict)
    language: str = "en"
    viewer_url: str | None = None
    package_url: str | None = None
    lei: str | None = None

    @property
    def fiscal_year(self) -> str:
        return self.period_end[:4]

    def as_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "EdgarFiling":
        figs = {k: TaggedFigure(**v) for k, v in (d.get("figures") or {}).items()}
        return EdgarFiling(**{**d, "figures": figs})


def _headers() -> dict:
    load_settings()
    contact = os.getenv("SEC_CONTACT")
    if not contact:
        raise SecContactMissing(
            "The SEC requires a contact in the User-Agent: set SEC_CONTACT=<your email> in .env")
    return {"User-Agent": f"annual-report-extractor/0.1 {contact}",
            "Accept-Encoding": "gzip, deflate"}


class _Retryable(Exception):
    pass


@retry(retry=retry_if_exception_type((httpx.TransportError, _Retryable)),
       stop=stop_after_attempt(4), wait=wait_exponential(min=2, max=30), reraise=True)
def _get(url: str) -> httpx.Response:
    global _last_call
    pause = _MIN_INTERVAL_S - (time.monotonic() - _last_call)
    if pause > 0:
        time.sleep(pause)
    _last_call = time.monotonic()
    r = httpx.get(url, headers=_headers(), timeout=120, follow_redirects=True)
    if r.status_code == 429 or r.status_code >= 500:
        raise _Retryable(f"HTTP {r.status_code} for {url}")
    r.raise_for_status()
    return r


# --- company lookup ---------------------------------------------------------------

def _tickers() -> list[dict]:
    """SEC's list of registrants with a ticker (cached for a week)."""
    path = CACHE_DIR / "sec_company_tickers.json"
    if path.exists() and dt.datetime.now() - dt.datetime.fromtimestamp(path.stat().st_mtime) < TICKERS_MAX_AGE:
        return json.loads(path.read_text(encoding="utf-8"))
    rows = list(_get(TICKERS_URL).json().values())
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(rows), encoding="utf-8")
    return rows


# "APPLIED MATERIALS INC /DE", "ORACLE CORP /DE/", "XYZ CORP\\MD\\": state of incorporation
_STATE_SUFFIX = re.compile(r"\s*[/\\][A-Z]{2,3}[/\\]?\s*$")


def sec_title(title: str) -> str:
    """The registrant's name without the state-of-incorporation suffix."""
    return _STATE_SUFFIX.sub("", title).strip()


def find_cik(legal_name: str) -> tuple[int | None, str]:
    """CIK for the company, matched on name like the LEI lookup (legal forms
    compared as equivalents: "Eli Lilly and Company" = "ELI LILLY & Co"). Only an
    exact base-name match counts; several CIKs for one name = ambiguous."""
    rows = _tickers()
    exact = {r["cik_str"]: r["title"] for r in rows
             if match_level(legal_name, sec_title(r["title"])) == "exact"}
    if len(exact) == 1:
        cik, title = next(iter(exact.items()))
        return cik, f"exact name match ({title})"
    if len(exact) > 1:
        return None, f"ambiguous: {len(exact)} SEC registrants named like {legal_name!r}"
    return None, "no SEC registrant with this name"


# --- the filing -------------------------------------------------------------------

def latest_annual(cik: int) -> dict | None:
    """The newest annual report filing (10-K / 20-F / 40-F) from the submissions API."""
    rec = _get(SUBMISSIONS_URL.format(cik=cik)).json()
    recent = rec.get("filings", {}).get("recent", {})
    for i, form in enumerate(recent.get("form", [])):
        if form in ANNUAL_FORMS and recent["primaryDocument"][i]:
            return {"name": rec.get("name"), "form": form,
                    "accession": recent["accessionNumber"][i],
                    "filed": recent["filingDate"][i],
                    "period_end": recent["reportDate"][i] or recent["filingDate"][i],
                    "document": recent["primaryDocument"][i]}
    return None


def _day(s: str) -> dt.date:
    return dt.date.fromisoformat(s[:10])


def tagged_figures(facts: dict, accession: str, period_end: str) -> dict[str, TaggedFigure]:
    """Revenue (12 months ending period_end), assets and liabilities+equity (at
    period_end), as tagged in this filing (accession)."""
    end = _day(period_end)
    out: dict[str, TaggedFigure] = {}

    def pick(concepts, duration: bool):
        for taxonomy, concept in concepts:
            units = facts.get("facts", {}).get(taxonomy, {}).get(concept, {}).get("units", {})
            for unit, rows in units.items():
                for r in rows:
                    if r.get("accn") != accession or "end" not in r or _day(r["end"]) != end:
                        continue
                    if duration:
                        if "start" not in r or not 350 <= (end - _day(r["start"])).days <= 380:
                            continue
                        period = f"{r['start']}/{r['end']}"
                    elif "start" in r:
                        continue
                    else:
                        period = r["end"]
                    return TaggedFigure(float(r["val"]), unit.upper(), f"{taxonomy}:{concept}", period)
        return None

    for key, concepts, duration in (("revenue", REVENUE_CONCEPTS, True),
                                    ("total_assets", ASSETS_CONCEPTS, False),
                                    ("total_equity_and_liabilities", EQUITY_AND_LIABILITIES_CONCEPTS, False)):
        fig = pick(concepts, duration)
        if fig:
            out[key] = fig
    return out


def find_filing(legal_name: str) -> tuple[EdgarFiling | None, str]:
    """(filing, reason). The company's latest annual SEC filing with its tagged figures."""
    cik, why = find_cik(legal_name)
    if cik is None:
        return None, why
    meta = latest_annual(cik)
    if not meta:
        return None, f"CIK {cik}: no 10-K / 20-F / 40-F filed"
    accession = meta["accession"]
    try:
        facts = _get(FACTS_URL.format(cik=cik)).json()
        figures = tagged_figures(facts, accession, meta["period_end"])
    except httpx.HTTPStatusError as e:      # some filers have no XBRL facts
        log.info("No SEC company facts for CIK %s (%s)", cik, e.response.status_code)
        figures = {}
    doc_url = ARCHIVE_URL.format(cik=cik, accession=accession.replace("-", ""),
                                 document=meta["document"])
    filing = EdgarFiling(cik=cik, company=meta["name"] or "", form=meta["form"],
                         filing_id=accession, period_end=meta["period_end"],
                         filed=meta["filed"], report_url=doc_url, figures=figures)
    log.info("EDGAR: %s %s for FY%s (CIK %s), tagged %s", filing.company, filing.form,
             filing.fiscal_year, cik, sorted(figures))
    return filing, why


def download_report(filing: EdgarFiling) -> str:
    """The filing's main document (HTML) as text."""
    r = _get(filing.report_url)
    r.encoding = r.encoding or "utf-8"
    return r.text


# --- pay documents (python -m extractor.datapoints) -------------------------------

PROXY_FORMS = ("DEF 14A",)       # not DEFA14A: additional materials only
_ANCHOR = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
_PAY_LABEL = re.compile(r"remuneration|compensation report|executive compensation", re.I)


def latest_proxy(cik: int) -> dict | None:
    """The newest proxy statement (DEF 14A): where US companies publish executive pay."""
    rec = _get(SUBMISSIONS_URL.format(cik=cik)).json()
    recent = rec.get("filings", {}).get("recent", {})
    for i, form in enumerate(recent.get("form", [])):
        if form in PROXY_FORMS and recent["primaryDocument"][i]:
            return {"accession": recent["accessionNumber"][i], "filed": recent["filingDate"][i],
                    "document": recent["primaryDocument"][i]}
    return None


def pay_documents(cik: int) -> list[tuple[str, str]]:
    """(url, label) of the SEC documents holding executive pay, best first: exhibits of
    the latest annual filing labelled as a remuneration / compensation report (a
    foreign issuer's 20-F attaches its home-country report: Equinor's Exhibit 15.6),
    then the latest proxy statement (DEF 14A) for US filers. Free, no Firecrawl."""
    out: list[tuple[str, str]] = []
    meta = latest_annual(cik)
    if meta:
        folder = ARCHIVE_URL.format(cik=cik, accession=meta["accession"].replace("-", ""),
                                    document="")
        html = _get(folder + meta["document"]).text
        for href, text in _ANCHOR.findall(html):
            label = re.sub(r"<[^>]+>|\s+", " ", text).strip()
            if _PAY_LABEL.search(label) and "policy" not in label.lower() \
                    and re.search(r"\.(htm|html|pdf)$", href, re.I):
                url = href if href.startswith("http") else folder + href.split("/")[-1]
                if url not in (u for u, _ in out):
                    out.append((url, f"{label} ({meta['form']} exhibit)"))
    proxy = latest_proxy(cik)
    if proxy:
        out.append((ARCHIVE_URL.format(cik=cik, accession=proxy["accession"].replace("-", ""),
                                       document=proxy["document"]), "Proxy statement (DEF 14A)"))
    return out
