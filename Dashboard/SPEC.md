# Allshares Part 1 accuracy dashboard: specification

Version 1.0, 4 Nov 2026. Scope: extraction accuracy only (Part 1). Cross-source verification is out of scope.

This spec is the contract for the scoring pipeline, the Angular dashboard and the single-file HTML export.
When something here changes, change the spec first, then the code, then the tests listed in section 10.

## 1. Data facts

| Fact | Value | Note |
|---|---|---|
| Tracker | `tracker_first50.csv`, 3,993 rows | Read-only. Scraped values are never changed. |
| Filled values | 2,584 | Blank value = not found (1,409). |
| Company IDs | 50 | |
| Companies | **49** | T0668 and T0671 share LEI 549300HX9MRFY47AH564. Count companies by LEI; keep both IDs' rows. |
| Data points | 55 | Not 56. |
| Countries | SE, NO, DK, FI | |
| Methods | PARSE, API, XBRL, DERIVED, **SCRAPE** | SCRAPE (49 values) is not in the original brief's list. |

Every output that states a company count says 49 companies (50 IDs) and names the duplicate.

Protocol field IDs that cover several data points (imports must give `data_point`):
C01, C05, C07, C08, C15, C17, C20, C23, R06, R07, R08. `cik` has no protocol ID (decision D13).

## 2. Architecture

```
tracker_first50.csv ──► accuracy/engine/scoring.py  (all gate rules, one place)
                              │
                     accuracy/build.py  (one command)
        ┌──────────────┬──────┴───────┬───────────────────┬──────────────────┐
  out/report.json  schema .js/.json  allshares_report.html  Excel workbooks
        │                                (single file)
  Dashboard/app (Angular) ◄── Dashboard/core/report-core.js ──► single-file HTML
```

- `accuracy/engine/scoring.py`: the only place gate rules live.
- `Dashboard/core/report-core.js`: the only place for front-end logic (filters, aggregations, import
  validation and upsert, ranges, metrics). No gate rules. Used by the Angular app and inlined in the HTML.
- Front ends render; they do not compute rules.
- Dependencies: Python 3 stdlib + openpyxl; vanilla JS for the core and the HTML; Angular (npm) for the
  app only (agreed 4 Nov 2026).
- Charts: the Angular app uses Apache ECharts 6 with the SVG renderer (`app/src/app/chart.ts`, agreed
  4 Nov 2026: use an existing chart library). The single-file HTML keeps the small built-in SVG builders in
  `core/report-charts.js` so it stays self-contained and light. Both follow DESIGN.md section 5.
- UI library: the Angular app uses Bootstrap 5.3 CSS (agreed 4 Nov 2026), CSS only, no Bootstrap JS: navbar
  and underline tabs, `form-select`/`form-control` filters, cards for KPIs and panels, `table table-sm
  table-hover`, `btn` buttons, `alert` callouts, `badge` chips and `breadcrumb` on Validation steps.
  Bootstrap's colours are mapped to the DESIGN.md palette in `app/src/bootstrap-theme.css`. The single-file
  HTML stays on `core/report.css` only, so it has no external dependency.

## 3. Scoring engine

### 3.1 Gates

Every filled value gets CORE-01..05 plus its field-specific gates. Result per gate: PASS, FAIL, NOT RUN.
A gate that does not apply is not listed (N/A, excluded from counts).

Hard (a FAIL blocks the value): CORE-01, CORE-02, COD-01, COD-03, COD-06, NUM-01, NUM-05, NUM-06, NUM-07,
NUM-09, NUM-11, DES-01, DES-02, DER-02, DER-03, DER-05, DER-07, XF-01, XF-03.

Soft (a FAIL lowers the score): CORE-03, CORE-04, CORE-05, COD-02, COD-04, COD-05, NUM-02, NUM-03, NUM-04,
NUM-08, NUM-10, NUM-12, DER-01, DER-06, DER-08, DER-09.

Always NOT RUN today: COD-04 (cross-source), NUM-03 (no annualisation fields), NUM-04 (no Allshares ranges),
NUM-10 (no performance-period fields), DER-08, DER-09.

### 3.2 Status per value

1. Any hard FAIL → **Fail (hard)**
2. Else any NOT RUN → **Incomplete**
3. Else score = passed / applicable × 100 → **Pass** ≥ 95, **Review** ≥ 80, else **Fail**.

Thresholds are configurable (`accuracy/config.json`), default 95 / 80.

### 3.3 Value status (protocol style)

- found: value, plus a unit when the protocol field is numeric, plus a period when the field is time-bound
- partial: value present but unit or period missing
- not_found: blank

Static (not time-bound) categories: Identity, Listing and market, Sector, Reporting basis.

### 3.4 Baseline that must reproduce

| Measure | Count |
|---|---|
| Values scored | 2,584 |
| Pass / Review / Fail / Fail (hard) / Incomplete | 683 / 493 / 8 / 404 / 996 |
| Gates PASS / FAIL / NOT RUN | 15,311 / 1,287 / 2,433 |
| Hard FAIL | 438 |
| Checks passing (PASS / (PASS + FAIL)) | 92.2% |
| Found % (found / all rows) | 49.0% |

`accuracy/tests/diff_baseline.py` checks these totals and every cell of the earlier report
(country × gate, country × field, per company, per-row value status). It must report 0 differences
while the defaults are unchanged.

### 3.5 Open decisions

Configurable or flagged, never hard-coded as answers. Listed in the Decisions sheet with the default used
and owner (Allshares): D01 LTI basis mapping, D02 STI cap above 100%, D03 pension keywords, D04 segment
tolerance, D05 FTE basis, D06 reference ranges, D07 ISO/taxonomy lists, D08 internal source ID,
D09 thresholds, D10 total components and tolerance, D11 NUM-11 tolerance, D12 annualisation and
performance period, D13 cik without protocol ID, D14 duplicate company IDs.

## 4. Build

`python accuracy/build.py` regenerates, in one run:

| Output | Where |
|---|---|
| `report.json` (scored values, gates, reasons, meta, baseline) | `accuracy/out/`, copied to `Dashboard/app/public/` and `Dashboard/` |
| `allshares_import_schema.json` and `.js` | `accuracy/out/` and `Dashboard/` |
| `allshares_results_template.csv` | `accuracy/out/` |
| `allshares_report.html` (single file, data and schema inline) | `accuracy/out/` and `Dashboard/` |
| `scored_values.csv`, `gate_results.csv` | `accuracy/out/` |
| `allshares_first50_scoring.xlsx` | Summary (live formulas), Value scoring, Gate results, Company summary, Gate frequency, Gate rules, Decisions |
| `allshares_reference_ranges.xlsx` | Provisional ranges, labelled NOT Allshares-approved |
| `allshares_field_checks.xlsx` (corrected copy) | fixed weight formulas, C17 for market_cap_band, 49 companies |
| `allshares_part1_validation.html` (corrected copy) | 49 companies |

The schema source is `accuracy/schema/allshares_import_schema.json`. Edit only that file.

## 5. Report data contract (`report.json`)

```
meta:     tracker, asOf, built, rows, filled, dataPoints, companyIds, companies, duplicates[], thresholds, target
gates:    { "CORE-01": [name, "Hard"|"Soft"], ... }
gateIds:  [ ...gate ids, index used in values[].gr ]
reasons:  [ ...distinct reason texts, index used in values[].gr ]
values[]: s source (T tracker, I import), c country, o company name, ck company key (LEI, else ID), id company ID,
          g grain, r role row, p 1 if pay data, k category, m module, f field ID, d data point,
          v value, u unit, st value status,
          filled only: pe period end, me method, so source, ep locator URL, nt note (first 300 chars),
          sc score status (P R F H I), sp score, gr [[gateIndex, "P"|"F"|"N", reasonIndex|-1], ...]
baseline: checksPct, foundPct, label
```

Pay data = categories Pay policy, Role and disclosure, Pay: fixed, Pay: STI, Pay: LTI, Pay: total.
Company data = everything else.

## 6. Dashboard (Angular app and single-file HTML: same pages, same numbers)

### 6.1 Layout

- Top bar: title, page tabs, values count.
- Filters (sticky, top, apply to every page): Country, Source (all / tracker / imported), Data type
  (all / company / pay), Field group (category), Company, Score status.
- KPI strip (sticky): Companies (distinct LEI), Countries, Values in view, Found %, Partial, Not found,
  Checks passing (vs tracker baseline and the 95% target), Values passing (Pass status), Hard fails,
  Imports applied. Each card has a comparison line.
- Footer: data source, data date, imports applied, values in view, 49 companies from 50 IDs.

### 6.2 Charts

SVG only, fixed height about 230 px, at most 5 colours from #0077BB, #EE7733, #009988, #CC3311, #888888.
Red (#CC3311) only for problems. Pies have at most 5 segments. Chart and page titles state the finding as
computed text, not a label.

Score status colours: Pass #009988, Review #0077BB, Incomplete #888888, Fail #EE7733, Fail (hard) #CC3311.

### 6.3 Pages

1. **Overview**: companies by country, value-status pie, country summary table.
2. **Pay vs company**: status by data type, share of values, by-country table.
3. **Countries**: status by country, companies by country, country × data type table.
4. **Fields** (new): one row per data point: field ID, category, rows, found, partial, not found, Pass,
   Review, Incomplete, Fail, Fail (hard), pass %, average score. Stacked bar of score status for the
   12 fields with most failures. Search and sort. Click a field to see every value of that field across
   companies (company, role, value, unit, status, score, reasons) and the companies where it is empty.
5. **Empty fields** (new): not-found values only. KPIs: empty values, fields with any empty, companies
   affected. Charts: top 12 fields by empty count, empty by data type. Tables: by field (rows, empty,
   empty %, companies with it empty), by company (rows, empty, empty %, empty fields listed). Click a
   company to open it on the Companies page.
6. **Companies** (new): one row per company (by LEI): country, IDs, rows, found, partial, not found, Pass,
   Review, Incomplete, Fail, Fail (hard), average score. Search and sort. Click to drill down: header
   (name, country, LEI, IDs, duplicate note), status pie, failures by gate, and a values table (category,
   field, role, value, unit, period, method, value status, score status, score, failed and not-run gates
   with reasons, source and locator link). Filter the table: all / problems only / empty only.
7. **Failures**: fails by check (top 12, hard red, soft orange), hard vs soft pie, fail rate by module,
   fail rate by field (top 12), fails-by-field table, and a "most attention" callout naming the hard check
   with the most fails. Computed from per-value gates, so every filter applies.
7a. **Validation steps** (new, 4 Nov 2026): the gates as the steps of the validation, grouped by family in
   this order: Core checks (CORE), Codes and lists (COD), Numbers (NUM), Descriptive claims (DES), Derived
   values (DER), Cross-field (XF).
   - Level 1, steps: chart of pass rate by family; table of every gate that ran: ID, name, hard/soft,
     fields it applies to, runs, PASS, FAIL, NOT RUN, pass rate of run checks, most common reason.
   - Level 2, one step (click a row): counts, fails by field (top 12), reasons with counts, and a table of
     the fields the step runs on (runs, PASS, FAIL, NOT RUN, fail rate).
   - Level 3, one step on one field (click a field): every value checked: company, country, role, value,
     unit, result, reason, overall score status. Filter: all / FAIL / NOT RUN / PASS. Click a company to open
     it on the Companies page.
   - URLs: `#/steps`, `#/steps/<gate>`, `#/steps/<gate>/<data_point>`. Every global filter applies.
8. **Ranges** (new): table with Field, Unit / currency, Values (n), Companies, Min, low percentile,
   Median, high percentile, Max, Caveat. Configurable: field, unit, grain, method, score status included
   (all / no hard fails / Pass and Review only), exclude zeros, exclude unknown or non-ISO units, low and
   high percentile (default 5 and 95), minimum n, split by country. Export CSV. Labelled provisional,
   sample only, not Allshares-approved. Percentiles use linear interpolation (Excel PERCENTILE.INC), the
   same as the Excel ranges workbook.
9. **Trend**: line chart of checks passing % and found % from the tracker baseline (92.2% / 49%) and after
   each import; per-import table of schema check pass rates (Required fields, Allowed values, Role row,
   Value when found, Unit when numeric, Data point when ambiguous).
10. **Metric register** (new): Metric, Category, Source module, Formula or method, Period, Value, Target,
    Trend, Owner, Last updated, Metric ID, for the current view. Targets only where agreed (95% checks
    passing); others show "not set". Owner "not assigned" until Allshares names one. Export CSV (UTF-8 BOM).
11. **Import data**: see section 7.

## 7. Import

- File: CSV in the schema format (`results_<CC>.csv` columns plus optional `lei` and `data_point`).
- Validate every row against the schema; show errors (first 50) and a preview:
  added / updated / unchanged / duplicates / ambiguous.
- Apply valid rows; Reset restores the tracker values and clears the trend.
- Upsert:
  1. Company: by LEI when the row gives an LEI known in the data, otherwise by company name + country.
  2. Record: field ID + role row + data_point.
  3. Value, unit or status differs → update (score cleared: imported values are not gate-scored);
     identical → unchanged; no match → add.
  4. No data_point and several records match → error (ambiguous), row skipped.
- In-memory only (browser session). No persistence (agreed 4 Nov 2026).

## 8. Excel checks

- Module Check weights sum to 1 per module, evaluating each row's formula as written
  (`accuracy/tests/check_field_checks.py`). The original workbook fails this (drifting SUMIF ranges).
- Every Field Checks row has a valid protocol ID (C01–C23, R01–R11); cik is a listed exception (D13).
- Excel formulas recalculate with zero errors (`accuracy/tests/excel_recalc.ps1`, uses Excel).

## 9. Labelling rules

- Never invent company values. Examples are illustrative and labelled "Illustrative example".
- Provisional ranges are labelled "Provisional: sample only, Allshares to approve".

## 10. Tests

| Test | Command |
|---|---|
| Engine reproduces baseline | `python accuracy/tests/diff_baseline.py` |
| Field Checks weights and IDs | `python accuracy/tests/check_field_checks.py` |
| Core logic (filters, import, ranges, metrics) | `node Dashboard/core/report-core.test.js` |
| Single-file HTML in a DOM stub (KPIs, filters, failures attention, import preview/apply/reset, trend, new pages) | `node accuracy/tests/report_dom.test.js` |
| Angular app builds and unit tests pass | `npm --prefix Dashboard/app test` |
| Excel recalculation, zero errors | `powershell -ExecutionPolicy Bypass -File accuracy/tests/excel_recalc.ps1` |

Angular 21 is used because this machine runs Node 22.20; Angular 22 needs Node 22.22.3 or later.

A browser check by a person is still needed for layout and interaction.
