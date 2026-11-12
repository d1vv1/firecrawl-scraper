# Output checks: dach_set3_datapoints.csv

125 companies, 3581 filled values checked (2026-11-12, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 3164 (88%) |
| Review | 176 (5%) |
| Fail | 13 (0%) |
| Fail (hard) | 228 (6%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 123 | 123 | 0 | 0 | 0 |
| Listing and market | 97 | 95 | 0 | 0 | 2 |
| Sector | 36 | 35 | 0 | 0 | 1 |
| Reporting basis | 260 | 257 | 0 | 0 | 3 |
| Financials | 76 | 59 | 13 | 0 | 4 |
| Workforce | 29 | 21 | 4 | 0 | 4 |
| Ownership and control | 93 | 89 | 0 | 0 | 4 |
| Segment and geography | 25 | 10 | 7 | 2 | 6 |
| Pay policy | 263 | 241 | 0 | 0 | 22 |
| Role and disclosure | 776 | 729 | 3 | 11 | 33 |
| Pay: fixed | 675 | 598 | 24 | 0 | 53 |
| Pay: STI | 484 | 419 | 29 | 0 | 36 |
| Pay: LTI | 365 | 316 | 16 | 0 | 33 |
| Pay: total | 279 | 172 | 80 | 0 | 27 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 3581 | 3578 | 3 | 0 | no endpoint URL |
| CORE-02 | Value can be read off its quote | yes | 1876 | 1802 | 74 | 1705 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 2882 | 2741 | 141 | 699 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 2396 | 2288 | 108 | 1185 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 3581 | 3581 | 0 | 0 |  |
| COD-01 | Value in its code list or closed set | yes | 1211 | 1209 | 2 | 2370 | unit '' is not a target form |
| COD-02 | Classification scheme named |  | 18 | 18 | 0 | 3563 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 37 | 37 | 0 | 3544 |  |
| COD-06 | Dates are valid | yes | 125 | 123 | 2 | 3456 | not a valid date |
| NUM-01 | Money has an ISO 4217 currency | yes | 1471 | 1471 | 0 | 2110 |  |
| NUM-02 | Printed figure and unit recorded |  | 1464 | 1464 | 0 | 2117 |  |
| NUM-04 | Magnitude in a plausible range |  | 1617 | 1607 | 10 | 1964 | N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 134 | 131 | 3 | 3447 | not a whole number |
| NUM-06 | Percentages in range | yes | 307 | 307 | 0 | 3274 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 17 | 17 | 0 | 3564 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 23 | 18 | 5 | 3558 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 224 | 224 | 0 | 3357 |  |
| NUM-11 | STI paid not above its maximum |  | 107 | 95 | 12 | 3474 | paid N% of baseN maximum N% |
| NUM-12 | A role's amounts share currency and period |  | 1412 | 1410 | 2 | 2169 | currency USDN the role's other amounts CHF |
| NUM-13 | FTE not above headcount |  | 12 | 12 | 0 | 3569 |  |
| DER-03 | Derived value recalculates | yes | 2 | 2 | 0 | 3579 |  |
| DER-06 | Derived value shows its formula |  | 103 | 103 | 0 | 3478 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 254 | 243 | 11 | 3327 | parts add up to N more than the stated N |
| XF-02 | Total equals its parts (2%) |  | 254 | 162 | 92 | 3327 | parts add up to N stated N |

## Fill rate

Company fields: 1002 of 5125 filled (20%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 1 | 125 |
| staff_by_segment | 1 | 125 |
| exchange_segment | 6 | 125 |
| staff_by_country | 7 | 125 |
| listing_date | 8 | 125 |
| revenue_by_segment | 8 | 125 |
| revenue_by_country | 9 | 125 |
| share_price | 11 | 125 |
| market_cap_band | 11 | 125 |
| fte | 12 | 125 |
| controlling_owner_name | 13 | 125 |
| other_names | 15 | 125 |
| controlling_owner | 15 | 125 |
| ownership_type | 15 | 125 |
| revenue | 16 | 125 |
| total_assets | 16 | 125 |
| ebitda | 16 | 125 |
| accounting_basis | 16 | 125 |
| ultimate_parent | 16 | 125 |
| website | 17 | 125 |
| headcount | 17 | 125 |
| shares_outstanding | 17 | 125 |
| largest_holders | 17 | 125 |
| pe_stake_5pct | 17 | 125 |
| legal_name | 18 | 125 |
| lei | 18 | 125 |
| business_id | 18 | 125 |
| isin | 18 | 125 |
| ticker | 18 | 125 |
| exchange | 18 | 125 |
| listing_status | 18 | 125 |
| country_code | 18 | 125 |
| head_office_city | 18 | 125 |
| sector_code | 18 | 125 |
| sub_sector | 18 | 125 |
| reporting_currency | 18 | 125 |
| shareholding_requirement | 54 | 125 |
| pension_type | 103 | 125 |
| benefits | 106 | 125 |
| fiscal_year | 109 | 125 |
| fiscal_year_end | 117 | 125 |

Pay fields, over 294 executive roles:

| Field | Filled |
|---|---|
| base_salary | 266 (90%) |
| sti_paid | 238 (81%) |
| sti_target | 77 (26%) |
| sti_max | 169 (57%) |
| lti_vested | 32 (11%) |
| lti_granted | 192 (65%) |
| lti_target | 52 (18%) |
| lti_max | 89 (30%) |
| benefits_value | 184 (63%) |
| pension_contribution | 225 (77%) |
| total_remuneration | 279 (95%) |

## Failed values (241)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| evonext-holdings-sa-be1893c4 | aggregate_headcount | Other members of Group Managem | 2 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | base_salary | CEO | 250000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | base_salary | Other members of Group Managem | 300000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | ebitda |  | -16700000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | fiscal_year_end |  | 12-31 | Fail (hard) | COD-06: not a valid date |
| evonext-holdings-sa-be1893c4 | lti_granted | CEO | 237500 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | lti_granted | Other members of Group Managem | 285000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | pay_currency | CEO | CHF | Fail | CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | pay_currency | Other members of Group Managem | CHF | Fail | CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| evonext-holdings-sa-be1893c4 | role_disclosure | Other members of Group Managem | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| evonext-holdings-sa-be1893c4 | total_remuneration | CEO | 487500 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| evonext-holdings-sa-be1893c4 | total_remuneration | Other members of Group Managem | 585000 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| galderma-group-ag-8c1dbf8c | shareholding_requirement |  | CEO: 300% of annual base salar | Fail (hard) | CORE-03: quote not in the source text |
| gam-holding-ag-6ce711d2 | benefits_value | Group Management Board | 822133 | Fail (hard) | CORE-02: 822133 not in the quote; CORE-03: quote not in the source text |
| gam-holding-ag-6ce711d2 | pension_type |  | defined contribution and defin | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| gam-holding-ag-6ce711d2 | role_disclosure | Group Management Board (aggreg | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| givaudan-sa-b9d48cbe | benefits_value | EC Members | 645192 | Fail (hard) | CORE-03: quote not in the source text |
| givaudan-sa-b9d48cbe | pension_contribution | EC Members | 1245193 | Fail (hard) | CORE-03: quote not in the source text |
| givaudan-sa-b9d48cbe | total_remuneration | EC Members | 14749265 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | base_salary | Group CEO (Michael Müller) | 788300 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | benefits_value | Group CEO (Michael Müller) | 6300 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | ebitda |  | 824200000 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | lti_granted | Group CEO (Michael Müller) | 473000 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | pension_contribution | Group CEO (Michael Müller) | 193800 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | role_disclosure | Group CEO (Fabian Ruprecht) | individual | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | role_disclosure | Group Executive Board | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | staff_by_country |  | Switzerland: 9165; Germany: 23 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| helvetia-baloise-holding-ag-784ff8e8 | sti_paid | Group CEO (Michael Müller) | 357600 | Fail (hard) | CORE-03: quote not in the source text |
| helvetia-baloise-holding-ag-784ff8e8 | total_remuneration | Group CEO (Michael Müller) | 1819100 | Fail (hard) | CORE-03: quote not in the source text |
| hiag-immobilien-holding-ag-3a28978d | sti_max | CEO | 300000 | Fail (hard) | CORE-03: quote not in the source text |
| hiag-immobilien-holding-ag-3a28978d | sti_max | Other members of the Executive | 220000 | Fail (hard) | CORE-03: quote not in the source text |
| holcim-ltd-b2e462f1 | ebitda |  | 3992000000 | Fail (hard) | CORE-03: quote not in the source text |
| holcim-ltd-b2e462f1 | largest_holders |  | UBS Fund Management (Switzerla | Fail (hard) | CORE-03: quote not in the source text |
| holcim-ltd-b2e462f1 | lti_granted | Other members | 4275934 | Fail (hard) | CORE-02: 4275934 not in the quote |
| holcim-ltd-b2e462f1 | pe_stake_5pct |  | no | Fail (hard) | CORE-03: quote not in the source text |
| holcim-ltd-b2e462f1 | revenue_by_segment |  | Europe: 8548; Latin America: 3 | Fail (hard) | CORE-03: quote not in the source text |
| huber-suhner-ag-11887265 | lti_max | CEO | 150 | Fail (hard) | CORE-02: 150 not in the quote |
| huber-suhner-ag-11887265 | role_disclosure | CEO | individual | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| huber-suhner-ag-11887265 | staff_by_country |  | Switzerland: 1099; Poland: 970 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| inficon-holding-ag-4220ed6f | base_salary | Other members of Group Managem | 365000 | Fail (hard) | CORE-02: 365 not in the quote |
| inficon-holding-ag-4220ed6f | benefits_value | President and Chief Executive  | 244000 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| inficon-holding-ag-4220ed6f | benefits_value | Total Group Management | 435000 | Fail (hard) | CORE-02: 435 not in the quote |
| inficon-holding-ag-4220ed6f | benefits_value | Other members of Group Managem | 172000 | Fail (hard) | CORE-02: 172 not in the quote |
| inficon-holding-ag-4220ed6f | lti_granted | Other members of Group Managem | 125000 | Fail (hard) | CORE-02: 125 not in the quote |
| inficon-holding-ag-4220ed6f | pension_contribution | Other members of Group Managem | 19000 | Fail (hard) | CORE-02: 19 not in the quote |
| inficon-holding-ag-4220ed6f | sti_paid | Other members of Group Managem | 95000 | Fail (hard) | CORE-02: 95 not in the quote |
| inficon-holding-ag-4220ed6f | total_remuneration | Other members of Group Managem | 776000 | Fail (hard) | CORE-02: 776 not in the quote |
| infomaniak-sa-87b05313 | controlling_owner_name |  | Infomaniak Foundation | Fail (hard) | CORE-02: not in the quote: infomaniak |
| infomaniak-sa-87b05313 | sti_max | Executive Chairman | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sti_max | Group Management | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sti_max | CEO | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| infomaniak-sa-87b05313 | sub_sector |  | Swiss provider of sovereign cl | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| infracore-sa-b3b0dcce | controlling_owner_name |  | Medical Properties Trust, Inc. | Fail (hard) | CORE-02: not in the quote: medical properties trust |
| infracore-sa-b3b0dcce | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| infracore-sa-b3b0dcce | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| interroll-holding-ag-ef2328b8 | sti_paid | CEO (03 - 12) | 417000 | Fail (hard) | CORE-02: 417 not in the quote |
| interroll-holding-ag-ef2328b8 | sti_paid | Other members of Group Managem | 493000 | Fail (hard) | CORE-02: 493 not in the quote |
| intershop-holding-ag-6e9d3cef | benefits |  | benefits in kind | Fail (hard) | CORE-03: quote not in the source text |
| intershop-holding-ag-6e9d3cef | sti_paid | Executive Board | 635000 | Fail (hard) | CORE-02: 635 not in the quote |
| julius-bar-gruppe-ag-de864d89 | lti_granted | Executive Board (excl. CEO) | 8100000 | Fail (hard) | CORE-02: 8.1 not in the quote |
| julius-bar-gruppe-ag-de864d89 | pension_contribution | CEO | 620000 | Fail (hard) | CORE-03: quote not in the source text |
| julius-bar-gruppe-ag-de864d89 | role_disclosure | Executive Board (1) | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| julius-bar-gruppe-ag-de864d89 | staff_by_country |  | United States: 1138; China: 40 | Fail | CORE-04: no period_end; NUM-08: adds up to 1,258 vs 7,390 (83.0% apart) |
| julius-bar-gruppe-ag-de864d89 | sti_paid | Executive Board (1) | 4074000 | Fail (hard) | CORE-03: quote not in the source text |
| julius-bar-gruppe-ag-de864d89 | sti_paid | Executive Board (2) | 4713000 | Fail (hard) | CORE-03: quote not in the source text |
| julius-bar-gruppe-ag-de864d89 | total_remuneration | CEO | 8271000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 3,343,000, stated 8,271,000 |
| jungfraubahn-holding-ag-90ceddd3 | aggregate_headcount | Executive Board | 3 | Fail (hard) | CORE-03: quote not in the source text; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Chairman of the Executive Boar | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | pay_currency | Executive Board | CHF | Fail | CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Chairman of the Executive Boar | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| jungfraubahn-holding-ag-90ceddd3 | sti_max | Executive Board | 66.67 | Fail (hard) | CORE-02: 66.67 not in the quote; CORE-04: no period_end |
| klingelnberg-ag-d32e6349 | benefits_value | Executive Management | 70334.18 | Fail (hard) | CORE-03: quote not in the source text |
| klingelnberg-ag-d32e6349 | benefits_value | CEO | 29343.67 | Fail (hard) | CORE-03: quote not in the source text |
| klingelnberg-ag-d32e6349 | lti_granted | Executive Management | 510000 | Fail (hard) | CORE-03: quote not in the source text |
| klingelnberg-ag-d32e6349 | lti_granted | CEO | 170000 | Fail (hard) | CORE-03: quote not in the source text |
| klingelnberg-ag-d32e6349 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| kuhne-nagel-international-ag-2949951f | benefits |  | Pension and insurance benefits | Fail (hard) | CORE-03: quote not in the source text |
| kuhne-nagel-international-ag-2949951f | benefits_value | Chief Executive Officer | 32000 | Fail (hard) | CORE-03: quote not in the source text |
| kuhne-nagel-international-ag-2949951f | lti_granted | Chief Executive Officer | 356000 | Fail (hard) | CORE-03: quote not in the source text |
| kuhne-nagel-international-ag-2949951f | pension_contribution | Chief Executive Officer | 117000 | Fail (hard) | CORE-03: quote not in the source text |
| kuhne-nagel-international-ag-2949951f | revenue_by_segment |  | Sea Logistics: 8817; Air Logis | Fail (hard) | CORE-03: quote not in the source text |
| kuhne-nagel-international-ag-2949951f | total_remuneration | Chief Executive Officer | 3159000 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 3,004,000, stated 3,159,000 |
| kuros-biosciences-ltd-32d9b34e | lti_granted | CEO | 3185300 | Fail (hard) | CORE-02: 3185.3 not in the quote |
| kuros-biosciences-ltd-32d9b34e | lti_granted | Other EC Members | 2021600 | Fail (hard) | CORE-02: 2021.6 not in the quote |
| kuros-biosciences-ltd-32d9b34e | total_remuneration | CEO | 3909900 | Fail (hard) | XF-01: parts add up to 4,055,500, more than the stated 3,909,900; XF-02: parts add up to 4,055,500, stated 3,909,900 |
| kuros-biosciences-ltd-32d9b34e | total_remuneration | Other EC Members | 3330400 | Fail (hard) | XF-01: parts add up to 3,545,300, more than the stated 3,330,400; XF-02: parts add up to 3,545,300, stated 3,330,400 |
| lem-holding-sa-cc5005fc | role_disclosure | Board of Directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| leonteq-ag-6723ca54 | benefits |  | representation and lunch allow | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| logitech-international-s-a-0a74f2ba | pension_type |  | defined benefit pension plans  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| logitech-international-s-a-0a74f2ba | total_remuneration | Chief Executive Officer | 8757096 | Fail (hard) | XF-01: parts add up to 9,228,576, more than the stated 8,757,096; XF-02: parts add up to 9,228,576, stated 8,757,096 |
| lonza-group-ag-e4f248d2 | accounting_basis |  | IFRS Accounting Standards | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| lonza-group-ag-e4f248d2 | aggregate_headcount | Executive Committee | 8.8 | Fail (hard) | NUM-05: not a whole number |
| lonza-group-ag-e4f248d2 | base_salary | Executive Committee | 5390000 | Fail (hard) | CORE-03: quote not in the source text |
| lonza-group-ag-e4f248d2 | benefits_value | CEO | 350000 | Fail (hard) | CORE-03: quote not in the source text |
| lonza-group-ag-e4f248d2 | benefits_value | Executive Committee | 1990000 | Fail (hard) | CORE-03: quote not in the source text |
| mch-group-ag-c6fc7898 | listing_date |  | 2001 | Fail (hard) | CORE-02: not in the quote: 2001 |
| medartis-holding-ag-4ef02932 | shareholding_requirement |  | BoD: shares equal to one year  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| medartis-holding-ag-4ef02932 | sti_max | Other members of the EMB | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| meier-tobler-group-ag-f96a3151 | benefits |  | Geschäftsfahrzeug | Fail (hard) | CORE-03: quote not in the source text |
| mindmaze-therapeutics-holding-sa-b2339575 | exchange_segment |  | MTF | Fail (hard) | CORE-02: not in the quote: mtf |
| mindmaze-therapeutics-holding-sa-b2339575 | sti_paid | Chief Business Officer | 0 | Fail (hard) | CORE-02: 0 not in the quote |
| mobilezone-holding-ag-fc013b59 | aggregate_headcount | Management Board | 5 | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | benefits |  | lump-sum expenses approved by  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| mobilezone-holding-ag-fc013b59 | role_disclosure | Executive Delegate of the Boar | individual | Fail (hard) | CORE-03: quote not in the source text |
| mobilezone-holding-ag-fc013b59 | sti_max | Management Board | 200 | Fail (hard) | CORE-03: quote not in the source text |
| mobilezone-holding-ag-fc013b59 | sti_max | Executive Delegate of the Boar | 200 | Fail (hard) | CORE-03: quote not in the source text |
| molecular-partners-ag-86d659ae | pension_type |  | defined benefit plans; compuls | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| naturenergie-holding-ag-a1be2274 | pension_contribution | Geschäftsleitung | 156656 | Fail (hard) | CORE-02: 156656 not in the quote |
| orior-ag-bfeb91d6 | aggregate_headcount | Executive Committee excl. CFO | 3.1 | Fail (hard) | NUM-05: not a whole number |
| orior-ag-bfeb91d6 | aggregate_headcount | Former Executive Committee mem | 0.4 | Fail (hard) | NUM-04: 0.4 outside 1..500; NUM-05: not a whole number |
| partners-group-holding-ag-d09fd15d | lti_granted | Chief Executive Officer | 14055000 | Fail (hard) | CORE-02: 14055 not in the quote |
| partners-group-holding-ag-d09fd15d | lti_granted | Executive Team | 54733000 | Fail (hard) | CORE-02: 54733 not in the quote |
| partners-group-holding-ag-d09fd15d | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| phoenix-mecano-ag-d882ab5c | base_salary | Management | 1934000 | Fail (hard) | CORE-02: 1934 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | Chairman of the Board of Direc | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| phoenix-mecano-ag-d882ab5c | sti_max | CEO | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| plazza-ag-a1578cf1 | pension_contribution | CEO/CFO | 72700 | Fail (hard) | CORE-02: 72.7 not in the quote |
| roche-holding-ag-5abd8231 | benefits_value | Other members of the Corporate | 120000 | Fail (hard) | CORE-03: quote not in the source text |
| roche-holding-ag-5abd8231 | lti_granted | CEO Roche Group | 2788169 | Fail (hard) | CORE-03: quote not in the source text |
| roche-holding-ag-5abd8231 | lti_granted | Other members of the Corporate | 10000000 | Fail (hard) | CORE-03: quote not in the source text |
| roche-holding-ag-5abd8231 | pension_contribution | Other members of the Corporate | 1597894 | Fail (hard) | CORE-03: quote not in the source text |
| roche-holding-ag-5abd8231 | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| roche-holding-ag-5abd8231 | shareholding_requirement |  | CEO Roche Group: Shares and/or | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | fiscal_year_end |  | YYYY-12-31 | Fail (hard) | COD-06: not a valid date |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | pay_currency | Executive Management | CHF | Fail | CORE-04: no period_end |
| santhera-pharmaceuticals-holding-ag-8f83ccd5 | revenue_by_country |  | Europe: 11577; North America:  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start); CORE-04: no period_end |
| schindler-holding-ag-d2b61912 | base_salary | Nonexecutive member with opera | 242000 | Fail (hard) | CORE-02: 242 not in the quote; CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | base_salary | Member of the Supervisory and  | 820000 | Fail (hard) | CORE-02: 820 not in the quote; CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | base_salary | Member of the Supervisory and  | 895000 | Fail (hard) | CORE-02: 895 not in the quote |
| schindler-holding-ag-d2b61912 | base_salary | Executive member with operatio | 665000 | Fail (hard) | CORE-02: 665 not in the quote; CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | benefits_value | Member of the Supervisory and  | 87000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | benefits_value | Executive member with operatio | 38000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | lti_granted | Member of the Supervisory and  | 907000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | lti_granted | Executive member with operatio | 349000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | lti_max | CEO | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| schindler-holding-ag-d2b61912 | lti_max | Group Executive Committee | 300 | Fail (hard) | CORE-02: 300 not in the quote |
| schindler-holding-ag-d2b61912 | pension_contribution | Nonexecutive member with opera | 20000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | pension_contribution | Member of the Supervisory and  | 207000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | pension_contribution | Executive member with operatio | 177000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | role_disclosure | Nonexecutive member with opera | individual | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | role_disclosure | Member of the Supervisory and  | individual | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | role_disclosure | Member of the Supervisory and  | individual | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | role_disclosure | Executive member with operatio | individual | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | sti_paid | Member of the Supervisory and  | 726000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | sti_paid | Executive member with operatio | 370000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | total_remuneration | Chairman (as of the General Me | 1826000 | Fail (hard) | XF-01: parts add up to 1,903,000, more than the stated 1,826,000; XF-02: parts add up to 1,903,000, stated 1,826,000 |
| schindler-holding-ag-d2b61912 | total_remuneration | former Chairman (until the Gen | 990000 | Fail (hard) | XF-01: parts add up to 1,087,000, more than the stated 990,000; XF-02: parts add up to 1,087,000, stated 990,000 |
| schindler-holding-ag-d2b61912 | total_remuneration | Nonexecutive member with opera | 262000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | total_remuneration | Member of the Supervisory and  | 2747000 | Fail (hard) | CORE-03: quote not in the source text |
| schindler-holding-ag-d2b61912 | total_remuneration | Executive member with operatio | 1599000 | Fail (hard) | CORE-03: quote not in the source text |
| schlatter-industries-ag-e8b6df3d | pension_contribution | Group Management | 219016 | Fail (hard) | CORE-02: 219016 not in the quote |
| schweiter-technologies-ag-b9dd7eca | aggregate_headcount | Group Management | 2 | Fail (hard) | CORE-03: quote not in the source text |
| schweiter-technologies-ag-b9dd7eca | base_salary | Group Management | 987000 | Fail (hard) | CORE-02: 987000 not in the quote |
| schweiter-technologies-ag-b9dd7eca | base_salary | CEO | 650000 | Fail (hard) | CORE-02: 650000 not in the quote |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | Group Management | 232000 | Fail (hard) | CORE-02: 232000 not in the quote; CORE-03: quote not in the source text |
| schweiter-technologies-ag-b9dd7eca | pension_contribution | CEO | 143000 | Fail (hard) | CORE-02: 143000 not in the quote; CORE-03: quote not in the source text |
| schweiter-technologies-ag-b9dd7eca | shareholding_requirement |  | Share-based compensation for B | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| schweiter-technologies-ag-b9dd7eca | sti_paid | Group Management | 126000 | Fail (hard) | CORE-02: 126000 not in the quote |
| schweiter-technologies-ag-b9dd7eca | sti_paid | CEO | 76000 | Fail (hard) | CORE-02: 76000 not in the quote |
| schweiter-technologies-ag-b9dd7eca | total_remuneration | CEO | 869000 | Fail (hard) | CORE-02: 869000 not in the quote |
| sensirion-holding-ag-0c2fb93b | aggregate_headcount | Total EC | 6 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | base_salary | CEO | 444184 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | base_salary | Other EC | 1213918 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | base_salary | Total EC | 1658102 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | role_disclosure | Other EC | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | role_disclosure | Total EC | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | sti_paid | CEO | 102168 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | sti_paid | Other EC | 252170 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | sti_paid | Total EC | 354339 | Fail (hard) | CORE-03: quote not in the source text |
| sensirion-holding-ag-0c2fb93b | total_remuneration | CEO | 628853 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 546,352, stated 628,853 |
| sensirion-holding-ag-0c2fb93b | total_remuneration | Other EC | 1686136 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 1,466,088, stated 1,686,136 |
| sensirion-holding-ag-0c2fb93b | total_remuneration | Total EC | 2314989 | Fail (hard) | CORE-03: quote not in the source text; XF-02: parts add up to 2,012,441, stated 2,314,989 |
| sgs-ag-65380806 | aggregate_headcount | Other ExCo | 13 | Fail (hard) | CORE-03: quote not in the source text |
| sgs-ag-65380806 | benefits_value | Chief Executive Officer | 24000 | Fail (hard) | CORE-03: quote not in the source text |
| sgs-ag-65380806 | pension_contribution | Chief Executive Officer | 119000 | Fail (hard) | CORE-03: quote not in the source text |
| sgs-ag-65380806 | revenue_by_country |  | North America: 1.5 | Fail | CORE-04: no period_end |
| sgs-ag-65380806 | total_remuneration | Chief Executive Officer | 1393000 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 4,355,000, more than the stated 1,393,000; XF-02: parts add up to 4,355,000, stated 1,393,000 |
| skan-group-ag-684bb9fa | sti_paid | CEO | 0 | Fail (hard) | CORE-03: quote not in the source text |
| smg-swiss-marketplace-group-holding-ag-40385dff | revenue_by_segment |  | Real Estate: 164147; Automotiv | Fail (hard) | CORE-03: quote not in the source text |
| softwareone-holding-ag-ee2860ae | lti_granted | CFO (until May 31, 2025) | 0 | Fail (hard) | CORE-03: quote not in the source text |
| softwareone-holding-ag-ee2860ae | lti_granted | Other EB members | 1320250 | Fail (hard) | CORE-03: quote not in the source text |
| softwareone-holding-ag-ee2860ae | lti_target | Other EB members | 27 | Fail (hard) | COD-01: unit '' is not a target form |
| softwareone-holding-ag-ee2860ae | sti_target | Other EB members | 22 | Fail (hard) | COD-01: unit '' is not a target form |
| sonova-holding-ag-e87e288d | pension_type |  | Sonova Group has both defined  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| st-galler-kantonalbank-ag-ba864955 | lti_granted | Übrige vier Mitglieder der Ges | 833000 | Fail (hard) | CORE-02: 833 not in the quote |
| st-galler-kantonalbank-ag-ba864955 | shareholding_requirement |  | For Board of Directors: 30% of | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| starragtornos-group-ag-15e3832b | base_salary | Other members of the Executive | 637000 | Fail (hard) | CORE-02: 637 not in the quote |
| starragtornos-group-ag-15e3832b | benefits_value | Other members of the Executive | 26000 | Fail (hard) | CORE-02: 26 not in the quote |
| starragtornos-group-ag-15e3832b | pension_contribution | Other members of the Executive | 130000 | Fail (hard) | CORE-02: 130 not in the quote |
| starragtornos-group-ag-15e3832b | sti_paid | Other members of the Executive | 7000 | Fail (hard) | CORE-02: 7 not in the quote |
| starragtornos-group-ag-15e3832b | total_remuneration | Other members of the Executive | 799000 | Fail (hard) | CORE-02: 799 not in the quote |
| straumann-holding-ag-d8e91d7f | lti_vested | CEO | 180000 | Fail (hard) | CORE-02: 180 not in the quote |
| swiss-re-ag-6528d850 | benefits_value | Group Chief Executive Officer | 27000 | Fail (hard) | CORE-03: quote not in the source text |
| swiss-re-ag-6528d850 | lti_vested | Group Chief Executive Officer | 3394000 | Fail (hard) | CORE-02: 3394 not in the quote; CORE-03: quote not in the source text |
| swiss-re-ag-6528d850 | sti_max | Group Chief Executive Officer | 200 | Fail (hard) | CORE-02: 200 not in the quote |
| swiss-re-ag-6528d850 | total_remuneration | Group Chief Executive Officer | 6065000 | Fail (hard) | XF-01: parts add up to 6,292,000, more than the stated 6,065,000; XF-02: parts add up to 6,292,000, stated 6,065,000 |
| temenos-ag-21209ec1 | shareholding_requirement |  | CEO: 5 times annual fixed sala | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| the-swatch-group-ag-6a144b9f | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-01: no endpoint URL |
| thurgauer-kantonalbank-3b36a058 | benefits |  | For Bank Council members: occa | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| thurgauer-kantonalbank-3b36a058 | pension_type |  | defined contribution. For fixe | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| tx-group-ag-cdcf98d0 | role_disclosure | Executive Management | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| ubs-group-ag-944a2b19 | sti_max | Group Executive Board | 7 | Fail (hard) | CORE-02: 7 not in the quote |
| varia-us-properties-ag-9f548364 | fte |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 0.5..5e+06 |
| varia-us-properties-ag-9f548364 | headcount |  | 0 | Fail (hard) | CORE-02: 0 not in the quote; NUM-04: 0 outside 1..5e+06 |
| vat-group-ag-ccdd96de | pay_currency | CEO (since January 1, 2024) | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pay_currency | Other GEC | CHF | Fail | CORE-04: no period_end |
| vat-group-ag-ccdd96de | pension_type |  | occupational pension plans, in | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Administratrice (Membre non ex | individual | Fail (hard) | CORE-03: quote not in the source text |
| villars-holding-s-a-0f65ebf6 | role_disclosure | Ancien Président | individual | Fail (hard) | CORE-03: quote not in the source text |
| vontobel-holding-ag-1d88ea32 | lti_granted | Co-CEO (Georg Schubiger) | 2571200 | Fail (hard) | CORE-02: 2571.2 not in the quote |
| vontobel-holding-ag-1d88ea32 | lti_granted | Co-CEO (Dr. Christel Rendu de  | 2571200 | Fail (hard) | CORE-02: 2571.2 not in the quote |
| vontobel-holding-ag-1d88ea32 | lti_vested | Executive Committee | 7400000 | Fail (hard) | CORE-03: quote not in the source text |
| vontobel-holding-ag-1d88ea32 | pension_contribution | Executive Committee | 700000 | Fail (hard) | CORE-03: quote not in the source text |
| vontobel-holding-ag-1d88ea32 | sti_paid | Executive Committee | 3000000 | Fail (hard) | CORE-03: quote not in the source text |
| vontobel-holding-ag-1d88ea32 | total_remuneration | Executive Committee | 15000000 | Fail (hard) | CORE-03: quote not in the source text |
| vp-bank-ag-e661c993 | lti_granted | Group Executive Management | 1284000 | Fail (hard) | CORE-02: 1284 not in the quote |
| vp-bank-ag-e661c993 | lti_granted | Chief Executive Officer (CEO) | 480000 | Fail (hard) | CORE-02: 480 not in the quote |
| ypsomed-holding-ag-9cb8acfe | benefits |  | Dienstaltersgeschenk | Fail (hard) | CORE-03: quote not in the source text |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Chief Executive Officer (CEO) | 130400 | Fail (hard) | CORE-02: 130.4 not in the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Other members of group managem | 479800 | Fail (hard) | CORE-02: 479.8 not in the quote |
| ypsomed-holding-ag-9cb8acfe | pension_contribution | Total Executive Management | 610200 | Fail (hard) | CORE-02: 610.2 not in the quote |
| zehnder-group-ag-125a701c | pension_type |  | For members of the Group Execu | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zehnder-group-ag-125a701c | role_disclosure | Board of directors (non-execut | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| zublin-immobilien-holding-ag-cf81b4e5 | benefits |  | Sozialversicherungs-Beiträge,  | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (ab 15. September 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pay_currency | CEO/CFO (bis 31. Dezember 2024 | CHF | Fail | CORE-04: no period_end |
| zublin-immobilien-holding-ag-cf81b4e5 | pension_type |  | leistungsorientierter Pensions | Fail (hard) | CORE-03: the run did not find the full quote (the note keeps only its start) |
| zublin-immobilien-holding-ag-cf81b4e5 | shares_outstanding |  | 3318027 | Fail (hard) | CORE-03: quote not in the source text |
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
