"""Every company of a region's list with every field: the value found, or why not.

    python -m extractor.region_fields "<...>/Nordics_Companies_Reports_FY2025.xlsx"
        [--out output/Nordics_fields_FY2025.xlsx]

Companies come from the region's workbook (region_status.read_workbook), their values from
the newest run of each (region_status.load_runs / RunMatcher). Writes one workbook:

- **Company fields**: one row per company, one column per company-level field (41). A cell
  holds the value (money with its currency), "NOT FOUND: <failure code>", "n/a" (does not
  apply), "not collected" (the run did not ask for it), or is empty when the company has
  not been run. Green: found; red: a required field not found; orange: an optional or
  conditional field not found; grey: n/a or not collected.
- **Pay fields**: one row per company and executive role, one column per pay field (14).
- **Field summary**: per field, its requirement and how many run companies have it.
- **Legend**: the colours and failure codes.

Bucket status comes from the mirrored metadata (gcs.py), not a live listing.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

from . import failures as fl
from . import gcs
from . import region_status as rs
from .config import PROJECT_ROOT
from .fields import COMPANY_POINTS
from .pay import ROLE_POINTS

GREEN, RED, ORANGE, GREY = "C6EFCE", "FFC7CE", "FFEB9C", "E7E6E6"
MONEY_UNITS = 3            # ISO currency codes are three letters
MAX_CELL = 250


def cell_value(row: dict) -> tuple[str, str]:
    """(text, state) of one data point row; state: found, missing, na, not_collected."""
    value = (row.get("value") or "").strip()
    if value:
        unit = (row.get("unit") or "").strip()
        text = f"{value} {unit}" if unit and len(unit) == MONEY_UNITS and unit.isupper() else value
        return text[:MAX_CELL], "found"
    code = fl.classify(row)
    if code is fl.Failure.NOT_APPLICABLE:
        return "n/a", "na"
    if code is fl.Failure.NOT_COLLECTED:
        return "not collected", "not_collected"
    return f"NOT FOUND: {code.value}", "missing"


def build(workbook: Path, out: Path) -> dict:
    companies = rs.read_workbook(workbook)
    runs = rs.load_runs()
    rmatch = rs.RunMatcher(runs)
    req = rs.requirements()
    try:
        gmatch = gcs.Matcher(gcs.records())
    except OSError:
        gmatch = None

    co_rows, pay_rows = [], []
    stats = defaultdict(Counter)                    # field -> state counts (run companies)
    for c in companies:
        cid = c["id"].split("\n")[0]
        rec = gmatch(company_id=cid, name=c["name"], country=c["country_code"], lei=c["lei"])[0] \
            if gmatch else None
        run_id, how = rmatch(c)
        rows, run_file = runs[run_id] if run_id else ([], "")
        base = {"Country": c["country_code"], "Company": c["name"], "Company ID": cid or "",
                "In GCS": "yes" if rec else "no", "Run": "yes" if rows else "not run yet",
                "Run company id": run_id or "", "Run file": run_file}
        cells: dict[str, tuple[str, str]] = {}
        by_point = {r["data_point"]: r for r in rows if r.get("grain") == "company"}
        have_staff = any((by_point.get(n) or {}).get("value") for n in ("headcount", "fte"))
        for name in COMPANY_POINTS:
            if not rows:
                cells[name] = ("", "")
                continue
            r = by_point.get(name)
            text, state = cell_value(r) if r else ("not collected", "not_collected")
            if state == "missing" and name in ("headcount", "fte") and have_staff:
                text, state = "n/a (the other of headcount/fte found)", "na"
            cells[name] = (text, state)
            stats[name][state] += 1
        found = sum(1 for t, s in cells.values() if s == "found")
        miss_req = [n for n, (t, s) in cells.items() if s == "missing" and rs.is_required(req.get(n, ""))]
        miss_opt = [n for n, (t, s) in cells.items() if s == "missing" and not rs.is_required(req.get(n, ""))]
        roles = defaultdict(dict)
        for r in rows:
            if r.get("grain") == "role":
                roles[r.get("role_row") or ""][r["data_point"]] = r
        pay_missing_req = set()
        for role, points in roles.items():
            prow = {**{k: base[k] for k in ("Country", "Company", "Company ID")},
                    "Role": role or "(no role found)"}
            pcells = {}
            for name in ROLE_POINTS:
                r = points.get(name)
                text, state = cell_value(r) if r else ("", "")
                pcells[name] = (text, state)
                if state:
                    stats[name][state] += 1
                if state == "missing" and rs.is_required(req.get(name, "")):
                    pay_missing_req.add(name)
            pay_rows.append((prow, pcells))
        co_rows.append(({**base,
                         "Company fields found": found if rows else "",
                         "Required company fields not found": len(miss_req) if rows else "",
                         "Required pay fields not found (any role)": len(pay_missing_req) if rows else "",
                         "Optional / conditional company fields not found": len(miss_opt) if rows else "",
                         "Not found (required)": ", ".join(miss_req + sorted(pay_missing_req)),
                         }, cells))
    summary = []
    for name in list(COMPANY_POINTS) + list(ROLE_POINTS):
        s = stats[name]
        total = sum(s.values())
        summary.append({"Field": name, "Level": "company" if name in COMPANY_POINTS else "role (pay)",
                        "Requirement": req.get(name, "Optional"),
                        "Found": s["found"], "Not found": s["missing"], "n/a": s["na"],
                        "Not collected": s["not_collected"],
                        "Found % (of found + not found)":
                            round(100 * s["found"] / (s["found"] + s["missing"]), 1)
                            if s["found"] + s["missing"] else "",
                        "Rows": total})
    _write(out, co_rows, pay_rows, summary, req)
    run = sum(1 for b, _ in co_rows if b["Run"] == "yes")
    return {"companies": len(co_rows), "run": run, "pay_rows": len(pay_rows), "out": out,
            "summary": summary}


def _write(out: Path, co_rows, pay_rows, summary, req) -> None:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    fills = {k: PatternFill("solid", fgColor=v) for k, v in
             {"found": GREEN, "missing_req": RED, "missing_opt": ORANGE, "na": GREY,
              "not_collected": GREY}.items()}
    head_fill = PatternFill("solid", fgColor="1F3864")
    white = Font(bold=True, color="FFFFFF")
    wb = openpyxl.Workbook()

    def sheet(ws, base_rows, field_names):
        base_head = list(base_rows[0][0]) if base_rows else []
        ws.append(base_head + field_names)
        ws.append([""] * len(base_head) + [req.get(n, "Optional") for n in field_names])
        for i in range(1, len(base_head) + len(field_names) + 1):
            ws.cell(1, i).font, ws.cell(1, i).fill = white, head_fill
            ws.cell(2, i).font = Font(italic=True, color="595959")
            ws.cell(1, i).alignment = Alignment(text_rotation=0, wrap_text=True, vertical="top")
        for base, cells in base_rows:
            ws.append([base[h] for h in base_head] + [cells[n][0] for n in field_names])
            r = ws.max_row
            for j, n in enumerate(field_names, len(base_head) + 1):
                state = cells[n][1]
                if state == "missing":
                    state = "missing_req" if rs.is_required(req.get(n, "")) else "missing_opt"
                if state in fills:
                    ws.cell(r, j).fill = fills[state]
        for i, h in enumerate(base_head + field_names, 1):
            ws.column_dimensions[get_column_letter(i)].width = 16 if i > len(base_head) else \
                min(40, max(10, len(h) + 2))
        ws.freeze_panes = ws.cell(3, len(base_head) + 1).coordinate if base_head else "A3"
        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

    ws = wb.active
    ws.title = "Company fields"
    sheet(ws, co_rows, list(COMPANY_POINTS))
    ws.column_dimensions["B"].width = 34
    sheet(wb.create_sheet("Pay fields"), pay_rows, list(ROLE_POINTS))

    s = wb.create_sheet("Field summary")
    head = list(summary[0])
    s.append(head)
    for r in summary:
        s.append([r[h] for h in head])
    for i, h in enumerate(head, 1):
        s.cell(1, i).font, s.cell(1, i).fill = white, head_fill
        s.column_dimensions[get_column_letter(i)].width = max(12, len(h) + 2)
    s.freeze_panes = "B2"
    s.auto_filter.ref = s.dimensions

    lg = wb.create_sheet("Legend")
    lg.append(["Cell", "Meaning"])
    for text, key, meaning in (
            ("value", "found", "Found (money shows its currency)"),
            ("NOT FOUND: <code>", "missing_req", "A required field not found; the code says why"),
            ("NOT FOUND: <code>", "missing_opt", "An optional or conditional field not found"),
            ("n/a", "na", "Does not apply (e.g. not listed, one person, fixed pay only)"),
            ("not collected", "not_collected", "The run did not ask for it (pay-only or company-only run)"),
            ("(empty row)", None, "The company has not been run yet")):
        lg.append([text, meaning])
        if key:
            lg.cell(lg.max_row, 1).fill = fills[key]
    lg.append([])
    lg.append(["Failure code", "Meaning", "What to do"])
    for code in fl.Failure:
        if code.info.real:
            lg.append([code.value, code.info.label, code.info.action])
    for col, w in (("A", 34), ("B", 50), ("C", 80)):
        lg.column_dimensions[col].width = w
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.region_fields",
                                description="Every company of a region list with every field: value or why not")
    p.add_argument("workbook", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args(argv)
    region = args.workbook.stem.split("_")[0]
    out = args.out or PROJECT_ROOT / "output" / f"{region}_fields_FY2025.xlsx"
    try:
        res = build(args.workbook, out)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"{res['companies']} companies ({res['run']} run), {res['pay_rows']} pay rows -> {res['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
