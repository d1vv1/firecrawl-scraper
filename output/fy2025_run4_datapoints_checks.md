# Output checks: fy2025_run4_datapoints.csv

19 companies, 791 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 702 (89%) |
| Review | 30 (4%) |
| Fail | 5 (1%) |
| Fail (hard) | 54 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 101 | 101 | 0 | 0 | 0 |
| Listing and market | 78 | 72 | 0 | 0 | 6 |
| Sector | 30 | 29 | 0 | 0 | 1 |
| Reporting basis | 60 | 60 | 0 | 0 | 0 |
| Financials | 59 | 47 | 5 | 0 | 7 |
| Workforce | 19 | 15 | 2 | 0 | 2 |
| Ownership and control | 77 | 62 | 0 | 0 | 15 |
| Segment and geography | 10 | 6 | 1 | 0 | 3 |
| Pay policy | 32 | 30 | 0 | 0 | 2 |
| Role and disclosure | 115 | 105 | 1 | 5 | 4 |
| Pay: fixed | 97 | 84 | 6 | 0 | 7 |
| Pay: STI | 48 | 39 | 5 | 0 | 4 |
| Pay: LTI | 28 | 27 | 0 | 0 | 1 |
| Pay: total | 37 | 25 | 10 | 0 | 2 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 791 | 790 | 1 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 351 | 330 | 21 | 440 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 577 | 552 | 25 | 214 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 416 | 387 | 29 | 375 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 791 | 790 | 1 | 0 | period_end 'N December N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 259 | 255 | 4 | 532 | 'Oslo Stock Exchange (Euronext Oslo Børs)' matches no ISO N exchange |
| COD-02 | Classification scheme named |  | 15 | 15 | 0 | 776 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 22 | 22 | 0 | 769 |  |
| COD-06 | Dates are valid | yes | 27 | 25 | 2 | 764 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 219 | 217 | 2 | 572 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 217 | 217 | 0 | 574 |  |
| NUM-04 | Magnitude in a plausible range |  | 264 | 264 | 0 | 527 |  |
| NUM-05 | Counts are whole numbers | yes | 35 | 35 | 0 | 756 |  |
| NUM-06 | Percentages in range | yes | 39 | 39 | 0 | 752 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 12 | 12 | 0 | 779 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 9 | 7 | 2 | 782 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 19 | 19 | 0 | 772 |  |
| NUM-11 | STI paid not above its maximum |  | 15 | 13 | 2 | 776 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 174 | 172 | 2 | 617 | currency N the role's other amounts DKK |
| NUM-13 | FTE not above headcount |  | 5 | 4 | 1 | 786 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 9 | 9 | 0 | 782 |  |
| DER-06 | Derived value shows its formula |  | 39 | 39 | 0 | 752 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 33 | 32 | 1 | 758 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 33 | 25 | 8 | 758 | parts add up to N stated N |

## Fill rate

Company fields: 466 of 779 filled (60%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 0 | 19 |
| staff_by_segment | 1 | 19 |
| staff_by_country | 2 | 19 |
| revenue_by_segment | 3 | 19 |
| revenue_by_country | 4 | 19 |
| shareholding_requirement | 6 | 19 |
| exchange_segment | 7 | 19 |
| share_price | 7 | 19 |
| market_cap_band | 7 | 19 |
| other_names | 9 | 19 |
| headcount | 9 | 19 |
| controlling_owner_name | 9 | 19 |
| ebitda | 10 | 19 |
| fte | 10 | 19 |
| lei | 11 | 19 |
| isin | 11 | 19 |
| listing_date | 11 | 19 |
| ticker | 12 | 19 |
| largest_holders | 12 | 19 |
| pe_stake_5pct | 12 | 19 |
| pension_type | 12 | 19 |
| accounting_basis | 13 | 19 |
| revenue | 14 | 19 |
| total_assets | 14 | 19 |
| shares_outstanding | 14 | 19 |
| ultimate_parent | 14 | 19 |
| benefits | 14 | 19 |
| business_id | 15 | 19 |
| exchange | 15 | 19 |
| listing_status | 15 | 19 |
| website | 15 | 19 |
| sector_code | 15 | 19 |
| sub_sector | 15 | 19 |
| fiscal_year | 15 | 19 |
| controlling_owner | 15 | 19 |
| ownership_type | 15 | 19 |
| fiscal_year_end | 16 | 19 |
| reporting_currency | 16 | 19 |
| legal_name | 17 | 19 |
| country_code | 17 | 19 |
| head_office_city | 17 | 19 |

Pay fields, over 44 executive roles:

| Field | Filled |
|---|---|
| base_salary | 40 (91%) |
| sti_paid | 28 (64%) |
| sti_target | 3 (7%) |
| sti_max | 17 (39%) |
| lti_vested | 3 (7%) |
| lti_granted | 16 (36%) |
| lti_target | 3 (7%) |
| lti_max | 6 (14%) |
| benefits_value | 24 (55%) |
| pension_contribution | 33 (75%) |
| total_remuneration | 37 (84%) |

## Failed values (59)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| addtech-nordic-ab | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | largest_holders |  | Tisenhult Invest 15.8%; Hedeli | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | listing_date |  | 2001-09 | Fail (hard) | COD-06: not a year or a date |
| addtech-nordic-ab | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| arzneiwerk-ag-vida | revenue |  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| arzneiwerk-ag-vida | total_assets |  | 1000 | Fail (hard) | CORE-03: quote not in the source text |
| atlantic-petroleum | benefits_value | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlantic-petroleum | sti_paid | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; XF-02: parts add up to 2,855,610, stated 3,028,977 |
| chill-brands-group-plc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chill-brands-group-plc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chill-brands-group-plc | revenue_by_country |  | US Operations: 19741; UK Opera | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 555,749 vs 1,908,020 (70.9% apart) |
| endeavour-mining-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner_name |  | La Mancha | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | fte |  | 5659 | Fail (hard) | CORE-02: 5659 not in the quote |
| endeavour-mining-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | revenue_by_segment |  | Ity Mine: 838.1; Houndé Mine:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Other leading executives | 5 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Övriga ledande befattningshava | 5 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | isin |  | SE0016785786 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | pension_type |  | premiebaserad pensionslösning | Fail (hard) | CORE-03: quote not in the source text |
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 4094000 | Fail (hard) | CORE-02: 4094 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3325000 | Fail (hard) | CORE-02: 3325 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 293000 | Fail (hard) | CORE-02: 293 not in the quote; CORE-04: no period_end |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 266000 | Fail (hard) | CORE-02: 266 not in the quote; CORE-04: no period_end |
| jinhui-shipping | benefits |  | medical insurance and contribu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | controlling_owner_name |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-02: not in the quote: company limited |
| jinhui-shipping | exchange |  | Oslo Stock Exchange (Euronext  | Fail (hard) | COD-01: 'Oslo Stock Exchange (Euronext Oslo Børs)' matches no ISO 10383 exchange |
| jinhui-shipping | largest_holders |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | pay_currency | Executive Director (Ng Siu Fai | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ng Kam Wah | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ng Ki Hung | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pay_currency | Executive Director (Ho Suk Lin | USD | Fail | CORE-04: no period_end |
| jinhui-shipping | pe_stake_5pct |  | no | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | ultimate_parent |  | Jinhui Holdings Company Limite | Fail (hard) | CORE-02: not in the quote: company limited |
| ostasiatiske | ebitda |  | -2500000 | Fail (hard) | CORE-02: -2.5 not in the quote |
| ostasiatiske | exchange |  | NASDAQ OMX Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ OMX Copenhagen A/S' matches no ISO 10383 exchange |
| ostasiatiske | sti_paid | CEO (Kresten M. Valdal) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| ostasiatiske | total_assets |  | 32700000 | Fail (hard) | CORE-02: 32.7 not in the quote |
| revolutionrace | staff_by_country |  | Sweden: 160 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 160 vs 170 (5.9% apart) |
| revolutionrace | sub_sector |  | Our driving force is to develo | Fail (hard) | CORE-03: quote not in the source text |
| s-d-standard-etc | controlling_owner_name |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-d-standard-etc | share_price |  | 1.688 | Fail (hard) | CORE-02: 1.688 not in the quote |
| s-d-standard-etc | ultimate_parent |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| sed-energy | pay_currency | Key management personnel | USD | Fail | CORE-04: no period_end |
| sed-energy | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
| uie | listing_date |  | 1983-05 | Fail (hard) | COD-06: not a year or a date |
| uie | share_price |  | 386.5 | Fail (hard) | CORE-03: quote not in the source text |
| uie | sti_max | Managing Director | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| voss-veksel-landmandsbank | fte |  | 28.4 | Fail (hard) | CORE-02: 28.4 not in the quote |
| voss-veksel-landmandsbank | revenue |  | 197537000 | Fail (hard) | CORE-03: quote not in the source text |
