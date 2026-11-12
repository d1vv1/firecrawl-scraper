# Output checks: dach_set1_datapoints.csv

123 companies, 6386 filled values checked (2026-11-12, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 5605 (88%) |
| Review | 222 (3%) |
| Fail | 22 (0%) |
| Fail (hard) | 537 (8%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 479 | 473 | 0 | 0 | 6 |
| Listing and market | 447 | 439 | 0 | 0 | 8 |
| Sector | 137 | 135 | 0 | 0 | 2 |
| Reporting basis | 371 | 369 | 0 | 0 | 2 |
| Financials | 317 | 270 | 23 | 0 | 24 |
| Workforce | 127 | 108 | 4 | 0 | 15 |
| Ownership and control | 352 | 329 | 0 | 0 | 23 |
| Segment and geography | 143 | 77 | 29 | 9 | 28 |
| Pay policy | 174 | 157 | 0 | 0 | 17 |
| Role and disclosure | 968 | 889 | 2 | 13 | 64 |
| Pay: fixed | 940 | 819 | 30 | 0 | 91 |
| Pay: STI | 777 | 680 | 28 | 0 | 69 |
| Pay: LTI | 735 | 611 | 23 | 0 | 101 |
| Pay: total | 419 | 249 | 83 | 0 | 87 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 6386 | 6380 | 6 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 3425 | 3251 | 174 | 2961 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 4744 | 4449 | 295 | 1642 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 4194 | 4030 | 164 | 2192 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 6386 | 6385 | 1 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 2365 | 2351 | 14 | 4021 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 67 | 67 | 0 | 6319 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 156 | 156 | 0 | 6230 |  |
| COD-06 | Dates are valid | yes | 179 | 176 | 3 | 6207 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 2283 | 2281 | 2 | 4103 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 2173 | 2173 | 0 | 4213 |  |
| NUM-04 | Magnitude in a plausible range |  | 2500 | 2493 | 7 | 3886 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 159 | 158 | 1 | 6227 | not a whole number |
| NUM-06 | Percentages in range | yes | 174 | 174 | 0 | 6212 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 52 | 50 | 2 | 6334 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 142 | 109 | 33 | 6244 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 357 | 357 | 0 | 6029 |  |
| NUM-11 | STI paid not above its maximum |  | 60 | 55 | 5 | 6326 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 2031 | 2029 | 2 | 4355 | currency N the role's other amounts EUR |
| NUM-13 | FTE not above headcount |  | 58 | 57 | 1 | 6328 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 14 | 14 | 0 | 6372 |  |
| DER-06 | Derived value shows its formula |  | 160 | 160 | 0 | 6226 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 337 | 269 | 68 | 6049 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 337 | 184 | 153 | 6049 | parts add up to N stated N |

## Fill rate

Company fields: 2547 of 5043 filled (51%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 8 | 123 |
| staff_by_segment | 17 | 123 |
| other_names | 33 | 123 |
| shareholding_requirement | 35 | 123 |
| revenue_by_country | 39 | 123 |
| staff_by_country | 41 | 123 |
| market_cap_band | 46 | 123 |
| revenue_by_segment | 46 | 123 |
| exchange_segment | 47 | 123 |
| share_price | 47 | 123 |
| pe_stake_5pct | 50 | 123 |
| largest_holders | 52 | 123 |
| controlling_owner_name | 52 | 123 |
| fte | 58 | 123 |
| listing_date | 61 | 123 |
| controlling_owner | 64 | 123 |
| ownership_type | 64 | 123 |
| shares_outstanding | 65 | 123 |
| sector_code | 67 | 123 |
| ebitda | 67 | 123 |
| website | 68 | 123 |
| total_assets | 68 | 123 |
| accounting_basis | 68 | 123 |
| headcount | 69 | 123 |
| benefits | 69 | 123 |
| sub_sector | 70 | 123 |
| revenue | 70 | 123 |
| reporting_currency | 70 | 123 |
| ultimate_parent | 70 | 123 |
| pension_type | 70 | 123 |
| ticker | 71 | 123 |
| legal_name | 74 | 123 |
| lei | 74 | 123 |
| business_id | 74 | 123 |
| isin | 74 | 123 |
| exchange | 74 | 123 |
| listing_status | 74 | 123 |
| country_code | 74 | 123 |
| head_office_city | 74 | 123 |
| fiscal_year | 115 | 123 |
| fiscal_year_end | 118 | 123 |

Pay fields, over 442 executive roles:

| Field | Filled |
|---|---|
| base_salary | 343 (78%) |
| sti_paid | 316 (71%) |
| sti_target | 205 (46%) |
| sti_max | 256 (58%) |
| lti_vested | 202 (46%) |
| lti_granted | 155 (35%) |
| lti_target | 175 (40%) |
| lti_max | 203 (46%) |
| benefits_value | 325 (74%) |
| pension_contribution | 272 (62%) |
| total_remuneration | 419 (95%) |

## Failed values (559)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| addiko-bank-ag-167fa5c3 | total_remuneration | CEO | 899204.92 | Fail (hard) | XF-01: parts add up to 1,132,160, more than the stated 899,205; XF-02: parts add up to 1,132,160, stated 899,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CRO | 649204.82 | Fail (hard) | XF-01: parts add up to 731,888, more than the stated 649,205; XF-02: parts add up to 731,888, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CMO/CIO | 649204.82 | Fail (hard) | XF-01: parts add up to 858,865, more than the stated 649,205; XF-02: parts add up to 858,865, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CFO | 549204.92 | Fail (hard) | XF-01: parts add up to 694,802, more than the stated 549,205; XF-02: parts add up to 694,802, stated 549,205 |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| agrana-beteiligungs-ag-60d4466c | revenue_by_segment |  | FBS: 1647834; ACS – Stärke: 98 | Fail (hard) | CORE-03: quote not in the source text |
| amag-austria-metall-ag-9da856cd | share_price |  | 32 | Fail (hard) | CORE-03: quote not in the source text |
| amag-austria-metall-ag-9da856cd | staff_by_country |  | Austria: 1866; Germany: 249 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | controlling_owner_name |  | AOB Invest GmbH | Fail (hard) | CORE-02: not in the quote: aob invest gmbh |
| atoss-software-se | revenue_by_country |  | Germany: 159951899; Austria: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| austriacard-holdings-ag | benefits_value | Executive Vice President Türki | 13810 | Fail (hard) | CORE-02: 13810 not in the quote |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 292,065, more than the stated 278,255; XF-02: parts add up to 292,065, stated 278,255 |
| auto1-group-se-0e2acd91 | revenue_by_country |  | Germany: 1963802; Italy: 11102 | Fail (hard) | CORE-03: quote not in the source text |
| auto1-group-se-0e2acd91 | revenue_by_segment |  | Merchant: 6413599; Retail: 175 | Fail (hard) | CORE-03: quote not in the source text |
| auto1-group-se-0e2acd91 | shares_outstanding |  | 220835000 | Fail (hard) | CORE-03: quote not in the source text |
| bajaj-mobility-ag-8e6bef55 | ebitda |  | 874000000 | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstand Finanzen (CFO) (from  | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | sti_max | Vorstandsvorsitzender (CEO) (u | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_max | Vorstand Commercial (CCO) und  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_max | Vorstand Finanzen (CFO) (from  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstandsvorsitzender (CEO) (u | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstand Commercial (CCO) und  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstand Finanzen (CFO) (from  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Chairman of the Board of Manag | 5784538 | Fail (hard) | XF-01: parts add up to 6,411,795, more than the stated 5,784,538; XF-02: parts add up to 6,411,795, stated 5,784,538 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 2643824 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,425,599, stated 2,643,824 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 3205763 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,879,500, stated 3,205,763 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 1637046 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,509,747, stated 1,637,046 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 2608564 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,390,937, stated 2,608,564 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 3048831 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,792,801, stated 3,048,831 |
| baywa-ag-na-o-n | base_salary | Member of the Board of Managem | 958400 | Fail (hard) | CORE-02: 958400 not in the quote |
| baywa-ag-na-o-n | base_salary | Chief Restructuring Officer (f | 150000 | Fail (hard) | CORE-02: 150000 not in the quote |
| baywa-ag-na-o-n | benefits_value | Member of the Board of Managem | 118700 | Fail (hard) | CORE-02: 118700 not in the quote |
| baywa-ag-na-o-n | lti_vested | Member of the Board of Managem | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| baywa-ag-na-o-n | pension_contribution | Member of the Board of Managem | 118900 | Fail (hard) | CORE-02: 118900 not in the quote |
| baywa-ag-na-o-n | sti_paid | Former Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| baywa-ag-na-o-n | sti_paid | Member of the Board of Managem | 284700 | Fail (hard) | CORE-02: 284700 not in the quote |
| baywa-ag-na-o-n | total_remuneration | Member of the Board of Managem | 3186300 | Fail (hard) | CORE-02: 3186300 not in the quote; XF-02: parts add up to 1,480,700, stated 3,186,300 |
| beiersdorf-ag-o-n | benefits |  | Provision of a company car, st | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands/CFO | 649000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (Grita  | 3355000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (Ramon  | 546000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (bis 30 | 393000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_max | Vorstandsvorsitzender | 8640000 | Fail (hard) | CORE-02: 8640000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Oswald | 4750000 | Fail (hard) | CORE-02: 4750000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CFO | 3850000 | Fail (hard) | CORE-02: 3850000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CHRO | 2550000 | Fail (hard) | CORE-02: 2550000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Grita  | 4766000 | Fail (hard) | CORE-02: 4766000 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Ramon  | 3975000 | Fail (hard) | CORE-02: 3975000 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (bis 30 | 700000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_target | Vorstandsvorsitzender | 4320000 | Fail (hard) | CORE-02: 4320000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Oswald | 2500000 | Fail (hard) | CORE-02: 2500000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands/CFO | 1925000 | Fail (hard) | CORE-02: 1925000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands/CHRO | 1275000 | Fail (hard) | CORE-02: 1275000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Grita  | 2383000 | Fail (hard) | CORE-02: 2383000 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Ramon  | 2050000 | Fail (hard) | CORE-02: 2050000 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (bis 30 | 350000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | sti_max | Mitglied des Vorstands (Grita  | 400000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands (Grita  | 138000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | sti_target | Mitglied des Vorstands (Grita  | 200000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | total_remuneration | Mitglied des Vorstands (Ramon  | 1390000 | Fail (hard) | CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | total_remuneration | Mitglied des Vorstands (bis 30 | 799000 | Fail (hard) | CORE-03: quote not in the source text |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Finanze | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Vertrie | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Technik | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Vorstand (gesamt) | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bilfinger-se-o-n | benefits_value | CEO | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | benefits_value | CFO | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | total_remuneration | CFO | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| biofrontera-ag-na-o-n | lti_target | CFO | 150 | Fail (hard) | CORE-03: quote not in the source text |
| biofrontera-ag-na-o-n | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| biofrontera-ag-na-o-n | shareholding_requirement |  | Vorstandsmitglieder sind zu ei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bks-bank-ag-5e8b8669 | revenue_by_segment |  | Privatkunden: 111406; Firmenku | Fail | CORE-04: no period_end; NUM-08: adds up to 388,487,000 vs 303,636,676 (27.9% apart) |
| bks-bank-ag-5e8b8669 | share_price |  | 18.4 | Fail (hard) | CORE-02: 18.4 not in the quote |
| branicks-group-ag | lti_max | Management Board | 55 | Fail (hard) | COD-01: unit '' is not a target form |
| branicks-group-ag | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | sti_max | Management Board | 35 | Fail (hard) | COD-01: unit '' is not a target form |
| btv-vier-lander-bank-ag-9e06fc63 | aggregate_headcount | Mitglieder des Vorstandes | 5 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied und Vorsitzender des  | 629100 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Mario | 384200 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Dr. M | 356000 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Dr. H | 307700 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied und Vorsitzender des  | 14400 | Fail (hard) | CORE-02: 14.4 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Mario | 10800 | Fail (hard) | CORE-02: 10.8 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Dr. M | 12700 | Fail (hard) | CORE-02: 12.7 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Dr. H | 12400 | Fail (hard) | CORE-02: 12.4 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | controlling_owner_name |  | CABO Beteiligungsgesellschaft  | Fail (hard) | CORE-02: not in the quote: m |
| btv-vier-lander-bank-ag-9e06fc63 | headcount |  | 1888.7 | Fail (hard) | NUM-05: not a whole number |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied und Vorsitzender des  | 170400 | Fail (hard) | CORE-02: 170.4 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Mario | 63000 | Fail (hard) | CORE-02: 63 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Dr. M | 58300 | Fail (hard) | CORE-02: 58.3 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Dr. H | 48300 | Fail (hard) | CORE-02: 48.3 not in the quote; CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | revenue |  | 396520000 | Fail (hard) | CORE-02: 396520 not in the quote |
| btv-vier-lander-bank-ag-9e06fc63 | shareholding_requirement |  | 50 % der variablen Vergütung,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied und Vorsitzender des  | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Mario | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Dr. M | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Dr. H | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied und Vorsitzender des  | 231000 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Mario | 141000 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Dr. M | 129000 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Dr. H | 37600 | Fail (hard) | CORE-02: 37.6 not in the quote; CORE-03: quote not in the source text |
| burgenland-holding-ag-a95d1abc | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| burgenland-holding-ag-a95d1abc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| burgenland-holding-ag-a95d1abc | largest_holders |  | VERBUND AG 10%; WIEN ENERGIE G | Fail (hard) | CORE-03: quote not in the source text |
| burgenland-holding-ag-a95d1abc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| burgenland-holding-ag-a95d1abc | pension_contribution | Mitglied des Vorstands (Dr. Kl | 144.87 | Fail (hard) | CORE-02: 144.87 not in the quote |
| burgenland-holding-ag-a95d1abc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burgenland-holding-ag-a95d1abc | share_price |  | 71.5 | Fail (hard) | CORE-02: 71.5 not in the quote; CORE-03: quote not in the source text |
| burgenland-holding-ag-a95d1abc | total_remuneration | Mitglied des Vorstands (Dr. Kl | 5500 | Fail (hard) | CORE-02: 5.5 not in the quote; XF-01: parts add up to 5,650, more than the stated 5,500; XF-02: parts add up to 5,650, stated 5,500 |
| burgenland-holding-ag-a95d1abc | total_remuneration | Mitglied des Vorstands (Dr. Al | 5500 | Fail (hard) | CORE-02: 5.5 not in the quote |
| ca-immobilien-anlagen-ag-a9ff4a4a | staff_by_segment |  | Austria: 80; Germany/Switzerla | Fail | CORE-04: no period_end; NUM-08: adds up to 348 vs 254 (37.0% apart) |
| cancom-se-o-n | lti_target | CEO | 201666.67 | Fail (hard) | CORE-03: quote not in the source text |
| cherry-se-57089b55 | benefits |  | Company car or car allowance,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | lti_max | CEO | 2500000 | Fail (hard) | CORE-02: 2500000 not in the quote; CORE-04: no period_end |
| cherry-se-57089b55 | lti_max | CFO (15.04. - 31.12.2023) | 1650000 | Fail (hard) | CORE-02: 1650000 not in the quote; CORE-04: no period_end |
| cherry-se-57089b55 | lti_max | Former CFO (until March 2023) | 1650000 | Fail (hard) | CORE-02: 1650000 not in the quote; CORE-04: no period_end |
| cherry-se-57089b55 | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| cherry-se-57089b55 | pay_currency | CFO (15.04. - 31.12.2023) | EUR | Fail | CORE-04: no period_end |
| cherry-se-57089b55 | pay_currency | COO | EUR | Fail | CORE-04: no period_end |
| cherry-se-57089b55 | pay_currency | Former CFO (until March 2023) | EUR | Fail | CORE-04: no period_end |
| cherry-se-57089b55 | pension_type |  | Defined contribution, company  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | role_disclosure | CFO (15.04. - 31.12.2023) | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | role_disclosure | COO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | role_disclosure | Former CFO (until March 2023) | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cherry-se-57089b55 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| cherry-se-57089b55 | total_remuneration | CEO | 886868 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 1,029,355, more than the stated 886,868; XF-02: parts add up to 1,029,355, stated 886,868 |
| commerzbank-ag | total_remuneration | Board of Managing Directors | 17457000 | Fail (hard) | XF-01: parts add up to 20,037,000, more than the stated 17,457,000; XF-02: parts add up to 20,037,000, stated 17,457,000 |
| continental-ag-o-n | base_salary | Vorstandsvorsitzender (01.12.2 | 1550000 | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | benefits |  | company car (personal use), re | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cts-eventim-kgaa-1664614e | controlling_owner_name |  | KPS Stiftung | Fail (hard) | CORE-02: not in the quote: stiftung |
| cts-eventim-kgaa-1664614e | lti_granted | CEO | 800000 | Fail (hard) | CORE-02: 800000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | COO | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | CTO (seit 1. Januar 2025) | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | revenue_by_country |  | Germany: 1347630; Italy: 60590 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cts-eventim-kgaa-1664614e | revenue_by_segment |  | Ticketing: 947220; Live Entert | Fail (hard) | CORE-03: quote not in the source text |
| data-modul-ag-9cac6e64 | ebitda |  | 2490000 | Fail (hard) | CORE-03: quote not in the source text |
| data-modul-ag-9cac6e64 | revenue_by_segment |  | Displays: 126601; Systems: 862 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: quote not in the source text |
| deutsche-post-ag-b89554ef | pension_contribution | Supply Chain (since August 16, | 100333 | Fail (hard) | CORE-02: 100333 not in the quote |
| deutz-ag-8a315ac8 | lti_target | Vorstandsvorsitzender | 622000 | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 37000 | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| deutz-ag-8a315ac8 | total_remuneration | ordentliches Vorstandsmitglied | 955000 | Fail (hard) | XF-01: parts add up to 1,005,000, more than the stated 955,000; XF-02: parts add up to 1,005,000, stated 955,000 |
| do-co-aktiengesellschaft-1ce4abbb | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| do-co-aktiengesellschaft-1ce4abbb | revenue_by_country |  | Türkiye: 648.16; Great Britain | Fail | CORE-04: no period_end; NUM-08: adds up to 2,298,120,000 vs 2,461,590,000 (6.6% apart) |
| do-co-aktiengesellschaft-1ce4abbb | staff_by_country |  | Austria: 1641; Germany: 2493;  | Fail | CORE-04: no period_end; NUM-08: adds up to 19,330 vs 14,762 (30.9% apart) |
| draegerwerk-6fd21937 | benefits_value | Vorstandsvorsitzender | 15800 | Fail (hard) | CORE-02: 15.8 not in the quote |
| draegerwerk-6fd21937 | benefits_value | Vorstand Finanzen und IT und s | 29700 | Fail (hard) | CORE-02: 29.7 not in the quote |
| draegerwerk-6fd21937 | benefits_value | Vorstand Medizintechnik | 22500 | Fail (hard) | CORE-02: 22.5 not in the quote |
| draegerwerk-6fd21937 | benefits_value | Vorstand Sicherheitstechnik | 28700 | Fail (hard) | CORE-02: 28.7 not in the quote |
| draegerwerk-6fd21937 | benefits_value | Vorstand Vertrieb und Personal | 24900 | Fail (hard) | CORE-02: 24.9 not in the quote |
| draegerwerk-6fd21937 | lti_vested | Executive Board | 2974525 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-6fd21937 | total_remuneration | Vorständin Nachhaltigkeit und  | 458800 | Fail (hard) | XF-01: parts add up to 533,800, more than the stated 458,800; XF-02: parts add up to 533,800, stated 458,800 |
| draegerwerk-be66d9df | benefits_value | Vorstandsvorsitzender | 15800 | Fail (hard) | CORE-02: 15.8 not in the quote |
| draegerwerk-be66d9df | benefits_value | Vorstand Finanzen und IT und s | 29700 | Fail (hard) | CORE-02: 29.7 not in the quote |
| draegerwerk-be66d9df | benefits_value | Vorstand Medizintechnik | 22500 | Fail (hard) | CORE-02: 22.5 not in the quote |
| draegerwerk-be66d9df | benefits_value | Vorstand Sicherheitstechnik | 28700 | Fail (hard) | CORE-02: 28.7 not in the quote |
| draegerwerk-be66d9df | benefits_value | Vorstand Vertrieb und Personal | 24900 | Fail (hard) | CORE-02: 24.9 not in the quote |
| draegerwerk-be66d9df | lti_granted | Vorstandsvorsitzender | 470700 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Vorstand Finanzen und IT und s | 319400 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Vorstand Medizintechnik | 259900 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Vorstand Sicherheitstechnik | 272500 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Vorstand Vertrieb und Personal | 177100 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Vorständin Nachhaltigkeit und  | 125900 | Fail (hard) | CORE-02: 125.9 not in the quote; CORE-03: quote not in the source text |
| draegerwerk-be66d9df | lti_granted | Executive Board | 2974525 | Fail (hard) | CORE-03: quote not in the source text |
| draegerwerk-be66d9df | total_remuneration | Vorstand Vertrieb und Personal | 1096600 | Fail (hard) | XF-01: parts add up to 1,149,100, more than the stated 1,096,600; XF-02: parts add up to 1,149,100, stated 1,096,600 |
| draegerwerk-be66d9df | total_remuneration | Vorständin Nachhaltigkeit und  | 458800 | Fail (hard) | XF-01: parts add up to 533,800, more than the stated 458,800; XF-02: parts add up to 533,800, stated 458,800 |
| dt-konsum-real-estae-ag-4e32eb34 | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-konsum-real-estae-ag-4e32eb34 | benefits_value | CIO (bis 31.01.2025) | 10400 | Fail (hard) | CORE-02: 10.4 not in the quote |
| dt-konsum-real-estae-ag-4e32eb34 | benefits_value | CIO (ab 01.02.2025) | 4100 | Fail (hard) | CORE-02: 4.1 not in the quote |
| dt-konsum-real-estae-ag-4e32eb34 | benefits_value | CFO | 21900 | Fail (hard) | CORE-02: 21.9 not in the quote |
| dt-konsum-real-estae-ag-4e32eb34 | lti_granted | Management Board | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: quote not in the source text; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts EUR |
| dt-konsum-real-estae-ag-4e32eb34 | lti_vested | Management Board | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: quote not in the source text; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts EUR |
| dt-pfandbriefbk-ag-71e35702 | revenue_by_country |  | Germany: 421; Rest of Europe:  | Fail (hard) | CORE-03: quote not in the source text |
| dt-telekom-ag-9dfbbd0c | revenue_by_segment |  | Germany: 25610; United States: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-telekom-ag-9dfbbd0c | staff_by_country |  | Germany: 70751; other EU membe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| emerald-horizon-ag-a6420623 | fte |  | 20.42 | Fail (hard) | CORE-02: 20.42 not in the quote |
| emerald-horizon-ag-a6420623 | revenue |  | 224983 | Fail (hard) | CORE-02: 224983 not in the quote; CORE-04: no period_end |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 960000 | Fail (hard) | CORE-02: 960000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| eurotelesites-ag | sti_paid | CEO | 132000 | Fail (hard) | CORE-02: 132000 not in the quote |
| eurotelesites-ag | sti_paid | CFO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| evn-ag-90cea5f3 | listing_date |  | 1989 und 1990 | Fail (hard) | COD-06: not a year or a date |
| evn-ag-90cea5f3 | other_names |  | NIOGAS Niederösterreichische G | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| evn-ag-90cea5f3 | share_price |  | 28.8 | Fail (hard) | CORE-02: 28.8 not in the quote |
| evotec-se-0d298d1f | staff_by_country |  | FRANCE: 874; GERMANY: 1143; IT | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 4,553 vs 3,682 (23.7% apart) |
| facc-ag-5f4b658e | headcount |  | 4050 | Fail (hard) | CORE-03: quote not in the source text |
| facc-ag-5f4b658e | revenue_by_country |  | Germany: 354938; USA: 149717;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| facc-ag-5f4b658e | revenue_by_segment |  | Aerostructures: 345100; Engine | Fail (hard) | CORE-03: quote not in the source text |
| facc-ag-5f4b658e | staff_by_country |  | Austria: 3218; Croatia: 473 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 3,691 vs 4,050 (8.9% apart) |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Supervisory Board (non-executi | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| fortec-elektro-b45e5cd6 | controlling_owner_name |  | JotWe GmbH and FloJulCosMAr Gm | Fail (hard) | CORE-02: not in the quote: and |
| fortec-elektro-b45e5cd6 | ebitda |  | 7100000 | Fail (hard) | CORE-02: 7.1 not in the quote |
| frequentis-ag-b26b4708 | benefits_value | Vorstandsvorsitzender | 11600 | Fail (hard) | CORE-02: 11.6 not in the quote |
| frequentis-ag-b26b4708 | benefits_value | Member of the Management Board | 8600 | Fail (hard) | CORE-02: 8.6 not in the quote |
| frequentis-ag-b26b4708 | benefits_value | Member of the Management Board | 5900 | Fail (hard) | CORE-02: 5.9 not in the quote |
| frequentis-ag-b26b4708 | sti_paid | Member of the Management Board | 152800 | Fail (hard) | CORE-02: 152.8 not in the quote |
| frequentis-ag-b26b4708 | sti_paid | Member of the Management Board | 152800 | Fail (hard) | CORE-02: 152.8 not in the quote |
| frequentis-ag-b26b4708 | sti_paid | Member of the Management Board | 76400 | Fail (hard) | CORE-02: 76.4 not in the quote |
| fuchs-se-4990a338 | role_disclosure | Gesamtbeträge aller Vorstandsm | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| fuchs-se-4990a338 | shareholding_requirement |  | Executive Board members must i | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| gerresheimer-ag-25295c16 | sti_paid | Member of the Board (since Nov | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| gerresheimer-ag-25295c16 | sti_paid | Chief Financial Officer (since | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| gurktaler-ag-313b0a0d | fte |  | 7 | Fail (hard) | CORE-02: 7 not in the quote |
| gurktaler-ag-313b0a0d | headcount |  | 7 | Fail (hard) | CORE-02: 7 not in the quote |
| hamborner-reit-ag-cb84ee44 | listing_date |  | 1954 | Fail (hard) | CORE-02: not in the quote: 1954 |
| hawesko-holding-se-bd2e62b7 | benefits_value | Vorsitzender | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (seit 01.10.2025) | 3000 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (bis 09.10.2025) | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | lti_vested | Vorsitzender | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (seit 01.10.2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (bis 09.10.2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Vorsitzender | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (seit 01.10.2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (bis 09.10.2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| heid-maschinenfabrik-ag-72bb31c5 | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| heidelberg-materials-ag-20cc4657 | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | lti_target | Member of the Management Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| heidelberg-materials-ag-20cc4657 | pension_type |  | defined contribution, cash all | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| heidelberg-materials-ag-20cc4657 | shareholding_requirement |  | CEO: shares worth 180% of fixe | Fail (hard) | CORE-03: quote not in the source text |
| heidelberg-materials-ag-20cc4657 | total_remuneration | CEO | 8272000 | Fail (hard) | XF-01: parts add up to 8,696,000, more than the stated 8,272,000; XF-02: parts add up to 8,696,000, stated 8,272,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3160000 | Fail (hard) | XF-01: parts add up to 3,338,000, more than the stated 3,160,000; XF-02: parts add up to 3,338,000, stated 3,160,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 1751000 | Fail (hard) | XF-01: parts add up to 1,939,000, more than the stated 1,751,000; XF-02: parts add up to 1,939,000, stated 1,751,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 1259000 | Fail (hard) | XF-01: parts add up to 1,455,000, more than the stated 1,259,000; XF-02: parts add up to 1,455,000, stated 1,259,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3799000 | Fail (hard) | XF-01: parts add up to 4,034,000, more than the stated 3,799,000; XF-02: parts add up to 4,034,000, stated 3,799,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3506000 | Fail (hard) | XF-01: parts add up to 3,671,000, more than the stated 3,506,000; XF-02: parts add up to 3,671,000, stated 3,506,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 4206000 | Fail (hard) | XF-01: parts add up to 4,370,000, more than the stated 4,206,000; XF-02: parts add up to 4,370,000, stated 4,206,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (bis 15.07.202 | 1868000 | Fail (hard) | XF-01: parts add up to 2,641,000, more than the stated 1,868,000; XF-02: parts add up to 2,641,000, stated 1,868,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführerin (seit 01.03. | 993000 | Fail (hard) | XF-01: parts add up to 1,143,000, more than the stated 993,000; XF-02: parts add up to 1,143,000, stated 993,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 1425000 | Fail (hard) | XF-01: parts add up to 1,622,000, more than the stated 1,425,000; XF-02: parts add up to 1,622,000, stated 1,425,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.03.20 | 1380000 | Fail (hard) | XF-01: parts add up to 1,551,000, more than the stated 1,380,000; XF-02: parts add up to 1,551,000, stated 1,380,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 2105000 | Fail (hard) | XF-01: parts add up to 2,369,000, more than the stated 2,105,000; XF-02: parts add up to 2,369,000, stated 2,105,000 |
| hochtief-ag-3d11e5c0 | pay_currency | Chairman of the Executive Boar | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Chief Financial Officer | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pension_type |  | For new appointees from 2021:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| hochtief-ag-3d11e5c0 | role_disclosure | Chairman of the Executive Boar | individual | Fail (hard) | CORE-03: quote not in the source text |
| hochtief-ag-3d11e5c0 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: quote not in the source text |
| hochtief-ag-3d11e5c0 | role_disclosure | Chief Financial Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| hochtief-ag-3d11e5c0 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: quote not in the source text |
| hypoport-se-73d5ece9 | staff_by_country |  | Germany: 2314; Netherlands: 59 | Fail | CORE-04: no period_end; NUM-08: adds up to 2,436 vs 2,203 (10.6% apart) |
| infineon-tech-ag-8660f215 | pension_type |  | Defined contribution plan that | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| infineon-tech-ag-8660f215 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Elke  | 1193214 | Fail (hard) | XF-01: parts add up to 1,446,414, more than the stated 1,193,214; XF-02: parts add up to 1,446,414, stated 1,193,214 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Dr. S | 2028369 | Fail (hard) | XF-01: parts add up to 2,281,569, more than the stated 2,028,369; XF-02: parts add up to 2,281,569, stated 2,028,369 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Andre | 1189604 | Fail (hard) | XF-01: parts add up to 1,442,804, more than the stated 1,189,604; XF-02: parts add up to 1,442,804, stated 1,189,604 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (until | 1197324 | Fail (hard) | XF-01: parts add up to 1,450,524, more than the stated 1,197,324; XF-02: parts add up to 1,450,524, stated 1,197,324 |
| init-innovation-3237f8ad | other_names |  | init AG | Fail (hard) | CORE-02: not in the quote: init |
| intica-systems-se-18005922 | sti_max | Vorsitzender des Vorstands | 150 | Fail (hard) | CORE-03: quote not in the source text |
| intica-systems-se-18005922 | sti_max | Mitglied des Vorstands (bis 30 | 150 | Fail (hard) | CORE-03: quote not in the source text |
| ivu-traffic-techn-ag-020c6212 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| josef-manner-comp-ag-4b81bd60 | largest_holders |  | Privatstiftung Manner 49.78%;  | Fail (hard) | CORE-03: quote not in the source text; NUM-07: holdings add up to 173.77% |
| josef-manner-comp-ag-4b81bd60 | other_names |  | Chocoladenfabrik Josef Manner | Fail (hard) | CORE-03: quote not in the source text |
| josef-manner-comp-ag-4b81bd60 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| josef-manner-comp-ag-4b81bd60 | revenue_by_segment |  | Süßwaren Österreich: 304316; S | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ebitda |  | 20600000 | Fail (hard) | CORE-02: 20.6 not in the quote; CORE-03: quote not in the source text |
| kapsch-trafficcom-ag-1d6bbc81 | revenue_by_country |  | Österreich: 15982; EMEA (exklu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ultimate_parent |  | Traditio-Privatstiftung; CHILD | Fail (hard) | CORE-02: not in the quote: traditio privatstiftung |
| koenig-bauer-ag-1f22b792 | benefits_value | CEO (from June 2025) | 36000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | benefits_value | CFO (from July 2025) | 23000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | benefits_value | Former CEO (until June 2025),  | 22000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 6000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 0 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | lti_granted | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357 not in the quote |
| koenig-bauer-ag-1f22b792 | lti_granted | Former Member of the Managemen | 312000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | lti_granted | Former Member of the Managemen | 312000 | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | lti_target | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_max | CEO (from June 2025) | 494000 | Fail (hard) | CORE-02: 494000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_target | CEO (from June 2025) | 330000 | Fail (hard) | CORE-02: 330000 not in the quote |
| koenig-bauer-ag-1f22b792 | total_remuneration | CEO (from June 2025) | 934000 | Fail (hard) | XF-01: parts add up to 959,000, more than the stated 934,000; XF-02: parts add up to 959,000, stated 934,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former CEO (until June 2025),  | 782000 | Fail (hard) | XF-01: parts add up to 813,000, more than the stated 782,000; XF-02: parts add up to 813,000, stated 782,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former Member of the Managemen | 446000 | Fail (hard) | XF-01: parts add up to 507,000, more than the stated 446,000; XF-02: parts add up to 507,000, stated 446,000 |
| krones-ag-f49c3596 | role_disclosure | Sales and Marketing | individual | Fail (hard) | CORE-03: quote not in the source text |
| krones-ag-f49c3596 | role_disclosure | International Operations and S | individual | Fail (hard) | CORE-03: quote not in the source text |
| krones-ag-f49c3596 | role_disclosure | Filling and Packaging Technolo | individual | Fail (hard) | CORE-03: quote not in the source text |
| krones-ag-f49c3596 | total_remuneration | International Operations and S | 1357000 | Fail (hard) | CORE-02: 1357 not in the quote; CORE-03: quote not in the source text |
| ksb-se-co-kgaa-22d5b1d9 | lti_target | Key management personnel (Mana | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| ksb-se-co-kgaa-22d5b1d9 | sti_target | Key management personnel (Mana | 15 | Fail (hard) | COD-01: unit '' is not a target form |
| lenzing-ag-c20f8b4a | base_salary | Vorsitzender des Vorstandes | 333000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | base_salary | Chief Pulp & Chief Technology  | 333000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | base_salary | Member of the Management Board | 333000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | base_salary | Chief Operating Officer (from  | 194000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | base_salary | Member of the Management Board | 111000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | benefits_value | Vorsitzender des Vorstandes | 2000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | benefits_value | Chief Pulp & Chief Technology  | 2000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | benefits_value | Member of the Management Board | 2000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | benefits_value | Chief Operating Officer (from  | 1000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | benefits_value | Member of the Management Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_granted | Chief Pulp & Chief Technology  | 333000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_granted | Member of the Management Board | 333000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_granted | Chief Operating Officer (from  | 292000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Vorsitzender des Vorstandes | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Chief Pulp & Chief Technology  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Member of the Management Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Chief Operating Officer (from  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Member of the Management Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | lti_vested | Managing Board | -46000 | Fail (hard) | CORE-02: -46 not in the quote; NUM-04: -46000 outside 0..5e+10 |
| lenzing-ag-c20f8b4a | pension_contribution | Vorsitzender des Vorstandes | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | pension_contribution | Chief Pulp & Chief Technology  | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | pension_contribution | Member of the Management Board | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | pension_contribution | Chief Operating Officer (from  | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | pension_contribution | Member of the Management Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | shareholding_requirement |  | Verpflichtung, 25 % der LTI-Au | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Vorsitzender des Vorstandes | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Chief Pulp & Chief Technology  | 248000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Member of the Management Board | 248000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Chief Operating Officer (from  | 144000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Member of the Management Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | sti_paid | Managing Board | 840000 | Fail (hard) | CORE-02: 840 not in the quote |
| lenzing-ag-c20f8b4a | total_remuneration | Vorsitzender des Vorstandes | 545000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 363,000, stated 545,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Chief Pulp & Chief Technology  | 608000 | Fail (hard) | CORE-03: quote not in the source text |
| lenzing-ag-c20f8b4a | total_remuneration | Member of the Management Board | 3011000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 944,000, stated 3,011,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Chief Operating Officer (from  | 547000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 647,000, more than the stated 547,000; XF-02: parts add up to 647,000, stated 547,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Member of the Management Board | 111000 | Fail (hard) | CORE-03: quote not in the source text |
| linz-textil-holding-ag-e11cf1a9 | ebitda |  | 939336 | Fail (hard) | CORE-02: 939.336 not in the quote; CORE-03: quote not in the source text |
| linz-textil-holding-ag-e11cf1a9 | largest_holders |  | TYLE-Privatstiftung 80%; Tyle  | Fail (hard) | NUM-07: holdings add up to 160% |
| linz-textil-holding-ag-e11cf1a9 | listing_date |  | 1872 | Fail (hard) | COD-06: not a year or a date |
| lufthansa-ag-0bc3d92c | controlling_owner_name |  | Deutsche Lufthansa Aktiengesel | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| masterflex-96d8f19f | pension_contribution | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| masterflex-96d8f19f | pension_contribution | Chief Financial Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| masterflex-96d8f19f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| mayr-melnhof-karton-ag-ef1c26e1 | staff_by_country |  | Poland: 3027; Germany: 2091; A | Fail (hard) | CORE-03: quote not in the source text |
| mbb-se-be761dea | lti_target | Executive Chairman | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mbb-se-be761dea | lti_target | CFO | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chairman of the Board of Manag | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chief Technology Officer, Deve | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Integrity, Governance & Sustai | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Human Relations & Labour Direc | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chief Technology Officer, Deve | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Integrity, Governance & Sustai | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Production, Quality & Supply C | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Human Relations & Labour Direc | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Greater China (February 1 - De | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Greater China (January 1 - Jul | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Finance & Controlling (January | individual | Fail (hard) | CORE-03: quote not in the source text |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Sales & Customer Experience (F | 1730000 | Fail (hard) | XF-01: parts add up to 1,859,000, more than the stated 1,730,000; XF-02: parts add up to 1,859,000, stated 1,730,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Human Relations & Labour Direc | 695000 | Fail (hard) | XF-01: parts add up to 976,000, more than the stated 695,000; XF-02: parts add up to 976,000, stated 695,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Integrity, Governance & Sustai | 445000 | Fail (hard) | XF-01: parts add up to 486,000, more than the stated 445,000; XF-02: parts add up to 486,000, stated 445,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Production, Quality & Supply C | 154000 | Fail (hard) | XF-01: parts add up to 166,000, more than the stated 154,000; XF-02: parts add up to 166,000, stated 154,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Greater China (February 1 - De | 2104000 | Fail (hard) | XF-01: parts add up to 2,193,000, more than the stated 2,104,000; XF-02: parts add up to 2,193,000, stated 2,104,000 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | controlling_owner_name |  | Munich Re | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | lti_vested | Member of the Board of Managem | 1828378 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | lti_vested | Board of Management | 14200000 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | pension_contribution | Board of Management | 4000000 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | revenue_by_segment |  | Reinsurance – Life and health: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 934365 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: quote not in the source text |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Chair of the Board of Manageme | 7088819 | Fail (hard) | XF-01: parts add up to 8,449,244, more than the stated 7,088,819; XF-02: parts add up to 8,449,244, stated 7,088,819 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4295095 | Fail (hard) | XF-01: parts add up to 4,901,220, more than the stated 4,295,095; XF-02: parts add up to 4,901,220, stated 4,295,095 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4937800 | Fail (hard) | XF-01: parts add up to 5,888,950, more than the stated 4,937,800; XF-02: parts add up to 5,888,950, stated 4,937,800 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4221643 | Fail (hard) | XF-01: parts add up to 4,560,518, more than the stated 4,221,643; XF-02: parts add up to 4,560,518, stated 4,221,643 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Board of Management | 47000000 | Fail (hard) | CORE-03: quote not in the source text |
| nagarro-se-9ed14a85 | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: quote not in the source text |
| nagarro-se-9ed14a85 | role_disclosure | Chairperson of the Management  | individual | Fail (hard) | CORE-03: quote not in the source text |
| nagarro-se-9ed14a85 | role_disclosure | Member of the Management Board | individual | Fail (hard) | CORE-03: quote not in the source text |
| nagarro-se-9ed14a85 | role_disclosure | Member of the Management Board | individual | Fail (hard) | CORE-03: quote not in the source text |
| omv-ag-2c5e8b21 | lti_target | Chairman of the Executive Boar | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Energ | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Fuels | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Vice Presiden | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Deputy Chairman of the  | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Officer Marke | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| palfinger-ag-e07e19f6 | exchange_segment |  | Prime Market | Fail (hard) | CORE-03: quote not in the source text |
| palfinger-ag-e07e19f6 | revenue_by_country |  | Inland: 44423.1; EU: 21235.8;  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 77,550,800 vs 2,339,288,000 (96.7% apart) |
| palfinger-ag-e07e19f6 | share_price |  | 33.35 | Fail (hard) | CORE-02: 33.35 not in the quote |
| palfinger-ag-e07e19f6 | staff_by_country |  | Österreich: 2707; Russland: 15 | Fail | CORE-04: no period_end; NUM-08: adds up to 5,657 vs 12,358 (54.2% apart) |
| patrizia-se-41659152 | revenue_by_segment |  | Investment Management: 264348; | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 276,070,000 vs 258,416,000 (6.8% apart) |
| pne-ag-1fc0baf7 | benefits |  | Health and long-term care insu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| pne-ag-1fc0baf7 | lti_max | Vorstandsvorsitzender | 630000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | lti_max | Vorstandsmitglied (Harald Wilb | 540000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | lti_max | Vorstandsmitglied (Roland Stan | 495000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | role_disclosure | Vorstandsmitglied (until March | individual | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | sti_paid | Vorstandsvorsitzender | 101000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | sti_paid | Vorstandsmitglied (Roland Stan | 79000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | total_remuneration | Vorstandsvorsitzender | 469000 | Fail (hard) | CORE-03: quote not in the source text |
| pne-ag-1fc0baf7 | total_remuneration | Vorstandsmitglied (Roland Stan | 378000 | Fail (hard) | CORE-03: quote not in the source text |
| polytec-holding-ag-2a433fdb | revenue_by_country |  | Austria: 3900; Germany: 359275 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| polytec-holding-ag-2a433fdb | share_price |  | 3.3 | Fail (hard) | CORE-02: 3.3 not in the quote |
| porr-ag-127fa41a | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| porr-ag-127fa41a | controlling_owner_name |  | Syndicate | Fail (hard) | CORE-03: quote not in the source text |
| porr-ag-127fa41a | largest_holders |  | Syndicate 32.1% | Fail (hard) | CORE-03: quote not in the source text |
| porr-ag-127fa41a | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| porr-ag-127fa41a | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| porsche-ag-531bb563 | benefits |  | discounts and employee benefit | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| porsche-ag-531bb563 | controlling_owner_name |  | Volkswagen Aktiengesellschaft | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| porsche-ag-531bb563 | listing_date |  | 2022-09-29 | Fail (hard) | CORE-02: not in the quote: 2022 29 |
| porsche-ag-531bb563 | shares_outstanding |  | 911000000 | Fail (hard) | CORE-03: quote not in the source text |
| porsche-ag-531bb563 | total_remuneration | Chairman of the Executive Boar | 1456359 | Fail (hard) | XF-01: parts add up to 1,529,692, more than the stated 1,456,359; XF-02: parts add up to 1,529,692, stated 1,456,359 |
| porsche-ag-531bb563 | total_remuneration | Deputy Chairman of the Executi | 197600 | Fail (hard) | XF-01: parts add up to 266,588, more than the stated 197,600; XF-02: parts add up to 266,588, stated 197,600 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 817464 | Fail (hard) | XF-01: parts add up to 1,135,839, more than the stated 817,464; XF-02: parts add up to 1,135,839, stated 817,464 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board, | 814050 | Fail (hard) | XF-01: parts add up to 1,132,426, more than the stated 814,050; XF-02: parts add up to 1,132,426, stated 814,050 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 1572933 | Fail (hard) | XF-01: parts add up to 1,820,294, more than the stated 1,572,933; XF-02: parts add up to 1,820,294, stated 1,572,933 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 992610 | Fail (hard) | XF-01: parts add up to 1,377,613, more than the stated 992,610; XF-02: parts add up to 1,377,613, stated 992,610 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 163610 | Fail (hard) | XF-01: parts add up to 223,136, more than the stated 163,610; XF-02: parts add up to 223,136, stated 163,610 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 360662 | Fail (hard) | XF-01: parts add up to 499,871, more than the stated 360,662; XF-02: parts add up to 499,871, stated 360,662 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 362721 | Fail (hard) | XF-01: parts add up to 501,930, more than the stated 362,721; XF-02: parts add up to 501,930, stated 362,721 |
| procredit-holding-ag-74495a3c | headcount |  | 4660 | Fail (hard) | CORE-02: 4660 not in the quote; CORE-03: quote not in the source text |
| procredit-holding-ag-74495a3c | listing_date |  | 2016-12-22 | Fail (hard) | CORE-02: not in the quote: 2016 |
| procredit-holding-ag-74495a3c | revenue_by_segment |  | South Eastern Europe: 319141;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 565,433,000 vs 439,266,000 (28.7% apart) |
| procredit-holding-ag-74495a3c | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| procredit-holding-ag-74495a3c | website |  | procredit-holding.com | Fail (hard) | CORE-02: not in the quote: procredit holding |
| r-stahl-ag-04fdadc0 | benefits_value | Vorstandsvorsitzender (until D | 22200 | Fail (hard) | CORE-02: 22.2 not in the quote |
| r-stahl-ag-04fdadc0 | lti_target | Vorstandsvorsitzender (until D | 250000 | Fail (hard) | CORE-03: quote not in the source text |
| r-stahl-ag-04fdadc0 | lti_target | Mitglied des Vorstands | 130000 | Fail (hard) | CORE-03: quote not in the source text |
| r-stahl-ag-04fdadc0 | pension_contribution | Vorstandsvorsitzender (until D | 15400 | Fail (hard) | CORE-02: 15.4 not in the quote |
| r-stahl-ag-04fdadc0 | pension_contribution | Mitglied des Vorstands (from O | 1480 | Fail (hard) | CORE-02: 1.48 not in the quote |
| r-stahl-ag-04fdadc0 | pension_contribution | Mitglied des Vorstands | 14900 | Fail (hard) | CORE-02: 14.9 not in the quote |
| r-stahl-ag-04fdadc0 | role_disclosure | Former Executives, total | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: quote not in the source text |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: quote not in the source text |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| rath-ag-9e9ac567 | pension_contribution | Member of the Management Board | 15000 | Fail (hard) | CORE-02: 15 not in the quote |
| rath-ag-9e9ac567 | pension_contribution | Member of the Management Board | 10000 | Fail (hard) | CORE-02: 10 not in the quote |
| rath-ag-9e9ac567 | sti_paid | Member of the Management Board | 44000 | Fail (hard) | CORE-03: quote not in the source text |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 349000 | Fail (hard) | XF-01: parts add up to 364,000, more than the stated 349,000; XF-02: parts add up to 364,000, stated 349,000 |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 419000 | Fail (hard) | XF-01: parts add up to 429,000, more than the stated 419,000; XF-02: parts add up to 429,000, stated 419,000 |
| rheinmetall-ag-cf2ff08a | sti_max | Vorsitzender des Vorstands | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (bis 31 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rhoen-klinikum-0a013089 | role_disclosure | Vorstandsvorsitzender (ab 1. N | individual | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | base_salary | Executive Board member (since  | 601000 | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | base_salary | Executive Board member (since  | 263000 | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | pension_contribution | Executive Board member (since  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | pension_contribution | Executive Board member (since  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | revenue_by_country |  | Austria: 105546; USA: 343575;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rosenbauer | role_disclosure | Executive Board member (since  | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rosenbauer | role_disclosure | Executive Board member (since  | individual | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | share_price |  | 46.5 | Fail (hard) | CORE-02: 46.5 not in the quote |
| rosenbauer | staff_by_country |  | Austria: 1632; Germany: 1038;  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,312 vs 4,922 (12.4% apart) |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Chairman of the Executi | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | total_remuneration | Executive Board member (since  | 601000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,009,000, more than the stated 601,000; XF-02: parts add up to 1,009,000, stated 601,000 |
| rosenbauer | total_remuneration | Executive Board member (since  | 263000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 501,000, more than the stated 263,000; XF-02: parts add up to 501,000, stated 263,000 |
| rosenbauer | total_remuneration | Executive Board member | 406000 | Fail (hard) | XF-01: parts add up to 741,000, more than the stated 406,000; XF-02: parts add up to 741,000, stated 406,000 |
| rosenbauer | total_remuneration | Former Executive Board member  | 641000 | Fail (hard) | CORE-02: 641 not in the quote |
| saf-holland-se-e07079b5 | other_names |  | Otto Sauer Achsenfabrik GmbH;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| saf-holland-se-e07079b5 | staff_by_country |  | EMEA: 2282; Americas: 2480; AP | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| sap-se-b1a5f6d4 | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| sap-se-b1a5f6d4 | fte |  | 110650 | Fail (hard) | CORE-03: quote not in the source text |
| sap-se-b1a5f6d4 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| sap-se-b1a5f6d4 | revenue_by_segment |  | Cloud: 21023; Software license | Fail (hard) | CORE-03: quote not in the source text |
| sap-se-b1a5f6d4 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: quote not in the source text |
| sap-se-b1a5f6d4 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| sap-se-b1a5f6d4 | total_remuneration | CEO | 16244000 | Fail (hard) | XF-01: parts add up to 18,145,000, more than the stated 16,244,000; XF-02: parts add up to 18,145,000, stated 16,244,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2246000 | Fail (hard) | XF-01: parts add up to 3,256,000, more than the stated 2,246,000; XF-02: parts add up to 3,256,000, stated 2,246,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2531000 | Fail (hard) | XF-01: parts add up to 3,286,000, more than the stated 2,531,000; XF-02: parts add up to 3,286,000, stated 2,531,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 7044000 | Fail (hard) | XF-01: parts add up to 7,908,000, more than the stated 7,044,000; XF-02: parts add up to 7,908,000, stated 7,044,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2131000 | Fail (hard) | XF-01: parts add up to 2,728,000, more than the stated 2,131,000; XF-02: parts add up to 2,728,000, stated 2,131,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2524000 | Fail (hard) | XF-01: parts add up to 2,983,000, more than the stated 2,524,000; XF-02: parts add up to 2,983,000, stated 2,524,000 |
| sap-se-b1a5f6d4 | total_remuneration | Total Executive Board | 32720000 | Fail (hard) | XF-01: parts add up to 36,550,000, more than the stated 32,720,000; XF-02: parts add up to 36,550,000, stated 32,720,000 |
| sartorius-ag-9a9c739c | lti_vested | Executive Board Member (Dr. Re | 186000 | Fail (hard) | CORE-02: 186 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Chairma | 288000 | Fail (hard) | CORE-02: 288 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Member  | 179000 | Fail (hard) | CORE-02: 179 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Member  | 186000 | Fail (hard) | CORE-02: 186 not in the quote |
| sartorius-ag-a22309c5 | benefits |  | company car, accident insuranc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sartorius-ag-a22309c5 | pension_type |  | defined-benefit plans; base am | Fail (hard) | CORE-03: quote not in the source text |
| sartorius-ag-a22309c5 | total_remuneration | Former Executive Board Chairma | 2341000 | Fail (hard) | XF-01: parts add up to 2,695,000, more than the stated 2,341,000; XF-02: parts add up to 2,695,000, stated 2,341,000 |
| schott-pharma-ag-co-kgaa-26f01ea5 | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| secunet-security-ag-c4d9b7e4 | headcount |  | 1171 | Fail (hard) | CORE-03: quote not in the source text |
| secunet-security-ag-c4d9b7e4 | total_assets |  | 410700000 | Fail (hard) | CORE-03: quote not in the source text |
| semperit-ag-holding-2a7b594a | listing_date |  | 1890 | Fail (hard) | COD-06: not a year or a date |
| siemens-health-ag-1a42fb66 | revenue_by_country |  | Europe, C.I.S., Africa, Middle | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| siemens-health-ag-1a42fb66 | sub_sector |  | Siemens Healthineers offers im | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 44000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 39000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | benefits_value | COO | 32000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | benefits_value | CBO | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | benefits_value | CFO | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | COO | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | COO | 347000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | CBO | 246000 | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | CFO | 198000 | Fail (hard) | CORE-03: quote not in the source text |
| snp-schneider-neureither-f82bee76 | fiscal_year_end |  | 2023-12-31 | Fail (hard) | CORE-03: quote not in the source text |
| snp-schneider-neureither-f82bee76 | headcount |  | 1500 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| snp-schneider-neureither-f82bee76 | revenue |  | 203400000 | Fail (hard) | CORE-03: quote not in the source text |
| stadlauer-malzfabrik-ag-8a23c30d | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| stadlauer-malzfabrik-ag-8a23c30d | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| stadlauer-malzfabrik-ag-8a23c30d | sub_sector |  | Holdingfunktion | Fail (hard) | CORE-03: quote not in the source text |
| strabag-se-8e9d954e | staff_by_segment |  | North + West: 23161 | Fail | CORE-04: no period_end; NUM-08: adds up to 23,161 vs 88,556 (73.8% apart) |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | ebitda |  | 13800000 | Fail (hard) | CORE-02: 13.8 not in the quote |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (Klaus Einfalt) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (János Váczi) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | share_price |  | 32.2 | Fail (hard) | CORE-02: 32.2 not in the quote |
| telekom-austria-ag-62fec5fa | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| verbund | other_names |  | Österreichische Elektrizitätsw | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| voestalpine-ag-0a494926 | pension_contribution | Vorstand | 1360000 | Fail (hard) | CORE-02: 1.36 not in the quote |
| voestalpine-ag-0a494926 | total_remuneration | Vorstand | 23410000 | Fail (hard) | CORE-02: 23.41 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | benefits |  | D&O-Versicherung, Abfertigung, | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | ebitda |  | 1804000 | Fail (hard) | CORE-02: 1804 not in the quote; CORE-04: no period_end |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | share_price |  | 0.452 | Fail (hard) | CORE-02: 0.452 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | staff_by_segment |  | Investment Properties: 5; Hote | Fail | CORE-04: no period_end; NUM-08: adds up to 82 vs 87 (5.7% apart) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Vorsitzender des Vorstands | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | stellvertretender Vorsitzender | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Dr. Al | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Mag. F | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| wiener-privatbank-se-e8881192 | share_price |  | 10.8 | Fail (hard) | CORE-02: 10.8 not in the quote |
| wolford-ag-638e2dc1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| wolford-ag-638e2dc1 | controlling_owner_name |  | FFG Wisdom (Luxembourg) S.à r. | Fail (hard) | CORE-03: quote not in the source text |
| wolford-ag-638e2dc1 | headcount |  | 712 | Fail (hard) | CORE-02: 712 not in the quote |
| wolford-ag-638e2dc1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| wolford-ag-638e2dc1 | staff_by_country |  | Slovenia: 160; Austria: 209 | Fail | CORE-04: no period_end; NUM-08: adds up to 369 vs 712 (48.2% apart) |
