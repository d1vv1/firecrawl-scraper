# Plan: finding and reading company documents without Firecrawl cloud

*22 October 2026 · firecrawl-scraper*

## Goal

Replace most Firecrawl cloud calls with our own code and cheaper services, while finding as many annual reports and fallback documents as we do today. Keep Firecrawl cloud only for the companies where our own route fails, if the measurement shows it is still needed.

## What we use Firecrawl for today

| Call | Used for | Credits | Where |
|---|---|---|---|
| `search` | Finding the company's website when Wikidata has none | 2 per 10 results | `website.py` |
| `map` (with a search term) | Listing a site's URLs to find the annual report, then the fallback documents | 1 per call | `report_finder.py`, `documents.py` |
| `scrape` | Reading the investor-relations (IR) page for report links; HTML reports; fallback web pages | 1 per page | `report_finder.py`, `scraper.py`, `documents.py` |

PDFs, which are 154 of the 157 reports found on company websites, are already downloaded and converted by our own code. So only finding URLs and reading HTML pages depend on Firecrawl.

All calls go through `firecrawl_client.py`, and the rest of the code only sees lists of URLs and markdown. A replacement can sit behind the same three methods without touching the report finder or the document fallback.

## Why Firecrawl cloud finds so many documents

Firecrawl documents its map endpoint as: URLs are "primarily discovered from the website's sitemap", "supplemented with SERP (search engine) results and previously crawled pages to improve coverage" ([docs](https://docs.firecrawl.dev/features/map)). Each part matters for us in a different way.

**1. The sitemap is almost no help for reports.** We checked, for free, the 157 companies whose annual report came from their website (not from a filing). For each we read the sitemaps listed in `robots.txt` (or `/sitemap.xml`) and compared them with the report Firecrawl found:

| Measure | Result |
|---|---|
| Site has a readable sitemap | 125 / 157 (80%) |
| Sitemap lists any PDF at all | 4 / 157 (3%) |
| **Sitemap lists the report we used** | **2 / 157 (1%)** |
| Report found by map (rest: IR-page scrape or follow-up links) | 93 / 157 (59%) |
| Report hosted off the company's own domain (storage.mfn.se, q4cdn.com, Azure/CDN hosts…) | 29 / 157 (18%) |

Sitemaps list HTML pages (a median of 780 URLs per site), not the PDFs linked from them. So nearly every report map found came from the other two sources, not the sitemap.

**2. Previously crawled pages: a shared crawl cache.** Firecrawl's index holds the URLs its crawlers have already seen on these sites. That includes PDFs linked from IR pages and PDFs on document hosts the company links to. We cannot copy this: every URL in it would have to be found by crawling the sites ourselves.

**3. Search-engine results.** A search engine's index knows PDFs on any host, including off-site document hosts that no company sitemap will ever list. This we *can* get, through a search API (see the plan), but per query and with about 10–20 results per query instead of a ranked list of up to 500 URLs.

**4. The `search` term ranks a large URL list.** `map(site, search="annual report")` returns the most relevant URLs first, so the right PDF makes the top 500 even on sites with 100,000 pages. Without it we need the full URL list and our own ranking. We already have that ranking (`report_finder.classify`, `documents.classify`), so this part is the easiest to replace.

**5. Fire-engine gets past bot blocking.** Firecrawl's proxies and browser fingerprints fetch pages and sitemaps that refuse plain requests. In our sitemap check, 10 sites answered our plain requests with 403 or similar refusals. Self-hosted Firecrawl does not include Fire-engine ([docs](https://docs.firecrawl.dev/contributing/self-host)).

**6. Rendering scripts.** Many IR pages build their report list with JavaScript (MFN, Cision and Q4 widgets). A plain HTTP fetch sees an empty list; Firecrawl renders the page in a browser first.

## Why we expect fewer results without it

| Firecrawl cloud has | Our replacement | Expected gap |
|---|---|---|
| Shared crawl cache | Our own crawl of the IR section | **The biggest loss.** We only find what we reach by following links from pages we can fetch. Reports linked only from deep, old or script-built pages will be missed. |
| Search-engine results | Search API with `site:` queries | Small to medium. Fewer results per query; each query costs money; queries must be precise. |
| Ranking by `search` term | Our own classifiers over the full URL list | None expected. |
| Fire-engine (anti-bot) | httpx → curl_cffi → Playwright from our own IP | Medium on protected sites: some IR pages and sitemaps will refuse us, and our IP can be rate-limited or blocked. |
| Browser rendering | Playwright, only for pages that need it | Small, but Playwright is slow and heavy. |

Self-hosted Firecrawl does not close these gaps: it has neither the shared cache nor Fire-engine, so its map is roughly a sitemap plus its own crawl. It is in the measurement below as a third option, not as the main plan.

**Expected result:** our own route should find most reports on cooperative sites, because 82% of reports are on the company's own domain and are usually linked from an IR page we can reach. We expect losses on protected sites, script-built report lists and off-site hosts. The measurement in Phase 3 replaces this guess with numbers.

## What needs to be built

1. **A discovery backend behind `firecrawl_client.py`** with the same three methods (`search`, `map`, `scrape`). It is switchable by setting: `firecrawl` (today), `own`, or `own+firecrawl` (own first, Firecrawl cloud only when our route fails).
2. **Website finding:** Wikidata first (exists), then a search API instead of Firecrawl search.
3. **URL listing (replaces `map`), cheapest first:**
   1. **Sitemaps:** `robots.txt`, sitemap indexes, gzip files (free). This gives the HTML pages, including the IR pages.
   2. **Short crawl of the IR section:** pick the IR, report, governance and shareholder pages from the sitemap and the home page's menu using the keyword lists we already have (`_IR_PAGE_HINTS`, `DOC_TYPES`). Fetch them and collect every link, PDFs included. Two levels deep, at most about 25 pages per company, cached.
   3. **Search-API queries** when the crawl finds no candidate: `site:<domain> annual report 2025 filetype:pdf`, the native term (`årsredovisning`, `vuosikertomus`…), and the document types the fallback needs (`remuneration report`, `shareholders`…). Also `"<company name>" annual report` restricted to the known document hosts (storage.mfn.se, mb.cision.com, q4cdn.com…).
   4. **Rendering** with Playwright only for pages that load a known report widget or have suspiciously few links.
   5. No `search` ranking is needed: we return the whole list, and our classifiers rank it.
4. **Page reading (replaces `scrape`):** httpx, then curl_cffi (browser TLS fingerprint), then Playwright. HTML is turned into markdown with links kept (trafilatura or markdownify), in the same page-tagged format the cache uses today.
5. **Fallback for hard cases** (`own+firecrawl` mode): Firecrawl cloud is called only when our route found no report, found only a stale one, or was blocked. The per-company credit caps stay.
6. **Good behaviour:** obey `robots.txt`, at most about 1 request per second per site, cache everything, and stop early once the report is found.

## Phases

| Phase | Scope | Effort |
|---|---|---|
| **0. Decide** | See "Decisions needed" below. | — |
| **1. Own route, basics** | Backend switch; sitemaps; short IR crawl; httpx/curl_cffi reading with HTML → markdown. | ~2 days |
| **2. Own route, the hard parts** | Search-API queries; document-host queries; Playwright rendering for script-built pages; `own+firecrawl` fallback mode. | ~1–1½ days |
| **3. Measure** | Run the 196-company golden sample three ways: Firecrawl cloud (the reference; results already cached), our own route, and our own route with cloud fallback. Self-hosted Firecrawl can be a fourth run if Docker capacity is available. | ~1 day + run time |
| **4. Choose** | Pick the mode per the success criteria below; remove what is not used. | ~½ day |

## How we measure

For each run, per company:

- **Report found:** the same report as Firecrawl cloud, or another report for the same fiscal year. A report for an older year counts as a loss.
- **Fallback documents read** and **data points filled** by the document fallback.
- **Accuracy** against the golden dataset, per data point, so that a route that finds *different* documents is not wrongly counted as worse.
- **Why it failed:** no URL found, page blocked, script-built page, off-site host.
- **Cost and time:** Firecrawl credits, search-API queries, minutes per company.

**Success criteria (proposed):**

| Mode | Keep it if |
|---|---|
| Own route only | It finds a same-year report for at least 90% of the companies Firecrawl cloud found one for, with no loss of accuracy. |
| Own route + cloud fallback | It matches Firecrawl cloud on at least 98% of companies and uses at least 70% fewer credits. |
| Firecrawl cloud only | Neither of the above holds. |

## Cost

- **Firecrawl:** today up to 6 credits per company for the report search and 10 for the document fallback. In `own+firecrawl` mode, credits are spent only for the companies where our route fails.
- **Search API:** a few queries per company where the crawl finds nothing. Prices and terms (especially rules on storing results) must be checked before choosing a provider.
- **Our side:** Playwright needs a machine with several GB of free memory. Runs will be slower than Firecrawl, because we crawl politely instead of reading a ready index.

## Risks

| Risk | What can go wrong | Guard |
|---|---|---|
| Blocking | IR sites behind Cloudflare or Akamai refuse our requests; with several workers, our IP gets rate-limited or blocked for a while. | Per-site rate limit, caching, cloud fallback for blocked sites. |
| Missed reports | Reports linked only from pages our crawl doesn't reach. | Search-API queries; cloud fallback; measured in Phase 3. |
| Crawling terms | Our own crawler now carries the responsibility for robots.txt and site terms that Firecrawl's terms cover today. | Obey robots.txt; legal or data governance confirms the user-agent policy (see decisions). |
| Upkeep | Sites, widgets and bot protection change; we maintain the crawler instead of Firecrawl. | Failure reasons are logged per company, so breakage shows up in each run. |

## Decisions needed

1. **Search API provider:** Brave, Serper, or another, given price and terms of storing results.
2. **Fallback:** keep Firecrawl cloud for hard cases (`own+firecrawl`), or drop it completely if the measurement allows?
3. **User agent:** keep the current browser user agent, or identify the tool honestly (e.g. with a contact address), knowing that some sites block non-browser agents?
4. **Self-hosted Firecrawl:** include it as a fourth run in Phase 3, or skip it?

## How the sitemap numbers were measured

The numbers come from the cached results in `output/`: the 157 companies whose report URL came from their website. Sitemaps were fetched with plain HTTP (up to 80 sitemap files per site), and URLs were compared on host and path. The check is simple, so treat the numbers as indicative. A sitemap may list the report's HTML page rather than the PDF, and some refusals (403, 404) may be bot blocking rather than a missing sitemap.
