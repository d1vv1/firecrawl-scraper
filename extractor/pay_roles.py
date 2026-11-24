"""Role-based pay from the remuneration reports already on disk: no search, no Firecrawl,
no web; the only call out is the AI.

    python -m extractor.pay_roles --mode role --roles required --countries SE,NO,DK,FI --dry-run
    python -m extractor.pay_roles --mode role --roles required --countries SE,NO,DK,FI --workers 3
    python -m extractor.pay_roles --mode field --fields base_salary,sti_paid --only <company_id>
    python -m extractor.pay_roles --mode all --countries SE --run-id <run_id>      # resume
    python -m extractor.pay_roles --mode gapfill --from-run <run_id>               # re-ask flags

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
  fact_pay_line.csv, evidence.csv, role_review.csv   see pay_roles_output.py

A gap-fill run (--mode gapfill --from-run <run_id>) takes an earlier run's results, asks the
AI again only about the cells its checks flag (a total that does not add up, a figure that
looks 1,000 times off, a quote not found in the text, an executive with no fixed pay), and
writes a new run with those cells replaced; the old value stays in the cell's "previous" and
in evidence.csv. The earlier run is not changed.
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
from . import pay_roles_output as output
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
    images: str                      # auto (pages with broken tables) | on | off
    ref_path: str
    cdp_roles: list[tuple[str, str]] | None = None
    from_run: str = ""               # gap-fill: the run whose flagged cells are asked again


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
    # the function first; the row's own label second ("Ellen Trane Nørby, formand")
    m = (ref.match(line.get("printed_title") or "", country)
         or ref.match(line.get("row_label") or "", country))
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


_ROW = re.compile(r"^\s*\|(.*)\|\s*$")
_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{3,}")
_FIGURE = re.compile(r"^[\s(−\-]*\d[\d\s.,]*\)?\s*%?$")
_FRAGMENT = re.compile(r"^[^\W\d_]{1,3}$")
_YEAR_CELL = re.compile(r"^(19|20)\d{2}(/\d{2})?$")     # "2025 | 2024" is a real header


def _cells(line: str) -> list[str] | None:
    m = _ROW.match(line)
    return [c.strip().strip("*") for c in m.group(1).split("|")] if m else None


def broken_tables(text: str) -> list[str]:
    """Signs that the PDF-to-markdown conversion damaged a table on this page: a row that is
    only the wrapped rest of a label ("|g||2024|138|"), a header row that holds figures (the
    second part of a cut table), or two tables in a row with the same columns."""
    lines = (text or "").splitlines()
    out: list[str] = []
    blocks: list[tuple[int, int]] = []          # (last line index, columns) of each table
    for i, line in enumerate(lines):
        cells = _cells(line)
        if cells is None or _SEPARATOR.match(line):
            continue
        filled = [c for c in cells if c]
        label = next((c for c in cells if c), "")
        if label and _FRAGMENT.match(label) and len(filled) < len(cells) - 1:
            out.append(f"fragment row: {line.strip()[:60]}")
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR.match(nxt) and filled:
            # whole years are a normal header; split ones ("20 | 25", "202 | 5") are not
            figures = sum(1 for c in filled if _FIGURE.match(c) and not _YEAR_CELL.match(c))
            if figures >= max(2, len(filled) // 2):
                out.append(f"figures in a header row: {line.strip()[:60]}")
            if blocks and i - blocks[-1][0] <= 3 and blocks[-1][1] == len(cells):
                out.append(f"table cut in two before: {line.strip()[:60]}")
        if blocks and blocks[-1][0] == i - 1:
            blocks[-1] = (i, blocks[-1][1])
        else:
            blocks.append((i, len(cells)))
    return out


def image_pages(mode: str, chunks, origin) -> list[int]:
    """The PDF pages to attach as images: none (off), the pay-table pages (on), or the
    pay-table pages whose tables the conversion damaged (auto). Images were not better on
    clean tables in earlier tests (pay.py), so auto keeps them for the broken ones."""
    if mode == "off" or not origin.pdf or not Path(origin.pdf).exists():
        return []
    texts = origin.page_text()
    pages = pay.table_pages(chunks, texts)
    return pages if mode == "on" else [p for p in pages if broken_tables(texts.get(p, ""))]


def build_request(c: Company, req: Request, ref: ref_roles.RefRoles,
                  gaps: list[prompts.Gap] | None = None):
    """(origin, chunks, system prompt, user message, page numbers shown, request key)."""
    from .datapoints import _pay_chunks

    origin, _ = read_origin(c.report)
    chunks = _pay_chunks(origin, pay.PAY_WORDS)
    fields = prompts.fields_for(req.mode, req.fields, gaps)
    system = prompts.system_prompt(req.mode, fields)
    user = prompts.user_message(req.mode, company=c.company_name, source=c.report["file_name"],
                                what="the company's remuneration report", chunks=chunks,
                                ref=ref, country=c.country, selected=req.roles or None,
                                cdp_roles=req.cdp_roles, gaps=gaps)
    shown = image_pages(req.images, chunks, origin)
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

    answer, tokens, cached = ask(key, system, user, origin, shown,
                                 prompts.answer_schema(req.mode,
                                                       prompts.fields_for(req.mode, req.fields)))
    texts = {ch.id: ch.text for ch in chunks}
    cdp_ids = {i for i, _ in req.cdp_roles or []}
    fy = answer.get("fiscal_year")
    lines = []
    for line in answer.get("lines", []):
        lines.append({"pay_line_id": pay_line_id(c.company_id, fy, line),
                      "mapping": map_role(ref, line, c.country, cdp_ids), "line": line,
                      "quote_check": quote_checks(line, texts)})
    count = {s: sum(1 for x in lines if x["mapping"]["mapping_source"] == s)
             for s in ("auto", "suggestion", "unmapped")}
    cells = sum(1 for x in lines for f in FIELDS if isinstance(x["line"].get(f), dict)
                and x["line"][f].get("value") is not None)
    detail = {"run_mode": req.mode, "fields": prompts.fields_for(req.mode, req.fields),
              "roles": req.roles, "model": llm.model_name(), "request_key": key,
              "ref_roles_version": ref.version, "image_pages": shown,
              "report": c.report, "annual_file": c.annual_file,
              "chunk_pages": {str(ch.id): ch.pages for ch in chunks}, "lines": lines}
    return finish("ok" if lines else "no_lines", "" if lines else "the AI found no pay line",
                  fiscal_year=fy or "", period_end=answer.get("period_end") or "",
                  lines=len(lines), mapped_auto=count["auto"],
                  mapped_suggestion=count["suggestion"], unmapped=count["unmapped"],
                  cells=cells, prompt_tokens=tokens.prompt,
                  completion_tokens=tokens.completion, cached=cached, _detail=detail)


def ask(key: str, system: str, user: str, origin, shown: list[int], schema) -> tuple:
    """The AI's answer to one request, from the cache when it was asked before.
    Returns (answer dict, _Tokens, cached)."""
    cache = CACHE_DIR / f"payroles_{key}.json"
    tokens = _Tokens()
    if cache.exists():
        saved = json.loads(cache.read_text(encoding="utf-8"))
        tokens.prompt = saved.get("prompt_tokens", 0)
        tokens.completion = saved.get("completion_tokens", 0)
        return saved["answer"], tokens, True
    images = pay.page_images(Path(origin.pdf), shown) if shown else None
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
    return answer, tokens, False


def quote_checks(line: dict, texts: dict[int, str]) -> dict[str, str]:
    """For each filled cell (and the line itself): how well its quote matches the text it was
    read from (pay_roles_output.quote_grade: exact, close or missing)."""
    out = {}
    for name in ["line", *FIELDS]:
        cell = line if name == "line" else line.get(name)
        if isinstance(cell, dict) and (name == "line" or cell.get("value") is not None):
            grade = output.quote_grade(cell.get("quote"), None if name == "line"
                                       else cell.get("printed"), cell.get("chunk_id"), texts)
            if grade is not None:
                out[name] = grade
    return out


def recheck(run_dir: Path) -> dict[str, int]:
    """Grade every quote of an existing run again from the cached report text, and rewrite
    the run's files. No AI call: for a run made before a change to the checks."""
    from .datapoints import _pay_chunks

    done = 0
    for path in sorted((run_dir / "companies").glob("*.json")):
        if path.name.endswith(".error.json"):
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("status") != "ok" or not doc.get("report"):
            continue
        origin, _ = read_origin(doc["report"])
        texts = {ch.id: ch.text for ch in _pay_chunks(origin, pay.PAY_WORDS)}
        for item in doc.get("lines", []):
            item["quote_check"] = quote_checks(item["line"], texts)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        done += 1
    files = output.export(run_dir)
    return {"companies": done, **files}


# --- gap-fill --------------------------------------------------------------------------------

def gaps_of(doc: dict) -> list[prompts.Gap]:
    """The cells of one company's result that the checks want asked again. A total that does
    not add up asks again for the total and each part the line has."""
    pages = doc.get("chunk_pages", {})
    lines = {x["pay_line_id"]: x["line"] for x in doc.get("lines", [])}
    out, seen = [], set()
    for f in output.check_company(doc):
        if not f.gap or f.pay_line_id not in lines:
            continue
        line = lines[f.pay_line_id]
        fields = [f.field]
        if f.kind == "total_mismatch":
            fields += [p for p in output.TOTAL_PARTS if output.filled(line.get(p))]
        for name in fields:
            if (f.pay_line_id, name) in seen:
                continue
            seen.add((f.pay_line_id, name))
            cell = line.get(name) if isinstance(line.get(name), dict) else {}
            chunk = cell.get("chunk_id") if cell.get("chunk_id") is not None else line.get("chunk_id")
            page = (pages.get(str(chunk)) or [None])[0]
            out.append(prompts.Gap(f.pay_line_id, line.get("printed_title", ""), name, page,
                                   f"{f.kind}: {f.detail}"))
    return out


def merge_gaps(doc: dict, answer: dict, gaps: list[prompts.Gap], texts: dict[int, str]) -> int:
    """Put a gap-fill answer into a copy of the earlier result. A cell found again replaces
    the old one, which is kept under "previous"; a cell not found keeps its old value with
    the reason. Returns the number of cells changed."""
    asked = {(g.line_ref, g.field): g for g in gaps}
    items = {x["pay_line_id"]: x for x in doc.get("lines", [])}
    changed = 0
    for cell in answer.get("cells", []):
        key = (cell.get("line_ref"), cell.get("field"))
        if key not in asked or key[0] not in items or key[1] not in FIELDS:
            continue
        item = items[key[0]]
        old = item["line"].get(key[1]) or {}
        if not cell.get("found"):
            if isinstance(old, dict) and old:
                old["gapfill_note"] = f"rechecked, not found: {cell.get('not_found_reason') or '-'}"
            continue
        keys = FIELDS[key[1]].cell.model_fields
        new = {k: cell.get(k) for k in keys}
        new["previous"] = {k: old.get(k) for k in keys} if old else None
        new["gapfill_note"] = f"rechecked: {asked[key].reason}"
        item["line"][key[1]] = new
        item.setdefault("quote_check", {}).pop(key[1], None)
        grade = output.quote_grade(new.get("quote"), new.get("printed"), new.get("chunk_id"), texts)
        if grade is not None:
            item["quote_check"][key[1]] = grade
        changed += 1
    return changed


def run_gapfill(doc: dict, req: Request, run_dir: Path, dry_run: bool = False) -> dict:
    """One company of a gap-fill run: its earlier result, with the flagged cells asked again
    (or copied as it is when nothing is flagged)."""
    started = time.monotonic()
    cid = doc["company_id"]
    gaps = gaps_of(doc) if doc.get("status") == "ok" else []
    row = {k: doc.get(k, "") for k in ("company_id", "company_name", "country", "also_listed_as",
                                       "match_type", "source_file", "format", "fiscal_year",
                                       "period_end", "lines", "mapped_auto",
                                       "mapped_suggestion", "unmapped", "cells")}
    if gaps and not dry_run:
        ref = ref_roles.load(req.ref_path)
        c = Company(cid, doc["company_name"], doc.get("country", ""), "", report=doc["report"])
        origin, chunks, system, user, shown, key = build_request(c, req, ref, gaps)
        answer, tokens, cached = ask(key, system, user, origin, shown,
                                     prompts.answer_schema("gapfill", []))
        doc = json.loads(json.dumps(doc))       # a copy: the earlier run stays as it was
        changed = merge_gaps(doc, answer, gaps, {ch.id: ch.text for ch in chunks})
        doc["gapfill"] = {"of_run": req.from_run, "asked": len(gaps), "changed": changed,
                          "request_key": key}
        row.update(status="ok", note=f"{len(gaps)} cell(s) asked again, {changed} changed",
                   prompt_tokens=tokens.prompt, completion_tokens=tokens.completion,
                   cached=cached)
    elif gaps:
        row.update(status="dry_run", note=f"{len(gaps)} cell(s) to ask again")
    else:
        row.update(status=doc.get("status", ""), note="nothing to ask again: copied")
    row["seconds"] = round(time.monotonic() - started, 1)
    if not dry_run:
        out = run_dir / "companies" / f"{cid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({**doc, **{k: v for k, v in row.items()
                                             if k in ("note", "seconds", "prompt_tokens",
                                                      "completion_tokens", "cached")}},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
    return row


def _gap_worker(doc: dict, req: Request, run_dir: Path, dry_run: bool) -> dict:
    try:
        return run_gapfill(doc, req, run_dir, dry_run)
    except Exception as e:  # noqa: BLE001
        log.exception("%s failed", doc.get("company_id"))
        return {"company_id": doc.get("company_id"), "company_name": doc.get("company_name"),
                "country": doc.get("country"), "status": "error", "note": repr(e)[:300]}


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
    p.add_argument("--mode", choices=["field", "role", "all", "gapfill"])
    p.add_argument("--recheck", default="", metavar="RUN_ID",
                   help="grade the quotes of an existing run again and rewrite its files (no AI)")
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
    p.add_argument("--images", choices=["auto", "on", "off"], default="auto",
                   help="attach pay-table page images: auto (only pages whose tables the PDF "
                        "conversion damaged; default), on (all pay-table pages) or off")
    p.add_argument("--ref-roles", default=os.getenv("REF_ROLES_XLSX") or "",
                   help="the role workbook (default: REF_ROLES_XLSX or ../../Reports/ref_roles.xlsx)")
    p.add_argument("--cdp-repo", type=Path,
                   default=Path(os.getenv("CDP_REPO_DIR") or DEFAULT_CDP_REPO))
    p.add_argument("--from-run", default="",
                   help="mode gapfill: the run whose flagged cells are asked again")
    args = p.parse_args(argv)
    _setup_logging()

    if args.recheck:
        run_dir = RUNS_DIR / args.recheck
        if not (run_dir / "companies").is_dir():
            print(f"ERROR: no run at {run_dir}", file=sys.stderr)
            return 1
        f = recheck(run_dir)
        print(f"rechecked {f['companies']} companies of {args.recheck}: {f['lines']} line(s), "
              f"{f['cells']} cell(s), {f['review']} review row(s), {f['gaps']} to ask again")
        return 0
    if not args.mode:
        p.error("--mode is required (or --recheck RUN_ID)")
    gapfill = args.mode == "gapfill"
    from_dir = RUNS_DIR / args.from_run if args.from_run else None
    if gapfill and not (from_dir and (from_dir / "companies").is_dir()):
        print(f"ERROR: --mode gapfill needs --from-run <run_id> of a run in {RUNS_DIR}",
              file=sys.stderr)
        return 1
    try:
        ref = ref_roles.load(args.ref_roles or None)
    except ref_roles.RefRolesError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    try:
        roles = ref.select(args.roles) if args.mode == "role" else []
        fields = [] if gapfill else prompts.fields_for(
            args.mode, [f.strip() for f in args.fields.split(",") if f.strip()])
    except (ValueError, ref_roles.RefRolesError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    root = rl.default_root()
    if not root:
        print("ERROR: LOCAL_REPORTS_DIR is not set: the reports folder is the only source",
              file=sys.stderr)
        return 1
    if not gapfill and not args.companies.is_file():
        print(f"ERROR: no company list at {args.companies}", file=sys.stderr)
        return 1

    if args.dry_run:
        from . import ocr
        ocr.ENABLED = False     # OCR reads scans with the AI: a dry run reports them instead
    images = args.images
    req = Request(args.mode, fields, roles, args.roles if args.mode == "role" else "", images,
                  str(ref.path), None if gapfill else load_cdp_roles(args.cdp_repo, ref),
                  args.from_run)
    countries = {c.strip().upper() for c in args.countries.split(",") if c.strip()}
    only = {c.strip() for c in args.only.split(",") if c.strip()}
    if gapfill:
        docs = [d for d in output.load_companies(from_dir)
                if (not countries or d.get("country") in countries)
                and (not only or d.get("company_id") in only)]
        docs = docs[:args.limit] if args.limit else docs
        return _run(args, req, ref, root, countries, only, docs,
                    [Company(d["company_id"], d.get("company_name", ""), d.get("country", ""), "")
                     for d in docs])
    companies = read_companies(args.companies, countries, only, args.limit)
    lib = rl.ReportRetriever(root)
    find_reports(companies, lib)
    return _run(args, req, ref, root, countries, only, companies, companies)


def _run(args, req: Request, ref: ref_roles.RefRoles, root: str, countries: set[str],
         only: set[str], items: list, companies: list[Company]) -> int:
    """Run `items` (companies, or a gap-fill's earlier results) and write the run's files."""
    gapfill, roles, fields, images = req.mode == "gapfill", req.roles, req.fields, req.images
    found = [c for c in companies if c.report]
    if gapfill:
        print(f"gap-fill of run {req.from_run}: {len(items)} companies")
    else:
        print(f"{len(companies)} companies; remuneration report on disk for {len(found)}; "
              f"{sum(1 for c in companies if c.duplicate_of)} share a PDF with another")
    for c in ([] if gapfill else companies):
        if c.match_type == "name-class" or (c.report and c.report["country"] != c.country):
            print(f"  check: {c.company_name} ({c.country}) -> {c.report['file_name']} "
                  f"[{c.match_type}]")
        if c.duplicate_of:
            print(f"  same PDF: {c.company_name} -> duplicate_of {c.duplicate_of}")
        if not c.report:
            print(f"  no remuneration report: {c.company_name} ({c.country})"
                  + (f", annual only: {c.annual_file}" if c.annual_file else ""))

    spec = (args.from_run if gapfill else
            args.roles if args.mode == "role" else (args.fields or args.mode))
    run_id = args.run_id or run_id_for(args.mode, spec)
    run_dir = RUNS_DIR / run_id
    todo = []
    for item, c in zip(items, companies):
        done = run_dir / "companies" / f"{c.company_id}.json"
        failed = done.with_suffix(".error.json")
        if not args.dry_run and not args.force:
            if done.exists():
                continue
            if failed.exists() and not args.retry_failed:
                continue
        todo.append(item)

    meta = {"run_id": run_id, "mode": args.mode, "from_run": req.from_run,
            "roles_spec": req.roles_spec, "roles": roles, "fields": fields,
            "countries": sorted(countries),
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
    work = _gap_worker if gapfill else _worker
    if workers == 1:
        for item in todo:
            row = work(item, req, run_dir, args.dry_run)
            rows[row["company_id"]] = row
            _progress(row, len(rows), len(todo))
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init,
                                 initargs=(args.dry_run,)) as pool:
            futures = [pool.submit(work, item, req, run_dir, args.dry_run) for item in todo]
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
        if not gapfill:
            print(f"estimated prompt tokens: {tokens:,} for {statuses.get('dry_run', 0)} AI "
                  "call(s) (output tokens not estimated)")
        return 0
    meta["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    meta["statuses"] = statuses
    meta["files"] = output.export(run_dir)
    (run_dir / "run.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"summary: {write_summary(run_dir, companies, rows)}")
    f = meta["files"]
    print(f"fact_pay_line.csv: {f['lines']} line(s); evidence.csv: {f['cells']} cell(s); "
          f"role_review.csv: {f['review']} row(s), {f['gaps']} to ask again "
          f"(--mode gapfill --from-run {run_dir.name})")
    return 1 if statuses.get("error") else 0


def _progress(row: dict, n: int, total: int) -> None:
    extra = f" {row.get('lines', 0)} line(s)" if row.get("status") == "ok" else ""
    print(f"[{n}/{total}] {row.get('company_name')}: {row.get('status')}{extra}"
          + (f" ({row['note']})" if row.get("note") else ""), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
