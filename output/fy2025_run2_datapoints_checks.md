# Output checks: fy2025_run2_datapoints.csv

100 companies, 4150 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 3416 (82%) |
| Review | 387 (9%) |
| Fail | 73 (2%) |
| Fail (hard) | 274 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 560 | 559 | 0 | 0 | 1 |
| Listing and market | 427 | 416 | 0 | 0 | 11 |
| Sector | 155 | 154 | 0 | 0 | 1 |
| Reporting basis | 263 | 261 | 0 | 0 | 2 |
| Financials | 266 | 222 | 28 | 1 | 15 |
| Workforce | 88 | 60 | 14 | 0 | 14 |
| Ownership and control | 295 | 266 | 0 | 0 | 29 |
| Segment and geography | 108 | 59 | 16 | 3 | 30 |
| Pay policy | 190 | 180 | 0 | 0 | 10 |
| Role and disclosure | 537 | 432 | 10 | 69 | 26 |
| Pay: fixed | 509 | 342 | 118 | 0 | 49 |
| Pay: STI | 305 | 193 | 85 | 0 | 27 |
| Pay: LTI | 246 | 173 | 43 | 0 | 30 |
| Pay: total | 201 | 99 | 73 | 0 | 29 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 4150 | 4145 | 5 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 1706 | 1609 | 97 | 2444 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 2800 | 2647 | 153 | 1350 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 2193 | 1738 | 455 | 1957 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 4150 | 4150 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 1347 | 1344 | 3 | 2803 | 'Euronext Oslo Børs' matches no ISO N exchange |
| COD-02 | Classification scheme named |  | 79 | 79 | 0 | 4071 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 158 | 158 | 0 | 3992 |  |
| COD-06 | Dates are valid | yes | 113 | 107 | 6 | 4037 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1205 | 1187 | 18 | 2945 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1104 | 1104 | 0 | 3046 |  |
| NUM-04 | Magnitude in a plausible range |  | 1373 | 1368 | 5 | 2777 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 125 | 125 | 0 | 4025 |  |
| NUM-06 | Percentages in range | yes | 267 | 267 | 0 | 3883 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 49 | 49 | 0 | 4101 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 97 | 75 | 22 | 4053 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 157 | 157 | 0 | 3993 |  |
| NUM-11 | STI paid not above its maximum |  | 82 | 77 | 5 | 4068 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 997 | 978 | 19 | 3153 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 28 | 24 | 4 | 4122 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 36 | 36 | 0 | 4114 |  |
| DER-06 | Derived value shows its formula |  | 155 | 155 | 0 | 3995 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 169 | 162 | 7 | 3981 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 169 | 124 | 45 | 3981 | parts add up to N stated N |

## Fill rate

Company fields: 2352 of 4100 filled (57%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 8 | 100 |
| staff_by_segment | 18 | 100 |
| staff_by_country | 20 | 100 |
| market_cap_band | 23 | 100 |
| controlling_owner_name | 28 | 100 |
| share_price | 34 | 100 |
| revenue_by_country | 34 | 100 |
| revenue_by_segment | 36 | 100 |
| listing_date | 42 | 100 |
| fte | 43 | 100 |
| headcount | 45 | 100 |
| exchange_segment | 47 | 100 |
| largest_holders | 49 | 100 |
| pe_stake_5pct | 49 | 100 |
| ownership_type | 51 | 100 |
| controlling_owner | 52 | 100 |
| shareholding_requirement | 52 | 100 |
| ebitda | 54 | 100 |
| other_names | 55 | 100 |
| fiscal_year | 57 | 100 |
| shares_outstanding | 58 | 100 |
| total_assets | 59 | 100 |
| revenue | 61 | 100 |
| accounting_basis | 62 | 100 |
| ultimate_parent | 66 | 100 |
| benefits | 68 | 100 |
| pension_type | 70 | 100 |
| isin | 71 | 100 |
| fiscal_year_end | 71 | 100 |
| website | 73 | 100 |
| reporting_currency | 73 | 100 |
| ticker | 76 | 100 |
| sub_sector | 76 | 100 |
| lei | 79 | 100 |
| sector_code | 79 | 100 |
| exchange | 83 | 100 |
| business_id | 84 | 100 |
| listing_status | 85 | 100 |
| legal_name | 87 | 100 |
| country_code | 87 | 100 |
| head_office_city | 87 | 100 |

Pay fields, over 227 executive roles:

| Field | Filled |
|---|---|
| base_salary | 189 (83%) |
| sti_paid | 144 (63%) |
| sti_target | 57 (25%) |
| sti_max | 104 (46%) |
| lti_vested | 83 (37%) |
| lti_granted | 74 (33%) |
| lti_target | 21 (9%) |
| lti_max | 68 (30%) |
| benefits_value | 148 (65%) |
| pension_contribution | 172 (76%) |
| total_remuneration | 201 (89%) |

## Failed values (347)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| addtech-nordic-ab | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | largest_holders |  | Tisenhult Invest 15.8%; Hedeli | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | listing_date |  | 2001-09 | Fail (hard) | COD-06: not a year or a date |
| addtech-nordic-ab | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| addtech-nordic-ab | pay_currency | Other members of Group Managem | SEK | Fail | CORE-04: no period_end |
| addtech-nordic-ab | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Human Resources, People | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vertriebsvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Sales (bis 31. Oktober  | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Operations (bis 10. Aug | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender (bis 30. | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand (bis 11. Mai 20 | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pension_type |  | For board members appointed be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| alpine-select-ag | fiscal_year_end |  | 2025 | Fail (hard) | COD-06: not a valid date |
| arbonia-ag | pay_currency | Group Management | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atlantic-petroleum | benefits_value | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlantic-petroleum | pay_currency | Managing Director – CEO | DKK | Fail | CORE-04: no period_end |
| atlantic-petroleum | sti_paid | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| banque-cantonale-du-jura-sa | base_salary | Other members of Direction | 910240 | Fail (hard) | CORE-02: 910240 not in the quote; CORE-04: no period_end |
| banque-cantonale-du-jura-sa | benefits |  | representation expenses, favor | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| banque-cantonale-du-jura-sa | pay_currency | Directeur général | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pay_currency | Other members of Direction | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pension_contribution | Other members of Direction | 323953 | Fail (hard) | CORE-02: 323953 not in the quote; CORE-04: no period_end |
| banque-cantonale-du-jura-sa | sti_paid | Other members of Direction | 367500 | Fail (hard) | CORE-02: 367500 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Chief Executive Officer | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Other members of the managemen | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_type |  | defined benefit plan, collecti | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; CORE-04: no period_end; XF-02: parts add up to 2,855,610, stated 3,028,977 |
| baywa-ag-na-o-n | benefits_value | Former Chief Executive Officer | 31400 | Fail (hard) | CORE-02: 31.4 not in the quote |
| baywa-ag-na-o-n | benefits_value | Member of the Board of Managem | 17200 | Fail (hard) | CORE-02: 17.2 not in the quote |
| baywa-ag-na-o-n | benefits_value | Member of the Board of Managem | 19900 | Fail (hard) | CORE-02: 19.9 not in the quote |
| baywa-ag-na-o-n | benefits_value | Chief Restructuring Officer (f | 15000 | Fail (hard) | CORE-02: 15 not in the quote |
| baywa-ag-na-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ebitda |  | -162500000 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | largest_holders |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_vested | Former Chief Executive Officer | 316700 | Fail (hard) | CORE-02: 316.7 not in the quote |
| baywa-ag-na-o-n | lti_vested | Member of the Board of Managem | 316700 | Fail (hard) | CORE-02: 316.7 not in the quote |
| baywa-ag-na-o-n | lti_vested | Member of the Board of Managem | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| baywa-ag-na-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pension_contribution | Former Chief Executive Officer | 188400 | Fail (hard) | CORE-02: 188.4 not in the quote |
| baywa-ag-na-o-n | pension_contribution | Member of the Board of Managem | 287800 | Fail (hard) | CORE-02: 287.8 not in the quote |
| baywa-ag-na-o-n | pension_contribution | Member of the Board of Managem | 128400 | Fail (hard) | CORE-02: 128.4 not in the quote |
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| baywa-ag-na-o-n | sti_paid | Member of the Board of Managem | 140000 | Fail (hard) | CORE-02: 140 not in the quote |
| baywa-ag-na-o-n | sti_paid | Member of the Board of Managem | 168000 | Fail (hard) | CORE-02: 168 not in the quote |
| baywa-ag-na-o-n | total_remuneration | Chief Restructuring Officer (f | 369500 | Fail (hard) | CORE-02: 369.5 not in the quote; XF-02: parts add up to 215,000, stated 369,500 |
| bell-food-group-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| bell-food-group-ag | pay_currency | Übrige Mitglieder der Gruppenl | CHF | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | Adm. Direktør (until February  | DKK | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | CFO (from July 1, 2025, regist | DKK | Fail | CORE-04: no period_end |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| canal-s-a | lti_granted | Other Management Board members | 100 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| canal-s-a | revenue_by_country |  | Europe: 3762; Africa: 2687; Re | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 9,136,000,000 vs 6,449,000,000 (41.7% apart) |
| cantargia-ab-1b3e1f95 | staff_by_country |  | Sweden: 23 | Fail (hard) | CORE-03: quote not in the source text |
| ceres-power-holdings-plc | total_assets |  | 145796000 | Fail (hard) | CORE-02: 145796 not in the quote; CORE-03: quote not in the source text |
| chesnara-plc | lti_granted | Key management personnel | 1200000 | Fail (hard) | CORE-02: 1200000 not in the quote |
| chesnara-plc | pension_contribution | Key management personnel | 100000 | Fail (hard) | CORE-02: 100000 not in the quote |
| chesnara-plc | pension_type |  | defined contribution, 9.5% of  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chesnara-plc | role_disclosure | Key management personnel | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| chesnara-plc | sti_paid | Key management personnel | 700000 | Fail (hard) | CORE-02: 700000 not in the quote |
| chesnara-plc | total_remuneration | Key management personnel | 4100000 | Fail (hard) | CORE-02: 4100000 not in the quote; XF-02: parts add up to 2,000,000, stated 4,100,000 |
| chesterfield-resources-plc | lti_granted | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| chesterfield-resources-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| chill-brands-group-plc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chill-brands-group-plc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chill-brands-group-plc | revenue_by_country |  | US Operations: 19741; UK Opera | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 555,749 vs 1,908,020 (70.9% apart) |
| cizzle-biotechnology-holdings-plc | exchange_segment |  | Equity Shares (transitional ca | Fail (hard) | CORE-02: not in the quote: shares |
| cizzle-biotechnology-holdings-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| clarkson-plc | fte |  | 2103 | Fail (hard) | CORE-03: quote not in the source text |
| clarkson-plc | staff_by_segment |  | Broking: 1504; Financial: 127; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 2,103 vs 2,250 (6.5% apart) |
| clarkson-plc | total_assets |  | 978500000 | Fail (hard) | CORE-03: quote not in the source text |
| cloudbreak-discovery-plc | accounting_basis |  | UK-adopted international accou | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cloudbreak-discovery-plc | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| cloudbreak-discovery-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| coats-group-plc | lti_granted | Group Chief Executive Officer | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | lti_granted | Group Chief Financial Officer | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | share_price |  | 84.55 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| cobra-resources-plc | headcount |  | 4 | Fail (hard) | CORE-02: 4 not in the quote |
| cobra-resources-plc | pension_type |  | No directors had benefits accr | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | lti_granted | Other current members | 5003494 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | lti_granted | Former members | 323421 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | pension_contribution | Other current members | 1068366 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | pension_contribution | Former members | 116009 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | revenue_by_country |  | Switzerland: 460.2; The Russia | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| coca-cola-hbc-ag | share_price |  | 38.42 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | staff_by_country |  | Armenia: 345; Austria: 871; Be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| coca-cola-hbc-ag | total_remuneration | Other current members | 20949564 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | total_remuneration | Former members | 1462462 | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | base_salary | ehemaliger Vorsitzender (bis 3 | 481000 | Fail (hard) | CORE-02: 481 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| commerzbank-ag | benefits_value | Vorsitzende (seit 1. Oktober 2 | 228000 | Fail (hard) | CORE-02: 228 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| commerzbank-ag | benefits_value | Chief Operating Officer (seit  | 273000 | Fail (hard) | CORE-02: 273 not in the quote; CORE-04: no period_end |
| commerzbank-ag | pay_currency | Vorsitzende (seit 1. Oktober 2 | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | stellvertretender Vorsitzender | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Group Human Resources & Group  | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Segment Privat- und Unternehme | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Chief Financial Officer (seit  | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Chief Risk Officer (seit 1. Ja | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Chief Operating Officer (seit  | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | ehemaliger Vorsitzender (bis 3 | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | Former Management Board Member | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pay_currency | ehemaliger Vorsitzender (bis 3 | EUR | Fail | CORE-04: no period_end |
| commerzbank-ag | pension_contribution | ehemaliger Vorsitzender (bis 3 | 159000 | Fail (hard) | CORE-02: 159 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| commerzbank-ag | pension_type |  | Beitragsorientierte Versorgung | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 3,511,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | stellvertretender Vorsitzender | 2917000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 2,453,000, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Group Human Resources & Group  | 2116000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,880,000, stated 2,116,000 |
| commerzbank-ag | total_remuneration | Segment Privat- und Unternehme | 2086000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,904,000, stated 2,086,000 |
| commerzbank-ag | total_remuneration | Chief Financial Officer (seit  | 1896000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,281,000, stated 1,896,000 |
| commerzbank-ag | total_remuneration | Chief Risk Officer (seit 1. Ja | 2113000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,500,000, stated 2,113,000 |
| commerzbank-ag | total_remuneration | Chief Operating Officer (seit  | 2312000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,620,000, stated 2,312,000 |
| compass-group-plc | benefits_value | Group COO, North America | 106000 | Fail (hard) | CORE-03: quote not in the source text |
| compass-group-plc | lti_vested | Group COO, North America | 3882000 | Fail (hard) | CORE-03: quote not in the source text |
| compass-group-plc | sti_paid | Group COO, North America | 2074000 | Fail (hard) | CORE-03: quote not in the source text |
| compass-group-plc | total_remuneration | Group COO, North America | 7213000 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | revenue_by_segment |  | UK: 1419.2; Germany: 2109.3; W | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | exchange |  | London Stock Exchange | Fail (hard) | CORE-02: not in the quote: london stock exchange |
| conduit-holdings-limited | headcount |  | 68 | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | staff_by_country |  | UK: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 2 vs 68 (97.1% apart) |
| contango-holdings-plc | website |  | contango-holdings-plc.co.uk | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | listing_date |  | 2016-10 | Fail (hard) | COD-06: not a year or a date |
| convatec-group-plc | staff_by_country |  | Europe: 5276; North America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | staff_by_segment |  | Operations: 3467; Sales and ma | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | sti_target | Former Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | total_remuneration | Former Chief Executive Officer | 7648000 | Fail (hard) | XF-01: parts add up to 8,565,000, more than the stated 7,648,000; XF-02: parts add up to 8,565,000, stated 7,648,000 |
| corem-property-d | benefits |  | company car, health insurance | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-d | pay_currency | Vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Vice vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| corem-property-d | sti_paid | Andra ledande befattningshavar | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote; CORE-04: no period_end |
| corpus-resources-plc | controlling_owner_name |  | James Antony Stenhouse | Fail (hard) | CORE-02: not in the quote: antony |
| corpus-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| crest-nicholson-holdings-plc | revenue_by_segment |  | UK housebuilding: 610.8 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| critical-metals-plc | share_price |  | 9.1 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | staff_by_country |  | DRC: 49 | Fail | CORE-04: no period_end |
| critical-mineral-resources-plc | fte |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| croda-international-plc | sti_paid | Chief Financial Officer (CFO)  | 359.203 | Fail (hard) | CORE-02: 359.203 not in the quote |
| currys-plc | fte |  | 25076 | Fail (hard) | CORE-02: 25076 not in the quote |
| cykel-ai-plc | total_assets |  | 1537768 | Fail (hard) | CORE-03: quote not in the source text |
| dar-global-plc | ebitda |  | 126600000 | Fail (hard) | CORE-02: 126.6 not in the quote |
| dcc-energy-plc | lti_granted | Chief Executive | 2051000 | Fail (hard) | CORE-03: quote not in the source text; NUM-12: currency GBP, the role's other amounts EUR |
| dcc-energy-plc | revenue_by_segment |  | DCC Energy: 12990355; DCC Tech | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | sti_paid | Chief Executive | 1928000 | Fail (hard) | CORE-02: 1928 not in the quote |
| defence-holdings-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| derwent-london-plc | lti_vested | CEO | 502000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | lti_vested | Other Executive Directors | 502000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| derwent-london-plc | sti_paid | CEO | 658000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | sti_paid | Other Executive Directors | 651000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | total_remuneration | CEO | 845000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,619,119, more than the stated 845,000; XF-02: parts add up to 1,619,119, stated 845,000 |
| derwent-london-plc | total_remuneration | Other Executive Directors | 651000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,215,600, more than the stated 651,000; XF-02: parts add up to 1,215,600, stated 651,000 |
| dfi-retail-group-holdings-limited | controlling_owner_name |  | Jardine Matheson Holdings Limi | Fail (hard) | CORE-02: not in the quote: holdings limited |
| dfs-furniture-plc | base_salary | CEO | 521000 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | benefits_value | CEO | 54000 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | pension_contribution | CEO | 18000 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| dfs-furniture-plc | sti_paid | CEO | 609000 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | total_remuneration | CEO | 1152000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,202,000, more than the stated 1,152,000; XF-02: parts add up to 1,202,000, stated 1,152,000 |
| dfs-furniture-plc | total_remuneration | Former interim CFO (until 2 Ap | 716000 | Fail (hard) | XF-01: parts add up to 1,181,000, more than the stated 716,000; XF-02: parts add up to 1,181,000, stated 716,000 |
| diageo-plc | revenue_by_country |  | United States: 7408; India: 32 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| diageo-plc | revenue_by_segment |  | North America: 7249; Europe: 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 19,643,000,000 vs 27,762,000,000 (29.2% apart) |
| diageo-plc | staff_by_segment |  | SC&P: 6963; Corporate and othe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 12,605 vs 27,972 (54.9% apart) |
| diageo-plc | total_remuneration | Chief Executive Officer | 1429000 | Fail (hard) | CORE-03: quote not in the source text |
| diageo-plc | total_remuneration | Chief Financial Officer | 1317000 | Fail (hard) | CORE-03: quote not in the source text |
| diageo-plc | total_remuneration | Former CEO (until July 2025) | 79000 | Fail (hard) | CORE-03: quote not in the source text |
| dialight-plc | pension_contribution | Group Chief Executive Officer | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dialight-plc | pension_contribution | Group Chief Financial Officer | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dialight-plc | shareholding_requirement |  | Executive Directors: shares wo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dialight-plc | sti_paid | Group Chief Executive Officer | 60 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dialight-plc | sti_paid | Group Chief Financial Officer | 60 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| diploma-plc | base_salary | Group Chief Executive | 918000 | Fail (hard) | CORE-02: 918000 not in the quote |
| diploma-plc | base_salary | Acting Chief Financial Officer | 56000 | Fail (hard) | CORE-02: 56000 not in the quote |
| diploma-plc | benefits_value | Group Chief Executive | 32000 | Fail (hard) | CORE-02: 32000 not in the quote |
| diploma-plc | benefits_value | Acting Chief Financial Officer | 1000 | Fail (hard) | CORE-02: 1000 not in the quote |
| diploma-plc | lti_vested | Group Chief Executive | 4326000 | Fail (hard) | CORE-02: 4326000 not in the quote |
| diploma-plc | lti_vested | Acting Chief Financial Officer | 514000 | Fail (hard) | CORE-02: 514000 not in the quote |
| diploma-plc | pension_contribution | Group Chief Executive | 37000 | Fail (hard) | CORE-02: 37000 not in the quote |
| diploma-plc | pension_contribution | Acting Chief Financial Officer | 2000 | Fail (hard) | CORE-02: 2000 not in the quote |
| diploma-plc | revenue_by_segment |  | Controls: 836.4; Seals: 456; L | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| diploma-plc | sti_paid | Group Chief Executive | 1837000 | Fail (hard) | CORE-02: 1837000 not in the quote |
| diploma-plc | sti_paid | Acting Chief Financial Officer | 84000 | Fail (hard) | CORE-02: 84000 not in the quote |
| diploma-plc | total_remuneration | Group Chief Executive | 7150000 | Fail (hard) | CORE-02: 7150000 not in the quote |
| diploma-plc | total_remuneration | Acting Chief Financial Officer | 657000 | Fail (hard) | CORE-02: 657000 not in the quote |
| domino-s-pizza-group-plc | fte |  | 2402 | Fail (hard) | CORE-02: 2402 not in the quote |
| domino-s-pizza-group-plc | lti_granted | Former CEO (until 24 November  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| domino-s-pizza-group-plc | lti_granted | Former CFO (until 18 September | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dr-martens-plc | benefits_value | CEO | 5000 | Fail (hard) | CORE-02: 5 not in the quote; CORE-03: quote not in the source text |
| dr-martens-plc | benefits_value | CFO | 19000 | Fail (hard) | CORE-02: 19 not in the quote; CORE-03: quote not in the source text |
| dr-martens-plc | fte |  | 3610 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 3,610 above headcount 2,377 |
| dr-martens-plc | headcount |  | 2377 | Fail (hard) | CORE-03: quote not in the source text |
| dr-martens-plc | lti_granted | CEO | 1950000 | Fail (hard) | CORE-02: 1950 not in the quote |
| dr-martens-plc | lti_granted | CFO | 1498650 | Fail (hard) | CORE-02: 1498.65 not in the quote |
| dr-martens-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| dr-martens-plc | lti_vested | CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| drax-group-plc | fte |  | 3128 | Fail (hard) | CORE-02: 3128 not in the quote |
| drax-group-plc | share_price |  | 837.8 | Fail (hard) | CORE-03: quote not in the source text |
| dunelm-group-plc | controlling_owner_name |  | Adderley family (Concert Party | Fail (hard) | CORE-02: not in the quote: family |
| dunelm-group-plc | listing_date |  | 2006-10 | Fail (hard) | COD-06: not a year or a date |
| easyjet-plc | lti_granted | CEO | 125 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| easyjet-plc | lti_granted | CFO (from 20 January 2025) | 100 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| easyjet-plc | revenue_by_segment |  | Airline: 8666; Holidays: 1917 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| easyjet-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| ecora-royalties-plc | base_salary | Chief Executive Officer | 485000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | base_salary | Chief Financial Officer | 345000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | lti_vested | Chief Executive Officer | 80000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | lti_vested | Chief Financial Officer | 52000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | pension_contribution | Chief Executive Officer | 49000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_country |  | Australia: 19664; Americas: 31 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_segment |  | Cobalt: 18871; Copper: 14180;  | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | sti_paid | Chief Executive Officer | 312000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | sti_paid | Chief Financial Officer | 220000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | total_remuneration | Chief Executive Officer | 940000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | total_remuneration | Chief Financial Officer | 654000 | Fail (hard) | CORE-03: quote not in the source text |
| elementis-plc | benefits_value | Former CEO (until 31 July 2025 | 84434 | Fail (hard) | CORE-03: quote not in the source text |
| elementis-plc | benefits_value | Former CFO (until 31 December  | 30466 | Fail (hard) | CORE-03: quote not in the source text |
| elixirr-international-plc | benefits_value | Chief Executive Officer | 13000 | Fail (hard) | CORE-02: 13 not in the quote |
| elixirr-international-plc | benefits_value | Deputy Chief Executive Officer | 8000 | Fail (hard) | CORE-02: 8 not in the quote |
| elixirr-international-plc | benefits_value | Chief Financial Officer (appoi | 12000 | Fail (hard) | CORE-02: 12 not in the quote |
| elixirr-international-plc | ebitda |  | 44300000 | Fail (hard) | CORE-02: 44300000 not in the quote |
| elixirr-international-plc | sti_paid | Chief Executive Officer | 1392000 | Fail (hard) | CORE-02: 1392 not in the quote |
| elixirr-international-plc | sti_paid | Deputy Chief Executive Officer | 1392000 | Fail (hard) | CORE-02: 1392 not in the quote |
| elixirr-international-plc | sti_paid | Chief Financial Officer (appoi | 580000 | Fail (hard) | CORE-02: 580 not in the quote |
| endeavour-mining-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner_name |  | La Mancha | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | fte |  | 5659 | Fail (hard) | CORE-02: 5659 not in the quote |
| endeavour-mining-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | revenue_by_segment |  | Ity Mine: 838.1; Houndé Mine:  | Fail (hard) | CORE-03: quote not in the source text |
| enquest-plc | lti_granted | Chief Executive | 185 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| enquest-plc | lti_granted | Chief Financial Officer | 185 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| enquest-plc | revenue_by_country |  | North Sea: 895313; Malaysia: 1 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | fte |  | 28867 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | revenue_by_segment |  | UK&I: 2180.1; International: 2 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| entain-plc | staff_by_segment |  | UK&I: 18582; International: 65 | Fail (hard) | CORE-03: quote not in the source text |
| eurocell-plc | listing_date |  | 2015-03 | Fail (hard) | COD-06: not a year or a date |
| everest-global-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | controlling_owner_name |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | largest_holders |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pension_contribution | Chief Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| everest-global-plc | pension_contribution | Executive Director of Precious | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Other leading executives | 5 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | Other leading executives | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pension_type |  | VD har en premiebaserad pensio | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Deputy Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Other members of Executive Man | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| intea-fastigheter-d | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pension_contribution | Övriga ledande befattningshava | 1300000 | Fail (hard) | CORE-02: 1.3 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Verkställande direktör | 3800000 | Fail (hard) | CORE-02: 3.8 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 4094000 | Fail (hard) | CORE-02: 4094 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3325000 | Fail (hard) | CORE-02: 3325 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 293000 | Fail (hard) | CORE-02: 293 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 266000 | Fail (hard) | CORE-02: 266 not in the quote; CORE-04: no period_end |
| jinhui-shipping | benefits |  | medical insurance and contribu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | controlling_owner_name |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-02: not in the quote: limited |
| jinhui-shipping | largest_holders |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | pay_currency | Executive Director (Ng Siu Fai | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ng Kam Wah | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ng Ki Hung | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ho Suk Lin | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pe_stake_5pct |  | no | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | ultimate_parent |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-02: not in the quote: limited |
| ostasiatiske | pay_currency | CEO (Kresten M. Valdal) | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | pay_currency | Direktionen | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | pay_currency | CEO (Martin Thaysen) | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | sti_paid | CEO (Kresten M. Valdal) | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| paratus-energy | revenue_by_segment |  | Seagems: 265; Fontis: 187 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 452,000,000 vs 153,200,000 (195.0% apart) |
| revolutionrace | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| revolutionrace | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Chief Financial Officer | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Chief Operations Officer | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | General Manager | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Subsidiary employee | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Total remuneration executive m | USD | Fail | CORE-04: no period_end |
| seb-c | revenue |  | -411000 | Fail | CORE-04: no period_end; NUM-04: -411000 outside 0..1e+14 |
| seb-c | revenue_by_country |  | Sweden: 46498; Norway: 4315; D | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 76,903,000,000 vs -411,000 (18711292.2% apart) |
| seb-c | revenue_by_segment |  | Corporate & Investment Banking | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 76,928,000,000 vs -411,000 (18717374.9% apart) |
| seb-c | staff_by_country |  | Sverige: 189 | Fail (hard) | CORE-03: quote not in the source text |
| sed-energy | pay_currency | Key management personnel | USD | Fail | CORE-04: no period_end |
| sed-energy | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| stora-enso-a | controlling_owner |  | state | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | controlling_owner_name |  | Solidium Oy | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | ownership_type |  | state_owned | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | revenue_by_country |  | Austria: 298; Baltic States: 3 | Fail (hard) | CORE-03: quote not in the source text |
| subsea7 | pension_contribution | Chief Financial Officer | 60500 | Fail (hard) | CORE-03: quote not in the source text |
| subsea7 | revenue_by_country |  | Norway: 1664.6; United Kingdom | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| subsea7 | staff_by_country |  | Angola: 242; Australia: 246; B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
| tallink-grupp-5c02812d | pay_currency | Chairman of the Management Boa | EUR | Fail | CORE-04: no period_end |
| tallink-grupp-5c02812d | pay_currency | Member of the Management Board | EUR | Fail | CORE-04: no period_end |
| tallink-grupp-5c02812d | pay_currency | Member of the Management Board | EUR | Fail | CORE-04: no period_end |
| tallink-grupp-5c02812d | pay_currency | Member of the Management Board | EUR | Fail | CORE-04: no period_end |
| tallink-grupp-5c02812d | pay_currency | Member of the Management Board | EUR | Fail | CORE-04: no period_end |
| uie | pay_currency | Managing Director | USD | Fail | CORE-04: no period_end |
| uie | sti_max | Managing Director | 50 | Fail (hard) | CORE-04: no period_end; COD-01: unit '' is not a target form |
| voss-veksel-landmandsbank | pay_currency | Banksjef | NOK | Fail | CORE-04: no period_end |
