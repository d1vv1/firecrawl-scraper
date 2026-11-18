# What the run could not find: runs_16nov_praveen.csv

483 missing values in 75 of 76 companies (built 18 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REPORT_NOT_FOUND` | Annual report not found | 32 | 5 | Put the FY annual report link (PDF, or a gs:// file) in `annual_report_url` and re-run |
| `REMUNERATION_REPORT_NOT_FOUND` | Remuneration report not found | 5 | 5 | Put the remuneration report link in `remuneration_report_url` and re-run with fields=pay |
| `WRONG_YEAR_REPORT` | Values read from an older report | 1 | 1 | Put the FY report link in `annual_report_url` and re-run with --redo |
| `CREDITS_EXHAUSTED` | Firecrawl credits ran out | 16 | 1 | Top up credits (or raise --max-run-credits / --doc-credits) and re-run |
| `DOCUMENT_UNREADABLE` | Document could not be read | 5 | 1 | Scanned or broken file: supply a text PDF, or check the download |
| `NETWORK_ERROR` | Network or site error | 27 | 1 | Re-run; if it repeats, supply the document link |
| `DERIVATION_INPUT_MISSING` | Calculated field: an input is missing | 29 | 27 | Fix the input field it rests on (share price, shares outstanding, business description) |
| `FX_RATE_MISSING` | Calculated field: no exchange rate | 1 | 1 | Re-run the field (the API step gives the ECB rate), or fix the currency unit |
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 123 | 30 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 244 | 52 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 48 | 18 | - |
| `NOT_COLLECTED` | Not asked for in this run | 2503 | 70 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| benefits_value | 72 | REMUNERATION_REPORT_NOT_READ 43, NOT_DISCLOSED 29 |
| pension_contribution | 64 | NOT_DISCLOSED 34, REMUNERATION_REPORT_NOT_READ 30 |
| market_cap_band | 28 | DERIVATION_INPUT_MISSING 27, FX_RATE_MISSING 1 |
| lti_vested | 26 | NOT_DISCLOSED 21, REMUNERATION_REPORT_NOT_READ 5 |
| share_price | 26 | NOT_DISCLOSED 23, REPORT_NOT_FOUND 2, NETWORK_ERROR 1 |
| shareholding_requirement | 17 | NOT_DISCLOSED 10, REPORT_NOT_FOUND 4, REMUNERATION_REPORT_NOT_READ 2 |
| sti_target | 15 | NOT_DISCLOSED 9, REMUNERATION_REPORT_NOT_READ 6 |
| lti_target | 14 | NOT_DISCLOSED 8, REMUNERATION_REPORT_NOT_READ 6 |
| lti_max | 14 | NOT_DISCLOSED 10, REMUNERATION_REPORT_NOT_READ 4 |
| sti_paid | 11 | NOT_DISCLOSED 8, REMUNERATION_REPORT_NOT_READ 3 |
| pension_type | 11 | NOT_DISCLOSED 5, REPORT_NOT_FOUND 4, DOCUMENT_UNREADABLE 1 |
| lti_granted | 11 | NOT_DISCLOSED 9, REMUNERATION_REPORT_NOT_READ 2 |
| benefits | 10 | REPORT_NOT_FOUND 4, NOT_DISCLOSED 3, REMUNERATION_REPORT_NOT_READ 2 |
| fiscal_year | 10 | REPORT_NOT_FOUND 5, NOT_DISCLOSED 2, NETWORK_ERROR 1 |
| staff_by_segment | 9 | NOT_DISCLOSED 7, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| role_disclosure | 9 | REMUNERATION_REPORT_NOT_FOUND 5, NOT_DISCLOSED 3, REMUNERATION_REPORT_NOT_READ 1 |
| staff_by_country | 8 | NOT_DISCLOSED 6, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| pe_stake_5pct | 8 | NOT_DISCLOSED 6, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| base_salary | 8 | REMUNERATION_REPORT_NOT_READ 6, NOT_DISCLOSED 2 |
| largest_holders | 7 | NOT_DISCLOSED 5, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| sti_max | 7 | REMUNERATION_REPORT_NOT_READ 4, NOT_DISCLOSED 3 |
| aggregate_headcount | 7 | REMUNERATION_REPORT_NOT_READ 5, NOT_DISCLOSED 2 |
| other_names | 6 | NOT_DISCLOSED 5, NETWORK_ERROR 1 |
| exchange_segment | 6 | NOT_DISCLOSED 4, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| revenue | 6 | NOT_DISCLOSED 3, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| fiscal_year_end | 6 | REPORT_NOT_FOUND 3, NETWORK_ERROR 1, DOCUMENT_UNREADABLE 1 |
| controlling_owner | 6 | NOT_DISCLOSED 3, REPORT_NOT_FOUND 2, NETWORK_ERROR 1 |
| ownership_type | 6 | NOT_DISCLOSED 3, REPORT_NOT_FOUND 2, NETWORK_ERROR 1 |
| revenue_by_country | 6 | NOT_DISCLOSED 4, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| shares_outstanding | 5 | NOT_DISCLOSED 3, NETWORK_ERROR 1, REPORT_NOT_FOUND 1 |
| revenue_by_segment | 5 | NOT_DISCLOSED 3, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| headcount | 5 | NOT_DISCLOSED 3, NETWORK_ERROR 1, REPORT_NOT_FOUND 1 |
| listing_date | 4 | NOT_DISCLOSED 2, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| sector_code | 4 | DERIVATION_INPUT_MISSING 2, NETWORK_ERROR 1, REPORT_NOT_FOUND 1 |
| ultimate_parent | 3 | NOT_DISCLOSED 2, NETWORK_ERROR 1 |
| website | 3 | NOT_DISCLOSED 1, NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| sub_sector | 3 | NETWORK_ERROR 1, NOT_DISCLOSED 1, REPORT_NOT_FOUND 1 |
| reporting_currency | 3 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1, REPORT_NOT_FOUND 1 |
| controlling_owner_name | 3 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1, NOT_DISCLOSED 1 |
| total_assets | 2 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| ebitda | 2 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| accounting_basis | 2 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| fte | 2 | NETWORK_ERROR 1, CREDITS_EXHAUSTED 1 |
| total_remuneration | 2 | REMUNERATION_REPORT_NOT_READ 2 |
| pay_currency | 1 | REMUNERATION_REPORT_NOT_READ 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Nexum Group AG (`nexum-group-ag-f3ad001d`) | 34 | DERIVATION_INPUT_MISSING: market_cap_band, sector_code; NOT_DISCLOSED: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, share_price, sti_paid, sti_target; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_granted, lti_max, lti_target, lti_vested, pay_currency, pension_contribution, sti_max, sti_paid, sti_target |
| Warimpex Finanz- und Beteiligungs AG (`warimpex-finanz-und-beteiligungs-ag-ae611bc8`) | 32 | NOT_DISCLOSED: benefits_value, exchange_segment, lti_granted, lti_max, lti_target, lti_vested, pension_contribution, shareholding_requirement, staff_by_country, sti_paid, sti_target |
| Arzneiwerk AG VIDA (`arzneiwerk-ag-vida`) | 29 | CREDITS_EXHAUSTED: accounting_basis, controlling_owner_name, ebitda, exchange_segment, fte, largest_holders, listing_date, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, staff_by_country, staff_by_segment, total_assets, website; DERIVATION_INPUT_MISSING: market_cap_band, sector_code; NOT_DISCLOSED: benefits, controlling_owner, fiscal_year, fiscal_year_end, headcount, ownership_type, pension_type, role_disclosure, share_price, shareholding_requirement, sub_sector |
| Frauenthal Holding AG (`frauenthal-holding-ag-edd167fb`) | 28 | NETWORK_ERROR: accounting_basis, controlling_owner, controlling_owner_name, ebitda, exchange_segment, fiscal_year, fiscal_year_end, fte, headcount, largest_holders, listing_date, other_names, ownership_type, pe_stake_5pct, reporting_currency, revenue, revenue_by_country, revenue_by_segment, sector_code, share_price, shares_outstanding, staff_by_country, staff_by_segment, sub_sector, total_assets, ultimate_parent, website; DERIVATION_INPUT_MISSING: market_cap_band |
| Emerald Horizon AG (`emerald-horizon-ag-a6420623`) | 18 | NOT_DISCLOSED: exchange_segment, other_names, pe_stake_5pct, revenue_by_segment, shares_outstanding, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits, benefits_value, lti_max, lti_target, lti_vested, shareholding_requirement, sti_max, sti_paid, sti_target |
| Stadlauer Malzfabrik AG (`stadlauer-malzfabrik-ag-8a23c30d`) | 18 | NOT_DISCLOSED: aggregate_headcount, benefits, largest_holders, listing_date, lti_max, lti_target, other_names, pe_stake_5pct, pension_type, revenue_by_country, revenue_by_segment, share_price, shareholding_requirement, staff_by_country, staff_by_segment, sti_max, sti_target; DERIVATION_INPUT_MISSING: market_cap_band |
| CHERRY SE (`cherry-se-57089b55`) | 18 | REPORT_NOT_FOUND: controlling_owner, fiscal_year, ownership_type, share_price; DERIVATION_INPUT_MISSING: market_cap_band; NOT_DISCLOSED: controlling_owner_name, largest_holders, lti_granted, lti_vested, pe_stake_5pct, pension_contribution, revenue_by_country, staff_by_segment, sti_paid |
| TISCON AG i.A. (`tiscon-ag-i-a-9dafa5a9`) | 16 | REPORT_NOT_FOUND: benefits, controlling_owner, fiscal_year, fiscal_year_end, headcount, ownership_type, pension_type, reporting_currency, revenue, sector_code, share_price, shareholding_requirement, shares_outstanding, sub_sector; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| EUROCOMMERCIAL (`eurocommercial`) | 13 | NOT_DISCLOSED: other_names, shareholding_requirement, staff_by_country, staff_by_segment, ultimate_parent; REMUNERATION_REPORT_NOT_READ: benefits_value, lti_target, lti_vested, sti_target |
| IVF HARTMANN Holding AG (`ivf-hartmann-holding-ag-fc38ba38`) | 12 | NOT_DISCLOSED: benefits_value, pension_type, shareholding_requirement, sti_target; REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_target |
| medmix AG (`medmix-ag-f840dcb1`) | 12 | NOT_DISCLOSED: benefits, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, base_salary, benefits_value, lti_max, lti_target, lti_vested, sti_max, sti_paid, sti_target |
| KOENIG + BAUER AG ST O.N. (`koenig-bauer-ag-1f22b792`) | 12 | NOT_DISCLOSED: lti_max, lti_vested, pension_contribution |
| LUFTHANSA AG VNA O.N. (`lufthansa-ag-0bc3d92c`) | 10 | NOT_DISCLOSED: exchange_segment, largest_holders, listing_date, pe_stake_5pct, revenue_by_country, revenue_by_segment, share_price, staff_by_country, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| HELIOS SOLAR AG (`helios-solar-ag-797724e7`) | 9 | NOT_DISCLOSED: controlling_owner, headcount, ownership_type, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits, pension_type, role_disclosure, shareholding_requirement |
| SCHOTT Pharma AG & Co. KGaA (`schott-pharma-ag-co-kgaa-26f01ea5`) | 9 | NOT_DISCLOSED: benefits_value, fiscal_year, lti_target, lti_vested, pension_contribution, shareholding_requirement, sti_max, sti_paid, sti_target |
| Leonteq AG (`leonteq-ag-6723ca54`) | 8 | NOT_DISCLOSED: lti_max, lti_vested, pension_contribution, sti_max |
| Santhera Pharmaceuticals Holding AG (`santhera-pharmaceuticals-holding-ag-8f83ccd5`) | 8 | WRONG_YEAR_REPORT: fiscal_year; NOT_DISCLOSED: controlling_owner, ownership_type, share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, total_remuneration |
| African Pioneer Plc (`african-pioneer-plc`) | 8 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| AGRANA Beteiligungs-AG (`agrana-beteiligungs-ag-60d4466c`) | 7 | NOT_DISCLOSED: exchange_segment, largest_holders, other_names, pe_stake_5pct, share_price, website; DERIVATION_INPUT_MISSING: market_cap_band |
| DT.PFANDBRIEFBK AG (`dt-pfandbriefbk-ag-71e35702`) | 7 | NOT_DISCLOSED: largest_holders, pe_stake_5pct, share_price, staff_by_country, staff_by_segment, ultimate_parent; DERIVATION_INPUT_MISSING: market_cap_band |
| Ems-Chemie Holding AG (`ems-chemie-holding-ag-d319099b`) | 6 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution |
| Groupe Minoteries SA (`groupe-minoteries-sa-11276f01`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| Mobimo Holding AG (`mobimo-holding-ag-df63dd1a`) | 6 | DOCUMENT_UNREADABLE: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| OC Oerlikon Corporation AG (`oc-oerlikon-corporation-ag-8ad162da`) | 6 | NOT_DISCLOSED: benefits_value |
| ACCENTRO REAL ESTATE AG  O.N. (`accentro-real-estate-ag-fbdf101b`) | 6 | REPORT_NOT_FOUND: benefits, fiscal_year, fiscal_year_end, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| READCREST CAPITAL AG O.N. (`readcrest-capital-ag-e4689651`) | 6 | NOT_DISCLOSED: benefits_value, pension_contribution |
| BATM Advanced Communications Limited (`batm-advanced-communications-limited`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Capital Limited (`capital-limited`) | 6 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| PSP Swiss Property AG (`psp-swiss-property-ag-05c2c3ad`) | 5 | REPORT_NOT_FOUND: benefits, fiscal_year, pension_type, shareholding_requirement; REMUNERATION_REPORT_NOT_FOUND: role_disclosure |
| INTICA SYSTEMS SE (`intica-systems-se-18005922`) | 5 | NOT_DISCLOSED: lti_granted, pension_contribution, shareholding_requirement |
| SMA SOLAR TECHNOL.AG (`sma-solar-technol-ag-1fa9e8e7`) | 5 | NOT_DISCLOSED: other_names, revenue_by_country, share_price, staff_by_segment; DERIVATION_INPUT_MISSING: market_cap_band |
| Alina Holdings Plc (`alina-holdings-plc`) | 5 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution, total_remuneration |
| Amicorp FS (UK) plc (`amicorp-fs-uk-plc`) | 5 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band; REMUNERATION_REPORT_NOT_READ: benefits_value |
| Electrovac AG (`electrovac-ag-8d562e26`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| PEARL GOLD AG (`pearl-gold-ag-da4e9b62`) | 4 | NOT_DISCLOSED: benefits_value, pension_contribution, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| SINGULUS TECHNOL. EO 1 (`singulus-technol-66103de1`) | 4 | NOT_DISCLOSED: revenue, share_price, shares_outstanding; DERIVATION_INPUT_MISSING: market_cap_band |
| Cloudbreak Discovery Plc (`cloudbreak-discovery-plc`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Critical Metals Plc (`critical-metals-plc`) | 4 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| WOLTERS KLUWER (`wolters-kluwer`) | 3 | NOT_DISCLOSED: lti_vested |
| Bucher Industries AG (`bucher-industries-ag`) | 3 | NOT_DISCLOSED: pension_type, role_disclosure, shareholding_requirement |
| Infomaniak SA (`infomaniak-sa-87b05313`) | 3 | NOT_DISCLOSED: share_price, shares_outstanding; DERIVATION_INPUT_MISSING: market_cap_band |
| Komax Holding AG (`komax`) | 3 | NOT_DISCLOSED: benefits_value |
| The Swatch Group AG (`the-swatch-group-ag-6a144b9f`) | 3 | NOT_DISCLOSED: pension_contribution |
| Vaudoise Assurances Holding SA (`vaudoise-assurances-holding-sa-00d7d6b4`) | 3 | NOT_DISCLOSED: benefits_value; REMUNERATION_REPORT_NOT_READ: benefits_value |
| ORBIS SE O.N. (`orbis-se-3d0d94ff`) | 3 | NOT_DISCLOSED: pension_contribution |
| Planoptik AG (`planoptik-ag-9429909d`) | 3 | NOT_DISCLOSED: pension_contribution, share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| VISCOM SE (`viscom-se-859e40d6`) | 3 | REMUNERATION_REPORT_NOT_READ: base_salary, benefits_value, pension_contribution |
| Acceler8 Ventures PLC (`acceler8-ventures-plc`) | 3 | NOT_DISCLOSED: revenue, role_disclosure, shareholding_requirement |
| Chesterfield Resources PLC (`chesterfield-resources-plc`) | 3 | NOT_DISCLOSED: revenue; REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| Cykel AI PLC (`cykel-ai-plc`) | 3 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Defence Holdings PLC (`defence-holdings-plc`) | 3 | NOT_DISCLOSED: headcount; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Addex Therapeutics Ltd (`addex-therapeutics-ltd`) | 2 | NOT_DISCLOSED: benefits_value, pension_contribution |
| Allreal Holding AG (`allreal-holding-ag`) | 2 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Autoneum Holding AG (`autoneum-holding-ag`) | 2 | NOT_DISCLOSED: pension_contribution; REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Bell Food Group AG (`bell-food-group-ag`) | 2 | NOT_DISCLOSED: benefits_value |
| Carlo Gavazzi Holding AG (`carlo-gavazzi-holding-ag-39d1d1b5`) | 2 | REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value |
| Clariant AG (`clariant-ag-0616ec80`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| CPH Group AG (`cph-group-ag-2a655fb2`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Dätwyler Holding AG (`datwyler-holding-ag-eca04fdb`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Sensirion Holding AG (`sensirion-holding-ag-0c2fb93b`) | 2 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| Stadler Rail AG (`stadler-rail-ag-ddc4f964`) | 2 | REMUNERATION_REPORT_NOT_READ: pension_contribution |
| Züblin Immobilien Holding AG (`zublin-immobilien-holding-ag-cf81b4e5`) | 2 | NOT_DISCLOSED: benefits_value |
| MAX AUTOMATION SE NA O.N. (`max-automation-se-e7586bc1`) | 2 | NOT_DISCLOSED: pension_contribution |
| MUELLER-DIE LILA LOGISTIK SE (`mueller-die-lila-logistik-se-f3c40a4b`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Aseana Properties Limited (`aseana-properties-limited`) | 2 | REMUNERATION_REPORT_NOT_READ: benefits_value, pension_contribution |
| AstraZeneca PLC (`astrazeneca-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Atlas Metals Group plc (`atlas-metals-group-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| B&M EUROPEAN VALUE RETAIL PLC (`b-m-european-value-retail-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| CASTINGS PLC (`castings-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Elixirr International plc (`elixirr-international-plc`) | 2 | NOT_DISCLOSED: share_price; DERIVATION_INPUT_MISSING: market_cap_band |
| Huber+Suhner AG (`huber-suhner-ag-11887265`) | 1 | NOT_DISCLOSED: benefits_value |
| Swissquote Group Holding Ltd (`swissquote-group-holding-ltd-8a2aaa88`) | 1 | REMUNERATION_REPORT_NOT_READ: benefits_value |
| BIOFRONTERA AG NA O.N. (`biofrontera-ag-na-o-n`) | 1 | NOT_DISCLOSED: pension_contribution |
| DEUTSCHE REAL ESTATE AG O.N. (`deutsche-real-estate-ag-8625fa60`) | 1 | NOT_DISCLOSED: pension_contribution |
| FISHER (JAMES) & SONS PLC (`fisher-james-sons-plc-1d273817`) | 1 | FX_RATE_MISSING: market_cap_band |
