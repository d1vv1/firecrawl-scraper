"""Year-end share prices entered by hand (not-found plan, Phase C).

The exchanges' own price files can't be used: Athens allows personal use only and no bots,
SIX no commercial use without written consent, Euronext and the LSE no automated retrieval
(docs/not_found_reduction_plan.md, Phase C). So the prices still missing are looked up by
a person on the company's own share page (or the exchange's page, read by hand) and loaded
from a sheet:

    python -m extractor.manual_prices build [--into output/fy2025_runs_datapoints.csv]
        [--out output/manual_share_prices.csv]
    # fill in share_price, currency, price_date, source_url (and entered_by)
    python -m extractor.manual_prices load output/manual_share_prices.csv
        [--into output/fy2025_runs_datapoints.csv] [--no-dashboard]

`build` lists every company whose share_price is missing, with what helps find it (ISIN,
ticker, exchange, fiscal year end, website) and empty columns to fill in. A sheet already
there keeps what was filled in: only new companies are added.

`load` checks each filled row and writes it as the company's share_price: method MANUAL,
confidence B, the page as `endpoint`. It refuses a row whose date is after the fiscal
year end or more than 31 days before it, a currency that is not ISO 4217 (pence: "GBp",
"GBX" or "pence", divided by 100), or no http(s) source. Then the current rules run over
the file (combine), so the market-cap band is derived from the new price. A later run
that finds no price keeps the one entered by hand (combine.merge_company).
"""

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

from . import combine
from .config import OUTPUT_DIR
from .validate import ISO_4217

COMBINED = OUTPUT_DIR / "fy2025_runs_datapoints.csv"
SHEET = OUTPUT_DIR / "manual_share_prices.csv"
INFO = ["company_id", "company_name", "country", "isin", "ticker", "exchange", "fiscal_year_end",
        "price_wanted", "shares_outstanding", "reporting_currency", "website"]
FILL = ["share_price", "currency", "price_date", "source_url", "entered_by", "comment"]
SOURCE = "Share price (entered by hand)"
PENCE = {"gbp_pence": "GBP", "gbx": "GBP", "pence": "GBP", "p": "GBP"}
MAX_DAYS_BEFORE = 31
# FY2025: a fiscal year ending before this was read from an older report, whose year-end
# price is not wanted (that company needs its FY2025 report first)
FIRST_FYE = "2025-01-01"
LAST_FYE = "2026-06-30"


def _missing(r: dict) -> bool:
    note = r["note"].lower()
    return not r["value"] and not note.startswith(("not applicable", "not collected"))


def _companies(rows: list[dict]) -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {}
    for r in rows:
        if r["grain"] == "company":
            out.setdefault(r["company_id"], {})[r["data_point"]] = r
    return out


def price_wanted(fye: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fye or ""):
        return ("the closing price on the last trading day of the fiscal year (no fiscal year end "
                "read: find it in the FY2025 report)")
    if fye < FIRST_FYE:
        return (f"skip: the values were read from an older report (fiscal year end {fye}); "
                "the company needs its FY2025 report first")
    return (f"the closing price on the last day the share traded on or before {fye} "
            "(an exchange closed on the last day: the trading day before; give its date)")


def build(into: Path = COMBINED, out: Path = SHEET) -> tuple[int, int]:
    """Write the sheet. Returns (companies listed, of which new)."""
    rows, _ = combine.read(into)
    old = {}
    if out.exists():
        with open(out, encoding="utf-8-sig", newline="") as fh:
            old = {r["company_id"]: r for r in csv.DictReader(fh)}
    listed, new = [], 0
    for cid, by in _companies(rows).items():
        price = by.get("share_price")
        if not price or not _missing(price):
            continue
        v = lambda k: by.get(k, {}).get("value", "")
        info = {"company_id": cid, "company_name": price["company_name"], "country": price["country"],
                "isin": v("isin"), "ticker": v("ticker"), "exchange": v("exchange"),
                "fiscal_year_end": v("fiscal_year_end"), "price_wanted": price_wanted(v("fiscal_year_end")),
                "shares_outstanding": v("shares_outstanding"),
                "reporting_currency": v("reporting_currency"), "website": v("website")}
        if cid in old:
            info.update({k: old[cid].get(k, "") for k in FILL})
        else:
            new += 1
            info.update({k: "" for k in FILL})
        listed.append(info)
    # sheets of people's work: companies no longer missing stay, filled or not
    for cid, r in old.items():
        if cid not in {x["company_id"] for x in listed}:
            listed.append({k: r.get(k, "") for k in INFO + FILL})
    listed.sort(key=lambda r: (r["country"], r["company_name"]))
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=INFO + FILL)
        w.writeheader()
        w.writerows(listed)
    return len(listed), new


def _number(text: str) -> float | None:
    t = (text or "").strip().replace(" ", "").replace(" ", "").replace("'", "")
    if re.fullmatch(r"\d+,\d+", t):            # 12,34 (a decimal comma)
        t = t.replace(",", ".")
    t = t.replace(",", "")
    try:
        n = float(t)
    except ValueError:
        return None
    return n if n > 0 else None


def check(entry: dict, fye: str) -> tuple[dict | None, str]:
    """(the values to write, or None with why)."""
    price = _number(entry.get("share_price", ""))
    if price is None:
        return None, f"share_price {entry.get('share_price')!r} is not a positive number"
    cur = (entry.get("currency") or "").strip()
    in_pence = cur.lower().replace(" ", "_") in PENCE or cur == "GBp"
    if in_pence:
        price, cur = price / 100, "GBP"
    cur = cur.upper()
    if cur not in ISO_4217:
        return None, f"currency {entry.get('currency')!r} is not ISO 4217 (or GBp / pence)"
    date = (entry.get("price_date") or "").strip()
    try:
        day = dt.date.fromisoformat(date)
    except ValueError:
        return None, f"price_date {date!r} is not YYYY-MM-DD"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fye or "") and fye < FIRST_FYE:
        return None, f"the fiscal year end {fye} is from an older report, not FY2025"
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fye or "") and not FIRST_FYE <= date <= LAST_FYE:
        return None, f"no fiscal year end read, and price_date {date} is not in FY2025"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fye or ""):
        end = dt.date.fromisoformat(fye)
        if day > end:
            return None, f"price_date {date} is after the fiscal year end {fye}"
        if (end - day).days > MAX_DAYS_BEFORE:
            return None, f"price_date {date} is more than {MAX_DAYS_BEFORE} days before the fiscal year end {fye}"
    url = (entry.get("source_url") or "").strip()
    if not re.match(r"https?://", url):
        return None, "source_url is not an http(s) link"
    by = (entry.get("entered_by") or "").strip()
    note = (f"entered by hand{' by ' + by if by else ''}: closing price on {date}"
            f"{' (entered in pence)' if in_pence else ''}, from the page at the endpoint")
    if (entry.get("comment") or "").strip():
        note += f"; {entry['comment'].strip()}"
    return {"value": f"{price:g}", "unit": cur, "period_end": date, "source": SOURCE,
            "endpoint": url, "method": "MANUAL", "confidence": "B", "note": note,
            "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}, ""


def load(sheet: Path, into: Path = COMBINED, replace: bool = False) -> dict:
    """Write the filled rows into the combined file, then apply the current rules."""
    with open(sheet, encoding="utf-8-sig", newline="") as fh:
        entries = [e for e in csv.DictReader(fh) if (e.get("share_price") or "").strip()]
    rows, cols = combine.read(into)
    by = _companies(rows)
    stats = {"loaded": [], "refused": [], "skipped": []}
    for e in entries:
        cid = e["company_id"]
        price = by.get(cid, {}).get("share_price")
        if not price:
            stats["refused"].append((cid, "not in the combined file"))
            continue
        if price["value"] and price["method"] != "MANUAL" and not replace:
            stats["skipped"].append((cid, f"has a price read from {price['source'] or 'a source'}"))
            continue
        new, why = check(e, by[cid].get("fiscal_year_end", {}).get("value", ""))
        if not new:
            stats["refused"].append((cid, why))
            continue
        price.update(new)
        stats["loaded"].append(cid)
    combine.write(into, rows, cols)
    combine.combine([], into)            # the rules: the market-cap band from the new prices
    return stats


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.manual_prices", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="List the companies with no share price, to fill in")
    b.add_argument("--into", type=Path, default=COMBINED)
    b.add_argument("--out", type=Path, default=SHEET)
    lo = sub.add_parser("load", help="Load the filled-in prices into the combined file")
    lo.add_argument("sheet", type=Path)
    lo.add_argument("--into", type=Path, default=COMBINED)
    lo.add_argument("--replace", action="store_true", help="Also replace a price a run read")
    lo.add_argument("--no-dashboard", action="store_true")
    args = p.parse_args(argv)
    if args.cmd == "build":
        n, new = build(args.into, args.out)
        print(f"{args.out}: {n} companies ({new} new)")
        return 0
    stats = load(args.sheet, args.into, args.replace)
    print(f"{len(stats['loaded'])} prices loaded into {args.into}")
    for kind in ("refused", "skipped"):
        for cid, why in stats[kind]:
            print(f"  {kind}: {cid}: {why}")
    if not args.no_dashboard:
        from . import dashboard
        print(f"Scored again, dashboard: {dashboard.build(args.into, rescore=True)}")
    return 1 if stats["refused"] else 0


if __name__ == "__main__":
    sys.exit(main())
