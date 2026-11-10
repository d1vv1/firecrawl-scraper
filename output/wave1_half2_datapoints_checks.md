# Output checks: wave1_half2_datapoints.csv

95 companies, 4397 filled values checked (2026-11-10, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 3734 (85%) |
| Review | 260 (6%) |
| Fail | 42 (1%) |
| Fail (hard) | 361 (8%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 532 | 530 | 0 | 0 | 2 |
| Listing and market | 405 | 397 | 0 | 0 | 8 |
| Sector | 151 | 149 | 0 | 0 | 2 |
| Reporting basis | 284 | 284 | 0 | 0 | 0 |
| Financials | 298 | 248 | 13 | 0 | 37 |
| Workforce | 96 | 66 | 11 | 0 | 19 |
| Ownership and control | 285 | 264 | 0 | 0 | 21 |
| Segment and geography | 128 | 75 | 13 | 8 | 32 |
| Pay policy | 200 | 185 | 0 | 0 | 15 |
| Role and disclosure | 543 | 455 | 7 | 34 | 47 |
| Pay: fixed | 558 | 404 | 90 | 0 | 64 |
| Pay: STI | 363 | 290 | 37 | 0 | 36 |
| Pay: LTI | 353 | 276 | 27 | 0 | 50 |
| Pay: total | 201 | 111 | 62 | 0 | 28 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 4397 | 4395 | 2 | 0 | PDF link without #page= |
| CORE-02 | Value can be read off its quote | yes | 1921 | 1861 | 60 | 2476 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 3038 | 2815 | 223 | 1359 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 2472 | 2182 | 290 | 1925 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 4397 | 4397 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 1435 | 1417 | 18 | 2962 | US$ is not ISO N |
| COD-02 | Classification scheme named |  | 76 | 76 | 0 | 4321 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 163 | 163 | 0 | 4234 |  |
| COD-06 | Dates are valid | yes | 117 | 116 | 1 | 4280 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1328 | 1272 | 56 | 3069 | unit 'US$' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1227 | 1227 | 0 | 3170 |  |
| NUM-04 | Magnitude in a plausible range |  | 1512 | 1509 | 3 | 2885 | Ne+N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 135 | 133 | 2 | 4262 | not a whole number |
| NUM-06 | Percentages in range | yes | 308 | 307 | 1 | 4089 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 55 | 54 | 1 | 4342 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 116 | 89 | 27 | 4281 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 184 | 184 | 0 | 4213 |  |
| NUM-11 | STI paid not above its maximum |  | 85 | 80 | 5 | 4312 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1090 | 1088 | 2 | 3307 | currency GBPN the role's other amounts EUR |
| NUM-13 | FTE not above headcount |  | 32 | 27 | 5 | 4365 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 29 | 29 | 0 | 4368 |  |
| DER-06 | Derived value shows its formula |  | 169 | 169 | 0 | 4228 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 182 | 175 | 7 | 4215 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 182 | 129 | 53 | 4215 | parts add up to N stated N |

## Fill rate

Company fields: 2379 of 3895 filled (61%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 14 | 95 |
| staff_by_segment | 15 | 95 |
| staff_by_country | 24 | 95 |
| controlling_owner_name | 28 | 95 |
| market_cap_band | 29 | 95 |
| share_price | 38 | 95 |
| exchange_segment | 39 | 95 |
| other_names | 42 | 95 |
| listing_date | 43 | 95 |
| revenue_by_country | 43 | 95 |
| revenue_by_segment | 46 | 95 |
| headcount | 47 | 95 |
| fte | 49 | 95 |
| controlling_owner | 49 | 95 |
| ownership_type | 49 | 95 |
| pe_stake_5pct | 49 | 95 |
| shareholding_requirement | 52 | 95 |
| largest_holders | 55 | 95 |
| ultimate_parent | 55 | 95 |
| shares_outstanding | 60 | 95 |
| ebitda | 64 | 95 |
| fiscal_year | 66 | 95 |
| total_assets | 67 | 95 |
| website | 68 | 95 |
| isin | 69 | 95 |
| revenue | 69 | 95 |
| accounting_basis | 70 | 95 |
| benefits | 72 | 95 |
| ticker | 73 | 95 |
| fiscal_year_end | 74 | 95 |
| reporting_currency | 74 | 95 |
| sub_sector | 75 | 95 |
| exchange | 76 | 95 |
| listing_status | 76 | 95 |
| sector_code | 76 | 95 |
| pension_type | 76 | 95 |
| lei | 80 | 95 |
| legal_name | 82 | 95 |
| business_id | 82 | 95 |
| country_code | 82 | 95 |
| head_office_city | 82 | 95 |

Pay fields, over 231 executive roles:

| Field | Filled |
|---|---|
| base_salary | 204 (88%) |
| sti_paid | 172 (74%) |
| sti_target | 63 (27%) |
| sti_max | 128 (55%) |
| lti_vested | 95 (41%) |
| lti_granted | 89 (39%) |
| lti_target | 56 (24%) |
| lti_max | 113 (49%) |
| benefits_value | 175 (76%) |
| pension_contribution | 179 (77%) |
| total_remuneration | 201 (87%) |

## Failed values (403)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| abb-ltd | listing_status |  | listed | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | revenue_by_country |  | Europe: 11.4; The Americas: 9. | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| abb-ltd | staff_by_country |  | Europe: 53407; The Americas: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 114,292 vs 105,000 (8.8% apart) |
| abb-ltd | sti_paid | Other EC members | 1500000 | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | sti_target | Other EC members | 1190000 | Fail (hard) | CORE-03: quote not in the source text |
| acceler8-ventures-plc | ebitda |  | -172772 | Fail (hard) | CORE-02: -172772 not in the quote |
| accelleron-industries-ag | aggregate_headcount | Former EC members | 1 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | benefits_value | CEO | 290692 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | benefits_value | Other EC members | 731363 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | benefits_value | Former EC members | 43269 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | lti_granted | CEO | 367451 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | lti_granted | Other EC members | 773397 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | lti_granted | Former EC members | 0 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | revenue_by_country |  | Asia, Middle East & Africa: 54 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | role_disclosure | Other EC members | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | role_disclosure | Former EC members | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | staff_by_country |  | Switzerland: 1014; Asia & Midd | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | sti_paid | CEO | 480054 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | sti_paid | Other EC members | 1124777 | Fail (hard) | CORE-03: quote not in the source text |
| accelleron-industries-ag | sti_paid | Former EC members | 0 | Fail (hard) | CORE-03: quote not in the source text |
| acg-metals-limited | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| acg-metals-limited | total_remuneration | Chairman & Chief Executive Off | 1256156 | Fail (hard) | XF-01: parts add up to 1,497,823, more than the stated 1,256,156; XF-02: parts add up to 1,497,823, stated 1,256,156 |
| adecco-group-ag | revenue_by_country |  | France: 4558; Northern Europe: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 17,911,000,000 vs 23,138,000,000 (22.6% apart) |
| african-pioneer-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| alcon-inc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | lti_max | CEO | 1150 | Fail (hard) | NUM-06: 1150 % of base salary |
| alcon-inc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | revenue_by_country |  | United States: 4657; Switzerla | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| also-holding-ag | base_salary | Group Management | 2091000 | Fail (hard) | CORE-02: 2091 not in the quote |
| also-holding-ag | benefits_value | Group Management | 1000 | Fail (hard) | CORE-02: 1 not in the quote |
| also-holding-ag | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | controlling_owner_name |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | fte |  | 5156 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | headcount |  | 5157 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | largest_holders |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | lti_granted | Group Management | 3418000 | Fail (hard) | CORE-02: 3418 not in the quote |
| also-holding-ag | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pension_contribution | Group Management | 181000 | Fail (hard) | CORE-02: 181 not in the quote |
| also-holding-ag | sti_paid | Group Management | 1646000 | Fail (hard) | CORE-02: 1646 not in the quote |
| also-holding-ag | total_remuneration | Group Management | 7337000 | Fail (hard) | CORE-02: 7337 not in the quote |
| amaroq-ltd | base_salary | Chief Executive Officer | 728651 | Fail (hard) | NUM-01: unit 'CA$' is not ISO 4217 |
| amaroq-ltd | benefits_value | Chief Executive Officer | 755210 | Fail (hard) | NUM-01: unit 'CA$' is not ISO 4217 |
| amaroq-ltd | pay_currency | Chief Executive Officer | CA$ | Fail (hard) | COD-01: CA$ is not ISO 4217 |
| amaroq-ltd | pension_type |  | The Corporation does not opera | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amaroq-ltd | revenue |  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| amaroq-ltd | share_price |  | 99.75 | Fail (hard) | NUM-01: unit 'GBX' is not ISO 4217 |
| amaroq-ltd | total_assets |  | 14000 | Fail (hard) | CORE-03: quote not in the source text |
| amaroq-ltd | total_remuneration | Chief Executive Officer | 1483861 | Fail (hard) | NUM-01: unit 'CA$' is not ISO 4217 |
| amicorp-fs-uk-plc | base_salary | Chief Executive Officer | 360753 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | base_salary | Chief Financial Officer (resig | 276437 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | base_salary | Chief Operating Officer (resig | 196623 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | ebitda |  | 2174000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | fte |  | 172 | Fail (hard) | CORE-03: quote not in the source text |
| amicorp-fs-uk-plc | pay_currency | Chief Executive Officer | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| amicorp-fs-uk-plc | pay_currency | Chief Financial Officer (resig | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| amicorp-fs-uk-plc | pay_currency | Chief Operating Officer (resig | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| amicorp-fs-uk-plc | pension_contribution | Chief Executive Officer | 3982 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | total_remuneration | Chief Executive Officer | 364735 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | total_remuneration | Chief Financial Officer (resig | 276437 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| amicorp-fs-uk-plc | total_remuneration | Chief Operating Officer (resig | 196623 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| arbonia-ag | benefits_value | Group Management | 72000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| arbonia-ag | benefits_value | CEO | 32000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| arbonia-ag | pay_currency | Group Management | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| arbonia-ag | pension_contribution | Group Management | 322000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| arbonia-ag | pension_contribution | CEO | 175000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aryzta-ag | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| aryzta-ag | ebitda |  | 306900000 | Fail (hard) | CORE-03: quote not in the source text |
| aryzta-ag | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| aryzta-ag | revenue_by_country |  | Switzerland: 280.9; Germany: 6 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aryzta-ag | revenue_by_segment |  | ARYZTA Europe: 1977; ARYZTA Re | Fail (hard) | CORE-03: quote not in the source text |
| asa-international-group-plc | listing_date |  | 2018 | Fail (hard) | CORE-02: not in the quote: 2018 |
| asa-international-group-plc | lti_vested | Deputy Chairperson and Special | 60 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| asa-international-group-plc | share_price |  | 247 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBp' is not ISO 4217 |
| aseana-properties-limited | base_salary | Executive Director and Chief E | 175138 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | ebitda |  | 15118000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | pay_currency | Executive Director and Chief E | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| aseana-properties-limited | revenue_by_country |  | Malaysia: 14415 | Fail (hard) | CORE-03: quote not in the source text |
| aseana-properties-limited | share_price |  | 0.075 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | total_remuneration | Executive Director and Chief E | 175138 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| ashtead-technology-holdings-plc | fte |  | 649 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 649 above headcount 396 |
| asos-plc | benefits |  | flexible benefits allowance of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | lti_granted | CFO (appointed 1 July 2025) | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| asos-plc | pension_type |  | defined contribution, 5% of ba | Fail (hard) | CORE-03: quote not in the source text |
| astrazeneca-plc | revenue_by_country |  | US: 25450; Emerging Markets: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 65,393,000,000 vs 58,739,000,000 (11.3% apart) |
| atoss-software-se | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | lti_max | Chief Executive Officer (CEO) | 120000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | lti_target | Chief Executive Officer (CEO) | 100000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | lti_target | Executive Board member (CFO) | 70000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | lti_target | Executive Board member (COO) | 85000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | pension_contribution | Executive Board member (CFO) | 41616000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | pension_contribution | Executive Board member (COO) | 54000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | pension_type |  | defined benefits plan for CEO; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| atoss-software-se | sti_max | Chief Executive Officer (CEO) | 240000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | sti_max | Executive Board member (CFO) | 210000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | sti_max | Executive Board member (COO) | 255000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | sti_target | Chief Executive Officer (CEO) | 200000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | sti_target | Executive Board member (CFO) | 140000000 | Fail (hard) | CORE-03: quote not in the source text |
| atoss-software-se | sti_target | Executive Board member (COO) | 170000000 | Fail (hard) | CORE-03: quote not in the source text |
| aurskog-sparebank | base_salary | Leder bedriftsmarked | 1257000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aurskog-sparebank | benefits_value | Leder bedriftsmarked | 80000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aurskog-sparebank | lti_vested | Leder bedriftsmarked | 0 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aurskog-sparebank | pay_currency | administrerende banksjef | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | CFO/banksjef | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | Leder bankdrift | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | Leder sparing og investering | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | Kommunikasjons- og markedssjef | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | Leder personmarked | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pay_currency | Leder bedriftsmarked | NOK | Fail | CORE-04: no period_end |
| aurskog-sparebank | pension_contribution | Leder bedriftsmarked | 156000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aurskog-sparebank | role_disclosure | Leder bedriftsmarked | individual | Fail (hard) | CORE-03: quote not in the source text |
| aurskog-sparebank | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| aurskog-sparebank | sti_paid | Leder bedriftsmarked | 45000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| aurskog-sparebank | total_remuneration | Leder bedriftsmarked | 1538000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| autoneum-holding-ag | base_salary | Group Executive Board | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| avation-plc | base_salary | Executive Chairman | 754000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | base_salary | Executive Director | 226000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | benefits_value | Executive Chairman | 50000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | benefits_value | Executive Director | 54000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | ebitda |  | 46444000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | lti_granted | Executive Chairman | 215000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | lti_granted | Executive Director | 16000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | pay_currency | Executive Chairman | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| avation-plc | pay_currency | Executive Director | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| avation-plc | pension_contribution | Executive Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | pension_contribution | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | sti_paid | Executive Director | 38000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | total_remuneration | Executive Chairman | 1019000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| avation-plc | total_remuneration | Executive Director | 334000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aviva-plc | headcount |  | 36160 | Fail (hard) | CORE-03: quote not in the source text |
| aviva-plc | role_disclosure | Executive Directors | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| aviva-plc | share_price |  | 752.6 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBp' is not ISO 4217 |
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| b-m-european-value-retail-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | interim CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bae-systems-plc | share_price |  | 1880.5 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBX' is not ISO 4217 |
| bakkafrost | ebitda |  | 1672664000 | Fail (hard) | CORE-03: quote not in the source text |
| banque-cantonale-du-jura-sa | benefits |  | Frais de représentation; taux  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| banque-cantonale-du-jura-sa | pay_currency | Directeur général | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pay_currency | Direction | CHF | Fail | CORE-04: no period_end |
| barclays-plc | pension_contribution | Group Chief Executive | 155000 | Fail (hard) | CORE-02: 155 not in the quote |
| barclays-plc | pension_contribution | Group Finance Director | 94000 | Fail (hard) | CORE-02: 94 not in the quote |
| barclays-plc | total_remuneration | Group Chief Executive | 15045000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 4,588,000, stated 15,045,000 |
| barclays-plc | total_remuneration | Group Finance Director | 8970000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,770,000, stated 8,970,000 |
| basellandschaftliche-kantonalbank | headcount |  | 1054 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Managemen | 605000 | Fail (hard) | CORE-02: 605000 not in the quote |
| basellandschaftliche-kantonalbank | pension_type |  | defined contribution, BLKB cov | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must acquire 2 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | staff_by_country |  | Canton of Basel-Landschaft: 92 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Managemen | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basler-ag-o-n | base_salary | Vorstandsvorsitzender (CEO) (u | 367000 | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | controlling_owner_name |  | Norbert Basler Holding GmbH | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | largest_holders |  | Norbert Basler Holding GmbH 53 | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | lti_max | Vorstandsvorsitzender (CEO) (u | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_max | Vorstand Commercial (CCO) und  | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_max | Vorstand Finanzen (CFO) (Eintr | 75 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstandsvorsitzender (CEO) (u | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstand Commercial (CCO) und  | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | lti_target | Vorstand Finanzen (CFO) (Eintr | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basler-ag-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | revenue_by_country |  | EMEA: 78.9; America: 47.9; Asi | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 272,200,000 vs 224,500,000 (21.2% apart) |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstandsvorsitzender (CEO) (u | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstand Commercial (CCO) und  | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | role_disclosure | Vorstand Finanzen (CFO) (Eintr | individual | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | shareholding_requirement |  | 50 % of the variable compensat | Fail (hard) | CORE-03: quote not in the source text |
| basler-ag-o-n | staff_by_country |  | Europe: 708; Asia: 178; Americ | Fail | CORE-04: no period_end; NUM-08: adds up to 920 vs 811 (13.4% apart) |
| basler-ag-o-n | staff_by_segment |  | R&D: 238 | Fail | CORE-04: no period_end; NUM-08: adds up to 238 vs 811 (70.7% apart) |
| basler-ag-o-n | ultimate_parent |  | Norbert Basler Holding GmbH | Fail (hard) | CORE-03: quote not in the source text |
| basler-kantonalbank | controlling_owner_name |  | Canton of Basel-Stadt | Fail (hard) | CORE-02: not in the quote: canton of |
| basler-kantonalbank | fte |  | 1273 | Fail (hard) | CORE-03: quote not in the source text |
| basler-kantonalbank | sub_sector |  | Die Bank versteht die Wahrnehm | Fail (hard) | CORE-03: quote not in the source text |
| batm-advanced-communications-limited | base_salary | Former CFO (until 21 June 2025 | 207000 | Fail (hard) | CORE-03: quote not in the source text |
| batm-advanced-communications-limited | ebitda |  | 18940000 | Fail (hard) | CORE-02: 18.94 not in the quote |
| batm-advanced-communications-limited | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main |
| batm-advanced-communications-limited | revenue_by_segment |  | Networks: 11626; Cyber: 8263;  | Fail (hard) | CORE-03: quote not in the source text |
| batm-advanced-communications-limited | total_remuneration | Former CFO (until 21 June 2025 | 207000 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | CEO | 24059 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | Management Board member (Enver | 18078 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | Management Board member (Sat S | 18462 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | Chief Administrative Officer | 7015 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | Chief Risk Officer | 11881 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | lti_vested | Management Board member (Andre | 17051 | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | revenue_by_country |  | Austria: 1020.5; Germany: 490. | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | revenue_by_segment |  | Retail & SME: 1876; Corporates | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | shareholding_requirement |  | CEO: 5x annual base salary; Ot | Fail (hard) | CORE-03: quote not in the source text |
| bawag-group-ag | sub_sector |  | BAWAG’s primary value creation | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| belimo-holding-ag | base_salary | CEO | 570000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | base_salary | Other members, Executive Commi | 2108000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_country |  | EMEA: 240.3; Americas: 341.3;  | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_segment |  | Damper Actuators: 253.8; Contr | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | role_disclosure | Other members, Executive Commi | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | CEO | 817000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | Other members, Executive Commi | 2449000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | total_remuneration | CEO | 1749000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,539,000, stated 1,749,000 |
| belimo-holding-ag | total_remuneration | Other members, Executive Commi | 5573000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 5,108,000, stated 5,573,000 |
| bellevue-group-ag | headcount |  | 72.8 | Fail (hard) | NUM-05: not a whole number |
| bellevue-group-ag | revenue_by_country |  | Switzerland: 47705; United Kin | Fail (hard) | CORE-03: quote not in the source text |
| bellevue-group-ag | total_assets |  | 155563000 | Fail (hard) | CORE-02: 155563 not in the quote; CORE-04: no period_end |
| berner-kantonalbank-ag | benefits_value | Geschäftsleitung | 30000 | Fail (hard) | CORE-02: 30000 not in the quote |
| berner-kantonalbank-ag | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| berner-kantonalbank-ag | revenue |  | 460000000 | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | role_disclosure | vice-CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | sti_max | Geschäftsleitung | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| bertrandt-ag-o-n | aggregate_headcount | Executive Board | 3 | Fail (hard) | CORE-03: quote not in the source text |
| bertrandt-ag-o-n | aggregate_headcount | Management Board | 3 | Fail (hard) | CORE-03: quote not in the source text |
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
| big-yellow-group-plc | fte |  | 453 | Fail (hard) | CORE-03: quote not in the source text |
| big-yellow-group-plc | listing_date |  | May 2000 | Fail (hard) | CORE-02: not a year or a date (see COD-06); COD-06: not a year or a date |
| big-yellow-group-plc | share_price |  | 967.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bp-plc | base_salary | Interim CEO (from 18 December  | 733000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | base_salary | Chief executive officer (until | 854000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | base_salary | Chief financial officer | 387000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | base_salary | Other executive directors | 2573000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | fte |  | 4158 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | headcount |  | 93700 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | lti_vested | Interim CEO (from 18 December  | 83000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | lti_vested | Chief executive officer (until | 2594000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | lti_vested | Chief financial officer | 1545000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | lti_vested | Other executive directors | 734000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | pension_contribution | Interim CEO (from 18 December  | 2000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | pension_contribution | Chief executive officer (until | 138000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | pension_contribution | Chief financial officer | 82000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | pension_contribution | Other executive directors | 132000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | revenue_by_country |  | US: 56703; Non-US: 132632; UK: | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 218,049,000,000 vs 192,549,000,000 (13.2% apart) |
| bp-plc | sti_paid | Interim CEO (from 18 December  | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | sti_paid | Chief executive officer (until | 287000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | sti_paid | Chief financial officer | 169000 | Fail (hard) | CORE-03: quote not in the source text |
| bp-plc | sti_paid | Other executive directors | 290000 | Fail (hard) | CORE-03: quote not in the source text |
| braemar-plc | base_salary | Former Group Chief Operating O | 7200 | Fail (hard) | CORE-02: 7.2 not in the quote |
| braemar-plc | pension_contribution | Group Chief Financial and Oper | 23100 | Fail (hard) | CORE-03: quote not in the source text |
| braemar-plc | revenue_by_segment |  | Chartering: 74713; Investment  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| braemar-plc | sti_paid | Group Chief Financial and Oper | 400000 | Fail (hard) | CORE-03: quote not in the source text |
| british-american-tobacco-plc | other_names |  | British American Tobacco Compa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| british-american-tobacco-plc | revenue_by_segment |  | NGP: 397; Strategic Portfolio: | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 17,108,000,000 vs 25,610,000,000 (33.2% apart) |
| brondbyernes-if | pay_currency | Adm. Direktør (until 28. febru | DKK | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | CFO (from 1. juli 2025) | DKK | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | Direktionen (Total) | DKK | Fail | CORE-04: no period_end |
| bsf-enterprise-plc | lti_granted | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | pension_contribution | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| bsf-enterprise-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| bunzl-plc | revenue_by_segment |  | North America: 6276.7; Contine | Fail (hard) | CORE-03: quote not in the source text |
| bunzl-plc | share_price |  | 2923.67 | Fail (hard) | NUM-01: unit 'GBp' is not ISO 4217 |
| burberry-group-plc | lti_max | CFO | 175 | Fail (hard) | CORE-03: quote not in the source text |
| burckhardt-compression-holding-ag | revenue_by_country |  | Europe: 194414; Africa: 10564; | Fail (hard) | CORE-03: quote not in the source text |
| bvz-holding-ag | revenue_by_segment |  | Gornergrat: 47.1; Immobilien:  | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 181,900,000 vs 216,170,312 (15.9% apart) |
| c-c-group-plc | lti_granted | Chief Financial and Transforma | 404411 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| c-c-group-plc | revenue_by_segment |  | Branded: 453.6; Distribution:  | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,861,600,000 vs 1,569,800,000 (18.6% apart) |
| caffyns-plc | headcount |  | 485 | Fail (hard) | CORE-02: 485 not in the quote |
| canal-s-a | lti_granted | CEO | 982502 | Fail (hard) | CORE-02: 982502 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| canal-s-a | lti_granted | Management Board | 989544 | Fail (hard) | CORE-02: 989544 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| canal-s-a | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| canal-s-a | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| cancom-se-o-n | ebitda |  | 102700000 | Fail (hard) | CORE-02: 102.7 not in the quote |
| cancom-se-o-n | share_price |  | 26.65 | Fail (hard) | CORE-02: 26.65 not in the quote |
| capita-plc | share_price |  | 4.055 | Fail (hard) | CORE-02: 4.055 not in the quote |
| capita-plc | shares_outstanding |  | 120030667 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | benefits_value | Chief Executive Officer | 14082 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | ebitda |  | 5700000 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | fte |  | 41 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | lti_vested | Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | pension_contribution | Chief Executive Officer | 62500 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | revenue_by_segment |  | Egypt: 134.3; Other Capricorn  | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| capricorn-energy-plc | sti_paid | Chief Executive Officer | 550000 | Fail (hard) | CORE-03: quote not in the source text |
| capricorn-energy-plc | sti_target | Chief Executive Officer | 62.5 | Fail (hard) | CORE-02: 62.5 not in the quote |
| capricorn-energy-plc | total_remuneration | Chief Executive Officer | 1126582 | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: quote not in the source text |
| chemring-group-plc | lti_vested | Chief Financial Officer | 230000 | Fail (hard) | CORE-02: 230 not in the quote |
| chemring-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chemring-group-plc | shares_outstanding |  | 272099390 | Fail (hard) | CORE-02: 272099390 not in the quote; CORE-03: quote not in the source text |
| chemring-group-plc | sti_max | Group Chief Executive | 150 | Fail (hard) | CORE-03: quote not in the source text |
| chemring-group-plc | sti_target | Group Chief Executive | 150 | Fail (hard) | CORE-03: quote not in the source text |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: quote not in the source text |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: quote not in the source text |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 44.25 | Fail (hard) | CORE-03: quote not in the source text; NUM-01: unit 'GBp' is not ISO 4217 |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| continental-ag-o-n | role_disclosure | Former Group Human Relations a | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | total_remuneration | Automotive, Vorstandsmitglied  | 1537000 | Fail (hard) | XF-01: parts add up to 1,590,000, more than the stated 1,537,000; XF-02: parts add up to 1,590,000, stated 1,537,000 |
| continental-ag-o-n | total_remuneration | Tires, Vorstandsmitglied seit  | 1739000 | Fail (hard) | XF-01: parts add up to 1,901,000, more than the stated 1,739,000; XF-02: parts add up to 1,901,000, stated 1,739,000 |
| continental-ag-o-n | total_remuneration | ContiTech, Vorstandsmitglied s | 1467000 | Fail (hard) | XF-01: parts add up to 1,747,000, more than the stated 1,467,000; XF-02: parts add up to 1,747,000, stated 1,467,000 |
| costain-group-plc | base_salary | Chief Financial Officer | 439544 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | benefits_value | Chief Financial Officer | 14945 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | ebitda |  | 47100000 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| costain-group-plc | fte |  | 3049 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | lti_vested | Chief Financial Officer | 1040064 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | pension_contribution | Chief Financial Officer | 43954 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | revenue_by_segment |  | Natural Resources: 440.4; Tran | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | share_price |  | 160 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| costain-group-plc | sti_paid | Chief Financial Officer | 565196 | Fail (hard) | CORE-03: quote not in the source text |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: quote not in the source text |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | sti_max | Chief Financial Officer (since | 264000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | sti_target | Chief Financial Officer (since | 132000 | Fail (hard) | CORE-03: quote not in the source text |
| eurotelesites-ag | benefits |  | company car or a corresponding | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| eurotelesites-ag | revenue_by_country |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: quote not in the source text |
| eurotelesites-ag | revenue_by_segment |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: quote not in the source text |
| eurotelesites-ag | sti_paid | CEO | 132000 | Fail (hard) | CORE-02: 132000 not in the quote |
| eurotelesites-ag | sti_paid | CFO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| eurotelesites-ag | total_remuneration | Management Board | 1224000 | Fail (hard) | XF-01: parts add up to 1,272,000, more than the stated 1,224,000; XF-02: parts add up to 1,272,000, stated 1,224,000 |
| fastighetsbolag-emilshus-pref | aggregate_headcount | Övriga ledande befattningshava | 5 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| fastighetsbolag-emilshus-pref | pension_type |  | VD has a premium-based pension | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| fastighetsbolag-emilshus-pref | role_disclosure | VD | individual | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | role_disclosure | Övriga ledande befattningshava | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| framery-group | base_salary | CEO | 219240 | Fail (hard) | CORE-03: quote not in the source text |
| framery-group | benefits |  | company car, phone and accommo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| framery-group | ebitda |  | 56400000 | Fail (hard) | CORE-02: 56.4 not in the quote; CORE-04: no period_end |
| framery-group | lti_vested | Management team | 3273000 | Fail (hard) | CORE-03: quote not in the source text |
| framery-group | revenue_by_country |  | Eurooppa, Lähi-itä ja Afrikka: | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | revenue_by_segment |  | Äänieristetyt työtilat: 216017 | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | share_price |  | 8.35 | Fail (hard) | CORE-02: 8.35 not in the quote |
| framery-group | staff_by_country |  | Finland: 357; Americas: 21; EM | Fail | CORE-04: no period_end; NUM-08: adds up to 398 vs 484 (17.8% apart) |
| framery-group | sti_paid | CEO | 36000 | Fail (hard) | CORE-03: quote not in the source text |
| framery-group | total_remuneration | CEO | 255240 | Fail (hard) | CORE-03: quote not in the source text |
| framery-group | website |  | framery.com | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| himalaya-shipping | controlling_owner_name |  | Drew Holdings Ltd. | Fail (hard) | CORE-02: not in the quote: ltd |
| himalaya-shipping | ebitda |  | 97400000 | Fail (hard) | NUM-01: unit '$' is not ISO 4217 |
| himalaya-shipping | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| jinhui-shipping | base_salary | Executive Director (Ng Siu Fai | 3846000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | base_salary | Executive Director (Ng Kam Wah | 3077000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | base_salary | Executive Director (Ng Ki Hung | 123000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | base_salary | Executive Director (Ho Suk Lin | 206000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | pay_currency | Executive Director (Ng Siu Fai | US$ | Fail (hard) | CORE-04: no period_end; COD-01: US$ is not ISO 4217 |
| jinhui-shipping | pay_currency | Executive Director (Ng Kam Wah | US$ | Fail (hard) | CORE-04: no period_end; COD-01: US$ is not ISO 4217 |
| jinhui-shipping | pay_currency | Executive Director (Ng Ki Hung | US$ | Fail (hard) | CORE-04: no period_end; COD-01: US$ is not ISO 4217 |
| jinhui-shipping | pay_currency | Executive Director (Ho Suk Lin | US$ | Fail (hard) | CORE-04: no period_end; COD-01: US$ is not ISO 4217 |
| jinhui-shipping | pension_contribution | Executive Director (Ng Siu Fai | 231000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | pension_contribution | Executive Director (Ng Kam Wah | 185000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | pension_contribution | Executive Director (Ng Ki Hung | 7000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | pension_contribution | Executive Director (Ho Suk Lin | 12000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | pension_type |  | defined contribution provident | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jinhui-shipping | sti_paid | Executive Director (Ng Siu Fai | 891000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | sti_paid | Executive Director (Ng Kam Wah | 577000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | sti_paid | Executive Director (Ho Suk Lin | 13000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217 |
| jinhui-shipping | total_remuneration | Executive Director (Ng Siu Fai | 5216000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217; XF-02: parts add up to 4,968,000, stated 5,216,000 |
| jinhui-shipping | total_remuneration | Executive Director (Ng Kam Wah | 4087000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217; XF-02: parts add up to 3,839,000, stated 4,087,000 |
| jinhui-shipping | total_remuneration | Executive Director (Ng Ki Hung | 300000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217; XF-02: parts add up to 130,000, stated 300,000 |
| jinhui-shipping | total_remuneration | Executive Director (Ho Suk Lin | 291000 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'US$' is not ISO 4217; XF-02: parts add up to 231,000, stated 291,000 |
| public-property-invest | largest_holders |  | Samhällsbyggnadsbolaget i Nord | Fail (hard) | CORE-03: quote not in the source text |
| public-property-invest | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| sed-energy | pay_currency | Key management personnel | USD | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | benefits |  | Ansattbetingelser, mobil og bi | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sparebank-1-nordmore | pay_currency | Administrerende direktør | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør økonomi og finans, CF | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør Bedriftsmarked | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør Forretningsutvikling | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør organisasjon og utvik | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør Personmarked | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Direktør Forretningsstøtte | NOK | Fail | CORE-04: no period_end |
| sparebank-1-nordmore | pay_currency | Administrerende direktør SB1NM | NOK | Fail | CORE-04: no period_end |
| ssab-b | headcount |  | 14609 | Fail (hard) | CORE-03: quote not in the source text |
| ssab-b | listing_date |  | 1988 | Fail (hard) | CORE-02: not in the quote: 1988 |
| ssab-b | shareholding_requirement |  | LTI participants must hold sha | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-a | aggregate_headcount | Other members of the Group Lea | 10.25 | Fail (hard) | CORE-04: no period_end; NUM-05: not a whole number |
| stora-enso-a | pay_currency | President and Chief Executive  | EUR | Fail | CORE-04: no period_end |
| stora-enso-a | pay_currency | Other members of the Group Lea | EUR | Fail | CORE-04: no period_end |
| stora-enso-a | pay_currency | Group Leadership Team | EUR | Fail | CORE-04: no period_end |
| stora-enso-a | role_disclosure | Other members of the Group Lea | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| subsea7 | pay_currency | CHIEF EXECUTIVE OFFICER | USD | Fail | CORE-04: no period_end |
| subsea7 | pay_currency | CHIEF FINANCIAL OFFICER | USD | Fail | CORE-04: no period_end |
| subsea7 | pay_currency | Executive Management Team | USD | Fail | CORE-04: no period_end |
| uie | pay_currency | Managing Director | USD | Fail | CORE-04: no period_end |
