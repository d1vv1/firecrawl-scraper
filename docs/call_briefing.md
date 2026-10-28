# Call briefing: company and executive-pay data collector

*26 October 2026. For the call with the client's developers. Full flow: `docs/pipeline_flow.html`. Open problems: `docs/known_issues.md`.*

## In one sentence

A CSV of companies goes in; out comes one row per data point (41 company fields, C01–C23) and per executive role and pay field (14 fields, R01–R11). Each row has the value, the source, the exact URL (a PDF opened at the page, an API request, an XBRL tag), the method, and a confidence grade.

Run it: `python -m extractor.datapoints <input.csv> --out output/<name>.csv --workers 2`

## The flow (the order of precedence)

1. **Identify:** GLEIF turns name, ISIN or register number into an LEI. The match must be exact; it never guesses.
2. **Official APIs (free, exact, grade A):**
   - GLEIF
   - ESMA FIRDS + ISO MIC list + OpenFIGI (ISIN, exchange, ticker)
   - Brønnøysund (NO), PRH (FI) and Companies House (UK)
   - SEC EDGAR
3. **Annual report:**
   - **Filings first, found by identifier:** ESEF (filings.xbrl.org), SEC, registers. Revenue and total assets come from XBRL tags, with no AI.
   - **Otherwise the company website, via Firecrawl:** find the site (Wikidata, then search); map it; rank the PDFs with guards against the wrong year or a subsidiary's report.
4. **AI pass on the report:**
   - The report is cut into chunks and scored per topic; the best chunks go to Gemini 2.5 Flash (Vertex), using structured output.
   - **Every value needs an exact quote.** We find that quote in the PDF ourselves, which gives the page link.
5. **Executive pay, per role.** Sources in order:
   1. a supplied URL;
   2. SEC 20-F exhibits or the DEF 14A proxy;
   3. (UK/IE) the annual report;
   4. the remuneration report on the site, including the report-downloads page;
   5. the annual report's pay section.

   **Checks:**
   - **Year:** an older year's pay is skipped.
   - **Policy:** read for targets and maxima.
   - **Derived values** are marked DERIVED.
   - **Total:** parts must add up to the total within 2%.
6. **Document fallback** for gaps: share, shareholder, governance and sustainability pages and so on. Up to 3 rounds of 3 documents.
7. **Pick the best value:** A > B > C, then API/XBRL > document > web page > derived. A disagreeing value is kept in `note`, never hidden.

*In run order, step 3 (finding and downloading the report) runs first: every company needs the report anyway, and the API step uses the filing's CIK and register number. Then the APIs run, and only then does the AI read the report, asked only for what the APIs left open (plus legal name, country and ticker for checks). The pipeline's old revenue-model/business-structure AI call is skipped (about 8,600 tokens per company).*

## Numbers

| | |
|---|---|
| Company fields filled | 80–82% (validation set 82%; Nordic/UK set 327 of 410) |
| Golden check, Nordic/UK (10 companies) | company values 16 of 18; pay figures 98 to 121 of 148 between runs (fresh AI answers vary; issue 5) |
| Equinor pay, found automatically | 66 to 89 of 91 golden figures between runs (via its 20-F exhibit) |
| Time | 7.7 min per new company on average (4–15); 3.6 min of wall-clock time per company with 2 workers; re-runs of cached companies take seconds |
| Firecrawl | at most 6 credits to find the report + 10 for pay and fallback documents per company; `--max-run-credits` caps the run; PDFs download for free |
| Tests | 308, run in about 10 s (`pytest`) |

**6,000 companies at 3.6 minutes each is about 15 days with 2 workers.** More workers need a higher Gemini quota on Vertex; we hit rate limits at 4 workers. Before the big run, a 200-company sample is planned to measure real credits per company and time per company.

## Why it was built this way

- **Quotes plus our own lookup** make every AI value checkable, with a page link. A quote we can't find gives grade C.
- **Exact sources beat the AI:** XBRL tags and registers always win over values read from text.
- **Numbers are copied as printed and scaled in code.** There's a guard for when the AI has already multiplied a value.
- **Everything is cached:** API answers for 7 days; documents, maps and AI answers keyed by prompt and chunks. A crash or re-run costs nothing for finished work.
- **Failing sources are skipped, not fatal.** If credits run out, the run continues on free sources and flags the company.

## How their code was used

- **Colleague's `extras/collect_company_data.py`:** we ported the company matching ideas (legal forms written as letters, LEI lookup by ISIN or register number, LEI name for SEC) and the Companies House part. Bolagsverket and CVR are parked because they need Swedish and Danish credentials.
- **`annual_report_fetcher` (client's crawler):** reviewed. It finds and downloads reports but doesn't parse them, so it covers our step 3 only.

## Known limits (say these before they ask)

1. **Merged pay-table columns:** the PDF conversion can merge two columns. The AI then reads those cells inconsistently between runs. Temperature is already 0; tested on 26 Oct, and no model setting fixes it. Plan: re-read only the flagged pay pages as images.
2. **Exchange segments** like Large/Mid Cap and Prime Standard need the exchanges' own files; FIRDS only gives regulated market vs MTF.
3. **UK holding companies:** their own filed accounts have no group figures. Register industry codes describe the holding company ("head office", SIC 70100).
4. **The report finder** can still pick a placeholder page or a plainly named subsidiary report. An identity check grades those values C.
5. **Scanned PDFs** are skipped: there's no OCR.

## What we need from them

1. **HANDOVER.md, or answers to the open definitions:**
   - base salary: salary alone, or salary plus benefits;
   - revenue line: "revenue" or "revenue and other operating income";
   - market-cap band thresholds, and which exchange rate to use.
2. **The Allshares industry taxonomy**, to classify sub-sector from the business description.
3. **Which fiscal year the golden files hold.** Nokia and Bang & Olufsen look like the previous year.
4. **The final company list and its format** (LEIs included makes matching certain), and the deadline for the 6,000 run.

## Likely questions, short answers

- **Can it hallucinate?** Only as grade C: any value whose quote we can't find in the source is marked C. Exact sources win, and every value links to its page.
- **Why Firecrawl?** Its map finds report URLs on sites we never crawl in full. PDFs bypass it, so it's mostly 1-credit maps and page scrapes. Self-hosting was evaluated in `docs/firecrawl_alternative_plan.md`.
- **Why Gemini?** It's on our GCP project; structured outputs work; it's cheap. The model is a setting (`VERTEX_MODEL`).
- **Adding a country?** Keywords and native terms are in `sections.py` and `report_finder.py`. A register is a function in `apis.py`.
- **Where to start reading the code?** `collect()` in `extractor/datapoints.py`, about 100 lines covering the whole flow.

## Agenda topics

*Their side comes from `annual_report_fetcher/` (README, INTRODUCTION, MODULE_MAP, docs, config) and `extras/` (PROCESS_NOTES, the 22 Oct validation page). Their fetcher was shared as a partial export: INTRODUCTION.md says the search and matching code, the AI prompts and the validation classifiers were left out on purpose, so it doesn't run.*

### 1. Overlap: what can be shared or reused

| Step | Theirs | Ours | Reuse |
|---|---|---|---|
| Company list | FactSet export with ticker, exchange and IR/home URLs; about 5,700 companies, 35 countries | CSV with name, country, optional LEI/ISIN | **Their FactSet IR URLs as our website input**: they skip our website search, saving up to 2 credits and avoiding wrong sites |
| Finding the annual report | Last year's URL shifted by a year → aggregators (companiesmarketcap, annualreports.com) → Gemini with Google grounding → manual review | Filings by LEI (ESEF, SEC, registers) → company website via Firecrawl | **Their 2,768 validated report URLs as our `annual_report_url` input**: 0 search credits for half the list. **Our ESEF/SEC route for them**: free, certain identity, no aggregator |
| Checking the PDF | Validator: company name and year on the cover pages; type classifier; quarantine folders | Ranking guards before download; identity check after reading (legal name and country) | Their cover-page check is the "check the cover before extracting" fix for our issue 4 |
| Extracting data | Out of scope: "downstream… separate repo" | Our main work: 41 company fields and pay per role, with quotes and page links | Nothing to reuse from them; this is what we bring |
| Identifiers, registers | Colleague's script: GLEIF, Companies House, PRH, SEC, Brønnøysund, Bolagsverket, CVR | Same (ported from it) except Bolagsverket and CVR; plus FIRDS and OpenFIGI | Already shared. Their Bolagsverket/CVR credentials would unblock our issue 8 |

**Ask:** can we get the validated URL list (company, year, URL, source) and the FactSet IR/home URLs in a CSV? It's the biggest single saving for the 6,000 run.

### 2. Missing pieces in their shared code: ranking and reasoning

What's present is configuration only, not the logic:
- **Thresholds:** auto-accept at score 2.5; download at 1.0; stop early at 2.0.
- **Source scores:** the prior-year URL 4.2; a companiesmarketcap slug 4.5.
- **Name match:** at least 50% of distinctive words.
- **Year:** a 4-year lookback.

Missing: the link scorer (`page_analyzer`, `known_source_search`), the per-language keyword lists (`keywords.py`), all Gemini prompts, and the validation classifiers (`company_match`, `validate_regex`, `validate_gemini`). Even the included `decide.py` and `pdf_validator.py` import missing modules.

**Ask:** was this removed on purpose (IP) or by accident? If it can be shared:
- **`keywords.py`** would extend our language coverage for Baltic, Balkan and Turkish markets, where their find rates are weakest.
- **`company_match`** could strengthen our identity check.

### 3. How they find candidate links (we use Wikidata)

Theirs, in order:
1. **Last year's confirmed URL with the year shifted** ("24-25" → "25-26"), checked by HEAD request, with a content hash to catch last year's file under a new name.
2. **Aggregators:** a guessed companiesmarketcap slug, the aggregators' own search, a slug cache.
3. **National portal scaffolding** (Turkey, Romania, Croatia, Bulgaria), mostly blocked.
4. **Gemini with Google Search grounding**, visiting up to 3 result pages.
5. **Manual Google search.**

DuckDuckGo is off ("blocked from this IP"), and so is their IR site crawl. Their policy is no paid search services.

Ours: filings by LEI first (ESEF, SEC, registers), so no link search at all for most EU/UK companies. Otherwise:
1. **Find the website:** Wikidata by LEI, then Wikidata by name, then Firecrawl search.
2. **Find the report on it:** Firecrawl map of the site, the investor page's PDF links, native-language terms, and report-downloads pages (including files behind buttons).

**Point to make:** their year-shift trick is cheap and smart for yearly re-runs; we could add it once we have last year's URLs. Their measured weak spot is the year: only 348 of 573 finds were 2025. Ours is anchored on filing dates and a year check.

### 4. Edge cases they've already hit

| Edge case | Theirs | Ours |
|---|---|---|
| Wrong company with a similar name | "European Green Transition" got the report of "European Medical Solutions", 255 times; Surgical Innovations matched Intuitive Surgical's report; 5.2% of 2,876 held PDFs were the wrong company | Filings by LEI can't collide; website reports: legal-form and subsidiary guards, identity check grades C. We also met it (Siemens' Dutch financing subsidiary, Volvo Treasury) |
| Parent vs group accounts | Fetcher: not addressed. Colleague's script prefers group (KONSERN) over parent-only (SELSKAP) accounts in Norway; notes the top Companies House hit is often a subsidiary | Our issue 6 (UK holding companies) is open; ultimate parent from GLEIF level 2 |
| Wrong year | Year-shifted URL serving last year's file (hash guard); year check is "containment-based" and can be fooled by a page mentioning a nearby year | Year from file name, dates, filing period; pay for an older year is skipped; stale yearly figures graded C |
| Missing reports | 49% validated coverage (2,768 of 5,701); Baltic, Croatian, Hungarian, Romanian, Turkish markets weakest; 15 of 43 sampled companies out of scope (growth markets, funds, delisted) | "not found in: …" rows with every source tried; Firecrawl search fallback |
| Separate remuneration report | 17 of 28 companies (Claude Desktop test) | Built: SEC exhibits, report-downloads pages, map search |
| Scanned PDFs | Judged by page count only (≥ 20 pages passes) | Rejected (no OCR) |
| Bot blocks, JS sites | Manual save; browser-like headers; portals blocked | Firecrawl; files read from the page's data |
| ESEF / XHTML | PDF only | ESEF is our first source |

**Ask:** which edge cases cost them the most time, and do they have a list of known-bad companies we should test against?

### 5. Their safety mechanisms vs ours

| | Theirs | Ours |
|---|---|---|
| Right file | Validator on the cover pages: company score ≥ 0.5, year confirmed, document type; byte-identical duplicates of another company's file rejected; nothing deleted, files moved to Success / Needs_AI / Mismatch; rejected URLs blacklisted | Identifier-based filings; ranking guards; identity check on the report's own legal name and country |
| Right value | (no extraction) Claude Desktop test: a blind second reader, scored against the CDP | Exact quote required and found in the source (B) or not (C); XBRL/API beats AI; units scaled in code; parts vs total check; disagreements kept in `note` |
| Human in the loop | Manual review step with override | None in the run; C grades and notes mark what to review |
| Politeness | 0.5 requests/s per domain, circuit breaker after 5 failures, retries with backoff | Firecrawl handles crawling; our own downloads retry once with a browser fingerprint; Gemini retries on rate limits |

**Worth borrowing:**
- the **duplicate-file guard**: the same PDF bytes for two companies means one is wrong;
- the **cover-page company check** before extracting;
- the **blacklist** of rejected URLs, so a re-run doesn't fetch them again.

### 6. Third-party aggregators

- **They rely on them heavily:** companiesmarketcap.com gave 66.7% of validated reports and annualreports.com 15.3%. Yahoo Finance, Bloomberg and MarketScreener don't appear anywhere in their material.
- **We use none.** Every value comes from the company, a regulator or a register: the source the protocol asks for.
- **Our only third-party lookups:** Wikidata (to find the website) and OpenFIGI (tickers, run by Bloomberg).
- **Risks of aggregators:**
  - an aggregator can serve the wrong company's or an old file (their slug collisions);
  - their terms of use may not allow automated downloading at scale;
  - the source URL isn't the company's own, which matters if the client must cite official sources.

**Ask:** does the client accept an aggregator copy as the source, or must the URL be the company's or regulator's? Their answer decides whether we should add companiesmarketcap as a fallback.

### 7. Their next steps: is PDF extraction one-time or ongoing?

- **What their material says:** extraction is "out of scope (downstream classify/extract stages, separate repo)". The fetcher is built to recur yearly, reusing last year's URL.
- **Pending on their side:**
  - measurement re-runs;
  - a repair pass for about 100 wrong-company files;
  - Baltic, Turkish and Polish sources (Nasdaq Baltic, KAP, GPW/ESPI);
  - browser-based fetching for portals.
- **The Claude Desktop work was research:** a 7-stage protocol on 30–54 companies, CEO pay extracted with PyMuPDF and scored against the CDP (85% match, 16% unit errors).

**Ask:**
1. Is our extraction expected to run once for the 6,000 list, or every year (each reporting season)? That changes priorities: yearly means caching last year's URLs, and the year-shift trick, become worth building.
2. Does the "separate repo" for extraction already exist on their side? Is our pipeline meant to become it, or to feed it?
3. Who maintains it after handover: their team or us?
