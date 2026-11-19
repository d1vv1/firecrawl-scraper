# What the run could not find: runs_16nov_revanth_j.csv

2652 missing values in 258 of 277 companies (built 19 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REPORT_NOT_FOUND` | Annual report not found | 150 | 7 | Put the FY annual report link (PDF, or a gs:// file) in `annual_report_url` and re-run |
| `REMUNERATION_REPORT_NOT_FOUND` | Remuneration report not found | 6 | 6 | Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay |
| `WRONG_YEAR_REPORT` | Values read from an older report | 14 | 14 | Put the FY report link in `annual_report_url` and re-run with --redo |
| `CREDITS_EXHAUSTED` | Firecrawl credits ran out | 8 | 1 | Top up credits (or raise --max-run-credits / --doc-credits) and re-run |
| `DOCUMENT_UNREADABLE` | Document could not be read | 28 | 1 | Scanned or broken file: supply a text PDF, or check the download |
| `NETWORK_ERROR` | Network or site error | 31 | 3 | Re-run; if it repeats, supply the document link |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 115 | 113 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `FX_RATE_MISSING` | Calculated field: no exchange rate | 1 | 1 | Re-run the field (the API step gives the ECB rate), or fix the currency unit |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 714 | 92 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 1585 | 216 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 830 | 186 | - |
| `NOT_COLLECTED` | Not asked for in this run | 4748 | 192 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| pension_contribution | 237 | NOT_DISCLOSED 135, REMUNERATION_REPORT_NOT_READ 102 |
| benefits_value | 186 | REMUNERATION_REPORT_NOT_READ 107, NOT_DISCLOSED 79 |
| lti_vested | 167 | NOT_DISCLOSED 90, REMUNERATION_REPORT_NOT_READ 77 |
| lti_granted | 154 | REMUNERATION_REPORT_NOT_READ 83, NOT_DISCLOSED 71 |
| sti_target | 139 | NOT_DISCLOSED 76, REMUNERATION_REPORT_NOT_READ 63 |
| staff_by_segment | 127 | NOT_DISCLOSED 118, REPORT_NOT_FOUND 5, NETWORK_ERROR 2 |
| lti_target | 126 | NOT_DISCLOSED 67, REMUNERATION_REPORT_NOT_READ 59 |
| market_cap_band | 113 | DERIVATION_INPUT_MISSING 112, FX_RATE_MISSING 1 |
| share_price | 110 | NOT_DISCLOSED 101, REPORT_NOT_FOUND 5, NETWORK_ERROR 3 |
| lti_max | 104 | NOT_DISCLOSED 53, REMUNERATION_REPORT_NOT_READ 51 |
| sti_paid | 83 | NOT_DISCLOSED 51, REMUNERATION_REPORT_NOT_READ 32 |
| sti_max | 82 | NOT_DISCLOSED 42, REMUNERATION_REPORT_NOT_READ 40 |
| other_names | 80 | NOT_DISCLOSED 75, REPORT_NOT_FOUND 3, DOCUMENT_UNREADABLE 1 |
| staff_by_country | 79 | NOT_DISCLOSED 71, REPORT_NOT_FOUND 5, NETWORK_ERROR 2 |
| fte | 71 | NOT_DISCLOSED 63, REPORT_NOT_FOUND 5, CREDITS_EXHAUSTED 1 |
| revenue_by_country | 69 | NOT_DISCLOSED 61, REPORT_NOT_FOUND 5, CREDITS_EXHAUSTED 1 |
| shareholding_requirement | 67 | NOT_DISCLOSED 47, REMUNERATION_REPORT_NOT_READ 11, REPORT_NOT_FOUND 6 |
| exchange_segment | 58 | NOT_DISCLOSED 50, REPORT_NOT_FOUND 5, NETWORK_ERROR 1 |
| ultimate_parent | 53 | NOT_DISCLOSED 47, REPORT_NOT_FOUND 4, DOCUMENT_UNREADABLE 1 |
| revenue_by_segment | 45 | NOT_DISCLOSED 38, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| total_remuneration | 45 | NOT_DISCLOSED 23, REMUNERATION_REPORT_NOT_READ 22 |
| ticker | 45 | NOT_DISCLOSED 41, REPORT_NOT_FOUND 3, DOCUMENT_UNREADABLE 1 |
| base_salary | 36 | REMUNERATION_REPORT_NOT_READ 25, NOT_DISCLOSED 11 |
| pension_type | 32 | NOT_DISCLOSED 19, REPORT_NOT_FOUND 6, REMUNERATION_REPORT_NOT_READ 5 |
| pe_stake_5pct | 29 | NOT_DISCLOSED 22, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| benefits | 28 | NOT_DISCLOSED 12, REMUNERATION_REPORT_NOT_READ 8, REPORT_NOT_FOUND 5 |
| fiscal_year | 25 | WRONG_YEAR_REPORT 14, REPORT_NOT_FOUND 6, NETWORK_ERROR 2 |
| role_disclosure | 24 | NOT_DISCLOSED 12, REMUNERATION_REPORT_NOT_READ 6, REMUNERATION_REPORT_NOT_FOUND 6 |
| largest_holders | 24 | NOT_DISCLOSED 17, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| aggregate_headcount | 22 | REMUNERATION_REPORT_NOT_READ 14, NOT_DISCLOSED 8 |
| headcount | 19 | NOT_DISCLOSED 12, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| controlling_owner | 16 | NOT_DISCLOSED 9, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| ownership_type | 16 | NOT_DISCLOSED 9, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| ebitda | 15 | NOT_DISCLOSED 9, REPORT_NOT_FOUND 4, DOCUMENT_UNREADABLE 1 |
| accounting_basis | 15 | NOT_DISCLOSED 8, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| pay_currency | 14 | REMUNERATION_REPORT_NOT_READ 9, NOT_DISCLOSED 5 |
| controlling_owner_name | 14 | NOT_DISCLOSED 7, REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1 |
| listing_date | 14 | NOT_DISCLOSED 10, REPORT_NOT_FOUND 3, DOCUMENT_UNREADABLE 1 |
| shares_outstanding | 13 | REPORT_NOT_FOUND 5, NOT_DISCLOSED 5, NETWORK_ERROR 2 |
| sector_code | 9 | REPORT_NOT_FOUND 5, DERIVATION_INPUT_MISSING 3, NETWORK_ERROR 1 |
| revenue | 9 | REPORT_NOT_FOUND 4, NOT_DISCLOSED 3, DOCUMENT_UNREADABLE 1 |
| total_assets | 8 | REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1, NOT_DISCLOSED 1 |
| website | 7 | REPORT_NOT_FOUND 4, NOT_DISCLOSED 3 |
| sub_sector | 7 | REPORT_NOT_FOUND 5, NETWORK_ERROR 1, NOT_DISCLOSED 1 |
| fiscal_year_end | 7 | REPORT_NOT_FOUND 5, DOCUMENT_UNREADABLE 1, NOT_DISCLOSED 1 |
| reporting_currency | 6 | REPORT_NOT_FOUND 4, DOCUMENT_UNREADABLE 1, NOT_DISCLOSED 1 |
| isin | 1 | REPORT_NOT_FOUND 1 |
| exchange | 1 | REPORT_NOT_FOUND 1 |
| listing_status | 1 | REPORT_NOT_FOUND 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Abitare In (`abitare-in`) | 98 | NOT_DISCLOSED: benefits_value, controlling_owner, controlling_owner_name, exchange_segment, largest_holders, lti_granted, lti_max, lti_target, lti_vested, other_names, ownership_type, pe_stake_5pct, pension_contribution, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| ABN AMRO BANK N.V. (`abn-amro-bank-n-v`) | 58 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, shareholding_requirement, sti_paid, sti_target, ultimate_parent |
| EKOPAK (`ekopak`) | 50 | NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, staff_by_country, staff_by_segment, sti_max, sti_target; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| OXURION (`oxurion`) | 43 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pe_stake_5pct, pension_contribution, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, total_remuneration, ultimate_parent |
| General Commercial & Industrial S.A. (`general-commercial-industrial-s-a`) | 43 | NOT_DISCLOSED: accounting_basis, aggregate_headcount, exchange_segment, fte, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_target, ticker; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| European Innovation Solutions S.A. (`european-innovation-solutions-s-a`) | 39 | NOT_DISCLOSED: aggregate_headcount, fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, share_price, staff_by_country, staff_by_segment, sti_max, sti_target, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| DECEUNINCK (`deceuninck`) | 36 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_paid |
| Lingotes Especiales, S.A. (`lingotes-especiales-s-a`) | 36 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, ticker, ultimate_parent; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Newprinces (`newprinces`) | 36 | NOT_DISCLOSED: benefits_value, fte, headcount, lti_granted, lti_vested, pension_contribution, pension_type, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| QUESTFOR GR-PRICAF (`questfor-gr-pricaf`) | 35 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, isin, largest_holders, listing_date, listing_status, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, ultimate_parent, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Wool Industry Tria Alfa S.A. (`wool-industry-tria-alfa-s-a`) | 35 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: aggregate_headcount, benefits_value, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| HAVAS (`havas`) | 35 | NOT_DISCLOSED: revenue_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target, total_remuneration |
| Profile Systems & Software SA (`profile-systems-software-sa`) | 34 | NOT_DISCLOSED: aggregate_headcount, exchange_segment, fte, largest_holders, lti_max, lti_target, lti_vested, other_names, pe_stake_5pct, pension_contribution, pension_type, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| VOPAK (`vopak`) | 34 | NOT_DISCLOSED: other_names, revenue_by_country; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Autohellas S.A. (`autohellas-s-a`) | 32 | NOT_DISCLOSED: largest_holders, lti_granted, lti_max, lti_target, lti_vested, pe_stake_5pct, pension_contribution, pension_type, revenue_by_country, shareholding_requirement, staff_by_segment, sti_paid, sti_target, ticker |
| Centrale del Latte d'Italia (`centrale-del-latte-d-italia`) | 32 | NOT_DISCLOSED: benefits_value, exchange_segment, fte, lti_granted, lti_target, lti_vested, pension_contribution, staff_by_country, staff_by_segment, sti_paid, sti_target |
| IMMO MCC (`immo-mcc`) | 31 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, ultimate_parent, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| BANQUP GROUP (`banqup-group`) | 30 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_paid |
| Indra Sistemas, S.A. (`indra-sistemas-s-a`) | 30 | NOT_DISCLOSED: accounting_basis, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_segment, staff_by_country, staff_by_segment, sti_max, sti_paid, sti_target, ultimate_parent |
| Kekrops S.A. (`kekrops-s-a`) | 30 | DOCUMENT_UNREADABLE: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, ticker, total_assets, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| WAREHOUSES ESTATES (`warehouses-estates`) | 29 | REPORT_NOT_FOUND: accounting_basis, benefits, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, ownership_type, pe_stake_5pct, pension_type, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shareholding_requirement, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Intertech S.A. Inter. Technologies (`intertech-s-a-inter-technologies`) | 29 | REPORT_NOT_FOUND: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, ticker, total_assets, ultimate_parent, website; DERIVATION_INPUT_MISSING: market_cap_band |
| ASML Holding N.V. (`asml`) | 29 | NOT_DISCLOSED: base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ROULARTA (`roularta`) | 28 | NOT_DISCLOSED: benefits, exchange_segment, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Prim, S.A. (`prim-s-a`) | 28 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, share_price, staff_by_country, sti_paid, sti_target, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| Eurotech (`eurotech`) | 27 | NOT_DISCLOSED: accounting_basis, ebitda, fte, headcount, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Kruso Kapital (`kruso-kapital`) | 27 | NOT_DISCLOSED: ebitda, fte, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target |
| NEXTENSA (`nextensa`) | 26 | NOT_DISCLOSED: fte, staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Arteche Lantegi Elkartea, S.A. (`arteche-lantegi-elkartea-s-a`) | 24 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, ticker; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| ACCENTIS (`accentis`) | 23 | NOT_DISCLOSED: benefits, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| AS Commercial Industrial Company of Computers and Toys S.A. (`as-commercial-industrial-company-of-computers-and-toys-s-a`) | 23 | NOT_DISCLOSED: fte, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, share_price, shareholding_requirement, staff_by_segment, sti_max, sti_target, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Unidata (`unidata`) | 23 | NETWORK_ERROR: accounting_basis, controlling_owner, controlling_owner_name, ebitda, fiscal_year, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Desarrollos Especiales de Sistemas de Anclaje, S.A. (`desarrollos-especiales-de-sistemas-de-anclaje-s-a`) | 21 | NOT_DISCLOSED: lti_granted, lti_target, lti_vested, other_names, pension_contribution, pension_type, revenue_by_segment, share_price, staff_by_country, staff_by_segment, sti_paid, sti_target, ultimate_parent, website; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, pension_contribution, sti_max, sti_paid, sti_target |
| Talgo, S.A. (`talgo-s-a`) | 21 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_max, lti_target, lti_vested, other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, shares_outstanding, staff_by_segment, sti_paid, sti_target, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Petros Petropoulos AEVE (`petros-petropoulos-aeve`) | 21 | NOT_DISCLOSED: accounting_basis, benefits, controlling_owner, controlling_owner_name, exchange_segment, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Fourlis Holdings S.A. (`fourlis-holdings-s-a`) | 20 | NOT_DISCLOSED: exchange_segment, fte, listing_date, lti_granted, lti_vested, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_segment, sti_paid, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Aegean Airlines S.A. (`aegean-airlines-s-a`) | 19 | NOT_DISCLOSED: lti_granted, lti_max, lti_target, lti_vested, pension_contribution, share_price, staff_by_segment, sti_target, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Banco Comercial Português, S.A. (`banco-comercial-portugues-s-a`) | 19 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted, lti_vested |
| COLRUYT (`colruyt`) | 18 | NOT_DISCLOSED: exchange_segment, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, sti_max, sti_target |
| MIKO (`miko`) | 18 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Duro Felguera, S.A. (`duro-felguera-s-a`) | 18 | NOT_DISCLOSED: ebitda, exchange_segment, fte, headcount, lti_granted, lti_max, lti_target, pension_contribution, pension_type, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Montebalito, S.A. (`montebalito-s-a`) | 18 | NOT_DISCLOSED: base_salary, benefits_value, exchange_segment, other_names, pay_currency, pension_contribution, shareholding_requirement, staff_by_segment, ticker, total_remuneration, ultimate_parent |
| Nicolás Correa, S.A. (`nicolas-correa-s-a`) | 18 | NOT_DISCLOSED: accounting_basis, controlling_owner, controlling_owner_name, exchange_segment, fte, headcount, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| DiaSorin (`diasorin`) | 18 | NOT_DISCLOSED: fte, lti_max, lti_target, lti_vested, other_names, pension_contribution, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| XIOR (`xior`) | 17 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, benefits_value, lti_granted, lti_vested, pension_contribution, pension_type, sti_paid, total_remuneration |
| Renta Corporación Real Estate, S.A. (`renta-corporacion-real-estate-s-a`) | 17 | NOT_DISCLOSED: accounting_basis, fte, largest_holders, other_names, pe_stake_5pct, pension_contribution, pension_type, revenue_by_country, staff_by_country, staff_by_segment, sti_max, sti_target, ticker, ultimate_parent |
| OPS Ecom (`ops-ecom`) | 17 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: benefits_value, fte, pension_contribution, revenue_by_country, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| EVS (`evs`) | 16 | NOT_DISCLOSED: staff_by_segment; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_vested, pay_currency, pension_contribution, sti_paid, total_remuneration |
| Nafpaktos Textile Industry S.A. (`nafpaktos-textile-industry-s-a`) | 16 | NOT_DISCLOSED: benefits_value, fte, listing_date, other_names, pension_contribution, pension_type, share_price, shareholding_requirement, staff_by_country, staff_by_segment, total_remuneration, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| RANDSTAD NV (`randstad-nv`) | 16 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target |
| ATENOR (`atenor`) | 15 | NOT_DISCLOSED: benefits, exchange_segment, fte, headcount, other_names, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| UCB (`ucb`) | 15 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pay_currency, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
| Audax Renovables, S.A. (`audax-renovables-s-a`) | 15 | NOT_DISCLOSED: benefits, benefits_value, lti_granted, lti_vested, pension_contribution, pension_type, shareholding_requirement, staff_by_segment, sti_paid, sti_target |
| Solaria Energía y Medio Ambiente, S.A. (`solaria-energia-y-medio-ambiente-s-a`) | 15 | NOT_DISCLOSED: other_names, pension_contribution, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker, ultimate_parent; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, pension_contribution |
| Hellenic Telecommunications Organization S.A. (`hellenic-telecommunications-organization-s-a`) | 15 | NOT_DISCLOSED: exchange_segment, fte, listing_date, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_target, pension_contribution, sti_paid, sti_target |
| Ibersol, S.G.P.S., S.A. (`ibersol-s-g-p-s-s-a`) | 15 | NOT_DISCLOSED: benefits_value, exchange_segment, listing_date, other_names, pension_contribution, share_price, shareholding_requirement, staff_by_segment, sti_paid, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| Grupo Ezentis, S.A. (`grupo-ezentis-s-a`) | 14 | NOT_DISCLOSED: benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_paid, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Innovative Solutions Ecosystem, S.A. (`innovative-solutions-ecosystem-s-a`) | 14 | NOT_DISCLOSED: exchange_segment, pension_type, share_price, shareholding_requirement, staff_by_segment, ticker, website; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Technical Olympic S.A. (`technical-olympic-s-a`) | 14 | NOT_DISCLOSED: benefits_value, pension_contribution, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker, total_remuneration; DERIVATION_INPUT_MISSING: market_cap_band |
| EPH Invest (`eph-invest`) | 14 | NOT_DISCLOSED: benefits, exchange_segment, fte, largest_holders, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| EURONEXT (`euronext`) | 14 | NOT_DISCLOSED: benefits_value, lti_granted, lti_vested, staff_by_segment, sti_paid |
| Edisun Power Europe AG (`edisun-power-europe-ag-e6666cb6`) | 14 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, pension_type, shareholding_requirement, sti_max, sti_paid, sti_target |
| Elastron S.A. - Steel Service Centers (`elastron-s-a-steel-service-centers`) | 13 | NOT_DISCLOSED: fte, pension_contribution, pension_type, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| MIG Holdings S.A. (`mig-holdings-s-a`) | 13 | NOT_DISCLOSED: exchange_segment, fte, largest_holders, listing_date, pe_stake_5pct, revenue_by_country, role_disclosure, share_price, shareholding_requirement, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| AZERION (`azerion`) | 13 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, lti_vested, sti_max, sti_target |
| Banco BPM (`banco-bpm`) | 12 | NOT_DISCLOSED: accounting_basis, ebitda, fte, headcount, revenue, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| IT Way (`it-way`) | 12 | NOT_DISCLOSED: accounting_basis, exchange_segment, fte, largest_holders, other_names, pe_stake_5pct, revenue_by_country, share_price, shares_outstanding, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band, sector_code |
| Rai Way (`rai-way`) | 12 | NOT_DISCLOSED: fte, lti_vested, other_names, pension_contribution, revenue_by_country, shareholding_requirement, shares_outstanding, staff_by_segment, total_assets; DERIVATION_INPUT_MISSING: market_cap_band |
| AMG (`amg`) | 12 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, lti_granted, ownership_type, pe_stake_5pct, ultimate_parent |
| Banque Cantonale du Jura SA (`banque-cantonale-du-jura-sa`) | 12 | NOT_DISCLOSED: benefits_value, total_remuneration |
| GBL (`gbl`) | 11 | NOT_DISCLOSED: ebitda, fte, staff_by_country; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target, lti_vested, sti_target, total_remuneration |
| HYLORIS (`hyloris`) | 11 | NOT_DISCLOSED: exchange_segment, lti_granted, lti_vested, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Cirsa Enterprises, S.A. (`cirsa-enterprises-s-a`) | 11 | NOT_DISCLOSED: fte, headcount, largest_holders, pe_stake_5pct, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Prosegur Compañía de Seguridad, S.A. (`prosegur-compania-de-seguridad-s-a`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, other_names, ownership_type, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| Applied Nutrition plc (`applied-nutrition-plc`) | 11 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_vested |
| Optima bank S.A. (`optima-bank-s-a`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, fte, ownership_type, revenue_by_country, revenue_by_segment, share_price, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| BFF Bank (`bff-bank`) | 11 | NOT_DISCLOSED: largest_holders, lti_target, other_names, pe_stake_5pct, pension_contribution, revenue_by_country, staff_by_segment, sti_max, sti_target |
| Emak (`emak`) | 11 | NOT_DISCLOSED: controlling_owner, controlling_owner_name, exchange_segment, fte, largest_holders, other_names, ownership_type, pe_stake_5pct, revenue_by_segment, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Gabetti Property Solutions (`gabetti-property-solutions`) | 11 | NOT_DISCLOSED: exchange_segment, largest_holders, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Geox (`geox`) | 11 | NOT_DISCLOSED: ebitda, exchange_segment, fte, headcount, other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Met.Extra Group (`met-extra-group`) | 11 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, benefits_value, pension_contribution, pension_type, shareholding_requirement |
| Risanamento (`risanamento`) | 11 | NOT_DISCLOSED: exchange_segment, fte, other_names, share_price, staff_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, role_disclosure, shareholding_requirement |
| V LANSCHOT KEMPEN (`v-lanschot-kempen`) | 11 | NOT_DISCLOSED: ebitda, exchange_segment, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: benefits_value |
| Estoril Sol, SGPS, S.A. (`estoril-sol-sgps-s-a`) | 11 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, shareholding_requirement, sti_target |
| Martifer SGPS, S.A. (`martifer-sgps-s-a`) | 11 | NOT_DISCLOSED: other_names, revenue_by_country, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: pension_contribution, sti_target |
| Sport Lisboa e Benfica - Futebol, SAD (`sport-lisboa-e-benfica-futebol-sad`) | 11 | NOT_DISCLOSED: benefits_value, exchange_segment, other_names, pension_contribution, revenue_by_country, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| CARE PROPERTY INV. (`care-property-inv`) | 10 | NOT_DISCLOSED: exchange_segment, largest_holders, pe_stake_5pct, staff_by_segment; REMUNERATION_REPORT_NOT_READ: lti_granted |
| FLORIDIENNE (`floridienne`) | 10 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, staff_by_country; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, sti_target |
| TINC (`tinc`) | 10 | NOT_DISCLOSED: fte, headcount, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Tubacex, S.A. (`tubacex-s-a`) | 10 | NOT_DISCLOSED: exchange_segment, fte, listing_date, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: sector_code |
| E. Pairis S.A. (`e-pairis-s-a`) | 10 | NOT_DISCLOSED: fte, listing_date, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| AHOLD DEL (`ahold-del`) | 10 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_country, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| ENVIPCO HOLDING (`envipco-holding`) | 10 | NOT_DISCLOSED: benefits, other_names, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_target |
| NEDAP (`nedap`) | 10 | NOT_DISCLOSED: benefits_value, lti_granted, lti_vested, sti_paid |
| Orell Füssli AG (`orell-fussli-ag-c5631ff9`) | 10 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, shareholding_requirement, sti_target |
| DWS GROUP GMBH+CO.KGAA ON (`dws-group-gmbh-co-kgaa-c6d99d12`) | 10 | DERIVATION_INPUT_MISSING: market_cap_band, sector_code; NOT_DISCLOSED: fiscal_year, fiscal_year_end, headcount, reporting_currency, revenue, share_price, shares_outstanding, sub_sector |
| BELYSSE GROUP (`belysse-group`) | 9 | NETWORK_ERROR: benefits, exchange_segment, fiscal_year, share_price, shareholding_requirement, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: role_disclosure |
| CFE (`cfe`) | 9 | CREDITS_EXHAUSTED: benefits, exchange_segment, fiscal_year, fte, pension_type, revenue_by_country, shareholding_requirement, staff_by_segment; REMUNERATION_REPORT_NOT_READ: role_disclosure |
| SOLVAC (`solvac`) | 9 | NOT_DISCLOSED: ebitda, other_names, revenue_by_country, revenue_by_segment, shareholding_requirement, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| J. & B. Ladenis Bros S.A. - Minerva - Knitwear Manufacturing Company (`j-b-ladenis-bros-s-a-minerva-knitwear-manufacturing-company`) | 9 | NOT_DISCLOSED: fte, other_names, revenue_by_segment, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| OCI (`oci`) | 9 | NOT_DISCLOSED: exchange_segment, fte, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution, sti_max, sti_paid, sti_target |
| KBC ANCORA (`kbc-ancora`) | 8 | NOT_DISCLOSED: fte, headcount, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Unicaja Banco, S.A. (`unicaja-banco-s-a`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, ticker, ultimate_parent |
| Alpha Real Estate Services S.A. (`alpha-real-estate-services-s-a`) | 8 | NOT_DISCLOSED: exchange_segment, fte, revenue_by_country, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Daios Plastics S.A. (`daios-plastics-s-a`) | 8 | NOT_DISCLOSED: fte, other_names, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Revoil S.A. (`revoil-s-a`) | 8 | NOT_DISCLOSED: fte, other_names, revenue_by_country, share_price, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Aeffe (`aeffe`) | 8 | NOT_DISCLOSED: other_names, pension_type, role_disclosure, share_price, shareholding_requirement, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Hera (`hera`) | 8 | NOT_DISCLOSED: exchange_segment, other_names, revenue_by_country, role_disclosure, share_price, shareholding_requirement, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Philogen (`philogen`) | 8 | NOT_DISCLOSED: fte, headcount, other_names, pe_stake_5pct, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment |
| PARAGON KGAA  INH O.N. (`paragon-kgaa-7616d267`) | 8 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Cindrigo Holdings Limited (`cindrigo-holdings-limited`) | 8 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Bodegas Riojanas, S.A. (`bodegas-riojanas-s-a`) | 7 | NOT_DISCLOSED: lti_max, pension_contribution, shareholding_requirement, staff_by_country, staff_by_segment, sti_target, ticker |
| Elton International Trading Company S.A. (`elton-international-trading-company-s-a`) | 7 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Iktinos Hellas S.A. Greek Marble Industry Technical and Touristic Company (`iktinos-hellas-s-a-greek-marble-industry-technical-and-touristic-company`) | 7 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Thrace Plastics Holding Company S.A. (`thrace-plastics-holding-company-s-a`) | 7 | NOT_DISCLOSED: fte, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: role_disclosure, shareholding_requirement |
| Altea Green Power (`altea-green-power`) | 7 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Tessellis (`tessellis`) | 7 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, role_disclosure, shareholding_requirement |
| HYDRATEC (`hydratec`) | 7 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: lti_target, lti_vested, sti_target |
| Compagnie Financière Richemont SA (`compagnie-financiere-richemont-sa-060892f5`) | 7 | NOT_DISCLOSED: benefits_value, lti_vested, shareholding_requirement |
| INCLUSIO SA/NV (`inclusio-sa-nv`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, lti_granted |
| Obrascón Huarte Lain, S.A. (`obrascon-huarte-lain-s-a`) | 6 | NOT_DISCLOSED: exchange_segment, fte, listing_date, other_names, staff_by_segment, ultimate_parent |
| Fais Holding Societe Anonyme (`fais-holding-societe-anonyme`) | 6 | NOT_DISCLOSED: share_price, staff_by_segment, ticker, ultimate_parent; WRONG_YEAR_REPORT: fiscal_year; DERIVATION_INPUT_MISSING: market_cap_band |
| Mathios Refractories S.A. (`mathios-refractories-s-a`) | 6 | NOT_DISCLOSED: fte, share_price, staff_by_country, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Cy4gate (`cy4gate`) | 6 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Inwit (`inwit`) | 6 | NOT_DISCLOSED: exchange_segment, fte, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| BASIC-FIT (`basic-fit`) | 6 | NOT_DISCLOSED: lti_vested; REMUNERATION_REPORT_NOT_READ: lti_max, lti_target, lti_vested, sti_max, sti_target |
| CTP (`ctp`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target, sti_max, sti_target |
| MAGNUM (`magnum`) | 6 | NOT_DISCLOSED: exchange_segment, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution |
| REN - Redes Energéticas Nacionais, SGPS, S.A. (`ren-redes-energeticas-nacionais-sgps-s-a`) | 6 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Wiener Privatbank SE (`wiener-privatbank-se-e8881192`) | 6 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value |
| Gurit Holding AG (`gurit-holding-ag-02374e88`) | 6 | REMUNERATION_REPORT_NOT_READ: lti_vested, pension_contribution, sti_target |
| Hypothekarbank Lenzburg AG (`hypothekarbank-lenzburg-ag-52099ad5`) | 6 | NOT_DISCLOSED: base_salary, benefits_value, pension_contribution; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution |
| Infracore SA (`infracore-sa-b3b0dcce`) | 6 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| Liechtensteinische Landesbank AG (`liechtensteinische-landesbank-ag-53271b6c`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| MCH Group AG (`mch-group-ag-c6fc7898`) | 6 | NOT_DISCLOSED: benefits_value, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| KPS AG NA O.N. (`kps-ag-d763be73`) | 6 | NOT_DISCLOSED: base_salary, benefits_value, pension_contribution |
| PROCREDIT HOLDING AG NA EO 5 (`procredit-holding-ag-74495a3c`) | 6 | NOT_DISCLOSED: pension_contribution |
| Baltic Classifieds Group PLC (`baltic-classifieds-group-plc`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Blencowe Resources Plc (`blencowe-resources-plc`) | 6 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| ACS, Actividades de Construcción y Servicios, S.A. (`acs-actividades-de-construccion-y-servicios-s-a`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, revenue_by_segment, staff_by_segment, ultimate_parent |
| Grenergy Renovables, S.A. (`grenergy-renovables-s-a`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| LAMDA Development S.A. (`lamda-development-s-a`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Lavipharm S.A. (`lavipharm-s-a`) | 5 | NOT_DISCLOSED: revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Quality & Reliability A.B.E.E. (`quality-reliability-a-b-e-e`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, staff_by_country, staff_by_segment |
| Brioschi Sviluppo Immobiliare (`brioschi-sviluppo-immobiliare`) | 5 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Edison (`edison`) | 5 | NOT_DISCLOSED: exchange_segment, revenue_by_country, share_price, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Fiera Milano (`fiera-milano`) | 5 | NOT_DISCLOSED: lti_granted, pension_contribution, shareholding_requirement |
| IGD Immobiliare Grande Distribuzione SIIQ (`igd-immobiliare-grande-distribuzione-siiq`) | 5 | NOT_DISCLOSED: fte, other_names, revenue_by_country, staff_by_segment; WRONG_YEAR_REPORT: fiscal_year |
| Italmobiliare (`italmobiliare`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sit (`sit`) | 5 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sys-Dat (`sys-dat`) | 5 | NOT_DISCLOSED: other_names, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Telecom Italia (`telecom-italia`) | 5 | NOT_DISCLOSED: shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_vested |
| Webuild (`webuild`) | 5 | NOT_DISCLOSED: fte, pe_stake_5pct, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| NN GROUP (`nn-group`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_vested, total_remuneration |
| SIGNIFY NV (`signify-nv`) | 5 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_vested |
| Erste Group Bank AG (`erste-group-bank-ag`) | 5 | NOT_DISCLOSED: pension_contribution |
| Julius Bär Gruppe AG (`julius-bar-gruppe-ag-de864d89`) | 5 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value |
| SF Urban Properties AG (`sf-urban-properties-ag-b860022e`) | 5 | REPORT_NOT_FOUND: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| CTS EVENTIM KGAA (`cts-eventim-kgaa-1664614e`) | 5 | NOT_DISCLOSED: pension_contribution; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Cobra Resources plc (`cobra-resources-plc`) | 5 | NOT_DISCLOSED: revenue, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Critical Mineral Resources Plc (`critical-mineral-resources-plc`) | 5 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| ONTEX GROUP (`ontex-group`) | 4 | WRONG_YEAR_REPORT: fiscal_year; REMUNERATION_REPORT_NOT_READ: lti_granted, lti_target |
| SYENSQO (`syensqo`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| VASTNED (`vastned`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| Meliá Hotels International, S.A. (`melia-hotels-international-s-a`) | 4 | NOT_DISCLOSED: listing_date, staff_by_segment, ticker, ultimate_parent |
| Athens Water Supply and Sewerage Company S.A. (`athens-water-supply-and-sewerage-company-s-a`) | 4 | NOT_DISCLOSED: fte, other_names, revenue_by_country, revenue_by_segment |
| Piraeus Bank S.A. (`piraeus-bank-s-a`) | 4 | NOT_DISCLOSED: share_price, staff_by_segment, ticker; DERIVATION_INPUT_MISSING: market_cap_band |
| Bastogi (`bastogi`) | 4 | NOT_DISCLOSED: revenue_by_country, share_price, staff_by_country; DERIVATION_INPUT_MISSING: market_cap_band |
| Caleffi (`caleffi`) | 4 | NOT_DISCLOSED: fte, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Gefran (`gefran`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| LU-VE (`lu-ve`) | 4 | NOT_DISCLOSED: largest_holders, other_names, pe_stake_5pct, staff_by_segment |
| Piquadro (`piquadro`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Recordati (`recordati`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Sogefi (`sogefi`) | 4 | NOT_DISCLOSED: fte, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Trevi Finanziaria Industriale (`trevi-finanziaria-industriale`) | 4 | NOT_DISCLOSED: other_names, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Zignago Vetro (`zignago-vetro`) | 4 | NOT_DISCLOSED: fte, other_names, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| ALFEN (`alfen`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_vested |
| BRUNEL INTERNAT (`brunel-internat`) | 4 | NOT_DISCLOSED: ebitda, other_names; REMUNERATION_REPORT_NOT_READ: lti_vested |
| CORBION (`corbion`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, pension_contribution |
| FORFARMERS (`forfarmers`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted, lti_max, lti_target |
| POSTNL (`postnl`) | 4 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Galp Energia, SGPS, S.A. (`galp-energia-sgps-s-a`) | 4 | NOT_DISCLOSED: exchange_segment, fte, staff_by_segment, ultimate_parent |
| Centiel AG (`centiel-ag-eeeda54a`) | 4 | NOT_DISCLOSED: controlling_owner, ownership_type, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Swiss Life Holding AG (`swiss-life-holding-ag-403064f3`) | 4 | NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, pension_contribution |
| Tecan Group AG (`tecan-group-ag-328eeee8`) | 4 | NOT_DISCLOSED: benefits, pension_type, role_disclosure, shareholding_requirement |
| IVU TRAFFIC TECHN.AG O.N. (`ivu-traffic-techn-ag-020c6212`) | 4 | NOT_DISCLOSED: controlling_owner, ownership_type, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| MBB SE O.N. (`mbb-se-be761dea`) | 4 | NOT_DISCLOSED: pension_contribution |
| NAGARRO SE  NA O.N. (`nagarro-se-9ed14a85`) | 4 | NOT_DISCLOSED: pension_contribution; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| ACG Metals Limited (`acg-metals-limited`) | 4 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Alkemy Capital Investments PLC (`alkemy-capital-investments-plc`) | 4 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value |
| Colonial SFL, Socimi S. A. (`colonial-sfl-socimi-s-a`) | 3 | NOT_DISCLOSED: staff_by_segment, ticker, ultimate_parent |
| General de Alquiler de Maquinaria, S.A. (`general-de-alquiler-de-maquinaria-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment |
| Viscofan, S.A. (`viscofan-s-a`) | 3 | NOT_DISCLOSED: pension_contribution, staff_by_segment, ultimate_parent |
| Centric Holdings S.A. (`centric-holdings-s-a`) | 3 | NOT_DISCLOSED: exchange_segment, staff_by_country, ultimate_parent |
| Emporiki Eisagogiki Aftokiniton Ditrohon kai Mihanon Thalassis Societe Anonyme (`emporiki-eisagogiki-aftokiniton-ditrohon-kai-mihanon-thalassis-societe-anonyme`) | 3 | NOT_DISCLOSED: revenue_by_country, staff_by_country, ultimate_parent |
| Banca Generali (`banca-generali`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, pe_stake_5pct |
| Comer Industries (`comer-industries`) | 3 | NOT_DISCLOSED: share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Industrie De Nora (`industrie-de-nora`) | 3 | NOT_DISCLOSED: exchange_segment, other_names, staff_by_segment |
| Sanlorenzo (`sanlorenzo`) | 3 | NOT_DISCLOSED: fte, other_names, staff_by_segment |
| The Navigator Company, S.A. (`the-navigator-company-s-a`) | 3 | NOT_DISCLOSED: revenue_by_country, staff_by_country, staff_by_segment |
| SW Umwelttechnik Stoiser & Wolschner AG (`sw-umwelttechnik-stoiser-wolschner-ag-fbdd5b89`) | 3 | NOT_DISCLOSED: benefits_value; REMUNERATION_REPORT_NOT_READ: benefits_value |
| BioVersys AG (`bioversys-ag`) | 3 | NOT_DISCLOSED: benefits_value |
| EvoNext Holdings SA (`evonext-holdings-sa-be1893c4`) | 3 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: benefits_value, pension_contribution |
| Schweiter Technologies AG (`schweiter-technologies-ag-b9dd7eca`) | 3 | NOT_DISCLOSED: benefits_value; REMUNERATION_REPORT_NOT_READ: benefits_value |
| CAMERIT AG (`camerit-ag-45f4d990`) | 3 | NOT_DISCLOSED: benefits_value, pension_contribution |
| DIERIG HOLDING AG O.N. (`dierig-holding-ag-91dc6032`) | 3 | NETWORK_ERROR: share_price, shares_outstanding; DERIVATION_INPUT_MISSING: market_cap_band |
| Dar Global PLC (`dar-global-plc`) | 3 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| LOTUS BAKERIES (`lotus-bakeries`) | 2 | NOT_DISCLOSED: pension_type, role_disclosure |
| Amadeus IT Group, S.A. (`amadeus-it-group-s-a`) | 2 | NOT_DISCLOSED: other_names, ultimate_parent |
| Corporación Acciona Energías Renovables, S.A. (`corporacion-acciona-energias-renovables-s-a`) | 2 | NOT_DISCLOSED: other_names, ticker |
| Elecnor, S.A. (`elecnor-s-a`) | 2 | NOT_DISCLOSED: other_names, ticker |
| Ascopiave (`ascopiave`) | 2 | NOT_DISCLOSED: revenue_by_country, staff_by_segment |
| Carel Industries (`carel-industries`) | 2 | NOT_DISCLOSED: fte, other_names |
| Mondadori Editore (`mondadori-editore`) | 2 | NOT_DISCLOSED: fte, other_names |
| Orsero (`orsero`) | 2 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: fte |
| HEINEKEN (`heineken`) | 2 | NOT_DISCLOSED: exchange_segment, other_names |
| TOMTOM (`tomtom`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution, sti_max |
| Marinomed Biotech AG (`marinomed-biotech-ag-807f84bd`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Curatis Holding AG (`curatis-holding-ag-adc33085`) | 2 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Glarner Kantonalbank (`glarner-kantonalbank-8ede902a`) | 2 | NOT_DISCLOSED: base_salary, benefits_value |
| Kudelski S.A. (`kudelski-s-a-fca01ba3`) | 2 | NOT_DISCLOSED: pension_contribution |
| Molecular Partners AG (`molecular-partners-ag-86d659ae`) | 2 | NOT_DISCLOSED: benefits_value |
| R&S Group Holding AG (`r-s-group-holding-ag-8cdcd57a`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| ALBIS LEASING AG O.N. (`albis-leasing-ag-30344d1d`) | 2 | NOT_DISCLOSED: pension_contribution |
| AUTO1 GROUP SE (`auto1-group-se-0e2acd91`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| EPIGENOMICS AG NA O.N. (`epigenomics-ag-ddb6ea6d`) | 2 | NOT_DISCLOSED: pension_contribution |
| FRESENIUS MEDICAL CARE AG O.N. (`fresenius-medical-care-ag-241c7b04`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| SAF HOLLAND SE  INH EO 1 (`saf-holland-se-e07079b5`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| SINO-GERMAN UNITED AG O.N. (`sino-german-united-ag-388acb2d`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| STO SE+CO.KGAA VZO O.N. (`sto-se-co-kgaa-9a1ae007`) | 2 | NOT_DISCLOSED: aggregate_headcount, benefits_value |
| VILLEROY + BOCH AG VZ (`villeroy-boch-ag-c5a85d57`) | 2 | NOT_DISCLOSED: shares_outstanding; DERIVATION_INPUT_MISSING: market_cap_band |
| WASGAU PRODUKTIONS & HANDELS NA O.N. (`wasgau-produktions-handels-8c33a77d`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| AIB Group plc (`aib-group-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| BSF Enterprise Plc (`bsf-enterprise-plc`) | 2 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Contango Holdings plc (`contango-holdings-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| DFI Retail Group Holdings Limited (`dfi-retail-group-holdings-limited`) | 2 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value |
| East Star Resources Plc (`east-star-resources-plc`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Fairview International PLC (`fairview-international-plc-ae11bf81`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Fevara plc (`fevara-plc-92307031`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Foresight Group Holdings Limited (`foresight-group-holdings-limited-122103c3`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| AGEAS (`ageas`) | 1 | NOT_DISCLOSED: role_disclosure |
| BPOST (`bpost`) | 1 | NOT_DISCLOSED: lti_vested |
| Aena S.M.E., S.A. (`aena-s-m-e-s-a`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Bally's Intralot S.A. (`bally-s-intralot-s-a`) | 1 | NOT_DISCLOSED: ticker |
| Avio (`avio`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Banca Monte dei Paschi di Siena (`banca-monte-dei-paschi-di-siena`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Esprinet (`esprinet`) | 1 | NOT_DISCLOSED: staff_by_segment |
| Fine Foods & Pharmaceuticals NTM (`fine-foods-pharmaceuticals-ntm`) | 1 | NOT_DISCLOSED: staff_by_country |
| PHARMING GROUP (`pharming-group`) | 1 | REMUNERATION_REPORT_NOT_READ: lti_granted |
| Novabase - Sociedade Gestora de Participações Sociais, S.A. (`novabase-sociedade-gestora-de-participacoes-sociais-s-a`) | 1 | NOT_DISCLOSED: staff_by_country |
| Gurktaler AG (`gurktaler-ag-313b0a0d`) | 1 | NOT_DISCLOSED: pension_contribution |
| Metall Zug AG (`metall-zug-ag-7412eb32`) | 1 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| VP Bank AG (`vp-bank-ag-e661c993`) | 1 | NOT_DISCLOSED: benefits_value |
| Zuger Kantonalbank (`zuger-kantonalbank-67b7c3b8`) | 1 | NOT_DISCLOSED: benefits_value |
| TKMS AG + CO. KGAA O.N. (`tkms-ag-co-kgaa-f468ef4d`) | 1 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Antofagasta plc (`antofagasta-plc`) | 1 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Ashmore Group Plc (`ashmore-group-plc`) | 1 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Autotrader Group plc (`autotrader-group-plc`) | 1 | FX_RATE_MISSING: market_cap_band |
