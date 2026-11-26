# What the run could not find: fy2025_runs_datapoints.csv

18470 missing values in 1486 of 1510 companies (built 26 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REPORT_NOT_FOUND` | Annual report not found | 564 | 34 | Put the FY annual report link (PDF, or a gs:// file) in `annual_report_url` and re-run |
| `REMUNERATION_REPORT_NOT_FOUND` | Remuneration report not found | 28 | 28 | Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay |
| `NO_IDENTIFIER` | Needs an LEI or register number | 20 | 20 | Add `lei` or `business_id` to the input: only an official register gives this field |
| `WRONG_YEAR_REPORT` | Values read from an older report | 81 | 81 | Put the FY report link in `annual_report_url` and re-run with --redo |
| `CREDITS_EXHAUSTED` | Firecrawl credits ran out | 1 | 1 | Top up credits (or raise --max-run-credits / --doc-credits) and re-run |
| `DOCUMENT_UNREADABLE` | Document could not be read | 32 | 4 | Scanned or broken file: supply a text PDF, or check the download |
| `NETWORK_ERROR` | Network or site error | 104 | 9 | Re-run; if it repeats, supply the document link |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 459 | 450 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `FX_RATE_MISSING` | Calculated field: no exchange rate | 1 | 1 | Re-run the field (the API step gives the ECB rate), or fix the currency unit |
| `STATED_IN_OTHER_FORM` | Stated, but not in the form asked for | 50 | 25 | Accept or review: e.g. a % of salary where an amount is asked |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 7264 | 813 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 9865 | 1142 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 7203 | 1427 | - |
| `NOT_COLLECTED` | Not asked for in this run | 17908 | 828 | - |
| `UNKNOWN` | No reason recorded | 1 | 1 | Check the company's log in output/ |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| lti_target | 1922 | REMUNERATION_REPORT_NOT_READ 1230, NOT_DISCLOSED 692 |
| sti_target | 1882 | REMUNERATION_REPORT_NOT_READ 1135, NOT_DISCLOSED 747 |
| lti_vested | 1735 | REMUNERATION_REPORT_NOT_READ 934, NOT_DISCLOSED 799, STATED_IN_OTHER_FORM 2 |
| lti_granted | 1620 | REMUNERATION_REPORT_NOT_READ 945, NOT_DISCLOSED 627, STATED_IN_OTHER_FORM 48 |
| lti_max | 1422 | REMUNERATION_REPORT_NOT_READ 774, NOT_DISCLOSED 648 |
| sti_max | 1022 | REMUNERATION_REPORT_NOT_READ 556, NOT_DISCLOSED 466 |
| staff_by_segment | 769 | NOT_DISCLOSED 737, REPORT_NOT_FOUND 23, NETWORK_ERROR 8 |
| sti_paid | 670 | REMUNERATION_REPORT_NOT_READ 377, NOT_DISCLOSED 293 |
| pension_contribution | 580 | NOT_DISCLOSED 308, REMUNERATION_REPORT_NOT_READ 272 |
| staff_by_country | 549 | NOT_DISCLOSED 519, REPORT_NOT_FOUND 21, NETWORK_ERROR 8 |
| benefits_value | 516 | REMUNERATION_REPORT_NOT_READ 309, NOT_DISCLOSED 207 |
| market_cap_band | 445 | DERIVATION_INPUT_MISSING 444, FX_RATE_MISSING 1 |
| other_names | 437 | NOT_DISCLOSED 419, REPORT_NOT_FOUND 14, NETWORK_ERROR 4 |
| share_price | 426 | NOT_DISCLOSED 399, REPORT_NOT_FOUND 22, NETWORK_ERROR 4 |
| revenue_by_country | 403 | NOT_DISCLOSED 371, REPORT_NOT_FOUND 24, NETWORK_ERROR 7 |
| base_salary | 358 | REMUNERATION_REPORT_NOT_READ 195, NOT_DISCLOSED 163 |
| exchange_segment | 339 | NOT_DISCLOSED 318, REPORT_NOT_FOUND 19, NETWORK_ERROR 2 |
| revenue_by_segment | 328 | NOT_DISCLOSED 296, REPORT_NOT_FOUND 23, NETWORK_ERROR 8 |
| fte | 326 | NOT_DISCLOSED 297, REPORT_NOT_FOUND 23, NETWORK_ERROR 5 |
| total_remuneration | 258 | REMUNERATION_REPORT_NOT_READ 155, NOT_DISCLOSED 103 |
| shareholding_requirement | 226 | REMUNERATION_REPORT_NOT_READ 128, NOT_DISCLOSED 74, REPORT_NOT_FOUND 18 |
| listing_date | 214 | NOT_DISCLOSED 200, REPORT_NOT_FOUND 10, NETWORK_ERROR 4 |
| ticker | 180 | NOT_DISCLOSED 170, REPORT_NOT_FOUND 8, NETWORK_ERROR 2 |
| aggregate_headcount | 166 | REMUNERATION_REPORT_NOT_READ 113, NOT_DISCLOSED 53 |
| pe_stake_5pct | 140 | NOT_DISCLOSED 121, REPORT_NOT_FOUND 17, NETWORK_ERROR 2 |
| benefits | 137 | REMUNERATION_REPORT_NOT_READ 70, NOT_DISCLOSED 41, REPORT_NOT_FOUND 19 |
| pension_type | 133 | NOT_DISCLOSED 67, REMUNERATION_REPORT_NOT_READ 41, REPORT_NOT_FOUND 19 |
| fiscal_year | 127 | WRONG_YEAR_REPORT 81, REPORT_NOT_FOUND 28, NOT_DISCLOSED 9 |
| largest_holders | 123 | NOT_DISCLOSED 104, REPORT_NOT_FOUND 17, NETWORK_ERROR 2 |
| isin | 99 | NOT_DISCLOSED 94, REPORT_NOT_FOUND 4, NETWORK_ERROR 1 |
| role_disclosure | 81 | NOT_DISCLOSED 30, REMUNERATION_REPORT_NOT_FOUND 28, REMUNERATION_REPORT_NOT_READ 23 |
| headcount | 80 | NOT_DISCLOSED 57, REPORT_NOT_FOUND 18, NETWORK_ERROR 4 |
| ebitda | 70 | NOT_DISCLOSED 47, REPORT_NOT_FOUND 20, NETWORK_ERROR 2 |
| accounting_basis | 67 | NOT_DISCLOSED 43, REPORT_NOT_FOUND 20, NETWORK_ERROR 3 |
| ownership_type | 65 | NOT_DISCLOSED 48, REPORT_NOT_FOUND 15, NETWORK_ERROR 2 |
| controlling_owner | 64 | NOT_DISCLOSED 48, REPORT_NOT_FOUND 14, NETWORK_ERROR 2 |
| controlling_owner_name | 64 | NOT_DISCLOSED 47, REPORT_NOT_FOUND 15, NETWORK_ERROR 2 |
| revenue | 64 | NOT_DISCLOSED 40, REPORT_NOT_FOUND 18, NETWORK_ERROR 5 |
| total_assets | 59 | NOT_DISCLOSED 28, REPORT_NOT_FOUND 24, NETWORK_ERROR 6 |
| shares_outstanding | 57 | NOT_DISCLOSED 36, REPORT_NOT_FOUND 18, NETWORK_ERROR 2 |
| fiscal_year_end | 32 | REPORT_NOT_FOUND 22, NOT_DISCLOSED 4, DOCUMENT_UNREADABLE 4 |
| sector_code | 30 | DERIVATION_INPUT_MISSING 15, REPORT_NOT_FOUND 12, NETWORK_ERROR 2 |
| website | 27 | NOT_DISCLOSED 14, REPORT_NOT_FOUND 13 |
| sub_sector | 23 | REPORT_NOT_FOUND 14, NOT_DISCLOSED 8, NETWORK_ERROR 1 |
| reporting_currency | 21 | REPORT_NOT_FOUND 14, NOT_DISCLOSED 6, NETWORK_ERROR 1 |
| lei | 20 | NO_IDENTIFIER 20 |
| ultimate_parent | 20 | NOT_DISCLOSED 18, REPORT_NOT_FOUND 2 |
| exchange | 18 | NOT_DISCLOSED 13, REPORT_NOT_FOUND 4, NETWORK_ERROR 1 |
| listing_status | 15 | NOT_DISCLOSED 10, REPORT_NOT_FOUND 4, NETWORK_ERROR 1 |
| pay_currency | 10 | NOT_DISCLOSED 5, REMUNERATION_REPORT_NOT_READ 5 |
| business_id | 6 | NOT_DISCLOSED 4, REPORT_NOT_FOUND 2 |
| lti_max_pct | 6 | NOT_DISCLOSED 4, REMUNERATION_REPORT_NOT_READ 2 |
| lti_target_pct | 4 | NOT_DISCLOSED 4 |
| head_office_city | 3 | REPORT_NOT_FOUND 2, NETWORK_ERROR 1 |
| legal_name | 2 | REPORT_NOT_FOUND 2 |
| country_code | 2 | REPORT_NOT_FOUND 2 |
| lti_basis | 2 | NOT_DISCLOSED 2 |
| sti_target_pct | 2 | NOT_DISCLOSED 2 |
| sti_max_pct | 2 | NOT_DISCLOSED 2 |
| lti_received | 2 | NOT_DISCLOSED 2 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| COMMERZBANK AG (`commerzbank-ag`) | 116 | NOT_DISCLOSED: base_salary, benefits_value, fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, sti_max, sti_paid, sti_target |
| RHEINMETALL AG (`rheinmetall-ag-cf2ff08a`) | 109 | NOT_DISCLOSED: base_salary, benefits_value, controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, pension_contribution, shares_outstanding, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| VOLKSWAGEN AG ST O.N. (`volkswagen-ag-be878a5e`) | 103 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Ble Kedros REIC (`ble-kedros-reic`) | 99 | NOT_DISCLOSED: base_salary, benefits, benefits_value, fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, ticker, total_remuneration, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Credito Emiliano (Credem) (`credito-emiliano-credem`) | 97 | NOT_DISCLOSED: benefits_value, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_country, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Abitare In (`abitare-in`) | 97 | NOT_DISCLOSED: benefits_value, controlling_owner, controlling_owner_name, exchange_segment, largest_holders, lti_granted, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, pension_contribution, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| MERCEDES BENZ GROUP AG (`mercedes-benz-group-ag-1545d718`) | 92 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, controlling_owner, controlling_owner_name, exchange_segment, largest_holders, lti_granted, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, pension_contribution, share_price, sti_max, sti_paid, sti_target, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| MUENCH.RUECKVERSICHERUNGS GESELLSCHAFT.VNA O.N. (`muench-rueckversicherungs-gesellschaft-5bba2145`) | 90 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, largest_holders, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_contribution, revenue_by_country, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target |
| CONTINENTAL AG O.N. (`continental-ag-o-n`) | 85 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_target, lti_vested, sti_max, sti_target |
| Villars Holding S.A. (`villars-holding-s-a-0f65ebf6`) | 84 | NETWORK_ERROR: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fte, head_office_city, headcount, isin, largest_holders, listing_date, listing_status, other_names, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets; NO_IDENTIFIER: lei; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Sparebanken More (`sparebanken-more`) | 81 | NOT_DISCLOSED: exchange_segment, isin, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, sti_max, sti_target |
| Melhus Sparebank (`melhus-sparebank`) | 63 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fte, isin, largest_holders, listing_date, listing_status, lti_granted, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| FNM (`fnm`) | 62 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, staff_by_segment, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Plastika Kritis S.A. (`plastika-kritis-s-a`) | 61 | NOT_DISCLOSED: base_salary, benefits_value, fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, share_price, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| DEUTZ AG O.N. (`deutz-ag-8a315ac8`) | 59 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, listing_date, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target |
| Sparebank 1 Helgeland (`sparebank-1-helgeland`) | 58 | NOT_DISCLOSED: base_salary, exchange_segment, isin, listing_date, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target |
| Porsche AG Vz (`porsche-ag-531bb563`) | 56 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, exchange_segment, isin, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target, ticker |
| ABN AMRO BANK N.V. (`abn-amro-bank-n-v`) | 56 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, sti_paid, sti_target |
| VILLEROY + BOCH AG VZ (`villeroy-boch-ag-c5a85d57`) | 54 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, sti_max, sti_paid, sti_target |
| VIOHALCO (`viohalco`) | 52 | NOT_DISCLOSED: exchange_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Avax S.A. (`avax-s-a`) | 51 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target, total_remuneration |
| Nestlé AG (`nestle-ag-371e324c`) | 50 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, exchange_segment, fiscal_year, fte, largest_holders, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_contribution, share_price, staff_by_segment, sti_max, sti_paid, sti_target, total_assets, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| Gek Terna S.A. (`gek-terna-s-a`) | 50 | NOT_DISCLOSED: base_salary, benefits_value, fte, largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, share_price, staff_by_segment, sti_paid, sti_target, ticker, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| HONGKONG LAND HOLDINGS LD (`hongkong-land-holdings-ld-a80908bb`) | 48 | NOT_DISCLOSED: fte, listing_date, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, pension_type, sti_max, sti_paid, sti_target, total_remuneration |
| Cykel AI PLC (`cykel-ai-plc`) | 47 | NOT_DISCLOSED: ebitda, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Upland Resources Limited (`upland-resources-limited-813e7dce`) | 47 | NOT_DISCLOSED: fte, headcount, isin, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| CPI Computer Peripherals International (`cpi-computer-peripherals-international`) | 47 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Public Property Invest (`public-property-invest`) | 46 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_vested, pension_contribution, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Unicorn Mineral Resources plc (`unicorn-mineral-resources-plc-3fc39557`) | 46 | NOT_DISCLOSED: listing_date, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| OPS Retail (`ops-retail`) | 46 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Banca Profilo (`banca-profilo`) | 45 | NOT_DISCLOSED: exchange_segment, fte, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Sol (`sol`) | 45 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, other_names, pension_contribution, revenue, revenue_by_country, revenue_by_segment, staff_by_segment, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Atlantic Sapphire ASA (`T0157`) | 45 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Wolford AG (`wolford-ag-638e2dc1`) | 43 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, sti_paid, sti_target, total_remuneration; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| PROSIEBENSAT.1 MEDIA SE  NA O.N. (`prosiebensat-1-media-se-52d34a8f`) | 43 | NOT_DISCLOSED: exchange_segment, other_names; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Y/Knot Invest S.A. (`y-knot-invest-s-a`) | 43 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target |
| Caltagirone (`caltagirone`) | 43 | NOT_DISCLOSED: exchange_segment, other_names, pension_contribution, share_price, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Tekna Holding (`tekna-holding`) | 41 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, staff_by_segment, sti_paid, sti_target |
| Bergbahnen Engelberg-Trübsee-Titlis AG (`bergbahnen-engelberg-trubsee-titlis-ag`) | 41 | REPORT_NOT_FOUND: accounting_basis, benefits, business_id, controlling_owner, controlling_owner_name, country_code, ebitda, exchange, exchange_segment, fiscal_year, fiscal_year_end, fte, head_office_city, headcount, isin, largest_holders, legal_name, listing_date, listing_status, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, ultimate_parent, website; NO_IDENTIFIER: lei; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Bergbahnen Engelberg-Trübsee-Titlis AG (`bergbahnen-engelberg-trubsee-titlis-ag-e3e76859`) | 41 | REPORT_NOT_FOUND: accounting_basis, benefits, business_id, controlling_owner, controlling_owner_name, country_code, ebitda, exchange, exchange_segment, fiscal_year, fiscal_year_end, fte, head_office_city, headcount, isin, largest_holders, legal_name, listing_date, listing_status, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, ultimate_parent, website; NO_IDENTIFIER: lei; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| SW Umwelttechnik Stoiser & Wolschner AG (`sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89`) | 41 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration |
| VAN DE VELDE (`van-de-velde`) | 41 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| BAWAG Group AG (`bawag-group-ag`) | 40 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, staff_by_segment, sti_max, sti_target, total_remuneration; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Nexum Group AG (`nexum-group-ag-f3ad001d`) | 40 | REPORT_NOT_FOUND: accounting_basis, controlling_owner_name, ebitda, exchange_segment, fte, largest_holders, pe_stake_5pct, revenue_by_country, revenue_by_segment, sector_code, share_price, staff_by_country, staff_by_segment, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, sti_max, sti_target |
| OPS Italia (`ops-italia`) | 40 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: fte, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ASA International Group Plc (`asa-international-group-plc`) | 39 | NOT_DISCLOSED: other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Anemoi International Ltd (`anemoi-international-ltd`) | 39 | NOT_DISCLOSED: fte, headcount, isin, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Acerinox, S.A. (`acerinox-s-a`) | 39 | NOT_DISCLOSED: listing_date, lti_granted, other_names, revenue_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| EKOPAK (`ekopak`) | 39 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, other_names, staff_by_country, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| OXURION (`oxurion`) | 39 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration |
| Cloudbreak Discovery Plc (`cloudbreak-discovery-plc`) | 38 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| EXMAR (`exmar`) | 38 | NOT_DISCLOSED: fte, largest_holders, other_names, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_target, total_remuneration |
| Urbas Grupo Financiero, S.A. (`urbas-grupo-financiero-s-a`) | 38 | NOT_DISCLOSED: listing_date, share_price, staff_by_segment, ticker; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| Aptitude Software Group PLC (`aptitude-software-group-plc`) | 37 | NOT_DISCLOSED: exchange_segment, largest_holders, listing_date, pe_stake_5pct, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; STATED_IN_OTHER_FORM: lti_vested; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| WASGAU PRODUKTIONS & HANDELS NA O.N. (`wasgau-produktions-handels-8c33a77d`) | 37 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, other_names, share_price, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, sti_max, sti_paid, sti_target |
| FAGRON (`fagron`) | 37 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_vested, pension_contribution, sti_paid, total_remuneration; STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target, total_remuneration |
| Olidata (`olidata`) | 37 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, other_names, pension_contribution, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Aurskog Sparebank (`aurskog-sparebank`) | 36 | NOT_DISCLOSED: isin, listing_date, lti_granted, lti_max, lti_target, other_names, revenue_by_country, staff_by_country, staff_by_segment, sti_target, ticker, website |
| VISCOM SE (`viscom-se-859e40d6`) | 36 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, sti_max, sti_paid, sti_target, total_remuneration |
| HEIDELBERG MATERIALS AG O.N. (`heidelberg-materials-ag-20cc4657`) | 36 | NOT_DISCLOSED: base_salary, benefits_value, listing_date, lti_granted, lti_vested, pension_contribution, staff_by_country, staff_by_segment, sti_paid |
| TRIAD GROUP PLC (`triad-group-plc-f815b4d8`) | 36 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| BRANICKS Group AG (`branicks-group-ag`) | 35 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: controlling_owner, controlling_owner_name, fte, headcount, largest_holders, lti_granted, lti_target, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| FUCHS SE O.N. (`fuchs-se-4990a338`) | 35 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| The Swatch Group AG (`the-swatch-group-ag-6a144b9f`) | 35 | NOT_DISCLOSED: aggregate_headcount, base_salary, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Lingotes Especiales, S.A. (`lingotes-especiales-s-a`) | 35 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Newprinces (`newprinces`) | 35 | NOT_DISCLOSED: benefits_value, fte, headcount, lti_granted, lti_vested, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Bluebird Mining Ventures Ltd (`bluebird-mining-ventures-ltd`) | 34 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, isin, largest_holders, listing_date, listing_status, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| OMV AG (`omv-ag-2c5e8b21`) | 34 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, lti_granted, lti_max, sti_paid, sti_target |
| Partners Group Holding AG (`partners-group-holding-ag-d09fd15d`) | 34 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| JENSEN-GROUP (`jensen-group`) | 34 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Atresmedia Corporación de Medios de Comunicación, S.A. (`atresmedia-corporacion-de-medios-de-comunicacion-s-a`) | 34 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, pension_type, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Gr. Sarantis S.A. (`gr-sarantis-s-a`) | 34 | NOT_DISCLOSED: fte, lti_max, lti_target, lti_vested, other_names, share_price, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| European Innovation Solutions S.A. (`european-innovation-solutions-s-a`) | 34 | NOT_DISCLOSED: aggregate_headcount, fte, lti_granted, lti_max, lti_target, lti_vested, pension_type, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| SEB C (`seb-c`) | 33 | NOT_DISCLOSED: exchange, exchange_segment, isin, listing_date, other_names, share_price, shareholding_requirement, ticker; NO_IDENTIFIER: lei; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| SINO-GERMAN UNITED AG O.N. (`sino-german-united-ag-388acb2d`) | 33 | NOT_DISCLOSED: base_salary, benefits_value, ebitda, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| Burgenland Holding AG (`burgenland-holding-ag-a95d1abc`) | 33 | NOT_DISCLOSED: largest_holders, listing_date, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| KPN KON (`kpn-kon`) | 33 | NOT_DISCLOSED: benefits_value, exchange_segment, lti_granted, lti_max, lti_vested, other_names, pension_contribution, revenue_by_country, sti_max, sti_paid, total_remuneration |
| ADYEN (`adyen`) | 33 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ASMALLWORLD AG (`asmallworld-ag`) | 32 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fte, headcount, largest_holders, listing_date, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| SAP SE O.N. (`sap-se-b1a5f6d4`) | 32 | NOT_DISCLOSED: base_salary, exchange_segment, listing_date, lti_max, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target |
| Flexopack Société Anonyme Commercial and Industrial Plastics Company (`flexopack-societe-anonyme-commercial-and-industrial-plastics-company`) | 32 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, fte, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, share_price, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| I Grandi Viaggi (`i-grandi-viaggi`) | 32 | NOT_DISCLOSED: accounting_basis, ebitda, exchange_segment, fte, headcount, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, pension_type, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sti_paid, sti_target, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Caltagirone Editore (`caltagirone-editore`) | 32 | NOT_DISCLOSED: accounting_basis, base_salary, benefits_value, exchange_segment, fiscal_year, fte, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Wool Industry Tria Alfa S.A. (`wool-industry-tria-alfa-s-a`) | 32 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| VOPAK (`vopak`) | 32 | NOT_DISCLOSED: other_names, revenue_by_country; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Wiener Privatbank SE (`wiener-privatbank-se-e8881192`) | 31 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| BAY.MOTOREN WERKE AG ST (`bay-motoren-werke-ag-2bc720d9`) | 31 | NOT_DISCLOSED: ebitda, exchange_segment, listing_date, lti_vested, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Schindler Holding AG (`schindler-holding-ag-d2b61912`) | 31 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Kavango Resources PLC (`kavango-resources-plc-86ebc0c1`) | 31 | NOT_DISCLOSED: benefits, fte, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Kelso Group Holdings Plc (`kelso-group-holdings-plc-5218b8cc`) | 31 | NOT_DISCLOSED: exchange_segment, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_max, lti_target, lti_vested, shareholding_requirement |
| QUESTFOR GR-PRICAF (`questfor-gr-pricaf`) | 31 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, isin, largest_holders, listing_date, listing_status, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Samhällsbyggnadsbolag B (`samhallsbyggnadsbolag-b`) | 31 | NOT_DISCLOSED: isin, listing_date, other_names, revenue_by_country, staff_by_segment; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Fastpartner D (`fastpartner-d`) | 30 | NO_IDENTIFIER: lei; NOT_DISCLOSED: isin, revenue_by_country, shares_outstanding, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_paid, sti_target, total_remuneration |
| Banque Cantonale du Jura SA (`banque-cantonale-du-jura-sa`) | 30 | NOT_DISCLOSED: accounting_basis, benefits_value, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sti_max, sti_target, total_assets, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| City of London Investment Group PLC (`city-of-london-investment-group-plc`) | 30 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| TISCON AG i.A. (`tiscon-ag-i-a-9dafa5a9`) | 30 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| voestalpine AG (`voestalpine-ag-0a494926`) | 30 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Linz Textil Holding AG (`linz-textil-holding-ag-e11cf1a9`) | 30 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| SARTORIUS AG O.N. (`sartorius-ag-9a9c739c`) | 30 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, sti_max, sti_paid, sti_target, ticker |
| Attica Holdings S.A. (`attica-holdings-s-a`) | 30 | NOT_DISCLOSED: lti_max, lti_vested, staff_by_country, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Pharma Mar, S.A. (`pharma-mar-s-a`) | 30 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Pharmanutra (`pharmanutra`) | 30 | NOT_DISCLOSED: fte, lti_vested, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Pininfarina (`pininfarina`) | 30 | NOT_DISCLOSED: ebitda, fte, other_names, pe_stake_5pct, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| DECEUNINCK (`deceuninck`) | 30 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_paid |
| Profile Systems & Software SA (`profile-systems-software-sa`) | 30 | NOT_DISCLOSED: aggregate_headcount, exchange_segment, fte, largest_holders, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| HAVAS (`havas`) | 30 | NOT_DISCLOSED: revenue_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Agilyx (`agilyx`) | 29 | NOT_DISCLOSED: benefits, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| A.I.S. AG (`a-i-s-ag-4ae0fbee`) | 29 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fte, isin, largest_holders, listing_date, listing_status, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band, sector_code; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Rosenbauer International AG (`rosenbauer`) | 29 | NOT_DISCLOSED: benefits_value, listing_date, other_names, pension_contribution, staff_by_segment, sti_max, sti_target, total_remuneration |
| HELLA GMBH+CO.KGAA (`hella-gmbh-co-kgaa-740cce46`) | 29 | NOT_DISCLOSED: lti_granted, pension_contribution; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| KRONES AG O.N. (`krones-ag-f49c3596`) | 29 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, fte, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, staff_by_segment, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Julius Bär Gruppe AG (`julius-bar-gruppe-ag-de864d89`) | 29 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| DIGI Spain Telecom, S.A. (`digi-spain-telecom-s-a`) | 29 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Eurobank S.A. (`eurobank-s-a`) | 29 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, share_price, staff_by_segment, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target, total_remuneration |
| Juventus Football Club (`juventus-football-club`) | 29 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_vested, other_names, pension_contribution, revenue_by_country, share_price, staff_by_country, sti_paid, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| Landi Renzo (`landi-renzo`) | 29 | NOT_DISCLOSED: fte, headcount, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sti_max, sti_target, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| CENERGY (`cenergy`) | 29 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Haidemenos Integrated Printing Services S.A. (`haidemenos-integrated-printing-services-s-a`) | 29 | NOT_DISCLOSED: fte, revenue_by_country, share_price, staff_by_country, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Sonaecom, SGPS, S.A. (`sonaecom-sgps-s-a`) | 29 | NOT_DISCLOSED: exchange_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target |
| Indra Sistemas, S.A. (`indra-sistemas-s-a`) | 29 | NOT_DISCLOSED: accounting_basis, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target |
| Goodtech ASA (`T0428`) | 29 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Atlas Metals Group plc (`atlas-metals-group-plc`) | 28 | NOT_DISCLOSED: fte, listing_date, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_target |
| Burkhalter Holding AG (`burkhalter-holding-ag`) | 28 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, largest_holders, lti_granted, lti_max, lti_target, lti_vested, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, sti_paid, sti_target, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| GAM Holding AG (`gam-holding-ag-6ce711d2`) | 28 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Valiant Holding AG (`valiant-holding-ag-1e2ca715`) | 28 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target |
| Hamak Gold Limited (`hamak-gold-limited-68536373`) | 28 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, sti_max, sti_paid, sti_target |
| London BTC Company Limited (`london-btc-company-limited-acdfd558`) | 28 | NOT_DISCLOSED: fte, headcount, isin, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Predator Oil & Gas Holdings Plc (`predator-oil-gas-holdings-plc-0ba3277f`) | 28 | NOT_DISCLOSED: fte, isin, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| BQUE NAT. BELGIQUE (`bque-nat-belgique`) | 28 | NOT_DISCLOSED: accounting_basis, ebitda, exchange_segment, fte, headcount, other_names, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band, sector_code; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, shareholding_requirement, total_remuneration |
| Irce (`irce`) | 28 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, other_names, pension_type, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Triboo (`triboo`) | 28 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Autohellas S.A. (`autohellas-s-a`) | 28 | NOT_DISCLOSED: largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, pension_type, revenue_by_country, staff_by_segment, sti_paid, sti_target, ticker |
| Intertech S.A. Inter. Technologies (`intertech-s-a-inter-technologies`) | 28 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band |
| Samhällsbyggnadsbolag D (`samhallsbyggnadsbolag-d`) | 28 | NOT_DISCLOSED: ebitda, isin, listing_date, other_names, staff_by_segment, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Amigo Resources PLC (`amigo-resources-plc`) | 27 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fte, headcount, largest_holders, listing_date, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, website; WRONG_YEAR_REPORT: fiscal_year; UNKNOWN: fiscal_year_end; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| IQM Finland Oy (`iqm-finland-oy`) | 27 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Arzneiwerk AG VIDA (`arzneiwerk-ag-vida`) | 27 | NOT_DISCLOSED: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fte, headcount, isin, largest_holders, listing_date, ownership_type, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker; DERIVATION_INPUT_MISSING: market_cap_band, sector_code |
| Cizzle Biotechnology Holdings plc (`cizzle-biotechnology-holdings-plc`) | 27 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_paid, sti_target |
| Compagnie financière Tradition SA (`compagnie-financiere-tradition-sa-940d20ce`) | 27 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| BTV Vier Länder Bank AG (`btv-vier-lander-bank-ag-9e06fc63`) | 27 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid |
| TX Group AG (`tx-group-ag-cdcf98d0`) | 27 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Mobico Group PLC (`mobico-group-plc-3ce9316e`) | 27 | NOT_DISCLOSED: ebitda, exchange, fte, isin, listing_status, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target, total_remuneration |
| MERLIN Properties SOCIMI, S.A. (`merlin-properties-socimi-s-a`) | 27 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_vested, other_names, pension_contribution, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ER Capital (`er-capital`) | 27 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| HOME INVEST BE. (`home-invest-be`) | 27 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, exchange_segment, fte, lti_granted, lti_target, lti_vested, revenue_by_segment, staff_by_country, staff_by_segment, sti_paid, sti_target, total_remuneration; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| ANGLO AMERICAN PLC (`anglo-american-plc`) | 27 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Interlife General Insurance Company S.A. (`interlife-general-insurance-company-s-a`) | 27 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band |
| IMMO MCC (`immo-mcc`) | 27 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Prim, S.A. (`prim-s-a`) | 27 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, share_price, staff_by_country, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Kruso Kapital (`kruso-kapital`) | 27 | NOT_DISCLOSED: ebitda, fte, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| AEVIS VICTORIA SA (`aevis-victoria-sa`) | 26 | NOT_DISCLOSED: listing_date, other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Holand Og Setskog Sparebank (`holand-og-setskog-sparebank`) | 26 | NOT_DISCLOSED: exchange_segment, isin, listing_date, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, staff_by_country, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, sti_max, sti_target, total_remuneration |
| Himalaya Shipping (`himalaya-shipping`) | 26 | NOT_DISCLOSED: base_salary, benefits, benefits_value, exchange_segment, fte, lti_max, lti_vested, other_names, pay_currency, pension_contribution, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_remuneration, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Defence Holdings PLC (`defence-holdings-plc`) | 26 | NOT_DISCLOSED: fte, headcount, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, website; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, shareholding_requirement, sti_max, sti_paid, sti_target |
| Warimpex Finanz- und Beteiligungs AG (`warimpex-finanz-und-beteiligungs-ag-ae611bc8`) | 26 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, staff_by_country, sti_paid, sti_target |
| Q.BEYOND AG NA O.N. (`q-beyond-ag-a25f57b8`) | 26 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band |
| Varia US Properties AG (`varia-us-properties-ag-9f548364`) | 26 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, other_names, staff_by_country, staff_by_segment, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Meridian Mining PLC (`meridian-mining-plc-5760f027`) | 26 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Neo Energy Metals plc (`neo-energy-metals-plc-5b9d4be5`) | 26 | NOT_DISCLOSED: exchange_segment, fte, isin, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Intercos (`intercos`) | 26 | NOT_DISCLOSED: lti_max, lti_target, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Zucchi (`zucchi`) | 26 | NOT_DISCLOSED: largest_holders, other_names, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| QRF (`qrf`) | 26 | NOT_DISCLOSED: benefits, other_names, pension_type, revenue_by_country, revenue_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| CSP International Industria Calze (`csp-international-industria-calze`) | 26 | NOT_DISCLOSED: benefits_value, fte, lti_vested, other_names, pension_contribution, share_price, staff_by_segment, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| BANIJAY GROUP (`banijay-group`) | 26 | NOT_DISCLOSED: exchange_segment, fte, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ROULARTA (`roularta`) | 26 | NOT_DISCLOSED: benefits, exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| WAREHOUSES ESTATES (`warehouses-estates`) | 26 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Kekrops S.A. (`kekrops-s-a`) | 26 | NETWORK_ERROR: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| ABB Ltd (`abb-ltd`) | 25 | NOT_DISCLOSED: ebitda, fte, largest_holders, lti_vested, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_vested, pension_contribution, shareholding_requirement |
| ADIDAS AG NA O.N. (`adidas-ag-na-o-n`) | 25 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fte, headcount, largest_holders, lti_vested, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Arbonia AG (`arbonia-ag`) | 25 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fte, headcount, largest_holders, listing_date, lti_vested, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band |
| Tallink Grupp (`tallink-grupp-5c02812d`) | 25 | NOT_DISCLOSED: other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_target |
| Kendrick Resources plc (`kendrick-resources-plc-f52b1485`) | 25 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| Telefónica, S.A. (`telefonica-s-a`) | 25 | NOT_DISCLOSED: exchange_segment, fte, largest_holders, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Philippos Nakas S.A. (`philippos-nakas-s-a`) | 25 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| General Commercial & Industrial S.A. (`general-commercial-industrial-s-a`) | 25 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: aggregate_headcount, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| AUSTRIACARD HOLDINGS AG (`austriacard-holdings-ag`) | 24 | NOT_DISCLOSED: lti_target, lti_vested, share_price, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Digia Oyj (`digia-oyj`) | 24 | NOT_DISCLOSED: aggregate_headcount, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, staff_by_segment, sti_target, total_remuneration; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| CAFFYNS PLC (`caffyns-plc`) | 24 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Addiko Bank AG (`addiko-bank-ag-167fa5c3`) | 24 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| DEUTSCHE POST AG NA O.N. (`deutsche-post-ag-b89554ef`) | 24 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| PNE AG  NA O.N. (`pne-ag-1fc0baf7`) | 24 | NOT_DISCLOSED: lti_granted, lti_vested, other_names, revenue_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Severfield Plc (`severfield-plc-598e26e7`) | 24 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| NYRSTAR (`nyrstar`) | 24 | REPORT_NOT_FOUND: accounting_basis, benefits, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| Performance Technologies S.A. (`performance-technologies-s-a`) | 24 | NOT_DISCLOSED: fte, headcount, largest_holders, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Class Editori (`class-editori`) | 24 | NOT_DISCLOSED: benefits_value, exchange_segment, isin, other_names, pension_contribution, pension_type, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| KME Group (`kme-group`) | 24 | NOT_DISCLOSED: exchange_segment, lti_max, lti_target, lti_vested, pension_contribution, share_price, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Tesmec (`tesmec`) | 24 | NOT_DISCLOSED: benefits_value, fte, other_names, pension_contribution, pension_type, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target |
| ING GROEP N.V. (`ing-groep-n-v`) | 24 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, total_remuneration |
| Futebol Clube do Porto - Futebol, SAD (`futebol-clube-do-porto-futebol-sad`) | 24 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, shareholding_requirement, sti_target |
| Arteche Lantegi Elkartea, S.A. (`arteche-lantegi-elkartea-s-a`) | 24 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Centrale del Latte d'Italia (`centrale-del-latte-d-italia`) | 24 | NOT_DISCLOSED: exchange_segment, fte, lti_granted, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_paid, sti_target |
| Brooks Macdonald Group plc (`brooks-macdonald-group-plc`) | 23 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Okeanis Eco Tankers (`okeanis-eco-tankers`) | 23 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, fte, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target; FX_RATE_MISSING: market_cap_band |
| Bakkafrost (`bakkafrost`) | 23 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, ownership_type, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| DWS GROUP GMBH+CO.KGAA ON (`dws-group-gmbh-co-kgaa-c6d99d12`) | 23 | NOT_DISCLOSED: accounting_basis, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band, sector_code |
| HAWESKO HOLDING SE (`hawesko-holding-se-bd2e62b7`) | 23 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| INFINEON TECH.AG NA O.N. (`infineon-tech-ag-8660f215`) | 23 | NOT_DISCLOSED: lti_vested, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Helvetia Baloise Holding AG (`helvetia-baloise-holding-ag-784ff8e8`) | 23 | NOT_DISCLOSED: listing_date, lti_max, lti_target, lti_vested, revenue_by_country, staff_by_segment, sti_max, sti_target |
| Panther Metals plc (`panther-metals-plc-a717d305`) | 23 | NOT_DISCLOSED: isin, listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_target, shareholding_requirement, sti_max, sti_target; STATED_IN_OTHER_FORM: lti_vested |
| TOWN CENTRE SECURITIES PLC (`town-centre-securities-plc-5107b789`) | 23 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Pescanova, S.A. (`pescanova-s-a`) | 23 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, largest_holders, listing_date, ownership_type, pe_stake_5pct, pension_type, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: role_disclosure |
| Promotora de Informaciones, S.A. (`promotora-de-informaciones-s-a`) | 23 | NOT_DISCLOSED: lti_vested, other_names, pension_contribution, pension_type, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| Eukedos (`eukedos`) | 23 | NOT_DISCLOSED: fte, largest_holders, other_names, pe_stake_5pct, share_price, staff_by_country, staff_by_segment, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Eurotech (`eurotech`) | 23 | NOT_DISCLOSED: accounting_basis, fte, headcount, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Addex Therapeutics Ltd (`addex-therapeutics-ltd`) | 22 | NOT_DISCLOSED: base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target, total_remuneration |
| Sagax D (`sagax-d`) | 22 | NOT_DISCLOSED: benefits, isin, listing_date, other_names, ticker, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_target, total_remuneration |
| Framery Group (`framery-group`) | 22 | NOT_DISCLOSED: revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Addtech Nordic AB (`addtech-nordic-ab`) | 22 | NOT_DISCLOSED: accounting_basis, fte, isin, other_names, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| DFI Retail Group Holdings Limited (`dfi-retail-group-holdings-limited`) | 22 | NOT_DISCLOSED: fte, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| PITTLER MASCHINENFABRIK AG (`pittler-maschinenfabrik-ag-fb62b449`) | 22 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| HELICAL PLC (`helical-plc-cefce900`) | 22 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target |
| KR1 plc (`kr1-plc-4c4ecf76`) | 22 | NOT_DISCLOSED: isin, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_max, sti_target |
| NeoTerra Group PLC (`neoterra-group-plc-e1ef6c9d`) | 22 | NETWORK_ERROR: benefits, fiscal_year, fte, headcount, pension_type, revenue, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| S & U PLC (`s-u-plc-d076a510`) | 22 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Naturgy Energy Group, S.A. (`naturgy-energy-group-s-a`) | 22 | NOT_DISCLOSED: business_id, isin, listing_date, lti_granted, other_names, revenue_by_country, revenue_by_segment, staff_by_segment, sti_paid, ticker; NO_IDENTIFIER: lei; WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Motor Oil (Hellas) Corinth Refineries S.A. (`motor-oil-hellas-corinth-refineries-s-a`) | 22 | NOT_DISCLOSED: fte, lti_max, lti_target, revenue_by_country, staff_by_segment, sti_max, sti_target, ticker |
| BIOTALYS (`biotalys`) | 22 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target |
| FOUNTAIN (`fountain`) | 22 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sub_sector; DERIVATION_INPUT_MISSING: market_cap_band, sector_code; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Onyx Touristiki Societe Anonyme (`onyx-touristiki-societe-anonyme`) | 22 | NOT_DISCLOSED: fte, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_paid, sti_target |
| De'Longhi (`de-longhi`) | 22 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, pension_contribution, pension_type, share_price, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| BANQUP GROUP (`banqup-group`) | 22 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_paid |
| NEXTENSA (`nextensa`) | 22 | NOT_DISCLOSED: fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| DEMIRE DEUTSCHE MITTELSTAND REAL ESTATE AG (`demire-deutsche-mittelstand-real-estate-ag`) | 21 | NOT_DISCLOSED: other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| BATM Advanced Communications Limited (`batm-advanced-communications-limited`) | 21 | NOT_DISCLOSED: isin, listing_date, other_names, staff_by_country, staff_by_segment, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| APG SGA SA (`apg-sga-sa`) | 21 | NOT_DISCLOSED: business_id, exchange_segment, listing_date, other_names, revenue_by_segment, staff_by_segment, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_max, sti_target |
| EASYJET PLC (`easyjet-plc`) | 21 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| ESSENTRA PLC (`essentra-plc`) | 21 | NOT_DISCLOSED: accounting_basis, ebitda, exchange_segment, fte, listing_date, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Alvotech SDB (`alvotech-sdb`) | 21 | NOT_DISCLOSED: revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| HIAG Immobilien Holding AG (`hiag-immobilien-holding-ag-3a28978d`) | 21 | NOT_DISCLOSED: accounting_basis, exchange, exchange_segment, isin, listing_status, revenue_by_segment, shareholding_requirement, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target, total_remuneration |
| OC Oerlikon Corporation AG (`oc-oerlikon-corporation-ag-8ad162da`) | 21 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_vested, sti_paid |
| Gem Resources Plc (`gem-resources-plc-cf7e06ac`) | 21 | NOT_DISCLOSED: exchange, isin, listing_status, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, shareholding_requirement |
| Rainbow Rare Earths Limited (`rainbow-rare-earths-limited-53b9f467`) | 21 | NOT_DISCLOSED: other_names, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, lti_granted, lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_max, sti_target |
| AGFA-GEVAERT (`agfa-gevaert`) | 21 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_vested, pension_contribution, sti_paid, total_remuneration; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested, sti_paid, total_remuneration |
| D'IETEREN GROUP (`d-ieteren-group`) | 21 | NOT_DISCLOSED: fte; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_max, sti_max, sti_target, total_remuneration |
| Intracom Holdings S.A. (`intracom-holdings-s-a`) | 21 | NOT_DISCLOSED: fte, pension_contribution, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ASML Holding N.V. (`asml`) | 21 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, lti_max_pct, lti_received, lti_target_pct, pension_contribution, sti_max_pct, sti_paid, sti_target_pct, total_remuneration |
| CAB Payments Holdings Plc (`cab-payments-holdings-plc`) | 20 | NOT_DISCLOSED: accounting_basis, benefits, ebitda, exchange_segment, fte, headcount, listing_date, other_names, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Avation PLC (`avation-plc`) | 20 | NOT_DISCLOSED: largest_holders, listing_date, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Industrivärden C (`industrivarden-c`) | 20 | NOT_DISCLOSED: ebitda, isin, other_names, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| Cantargia AB (`cantargia-ab-1b3e1f95`) | 20 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, other_names, revenue_by_segment, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_target, lti_vested, sti_target |
| East Star Resources Plc (`east-star-resources-plc`) | 20 | NOT_DISCLOSED: ebitda, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_vested, pension_type, shareholding_requirement, sti_max, sti_target |
| TTL BETEILIGUNGS- UND GRUNDBESITZ AG INH ON (`ttl-beteiligungs-und-grundbesitz-ag-02636470`) | 20 | REPORT_NOT_FOUND: fte, headcount, other_names, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, total_assets; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: lti_granted, lti_max, pension_contribution, sti_target |
| Dottikon ES Holding AG (`dottikon-es-holding-ag-d22b9c0d`) | 20 | NOT_DISCLOSED: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| DSM-Firmenich AG (`dsm-firmenich-ag-62366aa6`) | 20 | NOT_DISCLOSED: aggregate_headcount, base_salary, exchange_segment, fte, largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, share_price, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| R. STAHL AG NA O.N. (`r-stahl-ag-04fdadc0`) | 20 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, sti_max, sti_target |
| Pensana Plc (`pensana-plc-3caf2324`) | 20 | NOT_DISCLOSED: pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| SERCO GROUP PLC (`serco-group-plc-96a15710`) | 20 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Sealand Capital Galaxy Limited (`sealand-capital-galaxy-limited-126bc181`) | 20 | NOT_DISCLOSED: isin, listing_date, other_names, share_price, staff_by_country, staff_by_segment, ticker, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| Vox Valor Capital Limited (`vox-valor-capital-limited-f573f9e1`) | 20 | NO_IDENTIFIER: lei; WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: fte, largest_holders, pe_stake_5pct, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| OPTION (`option`) | 20 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Logismos Information Systems S.A. (`logismos-information-systems-s-a`) | 20 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Glintt - Global Intelligent Technologies, S.A. (`glintt-global-intelligent-technologies-s-a`) | 20 | REPORT_NOT_FOUND: accounting_basis, benefits, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Cembre (`cembre`) | 20 | NOT_DISCLOSED: largest_holders, lti_granted, lti_vested, other_names, pe_stake_5pct, share_price, sti_max; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| CM.COM (`cm-com`) | 20 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| CTAC (`ctac`) | 20 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Petros Petropoulos AEVE (`petros-petropoulos-aeve`) | 20 | NOT_DISCLOSED: accounting_basis, benefits, controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Sentia (`sentia`) | 19 | NOT_DISCLOSED: lti_max, lti_vested, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| B&M EUROPEAN VALUE RETAIL PLC (`b-m-european-value-retail-plc`) | 19 | NOT_DISCLOSED: isin, share_price, staff_by_country, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_paid, sti_target |
| BP PLC (`bp-plc`) | 19 | NOT_DISCLOSED: exchange_segment, listing_date; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, sti_max, sti_target |
| Barratt Redrow plc (`barratt-redrow-plc`) | 19 | NOT_DISCLOSED: exchange_segment, listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Braemar Plc (`braemar-plc`) | 19 | NOT_DISCLOSED: listing_date, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Brondbyernes IF (`brondbyernes-if`) | 19 | NOT_DISCLOSED: exchange_segment, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_target, ticker |
| Ostasiatiske (`ostasiatiske`) | 19 | NOT_DISCLOSED: exchange_segment, isin, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_type, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_target, ticker, ultimate_parent; NO_IDENTIFIER: lei |
| Endeavour Mining plc (`endeavour-mining-plc`) | 19 | NOT_DISCLOSED: ebitda, other_names, revenue_by_country, share_price, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Vincorion SE (`vincorion-se-16aba459`) | 19 | DOCUMENT_UNREADABLE: accounting_basis, benefits, ebitda, fiscal_year, fiscal_year_end, fte, headcount, pension_type, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| C Capital Holdings AG (`c-capital-holdings-ag-53a1594e`) | 19 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, ownership_type, pe_stake_5pct, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, lti_max, lti_target, lti_vested, pension_type, sti_max, sti_paid, sti_target |
| Lenzing AG (`lenzing-ag-c20f8b4a`) | 19 | NOT_DISCLOSED: lti_granted, lti_target, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, sti_max, sti_target |
| MBB SE O.N. (`mbb-se-be761dea`) | 19 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| RHOEN-KLINIKUM O.N. (`rhoen-klinikum-0a013089`) | 19 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_segment, staff_by_segment, sti_target |
| Orior AG (`orior-ag-bfeb91d6`) | 19 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Peach Property Group AG (`peach-property-group-ag-b0194e98`) | 19 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| HAYS PLC (`hays-plc-7467dcac`) | 19 | NOT_DISCLOSED: isin, listing_date, other_names, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_paid, sti_target, total_remuneration |
| IMC EXPLORATION GROUP PLC (`imc-exploration-group-plc-91b5483e`) | 19 | NOT_DISCLOSED: isin, listing_date, other_names, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target |
| JERSEY ELECTRICITY PLC (`jersey-electricity-plc-f27b7332`) | 19 | NOT_DISCLOSED: exchange_segment, isin, listing_date, other_names, revenue_by_country, staff_by_country, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Mantle Resilience Plc (`mantle-resilience-plc-90cc3350`) | 19 | REPORT_NOT_FOUND: accounting_basis, ebitda, exchange_segment, fte, largest_holders, listing_date, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: sti_target |
| RIO TINTO PLC (`rio-tinto-plc-1ed16286`) | 19 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Zenith Energy Ltd (`zenith-energy-ltd-4fdd6c5a`) | 19 | NOT_DISCLOSED: isin, listing_date, other_names, staff_by_country, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| BIOSENIC (`biosenic`) | 19 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested, pension_contribution, sti_paid, sti_target |
| Frigoglass S.A.I.C. (`frigoglass-s-a-i-c`) | 19 | NOT_DISCLOSED: fte, other_names, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Moltiply Group (`moltiply-group`) | 19 | NOT_DISCLOSED: lti_max, lti_vested, staff_by_segment, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| TEXAF (`texaf`) | 19 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Técnicas Reunidas, S.A. (`tecnicas-reunidas-s-a`) | 19 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, lti_granted, lti_max, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, shares_outstanding, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Thessaloniki Water Supply & Sewerage Co S.A. (`thessaloniki-water-supply-sewerage-co-s-a`) | 19 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Desarrollos Especiales de Sistemas de Anclaje, S.A. (`desarrollos-especiales-de-sistemas-de-anclaje-s-a`) | 19 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, other_names, pension_type, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_paid, sti_target, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, pension_contribution, sti_max, sti_paid, sti_target |
| Talgo, S.A. (`talgo-s-a`) | 19 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_segment, sti_paid, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| CMC Markets Plc (`cmc-markets-plc`) | 18 | NOT_DISCLOSED: other_names, share_price, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Alina Holdings Plc (`alina-holdings-plc`) | 18 | NOT_DISCLOSED: fte, listing_date, revenue_by_country, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Voss Veksel Landmandsbank (`voss-veksel-landmandsbank`) | 18 | NOT_DISCLOSED: business_id, exchange_segment, isin, listing_date, other_names, revenue_by_country, staff_by_country, staff_by_segment, ticker, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, sti_paid, sti_target, total_remuneration |
| BAYWA AG NA O.N. (`baywa-ag-na-o-n`) | 18 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted |
| Cindrigo Holdings Limited (`cindrigo-holdings-limited`) | 18 | NOT_DISCLOSED: fte, isin, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_max, sti_target |
| Contango Holdings plc (`contango-holdings-plc`) | 18 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| DFS Furniture plc (`dfs-furniture-plc`) | 18 | NOT_DISCLOSED: listing_date, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| NORDWEST HANDEL AG (`nordwest-handel-ag-ee04116a`) | 18 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| Swisscom AG (`swisscom-ag-b3649c71`) | 18 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| MOUNTVIEW ESTATES PLC (`mountview-estates-plc-6b66d1a5`) | 18 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Ondo InsurTech Plc (`ondo-insurtech-plc-e2c31efb`) | 18 | NOT_DISCLOSED: listing_date, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| VP PLC (`vp-plc-94ebb5f9`) | 18 | NOT_DISCLOSED: exchange_segment, fte, listing_date, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| SIPEF (`sipef`) | 18 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| Acciona, S.A. (`acciona-s-a`) | 18 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, lti_granted, lti_target, other_names, ownership_type, pe_stake_5pct, revenue_by_country, staff_by_country, staff_by_segment, sti_target, ticker |
| Airtificial Intelligence Structures, S.A. (`airtificial-intelligence-structures-s-a`) | 18 | NOT_DISCLOSED: exchange_segment, fte, headcount, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Elvalhalcor Hellenic Copper and Aluminium Industry S.A. (`elvalhalcor-hellenic-copper-and-aluminium-industry-s-a`) | 18 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_max, sti_target |
| CIR (`cir`) | 18 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, share_price, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| VALUE8 (`value8`) | 18 | NOT_DISCLOSED: exchange_segment, fte, headcount, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement |
| ENERGYVISION (`energyvision`) | 18 | NOT_DISCLOSED: exchange_segment, other_names, pension_type, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Icop (`icop`) | 18 | NOT_DISCLOSED: accounting_basis, ebitda, fiscal_year, fiscal_year_end, fte, headcount, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| ACCENTIS (`accentis`) | 18 | NOT_DISCLOSED: benefits, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| MIKO (`miko`) | 18 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Fourlis Holdings S.A. (`fourlis-holdings-s-a`) | 18 | NOT_DISCLOSED: exchange_segment, fte, listing_date, lti_granted, lti_vested, revenue_by_country, revenue_by_segment, share_price, staff_by_segment, sti_paid, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Ilkka 2 (`ilkka-2`) | 18 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| BioVersys AG (`bioversys-ag`) | 17 | NOT_DISCLOSED: benefits, exchange_segment, lti_max, lti_target, lti_vested, other_names, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_target |
| ASIA STRATEGIC HOLDINGS LIMITED (`asia-strategic-holdings-limited`) | 17 | NOT_DISCLOSED: fte, isin, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_target |
| BSF Enterprise Plc (`bsf-enterprise-plc`) | 17 | NETWORK_ERROR: other_names, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| C&C Group PLC (`c-c-group-plc`) | 17 | NOT_DISCLOSED: listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| Jinhui Shipping (`jinhui-shipping`) | 17 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Chesnara PLC (`chesnara-plc`) | 17 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, shares_outstanding, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Dunelm Group plc (`dunelm-group-plc`) | 17 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, lti_granted, lti_vested, pension_contribution, sti_paid, sti_target |
| Elixirr International plc (`elixirr-international-plc`) | 17 | NOT_DISCLOSED: revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Fastighetsbolag Emilshus Pref (`fastighetsbolag-emilshus-pref`) | 17 | NOT_DISCLOSED: other_names, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target, total_remuneration |
| dormakaba Holding AG (`dormakaba-holding-ag-9c17f7d1`) | 17 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Emerald Horizon AG (`emerald-horizon-ag-a6420623`) | 17 | NOT_DISCLOSED: exchange_segment, other_names, pe_stake_5pct, revenue_by_segment, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Stadlauer Malzfabrik AG (`stadlauer-malzfabrik-ag-8a23c30d`) | 17 | NOT_DISCLOSED: aggregate_headcount, benefits, largest_holders, listing_date, lti_max, lti_target, other_names, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| PROCREDIT HOLDING AG NA EO 5 (`procredit-holding-ag-74495a3c`) | 17 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_country, sti_max, sti_paid, sti_target |
| SARTORIUS AG VZO O.N. (`sartorius-ag-a22309c5`) | 17 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_vested, other_names, pension_contribution, sti_max, sti_paid |
| Feintool International Holding AG (`feintool-international-holding-ag-dd22099c`) | 17 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Forbo Holding AG (`forbo-holding-ag-6863b5df`) | 17 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Glarner Kantonalbank (`glarner-kantonalbank-8ede902a`) | 17 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_target, sti_target, total_remuneration; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_target, sti_target |
| Graubündner Kantonalbank (`graubundner-kantonalbank-746931b2`) | 17 | NOT_DISCLOSED: accounting_basis, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, revenue_by_segment, staff_by_segment, sti_max, sti_target |
| Kühne + Nagel International AG (`kuhne-nagel-international-ag-2949951f`) | 17 | NOT_DISCLOSED: aggregate_headcount, exchange_segment, listing_date, lti_max, lti_target, lti_vested, other_names, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_target |
| Schlatter Industries AG (`schlatter-industries-ag-e8b6df3d`) | 17 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Nanoco Group plc (`nanoco-group-plc-c86c4088`) | 17 | NOT_DISCLOSED: exchange, isin, listing_date, listing_status, revenue_by_segment, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Narf Industries Plc (`narf-industries-plc-2c307c53`) | 17 | NOT_DISCLOSED: exchange_segment, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| Pennon Group Plc (`pennon-group-plc-7143cdb4`) | 17 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| RENISHAW PLC (`renishaw-plc-02f27561`) | 17 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Biesse (`biesse`) | 17 | NOT_DISCLOSED: largest_holders, lti_granted, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_contribution, share_price, staff_by_segment, sti_max, sti_target; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| El.En. (`el-en`) | 17 | NOT_DISCLOSED: fte, largest_holders, lti_max, lti_vested, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| ONWARD MEDICAL (`onward-medical`) | 17 | NOT_DISCLOSED: exchange_segment, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Mota-Engil, SGPS, S.A. (`mota-engil-sgps-s-a`) | 17 | NOT_DISCLOSED: benefits, exchange_segment, fte, other_names, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_target |
| ECONOCOM GROUP (`econocom-group`) | 17 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| KBC (`kbc`) | 17 | NOT_DISCLOSED: exchange_segment, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_target, sti_paid, sti_target |
| Alpha Bank S.A. (`alpha-bank-s-a`) | 17 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, staff_by_segment, sti_target, ticker |
| Flour Mills C. Sarantopoulos S.A. (`flour-mills-c-sarantopoulos-s-a`) | 17 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, pay_currency, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| VIVORYON (`vivoryon`) | 17 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max |
| Ramada Investimentos e Indústria, S.A. (`ramada-investimentos-e-industria-s-a`) | 17 | NOT_DISCLOSED: benefits_value, exchange_segment, lti_granted, lti_target, lti_vested, pension_contribution, staff_by_country, staff_by_segment, sti_target, total_remuneration |
| XIOR (`xior`) | 17 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_vested, pension_contribution, pension_type, sti_paid, total_remuneration |
| Nicolás Correa, S.A. (`nicolas-correa-s-a`) | 17 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| AS Commercial Industrial Company of Computers and Toys S.A. (`as-commercial-industrial-company-of-computers-and-toys-s-a`) | 17 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, share_price, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| DiaSorin (`diasorin`) | 17 | NOT_DISCLOSED: fte, lti_max, lti_target, lti_vested, other_names, pension_contribution, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| SEQUANA MEDICAL (`sequana-medical`) | 17 | NOT_DISCLOSED: exchange_segment, revenue_by_segment, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Flughafen Wien AG (`flughafen-wien-ag`) | 16 | NOT_DISCLOSED: other_names, shareholding_requirement, staff_by_country; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Alkemy Capital Investments PLC (`alkemy-capital-investments-plc`) | 16 | NOT_DISCLOSED: ebitda, fte, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution |
| BELLWAY PLC (`bellway-plc`) | 16 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Berkeley Group Holdings (The) Plc (`berkeley-group-holdings-the-plc`) | 16 | NOT_DISCLOSED: exchange_segment, fte, headcount, listing_date, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested, sti_max, sti_paid, sti_target |
| CARDIFF PROPERTY PLC (`cardiff-property-plc`) | 16 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, shareholding_requirement, sti_target |
| Petrolia (`petrolia`) | 16 | NOT_DISCLOSED: base_salary, benefits, benefits_value, exchange_segment, listing_date, pension_contribution, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| ALSO Holding AG (`also-holding-ag`) | 16 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target |
| ASOS plc (`asos-plc`) | 16 | NOT_DISCLOSED: isin, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| CHEMRING GROUP PLC (`chemring-group-plc`) | 16 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| Adval Tech Holding AG (`adval-tech-holding-ag`) | 16 | NOT_DISCLOSED: accounting_basis, ebitda, fte, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| Alpine Select AG (`alpine-select-ag`) | 16 | NOT_DISCLOSED: exchange_segment, other_names, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: shareholding_requirement, sti_max, sti_target |
| Croda International Plc (`croda-international-plc`) | 16 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, share_price, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested |
| DERWENT LONDON PLC (`derwent-london-plc`) | 16 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, listing_date, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker, ultimate_parent; REMUNERATION_REPORT_NOT_READ: sti_paid |
| Electrovac AG (`electrovac-ag-8d562e26`) | 16 | NOT_DISCLOSED: other_names, pe_stake_5pct, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| READCREST CAPITAL AG O.N. (`readcrest-capital-ag-e4689651`) | 16 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, staff_by_segment, sti_paid, sti_target |
| HELIOS SOLAR AG (`helios-solar-ag-797724e7`) | 16 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, ebitda, headcount, largest_holders, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Hypothekarbank Lenzburg AG (`hypothekarbank-lenzburg-ag-52099ad5`) | 16 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| Implenia AG (`implenia-ag-9355840d`) | 16 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Infomaniak SA (`infomaniak-sa-87b05313`) | 16 | NOT_DISCLOSED: exchange_segment, staff_by_country; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_target |
| mobilezone holding ag (`mobilezone-holding-ag-fc013b59`) | 16 | NOT_DISCLOSED: isin, listing_date, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Siegfried Holding AG (`siegfried-holding-ag-5b520bab`) | 16 | NOT_DISCLOSED: lti_max, lti_target, lti_vested; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| VZ Holding AG (`vz-holding-ag-6150cdf9`) | 16 | NOT_DISCLOSED: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested |
| Walliser Kantonalbank (`walliser-kantonalbank-2ca3a748`) | 16 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| FDM Group (Holdings) plc (`fdm-group-holdings-plc-5f964aeb`) | 16 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Hikma Pharmaceuticals PLC (`hikma-pharmaceuticals-plc-b8d686c5`) | 16 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Hydrogen Utopia International PLC (`hydrogen-utopia-international-plc-51b104d1`) | 16 | NOT_DISCLOSED: exchange_segment, listing_date, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_paid, sti_target |
| JARDINE MATHESON HOLDINGS LD (`jardine-matheson-holdings-ld-9fc044a9`) | 16 | NOT_DISCLOSED: fte, isin, listing_date, other_names, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target, total_remuneration |
| PPHE Hotel Group Limited (`pphe-hotel-group-limited-8368d7b3`) | 16 | NOT_DISCLOSED: fte, headcount, isin, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Pan African Resources PLC (`pan-african-resources-plc-e4db7ca3`) | 16 | NOT_DISCLOSED: listing_date, other_names; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, shareholding_requirement, sti_target |
| WPP PLC (`wpp-plc-8fd77caa`) | 16 | NOT_DISCLOSED: exchange_segment, isin, listing_date; DERIVATION_INPUT_MISSING: sector_code; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Zegona Communications plc (`zegona-communications-plc-62fe3df0`) | 16 | NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| iFOREX Financial Trading Holdings Ltd (`iforex-financial-trading-holdings-ltd-74e42f45`) | 16 | NOT_DISCLOSED: fte, headcount, isin, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| Azkoyen SA (`azkoyen`) | 16 | NOT_DISCLOSED: staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: base_salary, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Ekter SA (`ekter-sa`) | 16 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| AJAX (`ajax`) | 16 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, shareholding_requirement, sti_max, sti_target, total_remuneration |
| Flexdeal Simfe S.A. (`flexdeal-simfe-s-a`) | 16 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_vested, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Distribuidora Internacional de Alimentación, S.A. (`distribuidora-internacional-de-alimentacion-s-a`) | 16 | NOT_DISCLOSED: other_names, pension_type, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Athens Medical C.S.A. (`athens-medical-c-s-a`) | 16 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| NAI ORD SHARES (`nai-ord-shares`) | 16 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, other_names, ownership_type, pe_stake_5pct, share_price, staff_by_country, staff_by_segment, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, shareholding_requirement |
| PORCELEYNE FLES (`porceleyne-fles`) | 16 | NOT_DISCLOSED: exchange_segment, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Renta Corporación Real Estate, S.A. (`renta-corporacion-real-estate-s-a`) | 16 | NOT_DISCLOSED: accounting_basis, fte, largest_holders, other_names, pe_stake_5pct, pension_contribution, pension_type, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_target, ticker |
| RANDSTAD NV (`randstad-nv`) | 16 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target |
| Erste Group Bank AG (`erste-group-bank-ag`) | 15 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| Atalaya Mining Copper, S.A. (`atalaya-mining-copper-s-a`) | 15 | NOT_DISCLOSED: isin, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target, total_remuneration |
| BABCOCK INTERNATIONAL GROUP PLC (`babcock-international-group-plc`) | 15 | NOT_DISCLOSED: exchange_segment, fte, headcount, largest_holders, listing_date, other_names, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Blencowe Resources Plc (`blencowe-resources-plc`) | 15 | NOT_DISCLOSED: exchange_segment, fte, listing_date, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| CLOSE BROTHERS GROUP PLC (`close-brothers-group-plc`) | 15 | NOT_DISCLOSED: largest_holders, other_names, pe_stake_5pct, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_paid, sti_target |
| BVZ Holding AG (`bvz-holding-ag`) | 15 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, pension_contribution, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: sti_target |
| Basler Kantonalbank (`basler-kantonalbank`) | 15 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_target; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| BAYWA AG VINK.NA. O.N. (`baywa-ag-vink-na-o-n`) | 15 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Burberry Group plc (`burberry-group-plc`) | 15 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Paratus Energy (`paratus-energy`) | 15 | NO_IDENTIFIER: lei; NOT_DISCLOSED: benefits, business_id, exchange_segment, isin, largest_holders, pe_stake_5pct, pension_type, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Crest Nicholson Holdings PLC (`crest-nicholson-holdings-plc`) | 15 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, ownership_type, pe_stake_5pct, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested, sti_paid |
| EnQuest PLC (`enquest-plc`) | 15 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; STATED_IN_OTHER_FORM: lti_granted |
| KPS AG NA O.N. (`kps-ag-d763be73`) | 15 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| PFERDEWETTEN.DE AG NA ON (`pferdewetten-de-ag-07705286`) | 15 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: pension_type, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, sti_target |
| STO SE+CO.KGAA VZO O.N. (`sto-se-co-kgaa-9a1ae007`) | 15 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target |
| Centiel AG (`centiel-ag-eeeda54a`) | 15 | NOT_DISCLOSED: exchange_segment, fte, listing_date, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, shareholding_requirement, sti_max, sti_paid, sti_target |
| Chocoladefabriken Lindt & Sprüngli AG (`chocoladefabriken-lindt-sprungli-ag-f056b804`) | 15 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_segment, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| Comet Holding AG (`comet-holding-ag-f1ab2b78`) | 15 | NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_target |
| CTS EVENTIM KGAA (`cts-eventim-kgaa-1664614e`) | 15 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, pension_contribution, sti_max, sti_target |
| SIXT SE ST O.N. (`sixt-se-8094cf8b`) | 15 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| Luzerner Kantonalbank AG (`luzerner-kantonalbank-ag-79246b45`) | 15 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Medacta Group SA (`medacta-group-sa-00954b7f`) | 15 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| MindMaze Therapeutics Holding SA (`mindmaze-therapeutics-holding-sa-b2339575`) | 15 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target, total_remuneration |
| Santhera Pharmaceuticals Holding AG (`santhera-pharmaceuticals-holding-ag-8f83ccd5`) | 15 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, listing_date, ownership_type, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| SGS AG (`sgs-ag-65380806`) | 15 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, fte, listing_date, lti_vested, pension_contribution, staff_by_country, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| Vontobel Holding AG (`vontobel-holding-ag-1d88ea32`) | 15 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| GREAT SOUTHERN COPPER PLC (`great-southern-copper-plc-d619eabd`) | 15 | NETWORK_ERROR: revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| HSBC HOLDINGS PLC (`hsbc-holdings-plc-4c10f5ba`) | 15 | NOT_DISCLOSED: exchange, isin, listing_date, listing_status, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_vested, sti_paid |
| Imaging Biometrics Limited (`imaging-biometrics-limited-3542bcb1`) | 15 | NOT_DISCLOSED: isin, listing_date, share_price, staff_by_country, staff_by_segment, ticker, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| KIER GROUP PLC (`kier-group-plc-bc0b668a`) | 15 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Metlen Energy & Metals Plc (`metlen-energy-metals-plc-f17cd684`) | 15 | NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target |
| Mila Resources Plc (`mila-resources-plc-585b51da`) | 15 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, sti_max, sti_target |
| NEXT PLC (`next-plc-37d4cfcc`) | 15 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| On The Beach Group PLC (`on-the-beach-group-plc-bb910bc1`) | 15 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Rosebank Industries plc (`rosebank-industries-plc-0724d06f`) | 15 | NOT_DISCLOSED: isin, other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| ST. JAMES'S PLACE PLC (`st-james-s-place-plc-23c228ff`) | 15 | NOT_DISCLOSED: ebitda, exchange_segment, listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Technologies New Energy plc (`technologies-new-energy-plc-2628dc2d`) | 15 | NETWORK_ERROR: benefits, fte, headcount, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| Unite Group Plc (`unite-group-plc-507a1ba4`) | 15 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| CUMULEX (`cumulex`) | 15 | NOT_DISCLOSED: exchange_segment, fte, headcount, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sub_sector; DERIVATION_INPUT_MISSING: market_cap_band, sector_code; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| IMMO MOURY (`immo-moury`) | 15 | NOT_DISCLOSED: fte, other_names, revenue_by_country, shareholding_requirement, staff_by_country; WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: sti_max, sti_target, total_remuneration |
| Inmocemento, S.A. (`inmocemento-s-a`) | 15 | NOT_DISCLOSED: exchange_segment, other_names, pension_contribution, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Libertas 7, S.A. (`libertas-7-s-a`) | 15 | NOT_DISCLOSED: benefits, fte, lti_granted, lti_target, lti_vested, other_names, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| TSK Electrónica y Electricidad, S.A. (`tsk-electronica-y-electricidad-s-a`) | 15 | NOT_DISCLOSED: exchange_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Pipe Works L. Girakian Profil S.A. (`pipe-works-l-girakian-profil-s-a`) | 15 | NOT_DISCLOSED: fte, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, pension_contribution, shareholding_requirement, total_remuneration |
| Aedes (`aedes`) | 15 | NOT_DISCLOSED: accounting_basis, fte, headcount, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| NEW SOURCES ENERGY (`new-sources-energy`) | 15 | NOT_DISCLOSED: benefits_value, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, revenue_by_segment, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration |
| COLRUYT (`colruyt`) | 15 | NOT_DISCLOSED: exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| EVS (`evs`) | 15 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_vested, pension_contribution, sti_paid, total_remuneration |
| Duro Felguera, S.A. (`duro-felguera-s-a`) | 15 | NOT_DISCLOSED: exchange_segment, fte, headcount, lti_granted, lti_max, lti_target, pension_type, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Aegean Airlines S.A. (`aegean-airlines-s-a`) | 15 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, share_price, staff_by_segment, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| ATOSS SOFTWARE SE (`atoss-software-se`) | 14 | NOT_DISCLOSED: lti_granted, lti_vested, other_names, revenue_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| ACG Metals Limited (`acg-metals-limited`) | 14 | NOT_DISCLOSED: fte, isin, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| SpareBank 1 Nordmore (`sparebank-1-nordmore`) | 14 | NOT_DISCLOSED: exchange_segment, isin, listing_date, revenue_by_country, revenue_by_segment, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_paid, sti_target |
| Chesterfield Resources PLC (`chesterfield-resources-plc`) | 14 | NOT_DISCLOSED: fte, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Compass Group PLC (`compass-group-plc`) | 14 | NOT_DISCLOSED: exchange_segment, largest_holders, listing_date, other_names, pe_stake_5pct, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Besqab Pref B (`besqab-pref-b`) | 14 | NOT_DISCLOSED: revenue_by_country, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| EPIC Suisse AG (`epic-suisse-ag-7c2f8dc4`) | 14 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| DRAEGERWERK ST.A.O.N. (`draegerwerk-6fd21937`) | 14 | NOT_DISCLOSED: lti_granted, lti_max, lti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, sti_max, sti_paid, sti_target |
| DT. Konsum Real Estae AG (`dt-konsum-real-estae-ag-4e32eb34`) | 14 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, pension_contribution, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| FIRST SENSOR AG O.N. (`first-sensor-ag-34cd25ce`) | 14 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| EvoNext Holdings SA (`evonext-holdings-sa-be1893c4`) | 14 | REPORT_NOT_FOUND: exchange_segment, fte, headcount, listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: lti_vested, sti_paid |
| Sandoz Group AG (`sandoz-group-ag-7e6ec0e7`) | 14 | NOT_DISCLOSED: lti_target, lti_vested, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Vaudoise Assurances Holding SA (`vaudoise-assurances-holding-sa-00d7d6b4`) | 14 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| Züblin Immobilien Holding AG (`zublin-immobilien-holding-ag-cf81b4e5`) | 14 | NOT_DISCLOSED: benefits_value, fte, listing_date, lti_granted, lti_target, lti_vested, revenue_by_segment, staff_by_segment, sti_target |
| GAMES WORKSHOP GROUP PLC (`games-workshop-group-plc-0f667d1d`) | 14 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| HAMMERSON PLC (`hammerson-plc-f1d49abe`) | 14 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| IRISH CONTINENTAL GROUP PLC (`irish-continental-group-plc-7ab1ffb0`) | 14 | NOT_DISCLOSED: other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| InvestAcc Group Limited (`investacc-group-limited-a223f237`) | 14 | NOT_DISCLOSED: isin, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_paid, sti_target, total_remuneration |
| Malibu Life Holdings Limited (`malibu-life-holdings-limited-bdcf12a6`) | 14 | NOT_DISCLOSED: ebitda, fte, isin, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, pension_type, sti_max, sti_target |
| Orient Telecoms Plc (`orient-telecoms-plc-9de5e795`) | 14 | NOT_DISCLOSED: exchange, isin, listing_status, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, shareholding_requirement |
| Quantum Data Energy PLC (`quantum-data-energy-plc-52f9bd33`) | 14 | NOT_DISCLOSED: isin, largest_holders, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| The Smarter Web Company PLC (`the-smarter-web-company-plc-1e8404aa`) | 14 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Total Graphite Plc (`total-graphite-plc-c68433cc`) | 14 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, shareholding_requirement, sti_target |
| Aktor Societe Anonyme Holding Company Technical and Energy Projects (`aktor-societe-anonyme-holding-company-technical-and-energy-projects`) | 14 | NOT_DISCLOSED: base_salary, fte, lti_granted, lti_max, lti_target, lti_vested, share_price, staff_by_segment, sti_max; DERIVATION_INPUT_MISSING: market_cap_band |
| EXOR NV (`exor-nv`) | 14 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, ebitda, exchange_segment, lti_target, lti_vested, pay_currency, pension_contribution, revenue_by_country, revenue_by_segment, sti_paid, total_remuneration; STATED_IN_OTHER_FORM: lti_granted |
| NEPI ROCKCASTLE (`nepi-rockcastle`) | 14 | NOT_DISCLOSED: fte, pension_type, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution |
| ASCENCIO (`ascencio`) | 14 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| CMB.TECH (`cmb-tech`) | 14 | NOT_DISCLOSED: benefits, exchange_segment, pension_type, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| RETAIL ESTATES (`retail-estates`) | 14 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target, total_remuneration |
| Alumil Aluminium Industry S.A. (`alumil-aluminium-industry-s-a`) | 14 | NOT_DISCLOSED: other_names, pension_contribution, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, sti_max, sti_paid, sti_target |
| EDP, S.A. (`edp-s-a`) | 14 | NOT_DISCLOSED: exchange_segment, fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, shareholding_requirement |
| Teixeira Duarte, S.A. (`teixeira-duarte-s-a`) | 14 | REMUNERATION_REPORT_NOT_READ: pension_contribution, shareholding_requirement, sti_max, sti_target |
| ATENOR (`atenor`) | 14 | NOT_DISCLOSED: benefits, exchange_segment, fte, headcount, other_names, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| UCB (`ucb`) | 14 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Nafpaktos Textile Industry S.A. (`nafpaktos-textile-industry-s-a`) | 14 | NOT_DISCLOSED: benefits_value, fte, listing_date, other_names, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| EPH Invest (`eph-invest`) | 14 | NOT_DISCLOSED: benefits, exchange_segment, fte, largest_holders, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| DELTICOM AG  NA O.N. (`delticom-ag-na-o-n`) | 13 | NOT_DISCLOSED: lti_max, lti_vested, other_names, pension_type, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year |
| Kesko B (`kesko-b`) | 13 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| BARCLAYS PLC (`barclays-plc`) | 13 | NOT_DISCLOSED: exchange_segment, isin, largest_holders, listing_date, pe_stake_5pct, staff_by_country, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Revolutionrace (`revolutionrace`) | 13 | NOT_DISCLOSED: isin, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Energean PLC (`energean-plc`) | 13 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, ownership_type, pe_stake_5pct, revenue_by_country, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target |
| Corem Property D (`corem-property-d`) | 13 | NOT_DISCLOSED: shareholding_requirement, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: benefits_value, sti_paid, sti_target |
| TKMS AG + CO. KGAA O.N. (`tkms-ag-co-kgaa-f468ef4d`) | 13 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Edisun Power Europe AG (`edisun-power-europe-ag-e6666cb6`) | 13 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target |
| Emmi AG (`emmi-ag-ad10f47a`) | 13 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| HOCHTIEF AG (`hochtief-ag-3d11e5c0`) | 13 | NOT_DISCLOSED: fiscal_year, lti_target, lti_vested, sti_target |
| Galenica AG (`galenica-ag-3e4e6756`) | 13 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, pension_type, sti_max, sti_paid, sti_target |
| Kudelski S.A. (`kudelski-s-a-fca01ba3`) | 13 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Valartis Group AG (`valartis-group-ag-1d140c83`) | 13 | NOT_DISCLOSED: benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Frasers Group Plc (`frasers-group-plc-6a13d052`) | 13 | NOT_DISCLOSED: exchange, exchange_segment, fte, isin, listing_status, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target |
| Fresnillo Plc (`fresnillo-plc-c4b75885`) | 13 | NOT_DISCLOSED: fte, listing_date, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Georgina Energy plc (`georgina-energy-plc-7639c631`) | 13 | NOT_DISCLOSED: exchange, exchange_segment, isin, listing_date, listing_status, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, shareholding_requirement |
| Howden Joinery Group Plc (`howden-joinery-group-plc-c3913525`) | 13 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| MONY GROUP PLC (`mony-group-plc-1ebb7a16`) | 13 | NOT_DISCLOSED: exchange_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| National Grid plc (`national-grid-plc-08987e06`) | 13 | NOT_DISCLOSED: exchange_segment, listing_date, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Pets at Home Group Plc (`pets-at-home-group-plc-d9594ce2`) | 13 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_paid, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Plus500 Ltd. (`plus500-ltd-c1762b4f`) | 13 | NOT_DISCLOSED: fte, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Thalassa Holdings Ltd (`thalassa-holdings-ltd-0eaa446d`) | 13 | NOT_DISCLOSED: isin, listing_date, other_names, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, pay_currency, shareholding_requirement, sti_max, sti_target |
| CELYAD ONCOLOGY (`celyad-oncology`) | 13 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| DEME GROUP (`deme-group`) | 13 | NOT_DISCLOSED: other_names, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| TESSENDERLO (`tessenderlo`) | 13 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Adolfo Domínguez, S.A. (`adolfo-dominguez-s-a`) | 13 | NOT_DISCLOSED: exchange_segment, fte, headcount, other_names, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Amper, S.A. (`amper-s-a`) | 13 | NOT_DISCLOSED: accounting_basis, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Realia Business, S.A. (`realia-business-s-a`) | 13 | NOT_DISCLOSED: exchange_segment, shareholding_requirement, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| Cellularline (`cellularline`) | 13 | NOT_DISCLOSED: accounting_basis, fte, lti_granted, lti_target, lti_vested, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Generalfinance (`generalfinance`) | 13 | REPORT_NOT_FOUND: accounting_basis, ebitda, fiscal_year, fte, other_names, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| CSG (`csg`) | 13 | NOT_DISCLOSED: fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target |
| LAKEFRONT BIOTHER. (`lakefront-biother`) | 13 | NOT_DISCLOSED: revenue_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| Aedas Homes, S.A. (`aedas-homes-s-a`) | 13 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Clínica Baviera, S.A. (`clinica-baviera-s-a`) | 13 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, fte, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Hellenic Telecommunications Organization S.A. (`hellenic-telecommunications-organization-s-a`) | 13 | NOT_DISCLOSED: exchange_segment, fte, listing_date, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_target, sti_paid, sti_target |
| MIG Holdings S.A. (`mig-holdings-s-a`) | 13 | NOT_DISCLOSED: exchange_segment, fte, largest_holders, listing_date, pe_stake_5pct, revenue_by_country, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Technical Olympic S.A. (`technical-olympic-s-a`) | 13 | NOT_DISCLOSED: benefits_value, pension_contribution, share_price, staff_by_country, staff_by_segment, ticker, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| AZERION (`azerion`) | 13 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| EURONEXT (`euronext`) | 13 | NOT_DISCLOSED: lti_granted, lti_vested, staff_by_segment, sti_paid |
| Banco Comercial Português, S.A. (`banco-comercial-portugues-s-a`) | 13 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Avolta AG (`avolta-ag`) | 12 | NOT_DISCLOSED: exchange_segment, listing_date, revenue_by_country, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement |
| Alfa Financial Software Holdings PLC (`alfa-financial-software-holdings-plc`) | 12 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_paid |
| CMB.TECH NV (`cmb-tech-nv`) | 12 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max; DERIVATION_INPUT_MISSING: market_cap_band |
| SEB A (`seb-a`) | 12 | NOT_DISCLOSED: listing_date, other_names, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_max, lti_vested, sti_max, sti_paid, sti_target |
| Basellandschaftliche Kantonalbank (`basellandschaftliche-kantonalbank`) | 12 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| CANCOM SE O.N. (`cancom-se-o-n`) | 12 | NOT_DISCLOSED: lti_vested, pension_contribution; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| CVS GROUP PLC (`cvs-group-plc`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_vested, sti_paid, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Odfjell Technology (`odfjell-technology`) | 12 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, share_price, staff_by_country, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Subsea7 (`subsea7`) | 12 | NO_IDENTIFIER: lei; NOT_DISCLOSED: exchange_segment, fte, sti_target, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target |
| Aterian plc (`aterian-plc`) | 12 | REPORT_NOT_FOUND: accounting_basis, ebitda, fiscal_year, fte, headcount, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Atlantic Petroleum (`atlantic-petroleum`) | 12 | NOT_DISCLOSED: exchange_segment, isin, largest_holders, listing_date, pe_stake_5pct, pension_type, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_target, total_remuneration |
| S.D. Standard ETC (`s-d-standard-etc`) | 12 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target |
| Dialight PLC (`dialight-plc`) | 12 | NOT_DISCLOSED: other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| EISEN- UND HUETTENWERKE (`eisen-und-huettenwerke-5b76d547`) | 12 | NOT_DISCLOSED: base_salary, benefits_value, ebitda, lti_granted, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, sti_max, sti_paid, sti_target |
| APG SGA SA (`apg-sga-sa-8679206d`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_max, sti_target |
| Elma Electronic AG (`elma-electronic-ag-e6027e1b`) | 12 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested |
| Rath AG (`rath-ag-9e9ac567`) | 12 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, other_names, staff_by_segment, sti_target |
| KOENIG + BAUER AG ST O.N. (`koenig-bauer-ag-1f22b792`) | 12 | NOT_DISCLOSED: lti_max, lti_vested, pension_contribution |
| NAGARRO SE  NA O.N. (`nagarro-se-9ed14a85`) | 12 | NOT_DISCLOSED: lti_max; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Intershop Holding AG (`intershop-holding-ag-6e9d3cef`) | 12 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Investis Holding SA (`investis-holding-sa-b57723a7`) | 12 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| medmix AG (`medmix-ag-f840dcb1`) | 12 | NOT_DISCLOSED: benefits, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| PLAZZA AG (`plazza-ag-a1578cf1`) | 12 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_paid; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_paid |
| UBS Group AG (`ubs-group-ag-944a2b19`) | 12 | NOT_DISCLOSED: benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_target |
| Zuger Kantonalbank (`zuger-kantonalbank-67b7c3b8`) | 12 | NOT_DISCLOSED: benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Hiscox Ltd (`hiscox-ltd-e0375f35`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_max, sti_target |
| KELLER GROUP PLC (`keller-group-plc-85e72b53`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| ME Group International plc (`me-group-international-plc-174d99a5`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_max, sti_target |
| Mortgage Advice Bureau (Holdings) PLC (`mortgage-advice-bureau-holdings-plc-6818e743`) | 12 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested, shareholding_requirement, sti_target |
| SAINSBURY (J) PLC (`sainsbury-j-plc-5943ac28`) | 12 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| SIG PLC (`sig-plc-36f9635a`) | 12 | NOT_DISCLOSED: isin, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| SSE Plc (`sse-plc-640d28c9`) | 12 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Taylor Maritime Limited (`taylor-maritime-limited-6aeccfd1`) | 12 | NOT_DISCLOSED: benefits, fte, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| WETHERSPOON ( J D ) PLC (`wetherspoon-j-d-plc-f0b40e8d`) | 12 | NOT_DISCLOSED: exchange_segment, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| AB INBEV (`ab-inbev`) | 12 | NOT_DISCLOSED: exchange_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target, total_remuneration |
| IBA (`iba`) | 12 | NOT_DISCLOSED: benefits, other_names; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested |
| MATERIALISE (`materialise`) | 12 | NOT_DISCLOSED: other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_paid, sti_target |
| Ebro Foods, S.A. (`ebro-foods-s-a`) | 12 | NOT_DISCLOSED: exchange_segment, fte, headcount, listing_date, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Inmobiliaria del Sur, S.A. (`inmobiliaria-del-sur-s-a`) | 12 | REPORT_NOT_FOUND: benefits, fiscal_year, fte, other_names, pension_type, revenue_by_country, share_price, shareholding_requirement, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Piraeus Port Authority S.A. (`piraeus-port-authority-s-a`) | 12 | NOT_DISCLOSED: accounting_basis, exchange_segment, fte, largest_holders, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Maire (`maire`) | 12 | NOT_DISCLOSED: largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, revenue_by_country, sti_max, sti_paid, sti_target |
| Seco (`seco`) | 12 | NETWORK_ERROR: accounting_basis, fiscal_year, fte, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| TUBIZE-FIN (`tubize-fin`) | 12 | NOT_DISCLOSED: ebitda, exchange_segment, pension_type, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, sti_max |
| Fomento de Construcciones y Contratas, S.A. (`fomento-de-construcciones-y-contratas-s-a`) | 12 | NOT_DISCLOSED: fte, listing_date, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, sti_target, ticker; DERIVATION_INPUT_MISSING: sector_code; REMUNERATION_REPORT_NOT_READ: aggregate_headcount |
| Prosegur Cash, S.A. (`prosegur-cash-s-a`) | 12 | NOT_DISCLOSED: exchange_segment, fte, largest_holders, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, sub_sector, ticker; DERIVATION_INPUT_MISSING: sector_code |
| Vidrala, S.A. (`vidrala-s-a`) | 12 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, revenue_by_country, role_disclosure, staff_by_segment, ticker |
| Euronext Athens Holding S.A. (`euronext-athens-holding-s-a`) | 12 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, ebitda, largest_holders, ownership_type, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Gens Aurea (`gens-aurea`) | 12 | REPORT_NOT_FOUND: ebitda, exchange_segment, fiscal_year, fte, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| EUROCOMMERCIAL (`eurocommercial`) | 12 | NOT_DISCLOSED: other_names, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, lti_vested, sti_target |
| Grupo Ezentis, S.A. (`grupo-ezentis-s-a`) | 12 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_paid; DERIVATION_INPUT_MISSING: market_cap_band |
| Banco BPM (`banco-bpm`) | 12 | NOT_DISCLOSED: accounting_basis, ebitda, fte, headcount, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| IT Way (`it-way`) | 12 | NOT_DISCLOSED: accounting_basis, exchange_segment, fte, largest_holders, other_names, pe_stake_5pct, revenue_by_country, share_price, shares_outstanding, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band, sector_code |
| Ascom Holding AG (`ascom-holding-ag`) | 11 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_max, sti_target |
| 4IMPRINT GROUP PLC (`4imprint-group-plc`) | 11 | NOT_DISCLOSED: exchange_segment, fte, headcount, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| AMINEX PLC (`aminex-plc`) | 11 | NOT_DISCLOSED: isin, listing_date, revenue_by_country, shareholding_requirement, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Airtel Africa plc (`airtel-africa-plc`) | 11 | NOT_DISCLOSED: fte, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Autotrader Group plc (`autotrader-group-plc`) | 11 | NOT_DISCLOSED: exchange_segment, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_max, sti_paid, sti_target |
| BELIMO Holding AG (`belimo-holding-ag`) | 11 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| BASLER AG O.N. (`basler-ag-o-n`) | 11 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_paid |
| BERTRANDT AG O.N. (`bertrandt-ag-o-n`) | 11 | NOT_DISCLOSED: fiscal_year, fiscal_year_end, lti_granted, lti_target, sti_target |
| British American Tobacco Plc (`british-american-tobacco-plc`) | 11 | NOT_DISCLOSED: exchange_segment, fte, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Stora Enso A (`stora-enso-a`) | 11 | NOT_DISCLOSED: listing_date, other_names, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| Bell Food Group AG (`bell-food-group-ag`) | 11 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested, sti_max |
| Coats Group PLC (`coats-group-plc`) | 11 | NOT_DISCLOSED: exchange_segment, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Cobra Resources plc (`cobra-resources-plc`) | 11 | NOT_DISCLOSED: fte, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: benefits, shareholding_requirement, sti_max, sti_target |
| Coca-Cola HBC AG (`coca-cola-hbc-ag`) | 11 | STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Dar Global PLC (`dar-global-plc`) | 11 | NOT_DISCLOSED: pension_type, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_target |
| MASCHINENFABRIK BERTHOLD HERMLE O.N. VZO (`maschinenfabrik-berthold-hermle-6808fdaf`) | 11 | NOT_DISCLOSED: exchange_segment, lti_max, lti_vested, sti_max, ticker |
| Cham Swiss Properties AG (`cham-swiss-properties-ag-7d9cb227`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Cicor Technologies Ltd. (`cicor-technologies-ltd-39bd9715`) | 11 | NOT_DISCLOSED: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target |
| MCH Group AG (`mch-group-ag-c6fc7898`) | 11 | NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, staff_by_segment, sti_target |
| Metall Zug AG (`metall-zug-ag-7412eb32`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Molecular Partners AG (`molecular-partners-ag-86d659ae`) | 11 | NOT_DISCLOSED: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Sensirion Holding AG (`sensirion-holding-ag-0c2fb93b`) | 11 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution |
| Swiss Life Holding AG (`swiss-life-holding-ag-403064f3`) | 11 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Swiss Prime Site AG (`swiss-prime-site-ag-da6d9b3d`) | 11 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| FISHER (JAMES) & SONS PLC (`fisher-james-sons-plc-1d273817`) | 11 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, sti_paid, sti_target |
| Future Plc (`future-plc-efa5f84f`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_paid, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Genus PLC (`genus-plc-01b59a75`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Grand Vision Media Holdings PLC (`grand-vision-media-holdings-plc-aca75f65`) | 11 | NOT_DISCLOSED: exchange_segment, fte, listing_date, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, shareholding_requirement, total_remuneration |
| Hansard Global Plc (`hansard-global-plc-f13a5b81`) | 11 | NOT_DISCLOSED: isin, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Harena Rare Earths Plc (`harena-rare-earths-plc-229c562b`) | 11 | NOT_DISCLOSED: exchange_segment, lti_granted, pension_contribution, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| IMI PLC (`imi-plc-cbc5827b`) | 11 | STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Man Group plc (`man-group-plc-ff3bca71`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, isin, listing_date, ownership_type, revenue_by_segment, staff_by_country, staff_by_segment |
| Marks and Spencer Group plc (`marks-and-spencer-group-plc-1955eb29`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Nostrum Oil & Gas plc (`nostrum-oil-gas-plc-2662c1d0`) | 11 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_paid, total_remuneration |
| Playtech Plc (`playtech-plc-4d633d69`) | 11 | NOT_DISCLOSED: fiscal_year, lti_granted, lti_target, sti_paid, sti_target |
| RM PLC (`rm-plc-e6d5fda7`) | 11 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, sti_target |
| Rentokil Initial Plc (`rentokil-initial-plc-8eff6540`) | 11 | STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target, total_remuneration |
| SEGRO plc (`segro-plc-83f811d0`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Saga PLC (`saga-plc-3572ddce`) | 11 | NOT_DISCLOSED: exchange_segment, listing_date, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_vested |
| Symphony International Holdings Limited (`symphony-international-holdings-limited-fa241bdf`) | 11 | NOT_DISCLOSED: fte, headcount, other_names, revenue, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| ZOTEFOAMS PLC (`zotefoams-plc-4b8f7aee`) | 11 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| FLUXYS BELGIUM D (`fluxys-belgium-d`) | 11 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| Recticel SA/NV (`recticel`) | 11 | NOT_DISCLOSED: listing_date, lti_basis, lti_max_pct, lti_target_pct, revenue_by_country, revenue_by_segment, sector_code, staff_by_segment |
| Grifols, S.A. (`grifols-s-a`) | 11 | WRONG_YEAR_REPORT: fiscal_year; REPORT_NOT_FOUND: benefits, pension_type; NOT_DISCLOSED: lti_granted, lti_max, lti_target, sti_target |
| Kordellos Ch. Bros S.A. (`kordellos-ch-bros-s-a`) | 11 | NOT_DISCLOSED: base_salary, controlling_owner, fte, ownership_type, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Medicon Hellas S.A. (`medicon-hellas-s-a`) | 11 | NOT_DISCLOSED: base_salary, fte, other_names, pension_contribution, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| GPI (`gpi`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, fte, largest_holders, other_names, ownership_type, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| HAWICK DATA NV (`hawick-data-nv`) | 11 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, shareholding_requirement, sti_target |
| HEINEKEN HOLDING (`heineken-holding`) | 11 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, other_names, pension_contribution, revenue_by_country, staff_by_country, staff_by_segment |
| MKB Nedsense (`mkb-nedsense`) | 11 | NOT_DISCLOSED: exchange_segment, headcount, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Toyota Caetano Portugal, S.A. (`toyota-caetano-portugal-s-a`) | 11 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: sti_target |
| Elve S.A. (`elve-s-a`) | 11 | NOT_DISCLOSED: base_salary, exchange_segment, fte, listing_date, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Softlab (`softlab`) | 11 | NOT_DISCLOSED: accounting_basis, fte, other_names, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band, sector_code |
| ALUMEXX N.V. (`alumexx-n-v`) | 11 | NOT_DISCLOSED: lti_target, lti_vested, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| UMG (`umg`) | 11 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_target, lti_vested, sti_paid, sti_target |
| GBL (`gbl`) | 11 | NOT_DISCLOSED: ebitda, fte, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target, total_remuneration |
| HYLORIS (`hyloris`) | 11 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_vested, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Audax Renovables, S.A. (`audax-renovables-s-a`) | 11 | NOT_DISCLOSED: benefits, lti_granted, lti_vested, pension_type, staff_by_segment, sti_paid, sti_target |
| Prosegur Compañía de Seguridad, S.A. (`prosegur-compania-de-seguridad-s-a`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Applied Nutrition plc (`applied-nutrition-plc`) | 11 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Emak (`emak`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| AMG (`amg`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, lti_granted, ownership_type, pe_stake_5pct |
| BALFOUR BEATTY PLC (`balfour-beatty-plc`) | 10 | NOT_DISCLOSED: exchange_segment, fte, headcount, listing_date, other_names, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Bodycote Plc (`bodycote-plc`) | 10 | NOT_DISCLOSED: exchange_segment, fte, headcount, listing_date, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested |
| BW Offshore Limited (`bw-offshore-limited`) | 10 | NOT_DISCLOSED: exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, lti_max, lti_target, lti_vested, pension_type, shareholding_requirement, sti_target, total_remuneration |
| AIB Group plc (`aib-group-plc`) | 10 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Airtel Mobile Commerce N.V., (`airtel-mobile-commerce-n-v`) | 10 | NOT_DISCLOSED: ebitda, fte, headcount, largest_holders, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, website |
| Ceres Power Holdings PLC (`ceres-power-holdings-plc`) | 10 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Clarkson PLC (`clarkson-plc`) | 10 | NOT_DISCLOSED: listing_date, other_names, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: sti_max, sti_target |
| DIAGEO PLC (`diageo-plc`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| ELEMENTIS PLC (`elementis-plc`) | 10 | NOT_DISCLOSED: exchange_segment, fte, largest_holders, listing_date, other_names, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Eurocell plc (`eurocell-plc`) | 10 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_paid |
| Intea Fastigheter D (`intea-fastigheter-d`) | 10 | NOT_DISCLOSED: fte, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, total_remuneration |
| ALBIS LEASING AG O.N. (`albis-leasing-ag-30344d1d`) | 10 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_paid, total_remuneration |
| EPIGENOMICS AG NA O.N. (`epigenomics-ag-ddb6ea6d`) | 10 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Path2 Hydrogen AG (`path2-hydrogen-ag-4a522574`) | 10 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, revenue_by_country, sti_max, sti_target |
| COLTENE Holding AG (`coltene-holding-ag-8c3c775c`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Frequentis AG (`frequentis-ag-b26b4708`) | 10 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested |
| DRAEGERWERK VZO O.N. (`draegerwerk-be66d9df`) | 10 | NOT_DISCLOSED: lti_max, lti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_vested, sti_max, sti_paid, sti_target |
| LUFTHANSA AG VNA O.N. (`lufthansa-ag-0bc3d92c`) | 10 | NOT_DISCLOSED: exchange_segment, largest_holders, listing_date, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Givaudan SA (`givaudan-sa-b9d48cbe`) | 10 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| IVF HARTMANN Holding AG (`ivf-hartmann-holding-ag-fc38ba38`) | 10 | NOT_DISCLOSED: pension_type, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| Medartis Holding AG (`medartis-holding-ag-4ef02932`) | 10 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Orell Füssli AG (`orell-fussli-ag-c5631ff9`) | 10 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Rieter Holding AG (`rieter-holding-ag-73ac7c64`) | 10 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_paid |
| SKAN Group AG (`skan-group-ag-684bb9fa`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| StarragTornos Group AG (`starragtornos-group-ag-15e3832b`) | 10 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| TEMENOS AG (`temenos-ag-21209ec1`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Thurgauer Kantonalbank (`thurgauer-kantonalbank-3b36a058`) | 10 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| V-ZUG Holding AG (`v-zug-holding-ag-f40cbd57`) | 10 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_target, lti_vested, total_remuneration |
| VP Bank AG (`vp-bank-ag-e661c993`) | 10 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Warteck Invest AG (`warteck-invest-ag-66b36e41`) | 10 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: aggregate_headcount, lti_max, lti_target, lti_vested, sti_target |
| Zug Estates Holding AG (`zug-estates-holding-ag-4947dbda`) | 10 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Haleon plc (`haleon-plc-fbfe0678`) | 10 | NOT_DISCLOSED: isin, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Halfords Group PLC (`halfords-group-plc-f8d1c722`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested, sti_target |
| KERRY GROUP PLC (`kerry-group-plc-56fe152d`) | 10 | NOT_DISCLOSED: exchange_segment, fte, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| LSL Property Services PLC (`lsl-property-services-plc-b9f0b280`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_paid, sti_target |
| Lancashire Holdings Limited (`lancashire-holdings-limited-94cc95db`) | 10 | NOT_DISCLOSED: isin, other_names, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Michael Page plc (`michael-page-plc-f65a03eb`) | 10 | NOT_DISCLOSED: exchange_segment, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| OXFORD INSTRUMENTS PLC (`oxford-instruments-plc-25a1fbdf`) | 10 | NOT_DISCLOSED: exchange_segment, isin, listing_date, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| PORVAIR PLC (`porvair-plc-4e103c62`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Petra Diamonds Limited (`petra-diamonds-limited-5f8d5389`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Prudential PLC (`prudential-plc-c6ad5538`) | 10 | NOT_DISCLOSED: exchange_segment, listing_date, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| R.E.A. HOLDINGS PLC (`r-e-a-holdings-plc-5b9a0020`) | 10 | NOT_DISCLOSED: listing_date, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Raspberry Pi Holdings plc (`raspberry-pi-holdings-plc-d0b387d0`) | 10 | NOT_DISCLOSED: revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| SSP Group PLC (`ssp-group-plc-e4d12504`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| TT ELECTRONICS PLC (`tt-electronics-plc-a0096882`) | 10 | NOT_DISCLOSED: listing_date, other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| The Beauty Tech Group plc (`the-beauty-tech-group-plc-65ff7e12`) | 10 | NOT_DISCLOSED: revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| W.A.G PAYMENT SOLUTIONS PLC (`w-a-g-payment-solutions-plc-44f2e7ea`) | 10 | NOT_DISCLOSED: fte, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| WORKSPACE GROUP PLC (`workspace-group-plc-23f80ffe`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| XAAR PLC (`xaar-plc-44438ac8`) | 10 | NOT_DISCLOSED: exchange_segment, isin, listing_date, revenue_by_country, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| ACKERMANS V.HAAREN (`ackermans-v-haaren`) | 10 | NOT_DISCLOSED: exchange_segment, other_names; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| CIE BOIS SAUVAGE (`cie-bois-sauvage`) | 10 | NOT_DISCLOSED: fte, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Iberdrola, S.A. (`iberdrola-s-a`) | 10 | NOT_DISCLOSED: lti_granted, lti_target, pension_contribution, sti_target |
| Biokarpet S.A. (`biokarpet-s-a`) | 10 | NOT_DISCLOSED: fte, listing_date, share_price, staff_by_country, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, shareholding_requirement |
| Digital Bros (`digital-bros`) | 10 | NOT_DISCLOSED: lti_max, other_names, share_price, staff_by_segment, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| PROSUS (`prosus`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_target |
| SBM OFFSHORE (`sbm-offshore`) | 10 | NOT_DISCLOSED: lti_max, lti_vested; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Impresa - Sociedade Gestora de Participações Sociais, S.A. (`impresa-sociedade-gestora-de-participacoes-sociais-s-a`) | 10 | NOT_DISCLOSED: other_names, share_price, shareholding_requirement, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, pension_contribution, sti_target |
| MELEXIS (`melexis`) | 10 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| MOURY CONSTRUCT (`moury-construct`) | 10 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: sti_max, sti_target, total_remuneration |
| Naturhouse Health, S.A. (`naturhouse-health-s-a`) | 10 | NOT_DISCLOSED: exchange_segment, fte, headcount, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Nyesa Valores Corporación, S.A. (`nyesa-valores-corporacion-s-a`) | 10 | NOT_DISCLOSED: exchange_segment, fte, headcount, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Karelia Tobacco Company Inc. (`karelia-tobacco-company-inc`) | 10 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, pension_type, shareholding_requirement |
| B.F. (`b-f`) | 10 | NOT_DISCLOSED: exchange_segment, lti_target, other_names, pension_type, revenue_by_country, share_price, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| AKZO NOBEL (`akzo-nobel`) | 10 | NOT_DISCLOSED: base_salary, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| BEVER HOLDING (`bever-holding`) | 10 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, role_disclosure, shareholding_requirement |
| CARE PROPERTY INV. (`care-property-inv`) | 10 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| TINC (`tinc`) | 10 | NOT_DISCLOSED: fte, headcount, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Cirsa Enterprises, S.A. (`cirsa-enterprises-s-a`) | 10 | NOT_DISCLOSED: fte, headcount, largest_holders, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Elastron S.A. - Steel Service Centers (`elastron-s-a-steel-service-centers`) | 10 | NOT_DISCLOSED: fte, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| BFF Bank (`bff-bank`) | 10 | NOT_DISCLOSED: largest_holders, lti_target, other_names, pe_stake_5pct, pension_contribution, revenue_by_country, staff_by_segment, sti_max, sti_target |
| Geox (`geox`) | 10 | NOT_DISCLOSED: exchange_segment, fte, headcount, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Ibersol, S.G.P.S., S.A. (`ibersol-s-g-p-s-s-a`) | 10 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_segment, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Martifer SGPS, S.A. (`martifer-sgps-s-a`) | 10 | NOT_DISCLOSED: other_names, revenue_by_country, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: pension_contribution, sti_target |
| Barry Callebaut AG (`barry-callebaut-ag`) | 9 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| BEIERSDORF AG O.N. (`beiersdorf-ag-o-n`) | 9 | NOT_DISCLOSED: fte, lti_granted, lti_target |
| AO World PLC (`ao-world-plc`) | 9 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Bytes Technology Group plc (`bytes-technology-group-plc`) | 9 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, ownership_type, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| CALEDONIA INVESTMENTS PLC (`caledonia-investments-plc`) | 9 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Bellevue Group AG (`bellevue-group-ag`) | 9 | NOT_DISCLOSED: lti_target, lti_vested, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| AJ Bell plc (`aj-bell-plc`) | 9 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Canal+ S.A (`canal-s-a`) | 9 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Basilea Pharmaceutica AG, Allschwil (`basilea-pharmaceutica-ag-allschwil`) | 9 | NOT_DISCLOSED: exchange_segment, fte, lti_vested, revenue_by_country, revenue_by_segment, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested |
| Corpus Resources Plc (`corpus-resources-plc`) | 9 | NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, shareholding_requirement |
| Currys plc (`currys-plc`) | 9 | NOT_DISCLOSED: largest_holders, listing_date, pe_stake_5pct, share_price, shares_outstanding, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted |
| DIPLOMA PLC (`diploma-plc`) | 9 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, staff_by_country |
| Entain Plc (`entain-plc`) | 9 | NOT_DISCLOSED: isin, staff_by_country, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| SCA A (`sca-a`) | 9 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, other_names, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| ALLGEIER SE  NA O.N. (`allgeier-se-9971b49d`) | 9 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| NORCOM INFORMATION TECHNOLOGY INH ON (`norcom-information-technology-2811f08c`) | 9 | NOT_DISCLOSED: lti_granted, lti_max, lti_vested, revenue_by_segment, staff_by_country, staff_by_segment |
| Calida Holding AG (`calida-holding-ag-1793bfba`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| Frauenthal Holding AG (`frauenthal-holding-ag-edd167fb`) | 9 | NOT_DISCLOSED: accounting_basis, largest_holders, listing_date, other_names, pe_stake_5pct, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| Gurktaler AG (`gurktaler-ag-313b0a0d`) | 9 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_segment, staff_by_country, staff_by_segment |
| IVU TRAFFIC TECHN.AG O.N. (`ivu-traffic-techn-ag-020c6212`) | 9 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Huber+Suhner AG (`huber-suhner-ag-11887265`) | 9 | NOT_DISCLOSED: benefits_value, lti_max, lti_target, lti_vested, staff_by_segment, sti_max, sti_target |
| Jungfraubahn Holding AG (`jungfraubahn-holding-ag-90ceddd3`) | 9 | CREDITS_EXHAUSTED: fiscal_year; NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target |
| Kardex Holding AG (`kardex-holding-ag-b5808d3c`) | 9 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_target |
| Kuros Biosciences Ltd. (`kuros-biosciences-ltd-32d9b34e`) | 9 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_target |
| Montana Aerospace AG (`montana-aerospace-ag-bc5706d8`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, shareholding_requirement |
| R&S Group Holding AG (`r-s-group-holding-ag-8cdcd57a`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Stadler Rail AG (`stadler-rail-ag-ddc4f964`) | 9 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_max, lti_target, lti_vested, sti_target |
| Straumann Holding AG (`straumann-holding-ag-d8e91d7f`) | 9 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| Swiss Re AG (`swiss-re-ag-6528d850`) | 9 | NOT_DISCLOSED: exchange_segment, isin, lti_granted, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_target |
| Vetropack Holding AG (`vetropack-holding-ag-3a954192`) | 9 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_max, lti_target, lti_vested |
| Ypsomed Holding AG (`ypsomed-holding-ag-9cb8acfe`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| Zurich Insurance Group AG (`zurich-insurance-group-ag-d14f6a93`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, pension_contribution, sti_target |
| Ferrexpo plc (`ferrexpo-plc-5653b4e7`) | 9 | NOT_DISCLOSED: other_names, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Fevara plc (`fevara-plc-92307031`) | 9 | NOT_DISCLOSED: fte, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| GRAFTON GROUP PLC (`grafton-group-plc-79b8acde`) | 9 | NOT_DISCLOSED: exchange_segment, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| GSTechnologies Ltd (`gstechnologies-ltd-43df31ee`) | 9 | NOT_DISCLOSED: isin, listing_date, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits |
| Gem Diamonds Limited (`gem-diamonds-limited-a386ff99`) | 9 | NOT_DISCLOSED: isin, listing_date, other_names; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| Glencore Plc (`glencore-plc-e07e9a2a`) | 9 | NOT_DISCLOSED: fte, isin, listing_date, staff_by_country, staff_by_segment, ticker; REMUNERATION_REPORT_NOT_READ: sti_max, sti_paid, sti_target |
| GlobalData Plc (`globaldata-plc-8552de44`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Hill & Smith PLC (`hill-smith-plc-f6cb355e`) | 9 | NOT_DISCLOSED: listing_date, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Hilton Food Group Plc (`hilton-food-group-plc-3a56b109`) | 9 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, pension_contribution, sti_target |
| ICG plc (`icg-plc-b82eb2fc`) | 9 | NOT_DISCLOSED: exchange_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target |
| Informa plc (`informa-plc-40c3a060`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| International Consolidated Airlines Group S.A. (`international-consolidated-airlines-group-s-a-afe59a89`) | 9 | NOT_DISCLOSED: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| LAW DEBENTURE CORPORATION PLC (THE) (`law-debenture-corporation-plc-the-d1b5e75c`) | 9 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| LEGAL & GENERAL GROUP PLC (`legal-general-group-plc-c48e212e`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, sti_max |
| MJ Gleeson Plc (`mj-gleeson-plc-f432eba6`) | 9 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| Marston's Plc (`marston-s-plc-1442ebdc`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Metro Bank Holdings plc (`metro-bank-holdings-plc-3ac1d88a`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Ninety One plc (`ninety-one-plc-23209795`) | 9 | NOT_DISCLOSED: exchange_segment, revenue_by_segment, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| PHAROS ENERGY PLC (`pharos-energy-plc-c7b796c5`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| S4 Capital PLC (`s4-capital-plc-c1328a0a`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| SEVERN TRENT PLC (`severn-trent-plc-2f585ef6`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| SMITH & NEPHEW PLC (`smith-nephew-plc-c9e41729`) | 9 | NOT_DISCLOSED: fte, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| Secure Trust Bank PLC (`secure-trust-bank-plc-f393d9db`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Sirius Real Estate Limited (`sirius-real-estate-limited-9190d4f5`) | 9 | NOT_DISCLOSED: other_names, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_target |
| Softcat Plc (`softcat-plc-d9d4c66c`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| TP ICAP Group plc (`tp-icap-group-plc-4a64e99a`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Wise Group plc (`wise-group-plc-0765a8ab`) | 9 | NOT_DISCLOSED: fte, lti_vested, revenue_by_segment, share_price, shareholding_requirement, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| XP Power Ltd (`xp-power-ltd-2507bfe3`) | 9 | NOT_DISCLOSED: isin, lti_target, lti_vested, staff_by_segment, ticker |
| XPS Pensions Group plc (`xps-pensions-group-plc-bf3a20e5`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| ZIGUP plc (`zigup-plc-d5f0480d`) | 9 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| ELIA GROUP (`elia-group`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Árima Real Estate SOCIMI, S.A. (`arima-real-estate-socimi-s-a`) | 9 | NOT_DISCLOSED: other_names, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, shareholding_requirement, staff_by_country, staff_by_segment, ticker |
| Quest Holdings S.A. (`quest-holdings-s-a`) | 9 | NOT_DISCLOSED: fte, share_price, staff_by_segment, sti_max, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Aeroporto Guglielmo Marconi di Bologna (`aeroporto-guglielmo-marconi-di-bologna`) | 9 | NOT_DISCLOSED: fte, headcount, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| CABKA (`cabka`) | 9 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_paid |
| EASE2PAY NV (`ease2pay-nv`) | 9 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| CAMPINE (`campine`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| NYXOAH (`nyxoah`) | 9 | NOT_DISCLOSED: lti_granted, lti_max, lti_vested, sti_max, total_remuneration |
| ORANGE BELGIUM (`orange-belgium`) | 9 | NOT_DISCLOSED: exchange_segment, fte, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested, sti_max, sti_target |
| Neodecortech (`neodecortech`) | 9 | NOT_DISCLOSED: accounting_basis, fte, other_names, revenue_by_country, revenue_by_segment, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Zest (`zest`) | 9 | NOT_DISCLOSED: exchange_segment, fte, headcount, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| AVANTIUM (`avantium`) | 9 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, sti_max, sti_target |
| SIF HOLDING (`sif-holding`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Grupo Média Capital, SGPS, S.A. (`grupo-media-capital-sgps-s-a`) | 9 | NOT_DISCLOSED: revenue_by_country, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, shareholding_requirement, sti_paid, sti_target, total_remuneration |
| Tubacex, S.A. (`tubacex-s-a`) | 9 | NOT_DISCLOSED: exchange_segment, fte, listing_date, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: sector_code |
| E. Pairis S.A. (`e-pairis-s-a`) | 9 | NOT_DISCLOSED: fte, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Met.Extra Group (`met-extra-group`) | 9 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, pension_type, shareholding_requirement |
| Rai Way (`rai-way`) | 9 | NOT_DISCLOSED: fte, lti_vested, other_names, revenue_by_country, shares_outstanding, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Unidata (`unidata`) | 9 | NOT_DISCLOSED: fte, other_names, pe_stake_5pct, share_price, shares_outstanding, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| AHOLD DEL (`ahold-del`) | 9 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| ENVIPCO HOLDING (`envipco-holding`) | 9 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| NEDAP (`nedap`) | 9 | NOT_DISCLOSED: benefits_value, lti_granted, lti_vested, sti_paid |
| SRV Group Plc (`T0531`) | 9 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target, total_remuneration |
| Amrize Ltd (`amrize-ltd`) | 8 | NOT_DISCLOSED: exchange_segment, fte, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_target |
| Bachem Holding AG (`bachem-holding-ag`) | 8 | NOT_DISCLOSED: benefits, exchange_segment, lti_vested, revenue_by_segment, staff_by_segment, sti_max |
| AIQ Limited (`aiq-limited`) | 8 | NOT_DISCLOSED: listing_date, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, pension_type |
| ALTYNGOLD PLC (`altyngold-plc`) | 8 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, pension_contribution, shareholding_requirement |
| ASSOCIATED BRITISH FOODS PLC (`associated-british-foods-plc`) | 8 | NOT_DISCLOSED: listing_date, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution |
| Aston Martin Lagonda Global Holdings PLC (`aston-martin-lagonda-global-holdings-plc`) | 8 | NOT_DISCLOSED: fte, headcount, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_vested |
| CRANSWICK PLC (`cranswick-plc`) | 8 | NOT_DISCLOSED: listing_date, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target |
| Capital Limited (`capital-limited`) | 8 | NOT_DISCLOSED: fte, isin, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, sti_paid |
| Hermana Holding (`hermana-holding`) | 8 | NOT_DISCLOSED: other_names, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Stora Enso R (`stora-enso-r`) | 8 | NOT_DISCLOSED: listing_date, other_names, staff_by_segment, ultimate_parent; NO_IDENTIFIER: lei; REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| African Pioneer Plc (`african-pioneer-plc`) | 8 | NOT_DISCLOSED: isin, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Ashtead Technology Holdings plc (`ashtead-technology-holdings-plc`) | 8 | NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Big Yellow Group plc (`big-yellow-group-plc`) | 8 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| CAPITA PLC (`capita-plc`) | 8 | NOT_DISCLOSED: listing_date, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| CASTINGS PLC (`castings-plc`) | 8 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: sti_target |
| Domino's Pizza Group Plc (`domino-s-pizza-group-plc`) | 8 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, listing_date, ownership_type, pe_stake_5pct, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted |
| United Eco Solutions AG (`united-eco-solutions-ag-44c5756c`) | 8 | NOT_DISCLOSED: ebitda, listing_date, revenue_by_segment, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| PEARL GOLD AG (`pearl-gold-ag-da4e9b62`) | 8 | NOT_DISCLOSED: other_names, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Telekom Austria AG (`telekom-austria-ag-62fec5fa`) | 8 | NOT_DISCLOSED: benefits_value, lti_granted, lti_target, pension_contribution, sti_target; REMUNERATION_REPORT_NOT_READ: lti_target, sti_max, sti_target |
| Heid Maschinenfabrik AG (`heid-maschinenfabrik-ag-72bb31c5`) | 8 | NOT_DISCLOSED: fte, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| CHERRY SE (`cherry-se-57089b55`) | 8 | NOT_DISCLOSED: lti_granted, lti_vested, pension_contribution, sti_paid |
| SCHOTT Pharma AG & Co. KGaA (`schott-pharma-ag-co-kgaa-26f01ea5`) | 8 | NOT_DISCLOSED: benefits_value, fiscal_year, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Infracore SA (`infracore-sa-b3b0dcce`) | 8 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| Phoenix Mecano AG (`phoenix-mecano-ag-d882ab5c`) | 8 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: lti_vested, sti_max, sti_target |
| SFS Group AG (`sfs-group-ag-f427427a`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| St.Galler Kantonalbank AG (`st-galler-kantonalbank-ag-ba864955`) | 8 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target |
| Zehnder Group AG (`zehnder-group-ag-125a701c`) | 8 | NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_max, lti_vested, sti_target |
| FULLER, SMITH & TURNER PLC (`fuller-smith-turner-plc-0314e97e`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| First Class Metals PLC (`first-class-metals-plc-ae225da0`) | 8 | NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| GENFLOW BIOSCIENCES PLC (`genflow-biosciences-plc-e8a62139`) | 8 | NOT_DISCLOSED: isin, listing_date, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, shareholding_requirement |
| GOODWIN PLC (`goodwin-plc-9f507dfb`) | 8 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| GREAT PORTLAND ESTATES PLC (`great-portland-estates-plc-808a0fed`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| IG Group Holdings Plc (`ig-group-holdings-plc-702b4563`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| INCHCAPE PLC (`inchcape-plc-ea221c9f`) | 8 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Ithaca Energy plc (`ithaca-energy-plc-c6840a94`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| JOHNSON MATTHEY PLC (`johnson-matthey-plc-e14061cd`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| Paragon Banking Group Plc (`paragon-banking-group-plc-4e0326d5`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| PureTech Health PLC (`puretech-health-plc-df8e539a`) | 8 | NOT_DISCLOSED: revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid |
| RC365 Holding plc (`rc365-holding-plc-1f4ebdbd`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Rathbones Group Plc (`rathbones-group-plc-272d1adc`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| SAVILLS PLC (`savills-plc-159e730d`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_max |
| STANDARD CHARTERED PLC (`standard-chartered-plc-4f4cc096`) | 8 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| Smiths Group Plc (`smiths-group-plc-74ee79d4`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| Synthomer Plc (`synthomer-plc-3c60ceb4`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| TRAVIS PERKINS PLC (`travis-perkins-plc-53aadfa6`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| Telecom plus Plc (`telecom-plus-plc-64a59f0e`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| The Sage Group Plc (`the-sage-group-plc-a2e841b0`) | 8 | NOT_DISCLOSED: exchange_segment, isin, listing_date, other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| United Utilities Group Plc (`united-utilities-group-plc-4e52d704`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| YOUNG & CO'S BREWERY PLC (`young-co-s-brewery-plc-dea1760d`) | 8 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target |
| Interwood-Xylemporia A.T.E.N.E. (`interwood-xylemporia-a-t-e-n-e`) | 8 | NOT_DISCLOSED: fte, listing_date, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Jumbo SA (`jumbo`) | 8 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: share_price, shareholding_requirement; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: sti_max, sti_paid, sti_target, total_remuneration |
| Lampsa Hellenic Hotels S.A. (`lampsa-hellenic-hotels-s-a`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Banco di Desio e della Brianza (`banco-di-desio-e-della-brianza`) | 8 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| NSI N.V. (`nsi-n-v`) | 8 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| IMMOBEL (`immobel`) | 8 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_vested, pension_contribution, sti_paid |
| SPADEL (`spadel`) | 8 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| Bankinter, S.A. (`bankinter-s-a`) | 8 | NOT_DISCLOSED: benefits_value, lti_granted, lti_vested, pension_contribution, revenue_by_segment, ticker, website |
| Miquel y Costas & Miquel, S.A. (`miquel-y-costas-miquel-s-a`) | 8 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, largest_holders, other_names, ownership_type, pe_stake_5pct, staff_by_country, staff_by_segment |
| Vogiatzoglou Systems S.A. (`vogiatzoglou-systems-s-a`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Enervit (`enervit`) | 8 | NOT_DISCLOSED: accounting_basis, exchange_segment, fte, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Poste Italiane (`poste-italiane`) | 8 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| Valsoia (`valsoia`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment, share_price, shares_outstanding, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| GREEN EARTH GROUP (`green-earth-group`) | 8 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: benefits; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| QEV (`qev`) | 8 | NOT_DISCLOSED: exchange_segment, fte, other_names, pension_type, role_disclosure, shareholding_requirement, staff_by_country, staff_by_segment |
| Montebalito, S.A. (`montebalito-s-a`) | 8 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, other_names, pension_contribution, staff_by_segment, ticker, total_remuneration |
| Alpha Real Estate Services S.A. (`alpha-real-estate-services-s-a`) | 8 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| J. & B. Ladenis Bros S.A. - Minerva - Knitwear Manufacturing Company (`j-b-ladenis-bros-s-a-minerva-knitwear-manufacturing-company`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Hera (`hera`) | 8 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, role_disclosure, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Philogen (`philogen`) | 8 | NOT_DISCLOSED: fte, headcount, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Kendrion N.V. (`kendrion`) | 8 | NOT_DISCLOSED: exchange_segment, fte; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_max_pct, total_remuneration |
| OCI (`oci`) | 8 | NOT_DISCLOSED: exchange_segment, fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution, sti_max, sti_paid, sti_target |
| Sport Lisboa e Benfica - Futebol, SAD (`sport-lisboa-e-benfica-futebol-sad`) | 8 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Ashmore Group Plc (`ashmore-group-plc`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_vested, sti_max, sti_target |
| Cadogan Energy Solutions plc (`cadogan-energy-solutions-plc`) | 7 | NOT_DISCLOSED: listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Carclo PLC (`carclo-plc`) | 7 | NOT_DISCLOSED: listing_date, other_names; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| EuroTeleSites AG (`eurotelesites-ag`) | 7 | NOT_DISCLOSED: lti_vested; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Accelleron Industries AG (`accelleron-industries-ag`) | 7 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_max, sti_target |
| Berner Kantonalbank AG (`berner-kantonalbank-ag`) | 7 | NOT_DISCLOSED: lti_max, lti_target, lti_vested, sti_target |
| SSAB B (`ssab-b`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| AVIVA PLC (`aviva-plc`) | 7 | NOT_DISCLOSED: listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| COSTAIN GROUP PLC (`costain-group-plc`) | 7 | NOT_DISCLOSED: exchange_segment, listing_date, other_names; REMUNERATION_REPORT_NOT_READ: lti_granted, sti_target |
| UIE (`uie`) | 7 | NOT_DISCLOSED: fte, lti_max, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_target |
| Computacenter Plc (`computacenter-plc`) | 7 | NOT_DISCLOSED: exchange_segment, listing_date, other_names; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| ConvaTec Group Plc (`convatec-group-plc`) | 7 | NOT_DISCLOSED: exchange_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Critical Metals Plc (`critical-metals-plc`) | 7 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type |
| Critical Mineral Resources Plc (`critical-mineral-resources-plc`) | 7 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, shareholding_requirement |
| Dr. Martens plc (`dr-martens-plc`) | 7 | NOT_DISCLOSED: ebitda, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| BIJOU BRIGITTE O.N. (`bijou-brigitte-c3387b07`) | 7 | NOT_DISCLOSED: exchange_segment, largest_holders, other_names, pe_stake_5pct, staff_by_country, staff_by_segment, ticker |
| KHD HUMBOLDT WEDAG O.N. (`khd-humboldt-wedag-eff61cda`) | 7 | NOT_DISCLOSED: ebitda, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| MATERNUS-KLINIKEN AG O.N. (`maternus-kliniken-ag-fe2ae118`) | 7 | NOT_DISCLOSED: listing_date, lti_max, lti_target, other_names, pension_type, sti_max, sti_target |
| MAX AUTOMATION SE NA O.N. (`max-automation-se-e7586bc1`) | 7 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, sti_target |
| AGRANA Beteiligungs-AG (`agrana-beteiligungs-ag-60d4466c`) | 7 | NOT_DISCLOSED: exchange_segment, largest_holders, other_names, pe_stake_5pct, share_price, website; DERIVATION_INPUT_MISSING: market_cap_band |
| CPI Europe AG (`cpi-europe-ag-27dac1eb`) | 7 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| PARAGON KGAA  INH O.N. (`paragon-kgaa-7616d267`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| SIEMENS HEALTH.AG NA O.N. (`siemens-health-ag-1a42fb66`) | 7 | NOT_DISCLOSED: exchange_segment, largest_holders, other_names, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Interroll Holding AG (`interroll-holding-ag-ef2328b8`) | 7 | NOT_DISCLOSED: aggregate_headcount, lti_granted, lti_target, lti_vested, pension_type, sti_target |
| Lonza Group AG (`lonza-group-ag-e4f248d2`) | 7 | NOT_DISCLOSED: listing_date, lti_target, lti_vested, staff_by_country, staff_by_segment, sti_target |
| SoftwareOne Holding AG (`softwareone-holding-ag-ee2860ae`) | 7 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| Ferro-Alloy Resources Limited (`ferro-alloy-resources-limited-e5e70579`) | 7 | NOT_DISCLOSED: isin, other_names, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, shareholding_requirement |
| First Tin PLC (`first-tin-plc-9086dd77`) | 7 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets; REMUNERATION_REPORT_NOT_READ: role_disclosure, shareholding_requirement |
| HALMA PLC (`halma-plc-9844443d`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| HIDONG ESTATE PLC (`hidong-estate-plc-cc203b38`) | 7 | NETWORK_ERROR: listing_date, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets |
| Integrated Diagnostics Holdings plc (`integrated-diagnostics-holdings-plc-b28b60df`) | 7 | NOT_DISCLOSED: isin, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| Luceco plc (`luceco-plc-1431e7e2`) | 7 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, sti_target, total_remuneration |
| NatWest Group Plc (`natwest-group-plc-0cca2e57`) | 7 | NOT_DISCLOSED: isin, listing_date, ticker; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| QinetiQ Group PLC (`qinetiq-group-plc-f5a9622e`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| Reach plc (`reach-plc-e8816dd8`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Record PLC (`record-plc-8e9102d2`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_paid, sti_target |
| Solvonis Therapeutics Plc (`solvonis-therapeutics-plc-6f6b5d21`) | 7 | NOT_DISCLOSED: listing_date, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, pension_type |
| Tharisa plc (`tharisa-plc-f4ea0c2f`) | 7 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| The Magnum Ice Cream Company N.V. (`the-magnum-ice-cream-company-n-v-6d471687`) | 7 | NOT_DISCLOSED: exchange_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, pension_contribution |
| WEIR PLC (`weir-plc-2d38cf63`) | 7 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Wizz Air Holdings plc (`wizz-air-holdings-plc-fca22f4f`) | 7 | NOT_DISCLOSED: isin, other_names, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_target |
| evoke plc (`evoke-plc-5c77d1d2`) | 7 | NOT_DISCLOSED: fte, isin, ticker; REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target |
| MONTEA (`montea`) | 7 | NOT_DISCLOSED: benefits; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_target |
| WDP (`wdp`) | 7 | NOT_DISCLOSED: exchange_segment, revenue_by_segment, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Athens International Airport S.A. (`athens-international-airport-s-a`) | 7 | NOT_DISCLOSED: fte, lti_vested, other_names, revenue_by_country, staff_by_country, staff_by_segment, ticker |
| Domiki Kritis S.A. (`domiki-kritis-s-a`) | 7 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Unibios Holdings S.A. (`unibios-holdings-s-a`) | 7 | NOT_DISCLOSED: fte, listing_date, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Acinque (`acinque`) | 7 | DERIVATION_INPUT_MISSING: market_cap_band, sector_code; NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, share_price, staff_by_segment |
| S.S. Lazio (`s-s-lazio`) | 7 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Unipol (`unipol`) | 7 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, revenue_by_country, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| PHILIPS KON (`philips-kon`) | 7 | NOT_DISCLOSED: exchange_segment, lti_granted, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Corticeira Amorim, S.G.P.S., S.A. (`corticeira-amorim-s-g-p-s-s-a`) | 7 | NOT_DISCLOSED: exchange_segment, fte, headcount, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| Pharol, SGPS, S.A. (`pharol-sgps-s-a`) | 7 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| IEP INVEST (`iep-invest`) | 7 | NOT_DISCLOSED: benefits, pension_type, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, total_remuneration |
| CIE Automotive, S.A. (`cie-automotive-s-a`) | 7 | NOT_DISCLOSED: accounting_basis, exchange_segment, fte, largest_holders, other_names, pe_stake_5pct, staff_by_segment |
| Attica Publications S.A. (`attica-publications-s-a`) | 7 | NOT_DISCLOSED: fte, listing_date, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| AVE S.A. (`ave-s-a`) | 7 | NOT_DISCLOSED: benefits, fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Evropi Holdings Societe Anonyme (`evropi-holdings-societe-anonyme`) | 7 | NOT_DISCLOSED: fte, pension_type, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Aquafil (`aquafil`) | 7 | NOT_DISCLOSED: accounting_basis, fte, other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Autostrade Meridionali (`autostrade-meridionali`) | 7 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| LAVIDE HOLDING (`lavide-holding`) | 7 | NOT_DISCLOSED: exchange_segment, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| SOLVAC (`solvac`) | 7 | NOT_DISCLOSED: ebitda, other_names, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment |
| Unicaja Banco, S.A. (`unicaja-banco-s-a`) | 7 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker |
| Daios Plastics S.A. (`daios-plastics-s-a`) | 7 | NOT_DISCLOSED: fte, other_names, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Optima bank S.A. (`optima-bank-s-a`) | 7 | NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Revoil S.A. (`revoil-s-a`) | 7 | NOT_DISCLOSED: fte, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Thrace Plastics Holding Company S.A. (`thrace-plastics-holding-company-s-a`) | 7 | NOT_DISCLOSED: fte, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: role_disclosure, shareholding_requirement |
| Altea Green Power (`altea-green-power`) | 7 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Tessellis (`tessellis`) | 7 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, role_disclosure, shareholding_requirement |
| HYDRATEC (`hydratec`) | 7 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Estoril Sol, SGPS, S.A. (`estoril-sol-sgps-s-a`) | 7 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement, sti_target |
| Nilfisk Holding A/S (`T0149`) | 7 | NOT_DISCLOSED: aggregate_headcount, pension_contribution; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, pension_contribution |
| Otello Corp ASA (`T0325`) | 7 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Aberdeen Group plc (`aberdeen-group-plc`) | 6 | NOT_DISCLOSED: exchange_segment, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Admiral Group PLC (`admiral-group-plc`) | 6 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| BT Group plc (`bt-group-plc`) | 6 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, revenue_by_country, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Baltic Classifieds Group PLC (`baltic-classifieds-group-plc`) | 6 | NOT_DISCLOSED: other_names, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| CENTRICA PLC (`centrica-plc`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_paid; STATED_IN_OTHER_FORM: lti_granted |
| AMAROQ LTD. (`amaroq-ltd`) | 6 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| Acceler8 Ventures PLC (`acceler8-ventures-plc`) | 6 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, role_disclosure, staff_by_country, staff_by_segment |
| AstraZeneca PLC (`astrazeneca-plc`) | 6 | NOT_DISCLOSED: exchange_segment, fte; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| BUNZL PLC (`bunzl-plc`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Bystronic AG (`bystronic-ag`) | 6 | NOT_DISCLOSED: exchange_segment, revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_vested |
| Conduit Holdings Limited (`conduit-holdings-limited`) | 6 | NOT_DISCLOSED: isin, other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Drax Group PLC (`drax-group-plc`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Everest Global PLC (`everest-global-plc`) | 6 | DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, shareholding_requirement |
| ACCENTRO REAL ESTATE AG  O.N. (`accentro-real-estate-ag-fbdf101b`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| NEXR TECHNOLOGIES SE  INH O.N. (`nexr-technologies-se-d1999a2e`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Planoptik AG (`planoptik-ag-9429909d`) | 6 | NOT_DISCLOSED: other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| TC UNTERHALTUNGSELEKTRONIK (`tc-unterhaltungselektronik-7628c15f`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Compagnie Financière Richemont SA (`compagnie-financiere-richemont-sa-060892f5`) | 6 | NOT_DISCLOSED: benefits_value, lti_vested |
| Curatis Holding AG (`curatis-holding-ag-adc33085`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| Porr AG (`porr-ag-127fa41a`) | 6 | NOT_DISCLOSED: accounting_basis, fte, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| DT.PFANDBRIEFBK AG (`dt-pfandbriefbk-ag-71e35702`) | 6 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| KSB SE+CO.KGAA  ST O.N. (`ksb-se-co-kgaa-22d5b1d9`) | 6 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_vested, sti_max |
| Groupe Minoteries SA (`groupe-minoteries-sa-11276f01`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Highlight Event and Entertainment AG (`highlight-event-and-entertainment-ag-de285c44`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Klingelnberg AG (`klingelnberg-ag-d32e6349`) | 6 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| Leclanché SA (`leclanche-sa-29b435c9`) | 6 | DOCUMENT_UNREADABLE: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Liechtensteinische Landesbank AG (`liechtensteinische-landesbank-ag-53271b6c`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Meier Tobler Group AG (`meier-tobler-group-ag-f96a3151`) | 6 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, shareholding_requirement, sti_target |
| Mikron Holding AG (`mikron-holding-ag-0842218f`) | 6 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| Mobimo Holding AG (`mobimo-holding-ag-df63dd1a`) | 6 | DOCUMENT_UNREADABLE: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| naturenergie holding AG (`naturenergie-holding-ag-a1be2274`) | 6 | NOT_DISCLOSED: lti_max, lti_target, lti_vested |
| Romande Energie Holding SA (`romande-energie-holding-sa-3dac8f90`) | 6 | DOCUMENT_UNREADABLE: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Schweizerische Nationalbank (`schweizerische-nationalbank-e298a12f`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| SMG Swiss Marketplace Group Holding AG (`smg-swiss-marketplace-group-holding-ag-40385dff`) | 6 | NOT_DISCLOSED: exchange_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_target, lti_vested |
| Sonova Holding AG (`sonova-holding-ag-e87e288d`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Swissquote Group Holding Ltd (`swissquote-group-holding-ltd-8a2aaa88`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| Forterra plc (`forterra-plc-101232a7`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Foxtons Group Plc (`foxtons-group-plc-1852b951`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, lti_vested, pension_contribution |
| GAMMA COMMUNICATIONS PLC (`gamma-communications-plc-4deb67ef`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| GREGGS PLC (`greggs-plc-5347e6c0`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Genuit Group plc (`genuit-group-plc-d097219b`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| HUNTING PLC (`hunting-plc-1f6cc394`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| Harbour Energy PLC (`harbour-energy-plc-7a9017f1`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Hemogenyx Pharmaceuticals Plc (`hemogenyx-pharmaceuticals-plc-ff627795`) | 6 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| ICFG Limited (`icfg-limited-cfbafea2`) | 6 | NOT_DISCLOSED: fte, isin, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| IMPERIAL BRANDS PLC (`imperial-brands-plc-323b70dc`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Ibstock plc (`ibstock-plc-81ff3340`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| Investec PLC (`investec-plc-422fa59c`) | 6 | NOT_DISCLOSED: exchange_segment, fte, other_names; REMUNERATION_REPORT_NOT_READ: shareholding_requirement, sti_max, sti_target |
| JD Sports Fashion Plc (`jd-sports-fashion-plc-bb0972c8`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Jupiter Fund Management PLC (`jupiter-fund-management-plc-fdbf14df`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Land Securities Group PLC (`land-securities-group-plc-07e79f8d`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| Liontrust Asset Management PLC (`liontrust-asset-management-plc-0a50daee`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| MACFARLANE GROUP PLC (`macfarlane-group-plc-be6437b7`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| MITIE GROUP PLC (`mitie-group-plc-78834590`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| MORGAN SINDALL GROUP PLC (`morgan-sindall-group-plc-a9def688`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_paid |
| Melrose Industries Plc (`melrose-industries-plc-2473b10a`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_target |
| Mondi plc (`mondi-plc-b3f2e211`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_target |
| Moonpig Group plc (`moonpig-group-plc-1a2a5dc2`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_paid |
| Motorpoint Group plc (`motorpoint-group-plc-a642e064`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, sti_target |
| NCC Group PLC (`ncc-group-plc-ef9a927a`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Nuformix plc (`nuformix-plc-98385a38`) | 6 | NOT_DISCLOSED: listing_date, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Ocado Group Plc (`ocado-group-plc-87573c24`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| PEARSON PLC (`pearson-plc-0f5eb5e5`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Quilter plc (`quilter-plc-fd79ebd8`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| Reckitt Benckiser Group Plc (`reckitt-benckiser-group-plc-06559416`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| Rightmove Plc (`rightmove-plc-f30003db`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| SMART (J.) & CO. (CONTRACTORS) PLC (`smart-j-co-contractors-plc-5d0db364`) | 6 | NOT_DISCLOSED: exchange_segment, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| STV Group PLC (`stv-group-plc-8c122da5`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| Serica Energy plc (`serica-energy-plc-4b22024a`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target |
| Standard Life plc (`standard-life-plc-77687025`) | 6 | NOT_DISCLOSED: fte, listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| TOPPS TILES PLC (`topps-tiles-plc-85c83f1d`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, sti_paid |
| TULLOW OIL PLC (`tullow-oil-plc-22ae25bd`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| The British Land Company PLC (`the-british-land-company-plc-ff87bb98`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| The Gym Group plc (`the-gym-group-plc-ddd9174c`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| VICTREX PLC (`victrex-plc-88643903`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Videndum plc (`videndum-plc-a3c6fcc6`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Volex plc (`volex-plc-4ceba090`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Volution Group plc (`volution-group-plc-111343a8`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| WH Smith PLC (`wh-smith-plc-c56b3bfb`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| WILMINGTON PLC (`wilmington-plc-55c4248b`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Whitbread plc (`whitbread-plc-5a7a51cc`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| World Chess plc (`world-chess-plc-fa996740`) | 6 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| VGP (`vgp`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| Cleop (`cleop`) | 6 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| Soltec Power Holdings, S.A. (`soltec-power-holdings-s-a`) | 6 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker |
| Evrofarma SA (`evrofarma-sa`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Assicurazioni Generali (`assicurazioni-generali`) | 6 | NOT_DISCLOSED: fte, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Beewize (`beewize`) | 6 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| The Italian Sea Group (`the-italian-sea-group`) | 6 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| ALMUNDA PRO NV (`almunda-pro-nv`) | 6 | NOT_DISCLOSED: exchange_segment, other_names, share_price, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| ARCADIS (`arcadis`) | 6 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, pension_contribution, sti_paid |
| BAM GROEP KON (`bam-groep-kon`) | 6 | NOT_DISCLOSED: exchange_segment, lti_vested, pe_stake_5pct, sti_paid |
| Almirall, S.A. (`almirall-s-a`) | 6 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_segment, staff_by_country, staff_by_segment, ticker |
| Línea Directa Aseguradora, S.A., Compañía de Seguros y Reaseguros (`linea-directa-aseguradora-s-a-compania-de-seguros-y-reaseguros`) | 6 | NOT_DISCLOSED: ebitda, fte, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Sacyr, S.A. (`sacyr-s-a`) | 6 | NOT_DISCLOSED: fte, listing_date, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| Dromeas SA (`dromeas-sa`) | 6 | NOT_DISCLOSED: fte, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| EL. D. Mouzakis S.A. (`el-d-mouzakis-s-a`) | 6 | NOT_DISCLOSED: fte, other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Lanakam S.A. (`lanakam-s-a`) | 6 | NOT_DISCLOSED: fte, listing_date, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Loulis Food Ingredients S.A. (`loulis-food-ingredients-s-a`) | 6 | NOT_DISCLOSED: fte, listing_date, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| N. Varveris-Moda Bagno S.A. (`n-varveris-moda-bagno-s-a`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Cairo Communication (`cairo-communication`) | 6 | NOT_DISCLOSED: fte, other_names, pe_stake_5pct, revenue_by_country, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Technoprobe (`technoprobe`) | 6 | NOT_DISCLOSED: other_names, revenue_by_segment, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Toscana Aeroporti (`toscana-aeroporti`) | 6 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, revenue_by_country, staff_by_country, staff_by_segment |
| FLORIDIENNE (`floridienne`) | 6 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: sti_target |
| KBC ANCORA (`kbc-ancora`) | 6 | NOT_DISCLOSED: fte, headcount, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Bodegas Riojanas, S.A. (`bodegas-riojanas-s-a`) | 6 | NOT_DISCLOSED: lti_max, pension_contribution, staff_by_country, staff_by_segment, sti_target, ticker |
| Elton International Trading Company S.A. (`elton-international-trading-company-s-a`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Iktinos Hellas S.A. Greek Marble Industry Technical and Touristic Company (`iktinos-hellas-s-a-greek-marble-industry-technical-and-touristic-company`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Mathios Refractories S.A. (`mathios-refractories-s-a`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Cy4gate (`cy4gate`) | 6 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Inwit (`inwit`) | 6 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| BASIC-FIT (`basic-fit`) | 6 | NOT_DISCLOSED: lti_vested; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| CTP (`ctp`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| REN - Redes Energéticas Nacionais, SGPS, S.A. (`ren-redes-energeticas-nacionais-sgps-s-a`) | 6 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sydbank AS (`T0002`) | 6 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: pension_contribution, sti_max, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: benefits_value |
| Thor Medical ASA (`T0023`) | 6 | NOT_DISCLOSED: exchange_segment, isin, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Allreal Holding AG (`allreal-holding-ag`) | 5 | NOT_DISCLOSED: aggregate_headcount, listing_date, lti_vested, staff_by_segment |
| AEP Plantations plc (`aep-plantations-plc`) | 5 | NOT_DISCLOSED: exchange_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: sti_max, sti_target |
| Avon Technologies plc (`avon-technologies-plc`) | 5 | NOT_DISCLOSED: exchange_segment, listing_date, staff_by_country; STATED_IN_OTHER_FORM: lti_granted |
| BOOT (HENRY) PLC (`boot-henry-plc`) | 5 | NOT_DISCLOSED: listing_date, other_names, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Bridgepoint Group Plc (`bridgepoint-group-plc`) | 5 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| Autoneum Holding AG (`autoneum-holding-ag`) | 5 | NOT_DISCLOSED: lti_target, sti_target; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Burckhardt Compression Holding AG (`burckhardt-compression-holding-ag`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Aseana Properties Limited (`aseana-properties-limited`) | 5 | NOT_DISCLOSED: fte, isin, other_names, staff_by_country, staff_by_segment |
| BAE SYSTEMS PLC (`bae-systems-plc`) | 5 | NOT_DISCLOSED: exchange_segment, listing_date; REMUNERATION_REPORT_NOT_READ: lti_vested |
| BLOOMSBURY PUBLISHING PLC (`bloomsbury-publishing-plc`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_paid, sti_target |
| CLS HOLDINGS PLC (`cls-holdings-plc`) | 5 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target |
| Capricorn Energy PLC (`capricorn-energy-plc`) | 5 | NOT_DISCLOSED: listing_date, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted |
| Dellia Group (`dellia-group`) | 5 | NOT_DISCLOSED: exchange_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Ecora Royalties PLC (`ecora-royalties-plc`) | 5 | NOT_DISCLOSED: listing_date, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| BILFINGER SE O.N. (`bilfinger-se-o-n`) | 5 | NOT_DISCLOSED: listing_date, lti_granted, lti_vested |
| DIERIG HOLDING AG O.N. (`dierig-holding-ag-91dc6032`) | 5 | NOT_DISCLOSED: exchange_segment, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| FAIR VALUE REIT-AG INH.ON (`fair-value-reit-ag-cef1dc63`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| ORBIS SE O.N. (`orbis-se-3d0d94ff`) | 5 | NOT_DISCLOSED: lti_max, lti_vested |
| CPH Group AG (`cph-group-ag-2a655fb2`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Dätwyler Holding AG (`datwyler-holding-ag-eca04fdb`) | 5 | NOT_DISCLOSED: exchange_segment, lti_vested, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| Ems-Chemie Holding AG (`ems-chemie-holding-ag-d319099b`) | 5 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution, sti_max, sti_target |
| AUTO1 GROUP SE (`auto1-group-se-0e2acd91`) | 5 | NOT_DISCLOSED: other_names, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| DATA MODUL AG O.N. (`data-modul-ag-9cac6e64`) | 5 | NOT_DISCLOSED: largest_holders, other_names, pe_stake_5pct, staff_by_country, staff_by_segment |
| FORTEC ELEKTRO. O.N. (`fortec-elektro-b45e5cd6`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| HAMBORNER REIT AG O.N. (`hamborner-reit-ag-cb84ee44`) | 5 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker |
| SMA SOLAR TECHNOL.AG (`sma-solar-technol-ag-1fa9e8e7`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Galderma Group AG (`galderma-group-ag-8c1dbf8c`) | 5 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, lti_target, lti_vested, sti_target |
| Holcim Ltd (`holcim-ltd-b2e462f1`) | 5 | NOT_DISCLOSED: exchange_segment, listing_date, lti_vested, staff_by_segment |
| Leonteq AG (`leonteq-ag-6723ca54`) | 5 | NOT_DISCLOSED: lti_max, lti_vested, sti_max |
| Logitech International S.A. (`logitech-international-s-a-0a74f2ba`) | 5 | NOT_DISCLOSED: benefits_value, lti_vested, pension_contribution, sti_paid |
| Novartis AG (`novartis-ag-f0d1b7d5`) | 5 | NOT_DISCLOSED: lti_vested |
| PolyPeptide Group AG (`polypeptide-group-ag-ec98be88`) | 5 | NOT_DISCLOSED: lti_target, lti_vested, sti_max, sti_target |
| PSP Swiss Property AG (`psp-swiss-property-ag-05c2c3ad`) | 5 | REPORT_NOT_FOUND: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Roche Holding AG (`roche-holding-ag-5abd8231`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_vested, total_remuneration |
| SF Urban Properties AG (`sf-urban-properties-ag-b860022e`) | 5 | REPORT_NOT_FOUND: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| SIG Group Ltd (`sig-group-ltd-69ad78ae`) | 5 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| Xlife Sciences AG (`xlife-sciences-ag-1d9f77f3`) | 5 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Fairview International PLC (`fairview-international-plc-ae11bf81`) | 5 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Funding Circle Holdings Plc (`funding-circle-holdings-plc-5c033007`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target; STATED_IN_OTHER_FORM: lti_granted |
| Galliford Try Holdings plc (`galliford-try-holdings-plc-46fc9d1a`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Genel Energy plc (`genel-energy-plc-dc8659be`) | 5 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_target |
| Georgia Capital PLC (`georgia-capital-plc-298a1d16`) | 5 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Gulf Marine Services PLC (`gulf-marine-services-plc-f393af40`) | 5 | NOT_DISCLOSED: exchange_segment, listing_date, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Hostelworld Group PLC (`hostelworld-group-plc-162ea308`) | 5 | NOT_DISCLOSED: other_names, revenue_by_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: sti_target |
| Intertek Group Plc (`intertek-group-plc-0f840c70`) | 5 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_vested, pension_contribution, sti_paid |
| Morgan Advanced Materials Plc (`morgan-advanced-materials-plc-58a5cd32`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| PERSIMMON PLC (`persimmon-plc-03d19fa0`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| ProCook Group Plc (`procook-group-plc-45a2e6f4`) | 5 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| RHI Magnesita N.V. (`rhi-magnesita-n-v-fb7495f7`) | 5 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_max, sti_target |
| ROTORK PLC (`rotork-plc-119d0a2a`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Rolls-Royce Holdings PLC (`rolls-royce-holdings-plc-5c92af4f`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested; STATED_IN_OTHER_FORM: lti_granted |
| Supermarket Income REIT plc (`supermarket-income-reit-plc-3dbe8d27`) | 5 | DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: sti_target |
| THG plc (`thg-plc-24b2c5db`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| Trustpilot Group Plc (`trustpilot-group-plc-f322927b`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_target |
| VANQUIS BANKING GROUP PLC (`vanquis-banking-group-plc-0a416b36`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested |
| Vodafone Group PLC (`vodafone-group-plc-8b2b35c3`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Nueva Expresión Textil, S.A. (`nueva-expresion-textil-s-a`) | 5 | NOT_DISCLOSED: share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Repsol, S.A. (`repsol-s-a`) | 5 | NOT_DISCLOSED: listing_date, other_names, staff_by_country, staff_by_segment, ticker |
| Tubos Reunidos, S.A. (`tubos-reunidos-s-a`) | 5 | NOT_DISCLOSED: pension_type, role_disclosure, shareholding_requirement, staff_by_segment, ticker |
| Ilyda SA (`ilyda-sa`) | 5 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Papoutsanis S.A. (`papoutsanis-s-a`) | 5 | NOT_DISCLOSED: other_names, revenue_by_segment, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year |
| Public Power Corporation S.A. (`public-power-corporation-s-a`) | 5 | NOT_DISCLOSED: fte, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Danieli & C. (`danieli-c`) | 5 | NOT_DISCLOSED: exchange_segment, other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Fila (`fila`) | 5 | NOT_DISCLOSED: fte, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Nexi (`nexi`) | 5 | NOT_DISCLOSED: exchange_segment, fte, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| PLC (`plc`) | 5 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year |
| Reply (`reply`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment, staff_by_segment |
| IMCD (`imcd`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested, shareholding_requirement |
| AEDIFICA (`aedifica`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| BANIMMO A (`banimmo-a`) | 5 | NOT_DISCLOSED: benefits, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| Ecoener, S.A. (`ecoener-s-a`) | 5 | NOT_DISCLOSED: share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Iberpapel Gestión, S.A. (`iberpapel-gestion-s-a`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, staff_by_segment, ticker |
| Kri-Kri Milk Industry S.A. (`kri-kri-milk-industry-s-a`) | 5 | NOT_DISCLOSED: fte, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Space Hellas S.A. (`space-hellas-s-a`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Banca Sistema (`banca-sistema`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Gas Plus (`gas-plus`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| AALBERTS NV (`aalberts-nv`) | 5 | NOT_DISCLOSED: benefits_value, lti_vested, pension_contribution |
| NOS, S.G.P.S., S.A. (`nos-s-g-p-s-s-a`) | 5 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Grenergy Renovables, S.A. (`grenergy-renovables-s-a`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Obrascón Huarte Lain, S.A. (`obrascon-huarte-lain-s-a`) | 5 | NOT_DISCLOSED: exchange_segment, fte, listing_date, other_names, staff_by_segment |
| LAMDA Development S.A. (`lamda-development-s-a`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Lavipharm S.A. (`lavipharm-s-a`) | 5 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Quality & Reliability A.B.E.E. (`quality-reliability-a-b-e-e`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| Brioschi Sviluppo Immobiliare (`brioschi-sviluppo-immobiliare`) | 5 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Edison (`edison`) | 5 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Italmobiliare (`italmobiliare`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sit (`sit`) | 5 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sys-Dat (`sys-dat`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Telecom Italia (`telecom-italia`) | 5 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_vested |
| Webuild (`webuild`) | 5 | NOT_DISCLOSED: fte, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| NN GROUP (`nn-group`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_vested, total_remuneration |
| SIGNIFY NV (`signify-nv`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested |
| Corem Property Pref (`corem-property-pref`) | 5 | NOT_DISCLOSED: other_names, staff_by_segment, sti_max, sti_target |
| Handelsbanken (`handelsbanken`) | 5 | NETWORK_ERROR: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| KDventures AB (`T0174`) | 5 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Mendus AB (`T0443`) | 5 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Vivesto AB (`T0255`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Ascelia Pharma AB (`T0368`) | 5 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Bure Equity AB (`T0488`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Industrivärden AB (`T0090`) | 5 | NOT_DISCLOSED: other_names, revenue, revenue_by_country, revenue_by_segment, staff_by_segment |
| Investment Oresund AB (`T0159`) | 5 | NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| NAXS AB (`T0373`) | 5 | NOT_DISCLOSED: revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| SynAct Pharma AB (`T0398`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment, staff_by_segment |
| Traction AB (`T0533`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| BARR (A.G.) PLC (`barr-a-g-plc`) | 4 | NOT_DISCLOSED: exchange_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_vested |
| Amicorp FS (UK) plc (`amicorp-fs-uk-plc`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| SED Energy (`sed-energy`) | 4 | NOT_DISCLOSED: benefits, exchange_segment, staff_by_country, staff_by_segment |
| Chill Brands Group plc (`chill-brands-group-plc`) | 4 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: revenue_by_segment, staff_by_country, staff_by_segment |
| Experian plc (`experian-plc`) | 4 | NOT_DISCLOSED: other_names, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| K2A Knaust & Andersson Pref (`k2a-knaust-andersson-pref`) | 4 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: shareholding_requirement |
| CAMERIT AG (`camerit-ag-45f4d990`) | 4 | NOT_DISCLOSED: base_salary, benefits_value, pension_contribution, total_remuneration |
| SINGULUS TECHNOL. EO 1 (`singulus-technol-66103de1`) | 4 | NOT_DISCLOSED: exchange_segment, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| DocMorris AG (`docmorris-ag-be190279`) | 4 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| DO & CO Aktiengesellschaft (`do-co-aktiengesellschaft-1ce4abbb`) | 4 | NOT_DISCLOSED: exchange_segment, listing_date, other_names, staff_by_segment |
| Semperit AG Holding (`semperit-ag-holding-2a7b594a`) | 4 | NOT_DISCLOSED: exchange_segment, other_names, pe_stake_5pct, staff_by_segment |
| VERBUND AG (`verbund`) | 4 | NOT_DISCLOSED: exchange_segment, revenue_by_country, staff_by_country, staff_by_segment |
| Marinomed Biotech AG (`marinomed-biotech-ag-807f84bd`) | 4 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| DT.TELEKOM AG NA (`dt-telekom-ag-9dfbbd0c`) | 4 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, ticker |
| FLATEXDEGIRO SE (`flatexdegiro-se-0d4c8d91`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| GERRESHEIMER AG (`gerresheimer-ag-25295c16`) | 4 | NOT_DISCLOSED: lti_granted, lti_vested |
| Gurit Holding AG (`gurit-holding-ag-02374e88`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target |
| Komax Holding AG (`komax`) | 4 | NOT_DISCLOSED: lti_vested, sti_target |
| Landis+Gyr Group AG (`landis-gyr-group-ag-7b8d0754`) | 4 | NOT_DISCLOSED: lti_max, lti_vested |
| LEM Holding SA (`lem-holding-sa-cc5005fc`) | 4 | NOT_DISCLOSED: lti_target, sti_target |
| Schweiter Technologies AG (`schweiter-technologies-ag-b9dd7eca`) | 4 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| Sunrise Communications AG (`sunrise-communications-ag-548ca7af`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Tecan Group AG (`tecan-group-ag-328eeee8`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| VAT Group AG (`vat-group-ag-ccdd96de`) | 4 | NOT_DISCLOSED: lti_target, lti_vested, sti_target |
| FIRSTGROUP PLC (`firstgroup-plc-14f42f50`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| GB Group plc (`gb-group-plc-a9e1b652`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, sti_target |
| GSK plc (`gsk-plc-669dcd41`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| Harworth Group PLC (`harworth-group-plc-7d3f06a0`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Helios Towers plc (`helios-towers-plc-e4fbb8f9`) | 4 | STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_target |
| IP Group PLC (`ip-group-plc-116a40f2`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| ITV PLC (`itv-plc-304113fa`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| IntegraFin Holdings plc (`integrafin-holdings-plc-27547212`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| International Workplace Group plc (`international-workplace-group-plc-3ae007b6`) | 4 | NOT_DISCLOSED: isin, staff_by_country, staff_by_segment, ticker |
| Johnson Service Group PLC (`johnson-service-group-plc-9e93b50d`) | 4 | STATED_IN_OTHER_FORM: lti_granted; REMUNERATION_REPORT_NOT_READ: lti_vested |
| KENMARE RESOURCES PLC (`kenmare-resources-plc-e7d5776b`) | 4 | NOT_DISCLOSED: fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Kainos Group plc (`kainos-group-plc-c7147294`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| LLOYDS BANKING GROUP PLC (`lloyds-banking-group-plc-003b014c`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| Lion Finance Group PLC (`lion-finance-group-plc-03b7fac3`) | 4 | NOT_DISCLOSED: revenue_by_country; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested |
| London Stock Exchange Group PLC (`london-stock-exchange-group-plc-e057fe1a`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| LondonMetric Property PLC (`londonmetric-property-plc-7b6ae645`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| M&G plc (`m-g-plc-b3f586ff`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Marshalls Plc (`marshalls-plc-ba8b711a`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Mears Group PLC (`mears-group-plc-67e5aca9`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| NewRiver REIT plc (`newriver-reit-plc-20056ec9`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Oxford Nanopore Technologies plc (`oxford-nanopore-technologies-plc-0e6547be`) | 4 | NOT_DISCLOSED: staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested |
| Palace Capital plc (`palace-capital-plc-d1ecc7a0`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| Pollen Street Group Limited (`pollen-street-group-limited-18ef67f4`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested |
| Primary Health Properties plc (`primary-health-properties-plc-dc3a3b23`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Princes Group plc (`princes-group-plc-95096765`) | 4 | NOT_DISCLOSED: share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| RELX PLC (`relx-plc-28248427`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| RS Group plc (`rs-group-plc-9ec766f0`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Sabre Insurance Group PLC (`sabre-insurance-group-plc-39f58b74`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Safestore Holdings PLC (`safestore-holdings-plc-c17fb612`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, sti_target |
| Shaftesbury Capital PLC (`shaftesbury-capital-plc-1cc22072`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Speedy Hire PLC (`speedy-hire-plc-a0c06d9a`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Spirax Group plc (`spirax-group-plc-13efaf7d`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, pension_contribution |
| Spire Healthcare Group plc (`spire-healthcare-group-plc-ca3dba5b`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Stelrad Group PLC (`stelrad-group-plc-2e1bd2c0`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| TATE & LYLE PLC (`tate-lyle-plc-0f1c0dfd`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| TBC Bank Group plc (`tbc-bank-group-plc-6b9bee2a`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, sti_max, sti_target |
| TRIFAST PLC (`trifast-plc-3989d139`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target |
| Trainline plc (`trainline-plc-b4b3d1ca`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| Vesuvius plc (`vesuvius-plc-2a126702`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| Watches of Switzerland Group PLC (`watches-of-switzerland-group-plc-cbe5a2bd`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_target, sti_target |
| GIMV (`gimv`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, pension_contribution |
| Cementos Molins, S.A. (`cementos-molins-s-a`) | 4 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment, ticker |
| Compañía Española de Viviendas en Alquiler S.A. (`compania-espanola-de-viviendas-en-alquiler-s-a`) | 4 | NOT_DISCLOSED: other_names, revenue_by_country, staff_by_country, staff_by_segment |
| Elinoil Hellenic Petroleum Company S.A. (`elinoil-hellenic-petroleum-company-s-a`) | 4 | NOT_DISCLOSED: fte, revenue_by_country, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| National Bank of Greece S.A. (`national-bank-of-greece-s-a`) | 4 | NOT_DISCLOSED: exchange_segment, revenue_by_country, revenue_by_segment, staff_by_segment |
| Sidma Steel S.A. (`sidma-steel-s-a`) | 4 | NOT_DISCLOSED: pension_contribution, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Thessaloniki Port Authority Societe Anonyme (`thessaloniki-port-authority-societe-anonyme`) | 4 | NOT_DISCLOSED: fte, revenue_by_country, staff_by_segment, ticker |
| Ferretti (`ferretti`) | 4 | NOT_DISCLOSED: fte, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| FinecoBank (`finecobank`) | 4 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_segment, staff_by_segment |
| Garofalo Health Care (`garofalo-health-care`) | 4 | NOT_DISCLOSED: fte, other_names, staff_by_country, staff_by_segment |
| Mondo TV (`mondo-tv`) | 4 | NOT_DISCLOSED: fte, pension_type, revenue_by_segment, staff_by_segment |
| ACOMO (`acomo`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target |
| Sporting Clube de Portugal - Futebol, SAD (`sporting-clube-de-portugal-futebol-sad`) | 4 | NOT_DISCLOSED: other_names, revenue_by_country, staff_by_country, staff_by_segment |
| SOFINA (`sofina`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_max, lti_target |
| Deoleo, S.A. (`deoleo-s-a`) | 4 | NOT_DISCLOSED: exchange_segment, fte, other_names, staff_by_segment |
| CrediaBank S.A. (`crediabank-s-a`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Banca Mediolanum (`banca-mediolanum`) | 4 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| GVS (`gvs`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Interpump Group (`interpump-group`) | 4 | NOT_DISCLOSED: share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| RCS MediaGroup (`rcs-mediagroup`) | 4 | NOT_DISCLOSED: exchange_segment, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Seri Industrial (`seri-industrial`) | 4 | NOT_DISCLOSED: fte, other_names, revenue_by_country, staff_by_country |
| EBUSCO HOLDING (`ebusco-holding`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| HOLLAND COLOURS (`holland-colours`) | 4 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted |
| BELYSSE GROUP (`belysse-group`) | 4 | NOT_DISCLOSED: exchange_segment, role_disclosure, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year |
| ONTEX GROUP (`ontex-group`) | 4 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| SYENSQO (`syensqo`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| VASTNED (`vastned`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| ACS, Actividades de Construcción y Servicios, S.A. (`acs-actividades-de-construccion-y-servicios-s-a`) | 4 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_segment |
| Athens Water Supply and Sewerage Company S.A. (`athens-water-supply-and-sewerage-company-s-a`) | 4 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment |
| Piraeus Bank S.A. (`piraeus-bank-s-a`) | 4 | NOT_DISCLOSED: share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Bastogi (`bastogi`) | 4 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| Caleffi (`caleffi`) | 4 | NOT_DISCLOSED: fte, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Fiera Milano (`fiera-milano`) | 4 | NOT_DISCLOSED: lti_granted, pension_contribution |
| Gefran (`gefran`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| LU-VE (`lu-ve`) | 4 | NOT_DISCLOSED: largest_holders, other_names, pe_stake_5pct, staff_by_segment |
| Piquadro (`piquadro`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Recordati (`recordati`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sogefi (`sogefi`) | 4 | NOT_DISCLOSED: fte, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Trevi Finanziaria Industriale (`trevi-finanziaria-industriale`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Zignago Vetro (`zignago-vetro`) | 4 | NOT_DISCLOSED: fte, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| ALFEN (`alfen`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| FORFARMERS (`forfarmers`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| POSTNL (`postnl`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Pharma Equity Group A/S (`T0099`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Circio Holding ASA (`T0013`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Byggmästare Anders J Ahlström Holding AB (publ) (`T0139`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Flerie AB (`T0292`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Isofol Medical AB (`T0568`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Keo Capital AB (`T0262`) | 4 | NOT_DISCLOSED: fte, revenue_by_country, revenue_by_segment, staff_by_segment |
| XSpray Pharma AB (`T0299`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Cadeler A/S (`T0397`) | 4 | NOT_DISCLOSED: lti_target, lti_vested |
| Lumo Kodit Oyj (`T0609`) | 4 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| BREEDON GROUP PLC (`breedon-group-plc`) | 3 | NOT_DISCLOSED: listing_date, other_names, staff_by_segment |
| BKW AG (`bkw-ag`) | 3 | NOT_DISCLOSED: fte; REMUNERATION_REPORT_NOT_READ: lti_vested |
| Bucher Industries AG (`bucher-industries-ag`) | 3 | NOT_DISCLOSED: pension_type, role_disclosure, shareholding_requirement |
| DCC Energy plc (`dcc-energy-plc`) | 3 | NOT_DISCLOSED: isin, staff_by_country, ticker |
| SOFTING AG O.N. (`softing-ag-365a9352`) | 3 | NOT_DISCLOSED: other_names, staff_by_country, staff_by_segment |
| THYSSENKRUPP NUCERA AG & KGAA (`thyssenkrupp-nucera-ag-kgaa-fac8c580`) | 3 | NOT_DISCLOSED: fiscal_year, lti_vested |
| Voltatron AG (`voltatron-ag-57b867a2`) | 3 | NOT_DISCLOSED: revenue_by_segment, staff_by_country, staff_by_segment |
| ENBW ENERGIE BADEN-WUERTTEMBERG ON (`enbw-energie-baden-wuerttemberg-30b5438b`) | 3 | NOT_DISCLOSED: listing_date, other_names, staff_by_country |
| INTERTAINMENT AG INH O.N. (`intertainment-ag-db87b5a6`) | 3 | NOT_DISCLOSED: benefits, benefits_value, pension_contribution |
| MUELLER-DIE LILA LOGISTIK SE (`mueller-die-lila-logistik-se-f3c40a4b`) | 3 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| UZIN UTZ SE O.N. (`uzin-utz-se-808b3f93`) | 3 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: fiscal_year_end, role_disclosure |
| WILD BUNCH AG O.N. (`wild-bunch-ag-7b9483b1`) | 3 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: shareholding_requirement, staff_by_segment |
| DKSH Holding AG (`dksh-holding-ag-6576340c`) | 3 | NOT_DISCLOSED: lti_target, lti_vested |
| EFG International AG (`efg-international-ag-549347cb`) | 3 | REMUNERATION_REPORT_NOT_READ: benefits, role_disclosure, shareholding_requirement |
| Kapsch TrafficCom AG (`kapsch-trafficcom-ag-1d6bbc81`) | 3 | NOT_DISCLOSED: fte, other_names, staff_by_segment |
| Palfinger AG (`palfinger-ag-e07e19f6`) | 3 | NOT_DISCLOSED: fte, other_names, staff_by_segment |
| BKS Bank AG (`bks-bank-ag-5e8b8669`) | 3 | NOT_DISCLOSED: fte, revenue_by_country, staff_by_segment |
| INIT INNOVATION O.N. (`init-innovation-3237f8ad`) | 3 | NOT_DISCLOSED: fte, revenue_by_segment, staff_by_segment |
| SNP SCHNEIDER-NEUREITHER O.N. (`snp-schneider-neureither-f82bee76`) | 3 | NOT_DISCLOSED: largest_holders, other_names, staff_by_segment |
| GREENCORE GROUP PLC (`greencore-group-plc-1026165b`) | 3 | NOT_DISCLOSED: isin, listing_date, other_names |
| Hollywood Bowl Group plc (`hollywood-bowl-group-plc-cf76bae2`) | 3 | REMUNERATION_REPORT_NOT_READ: sti_target |
| PZ CUSSONS PLC (`pz-cussons-plc-a434b740`) | 3 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Shawbrook Group plc (`shawbrook-group-plc-d45cea57`) | 3 | NOT_DISCLOSED: isin, revenue_by_country, staff_by_country |
| UNILEVER PLC (`unilever-plc-b59b11b1`) | 3 | NOT_DISCLOSED: lti_granted, total_remuneration |
| SOLVAY (`solvay`) | 3 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: pension_type, role_disclosure |
| HELLENiQ ENERGY Holdings S.A. (`helleniq-energy-holdings-s-a`) | 3 | NOT_DISCLOSED: fte, revenue_by_country, ticker |
| B&C Speakers (`b-c-speakers`) | 3 | NOT_DISCLOSED: fte, revenue_by_segment, staff_by_segment |
| OVS (`ovs`) | 3 | NOT_DISCLOSED: revenue_by_country, staff_by_segment, ticker |
| Ratti (`ratti`) | 3 | NOT_DISCLOSED: exchange_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| SLIGRO FOOD GROUP (`sligro-food-group`) | 3 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Construcciones y Auxiliar de Ferrocarriles, S.A. (`construcciones-y-auxiliar-de-ferrocarriles-s-a`) | 3 | NOT_DISCLOSED: other_names, revenue_by_country, staff_by_segment |
| Global Dominion Access, S.A. (`global-dominion-access-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment |
| Squirrel Media, S.A. (`squirrel-media-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, staff_by_country, staff_by_segment |
| Qualco Group S.A. (`qualco-group-s-a`) | 3 | NOT_DISCLOSED: fte, staff_by_segment, ticker |
| Alerion (`alerion`) | 3 | NOT_DISCLOSED: other_names, staff_by_country, staff_by_segment |
| Fidia (`fidia`) | 3 | NOT_DISCLOSED: other_names, staff_by_country, staff_by_segment |
| Fincantieri (`fincantieri`) | 3 | NOT_DISCLOSED: other_names, staff_by_segment, ticker |
| Iren (`iren`) | 3 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment |
| Lottomatica Group (`lottomatica-group`) | 3 | NOT_DISCLOSED: fte, revenue_by_country, staff_by_segment |
| MARR (`marr`) | 3 | NOT_DISCLOSED: fte, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Moncler (`moncler`) | 3 | NOT_DISCLOSED: other_names, revenue_by_country; DERIVATION_INPUT_MISSING: sector_code |
| Revo Insurance (`revo-insurance`) | 3 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| HEIJMANS KON (`heijmans-kon`) | 3 | DERIVATION_INPUT_MISSING: sector_code; NOT_DISCLOSED: lti_vested |
| NX FILTRATION (`nx-filtration`) | 3 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| TKH GROUP (`tkh-group`) | 3 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| WOLTERS KLUWER (`wolters-kluwer`) | 3 | NOT_DISCLOSED: lti_vested |
| Jerónimo Martins, SGPS, S.A. (`jeronimo-martins-sgps-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, fte, other_names |
| CFE (`cfe`) | 3 | NOT_DISCLOSED: exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| INCLUSIO SA/NV (`inclusio-sa-nv`) | 3 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| General de Alquiler de Maquinaria, S.A. (`general-de-alquiler-de-maquinaria-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment |
| Meliá Hotels International, S.A. (`melia-hotels-international-s-a`) | 3 | NOT_DISCLOSED: listing_date, staff_by_segment, ticker |
| Banca Generali (`banca-generali`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, pe_stake_5pct |
| Comer Industries (`comer-industries`) | 3 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Industrie De Nora (`industrie-de-nora`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment |
| Sanlorenzo (`sanlorenzo`) | 3 | NOT_DISCLOSED: fte, other_names, staff_by_segment |
| BRUNEL INTERNAT (`brunel-internat`) | 3 | NOT_DISCLOSED: other_names; REMUNERATION_REPORT_NOT_READ: lti_vested |
| MAGNUM (`magnum`) | 3 | NOT_DISCLOSED: exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| V LANSCHOT KEMPEN (`v-lanschot-kempen`) | 3 | NOT_DISCLOSED: ebitda, exchange_segment, staff_by_segment |
| Galp Energia, SGPS, S.A. (`galp-energia-sgps-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, fte, staff_by_segment |
| The Navigator Company, S.A. (`the-navigator-company-s-a`) | 3 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment |
| Nekkar ASA (`T0143`) | 3 | NOT_DISCLOSED: fte, listing_date, staff_by_segment |
| Infant Bacterial Therapeutics AB (`T0413`) | 3 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_segment |
| VNV Global AB (`T0089`) | 3 | NOT_DISCLOSED: revenue_by_country, revenue_by_segment, staff_by_segment |
| Shell PLC (`shell-plc`) | 3 | NOT_DISCLOSED: isin; REMUNERATION_REPORT_NOT_READ: lti_granted |
| AO World plc (`ao-world-plc`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Antofagasta plc (`antofagasta-plc`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution |
| ARYZTA AG (`aryzta-ag`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Adecco Group AG (`adecco-group-ag`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Alcon Inc. (`alcon-inc`) | 2 | NOT_DISCLOSED: lti_vested |
| Bossard Holding AG (`bossard-holding-ag`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested, sti_target |
| TRATON SE   INH O.N. (`traton-se-8a6b8f62`) | 2 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: staff_by_segment |
| WUESTENROT+WUERTTEMBERGISCHE AG O.N. (`wuestenrot-wuerttembergische-ag-07b9dfbc`) | 2 | NOT_DISCLOSED: ebitda, revenue_by_country |
| BERENTZEN-GRUPPE AG (`berentzen-gruppe-ag-957f8708`) | 2 | NOT_DISCLOSED: pension_contribution |
| DEUTSCHE REAL ESTATE AG O.N. (`deutsche-real-estate-ag-8625fa60`) | 2 | NOT_DISCLOSED: revenue_by_segment, staff_by_segment |
| MING LE SPORTS AG (`ming-le-sports-ag-fc0affd5`) | 2 | NOT_DISCLOSED: pension_type, shareholding_requirement |
| Cembra Money Bank AG (`cembra-money-bank-ag-752ce099`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Clariant AG (`clariant-ag-0616ec80`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| CA Immobilien Anlagen AG (`ca-immobilien-anlagen-ag-a9ff4a4a`) | 2 | NOT_DISCLOSED: other_names, revenue_by_country |
| EVN AG (`evn-ag-90cea5f3`) | 2 | NOT_DISCLOSED: staff_by_country, staff_by_segment |
| FACC AG (`facc-ag-5f4b658e`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Polytec Holding AG (`polytec-holding-ag-2a433fdb`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Josef Manner & Comp. AG (`josef-manner-comp-ag-4b81bd60`) | 2 | NOT_DISCLOSED: revenue_by_country, staff_by_segment |
| FRESENIUS MEDICAL CARE AG O.N. (`fresenius-medical-care-ag-241c7b04`) | 2 | NOT_DISCLOSED: listing_date, staff_by_segment |
| INTICA SYSTEMS SE (`intica-systems-se-18005922`) | 2 | NOT_DISCLOSED: lti_granted |
| PATRIZIA SE NA ON (`patrizia-se-41659152`) | 2 | NOT_DISCLOSED: exchange_segment, staff_by_segment |
| SECUNET SECURITY AG O.N. (`secunet-security-ag-c4d9b7e4`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Geberit AG (`geberit-ag-c1d8a2d9`) | 2 | NOT_DISCLOSED: lti_vested |
| Idorsia Ltd (`idorsia-ltd-c5656188`) | 2 | NOT_DISCLOSED: role_disclosure, shareholding_requirement |
| INFICON HOLDING AG (`inficon-holding-ag-4220ed6f`) | 2 | NOT_DISCLOSED: lti_vested; REMUNERATION_REPORT_NOT_READ: lti_vested |
| GRAINGER PLC (`grainger-plc-e2cb3986`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Gulf Keystone Petroleum Limited (`gulf-keystone-petroleum-limited-88d8a58d`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_target |
| KINGFISHER PLC (`kingfisher-plc-94bd46d7`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| MCBRIDE PLC (`mcbride-plc-fd766eb4`) | 2 | REMUNERATION_REPORT_NOT_READ: sti_target |
| Mitchells & Butlers plc (`mitchells-butlers-plc-30f2f1e2`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Norcros plc (`norcros-plc-c8639b5b`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_target |
| OSB GROUP PLC (`osb-group-plc-0972698d`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| PayPoint PLC (`paypoint-plc-c431010f`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_target |
| Premier Foods plc (`premier-foods-plc-b6f5f233`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| RANK GROUP PLC (`rank-group-plc-26f67d4c`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_max |
| Robert Walters PLC (`robert-walters-plc-ee19d4ce`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Smiths News PLC (`smiths-news-plc-e1bd4c22`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| TAYLOR WIMPEY PLC (`taylor-wimpey-plc-66b3fcee`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| TESCO PLC (`tesco-plc-596de5a2`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Wickes Group PLC (`wickes-group-plc-8a2fb481`) | 2 | REMUNERATION_REPORT_NOT_READ: sti_target |
| discoverIE Group plc (`discoverie-group-plc-d676c327`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| AZELIS GROUP (`azelis-group`) | 2 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_target |
| BARCO (`barco`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_max |
| KINEPOLIS GROUP (`kinepolis-group`) | 2 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_max |
| PROXIMUS (`proximus`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| UMICORE (`umicore`) | 2 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: role_disclosure |
| Cox Infrastructure Group, S.A. (`cox-infrastructure-group-s-a`) | 2 | NOT_DISCLOSED: revenue_by_segment, staff_by_segment |
| Laboratorio Reig Jofre, S.A. (`laboratorio-reig-jofre-s-a`) | 2 | NOT_DISCLOSED: exchange_segment, staff_by_segment |
| Logista Integral, S.A. (`logista-integral-s-a`) | 2 | NOT_DISCLOSED: revenue_by_country, ticker |
| Auction Technology Group plc (`auction-technology-group-plc`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Alter Ego Media S.A. (`alter-ego-media-s-a`) | 2 | NOT_DISCLOSED: staff_by_segment, ticker |
| Anima Holding (`anima-holding`) | 2 | NOT_DISCLOSED: sti_target |
| Banca Ifis (`banca-ifis`) | 2 | NOT_DISCLOSED: ebitda, staff_by_segment |
| Equita Group (`equita-group`) | 2 | NOT_DISCLOSED: revenue_by_country, staff_by_segment |
| Immsi (`immsi`) | 2 | NOT_DISCLOSED: exchange_segment, other_names |
| Italgas (`italgas`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Technogym (`technogym`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Wiit (`wiit`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| FUGRO (`fugro`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| WERELDHAVE (`wereldhave`) | 2 | NOT_DISCLOSED: lti_max |
| Semapa - Sociedade de Investimento e Gestão, SGPS, S.A. (`semapa-sociedade-de-investimento-e-gestao-sgps-s-a`) | 2 | NOT_DISCLOSED: fte, other_names |
| ABO GROUP (`abo-group`) | 2 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| BEKAERT (`bekaert`) | 2 | NOT_DISCLOSED: staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted |
| WERELDHAVE BELGIUM (`wereldhave-belgium`) | 2 | NOT_DISCLOSED: lti_max |
| Atrys Health, S.A. (`atrys-health-s-a`) | 2 | NOT_DISCLOSED: staff_by_segment, ticker |
| Grupo Empresarial San José, S.A. (`grupo-empresarial-san-jose-s-a`) | 2 | NOT_DISCLOSED: staff_by_segment, ticker |
| Ellaktor S.A. (`ellaktor-s-a`) | 2 | NOT_DISCLOSED: staff_by_segment, ticker |
| Real Consulting S.A. (`real-consulting-s-a`) | 2 | NOT_DISCLOSED: staff_by_country, staff_by_segment |
| Basicnet (`basicnet`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| Bestbe Holding (`bestbe-holding`) | 2 | NOT_DISCLOSED: fte, pension_type |
| Elica (`elica`) | 2 | NOT_DISCLOSED: fte, other_names |
| Indel B (`indel-b`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| TXT e-solutions (`txt-e-solutions`) | 2 | NOT_DISCLOSED: other_names, staff_by_segment |
| ASM INTERNATIONAL (`asm-international`) | 2 | NOT_DISCLOSED: lti_vested |
| LOTUS BAKERIES (`lotus-bakeries`) | 2 | NOT_DISCLOSED: pension_type, role_disclosure |
| Colonial SFL, Socimi S. A. (`colonial-sfl-socimi-s-a`) | 2 | NOT_DISCLOSED: staff_by_segment, ticker |
| Corporación Acciona Energías Renovables, S.A. (`corporacion-acciona-energias-renovables-s-a`) | 2 | NOT_DISCLOSED: other_names, ticker |
| Elecnor, S.A. (`elecnor-s-a`) | 2 | NOT_DISCLOSED: other_names, ticker |
| Solaria Energía y Medio Ambiente, S.A. (`solaria-energia-y-medio-ambiente-s-a`) | 2 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: aggregate_headcount |
| Viscofan, S.A. (`viscofan-s-a`) | 2 | NOT_DISCLOSED: pension_contribution, staff_by_segment |
| Centric Holdings S.A. (`centric-holdings-s-a`) | 2 | NOT_DISCLOSED: exchange_segment, staff_by_country |
| Emporiki Eisagogiki Aftokiniton Ditrohon kai Mihanon Thalassis Societe Anonyme (`emporiki-eisagogiki-aftokiniton-ditrohon-kai-mihanon-thalassis-societe-anonyme`) | 2 | NOT_DISCLOSED: revenue_by_country, staff_by_country |
| Aeffe (`aeffe`) | 2 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: role_disclosure |
| Ascopiave (`ascopiave`) | 2 | NOT_DISCLOSED: revenue_by_country, staff_by_segment |
| Carel Industries (`carel-industries`) | 2 | NOT_DISCLOSED: fte, other_names |
| Mondadori Editore (`mondadori-editore`) | 2 | NOT_DISCLOSED: fte, other_names |
| Risanamento (`risanamento`) | 2 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| CORBION (`corbion`) | 2 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| HEINEKEN (`heineken`) | 2 | NOT_DISCLOSED: exchange_segment, other_names |
| TOMTOM (`tomtom`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution, sti_max |
| Ponsse 1 (`ponsse-1`) | 2 | NOT_DISCLOSED: lti_target, sti_target |
| Det Østasiatiske Kompagni (`T0233`) | 2 | NOT_DISCLOSED: revenue_by_segment, staff_by_segment |
| Interoil Exploration and Production ASA (`T0423`) | 2 | NOT_DISCLOSED: total_remuneration |
| Orron Energy AB (`T0470`) | 2 | NOT_DISCLOSED: fte, staff_by_segment |
| Coca-Cola Europacific Partners plc (`coca-cola-europacific-partners-plc`) | 1 | NOT_DISCLOSED: exchange_segment |
| SUSS MicroTec SE (`suss-microtec-se-b7558a97`) | 1 | NOT_DISCLOSED: staff_by_country |
| UNIPER SE  NA O.N. (`uniper-se-2cd8e9fe`) | 1 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount |
| UTD.INTERNET AG NA (`utd-internet-ag-fa5f4803`) | 1 | NOT_DISCLOSED: other_names |
| PFEIFFER VACUUM TECH. AG O.N. (`pfeiffer-vacuum-tech-ag-a38e65f0`) | 1 | NOT_DISCLOSED: other_names |
| Carlo Gavazzi Holding AG (`carlo-gavazzi-holding-ag-39d1d1b5`) | 1 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount |
| AMAG Austria Metall AG (`amag-austria-metall-ag-9da856cd`) | 1 | NOT_DISCLOSED: other_names |
| AT&S Austria Technologie & Systemtechnik Aktiengesellschaft (`at-s-austria-technologie-systemtechnik-aktiengesel-768eb540`) | 1 | NOT_DISCLOSED: other_names |
| Bajaj Mobility AG (`bajaj-mobility-ag-8e6bef55`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Mayr-Melnhof Karton AG (`mayr-melnhof-karton-ag-ef1c26e1`) | 1 | NOT_DISCLOSED: other_names |
| Österreichische Post AG (`osterreichische-post-ag-73cb1454`) | 1 | NOT_DISCLOSED: exchange_segment |
| Vienna Insurance Group AG Wiener Versicherung Gruppe (`vienna-insurance-group-ag-wiener-versicherung-grup-cf6631de`) | 1 | NOT_DISCLOSED: other_names |
| EVOTEC SE  INH O.N. (`evotec-se-0d298d1f`) | 1 | NOT_DISCLOSED: staff_by_segment |
| HAMBURGER HAFEN UND LOGISTIK A-SP NA (`hamburger-hafen-und-logistik-a-sp-53728df8`) | 1 | NOT_DISCLOSED: exchange_segment |
| SAF HOLLAND SE  INH EO 1 (`saf-holland-se-e07079b5`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Novavest Real Estate AG (`novavest-real-estate-ag-796f6493`) | 1 | NOT_DISCLOSED: pension_type |
| Hochschild Mining PLC (`hochschild-mining-plc-4d2379f4`) | 1 | REMUNERATION_REPORT_NOT_READ: lti_target |
| InterContinental Hotels Group PLC (`intercontinental-hotels-group-plc-ca6a391f`) | 1 | NOT_DISCLOSED: staff_by_country |
| Oxford Biomedica plc (`oxford-biomedica-plc-76dcfac7`) | 1 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| Zoyo Limited (`zoyo-limited-7dac566f`) | 1 | NO_IDENTIFIER: lei |
| TITAN S.A. (`titan-s-a`) | 1 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| ENCE Energía y Celulosa, S.A. (`ence-energia-y-celulosa-s-a`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Gestamp Automoción, S.A. (`gestamp-automocion-s-a`) | 1 | NOT_DISCLOSED: other_names |
| Piaggio (`piaggio`) | 1 | NOT_DISCLOSED: exchange_segment |
| Snam (`snam`) | 1 | NOT_DISCLOSED: ticker |
| Terna (`terna`) | 1 | NOT_DISCLOSED: other_names |
| TRIODOS BANK (`triodos-bank`) | 1 | NOT_DISCLOSED: other_names |
| AmRest Holdings SE (`amrest-holdings-se`) | 1 | NOT_DISCLOSED: pension_contribution |
| Redeia Corporación, S.A. (`redeia-corporacion-s-a`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Admie Holding S.A. (`admie-holding-s-a`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| Ideal Holdings S.A. (`ideal-holdings-s-a`) | 1 | NOT_DISCLOSED: other_names |
| Mevaco S.A. (`mevaco-s-a`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| A2a (`a2a`) | 1 | NOT_DISCLOSED: revenue_by_country |
| Borgosesia (`borgosesia`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| doValue (`dovalue`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Eurogroup Laminations (`eurogroup-laminations`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Italian Exhibition Group (`italian-exhibition-group`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| Sabaf (`sabaf`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| FASTNED (`fastned`) | 1 | NOT_DISCLOSED: other_names |
| PB HOLDING (`pb-holding`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| AGEAS (`ageas`) | 1 | NOT_DISCLOSED: role_disclosure |
| BPOST (`bpost`) | 1 | NOT_DISCLOSED: lti_vested |
| Aena S.M.E., S.A. (`aena-s-m-e-s-a`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Amadeus IT Group, S.A. (`amadeus-it-group-s-a`) | 1 | NOT_DISCLOSED: other_names |
| Innovative Solutions Ecosystem, S.A. (`innovative-solutions-ecosystem-s-a`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| Bally's Intralot S.A. (`bally-s-intralot-s-a`) | 1 | NOT_DISCLOSED: ticker |
| Fais Holding Societe Anonyme (`fais-holding-societe-anonyme`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| Avio (`avio`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Banca Monte dei Paschi di Siena (`banca-monte-dei-paschi-di-siena`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Esprinet (`esprinet`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Fine Foods & Pharmaceuticals NTM (`fine-foods-pharmaceuticals-ntm`) | 1 | NOT_DISCLOSED: staff_by_country |
| Gabetti Property Solutions (`gabetti-property-solutions`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| IGD Immobiliare Grande Distribuzione SIIQ (`igd-immobiliare-grande-distribuzione-siiq`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| OPS Ecom (`ops-ecom`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| Orsero (`orsero`) | 1 | WRONG_YEAR_REPORT: fiscal_year |
| PHARMING GROUP (`pharming-group`) | 1 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Novabase - Sociedade Gestora de Participações Sociais, S.A. (`novabase-sociedade-gestora-de-participacoes-sociais-s-a`) | 1 | NOT_DISCLOSED: staff_by_country |
| Napatech A/S (`T0083`) | 1 | REMUNERATION_REPORT_NOT_READ: base_salary |
| Metsä Board Corporation (`T0448`) | 1 | NOT_DISCLOSED: other_names |
| PowerCell Sweden AB (`T0038`) | 1 | NOT_DISCLOSED: staff_by_segment |
