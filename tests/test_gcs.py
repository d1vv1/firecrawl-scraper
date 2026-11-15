import json

from extractor import datapoints as dp
from extractor import gcs


def _record(mirror, folder, cid, name, country, files, coverage, isin=()):
    d = mirror / folder
    d.mkdir(parents=True)
    rec = {"company_id": cid, "name": name, "country": country,
           "identifiers": {"isin": list(isin), "lei": None},
           "files": files, "coverage": {"fy2025": coverage}}
    (d / "metadata.json").write_text(json.dumps(rec), encoding="utf-8")


def _file(name, covers, fmt="pdf", current=True):
    return {"file_name": name, "fiscal_year": "fy2025", "covers": covers, "format": fmt,
            "is_current": current}


def _cov(status, file=None, covered_by=None):
    return {"status": status, "file": file, "covered_by": covered_by}


def test_match_and_documents(tmp_path):
    _record(tmp_path, "nordics/se/listed/seb-c-523d13d0--seb", "seb-c-523d13d0", "SEB C", "se",
            [_file("ar.xhtml", ["annual-report"], "esef_xhtml"), _file("ar.pdf", ["annual-report"]),
             _file("rem.pdf", ["remuneration-report"]), _file("old.pdf", ["annual-report"], current=False)],
            {"annual-report": _cov("found", "ar.xhtml"), "remuneration-report": _cov("found", "rem.pdf")})
    _record(tmp_path, "nordics/fi/listed/ponsse-oyj-69c36e97--ponsse", "ponsse-oyj-69c36e97",
            "Ponsse Oyj", "fi", [_file("p.pdf", ["annual-report", "remuneration-report"])],
            {"annual-report": _cov("found", "p.pdf"),
             "remuneration-report": _cov("covered_by", covered_by="p.pdf")}, isin=["FI0009005078"])
    recs = gcs.records(tmp_path)
    m = gcs.Matcher(recs)
    assert m(tracker_id="seb-c")[1] == "id without its suffix"
    assert m(name="Ponsse 1", country="FI")[1] == "name"           # share-series number
    assert m(isin="fi0009005078")[1] == "ISIN"
    assert m(name="Nobody AB", country="SE") == (None, "not in the bucket")
    seb = gcs.documents(m(tracker_id="seb-c")[0])
    assert seb["annual"].endswith("/seb-c-523d13d0--seb/fy2025/ar.pdf")   # PDF over ESEF
    assert seb["remuneration"].endswith("/fy2025/rem.pdf")
    ponsse = gcs.documents(m(isin="FI0009005078")[0])
    assert ponsse["annual"].endswith("/p.pdf") and ponsse["remuneration"] is None


def test_gs_link_in_the_input_is_read_like_a_file(tmp_path, monkeypatch):
    monkeypatch.setattr(gcs, "CACHE", tmp_path / "gcs")
    uri = "gs://b/uploads/nordics/se/listed/x--x/fy2025/Annual Report 2025.pdf"
    csv = tmp_path / "in.csv"
    csv.write_text(f"company_id,company_name,annual_report_url\nx,X AB,{uri}\n", encoding="utf-8")
    t = dp.read_targets(csv)[0]
    assert t.annual_report_url.startswith("file:") and t.company.report_url == t.annual_report_url
    assert t.gcs == {t.annual_report_url: uri}
    steps = dict(dp.plan(t, {"apis": True, "docs": False, "pipeline_credits": 8, "doc_credits": 10,
                             "retry_failed": False}))
    assert steps.get("report step (file given)") == 0 and "report search" not in steps
    # a download that fails drops the link: the report is searched for instead
    monkeypatch.setattr(gcs, "ensure", lambda sources: ["boom"])
    dp.fetch_bucket_files(t)
    assert t.annual_report_url is None and t.company.report_url is None


def test_bucket_only_runs_bucket_companies_without_firecrawl(tmp_path, monkeypatch, capsys):
    from extractor.batch import Company
    monkeypatch.setattr(gcs, "CACHE", tmp_path / "gcs")
    monkeypatch.setattr(dp, "DP_DIR", tmp_path / "dp")
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.company_id}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.company_id}.err"))
    ar = "gs://b/uploads/nordics/se/listed/a--a/fy2025/Annual Report 2025.pdf"
    rem = "gs://b/uploads/nordics/se/listed/b--b/fy2025/Remuneration Report 2025.pdf"
    csv = tmp_path / "in.csv"
    csv.write_text("company_id,company_name,annual_report_url,remuneration_report_url\n"
                   f"a,A AB,{ar},\nb,B AB,,{rem}\nc,C AB,,\n", encoding="utf-8")
    assert dp.main([str(csv), "--dry-run", "--bucket-only"]) == 0
    out = capsys.readouterr().out
    assert "1 companies skipped: no report of theirs in the bucket (c)" in out
    assert "a A AB" in out and "b B AB" in out and "C AB" not in out.split("skipped")[-1]
    assert "report (no annual report in the bucket: not searched)" in out    # b
    assert "company documents" not in out and "at most 0 Firecrawl credits" in out


def test_bucket_only_gaps_say_the_website_was_not_searched():
    from extractor.failures import Failure, classify
    note = "not found in: GLEIF, Annual report (PDF), company website (not searched: bucket only)"
    row = {"grain": "company", "data_point": "listing_date", "value": "", "note": note}
    assert classify(row) is Failure.WEBSITE_NOT_SEARCHED
    row["note"] = "remuneration report not searched: bucket only"
    assert classify({**row, "grain": "role"}) is Failure.WEBSITE_NOT_SEARCHED
    row["note"] = "not derived: no share price"
    assert classify(row) is Failure.DERIVATION_INPUT_MISSING
