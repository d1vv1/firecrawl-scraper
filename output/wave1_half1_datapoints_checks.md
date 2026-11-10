# Output checks: wave1_half1_datapoints.csv

99 companies, 5055 filled values checked (2026-11-10, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 4293 (85%) |
| Review | 319 (6%) |
| Fail | 64 (1%) |
| Fail (hard) | 379 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 608 | 605 | 0 | 0 | 3 |
| Listing and market | 467 | 451 | 0 | 0 | 16 |
| Sector | 167 | 164 | 0 | 0 | 3 |
| Reporting basis | 318 | 317 | 0 | 0 | 1 |
| Financials | 329 | 276 | 23 | 0 | 30 |
| Workforce | 102 | 73 | 11 | 0 | 18 |
| Ownership and control | 345 | 334 | 0 | 0 | 11 |
| Segment and geography | 140 | 86 | 23 | 9 | 22 |
| Pay policy | 209 | 194 | 0 | 0 | 15 |
| Role and disclosure | 678 | 571 | 5 | 55 | 47 |
| Pay: fixed | 624 | 451 | 97 | 0 | 76 |
| Pay: STI | 443 | 342 | 65 | 0 | 36 |
| Pay: LTI | 361 | 262 | 34 | 0 | 65 |
| Pay: total | 264 | 167 | 61 | 0 | 36 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 5055 | 5051 | 4 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 2201 | 2034 | 167 | 2854 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 3465 | 3265 | 200 | 1590 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 2851 | 2478 | 373 | 2204 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 5055 | 5053 | 2 | 0 | period_end 'N December' is not a date |
| COD-01 | Value in its code list or closed set | yes | 1661 | 1658 | 3 | 3394 | 'Vienna' matches no ISO N exchange |
| COD-02 | Classification scheme named |  | 84 | 84 | 0 | 4971 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 177 | 177 | 0 | 4878 |  |
| COD-06 | Dates are valid | yes | 131 | 126 | 5 | 4924 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1551 | 1519 | 32 | 3504 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1436 | 1436 | 0 | 3619 |  |
| NUM-04 | Magnitude in a plausible range |  | 1757 | 1750 | 7 | 3298 | Ne+N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 153 | 153 | 0 | 4902 |  |
| NUM-06 | Percentages in range | yes | 335 | 335 | 0 | 4720 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 61 | 60 | 1 | 4994 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 134 | 99 | 35 | 4921 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 224 | 224 | 0 | 4831 |  |
| NUM-11 | STI paid not above its maximum |  | 111 | 109 | 2 | 4944 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1292 | 1268 | 24 | 3763 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 38 | 33 | 5 | 5017 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 38 | 38 | 0 | 5017 |  |
| DER-06 | Derived value shows its formula |  | 175 | 175 | 0 | 4880 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 222 | 213 | 9 | 4833 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 222 | 181 | 41 | 4833 | parts add up to N stated N |

## Fill rate

Company fields: 2685 of 4059 filled (66%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 9 | 99 |
| staff_by_segment | 17 | 99 |
| staff_by_country | 25 | 99 |
| market_cap_band | 27 | 99 |
| share_price | 37 | 99 |
| controlling_owner_name | 39 | 99 |
| revenue_by_country | 44 | 99 |
| exchange_segment | 45 | 99 |
| listing_date | 49 | 99 |
| headcount | 49 | 99 |
| shareholding_requirement | 50 | 99 |
| fte | 53 | 99 |
| other_names | 54 | 99 |
| revenue_by_segment | 54 | 99 |
| pe_stake_5pct | 56 | 99 |
| controlling_owner | 59 | 99 |
| ownership_type | 59 | 99 |
| largest_holders | 61 | 99 |
| ebitda | 66 | 99 |
| shares_outstanding | 70 | 99 |
| ultimate_parent | 71 | 99 |
| accounting_basis | 76 | 99 |
| fiscal_year | 77 | 99 |
| revenue | 78 | 99 |
| total_assets | 78 | 99 |
| benefits | 79 | 99 |
| isin | 80 | 99 |
| pension_type | 80 | 99 |
| fiscal_year_end | 82 | 99 |
| sub_sector | 83 | 99 |
| reporting_currency | 83 | 99 |
| sector_code | 84 | 99 |
| ticker | 85 | 99 |
| website | 85 | 99 |
| lei | 88 | 99 |
| exchange | 90 | 99 |
| listing_status | 91 | 99 |
| legal_name | 93 | 99 |
| business_id | 93 | 99 |
| country_code | 93 | 99 |
| head_office_city | 93 | 99 |

Pay fields, over 288 executive roles:

| Field | Filled |
|---|---|
| base_salary | 241 (84%) |
| sti_paid | 205 (71%) |
| sti_target | 82 (28%) |
| sti_max | 156 (54%) |
| lti_vested | 89 (31%) |
| lti_granted | 135 (47%) |
| lti_target | 44 (15%) |
| lti_max | 93 (32%) |
| benefits_value | 180 (62%) |
| pension_contribution | 203 (70%) |
| total_remuneration | 264 (92%) |

## Failed values (443)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | lti_vested | CEO | 497000 | Fail (hard) | CORE-02: 497 not in the quote |
| aberdeen-group-plc | sti_paid | CEO | 1550000 | Fail (hard) | CORE-02: 1550 not in the quote |
| aberdeen-group-plc | sti_paid | Chief Financial Officer | 258000 | Fail (hard) | CORE-02: 258 not in the quote |
| addex-therapeutics-ltd | lti_granted | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | lti_granted | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | sti_paid | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Human Resources, People | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vertriebsvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Sales (bis 31. Oktober  | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Operations (bis 10. Aug | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender (bis 30. | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand (bis 11. Mai 20 | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pension_type |  | For board members appointed be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| adidas-ag-na-o-n | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| admiral-group-plc | listing_date |  | 2004-09 | Fail (hard) | CORE-02: not in the quote: 2004; CORE-03: the run did not find the full quote (the note keeps only its start); COD-06: not a year or a date |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| aep-plantations-plc | pension_contribution | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aep-plantations-plc | sti_paid | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aevis-victoria-sa | aggregate_headcount | Other Members of Senior Manage | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aevis-victoria-sa | base_salary | Other Members of Senior Manage | 1202900 | Fail (hard) | CORE-02: 1202.9 not in the quote |
| aevis-victoria-sa | ebitda |  | 72446000 | Fail (hard) | CORE-02: 72446 not in the quote |
| aevis-victoria-sa | fte |  | 4870 | Fail (hard) | CORE-02: 4870 not in the quote |
| aevis-victoria-sa | revenue |  | 1208366000 | Fail (hard) | CORE-02: 1208366 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | total_assets |  | 1905326000 | Fail (hard) | CORE-02: 1905326 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | total_remuneration | Executive Chairman (as of 21.0 | 1250600 | Fail (hard) | CORE-02: 1250.6 not in the quote |
| aevis-victoria-sa | total_remuneration | Other Members of Senior Manage | 2098600 | Fail (hard) | CORE-02: 2098.6 not in the quote |
| agilyx | exchange |  | OSE | Fail (hard) | COD-01: 'OSE' matches no ISO 10383 exchange |
| agilyx | revenue_by_country |  | Europe: 544402; USA: 255044; A | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| agilyx | revenue_by_segment |  | Cyclyx: 16574621; Agilyx: 1214 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 17,789,146 vs 1,214,525 (1364.7% apart) |
| airtel-africa-plc | accounting_basis |  | International Financial Report | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | benefits_value | Former CFO (until 9 July 2025) | 55000 | Fail (hard) | CORE-02: 55 not in the quote |
| airtel-africa-plc | exchange_segment |  | premium listing segment | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | staff_by_segment |  | Executive management: 174; Man | Fail | CORE-04: no period_end; NUM-08: adds up to 4,132 vs 11,520 (64.1% apart) |
| airtel-africa-plc | sub_sector |  | the provision of telecommunica | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | ultimate_parent |  | Bharti Enterprises (Holding) P | Fail (hard) | CORE-03: quote not in the source text |
| alfa-financial-software-holdings-plc | base_salary | Executive Chairman | 29000 | Fail (hard) | CORE-02: 29000 not in the quote |
| alfa-financial-software-holdings-plc | base_salary | CEO | 29000 | Fail (hard) | CORE-02: 29000 not in the quote |
| alfa-financial-software-holdings-plc | base_salary | CFO | 310000 | Fail (hard) | CORE-02: 310000 not in the quote |
| alfa-financial-software-holdings-plc | base_salary | COO | 250000 | Fail (hard) | CORE-02: 250000 not in the quote |
| alfa-financial-software-holdings-plc | benefits_value | Executive Chairman | 1000 | Fail (hard) | CORE-02: 1000 not in the quote |
| alfa-financial-software-holdings-plc | benefits_value | CEO | 3000 | Fail (hard) | CORE-02: 3000 not in the quote |
| alfa-financial-software-holdings-plc | benefits_value | CFO | 3000 | Fail (hard) | CORE-02: 3000 not in the quote |
| alfa-financial-software-holdings-plc | benefits_value | COO | 3000 | Fail (hard) | CORE-02: 3000 not in the quote |
| alfa-financial-software-holdings-plc | lti_vested | CFO | 528000 | Fail (hard) | CORE-02: 528000 not in the quote |
| alfa-financial-software-holdings-plc | lti_vested | COO | 281000 | Fail (hard) | CORE-02: 281000 not in the quote |
| alfa-financial-software-holdings-plc | pension_contribution | CFO | 18000 | Fail (hard) | CORE-02: 18000 not in the quote |
| alfa-financial-software-holdings-plc | pension_contribution | COO | 15000 | Fail (hard) | CORE-02: 15000 not in the quote |
| alfa-financial-software-holdings-plc | revenue_by_segment |  | Subscription: 43.6; Software E | Fail (hard) | CORE-03: quote not in the source text |
| alfa-financial-software-holdings-plc | sti_paid | CFO | 288000 | Fail (hard) | CORE-02: 288000 not in the quote |
| alfa-financial-software-holdings-plc | sti_paid | COO | 228000 | Fail (hard) | CORE-02: 228000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | Executive Chairman | 30000 | Fail (hard) | CORE-02: 30000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | CEO | 32000 | Fail (hard) | CORE-02: 32000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | CFO | 1147000 | Fail (hard) | CORE-02: 1147000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | COO | 777000 | Fail (hard) | CORE-02: 777000 not in the quote |
| alkemy-capital-investments-plc | fte |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| alkemy-capital-investments-plc | lti_granted | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | pension_contribution | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | sti_paid | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| allreal-holding-ag | ebitda |  | 310500000 | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | lti_target | Other members of Group Managem | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | staff_by_segment |  | Real Estate: 50 | Fail | CORE-04: no period_end; NUM-08: adds up to 50 vs 224 (77.7% apart) |
| altyngold-plc | benefits |  | Health insurance for the Execu | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Executive Director (Sanzhar As | individual | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Chief Financial Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| amigo-resources-plc | total_assets |  | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | share_price |  | 0.0208 | Fail (hard) | CORE-03: quote not in the source text |
| amrize-ltd | benefits |  | deferred compensation plan, 40 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | lti_granted | Chief Executive Officer (23 Ju | 9942122 | Fail (hard) | CORE-02: 9942122 not in the quote |
| amrize-ltd | lti_granted | Other Members of Executive Man | 12411396 | Fail (hard) | CORE-02: 12411396 not in the quote |
| amrize-ltd | pension_type |  | defined benefit (cash balance  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| amrize-ltd | sub_sector |  | The Company is organized into  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| antofagasta-plc | headcount |  | 8457 | Fail (hard) | CORE-02: 8457 not in the quote |
| antofagasta-plc | listing_date |  | 1888 | Fail (hard) | CORE-02: not in the quote: 1888; COD-06: not a year or a date |
| antofagasta-plc | staff_by_country |  | Chile: 6053; United Kingdom: 5 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,062 vs 8,457 (28.3% apart) |
| ao-world-plc | fte |  | 2892 | Fail (hard) | CORE-03: quote not in the source text |
| aptitude-software-group-plc | fte |  | 359 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 359 above headcount 317 |
| aptitude-software-group-plc | lti_vested | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aptitude-software-group-plc | revenue_by_country |  | United Kingdom: 10586; Rest of | Fail (hard) | CORE-03: quote not in the source text |
| aptitude-software-group-plc | staff_by_country |  | United Kingdom: 102; Rest of W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 359 vs 317 (13.2% apart) |
| ashmore-group-plc | listing_date |  | 2006 | Fail (hard) | CORE-02: not in the quote: 2006 |
| ashmore-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| associated-british-foods-plc | largest_holders |  | Wittington Investments Limited | Fail (hard) | NUM-07: holdings add up to 121.6% |
| associated-british-foods-plc | lti_granted | Chief Executive | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| associated-british-foods-plc | lti_granted | Finance Director (interim CEO  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| aston-martin-lagonda-global-holdings-plc | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | total_remuneration | Executive Director | 1000 | Fail (hard) | XF-01: parts add up to 3,000, more than the stated 1,000; XF-02: parts add up to 3,000, stated 1,000 |
| atalaya-mining-copper-s-a | fte |  | 509 | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | headcount |  | 518 | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | role_disclosure | Chief Financial Officer (PDMR) | individual | Fail (hard) | CORE-03: quote not in the source text |
| atlantic-petroleum | benefits_value | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlantic-petroleum | pay_currency | Managing Director – CEO | DKK | Fail | CORE-04: no period_end |
| atlantic-petroleum | sti_paid | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlas-metals-group-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| atlas-metals-group-plc | website |  | atlasmetalsgroup.com | Fail (hard) | CORE-02: not in the quote: atlasmetalsgroup com |
| austriacard-holdings-ag | ebitda |  | 51773000 | Fail (hard) | CORE-03: quote not in the source text |
| austriacard-holdings-ag | staff_by_country |  | Romania: 1346 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,346 vs 2,360 (43.0% apart) |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 289,459, more than the stated 278,255; XF-02: parts add up to 289,459, stated 278,255 |
| autotrader-group-plc | shareholding_requirement |  | 200% of salary in-post; 200% o | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| avolta-ag | base_salary | Other members of Global Execut | 6297100 | Fail (hard) | CORE-02: 6297.1 not in the quote |
| avolta-ag | lti_granted | Other members of Global Execut | 5772800 | Fail (hard) | CORE-02: 5772.8 not in the quote |
| avolta-ag | pension_contribution | Other members of Global Execut | 1310800 | Fail (hard) | CORE-02: 1310.8 not in the quote |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: quote on page 207, link says page 206 |
| avolta-ag | sti_paid | Other members of Global Execut | 7231600 | Fail (hard) | CORE-02: 7231.6 not in the quote |
| avolta-ag | total_remuneration | Other members of Global Execut | 21103400 | Fail (hard) | CORE-02: 21103.4 not in the quote |
| avon-technologies-plc | fte |  | 911 | Fail (hard) | CORE-03: quote not in the source text |
| avon-technologies-plc | lti_granted | CEO | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | revenue_by_segment |  | Avon Protection: 168.8; Team W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| avon-technologies-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| avon-technologies-plc | total_assets |  | 314800000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | base_salary | Deputy Chief Executive | 108000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | benefits_value | Deputy Chief Executive | 21000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | pension_contribution | Deputy Chief Executive | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| bachem-holding-ag | lti_granted | Rest of the Corporate Executiv | 261000 | Fail (hard) | CORE-02: 261 not in the quote |
| bachem-holding-ag | pension_contribution | Rest of the Corporate Executiv | 274000 | Fail (hard) | CORE-02: 274 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | sti_paid | CEO | 247000 | Fail (hard) | CORE-02: 247 not in the quote |
| bachem-holding-ag | sti_paid | Corporate Executive Committee | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| balfour-beatty-plc | pension_contribution | Former Group Chief Executive ( | 43183 | Fail (hard) | CORE-03: quote not in the source text |
| balfour-beatty-plc | revenue_by_country |  | United Kingdom: 4778; United S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | revenue_by_segment |  | Construction Services: 8711; S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| balfour-beatty-plc | sti_target | Group Chief Executive (appoint | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Executive Director | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Former Group Chief Executive ( | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| baltic-classifieds-group-plc | ebitda |  | 68626000 | Fail (hard) | CORE-02: 68626 not in the quote |
| baltic-classifieds-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: quote not in the source text |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Chief Executive Officer | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Other members of the managemen | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_type |  | defined benefit plan, collecti | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; CORE-04: no period_end; XF-02: parts add up to 2,855,610, stated 3,028,977 |
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 25,605 (29.0% apart) |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (Grita  | 1705000 | Fail (hard) | CORE-02: 1705 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (bis 30 | 393000 | Fail (hard) | CORE-02: 393 not in the quote |
| beiersdorf-ag-o-n | sti_target | Mitglied des Vorstands (bis 30 | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| bell-food-group-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| bell-food-group-ag | pay_currency | Übrige Mitglieder der Gruppenl | CHF | Fail | CORE-04: no period_end |
| berkeley-group-holdings-the-plc | lti_granted | Executive Chair | 400 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CEO | 250 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CFO (from 29 September 2025) | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| blencowe-resources-plc | aggregate_headcount | Key management personnel (excl | 2 | Fail (hard) | CORE-03: quote not in the source text |
| blencowe-resources-plc | headcount |  | 2 | Fail (hard) | CORE-02: 2 not in the quote |
| blencowe-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bodycote-plc | base_salary | CEO | 640000 | Fail (hard) | CORE-02: 640000 not in the quote |
| bodycote-plc | base_salary | CFO | 537000 | Fail (hard) | CORE-02: 537000 not in the quote |
| bodycote-plc | benefits_value | CEO | 19000 | Fail (hard) | CORE-02: 19000 not in the quote |
| bodycote-plc | benefits_value | CFO | 16000 | Fail (hard) | CORE-02: 16000 not in the quote |
| bodycote-plc | pension_contribution | CEO | 64000 | Fail (hard) | CORE-02: 64000 not in the quote |
| bodycote-plc | pension_contribution | CFO | 54000 | Fail (hard) | CORE-02: 54000 not in the quote |
| bodycote-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | shareholding_requirement |  | 200% of salary during employme | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | sti_paid | CEO | 399000000 | Fail (hard) | CORE-02: 399000 not in the quote; NUM-11: paid 62344% of base, maximum 175% |
| bodycote-plc | sti_paid | CFO | 293000000 | Fail (hard) | CORE-02: 293000 not in the quote; NUM-11: paid 54562% of base, maximum 150% |
| bodycote-plc | total_remuneration | CEO | 1122000 | Fail (hard) | CORE-02: 1122000 not in the quote; XF-01: parts add up to 399,723,000, more than the stated 1,122,000; XF-02: parts add up to 399,723,000, stated 1,122,000 |
| bodycote-plc | total_remuneration | CFO | 900000000 | Fail (hard) | CORE-02: 900000 not in the quote; XF-02: parts add up to 293,752,195, stated 900,000,000 |
| boot-henry-plc | role_disclosure | Other key management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | revenue |  | 100000000 | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-02: 2.23 not in the quote; CORE-03: quote not in the source text |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: quote not in the source text |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| brooks-macdonald-group-plc | lti_granted | CEO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| brooks-macdonald-group-plc | lti_granted | CFO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bt-group-plc | fte |  | 81600 | Fail (hard) | CORE-02: 81.6 not in the quote |
| bt-group-plc | headcount |  | 77200 | Fail (hard) | CORE-02: 77.2 not in the quote |
| bt-group-plc | lti_granted | Executive Director (Allison Ki | 2803899 | Fail (hard) | CORE-02: 2803899 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | lti_granted | Executive Director (Simon Lowt | 2057634 | Fail (hard) | CORE-02: 2057634 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | sti_paid | Executive Director (Allison Ki | 1081000 | Fail (hard) | CORE-02: 1081 not in the quote |
| bt-group-plc | sti_paid | Executive Director (Simon Lowt | 793000 | Fail (hard) | CORE-02: 793 not in the quote |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| bw-offshore-limited | role_disclosure | Senior Management Team | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bw-offshore-limited | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bytes-technology-group-plc | ebitda |  | 62732000 | Fail (hard) | CORE-02: 62732 not in the quote |
| bytes-technology-group-plc | lti_granted | CEO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bytes-technology-group-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| cab-payments-holdings-plc | revenue |  | 109400000 | Fail (hard) | CORE-03: quote not in the source text |
| cab-payments-holdings-plc | total_assets |  | 188000000 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | ebitda |  | 1258000 | Fail (hard) | CORE-02: 1.258 not in the quote; CORE-04: no period_end |
| cadogan-energy-solutions-plc | lti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | revenue_by_country |  | Ukraine: 7.55 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| cadogan-energy-solutions-plc | revenue_by_segment |  | Exploration and Production: 71 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| caledonia-investments-plc | benefits_value | Executive Director (J M B Cayz | 31000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | headcount |  | 82 | Fail (hard) | CORE-02: 82 not in the quote |
| caledonia-investments-plc | lti_vested | Executive Director (J M B Cayz | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | revenue_by_segment |  | Public Companies: 21.8; Privat | Fail | CORE-04: no period_end; NUM-08: adds up to 43,700,000 vs 166,000,000 (73.7% apart) |
| capital-limited | base_salary | Executive Chair | 528000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | CEO (until 8 March 2025) | 442000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | Executive Director | 417000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | Executive Chair | 95000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | CEO (until 8 March 2025) | 73000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | Executive Director | 49000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Chair | 722000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Director | 546000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | Executive Chair | 1345000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | CEO (until 8 March 2025) | 515000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | Executive Director | 1012000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | base_salary | Chief Executive Officer | 400000 | Fail (hard) | CORE-02: 400000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | base_salary | Chief Financial Officer (from  | 280000 | Fail (hard) | CORE-02: 280000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Executive Officer | 11000 | Fail (hard) | CORE-02: 11000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Financial Officer (from  | 12000 | Fail (hard) | CORE-02: 12000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | fte |  | 907 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Executive Officer | 149000 | Fail (hard) | CORE-02: 149000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Financial Officer (from  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Financial Officer (from  | 16000 | Fail (hard) | CORE-02: 16000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | revenue_by_country |  | United Kingdom: 8125; Rest of  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| carclo-plc | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | sti_paid | Chief Executive Officer | 180000 | Fail (hard) | CORE-02: 180000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | sti_paid | Chief Financial Officer (from  | 101000 | Fail (hard) | CORE-02: 101000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | total_remuneration | Chief Executive Officer | 740000 | Fail (hard) | CORE-02: 740000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | total_remuneration | Chief Financial Officer (from  | 409000 | Fail (hard) | CORE-02: 409000 not in the quote; CORE-03: quote not in the source text |
| cardiff-property-plc | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| cardiff-property-plc | total_remuneration | Chief Executive Officer | 182000 | Fail (hard) | XF-01: parts add up to 206,000, more than the stated 182,000; XF-02: parts add up to 206,000, stated 182,000 |
| centrica-plc | fte |  | 22066 | Fail (hard) | CORE-03: quote not in the source text |
| centrica-plc | listing_date |  | 1997-02-17 | Fail (hard) | CORE-02: not in the quote: 1997 |
| centrica-plc | lti_granted | Group Chief Executive | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| centrica-plc | lti_granted | Group Chief Financial Officer | 125 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| centrica-plc | share_price |  | 1.4065 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| close-brothers-group-plc | lti_granted | Chief Executive (from 10 Septe | 726000 | Fail (hard) | CORE-02: 726 not in the quote |
| cmb-tech-nv | base_salary | Management Board Members (excl | 1000000 | Fail (hard) | CORE-02: 1000000 not in the quote |
| cmb-tech-nv | benefits |  | Fringe benefits include health | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cmb-tech-nv | sti_paid | Management Board Members (excl | 250000 | Fail (hard) | CORE-02: 250000 not in the quote |
| cmc-markets-plc | ebitda |  | 117842 | Fail (hard) | CORE-02: 117.842 not in the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: quote not in the source text |
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
| commerzbank-ag | shareholding_requirement |  | Sämtliche Mitglieder des Vorst | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 3,511,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | stellvertretender Vorsitzender | 2917000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 2,453,000, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Group Human Resources & Group  | 2116000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,880,000, stated 2,116,000 |
| commerzbank-ag | total_remuneration | Segment Privat- und Unternehme | 2086000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,904,000, stated 2,086,000 |
| commerzbank-ag | total_remuneration | Chief Financial Officer (seit  | 1896000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,281,000, stated 1,896,000 |
| commerzbank-ag | total_remuneration | Chief Risk Officer (seit 1. Ja | 2113000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,500,000, stated 2,113,000 |
| commerzbank-ag | total_remuneration | Chief Operating Officer (seit  | 2312000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; XF-02: parts add up to 1,620,000, stated 2,312,000 |
| corem-property-d | benefits |  | company car, health insurance | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-d | pay_currency | Vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Vice vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| corem-property-d | sti_paid | Andra ledande befattningshavar | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote; CORE-04: no period_end |
| cranswick-plc | fte |  | 13033 | Fail (hard) | CORE-03: quote not in the source text |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | COD-06: not a year or a date |
| delticom-ag-na-o-n | share_price |  | 2.14 | Fail (hard) | CORE-02: 2.14 not in the quote; CORE-03: quote not in the source text |
| digia-oyj | aggregate_headcount | Other key personnel | 20 | Fail (hard) | CORE-03: quote not in the source text |
| digia-oyj | shareholding_requirement |  | participants have the chance t | Fail (hard) | CORE-03: quote not in the source text |
| erste-group-bank-ag | benefits |  | insurance benefits, other non- | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | exchange |  | Vienna | Fail (hard) | COD-01: 'Vienna' matches no ISO 10383 exchange |
| erste-group-bank-ag | listing_date |  | 1997-12-04 | Fail (hard) | CORE-02: not in the quote: 1997 |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 960000 | Fail (hard) | CORE-02: 960000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_vested | Chief Corporates and Markets O | 939970.49 | Fail (hard) | CORE-02: 939970.49 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Financial Officer | 939791.52 | Fail (hard) | CORE-02: 939791.52 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Risk Officer | 938922.19 | Fail (hard) | CORE-02: 938922.19 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Platform Officer / Chief | 463518.82 | Fail (hard) | CORE-02: 463518.82 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | other_names |  | Erste oesterreichische Spar-Ca | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | staff_by_country |  | Austria: 20111; Czechia: 10097 | Fail | CORE-04: no period_end; NUM-08: adds up to 49,024 vs 46,000 (6.6% apart) |
| fastpartner-d | base_salary | Other members of the Executive | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | base_salary | Other senior executives | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | pension_contribution | Other members of the Executive | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | pension_contribution | Other senior executives | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | share_price |  | 47.45 | Fail (hard) | CORE-03: quote not in the source text |
| fastpartner-d | sti_max | Other senior executives | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_paid | Other members of the Executive | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| fastpartner-d | sti_paid | Other senior executives | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flughafen-wien-ag | base_salary | Management Board | 1186800 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | base_salary | Key employees | 5002300 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | benefits_value | Management Board | 12200 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | benefits_value | Key employees | 41200 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | lti_granted | Management Board | 863200 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | pension_contribution | Management Board | 169600 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Supervisory Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Key employees | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | sti_paid | Management Board | 452200 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | sub_sector |  | The FWAG Group generates reven | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| flughafen-wien-ag | total_remuneration | Key employees | 5169200 | Fail (hard) | CORE-03: quote not in the source text |
| hermana-holding | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| hermana-holding | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| holand-og-setskog-sparebank | ebitda |  | 57700000 | Fail (hard) | CORE-02: 57.7 not in the quote |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (1) | individual | Fail (hard) | CORE-03: quote not in the source text |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (2) | individual | Fail (hard) | CORE-03: quote not in the source text |
| intea-fastigheter-d | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pension_contribution | Övriga ledande befattningshava | 1300000 | Fail (hard) | CORE-02: 1.3 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Verkställande direktör | 3800000 | Fail (hard) | CORE-02: 3.8 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| kesko-b | aggregate_headcount | Group Management Board | 7 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kesko-b | role_disclosure | Hallituksen jäsenet | aggregate | Fail (hard) | CORE-03: quote not in the source text |
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
| ostasiatiske | pay_currency | CEO (Kresten M. Valdal) | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | pay_currency | Direktionen | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | pay_currency | CEO (Martin Thaysen) | DKK | Fail | CORE-04: no period_end |
| ostasiatiske | sti_paid | CEO (Kresten M. Valdal) | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| revolutionrace | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| revolutionrace | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Chief Financial Officer | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Chief Operations Officer | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | General Manager | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Subsidiary employee | USD | Fail | CORE-04: no period_end |
| s-d-standard-etc | pay_currency | Total remuneration executive m | USD | Fail | CORE-04: no period_end |
| sagax-d | base_salary | Other members of Group managem | 5300000 | Fail (hard) | CORE-02: 5.3 not in the quote |
| seb-a | benefits_value | CEO | 385000 | Fail (hard) | CORE-02: 385 not in the quote |
| seb-a | benefits_value | Deputy CEO (Mats Torstendahl) | 236000 | Fail (hard) | CORE-02: 236 not in the quote |
| seb-a | benefits_value | Deputy CEO (Jonas Ahlström) | 205000 | Fail (hard) | CORE-02: 205 not in the quote |
| seb-a | benefits_value | Other members of the Group Exe | 2171847 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | lti_granted | CEO | 5875000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | lti_vested | CEO | 16884000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | pension_contribution | CEO | 5250000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | pension_contribution | Deputy CEO (Mats Torstendahl) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | pension_contribution | Deputy CEO (Jonas Ahlström) | 1806000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| seb-a | total_remuneration | CEO | 37519000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | total_remuneration | Deputy CEO (Mats Torstendahl) | 8887000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | total_remuneration | Deputy CEO (Jonas Ahlström) | 12911000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-a | total_remuneration | Other members of the Group Exe | 85984864 | Fail (hard) | XF-01: parts add up to 105,243,201, more than the stated 85,984,864; XF-02: parts add up to 105,243,201, stated 85,984,864 |
| sentia | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| sentia | controlling_owner_name |  | Ratos AB | Fail (hard) | CORE-03: quote not in the source text |
| sentia | largest_holders |  | Ratos AB 39% | Fail (hard) | CORE-03: quote not in the source text |
| sentia | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| sentia | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_country |  | Norge: 9404; Sverige: 2369 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_segment |  | HENT: 9404; Sentia Sverige: 23 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | share_price |  | 62.99 | Fail (hard) | CORE-02: 62.99 not in the quote |
| sentia | staff_by_segment |  | HENT: 1338; Sentia Sverige: 17 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,516 vs 6 (25166.7% apart) |
| sparebank-1-helgeland | benefits_value | Administrerende direktør | 274607 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | benefits_value | Finansdirektør | 83294 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | benefits_value | Direktør risikostyring | 95655 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | benefits_value | Direktør forretningsutvikling | 96803 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | pension_contribution | Administrerende direktør | 305424 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | pension_contribution | Finansdirektør | 275351 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | pension_contribution | Direktør risikostyring | 279012 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | pension_contribution | Direktør forretningsutvikling | 273096 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | revenue_by_segment |  | Retail division: 3198; Corpora | Fail | CORE-04: no period_end; NUM-08: adds up to 6,786,000,000 vs 14,040,000,000 (51.7% apart) |
| sparebank-1-helgeland | role_disclosure | Administrerende direktør | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Finansdirektør | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Direktør risikostyring | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Direktør forretningsutvikling | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Direktør bedriftsmarked | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Tidligere adm.dir (Lisbeth Flå | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | role_disclosure | Tidligere adm dir. (Arnt Krane | individual | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-helgeland | sti_paid | Direktør risikostyring | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | benefits_value | Other members of the Group Lea | 250000 | Fail (hard) | CORE-02: 250 not in the quote |
| stora-enso-r | controlling_owner |  | state | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | controlling_owner_name |  | Solidium Oy | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | lti_granted | President and Chief Executive  | 380200 | Fail (hard) | CORE-02: 380200 not in the quote |
| stora-enso-r | other_names |  | FuraCore AB; Ingerois Oy | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | ownership_type |  | state_owned | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | pension_contribution | Other members of the Group Lea | 1445000 | Fail (hard) | CORE-02: 1445 not in the quote |
| stora-enso-r | revenue_by_country |  | Austria: 298; Baltic States: 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-r | revenue_by_segment |  | Packaging Materials: 4255; Pac | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | role_disclosure | Other members of the Group Lea | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | benefits |  | Health insurance plan for its  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| tekna-holding | controlling_owner_name |  | Arendals Fossekompani ASA | Fail (hard) | CORE-02: not in the quote: arendals fossekompani asa |
| tekna-holding | lti_granted | CEO (2025 - ) | 1000000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | EVP - Materials, Managing dire | 200000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | CFO Tekna Holding Canada Inc ( | 200000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | Executive Leadership Team | 2000000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_vested | EVP - Materials, Managing dire | 46667 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_vested | Executive Leadership Team | 186667 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | revenue_by_country |  | America: 19803; Europe: 10036; | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | revenue_by_segment |  | Systems & Equipment: 6431; Mat | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | role_disclosure | CFO (2023 - ) | individual | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | role_disclosure | CEO (2014 - April 27, 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | role_disclosure | VP Operations (2020 - 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
