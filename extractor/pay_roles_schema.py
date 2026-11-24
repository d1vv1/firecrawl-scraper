"""What the AI returns to the role-based pay extractor (pay_roles.py), and how each pay field
lands in the BigQuery fact_pay_line table.

Everything is verbatim: a value is the number as the report prints it ("12 400" in a tkr
table is 12400, never 12,400,000), with the figure, its unit and its currency also kept as
printed ("12 400", "tkr", "SEK"). Nothing is scaled, converted or added up here; the CDP
normalises units and currencies when it loads the rows.

The models are built per request: a by-field run asks only for the fields it names, so the
AI is never shown (or asked to fill) a field nobody wants. Like schemas.py, the models have no
defaults: structured outputs in strict mode need every field.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel, create_model

from .schemas import LtiForm, TargetForm, Unit

RoleDisclosure = Literal["individual", "individual_unnamed", "aggregate", "not_disclosed"]
PeriodCoverage = Literal["full_year", "joined_in_year", "left_in_year", "joined_and_left",
                         "not_stated"]


class PayCell(BaseModel):
    """One amount of money, as printed."""
    value: Optional[float]          # the printed number, no scaling ("12 400" -> 12400)
    printed: Optional[str]          # the figure exactly as printed: "12 400", "(1,250)", "1.234,5"
    unit_printed: Optional[str]     # the unit as printed: "tkr", "TSEK", "SEK thousand", "T€", "MNOK"
    unit: Optional[Unit]            # the scale that unit stands for (for checks only)
    currency_printed: Optional[str]  # as printed: "SEK", "kr", "€", "EUR"
    includes: Optional[str]         # other components bundled in, e.g. "incl. holiday pay"
    quote: Optional[str]
    chunk_id: Optional[int]


class LtiCell(BaseModel):
    """A long-term incentive amount, as printed: money or a number of instruments."""
    value: Optional[float]
    printed: Optional[str]
    unit_printed: Optional[str]
    unit: Optional[Unit]
    currency_printed: Optional[str]  # null for a number of instruments
    form: Optional[LtiForm]
    includes: Optional[str]
    quote: Optional[str]
    chunk_id: Optional[int]


class TargetCell(BaseModel):
    """A target or maximum opportunity in the form the report states it."""
    value: Optional[float]          # as stated: 60 (% of base), 200 (% of target), 6 (months)
    printed: Optional[str]          # as printed: "60%", "6 months' salary", "SEK 2.4m"
    form: Optional[TargetForm]
    unit_printed: Optional[str]     # for an amount only
    currency_printed: Optional[str]  # for an amount only
    quote: Optional[str]
    chunk_id: Optional[int]


@dataclass(frozen=True)
class Field:
    name: str
    cell: type[BaseModel]
    columns: tuple[str, ...]        # fact_pay_line column(s); () = evidence file only
    phase: int = 1                  # 2: LTI detail, not asked yet


# Order is the prompt's and the CSV's order. Targets fill a value and a basis column.
FIELDS: dict[str, Field] = {f.name: f for f in [
    Field("base_salary", PayCell, ("base_salary",)),
    Field("committee_fees", PayCell, ()),
    Field("meeting_fees", PayCell, ()),
    Field("benefits", PayCell, ("benefits_value",)),
    Field("pension", PayCell, ("pension_contribution",)),
    Field("pension_allowance", PayCell, ()),
    Field("sti_paid", PayCell, ("sti_paid",)),
    Field("sti_deferred", PayCell, ()),
    Field("lti_vested", LtiCell, ("lti_vested",)),
    Field("lti_granted", LtiCell, ("lti_granted",)),
    Field("other_pay", PayCell, ()),
    Field("total", PayCell, ("total_remuneration",)),
    Field("sti_target", TargetCell, ("sti_target_value", "sti_target_basis")),
    Field("sti_max", TargetCell, ("sti_max_value", "sti_max_basis")),
    Field("lti_target", TargetCell, ("lti_target_value", "lti_target_basis")),
    Field("lti_max", TargetCell, ("lti_max_value", "lti_max_basis")),
]}
CORE_FIELDS = [n for n, f in FIELDS.items() if f.phase == 1]

# What every line carries whatever fields are asked for.
LINE_FIELDS: dict[str, tuple] = {
    # the row's label as printed, which is often only a name ("Henrik Lind"): a place for it,
    # so that printed_title can be the function (in the pilot, names ended up as titles)
    "row_label": (Optional[str], ...),
    "printed_title": (str, ...),                    # the role or person's function, as printed
    "person_name": (Optional[str], ...),
    "is_aggregate": (bool, ...),
    "aggregate_headcount": (Optional[float], ...),
    "aggregate_excludes": (Optional[str], ...),     # who an aggregate leaves out ("the CEO")
    "role_disclosure": (RoleDisclosure, ...),
    "period_coverage": (PeriodCoverage, ...),
    "months_in_role": (Optional[float], ...),       # only when the text states months
    "period_quote": (Optional[str], ...),           # the words that say joined / left / dates
    "suggested_role_detail": (Optional[str], ...),  # one of the role list given, or null
    "suggested_cdp_role_id": (Optional[str], ...),  # only when no role_detail fits
    "suggestion_reason": (Optional[str], ...),
    "quote": (Optional[str], ...),                  # where the line is disclosed
    "chunk_id": (Optional[int], ...),
}


def check_fields(names: list[str]) -> list[str]:
    unknown = [n for n in names if n not in FIELDS]
    if unknown:
        raise ValueError(f"unknown pay field(s): {', '.join(unknown)}; "
                         f"known: {', '.join(FIELDS)}")
    return [n for n in FIELDS if n in names]        # in FIELDS order, no repeats


def line_model(fields: list[str]) -> type[BaseModel]:
    """A pay line with these pay fields (and the line fields every line has)."""
    fields = check_fields(fields)
    spec = dict(LINE_FIELDS)
    # a field the text does not give is null, not an object of nulls: an answer of 30 lines
    # with 14 empty objects each ran past the output limit in the pilot (Sydbank)
    spec.update({n: (Optional[FIELDS[n].cell], ...) for n in fields})
    return create_model("PayLine", **spec)


def answer_model(fields: list[str]) -> type[BaseModel]:
    """The answer of a by-field, by-role or all-fields call."""
    return create_model("PayLines",
                        fiscal_year=(Optional[str], ...),   # "2025", "2024/25"
                        period_end=(Optional[str], ...),    # YYYY-MM-DD
                        lines=(list[line_model(fields)], ...))


class GapCell(BaseModel):
    """One cell a gap-fill call was asked about."""
    line_ref: str                   # the reference given in the question
    field: str
    found: bool
    value: Optional[float]
    printed: Optional[str]
    unit_printed: Optional[str]
    unit: Optional[Unit]
    currency_printed: Optional[str]
    form: Optional[str]             # LTI form or target form, for those fields
    includes: Optional[str]
    quote: Optional[str]
    chunk_id: Optional[int]
    not_found_reason: Optional[str]


class GapAnswer(BaseModel):
    cells: list[GapCell]
