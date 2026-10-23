"""Data points from official APIs (no scraping, no AI): GLEIF, SEC EDGAR, and the
national registers of Norway (Brønnøysund), the UK (Companies House) and Finland
(PRH). Each function returns Found values with the exact URL it read them from.

Responses are cached in cache/api_<hash>.json for a week, so re-runs are free.
"""

import datetime as dt
import hashlib
import json
import logging
import re
from dataclasses import dataclass

import httpx

from . import edgar, lei as gleif, registries
from .config import CACHE_DIR

log = logging.getLogger(__name__)

API_CACHE_DAYS = 7
GLEIF_RECORD = gleif.GLEIF_API + "/lei-records/{lei}"
PRH_COMPANY = "https://avoindata.prh.fi/opendata-ytj-api/v3/companies?businessId={bid}"


@dataclass
class Found:
    """One value for one data point, with where it came from."""
    data_point: str
    value: str | float | int | None
    unit: str = ""
    period_end: str = ""
    source: str = ""          # who published it, in words
    endpoint: str = ""        # the exact URL (with #page=N for PDF pages)
    method: str = ""          # API / XBRL / PARSE / SCRAPE / BUY
    confidence: str = ""      # A exact from a register or tag, B quote verified, C unverified
    note: str = ""
    retrieved_at: str = ""    # when the source was read (UTC, ISO 8601)
    grain: str = "company"    # company, or role (executive pay per disclosed role)
    role_row: str = ""        # role grain: the role as stated, e.g. "CEO"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


_fetched_at: dict[str, str] = {}


def _cached(url: str, fetch) -> dict | None:
    """fetch() -> parsed JSON, or None for "not there" (404): both are cached.
    retrieved_at(url) then says when it was really fetched."""
    path = CACHE_DIR / f"api_{hashlib.sha1(url.encode()).hexdigest()}.json"
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(saved["at"])
        if age < dt.timedelta(days=API_CACHE_DAYS):
            _fetched_at[url] = dt.datetime.fromisoformat(saved["at"]).isoformat(timespec="seconds")
            return saved["data"]
    data = fetch()
    _fetched_at[url] = _now()
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"url": url, "at": _fetched_at[url], "data": data}), encoding="utf-8")
    return data


def retrieved_at(url: str) -> str:
    return _fetched_at.get(url) or _now()


def _gleif_key(path: str, params: dict | None = None) -> str:
    return f"{gleif.GLEIF_API}/{path}?{json.dumps(params or {}, sort_keys=True)}"


def _gleif(path: str, params: dict | None = None) -> dict | None:
    def fetch():
        try:
            return gleif._get(path, params or {})
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
    return _cached(_gleif_key(path, params), fetch)


# --- GLEIF ------------------------------------------------------------------------

def gleif_values(lei: str) -> list[Found]:
    url = GLEIF_RECORD.format(lei=lei)
    rec = _gleif(f"lei-records/{lei}")
    if not rec:
        return []
    e = rec["data"]["attributes"]["entity"]
    src = dict(source="GLEIF", endpoint=url, method="API", confidence="A",
               retrieved_at=retrieved_at(_gleif_key(f"lei-records/{lei}")))
    out = [Found("lei", lei, **src),
           Found("legal_name", e["legalName"]["name"], **src)]
    legal, hq = e.get("legalAddress") or {}, e.get("headquartersAddress") or {}
    if legal.get("country"):
        out.append(Found("country_code", legal["country"], **src,
                         note="legal address country"))
    if hq.get("city") or legal.get("city"):
        out.append(Found("head_office_city", (hq.get("city") or legal.get("city")).title(), **src,
                         note="headquarters address" if hq.get("city") else "legal address"))
    if e.get("registeredAs"):
        out.append(Found("business_id", e["registeredAs"], **src,
                         note=f"registration authority {(e.get('registeredAt') or {}).get('id') or '?'}"))
    others = [n["name"] for n in e.get("otherNames") or []]
    if others:
        out.append(Found("other_names", "; ".join(others), **src))

    parent = _gleif(f"lei-records/{lei}/ultimate-parent")
    purl = url + "/ultimate-parent"
    if parent and parent.get("data"):
        p = parent["data"]
        pname = p["attributes"]["entity"]["legalName"]["name"]
        out.append(Found("ultimate_parent", pname, source="GLEIF level 2", endpoint=purl,
                         method="API", confidence="A", note=f"parent LEI {p['id']}",
                         retrieved_at=retrieved_at(_gleif_key(f"lei-records/{lei}/ultimate-parent"))))
    else:
        exc = _gleif(f"lei-records/{lei}/ultimate-parent-reporting-exception")
        reason = ((exc or {}).get("data") or {}).get("attributes", {}).get("reason")
        if reason:
            # NO_KNOWN_PERSON / NATURAL_PERSONS: no company above this one
            out.append(Found("ultimate_parent", "none (top of group)" if reason in
                             ("NO_KNOWN_PERSON", "NATURAL_PERSONS") else None,
                             source="GLEIF level 2", endpoint=purl + "-reporting-exception",
                             method="API", confidence="A" if reason in
                             ("NO_KNOWN_PERSON", "NATURAL_PERSONS") else "",
                             note=f"reporting exception: {reason}", retrieved_at=src["retrieved_at"]))

    isins = _gleif(f"lei-records/{lei}/isins", {"page[size]": 200})
    codes = [d["attributes"]["isin"] for d in (isins or {}).get("data") or []]
    if codes:
        # Shares and bonds alike: only used to confirm an ISIN read from the report.
        out.append(Found("_gleif_isins", ";".join(codes), source="GLEIF ISIN map",
                         endpoint=url + "/isins", method="API"))
    return out


# --- SEC EDGAR --------------------------------------------------------------------

def edgar_values(cik: int) -> list[Found]:
    surl = edgar.SUBMISSIONS_URL.format(cik=cik)
    sub = _cached(surl, lambda: edgar._get(surl).json())
    src = dict(source="SEC EDGAR submissions", endpoint=surl, method="API", confidence="A",
               retrieved_at=retrieved_at(surl))
    out = [Found("cik", str(cik), **src)]
    if sub.get("name"):
        out.append(Found("legal_name", edgar.sec_title(sub["name"]), **src))
    if sub.get("tickers"):
        out.append(Found("ticker", "; ".join(sub["tickers"]), **src))
        out.append(Found("listing_status", "listed", **src,
                         note="has an exchange ticker at the SEC"))
    if [x for x in sub.get("exchanges") or [] if x]:
        out.append(Found("exchange", "; ".join(x for x in sub["exchanges"] if x), **src))
    if sub.get("sic"):
        out.append(Found("sector_code", f"SIC {sub['sic']}", **src, note=sub.get("sicDescription") or ""))
        if sub.get("sicDescription"):
            out.append(Found("sub_sector", sub["sicDescription"], **src, note=f"SIC {sub['sic']}"))
    city = ((sub.get("addresses") or {}).get("business") or {}).get("city")
    if city:
        out.append(Found("head_office_city", city.title(), **src, note="business address"))
    former = [f["name"] for f in sub.get("formerNames") or []]
    if former:
        out.append(Found("other_names", "; ".join(former), **src, note="former names"))

    furl = edgar.FACTS_URL.format(cik=cik)
    try:
        facts = _cached(furl, lambda: edgar._get(furl).json())
    except httpx.HTTPStatusError:
        facts = None
    dei = ((facts or {}).get("facts") or {}).get("dei") or {}
    shares = ((dei.get("EntityCommonStockSharesOutstanding") or {}).get("units") or {}).get("shares")
    if shares:
        latest = max(shares, key=lambda f: (f["end"], f.get("filed", "")))
        # Several share classes are tagged separately on the same date: add them up.
        total = sum(f["val"] for f in shares if f["end"] == latest["end"]
                    and f.get("accn") == latest.get("accn"))
        out.append(Found("shares_outstanding", total, unit="shares", period_end=latest["end"],
                         source="SEC EDGAR XBRL", endpoint=furl, method="XBRL", confidence="A",
                         retrieved_at=retrieved_at(furl),
                         note=f"dei:EntityCommonStockSharesOutstanding, {latest.get('form')} "
                              f"accession {latest.get('accn')}"))
    return out


# --- Norway: Brønnøysund ------------------------------------------------------------

def brreg_values(orgnr: str) -> list[Found]:
    url = registries.BRREG_ENTITY.format(orgnr=orgnr)

    def fetch():
        r = registries._request("GET", url)
        return r.json() if r.status_code == 200 else None
    ent = _cached(url, fetch)
    if not ent:
        return []
    src = dict(source="Brønnøysund entity register", endpoint=url, method="API", confidence="A",
               retrieved_at=retrieved_at(url))
    out = [Found("country_code", "NO", **src, note="registered in Norway"),
           Found("business_id", ent["organisasjonsnummer"], **src),
           Found("legal_name", ent.get("navn"), **src)]
    form = (ent.get("organisasjonsform") or {}).get("kode")
    if form:
        out.append(Found("legal_form", form, **src, note=(ent["organisasjonsform"].get("beskrivelse") or "")))
    nace = ent.get("naeringskode1") or {}
    if nace.get("kode"):
        out.append(Found("sector_code", f"NACE {nace['kode']}", **src, note=nace.get("beskrivelse") or ""))
        out.append(Found("sub_sector", nace.get("beskrivelse"), **src, note=f"NACE {nace['kode']}"))
    city = (ent.get("forretningsadresse") or {}).get("poststed")
    if city:
        out.append(Found("head_office_city", city.title(), **src, note="business address"))
    if ent.get("antallAnsatte") is not None and ent.get("harRegistrertAntallAnsatte", True):
        out.append(Found("headcount", ent["antallAnsatte"], unit="employees", **src,
                         note="employees registered in the Aa register (null when 0-4)"))
    if form == "ASA":
        out.append(Found("listing_status", "listed", **src,
                         note="ASA: public limited company (usually listed); confirm on the exchange"))
    return out


# --- UK: Companies House --------------------------------------------------------------

def companies_house_values(number: str) -> list[Found]:
    if not registries.ch_key():
        return []
    purl = f"{registries.CH_API}/company/{number}"

    def fetch(path):
        def go():
            r = registries._ch(path)
            return r.json() if r.status_code == 200 else None
        return go
    prof = _cached(purl, fetch(f"/company/{number}"))
    if not prof:
        return []
    src = dict(source="Companies House", endpoint=purl, method="API", confidence="A",
               retrieved_at=retrieved_at(purl))
    out = [Found("country_code", "GB", **src, note="registered in the UK"),
           Found("business_id", prof["company_number"], **src),
           Found("legal_name", prof.get("company_name"), **src)]
    if prof.get("type"):
        out.append(Found("legal_form", prof["type"], **src))
    if prof.get("sic_codes"):
        out.append(Found("sector_code", "SIC (UK) " + "; ".join(prof["sic_codes"]), **src))
    city = (prof.get("registered_office_address") or {}).get("locality")
    if city:
        out.append(Found("head_office_city", city.title(), **src, note="registered office"))

    psc_url = purl + "/persons-with-significant-control"
    psc = _cached(psc_url, fetch(f"/company/{number}/persons-with-significant-control"))
    active = [p for p in (psc or {}).get("items") or [] if not p.get("ceased_on")]
    major = [p for p in active if any("75-to-100" in n or "more-than-50" in n
                                      for n in p.get("natures_of_control") or [])]
    if major:
        p = major[0]
        corporate = "corporate" in (p.get("kind") or "") or "legal-person" in (p.get("kind") or "")
        out.append(Found("controlling_owner_name", p.get("name"), source="Companies House PSC register",
                         endpoint=psc_url, method="API", confidence="A",
                         note="; ".join(p.get("natures_of_control") or []),
                         retrieved_at=retrieved_at(psc_url)))
        if corporate:
            out.append(Found("ultimate_parent", p.get("name"), source="Companies House PSC register",
                             endpoint=psc_url, method="API", confidence="B",
                             note="corporate PSC with control of more than half (immediate parent)",
                             retrieved_at=retrieved_at(psc_url)))
    elif psc is not None and active:
        out.append(Found("_psc_none_major", "; ".join(p.get("name", "") for p in active),
                         source="Companies House PSC register", endpoint=psc_url, method="API"))
    return out


# --- Finland: PRH -------------------------------------------------------------------

def prh_values(business_id: str) -> list[Found]:
    url = PRH_COMPANY.format(bid=business_id)

    def fetch():
        r = registries._request("GET", url)
        return r.json() if r.status_code == 200 else None
    data = _cached(url, fetch)
    companies = (data or {}).get("companies") or []
    if not companies:
        return []
    c = companies[0]
    src = dict(source="PRH / YTJ open data", endpoint=url, method="API", confidence="A",
               retrieved_at=retrieved_at(url))
    out = [Found("country_code", "FI", **src, note="registered in Finland"),
           Found("business_id", (c.get("businessId") or {}).get("value") or business_id, **src)]
    names = [n for n in c.get("names") or [] if not n.get("endDate")]
    if names:
        out.append(Found("legal_name", names[0]["name"], **src))
    line = c.get("mainBusinessLine") or {}
    if line.get("type"):
        desc = next((d["description"] for d in line.get("descriptions") or []
                     if str(d.get("languageCode")) == "3"), "")
        out.append(Found("sector_code", f"TOL/NACE {line['type']}", **src, note=desc))
        if desc:
            out.append(Found("sub_sector", desc, **src, note=f"TOL {line['type']}"))
    for a in c.get("addresses") or []:
        offices = a.get("postOffices") or []
        city = next((o["city"] for o in offices if str(o.get("languageCode")) == "1"), None) \
            or (offices[0]["city"] if offices else None)
        if city:
            out.append(Found("head_office_city", city.title(), **src, note="registered address"))
            break
    return out


def registry_values(country: str | None, number: str | None) -> list[Found]:
    """The home register's facts, where it is open and we have the number."""
    if not number:
        return []
    try:
        if country == "NO":
            return brreg_values(re.sub(r"\D", "", number))
        if country == "GB":
            n = re.sub(r"[^A-Za-z0-9]", "", number).upper()
            return companies_house_values(n.zfill(8) if n.isdigit() else n)
        if country == "FI":
            return prh_values(number.strip())
    except (httpx.HTTPError, registries.RegistryUnavailable, ValueError) as e:
        log.warning("Register lookup for %s %s failed: %s", country, number, str(e)[:150])
    return []
