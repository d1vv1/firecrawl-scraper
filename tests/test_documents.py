"""Document fallback: which documents fit which data points, and finding them."""

import json

from extractor import documents as docs
from extractor.documents import DOC_TYPES, Library, classify, gap_types, links_in


def test_document_types_ordered_by_expected_yield():
    keys = [d.key for d in gap_types(["pension_type", "shareholding_requirement", "isin"])]
    assert keys[0] == "remuneration_policy"    # first choice for two gaps
    assert set(keys) == {"remuneration_policy", "remuneration", "agm_notice", "share"}


def test_a_remuneration_policy_ranks_below_the_report():
    rem = DOC_TYPES["remuneration"]
    report = classify("https://acme.com/remuneration-report-2025.pdf", rem, report_year=2025)
    policy = classify("https://acme.com/remuneration-policy-2024.pdf", rem, report_year=2025)
    assert report.score > policy.score
    assert classify("https://acme.de/hv/verguetungssystem-2025.pdf", DOC_TYPES["remuneration_policy"])


def test_classify_reads_native_words_and_link_text():
    rem = DOC_TYPES["remuneration"]
    assert classify("https://acme.se/ersattningsrapport-2025.pdf", rem, report_year=2025).score == 2
    assert classify("https://acme.de/hv/Verguetungsbericht_2025.pdf", rem, report_year=2025)
    # the file name says nothing; the link text does
    c = classify("https://cdn.acme.com/a8f7e1.pdf", rem, "Remuneration report 2025", 2025)
    assert c and c.year == 2025
    assert classify("https://acme.com/products/remuneration", rem) is None       # skip list
    assert classify("https://acme.com/remuneration-report-2019.pdf", rem, report_year=2025) is None
    assert classify("https://acme.com/remuneration.xlsx", rem) is None           # phase 2
    assert classify("https://www.linkedin.com/remuneration", rem) is None     # blocked domain


def test_short_keywords_stand_alone():
    assert classify("https://acme.com/reports/q4-2025.pdf", DOC_TYPES["year_end"])
    assert classify("https://acme.com/faq4", DOC_TYPES["year_end"]) is None


def test_links_in_a_page():
    md = "[Remuneration report 2025](/files/abc.pdf) see https://storage.mfn.se/x/rem.pdf"
    links = links_in(md, "https://acme.com/governance/")
    assert links["https://acme.com/files/abc.pdf"] == "Remuneration report 2025"
    assert "https://storage.mfn.se/x/rem.pdf" in links


def test_library_picks_from_cached_urls_without_credits(tmp_path, monkeypatch):
    monkeypatch.setattr(docs, "CACHE_DIR", tmp_path)
    (tmp_path / "x_discovery.json").write_text(json.dumps({"report_candidates": [
        {"url": "https://www.acme.com/investors/annual-report-2025.pdf"},
        {"url": "https://www.acme.com/governance/remuneration-report-2024.pdf"},
        {"url": "https://www.acme.com/governance/remuneration-report-2025.pdf"},
        {"url": "https://other.com/about/remuneration-report-2025"},
    ]}), encoding="utf-8")

    class NoCalls:
        max_credits = 10

        def map(self, *a, **k):
            raise AssertionError("no map needed")

    lib = Library("x", "https://www.acme.com", 2025, NoCalls(),
                  skip_urls=["https://www.acme.com/investors/annual-report-2025.pdf"])
    picked = lib._best(DOC_TYPES["remuneration"])
    assert picked.url == "https://www.acme.com/governance/remuneration-report-2025.pdf"
    assert "https://other.com/about/remuneration-report-2025" not in lib.pool   # off-site page


def test_library_maps_the_site_when_nothing_is_cached(tmp_path, monkeypatch):
    monkeypatch.setattr(docs, "CACHE_DIR", tmp_path)
    calls = []

    class Fc:
        max_credits = 10

        def map(self, site, search, limit):
            calls.append(search)
            return [{"url": "https://www.acme.com/investors/the-share", "title": "The share"}] \
                if search == "share" else []

    lib = Library("x", "https://www.acme.com", 2025, Fc())
    picked = lib.pick(["isin"], 3)
    assert calls == [None, "share"]                # plain map first, then the targeted one
    assert [c.url for c in picked] == ["https://www.acme.com/investors/the-share"]
    Library("x", "https://www.acme.com", 2025, Fc()).pick(["isin"], 3)
    assert calls == [None, "share"]                # cached: no second charge


def test_news_pages_are_not_the_page_itself():
    sh = DOC_TYPES["shareholders"]
    assert classify("https://acme.com/blog/shareholders-approve-the-merger", sh) is None
    assert classify("https://acme.com/news/2025/shareholders-report.pdf", sh)        # a PDF is fine
    assert classify("https://acme.com/press/acme-ipo-first-day-of-trading", DOC_TYPES["listing"])
    assert classify("https://acme.no/en/investors/announcements/acme-shares-ex-dividend",
                    DOC_TYPES["share"]) is None


def test_a_page_with_and_without_trailing_slash_is_one_page(tmp_path, monkeypatch):
    monkeypatch.setattr(docs, "CACHE_DIR", tmp_path)
    lib = Library("x", "https://www.acme.com", 2025, None)
    lib._add({"https://www.acme.com/investors/owners": "", "https://www.acme.com/investors/owners/": ""})
    assert list(lib.pool) == ["https://www.acme.com/investors/owners"]
