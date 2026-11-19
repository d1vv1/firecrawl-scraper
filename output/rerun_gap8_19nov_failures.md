# What the run could not find: rerun_gap8_19nov.csv

124 missing values in 6 of 7 companies (built 19 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `WRONG_YEAR_REPORT` | Values read from an older report | 1 | 1 | Put the FY report link in `annual_report_url` and re-run with --redo |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 1 | 1 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 22 | 2 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 100 | 5 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 24 | 7 | - |
| `NOT_COLLECTED` | Not asked for in this run | 152 | 6 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| sti_target | 18 | NOT_DISCLOSED 14, REMUNERATION_REPORT_NOT_READ 4 |
| lti_max | 18 | NOT_DISCLOSED 14, REMUNERATION_REPORT_NOT_READ 4 |
| lti_granted | 16 | NOT_DISCLOSED 14, REMUNERATION_REPORT_NOT_READ 2 |
| lti_target | 14 | NOT_DISCLOSED 11, REMUNERATION_REPORT_NOT_READ 3 |
| lti_vested | 12 | NOT_DISCLOSED 9, REMUNERATION_REPORT_NOT_READ 3 |
| sti_max | 9 | NOT_DISCLOSED 8, REMUNERATION_REPORT_NOT_READ 1 |
| benefits_value | 8 | NOT_DISCLOSED 6, REMUNERATION_REPORT_NOT_READ 2 |
| sti_paid | 7 | NOT_DISCLOSED 6, REMUNERATION_REPORT_NOT_READ 1 |
| shareholding_requirement | 3 | NOT_DISCLOSED 3 |
| pension_contribution | 3 | NOT_DISCLOSED 2, REMUNERATION_REPORT_NOT_READ 1 |
| revenue_by_segment | 2 | NOT_DISCLOSED 2 |
| staff_by_segment | 2 | NOT_DISCLOSED 2 |
| staff_by_country | 2 | NOT_DISCLOSED 2 |
| total_remuneration | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| revenue_by_country | 1 | NOT_DISCLOSED 1 |
| exchange_segment | 1 | NOT_DISCLOSED 1 |
| fiscal_year | 1 | WRONG_YEAR_REPORT 1 |
| share_price | 1 | NOT_DISCLOSED 1 |
| market_cap_band | 1 | DERIVATION_INPUT_MISSING 1 |
| controlling_owner | 1 | NOT_DISCLOSED 1 |
| controlling_owner_name | 1 | NOT_DISCLOSED 1 |
| ownership_type | 1 | NOT_DISCLOSED 1 |
| ultimate_parent | 1 | NOT_DISCLOSED 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Atlantic Sapphire ASA (`T0157`) | 52 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| Goodtech ASA (`T0428`) | 30 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, shareholding_requirement, sti_max, sti_target |
| SEQUANA MEDICAL (`sequana-medical`) | 23 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, ownership_type, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ultimate_parent; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_target |
| SRV Group Plc (`T0531`) | 10 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| Cadeler A/S (`T0397`) | 5 | NOT_DISCLOSED: lti_target, lti_vested, shareholding_requirement |
| Lumo Kodit Oyj (`T0609`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
