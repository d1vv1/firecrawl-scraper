"""Allshares Part 1 accuracy scoring engine.

The one place where gate rules live. Everything else (report data, Excel
outputs, tests) reads the scored output of score_tracker().

Scope: extraction accuracy only. Cross-source verification is out of scope,
so gates that need a second source (COD-04) stay NOT RUN.

Gate results: PASS, FAIL, NOT RUN. A gate that does not apply to a value is
simply not listed for it (N/A, excluded from all counts).

Value status:
  any hard FAIL            -> "Fail (hard)"
  else any NOT RUN         -> "Incomplete"
  else score = passed / applicable x 100
       score >= pass       -> "Pass"   (default 95)
       score >= review     -> "Review" (default 80)
       else                -> "Fail"

Open design decisions (see DECISIONS) are config values, not hard-coded
answers. Defaults reproduce the 3 Nov 2026 baseline run.
"""
import csv
import json
import math
import re
from collections import defaultdict

PASS, FAIL, NOT_RUN = "PASS", "FAIL", "NOT RUN"

# ---------------------------------------------------------------- gate catalogue
GATES = {
    "CORE-01": ("Locator present", "Hard"),
    "CORE-02": ("Snippet re-parses to same value", "Hard"),
    "CORE-03": ("Source registered", "Soft"),
    "CORE-04": ("As-of or period date present", "Soft"),
    "CORE-05": ("Schema type matches", "Soft"),
    "COD-01": ("Value in controlled list", "Hard"),
    "COD-02": ("Taxonomy or list version recorded", "Soft"),
    "COD-03": ("LEI format and check digits", "Hard"),
    "COD-04": ("Name matches source legal name", "Soft"),
    "COD-05": ("Status from fixed set", "Soft"),
    "COD-06": ("Fiscal year end is a valid date", "Hard"),
    "NUM-01": ("Currency is ISO 4217", "Hard"),
    "NUM-02": ("Units recorded", "Soft"),
    "NUM-03": ("Value annualised", "Soft"),
    "NUM-04": ("Magnitude in plausible range", "Soft"),
    "NUM-05": ("Counts whole; FTE <= headcount", "Hard"),
    "NUM-06": ("Percentages 0 to 100", "Hard"),
    "NUM-07": ("Combined holdings <= 100%", "Hard"),
    "NUM-08": ("Segments sum to total", "Soft"),
    "NUM-09": ("Valuation basis stated (grant, face, realised)", "Hard"),
    "NUM-10": ("Performance period recorded", "Soft"),
    "NUM-11": ("Payout <= maximum", "Hard"),
    "NUM-12": ("Period consistent across pay fields", "Soft"),
    "DES-01": ("Claim tied to locator", "Hard"),
    "DES-02": ("Enumerated value in allowed list", "Hard"),
    "DER-01": ("Formula recorded", "Soft"),
    "DER-02": ("Inputs pass own checks", "Hard"),
    "DER-03": ("Recalculation matches stored value", "Hard"),
    "DER-05": ("Denominator non-zero and result plausible", "Hard"),
    "DER-06": ("Marked as derived", "Soft"),
    "DER-07": ("Holdings share as-of date and basis", "Hard"),
    "DER-08": ("Entity consolidation applied", "Soft"),
    "DER-09": ("Ties listed explicitly", "Soft"),
    "XF-01": ("Total reconciles to components", "Hard"),
    "XF-03": ("Ratios recalculate from stored inputs", "Hard"),
}
CORE = ["CORE-01", "CORE-02", "CORE-03", "CORE-04", "CORE-05"]

# Field-specific gates per data point (CORE-01..05 apply to every value).
# Conditional gates are added in applicable_gates().
FIELD_GATES = {
    "legal_name": ["COD-04"],
    "lei": ["COD-03"],
    "country_code": ["COD-01"],
    "exchange": ["COD-01"],
    "sector_code": ["COD-01", "COD-02"],
    "accounting_basis": ["COD-01"],
    "listing_status": ["COD-05"],
    "fiscal_year_end": ["COD-06"],
    "role_disclosure": ["COD-01", "COD-02", "COD-05"],
    "revenue": ["NUM-01", "NUM-02", "NUM-04"],
    "ebitda": ["NUM-01", "NUM-02", "NUM-04"],
    "total_assets": ["NUM-01", "NUM-02", "NUM-04"],
    "shares_outstanding": ["NUM-02", "NUM-04"],
    "headcount": ["NUM-04", "NUM-05"],
    "fte": ["NUM-04", "NUM-05"],
    "revenue_by_country": ["NUM-02", "NUM-08"],
    "revenue_by_segment": ["NUM-02", "NUM-08"],
    "staff_by_country": ["NUM-02"],
    "staff_by_segment": ["NUM-02"],
    "largest_holders": ["NUM-06", "NUM-07", "DER-07", "DER-08", "DER-09"],
    "benefits": ["DES-01"],
    "shareholding_requirement": ["DES-01"],
    "pension_type": ["DES-01", "DES-02"],
    "pay_currency": ["NUM-01"],
    "base_salary": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-12"],
    "benefits_value": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-12"],
    "pension_contribution": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-12"],
    "sti_paid": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-10", "NUM-11", "NUM-12"],
    "sti_max": ["NUM-02", "NUM-03", "NUM-04", "NUM-10", "NUM-12"],
    "sti_target": ["NUM-02", "NUM-03", "NUM-04", "NUM-10", "NUM-12"],
    "lti_granted": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-09", "NUM-10", "NUM-12"],
    "lti_vested": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-09", "NUM-10", "NUM-12"],
    "lti_max": ["NUM-02", "NUM-03", "NUM-04", "NUM-09", "NUM-10", "NUM-12"],
    "lti_target": ["NUM-02", "NUM-03", "NUM-04", "NUM-09", "NUM-10", "NUM-12"],
    "total_remuneration": ["NUM-01", "NUM-02", "NUM-03", "NUM-04", "NUM-12", "XF-01"],
}
# Derived checks run on DERIVED values in these categories (Part 1 design list).
DER_CATEGORIES = {"Pay: total", "Pay: STI", "Pay: LTI", "Workforce",
                  "Segment and geography", "Role and disclosure", "Ownership and control"}
DER_GATES = ["DER-01", "DER-02", "DER-03", "DER-06"]
# Static fields: CORE-04 uses retrieved_at instead of a period date.
STATIC_CATEGORIES = {"Identity", "Listing and market", "Sector", "Reporting basis"}
PAY_FIELDS = ["base_salary", "benefits_value", "pension_contribution", "sti_paid", "sti_max",
              "sti_target", "lti_granted", "lti_vested", "lti_max", "lti_target", "total_remuneration"]
DATE_FIELDS = {"listing_date", "fiscal_year_end"}
NUMERIC_FIELDS = {"revenue", "ebitda", "total_assets", "shares_outstanding", "share_price", "headcount",
                  "fte", "aggregate_headcount", "fiscal_year"} | set(PAY_FIELDS)

# Protocol numeric field IDs: a found value needs a unit.
NUMERIC_FIELD_IDS = {"C12", "C13", "C14", "C16", "C17", "C18", "R02", "R04", "R05", "R06", "R07", "R08",
                     "R09", "R10", "R11"}
ISO_4217 = {"SEK", "NOK", "DKK", "EUR", "USD", "GBP", "CHF", "ISK", "PLN", "CAD", "AUD", "JPY", "CNY"}
UNIT_SCALE = {"thousands": 1e3, "millions": 1e6, "billions": 1e9, "units": 1}

# ---------------------------------------------------------------- configuration
DEFAULT_CONFIG = {
    "thresholds": {"pass": 95, "review": 80},
    # NUM-08: segments must sum to revenue within this share (open decision).
    "segment_tolerance": 0.01,
    # XF-01: total reconciles if within this share OR this absolute amount.
    "total_tolerance_pct": 0.01,
    "total_tolerance_abs": 1000,
    "total_components": ["base_salary", "benefits_value", "pension_contribution", "sti_paid", "lti_vested"],
    # NUM-06: STI percentages must lie in [0, sti_pct_cap]. 200% STI caps fail at 100 (open decision).
    "sti_pct_cap": 100,
    # NUM-11: tolerance on paid <= max (Allshares suggested 10%; not adopted).
    "sti_payout_tolerance": 0.0,
    # NUM-09: LTI 'form:' labels that count as a valuation basis (open decision).
    "lti_basis_ok": ["grant", "grant value", "face", "face value", "realised", "realized", "fair value"],
    # DES-02: pension_type keyword mapping (open decision).
    "pension_keywords": ["contribution", "premie", "premium", "benefit", "avgift", "fee", "pension"],
    # COD-01 accounting_basis allowed list.
    "accounting_basis_keywords": ["ifrs", "international financial reporting standards"],
    # NUM-05 FTE basis keywords (open decision: average vs year-end).
    "basis_average": ["average", "medel", "genomsnitt", "gennemsnit", "keskimäärin"],
    "basis_year_end": ["end of", "ultimo", "slut", "31 december", "as at", "as of", "lopussa", "per den",
                       "balance sheet date", "päättyessä", "utgång"],
    # NUM-04: reference ranges by (data_point, unit). Empty = NOT RUN until Allshares sets them.
    "reference_ranges": {},
}

DECISIONS = [
    # (id, decision, default used, effect on scoring, owner)
    ("D01", "LTI valuation basis mapping (which document labels count as grant, face or realised)",
     "Only grant / face / realised / fair value labels pass; shares, options, accounting expense, other fail",
     "NUM-09 fails all 92 LTI values", "Allshares"),
    ("D02", "STI cap: is a maximum above 100% of salary valid?",
     "Percentages must be 0-100 (sti_pct_cap = 100)", "200% caps fail NUM-06 (hard)", "Allshares"),
    ("D03", "Pension type keyword mapping (DES-02)",
     "Keywords: contribution, premie, premium, benefit, avgift, fee, pension (statutory-only wording fails)",
     "1 pension_type value fails DES-02", "Allshares"),
    ("D04", "Segment tolerance (NUM-08)", "1% of revenue", "9 segment splits fail (soft)", "Allshares"),
    ("D05", "FTE basis: average vs year-end (NUM-05)",
     "Compare FTE with headcount only when both are on the same stated basis; otherwise NOT RUN",
     "41 FTE values NOT RUN", "Allshares"),
    ("D06", "Reference magnitude ranges (NUM-04)",
     "None set: NUM-04 NOT RUN. Provisional sample ranges exist but are not applied",
     "945 values Incomplete on NUM-04", "Allshares"),
    ("D07", "ISO / taxonomy lists to load (ISO 3166, ISO 10383, national industry codes, list versions)",
     "ISO 3166 and industry code lists not loaded (COD-01 NOT RUN); versions not stored (COD-02 FAIL)",
     "64 COD-01 NOT RUN, 185 COD-02 FAIL", "Allshares"),
    ("D08", "Source ID: internal or printed?",
     "Generated internally at source registration; not printed in reports", "CORE-03 passes when a source is named",
     "Allshares"),
    ("D09", "Pass / Review thresholds", "Pass >= 95, Review >= 80 (configurable)", "Status split", "Allshares"),
    ("D10", "Total remuneration components and tolerance (XF-01)",
     "Base + benefits + pension + STI paid + LTI vested; within 1% or 1,000", "8 totals fail; 90 NOT RUN (a component missing)",
     "Allshares"),
    ("D11", "NUM-11 tolerance (Allshares suggested 10% on 2 Nov)", "0% (baseline); suggestion not applied",
     "8 STI payouts fail", "Allshares"),
    ("D12", "Annualisation (NUM-03) and performance period (NUM-10)",
     "NOT RUN: tracker has no months-in-role or performance period fields", "679 / 238 NOT RUN", "Allshares"),
]


def _num(s):
    """Parse a stored value as a number, or None."""
    if s is None:
        return None
    t = str(s).strip().replace("−", "-").replace(" ", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", t):
        return None
    return float(t)


def lei_valid(lei):
    if not re.fullmatch(r"[A-Z0-9]{18}[0-9]{2}", lei or ""):
        return False
    digits = "".join(str(int(ch, 36)) for ch in lei)
    return int(digits) % 97 == 1


def _iso_date(s):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", (s or "").strip())
    if not m:
        return False
    y, mo, d = map(int, m.groups())
    if not 1 <= mo <= 12:
        return False
    mdays = [31, 29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= d <= mdays[mo - 1]


def _has_snippet(row):
    return '"' in (row["note"] or "")


def _form(row):
    m = re.search(r"form:\s*([^;|]+)", row["note"] or "")
    return m.group(1).strip() if m else ""


def _pairs(value):
    """'A: 12; B: 3.5' -> [12.0, 3.5]"""
    out = []
    for part in re.split(r";", value or ""):
        if ":" in part:
            n = _num(part.rsplit(":", 1)[1])
            if n is not None:
                out.append(n)
    return out


def _percentages(value):
    return [float(x.replace(",", ".")) for x in re.findall(r"(-?\d+(?:[.,]\d+)?)\s*%", value or "")]


def _basis(note, cfg):
    t = (note or "").lower()
    if any(k in t for k in cfg["basis_average"]):
        return "average"
    if any(k in t for k in cfg["basis_year_end"]):
        return "year-end"
    return None


def _role_stem(role):
    return re.sub(r"\s*\(\d+\)\s*$", "", role or "")


def _scale(unit):
    for k, v in UNIT_SCALE.items():
        if k in (unit or "").lower():
            return v
    return 1


# ---------------------------------------------------------------- loading
def load_tracker(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows):
        r["_i"] = i
        for k in list(r):
            if isinstance(r[k], str):
                r[k] = r[k].strip() if k != "note" else r[k]
    return rows


def load_register(path):
    with open(path, encoding="utf-8") as f:
        return {x["data_point"]: x for x in json.load(f)}


# ---------------------------------------------------------------- scoring
def applicable_gates(row, reg):
    dp = row["data_point"]
    gates = list(CORE) + list(FIELD_GATES.get(dp, []))
    unit = row["unit"]
    if dp in ("sti_max", "sti_target") and "%" in unit:
        gates.insert(gates.index("NUM-10"), "NUM-06")
    if row["method"] == "DERIVED" and reg[dp]["category"] in DER_CATEGORIES:
        gates += DER_GATES
    return gates


class Context:
    """Lookups across rows of the same company and role."""

    def __init__(self, rows):
        self.by_company = defaultdict(dict)       # company_id -> data_point -> row (company grain)
        self.by_role = defaultdict(dict)          # (company_id, role) -> data_point -> row
        for r in rows:
            if not r["value"]:
                continue
            if r["grain"] == "role":
                self.by_role[(r["company_id"], r["role_row"])][r["data_point"]] = r
            else:
                self.by_company[r["company_id"]][r["data_point"]] = r

    def company(self, r, dp):
        return self.by_company[r["company_id"]].get(dp)

    def role(self, r, dp):
        return self.by_role[(r["company_id"], r["role_row"])].get(dp)

    def roles_like(self, r, dp):
        """Rows of dp whose role title matches r's once a trailing '(n)' is removed."""
        stem = _role_stem(r["role_row"])
        return [d[dp] for (cid, role), d in self.by_role.items()
                if cid == r["company_id"] and _role_stem(role) == stem and dp in d]


def evaluate(gate, r, reg, ctx, cfg):
    """Return (result, reason). Reason is empty for PASS."""
    dp, v, unit, note = r["data_point"], r["value"], r["unit"], r["note"] or ""
    cat = reg[dp]["category"]

    if gate == "CORE-01":
        return (PASS, "") if r["endpoint"] else (FAIL, "no locator (endpoint) recorded")
    if gate == "CORE-02":
        if "not found verbatim" in note:
            return FAIL, "snippet not found verbatim in source"
        if r["method"] in ("API", "XBRL"):
            return PASS, ""
        if _has_snippet(r):
            return PASS, ""
        return NOT_RUN, "no snippet recorded"
    if gate == "CORE-03":
        return (PASS, "") if r["source"] else (FAIL, "source not registered")
    if gate == "CORE-04":
        if cat in STATIC_CATEGORIES and (r["retrieved_at"] or r["period_end"]):
            return PASS, ""
        return (PASS, "") if r["period_end"] else (FAIL, "no as-of or period date")
    if gate == "CORE-05":
        if dp == "largest_holders" and not _percentages(v):
            return FAIL, "holder list has no percentages"
        if dp in DATE_FIELDS and not _iso_date(v):
            return FAIL, "not an ISO date"
        if dp in NUMERIC_FIELDS and _num(v) is None:
            return FAIL, "not a number"
        return PASS, ""

    if gate == "COD-01":
        if dp == "country_code":
            return NOT_RUN, "ISO 3166 list not loaded"
        if dp == "sector_code":
            return NOT_RUN, "national industry code list not loaded"
        if dp == "exchange":
            return (PASS, "") if re.fullmatch(r"[A-Z0-9]{4}", v) else (FAIL, "stored as exchange name, not an ISO 10383 MIC")
        if dp == "accounting_basis":
            ok = any(k in v.lower() for k in cfg["accounting_basis_keywords"])
            return (PASS, "") if ok else (FAIL, "accounting basis not in allowed list (IFRS)")
        if dp == "role_disclosure":
            return (PASS, "") if v in ("individual", "aggregate") else (FAIL, "not individual or aggregate")
    if gate == "COD-02":
        return FAIL, "taxonomy or list version not stored in tracker"
    if gate == "COD-03":
        return (PASS, "") if lei_valid(v) else (FAIL, "LEI fails ISO 17442 format or mod-97 check")
    if gate == "COD-04":
        return NOT_RUN, "cross-source name comparison, out of scope for this pass"
    if gate == "COD-05":
        allowed = {"listing_status": {"listed", "delisted", "suspended"},
                   "role_disclosure": {"individual", "aggregate"}}[dp]
        return (PASS, "") if v in allowed else (FAIL, "status not in fixed set")
    if gate == "COD-06":
        return (PASS, "") if _iso_date(v) else (FAIL, "fiscal year end is not a valid date")

    if gate == "NUM-01":
        code = v if dp == "pay_currency" else unit
        return (PASS, "") if code in ISO_4217 else (FAIL, 'currency "%s" is not ISO 4217' % (code or "blank"))
    if gate == "NUM-02":
        return (PASS, "") if unit else (FAIL, "unit not recorded")
    if gate == "NUM-03":
        return NOT_RUN, "annualisation basis not recorded in tracker"
    if gate == "NUM-04":
        rng = cfg["reference_ranges"].get("%s|%s" % (dp, unit))
        if not rng:
            return NOT_RUN, "plausible range not supplied by Allshares"
        n = _num(v)
        if n is None:
            return NOT_RUN, "value is not a number"
        return (PASS, "") if rng[0] <= n <= rng[1] else (FAIL, "outside range %s to %s" % (rng[0], rng[1]))
    if gate == "NUM-05":
        n = _num(v)
        if dp == "headcount":
            return (PASS, "") if n is not None and n == int(n) else (FAIL, "headcount is not a whole number")
        hc = ctx.company(r, "headcount")
        if not hc:
            return NOT_RUN, "no headcount row to compare with"
        b1, b2 = _basis(note, cfg), _basis(hc["note"], cfg)
        if not b1 or not b2:
            return NOT_RUN, "FTE or headcount basis (average or year-end) not stated"
        if b1 != b2:
            return NOT_RUN, "FTE is %s and headcount is %s: bases differ" % (b1, b2)
        h = _num(hc["value"])
        if n is None or h is None:
            return NOT_RUN, "FTE or headcount is not a number"
        return (PASS, "") if n <= h else (FAIL, "FTE %s above headcount %s" % (v, hc["value"]))
    if gate == "NUM-06":
        if dp == "largest_holders":
            ps = _percentages(v)
            if not ps:
                return NOT_RUN, "no percentages in holder list"
            bad = [p for p in ps if p < 0 or p > 100]
            return (PASS, "") if not bad else (FAIL, "percentage outside 0-100: %s" % bad[0])
        n = _num(v)
        cap = cfg["sti_pct_cap"]
        if n is None:
            return FAIL, "not a number"
        return (PASS, "") if 0 <= n <= cap else (FAIL, "%s%% is outside 0-%s%%" % (v, cap))
    if gate == "NUM-07":
        ps = _percentages(v)
        if not ps:
            return NOT_RUN, "no percentages in holder list"
        return (PASS, "") if sum(ps) <= 100 else (FAIL, "holdings sum to %.1f%%" % sum(ps))
    if gate == "NUM-08":
        rev = ctx.company(r, "revenue")
        revn = _num(rev["value"]) if rev else None
        if revn is None:
            return NOT_RUN, "no revenue to compare with"
        if revn == 0:
            return NOT_RUN, "revenue is zero"
        total = sum(_pairs(v)) * _scale(unit)
        gap = abs(total - revn) / abs(revn)
        if gap <= cfg["segment_tolerance"]:
            return PASS, ""
        return FAIL, "segments %s vs revenue %s (%.1f%% apart)" % (f"{total:,.0f}", f"{revn:,.0f}", gap * 100)
    if gate == "NUM-09":
        form = _form(r)
        if form.lower() in cfg["lti_basis_ok"]:
            return PASS, ""
        if form:
            return FAIL, 'form "%s" is an instrument or accounting label, not grant/face/realised' % form
        return FAIL, "no valuation basis recorded"
    if gate == "NUM-10":
        return NOT_RUN, "tracker has no performance period start and end fields"
    if gate == "NUM-11":
        mx = ctx.role(r, "sti_max")
        if not mx:
            return NOT_RUN, "no sti_max for this role"
        paid, mxv = _num(v), _num(mx["value"])
        if paid is None or mxv is None:
            return NOT_RUN, "paid or maximum STI is not a number"
        if "%" in mx["unit"]:
            base = ctx.role(r, "base_salary")
            bn = _num(base["value"]) if base else None
            if bn is None:
                return NOT_RUN, "no base salary to convert maximum STI %"
            cap_amt = mxv / 100 * bn
        else:
            cap_amt = mxv
        cap_amt *= 1 + cfg["sti_payout_tolerance"]
        return (PASS, "") if paid <= cap_amt else (FAIL, "paid %s above maximum %s" % (f"{paid:,.0f}", f"{cap_amt:,.0f}"))
    if gate == "NUM-12":
        if not r["period_end"]:
            return FAIL, "no period recorded for this pay value"
        others = [x["period_end"] for d, x in ctx.by_role[(r["company_id"], r["role_row"])].items()
                  if d in PAY_FIELDS and x is not r and x["period_end"]]
        if not others:
            return NOT_RUN, "no other pay field for this role to compare with"
        diff = sorted({p for p in others if p != r["period_end"]})
        return (PASS, "") if not diff else (FAIL, "period %s differs from %s" % (r["period_end"], diff[0]))

    if gate == "DES-01":
        return (PASS, "") if r["endpoint"] else (FAIL, "claim has no locator")
    if gate == "DES-02":
        ok = any(k in v.lower() for k in cfg["pension_keywords"])
        return (PASS, "") if ok else (FAIL, 'pension type "%s" not in allowed list' % v[:40])

    if gate == "DER-01":
        return (PASS, "") if ("derived" in note.lower() or "=" in note) else (FAIL, "formula not recorded")
    if gate == "DER-02":
        base = ctx.role(r, "base_salary")
        if not base:
            return NOT_RUN, "input base_salary not found for this role"
        if len(ctx.roles_like(r, "base_salary")) > 1:
            return NOT_RUN, "input base_salary ambiguous: several rows share this role title"
        return PASS, ""
    if gate == "DER-03":
        m = re.search(r"([\d.]+)\s*months? of salary", note)
        n = _num(v)
        if m and n is not None:
            return (PASS, "") if abs(float(m.group(1)) / 12 * 100 - n) < 0.5 else (FAIL, "recalculation differs")
        return PASS, ""
    if gate == "DER-06":
        return (PASS, "") if r["method"] == "DERIVED" else (FAIL, "not marked as derived")
    if gate == "DER-07":
        return (PASS, "") if r["period_end"] else (FAIL, "holdings have no as-of date")
    if gate == "DER-08":
        return NOT_RUN, "consolidation cannot be checked from the tracker"
    if gate == "DER-09":
        return NOT_RUN, "ties not recorded in tracker"

    if gate == "XF-01":
        missing = [c for c in cfg["total_components"] if not ctx.role(r, c)]
        if missing:
            return NOT_RUN, "component not found: " + ", ".join(missing)
        parts = [_num(ctx.role(r, c)["value"]) for c in cfg["total_components"]]
        total = _num(v)
        if total is None or any(p is None for p in parts):
            return NOT_RUN, "a component is not a number"
        s = sum(parts)
        if abs(s - total) <= max(cfg["total_tolerance_pct"] * abs(total), cfg["total_tolerance_abs"]):
            return PASS, ""
        return FAIL, "components sum %s vs stated %s (outside 1%% or 1,000)" % (f"{s:,.0f}", f"{total:,.0f}")

    raise ValueError("no rule for gate %s on %s" % (gate, dp))


def value_status(row, reg):
    """found / partial / not_found (protocol-style)."""
    if not row["value"]:
        return "not_found"
    dp = row["data_point"]
    needs_unit = reg[dp]["field_id"] in NUMERIC_FIELD_IDS
    needs_period = reg[dp]["category"] not in STATIC_CATEGORIES
    if (needs_unit and not row["unit"]) or (needs_period and not row["period_end"]):
        return "partial"
    return "found"


def score_value(gates, cfg):
    passed = sum(1 for g in gates if g["result"] == PASS)
    applicable = len(gates)
    hard_fail = [g["gate"] for g in gates if g["result"] == FAIL and GATES[g["gate"]][1] == "Hard"]
    not_run = sum(1 for g in gates if g["result"] == NOT_RUN)
    score = round(passed / applicable * 100) if applicable else 0
    t = cfg["thresholds"]
    if hard_fail:
        status = "Fail (hard)"
    elif not_run:
        status = "Incomplete"
    elif score >= t["pass"]:
        status = "Pass"
    elif score >= t["review"]:
        status = "Review"
    else:
        status = "Fail"
    return {"passed": passed, "applicable": applicable, "not_run": not_run, "score": score,
            "hard": hard_fail, "status": status}


def merge_config(overrides=None):
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    for k, v in (overrides or {}).items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            cfg[k].update(v)
        else:
            cfg[k] = v
    return cfg


def score_tracker(rows, reg, cfg=None):
    """Score every row. Blank values get value_status not_found and no gates."""
    cfg = cfg or merge_config()
    ctx = Context(rows)
    out = []
    for r in rows:
        rec = {"row": r, "value_status": value_status(r, reg), "gates": [], "result": None}
        if r["value"]:
            for g in applicable_gates(r, reg):
                res, why = evaluate(g, r, reg, ctx, cfg)
                rec["gates"].append({"gate": g, "result": res, "reason": why})
            rec["result"] = score_value(rec["gates"], cfg)
        out.append(rec)
    return out


def summarise(scored):
    """Totals used to check a run against the baseline."""
    st = defaultdict(int)
    gt = defaultdict(int)
    hard_fail = 0
    per_gate = defaultdict(lambda: defaultdict(int))
    for s in scored:
        if not s["result"]:
            continue
        st[s["result"]["status"]] += 1
        for g in s["gates"]:
            gt[g["result"]] += 1
            per_gate[g["gate"]][g["result"]] += 1
            if g["result"] == FAIL and GATES[g["gate"]][1] == "Hard":
                hard_fail += 1
    return {"values": sum(st.values()), "status": dict(st), "gates": dict(gt), "hard_fail": hard_fail,
            "per_gate": {k: dict(v) for k, v in per_gate.items()}}
