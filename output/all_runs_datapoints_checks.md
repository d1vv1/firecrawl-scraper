# Output checks: all_runs_datapoints.csv

244 companies, 12031 filled values checked (2026-11-06, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 9745 (81%) |
| Review | 667 (6%) |
| Fail | 454 (4%) |
| Fail (hard) | 1165 (10%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 1468 | 1458 | 0 | 0 | 10 |
| Listing and market | 1138 | 1108 | 0 | 0 | 30 |
| Sector | 381 | 372 | 0 | 0 | 9 |
| Reporting basis | 792 | 789 | 0 | 0 | 3 |
| Financials | 848 | 670 | 72 | 0 | 106 |
| Workforce | 279 | 199 | 33 | 0 | 47 |
| Ownership and control | 876 | 640 | 44 | 141 | 51 |
| Segment and geography | 336 | 159 | 14 | 89 | 74 |
| Pay policy | 510 | 473 | 0 | 0 | 37 |
| Role and disclosure | 1557 | 1203 | 12 | 224 | 118 |
| Pay: fixed | 1512 | 1024 | 187 | 0 | 301 |
| Pay: STI | 952 | 730 | 107 | 0 | 115 |
| Pay: LTI | 806 | 601 | 64 | 0 | 141 |
| Pay: total | 576 | 319 | 134 | 0 | 123 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 12031 | 12025 | 6 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 5168 | 4819 | 349 | 6863 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 3539 | 2863 | 676 | 8492 | source not cached; the run itself did not find the quote |
| CORE-04 | Period end present (dated fields only) |  | 6739 | 5602 | 1137 | 5292 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 12031 | 12029 | 2 | 0 | period_end 'N December' is not a date |
| COD-01 | Value in its code list or closed set | yes | 3820 | 3788 | 32 | 8211 | US$ is not ISO N |
| COD-02 | Classification scheme named |  | 174 | 174 | 0 | 11857 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 434 | 434 | 0 | 11597 |  |
| COD-06 | Dates are valid | yes | 341 | 334 | 7 | 11690 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 3641 | 3504 | 137 | 8390 | unit 'US$' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 3337 | 3337 | 0 | 8694 |  |
| NUM-04 | Magnitude in a plausible range |  | 4190 | 4178 | 12 | 7841 | Ne+N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 404 | 402 | 2 | 11627 | not a whole number |
| NUM-06 | Percentages in range | yes | 757 | 756 | 1 | 11274 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 162 | 160 | 2 | 11869 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 304 | 228 | 76 | 11727 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 486 | 486 | 0 | 11545 |  |
| NUM-11 | STI paid not above its maximum |  | 233 | 218 | 15 | 11798 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 2971 | 2943 | 28 | 9060 | currency N the role's other amounts GBP |
| NUM-13 | FTE not above headcount |  | 103 | 90 | 13 | 11928 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 77 | 77 | 0 | 11954 |  |
| DER-06 | Derived value shows its formula |  | 355 | 355 | 0 | 11676 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 506 | 486 | 20 | 11525 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 506 | 392 | 114 | 11525 | parts add up to N stated N |

## Fill rate

Company fields: 6628 of 10004 filled (66%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 25 | 244 |
| staff_by_segment | 40 | 244 |
| market_cap_band | 57 | 244 |
| staff_by_country | 72 | 244 |
| controlling_owner_name | 94 | 244 |
| revenue_by_country | 104 | 244 |
| share_price | 111 | 244 |
| exchange_segment | 113 | 244 |
| shareholding_requirement | 118 | 244 |
| revenue_by_segment | 120 | 244 |
| other_names | 126 | 244 |
| headcount | 134 | 244 |
| listing_date | 136 | 244 |
| fte | 145 | 244 |
| pe_stake_5pct | 148 | 244 |
| controlling_owner | 151 | 244 |
| ownership_type | 151 | 244 |
| largest_holders | 162 | 244 |
| ultimate_parent | 170 | 244 |
| sector_code | 174 | 244 |
| ebitda | 174 | 244 |
| shares_outstanding | 178 | 244 |
| fiscal_year | 189 | 244 |
| total_assets | 192 | 244 |
| accounting_basis | 192 | 244 |
| benefits | 192 | 244 |
| revenue | 193 | 244 |
| isin | 194 | 244 |
| pension_type | 200 | 244 |
| website | 202 | 244 |
| ticker | 205 | 244 |
| fiscal_year_end | 205 | 244 |
| reporting_currency | 206 | 244 |
| sub_sector | 207 | 244 |
| lei | 215 | 244 |
| exchange | 216 | 244 |
| listing_status | 217 | 244 |
| legal_name | 225 | 244 |
| business_id | 225 | 244 |
| country_code | 225 | 244 |
| head_office_city | 225 | 244 |

Pay fields, over 655 executive roles:

| Field | Filled |
|---|---|
| base_salary | 570 (87%) |
| sti_paid | 462 (71%) |
| sti_target | 156 (24%) |
| sti_max | 334 (51%) |
| lti_vested | 213 (33%) |
| lti_granted | 273 (42%) |
| lti_target | 102 (16%) |
| lti_max | 218 (33%) |
| benefits_value | 457 (70%) |
| pension_contribution | 485 (74%) |
| total_remuneration | 576 (88%) |

## Failed values (1619)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 4imprint-group-plc | revenue_by_segment |  | North America: 1321.5; UK & Ir | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| 4imprint-group-plc | share_price |  | 4474 | Fail (hard) | NUM-01: unit 'GBX' is not ISO 4217 |
| 4imprint-group-plc | total_assets |  | 308900000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0002 | base_salary | Direktionen | 23200000 | Fail (hard) | CORE-02: 23.2 not in the quote |
| T0002 | pay_currency | Direktionen | DKK | Fail | CORE-04: no period_end |
| T0002 | revenue |  | 7548000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0002 | revenue_by_country |  | Danmark: 7109; Udlandet: 386 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0002 | revenue_by_segment |  | Bankaktiviteter: 6654; Kapital | Fail | CORE-04: no period_end |
| T0002 | staff_by_country |  | Danmark: 2023; Tyskland: 71 | Fail | CORE-04: no period_end |
| T0002 | staff_by_segment |  | Bankaktiviteter: 1928; Kapital | Fail | CORE-04: no period_end |
| T0002 | total_remuneration | Direktionen | 23700000 | Fail (hard) | CORE-02: 23.7 not in the quote; XF-01: parts add up to 24,200,000, more than the stated 23,700,000; XF-02: parts add up to 24,200,000, stated 23,700,000 |
| T0011 | base_salary | Verkställande direktör | 14600000 | Fail (hard) | CORE-02: 14.6 not in the quote |
| T0011 | base_salary | Vice verkställande direktör (C | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote |
| T0011 | base_salary | Vice verkställande direktör (P | 9600000 | Fail (hard) | CORE-02: 9.6 not in the quote |
| T0011 | base_salary | Övrig verkställande ledning | 29600000 | Fail (hard) | CORE-02: 29.6 not in the quote |
| T0011 | benefits_value | Verkställande direktör | 100000 | Fail (hard) | CORE-02: 0.1 not in the quote |
| T0011 | benefits_value | Vice verkställande direktör (C | 200000 | Fail (hard) | CORE-02: 0.2 not in the quote |
| T0011 | benefits_value | Vice verkställande direktör (P | 300000 | Fail (hard) | CORE-02: 0.3 not in the quote |
| T0011 | benefits_value | Övrig verkställande ledning | 1800000 | Fail (hard) | CORE-02: 1.8 not in the quote |
| T0011 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0011 | ebitda |  | 30750000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0011 | listing_date |  | 1871 | Fail (hard) | COD-06: not a year or a date |
| T0011 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0011 | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| T0011 | pay_currency | Vice verkställande direktör (C | SEK | Fail | CORE-04: no period_end |
| T0011 | pay_currency | Vice verkställande direktör (P | SEK | Fail | CORE-04: no period_end |
| T0011 | pay_currency | Övrig verkställande ledning | SEK | Fail | CORE-04: no period_end |
| T0011 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0011 | pension_contribution | Verkställande direktör | 5100000 | Fail (hard) | CORE-02: 5.1 not in the quote |
| T0011 | pension_contribution | Vice verkställande direktör (C | 1600000 | Fail (hard) | CORE-02: 1.6 not in the quote |
| T0011 | pension_contribution | Vice verkställande direktör (P | 3400000 | Fail (hard) | CORE-02: 3.4 not in the quote |
| T0011 | revenue_by_country |  | Sverige: 37482; Storbritannien | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0011 | revenue_by_segment |  | Sverige: 36109; Storbritannien | Fail | CORE-04: no period_end |
| T0011 | staff_by_segment |  | Sverige: 4602; Storbritannien: | Fail | CORE-04: no period_end |
| T0011 | sub_sector |  | Vi ska ge det bästa erbjudande | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0011 | ticker |  | SHB A | Fail (hard) | CORE-02: not in the quote: shb; CORE-03: source not cached; the run itself did not find the quote |
| T0011 | total_remuneration | Verkställande direktör | 19800000 | Fail (hard) | CORE-02: 19.8 not in the quote |
| T0011 | total_remuneration | Vice verkställande direktör (C | 7600000 | Fail (hard) | CORE-02: 7.6 not in the quote |
| T0011 | total_remuneration | Vice verkställande direktör (P | 13300000 | Fail (hard) | CORE-02: 13.3 not in the quote |
| T0011 | total_remuneration | Övrig verkställande ledning | 44600000 | Fail (hard) | CORE-02: 44.6 not in the quote; XF-02: parts add up to 38,400,000, stated 44,600,000 |
| T0013 | aggregate_headcount | Total Management Team | 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0013 | base_salary | Chief Executive Officer | 2354000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | base_salary | Chief Technology Officer | 2164000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | base_salary | Chief Operating Officer | 1847000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | base_salary | Total Management Team | 10171000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | benefits |  | other fixed benefits, benefits | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | benefits_value | Chief Executive Officer | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | benefits_value | Chief Technology Officer | 3000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | benefits_value | Chief Operating Officer | 20000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | benefits_value | Total Management Team | 590000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0013 | lti_vested | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0013 | lti_vested | Chief Technology Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0013 | lti_vested | Chief Operating Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0013 | lti_vested | Total Management Team | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Chief Executive Officer | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Chief Financial Officer | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Chief Scientific Officer | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Chief Technology Officer | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Chief Operating Officer | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Total Management Team | NOK | Fail | CORE-04: no period_end |
| T0013 | pay_currency | Management Team | NOK | Fail | CORE-04: no period_end |
| T0013 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0013 | pension_contribution | Chief Executive Officer | 90000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | pension_contribution | Chief Technology Officer | 95000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | pension_contribution | Chief Operating Officer | 476000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | pension_contribution | Total Management Team | 662000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_paid | Chief Executive Officer | 561000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_paid | Chief Technology Officer | 197000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_paid | Chief Operating Officer | 184000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_paid | Total Management Team | 1557000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_target | Chief Executive Officer | 50 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_target | Chief Financial Officer | 35 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_target | Chief Scientific Officer | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_target | Chief Technology Officer | 20 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | sti_target | Chief Operating Officer | 20 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | total_remuneration | Chief Executive Officer | 3021000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | total_remuneration | Chief Technology Officer | 2459000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | total_remuneration | Chief Operating Officer | 2528000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0013 | total_remuneration | Total Management Team | 12980000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0023 | benefits |  | restricted stock units, option | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0023 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0023 | controlling_owner_name |  | Scatec Innovation AS | Fail | CORE-04: no period_end |
| T0023 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0023 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0038 | base_salary | CEO | 3403000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | base_salary | Deputy CEO | 2374000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | benefits_value | CEO | 109000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | benefits_value | Deputy CEO | 79000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0038 | lti_vested | CEO | 1265000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | lti_vested | Deputy CEO | 226000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0038 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0038 | pay_currency | Deputy CEO | SEK | Fail | CORE-04: no period_end |
| T0038 | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| T0038 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0038 | pension_contribution | CEO | 1018000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | pension_contribution | Deputy CEO | 931000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | staff_by_country |  | Sweden: 128; Germany: 1; Norwa | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 131 vs 154 (14.9% apart) |
| T0038 | sti_paid | CEO | 681000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | sti_paid | Deputy CEO | 464000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | total_remuneration | CEO | 6476000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0038 | total_remuneration | Deputy CEO | 4074000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0047 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0047 | controlling_owner_name |  | ES – PARKEN ApS | Fail | CORE-04: no period_end |
| T0047 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0047 | pay_currency | koncerndirektør | DKK | Fail | CORE-04: no period_end |
| T0047 | pay_currency | direktør | DKK | Fail | CORE-04: no period_end |
| T0047 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0047 | revenue_by_country |  | Denmark: 1884619 | Fail | CORE-04: no period_end |
| T0047 | revenue_by_segment |  | Lalandia: 835134.96; Parken Ej | Fail | CORE-04: no period_end |
| T0047 | staff_by_country |  | Denmark: 4008 | Fail | CORE-04: no period_end |
| T0083 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0083 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0083 | pay_currency | CEO | DKK | Fail | CORE-04: no period_end |
| T0083 | pay_currency | Other members of group managem | DKK | Fail | CORE-04: no period_end |
| T0083 | pe_stake_5pct |  | yes | Fail | CORE-04: no period_end |
| T0083 | revenue_by_country |  | AMERICAS: 101553; ROW: 45056 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0083 | revenue_by_segment |  | SMARTNIC PRODUCTS: 141903; ENG | Fail | CORE-04: no period_end |
| T0089 | accounting_basis |  | IFRS som antagits av EU | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0089 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0089 | headcount |  | 7 | Fail (hard) | CORE-02: 7 not in the quote |
| T0089 | lti_granted | Koncernens ledande befattnings | 245000 | Fail (hard) | CORE-02: 245 not in the quote |
| T0089 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0089 | pay_currency | CEO | USD | Fail | CORE-04: no period_end |
| T0089 | pay_currency | Koncernens ledande befattnings | USD | Fail | CORE-04: no period_end |
| T0089 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0090 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0090 | controlling_owner_name |  | L E Lundbergföretagen | Fail | CORE-04: no period_end |
| T0090 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0090 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0090 | pay_currency | Deputy Chief Executive Officer | SEK | Fail | CORE-04: no period_end |
| T0090 | pay_currency | Other members of Executive Man | SEK | Fail | CORE-04: no period_end |
| T0090 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0090 | staff_by_country |  | Sweden: 15 | Fail | CORE-04: no period_end |
| T0099 | pay_currency | CEO | DKK | Fail | CORE-04: no period_end |
| T0099 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0139 | base_salary | VD | 3294000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | base_salary | Andra ledande befattningshavar | 1875000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | benefits_value | VD | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | benefits_value | Andra ledande befattningshavar | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0139 | controlling_owner_name |  | Mikael Ahlström | Fail | CORE-04: no period_end |
| T0139 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0139 | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| T0139 | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| T0139 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0139 | pension_contribution | VD | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | pension_contribution | Andra ledande befattningshavar | 395000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | role_disclosure | Board (non-executive) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | role_disclosure | VD | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | role_disclosure | Andra ledande befattningshavar | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | sti_paid | VD | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | sti_paid | Andra ledande befattningshavar | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | total_remuneration | VD | 3296000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0139 | total_remuneration | Andra ledande befattningshavar | 2270000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0143 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0143 | controlling_owner_name |  | Skeie Technology AS | Fail | CORE-04: no period_end |
| T0143 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0143 | pay_currency | CEO | NOK | Fail | CORE-04: no period_end |
| T0143 | pay_currency | Chief Financial Officer | NOK | Fail | CORE-04: no period_end |
| T0143 | pay_currency | EVP Nekkar and CEO Techano Oce | NOK | Fail | CORE-04: no period_end |
| T0143 | pay_currency | Head of Strategy | NOK | Fail | CORE-04: no period_end |
| T0143 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0143 | revenue_by_segment |  | Syncrolift: 315; Intellilift:  | Fail | CORE-04: no period_end; NUM-08: adds up to 606,000,000 vs 571,087,000 (6.1% apart) |
| T0143 | staff_by_segment |  | Syncrolift: 55; Intellilift: 1 | Fail | CORE-04: no period_end; NUM-08: adds up to 125 vs 8 (1462.5% apart) |
| T0149 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0149 | controlling_owner_name |  | Ferd AS | Fail | CORE-04: no period_end |
| T0149 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0149 | pay_currency | Executive Management Board | EUR | Fail | CORE-04: no period_end |
| T0149 | pay_currency | Nilfisk Leadership Team | EUR | Fail | CORE-04: no period_end |
| T0149 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0149 | revenue_by_country |  | USA: 243.1; Germany: 146.8; Fr | Fail | CORE-04: no period_end |
| T0149 | revenue_by_segment |  | Professional Business: 558.1;  | Fail | CORE-04: no period_end |
| T0149 | staff_by_country |  | Hungary: 828; China: 570; US:  | Fail | CORE-04: no period_end |
| T0149 | website |  | nilfisk.com | Fail (hard) | CORE-02: not in the quote: nilfisk com |
| T0157 | base_salary | Chief Executive Officer | 528000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | Deputy CEO & CFO | 418000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | Chief Sales and Marketing Offi | 298000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | Director of Human Resources | 195000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | Chief Operating Officer (From  | 98000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | Chief Manufacturing Officer (F | 172000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | base_salary | COO (Until June 2025) | 201000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | benefits_value | Chief Operating Officer (From  | 22000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: market |
| T0157 | lti_vested | COO (Until June 2025) | 69000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | pay_currency | Chief Executive Officer | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Deputy CEO & CFO | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Chief Sales and Marketing Offi | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Director of Human Resources | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Chief Operating Officer (From  | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Chief Manufacturing Officer (F | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | COO (Until June 2025) | USD | Fail | CORE-04: no period_end |
| T0157 | pay_currency | Rest of management team | USD | Fail | CORE-04: no period_end |
| T0157 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0157 | pension_contribution | Chief Executive Officer | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | pension_contribution | Deputy CEO & CFO | 14000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | pension_contribution | Chief Sales and Marketing Offi | 12000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | pension_contribution | Director of Human Resources | 8000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | pension_contribution | Chief Operating Officer (From  | 5000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | revenue_by_segment |  | Denmark operations: 0; US oper | Fail | CORE-04: no period_end |
| T0157 | sti_paid | Chief Operating Officer (From  | 21000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Chief Executive Officer | 542000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Deputy CEO & CFO | 432000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Chief Sales and Marketing Offi | 310000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Director of Human Resources | 203000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Chief Operating Officer (From  | 146000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | Chief Manufacturing Officer (F | 172000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0157 | total_remuneration | COO (Until June 2025) | 270000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0159 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0159 | lti_vested | Verkställande direktören | 300000 | Fail (hard) | CORE-02: 0.3 not in the quote |
| T0159 | lti_vested | Ekonomichefen | 100000 | Fail (hard) | CORE-02: 0.1 not in the quote |
| T0159 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0159 | pay_currency | Verkställande direktören | SEK | Fail | CORE-04: no period_end |
| T0159 | pay_currency | Ekonomichefen | SEK | Fail | CORE-04: no period_end |
| T0159 | pension_contribution | Verkställande direktören | 1400000 | Fail (hard) | CORE-02: 1.4 not in the quote |
| T0159 | pension_contribution | Ekonomichefen | 800000 | Fail (hard) | CORE-02: 0.8 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0159 | sti_paid | Verkställande direktören | 6900000 | Fail (hard) | CORE-02: 6.9 not in the quote |
| T0159 | sti_paid | Ekonomichefen | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote |
| T0159 | total_remuneration | Verkställande direktören | 11700000 | Fail (hard) | CORE-02: 11.7 not in the quote; XF-02: parts add up to 8,600,000, stated 11,700,000 |
| T0159 | total_remuneration | Ekonomichefen | 2400000 | Fail (hard) | CORE-02: 2.4 not in the quote; XF-02: parts add up to 1,800,000, stated 2,400,000 |
| T0174 | base_salary | CEO | 3062000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0174 | base_salary | Deputy CEO | 1877000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0174 | benefits_value | CEO | 15000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0174 | benefits_value | Deputy CEO | 3000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0174 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0174 | controlling_owner_name |  | invoX Pharma Ltd | Fail | CORE-04: no period_end |
| T0174 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0174 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0174 | pay_currency | Deputy CEO | SEK | Fail | CORE-04: no period_end |
| T0174 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0174 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0174 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0174 | pension_contribution | CEO | 992000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0174 | pension_contribution | Deputy CEO | 458000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0174 | revenue_by_country |  | Sweden: 1838 | Fail | CORE-04: no period_end |
| T0206 | base_salary | CEO | 2378000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0206 | benefits_value | CEO | 24000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0206 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0206 | ebitda |  | -173900000 | Fail (hard) | CORE-02: -173.9 not in the quote; CORE-04: no period_end |
| T0206 | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| T0206 | lti_vested | CEO | 834000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0206 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0206 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0206 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0206 | pension_contribution | CEO | 972000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0206 | share_price |  | 1.85 | Fail (hard) | CORE-02: 1.85 not in the quote |
| T0206 | sti_paid | CEO | 635000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0206 | total_remuneration | CEO | 4843000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0233 | base_salary | Administrerende Direktør | 400000 | Fail (hard) | CORE-02: 0.4 not in the quote |
| T0233 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0233 | controlling_owner_name |  | Olav W. Hansen A/S | Fail | CORE-04: no period_end |
| T0233 | ebitda |  | -2500000 | Fail (hard) | CORE-02: -2.5 not in the quote; CORE-04: no period_end |
| T0233 | fte |  | 1 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0233 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| T0233 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0233 | pay_currency | Administrerende Direktør | DKK | Fail | CORE-04: no period_end |
| T0233 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0255 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0255 | controlling_owner_name |  | Per Arwidsson | Fail | CORE-04: no period_end |
| T0255 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0255 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0255 | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| T0255 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0255 | pension_type |  | defined contribution, 10 perce | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0255 | revenue_by_country |  | USA: 0; Ryssland: 0; Sverige:  | Fail | CORE-04: no period_end |
| T0255 | staff_by_country |  | Sverige: 18 | Fail | CORE-04: no period_end |
| T0255 | sub_sector |  | Vivestos verksamhet består frä | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0262 | controlling_owner_name |  | Starboard | Fail | CORE-04: no period_end |
| T0262 | ebitda |  | -11872000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0262 | pay_currency | Verkställande direktör och Chi | USD | Fail | CORE-04: no period_end |
| T0262 | pay_currency | Former Verkställande direktör  | USD | Fail | CORE-04: no period_end |
| T0262 | pay_currency | Chief Legal Officer | USD | Fail | CORE-04: no period_end |
| T0262 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0262 | staff_by_country |  | Brazil: 17 | Fail | CORE-04: no period_end |
| T0292 | base_salary | CEO | 3900000 | Fail (hard) | CORE-02: 3.9 not in the quote |
| T0292 | base_salary | Other senior executives | 5300000 | Fail (hard) | CORE-02: 5.3 not in the quote |
| T0292 | base_salary | Övriga ledande befattningshava | 5300000 | Fail (hard) | CORE-02: 5.3 not in the quote |
| T0292 | benefits_value | CEO | 1200000 | Fail (hard) | CORE-02: 1.2 not in the quote |
| T0292 | benefits_value | Other senior executives | 200000 | Fail (hard) | CORE-02: 0.2 not in the quote |
| T0292 | benefits_value | Övriga ledande befattningshava | 200000 | Fail (hard) | CORE-02: 0.2 not in the quote |
| T0292 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0292 | controlling_owner_name |  | Thomas Eldered | Fail | CORE-04: no period_end |
| T0292 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0292 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0292 | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| T0292 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0292 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0292 | pension_contribution | CEO | 700000 | Fail (hard) | CORE-02: 0.7 not in the quote |
| T0292 | pension_contribution | Other senior executives | 1100000 | Fail (hard) | CORE-02: 1.1 not in the quote |
| T0292 | pension_contribution | Övriga ledande befattningshava | 1100000 | Fail (hard) | CORE-02: 1.1 not in the quote |
| T0292 | share_price |  | 37.45 | Fail (hard) | CORE-02: 37.45 not in the quote |
| T0292 | total_remuneration | CEO | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote |
| T0292 | total_remuneration | Other senior executives | 6600000 | Fail (hard) | CORE-02: 6.6 not in the quote |
| T0292 | total_remuneration | Övriga ledande befattningshava | 6600000 | Fail (hard) | CORE-02: 6.6 not in the quote |
| T0295 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0295 | controlling_owner_name |  | Sjuenda Holding AB/Peter Theli | Fail | CORE-04: no period_end |
| T0295 | ebitda |  | -37600000 | Fail (hard) | CORE-02: -37.6 not in the quote; CORE-04: no period_end |
| T0295 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0295 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0295 | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| T0295 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0295 | revenue_by_country |  | Sweden: 0 | Fail | CORE-04: no period_end |
| T0295 | revenue_by_segment |  | Total Group: 0 | Fail | CORE-04: no period_end |
| T0295 | share_price |  | 0.046 | Fail (hard) | CORE-02: 0.046 not in the quote |
| T0295 | staff_by_country |  | Sweden: 5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0295 | staff_by_segment |  | Total Group: 5 | Fail | CORE-04: no period_end |
| T0299 | aggregate_headcount | Övriga ledande befattningshava | 4 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | base_salary | VD | 3062000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | base_salary | Övriga ledande befattningshava | 7715000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | benefits_value | VD | 112000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | benefits_value | Övriga ledande befattningshava | 394000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0299 | exchange_segment |  | Small Cap | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | lti_granted | VD | 0 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts SEK |
| T0299 | lti_granted | Övriga ledande befattningshava | 45867 | Fail (hard) | CORE-02: 45867 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0299 | lti_vested | VD | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts SEK |
| T0299 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0299 | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| T0299 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0299 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0299 | pension_contribution | VD | 917000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | pension_contribution | Övriga ledande befattningshava | 264000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | role_disclosure | Övriga ledande befattningshava | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | share_price |  | 31.45 | Fail (hard) | CORE-02: 31.45 not in the quote |
| T0299 | sti_paid | VD | 410000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | sti_paid | Övriga ledande befattningshava | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | sub_sector |  | Xspray Pharma utvecklar protei | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0299 | total_remuneration | VD | 4502000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0299 | total_remuneration | Övriga ledande befattningshava | 11394000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 8,384,000, stated 11,394,000 |
| T0325 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0325 | controlling_owner_name |  | Kunlun | Fail | CORE-04: no period_end |
| T0325 | ebitda |  | 227000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0325 | fte |  | 3.6 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0325 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0325 | pay_currency | CEO | USD | Fail | CORE-04: no period_end |
| T0325 | pay_currency | CFO | USD | Fail | CORE-04: no period_end |
| T0325 | pay_currency | Board and CEO Advisor | USD | Fail | CORE-04: no period_end |
| T0325 | revenue_by_segment |  | Advertising: 396040; Query: 21 | Fail | CORE-04: no period_end; NUM-08: adds up to 614,825,000 vs 2,535,000 (24153.5% apart) |
| T0325 | shares_outstanding |  | 73790829 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0325 | sub_sector |  | Otello primarily holds shares  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0325 | website |  | otellocorp.com | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0341 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0341 | controlling_owner_name |  | Infortar AS | Fail | CORE-04: no period_end |
| T0341 | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
| T0341 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| T0341 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0341 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0341 | revenue_by_segment |  | Sea and coastal freight water  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 119,500,000 vs 765,300,000 (84.4% apart) |
| T0341 | share_price |  | 0.69 | Fail (hard) | NUM-01: unit 'EURO' is not ISO 4217 |
| T0341 | staff_by_country |  | Estonia: 2944; Finland: 1007;  | Fail | CORE-04: no period_end |
| T0341 | website |  | company.tallink.com | Fail (hard) | CORE-02: not in the quote: company com |
| T0368 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0368 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0368 | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| T0368 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0368 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0368 | shares_outstanding |  | 127902580 | Fail (hard) | CORE-02: 127902580 not in the quote |
| T0368 | staff_by_country |  | Sweden: 11 | Fail | CORE-04: no period_end; NUM-08: adds up to 11 vs 10 (10.0% apart) |
| T0373 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0373 | controlling_owner_name |  | Oliver Molse | Fail | CORE-04: no period_end |
| T0373 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| T0373 | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| T0373 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0373 | pay_currency | interim Chief Executive Office | SEK | Fail | CORE-04: no period_end |
| T0373 | pay_currency | interim Chief Executive Office | SEK | Fail | CORE-04: no period_end |
| T0373 | pay_currency | CFO | SEK | Fail | CORE-04: no period_end |
| T0373 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0377 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0377 | lti_granted | Group CEO | 11500 | Fail (hard) | CORE-02: 11500 not in the quote |
| T0377 | lti_granted | Group CFO | 3900 | Fail (hard) | CORE-02: 3900 not in the quote |
| T0377 | lti_max | Group CEO | 125 | Fail (hard) | CORE-02: 125 not in the quote |
| T0377 | lti_max | Group CFO | 83 | Fail (hard) | CORE-02: 83 not in the quote |
| T0377 | lti_target | Group CFO | 83 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0377 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0377 | pay_currency | Group CEO | DKK | Fail | CORE-04: no period_end |
| T0377 | pay_currency | Group CFO | DKK | Fail | CORE-04: no period_end |
| T0377 | pay_currency | Executive Group Management Boa | DKK | Fail | CORE-04: no period_end |
| T0377 | pay_currency | Corporate Senior Officers | DKK | Fail | CORE-04: no period_end |
| T0377 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0377 | revenue_by_country |  | UK & Ireland: 12400; Switzerla | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0377 | revenue_by_segment |  | Northern Europe: 32286; Centra | Fail | CORE-04: no period_end |
| T0377 | role_disclosure | Group CEO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0377 | role_disclosure | Group CFO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0397 | benefits_value | CEO | 350753 | Fail (hard) | CORE-02: 350753 not in the quote |
| T0397 | benefits_value | CFO | 350753 | Fail (hard) | CORE-02: 350753 not in the quote |
| T0397 | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| T0397 | pay_currency | CFO | EUR | Fail | CORE-04: no period_end |
| T0397 | pay_currency | Executive management | EUR | Fail | CORE-04: no period_end |
| T0397 | revenue_by_country |  | Denmark: 102466; UK: 131679; G | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0397 | staff_by_country |  | Denmark: 638; United Kingdom:  | Fail | CORE-04: no period_end |
| T0398 | fte |  | 7 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0398 | largest_holders |  | Sanos Group NBCD A/S 10%; Avan | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0398 | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| T0398 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0398 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0398 | share_price |  | 22.6 | Fail (hard) | CORE-02: 22.6 not in the quote |
| T0398 | staff_by_country |  | Sverige: 2; Danmark: 5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0413 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0413 | controlling_owner_name |  | ANNWALL & ROTHSCHILD INVESTMEN | Fail | CORE-04: no period_end |
| T0413 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0413 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0413 | pay_currency | Other management | SEK | Fail | CORE-04: no period_end |
| T0413 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0413 | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0413 | staff_by_country |  | Sweden: 7 | Fail | CORE-04: no period_end; NUM-08: adds up to 7 vs 6 (16.7% apart) |
| T0423 | benefits_value | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0423 | benefits_value | Chief Financial Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0423 | controlling_owner |  | none | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0423 | ownership_type |  | widely_held | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0423 | pay_currency | Chief Executive Officer | USD | Fail | CORE-04: no period_end |
| T0423 | pay_currency | Chief Financial Officer | USD | Fail | CORE-04: no period_end |
| T0423 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0423 | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0423 | pension_contribution | Chief Financial Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0423 | revenue_by_country |  | Colombia: 8683; Argentina: 107 | Fail | CORE-04: no period_end; NUM-08: adds up to 19,456,000 vs 8,683,000 (124.1% apart) |
| T0423 | revenue_by_segment |  | Colombia: 8683; Argentina: 107 | Fail | CORE-04: no period_end; NUM-08: adds up to 19,829,000 vs 8,683,000 (128.4% apart) |
| T0423 | staff_by_country |  | Colombia: 45; Argentina: 75 | Fail | CORE-04: no period_end |
| T0423 | staff_by_segment |  | Colombia: 45; Argentina: 75 | Fail | CORE-04: no period_end |
| T0428 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0428 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0428 | pay_currency | CEO | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | CFO (from 20.01.2025) | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | CFO (until 28.02.2025) | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | COO | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | CSO | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | CBDO | NOK | Fail | CORE-04: no period_end |
| T0428 | pay_currency | Dir. Bus. Dev. Sweden | NOK | Fail | CORE-04: no period_end |
| T0428 | revenue_by_country |  | Norway: 628.6; Sweden: 3.3; US | Fail | CORE-04: no period_end |
| T0428 | revenue_by_segment |  | Operating segment: 721.2 | Fail | CORE-04: no period_end |
| T0428 | shares_outstanding |  | 29147972 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0428 | staff_by_country |  | Norway: 304; Sweden: 6 | Fail | CORE-04: no period_end |
| T0443 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0443 | controlling_owner_name |  | Adrianus Van Herk | Fail | CORE-04: no period_end |
| T0443 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0443 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0443 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0443 | pension_contribution | CEO | 312218 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0443 | staff_by_country |  | Sverige: 6; Nederländerna: 28 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0443 | sti_paid | CEO | 1778650 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0443 | total_remuneration | CEO | 6537506 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0448 | benefits |  | fringe benefits, index increas | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0448 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0448 | controlling_owner_name |  | Metsäliitto Cooperative | Fail | CORE-04: no period_end |
| T0448 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0448 | pension_type |  | defined benefit supplementary  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0448 | staff_by_country |  | Finland: 1007; Sweden: 665; Po | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 1,900 vs 9,581 (80.2% apart) |
| T0469 | base_salary | Other management (including su | 3684000 | Fail (hard) | CORE-02: 3684 not in the quote |
| T0469 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0469 | controlling_owner_name |  | Vidgren Juha Einari | Fail | CORE-04: no period_end |
| T0469 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0469 | pay_currency | President and CEO | EUR | Fail | CORE-04: no period_end |
| T0469 | pay_currency | Other management (including su | EUR | Fail | CORE-04: no period_end |
| T0469 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0469 | pension_contribution | Other management (including su | 326000 | Fail (hard) | CORE-02: 326 not in the quote |
| T0469 | share_price |  | 25.9 | Fail (hard) | CORE-02: 25.9 not in the quote |
| T0469 | staff_by_country |  | Eurooppa: 1404; Etelä-Amerikka | Fail | CORE-04: no period_end |
| T0469 | total_remuneration | Other management (including su | 4010000 | Fail (hard) | CORE-02: 4010 not in the quote |
| T0470 | base_salary | vd | 491000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | base_salary | Other executives | 736000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | benefits_value | vd | 23000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | benefits_value | Other executives | 109000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | controlling_owner |  | corporate | Fail | CORE-04: no period_end |
| T0470 | controlling_owner_name |  | Nemesia S.à r.l. | Fail | CORE-04: no period_end |
| T0470 | ebitda |  | -10300000 | Fail (hard) | CORE-02: -10.3 not in the quote; CORE-04: no period_end |
| T0470 | lti_granted | vd | 1040000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | lti_granted | Other executives | 999000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | ownership_type |  | subsidiary | Fail | CORE-04: no period_end |
| T0470 | pay_currency | vd | EUR | Fail | CORE-04: no period_end |
| T0470 | pay_currency | Other executives | EUR | Fail | CORE-04: no period_end |
| T0470 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0470 | pension_contribution | vd | 71000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | pension_contribution | Other executives | 135000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | revenue |  | 29500000 | Fail (hard) | CORE-02: 29.5 not in the quote |
| T0470 | revenue_by_country |  | Tyskland: 4; Sverige: 25.5 | Fail | CORE-04: no period_end |
| T0470 | revenue_by_segment |  | Produktion: 25.5; Projektutvec | Fail | CORE-04: no period_end |
| T0470 | sti_paid | vd | 276000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | sti_paid | Other executives | 418000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | total_remuneration | vd | 1901000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0470 | total_remuneration | Other executives | 2397000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0477 | base_salary | CEO | 9491000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0477 | benefits_value | CEO | 190000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0477 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0477 | controlling_owner_name |  | Anders Börjesson | Fail | CORE-04: no period_end |
| T0477 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0477 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0477 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0477 | pension_contribution | CEO | 2772000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0477 | sti_paid | CEO | 5099000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-11: paid 54% of base, maximum 40% |
| T0477 | total_remuneration | CEO | 17552000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0477 | website |  | addtech.com | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0488 | base_salary | Verkställande direktör | 6400000 | Fail (hard) | CORE-02: 6.4 not in the quote |
| T0488 | controlling_owner |  | none | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0488 | lti_granted | Verkställande direktör | 1800000 | Fail (hard) | CORE-02: 1.8 not in the quote |
| T0488 | lti_granted | CFO | 500000 | Fail (hard) | CORE-02: 0.5 not in the quote |
| T0488 | ownership_type |  | widely_held | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0488 | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| T0488 | pay_currency | CFO | SEK | Fail | CORE-04: no period_end |
| T0488 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0488 | sti_paid | Verkställande direktör | 10600000 | Fail (hard) | CORE-02: 10.6 not in the quote; NUM-11: paid 166% of base, maximum 100% |
| T0488 | total_remuneration | Verkställande direktör | 16000000 | Fail (hard) | XF-01: parts add up to 19,000,000, more than the stated 16,000,000; XF-02: parts add up to 19,000,000, stated 16,000,000 |
| T0504 | accounting_basis |  | IFRS | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0504 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0504 | lti_granted | Other group management | 700000 | Fail (hard) | CORE-02: 700000 not in the quote |
| T0504 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0504 | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| T0504 | pay_currency | Other group management | EUR | Fail | CORE-04: no period_end |
| T0504 | pay_currency | Konsernin johtoryhmä | EUR | Fail | CORE-04: no period_end |
| T0504 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0504 | pension_contribution | Konsernin johtoryhmä | 137000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0504 | revenue_by_country |  | Suomi: 32311; Ulkomaat: 5489 | Fail | CORE-04: no period_end |
| T0504 | revenue_by_segment |  | Teknologiapalvelut, jatkuvalas | Fail | CORE-04: no period_end |
| T0504 | role_disclosure | Konsernin johtoryhmä | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0504 | share_price |  | 4.0318 | Fail (hard) | CORE-02: 4.0318 not in the quote |
| T0504 | staff_by_segment |  | Konsernin tukipalvelut: 20; Ma | Fail | CORE-04: no period_end |
| T0504 | total_remuneration | Konsernin johtoryhmä | 794590 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0531 | base_salary | Other members of group managem | 2325000 | Fail (hard) | CORE-02: 2325000 not in the quote |
| T0531 | benefits |  | Fringe benefits for CEO; trave | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0531 | controlling_owner |  | corporate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0531 | controlling_owner_name |  | AS Pontos Baltic | Fail (hard) | CORE-02: not in the quote: baltic; CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0531 | lti_granted | Other members of group managem | 152000 | Fail (hard) | CORE-02: 152000 not in the quote |
| T0531 | ownership_type |  | subsidiary | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| T0531 | pay_currency | President and CEO | EUR | Fail | CORE-04: no period_end |
| T0531 | pay_currency | Other members of group managem | EUR | Fail | CORE-04: no period_end |
| T0531 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0531 | role_disclosure | Other members of group managem | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0531 | staff_by_country |  | Finland: 721; Estonia: 2 | Fail | CORE-04: no period_end |
| T0531 | sti_max | President and CEO | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote |
| T0531 | total_remuneration | Other members of group managem | 3266000 | Fail (hard) | CORE-02: 3266000 not in the quote |
| T0533 | benefits_value | VD | 12000 | Fail (hard) | CORE-02: 12 not in the quote |
| T0533 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0533 | controlling_owner_name |  | Petter Stillström | Fail | CORE-04: no period_end |
| T0533 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0533 | pay_currency | VD | SEK | Fail | CORE-04: no period_end |
| T0533 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0533 | sti_paid | VD | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| T0568 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0568 | fte |  | 5.9 | Fail (hard) | CORE-02: 5.9 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| T0568 | headcount |  | 6 | Fail (hard) | CORE-02: 6 not in the quote |
| T0568 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0568 | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| T0568 | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| T0568 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0568 | staff_by_country |  | Sverige: 5.9 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0604 | aggregate_headcount | Other members of group managem | 7 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0604 | benefits |  | benefits in kind | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0604 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0604 | ebitda |  | 26200000 | Fail (hard) | CORE-02: 26.2 not in the quote; CORE-04: no period_end |
| T0604 | headcount |  | 4608 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0604 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0604 | pay_currency | Toimitusjohtaja | EUR | Fail | CORE-04: no period_end |
| T0604 | pay_currency | Other members of group managem | EUR | Fail | CORE-04: no period_end |
| T0604 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0604 | revenue_by_segment |  | Kustannustoiminta: 161.3; Tuot | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 269,100,000 vs 212,768,000 (26.5% apart) |
| T0604 | role_disclosure | Other members of group managem | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0604 | share_price |  | 8.596 | Fail (hard) | CORE-02: 8.596 not in the quote |
| T0604 | website |  | keskisuomalainen.com | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0609 | base_salary | Other members of the Managemen | 800 | Fail (hard) | CORE-02: 800 not in the quote |
| T0609 | controlling_owner |  | none | Fail | CORE-04: no period_end |
| T0609 | ownership_type |  | widely_held | Fail | CORE-04: no period_end |
| T0609 | pay_currency | Interim CEO (until 31 May 2025 | EUR | Fail | CORE-04: no period_end |
| T0609 | pay_currency | Deputy CEO (from 1 June 2025) | EUR | Fail | CORE-04: no period_end |
| T0609 | pay_currency | CEO (from 1 June 2025) | EUR | Fail | CORE-04: no period_end |
| T0609 | pay_currency | Other members of the Managemen | EUR | Fail | CORE-04: no period_end |
| T0609 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0609 | staff_by_segment |  | Housing: 58.2; Investing: 9; O | Fail | CORE-04: no period_end; NUM-08: adds up to 100 vs 256 (60.9% apart) |
| T0609 | sub_sector |  | Kojamo offers rental apartment | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0609 | total_remuneration | Deputy CEO (from 1 June 2025) | 146865.6 | Fail (hard) | XF-01: parts add up to 171,342, more than the stated 146,866; XF-02: parts add up to 171,342, stated 146,866 |
| T0609 | total_remuneration | CEO (from 1 June 2025) | 315211.61 | Fail (hard) | XF-01: parts add up to 367,712, more than the stated 315,212; XF-02: parts add up to 367,712, stated 315,212 |
| T0668 | base_salary | CEO | 6558000 | Fail (hard) | CORE-02: 6558 not in the quote |
| T0668 | base_salary | Deputy CEO (Krister Karlsson) | 2810000 | Fail (hard) | CORE-02: 2810 not in the quote |
| T0668 | base_salary | Deputy CEO (Annika Ekström) | 2821000 | Fail (hard) | CORE-02: 2821 not in the quote |
| T0668 | base_salary | Other senior executives | 6118000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0668 | benefits_value | CEO | 87000 | Fail (hard) | CORE-02: 87 not in the quote |
| T0668 | benefits_value | Deputy CEO (Krister Karlsson) | 113000 | Fail (hard) | CORE-02: 113 not in the quote |
| T0668 | benefits_value | Deputy CEO (Annika Ekström) | 74000 | Fail (hard) | CORE-02: 74 not in the quote |
| T0668 | benefits_value | Other senior executives | 411000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0668 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0668 | controlling_owner_name |  | Ilija Batljan | Fail | CORE-04: no period_end |
| T0668 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0668 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0668 | pay_currency | Deputy CEO (Krister Karlsson) | SEK | Fail | CORE-04: no period_end |
| T0668 | pay_currency | Deputy CEO (Annika Ekström) | SEK | Fail | CORE-04: no period_end |
| T0668 | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| T0668 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0668 | pension_contribution | CEO | 2816000 | Fail (hard) | CORE-02: 2816 not in the quote |
| T0668 | pension_contribution | Deputy CEO (Krister Karlsson) | 1193000 | Fail (hard) | CORE-02: 1193 not in the quote |
| T0668 | pension_contribution | Deputy CEO (Annika Ekström) | 928000 | Fail (hard) | CORE-02: 928 not in the quote |
| T0668 | pension_contribution | Other senior executives | 1669000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0668 | revenue_by_country |  | Sweden: 2817.08; Finland: 667. | Fail | CORE-04: no period_end |
| T0668 | revenue_by_segment |  | Community: 2184; Residentials: | Fail | CORE-04: no period_end |
| T0668 | role_disclosure | Other senior executives | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0668 | shares_outstanding |  | 1603823774 | Fail (hard) | CORE-02: 1603823774 not in the quote |
| T0668 | staff_by_country |  | Sweden: 308; Norway: 0; Finlan | Fail | CORE-04: no period_end |
| T0668 | sti_paid | Other senior executives | 3852000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-11: paid 63% of base, maximum 50% |
| T0668 | total_remuneration | Other senior executives | 12050000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0669 | controlling_owner |  | other | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0669 | controlling_owner_name |  | The primary fund | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0669 | exchange |  | Oslo Børs | Fail (hard) | CORE-02: not in the quote: oslo |
| T0669 | ownership_type |  | other | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0669 | pay_currency | Administrerende direktør | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder divisjon Næringslivsmark | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder divisjon Personmarked | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder seksjon Økonomi og Finan | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder seksjon Risikostyring og | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder seksjon Organisasjonsutv | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder seksjon Forretningsstøtt | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Tidligere medlem av konsernled | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Daglig leder Møre Boligkreditt | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder avdeling Treasury | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder avdeling Kreditt | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder avdeling Compliance | NOK | Fail | CORE-04: no period_end |
| T0669 | pay_currency | Leder avdeling Risikostyring | NOK | Fail | CORE-04: no period_end |
| T0669 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0669 | revenue_by_segment |  | Næringsliv: 515; Personmarked: | Fail | CORE-04: no period_end |
| T0669 | staff_by_segment |  | Næringsliv: 152; Personmarked: | Fail | CORE-04: no period_end; NUM-08: adds up to 393 vs 468 (16.0% apart) |
| T0670 | base_salary | Other senior executives | 8317000 | Fail (hard) | CORE-02: 8317 not in the quote |
| T0670 | controlling_owner |  | family | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | controlling_owner_name |  | Rutger Arnhult privately and v | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | largest_holders |  | Rutger Arnhult privately and v | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0670 | pay_currency | Deputy CEO | SEK | Fail | CORE-04: no period_end |
| T0670 | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| T0670 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | revenue_by_country |  | Denmark: 59; USA: 162 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 221,000,000 vs 3,465,000,000 (93.6% apart) |
| T0670 | revenue_by_segment |  | Stockholm North: 1014; Stockho | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | shares_outstanding |  | 1396281000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| T0670 | staff_by_country |  | Sweden: 277; Denmark: 3 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| T0670 | sti_paid | Other senior executives | 900 | Fail (hard) | CORE-02: 900 not in the quote |
| T0671 | base_salary | CEO | 6558000 | Fail (hard) | CORE-02: 6558 not in the quote |
| T0671 | base_salary | Deputy CEO (Krister Karlsson) | 2810000 | Fail (hard) | CORE-02: 2810 not in the quote |
| T0671 | base_salary | Deputy CEO (Annika Ekström) | 2821000 | Fail (hard) | CORE-02: 2821 not in the quote |
| T0671 | base_salary | Other senior executives | 6118000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0671 | benefits_value | CEO | 87000 | Fail (hard) | CORE-02: 87 not in the quote |
| T0671 | benefits_value | Deputy CEO (Krister Karlsson) | 113000 | Fail (hard) | CORE-02: 113 not in the quote |
| T0671 | benefits_value | Deputy CEO (Annika Ekström) | 74000 | Fail (hard) | CORE-02: 74 not in the quote |
| T0671 | benefits_value | Other senior executives | 411000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0671 | controlling_owner |  | family | Fail | CORE-04: no period_end |
| T0671 | controlling_owner_name |  | Ilija Batljan | Fail | CORE-04: no period_end |
| T0671 | ownership_type |  | family_owned | Fail | CORE-04: no period_end |
| T0671 | pay_currency | CEO | SEK | Fail | CORE-04: no period_end |
| T0671 | pay_currency | Deputy CEO (Krister Karlsson) | SEK | Fail | CORE-04: no period_end |
| T0671 | pay_currency | Deputy CEO (Annika Ekström) | SEK | Fail | CORE-04: no period_end |
| T0671 | pay_currency | Other senior executives | SEK | Fail | CORE-04: no period_end |
| T0671 | pe_stake_5pct |  | no | Fail | CORE-04: no period_end |
| T0671 | pension_contribution | CEO | 2816000 | Fail (hard) | CORE-02: 2816 not in the quote |
| T0671 | pension_contribution | Deputy CEO (Krister Karlsson) | 1193000 | Fail (hard) | CORE-02: 1193 not in the quote |
| T0671 | pension_contribution | Deputy CEO (Annika Ekström) | 928000 | Fail (hard) | CORE-02: 928 not in the quote |
| T0671 | pension_contribution | Other senior executives | 1669000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0671 | revenue_by_country |  | Sweden: 2817.08; Finland: 667. | Fail | CORE-04: no period_end |
| T0671 | revenue_by_segment |  | Community: 2184; Residentials: | Fail | CORE-04: no period_end |
| T0671 | role_disclosure | Other senior executives | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| T0671 | shares_outstanding |  | 1603823774 | Fail (hard) | CORE-02: 1603823774 not in the quote |
| T0671 | staff_by_country |  | Sweden: 308; Norway: 0; Finlan | Fail | CORE-04: no period_end |
| T0671 | sti_paid | Other senior executives | 3852000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-11: paid 63% of base, maximum 50% |
| T0671 | total_remuneration | Other senior executives | 12050000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| abb-ltd | listing_status |  | listed | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | revenue_by_country |  | Europe: 11.4; The Americas: 9. | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| abb-ltd | staff_by_country |  | Europe: 53407; The Americas: 2 | Fail | CORE-04: no period_end; NUM-08: adds up to 114,292 vs 105,000 (8.8% apart) |
| abb-ltd | sti_paid | Other EC members | 1500000 | Fail (hard) | CORE-03: quote not in the source text |
| abb-ltd | sti_target | Other EC members | 1190000 | Fail (hard) | CORE-03: quote not in the source text |
| aberdeen-group-plc | lti_vested | CEO | 497000 | Fail (hard) | CORE-02: 497 not in the quote |
| aberdeen-group-plc | share_price |  | 230 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBp' is not ISO 4217 |
| aberdeen-group-plc | sti_paid | CEO | 1550000 | Fail (hard) | CORE-02: 1550 not in the quote |
| aberdeen-group-plc | sti_paid | Chief Financial Officer | 258000 | Fail (hard) | CORE-02: 258 not in the quote |
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
| addex-therapeutics-ltd | lti_granted | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | lti_granted | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | sti_paid | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| adecco-group-ag | revenue_by_country |  | France: 4558; Northern Europe: | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end; NUM-08: adds up to 17,911,000,000 vs 23,138,000,000 (22.6% apart) |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Human Resources, People | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vertriebsvorstand | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Sales (bis 31. Oktober  | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Global Operations (bis 10. Aug | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Vorstandsvorsitzender (bis 30. | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pay_currency | Finanzvorstand (bis 11. Mai 20 | EUR | Fail | CORE-04: no period_end |
| adidas-ag-na-o-n | pension_type |  | For board members appointed be | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| adidas-ag-na-o-n | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| adidas-ag-na-o-n | total_remuneration | Finanzvorstand | 2866084 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 3,344,070, more than the stated 2,866,084; XF-02: parts add up to 3,344,070, stated 2,866,084 |
| admiral-group-plc | listing_date |  | 2004-09 | Fail (hard) | CORE-02: not in the quote: 2004; CORE-03: the run did not find the full quote (the note keeps only its start) |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| adval-tech-holding-ag | staff_by_country |  | Europa: 707; Nordamerika (Mexi | Fail | CORE-04: no period_end |
| aep-plantations-plc | pension_contribution | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aep-plantations-plc | sti_paid | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aevis-victoria-sa | aggregate_headcount | Other Members of Senior Manage | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aevis-victoria-sa | base_salary | Other Members of Senior Manage | 1202900 | Fail (hard) | CORE-02: 1202.9 not in the quote |
| aevis-victoria-sa | ebitda |  | 72446000 | Fail (hard) | CORE-02: 72446 not in the quote |
| aevis-victoria-sa | fte |  | 4870 | Fail (hard) | CORE-02: 4870 not in the quote |
| aevis-victoria-sa | revenue |  | 1208366000 | Fail (hard) | CORE-02: 1208366 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | revenue_by_segment |  | HEALTHCARE: 832583; HOSPITALIT | Fail | NUM-08: adds up to 1,055,058,000 vs 1,208,366,000 (12.7% apart) |
| aevis-victoria-sa | total_assets |  | 1905326000 | Fail (hard) | CORE-02: 1905326 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | total_remuneration | Executive Chairman (as of 21.0 | 1250600 | Fail (hard) | CORE-02: 1250.6 not in the quote |
| aevis-victoria-sa | total_remuneration | Other Members of Senior Manage | 2098600 | Fail (hard) | CORE-02: 2098.6 not in the quote |
| african-pioneer-plc | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| agilyx | exchange |  | OSE | Fail (hard) | COD-01: 'OSE' matches no ISO 10383 exchange |
| agilyx | revenue_by_country |  | Europe: 544402; USA: 255044; A | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| agilyx | revenue_by_segment |  | Cyclyx: 16574621; Agilyx: 1214 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 17,789,146 vs 1,214,525 (1364.7% apart) |
| aiq-limited | base_salary | Executive Director (Li Chun Ch | 19320 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| aiq-limited | base_salary | Executive Director (Charles Yo | 14400 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| aiq-limited | pay_currency | Executive Director (Li Chun Ch | £ | Fail (hard) | COD-01: £ is not ISO 4217 |
| aiq-limited | pay_currency | Executive Director (Charles Yo | £ | Fail (hard) | COD-01: £ is not ISO 4217 |
| aiq-limited | total_remuneration | Executive Director (Li Chun Ch | 19320 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| aiq-limited | total_remuneration | Executive Director (Charles Yo | 14400 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| airtel-africa-plc | benefits_value | Former CFO (until 9 July 2025) | 55000 | Fail (hard) | CORE-02: 55 not in the quote |
| airtel-africa-plc | staff_by_segment |  | Executive management: 174; Man | Fail | CORE-04: no period_end; NUM-08: adds up to 4,132 vs 11,520 (64.1% apart) |
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
| alfa-financial-software-holdings-plc | revenue_by_segment |  | Subscription: 43.6; Software E | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| alfa-financial-software-holdings-plc | sti_paid | CFO | 288000 | Fail (hard) | CORE-02: 288000 not in the quote |
| alfa-financial-software-holdings-plc | sti_paid | COO | 228000 | Fail (hard) | CORE-02: 228000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | Executive Chairman | 30000 | Fail (hard) | CORE-02: 30000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | CEO | 32000 | Fail (hard) | CORE-02: 32000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | CFO | 1147000 | Fail (hard) | CORE-02: 1147000 not in the quote |
| alfa-financial-software-holdings-plc | total_remuneration | COO | 777000 | Fail (hard) | CORE-02: 777000 not in the quote |
| alina-holdings-plc | largest_holders |  | Vidacos Nominees Limited 44.22 | Fail (hard) | NUM-07: holdings add up to 107.27% |
| alkemy-capital-investments-plc | fte |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| alkemy-capital-investments-plc | lti_granted | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | pension_contribution | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| alkemy-capital-investments-plc | sti_paid | Director | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| allreal-holding-ag | ebitda |  | 310500000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| allreal-holding-ag | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | lti_target | Other members of Group Managem | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | staff_by_segment |  | Real Estate: 50 | Fail | CORE-04: no period_end; NUM-08: adds up to 50 vs 224 (77.7% apart) |
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
| altyngold-plc | base_salary | Executive Director (Kanat Assa | 39300 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | base_salary | Chief Executive Officer | 98250 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | base_salary | Executive Director (Sanzhar As | 39300 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | base_salary | Chief Financial Officer | 50108 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | benefits |  | Health insurance for the Execu | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| altyngold-plc | pay_currency | Executive Director (Kanat Assa | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| altyngold-plc | pay_currency | Chief Executive Officer | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| altyngold-plc | pay_currency | Executive Director (Sanzhar As | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| altyngold-plc | pay_currency | Chief Financial Officer | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| altyngold-plc | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| altyngold-plc | role_disclosure | Executive Director (Sanzhar As | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| altyngold-plc | role_disclosure | Chief Financial Officer | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| altyngold-plc | total_remuneration | Executive Director (Kanat Assa | 39300 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | total_remuneration | Chief Executive Officer | 98250 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | total_remuneration | Executive Director (Sanzhar As | 39300 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| altyngold-plc | total_remuneration | Chief Financial Officer | 50108 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
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
| amigo-resources-plc | total_assets |  | 4000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aminex-plc | ebitda |  | -2885000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aminex-plc | share_price |  | 2.08 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-01: unit 'GBX' is not ISO 4217 |
| amrize-ltd | benefits |  | deferred compensation plan, 40 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | lti_granted | Chief Executive Officer (23 Ju | 9942122 | Fail (hard) | CORE-02: 9942122 not in the quote |
| amrize-ltd | lti_granted | Other Members of Executive Man | 12411396 | Fail (hard) | CORE-02: 12411396 not in the quote |
| amrize-ltd | pension_type |  | defined benefit (cash balance  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | revenue_by_segment |  | Building Materials: 8514; Buil | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| amrize-ltd | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| amrize-ltd | sub_sector |  | The Company is organized into  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| antofagasta-plc | ebitda |  | 5201900000 | Fail (hard) | NUM-01: unit '$' is not ISO 4217 |
| antofagasta-plc | headcount |  | 8457 | Fail (hard) | CORE-02: 8457 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| antofagasta-plc | listing_date |  | 1888 | Fail (hard) | CORE-02: not in the quote: 1888; COD-06: not a year or a date |
| antofagasta-plc | share_price |  | 3125 | Fail (hard) | NUM-01: unit 'GBX' is not ISO 4217 |
| antofagasta-plc | staff_by_country |  | Chile: 6053; United Kingdom: 5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 6,062 vs 8,457 (28.3% apart) |
| antofagasta-plc | staff_by_segment |  | Mining and Corporate: 6053; Tr | Fail | NUM-08: adds up to 7,213 vs 8,457 (14.7% apart) |
| ao-world-plc | fte |  | 2892 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aptitude-software-group-plc | fte |  | 359 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-13: FTE 359 above headcount 317 |
| aptitude-software-group-plc | lti_vested | Executive Director | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| aptitude-software-group-plc | revenue_by_country |  | United Kingdom: 10586; Rest of | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aptitude-software-group-plc | staff_by_country |  | United Kingdom: 102; Rest of W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 359 vs 317 (13.2% apart) |
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
| ascom-holding-ag | revenue_by_country |  | DACH: 53.2; France & Spain: 18 | Fail | NUM-08: adds up to 272,100,000 vs 286,700,000 (5.1% apart) |
| ascom-holding-ag | revenue_by_segment |  | OEM: 14.6 | Fail | NUM-08: adds up to 14,600,000 vs 286,700,000 (94.9% apart) |
| aseana-properties-limited | base_salary | Executive Director and Chief E | 175138 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | ebitda |  | 15118000 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | pay_currency | Executive Director and Chief E | US$ | Fail (hard) | COD-01: US$ is not ISO 4217 |
| aseana-properties-limited | revenue_by_country |  | Malaysia: 14415 | Fail (hard) | CORE-03: quote not in the source text |
| aseana-properties-limited | share_price |  | 0.075 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| aseana-properties-limited | total_remuneration | Executive Director and Chief E | 175138 | Fail (hard) | NUM-01: unit 'US$' is not ISO 4217 |
| ashmore-group-plc | listing_date |  | 2006 | Fail (hard) | CORE-02: not in the quote: 2006 |
| ashmore-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| ashtead-technology-holdings-plc | fte |  | 649 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 649 above headcount 396 |
| asia-strategic-holdings-limited | ebitda |  | -250237 | Fail (hard) | NUM-01: unit '$' is not ISO 4217 |
| asos-plc | benefits |  | flexible benefits allowance of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| asos-plc | lti_granted | CFO (appointed 1 July 2025) | 5 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| asos-plc | pension_type |  | defined contribution, 5% of ba | Fail (hard) | CORE-03: quote not in the source text |
| associated-british-foods-plc | largest_holders |  | Wittington Investments Limited | Fail (hard) | NUM-07: holdings add up to 121.6% |
| associated-british-foods-plc | lti_granted | Chief Executive | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| associated-british-foods-plc | lti_granted | Finance Director (interim CEO  | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| aston-martin-lagonda-global-holdings-plc | base_salary | Executive Director | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aston-martin-lagonda-global-holdings-plc | benefits_value | Executive Director | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aston-martin-lagonda-global-holdings-plc | pension_contribution | Executive Director | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aston-martin-lagonda-global-holdings-plc | role_disclosure | CEO | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| aston-martin-lagonda-global-holdings-plc | total_remuneration | Executive Director | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 3,000, more than the stated 1,000; XF-02: parts add up to 3,000, stated 1,000 |
| astrazeneca-plc | revenue_by_country |  | US: 25450; Emerging Markets: 1 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-08: adds up to 65,393,000,000 vs 58,739,000,000 (11.3% apart) |
| atalaya-mining-copper-s-a | fte |  | 509 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atalaya-mining-copper-s-a | headcount |  | 518 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atalaya-mining-copper-s-a | role_disclosure | Chief Financial Officer (PDMR) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| atlantic-petroleum | benefits_value | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlantic-petroleum | pay_currency | Managing Director – CEO | DKK | Fail | CORE-04: no period_end |
| atlantic-petroleum | sti_paid | Managing Director – CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-04: no period_end; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts DKK |
| atlas-metals-group-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| atlas-metals-group-plc | website |  | atlasmetalsgroup.com | Fail (hard) | CORE-02: not in the quote: atlasmetalsgroup com |
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
| austriacard-holdings-ag | ebitda |  | 51773000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| austriacard-holdings-ag | revenue_by_country |  | Austria: 24414; Romania: 83072 | Fail | NUM-08: adds up to 242,237,000 vs 360,171,000 (32.7% apart) |
| austriacard-holdings-ag | revenue_by_segment |  | CEE: 203017; WEST: 122776; MEA | Fail | NUM-08: adds up to 390,401,000 vs 360,171,000 (8.4% apart) |
| austriacard-holdings-ag | staff_by_country |  | Romania: 1346 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,346 vs 2,360 (43.0% apart) |
| austriacard-holdings-ag | total_remuneration | Stellvertretender Vorsitzender | 130691 | Fail (hard) | XF-01: parts add up to 135,116, more than the stated 130,691; XF-02: parts add up to 135,116, stated 130,691 |
| austriacard-holdings-ag | total_remuneration | Executive Vice President Türki | 278255 | Fail (hard) | XF-01: parts add up to 289,459, more than the stated 278,255; XF-02: parts add up to 289,459, stated 278,255 |
| autoneum-holding-ag | base_salary | Group Executive Board | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| autotrader-group-plc | shareholding_requirement |  | 200% of salary in-post; 200% o | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
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
| avolta-ag | base_salary | Other members of Global Execut | 6297100 | Fail (hard) | CORE-02: 6297.1 not in the quote |
| avolta-ag | benefits_value | Other members of Global Execut | 491000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | ebitda |  | 1324000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | lti_granted | Other members of Global Execut | 5772800 | Fail (hard) | CORE-02: 5772.8 not in the quote |
| avolta-ag | pension_contribution | Other members of Global Execut | 1310800 | Fail (hard) | CORE-02: 1310.8 not in the quote |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avolta-ag | staff_by_segment |  | Europe,Middle East and Africa  | Fail | NUM-08: adds up to 68,836 vs 78,116 (11.9% apart) |
| avolta-ag | sti_paid | Other members of Global Execut | 7231600 | Fail (hard) | CORE-02: 7231.6 not in the quote |
| avolta-ag | total_remuneration | Other members of Global Execut | 21103400 | Fail (hard) | CORE-02: 21103.4 not in the quote |
| avon-technologies-plc | ebitda |  | 51500000 | Fail (hard) | NUM-01: unit '$' is not ISO 4217 |
| avon-technologies-plc | fte |  | 911 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| avon-technologies-plc | lti_granted | CEO | 175 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| avon-technologies-plc | revenue_by_segment |  | Avon Protection: 168.8; Team W | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| avon-technologies-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| avon-technologies-plc | total_assets |  | 314800000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| b-m-european-value-retail-plc | ebitda |  | 672000000 | Fail (hard) | CORE-02: 672 not in the quote |
| b-m-european-value-retail-plc | lti_vested | CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CEO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | interim CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| b-m-european-value-retail-plc | lti_vested | former CFO | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| babcock-international-group-plc | base_salary | Deputy Chief Executive | 108000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| babcock-international-group-plc | benefits_value | Deputy Chief Executive | 21000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| babcock-international-group-plc | pension_contribution | Deputy Chief Executive | 11000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| babcock-international-group-plc | sti_paid | Deputy Chief Executive | 56000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bachem-holding-ag | lti_granted | Rest of the Corporate Executiv | 261000 | Fail (hard) | CORE-02: 261 not in the quote |
| bachem-holding-ag | pension_contribution | Rest of the Corporate Executiv | 274000 | Fail (hard) | CORE-02: 274 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | sti_paid | CEO | 247000 | Fail (hard) | CORE-02: 247 not in the quote |
| bachem-holding-ag | sti_paid | Corporate Executive Committee | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bae-systems-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| bae-systems-plc | share_price |  | 1880.5 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBX' is not ISO 4217 |
| bakkafrost | ebitda |  | 1672664000 | Fail (hard) | CORE-03: quote not in the source text |
| balfour-beatty-plc | pension_contribution | Former Group Chief Executive ( | 43183 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| balfour-beatty-plc | revenue_by_country |  | United Kingdom: 4778; United S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | revenue_by_segment |  | Construction Services: 8711; S | Fail | CORE-04: no period_end; NUM-08: adds up to 10,767,000,000 vs 9,489,000,000 (13.5% apart) |
| balfour-beatty-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| balfour-beatty-plc | sti_target | Group Chief Executive (appoint | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Executive Director | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| balfour-beatty-plc | sti_target | Former Group Chief Executive ( | 75 | Fail (hard) | CORE-02: 75 not in the quote |
| baltic-classifieds-group-plc | ebitda |  | 68626000 | Fail (hard) | CORE-02: 68626 not in the quote |
| baltic-classifieds-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| banque-cantonale-du-jura-sa | benefits |  | Frais de représentation; taux  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| banque-cantonale-du-jura-sa | pay_currency | Directeur général | CHF | Fail | CORE-04: no period_end |
| banque-cantonale-du-jura-sa | pay_currency | Direction | CHF | Fail | CORE-04: no period_end |
| barclays-plc | pension_contribution | Group Chief Executive | 155000 | Fail (hard) | CORE-02: 155 not in the quote |
| barclays-plc | pension_contribution | Group Finance Director | 94000 | Fail (hard) | CORE-02: 94 not in the quote |
| barclays-plc | total_remuneration | Group Chief Executive | 15045000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 4,588,000, stated 15,045,000 |
| barclays-plc | total_remuneration | Group Finance Director | 8970000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,770,000, stated 8,970,000 |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| basellandschaftliche-kantonalbank | headcount |  | 1054 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Managemen | 605000 | Fail (hard) | CORE-02: 605000 not in the quote |
| basellandschaftliche-kantonalbank | pension_type |  | defined contribution, BLKB cov | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must acquire 2 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | staff_by_country |  | Canton of Basel-Landschaft: 92 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Managemen | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Chief Executive Officer | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pay_currency | Other members of the managemen | CHF | Fail | CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | pension_type |  | defined benefit plan, collecti | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote; CORE-04: no period_end |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | CORE-04: no period_end; XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; CORE-04: no period_end; XF-02: parts add up to 2,855,610, stated 3,028,977 |
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
| baywa-ag-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote |
| baywa-ag-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 25,605 (29.0% apart) |
| baywa-ag-vink-na-o-n | controlling_owner_name |  | Bayerische Raiffeisen-Beteilig | Fail (hard) | CORE-02: not in the quote: bayerische raiffeisen beteiligungs ag |
| baywa-ag-vink-na-o-n | share_price |  | 2.24 | Fail (hard) | CORE-02: 2.24 not in the quote |
| baywa-ag-vink-na-o-n | staff_by_country |  | Germany: 14595; Austria: 3593 | Fail | CORE-04: no period_end; NUM-08: adds up to 18,188 vs 22,111 (17.7% apart) |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (Grita  | 1705000 | Fail (hard) | CORE-02: 1705 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | benefits_value | Mitglied des Vorstands (bis 30 | 393000 | Fail (hard) | CORE-02: 393 not in the quote |
| beiersdorf-ag-o-n | sti_paid | Vorstandsvorsitzender | 407000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands (Oswald | 142000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands/CFO | 153000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands/CHRO | 166000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands (Grita  | 138000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands (Ramon  | 144000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_paid | Mitglied des Vorstands (bis 30 | 56000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| beiersdorf-ag-o-n | sti_target | Mitglied des Vorstands (bis 30 | 100000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| belimo-holding-ag | base_salary | CEO | 570000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | base_salary | Other members, Executive Commi | 2108000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_country |  | EMEA: 240.3; Americas: 341.3;  | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | revenue_by_segment |  | Damper Actuators: 253.8; Contr | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | role_disclosure | Other members, Executive Commi | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | CEO | 817000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | Other members, Executive Commi | 2449000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | total_remuneration | CEO | 1749000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,539,000, stated 1,749,000 |
| belimo-holding-ag | total_remuneration | Other members, Executive Commi | 5573000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 5,108,000, stated 5,573,000 |
| bell-food-group-ag | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| bell-food-group-ag | pay_currency | Übrige Mitglieder der Gruppenl | CHF | Fail | CORE-04: no period_end |
| bellevue-group-ag | headcount |  | 72.8 | Fail (hard) | NUM-05: not a whole number |
| bellevue-group-ag | revenue_by_country |  | Switzerland: 47705; United Kin | Fail (hard) | CORE-03: quote not in the source text |
| bellevue-group-ag | total_assets |  | 155563000 | Fail (hard) | CORE-02: 155563 not in the quote; CORE-04: no period_end |
| berkeley-group-holdings-the-plc | lti_granted | Executive Chair | 400 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CEO | 250 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| berkeley-group-holdings-the-plc | lti_granted | CFO (from 29 September 2025) | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
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
| blencowe-resources-plc | aggregate_headcount | Key management personnel (excl | 2 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| blencowe-resources-plc | headcount |  | 2 | Fail (hard) | CORE-02: 2 not in the quote |
| blencowe-resources-plc | revenue |  | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| blencowe-resources-plc | share_price |  | 5.85 | Fail (hard) | NUM-01: unit 'GBp' is not ISO 4217 |
| bodycote-plc | base_salary | CEO | 640000 | Fail (hard) | CORE-02: 640000 not in the quote |
| bodycote-plc | base_salary | CFO | 537000 | Fail (hard) | CORE-02: 537000 not in the quote |
| bodycote-plc | benefits_value | CEO | 19000 | Fail (hard) | CORE-02: 19000 not in the quote |
| bodycote-plc | benefits_value | CFO | 16000 | Fail (hard) | CORE-02: 16000 not in the quote |
| bodycote-plc | lti_granted | CFO | 145195 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bodycote-plc | pension_contribution | CEO | 64000 | Fail (hard) | CORE-02: 64000 not in the quote |
| bodycote-plc | pension_contribution | CFO | 54000 | Fail (hard) | CORE-02: 54000 not in the quote |
| bodycote-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | shareholding_requirement |  | 200% of salary during employme | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bodycote-plc | sti_paid | CEO | 399000000 | Fail (hard) | CORE-02: 399000 not in the quote; NUM-11: paid 62344% of base, maximum 175% |
| bodycote-plc | sti_paid | CFO | 293000000 | Fail (hard) | CORE-02: 293000 not in the quote; NUM-11: paid 54562% of base, maximum 150% |
| bodycote-plc | total_remuneration | CEO | 1122000 | Fail (hard) | CORE-02: 1122000 not in the quote; XF-01: parts add up to 399,723,000, more than the stated 1,122,000; XF-02: parts add up to 399,723,000, stated 1,122,000 |
| bodycote-plc | total_remuneration | CFO | 900000000 | Fail (hard) | CORE-02: 900000 not in the quote; XF-02: parts add up to 293,752,195, stated 900,000,000 |
| boot-henry-plc | role_disclosure | Other key management | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| branicks-group-ag | revenue |  | 100000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| branicks-group-ag | share_price |  | 2.23 | Fail (hard) | CORE-02: 2.23 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| breedon-group-plc | fte |  | 4780 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| breedon-group-plc | share_price |  | 345.4 | Fail (hard) | CORE-04: no period_end; NUM-01: unit 'GBX' is not ISO 4217 |
| bridgepoint-group-plc | revenue_by_country |  | UK: 343.2; USA: 178; EU countr | Fail | NUM-08: adds up to 629,900,000 vs 416,000,000 (51.4% apart) |
| bridgepoint-group-plc | revenue_by_segment |  | Private Equity: 311.8; Credit: | Fail | NUM-08: adds up to 592,800,000 vs 416,000,000 (42.5% apart) |
| bridgepoint-group-plc | share_price |  | 2.838 | Fail (hard) | CORE-02: 2.838 not in the quote |
| british-american-tobacco-plc | other_names |  | British American Tobacco Compa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| british-american-tobacco-plc | revenue_by_segment |  | NGP: 397; Strategic Portfolio: | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 17,108,000,000 vs 25,610,000,000 (33.2% apart) |
| brondbyernes-if | pay_currency | Adm. Direktør (until 28. febru | DKK | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | CFO (from 1. juli 2025) | DKK | Fail | CORE-04: no period_end |
| brondbyernes-if | pay_currency | Direktionen (Total) | DKK | Fail | CORE-04: no period_end |
| brooks-macdonald-group-plc | lti_granted | CEO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| brooks-macdonald-group-plc | lti_granted | CFO | 200 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bsf-enterprise-plc | lti_granted | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| bsf-enterprise-plc | pension_contribution | Chairman | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| bsf-enterprise-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| bt-group-plc | fte |  | 81600 | Fail (hard) | CORE-02: 81.6 not in the quote |
| bt-group-plc | headcount |  | 77200 | Fail (hard) | CORE-02: 77.2 not in the quote |
| bt-group-plc | lti_granted | Executive Director (Allison Ki | 2803899 | Fail (hard) | CORE-02: 2803899 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| bt-group-plc | lti_granted | Executive Director (Simon Lowt | 2057634 | Fail (hard) | CORE-02: 2057634 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| bt-group-plc | sti_paid | Executive Director (Allison Ki | 1081000 | Fail (hard) | CORE-02: 1081 not in the quote |
| bt-group-plc | sti_paid | Executive Director (Simon Lowt | 793000 | Fail (hard) | CORE-02: 793 not in the quote |
| bunzl-plc | revenue_by_segment |  | North America: 6276.7; Contine | Fail (hard) | CORE-03: quote not in the source text |
| bunzl-plc | share_price |  | 2923.67 | Fail (hard) | NUM-01: unit 'GBp' is not ISO 4217 |
| burberry-group-plc | lti_max | CFO | 175 | Fail (hard) | CORE-03: quote not in the source text |
| burckhardt-compression-holding-ag | revenue_by_country |  | Europe: 194414; Africa: 10564; | Fail (hard) | CORE-03: quote not in the source text |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | CORE-02: not a year or a date (see COD-06); COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| bvz-holding-ag | revenue_by_segment |  | Gornergrat: 47.1; Immobilien:  | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 181,900,000 vs 216,170,312 (15.9% apart) |
| bw-offshore-limited | role_disclosure | Senior Management Team | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bw-offshore-limited | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| bw-offshore-limited | staff_by_country |  | Singapore: 238; UK: 195; Austr | Fail | CORE-04: no period_end |
| bytes-technology-group-plc | ebitda |  | 62732000 | Fail (hard) | CORE-02: 62732 not in the quote |
| bytes-technology-group-plc | lti_granted | CEO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| bytes-technology-group-plc | lti_granted | CFO | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| c-c-group-plc | lti_granted | Chief Financial and Transforma | 404411 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| c-c-group-plc | revenue_by_segment |  | Branded: 453.6; Distribution:  | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,861,600,000 vs 1,569,800,000 (18.6% apart) |
| cab-payments-holdings-plc | revenue |  | 109400000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cab-payments-holdings-plc | total_assets |  | 188000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cadogan-energy-solutions-plc | ebitda |  | 1258000 | Fail (hard) | CORE-02: 1.258 not in the quote; CORE-04: no period_end |
| cadogan-energy-solutions-plc | lti_max | Chief Executive Officer | 200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cadogan-energy-solutions-plc | revenue_by_country |  | Ukraine: 7.55 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| cadogan-energy-solutions-plc | revenue_by_segment |  | Exploration and Production: 71 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; NUM-08: adds up to 7,550,000 vs 5,792,000 (30.4% apart) |
| cadogan-energy-solutions-plc | staff_by_country |  | Ukraine: 74 | Fail | CORE-04: no period_end |
| caffyns-plc | headcount |  | 485 | Fail (hard) | CORE-02: 485 not in the quote |
| caledonia-investments-plc | benefits_value | Executive Director (J M B Cayz | 31000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| caledonia-investments-plc | headcount |  | 82 | Fail (hard) | CORE-02: 82 not in the quote |
| caledonia-investments-plc | lti_vested | Executive Director (J M B Cayz | 409000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| caledonia-investments-plc | revenue_by_segment |  | Public Companies: 21.8; Privat | Fail | CORE-04: no period_end; NUM-08: adds up to 43,700,000 vs 166,000,000 (73.7% apart) |
| caledonia-investments-plc | share_price |  | 382.5 | Fail (hard) | NUM-01: unit 'GBX' is not ISO 4217 |
| caledonia-investments-plc | sti_paid | Executive Director (J M B Cayz | 259000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| canal-s-a | lti_granted | CEO | 982502 | Fail (hard) | CORE-02: 982502 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| canal-s-a | lti_granted | Management Board | 989544 | Fail (hard) | CORE-02: 989544 not in the quote; CORE-03: quote not in the source text; CORE-04: no period_end |
| canal-s-a | pay_currency | CEO | EUR | Fail | CORE-04: no period_end |
| canal-s-a | pay_currency | Management Board | EUR | Fail | CORE-04: no period_end |
| cancom-se-o-n | ebitda |  | 102700000 | Fail (hard) | CORE-02: 102.7 not in the quote |
| cancom-se-o-n | share_price |  | 26.65 | Fail (hard) | CORE-02: 26.65 not in the quote |
| capita-plc | share_price |  | 4.055 | Fail (hard) | CORE-02: 4.055 not in the quote |
| capita-plc | shares_outstanding |  | 120030667 | Fail (hard) | CORE-03: quote not in the source text |
| capital-limited | base_salary | Executive Chair | 528000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | base_salary | CEO (until 8 March 2025) | 442000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | base_salary | Executive Director | 417000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | lti_vested | Executive Chair | 95000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | lti_vested | CEO (until 8 March 2025) | 73000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | lti_vested | Executive Director | 49000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | sti_paid | Executive Chair | 722000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | sti_paid | Executive Director | 546000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | total_remuneration | Executive Chair | 1345000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | total_remuneration | CEO (until 8 March 2025) | 515000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| capital-limited | total_remuneration | Executive Director | 1012000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| carclo-plc | base_salary | Chief Executive Officer | 400000 | Fail (hard) | CORE-02: 400000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | base_salary | Chief Financial Officer (from  | 280000 | Fail (hard) | CORE-02: 280000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | benefits_value | Chief Executive Officer | 11000 | Fail (hard) | CORE-02: 11000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | benefits_value | Chief Financial Officer (from  | 12000 | Fail (hard) | CORE-02: 12000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | fte |  | 907 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | lti_vested | Chief Executive Officer | 149000 | Fail (hard) | CORE-02: 149000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | lti_vested | Chief Financial Officer (from  | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | pension_contribution | Chief Executive Officer | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | pension_contribution | Chief Financial Officer (from  | 16000 | Fail (hard) | CORE-02: 16000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | revenue_by_country |  | United Kingdom: 8125; Rest of  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| carclo-plc | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | sti_paid | Chief Executive Officer | 180000 | Fail (hard) | CORE-02: 180000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | sti_paid | Chief Financial Officer (from  | 101000 | Fail (hard) | CORE-02: 101000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | total_remuneration | Chief Executive Officer | 740000 | Fail (hard) | CORE-02: 740000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| carclo-plc | total_remuneration | Chief Financial Officer (from  | 409000 | Fail (hard) | CORE-02: 409000 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| cardiff-property-plc | exchange_segment |  | Main Market | Fail (hard) | CORE-02: not in the quote: main market |
| cardiff-property-plc | total_remuneration | Chief Executive Officer | 182000 | Fail (hard) | XF-01: parts add up to 206,000, more than the stated 182,000; XF-02: parts add up to 206,000, stated 182,000 |
| castings-plc | lti_vested | Company Secretary | 45000 | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | revenue_by_segment |  | Foundry operations: 171746; Ma | Fail (hard) | CORE-03: quote not in the source text |
| castings-plc | sti_paid | Company Secretary | 6000 | Fail (hard) | CORE-03: quote not in the source text |
| centrica-plc | fte |  | 22066 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| centrica-plc | listing_date |  | 1997-02-17 | Fail (hard) | CORE-02: not in the quote: 1997 |
| centrica-plc | lti_granted | Group Chief Executive | 150 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts GBP |
| centrica-plc | lti_granted | Group Chief Financial Officer | 125 | Fail (hard) | NUM-01: unit '' is not ISO 4217 |
| centrica-plc | revenue_by_segment |  | Retail: 16300; Optimisation: 5 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 22,365,000,000 vs 19,492,000,000 (14.7% apart) |
| centrica-plc | share_price |  | 1.4065 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| centrica-plc | staff_by_segment |  | Retail: 18504; Optimisation: 8 | Fail | NUM-08: adds up to 22,066 vs 21,000 (5.1% apart) |
| chemring-group-plc | lti_vested | Chief Financial Officer | 230000 | Fail (hard) | CORE-02: 230 not in the quote |
| chemring-group-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| chemring-group-plc | shares_outstanding |  | 272099390 | Fail (hard) | CORE-02: 272099390 not in the quote; CORE-03: quote not in the source text |
| chemring-group-plc | sti_max | Group Chief Executive | 150 | Fail (hard) | CORE-03: quote not in the source text |
| chemring-group-plc | sti_target | Group Chief Executive | 150 | Fail (hard) | CORE-03: quote not in the source text |
| close-brothers-group-plc | listing_date |  | 2983 | Fail (hard) | COD-06: not a year or a date |
| close-brothers-group-plc | lti_granted | Chief Executive (from 10 Septe | 726000 | Fail (hard) | CORE-02: 726 not in the quote |
| close-brothers-group-plc | revenue_by_segment |  | Commercial: 491.4; Retail: 364 | Fail | NUM-08: adds up to 1,070,800,000 vs 659,500,000 (62.4% apart) |
| cls-holdings-plc | fte |  | 113 | Fail (hard) | CORE-03: quote not in the source text; NUM-13: FTE 113 above headcount 86 |
| cls-holdings-plc | listing_date |  | 1994 | Fail (hard) | CORE-02: not in the quote: 1994 |
| cls-holdings-plc | revenue_by_country |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: quote not in the source text |
| cls-holdings-plc | revenue_by_segment |  | United Kingdom: 66.2; Germany: | Fail (hard) | CORE-03: quote not in the source text |
| cls-holdings-plc | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cls-holdings-plc | share_price |  | 44.25 | Fail (hard) | CORE-03: quote not in the source text; NUM-01: unit 'GBp' is not ISO 4217 |
| cls-holdings-plc | staff_by_segment |  | Property: 95; Hotel: 18 | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 113 vs 86 (31.4% apart) |
| cmb-tech-nv | base_salary | Management Board Members (excl | 1000000 | Fail (hard) | CORE-02: 1000000 not in the quote |
| cmb-tech-nv | benefits |  | Fringe benefits include health | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| cmb-tech-nv | pension_contribution | CEO | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmb-tech-nv | sti_paid | CEO | 62499 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmb-tech-nv | sti_paid | Management Board Members (excl | 250000 | Fail (hard) | CORE-02: 250000 not in the quote |
| cmb-tech-nv | total_remuneration | CEO | 312495 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-02: parts add up to 62,499, stated 312,495 |
| cmc-markets-plc | controlling_owner |  | family | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmc-markets-plc | controlling_owner_name |  | Lord Peter Andrew Cruddas | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmc-markets-plc | ebitda |  | 117842 | Fail (hard) | CORE-02: 117.842 not in the quote |
| cmc-markets-plc | ownership_type |  | family_owned | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmc-markets-plc | revenue_by_country |  | UK: 133.4; Rest of the world:  | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cmc-markets-plc | revenue_by_segment |  | Trading: 333694; Investing: 84 | Fail | NUM-08: adds up to 418,667,000 vs 376,756,000 (11.1% apart) |
| commerzbank-ag | base_salary | ehemaliger Vorsitzender (bis 3 | 481000 | Fail (hard) | CORE-02: 481 not in the quote; CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| commerzbank-ag | benefits_value | Vorsitzende (seit 1. Oktober 2 | 228000 | Fail (hard) | CORE-02: 228 not in the quote; CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
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
| commerzbank-ag | pension_contribution | ehemaliger Vorsitzender (bis 3 | 159000 | Fail (hard) | CORE-02: 159 not in the quote; CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
| commerzbank-ag | pension_type |  | Beitragsorientierte Versorgung | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | role_disclosure | Vorsitzende (seit 1. Oktober 2 | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | stellvertretender Vorsitzender | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Chief Financial Officer (seit  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Chief Risk Officer (seit 1. Ja | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Chief Operating Officer (seit  | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | Former Management Board Member | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | role_disclosure | ehemaliger Vorsitzender (bis 3 | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| commerzbank-ag | shareholding_requirement |  | Sämtliche Mitglieder des Vorst | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| commerzbank-ag | total_remuneration | Vorsitzende (seit 1. Oktober 2 | 3744000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 3,511,000, stated 3,744,000 |
| commerzbank-ag | total_remuneration | stellvertretender Vorsitzender | 2917000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 2,453,000, stated 2,917,000 |
| commerzbank-ag | total_remuneration | Group Human Resources & Group  | 2116000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 1,880,000, stated 2,116,000 |
| commerzbank-ag | total_remuneration | Segment Privat- und Unternehme | 2086000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 1,904,000, stated 2,086,000 |
| commerzbank-ag | total_remuneration | Chief Financial Officer (seit  | 1896000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 1,281,000, stated 1,896,000 |
| commerzbank-ag | total_remuneration | Chief Risk Officer (seit 1. Ja | 2113000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 1,500,000, stated 2,113,000 |
| commerzbank-ag | total_remuneration | Chief Operating Officer (seit  | 2312000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end; XF-02: parts add up to 1,620,000, stated 2,312,000 |
| continental-ag-o-n | role_disclosure | Former Group Human Relations a | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | role_disclosure | Former Vorstandsmitglied (unti | individual | Fail (hard) | CORE-03: quote not in the source text |
| continental-ag-o-n | total_remuneration | Automotive, Vorstandsmitglied  | 1537000 | Fail (hard) | XF-01: parts add up to 1,590,000, more than the stated 1,537,000; XF-02: parts add up to 1,590,000, stated 1,537,000 |
| continental-ag-o-n | total_remuneration | Tires, Vorstandsmitglied seit  | 1739000 | Fail (hard) | XF-01: parts add up to 1,901,000, more than the stated 1,739,000; XF-02: parts add up to 1,901,000, stated 1,739,000 |
| continental-ag-o-n | total_remuneration | ContiTech, Vorstandsmitglied s | 1467000 | Fail (hard) | XF-01: parts add up to 1,747,000, more than the stated 1,467,000; XF-02: parts add up to 1,747,000, stated 1,467,000 |
| corem-property-d | benefits |  | company car, health insurance | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| corem-property-d | pay_currency | Vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Vice vd | SEK | Fail | CORE-04: no period_end |
| corem-property-d | pay_currency | Andra ledande befattningshavar | SEK | Fail | CORE-04: no period_end |
| corem-property-d | sti_paid | Andra ledande befattningshavar | 900000 | Fail (hard) | CORE-02: 0.9 not in the quote; CORE-04: no period_end |
| costain-group-plc | base_salary | Chief Financial Officer | 439544 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | benefits_value | Chief Financial Officer | 14945 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | ebitda |  | 47100000 | Fail (hard) | NUM-01: unit '£' is not ISO 4217 |
| costain-group-plc | fte |  | 3049 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | lti_vested | Chief Financial Officer | 1040064 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | pension_contribution | Chief Financial Officer | 43954 | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | revenue_by_segment |  | Natural Resources: 440.4; Tran | Fail (hard) | CORE-03: quote not in the source text |
| costain-group-plc | share_price |  | 160 | Fail (hard) | NUM-01: unit 'pence' is not ISO 4217 |
| costain-group-plc | sti_paid | Chief Financial Officer | 565196 | Fail (hard) | CORE-03: quote not in the source text |
| cranswick-plc | fte |  | 13033 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| cranswick-plc | share_price |  | 5130 | Fail (hard) | NUM-01: unit 'GBp' is not ISO 4217 |
| dellia-group | ebitda |  | 74500000 | Fail (hard) | CORE-03: quote not in the source text |
| dellia-group | listing_date |  | 2025-09-29 | Fail (hard) | CORE-02: not in the quote: 2025 |
| delticom-ag-na-o-n | listing_date |  | October 2006 | Fail (hard) | CORE-02: not a year or a date (see COD-06); COD-06: not a year or a date |
| delticom-ag-na-o-n | share_price |  | 2.14 | Fail (hard) | CORE-02: 2.14 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_granted | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Executive Officer (since | 243750 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | lti_target | Chief Financial Officer (since | 192000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | share_price |  | 0.39 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | sti_max | Chief Financial Officer (since | 264000 | Fail (hard) | CORE-03: quote not in the source text |
| demire-deutsche-mittelstand-real-estate-ag | sti_target | Chief Financial Officer (since | 132000 | Fail (hard) | CORE-03: quote not in the source text |
| digia-oyj | aggregate_headcount | Other key personnel | 20 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| digia-oyj | revenue_by_segment |  | Total: 217 | Fail | CORE-04: no period_end |
| digia-oyj | shareholding_requirement |  | participants have the chance t | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| digia-oyj | staff_by_country |  | Finland: 1409; Sweden: 120; Po | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| erste-group-bank-ag | benefits |  | insurance benefits, other non- | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | exchange |  | Vienna | Fail (hard) | COD-01: 'Vienna' matches no ISO 10383 exchange |
| erste-group-bank-ag | listing_date |  | 1997-12-04 | Fail (hard) | CORE-02: not in the quote: 1997 |
| erste-group-bank-ag | lti_granted | Vorsitzender des Vorstands / C | 960000 | Fail (hard) | CORE-02: 960000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Corporates and Markets O | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Financial Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Risk Officer | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_granted | Chief Platform Officer / Chief | 636000 | Fail (hard) | CORE-02: 636000 not in the quote |
| erste-group-bank-ag | lti_vested | Chief Corporates and Markets O | 939970.49 | Fail (hard) | CORE-02: 939970.49 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| erste-group-bank-ag | lti_vested | Chief Financial Officer | 939791.52 | Fail (hard) | CORE-02: 939791.52 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| erste-group-bank-ag | lti_vested | Chief Risk Officer | 938922.19 | Fail (hard) | CORE-02: 938922.19 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| erste-group-bank-ag | lti_vested | Chief Platform Officer / Chief | 463518.82 | Fail (hard) | CORE-02: 463518.82 not in the quote; CORE-03: source not cached; the run itself did not find the quote |
| erste-group-bank-ag | other_names |  | Erste oesterreichische Spar-Ca | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| erste-group-bank-ag | staff_by_country |  | Austria: 20111; Czechia: 10097 | Fail | CORE-04: no period_end; NUM-08: adds up to 49,024 vs 46,000 (6.6% apart) |
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
| fastpartner-d | base_salary | Other members of the Executive | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | base_salary | Other senior executives | 12529000 | Fail (hard) | CORE-02: 12.529 not in the quote |
| fastpartner-d | pension_contribution | Other members of the Executive | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | pension_contribution | Other senior executives | 3667000 | Fail (hard) | CORE-02: 3.667 not in the quote |
| fastpartner-d | share_price |  | 47.45 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| fastpartner-d | sti_max | Other senior executives | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_paid | Other members of the Executive | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| fastpartner-d | sti_paid | Other senior executives | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| flughafen-wien-ag | base_salary | Management Board | 1186800 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | base_salary | Key employees | 5002300 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | benefits_value | Management Board | 12200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | benefits_value | Key employees | 41200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | exchange_segment |  | Kassamarkt | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | lti_granted | Management Board | 863200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | pension_contribution | Management Board | 169600 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | pension_contribution | Key employees | 40000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | revenue_by_country |  | Austria: 971981.6; Malta: 1569 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | role_disclosure | Management Board | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | role_disclosure | Supervisory Board | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | role_disclosure | Key employees | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | staff_by_segment |  | Airport: 561; Handling & Secur | Fail | NUM-08: adds up to 5,252 vs 6,774 (22.5% apart) |
| flughafen-wien-ag | sti_paid | Management Board | 452200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| flughafen-wien-ag | sub_sector |  | The FWAG Group generates reven | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| flughafen-wien-ag | total_remuneration | Management Board | 2514400 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; XF-01: parts add up to 2,684,000, more than the stated 2,514,400; XF-02: parts add up to 2,684,000, stated 2,514,400 |
| flughafen-wien-ag | total_remuneration | Key employees | 5169200 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| hermana-holding | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| hermana-holding | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| himalaya-shipping | controlling_owner_name |  | Drew Holdings Ltd. | Fail (hard) | CORE-02: not in the quote: ltd |
| himalaya-shipping | ebitda |  | 97400000 | Fail (hard) | NUM-01: unit '$' is not ISO 4217 |
| himalaya-shipping | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| holand-og-setskog-sparebank | ebitda |  | 57700000 | Fail (hard) | CORE-02: 57.7 not in the quote |
| holand-og-setskog-sparebank | revenue_by_segment |  | Privatmarked: 137049; Bedrifts | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 227,561,000 vs 195,672,000 (16.3% apart) |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (1) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| holand-og-setskog-sparebank | role_disclosure | Banksjef (2) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| intea-fastigheter-d | pay_currency | Verkställande direktör | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pay_currency | Övriga ledande befattningshava | SEK | Fail | CORE-04: no period_end |
| intea-fastigheter-d | pension_contribution | Övriga ledande befattningshava | 1300000 | Fail (hard) | CORE-02: 1.3 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Verkställande direktör | 3800000 | Fail (hard) | CORE-02: 3.8 not in the quote; CORE-04: no period_end |
| intea-fastigheter-d | total_remuneration | Övriga ledande befattningshava | 5800000 | Fail (hard) | CORE-02: 5.8 not in the quote; CORE-03: source not cached; the run itself did not find the quote; CORE-04: no period_end |
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
| kesko-b | aggregate_headcount | Group Management Board | 7 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| kesko-b | role_disclosure | Hallituksen jäsenet | aggregate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| kesko-b | staff_by_segment |  | Grocerytrade: 6257; Buildingan | Fail | NUM-08: adds up to 14,766 vs 17,702 (16.6% apart) |
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
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| public-property-invest | largest_holders |  | Samhällsbyggnadsbolaget i Nord | Fail (hard) | CORE-03: quote not in the source text |
| public-property-invest | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
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
| seb-a | benefits_value | Other members of the Group Exe | 2171847 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | lti_granted | CEO | 5875000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | lti_vested | CEO | 16884000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | pension_contribution | CEO | 5250000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | pension_contribution | Deputy CEO (Mats Torstendahl) | 0 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | pension_contribution | Deputy CEO (Jonas Ahlström) | 1806000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | revenue_by_country |  | Sweden: 113051; Denmark: 8466; | Fail | NUM-08: adds up to 195,269,000,000 vs 76,939,000,000 (153.8% apart) |
| seb-a | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| seb-a | total_remuneration | CEO | 37519000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | total_remuneration | Deputy CEO (Mats Torstendahl) | 8887000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | total_remuneration | Deputy CEO (Jonas Ahlström) | 12911000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| seb-a | total_remuneration | Other members of the Group Exe | 85984864 | Fail (hard) | XF-01: parts add up to 105,243,201, more than the stated 85,984,864; XF-02: parts add up to 105,243,201, stated 85,984,864 |
| sed-energy | pay_currency | Key management personnel | USD | Fail | CORE-04: no period_end |
| sentia | base_salary | Konsernsjef | 4309000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | base_salary | Visekonsernsjef og konserndire | 3132000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | base_salary | Konserndirektør HENT | 1700000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | base_salary | Konserndirektør kommunikasjon  | 901000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | benefits_value | Konsernsjef | 260000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | benefits_value | Visekonsernsjef og konserndire | 248000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | benefits_value | Konserndirektør HENT | 58000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | benefits_value | Konserndirektør kommunikasjon  | 63000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | controlling_owner |  | corporate | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | controlling_owner_name |  | Ratos AB | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | ebitda |  | 683000000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | largest_holders |  | Ratos AB 39% | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | ownership_type |  | subsidiary | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | pay_currency | Konsernsjef | kroner | Fail (hard) | COD-01: kroner is not ISO 4217 |
| sentia | pay_currency | Visekonsernsjef og konserndire | kroner | Fail (hard) | COD-01: kroner is not ISO 4217 |
| sentia | pay_currency | Konserndirektør HENT | kroner | Fail (hard) | COD-01: kroner is not ISO 4217 |
| sentia | pay_currency | Konserndirektør kommunikasjon  | kroner | Fail (hard) | COD-01: kroner is not ISO 4217 |
| sentia | pe_stake_5pct |  | no | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | pension_contribution | Konsernsjef | 422000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | pension_contribution | Visekonsernsjef og konserndire | 910000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | pension_contribution | Konserndirektør HENT | 97000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | pension_contribution | Konserndirektør kommunikasjon  | 38000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | revenue_by_country |  | Norge: 9404; Sverige: 2369 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | revenue_by_segment |  | HENT: 9404; Sentia Sverige: 23 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sentia | share_price |  | 62.99 | Fail (hard) | CORE-02: 62.99 not in the quote; NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | staff_by_country |  | Norge: 1344; Sverige: 172 | Fail | NUM-08: adds up to 1,516 vs 6 (25166.7% apart) |
| sentia | staff_by_segment |  | HENT: 1338; Sentia Sverige: 17 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote; NUM-08: adds up to 1,516 vs 6 (25166.7% apart) |
| sentia | sti_paid | Konsernsjef | 2159000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | sti_paid | Visekonsernsjef og konserndire | 461000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | sti_paid | Konserndirektør HENT | 0 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | sti_paid | Konserndirektør kommunikasjon  | 0 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | total_remuneration | Konsernsjef | 7150000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | total_remuneration | Visekonsernsjef og konserndire | 4751000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | total_remuneration | Konserndirektør HENT | 1854000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sentia | total_remuneration | Konserndirektør kommunikasjon  | 1002000 | Fail (hard) | NUM-01: unit 'kroner' is not ISO 4217 |
| sparebank-1-helgeland | base_salary | Administrerende direktør | 2918081 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | base_salary | Finansdirektør | 1758912 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | base_salary | Direktør risikostyring | 1587358 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | base_salary | Direktør forretningsutvikling | 1657756 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Administrerende direktør | 274607 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Finansdirektør | 83294 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Direktør risikostyring | 95655 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Direktør forretningsutvikling | 96803 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Tidligere adm.dir (Lisbeth Flå | 31338 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | benefits_value | Tidligere adm dir. (Arnt Krane | 1979 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Administrerende direktør | 305424 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Finansdirektør | 275351 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Direktør risikostyring | 279012 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Direktør forretningsutvikling | 273096 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Tidligere adm.dir (Lisbeth Flå | 634351 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | pension_contribution | Tidligere adm dir. (Arnt Krane | 171925 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | revenue_by_segment |  | Retail division: 3198; Corpora | Fail | CORE-04: no period_end; NUM-08: adds up to 6,786,000,000 vs 14,040,000,000 (51.7% apart) |
| sparebank-1-helgeland | role_disclosure | Administrerende direktør | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Finansdirektør | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Direktør risikostyring | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Direktør forretningsutvikling | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Direktør bedriftsmarked | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Tidligere adm.dir (Lisbeth Flå | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | role_disclosure | Tidligere adm dir. (Arnt Krane | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | sti_paid | Direktør risikostyring | 20000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Administrerende direktør | 3518112 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Finansdirektør | 2137557 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Direktør risikostyring | 1982025 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Direktør forretningsutvikling | 2047655 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Tidligere adm.dir (Lisbeth Flå | 665689 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| sparebank-1-helgeland | total_remuneration | Tidligere adm dir. (Arnt Krane | 173904 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
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
| subsea7 | pay_currency | CHIEF EXECUTIVE OFFICER | USD | Fail | CORE-04: no period_end |
| subsea7 | pay_currency | CHIEF FINANCIAL OFFICER | USD | Fail | CORE-04: no period_end |
| subsea7 | pay_currency | Executive Management Team | USD | Fail | CORE-04: no period_end |
| tekna-holding | base_salary | CEO (2014 - April 27, 2025) | 156000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | base_salary | VP Operations (2020 - 2025) | 44000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | benefits |  | Health insurance plan for its  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| tekna-holding | benefits_value | CFO (2023 - ) | 2000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | benefits_value | CEO (2014 - April 27, 2025) | 18000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | benefits_value | VP Operations (2020 - 2025) | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | controlling_owner_name |  | Arendals Fossekompani ASA | Fail (hard) | CORE-02: not in the quote: arendals fossekompani asa |
| tekna-holding | lti_granted | CEO (2025 - ) | 1000000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | EVP - Materials, Managing dire | 200000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | CFO Tekna Holding Canada Inc ( | 200000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_granted | Executive Leadership Team | 2000000 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_vested | EVP - Materials, Managing dire | 46667 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | lti_vested | Executive Leadership Team | 186667 | Fail (hard) | NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CAD |
| tekna-holding | pension_contribution | VP Operations (2020 - 2025) | 1000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | revenue_by_country |  | America: 19803; Europe: 10036; | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | revenue_by_segment |  | Systems & Equipment: 6431; Mat | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | role_disclosure | CFO (2023 - ) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | role_disclosure | CEO (2014 - April 27, 2025) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | role_disclosure | VP Operations (2020 - 2025) | individual | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | total_remuneration | CEO (2014 - April 27, 2025) | 174000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| tekna-holding | total_remuneration | VP Operations (2020 - 2025) | 46000 | Fail (hard) | CORE-03: source not cached; the run itself did not find the quote |
| uie | pay_currency | Managing Director | USD | Fail | CORE-04: no period_end |
