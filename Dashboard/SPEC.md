# Allshares Part 1 accuracy dashboard: specification

Version 1.1, 5 Nov 2026 (1.0, 4 Nov 2026, scored the client's tracker with its own engine). Scope: extraction accuracy only (Part 1). Cross-source verification is out of scope.

This spec is the contract for the dashboard's data, the Angular dashboard and the single-file HTML export.
When something here changes, change the spec first, then the code, then the tests listed in section 9.

## 1. Data

The data is a collector run: the data-point CSV written by `python -m extractor.datapoints` (one row per
company, role and data point; a blank value means not found). Companies are counted by LEI, falling back to
the company ID, and IDs that share an LEI are named. Countries, companies and fields come from the run.

Protocol field IDs that cover several data points (imports must give `data_point`):
C01, C05, C07, C08, C15, C17, C20, C23, R06, R07, R08. `cik` has no protocol ID (decision D13).

## 2. Architecture

```
python -m extractor.datapoints   (a run)      ──► <run>_datapoints.csv
        │ at the end, or python -m extractor.dashboard <csv>
extractor/output_checks.py  (all check rules, one place) ──► <run>_datapoints_checks.md / .csv
        │
extractor/dashboard.py
        ├──► Dashboard/report.json, app/public/report.json ──► Dashboard/app (Angular)
        └──► Dashboard/allshares_report.html (single file)
                     both use Dashboard/core/report-core.js
```

- `extractor/output_checks.py`: the only place check rules live (`docs/output_checks.md`).
- `extractor/dashboard.py`: maps scored values to `report.json` (section 5). No rules.
- `Dashboard/core/report-core.js`: the only place for front-end logic (filters, aggregations, import
  validation and upsert, ranges, metrics). No check rules. Used by the Angular app and inlined in the HTML.
- Front ends render; they do not compute rules.
- Dependencies: Python (the collector's own); vanilla JS for the core and the HTML; Angular (npm) for the
  app only (agreed 4 Nov 2026).
- Charts: the Angular app uses Apache ECharts 6 with the SVG renderer (`app/src/app/chart.ts`, agreed
  4 Nov 2026: use an existing chart library). The single-file HTML keeps the small built-in SVG builders in
  `core/report-charts.js` so it stays self-contained and light. Both follow DESIGN.md section 5.
- UI library: the Angular app uses Bootstrap 5.3 CSS (agreed 4 Nov 2026), CSS only, no Bootstrap JS: navbar
  and underline tabs, `form-select`/`form-control` filters, cards for KPIs and panels, `table table-sm
  table-hover`, `btn` buttons, `alert` callouts, `badge` chips and `breadcrumb` on Validation steps.
  Bootstrap's colours are mapped to the DESIGN.md palette in `app/src/bootstrap-theme.css`. The single-file
  HTML stays on `core/report.css` only, so it has no external dependency.

## 3. Checks

### 3.1 Gates

The checks of `extractor/output_checks.py` (CORE, COD, NUM, DER, XF; the list and which are hard is in
`docs/output_checks.md`). Result per check on a value: PASS or FAIL. A check that doesn't apply, or needs
something the run doesn't have, is n/a: it is not listed for the value and excluded from all counts. The
dashboard can still show NOT RUN (for imported data), but the collector's checks never produce it.

### 3.2 Status per value

1. Any hard FAIL → **Fail (hard)**
2. Else score = passed / applied × 100 → **Pass** ≥ 95, **Review** ≥ 80, else **Fail**.

### 3.3 Value status (protocol style)

- found: value, plus a unit when the protocol field is numeric, plus a period when the field is time-bound
- partial: value present but unit or period missing
- not_found: blank

Static (not time-bound) categories: Identity, Listing and market, Sector, Reporting basis.

### 3.4 Baseline

The run the dashboard showed before a rebuild is the baseline: the KPIs compare with it ("vs previous
run") and the Trend page starts with it, then this run, then each import. On the first build the run is its
own baseline.

### 3.5 Open decisions

Configurable or flagged, never hard-coded as answers (owner Allshares): D01 LTI basis mapping, D02 STI cap
above 100%, D03 pension keywords, D04 segment tolerance, D05 FTE basis, D06 reference ranges, D07
ISO/taxonomy lists, D08 internal source ID, D09 thresholds, D10 total components and tolerance, D11 NUM-11
tolerance, D12 annualisation and performance period, D13 cik without protocol ID, D14 duplicate company IDs.

## 4. Build

`python -m extractor.dashboard <run>_datapoints.csv`, and automatically at the end of every
`python -m extractor.datapoints` run (unless `--no-dashboard`), regenerates:

| Output | Where |
|---|---|
| `report.json` (scored values, gates, reasons, meta, baseline) | `Dashboard/` and `Dashboard/app/public/` |
| `allshares_import_schema.json` and `.js` | `Dashboard/` (the .json also in `app/public/`) |
| `allshares_results_template.csv` | `Dashboard/app/public/` |
| `allshares_report.html` (single file, data and schema inline) | `Dashboard/` |
| `<run>_datapoints_checks.md` and `.csv` (the checks report) | next to the run's CSV |

The schema source is `accuracy/schema/allshares_import_schema.json`. Edit only that file.

## 5. Report data contract (`report.json`)

```
meta:     tracker (the run's CSV name), asOf, built, rows, filled, dataPoints, companyIds, companies, countries[],
          duplicates[], thresholds, target, checksPct, foundPct
gates:    { "CORE-01": [name, "Hard"|"Soft"], ... }
gateIds:  [ ...gate ids, index used in values[].gr ]
reasons:  [ ...distinct reason texts, index used in values[].gr ]
values[]: s source (T the run, I import), c country, o company name, ck company key (LEI, else ID), id company ID,
          g grain, r role row, p 1 if pay data, k category, m module, f field ID, d data point,
          v value, u unit, st value status,
          filled only: pe period end, me method, so source, ep locator URL, nt note (first 300 chars),
          sc score status (P R F H I), sp score, gr [[gateIndex, "P"|"F"|"N", reasonIndex|-1], ...]
baseline: checksPct, foundPct, label (the previous run, or "This run")
```

Pay data = categories Pay policy, Role and disclosure, Pay: fixed, Pay: STI, Pay: LTI, Pay: total.
Company data = everything else.

## 6. Dashboard (Angular app and single-file HTML: same pages, same numbers)

### 6.1 Layout

- Top bar: title, page tabs, values count.
- Filters (sticky, top, apply to every page): Country, Source (all / this run / imported), Data type
  (all / company / pay), Field group (category), Company, Score status.
- KPI strip (sticky): Companies (distinct LEI), Countries, Values in view, Found %, Partial, Not found,
  Checks passing (vs the previous run and the 95% target), Values passing (Pass status), Hard fails,
  Imports applied. Each card has a comparison line.
- Footer: data source, data date, imports applied, values in view, companies and company IDs.

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
   sample only, not Allshares-approved. Percentiles use linear interpolation (Excel PERCENTILE.INC).
9. **Trend**: line chart of checks passing % and found % from the baseline (the previous run), this run, and after
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
- Apply valid rows; Reset restores the run's values and clears the imports from the trend.
- Upsert:
  1. Company: by LEI when the row gives an LEI known in the data, otherwise by company name + country.
  2. Record: field ID + role row + data_point.
  3. Value, unit or status differs → update (score cleared: imported values are not gate-scored);
     identical → unchanged; no match → add.
  4. No data_point and several records match → error (ambiguous), row skipped.
- In-memory only (browser session). No persistence (agreed 4 Nov 2026).

## 8. Labelling rules

- Never invent company values. Examples are illustrative and labelled "Illustrative example".
- Provisional ranges are labelled "Provisional: sample only, Allshares to approve".

## 9. Tests

The tests read the last built run and check the pages against its own data.

| Test | Command |
|---|---|
| report.json from the output checks | `python -m pytest tests/test_dashboard.py` |
| Core logic (filters, import, ranges, metrics, steps) | `node Dashboard/core/report-core.test.js` |
| Single-file HTML in a DOM stub (KPIs, filters, failures attention, import preview/apply/reset, trend, pages) | `node accuracy/tests/report_dom.test.js` |
| Angular app builds and unit tests pass | `npm --prefix Dashboard/app test` |

Angular 21 is used because this machine runs Node 22.20; Angular 22 needs Node 22.22.3 or later.

A browser check by a person is still needed for layout and interaction.
