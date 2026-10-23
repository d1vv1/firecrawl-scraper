"""Pydantic models. The LLM-facing models are exactly as specified; don't add
defaults to them (structured outputs in strict mode needs every field)."""

from typing import Literal, Optional

from pydantic import BaseModel

Unit = Literal["units", "thousands", "millions", "billions", "lakhs", "crores"]
Scope = Literal["consolidated", "parent_only", "unclear"]

UNIT_MULTIPLIERS: dict[str, int] = {
    "units": 1,
    "thousands": 1_000,
    "millions": 1_000_000,
    "billions": 1_000_000_000,
    "lakhs": 100_000,        # Indian numbering: 1 lakh = 100,000
    "crores": 10_000_000,    # 1 crore = 10 million
}


class MoneyFigure(BaseModel):
    value: Optional[float]          # number exactly as printed in the table
    unit: Optional[Unit]            # from the table header, e.g. "€ million"
    currency: Optional[str]         # ISO 4217, e.g. "EUR"
    label_in_report: Optional[str]  # e.g. "Turnover", "Net sales"
    scope: Scope
    quote: Optional[str]            # short exact text from the source
    chunk_id: Optional[int]
    not_found_reason: Optional[str]


class FinancialsResult(BaseModel):
    fiscal_year: Optional[str]      # e.g. "2025" or "2024/25"
    period_end_date: Optional[str]  # YYYY-MM-DD if stated
    revenue: MoneyFigure
    total_assets: MoneyFigure
    total_equity_and_liabilities: MoneyFigure  # for cross-checking only


RevenueCategory = Literal[
    "product_sales", "subscription", "services", "licensing_royalties",
    "commission_marketplace", "advertising", "interest_income", "other"]


class RevenueModel(BaseModel):
    categories: list[RevenueCategory]   # main ones first
    description: Optional[str]          # 1–2 plain sentences
    quote: Optional[str]
    chunk_id: Optional[int]


class BusinessStructure(BaseModel):
    legal_form: Optional[str]           # e.g. "plc", "SE", "AG"
    is_listed: Optional[bool]
    ultimate_parent: Optional[str]      # null if the company is the top parent
    segments: list[str]                 # reported segments / business groups
    description: Optional[str]          # 1–2 plain sentences
    quote: Optional[str]
    chunk_id: Optional[int]


class QualitativeResult(BaseModel):
    revenue_model: RevenueModel
    business_structure: BusinessStructure


# --- data points (python -m extractor.datapoints) ----------------------------------

class TextFact(BaseModel):
    value: Optional[str]
    quote: Optional[str]            # short exact text from the source
    chunk_id: Optional[int]


class NumberFact(BaseModel):
    value: Optional[float]          # exactly as printed
    unit: Optional[Unit]            # for money; "units" for counts
    currency: Optional[str]         # ISO 4217 for money, else null
    period_end: Optional[str]       # YYYY-MM-DD the figure relates to, if stated
    quote: Optional[str]
    chunk_id: Optional[int]


HolderType = Literal[
    "private_equity", "family_or_individual", "state", "listed_company", "other_company",
    "foundation", "institutional_investor", "employees", "other"]


class Holder(BaseModel):
    name: Optional[str]
    holder_type: Optional[HolderType]
    stake_pct: Optional[float]      # share of capital or votes, in percent
    quote: Optional[str]
    chunk_id: Optional[int]


class CountryValue(BaseModel):
    country: str                    # country or region as written
    value: float                    # as printed


class CountryBreakdown(BaseModel):
    items: list[CountryValue]
    unit: Optional[Unit]
    currency: Optional[str]         # null for staff numbers
    basis: Optional[str]            # e.g. "by customer location", "average FTE"
    quote: Optional[str]
    chunk_id: Optional[int]


class SegmentValue(BaseModel):
    segment: str                    # reportable segment as written
    value: float                    # as printed


class SegmentBreakdown(BaseModel):
    items: list[SegmentValue]
    unit: Optional[Unit]
    currency: Optional[str]         # null for staff numbers
    basis: Optional[str]            # e.g. "external revenue", "FTE at year end"
    quote: Optional[str]
    chunk_id: Optional[int]


ProfitMeasure = Literal["ebitda", "adjusted_ebitda", "operating_profit"]


class ProfitFact(BaseModel):
    value: Optional[float]          # exactly as printed
    unit: Optional[Unit]
    currency: Optional[str]
    measure: Optional[ProfitMeasure]   # operating_profit only when EBITDA isn't reported
    company_defined: Optional[bool]    # an alternative performance measure (not IFRS)
    label_in_report: Optional[str]
    quote: Optional[str]
    chunk_id: Optional[int]


class PriceFact(BaseModel):
    value: Optional[float]          # closing share price at fiscal year end, as printed
    currency: Optional[str]
    date: Optional[str]             # YYYY-MM-DD of the price, if stated
    quote: Optional[str]
    chunk_id: Optional[int]


class DataPointFacts(BaseModel):
    """Everything the report (or a web page) can tell beyond the core figures."""
    revenue: NumberFact
    total_assets: NumberFact
    ebitda: ProfitFact
    fte: NumberFact                 # average full-time equivalents
    headcount: NumberFact           # employees at year end
    legal_name: TextFact
    business_id: TextFact           # national register number
    country_code: TextFact          # ISO 3166 alpha-2 of the registered office
    other_names: TextFact           # former names
    ultimate_parent: TextFact       # top company of the group, if a subsidiary
    head_office_city: TextFact
    website: TextFact               # the company's own website domain
    ticker: TextFact
    isin: TextFact
    exchange: TextFact
    exchange_segment: TextFact
    listing_date: TextFact
    is_listed: TextFact             # "listed" / "unlisted"
    sub_sector: TextFact
    fiscal_year_end: TextFact       # YYYY-MM-DD
    reporting_currency: TextFact
    accounting_basis: TextFact      # e.g. "IFRS as adopted by the EU", "HGB"
    shares_outstanding: NumberFact
    share_price: PriceFact
    controlling_owner: Holder       # 20%+ of votes; name null if no one has that
    major_shareholders: list[Holder]   # the largest holders listed, with stakes
    revenue_by_country: CountryBreakdown
    staff_by_country: CountryBreakdown
    revenue_by_segment: SegmentBreakdown
    staff_by_segment: SegmentBreakdown
    pension_type: TextFact
    benefits: TextFact              # company-level executive benefits
    shareholding_requirement: TextFact


# --- executive pay, role grain (python -m extractor.datapoints) --------------------

# What an LTI figure is made of: cash paid, shares or options, or a number of instruments.
LtiForm = Literal["cash", "shares", "options", "number_of_instruments", "accounting_expense",
                  "other"]
# How a target or maximum is stated (HANDOVER decision: keep the stated form).
TargetForm = Literal["pct_of_base", "pct_of_max", "months_of_salary", "amount",
                     "number_of_shares", "other"]


class PayAmount(BaseModel):
    value: Optional[float]          # exactly as printed
    unit: Optional[Unit]            # from the table header ("in T€" -> thousands)
    currency: Optional[str]
    includes: Optional[str]         # other components bundled in, e.g. "social security"
    quote: Optional[str]
    chunk_id: Optional[int]


class LtiAmount(BaseModel):
    value: Optional[float]          # exactly as printed
    unit: Optional[Unit]
    currency: Optional[str]         # null for a number of instruments
    form: Optional[LtiForm]
    includes: Optional[str]
    quote: Optional[str]
    chunk_id: Optional[int]


class PayTarget(BaseModel):
    value: Optional[float]          # as stated: 60 (% of base), 50 (% of max), 6 (months)
    form: Optional[TargetForm]
    currency: Optional[str]         # for an amount only
    unit: Optional[Unit]            # for an amount only
    quote: Optional[str]
    chunk_id: Optional[int]


class RoleHeadcount(BaseModel):
    value: Optional[float]          # people in an aggregate row
    excludes: Optional[str]         # who is left out, e.g. "the CEO"
    quote: Optional[str]
    chunk_id: Optional[int]


class RolePay(BaseModel):
    role_title: str                 # as stated: "CEO", "Other members of group management"
    person_name: Optional[str]      # only to tell rows with the same title apart
    executive: bool                 # false: non-executive board member(s)
    is_aggregate: bool              # one row for several people
    quote: Optional[str]            # where the role is disclosed
    chunk_id: Optional[int]
    aggregate_headcount: RoleHeadcount
    base_salary: PayAmount
    sti_paid: PayAmount             # short-term incentive / bonus for the year
    lti_vested: LtiAmount           # vested, paid out or exercised for the year
    lti_granted: LtiAmount          # granted (awarded) in the year
    benefits: PayAmount
    pension: PayAmount
    pension_allowance: PayAmount    # salary addition paid instead of pension (Norway)
    total: PayAmount                # as stated by the company
    sti_target: PayTarget
    sti_max: PayTarget
    lti_target: PayTarget
    lti_max: PayTarget


class RemunerationFacts(BaseModel):
    """A remuneration report or policy: pay per executive role, plus company-level terms."""
    fiscal_year: Optional[str]
    roles: list[RolePay]
    pension_type: TextFact
    benefits: TextFact
    shareholding_requirement: TextFact
