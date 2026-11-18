# Output checks: runs_16nov_praveen.csv

277 companies, 8465 filled values checked (2026-11-18, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 7846 (93%) |
| Review | 253 (3%) |
| Fail | 18 (0%) |
| Fail (hard) | 348 (4%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 1099 | 1099 | 0 | 0 | 0 |
| Listing and market | 977 | 956 | 0 | 0 | 21 |
| Sector | 322 | 316 | 0 | 0 | 6 |
| Reporting basis | 734 | 730 | 0 | 0 | 4 |
| Financials | 751 | 674 | 46 | 0 | 31 |
| Workforce | 254 | 217 | 22 | 1 | 14 |
| Ownership and control | 854 | 826 | 0 | 0 | 28 |
| Segment and geography | 317 | 216 | 60 | 11 | 30 |
| Pay policy | 268 | 255 | 0 | 0 | 13 |
| Role and disclosure | 931 | 899 | 1 | 6 | 25 |
| Pay: fixed | 674 | 619 | 11 | 0 | 44 |
| Pay: STI | 501 | 422 | 25 | 0 | 54 |
| Pay: LTI | 438 | 366 | 23 | 0 | 49 |
| Pay: total | 345 | 251 | 65 | 0 | 29 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 8465 | 8460 | 5 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 3148 | 2999 | 149 | 5317 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 5417 | 5242 | 175 | 3048 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 4425 | 4269 | 156 | 4040 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 8465 | 8463 | 2 | 0 | period_end 'N December N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 2791 | 2774 | 17 | 5674 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 158 | 158 | 0 | 8307 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 346 | 346 | 0 | 8119 |  |
| COD-06 | Dates are valid | yes | 365 | 363 | 2 | 8100 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1948 | 1946 | 2 | 6517 | unit 'Rs' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1669 | 1669 | 0 | 6796 |  |
| NUM-04 | Magnitude in a plausible range |  | 2442 | 2429 | 13 | 6023 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 389 | 387 | 2 | 8076 | not a whole number |
| NUM-06 | Percentages in range | yes | 492 | 492 | 0 | 7973 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 143 | 140 | 3 | 8322 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 315 | 252 | 63 | 8150 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 198 | 198 | 0 | 8267 |  |
| NUM-11 | STI paid not above its maximum |  | 86 | 80 | 6 | 8379 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1381 | 1381 | 0 | 7084 |  |
| NUM-13 | FTE not above headcount |  | 92 | 82 | 10 | 8373 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 27 | 27 | 0 | 8438 |  |
| DER-06 | Derived value shows its formula |  | 416 | 416 | 0 | 8049 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 222 | 207 | 15 | 8243 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 222 | 145 | 77 | 8243 | parts add up to N stated N |

## Fill rate

Company fields: 5576 of 11357 filled (49%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 11 | 277 |
| staff_by_segment | 33 | 277 |
| shareholding_requirement | 58 | 277 |
| staff_by_country | 78 | 277 |
| other_names | 86 | 277 |
| market_cap_band | 88 | 277 |
| revenue_by_country | 91 | 277 |
| fte | 92 | 277 |
| share_price | 93 | 277 |
| pension_type | 97 | 277 |
| exchange_segment | 107 | 277 |
| benefits | 113 | 277 |
| revenue_by_segment | 115 | 277 |
| ultimate_parent | 123 | 277 |
| ticker | 124 | 277 |
| controlling_owner_name | 135 | 277 |
| pe_stake_5pct | 139 | 277 |
| largest_holders | 143 | 277 |
| ebitda | 148 | 277 |
| accounting_basis | 151 | 277 |
| listing_date | 155 | 277 |
| controlling_owner | 157 | 277 |
| ownership_type | 157 | 277 |
| sector_code | 158 | 277 |
| total_assets | 160 | 277 |
| website | 162 | 277 |
| headcount | 162 | 277 |
| sub_sector | 164 | 277 |
| revenue | 166 | 277 |
| reporting_currency | 166 | 277 |
| isin | 167 | 277 |
| legal_name | 168 | 277 |
| lei | 168 | 277 |
| business_id | 168 | 277 |
| exchange | 168 | 277 |
| listing_status | 168 | 277 |
| country_code | 168 | 277 |
| head_office_city | 168 | 277 |
| shares_outstanding | 184 | 277 |
| fiscal_year | 207 | 277 |
| fiscal_year_end | 210 | 277 |

Pay fields, over 408 executive roles:

| Field | Filled |
|---|---|
| base_salary | 326 (80%) |
| sti_paid | 207 (51%) |
| sti_target | 112 (27%) |
| sti_max | 182 (45%) |
| lti_vested | 70 (17%) |
| lti_granted | 126 (31%) |
| lti_target | 112 (27%) |
| lti_max | 127 (31%) |
| benefits_value | 189 (46%) |
| pension_contribution | 138 (34%) |
| total_remuneration | 337 (83%) |

## Failed values (366)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| a2a | fte |  | 14762 | Fail (hard) | CORE-02: 14762 not in the quote; CORE-03: quote not in the source text |
| aalberts-nv | total_remuneration | CFO (up to 10 April 2025) | -16000 | Fail (hard) | NUM-04: -16000 outside 0..5e+10; XF-01: parts add up to -16,000, more than the stated -16,000 |
| abo-group | revenue |  | 200000000 | Fail (hard) | CORE-03: quote not in the source text |
| abo-group | revenue_by_country |  | Belgium: 33579; Netherlands: 1 | Fail | CORE-04: no period_end; NUM-08: adds up to 95,857,000 vs 200,000,000 (52.1% apart) |
| abo-group | revenue_by_segment |  | Geotechnical: 43904; Environme | Fail | CORE-04: no period_end; NUM-08: adds up to 95,857,000 vs 200,000,000 (52.1% apart) |
| abo-group | total_assets |  | 150000000 | Fail (hard) | CORE-03: quote not in the source text |
| acerinox-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| aedas-homes-s-a | base_salary | personal directivo | 1896000 | Fail (hard) | CORE-02: 1896 not in the quote; CORE-03: quote not in the source text |
| aedes | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| aedes | revenue |  | 10600000 | Fail (hard) | CORE-03: quote not in the source text |
| aedes | total_assets |  | 318000000 | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| agrana-beteiligungs-ag-60d4466c | revenue_by_segment |  | FBS: 1647834; ACS – Stärke: 98 | Fail (hard) | CORE-03: quote not in the source text |
| alpha-bank-s-a | base_salary | Chief of Growth and Innovation | 55714 | Fail (hard) | CORE-02: 55714 not in the quote |
| alpha-bank-s-a | benefits_value | CEO | 26242 | Fail (hard) | CORE-02: 26242 not in the quote |
| alpha-bank-s-a | fte |  | 6371 | Fail (hard) | CORE-02: 6371 not in the quote |
| alpha-bank-s-a | pension_contribution | Deputy CEO (as of 27.2.2025) | 69866 | Fail (hard) | CORE-02: 69866 not in the quote |
| alpha-bank-s-a | revenue_by_country |  | Greece: 2024; Other countries: | Fail (hard) | CORE-03: quote not in the source text |
| alumil-aluminium-industry-s-a | listing_date |  | May 2007 | Fail (hard) | COD-06: not a year or a date |
| amrest-holdings-se | benefits_value | Executive Chairman | 2000 | Fail (hard) | CORE-02: 2 not in the quote |
| ascencio | aggregate_headcount | Other members of the executive | 3 | Fail (hard) | CORE-03: quote not in the source text |
| athens-medical-c-s-a | listing_date |  | 1991 | Fail (hard) | CORE-02: not in the quote: 1991 |
| autostrade-meridionali | benefits |  | Erogazione di beni e/o servizi | Fail (hard) | CORE-03: quote not in the source text |
| autostrade-meridionali | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-04: 0 outside 1..5e+06 |
| b-f | lti_vested | Presidente del Consiglio di Am | 273486 | Fail (hard) | CORE-02: 273486 not in the quote; CORE-03: quote not in the source text |
| banca-mediolanum | revenue_by_country |  | Italia: 2978604; Spagna: 35928 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 5,064,671,000 vs 2,500,000,000 (102.6% apart) |
| banca-sistema | staff_by_country |  | Italy: 319; Greece: 3; Portuga | Fail (hard) | CORE-03: quote not in the source text |
| banijay-group | lti_target | Senior Management Members | 3.3 | Fail (hard) | COD-01: unit '' is not a target form |
| banijay-group | staff_by_segment |  | BGNV: 9; Banijay Entertainment | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | lti_max | Executive Vice-chairman | 120 | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | lti_max | Chief Executive Officer | 120 | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | pension_type |  | complementary pension scheme t | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | revenue_by_country |  | Spain: 2563; Portugal: 366.7;  | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | sti_max | Executive Vice-chairman | 42 | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | sti_max | Chief Executive Officer | 42 | Fail (hard) | CORE-03: quote not in the source text |
| bankinter-s-a | total_remuneration | Chief Executive Officer | 1336000 | Fail (hard) | XF-01: parts add up to 1,529,000, more than the stated 1,336,000; XF-02: parts add up to 1,529,000, stated 1,336,000 |
| basicnet | revenue_by_segment |  | Clothing, footwear and accesso | Fail | CORE-04: no period_end; NUM-08: adds up to 414,700,000 vs 348,282,000 (19.1% apart) |
| bekaert | benefits |  | company car, risk insurances,  | Fail (hard) | CORE-03: quote not in the source text |
| bekaert | benefits_value | Chief Executive Officer | 86264 | Fail (hard) | CORE-02: 86264 not in the quote |
| bekaert | benefits_value | Other members of the Executive | 393967 | Fail (hard) | CORE-02: 393967 not in the quote |
| bekaert | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bestbe-holding | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| bestbe-holding | share_price |  | 0.06 | Fail (hard) | CORE-02: 0.06 not in the quote |
| biofrontera-ag-na-o-n | lti_target | CFO | 150 | Fail (hard) | CORE-03: quote not in the source text |
| biofrontera-ag-na-o-n | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| biofrontera-ag-na-o-n | shareholding_requirement |  | Vorstandsmitglieder sind zu ei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| biotalys | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| biotalys | role_disclosure | Chief Financial Officer (from  | individual | Fail (hard) | CORE-03: quote not in the source text |
| biotalys | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ble-kedros-reic | accounting_basis |  | Διεθνή Πρότυπα Χρηματοοικονομι | Fail (hard) | CORE-03: quote not in the source text |
| ble-kedros-reic | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| borgosesia | revenue_by_segment |  | Real Estate: 16427; Alternativ | Fail (hard) | CORE-03: quote not in the source text |
| borgosesia | share_price |  | 0.576 | Fail (hard) | CORE-02: 0.576 not in the quote |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| cairo-communication | controlling_owner_name |  | Urbano Roberto Cairo | Fail (hard) | CORE-02: not in the quote: roberto |
| caltagirone-editore | fiscal_year_end |  | 2023-12-31 | Fail (hard) | CORE-03: quote not in the source text |
| cembre | lti_target | Chair of BOD and Managing Dire | 180000 | Fail (hard) | CORE-03: quote not in the source text |
| cembre | lti_target | Director | 0 | Fail (hard) | CORE-03: quote not in the source text |
| cembre | sti_target | Director | 140000 | Fail (hard) | CORE-03: quote not in the source text |
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
| cie-automotive-s-a | revenue_by_country |  | EUROPA: 1415.2; NORTEAMÉRICA:  | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | controlling_owner |  | family | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | controlling_owner_name |  | Paolo Panerai | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | ebitda |  | 7971000 | Fail (hard) | CORE-02: 7971 not in the quote |
| class-editori | exchange |  | borsa di Milano | Fail (hard) | COD-01: 'borsa di Milano' matches no ISO 10383 exchange |
| class-editori | fte |  | 355 | Fail (hard) | CORE-02: 355 not in the quote |
| class-editori | largest_holders |  | Paolo Panerai 52.47%; Nicolett | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | ownership_type |  | family_owned | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| class-editori | revenue |  | 80374000 | Fail (hard) | CORE-02: 80374 not in the quote |
| clinica-baviera-s-a | shares_outstanding |  | 16307.58 | Fail (hard) | CORE-02: 16307.58 not in the quote; CORE-04: no period_end; NUM-05: not a whole number |
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
| conduit-holdings-limited | total_remuneration | CEO (until 31 March 2025) | 1072000 | Fail (hard) | CORE-03: quote not in the source text |
| construcciones-y-auxiliar-de-ferrocarriles-s-a | revenue_by_segment |  | Railway: 3285; Buses: 927 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,212,000,000 vs 4,486,534,000 (6.1% apart) |
| construcciones-y-auxiliar-de-ferrocarriles-s-a | staff_by_country |  | Europe: 13582; Spain: 7687; Po | Fail | CORE-04: no period_end; NUM-08: adds up to 30,333 vs 15,451 (96.3% apart) |
| crediabank-s-a | benefits |  | ασφάλιση αστικής, επαγγελματικ | Fail (hard) | CORE-03: quote not in the source text |
| csp-international-industria-calze | base_salary | Presidente e Amministratore De | 253009 | Fail (hard) | CORE-02: 253009 not in the quote |
| csp-international-industria-calze | base_salary | Vice Presidente e Amministrato | 249618 | Fail (hard) | CORE-02: 249618 not in the quote |
| d-ieteren-group | revenue_by_segment |  | Belron: 3381.2; TVH: 667.4; D' | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 12,082,200,000 vs 8,033,500,000 (50.4% apart) |
| de-longhi | total_remuneration | Chairman and Chief Executive O | 2022823 | Fail (hard) | XF-01: parts add up to 2,602,823, more than the stated 2,022,823; XF-02: parts add up to 2,602,823, stated 2,022,823 |
| distribuidora-internacional-de-alimentacion-s-a | ebitda |  | 316000000 | Fail (hard) | CORE-03: quote not in the source text |
| distribuidora-internacional-de-alimentacion-s-a | fte |  | 27364 | Fail (hard) | CORE-02: 27364 not in the quote; NUM-13: FTE 27,364 above headcount 16,887 |
| dromeas-sa | ebitda |  | 2439338 | Fail (hard) | CORE-03: quote not in the source text |
| dromeas-sa | revenue_by_country |  | ΕΛΛΑΔΑ: 7768741; ΤΡΙΤΕΣ ΧΩΡΕΣ: | Fail (hard) | CORE-03: quote not in the source text |
| dt-pfandbriefbk-ag-71e35702 | revenue_by_country |  | Germany: 421; Rest of Europe:  | Fail (hard) | CORE-03: quote not in the source text |
| ebusco-holding | lti_granted | CFO | 187500 | Fail (hard) | CORE-02: 187500 not in the quote; CORE-03: quote not in the source text |
| econocom-group | role_disclosure | Chairman of the Board of Direc | individual | Fail (hard) | CORE-03: quote not in the source text |
| econocom-group | sti_max | Chairman of the Board of Direc | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| econocom-group | sti_max | Executive Directors, non-Execu | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| edp-s-a | ebitda |  | 5028000000 | Fail (hard) | CORE-02: 5028 not in the quote |
| edp-s-a | share_price |  | 3.915 | Fail (hard) | CORE-02: 3.915 not in the quote |
| el-d-mouzakis-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| el-d-mouzakis-s-a | sub_sector |  | Κατασκευή κλωστικών προϊόντων  | Fail (hard) | CORE-03: quote not in the source text |
| elica | share_price |  | 1.665 | Fail (hard) | CORE-02: 1.665 not in the quote |
| ellaktor-s-a | listing_date |  | April 1994 | Fail (hard) | COD-06: not a year or a date |
| ellaktor-s-a | revenue_by_country |  | Greece: 87271; Romania: 532; C | Fail (hard) | CORE-03: quote not in the source text |
| ellaktor-s-a | share_price |  | 1.348 | Fail (hard) | CORE-02: 1.348 not in the quote |
| elve-s-a | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| emerald-horizon-ag-a6420623 | base_salary | Vorstand | 133354 | Fail (hard) | CORE-02: 133354 not in the quote; CORE-03: quote not in the source text |
| enervit | ebitda |  | 9411000 | Fail (hard) | CORE-02: 9.411 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| enervit | staff_by_country |  | Province of Como: 162; Provinc | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| erg | ebitda |  | 4700000000 | Fail (hard) | NUM-01: unit 'Rs' is not ISO 4217 |
| erg | shares_outstanding |  | 1067435965 | Fail (hard) | CORE-03: quote not in the source text |
| erg | staff_by_country |  | Kenya: 492; Madagascar: 185; M | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 916 vs 7,278 (87.4% apart) |
| eurocommercial | revenue_by_segment |  | Belgium: 28385; France: 49862; | Fail | CORE-04: no period_end; NUM-08: adds up to 241,864,000 vs 274,219,000 (11.8% apart) |
| eurogroup-laminations | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| euronext-athens-holding-s-a | revenue_by_segment |  | Listing: 5.7; Trading: 8.6; Po | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 47,000,000 vs 82,855,000 (43.3% apart) |
| fagron | base_salary | Other members of Executive Lea | 1540660 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fagron | benefits_value | Other members of Executive Lea | 75627 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fagron | pay_currency | Other members of Executive Lea | EUR | Fail | CORE-04: no period_end |
| fagron | pension_contribution | Other members of Executive Lea | 22517 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fagron | sti_paid | Other members of Executive Lea | 2432078 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| fastned | controlling_owner_name |  | Fastned Administratie Stichtin | Fail (hard) | CORE-02: not in the quote: administratie stichting |
| fastned | staff_by_segment |  | corporate functions: 4; Networ | Fail | CORE-04: no period_end; NUM-08: adds up to 40 vs 414 (90.3% apart) |
| fidia | fte |  | 152.5 | Fail (hard) | CORE-03: quote not in the source text |
| fidia | share_price |  | 0.127 | Fail (hard) | CORE-02: 0.127 not in the quote |
| fisher-james-sons-plc-1d273817 | share_price |  | 375 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| fnm | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| fnm | sti_target | Dirigente | 40 | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | benefits |  | seguro de saúde, telemóvel e v | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| futebol-clube-do-porto-futebol-sad | role_disclosure | Administrador (Carlos Nuno Gom | individual | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | sti_paid | Presidente da Comissão Executi | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (José Pedro Fari | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Carlos Nuno Gom | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Ana Teresa Cunh | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | sti_paid | Administrador (Maria do Rosári | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (José Pedro Fari | 350000 | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Carlos Nuno Gom | 80500 | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Ana Teresa Cunh | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| futebol-clube-do-porto-futebol-sad | total_remuneration | Administrador (Maria do Rosári | 28000 | Fail (hard) | CORE-03: quote not in the source text |
| gek-terna-s-a | benefits_value | Chairman and Chief Executive O | 29547 | Fail (hard) | CORE-02: 29547 not in the quote |
| gek-terna-s-a | benefits_value | Executive Director, Executive  | 9583 | Fail (hard) | CORE-02: 9583 not in the quote |
| gek-terna-s-a | benefits_value | Executive BoD Member | 10320 | Fail (hard) | CORE-02: 10320 not in the quote |
| gek-terna-s-a | sub_sector |  | The main activity of the Compa | Fail (hard) | CORE-03: quote not in the source text |
| gek-terna-s-a | total_remuneration | Chairman and Chief Executive O | 700000 | Fail (hard) | XF-01: parts add up to 729,547, more than the stated 700,000; XF-02: parts add up to 729,547, stated 700,000 |
| gek-terna-s-a | total_remuneration | Executive BoD Member | 511620 | Fail (hard) | XF-01: parts add up to 521,940, more than the stated 511,620; XF-02: parts add up to 521,940, stated 511,620 |
| gens-aurea | staff_by_country |  | Italia: 568; Spagna: 283; Port | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| global-dominion-access-s-a | staff_by_country |  | Colombia: 3048; Spain: 2033; C | Fail | CORE-04: no period_end; NUM-08: adds up to 7,945 vs 11,629 (31.7% apart) |
| green-earth-group | aggregate_headcount | Key management personnel | 3 | Fail (hard) | CORE-03: quote not in the source text |
| grupo-media-capital-sgps-s-a | revenue_by_segment |  | Televisão, Digital e Entreteni | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 214,356,123 vs 259,191 (82602.0% apart) |
| haidemenos-integrated-printing-services-s-a | total_remuneration | Board of Directors | 274964 | Fail (hard) | XF-01: parts add up to 316,559, more than the stated 274,964; XF-02: parts add up to 316,559, stated 274,964 |
| holland-colours | lti_max | CEO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | lti_max | CFO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | lti_max | CTO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| holland-colours | sti_max | CEO | 45 | Fail (hard) | CORE-03: quote not in the source text |
| holland-colours | sti_max | CFO | 45 | Fail (hard) | CORE-03: quote not in the source text |
| holland-colours | sti_max | CTO | 45 | Fail (hard) | CORE-03: quote not in the source text |
| home-invest-be | headcount |  | 48 | Fail (hard) | CORE-02: 48 not in the quote |
| ideal-holdings-s-a | staff_by_country |  | Ελλάδα: 2427; Κύπρος: 16; Βουλ | Fail (hard) | CORE-03: quote not in the source text |
| ideal-holdings-s-a | sub_sector |  | Αποστολή της IDEAL Holdings εί | Fail (hard) | CORE-03: quote not in the source text |
| inmocemento-s-a | fte |  | 1360 | Fail (hard) | CORE-03: quote not in the source text |
| inmocemento-s-a | headcount |  | 1486 | Fail (hard) | CORE-03: quote not in the source text |
| inmocemento-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| inmocemento-s-a | share_price |  | 3.59 | Fail (hard) | CORE-02: 3.59 not in the quote |
| interpump-group | accounting_basis |  | IFRS issued by the Internaonal | Fail (hard) | CORE-03: quote not in the source text |
| interpump-group | controlling_owner |  | family | Fail (hard) | CORE-03: quote not in the source text |
| interpump-group | controlling_owner_name |  | Leila Monpò e Sorelle S.A.p.A. | Fail (hard) | CORE-03: quote not in the source text |
| interpump-group | largest_holders |  | Leila Monpò e Sorelle S.A.p.A. | Fail (hard) | CORE-03: quote not in the source text |
| interpump-group | ownership_type |  | family_owned | Fail (hard) | CORE-03: quote not in the source text |
| interpump-group | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| intica-systems-se-18005922 | sti_max | Vorsitzender des Vorstands | 150 | Fail (hard) | CORE-03: quote not in the source text |
| intica-systems-se-18005922 | sti_max | Mitglied des Vorstands (bis 30 | 150 | Fail (hard) | CORE-03: quote not in the source text |
| intracom-holdings-s-a | controlling_owner_name |  | Sokratis Kokkalis | Fail (hard) | CORE-02: not in the quote: sokratis |
| intracom-holdings-s-a | lti_max | Πρόεδρος Δ.Σ., & Δ/νων Σύμβουλ | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_max | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Πρόεδρος Δ.Σ., & Δ/νων Σύμβουλ | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| intracom-holdings-s-a | lti_target | Αντιπρόεδρος Δ.Σ., Εκτελεστικό | 0 | Fail (hard) | CORE-02: 0 not in the quote; COD-01: unit '' is not a target form |
| iren | share_price |  | 2.556 | Fail (hard) | CORE-02: 2.556 not in the quote |
| jeronimo-martins-sgps-s-a | ultimate_parent |  | Sociedade Francisco Manuel dos | Fail (hard) | CORE-02: not in the quote: sociedade francisco manuel dos santos holding b v |
| kapsch-trafficcom-ag-1d6bbc81 | ebitda |  | 20600000 | Fail (hard) | CORE-03: quote not in the source text |
| kapsch-trafficcom-ag-1d6bbc81 | revenue_by_country |  | Österreich: 15982; EMEA (exklu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kapsch-trafficcom-ag-1d6bbc81 | ultimate_parent |  | Traditio-Privatstiftung; CHILD | Fail (hard) | CORE-02: not in the quote: traditio privatstiftung |
| karelia-tobacco-company-inc | exchange_segment |  | Securities Market | Fail (hard) | CORE-02: not in the quote: securities market |
| kbc | base_salary | CEO | 2279730 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CEO of the International Marke | 160690 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CEO of the Czech Republic Busi | 102964 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CIO | 160690 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CEO of the Belgium Business Un | 160690 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CFO | 160690 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | lti_granted | CRO | 156695 | Fail (hard) | CORE-03: quote not in the source text |
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
| kbc | sti_paid | CEO of the International Marke | 231494 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | sti_paid | CEO of the Czech Republic Busi | 140778 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | sti_paid | CIO | 230741 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | sti_paid | CEO of the Belgium Business Un | 228481 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | sti_paid | CFO | 223209 | Fail (hard) | CORE-03: quote not in the source text |
| kbc | sti_paid | CRO | 218461 | Fail (hard) | CORE-03: quote not in the source text |
| kme-group | pension_type |  | defined contribution (for exec | Fail (hard) | CORE-03: quote not in the source text |
| koenig-bauer-ag-1f22b792 | lti_granted | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357 not in the quote |
| koenig-bauer-ag-1f22b792 | lti_target | CEO (from June 2025) | 357000 | Fail (hard) | CORE-02: 357000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_max | CEO (from June 2025) | 494000 | Fail (hard) | CORE-02: 494000 not in the quote |
| koenig-bauer-ag-1f22b792 | sti_target | CEO (from June 2025) | 330000 | Fail (hard) | CORE-02: 330000 not in the quote |
| koenig-bauer-ag-1f22b792 | total_remuneration | CEO (from June 2025) | 934000 | Fail (hard) | XF-01: parts add up to 959,000, more than the stated 934,000; XF-02: parts add up to 959,000, stated 934,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former CEO (until June 2025),  | 782000 | Fail (hard) | XF-01: parts add up to 813,000, more than the stated 782,000; XF-02: parts add up to 813,000, stated 782,000 |
| koenig-bauer-ag-1f22b792 | total_remuneration | Former Member of the Managemen | 446000 | Fail (hard) | XF-01: parts add up to 507,000, more than the stated 446,000; XF-02: parts add up to 507,000, stated 446,000 |
| kri-kri-milk-industry-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| kri-kri-milk-industry-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| kri-kri-milk-industry-s-a | headcount |  | 752 | Fail (hard) | CORE-03: quote not in the source text |
| kri-kri-milk-industry-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| kri-kri-milk-industry-s-a | revenue_by_country |  | Ελλάδα: 122949638; Εξωτερικό:  | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | base_salary | Chief Executive Officer | 427888 | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | benefits_value | Chief Executive Officer | 13630 | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | lti_granted | Chief Executive Officer | 101750 | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | pension_contribution | Chief Executive Officer | 14682 | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | staff_by_segment |  | Senior leadership: 121; Middle | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 1,027 vs 452 (127.2% apart) |
| lakefront-biother | sti_paid | Chief Executive Officer | 478731 | Fail (hard) | CORE-03: quote not in the source text |
| lakefront-biother | total_remuneration | Chief Executive Officer | 1036682 | Fail (hard) | CORE-03: quote not in the source text |
| lanakam-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| lanakam-s-a | headcount |  | 22 | Fail (hard) | CORE-02: 22 not in the quote |
| leonteq-ag-6723ca54 | lti_max | Executive Committee (current m | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| leonteq-ag-6723ca54 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| leonteq-ag-6723ca54 | sti_max | Executive Committee (current m | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| leonteq-ag-6723ca54 | sti_max | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| libertas-7-s-a | base_salary | Consejero Ejecutivo | 143000 | Fail (hard) | CORE-02: 143 not in the quote |
| libertas-7-s-a | lti_max | Consejero Ejecutivo | 37500 | Fail (hard) | CORE-02: 37500 not in the quote |
| libertas-7-s-a | sti_max | Consejero Ejecutivo | 87500 | Fail (hard) | CORE-02: 87500 not in the quote |
| libertas-7-s-a | sub_sector |  | desarrollo de actividades de i | Fail (hard) | CORE-03: quote not in the source text |
| linea-directa-aseguradora-s-a-compania-de-seguros-y-reaseguros | share_price |  | 1.118 | Fail (hard) | CORE-02: 1.118 not in the quote |
| lufthansa-ag-0bc3d92c | controlling_owner_name |  | Deutsche Lufthansa Aktiengesel | Fail (hard) | CORE-02: not in the quote: aktiengesellschaft |
| moury-construct | aggregate_headcount | Autres dirigeants | 3.5 | Fail (hard) | NUM-05: not a whole number |
| nai-ord-shares | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| naturhouse-health-s-a | largest_holders |  | DON FÉLIX REVUELTA FERNÁNDEZ 7 | Fail (hard) | NUM-07: holdings add up to 156.36% |
| new-sources-energy | share_price |  | 0.015 | Fail (hard) | CORE-02: 0.015 not in the quote |
| new-sources-energy | staff_by_country |  | Netherlands: 1.8 | Fail | CORE-04: no period_end |
| nyesa-valores-corporacion-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| nyesa-valores-corporacion-s-a | listing_date |  | 2018 | Fail (hard) | CORE-02: not in the quote: 2018 |
| nyesa-valores-corporacion-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| nyxoah | lti_granted | Other members of executive man | 25000 | Fail (hard) | CORE-02: 25000 not in the quote |
| nyxoah | lti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| nyxoah | lti_target | Other members of executive man | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| nyxoah | sti_target | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| onyx-touristiki-societe-anonyme | base_salary | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| onyx-touristiki-societe-anonyme | benefits_value | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| onyx-touristiki-societe-anonyme | revenue_by_segment |  | Ένδυση: 2286057 | Fail (hard) | CORE-03: quote not in the source text |
| onyx-touristiki-societe-anonyme | sti_max | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | sti_max | Εκτελεστικό Μέλος (until 18/12 | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | sti_max | Επικεφαλής Μονάδας Εσωτερικού  | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| onyx-touristiki-societe-anonyme | total_remuneration | Πρόεδρος Δ.Σ. & Διευθύνων Σύμβ | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| orange-belgium | benefits_value | CEO | 358681 | Fail (hard) | CORE-03: quote not in the source text |
| pb-holding | controlling_owner_name |  | Nafimij B.V. | Fail (hard) | CORE-02: not in the quote: b v |
| pb-holding | fte |  | 2100 | Fail | CORE-04: no period_end; NUM-13: FTE 2,100 above headcount 1 |
| pb-holding | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| pb-holding | ultimate_parent |  | Nafimij B.V. | Fail (hard) | CORE-02: not in the quote: v |
| performance-technologies-s-a | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| performance-technologies-s-a | role_disclosure | Εκτελεστικό Μέλος, Αντιπρόεδρο | individual | Fail (hard) | CORE-03: quote not in the source text |
| performance-technologies-s-a | role_disclosure | Εκτελεστικό Μέλος, Πρόεδρος &  | individual | Fail (hard) | CORE-03: quote not in the source text |
| performance-technologies-s-a | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| pharma-mar-s-a | total_remuneration | Executive Chairman | 3125807000 | Fail (hard) | CORE-03: quote not in the source text |
| pharma-mar-s-a | total_remuneration | Executive Vice-Chairman | 577000 | Fail (hard) | XF-01: parts add up to 12,597,000, more than the stated 577,000; XF-02: parts add up to 12,597,000, stated 577,000 |
| pharmanutra | base_salary | Amministratore esecutivo (Germ | 342292.81 | Fail (hard) | CORE-02: 342292.81 not in the quote |
| pharmanutra | total_remuneration | Presidente e amministratore es | 2592600 | Fail (hard) | XF-01: parts add up to 2,848,860, more than the stated 2,592,600; XF-02: parts add up to 2,848,860, stated 2,592,600 |
| pharmanutra | total_remuneration | Vice Presidente e amministrato | 2328600 | Fail (hard) | XF-01: parts add up to 2,558,460, more than the stated 2,328,600; XF-02: parts add up to 2,558,460, stated 2,328,600 |
| pharmanutra | total_remuneration | Amministratore esecutivo (Carl | 2148600 | Fail (hard) | XF-01: parts add up to 2,360,460, more than the stated 2,148,600; XF-02: parts add up to 2,360,460, stated 2,148,600 |
| pharmanutra | total_remuneration | Amministratore esecutivo (Germ | 646492.81 | Fail (hard) | XF-01: parts add up to 700,913, more than the stated 646,493; XF-02: parts add up to 700,913, stated 646,493 |
| pininfarina | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| pipe-works-l-girakian-profil-s-a | revenue_by_segment |  | Κατασκευή χαλυβδοσωλήνων: 1886 | Fail (hard) | CORE-03: quote not in the source text |
| plastika-kritis-s-a | accounting_basis |  | Διεθνή Πρότυπα Χρηματοοικονομι | Fail (hard) | CORE-03: quote not in the source text |
| plastika-kritis-s-a | staff_by_country |  | Ελλάδα: 504; Πολωνία: 128; Ρου | Fail (hard) | CORE-03: quote not in the source text |
| plastika-kritis-s-a | ticker |  | PLAKR | Fail (hard) | CORE-02: not in the quote: plakr |
| porceleyne-fles | base_salary | Director (until May 2025) | 104000 | Fail (hard) | CORE-03: quote not in the source text |
| porceleyne-fles | pension_contribution | Director (until May 2025) | 11000 | Fail (hard) | CORE-03: quote not in the source text |
| porceleyne-fles | sti_paid | Director (until May 2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| poste-italiane | revenue_by_segment |  | Mail, Parcel and Distribution: | Fail | CORE-04: no period_end; NUM-08: adds up to 14,150,000,000 vs 13,120,000,000 (7.9% apart) |
| qev | revenue_by_country |  | Sweden: 4144785; Spain: 251881 | Fail | CORE-04: no period_end; NUM-08: adds up to 13,446,829 vs 22,991,751 (41.5% apart) |
| qrf | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| qualco-group-s-a | controlling_owner_name |  | Wokalon Finances Limited | Fail (hard) | CORE-02: not in the quote: finances limited |
| qualco-group-s-a | ultimate_parent |  | Wokalon Finances Limited | Fail (hard) | CORE-02: not in the quote: finances limited |
| ramada-investimentos-e-industria-s-a | lti_max | executivo | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ramada-investimentos-e-industria-s-a | lti_max | executiva | 50 | Fail (hard) | COD-01: unit '' is not a target form |
| ramada-investimentos-e-industria-s-a | sti_max | executivo | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| ramada-investimentos-e-industria-s-a | sti_max | executiva | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| rcs-mediagroup | staff_by_country |  | Italia: 1781; Spagna: 1083; Al | Fail (hard) | CORE-03: quote not in the source text |
| redeia-corporacion-s-a | sub_sector |  | Its core activities comprise t | Fail (hard) | CORE-03: quote not in the source text |
| redeia-corporacion-s-a | ticker |  | REE | Fail (hard) | CORE-02: not in the quote: ree |
| retail-estates | lti_target | Other members of the managemen | 15 | Fail (hard) | CORE-02: 15 not in the quote |
| revo-insurance | revenue_by_country |  | Italia: 379931; Estero (tra cu | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 398,121,000 vs 287,519,000 (38.5% apart) |
| sacyr-s-a | revenue |  | 4660000000 | Fail (hard) | CORE-02: 4660 not in the quote |
| sacyr-s-a | share_price |  | 3.866 | Fail (hard) | CORE-02: 3.866 not in the quote |
| schott-pharma-ag-co-kgaa-26f01ea5 | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| seri-industrial | exchange_segment |  | main market EXM | Fail (hard) | CORE-02: not in the quote: main market |
| seri-industrial | staff_by_segment |  | Batteries: 450; Plastic Materi | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 1,270 vs 1,339 (5.2% apart) |
| somec | staff_by_segment |  | Horizons: sistemi ingegnerizza | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 607 vs 995 (39.0% apart) |
| sonaecom-sgps-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| sonaecom-sgps-s-a | share_price |  | 2.8 | Fail (hard) | CORE-02: 2.8 not in the quote |
| space-hellas-s-a | staff_by_country |  | Ελλάδα: 798; Κύπρος: 2 | Fail (hard) | CORE-03: quote not in the source text |
| stadlauer-malzfabrik-ag-8a23c30d | sub_sector |  | Holdingfunktion | Fail (hard) | CORE-03: quote not in the source text |
| teixeira-duarte-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| tesmec | benefits |  | company car (fringe benefit),  | Fail (hard) | CORE-03: quote not in the source text |
| texaf | lti_max | Directeur de l’activité digita | 750000 | Fail (hard) | CORE-03: quote not in the source text |
| tkh-group | benefits |  | business allowances, private u | Fail (hard) | CORE-03: quote not in the source text |
| tkh-group | lti_max | Chairman of the Executive Boar | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tkh-group | lti_max | Member of the Executive Board, | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tkh-group | lti_max | Member of the Executive Board | 270 | Fail (hard) | CORE-02: 270 not in the quote |
| tsk-electronica-y-electricidad-s-a | largest_holders |  | Sabino García Vallina 84.37%;  | Fail (hard) | NUM-07: holdings add up to 108.95% |
| tubize-fin | controlling_owner_name |  | FEJ SRL, Daniel Janssen, Altaï | Fail (hard) | CORE-02: not in the quote: fej srl |
| umg | benefits_value | Chairman and Chief Executive O | 5265744 | Fail (hard) | CORE-02: 5265744 not in the quote; CORE-03: quote not in the source text |
| umg | benefits_value | Deputy Chief Executive Officer | 60783 | Fail (hard) | CORE-02: 60783 not in the quote |
| umg | largest_holders |  | Vivendi SE 43.38%; V. Bolloré  | Fail (hard) | NUM-07: holdings add up to 131.23% |
| uniper-se-2cd8e9fe | benefits_value | Chief Executive Officer (since | 719000 | Fail (hard) | CORE-02: 719 not in the quote |
| uniper-se-2cd8e9fe | benefits_value | Chief Executive Officer (until | 1554000 | Fail (hard) | CORE-02: 1554 not in the quote |
| uniper-se-2cd8e9fe | benefits_value | Chief Commercial Officer (unti | 891000 | Fail (hard) | CORE-02: 891 not in the quote |
| uniper-se-2cd8e9fe | benefits_value | Chief Operating Officer (until | 878000 | Fail (hard) | CORE-02: 878 not in the quote |
| viohalco | fte |  | 13260 | Fail (hard) | CORE-03: quote not in the source text |
| vivoryon | shareholding_requirement |  | Non-Executive Director: Shares | Fail (hard) | CORE-03: quote not in the source text |
| vivoryon | total_remuneration | CFO (from Apr 1, 2021 until Fe | 77000 | Fail (hard) | CORE-03: quote not in the source text |
| vogiatzoglou-systems-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | benefits |  | D&O-Versicherung, Abfertigung, | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | ebitda |  | 1804000 | Fail (hard) | CORE-02: 1804 not in the quote; CORE-04: no period_end |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | share_price |  | 0.452 | Fail (hard) | CORE-02: 0.452 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | staff_by_segment |  | Investment Properties: 5; Hote | Fail | CORE-04: no period_end; NUM-08: adds up to 82 vs 87 (5.7% apart) |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Vorsitzender des Vorstands | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | stellvertretender Vorsitzender | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Dr. Al | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| warimpex-finanz-und-beteiligungs-ag-ae611bc8 | sti_max | Mitglied des Vorstands (Mag. F | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| wolters-kluwer | lti_target | Designated CEO (from May 15, 2 | 240 | Fail (hard) | CORE-02: 240 not in the quote |
| wolters-kluwer | sti_max | Designated CEO (from May 15, 2 | 175 | Fail (hard) | CORE-02: 175 not in the quote |
| wolters-kluwer | sti_target | Designated CEO (from May 15, 2 | 125 | Fail (hard) | CORE-02: 125 not in the quote |
| zehnder-group-ag-125a701c | benefits_value | Other members of the Group Exe | 89570 | Fail (hard) | CORE-02: 89570 not in the quote |
