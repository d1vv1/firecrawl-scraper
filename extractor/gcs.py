"""Reports already in the CDP bucket: use them instead of searching the web.

    python -m extractor.gcs sync          # mirror every company's metadata.json (no reports)
    python -m extractor.gcs find "BHG Group AB" --country SE

The bucket (gs://allshares-data-ingest-cdp-pipeline/uploads/, layout in the GCS storage
kit's GCS_REPORT_STORAGE_SETUP.md) holds one folder per company:
`{region}/{country}/{company_type}/{company_id}--{slug}/metadata.json` and `fy{YYYY}/<report>`.
Each metadata.json lists the files, and its `coverage` names the file that is the year's
annual report and remuneration report ("found"), or the file that contains it ("covered_by").

- `sync()` mirrors the metadata files to cache/gcs/uploads/ (small; the reports are not
  downloaded). `records()` reads the mirror.
- `Matcher` finds a company's record: its CDP id, the id without its 8-hex suffix (the
  tracker id), the ISIN or LEI, then the name without legal words in the same country.
- `documents(record)` gives the gs:// links of the year's annual and remuneration report.
- An input link `gs://...` is read like a report on disk: `local_uri()` names the file it
  will be at in cache/gcs/, and `fetch()` downloads it once (`ensure()` for a company).

Access goes through the gcloud CLI, signed in as a user with read access to the bucket
(`gcloud auth login`); the service account in .env has none. Nothing is written to the bucket.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

from .cdp_slug import strip_legal
from .config import PROJECT_ROOT

BUCKET = os.environ.get("GCS_BUCKET", "allshares-data-ingest-cdp-pipeline")
PREFIX = os.environ.get("GCS_PREFIX", "uploads").strip("/")
CACHE = PROJECT_ROOT / "cache" / "gcs"
MIRROR = CACHE / PREFIX
FISCAL_YEAR = "fy2025"
MAX_AGE_HOURS = 24
# Reports are not mirrored by sync(): only the metadata and the index.
# "(?x) " (verbose regex: the space is ignored) makes the argument contain a space, so it
# is passed in quotes: gcloud is a .cmd on Windows, and cmd.exe takes a bare | as a pipe.
_NOT_METADATA = r"(?x) .*\.(pdf|PDF|xhtml|XHTML|html?|HTML?|zip|md|MD)$"


class GcsError(RuntimeError):
    pass


def _gcloud() -> str:
    exe = shutil.which("gcloud") or shutil.which("gcloud.cmd")
    if not exe:
        raise GcsError("gcloud CLI not found: install the Google Cloud SDK and run gcloud auth login")
    return exe


def _run(args: list[str], timeout: int = 900) -> str:
    try:
        # gcloud (Python) prints in the console code page when its output is captured,
        # and crashes on file names like "Ersättningsrapport": force UTF-8
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        # no stdin: a sign-in prompt fails at once instead of waiting for an answer
        p = subprocess.run([_gcloud(), "storage", *args], capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace", env=env,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired as e:
        raise GcsError(f"gcloud storage {args[0]} timed out") from e
    if p.returncode != 0:
        raise GcsError(f"gcloud storage {args[0]} failed: {(p.stderr or p.stdout).strip()[-400:]}")
    return p.stdout


def sync(force: bool = False) -> Path:
    """Mirror the bucket's metadata.json files and index (not the reports) to MIRROR. Done
    at most once a day unless `force`."""
    stamp = CACHE / ".synced"
    if not force and stamp.exists() and time.time() - stamp.stat().st_mtime < MAX_AGE_HOURS * 3600:
        return MIRROR
    MIRROR.mkdir(parents=True, exist_ok=True)
    _run(["rsync", "-r", f"gs://{BUCKET}/{PREFIX}", str(MIRROR), f"--exclude={_NOT_METADATA}"])
    stamp.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), encoding="utf-8")
    return MIRROR


def records(mirror: Path = MIRROR) -> list[dict]:
    """Every company's metadata.json in the mirror, with `_folder` (its path under PREFIX)."""
    out = []
    for f in sorted(mirror.glob("*/*/*/*/metadata.json")):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rec["_folder"] = f.parent.relative_to(mirror).as_posix()
        out.append(rec)
    return out


def _name_key(country: str, name: str) -> str:
    return f"{(country or '').lower()}|{strip_legal(name or '')}"


class Matcher:
    """A company in the input -> its bucket record (or None)."""

    def __init__(self, recs: list[dict]):
        self.by_id: dict[str, dict] = {}
        self.by_bare: dict[str, list[dict]] = defaultdict(list)
        self.by_isin: dict[str, dict] = {}
        self.by_lei: dict[str, dict] = {}
        self.by_name: dict[str, list[dict]] = defaultdict(list)
        for r in recs:
            cid = r.get("company_id") or ""
            self.by_id[cid] = r
            self.by_bare[re.sub(r"-[0-9a-f]{8}$", "", cid)].append(r)
            ids = r.get("identifiers") or {}
            for isin in ids.get("isin") or []:
                self.by_isin[isin.upper()] = r
            if ids.get("lei"):
                self.by_lei[ids["lei"].upper()] = r
            self.by_name[_name_key(r.get("country", ""), r.get("name", ""))].append(r)

    def __call__(self, company_id: str = "", name: str = "", country: str = "",
                 isin: str = "", lei: str = "", tracker_id: str = "") -> tuple[dict | None, str]:
        """(record, how it was matched); (None, why not)."""
        for cid in (company_id, tracker_id):
            if cid and cid in self.by_id:
                return self.by_id[cid], "company_id"
        for cid in (tracker_id, company_id):
            hits = self.by_bare.get(cid or "", [])
            if len(hits) == 1:
                return hits[0], "id without its suffix"
        if isin and isin.upper() in self.by_isin:
            return self.by_isin[isin.upper()], "ISIN"
        if lei and lei.upper() in self.by_lei:
            return self.by_lei[lei.upper()], "LEI"
        hits = self.by_name.get(_name_key(country, name), [])
        if not hits:
            # a share-series number in the tracker's name: "Ponsse 1", "Ilkka 2"
            hits = self.by_name.get(_name_key(country, re.sub(r"\s+\d$", "", name or "")), [])
        if len(hits) == 1:
            return hits[0], "name"
        if len(hits) > 1:
            return None, f"name matches {len(hits)} bucket companies"
        return None, "not in the bucket"


def gs_uri(record: dict, file_name: str, fiscal_year: str) -> str:
    return f"gs://{BUCKET}/{PREFIX}/{record['_folder']}/{fiscal_year}/{file_name}"


def documents(record: dict, fiscal_year: str = FISCAL_YEAR) -> dict[str, str | None]:
    """{"annual": gs://..., "remuneration": gs://...} for the year: the file coverage says
    is that report ("found"). A remuneration report covered by the annual report gives no
    separate link: the annual report is read for pay anyway. A PDF is preferred to an
    ESEF .xhtml of the same report when both are current."""
    cov = (record.get("coverage") or {}).get(fiscal_year) or {}
    files = [f for f in record.get("files") or []
             if f.get("fiscal_year") == fiscal_year and f.get("is_current")]
    out: dict[str, str | None] = {"annual": None, "remuneration": None}
    for key, kind in (("annual", "annual-report"), ("remuneration", "remuneration-report")):
        entry = cov.get(kind) or {}
        name = entry.get("file") if entry.get("status") == "found" else None
        if not name and key == "annual":
            name = entry.get("covered_by")
        main = [f for f in files if (f.get("covers") or [None])[0] == kind]
        pdfs = [f for f in main if f.get("format") == "pdf"]
        if name and not name.lower().endswith(".pdf") and pdfs:
            name = pdfs[0]["file_name"]
        if not name and main:
            name = (pdfs or main)[0]["file_name"]
        if name:
            out[key] = gs_uri(record, name, fiscal_year)
    return out


def is_gs(url: str | None) -> bool:
    return bool(url) and url.lower().startswith("gs://")


def local_path(uri: str) -> Path:
    """gs://bucket/a/b c.pdf -> cache/gcs/objects/bucket/a/b c.pdf"""
    rest = unquote(uri[5:])
    return CACHE / "objects" / Path(*rest.split("/"))


def local_uri(uri: str) -> str:
    return local_path(uri).resolve().as_uri()


def fetch(uri: str) -> Path:
    """Download a bucket object once; the cached copy is reused."""
    path = local_path(uri)
    if path.is_file() and path.stat().st_size > 0:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    _run(["cp", uri, str(tmp)])
    tmp.replace(path)
    return path


def ensure(sources: dict[str, str]) -> list[str]:
    """Download a company's bucket files (local file: URI -> gs:// URI). Returns the
    problems; a file that fails is left missing and the report is searched for instead."""
    problems = []
    for gs in sources.values():
        try:
            fetch(gs)
        except GcsError as e:
            problems.append(f"{gs}: {e}")
    return problems


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.gcs",
                                description="Reports already in the CDP bucket")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync", help="Mirror the metadata files (not the reports)")
    s.add_argument("--force", action="store_true")
    f = sub.add_parser("find", help="A company's bucket record and FY reports")
    f.add_argument("name")
    f.add_argument("--country", default="")
    f.add_argument("--isin", default="")
    f.add_argument("--year", default=FISCAL_YEAR)
    args = p.parse_args(argv)
    try:
        sync(force=getattr(args, "force", False))
    except GcsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    recs = records()
    if args.cmd == "sync":
        print(f"{len(recs)} company records in {MIRROR}")
        return 0
    rec, how = Matcher(recs)(name=args.name, country=args.country, isin=args.isin,
                             company_id=args.name)
    if not rec:
        print(how)
        return 2
    print(f"{rec['company_id']} ({rec['name']}), matched by {how}: {rec['_folder']}")
    for k, v in documents(rec, args.year).items():
        print(f"  {k}: {v or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
