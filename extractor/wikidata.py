"""Step 2a: LEI -> official website via Wikidata (free, no key).

Wikidata links an item to its LEI (property P1278) and official website (P856).
Coverage is good for large listed companies and poor for small ones, so a miss
here is normal; the caller falls back to Firecrawl search.

We use the main Wikidata API (wikidata.org/w/api.php), not the SPARQL query
service: the query service has frequent outages and was throttled to 1 request
per minute when this was built. Two calls: search items with
`haswbstatement:P1278=<LEI>`, then read their P856 claims.
"""

import logging
from urllib.parse import urlparse

import os
import time

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import load_settings  # noqa: F401  (loads .env so WIKIMEDIA_CONTACT is set)
from .website import country_adjustment, is_blocked, registered_domain, score_candidate

log = logging.getLogger(__name__)

API_URL = "https://www.wikidata.org/w/api.php"
TIMEOUT_S = 30
_RANK_ORDER = {"preferred": 2, "normal": 1}   # "deprecated" claims are ignored
_MIN_INTERVAL_S = 1.0                         # Wikimedia asks bots not to burst
_last_call = 0.0


def _headers() -> dict:
    """Wikimedia's API policy asks automated clients to name themselves and give a
    contact (email or URL); requests without one are rate-limited harder. Set
    WIKIMEDIA_CONTACT in .env to add yours."""
    load_settings()
    contact = os.getenv("WIKIMEDIA_CONTACT") or "contact not configured"
    return {"User-Agent": f"annual-report-extractor/0.1 ({contact}) python-httpx/{httpx.__version__}"}


class _Retryable(Exception):
    def __init__(self, msg: str, retry_after: float | None = None):
        super().__init__(msg)
        self.retry_after = retry_after


_backoff = wait_exponential(min=2, max=30)


def _wait(retry_state) -> float:
    exc = retry_state.outcome.exception()
    if isinstance(exc, _Retryable) and exc.retry_after:
        return min(exc.retry_after + 1, 120)
    return _backoff(retry_state)


@retry(retry=retry_if_exception_type((httpx.TransportError, _Retryable)),
       stop=stop_after_attempt(5), wait=_wait, reraise=True)
def _api(params: dict) -> dict:
    global _last_call
    pause = _MIN_INTERVAL_S - (time.monotonic() - _last_call)
    if pause > 0:
        time.sleep(pause)
    _last_call = time.monotonic()
    r = httpx.get(API_URL, params=params | {"format": "json"}, headers=_headers(), timeout=TIMEOUT_S)
    if r.status_code == 429 or r.status_code >= 500:
        try:
            retry_after = float(r.headers.get("retry-after", ""))
        except ValueError:
            retry_after = None
        log.info("Wikidata HTTP %s; retrying in %ss", r.status_code, retry_after or "a few ")
        raise _Retryable(f"HTTP {r.status_code}", retry_after)
    r.raise_for_status()
    try:
        return r.json()
    except ValueError as e:   # occasional empty/HTML body under load
        raise _Retryable("non-JSON response") from e


def _items_with_lei(lei: str) -> list[str]:
    data = _api({"action": "query", "list": "search", "srlimit": 5,
                 "srsearch": f"haswbstatement:P1278={lei}"})
    return [s["title"] for s in data["query"]["search"]]


ENGLISH = "Q1860"   # Wikidata item for the English language (P407 qualifier)
_GENERIC_TLDS = {"com", "org", "net", "group", "global", "biz", "info", "io", "co"}


def _websites(item_ids: list[str]) -> list[tuple[str, str, bool]]:
    """[(rank, url, is_english)] of non-deprecated official-website claims. Sites
    are often tagged with their language (P407), e.g. equinor.com = English,
    equinor.no = Norwegian."""
    data = _api({"action": "wbgetentities", "ids": "|".join(item_ids), "props": "claims"})
    out = []
    for entity in data.get("entities", {}).values():
        for claim in entity.get("claims", {}).get("P856", []):
            url = claim["mainsnak"].get("datavalue", {}).get("value")
            langs = {q.get("datavalue", {}).get("value", {}).get("id")
                     for q in claim.get("qualifiers", {}).get("P407", [])}
            if url and claim.get("rank") in _RANK_ORDER:
                out.append((claim["rank"], url, ENGLISH in langs))
    return out


def _tld_preference(domain: str, country: str | None) -> int:
    """2 = generic (.com: usually the English group site), 1 = the company's own
    country TLD, 0 = another country's TLD."""
    tld = domain.rsplit(".", 1)[-1]
    if tld in _GENERIC_TLDS or len(tld) != 2:
        return 2
    return 1 if country_adjustment(domain, country) > 0 else 0


def choose_website(sites: list, clean: str, country: str | None = None) -> str | None:
    """Pick one site. Order: rank (preferred > normal), tagged English, name match
    of the domain, generic TLD > own-country TLD > foreign TLD (equinor.com over
    equinor.no and equinor.jp; siemens.com over siemens.com.mx), then the shortest
    domain. Accepts plain URLs, (rank, url) or (rank, url, is_english). Returns the
    site's origin."""
    norm = []
    for s in sites:
        if isinstance(s, str):
            s = ("normal", s, False)
        elif len(s) == 2:
            s = (s[0], s[1], False)
        norm.append(s)
    usable = [s for s in norm if s[1] and urlparse(s[1]).netloc
              and not is_blocked(urlparse(s[1]).netloc)]
    if not usable:
        return None

    def key(s):
        rank, url, english = s
        domain = registered_domain(urlparse(url).netloc)
        return (_RANK_ORDER[rank], english, score_candidate(clean, domain, None),
                _tld_preference(domain, country), -len(domain))
    p = urlparse(max(usable, key=key)[1])
    return f"{p.scheme}://{p.netloc}"


def website_for_lei(lei: str, clean: str, country: str | None = None) -> tuple[str | None, str]:
    """Return (website origin or None, reason). Never raises: any failure is a miss."""
    try:
        items = _items_with_lei(lei)
        if not items:
            return None, "no Wikidata item with this LEI"
        sites = _websites(items)
    except (httpx.HTTPError, _Retryable, KeyError) as e:
        log.warning("Wikidata lookup failed for %s: %s", lei, str(e)[:200])
        return None, f"wikidata error: {str(e)[:200]}"
    if not sites:
        return None, f"Wikidata item {', '.join(items)} has no official website"
    site = choose_website(sites, clean, country)
    if not site:
        return None, f"Wikidata websites unusable: {[s[1] for s in sites][:5]}"
    log.info("Wikidata %s -> %s (from %d listed site(s))", ", ".join(items), site, len(sites))
    return site, f"wikidata {', '.join(items)}"


# Wikidata items for countries (P17 values), for the name search below.
COUNTRY_ITEMS = {
    "SE": "Q34", "NO": "Q20", "DK": "Q35", "FI": "Q33", "IS": "Q189", "FO": "Q4628",
    "DE": "Q183", "GB": "Q145", "NL": "Q55", "FR": "Q142", "CH": "Q39", "AT": "Q40",
    "BE": "Q31", "IE": "Q27", "LU": "Q32", "ES": "Q29", "IT": "Q38", "PL": "Q36",
    "US": "Q30", "BM": "Q23635", "MT": "Q233", "EE": "Q191", "LV": "Q211", "LT": "Q37",
}


def website_for_name(clean: str, country: str | None) -> tuple[str | None, str]:
    """Free fallback when the LEI isn't on Wikidata (common for small caps): search
    Wikidata by name and accept an item only if its label is the same name (legal
    form ignored), its country (P17) is the company's country, and it lists an
    official website. Returns (website origin or None, reason). Never raises."""
    from .config import clean_name

    country_item = COUNTRY_ITEMS.get((country or "").upper())
    if not clean or not country_item:
        return None, "name search needs a known country"
    try:
        hits = _api({"action": "wbsearchentities", "search": clean, "language": "en",
                     "type": "item", "limit": 5}).get("search", [])
        ids = [h["id"] for h in hits]
        if not ids:
            return None, "no Wikidata item with this name"
        entities = _api({"action": "wbgetentities", "ids": "|".join(ids),
                         "props": "claims|labels", "languages": "en"}).get("entities", {})
    except (httpx.HTTPError, _Retryable, KeyError) as e:
        log.warning("Wikidata name search failed for %r: %s", clean, str(e)[:200])
        return None, f"wikidata error: {str(e)[:200]}"

    for qid in ids:                      # search order = Wikidata's relevance order
        e = entities.get(qid, {})
        claims = e.get("claims", {})
        label = e.get("labels", {}).get("en", {}).get("value", "")
        countries = {c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                     for c in claims.get("P17", [])}
        if clean_name(label) != clean or country_item not in countries:
            continue
        sites = []
        for c in claims.get("P856", []):
            url = c["mainsnak"].get("datavalue", {}).get("value")
            langs = {q.get("datavalue", {}).get("value", {}).get("id")
                     for q in c.get("qualifiers", {}).get("P407", [])}
            if url and c.get("rank") in _RANK_ORDER:
                sites.append((c["rank"], url, ENGLISH in langs))
        site = choose_website(sites, clean, country)
        if site:
            log.info("Wikidata name search %s (%s) -> %s", qid, label, site)
            return site, f"wikidata name search {qid} ({label})"
    return None, "no Wikidata item with this name, country and a website"
