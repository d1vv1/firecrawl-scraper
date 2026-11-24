"""The run-level files of the role-based pay extractor (pay_roles.py), and the checks that
decide which cells a gap-fill run asks about again.

From the companies/<id>.json files of one run:
  fact_pay_line.csv   one row per pay line, in the BigQuery fact_pay_line columns plus the
                      role and provenance columns; values verbatim (as printed, not scaled)
  evidence.csv        one row per filled cell: value, figure, unit and currency as printed,
                      page, chunk and the exact quote, and whether the quote was found
  role_review.csv     what a person should look at: role suggestions and unmapped titles,
                      missing required roles, totals that do not add up, unit and currency
                      warnings, quotes not found in the text
Nothing here changes a value: a check only adds a review row (and, for some, a gap).
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .pay_roles_schema import FIELDS
from .schemas import UNIT_MULTIPLIERS

FACT_COLUMNS = [
    "pay_line_id", "company_id", "fiscal_year", "role_title", "role_code", "role_disclosure",
    "is_aggregated", "aggregate_headcount", "aggregate_excludes", "months_in_role",
    "period_coverage", "pay_currency", "units", "base_salary", "token_salary", "benefits_value",
    "pension_contribution", "sti_paid", "sti_target_value", "sti_target_basis", "sti_max_value",
    "sti_max_basis", "lti_vested", "lti_granted", "lti_basis", "lti_units", "lti_face_value",
    "lti_fair_value", "lti_target_value", "lti_target_basis", "lti_max_value", "lti_max_basis",
    "performance_period_start", "performance_period_end", "total_remuneration"]
EXTRA_COLUMNS = ["role_detail", "cdp_role_id", "mapping_source", "mapping_confidence",
                 "person_name", "company_name", "country", "period_end", "fiscal_year_printed",
                 "source_file", "match_type", "ref_roles_version", "run_id", "review_flags"]
EVIDENCE_COLUMNS = ["pay_line_id", "company_id", "role_title", "role_detail", "field", "value",
                    "printed", "unit_printed", "unit", "currency_printed", "form", "includes",
                    "page", "chunk_id", "quote", "quote_found", "goes_to", "previous_value",
                    "note", "source_file"]
REVIEW_COLUMNS = ["company_id", "company_name", "pay_line_id", "role_title", "kind", "field",
                  "detail", "gap"]

MONEY = [n for n, f in FIELDS.items() if f.cell.__name__ in ("PayCell", "LtiCell")]
TOTAL_PARTS = ["base_salary", "committee_fees", "meeting_fees", "benefits", "pension",
               "pension_allowance", "sti_paid", "sti_deferred", "other_pay"]
TOTAL_TOLERANCE = 0.005          # 0.5% of the total, or 1 printed unit, for rounding
TOKEN_SALARY_MAX = float(os.getenv("PAY_ROLES_TOKEN_SALARY_MAX", "1000"))   # in currency units

# The completeness rules of the Allshares role list ("When" column), per company: one of
# each group must be there. Supervisory board members count as board members.
COMPLETENESS = [
    ("CEO", {"ceo", "former_ceo"}),
    ("board chair", {"board_chair", "executive_chair"}),
    ("CFO or the executive group line", {"cfo", "executive_management_group"}),
    ("board members or the board group line",
     {"non_executive_director", "supervisory_board_member", "board_group",
      "employee_representative", "senior_independent_director", "audit_committee_chair",
      "remuneration_committee_chair", "nomination_committee_chair", "committee_chair_member",
      "board_vice_chair", "former_board_member"}),
]


@dataclass
class Finding:
    company_id: str
    company_name: str
    pay_line_id: str
    role_title: str
    kind: str
    field: str
    detail: str
    gap: bool                    # a gap-fill run asks about this cell again

    def row(self) -> dict:
        return {k: getattr(self, k) for k in REVIEW_COLUMNS}


# --- helpers ---------------------------------------------------------------------------------

def words(text: str | None) -> str:
    """Letters and digits only, lower case: how a quote is looked for in the text."""
    return re.sub(r"[\W_]+", "", (text or "").casefold())


CLOSE_COVERAGE = 0.8             # a "close" quote: this share of its words is in the chunk


def quote_found(quote: str | None, chunk_id: int | None, chunks: dict[int, str]) -> bool | None:
    """Whether the quote is in its chunk (or, failing that, any chunk). None: no quote."""
    if not quote:
        return None
    q = words(quote)
    if not q:
        return None
    if chunk_id in chunks and q in words(chunks[chunk_id]):
        return True
    return any(q in words(t) for t in chunks.values())


def quote_grade(quote: str | None, printed: str | None, chunk_id: int | None,
                chunks: dict[int, str]) -> str | None:
    """How well a cell's quote matches the text it was read from:
      exact    the quote is in the text as it stands (letters and digits);
      close    not as it stands, but the printed figure is in the quote's chunk and most of
               the quote's words are too: the AI tidied a damaged row (joined a wrapped label,
               skipped empty cells), which the prompt asks it to do;
      missing  neither: the figure may not come from the text.
    None when there is no quote (a line's own quote with no figure is graded on words)."""
    if not quote or not words(quote):
        return None
    if quote_found(quote, chunk_id, chunks):
        return "exact"
    home = [chunks[chunk_id]] if chunk_id in chunks else list(chunks.values())
    for text in home:
        body = words(text)
        figure = words(printed)
        if figure and figure not in body:
            continue
        tokens = [words(t) for t in re.split(r"[\s|]+", quote) if words(t)]
        if tokens and sum(t in body for t in tokens) / len(tokens) >= CLOSE_COVERAGE:
            return "close"
    return "missing"


def comparison_year(quote: str | None, fiscal_year: int | None) -> bool:
    """The quote shows the year before the pay year and not the pay year itself: the figure
    is likely the comparison year's (a table with one row per person and year)."""
    if not quote or not fiscal_year:
        return False
    years = set(re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", quote))
    return str(fiscal_year - 1) in years and str(fiscal_year) not in years


def filled(cell) -> bool:
    return isinstance(cell, dict) and cell.get("value") is not None


def fiscal_year_int(fy: str | None, period_end: str | None) -> int | None:
    if period_end and re.match(r"\d{4}-\d{2}-\d{2}$", period_end):
        return int(period_end[:4])
    short = re.match(r"((?:19|20)\d{2})\s*/\s*(\d{2})$", (fy or "").strip())   # 2024/25
    if short:
        return int(short.group(1)[:2] + short.group(2))
    years = re.findall(r"(?:19|20)\d{2}", fy or "")
    return int(years[-1]) if years else None


def _most(values: list[str]) -> str:
    values = [v for v in values if v]
    return Counter(values).most_common(1)[0][0] if values else ""


def _num(v) -> str:
    if v is None:
        return ""
    return str(int(v)) if float(v).is_integer() else repr(float(v))


# --- checks ----------------------------------------------------------------------------------

def check_company(doc: dict) -> list[Finding]:
    """Everything a person should look at in one company's result."""
    cid, cname = doc.get("company_id", ""), doc.get("company_name", "")
    out: list[Finding] = []

    def add(item, kind, detail, field="", gap=False):
        line = item["line"] if item else {}
        out.append(Finding(cid, cname, item["pay_line_id"] if item else "",
                           line.get("printed_title", ""), kind, field, detail, gap))

    lines = doc.get("lines", [])
    seen: dict[tuple, str] = {}
    for item in lines:
        line, m = item["line"], item["mapping"]
        title = line.get("printed_title", "")
        # roles
        if m["mapping_source"] == "suggestion":
            add(item, "role_suggestion", f"AI: {m.get('role_detail') or m.get('cdp_role_id')} "
                f"({m['mapping_confidence']}); reason: {line.get('suggestion_reason') or '-'}")
        elif m["mapping_source"] == "unmapped":
            add(item, "role_unmapped", m.get("note") or "no workbook title and no usable suggestion")
        elif m.get("note"):
            add(item, "role_disagree", f"title says {m['role_detail']}; {m['note']}")
        if m.get("title_part_year") and line.get("period_coverage") in ("full_year", "not_stated"):
            add(item, "period_check", f"the title marks a former holder but period_coverage is "
                f"{line.get('period_coverage')}")
        key = (title.casefold().strip(), (line.get("person_name") or "").casefold().strip())
        if key in seen:
            add(item, "duplicate_line", f"same title and name as {seen[key]}")
        seen[key] = item["pay_line_id"]
        # quotes (True/False: runs before quotes were graded)
        fy = fiscal_year_int(doc.get("fiscal_year"), doc.get("period_end"))
        for f in FIELDS:
            cell = line.get(f)
            if not filled(cell):
                continue
            if item.get("quote_check", {}).get(f) in (False, "missing"):
                add(item, "quote_not_found", f"quote not in the text: {cell.get('quote')!r}", f, True)
            if comparison_year(cell.get("quote"), fy):
                add(item, "comparison_year", f"the quote shows {fy - 1}, not {fy}: "
                    f"{cell.get('quote')!r}", f, True)
        # units and currencies
        money = [(f, line[f]) for f in MONEY if filled(line.get(f))]
        currencies = {c.get("currency_printed") for _, c in money if c.get("currency_printed")}
        units = {c.get("unit_printed") for _, c in money if c.get("unit_printed")}
        if len(currencies) > 1 or len(units) > 1:
            add(item, "currency_mix", f"currencies {sorted(currencies)}, units {sorted(units)}",
                "", False)
        for f, c in money:
            if c.get("unit") in ("thousands", "millions") and abs(c["value"]) >= 1_000_000:
                add(item, "unit_scale", f"{c.get('printed')} {c.get('unit_printed')}: looks like a "
                    "full amount in a thousands/millions table", f, True)
            if (f == "base_salary" and c.get("unit") == "units" and 0 < abs(c["value"]) < 1000
                    and not line.get("is_aggregate") and m.get("role_code") in
                    ("ceo", "cfo", "deputy_ceo", "coo", "other_executive")):
                add(item, "unit_scale", f"{c.get('printed')} {c.get('unit_printed')}: an executive "
                    "salary under 1,000 currency units; is the table in thousands?", f, True)
        # totals
        total = line.get("total")
        parts = [f for f in TOTAL_PARTS if filled(line.get(f))]
        if filled(total) and parts:
            base = sum(line[f]["value"] for f in parts)
            sums = {"without LTI": base}
            if filled(line.get("lti_vested")):
                sums["with LTI vested"] = base + line["lti_vested"]["value"]
            if filled(line.get("lti_granted")):
                sums["with LTI granted"] = base + line["lti_granted"]["value"]
            tol = max(1.0, abs(total["value"]) * TOTAL_TOLERANCE)
            if not any(abs(s - total["value"]) <= tol for s in sums.values()):
                add(item, "total_mismatch", f"total {total.get('printed')} vs parts "
                    + ", ".join(f"{k} {_num(v)}" for k, v in sums.items()), "total", True)
        # an individual executive with no fixed pay at all
        if (m.get("role_code") in ("ceo", "cfo", "deputy_ceo", "coo", "other_executive")
                and line.get("role_disclosure") in ("individual", "individual_unnamed")
                and not filled(line.get("base_salary")) and not filled(total)
                and "base_salary" in doc.get("fields", FIELDS)):
            add(item, "empty_core", "no base salary and no total", "base_salary", True)

    found = {x["mapping"].get("role_detail") for x in lines}
    if doc.get("status") == "ok" and doc.get("run_mode") in ("role", "all"):
        asked = set(doc.get("roles") or []) or None
        for label, any_of in COMPLETENESS:
            if asked is not None and not (any_of & asked):
                continue                    # this request did not ask for these roles
            if not (any_of & found):
                add(None, "completeness", f"no {label} line")
    return out


# --- rows ------------------------------------------------------------------------------------

def fact_row(doc: dict, item: dict, run_id: str, flags: list[str]) -> dict:
    line, m = item["line"], item["mapping"]
    money = [line[f] for f in MONEY if filled(line.get(f))]
    row = {c: "" for c in FACT_COLUMNS + EXTRA_COLUMNS}
    row.update({
        "pay_line_id": item["pay_line_id"], "company_id": doc["company_id"],
        "fiscal_year": fiscal_year_int(doc.get("fiscal_year"), doc.get("period_end")) or "",
        "role_title": line.get("printed_title", ""), "role_code": m.get("role_code", ""),
        "role_disclosure": line.get("role_disclosure", ""),
        "is_aggregated": bool(line.get("is_aggregate")),
        "aggregate_headcount": _num(line.get("aggregate_headcount")),
        "aggregate_excludes": line.get("aggregate_excludes") or "",
        "months_in_role": _num(line.get("months_in_role")),
        "period_coverage": line.get("period_coverage", ""),
        "pay_currency": _most([c.get("currency_printed") for c in money]),
        "units": _most([c.get("unit_printed") for c in money]),
        "role_detail": m.get("role_detail", ""), "cdp_role_id": m.get("cdp_role_id", ""),
        "mapping_source": m.get("mapping_source", ""),
        "mapping_confidence": m.get("mapping_confidence", ""),
        "person_name": line.get("person_name") or "", "company_name": doc.get("company_name", ""),
        "country": doc.get("country", ""), "period_end": doc.get("period_end", ""),
        "fiscal_year_printed": doc.get("fiscal_year", ""),
        "source_file": doc.get("source_file", ""), "match_type": doc.get("match_type", ""),
        "ref_roles_version": doc.get("ref_roles_version", ""), "run_id": run_id,
        "review_flags": ";".join(sorted(set(flags))),
    })
    for name, f in FIELDS.items():
        cell = line.get(name)
        if not filled(cell) or not f.columns:
            continue
        row[f.columns[0]] = _num(cell["value"])
        if len(f.columns) == 2:
            row[f.columns[1]] = cell.get("form") or ""
    base = line.get("base_salary")
    if filled(base) and m.get("role_code") in ("ceo", "cfo", "deputy_ceo", "coo",
                                               "other_executive", "executive_chair"):
        scale = UNIT_MULTIPLIERS.get(base.get("unit") or "")
        if scale:
            row["token_salary"] = abs(base["value"]) * scale <= TOKEN_SALARY_MAX
    return row


def evidence_rows(doc: dict, item: dict) -> list[dict]:
    line, m = item["line"], item["mapping"]
    pages = doc.get("chunk_pages", {})
    out = []
    for name, f in FIELDS.items():
        cell = line.get(name)
        if not filled(cell):
            continue
        cid = cell.get("chunk_id")
        out.append({
            "pay_line_id": item["pay_line_id"], "company_id": doc["company_id"],
            "role_title": line.get("printed_title", ""), "role_detail": m.get("role_detail", ""),
            "field": name, "value": _num(cell["value"]), "printed": cell.get("printed") or "",
            "unit_printed": cell.get("unit_printed") or "", "unit": cell.get("unit") or "",
            "currency_printed": cell.get("currency_printed") or "", "form": cell.get("form") or "",
            "includes": cell.get("includes") or "",
            "page": ",".join(map(str, pages.get(str(cid), []))) if cid is not None else "",
            "chunk_id": "" if cid is None else cid, "quote": cell.get("quote") or "",
            "quote_found": item.get("quote_check", {}).get(name, ""),
            "goes_to": "+".join(f.columns) or "evidence only",
            "previous_value": _num((cell.get("previous") or {}).get("value")),
            "note": cell.get("gapfill_note") or "", "source_file": doc.get("source_file", ""),
        })
    return out


def load_companies(run_dir: Path) -> list[dict]:
    docs = []
    for p in sorted((run_dir / "companies").glob("*.json")):
        if not p.name.endswith(".error.json"):
            docs.append(json.loads(p.read_text(encoding="utf-8")))
    return docs


def export(run_dir: Path) -> dict[str, int]:
    """Write fact_pay_line.csv, evidence.csv and role_review.csv for one run."""
    run_id = run_dir.name
    facts, evidence, review = [], [], []
    for doc in load_companies(run_dir):
        findings = check_company(doc)
        review += [f.row() for f in findings]
        by_line: dict[str, list[str]] = {}
        for f in findings:
            by_line.setdefault(f.pay_line_id, []).append(f.kind)
        for item in doc.get("lines", []):
            facts.append(fact_row(doc, item, run_id, by_line.get(item["pay_line_id"], [])))
            evidence += evidence_rows(doc, item)
    for name, cols, rows in (("fact_pay_line.csv", FACT_COLUMNS + EXTRA_COLUMNS, facts),
                             ("evidence.csv", EVIDENCE_COLUMNS, evidence),
                             ("role_review.csv", REVIEW_COLUMNS, review)):
        with (run_dir / name).open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    return {"lines": len(facts), "cells": len(evidence), "review": len(review),
            "gaps": sum(1 for r in review if r["gap"])}
