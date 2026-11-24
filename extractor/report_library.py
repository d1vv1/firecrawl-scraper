"""Reports already on disk: the FY2025 "2025 Reports" folder (Google Drive download).

When a company's annual or remuneration report is in that folder, the collector reads
it from disk instead of searching for it with Firecrawl; a company that is not there
is searched for with Firecrawl as before. The folder comes from LOCAL_REPORTS_DIR
(.env) or --local-reports.

The folder's 00_START_HERE.xlsx ("Index" and "Missing" sheets) is converted once to
cache/local_reports_index.json, and rebuilt when the xlsx changes.

Lookup, most exact first:
  1. LEI (20 characters), when the company list has one;
  2. company name (+ country): case, accents, punctuation and legal forms (AG, ASA,
     A/S, plc...) ignored, with a fuzzy fallback for small typos. The fuzzy step is for
     find() and the command line only: attach() takes LEI, exact and legal-form matches
     only, so the collector never reads another company's report.
If nothing is found, the "Missing" sheet says why.

    python -m extractor.report_library --company "Kuhne Nagel" --country CH
    python -m extractor.report_library --lei 5493008H3828EMEXB082
    python -m extractor.report_library --rebuild-json
"""
from __future__ import annotations

import argparse
import difflib
import json
import logging
import os
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass, field, asdict

from pathlib import Path

from .config import CACHE_DIR, PROJECT_ROOT

log = logging.getLogger(__name__)

INDEX_FILE = "00_START_HERE.xlsx"
DEFAULT_JSON = str(CACHE_DIR / "local_reports_index.json")


def default_root() -> str | None:
    """LOCAL_REPORTS_DIR from the environment or .env; None when not set."""
    if not os.getenv("LOCAL_REPORTS_DIR"):
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env", override=False)
    return os.getenv("LOCAL_REPORTS_DIR") or None

# Legal-form and filler words dropped to get a company's "core" name.
LEGAL_WORDS = {
    "ab", "ag", "as", "asa", "bv", "co", "corp", "corporation", "company", "cv",
    "gmbh", "group", "holding", "holdings", "inc", "kgaa", "limited", "ltd", "nv", "oy",
    "oyj", "plc", "publ", "sa", "sab", "sas", "se", "sgps", "spa", "the", "kg",
    "hf", "aps", "llc", "srl", "bhd", "tbk", "and", "sad",
    "aktiengesellschaft",       # 'HOCHTIEF Aktiengesellschaft' = 'HOCHTIEF AG'
    "cokgaa", "cokg",           # 'Henkel Ag+co.kgaa': the dot joins 'co' and 'kgaa'
}

COUNTRY_ALIASES = {
    "uk": "GB", "u.k.": "GB", "great britain": "GB", "britain": "GB", "england": "GB",
    "scotland": "GB", "wales": "GB", "united kingdom": "GB",
    "usa": "US", "u.s.": "US", "u.s.a.": "US", "united states": "US", "america": "US",
    "holland": "NL", "the netherlands": "NL", "netherlands": "NL",
    "deutschland": "DE", "germany": "DE", "sverige": "SE", "sweden": "SE",
    "norge": "NO", "norway": "NO", "danmark": "DK", "denmark": "DK",
    "suomi": "FI", "finland": "FI", "schweiz": "CH", "suisse": "CH", "switzerland": "CH",
    "osterreich": "AT", "austria": "AT", "espana": "ES", "spain": "ES",
    "italia": "IT", "italy": "IT", "hellas": "GR", "greece": "GR", "belgium": "BE",
    "belgie": "BE", "belgique": "BE", "portugal": "PT", "france": "FR", "poland": "PL",
    "ireland": "IE", "australia": "AU", "bermuda": "BM", "indonesia": "ID",
    "south africa": "ZA", "luxembourg": "LU", "iceland": "IS",
}

LEI_RE = re.compile(r"^[A-Z0-9]{18}[0-9]{2}$")


def strip_accents(s: str) -> str:
    s = s.replace("ß", "ss").replace("æ", "ae").replace("Æ", "AE").replace("ø", "o").replace("Ø", "O")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_name(s: str) -> str:
    """'Chocoladefabriken Lindt & Sprüngli AG' -> 'chocoladefabriken lindt and sprungli ag'."""
    s = strip_accents(str(s or "")).casefold()
    # spaced initials too: 'S. A.' -> 'S.A.' (Colonial SFL, Socimi S. A.)
    # (single letters on their own only: 'B.f. S.p.a' stays 'bf spa')
    s = re.sub(r"(?<![a-z0-9.])([a-z])\.\s+(?=[a-z]\.?(?:\s|,|$))", r"\1.", s)
    # dots and slashes join letters: 'S.A.' -> 'sa', 'N.V' -> 'nv', 'A/S' -> 'as'
    s = s.replace("&", " and ").replace("+", " and ").replace("/", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    # German listing tags after the name, one or more: 'FIRST SENSOR AG O.N.', 'X AG NA O.N.', 'Y INH ON'
    return re.sub(r"(?<=\S)(?: (?:on|inh|na|vna))+$", "", s)


def core_name(s: str) -> str:
    """Normalised name without legal-form words: 'Siemens AG' -> 'siemens'."""
    toks = norm_name(s).split()
    return " ".join([t for t in toks if t not in LEGAL_WORDS] or toks)


@dataclass
class Report:
    company: str
    country: str
    region: str
    report_type: str
    format: str
    file_name: str
    path: str
    lei: str | None
    cdp_company_id: str | None
    period_end: str | None
    drive_link: str | None
    in_scope_28Oct: str | None


@dataclass
class Match:
    report: Report
    score: float
    matched_by: str  # "lei" | "name-exact" | "name-core" | "name-fuzzy"

    @property
    def path(self) -> str:
        return self.report.path


@dataclass
class Result:
    matches: list[Match] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def paths(self) -> list[str]:
        return [m.path for m in self.matches]

    def __bool__(self) -> bool:
        return bool(self.matches)


def _cell(v):
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()[:10]
    s = str(v).strip()
    return s or None


ADDITIONS_FILE = "00_ADDITIONS.json"   # reports added after the Drive download (find_rem_reports)


def additions_mtime(root: str) -> float | None:
    p = os.path.join(root, ADDITIONS_FILE)
    return os.path.getmtime(p) if os.path.exists(p) else None


def additions(root: str) -> list[dict]:
    """Index rows for reports saved into the folder later; same columns as the xlsx Index."""
    p = os.path.join(root, ADDITIONS_FILE)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [{k: _cell(v) for k, v in d.items()} for d in json.load(f).get("index", [])]


def add_report(root: str, row: dict) -> None:
    """Record one saved report in 00_ADDITIONS.json (replacing a row for the same file);
    the JSON index picks it up on its next load."""
    _update_additions(root, lambda rows: [d for d in rows if d.get("file_name") != row["file_name"]] + [row])


def remove_report(root: str, file_name: str, delete_file: bool = True) -> int:
    """Drop a wrongly saved report: its 00_ADDITIONS.json row and, by default, the file
    (only one recorded there: never a Drive file). Returns the rows removed."""
    gone = [d for d in additions(root) if d.get("file_name") == file_name]
    if not gone:
        return 0
    _update_additions(root, lambda rows: [d for d in rows if d.get("file_name") != file_name])
    if delete_file:
        for p in Path(root).rglob(file_name):
            if p.is_file() and ("Remuneration" in p.parts or "Annual" in p.parts):
                p.unlink()
    return len(gone)


def _update_additions(root: str, change) -> None:
    """Read-change-write 00_ADDITIONS.json under its lock file."""
    import time
    p = os.path.join(root, ADDITIONS_FILE)
    lock = p + ".lock"
    # several runs (countries, steps) add reports at once: one writer at a time, or a
    # read-change-write loses the other's rows
    for _ in range(600):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if time.time() - os.path.getmtime(lock) > 120:    # left by a killed run
                try:
                    os.remove(lock)
                except OSError:
                    pass
            time.sleep(0.2)
    else:
        raise TimeoutError(f"{lock} held for too long")
    try:
        doc = {"index": []}
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                doc = json.load(f)
        doc["index"] = change(doc["index"])
        tmp = f"{p}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        os.replace(tmp, p)
    finally:
        os.close(fd)
        os.remove(lock)


def build_json(root: str, out: str = DEFAULT_JSON, index_file: str = INDEX_FILE) -> dict:
    """Convert the Index and Missing sheets of 00_START_HERE.xlsx to JSON.

    Each Index row gets 'rel_path' (path under root) found by scanning the folder,
    or null when the file is not on disk.
    """
    import openpyxl

    xlsx = os.path.join(root, index_file)
    on_disk: dict[str, str] = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            on_disk.setdefault(f, os.path.relpath(os.path.join(dp, f), root))

    def sheet(wb, name):
        if name not in wb.sheetnames:
            return []
        rows = wb[name].iter_rows(values_only=True)
        head = [str(h).strip() for h in next(rows)]
        return [{k: _cell(v) for k, v in zip(head, r)} for r in rows if any(r)]

    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    try:
        index, missing = sheet(wb, "Index"), sheet(wb, "Missing")
    finally:
        wb.close()
    index += additions(root)
    for d in index:
        d["rel_path"] = on_disk.get(d.get("file_name") or "")
    doc = {"source": xlsx, "source_mtime": os.path.getmtime(xlsx), "root": os.path.abspath(root),
           "additions_mtime": additions_mtime(root), "index": index, "missing": missing}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    import threading
    import time
    tmp = f"{out}.{os.getpid()}-{threading.get_ident()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    # another process (a parallel run) may have the cache open: Windows then refuses the
    # replace. Retry a while; the cache is only a speed-up, so give up quietly after that.
    for _ in range(50):
        try:
            os.replace(tmp, out)
            break
        except PermissionError:
            time.sleep(0.2)
    else:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return doc


class ReportRetriever:
    def __init__(self, root: str, index_json: str = DEFAULT_JSON, index_file: str = INDEX_FILE):
        """Loads reports_index.json; rebuilds it from the xlsx when missing or out of date."""
        self.root = os.path.abspath(root)
        self.reports: list[Report] = []
        self.missing: list[dict] = []
        self.not_on_disk: list[dict] = []
        self._country_names: dict[str, str] = {}  # 'belgium' -> 'BE', taken from the folder layout
        xlsx = os.path.join(self.root, index_file)
        doc = None
        if os.path.exists(index_json):
            with open(index_json, encoding="utf-8") as f:
                doc = json.load(f)
            stale = (os.path.exists(xlsx) and doc.get("source_mtime") != os.path.getmtime(xlsx)) \
                or os.path.normcase(doc.get("root", "")) != os.path.normcase(self.root) \
                or doc.get("additions_mtime") != additions_mtime(self.root)
            if stale:
                doc = None
        if doc is None:
            doc = build_json(self.root, index_json, index_file)
        self._load(doc)

    # ---------------------------------------------------------------- loading
    def _load(self, doc: dict) -> None:
        for d in doc["index"]:
            rel = d.get("rel_path")
            path = os.path.join(self.root, rel) if rel else None
            if not path or not os.path.exists(path):
                self.not_on_disk.append(d)  # never return a dead path
                continue
            country = (d.get("country") or "").upper()
            parts = rel.replace("/", os.sep).split(os.sep)
            if len(parts) >= 3 and country:
                self._country_names.setdefault(norm_name(parts[1]), country)
            self.reports.append(Report(
                company=d.get("company") or "", country=country, region=d.get("region") or "",
                report_type=d.get("report_type") or "", format=(d.get("format") or "").lower(),
                file_name=d.get("file_name") or "", path=path, lei=(d.get("lei") or "").upper() or None,
                cdp_company_id=d.get("cdp_company_id"), period_end=d.get("period_end"),
                drive_link=d.get("drive_link"), in_scope_28Oct=d.get("in_scope_28Oct"),
            ))
        self.missing = doc.get("missing", [])

        for r in self.reports:
            r._norm = norm_name(r.company)  # type: ignore[attr-defined]
            r._core = core_name(r.company)  # type: ignore[attr-defined]

    # ---------------------------------------------------------------- helpers
    def country_code(self, country: str | None) -> str | None:
        """Accepts 'DE', 'de', 'Germany', 'UK', 'United Kingdom' -> ISO-2 code."""
        if not country:
            return None
        c = country.strip()
        if len(c) == 2 and c.isalpha():
            return "GB" if c.upper() == "UK" else c.upper()
        n = norm_name(c)
        code = self._country_names.get(n) or COUNTRY_ALIASES.get(n) or COUNTRY_ALIASES.get(c.casefold())
        if not code:
            raise ValueError(f"Unknown country: {country!r}. Use an ISO-2 code like 'DE' or a name like 'Germany'.")
        return code

    @staticmethod
    def _filter(reports, report_type=None, formats=None):
        if report_type:
            reports = [r for r in reports if r.report_type.casefold() == report_type.casefold()]
        if formats:
            fs = {f.lower().lstrip(".") for f in formats}
            reports = [r for r in reports if r.format in fs]
        return reports

    # ---------------------------------------------------------------- main API
    def find(self, company: str | None = None, country: str | None = None, lei: str | None = None,
             report_type: str | None = None, formats: list[str] | tuple[str, ...] | None = None,
             min_score: float = 0.85) -> Result:
        """Return matching report files, best first.

        - lei: tried first. If it matches, company name is not needed.
        - company + country: name match restricted to that country.
        - report_type: 'Annual' or 'Remuneration'. formats: e.g. ['pdf'].
        """
        if not (company or lei):
            raise ValueError("Give at least a company name or an LEI.")
        res = Result()
        cc = self.country_code(country)

        # 1) LEI
        if lei:
            lei_n = re.sub(r"\s+", "", lei).upper()
            if not LEI_RE.match(lei_n):
                res.notes.append(f"'{lei}' is not a valid 20-character LEI; ignored.")
            else:
                hits = [r for r in self.reports if r.lei == lei_n]
                if cc:
                    other = [r for r in hits if r.country != cc]
                    hits = [r for r in hits if r.country == cc]
                    if other and not hits:
                        res.notes.append(f"LEI {lei_n} is filed under {sorted({r.country for r in other})}, not {cc}.")
                hits = self._filter(hits, report_type, formats)
                if hits:
                    res.matches = [Match(r, 1.0, "lei") for r in hits]
                    if company and core_name(company) not in {r._core for r in hits} and \
                            max(difflib.SequenceMatcher(None, core_name(company), r._core).ratio() for r in hits) < 0.6:
                        res.notes.append(f"LEI belongs to {sorted({r.company for r in hits})}, which differs from '{company}'.")
                    return self._sorted(res)
                res.notes.append(f"No file with LEI {lei_n}" + (f" in {cc}" if cc else "") + "; trying company name.")

        # 2) company name
        if company:
            pool = [r for r in self.reports if not cc or r.country == cc]
            pool = self._filter(pool, report_type, formats)
            res.matches = self._name_matches(company, pool, min_score)
            names = sorted({(m.report.company, m.report.country) for m in res.matches})
            if len(names) > 1 and res.matches[0].matched_by == "name-fuzzy":
                res.notes.append(f"'{company}' matches {len(names)} companies; add country or use the full name/LEI: "
                                 + ", ".join(f"{c} ({k})" for c, k in names[:8]))
            if not res.matches and cc:
                elsewhere = self._name_matches(company, self._filter(self.reports, report_type, formats), min_score)
                if elsewhere:
                    res.notes.append(f"'{company}' not found in {cc} but exists in "
                                     f"{sorted({m.report.country for m in elsewhere})}.")
            if not res.matches:
                res.notes.extend(self._missing_reason(company, cc))
        return self._sorted(res)

    def _name_matches(self, company: str, pool: list[Report], min_score: float) -> list[Match]:
        q_norm, q_core = norm_name(company), core_name(company)
        exact = [Match(r, 1.0, "name-exact") for r in pool if r._norm == q_norm]
        q_flat = q_core.replace(" ", "")  # "St.Galler" = "St Galler"
        core = [Match(r, 0.97, "name-core") for r in pool
                if r._norm != q_norm and q_core
                and (r._core == q_core or r._core.replace(" ", "") == q_flat)]
        if exact or core:
            # both: a report added under the tracker's spelling ('BASIC-FIT') must not hide
            # the Drive's annual report ('Basic-Fit NV'); exact matches first
            return exact + core
        # fuzzy: best company only, so 'Telia' does not also return 'Telenor'
        scored: dict[str, float] = {}
        for r in pool:
            if r.company in scored:
                continue
            s = difflib.SequenceMatcher(None, q_core, r._core).ratio()
            # every query word appears in the name ('Kuhne Nagel' -> 'Kuhne + Nagel International AG')
            q_toks, r_toks = set(q_core.split()), set(r._core.split())
            if q_toks and q_toks <= r_toks and max(map(len, q_toks)) >= 4:
                s = max(s, 0.9)
            scored[r.company] = s
        if not scored:
            return []
        best = max(scored.values())
        if best < min_score:
            return []
        winners = {c for c, s in scored.items() if s == best}
        return [Match(r, round(best, 3), "name-fuzzy") for r in pool if r.company in winners]

    def _missing_reason(self, company: str, cc: str | None) -> list[str]:
        q = core_name(company)
        out = []
        for m in self.missing:
            if cc and str(m.get("country") or "").upper() != cc:
                continue
            if core_name(m.get("company")) == q or norm_name(m.get("company")) == norm_name(company):
                out.append(f"Listed on the Missing sheet: {m.get('company')} ({m.get('country')}): {m.get('check_result')}")
        return out or [f"No report found for '{company}'" + (f" in {cc}" if cc else "") + "."]

    @staticmethod
    def _sorted(res: Result) -> Result:
        res.matches.sort(key=lambda m: (-m.score, m.report.company, m.report.report_type, m.report.format != "pdf", m.report.file_name))
        return res

    def suggest(self, company: str, country: str | None = None, n: int = 5) -> list[tuple[str, str, float]]:
        """Closest company names, for 'did you mean' when find() returns nothing."""
        cc = self.country_code(country)
        q = core_name(company)
        seen = {}
        for r in self.reports:
            if cc and r.country != cc:
                continue
            seen[(r.company, r.country)] = max(seen.get((r.company, r.country), 0),
                                               difflib.SequenceMatcher(None, q, r._core).ratio())
        return sorted(((c, k, round(s, 3)) for (c, k), s in seen.items()), key=lambda x: -x[2])[:n]


# -------------------------------------------------------------------- collector hook
SAFE_MATCHES = {"lei", "name-exact", "name-core"}   # never a fuzzy guess for the collector
FORMAT_ORDER = ("pdf", "xhtml", "html")              # pdf first: pages for the quotes; no zip


def _local_reports(lib: ReportRetriever, name: str, country: str | None, lei: str | None
                   ) -> tuple[dict[str, Report], str]:
    """{'Annual': Report, 'Remuneration': Report} on disk for one company, and how it was
    matched ('' when not found). An LEI match ignores the country (Telia files its annual
    report in FI and its remuneration report in SE); a name match keeps it."""
    res = None
    if lei:
        res = lib.find(company=name, lei=lei)
        if not (res and res.matches[0].matched_by == "lei"):
            res = None
    if res is None:
        try:
            res = lib.find(company=name, country=country)
        except ValueError:          # a country the library doesn't know
            return {}, ""
    hits = [m for m in res.matches if m.matched_by in SAFE_MATCHES]
    # one company. An LEI match is one company whatever the spellings ('Arcadis NV' in the
    # Drive index, 'ARCADIS' on a report added from the tracker; 'Cenergy' and 'Cenergy
    # Holdings SA'). A name match: names compared without legal forms ('Piraeus Bank S.A.'
    # = 'Piraeus Bank SA'), and spaces too ("De'Longhi" = 'DeLonghi SpA').
    if not hits or (hits[0].matched_by != "lei" and len({core_name(m.report.company).replace(" ", "") for m in hits}) != 1):
        return {}, ""               # nothing, or two different companies: Firecrawl decides
    if hits[0].matched_by == "lei" and country:
        # an LEI match also takes the same company's rows that carry no LEI (a report saved
        # from the web: Basic-Fit's remuneration report next to its Drive annual report)
        try:
            more = lib.find(company=name, country=country).matches
        except ValueError:
            more = []
        seen = {m.report.path for m in hits}
        hits += [m for m in more if m.matched_by in ("name-exact", "name-core")
                 and not m.report.lei and m.report.path not in seen]
    out = _pick(m.report for m in hits)
    return out, (hits[0].matched_by if out else "")


def _pick(reports) -> dict[str, Report]:
    out: dict[str, Report] = {}
    reports = list(reports)
    for kind in ("Annual", "Remuneration"):
        files = [r for r in reports if r.report_type == kind and r.format in FORMAT_ORDER]
        files.sort(key=lambda r: (FORMAT_ORDER.index(r.format), len(r.file_name), r.file_name))
        if files:
            out[kind] = files[0]
    return out


# share-class tags after a name: 'SEB A', 'Sagax D', 'Corem Property Pref', 'Ponsse 1',
# 'Alvotech SDB', 'Ser. B'. One company's pay report covers all its share lines.
SHARE_CLASS = {"a", "b", "c", "d", "r", "pref", "pr", "sdb", "ser", "1", "2",
               # German and Swiss lines: Vz/VzO/Vorzüge (preferred), St (ordinary), PS
               # (participation certificate), N/I (registered/bearer): 'SIXT SE ST O.N.',
               # 'SARTORIUS AG VZO O.N.', 'Schindler PS', 'Swatch Group I'
               "vz", "vzo", "vorzuge", "vorzugsaktien", "st", "stamm", "stammaktien",
               "ps", "n", "i", "inh", "nam"}
# German listing tags, wherever they sit among the share-class tags ('HERMLE O.N. VZO',
# 'FAIR VALUE REIT-AG INH.ON'); 'EO 5' is the nominal value ('PROCREDIT HOLDING AG NA EO 5')
LISTING_TAGS = {"on", "inh", "na", "vna", "inhon", "nam", "vinkna", "vink"}   # VINK.NA.: restricted registered
_NOMINAL = re.compile(r"(?: eo(?: \d+)+)+$")
# words a tracker name may add to the folder's shorter one: 'PowerCell Sweden AB' = 'PowerCell',
# 'Orrön Energy AB' = 'Orrön', 'Infant Bacterial Therapeutics AB' = 'Infant Bacterial'
NAME_EXTRAS = {"sweden", "norway", "denmark", "finland", "iceland", "energy", "therapeutics", "nordic",
               "technologies"}     # 'Cicor Technologies Ltd.' = 'Cicor'
NORDIC = {"SE", "NO", "DK", "FI", "IS"}


def class_free(s: str) -> list[str]:
    """core_name words without share-class and listing tags: 'SEB A' -> ['seb'],
    'Kesko B' -> ['kesko'], 'MASCHINENFABRIK BERTHOLD HERMLE O.N. VZO' -> [..., 'hermle'],
    'PROCREDIT HOLDING AG NA EO 5' -> ['procredit']."""
    toks = _NOMINAL.sub("", core_name(s)).split()
    while len(toks) > 1 and (toks[-1] in SHARE_CLASS or toks[-1] in LISTING_TAGS):
        toks.pop()
        toks = _NOMINAL.sub("", " ".join(toks)).split()
    return toks


def _umlaut_free(t: str) -> str:
    """'baer' = 'bar' ('Julius Bär' in the tracker, 'Julius Baer' in the folder)."""
    for digraph, single in (("ae", "a"), ("oe", "o"), ("ue", "u")):
        t = t.replace(digraph, single)
    return t


def _same_company(q: list[str], r: list[str], extras: bool) -> bool:
    if "".join(q) == "".join(r) or _umlaut_free("".join(q)) == _umlaut_free("".join(r)):
        return True
    # an abbreviated last word in the tracker: 'FORTEC ELEKTRO. O.N.' = 'FORTEC Elektronik AG'
    if (len(q) == len(r) >= 2 and q[:-1] == r[:-1] and len(q[-1]) >= 4
            and r[-1].startswith(q[-1]) and len("".join(q)) >= 8):
        return True
    return (extras and 0 < len(r) < len(q) and q[:len(r)] == r and len("".join(r)) >= 5
            and all(t in NAME_EXTRAS for t in q[len(r):]))


def local_reports(lib: ReportRetriever, name: str, country: str | None, lei: str | None
                  ) -> tuple[dict[str, Report], str]:
    """As _local_reports, then for the kinds still missing: the same company under another
    share line or spelling in the same country ('SEB A' -> 'Seb C', 'Sagax D' -> 'Sagax AB'),
    and in the Nordics the pay report also in a neighbouring country ('SSAB B' FI -> 'Ssab AB' SE;
    'Stora Enso A' SE -> 'Stora Enso Oyj' FI): matched by 'name-class'."""
    out, how = _local_reports(lib, name, country, lei)
    if "Remuneration" in out and "Annual" in out:
        return out, how
    try:
        cc = lib.country_code(country)
    except ValueError:
        return out, how
    q = class_free(name)
    if not cc or not q:
        return out, how
    pools = [[r for r in lib.reports if r.country == cc and _same_company(q, class_free(r.company), True)]]
    if cc in NORDIC:      # the pay report only: an annual report found by name keeps its country
        pools.append([r for r in lib.reports if r.country in NORDIC and r.country != cc
                      and r.report_type == "Remuneration" and _same_company(q, class_free(r.company), False)])
    for pool in pools:
        for kind, rep in _pick(pool).items():
            if kind not in out:
                out[kind] = rep
                how = how or "name-class"
    return out, how


def attach(targets, root: str, index_json: str = DEFAULT_JSON) -> dict[str, int]:
    """Point each target's empty annual_report_url / remuneration_report_url at the copy
    on disk (a file: URI, read with no search and no Firecrawl credits). Links already in
    the company list win. A company not in the folder is left alone: the collector then
    searches for its reports with Firecrawl as before.

    Targets are datapoints.Target (duck-typed: .company.name/.country/.lei, the two URLs)."""
    lib = ReportRetriever(root, index_json)
    stats = {"companies": 0, "annual": 0, "remuneration": 0, "not_found": 0}
    for t in targets:
        if t.annual_report_url and t.remuneration_report_url:
            continue
        c = t.company
        found, how = local_reports(lib, c.name, c.country, c.lei)
        if not found:
            stats["not_found"] += 1
            continue
        stats["companies"] += 1
        if "Annual" in found and not t.annual_report_url:
            t.annual_report_url = Path(found["Annual"].path).resolve().as_uri()
            stats["annual"] += 1
        if "Remuneration" in found and not t.remuneration_report_url:
            t.remuneration_report_url = Path(found["Remuneration"].path).resolve().as_uri()
            stats["remuneration"] += 1
        # the report step reads a supplied file instead of searching (as read_targets does)
        if t.annual_report_url and t.annual_report_url.startswith("file:") and not c.report_url:
            c.report_url = t.annual_report_url
        log.info("%s: local reports by %s: %s", c.company_id, how,
                 ", ".join(f"{k} {r.file_name}" for k, r in found.items()))
    return stats


# -------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Find FY2025 company report files by company, country and/or LEI.")
    p.add_argument("--company", "-c")
    p.add_argument("--country", "-k", help="ISO-2 code or name, e.g. DE or Germany")
    p.add_argument("--lei", "-l")
    p.add_argument("--type", "-t", dest="report_type", choices=["Annual", "Remuneration"])
    p.add_argument("--format", "-f", dest="formats", action="append", help="pdf, xhtml, html, zip (repeatable)")
    p.add_argument("--root", default=default_root(), help="the 2025 Reports folder (default: LOCAL_REPORTS_DIR)")
    p.add_argument("--index-json", default=DEFAULT_JSON)
    p.add_argument("--rebuild-json", action="store_true", help="re-convert 00_START_HERE.xlsx to JSON and exit if no query")
    p.add_argument("--copy-to", help="copy matched files into this folder")
    p.add_argument("--open", action="store_true", help="open the first match with the default app")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if not a.root:
        p.error("set LOCAL_REPORTS_DIR in .env or pass --root")
    if a.rebuild_json:
        doc = build_json(a.root, a.index_json)
        print(f"wrote {a.index_json}: {len(doc['index'])} index rows, {len(doc['missing'])} missing rows")
        if not (a.company or a.lei):
            return 0
    if not (a.company or a.lei):
        p.error("give --company and/or --lei")

    r = ReportRetriever(a.root, a.index_json)
    res = r.find(company=a.company, country=a.country, lei=a.lei, report_type=a.report_type, formats=a.formats)

    if a.json:
        print(json.dumps({"matches": [dict(asdict(m.report), score=m.score, matched_by=m.matched_by) for m in res.matches],
                          "notes": res.notes}, ensure_ascii=False, indent=1))
    else:
        for n in res.notes:
            print("note:", n)
        for m in res.matches:
            rp = m.report
            print(f"[{m.matched_by} {m.score:.2f}] {rp.company} | {rp.country} | {rp.report_type} | {rp.format}\n    {rp.path}")
        if not res and a.company:
            print("did you mean:", ", ".join(f"{c} ({k})" for c, k, _ in r.suggest(a.company, a.country)))
    if a.copy_to and res:
        os.makedirs(a.copy_to, exist_ok=True)
        for m in res.matches:
            dst = os.path.join(a.copy_to, m.report.file_name)
            if not os.path.exists(dst):
                shutil.copy2(m.path, dst)
        print(f"copied {len(res.matches)} file(s) to {os.path.abspath(a.copy_to)}")
    if a.open and res:
        os.startfile(res.matches[0].path)  # type: ignore[attr-defined]
    return 0 if res else 1


if __name__ == "__main__":
    sys.exit(main())
