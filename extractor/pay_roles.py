"""Role-based pay from the remuneration reports already on disk: no search, no Firecrawl,
no web; the only call out is the AI.

    python -m extractor.pay_roles --mode role --roles required --countries SE,NO,DK,FI --dry-run
    python -m extractor.pay_roles --mode role --roles required --countries SE,NO,DK,FI --workers 3
    python -m extractor.pay_roles --mode field --fields base_salary,sti_paid --only <company_id>
    python -m extractor.pay_roles --mode all --countries SE --run-id <run_id>      # resume

For each company of the list (default ../fy2025_pipeline_required.csv; `run_required` and the
gs:// URL columns are ignored):
  1. its remuneration report from the local folder (report_library.local_reports); none:
     `no_local_report` (with the annual report's name when there is one), never fetched;
  2. the report's text (pay_from_pdf.pdf_origin for a PDF, from_reports.read_pages for
     xhtml/html), and the pay chunks (datapoints._pay_chunks);
  3. one AI call with the mode's prompt (pay_roles_prompts.py), cached by the request
     (prompt, message, page images, role workbook version): a re-run asks nothing again;
  4. each line's role mapped in code (ref_roles.match); only a title the workbook does not
     know takes the AI's suggestion, with lower confidence.
Two companies that resolve to the same PDF (share lines: "Stora Enso A" and "Stora Enso R")
are read once: the first in list order gets the lines, the other `duplicate_of:<id>`.

Output, in output/pay_roles/<run_id>/:
  companies/<company_id>.json   one per company (resume: done companies are skipped;
                                <id>.error.json is retried only with --retry-failed)
  summary.csv                   one line per company
  run.json                      the request, model, prompt and workbook versions
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import llm, pay, ref_roles
from . import pay_roles_prompts as prompts
from . import report_library as rl
from .config import CACHE_DIR, OUTPUT_DIR, PROJECT_ROOT
from .pay_roles_schema import FIELDS

log = logging.getLogger(__name__)

DEFAULT_COMPANIES = PROJECT_ROOT.parent / "fy2025_pipeline_required.csv"
DEFAULT_CDP_REPO = PROJECT_ROOT.parent.parent / "Allshares-Centralized-Data-Hub"
RUNS_DIR = OUTPUT_DIR / "pay_roles"
CDP_TAXONOMY = "origin/master:backend/scripts/role_taxonomy.json"
CDP_LEVELS = ("L9", "L10")          # the CDP roles offered for lines no role_detail fits
IMAGE_TOKENS = 1900                 # about one landscape page at pay.IMAGE_DPI (pay.py)
SUMMARY_COLUMNS = ["company_id", "company_name", "country", "also_listed_as", "status", "note",
                   "match_type",
                   "source_file", "format", "fiscal_year", "period_end", "lines", "mapped_auto",
                   "mapped_suggestion", "unmapped", "cells", "prompt_tokens",
                   "completion_tokens", "cached", "seconds"]


# --- the request ---------------------------------------------------------------------------

@dataclass
class Request:
    mode: str
    fields: list[str]
    roles: list[str]                 # role_details (mode role), else []
    roles_spec: str
    images: bool
    ref_path: str
    cdp_roles: list[tuple[str, str]] | None = None


@dataclass
class Company:
    company_id: str
    company_name: str
    country: str
    lei: str
    report: dict | None = None       # the Report found, as a dict
    match_type: str = ""
    annual_file: str = ""
    duplicate_of: str = ""
    also_listed_as: list[str] = field(default_factory=list)   # same company_id, other rows


def read_companies(path: Path, countries: set[str], only: set[str], limit: int) -> list[Company]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out: list[Company] = []
    by_id: dict[str, Company] = {}
    for r in rows:
        cc = (r.get("country") or "").strip().upper()
        name = (r.get("company_name") or "").strip()
        cid = (r.get("company_id") or "").strip() or fallback_id(name, cc)
        if (countries and cc not in countries) or (only and cid not in only):
            continue
        if not (r.get("company_id") or "").strip():
            log.warning("%s (%s) has no company_id in the list: using %s", name, cc, cid)
        if cid in by_id:
            # share lines the list already gives one id ("SEB A" and "SEB C"): one company
            by_id[cid].also_listed_as.append(name)
            log.info("%s is listed again as %s: read once", by_id[cid].company_name, name)
            continue
        by_id[cid] = Company(cid, name, cc, (r.get("lei") or "").strip())
        out.append(by_id[cid])
    return out[:limit] if limit else out


def fallback_id(name: str, country: str) -> str:
    """A stable id for a list row with no company_id ("Stora Enso A" -> noid-stora-enso-a-se)."""
    slug = re.sub(r"[^a-z0-9]+", "-", ref_roles.norm(name)).strip("-")
    return f"noid-{slug}-{country.lower()}"


def find_reports(companies: list[Company], lib: rl.ReportRetriever) -> None:
    """Each company's remuneration report on disk, and which companies share one PDF."""
    first_by_path: dict[str, str] = {}
    for c in companies:
        reports, how = rl.local_reports(lib, c.company_name, c.country, c.lei or None)
        rem = reports.get("Remuneration")
        c.match_type = how
        if "Annual" in reports:
            c.annual_file = reports["Annual"].file_name
        if not rem:
            continue
        c.report = asdict(rem)
        key = os.path.normcase(os.path.abspath(rem.path))
        if key in first_by_path:
            c.duplicate_of = first_by_path[key]
        else:
            first_by_path[key] = c.company_id


def load_cdp_roles(repo: Path, ref: ref_roles.RefRoles) -> list[tuple[str, str]] | None:
    """The CDP's L9-L10 roles that no role_detail stands for, read with `git show` from the
    CDP repo's origin/master (its working tree is never touched). None when unreadable."""
    try:
        out = subprocess.run(["git", "-C", str(repo), "show", CDP_TAXONOMY], capture_output=True,
                             check=True, timeout=60).stdout
        taxonomy = json.loads(out.decode("utf-8"))
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        log.warning("CDP role taxonomy not read from %s (%s): no CDP list in the prompt", repo, e)
        return None
    linked = {row.get("cdp_role_id") for row in ref.details.values()}
    return [(r["role_id"], r["role_title_generic"]) for r in taxonomy
            if r.get("seniority_level") in CDP_LEVELS and r["role_id"] not in linked
            and "-V" not in r["role_id"]]


# --- one company -----------------------------------------------------------------------------

def read_origin(report: dict):
    """The report as the pay route reads it: pages, chunks and (for a PDF) the file."""
    from .datapoints import Origin, _now
    from .pay_from_pdf import pdf_origin
    from .sections import split_chunks

    path = Path(report["path"])
    if report["format"] == "pdf":
        return pdf_origin(path)
    from .from_reports import read_pages
    pages = read_pages(path)
    key = "file_" + hashlib.sha1(path.read_bytes()).hexdigest()[:16]
    chunks = {c.id: c for c in split_chunks(pages)}
    return Origin(report["format"], path.resolve().as_uri(), f"{path.name} ({report['format']})",
                  "PARSE", _now(), pages, chunks), key


class _Tokens(logging.Handler):
    """Counts the tokens llm.call_llm logs ("LLM %s: %d prompt + %d completion tokens")."""

    def __init__(self):
        super().__init__(logging.INFO)
        self.prompt = self.completion = 0

    def emit(self, record):
        if record.msg.startswith("LLM %s:") and len(record.args or ()) == 3:
            self.prompt += int(record.args[1])
            self.completion += int(record.args[2])


def pay_line_id(company_id: str, fiscal_year: str | None, line: dict) -> str:
    key = "|".join([company_id, fiscal_year or "", (line.get("printed_title") or "").strip(),
                    (line.get("person_name") or "").strip()]).casefold()
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def map_role(ref: ref_roles.RefRoles, line: dict, country: str,
             cdp_ids: set[str]) -> dict:
    """The line's role: the workbook title in it (source auto), else the AI's suggestion
    when it names a known role_detail (source suggestion) or, failing that, a CDP role from
    the list it was given (low), else unmapped."""
    suggested = line.get("suggested_role_detail") or ""
    m = ref.match(line.get("printed_title") or "", country)
    if m:
        out = {"role_detail": m.role_detail, "role_code": m.role_code,
               "cdp_role_id": m.cdp_role_id, "mapping_source": "auto",
               "mapping_confidence": m.confidence, "matched_title": m.title,
               "title_part_year": m.part_year, "title_flags": m.flags}
        if suggested and suggested != m.role_detail:
            out["note"] = f"AI suggested {suggested}"
        return out
    if suggested in ref.details:
        row = ref.details[suggested]
        return {"role_detail": suggested, "role_code": row["role_code"],
                "cdp_role_id": row.get("cdp_role_id") or "", "mapping_source": "suggestion",
                "mapping_confidence": "medium", "matched_title": "",
                "title_part_year": False, "title_flags": []}
    cdp = line.get("suggested_cdp_role_id") or ""
    if cdp in cdp_ids:
        return {"role_detail": "", "role_code": "", "cdp_role_id": cdp,
                "mapping_source": "suggestion", "mapping_confidence": "low",
                "matched_title": "", "title_part_year": False, "title_flags": []}
    note = f"AI suggested unknown {suggested!r}" if suggested else ""
    return {"role_detail": "", "role_code": "", "cdp_role_id": "", "mapping_source": "unmapped",
            "mapping_confidence": "", "matched_title": "", "title_part_year": False,
            "title_flags": [], **({"note": note} if note else {})}


def build_request(c: Company, req: Request, ref: ref_roles.RefRoles):
    """(origin, chunks, system prompt, user message, page numbers shown, request key)."""
    from .datapoints import _pay_chunks

    origin, _ = read_origin(c.report)
    chunks = _pay_chunks(origin, pay.PAY_WORDS)
    fields = prompts.fields_for(req.mode, req.fields)
    system = prompts.system_prompt(req.mode, fields)
    user = prompts.user_message(req.mode, company=c.company_name, source=c.report["file_name"],
                                what="the company's remuneration report", chunks=chunks,
                                ref=ref, country=c.country, selected=req.roles or None,
                                cdp_roles=req.cdp_roles)
    shown = (pay.table_pages(chunks, origin.page_text())
             if req.images and origin.pdf and Path(origin.pdf).exists() else [])
    if shown:
        user += pay.IMAGE_NOTE.format(pages=", ".join(map(str, shown)))
    key = prompts.request_key(system, user + f"|images:{shown}", ref.version)
    return origin, chunks, system, user, shown, key


def run_company(c: Company, req: Request, run_dir: Path, dry_run: bool = False) -> dict:
    """One company, start to end. Returns its summary row; writes companies/<id>.json."""
    started = time.monotonic()
    row = {"company_id": c.company_id, "company_name": c.company_name, "country": c.country,
           "also_listed_as": "; ".join(c.also_listed_as), "match_type": c.match_type,
           "source_file": (c.report or {}).get("file_name", ""),
           "format": (c.report or {}).get("format", "")}
    out = run_dir / "companies" / f"{c.company_id}.json"
    err = out.with_suffix(".error.json")

    def finish(status: str, note: str = "", **extra) -> dict:
        detail = extra.pop("_detail", {})
        row.update(status=status, note=note, seconds=round(time.monotonic() - started, 1), **extra)
        if not dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({**row, **detail}, ensure_ascii=False, indent=1),
                           encoding="utf-8")
            err.unlink(missing_ok=True)
        return row

    if not c.report:
        return finish("no_local_report", f"annual_only:{c.annual_file}" if c.annual_file else "")
    if c.duplicate_of:
        return finish(f"duplicate_of:{c.duplicate_of}", "same remuneration PDF")

    ref = ref_roles.load(req.ref_path)
    origin, chunks, system, user, shown, key = build_request(c, req, ref)
    if dry_run:
        est = (len(system) + len(user)) // 4 + IMAGE_TOKENS * len(shown)
        return finish("dry_run", f"{len(chunks)} chunk(s), {len(shown)} image page(s)",
                      prompt_tokens=est)

    cache = CACHE_DIR / f"payroles_{key}.json"
    tokens, cached = _Tokens(), cache.exists()
    if cached:
        saved = json.loads(cache.read_text(encoding="utf-8"))
        answer = saved["answer"]
        tokens.prompt, tokens.completion = saved.get("prompt_tokens", 0), saved.get("completion_tokens", 0)
    else:
        images = pay.page_images(Path(origin.pdf), shown) if shown else None
        schema = prompts.answer_schema(req.mode, prompts.fields_for(req.mode, req.fields))
        llm_log = logging.getLogger(llm.__name__)
        level = llm_log.level
        llm_log.setLevel(logging.INFO)          # the token line is INFO, whatever the setup
        llm_log.addHandler(tokens)
        try:
            answer = llm.call_llm(system, user, schema, images=images).model_dump()
        finally:
            llm_log.removeHandler(tokens)
            llm_log.setLevel(level)
        CACHE_DIR.mkdir(exist_ok=True)
        cache.write_text(json.dumps({"model": llm.model_name(), "request_key": key,
                                     "prompt_tokens": tokens.prompt,
                                     "completion_tokens": tokens.completion, "answer": answer},
                                    ensure_ascii=False, indent=1), encoding="utf-8")

    cdp_ids = {i for i, _ in req.cdp_roles or []}
    fy = answer.get("fiscal_year")
    lines = []
    for line in answer.get("lines", []):
        lines.append({"pay_line_id": pay_line_id(c.company_id, fy, line),
                      "mapping": map_role(ref, line, c.country, cdp_ids), "line": line})
    count = {s: sum(1 for x in lines if x["mapping"]["mapping_source"] == s)
             for s in ("auto", "suggestion", "unmapped")}
    cells = sum(1 for x in lines for f in FIELDS if isinstance(x["line"].get(f), dict)
                and x["line"][f].get("value") is not None)
    detail = {"run_mode": req.mode, "fields": prompts.fields_for(req.mode, req.fields),
              "roles": req.roles, "model": llm.model_name(), "request_key": key,
              "ref_roles_version": ref.version, "image_pages": shown,
              "report": c.report, "annual_file": c.annual_file, "lines": lines}
    return finish("ok" if lines else "no_lines", "" if lines else "the AI found no pay line",
                  fiscal_year=fy or "", period_end=answer.get("period_end") or "",
                  lines=len(lines), mapped_auto=count["auto"],
                  mapped_suggestion=count["suggestion"], unmapped=count["unmapped"],
                  cells=cells, prompt_tokens=tokens.prompt,
                  completion_tokens=tokens.completion, cached=cached, _detail=detail)


def _worker(c: Company, req: Request, run_dir: Path, dry_run: bool) -> dict:
    try:
        return run_company(c, req, run_dir, dry_run)
    except Exception as e:  # noqa: BLE001 - one company's failure must not stop the run
        log.exception("%s failed", c.company_id)
        if not dry_run:
            err = run_dir / "companies" / f"{c.company_id}.error.json"
            err.parent.mkdir(parents=True, exist_ok=True)
            err.write_text(json.dumps({"company_id": c.company_id, "error": repr(e)[:2000]},
                                      ensure_ascii=False, indent=1), encoding="utf-8")
        return {"company_id": c.company_id, "company_name": c.company_name,
                "country": c.country, "status": "error", "note": repr(e)[:300]}


def _worker_init(dry_run: bool = False) -> None:
    _setup_logging()
    if dry_run:
        from . import ocr
        ocr.ENABLED = False


def _setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    for noisy in ("httpx", "openai", "urllib3", "google"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


# --- the run --------------------------------------------------------------------------------

def write_summary(run_dir: Path, companies: list[Company], rows: dict[str, dict]) -> Path:
    """summary.csv from this run's rows, and for companies not run now, their saved files."""
    path = run_dir / "summary.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=SUMMARY_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for c in companies:
            row = rows.get(c.company_id)
            if row is None:
                done = run_dir / "companies" / f"{c.company_id}.json"
                failed = done.with_suffix(".error.json")
                if done.exists():
                    row = json.loads(done.read_text(encoding="utf-8"))
                elif failed.exists():
                    row = {"company_id": c.company_id, "company_name": c.company_name,
                           "country": c.country, "status": "error",
                           "note": json.loads(failed.read_text(encoding="utf-8"))["error"][:300]}
                else:
                    row = {"company_id": c.company_id, "company_name": c.company_name,
                           "country": c.country, "status": "not_run"}
            w.writerow(row)
    return path


def run_id_for(mode: str, spec: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", spec.lower()).strip("-")[:30] or "all"
    return f"{dt.datetime.now():%Y%m%d-%H%M}_{mode}_{slug}"


def git_commit() -> str:
    try:
        return subprocess.run(["git", "-C", str(PROJECT_ROOT), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.pay_roles",
                                description="Role-based pay from the remuneration reports on disk.")
    p.add_argument("--mode", required=True, choices=["field", "role", "all", "gapfill"])
    p.add_argument("--roles", default="required",
                   help="mode role: required | optional | all | role_details or codes, comma-separated")
    p.add_argument("--fields", default="", help="mode field: pay fields, comma-separated")
    p.add_argument("--companies", type=Path, default=DEFAULT_COMPANIES)
    p.add_argument("--countries", default="", help="ISO-2 codes, comma-separated (default: all)")
    p.add_argument("--only", default="", help="company_ids, comma-separated")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--run-id", default="", help="resume this run (default: a new one)")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--force", action="store_true", help="run companies already done again")
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--dry-run", action="store_true",
                   help="find and read the reports and build the prompts, but ask no AI")
    p.add_argument("--images", choices=["on", "off"], default=None,
                   help="attach pay-table page images (default: PAY_PAGE_IMAGES, as pay.py)")
    p.add_argument("--ref-roles", default=os.getenv("REF_ROLES_XLSX") or "",
                   help="the role workbook (default: REF_ROLES_XLSX or ../../Reports/ref_roles.xlsx)")
    p.add_argument("--cdp-repo", type=Path,
                   default=Path(os.getenv("CDP_REPO_DIR") or DEFAULT_CDP_REPO))
    args = p.parse_args(argv)
    _setup_logging()

    if args.mode == "gapfill":
        print("ERROR: --mode gapfill needs the run checks (next build step); not available yet",
              file=sys.stderr)
        return 2
    try:
        ref = ref_roles.load(args.ref_roles or None)
    except ref_roles.RefRolesError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    try:
        roles = ref.select(args.roles) if args.mode == "role" else []
        fields = prompts.fields_for(args.mode, [f.strip() for f in args.fields.split(",")
                                                if f.strip()])
    except (ValueError, ref_roles.RefRolesError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    root = rl.default_root()
    if not root:
        print("ERROR: LOCAL_REPORTS_DIR is not set: the reports folder is the only source",
              file=sys.stderr)
        return 1
    if not args.companies.is_file():
        print(f"ERROR: no company list at {args.companies}", file=sys.stderr)
        return 1

    if args.dry_run:
        from . import ocr
        ocr.ENABLED = False     # OCR reads scans with the AI: a dry run reports them instead
    images = pay.PAGE_IMAGES if args.images is None else args.images == "on"
    req = Request(args.mode, fields, roles, args.roles if args.mode == "role" else "", images,
                  str(ref.path), load_cdp_roles(args.cdp_repo, ref))
    countries = {c.strip().upper() for c in args.countries.split(",") if c.strip()}
    only = {c.strip() for c in args.only.split(",") if c.strip()}
    companies = read_companies(args.companies, countries, only, args.limit)
    lib = rl.ReportRetriever(root)
    find_reports(companies, lib)

    found = [c for c in companies if c.report]
    print(f"{len(companies)} companies; remuneration report on disk for {len(found)}; "
          f"{sum(1 for c in companies if c.duplicate_of)} share a PDF with another")
    for c in companies:
        if c.match_type == "name-class" or (c.report and c.report["country"] != c.country):
            print(f"  check: {c.company_name} ({c.country}) -> {c.report['file_name']} "
                  f"[{c.match_type}]")
        if c.duplicate_of:
            print(f"  same PDF: {c.company_name} -> duplicate_of {c.duplicate_of}")
        if not c.report:
            print(f"  no remuneration report: {c.company_name} ({c.country})"
                  + (f", annual only: {c.annual_file}" if c.annual_file else ""))

    spec = args.roles if args.mode == "role" else (args.fields or args.mode)
    run_id = args.run_id or run_id_for(args.mode, spec)
    run_dir = RUNS_DIR / run_id
    todo = []
    for c in companies:
        done = run_dir / "companies" / f"{c.company_id}.json"
        failed = done.with_suffix(".error.json")
        if not args.dry_run and not args.force:
            if done.exists():
                continue
            if failed.exists() and not args.retry_failed:
                continue
        todo.append(c)

    meta = {"run_id": run_id, "mode": args.mode, "roles_spec": req.roles_spec,
            "roles": roles, "fields": fields, "countries": sorted(countries),
            "only": sorted(only), "companies_file": str(args.companies),
            "reports_folder": root, "model": llm.model_name(), "images": images,
            "ref_roles": str(ref.path), "ref_roles_version": ref.version,
            "cdp_roles_offered": len(req.cdp_roles or []), "git_commit": git_commit(),
            "prompt_files": {n: hashlib.sha1(llm.load_prompt(n).encode()).hexdigest()[:12]
                             for n in ("pay_base_system", "pay_fields", f"pay_mode_{args.mode}")},
            "started": dt.datetime.now().isoformat(timespec="seconds")}
    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "run.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"run {run_id}: {len(todo)} to do, {len(companies) - len(todo)} already done"
          + (" (dry run: no AI calls, nothing written)" if args.dry_run else ""))

    rows: dict[str, dict] = {}
    workers = max(1, args.workers)
    if workers == 1:
        for c in todo:
            rows[c.company_id] = _worker(c, req, run_dir, args.dry_run)
            _progress(rows[c.company_id], len(rows), len(todo))
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init,
                                 initargs=(args.dry_run,)) as pool:
            futures = [pool.submit(_worker, c, req, run_dir, args.dry_run) for c in todo]
            for f in as_completed(futures):
                row = f.result()
                rows[row["company_id"]] = row
                _progress(row, len(rows), len(todo))

    statuses: dict[str, int] = {}
    for row in rows.values():
        s = row.get("status", "").split(":")[0]
        statuses[s] = statuses.get(s, 0) + 1
    tokens = sum(int(r.get("prompt_tokens") or 0) for r in rows.values())
    print("statuses: " + ", ".join(f"{k} {v}" for k, v in sorted(statuses.items())))
    if args.dry_run:
        print(f"estimated prompt tokens: {tokens:,} for {statuses.get('dry_run', 0)} AI call(s) "
              "(output tokens not estimated)")
        return 0
    meta["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    meta["statuses"] = statuses
    (run_dir / "run.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"summary: {write_summary(run_dir, companies, rows)}")
    return 1 if statuses.get("error") else 0


def _progress(row: dict, n: int, total: int) -> None:
    extra = f" {row.get('lines', 0)} line(s)" if row.get("status") == "ok" else ""
    print(f"[{n}/{total}] {row.get('company_name')}: {row.get('status')}{extra}"
          + (f" ({row['note']})" if row.get("note") else ""), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
