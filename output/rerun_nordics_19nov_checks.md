# Output checks: rerun_nordics_19nov.csv

76 companies, 2265 filled values checked (2026-11-19, `python -m extractor.output_checks`). A check that doesn't apply is n/a and doesn't count; quotes are looked up again in the cached source documents.

| Status | Values |
|---|---|
| Pass | 2150 (95%) |
| Review | 56 (2%) |
| Fail | 5 (0%) |
| Fail (hard) | 54 (2%) |

## By category

| Category | Values | Pass | Review | Fail | Fail (hard) |
|---|---|---|---|---|---|
| Identity | 227 | 227 | 0 | 0 | 0 |
| Listing and market | 219 | 214 | 0 | 0 | 5 |
| Sector | 113 | 112 | 0 | 0 | 1 |
| Reporting basis | 159 | 159 | 0 | 0 | 0 |
| Financials | 212 | 198 | 10 | 1 | 3 |
| Workforce | 71 | 65 | 5 | 1 | 0 |
| Ownership and control | 194 | 192 | 0 | 0 | 2 |
| Segment and geography | 62 | 41 | 16 | 3 | 2 |
| Pay policy | 78 | 75 | 0 | 0 | 3 |
| Role and disclosure | 328 | 323 | 0 | 0 | 5 |
| Pay: fixed | 272 | 253 | 8 | 0 | 11 |
| Pay: STI | 155 | 144 | 1 | 0 | 10 |
| Pay: LTI | 65 | 59 | 2 | 0 | 4 |
| Pay: total | 110 | 88 | 14 | 0 | 8 |

## By check

| Check | What it checks | Hard | Ran | Pass | Fail | n/a | Most common failure |
|---|---|---|---|---|---|---|---|
| CORE-01 | Locator present (PDF links open at a page) | yes | 2265 | 2265 | 0 | 0 |  |
| CORE-02 | Value can be read off its quote | yes | 992 | 975 | 17 | 1273 | N not in the quote |
| CORE-03 | Quote is in the cached source, on the linked page | yes | 1660 | 1630 | 30 | 605 | quote not in the source text |
| CORE-04 | Period end present (dated fields only) |  | 1273 | 1257 | 16 | 992 | no period_end |
| CORE-05 | Type matches (number, date, breakdown) |  | 2265 | 2263 | 2 | 0 | period_end 'N-N' is not a date |
| COD-01 | Value in its code list or closed set | yes | 743 | 740 | 3 | 1522 | 'NASDAQ Copenhagen A/S' matches no ISO N exchange |
| COD-02 | Classification scheme named |  | 57 | 57 | 0 | 2208 |  |
| COD-03 | Identifier check digits (LEI, ISIN) | yes | 50 | 50 | 0 | 2215 |  |
| COD-06 | Dates are valid | yes | 69 | 69 | 0 | 2196 |  |
| NUM-01 | Money has an ISO 4217 currency | yes | 645 | 645 | 0 | 1620 |  |
| NUM-02 | Printed figure and unit recorded |  | 595 | 595 | 0 | 1670 |  |
| NUM-04 | Magnitude in a plausible range |  | 811 | 793 | 18 | 1454 | -Ne+N outside Ne+N |
| NUM-05 | Counts are whole numbers | yes | 131 | 131 | 0 | 2134 |  |
| NUM-06 | Percentages in range | yes | 112 | 112 | 0 | 2153 |  |
| NUM-07 | Holdings add up to 100% or less | yes | 32 | 32 | 0 | 2233 |  |
| NUM-08 | Breakdown adds up to the company total (5%) |  | 61 | 41 | 20 | 2204 | adds up to N vs N (N% apart) |
| NUM-09 | LTI says what it measures (granted, vested, expensed) |  | 46 | 46 | 0 | 2219 |  |
| NUM-11 | STI paid not above its maximum |  | 50 | 50 | 0 | 2215 |  |
| NUM-12 | A role's amounts share currency and period |  | 495 | 495 | 0 | 1770 |  |
| NUM-13 | FTE not above headcount |  | 31 | 30 | 1 | 2234 | FTE N above headcount N |
| DER-03 | Derived value recalculates | yes | 30 | 30 | 0 | 2235 |  |
| DER-06 | Derived value shows its formula |  | 156 | 156 | 0 | 2109 |  |
| XF-01 | Parts not above the stated total (2%) | yes | 95 | 88 | 7 | 2170 | parts add up to -N more than the stated -N |
| XF-02 | Total equals its parts (2%) |  | 95 | 77 | 18 | 2170 | parts add up to N stated N |

## Fill rate

Company fields: 1335 of 3116 filled (43%). Blank values are not checked above.

| Field | Filled | Of |
|---|---|---|
| cik | 4 | 76 |
| staff_by_segment | 4 | 76 |
| shareholding_requirement | 10 | 76 |
| staff_by_country | 15 | 76 |
| other_names | 18 | 76 |
| revenue_by_country | 20 | 76 |
| exchange_segment | 22 | 76 |
| lei | 23 | 76 |
| isin | 23 | 76 |
| revenue_by_segment | 23 | 76 |
| listing_date | 24 | 76 |
| ultimate_parent | 26 | 76 |
| controlling_owner_name | 29 | 76 |
| ticker | 31 | 76 |
| fte | 31 | 76 |
| pe_stake_5pct | 31 | 76 |
| largest_holders | 32 | 76 |
| ebitda | 33 | 76 |
| benefits | 33 | 76 |
| revenue | 34 | 76 |
| accounting_basis | 34 | 76 |
| business_id | 35 | 76 |
| pension_type | 35 | 76 |
| exchange | 36 | 76 |
| website | 36 | 76 |
| total_assets | 36 | 76 |
| reporting_currency | 36 | 76 |
| legal_name | 37 | 76 |
| country_code | 37 | 76 |
| head_office_city | 37 | 76 |
| listing_status | 38 | 76 |
| controlling_owner | 38 | 76 |
| ownership_type | 38 | 76 |
| headcount | 40 | 76 |
| fiscal_year | 44 | 76 |
| fiscal_year_end | 45 | 76 |
| market_cap_band | 45 | 76 |
| share_price | 47 | 76 |
| sub_sector | 56 | 76 |
| sector_code | 57 | 76 |
| shares_outstanding | 62 | 76 |

Pay fields, over 133 executive roles:

| Field | Filled |
|---|---|
| base_salary | 109 (82%) |
| sti_paid | 86 (65%) |
| sti_target | 2 (2%) |
| sti_max | 67 (50%) |
| lti_vested | 17 (13%) |
| lti_granted | 29 (22%) |
| lti_target | 8 (6%) |
| lti_max | 11 (8%) |
| benefits_value | 68 (51%) |
| pension_contribution | 92 (69%) |
| total_remuneration | 109 (82%) |

## Failed values (59)

| Company | Field | Role | Value | Status | Why |
|---|---|---|---|---|---|
| T0002 | total_remuneration | Executive Management | -24000000 | Fail (hard) | NUM-04: -2.4e+07 outside 0..5e+10; XF-01: parts add up to -24,000,000, more than the stated -24,000,000 |
| T0295 | share_price |  | 0.046 | Fail (hard) | CORE-02: 0.046 not in the quote |
| T0325 | shares_outstanding |  | 73790829 | Fail (hard) | CORE-03: quote not in the source text |
| T0377 | sub_sector |  | Global Workplace and facility  | Fail (hard) | CORE-03: quote not in the source text |
| bakkafrost | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| bakkafrost | sti_max | Managing Director | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| bakkafrost | sti_max | Chief Financial Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| bakkafrost | total_remuneration | Chief Executive Officer | 6895000 | Fail (hard) | CORE-02: 6895 not in the quote; XF-02: parts add up to 3,035,000, stated 6,895,000 |
| bakkafrost | total_remuneration | Managing Director | 2011000 | Fail (hard) | XF-01: parts add up to 2,128,000, more than the stated 2,011,000; XF-02: parts add up to 2,128,000, stated 2,011,000 |
| bakkafrost | total_remuneration | Chief Financial Officer | 2010000 | Fail (hard) | XF-01: parts add up to 2,217,000, more than the stated 2,010,000; XF-02: parts add up to 2,217,000, stated 2,010,000 |
| besqab-pref-b | controlling_owner_name |  | Family Nordström | Fail (hard) | CORE-02: not in the quote: family |
| cmb-tech-nv | benefits_value | Chief Chartering Officer | 0 | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-d | base_salary | Other senior executives | 8317000 | Fail (hard) | CORE-02: 8317 not in the quote |
| corem-property-pref | revenue_by_country |  | Sweden: 3244; Denmark: 59; Uni | Fail (hard) | CORE-03: quote not in the source text |
| corem-property-pref | sti_max | VD | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| digia-oyj | aggregate_headcount | Key Management | 15 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | benefits |  | fast lön, övriga förmåner, pen | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | isin |  | SE0016785786 | Fail (hard) | CORE-03: quote not in the source text |
| fastighetsbolag-emilshus-pref | pension_type |  | premiebaserad pensionslösning | Fail (hard) | CORE-03: quote not in the source text |
| fastpartner-d | sti_max | Chief Executive Officer | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_max | Other Executive Management Tea | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| fastpartner-d | sti_max | Other members of the Executive | 100 | Fail (hard) | CORE-02: 100 not in the quote |
| framery-group | role_disclosure | Other members of the Managemen | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| hermana-holding | fte |  | 0 | Fail | CORE-05: period_end '2025-04' is not a date; NUM-04: 0 outside 0.5..5e+06 |
| ilkka-2 | base_salary | Toimitusjohtaja | 278869 | Fail (hard) | CORE-03: quote not in the source text |
| ilkka-2 | lti_max | Toimitusjohtaja | 60 | Fail (hard) | CORE-03: quote not in the source text |
| ilkka-2 | lti_vested | Toimitusjohtaja | 8217 | Fail (hard) | CORE-03: quote not in the source text |
| ilkka-2 | sti_paid | Toimitusjohtaja | 25717 | Fail (hard) | CORE-03: quote not in the source text |
| ilkka-2 | total_remuneration | Toimitusjohtaja | 312803 | Fail (hard) | CORE-03: quote not in the source text; XF-01: parts add up to 354,586, more than the stated 312,803; XF-02: parts add up to 354,586, stated 312,803 |
| industrivarden-c | role_disclosure | CEO | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Deputy Chief Executive Officer | individual | Fail (hard) | CORE-03: quote not in the source text |
| industrivarden-c | role_disclosure | Other members of Executive Man | aggregate | Fail (hard) | CORE-03: quote not in the source text |
| intea-fastigheter-d | revenue_by_segment |  | Rättsväsende: 983; Högre utbil | Fail (hard) | CORE-03: quote not in the source text; NUM-08: adds up to 1,779,000,000 vs 1,561,000,000 (14.0% apart) |
| kesko-b | controlling_owner_name |  | K-kauppiasliitto ry | Fail (hard) | CORE-02: not in the quote: ry |
| melhus-sparebank | pension_type |  | Defined contribution for emplo | Fail (hard) | CORE-03: quote not in the source text |
| odfjell-technology | lti_target | CEO Odfjell Technology AS | 300000 | Fail (hard) | CORE-02: 300000 not in the quote; CORE-03: quote not in the source text |
| odfjell-technology | lti_target | CFO Odfjell Technology AS | 100000 | Fail (hard) | CORE-02: 100000 not in the quote; CORE-03: quote not in the source text |
| ostasiatiske | exchange |  | NASDAQ Copenhagen A/S | Fail (hard) | COD-01: 'NASDAQ Copenhagen A/S' matches no ISO 10383 exchange |
| paratus-energy | exchange |  | Euronext Oslo Børs | Fail (hard) | COD-01: 'Euronext Oslo Børs' matches no ISO 10383 exchange |
| petrolia | revenue |  | 2000000 | Fail (hard) | CORE-03: quote not in the source text |
| seb-c | revenue |  | -411000 | Fail | CORE-04: no period_end; NUM-04: -411000 outside 0..1e+14 |
| seb-c | revenue_by_country |  | Sweden: 46498; Norway: 4315; D | Fail | CORE-04: no period_end; NUM-08: adds up to 76,903,000,000 vs -411,000 (18711292.2% apart) |
| seb-c | revenue_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 76,928,000,000 vs -411,000 (18717374.9% apart) |
| seb-c | staff_by_segment |  | Corporate & Investment Banking | Fail | CORE-04: no period_end; NUM-08: adds up to 11,889 vs 189 (6190.5% apart) |
| seb-c | total_remuneration | VD samt vice VD | -8931000 | Fail (hard) | NUM-04: -8.931e+06 outside 0..5e+10; XF-01: parts add up to -8,931,000, more than the stated -8,931,000 |
| seb-c | total_remuneration | Risktagare | -24486000 | Fail (hard) | NUM-04: -2.4486e+07 outside 0..5e+10; XF-01: parts add up to -24,486,000, more than the stated -24,486,000 |
| seb-c | total_remuneration | Övriga | -157650000 | Fail (hard) | NUM-04: -1.5765e+08 outside 0..5e+10; XF-01: parts add up to -157,651,000, more than the stated -157,650,000 |
| sparebanken-more | base_salary | Leder av Divisjon Næringslivsm | 1561492 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | base_salary | Medlem av konsernledelsen (Joh | 2100597 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | benefits_value | Leder av Divisjon Næringslivsm | 440515 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | benefits_value | Medlem av konsernledelsen (Joh | 127783 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | pension_contribution | Leder av Divisjon Næringslivsm | 159764 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | pension_contribution | Medlem av konsernledelsen (Joh | 176028 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | sti_paid | Leder av Divisjon Næringslivsm | 469005 | Fail (hard) | CORE-03: quote not in the source text |
| sparebanken-more | sti_paid | Medlem av konsernledelsen (Joh | 30488 | Fail (hard) | CORE-03: quote not in the source text |
| stora-enso-a | benefits_value | Other members of the Group Lea | 250000 | Fail (hard) | CORE-02: 250 not in the quote |
| stora-enso-a | exchange |  | Nasdaq Helsinki;Nasdaq Stockho | Fail (hard) | CORE-02: not in the quote: nasdaq |
| stora-enso-a | pension_contribution | Other members of Group Leaders | 1445000 | Fail (hard) | CORE-02: 1445 not in the quote |
| tallink-grupp-5c02812d | exchange |  | Nasdaq Tallinn Stock Exchange | Fail (hard) | COD-01: 'Nasdaq Tallinn Stock Exchange' matches no ISO 10383 exchange |
