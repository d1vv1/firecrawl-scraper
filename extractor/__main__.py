"""CLI: python -m extractor "Unilever PLC" [--lei LEI] [--website URL] [--report-url URL] [--no-cache]"""

import argparse
import logging
import sys

from .config import OUTPUT_DIR, slugify
from .pipeline import run


def _fmt_money(m: dict) -> str:
    if m.get("value") is None:
        return f"not found ({m.get('not_found_reason')})"
    full = m.get("value_full")
    full_s = f" = {full:,.0f} {m['currency']}" if full is not None else ""
    return (f"{m['value']:,g} {m['currency']} {m['unit']} ({m['label_in_report']}, "
            f"{m['scope']}, pages {m.get('source_pages')}){full_s}")


def print_summary(r: dict) -> None:
    rm, bs = r["revenue_model"], r["business_structure"]
    fails = [c for c in r["checks"] if c["result"] == "fail"]
    lines = [
        "",
        f"Company:        {r['input_name']}",
        f"LEI:            {r['lei'] or '-'} ({r['lei_lookup']})",
        f"Website:        {r['website']} (via {r['website_source']})",
        f"Report:         {r['report_url']}",
        f"Fiscal year:    {r['fiscal_year']} (period end {r['period_end_date']})",
        f"Revenue:        {_fmt_money(r['revenue'])}",
        f"Total assets:   {_fmt_money(r['total_assets'])}",
        f"Revenue model:  {', '.join(rm['categories']) or '-'} | {rm['description']}",
        f"Structure:      {bs['legal_form']}, listed={bs['is_listed']}, "
        f"parent={bs['ultimate_parent']}, segments={bs['segments']}",
        f"Checks:         {sum(c['result'] == 'pass' for c in r['checks'])} pass, "
        f"{len(fails)} fail, {sum(c['result'] == 'skipped' for c in r['checks'])} skipped",
        *[f"  FAIL {c['name']}/{c['target']}: {c['detail']}" for c in fails],
        f"Firecrawl:      ~{r['firecrawl_credits_used']} credit(s) this run",
        f"STATUS:         {r['status']}",
        f"Output:         {r['_output_path']}",
    ]
    print("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor",
                                description="Extract annual-report data for one company.")
    p.add_argument("legal_name", help='Company legal name, e.g. "Unilever PLC"')
    p.add_argument("--website", help="Official website URL (skips step 2)")
    p.add_argument("--report-url", help="Annual report URL (skips steps 2 and 3)")
    p.add_argument("--lei", help="Company LEI (skips the GLEIF name lookup)")
    p.add_argument("--no-cache", action="store_true", help="Ignore cached discovery/report files")
    p.add_argument("-v", "--verbose", action="store_true", help="Debug logging (shows dropped URLs)")
    args = p.parse_args(argv)

    OUTPUT_DIR.mkdir(exist_ok=True)
    log_file = OUTPUT_DIR / f"{slugify(args.legal_name)}.log"
    fmt = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)    # the file always has every candidate URL
    logging.basicConfig(level=logging.DEBUG, format=fmt, handlers=[console, file_handler])
    for noisy in ("httpx", "httpcore", "openai", "hpack", "urllib3", "firecrawl"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    try:
        result = run(args.legal_name, website=args.website, report_url=args.report_url,
                     use_cache=not args.no_cache, lei=args.lei)
    except Exception as e:  # noqa: BLE001 - report any failure clearly and exit non-zero
        logging.getLogger("extractor").debug("Pipeline failed", exc_info=True)
        print(f"\nERROR ({type(e).__name__}): {e}\nFull log: {log_file}", file=sys.stderr)
        return 1
    print_summary(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
