"""Fill-rate report: how many companies got each data point, per country segment.

    python -m extractor.report companies.csv [--out output/fill_rate.md]

Each cell is "companies with a value / companies processed in the segment (fill rate)".
"Processed" = has a result or an error file; companies not reached yet are listed
separately and are not counted as misses. The batch runner writes this report
automatically at the end of every run.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .config import CACHE_DIR, OUTPUT_DIR
from .validate import latest_year

# (row label, function(result_or_None, company_context) -> bool)
# result is the company's output JSON (None if it errored); ctx has cached LEI/website.


def _money(r, key):
    return bool(r) and (r.get(key) or {}).get("value") is not None


def _recent(r):
    year = latest_year((r or {}).get("fiscal_year"))
    return year is not None and year >= dt.date.today().year - 2


def _source(r, kind):
    src = (r or {}).get("data_source") or "website"   # older outputs: website route only
    return bool(r) and (src.startswith(kind) if kind != "website" else src == "website")


def _bs(r, key):
    return bool(r) and bool((r.get("business_structure") or {}).get(key))


# Column order and names as in the PO's fill-rate table; other segments follow.
SEGMENT_NAMES = {
    "nordic_listed": "Nordic listed",
    "europe_uk_listed": "EU & UK listed",
    "us_listed": "US listed",
    "nordic_uk_unlisted": "Nordic & UK private",
    "other_unlisted_or_unknown": "Other",
}

# Facts in the PO's table that this tool doesn't extract yet: shown as "not built".
NOT_BUILT = ["Employees (FTE)", "Employees (headcount)", "Controlling owner", "PE stake ≥5%"]

ROWS = [
    ("LEI found", lambda r, ctx: bool(ctx["lei"])),
    ("Annual report found", lambda r, ctx: r is not None),
    ("… read from an ESEF filing (filings.xbrl.org)", lambda r, ctx: _source(r, "esef")),
    ("… read from an SEC filing (10-K / 20-F)", lambda r, ctx: _source(r, "edgar")),
    ("… read from a company registry filing (NO, DK)", lambda r, ctx: _source(r, "registry")),
    ("… read from the company website", lambda r, ctx: _source(r, "website")),
    ("Report is recent (FY within 2 years)", lambda r, ctx: _recent(r)),
    ("Revenue", lambda r, ctx: _money(r, "revenue")),
    ("Revenue, verified (all checks pass)", lambda r, ctx: _money(r, "revenue") and r["status"] == "ok"),
    ("Total assets", lambda r, ctx: _money(r, "total_assets")),
    ("Total assets, verified (all checks pass)",
     lambda r, ctx: _money(r, "total_assets") and r["status"] == "ok"),
    ("Revenue model (categories)", lambda r, ctx: bool(r and r["revenue_model"].get("categories"))),
    ("Revenue model (description)", lambda r, ctx: bool(r and r["revenue_model"].get("description"))),
    ("Business structure: segments", lambda r, ctx: bool(r and r["business_structure"].get("segments"))),
    ("Business structure: legal form", lambda r, ctx: bool(r and r["business_structure"].get("legal_form"))),
    ("Business structure: listed (yes/no)",
     lambda r, ctx: bool(r) and r["business_structure"].get("is_listed") is not None),
    ("Business structure: ultimate parent named", lambda r, ctx: _bs(r, "ultimate_parent")),
    ("Status ok (no review needed)", lambda r, ctx: bool(r) and r["status"] == "ok"),
]


def _load(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _context(slug: str, result: dict | None) -> dict:
    """LEI and website also for companies that errored later in the pipeline."""
    lei = (result or {}).get("lei")
    website = (result or {}).get("website")
    if not lei:
        lei = ((_load(CACHE_DIR / f"{slug}_lei.json") or {}).get("record") or {}).get("lei")
    if not website:
        website = (_load(CACHE_DIR / f"{slug}_discovery.json") or {}).get("website")
    return {"lei": lei, "website": website}


def _cell(n: int, d: int, bold: bool = False) -> str:
    text = f"{n:,} / {d:,} ({n / d:.1%})" if d else "–"
    return f"**{text}**" if bold else text


def build_report(companies, output_dir: Path = OUTPUT_DIR) -> str:
    """Markdown fill-rate table for the companies (from batch.read_companies)."""
    seg_of = {}
    processed: dict[str, list] = {}
    pending: dict[str, int] = {}
    for c in companies:
        seg = c.segment or c.country or "Unknown"   # the CSV's segment column if it has one
        seg_of[c.company_id] = seg
        result = _load(output_dir / f"{c.slug}.json")
        if result is None and not (output_dir / f"{c.slug}.error.json").exists():
            pending[seg] = pending.get(seg, 0) + 1
            continue
        processed.setdefault(seg, []).append((result, _context(c.slug, result)))

    order = list(SEGMENT_NAMES)
    segments = sorted({*processed, *pending},
                      key=lambda s: (order.index(s) if s in order else len(order),
                                     -(len(processed.get(s, [])) + pending.get(s, 0)), s))
    header = ["Data point", *(SEGMENT_NAMES.get(s, s) for s in segments), "**Total**"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]

    total_in_list = len(companies)
    row = ["Companies in the list"]
    for s in segments:
        row.append(f"{len(processed.get(s, [])) + pending.get(s, 0):,}")
    row.append(f"**{total_in_list:,}**")
    lines.append("| " + " | ".join(row) + " |")
    row = ["Processed so far"]
    all_processed = sum(len(v) for v in processed.values())
    for s in segments:
        n = len(processed.get(s, []))
        row.append(_cell(n, n + pending.get(s, 0)))
    row.append(_cell(all_processed, total_in_list, bold=True))
    lines.append("| " + " | ".join(row) + " |")

    for label, test in ROWS:
        row = [label]
        tot_n = 0
        for s in segments:
            items = processed.get(s, [])
            n = sum(1 for r, ctx in items if test(r, ctx))
            tot_n += n
            row.append(_cell(n, len(items)))
        row.append(_cell(tot_n, all_processed, bold=True))
        lines.append("| " + " | ".join(row) + " |")
    for label in NOT_BUILT:
        lines.append("| " + " | ".join([label, *("not built yet" for _ in segments), "–"]) + " |")

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    intro = (f"Fill rate per data point, generated {now}. Each cell shows **companies with a "
             f"value / companies processed in the segment (fill rate)**. {all_processed:,} of "
             f"{total_in_list:,} companies processed; the rest haven't been run yet and aren't "
             f"counted as misses.\n\n"
             f"*Verified* rows count a value only when every check on the financial figures and "
             f"the company passed (status `ok`): the quote is in the report, the number is in the "
             f"quote, consolidated figures, assets = equity + liabilities, recent fiscal year, "
             f"right company and currency.\n")
    return intro + "\n" + "\n".join(lines) + "\n"


def write_report(companies, out: Path) -> Path:
    out.write_text(build_report(companies), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    from .batch import read_companies

    p = argparse.ArgumentParser(prog="python -m extractor.report",
                                description="Fill-rate report from batch output.")
    p.add_argument("csv", type=Path, help="The same company CSV the batch ran on")
    p.add_argument("--out", type=Path, default=OUTPUT_DIR / "fill_rate.md")
    args = p.parse_args(argv)
    try:
        companies = read_companies(args.csv)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    write_report(companies, args.out)
    print(args.out.read_text(encoding="utf-8"))
    print(f"Saved to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
