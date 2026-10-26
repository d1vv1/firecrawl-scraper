"""ESEF/XBRL tag reading and the text converter (no network)."""

import datetime as dt

from extractor import esef
from extractor.extract import extract
from extractor.esef import EsefFiling, TaggedFigure, annual_figures, is_recent, report_language
from extractor.xhtml_text import html_to_text, text_to_pages


def _fact(concept, value, period, unit="iso4217:DKK", **dims):
    return {"value": str(value), "dimensions": {"concept": concept, "entity": "scheme:LEI",
                                                "period": period, "unit": unit, **dims}}


ANNUAL = {
    "a": _fact("ifrs-full:Revenue", 6243956000, "2025-01-01T00:00:00/2026-01-01T00:00:00"),
    "b": _fact("ifrs-full:Revenue", 5716206000, "2024-01-01T00:00:00/2025-01-01T00:00:00"),
    "c": _fact("ifrs-full:Assets", 14954537000, "2026-01-01T00:00:00"),
    "d": _fact("ifrs-full:EquityAndLiabilities", 14954537000, "2026-01-01T00:00:00"),
    # a segment breakdown must not be taken as the total
    "e": _fact("ifrs-full:Revenue", 3105000000, "2025-01-01T00:00:00/2026-01-01T00:00:00",
               **{"ifrs-full:SegmentsAxis": "bava:PublicPreparednessMember"}),
}


def test_annual_figures_current_year_and_no_breakdowns():
    figs = annual_figures(ANNUAL, "2025-12-31")
    assert figs["revenue"].value == 6243956000 and figs["revenue"].currency == "DKK"
    assert figs["revenue"].period == "2025-01-01/2025-12-31"
    assert figs["total_assets"].value == 14954537000
    assert figs["total_equity_and_liabilities"].value == 14954537000


def test_half_year_filing_is_not_annual():
    h1 = {"a": _fact("ifrs-full:Revenue", 3000000000, "2026-01-01T00:00:00/2026-07-01T00:00:00"),
          "c": _fact("ifrs-full:Assets", 14723000000, "2026-07-01T00:00:00")}
    assert annual_figures(h1, "2026-06-30") == {}


def test_revenue_concept_alternatives():
    facts = {"a": _fact("ifrs-full:RevenueFromContractsWithCustomers", 19889000000,
                        "2025-01-01T00:00:00/2026-01-01T00:00:00", unit="iso4217:EUR")}
    assert annual_figures(facts, "2025-12-31")["revenue"].concept == "ifrs-full:RevenueFromContractsWithCustomers"


def test_report_language_and_recency():
    assert report_language("/x/bava-2025-12-31-en/reports/bava-2025-12-31-en.xhtml") == "en"
    assert report_language("/x/549300A0JPRWG1KI7U06-2025-12-31-1-fi.json") == "fi"
    f = EsefFiling("L", "id", "2025-12-31", "DK", "u", None, None)
    assert is_recent(f, dt.date(2026, 10, 16))
    assert not is_recent(EsefFiling("L", "id", "2024-12-31", "SE", "u", None, None), dt.date(2026, 10, 16))


def test_all_tagged_skips_the_financials_llm_call(monkeypatch):
    from extractor import extract as extract_mod
    from extractor.schemas import BusinessStructure, QualitativeResult, RevenueModel
    calls = []

    def fake_llm(system, user, schema):
        calls.append(schema.__name__)
        return QualitativeResult(
            revenue_model=RevenueModel(categories=[], description=None, quote=None, chunk_id=None),
            business_structure=BusinessStructure(legal_form=None, is_listed=None, ultimate_parent=None,
                                                 segments=[], description=None, quote=None, chunk_id=None))
    monkeypatch.setattr(extract_mod.llm, "call_llm", fake_llm)
    tags = annual_figures(ANNUAL, "2025-12-31")
    ex = extract("Bavarian Nordic A/S", "u", [], [], tags=tags, period_end="2025-12-31")
    assert calls == ["QualitativeResult"]
    assert ex.financials.revenue.value == 6243956000 and ex.financials.fiscal_year == "2025"
    assert ex.tagged["revenue"] == "ifrs-full:Revenue"
    from extractor.validate import run_checks
    checks = {(c.name, c.target): c for c in run_checks(ex)}
    assert checks[("quote", "revenue")].result == "pass"
    assert "XBRL tag" in checks[("quote", "revenue")].detail
    assert checks[("balance", "total_assets")].result == "pass"


def test_html_to_text_joins_word_boxes_and_keeps_table_rows():
    html = ("<html><body><div><span>Revenue</span></div><div><span>for the year was</span></div>"
            "<div><span>DKK 6,244 million.</span></div>"
            "<table><tr><td><p>Total assets</p></td><td>14,954,537</td><td>14,405,864</td></tr></table>"
            "<img src=\"data:image/png;base64,AAAA\"/></body></html>")
    text = html_to_text(html)
    assert "Revenue for the year was DKK 6,244 million." in text
    assert "| Total assets | 14,954,537 | 14,405,864 |" in text
    assert "base64" not in text
    pages = text_to_pages("\n".join(["word " * 100] * 10), words_per_page=450)
    assert [p.number for p in pages] == [1, 2]          # 500 + 500 words, split at paragraph ends


def _setup_routes(monkeypatch, tmp_path, filing, website_year=None, website_fails=False):
    """Fake GLEIF/ESEF/website/LLM so only the route choice in pipeline.run is tested."""
    from extractor import pipeline
    from extractor.report_finder import ReportNotFoundError
    from extractor.scraper import Page, ReportDocument
    monkeypatch.setattr(pipeline, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pipeline, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(pipeline, "identify_lei", lambda *a, **k: {
        "record": {"lei": "L", "legal_name": "ACME AB", "country": "SE"}, "reason": "given"})
    monkeypatch.setattr(pipeline, "get_esef", lambda *a, **k: filing)
    monkeypatch.setattr(pipeline, "get_edgar", lambda *a, **k: None)
    used = {}

    def fake_discover(*a, **k):
        if website_fails:
            raise ReportNotFoundError("nothing on the website")
        return {"website": "https://acme.se", "website_source": "wikidata",
                "report_url": "https://acme.se/ar.pdf", "report_year": website_year}
    monkeypatch.setattr(pipeline, "discover", fake_discover)
    pages = [Page(1, "ACME AB annual report " * 50)]
    monkeypatch.setattr(pipeline, "_fetch_first_usable", lambda urls, *a: used.setdefault(
        "doc", ReportDocument(urls[0], "pdf", pages, tmp_path / "w.md", None, True)))
    monkeypatch.setattr(pipeline, "_esef_doc_or_none", lambda f, *a: used.setdefault(
        "doc", ReportDocument(f.report_url, "xhtml", pages, tmp_path / "e.md", None, True)))

    def fake_extract(name, url, fin, qual, tags=None, period_end=None, qualitative=True):
        used["tags"] = tags
        return _ex_with(tags, period_end)
    monkeypatch.setattr(pipeline, "extract", fake_extract)
    monkeypatch.setattr(pipeline.llm, "model_name", lambda: "test")
    return pipeline, used


def _ex_with(tags, period_end):
    from extractor.extract import Extraction, tagged_figure
    from extractor.schemas import (BusinessStructure, FinancialsResult, MoneyFigure,
                                   QualitativeResult, RevenueModel)
    empty = MoneyFigure(value=None, unit=None, currency=None, label_in_report=None,
                        scope="unclear", quote=None, chunk_id=None, not_found_reason="x")
    figs = {k: tagged_figure(tags[k]) if tags and k in tags else empty
            for k in ("revenue", "total_assets", "total_equity_and_liabilities")}
    fin = FinancialsResult(fiscal_year=(period_end or "2025")[:4], period_end_date=period_end, **figs)
    qual = QualitativeResult(
        revenue_model=RevenueModel(categories=[], description=None, quote=None, chunk_id=None),
        business_structure=BusinessStructure(legal_form=None, is_listed=None, ultimate_parent=None,
                                             segments=[], description=None, quote=None, chunk_id=None))
    return Extraction(fin, qual, [], [], {k: v.concept for k, v in (tags or {}).items()})


def _filing(fy):
    return EsefFiling("L", "id", f"{fy}-12-31", "SE", f"https://filings/{fy}.xhtml", None, None,
                      annual_figures(ANNUAL, "2025-12-31") if fy == 2025 else
                      {"total_assets": TaggedFigure(1.0, "SEK", "ifrs-full:Assets", f"{fy}-12-31")},
                      language="en")


def test_older_filing_used_when_website_fails(monkeypatch, tmp_path):
    pipeline, used = _setup_routes(monkeypatch, tmp_path, _filing(2024), website_fails=True)
    r = pipeline.run("ACME AB", company_id="acme")
    assert r["data_source"] == "esef" and used["tags"] is not None


def test_older_filing_beats_an_even_older_website_report(monkeypatch, tmp_path):
    pipeline, used = _setup_routes(monkeypatch, tmp_path, _filing(2024), website_year=2022)
    r = pipeline.run("ACME AB", company_id="acme")
    assert r["data_source"] == "esef"


def test_newer_website_report_beats_older_filing(monkeypatch, tmp_path):
    pipeline, used = _setup_routes(monkeypatch, tmp_path, _filing(2024), website_year=2025)
    r = pipeline.run("ACME AB", company_id="acme")
    assert r["data_source"] == "website" and used["tags"] is None


def test_recent_foreign_language_filing_beats_an_older_english_website_report(monkeypatch, tmp_path):
    # Rosenbauer: FY2025 filing in German; the website's English PDF was FY2024.
    filing = _filing(2025)
    filing.language = "de"
    pipeline, used = _setup_routes(monkeypatch, tmp_path, filing, website_year=2024)
    r = pipeline.run("ACME AB", company_id="acme")
    assert r["data_source"] == "esef" and r["report_url"] == "https://filings/2025.xhtml"


def test_same_year_english_website_report_reads_next_to_a_foreign_filing(monkeypatch, tmp_path):
    filing = _filing(2025)
    filing.language = "de"
    pipeline, used = _setup_routes(monkeypatch, tmp_path, filing, website_year=2025)
    r = pipeline.run("ACME AB", company_id="acme")
    assert r["report_url"] == "https://acme.se/ar.pdf" and used["tags"] is not None
