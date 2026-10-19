"""Batch runner: one CSV of companies in, one JSON per company + summary.csv out.

    python -m extractor.batch companies.csv [--dry-run] [--limit N] [--max-credits N]
                                            [--retry-failed] [--force] [--only ID,ID]

CSV columns (header required, comma or semicolon separated, UTF-8):
    company_id, company_name, country_code

Resumable: companies that already have output/<id>.json are skipped, and so are
companies that failed before (output/<id>.error.json) unless --retry-failed.
--dry-run only does the free lookups (GLEIF + Wikidata) and estimates credits.
"""

import argparse
import csv
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
import datetime as dt
import json
import logging
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import httpx
import openai
import requests
from firecrawl import PaymentRequiredError, UnauthorizedError

from .config import CACHE_DIR, OUTPUT_DIR, PROJECT_ROOT, ConfigError, clean_name, load_settings, slugify
from .firecrawl_client import FirecrawlClient
from .llm import StructuredOutputsUnsupportedError
from .pipeline import identify_lei, run
from .monday import load_golden, pick_sample, write_sample, write_table
from .report import write_report
from .report_finder import MAX_AGE_YEARS, _looks_like_report_page, allowed_place_words, classify
from .wikidata import website_for_lei, website_for_name

log = logging.getLogger("extractor.batch")

# Errors that will hit every company: stop the batch instead of failing 100 times.
FATAL = (ConfigError, PaymentRequiredError, UnauthorizedError, StructuredOutputsUnsupportedError)

# Firecrawl credit estimates per company: (min, expected, max).
CREDITS_WEBSITE_KNOWN = (1, 1.5, 6)    # Wikidata gave the website: map(s) only
CREDITS_WEBSITE_SEARCH = (3, 3.5, 8)   # + one search
DEFAULT_MAX_CREDITS_PER_COMPANY = 6

_COLUMN_ALIASES = {
    "company_id": {"company_id", "companyid", "id", "company id"},
    "company_name": {"company_name", "companyname", "name", "company name", "legal_name",
                     "legal name"},
    "country_code": {"country_code", "countrycode", "country", "country code", "iso2"},
    "segment": {"segment", "group", "company_segment"},
    "lei": {"lei", "lei_code"},
}
_OPTIONAL_COLUMNS = {"country_code", "segment", "lei"}

SUMMARY_FIELDS = [
    "company_id", "company_name", "country_code", "status", "lei", "lei_match", "website",
    "website_source", "report_url", "fiscal_year", "currency", "revenue", "revenue_unit",
    "revenue_full", "total_assets", "total_assets_unit", "total_assets_full",
    "failed_checks", "firecrawl_credits", "error",
]


@dataclass
class Company:
    company_id: str
    name: str
    country: str | None
    segment: str | None = None   # e.g. "nordic_listed", from the CSV if given
    lei: str | None = None       # from the CSV if given: skips the GLEIF name search

    @property
    def slug(self) -> str:
        return slugify(self.company_id)

    @property
    def result_path(self) -> Path:
        return OUTPUT_DIR / f"{self.slug}.json"

    @property
    def error_path(self) -> Path:
        return OUTPUT_DIR / f"{self.slug}.error.json"


# --- input -----------------------------------------------------------------------

def fix_mojibake(text: str) -> str:
    """Undo UTF-8 text that was decoded as Windows-1252 and saved again:
    'HuhtamÃ¤ki' -> 'Huhtamäki', 'Ã…landsbanken' -> 'Ålandsbanken'. Text that isn't
    mojibake is returned unchanged."""
    if not any(marker in text for marker in ("Ã", "Â", "â€")):
        return text
    raw = bytearray()
    for ch in text:
        try:
            raw += ch.encode("cp1252")
        except UnicodeEncodeError:
            try:
                raw += ch.encode("latin-1")   # bytes cp1252 leaves undefined (0x81, 0x8D, ...)
            except UnicodeEncodeError:
                return text
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return text


def read_companies(path: Path) -> list[Company]:
    text = path.read_text(encoding="utf-8-sig")       # utf-8-sig: Excel's "CSV UTF-8" BOM
    try:
        dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    if not rows:
        raise ValueError(f"{path} has no data rows")

    header = {h: (h or "").strip().lower() for h in rows[0].keys()}
    col = {}
    for field, aliases in _COLUMN_ALIASES.items():
        match = [h for h, low in header.items() if low in aliases]
        if not match and field not in _OPTIONAL_COLUMNS:
            raise ValueError(f"Column {field!r} not found in {path}. Header: {list(header)}")
        col[field] = match[0] if match else None

    companies, seen = [], set()
    for i, row in enumerate(rows, start=2):           # line 1 is the header
        cid = (row.get(col["company_id"]) or "").strip()
        name = fix_mojibake((row.get(col["company_name"]) or "").strip())
        country = (row.get(col["country_code"]) or "").strip().upper() if col["country_code"] else ""
        if not cid and not name:
            continue
        if not cid or not name:
            raise ValueError(f"{path} line {i}: company_id and company_name are both required")
        if cid in seen:
            raise ValueError(f"{path} line {i}: duplicate company_id {cid!r}")
        if country and len(country) != 2:
            raise ValueError(f"{path} line {i}: country_code {country!r} is not a 2-letter code")
        seen.add(cid)
        segment = (row.get(col["segment"]) or "").strip() if col["segment"] else ""
        lei = (row.get(col["lei"]) or "").strip().upper() if col["lei"] else ""
        if lei and not (len(lei) == 20 and lei.isalnum()):
            raise ValueError(f"{path} line {i}: lei {lei!r} is not a 20-character LEI")
        companies.append(Company(cid, name, country or None, segment or None, lei or None))
    return companies


# --- summary -----------------------------------------------------------------------

def _money(m: dict | None) -> tuple:
    m = m or {}
    return m.get("value"), m.get("unit"), m.get("value_full")


def summary_row(c: Company) -> dict:
    row = {"company_id": c.company_id, "company_name": c.name, "country_code": c.country or ""}
    if c.result_path.exists():
        r = json.loads(c.result_path.read_text(encoding="utf-8"))
        rev, rev_unit, rev_full = _money(r.get("revenue"))
        ta, ta_unit, ta_full = _money(r.get("total_assets"))
        fails = [f"{x['name']}/{x['target']}" for x in r.get("checks", []) if x["result"] == "fail"]
        row |= {
            "status": r.get("status"), "lei": r.get("lei"), "lei_match": r.get("lei_lookup"),
            "website": r.get("website"), "website_source": r.get("website_source"),
            "report_url": r.get("report_url"), "fiscal_year": r.get("fiscal_year"),
            "currency": (r.get("revenue") or {}).get("currency")
                        or (r.get("total_assets") or {}).get("currency"),
            "revenue": rev, "revenue_unit": rev_unit, "revenue_full": rev_full,
            "total_assets": ta, "total_assets_unit": ta_unit, "total_assets_full": ta_full,
            "failed_checks": "; ".join(fails),
            "firecrawl_credits": r.get("firecrawl_credits_used"),
        }
    elif c.error_path.exists():
        e = json.loads(c.error_path.read_text(encoding="utf-8"))
        row |= {"status": "error", "error": f"{e.get('error_type')}: {e.get('error')}",
                "firecrawl_credits": e.get("firecrawl_credits_used")}
    else:
        row["status"] = "pending"
    return row


def write_summary(companies: list[Company], path: Path) -> None:
    tmp = path.with_suffix(".tmp")
    # utf-8-sig so Excel shows å/ä/ø correctly when the file is double-clicked
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS, extrasaction="ignore")
        w.writeheader()
        for c in companies:
            w.writerow(summary_row(c))
    # Windows: replace fails while the file is open in Excel (or briefly held by
    # antivirus). Retry, then skip: the summary is rebuilt after every company.
    for attempt in range(5):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            time.sleep(1 + attempt)
    log.warning("Could not update %s (open in Excel?); will retry after the next company", path)
    print(f"  (could not update {path.name}: close it in Excel; it is rewritten after each company)")


# --- logging -----------------------------------------------------------------------

def _setup_logging() -> None:
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, handlers=[console],
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    for noisy in ("httpx", "httpcore", "openai", "hpack", "urllib3", "firecrawl"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


class _CompanyLog:
    """Send all log records to output/<id>.log while one company is processed."""

    def __init__(self, c: Company):
        self.handler = logging.FileHandler(OUTPUT_DIR / f"{c.slug}.log", mode="w", encoding="utf-8")
        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))

    def __enter__(self):
        logging.getLogger().addHandler(self.handler)

    def __exit__(self, *exc):
        logging.getLogger().removeHandler(self.handler)
        self.handler.close()


# --- modes ---------------------------------------------------------------------------

def dry_run(companies: list[Company], out_csv: Path) -> None:
    """Free lookups only (GLEIF + Wikidata). LEI results are cached for the real run."""
    rows, mins, exps, maxs = [], 0.0, 0.0, 0.0
    n_lei = n_site = n_done = 0
    for i, c in enumerate(companies, 1):
        if c.result_path.exists():
            n_done += 1
            rows.append({"company_id": c.company_id, "company_name": c.name,
                         "country_code": c.country, "note": "already done (0 credits)"})
            continue
        lei_info = identify_lei(c.name, c.slug, None, True, c.country)
        rec = lei_info["record"]
        site, why = (website_for_lei(rec["lei"], clean_name(c.name), rec.get("country") or c.country)
                     if rec else (None, "no LEI"))
        for country in dict.fromkeys(x for x in (c.country, (rec or {}).get("country")) if x):
            if site:
                break
            site, why2 = website_for_name(clean_name(c.name), country)
            why = why2 if site else f"{why}; {why2}"
        est = CREDITS_WEBSITE_KNOWN if site else CREDITS_WEBSITE_SEARCH
        n_lei += bool(rec)
        n_site += bool(site)
        mins, exps, maxs = mins + est[0], exps + est[1], maxs + est[2]
        rows.append({"company_id": c.company_id, "company_name": c.name, "country_code": c.country,
                     "lei": rec["lei"] if rec else "", "gleif_name": rec["legal_name"] if rec else "",
                     "lei_match": lei_info["reason"], "wikidata_website": site or "",
                     "website_note": why, "est_credits": est[1]})
        print(f"[{i}/{len(companies)}] {c.company_id} {c.name}: "
              f"LEI {'yes' if rec else 'no '} | website {'Wikidata' if site else 'needs search'}")
        time.sleep(0.3)                                # be polite to GLEIF/Wikidata

    fields = ["company_id", "company_name", "country_code", "lei", "gleif_name", "lei_match",
              "wikidata_website", "website_note", "est_credits", "note"]
    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    todo = len(companies) - n_done
    print(f"\nDry run: {len(companies)} companies, {n_done} already done, {todo} to process")
    if todo:
        print(f"  LEI found:            {n_lei}/{todo}")
        print(f"  Website via Wikidata: {n_site}/{todo} (the rest need a Firecrawl search)")
        print(f"  Estimated Firecrawl credits: ~{exps:.0f} (range {mins:.0f}-{maxs:.0f})")
    print(f"  Details: {out_csv}")


# --- network outages -------------------------------------------------------------

NETWORK_ERRORS = (socket.gaierror, ConnectionError, httpx.ConnectError, httpx.ConnectTimeout,
                  requests.exceptions.ConnectionError, openai.APIConnectionError)
_NETWORK_ERROR_NAMES = {"APIConnectionError", "ConnectionError", "ConnectError", "ConnectTimeout",
                        "gaierror", "NameResolutionError"}
NETWORK_RETRIES_PER_COMPANY = 3
NETWORK_MAX_WAIT_S = 60 * 60
_PROBE_HOSTS = ["api.firecrawl.dev", "www.wikidata.org", "api.gleif.org"]


def is_network_error(exc: BaseException) -> bool:
    """True if the failure (or anything in its cause/context chain) is a lost
    connection. The Firecrawl SDK sometimes hides it behind an AttributeError."""
    stack, seen = [exc], set()
    while stack:
        e = stack.pop()
        if e is None or id(e) in seen:
            continue
        seen.add(id(e))
        if isinstance(e, NETWORK_ERRORS):
            return True
        stack += [e.__cause__, e.__context__]
    return False


def _failed_on_network(error_file: dict) -> bool:
    """Error files from before network errors were handled (or after 3 retries)."""
    return bool(error_file.get("network_error")
                or error_file.get("error_type") in _NETWORK_ERROR_NAMES
                or "object has no attribute 'status_code'" in (error_file.get("error") or ""))


def internet_up() -> bool:
    for host in _PROBE_HOSTS:
        try:
            with socket.create_connection((host, 443), timeout=5):
                return True
        except OSError:
            continue
    return False


def wait_for_internet(max_wait_s: int = NETWORK_MAX_WAIT_S, every_s: int = 30) -> bool:
    """Block until the internet is reachable again. False if it stays down too long."""
    waited = 0
    while not internet_up():
        if waited >= max_wait_s:
            return False
        time.sleep(every_s)
        waited += every_s
    return True


# --- --refresh ----------------------------------------------------------------------

def _cached_report_still_good(c: Company) -> bool:
    """Would the cached report choice still be accepted by today's rules?"""
    path = CACHE_DIR / f"{c.slug}_discovery.json"
    if not path.exists():
        return False
    try:
        found = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    url = found.get("report_url") or ""
    cand = classify(url, allowed_place_words(c.name, [c.country]))
    oldest_ok = dt.date.today().year - MAX_AGE_YEARS
    return bool(cand.kept and (cand.year is None or cand.year >= oldest_ok)
                and (cand.is_pdf or _looks_like_report_page(url)))


def prepare_refresh(c: Company) -> str | None:
    """--refresh: make an already-processed company run again under the current rules.
    Keeps the cached report if it still passes (then the redo costs 0 Firecrawl
    credits, only the LLM runs again); otherwise drops it so it's found again.
    Returns a note for the console, or None if the company shouldn't be redone."""
    if c.error_path.exists():
        try:
            err = json.loads(c.error_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            err = {}
        if err.get("error_type") in ("NeedsOCRError", "DownloadError"):
            cache = CACHE_DIR / f"{c.slug}_discovery.json"
            try:
                had_fallbacks = "report_alternatives" in json.loads(cache.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                had_fallbacks = False
            if had_fallbacks:
                return None          # the chosen file and its fallbacks were all unusable
            # Found before fallbacks existed (e.g. ABB's blank placeholder PDF): find again.
            _set_aside(cache)
    if not (c.result_path.exists() or c.error_path.exists()):
        return None
    keep = _cached_report_still_good(c)
    if not keep:
        _set_aside(CACHE_DIR / f"{c.slug}_discovery.json")
    _set_aside(c.result_path)
    _set_aside(c.error_path)
    return "re-checking with the cached report" if keep else "finding the report again"


# --refresh moves the old files here instead of deleting them, so a company that
# never gets to run (credit limit, Ctrl+C) gets its old result back.
REFRESH_BACKUP = OUTPUT_DIR / "_refresh_backup"


def _set_aside(path: Path) -> None:
    if path.exists():
        REFRESH_BACKUP.mkdir(parents=True, exist_ok=True)
        path.replace(REFRESH_BACKUP / f"{path.parent.name}__{path.name}")


def restore_refresh(c: Company) -> bool:
    """Put back the files --refresh set aside for a company that didn't run."""
    restored = False
    for path in (c.result_path, c.error_path, CACHE_DIR / f"{c.slug}_discovery.json"):
        backup = REFRESH_BACKUP / f"{path.parent.name}__{path.name}"
        if backup.exists() and not path.exists():
            backup.replace(path)
            restored = True
    # A new result and an old error (or the reverse) must not both exist.
    if c.result_path.exists() and c.error_path.exists():
        c.error_path.unlink()
    return restored


class _KeepAwake:
    """Ask Windows not to idle-sleep while the batch runs (the screen may still turn
    off). This does NOT override closing the lid; set "When I close the lid: Do
    nothing" in Windows power settings for that. No-op on other systems."""
    _CONTINUOUS, _SYSTEM_REQUIRED = 0x80000000, 0x00000001

    def __enter__(self):
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(self._CONTINUOUS | self._SYSTEM_REQUIRED)

    def __exit__(self, *exc):
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(self._CONTINUOUS)


def _worker_init(workers: int) -> None:
    """Each worker process: logging, and slower GLEIF/Wikidata pacing so that all
    workers together stay within those services' rate limits."""
    _setup_logging()
    from . import lei, wikidata
    lei._MIN_INTERVAL_S *= workers
    wikidata._MIN_INTERVAL_S *= workers


def process_company(c: Company, force: bool, per_company_cap: int) -> dict:
    """Run one company, waiting out internet outages. Returns
    {"kind": "done"|"error"|"fatal"|"offline", "status", "credits", "seconds", "error"}.
    Runs in a worker process when --workers > 1."""
    fc = FirecrawlClient(load_settings(), max_credits=per_company_cap)
    started = time.monotonic()
    network_tries = 0
    prefix = f"{c.company_id} {c.name}"

    def result(kind, **kw):
        return {"kind": kind, "credits": fc.credits.total,
                "seconds": time.monotonic() - started} | kw

    while True:
        outage: BaseException | None = None
        with _CompanyLog(c):
            try:
                r = run(c.name, company_id=c.company_id, country=c.country, fc=fc,
                        use_cache=not force, lei=c.lei)
                c.error_path.unlink(missing_ok=True)
                return result("done", status=r["status"])
            except FATAL as e:
                return result("fatal", error=f"{type(e).__name__}: {e}")
            except Exception as e:  # noqa: BLE001 - record and continue with the next company
                network_tries += is_network_error(e)
                # A connection error with the internet up is one site's problem
                # (bad certificate, server down), not an outage.
                if (is_network_error(e) and network_tries <= NETWORK_RETRIES_PER_COMPANY
                        and not internet_up()):
                    log.warning("Company %s: network error (%s); will wait and retry",
                                c.company_id, type(e).__name__)
                    outage = e
                else:
                    log.exception("Company %s failed", c.company_id)
                    c.error_path.write_text(json.dumps({
                        "company_id": c.company_id, "company_name": c.name,
                        "country_code": c.country, "error_type": type(e).__name__,
                        "error": str(e)[:1000], "network_error": is_network_error(e),
                        "firecrawl_credits_used": fc.credits.total,
                        "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    }, indent=2, ensure_ascii=False), encoding="utf-8")
                    return result("error", error=f"{type(e).__name__}: {str(e)[:150]}")
        print(f"{prefix}: connection lost ({type(outage).__name__}). Waiting for the "
              f"internet (checking every 30 s, up to {NETWORK_MAX_WAIT_S // 60} min)...", flush=True)
        if not wait_for_internet():
            return result("offline")
        print(f"{prefix}: internet is back, retrying this company", flush=True)


class _Inline:
    """Executor stand-in for --workers 1: runs each company in this process."""

    def __init__(self, *a, **k):
        pass

    def submit(self, fn, *args):
        f = Future()
        try:
            f.set_result(fn(*args))
        except BaseException as e:  # noqa: BLE001
            f.set_exception(e)
        return f

    def shutdown(self, wait=True, cancel_futures=False):
        pass


def run_batch(companies: list[Company], args) -> int:
    summary = OUTPUT_DIR / "summary.csv"
    everyone = getattr(args, "all_companies", None) or companies   # summary covers the whole list
    spent = 0
    per_company_cap = getattr(args, "max_credits_per_company", None) or DEFAULT_MAX_CREDITS_PER_COMPANY
    workers = max(1, getattr(args, "workers", 1) or 1)
    counts = {"ok": 0, "needs_review": 0, "not_found": 0, "error": 0, "skipped": 0}

    # 1. Decide what to run (skip rules, --refresh) in this process.
    todo: list[tuple[str, Company]] = []
    for i, c in enumerate(companies, 1):
        prefix = f"[{i}/{len(companies)}] {c.company_id} {c.name}"
        if getattr(args, "refresh", False) and (c.result_path.exists() or c.error_path.exists()):
            note = prepare_refresh(c)
            print(f"{prefix}: refresh, {note}" if note else f"{prefix}: refresh, skipped (scanned PDF)")
            if note is None:
                counts["skipped"] += 1
                continue
        if c.result_path.exists() and not args.force:
            counts["skipped"] += 1
            print(f"{prefix}: done before, skipped")
            continue
        if c.error_path.exists() and not (args.retry_failed or args.force):
            try:
                previous = json.loads(c.error_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                previous = {}
            if not _failed_on_network(previous):
                counts["skipped"] += 1
                print(f"{prefix}: failed before, skipped (use --retry-failed)")
                continue
            print(f"{prefix}: failed before on a network error, retrying")
        todo.append((prefix, c))

    def worst_case(c: Company) -> int:
        # Website + report already found and cached, or a cached recent English ESEF
        # filing (no website needed): the run can't spend Firecrawl credits.
        if args.force:
            return per_company_cap
        if (CACHE_DIR / f"{c.slug}_discovery.json").exists():
            return 0
        # In route order: the first recent filing is the one the run uses. A recent
        # filing in another language (Luxor's Danish ESEF) sends the run to the
        # website for English text, so it can cost credits even when a later route
        # (the registry) would have been free.
        for kind in ("esef", "edgar", "registry"):
            try:
                filing = json.loads((CACHE_DIR / f"{c.slug}_{kind}.json").read_text(encoding="utf-8"))["filing"]
                if filing and int(filing["period_end"][:4]) >= dt.date.today().year - 1:
                    return 0 if filing.get("language") in (None, "en") else per_company_cap
            except (OSError, ValueError, KeyError, TypeError):
                pass
        return per_company_cap

    # 2. Run them, up to `workers` at a time. A company only starts if the credits
    # spent plus the worst case of everything still running stay within --max-credits.
    factory = getattr(args, "executor_factory", None) or (
        _Inline if workers == 1 else
        (lambda: ProcessPoolExecutor(max_workers=workers, initializer=_worker_init,
                                     initargs=(workers,))))
    executor = factory()
    running: dict = {}
    stop_code, stop_message = 0, ""
    queue = list(todo)
    started: set[str] = set()
    reservation: dict[str, int] = {}      # company_id -> credits held back while it runs
    try:
        while queue or running:
            while queue and len(running) < workers and not stop_code:
                prefix, c = queue[0]
                # Fixed when each company starts: re-estimating mid-run drops to 0 as
                # soon as it caches its discovery, before its credits are counted.
                reserved = sum(reservation.values())
                if args.max_credits is not None and spent + reserved + worst_case(c) > args.max_credits:
                    if not running:
                        stop_code = -1
                        stop_message = (f"\nStopping: {spent} credits spent; the next company could "
                                        f"exceed --max-credits {args.max_credits}.")
                    break
                queue.pop(0)
                started.add(c.company_id)
                print(f"{prefix}: running...", flush=True)
                reservation[c.company_id] = worst_case(c)
                running[executor.submit(process_company, c, args.force, per_company_cap)] = (prefix, c)
            if not running:
                break
            done, _ = wait(list(running), return_when=FIRST_COMPLETED)
            for fut in done:
                prefix, c = running.pop(fut)
                reservation.pop(c.company_id, None)
                try:
                    res = fut.result()
                except Exception as e:  # noqa: BLE001 - a crashed worker: record, carry on
                    res = {"kind": "error", "credits": 0, "seconds": 0,
                           "error": f"worker crashed: {type(e).__name__}: {e}"}
                spent += res["credits"]
                if res["kind"] == "done":
                    counts[res["status"]] += 1
                    print(f"{prefix}: {res['status']} ({res['credits']} credits, {res['seconds']:.0f}s)")
                elif res["kind"] == "error":
                    counts["error"] += 1
                    print(f"{prefix}: ERROR {res['error']}")
                elif res["kind"] == "fatal":
                    stop_code = 2
                    stop_message = f"\nFATAL ({res['error']})\nStopping the batch."
                    print(stop_message, file=sys.stderr)
                elif res["kind"] == "offline":
                    stop_code = stop_code or 3
                    stop_message = (f"\nNo internet for {NETWORK_MAX_WAIT_S // 60} minutes. "
                                    f"Stopping; re-run the same command to continue.")
                write_summary(everyone, summary)          # after every company: crash-safe
            if stop_code > 0:
                queue.clear()                             # let running companies finish
    except KeyboardInterrupt:
        print("\nInterrupted. Re-run the same command to continue where it stopped.")
        executor.shutdown(wait=False, cancel_futures=True)
    else:
        executor.shutdown(wait=True)
    if stop_code == -1:
        print(stop_message)
    if getattr(args, "refresh", False):
        back = [c for _, c in todo if c.company_id not in started and restore_refresh(c)]
        if back:
            print(f"Not run, old result kept: {len(back)} compan{'y' if len(back) == 1 else 'ies'} "
                  f"(they keep their old status until refreshed again)")
    write_summary(everyone, summary)

    print(f"\nThis run: {spent} Firecrawl credits. "
          + ", ".join(f"{k} {v}" for k, v in counts.items() if v))
    print(f"Summary: {summary}")
    if stop_code > 0:
        print(stop_message)
        return stop_code
    try:   # fill-rate table over the whole list, not just this run's selection
        report = write_report(getattr(args, "all_companies", None) or companies,
                              OUTPUT_DIR / "fill_rate.md")
        print(f"Fill-rate report: {report}")
        if getattr(args, "sample", None):
            table = write_table(getattr(args, "sample_companies", None) or companies,
                                args.golden, OUTPUT_DIR / "monday_table.csv")
            print(f"Monday table: {table}")
    except Exception as e:  # noqa: BLE001 - a report problem must not hide the run's result
        log.warning("Could not write the fill-rate report: %s", e)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.batch",
                                description="Run the extractor over a CSV of companies.")
    p.add_argument("csv", type=Path, help="CSV with company_id, company_name, country_code")
    p.add_argument("--dry-run", action="store_true",
                   help="Only free lookups (GLEIF, Wikidata); estimate Firecrawl credits")
    p.add_argument("--limit", type=int, help="Only the first N companies")
    p.add_argument("--only", help="Comma-separated company_ids to run")
    p.add_argument("--sample", type=int, metavar="N",
                   help="Monday test: N companies per parse-route segment from the golden "
                        "dataset (fixed seed); writes output/sample_companies.csv and, at the "
                        "end, output/monday_table.csv")
    p.add_argument("--seed", type=int, default=7, help="Random seed for --sample (default 7)")
    p.add_argument("--golden", type=Path, default=PROJECT_ROOT / "golden_values.csv",
                   help="Golden dataset for --sample and the Monday table")
    p.add_argument("--max-credits", type=int,
                   help=f"Stop before Firecrawl spend could exceed this (assumes "
                        "the per-company cap as the worst case per company)")
    p.add_argument("--workers", type=int, default=1,
                   help="Companies processed at the same time (default 1; 3 is a good "
                        "choice on a normal laptop)")
    p.add_argument("--retry-failed", action="store_true", help="Retry companies that failed before")
    p.add_argument("--force", action="store_true", help="Redo everything, ignoring results and caches")
    p.add_argument("--refresh", action="store_true",
                   help="Redo already-processed companies under the current rules; keeps "
                        "cached reports that still pass (0 credits), re-finds the rest")
    p.add_argument("--max-credits-per-company", type=int, default=DEFAULT_MAX_CREDITS_PER_COMPANY,
                   help=f"Firecrawl credit cap per company (default {DEFAULT_MAX_CREDITS_PER_COMPANY})")
    args = p.parse_args(argv)

    OUTPUT_DIR.mkdir(exist_ok=True)
    _setup_logging()
    try:
        companies = read_companies(args.csv)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    args.all_companies = companies
    if args.sample:
        try:
            golden = load_golden(args.golden)
        except OSError as e:
            print(f"ERROR: golden dataset: {e}", file=sys.stderr)
            return 1
        companies = pick_sample(companies, golden, args.sample, args.seed)
        write_sample(companies, OUTPUT_DIR / "sample_companies.csv")
        args.sample_companies = list(companies)       # the Monday table covers all of them
        per_seg = {}
        for c in companies:
            per_seg[c.segment] = per_seg.get(c.segment, 0) + 1
        print(f"Sample: {per_seg} (saved to output/sample_companies.csv)")
    if args.only:
        wanted = {x.strip() for x in args.only.split(",")}
        companies = [c for c in companies if c.company_id in wanted]
    if args.limit:
        companies = companies[:args.limit]
    print(f"{len(companies)} companies from {args.csv}")

    if args.dry_run:
        dry_run(companies, OUTPUT_DIR / "dry_run.csv")
        return 0
    with _KeepAwake():
        return run_batch(companies, args)


if __name__ == "__main__":
    sys.exit(main())
