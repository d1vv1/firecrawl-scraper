# Known issues

Open problems found during test runs, to pick up later. Newest first.

| # | Issue | Status | Needs |
|---|---|---|---|
| 11 | Golden file values that look like a different fiscal year | open | client answer |
| 10 | Definitions the client still has to settle (base salary, revenue line, market-cap bands) | open | client answer |
| 9 | Exchange fields weak from documents (ISIN, ticker, segment, listing date) | partly fixed | exchange segment files (Large/Mid/Small Cap, Prime Standard) |
| 8 | Sweden and Denmark registers not connected | parked | credentials; only matters for Swedish private companies |
| 7 | Register industry codes describe the holding company | open | client's chosen approach not built |
| 6 | Holding companies' own filed accounts give no group figures | open | consolidated accounts |
| 5 | Run-to-run variation in AI answers | open | caused by issue 2; cache snapshot |
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

## 9. Exchange fields weak from documents — partly fixed

*Found 23 October 2026; **partly fixed 26 October 2026** (`extractor/listing.py`, in the API step):*

- **ESMA FIRDS** (the EU regulator's list of every share traded on an EU venue), searched by LEI: ISIN, the exchange where the company itself asked to be listed, and listing status. All graded A.
- **ISO 10383 MIC list:** the exchange's name, which exchange a segment code belongs to, and regulated market vs MTF. An MTF growth market (First North, Euronext Growth) is written as the segment.
- **OpenFIGI:** the ticker, in Bloomberg spelling ("VOLVB"); a document's own spelling ("VOLV B") is kept when it agrees. UK and Swiss companies (not in FIRDS) get their ISIN, exchange and ticker here.
- **Listing date:** FIRDS's first trading date only for listings since 2000 and not on a known system date, graded C, so a document's date wins.

Nordic/UK test: ISIN 10 of 10 (was 5), exchange fields 51 of 60 (was 47); Novo Nordisk's ticker went from its New York ADR (NVO) to NOVOB. Aker Carbon Capture has no FIRDS records.

**Still open:** the segment within a regulated market (Nasdaq Nordic Large/Mid/Small Cap, Deutsche Börse Prime/General Standard, SIX segments). It needs the exchanges' own files (Deutsche Börse xlsx, SIX csv, Nasdaq Nordic lists); until then it comes from documents. Old listing dates stay a document field.

## 8. Sweden and Denmark registers not connected

*Parked 25 October 2026.* Bolagsverket (SE) and CVR (DK) would give industry codes, and for private companies filed accounts (SE) and owners (DK). For listed companies they add little: identity comes from GLEIF, owners from the annual report, and Danish filed accounts already come from virk.dk without a login. Access: Bolagsverket by a free request form that sends keys by SMS (a Swedish phone number may be needed); CVR by email to cvrselvbetjening@erst.dk. **Revisit if the company list has many Swedish private companies.** Code to port: the colleague's `extras/collect_company_data.py`. Variables: `BOLAG_CLIENT_ID`, `BOLAG_CLIENT_SECRET`, `CVR_USER`, `CVR_PASSWORD`.

## 7. Register industry codes describe the holding company

*Found 25 October 2026.* Companies House gives Shell plc and AO World plc the code SIC 70100 ("activities of head offices"): the register codes the listed parent, not the business. The client's validation noted the same and decided to **derive the sector from the business description (found for 97%) with the Allshares taxonomy**. That classification is not built: it needs the taxonomy from the client, then an AI classification of `sub_sector`.

## 6. Holding companies' own filed accounts give no group figures

*Found 25 October 2026.* For a UK holding company, Companies House holds the parent's own accounts: TWMA Group Limited's tagged accounts have only investments, no revenue, and 0 employees (the staff are in its subsidiaries). The group figures are in consolidated accounts filed by the group's top company, or on its website. Fix option: when the latest accounts are parent-only (no revenue tag), look for the consolidated accounts of the same company or its parent.

## 5. Run-to-run variation in AI answers

*Found 24 October 2026; **tested 26 October 2026**.* The temperature was already 0 (`llm._parse`). Asking Gemini 2.5 Flash the same Equinor pay question three times still changed 25 of 136 values; a fixed seed (36 changed) and the thinking levels `minimal` (18) and `low` (25) did not fix it (`high` timed out). **Every value that changed was in the merged table columns of issue 2** (benefits, pension allowance, other fees); clean columns came back identical each time. So the fix is issue 2, not a model setting.

Meanwhile answers are cached per prompt and chunks, so a run without prompt changes is stable. A changed gap list or prompt asks again and can move such values: when the exchange lists filled Equinor's ISIN, the document step asked for a different set of facts and Equinor's `staff_by_country` was not found that time. Mitigations: keep a reviewed snapshot of the cache before prompt changes; flag a role whose parts don't add up to its total (already noted by the R11 check).

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
