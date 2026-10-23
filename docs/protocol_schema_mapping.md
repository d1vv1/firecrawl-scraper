# Protocol fields in the data-point schema

*23 October 2026 · firecrawl-scraper (`python -m extractor.datapoints`)*

The source-validation protocol (`Source_validation_listed_22Oct/PROTOCOL.md`) sets the fields to collect for listed companies: 23 at company grain (C01–C23) and 11 per executive role (R01–R11). This note maps them to our schema, records what was dropped, checks the sources the protocol names, and sets the build order.

**Build order.** In the finished pipeline the free official APIs come first and documents are the fallback. We are building it the other way round: document parsing and scraping first, because they are the hard part and they are needed for every field anyway (as primary source or as fallback). The API step is added afterwards (see "API step, later").

## Output

`output/datapoints.csv` gains two columns, `grain` and `role_row`, making 17:

`company_id, company_name, segment, country, lei, grain, role_row, data_point, value, unit, period_end, source, endpoint, method, retrieved_at, confidence, note`

- **Company grain:** 41 data points, one row each, including the ones not found.
- **Role grain:** one set of 14 rows per disclosed executive role. `role_row` holds the role title as stated; the person's name is added only when two roles share a title. Non-executive board members get one `role_disclosure` row and nothing else, as the protocol says.

The protocol's status values map onto our columns as follows:

| Protocol `status` | Our row |
|---|---|
| `found` | value, confidence A or B |
| `partial` | value with confidence C (quote not found word for word), or a note on what is missing (e.g. "some parts missing") |
| `not_found` | no value; `note` says "not found in: …" with the sources tried |
| `not_applicable` | no value; `note` starts with "not applicable" |

`source_type` maps to `method` (`api` = API, `filed_document` = PARSE/XBRL, `web` = SCRAPE, `derived` = DERIVED). `location` is in `endpoint` (`#page=N`, or a link to the quote) and `note`.

## Company grain

| ID | Field | Our data point(s) | Read from today | Changed |
|---|---|---|---|---|
| C01 | Legal name, former names | `legal_name`, `other_names` | Annual report; legal notice, history page | — |
| C02 | LEI | `lei` | GLEIF (API step) | API step |
| C03 | Registration number | `business_id` | Annual report; legal notice (*Impressum*) | — |
| C04 | ISIN | `isin` | Annual report; "The share" page | — |
| C05 | Ticker, primary exchange | `ticker`, `exchange` | Annual report; share page | — |
| C06 | Segment | `exchange_segment` | Annual report; share page. The prompt now says when the market is an MTF | prompt |
| C07 | Listing status, admission date | `listing_status`, `listing_date` | Annual report; listing notice, share page, history | — |
| C08 | Country, HQ city | `country_code`, `head_office_city` | Annual report; legal notice | — |
| C09 | Website domain | `website` | Annual report; legal notice, about page | **new** |
| C10 | National industry code | `sector_code` | Registers: Brønnøysund (NO), PRH (FI), Companies House (UK); SEC SIC for US registrants. Elsewhere not found | API step |
| C11 | Business description | `sub_sector` | Annual report: now one sentence of the business description | prompt |
| C12 | Revenue | `revenue` | XBRL tag or report | — |
| C13 | Total assets | `total_assets` | XBRL tag or report | — |
| C14 | EBITDA, else operating profit | `ebitda` | Annual report key figures; year-end report. `note` says which measure and whether it is company-defined | **new** |
| C15 | Fiscal year end, currency, accounting basis | `fiscal_year`, `fiscal_year_end`, `reporting_currency`, `accounting_basis` | Pipeline result; annual report | **new**: year end, basis |
| C16 | Headcount and FTE | `headcount`, `fte` | Annual report; sustainability report | — |
| C17 | Shares outstanding | `shares_outstanding` | Annual report; share page | — |
| C18 | Year-end share price | `share_price` | Annual report share section; share page | **now collected** (was "bought") |
| — | Market cap band | `market_cap_band` | Derived: C17 × C18, banded in EUR (≥ €1bn large, ≥ €150m mid, else small) | **derived**; other currencies wait for the year-end EUR rate (API step) |
| C19 | Largest holders, with % | `largest_holders` | Annual report shareholder table; shareholder page, governance report | **new** |
| C20 | Controlling owner (20%+), PE stake (5%+) | `controlling_owner`, `controlling_owner_name`, `ownership_type`, `pe_stake_5pct` | Derived from C19 | threshold now **20% of votes** (was "more than 50% or stated") |
| C21 | Parent company | `ultimate_parent` | Annual report; shareholder page | — |
| C22 | Revenue and staff by segment or country | `revenue_by_segment`, `staff_by_segment`, `revenue_by_country`, `staff_by_country` | Segment note (IFRS 8); year-end and sustainability reports | **new**: by segment |
| C23 | Pension type, benefits, shareholding requirement | `pension_type`, `benefits`, `shareholding_requirement` | Remuneration policy, then report; annual report | **new**: benefits |

`cik` stays: the golden dataset uses it (213 rows) for SEC registrants, and it comes free from SEC filings.

## Role grain

| ID | Field | Our data point(s) |
|---|---|---|
| R01 | Who is disclosed | `role_disclosure` (`individual` / `aggregate`; the note says executive or non-executive board) |
| R02 | Aggregate headcount, who is excluded | `aggregate_headcount` (exclusions in `note`) |
| R03 | Currency and unit of the pay table | `pay_currency` (table unit in `note`) |
| R04 | Base salary | `base_salary` |
| R05 | STI paid | `sti_paid` |
| R06 | STI target and maximum, % of base | `sti_target_pct`, `sti_max_pct` |
| R07 | LTI received, and its basis | `lti_received`, `lti_basis` (grant value, vested value, accounting expense, number of instruments) |
| R08 | LTI target and maximum, % of base | `lti_target_pct`, `lti_max_pct` |
| R09 | Benefits value | `benefits_value` |
| R10 | Pension contribution | `pension_contribution` |
| R11 | Total as stated | `total_remuneration`; checked against R04 + R05 + R07 + R09 + R10, and a difference over 2% is noted |

The validation run listed seven things the scrape must handle. How each is covered:

| Issue | How it is handled |
|---|---|
| Units per table ("in T€" in one header cell) | The AI copies the figure as printed with the table's unit; we convert to full units and keep the printed figure in `note` |
| LTI basis differs | `lti_basis` row for every LTI value |
| Bundled components | `includes` in the AI answer, in `note` ("includes social security") |
| Timing, report versions | Document year in `note`; the fiscal year comes from the report |
| Document access | Remuneration reports are found like the other fallback documents; PDFs are downloaded directly |
| Disclosure depth | One row set per disclosed role, aggregates included |
| Conflicts between filings | The most exact source wins; a differing value goes in `note` |

## Dropped from the schema

| Data point | Why |
|---|---|
| `revenue_model`, `business_structure` | Not in the protocol or the golden dataset. The annual-report pipeline still produces them, because the monday.com push and the coverage report use them. |
| `legal_form` | Not in the protocol or the golden dataset |
| `segments` (names only) | Replaced by `revenue_by_segment`, which carries the names |
| `market_cap` | The protocol only needs the band; the market cap is shown in the band's `note` |

## Source check

Checked on 23 October 2026: live requests where possible, otherwise official documentation. The found rates are from the validation team's run on 20 companies.

| Source in the protocol | Verdict | For us |
|---|---|---|
| **GLEIF API** | Works, free, no login, current | The API step's anchor for C01–C04, C08, C21. Catches: the parent endpoints return 404 for a group's top company (then read the reporting-exception endpoint); the ISIN list is incomplete (4 for Siemens). Missed parents in AT, PT and DE in the validation run. |
| **ESMA FIRDS** | Free Solr API and files; ISIN, venue (MIC) and LEI reliable | **Never for the listing date:** old listings show placeholders (Siemens 1899-12-31; Euronext Paris listings show 2000-09-25, the Euronext merger). Admission date stays a document field. |
| **filings.xbrl.org** | Works; xBRL-JSON available | FY2025 coverage is partial: good for NL, ES, AT, PT; sparse for BE; **none for DE ever**; GR and LU feeds stalled since May 2025. We already use it (ESEF route). |
| National registers (C03, C10) | Free machine access only in CH (Zefix, credentials by email), BE (KBO, free registration) and GR (GEMI, API key). NL KvK is cheap but paid. IT, ES and PT need paid extracts; LU and DE are website-only. | C03 comes from documents and GLEIF `registeredAs`. **C10 national industry code failed the validation (0 found)** and the registers are mostly paid: leave it out of the scrape, or buy it. |
| Exchange segment lists (C05–C06) | Free files: Deutsche Börse (xlsx by segment), SIX (csv), Euronext (csv, market only, no A/B/C compartments, no Athens) | Useful later for C06. BME, LuxSE, Wiener Börse, Athex: no download found. |
| Major-holdings notices (C19) | Free and machine-readable only at AFM (NL, CSV/XML export). FSMA, Consob, CNMV, CMVM, HCMC are web pages or PDFs; Consob and CNMV block scripts. | Annual report first (85% found in the validation run); AFM export as a later extra for NL. |
| Spain IARC / IAGC (R01–R11) | Real documents, filed at the CNMV in a standard format; in practice PDFs | Treated as remuneration reports (the "iarc" keyword is in the document finder). CNMV blocks scripts, so fetch them from the company's site. |
| Italy Relazione, section II, tables 1, 3A, 3B | Confirmed: Consob Schema 7-bis, mandatory and standard | Same as remuneration reports; the fixed table layout helps the AI. |
| National OAMs | One per country; only AFM (NL) has an export | Not needed while company sites work; a fallback for documents later. |

## API step

Built (23 Oct 2026): GLEIF, the registers of NO, FI and the UK, and SEC EDGAR run before any document; documents fill the rest. Still to add, in this order:

Once the document side is solid, the API step goes in front of it, for the fields where an API is exact:

1. **GLEIF:** LEI, legal name and former names, registration number, country and HQ city, parent (direct and ultimate, with the reporting exception), ISINs.
2. **ESMA FIRDS:** ISIN and trading venue (MIC → exchange). Not the admission date.
3. **filings.xbrl.org:** already in the pipeline for revenue and total assets; extend to EBITDA where tagged, fiscal year end, currency.
4. **Exchange files** (Deutsche Börse, SIX, Euronext): segment.
5. **AFM export** (NL): major holdings.
6. **ECB reference rates:** the year-end EUR rate, so `market_cap_band` can be derived for non-EUR companies.

Documents then only fill what the APIs leave empty, and act as a cross-check.

## Open points

- **Market cap band thresholds:** €1bn / €150m are Nasdaq Nordic's segments, used as a placeholder. They need the CDP band definition.
- **C10 industry code:** drop from the scrape, or buy register extracts?
- **Annual-report pipeline:** stop producing revenue model and business structure (saves one AI call per company) once the monday.com board no longer needs them.

## First test against the validation run

Three of the validation team's companies (Kendrion NL, Komax CH, Rosenbauer AT) plus Yubico (SE), run on 23 October 2026:

- **Role grain:** every executive pay figure we found equals the validation team's value: Kendrion CEO and CFO (base, STI, STI target and max, LTI, LTI target and max, total), Komax CEO and the aggregate of the other executive committee members, and Rosenbauer's executive board members. All came from the remuneration report PDF with a page link.
- **Company grain:** close agreement where both read the same year. Differences found:
  - Rosenbauer: the report finder chose the FY2024 annual report (`RB_Annual_Report_2024.pdf` in the 2025 folder), so its share data, EBITDA and headcount are a year old. A report-finder fix, not a schema issue.
  - Komax registration number: ours (`CHE-103.285.290`) is quoted from Komax's own legal notice; the validation file has `CHE-103.485.290`. One of the two is a typo; check the register.
  - Komax EBIT: a fallback web page gave an older year's figure. Yearly figures from fallback documents that aren't dated for the report's year are now graded C, with a note.
- Fixed during the test: shares *outstanding* (not issued); a 20–50% holder is no longer taken as the parent; the company itself is never its own parent; a governance web page without figures no longer counts as the remuneration report; non-executive board members become one row; role titles use the person's function and include people who left during the year.
