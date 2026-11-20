# Plan: a document fallback for missing data points

*21 October 2026 · firecrawl-scraper (`python -m extractor.datapoints`)*

## Goal

Fill the data points that are still empty after the annual report has been read, by finding and reading **other documents in any format** that are likely to hold them. This replaces the official-API step (GLEIF, SEC EDGAR, Brønnøysund, PRH, Companies House) in this tool, since that data is collected upstream.

## Where we are

Today, for each company, the tool:

1. finds **one** annual-report document (ESEF filing, SEC filing, register filing, or the report on the company's website);
2. looks up official APIs (to be removed from this tool);
3. has the AI read the annual report for the remaining data points, with a quote for every value and the page it was found on;
4. as a backup, reads **at most 3 web pages** of the company's site, chosen only by their URLs.

The weakest data points, measured on the first 157 companies of the golden sample (only counting data points that apply to each company):

| Data point | Found | Where it is usually published |
|---|---|---|
| shareholding_requirement | 13% | remuneration report, remuneration policy, AGM notice |
| isin | 21% | investor "The share" page, share section of the annual report |
| controlling_owner_name | 22% | "Largest shareholders" page; corporate-governance report (Swedish companies must name holders of 10% or more); major-holding notices |
| revenue_by_country | 26% | segment / geographic note; year-end report |
| fte | 27% | sustainability report (GRI 2-7 employee tables); staff note |
| listing_date | 28% | IPO press release, listing notice, "The share" page |
| exchange_segment | 29% | "The share" page, annual report |
| staff_by_country | 29% | sustainability report |
| pension_type | 38% | remuneration report |

**Why they are missing:** to find *the* annual report, the report finder deliberately drops remuneration, corporate-governance and sustainability reports, interim and year-end reports, and presentations. Those are exactly the documents that hold these data points. For example, Yubico's remuneration report was among the 1,861 URLs found on its site, and was dropped.

**Fields that come from APIs today** can mostly be found in documents too:

| Data point | Document source |
|---|---|
| legal_name, legal_form, country_code, head_office_city | IFRS reporters must state their registered office, legal form and domicile in the notes (IAS 1); report cover; website legal notice |
| business_id | Swedish reports print the registration number; German, Austrian and Swiss websites must have a legal notice (*Impressum*) with the register number and seat |
| cik | the company's CIK is part of every SEC filing's web address |
| other_names | "formerly …" in the report or the company history page |
| ultimate_parent | subsidiaries' reports name their parent |
| lei, sector_code | rarely printed in company documents: left to the upstream API work |

## What needs to be built

1. **Gap list per company:** the data points still empty after the annual report has been read.
2. **Data point → document type map**, each document type with search words in about 10 languages. For example, `pension_type` → remuneration report, then remuneration policy, then AGM notice. This extends the report finder's keyword lists, which today only know "annual report".
3. **Discovery, cheapest first:**
   1. re-sort the site URL lists the report search already fetched (cached; free);
   2. targeted Firecrawl map searches per document type ("remuneration report", "largest shareholders"…), 1 credit each;
   3. follow links on pages already scraped;
   4. (Phase 3 only) allowlisted off-site sources, see below.
4. **Classifier and ranking per document type**, reusing the report finder's logic: keyword match, year (prefer the annual report's year), language, and a do-not-scrape list enforced in code.
5. **Readers for any format:**

   | Format | Status |
   |---|---|
   | PDF, HTML | exists |
   | iXBRL / XBRL | exists |
   | Excel / CSV (key-figures downloads) | new: read as tables |
   | Word (AGM notices) | new |
   | Scanned PDF | needs OCR; Firecrawl can do it but charges per page; optional |

6. **One document store per company, with an exact location per format** (today the code assumes one document per company):

   | Format | `endpoint` / `note` location |
   |---|---|
   | PDF | `…pdf#page=N` |
   | HTML | `…#:~:text=<quote>` |
   | Excel | file URL; note gives sheet and cell, e.g. `'Key figures'!C14` |
   | Word | file URL; note gives the paragraph number |
   | XBRL | filing URL; note gives the tag |

7. **Targeted AI questions:** send only the parts of each document relevant to the missing data points, and ask only for those. The quote rule, the page lookup and the A/B/C confidence grades stay as they are.
8. **Freshness and conflicts:** every value carries its document's date ("shareholders as of 30 September 2026"); prefer the annual report's fiscal year; the more exact source wins and a disagreeing value goes in `note`, as today.
9. **Budget and stopping:** a per-company credit cap; stop as soon as the gaps are filled; try document types in order of expected yield.

The output format does not change: `output/datapoints.csv`, same 15 columns, one row per company and data point.

## Phases

| Phase | Scope | Effort |
|---|---|---|
| **0. Decide** | See "Decisions needed" below. | — |
| **1. The company's own documents** | Remove the API step; gap list; data point → document type map; re-sort cached URL lists; targeted map searches; classifier per document type; PDF/HTML fetching; multi-document store; targeted AI questions. Covers remuneration, governance and sustainability reports, "The share" and "Largest shareholders" pages, the legal notice and the year-end report. **The biggest gain.** | ~2 days |
| **2. More formats and filed documents** | Excel/CSV/Word readers; documents filed at the registers (Danish virk.dk PDFs, Norwegian accounts, UK accounts once a working Companies House key is in place). | ~1 day |
| **3. Allowlisted off-site sources** | Only if data points are still weak after Phase 2, mainly ownership of private companies. See the risks section. | ~1 day |
| **4. Measure** | Re-run the 196 companies; fill rate and accuracy against the golden dataset per data point, before and after; tune the document-type order. | ~½ day + run time |

**Cost:**
- **Firecrawl, Phase 1:** about 4–8 credits per company where the site's URL list is already cached, more where it isn't. Roughly 1,000–1,500 credits for the 196-company sample.
- **AI:** one extra call per group of documents (Gemini Flash), which costs little at this size.

## Off-site sources: risks and guards

| Risk | What can go wrong |
|---|---|
| **Display rights and licensing** (the biggest) | Values scraped from third-party sites may not count as self-collected, which is the point of this build. Aggregators, exchange sites and financial portals often forbid automated collection or reuse, and in the EU a collection of data can be protected as a database in its own right. The source review already bans Yahoo, Börsdata, LSEG, Infront and LinkedIn, and holds the Nasdaq Nordic website and Allabolag.se until their terms are checked. An open web search would land on exactly these. |
| **Personal data (GDPR)** | Ownership searches turn up individuals: family owners, board members' holdings, people-search sites. Storing a private person's name and stake needs a legal basis. |
| **Wrong company** | Off the company's own site there is no LEI or domain to tie a page to the company. Same-name companies, parents, subsidiaries and former names get mixed up, most of all for the private companies that need off-site sources most. |
| **Second-hand and stale data** | News rounds figures; aggregators copy each other, sometimes from licensed sources. Pages may be years old. The quote check still passes: it proves the page says it, not that it is true. |
| **Manipulated content** | Any page can contain text aimed at the AI or plain false claims. Structured output and the quote rule limit this but don't rule it out. |
| **Operational** | Bot blocking, robots.txt, pages changing, extra credits for searches that find nothing. |

**Guards:**

- **Allowlist of primary sources only**, no open web search:

  | Allowed source | Why | Check first |
  |---|---|---|
  | The owner's own publications: PE fund portfolio pages, the parent's annual report | first-hand statements by the owner | each site's terms and robots.txt |
  | Regulators' major-holding notices: Finansinspektionen Börsinformation, Oslo Børs NewsWeb, Danish FSA | official, dated, legally required disclosures | terms of reuse (unverified in the source review) |
  | Documents filed at registers | official copies | — |

- **Never**: aggregators, news, social media, people-search sites, or anything on the do-not-scrape list (enforced in code).
- **Identity check** before a page is used: company name and country, plus registration number, LEI or website where available.
- **Grading**: off-site values get confidence **C** at most, with the domain in `source` and "off-site" in `note`.
- **Ownership**: store the owner's category (family, private equity…); store an individual's name only if legal agrees.
- **Dates**: every value carries its page's date; older pages lose to newer ones.

**Recommendation:** build Phase 1 first. It closes most of the gaps with none of these risks. Add Phase 3 only for what is still weak, and only after legal or data governance has confirmed the allowlist's terms.

## Decisions needed

1. **API step:** remove it completely, or keep it only as a silent cross-check (not in the output)?
2. **Off-site sources:** company-owned documents only, or allow the allowlisted sources in Phase 3?
3. **Credits:** what Firecrawl budget per company is acceptable?
4. **Companies House:** the current `COMPANIES_HOUSE_API_KEY` is refused (HTTP 401, likely a test-environment key). It needs a live key if UK filed accounts are wanted in Phase 2.
