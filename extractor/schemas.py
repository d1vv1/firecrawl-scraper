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
