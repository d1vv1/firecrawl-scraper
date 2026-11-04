# Allshares Part 1 accuracy dashboard

- `SPEC.md`: what the pipeline and dashboard do (the contract). `DESIGN.md`: how the dashboard looks.
- `allshares_report.html`: single-file report. Open it directly or email it; data and code are inline.
- `app/`: the Angular app (same pages and numbers, reads `report.json`).
- `core/`: logic and charts shared by both front ends. Gate rules live only in `../accuracy/engine/scoring.py`.

## Data is not in git

The repository does not commit datasets, so these files are git-ignored and must be supplied or rebuilt:

- Inputs, put in `accuracy/inputs/`: `tracker_first50.csv`, `allshares_field_checks.xlsx`,
  `allshares_reference_ranges.xlsx`, `Allshares_Part1_gate_reference_02Nov.xlsx`,
  `allshares_part1_validation.html`, `allshares_report_v1.html`. `field_register.json` (protocol field
  definitions, no company data) is committed.
- Baseline for `diff_baseline.py`: `accuracy/tests/baseline/v1_targets.json`.
- Built by `python accuracy/build.py`: everything in `accuracy/out/`, `Dashboard/report.json`,
  `Dashboard/allshares_report.html`, `Dashboard/app/public/report.json` and the results template CSV.

## Rebuild everything from the tracker

```bash
python accuracy/build.py
```

Run from the folder that holds `accuracy/` and `Dashboard/`. This rescores the tracker and refreshes `report.json`, the schema files, the single-file
report, `app/public/` and the Excel workbooks in `accuracy/out/`.

## Run the Angular app

```bash
npm --prefix Dashboard/app start
```

Then open http://localhost:4200. For a static build: `npm --prefix Dashboard/app run build`, then serve
`Dashboard/app/dist/allshares-dashboard/browser/` with any web server (opening `index.html` from disk
does not work: browsers block module scripts on file://).

The app needs Node 22.12 or later (Angular 21). Angular 22 needs Node 22.22.3+.

## Tests

```bash
python accuracy/tests/diff_baseline.py
```

```bash
python accuracy/tests/check_field_checks.py
```

```bash
node Dashboard/core/report-core.test.js
```

```bash
node accuracy/tests/report_dom.test.js
```

```bash
npm --prefix Dashboard/app test
```

```bash
powershell -ExecutionPolicy Bypass -File accuracy/tests/excel_recalc.ps1
```
