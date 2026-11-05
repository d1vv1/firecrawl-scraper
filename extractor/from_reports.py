"""Companies from a list of their reports (python -m extractor.from_reports).

Given annual reports or remuneration reports on disk (PDF, or the HTML/XHTML of an
ESEF filing), each file is identified, then collected like any other company:

1. The file is read with the collector's own converters (a scanned PDF from page images).
2. Unique identifiers first: LEIs and ISINs (with their check digits) and register
   numbers by their labels ("Company number", "Org. nr", "CVR", "Business ID"), each
   confirmed in GLEIF.
3. Then the company: a report names others too (subsidiaries, bond issuers, the
   auditor), so the confirmed company mentioned most, and earliest, wins, with a bonus
   when its name is on the first pages. Without any identifier, one AI call reads the
   first pages for the legal name and country, matched in GLEIF by name.
4. Then the rest: each file is an annual or a remuneration report (its title); files of
   one company are grouped. The result is a company list for the collector, with the
   files as the reports it reads (no report search). With --collect it runs at once.

    python -m extractor.from_reports reports/                (every PDF/XHTML/HTML in it)
    python -m extractor.from_reports a.pdf b.xhtml --collect

Writes output/<name>_companies.csv (and, with --collect, <name>_datapoints.csv).
"""

import argparse
import csv
import hashlib
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from . import lei as gleif
from . import llm, ocr
from .config import CACHE_DIR, OUTPUT_DIR, fold, slugify
from .output_checks import isin_ok, lei_ok
from .schemas import ReportIdentity
from .scraper import (NeedsOCRError, Page, check_not_scanned, markdown_to_pages,
                      pages_to_markdown, pdf_to_pages)
from .xhtml_text import html_to_text, text_to_pages

log = logging.getLogger(__name__)

SUFFIXES = {".pdf", ".xhtml", ".html", ".htm"}
FIRST_PAGES = 3                  # the cover and title pages: a name there counts most
EARLY_BONUS = 5                  # an identifier on the first pages counts this much more
NAME_BONUS = 10                  # the GLEIF name printed on the first pages
MAX_LOOKUPS = 10                 # GLEIF lookups per file, best candidates first
IDENTITY_WORDS = 2500            # words of the first pages for the AI fallback
COVER_CHARS = 600                # the start of page 1: where a report's title is

_LEI = re.compile(r"\b[A-Z0-9]{18}\d{2}\b")
_ISIN = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b")
# National register numbers by the label printed before them; the value as GLEIF stores
# it (entity.registeredAs): spaces dropped, Swedish and Finnish dashes kept.
REGISTERS = {
    "GB": r"(?:company|registered|registration)\s+(?:number|no\.?)\s*:?\s*([A-Z]{2}\d{6}|\d{7,8})\b",
    "SE": r"(?:org(?:anisations)?\.?\s*(?:nr|nummer)|corp(?:orate)?\.?\s*id(?:entity)?\.?\s*(?:number|no\.?)|"
          r"reg(?:istration)?\.?\s*no\.?)\s*:?\s*(\d{6}-\d{4})\b",
    "NO": r"(?:org(?:anisasjons)?\.?\s*(?:nr|nummer)|organi[sz]ation(?:al)? (?:number|no\.?)|"
          r"business register(?:ed)? (?:number|no\.?))\s*:?\s*(\d{3}\s?\d{3}\s?\d{3})\b",
    "DK": r"(?:cvr|company reg(?:istration)?\.?)\s*(?:-?nr\.?|no\.?|number)?\s*:?\s*"
          r"(\d{2}\s?\d{2}\s?\d{2}\s?\d{2})\b",
    "FI": r"(?:business id|y-tunnus|business identity code)\s*:?\s*(\d{7}-\d)\b",
}
ANNUAL = re.compile(
    r"annual report|annual and sustainability report|report and accounts|annual financial report|"
    r"form 10-k|form 20-f|årsredovisning|års- och hållbarhetsredovisning|årsrapport|årsberetning|"
    r"vuosikertomus|tilinpäätös|geschäftsbericht|jahresbericht|rapport annuel|"
    r"document d.enregistrement universel|relazione finanziaria annuale|informe anual", re.I)
REMUNERATION = re.compile(
    r"remuneration report|compensation report|remuneration policy|directors.? remuneration|"
    r"ersättningsrapport|lønrapport|godtgørelsesrapport|vederlagsrapport|palkitsemisraportti|"
    r"palkitsemispolitiikka|vergütungsbericht|rapport de rémunération|rapporto sulla remunerazione",
    re.I)


@dataclass
class Candidate:
    kind: str                        # LEI, ISIN, or a register ("GB register")
    value: str
    country: str | None = None
    count: int = 0
    first_page: int = 10 ** 6

    @property
    def score(self) -> int:
        return self.count + (EARLY_BONUS if self.first_page <= FIRST_PAGES else 0)


@dataclass
class Identified:
    path: Path
    document_type: str               # annual_report / remuneration_report
    record: gleif.LeiRecord | None = None
    name: str | None = None
    country: str | None = None
    how: str = ""
    isin: str | None = None
    evidence: list[str] = field(default_factory=list)


# --- reading -------------------------------------------------------------------------------

def read_pages(path: Path) -> list[Page]:
    """The file's text, page by page, cached by its contents."""
    body = path.read_bytes()
    md = CACHE_DIR / f"file_{hashlib.sha1(body).hexdigest()[:16]}.md"
    if md.exists():
        return markdown_to_pages(md.read_text(encoding="utf-8"))
    if body[:1024].lstrip().startswith(b"%PDF"):
        pages = pdf_to_pages(path)
        try:
            check_not_scanned(pages)
        except NeedsOCRError:
            pages = ocr.pdf_pages(path)
            check_not_scanned(pages)
    else:
        pages = text_to_pages(html_to_text(body.decode("utf-8", errors="replace")))
        check_not_scanned(pages)
    CACHE_DIR.mkdir(exist_ok=True)
    md.write_text(pages_to_markdown(pages), encoding="utf-8")
    return pages


# --- identifiers ---------------------------------------------------------------------------

def candidates(pages: list[Page]) -> list[Candidate]:
    """Every LEI, ISIN and labelled register number with valid form, counted, best first."""
    found: dict[tuple[str, str], Candidate] = {}

    def add(kind, value, page, country=None):
        c = found.setdefault((kind, value), Candidate(kind, value, country))
        c.count += 1
        c.first_page = min(c.first_page, page)

    for p in pages:
        for v in _LEI.findall(p.text):
            if lei_ok(v):
                add("LEI", v, p.number)
        for v in _ISIN.findall(p.text):
            if isin_ok(v):
                add("ISIN", v, p.number)
        for cc, pattern in REGISTERS.items():
            for v in re.findall(pattern, p.text, re.I):
                v = re.sub(r"\s", "", v)          # a UK number may drop its leading 0
                add(f"{cc} register", v.zfill(8) if cc == "GB" and v.isdigit() else v, p.number, cc)
    return sorted(found.values(), key=lambda c: (-c.score, c.first_page))


def resolve(c: Candidate) -> gleif.LeiRecord | None:
    """The GLEIF record an identifier belongs to (one record only)."""
    if c.kind == "LEI":
        return gleif.fetch_by_lei(c.value)
    if c.kind == "ISIN":
        return gleif.find_lei_by_id(isin=c.value)[0]
    return gleif.find_lei_by_id(registered_as=c.value, country=c.country)[0]


def _name_on(record: gleif.LeiRecord, text: str) -> bool:
    """The legal name (without its legal form) printed in the text."""
    words = " ".join(gleif.name_key(record.legal_name).base)
    return bool(words) and words in " ".join(gleif.name_key(text).base)


def by_identifiers(pages: list[Page]) -> tuple[gleif.LeiRecord | None, list[str], str | None]:
    """The reporting company from its identifiers: (record, evidence, its ISIN)."""
    cands = candidates(pages)
    first = "\n".join(p.text for p in pages[:FIRST_PAGES])
    scores: dict[str, int] = defaultdict(int)
    records: dict[str, gleif.LeiRecord] = {}
    evidence: dict[str, list[str]] = defaultdict(list)
    isins: dict[str, str] = {}
    for c in cands[:MAX_LOOKUPS]:
        try:
            rec = resolve(c)
        except httpx.HTTPError as e:
            log.warning("GLEIF lookup of %s %s failed: %s", c.kind, c.value, str(e)[:100])
            continue
        if rec is None:
            continue
        records[rec.lei] = rec
        scores[rec.lei] += c.score
        evidence[rec.lei].append(f"{c.kind} {c.value} ({c.count}x, first on page {c.first_page})")
        if c.kind == "ISIN":
            isins.setdefault(rec.lei, c.value)
    for lei_code, rec in records.items():
        if _name_on(rec, first):
            scores[lei_code] += NAME_BONUS
            evidence[lei_code].append("name on the first pages")
    if not scores:
        return None, [], None
    best = max(scores, key=lambda k: scores[k])
    return records[best], evidence[best], isins.get(best)


# --- the AI fallback -----------------------------------------------------------------------

def by_cover(pages: list[Page]) -> ReportIdentity:
    """One AI call on the first pages: whose report, which country, which kind. Cached
    by the text and the prompt, so the same files cost nothing again."""
    text = " ".join(" ".join(p.text for p in pages[:6]).split()[:IDENTITY_WORDS])
    prompt = llm.load_prompt("report_identity_system")
    path = CACHE_DIR / f"identity_{hashlib.sha1((prompt + text).encode()).hexdigest()[:16]}.json"
    if path.exists():
        return ReportIdentity.model_validate_json(path.read_text(encoding="utf-8"))
    got = llm.call_llm(prompt, text, ReportIdentity)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(got.model_dump_json(), encoding="utf-8")
    return got


def document_type(path: Path, pages: list[Page]) -> str | None:
    """From the title: the file name and the start of the cover page. Not the pages
    after it: an annual report's contents list its remuneration report. None when the
    title says neither, and the cover read decides."""
    title = path.stem.replace("_", " ").replace("-", " ") + "\n" + (pages[0].text[:COVER_CHARS]
                                                                     if pages else "")
    rem, annual = REMUNERATION.search(title), ANNUAL.search(title)
    if rem and annual:
        return None            # both named (a contents page): the cover read decides
    return "remuneration_report" if rem else "annual_report" if annual else None


def identify(path: Path) -> Identified:
    pages = read_pages(path)
    kind = document_type(path, pages)
    out = Identified(path, kind or "other")
    record, evidence, isin = by_identifiers(pages)
    cover = by_cover(pages) if record is None or kind is None else None
    if cover and kind is None:
        out.document_type = cover.document_type
    if record:
        out.record, out.evidence, out.isin = record, evidence, isin
        out.how = "identifiers"
    else:
        out.name, out.country = cover.legal_name, cover.country
        if cover.legal_name:
            res = gleif.find_lei(cover.legal_name, cover.country)
            out.record = res.record
            out.how = f"name on the cover, {res.reason}"
            out.evidence = [f'cover: "{cover.quote}"'] if cover.quote else []
        else:
            out.how = "not identified: no identifier, no name on the first pages"
    if out.record:
        out.name, out.country = out.record.legal_name, out.record.country
    return out


# --- the company list ----------------------------------------------------------------------

COLUMNS = ["company_id", "company_name", "country", "lei", "isin", "annual_report_url",
           "remuneration_report_url", "identified_by"]


def company_rows(found: list[Identified]) -> list[dict]:
    """One row per company, its files as the reports to read."""
    rows: dict[str, dict] = {}
    for f in found:
        if not f.name or f.document_type == "other":
            continue
        key = f.record.lei if f.record else fold(f.name)
        row = rows.setdefault(key, {"company_id": slugify(f.name), "company_name": f.name,
                                    "country": f.country or "",
                                    "lei": f.record.lei if f.record else "",
                                    "isin": f.isin or "", "annual_report_url": "",
                                    "remuneration_report_url": "", "identified_by": ""})
        col = "remuneration_report_url" if f.document_type == "remuneration_report" else "annual_report_url"
        if row[col]:
            log.warning("%s: a second %s (%s) is left out; keeping %s", f.name,
                        col.replace("_url", "").replace("_", " "), f.path.name, row[col])
        else:
            row[col] = f.path.resolve().as_uri()
        row["isin"] = row["isin"] or f.isin or ""
        row["identified_by"] = "; ".join(x for x in (row["identified_by"],
                                                     f"{f.path.name}: {f.how}") if x)
    return list(rows.values())


def files_in(args: list[str]) -> list[Path]:
    out = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out += sorted(x for x in p.iterdir() if x.suffix.lower() in SUFFIXES)
        elif p.is_file():
            out.append(p)
        else:
            log.warning("No such file or folder: %s", a)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.from_reports",
                                description="Identify the companies of report files and collect them.")
    p.add_argument("files", nargs="+", help="report files (PDF, XHTML, HTML) or folders of them")
    p.add_argument("--name", default="from_reports", help="output name (default: from_reports)")
    p.add_argument("--collect", action="store_true",
                   help="run the collector on the companies found (python -m extractor.datapoints)")
    args, rest = p.parse_known_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    files = files_in(args.files)
    if not files:
        print("ERROR: no report files given", file=sys.stderr)
        return 1
    found = []
    for f in files:
        try:
            got = identify(f)
        except (NeedsOCRError, OSError) as e:
            print(f"{f.name}: not readable ({e})")
            continue
        found.append(got)
        kind = {"annual_report": "annual report", "remuneration_report": "remuneration report"}.get(
            got.document_type, "not an annual or remuneration report (left out)")
        print(f"{f.name}: {kind} of {got.name or '?'}"
              + (f" ({got.record.lei}, {got.country})" if got.record else "")
              + f": {got.how}" + (f" [{'; '.join(got.evidence[:3])}]" if got.evidence else ""))
    rows = company_rows(found)
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / f"{args.name}_companies.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows)} compan{'y' if len(rows) == 1 else 'ies'} from {len(files)} file(s): {out}")
    if args.collect and rows:
        from . import datapoints
        # --redo: these files are the reports to read, also for a company collected before
        return datapoints.main([str(out), "--out", str(OUTPUT_DIR / f"{args.name}_datapoints.csv"), "--redo"]
                               + rest)
    return 0 if rows else 2


if __name__ == "__main__":
    raise SystemExit(main())
