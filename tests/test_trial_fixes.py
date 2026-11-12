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


def _roles(*specs):
    """CSV-style role rows: (role, aggregate?, {field: value}) in output order."""
    rows = []
    for role, agg, amounts in specs:
        rows.append({"grain": "role", "role_row": role, "data_point": "role_disclosure",
                     "value": "aggregate" if agg else "individual", "unit": ""})
        rows += [{"grain": "role", "role_row": role, "data_point": k, "value": str(v), "unit": "CHF"}
                 for k, v in amounts.items()]
    return rows


def test_a_group_role_read_from_two_documents_is_kept_once():
    from extractor import pay
    other = {"base_salary": 2015000, "sti_paid": 1888000, "total_remuneration": 6706000}
    former = {"base_salary": 537000, "total_remuneration": 1746000}
    rows = _roles(("CEO", False, {"base_salary": 1000000, "total_remuneration": 3574000}),
                  ("Other EC Members", True, other), ("Former EC Members", True, former),
                  ("Other EC", True, other), ("Former EC", True, former))
    assert pay.duplicate_groups(rows) == ["Other EC", "Former EC"]
    left = dp.refresh([dict(r, company_id="dk", company_name="D", segment="", country="CH", lei="",
                            period_end="", source="", endpoint="", method="PARSE", retrieved_at="",
                            confidence="B", note="") for r in rows])
    assert {r["role_row"] for r in left} == {"CEO", "Other EC Members", "Former EC Members"}
    # two people paid the same are two people; a row of zeros says nothing about who it is
    same = {"base_salary": 800000, "total_remuneration": 2000000}
    assert pay.duplicate_groups(_roles(("Co-CEO (A)", False, same), ("Co-CEO (B)", False, same))) == []
    zeros = {"base_salary": 0, "total_remuneration": 0}
    assert pay.duplicate_groups(_roles(("Former members", True, zeros), ("Former", True, zeros))) == []
    # one field apart: not the same row
    assert pay.duplicate_groups(_roles(("Other EC", True, other),
                                       ("Other", True, {**other, "sti_paid": 1})) ) == []


def test_an_accounting_line_is_not_a_person():
    from extractor import pay

    def role(name, quote, amounts):
        rows = [{"grain": "role", "role_row": name, "data_point": "role_disclosure",
                 "value": "individual", "unit": "", "note": f'PDF page 37: "{quote}"'}]
        return rows + [{"grain": "role", "role_row": name, "data_point": k, "value": str(v),
                        "unit": "USD", "note": ""} for k, v in amounts.items()]
    rows = (role("Subsidiary employee", "Option and share program<br>expenses (note 17)<br>-|-|-|(49)|",
                 {"lti_granted": 0, "total_remuneration": 0})
            + role("CEO", "Der Vorstandsvorsitzende Hui Wang", {"base_salary": 0, "total_remuneration": 0})
            + role("CFO", "CFO expenses 105", {"base_salary": 68000, "total_remuneration": 105000}))
    # a person paid nothing stays; so does a paid role whatever its quote says
    assert pay.accounting_lines(rows) == ["Subsidiary employee"]
