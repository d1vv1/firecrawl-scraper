"""The fixed pipeline: steps 1-7 as plain function calls."""

import datetime as dt
import json
import logging
from dataclasses import asdict
from urllib.parse import urlparse

import httpx

from . import llm
from .config import CACHE_DIR, OUTPUT_DIR, clean_name, load_settings, slugify
from .extract import extract, iso_period_end, money_with_full_value
from .firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from .report_finder import ReportNotFoundError, find_report, reports_linked_from
from . import edgar, registries
from .edgar import EdgarFiling
from .registries import RegistryFiling
from .esef import EsefFiling, download_report, is_recent, latest_annual_filing
from .scraper import (DownloadError, NeedsOCRError, ReportDocument, TeaserPageError, cache_stem,
                      pdf_to_pages,
                      check_not_scanned, fetch_report, markdown_to_pages, pages_to_markdown)
from .xhtml_text import html_to_text, text_to_pages
from .sections import select_chunks, split_chunks
from .validate import (ENTITY_FRONT_PAGES, Check, check_entity, checks_as_dicts, overall_status,
                       run_checks, warnings_for)
from .lei import fetch_by_lei, find_lei
from .website import WebsiteNotFoundError, find_website, registered_domain
from .wikidata import website_for_lei, website_for_name

log = logging.getLogger(__name__)


def _discovery_path(slug: str):
    return CACHE_DIR / f"{slug}_discovery.json"


def identify_lei(legal_name: str, slug: str, lei: str | None, use_cache: bool,
                 country: str | None = None) -> dict:
    """Step 1b: legal name -> LEI via GLEIF (or fetch the --lei given). Cached."""
    path = CACHE_DIR / f"{slug}_lei.json"
    if use_cache and path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        # Misses aren't reused: GLEIF is free, and matching rules improve over time.
        if cached.get("record") and (lei is None or cached["record"]["lei"] == lei.upper()):
            log.info("Using cached LEI lookup %s", path.name)
            return cached

    try:
        if lei:
            record = fetch_by_lei(lei)
            info = {"record": record.as_dict() if record else None,
                    "reason": "override (--lei)" if record else f"--lei {lei} not found in GLEIF",
                    "candidates": []}
        else:
            log.info("Step 1b: looking up the LEI in GLEIF")
            res = find_lei(legal_name, country)
            info = {"record": res.record.as_dict() if res.record else None,
                    "reason": res.reason, "candidates": res.candidates}
    except httpx.HTTPError as e:
        # GLEIF being down shouldn't stop the run: continue without an LEI, don't cache.
        log.warning("GLEIF lookup failed (%s); continuing without LEI", e)
        return {"record": None, "reason": f"GLEIF error: {e}", "candidates": []}

    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(info, indent=2), encoding="utf-8")
    return info


def find_official_website(legal_name: str, fc: FirecrawlClient, lei_record: dict | None,
                          country: str | None = None) -> dict:
    """Step 2, cheapest first:
    1. LEI -> Wikidata website (free);
    2. Wikidata name search: same name + same country + a website (free; catches
       small caps whose Wikidata item has no LEI);
    3. Firecrawl web search (2 credits), scored with the company's country."""
    listing_country = country
    country = (lei_record or {}).get("country") or country
    if lei_record:
        log.info("Step 2: looking up the website for LEI %s in Wikidata", lei_record["lei"])
        site, reason = website_for_lei(lei_record["lei"], clean_name(legal_name), country)
        if site:
            return {"website": site, "website_score": None, "website_source": "wikidata",
                    "website_detail": reason}
        log.info("Wikidata gave no website for the LEI (%s)", reason)

    for c in dict.fromkeys(x for x in (listing_country, country) if x):
        site, reason = website_for_name(clean_name(legal_name), c)
        if site:
            return {"website": site, "website_score": None, "website_source": "wikidata-name",
                    "website_detail": reason}
        log.info("Wikidata name search (%s): %s", c, reason)

    log.info("Step 2: searching for the official website%s",
             f" (country {country})" if country else "")
    w = find_website(legal_name, fc, country=country)
    log.info("Website: %s (score %.2f)", w.url, w.score)
    return {"website": w.url, "website_score": w.score,
            "website_source": "search+lei" if lei_record else "search",
            "website_candidates": w.candidates}


def discover(legal_name: str, slug: str, fc: FirecrawlClient, website: str | None,
             report_url: str | None, use_cache: bool, lei_record: dict | None = None,
             country: str | None = None) -> dict:
    """Steps 2-3, with overrides and a small JSON cache so re-runs cost nothing."""
    if report_url:
        site = website or f"{urlparse(report_url).scheme}://{urlparse(report_url).netloc}"
        return {"website": site, "website_score": None, "website_source": "override"
                if website else "derived from --report-url",
                "report_url": report_url, "report_source": "override"}

    path = _discovery_path(slug)
    if use_cache and path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if website is None or cached.get("website") == website:
            log.info("Using cached discovery %s", path.name)
            return cached | {"from_cache": True}

    if website:
        site_info = {"website": website, "website_score": None, "website_source": "override"}
    else:
        site_info = find_official_website(legal_name, fc, lei_record, country)

    report_country = (lei_record or {}).get("country") or country
    log.info("Step 3: looking for the latest annual report on %s", site_info["website"])
    try:
        r = find_report(site_info["website"], fc, country=report_country,
                        company_name=legal_name, other_countries=[country])
    except ReportNotFoundError as first_error:
        # Wikidata's "official website" is sometimes the consumer site (H&M -> www2.hm.com,
        # while reports live on hmgroup.com). Search for the investor site and try once more.
        if not site_info["website_source"].startswith("wikidata"):
            raise
        log.info("No report on the Wikidata site; searching for the investor-relations site")
        try:
            w = find_website(legal_name, fc, country=report_country)
        except (WebsiteNotFoundError, CreditBudgetExceeded):
            raise first_error from None
        if registered_domain(urlparse(w.url).netloc) == registered_domain(
                urlparse(site_info["website"]).netloc):
            raise
        log.info("Trying %s (score %.2f) instead", w.url, w.score)
        site_info = {"website": w.url, "website_score": w.score,
                     "website_source": "search (wikidata site had no report)",
                     "website_detail": f"wikidata site {site_info['website']} had no report",
                     "website_candidates": w.candidates}
        r = find_report(w.url, fc, country=report_country,
                        company_name=legal_name, other_countries=[country])
    log.info("Report: %s (year %s, pdf=%s)", r.url, r.year, r.is_pdf)
    result = site_info | {"report_url": r.url, "report_year": r.year, "report_source": "map",
                          "report_alternatives": r.alternatives,
                          "report_candidates": [asdict(c) for c in r.candidates]}
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def _fetch_first_usable(urls: list[str], slug: str, fc: FirecrawlClient, use_cache: bool):
    """The chosen file is sometimes unusable: a blank placeholder PDF (ABB's 2025 link
    was a 19 KB empty page), a blocked download, a short teaser page. Then try the next
    best candidates step 3 already found (no extra Firecrawl calls for PDFs)."""
    for i, url in enumerate(urls):
        try:
            return fetch_report(url, slug, fc, use_cache=use_cache)
        except TeaserPageError as e:
            # "Annual report 2025 now available": the page links the PDF; follow it.
            for link in reports_linked_from(e.markdown, url)[:2]:
                log.info("Report %s is a teaser page; following its link %s", url, link)
                try:
                    return fetch_report(link, slug, fc, use_cache=use_cache)
                except (NeedsOCRError, DownloadError) as e2:
                    log.warning("Linked report %s unusable (%s)", link, str(e2)[:120])
            if i == len(urls) - 1:
                raise
            log.warning("Report %s unusable (%s); trying the next candidate %s",
                        url, str(e)[:120], urls[i + 1])
        except (NeedsOCRError, DownloadError) as e:
            if i == len(urls) - 1:
                raise
            log.warning("Report %s unusable (%s); trying the next candidate %s",
                        url, str(e)[:120], urls[i + 1])


def get_esef(lei: str, slug: str, use_cache: bool) -> EsefFiling | None:
    """The latest annual ESEF filing for this LEI (cached; a "none" answer is reused
    for a week, since the index keeps growing)."""
    path = CACHE_DIR / f"{slug}_esef.json"
    if use_cache and path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("filing"):
            return EsefFiling.from_dict(cached["filing"])
        checked = dt.datetime.fromisoformat(cached.get("checked_at", "2000-01-01T00:00:00+00:00"))
        if dt.datetime.now(dt.timezone.utc) - checked < dt.timedelta(days=7):
            return None
    try:
        filing = latest_annual_filing(lei)
    except httpx.HTTPError as e:
        log.warning("ESEF lookup failed (%s); using the website route", str(e)[:120])
        return None
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"filing": filing.as_dict() if filing else None,
                                "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()},
                               indent=2), encoding="utf-8")
    return filing


def esef_document(filing: EsefFiling, slug: str, use_cache: bool) -> ReportDocument:
    """The filing's full report (.xhtml) as page-like text, cached like a PDF's."""
    md_path = CACHE_DIR / f"{cache_stem(slug, filing.report_url)}.md"
    if use_cache and md_path.exists():
        pages = markdown_to_pages(md_path.read_text(encoding="utf-8"))
        return ReportDocument(filing.report_url,
                              "registry" if isinstance(filing, RegistryFiling) else "xhtml",
                              pages, md_path, None, True)
    if isinstance(filing, RegistryFiling):
        kind, content = registries.download_text(filing)
        log.info("Using the registry's %s as the text source",
                 "company profile" if kind == "text" else f"filed report ({kind})")
        CACHE_DIR.mkdir(exist_ok=True)
        if kind == "pdf":
            pdf_path = CACHE_DIR / f"{cache_stem(slug, filing.report_url)}.pdf"
            pdf_path.write_bytes(content)
            pages = pdf_to_pages(pdf_path)
            check_not_scanned(pages)
        elif kind == "html":
            pages = text_to_pages(html_to_text(content))
            check_not_scanned(pages)
        else:                       # a short profile: the "scanned PDF" test doesn't apply
            pages = text_to_pages(content)
        md_path.write_text(pages_to_markdown(pages), encoding="utf-8")
        return ReportDocument(filing.report_url, "registry", pages, md_path, None, False)
    log.info("Downloading the filed report %s", filing.report_url)
    html = (edgar.download_report(filing) if isinstance(filing, EdgarFiling)
            else download_report(filing))
    pages = text_to_pages(html_to_text(html))
    check_not_scanned(pages)
    CACHE_DIR.mkdir(exist_ok=True)
    md_path.write_text(pages_to_markdown(pages), encoding="utf-8")
    return ReportDocument(filing.report_url, "xhtml", pages, md_path, None, False)


def get_edgar(legal_name: str, slug: str, use_cache: bool) -> EdgarFiling | None:
    """The company's latest annual SEC filing (10-K / 20-F / 40-F), if it is an SEC
    registrant. Cached; a "none" answer is reused for a week."""
    path = CACHE_DIR / f"{slug}_edgar.json"
    if use_cache and path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("filing"):
            return EdgarFiling.from_dict(cached["filing"])
        checked = dt.datetime.fromisoformat(cached.get("checked_at", "2000-01-01T00:00:00+00:00"))
        if dt.datetime.now(dt.timezone.utc) - checked < dt.timedelta(days=7):
            return None
    try:
        filing, reason = edgar.find_filing(legal_name)
    except edgar.SecContactMissing as e:
        log.warning("%s; skipping the SEC route", e)
        return None
    except (httpx.HTTPError, ValueError) as e:
        log.warning("SEC lookup failed (%s); skipping the SEC route", str(e)[:120])
        return None
    log.info("SEC: %s", reason)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"filing": filing.as_dict() if filing else None, "reason": reason,
                                "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()},
                               indent=2), encoding="utf-8")
    return filing


def get_registry(legal_name: str, slug: str, lei_record: dict | None, country: str | None,
                 use_cache: bool) -> RegistryFiling | None:
    """The latest accounts filed in the company's home registry (Norway, Denmark), if
    open. Cached; a "none" answer is reused for a week."""
    home = (lei_record or {}).get("country") or country
    if not registries.available(home):       # no open registry, or no UK API key yet
        return None
    path = CACHE_DIR / f"{slug}_registry.json"
    if use_cache and path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("filing"):
            return RegistryFiling.from_dict(cached["filing"])
        checked = dt.datetime.fromisoformat(cached.get("checked_at", "2000-01-01T00:00:00+00:00"))
        if dt.datetime.now(dt.timezone.utc) - checked < dt.timedelta(days=7):
            return None
    try:
        filing, reason = registries.find_filing(legal_name, country, lei_record)
    except (httpx.HTTPError, ValueError, registries.RegistryUnavailable) as e:
        log.warning("Registry lookup failed (%s); skipping the registry route", str(e)[:120])
        return None
    log.info("Registry: %s", reason)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"filing": filing.as_dict() if filing else None, "reason": reason,
                                "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()},
                               indent=2), encoding="utf-8")
    return filing


def _esef_doc_or_none(filing, slug: str, use_cache: bool) -> ReportDocument | None:
    try:
        doc = esef_document(filing, slug, use_cache)
        log.info("Using the ESEF filing %s (FY%s)", filing.filing_id, filing.fiscal_year)
        return doc
    except (httpx.HTTPError, NeedsOCRError) as e:
        log.warning("ESEF report text unusable (%s)", str(e)[:120])
        return None


def _identifier(filing) -> str:
    """How the filing was tied to the company: LEI, SEC CIK or registration number."""
    if isinstance(filing, RegistryFiling):
        return filing.identifier
    if isinstance(filing, EdgarFiling):
        return f"SEC CIK {filing.cik}"
    return f"LEI {filing.lei}"


def run(legal_name: str, website: str | None = None, report_url: str | None = None,
        use_cache: bool = True, lei: str | None = None, company_id: str | None = None,
        country: str | None = None, fc: FirecrawlClient | None = None,
        qualitative: bool = True) -> dict:
    """One company, steps 1-7. `qualitative=False` skips the revenue-model and
    business-structure LLM call (the data-point collector doesn't use them). `company_id` (if given) names the cache/output files;
    `country` (ISO alpha-2) helps the LEI search and is the fallback country when no
    LEI is found. Pass `fc` to read its credit meter even if the run fails."""
    # Step 1
    slug = slugify(company_id) if company_id else slugify(legal_name)
    clean = clean_name(legal_name)
    country = country.strip().upper() if country else None
    log.info("Step 1: %r -> clean name %r, slug %r, country %s", legal_name, clean, slug, country)
    fc = fc or FirecrawlClient(load_settings())
    lei_info = identify_lei(legal_name, slug, lei, use_cache, country)

    # Steps 2-4. A recent ESEF filing (EU/UK/Nordic listed) gives exact tagged figures
    # and the full report text: no website search, no Firecrawl, no PDF. Otherwise
    # (no LEI, no filing, Germany/Ireland, growth markets, stale filing): the website.
    # A filing in another language (Nokia files in Finnish, AAK in Swedish) still gives
    # exact tagged figures, but the descriptive facts read better from the English
    # report on the website; the filing's own text is the fallback.
    filing, older, doc, found = None, None, None, {}
    if lei_info["record"] and not (website or report_url):
        filing = get_esef(lei_info["record"]["lei"], slug, use_cache)
        if filing and not is_recent(filing):
            # Kept as a fallback: the index often lags (337 Nordic companies only had
            # FY2024 indexed in Oct 2026), so try the website for a newer report first.
            log.info("ESEF filing is FY%s; trying the website for a newer report first",
                     filing.fiscal_year)
            older, filing = filing, None
    if filing is None and not (website or report_url):
        # SEC registrants (US companies, and others listed in the US: Chubb, NXP, ...)
        sec = get_edgar(legal_name, slug, use_cache)
        if sec and is_recent(sec):
            filing = sec
        elif sec and older is None:
            older = sec
    if filing is None and not (website or report_url):
        # Accounts filed in the home registry (Norway, Denmark): mostly private
        # companies, which rarely publish reports on their websites.
        reg = get_registry(legal_name, slug, lei_info["record"], country, use_cache)
        if reg and is_recent(reg):
            filing = reg
        elif reg and older is None:
            older = reg
    use_tags = filing is not None
    if use_tags and filing.language in (None, "en"):
        doc = _esef_doc_or_none(filing, slug, use_cache)
    if doc is None:
        website_error = None
        try:
            found = discover(legal_name, slug, fc, website, report_url, use_cache,
                             lei_info["record"], country)
            web_year = found.get("report_year")
            # A recent filing in another language (Rosenbauer files in German) or an
            # older one: either way the filing wins over an even older website report.
            # Otherwise the old report's text would be read next to the filing's tags.
            ref = filing or older
            if ref and web_year and web_year < int(ref.fiscal_year):
                log.info("Website report is FY%s, older than the ESEF filing (FY%s); using the filing",
                         web_year, ref.fiscal_year)
                filing, use_tags = ref, True
                doc = _esef_doc_or_none(filing, slug, use_cache)
            if doc is None:
                log.info("Step 4: fetching report")
                doc = _fetch_first_usable([found["report_url"], *found.get("report_alternatives", [])],
                                          slug, fc, use_cache)
        except (ReportNotFoundError, WebsiteNotFoundError, DownloadError, NeedsOCRError,
                CreditBudgetExceeded) as e:
            website_error = e
        if doc is None:
            fallback = filing or older
            if fallback is None:
                raise website_error
            log.info("No usable website report (%s); using the ESEF filing (FY%s)",
                     str(website_error)[:120], fallback.fiscal_year)
            filing, use_tags = fallback, True
            doc = _esef_doc_or_none(filing, slug, use_cache)
            if doc is None:
                raise website_error
    if doc.source_url == (filing.report_url if filing else None):
        found = {"website": None, "website_source": "not needed (filed accounts)",
                 "report_url": filing.report_url}

    # Step 5
    log.info("Step 5: selecting relevant sections")
    chunks = split_chunks(doc.pages)
    fin_chunks = select_chunks(chunks, "financials")
    qual_chunks = select_chunks(chunks, "qualitative") if qualitative else []

    # Step 6
    log.info("Step 6: extracting with the LLM")
    ex = extract(legal_name, doc.source_url, fin_chunks, qual_chunks,
                 tags=filing.figures if use_tags else None,
                 period_end=filing.period_end if use_tags else None,
                 qualitative=qualitative)

    # Step 7
    log.info("Step 7: validating")
    checks = run_checks(ex)
    lei_rec = lei_info["record"] or {}
    currency = ex.financials.revenue.currency or ex.financials.total_assets.currency
    front = "\n".join(p.text for p in doc.pages[:ENTITY_FRONT_PAGES])
    checks += check_entity(legal_name, lei_rec.get("legal_name"),
                           [country, lei_rec.get("country")], currency, front)
    if use_tags and doc.source_url == filing.report_url:
        # The filing is filed under this company's LEI: its identity is certain, even
        # when the report uses a trade name ("Nokian Tyres" for Nokian Renkaat Oyj).
        checks = [Check("entity", "company_name", "pass",
                        f"filing found by the company's own identifier "
                        f"({_identifier(filing)})")
                  if c.name == "entity" and c.target == "company_name" else c for c in checks]
    status = overall_status(ex, checks)
    kind = ("edgar" if isinstance(filing, EdgarFiling)
            else "registry" if isinstance(filing, RegistryFiling) else "esef")
    pages_of = {c.id: c.pages for c in chunks}

    def with_pages(d: dict) -> dict:
        return d | {"source_pages": pages_of.get(d.get("chunk_id"))}

    def money(name: str, fig) -> dict:
        d = with_pages(money_with_full_value(fig))
        return d | {"method": "xbrl_tag" if name in ex.tagged else "llm",
                    "xbrl_concept": ex.tagged.get(name)}

    fin, qual = ex.financials, ex.qualitative
    result = {
        "company_id": company_id,
        "input_name": legal_name,
        "country_code": country,
        "clean_name": clean,
        "status": status,
        "lei": lei_info["record"]["lei"] if lei_info["record"] else None,
        "lei_record": lei_info["record"],
        "lei_lookup": lei_info["reason"],
        "data_source": (f"{kind}" if use_tags and doc.source_url == filing.report_url
                        else f"{kind} tags + website text" if use_tags else "website"),
        "filing": ({"type": kind, "filing_id": filing.filing_id, "period_end": filing.period_end,
                    "form": getattr(filing, "form", "ESEF"), "cik": getattr(filing, "cik", None),
                    "registry": getattr(filing, "registry", None),
                    "registration_number": getattr(filing, "org_number", None),
                    "employees_in_filing": getattr(filing, "employees", None),
                    "revenue_and_operating_income": getattr(
                        (getattr(filing, "figures", None) or {}).get("revenue_and_operating_income"), "value", None),
                    "report_url": filing.report_url, "viewer_url": filing.viewer_url,
                    "package_url": filing.package_url}
                   if filing else None),
        "website": found.get("website"),
        "website_source": found.get("website_source"),
        "website_score": found.get("website_score"),
        "report_url": doc.source_url,
        "report_type": doc.kind,
        "fiscal_year": fin.fiscal_year,
        "period_end_date": iso_period_end(fin.period_end_date, fin.fiscal_year),
        "period_end_date_raw": fin.period_end_date,
        "revenue": money("revenue", fin.revenue),
        "total_assets": money("total_assets", fin.total_assets),
        "revenue_model": with_pages(qual.revenue_model.model_dump()) if qual else {},
        "business_structure": with_pages(qual.business_structure.model_dump()) if qual else {},
        "cross_check": {
            "total_equity_and_liabilities":
                money("total_equity_and_liabilities", fin.total_equity_and_liabilities),
        },
        "checks": checks_as_dicts(checks),
        "warnings": warnings_for(checks),
        "extracted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "model": llm.model_name(),
        "firecrawl_credits_used": fc.credits.total,
        "debug": {
            "cache_used": {"discovery": bool(found.get("from_cache")), "report": doc.from_cache},
            "markdown_file": str(doc.markdown_path.name),
            "chunks_total": len(chunks),
            "chunks_sent": {"financials": [c.id for c in fin_chunks],
                            "qualitative": [c.id for c in qual_chunks]},
        },
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{slug}.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    result["_output_path"] = str(out_path)
    return result
