"""An annual report found outside the report step is used as the report (issue 15)."""

import datetime as dt
import json

from extractor import datapoints as dp
from extractor.batch import Company
from extractor.documents import DOC_TYPES, Candidate, Document, title_year
from extractor.scraper import Page


def _pages(cover: str, n: int = 177) -> list[Page]:
    return [Page(1, cover)] + [Page(i, f"page {i} text") for i in range(2, n + 1)]


def test_an_annual_report_is_known_by_the_title_on_its_cover():
    assert title_year(_pages("# ANNUAL REPORT 2025 \n\nAS TALLINK GRUPP")) == 2025
    assert title_year(_pages("Page 1 Annual Report 2025/26 Page 2")) == 2026     # year ending 2026
    assert title_year(_pages("Equinor 2025 Årsrapport")) == 2025
    assert title_year(_pages("ANNUAL REPORT 2025", n=12)) is None                 # too short
    assert title_year(_pages("Annual report on remuneration 2025")) is None       # UK pay report
    assert title_year(_pages("Sustainability report 2023")) is None
    assert title_year(_pages("Annual report")) is None                            # no year


def test_a_report_is_lacking_when_missing_or_older_than_sought(monkeypatch):
    assert dp.sought_year(dt.date(2026, 11, 11)) == 2025
    monkeypatch.setattr(dp, "sought_year", lambda today=None: 2025)
    assert dp.lacks_report(None)
    assert dp.lacks_report({"fiscal_year": "2024"})
    assert not dp.lacks_report({"fiscal_year": "2025"})
    assert not dp.lacks_report({"fiscal_year": "2025/26"})
    assert not dp.lacks_report({"fiscal_year": None})        # unknown: left alone


def _company(tmp_path, monkeypatch):
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.company_id}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.company_id}.err"))
    monkeypatch.setattr(dp, "share_conversion", lambda slug, url: None)
    return Company("tallink", "Tallink Grupp", "FI")


def test_a_found_report_replaces_a_failed_report_step(tmp_path, monkeypatch):
    c = _company(tmp_path, monkeypatch)
    c.error_path.write_text("{}")

    def fake_run(name, **kw):
        result = {"fiscal_year": "2025", "report_url": kw["report_url"], "website": "https://image.tallink.com"}
        c.result_path.write_text(json.dumps(result))
        return result | {"_output_path": "x"}
    monkeypatch.setattr(dp, "run_report", fake_run)
    url = "https://image.tallink.com/annual-reports/2025/tallink-annual-report-2025-eng.pdf"
    got = dp.use_as_report(dp.Target(c), url, None, None, "annual_report_url in the input")
    assert got["fiscal_year"] == "2025" and "_output_path" not in got
    assert got["website"] is None                     # not the report's host
    assert got["report_source"] == "annual_report_url in the input"
    assert not c.error_path.exists()
    assert json.loads(c.result_path.read_text())["fiscal_year"] == "2025"


def test_a_found_report_never_replaces_a_newer_one(tmp_path, monkeypatch):
    c = _company(tmp_path, monkeypatch)
    c.result_path.write_text(json.dumps({"fiscal_year": "2024", "report_url": "old.pdf"}))

    def fake_run(name, **kw):
        c.result_path.write_text(json.dumps({"fiscal_year": "2023"}))
        return {"fiscal_year": "2023"}
    monkeypatch.setattr(dp, "run_report", fake_run)
    assert dp.use_as_report(dp.Target(c), "https://x.com/ar-2023.pdf", "https://x.com", None, "t") is None
    assert json.loads(c.result_path.read_text())["report_url"] == "old.pdf"       # restored

    def failing_run(name, **kw):
        raise ValueError("no text")
    monkeypatch.setattr(dp, "run_report", failing_run)
    assert dp.use_as_report(dp.Target(c), "https://x.com/ar.pdf", None, None, "t") is None


def test_the_annual_report_is_looked_for_among_the_documents():
    report = Document("https://x.com/annual-report-2025.pdf", DOC_TYPES["annual_report"], "pdf",
                      _pages("ANNUAL REPORT 2025"), 2025, "")
    hub = Document("https://x.com/reports", DOC_TYPES["annual_report"], "web", [Page(1, "Reports")], None, "")

    class Lib:
        def __init__(self, docs):
            self.docs, self.accepts = list(docs), []

        def find(self, key, search=False, accept=None):
            assert key == "annual_report"
            self.accepts.append(accept)
            return self.docs.pop(0) if self.docs else None
    lib = Lib([hub, report])
    assert dp.find_annual_report(lib, 2025) is report        # the hub page first, then its PDF
    old = Candidate("https://x.com/annual-reports-2024", DOC_TYPES["annual_report"], 2, 2024, False, 0)
    assert not lib.accepts[0](old)                           # an older year is not fetched
    assert dp.find_annual_report(Lib([hub]), 2025) is None
    old_pdf = Document("https://x.com/ar.pdf", DOC_TYPES["annual_report"], "pdf",
                       _pages("ANNUAL REPORT 2024"), None, "")
    assert dp.find_annual_report(Lib([old_pdf]), 2025) is None


def test_collect_reads_the_inputs_annual_report_when_the_report_step_failed(tmp_path, monkeypatch):
    c = _company(tmp_path, monkeypatch)
    c.error_path.write_text(json.dumps({"error_type": "NeedsOCRError", "error": "scanned"}))
    monkeypatch.setattr(dp, "identify_lei", lambda *a, **k: {"record": None})
    monkeypatch.setattr(dp, "load_settings", lambda: None)
    monkeypatch.setattr(dp, "FirecrawlClient", lambda *a, **k: type("FC", (), {"credits": type("C", (), {"total": 0})()})())
    monkeypatch.setattr(dp.sector, "from_description", lambda chosen, name: None)
    used = []
    monkeypatch.setattr(dp, "use_as_report", lambda t, url, site, fc, how: used.append((url, how)))
    url = "https://image.tallink.com/annual-reports/2025/tallink-annual-report-2025-eng.pdf"
    t = dp.Target(c, annual_report_url=url)
    dp.collect(t, docs=False, use_apis=False)
    assert used == [(url, "annual_report_url in the input")]
    used.clear()
    c.result_path.write_text(json.dumps({"fiscal_year": str(dp.sought_year())}))
    monkeypatch.setattr(dp, "read_report", lambda *a, **k: (None, []))
    dp.collect(t, docs=False, use_apis=False)
    assert used == []                                        # a report of the year: kept
    used.clear()
    t.fields = frozenset({"isin"})                           # API fields need no report
    c.result_path.unlink()
    dp.collect(t, docs=False, use_apis=False)
    assert used == []


def test_a_report_found_on_the_site_by_another_company_is_not_used(tmp_path, monkeypatch):
    from extractor.apis import Found
    c = _company(tmp_path, monkeypatch)
    c.error_path.write_text('{"error_type": "ReportNotFoundError"}')
    fake_fc = type("FC", (), {"credits": type("C", (), {"total": 0})()})()
    monkeypatch.setattr(dp, "identify_lei", lambda *a, **k: {"record": None})
    monkeypatch.setattr(dp, "load_settings", lambda: None)
    monkeypatch.setattr(dp, "FirecrawlClient", lambda *a, **k: fake_fc)
    monkeypatch.setattr(dp, "website_for", lambda *a: "https://jinhuiship.com")
    monkeypatch.setattr(dp, "Library", lambda *a, **k: type("L", (), {"report_year": None})())
    monkeypatch.setattr(dp.sector, "from_description", lambda chosen, name: None)
    monkeypatch.setattr(dp, "from_pay", lambda *a, **k: ([], [], []))
    monkeypatch.setattr(dp, "from_documents", lambda *a, **k: ([], []))
    parent = Document("https://jinhuiship.com/jh2025AR.pdf", DOC_TYPES["annual_report"], "pdf",
                      _pages("ANNUAL REPORT 2025"), 2025, "")
    monkeypatch.setattr(dp, "find_annual_report", lambda lib, year: parent)

    def fake_use(t, url, site, fc, how):
        c.result_path.write_text('{"fiscal_year": "2025"}')
        c.error_path.unlink()
        return {"fiscal_year": "2025", "report_url": url}
    monkeypatch.setattr(dp, "use_as_report", fake_use)
    flagged = Found("revenue", 1228e6, source="Annual report (PDF)", confidence="C",
                    note=f"check: the report is by 'JINHUI HOLDINGS': {dp.OTHER_COMPANY}")
    monkeypatch.setattr(dp, "read_report", lambda *a, **k: (None, [flagged]))
    rows = {f.data_point: f for f in dp.collect(dp.Target(c), use_apis=False)}
    assert rows["revenue"].value is None                   # the parent's figure is not taken
    assert not c.result_path.exists() and c.error_path.exists()     # as before the search
    monkeypatch.setattr(dp, "read_report", lambda *a, **k: (None, [Found(
        "revenue", 131e6, source="Annual report (PDF)", confidence="B")]))
    rows = {f.data_point: f for f in dp.collect(dp.Target(c), use_apis=False)}
    assert rows["revenue"].value == 131e6 and c.result_path.exists()


def test_a_conversion_is_shared_between_the_report_step_and_the_library(tmp_path, monkeypatch):
    monkeypatch.setattr(dp, "CACHE_DIR", tmp_path)
    url = "https://x.com/ar.pdf"
    doc = tmp_path / dp.doc_stem("s", url)
    doc.with_suffix(".md").write_text("<!-- page 1 -->\nx")
    doc.with_suffix(".pdf").write_bytes(b"%PDF")
    dp.share_conversion("s", url)
    report = tmp_path / dp.cache_stem("s", url)
    assert report.with_suffix(".md").exists() and report.with_suffix(".pdf").exists()
