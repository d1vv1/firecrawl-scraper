"""Step 6: two LLM calls (financials, qualitative), then unit conversion in code."""

import datetime as dt
import logging
import re
from dataclasses import dataclass, field

from . import llm
from .schemas import (UNIT_MULTIPLIERS, FinancialsResult, MoneyFigure,
                      QualitativeResult)
from .sections import Chunk, is_statement_table

log = logging.getLogger(__name__)


@dataclass
class Extraction:
    financials: FinancialsResult
    qualitative: QualitativeResult
    financial_chunks: list[Chunk]
    qualitative_chunks: list[Chunk]
    # figures read from XBRL tags (no AI): target -> tag concept, e.g. "ifrs-full:Revenue"
    tagged: dict[str, str] = field(default_factory=dict)


def build_user_prompt(legal_name: str, source_url: str, chunks: list[Chunk],
                      statement_ids: list[int] | None = None) -> str:
    body = "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)
    hint = ""
    if statement_ids:
        hint = (f"Chunks that look like primary financial statement tables (group or "
                f"parent-company): {', '.join(map(str, statement_ids))}. Other chunks are "
                f"summaries, notes or narrative.\n\n")
    return (f"Company legal name: {legal_name}\n"
            f"Source URL: {source_url}\n\n"
            f"{hint}"
            f"The report may be written in Swedish, Norwegian, Danish, Finnish or another "
            f"language. Copy quotes EXACTLY in the report's own language (never translate a "
            f"quote); write descriptions in English. Native revenue labels include "
            f"Nettoomsättning, Intäkter, Driftsinntekter, Nettoomsætning, Omsætning, Liikevaihto; "
            f"total assets: Summa tillgångar, Sum eiendeler, Aktiver i alt, Vastaavaa yhteensä. "
            f"Native units: MSEK/Mkr/MNOK/mio. kr./milj. euroa = millions; TSEK/tkr/TNOK/"
            f"t.kr./tuhatta euroa = thousands; mdr/mrd = billions.\n"
            f"Each quote must be ONE continuous passage copied from a single chunk, "
            f"under 25 words, with no '...' joining separate passages.\n\n"
            f"Excerpts from the annual report (tables are in markdown):\n\n{body}")


_FIGURES = ("revenue", "total_assets", "total_equity_and_liabilities")


def tagged_figure(tag) -> MoneyFigure:
    """A MoneyFigure for a value read from an XBRL tag (full units, exact)."""
    return MoneyFigure(value=tag.value, unit="units", currency=tag.currency,
                       label_in_report=tag.concept.split(":", 1)[-1], scope="consolidated",
                       quote=f"{tag.concept} = {tag.value:,.0f} {tag.currency} ({tag.period})",
                       chunk_id=None, not_found_reason=None)


def extract(legal_name: str, source_url: str, financial_chunks: list[Chunk],
            qualitative_chunks: list[Chunk], tags: dict | None = None,
            period_end: str | None = None) -> Extraction:
    """Two LLM calls, except when `tags` (ESEF/XBRL figures) already give revenue,
    total assets and total equity and liabilities: then the financials call is
    skipped. Tagged values always win over values the AI read from the text."""
    tags = tags or {}
    if all(k in tags for k in _FIGURES):
        log.info("Financial figures all come from XBRL tags; skipping the financials LLM call")
        fin = FinancialsResult(fiscal_year=(period_end or "")[:4] or None,
                               period_end_date=period_end,
                               **{k: tagged_figure(tags[k]) for k in _FIGURES})
    else:
        log.info("LLM call 1/2: financials (%d chunks)", len(financial_chunks))
        fin = llm.call_llm(llm.load_prompt("financials_system"),
                           build_user_prompt(legal_name, source_url, financial_chunks,
                                             [c.id for c in financial_chunks
                                              if is_statement_table(c.text)]),
                           FinancialsResult)
        for k in _FIGURES:
            if k in tags:
                setattr(fin, k, tagged_figure(tags[k]))
        if tags and period_end:
            fin.fiscal_year, fin.period_end_date = period_end[:4], period_end
    log.info("LLM call 2/2: qualitative (%d chunks)", len(qualitative_chunks))
    qual = llm.call_llm(llm.load_prompt("qualitative_system"),
                        build_user_prompt(legal_name, source_url, qualitative_chunks),
                        QualitativeResult)
    return Extraction(fin, qual, financial_chunks, qualitative_chunks,
                      {k: tags[k].concept for k in _FIGURES if k in tags})


def full_value(value: float | None, unit: str | None) -> float | None:
    """value_full = value x multiplier(unit). None if either is missing."""
    if value is None or unit is None:
        return None
    return value * UNIT_MULTIPLIERS[unit]


def iso_period_end(raw: str | None, fiscal_year: str | None) -> str | None:
    """'2025-12-31' / '31 December 2025' / '31 December' (+ fiscal year 2025) -> '2025-12-31'.
    Returns None when the date can't be pinned down."""
    if not raw:
        return None
    text = re.sub(r"\s+", " ", raw.strip().rstrip("."))
    for fmt in ("%Y-%m-%d", "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    from .validate import latest_year   # local import: validate imports this module
    year = latest_year(fiscal_year)
    if year:
        for fmt in ("%d %B %Y", "%d %b %Y", "%B %d %Y"):
            try:
                return dt.datetime.strptime(f"{text.replace(',', '')} {year}", fmt).date().isoformat()
            except ValueError:
                pass
    return None


def money_with_full_value(fig: MoneyFigure) -> dict:
    d = fig.model_dump()
    d["value_full"] = full_value(fig.value, fig.unit)
    return d
