"""A plain-language Excel report of what legal's source rules would do to our data.

Reads output/source_rules_impact_values.csv (from extractor.source_impact) and the combined
file for the totals, and writes output/legal_rules_impact.xlsx. Nothing is enforced.

    python -m extractor.legal_impact_report
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .rerun_list import PRIORITY

ROOT = Path(__file__).resolve().parent.parent
VALUES = ROOT / "output" / "source_rules_impact_values.csv"
COMBINED = ROOT / "output" / "fy2025_runs_datapoints.csv"
OUT = ROOT / "output" / "legal_rules_impact.xlsx"

# rule code -> (plain name, what legal's rule says, what it means for the value, outcome group)
LOST, LINK, ASK = "Must be re-read from an allowed source", "Can stay, but a missing link must be recorded", \
    "Waiting on legal's answer"
RULES = {
    "blocked host": (
        "Website is on legal's blocked list",
        "Do not download from stock exchanges (Oslo Børs, Euronext, Nasdaq, JSE), the listed news sites "
        "(eMarket Storage, 1info, EQS, Q4, InvestorWeb, MFN, Cision, hauptversammlung.de) or PDFs on cdn.sanity.io.",
        "The value cannot be used. It must be read again from the company's own website or its national "
        "filing archive.", LOST),
    "identifier: OpenFIGI only for FIGI": (
        "Identifier taken from OpenFIGI",
        "Only the FIGI code may come from OpenFIGI.",
        "Ticker, ISIN, exchange or listing status read from OpenFIGI must be taken from the allowed source "
        "instead (GLEIF for ISIN; ESMA FIRDS or the annual report for the rest).", LOST),
    "identifier: ISIN only from GLEIF": (
        "ISIN not taken from GLEIF",
        "The ISIN must come from GLEIF's ISIN-to-LEI file.",
        "The ISIN must be looked up again in GLEIF's ISIN-to-LEI file.", LOST),
    "identifier: exchange/listing from FIRDS or annual report": (
        "Exchange or listing status from another source",
        "Exchange and listing status must come from ESMA FIRDS or the annual report.",
        "The value must be taken again from ESMA FIRDS or the annual report.", LOST),
    "robots.txt disallows all crawlers": (
        "Website's robots.txt forbids automated downloads",
        "Respect robots.txt before every download; skip and log if blocked.",
        "The document could not be downloaded under the rule, so the value is lost unless an allowed copy "
        "exists (for example in the national filing archive).", LOST),
    "robots.txt disallows FirecrawlAgent": (
        "Website's robots.txt forbids our crawler by name",
        "Respect robots.txt before every download; skip and log if blocked.",
        "As above: the value is lost unless an allowed copy exists.", LOST),
    "TDM reservation (TDM-Rep)": (
        "Website opts out of text and data mining (TDM-Rep)",
        "Respect text-and-data-mining opt-outs (TDM-Rep header, tdmrep.json).",
        "As above: the value is lost unless an allowed copy exists.", LOST),
    "ai.txt disallows": (
        "Website's ai.txt forbids AI use",
        "Respect ai.txt opt-outs.",
        "As above: the value is lost unless an allowed copy exists.", LOST),
    "referrer missing (file host)": (
        "Document on a file-hosting service, linking page not recorded",
        "When a file sits on a web host (Contentful, Cloudinary, Storyblok and similar), record the "
        "company page that links to it.",
        "The value can stay. We must find and record the company web page that links to the document.", LINK),
    "bucket file: original URL not recorded": (
        "Document from the shared CDP bucket, original web address not recorded",
        "Record the document URL on every value.",
        "The value can stay. The bucket's file details do not say where the document was downloaded "
        "from, so that address must be found and recorded.", LINK),
    "question: filings.xbrl.org": (
        "Read from filings.xbrl.org (not on legal's list)",
        "Values must come from the company's own website or its national filing archive.",
        "filings.xbrl.org republishes the official ESEF filings but is neither the company's site nor a "
        "national archive. Legal must say whether it counts; if not, these values must be re-read from "
        "the national archive copy of the same filing.", ASK),
}
ORDER = list(RULES)
GROUP_RANK = {LOST: 0, LINK: 1, ASK: 2}
NOT_AFFECTED = "Not affected"

FONT = "Arial"
H1 = Font(name=FONT, size=14, bold=True)
H2 = Font(name=FONT, size=11, bold=True)
BOLD = Font(name=FONT, bold=True)
NORMAL = Font(name=FONT)
NOTE = Font(name=FONT, italic=True, color="555555")
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(name=FONT, bold=True, color="FFFFFF")
FILLS = {LOST: "F8CBAD", LINK: "FFE699", ASK: "BDD7EE", NOT_AFFECTED: "C6E0B4"}
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
INT, PCT = "#,##0;-#,##0;-", "0.0%;-0.0%;-"


def _header(ws, row: int, names: list[str], widths: list[int] | None = None) -> None:
    for i, n in enumerate(names, 1):
        c = ws.cell(row, i, n)
        c.font, c.fill, c.alignment, c.border = HEAD_FONT, HEAD_FILL, WRAP, BOX
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def _put(ws, row: int, col: int, value, fmt: str | None = None, font=NORMAL, fill: str | None = None):
    c = ws.cell(row, col, value)
    c.font, c.border, c.alignment = font, BOX, WRAP
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = PatternFill("solid", fgColor=fill)
    return c


def build(values: Path = VALUES, combined: Path = COMBINED, out: Path = OUT) -> dict:
    with open(combined, encoding="utf-8-sig", newline="") as fh:
        all_rows = [r for r in csv.DictReader(fh) if r["value"]]
    with open(values, encoding="utf-8-sig", newline="") as fh:
        vals = list(csv.DictReader(fh))
    total = len(all_rows)
    total_priority = sum(r["data_point"] in PRIORITY for r in all_rows)
    per_field = Counter(r["data_point"] for r in all_rows)
    names: dict[str, tuple[str, str]] = {}
    for r in all_rows:
        names.setdefault(r["company_id"], (r["company_name"], r["country"]))
    per_company = Counter((r["company_id"], *names[r["company_id"]]) for r in all_rows)
    for v in vals:
        v["company_name"], v["country"] = names.get(v["company_id"], (v["company_name"], v["country"]))

    for v in vals:
        codes = [c for c in ORDER if c in v["rules"].split("; ")]
        v["_codes"] = codes
        v["_group"] = min((RULES[c][3] for c in codes), key=GROUP_RANK.get) if codes else NOT_AFFECTED

    wb = Workbook()
    wb.calculation.fullCalcOnLoad = True

    # --- Detail sheet first (the others count from it) ---------------------------------------------
    det = wb.active
    det.title = "Affected values"
    cols = ["Company", "Country", "Field", "Priority field", "Value", "Source as recorded", "Document URL",
            "Linking company page", "Website", "Rules it breaks", "Result", "What must happen",
            "Where to read it again", "Came via the CDP bucket (file address)"]
    det.cell(1, 1, "Every value touched by at least one of legal's rules (one row per value)").font = H1
    _header(det, 2, cols, [34, 8, 22, 9, 28, 28, 50, 40, 30, 45, 30, 60, 34, 40])
    det.freeze_panes = "A3"
    vals.sort(key=lambda v: (GROUP_RANK[v["_group"]], v["company_name"], v["data_point"]))
    for i, v in enumerate(vals, 3):
        row = [v["company_name"], v["country"], v["data_point"], "yes" if v["priority_field"] else "",
               v["value"], v["source"], v["document_url"], v["referrer_url"], v["host"] or "(not recorded)",
               "; ".join(RULES[c][0] for c in v["_codes"]), v["_group"],
               " ".join(dict.fromkeys(RULES[c][2] for c in v["_codes"])), v["replacement_source"],
               v["via_bucket"]]
        for j, x in enumerate(row, 1):
            c = det.cell(i, j, x)
            c.font = NORMAL
        det.cell(i, 11).fill = PatternFill("solid", fgColor=FILLS[v["_group"]])
    last = len(vals) + 2
    det.auto_filter.ref = f"A2:{get_column_letter(len(cols))}{last}"
    R = lambda col: f"'Affected values'!${col}$3:${col}${last}"  # noqa: E731
    RULE, RESULT, PRIO, FIELD, COMP, HOST = R("J"), R("K"), R("D"), R("C"), R("A"), R("I")

    # --- Summary ---------------------------------------------------------------------------------
    s = wb.create_sheet("Summary", 0)
    s.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", [44, 13, 12, 13, 12, 58, 4]):
        s.column_dimensions[col].width = w
    s["A1"] = "Legal's data-source rules: what they would do to our FY2025 data"
    s["A1"].font = H1
    s["A2"] = ("Measured on the combined FY2025 file. The rules are not applied yet: this shows what would "
               "change if they were.")
    s["A2"].font = NOTE
    s["A4"], s["B4"] = "Values in the file", total
    s["A5"], s["B5"] = "of which priority-field values", total_priority
    s["A6"], s["B6"] = "Companies", len(per_company)
    for r in (4, 5, 6):
        s[f"A{r}"].font, s[f"B{r}"].font, s[f"B{r}"].number_format = BOLD, BOLD, INT
    s["C4"] = "Source: output/fy2025_runs_datapoints.csv (rows with a value)"
    s["C4"].font = NOTE

    s["A8"] = "1. The bottom line: each value counted once, by its most serious result"
    s["A8"].font = H2
    _header(s, 9, ["Result", "Values", "% of all values", "Priority-field values", "% of priority values",
                   "What it means"])
    meaning = {
        LOST: "The value cannot be used as it is. It has to be read again from the company's own site, the "
              "national filing archive, GLEIF or ESMA FIRDS.",
        LINK: "The value is fine, but we must add the company page that links to the document, or the "
              "document's original web address.",
        ASK: "Only rule touched is filings.xbrl.org. Fine if legal accepts it as a filing archive; otherwise "
             "these move to the first row.",
        NOT_AFFECTED: "No change needed.",
    }
    for i, g in enumerate([LOST, LINK, ASK], 10):
        _put(s, i, 1, g, font=BOLD, fill=FILLS[g])
        _put(s, i, 2, f'=COUNTIF({RESULT},A{i})', INT)
        _put(s, i, 3, f"=B{i}/$B$4", PCT)
        _put(s, i, 4, f'=COUNTIFS({RESULT},A{i},{PRIO},"yes")', INT)
        _put(s, i, 5, f"=D{i}/$B$5", PCT)
        _put(s, i, 6, meaning[g])
    _put(s, 13, 1, NOT_AFFECTED, font=BOLD, fill=FILLS[NOT_AFFECTED])
    _put(s, 13, 2, "=B4-SUM(B10:B12)", INT)
    _put(s, 13, 3, "=B13/$B$4", PCT)
    _put(s, 13, 4, "=B5-SUM(D10:D12)", INT)
    _put(s, 13, 5, "=D13/$B$5", PCT)
    _put(s, 13, 6, meaning[NOT_AFFECTED])
    _put(s, 14, 1, "Total", font=BOLD)
    for col in "BD":
        _put(s, 14, ord(col) - 64, f"=SUM({col}10:{col}13)", INT, BOLD)
    for col in "CE":
        _put(s, 14, ord(col) - 64, f"=SUM({col}10:{col}13)", PCT, BOLD)
    _put(s, 14, 6, "")

    s["A16"] = "2. Rule by rule (a value can break more than one rule, so these rows overlap)"
    s["A16"].font = H2
    _header(s, 17, ["Rule", "Values", "% of all values", "Priority-field values", "Companies",
                    "What legal's rule says / what it means for the value"])
    r = 18
    for code in ORDER:
        name, says, means, group = RULES[code]
        n_comp = len({v["company_name"] for v in vals if code in v["_codes"]})
        _put(s, r, 1, name, font=BOLD, fill=FILLS[group])
        _put(s, r, 2, f'=COUNTIF({RULE},"*"&A{r}&"*")', INT)
        _put(s, r, 3, f"=B{r}/$B$4", PCT)
        _put(s, r, 4, f'=COUNTIFS({RULE},"*"&A{r}&"*",{PRIO},"yes")', INT)
        _put(s, r, 5, n_comp, INT)
        _put(s, r, 6, f"Rule: {says}\nMeans: {means}")
        s.row_dimensions[r].height = 75
        r += 1
    s.cell(r, 1, "Companies column: counted from the 'Affected values' sheet when the file was built.").font = NOTE
    r += 2

    s.cell(r, 1, "3. Points to note").font = H2
    notes = [
        "Stock exchanges also have to move out of the 'official' sources list in CDP's web_sources.toml. "
        "That changes where we look, not any stored value, so it is not counted above.",
        "robots.txt, ai.txt and TDM opt-outs were checked live on every website and document we used "
        "(robots.txt read per the RFC 9309 standard). No website we use publishes a TDM opt-out.",
        "5 documents are sent with a 'noai' X-Robots-Tag header. That opt-out is not on legal's list, so it "
        "is not counted; it is worth asking legal whether it should be.",
        "Two bucket files belong to the wrong company (Villars holds Coty Inc.'s report, Hidong holds "
        "Mercury Securities Group Berhad's). That is a bucket problem, separate from these rules.",
        "Legal's list has 5,128 values to re-read; our count is the first row of table 1. The numbers differ "
        "a little because our file has changed since legal's snapshot. Legal's attachment "
        "(replace_list_by_host_and_field.csv) was not available here to match row by row.",
        "Colours: red = value must be re-read, yellow = value stays but a link must be added, "
        "blue = waiting on legal, green = not affected.",
    ]
    for n in notes:
        r += 1
        s.cell(r, 1, "• " + n).font = NORMAL
        s.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        s.cell(r, 1).alignment = WRAP
        s.row_dimensions[r].height = 32

    # --- By website --------------------------------------------------------------------------------
    w = wb.create_sheet("By website", 1)
    _header(w, 1, ["Website", "Values affected", "Must be re-read", "Link to add", "Waiting on legal",
                   "Priority-field values", "Companies", "Rules it breaks"], [44, 12, 12, 12, 12, 12, 11, 70])
    w.freeze_panes = "A2"
    hosts = Counter(v["host"] or "(not recorded)" for v in vals)
    for i, (h, _) in enumerate(hosts.most_common(), 2):
        hv = [v for v in vals if (v["host"] or "(not recorded)") == h]
        _put(w, i, 1, h)
        _put(w, i, 2, f"=COUNTIF({HOST},A{i})", INT)
        for j, g in enumerate([LOST, LINK, ASK], 3):
            _put(w, i, j, f'=COUNTIFS({HOST},A{i},{RESULT},"{g}")', INT)
        _put(w, i, 6, f'=COUNTIFS({HOST},A{i},{PRIO},"yes")', INT)
        _put(w, i, 7, len({v["company_name"] for v in hv}), INT)
        _put(w, i, 8, "; ".join(RULES[c][0] for c in ORDER if any(c in v["_codes"] for v in hv)))
    w.auto_filter.ref = f"A1:H{len(hosts) + 1}"

    # --- By field ------------------------------------------------------------------------------------
    f = wb.create_sheet("By field", 2)
    _header(f, 1, ["Field", "Priority field", "Values in the file", "Must be re-read", "% must be re-read",
                   "Link to add", "Waiting on legal", "Not affected"], [26, 9, 12, 12, 11, 12, 12, 12])
    f.freeze_panes = "A2"
    fields = sorted(per_field, key=lambda k: (k not in PRIORITY, -per_field[k]))
    for i, fld in enumerate(fields, 2):
        _put(f, i, 1, fld)
        _put(f, i, 2, "yes" if fld in PRIORITY else "")
        _put(f, i, 3, per_field[fld], INT)
        _put(f, i, 4, f'=COUNTIFS({FIELD},A{i},{RESULT},"{LOST}")', INT)
        _put(f, i, 5, f"=IF(C{i}=0,0,D{i}/C{i})", PCT)
        _put(f, i, 6, f'=COUNTIFS({FIELD},A{i},{RESULT},"{LINK}")', INT)
        _put(f, i, 7, f'=COUNTIFS({FIELD},A{i},{RESULT},"{ASK}")', INT)
        _put(f, i, 8, f"=C{i}-D{i}-F{i}-G{i}", INT)
    f.auto_filter.ref = f"A1:H{len(fields) + 1}"

    # --- By company ----------------------------------------------------------------------------------
    c = wb.create_sheet("By company", 3)
    _header(c, 1, ["Company", "Country", "Values in the file", "Must be re-read", "% must be re-read",
                   "Link to add", "Waiting on legal", "Not affected"], [40, 8, 12, 12, 11, 12, 12, 12])
    c.freeze_panes = "A2"
    touched = {v["company_name"] for v in vals}
    comps = sorted((k for k in per_company if k[1] in touched),
                   key=lambda k: -sum(v["company_name"] == k[1] and v["_group"] == LOST for v in vals))
    lost_by = Counter(v["company_name"] for v in vals if v["_group"] == LOST)
    comps.sort(key=lambda k: (-lost_by[k[1]], k[1]))
    for i, (_, name, ctry) in enumerate(comps, 2):
        _put(c, i, 1, name)
        _put(c, i, 2, ctry)
        _put(c, i, 3, sum(n for k, n in per_company.items() if k[1] == name), INT)
        _put(c, i, 4, f'=COUNTIFS({COMP},A{i},{RESULT},"{LOST}")', INT)
        _put(c, i, 5, f"=IF(C{i}=0,0,D{i}/C{i})", PCT)
        _put(c, i, 6, f'=COUNTIFS({COMP},A{i},{RESULT},"{LINK}")', INT)
        _put(c, i, 7, f'=COUNTIFS({COMP},A{i},{RESULT},"{ASK}")', INT)
        _put(c, i, 8, f"=C{i}-D{i}-F{i}-G{i}", INT)
    c.cell(len(comps) + 3, 1, f"{len(per_company) - len(comps)} other companies have no value touched by "
                              "any rule.").font = NOTE
    c.auto_filter.ref = f"A1:H{len(comps) + 1}"

    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    groups = Counter(v["_group"] for v in vals)
    prio = Counter(v["_group"] for v in vals if v["priority_field"])
    return {"total": total, "priority": total_priority, "companies": len(per_company),
            "groups": dict(groups), "priority_groups": dict(prio),
            "rules": {RULES[k][0]: sum(k in v["_codes"] for v in vals) for k in ORDER}}


def main(argv: list[str] | None = None) -> int:
    res = build()
    print(res)
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
