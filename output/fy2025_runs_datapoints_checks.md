# Output checks: fy2025_runs_datapoints.csv

339 companies, 16282 filled values checked (2026-11-12, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 14492 (89%) |
| Review | 596 (4%) |
| Fail | 74 (0%) |
| Fail (hard) | 1120 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 1909 | 1899 | 0 | 0 | 10 |
| Listing and market | 1568 | 1521 | 0 | 0 | 47 |
| Sector | 563 | 551 | 0 | 0 | 12 |
| Reporting basis | 1178 | 1173 | 0 | 0 | 5 |
| Financials | 1131 | 935 | 98 | 1 | 97 |
| Workforce | 436 | 323 | 39 | 0 | 74 |
| Ownership and control | 1173 | 1100 | 0 | 0 | 73 |
| Segment and geography | 472 | 267 | 77 | 24 | 104 |
| Pay policy | 706 | 670 | 0 | 0 | 36 |
| Role and disclosure | 2079 | 1914 | 3 | 49 | 113 |
| Pay: fixed | 1932 | 1628 | 107 | 0 | 197 |
| Pay: STI | 1257 | 1069 | 81 | 0 | 107 |
| Pay: LTI | 1091 | 884 | 54 | 0 | 153 |
| Pay: total | 787 | 558 | 137 | 0 | 92 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 16282 | 16267 | 15 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 6973 | 6536 | 437 | 9309 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 11180 | 10581 | 599 | 5102 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 9017 | 8500 | 517 | 7265 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 16282 | 16279 | 3 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 5220 | 5191 | 29 | 11062 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 283 | 283 | 0 | 15999 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 562 | 562 | 0 | 15720 |  |
| COD-06 | Dates are valid | yes | 497 | 480 | 17 | 15785 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 4811 | 4758 | 53 | 11471 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 4446 | 4446 | 0 | 11836 |  |
| NUM-04 | Magnitude in a plausible range |  | 5605 | 5577 | 28 | 10677 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 599 | 596 | 3 | 15683 | not a whole number |
| NUM-06 | Percentages in range | yes | 965 | 964 | 1 | 15317 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 207 | 204 | 3 | 16075 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 467 | 353 | 114 | 15815 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 644 | 644 | 0 | 15638 |  |
| NUM-11 | STI paid not above its maximum |  | 292 | 280 | 12 | 15990 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 3916 | 3871 | 45 | 12366 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 194 | 176 | 18 | 16088 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 100 | 100 | 0 | 16182 |  |
| DER-06 | Derived value shows its formula |  | 658 | 658 | 0 | 15624 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 672 | 637 | 35 | 15610 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 672 | 520 | 152 | 15610 | parts add up to N stated N |

## Fill rate

Company fields: 9136 of 13899 filled (66%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 33 | 339 |
| staff_by_segment | 62 | 339 |
| staff_by_country | 88 | 339 |
| market_cap_band | 128 | 339 |
| controlling_owner_name | 137 | 339 |
| share_price | 143 | 339 |
| revenue_by_country | 150 | 339 |
| other_names | 164 | 339 |
| exchange_segment | 168 | 339 |
| shareholding_requirement | 169 | 339 |
| revenue_by_segment | 172 | 339 |
| listing_date | 177 | 339 |
| fte | 195 | 339 |
| pe_stake_5pct | 196 | 339 |
| largest_holders | 207 | 339 |
| ownership_type | 207 | 339 |
| controlling_owner | 208 | 339 |
| ultimate_parent | 218 | 339 |
| ebitda | 227 | 339 |
| shares_outstanding | 236 | 339 |
| headcount | 241 | 339 |
| isin | 255 | 339 |
| accounting_basis | 260 | 339 |
| revenue | 262 | 339 |
| total_assets | 263 | 339 |
| benefits | 263 | 339 |
| ticker | 265 | 339 |
| website | 269 | 339 |
| lei | 274 | 339 |
| pension_type | 274 | 339 |
| reporting_currency | 279 | 339 |
| sub_sector | 280 | 339 |
| sector_code | 283 | 339 |
| exchange | 287 | 339 |
| listing_status | 288 | 339 |
| business_id | 290 | 339 |
| legal_name | 293 | 339 |
| country_code | 293 | 339 |
| head_office_city | 293 | 339 |
| fiscal_year | 319 | 339 |
| fiscal_year_end | 320 | 339 |

Pay fields, over 863 executive roles:

| Field | Filled |
|---|---|
| base_salary | 739 (86%) |
| sti_paid | 610 (71%) |
| sti_target | 225 (26%) |
| sti_max | 422 (49%) |
| lti_vested | 299 (35%) |
| lti_granted | 345 (40%) |
| lti_target | 146 (17%) |
| lti_max | 301 (35%) |
| benefits_value | 582 (67%) |
| pension_contribution | 611 (71%) |
| total_remuneration | 787 (91%) |

## Failed values (1194)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 2invest-ag-bf4e0781 | base_salary | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| 2invest-ag-bf4e0781 | total_remuneration | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | lti_vested | CEO | 497000 | Fail (hard) | CORE-02: 497 not in the quote |
| aberdeen-group-plc | sti_paid | CEO | 1550000 | Fail (hard) | CORE-02: 1550 not in the quote |
| aberdeen-group-plc | sti_paid | Chief Financial Officer | 258000 | Fail (hard) | CORE-02: 258 not in the quote |
| acceler8-ventures-plc | ebitda |  | -172772 | Fail (hard) | CORE-02: -172772 not in the quote |
| accelleron-industries-ag | revenue_by_country |  | Asia, Middle East & Africa: 54 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| accelleron-industries-ag | staff_by_country |  | Switzerland: 1014; Asia & Midd | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| acg-metals-limited | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| acg-metals-limited | total_remuneration | Chairman & Chief Executive Off | 1256156 | Fail (hard) | XF-01: parts add up to 1,497,823, more than the stated 1,256,156; XF-02: parts add up to 1,497,823, stated 1,256,156 |
| addex-therapeutics-ltd | lti_granted | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | lti_granted | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | sti_paid | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addtech-nordic-ab | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | largest_holders |  | Tisenhult Invest 15.8%; Hedeli | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | listing_date |  | 2001-09 | Fail (hard) | COD-06: not a year or a date |
| addtech-nordic-ab | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| adecco-group-ag | revenue_by_country |  | France: 4558; Northern Europe: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 17,911,000,000 vs 23,138,000,000 (22.6% apart) |
| adecco-group-ag | revenue_by_segment |  | Adecco: 17908; Akkodis: 3565;  | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
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
| african-pioneer-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| agilyx | exchange |  | OSE | Fail (hard) | COD-01: 'OSE' matches no ISO 10383 exchange |
| agilyx | revenue_by_country |  | Europe: 544402; USA: 255044; A | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| agilyx | revenue_by_segment |  | Cyclyx: 16574621; Agilyx: 1214 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 17,789,146 vs 1,214,525 (1364.7% apart) |
| airtel-africa-plc | accounting_basis |  | International Financial Report | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | benefits_value | Former CFO (until 9 July 2025) | 55000 | Fail (hard) | CORE-02: 55 not in the quote |
| airtel-africa-plc | exchange_segment |  | premium listing segment | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | staff_by_segment |  | Executive management: 174; Man | Fail | CORE-04: no period_end; NUM-08: adds up to 4,132 vs 11,520 (64.1% apart) |
| airtel-africa-plc | sub_sector |  | the provision of telecommunica | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | ultimate_parent |  | Bharti Enterprises (Holding) P | Fail (hard) | CORE-03: quote not in the source text |
| airtel-mobile-commerce-n-v | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| airtel-mobile-commerce-n-v | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| alcon-inc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | lti_max | CEO | 1150 | Fail (hard) | NUM-06: 1150 % of base salary |
| alcon-inc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | revenue_by_country |  | United States: 4657; Switzerla | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| alina-holdings-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| alkemy-capital-investments-plc | fte |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| alkemy-capital-investments-plc | lti_granted | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | pension_contribution | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | sti_paid | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| allgeier-se-9971b49d | pension_type |  | defined benefit plans; defined | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| allreal-holding-ag | ebitda |  | 310500000 | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | lti_target | Other members of Group Managem | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | staff_by_segment |  | Real Estate: 50 | Fail | CORE-04: no period_end; NUM-08: adds up to 50 vs 224 (77.7% apart) |
| alpine-select-ag | benefits |  | fringe benefits, flat-rat allo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alpine-select-ag | fte |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| alpine-select-ag | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| also-holding-ag | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | controlling_owner_name |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | fte |  | 5156 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | headcount |  | 5157 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | largest_holders |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | benefits |  | Health insurance for the Execu | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Executive Director (Sanzhar As | individual | Fail (hard) | CORE-03: quote not in the source text |
| altyngold-plc | role_disclosure | Chief Financial Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| alvotech-sdb | accounting_basis |  | IFRS as adopted by the Europea | Fail (hard) | CORE-03: quote not in the source text |
| amaroq-ltd | pension_type |  | The Corporation does not opera | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amaroq-ltd | revenue |  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | total_assets |  | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amicorp-fs-uk-plc | fte |  | 172 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| apg-sga-sa | benefits_value | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| apg-sga-sa | pension_contribution | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| apg-sga-sa | pension_contribution | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| apg-sga-sa-8679206d | benefits_value | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| apg-sga-sa-8679206d | benefits_value | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| aptitude-software-group-plc | lti_vested | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aptitude-software-group-plc | revenue_by_country |  | United Kingdom: 10586; Rest of | Fail (hard) | CORE-03: quote not in the source text |
| aptitude-software-group-plc | staff_by_country |  | United Kingdom: 102; Rest of W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 359 vs 317 (13.2% apart) |
| arbonia-ag | base_salary | Other members of Group Managem | 628000 | Fail (hard) | CORE-02: 628 not in the quote |
| arbonia-ag | benefits_value | Other members of Group Managem | 40000 | Fail (hard) | CORE-02: 40 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_granted | Other members of Group Managem | 149000 | Fail (hard) | CORE-02: 149 not in the quote |
| arbonia-ag | pension_contribution | Other members of Group Managem | 147000 | Fail (hard) | CORE-02: 147 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | sti_paid | Other members of Group Managem | 542000 | Fail (hard) | CORE-02: 542 not in the quote |
| arbonia-ag | total_remuneration | Other members of Group Managem | 1507000 | Fail (hard) | CORE-02: 1507 not in the quote |
| aryzta-ag | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ebitda |  | 306900000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | revenue_by_country |  | Switzerland: 280.9; Germany: 6 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aryzta-ag | revenue_by_segment |  | ARYZTA Europe: 1977; ARYZTA Re | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| arzneiwerk-ag-vida | revenue |  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| arzneiwerk-ag-vida | total_assets |  | 1000 | Fail (hard) | CORE-03: quote not in the source text |
| asa-international-group-plc | listing_date |  | 2018 | Fail (hard) | CORE-02: not in the quote: 2018 |
| asa-international-group-plc | lti_vested | Deputy Chairperson and Special | 60 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| aseana-properties-limited | revenue_by_country |  | Malaysia: 14415 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ashmore-group-plc | listing_date |  | 2006 | Fail (hard) | CORE-02: not in the quote: 2006 |
| ashmore-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ashtead-technology-holdings-plc | fte |  | 649 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 649 above headcount 396 |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | benefits |  | flexible benefits allowance of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | listing_date |  | 2022-02 | Fail (hard) | COD-06: not a year or a date |
| asos-plc | lti_granted | CFO (appointed 1 July 2025) | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| asos-plc | pension_type |  | defined contribution, 5% of ba | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| associated-british-foods-plc | largest_holders |  | Wittington Investments Limited | Fail (hard) | NUM-07: holdings add up to 121.6% |
| associated-british-foods-plc | lti_granted | Chief Executive | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| associated-british-foods-plc | lti_granted | Finance Director (interim CEO  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| aston-martin-lagonda-global-holdings-plc | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | total_remuneration | Executive Director | 1000 | Fail (hard) | XF-01: parts add up to 3,000, more than the stated 1,000; XF-02: parts add up to 3,000, stated 1,000 |
| astrazeneca-plc | revenue_by_country |  | US: 25450; Emerging Markets: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 65,393,000,000 vs 58,739,000,000 (11.3% apart) |
| atalaya-mining-copper-s-a | fte |  | 509 | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | headcount |  | 518 | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | role_disclosure | Chief Financial Officer (PDMR) | individual | Fail (hard) | CORE-03: quote not in the source text |
| atlantic-petroleum | benefits_value | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlantic-petroleum | sti_paid | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlas-metals-group-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| atlas-metals-group-plc | website |  | atlasmetalsgroup.com | Fail (hard) | CORE-02: not in the quote: atlasmetalsgroup com |
| atoss-software-se | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | lti_max | Chief Executive Officer (CEO) | 120000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Chief Executive Officer (CEO) | 100000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Executive Board member (CFO) | 70000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Executive Board member (COO) | 85000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_contribution | Executive Board member (CFO) | 41616000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_contribution | Executive Board member (COO) | 54000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_type |  | defined benefits plan for CEO; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | sti_max | Chief Executive Officer (CEO) | 240000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_max | Executive Board member (CFO) | 210000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_max | Executive Board member (COO) | 255000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Chief Executive Officer (CEO) | 200000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Executive Board member (CFO) | 140000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Executive Board member (COO) | 170000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| austriacard-holdings-ag | staff_by_country |  | Romania: 1346 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,346 vs 2,360 (43.0% apart) |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 289,459, more than the stated 278,255; XF-02: parts add up to 289,459, stated 278,255 |
| autoneum-holding-ag | base_salary | All members | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| autoneum-holding-ag | base_salary | CEO | 870000 | Fail (hard) | CORE-02: 870000 not in the quote |
| autoneum-holding-ag | base_salary | Other members of Group Executi | 2142658 | Fail (hard) | CORE-02: 2142658 not in the quote |
| autoneum-holding-ag | benefits_value | Other members of Group Executi | 830372 | Fail (hard) | CORE-02: 830372 not in the quote |
| autoneum-holding-ag | lti_granted | Other members of Group Executi | 393122 | Fail (hard) | CORE-02: 393122 not in the quote |
| autoneum-holding-ag | sti_paid | Other members of Group Executi | 1568370 | Fail (hard) | CORE-02: 1568370 not in the quote |
| autoneum-holding-ag | total_remuneration | Other members of Group Executi | 4934523 | Fail (hard) | CORE-02: 4934523 not in the quote |
| autotrader-group-plc | shareholding_requirement |  | 200% of salary in-post; 200% o | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| avation-plc | pension_contribution | Executive Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| avation-plc | pension_contribution | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aviva-plc | headcount |  | 36160 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aviva-plc | role_disclosure | Executive Directors | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| b-m-european-value-retail-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | interim CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| babcock-international-group-plc | base_salary | Deputy Chief Executive | 108000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | benefits_value | Deputy Chief Executive | 21000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | pension_contribution | Deputy Chief Executive | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| bachem-holding-ag | lti_granted | Rest of the Corporate Executiv | 261000 | Fail (hard) | CORE-02: 261 not in the quote |
| bachem-holding-ag | pension_contribution | Rest of the Corporate Executiv | 274000 | Fail (hard) | CORE-02: 274 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | sti_paid | CEO | 247000 | Fail (hard) | CORE-02: 247 not in the quote |
| bachem-holding-ag | sti_paid | Corporate Executive Committee | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bakkafrost | ebitda |  | 1672664000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| balfour-beatty-plc | pension_contribution | Former Group Chief Executive ( | 43183 | Fail (hard) | CORE-03: quote not in the source text |
| balfour-beatty-plc | revenue_by_country |  | United Kingdom: 4778; United S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | revenue_by_segment |  | Construction Services: 8711; S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| balfour-beatty-plc | sti_target | Group Chief Executive (appoint | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Executive Director | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Former Group Chief Executive ( | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| baltic-classifieds-group-plc | ebitda |  | 68626000 | Fail (hard) | CORE-02: 68626 not in the quote |
| baltic-classifieds-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| barclays-plc | pension_contribution | Group Chief Executive | 155000 | Fail (hard) | CORE-02: 155 not in the quote |
| barclays-plc | pension_contribution | Group Finance Director | 94000 | Fail (hard) | CORE-02: 94 not in the quote |
| barclays-plc | total_remuneration | Group Chief Executive | 15045000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 4,588,000, stated 15,045,000 |
| barclays-plc | total_remuneration | Group Finance Director | 8970000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,770,000, stated 8,970,000 |
| barry-callebaut-ag | pension_type |  | Defined benefit plans in Switz | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | headcount |  | 1054 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Managemen | 605000 | Fail (hard) | CORE-02: 605000 not in the quote |
| basellandschaftliche-kantonalbank | pension_type |  | defined contribution, BLKB cov | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must acquire 2 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | staff_by_country |  | Canton of Basel-Landschaft: 92 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Managemen | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; XF-02: parts add up to 2,855,610, stated 3,028,977 |
| basler-ag-o-n | base_salary | Vorstandsvorsitzender (CEO) (u | 367000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | controlling_owner_name |  | Norbert Basler Holding GmbH | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | largest_holders |  | Norbert Basler Holding GmbH 53 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | lti_max | Vorstandsvorsitzender (CEO) (u | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_max | Vorstand Commercial (CCO) und  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_max | Vorstand Finanzen (CFO) (Eintr | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstandsvorsitzender (CEO) (u | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstand Commercial (CCO) und  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstand Finanzen (CFO) (Eintr | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | revenue_by_country |  | EMEA: 78.9; America: 47.9; Asi | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 272,200,000 vs 224,500,000 (21.2% apart) |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstand Finanzen (CFO) (Eintr | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | shareholding_requirement |  | 50 % of the variable compensat | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | staff_by_country |  | Europe: 708; Asia: 178; Americ | Fail | CORE-04: no period_end; NUM-08: adds up to 920 vs 811 (13.4% apart) |
| basler-ag-o-n | staff_by_segment |  | R&D: 238 | Fail | CORE-04: no period_end; NUM-08: adds up to 238 vs 811 (70.7% apart) |
| basler-ag-o-n | ultimate_parent |  | Norbert Basler Holding GmbH | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-kantonalbank | controlling_owner_name |  | Canton of Basel-Stadt | Fail (hard) | CORE-02: not in the quote: canton of |
| basler-kantonalbank | fte |  | 1273 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-kantonalbank | sub_sector |  | Die Bank versteht die Wahrnehm | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-kantonalbank | total_remuneration | CEO (ab 1.3.2025), Mitglied de | 834147 | Fail (hard) | XF-01: parts add up to 1,006,080, more than the stated 834,147; XF-02: parts add up to 1,006,080, stated 834,147 |
| basler-kantonalbank | total_remuneration | Geschäftsleitungsmitglieder | 3498135 | Fail (hard) | XF-01: parts add up to 4,265,533, more than the stated 3,498,135; XF-02: parts add up to 4,265,533, stated 3,498,135 |
| batm-advanced-communications-limited | base_salary | Former CFO (until 21 June 2025 | 207000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| batm-advanced-communications-limited | ebitda |  | 18940000 | Fail (hard) | CORE-02: 18.94 not in the quote |
| batm-advanced-communications-limited | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main |
| batm-advanced-communications-limited | revenue_by_segment |  | Networks: 11626; Cyber: 8263;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| batm-advanced-communications-limited | total_remuneration | Former CFO (until 21 June 2025 | 207000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | CEO | 24059 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | Management Board member (Enver | 18078 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | Management Board member (Sat S | 18462 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | Chief Administrative Officer | 7015 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | Chief Risk Officer | 11881 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | lti_vested | Management Board member (Andre | 17051 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | revenue_by_country |  | Austria: 1020.5; Germany: 490. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | revenue_by_segment |  | Retail & SME: 1876; Corporates | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | shareholding_requirement |  | CEO: 5x annual base salary; Ot | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | sub_sector |  | BAWAG’s primary value creation | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (Grita  | 1705000 | Fail (hard) | CORE-02: 1705 not in the quote; CORE-03: quote not in the source text |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (bis 30 | 393000 | Fail (hard) | CORE-02: 393 not in the quote |
| beiersdorf-ag-o-n | sti_target | Mitglied des Vorstands (bis 30 | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | base_salary | Other members, Executive Commi | 2108000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_country |  | EMEA: 240.3; Americas: 341.3;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| belimo-holding-ag | revenue_by_segment |  | Damper Actuators: 253.8; Contr | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| belimo-holding-ag | role_disclosure | Other members, Executive Commi | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | Other members, Executive Commi | 2449000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | total_remuneration | CEO | 1749000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,539,000, stated 1,749,000 |
| belimo-holding-ag | total_remuneration | Other members, Executive Commi | 5573000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 5,108,000, stated 5,573,000 |
| bell-food-group-ag | aggregate_headcount | Other members of the Group Exe | 8 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bellevue-group-ag | headcount |  | 72.8 | Fail (hard) | NUM-05: not a whole number |
| bellevue-group-ag | revenue_by_country |  | Switzerland: 47705; United Kin | Fail (hard) | CORE-03: quote not in the source text |
| bellevue-group-ag | role_disclosure | Group Executive Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bellevue-group-ag | total_assets |  | 155563000 | Fail (hard) | CORE-02: 155563 not in the quote; CORE-04: no period_end |
| berentzen-gruppe-ag-957f8708 | benefits |  | company car (including private | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| berentzen-gruppe-ag-957f8708 | benefits_value | Member of the Executive Board  | 42300 | Fail (hard) | CORE-02: 42.3 not in the quote |
| berentzen-gruppe-ag-957f8708 | lti_vested | Member of the Executive Board  | 135400 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | lti_vested | Member of the Executive Board  | 135400 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | sti_paid | Member of the Executive Board  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | sti_paid | Member of the Executive Board  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| berkeley-group-holdings-the-plc | lti_granted | Executive Chair | 400 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CEO | 250 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CFO (from 29 September 2025) | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berner-kantonalbank-ag | aggregate_headcount | Geschäftsleitung | 6.6 | Fail (hard) | NUM-05: not a whole number |
| berner-kantonalbank-ag | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| berner-kantonalbank-ag | pension_type |  | defined contribution, employer | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | revenue |  | 460000000 | Fail (hard) | CORE-03: quote not in the source text |
| bertrandt-ag-o-n | aggregate_headcount | Executive Board | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bertrandt-ag-o-n | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bertrandt-ag-o-n | base_salary | Management Board | 1614000 | Fail (hard) | CORE-02: 1.614 not in the quote |
| bertrandt-ag-o-n | benefits_value | Management Board | 39000 | Fail (hard) | CORE-02: 0.039 not in the quote |
| bertrandt-ag-o-n | ebitda |  | -98046000 | Fail (hard) | CORE-02: -98.046 not in the quote |
| bertrandt-ag-o-n | fte |  | 13824 | Fail (hard) | CORE-02: 13824 not in the quote |
| bertrandt-ag-o-n | revenue |  | 1186884000 | Fail (hard) | CORE-02: 1186.884 not in the quote |
| bertrandt-ag-o-n | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bertrandt-ag-o-n | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bertrandt-ag-o-n | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bertrandt-ag-o-n | role_disclosure | Executive Board | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bertrandt-ag-o-n | staff_by_country |  | Romania: 1000 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,000 vs 14,028 (92.9% apart) |
| bertrandt-ag-o-n | total_assets |  | 879538000 | Fail (hard) | CORE-02: 879.538 not in the quote |
| bertrandt-ag-o-n | total_remuneration | Management Board | 1653000 | Fail (hard) | CORE-02: 1.653 not in the quote |
| besqab-pref-b | base_salary | VD | 4500000 | Fail (hard) | CORE-02: 4.5 not in the quote |
| besqab-pref-b | controlling_owner_name |  | Aros Bostad | Fail (hard) | CORE-02: not in the quote: aros bostad |
| besqab-pref-b | fte |  | 110 | Fail (hard) | CORE-03: quote not in the source text |
| besqab-pref-b | pension_contribution | VD | 1100000 | Fail (hard) | CORE-02: 1.1 not in the quote |
| besqab-pref-b | pension_contribution | Övriga ledande befattningshava | 2400000 | Fail (hard) | CORE-02: 2.4 not in the quote |
| besqab-pref-b | revenue_by_segment |  | Projektutveckling Ägda hem: 18 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,939,200,000 vs 836,400,000 (131.9% apart) |
| besqab-pref-b | sti_paid | VD | 2100000 | Fail (hard) | CORE-02: 2.1 not in the quote |
| besqab-pref-b | total_remuneration | VD | 7700000 | Fail (hard) | CORE-02: 7.7 not in the quote |
| besqab-pref-b | total_remuneration | Övriga ledande befattningshava | 14400000 | Fail (hard) | CORE-02: 14.4 not in the quote |
| big-yellow-group-plc | fte |  | 453 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| big-yellow-group-plc | listing_date |  | May 2000 | Fail (hard) | COD-06: not a year or a date |
| big-yellow-group-plc | share_price |  | 967.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bijou-brigitte-c3387b07 | revenue_by_country |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bijou-brigitte-c3387b07 | revenue_by_segment |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bilfinger-se-o-n | benefits_value | Chairman of the Executive Boar | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | benefits_value | member of the Executive Board, | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | shareholding_requirement |  | Executive Board members are ob | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bilfinger-se-o-n | total_remuneration | member of the Executive Board, | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| bkw-ag | sti_target | CEO | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_target | Group Executive Board | 30 | Fail (hard) | CORE-03: quote not in the source text |
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
| bp-plc | base_salary | Interim CEO (from 18 December  | 733000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | base_salary | Chief executive officer (until | 854000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | base_salary | Chief financial officer | 387000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | base_salary | Other executive directors | 2573000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | fte |  | 4158 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | headcount |  | 93700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | lti_vested | Interim CEO (from 18 December  | 83000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | lti_vested | Chief executive officer (until | 2594000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | lti_vested | Chief financial officer | 1545000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | lti_vested | Other executive directors | 734000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | pension_contribution | Interim CEO (from 18 December  | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | pension_contribution | Chief executive officer (until | 138000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | pension_contribution | Chief financial officer | 82000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | pension_contribution | Other executive directors | 132000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | revenue_by_country |  | US: 56703; Non-US: 132632; UK: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 218,049,000,000 vs 192,549,000,000 (13.2% apart) |
| bp-plc | sti_paid | Interim CEO (from 18 December  | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | sti_paid | Chief executive officer (until | 287000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | sti_paid | Chief financial officer | 169000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bp-plc | sti_paid | Other executive directors | 290000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| braemar-plc | base_salary | Former Group Chief Operating O | 7200 | Fail (hard) | CORE-02: 7.2 not in the quote |
| braemar-plc | pension_contribution | Group Chief Financial and Oper | 23100 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| braemar-plc | revenue_by_segment |  | Chartering: 74713; Investment  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| braemar-plc | sti_paid | Group Chief Financial and Oper | 400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| branicks-group-ag | revenue |  | 100000000 | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-02: 2.23 not in the quote; CORE-03: quote not in the source text |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: quote not in the source text |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| british-american-tobacco-plc | other_names |  | British American Tobacco Compa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| british-american-tobacco-plc | revenue_by_segment |  | NGP: 397; Strategic Portfolio: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 17,108,000,000 vs 25,610,000,000 (33.2% apart) |
| brooks-macdonald-group-plc | lti_granted | CEO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| brooks-macdonald-group-plc | lti_granted | CFO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bsf-enterprise-plc | largest_holders |  | GBF Nominees Limited 19.48%; B | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | lti_granted | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bsf-enterprise-plc | pension_contribution | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bt-group-plc | fte |  | 81600 | Fail (hard) | CORE-02: 81.6 not in the quote |
| bt-group-plc | headcount |  | 77200 | Fail (hard) | CORE-02: 77.2 not in the quote |
| bt-group-plc | lti_granted | Executive Director (Allison Ki | 2803899 | Fail (hard) | CORE-02: 2803899 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | lti_granted | Executive Director (Simon Lowt | 2057634 | Fail (hard) | CORE-02: 2057634 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | sti_paid | Executive Director (Allison Ki | 1081000 | Fail (hard) | CORE-02: 1081 not in the quote |
| bt-group-plc | sti_paid | Executive Director (Simon Lowt | 793000 | Fail (hard) | CORE-02: 793 not in the quote |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| bunzl-plc | revenue_by_segment |  | North America: 6276.7; Contine | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burberry-group-plc | lti_max | CFO | 175 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burckhardt-compression-holding-ag | benefits_value | CEO | 221000 | Fail (hard) | CORE-02: 221 not in the quote |
| burckhardt-compression-holding-ag | benefits_value | Other members of the Executive | 488000 | Fail (hard) | CORE-02: 488 not in the quote |
| burckhardt-compression-holding-ag | listing_date |  | 2006-06 | Fail (hard) | COD-06: not a year or a date |
| burckhardt-compression-holding-ag | revenue_by_country |  | Europe: 194414; Africa: 10564; | Fail (hard) | CORE-03: quote not in the source text |
| burckhardt-compression-holding-ag | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burckhardt-compression-holding-ag | sti_target | CEO | 0.28 | Fail (hard) | COD-01: unit '' is not a target form |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| bvz-holding-ag | aggregate_headcount | Geschäftsleitung | 7 | Fail (hard) | CORE-03: quote not in the source text |
| bvz-holding-ag | revenue_by_segment |  | Gornergrat: 47.1; Immobilien:  | Fail (hard) | CORE-03: quote on page 5, link says page 4; NUM-08: adds up to 181,900,000 vs 216,170,312 (15.9% apart) |
| bvz-holding-ag | role_disclosure | Geschäftsleitung | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bw-offshore-limited | role_disclosure | Senior Management Team | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bw-offshore-limited | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bystronic-ag | aggregate_headcount | Executive Committee | 4.1 | Fail (hard) | NUM-05: not a whole number |
| bystronic-ag | lti_target | Executive Committee | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | lti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | Executive Committee | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| bytes-technology-group-plc | ebitda |  | 62732000 | Fail (hard) | CORE-02: 62732 not in the quote |
| bytes-technology-group-plc | lti_granted | CEO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bytes-technology-group-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| c-c-group-plc | lti_granted | Chief Financial and Transforma | 404411 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| c-c-group-plc | revenue_by_segment |  | Branded: 453.6; Distribution:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 1,861,600,000 vs 1,569,800,000 (18.6% apart) |
| c-capital-holdings-ag-53a1594e | lti_granted | Key management personnel | 5000000 | Fail (hard) | CORE-03: quote not in the source text |
| cab-payments-holdings-plc | revenue |  | 109400000 | Fail (hard) | CORE-03: quote not in the source text |
| cab-payments-holdings-plc | total_assets |  | 188000000 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | ebitda |  | 1258000 | Fail (hard) | CORE-02: 1.258 not in the quote; CORE-04: no period_end |
| cadogan-energy-solutions-plc | lti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | revenue_by_country |  | Ukraine: 7.55 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| cadogan-energy-solutions-plc | revenue_by_segment |  | Exploration and Production: 71 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| caffyns-plc | headcount |  | 485 | Fail (hard) | CORE-02: 485 not in the quote |
| caledonia-investments-plc | benefits_value | Executive Director (J M B Cayz | 31000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | headcount |  | 82 | Fail (hard) | CORE-02: 82 not in the quote |
| caledonia-investments-plc | lti_vested | Executive Director (J M B Cayz | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | revenue_by_segment |  | Public Companies: 21.8; Privat | Fail | CORE-04: no period_end; NUM-08: adds up to 43,700,000 vs 166,000,000 (73.7% apart) |
| calida-holding-ag-1793bfba | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| cancom-se-o-n | ebitda |  | 102700000 | Fail (hard) | CORE-02: 102.7 not in the quote |
| cancom-se-o-n | share_price |  | 26.65 | Fail (hard) | CORE-02: 26.65 not in the quote |
| cantargia-ab-1b3e1f95 | staff_by_country |  | Sweden: 23 | Fail (hard) | CORE-03: quote not in the source text |
| capita-plc | share_price |  | 4.055 | Fail (hard) | CORE-02: 4.055 not in the quote |
| capita-plc | shares_outstanding |  | 120030667 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | base_salary | Executive Chair | 528000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | CEO (until 8 March 2025) | 442000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | Executive Director | 417000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | CEO (until 8 March 2025) | 73000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | Executive Director | 49000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Chair | 722000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Director | 546000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | Executive Chair | 1345000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | CEO (until 8 March 2025) | 515000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | Executive Director | 1012000 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | benefits_value | Chief Executive Officer | 14082 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | ebitda |  | 5700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | fte |  | 41 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | headcount |  | 41 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | lti_vested | Chief Executive Officer | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | pension_contribution | Chief Executive Officer | 62500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | revenue_by_segment |  | Egypt: 134.3; Other Capricorn  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| capricorn-energy-plc | sti_paid | Chief Executive Officer | 550000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capricorn-energy-plc | sti_target | Chief Executive Officer | 62.5 | Fail (hard) | CORE-02: 62.5 not in the quote |
| capricorn-energy-plc | total_remuneration | Chief Executive Officer | 1126582 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | base_salary | Chief Executive Officer | 400000 | Fail (hard) | CORE-02: 400000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | base_salary | Chief Financial Officer (from  | 280000 | Fail (hard) | CORE-02: 280000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Executive Officer | 11000 | Fail (hard) | CORE-02: 11000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Financial Officer (from  | 12000 | Fail (hard) | CORE-02: 12000 not in the quote; CORE-03: quote not in the source text |
| carclo-plc | fte |  | 907 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | headcount |  | 907 | Fail (hard) | CORE-03: quote not in the source text |
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
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cembra-money-bank-ag-752ce099 | pension_contribution | CEO | 147149 | Fail (hard) | CORE-02: 147149 not in the quote |
| cembra-money-bank-ag-752ce099 | pension_contribution | Active Management Board | 539983 | Fail (hard) | CORE-02: 539983 not in the quote |
| centiel-ag-eeeda54a | base_salary | Mitglied des Verwaltungsrates  | 18000 | Fail (hard) | CORE-02: 18000 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | base_salary | CFO (seit 6. Mai 2025) | 55032 | Fail (hard) | CORE-02: 55032 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | base_salary | Geschäftsleitung Total | 98064 | Fail (hard) | CORE-02: 98064 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | benefits_value | Mitglied des Verwaltungsrates  | 1200 | Fail (hard) | CORE-02: 1200 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | pay_currency | Mitglied des Verwaltungsrates  | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | pay_currency | CFO (seit 6. Mai 2025) | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | pay_currency | Geschäftsleitung Total | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | pension_contribution | Mitglied des Verwaltungsrates  | 3391 | Fail (hard) | CORE-02: 3391 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | pension_contribution | CFO (seit 6. Mai 2025) | 10509 | Fail (hard) | CORE-02: 10509 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | pension_contribution | Geschäftsleitung Total | 18617 | Fail (hard) | CORE-02: 18617 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | sti_paid | CFO (seit 6. Mai 2025) | 20000 | Fail (hard) | CORE-02: 20000 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | sti_paid | Geschäftsleitung Total | 20000 | Fail (hard) | CORE-02: 20000 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | sub_sector |  | Centiel develops and sells thr | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| centiel-ag-eeeda54a | total_assets |  | 12335000 | Fail (hard) | CORE-02: 12335 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | total_remuneration | Mitglied des Verwaltungsrates  | 22591 | Fail (hard) | CORE-02: 22591 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | total_remuneration | CFO (seit 6. Mai 2025) | 85541 | Fail (hard) | CORE-02: 85541 not in the quote; CORE-04: no period_end |
| centiel-ag-eeeda54a | total_remuneration | Geschäftsleitung Total | 136681 | Fail (hard) | CORE-02: 136681 not in the quote; CORE-04: no period_end |
| centrica-plc | listing_date |  | 1997-02-17 | Fail (hard) | CORE-02: not in the quote: 1997 |
| centrica-plc | lti_granted | Group Chief Executive | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| centrica-plc | lti_granted | Group Chief Financial Officer | 125 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| centrica-plc | share_price |  | 1.4065 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| ceres-power-holdings-plc | total_assets |  | 145796000 | Fail (hard) | CORE-02: 145796 not in the quote; CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | base_salary | Former members of group manage | 747000 | Fail (hard) | CORE-02: 747 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | CEO | 227000 | Fail (hard) | CORE-02: 227 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Other members of group managem | 409000 | Fail (hard) | CORE-02: 409 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Former members of group manage | 89000 | Fail (hard) | CORE-02: 89 not in the quote |
| chemring-group-plc | lti_vested | Chief Financial Officer | 230000 | Fail (hard) | CORE-02: 230 not in the quote |
| chemring-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chemring-group-plc | shares_outstanding |  | 272099390 | Fail (hard) | CORE-02: 272099390 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| chemring-group-plc | sti_max | Group Chief Executive | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| chemring-group-plc | sti_target | Group Chief Executive | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| chocoladefabriken-lindt-sprungli-ag-f056b804 | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | revenue_by_segment |  | Europe: 2955.5; North America: | Fail (hard) | CORE-03: quote not in the source text |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | shares_outstanding |  | 1095704 | Fail (hard) | CORE-02: 1095704 not in the quote |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | staff_by_country |  | North America: 4220; Europe: 9 | Fail (hard) | CORE-03: quote not in the source text |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | staff_by_segment |  | North America: 4220; Europe: 9 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | base_salary | Group Management | 1204000 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | total_remuneration | Group Management | 4564000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,293,000, stated 4,564,000 |
| cicor-technologies-ltd-39bd9715 | total_remuneration | CEO | 2051000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,072,000, stated 2,051,000 |
| cizzle-biotechnology-holdings-plc | exchange_segment |  | Equity Shares (transitional ca | Fail (hard) | CORE-02: not in the quote: shares |
| cizzle-biotechnology-holdings-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| clariant-ag-0616ec80 | lti_granted | Other ESC members | 2389017 | Fail (hard) | CORE-02: 2389017 not in the quote; CORE-03: quote not in the source text |
| clariant-ag-0616ec80 | shareholding_requirement |  | CEO: 150,000 shares; Other ESC | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| clarkson-plc | fte |  | 2103 | Fail (hard) | CORE-03: quote not in the source text |
| clarkson-plc | staff_by_segment |  | Broking: 1504; Financial: 127; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 2,103 vs 2,250 (6.5% apart) |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| close-brothers-group-plc | lti_granted | Chief Executive (from 10 Septe | 726000 | Fail (hard) | CORE-02: 726 not in the quote |
| cloudbreak-discovery-plc | accounting_basis |  | UK-adopted international accou | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cloudbreak-discovery-plc | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| cloudbreak-discovery-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 0.4425 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| cmb-tech-nv | base_salary | Management Board Members (excl | 1000000 | Fail (hard) | CORE-02: 1000000 not in the quote |
| cmb-tech-nv | benefits |  | Fringe benefits include health | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cmb-tech-nv | sti_paid | Management Board Members (excl | 250000 | Fail (hard) | CORE-02: 250000 not in the quote |
| cmc-markets-plc | ebitda |  | 117842 | Fail (hard) | CORE-02: 117.842 not in the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: quote not in the source text |
| coats-group-plc | lti_granted | Group Chief Executive Officer | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | lti_granted | Group Chief Financial Officer | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | share_price |  | 84.55 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| coca-cola-hbc-ag | revenue_by_country |  | Switzerland: 460.2; The Russia | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| coca-cola-hbc-ag | share_price |  | 38.42 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | staff_by_country |  | Armenia: 345; Austria: 871; Be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| comet-holding-ag-f1ab2b78 | role_disclosure | Current Executive Committee me | aggregate | Fail (hard) | CORE-03: quote not in the source text |
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
| compagnie-financiere-tradition-sa-940d20ce | pension_type |  | defined contribution schemes;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| compass-group-plc | benefits_value | Group COO, North America | 106000 | Fail (hard) | CORE-03: quote not in the source text |
| compass-group-plc | lti_vested | Group COO, North America | 3882000 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | revenue_by_segment |  | UK: 1419.2; Germany: 2109.3; W | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | exchange |  | London Stock Exchange | Fail (hard) | CORE-02: not in the quote: london stock exchange |
| conduit-holdings-limited | headcount |  | 68 | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | staff_by_country |  | UK: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 2 vs 68 (97.1% apart) |
| contango-holdings-plc | website |  | contango-holdings-plc.co.uk | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Group Human Relations a | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | total_remuneration | Automotive, Vorstandsmitglied  | 1537000 | Fail (hard) | XF-01: parts add up to 1,590,000, more than the stated 1,537,000; XF-02: parts add up to 1,590,000, stated 1,537,000 |
| continental-ag-o-n | total_remuneration | Tires, Vorstandsmitglied seit  | 1739000 | Fail (hard) | XF-01: parts add up to 1,901,000, more than the stated 1,739,000; XF-02: parts add up to 1,901,000, stated 1,739,000 |
| continental-ag-o-n | total_remuneration | ContiTech, Vorstandsmitglied s | 1467000 | Fail (hard) | XF-01: parts add up to 1,747,000, more than the stated 1,467,000; XF-02: parts add up to 1,747,000, stated 1,467,000 |
| convatec-group-plc | listing_date |  | 2016-10 | Fail (hard) | COD-06: not a year or a date |
| convatec-group-plc | staff_by_country |  | Europe: 5276; North America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | staff_by_segment |  | Operations: 3467; Sales and ma | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | sti_target | Former Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | total_remuneration | Former Chief Executive Officer | 7648000 | Fail (hard) | XF-01: parts add up to 8,565,000, more than the stated 7,648,000; XF-02: parts add up to 8,565,000, stated 7,648,000 |
| corem-property-d | shares_outstanding |  | 1396281000 | Fail (hard) | CORE-02: 1396281000 not in the quote |
| corem-property-d | sti_paid | Andra ledande befattningshavar | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote |
| corem-property-d | sti_paid | Other senior executives | 900 | Fail (hard) | CORE-02: 900 not in the quote |
| corpus-resources-plc | controlling_owner_name |  | James Antony Stenhouse | Fail (hard) | CORE-02: not in the quote: antony |
| corpus-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| costain-group-plc | base_salary | Chief Financial Officer | 439544 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | benefits_value | Chief Financial Officer | 14945 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | fte |  | 3049 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | headcount |  | 3049 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | lti_vested | Chief Financial Officer | 1040064 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | pension_contribution | Chief Financial Officer | 43954 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | revenue_by_segment |  | Natural Resources: 440.4; Tran | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| costain-group-plc | share_price |  | 160 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| costain-group-plc | sti_paid | Chief Financial Officer | 565196 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cranswick-plc | fte |  | 13033 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | headcount |  | 13033 | Fail (hard) | CORE-03: quote not in the source text |
| crest-nicholson-holdings-plc | revenue_by_segment |  | UK housebuilding: 610.8 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| critical-metals-plc | share_price |  | 9.1 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | staff_by_country |  | DRC: 49 | Fail | CORE-04: no period_end |
| critical-mineral-resources-plc | fte |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | headcount |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| croda-international-plc | sti_paid | Chief Financial Officer (CFO)  | 359.203 | Fail (hard) | CORE-02: 359.203 not in the quote |
| curatis-holding-ag-adc33085 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| currys-plc | fte |  | 25076 | Fail (hard) | CORE-02: 25076 not in the quote |
| cykel-ai-plc | total_assets |  | 1537768 | Fail (hard) | CORE-03: quote not in the source text |
| dar-global-plc | ebitda |  | 126600000 | Fail (hard) | CORE-02: 126.6 not in the quote |
| datwyler-holding-ag-eca04fdb | shares_outstanding |  | 34600000 | Fail (hard) | CORE-02: 34600000 not in the quote |
| datwyler-holding-ag-eca04fdb | sti_max | Executive Committee | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| dcc-energy-plc | lti_granted | Chief Executive | 2051000 | Fail (hard) | CORE-03: quote not in the source text; NUM-12: currency GBP, the role's other amounts EUR |
| dcc-energy-plc | revenue_by_segment |  | DCC Energy: 12990355; DCC Tech | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | sti_paid | Chief Executive | 1928000 | Fail (hard) | CORE-02: 1928 not in the quote |
| defence-holdings-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | COD-06: not a year or a date |
| delticom-ag-na-o-n | share_price |  | 2.14 | Fail (hard) | CORE-02: 2.14 not in the quote; CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_max | Chief Financial Officer (since | 264000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_target | Chief Financial Officer (since | 132000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| derwent-london-plc | lti_vested | CEO | 502000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | lti_vested | Other Executive Directors | 502000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| derwent-london-plc | sti_paid | Other Executive Directors | 651000 | Fail (hard) | CORE-03: quote not in the source text |
| derwent-london-plc | total_remuneration | CEO | 845000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,619,119, more than the stated 845,000; XF-02: parts add up to 1,619,119, stated 845,000 |
| derwent-london-plc | total_remuneration | Other Executive Directors | 651000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 1,215,600, more than the stated 651,000; XF-02: parts add up to 1,215,600, stated 651,000 |
| deutsche-real-estate-ag-8625fa60 | largest_holders |  | Summit Real Estate Holdings Lt | Fail (hard) | NUM-07: holdings add up to 165.96% |
| deutsche-real-estate-ag-8625fa60 | other_names |  | Geestemünder Bank AG; Geestemü | Fail (hard) | CORE-02: not in the quote: bank |
| deutsche-real-estate-ag-8625fa60 | share_price |  | 10.7 | Fail (hard) | CORE-02: 10.7 not in the quote |
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
| dierig-holding-ag-91dc6032 | ebitda |  | 3400000 | Fail (hard) | CORE-02: 3.4 not in the quote |
| dierig-holding-ag-91dc6032 | fte |  | 107.7 | Fail (hard) | CORE-02: 107.7 not in the quote |
| digia-oyj | aggregate_headcount | Other key personnel | 20 | Fail (hard) | CORE-03: quote not in the source text |
| digia-oyj | shareholding_requirement |  | participants have the chance t | Fail (hard) | CORE-03: quote not in the source text |
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
| dksh-holding-ag-6576340c | ultimate_parent |  | DKSH Holding Ltd. | Fail (hard) | CORE-02: not in the quote: dksh ltd |
| docmorris-ag-be190279 | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | fte |  | 2402 | Fail (hard) | CORE-02: 2402 not in the quote |
| domino-s-pizza-group-plc | lti_granted | Former CEO (until 24 November  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| domino-s-pizza-group-plc | lti_granted | Former CFO (until 18 September | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Präsident, exekutiv | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Mitglieder des Verwaltun | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Gruppenleitung | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | CEO/Vorsitzender der Gruppenle | CHF | Fail | CORE-04: no period_end |
| dr-martens-plc | benefits_value | CEO | 5000 | Fail (hard) | CORE-02: 5 not in the quote; CORE-03: quote not in the source text |
| dr-martens-plc | benefits_value | CFO | 19000 | Fail (hard) | CORE-02: 19 not in the quote; CORE-03: quote not in the source text |
| dr-martens-plc | lti_granted | CEO | 1950000 | Fail (hard) | CORE-02: 1950 not in the quote |
| dr-martens-plc | lti_granted | CFO | 1498650 | Fail (hard) | CORE-02: 1498.65 not in the quote |
| dr-martens-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| dr-martens-plc | lti_vested | CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| drax-group-plc | fte |  | 3128 | Fail (hard) | CORE-02: 3128 not in the quote |
| drax-group-plc | share_price |  | 837.8 | Fail (hard) | CORE-03: quote not in the source text |
| dsm-firmenich-ag-62366aa6 | controlling_owner_name |  | Firmenich Family | Fail (hard) | CORE-02: not in the quote: family |
| dsm-firmenich-ag-62366aa6 | lti_max | CEO | 300 | Fail (hard) | CORE-03: quote not in the source text |
| dsm-firmenich-ag-62366aa6 | revenue_by_country |  | Switzerland: 214; Netherlands: | Fail | CORE-04: no period_end; NUM-08: adds up to 9,034,000,000 vs 12,521,000,000 (27.8% apart) |
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
| eisen-und-huettenwerke-5b76d547 | share_price |  | 15.5 | Fail (hard) | CORE-02: 15.5 not in the quote |
| eisen-und-huettenwerke-5b76d547 | sub_sector |  | Die Eisen- und Hüttenwerke AG  | Fail (hard) | CORE-03: quote not in the source text |
| elementis-plc | benefits_value | Former CEO (until 31 July 2025 | 84434 | Fail (hard) | CORE-03: quote not in the source text |
| elementis-plc | benefits_value | Former CFO (until 31 December  | 30466 | Fail (hard) | CORE-03: quote not in the source text |
| elixirr-international-plc | benefits_value | Chief Executive Officer | 13000 | Fail (hard) | CORE-02: 13 not in the quote |
| elixirr-international-plc | benefits_value | Deputy Chief Executive Officer | 8000 | Fail (hard) | CORE-02: 8 not in the quote |
| elixirr-international-plc | benefits_value | Chief Financial Officer (appoi | 12000 | Fail (hard) | CORE-02: 12 not in the quote |
| elixirr-international-plc | ebitda |  | 44300000 | Fail (hard) | CORE-02: 44300000 not in the quote |
| elixirr-international-plc | sti_paid | Chief Executive Officer | 1392000 | Fail (hard) | CORE-02: 1392 not in the quote |
| elixirr-international-plc | sti_paid | Deputy Chief Executive Officer | 1392000 | Fail (hard) | CORE-02: 1392 not in the quote |
| elixirr-international-plc | sti_paid | Chief Financial Officer (appoi | 580000 | Fail (hard) | CORE-02: 580 not in the quote |
| emmi-ag-ad10f47a | pension_contribution | CEO | 204000 | Fail (hard) | CORE-02: 204 not in the quote |
| emmi-ag-ad10f47a | pension_contribution | Other members of Group Executi | 838000 | Fail (hard) | CORE-02: 838 not in the quote |
| enbw-energie-baden-wuerttemberg-30b5438b | revenue_by_country |  | Germany: 24310; European curre | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner_name |  | La Mancha | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | fte |  | 5659 | Fail (hard) | CORE-02: 5659 not in the quote |
| endeavour-mining-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | revenue_by_segment |  | Ity Mine: 838.1; Houndé Mine:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| enquest-plc | lti_granted | Chief Executive | 185 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| enquest-plc | lti_granted | Chief Financial Officer | 185 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| enquest-plc | revenue_by_country |  | North Sea: 895313; Malaysia: 1 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | revenue_by_segment |  | UK&I: 2180.1; International: 2 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| entain-plc | staff_by_segment |  | UK&I: 18582; International: 65 | Fail (hard) | CORE-03: quote not in the source text |
| epic-suisse-ag-7c2f8dc4 | benefits_value | Chief Executive Officer | 9000 | Fail (hard) | CORE-03: quote not in the source text |
| epic-suisse-ag-7c2f8dc4 | benefits_value | Group Executive Management | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| epic-suisse-ag-7c2f8dc4 | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| epigenomics-ag-ddb6ea6d | total_remuneration | Vorstand (bis 30.April 2024) | -33000 | Fail (hard) | NUM-04: -33000 outside 0..5e+10; XF-01: parts add up to -32,468, more than the stated -33,000 |
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
| essentra-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| eurocell-plc | listing_date |  | 2015-03 | Fail (hard) | COD-06: not a year or a date |
| eurotelesites-ag | benefits |  | company car or a corresponding | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| eurotelesites-ag | revenue_by_country |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | revenue_by_segment |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | sti_paid | CEO | 132000 | Fail (hard) | CORE-02: 132000 not in the quote |
| eurotelesites-ag | sti_paid | CFO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| eurotelesites-ag | total_remuneration | Management Board | 1224000 | Fail (hard) | XF-01: parts add up to 1,272,000, more than the stated 1,224,000; XF-02: parts add up to 1,272,000, stated 1,224,000 |
| everest-global-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | controlling_owner_name |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | largest_holders |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pension_contribution | Chief Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| everest-global-plc | pension_contribution | Executive Director of Precious | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| fair-value-reit-ag-cef1dc63 | exchange |  | Frankfurter Wertpapierbörse | Fail (hard) | COD-01: 'Frankfurter Wertpapierbörse' matches no ISO 10383 exchange |
| fair-value-reit-ag-cef1dc63 | fte |  | 2 | Fail (hard) | CORE-02: 2 not in the quote |
| fair-value-reit-ag-cef1dc63 | isin |  | DE000A0MW975 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Other leading executives | 5 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Övriga ledande befattningshava | 5 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | isin |  | SE0016785786 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | pension_type |  | premiebaserad pensionslösning | Fail (hard) | CORE-03: quote not in the source text |
| fastpartner-d | base_salary | Other members of the Executive | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | base_salary | Other senior executives | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | pension_contribution | Other members of the Executive | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | pension_contribution | Other senior executives | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | share_price |  | 47.45 | Fail (hard) | CORE-03: quote not in the source text |
| fastpartner-d | sti_max | Other senior executives | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_paid | Other members of the Executive | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| fastpartner-d | sti_paid | Other senior executives | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Supervisory Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | role_disclosure | Key employees | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | sub_sector |  | The FWAG Group generates reven | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| framery-group | base_salary | CEO | 219240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | benefits |  | company car, phone and accommo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| framery-group | ebitda |  | 56400000 | Fail (hard) | CORE-02: 56.4 not in the quote; CORE-04: no period_end |
| framery-group | lti_vested | Management team | 3273000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | revenue_by_country |  | Eurooppa, Lähi-itä ja Afrikka: | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | revenue_by_segment |  | Äänieristetyt työtilat: 216017 | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | share_price |  | 8.35 | Fail (hard) | CORE-02: 8.35 not in the quote |
| framery-group | staff_by_country |  | Finland: 357; Americas: 21; EM | Fail | CORE-04: no period_end; NUM-08: adds up to 398 vs 484 (17.8% apart) |
| framery-group | sti_paid | CEO | 36000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | total_remuneration | CEO | 255240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | website |  | framery.com | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| helios-solar-ag-797724e7 | ebitda |  | -154.8 | Fail (hard) | CORE-02: -154.8 not in the quote |
| helios-solar-ag-797724e7 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| helios-solar-ag-797724e7 | total_assets |  | 50089.1 | Fail (hard) | CORE-03: quote not in the source text |
| hermana-holding | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| hermana-holding | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| himalaya-shipping | controlling_owner_name |  | Drew Holdings Ltd. | Fail (hard) | CORE-02: not in the quote: ltd |
| himalaya-shipping | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| holand-og-setskog-sparebank | ebitda |  | 57700000 | Fail (hard) | CORE-02: 57.7 not in the quote |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (1) | individual | Fail (hard) | CORE-03: quote not in the source text |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (2) | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Deputy Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Other members of Executive Man | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| intea-fastigheter-d | fte |  | 60 | Fail (hard) | CORE-02: 60 not in the quote; CORE-03: quote not in the source text |
| intea-fastigheter-d | pension_contribution | Övriga ledande befattningshava | 1300000 | Fail (hard) | CORE-02: 1.3 not in the quote |
| intea-fastigheter-d | revenue_by_segment |  | project properties: 265 | Fail | CORE-04: no period_end; NUM-08: adds up to 265,000,000 vs 1,561,000,000 (83.0% apart) |
| intea-fastigheter-d | total_remuneration | Verkställande direktör | 3800000 | Fail (hard) | CORE-02: 3.8 not in the quote |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote; CORE-03: quote not in the source text |
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 4094000 | Fail (hard) | CORE-02: 4094 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3325000 | Fail (hard) | CORE-02: 3325 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 293000 | Fail (hard) | CORE-02: 293 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 266000 | Fail (hard) | CORE-02: 266 not in the quote |
| k2a-knaust-andersson-pref | fte |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| k2a-knaust-andersson-pref | headcount |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| k2a-knaust-andersson-pref | share_price |  | 4.98 | Fail (hard) | CORE-02: 4.98 not in the quote |
| kesko-b | aggregate_headcount | Group Management Board | 7 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kesko-b | role_disclosure | Hallituksen jäsenet | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| khd-humboldt-wedag-eff61cda | fte |  | 5 | Fail (hard) | CORE-02: 5 not in the quote |
| khd-humboldt-wedag-eff61cda | revenue_by_country |  | India: 1670; Germany: 272; USA | Fail (hard) | CORE-03: quote not in the source text |
| maschinenfabrik-berthold-hermle-6808fdaf | exchange |  | Stuttgart Stock Exchange | Fail (hard) | COD-01: 'Stuttgart Stock Exchange' matches no ISO 10383 exchange |
| maschinenfabrik-berthold-hermle-6808fdaf | pension_type |  | defined contribution, up to 1, | Fail (hard) | CORE-03: quote not in the source text |
| maschinenfabrik-berthold-hermle-6808fdaf | revenue_by_country |  | Federal Republic of Germany: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 232,367,000 vs 491,891,000 (52.8% apart) |
| maschinenfabrik-berthold-hermle-6808fdaf | revenue_by_segment |  | Domestic companies: 255538; Fo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 983,782,000 vs 491,891,000 (100.0% apart) |
| maschinenfabrik-berthold-hermle-6808fdaf | staff_by_country |  | Germany: 1228 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,228 vs 1,639 (25.1% apart) |
| maternus-kliniken-ag-fe2ae118 | ebitda |  | 3900000 | Fail (hard) | CORE-02: 3.9 not in the quote |
| maternus-kliniken-ag-fe2ae118 | share_price |  | 1.02 | Fail (hard) | CORE-02: 1.02 not in the quote |
| max-automation-se-e7586bc1 | pay_currency | Geschäftsführender Direktor (C | EUR | Fail | CORE-04: no period_end |
| max-automation-se-e7586bc1 | pay_currency | Geschäftsführender Direktor (C | EUR | Fail | CORE-04: no period_end |
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
| ming-le-sports-ag-fc0affd5 | sti_target | Vorstandsmitglied | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote; COD-01: unit '' is not a target form |
| mueller-die-lila-logistik-se-f3c40a4b | ebitda |  | 11300000 | Fail (hard) | CORE-02: 11.3 not in the quote |
| mueller-die-lila-logistik-se-f3c40a4b | other_names |  | Müller – Lila Logistik AG | Fail (hard) | CORE-03: quote not in the source text |
| mueller-die-lila-logistik-se-f3c40a4b | revenue_by_country |  | Deutschland: 214187; Ausland:  | Fail | CORE-04: no period_end; NUM-08: adds up to 250,478,000 vs 11,374,899 (2102.0% apart) |
| mueller-die-lila-logistik-se-f3c40a4b | revenue_by_segment |  | Lila Operating: 249948; Lila R | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 250,478,000 vs 11,374,899 (2102.0% apart) |
| norcom-information-technology-2811f08c | listing_date |  | 1999-10 | Fail (hard) | COD-06: not a year or a date |
| norcom-information-technology-2811f08c | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| norcom-information-technology-2811f08c | share_price |  | 1.55 | Fail (hard) | CORE-02: 1.55 not in the quote |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| orbis-se-3d0d94ff | benefits_value | Vorstandssprecher | 18700 | Fail (hard) | CORE-02: 18.7 not in the quote |
| orbis-se-3d0d94ff | benefits_value | Vorstand | 12800 | Fail (hard) | CORE-02: 12.8 not in the quote |
| orbis-se-3d0d94ff | benefits_value | Vorstand (until December 2025) | 20300 | Fail (hard) | CORE-02: 20.3 not in the quote |
| orbis-se-3d0d94ff | lti_granted | Vorstand | 51300 | Fail (hard) | CORE-02: 51.3 not in the quote |
| orbis-se-3d0d94ff | lti_max | Vorstandssprecher | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | lti_max | Vorstand | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | lti_max | Vorstand (until December 2025) | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | sti_max | Vorstandssprecher | 18 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | sti_paid | Vorstandssprecher | 72800 | Fail (hard) | CORE-02: 72.8 not in the quote |
| ostasiatiske | ebitda |  | -2500000 | Fail (hard) | CORE-02: -2.5 not in the quote |
| ostasiatiske | exchange |  | NASDAQ OMX Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ OMX Copenhagen A/S' matches no ISO 10383 exchange |
| ostasiatiske | sti_paid | CEO (Kresten M. Valdal) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| ostasiatiske | total_assets |  | 32700000 | Fail (hard) | CORE-02: 32.7 not in the quote |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| paratus-energy | revenue_by_segment |  | Seagems: 265; Fontis: 187 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 452,000,000 vs 153,200,000 (195.0% apart) |
| path2-hydrogen-ag-4a522574 | benefits |  | mögliche Vereinbarungen über e | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| path2-hydrogen-ag-4a522574 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| pearl-gold-ag-da4e9b62 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| pearl-gold-ag-da4e9b62 | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| pfeiffer-vacuum-tech-ag-a38e65f0 | ebitda |  | 90600000 | Fail (hard) | CORE-02: 90.6 not in the quote |
| pfeiffer-vacuum-tech-ag-a38e65f0 | listing_date |  | 2023-12-29 | Fail (hard) | CORE-02: not in the quote: 2023 29 |
| pferdewetten-de-ag-07705286 | aggregate_headcount | Vorstand | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| pittler-maschinenfabrik-ag-fb62b449 | benefits_value | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | controlling_owner_name |  | Herr Günter Rothenberger | Fail (hard) | CORE-02: not in the quote: nter |
| pittler-maschinenfabrik-ag-fb62b449 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| pittler-maschinenfabrik-ag-fb62b449 | other_names |  | Leipziger Werkzeugmaschinenfab | Fail (hard) | CORE-03: quote not in the source text |
| pittler-maschinenfabrik-ag-fb62b449 | sti_paid | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| planoptik-ag-9429909d | sti_target | Vorstandsmitglied | 10 | Fail (hard) | COD-01: unit '' is not a target form |
| public-property-invest | largest_holders |  | Samhällsbyggnadsbolaget i Nord | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| public-property-invest | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| readcrest-capital-ag-e4689651 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| readcrest-capital-ag-e4689651 | role_disclosure | CEO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| readcrest-capital-ag-e4689651 | role_disclosure | CFO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| readcrest-capital-ag-e4689651 | share_price |  | 1.34 | Fail (hard) | CORE-02: 1.34 not in the quote |
| revolutionrace | staff_by_country |  | Sweden: 160 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 160 vs 170 (5.9% apart) |
| revolutionrace | sub_sector |  | Our driving force is to develo | Fail (hard) | CORE-03: quote not in the source text |
| s-d-standard-etc | controlling_owner_name |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-d-standard-etc | share_price |  | 1.688 | Fail (hard) | CORE-02: 1.688 not in the quote |
| s-d-standard-etc | ultimate_parent |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| sagax-d | base_salary | Other members of Group managem | 5300000 | Fail (hard) | CORE-02: 5.3 not in the quote |
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
| seb-c | revenue |  | -411000 | Fail | CORE-04: no period_end; NUM-04: -411000 outside 0..1e+14 |
| seb-c | revenue_by_country |  | Sweden: 46498; Norway: 4315; D | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 76,903,000,000 vs -411,000 (18711292.2% apart) |
| seb-c | revenue_by_segment |  | Corporate & Investment Banking | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 76,928,000,000 vs -411,000 (18717374.9% apart) |
| seb-c | staff_by_country |  | Sverige: 189 | Fail (hard) | CORE-03: quote not in the source text |
| sed-energy | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| sentia | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| sentia | controlling_owner_name |  | Ratos AB | Fail (hard) | CORE-03: quote not in the source text |
| sentia | largest_holders |  | Ratos AB 39% | Fail (hard) | CORE-03: quote not in the source text |
| sentia | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| sentia | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_country |  | Norge: 9404; Sverige: 2369 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_segment |  | HENT: 9404; Sentia Sverige: 23 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | share_price |  | 62.99 | Fail (hard) | CORE-02: 62.99 not in the quote |
| sentia | staff_by_segment |  | HENT: 1338; Sentia Sverige: 17 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,516 vs 6 (25166.7% apart) |
| sino-german-united-ag-388acb2d | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| sino-german-united-ag-388acb2d | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| sino-german-united-ag-388acb2d | role_disclosure | Vorstand/Chief Operating Offic | individual | Fail (hard) | CORE-03: quote not in the source text |
| softing-ag-365a9352 | share_price |  | 2.3 | Fail (hard) | CORE-03: quote not in the source text |
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
| ssab-b | headcount |  | 14609 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ssab-b | listing_date |  | 1988 | Fail (hard) | CORE-02: not in the quote: 1988 |
| ssab-b | shareholding_requirement |  | LTI participants must hold sha | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stabilus-se-52dccb73 | listing_date |  | 2014-05 | Fail (hard) | COD-06: not a year or a date |
| stabilus-se-52dccb73 | revenue_by_country |  | Germany: 367128; Romania: 1322 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stabilus-se-52dccb73 | revenue_by_segment |  | EMEA: 542183; Americas: 480899 | Fail (hard) | CORE-03: quote not in the source text |
| stabilus-se-52dccb73 | sub_sector |  | The object of the Company is t | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | controlling_owner |  | state | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | controlling_owner_name |  | Solidium Oy | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | ownership_type |  | state_owned | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stora-enso-a | revenue_by_country |  | Austria: 298; Baltic States: 3 | Fail (hard) | CORE-03: quote not in the source text |
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
| subsea7 | pension_contribution | Chief Financial Officer | 60500 | Fail (hard) | CORE-03: quote not in the source text |
| subsea7 | revenue_by_country |  | Norway: 1664.6; United Kingdom | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| subsea7 | staff_by_country |  | Angola: 242; Australia: 246; B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| suss-microtec-se-b7558a97 | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | fte |  | 1497 | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | largest_holders |  | Janus Henderson 9.89%; Univers | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | revenue_by_country |  | North America: 46; Asia / Paci | Fail (hard) | CORE-03: quote not in the source text |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
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
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | lti_max | Vorsitzender des Vorstands | 870000 | Fail (hard) | CORE-02: 870000 not in the quote; CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | lti_max | Ordentliches Vorstandsmitglied | 338332.5 | Fail (hard) | CORE-02: 338332.5 not in the quote; CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | lti_max | Ordentliches Vorstandsmitglied | 145000 | Fail (hard) | CORE-02: 145000 not in the quote; CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | lti_max | Ordentliches Vorstandsmitglied | 241667.5 | Fail (hard) | CORE-02: 241667.5 not in the quote; CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | lti_max | Ordentliches Vorstandsmitglied | 241667.5 | Fail (hard) | CORE-02: 241667.5 not in the quote; CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pay_currency | Vorsitzender des Vorstands | EUR | Fail | CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pay_currency | Ordentliches Vorstandsmitglied | EUR | Fail | CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pay_currency | Ordentliches Vorstandsmitglied | EUR | Fail | CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pay_currency | Ordentliches Vorstandsmitglied | EUR | Fail | CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pay_currency | Ordentliches Vorstandsmitglied | EUR | Fail | CORE-04: no period_end |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | pension_type |  | Defined contribution (cash all | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | role_disclosure | Vorsitzender des Vorstands | individual | Fail (hard) | CORE-03: quote not in the source text |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | role_disclosure | Ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | role_disclosure | Ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | role_disclosure | Ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| thyssenkrupp-nucera-ag-kgaa-fac8c580 | role_disclosure | Ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| tkms-ag-co-kgaa-f468ef4d | aggregate_headcount | Management Board | 4 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| traton-se-8a6b8f62 | controlling_owner_name |  | Volkswagen Aktiengesellschaft | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | pay_currency | CFO | EUR | Fail | CORE-04: no period_end |
| uie | listing_date |  | 1983-05 | Fail (hard) | COD-06: not a year or a date |
| uie | share_price |  | 386.5 | Fail (hard) | CORE-03: quote not in the source text |
| uie | sti_max | Managing Director | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| united-eco-solutions-ag-44c5756c | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| united-eco-solutions-ag-44c5756c | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| united-eco-solutions-ag-44c5756c | pension_contribution | Vorstand (Mathias Schmid) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| united-eco-solutions-ag-44c5756c | pension_contribution | Vorstand (Armin Schulz) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| united-eco-solutions-ag-44c5756c | sti_paid | Vorstand (Mathias Schmid) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| united-eco-solutions-ag-44c5756c | sti_paid | Vorstand (Armin Schulz) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| utd-internet-ag-fa5f4803 | controlling_owner_name |  | Ralph Dommermuth | Fail (hard) | CORE-02: not in the quote: ralph |
| uzin-utz-se-808b3f93 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| verbio-se-9b8df34d | ebitda |  | 193900000 | Fail (hard) | CORE-02: 193.9 not in the quote; CORE-03: quote not in the source text |
| verbio-se-9b8df34d | share_price |  | 29.8 | Fail (hard) | CORE-02: 29.8 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | accounting_basis |  | IFRS Accounting Standards | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorstand Digitalisierung / IT  | 17300 | Fail (hard) | CORE-02: 17.3 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorständin HR / Organisationse | 16100 | Fail (hard) | CORE-02: 16.1 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorstand Bad & Wellness (seit  | 7200 | Fail (hard) | CORE-02: 7.2 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorstandsvorsitzende (seit 01. | 22900 | Fail (hard) | CORE-02: 22.9 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorstand Finanzen (seit 01.01. | 18500 | Fail (hard) | CORE-02: 18.5 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Für alle weiteren früheren Vor | 39200 | Fail (hard) | CORE-02: 39.2 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | exchange_segment |  | Prime Standard | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | listing_date |  | 1992 | Fail (hard) | CORE-02: not in the quote: 1992 |
| villeroy-boch-ag-c5a85d57 | lti_vested | Vorständin HR / Organisationse | 88900 | Fail (hard) | CORE-02: 88.9 not in the quote |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Vorstand Digitalisierung / IT  | 15500 | Fail (hard) | CORE-02: 15.5 not in the quote |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Vorständin HR / Organisationse | 20600 | Fail (hard) | CORE-02: 20.6 not in the quote |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Vorstand Finanzen (seit 01.01. | 42500 | Fail (hard) | CORE-02: 42.5 not in the quote |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Vorstand Tischkultur (bis 31.0 | 12200 | Fail (hard) | CORE-02: 12.2 not in the quote; CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Vorstandsvorsitzender (bis 31. | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | pension_contribution | Für alle weiteren früheren Vor | 1558400 | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | pension_type |  | defined-contribution pension p | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villeroy-boch-ag-c5a85d57 | role_disclosure | Vorstandsvorsitzende (seit 01. | individual | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | staff_by_country |  | Germany: 2817; Outside Germany | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 12,389 vs 2,122 (483.8% apart) |
| villeroy-boch-ag-c5a85d57 | sti_paid | Vorstand Digitalisierung / IT  | 62700 | Fail (hard) | CORE-02: 62.7 not in the quote |
| villeroy-boch-ag-c5a85d57 | sti_paid | Vorständin HR / Organisationse | 78400 | Fail (hard) | CORE-02: 78.4 not in the quote |
| villeroy-boch-ag-c5a85d57 | sti_paid | Vorstand Bad & Wellness (seit  | 112600 | Fail (hard) | CORE-02: 112.6 not in the quote |
| villeroy-boch-ag-c5a85d57 | sub_sector |  | Group is a leading internation | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstand Bad & Wellness (seit  | 869700 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 662,200, stated 869,700 |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstandsvorsitzende (seit 01. | 1616800 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,340,100, stated 1,616,800 |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstand Finanzen (seit 01.01. | 869400 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 661,900, stated 869,400 |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstand Tischkultur (bis 31.0 | 12200 | Fail (hard) | CORE-02: 12.2 not in the quote |
| vincorion-se-16aba459 | sub_sector |  | VINCORION offers Vehicle Syste | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | controlling_owner_name |  | Dr. Martin Heuser and Volker P | Fail (hard) | CORE-02: not in the quote: and |
| viscom-se-859e40d6 | ebitda |  | -1815000 | Fail (hard) | CORE-02: -1.815 not in the quote |
| viscom-se-859e40d6 | listing_date |  | 2006-05 | Fail (hard) | COD-06: not a year or a date |
| viscom-se-859e40d6 | revenue_by_country |  | Amerika: 10.681; Asien: 24.175 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 34,856,000 vs 81,705,000 (57.3% apart) |
| viscom-se-859e40d6 | share_price |  | 6.34 | Fail (hard) | CORE-02: 6.34 not in the quote |
| viscom-se-859e40d6 | staff_by_country |  | Europa: 343; Amerika: 27; Asie | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | pay_currency | Chair, Sport Luxury brand grou | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Finance and Operations | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | China, Chair of the Board of M | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Progressive brand group, Chair | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Integrity and Legal Affairs | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Human Resources and Trucks bra | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Core brand group, Chair of the | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Technology, Chair of the Board | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | IT | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | pay_currency | Former Board of Management mem | EUR | Fail | CORE-04: no period_end |
| volkswagen-ag-be878a5e | role_disclosure | Chair, Sport Luxury brand grou | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| volkswagen-ag-be878a5e | role_disclosure | Former Board of Management mem | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | total_remuneration | Finance and Operations | 5075339.19 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 5,683,225, more than the stated 5,075,339; XF-02: parts add up to 5,683,225, stated 5,075,339 |
| volkswagen-ag-be878a5e | total_remuneration | Progressive brand group, Chair | 3404523 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,029,494, more than the stated 3,404,523; XF-02: parts add up to 4,029,494, stated 3,404,523 |
| volkswagen-ag-be878a5e | total_remuneration | Integrity and Legal Affairs | 2545518 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,995,518, more than the stated 2,545,518; XF-02: parts add up to 2,995,518, stated 2,545,518 |
| volkswagen-ag-be878a5e | total_remuneration | Human Resources and Trucks bra | 1791959.7 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,033,682, more than the stated 1,791,960; XF-02: parts add up to 2,033,682, stated 1,791,960 |
| volkswagen-ag-be878a5e | total_remuneration | Core brand group, Chair of the | 3401649 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,012,452, more than the stated 3,401,649; XF-02: parts add up to 4,012,452, stated 3,401,649 |
| volkswagen-ag-be878a5e | total_remuneration | Technology, Chair of the Board | 5630301.3 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 6,236,765, more than the stated 5,630,301; XF-02: parts add up to 6,236,765, stated 5,630,301 |
| volkswagen-ag-be878a5e | total_remuneration | IT | 3401076 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,026,786, more than the stated 3,401,076; XF-02: parts add up to 4,026,786, stated 3,401,076 |
| volkswagen-ag-be878a5e | total_remuneration | Former Board of Management mem | 1560554.53 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 1,676,039, more than the stated 1,560,555; XF-02: parts add up to 1,676,039, stated 1,560,555 |
| voltatron-ag-57b867a2 | fte |  | 112 | Fail (hard) | CORE-03: quote not in the source text |
| voss-veksel-landmandsbank | fte |  | 28.4 | Fail (hard) | CORE-02: 28.4 not in the quote |
| voss-veksel-landmandsbank | revenue |  | 197537000 | Fail (hard) | CORE-03: quote not in the source text |
| wasgau-produktions-handels-8c33a77d | lti_max | Sprecher des Vorstands (ab 01/ | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | revenue_by_segment |  | Großhandel: 170897; Einzelhand | Fail (hard) | CORE-03: quote not in the source text |
| wild-bunch-ag-7b9483b1 | revenue_by_segment |  | Internationaler Vertrieb und V | Fail (hard) | CORE-03: quote not in the source text |
| wild-bunch-ag-7b9483b1 | share_price |  | 31.2 | Fail (hard) | CORE-02: 31.2 not in the quote |
| wuestenrot-wuerttembergische-ag-07b9dfbc | revenue_by_segment |  | Housing: 1104; Life and health | Fail (hard) | CORE-03: quote not in the source text |
