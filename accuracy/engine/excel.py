"""Excel outputs. Reads scored output from engine.scoring; holds no gate rules."""
import math
import re
from collections import Counter, defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from . import scoring as E

HEAD = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="0077BB")
NOTE = Font(italic=True, color="605E5C")
PROTOCOL_IDS = {"C%02d" % i for i in range(1, 24)} | {"R%02d" % i for i in range(1, 12)}
RANGE_STATUS = "Provisional: sample only, Allshares to approve"


def _sheet(wb, title, header, rows, widths=None):
    ws = wb.create_sheet(title)
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = HEAD, HEAD_FILL
    for r in rows:
        ws.append(list(r))
    ws.freeze_panes = "A2"
    for i, h in enumerate(header, start=1):
        w = (widths or {}).get(h) or min(60, max(10, len(str(h)) + 2))
        ws.column_dimensions[get_column_letter(i)].width = w
    if rows:
        ws.auto_filter.ref = ws.dimensions
    return ws


def companies_note(facts):
    d = facts["duplicates"]
    s = "%d companies from %d company IDs" % (facts["companies"], facts["company_ids"])
    if d:
        s += " (%s are the same company: LEI %s; counted once)" % (" and ".join(d[0]["ids"]), d[0]["lei"])
    return s


# ---------------------------------------------------------------- scoring workbook
def write_scoring_workbook(path, scored, reg, facts, summary, cfg):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    filled = [x for x in scored if x["result"]]
    n = len(filled)

    # Value scoring first so Summary formulas can point at it.
    vrows = []
    for x in filled:
        r, res = x["row"], x["result"]
        vrows.append([r["company_id"], facts["key_by_id"][r["company_id"]], r["company_name"], r["country"],
                      r["grain"], r["role_row"], r["data_point"], reg[r["data_point"]]["field_id"],
                      reg[r["data_point"]]["category"], "Pay" if reg[r["data_point"]]["pay"] else "Company",
                      r["value"][:200], r["unit"], r["period_end"], r["method"], x["value_status"],
                      res["passed"], res["applicable"], res["not_run"], len(res["hard"]), None, None,
                      "; ".join("%s %s: %s" % (g["gate"], g["result"].lower(), g["reason"])
                                for g in x["gates"] if g["result"] != E.PASS)])
    hdr = ["company_id", "company_key (LEI)", "company_name", "country", "grain", "role_row", "data_point",
           "field_id", "category", "data_type", "value", "unit", "period_end", "method", "value_status",
           "passed", "applicable", "not_run", "hard_fails", "score", "status", "reasons"]
    ws_v = _sheet(wb, "Value scoring", hdr, vrows, {"company_name": 30, "value": 40, "reasons": 80, "role_row": 28})
    last = n + 1
    for i in range(2, last + 1):
        # Live formulas: thresholds come from the Summary sheet.
        ws_v["T%d" % i] = "=ROUND(P%d/Q%d*100,0)" % (i, i)
        ws_v["U%d" % i] = ('=IF(S{0}>0,"Fail (hard)",IF(R{0}>0,"Incomplete",IF(T{0}>=Summary!$B$4,"Pass",'
                           'IF(T{0}>=Summary!$B$5,"Review","Fail"))))').format(i)

    ws = wb.create_sheet("Summary", 0)
    ws.append(["Allshares Part 1 accuracy scoring: tracker_first50.csv"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append([companies_note(facts)])
    ws["A2"].font = NOTE
    ws.append(["Setting", "Value"])
    ws.append(["Pass threshold (score >=)", cfg["thresholds"]["pass"]])
    ws.append(["Review threshold (score >=)", cfg["thresholds"]["review"]])
    ws.append([])
    ws.append(["Measure", "Formula result", "Engine result"])
    rng = "'Value scoring'!$U$2:$U$%d" % last
    measures = [("Values scored", "=COUNTA('Value scoring'!$A$2:$A$%d)" % last, summary["values"])]
    for s in ("Pass", "Review", "Fail", "Fail (hard)", "Incomplete"):
        measures.append(("Status: " + s, '=COUNTIF(%s,"%s")' % (rng, s), summary["status"].get(s, 0)))
    gr = "'Gate results'!$F$2:$F$%d" % (sum(len(x["gates"]) for x in filled) + 1)
    for g in (E.PASS, E.FAIL, E.NOT_RUN):
        measures.append(("Gates " + g, '=COUNTIF(%s,"%s")' % (gr, g), summary["gates"].get(g, 0)))
    measures.append(("Hard FAIL", "=COUNTIFS(%s,\"FAIL\",'Gate results'!$E$2:$E$%d,\"Hard\")" %
                     (gr, sum(len(x["gates"]) for x in filled) + 1), summary["hard_fail"]))
    measures.append(("Checks passing % (PASS / (PASS+FAIL))", "=ROUND(B14/(B14+B15)*100,1)",
                     round(summary["gates"][E.PASS] / (summary["gates"][E.PASS] + summary["gates"][E.FAIL]) * 100, 1)))
    measures.append(("Companies (distinct LEI)", facts["companies"], facts["companies"]))
    measures.append(("Company IDs in tracker", facts["company_ids"], facts["company_ids"]))
    measures.append(("Data points", len(reg), len(reg)))
    for m in measures:
        ws.append(list(m))
    ws.append([])
    ws.append(["Formula results recalculate from the Value scoring and Gate results sheets; change the thresholds "
               "in B4:B5 to see the status split move. Engine result is the build's own count."])
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 16
    for c in ws[3] + ws[7]:
        c.font = Font(bold=True)

    grows = []
    for x in filled:
        r = x["row"]
        for g in x["gates"]:
            grows.append([r["company_id"], r["data_point"], r["role_row"], g["gate"], E.GATES[g["gate"]][1],
                          g["result"], g["reason"]])
    _sheet(wb, "Gate results", ["company_id", "data_point", "role_row", "gate", "severity", "result", "reason"],
           grows, {"reason": 70, "role_row": 28})

    # Company summary by LEI
    by = defaultdict(lambda: Counter())
    names, ids, ctry = {}, defaultdict(set), {}
    for x in scored:
        r = x["row"]
        k = facts["key_by_id"][r["company_id"]]
        names.setdefault(k, r["company_name"])
        ids[k].add(r["company_id"])
        ctry[k] = r["country"]
        by[k]["rows"] += 1
        by[k][x["value_status"]] += 1
        if x["result"]:
            by[k][x["result"]["status"]] += 1
    crow = []
    for k, c in by.items():
        crow.append([k, names[k], ctry[k], ", ".join(sorted(ids[k])), c["rows"], c["found"], c["partial"],
                     c["not_found"], c["Pass"], c["Review"], c["Fail"], c["Fail (hard)"], c["Incomplete"],
                     "same company under %d IDs" % len(ids[k]) if len(ids[k]) > 1 else ""])
    _sheet(wb, "Company summary", ["company_key (LEI)", "company_name", "country", "company_ids", "rows", "found",
                                   "partial", "not_found", "Pass", "Review", "Fail", "Fail (hard)", "Incomplete",
                                   "note"], sorted(crow, key=lambda r: (r[2], r[1])), {"company_name": 36})

    frows = []
    for g in E.GATES:
        pg = summary["per_gate"].get(g, {})
        runs = sum(pg.values())
        if not runs:
            continue
        frows.append([g, E.GATES[g][0], E.GATES[g][1], runs, pg.get(E.PASS, 0), pg.get(E.FAIL, 0),
                      pg.get(E.NOT_RUN, 0)])
    _sheet(wb, "Gate frequency", ["gate", "name", "severity", "runs", "pass", "fail", "not run"], frows,
           {"name": 44})

    rules = []
    for g, (name, sev) in E.GATES.items():
        fields = sorted(d for d, gs in E.FIELD_GATES.items() if g in gs)
        if g in E.CORE:
            fields = ["all values"]
        if g == "NUM-06":
            fields = ["largest_holders", "sti_max / sti_target when unit is %"]
        if g in E.DER_GATES:
            fields = ["DERIVED values in pay, workforce, segment, role and ownership categories"]
        rules.append([g, name, sev, ", ".join(fields) or "not applied to tracker fields"])
    _sheet(wb, "Gate rules", ["gate", "name", "severity", "applies to"], rules, {"name": 44, "applies to": 80})

    dec = [list(d) + ["Open"] for d in E.DECISIONS]
    dec.append(["D13", "cik has no protocol field ID (not in C01-C23)", "Kept as data point; shown as n/a",
                "Field Checks rows for cik cannot carry a valid protocol ID", "Allshares", "Open"])
    dec.append(["D14", "Company count: T0668 and T0671 share LEI 549300HX9MRFY47AH564",
                "Counted once by LEI (49 companies); both IDs' rows kept", "All company counts", "Allshares",
                "Open: confirm and de-duplicate in the tracker"])
    ws_d = _sheet(wb, "Decisions", ["id", "decision", "default used", "effect today", "owner", "status"], dec,
                  {"decision": 60, "default used": 60, "effect today": 44})
    for row in ws_d.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


# ---------------------------------------------------------------- ranges
def percentile(sorted_vals, p):
    """Linear interpolation between closest ranks (same as Excel PERCENTILE.INC)."""
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return sorted_vals[int(k)]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


RANGE_FIELDS = ["aggregate_headcount", "base_salary", "benefits_value", "ebitda", "fte", "headcount", "lti_granted",
                "lti_max", "lti_target", "lti_vested", "pension_contribution", "revenue", "share_price",
                "shares_outstanding", "sti_max", "sti_paid", "sti_target", "total_assets", "total_remuneration"]


def range_unit(unit):
    return "unknown" if unit in ("", "instruments") else unit


def compute_ranges(rows, facts, lo=0.05, hi=0.95):
    groups = defaultdict(list)
    for r in rows:
        if r["data_point"] not in RANGE_FIELDS:
            continue
        n = E._num(r["value"])
        if n is None:
            continue
        groups[(r["data_point"], range_unit(r["unit"]))].append((n, facts["key_by_id"][r["company_id"]]))
    out = []
    for (dp, unit), xs in sorted(groups.items()):
        vals = sorted(v for v, _ in xs)
        med = percentile(vals, 0.5)
        cav = []
        if any(v == 0 for v in vals):
            cav.append("zero values present (check not found vs true zero)")
        if dp == "ebitda":
            cav.append("losses expected; negatives are valid")
        if med and med > 0 and vals[-1] > 100 * med:
            cav.append("max is over 100x median: possible unit error")
        if unit == "unknown":
            cav.append("currency not recorded")
        if unit == "EURO":
            cav.append("non-ISO unit label")
        if len(vals) < 10:
            cav.append("n under 10: indicative only")
        out.append([dp, unit, len(vals), len({k for _, k in xs}), vals[0], percentile(vals, lo), med,
                    percentile(vals, hi), vals[-1], RANGE_STATUS, "; ".join(cav) or None])
    return out


RANGE_NOTES = [
    "Provisional ranges: computed from the first 50 tracker company IDs ({companies}; 2,584 filled values).",
    "They are NOT Allshares-approved and are NOT published survey data.",
    "Method: min, 5th percentile, median, 95th percentile and max per field and unit (linear interpolation, "
    "as Excel PERCENTILE.INC). Values are stored in base units.",
    "Money fields are split by currency. Non-currency fields are split by unit (people, employees, shares, "
    "% of base salary). Companies are counted by LEI.",
    "No outliers are removed. Caveats are listed per row.",
    "Sample is small for many rows (n under 10). Treat those ranges as indicative only.",
    "Gate NUM-04 (magnitude in plausible range) stays NOT RUN until Allshares approves ranges. "
    "These ranges are not yet applied to scoring.",
    "Known data issues to fix before ranges are used: zero values that may be 'not found', mixed units in "
    "revenue (for example SEK), and the non-ISO label 'EURO'.",
    "Next steps: Allshares to confirm or replace each range, and to set ranges for fields not listed here "
    "(for example headcount by sector and size).",
]


def _range_sheets(wb, ranges, facts):
    _sheet(wb, "Provisional Ranges", ["Field", "Unit / currency", "Values (n)", "Companies", "Min", "5th percentile",
                                      "Median", "95th percentile", "Max", "Status", "Data caveat"], ranges,
           {"Field": 22, "Status": 44, "Data caveat": 60})
    ws = wb.create_sheet("Range Notes")
    for line in RANGE_NOTES:
        ws.append([line.format(companies=companies_note(facts))])
    ws.column_dimensions["A"].width = 140


def write_ranges_workbook(path, rows, reg, facts):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    ranges = compute_ranges(rows, facts)
    _range_sheets(wb, ranges, facts)
    wb.save(path)
    return ranges


# ---------------------------------------------------------------- field checks
def fix_field_checks(src, dst, facts, ranges):
    """Corrected copy of allshares_field_checks.xlsx.

    - Weighted score formulas use one absolute range for every row (they had drifting end rows).
    - market_cap_band uses protocol ID C17 (shares outstanding, for the market cap band).
    - Range sheets rebuilt; notes state 49 companies.
    """
    wb = openpyxl.load_workbook(src)
    ws = wb["Field Checks"]
    last = ws.max_row
    while last > 1 and not ws.cell(last, 1).value:
        last -= 1
    for i in range(2, last + 1):
        ws.cell(i, 11).value = "=J{0}/SUMIF($A$2:$A${1},A{0},$J$2:$J${1})".format(i, last)
        if ws.cell(i, 4).value == "Derived: C17 x C18":
            ws.cell(i, 4).value = "C17"
            ws.cell(i, 17).value = ((ws.cell(i, 17).value or "") + " Protocol ID C17 (market cap band is derived "
                                    "from C17 x C18).").strip()
    pm = wb["Protocol Map"]
    for row in pm.iter_rows(min_row=2):
        if row[2].value == "Derived: C17 x C18":
            row[2].value = "C17"
    for name in ("Provisional Ranges", "Range Notes"):
        if name in wb.sheetnames:
            del wb[name]
    _range_sheets(wb, ranges, facts)
    wb.save(dst)


def check_field_checks(path, allow_missing_id=("cik",)):
    """Reproducible check: weights per module sum to 1 (formulas evaluated as written)
    and every Field Checks row has a valid protocol ID. Returns (errors, warnings, sums)."""
    wb = openpyxl.load_workbook(path)
    ws = wb["Field Checks"]
    rows = []
    for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not r[0]:
            continue
        rows.append((i, r))
    score = {}
    for i, r in rows:
        j = r[9]
        if isinstance(j, str) and j.startswith("=IF("):
            score[i] = 2 if r[8] == "Hard" else 1
        else:
            score[i] = float(j)
    errors, warnings = [], []
    sums = defaultdict(float)
    for i, r in rows:
        k = r[10]
        m = re.fullmatch(r"=J(\d+)/SUMIF\(\$A\$(\d+):\$A\$?(\d+),A(\d+),\$J\$(\d+):\$J\$?(\d+)\)", str(k))
        if not m:
            errors.append("row %d: weighted score formula not recognised: %s" % (i, k))
            continue
        a0, a1, b0, b1 = int(m.group(2)), int(m.group(3)), int(m.group(5)), int(m.group(6))
        if (a0, a1) != (b0, b1):
            errors.append("row %d: SUMIF criteria and sum ranges differ" % i)
        denom = sum(score[x] for x, rr in rows if a0 <= x <= a1 and rr[0] == r[0])
        sums[r[0]] += score[i] / denom if denom else float("inf")
    for mod, s in sums.items():
        if abs(s - 1) > 1e-9:
            errors.append("module %s: weights sum to %.4f, not 1" % (mod, s))
    for i, r in rows:
        fid = r[3]
        if fid not in PROTOCOL_IDS:
            if r[2] in allow_missing_id:
                warnings.append("row %d: %s has no protocol ID (%s); listed as decision D13" % (i, r[2], fid))
            else:
                errors.append("row %d: %s has invalid protocol ID %r" % (i, r[2], fid))
    return errors, warnings, dict(sums)
