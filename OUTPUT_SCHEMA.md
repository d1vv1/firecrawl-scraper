# Output JSON: field guide

Every processed company gets one file, `output/<company_id>.json`. This guide explains
each field, using Bavarian Nordic A/S (`output/bavarian-nordic-a-s-da1f9b25.json`) as the
example.

A company that **failed** doesn't get this file. It gets `output/<company_id>.error.json`
instead (see [Error files](#error-files) at the end).

The file has seven parts:

1. [Who the company is](#1-who-the-company-is): input, identity, LEI
2. [Where the data came from](#2-where-the-data-came-from): website and report
3. [The financial figures](#3-the-financial-figures): revenue, total assets
4. [The descriptive fields](#4-the-descriptive-fields): revenue model, business structure
5. [The cross-check figure](#5-the-cross-check-figure)
6. [Checks, status and warnings](#6-checks-status-and-warnings)
7. [Run information](#7-run-information)

---

## 1. Who the company is

| Field | Example | Meaning |
|---|---|---|
| `company_id` | `"bavarian-nordic-a-s-da1f9b25"` | The ID from your CSV, unchanged. Also used for the file name. |
| `input_name` | `"Bavarian Nordic A/S"` | The company name exactly as given in the CSV. |
| `country_code` | `"DK"` | The country code from the CSV (the listing country). |
| `clean_name` | `"bavarian nordic"` | The name lowercased, with accents and legal form removed. Used only to match websites; you can ignore it. |
| `lei` | `"2138006JCDVYIN6INP51"` | The company's **Legal Entity Identifier**, found by searching GLEIF (the global LEI register) by name. `null` if no single, unambiguous match was found. |
| `lei_lookup` | `"exact name match"` | How the LEI was matched, or why it wasn't. See the values below. |
| `lei_record` | *(object)* | The company's entry in GLEIF. `null` when there's no LEI. Fields below. |

**`lei_lookup` values:**
- `exact name match`: the name matches GLEIF's legal name, ignoring case, accents and spelling of the legal form (AB = Aktiebolag, Oyj = plc, …), and it's registered in the CSV country.
- `exact name match (registered outside DK)`: same, but the company is registered in another country (e.g. Bermuda for some Norwegian-listed companies).
- `partial name match`: GLEIF's name has extra words *in front*, e.g. "H & M Hennes & Mauritz AB" for "Hennes & Mauritz AB". Worth a glance.
- `ambiguous: …`: several companies have that name, so no LEI was used. The message lists them.
- `no GLEIF record matching …`: nothing matched.

**`lei_record` fields** (straight from GLEIF):

| Field | Example | Meaning |
|---|---|---|
| `lei` | `"2138006JCDVYIN6INP51"` | Same as above. |
| `legal_name` | `"BAVARIAN NORDIC A/S"` | The official registered name. |
| `country` | `"DK"` | Country of the registered (legal) address. |
| `jurisdiction` | `"DK"` | The legal system the company is registered under. |
| `legal_form_id` | `"ZRPO"` | ISO 20275 legal-form code (here: Danish A/S). |
| `entity_status` | `"ACTIVE"` | `ACTIVE` or `INACTIVE` (e.g. merged or dissolved). |
| `registration_status` | `"ISSUED"` | Whether the LEI is up to date: `ISSUED` = current, `LAPSED` = not renewed. |
| `registered_as` | `"16271187"` | The company's number in its national register (here the Danish CVR number). |

---

## 2. Where the data came from

| Field | Example | Meaning |
|---|---|---|
| `website` | `"https://www.bavarian-nordic.com"` | The company website the report was searched on. |
| `website_source` | `"wikidata"` | How the website was found. See the values below. |
| `website_score` | `null` | Only for web-search results: how well the domain and page title matched the name, from 0 to 1 (0.5 needed). `null` when the website came from Wikidata. |
| `report_url` | `".../bn_annual_report_2025.pdf"` | **The exact document the text came from.** Open it to verify anything. For the ESEF route this is the filing's `.xhtml` report. |
| `data_source` | `"esef"` | Where the data came from: `esef` (tags and text from the company's ESEF filing), `edgar` (tags and text from its SEC 10-K / 20-F), `… tags + website text` (tagged figures from the filing, text from the English report on the website), or `website` (everything from the report found on the website). |
| `filing` | *(object or `null`)* | The filing used: `type` (`esef` / `edgar`), `form` (`ESEF`, `10-K`, `20-F`…), `filing_id` (ESEF id or SEC accession number), `cik` (SEC filings), `period_end`, `report_url`, and for ESEF `viewer_url` (an XBRL viewer showing each tag) and `package_url`. `null` if no filing was used. |
| `report_type` | `"pdf"` | `pdf`, or `html` if the annual report is a web page. |
| `fiscal_year` | `"2025"` | The financial year the figures are for, as written in the report (`"2025"`, `"2024/25"`, …). |
| `period_end_date` | `"2025-12-31"` | The balance-sheet date, as YYYY-MM-DD. `null` if the report doesn't state it clearly. |
| `period_end_date_raw` | `"2025-12-31"` | The date as the model read it from the report, before conversion (e.g. `"31 December"`). |

**`website_source` values:**
- `wikidata`: the LEI is listed on Wikidata together with the official website. Free and most reliable.
- `wikidata-name`: found on Wikidata by company name and country (for companies whose LEI isn't on Wikidata). Free.
- `search+lei`: found by a Firecrawl web search (2 credits), scored using the LEI's country.
- `search`: found by web search, without an LEI.
- `search (wikidata site had no report)`: Wikidata gave a site with no annual report (e.g. a shop site), so the investor site was found by web search.
- `override` / `derived from --report-url`: given on the command line.

---

## 3. The financial figures

`revenue` and `total_assets` have the same shape. Here's revenue:

```json
"revenue": {
  "value": 6243956.0,
  "unit": "thousands",
  "currency": "DKK",
  "label_in_report": "Revenue",
  "scope": "consolidated",
  "quote": "Revenue|3|6,243,956|5,716,206",
  "chunk_id": 334,
  "not_found_reason": null,
  "value_full": 6243956000.0,
  "source_pages": [123]
}
```

| Field | Meaning |
|---|---|
| `value` | The number **exactly as printed** in the report's table: here 6,243,956, in thousands. Not converted. |
| `unit` | The unit from the table header: `units`, `thousands`, `millions`, `billions` (and `lakhs`, `crores` for Indian reports). |
| `currency` | ISO 4217 currency code, e.g. `DKK`, `SEK`, `EUR`. |
| **`value_full`** | **`value` × `unit`, worked out in code (not by the LLM).** Here 6,243,956 × 1,000 = **DKK 6,243,956,000** (≈ DKK 6.24 billion). **This is the number to use for comparisons.** |
| `label_in_report` | The row label the report uses: "Revenue", "Net sales", "Turnover", "Nettoomsättning", "Liikevaihto", … |
| `scope` | `consolidated` (whole group: what we want), `parent_only` (the parent company alone, usually much smaller), or `unclear`. |
| `quote` | The short text the figure was read from, copied from the report. Table rows look like `Revenue\|3\|6,243,956\|5,716,206`: the label, a note number (3), this year, last year. |
| `chunk_id` | Which excerpt of the report the quote came from. The report is split into numbered chunks before it's sent to the LLM. |
| `source_pages` | **The PDF page(s)** of that excerpt. Open the PDF at page 123 to see the income statement. |
| `not_found_reason` | When `value` is `null`, the model's explanation of why the figure wasn't found. Otherwise `null`. |
| `method` | `xbrl_tag`: read directly from the filing's XBRL tag (ESEF or SEC; exact, no AI). `llm`: read by the AI from the report text. |
| `xbrl_concept` | For `xbrl_tag` figures, the tag that was read, e.g. `ifrs-full:Revenue`. `null` otherwise. |

**Tagged figures look slightly different:** `value` is the full number in `units` (e.g. 6,243,956,000 DKK), `quote` names the tag and period (e.g. `ifrs-full:Revenue = 6,243,956,000 DKK (2025-01-01/2025-12-31)`), and `chunk_id` / `source_pages` are `null` because the number comes from the filing's data, not from a page of text.

For revenue the figure comes from the **income statement**; for total assets, from the **balance sheet** (statement of financial position). Both are for the current year: the prior-year column is ignored.

---

## 4. The descriptive fields

### `revenue_model`: how the company makes money

| Field | Example | Meaning |
|---|---|---|
| `categories` | `["product_sales", "services"]` | Main revenue types, most important first. Allowed values: `product_sales`, `subscription`, `services`, `licensing_royalties`, `commission_marketplace`, `advertising`, `interest_income`, `other`. |
| `description` | "The company sells vaccines primarily to governments and consumers…" | 1–2 plain sentences, in English: what it sells, to whom, through which channels. |
| `quote` | "Revenue for the year was DKK 6,244 million…" | Text from the report that supports the answer (in the report's language). |
| `chunk_id`, `source_pages` | `44`, `[23]` | Where the quote came from (as above). |

### `business_structure`: how the company is organised

| Field | Example | Meaning |
|---|---|---|
| `legal_form` | `"A/S"` | The legal form: A/S, AB, ASA, Oyj, plc, SE, … |
| `is_listed` | `true` | `true` only if the report says the shares trade on a stock exchange. `null` if it doesn't say. |
| `ultimate_parent` | `null` | The company that controls this one, if the report says there is one. **`null` means it's the top company of its group** (normal for listed companies). |
| `segments` | `["Public Preparedness", "Travel Health"]` | The reported business segments, named as in the report. Not brands or subsidiaries. |
| `description` | "Bavarian Nordic A/S is a publicly listed company organized into two main segments…" | 1–2 plain sentences, in English. |
| `quote`, `chunk_id`, `source_pages` | | Supporting text and its location (as above). |

---

## 5. The cross-check figure

```json
"cross_check": { "total_equity_and_liabilities": { ... same shape as revenue ... } }
```

**Total equity and liabilities**, the other side of the balance sheet. A balance sheet always balances, so this must equal total assets. It's extracted only to check that total assets was read correctly (the `balance` check). You don't need to use it.

---

## 6. Checks, status and warnings

### `status`: the one field to filter on

| Value | Meaning |
|---|---|
| `ok` | Every check on the **financial figures and the company** passed. Safe to use. |
| `needs_review` | At least one of those checks failed. Look at `checks` for the reason. |
| `not_found` | A report was processed, but neither revenue nor total assets was found in it. |

### `checks`: one entry per test

```json
{ "name": "quote", "target": "revenue", "result": "pass", "detail": "exact match in chunk 334" }
```

- `name`: which test (below).
- `target`: which field it tested (`revenue`, `total_assets`, `fiscal_year`, `revenue_model`, …).
- `result`: `pass`, `fail` or `skipped` (e.g. nothing to test because the value is missing).
- `detail`: the explanation. Always read this on a fail.

| Check | What it tests | A fail means |
|---|---|---|
| `quote` | The quote really appears in the report. | **Probable hallucination**: the model's text isn't in the report. The detail shows the quote. A detail like "exact match in chunk 337 (model cited chunk 334)" is a pass: the text is in the report, the model only cited the wrong excerpt number. |
| `value_in_quote` | The extracted number appears in its own quote. | The number may have been taken from somewhere else. |
| `scope` | The figure is `consolidated`. | Parent-only or unclear figure. |
| `sanity` (on a figure) | Value > 0, valid currency code, unit present. | Something basic is wrong with the number. |
| `sanity` (on `fiscal_year`) | The fiscal year is within the last 3 years. | The report is too old. |
| `balance` | Total assets = total equity and liabilities, within 0.5%. | One of the two balance-sheet numbers was misread. |
| `entity` / `company_name` | The company's name appears in the report's first 20 pages. | **Possibly another company's report.** |
| `entity` / `currency` | The reporting currency fits the company's country (home currency, EUR or USD). | **Possibly a subsidiary's report** (e.g. INR for ABB Ltd meant ABB India's report was used). |

### `warnings`

Problems that **don't** change the status:
- a failed quote on `revenue_model` or `business_structure` (the descriptive text might be slightly reworded; the numbers are unaffected)
- a non-consolidated `scope`

> **About this example file:** it was produced in the first batch run, *before* two changes:
> - Back then, the two descriptive quote failures counted towards the status. That's why
>   Bavarian Nordic shows `needs_review` with an empty `warnings` list, even though every
>   check on the figures passed.
> - The `entity` checks didn't exist yet.
>
> After the next `--refresh` run, this company becomes `ok`, the two descriptive failures
> move to `warnings`, and the two `entity` checks are added.

---

## 7. Run information

| Field | Example | Meaning |
|---|---|---|
| `extracted_at` | `"2026-10-15T22:42:59+00:00"` | When this result was produced (UTC). |
| `model` | `"gpt-4.1-mini-1"` | The Foundry deployment that did the extraction. |
| `firecrawl_credits_used` | `1` | Firecrawl credits this company cost in **this** run. `0` when everything came from the cache. |
| `debug` | *(object)* | Technical details for troubleshooting. You can ignore it. |

**`debug` fields:**
- `cache_used.discovery` / `cache_used.report`: `true` if the website/report choice or the converted report were reused from an earlier run (`cache/`).
- `markdown_file`: the converted report text in `cache/` (with `<!-- page N -->` markers).
- `chunks_total`: how many excerpts the report was split into.
- `chunks_sent.financials` / `chunks_sent.qualitative`: which excerpts were sent to the LLM for each question.

---

## Error files

A company that failed gets `output/<company_id>.error.json` instead:

| Field | Meaning |
|---|---|
| `company_id`, `company_name`, `country_code` | From the CSV. |
| `error_type` | The kind of failure. See below. |
| `error` | The message, usually including what to do next (e.g. "Pass --report-url URL"). |
| `network_error` | `true` if the internet connection was the problem. Retried automatically on the next run. |
| `firecrawl_credits_used` | Credits spent before it failed. |
| `at` | When it failed (UTC). |

**Common `error_type` values:**
- `ReportNotFoundError`: no usable annual report was found on the website, or only reports older than 3 years.
- `WebsiteNotFoundError`: no confident match for the company's website.
- `NeedsOCRError`: the PDF is a scan with no text layer (out of scope).
- `DownloadError`: the report couldn't be downloaded (e.g. blocked), or was only a short teaser page.

The whole run is also summarised in `output/summary.csv` (one row per company) and `output/fill_rate.md` (fill rates per country).
