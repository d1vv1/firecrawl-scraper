# Allshares Part 1 accuracy dashboard

The web view of a collector run: what was found, what is empty, and which checks pass or fail, for
every company, field and value.

- `SPEC.md`: what the dashboard does (the contract). `DESIGN.md`: how it looks.
- `allshares_report.html`: single-file report. Open it directly or email it; data and code are inline.
- `app/`: the Angular app (same pages and numbers, reads `report.json`).
- `core/`: logic and charts shared by both front ends. No check rules here.

## Where the data comes from

The checks are `extractor/output_checks.py`, the same ones as the checks report
(`docs/output_checks.md`). `extractor/dashboard.py` turns a run's scored values into `report.json`
(SPEC section 5) and the single-file report. There is one set of check rules, so the dashboard and the
checks report always agree.

**It updates by itself.** At the end of every data-point run (`python -m extractor.datapoints ...`) the
output checks run and the dashboard is rebuilt from that run's CSV. `--no-dashboard` turns this off. The
run the dashboard showed before becomes the baseline it compares with ("+1.2 pts vs previous run").

To rebuild by hand, for any data-point CSV:

```bash
python -m extractor.dashboard output/nordic_uk_10_datapoints.csv
```

This writes `Dashboard/report.json`, `Dashboard/allshares_report.html`, the import schema files, and the
same into `app/public/`. It also refreshes `<name>_checks.md` and `<name>_checks.csv` next to the CSV.
Built files are git-ignored (the repository holds no datasets).

## Run the Angular app

```bash
npm --prefix Dashboard/app ci        # once
npm --prefix Dashboard/app start
```

Then open http://localhost:4200. After a run finishes, reload the page to see it. For a static build:
`npm --prefix Dashboard/app run build`, then serve `Dashboard/app/dist/allshares-dashboard/browser/` with any
web server (opening `index.html` from disk does not work: browsers block module scripts on file://).

The app needs Node 22.12 or later (Angular 21). Angular 22 needs Node 22.22.3+.

## Tests

The tests read the last built run and check the pages against its own data, so they pass for any run.

```bash
python -m pytest tests/test_dashboard.py
node Dashboard/core/report-core.test.js
node accuracy/tests/report_dom.test.js
npm --prefix Dashboard/app test
```

`npm test` finds no test files when the project path contains brackets, as in `C:\Users\Name(XX)\...`
(a vitest limitation). Run it from a copy of `Dashboard/` at a plain path, such as `C:\dashtest`.

## Other files

- `accuracy/inputs/field_register.json`: protocol field ID, category and module per data point.
- `accuracy/schema/allshares_import_schema.json`: the import format (Import page). It spells the UK
  `UK`; the collector writes ISO `GB`.
- `accuracy/report/template.html`: the single-file report's page.

Rahul's first version scored the client's `tracker_first50.csv` with its own engine
(`accuracy/engine/scoring.py`) and also wrote Excel workbooks. Both were removed on 5 Nov 2026 in favour of
the output checks; they are in git history (commit 4335ac4) if the workbooks are needed again.
