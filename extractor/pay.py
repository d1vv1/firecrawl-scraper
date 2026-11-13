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
a PDF, the amounts of roles found in a pay table are taken from the table itself
(pay_tables.py: Camelot reads it, a small AI call maps its columns, code adds up), and
the pages that look like pay tables (table_pages) are the ones it reads. Showing those
pages to the AI as images (page_images) is off unless PAY_PAGE_IMAGES=1: see PAGE_IMAGES
and docs/known_issues.md, issue 2.
"""

import json
import logging
import os
import re
from pathlib import Path

from . import llm
from .apis import Found
from .config import CACHE_DIR
from .extract import _QUOTE_NUMBER, _quote_numbers, full_value_quoted, printed_figure
from .validate import ISO_4217, figure_in_quote, iso_currency, normalize
from .schemas import LtiAmount, PayAmount, PayTarget, RemunerationFacts, RolePay
from .sections import Chunk

log = logging.getLogger(__name__)


def percent_only(value: float, quote: str | None) -> bool:
    """The quote prints the value only as a percentage ("200% of salary"), never bare."""
    if not quote:
        return False
    t = re.sub(r"(?<=\d),(?=\d)", ".", normalize(quote))
    hits = [m for m in re.finditer(r"\d+(?:\.\d+)?", t) if abs(float(m.group()) - value) < 1e-9]
    return bool(hits) and all(re.match(r"\s*(%|per ?cent|prozent|procent|prosent)", t[m.end():])
                              for m in hits)

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
               "pct_of_target": "% of target",
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


def _num(v: float) -> str:
    """1057875.0 -> "1057875", 12.5 -> "12.5" (never "1.05788e+06", which loses digits)."""
    return str(int(v)) if float(v).is_integer() else f"{v:.6f}".rstrip("0").rstrip(".")


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
                    "note": f"derived: stated as {_num(f.value)} months of salary; {f.note}"})


def _second_source(note: str) -> str:
    """A second figure's note, worded so that it is not taken for the row's own source:
    datapoints.repair_quotes reads one `PDF page N: "quote" (quote not found verbatim)`
    per note and would run from the first figure's quote into this one's marker."""
    note = re.sub(r'(PDF page \d+|report text|web page): "', r'\1, quote "', note)
    note = note.replace("is not in the quote", "is not in that quote")
    return note.replace("(quote not found verbatim)", "(this quote was not found verbatim)")


# A second figure's source that could not be checked: the row stays at confidence C.
SECOND_SOURCE_UNSURE = re.compile("this quote was not found verbatim|is not in that quote")


def same_cell(r: RolePay) -> bool:
    """sti_deferred is no figure of its own: the bonus figure given a second time (same
    quote, same amount, and the quote prints it once; twice is a bonus split in two
    equal columns), or the role's LTI figure (a deferred share award read as both)."""
    paid, d = r.sti_paid, r.sti_deferred
    amount = _amount(d)
    if amount in (_amount(r.lti_vested), _amount(r.lti_granted)):
        return True
    if paid.value is None or _amount(paid) != amount or paid.quote != d.quote:
        return False
    figure = printed_figure(d.value, d.unit, d.quote)
    return sum(figure in _quote_numbers(t) for t in _QUOTE_NUMBER.findall(d.quote or "")) < 2


def other_currency(a: str | None, b: str | None) -> bool:
    """Two currencies known to differ: both ISO codes once normalised ("US$" is "USD").
    A spelling that is not recognised ("kr", "pounds") is not taken as another currency."""
    a, b = iso_currency(a or ""), iso_currency(b or "")
    return a in ISO_4217 and b in ISO_4217 and a != b


def with_deferred(cash: Found | None, deferred: Found, how: str | None = None) -> Found:
    """The year's bonus = the part paid in cash + the part deferred, which the pay table
    gives in two columns (Big Yellow: "Annual bonus – cash" 29,689 and "Annual bonus –
    deferred" 300,494, in shares). `how`: the form of the deferred part, for the note."""
    form = f" ({how})" if how else ""
    if cash is None or not isinstance(cash.value, (int, float)):
        return Found(**{**deferred.__dict__, "method": "DERIVED",
                        "note": f"derived: the annual bonus = the part deferred{form} (no cash "
                                f"part given); {deferred.note}"})
    return Found(**{**cash.__dict__, "value": cash.value + deferred.value, "method": "DERIVED",
                    "unit": cash.unit or deferred.unit,
                    "confidence": max(cash.confidence or "C", deferred.confidence or "C",
                                      key="ABC".index),
                    # .15g: whole amounts as 29,689, a table in millions as 0.4 (DER-03
                    # adds the two up again from this note)
                    "note": f"derived: annual bonus in cash {cash.value:,.15g} + deferred bonus "
                            f"{deferred.value:,.15g}{form}; {cash.note}; the deferred part: "
                            f"{_second_source(deferred.note)}"})


def _lti_options(r: RolePay) -> list[tuple[str, float]]:
    """The LTI figures a stated total can include: the vested one, the granted one or
    none. A number of instruments is no amount."""
    ltis = [("vested", _amount(r.lti_vested)), ("granted", _amount(r.lti_granted)), ("no", 0)]
    return [(k, v) for k, v in ltis if v is not None and not (
        k != "no" and getattr(r, f"lti_{k}").form == "number_of_instruments")]


def deferred_on_top(r: RolePay) -> bool:
    """Whether sti_deferred comes on top of sti_paid (two columns, cash and deferred) and
    is not a part of a sti_paid that is already the whole bonus ("Annual bonus 330,183,
    of which deferred 300,494"). A deferred part above sti_paid can't be a part of it.
    Otherwise the stated total decides: not on top only when the total fits the parts
    without it, and fits them better than with it. With no total to go by it is on top,
    which is what the prompt asks for (it tells the AI to leave an "of which" null)."""
    cash, deferred, total = _amount(r.sti_paid), _amount(r.sti_deferred), _amount(r.total)
    if cash is None or deferred is None or not total or deferred > cash:
        return True
    rest = sum(_amount(getattr(r, p)) for p in PARTS
               if p != "sti_paid" and getattr(r, p).value is not None)

    def off(bonus: float) -> float:
        return min(abs(rest + bonus + lti - total) for _, lti in _lti_options(r))
    return not (off(cash) <= TOTAL_TOLERANCE * abs(total) and off(cash) < off(cash + deferred))


def with_allowance(pension: Found | None, allowance: Found) -> Found:
    """Pension = pension cost + a salary addition paid instead of pension (the golden
    definition for Norway: Equinor's EVP pension 123 = addition 93 + pension 30)."""
    if pension is None or not isinstance(pension.value, (int, float)):
        return Found(**{**allowance.__dict__, "method": "DERIVED",
                        "note": f"derived: pension = the salary addition or cash paid in lieu of "
                                f"pension (no pension cost given); {allowance.note}"})
    return Found(**{**pension.__dict__, "value": pension.value + allowance.value,
                    "method": "DERIVED", "confidence": max(pension.confidence or "C",
                                                           allowance.confidence or "C",
                                                           key="ABC".index),
                    "note": f"derived: pension {pension.value:,.0f} + salary addition in lieu of "
                            f"pension {allowance.value:,.0f}; {pension.note}"})


# Words that mark a salary addition paid instead of pension, in the report languages.
IN_LIEU = re.compile(r"addition|allowance|in lieu|instead|cash|supplement|tillegg|tillägg|"
                     r"i stedet|i stället|lisä|kompensa|compensat", re.I)


def derived_max(maximum: Found, target: Found) -> Found | None:
    """'Maximum bonus: 200% of target' with a target of 125% of base -> 250% of base."""
    if maximum.unit != "% of target" or target.unit != "% of base salary":
        return None
    value = round(float(target.value) * float(maximum.value) / 100, 4)
    return Found(maximum.data_point, value, unit="% of base salary", period_end=maximum.period_end,
                 source=maximum.source, endpoint=maximum.endpoint, method="DERIVED",
                 confidence=max(target.confidence or "C", maximum.confidence or "C",
                                key="ABC".index),
                 note=f"derived: {_num(maximum.value)}% of the target of {_num(target.value)}% of "
                      f"base salary; {maximum.note}",
                 retrieved_at=maximum.retrieved_at, grain="role", role_row=maximum.role_row)


def derived_target(target: Found, maximum: Found) -> Found | None:
    """'Target: 50% of the maximum' with a maximum of 80% of base -> 40% of base."""
    if target.unit != "% of maximum" or maximum.unit != "% of base salary":
        return None
    value = round(float(maximum.value) * float(target.value) / 100, 4)
    return Found(target.data_point, value, unit="% of base salary", period_end=target.period_end,
                 source=target.source, endpoint=target.endpoint, method="DERIVED",
                 confidence=max(target.confidence or "C", maximum.confidence or "C",
                                key="ABC".index),     # the weaker of the two
                 note=f"derived: {_num(target.value)}% of the maximum of {_num(maximum.value)}% of base "
                      f"salary; {target.note}",
                 retrieved_at=target.retrieved_at, grain="role", role_row=target.role_row)


def misread_targets(rows: dict[str, Found]) -> None:
    """Undo three AI misreadings of a role's target and maximum. Nothing is filled in:
    a target or maximum the documents don't state stays empty (a target isn't always
    half the maximum: Bang & Olufsen's are 100% and 175%; many Nordic policies state
    only a maximum).
    - A maximum read as a share of the target but below 100% of it is the % of base
      salary it is printed as ("a maximum opportunity of 87.5%").
    - A target and maximum with one figure from one quote are that figure as the
      maximum ("the target bonus may amount to a maximum of 50 percent").
    - A target above its maximum is not kept."""
    pct = "% of base salary"
    for tgt, mx in (("sti_target", "sti_max"), ("lti_target", "lti_max")):
        t, m = rows.get(tgt), rows.get(mx)
        below = re.match(r"derived: ([\d.]+)% of the target of [\d.]+% of base salary; (.*)", m.note) if m else None
        if below and float(below.group(1)) < 100:
            # "a maximum opportunity of 87.5%" read as % of target: a maximum below the
            # target is impossible, so it is the % of base salary it is printed as
            rows[mx] = m = Found(**{**m.__dict__, "value": float(below.group(1)), "method": "PARSE",
                                    "note": f"{below.group(2)}; read as % of base salary (below "
                                            f"100% of the target, it can't be a share of it)"})
        if t and m and t.unit == pct and m.unit == pct and t.method != "DERIVED" and (
                (float(t.value) == float(m.value) and t.note == m.note)
                or float(t.value) > float(m.value)):
            del rows[tgt]


def role_found(facts: RemunerationFacts, origin, policy: RemunerationFacts | None = None,
               policy_origin=None, period_end: str = "") -> list[Found]:
    """The role rows: every ROLE_POINTS field for each executive role (missing ones with
    a reason), only role_disclosure for non-executive board members."""
    roles = merge_board([r for r in facts.roles if r.role_title])
    names = role_names(roles)
    from_policy = merge_policy(roles, policy.roles) if policy and policy_origin else {}
    out: list[Found] = []

    def placed(name, row, value, fact, src, unit="", extra="", figure=None):
        doc, endpoint, conf, where, quote = src.place(fact.quote, fact.chunk_id, figure)
        if figure is not None and not figure_in_quote(figure, quote):
            # added up, multiplied or taken from the wrong sentence (Nokia's LTI target
            # 2.8m + 5.6m; a maximum quoted from "300% of salary")
            conf, where = "C", f"{where}; the figure {_num(figure)} is not in the quote"
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
            # a pay figure in the cited row lets a pieced-together quote become its source row
            amounts = [getattr(r, f).value for f in AMOUNTS.values() if getattr(r, f).value is not None]
            figure = next((v for v in amounts if figure_in_quote(v, cite.quote)), None)
            out.append(placed("role_disclosure", row, kind, cite, origin, extra=who, figure=figure))
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
            if not number and not a.currency and percent_only(a.value, a.quote):
                # "LTIP award of 200% of salary", "Bonus achieved 60%": a share, not an amount
                rows[name] = missing(name, row, f"stated only as {_num(a.value)}% "
                                                f"(\"{a.quote[:80]}\"), not as an amount")
                continue
            figure = a.value if number else printed_figure(a.value, a.unit, a.quote)
            extra = [f"printed {_num(figure)} {a.unit or ''}".strip()]
            if getattr(a, "form", None):
                extra.append(f"form: {a.form.replace('_', ' ')}")
            if a.includes:
                extra.append(f"includes {a.includes}")
            rows[name] = placed(name, row, _amount(a), a, origin,
                                unit="instruments" if number else (a.currency or ""),
                                extra="; ".join(extra), figure=figure)
        money = next((rows[k] for k in ("total_remuneration", "base_salary") if k in rows), None)
        unit_of = next((getattr(r, f) for f in ("total", "base_salary")
                        if getattr(r, f).value is not None and getattr(r, f).quote), None)
        if money and money.unit and unit_of:
            rows["pay_currency"] = Found("pay_currency", money.unit, period_end=money.period_end,
                                         source=money.source,
                                         endpoint=money.endpoint, method=money.method,
                                         confidence=money.confidence,
                                         note=f"table unit: {unit_of.unit or 'not stated'}",
                                         retrieved_at=money.retrieved_at, grain="role", role_row=row)
        for name in TARGETS:
            t: PayTarget = getattr(r, name)
            if t.value is not None and t.quote:
                value, unit = _target(name, t)
                rows[name] = placed(name, row, value, t, origin, unit=unit, figure=t.value)
        for name, t in from_policy.get(i, {}).items():
            if t.quote:
                value, unit = _target(name, t)
                rows[name] = placed(name, row, value, t, policy_origin, unit=unit,
                                    extra="from the remuneration policy", figure=t.value)
        for name in TARGETS:
            if name in rows and rows[name].unit == "months of salary":
                rows[name] = months_as_pct(rows[name])
        for tgt, mx in (("sti_target", "sti_max"), ("lti_target", "lti_max")):
            if tgt in rows and mx in rows:
                d = derived_max(rows[mx], rows[tgt])
                if d:
                    rows[mx] = d
                d = derived_target(rows[tgt], rows[mx])
                if d:
                    rows[tgt] = d
        misread_targets(rows)
        deferred, added = r.sti_deferred, False     # added: the deferred bonus is in sti_paid
        cash = rows.get("sti_paid")
        if cash is not None and not isinstance(cash.value, (int, float)):
            cash = None                             # stated only as a percentage: no amount
        if (deferred.value and deferred.quote       # a deferred part of 0 or "–" is none
                # an amount of money: not "50% of the bonus is deferred into shares", and
                # not a number of shares, which comes with no currency and no unit
                and (deferred.currency or deferred.unit)
                and not percent_only(deferred.value, deferred.quote)):
            amount = _amount(deferred)
            if same_cell(r):
                pass                                # the bonus or LTI figure given twice
            elif not cash and r.sti_paid.value is not None:
                pass        # a cash part that is no amount (a percentage, no quote): the
                #             deferred part alone would pass for the whole bonus
            elif cash and other_currency(deferred.currency, cash.unit):
                cash.note += (f"; a deferred part of {amount:,.0f} {deferred.currency} is "
                              f"stated in another currency and is not added")
            elif cash and not deferred_on_top(r):
                cash.note += (f"; includes the deferred part of {amount:,.0f} (the stated "
                              f"total fits the parts only without adding it)")
            else:
                figure = printed_figure(deferred.value, deferred.unit, deferred.quote)
                rows["sti_paid"] = with_deferred(
                    cash, placed("sti_paid", row, amount, deferred, origin,
                                 unit=deferred.currency or "", figure=figure,
                                 extra=f"printed {_num(figure)} {deferred.unit or ''}".strip()),
                    deferred.includes)
                added = True
        allowance = r.pension_allowance
        if (allowance.value is not None and allowance.quote and "pension_contribution" not in rows
                and not IN_LIEU.search(f"{allowance.quote} {allowance.includes or ''}")):
            # Shell's "Pension [C] | 307": a pension, not an addition paid instead of one
            rows["pension_contribution"] = placed(
                "pension_contribution", row, _amount(allowance), allowance, origin,
                unit=allowance.currency or "", figure=allowance.value,
                extra=f"printed {_num(allowance.value)} {allowance.unit or ''}".strip())
        elif allowance.value is not None and allowance.quote:
            rows["pension_contribution"] = with_allowance(
                rows.get("pension_contribution"), placed(
                    "pension_contribution", row, _amount(allowance), allowance, origin,
                    unit=allowance.currency or "", extra=f"printed {_num(allowance.value)} "
                                                         f"{allowance.unit or ''}".strip()))
        check_total(r, rows, added)
        for name in ROLE_POINTS[1:]:
            if name in rows:
                out.append(rows[name])
            elif name == "aggregate_headcount" and not r.is_aggregate:
                out.append(missing(name, row, "not applicable: one person"))
            else:
                out.append(missing(name, row))
    return out


SUM_TOLERANCE = 0.01        # a total line's parts: within 1%,
ROUNDED_TOLERANCE = 0.05    # or within their printed rounding, up to 5%
_PRINTED = re.compile(r"printed (-?\d+(?:\.(\d+))?)(?: (thousands|millions|billions|units))?")
_SCALE = {"thousands": 1e3, "millions": 1e6, "billions": 1e9, "units": 1}


def _rounding(note: str) -> float:
    """Half the last printed digit of an amount, in full units, from its note: "printed
    2.4 millions" -> 50,000. 0 when the note doesn't say."""
    m = _PRINTED.search(note or "")
    if not m:
        return 0.0
    return 0.5 * 10 ** -len(m.group(2) or "") * _SCALE.get(m.group(3) or "units", 1)


def total_roles(rows: list) -> list[str]:
    """The role rows that are a pay table's "Total" line: an aggregate role whose amounts
    are the sums of the roles listed next to it (Brøndby IF: "Total" = CEO + CFO; Stora
    Enso: "GLT Total" = CEO + other members). Those people are already in the output, so
    the line would count their pay twice. An aggregate that is the only record of its
    people ("Other members of the Group Leadership Team") is no sum of other rows.
    `rows`: role rows as Found or as CSV rows, in output order.

    The roles next to it: two or more with amounts, directly before it, after it, or on
    both sides (CEO, Total, Other members). Fields are compared where every one of them
    states the field in the total's unit. A field adds up within 1%, or within the
    rounding of the printed figures up to 5% (CEO 1.4 + CFO 0.9 against a Total of 2.4,
    in EUR m). The total remuneration within 1% is enough; otherwise two fields must add
    up: a lone figure in whole millions is matched by too many mixes of roles (BMW's
    "Board of Management 23 million"). One field that doesn't is no objection: Aurskog Sparebank's total line has the base salaries and pensions of
    its seven executives to the krone, and a benefits figure misread."""
    def get(r, k):
        return r.get(k) if isinstance(r, dict) else getattr(r, k, None)

    amounts: dict[str, dict[str, tuple[float, str, float]]] = {}
    aggregate: set[str] = set()
    for r in rows:
        name, point, value = get(r, "role_row"), get(r, "data_point"), get(r, "value")
        if get(r, "grain") != "role" or value in (None, ""):
            continue
        if point == "role_disclosure" and value == "aggregate":
            aggregate.add(name)
        if point in AMOUNTS:
            try:
                amounts.setdefault(name, {})[point] = (float(value), get(r, "unit") or "",
                                                       _rounding(get(r, "note")))
            except ValueError:
                pass
    order = list(amounts)

    def is_sum(total: dict, parts: list[dict]) -> bool:
        exact, good = [], []
        for point, (value, unit, step) in total.items():
            if not value or not all(point in p and p[point][1] == unit for p in parts):
                continue
            off = abs(sum(p[point][0] for p in parts) - value)
            rounding = step + sum(p[point][2] for p in parts)
            if off <= SUM_TOLERANCE * abs(value):
                exact.append(point)
                good.append(point)
            elif off <= rounding and off <= ROUNDED_TOLERANCE * abs(value):
                good.append(point)
        return "total_remuneration" in exact or len(good) >= 2

    found: list[str] = []
    for i, name in enumerate(order):
        if name not in aggregate:
            continue
        before = [n for n in order[:i] if n not in found]
        after = [n for n in order[i + 1:] if n not in found]
        runs = [before[len(before) - b:] + after[:a]
                for b in range(len(before) + 1) for a in range(len(after) + 1) if a + b >= 2]
        if any(is_sum(amounts[name], [amounts[n] for n in run]) for run in runs):
            found.append(name)
    return found


def check_total(r: RolePay, rows: dict[str, Found], deferred_added: bool = False) -> None:
    """Protocol R11: the stated total against base + STI + LTI + benefits + pension. The
    LTI figure the total includes is the one that fits: vested, granted or none.
    `deferred_added`: role_found added the deferred bonus to sti_paid; the STI part is
    then the sti_paid row as written out."""
    total = rows.get("total_remuneration")
    if not total or not isinstance(total.value, (int, float)) or not total.value:
        return
    amounts = {p: _amount(getattr(r, p)) for p in PARTS if getattr(r, p).value is not None}
    if deferred_added:
        amounts["sti_paid"] = rows["sti_paid"].value
    parts = list(amounts.values())
    ltis = _lti_options(r)
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
            doc, endpoint, conf, where, _ = origin.place(t.quote, t.chunk_id)
            out.append(Found(name, t.value, source=doc.source, endpoint=endpoint, method=doc.method,
                             confidence=conf, note=where, retrieved_at=doc.retrieved_at))
    return out


def needs_policy(facts: RemunerationFacts) -> bool:
    """Some executive role lacks a target or maximum percentage."""
    return any(r.executive and any(getattr(r, k).value is None for k in TARGETS)
               for r in facts.roles)


def duplicate_groups(rows: list) -> list[str]:
    """Group roles read twice: an aggregate role whose amounts are the same as an earlier
    aggregate role's, field for field, value and unit. The remuneration report and the
    annual report's pay note print the same table, and the AI names the row differently
    in each ("Other EC Members" and "Other EC", dormakaba; "Other IEC members" and
    "Übrige Mitglieder des IEC", Implenia), so the pay was counted twice. The first one,
    from the document read first, stays. At least two amounts must be non-zero: a row of
    zeros ("Former members|0|0|0") says nothing about who it is.

    Individual roles are left alone: two executives can be paid the same (Vontobel's
    co-CEOs), and where they aren't, it is a misread no rule can resolve.
    `rows`: role rows as Found or as CSV rows, in output order."""
    def get(r, k):
        return r[k] if isinstance(r, dict) else getattr(r, k)

    amounts: dict[str, dict[str, tuple[float, str]]] = {}
    aggregate: set[str] = set()
    for r in rows:
        name, point, value = get(r, "role_row"), get(r, "data_point"), get(r, "value")
        if get(r, "grain") != "role" or value in (None, ""):
            continue
        if point == "role_disclosure" and value == "aggregate":
            aggregate.add(name)
        if point in AMOUNTS:
            try:
                amounts.setdefault(name, {})[point] = (float(value), get(r, "unit") or "")
            except ValueError:
                pass
    seen: dict[tuple, str] = {}
    out = []
    for name, d in amounts.items():
        if name not in aggregate or sum(1 for v, _ in d.values() if v) < 2:
            continue
        key = tuple(sorted(d.items()))
        if key in seen:
            out.append(name)
        else:
            seen[key] = name
    return out


# The line of a pay table that is an accounting item, not a person ("Option and share
# program expenses (note 17)", S&D Standard, where the AI took the section heading
# "Subsidiary employee:" above it for a role).
ACCOUNTING_LINE = re.compile(r"\b(expenses?|costs?|provisions?|accruals?|ifrs ?2|note \d+|"
                             r"aufwand|aufwendungen|kostnad\w*|kostnader|omkostninger)\b", re.I)


def accounting_lines(rows: list) -> list[str]:
    """Individual roles that are an accounting line of the pay table: every amount zero
    (dashes) and the line quoted names an expense, cost or note, not a person. A person
    paid nothing stays (Wild Bunch's CEO, Sino-German's board: "Der Vorstandsvorsitzende
    Hui Wang"). `rows`: role rows as Found or as CSV rows."""
    def get(r, k):
        return r[k] if isinstance(r, dict) else getattr(r, k)

    quote, individual, amounts = {}, set(), {}
    for r in rows:
        name, point, value = get(r, "role_row"), get(r, "data_point"), get(r, "value")
        if get(r, "grain") != "role" or value in (None, ""):
            continue
        if point == "role_disclosure":
            quote[name] = get(r, "note") or ""
            if value == "individual":
                individual.add(name)
        if point in AMOUNTS:
            try:
                amounts.setdefault(name, []).append(float(value))
            except ValueError:
                amounts.setdefault(name, []).append(1.0)
    return [n for n in amounts if n in individual and not any(amounts[n])
            and ACCOUNTING_LINE.search(quote.get(n, ""))]
