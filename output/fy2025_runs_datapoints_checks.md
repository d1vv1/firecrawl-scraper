# Output checks: fy2025_runs_datapoints.csv

567 companies, 25371 filled values checked (2026-11-14, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 23159 (91%) |
| Review | 773 (3%) |
| Fail | 73 (0%) |
| Fail (hard) | 1366 (5%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 2508 | 2497 | 0 | 0 | 11 |
| Listing and market | 2138 | 2085 | 0 | 0 | 53 |
| Sector | 734 | 722 | 0 | 0 | 12 |
| Reporting basis | 1786 | 1778 | 0 | 0 | 8 |
| Financials | 1563 | 1350 | 134 | 1 | 78 |
| Workforce | 610 | 487 | 69 | 3 | 51 |
| Ownership and control | 1668 | 1575 | 0 | 0 | 93 |
| Segment and geography | 673 | 411 | 120 | 39 | 103 |
| Pay policy | 1114 | 1039 | 0 | 0 | 75 |
| Role and disclosure | 3510 | 3335 | 6 | 30 | 139 |
| Pay: fixed | 3322 | 3061 | 64 | 0 | 197 |
| Pay: STI | 2330 | 2083 | 70 | 0 | 177 |
| Pay: LTI | 2021 | 1769 | 53 | 0 | 199 |
| Pay: total | 1370 | 944 | 257 | 0 | 169 |
| Other | 24 | 23 | 0 | 0 | 1 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 25371 | 25354 | 17 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 11696 | 11353 | 343 | 13675 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 18085 | 17243 | 842 | 7286 | source not cached; the run itself did not find the quote |
| CORE-04 | Period end present (dated fields only) |  | 14891 | 14425 | 466 | 10480 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 25371 | 25368 | 3 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 8409 | 8366 | 43 | 16962 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 366 | 366 | 0 | 25005 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 755 | 755 | 0 | 24616 |  |
| COD-06 | Dates are valid | yes | 795 | 774 | 21 | 24576 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 8050 | 8030 | 20 | 17321 | unit 'KCHF' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 7543 | 7543 | 0 | 17828 |  |
| NUM-04 | Magnitude in a plausible range |  | 9216 | 9168 | 48 | 16155 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 878 | 872 | 6 | 24493 | not a whole number |
| NUM-06 | Percentages in range | yes | 1468 | 1467 | 1 | 23903 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 292 | 287 | 5 | 25079 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 668 | 517 | 151 | 24703 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 1088 | 1088 | 0 | 24283 |  |
| NUM-11 | STI paid not above its maximum |  | 453 | 429 | 24 | 24918 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 6817 | 6809 | 8 | 18554 | currency GBPN the role's other amounts EUR |
| NUM-13 | FTE not above headcount |  | 272 | 251 | 21 | 25099 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 116 | 116 | 0 | 25255 |  |
| DER-06 | Derived value shows its formula |  | 964 | 964 | 0 | 24407 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 1184 | 1067 | 117 | 24187 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 1184 | 805 | 379 | 24187 | parts add up to N stated N |

## Fill rate

Company fields: 12794 of 23247 filled (55%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 42 | 567 |
| staff_by_segment | 86 | 567 |
| staff_by_country | 143 | 567 |
| market_cap_band | 200 | 567 |
| controlling_owner_name | 209 | 567 |
| revenue_by_country | 212 | 567 |
| other_names | 214 | 567 |
| share_price | 214 | 567 |
| exchange_segment | 219 | 567 |
| revenue_by_segment | 232 | 567 |
| listing_date | 253 | 567 |
| shareholding_requirement | 259 | 567 |
| fte | 273 | 567 |
| pe_stake_5pct | 280 | 567 |
| largest_holders | 292 | 567 |
| controlling_owner | 292 | 567 |
| ownership_type | 292 | 567 |
| ultimate_parent | 303 | 567 |
| ebitda | 328 | 567 |
| shares_outstanding | 330 | 567 |
| headcount | 337 | 567 |
| revenue | 344 | 567 |
| total_assets | 347 | 567 |
| isin | 348 | 567 |
| accounting_basis | 348 | 567 |
| website | 357 | 567 |
| ticker | 360 | 567 |
| lei | 365 | 567 |
| sector_code | 366 | 567 |
| reporting_currency | 367 | 567 |
| sub_sector | 368 | 567 |
| exchange | 378 | 567 |
| listing_status | 380 | 567 |
| business_id | 381 | 567 |
| legal_name | 383 | 567 |
| country_code | 383 | 567 |
| head_office_city | 383 | 567 |
| benefits | 422 | 567 |
| pension_type | 433 | 567 |
| fiscal_year | 529 | 567 |
| fiscal_year_end | 542 | 567 |

Pay fields, over 1459 executive roles:

| Field | Filled |
|---|---|
| base_salary | 1272 (87%) |
| sti_paid | 1091 (75%) |
| sti_target | 439 (30%) |
| sti_max | 800 (55%) |
| lti_vested | 490 (34%) |
| lti_granted | 598 (41%) |
| lti_target | 356 (24%) |
| lti_max | 577 (40%) |
| benefits_value | 1017 (70%) |
| pension_contribution | 1033 (71%) |
| total_remuneration | 1370 (94%) |

## Failed values (1439)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 2invest-ag-bf4e0781 | benefits |  | Dienstwagen, Telekommunikation | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | sti_paid | Other EC members | 1500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| abb-ltd | sti_target | Other EC members | 1190000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aberdeen-group-plc | lti_vested | Chief Executive Officer | 497000 | Fail (hard) | CORE-02: 497 not in the quote |
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
| adecco-group-ag | revenue_by_country |  | France: 4558; Northern Europe: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 17,911,000,000 vs 23,138,000,000 (22.6% apart) |
| adecco-group-ag | revenue_by_segment |  | Adecco: 17908; Akkodis: 3565;  | Fail | CORE-04: no period_end |
| adecco-group-ag | total_remuneration | CEO | 5400 | Fail (hard) | XF-01: parts add up to 3,413,000, more than the stated 5,400; XF-02: parts add up to 3,413,000, stated 5,400 |
| adecco-group-ag | total_remuneration | Executive Committee | 25800 | Fail (hard) | XF-01: parts add up to 15,454,000, more than the stated 25,800; XF-02: parts add up to 15,454,000, stated 25,800 |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| admiral-group-plc | listing_date |  | 2004-09 | Fail (hard) | CORE-02: not in the quote: 2004; CORE-03: the run did not find the full quote (the note keeps only its start); COD-06: not a year or a date |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| adval-tech-holding-ag | pension_type |  | Vorsorgeeinrichtung der Adval  | Fail (hard) | CORE-03: quote not in the source text |
| aevis-victoria-sa | aggregate_headcount | Other Members of Senior Manage | 3 | Fail (hard) | CORE-03: quote not in the source text |
| agrana-beteiligungs-ag-60d4466c | revenue_by_segment |  | FBS: 1647834; ACS – Stärke: 98 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aiq-limited | fte |  | 7 | Fail (hard) | CORE-03: quote not in the source text |
| aiq-limited | headcount |  | 7 | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | accounting_basis |  | International Financial Report | Fail (hard) | CORE-03: quote not in the source text |
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
| alkemy-capital-investments-plc | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| allgeier-se-9971b49d | pension_type |  | defined benefit and defined co | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: market |
| allreal-holding-ag | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | base_salary | Group Management | 2418000 | Fail (hard) | CORE-02: 2418 not in the quote |
| also-holding-ag | base_salary | Chief Executive Officer (CEO) | 326000 | Fail (hard) | CORE-02: 326 not in the quote |
| also-holding-ag | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | controlling_owner_name |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | fte |  | 5156 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | headcount |  | 5157 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | largest_holders |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| amag-austria-metall-ag-9da856cd | share_price |  | 32 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amag-austria-metall-ag-9da856cd | staff_by_country |  | Austria: 1866; Germany: 249 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | pension_type |  | The Corporation does not opera | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amaroq-ltd | revenue |  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | total_assets |  | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amicorp-fs-uk-plc | fte |  | 172 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amigo-resources-plc | total_assets |  | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | ebitda |  | -2885000 | Fail (hard) | CORE-02: -2.885 not in the quote |
| antofagasta-plc | headcount |  | 8457 | Fail (hard) | CORE-02: 8457 not in the quote |
| antofagasta-plc | listing_date |  | 1888 | Fail (hard) | CORE-02: not in the quote: 1888; COD-06: not a year or a date |
| antofagasta-plc | staff_by_country |  | Chile: 6053; United Kingdom: 5 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,062 vs 8,457 (28.3% apart) |
| aptitude-software-group-plc | revenue_by_country |  | United Kingdom: 10586; Rest of | Fail (hard) | CORE-03: quote not in the source text |
| aptitude-software-group-plc | staff_by_country |  | United Kingdom: 102; Rest of W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 359 vs 317 (13.2% apart) |
| arbonia-ag | base_salary | Other members of Group Managem | 628000 | Fail (hard) | CORE-02: 628 not in the quote |
| arbonia-ag | lti_max | CEO | 75 | Fail (hard) | CORE-02: 75 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_max | Other members of Group Managem | 75 | Fail (hard) | CORE-02: 75 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_target | CEO | 35 | Fail (hard) | CORE-02: 35 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_target | Other members of Group Managem | 35 | Fail (hard) | CORE-02: 35 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | shareholding_requirement |  | Making the Board of Directors  | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | sti_max | CEO | 75 | Fail (hard) | CORE-02: 75 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | sti_max | Other members of Group Managem | 75 | Fail (hard) | CORE-02: 75 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | sti_target | CEO | 35 | Fail (hard) | CORE-02: 35 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | sti_target | Other members of Group Managem | 35 | Fail (hard) | CORE-02: 35 not in the quote; CORE-03: quote not in the source text |
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
| ashmore-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| ashtead-technology-holdings-plc | fte |  | 649 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 649 above headcount 396 |
| asia-strategic-holdings-limited | revenue_by_segment |  | Education: 24970269; Services: | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | benefits |  | flexible benefits allowance of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | listing_date |  | 2022-02 | Fail (hard) | COD-06: not a year or a date |
| asos-plc | lti_granted | CFO (appointed 1 July 2025) | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| asos-plc | pension_type |  | defined contribution, 5% of ba | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| associated-british-foods-plc | largest_holders |  | Wittington Investments Limited | Fail (hard) | NUM-07: holdings add up to 121.6% |
| aston-martin-lagonda-global-holdings-plc | lti_max | CFO | 208.3 | Fail (hard) | CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | lti_target | CEO | 175 | Fail (hard) | CORE-02: 175 not in the quote; CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | lti_target | CFO | 145.8 | Fail (hard) | CORE-02: 145.8 not in the quote; CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | sti_max | CFO | 200 | Fail (hard) | CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | sti_target | CEO | 125 | Fail (hard) | CORE-02: 125 not in the quote; CORE-03: quote not in the source text |
| aston-martin-lagonda-global-holdings-plc | sti_target | CFO | 100 | Fail (hard) | CORE-02: 100 not in the quote; CORE-03: quote not in the source text |
| astrazeneca-plc | revenue_by_country |  | US: 25450; Emerging Markets: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 65,393,000,000 vs 58,739,000,000 (11.3% apart) |
| atalaya-mining-copper-s-a | base_salary | Other key management personnel | 1263000 | Fail (hard) | CORE-02: 1263000 not in the quote |
| atalaya-mining-copper-s-a | benefits_value | Other key management personnel | 30000 | Fail (hard) | CORE-02: 30000 not in the quote |
| atalaya-mining-copper-s-a | listing_date |  | May 2005 | Fail (hard) | COD-06: not a year or a date |
| atalaya-mining-copper-s-a | lti_granted | Other key management personnel | 1830000 | Fail (hard) | CORE-02: 1830000 not in the quote; CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | staff_by_country |  | Spain: 514; Cyprus: 3; United  | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | sti_paid | Other key management personnel | 343000 | Fail (hard) | CORE-02: 343000 not in the quote |
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
| aurskog-sparebank | revenue_by_segment |  | Personmarked: 393456; Bedrifts | Fail (hard) | CORE-03: quote not in the source text |
| aurskog-sparebank | sub_sector |  | Aurskog Sparebank skal være en | Fail (hard) | CORE-03: quote not in the source text |
| austriacard-holdings-ag | benefits_value | Executive Vice President Türki | 13810 | Fail (hard) | CORE-02: 13810 not in the quote |
| austriacard-holdings-ag | staff_by_country |  | Romania: 1346 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,346 vs 2,360 (43.0% apart) |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 292,065, more than the stated 278,255; XF-02: parts add up to 292,065, stated 278,255 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Weste | 1252850 | Fail (hard) | XF-01: parts add up to 1,278,896, more than the stated 1,252,850; XF-02: parts add up to 1,278,896, stated 1,252,850 |
| auto1-group-se-0e2acd91 | revenue_by_country |  | Germany: 1963802; Italy: 11102 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| auto1-group-se-0e2acd91 | revenue_by_segment |  | Merchant: 6413599; Retail: 175 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| auto1-group-se-0e2acd91 | shares_outstanding |  | 220835000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| autoneum-holding-ag | aggregate_headcount | Group Executive Board | 7 | Fail (hard) | CORE-03: quote not in the source text |
| autoneum-holding-ag | base_salary | Group Executive Board | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| autoneum-holding-ag | benefits_value | Group Executive Board | 1014408 | Fail (hard) | CORE-02: 1014408 not in the quote |
| autotrader-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| aviva-plc | headcount |  | 36160 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aviva-plc | role_disclosure | Executive Directors | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | lti_granted | Other members of the Global Ex | 5772800 | Fail (hard) | CORE-03: quote not in the source text |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: quote on page 207, link says page 206 |
| avon-technologies-plc | fte |  | 911 | Fail (hard) | CORE-03: quote not in the source text |
| avon-technologies-plc | total_assets |  | 314800000 | Fail (hard) | CORE-03: quote not in the source text |
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | shareholding_requirement |  | CEO is allocated 375 shares an | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bajaj-mobility-ag-8e6bef55 | ebitda |  | 874000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bakkafrost | ebitda |  | 1672664000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| balfour-beatty-plc | pension_contribution | Group Chief Executive (until 8 | 43183 | Fail (hard) | CORE-03: quote not in the source text |
| balfour-beatty-plc | revenue_by_country |  | United Kingdom: 4778; United S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | revenue_by_segment |  | Construction Services: 8711; S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| baltic-classifieds-group-plc | lti_max | CEO | 500 | Fail (hard) | COD-01: unit '' is not a target form |
| baltic-classifieds-group-plc | lti_max | CFO | 500 | Fail (hard) | COD-01: unit '' is not a target form |
| baltic-classifieds-group-plc | lti_max | COO | 500 | Fail (hard) | COD-01: unit '' is not a target form |
| banque-cantonale-du-jura-sa | base_salary | Membre de Direction | 910240 | Fail (hard) | CORE-02: 910240 not in the quote |
| banque-cantonale-du-jura-sa | pension_contribution | Membre de Direction | 323953 | Fail (hard) | CORE-02: 323953 not in the quote |
| banque-cantonale-du-jura-sa | sti_paid | Membre de Direction | 367500 | Fail (hard) | CORE-02: 367500 not in the quote |
| barclays-plc | total_remuneration | Group Chief Executive | 15045000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 4,588,000, stated 15,045,000 |
| barclays-plc | total_remuneration | Group Finance Director | 8970000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,770,000, stated 8,970,000 |
| barr-a-g-plc | pension_type |  | defined contribution, 8% of sa | Fail (hard) | CORE-03: quote not in the source text |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | base_salary | CEO (until 31.7.2025) | 650000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | headcount |  | 1054 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Executive | 605000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must hold a mi | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | staff_by_country |  | Canton of Basel-Landschaft: 92 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | sti_paid | CEO (until 31.7.2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | sti_paid | Other members of the Executive | 605000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Executive | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other management committee mem | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other management committee mem | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other management committee mem | 475160 | Fail (hard) | CORE-02: 475160 not in the quote |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other management committee mem | 815877 | Fail (hard) | CORE-02: 815877 not in the quote |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other management committee mem | 4028977 | Fail (hard) | CORE-02: 4028977 not in the quote |
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
| baywa-ag-na-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ebitda |  | -162500000 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | largest_holders |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| belimo-holding-ag | base_salary | Other members, Executive Commi | 2108000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_country |  | EMEA: 240.3; Americas: 341.3;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| belimo-holding-ag | revenue_by_segment |  | Damper Actuators: 253.8; Contr | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| belimo-holding-ag | sti_paid | Other members, Executive Commi | 2449000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | total_remuneration | CEO | 1749000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,539,000, stated 1,749,000 |
| belimo-holding-ag | total_remuneration | Other members, Executive Commi | 5573000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 5,108,000, stated 5,573,000 |
| bellevue-group-ag | headcount |  | 72.8 | Fail (hard) | NUM-05: not a whole number |
| bellevue-group-ag | revenue_by_country |  | Switzerland: 47705; United Kin | Fail (hard) | CORE-03: quote not in the source text |
| bellevue-group-ag | total_assets |  | 155563000 | Fail (hard) | CORE-02: 155563 not in the quote; CORE-04: no period_end |
| berentzen-gruppe-ag-957f8708 | benefits |  | Dienstwagen, einschließlich Pr | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| berner-kantonalbank-ag | aggregate_headcount | Other members of group managem | 5.6 | Fail (hard) | NUM-05: not a whole number |
| berner-kantonalbank-ag | benefits |  | Spesenpauschale (Präsidentin d | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | benefits_value | CEO | 30000 | Fail (hard) | CORE-02: 30 not in the quote |
| berner-kantonalbank-ag | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| berner-kantonalbank-ag | pension_type |  | defined contribution | Fail (hard) | CORE-03: quote not in the source text |
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
| besqab-pref-b | controlling_owner_name |  | Family Nordström | Fail (hard) | CORE-02: not in the quote: family |
| big-yellow-group-plc | fte |  | 453 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| big-yellow-group-plc | listing_date |  | May 2000 | Fail (hard) | COD-06: not a year or a date |
| big-yellow-group-plc | share_price |  | 967.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bilfinger-se-o-n | total_remuneration | member of the Executive Board, | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| biofrontera-ag-na-o-n | lti_target | CFO | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | role_disclosure | CFO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | shareholding_requirement |  | Vorstandsmitglieder sind zu ei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bioversys-ag | base_salary | CEO | 1224000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | lti_granted | CEO | 960000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | pension_contribution | CEO | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | sti_paid | CEO | 232000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | total_remuneration | CEO | 2676000 | Fail (hard) | CORE-03: quote not in the source text |
| bks-bank-ag-5e8b8669 | revenue_by_segment |  | Privatkunden: 111406; Firmenku | Fail | CORE-04: no period_end; NUM-08: adds up to 388,487,000 vs 303,636,676 (27.9% apart) |
| blencowe-resources-plc | ebitda |  | -1536243 | Fail (hard) | CORE-02: -1536243 not in the quote |
| bodycote-plc | benefits_value | CEO | 19000000 | Fail (hard) | CORE-02: 19000 not in the quote |
| bodycote-plc | benefits_value | CFO | 16000000 | Fail (hard) | CORE-02: 16000 not in the quote |
| bodycote-plc | total_remuneration | CEO | 1122000 | Fail (hard) | XF-01: parts add up to 20,103,000, more than the stated 1,122,000; XF-02: parts add up to 20,103,000, stated 1,122,000 |
| bodycote-plc | total_remuneration | CFO | 900000000 | Fail (hard) | CORE-02: 900000 not in the quote; XF-02: parts add up to 309,736,195, stated 900,000,000 |
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
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-03: quote on page 14, link says page 13 |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: quote not in the source text |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| british-american-tobacco-plc | other_names |  | British American Tobacco Compa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| british-american-tobacco-plc | revenue_by_segment |  | NGP: 397; Strategic Portfolio: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 17,108,000,000 vs 25,610,000,000 (33.2% apart) |
| bsf-enterprise-plc | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | largest_holders |  | GBF Nominees Limited 19.48%; B | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| bsf-enterprise-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| bt-group-plc | fte |  | 81600 | Fail (hard) | CORE-02: 81.6 not in the quote |
| bt-group-plc | headcount |  | 77200 | Fail (hard) | CORE-02: 77.2 not in the quote |
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
| burckhardt-compression-holding-ag | listing_date |  | 2006-06 | Fail (hard) | COD-06: not a year or a date |
| burckhardt-compression-holding-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| burckhardt-compression-holding-ag | pay_currency | Other members of the Executive | CHF | Fail | CORE-04: no period_end |
| burckhardt-compression-holding-ag | revenue_by_country |  | Europe: 194414; Africa: 10564; | Fail (hard) | CORE-03: quote not in the source text |
| burckhardt-compression-holding-ag | sti_target | CEO | 0.28 | Fail (hard) | CORE-04: no period_end; COD-01: unit '' is not a target form |
| burgenland-holding-ag-a95d1abc | largest_holders |  | VERBUND AG 10%; WIEN ENERGIE G | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burgenland-holding-ag-a95d1abc | share_price |  | 71.5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | total_remuneration | Mitglied des Vorstands (Dr. Kl | 5500 | Fail (hard) | XF-01: parts add up to 5,650, more than the stated 5,500; XF-02: parts add up to 5,650, stated 5,500 |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| burkhalter-holding-ag | sti_max | CEO | 60 | Fail (hard) | COD-01: unit '' is not a target form |
| burkhalter-holding-ag | sti_max | CFO | 60 | Fail (hard) | COD-01: unit '' is not a target form |
| bvz-holding-ag | revenue_by_segment |  | Gornergrat: 47.1; Immobilien:  | Fail (hard) | CORE-03: quote on page 5, link says page 4; NUM-08: adds up to 181,900,000 vs 216,170,312 (15.9% apart) |
| bystronic-ag | lti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| bytes-technology-group-plc | ebitda |  | 62732000 | Fail (hard) | CORE-02: 62732 not in the quote |
| c-c-group-plc | lti_granted | Chief Financial and Transforma | 404411 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| c-c-group-plc | revenue_by_segment |  | Branded: 453.6; Distribution:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 1,861,600,000 vs 1,569,800,000 (18.6% apart) |
| ca-immobilien-anlagen-ag-a9ff4a4a | staff_by_segment |  | Austria: 80; Germany/Switzerla | Fail | CORE-04: no period_end; NUM-08: adds up to 348 vs 254 (37.0% apart) |
| cab-payments-holdings-plc | revenue |  | 109400000 | Fail (hard) | CORE-03: quote not in the source text |
| cab-payments-holdings-plc | total_assets |  | 188000000 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | lti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | pension_type |  | defined contribution, not exce | Fail (hard) | CORE-03: quote not in the source text |
| caffyns-plc | headcount |  | 485 | Fail (hard) | CORE-02: 485 not in the quote |
| caledonia-investments-plc | benefits_value | Executive Director (J M B Cayz | 31000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | headcount |  | 82 | Fail (hard) | CORE-02: 82 not in the quote |
| caledonia-investments-plc | lti_vested | Executive Director (J M B Cayz | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | lti_vested | Former Executive Director (unt | 168000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | revenue_by_segment |  | Public Companies: 21.8; Privat | Fail | CORE-04: no period_end; NUM-08: adds up to 43,700,000 vs 166,000,000 (73.7% apart) |
| calida-holding-ag-1793bfba | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: quote on page 100, link says page 99 |
| canal-s-a | controlling_owner_name |  | Bolloré SE | Fail (hard) | CORE-02: not in the quote: se |
| cancom-se-o-n | lti_granted | Vorstand | 355640 | Fail (hard) | CORE-02: 355.64 not in the quote; CORE-03: quote not in the source text |
| capita-plc | share_price |  | 4.055 | Fail (hard) | CORE-02: 4.055 not in the quote |
| capita-plc | shares_outstanding |  | 120030667 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| carclo-plc | benefits_value | Chief Executive Officer | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | benefits_value | Chief Financial Officer | 12000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Executive Officer | 149000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | lti_vested | Chief Financial Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | pension_contribution | Chief Financial Officer | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | staff_by_country |  | United Kingdom: 318; North Ame | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | sti_paid | Chief Financial Officer | 101000 | Fail (hard) | CORE-03: quote not in the source text |
| carclo-plc | total_remuneration | Chief Financial Officer | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| cardiff-property-plc | total_remuneration | Chief Executive Officer | 182000 | Fail (hard) | XF-01: parts add up to 206,000, more than the stated 182,000; XF-02: parts add up to 206,000, stated 182,000 |
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| centrica-plc | listing_date |  | 1997-02-17 | Fail (hard) | CORE-02: not in the quote: 1997 |
| centrica-plc | share_price |  | 1.4065 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| centrica-plc | total_remuneration | Group Chief Executive | 4731000 | Fail (hard) | XF-01: parts add up to 5,213,750, more than the stated 4,731,000; XF-02: parts add up to 5,213,750, stated 4,731,000 |
| ceres-power-holdings-plc | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ceres-power-holdings-plc | total_assets |  | 145796000 | Fail (hard) | CORE-02: 145796 not in the quote; CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | base_salary | Former members of the Manageme | 747000 | Fail (hard) | CORE-02: 747 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | lti_granted | CEO | 354000 | Fail (hard) | CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | lti_granted | Other members of the Managemen | 720000 | Fail (hard) | CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | shareholding_requirement |  | Die Vergütung des Verwaltungsr | Fail (hard) | CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Other members of the Managemen | 239000 | Fail (hard) | CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Former members of the Manageme | 89000 | Fail (hard) | CORE-02: 89 not in the quote |
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
| chesnara-plc | pension_type |  | defined contribution pension s | Fail (hard) | CORE-03: quote not in the source text |
| chesnara-plc | role_disclosure | Key management personnel | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| chesnara-plc | shareholding_requirement |  | executive directors to build u | Fail (hard) | CORE-03: quote not in the source text |
| chesnara-plc | sti_paid | Key management personnel | 700000 | Fail (hard) | CORE-02: 700000 not in the quote |
| chesnara-plc | total_remuneration | Key management personnel | 4100000 | Fail (hard) | CORE-02: 4100000 not in the quote; XF-02: parts add up to 2,000,000, stated 4,100,000 |
| chill-brands-group-plc | share_price |  | 1.575 | Fail (hard) | CORE-02: 1.575 not in the quote |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | shares_outstanding |  | 1095704 | Fail (hard) | CORE-02: 1095704 not in the quote |
| cicor-technologies-ltd-39bd9715 | base_salary | Group Management | 1204000 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | benefits |  | contributions to professional  | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | benefits_value | Group Management | 420000 | Fail (hard) | CORE-02: 420 not in the quote; CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | lti_granted | Group Management | 2272000 | Fail (hard) | CORE-02: 2272 not in the quote; CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | lti_granted | CEO | 980000 | Fail (hard) | CORE-02: 980 not in the quote |
| cicor-technologies-ltd-39bd9715 | pension_type |  | collective pension scheme, con | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | sti_paid | Group Management | 669000 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | total_remuneration | Group Management | 4564000 | Fail (hard) | CORE-03: quote not in the source text |
| cindrigo-holdings-limited | benefits_value | Executive Director (resigned 1 | 69444 | Fail (hard) | CORE-02: 69444 not in the quote |
| cizzle-biotechnology-holdings-plc | fte |  | 0 | Fail | CORE-04: no period_end; NUM-04: 0 outside 0.5..5e+06 |
| clarkson-plc | fte |  | 2103 | Fail (hard) | CORE-03: quote not in the source text |
| clarkson-plc | staff_by_segment |  | Broking: 1504; Financial: 127; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 2,103 vs 2,250 (6.5% apart) |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| cloudbreak-discovery-plc | sti_paid | Managing Director (appointed J | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| cloudbreak-discovery-plc | sti_paid | Executive Chairman (appointed  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 0.4425 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| cmb-tech-nv | headcount |  | 2826 | Fail (hard) | CORE-02: 2826 not in the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: quote not in the source text |
| coats-group-plc | share_price |  | 84.55 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| coca-cola-europacific-partners-plc | revenue_by_country |  | Great Britain: 3470; Iberia: 3 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-europacific-partners-plc | revenue_by_segment |  | Europe: 15404; APS: 5497 | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | lti_granted | Vorsitzende (seit 1. Oktober 2 | 777000 | Fail (hard) | CORE-02: 777 not in the quote |
| commerzbank-ag | lti_granted | stellvertretender Vorsitzender | 634200 | Fail (hard) | CORE-02: 634.2 not in the quote |
| commerzbank-ag | lti_granted | Group Human Resources & Group  | 439800 | Fail (hard) | CORE-02: 439.8 not in the quote |
| commerzbank-ag | lti_granted | Segment Privat- und Unternehme | 423600 | Fail (hard) | CORE-02: 423.6 not in the quote |
| commerzbank-ag | lti_granted | Chief Financial Officer (seit  | 369000 | Fail (hard) | CORE-02: 369 not in the quote |
| commerzbank-ag | lti_granted | Chief Risk Officer (seit 1. Ja | 439800 | Fail (hard) | CORE-02: 439.8 not in the quote |
| commerzbank-ag | lti_granted | Chief Operating Officer (seit  | 439800 | Fail (hard) | CORE-02: 439.8 not in the quote |
| commerzbank-ag | lti_max | stellvertretender Vorsitzender | 799200 | Fail (hard) | CORE-02: 799200 not in the quote |
| commerzbank-ag | lti_max | Group Human Resources & Group  | 594000 | Fail (hard) | CORE-02: 594000 not in the quote |
| commerzbank-ag | lti_max | Segment Privat- und Unternehme | 594000 | Fail (hard) | CORE-02: 594000 not in the quote |
| commerzbank-ag | lti_max | Chief Financial Officer (seit  | 512400 | Fail (hard) | CORE-02: 512400 not in the quote |
| commerzbank-ag | lti_max | Chief Risk Officer (seit 1. Ja | 594000 | Fail (hard) | CORE-02: 594000 not in the quote |
| commerzbank-ag | lti_max | Chief Operating Officer (seit  | 594000 | Fail (hard) | CORE-02: 594000 not in the quote |
| commerzbank-ag | lti_target | Vorsitzende (seit 1. Oktober 2 | 669600 | Fail (hard) | CORE-02: 669600 not in the quote |
| commerzbank-ag | lti_target | stellvertretender Vorsitzender | 532800 | Fail (hard) | CORE-02: 532800 not in the quote |
| commerzbank-ag | lti_target | Group Human Resources & Group  | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | lti_target | Segment Privat- und Unternehme | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | lti_target | Chief Financial Officer (seit  | 342000 | Fail (hard) | CORE-02: 342000 not in the quote |
| commerzbank-ag | lti_target | Chief Risk Officer (seit 1. Ja | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | lti_target | Chief Operating Officer (seit  | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | other_names |  | Commerz- und Disconto-Bank; Co | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | revenue_by_country |  | Deutschland: 8043; China einsc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | staff_by_country |  | Deutschland: 23991; China eins | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | sti_max | Vorsitzende (seit 1. Oktober 2 | 669600 | Fail (hard) | CORE-02: 669600 not in the quote |
| commerzbank-ag | sti_max | stellvertretender Vorsitzender | 532800 | Fail (hard) | CORE-02: 532800 not in the quote |
| commerzbank-ag | sti_max | Group Human Resources & Group  | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | sti_max | Segment Privat- und Unternehme | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | sti_max | Chief Financial Officer (seit  | 341600 | Fail (hard) | CORE-02: 341600 not in the quote |
| commerzbank-ag | sti_max | Chief Risk Officer (seit 1. Ja | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | sti_max | Chief Operating Officer (seit  | 396000 | Fail (hard) | CORE-02: 396000 not in the quote |
| commerzbank-ag | sti_target | Vorsitzende (seit 1. Oktober 2 | 446400 | Fail (hard) | CORE-02: 446400 not in the quote |
| commerzbank-ag | sti_target | stellvertretender Vorsitzender | 355200 | Fail (hard) | CORE-02: 355200 not in the quote |
| commerzbank-ag | sti_target | Group Human Resources & Group  | 264000 | Fail (hard) | CORE-02: 264000 not in the quote |
| commerzbank-ag | sti_target | Segment Privat- und Unternehme | 264000 | Fail (hard) | CORE-02: 264000 not in the quote |
| commerzbank-ag | sti_target | Chief Financial Officer (seit  | 228000 | Fail (hard) | CORE-02: 228000 not in the quote |
| commerzbank-ag | sti_target | Chief Risk Officer (seit 1. Ja | 264000 | Fail (hard) | CORE-02: 264000 not in the quote |
| commerzbank-ag | sti_target | Chief Operating Officer (seit  | 264000 | Fail (hard) | CORE-02: 264000 not in the quote |
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | XF-01: parts add up to 3,923,000, more than the stated 3,744,000; XF-02: parts add up to 3,923,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | stellvertretender Vorsitzender | 2917000 | Fail (hard) | XF-01: parts add up to 3,047,200, more than the stated 2,917,000; XF-02: parts add up to 3,047,200, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Group Human Resources & Group  | 2116000 | Fail (hard) | XF-01: parts add up to 2,295,800, more than the stated 2,116,000; XF-02: parts add up to 2,295,800, stated 2,116,000 |
| computacenter-plc | base_salary | CFO (from 1 September 2025) | 130000 | Fail (hard) | CORE-02: 130 not in the quote |
| computacenter-plc | benefits_value | CEO | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | benefits_value | CFO (from 1 September 2025) | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | pension_contribution | CEO | 31600 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | pension_contribution | CFO (from 1 September 2025) | 5800 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | revenue_by_segment |  | UK: 1419.2; Germany: 2109.3; W | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | sti_paid | CEO | 972800 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | sti_paid | CFO (from 1 September 2025) | 126700 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | total_remuneration | CEO | 1745400 | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | total_remuneration | CFO (from 1 September 2025) | 266500 | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | exchange |  | London Stock Exchange | Fail (hard) | CORE-02: not in the quote: london stock exchange |
| conduit-holdings-limited | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | staff_by_country |  | Bermuda: 64 | Fail | CORE-04: no period_end; NUM-08: adds up to 64 vs 68 (5.9% apart) |
| conduit-holdings-limited | sub_sector |  | Conduit Re is a Bermuda-based, | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | total_remuneration | CEO (from 31 March 2025) | 1004000 | Fail (hard) | XF-01: parts add up to 2,334,473, more than the stated 1,004,000; XF-02: parts add up to 2,334,473, stated 1,004,000 |
| contango-holdings-plc | fte |  | 10 | Fail (hard) | CORE-03: quote not in the source text |
| contango-holdings-plc | headcount |  | 10 | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | base_salary | Vorstandsvorsitzender (01.12.2 | 1550000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | benefits |  | company car (personal use), re | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| convatec-group-plc | listing_date |  | 2016-10 | Fail (hard) | COD-06: not a year or a date |
| convatec-group-plc | staff_by_country |  | Europe: 5276; North America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | staff_by_segment |  | Operations: 3467; Sales and ma | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-d | base_salary | Other senior executives | 8317000 | Fail (hard) | CORE-02: 8317 not in the quote |
| corem-property-d | shareholding_requirement |  | There are no agreements regard | Fail (hard) | CORE-03: quote not in the source text |
| corpus-resources-plc | shares_outstanding |  | 3309339766 | Fail (hard) | CORE-02: 3309339766 not in the quote |
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
| cranswick-plc | lti_max | CEO | 300 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | lti_max | Executive Director (Chris Alde | 250 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | lti_max | Executive Director (Mark Botto | 250 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | lti_max | Executive Director (Jim Brisby | 250 | Fail (hard) | CORE-03: quote not in the source text |
| crest-nicholson-holdings-plc | revenue_by_segment |  | UK housebuilding: 610.8 | Fail (hard) | CORE-03: quote not in the source text |
| crest-nicholson-holdings-plc | sti_target | Chief Executive Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| crest-nicholson-holdings-plc | sti_target | Executive Director | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| critical-metals-plc | listing_date |  | 2017 | Fail (hard) | CORE-02: not in the quote: 2017 |
| critical-metals-plc | share_price |  | 14.25 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | staff_by_country |  | DRC: 49 | Fail | CORE-04: no period_end |
| critical-mineral-resources-plc | fte |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | headcount |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | staff_by_country |  | Morocco: 1; UK: 4 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | base_salary | Group Chief Executive (CEO) | 786656 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | base_salary | Chief Financial Officer (CFO)  | 435000 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | benefits_value | Chief Financial Officer (CFO)  | 37453 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | lti_vested | Group Chief Executive (CEO) | 45934 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | pension_contribution | Chief Financial Officer (CFO)  | 87000 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | sti_paid | Chief Financial Officer (CFO)  | 359203 | Fail (hard) | CORE-03: quote not in the source text |
| cts-eventim-kgaa-1664614e | controlling_owner_name |  | KPS Stiftung | Fail (hard) | CORE-02: not in the quote: stiftung |
| cts-eventim-kgaa-1664614e | lti_granted | CEO | 800000 | Fail (hard) | CORE-02: 800000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | COO | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | lti_granted | CTO (seit 1. Januar 2025) | 300000 | Fail (hard) | CORE-02: 300000 not in the quote |
| cts-eventim-kgaa-1664614e | revenue_by_country |  | Germany: 1347630; Italy: 60590 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cts-eventim-kgaa-1664614e | revenue_by_segment |  | Ticketing: 947220; Live Entert | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| curatis-holding-ag-adc33085 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| currys-plc | fte |  | 25076 | Fail (hard) | CORE-02: 25076 not in the quote |
| cykel-ai-plc | headcount |  | 9 | Fail (hard) | CORE-02: 9 not in the quote |
| cykel-ai-plc | total_assets |  | 1537768 | Fail (hard) | CORE-03: quote not in the source text |
| dar-global-plc | headcount |  | 434 | Fail (hard) | CORE-02: 434 not in the quote; CORE-03: quote not in the source text |
| data-modul-ag-9cac6e64 | ebitda |  | 2490000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| data-modul-ag-9cac6e64 | revenue_by_segment |  | Displays: 126601; Systems: 862 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| datwyler-holding-ag-eca04fdb | largest_holders |  | Paul Hälg, Hanspeter Fässler,  | Fail (hard) | CORE-03: quote not in the source text |
| datwyler-holding-ag-eca04fdb | lti_target | CEO | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| datwyler-holding-ag-eca04fdb | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| datwyler-holding-ag-eca04fdb | revenue_by_segment |  | Healthcare: 462.7; Industrial: | Fail (hard) | CORE-03: quote not in the source text |
| datwyler-holding-ag-eca04fdb | shares_outstanding |  | 34600000 | Fail (hard) | CORE-02: 34600000 not in the quote |
| dcc-energy-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| dcc-energy-plc | sti_paid | Chief Executive | 1928000 | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | total_remuneration | Chief Executive | 4349000 | Fail (hard) | CORE-03: quote not in the source text |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | COD-06: not a year or a date |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Philip von  | 63000 | Fail (hard) | CORE-02: 63000 not in the quote |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Andreas Prü | 243750 | Fail (hard) | CORE-02: 243750 not in the quote |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Nathalie Kr | 105000 | Fail (hard) | CORE-02: 105000 not in the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_max | Chief Financial Officer (since | 264000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_target | Chief Financial Officer (since | 132000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| derwent-london-plc | sti_paid | CEO | 549000 | Fail (hard) | CORE-02: 549000 not in the quote |
| derwent-london-plc | sti_paid | Executive Director (Damian Wis | 423000 | Fail (hard) | CORE-02: 423000 not in the quote |
| derwent-london-plc | sti_paid | Executive Director (Nigel Geor | 423000 | Fail (hard) | CORE-02: 423000 not in the quote |
| derwent-london-plc | sti_paid | Executive Director (Emily Prid | 423000 | Fail (hard) | CORE-02: 423000 not in the quote |
| derwent-london-plc | total_remuneration | CEO | 1000000 | Fail (hard) | CORE-02: 1000000 not in the quote; CORE-03: quote not in the source text; XF-01: parts add up to 1,410,319, more than the stated 1,000,000; XF-02: parts add up to 1,410,319, stated 1,000,000 |
| derwent-london-plc | total_remuneration | Executive Director (Damian Wis | 778000 | Fail (hard) | CORE-02: 778000 not in the quote; CORE-03: quote not in the source text; XF-01: parts add up to 1,093,006, more than the stated 778,000; XF-02: parts add up to 1,093,006, stated 778,000 |
| derwent-london-plc | total_remuneration | Executive Director (Nigel Geor | 778000 | Fail (hard) | CORE-02: 778000 not in the quote; CORE-03: quote not in the source text; XF-01: parts add up to 1,091,683, more than the stated 778,000; XF-02: parts add up to 1,091,683, stated 778,000 |
| derwent-london-plc | total_remuneration | Executive Director (Emily Prid | 778000 | Fail (hard) | CORE-02: 778000 not in the quote; CORE-03: quote not in the source text; XF-01: parts add up to 1,093,006, more than the stated 778,000; XF-02: parts add up to 1,093,006, stated 778,000 |
| deutsche-post-ag-b89554ef | pension_contribution | Supply Chain (since August 16, | 100333 | Fail (hard) | CORE-02: 100333 not in the quote |
| deutsche-real-estate-ag-8625fa60 | benefits |  | Beiträge und/oder Zuschüsse zu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| deutsche-real-estate-ag-8625fa60 | largest_holders |  | Summit Real Estate Holdings Lt | Fail (hard) | NUM-07: holdings add up to 165.96% |
| deutsche-real-estate-ag-8625fa60 | other_names |  | Geestemünder Bank AG; Geestemü | Fail (hard) | CORE-03: quote not in the source text |
| deutsche-real-estate-ag-8625fa60 | sti_max | Vorstandsmitglied | 128000 | Fail (hard) | CORE-02: 128000 not in the quote |
| deutsche-real-estate-ag-8625fa60 | sti_paid | Vorstandsmitglied | 60000 | Fail (hard) | CORE-02: 60 not in the quote |
| deutz-ag-8a315ac8 | lti_target | Vorstandsvorsitzender | 622000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 37000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | lti_target | ordentliches Vorstandsmitglied | 370000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | role_disclosure | ordentliches Vorstandsmitglied | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| deutz-ag-8a315ac8 | total_remuneration | ordentliches Vorstandsmitglied | 955000 | Fail (hard) | XF-01: parts add up to 1,005,000, more than the stated 955,000; XF-02: parts add up to 1,005,000, stated 955,000 |
| dfs-furniture-plc | total_remuneration | CEO | 1152000 | Fail (hard) | XF-01: parts add up to 1,202,000, more than the stated 1,152,000; XF-02: parts add up to 1,202,000, stated 1,152,000 |
| dfs-furniture-plc | total_remuneration | Former interim CFO (until 2 Ap | 716000 | Fail (hard) | XF-01: parts add up to 1,181,000, more than the stated 716,000; XF-02: parts add up to 1,181,000, stated 716,000 |
| diageo-plc | revenue_by_country |  | United States: 7408; India: 32 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| diageo-plc | revenue_by_segment |  | North America: 7249; Europe: 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 19,643,000,000 vs 27,762,000,000 (29.2% apart) |
| diageo-plc | staff_by_segment |  | SC&P: 6963; Corporate and othe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 12,605 vs 27,972 (54.9% apart) |
| dialight-plc | lti_max | Group Chair | 35 | Fail (hard) | COD-01: unit '' is not a target form |
| dialight-plc | lti_max | Group CEO | 35 | Fail (hard) | COD-01: unit '' is not a target form |
| dialight-plc | lti_max | Group CFO | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| dialight-plc | pension_contribution | Group CEO | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| dialight-plc | pension_contribution | Group CFO | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| digia-oyj | aggregate_headcount | Key Management | 15 | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | revenue_by_segment |  | Controls: 836.4; Seals: 456; L | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | total_remuneration | Group Chief Executive | 7150000 | Fail (hard) | XF-01: parts add up to 2,755,069,000, more than the stated 7,150,000; XF-02: parts add up to 2,755,069,000, stated 7,150,000 |
| diploma-plc | total_remuneration | Acting Chief Financial Officer | 657000 | Fail (hard) | XF-01: parts add up to 140,003,000, more than the stated 657,000; XF-02: parts add up to 140,003,000, stated 657,000 |
| dksh-holding-ag-6576340c | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| do-co-aktiengesellschaft-1ce4abbb | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| do-co-aktiengesellschaft-1ce4abbb | revenue_by_country |  | Türkiye: 648.16; Great Britain | Fail | CORE-04: no period_end; NUM-08: adds up to 2,298,120,000 vs 2,461,590,000 (6.6% apart) |
| do-co-aktiengesellschaft-1ce4abbb | staff_by_country |  | Austria: 1641; Germany: 2493;  | Fail | CORE-04: no period_end; NUM-08: adds up to 19,330 vs 14,762 (30.9% apart) |
| docmorris-ag-be190279 | lti_granted | CEO | 470000 | Fail (hard) | CORE-02: 470 not in the quote |
| docmorris-ag-be190279 | lti_granted | Other members of the Executive | 714000 | Fail (hard) | CORE-02: 714 not in the quote |
| domino-s-pizza-group-plc | benefits_value | Interim CEO | 1000 | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | benefits_value | Former CEO (until 24 November  | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | benefits_value | Former Executive Director (unt | 9000 | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | fte |  | 2402 | Fail (hard) | CORE-02: 2402 not in the quote |
| domino-s-pizza-group-plc | total_remuneration | Interim CEO | 56000 | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | total_remuneration | Former CEO (until 24 November  | 745000 | Fail (hard) | CORE-03: quote not in the source text |
| domino-s-pizza-group-plc | total_remuneration | Former Executive Director (unt | 302000 | Fail (hard) | CORE-03: quote not in the source text |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | CEO | 388000 | Fail (hard) | CORE-02: 388 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | Other EC | 1365000 | Fail (hard) | CORE-02: 1365 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | Former EC | 452000 | Fail (hard) | CORE-02: 452 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: PDF link without #page= |
| dormakaba-holding-ag-9c17f7d1 | shareholding_requirement |  | CEO: 300% of annual base salar | Fail (hard) | CORE-03: quote not in the source text |
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
| dsm-firmenich-ag-62366aa6 | revenue_by_country |  | Switzerland: 214; Netherlands: | Fail | CORE-04: no period_end; NUM-08: adds up to 9,034,000,000 vs 12,521,000,000 (27.8% apart) |
| dsm-firmenich-ag-62366aa6 | revenue_by_segment |  | P&B: 3760; TTH: 3146; HNC: 210 | Fail | CORE-04: no period_end; NUM-08: adds up to 9,034,000,000 vs 12,521,000,000 (27.8% apart) |
| dt-konsum-real-estae-ag-4e32eb34 | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-konsum-real-estae-ag-4e32eb34 | lti_granted | Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-konsum-real-estae-ag-4e32eb34 | lti_vested | Management Board | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-pfandbriefbk-ag-71e35702 | revenue_by_country |  | Germany: 421; Rest of Europe:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dt-telekom-ag-9dfbbd0c | revenue_by_segment |  | Germany: 25610; United States: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dt-telekom-ag-9dfbbd0c | staff_by_country |  | Germany: 70751; other EU membe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| dunelm-group-plc | controlling_owner_name |  | Adderley family (Concert Party | Fail (hard) | CORE-02: not in the quote: family |
| dunelm-group-plc | listing_date |  | 2006-10 | Fail (hard) | COD-06: not a year or a date |
| east-star-resources-plc | base_salary | CEO | 125000000 | Fail (hard) | CORE-02: 125000 not in the quote |
| east-star-resources-plc | base_salary | CTO | 68000000 | Fail (hard) | CORE-02: 68000 not in the quote |
| east-star-resources-plc | fte |  | 13 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 13 above headcount 9 |
| east-star-resources-plc | total_remuneration | CEO | 196000000 | Fail (hard) | CORE-02: 196000 not in the quote; XF-02: parts add up to 125,071,000, stated 196,000,000 |
| east-star-resources-plc | total_remuneration | CTO | 88000 | Fail (hard) | XF-01: parts add up to 68,020,000, more than the stated 88,000; XF-02: parts add up to 68,020,000, stated 88,000 |
| easyjet-plc | revenue_by_segment |  | Airline: 8666; Holidays: 1917 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| ecora-royalties-plc | base_salary | Chief Executive Officer | 485000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | base_salary | Chief Financial Officer | 345000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | lti_vested | Chief Financial Officer | 52000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_country |  | Australia: 19664; Americas: 31 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_segment |  | Cobalt: 18871; Copper: 14180;  | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | sti_paid | Chief Financial Officer | 220000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | total_remuneration | Chief Financial Officer | 654000 | Fail (hard) | CORE-03: quote not in the source text |
| elixirr-international-plc | listing_date |  | 2025-07 | Fail (hard) | COD-06: not a year or a date |
| emerald-horizon-ag-a6420623 | revenue |  | 224983 | Fail (hard) | CORE-02: 224983 not in the quote; CORE-04: no period_end |
| emmi-ag-ad10f47a | base_salary | CEO | 767000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | base_salary | Other members of Group Executi | 2973000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | benefits_value | CEO | 4000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | benefits_value | Other members of Group Executi | 29000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | pay_currency | CEO | KCHF | Fail (hard) | COD-01: KCHF is not ISO 4217 |
| emmi-ag-ad10f47a | pay_currency | Other members of Group Executi | KCHF | Fail (hard) | COD-01: KCHF is not ISO 4217 |
| emmi-ag-ad10f47a | pension_contribution | CEO | 204000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | pension_contribution | Other members of Group Executi | 838000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | sti_paid | CEO | 382000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | sti_paid | Other members of Group Executi | 893000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | total_remuneration | CEO | 1357000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| emmi-ag-ad10f47a | total_remuneration | Other members of Group Executi | 4733000 | Fail (hard) | NUM-01: unit 'KCHF' is not ISO 4217 |
| endeavour-mining-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner_name |  | La Mancha | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | fte |  | 5659 | Fail (hard) | CORE-02: 5659 not in the quote |
| endeavour-mining-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | revenue_by_segment |  | Ity Mine: 838.1; Houndé Mine:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| enquest-plc | revenue_by_country |  | North Sea: 895313; Malaysia: 1 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | share_price |  | 7.666 | Fail (hard) | CORE-02: 7.666 not in the quote |
| epic-suisse-ag-7c2f8dc4 | benefits_value | Executive Chairman | 10000 | Fail (hard) | CORE-02: 10 not in the quote |
| epigenomics-ag-ddb6ea6d | total_remuneration | Former Vorstand (until January | -33000 | Fail (hard) | NUM-04: -33000 outside 0..5e+10; XF-01: parts add up to -32,468, more than the stated -33,000 |
| erste-group-bank-ag | exchange |  | Vienna | Fail (hard) | COD-01: 'Vienna' matches no ISO 10383 exchange |
| erste-group-bank-ag | listing_date |  | 1997-12-04 | Fail (hard) | CORE-02: not in the quote: 1997 |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 800128.68 | Fail (hard) | CORE-02: 800128.68 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_vested | Chief Corporates and Markets O | 435250.84 | Fail (hard) | CORE-02: 435250.84 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Financial Officer | 435616.87 | Fail (hard) | CORE-02: 435616.87 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Risk Officer | 426532.06 | Fail (hard) | CORE-02: 426532.06 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Chief Platform Officer / Chief | 312811.9 | Fail (hard) | CORE-02: 312811.9 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | lti_vested | Ehemalige Vorstandsmitglieder | 3066144.73 | Fail (hard) | CORE-02: 3066144.73 not in the quote; CORE-03: quote not in the source text |
| erste-group-bank-ag | other_names |  | Erste oesterreichische Spar-Ca | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | staff_by_country |  | Austria: 20111; Czechia: 10097 | Fail | CORE-04: no period_end; NUM-08: adds up to 49,024 vs 46,000 (6.6% apart) |
| erste-group-bank-ag | sti_max | Vorsitzender des Vorstands / C | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| erste-group-bank-ag | sti_max | Chief Corporates and Markets O | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| erste-group-bank-ag | sti_max | Chief Financial Officer | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| erste-group-bank-ag | sti_max | Chief Risk Officer | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| erste-group-bank-ag | sti_max | Chief Platform Officer / Chief | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| erste-group-bank-ag | sti_paid | Ehemalige Vorstandsmitglieder | 763537.04 | Fail (hard) | CORE-02: 763537.04 not in the quote |
| eurocell-plc | listing_date |  | 2015-03 | Fail (hard) | COD-06: not a year or a date |
| eurocell-plc | share_price |  | 130.5 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| eurotelesites-ag | revenue_by_country |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | revenue_by_segment |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | sti_paid | CEO | 132000 | Fail (hard) | CORE-02: 132000 not in the quote |
| eurotelesites-ag | sti_paid | CFO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| everest-global-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | controlling_owner_name |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | largest_holders |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | share_price |  | 2.51 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
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
| fair-value-reit-ag-cef1dc63 | exchange |  | Frankfurt Stock Exchange | Fail (hard) | CORE-02: not in the quote: stock exchange |
| fair-value-reit-ag-cef1dc63 | sub_sector |  | Immobilienbestandshalter mit F | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Övriga ledande befattningshava | 5 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | benefits |  | fast lön, övriga förmåner, pen | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | isin |  | SE0016785786 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | pension_type |  | premiebaserad pensionslösning | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | role_disclosure | VD | individual | Fail (hard) | CORE-03: quote not in the source text |
| fastpartner-d | base_salary | Other members of company’s man | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | base_salary | Other members of the Executive | 12529000 | Fail (hard) | CORE-02: 12529000 not in the quote |
| fastpartner-d | pension_contribution | Other members of company’s man | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | pension_contribution | Other members of the Executive | 3667000 | Fail (hard) | CORE-02: 3667000 not in the quote |
| fastpartner-d | sti_max | Other members of the Executive | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: quote on page 103, link says page 102 |
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
| intea-fastigheter-d | revenue_by_segment |  | Rättsväsende: 983; Högre utbil | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,779,000,000 vs 1,561,000,000 (14.0% apart) |
| intea-fastigheter-d | role_disclosure | Övriga ledande befattningshava | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| intershop-holding-ag-6e9d3cef | benefits |  | benefits in kind | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intica-systems-se-18005922 | sti_max | Vorsitzender des Vorstands | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intica-systems-se-18005922 | sti_max | Mitglied des Vorstands (bis 30 | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ivu-traffic-techn-ag-020c6212 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
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
| kapsch-trafficcom-ag-1d6bbc81 | ebitda |  | 20600000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kapsch-trafficcom-ag-1d6bbc81 | revenue_by_country |  | Österreich: 15982; EMEA (exklu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ultimate_parent |  | Traditio-Privatstiftung; CHILD | Fail (hard) | CORE-02: not in the quote: traditio privatstiftung |
| kesko-b | controlling_owner_name |  | K-kauppiasliitto ry | Fail (hard) | CORE-02: not in the quote: ry |
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
| komax | staff_by_segment |  | Production: 674; Research and  | Fail | CORE-04: no period_end; NUM-08: adds up to 1,841 vs 3,167 (41.9% apart) |
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
| linz-textil-holding-ag-e11cf1a9 | ebitda |  | 939336 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| maschinenfabrik-berthold-hermle-6808fdaf | staff_by_country |  | Germany: 1228 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,228 vs 1,639 (25.1% apart) |
| masterflex-96d8f19f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| mayr-melnhof-karton-ag-ef1c26e1 | staff_by_country |  | Poland: 3027; Germany: 2091; A | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mbb-se-be761dea | lti_target | Executive Chairman | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mbb-se-be761dea | lti_target | CFO | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mch-group-ag-c6fc7898 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| medartis-holding-ag-4ef02932 | shareholding_requirement |  | BoD: shares equal to one year  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| medartis-holding-ag-4ef02932 | sti_max | Other members of the EMB | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| meier-tobler-group-ag-f96a3151 | benefits |  | Geschäftsfahrzeug | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| melhus-sparebank | pension_type |  | Defined contribution for emplo | Fail (hard) | CORE-03: quote not in the source text |
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
| mobilezone-holding-ag-fc013b59 | aggregate_headcount | Management Board | 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | benefits |  | lump-sum expenses approved by  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | role_disclosure | Executive Delegate of the Boar | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Management Board | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Executive Delegate of the Boar | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| molecular-partners-ag-86d659ae | pension_type |  | defined benefit plans; compuls | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mueller-die-lila-logistik-se-f3c40a4b | revenue_by_segment |  | Lila Operating: 249948; Lila R | Fail | CORE-04: no period_end; NUM-08: adds up to 250,478,000 vs 11,374,899 (2102.0% apart) |
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
| omv-ag-2c5e8b21 | lti_target | Chairman of the Executive Boar | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Energ | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Fuels | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Vice Presiden | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Deputy Chairman of the  | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Officer Marke | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| orior-ag-bfeb91d6 | aggregate_headcount | Executive Committee excl. CFO | 3.1 | Fail (hard) | NUM-05: not a whole number |
| orior-ag-bfeb91d6 | aggregate_headcount | Former Executive Committee mem | 0.4 | Fail (hard) | NUM-04: 0.4 outside 1..500; NUM-05: not a whole number |
| ostasiatiske | exchange |  | NASDAQ Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ Copenhagen A/S' matches no ISO 10383 exchange |
| palfinger-ag-e07e19f6 | exchange_segment |  | Prime Market | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| palfinger-ag-e07e19f6 | revenue_by_country |  | Inland: 44423.1; EU: 21235.8;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 77,550,800 vs 2,339,288,000 (96.7% apart) |
| palfinger-ag-e07e19f6 | staff_by_country |  | Österreich: 2707; Russland: 15 | Fail | CORE-04: no period_end; NUM-08: adds up to 5,657 vs 12,358 (54.2% apart) |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| partners-group-holding-ag-d09fd15d | lti_granted | Chief Executive Officer | 14055000 | Fail (hard) | CORE-02: 14055 not in the quote |
| partners-group-holding-ag-d09fd15d | lti_granted | Executive Team | 54733000 | Fail (hard) | CORE-02: 54733 not in the quote |
| partners-group-holding-ag-d09fd15d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| path2-hydrogen-ag-4a522574 | base_salary | Vorstand (bis 27.03.2025) | 60000 | Fail (hard) | CORE-02: 60000 not in the quote |
| path2-hydrogen-ag-4a522574 | benefits_value | Vorstand (bis 27.03.2025) | 1500 | Fail (hard) | CORE-02: 1500 not in the quote |
| path2-hydrogen-ag-4a522574 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| patrizia-se-41659152 | revenue_by_segment |  | Investment Management: 264348; | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 276,070,000 vs 258,416,000 (6.8% apart) |
| pearl-gold-ag-da4e9b62 | listing_date |  | 2012-09 | Fail (hard) | COD-06: not a year or a date |
| pearl-gold-ag-da4e9b62 | pension_type |  | Ruhegehalts- und Vorruhestands | Fail (hard) | CORE-03: quote not in the source text |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| pfeiffer-vacuum-tech-ag-a38e65f0 | controlling_owner_name |  | Busch Group | Fail (hard) | CORE-02: not in the quote: group |
| pfeiffer-vacuum-tech-ag-a38e65f0 | staff_by_segment |  | Deutschland: 990; Frankreich:  | Fail | CORE-04: no period_end; NUM-08: adds up to 1,815 vs 3,847 (52.8% apart) |
| pferdewetten-de-ag-07705286 | aggregate_headcount | Vorstand | 3 | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | benefits |  | Dienstwagen, Mobilitätszulage, | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | shareholding_requirement |  | CEO and Prokurist received loa | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | website |  | pferdewetten.ag | Fail (hard) | CORE-03: quote not in the source text |
| phoenix-mecano-ag-d882ab5c | base_salary | Management | 1934000 | Fail (hard) | CORE-02: 1934 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | Chairman of the Board of Direc | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | CEO | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| pittler-maschinenfabrik-ag-fb62b449 | benefits_value | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | controlling_owner_name |  | Herr Günter Rothenberger | Fail (hard) | CORE-02: not in the quote: nter |
| planoptik-ag-9429909d | benefits |  | Zuschüsse zur Kranken- und Pfl | Fail (hard) | CORE-03: quote not in the source text |
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
| rath-ag-9e9ac567 | sti_paid | Member of the Management Board | 44000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 349000 | Fail (hard) | XF-01: parts add up to 364,000, more than the stated 349,000; XF-02: parts add up to 364,000, stated 349,000 |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 419000 | Fail (hard) | XF-01: parts add up to 429,000, more than the stated 419,000; XF-02: parts add up to 429,000, stated 419,000 |
| readcrest-capital-ag-e4689651 | ebitda |  | -39546000 | Fail (hard) | CORE-02: -39546000 not in the quote |
| readcrest-capital-ag-e4689651 | fte |  | 0 | Fail | CORE-04: no period_end; NUM-04: 0 outside 0.5..5e+06 |
| readcrest-capital-ag-e4689651 | revenue_by_segment |  | Pflegedienstleistungen: 128309 | Fail (hard) | CORE-03: quote not in the source text |
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
| rosenbauer | staff_by_country |  | Austria: 1632; Germany: 1038;  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,312 vs 4,922 (12.4% apart) |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member (since  | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | sti_max | Executive Board member | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| rosenbauer | total_remuneration | Executive Board member (since  | 601000 | Fail (hard) | XF-01: parts add up to 1,009,000, more than the stated 601,000; XF-02: parts add up to 1,009,000, stated 601,000 |
| rosenbauer | total_remuneration | Executive Board member (since  | 263000 | Fail (hard) | XF-01: parts add up to 501,000, more than the stated 263,000; XF-02: parts add up to 501,000, stated 263,000 |
| rosenbauer | total_remuneration | Executive Board member | 406000 | Fail (hard) | XF-01: parts add up to 741,000, more than the stated 406,000; XF-02: parts add up to 741,000, stated 406,000 |
| s-d-standard-etc | controlling_owner_name |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-d-standard-etc | ebitda |  | 4158000 | Fail (hard) | CORE-02: 4158000 not in the quote |
| s-d-standard-etc | revenue |  | 5920000 | Fail (hard) | CORE-02: 5920000 not in the quote |
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
| sca-a | revenue_by_segment |  | Forest: 9962; Wood: 6125; Pulp | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 30,231,000,000 vs 20,427,000,000 (48.0% apart) |
| sca-a | total_remuneration | Other senior executives | 32037696 | Fail (hard) | XF-01: parts add up to 40,234,080, more than the stated 32,037,696; XF-02: parts add up to 40,234,080, stated 32,037,696 |
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
| seb-c | revenue |  | -411000 | Fail | CORE-04: no period_end; NUM-04: -411000 outside 0..1e+14 |
| seb-c | revenue_by_country |  | Sweden: 46498; Norway: 4315; D | Fail | CORE-04: no period_end; NUM-08: adds up to 76,903,000,000 vs -411,000 (18711292.2% apart) |
| seb-c | revenue_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 76,928,000,000 vs -411,000 (18717374.9% apart) |
| seb-c | staff_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 11,889 vs 189 (6190.5% apart) |
| seb-c | total_remuneration | VD samt vice VD | -8931000 | Fail (hard) | NUM-04: -8.931e+06 outside 0..5e+10; XF-01: parts add up to -8,931,000, more than the stated -8,931,000 |
| seb-c | total_remuneration | Risktagare | -24486000 | Fail (hard) | NUM-04: -2.4486e+07 outside 0..5e+10; XF-01: parts add up to -24,486,000, more than the stated -24,486,000 |
| seb-c | total_remuneration | Övriga | -157650000 | Fail (hard) | NUM-04: -1.5765e+08 outside 0..5e+10; XF-01: parts add up to -157,651,000, more than the stated -157,650,000 |
| secunet-security-ag-c4d9b7e4 | headcount |  | 1171 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| secunet-security-ag-c4d9b7e4 | total_assets |  | 410700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sed-energy | total_remuneration | Key management personnel | 900 | Fail (hard) | XF-01: parts add up to 1,559,000, more than the stated 900; XF-02: parts add up to 1,559,000, stated 900 |
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
| sentia | revenue_by_country |  | Norway: 9404; Sweden: 2369 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| sgs-ag-65380806 | aggregate_headcount | Other ExCo | 13 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | benefits_value | Chief Executive Officer | 24000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | pension_contribution | Chief Executive Officer | 119000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | revenue_by_country |  | North America: 1.5 | Fail | CORE-04: no period_end |
| sgs-ag-65380806 | total_remuneration | Chief Executive Officer | 1393000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 4,355,000, more than the stated 1,393,000; XF-02: parts add up to 4,355,000, stated 1,393,000 |
| siemens-health-ag-1a42fb66 | revenue_by_country |  | Europe, C.I.S., Africa, Middle | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| siemens-health-ag-1a42fb66 | sub_sector |  | Siemens Healthineers offers im | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| singulus-technol-66103de1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| singulus-technol-66103de1 | controlling_owner_name |  | Triumph Science & Technology G | Fail (hard) | CORE-03: quote not in the source text |
| singulus-technol-66103de1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| sino-german-united-ag-388acb2d | benefits |  | D&O-Versicherung, D&O Selbstbe | Fail (hard) | CORE-03: quote not in the source text |
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
| softing-ag-365a9352 | share_price |  | 2.62 | Fail (hard) | CORE-03: quote not in the source text |
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
| sparebank-1-helgeland | sti_paid | Direktør risikostyring | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| sparebank-1-nordmore | benefits |  | Ansattbetingelser, mobil og bi | Fail (hard) | CORE-03: quote not in the source text |
| ssab-b | headcount |  | 14609 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ssab-b | listing_date |  | 1988 | Fail (hard) | CORE-02: not in the quote: 1988 |
| ssab-b | shareholding_requirement |  | LTI participants must hold sha | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| st-galler-kantonalbank-ag-ba864955 | shareholding_requirement |  | For Board of Directors: 30% of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stabilus-se-52dccb73 | sub_sector |  | specializing in particular in  | Fail (hard) | CORE-03: quote not in the source text |
| stadlauer-malzfabrik-ag-8a23c30d | sub_sector |  | Holdingfunktion | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| starragtornos-group-ag-15e3832b | base_salary | Other members of the Executive | 637000 | Fail (hard) | CORE-02: 637 not in the quote |
| starragtornos-group-ag-15e3832b | benefits_value | Other members of the Executive | 26000 | Fail (hard) | CORE-02: 26 not in the quote |
| starragtornos-group-ag-15e3832b | pension_contribution | Other members of the Executive | 130000 | Fail (hard) | CORE-02: 130 not in the quote |
| starragtornos-group-ag-15e3832b | sti_paid | Other members of the Executive | 7000 | Fail (hard) | CORE-02: 7 not in the quote |
| starragtornos-group-ag-15e3832b | total_remuneration | Other members of the Executive | 799000 | Fail (hard) | CORE-02: 799 not in the quote |
| stora-enso-a | exchange |  | Nasdaq Helsinki;Nasdaq Stockho | Fail (hard) | CORE-02: not in the quote: nasdaq |
| stora-enso-a | lti_granted | CEO | 380200 | Fail (hard) | CORE-02: 380200 not in the quote |
| stora-enso-r | benefits |  | pension, disability, death, an | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | benefits_value | Other members of Group Leaders | 250000 | Fail (hard) | CORE-02: 250 not in the quote |
| strabag-se-8e9d954e | staff_by_segment |  | North + West: 23161 | Fail | CORE-04: no period_end; NUM-08: adds up to 23,161 vs 88,556 (73.8% apart) |
| straumann-holding-ag-d8e91d7f | lti_vested | CEO | 180000 | Fail (hard) | CORE-02: 180 not in the quote |
| subsea7 | staff_by_segment |  | Onshore: 9205; Offshore: 5867 | Fail | CORE-04: no period_end; NUM-08: adds up to 15,072 vs 13,821 (9.1% apart) |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (Klaus Einfalt) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (János Váczi) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| swiss-re-ag-6528d850 | benefits_value | Group Chief Executive Officer | 27000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | lti_vested | Group Chief Executive Officer | 3394000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | sti_max | Group Chief Executive Officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| swiss-re-ag-6528d850 | total_remuneration | Group Chief Executive Officer | 6065000 | Fail (hard) | XF-01: parts add up to 6,292,000, more than the stated 6,065,000; XF-02: parts add up to 6,292,000, stated 6,065,000 |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
| tekna-holding | benefits |  | Health insurance plan, company | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | controlling_owner_name |  | Arendals Fossekompani ASA | Fail (hard) | CORE-02: not in the quote: arendals fossekompani asa |
| tekna-holding | lti_granted | EVP - Materials, Managing dire | 200000 | Fail (hard) | CORE-03: quote not in the source text |
| telekom-austria-ag-62fec5fa | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| temenos-ag-21209ec1 | shareholding_requirement |  | CEO: 5 times annual fixed sala | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| the-swatch-group-ag-6a144b9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| thurgauer-kantonalbank-3b36a058 | benefits |  | For Bank Council members: occa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| thurgauer-kantonalbank-3b36a058 | pension_type |  | defined contribution. For fixe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| tkms-ag-co-kgaa-f468ef4d | aggregate_headcount | TKMS Management Board | 4 | Fail (hard) | CORE-03: quote not in the source text |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | sti_max | CEO | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | sti_max | CFO (until July 2024) | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| tx-group-ag-cdcf98d0 | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| uie | sti_max | Managing Director | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| utd-internet-ag-fa5f4803 | controlling_owner_name |  | Ralph Dommermuth | Fail (hard) | CORE-02: not in the quote: ralph |
| vat-group-ag-ccdd96de | pay_currency | CEO (since January 1, 2024) | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pay_currency | Other GEC | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pension_type |  | occupational pension plans, in | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| verbio-se-9b8df34d | listing_date |  | 2006 | Fail (hard) | CORE-02: not in the quote: 2006 |
| verbio-se-9b8df34d | revenue_by_country |  | Germany: 1079756; Poland: 2799 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,608,060,000 vs 1,872,665,000 (14.1% apart) |
| verbund | lti_received | CRO (from 1 January 2024) | 0 | Fail (hard) | CORE-03: quote on page 21, link says page 19 |
| verbund | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| verbund | pay_currency | CFO | EUR | Fail | CORE-04: no period_end |
| verbund | pay_currency | COO | EUR | Fail | CORE-04: no period_end |
| verbund | pay_currency | CRO (from 1 January 2024) | EUR | Fail | CORE-04: no period_end |
| verbund | pension_contribution | CRO (from 1 January 2024) | 49000 | Fail (hard) | CORE-03: quote on page 21, link says page 19 |
| verbund | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote on page 20, link says page 19 |
| verbund | role_disclosure | CRO (from 1 January 2024) | individual | Fail (hard) | CORE-03: quote on page 21, link says page 19 |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Administratrice (Membre non ex | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Ancien Président | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villeroy-boch-ag-c5a85d57 | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | listing_date |  | 1990 | Fail (hard) | CORE-02: not in the quote: 1990 |
| villeroy-boch-ag-c5a85d57 | pension_type |  | defined contribution, 15 % of  | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | role_disclosure | Vorstandsvorsitzende (seit 01. | individual | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | shares_outstanding |  | 26765754 | Fail (hard) | CORE-02: 26765754 not in the quote; CORE-03: quote not in the source text |
| viscom-se-859e40d6 | base_salary | Vorstand Vertrieb / Operations | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | base_salary | Vorstand Entwicklung / Produkt | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | base_salary | Vorstand Finanzen | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | controlling_owner_name |  | Dr. Martin Heuser and Volker P | Fail (hard) | CORE-02: not in the quote: and |
| viscom-se-859e40d6 | listing_date |  | 2006-05 | Fail (hard) | COD-06: not a year or a date |
| viscom-se-859e40d6 | role_disclosure | Vorstand Vertrieb / Operations | individual | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | role_disclosure | Vorstand Entwicklung / Produkt | individual | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | role_disclosure | Vorstand Finanzen | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | lti_max | Integrity and Legal Affairs | 3750000 | Fail (hard) | CORE-02: 3750000 not in the quote |
| volkswagen-ag-be878a5e | lti_target | Integrity and Legal Affairs | 1875000 | Fail (hard) | CORE-02: 1875000 not in the quote |
| volkswagen-ag-be878a5e | role_disclosure | Chair, Sport Luxury brand grou | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | role_disclosure | Finance and Operations | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | role_disclosure | China, Chair of the Board of M | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | role_disclosure | Progressive brand group, Chair | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | role_disclosure | Integrity and Legal Affairs | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | role_disclosure | Human Resources and Trucks bra | individual | Fail (hard) | CORE-03: quote not in the source text |
| volkswagen-ag-be878a5e | sti_max | Integrity and Legal Affairs | 2250000 | Fail (hard) | CORE-02: 2250000 not in the quote |
| volkswagen-ag-be878a5e | sti_target | Integrity and Legal Affairs | 1125000 | Fail (hard) | CORE-02: 1125000 not in the quote |
| volkswagen-ag-be878a5e | total_remuneration | Finance and Operations | 5075339.19 | Fail (hard) | XF-01: parts add up to 5,683,225, more than the stated 5,075,339; XF-02: parts add up to 5,683,225, stated 5,075,339 |
| volkswagen-ag-be878a5e | total_remuneration | China, Chair of the Board of M | 3837923 | Fail (hard) | XF-01: parts add up to 4,443,267, more than the stated 3,837,923; XF-02: parts add up to 4,443,267, stated 3,837,923 |
| volkswagen-ag-be878a5e | total_remuneration | Progressive brand group, Chair | 3404523 | Fail (hard) | XF-01: parts add up to 4,029,494, more than the stated 3,404,523; XF-02: parts add up to 4,029,494, stated 3,404,523 |
| volkswagen-ag-be878a5e | total_remuneration | Integrity and Legal Affairs | 2545518 | Fail (hard) | XF-01: parts add up to 2,995,518, more than the stated 2,545,518; XF-02: parts add up to 2,995,518, stated 2,545,518 |
| volkswagen-ag-be878a5e | total_remuneration | Human Resources and Trucks bra | 1791959.7 | Fail (hard) | XF-01: parts add up to 2,033,682, more than the stated 1,791,960; XF-02: parts add up to 2,033,682, stated 1,791,960 |
| volkswagen-ag-be878a5e | total_remuneration | Core brand group, Chair of the | 3401649 | Fail (hard) | XF-01: parts add up to 4,012,452, more than the stated 3,401,649; XF-02: parts add up to 4,012,452, stated 3,401,649 |
| volkswagen-ag-be878a5e | total_remuneration | Technology, Chair of the Board | 5630301.3 | Fail (hard) | XF-01: parts add up to 6,236,765, more than the stated 5,630,301; XF-02: parts add up to 6,236,765, stated 5,630,301 |
| volkswagen-ag-be878a5e | total_remuneration | IT | 3401076 | Fail (hard) | XF-01: parts add up to 4,026,786, more than the stated 3,401,076; XF-02: parts add up to 4,026,786, stated 3,401,076 |
| volkswagen-ag-be878a5e | total_remuneration | Former Board of Management mem | 1560554.53 | Fail (hard) | XF-01: parts add up to 1,676,039, more than the stated 1,560,555; XF-02: parts add up to 1,676,039, stated 1,560,555 |
| vontobel-holding-ag-1d88ea32 | lti_vested | Executive Committee | 7400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | pension_contribution | Executive Committee | 700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | sti_paid | Executive Committee | 3000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | total_remuneration | Executive Committee | 15000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| wasgau-produktions-handels-8c33a77d | lti_max | Mitglied des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Mitglied des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | role_disclosure | Mitglied des Vorstands (ab 01/ | individual | Fail (hard) | CORE-03: quote not in the source text |
| wasgau-produktions-handels-8c33a77d | role_disclosure | Ehemaliges Mitglied des Vorsta | individual | Fail (hard) | CORE-03: quote not in the source text |
| wolford-ag-638e2dc1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | controlling_owner_name |  | FFG Wisdom (Luxembourg) S.à r. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | headcount |  | 712 | Fail (hard) | CORE-02: 712 not in the quote |
| wolford-ag-638e2dc1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | staff_by_country |  | Slovenia: 160; Austria: 209 | Fail | CORE-04: no period_end; NUM-08: adds up to 369 vs 712 (48.2% apart) |
| wuestenrot-wuerttembergische-ag-07b9dfbc | revenue_by_segment |  | Housing: 1074; Life and health | Fail (hard) | CORE-03: quote not in the source text |
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
| zuger-kantonalbank-67b7c3b8 | pay_currency | Präsident der Geschäftsleitung | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | pay_currency | Geschäftsleitung (total) | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Präsident der Geschäftsleitung | 850000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 938,000, more than the stated 850,000; XF-02: parts add up to 938,000, stated 850,000 |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Geschäftsleitung (total) | 3123000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,415,000, more than the stated 3,123,000; XF-02: parts add up to 3,415,000, stated 3,123,000 |
