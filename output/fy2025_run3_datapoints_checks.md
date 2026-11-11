# Output checks: fy2025_run3_datapoints.csv

9 companies, 503 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 425 (84%) |
| Review | 15 (3%) |
| Fail | 4 (1%) |
| Fail (hard) | 59 (12%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 47 | 46 | 0 | 0 | 1 |
| Listing and market | 44 | 44 | 0 | 0 | 0 |
| Sector | 14 | 14 | 0 | 0 | 0 |
| Reporting basis | 27 | 26 | 0 | 0 | 1 |
| Financials | 33 | 32 | 0 | 0 | 1 |
| Workforce | 12 | 10 | 0 | 0 | 2 |
| Ownership and control | 33 | 32 | 0 | 0 | 1 |
| Segment and geography | 16 | 8 | 3 | 2 | 3 |
| Pay policy | 17 | 14 | 0 | 0 | 3 |
| Role and disclosure | 87 | 74 | 0 | 2 | 11 |
| Pay: fixed | 73 | 51 | 6 | 0 | 16 |
| Pay: STI | 45 | 38 | 2 | 0 | 5 |
| Pay: LTI | 22 | 21 | 0 | 0 | 1 |
| Pay: total | 33 | 15 | 4 | 0 | 14 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 503 | 503 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 232 | 209 | 23 | 271 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 364 | 325 | 39 | 139 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 306 | 293 | 13 | 197 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 503 | 503 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 169 | 169 | 0 | 334 |  |
| COD-02 | Classification scheme named |  | 7 | 7 | 0 | 496 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 14 | 14 | 0 | 489 |  |
| COD-06 | Dates are valid | yes | 13 | 13 | 0 | 490 |  |
| NUM-01 | Money has an ISO 4217 currency | yes | 169 | 169 | 0 | 334 |  |
| NUM-02 | Printed figure and unit recorded |  | 158 | 158 | 0 | 345 |  |
| NUM-04 | Magnitude in a plausible range |  | 195 | 195 | 0 | 308 |  |
| NUM-05 | Counts are whole numbers | yes | 20 | 20 | 0 | 483 |  |
| NUM-06 | Percentages in range | yes | 14 | 14 | 0 | 489 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 6 | 6 | 0 | 497 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 16 | 11 | 5 | 487 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 17 | 17 | 0 | 486 |  |
| NUM-11 | STI paid not above its maximum |  | 4 | 4 | 0 | 499 |  |
| NUM-12 | A role's amounts share currency and period |  | 143 | 143 | 0 | 360 |  |
| NUM-13 | FTE not above headcount |  | 5 | 5 | 0 | 498 |  |
| DER-03 | Derived value recalculates | yes | 6 | 6 | 0 | 497 |  |
| DER-06 | Derived value shows its formula |  | 20 | 20 | 0 | 483 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 22 | 19 | 3 | 481 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 22 | 8 | 14 | 481 | parts add up to N stated N |

## Fill rate

Company fields: 243 of 369 filled (66%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 1 | 9 |
| staff_by_segment | 1 | 9 |
| shareholding_requirement | 3 | 9 |
| controlling_owner_name | 4 | 9 |
| staff_by_country | 4 | 9 |
| other_names | 5 | 9 |
| exchange_segment | 5 | 9 |
| ultimate_parent | 5 | 9 |
| revenue_by_country | 5 | 9 |
| lei | 6 | 9 |
| ticker | 6 | 9 |
| listing_date | 6 | 9 |
| ebitda | 6 | 9 |
| fiscal_year | 6 | 9 |
| headcount | 6 | 9 |
| fte | 6 | 9 |
| share_price | 6 | 9 |
| market_cap_band | 6 | 9 |
| largest_holders | 6 | 9 |
| controlling_owner | 6 | 9 |
| ownership_type | 6 | 9 |
| pe_stake_5pct | 6 | 9 |
| revenue_by_segment | 6 | 9 |
| benefits | 6 | 9 |
| legal_name | 7 | 9 |
| business_id | 7 | 9 |
| isin | 7 | 9 |
| exchange | 7 | 9 |
| listing_status | 7 | 9 |
| country_code | 7 | 9 |
| head_office_city | 7 | 9 |
| website | 7 | 9 |
| sector_code | 7 | 9 |
| sub_sector | 7 | 9 |
| revenue | 7 | 9 |
| total_assets | 7 | 9 |
| fiscal_year_end | 7 | 9 |
| reporting_currency | 7 | 9 |
| accounting_basis | 7 | 9 |
| shares_outstanding | 7 | 9 |
| pension_type | 8 | 9 |

Pay fields, over 37 executive roles:

| Field | Filled |
|---|---|
| base_salary | 24 (65%) |
| sti_paid | 20 (54%) |
| sti_target | 12 (32%) |
| sti_max | 13 (35%) |
| lti_vested | 15 (41%) |
| lti_granted | 2 (5%) |
| lti_target | 2 (5%) |
| lti_max | 3 (8%) |
| benefits_value | 18 (49%) |
| pension_contribution | 31 (84%) |
| total_remuneration | 33 (89%) |

## Failed values (63)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| alvotech-sdb | accounting_basis |  | IFRS as adopted by the Europea | Fail (hard) | CORE-03: quote not in the source text |
| besqab-pref-b | base_salary | VD | 4500000 | Fail (hard) | CORE-02: 4.5 not in the quote |
| besqab-pref-b | controlling_owner_name |  | Aros Bostad | Fail (hard) | CORE-02: not in the quote: aros bostad |
| besqab-pref-b | fte |  | 110 | Fail (hard) | CORE-03: quote not in the source text |
| besqab-pref-b | pension_contribution | VD | 1100000 | Fail (hard) | CORE-02: 1.1 not in the quote |
| besqab-pref-b | pension_contribution | Övriga ledande befattningshava | 2400000 | Fail (hard) | CORE-02: 2.4 not in the quote |
| besqab-pref-b | revenue_by_segment |  | Projektutveckling Ägda hem: 18 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,939,200,000 vs 836,400,000 (131.9% apart) |
| besqab-pref-b | sti_paid | VD | 2100000 | Fail (hard) | CORE-02: 2.1 not in the quote |
| besqab-pref-b | total_remuneration | VD | 7700000 | Fail (hard) | CORE-02: 7.7 not in the quote |
| besqab-pref-b | total_remuneration | Övriga ledande befattningshava | 14400000 | Fail (hard) | CORE-02: 14.4 not in the quote |
| bilfinger-se-o-n | benefits_value | Chairman of the Executive Boar | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | benefits_value | member of the Executive Board, | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | shareholding_requirement |  | Executive Board members are ob | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bilfinger-se-o-n | total_remuneration | member of the Executive Board, | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| commerzbank-ag | base_salary | ehemaliger Vorsitzender (bis 3 | 481000 | Fail (hard) | CORE-02: 481 not in the quote; CORE-03: quote not in the source text |
| commerzbank-ag | benefits_value | Vorsitzende (seit 1. Oktober 2 | 228000 | Fail (hard) | CORE-02: 228 not in the quote; CORE-03: quote not in the source text |
| commerzbank-ag | benefits_value | Chief Operating Officer (seit  | 273000 | Fail (hard) | CORE-02: 273 not in the quote |
| commerzbank-ag | other_names |  | Commerz- und Disconto-Bank; Co | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | pension_contribution | ehemaliger Vorsitzender (bis 3 | 159000 | Fail (hard) | CORE-02: 159 not in the quote; CORE-03: quote not in the source text |
| commerzbank-ag | pension_type |  | Beitragsorientierte Versorgung | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | revenue_by_country |  | Deutschland: 8043; China einsc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | role_disclosure | Vorsitzende (seit 1. Oktober 2 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | stellvertretender Vorsitzender | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Chief Financial Officer (seit  | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Chief Risk Officer (seit 1. Ja | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Chief Operating Officer (seit  | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | staff_by_country |  | Deutschland: 23991; China eins | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 3,511,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | stellvertretender Vorsitzender | 2917000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,453,000, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Group Human Resources & Group  | 2116000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,880,000, stated 2,116,000 |
| commerzbank-ag | total_remuneration | Segment Privat- und Unternehme | 2086000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,904,000, stated 2,086,000 |
| commerzbank-ag | total_remuneration | Chief Financial Officer (seit  | 1896000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,281,000, stated 1,896,000 |
| commerzbank-ag | total_remuneration | Chief Risk Officer (seit 1. Ja | 2113000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,500,000, stated 2,113,000 |
| commerzbank-ag | total_remuneration | Chief Operating Officer (seit  | 2312000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,620,000, stated 2,312,000 |
| commerzbank-ag | total_remuneration | Vorstand | 17494000 | Fail (hard) | XF-01: parts add up to 18,627,000, more than the stated 17,494,000; XF-02: parts add up to 18,627,000, stated 17,494,000 |
| corem-property-d | shares_outstanding |  | 1396281000 | Fail (hard) | CORE-02: 1396281000 not in the quote |
| corem-property-d | sti_paid | Andra ledande befattningshavar | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote |
| corem-property-d | sti_paid | Other senior executives | 900 | Fail (hard) | CORE-02: 900 not in the quote |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Other leading executives | 5 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | Other leading executives | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pension_type |  | VD har en premiebaserad pensio | Fail (hard) | CORE-03: quote not in the source text |
| intea-fastigheter-d | fte |  | 60 | Fail (hard) | CORE-02: 60 not in the quote; CORE-03: quote not in the source text |
| intea-fastigheter-d | pension_contribution | Övriga ledande befattningshava | 1300000 | Fail (hard) | CORE-02: 1.3 not in the quote |
| intea-fastigheter-d | revenue_by_segment |  | project properties: 265 | Fail | CORE-04: no period_end; NUM-08: adds up to 265,000,000 vs 1,561,000,000 (83.0% apart) |
| intea-fastigheter-d | total_remuneration | Verkställande direktör | 3800000 | Fail (hard) | CORE-02: 3.8 not in the quote |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote; CORE-03: quote not in the source text |
| sca-a | base_salary | President and CEO | 11750000 | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | base_salary | Other senior executives | 26168260 | Fail (hard) | CORE-02: 26.16826 not in the quote |
| sca-a | benefits_value | President and CEO | 203597 | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | benefits_value | Other senior executives | 1166613 | Fail (hard) | CORE-02: 1.166613 not in the quote |
| sca-a | lti_vested | President and CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | pension_contribution | President and CEO | 4746299 | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | pension_contribution | Other senior executives | 8196384 | Fail (hard) | CORE-02: 8.196384 not in the quote |
| sca-a | revenue_by_country |  | Sweden: 3850; Germany: 2115; U | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | sti_paid | President and CEO | 1175000 | Fail (hard) | CORE-03: quote not in the source text |
| sca-a | sti_paid | Other senior executives | 4702823 | Fail (hard) | CORE-02: 4.702823 not in the quote |
| sca-a | total_remuneration | Other senior executives | 32037696 | Fail (hard) | CORE-02: 32.037696 not in the quote; XF-01: parts add up to 40,234,080, more than the stated 32,037,696; XF-02: parts add up to 40,234,080, stated 32,037,696 |
