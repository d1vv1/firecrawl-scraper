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
"""

import json
import logging
import re

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
PARTS = ("base_salary", "sti_paid", "benefits", "pension")    # + one LTI figure
TOTAL_TOLERANCE = 0.02                       # protocol: a difference over 2% is noted
PAY_WORDS = 12_000                           # words of a pay document sent to the AI


def ask_pay(name: str, url: str, chunks: list[Chunk], what: str, cache_key: str) -> RemunerationFacts:
    """The remuneration LLM call, cached by the document and chunks it was given."""
    path = CACHE_DIR / f"{cache_key}_pay_llm.json"
    ids = [c.id for c in chunks]
    prompt = llm.load_prompt("remuneration_system")
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if saved.get("chunk_ids") == ids and saved.get("prompt") == prompt:
            return RemunerationFacts.model_validate(saved["facts"])
    body = "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)
    facts = llm.call_llm(prompt, f"Company legal name: {name}\nSource: {url}\n\nExcerpts from "
                                 f"{what} (tables are in markdown):\n\n{body}", RemunerationFacts)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"chunk_ids": ids, "prompt": prompt, "model": llm.model_name(),
                                "facts": facts.model_dump()}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
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
        for tgt, mx in (("sti_target", "sti_max"), ("lti_target", "lti_max")):
            if tgt in rows and mx in rows:
                d = derived_target(rows[tgt], rows[mx])
                if d:
                    rows[tgt] = d
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
