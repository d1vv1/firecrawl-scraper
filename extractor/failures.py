"""Why a value is missing: one failure code per empty data point, and a report per run.

    python -m extractor.failures output/rerun_nordics_datapoints.csv [--only ID,ID]

Every empty row of a run gets a `Failure` code read from its note (the collector writes
why a value is missing in `note`: "not found in: ...", "not derived: ...", the route's
error). The codes are grouped by what fixes them, so a re-run plan can be read off the
counts: supply a link, top up credits, retry, or accept that the company does not state it.

At the end of every `python -m extractor.datapoints` run this writes, next to the run's CSV:
- `<run>_failures.csv`: one row per missing value of the companies the run processed:
  company, field, failure code, the note it was read from, and what to do;
- `<run>_failures.md`: counts per code, per field, and per company.
Rows the run did not ask for (NOT_COLLECTED) and fields that do not apply
(NOT_APPLICABLE) are counted but are not failures.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass(frozen=True)
class _Info:
    label: str
    action: str
    real: bool = True          # False: not a failure (not asked for, does not apply)
    retry: bool = False        # True: the same run again may find it


class Failure(str, Enum):
    """Why a data point has no value. Ordered from 'fix the input' to 'nothing to fix'."""

    # --- the source was never reached ----------------------------------------------
    WEBSITE_NOT_FOUND = "WEBSITE_NOT_FOUND"
    REPORT_NOT_FOUND = "REPORT_NOT_FOUND"
    REMUNERATION_REPORT_NOT_FOUND = "REMUNERATION_REPORT_NOT_FOUND"
    DOCUMENTS_NOT_FOUND = "DOCUMENTS_NOT_FOUND"
    NO_IDENTIFIER = "NO_IDENTIFIER"
    WRONG_YEAR_REPORT = "WRONG_YEAR_REPORT"
    # --- the run stopped short -----------------------------------------------------
    CREDITS_EXHAUSTED = "CREDITS_EXHAUSTED"
    DOCUMENT_UNREADABLE = "DOCUMENT_UNREADABLE"
    NETWORK_ERROR = "NETWORK_ERROR"
    # --- read, but the value could not be made ---------------------------------------
    DERIVATION_INPUT_MISSING = "DERIVATION_INPUT_MISSING"
    FX_RATE_MISSING = "FX_RATE_MISSING"
    STATED_IN_OTHER_FORM = "STATED_IN_OTHER_FORM"
    # --- read, and not there -------------------------------------------------------
    REMUNERATION_REPORT_NOT_READ = "REMUNERATION_REPORT_NOT_READ"
    NOT_DISCLOSED = "NOT_DISCLOSED"
    # --- not failures --------------------------------------------------------------
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_COLLECTED = "NOT_COLLECTED"
    UNKNOWN = "UNKNOWN"

    @property
    def info(self) -> _Info:
        return INFO[self]


INFO: dict[Failure, _Info] = {
    Failure.WEBSITE_NOT_FOUND: _Info(
        "Company website not found",
        "Fill in `website` (or `annual_report_url`) in the input and re-run"),
    Failure.REPORT_NOT_FOUND: _Info(
        "Annual report not found",
        "Put the FY annual report link (PDF, or a gs:// file) in `annual_report_url` and re-run"),
    Failure.REMUNERATION_REPORT_NOT_FOUND: _Info(
        "Remuneration report not found",
        "Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay"),
    Failure.DOCUMENTS_NOT_FOUND: _Info(
        "No usable company documents found",
        "Supply the report links; the site search found nothing usable"),
    Failure.NO_IDENTIFIER: _Info(
        "Needs an LEI or register number",
        "Add `lei` or `business_id` to the input: only an official register gives this field"),
    Failure.WRONG_YEAR_REPORT: _Info(
        "Values read from an older report",
        "Put the FY report link in `annual_report_url` and re-run with --redo"),
    Failure.CREDITS_EXHAUSTED: _Info(
        "Firecrawl credits ran out",
        "Top up credits (or raise --max-run-credits / --doc-credits) and re-run", retry=True),
    Failure.DOCUMENT_UNREADABLE: _Info(
        "Document could not be read",
        "Scanned or broken file: supply a text PDF, or check the download", retry=True),
    Failure.NETWORK_ERROR: _Info(
        "Network or site error",
        "Re-run; if it repeats, supply the document link", retry=True),
    Failure.DERIVATION_INPUT_MISSING: _Info(
        "Calculated field: an input is missing",
        "Fix the input field it rests on (share price, shares outstanding, business description)"),
    Failure.FX_RATE_MISSING: _Info(
        "Calculated field: no exchange rate",
        "Re-run the field (the API step gives the ECB rate), or fix the currency unit"),
    Failure.STATED_IN_OTHER_FORM: _Info(
        "Stated, but not in the form asked for",
        "Accept or review: e.g. a % of salary where an amount is asked"),
    Failure.REMUNERATION_REPORT_NOT_READ: _Info(
        "Pay field: only the annual report was read",
        "Supply the remuneration report in `remuneration_report_url` and re-run the field"),
    Failure.NOT_DISCLOSED: _Info(
        "Not stated in the documents read",
        "Review: the documents were read and do not state it; re-run only with a new source"),
    Failure.NOT_APPLICABLE: _Info("Does not apply", "Nothing to do", real=False),
    Failure.NOT_COLLECTED: _Info("Not asked for in this run", "Nothing to do", real=False),
    Failure.UNKNOWN: _Info("No reason recorded", "Check the company's log in output/"),
}

# The annual-report route's error (in "route failed: X" / "was not read (X: ...)").
_ROUTE = {
    "WebsiteNotFoundError": Failure.WEBSITE_NOT_FOUND,
    "ReportNotFoundError": Failure.REPORT_NOT_FOUND,
    "Firecrawl": Failure.CREDITS_EXHAUSTED,
    "CreditBudgetExceeded": Failure.CREDITS_EXHAUSTED,
    "NeedsOCRError": Failure.DOCUMENT_UNREADABLE,
    "ScannedPDFError": Failure.DOCUMENT_UNREADABLE,
    "DownloadError": Failure.DOCUMENT_UNREADABLE,
    "CertificateVerifyError": Failure.NETWORK_ERROR,
    "ConnectTimeout": Failure.NETWORK_ERROR,
    "ConnectError": Failure.NETWORK_ERROR,
    "ReadTimeout": Failure.NETWORK_ERROR,
}
_ROUTE_RE = re.compile(r"(?:route failed|was not read) ?[:(]\s*(\w+)")
# Sources that are registers or filings, not documents found on the company's site.
_REGISTERS = re.compile(r"GLEIF|ESMA FIRDS|OpenFIGI|SEC EDGAR$|PRH|Br.nn.ysund|Companies House$|register",
                        re.I)


_REM = re.compile(r"remuneration|compensation|proxy|DEF 14A|20-F|vergütung|ersättning|"
                  r"palkitsemis|godtgørelse|godtgjørelse", re.I)
_PAY_TERMS = {"pension_type", "benefits", "shareholding_requirement"}


def _is_pay(row: dict) -> bool:
    return row.get("grain") == "role" or row.get("data_point") in _PAY_TERMS


def _route(note: str) -> Failure | None:
    m = _ROUTE_RE.search(note)
    return _ROUTE.get(m.group(1), Failure.NETWORK_ERROR) if m else None


def _sources(note: str) -> list[str]:
    """'not found in: GLEIF, Annual report (PDF), company documents (none usable found)'
    -> the sources, without the route's error."""
    body = note.split("not found in:", 1)[1] if "not found in:" in note else ""
    body = re.split(r"\s*\((?:annual-report )?route failed", body)[0]
    return [p.strip() for p in re.split(r",\s*(?![^()]*\))", body) if p.strip()]


def classify(row: dict) -> Failure | None:
    """The failure code of a row; None when the row has a value."""
    if (row.get("value") or "").strip():
        return None
    note = (row.get("note") or "").strip()
    low = note.lower()
    if not note:
        return Failure.UNKNOWN
    if low.startswith("not collected"):
        return Failure.NOT_COLLECTED
    if low.startswith("not applicable"):
        return Failure.NOT_APPLICABLE
    if "out of credits" in low or "creditbudgetexceeded" in low:
        return Failure.CREDITS_EXHAUSTED
    if low.startswith("stated only as"):
        return Failure.STATED_IN_OTHER_FORM
    if low.startswith("not derived"):
        if "exchange rate" in low or "euro rate" in low:
            return Failure.FX_RATE_MISSING
        return Failure.DERIVATION_INPUT_MISSING
    if "no business description to classify" in low:
        return _route(note) or Failure.DERIVATION_INPUT_MISSING
    if "only an official api gives it" in low:
        return Failure.NO_IDENTIFIER
    if low.startswith("no remuneration report found"):
        return Failure.REMUNERATION_REPORT_NOT_FOUND
    if low.startswith("no source reached"):
        return _route(note) or Failure.DOCUMENTS_NOT_FOUND
    if low.startswith("not found: the annual report was not read"):
        return _route(note) or Failure.REPORT_NOT_FOUND
    if "not found in:" in low:
        sources = _sources(note)
        documents = [s for s in sources if not _REGISTERS.search(re.sub(r"\s*\(.*", "", s))]
        read = [s for s in documents if "none usable found" not in s and "skipped" not in s]
        if read:
            # a document was read and does not state it; for pay, say whether one of the
            # documents was a remuneration report (a proxy statement, a 20-F exhibit)
            if _is_pay(row) and not any(_REM.search(s) for s in read):
                return Failure.REMUNERATION_REPORT_NOT_READ
            return Failure.NOT_DISCLOSED
        route = _route(note)
        if route:
            return route
        if any("none usable found" in s for s in documents):
            return Failure.DOCUMENTS_NOT_FOUND
        return Failure.NOT_DISCLOSED            # only registers asked, and they don't have it
    return _route(note) or Failure.UNKNOWN


def target_year() -> int:
    return dt.date.today().year - 1


def failures(rows: list[dict], year: int | None = None) -> list[dict]:
    """One row per missing value: the data point rows with their failure code, plus a
    WRONG_YEAR_REPORT row for a company whose fiscal year is older than `year`."""
    year = year or target_year()
    out = []
    for r in rows:
        code = classify(r)
        if r.get("data_point") == "fiscal_year" and re.fullmatch(r"\d{4}", r.get("value") or "") \
                and int(r["value"]) < year:
            out.append(_row(r, Failure.WRONG_YEAR_REPORT, f"report read is FY{r['value']}, "
                                                          f"FY{year} wanted"))
        if code is not None:
            out.append(_row(r, code, r.get("note") or ""))
    return out


def _row(r: dict, code: Failure, reason: str) -> dict:
    return {"company_id": r.get("company_id", ""), "company_name": r.get("company_name", ""),
            "country": r.get("country", ""), "grain": r.get("grain", ""),
            "role_row": r.get("role_row", ""), "data_point": r.get("data_point", ""),
            "failure_code": code.value, "failure": code.info.label,
            "is_failure": "yes" if code.info.real else "no",
            "retry_may_help": "yes" if code.info.retry else "no",
            "action": code.info.action, "reason": reason,
            "sources_checked": "; ".join(_sources(reason))}


COLUMNS = ["company_id", "company_name", "country", "grain", "role_row", "data_point",
           "failure_code", "failure", "is_failure", "retry_may_help", "action", "reason",
           "sources_checked"]


def write(rows: list[dict], run_csv: Path, only: set[str] | None = None) -> tuple[Path, Path, list[dict]]:
    """`<run>_failures.csv` and `.md` for the run's rows (of the companies in `only`)."""
    if only is not None:
        rows = [r for r in rows if r.get("company_id") in only]
    fails = failures(rows)
    base = run_csv.with_name(run_csv.stem.removesuffix("_datapoints") + "_failures")
    csv_path, md_path = base.with_suffix(".csv"), base.with_suffix(".md")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(fails)
    md_path.write_text(_markdown(fails, run_csv), encoding="utf-8")
    return csv_path, md_path, fails


def _markdown(fails: list[dict], run_csv: Path) -> str:
    real = [f for f in fails if f["is_failure"] == "yes"]
    companies = {f["company_id"] for f in fails}
    by_code = Counter(f["failure_code"] for f in fails)
    lines = [f"# What the run could not find: {run_csv.name}", "",
             f"{len(real)} missing values in {len({f['company_id'] for f in real})} of "
             f"{len(companies)} companies (built {dt.date.today():%d %b %Y}). "
             "Not asked for and not applicable rows are counted but are not failures.", "",
             "## By reason", "", "| Code | Reason | Values | Companies | What to do |",
             "|---|---|---:|---:|---|"]
    for code in Failure:
        if by_code[code.value]:
            n_co = len({f["company_id"] for f in fails if f["failure_code"] == code.value})
            lines.append(f"| `{code.value}` | {code.info.label} | {by_code[code.value]} | {n_co} "
                         f"| {code.info.action if code.info.real else '-'} |")
    by_field = defaultdict(Counter)
    for f in real:
        by_field[f["data_point"]][f["failure_code"]] += 1
    lines += ["", "## By field", "", "| Field | Missing | Top reasons |", "|---|---:|---|"]
    for field, c in sorted(by_field.items(), key=lambda kv: -sum(kv[1].values())):
        top = ", ".join(f"{k} {v}" for k, v in c.most_common(3))
        lines.append(f"| {field} | {sum(c.values())} | {top} |")
    per = defaultdict(list)
    for f in real:
        per[(f["company_id"], f["company_name"])].append(f)
    lines += ["", "## By company", "", "| Company | Missing | Fields (reason) |", "|---|---:|---|"]
    for (cid, name), fs in sorted(per.items(), key=lambda kv: -len(kv[1])):
        grouped = defaultdict(set)
        for f in fs:
            grouped[f["failure_code"]].add(f["data_point"])
        detail = "; ".join(f"{code}: {', '.join(sorted(v))}" for code, v in grouped.items())
        lines.append(f"| {name} (`{cid}`) | {len(fs)} | {detail} |")
    return "\n".join(lines) + "\n"


def summary_lines(fails: list[dict], top: int = 8) -> list[str]:
    """A few console lines: missing values per failure code."""
    real = [f for f in fails if f["is_failure"] == "yes"]
    if not real:
        return ["Nothing missing among the fields asked for."]
    c = Counter(f["failure_code"] for f in real)
    out = [f"Not found: {len(real)} values in {len({f['company_id'] for f in real})} companies"]
    for code, n in c.most_common(top):
        out.append(f"  {code:<31} {n:>5}  {Failure(code).info.label}")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.failures",
                                description="Failure report (what was not found and why) for a run's CSV")
    p.add_argument("csv", type=Path, help="A run's <name>_datapoints.csv")
    p.add_argument("--only", help="Comma-separated company_ids")
    args = p.parse_args(argv)
    with open(args.csv, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    only = {x.strip() for x in args.only.split(",")} if args.only else None
    csv_path, md_path, fails = write(rows, args.csv, only)
    print("\n".join(summary_lines(fails)))
    print(f"Failure report: {csv_path} and {md_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
