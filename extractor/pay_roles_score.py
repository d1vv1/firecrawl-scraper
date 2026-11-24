"""Score a role-based pay run (pay_roles.py) against a hand-made golden sample.

    python -m extractor.pay_roles_score --run <run_id> --golden ../Field_Validation/pay_roles_golden/golden.csv

The golden CSV has one row per pay line a person read from the PDF, verbatim (the template is
Field_Validation/pay_roles_golden/golden_template.csv): company_id, role_title, person_name,
role_detail, role_code, role_disclosure, period_coverage, ..., the pay columns, page, note.
Only the companies in the golden file are scored.

Each golden line is paired with one line of the run: the same person (name), else the same
role_detail, else the same role_code, else the same printed title; each run line is used once.
Then, against the agreed pass bars:
  required-role recall   golden lines of a required role the run found          100%
  role code correct      paired lines whose role_code is the golden one         >= 95%
  exact values           golden cells the run has with the same number          >= 95%
  wrong values           golden cells the run has with a different number       <= 2%
  completeness           companies with no missing required role (When rules)   all
Cells the run filled where the golden row is empty are counted as "extra" (not a bar).
score_cells.csv lists every golden cell with the run's value, page and quote, worst first.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from . import pay_roles
from . import pay_roles_output as output
from . import ref_roles

# golden column -> (run field, part): part "value" or "form" (a target's basis)
GOLDEN_FIELDS = {
    "base_salary": ("base_salary", "value"), "committee_fees": ("committee_fees", "value"),
    "meeting_fees": ("meeting_fees", "value"), "other_pay": ("other_pay", "value"),
    "benefits_value": ("benefits", "value"), "pension_contribution": ("pension", "value"),
    "pension_allowance": ("pension_allowance", "value"), "sti_paid": ("sti_paid", "value"),
    "sti_deferred": ("sti_deferred", "value"), "lti_vested": ("lti_vested", "value"),
    "lti_granted": ("lti_granted", "value"), "total_remuneration": ("total", "value"),
    "sti_target_value": ("sti_target", "value"), "sti_target_basis": ("sti_target", "form"),
    "sti_max_value": ("sti_max", "value"), "sti_max_basis": ("sti_max", "form"),
    "lti_target_value": ("lti_target", "value"), "lti_target_basis": ("lti_target", "form"),
    "lti_max_value": ("lti_max", "value"), "lti_max_basis": ("lti_max", "form"),
}
LINE_FIELDS = ["role_disclosure", "period_coverage", "aggregate_headcount", "months_in_role"]
BARS = {"required_recall": (1.0, ">="), "role_code": (0.95, ">="), "exact": (0.95, ">="),
        "wrong": (0.02, "<="), "completeness": (1.0, ">=")}
CELL_COLUMNS = ["company_id", "role_title", "person_name", "run_role_title", "field",
                "golden", "run", "result", "page", "quote", "golden_page", "note"]


def number(text) -> float | None:
    """A printed figure as a number: "12 400", "1.234,5", "(250)", "-250", "60%"."""
    if text is None:
        return None
    s = str(text).strip().replace(" ", " ").replace("−", "-")
    if not s:
        return None
    neg = s.startswith("(") and s.endswith(")") or s.startswith("-")
    s = re.sub(r"[^\d.,]", "", s)
    if not s:
        return None
    if "," in s and "." in s:                       # the last separator is the decimal one
        dec = "," if s.rfind(",") > s.rfind(".") else "."
        s = s.replace("." if dec == "," else ",", "").replace(dec, ".")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = s.replace(",", "") if len(tail) == 3 and head else s.replace(",", ".")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3
                              and len(s.split(".")[0]) <= 3 and float(s.replace(".", "")) >= 1000):
        s = s.replace(".", "")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def read_golden(path: Path) -> dict[str, list[dict]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if (r.get("company_id") or "").strip()]
    out: dict[str, list[dict]] = {}
    for r in rows:
        out.setdefault(r["company_id"].strip(), []).append(r)
    return out


def pair(golden: list[dict], run: list[dict]) -> list[tuple[dict, dict | None]]:
    """Each golden line with the run line it stands for (or None)."""
    free = list(run)
    out = []

    def take(pred):
        for item in free:
            if pred(item):
                free.remove(item)
                return item
        return None

    for g in golden:
        name = ref_roles.norm(g.get("person_name", ""))
        title = ref_roles.norm(g.get("role_title", ""))
        detail, code = g.get("role_detail", "").strip(), g.get("role_code", "").strip()
        hit = None
        if name:
            hit = take(lambda x: ref_roles.norm(x["line"].get("person_name") or "") == name)
        if not hit and detail:
            hit = take(lambda x: x["mapping"].get("role_detail") == detail)
        if not hit and code:
            hit = take(lambda x: x["mapping"].get("role_code") == code)
        if not hit and title:
            hit = take(lambda x: ref_roles.norm(x["line"].get("printed_title") or "") == title)
        out.append((g, hit))
    return out


def same(golden_text: str, run_value, part: str, cell: dict | None = None) -> bool:
    """The golden value equals the run's: as printed ("15,000" in a SEK-thousands table), or
    in full currency units ("15000000", as the old export and some checkers write it)."""
    if part == "form":
        return (golden_text or "").strip().casefold() == str(run_value or "").strip().casefold()
    g, r = number(golden_text), run_value
    if g is None or r is None:
        return False
    full = float(r) * output.scale(cell) if cell else float(r)
    return any(abs(g - v) <= 1e-6 * max(1.0, abs(g)) for v in (float(r), full))


def score(run_dir: Path, golden_path: Path, ref: ref_roles.RefRoles) -> tuple[dict, list[dict]]:
    golden = read_golden(golden_path)
    docs = {d["company_id"]: d for d in output.load_companies(run_dir)}
    required = set(ref.required())
    n = {"required": 0, "required_found": 0, "paired": 0, "role_ok": 0, "cells": 0,
         "exact": 0, "wrong": 0, "missing": 0, "extra": 0, "companies": 0,
         "complete": 0, "line_agree": 0, "line_compared": 0}
    cells: list[dict] = []
    missing_companies = []
    for cid, glines in golden.items():
        doc = docs.get(cid)
        if not doc:
            missing_companies.append(cid)
        n["companies"] += 1
        run_lines = (doc or {}).get("lines", [])
        if doc and not any(f.kind == "completeness" for f in output.check_company(doc)):
            n["complete"] += 1
        pages = (doc or {}).get("chunk_pages", {})
        for g, hit in pair(glines, run_lines):
            if g.get("role_detail", "").strip() in required:
                n["required"] += 1
                n["required_found"] += hit is not None
            line = hit["line"] if hit else {}
            if hit:
                n["paired"] += 1
                n["role_ok"] += hit["mapping"].get("role_code") == g.get("role_code", "").strip()
                for f in LINE_FIELDS:
                    if (g.get(f) or "").strip():
                        n["line_compared"] += 1
                        n["line_agree"] += same(g[f], line.get(f), "form"
                                                if f in ("role_disclosure", "period_coverage")
                                                else "value")
            for col, (field, part) in GOLDEN_FIELDS.items():
                gtext = (g.get(col) or "").strip()
                cell = line.get(field) if isinstance(line.get(field), dict) else {}
                rv = cell.get(part)
                if not gtext and rv in (None, ""):
                    continue
                if not gtext:
                    result = "extra"
                elif rv in (None, ""):
                    result = "missing"
                elif same(gtext, rv, part, cell):
                    result = "exact"
                else:
                    result = "wrong"
                if gtext:
                    n["cells"] += 1
                n[result] += 1
                chunk = cell.get("chunk_id")
                cells.append({
                    "company_id": cid, "role_title": g.get("role_title", ""),
                    "person_name": g.get("person_name", ""),
                    "run_role_title": line.get("printed_title", "") if hit else "(not found)",
                    "field": col, "golden": gtext, "run": "" if rv is None else rv,
                    "result": result,
                    "page": ",".join(map(str, pages.get(str(chunk), []))) if chunk is not None else "",
                    "quote": cell.get("quote") or "", "golden_page": g.get("page", ""),
                    "note": g.get("note", "")})

    def rate(a, b):
        return a / b if b else None

    rates = {"required_recall": rate(n["required_found"], n["required"]),
             "role_code": rate(n["role_ok"], n["paired"]),
             "exact": rate(n["exact"], n["cells"]), "wrong": rate(n["wrong"], n["cells"]),
             "completeness": rate(n["complete"], n["companies"]),
             "line_fields": rate(n["line_agree"], n["line_compared"])}
    passed = {k: (rates[k] is not None and (rates[k] >= bar if op == ">=" else rates[k] <= bar))
              for k, (bar, op) in BARS.items()}
    order = {"wrong": 0, "missing": 1, "extra": 2, "exact": 3}
    cells.sort(key=lambda c: (order[c["result"]], c["company_id"], c["role_title"], c["field"]))
    return {"counts": n, "rates": rates, "passed": passed, "all_passed": all(passed.values()),
            "companies_not_in_run": missing_companies}, cells


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.pay_roles_score",
                                description="Score a pay_roles run against a golden sample.")
    p.add_argument("--run", required=True,
                   help="the run_id (output/pay_roles/<run_id>), or the run's folder")
    p.add_argument("--golden", type=Path, required=True, help="the hand-made golden CSV")
    p.add_argument("--ref-roles", default="", help="the role workbook (default: REF_ROLES_XLSX)")
    args = p.parse_args(argv)
    run_dir = Path(args.run) if Path(args.run).is_dir() else pay_roles.RUNS_DIR / args.run
    if not (run_dir / "companies").is_dir():
        print(f"ERROR: no run at {run_dir}", file=sys.stderr)
        return 1
    if not args.golden.is_file():
        print(f"ERROR: no golden file at {args.golden}", file=sys.stderr)
        return 1
    ref = ref_roles.load(args.ref_roles or None)
    result, cells = score(run_dir, args.golden, ref)
    with (run_dir / "score_cells.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=CELL_COLUMNS)
        w.writeheader()
        w.writerows(cells)
    (run_dir / "score.json").write_text(json.dumps({"golden": str(args.golden), **result},
                                                   indent=1), encoding="utf-8")
    n, r = result["counts"], result["rates"]

    def pct(v):
        return "n/a" if v is None else f"{v:.1%}"

    print(f"golden companies: {n['companies']}"
          + (f" (not in the run: {', '.join(result['companies_not_in_run'])})"
             if result["companies_not_in_run"] else ""))
    for key, label, detail in [
            ("required_recall", "required-role recall", f"{n['required_found']}/{n['required']}"),
            ("role_code", "role code correct", f"{n['role_ok']}/{n['paired']}"),
            ("exact", "exact values", f"{n['exact']}/{n['cells']}"),
            ("wrong", "wrong values", f"{n['wrong']}/{n['cells']}"),
            ("completeness", "completeness", f"{n['complete']}/{n['companies']}")]:
        bar, op = BARS[key]
        mark = "PASS" if result["passed"][key] else "FAIL"
        print(f"  {mark}  {label:22} {pct(r[key]):>7}  ({detail}; bar {op} {bar:.0%})")
    print(f"  info  missing cells {n['missing']}, extra cells {n['extra']}, "
          f"line fields agree {pct(r['line_fields'])}")
    print(f"cells: {run_dir / 'score_cells.csv'}")
    return 0 if result["all_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
