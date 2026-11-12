# Output checks: dach_set2_datapoints.csv

125 companies, 4292 filled values checked (2026-11-12, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 3609 (84%) |
| Review | 338 (8%) |
| Fail | 45 (1%) |
| Fail (hard) | 300 (7%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 437 | 434 | 0 | 0 | 3 |
| Listing and market | 387 | 374 | 0 | 0 | 13 |
| Sector | 121 | 114 | 0 | 0 | 7 |
| Reporting basis | 332 | 330 | 0 | 0 | 2 |
| Financials | 234 | 159 | 49 | 0 | 26 |
| Workforce | 98 | 75 | 5 | 0 | 18 |
| Ownership and control | 290 | 279 | 0 | 0 | 11 |
| Segment and geography | 94 | 42 | 27 | 4 | 21 |
| Pay policy | 198 | 183 | 0 | 0 | 15 |
| Role and disclosure | 665 | 590 | 3 | 41 | 31 |
| Pay: fixed | 541 | 398 | 90 | 0 | 53 |
| Pay: STI | 348 | 258 | 56 | 0 | 34 |
| Pay: LTI | 302 | 217 | 51 | 0 | 34 |
| Pay: total | 245 | 156 | 57 | 0 | 32 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 4292 | 4288 | 4 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 1906 | 1750 | 156 | 2386 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 3027 | 2910 | 117 | 1265 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 2406 | 2053 | 353 | 1886 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 4292 | 4291 | 1 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 1381 | 1365 | 16 | 2911 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 60 | 60 | 0 | 4232 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 138 | 138 | 0 | 4154 |  |
| COD-06 | Dates are valid | yes | 163 | 158 | 5 | 4129 | not a year or a date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1324 | 1318 | 6 | 2968 | unit '' is not ISO N |
| NUM-02 | Printed figure and unit recorded |  | 1294 | 1294 | 0 | 2998 |  |
| NUM-04 | Magnitude in a plausible range |  | 1542 | 1526 | 16 | 2750 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 173 | 171 | 2 | 4119 | not a whole number |
| NUM-06 | Percentages in range | yes | 184 | 183 | 1 | 4108 | N % of base salary |
| NUM-07 | Holdings add up to 100% or less | yes | 44 | 43 | 1 | 4248 | holdings add up to N% |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 94 | 63 | 31 | 4198 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 170 | 170 | 0 | 4122 |  |
| NUM-11 | STI paid not above its maximum |  | 43 | 42 | 1 | 4249 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1143 | 1140 | 3 | 3149 | currency N the role's other amounts CHF |
| NUM-13 | FTE not above headcount |  | 44 | 41 | 3 | 4248 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 0 | 0 | 0 | 4292 |  |
| DER-06 | Derived value shows its formula |  | 141 | 141 | 0 | 4151 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 201 | 187 | 14 | 4091 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 201 | 152 | 49 | 4091 | parts add up to N stated N |

## Fill rate

Company fields: 2191 of 5125 filled (43%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 5 | 125 |
| staff_by_segment | 16 | 125 |
| staff_by_country | 20 | 125 |
| revenue_by_country | 26 | 125 |
| market_cap_band | 30 | 125 |
| share_price | 31 | 125 |
| revenue_by_segment | 32 | 125 |
| shareholding_requirement | 34 | 125 |
| other_names | 36 | 125 |
| controlling_owner_name | 41 | 125 |
| exchange_segment | 42 | 125 |
| largest_holders | 44 | 125 |
| pe_stake_5pct | 44 | 125 |
| ebitda | 45 | 125 |
| fte | 45 | 125 |
| controlling_owner | 50 | 125 |
| ownership_type | 50 | 125 |
| listing_date | 52 | 125 |
| total_assets | 52 | 125 |
| accounting_basis | 52 | 125 |
| revenue | 53 | 125 |
| headcount | 53 | 125 |
| shares_outstanding | 53 | 125 |
| reporting_currency | 58 | 125 |
| sector_code | 60 | 125 |
| website | 61 | 125 |
| sub_sector | 61 | 125 |
| ultimate_parent | 61 | 125 |
| ticker | 63 | 125 |
| isin | 66 | 125 |
| legal_name | 67 | 125 |
| lei | 67 | 125 |
| business_id | 67 | 125 |
| exchange | 67 | 125 |
| listing_status | 67 | 125 |
| country_code | 67 | 125 |
| head_office_city | 67 | 125 |
| benefits | 81 | 125 |
| pension_type | 83 | 125 |
| fiscal_year | 111 | 125 |
| fiscal_year_end | 111 | 125 |

Pay fields, over 262 executive roles:

| Field | Filled |
|---|---|
| base_salary | 212 (81%) |
| sti_paid | 190 (73%) |
| sti_target | 68 (26%) |
| sti_max | 90 (34%) |
| lti_vested | 54 (21%) |
| lti_granted | 116 (44%) |
| lti_target | 61 (23%) |
| lti_max | 71 (27%) |
| benefits_value | 164 (63%) |
| pension_contribution | 165 (63%) |
| total_remuneration | 245 (94%) |

## Failed values (345)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| 2invest-ag-bf4e0781 | base_salary | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| 2invest-ag-bf4e0781 | total_remuneration | Vorstand | 72000 | Fail (hard) | CORE-02: 72 not in the quote |
| addex-therapeutics-ltd | lti_granted | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | lti_granted | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | lti_granted | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Executive Management | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217; NUM-12: currency , the role's other amounts CHF |
| addex-therapeutics-ltd | sti_paid | Head of Finance | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| addex-therapeutics-ltd | sti_paid | Chief Executive Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-01: unit '' is not ISO 4217 |
| adval-tech-holding-ag | listing_date |  | 1998 | Fail (hard) | CORE-02: not in the quote: 1998 |
| aevis-victoria-sa | aggregate_headcount | Other Members of Senior Manage | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| aevis-victoria-sa | base_salary | Other Members of Senior Manage | 1202900 | Fail (hard) | CORE-02: 1202.9 not in the quote |
| aevis-victoria-sa | ebitda |  | 72446000 | Fail (hard) | CORE-02: 72446 not in the quote |
| aevis-victoria-sa | fte |  | 4870 | Fail (hard) | CORE-02: 4870 not in the quote |
| aevis-victoria-sa | revenue |  | 1208366000 | Fail (hard) | CORE-02: 1208366 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | total_assets |  | 1905326000 | Fail (hard) | CORE-02: 1905326 not in the quote; CORE-04: no period_end |
| aevis-victoria-sa | total_remuneration | Executive Chairman (as of 21.0 | 1250600 | Fail (hard) | CORE-02: 1250.6 not in the quote |
| aevis-victoria-sa | total_remuneration | Other Members of Senior Manage | 2098600 | Fail (hard) | CORE-02: 2098.6 not in the quote |
| alcon-inc | lti_max | CEO | 1150 | Fail (hard) | NUM-06: 1150 % of base salary |
| allgeier-se-9971b49d | pension_type |  | defined benefit plans; defined | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| allreal-holding-ag | ebitda |  | 310500000 | Fail (hard) | CORE-03: quote not in the source text |
| allreal-holding-ag | lti_target | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | lti_target | Other members of Group Managem | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| allreal-holding-ag | staff_by_segment |  | Real Estate: 50 | Fail | CORE-04: no period_end; NUM-08: adds up to 50 vs 224 (77.7% apart) |
| alpine-select-ag | benefits |  | fringe benefits, flat-rat allo | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| alpine-select-ag | fte |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| alpine-select-ag | headcount |  | 3 | Fail (hard) | CORE-02: 3 not in the quote |
| amrize-ltd | benefits |  | deferred compensation plan, 40 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | lti_granted | Chief Executive Officer (23 Ju | 9942122 | Fail (hard) | CORE-02: 9942122 not in the quote |
| amrize-ltd | lti_granted | Other Members of Executive Man | 12411396 | Fail (hard) | CORE-02: 12411396 not in the quote |
| amrize-ltd | pension_type |  | defined benefit (cash balance  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| amrize-ltd | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| amrize-ltd | sub_sector |  | The Company is organized into  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| apg-sga-sa-8679206d | benefits_value | Executive Board | 619000 | Fail (hard) | CORE-02: 619000 not in the quote |
| apg-sga-sa-8679206d | benefits_value | Chief Executive Officer | 182000 | Fail (hard) | CORE-02: 182000 not in the quote |
| arbonia-ag | base_salary | Other members of Group Managem | 628000 | Fail (hard) | CORE-02: 628 not in the quote |
| arbonia-ag | benefits_value | Other members of Group Managem | 40000 | Fail (hard) | CORE-02: 40 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | lti_granted | Other members of Group Managem | 149000 | Fail (hard) | CORE-02: 149 not in the quote |
| arbonia-ag | pension_contribution | Other members of Group Managem | 147000 | Fail (hard) | CORE-02: 147 not in the quote; CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | Group Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| arbonia-ag | sti_paid | Other members of Group Managem | 542000 | Fail (hard) | CORE-02: 542 not in the quote |
| arbonia-ag | total_remuneration | Other members of Group Managem | 1507000 | Fail (hard) | CORE-02: 1507 not in the quote |
| asmallworld-ag | sub_sector |  | ASMALLWORLD Bespoke Travel tea | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| autoneum-holding-ag | base_salary | All members | 3012658 | Fail (hard) | CORE-02: 3012658 not in the quote |
| autoneum-holding-ag | base_salary | CEO | 870000 | Fail (hard) | CORE-02: 870000 not in the quote |
| autoneum-holding-ag | base_salary | Other members of Group Executi | 2142658 | Fail (hard) | CORE-02: 2142658 not in the quote |
| autoneum-holding-ag | benefits_value | Other members of Group Executi | 830372 | Fail (hard) | CORE-02: 830372 not in the quote |
| autoneum-holding-ag | lti_granted | Other members of Group Executi | 393122 | Fail (hard) | CORE-02: 393122 not in the quote |
| autoneum-holding-ag | sti_paid | Other members of Group Executi | 1568370 | Fail (hard) | CORE-02: 1568370 not in the quote |
| autoneum-holding-ag | total_remuneration | Other members of Group Executi | 4934523 | Fail (hard) | CORE-02: 4934523 not in the quote |
| avolta-ag | base_salary | Other members of Global Execut | 6297100 | Fail (hard) | CORE-02: 6297.1 not in the quote |
| avolta-ag | lti_granted | Other members of Global Execut | 5772800 | Fail (hard) | CORE-02: 5772.8 not in the quote |
| avolta-ag | pension_contribution | Other members of Global Execut | 1310800 | Fail (hard) | CORE-02: 1310.8 not in the quote |
| avolta-ag | revenue_by_segment |  | Europe, Middle East and Africa | Fail (hard) | CORE-03: quote on page 207, link says page 206 |
| avolta-ag | sti_paid | Other members of Global Execut | 7231600 | Fail (hard) | CORE-02: 7231.6 not in the quote |
| avolta-ag | total_remuneration | Other members of Global Execut | 21103400 | Fail (hard) | CORE-02: 21103.4 not in the quote |
| bachem-holding-ag | lti_granted | Rest of the Corporate Executiv | 261000 | Fail (hard) | CORE-02: 261 not in the quote |
| bachem-holding-ag | pension_contribution | Rest of the Corporate Executiv | 274000 | Fail (hard) | CORE-02: 274 not in the quote |
| bachem-holding-ag | revenue |  | 695070000 | Fail (hard) | CORE-02: 695070 not in the quote |
| bachem-holding-ag | sti_paid | CEO | 247000 | Fail (hard) | CORE-02: 247 not in the quote |
| bachem-holding-ag | sti_paid | Corporate Executive Committee | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| bachem-holding-ag | sti_paid | Rest of the Corporate Executiv | 592000 | Fail (hard) | CORE-02: 592 not in the quote |
| barry-callebaut-ag | pension_type |  | Defined benefit plans in Switz | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| barry-callebaut-ag | share_price |  | 1376 | Fail (hard) | CORE-03: quote not in the source text |
| basellandschaftliche-kantonalbank | lti_granted | Other members of the Managemen | 605000 | Fail (hard) | CORE-02: 605000 not in the quote |
| basellandschaftliche-kantonalbank | pension_type |  | defined contribution, BLKB cov | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | shareholding_requirement |  | Bankrat members must acquire 2 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| basellandschaftliche-kantonalbank | total_remuneration | CEO (until 31.7.2025) | 664000 | Fail (hard) | XF-01: parts add up to 844,926, more than the stated 664,000; XF-02: parts add up to 844,926, stated 664,000 |
| basellandschaftliche-kantonalbank | total_remuneration | Other members of the Managemen | 2831670 | Fail (hard) | XF-01: parts add up to 3,511,435, more than the stated 2,831,670; XF-02: parts add up to 3,511,435, stated 2,831,670 |
| basilea-pharmaceutica-ag-allschwil | base_salary | Other members of the managemen | 1564573 | Fail (hard) | CORE-02: 1564573 not in the quote |
| basilea-pharmaceutica-ag-allschwil | lti_granted | Other members of the managemen | 1173367 | Fail (hard) | CORE-02: 1173367 not in the quote |
| basilea-pharmaceutica-ag-allschwil | pension_contribution | Other members of the managemen | 475160 | Fail (hard) | CORE-02: 475160 not in the quote |
| basilea-pharmaceutica-ag-allschwil | sti_paid | Other members of the managemen | 815877 | Fail (hard) | CORE-02: 815877 not in the quote |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Chief Executive Officer | 1903815 | Fail (hard) | XF-01: parts add up to 2,116,432, more than the stated 1,903,815; XF-02: parts add up to 2,116,432, stated 1,903,815 |
| basilea-pharmaceutica-ag-allschwil | total_remuneration | Other members of the managemen | 3028977 | Fail (hard) | CORE-02: 3028977 not in the quote; XF-02: parts add up to 2,855,610, stated 3,028,977 |
| basler-kantonalbank | total_remuneration | CEO (ab 1.3.2025), Mitglied de | 834147 | Fail (hard) | XF-01: parts add up to 1,006,080, more than the stated 834,147; XF-02: parts add up to 1,006,080, stated 834,147 |
| basler-kantonalbank | total_remuneration | Geschäftsleitungsmitglieder | 3498135 | Fail (hard) | XF-01: parts add up to 4,265,533, more than the stated 3,498,135; XF-02: parts add up to 4,265,533, stated 3,498,135 |
| belimo-holding-ag | base_salary | Other members, Executive Commi | 2108000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | role_disclosure | Other members, Executive Commi | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | sti_paid | Other members, Executive Commi | 2449000 | Fail (hard) | CORE-03: quote not in the source text |
| belimo-holding-ag | total_remuneration | CEO | 1749000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,539,000, stated 1,749,000 |
| belimo-holding-ag | total_remuneration | Other members, Executive Commi | 5573000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 5,108,000, stated 5,573,000 |
| bell-food-group-ag | aggregate_headcount | Other members of the Group Exe | 8 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bellevue-group-ag | role_disclosure | Group Executive Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | benefits |  | company car (including private | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| berentzen-gruppe-ag-957f8708 | benefits_value | Member of the Executive Board  | 42300 | Fail (hard) | CORE-02: 42.3 not in the quote |
| berentzen-gruppe-ag-957f8708 | lti_vested | Member of the Executive Board  | 135400 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | lti_vested | Member of the Executive Board  | 135400 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | sti_paid | Member of the Executive Board  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| berentzen-gruppe-ag-957f8708 | sti_paid | Member of the Executive Board  | 0 | Fail (hard) | CORE-03: quote not in the source text |
| berner-kantonalbank-ag | aggregate_headcount | Geschäftsleitung | 6.6 | Fail (hard) | NUM-05: not a whole number |
| berner-kantonalbank-ag | pension_type |  | defined contribution, employer | Fail (hard) | CORE-03: quote not in the source text |
| bijou-brigitte-c3387b07 | revenue_by_country |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bijou-brigitte-c3387b07 | revenue_by_segment |  | Germany: 169310382.43; Spain:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| bkw-ag | sti_target | CEO | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bkw-ag | sti_target | Group Executive Board | 30 | Fail (hard) | CORE-03: quote not in the source text |
| bucher-industries-ag | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| burckhardt-compression-holding-ag | benefits_value | CEO | 221000 | Fail (hard) | CORE-02: 221 not in the quote |
| burckhardt-compression-holding-ag | benefits_value | Other members of the Executive | 488000 | Fail (hard) | CORE-02: 488 not in the quote |
| burckhardt-compression-holding-ag | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| burckhardt-compression-holding-ag | sti_target | CEO | 0.28 | Fail (hard) | COD-01: unit '' is not a target form |
| burkhalter-holding-ag | listing_date |  | June 2008 | Fail (hard) | COD-06: not a year or a date |
| burkhalter-holding-ag | staff_by_segment |  | Elektro: 3410; HLKS: 1525 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end; NUM-08: adds up to 4,935 vs 3,361 (46.8% apart) |
| bvz-holding-ag | aggregate_headcount | Geschäftsleitung | 7 | Fail (hard) | CORE-03: quote not in the source text |
| bvz-holding-ag | role_disclosure | Geschäftsleitung | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| bystronic-ag | aggregate_headcount | Executive Committee | 4.1 | Fail (hard) | NUM-05: not a whole number |
| bystronic-ag | lti_target | Executive Committee | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | lti_target | CEO | 20 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | Executive Committee | 25 | Fail (hard) | COD-01: unit '' is not a target form |
| bystronic-ag | sti_target | CEO | 30 | Fail (hard) | COD-01: unit '' is not a target form |
| c-capital-holdings-ag-53a1594e | lti_granted | Key management personnel | 5000000 | Fail (hard) | CORE-03: quote not in the source text |
| calida-holding-ag-1793bfba | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
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
| cham-swiss-properties-ag-7d9cb227 | base_salary | Former members of group manage | 747000 | Fail (hard) | CORE-02: 747 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | CEO | 227000 | Fail (hard) | CORE-02: 227 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Other members of group managem | 409000 | Fail (hard) | CORE-02: 409 not in the quote |
| cham-swiss-properties-ag-7d9cb227 | sti_paid | Former members of group manage | 89000 | Fail (hard) | CORE-02: 89 not in the quote |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | listing_date |  | 1986 | Fail (hard) | CORE-02: not in the quote: 1986 |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | revenue_by_segment |  | Europe: 2955.5; North America: | Fail (hard) | CORE-03: quote not in the source text |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | shares_outstanding |  | 1095704 | Fail (hard) | CORE-02: 1095704 not in the quote |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | staff_by_country |  | North America: 4220; Europe: 9 | Fail (hard) | CORE-03: quote not in the source text |
| chocoladefabriken-lindt-sprungli-ag-f056b804 | staff_by_segment |  | North America: 4220; Europe: 9 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | base_salary | Group Management | 1204000 | Fail (hard) | CORE-03: quote not in the source text |
| cicor-technologies-ltd-39bd9715 | total_remuneration | Group Management | 4564000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,293,000, stated 4,564,000 |
| cicor-technologies-ltd-39bd9715 | total_remuneration | CEO | 2051000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,072,000, stated 2,051,000 |
| clariant-ag-0616ec80 | lti_granted | Other ESC members | 2389017 | Fail (hard) | CORE-02: 2389017 not in the quote; CORE-03: quote not in the source text |
| clariant-ag-0616ec80 | shareholding_requirement |  | CEO: 150,000 shares; Other ESC | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| comet-holding-ag-f1ab2b78 | role_disclosure | Current Executive Committee me | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| compagnie-financiere-tradition-sa-940d20ce | pension_type |  | defined contribution schemes;  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| curatis-holding-ag-adc33085 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| datwyler-holding-ag-eca04fdb | shares_outstanding |  | 34600000 | Fail (hard) | CORE-02: 34600000 not in the quote |
| datwyler-holding-ag-eca04fdb | sti_max | Executive Committee | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| deutsche-real-estate-ag-8625fa60 | largest_holders |  | Summit Real Estate Holdings Lt | Fail (hard) | NUM-07: holdings add up to 165.96% |
| deutsche-real-estate-ag-8625fa60 | other_names |  | Geestemünder Bank AG; Geestemü | Fail (hard) | CORE-02: not in the quote: bank |
| deutsche-real-estate-ag-8625fa60 | share_price |  | 10.7 | Fail (hard) | CORE-02: 10.7 not in the quote |
| dierig-holding-ag-91dc6032 | ebitda |  | 3400000 | Fail (hard) | CORE-02: 3.4 not in the quote |
| dierig-holding-ag-91dc6032 | fte |  | 107.7 | Fail (hard) | CORE-02: 107.7 not in the quote |
| dksh-holding-ag-6576340c | ultimate_parent |  | DKSH Holding Ltd. | Fail (hard) | CORE-02: not in the quote: dksh ltd |
| docmorris-ag-be190279 | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Präsident, exekutiv | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Mitglieder des Verwaltun | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | Total Gruppenleitung | CHF | Fail | CORE-04: no period_end |
| dottikon-es-holding-ag-d22b9c0d | pay_currency | CEO/Vorsitzender der Gruppenle | CHF | Fail | CORE-04: no period_end |
| dsm-firmenich-ag-62366aa6 | controlling_owner_name |  | Firmenich Family | Fail (hard) | CORE-02: not in the quote: family |
| dsm-firmenich-ag-62366aa6 | lti_max | CEO | 300 | Fail (hard) | CORE-03: quote not in the source text |
| dsm-firmenich-ag-62366aa6 | revenue_by_country |  | Switzerland: 214; Netherlands: | Fail | CORE-04: no period_end; NUM-08: adds up to 9,034,000,000 vs 12,521,000,000 (27.8% apart) |
| eisen-und-huettenwerke-5b76d547 | share_price |  | 15.5 | Fail (hard) | CORE-02: 15.5 not in the quote |
| eisen-und-huettenwerke-5b76d547 | sub_sector |  | Die Eisen- und Hüttenwerke AG  | Fail (hard) | CORE-03: quote not in the source text |
| emmi-ag-ad10f47a | pension_contribution | CEO | 204000 | Fail (hard) | CORE-02: 204 not in the quote |
| emmi-ag-ad10f47a | pension_contribution | Other members of Group Executi | 838000 | Fail (hard) | CORE-02: 838 not in the quote |
| enbw-energie-baden-wuerttemberg-30b5438b | revenue_by_country |  | Germany: 24310; European curre | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| epic-suisse-ag-7c2f8dc4 | benefits_value | Chief Executive Officer | 9000 | Fail (hard) | CORE-03: quote not in the source text |
| epic-suisse-ag-7c2f8dc4 | benefits_value | Group Executive Management | 15000 | Fail (hard) | CORE-03: quote not in the source text |
| epic-suisse-ag-7c2f8dc4 | role_disclosure | Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| epigenomics-ag-ddb6ea6d | total_remuneration | Vorstand (bis 30.April 2024) | -33000 | Fail (hard) | NUM-04: -33000 outside 0..5e+10; XF-01: parts add up to -32,468, more than the stated -33,000 |
| fair-value-reit-ag-cef1dc63 | exchange |  | Frankfurter Wertpapierbörse | Fail (hard) | COD-01: 'Frankfurter Wertpapierbörse' matches no ISO 10383 exchange |
| fair-value-reit-ag-cef1dc63 | fte |  | 2 | Fail (hard) | CORE-02: 2 not in the quote |
| fair-value-reit-ag-cef1dc63 | isin |  | DE000A0MW975 | Fail (hard) | CORE-03: quote not in the source text |
| helios-solar-ag-797724e7 | ebitda |  | -154.8 | Fail (hard) | CORE-02: -154.8 not in the quote |
| helios-solar-ag-797724e7 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| helios-solar-ag-797724e7 | total_assets |  | 50089.1 | Fail (hard) | CORE-03: quote not in the source text |
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
| path2-hydrogen-ag-4a522574 | benefits |  | mögliche Vereinbarungen über e | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| path2-hydrogen-ag-4a522574 | headcount |  | 1 | Fail (hard) | CORE-02: 1 not in the quote |
| pearl-gold-ag-da4e9b62 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| pearl-gold-ag-da4e9b62 | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| pfeiffer-vacuum-tech-ag-a38e65f0 | ebitda |  | 90600000 | Fail (hard) | CORE-02: 90.6 not in the quote |
| pfeiffer-vacuum-tech-ag-a38e65f0 | listing_date |  | 2023-12-29 | Fail (hard) | CORE-02: not in the quote: 2023 29 |
| pferdewetten-de-ag-07705286 | aggregate_headcount | Vorstand | 3 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| pittler-maschinenfabrik-ag-fb62b449 | benefits_value | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| pittler-maschinenfabrik-ag-fb62b449 | controlling_owner_name |  | Herr Günter Rothenberger | Fail (hard) | CORE-02: not in the quote: nter |
| pittler-maschinenfabrik-ag-fb62b449 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| pittler-maschinenfabrik-ag-fb62b449 | other_names |  | Leipziger Werkzeugmaschinenfab | Fail (hard) | CORE-03: quote not in the source text |
| pittler-maschinenfabrik-ag-fb62b449 | sti_paid | Alleinvorstand | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| planoptik-ag-9429909d | sti_target | Vorstandsmitglied | 10 | Fail (hard) | COD-01: unit '' is not a target form |
| readcrest-capital-ag-e4689651 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| readcrest-capital-ag-e4689651 | role_disclosure | CEO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| readcrest-capital-ag-e4689651 | role_disclosure | CFO (from 13. August 2025) | individual | Fail (hard) | CORE-03: quote not in the source text |
| readcrest-capital-ag-e4689651 | share_price |  | 1.34 | Fail (hard) | CORE-02: 1.34 not in the quote |
| sino-german-united-ag-388acb2d | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| sino-german-united-ag-388acb2d | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| sino-german-united-ag-388acb2d | role_disclosure | Vorstand/Chief Operating Offic | individual | Fail (hard) | CORE-03: quote not in the source text |
| softing-ag-365a9352 | share_price |  | 2.3 | Fail (hard) | CORE-03: quote not in the source text |
| stabilus-se-52dccb73 | listing_date |  | 2014-05 | Fail (hard) | COD-06: not a year or a date |
| stabilus-se-52dccb73 | revenue_by_country |  | Germany: 367128; Romania: 1322 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| stabilus-se-52dccb73 | revenue_by_segment |  | EMEA: 542183; Americas: 480899 | Fail (hard) | CORE-03: quote not in the source text |
| stabilus-se-52dccb73 | sub_sector |  | The object of the Company is t | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| suss-microtec-se-b7558a97 | controlling_owner |  | none | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | fte |  | 1497 | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | largest_holders |  | Janus Henderson 9.89%; Univers | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | ownership_type |  | widely_held | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| suss-microtec-se-b7558a97 | revenue_by_country |  | North America: 46; Asia / Paci | Fail (hard) | CORE-03: quote not in the source text |
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
| wasgau-produktions-handels-8c33a77d | lti_max | Sprecher des Vorstands (ab 01/ | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | lti_max | Vorstandsmitglied (ab 01/2025) | 2 | Fail (hard) | CORE-02: 2 not in the quote; COD-01: unit '' is not a target form |
| wasgau-produktions-handels-8c33a77d | revenue_by_segment |  | Großhandel: 170897; Einzelhand | Fail (hard) | CORE-03: quote not in the source text |
| wild-bunch-ag-7b9483b1 | revenue_by_segment |  | Internationaler Vertrieb und V | Fail (hard) | CORE-03: quote not in the source text |
| wild-bunch-ag-7b9483b1 | share_price |  | 31.2 | Fail (hard) | CORE-02: 31.2 not in the quote |
| wuestenrot-wuerttembergische-ag-07b9dfbc | revenue_by_segment |  | Housing: 1104; Life and health | Fail (hard) | CORE-03: quote not in the source text |
