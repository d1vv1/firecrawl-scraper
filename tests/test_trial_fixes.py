"""Two things the version 2 trial showed (12 Nov 2026): a site whose pages all fail kept a
worker over an hour (SEB), and an investment company's "Operating income" was taken as its
revenue and its EBITDA (Industrivärden)."""

from firecrawl import InternalServerError, RateLimitError

from extractor import datapoints as dp
from extractor import documents
from extractor.apis import Found
from extractor.firecrawl_client import _retryable


def test_a_page_firecrawl_could_not_get_is_not_tried_again():
    failed = InternalServerError("Internal Server Error: Failed to scrape. All scraping engines "
                                 "failed to retrieve content from this URL.", 500)
    assert not _retryable(failed)
    assert _retryable(InternalServerError("upstream connect error", 500))
    assert _retryable(RateLimitError("Rate limit exceeded", 429))
    assert not _retryable(ValueError("no"))


def test_the_document_fallback_stops_fetching_when_its_time_is_up(monkeypatch, tmp_path):
    monkeypatch.setattr(documents, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(documents, "DOC_MINUTES", 0)

    def no_download(*a, **k):
        raise AssertionError("fetched after the time was up")
    monkeypatch.setattr(documents, "download", no_download)
    lib = documents.Library("acme", "https://acme.com", 2025, fc=None)
    dt_ = documents.DocType("rem", "Remuneration report", "remuneration", ("remuneration",))
    c = documents.Candidate("https://acme.com/rem.pdf", dt_, 2, 2025, True, 1)
    assert lib.fetch(c) is None and lib.out_of_time
    lib._map("remuneration")                       # no map either
    # a document already cached is still read
    (tmp_path / f"{documents._stem('acme', c.url)}.md").write_text("Remuneration " * 200, encoding="utf-8")
    assert lib.fetch(c) is not None


def _found(rev, ebitda=None):
    out = [Found("revenue", rev, note="PDF page 3")]
    return out + ([Found("ebitda", ebitda)] if ebitda is not None else [])


def test_a_revenue_read_off_a_profit_line_is_dropped():
    kept = dp.not_a_profit_line(_found(1e9), "Operating profit 1,000")
    assert [f.data_point for f in kept] == []
    kept = dp.not_a_profit_line(_found(1e9), "Rörelseresultat 1 000")
    assert kept == []
    # the statement's name, or a label that names revenue, is not a profit line
    for q in ("In the Consolidated Statement of Profit or Loss, management fees total £416.0 million",
              "Consolidated revenues and other income and adjusted EBITDA 3,720", "Revenue 1,000"):
        assert len(dp.not_a_profit_line(_found(1e9), q)) == 1, q


def test_a_revenue_and_an_ebitda_of_the_same_figure():
    kept = dp.not_a_profit_line(_found(439266000, 439266000), "Operating income 439,266")
    assert [f.data_point for f in kept] == ["revenue"]
    assert kept[0].confidence == "C" and dp.SAME_AS_PROFIT in kept[0].note
    kept = dp.not_a_profit_line(_found(1e9, 2e8), "Revenue 1,000")
    assert [f.data_point for f in kept] == ["revenue", "ebitda"]
