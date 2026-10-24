# Known issues

Open problems found during test runs, to pick up later. Newest first.

| # | Issue | Status | Needs |
|---|---|---|---|
| 11 | Golden file values that look like a different fiscal year | open | client answer |
| 10 | Definitions the client still has to settle (base salary, revenue line, market-cap bands) | open | client answer |
| 9 | Exchange fields weak from documents (ISIN, ticker, segment, listing date) | open | build FIRDS + exchange files |
| 8 | Sweden and Denmark registers not connected | parked | credentials; only matters for Swedish private companies |
| 7 | Register industry codes describe the holding company | open | client's chosen approach not built |
| 6 | Holding companies' own filed accounts give no group figures | open | consolidated accounts |
| 5 | Run-to-run variation in AI answers | open | small change |
| 4 | Report finder can still pick a subsidiary's or a placeholder report | partly fixed | more guards |
| 3 | SEC name lookup misses some registrants | fixed | — |
| 2 | PDF tables converted with merged columns | open | better table extraction |
| 1 | Report downloads behind buttons | fixed | — |

## 11. Golden file values that look like a different fiscal year

*Found 24 October 2026, Nordic/UK test.* Some golden values don't match the report year we read, though our values match the reports exactly:

- **Nokia:** golden revenue €19,220m and total assets €39,149m are labelled FY2025; our FY2025 tagged figures are €19,889m and €37,597m. €19,220m appears to be Nokia's FY2024 net sales.
- **Bang & Olufsen:** golden pay is labelled 2025; we read the FY2025/26 report (year to May 2026), and the golden values look like FY2024/25.

**Needs:** the client to confirm which fiscal year the golden files are meant to hold. Until then these count as differences in `output/golden_uk_nordics_check.md`.

## 10. Definitions the client still has to settle

*Found 23–24 October 2026.* The code follows a default for each; each is a one-line switch once decided.

| Question | Our default | Seen in |
|---|---|---|
| Base salary: fixed salary only, or total fixed pay (base + benefits)? | fixed salary only (the client's own decision) | BioArctic: golden CEO base 4,967k = our base 4,846k + benefits 122k |
| Revenue when a filing tags both "revenue" and "revenue and operating income" | IFRS revenue, the other in `note` (`datapoints.REVENUE_RULE`) | CTT: 1,129m vs 1,292m |
| Market-cap band thresholds | €1bn / €150m, a placeholder (`datapoints.MARKET_CAP_BANDS_EUR`); non-EUR companies need a year-end EUR rate | all |

The client's field definitions are said to be in a HANDOVER.md that we have not received.

## 9. Exchange fields weak from documents

*Found 23 October 2026, validation run.* ISIN, ticker, exchange segment and listing date are each found for only 25–58% of companies from documents, below the protocol's 60% line. The planned sources are not built yet: ESMA FIRDS (ISIN and trading venue; **never** its admission date, which is a placeholder for old listings) and the free exchange files (Deutsche Börse, SIX, Euronext) for segments. See `docs/protocol_schema_mapping.md`, "API step".

## 8. Sweden and Denmark registers not connected

*Parked 25 October 2026.* Bolagsverket (SE) and CVR (DK) would give industry codes, and for private companies filed accounts (SE) and owners (DK). For listed companies they add little: identity comes from GLEIF, owners from the annual report, and Danish filed accounts already come from virk.dk without a login. Access: Bolagsverket by a free request form that sends keys by SMS (a Swedish phone number may be needed); CVR by email to cvrselvbetjening@erst.dk. **Revisit if the company list has many Swedish private companies.** Code to port: the colleague's `extras/collect_company_data.py`. Variables: `BOLAG_CLIENT_ID`, `BOLAG_CLIENT_SECRET`, `CVR_USER`, `CVR_PASSWORD`.

## 7. Register industry codes describe the holding company

*Found 25 October 2026.* Companies House gives Shell plc and AO World plc the code SIC 70100 ("activities of head offices"): the register codes the listed parent, not the business. The client's validation noted the same and decided to **derive the sector from the business description (found for 97%) with the Allshares taxonomy**. That classification is not built: it needs the taxonomy from the client, then an AI classification of `sub_sector`.

## 6. Holding companies' own filed accounts give no group figures

*Found 25 October 2026.* For a UK holding company, Companies House holds the parent's own accounts: TWMA Group Limited's tagged accounts have only investments, no revenue, and 0 employees (the staff are in its subsidiaries). The group figures are in consolidated accounts filed by the group's top company, or on its website. Fix option: when the latest accounts are parent-only (no revenue tag), look for the consolidated accounts of the same company or its parent.

## 5. Run-to-run variation in AI answers

*Found 24 October 2026.* Re-asking the AI the same question can move a few values (e.g. a merged table cell read as 156 one time and 53 the next, see issue 2), and a changed prompt re-asks every company. Answers are cached per prompt, so a run without prompt changes is stable. Fix options: set the model's temperature to 0 in `llm.py`; keep a reviewed snapshot of the cache before prompt changes.

## 4. Report finder can still pick a subsidiary's or a placeholder report

*Found 23–24 October 2026.* Fixed so far: Siemens (a Dutch financing subsidiary's report; now "plc"/legal-form and unexplained-word guards), Volvo (Volvo Treasury AB's report; now group-function words such as "treasury" rank lower, and report PDFs in event folders are kept), Rosenbauer (an older English report beat a current German filing), Jumbo (a year written as a date, `31122025`). An identity check grades values C when the report's own company name or country differs. **Still open:** a dated placeholder page can outrank a report-downloads page (Equinor's "annual-report-2025" vs "annual-reports"); subsidiaries with unremarkable file names are not caught before extraction. Fix options: prefer report-hub pages when choosing which page to scan; check the report's cover page before extracting from it.

## 3. SEC name lookup misses some registrants (Novo Nordisk) — fixed

*Found 24 October 2026; **fixed 25 October 2026**: name matching now joins a legal form written as separate letters ("A S" = "A/S", "S A", "N V", "S P A"), and the SEC lookup also tries the LEI's legal name. Novo Nordisk is found (CIK 353278). A company without an LEI can also be identified in GLEIF by its ISIN or register number (optional `isin` input column).*

*Original note:* `edgar.find_cik` matches on the company name only, and Novo Nordisk A/S (an SEC registrant with ADRs, ticker NVO) is not matched ("no SEC registrant with this name"), presumably because the SEC spells the name differently. Fix options: look the CIK up by ticker or ISIN as well; or accept the LEI's legal name and former names as alternatives; or list known name variants ("A/S" = "A S").

## 2. PDF tables converted with merged columns (Equinor pay table)

*Found 24 October 2026.*

**Symptom.** Equinor's executive pay matches the golden file on one run (89 of 91 figures) and not on another. Benefits once matched 1 of 13.

**Cause.** The PDF-to-text conversion (pymupdf4llm) merges two columns of the pay table into one cell and cuts header words at the wrong places:

```
| ... | Fees / Fixed salary addition | One-y / Other fees / Fringe benefits | ear variable / AVP | ... | Extraordinary items / Pensi | on expense | ...
| Anders Opedal | 1,242 | 224 | 96<br>23 | 292 | 306 | 0 | 0 | 30 | 2,213 |
```

"Other fees" (96) and "Fringe benefits" (23) share one cell, so every label after it sits partly over the wrong number. The AI usually still reads it right, but not always; telling it to split such cells made it shift every later column by one (LTI 0 of 13), so that instruction was reverted.

**Fix options.** Keep column boundaries in the conversion (pymupdf4llm table settings, or a table extractor such as pdfplumber/camelot for pages with pay tables); or read pay tables from the PDF layout (cell positions) rather than from converted text; or a consistency check that flags a role whose parts don't add up to its stated total (the R11 check already notes this).

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
