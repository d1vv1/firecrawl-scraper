"""Executive pay from one PDF: no search, no APIs, no other data points.

    python -m extractor.pay_from_pdf report.pdf --company "Equinor ASA"
    python -m extractor.pay_from_pdf rem.pdf --company "Volvo" --out volvo_pay.csv

The PDF (an annual report or a remuneration report) goes through the same pay route as
the full collector (datapoints.from_pay): the remuneration section is picked out, the
pay AI call reads it, Camelot reads the pay table where it can and code adds it up and
checks it against the table's total. The output is one CSV row per role and field, plus
the company-level pay terms (pension type, benefits, shareholding requirement), each
with its page, quote and grade. A scanned PDF is read from page images (ocr.py).
"""

import argparse
import csv
import hashlib
import logging
import sys
from dataclasses import asdict
from pathlib import Path

from . import ocr
from .config import CACHE_DIR, OUTPUT_DIR
from .datapoints import Origin, _now, from_pay
from .scraper import (NeedsOCRError, check_not_scanned, markdown_to_pages, pages_to_markdown,
                      pdf_to_pages)
from .sections import split_chunks

log = logging.getLogger(__name__)

COLUMNS = ["company", "grain", "role_row", "data_point", "value", "unit", "period_end",
           "confidence", "method", "source", "endpoint", "note"]


def pdf_origin(pdf: Path) -> tuple[Origin, str]:
    """The PDF as the document the pay route reads, and its cache key. The text is
    cached by the file's contents, so a second run reads no PDF and asks no AI."""
    key = "pdf_" + hashlib.sha1(pdf.read_bytes()).hexdigest()[:16]
    md = CACHE_DIR / f"{key}.md"
    if md.exists():
        pages = markdown_to_pages(md.read_text(encoding="utf-8"))
    else:
        pages = pdf_to_pages(pdf)
        try:
            check_not_scanned(pages)
        except NeedsOCRError:
            pages = ocr.pdf_pages(pdf)
            check_not_scanned(pages)
        CACHE_DIR.mkdir(exist_ok=True)
        md.write_text(pages_to_markdown(pages), encoding="utf-8")
    chunks = {c.id: c for c in split_chunks(pages)}
    origin = Origin("pdf", pdf.resolve().as_uri(), f"{pdf.name} (PDF)", "PARSE", _now(),
                    pages, chunks, pdf=pdf)
    return origin, key


def pay_rows(pdf: Path, company: str, period_end: str = "") -> list[dict]:
    origin, key = pdf_origin(pdf)
    roles, terms, read = from_pay(company, key, None, origin, key, period_end)
    if not roles:
        log.warning("No executive pay found in %s", pdf.name)
    return [{"company": company, **{k: v for k, v in asdict(f).items() if k in COLUMNS}}
            for f in roles + terms]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.pay_from_pdf",
                                description="Executive pay data from one PDF.")
    p.add_argument("pdf", type=Path, help="annual report or remuneration report (PDF)")
    p.add_argument("--company", help="the company's name (default: the file name)")
    p.add_argument("--period-end", default="", help="YYYY-MM-DD, written on each row")
    p.add_argument("--out", type=Path, help="CSV to write (default: output/<pdf name>_pay.csv)")
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    if not args.pdf.is_file():
        print(f"ERROR: no such file: {args.pdf}", file=sys.stderr)
        return 1
    company = args.company or args.pdf.stem
    try:
        rows = pay_rows(args.pdf, company, args.period_end)
    except NeedsOCRError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    out = args.out or OUTPUT_DIR / f"{args.pdf.stem}_pay.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    filled = [r for r in rows if r["value"] not in (None, "")]
    roles = sorted({r["role_row"] for r in rows if r["role_row"]})
    print(f"{len(filled)} pay values for {len(roles)} role(s) from {args.pdf.name}: {out}")
    for role in roles:
        got = {r["data_point"]: r["value"] for r in filled if r["role_row"] == role}
        print(f"  {role}: " + ", ".join(f"{k}={v}" for k, v in got.items()
                                        if k in ("base_salary", "sti_paid", "lti_vested",
                                                 "lti_granted", "total_remuneration")))
    return 0 if roles else 2


if __name__ == "__main__":
    raise SystemExit(main())
