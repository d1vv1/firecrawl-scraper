"""Steps 5-7 on a real converted report (Unilever ARA 2025), with the LLM mocked.

The fake LLM only answers from chunks that were actually sent to it, so these
tests also prove that step 5 picked the chunks holding the real statements.
"""

import re
from pathlib import Path

import pytest

from extractor import extract as extract_mod
from extractor.schemas import (BusinessStructure, FinancialsResult, MoneyFigure,
                               QualitativeResult, RevenueModel)
from extractor.scraper import markdown_to_pages
from extractor.sections import is_toc, select_chunks, split_chunks
from extractor.validate import overall_status, run_checks

FIXTURE = Path(__file__).parent / "fixtures" / "unilever-ara-2025.md"
SOURCE_URL = "https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf"


@pytest.fixture(scope="module")
def chunks():
    pages = markdown_to_pages(FIXTURE.read_text(encoding="utf-8"))
    assert len(pages) > 200
    return split_chunks(pages)


def _sent_chunks(user_prompt: str) -> dict[int, str]:
    return {int(i): t for i, t in re.findall(r'<chunk id="(\d+)">\n(.*?)\n</chunk>',
                                             user_prompt, re.S)}


def _find(sent: dict[int, str], pattern: str) -> int | None:
    for cid, text in sent.items():
        if re.search(pattern, text, re.S):
            return cid
    return None


def _money(value, label, quote, cid):
    return MoneyFigure(value=value if cid is not None else None, unit="millions",
                       currency="EUR", label_in_report=label, scope="consolidated",
                       quote=quote if cid is not None else None, chunk_id=cid,
                       not_found_reason=None if cid is not None else "not in excerpts")


def fake_call_llm(system_prompt, user_prompt, schema):
    sent = _sent_chunks(user_prompt)
    if schema is FinancialsResult:
        rev = _find(sent, r"Turnover\**\|\**2\**\|\**50,503")
        ta = _find(sent, r"Total assets\**\|\|\**70,471")
        tle = _find(sent, r"Total liabilities and equity\**\|\|\**70,471")
        return FinancialsResult(
            fiscal_year="2025", period_end_date="2025-12-31",
            revenue=_money(50503, "Turnover", "Turnover 2 50,503", rev),
            total_assets=_money(70471, "Total assets", "Total assets 70,471", ta),
            total_equity_and_liabilities=_money(
                70471, "Total liabilities and equity", "Total liabilities and equity 70,471", tle))
    seg = _find(sent, r"Segment information")
    return QualitativeResult(
        revenue_model=RevenueModel(categories=["product_sales"], description="Sells consumer goods.",
                                   quote=None, chunk_id=None),
        business_structure=BusinessStructure(
            legal_form="PLC", is_listed=True, ultimate_parent=None,
            segments=["Beauty & Wellbeing", "Personal Care", "Home Care", "Foods"],
            description=None, quote="Segment information" if seg is not None else None,
            chunk_id=seg))


def test_chunks_have_pages_and_reasonable_size(chunks):
    assert len(chunks) > 50
    assert all(c.pages for c in chunks)
    assert max(c.words for c in chunks) < 2_500


def test_selection_respects_budget_and_skips_toc(chunks):
    for group in ("financials", "qualitative"):
        picked = select_chunks(chunks, group, word_budget=6_000)
        assert picked
        assert sum(c.words for c in picked) <= 6_000
        assert [c.id for c in picked] == sorted(c.id for c in picked)
        assert not any(is_toc(c.text) for c in picked)


def test_financial_statements_are_selected(chunks):
    pages = {p for c in select_chunks(chunks, "financials") for p in c.pages}
    assert 131 in pages, "consolidated income statement (p.131) not selected"
    assert 134 in pages, "consolidated balance sheet (p.134) not selected"


def test_qualitative_sections_are_selected(chunks):
    text = "\n".join(c.text for c in select_chunks(chunks, "qualitative")).lower()
    assert "segment information" in text
    assert "business model" in text
    assert "significant subsidiaries" in text


def test_steps_5_to_7_with_mocked_llm(chunks, monkeypatch):
    monkeypatch.setattr(extract_mod.llm, "call_llm", fake_call_llm)
    ex = extract_mod.extract("Unilever PLC", SOURCE_URL,
                             select_chunks(chunks, "financials"),
                             select_chunks(chunks, "qualitative"))
    assert ex.financials.revenue.value == 50503
    assert extract_mod.money_with_full_value(ex.financials.revenue)["value_full"] == 50_503_000_000

    checks = run_checks(ex)
    by_key = {(c.name, c.target): c.result for c in checks}
    for target in ("revenue", "total_assets", "total_equity_and_liabilities"):
        assert by_key[("quote", target)] == "pass"
        assert by_key[("value_in_quote", target)] == "pass"
    for target in ("revenue", "total_assets"):
        assert by_key[("scope", target)] == "pass"
        assert by_key[("sanity", target)] == "pass"
    assert by_key[("balance", "total_assets")] == "pass"
    assert by_key[("quote", "business_structure")] == "pass"
    assert overall_status(ex, checks) == "ok"


def test_hallucinated_quote_fails(chunks, monkeypatch):
    def lying_llm(system_prompt, user_prompt, schema):
        r = fake_call_llm(system_prompt, user_prompt, schema)
        if schema is FinancialsResult:
            r.revenue.quote = "Turnover 2 60,073"
            r.revenue.value = 60073
        return r
    monkeypatch.setattr(extract_mod.llm, "call_llm", lying_llm)
    ex = extract_mod.extract("Unilever PLC", SOURCE_URL, select_chunks(chunks, "financials"),
                             select_chunks(chunks, "qualitative"))
    checks = run_checks(ex)
    assert any(c.name == "quote" and c.target == "revenue" and c.result == "fail" for c in checks)
    assert overall_status(ex, checks) == "needs_review"
