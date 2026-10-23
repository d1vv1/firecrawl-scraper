"""Unit tests: no network, no LLM."""

import datetime as dt

import pytest

from extractor.config import clean_name, slugify
from extractor.extract import full_value
from extractor.report_finder import ReportCandidate, classify, extract_year, pick_best
from extractor.schemas import MoneyFigure
from extractor.scraper import Page, looks_like_pdf, markdown_to_pages, pages_to_markdown
from extractor.sections import is_toc, score_chunk, FINANCIALS
from extractor.validate import (check_balance, check_fiscal_year, latest_year, normalize,
                                quote_in_text, value_in_quote)
from extractor.website import is_blocked, registered_domain, score_candidate


# --- step 1 ---------------------------------------------------------------------

@pytest.mark.parametrize("name,clean", [
    ("Unilever PLC", "unilever"),
    ("Siemens AG", "siemens"),
    ("Koninklijke Philips N.V.", "koninklijke philips"),
    ("Apple Inc.", "apple"),
    ("Robert Bosch GmbH", "robert bosch"),
    ("Marks and Spencer Group plc", "marks and spencer group"),
])
def test_clean_name(name, clean):
    assert clean_name(name) == clean


def test_slugify():
    assert slugify("Unilever PLC") == "unilever-plc"
    assert slugify("  L'Oréal S.A. ") == "l-oreal-s-a"
    assert slugify("Ørsted A/S") == "orsted-a-s"


# --- step 2 ---------------------------------------------------------------------

def test_blocklist_and_domains():
    assert is_blocked("en.wikipedia.org")
    assert is_blocked("uk.linkedin.com")
    assert not is_blocked("www.unilever.com")
    assert registered_domain("www.unilever.co.uk") == "unilever.co.uk"
    assert registered_domain("investors.unilever.com") == "unilever.com"


def test_website_scoring_prefers_official_domain():
    official = score_candidate("unilever", "unilever.com", "Investor relations | Unilever")
    other = score_candidate("unilever", "unileverfoodsolutions.com", "UFS")
    unrelated = score_candidate("unilever", "example.com", "Some page")
    assert official > other > unrelated
    assert official >= 0.9 and unrelated < 0.5


# --- step 3 ---------------------------------------------------------------------

@pytest.mark.parametrize("url", [
    "https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf",
    "https://x.com/docs/AnnualReport2024.pdf",
    "https://x.com/investors/integrated-report-2024/",
    "https://x.com/Universal-Registration-Document-2024.pdf",
    "https://x.com/annual_report_2023.pdf",
])
def test_keep_filter(url):
    assert classify(url).kept


@pytest.mark.parametrize("url,why", [
    ("https://x.com/half-year-annual-report-2025.pdf", "half-year"),
    ("https://x.com/annual-report-2024-q3.pdf", "q3"),
    ("https://x.com/annual-report-2024-summary.pdf", "summary"),
    ("https://x.com/sustainability-annual-report-2024.pdf", "sustainability"),
    ("https://x.com/annual-report-2024/remuneration.pdf", "remuneration"),
    ("https://x.com/annual-report-esg-2024.pdf", "esg"),
    ("https://x.com/investors/results-2024.pdf", "no annual-report keyword"),
])
def test_exclude_filter(url, why):
    c = classify(url)
    assert not c.kept and why in c.reason


def test_exclude_tokens_need_boundaries():
    # "faq1" must not trip the "q1" exclusion
    assert classify("https://x.com/faq1/annual-report-2024.pdf").kept


def test_extract_year():
    # the file name wins over the folder (folders are often the publication date)
    assert extract_year("https://x.com/2025/03/annual-report-2024.pdf") == 2024
    assert extract_year("https://x.com/2025/03/annual-report.pdf") == 2025
    assert extract_year("https://x.com/annual-report.pdf") is None


def test_pick_best_newest_year_then_pdf():
    cands = [classify(u) for u in [
        "https://x.com/annual-report-2023.pdf",
        "https://x.com/annual-report-2024/",
        "https://x.com/annual-report-2024.pdf",
        "https://x.com/half-year-report-2025.pdf",
    ]]
    assert pick_best(cands).url == "https://x.com/annual-report-2024.pdf"


def test_pick_best_prefers_report_and_accounts_over_20f():
    cands = [classify(u) for u in [
        "https://www.unilever.com/files/unilever-annual-report-on-form-20-f-2025.pdf",
        "https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf",
    ]]
    assert "and-accounts" in pick_best(cands).url


def test_pick_best_none():
    assert pick_best([ReportCandidate("u", False, "x")]) is None


# --- step 4 ---------------------------------------------------------------------

def test_looks_like_pdf():
    assert looks_like_pdf(b"%PDF-1.7 ...", "application/octet-stream")
    assert not looks_like_pdf(b"<html>cookie wall</html>", "application/pdf")
    assert not looks_like_pdf(b"<HTML>Access Denied", "text/html")


def test_markdown_page_roundtrip():
    pages = [Page(1, "first"), Page(2, "# Heading\nsecond"), Page(5, "")]
    back = markdown_to_pages(pages_to_markdown(pages))
    assert [(p.number, p.text) for p in back] == [(1, "first"), (2, "# Heading\nsecond"), (5, "")]


# --- step 5 ---------------------------------------------------------------------

TOC = """## Contents
Strategic report
Chair's statement 4
Chief Executive Officer's review 6
Our business model 10
Our strategy 14
Segment information 160
Consolidated income statement 131
Consolidated balance sheet 134
Principal subsidiaries 210
"""

TOC_TABLE = """|Strategic report||
|---|---|
|Business model|10|
|Our strategy|14|
|Consolidated income statement|131|
|Consolidated balance sheet|134|
|Related undertakings|212|
"""

INCOME_STATEMENT = """## **Consolidated income statement**
|**Notes**|**€ million**<br>**2025**|**€ million**<br>**2024**|
|---|---|---|
|**Turnover**|**2**|**50,503**|**52,479**|
|**Operating profit**|**2**|**9,037**|**8,829**|
|**Net finance costs**|**5**|**(503)**|**(520)**|
|**Finance income**||**398**|**391**|
|**Finance costs**||**(1,024)**|**(994)**|
|**Profit before taxation**||**8,693**|**8,371**|
|**Taxation**|**6A**|**(2,481)**|**(2,332)**|
|**Net profit**||**6,213**|**6,039**|
"""


def test_toc_detection():
    assert is_toc(TOC)
    assert is_toc(TOC_TABLE)
    assert not is_toc(INCOME_STATEMENT)
    assert not is_toc("Our business model creates value for shareholders. " * 20)


def test_statement_with_numbers_is_boosted():
    narrative = "Turnover grew this year and revenue rose. Our consolidated income statement shows it."
    table = INCOME_STATEMENT * 3   # enough numbers for the boost
    assert score_chunk(table, FINANCIALS, True) > 5 * score_chunk(narrative, FINANCIALS, True)


# --- step 6 ---------------------------------------------------------------------

@pytest.mark.parametrize("value,unit,expected", [
    (50503, "millions", 50_503_000_000),
    (1.5, "billions", 1_500_000_000),
    (1234, "thousands", 1_234_000),
    (99, "units", 99),
    (None, "millions", None),
    (12, None, None),
])
def test_unit_conversion(value, unit, expected):
    assert full_value(value, unit) == expected


# --- step 7 ---------------------------------------------------------------------

def test_normalize():
    assert normalize("**Turnover**  60,073") == "turnover 60073"
    assert normalize("Total assets 1.234.567") == "total assets 1234567"
    assert normalize("12 345 – x") == "12345 - x"
    assert normalize("|**Turnover**|**2**|**50,503**|") == "turnover 2 50503"


def test_quote_matching():
    src = INCOME_STATEMENT
    assert quote_in_text("Turnover 2 50,503", src) == "exact"
    assert quote_in_text("TURNOVER | 2 | 50,503 | 52,479", src) == "exact"
    # skipping the Notes column is accepted as a loose match
    assert quote_in_text("Turnover 50,503", src) == "loose"
    assert quote_in_text("Turnover 60,073", src) is None
    assert quote_in_text("Revenue 50,503", src) is None


def test_value_in_quote():
    assert value_in_quote(50503, "Turnover 50,503")
    assert value_in_quote(1024, "Finance costs (1,024)")
    assert value_in_quote(1.5, "Revenue €1.5 billion")
    assert not value_in_quote(52479, "Turnover 50,503")


def _money(value, unit="millions", currency="EUR"):
    return MoneyFigure(value=value, unit=unit, currency=currency, label_in_report="x",
                       scope="consolidated", quote=None, chunk_id=None, not_found_reason=None)


def test_balance_check():
    assert check_balance(_money(70471), _money(70471)).result == "pass"
    assert check_balance(_money(70471), _money(70700)).result == "pass"      # 0.32%
    assert check_balance(_money(70471), _money(71000)).result == "fail"      # 0.75%
    assert check_balance(_money(70.471, "billions"), _money(70471)).result == "pass"
    assert check_balance(_money(70471), _money(None)).result == "skipped"


def test_fiscal_year():
    today = dt.date(2026, 10, 15)
    assert latest_year("2024/25") == 2025
    assert latest_year("FY 2025") == 2025
    assert check_fiscal_year("2025", today).result == "pass"
    assert check_fiscal_year("2022", today).result == "fail"   # 2026 - 3 = 2023 is the oldest allowed
    assert check_fiscal_year("2023", today).result == "pass"
    assert check_fiscal_year("2021", today).result == "fail"
    assert check_fiscal_year(None, today).result == "fail"


def test_year_ignores_hashes_and_future():
    assert extract_year("https://x.com/files/origin/88e38cde205966bf/1956%20Annual%20Report.pdf") is None
    assert extract_year("https://x.com/annual-report-2099.pdf") is None
    assert extract_year("https://x.com/unilever-annual-report-and-accounts-2025.pdf") == 2025


def test_pdf_beats_newer_html_and_press_releases_excluded():
    cands = [classify(u) for u in [
        "https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf",
        "https://www.unilever.com/investors/annual-report-and-accounts-2026/",
        "https://www.unilever.com/news/press-and-media/press-releases/2026/filing-of-annual-report-on-form-20f-2026",
    ]]
    assert not cands[2].kept
    assert pick_best(cands).url.endswith("accounts-2025.pdf")


def test_iso_period_end():
    from extractor.extract import iso_period_end
    assert iso_period_end("2025-12-31", "2025") == "2025-12-31"
    assert iso_period_end("31 December 2025", None) == "2025-12-31"
    assert iso_period_end("31 December", "2025") == "2025-12-31"
    assert iso_period_end("31 March", "2024/25") == "2025-03-31"
    assert iso_period_end("year end", "2025") is None
    assert iso_period_end(None, "2025") is None


def test_quote_fragments_joined_with_ellipsis():
    from extractor.sections import Chunk
    from extractor.validate import check_quote
    src = [Chunk(1, "Unilever is the parent company of the Group. Other text here. "
                    "The segments are Beauty & Wellbeing, Personal Care, Home Care and Foods.")]
    ok = check_quote("x", "Unilever is the parent company...segments are Beauty & Wellbeing, Personal Care", 1, src)
    assert ok.result == "pass" and "fragments" in ok.detail
    bad = check_quote("x", "Unilever is the parent company...segments are Ice Cream and Tea", 1, src)
    assert bad.result == "fail"


def test_quote_cut_mid_sentence_with_added_period():
    src = "Its shares trade in the form of American Depositary Shares, with one ADS per share."
    assert quote_in_text("in the form of American Depositary Shares.", src) == "exact"
    assert quote_in_text("in the form of Global Depositary Receipts.", src) is None


@pytest.mark.parametrize("name,domain,title", [
    ("1&1 AG", "1und1.ag", "1&1 AG Investor Relations"),
    ("1&1 AG", "1und1.de", None),
    ("Marks & Spencer Group plc", "marksandspencer.com", "M&S Corporate"),
    ("Procter & Gamble Co", "pg.com", "P&G"),          # abbreviation: not solvable by spelling
])
def test_ampersand_spellings(name, domain, title):
    s = score_candidate(clean_name(name), domain, title)
    if domain == "pg.com":
        assert s < 0.5          # documented limit: needs Wikidata or --website
    else:
        assert s >= 0.5          # passes WEBSITE_MIN_SCORE


def test_ampersand_does_not_match_unrelated_domains():
    assert score_candidate(clean_name("1&1 AG"), "example1.com", "Some page") < 0.2
    assert score_candidate(clean_name("1&1 AG"), "1und1.ag", "x") > score_candidate(
        clean_name("1&1 AG"), "1and1.com", "x") - 0.01   # both spellings are equally fine


def test_value_in_quote_space_grouped_thousands():
    assert value_in_quote(19889, "Net sales 19 889")
    assert value_in_quote(37597, "Total shareholders' equity and liabilities 37 597")
    assert value_in_quote(1234567, "Revenue 1 234 567")
    assert not value_in_quote(19889, "Net sales 19 888")


def test_quote_in_other_chunk_than_cited():
    from extractor.sections import Chunk
    from extractor.validate import check_quote
    chunks = [Chunk(1, "Unrelated text about strategy."),
              Chunk(2, "|**Total shareholders’ equity and liabilities**||**37 597**|**39 149**|")]
    c = check_quote("x", "Total shareholders’ equity and liabilities 37 597", 1, chunks)
    assert c.result == "pass" and "model cited chunk 1" in c.detail
    assert check_quote("x", "Total equity 99 999", 1, chunks).result == "fail"


def test_dot_leaders_are_ignored_in_quotes():
    src = "|Net sales     . . . . . . . . . . . . . . . .|. .<br>$ 5,219,376|$ 4,206,289|"
    assert quote_in_text("Net sales . . . . . . .|. .\n$ 5,219,376", src) == "exact"
    assert normalize("Revenue 3.14 and 1.5") == "revenue 3.14 and 1.5"     # decimals untouched


# --- number-in-quote check, from real failures (Oct 2026) -------------------------

def test_value_in_quote_decimal_comma():
    from extractor.validate import match_value
    assert match_value(2473.7, "| Total | 2 473,7 | 2 450,8 |", "millions") == "exact"   # Altareit
    assert match_value(393.4, "Hyresintäkter 393,4", "millions") == "exact"               # Fortinova
    assert match_value(2450.8, "| Total | 2 473,7 | 2 450,8 |", "millions") == "exact"


def test_value_in_quote_table_cells_with_note_numbers():
    from extractor.validate import match_value
    assert match_value(136425, "|**Revenues**|5, 6|**136 425**|133 795|", "thousands")   # Infront
    assert match_value(403685, "|Revenue    5|403 685|369 236|", "thousands")            # Duett
    assert not match_value(136426, "|**Revenues**|5, 6|**136 425**|133 795|", "thousands")


def test_value_in_quote_other_units():
    from extractor.validate import match_value
    assert match_value(37400, "Total revenues were $37.4 billion in 2025", "millions") == "scaled"  # CRH
    assert match_value(1200, "Net sales SEK 1.2bn", "millions") == "scaled"
    assert match_value(1234, "Net sales SEK 1.2bn", "millions") == "scaled"    # within the quote's rounding
    assert not match_value(1300, "Net sales SEK 1.2bn", "millions")
    assert not match_value(37400, "Total revenues were $37.4 in 2025", "millions")     # no scale word


def test_prescaled_value_is_corrected():
    from extractor.schemas import MoneyFigure
    from extractor.validate import check_value_in_quote
    fig = MoneyFigure(value=906943000.0, unit="thousands", currency="NOK", label_in_report="Revenue",
                      scope="consolidated", quote="Total revenue and other income 906,943",
                      chunk_id=1, not_found_reason=None)                               # Bulk Infrastructure
    c = check_value_in_quote("revenue", fig)
    assert c.result == "pass" and fig.value == 906943
    real_miss = MoneyFigure(value=4430534.0, unit="thousands", currency="NOK", label_in_report="Revenue",
                            scope="consolidated", quote="Total revenue and other operating income 4 446 534",
                            chunk_id=1, not_found_reason=None)                         # Glamox: misread
    assert check_value_in_quote("revenue", real_miss).result == "fail"


def test_value_in_quote_swiss_apostrophe():
    from extractor.validate import match_value
    assert match_value(414843, "Net sales 414'843", "thousands") == "exact"     # R&S Group


def test_fiscal_year_prefix_and_subsidiary_files():
    from extractor.report_finder import allowed_place_words
    assert extract_year("https://x.com/Annual-Financial-Report-FY2025.pdf") == 2025
    assert extract_year("https://x.com/a/205966bf.pdf") is None          # still not a hash
    allowed = allowed_place_words("Siemens AG", ["DE"])
    plc = classify("https://x.com/siemens-plc-annual-report-and-financial-statements-2025.pdf", allowed)
    assert not plc.kept and "another legal entity" in plc.reason
    own = classify("https://x.com/Annual-Financial-Report-FY2025.pdf", allowed)
    sub = classify("https://x.com/sfm-annual-report-2025.pdf", allowed)
    assert pick_best([sub, own]).url == own.url                         # 'sfm' is unexplained
    assert classify("https://x.com/acme-ab-annual-report-2025.pdf",
                    allowed_place_words("Acme AB", ["SE"])).kept        # its own legal form


def test_a_value_the_ai_already_scaled_is_not_scaled_again():
    from extractor.extract import full_value_quoted
    assert full_value_quoted(13380, "millions", "EBITDA 13,380") == 13_380_000_000
    assert full_value_quoted(13_380_000_000, "millions", "EBITDA 13,380") == 13_380_000_000
    assert full_value_quoted(2326.2, "millions", "Net sales|3|2,326.2") == 2_326_200_000
    assert full_value_quoted(1050, "thousands", "Base salary|1.050|1.000") == 1_050_000
    assert full_value_quoted(5, "millions", None) == 5_000_000          # no quote: as before


def test_years_inside_dates_in_file_names():
    assert extract_year("https://x.gr/uploads/159286/51c9_jumboannualreport_31122025_en.pdf") == 2025
    assert extract_year("https://x.com/annual_report_20251231.pdf") == 2025
    assert extract_year("https://x.com/a/9f31122025aa.pdf") is None            # part of a hash


def test_report_pdfs_in_event_folders_and_subsidiary_functions():
    from extractor.report_finder import allowed_place_words, _rank
    allowed = allowed_place_words("Aktiebolaget Volvo", ["SE"])
    ar = classify("https://www.volvogroup.com/content/dam/volvo-group/markets/master/events/2026/"
                  "volvo-group%E2%80%93annual-report-2025.pdf", allowed)
    assert ar.kept and ar.year == 2025
    assert not classify("https://x.com/events/2026/annual-report-2025.html", allowed).kept   # a page
    treasury = classify("https://www.volvogroup.com/investors/debt-information/downloads/"
                        "volvo-treasury-annual-report-2025.pdf", allowed)
    assert treasury.unexplained == 1 and _rank(ar) > _rank(treasury)
    assert classify("https://x.com/AB-Volvo-Annual-Report-2022.pdf", allowed).unexplained == 0
