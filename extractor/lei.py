"""Step 1b: find the company's LEI from its legal name (GLEIF API, free, no key).

Names in company lists rarely match GLEIF letter for letter: "Volvo AB" is
"Aktiebolaget Volvo" in GLEIF, "Orsted A/S" is "ØRSTED A/S", "Sampo plc" is
"Sampo Oyj". So we:
  1. split every name into a base name and a legal form, treating equivalent forms
     as equal (AB = Aktiebolag, Oyj = Abp = plc, A/S = Aktieselskab, ...), and
     ignoring accents and "(publ)";
  2. search GLEIF by the base name, restricted to the company's country when we
     know it (GLEIF's name search only finds names that *contain* the query);
  3. accept an exact base-name match, or else a unique name that contains the
     listed name ("H & M Hennes & Mauritz AB" for "Hennes & Mauritz AB").
Anything ambiguous returns no LEI; the pipeline then falls back to web search.
"""

import logging
import re
import time
from dataclasses import asdict, dataclass, field

import httpx
from tenacity import (retry, retry_if_exception, stop_after_attempt,
                      wait_exponential)

from .config import fold

log = logging.getLogger(__name__)

GLEIF_API = "https://api.gleif.org/api/v1"
HEADERS = {"Accept": "application/vnd.api+json",
           "User-Agent": "annual-report-extractor/0.1"}
TIMEOUT_S = 30

# Spelled-out legal forms -> canonical short form (applied to folded text).
_FORM_PHRASES = [
    ("public limited company", "plc"), ("julkinen osakeyhtio", "plc"),
    ("aktiengesellschaft", "ag"), ("societas europaea", "se"),
    ("naamloze vennootschap", "nv"), ("allmennaksjeselskap", "asa"),
    ("aksjeselskap", "as"), ("aktieselskabet", "as"), ("aktieselskab", "as"),
    ("aktiebolaget", "ab"), ("aktiebolag", "ab"), ("osakeyhtio", "oy"),
    ("anpartsselskab", "aps"), ("einkahlutafelag", "ehf"), ("hlutafelag", "hf"),
    ("partafelag", "pf"), ("spolka akcyjna", "sa"),
    ("limited", "ltd"), ("incorporated", "inc"), ("corporation", "corp"),
    ("company", "co"),
]
# Short forms -> canonical (Finnish Oyj and its Swedish twin Abp are a plc).
_FORM_TOKENS = {"oyj": "plc", "abp": "plc", "plc": "plc", "ltd": "ltd", "inc": "inc",
                "corp": "corp", "co": "co", "ag": "ag", "se": "se", "sa": "sa", "nv": "nv",
                "bv": "bv", "gmbh": "gmbh", "ab": "ab", "as": "as", "asa": "asa", "oy": "oy",
                "aps": "aps", "hf": "hf", "ehf": "ehf", "spa": "spa", "sas": "sas",
                "llc": "llc", "kgaa": "kgaa", "pf": "pf"}
# English words lists use for any form ("Metsä Board Corporation" = GLEIF "Metsä Board
# Oyj", "Otello Corp ASA"): they never make two forms incompatible.
_WEAK_FORMS = {"corp", "co"}
_IGNORED = {"publ", "the"}


@dataclass
class LeiRecord:
    lei: str
    legal_name: str
    country: str | None          # legal address country (ISO 3166-1 alpha-2)
    jurisdiction: str | None
    legal_form_id: str | None    # ISO 20275 ELF code, e.g. "B6ES" = UK plc
    entity_status: str | None    # ACTIVE / INACTIVE
    registration_status: str | None  # ISSUED / LAPSED / ...
    registered_as: str | None    # local registry number, e.g. Companies House no.

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class LeiResult:
    record: LeiRecord | None
    reason: str
    candidates: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class NameKey:
    base: tuple[str, ...]
    forms: frozenset[str]


def name_key(name: str) -> NameKey:
    """'AB Volvo (publ)' / 'Aktiebolaget Volvo' -> base ('volvo',), forms {'ab'}."""
    t = fold(name).replace("&", " and ").replace("a/s", " as ").replace("p/f", " pf ")
    t = re.sub(r"(?<=\b[a-z])\.(?=[a-z]\b)", "", t)    # n.v. -> nv., p.l.c -> plc
    t = re.sub(r"[^a-z0-9]+", " ", t)
    for phrase, short in _FORM_PHRASES:
        t = re.sub(rf"\b{phrase}\b", f" {short} ", t)
    base, forms = [], set()
    for tok in t.split():
        if tok in _IGNORED:
            continue
        if tok in _FORM_TOKENS:
            forms.add(_FORM_TOKENS[tok])
        else:
            base.append(tok)
    return NameKey(tuple(base), frozenset(forms))


def normalize_legal_name(name: str) -> str:
    """Comparable string form of name_key(): 'Unilever Public Limited Company' -> 'unilever plc'."""
    k = name_key(name)
    return " ".join(k.base + tuple(sorted(k.forms)))


def _forms_compatible(a: NameKey, b: NameKey) -> bool:
    fa, fb = a.forms - _WEAK_FORMS, b.forms - _WEAK_FORMS
    return not fa or not fb or fa == fb


def _contains(outer: tuple[str, ...], inner: tuple[str, ...]) -> bool:
    """GLEIF's name ends with the listed name, with extra words only in front:
    "H & M Hennes & Mauritz" for "Hennes & Mauritz". Extra words after it usually
    mean a different company: "Volvo Car" for "Volvo", "Neste Asset Management"
    for "Neste"."""
    n = len(inner)
    return 0 < n < len(outer) and outer[-n:] == inner


def match_level(listed: str, gleif_name: str) -> str | None:
    """"exact" (same base name, compatible legal form), "partial" (GLEIF's name
    contains the listed base name), or None."""
    a, b = name_key(listed), name_key(gleif_name)
    if not a.base or not _forms_compatible(a, b):
        return None
    if a.base == b.base:
        return "exact"
    if _contains(b.base, a.base):
        return "partial"
    return None


def search_text(name: str) -> str:
    """The listed name without legal form and '(publ)', for GLEIF's contains-search:
    'AB Volvo (publ)' -> 'Volvo', 'Hennes & Mauritz AB' -> 'Hennes & Mauritz'."""
    t = re.sub(r"\([^)]*\)", " ", name)
    t = re.sub(r"(?i)\b[ap]/[sf]\b", " ", t)
    words = [w for w in t.split()
             if fold(w).strip(".,") not in _FORM_TOKENS
             and not any(fold(w).strip(".,") == p for p, _ in _FORM_PHRASES if " " not in p)]
    return " ".join(words) or name


def _retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code in (429, 500, 502, 503, 504)


_MIN_INTERVAL_S = 1.0        # GLEIF allows 60 requests/minute
_last_call = 0.0


@retry(retry=retry_if_exception(_retryable), stop=stop_after_attempt(4),
       wait=wait_exponential(min=2, max=30), reraise=True)
def _get(path: str, params: dict) -> dict:
    global _last_call
    wait = _MIN_INTERVAL_S - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()
    r = httpx.get(f"{GLEIF_API}/{path}", params=params, headers=HEADERS, timeout=TIMEOUT_S)
    r.raise_for_status()
    return r.json()


def _to_record(item: dict) -> LeiRecord:
    a = item["attributes"]
    e = a["entity"]
    return LeiRecord(
        lei=item["id"],
        legal_name=e["legalName"]["name"],
        country=(e.get("legalAddress") or {}).get("country"),
        jurisdiction=e.get("jurisdiction"),
        legal_form_id=(e.get("legalForm") or {}).get("id"),
        entity_status=e.get("status"),
        registration_status=(a.get("registration") or {}).get("status"),
        registered_as=e.get("registeredAs"),
    )


def _names(item: dict) -> list[str]:
    e = item["attributes"]["entity"]
    return [e["legalName"]["name"]] + [n["name"] for n in e.get("otherNames") or []]


def fetch_by_lei(lei: str) -> LeiRecord | None:
    data = _get("lei-records", {"filter[lei]": lei.strip().upper()})["data"]
    return _to_record(data[0]) if data else None


def _in_country(rec: LeiRecord, country: str | None) -> bool:
    c = (country or "").upper()
    return bool(c) and c in (rec.country, (rec.jurisdiction or "").split("-")[0])


def _narrow(recs: list[LeiRecord]) -> list[LeiRecord]:
    for keep in (lambda r: r.entity_status == "ACTIVE",
                 lambda r: r.registration_status == "ISSUED"):
        if len(recs) > 1 and any(keep(r) for r in recs):
            recs = [r for r in recs if keep(r)]
    return recs


def pick_match(legal_name: str, items: list[dict], country: str | None = None) -> LeiResult:
    """Choose one GLEIF record for the listed name. Tiers, best first:
    exact in country, exact anywhere, partial in country (or anywhere if no country
    given). Within a tier prefer ACTIVE, then ISSUED; more than one left = ambiguous."""
    candidates, by_level = [], {"exact": [], "partial": []}
    extra: dict[str, int] = {}     # partial matches: extra words in GLEIF's name
    by_legal_name: set[str] = set()  # exact on the current legal name, not a former name
    listed_len = len(name_key(legal_name).base)
    seen = set()
    for item in items:
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        rec = _to_record(item)
        levels = {match_level(legal_name, n) for n in _names(item)} - {None}
        level = "exact" if "exact" in levels else ("partial" if levels else None)
        candidates.append({"lei": rec.lei, "name": rec.legal_name, "country": rec.country,
                           "entity_status": rec.entity_status, "name_match": level})
        if level:
            by_level[level].append(rec)
        if level == "partial":
            extra[rec.lei] = min(len(name_key(n).base) - listed_len for n in _names(item)
                                 if match_level(legal_name, n) == "partial")
        if level == "exact" and match_level(legal_name, rec.legal_name) == "exact":
            by_legal_name.add(rec.lei)

    exact, partial = by_level["exact"], by_level["partial"]
    tiers = []
    if country:
        tiers.append(("exact name match", [r for r in exact if _in_country(r, country)]))
    tiers.append(("exact name match" + (" (registered outside " + country.upper() + ")"
                                        if country else ""), exact))
    tiers.append(("partial name match", [r for r in partial if _in_country(r, country)]
                  if country else partial))

    for reason, recs in tiers:
        if recs and reason.startswith("partial"):
            # "H & M Hennes & Mauritz AB" (3 extra words) beats "... GBC AB" (4)
            fewest = min(extra[r.lei] for r in recs)
            recs = [r for r in recs if extra[r.lei] == fewest]
        if reason.startswith("exact") and any(r.lei in by_legal_name for r in recs):
            # current legal name beats a former/other name: "F-Secure Oyj" is the new
            # F-Secure, not WithSecure (whose former name it is)
            recs = [r for r in recs if r.lei in by_legal_name]
        recs = _narrow(recs)
        if len(recs) == 1:
            return LeiResult(recs[0], reason, candidates)
        if len(recs) > 1:
            leis = ", ".join(f"{r.lei} {r.legal_name} ({r.country})" for r in recs[:5])
            return LeiResult(None, f"ambiguous: {len(recs)} records match {legal_name!r} "
                                   f"({reason}): {leis}. Pass --lei to choose.", candidates)
    return LeiResult(None, f"no GLEIF record matching {legal_name!r}"
                           + (f" in {country.upper()}" if country else ""), candidates)


def find_lei(legal_name: str, country: str | None = None) -> LeiResult:
    """Search GLEIF for the listed company. Queries: the full name; the base name
    (in the country, if known); if neither gives an answer,
    GLEIF's fuzzy completions. The first two always both run: an early partial
    answer ("Volvo Car AB" for "Volvo AB") can hide the exact one ("Aktiebolaget Volvo")."""
    items: list[dict] = []
    base = search_text(legal_name)
    queries = [{"filter[entity.legalName]": legal_name}]
    if country:
        queries.append({"filter[entity.names]": base,
                        "filter[entity.legalAddress.country]": country.upper()})
    else:
        queries.append({"filter[entity.names]": base})

    for q in queries:
        items += _get("lei-records", q | {"page[size]": 100})["data"]
    result = pick_match(legal_name, items, country)
    if result.record is None and not result.reason.startswith("ambiguous") and country:
        # Many Nordic-listed companies are registered abroad (Archer Ltd and BW Energy
        # in Bermuda, Catena Media in Malta): search the base name worldwide.
        items += _get("lei-records", {"filter[entity.names]": base, "page[size]": 100})["data"]
        result = pick_match(legal_name, items, country)
    if result.record is None and not result.reason.startswith("ambiguous"):
        fuzzy = _get("fuzzycompletions", {"field": "entity.legalName", "q": legal_name})["data"]
        leis = [f["relationships"]["lei-records"]["data"]["id"] for f in fuzzy
                if f.get("relationships", {}).get("lei-records")
                and match_level(legal_name, f["attributes"]["value"])]
        if leis:
            items += _get("lei-records", {"filter[lei]": ",".join(leis)})["data"]
            result = pick_match(legal_name, items, country)

    for c in result.candidates:
        if c["name_match"]:
            log.debug("LEI candidate %s %s (%s, %s) match=%s", c["lei"], c["name"],
                      c["country"], c["entity_status"], c["name_match"])
    if result.record:
        log.info("LEI: %s (%s, %s; %s)", result.record.lei, result.record.legal_name,
                 result.record.country, result.reason)
    else:
        log.info("No LEI: %s", result.reason)
    return result
