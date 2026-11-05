"""Companies from report files (extractor/from_reports.py), with GLEIF stubbed."""

from pathlib import Path

from extractor import from_reports as fr
from extractor.lei import LeiRecord
from extractor.scraper import Page

VOLVO = LeiRecord("OW6OFBNCKXC4US5C7523", "Aktiebolaget Volvo", "SE", "SE", None, "ACTIVE",
                  "ISSUED", "556012-5790")
BANK = LeiRecord("7437003B5WFBOIEFY714", "Skandinaviska Enskilda Banken AB", "SE", "SE", None,
                 "ACTIVE", "ISSUED", "502032-9081")


def _gleif(monkeypatch):
    monkeypatch.setattr(fr.gleif, "fetch_by_lei", lambda v: {VOLVO.lei: VOLVO, BANK.lei: BANK}.get(v))
    monkeypatch.setattr(fr.gleif, "find_lei_by_id", lambda registered_as=None, country=None, isin=None:
                        (VOLVO, "x") if isin == "SE0000115446" or registered_as == "556012-5790"
                        else (None, "x"))


def test_identifiers_are_found_with_valid_check_digits_only():
    pages = [Page(1, f"AB Volvo (publ), Org. nr 556012-5790. LEI {VOLVO.lei}. ISIN SE0000115446."),
             Page(2, "Not an LEI: OW6OFBNCKXC4US5C7524. Not an ISIN: SE0000115447.")]
    got = {(c.kind, c.value) for c in fr.candidates(pages)}
    assert got == {("LEI", VOLVO.lei), ("ISIN", "SE0000115446"), ("SE register", "556012-5790")}


def test_the_reporting_company_wins_over_others_named_in_the_report(monkeypatch):
    _gleif(monkeypatch)
    # the bank's LEI appears more often, but late; Volvo's on the cover, with its name
    pages = [Page(1, f"Annual and Sustainability Report 2025. AB Volvo (publ) LEI {VOLVO.lei}")] + \
            [Page(n, f"Credit facility arranged by {BANK.lei}.") for n in range(40, 46)]
    record, evidence, _ = fr.by_identifiers(pages)
    assert record is VOLVO and "name on the first pages" in evidence


def test_a_file_without_identifiers_falls_back_to_its_cover(monkeypatch, tmp_path):
    monkeypatch.setattr(fr, "read_pages", lambda p: [Page(1, "Remuneration Report 2025 Example Oyj")])
    monkeypatch.setattr(fr, "by_cover", lambda pages: fr.ReportIdentity(
        legal_name="Example Oyj", country="FI", document_type="remuneration_report",
        fiscal_year="2025", quote="Example Oyj"))
    monkeypatch.setattr(fr.gleif, "find_lei", lambda name, country: fr.gleif.LeiResult(None, "no match"))
    got = fr.identify(tmp_path / "x.pdf")
    assert (got.name, got.country, got.document_type, got.record) == \
        ("Example Oyj", "FI", "remuneration_report", None)


def test_files_of_one_company_become_one_row(tmp_path):
    a, b = tmp_path / "ar.pdf", tmp_path / "rem.pdf"
    found = [fr.Identified(a, "annual_report", VOLVO, VOLVO.legal_name, "SE", "identifiers", "SE0000115446"),
             fr.Identified(b, "remuneration_report", VOLVO, VOLVO.legal_name, "SE", "identifiers")]
    rows = fr.company_rows(found)
    assert len(rows) == 1
    r = rows[0]
    assert (r["company_id"], r["lei"], r["isin"]) == ("aktiebolaget-volvo", VOLVO.lei, "SE0000115446")
    assert r["annual_report_url"] == a.resolve().as_uri() and r["remuneration_report_url"] == b.resolve().as_uri()


def test_the_collector_reads_a_supplied_file_as_the_report(tmp_path):
    from extractor import datapoints as dp
    from extractor.scraper import local_file
    pdf = tmp_path / "ar.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    csv_path = tmp_path / "c.csv"
    csv_path.write_text("company_id,company_name,annual_report_url\nvolvo,AB Volvo," + pdf.as_uri() + "\n",
                        encoding="utf-8")
    t = dp.read_targets(csv_path)[0]
    assert t.company.report_url == pdf.as_uri() and local_file(t.company.report_url) == pdf
    assert Path(local_file(str(pdf))) == pdf


def test_a_supplied_file_reruns_the_report_step_without_deleting_or_spending(tmp_path, monkeypatch):
    import json
    from extractor import datapoints as dp
    from extractor.batch import Company
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.slug}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.slug}.error.json"))
    pdf = tmp_path / "ar.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    c = Company("x", "X AB", "SE", report_url=pdf.as_uri())
    c.result_path.write_text(json.dumps({"report_url": "https://x.com/ar.pdf"}), encoding="utf-8")
    opts = {"retry_failed": False, "pipeline_credits": 30, "doc_credits": 20, "docs": True}
    assert dp.needs_pipeline(c, opts) and c.result_path.exists()          # a check, never a delete
    assert dp.worst_case(dp.Target(c), opts) == 20                          # no search for a file
    c.result_path.write_text(json.dumps({"report_url": pdf.as_uri()}), encoding="utf-8")
    assert not dp.needs_pipeline(c, opts)                                   # done with this file
