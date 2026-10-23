# Annual-report extractor (website fallback)

Given a company's legal name, this tool finds the company's latest annual report on its
own website and extracts four fields into one JSON file:

1. **Revenue**
2. **Total assets**
3. **Revenue model**
4. **Business structure**

This is the fallback for when registries/APIs have no financial data. Version 1 targets
large listed companies with an English PDF annual report (tested on Unilever PLC).

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # (cp on macOS/Linux) then fill in the four values
```

`.env`:

| Variable | What it is |
|---|---|
| `FIRECRAWL_API_KEY` | Firecrawl key (search + map only; free tier is fine) |
| `FOUNDRY_ENDPOINT` | Microsoft Foundry OpenAI-compatible endpoint, ending in `/openai/v1/` |
| `FOUNDRY_API_KEY` | Foundry API key |
| `LLM_PROVIDER` | `foundry` (default) or `vertex` (Google Vertex AI / Gemini) |
| `VERTEX_PROJECT` | Google Cloud project ID (Vertex only; sign in with `gcloud auth application-default login`) |
| `VERTEX_LOCATION` | Vertex region, default `global` |
| `VERTEX_MODEL` | Vertex model, default `google/gemini-2.5-flash` |
| `FOUNDRY_DEPLOYMENT` | The **deployment** name, passed as `model`. It must support structured outputs (`json_schema`), e.g. gpt-4o, gpt-4.1, or gpt-5 family |
| `WIKIMEDIA_CONTACT` | Optional. Your email or a URL, sent to Wikidata in the User-Agent as Wikimedia's API policy asks. Without it Wikidata rate-limits harder in batch runs |

## CLI

```bash
python -m extractor "Unilever PLC"
python -m extractor "Unilever PLC" --lei 549300MKFYEKVRWML317               # skip the GLEIF name lookup
python -m extractor "Unilever PLC" --website https://www.unilever.com       # skip step 2
python -m extractor "Unilever PLC" --report-url https://.../report.pdf      # skip steps 2 and 3
python -m extractor "Unilever PLC" --no-cache                                # re-discover and re-download
python -m extractor "Unilever PLC" -v                                        # debug logging on the console
```

The run writes:

- `output/<slug>.json`: the result (e.g. `output/unilever-plc.json`)
- `output/<slug>.log`: full debug log. **Every candidate URL** from steps 2 and 3, and
  why it was kept or dropped, is in here.
- `cache/`: the PDF, its markdown (with `<!-- page N -->` markers),
  `<slug>_lei.json` (the GLEIF match and every name candidate it considered) and
  `<slug>_discovery.json` (website + report URL + candidate log).

A second run reuses `cache/`, so it makes no downloads, no GLEIF/Wikidata calls and no
Firecrawl calls. It does call the LLM again.

## Batch runs

Input: a CSV with a header row, saved as UTF-8 ("CSV UTF-8" in Excel). Comma- and
semicolon-separated files both work. See `companies.example.csv`.

```
company_id;company_name;country_code
SE001;Volvo AB;SE
DK001;Novo Nordisk A/S;DK
```

```bash
python -m extractor.batch companies.csv --dry-run                # free: GLEIF + Wikidata only, estimates credits
python -m extractor.batch companies.csv --limit 10 --max-credits 50
python -m extractor.batch companies.csv                          # all; re-run the same command to resume
python -m extractor.batch companies.csv --retry-failed           # also retry companies that errored
python -m extractor.batch companies.csv --only SE001,DK001       # just these ids
python -m extractor.batch companies.csv --refresh                # redo processed companies under the current rules
```

- **One file per company:** `output/<company_id>.json` (same format as the CLI),
  `output/<company_id>.log`, and `output/<company_id>.error.json` if it failed.
- **`output/fill_rate.md`:** fill rate per data point and country segment ("companies with
  a value / companies processed (rate)"), with *verified* rows counting only status `ok`.
  It's written at the end of every batch run; regenerate any time with
  `python -m extractor.report companies.csv`.
- **`output/summary.csv`:** one row per company with status, LEI, website, report URL,
  fiscal year, revenue, total assets, failed checks, credits and error. It's rewritten after
  every company, so it's current even if the run is interrupted. Excel opens it with
  å/ä/ø intact.
- **Resumable:** companies with a result are skipped, and so are earlier failures unless
  `--retry-failed` is given. A rerun never pays twice by accident. `--force` redoes
  everything, including downloads.
- **`--max-credits N`:** stops before the next company could push Firecrawl spend over N,
  assuming the per-company cap as the worst case.
- **`--workers N`** (default 1): companies processed at the same time, each in its own
  process. 3 is a good choice on a normal laptop: PDF conversion uses one CPU core per
  company, and the AI quota (50,000 tokens/min) and Firecrawl's free plan both tolerate it
  (their "too many requests" replies are retried). GLEIF and Wikidata requests are spaced
  out N times further in each process, so together they stay within those services'
  limits. The credit cap holds: a company only starts if the credits spent plus the worst
  case of every company still running stay within `--max-credits`.
- **`--max-credits-per-company N`** (default 6): no company can spend more. Step 3 stops
  searching and uses the best report found so far.
- **`--refresh`:** re-processes companies that already have a result or error, under the
  current rules. A cached report that still passes today's rules is kept, so the redo costs
  0 Firecrawl credits and only the LLM runs again. A stale, non-PDF or excluded one is
  dropped and found again. Scanned-PDF failures are skipped.
- **Network outages pause the batch** (e.g. the laptop slept and dropped Wi-Fi). A company
  that fails on a lost connection isn't marked failed. The batch checks every 30 s until
  the internet is back, then retries the same company. After 60 minutes offline it stops
  cleanly, so re-run the same command to continue. Companies that failed on a network error
  in an earlier run are retried automatically, without `--retry-failed`.
- **Fatal errors stop the batch:** Firecrawl out of credits or a bad key, missing `.env`
  values, or an LLM deployment without structured outputs. These would fail every
  company, so the batch stops at once.
- **`--dry-run`** writes `output/dry_run.csv` (LEI, GLEIF name, match type, Wikidata website
  per company) and prints the estimated credits. Its LEI lookups are cached and reused by
  the real run.

### Monday build test

```bash
python -m extractor.batch companies.csv --sample 30 --max-credits 350
python -m extractor.monday companies.csv          # rebuild the table any time
```

`--sample 30` picks 30 companies per parse-route segment (nordic_listed, europe_uk_listed,
us_listed, nordic_uk_unlisted) from `golden_values.csv`. Companies with golden revenue,
total assets or employee figures come first. The seed is fixed (`--seed`), so the same
sample can be re-run. The sample is saved to `output/sample_companies.csv`, and at the end
of the run `output/monday_table.csv` is written in the PO's format (one row per fact and
segment):
- **Revenue and total assets** are compared with the golden value for the same fiscal year
  and currency, within 1% or 1 million (golden values are rounded to millions).
- **Mismatches, other-year golden values and currency differences** are listed in `notes`
  for re-checking, not counted as wrong. The golden set sometimes labels last year's
  figures with this year (Nokia), or carries a different currency.
- **Revenue model and business structure** have no golden values. "Confirmed" there means
  the supporting quote was found word for word in the report.
- **Recommendation:** BUILD at ≥80% coverage and ≥95% accuracy on at least 10 checked values,
  BUY when clearly below, REVIEW otherwise. Facts not built yet show NOT_TESTED.

`country_code` (ISO 3166 alpha-2) is used to search GLEIF within that country, as the
country for website scoring, and for the native report search term when no LEI is found.

### All data points, with the exact source of each value

```bash
python -m extractor.datapoints golden_test_sample_5_per_segment_country_all.csv --workers 3
```

This collects the fields of the source-validation protocol
(`Source_validation_listed_22Oct/PROTOCOL.md`; mapping in `docs/protocol_schema_mapping.md`)
for the companies in the CSV, and writes **`output/datapoints.csv`**:

`company_id, company_name, segment, country, lei, grain, role_row, data_point, value, unit,
period_end, source, endpoint, method, retrieved_at, confidence, note`

- **Company grain** (`grain` = `company`): 41 data points per company (protocol C01-C23),
  one row each, including the ones not found.
- **Role grain** (`grain` = `role`): executive pay (protocol R01-R11), one set of 14 rows per
  disclosed executive role, `role_row` holding the role as stated ("CEO", "Other members of
  group management"; the name is added only when two roles share a title). Non-executive
  board members get one `role_disclosure` row. Read from the remuneration report, else the
  annual report's remuneration section; target and maximum percentages missing there come
  from the remuneration policy. Pay amounts are in full units like all money; the printed
  figure, bundled components and the LTI basis are in `note`, and a stated total that
  differs from the sum of its parts by more than 2% is flagged there.

Per company, cheapest and most exact first:
1. the annual-report pipeline above (run first if the company has no result yet);
2. one more AI pass over the same report for identity (legal name, register number,
   country, city, website, former names, parent), EBITDA, fiscal year end and accounting
   basis, employees, share data and year-end price, largest holders and owners, listing,
   pay terms, and revenue and staff by segment and country (`prompts/datapoints_system.md`);
3. **executive pay**: the remuneration report (found like the fallback documents below)
   and, if needed, the remuneration policy, read with `prompts/remuneration_system.md`;
4. **document fallback** (`extractor/documents.py`): the data points still empty are
   looked for in the company's other documents: remuneration report, AGM notice,
   corporate-governance and sustainability reports, "The share" and shareholder pages,
   legal notice (*Impressum*), year-end report, listing notice, history and about pages.
   Each data point has its document types in order of likely yield; URL keywords cover
   about 10 languages. Documents are found cheapest first: the site URLs the report
   search already listed (free), one map of the site and a map search per document type
   (1 credit each, cached), then links on the pages read. PDFs are downloaded for free;
   web pages cost 1 credit. Up to 3 rounds of 3 documents; each round asks the AI only
   for the remaining gaps, with only the relevant parts of each document, and stops when
   the gaps are filled. Only the company's own site and the PDFs it links to are used;
   blocked domains, news and blog pages, and documents more than 2 years older than the
   report are skipped. Default cap: 10 credits per company (`--doc-credits`,
   `--no-docs`).

The official APIs (GLEIF, SEC EDGAR, the registers) are not called here: that data is
collected upstream, so `lei` and `sector_code` are left empty with the note "not collected
here". The CIK still comes from an SEC filing when the report is one.

When several sources give a value, the most exact one wins (A before B before C, then
XBRL, then report, then web). A different value from another source is mentioned in
`note`. Values from fallback documents carry the document's year (`document dated 2025`).

**Where each value came from:**
- `endpoint` is the exact URL: the XBRL filing, the **PDF with
  `#page=N`** (opens at that page), or the web page / filed HTML report with a
  `#:~:text=` fragment that Chrome, Edge and Safari scroll to.
- `note` repeats the page and quote (`PDF page 45: "Net sales|3|2,326.2|1,827.3"`), the
  XBRL tag, or why there is no value (`not found in: …`, `not applicable: the company is
  not listed`, `not collected: market data … is bought`).
- `method`: `API` (register field), `XBRL` (tagged figure), `PARSE` (read from a filed
  document), `SCRAPE` (read from a web page), `BUY` (market data: not collected).
- `confidence`: `A` exact (register field or XBRL tag);
  `B` read by the AI and its quote found in the source; `C` read by the AI but the quote
  wasn't found word for word (check it).
- Money is in full units with the ISO currency in `unit` (`2326200000`, `SEK`);
  employees have unit `employees`.
- The page of a PDF value is the page its quote is found on, looked up in the PDF's text.
  It is the PDF's page number (what `#page=` opens), not the number printed on the page.

Re-runs skip companies already done (`output/datapoints/<id>.json`; `--redo` to redo).
When the input is the golden sample, `output/golden_test_filled.csv` is the same file with
`build_value` filled in, in the golden unit (millions), for the reviewers.

## ESEF route (tried first)

EU, EEA and UK companies listed on a regulated market file their annual report in ESEF
format: the full report as `.xhtml`, with the financial statements tagged as data.
[filings.xbrl.org](https://filings.xbrl.org) indexes these filings by LEI, free and
without a key ([extractor/esef.py](extractor/esef.py)).

For a company with an LEI, the pipeline first looks for its newest **annual** filing
(quarterly and half-year filings are skipped: a filing counts as annual only if it has
12-month figures).
- **Recent filing** (fiscal year = last year or newer):
  - **Revenue, total assets, total equity and liabilities** are read from the XBRL tags
    (`ifrs-full:Revenue` or `RevenueFromContractsWithCustomers` / `RevenueFromSaleOfGoods`,
    `ifrs-full:Assets`, `ifrs-full:EquityAndLiabilities`). These are exact: no AI, no units
    to misread. When all three are tagged, the financials AI call is skipped.
  - **The report text** comes from the filing's `.xhtml`
    ([extractor/xhtml_text.py](extractor/xhtml_text.py)), split into ~450-word sections.
    No website search, no Firecrawl credits, no PDF conversion: 10–30 seconds per company.
  - **A filing in another language** (Nokia files in Finnish, AAK in Swedish) still gives
    the tagged figures, but the descriptive facts are read from the English report on the
    website. If there is none, the filing's own text is used.
  - **The company-name check** passes on the LEI, since the filing is filed under the
    company's own LEI (the report may use a trade name, e.g. "Nokian Tyres").
- **No filing, or only an old one** (Germany and Ireland aren't in the index; growth
  markets such as First North don't file ESEF; the index lags publication by weeks or
  months): the website route below. An older filing (e.g. FY2024) is kept as a fallback:
  it's used if the website route fails, or if the website only has an even older report.

On the 3,675-company list (16 Oct 2026, LEIs from the CSV only), recent ESEF filings
covered about 490 companies: Nordic listed 173, EU/UK listed 299, others 17. Another 337
Nordic companies only had FY2024 indexed.

Results say which route was used: `data_source` = `esef`, `edgar`, `esef tags + website text`,
`edgar tags + website text` or `website`, and each figure has `method` = `xbrl_tag` or `llm`.

## SEC EDGAR route (tried next)

If there is no recent ESEF filing, the company's name is looked up in the SEC's list of
registrants (matched like the LEI lookup, so "Eli Lilly and Company" = "ELI LILLY & Co").
For a registrant, its latest **10-K** (or **20-F** / **40-F** for foreign issuers) is used
like an ESEF filing ([extractor/edgar.py](extractor/edgar.py)):
- **Tagged figures:** revenue (`us-gaap:Revenues`, `RevenueFromContractWithCustomer…`, or the
  IFRS equivalents), `Assets` and `LiabilitiesAndStockholdersEquity`, taken from that
  filing's own XBRL tags via the SEC company-facts API.
- **Report text:** the filing's main HTML document.

Free, no scraping, no Firecrawl credits. It also covers companies listed outside the US that
file with the SEC (Chubb, NXP, Smurfit WestRock, Johnson Controls), whose websites often
have no annual report PDF. **Requires `SEC_CONTACT` in `.env`**: the SEC refuses requests
without a contact in the User-Agent. Without it, the SEC route is skipped.

## Company registry route (Norway, Denmark, UK; tried after SEC)

Private companies rarely publish annual reports on their websites, but they must file
their accounts with the national registry ([extractor/registries.py](extractor/registries.py)).
Both registries below are open, free and need no key:

| Country | Registry | Figures | Text for the descriptive facts |
|---|---|---|---|
| Norway | Brønnøysund (Regnskapsregisteret) | Filed accounts as data: `sumDriftsinntekter` (revenue), `sumEiendeler` (total assets), `sumEgenkapitalGjeld`. Group accounts (KONSERN) preferred over company-only (SELSKAP). | The company profile (legal form, industry, activity, employees). |
| Denmark | Danish Business Authority | The filed XBRL: `fsa:Revenue` / `ifrs-full:Revenue`, `Assets`, `LiabilitiesAndEquity`. Group figures (`ConsolidatedMember`) preferred. | The filed annual report (inline XBRL or PDF). |
| UK | Companies House (needs a free **live** REST key: `COMPANIES_HOUSE_API_KEY`) | The latest filed accounts. iXBRL: `TurnoverRevenue`; UK balance sheets have no total-assets line, so total assets = `FixedAssets` + `CurrentAssets`. PDF-only accounts: the AI reads the figures. | The filed accounts (iXBRL or PDF). |

- **Finding the company:** by the registration number in its LEI record. Without an LEI, Norway
  falls back to an exact legal-name match (one match only); Denmark needs the LEI.
- **Parent-only accounts:** when only company accounts of a parent company are filed, the
  figures are marked `scope: parent_only` and the result needs review.
- **Small Danish companies** may file gross profit instead of revenue (allowed for small
  companies). Then revenue is left to the AI reading the report text, and may be missing.
- Sweden (Bolagsverket) needs an organisation account and isn't built yet.
- The UK route is skipped while `COMPANIES_HOUSE_API_KEY` is empty. A key from the Companies
  House *test* environment is refused by the live service (HTTP 401).

## Pipeline

A fixed sequence of plain functions ([extractor/pipeline.py](extractor/pipeline.py)):

| Step | Module | What it does | Firecrawl cost |
|---|---|---|---|
| 1 | `config.py` | Keep the legal name; build a clean name (lowercase, no plc/ag/nv/…) and a slug | – |
| 1b | `lei.py` | Find the LEI in GLEIF by legal name. Only an exact (normalized) name match counts; several equal matches = ambiguous = no LEI | – (free API) |
| 2 | `wikidata.py`, `website.py` | **LEI found:** Wikidata LEI → official website (free). If Wikidata has nothing, Firecrawl search, scored with the LEI's country. **No LEI:** Firecrawl search on the legal name. Search drops blocklisted domains (`BLOCKED_DOMAINS`) and scores domain/title vs. clean name | 0 (Wikidata hit) / 2 (search) |
| 3 | `report_finder.py` | Firecrawl map with search "annual report" → native term for the LEI country (e.g. "årsredovisning") → "integrated report" → "investors"; multilingual keep/exclude URL filters; PDF first, newest year, English version, keywords in file name. Fallback: scrape an IR page for PDF links | 1 per map (+1 scrape) |
| 4 | `scraper.py` | Download the PDF directly (not via Firecrawl) and convert it locally with `pymupdf4llm`; HTML reports go through Firecrawl scrape | 0 (PDF) / 1 (HTML) |
| 5 | `sections.py` | Chunk (headings, else ~1,500-word windows), skip table-of-contents chunks, score against FINANCIALS / QUALITATIVE keywords, boost real statement tables, keep the best up to ~6,000 words per group | – |
| 6 | `extract.py`, `llm.py` | Two structured-output LLM calls; unit conversion in code | – |
| 7 | `validate.py` | Quote, value-in-quote, scope, balance and sanity checks → status | – |

The estimated Firecrawl credits for the run are printed and stored in the output. A
first run costs about 1–2 credits when Wikidata knows the website (Unilever: 1) and 3–5
when it falls back to search.

Step 2 flow:

```
legal name ──GLEIF──► LEI found? ──yes──► Wikidata website? ──yes──► website (source "wikidata")
                          │                      │
                          no                     no
                          ▼                      ▼
              Firecrawl search on name    Firecrawl search on name + LEI country bonus
              (source "search")           (source "search+lei")
```

## Reading the output

```jsonc
{
  "input_name": "Unilever PLC",
  "status": "ok",                       // ok | needs_review | not_found
  "lei": "549300MKFYEKVRWML317",        // null if no unambiguous GLEIF match
  "lei_record": { "legal_name": "UNILEVER PLC", "country": "GB", "legal_form_id": "B6ES", ... },
  "lei_lookup": "exact name match",     // or why no LEI was used
  "website": "https://unilever.com",
  "website_source": "wikidata",         // wikidata | search+lei | search | override
  "report_url": "https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf",
  "fiscal_year": "2025",
  "revenue": {
    "value": 50503.0,                   // exactly as printed
    "unit": "millions",                 // from the table header
    "currency": "EUR",
    "value_full": 50503000000.0,        // value × unit, computed in code
    "label_in_report": "Turnover",
    "scope": "consolidated",
    "quote": "...",                     // exact text the figure came from
    "chunk_id": 412, "source_pages": [131]   // where to look in the PDF
  },
  "total_assets": { ... same shape ... },
  "revenue_model":      { "categories": [...], "description": "...", "quote": "...", "source_pages": [...] },
  "business_structure": { "legal_form": "...", "is_listed": true, "ultimate_parent": null,
                          "segments": [...], "description": "...", "quote": "...", "source_pages": [...] },
  "cross_check": { "total_equity_and_liabilities": { ... } },   // only used for the balance check
  "checks": [ { "name": "quote", "target": "revenue", "result": "pass", "detail": "exact match in chunk 412" }, ... ],
  "warnings": [],
  "extracted_at": "...", "model": "<deployment>", "firecrawl_credits_used": 4,
  "debug": { "cache_used": {...}, "chunks_sent": {...} }
}
```

**Status**

- `ok`: every check on the **financial figures and the company** passed or was skipped.
- `needs_review`: at least one of those failed. Look at `checks[].detail`.
- Checks on the descriptive fields (`revenue_model`, `business_structure` quotes) don't
  affect the status. A failure there is listed in `warnings`.
- `not_found`: neither revenue nor total assets was found.

**Checks** (each is `pass`, `fail` or `skipped`)

| Check | Meaning of a fail |
|---|---|
| `quote` | The quote isn't in the chunk it cites, so the value is a **probable hallucination**. `exact` = normalized substring; `loose` = same words in order with at most 3 extra tokens between them (e.g. a table's Notes column) |
| `value_in_quote` | The extracted number isn't in its own quote |
| `scope` | Figure isn't `consolidated` (parent-only or unclear). Also listed in `warnings` |
| `balance` | Total assets and total equity + liabilities differ by more than 0.5% |
| `sanity` | Value ≤ 0, currency not ISO 4217, unit missing, or fiscal year older than 3 years |
| `entity` / `company_name` | Neither the listed name nor the GLEIF legal name appears in the report's first 20 pages: possibly another company's report |
| `entity` / `currency` | The reporting currency isn't the home currency of the listing/LEI country, EUR or USD (e.g. INR for ABB Ltd means ABB India's report was used) |

To verify a number by hand, open the PDF at `source_pages`.

## Tests

```bash
pytest              # unit tests + fixture tests (no network, LLM mocked)
pytest -m live      # end-to-end on Unilever PLC (uses Firecrawl credits and the LLM)
```

`tests/fixtures/unilever-ara-2025.md` is the real Unilever Annual Report and Accounts 2025
converted by step 4. Steps 5–7 are tested against it.

## Assumptions

Decisions made where the spec was open:

- **Blocked downloads fall back to browser TLS impersonation.** unilever.com (Akamai) returns
  403 "Access Denied" to httpx and curl even with a browser User-Agent; it fingerprints the
  TLS handshake. The downloader tries `httpx` first as specified, then retries with
  `curl_cffi` (Chrome impersonation) on 401/403/429 or a non-PDF body. This adds one
  dependency beyond the listed ones.
- **Structured outputs via `client.chat.completions.parse`.** In `openai` 3.x this is GA (the
  `beta.` alias still exists). No free-text fallback: if the deployment rejects
  `json_schema`, the run stops with `StructuredOutputsUnsupportedError`.
- **Firecrawl SDK:** `firecrawl-py` 4.x, `from firecrawl import Firecrawl` with `.search()`,
  `.map(url, search=...)` and `.scrape()`. Map is called with `include_subdomains=True`
  because reports often sit on `investors.<domain>` or a CDN subdomain.
- **PDF converter:** `pymupdf4llm` uses its layout engine (via `pymupdf-layout`), which
  produces clean markdown tables. Converting the 285-page Unilever report takes about
  6 minutes, but only once because the result is cached. OCR is turned off.
- **Steps 2–3 are cached too** (`cache/<slug>_discovery.json`). Without that, "a second run
  makes no Firecrawl calls" isn't possible. `--no-cache` ignores all caches.
- **`--report-url` without `--website`:** the website is set to the report URL's origin.
- **Report ranking:** the order is: any PDF over any HTML page (HTML only when no PDF
  exists), then the newest year, then the English version, then keywords in the **file
  name**, then keywords elsewhere in the URL, then the shortest URL. Results: the 2025 PDF
  beats a 2026 press release (unilever.com); `annual-report-and-accounts-2025.pdf` beats
  `annual-report-on-form-20-f-2025.pdf`; Novo Nordisk's annual report beats the tax report in
  the same `annual_report/` folder; 1&1's `GB_…_ENG.pdf` beats `GB_…_DEU.pdf`. A newer
  non-English report still beats an older English one; that is logged as a warning.
- **Year in URL:** taken from the file name if it has one, because folders are often the
  publication year (`/2026/…-annual-report-2025.pdf`). `20\d{2}` must stand alone (not inside
  a hash such as `205966bf`) and not be in the future. Without this, a hash in a URL turned
  Unilever's 1956 report into "2059".
- **European languages:** `report_finder.py` has keep and exclude keywords for English,
  German, Swedish, Norwegian, Danish, Finnish, Icelandic, Dutch, French, Spanish and Italian
  (`KEEP_KEYWORDS`, `TYPE_EXCLUDES`, `TOPIC_EXCLUDES`, all easy to extend). URLs and
  keywords are folded the same way (å/ä→a, ö/ø→o, æ→a, ü→u, and aa/ae/oe/ue collapsed), so
  `årsrapport`, `arsrapport` and `aarsrapport` all match. The German `GB` abbreviation
  (Geschäftsbericht) counts only in the file name, right next to a year, because `/gb/` is
  also a UK locale folder. German `Jahresabschluss`/`Einzelabschluss` (parent-only accounts),
  Finnish `tilinpäätöstiedote` and Swedish `bokslutskommuniké` (year-end releases) are excluded.
- **Combined reports are kept.** Topic words (sustainability, governance, remuneration and
  their translations) don't exclude a URL when joined to the report by
  incl/and/och/og/ja/und/with/med. This keeps Atlas Copco's "annual report incl.
  sustainability report and corporate governance report" and Swedish
  "års- och hållbarhetsredovisning".
- **Native map search:** with an LEI, step 3's second map search uses the country's word
  ("årsredovisning" for SE, "vuosikertomus" for FI, …). It only runs if "annual report"
  found no PDF, so it costs nothing extra when English works.
- **Extra exclusions:** press releases, news, capital-markets-day, tax, impact, green-bond
  and modern-slavery documents, "bulletin"/"release" files, and parent-company statements.
- **Exclusion tokens:** short tokens (`q1`, `esg`, `h1`) must stand alone in the URL, so `faq1`
  doesn't exclude a URL. Longer words only need to start a word, so `kvartalsrapport` is
  excluded but `headquarters` doesn't trip "quarter".
- **Nordic-language reports are supported** (a change from the spec's "non-English out of
  scope", because many small Nordic caps publish only in their own language). Step 5 has
  Swedish, Norwegian, Danish, Finnish and Icelandic statement and section keywords
  (accent-insensitive). The user message tells the model to copy quotes in the report's
  language and write descriptions in English, and lists native labels and units
  (MSEK/Mkr = millions, TSEK/tkr = thousands…). English reports are still preferred when
  both exist.
- **Freshness (from the first batch run, where 34 of 96 reports were older than FY2024):**
  step 3 stops early only on a recent PDF (FY = last year or newer). Otherwise it scrapes
  the investor "annual reports" page right after the first map, which finds current
  reports hosted elsewhere (e.g. storage.mfn.se). A report older than 3 years is never
  returned (`not_found` with the reason instead).
- **Not reports:** calendar entries and `.ics` files, events, webcasts, press releases
  ("…publishes annual report"), news, notices/invitations, bond and prospectus documents,
  in English and the Nordic languages. Only PDF and web-page URLs count. A listing page
  ("annual-reports") is scraped for PDF links instead of being used as the report. An HTML
  report must have at least 20,000 characters.
- **Ranking among reports:** a recent PDF beats everything; when nothing recent is a PDF, a
  recent HTML report page beats an old PDF (AAK publishes web reports). "Presentation",
  "summary" and "factsheet" only exclude in the file name, since IR folders are often
  called `report-and-presentations`. The page scraped for links prefers pages without an
  old year, including the parent listing of an old report page, and never press releases.
- **Unusable files fall back:** if the chosen file is a blank placeholder (ABB's 2025 link
  was a 19 KB empty PDF), a blocked download or a short teaser page, the next 2 candidates
  step 3 already found are tried, with no extra search credits.
- **Subsidiary reports:** a URL naming another country ("ABB India Limited Integrated Annual
  Report") is excluded, unless the country word is part of the company's own name or
  country.
- **Units:** `lakhs` (100,000) and `crores` (10,000,000) were added for Indian-format reports.
- **Connection errors** count as an outage (batch pauses) only if the internet is really
  down. Otherwise, e.g. a site with a bad certificate, the company fails normally, and the
  download is retried with the browser-like client first.
- **User prompt additions** (the system prompt files are unchanged): quotes must be one
  passage under 25 words with no `...`, and the financials call names the chunks that look
  like statement tables. Without that hint the model took total assets from a summary table
  (same number, wrong source per rule 2).
- **`temperature=0`** for repeatable results. It is dropped automatically if a deployment
  rejects it.
- **Wrong chunk citations:** if a quote isn't in the chunk the model cited but appears
  exactly in another chunk that was sent, it passes, and the detail names both chunks. Seen
  on Nokia.
- **Space-grouped thousands:** Nordic reports write "19 889". The value check also reads a
  space-grouped run as one number. Plain spaces are still not removed when normalizing
  text, because in tables they also separate cells.
- **Quote edge punctuation is ignored.** The model often cuts a sentence and adds a ".".
  If a quote joins several real passages with `...`, each piece is checked on its own and
  the detail says `fragments`.
- **`period_end_date`** is normalized to YYYY-MM-DD in code. The model often returns
  "31 December", so the year is taken from `fiscal_year`. The model's raw text is kept in
  `period_end_date_raw`.
- **Quote normalization** also strips markdown table markup (`|`, `**`, `<br>`, `<sup>`),
  because PDF tables become markdown tables. Only `,` `.` and thin/no-break spaces between
  digits count as thousand separators. A normal space between digits separates table cells.
- **Loose quote match** (see Checks) passes but says `loose` in the detail. The LLM often
  drops the Notes column when quoting a table row.
- **Scope check:** a non-consolidated scope is recorded as `fail` (so status becomes
  `needs_review`) and listed in `warnings`.
- **Fiscal-year sanity:** the latest year in `fiscal_year` must be between (this year − 3)
  and this year.
- **LEI matching:** company lists rarely spell names the way GLEIF does ("Volvo AB" is
  "Aktiebolaget Volvo", "Orsted A/S" is "ØRSTED A/S", "Sampo plc" is "Sampo Oyj"). Each name
  is split into a base name and a legal form. Accents, punctuation and "(publ)" are
  ignored. Equivalent forms count as equal: AB = Aktiebolag(et), A/S = Aktieselskab,
  Oyj = Abp = plc, ASA, hf/ehf, "Public Limited Company" = PLC, etc. A name with no form is
  compatible with any form. GLEIF's name filter only finds names that *contain* the query,
  so we always also search by the base name (within `country_code` if given) and check
  GLEIF "other names", which catches renames such as Marel → JBT Marel and Össur → Embla
  Medical. Match tiers, best first: exact match registered in the given country, exact
  match anywhere (some Nordic-listed companies are registered abroad), then a GLEIF name
  that *ends with* the listed name in that country ("H & M Hennes & Mauritz AB" for
  "Hennes & Mauritz AB"), with fewest extra words winning. Within a tier, ACTIVE beats
  INACTIVE and ISSUED beats LAPSED. If more than one is left, no LEI is used (the reason is
  in `lei_lookup`), and `--lei` can resolve it. If GLEIF is down, the run continues
  without an LEI. Calls are spaced 1 s apart (GLEIF allows 60/min).
- **More LEI rules from a real 799-company Nordic list:** "Corporation"/"Corp"/"Company"
  are compatible with any legal form ("Metsä Board Corporation" = "Metsä Board Oyj");
  Faroese P/F and Polish "Spółka Akcyjna" (= SA) are known forms. If nothing matches in
  the listing country, the base name is searched worldwide (BW Energy and Archer are
  registered in Bermuda, Catena Media in Malta). A match on the current legal name beats
  a match on a former name ("F-Secure Oyj" is the new F-Secure, not WithSecure). A partial
  match may only add words *before* the listed name ("H & M Hennes & Mauritz AB"), never
  after it ("Volvo Car AB" is not "Volvo AB"). LEI misses aren't cached, so they're retried
  with the latest rules.
- **Wikidata name search (step 2b, free):** many small caps have a Wikidata item without
  the LEI. If the LEI lookup gives no website, Wikidata is searched by name. An item is
  accepted only if its label equals the company name (legal form ignored), its country
  (P17) equals the listing country (or the LEI country), and it lists an official website.
  On a 40-company sample this raised free website hits from 12 to 20 (`website_source`
  = `wikidata-name`).
- **Garbled names in the CSV are repaired:** UTF-8 text that was mis-decoded and saved
  again ("HuhtamÃ¤ki Oyj") is turned back into "Huhtamäki Oyj" on reading.
- **`summary.csv` open in Excel:** Excel locks the file. The batch retries, then skips that
  update and writes it after the next company, instead of crashing.
- **Wikidata website choice** (when several are listed): preferred rank, then sites tagged
  English (P407), then domain-name match, then generic TLD (.com) over the home-country
  TLD over a foreign one. That gives equinor.com, not equinor.no.
- **Wikidata site without a report:** Wikidata's "official website" is sometimes the
  consumer site (H&M → www2.hm.com; reports are on hmgroup.com). If step 3 finds no report
  there, the Firecrawl web search runs (2 credits), and step 3 is retried on the investor
  site it finds if that's a different domain.
- **Wikidata pacing:** at most 1 request/s, honours `Retry-After` on 429.
- **"LEI + legal name" search:** the fallback search query does **not** contain the LEI
  code. Tested on Unilever Ghana PLC, a query with the LEI returned only LEI/registry
  aggregator sites (lei.net, northdata, lei-registrar). Without it, the company's own site
  came first. The LEI is used instead as a ±0.1 country adjustment on the score: a matching
  country TLD gets a bonus, another country's TLD a penalty, `.com` is neutral. The
  aggregator domains were added to the blocklist.
- **Wikidata via the main API, not SPARQL:** `haswbstatement:P1278=<LEI>` search, then the
  item's P856 (official website). The SPARQL service was throttled to 1 request per minute
  during an outage while this was built. When several sites are listed: preferred rank
  first, then domain-name match, then the LEI country, then the shortest domain. That gives
  philips.com among 70+ regional sites, and siemens.com over siemens.com.mx. Wikidata's
  site is trusted as-is (no name-match threshold), because brand domains often differ from
  legal names (Tesco PLC → tescoplc.com).
- **Website score:** 70% domain-label match, 30% title match. Threshold 0.5 (`WEBSITE_MIN_SCORE`
  in `config.py`).
- **Chunking:** split on markdown headings when there are at least 0.3 headings per page,
  otherwise use page windows. Heading sections under 60 words are merged into the next one,
  and sections over 1,500 words are split by line (150-word overlap), so table rows stay intact.
- **Table-of-contents detection:** at least 5 lines, and ≥35% of non-empty lines, of the form
  "words … page-number" with no other numbers. Financial table rows have several numbers.
- **Keyword variants** were added to the spec's lists after testing on Unilever, which writes
  "Total liabilities and equity", "Business Group", "Unilever at a Glance",
  "Unilever's structure" and "Significant subsidiaries".
- **Section scoring:** the keyword score is divided by sqrt(words / 300), so a 1,700-word risk
  section that mentions "business model" once doesn't beat a 150-word segment note. A keyword
  inside a heading adds +8.
- **Statement boost:** a chunk gets +50 when it has a statement heading, at least 30 numbers,
  and numbers make up at least 20% of its tokens.
- The output also carries `source_pages` for each field and a `debug` block. These are
  additions beyond the required fields.
