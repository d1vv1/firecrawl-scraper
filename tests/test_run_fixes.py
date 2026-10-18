"""Regression tests for problems seen in the first 96-company Nordic batch run."""

import datetime as dt

import pytest

from extractor import report_finder as rf
from extractor.extract import full_value
from extractor.firecrawl_client import CreditBudgetExceeded, FirecrawlClient
from extractor.config import Settings
from extractor.schemas import (BusinessStructure, FinancialsResult, MoneyFigure,
                               QualitativeResult, RevenueModel)
from extractor.sections import FINANCIALS, QUALITATIVE, is_statement_table, score_chunk
from extractor.validate import Check, check_entity, overall_status, warnings_for
from extractor.extract import Extraction

THIS_YEAR = dt.date.today().year


# --- report finder: pages that are not reports -------------------------------------

@pytest.mark.parametrize("url", [
    "https://www.akerasa.com/investors/financial-calendar/module-holder/calendar-v2/2026%20annual%20report.ics",
    "https://www.almbrand.dk/english/nyheder-og-events/begivenheder/detaljer-for-begivenhed/2026/Annual-report-2025/default.aspx",
    "https://corporate.al.se/en/investor-relations/calendar/2027/annual-report-2026",
    "https://investor.bang-olufsen.com/events/event-details/annual-report-202627",
    "https://bwoffshore.com/media/bw-offshore-publishes-2025-annual-report-and-sustainability-statement",
    "https://corporate.asmodee.com/pressreleases/asmodee-publishes-annual-and-sustainability-report-for-2425",
    "https://www.bakkafrost.com/fo/um-okkum/tidindi/bakkafrost-presents-2022-annual-and-sustainability-report",
    "https://x.com/en/wp-content/uploads/2025/06/momentum-group-publishes-annual-report-201819-190626.pdf",
    "https://www.arionbanki.is/investors/Structured-Covered-Bonds/annual-report-2015.pdf",
])
def test_non_report_pages_are_excluded(url):
    assert not rf.classify(url).kept


def test_subsidiary_report_named_after_another_country_is_excluded():
    allowed = rf.allowed_place_words("ABB Ltd", ["SE", "CH"])
    india = ("https://library.e.abb.com/public/93c9/ABB%20India%20Limited%20Integrated%20"
             "Annual%20Report%202025.pdf")
    group = "https://library.e.abb.com/public/3fe5/ABB-Group-Annual-Report-2025-English.pdf"
    assert not rf.classify(india, allowed).kept
    assert rf.classify(group, allowed).kept
    # a country word that is part of the company's own name is fine
    own = rf.allowed_place_words("Norwegian Air Shuttle ASA", ["NO"])
    assert rf.classify("https://x.no/norwegian-annual-report-2025.pdf", own).kept
    assert rf.classify("https://x.se/sweden/annual-report-2025.pdf",
                       rf.allowed_place_words("Acme AB", ["SE"])).kept


# --- report finder: freshness, IR page, credit cap -----------------------------------

class FakeFC:
    """map/scrape responses by call order; records calls; optional credit cap."""

    def __init__(self, maps, scrape_links=(), cap=None):
        self.maps, self.scrape_links, self.calls = list(maps), list(scrape_links), []
        self.spent, self.cap = 0, cap

    def _pay(self, kind):
        if self.cap is not None and self.spent + 1 > self.cap:
            raise CreditBudgetExceeded(f"cap {self.cap}")
        self.spent += 1
        self.calls.append(kind)

    def map(self, url, search, limit):
        self._pay(f"map:{search}")
        return [{"url": u} for u in (self.maps.pop(0) if self.maps else [])]

    def scrape(self, url, formats):
        self._pay(f"scrape:{url}")
        return {"markdown": "", "links": list(self.scrape_links)}


def test_stale_pdf_triggers_ir_page_scrape_which_finds_current_report():
    fc = FakeFC(maps=[["https://aak.com/investors/annual-report-2021.pdf",
                       "https://aak.com/investors/reports-and-presentations/"]],
                scrape_links=[f"https://storage.mfn.se/abc/aak-annual-report-{THIS_YEAR - 1}.pdf"])
    r = rf.find_report("https://aak.com", fc, country="SE", company_name="AAK AB")
    assert r.url.endswith(f"aak-annual-report-{THIS_YEAR - 1}.pdf")
    assert fc.calls[:2] == ["map:annual report", "scrape:https://aak.com/investors/reports-and-presentations/"]


def test_fresh_pdf_stops_after_one_map():
    fc = FakeFC(maps=[[f"https://x.se/annual-report-{THIS_YEAR - 1}.pdf"]])
    rf.find_report("https://x.se", fc, country="SE", company_name="X AB")
    assert fc.calls == ["map:annual report"]


def test_only_ancient_reports_is_not_found():
    fc = FakeFC(maps=[["https://x.com/annual_report_2012_eng.pdf"]] * 5)
    with pytest.raises(rf.ReportNotFoundError, match="Only old reports"):
        rf.find_report("https://x.com", fc, company_name="X Inc")


def test_listing_page_is_never_the_report():
    fc = FakeFC(maps=[["https://ir.bts.com/financial-information/annual-reports"]] * 5)
    with pytest.raises(rf.ReportNotFoundError, match="listing page"):
        rf.find_report("https://ir.bts.com", fc, company_name="BTS Group AB")


def test_credit_cap_stops_search_and_uses_best_so_far():
    fc = FakeFC(maps=[[f"https://x.se/annual-report-{THIS_YEAR - 2}.pdf"]] * 5, cap=2)
    r = rf.find_report("https://x.se", fc, country="SE", company_name="X AB")
    assert r.year == THIS_YEAR - 2 and fc.spent == 2


def test_firecrawl_client_enforces_cap_before_spending():
    fc = FirecrawlClient(Settings("k", None, None, None), max_credits=1)
    fc.credits.add("map", "x", 1)
    with pytest.raises(CreditBudgetExceeded):
        fc.map("https://x.com", search="annual report", limit=10)


# --- units ---------------------------------------------------------------------------

def test_indian_units():
    assert full_value(13202.73, "crores") == pytest.approx(132_027_300_000)
    assert full_value(5, "lakhs") == 500_000


# --- entity check --------------------------------------------------------------------

def test_entity_check_catches_subsidiary_currency():
    front = "ABB India Limited Integrated Annual Report 2025. Registered office Bengaluru."
    checks = {c.target: c.result for c in check_entity("ABB Ltd", "ABB Ltd", ["SE", "CH"], "INR", front)}
    assert checks == {"company_name": "pass", "currency": "fail"}


def test_entity_check_name_and_currency_pass():
    front = "A.P. Møller - Mærsk A/S Annual Report 2025 ... USD million"
    checks = check_entity("AP Moller - Maersk A/S", None, ["DK"], "USD", front)
    assert [c.result for c in checks] == ["pass", "pass"]
    checks = check_entity("Volvo AB", "Aktiebolaget Volvo", ["SE"], "SEK", "AB Volvo (publ) annual")
    assert [c.result for c in checks] == ["pass", "pass"]


def test_entity_check_wrong_company_name():
    checks = check_entity("Axactor ASA", "AXACTOR ASA", ["NO"], "NOK", "Årsregnskap 2022 Hoist Capital AS")
    assert checks[0].result == "fail"


# --- decision B: descriptive quotes only warn --------------------------------------

def _ex():
    fig = MoneyFigure(value=1.0, unit="millions", currency="EUR", label_in_report="x",
                      scope="consolidated", quote=None, chunk_id=None, not_found_reason=None)
    fin = FinancialsResult(fiscal_year="2025", period_end_date=None, revenue=fig, total_assets=fig,
                           total_equity_and_liabilities=fig)
    qual = QualitativeResult(
        revenue_model=RevenueModel(categories=[], description=None, quote=None, chunk_id=None),
        business_structure=BusinessStructure(legal_form=None, is_listed=None, ultimate_parent=None,
                                             segments=[], description=None, quote=None, chunk_id=None))
    return Extraction(fin, qual, [], [])


def test_descriptive_quote_failure_is_a_warning_not_a_status():
    checks = [Check("quote", "revenue", "pass"),
              Check("quote", "revenue_model", "fail", "quote not found")]
    assert overall_status(_ex(), checks) == "ok"
    assert warnings_for(checks) == ["revenue_model: quote not found"]
    checks.append(Check("entity", "currency", "fail", "INR"))
    assert overall_status(_ex(), checks) == "needs_review"


# --- decision A: Nordic-language sections ------------------------------------------

SWEDISH_IS = "## Koncernens resultaträkning\n|Mkr|Not|2025|2024|\n|---|---|---|---|\n" + "".join(
    f"|Nettoomsättning|3|{1000 + i},5|{900 + i},1|\n" for i in range(12))


def test_nordic_statement_detected_and_scored():
    assert is_statement_table(SWEDISH_IS)
    assert score_chunk(SWEDISH_IS, FINANCIALS, True) > 50


def test_nordic_keywords_match_without_accents():
    assert score_chunk("Nettoomsaetning steg och omsaetning okade.", FINANCIALS, False) > 0
    assert score_chunk("Vår affärsmodell och våra rörelsesegment", QUALITATIVE, False) > 0
    assert score_chunk("Konsernin liikevaihto kasvoi.", FINANCIALS, False) > 0


def test_fresh_html_report_beats_stale_pdf_but_fresh_pdf_beats_html():
    stale_pdf = rf.classify("https://www.aak.com/siteassets/investors/aak-annual-report-2021.pdf")
    fresh_html = rf.classify(f"https://reports.aak.com/reports/Annual_Report_{THIS_YEAR - 1}")
    assert rf.pick_best([stale_pdf, fresh_html]) is fresh_html
    fresh_pdf = rf.classify(f"https://www.aak.com/aak-annual-report-{THIS_YEAR - 1}.pdf")
    assert rf.pick_best([stale_pdf, fresh_html, fresh_pdf]) is fresh_pdf


def test_ir_page_prefers_listing_parent_over_old_report_page():
    cands = [rf.classify("https://reports.aak.com/reports/Annual_Report_2021")]
    page = rf._pick_ir_page(cands, [], "https://www.aak.com")
    assert page == "https://reports.aak.com/reports/"
    urls = ["https://www.addnodegroup.com/release/addnode-groups-annual-report-2022-published",
            "https://www.addnodegroup.com/investors/reports/"]
    assert rf._pick_ir_page([], urls, "https://www.addnodegroup.com") == urls[1]


def test_alternatives_are_kept_for_fallback():
    fc = FakeFC(maps=[[f"https://x.se/annual-report-{THIS_YEAR - 1}.pdf",
                       f"https://x.se/annual-report-{THIS_YEAR - 2}.pdf",
                       "https://x.se/annual-report-2012.pdf"]])
    r = rf.find_report("https://x.se", fc, country="SE", company_name="X AB")
    assert r.alternatives == [f"https://x.se/annual-report-{THIS_YEAR - 2}.pdf"]   # 2012 too old


def test_unusable_report_falls_back_to_next_candidate(monkeypatch):
    from extractor import pipeline
    from extractor.scraper import NeedsOCRError
    tried = []

    def fake_fetch(url, slug, fc, use_cache):
        tried.append(url)
        if url.endswith("placeholder.pdf"):
            raise NeedsOCRError("0 characters per page")
        return "doc"
    monkeypatch.setattr(pipeline, "fetch_report", fake_fetch)
    assert pipeline._fetch_first_usable(["https://x/placeholder.pdf", "https://x/real.pdf"],
                                        "x", None, True) == "doc"
    assert tried == ["https://x/placeholder.pdf", "https://x/real.pdf"]


def test_presentation_in_folder_name_is_fine_but_not_in_file_name():
    assert rf.classify("https://www.akerasa.com/investors/report-and-presentations/annual-report-2025").kept
    assert not rf.classify("https://x.com/investors/annual-report-2025-presentation.pdf").kept


def test_entity_check_short_names_with_double_letters():
    checks = check_entity("AAK AB", "AAK AB (publ)", ["SE"], "SEK", "AAK Annual Report 2025")
    assert [c.result for c in checks] == ["pass", "pass"]


def test_search_keeps_one_credit_to_fetch_the_report():
    from extractor.firecrawl_client import CreditMeter

    class MeteredFC(FakeFC):
        def __init__(self, *a, cap, **k):
            super().__init__(*a, **k)
            self.max_credits, self.credits = cap, CreditMeter()

        def _pay(self, kind):
            super()._pay(kind)
            self.credits.add(kind, "x", 1)

    fc = MeteredFC(maps=[[f"https://x.se/annual-report-{THIS_YEAR - 2}.pdf"]] * 5, cap=4)
    rf.find_report("https://x.se", fc, country="SE", company_name="X AB")
    assert fc.credits.total == 3          # 4 cap - 1 kept for fetching the report


def test_ir_page_ignores_domain_and_calendar_downloads():
    cands = [rf.classify("https://investor.firstsolar.com/financials/annual-reports/default.aspx")]
    urls = ["https://investor.firstsolar.com/DownloadICal.aspx",
            "https://investor.firstsolar.com/overview/default.aspx",
            "https://investor.firstsolar.com/financials/annual-reports/default.aspx"]
    assert rf._pick_ir_page(cands, urls, "https://www.firstsolar.com") == \
        "https://investor.firstsolar.com/financials/annual-reports/default.aspx"


def test_link_text_rescues_meaningless_pdf_names():
    md = ("[2025 Annual Report](https://s202.q4cdn.com/499595574/files/doc_financials/2026/ar/8769e063.pdf) "
          "[Q2 Earnings Presentation](https://s202.q4cdn.com/499595574/files/doc_financials/2026/q2/abc.pdf)")
    fc = FakeFC(maps=[["https://investor.firstsolar.com/financials/annual-reports/default.aspx"]],
                scrape_links=["https://s202.q4cdn.com/499595574/files/doc_financials/2026/ar/8769e063.pdf",
                              "https://s202.q4cdn.com/499595574/files/doc_financials/2026/q2/abc.pdf"])
    fc.scrape = lambda url, formats: (fc._pay("scrape:" + url) or
                                      {"markdown": md, "links": list(fc.scrape_links)})
    r = rf.find_report("https://www.firstsolar.com", fc, country="US", company_name="First Solar, Inc.")
    assert r.url.endswith("8769e063.pdf") and r.year == 2025


def test_10k_is_kept_but_below_an_annual_report():
    assert rf.classify("https://x.com/files/2025-form-10-k.pdf").kept
    best = rf.pick_best([rf.classify("https://x.com/novo-nordisk-form-20-f-2025.pdf"),
                         rf.classify("https://x.com/novo-nordisk-annual-report-2025.pdf")])
    assert best.url.endswith("annual-report-2025.pdf")


# --- retry-run fixes (Oct 2026) ---------------------------------------------------

def test_sec_title_drops_state_suffix():
    from extractor.edgar import sec_title
    from extractor.lei import match_level
    assert sec_title("APPLIED MATERIALS INC /DE") == "APPLIED MATERIALS INC"
    assert sec_title("ORACLE CORP /DE/") == "ORACLE CORP"
    assert match_level("Applied Materials, Inc.", sec_title("APPLIED MATERIALS INC /DE")) == "exact"


def test_report_announcement_pages_are_excluded():
    from extractor.report_finder import classify
    for url in ["https://www.hacksawgaming.com/sv/hacksaw-publicerar-arsredovisning-2025",
                "https://allgon.se/annual-report-2025-now-available",
                "https://accentro.de/aktuelles/accentro-gibt-verschiebung-bekannt"]:
        assert not classify(url).kept, url


def test_teaser_page_links_are_followed():
    from extractor.report_finder import reports_linked_from
    md = ("[Download](/files/x8f3a.pdf) [Governance](https://a.com/cg-2025.pdf) "
          "[Annual Report 2025](https://a.com/q/ab12.pdf)")
    assert reports_linked_from(md, "https://a.com/news/x") == ["https://a.com/q/ab12.pdf"]
    # one PDF on a page about the report: that's the report
    assert reports_linked_from("[Download](/f/abc.pdf)", "https://a.com/x") == ["https://a.com/f/abc.pdf"]
    assert reports_linked_from("[A](/a.pdf) [B](/b.pdf)", "https://a.com/x") == []


def test_llm_rate_limit_waits_at_least_the_floor():
    from types import SimpleNamespace
    import httpx
    import openai
    from extractor import llm
    resp = httpx.Response(429, headers={"retry-after": "1"},
                          request=httpx.Request("POST", "https://x"))
    exc = openai.RateLimitError("429", response=resp, body=None)
    state = SimpleNamespace(outcome=SimpleNamespace(exception=lambda: exc), attempt_number=2)
    assert llm._wait(state) == 2 * llm.RATE_LIMIT_MIN_WAIT_S


def test_inline_xbrl_header_is_dropped():
    from extractor.xhtml_text import html_to_text
    html = ('<html><body><div style="display:none"><ix:header><ix:hidden>FALSE2025FY'
            '</ix:hidden><ix:resources>us-gaap:RevenuesMember</ix:resources></ix:header></div>'
            '<p>Total revenue was 64 billion.</p><header>Merck</header></body></html>')
    text = html_to_text(html)
    assert "FALSE2025FY" not in text and "RevenuesMember" not in text
    assert "Total revenue" in text and "Merck" in text


def test_chunk_size_counts_spaceless_text():
    from extractor.sections import Chunk
    assert Chunk(1, "x" * 80_000).words >= 10_000
