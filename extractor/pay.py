"""Executive pay, role grain (Source_validation protocol R01-R11): one set of rows per
disclosed executive role, read from the remuneration report.

Sources, in order:
  1. the remuneration report (a separate document, found by documents.Library);
  2. else the remuneration section of the annual report (UK and Swiss reports
     include it);
  3. the remuneration policy, only for the STI/LTI targets and maximums the report
     doesn't state.
Amounts are converted to full units like every other money value; the printed figure
and unit, any bundled components and the LTI form go in `note`. LTI is two fields:
vested (paid out for the year) and granted (awarded in the year). Targets and maximums
keep the form the report states (% of base, % of maximum, months of salary, an amount,
a number of shares), with the form in `unit`; a target stated as a share of a maximum
that is a % of base is also given as % of base (method DERIVED). The stated total is
checked against the sum of its parts (a difference over 2% is noted).

Pay tables are wide, and the PDF-to-text conversion can merge two neighbouring columns
into one cell ("96<br>23"); the AI then reads them differently from run to run. So for
a PDF, the pages that look like pay tables are also shown to the AI as images
(table_pages, page_images). Off unless PAY_PAGE_IMAGES=1: see PAGE_IMAGES and
docs/known_issues.md, issue 2.
"""

import json
import logging
import os
import re
from pathlib import Path

from . import llm
from .apis import Found
from .config import CACHE_DIR
from .extract import full_value_quoted
from .schemas import LtiAmount, PayAmount, PayTarget, RemunerationFacts, RolePay
from .sections import Chunk

log = logging.getLogger(__name__)

# Role-grain data points, in output order (protocol field in the comment).
ROLE_POINTS = [
    "role_disclosure",          # R01 individual / aggregate
    "aggregate_headcount",      # R02
    "pay_currency",             # R03
    "base_salary",              # R04
    "sti_paid",                 # R05
    "sti_target", "sti_max",                # R06
    "lti_vested", "lti_granted",            # R07
    "lti_target", "lti_max",                # R08
    "benefits_value",           # R09
    "pension_contribution",     # R10
    "total_remuneration",       # R11
]
AMOUNTS = {"base_salary": "base_salary", "sti_paid": "sti_paid", "lti_vested": "lti_vested",
           "lti_granted": "lti_granted", "benefits_value": "benefits",
           "pension_contribution": "pension", "total_remuneration": "total"}
LTIS = ("lti_vested", "lti_granted")
TARGETS = ("sti_target", "sti_max", "lti_target", "lti_max")
TARGET_UNIT = {"pct_of_base": "% of base salary", "pct_of_max": "% of maximum",
               "months_of_salary": "months of salary", "number_of_shares": "shares", "other": ""}
PARTS = ("base_salary", "sti_paid", "benefits", "pension", "pension_allowance")  # + one LTI
TOTAL_TOLERANCE = 0.02                       # protocol: a difference over 2% is noted
PAY_WORDS = 12_000                           # words of a pay document sent to the AI
MAX_IMAGE_PAGES = 4                          # pay-table pages shown as images, at most
# Off by default: on Equinor's table alone the image gave 5 of 5 fully right answers, but
# in full runs of the 10-company set the golden pay match moved 119 -> 121 -> 119 -> 109
# with small changes to IMAGE_NOTE, and more quotes failed verification (issue 2).
PAGE_IMAGES = os.getenv("PAY_PAGE_IMAGES", "").lower() in ("1", "true", "yes")
IMAGE_DPI = 150                              # about 1,900 tokens for a landscape page
IMAGE_NOTE = ("\n\nImages of the pay-table pages are attached (PDF pages {pages}). The text "
              "above comes from an automatic PDF conversion that can merge neighbouring "
              "table columns; read each figure from its own column in the images. Copy "
              "quotes from the text above.")   # the best-scoring wording tried (121 of 148)
# Words of pay-table headers, in the languages of the company lists.
PAY_TABLE_WORDS = re.compile(
    r"salary|base pay|fixed pay|bonus|incentive|pension|benefit|fees|remuneration|"
    r"compensation|total|lön|ersättning|lønn|godtgjørelse|vederlag|pensjon|palkka|"
    r"palkkio|eläke|vergütung|gehalt|rémunération|salaire|retribución|sueldo|"
    r"retribuzione|compenso|remuneração|bezoldiging|vergoeding|salaris|αποδοχές", re.I)
_YEAR = re.compile(r"(19|20)\d{2}")                 # years in prose are not table figures
_NUMBER = re.compile(r"(?<![\w.])\d{1,3}(?:[ ,.\u00a0]\d{3})+(?:[.,]\d+)?(?!\w)"
                     r"|(?<![\w.])\d+(?:[.,]\d+)?(?!\w)")


def table_pages(chunks: list[Chunk], page_text: dict[int, str],
                n: int = MAX_IMAGE_PAGES) -> list[int]:
    """The pages of these chunks that look like pay tables: many numbers and several
    pay words. At most n, the strongest first; returned in page order."""
    scored = []
    for number in sorted({p for c in chunks for p in c.pages}):
        text = page_text.get(number) or ""
        numbers = sum(1 for n in _NUMBER.findall(text) if not _YEAR.fullmatch(n))
        words = len(PAY_TABLE_WORDS.findall(text))
        if numbers >= 20 and words >= 3:
            scored.append((min(numbers, 200) * min(words, 20), number))
    return sorted(number for _, number in sorted(scored, reverse=True)[:n])


def page_images(pdf: Path, pages: list[int], dpi: int = IMAGE_DPI) -> list[bytes]:
    """PNG renderings of PDF pages (1-based numbers, as in the page markers)."""
    import pymupdf
    with pymupdf.open(pdf) as doc:
        return [doc[p - 1].get_pixmap(dpi=dpi).tobytes("png")
                for p in pages if 1 <= p <= doc.page_count]


def ask_pay(name: str, url: str, chunks: list[Chunk], what: str, cache_key: str,
            pdf: Path | None = None, page_text: dict[int, str] | None = None) -> RemunerationFacts:
    """The remuneration LLM call, cached by the document, the chunks and the page
    images it was given. With the document's PDF (`pdf`) and its page texts, the
    pay-table pages are attached as images."""
    path = CACHE_DIR / f"{cache_key}_pay_llm.json"
    ids = [c.id for c in chunks]
    prompt = llm.load_prompt("remuneration_system")
    shown = (table_pages(chunks, page_text or {})
             if PAGE_IMAGES and pdf and Path(pdf).exists() else [])
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if (saved.get("chunk_ids") == ids and saved.get("prompt") == prompt
                and saved.get("image_pages", []) == shown
                and saved.get("image_note") == (IMAGE_NOTE if shown else None)):
            return RemunerationFacts.model_validate(saved["facts"])
    body = "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)
    user = (f"Company legal name: {name}\nSource: {url}\n\nExcerpts from {what} (tables are "
            f"in markdown):\n\n{body}")
    images = []
    if shown:
        try:
            images = page_images(Path(pdf), shown)
        except Exception as e:  # noqa: BLE001 - a broken render must not cost the text answer
            log.warning("Pay: page images of %s failed: %s", pdf, str(e)[:150])
            shown = []
    if images:
        log.info("Pay: showing PDF page(s) %s as images", ", ".join(map(str, shown)))
        user += IMAGE_NOTE.format(pages=", ".join(map(str, shown)))
    facts = llm.call_llm(prompt, user, RemunerationFacts, images=images or None)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"chunk_ids": ids, "prompt": prompt, "image_pages": shown,
                                "image_note": IMAGE_NOTE if shown else None,
                                "model": llm.model_name(), "facts": facts.model_dump()},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return facts


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def role_names(roles: list[RolePay]) -> list[str]:
    """`role_row` per role: the title; the person's name (or a number) added only when
    two roles share a title."""
    counts: dict[str, int] = {}
    for r in roles:
        counts[_norm_title(r.role_title)] = counts.get(_norm_title(r.role_title), 0) + 1
    out, seen = [], {}
    for r in roles:
        key = _norm_title(r.role_title)
        if counts[key] == 1:
            out.append(r.role_title)
            continue
        seen[key] = seen.get(key, 0) + 1
        out.append(f"{r.role_title} ({r.person_name or seen[key]})")
    return out


def merge_policy(roles: list[RolePay], policy: list[RolePay]) -> dict[int, dict[str, PayTarget]]:
    """Targets and maximums from the policy for roles whose report gives none: by the
    same title, else from the policy's only executive entry (one rule for all)."""
    execs = [p for p in policy if p.executive]
    by_title = {_norm_title(p.role_title): p for p in execs}
    out = {}
    for i, r in enumerate(roles):
        if not r.executive:
            continue
        src = by_title.get(_norm_title(r.role_title)) or (execs[0] if len(execs) == 1 else None)
        if src is None:
            continue
        got = {k: getattr(src, k) for k in TARGETS
               if getattr(r, k).value is None and getattr(src, k).value is not None}
        if got:
            out[i] = got
    return out


def merge_board(roles: list[RolePay]) -> list[RolePay]:
    """All non-executive board entries as one role (protocol: R01 only for the board):
    'individual' when members are listed one by one, else as given."""
    board = [r for r in roles if not r.executive]
    if len(board) <= 1:
        return roles
    first = board[0]
    one = first.model_copy(update={
        "role_title": "Board (non-executive)", "person_name": None,
        "is_aggregate": all(r.is_aggregate for r in board)})
    return [one if r is first else r for r in roles if r.executive or r is first]


def has_pay(facts: RemunerationFacts) -> bool:
    """Some executive role has at least one amount: the document really is a pay
    disclosure, not a page that only names the boards."""
    return any(r.executive and any(getattr(r, f).value is not None and getattr(r, f).quote
                                   for f in AMOUNTS.values())
               for r in facts.roles)


def _amount(a) -> float | None:
    if a.value is None:
        return None
    if getattr(a, "form", None) == "number_of_instruments" or a.unit is None:
        return a.value
    return full_value_quoted(a.value, a.unit, a.quote)


def _target(name: str, t: PayTarget) -> tuple[float, str]:
    """(value, unit) of a target as stated: an amount in full units with its currency,
    else the number with its form ('% of base salary', 'months of salary'...)."""
    if t.form == "amount":
        return (full_value_quoted(t.value, t.unit, t.quote) if t.unit else t.value), t.currency or ""
    return t.value, TARGET_UNIT.get(t.form or "", "") if t.form else "% of base salary"


def months_as_pct(f: Found) -> Found:
    """'Up to 12 months of salary' -> 100% of base salary (12 months = one year's base)."""
    return Found(**{**f.__dict__, "value": round(float(f.value) / 12 * 100, 4),
                    "unit": "% of base salary", "method": "DERIVED",
                    "note": f"derived: stated as {f.value:g} months of salary; {f.note}"})


def with_allowance(pension: Found | None, allowance: Found) -> Found:
    """Pension = pension cost + a salary addition paid instead of pension (the golden
    definition for Norway: Equinor's EVP pension 123 = addition 93 + pension 30)."""
    if pension is None or not isinstance(pension.value, (int, float)):
        return Found(**{**allowance.__dict__, "method": "DERIVED",
                        "note": f"salary addition in lieu of pension only; {allowance.note}"})
    return Found(**{**pension.__dict__, "value": pension.value + allowance.value,
                    "method": "DERIVED", "confidence": max(pension.confidence or "C",
                                                           allowance.confidence or "C",
                                                           key="ABC".index),
                    "note": f"derived: pension {pension.value:,.0f} + salary addition in lieu of "
                            f"pension {allowance.value:,.0f}; {pension.note}"})


def derived_target(target: Found, maximum: Found) -> Found | None:
    """'Target: 50% of the maximum' with a maximum of 80% of base -> 40% of base."""
    if target.unit != "% of maximum" or maximum.unit != "% of base salary":
        return None
    value = round(float(maximum.value) * float(target.value) / 100, 4)
    return Found(target.data_point, value, unit="% of base salary", period_end=target.period_end,
                 source=target.source, endpoint=target.endpoint, method="DERIVED",
                 confidence=max(target.confidence or "C", maximum.confidence or "C",
                                key="ABC".index),     # the weaker of the two
                 note=f"derived: {target.value:g}% of the maximum of {maximum.value:g}% of base "
                      f"salary; {target.note}",
                 retrieved_at=target.retrieved_at, grain="role", role_row=target.role_row)


def role_found(facts: RemunerationFacts, origin, policy: RemunerationFacts | None = None,
               policy_origin=None, period_end: str = "") -> list[Found]:
    """The role rows: every ROLE_POINTS field for each executive role (missing ones with
    a reason), only role_disclosure for non-executive board members."""
    roles = merge_board([r for r in facts.roles if r.role_title])
    names = role_names(roles)
    from_policy = merge_policy(roles, policy.roles) if policy and policy_origin else {}
    out: list[Found] = []

    def placed(name, row, value, fact, src, unit="", extra=""):
        doc, endpoint, conf, where = src.place(fact.quote, fact.chunk_id)
        return Found(name, value, unit=unit, period_end=period_end, source=doc.source,
                     endpoint=endpoint, method=doc.method, confidence=conf,
                     note="; ".join(x for x in (extra, where) if x), retrieved_at=doc.retrieved_at,
                     grain="role", role_row=row)

    def missing(name, row, why=f"not found in: {origin.source}"):
        return Found(name, None, note=why, grain="role", role_row=row)

    for i, (r, row) in enumerate(zip(roles, names)):
        kind = "aggregate" if r.is_aggregate else "individual"
        who = "executive" if r.executive else "non-executive board"
        # Where the role is disclosed: its own quote, else its first pay figure's row.
        cite = r if r.quote else next((getattr(r, f) for f in AMOUNTS.values()
                                       if getattr(r, f).quote), None)
        if cite is not None:
            out.append(placed("role_disclosure", row, kind, cite, origin, extra=who))
        else:
            out.append(Found("role_disclosure", kind, source=origin.source,
                             note=f"{who}; role named without a quote", confidence="C",
                             grain="role", role_row=row))
        if not r.executive:
            continue                                # protocol: R01 only for the board
        rows: dict[str, Found] = {}
        h = r.aggregate_headcount
        if r.is_aggregate and h.value is not None and h.quote:
            rows["aggregate_headcount"] = placed(
                "aggregate_headcount", row, h.value, h, origin, unit="people",
                extra=f"excludes {h.excludes}" if h.excludes else "")
        for name, field in AMOUNTS.items():
            a = getattr(r, field)
            if a.value is None or not a.quote:
                continue
            number = getattr(a, "form", None) == "number_of_instruments"
            extra = [f"printed {a.value:g} {a.unit or ''}".strip()]
            if getattr(a, "form", None):
                extra.append(f"form: {a.form.replace('_', ' ')}")
            if a.includes:
                extra.append(f"includes {a.includes}")
            rows[name] = placed(name, row, _amount(a), a, origin,
                                unit="instruments" if number else (a.currency or ""),
                                extra="; ".join(extra))
        money = next((rows[k] for k in ("total_remuneration", "base_salary") if k in rows), None)
        unit_of = next((getattr(r, f) for f in ("total", "base_salary")
                        if getattr(r, f).value is not None and getattr(r, f).quote), None)
        if money and money.unit and unit_of:
            rows["pay_currency"] = Found("pay_currency", money.unit, source=money.source,
                                         endpoint=money.endpoint, method=money.method,
                                         confidence=money.confidence,
                                         note=f"table unit: {unit_of.unit or 'not stated'}",
                                         retrieved_at=money.retrieved_at, grain="role", role_row=row)
        for name in TARGETS:
            t: PayTarget = getattr(r, name)
            if t.value is not None and t.quote:
                value, unit = _target(name, t)
                rows[name] = placed(name, row, value, t, origin, unit=unit)
        for name, t in from_policy.get(i, {}).items():
            if t.quote:
                value, unit = _target(name, t)
                rows[name] = placed(name, row, value, t, policy_origin, unit=unit,
                                    extra="from the remuneration policy")
        for name in TARGETS:
            if name in rows and rows[name].unit == "months of salary":
                rows[name] = months_as_pct(rows[name])
        for tgt, mx in (("sti_target", "sti_max"), ("lti_target", "lti_max")):
            if tgt in rows and mx in rows:
                d = derived_target(rows[tgt], rows[mx])
                if d:
                    rows[tgt] = d
        allowance = r.pension_allowance
        if allowance.value is not None and allowance.quote:
            rows["pension_contribution"] = with_allowance(
                rows.get("pension_contribution"), placed(
                    "pension_contribution", row, _amount(allowance), allowance, origin,
                    unit=allowance.currency or "", extra=f"printed {allowance.value:g} "
                                                         f"{allowance.unit or ''}".strip()))
        check_total(r, rows)
        for name in ROLE_POINTS[1:]:
            if name in rows:
                out.append(rows[name])
            elif name == "aggregate_headcount" and not r.is_aggregate:
                out.append(missing(name, row, "not applicable: one person"))
            else:
                out.append(missing(name, row))
    return out


def check_total(r: RolePay, rows: dict[str, Found]) -> None:
    """Protocol R11: the stated total against base + STI + LTI + benefits + pension. The
    LTI figure the total includes is the one that fits: vested, granted or none."""
    total = rows.get("total_remuneration")
    if not total or not isinstance(total.value, (int, float)) or not total.value:
        return
    parts = [_amount(getattr(r, p)) for p in PARTS if getattr(r, p).value is not None]
    ltis = [("vested", _amount(r.lti_vested)), ("granted", _amount(r.lti_granted)), ("no", 0)]
    ltis = [(k, v) for k, v in ltis if v is not None and not (
        k != "no" and getattr(r, f"lti_{k}").form == "number_of_instruments")]
    if len(parts) < 2:
        return
    kind, lti = min(ltis, key=lambda kv: abs(sum(parts) + kv[1] - total.value))
    s = sum(parts) + lti
    diff = (s - total.value) / total.value
    if abs(diff) > TOTAL_TOLERANCE:
        total.note += (f"; the parts found add up to {s:,.0f} ({diff:+.1%} against the "
                       f"stated total){'' if len(parts) == len(PARTS) else ', some parts missing'}")
    elif kind != "no":
        total.note += f"; equals the parts with the LTI {kind}"


def company_terms(facts: RemunerationFacts, origin) -> list[Found]:
    """Protocol C23 at company level: pension type, benefits, shareholding requirement."""
    out = []
    for name in ("pension_type", "benefits", "shareholding_requirement"):
        t = getattr(facts, name)
        if t.value and t.quote:
            doc, endpoint, conf, where = origin.place(t.quote, t.chunk_id)
            out.append(Found(name, t.value, source=doc.source, endpoint=endpoint, method=doc.method,
                             confidence=conf, note=where, retrieved_at=doc.retrieved_at))
    return out


def needs_policy(facts: RemunerationFacts) -> bool:
    """Some executive role lacks a target or maximum percentage."""
    return any(r.executive and any(getattr(r, k).value is None for k in TARGETS)
               for r in facts.roles)
