# Plan: priority fields under 3% not found

*18 November 2026 · firecrawl-scraper (`python -m extractor.datapoints`) · status: decisions made (22 Nov); Phase A and B done, tested on 50 companies and applied to the combined file (22 Nov); Phase C next*

## Progress

**19 Nov 2026, Phase A (branch `not-found-phase-a`).** The rules run in `datapoints.refresh`, so `python -m extractor.combine --into output/fy2025_runs_datapoints.csv --gleif` applies them to every company, including those whose caches are on other machines. Tests: `tests/test_not_found_phase_a.py`.

| # | Done | Measured on a copy of the 18 Nov file (missing before → after) |
|---|---|---|
| A1 | `apis.gleif_parent`; `combine --gleif` asks GLEIF again for every empty `ultimate_parent`. NON_CONSOLIDATING → "none (no consolidating parent)" **only once signed off** (`SIGNED_OFF_RULES=gleif_non_consolidating`, decision D1). Never used for ownership. | ultimate_parent 205 → 204 without sign-off (PETROLIA: the parent record, a stale cache); **22 (2.7%)** with it |
| A2 | `ownership_from_holders`: needs 2+ named holders with stakes; groups ("Institutional", "Free float") left out. Largest under 20% → controlling_owner "none", ownership_type "widely_held"; 20% or more → that holder's name only (its type is not in the list); every stake under 5% (3+ holders) → pe_stake_5pct "no" | controlling_owner 124 → 77, ownership_type 125 → 78, controlling_owner_name 120 → 71 (47 now "not applicable"), pe_stake_5pct 139 → 136 |
| A3 | `zero_from_total`: benefits or pension 0 when the stated total is the sum of the other amounts within **0.5%** (tighter than XF-02's 2%: a benefit is often under 2% of the total). **Only once signed off** (`zero_from_total`, D1) | benefits_value 951 → **579 (19.2%)**, pension_contribution 1,121 → **584 (19.4%)** |
| A4 | `pay_currency_from_amounts`: the role's own amounts' currency, else the company's other roles' | pay_currency 134 → **11 (0.4%)** |
| A5 | Partly: a role whose stated total is 0 → its empty amounts "not applicable: no pay for the year". **Not done:** moving non-executive entries into the board row (a scope change, to look at with the 50-company test) | base_salary 400 → 392; about 20 per pay field |
| A6 | Share prices in "pence", "p", "GBx", "USD cents" and a page's "ZAR cents" → the whole currency (10 prices); no band from a price dated over a year from the fiscal year end (Centrica's 2023 price). **Not done:** several share classes | market_cap_band 398 → 391 |

The sign-off switch is gone since 22 Nov: the D1 rules are decided and on (see section 6); `RULES_OFF=<rule>` in `.env` switches one off. Centrica's report prints "1.4065 pence" for £1.4065: its price is now 0.014065 GBP and wrong (it was wrong before as well, and it is a 2023 price); fix it by hand.

**22 Nov 2026, Phase B (branch `not-found-phase-b`, on top of Phase A; scraper version 6).** Tests: `tests/test_not_found_phase_b.py`. Measured on a copy of the 1,508-company file of 22 Nov (Phase A rules, then Phase B's rules on saved rows); prompt changes show only after a re-run.

| # | Done | Effect (missing before → after, on saved rows) |
|---|---|---|
| B1 | Pay prompt: a dash, "nil" or "0" in a component's own cell is 0; a component folded into another column is null and named in that column's `includes` (Italy's Schema 7-bis). `pay_tables.py` already read dashes as 0. D4 on saved rows: `included_in_other` | re-run needed; a few roles now "included in" |
| B2 | Prompts: "None" / "no pension" / "cash allowance" when the text says so, quoting it. On saved rows: `shareholding_none_if_absent`: "None" (confidence C) when the role pay was read from a remuneration report that was searched for the rule | shareholding_requirement 37.1% → **21.4%** |
| B3 | ESEF tags: the company's own EBITDA tag, else `ProfitLossFromOperatingActivities` (note says "operating profit"); `combine --esef` and every new run. The prompt already had the operating-profit fallback | ebitda 10.1% → **8.0%** |
| B4 | ESEF tags `NumberOfSharesOutstanding`, else `NumberOfSharesIssued` (note says which) | shares_outstanding 7.4% → 7.2% |
| B5 | Prompt: year-end close wording in each language, pence/cents named. The planned `market_cap` fact was dropped: `DataPointFacts` is at Vertex's schema size limit, and any further nested fact gives 400 INVALID_ARGUMENT | share_price 76.1% → 68.1% on the 50 |
| B6 | An empty answer for the financial facts, or a pay document with no amount at all, is asked once more of `LLM_FALLBACK_MODEL` (default Gemini 3.1 Pro preview on Vertex: the project has no 2.5 Pro or 3 Pro; "off" to switch off); the cache records the model and that the retry was made. A model the project rejects is not asked again in the run; an empty answer is a miss for that question only | not measured: in the test it answered once (empty) and was then switched off, since fixed |
| B7 | The GB annual report is already read whole (up to 150,000 words); the GB gaps (86 of 1,124 roles) are mostly members who left, whose single-figure row is all dashes: `no_pay_for_year` now reads such a row as no pay | about 20–40 GB roles |

**50-company test (22 Nov).** List `data/not_found_phase_b_test.csv` (50 companies with the most priority gaps, 12 countries), run with `--redo` at version 6: 118 Firecrawl credits, no company failed (a first attempt failed 47 of 50 on the `market_cap` schema error and the missing 2.5 Pro; both fixed in `ecd1421`). Output `output/not_found_phase_b_test_datapoints.csv`. Missing values on the 50, as the dashboard counts them:

| Field | Original | Rules only (A + B on saved rows) | Re-run (+ rules) |
|---|---|---|---|
| base_salary | 40.0% | 40.0% | **17.7%** |
| total_remuneration | 37.6% | 37.6% | **29.3%** |
| benefits_value | 72.3% | 61.1% | **41.5%** |
| pension_contribution | 70.0% | 57.7% | **42.6%** |
| pay_currency | 16.4% | 1.3% | 1.4% |
| pension_type / benefits | 35.4% / 37.5% | same | 25.0% / 25.0% |
| shareholding_requirement | 76.6% | 51.1% | **39.6%** |
| ownership_type | 31.9% | 29.8% | 25.0% |
| ultimate_parent | 32.6% | 8.7% | 8.3% |
| share_price | 76.1% | 76.1% | 68.1% |
| market_cap_band | 78.3% | 78.3% | 70.2% |
| revenue / total_assets | 19.1% / 12.8% | same | 22.9% / 18.8% |
| **All priority fields** | **44.0%** | **38.1%** | **28.9%** |

The 50 are the worst companies, so the rates are far above the file's. Revenue and total assets lost values at C-Capital Holdings and SECO: the run now rejects their reports as another company's (the old values came from those same reports, so they were likely wrong), plus run-to-run misses at Helios Solar, Cykel AI (EBITDA) and Arzneiwerk (shares). Share price and the band stay the largest gap: Phase C's exchange files are still needed.

**Applied to the combined file (22 Nov):** the 50 spliced in and `combine --gleif --esef` run over all 1,510. Missing on the whole file: ultimate_parent 25.4% → 2.2%, benefits_value 32.3% → 17.3%, pension_contribution 38.8% → 18.7%, shareholding_requirement 37.1% → 20.8%, ebitda 10.1% → 7.7%, share_price 45.2% → 44.8%, market_cap_band 47.8% → 46.5%. Hard fails 3,013 → 3,035 on 1,792 more values (improvement log 66).

Still open in B: the fallback model's effect (re-run the companies with an empty answer).

## Goal

Bring the dashboard's "not found" rate under 3% for these fields (priority 0 is highest):

| Group | Field | Priority |
|---|---|---|
| Financials | ebitda | 0 |
| Financials | total_assets, revenue, shares_outstanding | 1 |
| Pay: total | total_remuneration | 0 |
| Pay: fixed | base_salary | 0 |
| Pay: fixed | benefits_value | 1 |
| Pay: fixed | pension_contribution, pay_currency | 2 |
| Pay policy | pension_type, benefits, shareholding_requirement | 2 |
| Ownership and control | largest_holders, controlling_owner, controlling_owner_name, ownership_type, pe_stake_5pct, ultimate_parent | 2 |
| Listing and market | market_cap_band, share_price | 1 |

**How "not found" is counted:** the dashboard's definition (`extractor/dashboard.py` `value_status`). A value is not found when it is blank and its note does not start with "not applicable" or "not collected". Values that don't apply are left out of the count.

**Baseline:** `output/fy2025_runs_datapoints.csv`, 1,272 companies, 18 Nov 2026, after Praveen's splice. Revanth J's run is not in it yet. At under 3%, a company field can be missing for at most about 24 of the roughly 815 companies it applies to. A pay field can be missing for at most about 90 of the roughly 3,024 executive roles.

---

## 1. Where we are and why

| Field | Missing now | Found | Main causes (failure codes) |
|---|---|---|---|
| ebitda | **11.3%** (92) | 725 | NOT_DISCLOSED 70, REPORT_NOT_FOUND 16, CREDITS_EXHAUSTED 3 |
| revenue | 7.6% (63) | 762 | NOT_DISCLOSED 40, REPORT_NOT_FOUND 18 |
| total_assets | 6.1% (50) | 767 | NOT_DISCLOSED 28, REPORT_NOT_FOUND 17 |
| shares_outstanding | 8.3% (68) | 754 | NOT_DISCLOSED 47, REPORT_NOT_FOUND 16 |
| total_remuneration | **9.1%** (276 roles) | 2,747 | REMUNERATION_REPORT_NOT_READ 185, NOT_DISCLOSED 91 |
| base_salary | **13.2%** (400) | 2,624 | REMUNERATION_REPORT_NOT_READ 227, NOT_DISCLOSED 173 |
| benefits_value | 32.0% (966) | 2,057 | REMUNERATION_REPORT_NOT_READ 626, NOT_DISCLOSED 340 |
| pension_contribution | 37.7% (1,141) | 1,884 | REMUNERATION_REPORT_NOT_READ 577, NOT_DISCLOSED 564 |
| pay_currency | 4.4% (134) | 2,889 | REMUNERATION_REPORT_NOT_READ 82, NOT_DISCLOSED 52 |
| pension_type | 13.3% (142) | 928 | NOT_DISCLOSED 64, REMUNERATION_REPORT_NOT_READ 50, REPORT_NOT_FOUND 21 |
| benefits | 12.8% (136) | 926 | REMUNERATION_REPORT_NOT_READ 76, NOT_DISCLOSED 34, REPORT_NOT_FOUND 20 |
| shareholding_requirement | 37.4% (385) | 645 | NOT_DISCLOSED 220, REMUNERATION_REPORT_NOT_READ 132, REPORT_NOT_FOUND 23 |
| largest_holders | 15.2% (123) | 684 | NOT_DISCLOSED 106, REPORT_NOT_FOUND 13 |
| controlling_owner | 15.2% (124) | 691 | NOT_DISCLOSED 101, REPORT_NOT_FOUND 16 |
| controlling_owner_name | 18.6% (120) | 525 | NOT_DISCLOSED 99, REPORT_NOT_FOUND 13 |
| ownership_type | 15.3% (125) | 690 | NOT_DISCLOSED 102, REPORT_NOT_FOUND 16 |
| pe_stake_5pct | 17.3% (139) | 664 | NOT_DISCLOSED 121, REPORT_NOT_FOUND 13 |
| ultimate_parent | 25.2% (205) | 607 | NOT_DISCLOSED 195 |
| share_price | **46.3%** (377) | 438 | NOT_DISCLOSED 349, REPORT_NOT_FOUND 19 |
| market_cap_band | **48.8%** (398) | 417 | DERIVATION_INPUT_MISSING 387 (no share price), FX_RATE_MISSING 10 |

Missing share prices by country: GB 124, IT 61, GR 55, DE 36, CH 23, ES 19, BE 16, NO 12, NL 11, AT 8, PT 8, SE 3, FI 1.

### 1.1 What the analysis found

1. **About half of the gaps were written by old scraper versions.** These are counts of missing values by `scraper_version`; the current version is 5.

   | Field | v0 | v1 | v2 | v4 | v5 |
   |---|---|---|---|---|---|
   | revenue | 0 | 11 | 12 | 15 | 25 |
   | total_assets | 1 | 18 | 7 | 10 | 14 |
   | ebitda | 7 | 18 | 10 | 22 | 35 |
   | shares_outstanding | 11 | 18 | 3 | 7 | 29 |
   | base_salary | 8 | 96 | 62 | 85 | 149 |
   | pension_contribution | 27 | 178 | 195 | 183 | 557 |
   | share_price | 37 | 36 | 58 | 35 | 211 |
   | ultimate_parent | 25 | 14 | 49 | 31 | 86 |

   Some of these are clearly stale. ASOS has no `total_assets` although its ESEF filing was read (v0). adidas and Arbonia hit a `ReportNotFoundError` under v1. Large companies with no revenue or share count (adidas, ASOS, easyJet, BAE Systems, Barclays) are pipeline misses, not companies that don't disclose.

2. **`ultimate_parent`: GLEIF's `NON_CONSOLIDATING` is turned into a blank.** All 188 missing companies with an LEI were checked against GLEIF Level 2 on 18 Nov 2026:

   | GLEIF code | Companies |
   |---|---|
   | NON_CONSOLIDATING | 182 |
   | NON_PUBLIC | 3 |
   | NATURAL_PERSONS | 1 |
   | NO_LEI | 1 |
   | a parent record exists (shown blank: a bug or a stale cache) | 1 |

   `extractor/apis.py` `gleif_values()` sets a value only for `NO_KNOWN_PERSON` and `NATURAL_PERSONS`.
   - **GLEIF's meaning:** the entity has no accounting-consolidation parent. No parent includes it in consolidated accounts.
   - **Caveat:** the code also allows a *controlling* entity that does not consolidate (a PE fund, a foundation, the state, an investment entity). So it can fill `ultimate_parent`, but it must **never** be used to work out `controlling_owner` or `ownership_type`.

3. **The client's field list (`accuracy/inputs/fields_list.json` and `field_requirements.json`) already settles several gaps:**

   | Field | The client's rule | Our behaviour today |
   |---|---|---|
   | shareholding_requirement | "record 'None' if absent" | the prompt says "Null if there is no such rule" |
   | benefits_value | "record 0, not blank" | null unless an amount is printed |
   | ownership_type | "record 'widely held', not blank" | set only when the AI quotes a "no 20% holder" sentence |
   | ebitda | "EBITDA, else operating profit (note says which)" | EBITDA only |
   | controlling_owner, ownership_type, pe_stake_5pct | "Derived from largest_holders" | read separately by the AI |
   | ultimate_parent | source "GLEIF; annual report; shareholder page" | GLEIF used, but see 2 above |
   | market_cap_band | severity "**Never used**: size is shown as values, not bands; derivation looks broken" | |

4. **The pay gaps are partly gaps in how roles are defined.** The 1,141 missing `pension_contribution` values, by the role's title (rough rules):

   | Bucket | Pension | Benefits | Base salary | Total |
   |---|---|---|---|---|
   | Named executive, total = the other parts (implies 0) | 321 | 221 | 9 | |
   | Former member, or left during the year | 171 | 146 | 116 | 49 |
   | Aggregate group ("other members") | 146 | 153 | 74 | 58 |
   | Non-executive or board entry (shouldn't be an executive role) | 136 | 100 | 36 | 19 |
   | Named executive, other | about 360 | about 340 | about 165 | about 150 |

   - **Italy:** the CONSOB Schema 7-bis Table 1 has **no pension column**; pension is inside "benefici non monetari" or "altri compensi".
   - **Switzerland:** tables often combine "pension and social security".
   - **UK:** the Directors' Remuneration Report is inside the annual report. So REMUNERATION_REPORT_NOT_READ there means the section was missed in extraction, not that a document is missing.

5. **Ownership: 55 companies have `largest_holders` filled but no `controlling_owner` or `ownership_type`.** Examples: 4imprint (largest holder 7.13%), Aberdeen (8.3%), Bioversys (15.98%). All of them can be worked out under the client's own rule. 66 companies are missing all four ownership fields: GB 20, CH 11, DE 10, ES 7, IT 7, others 11.

6. **Source restrictions.** The client's source review bans **Yahoo (including yfinance), Börsdata, LSEG/Refinitiv, Infront and LinkedIn**. It also holds the **Nasdaq Nordic website** and Allabolag.se until their terms are checked (`docs/document_fallback_plan.md`, "Off-site sources"). Its rules: off-site values get at most confidence C, and aggregators, news and people-search sites are never used.

---

## 2. Research: external sources for share price and market cap

Researched on 18 Nov 2026. **[V]** means read on the official page; **[I]** means inferred or from memory, to be checked before building.

### 2.1 Ranked recommendation

1. **The company's own figure (primary source, no licence issue).**
   - The annual report's share section ("The share", "Die Aktie", "Andamento del titolo", "Share information") very often states the year-end close and the market cap [I]. Greek reports state κεφαλαιοποίηση [I]. The prompt and document fallback can target it better (B5).
   - Share-price look-up tools on company IR sites: Euroland's "Share Price Look-Up" returns the close for a chosen date as HTML or Excel [V]; Euronext Corporate Solutions "My Share Price Live" [V]; Investis, Q4, QuoteMedia [I]. These tools are rare at AIM, Greek and growth-market small caps, which is exactly where our gaps are [I].
   - A market cap the company states gives the band directly, even without a price.

2. **The home exchange's official close for the year-end date:**

   | Venue | Route | Lookup | Terms and risks | Covers |
   |---|---|---|---|---|
   | **Athens** (now Euronext Athens) | Daily closing-price file per trading day: `https://athens.euronext.com/en/market-data/statistics/eod-closing-prices/regulated/stocks/0/{YYYYMMDD}/xlsx` (also `/txt`) [V]; a field specification xlsx is linked [V]. Daily Official List PDFs, e.g. `.../sites/default/files/2025-12/DOL-2025-245%20%2823%20Dec%29.pdf` [V that it exists], probably with closing price, listed shares and market value per company [I] | Whole market in one file | Not yet checked: whether 2025 dates are still served, the columns, the terms | GR 55 |
   | **SIX Swiss Exchange** | Daily closing-price files: `https://www.six-group.com/en/market-data/statistics/historical-prices.html` [V]. Avoid the undocumented `fqs/movie.json` endpoint | Whole market | Site's general terms; format and history depth not stated | CH 23 |
   | **Wiener Börse** | `https://www.wienerborse.at/en/stock-prime-market/{slug}-{ISIN}/historical-data/`, CSV back to 2000 [V] | ISIN | **Prices are adjusted for corporate actions** [V]; volume 0 when there was no trade | AT 8 |
   | **Euronext** (Milan, Brussels, Amsterdam, Lisbon, Oslo, Paris, Dublin) | `https://live.euronext.com/{lang}/popout-page/getHistoricalPrice/{ISIN}-{MIC}`, csv/xls/txt, **adjusted or unadjusted** option [V] | ISIN-MIC | Terms (`euronext.com/terms-use`): personal non-commercial use only; **no robots, no systematic retrieval into databases** [V]. Commercial use needs a Euronext Market Data licence (databyeuronext@euronext.com; NextHistory product) | IT 61, BE 16, NO 12, NL 11, PT 8 |
   | **London Stock Exchange / AIM** | No free programmatic route; the site disclaimer bans "programmatic, scripted or other mechanical means" [V]. **Lead:** the "Issuer list" archive at `londonstockexchange.com/en/reports/issuers-and-instruments` is a monthly xlsx with, from memory, a market cap (£m) column per company [I]. A December 2025 copy would give an official month-end market cap for every GB company, enough for the band | | LSE Data Shop sells history by ISIN; whether it counts as banned "LSEG" is for the client | GB 124 |
   | **Deutsche Börse (Xetra)** | No documented free history; paid Data Shop / end-of-day snapshots [V] | | Terms likely forbid automated reuse [I] | DE 36 |
   | **BME (Spain)** | No official per-share history found | | | ES 19 |
   | **Nasdaq Nordic** | On hold (source review) | | | SE 3, FI 1: do by hand |

3. **Paid fallback:**

   | Vendor | Coverage | Unadjusted close | Cost | Redistribution |
   |---|---|---|---|---|
   | **EODHD** | LSE and XETRA [V]; Athens, Milan, SIX, Vienna, Madrid probably [I] | `GET /api/eod/{SYM}.{EXCH}`: `close` is raw, `adjusted_close` is adjusted [V]; ISIN search `GET /api/search/{ISIN}` [V] | All-world end-of-day $19.99/month, 100k calls a day [V]; commercial plans priced on request | Personal plans: no redistribution. Commercial: "upon prior written approval" [V] |
   | Financial Modeling Prep | Euronext [V]; others not confirmed | `/stable/historical-price-eod/non-split-adjusted` [V] | Enterprise tier | Needs a display and licensing agreement [V] |
   | Twelve Data | European prices from Cboe UK and NL feeds (not the home exchange's official close) [V] | | from $9k a year for business add-ons [V] | Separate agreement [V] |
   | Bloomberg, FactSet, Capital IQ, Morningstar | Everything, including historical shares and market cap [I] | yes | five figures or more a year [I] | Explicit licence; delivering only a band may count as "derived data" [I] |

   EODHD's historical market cap endpoint covers the US only [V], so it doesn't help here.

4. **Band without a price (lower bound only).** Indices weight by free-float market cap, so membership proves a minimum, never a maximum:
   - FTSE 100, DAX and STOXX Europe 600 members → large [I]. STOXX components PDF: `stoxx.com/document/Bookmarks/CurrentComponents/SXXP.pdf` [V].
   - FTSE 250 → at least mid; its smallest member was about £294m in Dec 2025 [V].
   - Euronext compartments A/B/C use ≥€1bn / ≥€150m [V, secondary source]. They exist for Paris, Amsterdam, Brussels and Lisbon only, and we have no per-ISIN source yet.
   - Nasdaq Nordic Large/Mid/Small Cap use the same cut-offs, but with buffer rules (a company stays Large down to €500m), so they are not exact [V].
   - SDAX, FTSE SmallCap, AIM, the Italian mid and small indices and the Athens indices say nothing reliable.

5. **Dead ends:**
   - **Wikidata:** a query found only 82 European items with any market cap (P2226), none dated 2025 or later [V].
   - **ESMA FASTER:** market cap data is country totals only, with no ISINs [V].
   - **ESEF XBRL:** has no element for share price or market cap [I]. It does have `NumberOfSharesIssued` / `NumberOfSharesOutstanding`, but these are tagged only where the company chose to [I].

### 2.2 Data risks to handle in code

- **Year-end date:** 31 Dec 2025 was a Wednesday. Xetra, SIX, Borsa Italiana and Oslo were probably closed; LSE and Euronext ran half days [I]. Use the last trading day on or before the fiscal year end, and record that date.
- **GBX:** pence-quoted LSE lines need dividing by 100. Check against the report's per-share figures. Some LSE lines are quoted in USD or EUR. Fix the "USD CENTS" unit the ECB lookup rejects.
- **Adjusted prices:** Wiener Börse is adjusted; with Euronext choose "unadjusted"; with EODHD use `close`.
- **Thinly traded or suspended stocks:** record the last trade date. This is common in Athens and AIM.
- **Several share classes:** Italian savings shares, A/B shares, Swiss bearer and registered shares. Market cap = the sum over classes of shares × that class's price.
- **Home listing only:** use the home MIC from FIRDS, not Frankfurt or Cboe prices.
- **The locator must open without a key:** store the exchange page or file as `endpoint`, never an API URL with a token.

---

## 3. Research: official sources for ownership

| Country (companies) | Source | Machine-readable | Snapshot or stream | Integrate |
|---|---|---|---|---|
| IT (110) | CONSOB "Azionariato": `consob.it/web/area-pubblica/quotate`, per-company pages `/w/azionisti-rilevanti-di-<issuer>-...` [V] | HTML (chart data in URL parameters) [V] | **Snapshot**, top of the ownership chain [V] | 1st |
| DE (137) | BaFin voting-rights database: `portal.mvp.bafin.de/database/AnteileInfo/` [S] | Stable HTML [I]; needs a client that keeps a session | **Current holdings per company** [S] | 2nd |
| BE (64) | FSMA company pages `fsma.be/en/issuer/<slug>`, with LEI and the share denominator; PDF per company `/sites/default/files/issuers/files/<companyNumber>_<lang>.pdf` [V] | PDF at a stable URL | **Snapshot** [S] | 3rd |
| NL (57) | AFM substantial holdings: CSV export `afm.nl/export.aspx?type=1331d46f-3fb6-4a36-b903-9584972675af&format=csv` [V] | **CSV / XML** [V] | Stream; needs netting | 4th |
| CH (191) | SIX Exchange Regulation significant shareholders `ser-ag.com/.../significant-shareholders.html` [V] | JavaScript app; backend not inspected | Notifications since 1998 [V] | 5th |
| ES (61) | CNMV significant holdings | Returned 403 to automated access [V] | Snapshot per company [I] | 6th |
| GB (466) | FCA National Storage Mechanism, "Holding(s) in Company" TR-1s; CSV export of search results [V/S]. For AIM: Companies House CS01 (≥5% holders) [S] | Free-text TR-1s to parse | Stream | 7th (the FCA bulk API is "planned") |
| GR, AT, NO, SE, PT, FI, DK | Announcements by the company or the exchange | PDF/HTML | Stream | Low |

- **UK reports:** UK annual reports must disclose major shareholdings (substantial shareholding notifications). So GB ownership gaps are mostly extraction misses: fix those first.
- **ESEF tag:** "Name of ultimate parent of group" (IAS 24.13) is a mandatory ESEF mark-up [S]. Read it as a second source for `ultimate_parent`.
- **ESAP:** the EU's single access point is collecting data now, but public access is due in **July 2027** [V]. No help for FY2025, and it will never cover GB, CH or NO.
- **GDPR:** every register names private individuals (family owners). Our reuse needs its own lawful basis (legitimate interest with a documented balancing test). Store only the name, % and date.
- **Not verified:** terms of use and robots rules at all 14 sources, BaFin's output, CNMV's page structure, SIX's backend, Finland and Denmark.

---

## 4. The plan

### Phase A: fixes on the data we already have (2–3 days, no new run)

Each item: a rule in code, a test, a note on the value saying how it was obtained, then `combine` and a rebuild of the checks, failures and dashboard.

| # | Change | Where | Fields | Expected effect |
|---|---|---|---|---|
| A1 | GLEIF `NON_CONSOLIDATING` → "none (no consolidating parent)", confidence A, note "GLEIF reporting exception NON_CONSOLIDATING". `NON_PUBLIC` stays blank with that reason. Check the one company that has a parent record but is blank (stale cache?). Never use the code for ownership. | `extractor/apis.py` `gleif_values()`; re-apply over saved rows without re-running | ultimate_parent | 205 → about 20 |
| A2 | Work out the ownership fields from `largest_holders`, as the field list says: highest stake < 20% → controlling_owner "none" and ownership_type "widely_held"; ≥ 20% → that holder becomes the controlling owner, typed by the AI or a name list; pe_stake_5pct "no" when the list includes every holder above the disclosure threshold and none is PE; controlling_owner_name "not applicable" when there is no controlling owner. | `datapoints.py`, after the facts are chosen | controlling_owner, ownership_type, pe_stake_5pct | about 55 companies |
| A3 | benefits_value or pension_contribution = 0 when the role's stated total equals its other parts within 2% (the same tolerance as the existing check XF-02); method DERIVED, note shows the sum | `pay.py` role rows | benefits_value, pension_contribution | about 220 + 320 roles |
| A4 | pay_currency from the currency of any amount of that role, else the company's pay table, else the pay document's currency | `pay.py` | pay_currency | 134 → about 10 |
| A5 | Role scope: put non-executive board entries into the single "Board (non-executive)" row, as the prompt intends. Former members with no pay in the year → "not applicable: no pay for the year". Rows that are only an accounting line of the table are dropped (the existing rule). | `pay.py` role rows | all pay fields | about 100–250 per field leave the not-found count |
| A6 | Fix the market_cap_band derivation: the "USD CENTS" unit, the 10 missing ECB rates, a GBX check, several share classes | `datapoints.py` `market_cap_band()`, `fx.py` | market_cap_band | about 10 |

### Phase B: extraction rules (3–4 days, plus a test re-run of about 50 companies)

| # | Change | Fields |
|---|---|---|
| B1 | Pay prompt and `pay_tables.py`: a dash, "nil", "–" or "0" in a component's cell → 0, quoting the cell. A component combined with another ("pension and social security", Italy's "benefici non monetari") → recorded as "included in X" (STATED_IN_OTHER_FORM), never 0. | benefits_value, pension_contribution |
| B2 | Pay policy prompt: shareholding_requirement = "None" when a remuneration policy or full remuneration report was read and states none (the client's rule). pension_type "no pension" or "cash allowance" when stated. Only when such a document was actually read. | pay policy fields |
| B3 | EBITDA fallback: when the report has no EBITDA, take operating profit (the client's rule), with the note naming the measure. Optionally operating profit + depreciation and amortisation from ESEF tags or the cash flow statement, marked as derived. | ebitda |
| B4 | Shares outstanding from extra sources: ESEF tags `ifrs-full:NumberOfSharesOutstanding` / `NumberOfSharesIssued` minus treasury shares; UK monthly "Total voting rights" announcements (published by the company); the share denominator on major-holding notices (FSMA). | shares_outstanding |
| B5 | Share price and market cap: target each language's year-end close wording ("prezzo ufficiale", "Schlusskurs", "Jahresschlusskurs", "market price at year end", "κεφαλαιοποίηση"). Add a `market_cap_stated` fact, so a market cap the company states gives the band even without a price. | share_price, market_cap_band |
| B6 | An empty answer for pay or financials → one retry with a stronger model (`LLM_FALLBACK_MODEL`, e.g. Gemini Pro); record which model answered (improvement 3.2). | all |
| B7 | UK: make sure the Directors' Remuneration Report section and its single-figure table are always read in full. The GB gaps are extraction misses, not missing documents. | GB pay fields |

### Phase C: new official sources (4–6 days; most items depend on decision D2)

| # | Source | Fields | Notes |
|---|---|---|---|
| C1 | Athens daily closing-price file or Daily Official List for the last 2025 trading day | share_price, market_cap_band | One download for all GR companies; check terms and columns first |
| C2 | SIX closing-price files; Wiener Börse history | share_price | Check for corporate-action adjustment at Vienna |
| C3 | LSE issuer-list archive, December 2025 | market_cap_band (GB) | Check the market cap column exists first |
| C4 | Index membership lists (STOXX 600, FTSE 100/250, DAX) | market_cap_band | Lower bound only; note "at least mid/large" |
| C5 | Paid price API (EODHD, or a Euronext / LSE licence) | share_price | **Only after a written licence.** The endpoint stored is a key-free exchange page |
| C6 | Major-holding registers, in this order: CONSOB → BaFin → FSMA → AFM → SIX SER → FCA National Storage Mechanism → Companies House CS01 (AIM) | ownership fields | Only after the terms check and GDPR decision D5; confidence C at most for off-site values |
| C7 | Remuneration reports: push for read access to the CDP bucket (the service account gets 403). Widen our own search: EU listed companies must publish the remuneration report and policy on their website (Shareholder Rights Directive II, Arts. 9a/9b), so look for the policy, AGM documents and "corporate governance → remuneration" pages. | all pay fields | The biggest single lever: about 580–630 missing values per pay field are REMUNERATION_REPORT_NOT_READ |

### Phase D: re-run and close out (about 3 run days split across 3 people, plus 2 days of review)

*(The steps are numbered 1–4, not D1–D4: D1–D6 are the decisions in section 6.)*

1. **Re-run list:** build it with `python -m extractor.rerun_list`, with a `fields` column of only the missing priority fields. Order:
   1. companies whose values date from v0–v2;
   2. REMUNERATION_REPORT_NOT_READ companies, with remuneration report links;
   3. REPORT_NOT_FOUND and WRONG_YEAR_REPORT companies, with links found by hand;
   4. the rest.
2. **Documents by hand:** find the roughly 18 missing annual reports and the remaining `data/runs_16nov/documents_to_find.csv` companies.
3. **Review queue:** whatever is still blank goes through a review queue (improvement 3.1). Every remaining blank must carry a specific, true reason.
4. **Splice and refresh:** `combine`, then the checks and failures reports, dashboard, spot-check sheet and `docs/improvement_log.md`.

### Guardrails (so the number isn't gamed)

- Every "0", "None", "not applicable", "widely held" and GLEIF rule has a test and a note on the value that shows the rule. It goes live only with the client's sign-off (D1).
- After each phase:
  - accuracy against the golden set must not drop;
  - the share of values passing the checks stays at 93% or higher;
  - no rise in hard fails;
  - spot-check sheet sent to Oggy.
- Off-site values: domain in `source`, "off-site" in `note`, confidence C at most.

---

## 5. Expected results

| Field | Now | After A+B | After C+D | Below 3%? |
|---|---|---|---|---|
| ultimate_parent | 25.2% | about 3% | about 2% | yes |
| largest_holders | 15.2% | about 12% | 2–4% | yes, with C6 and B7 |
| controlling_owner / ownership_type | 15.2% / 15.3% | about 8% | 2–3% | yes |
| controlling_owner_name | 18.6% | about 8% | about 3% | yes |
| pe_stake_5pct | 17.3% | about 10% | 3–4% | borderline |
| revenue | 7.6% | about 5% | about 2% | yes |
| total_assets | 6.1% | about 4% | about 2% | yes |
| ebitda | 11.3% | about 4% | about 2% | yes, once B3 is agreed |
| shares_outstanding | 8.3% | about 6% | about 3% | borderline |
| total_remuneration | 9.1% | about 6% | about 3% | needs C7 |
| base_salary | 13.2% | about 8% | about 3% | needs C7 |
| benefits_value | 32.0% | about 12% | 4–6% | **only with decision D4** |
| pension_contribution | 37.7% | about 15% | 5–7% | **only with decision D4** |
| pay_currency | 4.4% | about 0.5% | about 0.5% | yes |
| pension_type / benefits | 13.3% / 12.8% | about 7% | about 3% | yes |
| shareholding_requirement | 37.4% | about 8% | about 3% | yes, once B2 is agreed |
| share_price | 46.3% | about 38% | **15–20% free, about 3% paid** | **only with decision D2** |
| market_cap_band | 48.8% | about 35% | 10–15% free, about 3% paid | **only with D2** (C3 may close GB) |

These are estimates from the bucket analysis in section 1, not measurements. The 50-company re-run in Phase B checks them before the full re-run.

---

## 6. Decisions

**22 Nov 2026: decided on the client's behalf** (they would most likely decide the same; the "Decided" column), each reversible: a D1 or D4 rule the client rejects goes off with `RULES_OFF=<rule>` in `.env` and a `combine`.

| # | Decided |
|---|---|
| D1 | **All four accepted**, each only where its condition holds (details below). On by default: `gleif_non_consolidating`, `zero_from_total`, `none_if_absent`; operating profit for EBITDA was already in the prompt, and now also from the ESEF tag. |
| D2 | **Free official sources only, no paid licence for now.** The company's own figure first (B5), then exchange files whose terms allow download (Athens, SIX, Wiener Börse: terms to be read before C1/C2). No automated Euronext or LSE downloads (their terms forbid it). LSE Data Shop counts as banned "LSEG". Accept about 15–20% share prices missing; reopen if the client wants the last points. |
| D3 | **market_cap_band is best effort.** The client's own list says "never used", so no paid source for it; it is derived where a price or a stated market cap exists. |
| D4 | **A folded pension or benefit is "not applicable: included in <field>"** (rule `included_in_other`): not 0, not missing, the note names the column it is in. |
| D5 | **Names from the registers allowed**: name, % and date only, from regulators whose terms allow automated reuse (the same names are already in the annual reports we store). CNMV (403 to automated access) left out. |
| D6 | **Not ours to decide**: ask the client for read access to the CDP bucket; meanwhile widen our own remuneration report search (C7). |

The questions as first put:

| # | Question | Who |
|---|---|---|
| D1 | Are these acceptable values: "none (no consolidating parent)" from GLEIF `NON_CONSOLIDATING`; pension or benefits = 0 worked out from total = other parts; operating profit in place of EBITDA; "None" for no shareholding requirement? | Client |
| D2 | Share prices: may we buy a commercial licence (EODHD commercial, Euronext market data, LSE Data Shop), or stay with free sources only and accept about 15–20% missing? Does the LSE Data Shop count as banned "LSEG"? Are the Athens, SIX and Wiener Börse download terms acceptable? | Client / legal |
| D3 | Is market_cap_band really priority 1? The client's field list marks it "never used". | Client |
| D4 | How should a pension or benefit that is combined with another item (Italy, Switzerland) count? It is neither 0 nor missing. Proposal: STATED_IN_OTHER_FORM, shown separately and not counted as not found. | Client |
| D5 | May we store private individuals' names from the major-holding registers (GDPR)? Are the regulators' terms acceptable for automated reuse? | Legal / data governance |
| D6 | Read access to the CDP bucket for the service account in `.env` (currently 403). The pay targets depend on it. | Client |

### D1 in detail: four values that fill a blank the source doesn't print

Each of these turns "not found" into an answer, so each moves the dashboard a lot. But each is our reading of a rule or a register code, not a figure we can quote. If the client later disagreed, the values would count as wrong, which is worse than blank. So none goes live before the client agrees (see "Guardrails" in section 4).

| # | Value | Why it needs agreement | Effect on missing | Status |
|---|---|---|---|---|
| 1 | `ultimate_parent` = "none (no consolidating parent)" when GLEIF gives the reporting exception `NON_CONSOLIDATING` (no parent includes the company in its consolidated accounts; about 182 of the 205 blanks) | "No company consolidates it" is close to "no parent", but not the same: a PE fund, a foundation or the state can control a company without consolidating it. So it fills `ultimate_parent` only, never `controlling_owner` or `ownership_type`. | ultimate_parent 25.2% → 2.7% (measured) | A1, built, off until signed off (`gleif_non_consolidating`) |
| 2 | benefits_value or pension_contribution = 0 when the role's stated total equals its other amounts (a CEO's total 800,000 = base + bonus + LTI 800,000), within 0.5% | The field list says "record 0, not blank" for benefits, but a 0 we work out is not a 0 the report prints. The note shows the sum: "derived: 0, the stated total 800,000 = …". It never fires where a pension is folded into another column (that is D4): the total would not equal the other parts. | benefits_value 32.0% → 19.2%, pension_contribution 37.7% → 19.4% (measured) | A3, built, off until signed off (`zero_from_total`) |
| 3 | `ebitda` = operating profit when the report has no EBITDA, the note naming the measure | The field list says "EBITDA, else operating profit", but the two differ by depreciation and amortisation. The client should confirm they want operating profit under `ebitda` rather than a blank. | ebitda 11.3% → about 4% (estimate) | B3, not built |
| 4 | `shareholding_requirement` = "None" when no requirement is stated | The field list says "record 'None' if absent"; our prompt says null. "None" is true only when a remuneration policy or full remuneration report was actually read and states none, so the rule would apply only then. | shareholding_requirement 37.4% → about 8% (estimate) | B2, not built |

Decided 22 Nov (above): items 1, 2 and 4 are rules on saved rows, on by default; item 3 is in the prompt and the ESEF tag fill.

---

## 7. Effort and order

| Phase | Effort | Depends on |
|---|---|---|
| A: fixes on existing data | 2–3 days | D1 (A1, A3) |
| B: extraction rules plus a 50-company test | 3–4 days | D1 (B2, B3), D4 (B1) |
| C: new sources | 4–6 days | D2, D5, D6 |
| D: re-run and close out | about 3 run days (split 3 ways) plus 2 review days | A–C |

About 3 weeks for one person, including run time, or about 1.5 weeks with the runs split three ways.

Phase A can start at once for everything except the rules that need sign-off. Send D1–D6 to the client on day 1, so the answers arrive before Phase C.
