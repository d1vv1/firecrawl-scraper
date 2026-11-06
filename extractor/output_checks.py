"""Checks on a data-point CSV, value by value (python -m extractor.output_checks).

Replaces the scoring in docs/allshares_part1_validation.html, which was a page of
results with no script behind it. The check names follow that page (CORE, COD, NUM,
DER, XF) so results can be compared, but:

  - every check is run here, by code, on the CSV and the cached source documents;
  - a check that doesn't apply to a value, or needs something the run doesn't have,
    is "n/a" with a reason: it never lowers a score and never blocks a status (on the
    page, one check that couldn't run made a value "Incomplete");
  - quotes are looked up again in the cached source text, not taken from the
    tool's own confidence grade; the page link must hold the quote;
  - fill rates are reported too (the page skipped blank values entirely).

Status of a value: "Fail (hard)" if a hard check fails; otherwise the score is
passed / applied checks: Pass at 95% or more, Review at 80% or more, else Fail.

  python -m extractor.output_checks output/nordic_uk_10_datapoints.csv
  python -m extractor.output_checks run.csv --out output/run_checks --ranges ranges.json

Writes <out>.md (the report) and <out>.csv (one row per value and check).
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .config import CACHE_DIR, OUTPUT_DIR
from .datapoints import MARKET_CAP_BANDS_EUR, OWNER_CATEGORY, OWNERSHIP_TYPE
from .scraper import markdown_to_pages
from .validate import ISO_4217, figure_in_quote, normalize, quote_in_text

PASS, REVIEW = 95.0, 80.0
TOTAL_TOLERANCE = 0.02           # protocol R11: parts vs stated total
SEGMENT_TOLERANCE = 0.05         # segments vs the company total
ISO_3166 = set("""
AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ
BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM
DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS
GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN
KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ
MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM
PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV
SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI
VN VU WF WS YE YT ZA ZM ZW XK
""".split())

CATEGORIES = {
    "Identity": ["legal_name", "other_names", "lei", "business_id", "cik", "country_code",
                 "head_office_city", "website"],
    "Listing and market": ["isin", "ticker", "exchange", "exchange_segment", "listing_status",
                           "listing_date", "market_cap_band"],
    "Sector": ["sector_code", "sub_sector"],
    "Reporting basis": ["fiscal_year", "fiscal_year_end", "reporting_currency", "accounting_basis"],
    "Financials": ["revenue", "total_assets", "ebitda", "shares_outstanding", "share_price"],
    "Workforce": ["headcount", "fte"],
    "Ownership and control": ["largest_holders", "controlling_owner", "controlling_owner_name",
                              "ownership_type", "pe_stake_5pct", "ultimate_parent"],
    "Segment and geography": ["revenue_by_segment", "staff_by_segment", "revenue_by_country",
                              "staff_by_country"],
    "Pay policy": ["pension_type", "benefits", "shareholding_requirement"],
    "Role and disclosure": ["role_disclosure", "aggregate_headcount", "pay_currency"],
    "Pay: fixed": ["base_salary", "benefits_value", "pension_contribution"],
    "Pay: STI": ["sti_paid", "sti_target", "sti_max"],
    "Pay: LTI": ["lti_vested", "lti_granted", "lti_target", "lti_max"],
    "Pay: total": ["total_remuneration"],
}
CATEGORY = {f: c for c, fs in CATEGORIES.items() for f in fs}

MONEY = {"revenue", "total_assets", "ebitda", "share_price", "base_salary", "sti_paid",
         "lti_vested", "lti_granted", "benefits_value", "pension_contribution",
         "total_remuneration"}
PAY_MONEY = MONEY - {"revenue", "total_assets", "ebitda", "share_price"}
COUNTS = {"headcount", "fte", "shares_outstanding", "aggregate_headcount"}
TARGETS = {"sti_target", "sti_max", "lti_target", "lti_max"}
NUMERIC = MONEY | COUNTS | TARGETS
BREAKDOWNS = {"revenue_by_segment", "staff_by_segment", "revenue_by_country", "staff_by_country"}
# Values that hold for a date or a period: they need one (CORE-04).
PERIODIC = (MONEY | COUNTS | TARGETS | BREAKDOWNS | {"pay_currency", "largest_holders",
            "controlling_owner", "controlling_owner_name", "ownership_type", "pe_stake_5pct"})
# Copied from the document: the value itself must be in the quote (CORE-02).
REPORT_LEVEL = {"fiscal_year", "fiscal_year_end", "reporting_currency", "pay_currency"}
VERBATIM = {"legal_name", "other_names", "head_office_city", "website", "ticker", "isin",
            "business_id", "exchange", "exchange_segment", "listing_date",
            "controlling_owner_name", "ultimate_parent"}
ALLOWED = {
    "listing_status": {"listed", "unlisted"},
    "controlling_owner": set(OWNER_CATEGORY.values()) | {"none"},
    "ownership_type": set(OWNERSHIP_TYPE.values()) | {"widely_held"},
    "pe_stake_5pct": {"yes", "no"},
    "role_disclosure": {"individual", "aggregate"},
    "market_cap_band": {name for _, name in MARKET_CAP_BANDS_EUR},
}
TARGET_UNITS = {"% of base salary", "% of maximum", "% of target", "shares", "instruments",
                "months of salary"}   # "% of target": as stated when no target is given
DEFAULT_RANGES = {   # plausible magnitudes in full units of the local currency
    "revenue": (0, 1e14), "total_assets": (0, 1e15), "ebitda": (-1e13, 1e13),
    "share_price": (0, 1e6), "headcount": (1, 5e6), "fte": (0.5, 5e6),
    "shares_outstanding": (1e3, 1e12), "aggregate_headcount": (1, 500),
    "base_salary": (0, 1e9), "sti_paid": (0, 5e9), "lti_vested": (0, 5e10),
    "lti_granted": (0, 5e10), "benefits_value": (0, 1e9), "pension_contribution": (0, 1e9),
    "total_remuneration": (0, 5e10),
}
SCALE = {"thousand": 1e3, "thousands": 1e3, "million": 1e6, "millions": 1e6,
         "billion": 1e9, "billions": 1e9, "units": 1, "lakhs": 1e5, "crores": 1e7}


# --- reading a row --------------------------------------------------------------

@dataclass
class Row:
    d: dict

    def __getattr__(self, k):
        return self.d.get(k, "")

    @property
    def number(self) -> float | None:
        try:
            return float(self.value)
        except ValueError:
            return None

    @property
    def quote(self) -> tuple[str | None, int | None]:
        """The quote in the note and the PDF page it was linked to."""
        m = re.search(r'(?:PDF page (\d+)|report text|web page): "', self.note)
        if not m:
            return None, None
        rest = self.note[m.end():]
        ends = [i for i in (rest.find('" (quote not found'), rest.find('"; ')) if i >= 0]
        q = rest[:min(ends)] if ends else rest.rstrip('"')
        return q.rstrip("…").strip(), int(m.group(1)) if m.group(1) else None

    @property
    def printed(self) -> tuple[float | None, float]:
        """(figure as printed, its multiplier) from 'printed 1242 thousands'."""
        m = re.search(r"printed (-?[\d.]+(?:e[+-]?\d+)?)(?: (\w+))?", self.note)
        if not m:
            return self.number, 1
        return float(m.group(1)), SCALE.get(m.group(2) or "", 1)

    @property
    def read_from_document(self) -> bool:
        return self.method in ("PARSE", "SCRAPE")


@dataclass
class Result:
    check: str
    outcome: str        # pass / fail / n/a
    reason: str = ""


def ok(check, reason=""):
    return Result(check, "pass", reason)


def bad(check, reason):
    return Result(check, "fail", reason)


def na(check, reason):
    return Result(check, "n/a", reason)


def self_clipped(r: "Row") -> bool:
    """The note's quote was shortened (datapoints.clip keeps 160 characters)."""
    return bool(re.search(r'…"', r.note))


def fmt(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:.6f}".rstrip("0").rstrip(".")


def same(a: float, b: float, tol: float = 0.005) -> bool:
    return abs(a - b) <= max(tol * abs(b), 1e-9)


def is_date(s: str) -> bool:
    try:
        dt.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def lei_ok(s: str) -> bool:
    """ISO 17442: 18 characters + 2 check digits, mod 97 = 1."""
    if not re.fullmatch(r"[A-Z0-9]{18}\d{2}", s):
        return False
    return int("".join(str(int(c, 36)) for c in s)) % 97 == 1


def isin_ok(s: str) -> bool:
    """ISO 6166: country, 9 characters, Luhn check digit."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", s):
        return False
    digits = "".join(str(int(c, 36)) for c in s[:-1])
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d) * (2 if i % 2 == 0 else 1)
        total += n // 10 + n % 10
    return (10 - total % 10) % 10 == int(s[-1])


def breakdown(value: str) -> list[tuple[str, float]]:
    out = []
    for part in value.split(";"):
        name, _, num = part.rpartition(":")
        try:
            out.append((name.strip(), float(num)))
        except ValueError:
            pass
    return out


# --- source documents ---------------------------------------------------------------

class Sources:
    """The cached text of the documents a run read, found by the endpoint URL."""

    def __init__(self, cache: Path = CACHE_DIR, output: Path = OUTPUT_DIR):
        self.cache, self.output = cache, output
        self._reports: dict[str, Path] | None = None
        self._pages: dict[str, dict[int, str] | None] = {}

    def reports(self) -> dict[str, Path]:
        """Annual-report URL -> its converted text, from the pipeline's result files."""
        if self._reports is None:
            self._reports = {}
            for p in self.output.glob("*.json"):
                try:
                    r = json.loads(p.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    continue
                md = ((r.get("debug") or {}) if isinstance(r, dict) else {}).get("markdown_file")
                if md and r.get("report_url"):
                    self._reports[r["report_url"]] = self.cache / md
        return self._reports

    def pages(self, endpoint: str) -> dict[int, str] | None:
        url = endpoint.split("#")[0]
        if url not in self._pages:
            self._pages[url] = self._load(url)
        return self._pages[url]

    def _load(self, url: str) -> dict[int, str] | None:
        variants = {url, url.rstrip("/")}
        for u in variants:
            h = hashlib.sha1(u.encode()).hexdigest()[:16]
            for path in list(self.cache.glob(f"*_doc_{h}.md")) + list(self.cache.glob(f"*_sec_{h}.md")):
                return {p.number: p.text for p in markdown_to_pages(path.read_text(encoding="utf-8"))}
        path = self.reports().get(url)
        if path and path.exists():
            return {p.number: p.text for p in markdown_to_pages(path.read_text(encoding="utf-8"))}
        return None


# --- the checks -------------------------------------------------------------------------

@dataclass
class Ctx:
    sources: Sources
    ranges: dict
    company: list[Row] = field(default_factory=list)

    def get(self, name: str, role: str = "") -> Row | None:
        return next((r for r in self.company if r.data_point == name and r.role_row == role
                     and r.value), None)


def core_01(r: Row, ctx: Ctx):
    """Locator: an http(s) endpoint; a PDF link opens at a page."""
    if not r.endpoint.startswith(("http://", "https://")):
        return bad("CORE-01", "no endpoint URL")
    if r.data_point in REPORT_LEVEL:
        return ok("CORE-01", "a fact about the whole report")
    if r.read_from_document and ".pdf" in r.endpoint.lower().split("#")[0] and "#page=" not in r.endpoint:
        return bad("CORE-01", "PDF link without #page=")
    return ok("CORE-01")


def core_02(r: Row, ctx: Ctx):
    """The value can be read off its quote."""
    if not r.read_from_document:
        return na("CORE-02", f"{r.method}: no quote, the endpoint is the source")
    if r.data_point in REPORT_LEVEL:
        return na("CORE-02", "a fact about the whole report (its year, currency)")
    if r.data_point == "aggregate_headcount":
        return na("CORE-02", "often counted from a list of names or written in words")
    if r.data_point not in NUMERIC | VERBATIM:
        return na("CORE-02", "a classification or summary, not copied from the text")
    q, _ = r.quote
    if not q:
        return bad("CORE-02", "no quote in the note")
    if r.data_point in NUMERIC:
        printed, _ = r.printed
        if printed is None:
            return bad("CORE-02", "value is not a number")
        # the figure as printed; with no "printed" note, also as a table "(000s)" or "m" prints it
        if figure_in_quote(printed, q, scaled="printed " not in r.note):
            return ok("CORE-02")
        if self_clipped(r):
            return na("CORE-02", "quote cut short in the note; the figure may be past the cut")
        return bad("CORE-02", f"{fmt(printed)} not in the quote")
    if r.data_point == "listing_date":
        parts = r.value.split("-")
        if all(p.isdigit() for p in parts):
            need = [int(parts[0])] + ([int(parts[2])] if len(parts) == 3 else [])
        else:
            # not an ISO date ("June 2008", COD-06 fails it): its own figures
            need = [int(x) for x in re.findall(r"\d+", r.value)]
        numbers = {int(x) for x in re.findall(r"\d+", normalize(q))}
        missing = [str(x) for x in need if x not in numbers]
        return bad("CORE-02", f"not in the quote: {' '.join(missing)}") if missing else ok("CORE-02")
    if r.data_point in VERBATIM:
        first = re.sub(r"\([^)]*\)", " ", re.split(r"[;,]", r.value)[0])   # "AB Volvo (publ)"
        words = re.findall(r"[a-z0-9]+", normalize(first))
        text = normalize(q)
        missing = [w for w in words if w not in text]
        return bad("CORE-02", f"not in the quote: {' '.join(missing)}") if missing else ok("CORE-02")
    return na("CORE-02", "a classification or summary, not copied from the text")


def core_03(r: Row, ctx: Ctx):
    """The quote is in the cached source text, on the linked page."""
    q, page = r.quote
    if not q:
        return na("CORE-03", f"{r.method}: no quote" if not r.read_from_document
                  else "no quote (see CORE-02)")
    if self_clipped(r):
        if "quote not found verbatim" in r.note:
            return bad("CORE-03", "the run did not find the full quote (the note keeps only its start)")
        # the cut can split a word or a figure ("|10,41…"): drop that last piece
        q = re.sub(r"[^\s|]*$", "", q).rstrip(" |") or q
    pages = ctx.sources.pages(r.endpoint)
    if pages is None:
        if "quote not found verbatim" in r.note:
            return bad("CORE-03", "source not cached; the run itself did not find the quote")
        return na("CORE-03", "source text not cached")
    if page:
        # the linked page, or the one before it (a quote can run over a page break)
        if any(quote_in_text(q, pages.get(n, "")) for n in (page, page - 1)):
            return ok("CORE-03")
        elsewhere = next((n for n, text in pages.items() if quote_in_text(q, text)), None)
        return bad("CORE-03", f"quote on page {elsewhere}, link says page {page}" if elsewhere
                   else "quote not in the source text")
    found = quote_in_text(q, "\n".join(pages.values()))
    return ok("CORE-03") if found else bad("CORE-03", "quote not in the source text")


def core_04(r: Row, ctx: Ctx):
    if r.data_point not in PERIODIC:
        return na("CORE-04", "holds without a date")
    if not r.period_end:
        return bad("CORE-04", "no period_end")
    return ok("CORE-04")


def core_05(r: Row, ctx: Ctx):
    """Type: numbers are numbers, dates are dates."""
    if r.data_point in NUMERIC and r.number is None:
        return bad("CORE-05", "not a number")
    if r.period_end and not (is_date(r.period_end) or re.fullmatch(r"\d{4}", r.period_end)):
        return bad("CORE-05", f"period_end {r.period_end!r} is not a date")
    if r.data_point in BREAKDOWNS and not breakdown(r.value):
        return bad("CORE-05", "breakdown not as 'name: number; ...'")
    return ok("CORE-05")


def cod_01(r: Row, ctx: Ctx):
    """Codes and closed sets."""
    v, name = r.value, r.data_point
    if name in ALLOWED:
        return ok("COD-01") if v in ALLOWED[name] else bad("COD-01", f"{v!r} not in the allowed set")
    if name == "country_code":
        return ok("COD-01") if v in ISO_3166 else bad("COD-01", f"{v} is not ISO 3166")
    if name in ("reporting_currency", "pay_currency"):
        return ok("COD-01") if v in ISO_4217 else bad("COD-01", f"{v} is not ISO 4217")
    if name == "exchange":
        from . import listing
        m = re.search(r"\bMIC ([A-Z0-9]{4})\b", r.note)
        mic = m.group(1) if m else listing.mic_for_name(v, ctx.get("country_code") and ctx.get("country_code").value)
        if not mic:
            return bad("COD-01", f"{v!r} matches no ISO 10383 exchange")
        try:
            known = mic in listing.mics()
        except Exception:  # noqa: BLE001 - no list, no check
            return na("COD-01", "ISO 10383 list not available")
        return ok("COD-01", mic) if known else bad("COD-01", f"{mic} not in ISO 10383")
    if name == "sector_code":
        from . import sector
        m = re.match(r"NACE (\d{2}\.\d{1,2})$", v)
        if m and sector.SCHEME == "NACE":
            return (ok("COD-01", "NACE Rev. 2 class") if m.group(1) in sector.taxonomy()
                    else bad("COD-01", f"{m.group(1)} is not a NACE Rev. 2 code"))
        return (ok("COD-01") if re.search(r"\d{2}", v)
                else bad("COD-01", "no industry code number"))
    if name in TARGETS:
        return ok("COD-01") if r.unit in TARGET_UNITS or r.unit in ISO_4217 \
            else bad("COD-01", f"unit {r.unit!r} is not a target form")
    return na("COD-01", "not a coded field")


def cod_02(r: Row, ctx: Ctx):
    """The classification scheme is named with the code."""
    if r.data_point != "sector_code":
        return na("COD-02", "not a classified field")
    return (ok("COD-02") if re.match(r"(NACE|SIC|TOL|NAICS|GICS|ICB)\b", r.value)
            else bad("COD-02", "scheme not named (NACE, SIC...)"))


def cod_03(r: Row, ctx: Ctx):
    """Identifier check digits."""
    if r.data_point == "lei":
        return ok("COD-03") if lei_ok(r.value) else bad("COD-03", "LEI check digits fail")
    if r.data_point == "isin":
        codes = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", r.value)
        wrong = [c for c in codes if not isin_ok(c)]
        if not codes:
            return bad("COD-03", "no ISIN")
        return bad("COD-03", f"check digit fails: {', '.join(wrong)}") if wrong else ok("COD-03")
    if r.data_point == "cik":
        return ok("COD-03") if r.value.isdigit() else bad("COD-03", "CIK is not a number")
    return na("COD-03", "not an identifier")


def cod_06(r: Row, ctx: Ctx):
    if r.data_point == "fiscal_year_end":
        return ok("COD-06") if is_date(r.value) else bad("COD-06", "not a valid date")
    if r.data_point == "listing_date":
        good = is_date(r.value) or re.fullmatch(r"(19|20)\d{2}", r.value)
        return ok("COD-06") if good else bad("COD-06", "not a year or a date")
    return na("COD-06", "not a date field")


def num_01(r: Row, ctx: Ctx):
    if r.data_point not in MONEY:
        return na("NUM-01", "not money")
    if r.unit == "instruments":
        return na("NUM-01", "a number of instruments, not money")
    return ok("NUM-01") if r.unit in ISO_4217 else bad("NUM-01", f"unit {r.unit!r} is not ISO 4217")


def num_02(r: Row, ctx: Ctx):
    """A money value read from a table keeps the figure and unit as printed."""
    if r.data_point not in MONEY or not r.read_from_document or r.data_point == "share_price":
        return na("NUM-02", "not a scaled figure read from a document")
    return ok("NUM-02") if "printed " in r.note else bad("NUM-02", "printed figure and unit not recorded")


def num_04(r: Row, ctx: Ctx):
    rng = ctx.ranges.get(r.data_point)
    if not rng or r.number is None:
        return na("NUM-04", "no range for this field")
    if r.unit == "instruments":
        return na("NUM-04", "a number of instruments")
    lo, hi = rng
    return ok("NUM-04") if lo <= r.number <= hi else bad("NUM-04", f"{r.number:g} outside {lo:g}..{hi:g}")


def num_05(r: Row, ctx: Ctx):
    if r.data_point not in COUNTS - {"fte"} or r.number is None:
        return na("NUM-05", "not a count")
    return ok("NUM-05") if r.number == int(r.number) else bad("NUM-05", "not a whole number")


def num_06(r: Row, ctx: Ctx):
    """Percentages in range: stakes and '% of maximum' 0-100, '% of base' 0-1000."""
    if r.data_point == "largest_holders":
        stakes = [float(x) for x in re.findall(r"(-?[\d.]+)%", r.value)]
        wrong = [s for s in stakes if not 0 <= s <= 100]
        return bad("NUM-06", f"stake {wrong[0]:g}%") if wrong else ok("NUM-06")
    if r.data_point in TARGETS and r.number is not None:
        hi = 100 if r.unit == "% of maximum" else 1000 if r.unit == "% of base salary" else None
        if hi is None:
            return na("NUM-06", "not a percentage")
        return ok("NUM-06") if 0 <= r.number <= hi else bad("NUM-06", f"{r.number:g} {r.unit}")
    return na("NUM-06", "no percentage")


def num_07(r: Row, ctx: Ctx):
    if r.data_point != "largest_holders":
        return na("NUM-07", "not a holdings list")
    total = sum(float(x) for x in re.findall(r"(-?[\d.]+)%", r.value))
    return ok("NUM-07") if total <= 100.5 else bad("NUM-07", f"holdings add up to {total:g}%")


def num_08(r: Row, ctx: Ctx):
    """A breakdown adds up to the company total (revenue or headcount)."""
    if r.data_point not in BREAKDOWNS:
        return na("NUM-08", "not a breakdown")
    whole = ctx.get("revenue" if r.data_point.startswith("revenue") else "headcount")
    items = breakdown(r.value)
    if not whole or whole.number is None or not items:
        return na("NUM-08", "no company total to compare with")
    unit = r.unit.split()
    if r.data_point.startswith("revenue") and (not unit or unit[0] != whole.unit):
        return na("NUM-08", "breakdown in another currency")
    scale = next((SCALE[u] for u in unit if u in SCALE), 1)
    total = sum(v for _, v in items) * scale
    if not whole.number:
        return na("NUM-08", "company total is zero")
    diff = abs(total - whole.number) / abs(whole.number)
    return ok("NUM-08") if diff <= SEGMENT_TOLERANCE else \
        bad("NUM-08", f"adds up to {total:,.0f} vs {whole.number:,.0f} ({diff:.1%} apart)")


def num_09(r: Row, ctx: Ctx):
    """An LTI amount says what it measures: granted (lti_granted), vested or paid out
    (lti_vested), or the IFRS 2 expense when that is all the report gives (the client's
    golden file uses the expensed figure then: BioArctic, Bang & Olufsen)."""
    if r.data_point not in ("lti_vested", "lti_granted"):
        return na("NUM-09", "not an LTI amount")
    if "form: accounting expense" in r.note:
        return ok("NUM-09", "expensed value (IFRS 2), stated in the note")
    return ok("NUM-09", "grant value" if r.data_point == "lti_granted" else "realised value")


def num_11(r: Row, ctx: Ctx):
    """STI paid is not above the maximum (as % of base salary)."""
    if r.data_point != "sti_paid" or r.number is None:
        return na("NUM-11", "not STI paid")
    mx, base = ctx.get("sti_max", r.role_row), ctx.get("base_salary", r.role_row)
    if not mx or not base or mx.unit != "% of base salary" or not base.number or mx.number is None:
        return na("NUM-11", "no maximum as % of base salary, or no base salary")
    pct = r.number / base.number * 100
    return ok("NUM-11") if pct <= mx.number * 1.02 else \
        bad("NUM-11", f"paid {pct:.0f}% of base, maximum {mx.number:g}%")


def num_12(r: Row, ctx: Ctx):
    """A role's amounts share one currency and one period."""
    if r.data_point not in PAY_MONEY or r.unit == "instruments":
        return na("NUM-12", "not a pay amount")
    peers = [x for x in ctx.company if x.role_row == r.role_row and x.data_point in PAY_MONEY
             and x.value and x.unit != "instruments"]
    cur = Counter(x.unit for x in peers).most_common(1)[0][0]
    per = Counter(x.period_end for x in peers).most_common(1)[0][0]
    if r.unit != cur:
        return bad("NUM-12", f"currency {r.unit}, the role's other amounts {cur}")
    if r.period_end != per:
        return bad("NUM-12", f"period {r.period_end}, the role's other amounts {per}")
    return ok("NUM-12")


def num_13(r: Row, ctx: Ctx):
    if r.data_point != "fte" or r.number is None:
        return na("NUM-13", "not FTE")
    head = ctx.get("headcount")
    if not head or head.number is None:
        return na("NUM-13", "no headcount to compare with")
    return ok("NUM-13") if r.number <= head.number * 1.10 else \
        bad("NUM-13", f"FTE {r.number:,.0f} above headcount {head.number:,.0f}")


def der_03(r: Row, ctx: Ctx):
    """A derived value recalculates from the inputs in its note."""
    if r.method != "DERIVED" or r.number is None:
        return na("DER-03", "not a derived number")
    n = r.note.replace(",", "")
    m = re.search(r"pension ([\d.]+) \+ salary addition in lieu of pension ([\d.]+)", n)
    if m:
        want = float(m.group(1)) + float(m.group(2))
    elif m := re.search(r"derived: ([\d.]+)% of the maximum of ([\d.]+)% of base", n):
        want = float(m.group(1)) * float(m.group(2)) / 100
    elif m := re.search(r"stated as ([\d.]+) months of salary", n):
        want = float(m.group(1)) / 12 * 100
    elif "printed " in n:
        p, mult = r.printed
        want = p * mult
    else:
        return na("DER-03", "no inputs in the note")
    return ok("DER-03") if same(r.number, want, 0.001) else \
        bad("DER-03", f"inputs give {want:,.2f}, value {r.number:,.2f}")


def der_06(r: Row, ctx: Ctx):
    if r.method != "DERIVED":
        return na("DER-06", "not derived")
    return ok("DER-06") if re.search(r"derived|=", r.note) else \
        bad("DER-06", "method DERIVED but the note gives no formula")


def _parts_and_total(r: Row, ctx: Ctx) -> tuple[float, float] | str:
    """(the parts' sum with the LTI that fits the total best, the total), or why not."""
    parts = [ctx.get(f, r.role_row) for f in ("base_salary", "sti_paid", "benefits_value",
                                               "pension_contribution")]
    parts = [p.number for p in parts if p and p.number is not None]
    if len(parts) < 2:
        return "fewer than two parts"
    lti = [p.number for p in (ctx.get("lti_vested", r.role_row), ctx.get("lti_granted", r.role_row))
           if p and p.number is not None and p.unit != "instruments"]
    options = [0] + lti + ([sum(lti)] if len(lti) == 2 else [])
    return min((sum(parts) + o for o in options), key=lambda s: abs(s - r.number)), r.number


def xf_01(r: Row, ctx: Ctx):
    """The parts are not more than the stated total: more means a figure is misread or
    counted twice."""
    if r.data_point != "total_remuneration" or not r.number:
        return na("XF-01", "not a total")
    got = _parts_and_total(r, ctx)
    if isinstance(got, str):
        return na("XF-01", got)
    parts, total = got
    if parts <= total * (1 + TOTAL_TOLERANCE):
        return ok("XF-01")
    return bad("XF-01", f"parts add up to {parts:,.0f}, more than the stated {total:,.0f}")


def xf_02(r: Row, ctx: Ctx):
    """The stated total equals its parts (protocol R11: a difference over 2% is noted).
    A total above the parts usually holds pay outside the fields (one-off, severance)."""
    if r.data_point != "total_remuneration" or not r.number:
        return na("XF-02", "not a total")
    got = _parts_and_total(r, ctx)
    if isinstance(got, str):
        return na("XF-02", got)
    parts, total = got
    if abs(parts - total) <= TOTAL_TOLERANCE * abs(total):
        return ok("XF-02")
    return bad("XF-02", f"parts add up to {parts:,.0f}, stated {total:,.0f}")


# (function, hard?) in report order
CHECKS = [
    (core_01, True, "Locator present (PDF links open at a page)"),
    (core_02, True, "Value can be read off its quote"),
    (core_03, True, "Quote is in the cached source, on the linked page"),
    (core_04, False, "Period end present (dated fields only)"),
    (core_05, False, "Type matches (number, date, breakdown)"),
    (cod_01, True, "Value in its code list or closed set"),
    (cod_02, False, "Classification scheme named"),
    (cod_03, True, "Identifier check digits (LEI, ISIN)"),
    (cod_06, True, "Dates are valid"),
    (num_01, True, "Money has an ISO 4217 currency"),
    (num_02, False, "Printed figure and unit recorded"),
    (num_04, False, "Magnitude in a plausible range"),
    (num_05, True, "Counts are whole numbers"),
    (num_06, True, "Percentages in range"),
    (num_07, True, "Holdings add up to 100% or less"),
    (num_08, False, "Breakdown adds up to the company total (5%)"),
    (num_09, False, "LTI says what it measures (granted, vested, expensed)"),
    (num_11, False, "STI paid not above its maximum"),
    (num_12, False, "A role's amounts share currency and period"),
    (num_13, False, "FTE not above headcount"),
    (der_03, True, "Derived value recalculates"),
    (der_06, False, "Derived value shows its formula"),
    (xf_01, True, "Parts not above the stated total (2%)"),
    (xf_02, False, "Total equals its parts (2%)"),
]
CHECK_ID = {fn: fn.__name__.upper().replace("_", "-", 1) for fn, _, _ in CHECKS}


@dataclass
class Scored:
    row: Row
    results: list[Result]
    hard_failed: list[str]
    score: float | None
    status: str


def score_row(r: Row, ctx: Ctx) -> Scored:
    results, hard_failed = [], []
    for fn, hard, _ in CHECKS:
        res = fn(r, ctx)
        results.append(res)
        if hard and res.outcome == "fail":
            hard_failed.append(res.check)
    applied = [x for x in results if x.outcome != "n/a"]
    score = 100 * sum(x.outcome == "pass" for x in applied) / len(applied) if applied else None
    status = ("Fail (hard)" if hard_failed else "Pass" if score is None or score >= PASS
              else "Review" if score >= REVIEW else "Fail")
    return Scored(r, results, hard_failed, score, status)


def run(csv_path: Path, sources: Sources, ranges: dict) -> tuple[list[Scored], list[Row]]:
    rows = [Row(d) for d in csv.DictReader(open(csv_path, encoding="utf-8-sig"))]
    by_company = defaultdict(list)
    for r in rows:
        by_company[r.company_id].append(r)
    scored = []
    for cid, company in by_company.items():
        ctx = Ctx(sources, ranges, company)
        scored += [score_row(r, ctx) for r in company if r.value]
    return scored, rows


# --- the report ---------------------------------------------------------------------------

STATUSES = ["Pass", "Review", "Fail", "Fail (hard)"]


def report(scored: list[Scored], rows: list[Row], name: str) -> str:
    n = len(scored)
    st = Counter(s.status for s in scored)
    pct = lambda k, tot=n: f"{st[k]} ({100 * st[k] / tot:.0f}%)" if tot else "0"  # noqa: E731
    companies = sorted({r.company_id for r in rows})
    lines = [f"# Output checks: {name}", "",
             f"{len(companies)} companies, {n} filled values checked ({dt.date.today().isoformat()}, "
             f"`python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't "
             f"count; quotes are looked up again in the cached source documents.", "",
             "| Status | Values |", "|---|---|"]
    lines += [f"| {k} | {pct(k)} |" for k in STATUSES]

    lines += ["", "## By category", "",
              "| Category | Values | Pass | Review | Fail | Fail (hard) |", "|---|---|---|---|---|---|"]
    for cat in list(CATEGORIES) + ["Other"]:
        sub = [s for s in scored if CATEGORY.get(s.row.data_point, "Other") == cat]
        if sub:
            c = Counter(s.status for s in sub)
            lines.append(f"| {cat} | {len(sub)} | " + " | ".join(str(c[k]) for k in STATUSES) + " |")

    lines += ["", "## By check", "",
              "| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |",
              "|---|---|---|---|---|---|---|---|"]
    for i, (fn, hard, title) in enumerate(CHECKS):
        res = [s.results[i] for s in scored]
        c = Counter(x.outcome for x in res)
        top = Counter(re.sub(r"[\d,.]+", "N", x.reason) for x in res if x.outcome == "fail").most_common(1)
        lines.append(f"| {CHECK_ID[fn]} | {title} | {'yes' if hard else ''} | {c['pass'] + c['fail']} | "
                     f"{c['pass']} | {c['fail']} | {c['n/a']} | {top[0][0] if top else ''} |")

    company_rows = [r for r in rows if r.grain == "company"]
    filled = Counter(r.data_point for r in company_rows if r.value)
    total = Counter(r.data_point for r in company_rows)
    fill = sum(filled.values()) / max(sum(total.values()), 1)
    lines += ["", "## Fill rate", "",
              f"Company fields: {sum(filled.values())} of {sum(total.values())} filled ({fill:.0%}). "
              f"Blank values are not checked above.", "",
              "| Field | Filled | Of |", "|---|---|---|"]
    lines += [f"| {f} | {filled[f]} | {total[f]} |" for f in sorted(total, key=lambda f: filled[f] / total[f])]
    roles = [r for r in rows if r.grain == "role"]
    execs = {(r.company_id, r.role_row) for r in roles if r.data_point == "base_salary"}
    if execs:
        rf = Counter(r.data_point for r in roles if r.value and (r.company_id, r.role_row) in execs)
        lines += ["", f"Pay fields, over {len(execs)} executive roles:", "", "| Field | Filled |", "|---|---|"]
        lines += [f"| {f} | {rf[f]} ({rf[f] / len(execs):.0%}) |" for f in
                  ("base_salary", "sti_paid", "sti_target", "sti_max", "lti_vested", "lti_granted",
                   "lti_target", "lti_max", "benefits_value", "pension_contribution", "total_remuneration")]

    fails = [s for s in scored if s.status in ("Fail (hard)", "Fail")]
    lines += ["", f"## Failed values ({len(fails)})", "",
              "| Company | Field | Role | Value | Status | Why |", "|---|---|---|---|---|---|"]
    for s in sorted(fails, key=lambda s: (s.row.company_id, s.row.data_point)):
        why = "; ".join(f"{x.check}: {x.reason}" for x in s.results if x.outcome == "fail")
        lines.append(f"| {s.row.company_id} | {s.row.data_point} | {s.row.role_row[:30]} | "
                     f"{s.row.value[:30]} | {s.status} | {why.replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def write_csv(scored: list[Scored], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["company_id", "data_point", "role_row", "value", "status", "score", "check",
                    "outcome", "reason"])
        for s in scored:
            for x in s.results:
                w.writerow([s.row.company_id, s.row.data_point, s.row.role_row, s.row.value,
                            s.status, "" if s.score is None else f"{s.score:.0f}", x.check,
                            x.outcome, x.reason])


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", type=Path, help="a data-point CSV from python -m extractor.datapoints")
    p.add_argument("--out", type=Path, help="report path without extension (default: next to the CSV)")
    p.add_argument("--ranges", type=Path, help="JSON {field: [min, max]} replacing the default ranges")
    p.add_argument("--cache", type=Path, default=CACHE_DIR, help="where the run cached its documents")
    p.add_argument("--results", type=Path, default=OUTPUT_DIR, help="the run's per-company result JSON")
    a = p.parse_args(argv)
    ranges = dict(DEFAULT_RANGES)
    if a.ranges:
        ranges.update({k: tuple(v) for k, v in json.loads(a.ranges.read_text(encoding="utf-8")).items()})
    scored, rows = run(a.csv, Sources(a.cache, a.results), ranges)
    out = a.out or a.csv.with_name(a.csv.stem + "_checks")
    out.with_suffix(".md").write_text(report(scored, rows, a.csv.name), encoding="utf-8")
    write_csv(scored, out.with_suffix(".csv"))
    st = Counter(s.status for s in scored)
    print(f"{len(scored)} values: " + ", ".join(f"{k} {st[k]}" for k in STATUSES))
    print(f"Report: {out.with_suffix('.md')}; details: {out.with_suffix('.csv')}")


if __name__ == "__main__":
    main()
