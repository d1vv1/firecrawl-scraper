"""The Allshares role list (ref_roles.xlsx) and the title mapper of the role-based pay
extractor (pay_roles.py).

A pay line's title, as the report prints it ("Verkställande direktör", "Former CEO (until
April 2025)", "Mitglied des Aufsichtsrats"), is matched in code against the workbook's
titles, so the role code never depends on the AI. Only a title the workbook does not know is
left to the AI's suggestion (pay_roles.py), and that one goes to the review file.

The workbook (REF_ROLES_XLSX, default ../../Reports/ref_roles.xlsx) has the sheets
  roles            code, label, role_level, role_group, meaning, is_ceo, sort_order, required, active
  role_details     role_detail, label, group, required, when_rule, role_code, cdp_role_id, ...
  titles           role_detail, role_code, title, lang, country, match, status, note
  exclusions       phrase, lang, effect (part_year | flag), note
  disclosure       code, label, meaning, status, list_source
  period_coverage  code, label, meaning, status, list_source
  version          version, date, agreed_by, ...
and is checked when it is loaded: a workbook with a title under two roles, an unknown code
or language, or a blank title is refused (RefRolesError lists every problem).

Matching, for one printed title:
  1. case, accents and punctuation are ignored ("verkstallande DIREKTOR" is the same title);
     an `abbrev` title ("VD", "CEO", "COO") only matches as a whole word in capitals, so
     "Cooperation" is not COO and "Vice VD" is not VD;
  2. of the titles found in it, one inside a longer one loses ("Vice VD" beats "VD",
     "Group Chief Executive Officer" beats "Chief Executive Officer"); of the rest, the one
     that starts first wins ("Vice Chairman of the Board" is the vice chair, not the chair);
  3. text in brackets is only read when the rest matches nothing;
  4. an exclusion word marks the line instead of stopping the match: "Former", "Tidigare",
     "Ehemalige" make it part-year (the role is still matched), "Acting", "Tf." flag it.

    python -m extractor.ref_roles "Tidigare verkställande direktör"
    python -m extractor.ref_roles --check
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .config import PROJECT_ROOT

DEFAULT_XLSX = PROJECT_ROOT.parent.parent / "Reports" / "ref_roles.xlsx"
LANGS = frozenset("en sv da nb fi is de nl it es fr el pt".split())
MATCH_TYPES = frozenset({"phrase", "abbrev"})
STATUSES = {"agreed": "high", "proposed": "medium"}     # title status -> match confidence
EFFECTS = frozenset({"part_year", "flag"})
SHEETS = ("roles", "role_details", "titles", "exclusions", "disclosure", "period_coverage",
          "version")


class RefRolesError(ValueError):
    """The workbook is not usable; the message lists every problem found."""


def norm(text: str) -> str:
    """Lower case, no accents, punctuation as spaces: the form titles are compared in.
    Letters without a decomposition (ø, æ, ß) are kept as they are."""
    text = re.sub(r"<br\s*/?>", " ", text or "", flags=re.I)    # a wrapped table label
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    return re.sub(r"[\W_]+", " ", text).strip()


# the functions that win over any other title in the same printed title, wherever they stand
FUNCTIONS = {"ceo", "former_ceo", "cfo", "deputy_ceo", "executive_chair", "board_chair",
             "board_vice_chair", "statutory_auditor"}
# "Presidente Comitato Nomine", "Chair of the Audit Committee": a committee's chair, not the
# board's (the words right after the title)
COMMITTEE = re.compile(r"^\W*(of the |del |della |de la |do |da |τη[σς] |tou )?(\w+ ){0,2}"
                       r"(comitat|comite|committee|comissao|comision|επιτροπ|udvalg|utskott|"
                       r"utvalg|valiokun|ausschuss)")


def _plain(text: str) -> str:
    """Accents removed, case and punctuation kept: the form abbreviations are found in."""
    text = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in text if not unicodedata.combining(c))


def _word(n: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(n) + r"(?!\w)")


@dataclass(frozen=True)
class Title:
    title: str
    role_detail: str
    role_code: str
    lang: str
    country: str
    match: str              # phrase | abbrev
    status: str             # agreed | proposed
    key: str = field(compare=False, default="")   # norm(title)


@dataclass(frozen=True)
class Exclusion:
    phrase: str
    lang: str
    effect: str             # part_year | flag
    key: str = field(compare=False, default="")


@dataclass
class Match:
    """What a printed title was matched to, and how."""
    printed_title: str
    role_detail: str
    role_code: str
    cdp_role_id: str
    title: str              # the workbook title found in it
    lang: str
    confidence: str         # high (agreed title) | medium (proposed title)
    source: str = "auto"    # the CDP's role_mapping_service values: auto | suggestion | user
    part_year: bool = False
    flags: list[str] = field(default_factory=list)       # e.g. ["acting"]
    exclusions: list[str] = field(default_factory=list)  # the exclusion words found


@dataclass
class RefRoles:
    path: Path
    version: str
    roles: dict[str, dict]
    details: dict[str, dict]
    titles: list[Title]                 # longest first
    exclusions: list[Exclusion]
    disclosure: dict[str, dict]
    period_coverage: dict[str, dict]

    # --- matching ---------------------------------------------------------------------

    def match(self, printed_title: str, country: str | None = None) -> Match | None:
        """The role a printed pay-line title stands for, or None when no workbook title is in
        it. `country` (ISO-2) only matters for titles the workbook ties to one country."""
        if not printed_title or not printed_title.strip():
            return None
        found = set()
        part_year, flags = False, []
        whole = norm(printed_title)
        for e in self.exclusions:
            if e.key and _word(e.key).search(whole):
                found.add(e.phrase)
                if e.effect == "part_year":
                    part_year = True
                else:
                    flags.append(e.phrase.rstrip(".").lower())
        outside = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", printed_title)
        hit = self._best(outside, country) or (self._best(printed_title, country)
                                               if outside != printed_title else None)
        if not hit:
            return None
        detail = self.details[hit.role_detail]
        return Match(printed_title=printed_title, role_detail=hit.role_detail,
                     role_code=hit.role_code, cdp_role_id=detail.get("cdp_role_id") or "",
                     title=hit.title, lang=hit.lang, confidence=STATUSES[hit.status],
                     part_year=part_year, flags=sorted(set(flags)),
                     exclusions=sorted(found))

    def _best(self, text: str, country: str | None) -> Title | None:
        n, plain = norm(text), _plain(text)
        spans: list[tuple[int, int, Title]] = []
        for t in self.titles:
            if t.country and country and t.country.upper() != country.upper():
                continue
            if t.match == "abbrev":
                if not re.search(r"(?<![A-Za-z0-9])" + re.escape(_plain(t.title))
                                 + r"(?![A-Za-z0-9])", plain):
                    continue
            m = _word(t.key).search(n)
            if m:
                spans.append((m.start(), m.end(), t))
        # a title inside a longer one loses; of the rest the first one wins, then the longest
        kept = [s for s in spans
                if not any(o is not s and o[0] <= s[0] and s[1] <= o[1]
                           and (o[1] - o[0]) > (s[1] - s[0]) for o in spans)]
        if not kept:
            return None
        # a function (CEO, chair, CFO, ...) beats a plain membership title wherever it stands:
        # "Executive member, Chairman", "Cons. non esecutivo - Presidente" are the chair
        # (Southern Europe run, 25 Nov 2026)
        functions = [s for s in kept if s[2].role_detail in FUNCTIONS
                     and not COMMITTEE.search(n[s[1]:s[1] + 30])]
        if functions:
            kept = functions
        kept.sort(key=lambda s: (s[0], -(s[1] - s[0])))
        return kept[0][2]

    # --- lists for the prompts -----------------------------------------------------------

    def required(self) -> list[str]:
        return [d for d, row in self.details.items() if row.get("required") == "Y"]

    def optional(self) -> list[str]:
        return [d for d, row in self.details.items() if row.get("required") != "Y"]

    def select(self, spec: str) -> list[str]:
        """role_details for --roles: 'required', 'optional', 'all', or a comma list of
        role_details and role codes (a code stands for all its role_details)."""
        spec = (spec or "").strip()
        if spec in ("required", "optional"):
            return getattr(self, spec)()
        if spec in ("all", ""):
            return list(self.details)
        out: list[str] = []
        for item in (s.strip() for s in spec.split(",") if s.strip()):
            if item in self.details:
                picked = [item]
            elif item in self.roles:
                picked = [d for d, row in self.details.items() if row["role_code"] == item]
            else:
                raise RefRolesError(f"--roles: {item!r} is neither a role_detail nor a role code")
            out += [d for d in picked if d not in out]
        return out

    def titles_for(self, role_details: list[str], langs: set[str] | None = None) -> dict[str, list[str]]:
        """The workbook titles of these role_details, in these languages (all if None)."""
        out: dict[str, list[str]] = {d: [] for d in role_details}
        for t in sorted(self.titles, key=lambda t: t.title.casefold()):
            if t.role_detail in out and (langs is None or t.lang in langs):
                out[t.role_detail].append(t.title)
        return out


# --- loading --------------------------------------------------------------------------

def _rows(wb, name: str, problems: list[str]) -> list[dict]:
    if name not in wb.sheetnames:
        problems.append(f"sheet {name!r} is missing")
        return []
    rows = list(wb[name].iter_rows(values_only=True))
    if not rows:
        return []
    head = [str(h).strip() if h is not None else "" for h in rows[0]]
    out = []
    for r in rows[1:]:
        if r is None or all(v is None or str(v).strip() == "" for v in r):
            continue
        out.append({h: ("" if v is None else str(v).strip()) for h, v in zip(head, r) if h})
    return out


def load(path: str | Path | None = None) -> RefRoles:
    """The workbook at `path` (default: REF_ROLES_XLSX, else ../../Reports/ref_roles.xlsx),
    checked. Raises RefRolesError with every problem found."""
    import openpyxl

    path = Path(path or os.getenv("REF_ROLES_XLSX") or DEFAULT_XLSX)
    if not path.is_file():
        raise RefRolesError(f"no role workbook at {path} (set REF_ROLES_XLSX)")
    body = path.read_bytes()
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    problems: list[str] = []
    try:
        sheets = {name: _rows(wb, name, problems) for name in SHEETS}
    finally:
        wb.close()

    roles: dict[str, dict] = {}
    for r in sheets["roles"]:
        code = r.get("code", "")
        if not code:
            problems.append("roles: a row has no code")
        elif code in roles:
            problems.append(f"roles: {code} is listed twice")
        else:
            roles[code] = r

    details: dict[str, dict] = {}
    for r in sheets["role_details"]:
        d = r.get("role_detail", "")
        if not d:
            problems.append("role_details: a row has no role_detail")
            continue
        if d in details:
            problems.append(f"role_details: {d} is listed twice")
        if r.get("role_code") not in roles:
            problems.append(f"role_details: {d} has unknown role_code {r.get('role_code')!r}")
        if r.get("required", "") not in ("Y", "N"):
            problems.append(f"role_details: {d} required must be Y or N, not {r.get('required')!r}")
        details[d] = r

    titles: list[Title] = []
    seen: dict[str, Title] = {}
    for i, r in enumerate(sheets["titles"], start=2):
        where = f"titles row {i}"
        text, d = r.get("title", ""), r.get("role_detail", "")
        if not text:
            problems.append(f"{where}: blank title")
            continue
        where = f"titles row {i} ({text!r})"
        if d not in details:
            problems.append(f"{where}: unknown role_detail {d!r}")
            continue
        code = details[d]["role_code"]
        if r.get("role_code") and r["role_code"] != code:
            problems.append(f"{where}: role_code {r['role_code']} but {d} belongs to {code}")
        lang, match, status = r.get("lang", ""), r.get("match") or "phrase", r.get("status", "")
        if lang not in LANGS:
            problems.append(f"{where}: lang {lang!r} is not one of {' '.join(sorted(LANGS))}")
        if match not in MATCH_TYPES:
            problems.append(f"{where}: match {match!r} is not phrase or abbrev")
        if status not in STATUSES:
            problems.append(f"{where}: status {status!r} is not agreed or proposed")
        key = norm(text)
        if not key:
            problems.append(f"{where}: nothing left of the title after normalising")
            continue
        t = Title(text, d, code, lang, r.get("country", "").upper(), match, status, key)
        other = seen.get((key, t.country))
        if other:
            problems.append(f"{where}: same title as {other.title!r} "
                            + (f"under {other.role_detail}" if other.role_detail != d
                               else "(listed twice)"))
            continue
        seen[(key, t.country)] = t
        titles.append(t)
    titles.sort(key=lambda t: (-len(t.key), t.key))

    exclusions: list[Exclusion] = []
    for i, r in enumerate(sheets["exclusions"], start=2):
        phrase, effect = r.get("phrase", ""), r.get("effect", "")
        if not phrase or not norm(phrase):
            problems.append(f"exclusions row {i}: blank phrase")
            continue
        if effect not in EFFECTS:
            problems.append(f"exclusions row {i} ({phrase!r}): effect {effect!r} is not "
                            "part_year or flag")
        if r.get("lang", "") not in LANGS:
            problems.append(f"exclusions row {i} ({phrase!r}): lang {r.get('lang')!r} unknown")
        exclusions.append(Exclusion(phrase, r.get("lang", ""), effect, norm(phrase)))

    disclosure = {r["code"]: r for r in sheets["disclosure"] if r.get("code")}
    coverage = {r["code"]: r for r in sheets["period_coverage"] if r.get("code")}
    if sheets["version"] is not None and not sheets["version"]:
        problems.append("version: the sheet has no row")

    if problems:
        raise RefRolesError(f"{path.name}: {len(problems)} problem(s)\n  " + "\n  ".join(problems))
    label = (sheets["version"][0].get("version") or "unversioned").split("+")[0]
    version = f"{label}+{hashlib.sha1(body).hexdigest()[:8]}"
    return RefRoles(path, version, roles, details, titles, exclusions, disclosure, coverage)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.ref_roles",
                                description="Check the role workbook, or map printed titles.")
    p.add_argument("titles", nargs="*", help="printed pay-line titles to map")
    p.add_argument("--xlsx", help="the workbook (default: REF_ROLES_XLSX)")
    p.add_argument("--country", help="ISO-2 country of the report")
    p.add_argument("--check", action="store_true", help="load, check and summarise only")
    args = p.parse_args(argv)
    try:
        ref = load(args.xlsx)
    except RefRolesError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if args.check or not args.titles:
        print(f"{ref.path}: version {ref.version}: {len(ref.roles)} roles, "
              f"{len(ref.details)} role_details ({len(ref.required())} required), "
              f"{len(ref.titles)} titles, {len(ref.exclusions)} exclusions")
    for text in args.titles:
        m = ref.match(text, args.country)
        if not m:
            print(f"{text!r}: no match")
            continue
        extra = ", ".join(x for x in ("part-year" if m.part_year else "",
                                      *(f"flag:{f}" for f in m.flags)) if x)
        print(f"{text!r}: {m.role_detail} ({m.role_code}"
              + (f", {m.cdp_role_id}" if m.cdp_role_id else "") + f") via {m.title!r} "
              f"[{m.lang}, {m.confidence}]" + (f" {extra}" if extra else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
