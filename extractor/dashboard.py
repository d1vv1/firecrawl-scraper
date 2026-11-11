"""The accuracy dashboard's data, from our output checks (python -m extractor.dashboard).

The dashboard (Dashboard/, by Rahul: an Angular app and a single-file HTML report) shows
one file, report.json (Dashboard/SPEC.md section 5). This writes it from a run's
data-point CSV scored by extractor.output_checks, so the dashboard and the checks
report can never disagree: there is one set of check rules, in output_checks.py.

    python -m extractor.dashboard output/nordic_uk_10_datapoints.csv

A batch run calls build() at its end, so the dashboard always shows the last run. The
run before it becomes the baseline the dashboard compares with ("vs previous run").

Writes:
  Dashboard/report.json, Dashboard/app/public/report.json  the data
  Dashboard/allshares_report.html                          single file: open or email it
  the import schema (.json, .js) and the results template CSV next to them
"""

import argparse
import csv
import datetime as dt
import json
import logging
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from . import delivery
from . import output_checks as oc
from .config import CACHE_DIR, OUTPUT_DIR, PROJECT_ROOT

log = logging.getLogger(__name__)

DASHBOARD = PROJECT_ROOT / "Dashboard"
ACCURACY = PROJECT_ROOT / "accuracy"
REGISTER = ACCURACY / "inputs" / "field_register.json"
FIELDS_LIST = ACCURACY / "inputs" / "fields_list.json"   # from allshares_fields_list.xlsx (Company / Pay Data)
FIELD_REQUIREMENTS = ACCURACY / "inputs" / "field_requirements.json"   # requirement, severity, why per field
BENCHMARK_RANK = ACCURACY / "inputs" / "benchmark_rank.json"   # rank per field, from the benchmarking severity Excel
SCHEMA = ACCURACY / "schema" / "allshares_import_schema.json"
TEMPLATE = ACCURACY / "report" / "template.html"
CORE = DASHBOARD / "core"
APP_PUBLIC = DASHBOARD / "app" / "public"

STATUS_CODE = {"Pass": "P", "Review": "R", "Fail": "F", "Fail (hard)": "H"}
OUTCOME_CODE = {"pass": "P", "fail": "F"}       # n/a is left out (SPEC 3.1: not listed)
# SPEC 3.3: a period is needed except for these; a unit for numeric protocol fields
STATIC_CATEGORIES = {"Identity", "Listing and market", "Sector", "Reporting basis"}
NUMERIC_FIELD_IDS = {"C12", "C13", "C14", "C16", "C17", "C18", "R02", "R04", "R05", "R06", "R07",
                     "R08", "R09", "R10", "R11"}
TARGET = 95


def register() -> dict[str, dict]:
    return {r["data_point"]: r for r in json.loads(REGISTER.read_text(encoding="utf-8"))}


def field_meta(dp: str, grain: str, reg: dict) -> dict:
    """Protocol field ID, category and module; a field the register lacks gets ours."""
    if dp in reg:
        return reg[dp]
    return {"field_id": "", "category": oc.CATEGORY.get(dp, "Other"), "module": "Other",
            "pay": grain == "role"}


def value_status(r: oc.Row, f: dict) -> str:
    if not r.value:
        # "not applicable: one person" (a group headcount on an individual's row), no SEC filing
        return "not_applicable" if r.note.startswith("not applicable") else "not_found"
    if (f["field_id"] in NUMERIC_FIELD_IDS and r.number is not None and not r.unit) or \
            (f["category"] not in STATIC_CATEGORIES and not r.period_end):
        return "partial"
    return "found"


def company_keys(rows: list[oc.Row]) -> tuple[dict[str, str], list[dict]]:
    """Company ID -> key (its LEI, else the ID), and IDs that share one LEI."""
    lei = {}
    for r in rows:
        if r.data_point == "lei" and r.value:
            lei.setdefault(r.company_id, r.value)
        elif r.lei:
            lei.setdefault(r.company_id, r.lei)
    ids = sorted({r.company_id for r in rows})
    groups = defaultdict(list)
    for i in ids:
        groups[lei.get(i, i)].append(i)
    return ({i: lei.get(i, i) for i in ids},
            [{"lei": k, "ids": v} for k, v in groups.items() if len(v) > 1])


def report_data(scored: list[oc.Scored], rows: list[oc.Row], name: str,
                baseline: dict | None = None) -> dict:
    """report.json (SPEC section 5) for the scored run."""
    reg = register()
    gate_ids = [oc.CHECK_ID[fn] for fn, _, _ in oc.CHECKS]
    gi = {g: i for i, g in enumerate(gate_ids)}
    by_row = {id(s.row): s for s in scored}
    key_by_id, dupes = company_keys(rows)
    reasons, ri = [], {}
    values = []
    for r in rows:
        f = field_meta(r.data_point, r.grain, reg)
        rec = {"s": "T", "c": r.country, "o": r.company_name, "g": r.grain, "p": 1 if f["pay"] else 0,
               "k": f["category"], "m": f["module"], "f": f["field_id"], "d": r.data_point,
               "st": value_status(r, f), "ck": key_by_id[r.company_id], "id": r.company_id,
               "r": r.role_row, "v": r.value, "u": r.unit}
        s = by_row.get(id(r))
        if s:
            rec.update({"pe": r.period_end, "me": r.method, "so": r.source, "ep": r.endpoint,
                        "nt": r.note[:300], "sc": STATUS_CODE[s.status],
                        "sp": None if s.score is None else round(s.score)})
            gr = []
            for x in s.results:
                if x.outcome not in OUTCOME_CODE:
                    continue
                if x.reason and x.reason not in ri:
                    ri[x.reason] = len(reasons)
                    reasons.append(x.reason)
                gr.append([gi[x.check], OUTCOME_CODE[x.outcome], ri[x.reason] if x.reason else -1])
            rec["gr"] = gr
        else:
            rec["nt"] = r.note[:160]
        values.append(rec)
    outcomes = Counter(x.outcome for s in scored for x in s.results)
    run = outcomes["pass"] + outcomes["fail"]
    checks_pct = round(100 * outcomes["pass"] / run, 1) if run else 0
    applicable = [v for v in values if v["st"] != "not_applicable"]
    found_pct = round(100 * sum(v["st"] == "found" for v in applicable) / len(applicable), 1) if applicable else 0
    today = dt.date.today()
    return {
        "meta": {"tracker": name, "asOf": f"{today.day} {today:%b %Y}", "built": today.isoformat(),
                 "rows": len(rows), "filled": len(scored), "dataPoints": len({r.data_point for r in rows}),
                 "companyIds": len(key_by_id), "companies": len(set(key_by_id.values())),
                 "countries": sorted({r.country for r in rows if r.country}),
                 "duplicates": dupes, "thresholds": {"pass": oc.PASS, "review": oc.REVIEW},
                 "target": TARGET, "checksPct": checks_pct, "foundPct": found_pct},
        "gates": {oc.CHECK_ID[fn]: [title, "Hard" if hard else "Soft"] for fn, hard, title in oc.CHECKS},
        "gateIds": gate_ids,
        "reasons": reasons,
        "values": values,
        # the dashboard's "vs ..." comparisons: the previous run, or this one on the first build
        "baseline": baseline or {"checksPct": checks_pct, "foundPct": found_pct, "label": "This run"},
        "fieldList": fields_list(),
    }


def fields_list() -> list[dict]:
    """The protocol field list (Company Data and Pay Data sheets), for the Field coverage, Company Data
    and Pay Data pages, with each field's requirement, severity, review fill and reason merged in."""
    try:
        fields = json.loads(FIELDS_LIST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    try:
        reqs = {r["d"]: r for r in json.loads(FIELD_REQUIREMENTS.read_text(encoding="utf-8"))["fields"]}
    except (OSError, ValueError, KeyError):
        reqs = {}
    try:
        ranks = {r["d"]: r["rank"] for r in json.loads(BENCHMARK_RANK.read_text(encoding="utf-8"))["fields"]}
    except (OSError, ValueError, KeyError):
        ranks = {}
    for f in fields:
        r = reqs.get(f["d"], {})
        f.update({k: r[k] for k in ("req", "sev", "fill50", "milestone", "why") if k in r})
        if f["d"] in ranks:
            f["rank"] = ranks[f["d"]]
    return fields


def previous_baseline(path: Path, name: str) -> dict | None:
    """The run the dashboard showed before this build, as the baseline to compare with."""
    try:
        m = json.loads(path.read_text(encoding="utf-8"))["meta"]
        return {"checksPct": m["checksPct"], "foundPct": m["foundPct"],
                "label": f"Previous run ({m['tracker']}, {m['asOf']})"}
    except (OSError, ValueError, KeyError):
        return None


def schema_module(schema: dict) -> str:
    return ("/* Allshares import schema module. Version %s.\n"
            "   Generated by extractor/dashboard.py from accuracy/schema/allshares_import_schema.json.\n"
            "   To change the format, edit that JSON file and rebuild. */\n"
            "window.ALLSHARES_IMPORT_SCHEMA = %s;\n") % (
        schema["schema_version"], json.dumps(schema, indent=2, ensure_ascii=False))


def render_report(schema_js: str, data: dict) -> str:
    """The single-file HTML: template with the CSS, schema, core, charts and data inline."""
    t = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    parts = {"/*__CSS__*/": (CORE / "report.css").read_text(encoding="utf-8"),
             "/*__SCHEMA__*/": schema_js,
             "/*__CORE__*/": (CORE / "report-core.js").read_text(encoding="utf-8"),
             "/*__CHARTS__*/": (CORE / "report-charts.js").read_text(encoding="utf-8"),
             "/*__UI__*/": (CORE / "report-ui.js").read_text(encoding="utf-8")}
    for k, v in parts.items():
        assert t.count(k) == 1, k
        t = t.replace(k, v)
    return t.replace("/*__DATA__*/", "var DATA = " + payload + ";")   # last: never scanned


def build(csv_path: Path | list[Path], cache: Path = CACHE_DIR, results: Path = OUTPUT_DIR,
          ranges: dict | None = None, out: Path = DASHBOARD, saved_checks: bool = False) -> Path:
    """Score the run's CSV and refresh the dashboard's files and the checks report next to
    the CSV (<name>_checks.md and .csv). Returns the HTML report.

    Several CSVs (the halves of one wave) show as one run. saved_checks: take each CSV's
    <name>_checks.csv as it is instead of scoring again (a run cached on another machine)."""
    paths = [csv_path] if isinstance(csv_path, Path) else list(csv_path)
    scored, rows = [], []
    for p in paths:
        checks = p.with_name(p.stem + "_checks")
        if saved_checks:
            s, r = oc.saved(p, checks.with_suffix(".csv"))
        else:
            s, r = oc.run(p, oc.Sources(cache, results), ranges or dict(oc.DEFAULT_RANGES))
            checks.with_suffix(".md").write_text(oc.report(s, r, p.name), encoding="utf-8")
            oc.write_csv(s, checks.with_suffix(".csv"))
        scored += s
        rows += r
    name = " + ".join(p.name for p in paths)
    data = report_data(scored, rows, name, previous_baseline(out / "report.json", name))
    data["delivery"] = delivery.build()   # SPEC 6.4: tracker, all runs and run outputs, not just this run
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    js = schema_module(schema)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    (out / "allshares_import_schema.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False),
                                                     encoding="utf-8")
    (out / "allshares_import_schema.js").write_text(js, encoding="utf-8")
    html = out / "allshares_report.html"
    html.write_text(render_report(js, data), encoding="utf-8")
    app_public = out / "app" / "public"
    if app_public.parent.is_dir():
        app_public.mkdir(exist_ok=True)
        shutil.copyfile(out / "report.json", app_public / "report.json")
        shutil.copyfile(out / "allshares_import_schema.json", app_public / "allshares_import_schema.json")
        (app_public / "allshares_results_template.csv").write_text(
            ",".join(c["name"] for c in schema["columns"]) + "\n", encoding="utf-8")
    st = Counter(s.status for s in scored)
    log.info("Dashboard: %d values (%s), checks passing %s%%: %s", len(scored),
             ", ".join(f"{k} {st[k]}" for k in oc.STATUSES), data["meta"]["checksPct"], html)
    return html


def rerender(out: Path = DASHBOARD) -> Path:
    """Rewrite the single-file HTML (and refresh the field list and the Delivery data) from the
    report.json already built, without scoring again: for changes to the dashboard's code, the field
    list, the tracker or the delivery inputs."""
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    data["fieldList"] = fields_list()
    data["delivery"] = delivery.build()   # SPEC 6.4: refreshed from the tracker and run outputs
    (out / "report.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    js = schema_module(json.loads(SCHEMA.read_text(encoding="utf-8")))
    html = out / "allshares_report.html"
    html.write_text(render_report(js, data), encoding="utf-8")
    if (out / "app" / "public").is_dir():
        shutil.copyfile(out / "report.json", out / "app" / "public" / "report.json")
    return html


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", type=Path, nargs="*",
                   help="data-point CSVs from python -m extractor.datapoints; several show as one run")
    p.add_argument("--saved-checks", action="store_true",
                   help="use each CSV's saved <name>_checks.csv instead of scoring again "
                        "(for a run whose cache is on another machine)")
    p.add_argument("--rerender", action="store_true",
                   help="rebuild the HTML from the existing report.json and refresh the Delivery data (no rescoring)")
    p.add_argument("--ranges", type=Path, help="JSON {field: [min, max]} replacing the default ranges")
    p.add_argument("--cache", type=Path, default=CACHE_DIR, help="where the run cached its documents")
    p.add_argument("--results", type=Path, default=OUTPUT_DIR, help="the run's per-company result JSON")
    a = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if a.rerender:
        print(f"Dashboard re-rendered: {rerender()}")
        return
    if not a.csv:
        p.error("give one or more data-point CSVs, or --rerender")
    ranges = dict(oc.DEFAULT_RANGES)
    if a.ranges:
        ranges.update({k: tuple(v) for k, v in json.loads(a.ranges.read_text(encoding="utf-8")).items()})
    html = build(a.csv, a.cache, a.results, ranges, saved_checks=a.saved_checks)
    print(f"Dashboard updated: {html}\nApp: npm --prefix Dashboard/app start, then http://localhost:4200")


if __name__ == "__main__":
    main()
