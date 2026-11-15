# What the run could not find: nordics_pay_datapoints.csv

356 missing values in 12 of 12 companies (built 15 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `NO_IDENTIFIER` | Needs an LEI or register number | 1 | 1 | Add `lei` or `business_id` to the input: only an official register gives this field |
| `CREDITS_EXHAUSTED` | Firecrawl credits ran out | 16 | 2 | Top up credits (or raise --max-run-credits / --doc-credits) and re-run |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 5 | 5 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 125 | 2 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 209 | 12 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 16 | 5 | - |
| `NOT_COLLECTED` | Not asked for in this run | 308 | 11 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| lti_target | 36 | NOT_DISCLOSED 22, REMUNERATION_REPORT_NOT_READ 14 |
| lti_max | 33 | NOT_DISCLOSED 19, REMUNERATION_REPORT_NOT_READ 14 |
| lti_granted | 30 | NOT_DISCLOSED 16, REMUNERATION_REPORT_NOT_READ 14 |
| sti_max | 29 | NOT_DISCLOSED 15, REMUNERATION_REPORT_NOT_READ 14 |
| lti_vested | 29 | NOT_DISCLOSED 15, REMUNERATION_REPORT_NOT_READ 14 |
| sti_target | 28 | NOT_DISCLOSED 14, REMUNERATION_REPORT_NOT_READ 14 |
| total_remuneration | 18 | REMUNERATION_REPORT_NOT_READ 14, NOT_DISCLOSED 4 |
| sti_paid | 17 | REMUNERATION_REPORT_NOT_READ 13, NOT_DISCLOSED 4 |
| pension_contribution | 13 | REMUNERATION_REPORT_NOT_READ 12, NOT_DISCLOSED 1 |
| staff_by_segment | 9 | NOT_DISCLOSED 9 |
| staff_by_country | 8 | NOT_DISCLOSED 8 |
| exchange_segment | 8 | NOT_DISCLOSED 8 |
| listing_date | 7 | NOT_DISCLOSED 7 |
| controlling_owner_name | 7 | NOT_DISCLOSED 7 |
| revenue_by_country | 7 | NOT_DISCLOSED 7 |
| shareholding_requirement | 6 | NOT_DISCLOSED 6 |
| other_names | 5 | NOT_DISCLOSED 5 |
| revenue_by_segment | 5 | NOT_DISCLOSED 4, CREDITS_EXHAUSTED 1 |
| isin | 5 | NOT_DISCLOSED 5 |
| share_price | 5 | NOT_DISCLOSED 5 |
| market_cap_band | 5 | DERIVATION_INPUT_MISSING 5 |
| pe_stake_5pct | 4 | NOT_DISCLOSED 4 |
| ultimate_parent | 3 | NOT_DISCLOSED 3 |
| ebitda | 3 | NOT_DISCLOSED 3 |
| accounting_basis | 3 | NOT_DISCLOSED 2, CREDITS_EXHAUSTED 1 |
| shares_outstanding | 3 | NOT_DISCLOSED 3 |
| largest_holders | 3 | NOT_DISCLOSED 3 |
| controlling_owner | 3 | NOT_DISCLOSED 2, CREDITS_EXHAUSTED 1 |
| ownership_type | 3 | NOT_DISCLOSED 2, CREDITS_EXHAUSTED 1 |
| benefits_value | 2 | REMUNERATION_REPORT_NOT_READ 1, NOT_DISCLOSED 1 |
| revenue | 2 | NOT_DISCLOSED 1, CREDITS_EXHAUSTED 1 |
| fte | 2 | CREDITS_EXHAUSTED 2 |
| aggregate_headcount | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| legal_name | 1 | CREDITS_EXHAUSTED 1 |
| lei | 1 | NO_IDENTIFIER 1 |
| ticker | 1 | NOT_DISCLOSED 1 |
| exchange | 1 | NOT_DISCLOSED 1 |
| listing_status | 1 | NOT_DISCLOSED 1 |
| country_code | 1 | CREDITS_EXHAUSTED 1 |
| head_office_city | 1 | CREDITS_EXHAUSTED 1 |
| website | 1 | CREDITS_EXHAUSTED 1 |
| sector_code | 1 | CREDITS_EXHAUSTED 1 |
| sub_sector | 1 | CREDITS_EXHAUSTED 1 |
| total_assets | 1 | CREDITS_EXHAUSTED 1 |
| reporting_currency | 1 | CREDITS_EXHAUSTED 1 |
| headcount | 1 | CREDITS_EXHAUSTED 1 |
| benefits | 1 | NOT_DISCLOSED 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Sparebanken Møre (`T0669`) | 121 | NOT_DISCLOSED: exchange_segment, isin, other_names, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Voss Veksel Landmandsbank (`voss-veksel-landmandsbank`) | 37 | CREDITS_EXHAUSTED: accounting_basis, controlling_owner, country_code, fte, head_office_city, headcount, legal_name, ownership_type, reporting_currency, revenue, revenue_by_segment, sector_code, sub_sector, total_assets, website; NOT_DISCLOSED: benefits, controlling_owner_name, ebitda, exchange, exchange_segment, isin, largest_holders, listing_date, listing_status, other_names, pe_stake_5pct, revenue_by_country, share_price, shares_outstanding, staff_by_country, staff_by_segment, sti_max, ticker, ultimate_parent; NO_IDENTIFIER: lei; DERIVATION_INPUT_MISSING: market_cap_band |
| Holand Og Setskog Sparebank (`holand-og-setskog-sparebank`) | 32 | NOT_DISCLOSED: controlling_owner_name, exchange_segment, isin, listing_date, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, shareholding_requirement, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target, total_remuneration |
| Circio Holding ASA (`T0013`) | 28 | NOT_DISCLOSED: controlling_owner_name, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment, sti_max |
| Interoil Exploration and Production ASA (`T0423`) | 22 | NOT_DISCLOSED: controlling_owner_name, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, share_price, sti_max, sti_paid, sti_target, total_remuneration, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Nekkar ASA (`T0143`) | 21 | NOT_DISCLOSED: listing_date, lti_granted, lti_max, lti_target, lti_vested, sti_target |
| Otello Corp ASA (`T0325`) | 21 | NOT_DISCLOSED: exchange_segment, lti_max, lti_target, lti_vested, revenue_by_country, share_price, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Alvotech SDB (`alvotech-sdb`) | 21 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration |
| Odfjell Technology (`odfjell-technology`) | 20 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, isin, largest_holders, listing_date, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, ultimate_parent; CREDITS_EXHAUSTED: fte; DERIVATION_INPUT_MISSING: market_cap_band |
| Melhus Sparebank (`melhus-sparebank`) | 19 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Bang & Olufsen A/S (`bang-olufsen-as`) | 7 | NOT_DISCLOSED: controlling_owner_name, listing_date, lti_target, other_names, staff_by_segment |
| Sparebank 1 Helgeland (`sparebank-1-helgeland`) | 7 | NOT_DISCLOSED: exchange_segment, isin, listing_date, revenue_by_country, shareholding_requirement, staff_by_country, staff_by_segment |
