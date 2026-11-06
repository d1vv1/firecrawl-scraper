# Output checks: nordic_uk_10_datapoints.csv

10 companies, 735 filled values checked (2026-11-05, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 701 (95%) |
| Review | 15 (2%) |
| Fail | 1 (0%) |
| Fail (hard) | 18 (2%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 69 | 69 | 0 | 0 | 0 |
| Listing and market | 60 | 60 | 0 | 0 | 0 |
| Sector | 20 | 19 | 0 | 0 | 1 |
| Reporting basis | 40 | 40 | 0 | 0 | 0 |
| Financials | 47 | 42 | 2 | 0 | 3 |
| Workforce | 17 | 14 | 2 | 0 | 1 |
| Ownership and control | 49 | 47 | 0 | 0 | 2 |
| Segment and geography | 20 | 12 | 2 | 1 | 5 |
| Pay policy | 23 | 23 | 0 | 0 | 0 |
| Role and disclosure | 98 | 98 | 0 | 0 | 0 |
| Pay: fixed | 107 | 106 | 0 | 0 | 1 |
| Pay: STI | 85 | 81 | 3 | 0 | 1 |
| Pay: LTI | 59 | 59 | 0 | 0 | 0 |
| Pay: total | 41 | 31 | 6 | 0 | 4 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 735 | 735 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 319 | 316 | 3 | 416 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 521 | 510 | 11 | 214 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 467 | 462 | 5 | 268 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 735 | 735 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 241 | 241 | 0 | 494 |  |
| COD-02 | Classification scheme named |  | 10 | 10 | 0 | 725 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 23 | 23 | 0 | 712 |  |
| COD-06 | Dates are valid | yes | 16 | 16 | 0 | 719 |  |
| NUM-01 | Money has an ISO 4217 currency | yes | 259 | 259 | 0 | 476 |  |
| NUM-02 | Printed figure and unit recorded |  | 225 | 225 | 0 | 510 |  |
| NUM-04 | Magnitude in a plausible range |  | 294 | 294 | 0 | 441 |  |
| NUM-05 | Counts are whole numbers | yes | 26 | 26 | 0 | 709 |  |
| NUM-06 | Percentages in range | yes | 71 | 71 | 0 | 664 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 8 | 8 | 0 | 727 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 19 | 15 | 4 | 716 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 43 | 43 | 0 | 692 |  |
| NUM-11 | STI paid not above its maximum |  | 28 | 25 | 3 | 707 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 222 | 222 | 0 | 513 |  |
| NUM-13 | FTE not above headcount |  | 8 | 7 | 1 | 727 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 26 | 26 | 0 | 709 |  |
| DER-06 | Derived value shows its formula |  | 50 | 50 | 0 | 685 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 36 | 32 | 4 | 699 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 36 | 26 | 10 | 699 | parts add up to N stated N |

## Fill rate

Company fields: 345 of 410 filled (84%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| staff_by_segment | 1 | 10 |
| cik | 4 | 10 |
| shareholding_requirement | 5 | 10 |
| other_names | 6 | 10 |
| listing_date | 6 | 10 |
| controlling_owner_name | 6 | 10 |
| revenue_by_country | 6 | 10 |
| staff_by_country | 6 | 10 |
| exchange_segment | 7 | 10 |
| pe_stake_5pct | 7 | 10 |
| revenue_by_segment | 7 | 10 |
| headcount | 8 | 10 |
| share_price | 8 | 10 |
| market_cap_band | 8 | 10 |
| largest_holders | 8 | 10 |
| ultimate_parent | 8 | 10 |
| isin | 9 | 10 |
| website | 9 | 10 |
| ebitda | 9 | 10 |
| fte | 9 | 10 |
| pension_type | 9 | 10 |
| benefits | 9 | 10 |
| legal_name | 10 | 10 |
| lei | 10 | 10 |
| business_id | 10 | 10 |
| ticker | 10 | 10 |
| exchange | 10 | 10 |
| listing_status | 10 | 10 |
| country_code | 10 | 10 |
| head_office_city | 10 | 10 |
| sector_code | 10 | 10 |
| sub_sector | 10 | 10 |
| revenue | 10 | 10 |
| total_assets | 10 | 10 |
| fiscal_year | 10 | 10 |
| fiscal_year_end | 10 | 10 |
| reporting_currency | 10 | 10 |
| accounting_basis | 10 | 10 |
| shares_outstanding | 10 | 10 |
| controlling_owner | 10 | 10 |
| ownership_type | 10 | 10 |

Pay fields, over 42 executive roles:

| Field | Filled |
|---|---|
| base_salary | 38 (90%) |
| sti_paid | 35 (83%) |
| sti_target | 22 (52%) |
| sti_max | 28 (67%) |
| lti_vested | 14 (33%) |
| lti_granted | 29 (69%) |
| lti_target | 0 (0%) |
| lti_max | 16 (38%) |
| benefits_value | 32 (76%) |
| pension_contribution | 37 (88%) |
| total_remuneration | 41 (98%) |

## Failed values (19)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| ao-world-plc | fte |  | 2892 | Fail (hard) | CORE-03: quote not in the source text |
| bang-olufsen-as | revenue_by_country |  | China: 364; USA: 271; Denmark: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 1,795,000,000 vs 2,468,000,000 (27.3% apart) |
| bang-olufsen-as | total_remuneration | Executive Vice President, Chie | 10413000 | Fail (hard) | XF-01: parts add up to 11,161,000, more than the stated 10,413,000; XF-02: parts add up to 11,161,000, stated 10,413,000 |
| bang-olufsen-as | total_remuneration | Chief Executive Officer (until | 16061000 | Fail (hard) | XF-01: parts add up to 18,891,000, more than the stated 16,061,000; XF-02: parts add up to 18,891,000, stated 16,061,000 |
| bang-olufsen-as | total_remuneration | Executive Vice President, Chie | 6023000 | Fail (hard) | XF-01: parts add up to 7,487,000, more than the stated 6,023,000; XF-02: parts add up to 7,487,000, stated 6,023,000 |
| equinor-asa | revenue_by_country |  | Algeria: 3662; Angola: 24961;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| equinor-asa | share_price |  | 442.8 | Fail (hard) | CORE-03: quote not in the source text |
| equinor-asa | staff_by_country |  | Norway: 20336; Rest of Europe: | Fail | CORE-04: no period_end; NUM-08: adds up to 23,413 vs 21,231 (10.3% apart) |
| equinor-asa | sub_sector |  | Vi er et internasjonalt energi | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| marimekko-oyj | revenue_by_segment |  | Marimekko business: 189.6 | Fail (hard) | CORE-03: quote not in the source text |
| nokia-oyj | benefits_value | Former President and CEO (unti | 19697 | Fail (hard) | CORE-02: 19697 not in the quote |
| nokia-oyj | total_remuneration | Former President and CEO (unti | 940269 | Fail (hard) | XF-01: parts add up to 979,560, more than the stated 940,269; XF-02: parts add up to 979,560, stated 940,269 |
| novo-nordisk-as | ebitda |  | 149640000000 | Fail (hard) | CORE-03: quote not in the source text |
| novo-nordisk-as | revenue_by_segment |  | Obesity and Diabetes care: 289 | Fail (hard) | CORE-03: quote not in the source text |
| shell-plc | controlling_owner_name |  | Shell RDS Holding B.V. | Fail (hard) | CORE-02: not in the quote: rds holding b |
| shell-plc | ebitda |  | 56135000000 | Fail (hard) | CORE-02: 56135 not in the quote |
| shell-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| volvo-ab | staff_by_country |  | Sweden: 26712; France: 9735; E | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| volvo-ab | sti_max | President and CEO | 100 | Fail (hard) | CORE-03: quote not in the source text |
