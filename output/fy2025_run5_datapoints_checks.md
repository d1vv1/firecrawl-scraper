# Output checks: fy2025_run5_datapoints.csv

31 companies, 1049 filled values checked (2026-11-11, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 829 (79%) |
| Review | 121 (12%) |
| Fail | 22 (2%) |
| Fail (hard) | 77 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 167 | 166 | 0 | 0 | 1 |
| Listing and market | 128 | 123 | 0 | 0 | 5 |
| Sector | 39 | 38 | 0 | 0 | 1 |
| Reporting basis | 48 | 48 | 0 | 0 | 0 |
| Financials | 44 | 37 | 5 | 0 | 2 |
| Workforce | 15 | 7 | 3 | 0 | 5 |
| Ownership and control | 80 | 77 | 0 | 0 | 3 |
| Segment and geography | 11 | 7 | 1 | 0 | 3 |
| Pay policy | 36 | 29 | 0 | 0 | 7 |
| Role and disclosure | 155 | 117 | 2 | 22 | 14 |
| Pay: fixed | 128 | 76 | 40 | 0 | 12 |
| Pay: STI | 81 | 43 | 37 | 0 | 1 |
| Pay: LTI | 54 | 28 | 14 | 0 | 12 |
| Pay: total | 63 | 33 | 19 | 0 | 11 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 1049 | 1048 | 1 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 416 | 382 | 34 | 633 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 655 | 616 | 39 | 394 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 526 | 371 | 155 | 523 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 1049 | 1049 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 358 | 357 | 1 | 691 | 'Euronext' matches no ISO N exchange |
| COD-02 | Classification scheme named |  | 21 | 21 | 0 | 1028 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 51 | 51 | 0 | 998 |  |
| COD-06 | Dates are valid | yes | 27 | 26 | 1 | 1022 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 292 | 289 | 3 | 757 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 289 | 289 | 0 | 760 |  |
| NUM-04 | Magnitude in a plausible range |  | 326 | 324 | 2 | 723 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 30 | 30 | 0 | 1019 |  |
| NUM-06 | Percentages in range | yes | 29 | 29 | 0 | 1020 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 13 | 12 | 1 | 1036 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 11 | 10 | 1 | 1038 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 40 | 40 | 0 | 1009 |  |
| NUM-11 | STI paid not above its maximum |  | 11 | 11 | 0 | 1038 |  |
| NUM-12 | A role's amounts share currency and period |  | 262 | 260 | 2 | 787 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 4 | 4 | 0 | 1045 |  |
| DER-03 | Derived value recalculates | yes | 8 | 8 | 0 | 1041 |  |
| DER-06 | Derived value shows its formula |  | 44 | 44 | 0 | 1005 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 48 | 44 | 4 | 1001 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 48 | 37 | 11 | 1001 | parts add up to N stated N |

## Fill rate

Company fields: 568 of 1271 filled (45%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 1 | 31 |
| staff_by_segment | 1 | 31 |
| staff_by_country | 2 | 31 |
| fte | 4 | 31 |
| revenue_by_segment | 4 | 31 |
| revenue_by_country | 4 | 31 |
| ebitda | 6 | 31 |
| shareholding_requirement | 6 | 31 |
| revenue | 8 | 31 |
| total_assets | 8 | 31 |
| share_price | 8 | 31 |
| market_cap_band | 8 | 31 |
| controlling_owner_name | 8 | 31 |
| accounting_basis | 9 | 31 |
| exchange_segment | 10 | 31 |
| headcount | 11 | 31 |
| fiscal_year | 12 | 31 |
| controlling_owner | 12 | 31 |
| ownership_type | 12 | 31 |
| fiscal_year_end | 13 | 31 |
| largest_holders | 13 | 31 |
| pe_stake_5pct | 13 | 31 |
| listing_date | 14 | 31 |
| reporting_currency | 14 | 31 |
| shares_outstanding | 14 | 31 |
| benefits | 14 | 31 |
| pension_type | 16 | 31 |
| other_names | 17 | 31 |
| sub_sector | 18 | 31 |
| website | 19 | 31 |
| sector_code | 21 | 31 |
| ultimate_parent | 22 | 31 |
| isin | 24 | 31 |
| ticker | 24 | 31 |
| exchange | 24 | 31 |
| listing_status | 24 | 31 |
| legal_name | 26 | 31 |
| lei | 26 | 31 |
| business_id | 26 | 31 |
| country_code | 26 | 31 |
| head_office_city | 26 | 31 |

Pay fields, over 67 executive roles:

| Field | Filled |
|---|---|
| base_salary | 51 (76%) |
| sti_paid | 41 (61%) |
| sti_target | 16 (24%) |
| sti_max | 24 (36%) |
| lti_vested | 15 (22%) |
| lti_granted | 25 (37%) |
| lti_target | 7 (10%) |
| lti_max | 7 (10%) |
| benefits_value | 26 (39%) |
| pension_contribution | 51 (76%) |
| total_remuneration | 63 (94%) |

## Failed values (99)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
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
| alina-holdings-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| alpine-select-ag | benefits |  | fringe benefits, flat-rat allo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alpine-select-ag | fte |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| alpine-select-ag | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| arbonia-ag | pay_currency | Group Management | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| banque-cantonale-du-jura-sa | base_salary | Other members of Direction | 910240 | Fail (hard) | CORE-02: 910240 not in the quote; CORE-04: no period_end |
| banque-cantonale-du-jura-sa | benefits |  | representation expenses, favor | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| banque-cantonale-du-jura-sa | pay_currency | Directeur général | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pay_currency | Other members of Direction | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pension_contribution | Other members of Direction | 323953 | Fail (hard) | CORE-02: 323953 not in the quote; CORE-04: no period_end |
| banque-cantonale-du-jura-sa | sti_paid | Other members of Direction | 367500 | Fail (hard) | CORE-02: 367500 not in the quote; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Managemen | 605000 | Fail (hard) | CORE-02: 605000 not in the quote |
| basellandschaftliche-kantonalbank | pension_type |  | defined contribution, BLKB cov | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must acquire 2 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Managemen | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| bell-food-group-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| bell-food-group-ag | pay_currency | Übrige Mitglieder der Gruppenl | CHF | Fail | CORE-04: no period_end |
| bsf-enterprise-plc | largest_holders |  | GBF Nominees Limited 19.48%; B | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | lti_granted | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bsf-enterprise-plc | pension_contribution | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| bucher-industries-ag | shareholding_requirement |  | shares are subject to a lock-u | Fail (hard) | CORE-03: quote not in the source text |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| chesterfield-resources-plc | lti_granted | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| chesterfield-resources-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | base_salary | ehemaliger Vorsitzender (bis 3 | 481000 | Fail (hard) | CORE-02: 481 not in the quote; CORE-03: quote not in the source text |
| commerzbank-ag | benefits_value | Vorsitzende (seit 1. Oktober 2 | 228000 | Fail (hard) | CORE-02: 228 not in the quote; CORE-03: quote not in the source text |
| commerzbank-ag | benefits_value | Chief Operating Officer (seit  | 273000 | Fail (hard) | CORE-02: 273 not in the quote |
| commerzbank-ag | other_names |  | Commerz- und Disconto-Bank; Co | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | pension_contribution | ehemaliger Vorsitzender (bis 3 | 159000 | Fail (hard) | CORE-02: 159 not in the quote; CORE-03: quote not in the source text |
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
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 4094000 | Fail (hard) | CORE-02: 4094 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3325000 | Fail (hard) | CORE-02: 3325 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 293000 | Fail (hard) | CORE-02: 293 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 266000 | Fail (hard) | CORE-02: 266 not in the quote |
| k2a-knaust-andersson-pref | fte |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| k2a-knaust-andersson-pref | headcount |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| k2a-knaust-andersson-pref | share_price |  | 4.98 | Fail (hard) | CORE-02: 4.98 not in the quote |
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
| sed-energy | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
