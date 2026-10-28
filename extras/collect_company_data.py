#!/usr/bin/env python3
"""
collect_company_data.py
=======================

Collects the "Open API" data points from data_point_endpoint_mapping.xlsx
(sheet "API endpoints") for a list of companies, and writes one row per
company x data point with source, endpoint, period_end and retrieved_at,
as the build-test "Load" stage asks for.

Sources and data points
-----------------------
  GLEIF            Legal name, Country, Registration ID, Head-office city
  Companies House  Legal name, Country, Registration ID, Sector, Head-office city,
                   Revenue, Total assets, Employees (FTE), Controlling owner, PE stake
  PRH YTJ / XBRL   Legal name, Country, Registration ID, Sector, Head-office city,
                   Revenue, Total assets, Employees
  SEC EDGAR        Legal name, Country, Registration ID, Ticker, Exchange, ISIN (n/a),
                   Listing status, Listing segment (n/a), Sector, Head-office city,
                   Revenue, Total assets
  Brønnøysund      Legal name, Country, Registration ID, Sector, Head-office city,
                   Employees (headcount), Revenue, Total assets
  Bolagsverket     Legal name, Country, Registration ID, Sector, Head-office city,
                   Revenue, Total assets, Employees (FTE)
  CVR              Legal name, Country, Registration ID, Sector, Head-office city,
                   Employees (FTE, headcount), Controlling owner, PE stake,
                   Revenue, Total assets

Which source runs for which company follows the route table: segment + country.

Input CSV (UTF-8, header row required)
--------------------------------------
  company_id   your own key (required)
  name         company name (optional; used for lookups when IDs are missing)
  segment      NL | EU | US | NP | OP   (Nordic listed, EU & UK listed, US listed,
               Nordic & UK private, Other private or unknown)
  country      ISO-2: SE, NO, DK, FI, GB, US, DE, ...
  lei          optional
  national_id  optional: SE org.nr, NO org.nr, DK CVR, FI Business ID, UK company number
  cik          optional (US)
  ticker       optional (US: used to find the CIK)
  isin         optional (used to find the LEI)

Credentials (environment variables)
-----------------------------------
  CH_API_KEY            Companies House REST API key            (UK)
  SEC_USER_AGENT        e.g. "Ariqt Data npraveen@ariqt.com"    (US, required by SEC)
  BOLAG_CLIENT_ID       Bolagsverket OAuth2 client id           (SE)
  BOLAG_CLIENT_SECRET   Bolagsverket OAuth2 client secret       (SE)
  BOLAG_TOKEN_URL       default https://portal.api.bolagsverket.se/oauth2/token
  BOLAG_BASE_URL        default https://gw.api.bolagsverket.se/vardefulla-datamangder/v1
  CVR_USER, CVR_PASSWORD  CVR Elasticsearch user from Erhvervsstyrelsen (DK)
A source whose credentials are missing is skipped with a warning.

Usage
-----
  pip install requests
  python collect_company_data.py companies.csv -o results.csv
  python collect_company_data.py companies.csv -o results.csv --sources gleif,sec --cache raw/
  python collect_company_data.py --dump-tags some_report.xhtml     # list XBRL tags in a file

Field names marked "verify" in the mapping workbook are coded defensively
(several candidate paths). Check the first results, and use --cache to keep
raw responses so you can adjust paths.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import logging
import os
import re
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from typing import Any, Iterable
from urllib.parse import urlparse

import requests

log = logging.getLogger("collect")

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
GLEIF = "https://api.gleif.org/api/v1"
CH = "https://api.company-information.service.gov.uk"
YTJ = "https://avoindata.prh.fi/opendata-ytj-api/v3"
PRHX = "https://avoindata.prh.fi/opendata-xbrl-api/v3"
SEC_DATA = "https://data.sec.gov"
SEC_WWW = "https://www.sec.gov"
BRREG = "https://data.brreg.no/enhetsregisteret/api"
BRREG_R = "https://data.brreg.no/regnskapsregisteret/regnskap"
CVR = "http://distribution.virk.dk"
BOLAG_BASE = os.getenv("BOLAG_BASE_URL", "https://gw.api.bolagsverket.se/vardefulla-datamangder/v1")
BOLAG_TOKEN = os.getenv("BOLAG_TOKEN_URL", "https://portal.api.bolagsverket.se/oauth2/token")

# Minimum seconds between requests, per host (published limits where known).
MIN_INTERVAL = {
    "api.gleif.org": 1.05,                               # 60 / minute
    "api.company-information.service.gov.uk": 0.55,      # 600 / 5 minutes
    "document-api.company-information.service.gov.uk": 0.55,
    "frontend-doc-api.company-information.service.gov.uk": 0.55,
    "data.sec.gov": 0.12, "www.sec.gov": 0.12,           # max 10 / second
    "avoindata.prh.fi": 0.5,
    "data.brreg.no": 0.2,
    "distribution.virk.dk": 0.5,
    "gw.api.bolagsverket.se": 0.5,
}

SEGMENTS = {
    "NL": "NL", "NORDIC LISTED": "NL",
    "EU": "EU", "EU & UK LISTED": "EU",
    "US": "US", "US LISTED": "US",
    "NP": "NP", "NORDIC & UK PRIVATE": "NP",
    "OP": "OP", "OTHER PRIVATE OR UNKNOWN": "OP",
}
NORDIC = {"SE", "NO", "DK", "FI", "IS"}

# The 16 data points in the mapping workbook (sheet "API endpoints"); every company gets a row for each.
DATA_POINTS = ["Legal name", "Country", "Registration ID", "Head-office city", "Ticker", "ISIN", "Exchange",
               "Listing status", "Listing segment", "Sector (NACE / SIC)", "Revenue", "Total assets",
               "Employees (FTE)", "Employees (headcount)", "Controlling owner", "PE stake of 5% or more"]
_IDENTITY = {"NL", "EU", "US", "NP", "OP"}
# Segments the mapping (or this script's GLEIF route) has a source for, per data point
DP_SEGMENTS = {
    "Legal name": _IDENTITY, "Country": _IDENTITY, "Registration ID": _IDENTITY, "Head-office city": _IDENTITY,
    "Ticker": {"US"}, "ISIN": {"US"}, "Exchange": {"US"}, "Listing status": {"US"}, "Listing segment": {"US"},
    "Sector (NACE / SIC)": {"NL", "US", "NP"}, "Revenue": {"US", "NP"}, "Total assets": {"US", "NP"},
    "Employees (FTE)": {"NP"}, "Employees (headcount)": {"NP"},
    "Controlling owner": {"NP"}, "PE stake of 5% or more": {"NP"},
}
SEGMENT_NAMES = {"NL": "Nordic listed", "EU": "EU & UK listed", "US": "US listed", "NP": "Nordic & UK private",
                 "OP": "Other private or unknown"}
NULL = "null"

OUT_FIELDS = ["company_id", "company_name", "segment", "country", "lei", "data_point", "value", "unit",
              "period_end", "source", "endpoint", "method", "retrieved_at", "confidence", "note"]

# XBRL tag candidates (local names, matched case-insensitively).
TAGS = {
    "uk_revenue": ["TurnoverRevenue", "Revenue"],
    "uk_fixed": ["FixedAssets"],
    "uk_current": ["CurrentAssets"],
    "uk_total_assets": ["TotalAssets", "Assets"],
    "uk_employees": ["AverageNumberEmployeesDuringPeriod"],
    "se_revenue": ["Nettoomsattning"],
    "se_assets": ["Tillgangar"],
    "se_employees": ["MedelantaletAnstallda"],
    "dk_revenue": ["Revenue"],
    "dk_gross_profit": ["GrossProfitLoss", "GrossResult"],
    "dk_assets": ["Assets"],
    "dk_employees": ["AverageNumberOfEmployees"],
    # Finnish CRR taxonomy: names NOT confirmed. Run --dump-tags on one
    # /financial response and put the right local names here.
    "fi_revenue": ["Liikevaihto", "NetSales", "Revenue", "Turnover"],
    "fi_assets": ["VastaavaaYhteensa", "Vastaavaa", "BalanceSheetTotal", "Assets", "TotalAssets"],
    "fi_employees": ["HenkilostoKeskimaarin", "AverageNumberOfPersonnel", "AverageNumberOfEmployees"],
}


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
class Http:
    def __init__(self, cache_dir: str | None = None, timeout: int = 60):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = os.getenv("SEC_USER_AGENT", "company-data-build-test (contact: set SEC_USER_AGENT)")
        self.last: dict[str, float] = {}
        self.cache_dir = cache_dir
        self.timeout = timeout
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    def _wait(self, url: str) -> None:
        host = urlparse(url).hostname or ""
        gap = MIN_INTERVAL.get(host, 0.3)
        since = time.monotonic() - self.last.get(host, 0)
        if since < gap:
            time.sleep(gap - since)
        self.last[host] = time.monotonic()

    def request(self, method: str, url: str, *, retries: int = 4, **kw) -> requests.Response | None:
        kw.setdefault("timeout", self.timeout)
        for attempt in range(retries + 1):
            self._wait(url)
            try:
                r = self.s.request(method, url, **kw)
            except requests.RequestException as e:
                log.warning("%s %s failed: %s", method, url, e)
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 404:
                return None
            if r.status_code in (429, 500, 502, 503, 504):
                wait = float(r.headers.get("Retry-After", 2 ** (attempt + 1)))
                log.info("HTTP %s from %s, retry in %.0fs", r.status_code, urlparse(url).hostname, wait)
                time.sleep(min(wait, 120))
                continue
            if r.status_code >= 400:
                log.warning("HTTP %s %s %s: %s", r.status_code, method, url, r.text[:300])
                return None
            self._save(method, url, kw, r)
            return r
        log.error("Giving up on %s %s", method, url)
        return None

    def _save(self, method, url, kw, r):
        if not self.cache_dir:
            return
        key = hashlib.sha1((method + url + json.dumps(kw.get("json"), sort_keys=True, default=str)).encode()).hexdigest()[:16]
        host = (urlparse(url).hostname or "x").replace(".", "_")
        ext = "json" if "json" in r.headers.get("Content-Type", "") else "bin"
        with open(os.path.join(self.cache_dir, f"{host}_{key}.{ext}"), "wb") as f:
            f.write(r.content)

    def json(self, method: str, url: str, **kw) -> Any:
        r = self.request(method, url, **kw)
        if r is None:
            return None
        try:
            return r.json()
        except ValueError:
            log.warning("Not JSON: %s", url)
            return None


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def dig(obj: Any, path: str, default=None):
    """dig(d, 'a.b.0.c') -> d['a']['b'][0]['c'] or default."""
    cur = obj
    for part in path.split("."):
        if cur is None:
            return default
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return default
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return default
    return default if cur is None else cur


def first(obj: Any, paths: Iterable[str]):
    for p in paths:
        v = dig(obj, p)
        if v not in (None, "", [], {}):
            return v
    return None


def find_key(obj: Any, key: str):
    """Depth-first search for the first value under `key` (used for unverified schemas)."""
    if isinstance(obj, dict):
        if key in obj and obj[key] not in (None, "", [], {}):
            return obj[key]
        for v in obj.values():
            r = find_key(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, key)
            if r is not None:
                return r
    return None


def digits(s: str | None) -> str:
    return re.sub(r"\D", "", s or "")


_LEGAL_FORMS = ("the|inc|incorporated|corp|corporation|co|company|plc|ltd|limited|public limited company|llc|lp|sa|ag|se|"
                "nv|bv|spa|sca|sas|sgps|kgaa|gmbh|ab|abp|publ|asa|as|a s|oyj|oy|hf|nyrt|pjsc|"
                "aktiengesellschaft|aktiebolag|aktiebolaget|allmennaksjeselskap|aksjeselskap|osakeyhtio")
_SUFFIXES = rf"\b({_LEGAL_FORMS})\b"
# Trailing legal forms as written in names ("S.p.A.", "N.V.", "A/S", "(publ)"), stripped to build a search term
_TRAILING_FORM = re.compile(rf"[\s,]*\(?\b({_LEGAL_FORMS.replace('a s', 'a/s')}|s\.?p\.?a|n\.?v|s\.?a|b\.?v|p\.?l\.?c)\.?\)?\s*$", re.I)
US_STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY "
                "NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR".split())


def _ascii(s: str | None) -> str:
    """Lower-case ASCII transliteration: "Mærsk" -> "maersk", "Møller" -> "moller", "Göta" -> "gota"."""
    s = (s or "").lower().translate(str.maketrans({"æ": "ae", "ø": "o", "ß": "ss", "œ": "oe", "đ": "d", "ł": "l"}))
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def name_key(s: str | None) -> str:
    """Company name normalised for exact matching: case, accents, punctuation and legal-form suffixes ignored."""
    s = re.sub(r"[^a-z0-9 ]", " ", _ascii(s).replace(".", "").replace("&", " and "))
    return " ".join(re.sub(_SUFFIXES, " ", s).split())


_FORM_FAMILY = {"plc": "plc", "public limited company": "plc", "ltd": "ltd", "limited": "ltd",
                "inc": "inc", "incorporated": "inc", "corp": "inc", "corporation": "inc", "llc": "llc", "lp": "lp",
                "ag": "ag", "se": "ag", "sa": "sa", "spa": "spa", "nv": "nv", "bv": "bv", "sca": "sca", "sas": "sas",
                "sgps": "sgps", "kgaa": "kgaa", "gmbh": "gmbh", "ab": "ab", "publ": "ab", "asa": "asa", "as": "as",
                "a s": "as", "oyj": "oy", "oy": "oy", "abp": "oy", "hf": "hf", "nyrt": "nyrt", "pjsc": "pjsc",
                "aktiengesellschaft": "ag", "aktiebolag": "ab", "aktiebolaget": "ab",
                "allmennaksjeselskap": "asa", "aksjeselskap": "as", "osakeyhtio": "oy"}


def legal_form(name: str | None) -> str:
    """Family of the trailing legal form ("Krones AG" -> "ag", "CRH Ltd" -> "ltd"), or "" if none.
    AG and SE count as one family (companies convert between them)."""
    s = re.sub(r"[^a-z0-9 ]", " ", _ascii(name).replace(".", "").replace("/", " "))
    words = s.split()
    for n in (3, 2, 1):   # longest trailing form first ("public limited company", "a s")
        tail = " ".join(words[-n:]) if len(words) > n else ""
        if tail in _FORM_FAMILY:
            return _FORM_FAMILY[tail]
    return ""


def same_company(wanted: str | None, found: str | None) -> bool:
    """Exact normalised-name match; when both names carry a legal form, the forms must agree
    (so "Krones AG" never matches "Krones, Inc." and "CRH plc" never matches "CRH Corporation Limited")."""
    fw, ff = legal_form(wanted), legal_form(found)
    return bool(name_key(wanted)) and name_key(wanted) == name_key(found) and (not fw or not ff or fw == ff)


def search_core(name: str | None) -> str:
    """Name with trailing legal forms removed, for register name searches ("Acea SpA" -> "Acea")."""
    s, prev = (name or "").strip(), None
    while s and s != prev:
        prev, s = s, _TRAILING_FORM.sub("", s).strip()
    return s or (name or "").strip()


# --------------------------------------------------------------------------- #
# XBRL / iXBRL parsing (stdlib only)
# --------------------------------------------------------------------------- #
def _num(text: str, fmt: str = "", scale: str | None = None, sign: str | None = None) -> float | None:
    t = (text or "").strip().replace(" ", " ")
    if t in ("", "-", "–", "—") or "zerodash" in fmt or "fixed-zero" in fmt:
        return 0.0
    if "commadecimal" in fmt or "comma-decimal" in fmt:
        t = t.replace(".", "").replace(" ", "").replace(",", ".")
    else:
        t = t.replace(",", "").replace(" ", "")
    t = re.sub(r"[^\d.\-]", "", t)
    if not t or t in ("-", "."):
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    if scale:
        try:
            v *= 10 ** int(scale)
        except ValueError:
            pass
    if sign == "-":
        v = -v
    return v


class _IxParser(HTMLParser):
    """Collects ix:nonFraction facts and xbrli contexts from an iXBRL (XHTML) document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.facts: list[dict] = []
        self.ctx: dict[str, dict] = {}
        self._fact: dict | None = None
        self._depth = 0
        self._cur_ctx: str | None = None
        self._ctx_field: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag.endswith("nonfraction"):
            self._fact = {"name": a.get("name", ""), "context": a.get("contextref", ""), "scale": a.get("scale"),
                          "sign": a.get("sign"), "format": a.get("format", ""), "unit": a.get("unitref", ""), "text": ""}
            self._depth = 1
        elif self._fact is not None:
            self._depth += 1
        if tag.endswith(":context") or tag == "context":
            self._cur_ctx = a.get("id")
            self.ctx[self._cur_ctx] = {"end": None, "dims": False}
        elif self._cur_ctx:
            if tag.endswith("enddate") or tag.endswith("instant"):
                self._ctx_field = "end"
            elif tag.endswith("explicitmember") or tag.endswith("typedmember"):
                self.ctx[self._cur_ctx]["dims"] = True

    def handle_endtag(self, tag):
        if self._fact is not None:
            self._depth -= 1
            if self._depth <= 0:
                self.facts.append(self._fact)
                self._fact = None
        if tag.endswith(":context") or tag == "context":
            self._cur_ctx = None
        self._ctx_field = None

    def handle_data(self, data):
        if self._fact is not None:
            self._fact["text"] += data
        if self._cur_ctx and self._ctx_field == "end":
            self.ctx[self._cur_ctx]["end"] = (self.ctx[self._cur_ctx]["end"] or "") + data.strip()


def parse_ixbrl(html: str) -> list[dict]:
    p = _IxParser()
    p.feed(html)
    out = []
    for f in p.facts:
        c = p.ctx.get(f["context"], {})
        out.append({"name": f["name"], "local": f["name"].split(":")[-1], "value": _num(f["text"], f["format"], f["scale"], f["sign"]),
                    "end": c.get("end"), "dims": c.get("dims", False), "unit": f["unit"]})
    return out


def parse_xbrl_instance(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    ctx = {}
    for c in root.iter():
        if c.tag.endswith("}context"):
            end = None
            dims = False
            for e in c.iter():
                if e.tag.endswith("}endDate") or e.tag.endswith("}instant"):
                    end = (e.text or "").strip()
                if e.tag.endswith("}explicitMember") or e.tag.endswith("}typedMember"):
                    dims = True
            ctx[c.get("id")] = {"end": end, "dims": dims}
    out = []
    for e in root.iter():
        ref = e.get("contextRef")
        if ref is None:
            continue
        local = e.tag.split("}")[-1]
        ns = e.tag[1:].split("}")[0] if e.tag.startswith("{") else ""
        c = ctx.get(ref, {})
        out.append({"name": f"{ns}:{local}", "local": local, "value": _num(e.text or "", "", None, None),
                    "end": c.get("end"), "dims": c.get("dims", False), "unit": e.get("unitRef", "")})
    return out


def pick(facts: list[dict], names: list[str]) -> tuple[float | None, str | None, str | None]:
    """Latest non-dimensional fact matching any local name (in priority order)."""
    lower = [n.lower() for n in names]
    for n in lower:
        cands = [f for f in facts if f["local"].lower() == n and not f["dims"] and f["value"] is not None]
        if cands:
            best = max(cands, key=lambda f: f["end"] or "")
            return best["value"], best["end"], best["name"]
    return None, None, None


# --------------------------------------------------------------------------- #
# Collector
# --------------------------------------------------------------------------- #
class Collector:
    def __init__(self, http: Http, sources: set[str] | None):
        self.http = http
        self.sources = sources
        self.rows: list[dict] = []
        self.errors: list[dict] = []
        self.co: dict = {}
        self._bolag_token: tuple[str, float] | None = None
        self._sec_tickers: dict | None = None
        self.ch_key = os.getenv("CH_API_KEY")
        self.cvr_auth = (os.getenv("CVR_USER"), os.getenv("CVR_PASSWORD")) if os.getenv("CVR_USER") else None
        self.bolag_ok = bool(os.getenv("BOLAG_CLIENT_ID") and os.getenv("BOLAG_CLIENT_SECRET"))
        self.skips: dict[str, list[str]] = {}   # company_id -> sources skipped, and why
        self._named: set[str] = set()           # company_ids with a legal name found

    # ---- output
    def add(self, dp: str, value, source: str, endpoint: str, *, unit: str = "", period_end: str | None = None,
            method: str = "API", confidence: str = "", note: str = ""):
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        if dp == "Legal name" and value not in (None, ""):
            self._named.add(self.co["company_id"])
        self.rows.append({
            "company_id": self.co["company_id"], "company_name": self.co.get("name", ""), "segment": self.co["segment"],
            "country": self.co["country"], "lei": self.co.get("lei", ""), "data_point": dp,
            "value": "" if value is None else value, "unit": unit,
            "period_end": period_end or "", "source": source, "endpoint": endpoint, "method": method,
            "retrieved_at": now(), "confidence": confidence, "note": note if value not in (None, "") else (note or "not found")})

    def on(self, name: str) -> bool:
        return self.sources is None or name in self.sources

    def run(self, co: dict):
        self.co = co
        cid, seg, cc = co["company_id"], co["segment"], co["country"]
        # Can a national register supply identity for a private company in this country?
        register_ok = {"GB": bool(self.ch_key), "FI": True, "NO": True, "SE": self.bolag_ok, "DK": bool(self.cvr_auth)}.get(cc, False)
        steps = []
        if seg in ("NL", "EU", "OP"):
            steps.append(("gleif", lambda: self.gleif(emit=True)))
        elif seg == "NP":   # GLEIF fills the ID gap; it supplies identity only when no register can
            steps.append(("gleif", lambda: self.gleif(emit=not register_ok)))
        if seg == "US":
            steps.append(("sec", self.sec))
        if cc == "GB" and seg in ("EU", "NP"):
            steps.append(("ch", self.companies_house))
        if seg in ("NL", "NP"):
            steps += {"FI": [("prh", self.prh)], "NO": [("brreg", self.brreg)],
                      "SE": [("bolag", self.bolagsverket)], "DK": [("cvr", self.cvr)]}.get(cc, [])
        unavailable = {"ch": None if self.ch_key else "Companies House skipped: no API key",
                       "bolag": None if self.bolag_ok else "Bolagsverket skipped: no credentials",
                       "cvr": None if self.cvr_auth else "CVR skipped: no credentials"}
        self.skips[cid] = []
        for name, fn in steps:
            if not self.on(name):
                continue
            if unavailable.get(name):
                self.skips[cid].append(unavailable[name])
                continue
            self._call(name, fn)
        # Fallback: nothing identified the company (e.g. no SEC match, register skipped) -> GLEIF by LEI or exact name
        if cid not in self._named and self.on("gleif"):
            self._call("gleif", lambda: self.gleif(emit=True))

    def _call(self, name, fn):
        try:
            fn()
        except Exception as e:  # keep going with the next source / company
            log.exception("%s failed for %s", name, self.co["company_id"])
            self.errors.append({"company_id": self.co["company_id"], "source": name, "error": repr(e)})

    # ======================================================================= #
    # GLEIF  (GLEIF API.postman_collection.json)
    # ======================================================================= #
    def _lei_by_name(self) -> str | None:
        """LEI for the company name, accepted only on an exact normalised-name match that is unambiguous."""
        co = self.co
        if not name_key(co.get("name")):
            return None

        def same(x):
            return same_company(co["name"], dig(x, "attributes.entity.legalName.name"))

        cands = []
        for params in ({"filter[entity.legalName]": search_core(co["name"]), "page[size]": 50},
                       {"filter[fulltext]": co["name"], "page[size]": 50}):
            d = self.http.json("GET", f"{GLEIF}/lei-records", params=params) or {}
            cands = [x for x in d.get("data", []) if same(x)]
            if cands:
                break
        if not cands:
            return None
        active = [x for x in cands if dig(x, "attributes.entity.status") == "ACTIVE"] or cands
        if len({x["attributes"]["lei"] for x in active}) > 1:
            same_cc = [x for x in active if dig(x, "attributes.entity.legalAddress.country") == co.get("country")]
            if len({x["attributes"]["lei"] for x in same_cc}) != 1:
                log.info("%s: %d GLEIF records match %r exactly - skipped as ambiguous", co["company_id"], len(active), co["name"])
                return None
            active = same_cc
        return active[0]["attributes"]["lei"]

    def gleif(self, emit: bool = True):
        co = self.co
        if "_gleif" not in co:   # look the company up once; later calls only decide whether to emit
            co["_gleif"] = None
            lei, how = co.get("lei"), "input"
            if not lei and co.get("isin"):
                d = self.http.json("GET", f"{GLEIF}/lei-records", params={"filter[isin]": co["isin"]})
                lei, how = dig(d, "data.0.attributes.lei"), "ISIN"
            if not lei and co.get("national_id"):
                d = self.http.json("GET", f"{GLEIF}/lei-records", params={
                    "filter[entity.registeredAs]": co["national_id"], "filter[entity.legalAddress.country]": co["country"]})
                lei, how = dig(d, "data.0.attributes.lei"), "registration ID"
            if not lei and co.get("name"):
                lei, how = self._lei_by_name(), "exact name match"
            if not lei:
                log.info("%s: no LEI found", co["company_id"])
                return
            co["lei"] = lei
            ep = f"{GLEIF}/lei-records/{lei}"
            e = dig(self.http.json("GET", ep), "data.attributes.entity") or {}
            co["_gleif"] = (ep, e, how)
            if not co.get("national_id") and e.get("registeredAs"):
                co["national_id"] = e["registeredAs"]
        if not emit or not co["_gleif"] or co.get("_gleif_emitted"):
            return
        co["_gleif_emitted"] = True
        ep, e, how = co["_gleif"]
        src, conf = "GLEIF", "confirmed in collection"
        via = "" if how == "input" else f"; LEI via {how}"
        self.add("Legal name", dig(e, "legalName.name"), src, ep, confidence=conf, note=via.lstrip("; "))
        self.add("Country", dig(e, "legalAddress.country"), src, ep, confidence=conf, note=f"jurisdiction {e.get('jurisdiction')}{via}")
        self.add("Registration ID", e.get("registeredAs"), src, ep, confidence=conf, note=f"register {dig(e, 'registeredAt.id')}{via}")
        self.add("Head-office city", dig(e, "headquartersAddress.city"), src, ep, confidence=conf, note=via.lstrip("; "))

    # ======================================================================= #
    # Companies House  (companies_house.json + Document API)
    # ======================================================================= #
    def companies_house(self):
        if not self.ch_key:
            log.warning("CH_API_KEY not set – skipping Companies House")
            return
        co, auth = self.co, (self.ch_key, "")
        num = (co.get("national_id") or "").strip().upper()
        if not num and co.get("name"):
            d = self.http.json("GET", f"{CH}/search/companies", params={"q": co["name"], "items_per_page": 20}, auth=auth)
            # Exact name only: the top hit is often a subsidiary or namesake with a similar name.
            num = next((i.get("company_number") for i in (d or {}).get("items", []) if same_company(co["name"], i.get("title"))), "")
            if not num:
                log.info("%s: no exact Companies House name match for %r", co["company_id"], co["name"])
        if not num:
            return
        num = num.zfill(8) if num.isdigit() else num
        src = "Companies House"
        ep = f"{CH}/company/{num}"
        p = self.http.json("GET", ep, auth=auth) or {}
        juris = p.get("jurisdiction")
        if co["segment"] in ("EU", "NP"):
            self.add("Legal name", p.get("company_name"), src, ep)
            self.add("Country", "GB" if juris in ("england-wales", "wales", "england", "scotland", "northern-ireland", "united-kingdom") else juris,
                     src, ep, note=f"jurisdiction {juris}")
            self.add("Registration ID", p.get("company_number"), src, ep)
        if co["segment"] == "NP":
            self.add("Sector (NACE / SIC)", ";".join(p.get("sic_codes") or []) or None, src, ep, unit="UK SIC 2007")
            self.add("Head-office city", dig(p, "registered_office_address.locality"), src, ep, note="registered office")
            self._ch_psc(num, auth)
            self._ch_accounts(num, auth)

    def _ch_psc(self, num, auth):
        ep = f"{CH}/company/{num}/persons-with-significant-control"
        d = self.http.json("GET", ep, auth=auth, params={"items_per_page": 100}) or {}
        active = [i for i in d.get("items", []) if not i.get("ceased_on")]

        def band(i):
            m = [re.search(r"(\d+)-to-(\d+)-percent", n) for n in i.get("natures_of_control", [])]
            m = [x for x in m if x]
            return max((int(x.group(1)) for x in m), default=0)

        top = max(active, key=band, default=None)
        if top:
            self.add("Controlling owner", top.get("name"), "Companies House PSC", ep,
                     note=f"kind={top.get('kind')}; control={','.join(top.get('natures_of_control', []))}")
        else:
            self.add("Controlling owner", None, "Companies House PSC", ep)
        corp = [i for i in active if "corporate" in (i.get("kind") or "") or "legal-person" in (i.get("kind") or "")]
        self.add("PE stake of 5% or more", "; ".join(f"{i.get('name')} ({band(i)}%+)" for i in corp) or None,
                 "Companies House PSC", ep, confidence="needs PE classification",
                 note="corporate PSCs only; bands start at 25%, so 5–25% stakes are not visible")

    def _ch_accounts(self, num, auth):
        ep = f"{CH}/company/{num}/filing-history"
        d = self.http.json("GET", ep, auth=auth, params={"category": "accounts", "items_per_page": 10}) or {}
        for item in d.get("items", []):
            meta_url = dig(item, "links.document_metadata")
            if not meta_url:
                continue
            meta = self.http.json("GET", meta_url, auth=auth) or {}
            if "application/xhtml+xml" not in (meta.get("resources") or {}):
                continue  # PDF-only filing; try an older one
            content_url = dig(meta, "links.document") or meta_url.rstrip("/") + "/content"
            r = self.http.request("GET", content_url, auth=auth, headers={"Accept": "application/xhtml+xml"})
            if r is None:
                continue
            facts = parse_ixbrl(r.text)
            src, ep2, m = "Companies House accounts (iXBRL)", content_url, "API+XBRL"
            v, end, tag = pick(facts, TAGS["uk_revenue"])
            self.add("Revenue", v, src, ep2, unit="GBP", period_end=end, method=m, note=tag or "small companies often omit P&L")
            v, end, tag = pick(facts, TAGS["uk_total_assets"])
            if v is None:
                fa, end1, _ = pick(facts, TAGS["uk_fixed"])
                ca, end2, _ = pick(facts, TAGS["uk_current"])
                if fa is not None or ca is not None:
                    v, end, tag = (fa or 0) + (ca or 0), end1 or end2, "FixedAssets + CurrentAssets"
            self.add("Total assets", v, src, ep2, unit="GBP", period_end=end, method=m, note=tag or "")
            v, end, tag = pick(facts, TAGS["uk_employees"])
            self.add("Employees (FTE)", v, src, ep2, period_end=end, method=m, note="average number employed")
            return
        for dp in ("Revenue", "Total assets", "Employees (FTE)"):
            self.add(dp, None, "Companies House accounts (iXBRL)", ep, note="no iXBRL accounts in last 10 filings")

    # ======================================================================= #
    # PRH  (prh_ytj_api_endpoints.json, prh_xbrl_api_endpoints.json)
    # ======================================================================= #
    def prh(self):
        co = self.co
        bid = co.get("national_id")
        params = {"businessId": bid} if bid else {"name": co.get("name")}
        ep = f"{YTJ}/companies"
        d = self.http.json("GET", ep, params=params) or {}
        c = dig(d, "companies.0")
        if not c:
            return
        bid = dig(c, "businessId.value")
        src, conf, url = "PRH YTJ", "confirmed in collection", f"{ep}?businessId={bid}"
        names = [n for n in c.get("names", []) if str(n.get("type")) == "1" and n.get("version") == 1]
        self.add("Legal name", (names[0] if names else (c.get("names") or [{}])[0]).get("name"), src, url, confidence=conf)
        self.add("Country", "FI", src, url, confidence=conf, note="Finnish trade register")
        self.add("Registration ID", bid, src, url, confidence=conf)
        mbl = c.get("mainBusinessLine") or {}
        desc = next((x.get("description") for x in mbl.get("descriptions", []) if str(x.get("languageCode")) == "3"), None)
        self.add("Sector (NACE / SIC)", mbl.get("type"), src, url, confidence=conf, unit="TOL 2008", note=desc or "")
        city = None
        for a in c.get("addresses", []):
            if a.get("type") == 1:
                city = next((p.get("city") for p in a.get("postOffices", []) if str(p.get("languageCode")) == "1"), None) \
                       or dig(a, "postOffices.0.city")
                break
        self.add("Head-office city", city, src, url, confidence=conf)
        if co["segment"] == "NP":
            self._prh_xbrl(bid)

    def _prh_xbrl(self, bid):
        ep = f"{PRHX}/financials"
        d = self.http.json("GET", ep, params={"businessId": bid}) or {}
        dates = sorted((f.get("financialDate") for f in d.get("financials", []) if f.get("financialDate")), reverse=True)
        src = "PRH XBRL"
        if not dates:
            for dp in ("Revenue", "Total assets", "Employees (FTE)"):
                self.add(dp, None, src, f"{ep}?businessId={bid}", note="no iXBRL statement filed (~5% of filers have one)")
            return
        url = f"{PRHX}/financial"
        r = self.http.request("GET", url, params={"businessId": bid, "financialDate": dates[0]})
        if r is None:
            return
        facts = parse_xbrl_instance(r.content)
        full = f"{url}?businessId={bid}&financialDate={dates[0]}"
        for dp, key, unit in (("Revenue", "fi_revenue", "EUR"), ("Total assets", "fi_assets", "EUR"), ("Employees (FTE)", "fi_employees", "")):
            v, end, tag = pick(facts, TAGS[key])
            self.add(dp, v, src, full, unit=unit, period_end=end or dates[0], method="API+XBRL",
                     confidence="verify tag name", note=tag or "tag not matched – run --dump-tags")

    # ======================================================================= #
    # SEC EDGAR  (data.sec.gov – not in collection)
    # ======================================================================= #
    def _cik(self) -> str | None:
        co = self.co
        if co.get("cik"):
            return digits(co["cik"]).zfill(10)
        if self._sec_tickers is None:
            d = self.http.json("GET", f"{SEC_WWW}/files/company_tickers_exchange.json") or {}
            fields = d.get("fields", [])
            self._sec_tickers, names = {}, {}
            for row in d.get("data", []):
                rec = dict(zip(fields, row))
                if rec.get("ticker"):
                    self._sec_tickers[rec["ticker"].upper()] = rec
                names.setdefault(name_key(rec.get("name")), set()).add(rec["cik"])
            # Name -> CIK only where the normalised name is unique
            self._sec_names = {k: next(iter(v)) for k, v in names.items() if k and len(v) == 1}
        rec = self._sec_tickers.get((co.get("ticker") or "").upper())
        if rec:
            return str(rec["cik"]).zfill(10)
        cik = self._sec_names.get(name_key(co.get("name")))
        return str(cik).zfill(10) if cik else None

    def sec(self):
        cik = self._cik()
        if not cik:
            log.info("%s: no CIK", self.co["company_id"])
            return
        src = "SEC EDGAR submissions"
        ep = f"{SEC_DATA}/submissions/CIK{cik}.json"
        s = self.http.json("GET", ep) or {}
        self.add("Legal name", s.get("name"), src, ep)
        inc = s.get("stateOfIncorporation") or dig(s, "addresses.business.stateOrCountry")
        self.add("Country", "US" if inc in US_STATES else inc, src, ep,
                 note=f"incorporated in {inc}" if inc in US_STATES else "EDGAR country code of incorporation")
        self.add("Registration ID", int(cik), src, ep, unit="CIK")
        tickers, exch = s.get("tickers") or [], s.get("exchanges") or []
        self.add("Ticker", ";".join(tickers) or None, src, ep)
        self.add("Exchange", ";".join(e for e in exch if e) or None, src, ep)
        self.add("ISIN", None, src, ep, note="EDGAR has no ISIN; use GLEIF /lei-records/{lei}/isins")
        forms = dig(s, "filings.recent.form") or []
        delisted = any(f in ("25-NSE", "25", "15-12B", "15-12G") for f in forms[:50])
        status = "listed" if any(exch) and not delisted else ("delisting filed" if delisted else "not listed")
        self.add("Listing status", status, src, ep, note="from exchanges[] and recent 25-NSE / 15-12 forms")
        self.add("Listing segment", None, src, ep, note="EDGAR gives exchange only, not market tier – buy")
        self.add("Sector (NACE / SIC)", s.get("sic"), src, ep, unit="US SIC", note=s.get("sicDescription") or "")
        self.add("Head-office city", dig(s, "addresses.business.city"), src, ep)
        self._sec_concept(cik, "Revenue",
                          ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
                           "RevenueFromContractWithCustomerIncludingAssessedTax"], duration=True)
        self._sec_concept(cik, "Total assets", ["Assets"], duration=False)

    def _sec_concept(self, cik, dp, tags, duration):
        best = None
        for tag in tags:
            ep = f"{SEC_DATA}/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
            d = self.http.json("GET", ep)
            for f in dig(d, "units.USD") or []:
                if f.get("form") not in ("10-K", "10-K/A", "20-F", "40-F") or f.get("fp") != "FY":
                    continue
                if duration:
                    try:
                        days = (dt.date.fromisoformat(f["end"]) - dt.date.fromisoformat(f["start"])).days
                    except (KeyError, ValueError):
                        continue
                    if not 350 <= days <= 380:
                        continue
                key = (f["end"], f.get("filed", ""))
                if best is None or key > best[0]:
                    best = (key, f["val"], f["end"], tag, ep)
        if best:
            self.add(dp, best[1], "SEC EDGAR companyconcept", best[4], unit="USD", period_end=best[2],
                     method="API (XBRL)", note=f"us-gaap:{best[3]}")
        else:
            self.add(dp, None, "SEC EDGAR companyconcept", f"{SEC_DATA}/api/xbrl/companyconcept/CIK{cik}/us-gaap/…")

    # ======================================================================= #
    # Brønnøysund (NO)  – not in collection
    # ======================================================================= #
    def brreg(self):
        co = self.co
        org = digits(co.get("national_id"))
        if not org and co.get("name"):
            d = self.http.json("GET", f"{BRREG}/enheter", params={"navn": co["name"], "size": 1})
            org = dig(d, "_embedded.enheter.0.organisasjonsnummer") or ""
        if not org:
            return
        src, ep = "Brønnøysund Enhetsregisteret", f"{BRREG}/enheter/{org}"
        e = self.http.json("GET", ep) or {}
        self.add("Legal name", e.get("navn"), src, ep)
        self.add("Country", dig(e, "forretningsadresse.landkode") or "NO", src, ep)
        self.add("Registration ID", e.get("organisasjonsnummer"), src, ep)
        self.add("Sector (NACE / SIC)", dig(e, "naeringskode1.kode"), src, ep, unit="SN2007 (NACE)",
                 note=dig(e, "naeringskode1.beskrivelse") or "")
        self.add("Head-office city", first(e, ["forretningsadresse.poststed", "postadresse.poststed"]), src, ep)
        if co["segment"] == "NP":
            self.add("Employees (headcount)", e.get("antallAnsatte"), src, ep,
                     note="" if e.get("harRegistrertAntallAnsatte", True) else "no employees registered (0–4 not shown)")
            self.add("Employees (FTE)", None, src, ep, note="register gives headcount only")
            self._brreg_accounts(org)

    def _brreg_accounts(self, org):
        ep = f"{BRREG_R}/{org}"
        d = self.http.json("GET", ep)
        recs = d if isinstance(d, list) else ([d] if isinstance(d, dict) else [])
        # Latest year first; within a year prefer group (KONSERN) over parent-only (SELSKAP) accounts.
        r = max(recs, key=lambda x: (str(dig(x, "regnskapsperiode.tilDato") or ""), x.get("regnskapstype") == "KONSERN"), default={})
        end, cur = dig(r, "regnskapsperiode.tilDato"), r.get("valuta", "NOK")
        src, note = "Brønnøysund Regnskapsregisteret", f"{(r.get('regnskapstype') or '').lower() or 'unknown'} accounts"
        # Sales revenue (salgsinntekter), the golden pack's definition; total operating income only as a fallback.
        di = dig(r, "resultatregnskapResultat.driftsresultat.driftsinntekter") or {}
        rev = di.get("salgsinntekter")
        if rev is None and di.get("sumDriftsinntekter") is not None:
            rev, note = di["sumDriftsinntekter"], note + "; total operating income (no sales line)"
        self.add("Revenue", rev, src, ep, unit=cur, period_end=end, note=note)
        self.add("Total assets", dig(r, "eiendeler.sumEiendeler"), src, ep, unit=cur, period_end=end, note=note)

    # ======================================================================= #
    # Bolagsverket (SE)  – not in collection; field names to verify
    # ======================================================================= #
    def _bolag_headers(self) -> dict | None:
        cid, sec = os.getenv("BOLAG_CLIENT_ID"), os.getenv("BOLAG_CLIENT_SECRET")
        if not cid or not sec:
            log.warning("BOLAG_CLIENT_ID / BOLAG_CLIENT_SECRET not set – skipping Bolagsverket")
            return None
        if not self._bolag_token or self._bolag_token[1] < time.time() + 30:
            r = self.http.request("POST", BOLAG_TOKEN, data={"grant_type": "client_credentials", "client_id": cid,
                                                             "client_secret": sec, "scope": "vardefulla-datamangder:read"})
            if r is None:
                return None
            t = r.json()
            self._bolag_token = (t["access_token"], time.time() + int(t.get("expires_in", 3000)))
        return {"Authorization": f"Bearer {self._bolag_token[0]}", "Accept": "application/json"}

    def bolagsverket(self):
        h = self._bolag_headers()
        org = digits(self.co.get("national_id"))
        if not h or not org:
            return
        src, conf = "Bolagsverket", "verify field path"
        ep = f"{BOLAG_BASE}/organisationer"
        d = self.http.json("POST", ep, json={"identitetsbeteckning": org}, headers=h) or {}
        o = first(d, ["organisationer.0"]) or d
        name = first(o, ["organisationsnamn.organisationsnamnLista.0.namn", "organisationsnamn.namn", "organisationsnamn"])
        if isinstance(name, dict):
            name = find_key(name, "namn")
        self.add("Legal name", name, src, ep, confidence=conf)
        self.add("Country", "SE", src, ep, note="Swedish register")
        self.add("Registration ID", first(o, ["identitet.identitetsbeteckning", "organisationsidentitet.identitetsbeteckning"]) or org,
                 src, ep, confidence=conf)
        sni = first(o, ["naringsgrenOrganisation.sni.0.kod", "naringsgrenOrganisation.sni.0.code"]) or find_key(o.get("naringsgrenOrganisation", {}), "kod")
        self.add("Sector (NACE / SIC)", sni, src, ep, unit="SNI 2007 (NACE)", confidence=conf)
        city = first(o, ["postadressOrganisation.postadress.postort", "postadressOrganisation.postort"]) or find_key(o, "postort")
        self.add("Head-office city", city, src, ep, confidence=conf, note="postal address")
        if self.co["segment"] == "NP":
            self._bolag_docs(org, h)

    def _bolag_docs(self, org, h):
        ep = f"{BOLAG_BASE}/dokumentlista"
        d = self.http.json("POST", ep, json={"identitetsbeteckning": org}, headers=h) or {}
        docs = d.get("dokument") or find_key(d, "dokument") or []
        docs = sorted(docs, key=lambda x: str(x.get("rapporteringsperiodTom") or ""), reverse=True)
        src = "Bolagsverket annual report (iXBRL)"
        if not docs:
            for dp in ("Revenue", "Total assets", "Employees (FTE)"):
                self.add(dp, None, src, ep, note="no digital annual report")
            return
        doc_id = docs[0].get("dokumentId")
        url = f"{BOLAG_BASE}/dokument/{doc_id}"
        r = self.http.request("GET", url, headers={**h, "Accept": "application/zip"})
        if r is None:
            return
        facts = []
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for n in z.namelist():
                if n.lower().endswith((".xhtml", ".html", ".htm")):
                    facts += parse_ixbrl(z.read(n).decode("utf-8", "replace"))
        for dp, key, unit, note in (("Revenue", "se_revenue", "SEK", ""), ("Total assets", "se_assets", "SEK", ""),
                                    ("Employees (FTE)", "se_employees", "", "average number of employees")):
            v, end, tag = pick(facts, TAGS[key])
            self.add(dp, v, src, url, unit=unit, period_end=end or docs[0].get("rapporteringsperiodTom"),
                     method="API+XBRL", note=(tag or "") + ("; " + note if note else ""))

    # ======================================================================= #
    # CVR (DK)  – not in collection; nested field paths to verify
    # ======================================================================= #
    def _cvr_search(self, index: str, body: dict) -> list:
        url = f"{CVR}/{index}/_search"
        d = self.http.json("POST", url, json=body, auth=self.cvr_auth, headers={"Content-Type": "application/json"}) or {}
        return [h.get("_source", {}) for h in dig(d, "hits.hits") or []]

    def cvr(self):
        if not self.cvr_auth:
            log.warning("CVR_USER / CVR_PASSWORD not set – skipping CVR")
            return
        cvr = digits(self.co.get("national_id"))
        if not cvr:
            return
        url = f"{CVR}/cvr-permanent/virksomhed/_search"
        hits = self._cvr_search("cvr-permanent/virksomhed", {"query": {"term": {"Vrvirksomhed.cvrNummer": int(cvr)}}})
        v = dig(hits, "0.Vrvirksomhed") or {}
        m = v.get("virksomhedMetadata") or {}
        src = "CVR"
        self.add("Legal name", dig(m, "nyesteNavn.navn"), src, url)
        self.add("Country", dig(m, "nyesteBeliggenhedsadresse.landekode") or "DK", src, url)
        self.add("Registration ID", v.get("cvrNummer"), src, url)
        self.add("Sector (NACE / SIC)", dig(m, "nyesteHovedbranche.branchekode"), src, url, unit="DB07 (NACE)",
                 note=dig(m, "nyesteHovedbranche.branchetekst") or "")
        self.add("Head-office city", first(m, ["nyesteBeliggenhedsadresse.postdistrikt", "nyesteBeliggenhedsadresse.bynavn"]), src, url)
        if self.co["segment"] != "NP":
            return
        # employees
        aar = sorted(v.get("aarsbeskaeftigelse") or [], key=lambda x: x.get("aar") or 0, reverse=True)
        a = aar[0] if aar else {}
        self.add("Employees (FTE)", first(a, ["antalAarsvaerk"]), src, url, period_end=str(a.get("aar") or ""),
                 confidence="verify field path", note=a.get("intervalKodeAntalAarsvaerk") or "")
        self.add("Employees (headcount)", first(a, ["antalAnsatte"]), src, url, period_end=str(a.get("aar") or ""),
                 confidence="verify field path", note=a.get("intervalKodeAntalAnsatte") or "")
        self._cvr_owners(v, url)
        self._cvr_accounts(cvr)

    def _cvr_owners(self, v, url):
        owners = []
        for rel in v.get("deltagerRelation") or []:
            pct = None
            for org in rel.get("organisationer") or []:
                for md in org.get("medlemsData") or []:
                    for at in md.get("attributter") or []:
                        if at.get("type") == "EJERANDEL_PROCENT":
                            cur = [x for x in at.get("vaerdier") or [] if not dig(x, "periode.gyldigTil")]
                            if cur:
                                try:
                                    pct = float(cur[-1]["vaerdi"])
                                except (ValueError, KeyError):
                                    pass
            if pct is None:
                continue
            pct = pct * 100 if pct <= 1 else pct
            d = rel.get("deltager") or {}
            name = (d.get("navne") or [{}])[-1].get("navn")
            if not name and d.get("enhedsNummer"):
                h = self._cvr_search("cvr-permanent/deltager", {"query": {"term": {"Vrdeltager.enhedsNummer": d["enhedsNummer"]}}})
                name = ((dig(h, "0.Vrdeltager.navne") or [{}])[-1]).get("navn")
            owners.append((pct, name or str(d.get("enhedsNummer")), d.get("enhedstype")))
        owners.sort(reverse=True)
        if owners:
            p, n, t = owners[0]
            self.add("Controlling owner", n, "CVR owners", url, confidence="verify field path",
                     note=f"{p:.1f}% ({t})")
        else:
            self.add("Controlling owner", None, "CVR owners", url)
        corp = [o for o in owners if o[0] >= 5 and (o[2] or "").upper() != "PERSON"]
        self.add("PE stake of 5% or more", "; ".join(f"{n} ({p:.1f}%)" for p, n, _ in corp) or None, "CVR owners", url,
                 confidence="needs PE classification", note="non-person owners with ≥5%")

    def _cvr_accounts(self, cvr):
        url = f"{CVR}/offentliggoerelser/_search"
        hits = self._cvr_search("offentliggoerelser", {"size": 20, "query": {"term": {"cvrNummer": int(cvr)}}})
        hits.sort(key=lambda h: str(dig(h, "regnskab.regnskabsperiode.slutDato") or ""), reverse=True)
        src = "CVR annual report (XBRL)"
        for h in hits:
            xml = next((x for x in h.get("dokumenter") or []
                        if "xml" in (x.get("dokumentMimeType") or "").lower() and x.get("dokumentUrl")), None)
            if not xml:
                continue
            r = self.http.request("GET", xml["dokumentUrl"])
            if r is None:
                continue
            facts = parse_xbrl_instance(r.content)
            end = dig(h, "regnskab.regnskabsperiode.slutDato")
            v, e, tag = pick(facts, TAGS["dk_revenue"])
            if v is None:
                v, e, tag = pick(facts, TAGS["dk_gross_profit"])
                tag = f"{tag} (gross profit – revenue not disclosed)" if tag else None
            self.add("Revenue", v, src, xml["dokumentUrl"], unit="DKK", period_end=e or end, method="API+XBRL", note=tag or "")
            v, e, tag = pick(facts, TAGS["dk_assets"])
            self.add("Total assets", v, src, xml["dokumentUrl"], unit="DKK", period_end=e or end, method="API+XBRL", note=tag or "")
            return
        for dp in ("Revenue", "Total assets"):
            self.add(dp, None, src, url, note="no XBRL annual report found")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def read_companies(path: str) -> list[dict]:
    out = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.DictReader(f), 2):
            row = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
            seg = SEGMENTS.get(row.get("segment", "").upper())
            if not row.get("company_id") or not seg:
                log.warning("line %d skipped: need company_id and a valid segment (NL/EU/US/NP/OP)", i)
                continue
            row["segment"] = seg
            row["country"] = (row.get("country") or ("US" if seg == "US" else "")).upper().replace("UK", "GB")
            out.append(row)
    return out


def dump_tags(path: str) -> None:
    data = open(path, "rb").read()
    facts = parse_xbrl_instance(data) if data.lstrip()[:5] in (b"<?xml", b"<xbrl") and b"ix:" not in data[:5000] \
        else parse_ixbrl(data.decode("utf-8", "replace"))
    for f in sorted(facts, key=lambda f: f["name"]):
        if not f["dims"]:
            print(f"{f['name']:<70} {f['end'] or '':<12} {f['value']}")


def complete_grid(rows: list[dict], companies: list[dict], skips: dict[str, list[str]]) -> list[dict]:
    """One row per company x mapped data point. Found values are kept as-is (one row per source);
    a data point with no value gets a single row with value "null" and the reason in `note`."""
    by = {}
    for r in rows:
        by.setdefault((r["company_id"], r["data_point"]), []).append(r)
    found_any = {r["company_id"] for r in rows if r["value"] != ""}
    out = []
    for co in companies:
        cid = co["company_id"]
        skipped = skips.get(cid, [])
        for dp in DATA_POINTS + sorted({k[1] for k in by if k[0] == cid} - set(DATA_POINTS)):
            rs = by.get((cid, dp), [])
            vals = [r for r in rs if r["value"] != ""]
            if vals:
                out += vals
                continue
            if co["segment"] not in DP_SEGMENTS.get(dp, _IDENTITY):
                reason = f"no source in the mapping for {SEGMENT_NAMES[co['segment']]}"
            elif cid not in found_any:
                reason = "; ".join(["company not identified: no LEI or registration ID, and no exact name match in GLEIF/SEC"] + skipped)
            else:
                reason = "; ".join(dict.fromkeys([r["note"] for r in rs if r["note"]] + skipped)) or "not found in source"
            base = rs[0] if rs else {}
            out.append({
                "company_id": cid, "company_name": co.get("name", ""), "segment": co["segment"], "country": co["country"],
                "lei": co.get("lei", ""), "data_point": dp, "value": NULL, "unit": "", "period_end": "",
                "source": "; ".join(dict.fromkeys(r["source"] for r in rs)), "endpoint": base.get("endpoint", ""),
                "method": base.get("method", ""), "retrieved_at": base.get("retrieved_at") or now(),
                "confidence": "", "note": reason})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="companies CSV")
    ap.add_argument("-o", "--output", default="results.csv")
    ap.add_argument("--sources", help="comma list: gleif,ch,prh,sec,brreg,bolag,cvr (default all)")
    ap.add_argument("--cache", help="folder to keep raw responses (for the verify step)")
    ap.add_argument("--dump-tags", metavar="FILE", help="print XBRL/iXBRL tags in FILE and exit")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if a.dump_tags:
        dump_tags(a.dump_tags)
        return 0
    if not a.input:
        ap.error("input CSV is required")
    if not os.getenv("SEC_USER_AGENT"):
        log.warning("SEC_USER_AGENT not set – SEC requires a contact User-Agent and may block requests")

    companies = read_companies(a.input)
    col = Collector(Http(a.cache), set(a.sources.split(",")) if a.sources else None)
    for n, co in enumerate(companies, 1):
        log.info("[%d/%d] %s %s (%s, %s)", n, len(companies), co["company_id"], co.get("name", ""), co["segment"], co["country"])
        col.run(co)

    rows = complete_grid(col.rows, companies, col.skips)
    with open(a.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        w.writeheader()
        w.writerows(rows)
    if col.errors:
        err = os.path.splitext(a.output)[0] + "_errors.csv"
        with open(err, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["company_id", "source", "error"])
            w.writeheader()
            w.writerows(col.errors)
        log.warning("%d source errors written to %s", len(col.errors), err)
    found = sum(1 for r in rows if r["value"] != NULL)
    log.info("Wrote %d rows (%d with a value, %d null) to %s", len(rows), found, len(rows) - found, a.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
