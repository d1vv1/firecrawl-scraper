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


class DataPointFacts(BaseModel):
    """Everything the report (or a web page) can tell beyond the core figures."""
    revenue: NumberFact
    total_assets: NumberFact
    fte: NumberFact                 # average full-time equivalents
    headcount: NumberFact           # employees at year end
    head_office_city: TextFact
    ticker: TextFact
    isin: TextFact
    exchange: TextFact
    exchange_segment: TextFact
    listing_date: TextFact
    is_listed: TextFact             # "listed" / "unlisted"
    sub_sector: TextFact
    reporting_currency: TextFact
    shares_outstanding: NumberFact
    controlling_owner: Holder       # name null if no one controls the company
    major_shareholders: list[Holder]   # holders of 5% or more
    revenue_by_country: CountryBreakdown
    staff_by_country: CountryBreakdown
    pension_type: TextFact
    shareholding_requirement: TextFact
