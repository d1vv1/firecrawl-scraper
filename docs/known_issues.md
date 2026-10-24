# Known issues

Open problems found during test runs, to pick up later. Newest first.

## 3. SEC name lookup misses some registrants (Novo Nordisk)

*Found 24 October 2026.* `edgar.find_cik` matches on the company name only, and Novo Nordisk A/S (an SEC registrant with ADRs, ticker NVO) is not matched ("no SEC registrant with this name"), presumably because the SEC spells the name differently. Fix options: look the CIK up by ticker or ISIN as well; or accept the LEI's legal name and former names as alternatives; or list known name variants ("A/S" = "A S").

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

**Symptom.** Without help, Equinor ASA gets no executive pay for FY2025. The golden file (`golden_UK_Nordics_22Oct/golden_role_pay.csv`) has FY2025 pay for the CEO and 12 EVPs.

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
