# Output checks: uk_remaining_datapoints.csv

324 companies, 12116 filled values checked (2026-11-14, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 11488 (95%) |
| Review | 127 (1%) |
| Fail | 5 (0%) |
| Fail (hard) | 496 (4%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 852 | 849 | 0 | 0 | 3 |
| Listing and market | 696 | 672 | 0 | 0 | 24 |
| Sector | 253 | 250 | 0 | 0 | 3 |
| Reporting basis | 895 | 891 | 0 | 0 | 4 |
| Financials | 545 | 508 | 2 | 0 | 35 |
| Workforce | 206 | 168 | 16 | 0 | 22 |
| Ownership and control | 581 | 568 | 0 | 0 | 13 |
| Segment and geography | 198 | 139 | 36 | 5 | 18 |
| Pay policy | 854 | 831 | 0 | 0 | 23 |
| Role and disclosure | 1803 | 1770 | 0 | 0 | 33 |
| Pay: fixed | 1892 | 1782 | 1 | 0 | 109 |
| Pay: STI | 1370 | 1297 | 18 | 0 | 55 |
| Pay: LTI | 1248 | 1136 | 6 | 0 | 106 |
| Pay: total | 723 | 627 | 48 | 0 | 48 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 12116 | 12101 | 15 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 5989 | 5800 | 189 | 6127 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 9116 | 8854 | 262 | 3000 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 7446 | 7426 | 20 | 4670 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 12116 | 12114 | 2 | 0 | period_end 'March N N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 4196 | 4188 | 8 | 7920 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 127 | 127 | 0 | 11989 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 234 | 234 | 0 | 11882 |  |
| COD-06 | Dates are valid | yes | 404 | 391 | 13 | 11712 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 4222 | 4204 | 18 | 7894 | unit 'NIS' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 3970 | 3970 | 0 | 8146 |  |
| NUM-04 | Magnitude in a plausible range |  | 4581 | 4560 | 21 | 7535 | -N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 254 | 254 | 0 | 11862 |  |
| NUM-06 | Percentages in range | yes | 1474 | 1474 | 0 | 10642 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 116 | 116 | 0 | 12000 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 197 | 162 | 35 | 11919 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 662 | 662 | 0 | 11454 |  |
| NUM-11 | STI paid not above its maximum |  | 483 | 465 | 18 | 11633 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 3801 | 3794 | 7 | 8315 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 89 | 82 | 7 | 12027 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 200 | 200 | 0 | 11916 |  |
| DER-06 | Derived value shows its formula |  | 474 | 474 | 0 | 11642 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 647 | 635 | 12 | 11469 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 647 | 587 | 60 | 11469 | parts add up to N stated N |

## Fill rate

Company fields: 5080 of 13284 filled (38%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 14 | 324 |
| staff_by_segment | 22 | 324 |
| staff_by_country | 34 | 324 |
| controlling_owner_name | 59 | 324 |
| market_cap_band | 64 | 324 |
| share_price | 69 | 324 |
| revenue_by_segment | 70 | 324 |
| revenue_by_country | 72 | 324 |
| ultimate_parent | 77 | 324 |
| listing_date | 81 | 324 |
| other_names | 84 | 324 |
| fte | 89 | 324 |
| exchange_segment | 91 | 324 |
| isin | 95 | 324 |
| ownership_type | 107 | 324 |
| controlling_owner | 108 | 324 |
| ticker | 111 | 324 |
| pe_stake_5pct | 114 | 324 |
| revenue | 115 | 324 |
| largest_holders | 116 | 324 |
| ebitda | 117 | 324 |
| headcount | 117 | 324 |
| total_assets | 120 | 324 |
| website | 121 | 324 |
| accounting_basis | 124 | 324 |
| shares_outstanding | 124 | 324 |
| lei | 125 | 324 |
| sub_sector | 126 | 324 |
| reporting_currency | 126 | 324 |
| legal_name | 127 | 324 |
| business_id | 127 | 324 |
| exchange | 127 | 324 |
| listing_status | 127 | 324 |
| country_code | 127 | 324 |
| head_office_city | 127 | 324 |
| sector_code | 127 | 324 |
| shareholding_requirement | 270 | 324 |
| benefits | 285 | 324 |
| pension_type | 299 | 324 |
| fiscal_year | 322 | 324 |
| fiscal_year_end | 323 | 324 |

Pay fields, over 783 executive roles:

| Field | Filled |
|---|---|
| base_salary | 720 (92%) |
| sti_paid | 577 (74%) |
| sti_target | 248 (32%) |
| sti_max | 545 (70%) |
| lti_vested | 416 (53%) |
| lti_granted | 246 (31%) |
| lti_target | 140 (18%) |
| lti_max | 446 (57%) |
| benefits_value | 584 (75%) |
| pension_contribution | 588 (75%) |
| total_remuneration | 723 (92%) |

## Failed values (501)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| discoverie-group-plc-d676c327 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| evoke-plc-5c77d1d2 | lti_granted | CEO | 1351000 | Fail (hard) | CORE-02: 1351 not in the quote |
| evoke-plc-5c77d1d2 | lti_granted | CFO | 752500 | Fail (hard) | CORE-02: 752.5 not in the quote |
| evoke-plc-5c77d1d2 | share_price |  | 0.222 | Fail (hard) | CORE-02: 0.222 not in the quote |
| fairview-international-plc-ae11bf81 | pension_type |  | nil | Fail (hard) | CORE-03: quote not in the source text |
| fairview-international-plc-ae11bf81 | shares_outstanding |  | 556000000 | Fail (hard) | CORE-02: 556000000 not in the quote |
| fdm-group-holdings-plc-5f964aeb | sti_paid | Directors | 75000 | Fail (hard) | CORE-02: 75 not in the quote |
| fdm-group-holdings-plc-5f964aeb | total_remuneration | Highest paid Director | 726000 | Fail (hard) | CORE-02: 726 not in the quote |
| ferrexpo-plc-5653b4e7 | share_price |  | 74.1 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| ferrexpo-plc-5653b4e7 | shares_outstanding |  | 582306328 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| ferrexpo-plc-5653b4e7 | staff_by_country |  | Ukraine: 8542 | Fail | CORE-04: no period_end; NUM-08: adds up to 8,542 vs 7,570 (12.8% apart) |
| fevara-plc-92307031 | ebitda |  | 3497000 | Fail (hard) | CORE-02: 3.497 not in the quote |
| fevara-plc-92307031 | revenue_by_country |  | UK: 35471; USA: 37443; Republi | Fail (hard) | CORE-03: quote not in the source text |
| first-class-metals-plc-ae225da0 | listing_date |  | July 2022 | Fail (hard) | COD-06: not a year or a date |
| first-tin-plc-9086dd77 | headcount |  | 24 | Fail (hard) | CORE-02: 24 not in the quote |
| fisher-james-sons-plc-1d273817 | headcount |  | 1947 | Fail (hard) | CORE-03: quote not in the source text |
| fisher-james-sons-plc-1d273817 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| fisher-james-sons-plc-1d273817 | share_price |  | 375 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| fisher-james-sons-plc-1d273817 | total_remuneration | CEO | 1426000 | Fail (hard) | XF-01: parts add up to 1,694,000, more than the stated 1,426,000; XF-02: parts add up to 1,694,000, stated 1,426,000 |
| fisher-james-sons-plc-1d273817 | total_remuneration | CFO | 886000 | Fail (hard) | XF-01: parts add up to 993,000, more than the stated 886,000; XF-02: parts add up to 993,000, stated 886,000 |
| foxtons-group-plc-1852b951 | base_salary | CFO | 293500 | Fail (hard) | CORE-02: 293500 not in the quote |
| foxtons-group-plc-1852b951 | lti_granted | CEO | 506000 | Fail (hard) | CORE-02: 506000 not in the quote; CORE-03: quote not in the source text |
| foxtons-group-plc-1852b951 | lti_granted | CFO | 225000 | Fail (hard) | CORE-02: 225000 not in the quote |
| foxtons-group-plc-1852b951 | sti_paid | CEO | 87800 | Fail (hard) | CORE-02: 87800 not in the quote; CORE-03: quote not in the source text |
| foxtons-group-plc-1852b951 | sti_paid | CFO | 45900 | Fail (hard) | CORE-02: 45900 not in the quote; CORE-03: quote not in the source text |
| foxtons-group-plc-1852b951 | total_remuneration | CEO | 1062000 | Fail (hard) | CORE-02: 1062000 not in the quote |
| foxtons-group-plc-1852b951 | total_remuneration | CFO | 588000 | Fail (hard) | CORE-02: 588000 not in the quote; XF-02: parts add up to 564,400, stated 588,000 |
| frasers-group-plc-6a13d052 | shareholding_requirement |  | Executive Directors: share pri | Fail (hard) | CORE-03: quote not in the source text |
| frasers-group-plc-6a13d052 | total_remuneration | Chief Operating Officer | 251000 | Fail (hard) | CORE-03: quote not in the source text |
| funding-circle-holdings-plc-5c033007 | base_salary | CFO | 350000 | Fail (hard) | CORE-02: 350000 not in the quote |
| funding-circle-holdings-plc-5c033007 | benefits_value | CEO | 5000 | Fail (hard) | CORE-02: 5000 not in the quote |
| funding-circle-holdings-plc-5c033007 | benefits_value | CFO | 2000 | Fail (hard) | CORE-02: 2000 not in the quote |
| funding-circle-holdings-plc-5c033007 | pension_contribution | CEO | 22000 | Fail (hard) | CORE-02: 22000 not in the quote |
| funding-circle-holdings-plc-5c033007 | pension_contribution | CFO | 17000 | Fail (hard) | CORE-02: 17000 not in the quote |
| funding-circle-holdings-plc-5c033007 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| funding-circle-holdings-plc-5c033007 | sti_paid | CEO | 602000 | Fail (hard) | CORE-02: 602000 not in the quote |
| funding-circle-holdings-plc-5c033007 | sti_paid | CFO | 315000 | Fail (hard) | CORE-02: 315000 not in the quote |
| funding-circle-holdings-plc-5c033007 | total_remuneration | CEO | 1520000 | Fail (hard) | CORE-02: 1520000 not in the quote |
| funding-circle-holdings-plc-5c033007 | total_remuneration | CFO | 684000 | Fail (hard) | CORE-02: 684000 not in the quote |
| galliford-try-holdings-plc-46fc9d1a | sti_target | Chief Executive | 60 | Fail (hard) | CORE-02: 60 not in the quote |
| galliford-try-holdings-plc-46fc9d1a | sti_target | Chief Financial Officer | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| games-workshop-group-plc-0f667d1d | benefits |  | life assurance cover, sharesav | Fail (hard) | CORE-03: quote not in the source text |
| games-workshop-group-plc-0f667d1d | lti_granted | CEO | 2175000 | Fail (hard) | CORE-03: quote not in the source text |
| games-workshop-group-plc-0f667d1d | pension_type |  | defined contribution, up to 8. | Fail (hard) | CORE-03: quote not in the source text |
| games-workshop-group-plc-0f667d1d | shareholding_requirement |  | executive directors are requir | Fail (hard) | CORE-03: quote not in the source text |
| gamma-communications-plc-4deb67ef | benefits |  | participation in the Group’s l | Fail (hard) | CORE-03: quote not in the source text |
| gem-resources-plc-cf7e06ac | headcount |  | 23 | Fail (hard) | CORE-02: 23 not in the quote |
| georgia-capital-plc-298a1d16 | benefits |  | life insurance; health insuran | Fail (hard) | CORE-03: quote not in the source text |
| georgia-capital-plc-298a1d16 | sti_paid | Executive Director | 7960000 | Fail (hard) | CORE-03: quote not in the source text |
| georgina-energy-plc-7639c631 | total_assets |  | 1760635 | Fail (hard) | CORE-03: quote not in the source text |
| grafton-group-plc-79b8acde | listing_date |  | 2013 | Fail (hard) | CORE-02: not in the quote: 2013 |
| grand-vision-media-holdings-plc-aca75f65 | headcount |  | 9 | Fail (hard) | CORE-03: quote not in the source text |
| great-southern-copper-plc-d619eabd | largest_holders |  | Foreign Dimensions Pty Limited | Fail (hard) | CORE-03: quote not in the source text |
| great-southern-copper-plc-d619eabd | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| greggs-plc-5347e6c0 | sti_target | Chief Executive | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| greggs-plc-5347e6c0 | sti_target | Chief Financial Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| gsk-plc-669dcd41 | lti_target | Outgoing CEO (until 31 Decembe | 725 | Fail (hard) | CORE-02: 725 not in the quote |
| gulf-marine-services-plc-f393af40 | accounting_basis |  | UK Law, UK adopted internation | Fail (hard) | CORE-03: quote not in the source text |
| gulf-marine-services-plc-f393af40 | benefits |  | fixed cash and reimbursable al | Fail (hard) | CORE-03: quote not in the source text |
| gulf-marine-services-plc-f393af40 | fte |  | 745 | Fail (hard) | CORE-02: 745 not in the quote |
| gulf-marine-services-plc-f393af40 | pension_type |  | No pension provision | Fail (hard) | CORE-03: quote not in the source text |
| halfords-group-plc-f8d1c722 | lti_vested | Chief Financial Officer | 119055 | Fail (hard) | CORE-02: 119055 not in the quote |
| halfords-group-plc-f8d1c722 | lti_vested | Former Chief Executive Officer | 113086 | Fail (hard) | CORE-02: 113086 not in the quote |
| halfords-group-plc-f8d1c722 | total_remuneration | Chief Financial Officer | 1127523 | Fail (hard) | CORE-02: 1127523 not in the quote |
| hamak-gold-limited-68536373 | fte |  | 6 | Fail (hard) | CORE-03: quote not in the source text |
| hamak-gold-limited-68536373 | headcount |  | 6 | Fail (hard) | CORE-03: quote not in the source text |
| hammerson-plc-f1d49abe | pension_contribution | CEO (from 1 January 2026, CEO  | 10 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| hammerson-plc-f1d49abe | role_disclosure | CFO | individual | Fail (hard) | CORE-01: no endpoint URL |
| hansard-global-plc-f13a5b81 | ticker |  | HSD | Fail (hard) | CORE-02: not in the quote: hsd; CORE-03: quote not in the source text |
| harbour-energy-plc-7a9017f1 | lti_max | CFO | 320 | Fail (hard) | CORE-02: 320 not in the quote |
| harbour-energy-plc-7a9017f1 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| harena-rare-earths-plc-229c562b | controlling_owner |  | institutional | Fail (hard) | CORE-03: quote not in the source text |
| harena-rare-earths-plc-229c562b | controlling_owner_name |  | Vidacos Nominees Limited | Fail (hard) | CORE-03: quote not in the source text |
| harena-rare-earths-plc-229c562b | largest_holders |  | Vidacos Nominees Limited 28.91 | Fail (hard) | CORE-03: quote not in the source text |
| harena-rare-earths-plc-229c562b | ownership_type |  | other | Fail (hard) | CORE-03: quote not in the source text |
| harena-rare-earths-plc-229c562b | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| harworth-group-plc-7d3f06a0 | benefits_value | CFO | 17977 | Fail (hard) | CORE-03: quote not in the source text |
| harworth-group-plc-7d3f06a0 | lti_vested | CFO | 199357 | Fail (hard) | CORE-03: quote not in the source text |
| harworth-group-plc-7d3f06a0 | pension_contribution | CFO | 35203 | Fail (hard) | CORE-03: quote not in the source text |
| hays-plc-7467dcac | base_salary | CEO (from 27 February 2026) | 208000 | Fail (hard) | CORE-03: quote not in the source text |
| hays-plc-7467dcac | base_salary | CEO (until 27 February 2026) | 436000 | Fail (hard) | CORE-03: quote not in the source text |
| hays-plc-7467dcac | base_salary | CFO | 484000 | Fail (hard) | CORE-03: quote not in the source text |
| helical-plc-cefce900 | lti_vested | Chief Executive | 24000 | Fail (hard) | CORE-02: 24 not in the quote |
| helical-plc-cefce900 | lti_vested | Chief Financial Officer | 101000 | Fail (hard) | CORE-02: 101 not in the quote |
| helical-plc-cefce900 | shareholding_requirement |  | Matthew Bonning-Snook: 500% of | Fail (hard) | CORE-03: quote not in the source text |
| hemogenyx-pharmaceuticals-plc-ff627795 | fte |  | 16 | Fail (hard) | CORE-03: quote not in the source text |
| hemogenyx-pharmaceuticals-plc-ff627795 | headcount |  | 16 | Fail (hard) | CORE-03: quote not in the source text |
| hemogenyx-pharmaceuticals-plc-ff627795 | staff_by_segment |  | Research & development: 14; Ad | Fail (hard) | CORE-03: quote not in the source text |
| hidong-estate-plc-cc203b38 | base_salary | Executive Director | 1334 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | ebitda |  | 45144 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | pay_currency | Executive Director | RM | Fail (hard) | COD-01: RM is not ISO 4217 |
| hidong-estate-plc-cc203b38 | reporting_currency |  | RM | Fail (hard) | COD-01: RM is not ISO 4217 |
| hidong-estate-plc-cc203b38 | revenue |  | 417731 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | total_remuneration | Executive Director | 1334 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hilton-food-group-plc-3a56b109 | base_salary | Executive Chair (from 25 Novem | 850000 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | lti_granted | Chief Executive Officer (until | 1912500 | Fail (hard) | CORE-02: 1912500 not in the quote |
| hilton-food-group-plc-3a56b109 | lti_vested | Executive Chair (from 25 Novem | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | lti_vested | Chief Financial Officer | 7000 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | sti_paid | Executive Chair (from 25 Novem | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | sti_paid | Chief Financial Officer | 151000 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | total_remuneration | Executive Chair (from 25 Novem | 850000 | Fail (hard) | CORE-03: quote not in the source text |
| hilton-food-group-plc-3a56b109 | total_remuneration | Chief Financial Officer | 623000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 576,000, stated 623,000 |
| hochschild-mining-plc-4d2379f4 | lti_granted | CEO | 1320000 | Fail (hard) | CORE-02: 1320 not in the quote |
| hochschild-mining-plc-4d2379f4 | sti_target | CEO | 90 | Fail (hard) | CORE-02: 90 not in the quote; CORE-03: quote not in the source text |
| hollywood-bowl-group-plc-cf76bae2 | lti_granted | Chief Executive Officer | 719078 | Fail (hard) | CORE-02: 719.078 not in the quote |
| hollywood-bowl-group-plc-cf76bae2 | lti_granted | Chief Financial Officer | 471277 | Fail (hard) | CORE-02: 471.277 not in the quote |
| hollywood-bowl-group-plc-cf76bae2 | lti_granted | Chief People Officer | 186015 | Fail (hard) | CORE-02: 186.015 not in the quote |
| hollywood-bowl-group-plc-cf76bae2 | lti_vested | Chief Executive Officer | 735400 | Fail (hard) | CORE-02: 735.4 not in the quote |
| hollywood-bowl-group-plc-cf76bae2 | lti_vested | Chief Financial Officer | 482000 | Fail (hard) | CORE-02: 482 not in the quote |
| hollywood-bowl-group-plc-cf76bae2 | lti_vested | Chief People Officer | 190200 | Fail (hard) | CORE-02: 190.2 not in the quote |
| hostelworld-group-plc-162ea308 | listing_date |  | 2015 | Fail (hard) | CORE-02: not in the quote: 2015 |
| hostelworld-group-plc-162ea308 | revenue_by_country |  | Europe: 49.9; Americas: 16.9;  | Fail | CORE-04: no period_end; NUM-08: adds up to 93,800,000 vs 938,000,000 (90.0% apart) |
| hsbc-holdings-plc-4c10f5ba | lti_target | Group CEO (from 2 September 20 | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| hsbc-holdings-plc-4c10f5ba | lti_target | Group CFO (from 1 January 2025 | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| hsbc-holdings-plc-4c10f5ba | lti_target | Five highest paid employees | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| hsbc-holdings-plc-4c10f5ba | lti_target | Senior management | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| hsbc-holdings-plc-4c10f5ba | sti_target | Group CEO (from 2 September 20 | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| hsbc-holdings-plc-4c10f5ba | sti_target | Group CFO (from 1 January 2025 | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| hsbc-holdings-plc-4c10f5ba | sti_target | Five highest paid employees | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| hsbc-holdings-plc-4c10f5ba | sti_target | Senior management | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| hydrogen-utopia-international-plc-51b104d1 | share_price |  | 0.028 | Fail (hard) | CORE-02: 0.028 not in the quote |
| ibstock-plc-81ff3340 | base_salary | CEO | 572786 | Fail (hard) | CORE-02: 572.786 not in the quote |
| ibstock-plc-81ff3340 | base_salary | CFO (until 10 October 2025) | 294527 | Fail (hard) | CORE-02: 294.527 not in the quote |
| ibstock-plc-81ff3340 | benefits_value | CEO | 9078 | Fail (hard) | CORE-02: 9.078 not in the quote |
| ibstock-plc-81ff3340 | benefits_value | CFO (until 10 October 2025) | 1235 | Fail (hard) | CORE-02: 1.235 not in the quote |
| ibstock-plc-81ff3340 | lti_vested | CEO | 37766 | Fail (hard) | CORE-02: 37.766 not in the quote |
| ibstock-plc-81ff3340 | pension_contribution | CEO | 57279 | Fail (hard) | CORE-02: 57.279 not in the quote |
| ibstock-plc-81ff3340 | pension_contribution | CFO (until 10 October 2025) | 29453 | Fail (hard) | CORE-02: 29.453 not in the quote; CORE-03: quote not in the source text |
| ibstock-plc-81ff3340 | sti_paid | CEO | 378203 | Fail (hard) | CORE-02: 378.203 not in the quote |
| ibstock-plc-81ff3340 | total_remuneration | CEO | 1055112 | Fail (hard) | CORE-02: 1055.112 not in the quote |
| ibstock-plc-81ff3340 | total_remuneration | CFO (until 10 October 2025) | 325515 | Fail (hard) | CORE-02: 325.515 not in the quote; CORE-03: quote not in the source text |
| icfg-limited-cfbafea2 | revenue_by_country |  | Mongolia: 61340; Central Asia: | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 66,928,000 vs 72,364,000 (7.5% apart) |
| icfg-limited-cfbafea2 | revenue_by_segment |  | Microfinance: 66928; Other bus | Fail (hard) | CORE-03: quote not in the source text |
| icg-plc-b82eb2fc | revenue_by_segment |  | FMC: 900; IC: 96 | Fail (hard) | CORE-03: quote not in the source text |
| iforex-financial-trading-holdings-ltd-74e42f45 | base_salary | Chief Executive Officer | 840000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | base_salary | Chief Financial Officer | 456000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | benefits_value | Chief Financial Officer | 47035 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pay_currency | Chief Executive Officer | NIS | Fail (hard) | COD-01: NIS is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pay_currency | Chief Financial Officer | NIS | Fail (hard) | COD-01: NIS is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pension_contribution | Chief Financial Officer | 67625 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | total_remuneration | Chief Executive Officer | 840000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | total_remuneration | Chief Financial Officer | 570660 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| imaging-biometrics-limited-3542bcb1 | total_assets |  | 1014125 | Fail (hard) | CORE-03: quote not in the source text |
| imc-exploration-group-plc-91b5483e | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: market |
| imi-plc-cbc5827b | benefits_value | Chief Executive Officer | 37000 | Fail (hard) | CORE-02: 37 not in the quote |
| imi-plc-cbc5827b | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| imi-plc-cbc5827b | sti_target | Executive Director (from 1 Aug | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| inchcape-plc-ea221c9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| integrated-diagnostics-holdings-plc-b28b60df | listing_date |  | 2015-05 | Fail (hard) | COD-06: not a year or a date |
| integrated-diagnostics-holdings-plc-b28b60df | revenue_by_country |  | Egypt: 6642; Sudan: 2.3; Jorda | Fail (hard) | CORE-03: quote not in the source text |
| intercontinental-hotels-group-plc-ca6a391f | listing_date |  | April 2003 | Fail (hard) | COD-06: not a year or a date |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_granted | IAG Chief Executive Officer | 4113000000 | Fail (hard) | CORE-02: 4113000 not in the quote; CORE-03: quote not in the source text |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_max | IAG Chief Executive Officer | 450 | Fail (hard) | CORE-03: quote not in the source text |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_target | IAG Chief Executive Officer | 210 | Fail (hard) | CORE-02: 210 not in the quote |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_vested | Management Committee | 23000000 | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | controlling_owner |  | family | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | controlling_owner_name |  | Mark Dixon | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| international-workplace-group-plc-3ae007b6 | lti_granted | Chief Executive Officer | 2151000 | Fail (hard) | CORE-02: 2151 not in the quote; CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | lti_granted | Chief Financial Officer | 1148000 | Fail (hard) | CORE-02: 1148 not in the quote; CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | lti_max | Chief Executive Officer | 300 | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | lti_max | Chief Financial Officer | 300 | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | ownership_type |  | family_owned | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | revenue_by_segment |  | Company-owned: 3212; Managed & | Fail (hard) | CORE-03: quote not in the source text |
| international-workplace-group-plc-3ae007b6 | share_price |  | 2.314 | Fail (hard) | CORE-02: 2.314 not in the quote |
| investec-plc-422fa59c | staff_by_segment |  | Wealth & Investment: 520; Spec | Fail | CORE-04: no period_end; NUM-08: adds up to 7,520 vs 7,949 (5.4% apart) |
| ithaca-energy-plc-c6840a94 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| johnson-service-group-plc-9e93b50d | benefits_value | Former Chief Financial Officer | 14000 | Fail (hard) | CORE-03: quote not in the source text |
| johnson-service-group-plc-9e93b50d | lti_vested | Former Chief Financial Officer | 334000 | Fail (hard) | CORE-03: quote not in the source text |
| kavango-resources-plc-86ebc0c1 | headcount |  | 186 | Fail (hard) | CORE-02: 186 not in the quote |
| kavango-resources-plc-86ebc0c1 | listing_date |  | 2018-07 | Fail (hard) | COD-06: not a year or a date |
| keller-group-plc-85e72b53 | benefits_value | CFO | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| keller-group-plc-85e72b53 | lti_vested | CFO | 1277000 | Fail (hard) | CORE-03: quote not in the source text |
| keller-group-plc-85e72b53 | pension_contribution | CFO | 31000 | Fail (hard) | CORE-03: quote not in the source text |
| keller-group-plc-85e72b53 | sti_paid | CFO | 440000 | Fail (hard) | CORE-03: quote not in the source text |
| kelso-group-holdings-plc-5218b8cc | revenue |  | -542922 | Fail (hard) | CORE-03: quote not in the source text; NUM-04: -542922 outside 0..1e+14 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (J H Goold) | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (J D Brooke) | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (left 30 September 20 | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kenmare-resources-plc-e7d5776b | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| kerry-group-plc-56fe152d | revenue_by_country |  | USA: 2840; Republic of Ireland | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 2,939,400,000 vs 6,757,600,000 (56.5% apart) |
| kingfisher-plc-94bd46d7 | total_remuneration | CEO | 3936600 | Fail (hard) | XF-01: parts add up to 4,053,200, more than the stated 3,936,600; XF-02: parts add up to 4,053,200, stated 3,936,600 |
| kingfisher-plc-94bd46d7 | total_remuneration | CFO | 2394600 | Fail (hard) | XF-01: parts add up to 2,475,200, more than the stated 2,394,600; XF-02: parts add up to 2,475,200, stated 2,394,600 |
| lancashire-holdings-limited-94cc95db | staff_by_country |  | US: 33; Canada: 1; UK: 347; Be | Fail (hard) | CORE-03: quote not in the source text |
| law-debenture-corporation-plc-the-d1b5e75c | listing_date |  | 1889 | Fail (hard) | CORE-02: not in the quote: 1889; COD-06: not a year or a date |
| law-debenture-corporation-plc-the-d1b5e75c | lti_granted | Chief Executive Officer | 657000 | Fail (hard) | CORE-02: 657 not in the quote |
| law-debenture-corporation-plc-the-d1b5e75c | lti_granted | Chief Operating Officer | 453000 | Fail (hard) | CORE-02: 453 not in the quote |
| lion-finance-group-plc-03b7fac3 | lti_max | Executive Director | 200 | Fail (hard) | COD-01: unit '' is not a target form |
| lion-finance-group-plc-03b7fac3 | lti_target | Executive Director | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| london-stock-exchange-group-plc-e057fe1a | benefits_value | Chief Executive Officer | 157000 | Fail (hard) | CORE-02: 157 not in the quote |
| london-stock-exchange-group-plc-e057fe1a | lti_granted | Chief Executive Officer | 7562500 | Fail (hard) | CORE-02: 7562.5 not in the quote |
| london-stock-exchange-group-plc-e057fe1a | lti_granted | Chief Financial Officer | 3400000 | Fail (hard) | CORE-02: 3400 not in the quote |
| london-stock-exchange-group-plc-e057fe1a | shareholding_requirement |  | CEO: 600% of salary; other Exe | Fail (hard) | CORE-03: quote not in the source text |
| marshalls-plc-ba8b711a | lti_vested | Executive Director (Simon Bour | 140000 | Fail (hard) | CORE-02: 140 not in the quote |
| marshalls-plc-ba8b711a | lti_vested | Executive Director (Justin Loc | 142000 | Fail (hard) | CORE-02: 142 not in the quote |
| mcbride-plc-fd766eb4 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| me-group-international-plc-174d99a5 | pension_contribution | Executive Director (from 3 Jun | 6678 | Fail (hard) | CORE-03: quote not in the source text |
| me-group-international-plc-174d99a5 | total_remuneration | Executive Director (from 3 Jun | 87740 | Fail (hard) | CORE-03: quote not in the source text |
| meridian-mining-plc-5760f027 | share_price |  | 0.385 | Fail (hard) | CORE-02: 0.385 not in the quote |
| meridian-mining-plc-5760f027 | total_assets |  | 46120968 | Fail (hard) | CORE-03: quote not in the source text |
| metlen-energy-metals-plc-f17cd684 | controlling_owner_name |  | Evangelos Mytilineos | Fail (hard) | CORE-02: not in the quote: evangelos |
| metro-bank-holdings-plc-3ac1d88a | benefits |  | private healthcare cover, life | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | benefits_value | Chief Executive Officer | 1594 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | benefits_value | Chief Financial Officer | 292 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | lti_vested | Chief Executive Officer | 470382 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | pension_contribution | Chief Executive Officer | 75110 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | pension_contribution | Chief Financial Officer | 53933 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | pension_type |  | defined contribution plan, 8%  | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | shareholding_requirement |  | Executive Directors are requir | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | sti_max | Chief Executive Officer | 150 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | sti_max | Chief Financial Officer | 150 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | sti_paid | Chief Executive Officer | 1177449 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | sti_paid | Chief Financial Officer | 636459 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | total_remuneration | Chief Executive Officer | 2665749 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | total_remuneration | Chief Financial Officer | 1199131 | Fail (hard) | CORE-03: quote not in the source text |
| michael-page-plc-f65a03eb | share_price |  | 2.35 | Fail (hard) | CORE-02: 2.35 not in the quote |
| mila-resources-plc-585b51da | share_price |  | 0.01075 | Fail (hard) | CORE-02: 0.01075 not in the quote |
| mondi-plc-b3f2e211 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| moonpig-group-plc-1a2a5dc2 | base_salary | Former CEO (until December 202 | 424552 | Fail (hard) | CORE-03: quote not in the source text |
| moonpig-group-plc-1a2a5dc2 | benefits_value | Former CEO (until December 202 | 1543 | Fail (hard) | CORE-03: quote not in the source text |
| moonpig-group-plc-1a2a5dc2 | lti_vested | CEO (from March 2026) | 604311 | Fail (hard) | CORE-02: 604311 not in the quote; CORE-03: quote not in the source text |
| moonpig-group-plc-1a2a5dc2 | pension_contribution | Former CEO (until December 202 | 21228 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | base_salary | Former CEO (until 1 July 2025) | 333785 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | benefits_value | Former CEO (until 1 July 2025) | 7447 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | benefits_value | CFO | 14023 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | lti_granted | CFO | 1825 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | lti_vested | Former CEO (until 1 July 2025) | 114064 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | lti_vested | CFO | 68610 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | pension_contribution | Former CEO (until 1 July 2025) | 26703 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | pension_contribution | CFO | 37878 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | total_remuneration | Former CEO (until 1 July 2025) | 767385 | Fail (hard) | CORE-03: quote not in the source text |
| morgan-advanced-materials-plc-58a5cd32 | total_remuneration | CFO | 1000623 | Fail (hard) | CORE-03: quote not in the source text |
| nanoco-group-plc-c86c4088 | benefits |  | life assurance of eight times  | Fail (hard) | CORE-03: quote not in the source text |
| nanoco-group-plc-c86c4088 | fte |  | 42 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 42 above headcount 38 |
| nanoco-group-plc-c86c4088 | lti_vested | Former CEO (until October 2024 | 49000 | Fail (hard) | CORE-03: quote not in the source text |
| nanoco-group-plc-c86c4088 | pension_contribution | Former CEO (until October 2024 | 5000 | Fail (hard) | CORE-03: quote not in the source text |
| nanoco-group-plc-c86c4088 | revenue_by_country |  | South Korea: 6272; Japan: 810; | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 7,558,000 vs 7,018,000 (7.7% apart) |
| national-grid-plc-08987e06 | fte |  | 32391 | Fail (hard) | CORE-03: quote not in the source text |
| natwest-group-plc-0cca2e57 | shareholding_requirement |  | Group CEO – 500% of salary. Gr | Fail (hard) | CORE-03: quote not in the source text |
| ninety-one-plc-23209795 | listing_date |  | March 2020 | Fail (hard) | COD-06: not a year or a date |
| ninety-one-plc-23209795 | lti_granted | Chief Executive Officer | 634000 | Fail (hard) | CORE-03: quote not in the source text |
| ninety-one-plc-23209795 | lti_granted | Finance Director | 508000 | Fail (hard) | CORE-03: quote not in the source text |
| ninety-one-plc-23209795 | staff_by_segment |  | Investments: 281; Client group | Fail (hard) | CORE-03: quote not in the source text |
| ninety-one-plc-23209795 | sti_paid | Chief Executive Officer | 1902000 | Fail (hard) | CORE-03: quote not in the source text |
| ninety-one-plc-23209795 | sti_paid | Finance Director | 1522000 | Fail (hard) | CORE-03: quote not in the source text |
| norcros-plc-c8639b5b | lti_granted | Chief Financial Officer | 366080 | Fail (hard) | CORE-03: quote not in the source text |
| nostrum-oil-gas-plc-2662c1d0 | listing_date |  | March 2008 | Fail (hard) | COD-06: not a year or a date |
| nostrum-oil-gas-plc-2662c1d0 | lti_vested | CEO (until 30 June 2025) | 3357479 | Fail (hard) | CORE-02: 3357479 not in the quote |
| nuformix-plc-98385a38 | share_price |  | 0.09 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBx' is not ISO 4217 |
| nuformix-plc-98385a38 | shares_outstanding |  | 1995709368 | Fail (hard) | CORE-03: quote not in the source text |
| ondo-insurtech-plc-e2c31efb | ebitda |  | -6417000 | Fail (hard) | CORE-02: -6.417 not in the quote; CORE-03: quote not in the source text |
| ondo-insurtech-plc-e2c31efb | revenue |  | 4645000 | Fail (hard) | CORE-03: quote not in the source text |
| osb-group-plc-0972698d | sti_paid | CEO | 678000 | Fail (hard) | CORE-02: 678 not in the quote |
| osb-group-plc-0972698d | sti_paid | CFO | 406000 | Fail (hard) | CORE-02: 406 not in the quote |
| oxford-nanopore-technologies-plc-0e6547be | share_price |  | 1.284 | Fail (hard) | CORE-02: 1.284 not in the quote |
| pan-african-resources-plc-e4db7ca3 | base_salary | Other Prescribed Officers | 719000 | Fail (hard) | CORE-02: 719 not in the quote |
| pan-african-resources-plc-e4db7ca3 | benefits_value | Other Prescribed Officers | 39000 | Fail (hard) | CORE-02: 39 not in the quote |
| pan-african-resources-plc-e4db7ca3 | lti_vested | Other Prescribed Officers | 1201000 | Fail (hard) | CORE-02: 1201 not in the quote |
| pan-african-resources-plc-e4db7ca3 | sti_paid | Other Prescribed Officers | 355000 | Fail (hard) | CORE-02: 355 not in the quote |
| pan-african-resources-plc-e4db7ca3 | total_remuneration | Other Prescribed Officers | 2322000 | Fail (hard) | CORE-02: 2322 not in the quote |
| pennon-group-plc-7143cdb4 | sti_paid | CEO (until 31 December 2025) | 17.5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| pensana-plc-3caf2324 | share_price |  | 122.1 | Fail (hard) | NUM-01: unit 'USD cents' is not ISO 4217 |
| persimmon-plc-03d19fa0 | benefits_value | CFO | 11452 | Fail (hard) | CORE-02: 11452 not in the quote |
| petra-diamonds-limited-5f8d5389 | benefits_value | Former Chief Executive Officer | 47853 | Fail (hard) | CORE-02: 47853 not in the quote; CORE-03: quote not in the source text |
| petra-diamonds-limited-5f8d5389 | benefits_value | Former Chief Financial Officer | 93950 | Fail (hard) | CORE-03: quote not in the source text |
| petra-diamonds-limited-5f8d5389 | lti_vested | Former Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| petra-diamonds-limited-5f8d5389 | lti_vested | Former Chief Financial Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| petra-diamonds-limited-5f8d5389 | pension_contribution | Former Chief Financial Officer | 8089 | Fail (hard) | CORE-03: quote not in the source text |
| petra-diamonds-limited-5f8d5389 | total_remuneration | Former Chief Executive Officer | 347597 | Fail (hard) | CORE-02: 347597 not in the quote |
| playtech-plc-4d633d69 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| plus500-ltd-c1762b4f | benefits_value | CEO | 206000 | Fail (hard) | CORE-02: 206 not in the quote |
| plus500-ltd-c1762b4f | benefits_value | CFO | 206000 | Fail (hard) | CORE-02: 206 not in the quote |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | President & Co-CEO | 17116 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | Co-CEO | 4521 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | CFO | 17835 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | listing_date |  | 2007 | Fail (hard) | CORE-02: not in the quote: 2007 |
| pphe-hotel-group-limited-8368d7b3 | other_names |  | Park Plaza Hotels Limited | Fail (hard) | CORE-02: not in the quote: park plaza limited |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | President & Co-CEO | 29429 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | Co-CEO | 26189 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | CFO | 19313 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | President & Co-CEO | 755119 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | Co-CEO | 890014 | Fail (hard) | CORE-03: quote not in the source text |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | CFO | 871592 | Fail (hard) | CORE-03: quote not in the source text |
| predator-oil-gas-holdings-plc-0ba3277f | share_price |  | 0.00875 | Fail (hard) | CORE-02: 0.875 not in the quote; CORE-03: quote not in the source text |
| princes-group-plc-95096765 | revenue_by_segment |  | Foods: 623181; Fish: 350992; I | Fail (hard) | CORE-03: quote not in the source text |
| procook-group-plc-45a2e6f4 | listing_date |  | 2021-11 | Fail (hard) | COD-06: not a year or a date |
| procook-group-plc-45a2e6f4 | lti_granted | CEO | 412000 | Fail (hard) | CORE-02: 412 not in the quote |
| procook-group-plc-45a2e6f4 | lti_granted | CFO | 278512 | Fail (hard) | CORE-02: 278.512 not in the quote |
| procook-group-plc-45a2e6f4 | staff_by_country |  | UK: 600 | Fail | CORE-04: no period_end; NUM-08: adds up to 600 vs 729 (17.7% apart) |
| prudential-plc-c6ad5538 | benefits_value | Chief Executive Officer | 635000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | lti_vested | Chief Executive Officer | 3581000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | pension_contribution | Chief Executive Officer | 207000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | revenue_by_segment |  | Hong Kong: 2221; Indonesia: 25 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,990,000,000 vs 11,080,000,000 (36.9% apart) |
| prudential-plc-c6ad5538 | sti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| puretech-health-plc-df8e539a | share_price |  | 1.204 | Fail (hard) | CORE-02: 1.204 not in the quote |
| pz-cussons-plc-a434b740 | shareholding_requirement |  | Executive Directors: 200% of s | Fail (hard) | CORE-03: quote not in the source text |
| qinetiq-group-plc-f5a9622e | lti_vested | CFO | 624000 | Fail (hard) | CORE-03: quote not in the source text |
| quantum-data-energy-plc-52f9bd33 | listing_date |  | April 2021 | Fail (hard) | COD-06: not a year or a date |
| r-e-a-holdings-plc-5b9a0020 | fte |  | 8124 | Fail (hard) | CORE-03: quote not in the source text |
| r-e-a-holdings-plc-5b9a0020 | revenue_by_segment |  | Plantations: 193; Stone and sa | Fail (hard) | CORE-03: quote not in the source text |
| r-e-a-holdings-plc-5b9a0020 | staff_by_country |  | Indonesia: 7894; UK: 6 | Fail (hard) | CORE-03: quote not in the source text |
| rank-group-plc-26f67d4c | lti_granted | Chief Financial Officer | 514485 | Fail (hard) | CORE-03: quote not in the source text |
| raspberry-pi-holdings-plc-d0b387d0 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| raspberry-pi-holdings-plc-d0b387d0 | share_price |  | 3.002 | Fail (hard) | CORE-02: 3.002 not in the quote |
| rathbones-group-plc-272d1adc | lti_granted | Group Chief Financial Officer | 873600 | Fail (hard) | CORE-02: 873.6 not in the quote |
| rathbones-group-plc-272d1adc | lti_granted | Group Chief Executive (until 1 | 1236000 | Fail (hard) | CORE-02: 1236 not in the quote |
| rathbones-group-plc-272d1adc | pension_type |  | defined contribution, defined  | Fail (hard) | CORE-03: quote not in the source text |
| rc365-holding-plc-1f4ebdbd | largest_holders |  | LYS Limited 17.3%; Alvar Finan | Fail (hard) | CORE-03: quote not in the source text |
| rc365-holding-plc-1f4ebdbd | listing_date |  | March 2022 | Fail (hard) | COD-06: not a year or a date |
| rc365-holding-plc-1f4ebdbd | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| reach-plc-e8816dd8 | lti_vested | CFO | 177186 | Fail (hard) | CORE-02: 177186 not in the quote |
| record-plc-8e9102d2 | lti_granted | CEO | 4042000 | Fail (hard) | CORE-02: 4042000 not in the quote |
| record-plc-8e9102d2 | lti_granted | Executive Director (until 31 M | 2204000 | Fail (hard) | CORE-02: 2204000 not in the quote |
| record-plc-8e9102d2 | lti_granted | Executive Director (from 1 Jul | 1654000 | Fail (hard) | CORE-02: 1654000 not in the quote |
| relx-plc-28248427 | sti_paid | CEO | 2338000 | Fail (hard) | CORE-02: 2338 not in the quote |
| relx-plc-28248427 | sti_paid | CFO | 1472000 | Fail (hard) | CORE-02: 1472 not in the quote |
| renishaw-plc-02f27561 | total_remuneration | Group Finance Director (until  | 268000 | Fail (hard) | XF-01: parts add up to 562,000, more than the stated 268,000; XF-02: parts add up to 562,000, stated 268,000 |
| rentokil-initial-plc-8eff6540 | lti_vested | Former Chief Financial Officer | 436700 | Fail (hard) | CORE-03: quote not in the source text |
| rhi-magnesita-n-v-fb7495f7 | headcount |  | 15913 | Fail (hard) | CORE-03: quote not in the source text |
| rhi-magnesita-n-v-fb7495f7 | lti_granted | CEO | 2494900000 | Fail (hard) | CORE-02: 2494900 not in the quote |
| rhi-magnesita-n-v-fb7495f7 | lti_granted | CFO | 1082700000 | Fail (hard) | CORE-02: 1082700 not in the quote |
| rhi-magnesita-n-v-fb7495f7 | sub_sector |  | RHI Magnesita is a global supp | Fail (hard) | CORE-03: quote not in the source text |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive (from 25 Augus | 1230000 | Fail (hard) | CORE-02: 1230 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive (to 24 August  | 294000 | Fail (hard) | CORE-02: 294 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Financial Officer | 166000 | Fail (hard) | CORE-02: 166 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive, Iron Ore (fro | 73000 | Fail (hard) | CORE-02: 73 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive, Copper | 159000 | Fail (hard) | CORE-02: 159 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive, Minerals (unt | 86000 | Fail (hard) | CORE-02: 86 not in the quote |
| rio-tinto-plc-1ed16286 | benefits_value | Chief Executive, Aluminium | 266000 | Fail (hard) | CORE-02: 266 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive (from 25 Augus | 2971000 | Fail (hard) | CORE-02: 2971 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive (to 24 August  | 4677000 | Fail (hard) | CORE-02: 4677 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Financial Officer | 2889000 | Fail (hard) | CORE-02: 2889 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive, Iron Ore (fro | 412000 | Fail (hard) | CORE-02: 412 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive, Copper | 1417000 | Fail (hard) | CORE-02: 1417 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive, Minerals (unt | 1583000 | Fail (hard) | CORE-02: 1583 not in the quote |
| rio-tinto-plc-1ed16286 | lti_granted | Chief Executive, Aluminium | 1740000 | Fail (hard) | CORE-02: 1740 not in the quote |
| rs-group-plc-9ec766f0 | benefits_value | CFO | 16252000 | Fail (hard) | CORE-03: quote not in the source text |
| rs-group-plc-9ec766f0 | pension_contribution | CFO | 47093000 | Fail (hard) | CORE-03: quote not in the source text |
| rs-group-plc-9ec766f0 | sti_paid | CFO | 417729000 | Fail (hard) | CORE-03: quote not in the source text |
| s-u-plc-d076a510 | lti_vested | Executive Director (Ed Ahrens) | 41248 | Fail (hard) | CORE-02: 41.248 not in the quote |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Anthony Co | individual | Fail (hard) | CORE-03: quote not in the source text |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Graham Coo | individual | Fail (hard) | CORE-03: quote not in the source text |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Jack Coomb | individual | Fail (hard) | CORE-03: quote not in the source text |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Ed Ahrens) | individual | Fail (hard) | CORE-03: quote not in the source text |
| s-u-plc-d076a510 | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| s4-capital-plc-c1328a0a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| safestore-holdings-plc-c17fb612 | base_salary | CEO | 665000 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | benefits_value | CEO | 25000 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | benefits_value | CFO | 25000 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | lti_vested | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | lti_vested | CFO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | pension_contribution | CEO | 27000 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | pension_contribution | CFO | 18000 | Fail (hard) | CORE-03: quote not in the source text |
| safestore-holdings-plc-c17fb612 | sti_paid | CEO | 582000 | Fail (hard) | CORE-03: quote not in the source text |
| saga-plc-3572ddce | lti_granted | Executive Director (previously | 422300 | Fail (hard) | CORE-02: 422300 not in the quote |
| saga-plc-3572ddce | lti_vested | Group Chief Executive Officer  | 615000 | Fail (hard) | CORE-03: quote not in the source text |
| saga-plc-3572ddce | pension_type |  | defined contribution | Fail (hard) | CORE-03: quote not in the source text |
| sainsbury-j-plc-5943ac28 | fte |  | 91000 | Fail (hard) | CORE-03: quote not in the source text |
| sainsbury-j-plc-5943ac28 | headcount |  | 142000 | Fail (hard) | CORE-03: quote not in the source text |
| sainsbury-j-plc-5943ac28 | revenue_by_segment |  | Grocery, general merchandise a | Fail (hard) | CORE-03: quote not in the source text |
| savills-plc-159e730d | sti_target | Group Chief Executive Officer  | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| savills-plc-159e730d | sti_target | Group Chief Financial Officer  | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| sealand-capital-galaxy-limited-126bc181 | fte |  | 4 | Fail (hard) | CORE-03: quote not in the source text |
| sealand-capital-galaxy-limited-126bc181 | headcount |  | 4 | Fail (hard) | CORE-02: 4 not in the quote |
| serco-group-plc-96a15710 | benefits_value | Group Chief Financial Officer | 52599 | Fail (hard) | CORE-03: quote not in the source text |
| serco-group-plc-96a15710 | lti_vested | Group Chief Financial Officer | 1390285 | Fail (hard) | CORE-03: quote not in the source text |
| serco-group-plc-96a15710 | pension_contribution | Group Chief Financial Officer | 40368 | Fail (hard) | CORE-03: quote not in the source text |
| serco-group-plc-96a15710 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| serco-group-plc-96a15710 | sti_paid | Group Chief Financial Officer | 636820 | Fail (hard) | CORE-03: quote not in the source text |
| serco-group-plc-96a15710 | total_remuneration | Group Chief Financial Officer | 2624669 | Fail (hard) | CORE-03: quote not in the source text |
| severfield-plc-598e26e7 | pension_contribution | Chief Executive Officer (from  | 15000000 | Fail (hard) | CORE-02: 15000 not in the quote |
| severfield-plc-598e26e7 | pension_contribution | Former Chief Executive Officer | 8000000 | Fail (hard) | CORE-02: 8000 not in the quote |
| severfield-plc-598e26e7 | pension_contribution | Former Chief Financial Officer | 13000000 | Fail (hard) | CORE-02: 13000 not in the quote |
| severfield-plc-598e26e7 | total_remuneration | Chief Executive Officer (from  | 335000000 | Fail (hard) | CORE-02: 335000 not in the quote; XF-02: parts add up to 15,840,000, stated 335,000,000 |
| severfield-plc-598e26e7 | total_remuneration | Former Chief Executive Officer | 128000 | Fail (hard) | XF-01: parts add up to 8,120,000, more than the stated 128,000; XF-02: parts add up to 8,120,000, stated 128,000 |
| severfield-plc-598e26e7 | total_remuneration | Former Chief Financial Officer | 216000 | Fail (hard) | XF-01: parts add up to 13,203,000, more than the stated 216,000; XF-02: parts add up to 13,203,000, stated 216,000 |
| severn-trent-plc-2f585ef6 | benefits_value | CEO (from 1 January 2026) | 5700 | Fail (hard) | CORE-02: 5.7 not in the quote |
| shaftesbury-capital-plc-1cc22072 | pension_type |  | defined contribution, 17.5 per | Fail (hard) | CORE-03: quote not in the source text |
| shawbrook-group-plc-d45cea57 | revenue_by_country |  | UK: 682.1 | Fail | CORE-04: no period_end; NUM-08: adds up to 682,100,000 vs 1,421,900,000 (52.0% apart) |
| shawbrook-group-plc-d45cea57 | share_price |  | 4.86 | Fail (hard) | CORE-02: 4.86 not in the quote |
| shawbrook-group-plc-d45cea57 | total_remuneration | Chief Executive Officer | 9948000 | Fail (hard) | CORE-02: 9948000 not in the quote |
| sig-plc-36f9635a | pension_contribution | Previous CEO (until 8 July 202 | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| sig-plc-36f9635a | pension_contribution | CFO | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| sig-plc-36f9635a | sti_max | CEO (from 1 October 2025) | 0 | Fail (hard) | COD-01: unit '' is not a target form |
| sirius-real-estate-limited-9190d4f5 | share_price |  | 0.926 | Fail (hard) | CORE-02: 0.926 not in the quote |
| smiths-group-plc-74ee79d4 | benefits_value | CEO | 42000 | Fail (hard) | CORE-03: quote not in the source text |
| smiths-group-plc-74ee79d4 | benefits_value | Chief Financial Officer | 26000 | Fail (hard) | CORE-03: quote not in the source text |
| smiths-group-plc-74ee79d4 | pension_contribution | CEO | 120000 | Fail (hard) | CORE-03: quote not in the source text |
| smiths-group-plc-74ee79d4 | pension_contribution | Chief Financial Officer | 77000 | Fail (hard) | CORE-03: quote not in the source text |
| spire-healthcare-group-plc-ca3dba5b | lti_granted | Chief Executive Officer | 115979 | Fail (hard) | CORE-02: 115.979 not in the quote |
| spire-healthcare-group-plc-ca3dba5b | lti_granted | Chief Financial Officer | 43525 | Fail (hard) | CORE-02: 43.525 not in the quote |
| ssp-group-plc-e4d12504 | benefits |  | private health insurance for t | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | lti_max | Group CEO | 200 | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | lti_max | Deputy CEO (until 30 September | 200 | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Group CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Deputy CEO (until 30 September | individual | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | sti_max | Group CEO | 175 | Fail (hard) | CORE-03: quote not in the source text |
| st-james-s-place-plc-23c228ff | fte |  | 3102 | Fail (hard) | CORE-03: quote not in the source text |
| st-james-s-place-plc-23c228ff | share_price |  | 13.845 | Fail (hard) | CORE-02: 13.845 not in the quote |
| st-james-s-place-plc-23c228ff | sti_paid | Chief Executive Officer | 1702297 | Fail (hard) | CORE-03: quote not in the source text |
| st-james-s-place-plc-23c228ff | sti_paid | Chief Financial Officer | 1028438 | Fail (hard) | CORE-03: quote not in the source text |
| stv-group-plc-8c122da5 | benefits_value | Chief Executive Officer | 25000 | Fail (hard) | CORE-03: quote not in the source text |
| stv-group-plc-8c122da5 | benefits_value | Chief Financial & Operating Of | 25000 | Fail (hard) | CORE-03: quote not in the source text |
| stv-group-plc-8c122da5 | pension_contribution | Chief Executive Officer | 12000 | Fail (hard) | CORE-03: quote not in the source text |
| stv-group-plc-8c122da5 | pension_contribution | Chief Financial & Operating Of | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| stv-group-plc-8c122da5 | total_remuneration | Chief Financial & Operating Of | 391000 | Fail (hard) | CORE-03: quote not in the source text |
| supermarket-income-reit-plc-3dbe8d27 | lti_granted | Chief Financial Officer | 118350 | Fail (hard) | CORE-03: quote not in the source text |
| synthomer-plc-3c60ceb4 | pension_contribution | CEO | 50592 | Fail (hard) | CORE-03: quote not in the source text |
| synthomer-plc-3c60ceb4 | pension_contribution | CFO | 34247 | Fail (hard) | CORE-03: quote not in the source text |
| synthomer-plc-3c60ceb4 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | lti_granted | CEO | 1271900 | Fail (hard) | CORE-02: 1271.9 not in the quote; CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | lti_granted | Executive Director | 704900 | Fail (hard) | CORE-02: 704.9 not in the quote; CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | sti_paid | CEO | 545100 | Fail (hard) | CORE-02: 545.1 not in the quote; CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | sti_paid | Executive Director | 302100 | Fail (hard) | CORE-02: 302.1 not in the quote; CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | total_remuneration | Executive Director | 1609000 | Fail (hard) | CORE-03: quote not in the source text |
| tharisa-plc-f4ea0c2f | headcount |  | 2966 | Fail (hard) | CORE-02: 2966 not in the quote; CORE-03: quote not in the source text |
| tharisa-plc-f4ea0c2f | staff_by_country |  | South Africa: 1993; Zimbabwe:  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 2,699 vs 2,966 (9.0% apart) |
| the-beauty-tech-group-plc-65ff7e12 | listing_date |  | 2025-10 | Fail (hard) | COD-06: not a year or a date |
| the-beauty-tech-group-plc-65ff7e12 | lti_max | Chief Executive Officer | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | lti_max | Chief Financial Officer & Chie | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | sti_max | Chief Financial Officer & Chie | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| the-british-land-company-plc-ff87bb98 | base_salary | CFO | 670000 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | benefits_value | CFO | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | lti_vested | CEO (until 12 January 2026) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | lti_vested | CFO | 403000 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | pension_contribution | CFO | 54000 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | sti_paid | CFO | 702000 | Fail (hard) | CORE-03: quote not in the source text |
| the-british-land-company-plc-ff87bb98 | total_remuneration | CEO (until 12 January 2026) | 1275000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,243,000, stated 1,275,000 |
| the-british-land-company-plc-ff87bb98 | total_remuneration | CFO | 1862000 | Fail (hard) | CORE-03: quote not in the source text |
| the-sage-group-plc-a2e841b0 | base_salary | CEO | 1063750 | Fail (hard) | CORE-03: quote not in the source text |
| the-smarter-web-company-plc-1e8404aa | exchange_segment |  | AQSE Growth Market | Fail (hard) | CORE-02: not in the quote: aqse |
| thg-plc-24b2c5db | sti_target | COO (until 2 January 2025) | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| thg-plc-24b2c5db | total_remuneration | Executive Director and Chief E | 33000 | Fail (hard) | XF-01: parts add up to 34,000, more than the stated 33,000; XF-02: parts add up to 34,000, stated 33,000 |
| topps-tiles-plc-85c83f1d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| town-centre-securities-plc-5107b789 | sub_sector |  | a property investment and deve | Fail (hard) | CORE-03: quote not in the source text |
| travis-perkins-plc-53aadfa6 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| triad-group-plc-f815b4d8 | listing_date |  | 1996-03 | Fail (hard) | COD-06: not a year or a date |
| trifast-plc-3989d139 | benefits_value | Chief Executive Officer | 22000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | benefits_value | Chief Financial Officer | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | pension_contribution | Chief Executive Officer | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | pension_contribution | Chief Financial Officer | 14000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | total_remuneration | Chief Executive Officer | 449000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | total_remuneration | Chief Financial Officer | 304000 | Fail (hard) | CORE-03: quote not in the source text |
| trustpilot-group-plc-f322927b | lti_granted | Executive Director (Adrian Bla | 1127500 | Fail (hard) | CORE-02: 1127.5 not in the quote; NUM-12: currency GBP, the role's other amounts USD |
| trustpilot-group-plc-f322927b | lti_granted | Executive Director (Hanno Damm | 784913 | Fail (hard) | CORE-02: 784.913 not in the quote; NUM-12: currency GBP, the role's other amounts USD |
| upland-resources-limited-813e7dce | exchange |  | OTCQB market | Fail (hard) | COD-01: 'OTCQB market' matches no ISO 10383 exchange |
| upland-resources-limited-813e7dce | listing_date |  | 2015 | Fail (hard) | CORE-02: not in the quote: 2015 |
| vistry-group-plc-016bb23d | base_salary | CEO | 800000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | base_salary | CFO | 516000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | benefits_value | CEO | 101000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | benefits_value | CFO | 35000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | lti_granted | CFO | 425000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| vistry-group-plc-016bb23d | sti_paid | CEO | 1193000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | sti_paid | CFO | 790000 | Fail (hard) | CORE-03: quote not in the source text |
| vistry-group-plc-016bb23d | total_remuneration | CEO | 1994000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 2,094,000, more than the stated 1,994,000; XF-02: parts add up to 2,094,000, stated 1,994,000 |
| vistry-group-plc-016bb23d | total_remuneration | CFO | 1341000 | Fail (hard) | CORE-03: quote not in the source text |
| vp-plc-94ebb5f9 | revenue_by_segment |  | UK: 287088; International: 711 | Fail (hard) | CORE-03: quote not in the source text |
| vp-plc-94ebb5f9 | website |  | vpplc.com | Fail (hard) | CORE-03: quote not in the source text |
| w-a-g-payment-solutions-plc-44f2e7ea | listing_date |  | 2021 | Fail (hard) | CORE-02: not in the quote: 2021 |
| w-a-g-payment-solutions-plc-44f2e7ea | website |  | eurowag.com | Fail (hard) | CORE-03: quote not in the source text |
| watches-of-switzerland-group-plc-cbe5a2bd | base_salary | CEO | 500000 | Fail (hard) | CORE-02: 500 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | base_salary | CFO | 380000 | Fail (hard) | CORE-02: 380 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | benefits_value | CEO | 73793 | Fail (hard) | CORE-02: 73.793 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | benefits_value | CFO | 20237 | Fail (hard) | CORE-02: 20.237 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | lti_granted | CEO | 1000000 | Fail (hard) | CORE-02: 1000 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | lti_granted | CFO | 665000 | Fail (hard) | CORE-02: 665 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | sti_paid | CEO | 750000 | Fail (hard) | CORE-02: 750 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | sti_paid | CFO | 475000 | Fail (hard) | CORE-02: 475 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | total_remuneration | CEO | 1323793 | Fail (hard) | CORE-02: 1323.793 not in the quote |
| watches-of-switzerland-group-plc-cbe5a2bd | total_remuneration | CFO | 875237 | Fail (hard) | CORE-02: 875.237 not in the quote |
| wetherspoon-j-d-plc-f0b40e8d | accounting_basis |  | UK-adopted international accou | Fail (hard) | CORE-03: quote not in the source text |
| wetherspoon-j-d-plc-f0b40e8d | ebitda |  | 203300000 | Fail (hard) | CORE-03: quote not in the source text |
| wetherspoon-j-d-plc-f0b40e8d | pension_type |  | defined contribution, based on | Fail (hard) | CORE-03: quote not in the source text |
| wetherspoon-j-d-plc-f0b40e8d | shares_outstanding |  | 106144586 | Fail (hard) | CORE-03: quote not in the source text |
| wetherspoon-j-d-plc-f0b40e8d | sub_sector |  | Wetherspoon owns and operates  | Fail (hard) | CORE-03: quote not in the source text |
| wizz-air-holdings-plc-fca22f4f | lti_granted | Chief Executive Officer | 2325000 | Fail (hard) | CORE-02: 2325000 not in the quote |
| workspace-group-plc-23f80ffe | benefits_value | Outgoing CEO (1 April 2025 – 1 | 3700 | Fail (hard) | CORE-03: quote not in the source text |
| workspace-group-plc-23f80ffe | lti_vested | Outgoing CFO (1 April 2025 – 3 | 116900 | Fail (hard) | CORE-03: quote not in the source text |
| workspace-group-plc-23f80ffe | pension_contribution | Outgoing CFO (1 April 2025 – 3 | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| workspace-group-plc-23f80ffe | sti_paid | Outgoing CEO (1 April 2025 – 1 | 200400 | Fail (hard) | CORE-03: quote not in the source text |
| workspace-group-plc-23f80ffe | sti_paid | Outgoing CFO (1 April 2025 – 3 | 143300 | Fail (hard) | CORE-03: quote not in the source text |
| xaar-plc-44438ac8 | benefits |  | car allowance, private medical | Fail (hard) | CORE-03: quote not in the source text |
| xaar-plc-44438ac8 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| xp-power-ltd-2507bfe3 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| xps-pensions-group-plc-bf3a20e5 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| young-co-s-brewery-plc-dea1760d | lti_granted | Chief Executive Officer | 768750 | Fail (hard) | CORE-02: 768.75 not in the quote |
| young-co-s-brewery-plc-dea1760d | lti_granted | Chief Financial Officer | 538125 | Fail (hard) | CORE-02: 538.125 not in the quote |
| young-co-s-brewery-plc-dea1760d | lti_granted | Chief People Officer | 302215 | Fail (hard) | CORE-02: 302.215 not in the quote |
| zenith-energy-ltd-4fdd6c5a | ebitda |  | 591000 | Fail (hard) | CORE-02: 591000 not in the quote |
| zenith-energy-ltd-4fdd6c5a | shares_outstanding |  | 100 | Fail (hard) | CORE-02: 100 not in the quote; NUM-04: 100 outside 1000..1e+12 |
| zigup-plc-d5f0480d | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| zigup-plc-d5f0480d | fte |  | 7815 | Fail (hard) | CORE-03: quote not in the source text |
| zigup-plc-d5f0480d | headcount |  | 7600 | Fail (hard) | CORE-03: quote not in the source text |
| zigup-plc-d5f0480d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| zigup-plc-d5f0480d | share_price |  | 3.97 | Fail (hard) | CORE-02: 3.97 not in the quote |
| zoyo-limited-7dac566f | shares_outstanding |  | 55673122 | Fail (hard) | CORE-02: 55673122 not in the quote; CORE-05: period_end 'March 31, 2026' is not a date |
