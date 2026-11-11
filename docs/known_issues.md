# Known issues

Open problems found during test runs, to pick up later. Newest first. Every issue was checked against the code and the latest run (run 21, Nordic/UK set) on 5 November 2026.

| # | Issue | Status | Needs |
|---|---|---|---|
| 18 | Swiss and German reports not found: the search reads the consumer site, not the investor site | mostly fixed: web search for the report (13 of 19 found, 11 of 12 Swiss/German) | companies with no website and no report the search finds (Bergbahnen Engelberg, IQM, Bluebird, City of London) |
| 17 | Weak links on the High-severity fields (dashboard review against the benchmarking severity workbook) | mostly fixed: every High field up | 19 companies still without a report (report and website finders, issue 4); pay quotes pieced together from separate cells |
| 16 | No way to run companies for only one field or a few fields; the input's `run_required` (Pay Data / Company Data) is ignored | fixed: `--fields`, `run_required` followed, rows merged | — |
| 15 | An annual report found outside the report step isn't used as the report: no fiscal year, revenue or total assets, undated pay | fixed: the input's `annual_report_url`, then the site's documents (FY2025 run 4: 15 of 19 companies now read their FY2025 report) | 3 inputs give a filings.xbrl.org search, not a report |
| 14 | HTML annual reports (ESEF) converted with table rows run together and letters lost to private font codes | fixed | — |
| 13 | The dashboard's import format writes the UK as "UK"; the collector writes "GB" | fixed: both accepted | — |
| 12 | Values the output checks flag: computed figures shown as read, wrong target units, unsupported quotes | mostly fixed; 19 hard fails of 735 values | quotes the AI pieces together from several places; Bang & Olufsen's totals (bonus definition) |
| 11 | Golden file values from an older fiscal year | closed: golden mistakes; we keep the most recent year | — |
| 10 | Definitions (base salary, revenue line, STI, LTI, targets, market-cap bands) | closed: decided on the most widely accepted reading | — |
| 9 | Exchange fields weak from documents (ISIN, ticker, segment, listing date) | mostly fixed: Nasdaq Nordic segments from Nasdaq's lists | Deutsche Börse and SIX segment files; London |
| 8 | Sweden and Denmark registers not connected | parked | credentials; only matters for Swedish private companies |
| 7 | Register industry codes describe the holding company | fixed: sector classified from the business description (NACE Rev. 2) | the Allshares taxonomy, to replace NACE |
| 6 | Holding companies' own filed accounts give no group figures | fixed for the UK: the parent's consolidated accounts, scans read from page images | the ownership chain upwards (Bidco, Midco, Topco); countries other than UK, NO, DK |
| 5 | Run-to-run variation in AI answers | mostly fixed | pay tables Camelot can't use (no total column, people as columns) |
| 4 | Report finder can still pick a subsidiary's or a placeholder report | partly fixed | more guards |
| 3 | SEC name lookup misses some registrants | fixed | — |
| 2 | PDF tables converted with merged columns | fixed for pay tables with a total column | tables with people as columns; tables without a total |
| 1 | Report downloads behind buttons | fixed | — |

## 18. Swiss and German reports not found — mostly fixed

*Found and fixed 11 November 2026, before the DACH runs (`report_finder.web_search_report`).*

**Cause.** Of the 31 companies without a report, 12 were Swiss or German. The search maps the company's website, but DACH reports live elsewhere: an investor domain or report microsite (adidas.com vs report.adidas-group.com; bell.ch vs bellfoodgroup.com), a file server, or a renamed company's new domain (Arbonia's old afg.ch, Bystronic's conzzeta.ch). The map of a consumer site returns product pages, and the guessed `/investors/` page holds nothing.

**Fix.**
- After the first site map, a web search for "<name> annual report 2025 pdf" (2 credits), before guessing an investor page. Only the company's own documents: its site, a host carrying every word of its name, or a PDF named for it; never collectors of other companies' reports (annualreports.com, scribd...). A result is judged by its title when its URL misleads; "ar2025" in a file name counts; semi-annual reports don't. When no PDF is in the results, the best report or downloads page is scraped for it.
- The report's own domain becomes the website when it carries the company's name, so the remuneration report is looked for there.
- No website found: the report is searched for by name alone.
- Report search budget 8 credits (was 6): a website found by a paid search left no room for the web search.
- German, French and Italian section keywords (Mitarbeitende, Umsatz, Bilanzsumme, Verwaltungsrat, collaborateurs, chiffre d'affaires...); "Finanzbericht", "rapport de gestion"; Swiss thousands separators; German listing lines stripped from names ("Porsche AG VZO" -> Porsche).

**Test (FY2025 runs 6 and 6b, 159 credits):** 13 of the 19 found their FY2025 report, 11 of the 12 Swiss/German companies: Adidas, Arbonia, Asmallworld, Banque Cantonale du Jura, Bell Food Group, BKW, Bucher, Burkhalter, Bystronic, Adval Tech, APG SGA; also Essentra and Airtel Mobile Commerce. Perfect fiscal_year in the combined file 92% -> 98%.

**Still open:** Bergbahnen Engelberg, IQM, Bluebird and City of London (no website, nothing found); Aterian (a listing page); Melhus Sparebank (a report web page without a year). Swiss pay: one Swiss report gives both the executive committee's total (with the CEO) and the rest's total (Bachem); and a non-executive board is sometimes read as one person (Aevis, Also, Aryzta, Bioversys).

## 17. Weak links on the High-severity fields — mostly fixed

*Found 11 November 2026, reviewing the dashboard's data (`Dashboard/report.json`, the combined FY2025 file) against `Allshares_Benchmarking_Field_Severity_filled.xlsx`: 14 High fields, 13 Required and `market_cap_band` Required if listed. Aim: every High field passing every check for every company.*

**Found, and done the same day:**

| Weak link | Change | Effect |
|---|---|---|
| The dashboard's severities differed from the workbook on 17 fields (`sector_code` Medium/Optional, `market_cap_band` "Never used") | `accuracy/benchmark_rank_from_excel.py` also takes severity, requirement, reason and fill from the workbook; they override `field_requirements.json` | The dashboard ranks fields as the workbook does |
| 104 companies without a headcount, 53 of them with an FTE count | `datapoints.headcount_from_fte`: the FTE count, rounded half up, is the headcount, method DERIVED, note "derived: full-time equivalents (no headcount stated)" (decided 11 Nov 2026). DER-03 recalculates the rounding | headcount 41% → 61% perfect |
| Values with "US$", "CA$", "£" as currency in merged rows never refreshed | The current rules applied to every saved row of the combined file (`refresh`) | 27 hard fails gone |
| 8 market-cap bands not derived: a share price without a date has no ECB rate | The report's fiscal year end dates an undated year-end price | market_cap_band 35% → 43% (with the reports below) |
| Chesterfield and Cobra read their FY2025 report but showed no fiscal year: it was written only with revenue or total assets | The report's year and its end are written without figures too | |
| Commerzbank's report gave no fiscal year | `year_of_report`: from the year end the report states, else the year in its cover title | |
| K2A, SED Energy, Bluebird: the input's report URL is a filings.xbrl.org search | `read_targets` takes the LEI from it; the report step finds the filing by LEI | K2A and SED Energy read their FY2025 ESEF filing |
| A pay table drawn cell by cell (Flughafen Wien): label and figure in separate boxes, so no quote is one passage | `validate.lone_cell`: the figure printed alone exactly once in the document, on a page holding every word of the quote, is the quote; note "(the figure's own cell; …)" | 28 values now verified |
| Re-scoring a run whose sources are partly on another machine made their quote checks n/a (and so hid failures) | `output_checks.rescore` / `dashboard.build(rescore=True)`: fresh checks, but a check needing a source not cached here keeps its saved result | No status improves without a reason: the 27 hard fails → pass are all the currency fix |

**FY2025 run 5: the 31 companies without a report** (`data/fy2025_run5_no_report.csv`, `output/fy2025_run5_datapoints.csv`; 181 Firecrawl credits). 12 now read a FY2025 report: Adecco, Alina, Alpine Select, Basellandschaftliche Kantonalbank, BSF, Cancom, Chesterfield, Cobra, Commerzbank, Jinhui (its own ESEF filing, USD 157.5m revenue), K2A and SED Energy. Still none, 19: the report search fails (Adidas, Adval Tech, Arbonia, Asmallworld, Aterian, Banque Cantonale du Jura, Bell, BKW, Bucher, Bystronic on its old domain conzzeta.ch, Essentra; Burkhalter only FY2022), the website search fails (Airtel Mobile Commerce, APG SGA, Bergbahnen Engelberg, Bluebird, City of London Investment, IQM), and Melhus Sparebank's report is a web page without a year. These need work on the finders (issue 4), not another run.

**Merging into the combined file:** a company run here for the first time under "Pay Data" has no saved rows to merge into, so its company fields come out "not collected"; such a row must not replace a value in the combined file (74 values of Adecco, BLKB and Cancom were restored after the run-5 merge).

**High fields, perfect (filled and passing every check), before → after:** headcount 41 → 61%, market_cap_band 35 → 43%, total_remuneration 61 → 64%, base_salary 75 → 77%, revenue 76 → 78%, role_disclosure 87 → 88%, fiscal_year 88 → 92%, pay_currency 91 → 93%, sub_sector 91 → 92%, listing_status 96 → 97%, legal_name and country_code 98 → 99%; sector_code 96% and reporting_currency 94% unchanged.

**Still open:**
- the 19 companies above (12% of the High-field gaps for the company fields);
- pay quotes the AI pieces together where the table isn't drawn cell by cell (the prompt already asks for one continuous passage); a space-insensitive match would clear only 26 of 293 quote failures;
- `market_cap_band`: 112 companies lack a share price or share count; reading the market capitalisation the report states would be the next lever;
- headcount still missing for about 1 company in 5.

## 16. Runs always collect every field — fixed

*Noted 11 November 2026; **fixed the same day** (`extractor/fields.py`; README, "Only some data points").*

**Built, as planned below:**
- `--fields` takes names and groups (`pay`, `company`, `ownership`, `listing`, `financials`, `staff`). `pay` also holds `fiscal_year` and `fiscal_year_end`: they date the pay rows, so a pay-only run keeps them in step. A derived value brings what it rests on (`market_cap_band` → shares and price, `sector_code` → the description).
- The report AI pass, the document fallback and the sector call ask only for the selected fields; the pay step runs only for pay fields; the report search is skipped when every field is one an API gives (`fields.API_FIELDS`), and a report found before is reused. Firecrawl is not used at all when only API fields are asked for.
- The run replaces only the selected rows in `output/datapoints/<id>.json` (`fields.merge`); the others keep their values and `scraper_version`. A field never collected gets an empty row, "not collected: this run asked only for …". Role fields: all of them replace the whole role block; some of them are replaced per role.
- `run_required` is followed by default ("Pay Data" → `pay`, "Company Data" → `company`); `--ignore-run-required` turns it off. With `--fields` as well, a company gets what both ask for, and is skipped when that is nothing.
- With `--fields`, a company done before runs again only when a field asked for has no value (a top-up); `--redo` runs them all.
- `--dry-run` prints each company's fields, steps and worst-case credits. FY2025 run 2: 100 companies, at most 1,010 credits with `--redo`.

**Still true:** the AI answer cache is keyed by the facts asked for, so a run for a few fields asks the AI afresh and can get a different answer for them than a full run (issue 5).

**Original note.**

**Now.** `python -m extractor.datapoints` always collects all data points for each company: the free APIs, the report search and read, executive pay, and the document fallback for whatever is still missing. Options choose companies (`--only`, `--limit`, `--redo`, `--outdated`) and limit spending (`--no-docs`, `--doc-credits`, `--max-run-credits`), but none chooses fields. The input's `run_required` column ("Pay Data", "Company Data", "Company and Pay Data", from the tracker) is read by nobody: a company that only needs pay still has its company fields collected, and the reverse.

**Why it matters.**
- Topping up one field across many companies (headcount, `lti_target`, the exchange segment) costs a full run per company today.
- After a fix to one field, `--redo` re-runs everything for every company, and the AI's answers for unrelated fields can move between runs (issue 5).
- The tracker already says which half each company needs; following it would skip work and credits.

**Change (about a day).**
1. `--fields revenue,headcount` or groups (`--fields pay`, `--fields company`, `--fields ownership`). The gap list (`gap_list`), the fields asked of the AI (`wanted_fields`) and the document fallback are limited to them. Steps a field doesn't need are skipped: the pay step without pay fields, the report search when every field asked for comes from an API, and the report already found is reused from the cache when there is one (no credits).
2. Merge, not replace: the run updates only the chosen fields in the company's saved rows (`output/datapoints/<id>.json`); the other rows, and their scraper version, stay as they were.
3. Follow `run_required` by default: "Pay Data" runs the pay fields only, "Company Data" the company fields only; an option turns this off.
4. A dry run shows, per company, the steps that would run and their worst-case credits.

## 15. An annual report found outside the report step isn't used as the report — fixed

*Found 11 November 2026 in FY2025 run 2 (Tallink Grupp); **fixed the same day** (`datapoints.use_as_report`, `find_annual_report`; `documents.title_year`).*

**The cause was narrower than first written.** Tallink's annual report was not found by the document step: it was already in the input's `annual_report_url`, which only the pay step read (the report step took the column only for `file:` links). So the workaround below was already in place and did nothing. The report search itself had only the archive pages `annual-reports-2015` … `2024` and chose the AGM PDF.

**The fix.** When the report step read no report, or one older than last year (`sought_year`: FY2025 during 2026), the report step runs again on a report found elsewhere, and its result replaces the old one (only when newer; the error file goes):
1. the input's `annual_report_url`, before the API step, so the pay step and the report pass use it;
2. otherwise the site's documents: a new `annual_report` document type (about 15 languages), candidates dated before the year left out, and a document used only when it plainly is that year's report (`title_year`: 40 pages or more, an annual-report title with the year on its first 3 pages, not "Annual report on remuneration"). A reports page that isn't one adds its links, and the second try can be the PDF.

The report step and the document library cache a PDF's conversion under different names; it is now copied between them (Tallink's 177 pages took 4 minutes to convert). On cached reports the title test accepts Equinor (FY2025) and Bang & Olufsen (2025/26 → 2026), and rejects remuneration and sustainability reports; Marimekko's "Financial Statements and Report of the Board of Directors" has no annual-report title and is not accepted, which errs on the safe side.

**Tallink re-run (pay fields, its `run_required`):** report FY2025, year end 2025-12-31, revenue €765.3m and total assets €1,330.8m in the report step's result; every pay row now dated 2025-12-31; `fiscal_year_end` 2025-12-31 (was 2023-12-31, from the share page); `benefits` found on page 106. 0 Firecrawl credits, 140 s. The pay figures are unchanged. The report's values are graded C by the identity check: the input says FI and the report EE (Tallink is Estonian, listed in Tallinn and Helsinki), and GLEIF found no LEI under the name in FI. The input's country should be EE.

**Reach:** a dry run of FY2025 run 2 showed 18 of 100 companies whose `annual_report_url` the report step left unused (it failed or read an older year), Endeavour Mining among them (it read FY2024; the input names the FY2025 PDF).

**FY2025 run 4 (11 November 2026): those 18 and Tallink re-run** (`data/fy2025_run4_found_reports.csv`, `output/fy2025_run4_datapoints.csv`, merged into `fy2025_runs_datapoints.csv`; 52 Firecrawl credits):
- **15 now read their FY2025 report** (fiscal year, year end, revenue and total assets, every pay row dated): Canal+ (was FY2024), Endeavour Mining (was FY2024), Emilshus Pref, Voss Veksel, UIE, Brøndby (an ESEF annual filing ending 2026-06-30), Ostasiatiske, Addtech, Arzneiwerk, Atlantic Petroleum, Basilea, Revolutionrace (2025/26), S.D. Standard ETC and Tallink. Their values checked went from 627 to 791, the pass rate from 64% to 89%.
- Endeavour Mining and Addtech are "Pay Data" companies: their fiscal year and pay are the new report's, while their revenue and total assets rows stay from the earlier run, with that run's period end.
- **3 inputs give no report:** K2A Pref, SED Energy and Bluebird Mining's `annual_report_url` is a filings.xbrl.org search (`/api/filings?filter[entity.identifier]=<LEI>`), a list of filings. The LEI in it would let the report step find the filing itself; the input should give the LEI (or the filing's report) instead.
- **Chill Brands:** the supplied Companies House filing is FY2024, no newer than the report read before; kept.
- **Jinhui Shipping: a guard added.** The site search found `jh2025ARe_3371.pdf`, the annual report of Jinhui Holdings, its Hong Kong parent. The identity check flagged it (HK, another legal name), but the first run still used it. A report found on the site is now used only when it passes the identity check; otherwise the report step's files are restored and its values dropped. A report the input supplies stays trusted, since the name check also flags trade names (RVRC Holding for Revolutionrace, Det Østasiatiske Kompagni for Ostasiatiske). Jinhui was re-run under the guard and is as before: no report (its own FY2025 report isn't on its site).
- Identity check grades C on 5 of them; 4 look like false alarms from the name check (Revolutionrace, Ostasiatiske, Brøndby, Addtech Nordic: names that differ from the legal one), and Tallink's input country is FI where the report says EE.

**Original note.**

**Symptom.** Tallink got 62 values, 36 of them from its FY2025 annual report, yet it shows no fiscal year, revenue or total assets, its executive pay has no period end, and the dashboard counts it as having no FY2025 report.

**Cause.** A company is read in two stages. The report step finds the annual report and reads the core figures from it: fiscal year, fiscal year end, revenue, total assets. The year end also dates the pay rows. The document step then fills fields still missing from other documents. For Tallink the report step chose a one-page image of the 2023 supervisory board report (`AGM-2024-AS-Tallink-Grupp-Supervisory-Board-report-2023-eng.pdf`), found no text in it, had no other candidate and failed. The document step later found `tallink-annual-report-2025-eng.pdf` (177 pages, "Annual Report 2025", financial year 1 January to 31 December 2025) and read pay and other fields from it, but only fills gaps: the core figures, the fiscal year and the dates stay empty.

**Workaround (did not work, see above).** Put the report's address in the input CSV's `annual_report_url` column and run the company again; the report step then reads that file.

**Fix (about half a day).** When the report step has failed, or read a report older than the year sought, and the document step reads a file that is plainly the annual report for the year (titled "Annual report 2025" or the local equivalent, a financial year ending in that year, tens of pages or more), use it as the report: read the core figures from it as the report step would, take its fiscal year and year end, and date the values with them. This helps every company whose report search misses but whose website links the report elsewhere.

Related: the report step's choice of a board report over the annual report is issue 4 (the report finder can still pick the wrong document).

## 14. HTML annual reports converted badly — fixed

*Found 5 November 2026, looking for why AO World's annual report gave no headcount, EBITDA, owners or segments; **fixed the same day** (`extractor/xhtml_text.py`, version 3).* An ESEF annual report is a PDF redrawn as HTML, and three of the six in the Nordic/UK set came out of the converter damaged:

- **Table rows run together** (AO World, Novo Nordisk): the filing places every line as a positioned `<span>`, with no tag between rows, so "Sales, marketing and distribution 2,884 3,133Directors (Executive and Non-Executive) 8 72,892 3,140". A positioned box now starts a line, and boxes at the same height (within 4 px) stay on one line, since Bang & Olufsen draws each cell as its own box. Runs of glued figures: AO 172 → 1, Novo Nordisk 336 → 1.
- **Letters lost to private font codes.** AO World's font draws "fi", "fl", "ff" and "ffi" as private-use glyphs, which were dropped: "nancial" (139 times), "pro t", "bene ts". Bang & Olufsen's text is in a shifted font, every letter moved by 0xE5E3 and its digits by another offset (14,842 glyphs): headings such as "At a glance" and its key-management pay note were unreadable. Both are decoded from the words the same report spells out in plain text (a digits font: the shift that turns its figures into years). Nothing is hard-coded per company.
- A drawn table's row has no "|", so a quote that skips cells ("John Roberts FY26 461,262") is now matched within one line that holds three figures or more (`validate._in_one_row`).

Shell, Equinor and Marimekko convert as before (same words), plus line breaks at table rows. The cached conversion carries the converter's version (`_x3.md`), so every ESEF report is converted again on its next run.

Nordic/UK set after re-reading the three: AO World gains its staff number (2,892) and owner type; Novo Nordisk its FTE and staff by country; Bang & Olufsen its sector (its business description is readable now) and its key-management pay note.

## 13. The dashboard's import format spells the UK "UK" — fixed

*Found 5 November 2026, when the accuracy dashboard was connected to the collector (`Dashboard/README.md`).* The import schema (`accuracy/schema/allshares_import_schema.json`) allows `UK` as a country code, not ISO `GB`, which the collector writes. A CSV imported on the dashboard's Import page that gives `GB` is rejected, and one that gives `UK` doesn't match the UK companies already in the run when it has no LEI (companies are matched by LEI, otherwise by name and country). Imports with an LEI are not affected.

**Fixed 5 November 2026** (`Dashboard/core/report-core.js`, `previewImport`): an import may give `UK` or `GB`; both pass validation and are stored as `GB`, so the row matches the run's UK company by name. The schema file is unchanged, so the client's own `UK` files keep working.

## 12. Values the output checks flag — mostly fixed

*Found 3 November 2026 by `python -m extractor.output_checks` (`docs/output_checks.md`) on the Nordic/UK set; **fixed the same day**. Hard fails went from 46 of 710 values to 26 of 716; the golden pay match stayed at 120 of 148.*

| Found | Fix | Now |
|---|---|---|
| Shell's STI maximum "200% of maximum"; the quote says 200% of target | New target form "% of target" (`pct_of_target`); code turns it into % of base salary: 200% × 125% target = 250% (DERIVED, `pay.derived_max`) | 250% of base salary |
| AO World's maximums 100% and 200% not in their quote ("300% of salary") | The pay prompt: every value is one number printed in its quote; never add, multiply or work out. Code grades a figure missing from its quote C ("the figure … is not in the quote") | 300% of base salary, as quoted |
| Nokia's CEO LTI target 8.4m = 2.8m + 5.6m, maximum 16.8m = 200% of it | Same rule and guard | Not given (the report states no single figure) |
| Bang & Olufsen's shares outstanding worked out by the AI (the prompt asked it to subtract treasury shares) | The prompt asks for shares and treasury shares as printed; code subtracts when the share count isn't already "outstanding" | 142,607,006, DERIVED with "147,326,503 issued − 4,719,497 treasury shares" |
| BioArctic "R&D: 69" (69 percent) as a headcount | The prompt: breakdown items are amounts or people, never percentages; code drops a breakdown whose figures the quote prints as percentages | Not given |
| Marimekko's website from "available at Marimekko's website" | The domain must be in its quote | marimekko.com, from a quote that prints it |
| A long name cut mid-word across table cells ("Executive Vic\|e President") kept quotes from matching | The quote lookup joins a label row's cut words (`validate._in_one_row`) | Bang & Olufsen's pay rows found on page 12 |

**Not errors after all:**
- **Shell's pension "in lieu of pension".** The report says "Wael Sawan and Sinead Gorman received cash in lieu of pension contributions equal to 20% of base salary". The note now says it is derived, which DER-06 asked for. A guard still moves a plain "Pension" column with no in-lieu wording to pension.
- **LTI as an IFRS 2 expense** (BioArctic, Bang & Olufsen, Marimekko). The client's golden file uses the expensed figure for these companies (BioArctic CEO 1,650,000; Bang & Olufsen 7,079,000), so the check now accepts it as a stated basis.
- **A total above its parts** (BioArctic's CEO: a 3,004 column outside our fields). This is now a soft check (XF-02). Parts above the total stay a hard fail (XF-01).

**Still flagged: 30 hard fails of 720 values in run 21 (4 November), 26 of 716 on 3 November.** The four extra came from AI answers that changed when the description prompt changed (issue 7) made the report pass ask every field again, not from new code. By cause:
- **Quotes the run itself couldn't find (21, all graded C by the run).**
  - 12 are long quotes: business descriptions (AO World, Equinor, Volvo), breakdowns (Equinor's revenue by country, Volvo's segments and staff by country) and 6 of Bang & Olufsen's pay values. The note keeps only the first 160 characters, but that is not the cause: checked on 5 November, Volvo's description joins a sentence from the report with one that isn't in it, so the run is right not to find it. Keeping the full quote would not clear these.
  - 9 are short quotes not in the source: Volvo's pay table (3; its text is stored in fragments, "70 8 8 0", which Camelot can't read either), the "role disclosure" quotes of Nokia, Novo Nordisk and Volvo, Nokia's share count, Shell's PE-stake answer and Equinor's share price.
- **Parts above the stated total (4: Bang & Olufsen 3, Nokia 1).** Bang & Olufsen's "Total Remuneration Granted" includes the annual bonus *expensed*, while the AI took STI as "Cash Bonus Paid", which is what the golden file uses. This is a definitions question for the client (issue 10). It varies between runs because the table has no total column for code to check (issue 2). Nokia's former CEO is 4% over.
- **A figure not in its quote (4).** Shell's EBITDA (56,135 is not in the quoted line), Shell's controlling owner (Shell RDS Holding B.V. is not in the quote), Volvo's CEO base salary (22,868, Volvo's fragmented table again) and Nokia's former CEO's benefits (19,697).
- **An incomplete date (1).** AO World's listing date is "2014-03": the source gives a month, not a day.

**5 November 2026 (later): quote matching.** Most quotes that failed were real text in a shape the matcher didn't know, not invented. Now matched (`extractor/validate.py`, `pay_tables.row_quote`):
- a label wrapped over table cells, cut mid-word in some places ("Executive V|ice President") and between words in others ("(until|14-05-26)"): compared without spaces, for quotes of 40 characters or more (Bang & Olufsen's pay rows);
- a table cell grouped with plain spaces, "|22 868|", as one figure (Volvo's CEO salary);
- a quote that leaves words out with "...", when its parts are in the text in order and close together (Volvo's STI maximum, Nokia's board pay);
- a quote built from a pay table: as much of the row label as the page holds, with the cells.
"% of target" is also a valid stated unit (Bang & Olufsen's "maximum payout of index 200"). Nordic/UK set, same values: hard fails 32 → 19, values graded C by the run 38 → 23. Left: 4 totals whose parts exceed them (Bang & Olufsen 3: the bonus definition; Nokia's former CEO), and 15 quotes the AI pieced together from several places or that are not in the text.

**Next:** ask the AI to quote one continuous passage (a prompt change, which asks every field again, so it should come with a fresh comparison run); treat a month-only listing date as the first of the month with the precision noted.

## 11. Golden file values from an older fiscal year — closed: we keep the most recent year

*Found 24 October 2026, Nordic/UK test; **closed 5 November 2026**.* Some golden values are for the year before the report we read: Nokia's golden revenue €19,220m and total assets €39,149m are FY2024 figures labelled FY2025 (our FY2025 tagged figures are €19,889m and €37,597m), and Bang & Olufsen's golden pay is FY2024/25 where we read FY2025/26. These are mistakes in the golden file. The collector always takes the most recent report, and that stays.

The golden file is a reference, not the truth: the client collected it much as we do, from the same reports, with its own reading errors and conventions. A difference from it is a reason to look, not proof that we are wrong.

## 10. Definitions — closed: decided on the most widely accepted reading

*Found 23–24 October 2026; **decided 5 November 2026**.* The client is unlikely to rule on these, so each follows the most widely accepted reading. Each is one setting if a different choice is wanted later.

| Question | Decision | Why |
|---|---|---|
| Base salary: fixed salary only, or total fixed pay (base + benefits)? | Fixed salary only | What remuneration reports and the protocol (R04) call base salary; benefits are their own field (R09). BioArctic's golden CEO base 4,967k is our base 4,846k + benefits 122k |
| Revenue when a filing tags both "revenue" and "revenue and operating income" | IFRS revenue, the other in `note` (`datapoints.REVENUE_RULE`) | The line IFRS 15 defines as revenue (CTT: 1,129m, not 1,292m) |
| STI paid | The bonus earned for the year, as the report states it paid or awarded | Bang & Olufsen's "Total Remuneration Granted" counts the bonus as expensed instead; the stated total is kept as printed, and its difference from the parts stays flagged (XF-01) |
| LTI | Two fields: vested (realised) and granted; an IFRS 2 expense only when that is all the report gives, and the note says so | Reports give one or both, on different bases; one merged field would mix them (Novo Nordisk's golden LTI matches neither) |
| Target or maximum the report doesn't state | Left empty | A target is not always half the maximum (Bang & Olufsen: 100% and 175%; many Nordic policies state only a maximum). The golden file's "target = half the maximum" (all 1,535 rows that have both) is the client's own fill-in, not something the reports say; it was tried and removed on 5 November |
| Market-cap bands | Nasdaq Nordic's cap segments: large ≥ €1bn, mid ≥ €150m, else small (`datapoints.MARKET_CAP_BANDS_EUR`); other currencies at the ECB rate on the share price's date | The thresholds Nordic exchanges use for their own Large, Mid and Small Cap segments |

## 9. Exchange fields weak from documents — partly fixed

*Found 23 October 2026; **partly fixed 26 October 2026** (`extractor/listing.py`, in the API step):*

- **ESMA FIRDS** (the EU regulator's list of every share traded on an EU venue), searched by LEI: ISIN, the exchange where the company itself asked to be listed, and listing status. All graded A.
- **ISO 10383 MIC list:** the exchange's name, which exchange a segment code belongs to, and regulated market vs MTF. An MTF growth market (First North, Euronext Growth) is written as the segment.
- **OpenFIGI:** the ticker, in Bloomberg spelling ("VOLVB"); a document's own spelling ("VOLV B") is kept when it agrees. UK and Swiss companies (not in FIRDS) get their ISIN, exchange and ticker here.
- **Listing date:** FIRDS's first trading date only for listings since 2000 and not on a known system date, graded C, so a document's date wins.

Nordic/UK test: ISIN 10 of 10 (was 5), exchange fields 51 of 60 (was 47); Novo Nordisk's ticker went from its New York ADR (NVO) to NOVOB. Aker Carbon Capture has no FIRDS records.

**5 November 2026: Nasdaq Nordic cap segments.** For a share on Nasdaq Stockholm, Copenhagen, Helsinki or Iceland, the segment (Large, Mid or Small Cap) comes from Nasdaq's own list of each segment (`listing.nasdaq_segment`, graded A), in place of whatever wording a document used ("Large Cap Stockholm", "Nordic Main Market"). Nordic/UK set: Nokia, Volvo, BioArctic and Novo Nordisk Large Cap; Marimekko and Bang & Olufsen Mid Cap.

**Still open:** Oslo Børs has no cap segments on its main market (Equinor stays empty); Deutsche Börse Prime/General Standard and SIX segments need their own files; London ("Official List", from documents). Old listing dates stay a document field.

## 8. Sweden and Denmark registers not connected

*Parked 25 October 2026.* Bolagsverket (SE) and CVR (DK) would give industry codes, and for private companies filed accounts (SE) and owners (DK). For listed companies they add little: identity comes from GLEIF, owners from the annual report, and Danish filed accounts already come from virk.dk without a login. Access: Bolagsverket by a free request form that sends keys by SMS (a Swedish phone number may be needed); CVR by email to cvrselvbetjening@erst.dk. **Revisit if the company list has many Swedish private companies.** Code to port: the colleague's `extras/collect_company_data.py`. Variables: `BOLAG_CLIENT_ID`, `BOLAG_CLIENT_SECRET`, `CVR_USER`, `CVR_PASSWORD`.

## 7. Register industry codes describe the holding company — fixed

*Found 25 October 2026; **fixed 4 November 2026** (`extractor/sector.py`).* Companies House gives Shell plc and AO World plc the code SIC 70100 ("activities of head offices"), and PRH gives Nokia TOL 70100: the register codes the listed parent, not the business. Registers also exist only in the Nordics and the UK. The client's validation decided to **derive the sector from the business description (found for 97%)**, and this is now that route:

- The business description (`sub_sector`) is classified by one small AI call into a **NACE Rev. 2 class** (the EU's list of 615 classes, `data/nace_rev2.tsv` from Eurostat). The segment names help the AI read it; their revenues are not given, because an energy group's trading revenue dwarfs its production (Shell and Equinor became "fuel wholesale" when they were). Code checks that the class is in the list; a vague description gets no class.
- The value is `NACE 06.10`, method DERIVED, graded like the description it rests on. The note gives the class name, the words it rests on, and the register's own code: "register code SIC (UK) 70100 (Companies House) describes the parent company, not the business", or "…, the same class" when they agree (Equinor: NACE 06.100).
- The register's code is the value only when there is no description to classify.
- **The Allshares taxonomy** replaces the NACE list without code changes when it arrives: `SECTOR_TAXONOMY=<file>` (code, optional level, name) and `SECTOR_SCHEME=<name>`.
- The data-point prompt now asks for a description sentence that says what the company makes, sells or provides, not a sentence about a market (AO World's was "Given the size of the overall mobile market…"; Bang & Olufsen's was about segment reporting).

Nordic/UK set (run 21, 4 November): 9 of 10 companies have a class, against 4 register codes before, 3 of which named the holding company. Shell and Equinor are 06.10 (crude petroleum; Equinor's register agrees), Volvo 29.10, BioArctic and Novo Nordisk 21.20, Aker Carbon Capture 28.99, Nokia 26.30, AO World 47.19, Marimekko 14.19. Bang & Olufsen has none: its report again gave a sentence about segment reporting as the description. A classification is a judgement: Marimekko is "manufacture of wearing apparel" here and "retail sale of clothing" in its register. Both are defensible for a design company that sells through its own shops.

## 6. Holding companies' own filed accounts give no group figures — fixed for the UK

*Found 25 October 2026; **fixed 4 November 2026** (`registries._gb_filing`, `extractor/ocr.py`).* For a UK holding company, Companies House holds the parent's own accounts: TWMA Group Limited's tagged accounts have only investments, no revenue, and 0 employees (the staff are in its subsidiaries).

- **Where the group figures are.** A UK subsidiary that uses the audit exemption files its parent's consolidated accounts under its own number, as a separate filing (type PARENT_ACC, "Consolidated accounts of parent company for subsidiary company period ending 31/12/25"). When the company's own tagged accounts have no revenue and such a filing exists for the same year, that filing is read instead. A company whose own accounts have revenue keeps them. So do PDF-only accounts, which can't be told apart from a trading company's.
- **They are often a paper scan** (TWMA's: 80 pages, no text). A scanned register filing is now read by the AI from page images: 4 pages per call, 4 calls at a time, cached per page (`ocr.py`, prompt `ocr_system.md`). A call that times out is split into one call per page. A page that still fails stays empty, and is tried again on the next run. `OCR=0` turns this off. Scanned reports on websites are still skipped.
- **The parent's name is not the company's.** The accounts are BP INV3 TOPCO LTD's. Name, number, country and listing status read from them are dropped, and every value from them says "group figures from the parent company's consolidated accounts (BP INV3 TOPCO LTD)". The identity check is skipped for them.
- **The register is also tried when a website was given but has no report** (TWMA's twma.com had none, so the register was never reached before).
- A pay AI call whose reasoning runs to the output limit now skips that source instead of failing the company (TWMA's parent accounts have directors' pay, not an executive pay table).

TWMA Group now: revenue USD 67,419k (its website says "$67.4m"), total assets 98,806k, EBITDA 18,679k (company-defined), 592 staff on average, revenue by country, PE owner (Buckthorn Partners), sector NACE 39.00 (waste management). Before: only the revenue, from a web page.

**Still open:** the PSC chain upwards (Bidco, Midco, Topco) is not followed: the register's own PSC data is unreliable there (Midco's record names "Os" as its owner). Norway already prefers the group (KONSERN) accounts; Denmark reads the group figures when the XBRL file has them.

## 5. Run-to-run variation in AI answers

*Found 24 October 2026; **tested 26 October 2026**.* The temperature was already 0 (`llm._parse`). Asking Gemini 2.5 Flash the same Equinor pay question three times still changed 25 of 136 values; a fixed seed (36 changed) and the thinking levels `minimal` (18) and `low` (25) did not fix it (`high` timed out). **Every value that changed was in the merged table columns of issue 2** (benefits, pension allowance, other fees); clean columns came back identical each time. So the fix is issue 2, not a model setting.

**29 October 2026: pay amounts now come from the table where one is usable** (issue 2, `extractor/pay_tables.py`). Three fresh runs of the 10-company set (pay answers and table mappings cleared before each) scored 118, 120 and 120 of 148 golden pay figures, against 98 to 121 before. Equinor scored 91 of 91 and Novo Nordisk the same in all three runs. The rest of the spread is Bang & Olufsen (1 to 3 of 17), whose table has no total column and so keeps the AI's reading.

Meanwhile answers are cached per prompt and chunks, so a run without prompt changes is stable. **Seen again 5 November:** when the exchange segment started coming from Nasdaq, the list of open fields changed for every company, so the report pass asked the AI again even where the text was unchanged. BioArctic's owner type moved from family to subsidiary, Volvo's staff by country got a different breakdown, Marimekko lost its segments. Any change to the gap list re-rolls these answers. A changed gap list or prompt asks again and can move such values: when the exchange lists filled Equinor's ISIN, the document step asked for a different set of facts and Equinor's `staff_by_country` was not found that time. Mitigations: keep a reviewed snapshot of the cache before prompt changes; flag a role whose parts don't add up to its total (already noted by the R11 check).

## 4. Report finder can still pick a subsidiary's or a placeholder report

*Found 23–24 October 2026.* Fixed so far: Siemens (a Dutch financing subsidiary's report; now "plc"/legal-form and unexplained-word guards), Volvo (Volvo Treasury AB's report; now group-function words such as "treasury" rank lower, and report PDFs in event folders are kept), Rosenbauer (an older English report beat a current German filing), Jumbo (a year written as a date, `31122025`). An identity check grades values C when the report's own company name or country differs. **Still open:** a dated placeholder page can outrank a report-downloads page (Equinor's "annual-report-2025" vs "annual-reports"); subsidiaries with unremarkable file names are not caught before extraction. Fix options: prefer report-hub pages when choosing which page to scan; check the report's cover page before extracting from it.

## 3. SEC name lookup misses some registrants (Novo Nordisk) — fixed

*Found 24 October 2026; **fixed 25 October 2026**: name matching now joins a legal form written as separate letters ("A S" = "A/S", "S A", "N V", "S P A"), and the SEC lookup also tries the LEI's legal name. Novo Nordisk is found (CIK 353278). A company without an LEI can also be identified in GLEIF by its ISIN or register number (optional `isin` input column).*

*Original note:* `edgar.find_cik` matches on the company name only, and Novo Nordisk A/S (an SEC registrant with ADRs, ticker NVO) is not matched ("no SEC registrant with this name"), presumably because the SEC spells the name differently. Fix options: look the CIK up by ticker or ISIN as well; or accept the LEI's legal name and former names as alternatives; or list known name variants ("A/S" = "A S").

## 2. PDF tables converted with merged columns (Equinor pay table)

*Found 24 October 2026; **fixed for pay tables with a total column, 29 October 2026**.*

**The fix (built from `docs/pay_table_plan.md`).** pymupdf4llm still converts every page, and its text is what the AI reads and what quotes are checked against. On the pages that look like pay tables (`pay.table_pages`, up to 6), `extractor/pay_tables.py` then:
1. reads each table with Camelot (stream mode), dropping prose read as columns;
2. asks one small AI call, cached per table, which rows are this year's executives and which columns make up which field (rules in `prompts/pay_columns_system.md`), from the grid by row and column number, each column's header words and the page text;
3. adds up the mapped cells in code;
4. keeps a row only if its parts add up to the table's own total (2%).

A table is not used when it is for another year (Equinor's 2024 table on page 16), has no total column, maps one column to two fields, or has no base salary. Each checked row replaces the amounts of the role the pay AI call found for it (matched by name, title or base salary); titles, targets and maxima stay from the AI. Quotes are the person plus the cells added ("Anders Opedal | 96 | 23"), graded B with the page. `PAY_TABLES=0` turns it off.

| 10-company set, golden pay figures (of 148) | Result |
|---|---|
| Cached AI answers, before | 98 |
| The same cached AI answers, with tables | 123 |
| Three fresh runs, with tables | 118, 120, 120 |

**Not covered yet**, so these still rely on the AI's reading of the converted text:
- tables with people as columns (Nokia, Marimekko; rejected because one column maps to several fields);
- tables without a total column (Bang & Olufsen, whose figures then vary between runs);
- pay given in prose, and non-PDF sources (ESEF XHTML: Shell, AO World).

A missing column smaller than 2% of the total passes the check: leaving out Equinor's CEO's fringe benefits (23 of 2,213) would not be caught.

The original analysis follows.

**Symptom.** Equinor's executive pay matches the golden file on one run (89 of 91 figures) and not on another. Benefits once matched 1 of 13.

**Cause.** The PDF-to-text conversion (pymupdf4llm) merges two columns of the pay table into one cell and cuts header words at the wrong places:

```
| ... | Fees / Fixed salary addition | One-y / Other fees / Fringe benefits | ear variable / AVP | ... | Extraordinary items / Pensi | on expense | ...
| Anders Opedal | 1,242 | 224 | 96<br>23 | 292 | 306 | 0 | 0 | 30 | 2,213 |
```

"Other fees" (96) and "Fringe benefits" (23) share one cell, so every label after it sits partly over the wrong number. The AI usually still reads it right, but not always; telling it to split such cells made it shift every later column by one (LTI 0 of 13), so that instruction was reverted.

**Fix options.** Keep column boundaries in the conversion (pymupdf4llm table settings, or a table extractor such as pdfplumber/camelot for pages with pay tables); or read pay tables from the PDF layout (cell positions) rather than from converted text; or a consistency check that flags a role whose parts don't add up to its stated total (the R11 check already notes this).

**Tested 26 October 2026: send the pay-table page as an image too.** Equinor's 2025 remuneration report, the same prompt and text, with PDF page 15 rendered at 150 dpi attached and one added sentence (the text conversion can merge columns; read each figure from its own column in the image; copy quotes from the text). Scored against the printed table (13 executives × 7 fields = 91):

| | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---|---|---|---|---|
| Text only (today) | 67 | 91 | 91 | 67 | 84 |
| Text + page image | 91 | 91 | 91 | 91 | 91 |

The bad text-only runs put the salary addition into benefits (CEO: 343 = 224 + 96 + 23) and leave the allowance empty, or drop an executive. With the image all five answers were identical and fully right. Cost: about 1,900 more prompt tokens per page (+7% on this call). Quotes still come from the text, with the merged cell written as two cells ("96|23"), which the quote lookup matches.

**Built and tested on the 10-company set, 26 October 2026: not a reliable win, so off by default** (`PAY_PAGE_IMAGES=1` in `.env` turns it on; `pay.table_pages`, `pay.page_images`). The pay step shows up to 4 pages that look like pay tables (many numbers, several pay words). Each answer is now repeatable for a given input, but small changes to the added instruction moved the golden pay match a lot:

| Run | Golden pay match (of 148) | Equinor (of 91) | Role values graded C |
|---|---|---|---|
| Text only, before | 119 | 89 | 10 |
| Images, "copy quotes from the text" | 121 | 88 | 38, then 22 after the row-quote fix |
| Images, "quote the row, starting with the person" | 119 | — | 33 |
| Images, "quote the row exactly as the text gives it" | 109 | 77 | 40 |
| Text only again, asked afresh (images off) | 98 | 66 | 43 |

**The last row changes the reading.** Text only, asked afresh with the same code and inputs as the first row, scored 98 instead of 119: the 119 was one lucky answer kept in the cache. Text-only answers are a lottery (issue 5); with images each input gets the same answer every time (Equinor, 3 repeats each: 85/85/85, 86/86/86, 73/73/73), but which answer depends on the wording and the pages. Single runs can't separate the two; a fair comparison needs several fresh runs per setting. `IMAGE_NOTE` is set to the best wording tried (121).

What went wrong: with the full pay document (not one page), the extra pages and instructions changed other judgements, e.g. whether Equinor's share savings plan (SSP) counts as LTI, or which policy target is the CEO's; and the AI often quoted what it saw in the image ("Salary|352 625|38 %") or stitched a header onto a figure, which the text doesn't contain, so values dropped to C. Kept from this work: quotes may now match within one table row (or a name row plus the figures row below it), which a shortened row from any source needs.

Next options, if picked up: show only the single strongest page; or use the image only to re-check figures that fail the parts-vs-total check; or Camelot's column-preserving text for the pay pages (tested: right columns, but the AI still varied on SSP).

**Camelot (tested 26 October 2026).** Its "stream" mode extracts Equinor's pay table with every column right (lattice mode finds nothing: no ruled lines), 0.2 s a page, no AI. Given to Gemini next to the text, 5 runs scored 86, 91, 86, 73, 86 of 91: better than text alone, less stable than the single-page image.

**Parked idea: re-read only flagged pages with a layout-aware reader** (discussed 26 October 2026). A layout model such as OXR (SoMark, 1.3B parameters, tables out as HTML, also reads scanned pages) would fix merged cells, but is overkill as the main converter: about 1.8 million pages for 6,000 companies, self-hosting needs Linux and a 24 GB NVIDIA GPU, and the free hosted API is not for production. Use it only on the 1–3 pay-table pages per company that a check flags: parts don't add up to the total, a cell holds two numbers (`96<br>23`), or the page has no text layer. Order of trials:
1. Render the flagged page as an image and ask Gemini (already in use) for the table: no new service, about 30 minutes to test on Equinor's pay page.
2. If that is unreliable, try OXR's free demo on the same page.
3. CPU-only alternatives for text PDFs: pdfplumber or camelot.

## 1. Report downloads behind buttons, with the file URL only in the page's data (Equinor) — fixed

*Found 24 October 2026, Nordic/UK test run (`output/nordic_uk_10.csv`). **Fixed the same day**: without any supplied URL, Equinor now matches 89 of 91 golden pay figures, at 0 Firecrawl credits.*

**The fix, in two routes:**
- **SEC filings.** The API step looks up the CIK of every company, not only US ones, and the pay step reads SEC documents first: exhibits of the latest 10-K/20-F labelled as a remuneration or compensation report (Equinor's 20-F attaches its 2025 Remuneration Report as Exhibit 15.6), and the proxy statement (DEF 14A) for US filers. Free, no bot checks. Equinor was missed before because its recent ESEF filing meant the SEC was never asked, and the API step only looked up US companies.
- **Report download pages.** Before its second search for a remuneration report, the pay step opens the site's report hub (`annual-reports`, `reports`, `downloads`, `publications` and local equivalents), and every web page read now also yields the PDF addresses kept in its page data (from the plain HTML download, no extra credit). Equinor's reports page yields all 13 report PDFs, including `equinor 2025 remuneration report.pdf`. This covers companies that are not SEC registrants.

The original analysis follows.

**Symptom.** Without help, Equinor ASA gets no executive pay for FY2025. The golden file (`data/golden_UK_Nordics_22Oct/golden_role_pay.csv`) has FY2025 pay for the CEO and 12 EVPs.

**Cause.** Three things, all of which an automatic fix has to solve:

1. **Individual pay is only in a separate remuneration report.** The FY2025 annual report (the Norwegian ESEF filing, and the English PDF) gives only the executive committee total ("USD 12.0 million", page 261), and says the remuneration report is on `www.equinor.com/reports`.
2. **That page is not in our URL lists, and its address gives no hint.** It was not among the 1,026 Equinor URLs from the report search and the map searches, and `documents.classify` does not see `/reports` as a remuneration document.
3. **The download is a button, not a link.** On `https://www.equinor.com/reports` the text "2025 Remuneration report – pdf" is there, but the entry is `<button title="2025 Remuneration report" aria-haspopup="dialog">`, which opens a download dialog. There is no `<a href>`, so the scrape's link list has no PDF. The file URL exists only in the data the page carries for its own JavaScript: `"originalFilename":"equinor-2025-remuneration-report.pdf","url":"https://cdn.sanity.io/files/h61q9gi9/global/1512fd6a4bc0558a1be62359c47ca08b6ab0ac12.pdf"`. It is on another domain (`cdn.sanity.io`, the site's content system).

This is not a page-loading problem: waiting longer (`wait_for`) returns the same page. A browser that clicks each button would find the link, but so does reading the raw HTML.

Also seen on the way: `https://www.equinor.com/investors/annual-report-2025` is only a placeholder page ("To be announced"), and a web search finds only the FY2024 report, which the pay step's year check rightly rejects.

**Workaround in place.** The input CSV takes `remuneration_report_url` and `annual_report_url`. A supplied document is read first in the pay step, skips the year check, and costs no credits when it is a PDF. With Equinor's URL supplied, 77+ of the 91 golden pay figures match.

**Automatic fix (about half a day):**

1. When no current-year remuneration report has been found, visit the site's report hub pages: paths such as `/reports`, `/downloads`, `/publications`, `/investors/reports` and local equivalents (`rapporter`, `berichte`, `julkaisut`...).
2. On those pages, also read the raw HTML (Firecrawl `rawHtml`, 1 credit, same as a normal scrape) and pull out file URLs paired with their file names or labels, e.g. `"originalFilename":"...remuneration-report.pdf","url":"..."`, then classify them by that name.
3. Accept PDFs found this way from other domains (CDNs such as `cdn.sanity.io`), as for PDFs linked from company pages.

**Other options considered:**

| Option | Cost | Notes |
|---|---|---|
| Web search fallback | About 2 credits per search | Finds files the search engine has indexed; did not find Equinor's 2025 report on 24 Oct 2026 |
| Click buttons in a browser (Firecrawl `actions`, or Playwright) | 1 credit per page, or none with Playwright; slow | Works, but fragile; reading the raw HTML is simpler for sites like this |
