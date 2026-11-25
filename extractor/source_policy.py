"""Legal's source rules (24 Nov 2026), applied before every download and to identifiers.

The switch is LEGAL_SOURCE_RULES in .env or the environment:
- false (the default, or unset): no checks; everything works as before;
- true: a download that breaks a rule is skipped (scraper.SourceBlockedError, a
  DownloadError and a SourceBlocked) and
  an identifier from a source legal does not allow is not stored;
- report: every check runs and every would-be skip or drop is logged, but nothing changes
  (for measuring only).
Every skip or drop is logged to output/source_policy_log.csv.

The checks, per URL:
- blocked host (source_impact.BLOCKED_HOSTS: exchanges, the listed news sites, cdn.sanity.io);
- a bucket file is judged by its original address (the bucket's source_url);
- robots.txt (RFC 9309) for "*" and, for a Firecrawl call, for FirecrawlAgent; a robots.txt
  that cannot be fetched (5xx, no answer) counts as "disallow all", as the RFC says;
- /.well-known/tdmrep.json, /ai.txt and the TDM-Rep header (a HEAD on the document);
- filings.xbrl.org stays allowed until legal answers (SOURCE_POLICY_XBRL=block to block it).

Data APIs (GLEIF, ESMA FIRDS, OpenFIGI, registries) are not crawled: robots.txt is not asked.
The web answers share source_impact's cache (cache/source_impact/).
"""

from __future__ import annotations

import csv
import datetime as dt
import logging
import os
import re
import threading
from dataclasses import dataclass
from urllib.parse import urlparse

from .config import OUTPUT_DIR

log = logging.getLogger(__name__)

LOG = OUTPUT_DIR / "source_policy_log.csv"
LOG_COLUMNS = ["at", "mode", "action", "url", "agent", "rule", "detail"]
FIRECRAWL = "FirecrawlAgent"
DIRECT = "*"
# Identifiers: which source each may come from
ISIN_SOURCES = ("GLEIF",)
EXCHANGE_SOURCES = ("ESMA FIRDS",)        # or a report: Annual report (...)
IDENTIFIERS = ("isin", "ticker", "exchange", "listing_status", "exchange_segment", "listing_date")

_lock = threading.Lock()
_web = None
_bucket = None


class SourceBlocked(RuntimeError):
    """A download legal's rules do not allow (only raised with LEGAL_SOURCE_RULES=true)."""

    def __init__(self, url: str, rule: str, detail: str = ""):
        super().__init__(f"Not downloaded ({rule}): {url}" + (f" ({detail})" if detail else ""))
        self.url, self.rule, self.detail = url, rule, detail


@dataclass(frozen=True)
class Verdict:
    allowed: bool
    rule: str = ""
    detail: str = ""


def mode() -> str:
    """"enforce" (LEGAL_SOURCE_RULES=true), "report" or "off" (false, unset: as before)."""
    v = (os.getenv("LEGAL_SOURCE_RULES") or "").strip().lower()
    if v in ("true", "1", "yes", "on"):
        return "enforce"
    return "report" if v == "report" else "off"


def enforced() -> bool:
    return mode() == "enforce"


def _si():
    from . import source_impact
    return source_impact


def _web_checks():
    global _web
    with _lock:
        if _web is None:
            _web = _si().Web()
        return _web


def _bucket_origin(url: str) -> dict | None:
    global _bucket
    if not re.search(r"cache[\\/]+gcs[\\/]+objects|storage\.cloud\.google\.com|^gs://", url, re.I):
        return None
    with _lock:
        if _bucket is None:
            _bucket = _si().Bucket()
    return _bucket.origin(url.replace("\\", "/"))


_refetched: set[str] = set()


def _host_info(web, scheme_host: str) -> dict:
    """The host's robots.txt etc.; a failed or server-error answer (cached by an earlier
    check) is asked again once per run, with the downloader's own client (OS certificate
    store, then a browser TLS fingerprint), before it can block anything."""
    info = web.host(scheme_host)
    st = info.get("robots_status")
    if not (st is None or st == 429 or (isinstance(st, int) and st >= 500)) or scheme_host in _refetched:
        return info
    _refetched.add(scheme_host)
    from . import scraper
    status, body = None, ""
    for get in (scraper._httpx_get, scraper._impersonated_get):
        try:
            status, _, raw = get(scheme_host + "/robots.txt")
            body = raw[:400_000].decode("utf-8", "replace")
            if status < 500 and status != 429:
                break
        except Exception:  # noqa: BLE001 - try the next client
            continue
    info = {**info, "robots_status": status,
            "robots": body if status == 200 and "<html" not in body[:300].lower() else ""}
    with _lock:
        web.hosts[scheme_host] = info
    try:
        web.save()
    except OSError:
        pass
    return info


def blocked_host(url: str) -> str | None:
    """The blocked domain this URL is on, if any."""
    si = _si()
    host = urlparse(url).netloc.lower()
    return si._under(host, si.BLOCKED_HOSTS) if host else None


def check(url: str, agent: str = DIRECT, head: bool = True) -> Verdict:
    """May this URL be downloaded under legal's rules?"""
    si = _si()
    origin = _bucket_origin(url)
    if origin is not None:
        src = origin.get("source_url") or ""
        if not src:
            return Verdict(True, "", "bucket file; original address not recorded")
        b = blocked_host(src)
        return Verdict(False, "blocked host", f"bucket file from {b}: {src}") if b else Verdict(True)
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return Verdict(True)                 # a local file
    host = p.netloc.lower()
    b = blocked_host(url)
    if b:
        return Verdict(False, "blocked host", b)
    if (host == si.NOT_A_FILING_ARCHIVE or host.endswith("." + si.NOT_A_FILING_ARCHIVE)) \
            and (os.getenv("SOURCE_POLICY_XBRL") or "").lower() == "block":
        return Verdict(False, "filings.xbrl.org", "blocked by SOURCE_POLICY_XBRL")
    if si._under(host, si.API_HOSTS):
        return Verdict(True)
    web = _web_checks()
    info = _host_info(web, f"{p.scheme}://{p.netloc}")
    st = info.get("robots_status")
    if isinstance(st, int) and (st >= 500 or st == 429):
        return Verdict(False, "robots.txt unreachable", f"status {st}: RFC 9309 says assume disallow")
    if st is None:      # our request failed, not the site's answer: the download will tell
        _log("not checked", url, agent, Verdict(True, "robots.txt not fetched", "connection failed"))
    text = info.get("robots") or ""
    if text and not si.robots_allows(text, "*", url):
        return Verdict(False, "robots.txt", "disallows all crawlers")
    if text and agent != DIRECT and not si.robots_allows(text, agent, url):
        return Verdict(False, "robots.txt", f"disallows {agent}")
    if si.tdm_reserved(info, url):
        return Verdict(False, "TDM reservation", "tdmrep.json")
    if si.ai_txt_disallows(info, url):
        return Verdict(False, "ai.txt", "disallows")
    if head:
        d = web.doc(url)
        if str(d.get("tdm_reservation") or "").strip() == "1":
            return Verdict(False, "TDM reservation", "TDM-Rep header")
    return Verdict(True)


def _log(action: str, url: str, agent: str, v: Verdict) -> None:
    row = {"at": dt.datetime.now().isoformat(timespec="seconds"), "mode": mode(), "action": action,
           "url": url, "agent": agent, "rule": v.rule, "detail": v.detail}
    with _lock:
        new = not LOG.exists()
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=LOG_COLUMNS)
            if new:
                w.writeheader()
            w.writerow(row)


def gate(url: str, agent: str = DIRECT, head: bool = True) -> None:
    """Before a download: skip it (enforce) or log it (report) when a rule says no."""
    if mode() == "off" or not url:
        return
    try:
        v = check(url, agent, head)
    except Exception as e:  # noqa: BLE001 - the check itself failing must not stop a run
        log.warning("source check failed for %s: %s", url, str(e)[:150])
        return
    if v.allowed:
        return
    if enforced():
        _log("skipped", url, agent, v)
        log.warning("Source rules: not downloading %s (%s %s)", url, v.rule, v.detail)
        from .scraper import SourceBlockedError      # a DownloadError: callers already skip those
        raise SourceBlockedError(url, v.rule, v.detail)
    _log("would skip", url, agent, v)


def allows_candidate(url: str) -> bool:
    """For ranking report candidates: False only when enforcing and the host is blocked
    (cheap: no web request), so the finder goes for the company's own copy instead."""
    return not (enforced() and (blocked_host(url) or _bucket_blocked(url)))


def _bucket_blocked(url: str) -> bool:
    o = _bucket_origin(url)
    return bool(o and o.get("source_url") and blocked_host(o["source_url"]))


def identifier_allowed(data_point: str, source: str) -> bool:
    """Only the FIGI code from OpenFIGI; ISIN from GLEIF's ISIN-to-LEI file; exchange and
    listing status from ESMA FIRDS or the annual report."""
    source = source or ""
    if source == "OpenFIGI":
        return data_point == "figi"
    if data_point == "isin":
        return source in ISIN_SOURCES
    if data_point in ("exchange", "listing_status"):
        return source in EXCHANGE_SOURCES or source.startswith("Annual report")
    if data_point == "exchange_segment":
        return blocked_host_source(source) is None
    return True


def blocked_host_source(source: str) -> str | None:
    """Sources named after a blocked exchange's own API (Nasdaq Nordic, Euronext, Oslo Børs)."""
    s = source.lower()
    return next((n for n in ("nasdaq", "euronext", "oslo b") if n in s), None)


def keep_identifier(data_point: str, source: str, value: str = "") -> bool:
    """Whether to store this identifier: always outside enforce mode (a would-be drop is logged)."""
    if mode() == "off" or data_point not in IDENTIFIERS or identifier_allowed(data_point, source):
        return True
    v = Verdict(False, "identifier source", f"{data_point} from {source}")
    if enforced():
        _log("dropped", f"{data_point}={value}", "", v)
        return False
    _log("would drop", f"{data_point}={value}", "", v)
    return True
