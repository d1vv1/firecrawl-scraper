# Output checks: fy2025_run6_datapoints.csv

19 companies, 586 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 498 (85%) |
| Review | 46 (8%) |
| Fail | 8 (1%) |
| Fail (hard) | 34 (6%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 107 | 107 | 0 | 0 | 0 |
| Listing and market | 71 | 66 | 0 | 0 | 5 |
| Sector | 21 | 20 | 0 | 0 | 1 |
| Reporting basis | 24 | 24 | 0 | 0 | 0 |
| Financials | 9 | 5 | 3 | 0 | 1 |
| Workforce | 6 | 4 | 2 | 0 | 0 |
| Ownership and control | 30 | 30 | 0 | 0 | 0 |
| Segment and geography | 2 | 0 | 1 | 0 | 1 |
| Pay policy | 21 | 20 | 0 | 0 | 1 |
| Role and disclosure | 88 | 76 | 0 | 8 | 4 |
| Pay: fixed | 70 | 51 | 16 | 0 | 3 |
| Pay: STI | 66 | 45 | 16 | 0 | 5 |
| Pay: LTI | 40 | 29 | 0 | 0 | 11 |
| Pay: total | 31 | 21 | 8 | 0 | 2 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 586 | 586 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 232 | 213 | 19 | 354 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 355 | 345 | 10 | 231 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 281 | 218 | 63 | 305 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 586 | 586 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 209 | 204 | 5 | 377 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 12 | 12 | 0 | 574 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 33 | 33 | 0 | 553 |  |
| COD-06 | Dates are valid | yes | 16 | 15 | 1 | 570 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 150 | 149 | 1 | 436 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 156 | 156 | 0 | 430 |  |
| NUM-04 | Magnitude in a plausible range |  | 169 | 169 | 0 | 417 |  |
| NUM-05 | Counts are whole numbers | yes | 18 | 17 | 1 | 568 | not a whole number |
| NUM-06 | Percentages in range | yes | 30 | 30 | 0 | 556 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 4 | 4 | 0 | 582 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 2 | 1 | 1 | 584 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 24 | 24 | 0 | 562 |  |
| NUM-11 | STI paid not above its maximum |  | 15 | 15 | 0 | 571 |  |
| NUM-12 | A role's amounts share currency and period |  | 146 | 146 | 0 | 440 |  |
| NUM-13 | FTE not above headcount |  | 1 | 1 | 0 | 585 |  |
| DER-03 | Derived value recalculates | yes | 8 | 8 | 0 | 578 |  |
| DER-06 | Derived value shows its formula |  | 22 | 22 | 0 | 564 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 27 | 26 | 1 | 559 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 27 | 26 | 1 | 559 | parts add up to N stated N |

## Fill rate

Company fields: 291 of 779 filled (37%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| ebitda | 0 | 19 |
| accounting_basis | 0 | 19 |
| revenue_by_segment | 0 | 19 |
| revenue_by_country | 0 | 19 |
| cik | 1 | 19 |
| revenue | 1 | 19 |
| total_assets | 1 | 19 |
| fte | 1 | 19 |
| staff_by_segment | 1 | 19 |
| staff_by_country | 1 | 19 |
| share_price | 2 | 19 |
| market_cap_band | 2 | 19 |
| controlling_owner_name | 2 | 19 |
| exchange_segment | 3 | 19 |
| controlling_owner | 3 | 19 |
| ownership_type | 3 | 19 |
| shareholding_requirement | 3 | 19 |
| largest_holders | 4 | 19 |
| pe_stake_5pct | 4 | 19 |
| reporting_currency | 5 | 19 |
| headcount | 5 | 19 |
| shares_outstanding | 5 | 19 |
| listing_date | 6 | 19 |
| sub_sector | 9 | 19 |
| fiscal_year | 9 | 19 |
| pension_type | 9 | 19 |
| benefits | 9 | 19 |
| website | 10 | 19 |
| fiscal_year_end | 10 | 19 |
| other_names | 11 | 19 |
| sector_code | 12 | 19 |
| ultimate_parent | 14 | 19 |
| isin | 15 | 19 |
| ticker | 15 | 19 |
| exchange | 15 | 19 |
| listing_status | 15 | 19 |
| legal_name | 17 | 19 |
| lei | 17 | 19 |
| business_id | 17 | 19 |
| country_code | 17 | 19 |
| head_office_city | 17 | 19 |

Pay fields, over 38 executive roles:

| Field | Filled |
|---|---|
| base_salary | 29 (76%) |
| sti_paid | 29 (76%) |
| sti_target | 14 (37%) |
| sti_max | 23 (61%) |
| lti_vested | 3 (8%) |
| lti_granted | 21 (55%) |
| lti_target | 8 (21%) |
| lti_max | 8 (21%) |
| benefits_value | 12 (32%) |
| pension_contribution | 29 (76%) |
| total_remuneration | 31 (82%) |

## Failed values (42)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| arbonia-ag | base_salary | Other members of Group Managem | 628000 | Fail (hard) | CORE-02: 628 not in the quote |
| arbonia-ag | benefits_value | Other members of Group Managem | 40000 | Fail (hard) | CORE-02: 40 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_granted | Other members of Group Managem | 149000 | Fail (hard) | CORE-02: 149 not in the quote |
| arbonia-ag | pension_contribution | Other members of Group Managem | 147000 | Fail (hard) | CORE-02: 147 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | sti_paid | Other members of Group Managem | 542000 | Fail (hard) | CORE-02: 542 not in the quote |
| arbonia-ag | total_remuneration | Other members of Group Managem | 1507000 | Fail (hard) | CORE-02: 1507 not in the quote |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bell-food-group-ag | aggregate_headcount | Other members of the Group Exe | 8 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bkw-ag | sti_target | CEO | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_target | Group Executive Board | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| bystronic-ag | aggregate_headcount | Executive Committee | 4.1 | Fail (hard) | NUM-05: not a whole number |
| bystronic-ag | lti_target | Executive Committee | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | lti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | Executive Committee | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| melhus-sparebank | exchange |  | Euronext | Fail (hard) | CORE-02: not in the quote: euronext; COD-01: 'Euronext' matches no ISO 10383 exchange |
| melhus-sparebank | isin |  | NO0006001908 | Fail (hard) | CORE-02: not in the quote: no0006001908 |
| melhus-sparebank | lti_granted | Banksjef | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Ass. Banksjef | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Leder PM | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Leder BM | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Leder Forsikring& Marked | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Lederjuridisk | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Kredittsjef | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | lti_granted | Risk Compliance Manager | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| melhus-sparebank | pay_currency | Banksjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Ass. Banksjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder PM | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder BM | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder Forsikring& Marked | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Lederjuridisk | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Kredittsjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Risk Compliance Manager | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pension_type |  | defined contribution, 7 % of p | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| melhus-sparebank | total_assets |  | 15200000000 | Fail (hard) | CORE-02: 15.2 not in the quote; NUM-01: unit '' is not ISO 4217 |
