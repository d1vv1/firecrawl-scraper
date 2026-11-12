# Output checks: fy2025_runs_datapoints.csv

567 companies, 25265 filled values checked (2026-11-12, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 22638 (90%) |
| Review | 1033 (4%) |
| Fail | 110 (0%) |
| Fail (hard) | 1484 (6%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 2492 | 2476 | 0 | 0 | 16 |
| Listing and market | 2094 | 2037 | 0 | 0 | 57 |
| Sector | 732 | 717 | 0 | 0 | 15 |
| Reporting basis | 1764 | 1754 | 0 | 0 | 10 |
| Financials | 1512 | 1293 | 135 | 1 | 83 |
| Workforce | 588 | 460 | 73 | 1 | 54 |
| Ownership and control | 1605 | 1505 | 0 | 0 | 100 |
| Segment and geography | 637 | 352 | 113 | 35 | 137 |
| Pay policy | 1101 | 1031 | 0 | 0 | 70 |
| Role and disclosure | 3604 | 3344 | 8 | 73 | 179 |
| Pay: fixed | 3343 | 2955 | 167 | 0 | 221 |
| Pay: STI | 2354 | 2052 | 140 | 0 | 162 |
| Pay: LTI | 2047 | 1727 | 104 | 0 | 216 |
| Pay: total | 1392 | 935 | 293 | 0 | 164 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 25265 | 25241 | 24 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 11654 | 11317 | 337 | 13611 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 17995 | 17054 | 941 | 7270 | source not cached; the run itself did not find the quote |
| CORE-04 | Period end present (dated fields only) |  | 14869 | 14083 | 786 | 10396 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 25265 | 25261 | 4 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 8417 | 8378 | 39 | 16848 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 366 | 366 | 0 | 24899 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 749 | 749 | 0 | 24516 |  |
| COD-06 | Dates are valid | yes | 779 | 757 | 22 | 24486 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 8082 | 8044 | 38 | 17183 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 7613 | 7613 | 0 | 17652 |  |
| NUM-04 | Magnitude in a plausible range |  | 9245 | 9200 | 45 | 16020 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 883 | 876 | 7 | 24382 | not a whole number |
| NUM-06 | Percentages in range | yes | 1446 | 1445 | 1 | 23819 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 274 | 269 | 5 | 24991 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 629 | 478 | 151 | 24636 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 1130 | 1130 | 0 | 24135 |  |
| NUM-11 | STI paid not above its maximum |  | 453 | 424 | 29 | 24812 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 6886 | 6849 | 37 | 18379 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 262 | 243 | 19 | 25003 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 116 | 116 | 0 | 25149 |  |
| DER-06 | Derived value shows its formula |  | 933 | 933 | 0 | 24332 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 1192 | 1088 | 104 | 24073 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 1192 | 822 | 370 | 24073 | parts add up to N stated N |

## Fill rate

Company fields: 12525 of 23247 filled (54%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 42 | 567 |
| staff_by_segment | 80 | 567 |
| staff_by_country | 135 | 567 |
| market_cap_band | 183 | 567 |
| revenue_by_country | 197 | 567 |
| share_price | 199 | 567 |
| controlling_owner_name | 200 | 567 |
| other_names | 209 | 567 |
| exchange_segment | 219 | 567 |
| revenue_by_segment | 225 | 567 |
| listing_date | 244 | 567 |
| shareholding_requirement | 248 | 567 |
| pe_stake_5pct | 261 | 567 |
| fte | 263 | 567 |
| largest_holders | 274 | 567 |
| ownership_type | 284 | 567 |
| controlling_owner | 285 | 567 |
| ultimate_parent | 301 | 567 |
| ebitda | 308 | 567 |
| shares_outstanding | 316 | 567 |
| headcount | 325 | 567 |
| accounting_basis | 342 | 567 |
| isin | 344 | 567 |
| total_assets | 344 | 567 |
| revenue | 345 | 567 |
| ticker | 351 | 567 |
| website | 353 | 567 |
| lei | 363 | 567 |
| reporting_currency | 364 | 567 |
| sector_code | 366 | 567 |
| sub_sector | 366 | 567 |
| exchange | 376 | 567 |
| listing_status | 377 | 567 |
| business_id | 379 | 567 |
| legal_name | 382 | 567 |
| country_code | 382 | 567 |
| head_office_city | 382 | 567 |
| benefits | 422 | 567 |
| pension_type | 431 | 567 |
| fiscal_year | 523 | 567 |
| fiscal_year_end | 535 | 567 |

Pay fields, over 1500 executive roles:

| Field | Filled |
|---|---|
| base_salary | 1274 (85%) |
| sti_paid | 1094 (73%) |
| sti_target | 461 (31%) |
| sti_max | 799 (53%) |
| lti_vested | 479 (32%) |
| lti_granted | 651 (43%) |
| lti_target | 359 (24%) |
| lti_max | 558 (37%) |
| benefits_value | 1017 (68%) |
| pension_contribution | 1052 (70%) |
| total_remuneration | 1392 (93%) |

## Failed values (1594)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 2invest-ag-bf4e0781 | base_salary | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| 2invest-ag-bf4e0781 | total_remuneration | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | sti_paid | Other EC members | 1500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| abb-ltd | sti_target | Other EC members | 1190000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| acceler8-ventures-plc | ebitda |  | -172772 | Fail (hard) | CORE-02: -172772 not in the quote |
| accelleron-industries-ag | revenue_by_country |  | Asia, Middle East & Africa: 54 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| accelleron-industries-ag | staff_by_country |  | Switzerland: 1014; Asia & Midd | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| acg-metals-limited | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| acg-metals-limited | total_remuneration | Chairman & Chief Executive Off | 1256156 | Fail (hard) | XF-01: parts add up to 1,497,823, more than the stated 1,256,156; XF-02: parts add up to 1,497,823, stated 1,256,156 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CEO | 899204.92 | Fail (hard) | XF-01: parts add up to 1,132,160, more than the stated 899,205; XF-02: parts add up to 1,132,160, stated 899,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CRO | 649204.82 | Fail (hard) | XF-01: parts add up to 731,888, more than the stated 649,205; XF-02: parts add up to 731,888, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CMO/CIO | 649204.82 | Fail (hard) | XF-01: parts add up to 858,865, more than the stated 649,205; XF-02: parts add up to 858,865, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CFO | 549204.92 | Fail (hard) | XF-01: parts add up to 694,802, more than the stated 549,205; XF-02: parts add up to 694,802, stated 549,205 |
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
| aevis-victoria-sa | aggregate_headcount | Other Members of Senior Manage | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| agilyx | exchange |  | OSE | Fail (hard) | COD-01: 'OSE' matches no ISO 10383 exchange |
| agilyx | revenue_by_country |  | Europe: 544402; USA: 255044; A | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| agilyx | revenue_by_segment |  | Cyclyx: 16574621; Agilyx: 1214 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 17,789,146 vs 1,214,525 (1364.7% apart) |
| agrana-beteiligungs-ag-60d4466c | revenue_by_segment |  | FBS: 1647834; ACS – Stärke: 98 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| airtel-africa-plc | accounting_basis |  | International Financial Report | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | benefits_value | Former CFO (until 9 July 2025) | 55000 | Fail (hard) | CORE-02: 55 not in the quote |
| airtel-africa-plc | exchange_segment |  | premium listing segment | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | staff_by_segment |  | Executive management: 174; Man | Fail | CORE-04: no period_end; NUM-08: adds up to 4,132 vs 11,520 (64.1% apart) |
| airtel-africa-plc | sub_sector |  | the provision of telecommunica | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | ultimate_parent |  | Bharti Enterprises (Holding) P | Fail (hard) | CORE-03: quote not in the source text |
| alcon-inc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | lti_max | CEO | 1150 | Fail (hard) | NUM-06: 1150 % of base salary |
| alcon-inc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | revenue_by_country |  | United States: 4657; Switzerla | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alfa-financial-software-holdings-plc | revenue_by_segment |  | Subscription: 43.6; Software E | Fail (hard) | CORE-03: quote not in the source text |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| alkemy-capital-investments-plc | fte |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| allgeier-se-9971b49d | pension_type |  | defined benefit plans; defined | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| allreal-holding-ag | ebitda |  | 310500000 | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | lti_target | Other members of Group Managem | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | staff_by_segment |  | Real Estate: 50 | Fail | CORE-04: no period_end; NUM-08: adds up to 50 vs 224 (77.7% apart) |
| alpine-select-ag | benefits |  | fringe benefits, flat-rat allo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| amag-austria-metall-ag-9da856cd | share_price |  | 32 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amag-austria-metall-ag-9da856cd | staff_by_country |  | Austria: 1866; Germany: 249 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | pension_type |  | The Corporation does not opera | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amaroq-ltd | revenue |  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | total_assets |  | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amicorp-fs-uk-plc | fte |  | 172 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amigo-resources-plc | total_assets |  | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | share_price |  | 0.0208 | Fail (hard) | CORE-03: quote not in the source text |
| amrize-ltd | benefits |  | deferred compensation plan, 40 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | pension_type |  | defined benefit (cash balance  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| amrize-ltd | sub_sector |  | The Company is organized into  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| antofagasta-plc | headcount |  | 8457 | Fail (hard) | CORE-02: 8457 not in the quote |
| antofagasta-plc | listing_date |  | 1888 | Fail (hard) | CORE-02: not in the quote: 1888; COD-06: not a year or a date |
| antofagasta-plc | staff_by_country |  | Chile: 6053; United Kingdom: 5 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,062 vs 8,457 (28.3% apart) |
| apg-sga-sa | pension_contribution | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| apg-sga-sa | pension_contribution | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| apg-sga-sa-8679206d | benefits_value | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| aptitude-software-group-plc | revenue_by_country |  | United Kingdom: 10586; Rest of | Fail (hard) | CORE-03: quote not in the source text |
| aptitude-software-group-plc | staff_by_country |  | United Kingdom: 102; Rest of W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 359 vs 317 (13.2% apart) |
| arbonia-ag | base_salary | Other members of Group Managem | 628000 | Fail (hard) | CORE-02: 628 not in the quote |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | total_remuneration | Other members of Group Managem | 1507000 | Fail (hard) | CORE-02: 1507 not in the quote |
| aryzta-ag | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ebitda |  | 306900000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | revenue_by_country |  | Switzerland: 280.9; Germany: 6 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aryzta-ag | revenue_by_segment |  | ARYZTA Europe: 1977; ARYZTA Re | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| atlas-metals-group-plc | website |  | atlasmetalsgroup.com | Fail (hard) | CORE-02: not in the quote: atlasmetalsgroup com |
| atoss-software-se | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | controlling_owner_name |  | AOB Invest GmbH | Fail (hard) | CORE-02: not in the quote: aob invest gmbh |
| atoss-software-se | lti_max | Chief Executive Officer (CEO) | 120000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Chief Executive Officer (CEO) | 100000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Executive Board member (CFO) | 70000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | lti_target | Executive Board member (COO) | 85000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_contribution | Executive Board member (CFO) | 41616000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_contribution | Executive Board member (COO) | 54000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | pension_type |  | defined benefits plan for CEO; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | revenue_by_country |  | Germany: 159951899; Austria: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | sti_max | Chief Executive Officer (CEO) | 240000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_max | Executive Board member (CFO) | 210000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_max | Executive Board member (COO) | 255000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Chief Executive Officer (CEO) | 200000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Executive Board member (CFO) | 140000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atoss-software-se | sti_target | Executive Board member (COO) | 170000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| austriacard-holdings-ag | benefits_value | Executive Vice President Türki | 13810 | Fail (hard) | CORE-02: 13810 not in the quote |
| austriacard-holdings-ag | staff_by_country |  | Romania: 1346 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,346 vs 2,360 (43.0% apart) |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 292,065, more than the stated 278,255; XF-02: parts add up to 292,065, stated 278,255 |
| auto1-group-se-0e2acd91 | revenue_by_country |  | Germany: 1963802; Italy: 11102 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| auto1-group-se-0e2acd91 | revenue_by_segment |  | Merchant: 6413599; Retail: 175 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| auto1-group-se-0e2acd91 | shares_outstanding |  | 220835000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| autoneum-holding-ag | base_salary | All members | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| autoneum-holding-ag | base_salary | CEO | 870000 | Fail (hard) | CORE-02: 870000 not in the quote |
| autoneum-holding-ag | base_salary | Other members of Group Executi | 2142658 | Fail (hard) | CORE-02: 2142658 not in the quote |
| autotrader-group-plc | shareholding_requirement |  | 200% of salary in-post; 200% o | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aviva-plc | headcount |  | 36160 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aviva-plc | role_disclosure | Executive Directors | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: quote on page 207, link says page 206 |
| avon-technologies-plc | fte |  | 911 | Fail (hard) | CORE-03: quote not in the source text |
| avon-technologies-plc | lti_granted | CEO | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | revenue_by_segment |  | Avon Protection: 168.8; Team W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| avon-technologies-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| avon-technologies-plc | total_assets |  | 314800000 | Fail (hard) | CORE-03: quote not in the source text |
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| babcock-international-group-plc | base_salary | Deputy Chief Executive | 108000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | benefits_value | Deputy Chief Executive | 21000 | Fail (hard) | CORE-03: quote not in the source text |
| babcock-international-group-plc | pension_contribution | Deputy Chief Executive | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| bachem-holding-ag | lti_granted | Rest of the Corporate Executiv | 261000 | Fail (hard) | CORE-02: 261 not in the quote |
| bachem-holding-ag | pension_contribution | Rest of the Corporate Executiv | 274000 | Fail (hard) | CORE-02: 274 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bajaj-mobility-ag-8e6bef55 | ebitda |  | 874000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| basler-ag-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | controlling_owner_name |  | Norbert Basler Holding GmbH | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | largest_holders |  | Norbert Basler Holding GmbH 53 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | revenue_by_country |  | EMEA: 78.9; America: 47.9; Asi | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 272,200,000 vs 224,500,000 (21.2% apart) |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | role_disclosure | Vorstand Finanzen (CFO) (from  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basler-ag-o-n | staff_by_country |  | Europe: 708; Asia: 178; Americ | Fail | CORE-04: no period_end; NUM-08: adds up to 920 vs 811 (13.4% apart) |
| basler-ag-o-n | staff_by_segment |  | R&D: 238 | Fail | CORE-04: no period_end; NUM-08: adds up to 238 vs 811 (70.7% apart) |
| basler-ag-o-n | sti_max | Vorstandsvorsitzender (CEO) (u | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_max | Vorstand Commercial (CCO) und  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_max | Vorstand Finanzen (CFO) (from  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstandsvorsitzender (CEO) (u | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstand Commercial (CCO) und  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | sti_target | Vorstand Finanzen (CFO) (from  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
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
| bawag-group-ag | revenue_by_country |  | Austria: 1020.5; Germany: 490. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | revenue_by_segment |  | Retail & SME: 1876; Corporates | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bawag-group-ag | sub_sector |  | BAWAG’s primary value creation | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Chairman of the Board of Manag | 5784538 | Fail (hard) | XF-01: parts add up to 6,411,795, more than the stated 5,784,538; XF-02: parts add up to 6,411,795, stated 5,784,538 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 2643824 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,425,599, stated 2,643,824 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 3205763 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,879,500, stated 3,205,763 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 1637046 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 1,509,747, stated 1,637,046 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 2608564 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,390,937, stated 2,608,564 |
| bay-motoren-werke-ag-2bc720d9 | total_remuneration | Member of the Board of Managem | 3048831 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,792,801, stated 3,048,831 |
| baywa-ag-na-o-n | base_salary | Member of the Board of Managem | 958400 | Fail (hard) | CORE-02: 958400 not in the quote |
| baywa-ag-na-o-n | base_salary | Chief Restructuring Officer (f | 150000 | Fail (hard) | CORE-02: 150000 not in the quote |
| baywa-ag-na-o-n | benefits_value | Member of the Board of Managem | 118700 | Fail (hard) | CORE-02: 118700 not in the quote |
| baywa-ag-na-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ebitda |  | -162500000 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | largest_holders |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pension_contribution | Member of the Board of Managem | 118900 | Fail (hard) | CORE-02: 118900 not in the quote |
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| baywa-ag-na-o-n | sti_paid | Member of the Board of Managem | 284700 | Fail (hard) | CORE-02: 284700 not in the quote |
| baywa-ag-na-o-n | total_remuneration | Member of the Board of Managem | 3186300 | Fail (hard) | CORE-02: 3186300 not in the quote; XF-02: parts add up to 1,480,700, stated 3,186,300 |
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| beiersdorf-ag-o-n | benefits |  | Provision of a company car, st | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | lti_max | Vorstandsvorsitzender | 8640000 | Fail (hard) | CORE-02: 8640000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Oswald | 4750000 | Fail (hard) | CORE-02: 4750000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CFO | 3850000 | Fail (hard) | CORE-02: 3850000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CHRO | 2550000 | Fail (hard) | CORE-02: 2550000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Grita  | 4766000 | Fail (hard) | CORE-02: 4766000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Ramon  | 3975000 | Fail (hard) | CORE-02: 3975000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Vorstandsvorsitzender | 4320000 | Fail (hard) | CORE-02: 4320000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Oswald | 2500000 | Fail (hard) | CORE-02: 2500000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands/CFO | 1925000 | Fail (hard) | CORE-02: 1925000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands/CHRO | 1275000 | Fail (hard) | CORE-02: 1275000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Grita  | 2383000 | Fail (hard) | CORE-02: 2383000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Ramon  | 2050000 | Fail (hard) | CORE-02: 2050000 not in the quote |
| beiersdorf-ag-o-n | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote on page 24, link says page 23 |
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
| bellevue-group-ag | total_assets |  | 155563000 | Fail (hard) | CORE-02: 155563 not in the quote; CORE-04: no period_end |
| berentzen-gruppe-ag-957f8708 | benefits |  | company car (including private | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| bertrandt-ag-o-n | ebitda |  | -98046000 | Fail (hard) | CORE-02: -98.046 not in the quote |
| bertrandt-ag-o-n | fte |  | 13824 | Fail (hard) | CORE-02: 13824 not in the quote |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Finanze | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Vertrie | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Technik | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Vorstand (gesamt) | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | revenue |  | 1186884000 | Fail (hard) | CORE-02: 1186.884 not in the quote |
| bertrandt-ag-o-n | staff_by_country |  | Romania: 1000 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,000 vs 14,028 (92.9% apart) |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | total_assets |  | 879538000 | Fail (hard) | CORE-02: 879.538 not in the quote |
| besqab-pref-b | controlling_owner_name |  | Aros Bostad | Fail (hard) | CORE-02: not in the quote: aros bostad |
| besqab-pref-b | fte |  | 110 | Fail (hard) | CORE-03: quote not in the source text |
| besqab-pref-b | revenue_by_segment |  | Projektutveckling Ägda hem: 18 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,939,200,000 vs 836,400,000 (131.9% apart) |
| big-yellow-group-plc | fte |  | 453 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| big-yellow-group-plc | listing_date |  | May 2000 | Fail (hard) | COD-06: not a year or a date |
| big-yellow-group-plc | share_price |  | 967.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bijou-brigitte-c3387b07 | revenue_by_country |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bijou-brigitte-c3387b07 | revenue_by_segment |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bilfinger-se-o-n | benefits_value | CEO | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | benefits_value | CFO | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| bilfinger-se-o-n | total_remuneration | CFO | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| biofrontera-ag-na-o-n | lti_target | CFO | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | role_disclosure | CFO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | shareholding_requirement |  | Vorstandsmitglieder sind zu ei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bks-bank-ag-5e8b8669 | revenue_by_segment |  | Privatkunden: 111406; Firmenku | Fail | CORE-04: no period_end; NUM-08: adds up to 388,487,000 vs 303,636,676 (27.9% apart) |
| bkw-ag | sti_target | CEO | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_target | Group Executive Board | 30 | Fail (hard) | CORE-03: quote not in the source text |
| blencowe-resources-plc | aggregate_headcount | Key management personnel (excl | 2 | Fail (hard) | CORE-03: quote not in the source text |
| bodycote-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | shareholding_requirement |  | 200% of salary during employme | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | sti_paid | CEO | 399000000 | Fail (hard) | CORE-02: 399000 not in the quote; NUM-11: paid 62344% of base, maximum 175% |
| bodycote-plc | sti_paid | CFO | 293000000 | Fail (hard) | CORE-02: 293000 not in the quote; NUM-11: paid 54562% of base, maximum 150% |
| bodycote-plc | total_remuneration | CEO | 1122000 | Fail (hard) | XF-01: parts add up to 399,723,000, more than the stated 1,122,000; XF-02: parts add up to 399,723,000, stated 1,122,000 |
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
| branicks-group-ag | lti_max | Management Board | 55 | Fail (hard) | COD-01: unit '' is not a target form |
| branicks-group-ag | revenue |  | 100000000 | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote on page 9, link says page 8 |
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-03: quote on page 14, link says page 13 |
| branicks-group-ag | sti_max | Management Board | 35 | Fail (hard) | COD-01: unit '' is not a target form |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: quote not in the source text |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| british-american-tobacco-plc | other_names |  | British American Tobacco Compa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| british-american-tobacco-plc | revenue_by_segment |  | NGP: 397; Strategic Portfolio: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 17,108,000,000 vs 25,610,000,000 (33.2% apart) |
| brooks-macdonald-group-plc | lti_granted | CEO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| brooks-macdonald-group-plc | lti_granted | CFO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bsf-enterprise-plc | largest_holders |  | GBF Nominees Limited 19.48%; B | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| bt-group-plc | fte |  | 81600 | Fail (hard) | CORE-02: 81.6 not in the quote |
| bt-group-plc | headcount |  | 77200 | Fail (hard) | CORE-02: 77.2 not in the quote |
| bt-group-plc | lti_granted | Executive Director (Allison Ki | 2803899 | Fail (hard) | CORE-02: 2803899 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | lti_granted | Executive Director (Simon Lowt | 2057634 | Fail (hard) | CORE-02: 2057634 not in the quote; CORE-03: quote not in the source text |
| bt-group-plc | sti_paid | Executive Director (Allison Ki | 1081000 | Fail (hard) | CORE-02: 1081 not in the quote |
| bt-group-plc | sti_paid | Executive Director (Simon Lowt | 793000 | Fail (hard) | CORE-02: 793 not in the quote |
| btv-vier-lander-bank-ag-9e06fc63 | aggregate_headcount | Mitglieder des Vorstandes | 5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied und Vorsitzender des  | 629100 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Mario | 384200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Dr. M | 356000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | base_salary | Mitglied des Vorstandes (Dr. H | 307700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied und Vorsitzender des  | 14400 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Mario | 10800 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Dr. M | 12700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | benefits_value | Mitglied des Vorstandes (Dr. H | 12400 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | controlling_owner_name |  | CABO Beteiligungsgesellschaft  | Fail (hard) | CORE-02: not in the quote: m |
| btv-vier-lander-bank-ag-9e06fc63 | headcount |  | 1888.7 | Fail (hard) | NUM-05: not a whole number |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied und Vorsitzender des  | 170400 | Fail (hard) | CORE-02: 170.4 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Mario | 63000 | Fail (hard) | CORE-02: 63 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Dr. M | 58300 | Fail (hard) | CORE-02: 58.3 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | pension_contribution | Mitglied des Vorstandes (Dr. H | 48300 | Fail (hard) | CORE-02: 48.3 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | revenue |  | 396520000 | Fail (hard) | CORE-02: 396520 not in the quote |
| btv-vier-lander-bank-ag-9e06fc63 | shareholding_requirement |  | 50 % der variablen Vergütung,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied und Vorsitzender des  | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Mario | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Dr. M | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_max | Mitglied des Vorstandes (Dr. H | 40 | Fail (hard) | CORE-03: quote not in the source text |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied und Vorsitzender des  | 231000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Mario | 141000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Dr. M | 129000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| btv-vier-lander-bank-ag-9e06fc63 | sti_paid | Mitglied des Vorstandes (Dr. H | 37600 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| bunzl-plc | revenue_by_segment |  | North America: 6276.7; Contine | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burberry-group-plc | lti_max | CFO | 175 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burckhardt-compression-holding-ag | benefits_value | CEO | 221000 | Fail (hard) | CORE-02: 221 not in the quote |
| burckhardt-compression-holding-ag | benefits_value | Other members of the Executive | 488000 | Fail (hard) | CORE-02: 488 not in the quote |
| burckhardt-compression-holding-ag | listing_date |  | 2006-06 | Fail (hard) | COD-06: not a year or a date |
| burckhardt-compression-holding-ag | revenue_by_country |  | Europe: 194414; Africa: 10564; | Fail (hard) | CORE-03: quote not in the source text |
| burckhardt-compression-holding-ag | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burckhardt-compression-holding-ag | sti_target | CEO | 0.28 | Fail (hard) | COD-01: unit '' is not a target form |
| burgenland-holding-ag-a95d1abc | largest_holders |  | VERBUND AG 10%; WIEN ENERGIE G | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burgenland-holding-ag-a95d1abc | share_price |  | 71.5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | total_remuneration | Mitglied des Vorstands (Dr. Kl | 5500 | Fail (hard) | XF-01: parts add up to 5,650, more than the stated 5,500; XF-02: parts add up to 5,650, stated 5,500 |
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
| ca-immobilien-anlagen-ag-a9ff4a4a | staff_by_segment |  | Austria: 80; Germany/Switzerla | Fail | CORE-04: no period_end; NUM-08: adds up to 348 vs 254 (37.0% apart) |
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
| calida-holding-ag-1793bfba | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: quote on page 100, link says page 99 |
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
| carclo-plc | base_salary | Chief Executive Officer | 400000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | base_salary | Chief Financial Officer (from  | 280000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Executive Officer | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Financial Officer (from  | 12000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | fte |  | 907 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | headcount |  | 907 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Executive Officer | 149000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Financial Officer (from  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Financial Officer (from  | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | revenue_by_country |  | United Kingdom: 8125; Rest of  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| carclo-plc | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | sti_paid | Chief Executive Officer | 180000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | sti_paid | Chief Financial Officer (from  | 101000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | total_remuneration | Chief Executive Officer | 740000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | total_remuneration | Chief Financial Officer (from  | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| cardiff-property-plc | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| cardiff-property-plc | total_remuneration | Chief Executive Officer | 182000 | Fail (hard) | XF-01: parts add up to 206,000, more than the stated 182,000; XF-02: parts add up to 206,000, stated 182,000 |
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cembra-money-bank-ag-752ce099 | pension_contribution | CEO | 147149 | Fail (hard) | CORE-02: 147149 not in the quote |
| cembra-money-bank-ag-752ce099 | pension_contribution | Active Management Board | 539983 | Fail (hard) | CORE-02: 539983 not in the quote |
| centiel-ag-eeeda54a | pay_currency | Mitglied des Verwaltungsrates  | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | pay_currency | CFO (seit 6. Mai 2025) | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | pay_currency | Geschäftsleitung Total | CHF | Fail | CORE-04: no period_end |
| centiel-ag-eeeda54a | sub_sector |  | Centiel develops and sells thr | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| cherry-se-57089b55 | benefits |  | Company car or car allowance,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| chesnara-plc | lti_granted | Key management personnel | 1200000 | Fail (hard) | CORE-02: 1200000 not in the quote |
| chesnara-plc | pension_contribution | Key management personnel | 100000 | Fail (hard) | CORE-02: 100000 not in the quote |
| chesnara-plc | pension_type |  | defined contribution, 9.5% of  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chesnara-plc | role_disclosure | Key management personnel | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| chesnara-plc | sti_paid | Key management personnel | 700000 | Fail (hard) | CORE-02: 700000 not in the quote |
| chesnara-plc | total_remuneration | Key management personnel | 4100000 | Fail (hard) | CORE-02: 4100000 not in the quote; XF-02: parts add up to 2,000,000, stated 4,100,000 |
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
| clariant-ag-0616ec80 | lti_granted | Other ESC members | 2389017 | Fail (hard) | CORE-02: 2389017 not in the quote |
| clariant-ag-0616ec80 | shareholding_requirement |  | CEO: 150,000 shares; Other ESC | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| clarkson-plc | fte |  | 2103 | Fail (hard) | CORE-03: quote not in the source text |
| clarkson-plc | staff_by_segment |  | Broking: 1504; Financial: 127; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 2,103 vs 2,250 (6.5% apart) |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| close-brothers-group-plc | lti_granted | Chief Executive (from 10 Septe | 726000 | Fail (hard) | CORE-02: 726 not in the quote |
| cloudbreak-discovery-plc | accounting_basis |  | UK-adopted international accou | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 0.4425 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| cmb-tech-nv | benefits |  | Fringe benefits include health | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cmc-markets-plc | ebitda |  | 117842 | Fail (hard) | CORE-02: 117.842 not in the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: quote not in the source text |
| coats-group-plc | lti_granted | Group Chief Executive Officer | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | lti_granted | Group Chief Financial Officer | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| coats-group-plc | share_price |  | 84.55 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| coca-cola-hbc-ag | revenue_by_country |  | Switzerland: 460.2; The Russia | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| coca-cola-hbc-ag | share_price |  | 38.42 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-hbc-ag | staff_by_country |  | Armenia: 345; Austria: 871; Be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | other_names |  | Commerz- und Disconto-Bank; Co | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | revenue_by_country |  | Deutschland: 8043; China einsc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | staff_by_country |  | Deutschland: 23991; China eins | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | total_remuneration | Board of Managing Directors | 17457000 | Fail (hard) | XF-01: parts add up to 20,037,000, more than the stated 17,457,000; XF-02: parts add up to 20,037,000, stated 17,457,000 |
| compagnie-financiere-tradition-sa-940d20ce | pension_type |  | defined contribution schemes;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| compass-group-plc | benefits_value | Group COO, North America | 106000 | Fail (hard) | CORE-03: quote not in the source text |
| compass-group-plc | lti_vested | Group COO, North America | 3882000 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | revenue_by_segment |  | UK: 1419.2; Germany: 2109.3; W | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | exchange |  | London Stock Exchange | Fail (hard) | CORE-02: not in the quote: london stock exchange |
| conduit-holdings-limited | headcount |  | 68 | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | staff_by_country |  | UK: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 2 vs 68 (97.1% apart) |
| contango-holdings-plc | website |  | contango-holdings-plc.co.uk | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | base_salary | Vorstandsvorsitzender (01.12.2 | 1550000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | benefits |  | company car (personal use), re | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| convatec-group-plc | listing_date |  | 2016-10 | Fail (hard) | COD-06: not a year or a date |
| convatec-group-plc | staff_by_country |  | Europe: 5276; North America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | staff_by_segment |  | Operations: 3467; Sales and ma | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | sti_target | Former Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| convatec-group-plc | total_remuneration | Former Chief Executive Officer | 7648000 | Fail (hard) | XF-01: parts add up to 8,565,000, more than the stated 7,648,000; XF-02: parts add up to 8,565,000, stated 7,648,000 |
| corem-property-d | shares_outstanding |  | 1396281000 | Fail (hard) | CORE-02: 1396281000 not in the quote |
| corpus-resources-plc | controlling_owner_name |  | James Antony Stenhouse | Fail (hard) | CORE-02: not in the quote: antony |
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
| critical-metals-plc | share_price |  | 9.1 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | staff_by_country |  | DRC: 49 | Fail | CORE-04: no period_end |
| critical-mineral-resources-plc | fte |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | headcount |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | sti_paid | Chief Financial Officer (CFO)  | 359.203 | Fail (hard) | CORE-02: 359.203 not in the quote |
| cts-eventim-kgaa-1664614e | controlling_owner_name |  | KPS Stiftung | Fail (hard) | CORE-02: not in the quote: stiftung |
| cts-eventim-kgaa-1664614e | lti_granted | CEO | 800000 | Fail (hard) | CORE-02: 800000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | COO | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | CTO (seit 1. Januar 2025) | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | revenue_by_country |  | Germany: 1347630; Italy: 60590 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cts-eventim-kgaa-1664614e | revenue_by_segment |  | Ticketing: 947220; Live Entert | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| curatis-holding-ag-adc33085 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| currys-plc | fte |  | 25076 | Fail (hard) | CORE-02: 25076 not in the quote |
| cykel-ai-plc | total_assets |  | 1537768 | Fail (hard) | CORE-03: quote not in the source text |
| dar-global-plc | ebitda |  | 126600000 | Fail (hard) | CORE-02: 126.6 not in the quote |
| data-modul-ag-9cac6e64 | ebitda |  | 2490000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| data-modul-ag-9cac6e64 | revenue_by_segment |  | Displays: 126601; Systems: 862 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| datwyler-holding-ag-eca04fdb | shares_outstanding |  | 34600000 | Fail (hard) | CORE-02: 34600000 not in the quote |
| datwyler-holding-ag-eca04fdb | sti_max | Executive Committee | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| dcc-energy-plc | lti_granted | Chief Executive | 2051000 | Fail (hard) | CORE-03: quote not in the source text; NUM-12: currency GBP, the role's other amounts EUR |
| dcc-energy-plc | revenue_by_segment |  | DCC Energy: 12990355; DCC Tech | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | sti_paid | Chief Executive | 1928000 | Fail (hard) | CORE-02: 1928 not in the quote |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | COD-06: not a year or a date |
| delticom-ag-na-o-n | share_price |  | 2.14 | Fail (hard) | CORE-03: quote on page 20, link says page 19 |
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
| deutsche-post-ag-b89554ef | pension_contribution | Supply Chain (since August 16, | 100333 | Fail (hard) | CORE-02: 100333 not in the quote |
| deutsche-real-estate-ag-8625fa60 | largest_holders |  | Summit Real Estate Holdings Lt | Fail (hard) | NUM-07: holdings add up to 165.96% |
| deutsche-real-estate-ag-8625fa60 | other_names |  | Geestemünder Bank AG; Geestemü | Fail (hard) | CORE-02: not in the quote: bank |
| deutz-ag-8a315ac8 | lti_target | Vorstandsvorsitzender | 622000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 37000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | total_remuneration | ordentliches Vorstandsmitglied | 955000 | Fail (hard) | XF-01: parts add up to 1,005,000, more than the stated 955,000; XF-02: parts add up to 1,005,000, stated 955,000 |
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
| digia-oyj | aggregate_headcount | Other key personnel | 20 | Fail (hard) | CORE-03: quote not in the source text |
| digia-oyj | shareholding_requirement |  | participants have the chance t | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | revenue_by_segment |  | Controls: 836.4; Seals: 456; L | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| dksh-holding-ag-6576340c | ultimate_parent |  | DKSH Holding Ltd. | Fail (hard) | CORE-02: not in the quote: dksh ltd |
| do-co-aktiengesellschaft-1ce4abbb | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| do-co-aktiengesellschaft-1ce4abbb | revenue_by_country |  | Türkiye: 648.16; Great Britain | Fail | CORE-04: no period_end; NUM-08: adds up to 2,298,120,000 vs 2,461,590,000 (6.6% apart) |
| do-co-aktiengesellschaft-1ce4abbb | staff_by_country |  | Austria: 1641; Germany: 2493;  | Fail | CORE-04: no period_end; NUM-08: adds up to 19,330 vs 14,762 (30.9% apart) |
| docmorris-ag-be190279 | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | fte |  | 2402 | Fail (hard) | CORE-02: 2402 not in the quote |
| domino-s-pizza-group-plc | lti_granted | Former CEO (until 24 November  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| domino-s-pizza-group-plc | lti_granted | Former CFO (until 18 September | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Präsident, exekutiv | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Mitglieder des Verwaltun | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Gruppenleitung | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | CEO/Vorsitzender der Gruppenle | CHF | Fail | CORE-04: no period_end |
| dr-martens-plc | benefits_value | CEO | 5000 | Fail (hard) | CORE-03: quote not in the source text |
| dr-martens-plc | benefits_value | CFO | 19000 | Fail (hard) | CORE-02: 19 not in the quote; CORE-03: quote not in the source text |
| dr-martens-plc | lti_granted | CEO | 1950000 | Fail (hard) | CORE-02: 1950 not in the quote |
| dr-martens-plc | lti_granted | CFO | 1498650 | Fail (hard) | CORE-02: 1498.65 not in the quote |
| draegerwerk-6fd21937 | lti_vested | Executive Board | 2974525 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-6fd21937 | total_remuneration | Vorständin Nachhaltigkeit und  | 458800 | Fail (hard) | XF-01: parts add up to 533,800, more than the stated 458,800; XF-02: parts add up to 533,800, stated 458,800 |
| draegerwerk-be66d9df | lti_granted | Vorstandsvorsitzender | 470700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Vorstand Finanzen und IT und s | 319400 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Vorstand Medizintechnik | 259900 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Vorstand Sicherheitstechnik | 272500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Vorstand Vertrieb und Personal | 177100 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Vorständin Nachhaltigkeit und  | 125900 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | lti_granted | Executive Board | 2974525 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| draegerwerk-be66d9df | total_remuneration | Vorstand Vertrieb und Personal | 1096600 | Fail (hard) | XF-01: parts add up to 1,149,100, more than the stated 1,096,600; XF-02: parts add up to 1,149,100, stated 1,096,600 |
| draegerwerk-be66d9df | total_remuneration | Vorständin Nachhaltigkeit und  | 458800 | Fail (hard) | XF-01: parts add up to 533,800, more than the stated 458,800; XF-02: parts add up to 533,800, stated 458,800 |
| drax-group-plc | fte |  | 3128 | Fail (hard) | CORE-02: 3128 not in the quote |
| drax-group-plc | share_price |  | 837.8 | Fail (hard) | CORE-03: quote not in the source text |
| dsm-firmenich-ag-62366aa6 | controlling_owner_name |  | Firmenich Family | Fail (hard) | CORE-02: not in the quote: family |
| dsm-firmenich-ag-62366aa6 | lti_max | CEO | 300 | Fail (hard) | CORE-03: quote not in the source text |
| dsm-firmenich-ag-62366aa6 | revenue_by_country |  | Switzerland: 214; Netherlands: | Fail | CORE-04: no period_end; NUM-08: adds up to 9,034,000,000 vs 12,521,000,000 (27.8% apart) |
| dt-konsum-real-estae-ag-4e32eb34 | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-konsum-real-estae-ag-4e32eb34 | lti_granted | Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-konsum-real-estae-ag-4e32eb34 | lti_vested | Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-pfandbriefbk-ag-71e35702 | revenue_by_country |  | Germany: 421; Rest of Europe:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-telekom-ag-9dfbbd0c | revenue_by_segment |  | Germany: 25610; United States: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-telekom-ag-9dfbbd0c | staff_by_country |  | Germany: 70751; other EU membe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| emerald-horizon-ag-a6420623 | revenue |  | 224983 | Fail (hard) | CORE-02: 224983 not in the quote; CORE-04: no period_end |
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
| epic-suisse-ag-7c2f8dc4 | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote on page 85, link says page 91 |
| epigenomics-ag-ddb6ea6d | total_remuneration | Vorstand (bis 30.April 2024) | -33000 | Fail (hard) | NUM-04: -33000 outside 0..5e+10; XF-01: parts add up to -32,468, more than the stated -33,000 |
| erste-group-bank-ag | exchange |  | Vienna | Fail (hard) | COD-01: 'Vienna' matches no ISO 10383 exchange |
| erste-group-bank-ag | listing_date |  | 1997-12-04 | Fail (hard) | CORE-02: not in the quote: 1997 |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 960000 | Fail (hard) | CORE-02: 960000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | other_names |  | Erste oesterreichische Spar-Ca | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | staff_by_country |  | Austria: 20111; Czechia: 10097 | Fail | CORE-04: no period_end; NUM-08: adds up to 49,024 vs 46,000 (6.6% apart) |
| essentra-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| eurocell-plc | listing_date |  | 2015-03 | Fail (hard) | COD-06: not a year or a date |
| eurotelesites-ag | revenue_by_country |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | revenue_by_segment |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | sti_paid | CEO | 132000 | Fail (hard) | CORE-02: 132000 not in the quote |
| eurotelesites-ag | sti_paid | CFO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| everest-global-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | controlling_owner_name |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | largest_holders |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| evn-ag-90cea5f3 | listing_date |  | 1989 und 1990 | Fail (hard) | COD-06: not a year or a date |
| evn-ag-90cea5f3 | other_names |  | NIOGAS Niederösterreichische G | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| evn-ag-90cea5f3 | share_price |  | 28.8 | Fail (hard) | CORE-02: 28.8 not in the quote |
| evonext-holdings-sa-be1893c4 | aggregate_headcount | Other members of Group Managem | 2 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | base_salary | CEO | 250000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | base_salary | Other members of Group Managem | 300000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | ebitda |  | -16700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| evonext-holdings-sa-be1893c4 | lti_granted | CEO | 237500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | lti_granted | Other members of Group Managem | 285000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | pay_currency | Other members of Group Managem | CHF | Fail | CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| evonext-holdings-sa-be1893c4 | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| evonext-holdings-sa-be1893c4 | total_remuneration | CEO | 487500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | total_remuneration | Other members of Group Managem | 585000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| evotec-se-0d298d1f | staff_by_country |  | FRANCE: 874; GERMANY: 1143; IT | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 4,553 vs 3,682 (23.7% apart) |
| facc-ag-5f4b658e | headcount |  | 4050 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| facc-ag-5f4b658e | revenue_by_country |  | Germany: 354938; USA: 149717;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| facc-ag-5f4b658e | revenue_by_segment |  | Aerostructures: 345100; Engine | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| facc-ag-5f4b658e | staff_by_country |  | Austria: 3218; Croatia: 473 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 3,691 vs 4,050 (8.9% apart) |
| fair-value-reit-ag-cef1dc63 | exchange |  | Frankfurter Wertpapierbörse | Fail (hard) | COD-01: 'Frankfurter Wertpapierbörse' matches no ISO 10383 exchange |
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
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: quote on page 153, link says page 149 |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: quote on page 103, link says page 102 |
| flughafen-wien-ag | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: quote on page 152, link says page 149 |
| flughafen-wien-ag | role_disclosure | Supervisory Board (non-executi | aggregate | Fail (hard) | CORE-03: quote on page 153, link says page 149 |
| flughafen-wien-ag | sub_sector |  | The FWAG Group generates reven | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| fortec-elektro-b45e5cd6 | controlling_owner_name |  | JotWe GmbH and FloJulCosMAr Gm | Fail (hard) | CORE-02: not in the quote: and |
| framery-group | base_salary | CEO | 219240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | benefits |  | company car, phone and accommo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| framery-group | lti_vested | Management team | 3273000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | revenue_by_country |  | Eurooppa, Lähi-itä ja Afrikka: | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | revenue_by_segment |  | Äänieristetyt työtilat: 216017 | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | staff_by_country |  | Finland: 357; Americas: 21; EM | Fail | CORE-04: no period_end; NUM-08: adds up to 398 vs 484 (17.8% apart) |
| framery-group | sti_paid | CEO | 36000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | total_remuneration | CEO | 255240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | website |  | framery.com | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| fuchs-se-4990a338 | role_disclosure | Gesamtbeträge aller Vorstandsm | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fuchs-se-4990a338 | shareholding_requirement |  | Executive Board members must i | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| galderma-group-ag-8c1dbf8c | shareholding_requirement |  | CEO: 300% of annual base salar | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gam-holding-ag-6ce711d2 | benefits_value | Group Management Board | 822133 | Fail (hard) | CORE-02: 822133 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| gam-holding-ag-6ce711d2 | pension_type |  | defined contribution and defin | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| gam-holding-ag-6ce711d2 | role_disclosure | Group Management Board (aggreg | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gerresheimer-ag-25295c16 | sti_paid | Member of the Board (since Nov | 4000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gerresheimer-ag-25295c16 | sti_paid | Chief Financial Officer (since | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| givaudan-sa-b9d48cbe | benefits_value | EC Members | 645192 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| givaudan-sa-b9d48cbe | pension_contribution | EC Members | 1245193 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| givaudan-sa-b9d48cbe | total_remuneration | EC Members | 14749265 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hamborner-reit-ag-cb84ee44 | listing_date |  | 1954 | Fail (hard) | CORE-02: not in the quote: 1954 |
| hawesko-holding-se-bd2e62b7 | benefits_value | Vorsitzender | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied | 17000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (seit 01.10.2025) | 3000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (bis 09.10.2025) | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | lti_vested | Vorsitzender | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (seit 01.10.2025) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (bis 09.10.2025) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Vorsitzender | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (seit 01.10.2025) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (bis 09.10.2025) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| heidelberg-materials-ag-20cc4657 | shareholding_requirement |  | CEO: shares worth 180% of fixe | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| heidelberg-materials-ag-20cc4657 | total_remuneration | CEO | 8272000 | Fail (hard) | XF-01: parts add up to 8,696,000, more than the stated 8,272,000; XF-02: parts add up to 8,696,000, stated 8,272,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3160000 | Fail (hard) | XF-01: parts add up to 3,338,000, more than the stated 3,160,000; XF-02: parts add up to 3,338,000, stated 3,160,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 1751000 | Fail (hard) | XF-01: parts add up to 1,939,000, more than the stated 1,751,000; XF-02: parts add up to 1,939,000, stated 1,751,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 1259000 | Fail (hard) | XF-01: parts add up to 1,455,000, more than the stated 1,259,000; XF-02: parts add up to 1,455,000, stated 1,259,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3799000 | Fail (hard) | XF-01: parts add up to 4,034,000, more than the stated 3,799,000; XF-02: parts add up to 4,034,000, stated 3,799,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 3506000 | Fail (hard) | XF-01: parts add up to 3,671,000, more than the stated 3,506,000; XF-02: parts add up to 3,671,000, stated 3,506,000 |
| heidelberg-materials-ag-20cc4657 | total_remuneration | Member of the Management Board | 4206000 | Fail (hard) | XF-01: parts add up to 4,370,000, more than the stated 4,206,000; XF-02: parts add up to 4,370,000, stated 4,206,000 |
| helios-solar-ag-797724e7 | total_assets |  | 50089.1 | Fail (hard) | CORE-03: quote not in the source text |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (bis 15.07.202 | 1868000 | Fail (hard) | XF-01: parts add up to 2,641,000, more than the stated 1,868,000; XF-02: parts add up to 2,641,000, stated 1,868,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführerin (seit 01.03. | 993000 | Fail (hard) | XF-01: parts add up to 1,143,000, more than the stated 993,000; XF-02: parts add up to 1,143,000, stated 993,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 1425000 | Fail (hard) | XF-01: parts add up to 1,622,000, more than the stated 1,425,000; XF-02: parts add up to 1,622,000, stated 1,425,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.03.20 | 1380000 | Fail (hard) | XF-01: parts add up to 1,551,000, more than the stated 1,380,000; XF-02: parts add up to 1,551,000, stated 1,380,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 2105000 | Fail (hard) | XF-01: parts add up to 2,369,000, more than the stated 2,105,000; XF-02: parts add up to 2,369,000, stated 2,105,000 |
| helvetia-baloise-holding-ag-784ff8e8 | base_salary | Group CEO (Michael Müller) | 788300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | benefits_value | Group CEO (Michael Müller) | 6300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | ebitda |  | 824200000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | lti_granted | Group CEO (Michael Müller) | 473000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | pension_contribution | Group CEO (Michael Müller) | 193800 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | role_disclosure | Group CEO (Fabian Ruprecht) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | role_disclosure | Group Executive Board | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | staff_by_country |  | Switzerland: 9165; Germany: 23 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| helvetia-baloise-holding-ag-784ff8e8 | sti_paid | Group CEO (Michael Müller) | 357600 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| helvetia-baloise-holding-ag-784ff8e8 | total_remuneration | Group CEO (Michael Müller) | 1819100 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hermana-holding | fte |  | 0 | Fail | CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| hiag-immobilien-holding-ag-3a28978d | sti_max | CEO | 300000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hiag-immobilien-holding-ag-3a28978d | sti_max | Other members of the Executive | 220000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| himalaya-shipping | controlling_owner_name |  | Drew Holdings Ltd. | Fail (hard) | CORE-02: not in the quote: ltd |
| hochtief-ag-3d11e5c0 | pay_currency | Chairman of the Executive Boar | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Chief Financial Officer | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| hochtief-ag-3d11e5c0 | pension_type |  | For new appointees from 2021:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| hochtief-ag-3d11e5c0 | role_disclosure | Chairman of the Executive Boar | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hochtief-ag-3d11e5c0 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hochtief-ag-3d11e5c0 | role_disclosure | Chief Financial Officer | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hochtief-ag-3d11e5c0 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (1) | individual | Fail (hard) | CORE-03: quote not in the source text |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (2) | individual | Fail (hard) | CORE-03: quote not in the source text |
| holcim-ltd-b2e462f1 | ebitda |  | 3992000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holcim-ltd-b2e462f1 | largest_holders |  | UBS Fund Management (Switzerla | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holcim-ltd-b2e462f1 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holcim-ltd-b2e462f1 | revenue_by_segment |  | Europe: 8548; Latin America: 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| huber-suhner-ag-11887265 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| huber-suhner-ag-11887265 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| huber-suhner-ag-11887265 | staff_by_country |  | Switzerland: 1099; Poland: 970 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| hypoport-se-73d5ece9 | staff_by_country |  | Germany: 2314; Netherlands: 59 | Fail | CORE-04: no period_end; NUM-08: adds up to 2,436 vs 2,203 (10.6% apart) |
| industrivarden-c | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Deputy Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Other members of Executive Man | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| inficon-holding-ag-4220ed6f | base_salary | Other members of Group Managem | 365000 | Fail (hard) | CORE-02: 365 not in the quote |
| inficon-holding-ag-4220ed6f | benefits_value | President and Chief Executive  | 244000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| inficon-holding-ag-4220ed6f | benefits_value | Total Group Management | 435000 | Fail (hard) | CORE-02: 435 not in the quote |
| inficon-holding-ag-4220ed6f | benefits_value | Other members of Group Managem | 172000 | Fail (hard) | CORE-02: 172 not in the quote |
| inficon-holding-ag-4220ed6f | lti_granted | Other members of Group Managem | 125000 | Fail (hard) | CORE-02: 125 not in the quote |
| inficon-holding-ag-4220ed6f | pension_contribution | Other members of Group Managem | 19000 | Fail (hard) | CORE-02: 19 not in the quote |
| inficon-holding-ag-4220ed6f | sti_paid | Other members of Group Managem | 95000 | Fail (hard) | CORE-02: 95 not in the quote |
| inficon-holding-ag-4220ed6f | total_remuneration | Other members of Group Managem | 776000 | Fail (hard) | CORE-02: 776 not in the quote |
| infineon-tech-ag-8660f215 | pension_type |  | Defined contribution plan that | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| infineon-tech-ag-8660f215 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Elke  | 1193214 | Fail (hard) | XF-01: parts add up to 1,446,414, more than the stated 1,193,214; XF-02: parts add up to 1,446,414, stated 1,193,214 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Dr. S | 2028369 | Fail (hard) | XF-01: parts add up to 2,281,569, more than the stated 2,028,369; XF-02: parts add up to 2,281,569, stated 2,028,369 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (Andre | 1189604 | Fail (hard) | XF-01: parts add up to 1,442,804, more than the stated 1,189,604; XF-02: parts add up to 1,442,804, stated 1,189,604 |
| infineon-tech-ag-8660f215 | total_remuneration | Management Board member (until | 1197324 | Fail (hard) | XF-01: parts add up to 1,450,524, more than the stated 1,197,324; XF-02: parts add up to 1,450,524, stated 1,197,324 |
| infomaniak-sa-87b05313 | controlling_owner_name |  | Infomaniak Foundation | Fail (hard) | CORE-02: not in the quote: infomaniak |
| infomaniak-sa-87b05313 | sti_max | Executive Chairman | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sti_max | Group Management | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sti_max | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sub_sector |  | Swiss provider of sovereign cl | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| infracore-sa-b3b0dcce | controlling_owner_name |  | Medical Properties Trust, Inc. | Fail (hard) | CORE-02: not in the quote: medical properties trust |
| init-innovation-3237f8ad | other_names |  | init AG | Fail (hard) | CORE-02: not in the quote: init |
| intea-fastigheter-d | fte |  | 60 | Fail (hard) | CORE-02: 60 not in the quote; CORE-03: quote not in the source text |
| intea-fastigheter-d | revenue_by_segment |  | project properties: 265 | Fail | CORE-04: no period_end; NUM-08: adds up to 265,000,000 vs 1,561,000,000 (83.0% apart) |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-03: quote not in the source text |
| intershop-holding-ag-6e9d3cef | benefits |  | benefits in kind | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intica-systems-se-18005922 | sti_max | Vorsitzender des Vorstands | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intica-systems-se-18005922 | sti_max | Mitglied des Vorstands (bis 30 | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ivu-traffic-techn-ag-020c6212 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 4094000 | Fail (hard) | CORE-02: 4094 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3325000 | Fail (hard) | CORE-02: 3325 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 293000 | Fail (hard) | CORE-02: 293 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 266000 | Fail (hard) | CORE-02: 266 not in the quote |
| josef-manner-comp-ag-4b81bd60 | largest_holders |  | Privatstiftung Manner 49.78%;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-07: holdings add up to 173.77% |
| josef-manner-comp-ag-4b81bd60 | other_names |  | Chocoladenfabrik Josef Manner | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| josef-manner-comp-ag-4b81bd60 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| josef-manner-comp-ag-4b81bd60 | revenue_by_segment |  | Süßwaren Österreich: 304316; S | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| julius-bar-gruppe-ag-de864d89 | lti_granted | Executive Board (excl. CEO) | 8100000 | Fail (hard) | CORE-02: 8.1 not in the quote |
| julius-bar-gruppe-ag-de864d89 | pension_contribution | CEO | 620000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| julius-bar-gruppe-ag-de864d89 | role_disclosure | Executive Board (1) | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| julius-bar-gruppe-ag-de864d89 | staff_by_country |  | United States: 1138; China: 40 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,258 vs 7,390 (83.0% apart) |
| julius-bar-gruppe-ag-de864d89 | sti_paid | Executive Board (1) | 4074000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| julius-bar-gruppe-ag-de864d89 | sti_paid | Executive Board (2) | 4713000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| julius-bar-gruppe-ag-de864d89 | total_remuneration | CEO | 8271000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 3,343,000, stated 8,271,000 |
| jungfraubahn-holding-ag-90ceddd3 | aggregate_headcount | Executive Board | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Chairman of the Executive Boar | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Executive Board | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Chairman of the Executive Boar | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Executive Board | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| k2a-knaust-andersson-pref | fte |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| k2a-knaust-andersson-pref | headcount |  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| kapsch-trafficcom-ag-1d6bbc81 | ebitda |  | 20600000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kapsch-trafficcom-ag-1d6bbc81 | revenue_by_country |  | Österreich: 15982; EMEA (exklu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ultimate_parent |  | Traditio-Privatstiftung; CHILD | Fail (hard) | CORE-02: not in the quote: traditio privatstiftung |
| kesko-b | aggregate_headcount | Group Management Board | 7 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kesko-b | role_disclosure | Hallituksen jäsenet | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| khd-humboldt-wedag-eff61cda | revenue_by_country |  | India: 1670; Germany: 272; USA | Fail (hard) | CORE-03: quote not in the source text |
| klingelnberg-ag-d32e6349 | benefits_value | Executive Management | 70334.18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | benefits_value | CEO | 29343.67 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | lti_granted | Executive Management | 510000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | lti_granted | CEO | 170000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| koenig-bauer-ag-1f22b792 | benefits_value | CEO (from June 2025) | 36000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | benefits_value | CFO (from July 2025) | 23000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | benefits_value | Former CEO (until June 2025),  | 22000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 6000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 16000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | benefits_value | Former Member of the Managemen | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | lti_granted | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357 not in the quote |
| koenig-bauer-ag-1f22b792 | lti_granted | Former Member of the Managemen | 312000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | lti_granted | Former Member of the Managemen | 312000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | lti_target | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_max | CEO (from June 2025) | 494000 | Fail (hard) | CORE-02: 494000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_target | CEO (from June 2025) | 330000 | Fail (hard) | CORE-02: 330000 not in the quote |
| koenig-bauer-ag-1f22b792 | total_remuneration | CEO (from June 2025) | 934000 | Fail (hard) | XF-01: parts add up to 959,000, more than the stated 934,000; XF-02: parts add up to 959,000, stated 934,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former CEO (until June 2025),  | 782000 | Fail (hard) | XF-01: parts add up to 813,000, more than the stated 782,000; XF-02: parts add up to 813,000, stated 782,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former Member of the Managemen | 446000 | Fail (hard) | XF-01: parts add up to 507,000, more than the stated 446,000; XF-02: parts add up to 507,000, stated 446,000 |
| krones-ag-f49c3596 | role_disclosure | Sales and Marketing | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| krones-ag-f49c3596 | role_disclosure | International Operations and S | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| krones-ag-f49c3596 | role_disclosure | Filling and Packaging Technolo | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| krones-ag-f49c3596 | total_remuneration | International Operations and S | 1357000 | Fail (hard) | CORE-02: 1357 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| ksb-se-co-kgaa-22d5b1d9 | lti_target | Key management personnel (Mana | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| ksb-se-co-kgaa-22d5b1d9 | sti_target | Key management personnel (Mana | 15 | Fail (hard) | COD-01: unit '' is not a target form |
| kuhne-nagel-international-ag-2949951f | benefits |  | Pension and insurance benefits | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kuhne-nagel-international-ag-2949951f | benefits_value | Chief Executive Officer | 32000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kuhne-nagel-international-ag-2949951f | lti_granted | Chief Executive Officer | 356000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kuhne-nagel-international-ag-2949951f | pension_contribution | Chief Executive Officer | 117000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kuhne-nagel-international-ag-2949951f | revenue_by_segment |  | Sea Logistics: 8817; Air Logis | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kuhne-nagel-international-ag-2949951f | total_remuneration | Chief Executive Officer | 3159000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 3,004,000, stated 3,159,000 |
| kuros-biosciences-ltd-32d9b34e | total_remuneration | CEO | 3909900 | Fail (hard) | XF-01: parts add up to 4,055,500, more than the stated 3,909,900; XF-02: parts add up to 4,055,500, stated 3,909,900 |
| kuros-biosciences-ltd-32d9b34e | total_remuneration | Other EC Members | 3330400 | Fail (hard) | XF-01: parts add up to 3,545,300, more than the stated 3,330,400; XF-02: parts add up to 3,545,300, stated 3,330,400 |
| lem-holding-sa-cc5005fc | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| lenzing-ag-c20f8b4a | base_salary | Vorsitzender des Vorstandes | 333000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | base_salary | Chief Pulp & Chief Technology  | 333000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | base_salary | Member of the Management Board | 333000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | base_salary | Chief Operating Officer (from  | 194000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | base_salary | Member of the Management Board | 111000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | benefits_value | Vorsitzender des Vorstandes | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | benefits_value | Chief Pulp & Chief Technology  | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | benefits_value | Member of the Management Board | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | benefits_value | Chief Operating Officer (from  | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | benefits_value | Member of the Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_granted | Chief Pulp & Chief Technology  | 333000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_granted | Member of the Management Board | 333000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_granted | Chief Operating Officer (from  | 292000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Vorsitzender des Vorstandes | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Chief Pulp & Chief Technology  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Member of the Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Chief Operating Officer (from  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Member of the Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | lti_vested | Managing Board | -46000 | Fail (hard) | CORE-02: -46 not in the quote; NUM-04: -46000 outside 0..5e+10 |
| lenzing-ag-c20f8b4a | pension_contribution | Vorsitzender des Vorstandes | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | pension_contribution | Chief Pulp & Chief Technology  | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | pension_contribution | Member of the Management Board | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | pension_contribution | Chief Operating Officer (from  | 16000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | pension_contribution | Member of the Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | shareholding_requirement |  | Verpflichtung, 25 % der LTI-Au | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Vorsitzender des Vorstandes | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Chief Pulp & Chief Technology  | 248000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Member of the Management Board | 248000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Chief Operating Officer (from  | 144000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Member of the Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | sti_paid | Managing Board | 840000 | Fail (hard) | CORE-02: 840 not in the quote |
| lenzing-ag-c20f8b4a | total_remuneration | Vorsitzender des Vorstandes | 545000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 363,000, stated 545,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Chief Pulp & Chief Technology  | 608000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lenzing-ag-c20f8b4a | total_remuneration | Member of the Management Board | 3011000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 944,000, stated 3,011,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Chief Operating Officer (from  | 547000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 647,000, more than the stated 547,000; XF-02: parts add up to 647,000, stated 547,000 |
| lenzing-ag-c20f8b4a | total_remuneration | Member of the Management Board | 111000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| leonteq-ag-6723ca54 | benefits |  | representation and lunch allow | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| linz-textil-holding-ag-e11cf1a9 | ebitda |  | 939336 | Fail (hard) | CORE-02: 939.336 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| linz-textil-holding-ag-e11cf1a9 | largest_holders |  | TYLE-Privatstiftung 80%; Tyle  | Fail (hard) | NUM-07: holdings add up to 160% |
| linz-textil-holding-ag-e11cf1a9 | listing_date |  | 1872 | Fail (hard) | COD-06: not a year or a date |
| logitech-international-s-a-0a74f2ba | pension_type |  | defined benefit pension plans  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| logitech-international-s-a-0a74f2ba | total_remuneration | Chief Executive Officer | 8757096 | Fail (hard) | XF-01: parts add up to 9,228,576, more than the stated 8,757,096; XF-02: parts add up to 9,228,576, stated 8,757,096 |
| lonza-group-ag-e4f248d2 | accounting_basis |  | IFRS Accounting Standards | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| lonza-group-ag-e4f248d2 | aggregate_headcount | Executive Committee | 8.8 | Fail (hard) | NUM-05: not a whole number |
| lonza-group-ag-e4f248d2 | base_salary | Executive Committee | 5390000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lonza-group-ag-e4f248d2 | benefits_value | CEO | 350000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lonza-group-ag-e4f248d2 | benefits_value | Executive Committee | 1990000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lufthansa-ag-0bc3d92c | controlling_owner_name |  | Deutsche Lufthansa Aktiengesel | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| maschinenfabrik-berthold-hermle-6808fdaf | exchange |  | Stuttgart Stock Exchange | Fail (hard) | COD-01: 'Stuttgart Stock Exchange' matches no ISO 10383 exchange |
| maschinenfabrik-berthold-hermle-6808fdaf | pension_type |  | defined contribution, up to 1, | Fail (hard) | CORE-03: quote not in the source text |
| maschinenfabrik-berthold-hermle-6808fdaf | revenue_by_country |  | Federal Republic of Germany: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 232,367,000 vs 491,891,000 (52.8% apart) |
| maschinenfabrik-berthold-hermle-6808fdaf | revenue_by_segment |  | Domestic companies: 255538; Fo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 983,782,000 vs 491,891,000 (100.0% apart) |
| maschinenfabrik-berthold-hermle-6808fdaf | staff_by_country |  | Germany: 1228 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,228 vs 1,639 (25.1% apart) |
| masterflex-96d8f19f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| max-automation-se-e7586bc1 | pay_currency | Geschäftsführender Direktor (C | EUR | Fail | CORE-04: no period_end |
| max-automation-se-e7586bc1 | pay_currency | Geschäftsführender Direktor (C | EUR | Fail | CORE-04: no period_end |
| mayr-melnhof-karton-ag-ef1c26e1 | staff_by_country |  | Poland: 3027; Germany: 2091; A | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mbb-se-be761dea | lti_target | Executive Chairman | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mbb-se-be761dea | lti_target | CFO | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mch-group-ag-c6fc7898 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| medartis-holding-ag-4ef02932 | base_salary | CEO | 700000 | Fail (hard) | CORE-02: 700 not in the quote |
| medartis-holding-ag-4ef02932 | shareholding_requirement |  | BoD: shares equal to one year  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| medartis-holding-ag-4ef02932 | sti_max | Other members of the EMB | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| meier-tobler-group-ag-f96a3151 | benefits |  | Geschäftsfahrzeug | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| melhus-sparebank | exchange |  | Euronext | Fail (hard) | CORE-02: not in the quote: euronext; COD-01: 'Euronext' matches no ISO 10383 exchange |
| melhus-sparebank | isin |  | NO0006001908 | Fail (hard) | CORE-02: not in the quote: no0006001908 |
| melhus-sparebank | pay_currency | Banksjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Ass. Banksjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder PM | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder BM | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Leder Forsikring& Marked | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Lederjuridisk | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Kredittsjef | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pay_currency | Risk Compliance Manager | NOK | Fail | CORE-04: no period_end |
| melhus-sparebank | pension_type |  | defined contribution, 7 % of p | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| melhus-sparebank | total_assets |  | 15200000000 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chairman of the Board of Manag | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chief Technology Officer, Deve | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Integrity, Governance & Sustai | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Human Relations & Labour Direc | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Chief Technology Officer, Deve | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Integrity, Governance & Sustai | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Production, Quality & Supply C | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Human Relations & Labour Direc | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Greater China (February 1 - De | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Greater China (January 1 - Jul | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | role_disclosure | Finance & Controlling (January | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Sales & Customer Experience (F | 1730000 | Fail (hard) | XF-01: parts add up to 1,859,000, more than the stated 1,730,000; XF-02: parts add up to 1,859,000, stated 1,730,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Human Relations & Labour Direc | 695000 | Fail (hard) | XF-01: parts add up to 976,000, more than the stated 695,000; XF-02: parts add up to 976,000, stated 695,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Integrity, Governance & Sustai | 445000 | Fail (hard) | XF-01: parts add up to 486,000, more than the stated 445,000; XF-02: parts add up to 486,000, stated 445,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Production, Quality & Supply C | 154000 | Fail (hard) | XF-01: parts add up to 166,000, more than the stated 154,000; XF-02: parts add up to 166,000, stated 154,000 |
| mercedes-benz-group-ag-1545d718 | total_remuneration | Greater China (February 1 - De | 2104000 | Fail (hard) | XF-01: parts add up to 2,193,000, more than the stated 2,104,000; XF-02: parts add up to 2,193,000, stated 2,104,000 |
| mindmaze-therapeutics-holding-sa-b2339575 | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| ming-le-sports-ag-fc0affd5 | sti_target | Vorstandsmitglied | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote; COD-01: unit '' is not a target form |
| mobilezone-holding-ag-fc013b59 | aggregate_headcount | Management Board | 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | benefits |  | lump-sum expenses approved by  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | role_disclosure | Executive Delegate of the Boar | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Management Board | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Executive Delegate of the Boar | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| molecular-partners-ag-86d659ae | pension_type |  | defined benefit plans; compuls | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mueller-die-lila-logistik-se-f3c40a4b | other_names |  | Müller – Lila Logistik AG | Fail (hard) | CORE-03: quote not in the source text |
| mueller-die-lila-logistik-se-f3c40a4b | revenue_by_country |  | Deutschland: 214187; Ausland:  | Fail | CORE-04: no period_end; NUM-08: adds up to 250,478,000 vs 11,374,899 (2102.0% apart) |
| mueller-die-lila-logistik-se-f3c40a4b | revenue_by_segment |  | Lila Operating: 249948; Lila R | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 250,478,000 vs 11,374,899 (2102.0% apart) |
| muench-rueckversicherungs-gesellschaft-5bba2145 | controlling_owner_name |  | Munich Re | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | lti_vested | Member of the Board of Managem | 1828378 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | lti_vested | Board of Management | 14200000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | pension_contribution | Board of Management | 4000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | revenue_by_segment |  | Reinsurance – Life and health: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | role_disclosure | Member of the Board of Managem | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 934365 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | sti_paid | Member of the Board of Managem | 811620 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Chair of the Board of Manageme | 7088819 | Fail (hard) | XF-01: parts add up to 8,449,244, more than the stated 7,088,819; XF-02: parts add up to 8,449,244, stated 7,088,819 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4295095 | Fail (hard) | XF-01: parts add up to 4,901,220, more than the stated 4,295,095; XF-02: parts add up to 4,901,220, stated 4,295,095 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4937800 | Fail (hard) | XF-01: parts add up to 5,888,950, more than the stated 4,937,800; XF-02: parts add up to 5,888,950, stated 4,937,800 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Member of the Board of Managem | 4221643 | Fail (hard) | XF-01: parts add up to 4,560,518, more than the stated 4,221,643; XF-02: parts add up to 4,560,518, stated 4,221,643 |
| muench-rueckversicherungs-gesellschaft-5bba2145 | total_remuneration | Board of Management | 47000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nagarro-se-9ed14a85 | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nagarro-se-9ed14a85 | role_disclosure | Chairperson of the Management  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nagarro-se-9ed14a85 | role_disclosure | Member of the Management Board | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nagarro-se-9ed14a85 | role_disclosure | Member of the Management Board | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| naturenergie-holding-ag-a1be2274 | pension_contribution | Geschäftsleitung | 156656 | Fail (hard) | CORE-02: 156656 not in the quote |
| norcom-information-technology-2811f08c | listing_date |  | 1999-10 | Fail (hard) | COD-06: not a year or a date |
| norcom-information-technology-2811f08c | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| nordwest-handel-ag-ee04116a | pay_currency | Member of the Executive Board  | EUR | Fail | CORE-04: no period_end |
| omv-ag-2c5e8b21 | lti_target | Chairman of the Executive Boar | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Energ | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Fuels | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Vice Presiden | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Deputy Chairman of the  | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Officer Marke | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| orbis-se-3d0d94ff | lti_max | Vorstandssprecher | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | lti_max | Vorstand | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | lti_max | Vorstand (until December 2025) | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| orbis-se-3d0d94ff | sti_max | Vorstandssprecher | 18 | Fail (hard) | COD-01: unit '' is not a target form |
| orior-ag-bfeb91d6 | aggregate_headcount | Executive Committee excl. CFO | 3.1 | Fail (hard) | NUM-05: not a whole number |
| orior-ag-bfeb91d6 | aggregate_headcount | Former Executive Committee mem | 0.4 | Fail (hard) | NUM-04: 0.4 outside 1..500; NUM-05: not a whole number |
| ostasiatiske | exchange |  | NASDAQ OMX Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ OMX Copenhagen A/S' matches no ISO 10383 exchange |
| palfinger-ag-e07e19f6 | exchange_segment |  | Prime Market | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| palfinger-ag-e07e19f6 | revenue_by_country |  | Inland: 44423.1; EU: 21235.8;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 77,550,800 vs 2,339,288,000 (96.7% apart) |
| palfinger-ag-e07e19f6 | staff_by_country |  | Österreich: 2707; Russland: 15 | Fail | CORE-04: no period_end; NUM-08: adds up to 5,657 vs 12,358 (54.2% apart) |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| paratus-energy | revenue_by_segment |  | Seagems: 265; Fontis: 187 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 452,000,000 vs 153,200,000 (195.0% apart) |
| partners-group-holding-ag-d09fd15d | lti_granted | Chief Executive Officer | 14055000 | Fail (hard) | CORE-02: 14055 not in the quote |
| partners-group-holding-ag-d09fd15d | lti_granted | Executive Team | 54733000 | Fail (hard) | CORE-02: 54733 not in the quote |
| partners-group-holding-ag-d09fd15d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| path2-hydrogen-ag-4a522574 | benefits |  | mögliche Vereinbarungen über e | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| path2-hydrogen-ag-4a522574 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| patrizia-se-41659152 | revenue_by_segment |  | Investment Management: 264348; | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 276,070,000 vs 258,416,000 (6.8% apart) |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| pfeiffer-vacuum-tech-ag-a38e65f0 | listing_date |  | 2023-12-29 | Fail (hard) | CORE-02: not in the quote: 2023 29 |
| pferdewetten-de-ag-07705286 | aggregate_headcount | Vorstand | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| phoenix-mecano-ag-d882ab5c | base_salary | Management | 1934000 | Fail (hard) | CORE-02: 1934 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | Chairman of the Board of Direc | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | CEO | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | benefits_value | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | controlling_owner_name |  | Herr Günter Rothenberger | Fail (hard) | CORE-02: not in the quote: nter |
| pittler-maschinenfabrik-ag-fb62b449 | other_names |  | Leipziger Werkzeugmaschinenfab | Fail (hard) | CORE-03: quote not in the source text |
| planoptik-ag-9429909d | sti_target | Vorstandsmitglied | 10 | Fail (hard) | COD-01: unit '' is not a target form |
| pne-ag-1fc0baf7 | benefits |  | Health and long-term care insu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| pne-ag-1fc0baf7 | lti_max | Vorstandsvorsitzender | 630000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | lti_max | Vorstandsmitglied (Harald Wilb | 540000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | lti_max | Vorstandsmitglied (Roland Stan | 495000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | role_disclosure | Vorstandsmitglied (until March | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | sti_paid | Vorstandsvorsitzender | 101000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | sti_paid | Vorstandsmitglied (Roland Stan | 79000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | total_remuneration | Vorstandsvorsitzender | 469000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pne-ag-1fc0baf7 | total_remuneration | Vorstandsmitglied (Roland Stan | 378000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| polytec-holding-ag-2a433fdb | revenue_by_country |  | Austria: 3900; Germany: 359275 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| polytec-holding-ag-2a433fdb | share_price |  | 3.3 | Fail (hard) | CORE-02: 3.3 not in the quote |
| porr-ag-127fa41a | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porr-ag-127fa41a | controlling_owner_name |  | Syndicate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porr-ag-127fa41a | largest_holders |  | Syndicate 32.1% | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porr-ag-127fa41a | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porr-ag-127fa41a | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porsche-ag-531bb563 | benefits |  | discounts and employee benefit | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| porsche-ag-531bb563 | controlling_owner_name |  | Volkswagen Aktiengesellschaft | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| porsche-ag-531bb563 | listing_date |  | 2022-09-29 | Fail (hard) | CORE-02: not in the quote: 2022 29 |
| porsche-ag-531bb563 | shares_outstanding |  | 911000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porsche-ag-531bb563 | total_remuneration | Chairman of the Executive Boar | 1456359 | Fail (hard) | XF-01: parts add up to 1,529,692, more than the stated 1,456,359; XF-02: parts add up to 1,529,692, stated 1,456,359 |
| porsche-ag-531bb563 | total_remuneration | Deputy Chairman of the Executi | 197600 | Fail (hard) | XF-01: parts add up to 266,588, more than the stated 197,600; XF-02: parts add up to 266,588, stated 197,600 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 817464 | Fail (hard) | XF-01: parts add up to 1,135,839, more than the stated 817,464; XF-02: parts add up to 1,135,839, stated 817,464 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board, | 814050 | Fail (hard) | XF-01: parts add up to 1,132,426, more than the stated 814,050; XF-02: parts add up to 1,132,426, stated 814,050 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 1572933 | Fail (hard) | XF-01: parts add up to 1,820,294, more than the stated 1,572,933; XF-02: parts add up to 1,820,294, stated 1,572,933 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 992610 | Fail (hard) | XF-01: parts add up to 1,377,613, more than the stated 992,610; XF-02: parts add up to 1,377,613, stated 992,610 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 163610 | Fail (hard) | XF-01: parts add up to 223,136, more than the stated 163,610; XF-02: parts add up to 223,136, stated 163,610 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 360662 | Fail (hard) | XF-01: parts add up to 499,871, more than the stated 360,662; XF-02: parts add up to 499,871, stated 360,662 |
| porsche-ag-531bb563 | total_remuneration | Member of the Executive Board; | 362721 | Fail (hard) | XF-01: parts add up to 501,930, more than the stated 362,721; XF-02: parts add up to 501,930, stated 362,721 |
| procredit-holding-ag-74495a3c | headcount |  | 4660 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| procredit-holding-ag-74495a3c | listing_date |  | 2016-12-22 | Fail (hard) | CORE-02: not in the quote: 2016 |
| procredit-holding-ag-74495a3c | revenue_by_segment |  | South Eastern Europe: 319141;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 565,433,000 vs 439,266,000 (28.7% apart) |
| procredit-holding-ag-74495a3c | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| procredit-holding-ag-74495a3c | website |  | procredit-holding.com | Fail (hard) | CORE-02: not in the quote: procredit holding |
| public-property-invest | largest_holders |  | Samhällsbyggnadsbolaget i Nord | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| public-property-invest | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | lti_target | Vorstandsvorsitzender (until D | 250000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | lti_target | Mitglied des Vorstands | 130000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | role_disclosure | Former Executives, total | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 10000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | pension_contribution | Member of the Management Board | 15000 | Fail (hard) | CORE-02: 15 not in the quote |
| rath-ag-9e9ac567 | pension_contribution | Member of the Management Board | 10000 | Fail (hard) | CORE-02: 10 not in the quote |
| rath-ag-9e9ac567 | sti_paid | Member of the Management Board | 44000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 349000 | Fail (hard) | XF-01: parts add up to 364,000, more than the stated 349,000; XF-02: parts add up to 364,000, stated 349,000 |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 419000 | Fail (hard) | XF-01: parts add up to 429,000, more than the stated 419,000; XF-02: parts add up to 429,000, stated 419,000 |
| readcrest-capital-ag-e4689651 | role_disclosure | CEO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| readcrest-capital-ag-e4689651 | role_disclosure | CFO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| revolutionrace | staff_by_country |  | Sweden: 160 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 160 vs 170 (5.9% apart) |
| revolutionrace | sub_sector |  | Our driving force is to develo | Fail (hard) | CORE-03: quote not in the source text |
| rheinmetall-ag-cf2ff08a | sti_max | Vorsitzender des Vorstands | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (bis 31 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rhoen-klinikum-0a013089 | role_disclosure | Vorstandsvorsitzender (ab 1. N | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| roche-holding-ag-5abd8231 | benefits_value | Other members of the Corporate | 120000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| roche-holding-ag-5abd8231 | lti_granted | CEO Roche Group | 2788169 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| roche-holding-ag-5abd8231 | lti_granted | Other members of the Corporate | 10000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| roche-holding-ag-5abd8231 | pension_contribution | Other members of the Corporate | 1597894 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| roche-holding-ag-5abd8231 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| roche-holding-ag-5abd8231 | shareholding_requirement |  | CEO Roche Group: Shares and/or | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rosenbauer | base_salary | Executive Board member (since  | 601000 | Fail (hard) | CORE-03: quote on page 3, link says page 2 |
| rosenbauer | base_salary | Executive Board member (since  | 263000 | Fail (hard) | CORE-03: quote on page 3, link says page 2 |
| rosenbauer | pension_contribution | Executive Board member (since  | 0 | Fail (hard) | CORE-03: quote on page 3, link says page 2 |
| rosenbauer | pension_contribution | Executive Board member (since  | 0 | Fail (hard) | CORE-03: quote on page 3, link says page 2 |
| rosenbauer | revenue_by_country |  | Austria: 105546; USA: 343575;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rosenbauer | role_disclosure | Executive Board member (since  | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| rosenbauer | role_disclosure | Executive Board member (since  | individual | Fail (hard) | CORE-03: quote not in the source text |
| rosenbauer | staff_by_country |  | Austria: 1632; Germany: 1038;  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,312 vs 4,922 (12.4% apart) |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Chairman of the Executi | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Former Executive Board member  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | total_remuneration | Executive Board member (since  | 601000 | Fail (hard) | CORE-03: quote on page 3, link says page 2; XF-01: parts add up to 1,009,000, more than the stated 601,000; XF-02: parts add up to 1,009,000, stated 601,000 |
| rosenbauer | total_remuneration | Executive Board member (since  | 263000 | Fail (hard) | CORE-03: quote on page 3, link says page 2; XF-01: parts add up to 501,000, more than the stated 263,000; XF-02: parts add up to 501,000, stated 263,000 |
| rosenbauer | total_remuneration | Executive Board member | 406000 | Fail (hard) | XF-01: parts add up to 741,000, more than the stated 406,000; XF-02: parts add up to 741,000, stated 406,000 |
| rosenbauer | total_remuneration | Former Executive Board member  | 641000 | Fail (hard) | CORE-02: 641 not in the quote |
| s-d-standard-etc | controlling_owner_name |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-d-standard-etc | share_price |  | 1.688 | Fail (hard) | CORE-02: 1.688 not in the quote |
| s-d-standard-etc | ultimate_parent |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| saf-holland-se-e07079b5 | other_names |  | Otto Sauer Achsenfabrik GmbH;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| saf-holland-se-e07079b5 | staff_by_country |  | EMEA: 2282; Americas: 2480; AP | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | fiscal_year_end |  | YYYY-12-31 | Fail (hard) | COD-06: not a valid date |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | pay_currency | Executive Management | CHF | Fail | CORE-04: no period_end |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | revenue_by_country |  | Europe: 11577; North America:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| sap-se-b1a5f6d4 | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sap-se-b1a5f6d4 | fte |  | 110650 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sap-se-b1a5f6d4 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | lti_max | Member of the Executive Board  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| sap-se-b1a5f6d4 | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sap-se-b1a5f6d4 | revenue_by_segment |  | Cloud: 21023; Software license | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sap-se-b1a5f6d4 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| schindler-holding-ag-d2b61912 | base_salary | Nonexecutive member with opera | 242000 | Fail (hard) | CORE-02: 242 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | base_salary | Member of the Supervisory and  | 820000 | Fail (hard) | CORE-02: 820 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | base_salary | Member of the Supervisory and  | 895000 | Fail (hard) | CORE-02: 895 not in the quote |
| schindler-holding-ag-d2b61912 | base_salary | Executive member with operatio | 665000 | Fail (hard) | CORE-02: 665 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | benefits_value | Member of the Supervisory and  | 87000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | benefits_value | Executive member with operatio | 38000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | lti_granted | Member of the Supervisory and  | 907000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | lti_granted | Executive member with operatio | 349000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | lti_max | CEO | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| schindler-holding-ag-d2b61912 | lti_max | Group Executive Committee | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| schindler-holding-ag-d2b61912 | pension_contribution | Nonexecutive member with opera | 20000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | pension_contribution | Member of the Supervisory and  | 207000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | pension_contribution | Executive member with operatio | 177000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | role_disclosure | Nonexecutive member with opera | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | role_disclosure | Member of the Supervisory and  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | role_disclosure | Member of the Supervisory and  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | role_disclosure | Executive member with operatio | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | sti_paid | Member of the Supervisory and  | 726000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | sti_paid | Executive member with operatio | 370000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | total_remuneration | Chairman (as of the General Me | 1826000 | Fail (hard) | XF-01: parts add up to 1,903,000, more than the stated 1,826,000; XF-02: parts add up to 1,903,000, stated 1,826,000 |
| schindler-holding-ag-d2b61912 | total_remuneration | former Chairman (until the Gen | 990000 | Fail (hard) | XF-01: parts add up to 1,087,000, more than the stated 990,000; XF-02: parts add up to 1,087,000, stated 990,000 |
| schindler-holding-ag-d2b61912 | total_remuneration | Nonexecutive member with opera | 262000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | total_remuneration | Member of the Supervisory and  | 2747000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schindler-holding-ag-d2b61912 | total_remuneration | Executive member with operatio | 1599000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schlatter-industries-ag-e8b6df3d | pension_contribution | Group Management | 219016 | Fail (hard) | CORE-02: 219016 not in the quote |
| schott-pharma-ag-co-kgaa-26f01ea5 | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| schweiter-technologies-ag-b9dd7eca | aggregate_headcount | Group Management | 2 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | Group Management | 232000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | CEO | 143000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | shareholding_requirement |  | Share-based compensation for B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| seb-a | benefits_value | CEO | 385000 | Fail (hard) | CORE-02: 385 not in the quote |
| seb-a | benefits_value | Deputy CEO (Mats Torstendahl) | 236000 | Fail (hard) | CORE-02: 236 not in the quote |
| seb-a | benefits_value | Deputy CEO (Jonas Ahlström) | 205000 | Fail (hard) | CORE-02: 205 not in the quote |
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
| secunet-security-ag-c4d9b7e4 | headcount |  | 1171 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| secunet-security-ag-c4d9b7e4 | total_assets |  | 410700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sed-energy | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| semperit-ag-holding-2a7b594a | listing_date |  | 1890 | Fail (hard) | COD-06: not a year or a date |
| sensirion-holding-ag-0c2fb93b | aggregate_headcount | Total EC | 6 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | base_salary | CEO | 444184 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | base_salary | Other EC | 1213918 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | base_salary | Total EC | 1658102 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | role_disclosure | CEO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | role_disclosure | Other EC | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | role_disclosure | Total EC | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | sti_paid | CEO | 102168 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | sti_paid | Other EC | 252170 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | sti_paid | Total EC | 354339 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | total_remuneration | CEO | 628853 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 546,352, stated 628,853 |
| sensirion-holding-ag-0c2fb93b | total_remuneration | Other EC | 1686136 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 1,466,088, stated 1,686,136 |
| sensirion-holding-ag-0c2fb93b | total_remuneration | Total EC | 2314989 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,012,441, stated 2,314,989 |
| sentia | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| sentia | controlling_owner_name |  | Ratos AB | Fail (hard) | CORE-03: quote not in the source text |
| sentia | largest_holders |  | Ratos AB 39% | Fail (hard) | CORE-03: quote not in the source text |
| sentia | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| sentia | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_country |  | Norge: 9404; Sverige: 2369 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | revenue_by_segment |  | HENT: 9404; Sentia Sverige: 23 | Fail (hard) | CORE-03: quote not in the source text |
| sentia | staff_by_segment |  | HENT: 1338; Sentia Sverige: 17 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,516 vs 6 (25166.7% apart) |
| sgs-ag-65380806 | aggregate_headcount | Other ExCo | 13 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | benefits_value | Chief Executive Officer | 24000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | pension_contribution | Chief Executive Officer | 119000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | revenue_by_country |  | North America: 1.5 | Fail | CORE-04: no period_end |
| sgs-ag-65380806 | total_remuneration | Chief Executive Officer | 1393000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 4,355,000, more than the stated 1,393,000; XF-02: parts add up to 4,355,000, stated 1,393,000 |
| siemens-health-ag-1a42fb66 | revenue_by_country |  | Europe, C.I.S., Africa, Middle | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| siemens-health-ag-1a42fb66 | sub_sector |  | Siemens Healthineers offers im | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sino-german-united-ag-388acb2d | role_disclosure | Vorstand/Chief Operating Offic | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 44000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 39000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | benefits_value | COO | 32000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | benefits_value | CBO | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | benefits_value | CFO | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | role_disclosure | COO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | role_disclosure | CFO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | sti_paid | COO | 347000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | sti_paid | CBO | 246000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sixt-se-8094cf8b | sti_paid | CFO | 198000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| skan-group-ag-684bb9fa | sti_paid | CEO | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| smg-swiss-marketplace-group-holding-ag-40385dff | revenue_by_segment |  | Real Estate: 164147; Automotiv | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| snp-schneider-neureither-f82bee76 | fiscal_year_end |  | 2023-12-31 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| snp-schneider-neureither-f82bee76 | headcount |  | 1500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| snp-schneider-neureither-f82bee76 | revenue |  | 203400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softing-ag-365a9352 | share_price |  | 2.3 | Fail (hard) | CORE-03: quote not in the source text |
| softwareone-holding-ag-ee2860ae | lti_granted | CFO (until May 31, 2025) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softwareone-holding-ag-ee2860ae | lti_granted | Other EB members | 1320250 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softwareone-holding-ag-ee2860ae | lti_target | Other EB members | 27 | Fail (hard) | COD-01: unit '' is not a target form |
| softwareone-holding-ag-ee2860ae | sti_target | Other EB members | 22 | Fail (hard) | COD-01: unit '' is not a target form |
| sonova-holding-ag-e87e288d | pension_type |  | Sonova Group has both defined  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| st-galler-kantonalbank-ag-ba864955 | shareholding_requirement |  | For Board of Directors: 30% of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stabilus-se-52dccb73 | listing_date |  | 2014-05 | Fail (hard) | COD-06: not a year or a date |
| stabilus-se-52dccb73 | revenue_by_country |  | Germany: 367128; Romania: 1322 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stabilus-se-52dccb73 | revenue_by_segment |  | EMEA: 542183; Americas: 480899 | Fail (hard) | CORE-03: quote not in the source text |
| stabilus-se-52dccb73 | sub_sector |  | The object of the Company is t | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stadlauer-malzfabrik-ag-8a23c30d | sub_sector |  | Holdingfunktion | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| starragtornos-group-ag-15e3832b | base_salary | Other members of the Executive | 637000 | Fail (hard) | CORE-02: 637 not in the quote |
| starragtornos-group-ag-15e3832b | benefits_value | Other members of the Executive | 26000 | Fail (hard) | CORE-02: 26 not in the quote |
| starragtornos-group-ag-15e3832b | pension_contribution | Other members of the Executive | 130000 | Fail (hard) | CORE-02: 130 not in the quote |
| starragtornos-group-ag-15e3832b | sti_paid | Other members of the Executive | 7000 | Fail (hard) | CORE-02: 7 not in the quote |
| starragtornos-group-ag-15e3832b | total_remuneration | Other members of the Executive | 799000 | Fail (hard) | CORE-02: 799 not in the quote |
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
| strabag-se-8e9d954e | staff_by_segment |  | North + West: 23161 | Fail | CORE-04: no period_end; NUM-08: adds up to 23,161 vs 88,556 (73.8% apart) |
| straumann-holding-ag-d8e91d7f | lti_vested | CEO | 180000 | Fail (hard) | CORE-02: 180 not in the quote |
| subsea7 | pension_contribution | Chief Financial Officer | 60500 | Fail (hard) | CORE-03: quote not in the source text |
| subsea7 | revenue_by_country |  | Norway: 1664.6; United Kingdom | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| subsea7 | staff_by_country |  | Angola: 242; Australia: 246; B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| suss-microtec-se-b7558a97 | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | fte |  | 1497 | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | largest_holders |  | Janus Henderson 9.89%; Univers | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | revenue_by_country |  | North America: 46; Asia / Paci | Fail (hard) | CORE-03: quote not in the source text |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (Klaus Einfalt) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (János Váczi) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| swiss-re-ag-6528d850 | benefits_value | Group Chief Executive Officer | 27000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | lti_vested | Group Chief Executive Officer | 3394000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | sti_max | Group Chief Executive Officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| swiss-re-ag-6528d850 | total_remuneration | Group Chief Executive Officer | 6065000 | Fail (hard) | XF-01: parts add up to 6,292,000, more than the stated 6,065,000; XF-02: parts add up to 6,292,000, stated 6,065,000 |
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
| telekom-austria-ag-62fec5fa | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| temenos-ag-21209ec1 | shareholding_requirement |  | CEO: 5 times annual fixed sala | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| the-swatch-group-ag-6a144b9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| thurgauer-kantonalbank-3b36a058 | benefits |  | For Bank Council members: occa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| thurgauer-kantonalbank-3b36a058 | pension_type |  | defined contribution. For fixe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| tx-group-ag-cdcf98d0 | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| uie | listing_date |  | 1983-05 | Fail (hard) | COD-06: not a year or a date |
| uie | share_price |  | 386.5 | Fail (hard) | CORE-03: quote not in the source text |
| uie | sti_max | Managing Director | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| utd-internet-ag-fa5f4803 | controlling_owner_name |  | Ralph Dommermuth | Fail (hard) | CORE-02: not in the quote: ralph |
| uzin-utz-se-808b3f93 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| vat-group-ag-ccdd96de | pay_currency | CEO (since January 1, 2024) | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pay_currency | Other GEC | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pension_type |  | occupational pension plans, in | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| verbio-se-9b8df34d | ebitda |  | 193900000 | Fail (hard) | CORE-02: 193.9 not in the quote; CORE-03: quote not in the source text |
| verbio-se-9b8df34d | share_price |  | 29.8 | Fail (hard) | CORE-02: 29.8 not in the quote; CORE-03: quote not in the source text |
| verbund | other_names |  | Österreichische Elektrizitätsw | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Administratrice (Membre non ex | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Ancien Président | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villeroy-boch-ag-c5a85d57 | accounting_basis |  | IFRS Accounting Standards | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorstand Digitalisierung / IT  | 17300 | Fail (hard) | CORE-03: quote on page 13, link says page 11 |
| villeroy-boch-ag-c5a85d57 | benefits_value | Vorständin HR / Organisationse | 16100 | Fail (hard) | CORE-03: quote on page 13, link says page 11 |
| villeroy-boch-ag-c5a85d57 | exchange_segment |  | Prime Standard | Fail (hard) | CORE-03: quote on page 85, link says page 81 |
| villeroy-boch-ag-c5a85d57 | listing_date |  | 1992 | Fail (hard) | CORE-02: not in the quote: 1992 |
| villeroy-boch-ag-c5a85d57 | pension_type |  | defined-contribution pension p | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villeroy-boch-ag-c5a85d57 | role_disclosure | Vorstandsvorsitzende (seit 01. | individual | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | sub_sector |  | Group is a leading internation | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstandsvorsitzende (seit 01. | 1616800 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,340,100, stated 1,616,800 |
| villeroy-boch-ag-c5a85d57 | total_remuneration | Vorstand Finanzen (seit 01.01. | 869400 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 661,900, stated 869,400 |
| vincorion-se-16aba459 | sub_sector |  | VINCORION offers Vehicle Syste | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | controlling_owner_name |  | Dr. Martin Heuser and Volker P | Fail (hard) | CORE-02: not in the quote: and |
| viscom-se-859e40d6 | ebitda |  | -1815000 | Fail (hard) | CORE-02: -1.815 not in the quote |
| viscom-se-859e40d6 | listing_date |  | 2006-05 | Fail (hard) | COD-06: not a year or a date |
| viscom-se-859e40d6 | revenue_by_country |  | Amerika: 10.681; Asien: 24.175 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 34,856,000 vs 81,705,000 (57.3% apart) |
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
| volkswagen-ag-be878a5e | total_remuneration | Finance and Operations | 5075339.19 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 5,683,225, more than the stated 5,075,339; XF-02: parts add up to 5,683,225, stated 5,075,339 |
| volkswagen-ag-be878a5e | total_remuneration | Progressive brand group, Chair | 3404523 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,029,494, more than the stated 3,404,523; XF-02: parts add up to 4,029,494, stated 3,404,523 |
| volkswagen-ag-be878a5e | total_remuneration | Integrity and Legal Affairs | 2545518 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,995,518, more than the stated 2,545,518; XF-02: parts add up to 2,995,518, stated 2,545,518 |
| volkswagen-ag-be878a5e | total_remuneration | Human Resources and Trucks bra | 1791959.7 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,033,682, more than the stated 1,791,960; XF-02: parts add up to 2,033,682, stated 1,791,960 |
| volkswagen-ag-be878a5e | total_remuneration | Core brand group, Chair of the | 3401649 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,012,452, more than the stated 3,401,649; XF-02: parts add up to 4,012,452, stated 3,401,649 |
| volkswagen-ag-be878a5e | total_remuneration | Technology, Chair of the Board | 5630301.3 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 6,236,765, more than the stated 5,630,301; XF-02: parts add up to 6,236,765, stated 5,630,301 |
| volkswagen-ag-be878a5e | total_remuneration | IT | 3401076 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 4,026,786, more than the stated 3,401,076; XF-02: parts add up to 4,026,786, stated 3,401,076 |
| volkswagen-ag-be878a5e | total_remuneration | Former Board of Management mem | 1560554.53 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 1,676,039, more than the stated 1,560,555; XF-02: parts add up to 1,676,039, stated 1,560,555 |
| voltatron-ag-57b867a2 | fte |  | 112 | Fail (hard) | CORE-03: quote on page 2, link says page 1 |
| vontobel-holding-ag-1d88ea32 | lti_vested | Executive Committee | 7400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | pension_contribution | Executive Committee | 700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | sti_paid | Executive Committee | 3000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | total_remuneration | Executive Committee | 15000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| voss-veksel-landmandsbank | revenue |  | 197537000 | Fail (hard) | CORE-03: quote not in the source text |
| vp-bank-ag-e661c993 | lti_granted | Group Executive Management | 1284000 | Fail (hard) | CORE-02: 1284 not in the quote |
| vp-bank-ag-e661c993 | lti_granted | Chief Executive Officer (CEO) | 480000 | Fail (hard) | CORE-02: 480 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | benefits |  | D&O-Versicherung, Abfertigung, | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | ebitda |  | 1804000 | Fail (hard) | CORE-02: 1804 not in the quote; CORE-04: no period_end |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | share_price |  | 0.452 | Fail (hard) | CORE-02: 0.452 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | staff_by_segment |  | Investment Properties: 5; Hote | Fail | CORE-04: no period_end; NUM-08: adds up to 82 vs 87 (5.7% apart) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Vorsitzender des Vorstands | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | stellvertretender Vorsitzender | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Dr. Al | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Mag. F | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| wasgau-produktions-handels-8c33a77d | lti_max | Sprecher des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | revenue_by_segment |  | Großhandel: 170897; Einzelhand | Fail (hard) | CORE-03: quote not in the source text |
| wild-bunch-ag-7b9483b1 | revenue_by_segment |  | Internationaler Vertrieb und V | Fail (hard) | CORE-03: quote not in the source text |
| wolford-ag-638e2dc1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | controlling_owner_name |  | FFG Wisdom (Luxembourg) S.à r. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | headcount |  | 712 | Fail (hard) | CORE-02: 712 not in the quote |
| wolford-ag-638e2dc1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | staff_by_country |  | Slovenia: 160; Austria: 209 | Fail | CORE-04: no period_end; NUM-08: adds up to 369 vs 712 (48.2% apart) |
| wuestenrot-wuerttembergische-ag-07b9dfbc | revenue_by_segment |  | Housing: 1104; Life and health | Fail (hard) | CORE-03: quote not in the source text |
| ypsomed-holding-ag-9cb8acfe | benefits |  | Dienstaltersgeschenk | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Chief Executive Officer (CEO) | 130400 | Fail (hard) | CORE-02: 130.4 not in the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Other members of group managem | 479800 | Fail (hard) | CORE-02: 479.8 not in the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Total Executive Management | 610200 | Fail (hard) | CORE-02: 610.2 not in the quote |
| zehnder-group-ag-125a701c | pension_type |  | For members of the Group Execu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zehnder-group-ag-125a701c | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| zublin-immobilien-holding-ag-cf81b4e5 | benefits |  | Sozialversicherungs-Beiträge,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (ab 15. September 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (bis 31. Dezember 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pension_type |  | leistungsorientierter Pensions | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | shares_outstanding |  | 3318027 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| zublin-immobilien-holding-ag-cf81b4e5 | total_remuneration | CEO/CFO (ab 15. September 2024 | 197717 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 223,794, more than the stated 197,717; XF-02: parts add up to 223,794, stated 197,717 |
| zublin-immobilien-holding-ag-cf81b4e5 | total_remuneration | CEO/CFO (bis 31. Dezember 2024 | 246264 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 295,829, more than the stated 246,264; XF-02: parts add up to 295,829, stated 246,264 |
| zug-estates-holding-ag-4947dbda | sti_max | CEO | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| zug-estates-holding-ag-4947dbda | sti_max | Group Management | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| zug-estates-holding-ag-4947dbda | sti_max | Executive Management (total) | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| zuger-kantonalbank-67b7c3b8 | lti_granted | Präsident der Geschäftsleitung | 175000 | Fail (hard) | CORE-02: 175 not in the quote; CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | lti_granted | Geschäftsleitung (total) | 443785 | Fail (hard) | CORE-02: 443.785 not in the quote; CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | pay_currency | Präsident der Geschäftsleitung | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | pay_currency | Geschäftsleitung (total) | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Präsident der Geschäftsleitung | 850000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 938,000, more than the stated 850,000; XF-02: parts add up to 938,000, stated 850,000 |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Geschäftsleitung (total) | 3123000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,415,000, more than the stated 3,123,000; XF-02: parts add up to 3,415,000, stated 3,123,000 |
