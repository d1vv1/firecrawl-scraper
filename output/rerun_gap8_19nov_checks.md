# Output checks: rerun_gap8_19nov.csv

8 companies, 344 filled values checked (2026-11-19, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 328 (95%) |
| Review | 6 (2%) |
| Fail | 0 (0%) |
| Fail (hard) | 10 (3%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 29 | 28 | 0 | 0 | 1 |
| Listing and market | 25 | 25 | 0 | 0 | 0 |
| Sector | 8 | 8 | 0 | 0 | 0 |
| Reporting basis | 24 | 24 | 0 | 0 | 0 |
| Financials | 19 | 18 | 0 | 0 | 1 |
| Workforce | 8 | 8 | 0 | 0 | 0 |
| Ownership and control | 18 | 14 | 0 | 0 | 4 |
| Segment and geography | 8 | 6 | 1 | 0 | 1 |
| Pay policy | 15 | 15 | 0 | 0 | 0 |
| Role and disclosure | 54 | 54 | 0 | 0 | 0 |
| Pay: fixed | 57 | 56 | 0 | 0 | 1 |
| Pay: STI | 32 | 30 | 1 | 0 | 1 |
| Pay: LTI | 24 | 24 | 0 | 0 | 0 |
| Pay: total | 23 | 18 | 4 | 0 | 1 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 344 | 344 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 159 | 155 | 4 | 185 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 240 | 234 | 6 | 104 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 211 | 211 | 0 | 133 |  |
| CORE-05 | Type matches (number, date, breakdown) |  | 344 | 344 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 111 | 111 | 0 | 233 |  |
| COD-02 | Classification scheme named |  | 4 | 4 | 0 | 340 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 9 | 9 | 0 | 335 |  |
| COD-06 | Dates are valid | yes | 11 | 11 | 0 | 333 |  |
| NUM-01 | Money has an ISO 4217 currency | yes | 125 | 125 | 0 | 219 |  |
| NUM-02 | Printed figure and unit recorded |  | 113 | 113 | 0 | 231 |  |
| NUM-04 | Magnitude in a plausible range |  | 138 | 138 | 0 | 206 |  |
| NUM-05 | Counts are whole numbers | yes | 9 | 9 | 0 | 335 |  |
| NUM-06 | Percentages in range | yes | 23 | 23 | 0 | 321 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 4 | 4 | 0 | 340 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 8 | 7 | 1 | 336 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 16 | 16 | 0 | 328 |  |
| NUM-11 | STI paid not above its maximum |  | 13 | 12 | 1 | 331 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 110 | 110 | 0 | 234 |  |
| NUM-13 | FTE not above headcount |  | 4 | 4 | 0 | 340 |  |
| DER-03 | Derived value recalculates | yes | 2 | 2 | 0 | 342 |  |
| DER-06 | Derived value shows its formula |  | 13 | 13 | 0 | 331 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 19 | 18 | 1 | 325 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 19 | 14 | 5 | 325 | parts add up to N stated N |

## Fill rate

Company fields: 154 of 328 filled (47%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 1 | 8 |
| controlling_owner_name | 1 | 8 |
| revenue_by_segment | 2 | 8 |
| staff_by_segment | 2 | 8 |
| revenue_by_country | 2 | 8 |
| staff_by_country | 2 | 8 |
| exchange_segment | 3 | 8 |
| listing_date | 3 | 8 |
| share_price | 3 | 8 |
| market_cap_band | 3 | 8 |
| controlling_owner | 3 | 8 |
| ownership_type | 3 | 8 |
| ultimate_parent | 3 | 8 |
| shareholding_requirement | 3 | 8 |
| legal_name | 4 | 8 |
| other_names | 4 | 8 |
| lei | 4 | 8 |
| business_id | 4 | 8 |
| isin | 4 | 8 |
| ticker | 4 | 8 |
| exchange | 4 | 8 |
| listing_status | 4 | 8 |
| country_code | 4 | 8 |
| head_office_city | 4 | 8 |
| website | 4 | 8 |
| sector_code | 4 | 8 |
| sub_sector | 4 | 8 |
| revenue | 4 | 8 |
| total_assets | 4 | 8 |
| ebitda | 4 | 8 |
| reporting_currency | 4 | 8 |
| accounting_basis | 4 | 8 |
| headcount | 4 | 8 |
| fte | 4 | 8 |
| shares_outstanding | 4 | 8 |
| largest_holders | 4 | 8 |
| pe_stake_5pct | 4 | 8 |
| pension_type | 6 | 8 |
| benefits | 6 | 8 |
| fiscal_year | 8 | 8 |
| fiscal_year_end | 8 | 8 |

Pay fields, over 24 executive roles:

| Field | Filled |
|---|---|
| base_salary | 22 (92%) |
| sti_paid | 15 (62%) |
| sti_target | 4 (17%) |
| sti_max | 13 (54%) |
| lti_vested | 11 (46%) |
| lti_granted | 5 (21%) |
| lti_target | 6 (25%) |
| lti_max | 2 (8%) |
| benefits_value | 14 (58%) |
| pension_contribution | 21 (88%) |
| total_remuneration | 23 (96%) |

## Failed values (10)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| T0531 | sti_max | President and CEO | 0.666667 | Fail (hard) | CORE-02: 0.666667 not in the quote; CORE-03: quote not in the source text |
| T0531 | total_remuneration | President and CEO | 702283 | Fail (hard) | XF-01: parts add up to 820,466, more than the stated 702,283; XF-02: parts add up to 820,466, stated 702,283 |
| T0604 | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| T0604 | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| T0604 | staff_by_country |  | Suomi: 4608 | Fail (hard) | CORE-03: quote not in the source text |
| sequana-medical | benefits_value | Chief Executive Officer | 18985 | Fail (hard) | CORE-03: quote not in the source text |
| sequana-medical | other_names |  | Sequana Medical Aktiengesellsc | Fail (hard) | CORE-02: not in the quote: sequana medical |
| shell-plc | controlling_owner_name |  | Shell RDS Holding B.V. | Fail (hard) | CORE-02: not in the quote: rds holding b |
| shell-plc | ebitda |  | 56135000000 | Fail (hard) | CORE-02: 56135 not in the quote |
| shell-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
