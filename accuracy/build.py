"""One-command build: tracker -> scored values -> report data, schema module, report HTML, Excel.

    python accuracy/build.py            (writes accuracy/out/ and refreshes ../Dashboard/allshares_report.html)
    python accuracy/build.py --no-copy  (out/ only)

Inputs (read-only): inputs/tracker_first50.csv, inputs/field_register.json,
schema/allshares_import_schema.json, config.json (optional overrides of engine defaults).
Scoring rules live only in engine/scoring.py.
"""
import csv
import datetime
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from engine import scoring as E  # noqa: E402
from engine import excel  # noqa: E402

IN = os.path.join(ROOT, "inputs")
OUT = os.path.join(ROOT, "out")
DASHBOARD = os.path.join(os.path.dirname(ROOT), "Dashboard")
CORE = os.path.join(DASHBOARD, "core")
APP_PUBLIC = os.path.join(DASHBOARD, "app", "public")
TRACKER = os.path.join(IN, "tracker_first50.csv")
DATA_AS_OF = "3 Nov 2026"
RESULT_CODE = {E.PASS: "P", E.FAIL: "F", E.NOT_RUN: "N"}
STATUS_CODE = {"Pass": "P", "Review": "R", "Fail": "F", "Fail (hard)": "H", "Incomplete": "I"}


def load_config():
    p = os.path.join(ROOT, "config.json")
    over = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    over.pop("_comment", None)
    return E.merge_config(over)


def company_facts(rows):
    """Distinct companies by LEI (falling back to company_id), and duplicate IDs."""
    lei_by_id = {}
    for r in rows:
        if r["lei"]:
            lei_by_id.setdefault(r["company_id"], r["lei"])
    ids = sorted({r["company_id"] for r in rows})
    groups = defaultdict(list)
    for i in ids:
        groups[lei_by_id.get(i, i)].append(i)
    dupes = [{"lei": k, "ids": v} for k, v in groups.items() if len(v) > 1]
    return {"company_ids": len(ids), "companies": len(groups), "duplicates": dupes,
            "key_by_id": {i: lei_by_id.get(i, i) for i in ids}}


def build_data(rows, reg, scored, cfg, facts):
    gate_ids = list(E.GATES)
    gi = {g: i for i, g in enumerate(gate_ids)}
    reasons, ri = [], {}
    values = []
    for x in scored:
        r = x["row"]
        f = reg[r["data_point"]]
        rec = {"s": "T", "c": r["country"], "o": r["company_name"], "g": r["grain"], "p": 1 if f["pay"] else 0,
               "k": f["category"], "m": f["module"], "f": f["field_id"], "d": r["data_point"],
               "st": x["value_status"], "ck": facts["key_by_id"][r["company_id"]], "id": r["company_id"],
               "r": r["role_row"], "v": r["value"], "u": r["unit"]}
        if r["value"]:
            rec.update({"pe": r["period_end"], "me": r["method"], "so": r["source"], "ep": r["endpoint"],
                        "nt": (r["note"] or "")[:300]})
            res = x["result"]
            rec["sc"] = STATUS_CODE[res["status"]]
            rec["sp"] = res["score"]
            gr = []
            for g in x["gates"]:
                k = g["reason"]
                if k and k not in ri:
                    ri[k] = len(reasons)
                    reasons.append(k)
                gr.append([gi[g["gate"]], RESULT_CODE[g["result"]], ri[k] if k else -1])
            rec["gr"] = gr
        else:
            rec["nt"] = (r["note"] or "")[:160]
        values.append(rec)
    s = E.summarise(scored)
    run = s["gates"].get(E.PASS, 0) + s["gates"].get(E.FAIL, 0)
    found = sum(1 for v in values if v["st"] == "found")
    return {
        "meta": {"tracker": os.path.basename(TRACKER), "asOf": DATA_AS_OF,
                 "built": datetime.date.today().isoformat(),
                 "rows": len(rows), "filled": s["values"], "dataPoints": len(reg),
                 "companyIds": facts["company_ids"], "companies": facts["companies"],
                 "duplicates": facts["duplicates"], "thresholds": cfg["thresholds"], "target": 95},
        "gates": {g: [E.GATES[g][0], E.GATES[g][1]] for g in gate_ids},
        "gateIds": gate_ids,
        "reasons": reasons,
        "values": values,
        "baseline": {"checksPct": round(s["gates"][E.PASS] / run * 100, 1),
                     "foundPct": round(found / len(values) * 100, 1), "label": "Tracker"},
    }


def write_scored_csv(path, scored, reg, facts):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_id", "company_key", "company_name", "country", "grain", "role_row", "data_point",
                    "field_id", "category", "module", "value", "unit", "period_end", "method", "value_status",
                    "score_status", "score", "passed", "applicable", "not_run", "hard_fails", "reasons"])
        for x in scored:
            r, res = x["row"], x["result"] or {}
            reasons = "; ".join("%s %s: %s" % (g["gate"], g["result"].lower(), g["reason"])
                                for g in x["gates"] if g["result"] != E.PASS)
            w.writerow([r["company_id"], facts["key_by_id"][r["company_id"]], r["company_name"], r["country"],
                        r["grain"], r["role_row"], r["data_point"], reg[r["data_point"]]["field_id"],
                        reg[r["data_point"]]["category"], reg[r["data_point"]]["module"], r["value"], r["unit"],
                        r["period_end"], r["method"], x["value_status"], res.get("status", ""),
                        res.get("score", ""), res.get("passed", ""), res.get("applicable", ""),
                        res.get("not_run", ""), " ".join(res.get("hard", [])), reasons])


def write_gate_csv(path, scored):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_id", "data_point", "role_row", "gate", "severity", "result", "reason"])
        for x in scored:
            r = x["row"]
            for g in x["gates"]:
                w.writerow([r["company_id"], r["data_point"], r["role_row"], g["gate"], E.GATES[g["gate"]][1],
                            g["result"], g["reason"]])


def schema_module(schema):
    return ("/* Allshares import schema module. Version %s.\n"
            "   Generated by accuracy/build.py from accuracy/schema/allshares_import_schema.json.\n"
            "   To change the format, edit that JSON file and rebuild. */\n"
            "window.ALLSHARES_IMPORT_SCHEMA = %s;\n") % (schema["schema_version"], json.dumps(schema, indent=2,
                                                                                                ensure_ascii=False))


def render_report(template_path, schema_js, data):
    t = open(template_path, encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    core = open(os.path.join(CORE, "report-core.js"), encoding="utf-8").read()
    charts = open(os.path.join(CORE, "report-charts.js"), encoding="utf-8").read()
    css = open(os.path.join(CORE, "report.css"), encoding="utf-8").read()
    for k in ("/*__CSS__*/", "/*__SCHEMA__*/", "/*__CORE__*/", "/*__CHARTS__*/", "/*__DATA__*/"):
        assert t.count(k) == 1, k
    # Data goes in last so nothing inside it is scanned for placeholders.
    t = t.replace("/*__CSS__*/", css).replace("/*__SCHEMA__*/", schema_js).replace("/*__CORE__*/", core).replace("/*__CHARTS__*/", charts)
    return t.replace("/*__DATA__*/", "var DATA = " + payload + ";")


def fix_validation_html(src, dst, facts):
    """Corrected copy of the earlier validation page: 50 IDs are 49 companies."""
    if not os.path.exists(src):
        return False
    t = open(src, encoding="utf-8").read()
    d = facts["duplicates"][0] if facts["duplicates"] else None
    note = ("49 companies (50 company IDs; %s share LEI %s)" % (" and ".join(d["ids"]), d["lei"])) if d else ""
    t = t.replace("All 50 companies", "All %d companies (%d IDs)" % (facts["companies"], facts["company_ids"]))
    t = t.replace("from the first 50 tracker companies",
                  "from the first %d tracker company IDs, which are %s" % (facts["company_ids"], note))
    open(dst, "w", encoding="utf-8").write(t)
    return True


def main(copy=True):
    os.makedirs(OUT, exist_ok=True)
    cfg = load_config()
    rows = E.load_tracker(TRACKER)
    reg = E.load_register(os.path.join(IN, "field_register.json"))
    scored = E.score_tracker(rows, reg, cfg)
    facts = company_facts(rows)
    summary = E.summarise(scored)

    data = build_data(rows, reg, scored, cfg, facts)
    json.dump(data, open(os.path.join(OUT, "report.json"), "w", encoding="utf-8"), ensure_ascii=False)
    write_scored_csv(os.path.join(OUT, "scored_values.csv"), scored, reg, facts)
    write_gate_csv(os.path.join(OUT, "gate_results.csv"), scored)

    schema = json.load(open(os.path.join(ROOT, "schema", "allshares_import_schema.json"), encoding="utf-8"))
    json.dump(schema, open(os.path.join(OUT, "allshares_import_schema.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    js = schema_module(schema)
    open(os.path.join(OUT, "allshares_import_schema.js"), "w", encoding="utf-8").write(js)
    head = ",".join(c["name"] for c in schema["columns"])
    open(os.path.join(OUT, "allshares_results_template.csv"), "w", encoding="utf-8").write(head + "\n")

    html = render_report(os.path.join(ROOT, "report", "template.html"), js, data)
    open(os.path.join(OUT, "allshares_report.html"), "w", encoding="utf-8").write(html)

    excel.write_scoring_workbook(os.path.join(OUT, "allshares_first50_scoring.xlsx"), scored, reg, facts,
                                 summary, cfg)
    ranges = excel.write_ranges_workbook(os.path.join(OUT, "allshares_reference_ranges.xlsx"), rows, reg, facts)
    json.dump(ranges, open(os.path.join(OUT, "ranges_default.json"), "w", encoding="utf-8"), ensure_ascii=False)
    excel.fix_field_checks(os.path.join(IN, "allshares_field_checks.xlsx"),
                           os.path.join(OUT, "allshares_field_checks.xlsx"), facts, ranges)
    fix_validation_html(os.path.join(IN, "allshares_part1_validation.html"),
                        os.path.join(OUT, "allshares_part1_validation.html"), facts)
    if copy:
        os.makedirs(DASHBOARD, exist_ok=True)
        for name in ("allshares_report.html", "report.json", "allshares_import_schema.json", "allshares_import_schema.js"):
            shutil.copyfile(os.path.join(OUT, name), os.path.join(DASHBOARD, name))
        if os.path.isdir(os.path.dirname(APP_PUBLIC)):
            os.makedirs(APP_PUBLIC, exist_ok=True)
            for name in ("report.json", "allshares_import_schema.json", "allshares_results_template.csv"):
                shutil.copyfile(os.path.join(OUT, name), os.path.join(APP_PUBLIC, name))

    print("values %d  status %s" % (summary["values"], json.dumps(summary["status"])))
    print("gates %s  hard FAIL %d" % (json.dumps(summary["gates"]), summary["hard_fail"]))
    print("companies %d (by LEI) from %d IDs; duplicates %s" % (facts["companies"], facts["company_ids"],
                                                                facts["duplicates"]))
    print("report %d KB -> %s" % (len(html.encode("utf-8")) // 1024, os.path.join(OUT, "allshares_report.html")))


if __name__ == "__main__":
    main(copy="--no-copy" not in sys.argv)
