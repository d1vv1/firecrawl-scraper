# What the run could not find: rerun_nordics_19nov.csv

38 missing values in 4 of 4 companies (built 19 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REMUNERATION_REPORT_NOT_FOUND` | Remuneration report not found | 1 | 1 | Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay |
| `NO_IDENTIFIER` | Needs an LEI or register number | 1 | 1 | Add `lei` or `business_id` to the input: only an official register gives this field |
| `WRONG_YEAR_REPORT` | Values read from an older report | 2 | 2 | Put the FY report link in `annual_report_url` and re-run with --redo |
| `NETWORK_ERROR` | Network or site error | 4 | 1 | Re-run; if it repeats, supply the document link |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 1 | 1 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 1 | 1 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 28 | 3 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 38 | 3 | - |
| `NOT_COLLECTED` | Not asked for in this run | 76 | 3 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| pension_contribution | 4 | NOT_DISCLOSED 4 |
| fiscal_year | 3 | WRONG_YEAR_REPORT 2, NETWORK_ERROR 1 |
| shareholding_requirement | 3 | NOT_DISCLOSED 2, NETWORK_ERROR 1 |
| pension_type | 2 | NETWORK_ERROR 1, NOT_DISCLOSED 1 |
| benefits | 2 | NETWORK_ERROR 1, NOT_DISCLOSED 1 |
| role_disclosure | 2 | REMUNERATION_REPORT_NOT_FOUND 1, NOT_DISCLOSED 1 |
| staff_by_segment | 2 | NOT_DISCLOSED 2 |
| staff_by_country | 2 | NOT_DISCLOSED 2 |
| sti_paid | 1 | NOT_DISCLOSED 1 |
| sti_target | 1 | NOT_DISCLOSED 1 |
| sti_max | 1 | NOT_DISCLOSED 1 |
| benefits_value | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| revenue_by_segment | 1 | NOT_DISCLOSED 1 |
| revenue_by_country | 1 | NOT_DISCLOSED 1 |
| lei | 1 | NO_IDENTIFIER 1 |
| business_id | 1 | NOT_DISCLOSED 1 |
| isin | 1 | NOT_DISCLOSED 1 |
| exchange_segment | 1 | NOT_DISCLOSED 1 |
| share_price | 1 | NOT_DISCLOSED 1 |
| market_cap_band | 1 | DERIVATION_INPUT_MISSING 1 |
| largest_holders | 1 | NOT_DISCLOSED 1 |
| controlling_owner | 1 | NOT_DISCLOSED 1 |
| controlling_owner_name | 1 | NOT_DISCLOSED 1 |
| ownership_type | 1 | NOT_DISCLOSED 1 |
| pe_stake_5pct | 1 | NOT_DISCLOSED 1 |
| ultimate_parent | 1 | NOT_DISCLOSED 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Paratus Energy (`paratus-energy`) | 18 | NO_IDENTIFIER: lei; NOT_DISCLOSED: benefits, business_id, controlling_owner, controlling_owner_name, exchange_segment, isin, largest_holders, ownership_type, pe_stake_5pct, pension_type, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Sydbank AS (`T0002`) | 10 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: benefits_value |
| Handelsbanken (`handelsbanken`) | 5 | NETWORK_ERROR: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| KDventures AB (`T0174`) | 5 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
