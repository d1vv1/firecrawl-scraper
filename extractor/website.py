"""Step 2: find the company's official website with one Firecrawl search."""

import logging
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from .config import SEARCH_LIMIT, WEBSITE_MIN_SCORE, clean_name
from .firecrawl_client import FirecrawlClient

log = logging.getLogger(__name__)

# Domains that are never a company's own site. Matched on the registered domain
# and all its parents, so "uk.linkedin.com" is caught by "linkedin.com".
BLOCKED_DOMAINS = [
    # reference / social
    "wikipedia.org", "wikidata.org", "linkedin.com", "facebook.com", "twitter.com",
    "x.com", "instagram.com", "youtube.com", "glassdoor.com", "indeed.com",
    # company data / finance portals
    "bloomberg.com", "reuters.com", "crunchbase.com", "marketscreener.com",
    "zoominfo.com", "dnb.com", "craft.co", "owler.com", "companieshouse.gov.uk",
    "find-and-update.company-information.service.gov.uk", "opencorporates.com",
    "yahoo.com", "google.com", "morningstar.com", "morningstar.co.uk",
    "investing.com", "wsj.com", "marketwatch.com", "macrotrends.net",
    "stockanalysis.com", "companiesmarketcap.com", "londonstockexchange.com",
    "sec.gov", "annualreports.com", "simplywall.st", "tradingview.com",
    "cnbc.com", "fool.com", "seekingalpha.com", "statista.com",
    # news
    "ft.com", "bbc.co.uk", "bbc.com", "theguardian.com", "forbes.com",
    "businessinsider.com", "cnn.com", "nytimes.com", "economist.com",
    "telegraph.co.uk", "independent.co.uk", "thetimes.co.uk", "cityam.com",
    "fortune.com", "apnews.com", "prnewswire.com", "businesswire.com",
    "globenewswire.com",
    # LEI / registry aggregators
    "lei.net", "lei-registrar.com", "lei-lookup.com", "leilex.com", "gleif.org",
    "northdata.com", "northdata.de", "quartr.com",
]

COUNTRY_BONUS = 0.1   # domain's country TLD matches the LEI country (minus if it's another country's)
_CC_TLD_EXCEPTIONS = {"GB": "uk"}
_GENERIC_TLDS = {"com", "org", "net", "biz", "info", "group", "global", "co", "io", "eu"}

# Second-level public suffixes we need to know to find the registered domain.
_TWO_PART_SUFFIXES = {
    "co.uk", "org.uk", "gov.uk", "ac.uk", "com.au", "net.au", "co.nz", "co.jp",
    "co.za", "com.br", "com.mx", "com.cn", "com.hk", "com.sg", "co.in", "co.kr",
    "com.tr", "com.ar", "co.il",
}


@dataclass
class WebsiteResult:
    url: str          # e.g. "https://www.unilever.com"
    domain: str       # registered domain, e.g. "unilever.com"
    score: float
    candidates: list[dict] = field(default_factory=list)


class WebsiteNotFoundError(RuntimeError):
    pass


def registered_domain(host: str) -> str:
    host = host.lower().split(":")[0].removeprefix("www.")
    parts = host.split(".")
    n = 3 if ".".join(parts[-2:]) in _TWO_PART_SUFFIXES else 2
    return ".".join(parts[-n:])


def is_blocked(host: str) -> bool:
    host = host.lower().removeprefix("www.")
    return any(host == d or host.endswith("." + d) for d in BLOCKED_DOMAINS)


# clean_name() turns "&" into "and", but domains and titles spell it in the local
# language or not at all: "1&1 AG" -> 1und1.ag, "Marks & Spencer" -> marksandspencer.com.
_AND_SPELLINGS = ["and", "und", "et", "y", "n", ""]


def _and_variants(clean: str, spellings: list[str]) -> list[str]:
    words = clean.split()
    if "and" not in words:
        return [clean]
    return [" ".join(s if w == "and" else w for w in words).replace("  ", " ").strip()
            for s in spellings]


def score_candidate(clean: str, domain: str, title: str | None) -> float:
    """0..1. Domain match counts 70%, title match 30%. If the name has "and" (often
    from "&"), every spelling of it is tried and the best score wins."""
    label = re.sub(r"[^a-z0-9]", "", domain.split(".")[0])
    # Brand domains that use the ending as part of the name: add.life = "AddLife".
    whole = re.sub(r"[^a-z0-9]", "", domain)
    title_l = (title or "").lower()
    title_compact = re.sub(r"\s+", "", title_l)
    # "&" can only appear in titles; domain labels are alphanumeric.
    title_compacts = [v.replace(" ", "") for v in _and_variants(clean, _AND_SPELLINGS + ["&"])]
    return max(_score_one(v, lab, title_l, title_compact, title_compacts)
               for v in _and_variants(clean, _AND_SPELLINGS) for lab in (label, whole))


def _score_one(clean: str, label: str, title_l: str, title_compact: str,
               title_compacts: list[str]) -> float:
    compact = clean.replace(" ", "")
    # Single characters ("1" in "1 1") would partially match almost any domain.
    tokens = [t for t in clean.split() if len(t) >= 3] or [t for t in clean.split() if len(t) >= 2]

    if label == compact:
        domain_score = 1.0
    elif len(label) >= 4 and (compact.startswith(label) or label.startswith(compact)):
        domain_score = 0.8
    elif compact in label:
        domain_score = 0.7
    else:
        domain_score = 0.7 * sum(t in label for t in tokens) / len(tokens) if tokens else 0.0

    if any(len(c) >= 3 and c in title_compact for c in title_compacts):
        title_score = 1.0      # the whole name appears in the title, e.g. "1&1 AG | IR"
    else:
        title_score = sum(t in title_l for t in tokens) / len(tokens) if tokens else 0.0
    return round(0.7 * domain_score + 0.3 * title_score, 3)


def country_adjustment(domain: str, country: str | None) -> float:
    """+COUNTRY_BONUS if the domain's TLD is the company's country (unilever.co.uk for a
    GB company), -COUNTRY_BONUS if it is a different country's TLD, else 0."""
    if not country:
        return 0.0
    tld = domain.rsplit(".", 1)[-1]
    if tld in _GENERIC_TLDS or len(tld) != 2:
        return 0.0
    expected = _CC_TLD_EXCEPTIONS.get(country.upper(), country.lower())
    return COUNTRY_BONUS if tld == expected else -COUNTRY_BONUS


def find_website(legal_name: str, fc: FirecrawlClient,
                 country: str | None = None) -> WebsiteResult:
    """Firecrawl search on the legal name. `country` (from the LEI record, if any)
    nudges the score towards domains of the company's own country."""
    clean = clean_name(legal_name)
    query = f'"{legal_name}" official website investor relations'
    results = fc.search(query, limit=SEARCH_LIMIT)

    best: dict[str, dict] = {}
    candidates = []
    for r in results:
        url = r.get("url")
        if not url:
            continue
        host = urlparse(url).netloc
        if is_blocked(host):
            candidates.append({"url": url, "kept": False, "reason": "blocked domain"})
            continue
        domain = registered_domain(host)
        score = round(min(1.0, score_candidate(clean, domain, r.get("title"))
                          + country_adjustment(domain, country)), 3)
        candidates.append({"url": url, "kept": True, "domain": domain, "score": score,
                           "title": r.get("title")})
        if domain not in best or score > best[domain]["score"]:
            best[domain] = {"score": score, "url": url}

    for c in candidates:
        log.info("website candidate %s -> %s", c["url"],
                 f"score={c['score']}" if c["kept"] else f"dropped ({c['reason']})")

    if not best:
        raise WebsiteNotFoundError(
            f"No usable search results for {legal_name!r}. Pass --website URL.")
    domain, top = max(best.items(), key=lambda kv: kv[1]["score"])
    if top["score"] < WEBSITE_MIN_SCORE:
        raise WebsiteNotFoundError(
            f"Best website match {domain} has score {top['score']:.2f} "
            f"(< {WEBSITE_MIN_SCORE}). Not confident it is official; pass --website URL.")

    parsed = urlparse(top["url"])
    return WebsiteResult(url=f"{parsed.scheme}://{parsed.netloc}", domain=domain,
                         score=top["score"], candidates=candidates)
