# Output checks: nordic_uk_10_datapoints.csv

10 companies, 720 filled values checked (2026-11-04, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 672 (93%) |
| Review | 17 (2%) |
| Fail | 1 (0%) |
| Fail (hard) | 30 (4%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 69 | 69 | 0 | 0 | 0 |
| Listing and market | 51 | 50 | 0 | 0 | 1 |
| Sector | 19 | 16 | 0 | 0 | 3 |
| Reporting basis | 40 | 40 | 0 | 0 | 0 |
| Financials | 47 | 44 | 0 | 0 | 3 |
| Workforce | 15 | 11 | 4 | 0 | 0 |
| Ownership and control | 45 | 38 | 5 | 0 | 2 |
| Segment and geography | 19 | 15 | 0 | 1 | 3 |
| Pay policy | 24 | 24 | 0 | 0 | 0 |
| Role and disclosure | 98 | 94 | 0 | 0 | 4 |
| Pay: fixed | 107 | 103 | 0 | 0 | 4 |
| Pay: STI | 87 | 82 | 2 | 0 | 3 |
| Pay: LTI | 58 | 55 | 0 | 0 | 3 |
| Pay: total | 41 | 31 | 6 | 0 | 4 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 720 | 720 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 318 | 314 | 4 | 402 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 518 | 496 | 22 | 202 | the run did not find the full quote (the note keeps only its start) |
| CORE-04 | Period end present (dated fields only) |  | 461 | 451 | 10 | 259 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 720 | 718 | 2 | 0 | period_end 'N/N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 232 | 232 | 0 | 488 |  |
| COD-02 | Classification scheme named |  | 9 | 9 | 0 | 711 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 23 | 23 | 0 | 697 |  |
| COD-06 | Dates are valid | yes | 16 | 15 | 1 | 704 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 257 | 257 | 0 | 463 |  |
| NUM-02 | Printed figure and unit recorded |  | 224 | 224 | 0 | 496 |  |
| NUM-04 | Magnitude in a plausible range |  | 290 | 290 | 0 | 430 |  |
| NUM-05 | Counts are whole numbers | yes | 26 | 26 | 0 | 694 |  |
| NUM-06 | Percentages in range | yes | 75 | 75 | 0 | 645 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 8 | 8 | 0 | 712 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 18 | 17 | 1 | 702 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 42 | 42 | 0 | 678 |  |
| NUM-11 | STI paid not above its maximum |  | 30 | 27 | 3 | 690 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 220 | 220 | 0 | 500 |  |
| NUM-13 | FTE not above headcount |  | 7 | 6 | 1 | 713 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 26 | 26 | 0 | 694 |  |
| DER-06 | Derived value shows its formula |  | 46 | 46 | 0 | 674 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 36 | 32 | 4 | 684 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 36 | 26 | 10 | 684 | parts add up to N stated N |

## Fill rate

Company fields: 329 of 410 filled (80%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| staff_by_segment | 1 | 10 |
| market_cap_band | 2 | 10 |
| cik | 4 | 10 |
| exchange_segment | 4 | 10 |
| revenue_by_country | 5 | 10 |
| other_names | 6 | 10 |
| listing_date | 6 | 10 |
| controlling_owner_name | 6 | 10 |
| staff_by_country | 6 | 10 |
| shareholding_requirement | 6 | 10 |
| fte | 7 | 10 |
| pe_stake_5pct | 7 | 10 |
| revenue_by_segment | 7 | 10 |
| headcount | 8 | 10 |
| share_price | 8 | 10 |
| largest_holders | 8 | 10 |
| controlling_owner | 8 | 10 |
| ownership_type | 8 | 10 |
| ultimate_parent | 8 | 10 |
| isin | 9 | 10 |
| website | 9 | 10 |
| sector_code | 9 | 10 |
| ebitda | 9 | 10 |
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
| sub_sector | 10 | 10 |
| revenue | 10 | 10 |
| total_assets | 10 | 10 |
| fiscal_year | 10 | 10 |
| fiscal_year_end | 10 | 10 |
| reporting_currency | 10 | 10 |
| accounting_basis | 10 | 10 |
| shares_outstanding | 10 | 10 |

Pay fields, over 42 executive roles:

| Field | Filled |
|---|---|
| base_salary | 38 (90%) |
| sti_paid | 35 (83%) |
| sti_target | 22 (52%) |
| sti_max | 30 (71%) |
| lti_vested | 14 (33%) |
| lti_granted | 28 (67%) |
| lti_target | 0 (0%) |
| lti_max | 16 (38%) |
| benefits_value | 32 (76%) |
| pension_contribution | 37 (88%) |
| total_remuneration | 41 (98%) |

## Failed values (31)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| ao-world-plc | listing_date |  | 2014-03 | Fail (hard) | COD-06: not a year or a date |
| ao-world-plc | sub_sector |  | We operate a responsible, trus | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | base_salary | Executive Vice President, Chie | 3078000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | lti_granted | Executive Vice President, Chie | 1924000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | lti_vested | Executive Vice President, Chie | 85098 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | pension_contribution | Executive Vice President, Chie | 369000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | role_disclosure | Executive Vice President, Chie | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bang-olufsen-as | sti_paid | Executive Vice President, Chie | 3725000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-11: paid 121% of base, maximum 43.75% |
| bang-olufsen-as | total_remuneration | Executive Vice President, Chie | 10413000 | Fail (hard) | XF-01: parts add up to 11,161,000, more than the stated 10,413,000; XF-02: parts add up to 11,161,000, stated 10,413,000 |
| bang-olufsen-as | total_remuneration | Chief Executive Officer (until | 16061000 | Fail (hard) | XF-01: parts add up to 18,891,000, more than the stated 16,061,000; XF-02: parts add up to 18,891,000, stated 16,061,000 |
| bang-olufsen-as | total_remuneration | Executive Vice President, Chie | 6023000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); XF-01: parts add up to 7,487,000, more than the stated 6,023,000; XF-02: parts add up to 7,487,000, stated 6,023,000 |
| equinor-asa | revenue_by_country |  | Algeria: 3662; Angola: 24961;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| equinor-asa | share_price |  | 442.8 | Fail (hard) | CORE-03: quote not in the source text |
| equinor-asa | staff_by_country |  | Norway: 20336; Rest of Europe: | Fail | CORE-04: no period_end; NUM-08: adds up to 23,413 vs 21,231 (10.3% apart) |
| equinor-asa | sub_sector |  | Vi er et internasjonalt energi | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| nokia-oyj | benefits_value | Former President and CEO (unti | 19697 | Fail (hard) | CORE-02: 19697 not in the quote |
| nokia-oyj | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| nokia-oyj | shares_outstanding |  | 5582534000 | Fail (hard) | CORE-03: quote not in the source text |
| nokia-oyj | total_remuneration | Former President and CEO (unti | 940269 | Fail (hard) | XF-01: parts add up to 979,560, more than the stated 940,269; XF-02: parts add up to 979,560, stated 940,269 |
| novo-nordisk-as | role_disclosure | Executives in total | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| shell-plc | controlling_owner_name |  | Shell RDS Holding B.V. | Fail (hard) | CORE-02: not in the quote: rds holding b; CORE-04: no period_end |
| shell-plc | ebitda |  | 56135000000 | Fail (hard) | CORE-02: 56135 not in the quote |
| shell-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| volvo-ab | base_salary | President and CEO | 22868000 | Fail (hard) | CORE-02: 22868 not in the quote |
| volvo-ab | lti_max | Other members of the Group Exe | 80 | Fail (hard) | CORE-03: quote not in the source text |
| volvo-ab | revenue_by_segment |  | Trucks: 319700; Construction E | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| volvo-ab | role_disclosure | Other members of the Group Exe | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| volvo-ab | staff_by_country |  | Sweden: 25020; Western Europe  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| volvo-ab | sti_max | President and CEO | 100 | Fail (hard) | CORE-03: quote not in the source text |
| volvo-ab | sti_max | Other members of the Group Exe | 80 | Fail (hard) | CORE-03: quote not in the source text |
| volvo-ab | sub_sector |  | Volvo Group is one of the worl | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
