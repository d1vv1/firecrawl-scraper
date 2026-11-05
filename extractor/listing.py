"""Exchange data points from free official lists (no scraping, no AI):

- ESMA FIRDS: every share traded on an EU/EEA venue, by the issuer's LEI. Gives the
  ISIN, the venues, whether the issuer asked for the listing, and trading dates.
- ISO 10383 (MIC list): venue names, the exchange each segment belongs to, and
  whether a venue is a regulated market or an MTF.
- OpenFIGI: the ticker on a given exchange (Bloomberg style: "NOVOB" for "NOVO B").
  Works without a key (25 requests a minute); OPENFIGI_API_KEY in .env raises that.

UK and Swiss venues are not in FIRDS (the UK left at the end of 2020: London records
end on 2020-12-31), so for GB/CH companies the home exchange comes from OpenFIGI.

FIRDS trading start dates are not admission dates: old listings carry system dates
(1900-01-01, the MiFID start dates) and a new ISIN after a share change looks like a
new listing. They are only used for recent listings, and graded C.
"""

import csv
import datetime as dt
import io
import json
import logging
import os
import re
import time
import unicodedata

import httpx

from .apis import Found, _cached, retrieved_at
from .config import CACHE_DIR

log = logging.getLogger(__name__)

FIRDS = "https://registers.esma.europa.eu/solr/esma_registers_firds/select"
MIC_LIST = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv"
OPENFIGI = "https://api.openfigi.com/v3/mapping"
MIC_CACHE_DAYS = 30
TIMEOUT_S = 60

# Not in FIRDS: the home exchange's operating MIC, for OpenFIGI.
NON_EU_HOME = {"GB": "XLON", "CH": "XSWX"}
# Operating MIC -> Bloomberg exchange code, as OpenFIGI uses it.
BLOOMBERG_EXCH = {
    "XLON": "LN", "XSWX": "SW", "XSTO": "SS", "XCSE": "DC", "XHEL": "FH", "XOSL": "NO",
    "XICE": "IR", "XAMS": "NA", "XBRU": "BB", "XPAR": "FP", "XLIS": "PL", "XMAD": "SM",
    "XMIL": "IM", "XETR": "GY", "XFRA": "GF", "XWBO": "AV", "XATH": "GA", "XLUX": "LX",
    "XDUB": "ID", "XWAR": "PW", "XPRA": "CP", "XBUD": "HB", "XTAL": "ET", "XRIS": "LR",
    "XLIT": "LH", "XCYS": "CY", "XMAL": "MV", "XBUL": "BU", "XBSE": "RO", "XZAG": "ZA",
    "XLJU": "SV",
}
FRIENDLY = {"XLON": "London Stock Exchange", "XSWX": "SIX Swiss Exchange",
            "XSTO": "Nasdaq Stockholm", "XCSE": "Nasdaq Copenhagen", "XHEL": "Nasdaq Helsinki",
            "XICE": "Nasdaq Iceland", "XOSL": "Oslo Børs", "XETR": "Xetra (Deutsche Börse)",
            "XFRA": "Frankfurt Stock Exchange", "XWBO": "Wiener Börse", "XMAD": "Bolsa de Madrid",
            "XATH": "Athens Stock Exchange", "XLUX": "Luxembourg Stock Exchange",
            "XAMS": "Euronext Amsterdam", "XBRU": "Euronext Brussels", "XPAR": "Euronext Paris",
            "XLIS": "Euronext Lisbon", "XMIL": "Euronext Milan", "XDUB": "Euronext Dublin",
            "XOAM": "Euronext Oslo", "XWAR": "Warsaw Stock Exchange"}
# Trading start dates that are system dates, not listings.
PLACEHOLDER_DATES = {"1900-01-01", "2000-09-25", "2007-11-01", "2016-01-01", "2017-06-07", "2018-01-03",
                     "2018-05-22"}
EARLIEST_TRUSTED = "2000-01-01"     # FIRDS dates before this are data start dates
BREXIT_END = "2020-12-31"


def _today() -> str:
    return dt.date.today().isoformat()


# --- ISO 10383 --------------------------------------------------------------------

_mics: dict[str, dict] | None = None


def mics() -> dict[str, dict]:
    """MIC -> {operating, name, category (RMKT/MLTF/...), country}, cached 30 days."""
    global _mics
    if _mics is None:
        path = CACHE_DIR / "iso10383_mic.csv"
        fresh = path.exists() and (time.time() - path.stat().st_mtime) < MIC_CACHE_DAYS * 86400
        if not fresh:
            try:
                r = httpx.get(MIC_LIST, timeout=TIMEOUT_S, follow_redirects=True)
                r.raise_for_status()
                CACHE_DIR.mkdir(exist_ok=True)
                path.write_bytes(r.content)
            except httpx.HTTPError as e:
                if not path.exists():
                    raise
                log.warning("MIC list refresh failed, using the old copy: %s", str(e)[:120])
        text = path.read_bytes().decode("utf-8", errors="replace")
        _mics = {r["MIC"]: {"operating": r["OPERATING MIC"], "name": r["MARKET NAME-INSTITUTION DESCRIPTION"],
                            "category": r["MARKET CATEGORY CODE"], "country": r["ISO COUNTRY CODE (ISO 3166)"]}
                 for r in csv.DictReader(io.StringIO(text))}
    return _mics


def venue_name(mic: str) -> str:
    m = mics().get(mic) or {}
    return FRIENDLY.get(mic) or (m.get("name") or mic).title()


# Names reports use for an exchange that neither FRIENDLY nor the ISO list spells so.
EXCHANGE_ALIASES = {
    "oslo stock exchange": "XOSL", "oslo bors": "XOSL", "stockholm stock exchange": "XSTO",
    "nasdaq omx stockholm": "XSTO", "copenhagen stock exchange": "XCSE",
    "nasdaq omx copenhagen": "XCSE", "helsinki stock exchange": "XHEL",
    "nasdaq omx helsinki": "XHEL", "lse": "XLON", "london stock exchange main market": "XLON",
    "new york stock exchange": "XNYS", "nyse": "XNYS", "nasdaq": "XNAS",
    "nasdaq stock market": "XNAS", "swiss exchange": "XSWX", "six swiss exchange": "XSWX",
    "frankfurt stock exchange": "XFRA", "deutsche borse": "XETR", "euronext oslo bors": "XOSL",
}


def _exchange_key(name: str) -> str:
    t = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\b(the|ab|asa|as|plc|ltd|limited|inc|s\.?a\.?|ag)\b", " ", t)
    return " ".join(re.findall(r"[a-z0-9]+", t))


# Growth markets with one name in several countries: the market MIC per country.
FIRST_NORTH = {"SE": "FNSE", "DK": "FNDK", "FI": "FNFI", "IS": "FNIS", "EE": "FNEE",
               "LV": "FNLV", "LT": "FNLT"}
OTHER_GROWTH = {"spotlight stock market": "XSAT", "spotlight": "XSAT",
                "euronext growth oslo": "MERK", "euronext growth": None,
                "nordic growth market": "XNGM", "ngm": "XNGM"}


def mic_for_name(name: str | None, country: str | None = None) -> str | None:
    """The MIC of an exchange named in a document: "Nasdaq Stockholm" -> XSTO, "Oslo
    Børs" -> XOSL, "Nasdaq First North Growth Market" in Sweden -> FNSE. Only the first
    exchange of a list ("Oslo Børs, New York Stock Exchange") counts. None when the name
    matches no exchange or several."""
    first = re.split(r",|;| and |/", name or "")[0].strip()
    key = _exchange_key(first)
    if not key:
        return None
    if key in EXCHANGE_ALIASES:
        return EXCHANGE_ALIASES[key]
    if "first north" in key:
        return FIRST_NORTH.get((country or "").upper())
    for growth, mic in OTHER_GROWTH.items():
        if key == growth or key.startswith(growth + " "):
            return mic
    found = {mic for mic, n in FRIENDLY.items() if _exchange_key(n) == key}
    if not found:
        try:
            table = mics()
        except httpx.HTTPError:
            return None
        found = {m["operating"] or mic for mic, m in table.items()
                 if _exchange_key(m["name"]) == key}
    return found.pop() if len(found) == 1 else None


# --- FIRDS ------------------------------------------------------------------------

FIELDS = ("isin,mic,rca_mic,gnr_cfi_code,gnr_full_name,mrkt_issr_trdng_rqst_flag,"
          "mrkt_trdng_start_date,mrkt_trdng_trmination_date")


def firds_url(lei: str) -> str:
    return f"{FIRDS}?q=lei:{lei}%20AND%20gnr_cfi_code:ES*&wt=json"


def firds_shares(lei: str) -> list[dict]:
    """FIRDS records of the issuer's shares (CFI ES*), on every venue."""
    def fetch():
        r = httpx.get(FIRDS, params={"q": f"lei:{lei} AND gnr_cfi_code:ES*", "wt": "json",
                                     "rows": 2000, "fl": FIELDS}, timeout=TIMEOUT_S)
        r.raise_for_status()
        return r.json()["response"]["docs"]
    return _cached(firds_url(lei), fetch) or []


def _active(d: dict) -> bool:
    end = (d.get("mrkt_trdng_trmination_date") or "")[:10]
    return not end or end > _today()


def home_listings(docs: list[dict], country: str) -> tuple[str | None, list[dict]]:
    """(operating MIC, records) of the issuer-requested, still active listing on an
    exchange in the company's own country; failing that, on any one exchange (Shell:
    a UK company whose EU listing is Euronext Amsterdam)."""
    by_exchange: dict[str, list[dict]] = {}
    for d in docs:
        if d.get("mrkt_issr_trdng_rqst_flag") != "Yes" or not _active(d):
            continue
        m = mics().get(d.get("mic") or "")
        if not m or m["category"] not in ("RMKT", "MLTF"):
            continue
        by_exchange.setdefault(m["operating"], []).append(d)
    if not by_exchange:
        return None, []
    home = [op for op in by_exchange if (mics().get(op) or {}).get("country") == country]
    # most records first: the exchange that lists most of the issuer's share classes
    op = max(home or by_exchange, key=lambda o: len(by_exchange[o]))
    return op, by_exchange[op]


def _listing_date(docs: list[dict], op: str) -> str | None:
    """The first trading date on the home exchange, when it can be trusted."""
    dates = sorted((d.get("mrkt_trdng_start_date") or "")[:10] for d in docs
                   if (mics().get(d.get("mic") or "") or {}).get("operating") == op)
    dates = [x for x in dates if x]
    if not dates:
        return None
    first = dates[0]
    if first in PLACEHOLDER_DATES or first < EARLIEST_TRUSTED:
        return None
    return first


# --- OpenFIGI ---------------------------------------------------------------------

def openfigi(isin: str, exch: str) -> list[dict]:
    """OpenFIGI's listings of this ISIN on this Bloomberg exchange code (cached)."""
    key = f"{OPENFIGI}#{isin}/{exch}"

    def fetch():
        headers = {"Content-Type": "application/json"}
        if os.getenv("OPENFIGI_API_KEY"):
            headers["X-OPENFIGI-APIKEY"] = os.environ["OPENFIGI_API_KEY"]
        body = json.dumps([{"idType": "ID_ISIN", "idValue": isin, "exchCode": exch}])
        for attempt in range(4):
            r = httpx.post(OPENFIGI, content=body, headers=headers, timeout=TIMEOUT_S)
            if r.status_code == 429:               # 25 a minute without a key
                time.sleep(15 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()[0].get("data") or []
        r.raise_for_status()
        return []
    return _cached(key, fetch) or []


def _ticker(isin: str, op: str) -> str | None:
    exch = BLOOMBERG_EXCH.get(op)
    if not exch:
        return None
    rows = [r for r in openfigi(isin, exch) if r.get("marketSector") == "Equity"]
    # London tickers end in "/" for the class separator ("AO/", "BT/A"): drop a trailing one
    return rows[0]["ticker"].rstrip("/") if rows else None


# --- Nasdaq Nordic segments --------------------------------------------------------

# Nasdaq's own share lists, one per market and cap segment (the same lists as on
# nasdaq.com/european-market-activity/shares). No key; cached like the other APIs.
NASDAQ_SCREENER = "https://api.nasdaq.com/api/nordic/screener/shares"
NASDAQ_MARKETS = {"XSTO": "STO", "XCSE": "CPH", "XHEL": "HEL", "XICE": "ICE"}
NASDAQ_SEGMENTS = {"LARGE_CAP": "Large Cap", "MID_CAP": "Mid Cap", "SMALL_CAP": "Small Cap"}


def nasdaq_segment_url(market: str, segment: str) -> str:
    return f"{NASDAQ_SCREENER}?category=MAIN_MARKET&tableonly=true&market={market}&segment={segment}"


def nasdaq_segment(isins: list[str], op: str) -> tuple[str, str] | None:
    """(segment, list URL) of a share on a Nasdaq Nordic main market: Large, Mid or
    Small Cap, from Nasdaq's list of that segment."""
    market = NASDAQ_MARKETS.get(op)
    if not market:
        return None
    for seg, label in NASDAQ_SEGMENTS.items():
        url = nasdaq_segment_url(market, seg)

        def fetch(url=url):
            r = httpx.get(url, timeout=TIMEOUT_S, headers={"User-Agent": "Mozilla/5.0",
                                                           "Accept": "application/json"})
            r.raise_for_status()
            rows = ((r.json().get("data") or {}).get("instrumentListing") or {}).get("rows") or []
            return [x.get("isin") for x in rows if x.get("isin")]
        try:
            listed = _cached(url, fetch) or []
        except (httpx.HTTPError, ValueError) as e:
            log.warning("Nasdaq Nordic %s %s list: %s", market, label, str(e)[:120])
            return None
        if set(isins) & set(listed):
            return label, url
    return None


# --- data points -------------------------------------------------------------------

def listing_values(lei: str | None, country: str | None, gleif_isins=()) -> list[Found]:
    """isin, exchange, ticker, listing_status, exchange_segment (an MTF growth market,
    or the Large/Mid/Small Cap segment on a Nasdaq Nordic main market) and listing_date
    (recent listings only) from FIRDS, the MIC list, Nasdaq's segment lists and OpenFIGI."""
    if not lei:
        return []
    country = (country or "").upper()
    docs = firds_shares(lei)
    furl = firds_url(lei)
    src = dict(source="ESMA FIRDS", endpoint=furl, method="API",
               retrieved_at=retrieved_at(furl))
    out: list[Found] = []
    op, recs = home_listings(docs, country)
    if country in NON_EU_HOME and (not op or (mics().get(op) or {}).get("country") != country):
        # Home exchange outside FIRDS: the share ISINs FIRDS knows (any venue, also
        # London records closed at Brexit) or GLEIF's, then OpenFIGI on the home exchange.
        home = NON_EU_HOME[country]
        isins = list(dict.fromkeys([d["isin"] for d in docs if d["isin"].startswith(country)]
                                   + [i for i in gleif_isins if i.startswith(country)]))[:10]
        for isin in isins:
            ticker = _ticker(isin, home)
            if ticker:
                fig = dict(source="OpenFIGI", endpoint=f"{OPENFIGI} (ID_ISIN {isin}, exchCode "
                           f"{BLOOMBERG_EXCH[home]})", method="API",
                           retrieved_at=retrieved_at(f"{OPENFIGI}#{isin}/{BLOOMBERG_EXCH[home]}"))
                out += [Found("isin", isin, **fig, confidence="A",
                              note="share listed on the home exchange"),
                        Found("exchange", venue_name(home), **fig, confidence="A",
                              note=f"MIC {home}; " + _category(home)),
                        Found("ticker", ticker, **fig, confidence="B",
                              note="Bloomberg-style ticker (spaces and class separators dropped)"),
                        Found("listing_status", "listed", **fig, confidence="A",
                              note=f"share {isin} trades on {venue_name(home)}")]
                return out
        if not op:
            return []
    if not op:
        return []
    isins = sorted({d["isin"] for d in recs})
    names = {d["isin"]: d.get("gnr_full_name") or "" for d in recs}
    out.append(Found("isin", "; ".join(isins), **src, confidence="A",
                     note="issuer-requested listing on " + venue_name(op)
                          + ("" if len(isins) == 1 else "; share classes: "
                             + "; ".join(f"{i} {names[i].strip()}" for i in isins))))
    out.append(Found("exchange", venue_name(op), **src, confidence="A",
                     note=f"MIC {op}; " + _category(op)))
    out.append(Found("listing_status", "listed", **src, confidence="A",
                     note=f"issuer-requested, active listing on {venue_name(op)}"))
    segs = {d["mic"] for d in recs if d["mic"] != op
            and (mics().get(d["mic"]) or {}).get("category") == "MLTF"}
    if (mics().get(op) or {}).get("category") == "MLTF" or segs:
        seg = sorted(segs)[0] if segs else op
        out.append(Found("exchange_segment", venue_name(seg), **src, confidence="A",
                         note=f"MIC {seg}; multilateral trading facility (not a regulated market)"))
    elif (cap := nasdaq_segment(isins, op)):
        label, url = cap
        out.append(Found("exchange_segment", label, source="Nasdaq Nordic", endpoint=url,
                         method="API", confidence="A", retrieved_at=retrieved_at(url),
                         note=f"{venue_name(op)} {label} segment (Nasdaq's segment list)"))
    date = _listing_date(docs, op)
    if date:
        out.append(Found("listing_date", date, **src, confidence="C",
                         note=f"first trading date in FIRDS on {venue_name(op)}; FIRDS has "
                              f"trading dates, not admission dates"))
    # the most widely traded class first (most FIRDS venue records): Volvo B, not A
    for isin in sorted(isins, key=lambda i: -sum(d["isin"] == i for d in docs)):
        ticker = _ticker(isin, op)
        if ticker:
            fig_key = f"{OPENFIGI}#{isin}/{BLOOMBERG_EXCH[op]}"
            out.append(Found("ticker", ticker, source="OpenFIGI", method="API", confidence="B",
                             endpoint=f"{OPENFIGI} (ID_ISIN {isin}, exchCode {BLOOMBERG_EXCH[op]})",
                             retrieved_at=retrieved_at(fig_key),
                             note="Bloomberg-style ticker (spaces and class separators dropped)"
                                  + (f"; for {isin}" if len(isins) > 1 else "")))
            break
    return out


def _category(mic: str) -> str:
    return {"RMKT": "regulated market", "MLTF": "multilateral trading facility"}.get(
        (mics().get(mic) or {}).get("category"), "venue type not stated")
