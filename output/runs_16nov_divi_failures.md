# What the run could not find: runs_16nov_divi.csv

81 missing values in 8 of 8 companies (built 17 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REMUNERATION_REPORT_NOT_FOUND` | Remuneration report not found | 1 | 1 | Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay |
| `DOCUMENT_UNREADABLE` | Document could not be read | 5 | 1 | Scanned or broken file: supply a text PDF, or check the download |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 1 | 1 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 23 | 2 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 51 | 7 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 11 | 7 | - |
| `NOT_COLLECTED` | Not asked for in this run | 124 | 7 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| lti_granted | 9 | NOT_DISCLOSED 7, REMUNERATION_REPORT_NOT_READ 2 |
| pension_contribution | 6 | NOT_DISCLOSED 4, REMUNERATION_REPORT_NOT_READ 2 |
| sti_paid | 5 | REMUNERATION_REPORT_NOT_READ 3, NOT_DISCLOSED 2 |
| lti_vested | 5 | NOT_DISCLOSED 4, REMUNERATION_REPORT_NOT_READ 1 |
| lti_max | 5 | REMUNERATION_REPORT_NOT_READ 3, NOT_DISCLOSED 2 |
| sti_target | 5 | NOT_DISCLOSED 3, REMUNERATION_REPORT_NOT_READ 2 |
| lti_target | 5 | NOT_DISCLOSED 3, REMUNERATION_REPORT_NOT_READ 2 |
| total_remuneration | 4 | NOT_DISCLOSED 2, REMUNERATION_REPORT_NOT_READ 2 |
| pay_currency | 3 | NOT_DISCLOSED 2, REMUNERATION_REPORT_NOT_READ 1 |
| base_salary | 3 | NOT_DISCLOSED 2, REMUNERATION_REPORT_NOT_READ 1 |
| benefits_value | 3 | NOT_DISCLOSED 2, REMUNERATION_REPORT_NOT_READ 1 |
| other_names | 3 | NOT_DISCLOSED 3 |
| staff_by_segment | 3 | NOT_DISCLOSED 3 |
| ticker | 3 | NOT_DISCLOSED 3 |
| aggregate_headcount | 2 | NOT_DISCLOSED 1, REMUNERATION_REPORT_NOT_READ 1 |
| exchange_segment | 2 | NOT_DISCLOSED 2 |
| revenue_by_country | 2 | NOT_DISCLOSED 2 |
| staff_by_country | 2 | NOT_DISCLOSED 2 |
| sti_max | 2 | REMUNERATION_REPORT_NOT_READ 2 |
| ultimate_parent | 1 | NOT_DISCLOSED 1 |
| share_price | 1 | NOT_DISCLOSED 1 |
| market_cap_band | 1 | DERIVATION_INPUT_MISSING 1 |
| fiscal_year | 1 | DOCUMENT_UNREADABLE 1 |
| fiscal_year_end | 1 | DOCUMENT_UNREADABLE 1 |
| pension_type | 1 | DOCUMENT_UNREADABLE 1 |
| benefits | 1 | DOCUMENT_UNREADABLE 1 |
| shareholding_requirement | 1 | DOCUMENT_UNREADABLE 1 |
| role_disclosure | 1 | REMUNERATION_REPORT_NOT_FOUND 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| MERLIN Properties SOCIMI, S.A. (`merlin-properties-socimi-s-a`) | 30 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_vested, other_names, pension_contribution, staff_by_country, staff_by_segment, ticker, ultimate_parent; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| AGFA-GEVAERT (`agfa-gevaert`) | 23 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_vested, pay_currency, pension_contribution, sti_paid, total_remuneration; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested, sti_paid, total_remuneration |
| Iberdrola, S.A. (`iberdrola-s-a`) | 10 | NOT_DISCLOSED: lti_granted, lti_target, pension_contribution, sti_target |
| Domiki Kritis S.A. (`domiki-kritis-s-a`) | 7 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Romande Energie Holding SA (`romande-energie-holding-sa-3dac8f90`) | 6 | DOCUMENT_UNREADABLE: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Laboratorio Reig Jofre, S.A. (`laboratorio-reig-jofre-s-a`) | 2 | NOT_DISCLOSED: exchange_segment, staff_by_segment |
| Logista Integral, S.A. (`logista-integral-s-a`) | 2 | NOT_DISCLOSED: revenue_by_country, ticker |
| Gestamp Automoción, S.A. (`gestamp-automocion-s-a`) | 1 | NOT_DISCLOSED: other_names |
