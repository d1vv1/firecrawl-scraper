# Output checks: fy2025_runs_datapoints.csv

1272 companies, 53904 filled values checked (2026-11-18, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 49872 (93%) |
| Review | 1247 (2%) |
| Fail | 113 (0%) |
| Fail (hard) | 2672 (5%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 5414 | 5396 | 0 | 0 | 18 |
| Listing and market | 4636 | 4519 | 0 | 0 | 117 |
| Sector | 1595 | 1570 | 0 | 0 | 25 |
| Reporting basis | 4027 | 4009 | 0 | 0 | 18 |
| Financials | 3446 | 3079 | 201 | 1 | 165 |
| Workforce | 1283 | 1061 | 122 | 4 | 96 |
| Ownership and control | 3861 | 3687 | 0 | 0 | 174 |
| Segment and geography | 1473 | 946 | 282 | 73 | 172 |
| Pay policy | 2499 | 2376 | 0 | 0 | 123 |
| Role and disclosure | 7120 | 6875 | 6 | 35 | 204 |
| Pay: fixed | 6565 | 6058 | 62 | 0 | 445 |
| Pay: STI | 4844 | 4354 | 103 | 0 | 387 |
| Pay: LTI | 4364 | 3849 | 71 | 0 | 444 |
| Pay: total | 2747 | 2066 | 400 | 0 | 281 |
| Other | 30 | 27 | 0 | 0 | 3 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 53904 | 53855 | 49 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 24030 | 23268 | 762 | 29874 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 37960 | 36362 | 1598 | 15944 | source not cached; the run itself did not find the quote |
| CORE-04 | Period end present (dated fields only) |  | 31175 | 30525 | 650 | 22729 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 53904 | 53893 | 11 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 18228 | 18101 | 127 | 35676 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 792 | 792 | 0 | 53112 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 1631 | 1631 | 0 | 52273 |  |
| COD-06 | Dates are valid | yes | 1865 | 1824 | 41 | 52039 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 16112 | 16072 | 40 | 37792 | unit 'KCHF' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 14844 | 14844 | 0 | 39060 |  |
| NUM-04 | Magnitude in a plausible range |  | 18503 | 18413 | 90 | 35401 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 1809 | 1800 | 9 | 52095 | not a whole number |
| NUM-06 | Percentages in range | yes | 4192 | 4190 | 2 | 49712 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 684 | 674 | 10 | 53220 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 1461 | 1141 | 320 | 52443 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 2221 | 2221 | 0 | 51683 |  |
| NUM-11 | STI paid not above its maximum |  | 1167 | 1115 | 52 | 52737 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 13420 | 13403 | 17 | 40484 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 536 | 490 | 46 | 53368 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 433 | 433 | 0 | 53471 |  |
| DER-06 | Derived value shows its formula |  | 2285 | 2285 | 0 | 51619 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 2312 | 2163 | 149 | 51592 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 2312 | 1761 | 551 | 51592 | parts add up to N stated N |

## Fill rate

Company fields: 28234 of 52152 filled (54%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 75 | 1272 |
| staff_by_segment | 172 | 1272 |
| staff_by_country | 328 | 1272 |
| market_cap_band | 417 | 1272 |
| share_price | 438 | 1272 |
| revenue_by_country | 454 | 1272 |
| other_names | 458 | 1272 |
| exchange_segment | 509 | 1272 |
| revenue_by_segment | 519 | 1272 |
| controlling_owner_name | 525 | 1272 |
| fte | 538 | 1272 |
| ultimate_parent | 607 | 1272 |
| listing_date | 626 | 1272 |
| shareholding_requirement | 645 | 1272 |
| pe_stake_5pct | 664 | 1272 |
| largest_holders | 684 | 1272 |
| ownership_type | 690 | 1272 |
| controlling_owner | 691 | 1272 |
| ticker | 693 | 1272 |
| ebitda | 725 | 1272 |
| headcount | 745 | 1272 |
| isin | 753 | 1272 |
| shares_outstanding | 754 | 1272 |
| accounting_basis | 760 | 1272 |
| revenue | 762 | 1272 |
| total_assets | 767 | 1272 |
| website | 785 | 1272 |
| sector_code | 792 | 1272 |
| reporting_currency | 802 | 1272 |
| lei | 803 | 1272 |
| sub_sector | 803 | 1272 |
| exchange | 817 | 1272 |
| business_id | 821 | 1272 |
| listing_status | 821 | 1272 |
| legal_name | 824 | 1272 |
| country_code | 824 | 1272 |
| head_office_city | 824 | 1272 |
| benefits | 926 | 1272 |
| pension_type | 928 | 1272 |
| fiscal_year | 1226 | 1272 |
| fiscal_year_end | 1239 | 1272 |

Pay fields, over 3023 executive roles:

| Field | Filled |
|---|---|
| base_salary | 2624 (87%) |
| sti_paid | 2087 (69%) |
| sti_target | 992 (33%) |
| sti_max | 1765 (58%) |
| lti_vested | 1059 (35%) |
| lti_granted | 1159 (38%) |
| lti_target | 831 (27%) |
| lti_max | 1311 (43%) |
| benefits_value | 2057 (68%) |
| pension_contribution | 1884 (62%) |
| total_remuneration | 2742 (91%) |

## Failed values (2785)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 2invest-ag-bf4e0781 | benefits |  | Dienstwagen, Telekommunikation | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | lti_target | Chief Financial Officer (from  | 37.5 | Fail (hard) | CORE-02: 37.5 not in the quote |
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: quote not in the source text |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: quote not in the source text |
| a2a | fte |  | 14762 | Fail (hard) | CORE-02: 14762 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| aalberts-nv | total_remuneration | CFO (up to 10 April 2025) | -16000 | Fail (hard) | NUM-04: -16000 outside 0..5e+10; XF-01: parts add up to -16,000, more than the stated -16,000 |
| ab-inbev | ebitda |  | 21223000000 | Fail (hard) | NUM-01: unit 'US dollar' is not ISO 4217 |
| ab-inbev | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| abb-ltd | sti_paid | Other EC members | 1500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| abb-ltd | sti_target | Other EC members | 1190000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aberdeen-group-plc | benefits_value | Chief Executive Officer | 1000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | lti_granted | Chief Financial Officer (appoi | 282000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | lti_vested | Chief Executive Officer | 497000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | pension_contribution | Chief Executive Officer | 144000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | pension_contribution | Chief Financial Officer (appoi | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | sti_paid | Chief Executive Officer | 1550000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | sti_paid | Chief Financial Officer (appoi | 258000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | total_remuneration | Chief Executive Officer | 2992000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | total_remuneration | Chief Financial Officer (appoi | 802000 | Fail (hard) | CORE-03: quote not in the source text |
| abo-group | revenue |  | 200000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| abo-group | revenue_by_country |  | Belgium: 33579; Netherlands: 1 | Fail | CORE-04: no period_end; NUM-08: adds up to 95,857,000 vs 200,000,000 (52.1% apart) |
| abo-group | revenue_by_segment |  | Geotechnical: 43904; Environme | Fail | CORE-04: no period_end; NUM-08: adds up to 95,857,000 vs 200,000,000 (52.1% apart) |
| abo-group | total_assets |  | 150000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| acceler8-ventures-plc | ebitda |  | -172772 | Fail (hard) | CORE-02: -172772 not in the quote |
| accelleron-industries-ag | revenue_by_country |  | Asia, Middle East & Africa: 54 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| accelleron-industries-ag | staff_by_country |  | Switzerland: 1014; Asia & Midd | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| acciona-s-a | revenue_by_segment |  | Energy: 3547; Infrastructure:  | Fail | CORE-04: no period_end; NUM-08: adds up to 17,758,000,000 vs 20,236,000,000 (12.2% apart) |
| acciona-s-a | total_remuneration | Executive Chairman | 5995000 | Fail (hard) | XF-01: parts add up to 7,940,000, more than the stated 5,995,000; XF-02: parts add up to 7,940,000, stated 5,995,000 |
| acciona-s-a | total_remuneration | Executive Vice-Chairman | 1261000 | Fail (hard) | XF-01: parts add up to 3,051,000, more than the stated 1,261,000; XF-02: parts add up to 3,051,000, stated 1,261,000 |
| acerinox-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| acg-metals-limited | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| acg-metals-limited | total_remuneration | Chairman & Chief Executive Off | 1256156 | Fail (hard) | XF-01: parts add up to 1,497,823, more than the stated 1,256,156; XF-02: parts add up to 1,497,823, stated 1,256,156 |
| ackermans-v-haaren | base_salary | co-CEO (John-Eric Bertrand) | 637500 | Fail (hard) | CORE-03: quote not in the source text |
| ackermans-v-haaren | base_salary | Other members of the Executive | 439836 | Fail (hard) | CORE-03: quote not in the source text |
| ackermans-v-haaren | staff_by_country |  | België: 6725; Rest van Europa: | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 24,930 vs 10,183 (144.8% apart) |
| ackermans-v-haaren | staff_by_segment |  | Marine Engineering & Contracti | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 24,931 vs 10,183 (144.8% apart) |
| addiko-bank-ag-167fa5c3 | total_remuneration | CEO | 899204.92 | Fail (hard) | XF-01: parts add up to 1,132,160, more than the stated 899,205; XF-02: parts add up to 1,132,160, stated 899,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CRO | 649204.82 | Fail (hard) | XF-01: parts add up to 731,888, more than the stated 649,205; XF-02: parts add up to 731,888, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CMO/CIO | 649204.82 | Fail (hard) | XF-01: parts add up to 858,865, more than the stated 649,205; XF-02: parts add up to 858,865, stated 649,205 |
| addiko-bank-ag-167fa5c3 | total_remuneration | CFO | 549204.92 | Fail (hard) | XF-01: parts add up to 694,802, more than the stated 549,205; XF-02: parts add up to 694,802, stated 549,205 |
| addtech-nordic-ab | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | largest_holders |  | Tisenhult Invest 15.8%; Hedeli | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | listing_date |  | 2001-09 | Fail (hard) | COD-06: not a year or a date |
| addtech-nordic-ab | lti_granted | President and CEO | 1954000 | Fail (hard) | CORE-02: 1954 not in the quote |
| addtech-nordic-ab | lti_granted | Other members of Group Managem | 7671450 | Fail (hard) | CORE-02: 7671.45 not in the quote |
| addtech-nordic-ab | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| addtech-nordic-ab | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| adecco-group-ag | lti_granted | Other Executive Committee memb | 8397951 | Fail (hard) | CORE-02: 8397951 not in the quote |
| adecco-group-ag | pension_contribution | Chief Executive Officer | 420415 | Fail (hard) | CORE-02: 420415 not in the quote |
| adecco-group-ag | pension_contribution | Other Executive Committee memb | 1870628 | Fail (hard) | CORE-02: 1870628 not in the quote |
| adecco-group-ag | revenue_by_country |  | France: 4558; Northern Europe: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 17,911,000,000 vs 23,138,000,000 (22.6% apart) |
| adecco-group-ag | revenue_by_segment |  | Adecco: 17908; Akkodis: 3565;  | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| admiral-group-plc | listing_date |  | 2004-09 | Fail (hard) | CORE-02: not in the quote: 2004; CORE-03: the run did not find the full quote (the note keeps only its start); COD-06: not a year or a date |
| admiral-group-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| admiral-group-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| adolfo-dominguez-s-a | shares_outstanding |  | 9249216 | Fail (hard) | CORE-03: quote not in the source text |
| adval-tech-holding-ag | base_salary | Other members of Konzernleitun | 791334 | Fail (hard) | CORE-03: quote not in the source text |
| adval-tech-holding-ag | benefits_value | CEO | 27774 | Fail (hard) | CORE-02: 27774 not in the quote; CORE-03: quote not in the source text |
| adval-tech-holding-ag | benefits_value | Other members of Konzernleitun | 76213 | Fail (hard) | CORE-02: 76213 not in the quote; CORE-03: quote not in the source text |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| aedas-homes-s-a | base_salary | personal directivo | 1896000 | Fail (hard) | CORE-02: 1896 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| aedes | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| aedes | revenue |  | 10600000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aedes | total_assets |  | 318000000 | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| agrana-beteiligungs-ag-60d4466c | revenue_by_segment |  | FBS: 1647834; ACS – Stärke: 98 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aiq-limited | fte |  | 7 | Fail (hard) | CORE-03: quote not in the source text |
| aiq-limited | headcount |  | 7 | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | accounting_basis |  | International Financial Report | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | exchange_segment |  | premium listing segment | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | lti_granted | CEO | 1672000 | Fail (hard) | CORE-02: 1672 not in the quote |
| airtel-africa-plc | lti_granted | CFO | 455000 | Fail (hard) | CORE-02: 455 not in the quote |
| airtel-africa-plc | staff_by_segment |  | Executive management: 174; Man | Fail | CORE-04: no period_end; NUM-08: adds up to 4,132 vs 11,520 (64.1% apart) |
| airtel-africa-plc | sub_sector |  | the provision of telecommunica | Fail (hard) | CORE-03: quote not in the source text |
| airtel-africa-plc | ultimate_parent |  | Bharti Enterprises (Holding) P | Fail (hard) | CORE-03: quote not in the source text |
| ajax | base_salary | financieel directeur | 147000 | Fail (hard) | CORE-02: 147 not in the quote |
| ajax | base_salary | financieel directeur (tot en m | 447000 | Fail (hard) | CORE-02: 447 not in the quote |
| ajax | ebitda |  | -19405000 | Fail (hard) | CORE-02: -19.405 not in the quote |
| aktor-societe-anonyme-holding-company-technical-and-energy-projects | other_names |  | INTRAKAT ΑΝΩΝΥΜΗ ΕΤΑΙΡΕΙΑ ΤΕΧΝ | Fail (hard) | CORE-02: not in the quote: intrakat |
| aktor-societe-anonyme-holding-company-technical-and-energy-projects | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| aktor-societe-anonyme-holding-company-technical-and-energy-projects | ticker |  | ΑΚΤΩΡ | Fail (hard) | CORE-03: quote not in the source text |
| albis-leasing-ag-30344d1d | sti_target | Vorstand | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| alcon-inc | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | lti_max | CEO | 1150 | Fail (hard) | NUM-06: 1150 % of base salary |
| alcon-inc | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alcon-inc | revenue_by_country |  | United States: 4657; Switzerla | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alfa-financial-software-holdings-plc | revenue_by_segment |  | Subscription: 43.6; Software E | Fail (hard) | CORE-03: quote not in the source text |
| alfa-financial-software-holdings-plc | total_remuneration | Executive Chairman | 30000 | Fail (hard) | CORE-03: quote not in the source text |
| alfa-financial-software-holdings-plc | total_remuneration | Chief Executive Officer | 32000 | Fail (hard) | CORE-03: quote not in the source text |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| alkemy-capital-investments-plc | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| allreal-holding-ag | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: market |
| allreal-holding-ag | lti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| allreal-holding-ag | lti_target | Other members of the Group Man | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| almunda-pro-nv | base_salary | Management Board (Remko Hersch | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| almunda-pro-nv | controlling_owner_name |  | Value8 NV | Fail (hard) | CORE-02: not in the quote: nv |
| almunda-pro-nv | ultimate_parent |  | Value8 NV | Fail (hard) | CORE-02: not in the quote: nv |
| alpha-bank-s-a | base_salary | Chief of Growth and Innovation | 55714 | Fail (hard) | CORE-02: 55714 not in the quote |
| alpha-bank-s-a | benefits_value | CEO | 26242 | Fail (hard) | CORE-02: 26242 not in the quote |
| alpha-bank-s-a | fte |  | 6371 | Fail (hard) | CORE-02: 6371 not in the quote |
| alpha-bank-s-a | pension_contribution | Deputy CEO (as of 27.2.2025) | 69866 | Fail (hard) | CORE-02: 69866 not in the quote |
| alpha-bank-s-a | revenue_by_country |  | Greece: 2024; Other countries: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| also-holding-ag | base_salary | Other members of Group Managem | 1959000 | Fail (hard) | CORE-02: 1959 not in the quote |
| also-holding-ag | base_salary | Group Management | 2400000 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | benefits_value | Group Management | 18000 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | controlling_owner_name |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | fte |  | 5156 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | headcount |  | 5157 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | largest_holders |  | Special Distribution Holding G | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | lti_granted | Other members of Group Managem | 3202000 | Fail (hard) | CORE-02: 3202 not in the quote |
| also-holding-ag | lti_granted | Group Management | 4557000 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | pension_contribution | Other members of Group Managem | 170000 | Fail (hard) | CORE-02: 170 not in the quote |
| also-holding-ag | pension_contribution | Group Management | 254000 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | sti_paid | Group Management | 2064000 | Fail (hard) | CORE-03: quote not in the source text |
| also-holding-ag | total_remuneration | Other members of Group Managem | 6874000 | Fail (hard) | CORE-02: 6874 not in the quote |
| also-holding-ag | total_remuneration | Group Management | 9293000 | Fail (hard) | CORE-03: quote not in the source text |
| alter-ego-media-s-a | revenue_by_country |  | Ελλάδα: 131527883; Λοιπές χώρε | Fail (hard) | CORE-03: quote not in the source text |
| alter-ego-media-s-a | revenue_by_segment |  | Ευρυεκπομπής σε τηλεόραση και  | Fail (hard) | CORE-03: quote not in the source text |
| alumil-aluminium-industry-s-a | listing_date |  | May 2007 | Fail (hard) | COD-06: not a year or a date |
| amag-austria-metall-ag-9da856cd | share_price |  | 32 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amag-austria-metall-ag-9da856cd | staff_by_country |  | Austria: 1866; Germany: 249 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | pension_type |  | The Corporation does not opera | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amaroq-ltd | revenue |  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amaroq-ltd | total_assets |  | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amicorp-fs-uk-plc | fte |  | 172 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amigo-resources-plc | total_assets |  | 4000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | base_salary | Executive Chairman | 107000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | ebitda |  | -2885000 | Fail (hard) | CORE-02: -2.885 not in the quote |
| aminex-plc | sti_paid | Executive Chairman | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| aminex-plc | total_remuneration | Executive Chairman | 147000 | Fail (hard) | CORE-03: quote not in the source text |
| amper-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| amper-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| amrest-holdings-se | benefits_value | Executive Chairman | 2000 | Fail (hard) | CORE-02: 2 not in the quote |
| amrize-ltd | lti_max | Chief Executive Officer (23 Ju | 1300 | Fail (hard) | NUM-06: 1300 % of base salary |
| amrize-ltd | shareholding_requirement |  | CEO: shares worth 10 times bas | Fail (hard) | CORE-03: quote not in the source text |
| anima-holding | sti_max | Amministratore Delegato e Dire | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| anima-holding | sti_max | Altri Dirigenti con responsabi | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| antofagasta-plc | headcount |  | 8457 | Fail (hard) | CORE-02: 8457 not in the quote |
| antofagasta-plc | listing_date |  | 1888 | Fail (hard) | CORE-02: not in the quote: 1888; COD-06: not a year or a date |
| antofagasta-plc | lti_target | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| antofagasta-plc | staff_by_country |  | Chile: 6053; United Kingdom: 5 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,062 vs 8,457 (28.3% apart) |
| antofagasta-plc | sti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| ao-world-plc | lti_target | CEO | 125 | Fail (hard) | CORE-02: 125 not in the quote; CORE-03: quote not in the source text |
| ao-world-plc | lti_target | CFO and COO | 125 | Fail (hard) | CORE-02: 125 not in the quote; CORE-03: quote not in the source text |
| ao-world-plc | sti_target | CEO | 62.5 | Fail (hard) | CORE-03: quote not in the source text |
| ao-world-plc | sti_target | CFO and COO | 62.5 | Fail (hard) | CORE-03: quote not in the source text |
| apg-sga-sa | base_salary | Executive Board (excluding CEO | 1385000000 | Fail (hard) | CORE-02: 1385000 not in the quote; NUM-04: 1.385e+09 outside 0..1e+09 |
| apg-sga-sa | benefits_value | Executive Board (excluding CEO | 437000000 | Fail (hard) | CORE-02: 437000 not in the quote |
| apg-sga-sa | lti_granted | Executive Board (excluding CEO | 288000000 | Fail (hard) | CORE-02: 288000 not in the quote |
| apg-sga-sa | sti_paid | Executive Board (excluding CEO | 280000000 | Fail (hard) | CORE-02: 280000 not in the quote |
| apg-sga-sa | total_remuneration | Executive Board (excluding CEO | 2390000000 | Fail (hard) | CORE-02: 2390000 not in the quote |
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
| aryzta-ag | benefits_value | Group Chief Executive Officer  | 193000 | Fail (hard) | CORE-02: 193 not in the quote |
| aryzta-ag | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ebitda |  | 306900000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | revenue_by_country |  | Switzerland: 280.9; Germany: 6 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aryzta-ag | revenue_by_segment |  | ARYZTA Europe: 1977; ARYZTA Re | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aryzta-ag | role_disclosure | Other Executive Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| aryzta-ag | total_remuneration | Group Chief Executive Officer  | 1714000 | Fail (hard) | CORE-03: quote not in the source text |
| aryzta-ag | total_remuneration | Other Executive Management | 3601000 | Fail (hard) | CORE-02: 3601 not in the quote; CORE-03: quote not in the source text |
| asa-international-group-plc | listing_date |  | 2018 | Fail (hard) | CORE-02: not in the quote: 2018 |
| asa-international-group-plc | lti_vested | Deputy Chairperson and Special | 60 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| ascencio | aggregate_headcount | Other members of the executive | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aseana-properties-limited | revenue_by_country |  | Malaysia: 14415 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ashmore-group-plc | listing_date |  | 2006 | Fail (hard) | CORE-02: not in the quote: 2006 |
| ashtead-technology-holdings-plc | fte |  | 649 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 649 above headcount 396 |
| asia-strategic-holdings-limited | revenue_by_segment |  | Education: 24970269; Services: | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | base_salary | Member of the Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | lti_granted | Member of the Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | pension_contribution | Member of the Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | sti_paid | Member of the Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asmallworld-ag | total_remuneration | Member of the Board | 0 | Fail (hard) | CORE-03: quote not in the source text |
| asos-plc | benefits |  | flexible benefits allowance of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | listing_date |  | 2022-02 | Fail (hard) | COD-06: not a year or a date |
| asos-plc | lti_granted | CFO (appointed 1 July 2025) | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| asos-plc | pension_type |  | defined contribution, 5% of ba | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| assicurazioni-generali | revenue |  | 84690000000 | Fail (hard) | CORE-03: quote not in the source text |
| assicurazioni-generali | revenue_by_segment |  | PROPERTY & CASUALTY (P&C): 361 | Fail | CORE-04: no period_end; NUM-08: adds up to 36,181,000,000 vs 84,690,000,000 (57.3% apart) |
| associated-british-foods-plc | largest_holders |  | Wittington Investments Limited | Fail (hard) | NUM-07: holdings add up to 121.6% |
| associated-british-foods-plc | lti_target | Chief Executive | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| associated-british-foods-plc | lti_target | Finance Director | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| associated-british-foods-plc | sti_target | Chief Executive | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| associated-british-foods-plc | sti_target | Finance Director | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| aston-martin-lagonda-global-holdings-plc | lti_granted | Chief Executive Officer | 2250000 | Fail (hard) | CORE-02: 2250 not in the quote |
| aston-martin-lagonda-global-holdings-plc | lti_granted | Chief Financial Officer | 1200000 | Fail (hard) | CORE-02: 1200 not in the quote |
| aston-martin-lagonda-global-holdings-plc | lti_target | Chief Executive Officer | 175 | Fail (hard) | CORE-02: 175 not in the quote |
| aston-martin-lagonda-global-holdings-plc | lti_target | Chief Financial Officer | 145.8 | Fail (hard) | CORE-02: 145.8 not in the quote |
| aston-martin-lagonda-global-holdings-plc | sti_target | Chief Executive Officer | 125 | Fail (hard) | CORE-02: 125 not in the quote |
| aston-martin-lagonda-global-holdings-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| astrazeneca-plc | revenue_by_country |  | US: 25450; Emerging Markets: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 65,393,000,000 vs 58,739,000,000 (11.3% apart) |
| atalaya-mining-copper-s-a | listing_date |  | May 2005 | Fail (hard) | COD-06: not a year or a date |
| atalaya-mining-copper-s-a | staff_by_country |  | Spain: 514; Cyprus: 3; United  | Fail (hard) | CORE-03: quote not in the source text |
| atalaya-mining-copper-s-a | total_remuneration | Chief Executive Officer | 1838459 | Fail (hard) | CORE-03: quote not in the source text |
| aterian-plc | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| athens-international-airport-s-a | base_salary | Managing Director (CEO), Execu | 900000 | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | benefits_value | Managing Director (CEO), Execu | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | lti_granted | Managing Director (CEO), Execu | 269000 | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | sti_paid | Managing Director (CEO), Execu | 450000 | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | sub_sector |  | To carry out any and/or all th | Fail (hard) | CORE-03: quote not in the source text |
| athens-international-airport-s-a | total_remuneration | Managing Director (CEO), Execu | 1719000 | Fail (hard) | CORE-03: quote not in the source text |
| athens-medical-c-s-a | listing_date |  | 1991 | Fail (hard) | CORE-02: not in the quote: 1991 |
| atlas-metals-group-plc | benefits |  | medical contributions, reimbur | Fail (hard) | CORE-03: quote not in the source text |
| atlas-metals-group-plc | shares_outstanding |  | 72439612 | Fail (hard) | CORE-03: quote not in the source text |
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
| attica-holdings-s-a | listing_date |  | 1924 | Fail (hard) | CORE-02: not in the quote: 1924 |
| attica-holdings-s-a | sti_max | Πρόεδρος / Εκτελεστικό μέλος ( | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| attica-holdings-s-a | sti_max | Διευθύνων Σύμβουλος & Αναπληρω | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| attica-holdings-s-a | sti_max | Αναπληρωτής Διευθύνων Σύμβουλο | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| attica-holdings-s-a | sti_max | Μέλος Δ.Σ. Θυγατρικών Εταιριών | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| attica-holdings-s-a | sti_max | Μέλος Δ.Σ. Θυγατρικών Εταιριών | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| attica-holdings-s-a | sti_max | Μέλος Δ.Σ. Θυγατρικών Εταιριών | 8 | Fail (hard) | COD-01: unit '' is not a target form |
| aurskog-sparebank | revenue_by_segment |  | Personmarked: 393456; Bedrifts | Fail (hard) | CORE-03: quote not in the source text |
| aurskog-sparebank | sti_max | Administrerende banksjef | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | CFO/banksjef | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | Leder bankdrift | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | Leder sparing og investering | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | Kommunikasjons- og markedssjef | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | Leder personmarked | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sti_max | Leder bedriftsmarked | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| aurskog-sparebank | sub_sector |  | Aurskog Sparebank skal være en | Fail (hard) | CORE-03: quote not in the source text |
| austriacard-holdings-ag | benefits_value | Executive Vice President Türki | 13810 | Fail (hard) | CORE-02: 13810 not in the quote |
| austriacard-holdings-ag | lti_max | Executive Vice President Türki | 10 | Fail (hard) | COD-01: unit '' is not a target form |
| austriacard-holdings-ag | lti_target | Executive Vice President Türki | 1 | Fail (hard) | CORE-02: 1 not in the quote; COD-01: unit '' is not a target form |
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
| autostrade-meridionali | benefits |  | Erogazione di beni e/o servizi | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| autostrade-meridionali | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-04: 0 outside 1..5e+06 |
| avax-s-a | role_disclosure | Executive Members of the Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| avax-s-a | staff_by_segment |  | AVAX: 1985; ETETH: 98; iXion:  | Fail | CORE-04: no period_end; NUM-08: adds up to 3,307 vs 2,803 (18.0% apart) |
| avax-s-a | sti_paid | Executive Members of the Board | 1500000 | Fail (hard) | CORE-03: quote not in the source text |
| avax-s-a | total_remuneration | Chairman / Executive Director | 515000 | Fail (hard) | XF-01: parts add up to 527,622, more than the stated 515,000; XF-02: parts add up to 527,622, stated 515,000 |
| avax-s-a | total_remuneration | Alternate Chairman / Executive | 465000 | Fail (hard) | XF-01: parts add up to 481,872, more than the stated 465,000; XF-02: parts add up to 481,872, stated 465,000 |
| avax-s-a | total_remuneration | Managing Director | 1430000 | Fail (hard) | XF-01: parts add up to 1,478,494, more than the stated 1,430,000; XF-02: parts add up to 1,478,494, stated 1,430,000 |
| avax-s-a | total_remuneration | Executive Director (Anthony Mi | 490000 | Fail (hard) | XF-01: parts add up to 523,967, more than the stated 490,000; XF-02: parts add up to 523,967, stated 490,000 |
| avax-s-a | total_remuneration | Executive Director (Athena Eli | 718854 | Fail (hard) | XF-01: parts add up to 741,502, more than the stated 718,854; XF-02: parts add up to 741,502, stated 718,854 |
| aviva-plc | headcount |  | 36160 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: quote on page 207, link says page 206 |
| avolta-ag | sti_max | Chief Executive Officer (CEO) | 199.995 | Fail (hard) | CORE-03: quote not in the source text |
| avon-technologies-plc | fte |  | 911 | Fail (hard) | CORE-03: quote not in the source text |
| avon-technologies-plc | total_assets |  | 314800000 | Fail (hard) | CORE-03: quote not in the source text |
| azelis-group | lti_granted | Other members of the Executive | 1118033 | Fail (hard) | CORE-02: 1118033 not in the quote; CORE-03: quote not in the source text |
| azkoyen | base_salary | CEO (until January 2024) | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| azkoyen | base_salary | Executive Chairman (from May 2 | 138000 | Fail (hard) | CORE-03: quote not in the source text |
| azkoyen | pay_currency | CEO (until January 2024) | EUR | Fail | CORE-04: no period_end |
| azkoyen | pay_currency | Executive Chairman (from May 2 | EUR | Fail | CORE-04: no period_end |
| azkoyen | revenue_by_country |  | Alemania: 65563; España: 38179 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| azkoyen | staff_by_country |  | España: 410; Alemania: 302; Bé | Fail | CORE-04: no period_end; NUM-08: adds up to 1,025 vs 1,086 (5.6% apart) |
| azkoyen | sti_paid | CEO (until January 2024) | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| azkoyen | ultimate_parent |  | INVERLASA, S.L. | Fail (hard) | CORE-03: quote not in the source text |
| b-c-speakers | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| b-c-speakers | staff_by_country |  | Italy: 242; United States: 65; | Fail | CORE-04: no period_end; NUM-08: adds up to 361 vs 383 (5.7% apart) |
| b-f | lti_vested | Presidente del Consiglio di Am | 273486 | Fail (hard) | CORE-02: 273486 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | shareholding_requirement |  | CEO is allocated 375 shares an | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bachem-holding-ag | sti_paid | CEO | 247000 | Fail (hard) | CORE-03: quote not in the source text |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-03: quote not in the source text |
| bachem-holding-ag | total_remuneration | CEO | 800000 | Fail (hard) | XF-01: parts add up to 874,000, more than the stated 800,000; XF-02: parts add up to 874,000, stated 800,000 |
| bachem-holding-ag | total_remuneration | Rest of the Corporate Executiv | 1933000 | Fail (hard) | XF-01: parts add up to 2,090,000, more than the stated 1,933,000; XF-02: parts add up to 2,090,000, stated 1,933,000 |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bajaj-mobility-ag-8e6bef55 | ebitda |  | 874000000 | Fail (hard) | CORE-03: quote not in the source text |
| bakkafrost | ebitda |  | 1672664000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| balfour-beatty-plc | pension_contribution | Outgoing Group Chief Executive | 43183 | Fail (hard) | CORE-03: quote not in the source text |
| balfour-beatty-plc | revenue_by_country |  | United Kingdom: 4778; United S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | revenue_by_segment |  | Construction Services: 8711; S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | total_remuneration | Group Chief Executive (appoint | 2938735 | Fail (hard) | XF-01: parts add up to 3,217,745, more than the stated 2,938,735; XF-02: parts add up to 3,217,745, stated 2,938,735 |
| bam-groep-kon | lti_target | CEO | 150 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | lti_target | CFO | 100 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | lti_target | Member of the Executive Board | 100 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_max | CEO | 150 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_max | CFO | 112.5 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_max | Member of the Executive Board | 112.5 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_target | CEO | 100 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_target | CFO | 75 | Fail (hard) | CORE-03: quote not in the source text |
| bam-groep-kon | sti_target | Member of the Executive Board | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banca-mediolanum | revenue_by_country |  | Italia: 2978604; Spagna: 35928 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 5,064,671,000 vs 2,500,000,000 (102.6% apart) |
| banca-profilo | base_salary | Consiglio di amministrazione | 1215000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | base_salary | Dirigenti con Responsabilità S | 3069000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | benefits_value | Consiglio di amministrazione | 25000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | lti_granted | Consiglio di amministrazione | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | revenue_by_segment |  | Private Banking: 25676; Invest | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | share_price |  | 0.166 | Fail (hard) | CORE-02: 0.166 not in the quote |
| banca-profilo | sti_paid | Consiglio di amministrazione | 525000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | sti_paid | Dirigenti con Responsabilità S | 745000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | total_remuneration | Consiglio di amministrazione | 1862000 | Fail (hard) | CORE-03: quote not in the source text |
| banca-profilo | total_remuneration | Dirigenti con Responsabilità S | 4049000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 3,814,000, stated 4,049,000 |
| banca-sistema | staff_by_country |  | Italy: 319; Greece: 3; Portuga | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| banijay-group | lti_target | Senior Management Members | 3.3 | Fail (hard) | COD-01: unit '' is not a target form |
| banijay-group | staff_by_segment |  | BGNV: 9; Banijay Entertainment | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | lti_max | Executive Vice-chairman | 120 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | lti_max | Chief Executive Officer | 120 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | pension_type |  | complementary pension scheme t | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | revenue_by_country |  | Spain: 2563; Portugal: 366.7;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | sti_max | Executive Vice-chairman | 42 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | sti_max | Chief Executive Officer | 42 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bankinter-s-a | total_remuneration | Chief Executive Officer | 1336000 | Fail (hard) | XF-01: parts add up to 1,529,000, more than the stated 1,336,000; XF-02: parts add up to 1,529,000, stated 1,336,000 |
| barclays-plc | total_remuneration | Group Chief Executive | 15045000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 4,588,000, stated 15,045,000 |
| barclays-plc | total_remuneration | Group Finance Director | 8970000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 2,770,000, stated 8,970,000 |
| barco | lti_granted | CEO | 2528269 | Fail (hard) | CORE-02: 2528269 not in the quote |
| barco | lti_granted | Core Leadership Team | 3026313 | Fail (hard) | CORE-02: 3026313 not in the quote; CORE-03: quote not in the source text |
| barco | lti_target | CEO | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| barco | lti_vested | Core Leadership Team | 2726349 | Fail (hard) | CORE-02: 2726349 not in the quote; CORE-03: quote not in the source text |
| barco | sti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| barco | sti_max | Core Leadership Team | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| barco | sti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| barco | sti_target | Core Leadership Team | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| barr-a-g-plc | benefits_value | Chief Executive Officer | 32000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | benefits_value | Chief Finance and Operating Of | 16000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | lti_vested | Chief Finance and Operating Of | 678000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | pension_contribution | Chief Executive Officer | 47000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | pension_contribution | Chief Finance and Operating Of | 38000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | sti_paid | Chief Executive Officer | 476000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | sti_paid | Chief Finance and Operating Of | 299000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | total_remuneration | Chief Executive Officer | 1221000 | Fail (hard) | CORE-03: quote not in the source text |
| barr-a-g-plc | total_remuneration | Chief Finance and Operating Of | 1451000 | Fail (hard) | CORE-03: quote not in the source text |
| barry-callebaut-ag | base_salary | Other Executive Committee memb | 2853752 | Fail (hard) | CORE-02: 2853752 not in the quote |
| barry-callebaut-ag | benefits_value | Other Executive Committee memb | 406099 | Fail (hard) | CORE-02: 406099 not in the quote |
| barry-callebaut-ag | lti_granted | Other Executive Committee memb | 3789152 | Fail (hard) | CORE-02: 3789152 not in the quote |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: quote not in the source text |
| barry-callebaut-ag | sti_paid | Other Executive Committee memb | 2967901 | Fail (hard) | CORE-02: 2967901 not in the quote |
| basellandschaftliche-kantonalbank | base_salary | CEO (until 31.7.2025) | 650000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | headcount |  | 1054 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Executive | 605000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must hold a mi | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | staff_by_country |  | Canton of Basel-Landschaft: 92 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | sti_paid | CEO (until 31.7.2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | sti_paid | Other members of the Executive | 605000 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Executive | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basicnet | revenue_by_segment |  | Clothing, footwear and accesso | Fail | CORE-04: no period_end; NUM-08: adds up to 414,700,000 vs 348,282,000 (19.1% apart) |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other management committee mem | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote |
| basilea-pharmaceutica-ag-allschwil | benefits_value | Other management committee mem | 475160 | Fail (hard) | CORE-02: 475160 not in the quote |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other management committee mem | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote |
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
| baywa-ag-na-o-n | base_salary | Chief Restructuring Officer (f | 150000 | Fail (hard) | CORE-02: 150 not in the quote |
| baywa-ag-na-o-n | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ebitda |  | -162500000 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | largest_holders |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_max | Chief Executive Officer (until | 950000 | Fail (hard) | CORE-02: 950000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_max | Chief Financial Officer | 475000 | Fail (hard) | CORE-02: 475000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_max | Member of the Board of Managem | 475000 | Fail (hard) | CORE-02: 475000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_target | Chief Executive Officer (until | 700000 | Fail (hard) | CORE-02: 700000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_target | Chief Financial Officer | 350000 | Fail (hard) | CORE-02: 350000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | lti_target | Member of the Board of Managem | 350000 | Fail (hard) | CORE-02: 350000 not in the quote; CORE-03: quote not in the source text |
| baywa-ag-na-o-n | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-03: quote not in the source text |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| be-semiconductor | sti_max | Chief Executive Officer, Chair | 500 | Fail (hard) | CORE-02: 500 not in the quote |
| be-semiconductor | total_remuneration | Chief Executive Officer, Chair | 9925053 | Fail (hard) | XF-01: parts add up to 10,213,053, more than the stated 9,925,053; XF-02: parts add up to 10,213,053, stated 9,925,053 |
| beiersdorf-ag-o-n | lti_max | Vorstandsvorsitzender | 8640000 | Fail (hard) | CORE-02: 8640000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Oswald | 4750000 | Fail (hard) | CORE-02: 4750000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CFO | 3850000 | Fail (hard) | CORE-02: 3850000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands/CHRO | 2550000 | Fail (hard) | CORE-02: 2550000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Grita  | 4766000 | Fail (hard) | CORE-02: 4766000 not in the quote |
| beiersdorf-ag-o-n | lti_max | Mitglied des Vorstands (Ramon  | 3975000 | Fail (hard) | CORE-02: 3975000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Oswald | 2500000 | Fail (hard) | CORE-02: 2500000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Grita  | 2383000 | Fail (hard) | CORE-02: 2383000 not in the quote |
| beiersdorf-ag-o-n | lti_target | Mitglied des Vorstands (Ramon  | 2050000 | Fail (hard) | CORE-02: 2050000 not in the quote |
| bekaert | benefits |  | company car, risk insurances,  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bekaert | benefits_value | Chief Executive Officer | 86264 | Fail (hard) | CORE-02: 86264 not in the quote |
| bekaert | benefits_value | Other members of the Executive | 393967 | Fail (hard) | CORE-02: 393967 not in the quote |
| bekaert | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| berner-kantonalbank-ag | benefits |  | No specific benefits mentioned | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| berner-kantonalbank-ag | pension_type |  | Defined contribution. For the  | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | revenue |  | 460000000 | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bertrandt-ag-o-n | ebitda |  | -98046000 | Fail (hard) | CORE-02: -98.046 not in the quote |
| bertrandt-ag-o-n | fte |  | 13824 | Fail (hard) | CORE-02: 13824 not in the quote |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | lti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Finanze | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Vertrie | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | pay_currency | Mitglied des Vorstands Technik | EUR | Fail | CORE-04: no period_end |
| bertrandt-ag-o-n | revenue |  | 1186884000 | Fail (hard) | CORE-02: 1186.884 not in the quote |
| bertrandt-ag-o-n | staff_by_country |  | Romania: 1000 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,000 vs 14,028 (92.9% apart) |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Finanze | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Vertrie | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | sti_max | Mitglied des Vorstands Technik | 6 | Fail (hard) | CORE-02: 6 not in the quote; CORE-04: no period_end |
| bertrandt-ag-o-n | total_assets |  | 879538000 | Fail (hard) | CORE-02: 879.538 not in the quote |
| besqab-pref-b | controlling_owner_name |  | Family Nordström | Fail (hard) | CORE-02: not in the quote: family |
| bestbe-holding | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| bestbe-holding | share_price |  | 0.06 | Fail (hard) | CORE-02: 0.06 not in the quote |
| biesse | benefits |  | Mixed-use company cars, Accide | Fail (hard) | CORE-03: quote not in the source text |
| big-yellow-group-plc | fte |  | 453 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| big-yellow-group-plc | listing_date |  | May 2000 | Fail (hard) | COD-06: not a year or a date |
| big-yellow-group-plc | share_price |  | 967.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bilfinger-se-o-n | total_remuneration | member of the Executive Board, | 1541000 | Fail (hard) | XF-01: parts add up to 1,771,000, more than the stated 1,541,000; XF-02: parts add up to 1,771,000, stated 1,541,000 |
| biofrontera-ag-na-o-n | lti_target | CFO | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | role_disclosure | CFO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biofrontera-ag-na-o-n | shareholding_requirement |  | Vorstandsmitglieder sind zu ei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| biokarpet-s-a | benefits |  | medical/hospital care programs | Fail (hard) | CORE-03: quote not in the source text |
| biokarpet-s-a | pension_type |  | defined benefit (for retiremen | Fail (hard) | CORE-03: quote not in the source text |
| biosenic | aggregate_headcount | Other Members of the Executive | 4 | Fail (hard) | CORE-03: quote not in the source text |
| biosenic | headcount |  | 11 | Fail (hard) | CORE-02: 11 not in the quote |
| biotalys | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biotalys | role_disclosure | Chief Financial Officer (from  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| biotalys | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bioversys-ag | base_salary | CEO | 1224000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | lti_granted | CEO | 960000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | pension_contribution | CEO | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | pension_type |  | The basic Swiss pension plan q | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | sti_paid | CEO | 232000 | Fail (hard) | CORE-03: quote not in the source text |
| bioversys-ag | total_remuneration | CEO | 2676000 | Fail (hard) | CORE-03: quote not in the source text |
| bks-bank-ag-5e8b8669 | revenue_by_segment |  | Privatkunden: 111406; Firmenku | Fail | CORE-04: no period_end; NUM-08: adds up to 388,487,000 vs 303,636,676 (27.9% apart) |
| bkw-ag | base_salary | Other members of the Group Exe | 3791000 | Fail (hard) | CORE-02: 3791 not in the quote; CORE-03: quote not in the source text |
| bkw-ag | lti_granted | Other members of the Group Exe | 1127000 | Fail (hard) | CORE-02: 1127 not in the quote; CORE-03: quote not in the source text |
| bkw-ag | pension_contribution | Other members of the Group Exe | 1047000 | Fail (hard) | CORE-02: 1047 not in the quote; CORE-03: quote not in the source text |
| bkw-ag | role_disclosure | Other members of the Group Exe | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_max | CEO | 60 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_max | Other members of the Group Exe | 60 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_paid | Other members of the Group Exe | 1343000 | Fail (hard) | CORE-02: 1343 not in the quote; CORE-03: quote not in the source text |
| bkw-ag | total_remuneration | Other members of the Group Exe | 7308000 | Fail (hard) | CORE-02: 7308 not in the quote; CORE-03: quote not in the source text |
| ble-kedros-reic | accounting_basis |  | Διεθνή Πρότυπα Χρηματοοικονομι | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ble-kedros-reic | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| blencowe-resources-plc | ebitda |  | -1536243 | Fail (hard) | CORE-02: -1536243 not in the quote |
| bodycote-plc | benefits_value | Chief Executive Officer | 19000 | Fail (hard) | CORE-02: 19 not in the quote |
| bodycote-plc | benefits_value | Chief Financial Officer | 16000 | Fail (hard) | CORE-02: 16 not in the quote |
| borgosesia | revenue_by_segment |  | Real Estate: 16427; Alternativ | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| borgosesia | share_price |  | 0.576 | Fail (hard) | CORE-02: 0.576 not in the quote |
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
| bque-nat-belgique | controlling_owner_name |  | Belgian State | Fail (hard) | CORE-02: not in the quote: belgian state |
| bque-nat-belgique | website |  | nbb.be | Fail (hard) | CORE-03: quote not in the source text |
| braemar-plc | base_salary | Former Group Chief Operating O | 7200 | Fail (hard) | CORE-02: 7.2 not in the quote |
| braemar-plc | pension_contribution | Group Chief Financial and Oper | 23100 | Fail (hard) | CORE-03: quote not in the source text |
| braemar-plc | revenue_by_segment |  | Chartering: 74713; Investment  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| braemar-plc | sti_paid | Group Chief Financial and Oper | 400000 | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | revenue |  | 100000000 | Fail (hard) | CORE-03: quote not in the source text |
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-03: quote on page 14, link says page 13 |
| breedon-group-plc | base_salary | Chief Executive Officer | 692000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | base_salary | Chief Financial Officer | 477000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | benefits_value | Chief Executive Officer | 21000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | benefits_value | Chief Financial Officer | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | lti_vested | Chief Executive Officer | 186000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | lti_vested | Chief Financial Officer | 126000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | pension_contribution | Chief Executive Officer | 30000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | pension_contribution | Chief Financial Officer | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | sti_paid | Chief Financial Officer | 250000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | total_remuneration | Chief Executive Officer | 1289000 | Fail (hard) | CORE-03: quote not in the source text |
| breedon-group-plc | total_remuneration | Chief Financial Officer | 893000 | Fail (hard) | CORE-03: quote not in the source text |
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
| burgenland-holding-ag-a95d1abc | largest_holders |  | VERBUND AG 10%; WIEN ENERGIE G | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burgenland-holding-ag-a95d1abc | share_price |  | 71.5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| burgenland-holding-ag-a95d1abc | total_remuneration | Mitglied des Vorstands (Dr. Kl | 5500 | Fail (hard) | XF-01: parts add up to 5,650, more than the stated 5,500; XF-02: parts add up to 5,650, stated 5,500 |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| burkhalter-holding-ag | sti_max | Verwaltungsrat | 60 | Fail (hard) | COD-01: unit '' is not a target form |
| burkhalter-holding-ag | sti_max | CEO | 60 | Fail (hard) | COD-01: unit '' is not a target form |
| burkhalter-holding-ag | sti_max | CFO | 60 | Fail (hard) | COD-01: unit '' is not a target form |
| buzzi | staff_by_segment |  | Italia: 1560; Germania, Lussem | Fail | CORE-04: no period_end; NUM-08: adds up to 9,620 vs 10,532 (8.7% apart) |
| bvz-holding-ag | revenue_by_segment |  | Gornergrat: 47.1; Immobilien:  | Fail (hard) | CORE-03: quote on page 5, link says page 4; NUM-08: adds up to 181,900,000 vs 216,170,312 (15.9% apart) |
| bystronic-ag | aggregate_headcount | Other members of the Executive | 3.1 | Fail (hard) | NUM-05: not a whole number |
| bystronic-ag | base_salary | Other members of the Executive | 803600 | Fail (hard) | CORE-02: 803.6 not in the quote |
| bystronic-ag | benefits_value | Other members of the Executive | 134100 | Fail (hard) | CORE-02: 134.1 not in the quote |
| bystronic-ag | lti_granted | Other members of the Executive | 110900 | Fail (hard) | CORE-02: 110.9 not in the quote |
| bystronic-ag | lti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | lti_target | Other members of the Executive | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | pension_contribution | Other members of the Executive | 153300 | Fail (hard) | CORE-02: 153.3 not in the quote |
| bystronic-ag | sti_paid | Other members of the Executive | 288000 | Fail (hard) | CORE-02: 288 not in the quote |
| bystronic-ag | sti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | Other members of the Executive | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | total_remuneration | Other members of the Executive | 1489900 | Fail (hard) | CORE-02: 1489.9 not in the quote |
| bytes-technology-group-plc | ebitda |  | 62732000 | Fail (hard) | CORE-02: 62732 not in the quote |
| c-c-group-plc | lti_granted | Chief Financial and Transforma | 404411 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| ca-immobilien-anlagen-ag-a9ff4a4a | staff_by_segment |  | Austria: 80; Germany/Switzerla | Fail | CORE-04: no period_end; NUM-08: adds up to 348 vs 254 (37.0% apart) |
| cab-payments-holdings-plc | revenue |  | 109400000 | Fail (hard) | CORE-03: quote not in the source text |
| cab-payments-holdings-plc | total_assets |  | 188000000 | Fail (hard) | CORE-03: quote not in the source text |
| cabka | benefits_value | Chief Executive Officer | 42000 | Fail (hard) | CORE-03: quote not in the source text |
| cabka | benefits_value | Chief Financial Officer | 6000 | Fail (hard) | CORE-03: quote not in the source text |
| cabka | benefits_value | Former CFO (until September 20 | 61000 | Fail (hard) | CORE-03: quote not in the source text |
| cabka | sti_target | Chief Executive Officer | 15 | Fail (hard) | COD-01: unit '' is not a target form |
| cabka | sti_target | Chief Financial Officer | 15 | Fail (hard) | COD-01: unit '' is not a target form |
| cabka | sti_target | Former CFO (until September 20 | 15 | Fail (hard) | COD-01: unit '' is not a target form |
| cadogan-energy-solutions-plc | lti_max | Executive Director | 200 | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | pension_type |  | defined contribution, not exce | Fail (hard) | CORE-03: quote not in the source text |
| cadogan-energy-solutions-plc | share_price |  | 0.04 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| caffyns-plc | headcount |  | 485 | Fail (hard) | CORE-02: 485 not in the quote |
| cairo-communication | controlling_owner_name |  | Urbano Roberto Cairo | Fail (hard) | CORE-02: not in the quote: roberto |
| caledonia-investments-plc | benefits_value | Executive Director | 31000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | headcount |  | 82 | Fail (hard) | CORE-02: 82 not in the quote |
| caledonia-investments-plc | lti_vested | Executive Director | 409000 | Fail (hard) | CORE-03: quote not in the source text |
| caledonia-investments-plc | revenue_by_segment |  | Public Companies: 21.8; Privat | Fail | CORE-04: no period_end; NUM-08: adds up to 43,700,000 vs 166,000,000 (73.7% apart) |
| caledonia-investments-plc | sti_paid | Executive Director | 259000 | Fail (hard) | CORE-03: quote not in the source text |
| caltagirone | base_salary | Consigliere (Sarah Moscatelli) | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| caltagirone | base_salary | Consigliere (Filomena Passeggi | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| caltagirone | benefits_value | Consigliere (Elena De Simone) | 39500 | Fail (hard) | CORE-02: 39500 not in the quote |
| caltagirone | largest_holders |  | Francesco Gaetano Caltagirone  | Fail (hard) | NUM-07: holdings add up to 122.622% |
| caltagirone | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| caltagirone-editore | fiscal_year_end |  | 2023-12-31 | Fail (hard) | CORE-03: quote not in the source text |
| canal-s-a | controlling_owner_name |  | Bolloré SE | Fail (hard) | CORE-02: not in the quote: se |
| cancom-se-o-n | lti_granted | Vorstand | 355640 | Fail (hard) | CORE-02: 355.64 not in the quote; CORE-03: quote not in the source text |
| capita-plc | share_price |  | 4.055 | Fail (hard) | CORE-02: 4.055 not in the quote |
| capita-plc | shares_outstanding |  | 120030667 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | base_salary | Executive Chair | 528000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | CEO (until March 2025) | 442000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | Executive Director | 417000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_max | Executive Chair | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| capital-limited | lti_max | CEO (until March 2025) | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| capital-limited | lti_max | Executive Director | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| capital-limited | lti_vested | CEO (until March 2025) | 73000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | lti_vested | Executive Director | 49000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Chair | 722000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | sti_paid | Executive Director | 546000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | Executive Chair | 1345000 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | total_remuneration | CEO (until March 2025) | 515000 | Fail (hard) | CORE-03: quote not in the source text |
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
| carclo-plc | lti_granted | Chief Financial Officer | 472500 | Fail (hard) | CORE-02: 472500 not in the quote |
| carclo-plc | staff_by_country |  | United Kingdom: 318; North Ame | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | benefits_value | Chief Executive Officer | 23000 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | benefits_value | Chief Financial Officer | 7000 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | lti_granted | Chief Executive Officer | 429975 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | lti_granted | Chief Financial Officer | 274482 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | lti_vested | Chief Executive Officer | 396214 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | lti_vested | Chief Financial Officer | 247970 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | pension_contribution | Chief Executive Officer | 13313 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | pension_contribution | Chief Financial Officer | 10756 | Fail (hard) | CORE-03: quote not in the source text |
| card-factory-plc | total_remuneration | Chief Financial Officer | 631840 | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cellularline | lti_granted | Vicepresidente e Amministrator | 9720 | Fail (hard) | CORE-02: 9720 not in the quote |
| cellularline | lti_granted | Amministratore Esecutivo | 29495 | Fail (hard) | CORE-02: 29495 not in the quote |
| cellularline | revenue_by_country |  | Italia: 77.2; International: 8 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| cellularline | revenue_by_segment |  | Red: 135.2; Black: 8.4; Blue:  | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| celyad-oncology | base_salary | CEO (until September 2024) | 80612 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | base_salary | CEO | 101830 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | base_salary | Comité Exécutif (hors CEO) | 732428 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | benefits_value | CEO | 6294 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | benefits_value | Comité Exécutif (hors CEO) | 9392 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | lti_granted | CEO | 279643 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | lti_granted | Comité Exécutif (hors CEO) | 181000 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | pension_contribution | Comité Exécutif (hors CEO) | 175509 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | role_disclosure | CEO (until September 2024) | individual | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | sti_paid | Comité Exécutif (hors CEO) | 42416 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | total_remuneration | CEO (until September 2024) | 80612 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | total_remuneration | CEO | 179740 | Fail (hard) | CORE-03: quote not in the source text |
| celyad-oncology | total_remuneration | Comité Exécutif (hors CEO) | 977035 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | base_salary | Chief Executive Officer | 630000 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | base_salary | Other Management Board Members | 2350585 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | benefits_value | Chief Executive Officer | 12624 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | benefits_value | Other Management Board Members | 87596 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | lti_granted | Chief Executive Officer | 373161 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | lti_granted | Other Management Board Members | 1050930 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | pension_contribution | Chief Executive Officer | 101959 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | pension_contribution | Other Management Board Members | 354564 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | sti_paid | Chief Executive Officer | 311850 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | sti_paid | Other Management Board Members | 926706 | Fail (hard) | CORE-03: quote not in the source text |
| cembra-money-bank-ag-752ce099 | total_remuneration | Chief Executive Officer | 1517803 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,429,594, stated 1,517,803 |
| cembra-money-bank-ag-752ce099 | total_remuneration | Other Management Board Members | 5079996 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 4,770,381, stated 5,079,996 |
| cembre | lti_target | Chair of BOD and Managing Dire | 180000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cembre | lti_target | Director | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cembre | sti_target | Director | 140000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| centrica-plc | listing_date |  | 1997-02-17 | Fail (hard) | CORE-02: not in the quote: 1997 |
| centrica-plc | share_price |  | 1.4065 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| ceres-power-holdings-plc | lti_target | Chief Financial Officer | 120 | Fail (hard) | CORE-03: quote not in the source text |
| ceres-power-holdings-plc | total_assets |  | 145796000 | Fail (hard) | CORE-02: 145796 not in the quote; CORE-03: quote not in the source text |
| ceres-power-holdings-plc | total_remuneration | Chief Financial Officer | 554167 | Fail (hard) | CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | base_salary | Former members of the Manageme | 747000 | Fail (hard) | CORE-02: 747 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | lti_granted | Former members of the Manageme | 112000 | Fail (hard) | CORE-02: 112 not in the quote; CORE-03: quote not in the source text |
| cham-swiss-properties-ag-7d9cb227 | sti_max | CEO | 80 | Fail (hard) | CORE-02: 80 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_max | Other members of the Managemen | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | CEO | 123000 | Fail (hard) | CORE-02: 123 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Other members of the Managemen | 239000 | Fail (hard) | CORE-02: 239 not in the quote |
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
| chesnara-plc | pension_type |  | defined contribution pension s | Fail (hard) | CORE-03: quote not in the source text |
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
| cie-automotive-s-a | revenue_by_country |  | EUROPA: 1415.2; NORTEAMÉRICA:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cindrigo-holdings-limited | base_salary | Director & Chief Executive Off | 195000 | Fail (hard) | CORE-02: 195000 not in the quote |
| cindrigo-holdings-limited | base_salary | Director & Chief Financial Off | 45000 | Fail (hard) | CORE-02: 45000 not in the quote |
| cindrigo-holdings-limited | base_salary | Executive Director (resigned 1 | 103783 | Fail (hard) | CORE-02: 103783 not in the quote |
| cir | benefits |  | coperture assicurative vita, i | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cir | benefits_value | Amministratore Delegato e Dire | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| cizzle-biotechnology-holdings-plc | fte |  | 0 | Fail | CORE-04: no period_end; NUM-04: 0 outside 0.5..5e+06 |
| cizzle-biotechnology-holdings-plc | shares_outstanding |  | 13005176000 | Fail (hard) | CORE-02: 13005176000 not in the quote |
| clarkson-plc | fte |  | 2103 | Fail (hard) | CORE-03: quote not in the source text |
| clarkson-plc | lti_max | Chief Executive Officer | 310 | Fail (hard) | COD-01: unit '' is not a target form |
| clarkson-plc | lti_max | Chief Financial Officer & Chie | 310 | Fail (hard) | COD-01: unit '' is not a target form |
| clarkson-plc | lti_target | Chief Executive Officer | 290 | Fail (hard) | COD-01: unit '' is not a target form |
| clarkson-plc | lti_target | Chief Financial Officer & Chie | 290 | Fail (hard) | COD-01: unit '' is not a target form |
| clarkson-plc | staff_by_segment |  | Broking: 1504; Financial: 127; | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 2,103 vs 2,250 (6.5% apart) |
| class-editori | controlling_owner |  | family | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| class-editori | controlling_owner_name |  | Paolo Panerai | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| class-editori | ebitda |  | 7971000 | Fail (hard) | CORE-02: 7971 not in the quote |
| class-editori | exchange |  | borsa di Milano | Fail (hard) | COD-01: 'borsa di Milano' matches no ISO 10383 exchange |
| class-editori | fte |  | 355 | Fail (hard) | CORE-02: 355 not in the quote |
| class-editori | largest_holders |  | Paolo Panerai 52.47%; Nicolett | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| class-editori | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| class-editori | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| class-editori | revenue |  | 80374000 | Fail (hard) | CORE-02: 80374 not in the quote |
| clinica-baviera-s-a | shares_outstanding |  | 16307.58 | Fail (hard) | CORE-02: 16307.58 not in the quote; CORE-04: no period_end; NUM-05: not a whole number |
| close-brothers-group-plc | benefits_value | Group Chief Executive (until J | 12000 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | benefits_value | Chief Executive | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| close-brothers-group-plc | pension_contribution | Group Chief Executive (until J | 42000 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | pension_contribution | Chief Executive | 80000 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | total_remuneration | Group Chief Executive (until J | 472000 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | total_remuneration | Chief Executive | 1044000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 907,000, stated 1,044,000 |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 0.4425 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| cmb-tech | base_salary | Chief Executive Officer | 249996 | Fail (hard) | CORE-02: 249996 not in the quote; CORE-03: quote not in the source text |
| cmb-tech | base_salary | Chief Financial Officer | 249996 | Fail (hard) | CORE-02: 249996 not in the quote; CORE-03: quote not in the source text |
| cmb-tech | base_salary | Chief Chartering Officer | 249996 | Fail (hard) | CORE-02: 249996 not in the quote; CORE-03: quote not in the source text |
| cmb-tech | base_salary | Chief Commercial Officer | 249996 | Fail (hard) | CORE-02: 249996 not in the quote; CORE-03: quote not in the source text |
| cmb-tech | base_salary | Chief Strategy Officer | 249996 | Fail (hard) | CORE-02: 249996 not in the quote; CORE-03: quote not in the source text |
| cmb-tech | headcount |  | 2826 | Fail (hard) | CORE-02: 2826 not in the quote |
| cmb-tech | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | pension_contribution | Chief Financial Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | pension_contribution | Chief Chartering Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | pension_contribution | Chief Commercial Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | pension_contribution | Chief Strategy Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | sti_paid | Chief Executive Officer | 62499 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | sti_paid | Chief Financial Officer | 62499 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | sti_paid | Chief Chartering Officer | 62499 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | sti_paid | Chief Commercial Officer | 62499 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | sti_paid | Chief Strategy Officer | 62499 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | total_remuneration | Chief Executive Officer | 312495 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | total_remuneration | Chief Financial Officer | 312495 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | total_remuneration | Chief Chartering Officer | 312495 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | total_remuneration | Chief Commercial Officer | 312495 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech | total_remuneration | Chief Strategy Officer | 312495 | Fail (hard) | CORE-03: quote not in the source text |
| cmb-tech-nv | headcount |  | 2826 | Fail (hard) | CORE-02: 2826 not in the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: quote not in the source text |
| coats-group-plc | share_price |  | 84.55 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| cobra-resources-plc | base_salary | Managing Director & Chief Exec | 150000 | Fail (hard) | CORE-03: quote not in the source text |
| cobra-resources-plc | base_salary | Executive Director, Business D | 50000 | Fail (hard) | CORE-03: quote not in the source text |
| cobra-resources-plc | sti_paid | Managing Director & Chief Exec | 80000 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-europacific-partners-plc | lti_max | Chief Executive Officer (CEO) | 500 | Fail (hard) | CORE-02: 500 not in the quote |
| coca-cola-europacific-partners-plc | revenue_by_country |  | Great Britain: 3470; Iberia: 3 | Fail (hard) | CORE-03: quote not in the source text |
| coca-cola-europacific-partners-plc | revenue_by_segment |  | Europe: 15404; APS: 5497 | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | lti_granted | Vorsitzende (seit 1. Oktober 2 | 777000 | Fail (hard) | CORE-02: 777 not in the quote |
| commerzbank-ag | lti_granted | Stellvertretender Vorsitzender | 634000 | Fail (hard) | CORE-02: 634 not in the quote |
| commerzbank-ag | lti_granted | Chief of Group Human Resources | 440000 | Fail (hard) | CORE-02: 440 not in the quote |
| commerzbank-ag | lti_granted | Chief of Business Segment Priv | 424000 | Fail (hard) | CORE-02: 424 not in the quote |
| commerzbank-ag | lti_granted | Chief Financial Officer (seit  | 369000 | Fail (hard) | CORE-02: 369 not in the quote |
| commerzbank-ag | lti_granted | Chief Risk Officer (seit 1. Ja | 440000 | Fail (hard) | CORE-02: 440 not in the quote |
| commerzbank-ag | lti_granted | Chief Operating Officer (seit  | 440000 | Fail (hard) | CORE-02: 440 not in the quote |
| commerzbank-ag | other_names |  | Commerz- und Disconto-Bank; Co | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | revenue_by_country |  | Deutschland: 8043; China einsc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 8 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: quote not in the source text |
| commerzbank-ag | staff_by_country |  | Deutschland: 23991; China eins | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | XF-01: parts add up to 3,923,000, more than the stated 3,744,000; XF-02: parts add up to 3,923,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | Stellvertretender Vorsitzender | 2917000 | Fail (hard) | XF-01: parts add up to 3,047,000, more than the stated 2,917,000; XF-02: parts add up to 3,047,000, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Chief of Group Human Resources | 2116000 | Fail (hard) | XF-01: parts add up to 2,296,000, more than the stated 2,116,000; XF-02: parts add up to 2,296,000, stated 2,116,000 |
| compagnie-financiere-tradition-sa-940d20ce | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| computacenter-plc | revenue_by_segment |  | UK: 1419.2; Germany: 2109.3; W | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | exchange |  | London Stock Exchange | Fail (hard) | CORE-02: not in the quote: london stock exchange |
| conduit-holdings-limited | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| conduit-holdings-limited | share_price |  | 4.3665 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| conduit-holdings-limited | staff_by_country |  | Bermuda: 64 | Fail | CORE-04: no period_end; NUM-08: adds up to 64 vs 68 (5.9% apart) |
| conduit-holdings-limited | sub_sector |  | Conduit Re is a Bermuda-based, | Fail (hard) | CORE-03: quote not in the source text |
| construcciones-y-auxiliar-de-ferrocarriles-s-a | revenue_by_segment |  | Railway: 3285; Buses: 927 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 4,212,000,000 vs 4,486,534,000 (6.1% apart) |
| construcciones-y-auxiliar-de-ferrocarriles-s-a | staff_by_country |  | Europe: 13582; Spain: 7687; Po | Fail | CORE-04: no period_end; NUM-08: adds up to 30,333 vs 15,451 (96.3% apart) |
| contango-holdings-plc | fte |  | 10 | Fail (hard) | CORE-03: quote not in the source text |
| contango-holdings-plc | headcount |  | 10 | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | base_salary | Vorstandsvorsitzender (01.12.2 | 1550000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| continental-ag-o-n | benefits |  | company car (personal use), re | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| convatec-group-plc | listing_date |  | 2016-10 | Fail (hard) | COD-06: not a year or a date |
| convatec-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| convatec-group-plc | staff_by_country |  | Europe: 5276; North America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| convatec-group-plc | staff_by_segment |  | Operations: 3467; Sales and ma | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-d | base_salary | Other senior executives | 8317000 | Fail (hard) | CORE-02: 8317 not in the quote |
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
| cph-group-ag-2a655fb2 | aggregate_headcount | Other members of the Group Exe | 3 | Fail (hard) | CORE-03: quote not in the source text |
| cph-group-ag-2a655fb2 | benefits_value | CEO (up to 31.03.2025) | 662000 | Fail (hard) | CORE-02: 662 not in the quote |
| cph-group-ag-2a655fb2 | benefits_value | Other members of the Group Exe | 558000 | Fail (hard) | CORE-02: 558 not in the quote |
| cranswick-plc | fte |  | 13033 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | headcount |  | 13033 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | lti_granted | Chief Executive | 2923784 | Fail (hard) | CORE-02: 2923784 not in the quote |
| cranswick-plc | lti_granted | Chief Financial Officer | 1456866 | Fail (hard) | CORE-02: 1456866 not in the quote |
| cranswick-plc | lti_granted | Chief Commercial Officer | 1456866 | Fail (hard) | CORE-02: 1456866 not in the quote |
| cranswick-plc | lti_granted | Chief Operating Officer | 1456866 | Fail (hard) | CORE-02: 1456866 not in the quote |
| crediabank-s-a | benefits |  | ασφάλιση αστικής, επαγγελματικ | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| credito-emiliano-credem | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| credito-emiliano-credem | controlling_owner_name |  | Credito Emiliano Holding S.p.A | Fail (hard) | CORE-03: quote not in the source text |
| credito-emiliano-credem | headcount |  | 6771 | Fail (hard) | CORE-03: quote not in the source text |
| credito-emiliano-credem | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| credito-emiliano-credem | share_price |  | 15.28 | Fail (hard) | CORE-03: quote not in the source text |
| credito-emiliano-credem | staff_by_country |  | Italy: 6771 | Fail (hard) | CORE-03: quote not in the source text |
| crest-nicholson-holdings-plc | revenue_by_segment |  | UK housebuilding: 610.8 | Fail (hard) | CORE-03: quote not in the source text |
| crest-nicholson-holdings-plc | sti_target | Chief Executive Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| crest-nicholson-holdings-plc | sti_target | Chief Financial Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| critical-metals-plc | listing_date |  | 2017 | Fail (hard) | CORE-02: not in the quote: 2017 |
| critical-metals-plc | share_price |  | 14.25 | Fail (hard) | CORE-03: quote not in the source text |
| critical-metals-plc | staff_by_country |  | DRC: 49 | Fail | CORE-04: no period_end |
| critical-mineral-resources-plc | fte |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | headcount |  | 5 | Fail (hard) | CORE-03: quote not in the source text |
| critical-mineral-resources-plc | staff_by_country |  | Morocco: 1; UK: 4 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | benefits_value | Chief Financial Officer | 37453 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | pension_contribution | Chief Financial Officer | 87000 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | sti_paid | Chief Financial Officer | 359203 | Fail (hard) | CORE-03: quote not in the source text |
| croda-international-plc | total_remuneration | Chief Financial Officer | 1745977 | Fail (hard) | XF-01: parts add up to 2,078,640, more than the stated 1,745,977; XF-02: parts add up to 2,078,640, stated 1,745,977 |
| csg | shares_outstanding |  | 20 | Fail (hard) | CORE-02: 20 not in the quote; NUM-04: 20 outside 1000..1e+12 |
| csp-international-industria-calze | base_salary | Presidente e Amministratore De | 253009 | Fail (hard) | CORE-02: 253009 not in the quote |
| csp-international-industria-calze | base_salary | Vice Presidente e Amministrato | 249618 | Fail (hard) | CORE-02: 249618 not in the quote |
| cts-eventim-kgaa-1664614e | controlling_owner_name |  | KPS Stiftung | Fail (hard) | CORE-02: not in the quote: stiftung |
| cts-eventim-kgaa-1664614e | revenue_by_country |  | Germany: 1347630; Italy: 60590 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cts-eventim-kgaa-1664614e | revenue_by_segment |  | Ticketing: 947220; Live Entert | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cumulex | revenue |  | 1234567000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| cumulex | total_assets |  | 890123000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| currys-plc | fte |  | 25076 | Fail (hard) | CORE-02: 25076 not in the quote |
| cykel-ai-plc | headcount |  | 9 | Fail (hard) | CORE-02: 9 not in the quote |
| cykel-ai-plc | total_assets |  | 1537768 | Fail (hard) | CORE-03: quote not in the source text |
| d-ieteren-group | revenue_by_segment |  | Belron: 3381.2; TVH: 667.4; D' | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 12,082,200,000 vs 8,033,500,000 (50.4% apart) |
| danieli-c | revenue_by_country |  | Europa: 1900; Asia: 1400; Amer | Fail (hard) | CORE-03: quote not in the source text |
| danieli-c | revenue_by_segment |  | Plant Making: 3100; Steel Maki | Fail (hard) | CORE-03: quote not in the source text |
| danieli-c | total_assets |  | 6700000000 | Fail (hard) | CORE-03: quote not in the source text |
| dar-global-plc | headcount |  | 434 | Fail (hard) | CORE-02: 434 not in the quote; CORE-03: quote not in the source text |
| data-modul-ag-9cac6e64 | ebitda |  | 2490000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| data-modul-ag-9cac6e64 | revenue_by_segment |  | Displays: 126601; Systems: 862 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| datwyler-holding-ag-eca04fdb | largest_holders |  | Paul Hälg, Hanspeter Fässler,  | Fail (hard) | CORE-03: quote not in the source text |
| datwyler-holding-ag-eca04fdb | lti_target | CEO | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| datwyler-holding-ag-eca04fdb | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| datwyler-holding-ag-eca04fdb | revenue_by_segment |  | Healthcare: 462.7; Industrial: | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| dcc-energy-plc | lti_target | Chief Financial Officer | 112.5 | Fail (hard) | CORE-02: 112.5 not in the quote; CORE-03: quote not in the source text |
| dcc-energy-plc | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| dcc-energy-plc | sti_paid | Chief Executive | 1928000 | Fail (hard) | CORE-03: quote not in the source text |
| de-longhi | total_remuneration | Chairman and Chief Executive O | 2022823 | Fail (hard) | XF-01: parts add up to 2,602,823, more than the stated 2,022,823; XF-02: parts add up to 2,602,823, stated 2,022,823 |
| defence-holdings-plc | lti_vested | Executive Director, Chief Fina | 648000 | Fail (hard) | CORE-02: 648 not in the quote |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | COD-06: not a year or a date |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Philip von  | 63000 | Fail (hard) | CORE-02: 63000 not in the quote |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Andreas Prü | 243750 | Fail (hard) | CORE-02: 243750 not in the quote |
| delticom-ag-na-o-n | sti_max | Vorstandsmitglied (Nathalie Kr | 105000 | Fail (hard) | CORE-02: 105000 not in the quote |
| deme-group | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| deme-group | total_remuneration | CEO | 2306000 | Fail (hard) | XF-01: parts add up to 2,539,000, more than the stated 2,306,000; XF-02: parts add up to 2,539,000, stated 2,306,000 |
| deme-group | total_remuneration | Executive Committee members | 5458000 | Fail (hard) | XF-01: parts add up to 6,064,000, more than the stated 5,458,000; XF-02: parts add up to 6,064,000, stated 5,458,000 |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_max | Chief Financial Officer (since | 264000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | sti_target | Chief Financial Officer (since | 132000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| derwent-london-plc | lti_target | Chief Executive | 58.75 | Fail (hard) | CORE-02: 58.75 not in the quote |
| derwent-london-plc | lti_target | Chief Financial Officer | 58.75 | Fail (hard) | CORE-02: 58.75 not in the quote |
| derwent-london-plc | lti_target | Executive Director (until Marc | 58.75 | Fail (hard) | CORE-02: 58.75 not in the quote |
| derwent-london-plc | lti_target | Executive Director | 58.75 | Fail (hard) | CORE-02: 58.75 not in the quote |
| derwent-london-plc | sti_target | Chief Executive | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| derwent-london-plc | sti_target | Chief Financial Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| derwent-london-plc | sti_target | Executive Director (until Marc | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| derwent-london-plc | sti_target | Executive Director | 75 | Fail (hard) | CORE-02: 75 not in the quote |
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
| dfi-retail-group-holdings-limited | base_salary | Executive Directors | 5600000 | Fail (hard) | CORE-03: quote not in the source text |
| dfi-retail-group-holdings-limited | lti_vested | Executive Directors and execut | 1900000 | Fail (hard) | CORE-03: quote not in the source text |
| dfi-retail-group-holdings-limited | pension_contribution | Executive Directors | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| dfs-furniture-plc | benefits_value | Chief Executive Officer | 5000 | Fail (hard) | CORE-02: 5 not in the quote |
| dfs-furniture-plc | benefits_value | Chief Financial Officer | 3000 | Fail (hard) | CORE-02: 3 not in the quote |
| dfs-furniture-plc | benefits_value | Interim Chief Financial Office | 51000 | Fail (hard) | CORE-02: 51 not in the quote |
| dfs-furniture-plc | pension_contribution | Chief Executive Officer | 18000 | Fail (hard) | CORE-02: 18 not in the quote |
| dfs-furniture-plc | pension_contribution | Chief Financial Officer | 2000 | Fail (hard) | CORE-02: 2 not in the quote |
| dfs-furniture-plc | pension_contribution | Interim Chief Financial Office | 13000 | Fail (hard) | CORE-02: 13 not in the quote |
| diageo-plc | revenue_by_country |  | United States: 7408; India: 32 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| diageo-plc | revenue_by_segment |  | North America: 7249; Europe: 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 19,643,000,000 vs 27,762,000,000 (29.2% apart) |
| diageo-plc | staff_by_segment |  | SC&P: 6963; Corporate and othe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 12,605 vs 27,972 (54.9% apart) |
| dialight-plc | lti_max | Executive Group Chair | 35 | Fail (hard) | CORE-03: quote not in the source text |
| digi-spain-telecom-s-a | role_disclosure | Other members of Alta Direcció | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| digi-spain-telecom-s-a | total_remuneration | Other members of Alta Direcció | 1070000 | Fail (hard) | CORE-03: quote not in the source text |
| digi-spain-telecom-s-a | total_remuneration | Executive Directors | 3040000 | Fail (hard) | CORE-02: 3.04 not in the quote |
| digia-oyj | aggregate_headcount | Key Management | 15 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | lti_granted | Chairman/CEO | 131706 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | lti_granted | CEO | 131706 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | lti_granted | CFO/Executive Director | 79024 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | lti_granted | Executive Director | 32926 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | staff_by_country |  | Italy: 105; outside Italy: 165 | Fail (hard) | CORE-03: quote not in the source text |
| digital-bros | sti_max | Chairman/CEO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| digital-bros | sti_max | CEO | 120000 | Fail (hard) | CORE-02: 120000 not in the quote |
| digital-bros | sti_max | CFO/Executive Director | 99606.6 | Fail (hard) | CORE-02: 99606.6 not in the quote |
| digital-bros | sti_max | Executive Director | 90913.5 | Fail (hard) | CORE-02: 90913.5 not in the quote |
| digital-bros | sti_target | Chairman/CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| digital-bros | sti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| digital-bros | sti_target | CFO/Executive Director | 23 | Fail (hard) | COD-01: unit '' is not a target form |
| diploma-plc | lti_target | Chief Executive Officer | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| diploma-plc | lti_target | Acting Chief Financial Officer | 62.5 | Fail (hard) | CORE-02: 62.5 not in the quote |
| diploma-plc | lti_vested | Acting Chief Financial Officer | 498000 | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | revenue_by_segment |  | Controls: 836.4; Seals: 456; L | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-03: quote not in the source text |
| diploma-plc | sti_target | Acting Chief Financial Officer | 75 | Fail (hard) | CORE-03: quote not in the source text |
| discoverie-group-plc-d676c327 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| distribuidora-internacional-de-alimentacion-s-a | ebitda |  | 316000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| distribuidora-internacional-de-alimentacion-s-a | fte |  | 27364 | Fail (hard) | CORE-02: 27364 not in the quote; NUM-13: FTE 27,364 above headcount 16,887 |
| do-co-aktiengesellschaft-1ce4abbb | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| do-co-aktiengesellschaft-1ce4abbb | revenue_by_country |  | Türkiye: 648.16; Great Britain | Fail | CORE-04: no period_end; NUM-08: adds up to 2,298,120,000 vs 2,461,590,000 (6.6% apart) |
| do-co-aktiengesellschaft-1ce4abbb | staff_by_country |  | Austria: 1641; Germany: 2493;  | Fail | CORE-04: no period_end; NUM-08: adds up to 19,330 vs 14,762 (30.9% apart) |
| docmorris-ag-be190279 | base_salary | Other members of the Executive | 1426000 | Fail (hard) | CORE-02: 1426 not in the quote |
| docmorris-ag-be190279 | benefits_value | Other members of the Executive | 35000 | Fail (hard) | CORE-02: 35 not in the quote |
| docmorris-ag-be190279 | lti_granted | Other members of the Executive | 714000 | Fail (hard) | CORE-02: 714 not in the quote |
| docmorris-ag-be190279 | pension_contribution | Other members of the Executive | 282000 | Fail (hard) | CORE-02: 282 not in the quote |
| docmorris-ag-be190279 | sti_paid | Other members of the Executive | 514000 | Fail (hard) | CORE-02: 514 not in the quote |
| docmorris-ag-be190279 | total_remuneration | Other members of the Executive | 2971000 | Fail (hard) | CORE-02: 2971 not in the quote |
| domiki-kritis-s-a | exchange_segment |  | Small and Medium Capitalizatio | Fail (hard) | CORE-02: not in the quote: small and medium capitalization |
| domino-s-pizza-group-plc | fte |  | 2402 | Fail (hard) | CORE-02: 2402 not in the quote |
| domino-s-pizza-group-plc | lti_max | Interim CEO (from 24 November  | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| domino-s-pizza-group-plc | lti_max | Former CFO (until 18 September | 87.5 | Fail (hard) | CORE-02: 87.5 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | CEO | 388000 | Fail (hard) | CORE-02: 388 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | Other EC | 1365000 | Fail (hard) | CORE-02: 1365 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | benefits_value | Former EC | 452000 | Fail (hard) | CORE-02: 452 not in the quote |
| dormakaba-holding-ag-9c17f7d1 | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: PDF link without #page= |
| dormakaba-holding-ag-9c17f7d1 | shareholding_requirement |  | CEO: 300% of annual base salar | Fail (hard) | CORE-03: quote not in the source text |
| dottikon-es-holding-ag-d22b9c0d | lti_max | Präsident des Verwaltungsrates | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| dottikon-es-holding-ag-d22b9c0d | lti_target | Präsident des Verwaltungsrates | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| dottikon-es-holding-ag-d22b9c0d | sti_max | Präsident des Verwaltungsrates | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| dottikon-es-holding-ag-d22b9c0d | sti_target | Präsident des Verwaltungsrates | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
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
| dromeas-sa | ebitda |  | 2439338 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| dromeas-sa | revenue_by_country |  | ΕΛΛΑΔΑ: 7768741; ΤΡΙΤΕΣ ΧΩΡΕΣ: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| dunelm-group-plc | total_remuneration | Chief Financial Officer | 832000 | Fail (hard) | XF-01: parts add up to 873,000, more than the stated 832,000; XF-02: parts add up to 873,000, stated 832,000 |
| east-star-resources-plc | base_salary | Chief Executive Officer | 125000 | Fail (hard) | CORE-02: 125 not in the quote |
| east-star-resources-plc | base_salary | Technical Director | 68000 | Fail (hard) | CORE-02: 68 not in the quote |
| east-star-resources-plc | fte |  | 13 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 13 above headcount 9 |
| easyjet-plc | revenue_by_segment |  | Airline: 8666; Holidays: 1917 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| easyjet-plc | shareholding_requirement |  | The CEO and the CFO are requir | Fail (hard) | CORE-03: quote not in the source text |
| ebusco-holding | lti_granted | CFO | 187500 | Fail (hard) | CORE-02: 187500 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| econocom-group | role_disclosure | Chairman of the Board of Direc | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| econocom-group | sti_max | Chairman of the Board of Direc | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| econocom-group | sti_max | Executive Directors, non-Execu | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ecora-royalties-plc | base_salary | Chief Executive Officer | 485000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | base_salary | Chief Financial Officer | 345000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | lti_vested | Chief Financial Officer | 52000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_country |  | Australia: 19664; Americas: 31 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | revenue_by_segment |  | Cobalt: 18871; Copper: 14180;  | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | sti_paid | Chief Financial Officer | 220000 | Fail (hard) | CORE-03: quote not in the source text |
| ecora-royalties-plc | total_remuneration | Chief Financial Officer | 654000 | Fail (hard) | CORE-03: quote not in the source text |
| edp-s-a | ebitda |  | 5028000000 | Fail (hard) | CORE-02: 5028 not in the quote |
| edp-s-a | share_price |  | 3.915 | Fail (hard) | CORE-02: 3.915 not in the quote |
| el-d-mouzakis-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| el-d-mouzakis-s-a | sub_sector |  | Κατασκευή κλωστικών προϊόντων  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| el-en | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| el-en | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| el-en | pension_type |  | For Administrators (non-employ | Fail (hard) | CORE-03: quote not in the source text |
| el-en | shareholding_requirement |  | For Administrators and Directo | Fail (hard) | CORE-03: quote not in the source text |
| el-en | sti_max | Presidente e Consigliere deleg | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| el-en | sti_max | Consigliere delegato | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| elementis-plc | lti_max | CEO (from April 2025) | 17.5 | Fail (hard) | COD-01: unit 'cents' is not a target form |
| elementis-plc | lti_max | CFO Designate (from Nov 2025) | 17.5 | Fail (hard) | COD-01: unit 'cents' is not a target form |
| elementis-plc | lti_target | CEO (from April 2025) | 14.3 | Fail (hard) | COD-01: unit 'cents' is not a target form |
| elementis-plc | lti_target | CFO Designate (from Nov 2025) | 14.3 | Fail (hard) | COD-01: unit 'cents' is not a target form |
| elementis-plc | total_remuneration | CEO (from April 2025) | 1123000 | Fail (hard) | XF-01: parts add up to 1,146,000, more than the stated 1,123,000; XF-02: parts add up to 1,146,000, stated 1,123,000 |
| elia-group | lti_max | Chief Executive Officer (since | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Chief Executive Officer of 50H | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Chief Executive Officer of Eli | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Chief Financial Officer (since | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Chief Human Resources Officer  | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Co-Chief Human Resources Offic | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Chief Digital Officer (until 2 | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_max | Co-Chief Financial Officer (un | 45 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Executive Officer (since | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Executive Officer of 50H | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Executive Officer of Eli | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Financial Officer (since | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Human Resources Officer  | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Co-Chief Human Resources Offic | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elia-group | lti_target | Chief Digital Officer (until 2 | 30 | Fail (hard) | CORE-03: quote not in the source text |
| elica | share_price |  | 1.665 | Fail (hard) | CORE-02: 1.665 not in the quote |
| elinoil-hellenic-petroleum-company-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| elinoil-hellenic-petroleum-company-s-a | staff_by_country |  | Kifissia: 113; Aspropyrgos: 25 | Fail | CORE-04: no period_end; NUM-08: adds up to 224 vs 301 (25.6% apart) |
| elixirr-international-plc | listing_date |  | 2025-07 | Fail (hard) | COD-06: not a year or a date |
| ellaktor-s-a | listing_date |  | April 1994 | Fail (hard) | COD-06: not a year or a date |
| ellaktor-s-a | revenue_by_country |  | Greece: 87271; Romania: 532; C | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ellaktor-s-a | share_price |  | 1.348 | Fail (hard) | CORE-02: 1.348 not in the quote |
| elve-s-a | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| emerald-horizon-ag-a6420623 | base_salary | Vorstand | 133354 | Fail (hard) | CORE-02: 133354 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
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
| ems-chemie-holding-ag-d319099b | pension_type |  | Defined benefit plans for Swis | Fail (hard) | CORE-03: quote not in the source text |
| enav | controlling_owner_name |  | Ministry for the Economy and F | Fail (hard) | CORE-02: not in the quote: for |
| ence-energia-y-celulosa-s-a | fte |  | 1305 | Fail (hard) | CORE-03: quote not in the source text |
| ence-energia-y-celulosa-s-a | share_price |  | 2.406 | Fail (hard) | CORE-02: 2.406 not in the quote |
| endeavour-mining-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | controlling_owner_name |  | La Mancha | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | fte |  | 5659 | Fail (hard) | CORE-02: 5659 not in the quote |
| endeavour-mining-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| endeavour-mining-plc | revenue_by_segment |  | Ity Mine: 838.1; Houndé Mine:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| energean-plc | lti_vested | Chief Executive Officer | 272000 | Fail (hard) | CORE-03: quote not in the source text |
| energean-plc | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| energean-plc | sti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| enervit | ebitda |  | 9411000 | Fail (hard) | CORE-02: 9.411 not in the quote; CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| enervit | staff_by_country |  | Province of Como: 162; Provinc | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| enquest-plc | revenue_by_country |  | North Sea: 895313; Malaysia: 1 | Fail (hard) | CORE-03: quote not in the source text |
| entain-plc | share_price |  | 7.666 | Fail (hard) | CORE-02: 7.666 not in the quote |
| epic-suisse-ag-7c2f8dc4 | sti_max | Chief Executive Officer | 60.1 | Fail (hard) | CORE-02: 60.1 not in the quote |
| epic-suisse-ag-7c2f8dc4 | sti_max | Other members of Group Executi | 50.6 | Fail (hard) | CORE-02: 50.6 not in the quote |
| epigenomics-ag-ddb6ea6d | total_remuneration | Former Vorstand (until January | -33000 | Fail (hard) | NUM-04: -33000 outside 0..5e+10; XF-01: parts add up to -32,468, more than the stated -33,000 |
| equita-group | controlling_owner_name |  | Management and employees | Fail (hard) | CORE-02: not in the quote: management |
| equita-group | listing_date |  | 2018-10 | Fail (hard) | COD-06: not a year or a date |
| equita-group | staff_by_country |  | Italia: 194; Estero: 8 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| erg | ebitda |  | 4700000000 | Fail (hard) | NUM-01: unit 'Rs' is not ISO 4217 |
| erg | shares_outstanding |  | 1067435965 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| erg | staff_by_country |  | Kenya: 492; Madagascar: 185; M | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 916 vs 7,278 (87.4% apart) |
| erste-group-bank-ag | exchange |  | Vienna | Fail (hard) | COD-01: 'Vienna' matches no ISO 10383 exchange |
| erste-group-bank-ag | listing_date |  | 1997-12-04 | Fail (hard) | CORE-02: not in the quote: 1997 |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 800128.68 | Fail (hard) | CORE-02: 800128.68 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 530136.54 | Fail (hard) | CORE-02: 530136.54 not in the quote |
| erste-group-bank-ag | lti_max | Vorsitzender des Vorstands / C | 60 | Fail (hard) | CORE-02: 60 not in the quote; COD-01: unit '' is not a target form |
| erste-group-bank-ag | lti_max | Chief Corporates and Markets O | 60 | Fail (hard) | CORE-02: 60 not in the quote; COD-01: unit '' is not a target form |
| erste-group-bank-ag | lti_max | Chief Financial Officer | 60 | Fail (hard) | CORE-02: 60 not in the quote; COD-01: unit '' is not a target form |
| erste-group-bank-ag | lti_max | Chief Risk Officer | 60 | Fail (hard) | CORE-02: 60 not in the quote; COD-01: unit '' is not a target form |
| erste-group-bank-ag | lti_max | Chief Platform Officer / Chief | 60 | Fail (hard) | CORE-02: 60 not in the quote; COD-01: unit '' is not a target form |
| erste-group-bank-ag | lti_target | Vorsitzender des Vorstands / C | 45 | Fail (hard) | CORE-02: 45 not in the quote |
| erste-group-bank-ag | lti_target | Chief Corporates and Markets O | 45 | Fail (hard) | CORE-02: 45 not in the quote |
| erste-group-bank-ag | lti_target | Chief Financial Officer | 45 | Fail (hard) | CORE-02: 45 not in the quote |
| erste-group-bank-ag | lti_target | Chief Risk Officer | 45 | Fail (hard) | CORE-02: 45 not in the quote |
| erste-group-bank-ag | lti_target | Chief Platform Officer / Chief | 45 | Fail (hard) | CORE-02: 45 not in the quote |
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
| eukedos | base_salary | Presidente del Consiglio di Am | 60000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | base_salary | Amministratore Delegato | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | base_salary | Dirigente con responsabilità s | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | benefits_value | Presidente del Consiglio di Am | 5000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | benefits_value | Amministratore Delegato | 5000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | benefits_value | Dirigente con responsabilità s | 0 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | lti_granted | Presidente del Consiglio di Am | 0 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | lti_granted | Amministratore Delegato | 0 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | pension_type |  | mandatory | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | sti_paid | Presidente del Consiglio di Am | 0 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | sti_paid | Amministratore Delegato | 0 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | total_remuneration | Presidente del Consiglio di Am | 65000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | total_remuneration | Amministratore Delegato | 45000 | Fail (hard) | CORE-03: quote not in the source text |
| eukedos | total_remuneration | Dirigente con responsabilità s | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| eurobank-s-a | lti_granted | CEO | 1230000 | Fail (hard) | CORE-03: quote not in the source text |
| eurobank-s-a | lti_granted | Deputy CEO Group Chief Operati | 950000 | Fail (hard) | CORE-03: quote not in the source text |
| eurobank-s-a | lti_granted | Deputy CEO Head of Corporate & | 950000 | Fail (hard) | CORE-03: quote not in the source text |
| eurobank-s-a | pension_contribution | Deputy CEO Group Chief Operati | 144312 | Fail (hard) | CORE-03: quote not in the source text |
| eurobank-s-a | pension_contribution | Deputy CEO Head of Corporate & | 144312 | Fail (hard) | CORE-03: quote not in the source text |
| eurocell-plc | listing_date |  | 2015-03 | Fail (hard) | COD-06: not a year or a date |
| eurocell-plc | share_price |  | 130.5 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| eurocommercial | revenue_by_segment |  | Belgium: 28385; France: 49862; | Fail | CORE-04: no period_end; NUM-08: adds up to 241,864,000 vs 274,219,000 (11.8% apart) |
| eurogroup-laminations | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| euronext-athens-holding-s-a | revenue_by_segment |  | Listing: 5.7; Trading: 8.6; Po | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 47,000,000 vs 82,855,000 (43.3% apart) |
| eurotelesites-ag | revenue_by_country |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| eurotelesites-ag | revenue_by_segment |  | Austria: 164807; Bulgaria: 325 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| everest-global-plc | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | controlling_owner_name |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | largest_holders |  | Golden Nice International Grou | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| everest-global-plc | share_price |  | 2.51 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| evn-ag-90cea5f3 | listing_date |  | 1989 und 1990 | Fail (hard) | COD-06: not a year or a date |
| evn-ag-90cea5f3 | other_names |  | NIOGAS Niederösterreichische G | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| evn-ag-90cea5f3 | share_price |  | 28.8 | Fail (hard) | CORE-02: 28.8 not in the quote |
| evoke-plc-5c77d1d2 | share_price |  | 0.222 | Fail (hard) | CORE-02: 0.222 not in the quote |
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
| exor-nv | lti_max | Executive Directors | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| facc-ag-5f4b658e | headcount |  | 4050 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| facc-ag-5f4b658e | revenue_by_country |  | Germany: 354938; USA: 149717;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| facc-ag-5f4b658e | revenue_by_segment |  | Aerostructures: 345100; Engine | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| facc-ag-5f4b658e | staff_by_country |  | Austria: 3218; Croatia: 473 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 3,691 vs 4,050 (8.9% apart) |
| fagron | base_salary | Other members of Executive Lea | 1540660 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| fagron | benefits_value | Other members of Executive Lea | 75627 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| fagron | pay_currency | Other members of Executive Lea | EUR | Fail | CORE-04: no period_end |
| fagron | pension_contribution | Other members of Executive Lea | 22517 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| fagron | sti_paid | Other members of Executive Lea | 2432078 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| fair-value-reit-ag-cef1dc63 | exchange |  | Frankfurt Stock Exchange | Fail (hard) | CORE-02: not in the quote: stock exchange |
| fair-value-reit-ag-cef1dc63 | sub_sector |  | Immobilienbestandshalter mit F | Fail (hard) | CORE-03: quote not in the source text |
| fairview-international-plc-ae11bf81 | pension_type |  | nil | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fairview-international-plc-ae11bf81 | shares_outstanding |  | 556000000 | Fail (hard) | CORE-02: 556000000 not in the quote |
| fastighetsbolag-emilshus-pref | benefits |  | fast lön, övriga förmåner, pen | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | isin |  | SE0016785786 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | pension_type |  | premiebaserad pensionslösning | Fail (hard) | CORE-03: quote not in the source text |
| fastned | controlling_owner_name |  | Fastned Administratie Stichtin | Fail (hard) | CORE-02: not in the quote: administratie stichting |
| fastned | staff_by_segment |  | corporate functions: 4; Networ | Fail | CORE-04: no period_end; NUM-08: adds up to 40 vs 414 (90.3% apart) |
| fastpartner-d | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_max | Other Executive Management Tea | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_max | Other members of the Executive | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fdm-group-holdings-plc-5f964aeb | total_remuneration | Directors | 2108000 | Fail (hard) | XF-01: parts add up to 2,289,000, more than the stated 2,108,000; XF-02: parts add up to 2,289,000, stated 2,108,000 |
| ferretti | sub_sector |  | The Group designs, produces an | Fail (hard) | CORE-03: quote not in the source text |
| ferrexpo-plc-5653b4e7 | staff_by_country |  | Ukraine: 8542 | Fail | CORE-04: no period_end; NUM-08: adds up to 8,542 vs 7,570 (12.8% apart) |
| fevara-plc-92307031 | ebitda |  | 3497000 | Fail (hard) | CORE-02: 3.497 not in the quote |
| fevara-plc-92307031 | revenue_by_country |  | UK: 35471; USA: 37443; Republi | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fidia | fte |  | 152.5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fidia | share_price |  | 0.127 | Fail (hard) | CORE-02: 0.127 not in the quote |
| fila | ebitda |  | 93259000 | Fail (hard) | CORE-02: 93.259 not in the quote |
| fila | revenue_by_country |  | Europe: 293841; North America: | Fail | CORE-04: no period_end; NUM-08: adds up to 928,500,000 vs 572,213,000 (62.3% apart) |
| finecobank | revenue_by_country |  | Italia: 1650233; Irlanda: 4277 | Fail | CORE-04: no period_end; NUM-08: adds up to 2,077,989,000 vs 1,316,475,000 (57.8% apart) |
| finecobank | share_price |  | 15.79 | Fail (hard) | CORE-02: 15.79 not in the quote |
| first-class-metals-plc-ae225da0 | listing_date |  | July 2022 | Fail (hard) | COD-06: not a year or a date |
| first-tin-plc-9086dd77 | headcount |  | 24 | Fail (hard) | CORE-02: 24 not in the quote |
| fisher-james-sons-plc-1d273817 | headcount |  | 1947 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fisher-james-sons-plc-1d273817 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| fisher-james-sons-plc-1d273817 | share_price |  | 375 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| fisher-james-sons-plc-1d273817 | total_remuneration | CEO | 1426000 | Fail (hard) | XF-01: parts add up to 1,694,000, more than the stated 1,426,000; XF-02: parts add up to 1,694,000, stated 1,426,000 |
| fisher-james-sons-plc-1d273817 | total_remuneration | CFO | 886000 | Fail (hard) | XF-01: parts add up to 993,000, more than the stated 886,000; XF-02: parts add up to 993,000, stated 886,000 |
| flexdeal-simfe-s-a | total_remuneration | Presidente do Conselho de Admi | 177236 | Fail (hard) | XF-01: parts add up to 201,986, more than the stated 177,236; XF-02: parts add up to 201,986, stated 177,236 |
| flexdeal-simfe-s-a | total_remuneration | Administradora Executiva | 157847 | Fail (hard) | XF-01: parts add up to 180,122, more than the stated 157,847; XF-02: parts add up to 180,122, stated 157,847 |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | ebitda |  | 25861000 | Fail (hard) | NUM-01: unit 'Ευρώ' is not ISO 4217 |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | lti_target | Αντιπρόεδρος ΔΣ εκτελεστικό μέ | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | lti_target | Διευθύνων Σύμβουλος (Σταμάτιος | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | lti_target | Εκτελεστικό Μέλος ΔΣ (Ασημίνα  | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | lti_target | Αναπληρωτής Διευθύνων Σύμβουλο | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | lti_target | Αναπληρωτής Διευθύνων Σύμβουλο | 10000 | Fail (hard) | CORE-03: quote not in the source text |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | pension_contribution | Αντιπρόεδρος ΔΣ εκτελεστικό μέ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | pension_contribution | Διευθύνων Σύμβουλος (Σταμάτιος | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | pension_contribution | Εκτελεστικό Μέλος ΔΣ (Ασημίνα  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | pension_contribution | Αναπληρωτής Διευθύνων Σύμβουλο | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flexopack-societe-anonyme-commercial-and-industrial-plastics-company | pension_contribution | Αναπληρωτής Διευθύνων Σύμβουλο | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: quote not in the source text |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: quote on page 103, link says page 102 |
| flughafen-wien-ag | sub_sector |  | The FWAG Group generates reven | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| fluxys-belgium-d | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| fluxys-belgium-d | controlling_owner_name |  | Fluxys | Fail (hard) | CORE-03: quote not in the source text |
| fluxys-belgium-d | largest_holders |  | Fluxys 90%; The public 10%; Th | Fail (hard) | CORE-03: quote not in the source text |
| fluxys-belgium-d | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| fluxys-belgium-d | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| fnm | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fnm | sti_target | Dirigente | 40 | Fail (hard) | CORE-03: quote not in the source text |
| fortec-elektro-b45e5cd6 | controlling_owner_name |  | JotWe GmbH and FloJulCosMAr Gm | Fail (hard) | CORE-02: not in the quote: and |
| foxtons-group-plc-1852b951 | lti_granted | CEO | 506000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| foxtons-group-plc-1852b951 | sti_paid | CEO | 87800 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| foxtons-group-plc-1852b951 | sti_paid | CFO | 45900 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | base_salary | CEO | 219240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | benefits |  | company car, phone and accommo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| framery-group | lti_vested | Management team | 3273000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | revenue_by_country |  | Eurooppa, Lähi-itä ja Afrikka: | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | revenue_by_segment |  | Äänieristetyt työtilat: 216017 | Fail | CORE-04: no period_end; NUM-08: adds up to 222,127,000 vs 162,119,000 (37.0% apart) |
| framery-group | staff_by_country |  | Finland: 357; Americas: 21; EM | Fail | CORE-04: no period_end; NUM-08: adds up to 398 vs 484 (17.8% apart) |
| framery-group | sti_paid | CEO | 36000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | total_remuneration | CEO | 255240 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| framery-group | website |  | framery.com | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| frasers-group-plc-6a13d052 | shareholding_requirement |  | Executive Directors: share pri | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| frasers-group-plc-6a13d052 | total_remuneration | Chief Operating Officer | 251000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| frigoglass-s-a-i-c | headcount |  | 222 | Fail (hard) | CORE-03: quote not in the source text |
| frigoglass-s-a-i-c | pension_type |  | σύστημα δικαιωμάτων προαίρεσης | Fail (hard) | CORE-03: quote not in the source text |
| frigoglass-s-a-i-c | revenue_by_segment |  | Εξοπλισμός: 2635; Τεχνικές υπη | Fail (hard) | CORE-03: quote not in the source text |
| fuchs-se-4990a338 | shareholding_requirement |  | Executive Board members must i | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| funding-circle-holdings-plc-5c033007 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | benefits |  | seguro de saúde, telemóvel e v | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| futebol-clube-do-porto-futebol-sad | role_disclosure | Administrador (Carlos Nuno Gom | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Presidente da Comissão Executi | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (José Pedro Fari | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Carlos Nuno Gom | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Ana Teresa Cunh | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Maria do Rosári | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (José Pedro Fari | 350000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Carlos Nuno Gom | 80500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Ana Teresa Cunh | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Maria do Rosári | 28000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| galderma-group-ag-8c1dbf8c | shareholding_requirement |  | CEO: 300% of annual base salar | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| galliford-try-holdings-plc-46fc9d1a | sti_target | Chief Executive | 60 | Fail (hard) | CORE-02: 60 not in the quote |
| galliford-try-holdings-plc-46fc9d1a | sti_target | Chief Financial Officer | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| gam-holding-ag-6ce711d2 | benefits_value | Group Management Board | 822133 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gam-holding-ag-6ce711d2 | pension_type |  | defined contribution and defin | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| gam-holding-ag-6ce711d2 | role_disclosure | Group Management Board (aggreg | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| games-workshop-group-plc-0f667d1d | benefits |  | life assurance cover, sharesav | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| games-workshop-group-plc-0f667d1d | lti_granted | CEO | 2175000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| games-workshop-group-plc-0f667d1d | pension_type |  | defined contribution, up to 8. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| games-workshop-group-plc-0f667d1d | shareholding_requirement |  | executive directors are requir | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gamma-communications-plc-4deb67ef | benefits |  | participation in the Group’s l | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| garofalo-health-care | listing_date |  | November 9, 2018 | Fail (hard) | COD-06: not a year or a date |
| gek-terna-s-a | benefits_value | Chairman and Chief Executive O | 29547 | Fail (hard) | CORE-02: 29547 not in the quote |
| gek-terna-s-a | benefits_value | Executive Director, Executive  | 9583 | Fail (hard) | CORE-02: 9583 not in the quote |
| gek-terna-s-a | benefits_value | Executive BoD Member | 10320 | Fail (hard) | CORE-02: 10320 not in the quote |
| gek-terna-s-a | sub_sector |  | The main activity of the Compa | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gek-terna-s-a | total_remuneration | Chairman and Chief Executive O | 700000 | Fail (hard) | XF-01: parts add up to 729,547, more than the stated 700,000; XF-02: parts add up to 729,547, stated 700,000 |
| gek-terna-s-a | total_remuneration | Executive BoD Member | 511620 | Fail (hard) | XF-01: parts add up to 521,940, more than the stated 511,620; XF-02: parts add up to 521,940, stated 511,620 |
| gem-resources-plc-cf7e06ac | headcount |  | 23 | Fail (hard) | CORE-02: 23 not in the quote |
| gens-aurea | staff_by_country |  | Italia: 568; Spagna: 283; Port | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| georgia-capital-plc-298a1d16 | benefits |  | life insurance; health insuran | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| georgia-capital-plc-298a1d16 | sti_paid | Executive Director | 7960000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| georgina-energy-plc-7639c631 | total_assets |  | 1760635 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gerresheimer-ag-25295c16 | sti_paid | Member of the Board (since Nov | 4000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gerresheimer-ag-25295c16 | sti_paid | Chief Financial Officer (since | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| gimv | aggregate_headcount | Other members of the executive | 7 | Fail (hard) | CORE-03: quote not in the source text |
| gimv | lti_max | CEO | 14 | Fail (hard) | COD-01: unit '' is not a target form |
| gimv | lti_max | Other members of the executive | 14 | Fail (hard) | COD-01: unit '' is not a target form |
| gimv | lti_target | CEO | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| gimv | lti_target | Other members of the executive | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| gimv | lti_vested | Other members of the executive | 2383203 | Fail (hard) | CORE-02: 2383203 not in the quote |
| gimv | total_remuneration | Other members of the executive | 5617060 | Fail (hard) | XF-01: parts add up to 6,001,663, more than the stated 5,617,060; XF-02: parts add up to 6,001,663, stated 5,617,060 |
| global-dominion-access-s-a | staff_by_country |  | Colombia: 3048; Spain: 2033; C | Fail | CORE-04: no period_end; NUM-08: adds up to 7,945 vs 11,629 (31.7% apart) |
| gpi | revenue |  | 500000000 | Fail (hard) | CORE-03: quote not in the source text |
| gpi | revenue_by_country |  | Italy: 353.9; Abroad: 79.5 | Fail | CORE-04: no period_end; NUM-08: adds up to 433,400,000 vs 500,000,000 (13.3% apart) |
| gpi | revenue_by_segment |  | Software: 227.4; Care: 163.8;  | Fail | CORE-04: no period_end; NUM-08: adds up to 433,400,000 vs 500,000,000 (13.3% apart) |
| gpi | total_assets |  | 1000000000 | Fail (hard) | CORE-03: quote not in the source text |
| gr-sarantis-s-a | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| grafton-group-plc-79b8acde | listing_date |  | 2013 | Fail (hard) | CORE-02: not in the quote: 2013 |
| grand-vision-media-holdings-plc-aca75f65 | headcount |  | 9 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| great-southern-copper-plc-d619eabd | largest_holders |  | Foreign Dimensions Pty Limited | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| great-southern-copper-plc-d619eabd | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| green-earth-group | aggregate_headcount | Key management personnel | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| greggs-plc-5347e6c0 | sti_target | Chief Executive | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| greggs-plc-5347e6c0 | sti_target | Chief Financial Officer | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| grifols-s-a | base_salary | Co-Chief Executive Officer (Ra | 855000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | base_salary | Co-Chief Executive Officer (Vi | 855000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | lti_vested | Co-Chief Executive Officer (Ra | 169000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | lti_vested | Co-Chief Executive Officer (Vi | 174000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | role_disclosure | Co-Chief Executive Officer (Ra | individual | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | role_disclosure | Co-Chief Executive Officer (Vi | individual | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | sti_max | Co-Chief Executive Officer (Ra | 65 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | sti_max | Co-Chief Executive Officer (Vi | 65 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | sti_paid | Co-Chief Executive Officer (Ra | 252000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | sti_paid | Co-Chief Executive Officer (Vi | 183000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | total_remuneration | Co-Chief Executive Officer (Ra | 1276000 | Fail (hard) | CORE-01: PDF link without #page= |
| grifols-s-a | total_remuneration | Co-Chief Executive Officer (Vi | 1212000 | Fail (hard) | CORE-01: PDF link without #page= |
| grupo-media-capital-sgps-s-a | revenue_by_segment |  | Televisão, Digital e Entreteni | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 214,356,123 vs 259,191 (82602.0% apart) |
| gsk-plc-669dcd41 | lti_target | Outgoing CEO (until 31 Decembe | 725 | Fail (hard) | CORE-02: 725 not in the quote |
| gulf-marine-services-plc-f393af40 | accounting_basis |  | UK Law, UK adopted internation | Fail (hard) | CORE-03: quote not in the source text |
| gulf-marine-services-plc-f393af40 | benefits |  | fixed cash and reimbursable al | Fail (hard) | CORE-03: quote not in the source text |
| gulf-marine-services-plc-f393af40 | fte |  | 745 | Fail (hard) | CORE-02: 745 not in the quote |
| gulf-marine-services-plc-f393af40 | pension_type |  | No pension provision | Fail (hard) | CORE-03: quote not in the source text |
| haidemenos-integrated-printing-services-s-a | total_remuneration | Board of Directors | 274964 | Fail (hard) | XF-01: parts add up to 316,559, more than the stated 274,964; XF-02: parts add up to 316,559, stated 274,964 |
| hamak-gold-limited-68536373 | fte |  | 6 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hamak-gold-limited-68536373 | headcount |  | 6 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hamborner-reit-ag-cb84ee44 | listing_date |  | 1954 | Fail (hard) | CORE-02: not in the quote: 1954 |
| hammerson-plc-f1d49abe | pension_contribution | CEO (from 1 January 2026, CEO  | 10 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| hammerson-plc-f1d49abe | role_disclosure | CFO | individual | Fail (hard) | CORE-01: no endpoint URL |
| hansard-global-plc-f13a5b81 | ticker |  | HSD | Fail (hard) | CORE-02: not in the quote: hsd; CORE-03: source not cached; the run itself did not find the quote |
| harbour-energy-plc-7a9017f1 | lti_max | CFO | 320 | Fail (hard) | CORE-02: 320 not in the quote |
| harbour-energy-plc-7a9017f1 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| harena-rare-earths-plc-229c562b | controlling_owner |  | institutional | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harena-rare-earths-plc-229c562b | controlling_owner_name |  | Vidacos Nominees Limited | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harena-rare-earths-plc-229c562b | largest_holders |  | Vidacos Nominees Limited 28.91 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harena-rare-earths-plc-229c562b | ownership_type |  | other | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harena-rare-earths-plc-229c562b | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harworth-group-plc-7d3f06a0 | benefits_value | CFO | 17977 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harworth-group-plc-7d3f06a0 | lti_vested | CFO | 199357 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| harworth-group-plc-7d3f06a0 | pension_contribution | CFO | 35203 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hawesko-holding-se-bd2e62b7 | benefits_value | Vorsitzender | 28000 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied | 17000 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (seit 01.10.2025) | 3000 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | benefits_value | Mitglied (bis 09.10.2025) | 15000 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | lti_vested | Vorsitzender | 0 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied | 0 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (seit 01.10.2025) | 0 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | lti_vested | Mitglied (bis 09.10.2025) | 0 | Fail (hard) | CORE-03: quote on page 11, link says page 10 |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Vorsitzender | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (seit 01.10.2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawesko-holding-se-bd2e62b7 | role_disclosure | Mitglied (bis 09.10.2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| hawick-data-nv | pension_contribution | CEO | 18000 | Fail (hard) | CORE-03: quote not in the source text |
| hawick-data-nv | sti_paid | CEO | 19000 | Fail (hard) | CORE-03: quote not in the source text |
| hawick-data-nv | total_remuneration | CEO | 203000 | Fail (hard) | CORE-03: quote not in the source text |
| hays-plc-7467dcac | base_salary | CEO (from 27 February 2026) | 208000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hays-plc-7467dcac | base_salary | CEO (until 27 February 2026) | 436000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hays-plc-7467dcac | base_salary | CFO | 484000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| helical-plc-cefce900 | lti_vested | Chief Executive | 24000 | Fail (hard) | CORE-02: 24 not in the quote |
| helical-plc-cefce900 | lti_vested | Chief Financial Officer | 101000 | Fail (hard) | CORE-02: 101 not in the quote |
| helical-plc-cefce900 | shareholding_requirement |  | Matthew Bonning-Snook: 500% of | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (bis 15.07.202 | 1868000 | Fail (hard) | XF-01: parts add up to 2,641,000, more than the stated 1,868,000; XF-02: parts add up to 2,641,000, stated 1,868,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführerin (seit 01.03. | 993000 | Fail (hard) | XF-01: parts add up to 1,143,000, more than the stated 993,000; XF-02: parts add up to 1,143,000, stated 993,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 1425000 | Fail (hard) | XF-01: parts add up to 1,622,000, more than the stated 1,425,000; XF-02: parts add up to 1,622,000, stated 1,425,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.03.20 | 1380000 | Fail (hard) | XF-01: parts add up to 1,551,000, more than the stated 1,380,000; XF-02: parts add up to 1,551,000, stated 1,380,000 |
| hella-gmbh-co-kgaa-740cce46 | total_remuneration | Geschäftsführer (seit 01.04.20 | 2105000 | Fail (hard) | XF-01: parts add up to 2,369,000, more than the stated 2,105,000; XF-02: parts add up to 2,369,000, stated 2,105,000 |
| helleniq-energy-holdings-s-a | staff_by_country |  | Greece: 3154; Republic of Nort | Fail | CORE-04: no period_end; NUM-08: adds up to 3,705 vs 4,192 (11.6% apart) |
| helleniq-energy-holdings-s-a | staff_by_segment |  | HELLENiQ ENERGY HOLDINGS S.A.: | Fail | CORE-04: no period_end; NUM-08: adds up to 3,705 vs 4,192 (11.6% apart) |
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
| hemogenyx-pharmaceuticals-plc-ff627795 | fte |  | 16 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hemogenyx-pharmaceuticals-plc-ff627795 | headcount |  | 16 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hemogenyx-pharmaceuticals-plc-ff627795 | staff_by_segment |  | Research & development: 14; Ad | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hermana-holding | fte |  | 0 | Fail | CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| hiag-immobilien-holding-ag-3a28978d | sti_max | CEO | 300000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hiag-immobilien-holding-ag-3a28978d | sti_max | Other members of the Executive | 220000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hidong-estate-plc-cc203b38 | base_salary | Executive Director | 1334 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | ebitda |  | 45144 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | pay_currency | Executive Director | RM | Fail (hard) | COD-01: RM is not ISO 4217 |
| hidong-estate-plc-cc203b38 | reporting_currency |  | RM | Fail (hard) | COD-01: RM is not ISO 4217 |
| hidong-estate-plc-cc203b38 | revenue |  | 417731 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hidong-estate-plc-cc203b38 | total_remuneration | Executive Director | 1334 | Fail (hard) | NUM-01: unit 'RM' is not ISO 4217 |
| hilton-food-group-plc-3a56b109 | base_salary | Executive Chair (from 25 Novem | 850000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | lti_granted | Chief Executive Officer (until | 1912500 | Fail (hard) | CORE-02: 1912500 not in the quote |
| hilton-food-group-plc-3a56b109 | lti_vested | Executive Chair (from 25 Novem | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | lti_vested | Chief Financial Officer | 7000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | sti_paid | Executive Chair (from 25 Novem | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | sti_paid | Chief Financial Officer | 151000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | total_remuneration | Executive Chair (from 25 Novem | 850000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| hilton-food-group-plc-3a56b109 | total_remuneration | Chief Financial Officer | 623000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 576,000, stated 623,000 |
| himalaya-shipping | controlling_owner_name |  | Drew Holdings Ltd. | Fail (hard) | CORE-02: not in the quote: ltd |
| hochschild-mining-plc-4d2379f4 | sti_target | CEO | 90 | Fail (hard) | CORE-02: 90 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
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
| holland-colours | lti_max | CEO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | lti_max | CFO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | lti_max | CTO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | sti_max | CEO | 45 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holland-colours | sti_max | CFO | 45 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holland-colours | sti_max | CTO | 45 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| home-invest-be | headcount |  | 48 | Fail (hard) | CORE-02: 48 not in the quote |
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
| huber-suhner-ag-11887265 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| huber-suhner-ag-11887265 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| huber-suhner-ag-11887265 | staff_by_country |  | Switzerland: 1099; Poland: 970 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| hydrogen-utopia-international-plc-51b104d1 | share_price |  | 0.028 | Fail (hard) | CORE-02: 0.028 not in the quote |
| hypoport-se-73d5ece9 | staff_by_country |  | Germany: 2314; Netherlands: 59 | Fail | CORE-04: no period_end; NUM-08: adds up to 2,436 vs 2,203 (10.6% apart) |
| i-grandi-viaggi | base_salary | Presidente | 270000 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | base_salary | Vice Presidente | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | base_salary | Dirigente | 79983 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | base_salary | Dirigente preposto alle scritt | 79983 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | benefits |  | l’assegnazione di autovetture  | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | benefits_value | Dirigente | 1712 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | benefits_value | Dirigente preposto alle scritt | 1712 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | controlling_owner_name |  | MONFORTE & C. S.r.l. | Fail (hard) | CORE-02: not in the quote: monforte c |
| i-grandi-viaggi | role_disclosure | Presidente | individual | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | role_disclosure | Vice Presidente | individual | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | role_disclosure | Dirigente preposto alle scritt | individual | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | sti_paid | Presidente | 140000 | Fail (hard) | CORE-03: quote not in the source text; NUM-11: paid 52% of base, maximum 30% |
| i-grandi-viaggi | sti_paid | Vice Presidente | 40000 | Fail (hard) | CORE-03: quote not in the source text; NUM-11: paid 53% of base, maximum 30% |
| i-grandi-viaggi | total_remuneration | Presidente | 410000 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | total_remuneration | Vice Presidente | 115000 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | total_remuneration | Dirigente | 81695 | Fail (hard) | CORE-03: quote not in the source text |
| i-grandi-viaggi | total_remuneration | Dirigente preposto alle scritt | 81695 | Fail (hard) | CORE-03: quote not in the source text |
| iba | base_salary | CFO | 198977 | Fail (hard) | CORE-03: quote not in the source text |
| iba | controlling_owner_name |  | Sustainable Anchorage SRL | Fail (hard) | CORE-02: not in the quote: srl |
| iberdrola-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| iberdrola-s-a | total_remuneration | Consejero delegado (desde 24 d | 1452000 | Fail (hard) | XF-01: parts add up to 1,526,000, more than the stated 1,452,000; XF-02: parts add up to 1,526,000, stated 1,452,000 |
| ibstock-plc-81ff3340 | pension_contribution | CFO (until 10 October 2025) | 29453 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ibstock-plc-81ff3340 | total_remuneration | CFO (until 10 October 2025) | 325515 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| icfg-limited-cfbafea2 | revenue_by_country |  | Mongolia: 61340; Central Asia: | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 66,928,000 vs 72,364,000 (7.5% apart) |
| icfg-limited-cfbafea2 | revenue_by_segment |  | Microfinance: 66928; Other bus | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| icg-plc-b82eb2fc | revenue_by_country |  | Europe (including UK): 765.2;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| icg-plc-b82eb2fc | revenue_by_segment |  | FMC: 900; IC: 96 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ideal-holdings-s-a | staff_by_country |  | Ελλάδα: 2427; Κύπρος: 16; Βουλ | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ideal-holdings-s-a | sub_sector |  | Αποστολή της IDEAL Holdings εί | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| iforex-financial-trading-holdings-ltd-74e42f45 | base_salary | Chief Executive Officer | 840000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | base_salary | Chief Financial Officer | 456000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | benefits_value | Chief Financial Officer | 47035 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pay_currency | Chief Executive Officer | NIS | Fail (hard) | COD-01: NIS is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pay_currency | Chief Financial Officer | NIS | Fail (hard) | COD-01: NIS is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | pension_contribution | Chief Financial Officer | 67625 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | total_remuneration | Chief Executive Officer | 840000 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| iforex-financial-trading-holdings-ltd-74e42f45 | total_remuneration | Chief Financial Officer | 570660 | Fail (hard) | NUM-01: unit 'NIS' is not ISO 4217 |
| ilyda-sa | fiscal_year_end |  | 2025-12-31 | Fail (hard) | CORE-03: quote not in the source text |
| imaging-biometrics-limited-3542bcb1 | total_assets |  | 1014125 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| imc-exploration-group-plc-91b5483e | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: market |
| imcd | total_remuneration | Former CEO (until April 2025) | 2493000 | Fail (hard) | XF-01: parts add up to 2,623,000, more than the stated 2,493,000; XF-02: parts add up to 2,623,000, stated 2,493,000 |
| imi-plc-cbc5827b | benefits_value | Chief Executive Officer | 37000 | Fail (hard) | CORE-02: 37 not in the quote |
| imi-plc-cbc5827b | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| imi-plc-cbc5827b | sti_target | Executive Director (from 1 Aug | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| immo-moury | aggregate_headcount | Autres dirigeants | 3.5 | Fail (hard) | NUM-05: not a whole number |
| immo-moury | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| immo-moury | controlling_owner_name |  | G4 Finance SRL | Fail (hard) | CORE-03: quote not in the source text |
| immo-moury | largest_holders |  | G4 Finance SRL 99.99% | Fail (hard) | CORE-03: quote not in the source text |
| immo-moury | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| immo-moury | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| immo-moury | ultimate_parent |  | Gilles-Olivier Moury | Fail (hard) | CORE-03: quote not in the source text |
| impresa-sociedade-gestora-de-participacoes-sociais-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| impresa-sociedade-gestora-de-participacoes-sociais-s-a | sub_sector |  | produção e disseminação de con | Fail (hard) | CORE-03: quote not in the source text |
| inchcape-plc-ea221c9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| industrivarden-c | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Deputy Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Other members of Executive Man | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| inficon-holding-ag-4220ed6f | base_salary | Other members of Group Managem | 365000 | Fail (hard) | CORE-02: 365 not in the quote |
| inficon-holding-ag-4220ed6f | benefits_value | President and Chief Executive  | 244000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| inmocemento-s-a | fte |  | 1360 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| inmocemento-s-a | headcount |  | 1486 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| inmocemento-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| inmocemento-s-a | share_price |  | 3.59 | Fail (hard) | CORE-02: 3.59 not in the quote |
| intea-fastigheter-d | revenue_by_segment |  | Rättsväsende: 983; Högre utbil | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,779,000,000 vs 1,561,000,000 (14.0% apart) |
| integrated-diagnostics-holdings-plc-b28b60df | listing_date |  | 2015-05 | Fail (hard) | COD-06: not a year or a date |
| integrated-diagnostics-holdings-plc-b28b60df | revenue_by_country |  | Egypt: 6642; Sudan: 2.3; Jorda | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intercontinental-hotels-group-plc-ca6a391f | listing_date |  | April 2003 | Fail (hard) | COD-06: not a year or a date |
| intercos | base_salary | Presidente Esecutivo CdA | 1700000 | Fail (hard) | CORE-03: quote not in the source text |
| intercos | total_remuneration | Presidente Esecutivo CdA | 1723142.45 | Fail (hard) | CORE-03: quote not in the source text |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_granted | IAG Chief Executive Officer | 4113000 | Fail (hard) | CORE-02: 4113000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_max | IAG Chief Executive Officer | 450 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_target | IAG Chief Executive Officer | 210 | Fail (hard) | CORE-02: 210 not in the quote |
| international-consolidated-airlines-group-s-a-afe59a89 | lti_vested | Management Committee | 23000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | controlling_owner |  | family | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | controlling_owner_name |  | Mark Dixon | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | listing_date |  | 2000 | Fail (hard) | CORE-02: not in the quote: 2000 |
| international-workplace-group-plc-3ae007b6 | lti_granted | Chief Executive Officer | 2151000 | Fail (hard) | CORE-02: 2151 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | lti_granted | Chief Financial Officer | 1148000 | Fail (hard) | CORE-02: 1148 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | lti_max | Chief Executive Officer | 300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | lti_max | Chief Financial Officer | 300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | revenue_by_segment |  | Company-owned: 3212; Managed & | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| international-workplace-group-plc-3ae007b6 | share_price |  | 2.314 | Fail (hard) | CORE-02: 2.314 not in the quote |
| interpump-group | accounting_basis |  | IFRS issued by the Internaonal | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| interpump-group | controlling_owner |  | family | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| interpump-group | controlling_owner_name |  | Leila Monpò e Sorelle S.A.p.A. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| interpump-group | largest_holders |  | Leila Monpò e Sorelle S.A.p.A. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| interpump-group | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| interpump-group | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intershop-holding-ag-6e9d3cef | benefits |  | benefits in kind | Fail (hard) | CORE-03: quote not in the source text |
| interwood-xylemporia-a-t-e-n-e | shares_outstanding |  | 48834999 | Fail (hard) | CORE-03: quote not in the source text |
| intica-systems-se-18005922 | sti_max | Vorsitzender des Vorstands | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intica-systems-se-18005922 | sti_max | Mitglied des Vorstands (bis 30 | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intracom-holdings-s-a | controlling_owner_name |  | Sokratis Kokkalis | Fail (hard) | CORE-02: not in the quote: sokratis |
| intracom-holdings-s-a | lti_max | Πρόεδρος Δ.Σ., & Δ/νων Σύμβουλ | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Πρόεδρος Δ.Σ., & Δ/νων Σύμβουλ | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| investec-plc-422fa59c | staff_by_segment |  | Wealth & Investment: 520; Spec | Fail | CORE-04: no period_end; NUM-08: adds up to 7,520 vs 7,949 (5.4% apart) |
| irce | staff_by_country |  | Europe: 437; America: 133; Asi | Fail (hard) | CORE-03: quote not in the source text |
| iren | share_price |  | 2.556 | Fail (hard) | CORE-02: 2.556 not in the quote |
| italgas | share_price |  | 9.515 | Fail (hard) | CORE-02: 9.515 not in the quote |
| ithaca-energy-plc-c6840a94 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| ivu-traffic-techn-ag-020c6212 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| jeronimo-martins-sgps-s-a | ultimate_parent |  | Sociedade Francisco Manuel dos | Fail (hard) | CORE-02: not in the quote: sociedade francisco manuel dos santos holding b v |
| johnson-service-group-plc-9e93b50d | benefits_value | Former Chief Financial Officer | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| johnson-service-group-plc-9e93b50d | lti_vested | Former Chief Financial Officer | 334000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| jumbo | pay_currency | Directors and Board Members | EUR | Fail | CORE-04: no period_end |
| jumbo | pension_contribution | Directors and Board Members | 215291 | Fail (hard) | CORE-02: 215291 not in the quote |
| jumbo | revenue_by_segment |  | Toy: 216551175; Baby products: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| jumbo | shares_outstanding |  | 135120963 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| jungfraubahn-holding-ag-90ceddd3 | aggregate_headcount | Executive Board | 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Chairman of the Executive Boar | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Executive Board | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Chairman of the Executive Boar | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Executive Board | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| juventus-football-club | benefits_value | Amministratore Delegato (from  | 30200 | Fail (hard) | CORE-03: quote not in the source text |
| juventus-football-club | role_disclosure | Board (non-executive) | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| kapsch-trafficcom-ag-1d6bbc81 | ebitda |  | 20600000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kapsch-trafficcom-ag-1d6bbc81 | revenue_by_country |  | Österreich: 15982; EMEA (exklu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ultimate_parent |  | Traditio-Privatstiftung; CHILD | Fail (hard) | CORE-02: not in the quote: traditio privatstiftung |
| kardex-holding-ag-b5808d3c | total_remuneration | CEO | 882200 | Fail (hard) | XF-01: parts add up to 1,020,600, more than the stated 882,200; XF-02: parts add up to 1,020,600, stated 882,200 |
| karelia-tobacco-company-inc | exchange_segment |  | Securities Market | Fail (hard) | CORE-02: not in the quote: securities market |
| kavango-resources-plc-86ebc0c1 | headcount |  | 186 | Fail (hard) | CORE-02: 186 not in the quote |
| kavango-resources-plc-86ebc0c1 | listing_date |  | 2018-07 | Fail (hard) | COD-06: not a year or a date |
| kbc | base_salary | CEO | 2279730 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CEO of the International Marke | 160690 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CEO of the Czech Republic Busi | 102964 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CIO | 160690 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CEO of the Belgium Business Un | 160690 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CFO | 160690 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_granted | CRO | 156695 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | lti_max | CEO | 570662 | Fail (hard) | CORE-02: 570662 not in the quote |
| kbc | lti_max | CEO of the International Marke | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | lti_max | CEO of the Czech Republic Busi | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | lti_max | CIO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | lti_max | CEO of the Belgium Business Un | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | lti_max | CFO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | lti_max | CRO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CEO | 570662 | Fail (hard) | CORE-02: 570662 not in the quote |
| kbc | sti_max | CEO of the International Marke | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CEO of the Czech Republic Busi | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CIO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CEO of the Belgium Business Un | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CFO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_max | CRO | 242942.5 | Fail (hard) | CORE-02: 242942.5 not in the quote |
| kbc | sti_paid | CEO of the International Marke | 231494 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | sti_paid | CEO of the Czech Republic Busi | 140778 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | sti_paid | CIO | 230741 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | sti_paid | CEO of the Belgium Business Un | 228481 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | sti_paid | CFO | 223209 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kbc | sti_paid | CRO | 218461 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| keller-group-plc-85e72b53 | benefits_value | CFO | 20000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| keller-group-plc-85e72b53 | lti_vested | CFO | 1277000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| keller-group-plc-85e72b53 | pension_contribution | CFO | 31000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| keller-group-plc-85e72b53 | sti_paid | CFO | 440000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kelso-group-holdings-plc-5218b8cc | revenue |  | -542922 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-04: -542922 outside 0..1e+14 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (J H Goold) | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (J D Brooke) | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kelso-group-holdings-plc-5218b8cc | total_remuneration | Director (left 30 September 20 | -15563 | Fail (hard) | NUM-04: -15563 outside 0..5e+10; XF-01: parts add up to -15,563, more than the stated -15,563 |
| kenmare-resources-plc-e7d5776b | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| kerry-group-plc-56fe152d | revenue_by_country |  | USA: 2840; Republic of Ireland | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 2,939,400,000 vs 6,757,600,000 (56.5% apart) |
| kesko-b | controlling_owner_name |  | K-kauppiasliitto ry | Fail (hard) | CORE-02: not in the quote: ry |
| kinepolis-group | lti_granted | CEO | 112500 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts EUR |
| kinepolis-group | lti_vested | CEO | 2817 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts EUR |
| kinepolis-group | sti_max | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| kinepolis-group | sti_paid | CEO | 450000 | Fail (hard) | CORE-02: 450000 not in the quote; CORE-03: quote not in the source text |
| kingfisher-plc-94bd46d7 | total_remuneration | CEO | 3936600 | Fail (hard) | XF-01: parts add up to 4,053,200, more than the stated 3,936,600; XF-02: parts add up to 4,053,200, stated 3,936,600 |
| kingfisher-plc-94bd46d7 | total_remuneration | CFO | 2394600 | Fail (hard) | XF-01: parts add up to 2,475,200, more than the stated 2,394,600; XF-02: parts add up to 2,475,200, stated 2,394,600 |
| klingelnberg-ag-d32e6349 | benefits_value | Executive Management | 70334.18 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | benefits_value | CEO | 29343.67 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | lti_granted | Executive Management | 510000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | lti_granted | CEO | 170000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| klingelnberg-ag-d32e6349 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| kme-group | pension_type |  | defined contribution (for exec | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| koenig-bauer-ag-1f22b792 | lti_granted | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357 not in the quote |
| koenig-bauer-ag-1f22b792 | lti_target | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_max | CEO (from June 2025) | 494000 | Fail (hard) | CORE-02: 494000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_target | CEO (from June 2025) | 330000 | Fail (hard) | CORE-02: 330000 not in the quote |
| koenig-bauer-ag-1f22b792 | total_remuneration | CEO (from June 2025) | 934000 | Fail (hard) | XF-01: parts add up to 959,000, more than the stated 934,000; XF-02: parts add up to 959,000, stated 934,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former CEO (until June 2025),  | 782000 | Fail (hard) | XF-01: parts add up to 813,000, more than the stated 782,000; XF-02: parts add up to 813,000, stated 782,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former Member of the Managemen | 446000 | Fail (hard) | XF-01: parts add up to 507,000, more than the stated 446,000; XF-02: parts add up to 507,000, stated 446,000 |
| komax | staff_by_segment |  | Production: 674; Research and  | Fail | CORE-04: no period_end; NUM-08: adds up to 1,841 vs 3,167 (41.9% apart) |
| kri-kri-milk-industry-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kri-kri-milk-industry-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| kri-kri-milk-industry-s-a | headcount |  | 752 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kri-kri-milk-industry-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kri-kri-milk-industry-s-a | revenue_by_country |  | Ελλάδα: 122949638; Εξωτερικό:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| lakefront-biother | base_salary | Chief Executive Officer | 427888 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lakefront-biother | benefits_value | Chief Executive Officer | 13630 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lakefront-biother | lti_granted | Chief Executive Officer | 101750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lakefront-biother | pension_contribution | Chief Executive Officer | 14682 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lakefront-biother | staff_by_segment |  | Senior leadership: 121; Middle | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 1,027 vs 452 (127.2% apart) |
| lakefront-biother | sti_paid | Chief Executive Officer | 478731 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lakefront-biother | total_remuneration | Chief Executive Officer | 1036682 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lanakam-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| lanakam-s-a | headcount |  | 22 | Fail (hard) | CORE-02: 22 not in the quote |
| lancashire-holdings-limited-94cc95db | staff_by_country |  | US: 33; Canada: 1; UK: 347; Be | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| landi-renzo | aggregate_headcount | Dirigenti Strategici | 1 | Fail (hard) | CORE-03: quote not in the source text |
| landi-renzo | base_salary | Presidente del CdA | 407000 | Fail (hard) | CORE-03: quote not in the source text |
| landi-renzo | base_salary | AD e Direttore Generale | 427000 | Fail (hard) | CORE-02: 427000 not in the quote; CORE-03: quote not in the source text |
| landi-renzo | benefits_value | Dirigenti Strategici | 0 | Fail (hard) | CORE-03: quote not in the source text |
| landi-renzo | listing_date |  | June 2007 | Fail (hard) | COD-06: not a year or a date |
| landi-renzo | sti_paid | Dirigenti Strategici | 0 | Fail (hard) | CORE-03: quote not in the source text |
| law-debenture-corporation-plc-the-d1b5e75c | listing_date |  | 1889 | Fail (hard) | CORE-02: not in the quote: 1889; COD-06: not a year or a date |
| law-debenture-corporation-plc-the-d1b5e75c | lti_granted | Chief Executive Officer | 657000 | Fail (hard) | CORE-02: 657 not in the quote |
| law-debenture-corporation-plc-the-d1b5e75c | lti_granted | Chief Operating Officer | 453000 | Fail (hard) | CORE-02: 453 not in the quote |
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
| leonteq-ag-6723ca54 | lti_max | Executive Committee (current m | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| leonteq-ag-6723ca54 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| leonteq-ag-6723ca54 | sti_max | Executive Committee (current m | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| leonteq-ag-6723ca54 | sti_max | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| libertas-7-s-a | base_salary | Consejero Ejecutivo | 143000 | Fail (hard) | CORE-02: 143 not in the quote |
| libertas-7-s-a | lti_max | Consejero Ejecutivo | 37500 | Fail (hard) | CORE-02: 37500 not in the quote |
| libertas-7-s-a | sti_max | Consejero Ejecutivo | 87500 | Fail (hard) | CORE-02: 87500 not in the quote |
| libertas-7-s-a | sub_sector |  | desarrollo de actividades de i | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| linea-directa-aseguradora-s-a-compania-de-seguros-y-reaseguros | share_price |  | 1.118 | Fail (hard) | CORE-02: 1.118 not in the quote |
| linz-textil-holding-ag-e11cf1a9 | ebitda |  | 939336 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| linz-textil-holding-ag-e11cf1a9 | largest_holders |  | TYLE-Privatstiftung 80%; Tyle  | Fail (hard) | NUM-07: holdings add up to 160% |
| linz-textil-holding-ag-e11cf1a9 | listing_date |  | 1872 | Fail (hard) | COD-06: not a year or a date |
| lion-finance-group-plc-03b7fac3 | lti_max | Executive Director | 200 | Fail (hard) | COD-01: unit '' is not a target form |
| lion-finance-group-plc-03b7fac3 | lti_target | Executive Director | 100 | Fail (hard) | COD-01: unit '' is not a target form |
| logista-integral-s-a | fte |  | 7752 | Fail (hard) | CORE-02: 7752 not in the quote; CORE-03: quote not in the source text |
| logista-integral-s-a | headcount |  | 7695 | Fail (hard) | CORE-02: 7695 not in the quote |
| logitech-international-s-a-0a74f2ba | pension_type |  | defined benefit pension plans  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| london-stock-exchange-group-plc-e057fe1a | benefits_value | Chief Executive Officer | 157000 | Fail (hard) | CORE-02: 157 not in the quote |
| london-stock-exchange-group-plc-e057fe1a | shareholding_requirement |  | CEO: 600% of salary; other Exe | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lonza-group-ag-e4f248d2 | accounting_basis |  | IFRS Accounting Standards | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| lonza-group-ag-e4f248d2 | aggregate_headcount | Executive Committee | 8.8 | Fail (hard) | NUM-05: not a whole number |
| lonza-group-ag-e4f248d2 | base_salary | Executive Committee | 5390000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lonza-group-ag-e4f248d2 | benefits_value | CEO | 350000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lonza-group-ag-e4f248d2 | benefits_value | Executive Committee | 1990000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| lufthansa-ag-0bc3d92c | controlling_owner_name |  | Deutsche Lufthansa Aktiengesel | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| maire | ebitda |  | 500130000 | Fail (hard) | CORE-02: 500.13 not in the quote; CORE-03: quote not in the source text |
| maire | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| maire | share_price |  | 13.05 | Fail (hard) | CORE-02: 13.05 not in the quote |
| marshalls-plc-ba8b711a | lti_vested | Executive Director (Simon Bour | 140000 | Fail (hard) | CORE-02: 140 not in the quote |
| marshalls-plc-ba8b711a | lti_vested | Executive Director (Justin Loc | 142000 | Fail (hard) | CORE-02: 142 not in the quote |
| maschinenfabrik-berthold-hermle-6808fdaf | exchange |  | Stuttgart Stock Exchange | Fail (hard) | COD-01: 'Stuttgart Stock Exchange' matches no ISO 10383 exchange |
| maschinenfabrik-berthold-hermle-6808fdaf | lti_target | Vorstand (Günther Beck) | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| maschinenfabrik-berthold-hermle-6808fdaf | lti_target | Vorstand (Franz-Xaver Bernhard | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| maschinenfabrik-berthold-hermle-6808fdaf | lti_target | Vorstand (Benedikt Hermle) | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| maschinenfabrik-berthold-hermle-6808fdaf | staff_by_country |  | Germany: 1228 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,228 vs 1,639 (25.1% apart) |
| maschinenfabrik-berthold-hermle-6808fdaf | sti_target | Vorstand (Günther Beck) | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| maschinenfabrik-berthold-hermle-6808fdaf | sti_target | Vorstand (Franz-Xaver Bernhard | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| maschinenfabrik-berthold-hermle-6808fdaf | sti_target | Vorstand (Benedikt Hermle) | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| masterflex-96d8f19f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| materialise | base_salary | Chief Executive Officer | 489195 | Fail (hard) | CORE-03: quote not in the source text |
| materialise | base_salary | Other members of the Executive | 2434565 | Fail (hard) | CORE-03: quote not in the source text |
| materialise | controlling_owner_name |  | Wilfried Vancraen and Hilde In | Fail (hard) | CORE-02: not in the quote: and |
| materialise | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| materialise | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| materialise | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| materialise | sti_max | Other members of the Executive | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| mayr-melnhof-karton-ag-ef1c26e1 | staff_by_country |  | Poland: 3027; Germany: 2091; A | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mbb-se-be761dea | lti_target | Executive Chairman | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mbb-se-be761dea | lti_target | CFO | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| mcbride-plc-fd766eb4 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| mch-group-ag-c6fc7898 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| me-group-international-plc-174d99a5 | pension_contribution | Executive Director (from 3 Jun | 6678 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| me-group-international-plc-174d99a5 | total_remuneration | Executive Director (from 3 Jun | 87740 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| medartis-holding-ag-4ef02932 | shareholding_requirement |  | BoD: shares equal to one year  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| medartis-holding-ag-4ef02932 | sti_max | Other members of the EMB | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| medicon-hellas-s-a | benefits |  | Ομαδικό ιατροφαρμακευτικό πρόγ | Fail (hard) | CORE-03: quote not in the source text |
| medicon-hellas-s-a | revenue_by_country |  | Ελλάδα: 14961186.58; Ευρωπ. Έν | Fail (hard) | CORE-03: quote not in the source text |
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
| meridian-mining-plc-5760f027 | share_price |  | 0.385 | Fail (hard) | CORE-02: 0.385 not in the quote |
| meridian-mining-plc-5760f027 | total_assets |  | 46120968 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| merlin-properties-socimi-s-a | sub_sector |  | acquisition and management (th | Fail (hard) | CORE-03: quote not in the source text |
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
| metro-bank-holdings-plc-3ac1d88a | sti_max | Chief Executive Officer | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| metro-bank-holdings-plc-3ac1d88a | sti_max | Chief Financial Officer | 150 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| metro-bank-holdings-plc-3ac1d88a | sti_paid | Chief Executive Officer | 1177449 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | sti_paid | Chief Financial Officer | 636459 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | total_remuneration | Chief Executive Officer | 2665749 | Fail (hard) | CORE-03: quote not in the source text |
| metro-bank-holdings-plc-3ac1d88a | total_remuneration | Chief Financial Officer | 1199131 | Fail (hard) | CORE-03: quote not in the source text |
| michael-page-plc-f65a03eb | share_price |  | 2.35 | Fail (hard) | CORE-02: 2.35 not in the quote |
| mikron-holding-ag-0842218f | total_remuneration | CEO | 842000 | Fail (hard) | XF-01: parts add up to 860,000, more than the stated 842,000; XF-02: parts add up to 860,000, stated 842,000 |
| mila-resources-plc-585b51da | share_price |  | 0.01075 | Fail (hard) | CORE-02: 0.01075 not in the quote |
| mindmaze-therapeutics-holding-sa-b2339575 | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| mobilezone-holding-ag-fc013b59 | aggregate_headcount | Management Board | 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | benefits |  | lump-sum expenses approved by  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | role_disclosure | Executive Delegate of the Boar | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Management Board | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mobilezone-holding-ag-fc013b59 | sti_max | Executive Delegate of the Boar | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| molecular-partners-ag-86d659ae | pension_type |  | defined benefit plans; compuls | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mondi-plc-b3f2e211 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| mondo-tv | base_salary | Presidente e Amministratore De | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| mondo-tv | benefits_value | Presidente e Amministratore De | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| mondo-tv | lti_granted | Presidente e Amministratore De | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| mondo-tv | lti_vested | Presidente e Amministratore De | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| mondo-tv | sti_paid | Presidente e Amministratore De | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| montea | aggregate_headcount | Other members of the executive | 2 | Fail (hard) | CORE-03: quote not in the source text |
| montea | benefits_value | CEO | 5120 | Fail (hard) | CORE-03: quote not in the source text |
| montea | benefits_value | Other members of the executive | 19688 | Fail (hard) | CORE-03: quote not in the source text |
| montea | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| montea | lti_max | Other members of the executive | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| montea | pension_contribution | CEO | 41212 | Fail (hard) | CORE-03: quote not in the source text |
| montea | pension_contribution | Other members of the executive | 13285 | Fail (hard) | CORE-03: quote not in the source text |
| montea | sti_paid | CEO | 253453 | Fail (hard) | CORE-03: quote not in the source text |
| montea | sti_paid | Other members of the executive | 163249 | Fail (hard) | CORE-03: quote not in the source text |
| moonpig-group-plc-1a2a5dc2 | base_salary | Former CEO (until December 202 | 424552 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| moonpig-group-plc-1a2a5dc2 | benefits_value | Former CEO (until December 202 | 1543 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| moonpig-group-plc-1a2a5dc2 | lti_vested | CEO (from March 2026) | 604311 | Fail (hard) | CORE-02: 604311 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| moonpig-group-plc-1a2a5dc2 | pension_contribution | Former CEO (until December 202 | 21228 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | base_salary | Former CEO (until 1 July 2025) | 333785 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | benefits_value | Former CEO (until 1 July 2025) | 7447 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | benefits_value | CFO | 14023 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | lti_granted | CFO | 1825 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | lti_vested | Former CEO (until 1 July 2025) | 114064 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | lti_vested | CFO | 68610 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | pension_contribution | Former CEO (until 1 July 2025) | 26703 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | pension_contribution | CFO | 37878 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | total_remuneration | Former CEO (until 1 July 2025) | 767385 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| morgan-advanced-materials-plc-58a5cd32 | total_remuneration | CFO | 1000623 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| mota-engil-sgps-s-a | share_price |  | 4.948 | Fail (hard) | CORE-02: 4.948 not in the quote |
| motor-oil-hellas-corinth-refineries-s-a | staff_by_country |  | Greece: 2767; Bulgaria: 10; Cr | Fail | CORE-04: no period_end; NUM-08: adds up to 2,852 vs 4,503 (36.7% apart) |
| motor-oil-hellas-corinth-refineries-s-a | staff_by_segment |  | Senior Management: 99; Office- | Fail | CORE-04: no period_end; NUM-08: adds up to 2,852 vs 4,503 (36.7% apart) |
| moury-construct | aggregate_headcount | Autres dirigeants | 3.5 | Fail (hard) | NUM-05: not a whole number |
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
| nai-ord-shares | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| nanoco-group-plc-c86c4088 | benefits |  | life assurance of eight times  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nanoco-group-plc-c86c4088 | fte |  | 42 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 42 above headcount 38 |
| nanoco-group-plc-c86c4088 | lti_vested | Former CEO (until October 2024 | 49000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nanoco-group-plc-c86c4088 | pension_contribution | Former CEO (until October 2024 | 5000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nanoco-group-plc-c86c4088 | revenue_by_country |  | South Korea: 6272; Japan: 810; | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 7,558,000 vs 7,018,000 (7.7% apart) |
| national-bank-of-greece-s-a | controlling_owner |  | state | Fail (hard) | CORE-03: quote not in the source text |
| national-bank-of-greece-s-a | controlling_owner_name |  | HCAP | Fail (hard) | CORE-03: quote not in the source text |
| national-bank-of-greece-s-a | listing_date |  | 1880 | Fail (hard) | COD-06: not a year or a date |
| national-bank-of-greece-s-a | ownership_type |  | state_owned | Fail (hard) | CORE-03: quote not in the source text |
| national-grid-plc-08987e06 | fte |  | 32391 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| naturenergie-holding-ag-a1be2274 | pension_contribution | Geschäftsleitung | 156656 | Fail (hard) | CORE-02: 156656 not in the quote |
| naturgy-energy-group-s-a | base_salary | Executive Chairman | 1260000 | Fail (hard) | CORE-03: quote not in the source text |
| naturgy-energy-group-s-a | exchange |  | Bolsas Oficiales españolas | Fail (hard) | COD-01: 'Bolsas Oficiales españolas' matches no ISO 10383 exchange |
| naturgy-energy-group-s-a | lti_vested | Executive Chairman | 2763000 | Fail (hard) | CORE-03: quote not in the source text |
| naturgy-energy-group-s-a | revenue |  | 15000000000 | Fail (hard) | CORE-03: quote not in the source text |
| naturgy-energy-group-s-a | total_assets |  | 20800000000 | Fail (hard) | CORE-03: quote not in the source text |
| naturhouse-health-s-a | largest_holders |  | DON FÉLIX REVUELTA FERNÁNDEZ 7 | Fail (hard) | NUM-07: holdings add up to 156.36% |
| natwest-group-plc-0cca2e57 | shareholding_requirement |  | Group CEO – 500% of salary. Gr | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nepi-rockcastle | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| nepi-rockcastle | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| new-sources-energy | share_price |  | 0.015 | Fail (hard) | CORE-02: 0.015 not in the quote |
| new-sources-energy | staff_by_country |  | Netherlands: 1.8 | Fail | CORE-04: no period_end |
| ninety-one-plc-23209795 | listing_date |  | March 2020 | Fail (hard) | COD-06: not a year or a date |
| ninety-one-plc-23209795 | lti_granted | Chief Executive Officer | 634000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ninety-one-plc-23209795 | lti_granted | Finance Director | 508000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ninety-one-plc-23209795 | staff_by_segment |  | Investments: 281; Client group | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ninety-one-plc-23209795 | sti_paid | Chief Executive Officer | 1902000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ninety-one-plc-23209795 | sti_paid | Finance Director | 1522000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| norcros-plc-c8639b5b | lti_granted | Chief Financial Officer | 366080 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nostrum-oil-gas-plc-2662c1d0 | listing_date |  | March 2008 | Fail (hard) | COD-06: not a year or a date |
| nostrum-oil-gas-plc-2662c1d0 | lti_vested | CEO (until 30 June 2025) | 3357479 | Fail (hard) | CORE-02: 3357479 not in the quote |
| nsi-n-v | benefits_value | CEO | 4000 | Fail (hard) | CORE-02: 4 not in the quote |
| nsi-n-v | benefits_value | CFO (as from 1 May 2024) | 14000 | Fail (hard) | CORE-02: 14 not in the quote |
| nueva-expresion-textil-s-a | largest_holders |  | Businessgate, SL 59.49%; DON E | Fail (hard) | NUM-07: holdings add up to 178.805% |
| nuformix-plc-98385a38 | share_price |  | 0.09 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBx' is not ISO 4217 |
| nuformix-plc-98385a38 | shares_outstanding |  | 1995709368 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nyesa-valores-corporacion-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nyesa-valores-corporacion-s-a | listing_date |  | 2018 | Fail (hard) | CORE-02: not in the quote: 2018 |
| nyesa-valores-corporacion-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| nyxoah | lti_granted | Other members of executive man | 25000 | Fail (hard) | CORE-02: 25000 not in the quote |
| nyxoah | lti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| nyxoah | lti_target | Other members of executive man | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| nyxoah | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Chairman of the Executive Boar | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Energ | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Executive Vice President Fuels | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Vice Presiden | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Deputy Chairman of the  | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| omv-ag-2c5e8b21 | lti_target | Former Executive Officer Marke | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| ondo-insurtech-plc-e2c31efb | ebitda |  | -6417000 | Fail (hard) | CORE-02: -6.417 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| ondo-insurtech-plc-e2c31efb | revenue |  | 4645000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| onyx-touristiki-societe-anonyme | base_salary | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| onyx-touristiki-societe-anonyme | benefits_value | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| onyx-touristiki-societe-anonyme | revenue_by_segment |  | Ένδυση: 2286057 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| onyx-touristiki-societe-anonyme | sti_max | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | sti_max | Εκτελεστικό Μέλος (until 18/12 | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | sti_max | Επικεφαλής Μονάδας Εσωτερικού  | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | total_remuneration | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| orange-belgium | benefits_value | CEO | 358681 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| orior-ag-bfeb91d6 | aggregate_headcount | Executive Committee excl. CFO | 3.1 | Fail (hard) | NUM-05: not a whole number |
| orior-ag-bfeb91d6 | aggregate_headcount | Former Executive Committee mem | 0.4 | Fail (hard) | NUM-04: 0.4 outside 1..500; NUM-05: not a whole number |
| osb-group-plc-0972698d | sti_paid | CEO | 678000 | Fail (hard) | CORE-02: 678 not in the quote |
| osb-group-plc-0972698d | sti_paid | CFO | 406000 | Fail (hard) | CORE-02: 406 not in the quote |
| ostasiatiske | exchange |  | NASDAQ Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ Copenhagen A/S' matches no ISO 10383 exchange |
| ovs | controlling_owner_name |  | Tamburi Investment Partners S. | Fail (hard) | CORE-02: not in the quote: tamburi investment partners |
| oxford-nanopore-technologies-plc-0e6547be | share_price |  | 1.284 | Fail (hard) | CORE-02: 1.284 not in the quote |
| palfinger-ag-e07e19f6 | exchange_segment |  | Prime Market | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| palfinger-ag-e07e19f6 | revenue_by_country |  | Inland: 44423.1; EU: 21235.8;  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 77,550,800 vs 2,339,288,000 (96.7% apart) |
| palfinger-ag-e07e19f6 | staff_by_country |  | Österreich: 2707; Russland: 15 | Fail | CORE-04: no period_end; NUM-08: adds up to 5,657 vs 12,358 (54.2% apart) |
| pan-african-resources-plc-e4db7ca3 | base_salary | Other Prescribed Officers | 719000 | Fail (hard) | CORE-02: 719 not in the quote |
| pan-african-resources-plc-e4db7ca3 | benefits_value | Other Prescribed Officers | 39000 | Fail (hard) | CORE-02: 39 not in the quote |
| pan-african-resources-plc-e4db7ca3 | lti_vested | Other Prescribed Officers | 1201000 | Fail (hard) | CORE-02: 1201 not in the quote |
| pan-african-resources-plc-e4db7ca3 | sti_paid | Other Prescribed Officers | 355000 | Fail (hard) | CORE-02: 355 not in the quote |
| pan-african-resources-plc-e4db7ca3 | total_remuneration | Other Prescribed Officers | 2322000 | Fail (hard) | CORE-02: 2322 not in the quote |
| papoutsanis-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| papoutsanis-s-a | shares_outstanding |  | 26944438 | Fail (hard) | CORE-03: quote not in the source text |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| partners-group-holding-ag-d09fd15d | lti_granted | Chief Executive Officer | 14055000 | Fail (hard) | CORE-02: 14055 not in the quote |
| partners-group-holding-ag-d09fd15d | lti_granted | Executive Team | 54733000 | Fail (hard) | CORE-02: 54733 not in the quote |
| partners-group-holding-ag-d09fd15d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| path2-hydrogen-ag-4a522574 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| patrizia-se-41659152 | revenue_by_segment |  | Investment Management: 264348; | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 276,070,000 vs 258,416,000 (6.8% apart) |
| pb-holding | controlling_owner_name |  | Nafimij B.V. | Fail (hard) | CORE-02: not in the quote: b v |
| pb-holding | fte |  | 2100 | Fail | CORE-04: no period_end; NUM-13: FTE 2,100 above headcount 1 |
| pb-holding | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| pb-holding | ultimate_parent |  | Nafimij B.V. | Fail (hard) | CORE-02: not in the quote: v |
| pearl-gold-ag-da4e9b62 | listing_date |  | 2012-09 | Fail (hard) | COD-06: not a year or a date |
| pearl-gold-ag-da4e9b62 | pension_type |  | Ruhegehalts- und Vorruhestands | Fail (hard) | CORE-03: quote not in the source text |
| pennon-group-plc-7143cdb4 | sti_paid | CEO (until 31 December 2025) | 17.5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| pensana-plc-3caf2324 | share_price |  | 122.1 | Fail (hard) | NUM-01: unit 'USD cents' is not ISO 4217 |
| performance-technologies-s-a | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| performance-technologies-s-a | role_disclosure | Εκτελεστικό Μέλος, Αντιπρόεδρο | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| performance-technologies-s-a | role_disclosure | Εκτελεστικό Μέλος, Πρόεδρος &  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| performance-technologies-s-a | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| persimmon-plc-03d19fa0 | benefits_value | CFO | 11452 | Fail (hard) | CORE-02: 11452 not in the quote |
| pescanova-s-a | staff_by_country |  | Argentina: 727; Namibia: 377;  | Fail | CORE-04: no period_end; NUM-08: adds up to 5,932 vs 12,312 (51.8% apart) |
| pescanova-s-a | staff_by_segment |  | FISHING: 1599; AQUACULTURE: 46 | Fail | CORE-04: no period_end; NUM-08: adds up to 10,134 vs 12,312 (17.7% apart) |
| petra-diamonds-limited-5f8d5389 | benefits_value | Former Chief Executive Officer | 47853 | Fail (hard) | CORE-02: 47853 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| petra-diamonds-limited-5f8d5389 | benefits_value | Former Chief Financial Officer | 93950 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| petra-diamonds-limited-5f8d5389 | lti_vested | Former Chief Executive Officer | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| petra-diamonds-limited-5f8d5389 | lti_vested | Former Chief Financial Officer | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| petra-diamonds-limited-5f8d5389 | pension_contribution | Former Chief Financial Officer | 8089 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| petra-diamonds-limited-5f8d5389 | total_remuneration | Former Chief Executive Officer | 347597 | Fail (hard) | CORE-02: 347597 not in the quote |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| pfeiffer-vacuum-tech-ag-a38e65f0 | controlling_owner_name |  | Busch Group | Fail (hard) | CORE-02: not in the quote: group |
| pfeiffer-vacuum-tech-ag-a38e65f0 | staff_by_segment |  | Deutschland: 990; Frankreich:  | Fail | CORE-04: no period_end; NUM-08: adds up to 1,815 vs 3,847 (52.8% apart) |
| pferdewetten-de-ag-07705286 | aggregate_headcount | Vorstand | 3 | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | benefits |  | Dienstwagen, Mobilitätszulage, | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | shareholding_requirement |  | CEO and Prokurist received loa | Fail (hard) | CORE-03: quote not in the source text |
| pferdewetten-de-ag-07705286 | website |  | pferdewetten.ag | Fail (hard) | CORE-03: quote not in the source text |
| pharma-mar-s-a | total_remuneration | Executive Chairman | 3125807000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pharma-mar-s-a | total_remuneration | Executive Vice-Chairman | 577000 | Fail (hard) | XF-01: parts add up to 12,597,000, more than the stated 577,000; XF-02: parts add up to 12,597,000, stated 577,000 |
| pharmanutra | base_salary | Amministratore esecutivo (Germ | 342292.81 | Fail (hard) | CORE-02: 342292.81 not in the quote |
| pharmanutra | total_remuneration | Presidente e amministratore es | 2592600 | Fail (hard) | XF-01: parts add up to 2,848,860, more than the stated 2,592,600; XF-02: parts add up to 2,848,860, stated 2,592,600 |
| pharmanutra | total_remuneration | Vice Presidente e amministrato | 2328600 | Fail (hard) | XF-01: parts add up to 2,558,460, more than the stated 2,328,600; XF-02: parts add up to 2,558,460, stated 2,328,600 |
| pharmanutra | total_remuneration | Amministratore esecutivo (Carl | 2148600 | Fail (hard) | XF-01: parts add up to 2,360,460, more than the stated 2,148,600; XF-02: parts add up to 2,360,460, stated 2,148,600 |
| pharmanutra | total_remuneration | Amministratore esecutivo (Germ | 646492.81 | Fail (hard) | XF-01: parts add up to 700,913, more than the stated 646,493; XF-02: parts add up to 700,913, stated 646,493 |
| philippos-nakas-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| philippos-nakas-s-a | role_disclosure | Διευθυντικά στελέγη (1) | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| phoenix-mecano-ag-d882ab5c | sti_max | Chairman of the Board of Direc | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | CEO | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| piaggio | fte |  | 5745.7 | Fail (hard) | CORE-03: quote not in the source text |
| piaggio | other_names |  | Società Rinaldo Piaggio; Piagg | Fail (hard) | CORE-03: quote not in the source text |
| piaggio | share_price |  | 1.822 | Fail (hard) | CORE-02: 1.822 not in the quote |
| pininfarina | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| pipe-works-l-girakian-profil-s-a | revenue_by_segment |  | Κατασκευή χαλυβδοσωλήνων: 1886 | Fail (hard) | CORE-03: quote not in the source text |
| piraeus-port-authority-s-a | revenue_by_segment |  | Cruise: 9; Coastal Shipping: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 250,800,000 vs 230,878,455 (8.6% apart) |
| pittler-maschinenfabrik-ag-fb62b449 | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| pittler-maschinenfabrik-ag-fb62b449 | benefits_value | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | controlling_owner_name |  | Herr Günter Rothenberger | Fail (hard) | CORE-02: not in the quote: nter |
| planoptik-ag-9429909d | benefits |  | Zuschüsse zur Kranken- und Pfl | Fail (hard) | CORE-03: quote not in the source text |
| planoptik-ag-9429909d | sti_target | Member of the Management Board | 10 | Fail (hard) | COD-01: unit '' is not a target form |
| plastika-kritis-s-a | accounting_basis |  | Διεθνή Πρότυπα Χρηματοοικονομι | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| plastika-kritis-s-a | staff_by_country |  | Ελλάδα: 504; Πολωνία: 128; Ρου | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| plastika-kritis-s-a | ticker |  | PLAKR | Fail (hard) | CORE-02: not in the quote: plakr |
| playtech-plc-4d633d69 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| plus500-ltd-c1762b4f | benefits_value | CEO | 206000 | Fail (hard) | CORE-02: 206 not in the quote |
| plus500-ltd-c1762b4f | benefits_value | CFO | 206000 | Fail (hard) | CORE-02: 206 not in the quote |
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
| porceleyne-fles | base_salary | Director (until May 2025) | 104000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porceleyne-fles | pension_contribution | Director (until May 2025) | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| porceleyne-fles | sti_paid | Director (until May 2025) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| poste-italiane | revenue_by_segment |  | Mail, Parcel and Distribution: | Fail | CORE-04: no period_end; NUM-08: adds up to 14,150,000,000 vs 13,120,000,000 (7.9% apart) |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | President & Co-CEO | 17116 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | Co-CEO | 4521 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | benefits_value | CFO | 17835 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | listing_date |  | 2007 | Fail (hard) | CORE-02: not in the quote: 2007 |
| pphe-hotel-group-limited-8368d7b3 | other_names |  | Park Plaza Hotels Limited | Fail (hard) | CORE-02: not in the quote: park plaza limited |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | President & Co-CEO | 29429 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | Co-CEO | 26189 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | pension_contribution | CFO | 19313 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | President & Co-CEO | 755119 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | Co-CEO | 890014 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| pphe-hotel-group-limited-8368d7b3 | total_remuneration | CFO | 871592 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| predator-oil-gas-holdings-plc-0ba3277f | share_price |  | 0.00875 | Fail (hard) | CORE-02: 0.875 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| princes-group-plc-95096765 | revenue_by_segment |  | Foods: 623181; Fish: 350992; I | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| procook-group-plc-45a2e6f4 | listing_date |  | 2021-11 | Fail (hard) | COD-06: not a year or a date |
| procook-group-plc-45a2e6f4 | staff_by_country |  | UK: 600 | Fail | CORE-04: no period_end; NUM-08: adds up to 600 vs 729 (17.7% apart) |
| procredit-holding-ag-74495a3c | headcount |  | 4660 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| procredit-holding-ag-74495a3c | listing_date |  | 2016-12-22 | Fail (hard) | CORE-02: not in the quote: 2016 |
| procredit-holding-ag-74495a3c | revenue_by_segment |  | South Eastern Europe: 319141;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 565,433,000 vs 439,266,000 (28.7% apart) |
| procredit-holding-ag-74495a3c | website |  | procredit-holding.com | Fail (hard) | CORE-02: not in the quote: procredit holding |
| promotora-de-informaciones-s-a | benefits |  | Seguros de salud y vida/accide | Fail (hard) | CORE-03: quote not in the source text |
| promotora-de-informaciones-s-a | revenue_by_country |  | Europa: 358072; España: 358072 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,808,670,000 vs 883,172,000 (104.8% apart) |
| promotora-de-informaciones-s-a | share_price |  | 0.355 | Fail (hard) | CORE-02: 0.355 not in the quote |
| prosus | base_salary | Chief Financial Officer | 1008000 | Fail (hard) | CORE-03: quote not in the source text |
| prosus | benefits_value | Chief Financial Officer | 97000 | Fail (hard) | CORE-03: quote not in the source text |
| prosus | lti_granted | Chief Financial Officer | 3993000 | Fail (hard) | CORE-03: quote not in the source text |
| prosus | pension_contribution | Chief Financial Officer | 147000 | Fail (hard) | CORE-03: quote not in the source text |
| prosus | sti_paid | Chief Financial Officer | 634000 | Fail (hard) | CORE-03: quote not in the source text |
| prosus | total_remuneration | Chief Financial Officer | 5879000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | benefits_value | Chief Executive Officer | 635000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | lti_vested | Chief Executive Officer | 3581000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | pension_contribution | Chief Executive Officer | 207000 | Fail (hard) | CORE-03: quote not in the source text |
| prudential-plc-c6ad5538 | revenue_by_segment |  | Hong Kong: 2221; Indonesia: 25 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 6,990,000,000 vs 11,080,000,000 (36.9% apart) |
| prudential-plc-c6ad5538 | sti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| public-property-invest | largest_holders |  | Samhällsbyggnadsbolaget i Nord | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| public-property-invest | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| puretech-health-plc-df8e539a | share_price |  | 1.204 | Fail (hard) | CORE-02: 1.204 not in the quote |
| pz-cussons-plc-a434b740 | shareholding_requirement |  | Executive Directors: 200% of s | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| qev | revenue_by_country |  | Sweden: 4144785; Spain: 251881 | Fail | CORE-04: no period_end; NUM-08: adds up to 13,446,829 vs 22,991,751 (41.5% apart) |
| qinetiq-group-plc-f5a9622e | lti_vested | CFO | 624000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| qrf | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| qualco-group-s-a | controlling_owner_name |  | Wokalon Finances Limited | Fail (hard) | CORE-02: not in the quote: finances limited |
| qualco-group-s-a | ultimate_parent |  | Wokalon Finances Limited | Fail (hard) | CORE-02: not in the quote: finances limited |
| quantum-data-energy-plc-52f9bd33 | listing_date |  | April 2021 | Fail (hard) | COD-06: not a year or a date |
| quest-holdings-s-a | base_salary | Managing Director Executive Me | 537400 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | base_salary | Deputy Managing Director Execu | 397000 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | benefits |  | ιατροφαρμακευτική και νοσοκομε | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | benefits_value | Chairman - Executive Member | 56200 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | benefits_value | Managing Director Executive Me | 25400 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | benefits_value | Deputy Managing Director Execu | 13700 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | pension_type |  | group pension scheme, a volunt | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | sti_paid | Managing Director Executive Me | 772100 | Fail (hard) | CORE-03: quote not in the source text |
| quest-holdings-s-a | sti_paid | Deputy Managing Director Execu | 388800 | Fail (hard) | CORE-03: quote not in the source text |
| r-e-a-holdings-plc-5b9a0020 | fte |  | 8124 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-e-a-holdings-plc-5b9a0020 | revenue_by_segment |  | Plantations: 193; Stone and sa | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-e-a-holdings-plc-5b9a0020 | staff_by_country |  | Indonesia: 7894; UK: 6 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | lti_target | Vorstandsvorsitzender (until D | 250000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | lti_target | Mitglied des Vorstands | 130000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| r-stahl-ag-04fdadc0 | role_disclosure | Former Executives, total | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| ramada-investimentos-e-industria-s-a | lti_max | executivo | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ramada-investimentos-e-industria-s-a | lti_max | executiva | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ramada-investimentos-e-industria-s-a | sti_max | executivo | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| ramada-investimentos-e-industria-s-a | sti_max | executiva | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| rank-group-plc-26f67d4c | lti_granted | Chief Financial Officer | 514485 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| raspberry-pi-holdings-plc-d0b387d0 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| raspberry-pi-holdings-plc-d0b387d0 | share_price |  | 3.002 | Fail (hard) | CORE-02: 3.002 not in the quote |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | base_salary | Member of the Management Board | 290000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | benefits_value | Member of the Management Board | 10000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | sti_paid | Member of the Management Board | 44000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 349000 | Fail (hard) | XF-01: parts add up to 364,000, more than the stated 349,000; XF-02: parts add up to 364,000, stated 349,000 |
| rath-ag-9e9ac567 | total_remuneration | Member of the Management Board | 419000 | Fail (hard) | XF-01: parts add up to 429,000, more than the stated 419,000; XF-02: parts add up to 429,000, stated 419,000 |
| rathbones-group-plc-272d1adc | pension_type |  | defined contribution, defined  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rc365-holding-plc-1f4ebdbd | largest_holders |  | LYS Limited 17.3%; Alvar Finan | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rc365-holding-plc-1f4ebdbd | listing_date |  | March 2022 | Fail (hard) | COD-06: not a year or a date |
| rc365-holding-plc-1f4ebdbd | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rc365-holding-plc-1f4ebdbd | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rcs-mediagroup | staff_by_country |  | Italia: 1781; Spagna: 1083; Al | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| reach-plc-e8816dd8 | lti_vested | CFO | 177186 | Fail (hard) | CORE-02: 177186 not in the quote |
| readcrest-capital-ag-e4689651 | fte |  | 0 | Fail | CORE-04: no period_end; NUM-04: 0 outside 0.5..5e+06 |
| readcrest-capital-ag-e4689651 | revenue_by_segment |  | Pflegedienstleistungen: 128309 | Fail (hard) | CORE-03: quote not in the source text |
| realia-business-s-a | ebitda |  | 149982000 | Fail (hard) | CORE-02: 149982 not in the quote |
| record-plc-8e9102d2 | lti_granted | CEO | 4042000 | Fail (hard) | CORE-02: 4042000 not in the quote |
| record-plc-8e9102d2 | lti_granted | Executive Director (until 31 M | 2204000 | Fail (hard) | CORE-02: 2204000 not in the quote |
| record-plc-8e9102d2 | lti_granted | Executive Director (from 1 Jul | 1654000 | Fail (hard) | CORE-02: 1654000 not in the quote |
| recticel | base_salary | CEO | 671360 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | base_salary | Other members of the Managemen | 1983039 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | benefits_value | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | controlling_owner_name |  | SpringHoldco BV | Fail (hard) | CORE-02: not in the quote: springholdco |
| recticel | exchange |  | Euronext | Fail (hard) | COD-01: 'Euronext' matches no ISO 10383 exchange |
| recticel | lti_received | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | lti_received | Other members of the Managemen | 0 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | other_names |  | Cooppal; PRB; Gechem | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| recticel | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| recticel | pay_currency | Other members of the Managemen | EUR | Fail | CORE-04: no period_end |
| recticel | pension_contribution | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | pension_contribution | Other members of the Managemen | 98524 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | sti_paid | CEO | 468959 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | sti_paid | Other members of the Managemen | 646713 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | total_remuneration | CEO | 1140319 | Fail (hard) | CORE-03: quote not in the source text |
| recticel | total_remuneration | Other members of the Managemen | 2929820 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,804,820, stated 2,929,820 |
| redeia-corporacion-s-a | sub_sector |  | Its core activities comprise t | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| redeia-corporacion-s-a | ticker |  | REE | Fail (hard) | CORE-02: not in the quote: ree |
| relx-plc-28248427 | sti_paid | CEO | 2338000 | Fail (hard) | CORE-02: 2338 not in the quote |
| renishaw-plc-02f27561 | total_remuneration | Group Finance Director (until  | 268000 | Fail (hard) | XF-01: parts add up to 562,000, more than the stated 268,000; XF-02: parts add up to 562,000, stated 268,000 |
| rentokil-initial-plc-8eff6540 | lti_vested | Former Chief Financial Officer | 436700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| repsol-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| repsol-s-a | headcount |  | 2954 | Fail (hard) | CORE-03: quote not in the source text |
| repsol-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| repsol-s-a | revenue_by_segment |  | Upstream: 2266; Industrial: 27 | Fail | CORE-04: no period_end; NUM-08: adds up to 33,948,000,000 vs 54,421,000,000 (37.6% apart) |
| repsol-s-a | share_price |  | 15.925 | Fail (hard) | CORE-02: 15.925 not in the quote |
| retail-estates | lti_target | Other members of the managemen | 15 | Fail (hard) | CORE-02: 15 not in the quote |
| revo-insurance | revenue_by_country |  | Italia: 379931; Estero (tra cu | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 398,121,000 vs 287,519,000 (38.5% apart) |
| rheinmetall-ag-cf2ff08a | sti_max | Vorsitzender des Vorstands | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (seit 1 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rheinmetall-ag-cf2ff08a | sti_max | Mitglied des Vorstands (bis 31 | 250 | Fail (hard) | CORE-02: 250 not in the quote |
| rhi-magnesita-n-v-fb7495f7 | headcount |  | 15913 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rhi-magnesita-n-v-fb7495f7 | sub_sector |  | RHI Magnesita is a global supp | Fail (hard) | CORE-03: quote not in the source text |
| rhoen-klinikum-0a013089 | role_disclosure | Vorstandsvorsitzender (ab 1. N | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| rs-group-plc-9ec766f0 | benefits_value | CFO | 16252000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rs-group-plc-9ec766f0 | pension_contribution | CFO | 47093000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| rs-group-plc-9ec766f0 | sti_paid | CFO | 417729000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s-d-standard-etc | controlling_owner_name |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-d-standard-etc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| s-d-standard-etc | share_price |  | 1.688 | Fail (hard) | CORE-02: 1.688 not in the quote |
| s-d-standard-etc | ultimate_parent |  | Saga Pure ASA | Fail (hard) | CORE-02: not in the quote: asa |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Anthony Co | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Graham Coo | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Jack Coomb | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s-u-plc-d076a510 | role_disclosure | Executive Director (Ed Ahrens) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s-u-plc-d076a510 | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| s4-capital-plc-c1328a0a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| sacyr-s-a | revenue |  | 4660000000 | Fail (hard) | CORE-02: 4660 not in the quote |
| sacyr-s-a | share_price |  | 3.866 | Fail (hard) | CORE-02: 3.866 not in the quote |
| saf-holland-se-e07079b5 | other_names |  | Otto Sauer Achsenfabrik GmbH;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| saf-holland-se-e07079b5 | staff_by_country |  | EMEA: 2282; Americas: 2480; AP | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| safestore-holdings-plc-c17fb612 | base_salary | CEO | 665000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | benefits_value | CEO | 25000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | benefits_value | CFO | 25000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | lti_vested | CEO | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | lti_vested | CFO | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | pension_contribution | CEO | 27000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | pension_contribution | CFO | 18000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| safestore-holdings-plc-c17fb612 | sti_paid | CEO | 582000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| saga-plc-3572ddce | lti_granted | Executive Director (previously | 422300 | Fail (hard) | CORE-02: 422300 not in the quote |
| saga-plc-3572ddce | lti_vested | Group Chief Executive Officer  | 615000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| saga-plc-3572ddce | pension_type |  | defined contribution | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sainsbury-j-plc-5943ac28 | fte |  | 91000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sainsbury-j-plc-5943ac28 | headcount |  | 142000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sainsbury-j-plc-5943ac28 | revenue_by_segment |  | Grocery, general merchandise a | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | fiscal_year_end |  | YYYY-12-31 | Fail (hard) | COD-06: not a valid date |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | pay_currency | Executive Management | CHF | Fail | CORE-04: no period_end |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | revenue_by_country |  | Europe: 11577; North America:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
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
| sap-se-b1a5f6d4 | role_disclosure | Member of the Executive Board  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sap-se-b1a5f6d4 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| sap-se-b1a5f6d4 | total_remuneration | CEO | 16244000 | Fail (hard) | XF-01: parts add up to 18,145,000, more than the stated 16,244,000; XF-02: parts add up to 18,145,000, stated 16,244,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2246000 | Fail (hard) | XF-01: parts add up to 3,256,000, more than the stated 2,246,000; XF-02: parts add up to 3,256,000, stated 2,246,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2531000 | Fail (hard) | XF-01: parts add up to 3,286,000, more than the stated 2,531,000; XF-02: parts add up to 3,286,000, stated 2,531,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 7044000 | Fail (hard) | XF-01: parts add up to 7,908,000, more than the stated 7,044,000; XF-02: parts add up to 7,908,000, stated 7,044,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2131000 | Fail (hard) | XF-01: parts add up to 2,728,000, more than the stated 2,131,000; XF-02: parts add up to 2,728,000, stated 2,131,000 |
| sap-se-b1a5f6d4 | total_remuneration | Member of the Executive Board  | 2524000 | Fail (hard) | XF-01: parts add up to 2,983,000, more than the stated 2,524,000; XF-02: parts add up to 2,983,000, stated 2,524,000 |
| sartorius-ag-9a9c739c | lti_vested | Executive Board Member (Dr. Re | 186000 | Fail (hard) | CORE-02: 186 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Chairma | 288000 | Fail (hard) | CORE-02: 288 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Member  | 179000 | Fail (hard) | CORE-02: 179 not in the quote |
| sartorius-ag-9a9c739c | lti_vested | Former Executive Board Member  | 186000 | Fail (hard) | CORE-02: 186 not in the quote |
| sartorius-ag-a22309c5 | benefits |  | company car, accident insuranc | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sartorius-ag-a22309c5 | pension_type |  | defined-benefit plans; base am | Fail (hard) | CORE-03: quote not in the source text |
| sartorius-ag-a22309c5 | total_remuneration | Former Executive Board Chairma | 2341000 | Fail (hard) | XF-01: parts add up to 2,695,000, more than the stated 2,341,000; XF-02: parts add up to 2,695,000, stated 2,341,000 |
| savills-plc-159e730d | sti_target | Group Chief Executive Officer  | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| savills-plc-159e730d | sti_target | Group Chief Financial Officer  | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
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
| schott-pharma-ag-co-kgaa-26f01ea5 | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| schweiter-technologies-ag-b9dd7eca | aggregate_headcount | Group Management | 2 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | Group Management | 232000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | CEO | 143000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| schweiter-technologies-ag-b9dd7eca | shareholding_requirement |  | Share-based compensation for B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sealand-capital-galaxy-limited-126bc181 | fte |  | 4 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sealand-capital-galaxy-limited-126bc181 | headcount |  | 4 | Fail (hard) | CORE-02: 4 not in the quote |
| seb-a | total_remuneration | Other members of the Group Exe | 85984864 | Fail (hard) | XF-01: parts add up to 105,243,201, more than the stated 85,984,864; XF-02: parts add up to 105,243,201, stated 85,984,864 |
| seb-c | revenue |  | -411000 | Fail | CORE-04: no period_end; NUM-04: -411000 outside 0..1e+14 |
| seb-c | revenue_by_country |  | Sweden: 46498; Norway: 4315; D | Fail | CORE-04: no period_end; NUM-08: adds up to 76,903,000,000 vs -411,000 (18711292.2% apart) |
| seb-c | revenue_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 76,928,000,000 vs -411,000 (18717374.9% apart) |
| seb-c | staff_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 11,889 vs 189 (6190.5% apart) |
| seb-c | total_remuneration | VD samt vice VD | -8931000 | Fail (hard) | NUM-04: -8.931e+06 outside 0..5e+10; XF-01: parts add up to -8,931,000, more than the stated -8,931,000 |
| seb-c | total_remuneration | Risktagare | -24486000 | Fail (hard) | NUM-04: -2.4486e+07 outside 0..5e+10; XF-01: parts add up to -24,486,000, more than the stated -24,486,000 |
| seb-c | total_remuneration | Övriga | -157650000 | Fail (hard) | NUM-04: -1.5765e+08 outside 0..5e+10; XF-01: parts add up to -157,651,000, more than the stated -157,650,000 |
| secunet-security-ag-c4d9b7e4 | headcount |  | 1171 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| secunet-security-ag-c4d9b7e4 | total_assets |  | 410700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| semapa-sociedade-de-investimento-e-gestao-sgps-s-a | share_price |  | 20.9 | Fail (hard) | CORE-02: 20.9 not in the quote |
| semperit-ag-holding-2a7b594a | listing_date |  | 1890 | Fail (hard) | COD-06: not a year or a date |
| sensirion-holding-ag-0c2fb93b | base_salary | CEO | 444184 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | base_salary | Other EC | 1213918 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | role_disclosure | CEO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | role_disclosure | Other EC | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | sti_paid | CEO | 102168 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | sti_paid | Other EC | 252170 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | total_remuneration | CEO | 628853 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sensirion-holding-ag-0c2fb93b | total_remuneration | Other EC | 1686136 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 1,466,088, stated 1,686,136 |
| sentia | revenue_by_country |  | Norway: 9404; Sweden: 2369 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| serco-group-plc-96a15710 | benefits_value | Group Chief Financial Officer | 52599 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| serco-group-plc-96a15710 | lti_vested | Group Chief Financial Officer | 1390285 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| serco-group-plc-96a15710 | pension_contribution | Group Chief Financial Officer | 40368 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| serco-group-plc-96a15710 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| serco-group-plc-96a15710 | sti_paid | Group Chief Financial Officer | 636820 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| serco-group-plc-96a15710 | total_remuneration | Group Chief Financial Officer | 2624669 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seri-industrial | exchange_segment |  | main market EXM | Fail (hard) | CORE-02: not in the quote: main market |
| seri-industrial | staff_by_segment |  | Batteries: 450; Plastic Materi | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 1,270 vs 1,339 (5.2% apart) |
| severfield-plc-598e26e7 | pension_contribution | Chief Executive Officer (from  | 15000000 | Fail (hard) | CORE-02: 15000 not in the quote |
| severfield-plc-598e26e7 | total_remuneration | Chief Executive Officer (from  | 335000000 | Fail (hard) | CORE-02: 335000 not in the quote; XF-02: parts add up to 15,840,000, stated 335,000,000 |
| severn-trent-plc-2f585ef6 | benefits_value | CEO (from 1 January 2026) | 5700 | Fail (hard) | CORE-02: 5.7 not in the quote |
| sgs-ag-65380806 | aggregate_headcount | Other ExCo | 13 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | benefits_value | Chief Executive Officer | 24000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | pension_contribution | Chief Executive Officer | 119000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sgs-ag-65380806 | revenue_by_country |  | North America: 1.5 | Fail | CORE-04: no period_end |
| sgs-ag-65380806 | total_remuneration | Chief Executive Officer | 1393000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 4,355,000, more than the stated 1,393,000; XF-02: parts add up to 4,355,000, stated 1,393,000 |
| shaftesbury-capital-plc-1cc22072 | pension_type |  | defined contribution, 17.5 per | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| shawbrook-group-plc-d45cea57 | revenue_by_country |  | UK: 682.1 | Fail | CORE-04: no period_end; NUM-08: adds up to 682,100,000 vs 1,421,900,000 (52.0% apart) |
| shawbrook-group-plc-d45cea57 | share_price |  | 4.86 | Fail (hard) | CORE-02: 4.86 not in the quote |
| sidma-steel-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| siemens-health-ag-1a42fb66 | revenue_by_country |  | Europe, C.I.S., Africa, Middle | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| siemens-health-ag-1a42fb66 | sub_sector |  | Siemens Healthineers offers im | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| sig-plc-36f9635a | pension_contribution | Previous CEO (until 8 July 202 | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| sig-plc-36f9635a | pension_contribution | CFO | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| sig-plc-36f9635a | sti_max | CEO (from 1 October 2025) | 0 | Fail (hard) | COD-01: unit '' is not a target form |
| singulus-technol-66103de1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| singulus-technol-66103de1 | controlling_owner_name |  | Triumph Science & Technology G | Fail (hard) | CORE-03: quote not in the source text |
| singulus-technol-66103de1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| sino-german-united-ag-388acb2d | benefits |  | D&O-Versicherung, D&O Selbstbe | Fail (hard) | CORE-03: quote not in the source text |
| sino-german-united-ag-388acb2d | role_disclosure | Vorstand/Chief Operating Offic | individual | Fail (hard) | CORE-03: quote not in the source text |
| sipef | sti_max | Managing director | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sipef | sti_max | Former Managing Director (unti | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sipef | sti_max | Chief financial officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sipef | sti_max | Former member of the executive | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sipef | sti_max | Former member of the executive | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sipef | sti_max | Chief commercial officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| sirius-real-estate-limited-9190d4f5 | share_price |  | 0.926 | Fail (hard) | CORE-02: 0.926 not in the quote |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 44000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | benefits_value | Co-Vorsitzender des Vorstands  | 39000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | benefits_value | COO | 32000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | benefits_value | CBO | 28000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | benefits_value | CFO | 28000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | Co-Vorsitzender des Vorstands  | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | COO | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | sti_paid | Co-Vorsitzender des Vorstands  | 1411000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | sti_paid | COO | 347000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | sti_paid | CBO | 246000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| sixt-se-8094cf8b | sti_paid | CFO | 198000 | Fail (hard) | CORE-03: quote on page 4, link says page 2 |
| skan-group-ag-684bb9fa | sti_paid | CEO | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sligro-food-group | shareholding_requirement |  | A long-term bonus of 30% of th | Fail (hard) | CORE-03: quote not in the source text |
| smg-swiss-marketplace-group-holding-ag-40385dff | revenue_by_segment |  | Real Estate: 164147; Automotiv | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| smiths-group-plc-74ee79d4 | benefits_value | CEO | 42000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| smiths-group-plc-74ee79d4 | benefits_value | Chief Financial Officer | 26000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| smiths-group-plc-74ee79d4 | pension_contribution | CEO | 120000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| smiths-group-plc-74ee79d4 | pension_contribution | Chief Financial Officer | 77000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| snam | share_price |  | 5.656 | Fail (hard) | CORE-02: 5.656 not in the quote |
| snam | staff_by_country |  | Northern Italy: 2995; Central  | Fail (hard) | CORE-03: quote not in the source text |
| snp-schneider-neureither-f82bee76 | fiscal_year_end |  | 2023-12-31 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| snp-schneider-neureither-f82bee76 | headcount |  | 1500 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| snp-schneider-neureither-f82bee76 | revenue |  | 203400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softing-ag-365a9352 | share_price |  | 2.62 | Fail (hard) | CORE-03: quote not in the source text |
| softwareone-holding-ag-ee2860ae | lti_granted | CFO (until May 31, 2025) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softwareone-holding-ag-ee2860ae | lti_granted | Other EB members | 1320250 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| softwareone-holding-ag-ee2860ae | lti_target | Other EB members | 27 | Fail (hard) | COD-01: unit '' is not a target form |
| softwareone-holding-ag-ee2860ae | sti_target | Other EB members | 22 | Fail (hard) | COD-01: unit '' is not a target form |
| soltec-power-holdings-s-a | controlling_owner_name |  | DVCP I RAIF SICAV SCA – DVCP R | Fail (hard) | CORE-02: not in the quote: dvcp raif sicav sca dvcp renewable |
| soltec-power-holdings-s-a | exchange_segment |  | Mercado Continuo | Fail (hard) | CORE-02: not in the quote: mercado continuo |
| solvay | benefits |  | company car or vehicle allowan | Fail (hard) | CORE-03: quote not in the source text |
| solvay | shareholding_requirement |  | Non-executive directors: share | Fail (hard) | CORE-03: quote not in the source text |
| somec | staff_by_segment |  | Horizons: sistemi ingegnerizza | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 607 vs 995 (39.0% apart) |
| sonaecom-sgps-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sonaecom-sgps-s-a | share_price |  | 2.8 | Fail (hard) | CORE-02: 2.8 not in the quote |
| sonova-holding-ag-e87e288d | pension_type |  | Sonova Group has both defined  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| space-hellas-s-a | staff_by_country |  | Ελλάδα: 798; Κύπρος: 2 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| ssp-group-plc-e4d12504 | benefits |  | private health insurance for t | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | lti_max | Group CEO | 200 | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | lti_max | Deputy CEO (until 30 September | 200 | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Group CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Deputy CEO (until 30 September | individual | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ssp-group-plc-e4d12504 | sti_max | Group CEO | 175 | Fail (hard) | CORE-03: quote not in the source text |
| st-galler-kantonalbank-ag-ba864955 | shareholding_requirement |  | For Board of Directors: 30% of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| st-james-s-place-plc-23c228ff | fte |  | 3102 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| st-james-s-place-plc-23c228ff | share_price |  | 13.845 | Fail (hard) | CORE-02: 13.845 not in the quote |
| st-james-s-place-plc-23c228ff | sti_paid | Chief Executive Officer | 1702297 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| st-james-s-place-plc-23c228ff | sti_paid | Chief Financial Officer | 1028438 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stabilus-se-52dccb73 | sub_sector |  | specializing in particular in  | Fail (hard) | CORE-03: quote not in the source text |
| stadlauer-malzfabrik-ag-8a23c30d | sub_sector |  | Holdingfunktion | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| starragtornos-group-ag-15e3832b | base_salary | Other members of the Executive | 637000 | Fail (hard) | CORE-02: 637 not in the quote |
| starragtornos-group-ag-15e3832b | benefits_value | Other members of the Executive | 26000 | Fail (hard) | CORE-02: 26 not in the quote |
| starragtornos-group-ag-15e3832b | pension_contribution | Other members of the Executive | 130000 | Fail (hard) | CORE-02: 130 not in the quote |
| starragtornos-group-ag-15e3832b | sti_paid | Other members of the Executive | 7000 | Fail (hard) | CORE-02: 7 not in the quote |
| starragtornos-group-ag-15e3832b | total_remuneration | Other members of the Executive | 799000 | Fail (hard) | CORE-02: 799 not in the quote |
| stora-enso-a | benefits_value | Other members of the Group Lea | 250000 | Fail (hard) | CORE-02: 250 not in the quote |
| stora-enso-a | exchange |  | Nasdaq Helsinki;Nasdaq Stockho | Fail (hard) | CORE-02: not in the quote: nasdaq |
| stora-enso-a | pension_contribution | Other members of Group Leaders | 1445000 | Fail (hard) | CORE-02: 1445 not in the quote |
| stora-enso-r | benefits |  | pension, disability, death, an | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-r | benefits_value | Other members of Group Leaders | 707000 | Fail (hard) | CORE-02: 707 not in the quote |
| stora-enso-r | lti_granted | President and Chief Executive  | 380200 | Fail (hard) | CORE-02: 380200 not in the quote |
| stora-enso-r | pension_contribution | Other members of Group Leaders | 1445000 | Fail (hard) | CORE-02: 1445 not in the quote |
| strabag-se-8e9d954e | staff_by_segment |  | North + West: 23161 | Fail | CORE-04: no period_end; NUM-08: adds up to 23,161 vs 88,556 (73.8% apart) |
| straumann-holding-ag-d8e91d7f | lti_vested | CEO | 180000 | Fail (hard) | CORE-02: 180 not in the quote |
| stv-group-plc-8c122da5 | benefits_value | Chief Executive Officer | 25000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stv-group-plc-8c122da5 | benefits_value | Chief Financial & Operating Of | 25000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stv-group-plc-8c122da5 | pension_contribution | Chief Executive Officer | 12000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stv-group-plc-8c122da5 | pension_contribution | Chief Financial & Operating Of | 16000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| stv-group-plc-8c122da5 | total_remuneration | Chief Financial & Operating Of | 391000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| subsea7 | staff_by_segment |  | Onshore: 9205; Offshore: 5867 | Fail | CORE-04: no period_end; NUM-08: adds up to 15,072 vs 13,821 (9.1% apart) |
| supermarket-income-reit-plc-3dbe8d27 | lti_granted | Chief Financial Officer | 118350 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (Klaus Einfalt) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89 | lti_max | Vorstand (János Váczi) | 32 | Fail (hard) | COD-01: unit '' is not a target form |
| swiss-re-ag-6528d850 | benefits_value | Group Chief Executive Officer | 27000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | lti_vested | Group Chief Executive Officer | 3394000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| swiss-re-ag-6528d850 | sti_max | Group Chief Executive Officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| swiss-re-ag-6528d850 | total_remuneration | Group Chief Executive Officer | 6065000 | Fail (hard) | XF-01: parts add up to 6,292,000, more than the stated 6,065,000; XF-02: parts add up to 6,292,000, stated 6,065,000 |
| synthomer-plc-3c60ceb4 | pension_contribution | CEO | 50592 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| synthomer-plc-3c60ceb4 | pension_contribution | CFO | 34247 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| synthomer-plc-3c60ceb4 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
| teixeira-duarte-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | benefits |  | Health insurance plan, company | Fail (hard) | CORE-03: quote not in the source text |
| tekna-holding | controlling_owner_name |  | Arendals Fossekompani ASA | Fail (hard) | CORE-02: not in the quote: arendals fossekompani asa |
| tekna-holding | lti_granted | EVP - Materials, Managing dire | 200000 | Fail (hard) | CORE-03: quote not in the source text |
| telecom-plus-plc-64a59f0e | lti_granted | CEO | 1271900 | Fail (hard) | CORE-02: 1271.9 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| telecom-plus-plc-64a59f0e | lti_granted | Executive Director | 704900 | Fail (hard) | CORE-02: 704.9 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| telecom-plus-plc-64a59f0e | sti_paid | CEO | 545100 | Fail (hard) | CORE-02: 545.1 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| telecom-plus-plc-64a59f0e | sti_paid | Executive Director | 302100 | Fail (hard) | CORE-02: 302.1 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| telecom-plus-plc-64a59f0e | total_remuneration | Executive Director | 1609000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| telefonica-s-a | total_remuneration | Executive Chairman (from Janua | 5128 | Fail (hard) | XF-01: parts add up to 136,128, more than the stated 5,128; XF-02: parts add up to 136,128, stated 5,128 |
| telefonica-s-a | total_remuneration | Chief Operating Officer (from  | 3174 | Fail (hard) | XF-01: parts add up to 128,174, more than the stated 3,174; XF-02: parts add up to 128,174, stated 3,174 |
| telefonica-s-a | total_remuneration | Former Executive Chairman (unt | 23619 | Fail (hard) | XF-01: parts add up to 13,092,093, more than the stated 23,619; XF-02: parts add up to 13,092,093, stated 23,619 |
| telefonica-s-a | total_remuneration | Former Chief Operating Officer | 17670 | Fail (hard) | XF-01: parts add up to 9,712,292, more than the stated 17,670; XF-02: parts add up to 9,712,292, stated 17,670 |
| telekom-austria-ag-62fec5fa | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| temenos-ag-21209ec1 | shareholding_requirement |  | CEO: 5 times annual fixed sala | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| terna | share_price |  | 9.054 | Fail (hard) | CORE-02: 9.054 not in the quote |
| terna | staff_by_segment |  | Regulated Activities: 5694; No | Fail (hard) | CORE-03: quote not in the source text |
| tesmec | benefits |  | company car (fringe benefit),  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tessenderlo | role_disclosure | Uitvoerend bestuurder | individual | Fail (hard) | CORE-03: quote not in the source text |
| texaf | lti_max | Directeur de l’activité digita | 750000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tharisa-plc-f4ea0c2f | headcount |  | 2966 | Fail (hard) | CORE-02: 2966 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| tharisa-plc-f4ea0c2f | staff_by_country |  | South Africa: 1993; Zimbabwe:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 2,699 vs 2,966 (9.0% apart) |
| the-beauty-tech-group-plc-65ff7e12 | listing_date |  | 2025-10 | Fail (hard) | COD-06: not a year or a date |
| the-beauty-tech-group-plc-65ff7e12 | lti_max | Chief Executive Officer | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | lti_max | Chief Financial Officer & Chie | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| the-beauty-tech-group-plc-65ff7e12 | sti_max | Chief Financial Officer & Chie | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| the-british-land-company-plc-ff87bb98 | base_salary | CFO | 670000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | benefits_value | CFO | 16000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | lti_vested | CEO (until 12 January 2026) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | lti_vested | CFO | 403000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | pension_contribution | CFO | 54000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | sti_paid | CFO | 702000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-british-land-company-plc-ff87bb98 | total_remuneration | CEO (until 12 January 2026) | 1275000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 1,243,000, stated 1,275,000 |
| the-british-land-company-plc-ff87bb98 | total_remuneration | CFO | 1862000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-sage-group-plc-a2e841b0 | base_salary | CEO | 1063750 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| the-smarter-web-company-plc-1e8404aa | exchange_segment |  | AQSE Growth Market | Fail (hard) | CORE-02: not in the quote: aqse |
| the-swatch-group-ag-6a144b9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| thg-plc-24b2c5db | sti_target | COO (until 2 January 2025) | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| thg-plc-24b2c5db | total_remuneration | Executive Director and Chief E | 33000 | Fail (hard) | XF-01: parts add up to 34,000, more than the stated 33,000; XF-02: parts add up to 34,000, stated 33,000 |
| thurgauer-kantonalbank-3b36a058 | benefits |  | For Bank Council members: occa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| thurgauer-kantonalbank-3b36a058 | pension_type |  | defined contribution. For fixe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| titan-s-a | benefits_value | Management Committee | 127267 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | benefits_value | Management Committee (until hi | 18684 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | benefits_value | Management Committee member (a | 58200 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | pension_contribution | Management Committee | 30018 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | pension_contribution | Management Committee (until hi | 11092 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | pension_contribution | Management Committee member (a | 21250 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | sti_paid | Management Committee | 202953 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | sti_paid | Management Committee (until hi | 70000 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | sti_paid | Management Committee member (a | 196096 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | total_remuneration | Management Committee | 660416 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | total_remuneration | Management Committee (until hi | 315694 | Fail (hard) | CORE-03: quote not in the source text |
| titan-s-a | total_remuneration | Management Committee member (a | 488045 | Fail (hard) | CORE-03: quote not in the source text |
| tkh-group | benefits |  | business allowances, private u | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tkh-group | lti_max | Chairman of the Executive Boar | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tkh-group | lti_max | Member of the Executive Board, | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tkh-group | lti_max | Member of the Executive Board | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tkms-ag-co-kgaa-f468ef4d | aggregate_headcount | TKMS Management Board | 4 | Fail (hard) | CORE-03: quote not in the source text |
| topps-tiles-plc-85c83f1d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| town-centre-securities-plc-5107b789 | sub_sector |  | a property investment and deve | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| toyota-caetano-portugal-s-a | base_salary | Presidente Executivo | 370528 | Fail (hard) | CORE-02: 370528 not in the quote; CORE-03: quote not in the source text |
| toyota-caetano-portugal-s-a | base_salary | Vogal Executivo (Maria Angelin | 304724 | Fail (hard) | CORE-02: 304724 not in the quote; CORE-03: quote not in the source text |
| toyota-caetano-portugal-s-a | pension_type |  | Defined benefit (20% of last p | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| toyota-caetano-portugal-s-a | sti_max | Presidente Executivo | 3 | Fail (hard) | COD-01: unit '' is not a target form |
| toyota-caetano-portugal-s-a | sti_max | Vogal Executivo (Maria Angelin | 3 | Fail (hard) | COD-01: unit '' is not a target form |
| toyota-caetano-portugal-s-a | sti_max | Vogal Executivo (Gisela Maria  | 3 | Fail (hard) | COD-01: unit '' is not a target form |
| toyota-caetano-portugal-s-a | sti_max | Vogal Executivo (Miguel Pedro  | 3 | Fail (hard) | COD-01: unit '' is not a target form |
| travis-perkins-plc-53aadfa6 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| triad-group-plc-f815b4d8 | listing_date |  | 1996-03 | Fail (hard) | COD-06: not a year or a date |
| triboo | sti_target | Presidente | 89000 | Fail (hard) | CORE-03: quote not in the source text |
| trifast-plc-3989d139 | benefits_value | Chief Executive Officer | 22000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| trifast-plc-3989d139 | benefits_value | Chief Financial Officer | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| trifast-plc-3989d139 | pension_contribution | Chief Executive Officer | 20000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| trifast-plc-3989d139 | pension_contribution | Chief Financial Officer | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| trifast-plc-3989d139 | total_remuneration | Chief Executive Officer | 449000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| trifast-plc-3989d139 | total_remuneration | Chief Financial Officer | 304000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tsk-electronica-y-electricidad-s-a | largest_holders |  | Sabino García Vallina 84.37%;  | Fail (hard) | NUM-07: holdings add up to 108.95% |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | sti_max | CEO | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ttl-beteiligungs-und-grundbesitz-ag-02636470 | sti_max | CFO (until July 2024) | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| tubize-fin | controlling_owner_name |  | FEJ SRL, Daniel Janssen, Altaï | Fail (hard) | CORE-02: not in the quote: fej srl |
| tubos-reunidos-s-a | share_price |  | 0.317 | Fail (hard) | CORE-02: 0.317 not in the quote |
| tubos-reunidos-s-a | staff_by_country |  | Alemania: 4; España: 1259; Est | Fail (hard) | CORE-03: quote not in the source text |
| tx-group-ag-cdcf98d0 | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| uie | sti_max | Managing Director | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| umg | benefits_value | Chairman and Chief Executive O | 5265744 | Fail (hard) | CORE-02: 5265744 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| umg | benefits_value | Deputy Chief Executive Officer | 60783 | Fail (hard) | CORE-02: 60783 not in the quote |
| umg | largest_holders |  | Vivendi SE 43.38%; V. Bolloré  | Fail (hard) | NUM-07: holdings add up to 131.23% |
| unibios-holdings-s-a | revenue_by_segment |  | ΘΕΑΞ, NEOVENT: 127153.51; Επεξ | Fail (hard) | CORE-03: quote not in the source text |
| uniper-se-2cd8e9fe | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| unipol | staff_by_country |  | Italy: 11949; Serbia: 1219; Ir | Fail (hard) | CORE-03: quote not in the source text |
| upland-resources-limited-813e7dce | exchange |  | OTCQB market | Fail (hard) | COD-01: 'OTCQB market' matches no ISO 10383 exchange |
| upland-resources-limited-813e7dce | listing_date |  | 2015 | Fail (hard) | CORE-02: not in the quote: 2015 |
| urbas-grupo-financiero-s-a | sti_max | Consejero ejecutivo (Adolfo Jo | 5 | Fail (hard) | CORE-02: 5 not in the quote; COD-01: unit '' is not a target form |
| urbas-grupo-financiero-s-a | sti_max | Vicepresidente Ejecutivo | 5 | Fail (hard) | CORE-02: 5 not in the quote; COD-01: unit '' is not a target form |
| urbas-grupo-financiero-s-a | sti_max | Presidente Ejecutivo | 5 | Fail (hard) | CORE-02: 5 not in the quote; COD-01: unit '' is not a target form |
| urbas-grupo-financiero-s-a | sti_max | Consejero Ejecutivo (Pablo Cob | 5 | Fail (hard) | CORE-02: 5 not in the quote; COD-01: unit '' is not a target form |
| utd-internet-ag-fa5f4803 | controlling_owner_name |  | Ralph Dommermuth | Fail (hard) | CORE-02: not in the quote: ralph |
| van-de-velde | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| vgp | sti_max | Chief Executive Officer | 1.15 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| vgp | sti_max | Other members of the Executive | 1.09 | Fail (hard) | COD-01: unit '' is not a target form |
| vgp | sti_target | Chief Executive Officer | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| vgp | sti_target | Other members of the Executive | 0.4 | Fail (hard) | COD-01: unit '' is not a target form |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Administratrice (Membre non ex | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Ancien Président | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| villeroy-boch-ag-c5a85d57 | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | listing_date |  | 1990 | Fail (hard) | CORE-02: not in the quote: 1990 |
| villeroy-boch-ag-c5a85d57 | pension_type |  | defined contribution, 15 % of  | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | role_disclosure | Vorstandsvorsitzende (seit 01. | individual | Fail (hard) | CORE-03: quote not in the source text |
| villeroy-boch-ag-c5a85d57 | shares_outstanding |  | 26765754 | Fail (hard) | CORE-02: 26765754 not in the quote; CORE-03: quote not in the source text |
| viohalco | fte |  | 13260 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| viscom-se-859e40d6 | base_salary | Vorstand Vertrieb / Operations | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | base_salary | Vorstand Entwicklung / Produkt | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | base_salary | Vorstand Finanzen | 260000 | Fail (hard) | CORE-03: quote not in the source text |
| viscom-se-859e40d6 | controlling_owner_name |  | Dr. Martin Heuser and Volker P | Fail (hard) | CORE-02: not in the quote: and |
| viscom-se-859e40d6 | listing_date |  | 2006-05 | Fail (hard) | COD-06: not a year or a date |
| viscom-se-859e40d6 | lti_max | Executive Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| viscom-se-859e40d6 | lti_max | Vorstand Vertrieb / Operations | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| viscom-se-859e40d6 | lti_max | Vorstand Entwicklung / Produkt | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| viscom-se-859e40d6 | lti_max | Vorstand Finanzen | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| viscom-se-859e40d6 | sti_max | Executive Board | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| viscom-se-859e40d6 | sti_max | Vorstand Vertrieb / Operations | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| viscom-se-859e40d6 | sti_max | Vorstand Entwicklung / Produkt | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| viscom-se-859e40d6 | sti_max | Vorstand Finanzen | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| vistry-group-plc-016bb23d | base_salary | CEO | 800000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | base_salary | CFO | 516000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | benefits_value | CEO | 101000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | benefits_value | CFO | 35000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | lti_granted | CFO | 425000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| vistry-group-plc-016bb23d | sti_paid | CEO | 1193000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | sti_paid | CFO | 790000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vistry-group-plc-016bb23d | total_remuneration | CEO | 1994000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 2,094,000, more than the stated 1,994,000; XF-02: parts add up to 2,094,000, stated 1,994,000 |
| vistry-group-plc-016bb23d | total_remuneration | CFO | 1341000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vivoryon | shareholding_requirement |  | Non-Executive Director: Shares | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vivoryon | total_remuneration | CFO (from Apr 1, 2021 until Fe | 77000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vogiatzoglou-systems-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| volkswagen-ag-be878a5e | lti_vested | Chair of the Board of Manageme | 1558188.67 | Fail (hard) | CORE-02: 1558188.67 not in the quote |
| volkswagen-ag-be878a5e | total_remuneration | Finance and Operations | 5075339.19 | Fail (hard) | XF-01: parts add up to 5,683,225, more than the stated 5,075,339; XF-02: parts add up to 5,683,225, stated 5,075,339 |
| volkswagen-ag-be878a5e | total_remuneration | China, Chair of the Board of M | 3837923 | Fail (hard) | XF-01: parts add up to 4,443,267, more than the stated 3,837,923; XF-02: parts add up to 4,443,267, stated 3,837,923 |
| volkswagen-ag-be878a5e | total_remuneration | Progressive brand group, Chair | 3404523 | Fail (hard) | XF-01: parts add up to 4,029,494, more than the stated 3,404,523; XF-02: parts add up to 4,029,494, stated 3,404,523 |
| volkswagen-ag-be878a5e | total_remuneration | Integrity and Legal Affairs | 2545518 | Fail (hard) | XF-01: parts add up to 2,995,518, more than the stated 2,545,518; XF-02: parts add up to 2,995,518, stated 2,545,518 |
| volkswagen-ag-be878a5e | total_remuneration | Human Resources and Trucks bra | 1791959.7 | Fail (hard) | XF-01: parts add up to 2,033,682, more than the stated 1,791,960; XF-02: parts add up to 2,033,682, stated 1,791,960 |
| volkswagen-ag-be878a5e | total_remuneration | Core brand group, Chair of the | 3401649 | Fail (hard) | XF-01: parts add up to 4,012,452, more than the stated 3,401,649; XF-02: parts add up to 4,012,452, stated 3,401,649 |
| volkswagen-ag-be878a5e | total_remuneration | Technology, Chair of the Board | 5630301.3 | Fail (hard) | XF-01: parts add up to 6,236,765, more than the stated 5,630,301; XF-02: parts add up to 6,236,765, stated 5,630,301 |
| volkswagen-ag-be878a5e | total_remuneration | IT | 3401076 | Fail (hard) | XF-01: parts add up to 4,026,786, more than the stated 3,401,076; XF-02: parts add up to 4,026,786, stated 3,401,076 |
| volkswagen-ag-be878a5e | total_remuneration | Former Board of Management mem | 1560554.53 | Fail (hard) | XF-01: parts add up to 1,977,489, more than the stated 1,560,555; XF-02: parts add up to 1,977,489, stated 1,560,555 |
| vontobel-holding-ag-1d88ea32 | lti_vested | Executive Committee | 7400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | pension_contribution | Executive Committee | 700000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | sti_paid | Executive Committee | 3000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vontobel-holding-ag-1d88ea32 | total_remuneration | Executive Committee | 15000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vp-bank-ag-e661c993 | lti_granted | Group Executive Management | 1284000 | Fail (hard) | CORE-02: 1284 not in the quote |
| vp-bank-ag-e661c993 | lti_granted | Chief Executive Officer (CEO) | 480000 | Fail (hard) | CORE-02: 480 not in the quote |
| vp-plc-94ebb5f9 | revenue_by_segment |  | UK: 287088; International: 711 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| vp-plc-94ebb5f9 | website |  | vpplc.com | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| w-a-g-payment-solutions-plc-44f2e7ea | listing_date |  | 2021 | Fail (hard) | CORE-02: not in the quote: 2021 |
| w-a-g-payment-solutions-plc-44f2e7ea | website |  | eurowag.com | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| wasgau-produktions-handels-8c33a77d | sti_max | Sprecher des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | sti_max | Mitglied des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | sti_max | Mitglied des Vorstands (ab 01/ | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| wdp | aggregate_headcount | Other members of the Managemen | 5 | Fail (hard) | CORE-03: quote not in the source text |
| wdp | lti_target | Other members of the Managemen | 80 | Fail (hard) | CORE-03: quote not in the source text |
| wdp | shareholding_requirement |  | WDP wijkt af van dit principe  | Fail (hard) | CORE-03: quote not in the source text |
| wdp | sub_sector |  | WDP is een toonaangevende Euro | Fail (hard) | CORE-03: quote not in the source text |
| wetherspoon-j-d-plc-f0b40e8d | accounting_basis |  | UK-adopted international accou | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wetherspoon-j-d-plc-f0b40e8d | ebitda |  | 203300000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wetherspoon-j-d-plc-f0b40e8d | fte |  | 24329 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wetherspoon-j-d-plc-f0b40e8d | pension_type |  | defined contribution, based on | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wetherspoon-j-d-plc-f0b40e8d | shares_outstanding |  | 106144586 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wetherspoon-j-d-plc-f0b40e8d | sub_sector |  | Wetherspoon owns and operates  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | controlling_owner_name |  | FFG Wisdom (Luxembourg) S.à r. | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | headcount |  | 712 | Fail (hard) | CORE-02: 712 not in the quote |
| wolford-ag-638e2dc1 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wolford-ag-638e2dc1 | staff_by_country |  | Slovenia: 160; Austria: 209 | Fail | CORE-04: no period_end; NUM-08: adds up to 369 vs 712 (48.2% apart) |
| wolters-kluwer | lti_target | Designated CEO (from May 15, 2 | 240 | Fail (hard) | CORE-02: 240 not in the quote |
| wolters-kluwer | sti_max | Designated CEO (from May 15, 2 | 175 | Fail (hard) | CORE-02: 175 not in the quote |
| wolters-kluwer | sti_target | Designated CEO (from May 15, 2 | 125 | Fail (hard) | CORE-02: 125 not in the quote |
| workspace-group-plc-23f80ffe | benefits_value | Outgoing CEO (1 April 2025 – 1 | 3700 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| workspace-group-plc-23f80ffe | lti_vested | Outgoing CFO (1 April 2025 – 3 | 116900 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| workspace-group-plc-23f80ffe | pension_contribution | Outgoing CFO (1 April 2025 – 3 | 40000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| workspace-group-plc-23f80ffe | sti_paid | Outgoing CEO (1 April 2025 – 1 | 200400 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| workspace-group-plc-23f80ffe | sti_paid | Outgoing CFO (1 April 2025 – 3 | 143300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| wuestenrot-wuerttembergische-ag-07b9dfbc | revenue_by_segment |  | Housing: 1074; Life and health | Fail (hard) | CORE-03: quote not in the source text |
| xaar-plc-44438ac8 | benefits |  | car allowance, private medical | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| xaar-plc-44438ac8 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| xp-power-ltd-2507bfe3 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| xps-pensions-group-plc-bf3a20e5 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| y-knot-invest-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| ypsomed-holding-ag-9cb8acfe | benefits |  | Dienstaltersgeschenk | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Chief Executive Officer (CEO) | 130400 | Fail (hard) | CORE-02: 130.4 not in the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Other members of group managem | 479800 | Fail (hard) | CORE-02: 479.8 not in the quote |
| zehnder-group-ag-125a701c | pension_type |  | For members of the Group Execu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zehnder-group-ag-125a701c | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| zenith-energy-ltd-4fdd6c5a | shares_outstanding |  | 100 | Fail (hard) | CORE-02: 100 not in the quote; NUM-04: 100 outside 1000..1e+12 |
| zigup-plc-d5f0480d | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| zigup-plc-d5f0480d | fte |  | 7815 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| zigup-plc-d5f0480d | headcount |  | 7600 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| zigup-plc-d5f0480d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| zigup-plc-d5f0480d | share_price |  | 3.97 | Fail (hard) | CORE-02: 3.97 not in the quote |
| zoyo-limited-7dac566f | shares_outstanding |  | 55673122 | Fail (hard) | CORE-02: 55673122 not in the quote; CORE-05: period_end 'March 31, 2026' is not a date |
| zublin-immobilien-holding-ag-cf81b4e5 | benefits |  | Sozialversicherungs-Beiträge,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (ab 15. September 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (bis 31. Dezember 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pension_type |  | leistungsorientierter Pensions | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | total_remuneration | CEO/CFO (ab 15. September 2024 | 197717 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 223,794, more than the stated 197,717; XF-02: parts add up to 223,794, stated 197,717 |
| zublin-immobilien-holding-ag-cf81b4e5 | total_remuneration | CEO/CFO (bis 31. Dezember 2024 | 246264 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 295,829, more than the stated 246,264; XF-02: parts add up to 295,829, stated 246,264 |
| zucchi | revenue_by_country |  | Italia: 51634; Francia: 26583; | Fail (hard) | CORE-03: quote not in the source text |
| zug-estates-holding-ag-4947dbda | sti_max | CEO | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| zug-estates-holding-ag-4947dbda | sti_max | Group Management | 50 | Fail (hard) | CORE-02: 50 not in the quote |
| zuger-kantonalbank-67b7c3b8 | pay_currency | Präsident der Geschäftsleitung | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | pay_currency | Geschäftsleitung (total) | CHF | Fail | CORE-04: no period_end |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Präsident der Geschäftsleitung | 850000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 938,000, more than the stated 850,000; XF-02: parts add up to 938,000, stated 850,000 |
| zuger-kantonalbank-67b7c3b8 | total_remuneration | Geschäftsleitung (total) | 3123000 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,415,000, more than the stated 3,123,000; XF-02: parts add up to 3,415,000, stated 3,123,000 |
