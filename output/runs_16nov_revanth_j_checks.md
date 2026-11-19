# Output checks: runs_16nov_revanth_j.csv

277 companies, 7910 filled values checked (2026-11-19, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 7408 (94%) |
| Review | 166 (2%) |
| Fail | 7 (0%) |
| Fail (hard) | 329 (4%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 1046 | 1043 | 0 | 0 | 3 |
| Listing and market | 931 | 916 | 0 | 0 | 15 |
| Sector | 310 | 308 | 0 | 0 | 2 |
| Reporting basis | 684 | 683 | 0 | 0 | 1 |
| Financials | 727 | 684 | 21 | 0 | 22 |
| Workforce | 236 | 211 | 15 | 0 | 10 |
| Ownership and control | 815 | 778 | 0 | 0 | 37 |
| Segment and geography | 324 | 230 | 68 | 7 | 19 |
| Pay policy | 239 | 222 | 0 | 0 | 17 |
| Role and disclosure | 736 | 712 | 0 | 0 | 24 |
| Pay: fixed | 646 | 603 | 0 | 0 | 43 |
| Pay: STI | 506 | 439 | 19 | 0 | 48 |
| Pay: LTI | 434 | 371 | 1 | 0 | 62 |
| Pay: total | 276 | 208 | 42 | 0 | 26 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 7910 | 7906 | 4 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 3001 | 2913 | 88 | 4909 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 5080 | 4872 | 208 | 2830 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 4186 | 4139 | 47 | 3724 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 7910 | 7908 | 2 | 0 | period_end 'N-N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 2607 | 2584 | 23 | 5303 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 154 | 154 | 0 | 7756 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 327 | 327 | 0 | 7583 |  |
| COD-06 | Dates are valid | yes | 340 | 336 | 4 | 7570 | not a yearN a year and monthN or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1807 | 1805 | 2 | 6103 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1493 | 1493 | 0 | 6417 |  |
| NUM-04 | Magnitude in a plausible range |  | 2261 | 2259 | 2 | 5649 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 362 | 360 | 2 | 7548 | not a whole number |
| NUM-06 | Percentages in range | yes | 598 | 598 | 0 | 7312 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 137 | 132 | 5 | 7773 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 315 | 244 | 71 | 7595 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 172 | 172 | 0 | 7738 |  |
| NUM-11 | STI paid not above its maximum |  | 123 | 104 | 19 | 7787 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1265 | 1264 | 1 | 6645 | currency N the role's other amounts EUR |
| NUM-13 | FTE not above headcount |  | 90 | 82 | 8 | 7820 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 21 | 21 | 0 | 7889 |  |
| DER-06 | Derived value shows its formula |  | 401 | 401 | 0 | 7509 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 236 | 226 | 10 | 7674 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 236 | 178 | 58 | 7674 | parts add up to N stated N |

## Fill rate

Company fields: 5312 of 11357 filled (47%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 6 | 277 |
| staff_by_segment | 34 | 277 |
| shareholding_requirement | 55 | 277 |
| other_names | 81 | 277 |
| staff_by_country | 82 | 277 |
| market_cap_band | 85 | 277 |
| share_price | 88 | 277 |
| fte | 90 | 277 |
| pension_type | 90 | 277 |
| revenue_by_country | 92 | 277 |
| benefits | 94 | 277 |
| exchange_segment | 103 | 277 |
| ultimate_parent | 108 | 277 |
| ticker | 116 | 277 |
| revenue_by_segment | 116 | 277 |
| controlling_owner_name | 123 | 277 |
| pe_stake_5pct | 132 | 277 |
| largest_holders | 137 | 277 |
| ebitda | 146 | 277 |
| accounting_basis | 146 | 277 |
| headcount | 146 | 277 |
| listing_date | 147 | 277 |
| total_assets | 153 | 277 |
| website | 154 | 277 |
| sector_code | 154 | 277 |
| revenue | 155 | 277 |
| sub_sector | 156 | 277 |
| reporting_currency | 156 | 277 |
| controlling_owner | 157 | 277 |
| ownership_type | 158 | 277 |
| isin | 160 | 277 |
| exchange | 160 | 277 |
| listing_status | 160 | 277 |
| legal_name | 161 | 277 |
| lei | 161 | 277 |
| business_id | 161 | 277 |
| country_code | 161 | 277 |
| head_office_city | 161 | 277 |
| shares_outstanding | 185 | 277 |
| fiscal_year | 189 | 277 |
| fiscal_year_end | 193 | 277 |

Pay fields, over 321 executive roles:

| Field | Filled |
|---|---|
| base_salary | 289 (90%) |
| sti_paid | 189 (59%) |
| sti_target | 130 (40%) |
| sti_max | 187 (58%) |
| lti_vested | 79 (25%) |
| lti_granted | 93 (29%) |
| lti_target | 120 (37%) |
| lti_max | 142 (44%) |
| benefits_value | 188 (59%) |
| pension_contribution | 138 (43%) |
| total_remuneration | 274 (85%) |

## Failed values (336)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| abitare-in | total_remuneration | Presidente del Consiglio di Am | 335564 | Fail (hard) | XF-01: parts add up to 375,872, more than the stated 335,564; XF-02: parts add up to 375,872, stated 335,564 |
| abitare-in | total_remuneration | Amministratore Delegato | 290500 | Fail (hard) | XF-01: parts add up to 336,372, more than the stated 290,500; XF-02: parts add up to 336,372, stated 290,500 |
| abitare-in | total_remuneration | Dirigente con responsabilità s | 106000 | Fail (hard) | XF-01: parts add up to 117,432, more than the stated 106,000; XF-02: parts add up to 117,432, stated 106,000 |
| abn-amro-bank-n-v | staff_by_segment |  | Personal & Business Banking: 4 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 23,125 vs 24,632 (6.1% apart) |
| acs-actividades-de-construccion-y-servicios-s-a | staff_by_country |  | Spain: 86216; Australia: 21776 | Fail | CORE-04: no period_end; NUM-08: adds up to 167,803 vs 73 (229767.1% apart) |
| ahold-del | lti_vested | Former Management Board member | 635000 | Fail (hard) | CORE-03: quote not in the source text |
| alfen | benefits_value | CEO (from 1 November 2025) | 17000 | Fail (hard) | CORE-03: quote not in the source text |
| alfen | benefits_value | CEO (until 1 November 2025) | 43000 | Fail (hard) | CORE-03: quote not in the source text |
| alfen | benefits_value | CFO (from 1 January 2025) | 34000 | Fail (hard) | CORE-03: quote not in the source text |
| alfen | benefits_value | CCO (until 11 March 2025) | 12000 | Fail (hard) | CORE-03: quote not in the source text |
| amadeus-it-group-s-a | revenue_by_segment |  | Personnel Services segment: 20 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 363,868,000 vs 6,517,000,000 (94.4% apart) |
| amadeus-it-group-s-a | staff_by_country |  | Germany: 4058 | Fail | CORE-04: no period_end; NUM-08: adds up to 4,058 vs 3,199 (26.9% apart) |
| amadeus-it-group-s-a | staff_by_segment |  | Employees working for customer | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 3,376 vs 3,199 (5.5% apart) |
| amadeus-it-group-s-a | ticker |  | AAD | Fail (hard) | CORE-03: quote not in the source text |
| applied-nutrition-plc | lti_max | Chief Executive Officer | 33 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | lti_max | Chief Financial Officer | 33 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | lti_max | Chief Operating Officer | 33 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | lti_target | Chief Executive Officer | 22 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | lti_target | Chief Financial Officer | 22 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | lti_target | Chief Operating Officer | 22 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| applied-nutrition-plc | revenue_by_country |  | UK: 48.4; Europe: 15.6; Intern | Fail (hard) | CORE-03: quote not in the source text |
| arteche-lantegi-elkartea-s-a | lti_granted | Senior management | 4389000 | Fail (hard) | CORE-02: 4389 not in the quote; CORE-03: quote not in the source text |
| ascopiave | share_price |  | 3.3 | Fail (hard) | CORE-02: 3.3 not in the quote |
| asml | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| athens-water-supply-and-sewerage-company-s-a | staff_by_country |  | Αττική: 2610; Φωκίδα, Βοιωτία  | Fail (hard) | CORE-03: quote not in the source text |
| autotrader-group-plc | share_price |  | 469.5 | Fail (hard) | NUM-01: unit 'p' is not ISO 4217 |
| bally-s-intralot-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| bally-s-intralot-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| bally-s-intralot-s-a | share_price |  | 0.222 | Fail (hard) | CORE-02: 0.222 not in the quote |
| banca-generali | ebitda |  | 639112000 | Fail (hard) | CORE-02: 639.112 not in the quote |
| banca-monte-dei-paschi-di-siena | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| banca-monte-dei-paschi-di-siena | largest_holders |  | Deln S.A.R.L. 17.533%; Frances | Fail (hard) | CORE-03: quote not in the source text |
| banca-monte-dei-paschi-di-siena | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| banca-monte-dei-paschi-di-siena | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vice-Presidente do CA e Presid | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vice-Presidente da CE (Miguel  | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vice-Presidente da CE (João Nu | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vogal da CE (Rui Manuel da Sil | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vogal da CE (José Miguel Bensl | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_max | Vogal da CE (Maria José Henriq | 50 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vice-Presidente do CA e Presid | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vice-Presidente da CE (Miguel  | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vice-Presidente da CE (João Nu | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vogal da CE (Rui Manuel da Sil | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vogal da CE (José Miguel Bensl | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | lti_target | Vogal da CE (Maria José Henriq | 36 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vice-Presidente do CA e Presid | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vice-Presidente da CE (Miguel  | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vice-Presidente da CE (João Nu | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vogal da CE (Rui Manuel da Sil | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vogal da CE (José Miguel Bensl | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_max | Vogal da CE (Maria José Henriq | 75 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vice-Presidente do CA e Presid | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vice-Presidente da CE (Miguel  | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vice-Presidente da CE (João Nu | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vogal da CE (Rui Manuel da Sil | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vogal da CE (José Miguel Bensl | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banco-comercial-portugues-s-a | sti_target | Vogal da CE (Maria José Henriq | 54 | Fail (hard) | CORE-03: quote not in the source text |
| banqup-group | sti_max | CEO (until November 2024) / Ex | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_max | CEO (from December 2024) | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_max | COO | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_max | CFO (until April 2024) | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_max | CFO (from April 2024) | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_target | CEO (until November 2024) / Ex | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| banqup-group | sti_target | CEO (from December 2024) | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_target | COO | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| banqup-group | sti_target | CFO (until April 2024) | 33.33 | Fail (hard) | CORE-02: 33.33 not in the quote |
| banqup-group | sti_target | CFO (from April 2024) | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| basic-fit | benefits |  | company car, other benefits | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | benefits_value | CEO | 34044 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | benefits_value | CFO | 12170 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | lti_granted | CEO | 546801 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | lti_granted | CFO | 390721 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | lti_vested | CEO | 437438 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | pension_contribution | CEO | 109359 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | pension_contribution | CFO | 97500 | Fail (hard) | CORE-03: quote not in the source text |
| basic-fit | shareholding_requirement |  | shares subject to a mandatory  | Fail (hard) | CORE-03: quote not in the source text |
| bastogi | listing_date |  | 1863 | Fail (hard) | COD-06: not a year, a year and month, or a date |
| bastogi | other_names |  | Società Italiana per le Strade | Fail (hard) | CORE-02: not in the quote: italiana per |
| belysse-group | largest_holders |  | LSF9 Belysse Holdco S.à r.l. 5 | Fail (hard) | NUM-07: holdings add up to 114.08% |
| bff-bank | base_salary | Executives with Strategic Resp | 1138782 | Fail (hard) | CORE-02: 1138782 not in the quote |
| bff-bank | revenue_by_segment |  | Factoring & Lending: 166856; S | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 347,062,000 vs 490,181,000 (29.2% apart) |
| bff-bank | shareholding_requirement |  | Recipients must maintain, from | Fail (hard) | CORE-03: quote not in the source text |
| bodegas-riojanas-s-a | largest_holders |  | Van Gestión y Asesoramiento Em | Fail (hard) | CORE-03: quote not in the source text |
| bodegas-riojanas-s-a | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| bodegas-riojanas-s-a | total_remuneration | Presidente Ejecutivo | 139000 | Fail (hard) | XF-01: parts add up to 145,512, more than the stated 139,000; XF-02: parts add up to 145,512, stated 139,000 |
| brunel-internat | lti_granted | CEO | 199000 | Fail (hard) | CORE-02: 199 not in the quote |
| brunel-internat | total_remuneration | CEO | 814000 | Fail (hard) | XF-01: parts add up to 877,000, more than the stated 814,000; XF-02: parts add up to 877,000, stated 814,000 |
| burckhardt-compression-holding-ag | pension_contribution | CEO | 221000 | Fail (hard) | CORE-02: 221 not in the quote; CORE-04: no period_end |
| burckhardt-compression-holding-ag | pension_contribution | Other members of the Executive | 488000 | Fail (hard) | CORE-02: 488 not in the quote; CORE-04: no period_end |
| caleffi | staff_by_country |  | Italy: 1295; Other European co | Fail | CORE-04: no period_end; NUM-08: adds up to 1,638 vs 165 (892.7% apart) |
| care-property-inv | benefits_value | CEO | 8095 | Fail (hard) | CORE-02: 8095 not in the quote |
| care-property-inv | benefits_value | CFO | 7416 | Fail (hard) | CORE-02: 7416 not in the quote |
| care-property-inv | benefits_value | COO | 7429 | Fail (hard) | CORE-02: 7429 not in the quote |
| care-property-inv | benefits_value | Chief Business Development Off | 6691 | Fail (hard) | CORE-02: 6691 not in the quote |
| care-property-inv | benefits_value | Chief Legal Officer | 8765 | Fail (hard) | CORE-02: 8765 not in the quote |
| care-property-inv | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| care-property-inv | sti_paid | Former CEO (until 31 December  | 110028 | Fail (hard) | CORE-03: quote not in the source text |
| centiel-ag-eeeda54a | shares_outstanding |  | 100200 | Fail (hard) | CORE-03: quote not in the source text |
| centric-holdings-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| centric-holdings-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| centric-holdings-s-a | ticker |  | CNA | Fail (hard) | CORE-03: quote not in the source text |
| cfe | revenue_by_segment |  | Dredging, Environmental & Mari | Fail | CORE-04: no period_end; NUM-08: adds up to 3,055,600,000 vs 2,797,100,000 (9.2% apart) |
| colonial-sfl-socimi-s-a | share_price |  | 5.115 | Fail (hard) | CORE-02: 5.115 not in the quote |
| comer-industries | headcount |  | 2806 | Fail (hard) | CORE-03: quote not in the source text |
| ctp | sti_max | Chief Financial Officer | 200 | Fail (hard) | CORE-03: quote not in the source text |
| cy4gate | staff_by_country |  | Italy: 470 | Fail | CORE-04: no period_end; NUM-08: adds up to 470 vs 548 (14.2% apart) |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | controlling_owner |  | corporate | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | controlling_owner_name |  | Maden S.A. | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | largest_holders |  | Maden S.A. 29.64%; Sarm S.A. 1 | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | lti_max | Consejero Delegado | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | ownership_type |  | subsidiary | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | revenue_by_country |  | Mercado interior: 33800; Unión | Fail (hard) | CORE-03: quote not in the source text |
| desarrollos-especiales-de-sistemas-de-anclaje-s-a | sti_max | Consejero Delegado | 2 | Fail (hard) | COD-01: unit '' is not a target form |
| diasorin | total_remuneration | General Manager | 1964661.67 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,880,046, stated 1,964,662 |
| diasorin | total_remuneration | Strategy Executive | 1002763.21 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 959,686, stated 1,002,763 |
| diasorin | total_remuneration | Other Executives with Strategi | 1335407.5 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,226,608, stated 1,335,408 |
| duro-felguera-s-a | largest_holders |  | DON JOSÉ MIGUEL BEJOS 54.66%;  | Fail (hard) | NUM-07: holdings add up to 109.32% |
| east-star-resources-plc | base_salary | Chief Executive Officer and Ex | 125000 | Fail (hard) | CORE-02: 125 not in the quote |
| edison | fte |  | 6118 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | base_salary | CEO | 200000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | base_salary | CFO | 150000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | base_salary | COO | 150000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | base_salary | Other members of the Executive | 150000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | base_salary | Executive Management Team | 600000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | benefits_value | Executive Management Team | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | lti_granted | CEO | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | lti_granted | CFO | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | lti_granted | COO | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | lti_granted | Other members of the Executive | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | pension_type |  | Belgian (defined benefit), Fre | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | CFO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | COO | individual | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | Other members of the Executive | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | role_disclosure | Executive Management Team | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_paid | CEO | 100000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_paid | CFO | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_paid | COO | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_paid | Other members of the Executive | 75000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_paid | Executive Management Team | 150000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | sti_target | Executive Management Team | 25 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | total_remuneration | CEO | 400000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | total_remuneration | CFO | 300000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | total_remuneration | COO | 300000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | total_remuneration | Other members of the Executive | 300000 | Fail (hard) | CORE-03: quote not in the source text |
| ekopak | total_remuneration | Executive Management Team | 850000 | Fail (hard) | CORE-03: quote not in the source text |
| elastron-s-a-steel-service-centers | base_salary | Σύμβουλος - Εκτελεστικό Μέλος  | 133837.46 | Fail (hard) | CORE-02: 133837.46 not in the quote |
| elastron-s-a-steel-service-centers | headcount |  | 234 | Fail (hard) | CORE-03: quote not in the source text |
| elton-international-trading-company-s-a | exchange_segment |  | Small Cap | Fail (hard) | CORE-02: not in the quote: small cap |
| elton-international-trading-company-s-a | shares_outstanding |  | 26426617 | Fail (hard) | CORE-03: quote not in the source text |
| emak | ebitda |  | 591478000 | Fail (hard) | CORE-02: 591478 not in the quote |
| emak | staff_by_country |  | Mexico: 12357; USA: 6854; Euro | Fail (hard) | CORE-03: quote not in the source text |
| emporiki-eisagogiki-aftokiniton-ditrohon-kai-mihanon-thalassis-societe-anonyme | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| emporiki-eisagogiki-aftokiniton-ditrohon-kai-mihanon-thalassis-societe-anonyme | staff_by_segment |  | Management positions: 43; Prof | Fail | CORE-04: no period_end; NUM-08: adds up to 317 vs 390 (18.7% apart) |
| entain-plc | share_price |  | 7.666 | Fail (hard) | CORE-02: 7.666 not in the quote |
| envipco-holding | fte |  | 531 | Fail (hard) | CORE-03: quote not in the source text |
| envipco-holding | listing_date |  | December 2024 | Fail (hard) | COD-06: not a year, a year and month, or a date |
| envipco-holding | revenue_by_segment |  | Europe: 56.048; North America: | Fail (hard) | CORE-03: quote not in the source text |
| eph-invest | controlling_owner_name |  | RONA Limited Company S.r.l | Fail (hard) | CORE-02: not in the quote: limited company |
| eph-invest | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| estoril-sol-sgps-s-a | exchange_segment |  | Regulated Market | Fail (hard) | CORE-02: not in the quote: regulated market |
| estoril-sol-sgps-s-a | sti_max | Presidente do Conselho de Admi | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| estoril-sol-sgps-s-a | sti_max | Vogal do Conselho de Administr | 11 | Fail (hard) | COD-01: unit '' is not a target form |
| european-innovation-solutions-s-a | benefits |  | insurance coverage for medical | Fail (hard) | CORE-03: quote not in the source text |
| eurotech | lti_vested | Dirigenti strategici | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| eurotech | sti_paid | Presidente del Consiglio di Am | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| eurotech | sti_paid | Amministratore Delegato (until | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| eurotech | sti_paid | Amministratore Delegato (from  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| eurotech | sti_paid | Dirigenti strategici | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| fiera-milano | benefits |  | insurance cover for death, occ | Fail (hard) | CORE-03: quote not in the source text |
| floridienne | ebitda |  | 109977000 | Fail (hard) | CORE-02: 109.977 not in the quote |
| floridienne | revenue_by_segment |  | Life Sciences: 538.3; Food: 15 | Fail (hard) | CORE-03: quote not in the source text |
| floridienne | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| forfarmers | lti_target | COO | 52.5 | Fail (hard) | CORE-02: 52.5 not in the quote; CORE-03: quote not in the source text |
| fourlis-holdings-s-a | lti_max | Chairman, Executive Member | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| fourlis-holdings-s-a | lti_max | Vice-Chairman, Executive Membe | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| fourlis-holdings-s-a | lti_max | Chief Executive Officer (until | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| fourlis-holdings-s-a | lti_max | Chief Executive Officer (since | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| fourlis-holdings-s-a | lti_max | Director, Executive Member | 5 | Fail (hard) | COD-01: unit '' is not a target form |
| fourlis-holdings-s-a | staff_by_country |  | Greece: 3103; Cyprus: 373; Rom | Fail (hard) | CORE-03: quote not in the source text |
| fourlis-holdings-s-a | website |  | fourlis.com | Fail (hard) | CORE-01: PDF link without #page=; CORE-02: no quote in the note |
| general-de-alquiler-de-maquinaria-s-a | fte |  | 1946 | Fail (hard) | CORE-02: 1946 not in the quote |
| general-de-alquiler-de-maquinaria-s-a | share_price |  | 1.385 | Fail (hard) | CORE-02: 1.385 not in the quote; CORE-04: no period_end |
| gurit-holding-ag-02374e88 | aggregate_headcount | Other members | 4.1 | Fail (hard) | NUM-05: not a whole number |
| havas | benefits_value | Chairman and Chief Executive O | 1340727.92 | Fail (hard) | CORE-03: quote not in the source text |
| havas | benefits_value | Executive Director (Jean de Yt | 18027.53 | Fail (hard) | CORE-03: quote not in the source text |
| havas | benefits_value | Executive Director (Alfonso Ro | 119762.01 | Fail (hard) | CORE-03: quote not in the source text |
| havas | lti_vested | Chairman and Chief Executive O | 2566320 | Fail (hard) | CORE-03: quote not in the source text |
| havas | lti_vested | Executive Director (Jean de Yt | 139 | Fail (hard) | CORE-03: quote not in the source text |
| havas | lti_vested | Executive Director (Alfonso Ro | 120189 | Fail (hard) | CORE-03: quote not in the source text |
| havas | pension_contribution | Executive Director (Jean de Yt | 16975 | Fail (hard) | CORE-03: quote not in the source text |
| havas | total_remuneration | Chairman and Chief Executive O | 6907047.92 | Fail (hard) | CORE-03: quote not in the source text |
| havas | total_remuneration | Executive Director (Jean de Yt | 995141.53 | Fail (hard) | CORE-03: quote not in the source text |
| havas | total_remuneration | Executive Director (Alfonso Ro | 1269951.01 | Fail (hard) | CORE-03: quote not in the source text |
| hellenic-telecommunications-organization-s-a | role_disclosure | Senior Management Executives | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| hellenic-telecommunications-organization-s-a | shareholding_requirement |  | CEO: obligation to invest in D | Fail (hard) | CORE-03: quote not in the source text |
| hyloris | benefits_value | Co-CEO’s | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: quote not in the source text |
| hyloris | benefits_value | Other members of the Executive | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: quote not in the source text |
| hyloris | pension_contribution | Co-CEO’s | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| hyloris | pension_contribution | Other members of the Executive | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| ibersol-s-g-p-s-s-a | controlling_owner_name |  | ATPS – Sociedade Gestora de Pa | Fail (hard) | CORE-02: not in the quote: gestora participa sociais |
| igd-immobiliare-grande-distribuzione-siiq | headcount |  | 199 | Fail (hard) | CORE-02: 199 not in the quote; CORE-03: quote not in the source text |
| igd-immobiliare-grande-distribuzione-siiq | staff_by_country |  | Italy: 169; Romania: 30 | Fail (hard) | CORE-03: quote not in the source text |
| iktinos-hellas-s-a-greek-marble-industry-technical-and-touristic-company | headcount |  | 398 | Fail (hard) | CORE-03: quote not in the source text |
| iktinos-hellas-s-a-greek-marble-industry-technical-and-touristic-company | revenue_by_country |  | Ευρωζώνη: 1893948; Λοιπές Ευρω | Fail (hard) | CORE-03: quote not in the source text |
| indra-sistemas-s-a | share_price |  | 9.837 | Fail (hard) | CORE-02: 9.837 not in the quote |
| indra-sistemas-s-a | total_remuneration | Consejero Delegado | 1512000 | Fail (hard) | XF-01: parts add up to 1,937,000, more than the stated 1,512,000; XF-02: parts add up to 1,937,000, stated 1,512,000 |
| industrie-de-nora | staff_by_country |  | America: 576; Stati Uniti: 452 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 4,162 vs 2,081 (100.0% apart) |
| innovative-solutions-ecosystem-s-a | benefits_value | Presidente Dominical | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| it-way | staff_by_segment |  | Bestway Healthcare: 7000; Unit | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 31,750 vs 50,000 (36.5% apart) |
| italmobiliare | controlling_owner_name |  | Pesenti family | Fail (hard) | CORE-02: not in the quote: family |
| italmobiliare | staff_by_country |  | Italy: 1573; United Kingdom: 1 | Fail (hard) | CORE-03: quote not in the source text |
| j-b-ladenis-bros-s-a-minerva-knitwear-manufacturing-company | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| kbc-ancora | controlling_owner_name |  | Cera SC | Fail (hard) | CORE-02: not in the quote: sc |
| kendrion | benefits |  | car allowance or lease budget, | Fail (hard) | CORE-03: quote not in the source text |
| lamda-development-s-a | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| lamda-development-s-a | revenue_by_segment |  | Hellinikon: 465728; LAMDA Mall | Fail | CORE-04: no period_end; NUM-08: adds up to 665,021,000 vs 567,160,000 (17.3% apart) |
| lamda-development-s-a | staff_by_country |  | Greece: 769; Abroad: 3 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| lingotes-especiales-s-a | ebitda |  | 6860000 | Fail (hard) | CORE-02: 6.86 not in the quote |
| lingotes-especiales-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| magnum | lti_granted | Chief Executive Officer | 65912 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | accounting_basis |  | IFRS as adopted by the EU | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | base_salary | Chief Executive Officer (CEO) | 140000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | base_salary | Chief Financial Officer (CFO) | 133000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | base_salary | Chief Operating Officer (COO)  | 119000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | base_salary | Chief Operating Officer (COO)  | 119000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | benefits |  | health and personal accident i | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | benefits_value | Chief Executive Officer (CEO) | 63437 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | benefits_value | Chief Financial Officer (CFO) | 63451 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | benefits_value | Chief Operating Officer (COO)  | 58917 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | benefits_value | Chief Operating Officer (COO)  | 53878 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | controlling_owner |  | family | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | controlling_owner_name |  | I’M SGPS, S.A. | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market; CORE-03: quote not in the source text |
| martifer-sgps-s-a | fte |  | 1713 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | headcount |  | 1685 | Fail (hard) | CORE-02: 1685 not in the quote |
| martifer-sgps-s-a | largest_holders |  | I’M SGPS, S.A. 38.01%; Mota-En | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | listing_date |  | 2007 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | ownership_type |  | family_owned | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | pension_type |  | The remuneration policy allows | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | revenue |  | 296400000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | role_disclosure | Chief Executive Officer (CEO) | individual | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | role_disclosure | Chief Financial Officer (CFO) | individual | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | role_disclosure | Chief Operating Officer (COO)  | individual | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | role_disclosure | Chief Operating Officer (COO)  | individual | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | shares_outstanding |  | 95568180 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | staff_by_country |  | Angola: 235; Argentina: 1; Esp | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | sti_max | Chief Executive Officer (CEO) | 5 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| martifer-sgps-s-a | sti_max | Chief Financial Officer (CFO) | 5 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| martifer-sgps-s-a | sti_max | Chief Operating Officer (COO)  | 5 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| martifer-sgps-s-a | sti_max | Chief Operating Officer (COO)  | 5 | Fail (hard) | CORE-03: quote not in the source text; COD-01: unit '' is not a target form |
| martifer-sgps-s-a | sti_paid | Chief Executive Officer (CEO) | 178000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | sti_paid | Chief Financial Officer (CFO) | 105000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | sti_paid | Chief Operating Officer (COO)  | 105000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | sti_paid | Chief Operating Officer (COO)  | 90000 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | sub_sector |  | centrado na engenharia e que a | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | total_remuneration | Chief Executive Officer (CEO) | 441437 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 381,437, stated 441,437 |
| martifer-sgps-s-a | total_remuneration | Chief Financial Officer (CFO) | 351441 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 301,451, stated 351,441 |
| martifer-sgps-s-a | total_remuneration | Chief Operating Officer (COO)  | 319584 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 282,917, stated 319,584 |
| martifer-sgps-s-a | total_remuneration | Chief Operating Officer (COO)  | 262878 | Fail (hard) | CORE-03: quote not in the source text |
| martifer-sgps-s-a | website |  | martifer.pt | Fail (hard) | CORE-03: quote not in the source text |
| miko | aggregate_headcount | EXCO Members | 7.3 | Fail (hard) | NUM-05: not a whole number |
| miko | total_remuneration | Executive Director | 311763.47 | Fail (hard) | XF-01: parts add up to 361,885, more than the stated 311,763; XF-02: parts add up to 361,885, stated 311,763 |
| montebalito-s-a | largest_holders |  | José Alberto Barreras Barreras | Fail (hard) | NUM-07: holdings add up to 183.1% |
| nextensa | aggregate_headcount | Other members of the executive | 3 | Fail (hard) | CORE-03: quote not in the source text |
| nextensa | lti_granted | Other members of the executive | 35000 | Fail (hard) | CORE-02: 35000 not in the quote |
| nn-group | base_salary | Other members of the Managemen | 6294000 | Fail (hard) | CORE-02: 6294 not in the quote |
| nn-group | lti_granted | Chair, Chief Executive Officer | 195000 | Fail (hard) | CORE-02: 195 not in the quote |
| nn-group | lti_granted | Vice-chair, Chief Financial Of | 132000 | Fail (hard) | CORE-02: 132 not in the quote |
| nn-group | lti_granted | Other members of the Managemen | 530000 | Fail (hard) | CORE-02: 530 not in the quote |
| nn-group | lti_max | Chair, Chief Executive Officer | 12 | Fail (hard) | CORE-02: 12 not in the quote |
| nn-group | lti_max | Vice-chair, Chief Financial Of | 12 | Fail (hard) | CORE-02: 12 not in the quote |
| nn-group | lti_max | Other members of the Managemen | 12 | Fail (hard) | CORE-02: 12 not in the quote |
| nn-group | lti_target | Chair, Chief Executive Officer | 9.6 | Fail (hard) | CORE-02: 9.6 not in the quote |
| nn-group | lti_target | Vice-chair, Chief Financial Of | 9.6 | Fail (hard) | CORE-02: 9.6 not in the quote |
| nn-group | lti_target | Other members of the Managemen | 9.6 | Fail (hard) | CORE-02: 9.6 not in the quote |
| nn-group | sti_max | Other members of the Managemen | 8 | Fail (hard) | CORE-02: 8 not in the quote |
| nn-group | sti_target | Other members of the Managemen | 6.4 | Fail (hard) | CORE-02: 6.4 not in the quote |
| novabase-sociedade-gestora-de-participacoes-sociais-s-a | share_price |  | 8.75 | Fail (hard) | CORE-02: 8.75 not in the quote |
| oci | total_remuneration | Executive Chair | 1050000 | Fail (hard) | XF-01: parts add up to 1,260,000, more than the stated 1,050,000; XF-02: parts add up to 1,260,000, stated 1,050,000 |
| orell-fussli-ag-c5631ff9 | pension_type |  | defined contribution, paritäti | Fail (hard) | CORE-03: quote not in the source text |
| prosegur-compania-de-seguridad-s-a | sub_sector |  | Prosegur operates in business  | Fail (hard) | CORE-03: quote not in the source text |
| randstad-nv | lti_max | CEO and Chair of the Executive | 350 | Fail (hard) | CORE-02: 350 not in the quote |
| randstad-nv | lti_max | CFO | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| randstad-nv | lti_max | CHRO | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| randstad-nv | lti_max | COO | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| renta-corporacion-real-estate-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| renta-corporacion-real-estate-s-a | listing_date |  | April 2006 | Fail (hard) | COD-06: not a year, a year and month, or a date |
| renta-corporacion-real-estate-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| revoil-s-a | revenue_by_segment |  | Τομέας Καυσίμων & Λοιπών Παροχ | Fail (hard) | CORE-03: quote not in the source text |
| signify-nv | lti_max | CEO (from September 1, 2025) | 160 | Fail (hard) | CORE-02: 160 not in the quote |
| signify-nv | lti_max | CFO | 160 | Fail (hard) | CORE-02: 160 not in the quote |
| signify-nv | lti_max | CEO of Professional Business ( | 160 | Fail (hard) | CORE-02: 160 not in the quote |
| signify-nv | role_disclosure | CEO (from September 1, 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| signify-nv | role_disclosure | Former CEO (until April 25, 20 | individual | Fail (hard) | CORE-03: quote not in the source text |
| signify-nv | role_disclosure | CEO of Professional Business ( | individual | Fail (hard) | CORE-03: quote not in the source text |
| solaria-energia-y-medio-ambiente-s-a | base_salary | Consejero Ejecutivo | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| solaria-energia-y-medio-ambiente-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| solaria-energia-y-medio-ambiente-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| solaria-energia-y-medio-ambiente-s-a | revenue |  | 600000000 | Fail (hard) | CORE-03: quote not in the source text |
| solaria-energia-y-medio-ambiente-s-a | total_assets |  | 1990000000 | Fail (hard) | CORE-03: quote not in the source text |
| solaria-energia-y-medio-ambiente-s-a | total_remuneration | Consejero Ejecutivo | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| solvac | benefits |  | reimbursement of travel expens | Fail (hard) | CORE-03: quote not in the source text |
| sport-lisboa-e-benfica-futebol-sad | benefits |  | protocol benefits inherent to  | Fail (hard) | CORE-03: quote not in the source text |
| sport-lisboa-e-benfica-futebol-sad | ebitda |  | 32400000 | Fail (hard) | CORE-03: quote not in the source text |
| sport-lisboa-e-benfica-futebol-sad | sti_max | Administrador Executivo/Vice-P | 40 | Fail (hard) | COD-01: unit '' is not a target form |
| talgo-s-a | benefits |  | company car, life insurance, h | Fail (hard) | CORE-03: quote not in the source text |
| technical-olympic-s-a | benefits |  | use of company vehicle, health | Fail (hard) | CORE-03: quote not in the source text |
| technical-olympic-s-a | pension_type |  | defined contribution | Fail (hard) | CORE-03: quote not in the source text |
| tessellis | listing_date |  | October 1999 | Fail (hard) | COD-06: not a year, a year and month, or a date |
| tessellis | pension_type |  | defined contribution | Fail (hard) | CORE-03: quote not in the source text |
| the-navigator-company-s-a | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| thrace-plastics-holding-company-s-a | largest_holders |  | Κωνσταντίνος Χαλιορής 43.29%;  | Fail (hard) | NUM-07: holdings add up to 106.26% |
| tinc | exchange_segment |  | Continuous market | Fail (hard) | CORE-02: not in the quote: continuous market |
| tinc | revenue |  | 150000000 | Fail (hard) | CORE-03: quote not in the source text |
| trevi-finanziaria-industriale | controlling_owner_name |  | CDP Equity S.p.A. | Fail (hard) | CORE-02: not in the quote: equity |
| tubacex-s-a | share_price |  | 3.335 | Fail (hard) | CORE-02: 3.335 not in the quote |
| v-lanschot-kempen | largest_holders |  | Stichting Administratiekantoor | Fail (hard) | NUM-07: holdings add up to 149.73% |
| viscofan-s-a | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| viscofan-s-a | ebitda |  | 289990000 | Fail (hard) | CORE-02: 289990 not in the quote |
| viscofan-s-a | lti_granted | Consejero Delegado | 41577 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts EUR |
| viscofan-s-a | lti_vested | Consejero Delegado | 0 | Fail (hard) | CORE-03: quote not in the source text |
| viscofan-s-a | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| vopak | controlling_owner_name |  | HAL Holding N.V. | Fail (hard) | CORE-02: not in the quote: holding n v |
| vopak | total_remuneration | Chairman Executive Board and C | 3685200 | Fail (hard) | XF-01: parts add up to 3,892,800, more than the stated 3,685,200; XF-02: parts add up to 3,892,800, stated 3,685,200 |
| vopak | total_remuneration | Member of the Executive Board  | 2567700 | Fail (hard) | XF-01: parts add up to 2,705,500, more than the stated 2,567,700; XF-02: parts add up to 2,705,500, stated 2,567,700 |
| wool-industry-tria-alfa-s-a | lti_granted | Members of the Board of Direct | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| wool-industry-tria-alfa-s-a | role_disclosure | Members of the Board of Direct | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| xior | lti_max | CEO | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| xior | lti_max | Other members of the executive | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| xior | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
