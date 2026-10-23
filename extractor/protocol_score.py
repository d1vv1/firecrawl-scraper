"""Score our data points against the source-validation team's hand-checked results.

    python -m extractor.protocol_score output/datapoints.csv [Source_validation_listed_22Oct]

Companies are matched by name (our company_name = their `company`). Per protocol field:
  coverage  how often they found it and how often we did (the protocol's pass rule:
            90%+ passes, under 60% needs another source);
  values    where both have a value: numbers within 1% after the unit, codes (ISIN,
            register number, country, website) exactly; other fields are counted as
            found only. Role grain: each of their pay figures counts as matched if any of
            our role rows for that company has the same value, so role titles don't have
            to agree.
Writes output/protocol_score.md and prints the summary.
"""

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

from .config import OUTPUT_DIR

COMPANY_FIELDS = {
    "C01": ["legal_name"], "C02": ["lei"], "C03": ["business_id"], "C04": ["isin"], "C05": ["ticker"],
    "C06": ["exchange_segment"], "C07": ["listing_date"], "C08": ["country_code"],
    "C09": ["website"], "C10": ["sector_code"], "C11": ["sub_sector"], "C12": ["revenue"], "C13": ["total_assets"],
    "C14": ["ebitda"], "C15": ["fiscal_year_end"], "C16": ["headcount", "fte"],
    "C17": ["shares_outstanding"], "C18": ["share_price"], "C19": ["largest_holders"],
    "C20": ["controlling_owner"], "C21": ["ultimate_parent"],
    "C22": ["revenue_by_segment", "revenue_by_country"], "C23": ["pension_type"],
}
NOT_COLLECTED: dict[str, str] = {}
NUMERIC = {"C12", "C13", "C14", "C16", "C17", "C18"}
ROLE_FIELDS = {"R04": "base_salary", "R05": "sti_paid", "R07": "lti_received",
               "R09": "benefits_value", "R10": "pension_contribution", "R11": "total_remuneration"}
ROLE_PCT = {"R06": ("sti_target_pct", "sti_max_pct"), "R08": ("lti_target_pct", "lti_max_pct")}
SCALE = {"units": 1, "thousands": 1e3, "millions": 1e6, "billions": 1e9}
TOLERANCE = 0.01
FOUND = ("found", "partial")


def name_key(s: str) -> str:
    s = re.sub(r"\(.*?\)", " ", (s or "").lower())
    return re.sub(r"[^a-z0-9]", "", s)


def numbers(text: str) -> list[float]:
    """Numbers with ',' or ' ' as the thousands separator: '1,242,715', '1 292 435 282',
    '209380.50'."""
    out = []
    for m in re.findall(r"-?\d{1,3}(?:[, ]\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?", text or ""):
        try:
            out.append(float(re.sub(r"[, ]", "", m)))
        except ValueError:
            pass
    return out


def scale_of(unit: str) -> float:
    u = (unit or "").lower()
    return next((v for k, v in SCALE.items() if k in u), 1)


def close(a: float, b: float) -> bool:
    return a == b or (b != 0 and abs(a - b) / abs(b) <= TOLERANCE)


def compare(fid: str, theirs: dict, ours: list[dict]) -> str:
    """match / differs / found (no value comparison for this field)."""
    values = [r["value"] for r in ours if r["value"]]
    tv = theirs["value"]
    if fid in NUMERIC:
        nums = numbers(tv)
        if not nums:
            return "found"
        want = [n * scale_of(theirs["unit"]) for n in nums] + nums
        got = [float(v) for v in values if re.fullmatch(r"-?\d+(\.\d+)?", v)]
        return "match" if any(close(g, w) for g in got for w in want) else "differs"
    if fid == "C02":
        return "match" if any(v.upper() in tv.upper() for v in values) else "differs"
    if fid == "C04":
        codes = set(re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", tv.upper()))
        return "match" if any(c in codes for v in values for c in re.findall(
            r"[A-Z]{2}[A-Z0-9]{9}\d", v.upper())) else "differs"
    if fid == "C03":
        # any identifier in their text ("NIF A31065618 (... A-31065618)"), digits only
        theirs_ids = {re.sub(r"\D", "", t) for t in re.findall(r"[A-Z]*[\d][\d.\- ]{3,}\d", tv)}
        return "match" if any(re.sub(r"\D", "", v) in theirs_ids for v in values) else "differs"
    if fid == "C08":
        codes = set(re.findall(r"\b[A-Z]{2}\b", tv))
        return "match" if any(v[:2].upper() in codes for v in values) else "differs"
    if fid == "C09":
        return "match" if any(v.lower() in tv.lower() or tv.lower() in v.lower() for v in values) \
            else "differs"
    return "found"


def load(path: Path) -> list[dict]:
    return list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))


def score(ours_csv: Path, val_dir: Path) -> str:
    ours = load(ours_csv)
    val = [r for f in sorted(val_dir.glob("results_*.csv")) for r in load(f)]
    by_name = defaultdict(list)
    for r in ours:
        by_name[name_key(r["company_name"])].append(r)
    companies = sorted({r["company"] for r in val if name_key(r["company"]) in by_name})
    if not companies:
        return "No company in our output matches a company in the validation results."

    lines = [f"# Protocol score: {len(companies)} companies", "",
             "Companies: " + ", ".join(companies), "",
             "## Company grain", "",
             "| Field | They found | We found | Values match | Differ | Pass rule (ours) |",
             "|---|---|---|---|---|---|"]
    detail = ["", "## Differences", "", "| Company | Field | Theirs | Ours |", "|---|---|---|---|"]
    for fid, dps in COMPANY_FIELDS.items():
        they = we = match = differ = 0
        for comp in companies:
            mine = [r for r in by_name[name_key(comp)] if r["grain"] == "company"
                    and r["data_point"] in dps]
            t = next((r for r in val if r["company"] == comp and r["field_id"] == fid), None)
            has_ours = any(r["value"] for r in mine)
            we += has_ours
            if t and t["status"] in FOUND:
                they += 1
                if has_ours:
                    res = compare(fid, t, mine)
                    match += res == "match"
                    if res == "differs":
                        differ += 1
                        detail.append(f"| {comp} | {fid} | {t['value'][:60]} {t['unit']} | "
                                      + "; ".join(r["value"][:40] for r in mine if r["value"]) + " |")
        rate = we / len(companies)
        rule = "pass" if rate >= 0.9 else "fail" if rate < 0.6 else "weak"
        lines.append(f"| {fid} {'/'.join(dps)} | {they}/{len(companies)} | {we}/{len(companies)} | "
                     f"{match} | {differ} | {rule} ({rate:.0%}) |")
    for fid, why in NOT_COLLECTED.items():
        lines.append(f"| {fid} | | | | | not collected: {why} |")

    lines += ["", "## Role grain (their executive pay figures)", "",
              "| Field | Their figures | We have the same value | We have a different value | We have none |",
              "|---|---|---|---|---|"]
    for fid, dp in list(ROLE_FIELDS.items()) + list(ROLE_PCT.items()):
        total = same = other = none = 0
        for comp in companies:
            mine = [r for r in by_name[name_key(comp)] if r["grain"] == "role" and r["value"]
                    and r["data_point"] in ((dp,) if isinstance(dp, str) else dp)]
            got = [float(r["value"]) for r in mine if re.fullmatch(r"-?\d+(\.\d+)?", r["value"])]
            for t in (r for r in val if r["company"] == comp and r["field_id"] == fid
                      and r["status"] in FOUND):
                nums = numbers(t["value"])
                if not nums:
                    continue
                total += 1
                want = ([n * scale_of(t["unit"]) for n in nums] if isinstance(dp, str) else []) + nums
                if any(close(g, w) for g in got for w in want):
                    same += 1
                elif got:
                    other += 1
                else:
                    none += 1
        name = dp if isinstance(dp, str) else " / ".join(dp)
        lines.append(f"| {fid} {name} | {total} | {same} | {other} | {none} |")
    if len(detail) > 5:
        lines += detail
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.protocol_score",
                                description="Score data points against the validation results.")
    p.add_argument("ours", type=Path, help="our datapoints CSV")
    p.add_argument("validation", type=Path, nargs="?", default=Path("Source_validation_listed_22Oct"))
    p.add_argument("--out", type=Path, default=OUTPUT_DIR / "protocol_score.md")
    args = p.parse_args(argv)
    report = score(args.ours, args.validation)
    args.out.parent.mkdir(exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
