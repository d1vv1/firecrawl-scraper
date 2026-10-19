"""The Monday build-test table: one row per fact and segment, in the PO's format.

    python -m extractor.monday companies.csv [--golden golden_values.csv]
                               [--sample-file output/sample_companies.csv]
                               [--out output/monday_table.csv]

Columns: field, segment, companies_tested, found, coverage_pct, checked, confirmed,
accuracy_pct, source, method, refresh, recommendation, notes

- companies_tested: sample companies in the segment that were processed.
- found: those with a value for the fact.
- checked / confirmed: for revenue and total assets, values compared with the golden
  dataset (same fiscal year, same currency, within ROUNDING_TOLERANCE); for the
  descriptive facts, values whose supporting quote was found in the report.
- recommendation: BUILD (coverage >= 80% and accuracy >= ACCURACY_BAR on enough checked
  values), BUY (coverage or accuracy clearly too low), REVIEW (borderline or too few
  checked values to judge), NOT_TESTED (fact not built yet).

The sample itself (--sample in the batch runner) is picked here too: N companies per
segment from the golden dataset, favouring companies with golden revenue, total assets
or employee figures, with a fixed seed so the same sample can be re-run.
"""

import argparse
import csv
import io
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from .config import OUTPUT_DIR, PROJECT_ROOT
from .validate import latest_year

# Segments the parse route covers ("other_unlisted_or_unknown" is the scrape route).
PARSE_SEGMENTS = ["nordic_listed", "europe_uk_listed", "us_listed", "nordic_uk_unlisted"]
SCORABLE_FIELDS = {"revenue", "total_assets", "fte"}
ACCURACY_BAR = 95.0           # working line until the PO sets one
COVERAGE_BAR = 80.0
MIN_CHECKED_TO_JUDGE = 10
ROUNDING_TOLERANCE = 0.01     # golden values are rounded to millions: 1% or 1 million

COLUMNS = ["field", "segment", "companies_tested", "found", "coverage_pct", "checked",
           "confirmed", "accuracy_pct", "source", "method", "refresh", "recommendation", "notes"]

# Facts of the parse route that aren't built yet: listed as NOT_TESTED so the gaps show.
NOT_BUILT = ["employees_fte", "employees_headcount", "controlling_owner", "pe_stake",
             "revenue_by_country", "staff_by_country", "pension_type",
             "shareholding_requirement", "sector"]
REFRESH = {"revenue": "yearly (annual report)", "total_assets": "yearly (annual report)",
           "revenue_model": "yearly (annual report)", "business_structure": "yearly (annual report)"}


# --- golden dataset ------------------------------------------------------------------

def load_golden(path: Path) -> dict[str, dict[str, list[dict]]]:
    """company_id -> field -> rows."""
    text = path.read_text(encoding="utf-8-sig")
    golden: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in csv.DictReader(io.StringIO(text)):
        golden[row["company_id"]][row["field"]].append(row)
    return golden


def _golden_number(rows: list[dict], year: int | None) -> tuple[dict | None, str]:
    """The golden row for our fiscal year, or (None, reason)."""
    if not rows:
        return None, "no golden value"
    same_year = [r for r in rows if year and str(year) in (r.get("fiscal_year"), r.get("year"))]
    if same_year:
        return same_year[0], ""
    years = sorted({r.get("fiscal_year") or r.get("year") or "?" for r in rows})
    return None, f"golden year {'/'.join(years)} vs ours {year}"


def compare_money(ours: dict, rows: list[dict], fiscal_year: str | None) -> tuple[str, str]:
    """('confirmed' | 'differs' | 'skipped', detail) for one money figure."""
    year = latest_year(fiscal_year)
    gold, why = _golden_number(rows, year)
    if gold is None:
        return "skipped", why
    if (gold.get("currency") or "").upper() != (ours.get("currency") or "").upper():
        return "skipped", f"currency {ours.get('currency')} vs golden {gold.get('currency')}"
    try:
        g = float(gold["value"]) * (1_000_000 if gold.get("unit") == "millions" else 1)
    except (TypeError, ValueError):
        return "skipped", "golden value not a number"
    o = ours.get("value_full")
    if o is None:
        return "skipped", "no value of ours"
    ok = abs(o - g) <= max(ROUNDING_TOLERANCE * abs(g), 1_000_000)
    return ("confirmed" if ok else "differs"), f"ours {o:,.0f} vs golden {g:,.0f}"


# --- sample --------------------------------------------------------------------------

def pick_sample(companies, golden: dict, n: int, seed: int = 7,
                segments=PARSE_SEGMENTS) -> list:
    """n companies per segment from the golden dataset; those with golden revenue,
    total assets or employee numbers first (they can be scored), then the rest."""
    rng = random.Random(seed)
    picked = []
    for seg in segments:
        in_seg = [c for c in companies if c.segment == seg and c.company_id in golden]
        scorable = [c for c in in_seg if SCORABLE_FIELDS & set(golden[c.company_id])]
        others = [c for c in in_seg if c not in scorable]
        rng.shuffle(scorable)
        rng.shuffle(others)
        picked += (scorable + others)[:n]
    return picked


def write_sample(sample, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["company_id", "company_name", "country_code", "segment", "lei"])
        for c in sample:
            w.writerow([c.company_id, c.name, c.country or "", c.segment or "", c.lei or ""])


# --- the table -----------------------------------------------------------------------

def _pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f}" if b else ""


def _recommend(tested: int, found: int, checked: int, confirmed: int) -> str:
    if not tested:
        return "NOT_TESTED"
    coverage = 100 * found / tested
    if checked < MIN_CHECKED_TO_JUDGE:
        return "REVIEW" if coverage >= COVERAGE_BAR / 2 else "BUY"
    accuracy = 100 * confirmed / checked
    if coverage >= COVERAGE_BAR and accuracy >= ACCURACY_BAR:
        return "BUILD"
    if coverage < COVERAGE_BAR / 2 or accuracy < ACCURACY_BAR - 15:
        return "BUY"
    return "REVIEW"


def _source_mix(results: list[dict]) -> str:
    esef = sum(1 for r in results if (r.get("data_source") or "").startswith("esef"))
    sec = sum(1 for r in results if (r.get("data_source") or "").startswith("edgar"))
    reg = sum(1 for r in results if (r.get("data_source") or "").startswith("registry"))
    web = len(results) - esef - sec - reg
    parts = []
    if esef:
        parts.append(f"filings.xbrl.org ESEF ({esef})")
    if sec:
        parts.append(f"SEC EDGAR 10-K/20-F ({sec})")
    if reg:
        parts.append(f"company registry filings ({reg})")
    if web:
        parts.append(f"company website reports ({web})")
    return "; ".join(parts)


def build_table(companies, golden: dict, output_dir: Path = OUTPUT_DIR) -> list[dict]:
    by_seg = defaultdict(list)
    for c in companies:
        by_seg[c.segment or "unknown"].append(c)
    rows = []
    for seg, cs in by_seg.items():
        results, errors = [], 0
        for c in cs:
            p = output_dir / f"{c.slug}.json"
            if p.exists():
                results.append(json.loads(p.read_text(encoding="utf-8")))
            elif (output_dir / f"{c.slug}.error.json").exists():
                errors += 1
        tested = len(results) + errors
        source = _source_mix(results)

        for field in ("revenue", "total_assets"):
            found = [r for r in results if (r.get(field) or {}).get("value_full") is not None]
            outcomes = [compare_money(r[field], golden.get(r["company_id"], {}).get(field, []),
                                      r.get("fiscal_year")) for r in found]
            checked = sum(1 for o, _ in outcomes if o != "skipped")
            confirmed = sum(1 for o, _ in outcomes if o == "confirmed")
            tagged = sum(1 for r in found if r[field].get("method") == "xbrl_tag")
            year_gaps = sum(1 for o, d in outcomes if o == "skipped" and d.startswith("golden year"))
            no_gold = sum(1 for o, d in outcomes if d == "no golden value")
            currency_gaps = [f"{r['company_id']}: {d}" for r, (o, d) in zip(found, outcomes)
                             if o == "skipped" and d.startswith("currency")]
            differs = [f"{r['company_id']}: {d}" for r, (o, d) in zip(found, outcomes) if o == "differs"]
            notes = [f"{tagged} read from XBRL tags, {len(found) - tagged} by AI from report text",
                     f"{errors} companies failed before extraction" if errors else "",
                     f"{year_gaps} not compared: golden value is for another year" if year_gaps else "",
                     f"{no_gold} have no golden value" if no_gold else "",
                     ("not compared, currency differs (re-check the golden label): "
                      + "; ".join(currency_gaps[:5])) if currency_gaps else "",
                     ("mismatches to re-check: " + "; ".join(differs[:5])) if differs else ""]
            rows.append({"field": field, "segment": seg, "companies_tested": tested,
                         "found": len(found), "coverage_pct": _pct(len(found), tested),
                         "checked": checked, "confirmed": confirmed,
                         "accuracy_pct": _pct(confirmed, checked), "source": source,
                         "method": "PARSE", "refresh": REFRESH[field],
                         "recommendation": _recommend(tested, len(found), checked, confirmed),
                         "notes": " | ".join(n for n in notes if n)})

        for field, has_value in (
                ("revenue_model", lambda r: bool(r["revenue_model"].get("categories"))),
                ("business_structure", lambda r: bool(r["business_structure"].get("segments")))):
            found = [r for r in results if has_value(r)]
            quote_ok = [r for r in found if any(
                ch["name"] == "quote" and ch["target"] == field and ch["result"] == "pass"
                for ch in r.get("checks", []))]
            rows.append({"field": field, "segment": seg, "companies_tested": tested,
                         "found": len(found), "coverage_pct": _pct(len(found), tested),
                         "checked": len(found), "confirmed": len(quote_ok),
                         "accuracy_pct": _pct(len(quote_ok), len(found)), "source": source,
                         "method": "PARSE", "refresh": REFRESH[field],
                         "recommendation": _recommend(tested, len(found), len(found), len(quote_ok)),
                         "notes": "no golden values: 'confirmed' = supporting quote found word "
                                  "for word in the report; an analyst sample is still needed"})

        for field in NOT_BUILT:
            rows.append({"field": field, "segment": seg, "companies_tested": 0, "found": "",
                         "coverage_pct": "", "checked": "", "confirmed": "", "accuracy_pct": "",
                         "source": "", "method": "PARSE", "refresh": "",
                         "recommendation": "NOT_TESTED", "notes": "not built yet"})
    return rows


def write_table(companies, golden_path: Path, out: Path) -> Path:
    rows = build_table(companies, load_golden(golden_path))
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return out


def main(argv: list[str] | None = None) -> int:
    from .batch import read_companies

    p = argparse.ArgumentParser(prog="python -m extractor.monday",
                                description="Monday build-test table from batch output.")
    p.add_argument("csv", type=Path, help="The full company CSV")
    p.add_argument("--golden", type=Path, default=PROJECT_ROOT / "golden_values.csv")
    p.add_argument("--sample-file", type=Path, default=OUTPUT_DIR / "sample_companies.csv",
                   help="Companies to score (written by the batch runner's --sample)")
    p.add_argument("--out", type=Path, default=OUTPUT_DIR / "monday_table.csv")
    args = p.parse_args(argv)
    try:
        source = args.sample_file if args.sample_file.exists() else args.csv
        companies = read_companies(source)
        out = write_table(companies, args.golden, args.out)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"Scored {len(companies)} companies from {source}")
    print(f"Saved to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
