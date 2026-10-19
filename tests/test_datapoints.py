"""Data-point rows: where values come from, which value wins, and the CSV format."""

from pathlib import Path

from extractor import datapoints as dp
from extractor.apis import Found
from extractor.batch import Company
from extractor.schemas import DataPointFacts
from extractor.scraper import Page
from extractor.sections import Chunk

ROOT = Path(__file__).resolve().parent.parent


def _origin(kind="pdf"):
    pages = [Page(1, "Contents"), Page(7, "Net sales|3|2,326.2|1,827.3"),
             Page(8, "The CEO's pension is defined contribution, 25 percent of base salary.")]
    chunks = {0: Chunk(0, "Net sales|3|2,326.2|1,827.3\nThe CEO's pension is defined contribution, "
                          "25 percent of base salary.", [7, 8])}
    return dp.Origin(kind, "https://x.com/ar.pdf", "Annual report (PDF)", "PARSE",
                     "2026-10-19T00:00:00+00:00", pages, chunks)


def test_columns_match_the_requested_format():
    assert dp.COLUMNS == ["company_id", "company_name", "segment", "country", "lei", "data_point",
                          "value", "unit", "period_end", "source", "endpoint", "method",
                          "retrieved_at", "confidence", "note"]


def test_pdf_value_gets_the_page_of_its_quote():
    endpoint, conf, note = _origin().where("pension is defined contribution, 25 percent", 0)
    assert endpoint == "https://x.com/ar.pdf#page=8"
    assert conf == "B"
    assert note.startswith("PDF page 8:")


def test_quote_with_wrong_chunk_id_is_still_found():
    loc = dp.locate("Net sales|3|2,326.2", 99, _origin().chunks, _origin().pages)
    assert loc == dp.Located(7, True)


def test_quote_not_in_the_source_is_confidence_c():
    endpoint, conf, note = _origin().where("Revenue rose to 9,999", 0)
    assert conf == "C" and "not found verbatim" in note


def test_html_report_links_to_the_quote_text():
    endpoint, conf, _ = _origin("xhtml").where("pension is defined contribution, 25 percent", 0)
    assert endpoint.startswith("https://x.com/ar.pdf#:~:text=pension%20is%20defined")
    # table rows never match a rendered page: no fragment
    assert dp.text_fragment("https://x.com/a", "Net sales|3|2,326.2") == "https://x.com/a"


def test_exact_source_beats_ai_and_differences_are_noted():
    vals = [Found("headcount", 470, source="Annual report (PDF)", method="PARSE", confidence="B"),
            Found("headcount", 512, source="Brønnøysund", method="API", confidence="A"),
            Found("isin", "SE0015657788", method="SCRAPE", confidence="C")]
    chosen = dp.best(vals)
    assert chosen["headcount"].value == 512
    assert "other source says 470" in chosen["headcount"].note
    assert chosen["isin"].method == "SCRAPE"


def test_every_data_point_gets_a_row_with_a_reason():
    c = Company("x-1", "X AB", "SE", "nordic_uk_unlisted")
    chosen = {"listing_status": Found("listing_status", "unlisted", method="PARSE", confidence="B")}
    rows = dp.finish(dp.Target(c), chosen, ["GLEIF"], [], None)
    assert [r.data_point for r in rows] == dp.NAMES
    by = {r.data_point: r for r in rows}
    assert by["market_cap"].method == "BUY"
    assert by["ticker"].note.startswith("not applicable")
    assert by["cik"].note.startswith("not applicable")
    assert by["revenue"].note == "not found in: GLEIF"


def test_isin_confirmed_by_gleif_is_confidence_a():
    c = Company("x-1", "X AB", "SE")
    chosen = {"isin": Found("isin", "SE0015657788", method="PARSE", confidence="B", note="p. 34")}
    rows = {r.data_point: r for r in dp.finish(dp.Target(c), chosen, [], ["SE0015657788"], None)}
    assert rows["isin"].confidence == "A"
    assert rows["listing_status"].value == "listed"       # has an ISIN of its own shares


def _facts(**over) -> DataPointFacts:
    none_t = {"value": None, "quote": None, "chunk_id": None}
    none_n = {"value": None, "unit": None, "currency": None, "period_end": None, "quote": None,
              "chunk_id": None}
    none_h = {"name": None, "holder_type": None, "stake_pct": None, "quote": None, "chunk_id": None}
    none_b = {"items": [], "unit": None, "currency": None, "basis": None, "quote": None,
              "chunk_id": None}
    d = {k: none_n for k in ("revenue", "total_assets", "fte", "headcount", "shares_outstanding")}
    d |= {k: none_t for k in ("head_office_city", "ticker", "isin", "exchange", "exchange_segment",
                              "listing_date", "is_listed", "sub_sector", "reporting_currency",
                              "pension_type", "shareholding_requirement")}
    d |= {"controlling_owner": none_h, "major_shareholders": [], "revenue_by_country": none_b,
          "staff_by_country": none_b}
    return DataPointFacts.model_validate(d | over)


def test_owner_facts_map_to_golden_categories():
    owner = {"name": "EQT X", "holder_type": "private_equity", "stake_pct": 62.0,
             "quote": "Net sales|3|2,326.2", "chunk_id": 0}
    found = {f.data_point: f for f in dp.from_facts(_facts(controlling_owner=owner), _origin())}
    assert found["controlling_owner"].value == "private_equity"
    assert found["ownership_type"].value == "pe_backed"
    assert found["pe_stake_5pct"].value == "yes"
    assert found["controlling_owner_name"].value == "EQT X"


def test_facts_without_a_quote_are_dropped():
    fact = {"value": "Stockholm", "quote": None, "chunk_id": None}
    assert dp.from_facts(_facts(head_office_city=fact), _origin()) == []


def test_money_from_the_report_is_in_full_units():
    rev = {"value": 2326.2, "unit": "millions", "currency": "SEK", "period_end": "2024-12-31",
           "quote": "Net sales|3|2,326.2", "chunk_id": 0}
    f = dp.from_facts(_facts(revenue=rev), _origin())[0]
    assert (f.value, f.unit, f.endpoint) == (2326200000.0, "SEK", "https://x.com/ar.pdf#page=7")
    assert dp.fmt_number(f.value) == "2326200000"


def test_rank_pages_prefers_owner_pages_on_the_same_site():
    links = [{"url": "https://www.x.no/eng/owners"}, {"url": "https://www.x.no/news/2024/owners-meet"},
             {"url": "https://other.com/about"}, {"url": "https://www.x.no/eng/about-us"},
             {"url": "https://www.x.no/report.pdf"}]
    got = dp.rank_pages("https://www.x.no", links, ["controlling_owner", "head_office_city"], 3)
    assert got[0] == "https://www.x.no/eng/about-us"     # matches both topics
    assert "https://www.x.no/eng/owners" in got
    assert all("news" not in u and "other.com" not in u and ".pdf" not in u for u in got)


def test_golden_sample_reads_one_target_per_company():
    targets = dp.read_targets(ROOT / "golden_test_sample_5_per_segment_country_all.csv")
    ids = [t.company.company_id for t in targets]
    assert len(ids) == len(set(ids)) == 196
    none_country = [t for t in targets if t.company.segment == "other_unlisted_or_unknown"
                    and t.company.country is None]
    assert none_country                                   # "(none)" means unknown


def test_build_value_uses_the_golden_unit():
    golden = {"unit": "millions", "currency": "SEK"}
    assert dp.build_value(golden, {"value": "2326200000", "unit": "SEK"}) == "2326.2"
    assert dp.build_value({"unit": ""}, {"value": "listed", "unit": ""}) == "listed"
