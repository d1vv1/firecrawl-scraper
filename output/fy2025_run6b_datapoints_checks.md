# Output checks: fy2025_run6b_datapoints.csv

9 companies, 186 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 175 (94%) |
| Review | 4 (2%) |
| Fail | 0 (0%) |
| Fail (hard) | 7 (4%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 45 | 45 | 0 | 0 | 0 |
| Listing and market | 27 | 26 | 0 | 0 | 1 |
| Sector | 9 | 9 | 0 | 0 | 0 |
| Reporting basis | 14 | 14 | 0 | 0 | 0 |
| Financials | 5 | 3 | 2 | 0 | 0 |
| Workforce | 4 | 2 | 0 | 0 | 2 |
| Ownership and control | 19 | 19 | 0 | 0 | 0 |
| Segment and geography | 1 | 0 | 1 | 0 | 0 |
| Pay policy | 5 | 5 | 0 | 0 | 0 |
| Role and disclosure | 19 | 18 | 0 | 0 | 1 |
| Pay: fixed | 17 | 14 | 0 | 0 | 3 |
| Pay: STI | 11 | 11 | 0 | 0 | 0 |
| Pay: LTI | 4 | 4 | 0 | 0 | 0 |
| Pay: total | 6 | 5 | 1 | 0 | 0 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 186 | 185 | 1 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 54 | 48 | 6 | 132 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 97 | 97 | 0 | 89 |  |
| CORE-04 | Period end present (dated fields only) |  | 71 | 68 | 3 | 115 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 186 | 186 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 58 | 58 | 0 | 128 |  |
| COD-02 | Classification scheme named |  | 6 | 6 | 0 | 180 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 13 | 13 | 0 | 173 |  |
| COD-06 | Dates are valid | yes | 8 | 8 | 0 | 178 |  |
| NUM-01 | Money has an ISO 4217 currency | yes | 35 | 35 | 0 | 151 |  |
| NUM-02 | Printed figure and unit recorded |  | 34 | 34 | 0 | 152 |  |
| NUM-04 | Magnitude in a plausible range |  | 45 | 43 | 2 | 141 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 9 | 9 | 0 | 177 |  |
| NUM-06 | Percentages in range | yes | 7 | 7 | 0 | 179 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 3 | 3 | 0 | 183 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 1 | 1 | 0 | 185 |  |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 4 | 4 | 0 | 182 |  |
| NUM-11 | STI paid not above its maximum |  | 3 | 3 | 0 | 183 |  |
| NUM-12 | A role's amounts share currency and period |  | 33 | 33 | 0 | 153 |  |
| NUM-13 | FTE not above headcount |  | 1 | 1 | 0 | 185 |  |
| DER-03 | Derived value recalculates | yes | 0 | 0 | 0 | 186 |  |
| DER-06 | Derived value shows its formula |  | 5 | 5 | 0 | 181 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 6 | 6 | 0 | 180 |  |
| XF-02 | Total equals its parts (2%) |  | 6 | 5 | 1 | 180 | parts add up to N stated N |

## Fill rate

Company fields: 129 of 369 filled (35%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| revenue | 0 | 9 |
| ebitda | 0 | 9 |
| revenue_by_segment | 0 | 9 |
| staff_by_segment | 0 | 9 |
| revenue_by_country | 0 | 9 |
| cik | 1 | 9 |
| total_assets | 1 | 9 |
| accounting_basis | 1 | 9 |
| fte | 1 | 9 |
| share_price | 1 | 9 |
| market_cap_band | 1 | 9 |
| staff_by_country | 1 | 9 |
| shareholding_requirement | 1 | 9 |
| controlling_owner_name | 2 | 9 |
| pension_type | 2 | 9 |
| benefits | 2 | 9 |
| exchange_segment | 3 | 9 |
| listing_date | 3 | 9 |
| website | 3 | 9 |
| sub_sector | 3 | 9 |
| headcount | 3 | 9 |
| shares_outstanding | 3 | 9 |
| largest_holders | 3 | 9 |
| controlling_owner | 3 | 9 |
| ownership_type | 3 | 9 |
| pe_stake_5pct | 3 | 9 |
| fiscal_year | 4 | 9 |
| reporting_currency | 4 | 9 |
| isin | 5 | 9 |
| ticker | 5 | 9 |
| exchange | 5 | 9 |
| listing_status | 5 | 9 |
| fiscal_year_end | 5 | 9 |
| ultimate_parent | 5 | 9 |
| other_names | 6 | 9 |
| sector_code | 6 | 9 |
| legal_name | 7 | 9 |
| lei | 7 | 9 |
| business_id | 7 | 9 |
| country_code | 7 | 9 |
| head_office_city | 7 | 9 |

Pay fields, over 7 executive roles:

| Field | Filled |
|---|---|
| base_salary | 6 (86%) |
| sti_paid | 6 (86%) |
| sti_target | 1 (14%) |
| sti_max | 4 (57%) |
| lti_vested | 2 (29%) |
| lti_granted | 2 (29%) |
| lti_target | 0 (0%) |
| lti_max | 0 (0%) |
| benefits_value | 5 (71%) |
| pension_contribution | 6 (86%) |
| total_remuneration | 6 (86%) |

## Failed values (7)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| airtel-mobile-commerce-n-v | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| airtel-mobile-commerce-n-v | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| apg-sga-sa | benefits_value | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| apg-sga-sa | pension_contribution | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| apg-sga-sa | pension_contribution | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| essentra-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
