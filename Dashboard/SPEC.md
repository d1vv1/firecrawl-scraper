# Allshares Part 1 accuracy dashboard: specification

Version 1.3, 9 Nov 2026: the Delivery pages (stand-up, throughput, discovery queue, exceptions, pipeline
health) for the FY2025 gap-fill (section 6.4). 1.2, 9 Nov 2026: Reports & sources, Field coverage and Export for Claude pages, the not-found matrix
on Pay vs company, the Values filter, sortable tables and the notes bar (1.1, 5 Nov 2026; 1.0, 4 Nov 2026,
scored the client's tracker with its own engine). Scope: extraction accuracy only (Part 1). Cross-source verification is out of scope.

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
        ├──► Dashboard/allshares_report.html (single file)
        └── extractor/delivery.py adds report.json "delivery" (tracker, all runs, run outputs, inputs/delivery/)
                     both use Dashboard/core/report-core.js
```

- `extractor/output_checks.py`: the only place check rules live (`docs/output_checks.md`).
- `extractor/dashboard.py`: maps scored values to `report.json` (section 5). No rules.
- `Dashboard/core/report-core.js`: the only place for front-end logic (filters, aggregations, import
  validation and upsert, ranges, metrics, source groups, the not-found matrix, field coverage, the export
  for Claude). No check rules. Used by the Angular app and inlined in the HTML.
- `Dashboard/core/report-ui.js`: DOM helpers shared by both front ends: sortable tables and the notes bar.
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
| `delivery` in `report.json` (section 6.4) | rebuilt on every build and on `--rerender` |

The schema source is `accuracy/schema/allshares_import_schema.json`. Edit only that file.

The protocol field list is `accuracy/inputs/fields_list.json`, made from the Company Data and Pay Data sheets
of `allshares_fields_list.xlsx` by `python accuracy/fields_list_from_excel.py <xlsx>`. Re-run it when the
Excel changes.

`python -m extractor.dashboard --rerender` rewrites the HTML (and the field list in `report.json`) from the
`report.json` already built, without scoring again and without moving the baseline: for front-end or
field-list changes only.

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
fieldList[]: sheet ("Company Data" | "Pay Data"), n, d data point, f field ID, k category, g grain, what,
          format, readFrom, method, checks[] (checks applied), note   (from accuracy/inputs/fields_list.json),
          req, sev, fill50, milestone, why   (merged from accuracy/inputs/field_requirements.json)
delivery: see section 6.4 (absent or {error} when the tracker can't be read; the Delivery pages then say so)
```

Pay data = categories Pay policy, Role and disclosure, Pay: fixed, Pay: STI, Pay: LTI, Pay: total.
Company data = everything else.

## 6. Dashboard (Angular app and single-file HTML: same pages, same numbers)

### 6.1 Layout

- Top bar: title, page navigation, values count. Navigation (9 Nov 2026): Overview, then four menu buttons,
  each opening a list of its pages: **Coverage** (Company data, Pay data, Field coverage, Fields, Empty
  fields, Not found), **Companies** (Companies, Reports & sources, Countries, Pay vs company), **Checks**
  (Failures, Validation steps, Ranges, Trend, Metric register), **Delivery** (Stand-up, Throughput, Discovery
  queue, Exceptions, Pipeline health; section 6.4), **Data** (Export for Claude, Import data).
  The button of the open page's group is underlined and names that page. A menu closes when a page is
  chosen, on a click elsewhere or on Escape; arrow keys move through it (`report-ui.js` navMenus).
- Filters (sticky, top, apply to every page): Country, Source (all / this run / imported), Data type
  (all / company / pay), Field group (category), Company, Score status, Values (all / filled = found or
  partial / empty = not found).
- Every table sorts by a click on a column header, again to reverse (numbers largest first, text A to Z,
  blanks last). The sort stays when the rows change. Tables with group rows sort within each group; the
  not-found matrix sorts each level of its tree.
- Notes bar (right edge, every page): free text kept in this browser (localStorage), saved as you type.
  "Add current view" stamps the date, page and filters; Copy, Download .txt, Clear. Included in the export
  for Claude. Not shared and not in the report file.
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
1a. **Reports & sources** (new, 9 Nov 2026): whether each company's annual report and remuneration report
   were found, with links. A value's source group comes from its source name: Remuneration report (any
   source naming a remuneration report or policy), Annual report (annual report, ESEF filing, SEC 20-F /
   10-K, Companies House accounts), Other sources (the rest), as in the Source List sheet of
   `allshares_fields_list.xlsx`. A report counts as found when at least one value in view was read from it.
   KPIs: companies, annual found, remuneration found, both, neither, protocol fields filled (average per
   company). Chart of those counts; table by country. Company table: annual report found, its links,
   remuneration report found, its links, other source links (one link per document, URL fragment dropped,
   with the number of values read from it), protocol fields, fields filled, fields empty, values, found,
   partial, not found, found %, values from each source group, values pass %, checks pass %. Search,
   annual / remuneration found filters, Export CSV. Click a company to open it.
1b. **Company data** and **Pay data** (new, 9 Nov 2026): one page per sheet of the field list. The field
   review (`accuracy/inputs/field_requirements.json`: requirement, severity High / Medium / Low / Never
   used, fill in the 50-company review sample, why, and for pay the 1 Dec milestone In scope / Deferred)
   next to this run: companies with a value, filled %, found %, check pass %, values pass %. Requirement
   classes: Required, Required (conditional: "Required (one of …)", "Required if …"), Optional. KPIs:
   fields, required fields and their average filled %, high severity average filled %, required fields'
   check pass %, high-severity fields under 80% filled, and per milestone (pay) or fields never used
   (company). Chart: required fields by filled % (lowest 15), coloured by severity. Table of averages by
   requirement class, severity and milestone. Field table with search and requirement / severity /
   milestone filters, Export CSV; sorting Severity puts High first. Click a field to open it.
2. **Pay vs company**: status by data type, share of values, by-country table.
2a. **Not found** (moved from Pay vs company, 9 Nov 2026): KPIs (values not found, company and pay data
   not found, companies with something missing), then a matrix with rows data type › field group › field (each level opens and closes; open all /
   close all) and columns Not found, Not found %, Companies missing, Companies with data (companies with at least one value
   found or partial in that row, of the companies the row applies to; added 10 Nov 2026) and one per country. Cells show not
   found of the values that apply (not-applicable values excluded), as a count or a %, shaded by the share
   missing. Click any cell (any level, any country, or the All values row) to list the not-found values
   behind it: company, country, data type, group, field, ID, role, note; click a company to open it.
3. **Countries**: status by country, companies by country, country × data type table.
4. **Fields** (new): one row per data point: field ID, category, rows, found, partial, not found, Pass,
   Review, Incomplete, Fail, Fail (hard), pass %, average score. Stacked bar of score status for the
   12 fields with most failures. Search and sort. Click a field to see every value of that field across
   companies (company, role, value, unit, status, score, reasons) and the companies where it is empty.
4a. **Field coverage** (new, 9 Nov 2026): every field of the protocol field list (`fieldList`, section 5),
   in the Excel's order, grouped by sheet and field group. Per field: values (that apply), found, partial,
   not found, found %, filled % (found + partial), companies with a value, checks run and failed, check
   pass % (PASS / (PASS + FAIL)), values pass % (Pass / scored), average score, checks applied. Group rows
   and KPI cards give the average across fields (each field counts once) of found %, check pass % and
   values pass %, per field group and per sheet; also fields never found and fields always filled. Charts:
   the 15 fields with the lowest found % and the lowest check pass %. Search, sheet filter, group on/off,
   Export CSV. Click a field to open it on the Fields page.
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
10a. **Export for Claude** (new, 9 Nov 2026): the data in the current filters as one Markdown text to paste
    into Claude or upload as a file: a header (run, date, filters, a legend of statuses and source groups),
    then the parts ticked: My notes, Summary KPIs (with reports found), Companies (the Reports & sources
    table, links joined by " | "), Field coverage, Not found by field and country (cells "not found /
    values"), and Values (none / filled / empty / all; compact by default: no URL, note or company ID
    columns, failed checks as IDs only, values cut at 200 characters; optional row limit). Each table is a
    CSV block. Shows the size in characters and tokens (characters / 4) and advises downloading above about
    150,000 tokens. Copy to clipboard, Download .md, Download values CSV (all columns).
11. **Import data**: see section 7.

### 6.4 Delivery (new, 9 Nov 2026)

The daily stand-up view and client update for the FY2025 gap-fill: 1,258 companies remaining on 9 Nov, due
27 Nov at about 125 a day, exceptions accepted by Allshares on 1 Dec. Built by `extractor/delivery.py` from
`accuracy/inputs/delivery.json` (plan, batch windows, required fields, check → failure reason, Firecrawl
balance) and:

| Source | Used for |
|---|---|
| `../Excel_Documents/FY2025_Company_Pipeline_Tracker.xlsx`, Companies sheet | required companies, regional batch (Region), discovery needs, tracker exceptions |
| every `*_datapoints.csv` and `*_datapoints_checks.csv` in `output/` and `../Excel_Documents/OUTPUT/` | extracted values, extraction date, value status, failed checks |
| `output/*.json`, `output/*.error.json` | runs, failed runs, Firecrawl credits, the fiscal year of the report read |
| `accuracy/inputs/delivery/spot_checks.csv` | spot-check sample: company_id, batch, data_point, role_row, reviewer, checked_on, result (pass / fail), reason |
| `accuracy/inputs/delivery/discovery.csv` | company_id, status (open / in progress / found / not available), next_step, owner, updated_on, note |
| `accuracy/inputs/delivery/scheduled_runs.csv` | run_id, batch, scheduled_for, started_at, finished_at, status, companies, credits_used, note |
| `accuracy/inputs/delivery/exceptions.csv` | company_id, category, reason, accepted (yes / no / pending), note |

Companies join on the slug of the company name (`company_id`). Only the Country filter applies to these pages
(their data is per company, not per value).

Stages (each company counts at the furthest stage reached in order): Required (Pipeline Run = required) →
Document found (Find Required = NA) → Extracted (values in a run, or a run status ok / needs_review) →
Required fields 100% (every field in `required_fields` for its run type has a value) → Rules passed (no value
with status Fail or Fail (hard), and no report of an earlier fiscal year) → Spot-checked (its own sampled
values all pass, or, not sampled, its batch sample is at or above the pass line) → Done. Done date = the later
of the extraction date and the spot-check date.

Failure patterns: failed checks map to a reason through `failure_categories` (unmapped: "Wrong currency" when
the reason names a currency or ISO 4217, else "Other rule failure"); "Missing field" also counts required
fields without a value; "Wrong document" counts a report of an earlier fiscal year or a tracker "Wrong
document: replace".

Exceptions: tracker status "FY2025 not published" → No FY2025 report; "Still to find" → Document missing;
"Wrong document: replace" → Wrong document; a run with status not_found → Document missing; a run that read
an earlier year's report → Wrong document; a discovery row marked not available → No FY2025 report;
`exceptions.csv` adds rows and records acceptance.

Pages:
1. **Stand-up**: KPIs (remaining vs plan, done, extracted, working days left and the pace needed, rules pass
   rate, discovery open, exceptions); the status funnel: a table of stages × (all batches, each batch) with
   counts and % of required, the biggest drop per batch marked as the stuck stage; validation pass rate by
   batch against the 95% line, automated rules (values with status Pass of scored values) and the spot-check
   sample (values judged correct of those sampled) side by side; failure patterns: companies affected per
   reason (chart and table), click a reason for the company work list (company, batch, reason, count,
   example), Export CSV.
2. **Throughput**: burn-down of the remaining companies from the baseline date to the deadline: actual,
   plan at the daily target per working day, and the projection at the last three working days' pace;
   a batch table: window, to do, needed per day, expected done by today, done, status (not started, on track
   = done at least 90% of expected, behind by n, complete), so slippage shows from day two of a batch.
3. **Discovery queue**: the companies whose Find Required is not NA: counts by status and by need; table of
   company, country, batch, need, next step, owner (Unassigned when blank), status, updated; search and status
   filter.
4. **Exceptions**: counts by category with accepted / pending; table of company, country, batch, category,
   reason, source, Allshares acceptance; search; Export CSV (the list for the 1 Dec sign-off).
5. **Pipeline health**: KPIs (company runs, failed runs and their share, scheduled runs and missed ones,
   Firecrawl credits used, credits per run, credits needed for the remaining companies, balance when set);
   charts of runs per day (completed, failed) and credits per day; scheduled runs (a run past its time with no
   start and no done status is Missed); failed runs with their error.

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
| Delivery data from the tracker and run outputs | `python -m pytest tests/test_delivery.py` |
| Core logic (filters, import, ranges, metrics, steps, delivery) | `node Dashboard/core/report-core.test.js` |
| Single-file HTML in a DOM stub (KPIs, filters incl. Values, failures attention, reports & sources, not-found matrix, field coverage, export, import preview/apply/reset, trend, pages) | `node accuracy/tests/report_dom.test.js` |
| Angular app builds and unit tests pass | `npm --prefix Dashboard/app test` |

Angular 21 is used because this machine runs Node 22.20; Angular 22 needs Node 22.22.3 or later.

A browser check by a person is still needed for layout and interaction.
