"""Weak links on the High-severity fields (11 Nov 2026): headcount from FTE, an undated
share price, re-scoring a run cached partly elsewhere, the workbook's severities."""

import csv
import json

from extractor import dashboard
from extractor import datapoints as dp
from extractor import output_checks as oc
from extractor.apis import Found


class NoSources:
    def pages(self, endpoint):
        return None


def _row(name, value="", note="", **kw):
    return {"company_id": "acme", "company_name": "Acme", "segment": "", "country": "SE", "lei": "",
            "grain": "company", "role_row": "", "data_point": name, "value": value, "unit": "",
            "period_end": "", "source": "", "endpoint": "", "method": "", "retrieved_at": "",
            "confidence": "", "note": note, "scraper_version": "1"} | kw


def test_fte_is_the_headcount_when_none_is_stated():
    fte = _row("fte", "1234.5", 'PDF page 9: "Average FTEs 1,234.5"', unit="employees",
               period_end="2025-12-31", source="Annual report (PDF)", method="PARSE", confidence="B",
               endpoint="https://x.com/ar.pdf#page=9")
    rows = dp.refresh([_row("headcount", note="not found in: Annual report (PDF)"), fte])
    hc = rows[0]
    assert (hc["value"], hc["method"], hc["confidence"], hc["period_end"]) == ("1235", "DERIVED", "B", "2025-12-31")
    assert hc["note"].startswith(dp.FROM_FTE + ", rounded from 1234.5; printed 1234.5;")
    checks = {x.check: x for x in oc.score_row(oc.Row(hc), oc.Ctx(NoSources(), dict(oc.DEFAULT_RANGES), []))
              .results if x.check in ("DER-03", "DER-06", "NUM-05", "CORE-02")}
    assert all(x.outcome != "fail" for x in checks.values()), checks
    assert checks["DER-03"].outcome == checks["NUM-05"].outcome == "pass"
    # a stated headcount stays; a run limited to other fields leaves it alone
    stated = dp.refresh([_row("headcount", "900", method="PARSE"), dict(fte)])
    assert stated[0]["value"] == "900"
    skipped = dp.refresh([_row("headcount", note=dp.selection.NOT_COLLECTED + "pay"), dict(fte)])
    assert skipped[0]["value"] == ""


def test_an_undated_share_price_takes_the_fiscal_year_end(monkeypatch):
    monkeypatch.setattr(dp.fx, "eur_rate", lambda cur, date: (0.85, "2025-12-31") if date == "2025-12-31" else None)
    shares = Found("shares_outstanding", 1e9, unit="shares", source="AR", confidence="B")
    price = Found("share_price", 4.0, unit="GBP", source="AR", confidence="B")
    band, why = dp.market_cap_band({"shares_outstanding": shares, "share_price": price})
    assert band is None and "unknown date" in why
    fye = Found("fiscal_year_end", "2025-12-31", source="AR", confidence="B")
    band, _ = dp.market_cap_band({"shares_outstanding": shares, "share_price": price, "fiscal_year_end": fye})
    assert band.value == "large" and band.period_end == "2025-12-31"
    assert "the price has no date: the rate of the fiscal year end 2025-12-31" in band.note


def test_rescoring_keeps_saved_results_for_sources_not_cached_here(tmp_path):
    run, checks = tmp_path / "run.csv", tmp_path / "run_checks.csv"
    quote = 'PDF page 9: "Average FTEs 120"'
    rows = [_row("fte", "120", quote, unit="employees", period_end="2025-12-31", method="PARSE",
                 confidence="B", source="AR", endpoint="https://x.com/ar.pdf#page=9"),
            _row("headcount", "120", f"{dp.FROM_FTE}; {quote}", unit="employees", period_end="2025-12-31",
                 method="DERIVED", confidence="B", source="AR", endpoint="https://x.com/ar.pdf#page=9"),
            _row("pay_currency", "USD", 'PDF page 3: "US$"', method="PARSE", confidence="B", period_end="2025-12-31",
                 endpoint="https://x.com/ar.pdf#page=3")]
    with open(run, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(checks, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["company_id", "data_point", "role_row", "value", "status",
                                          "score", "check", "outcome", "reason"])
        w.writeheader()
        w.writerow({"company_id": "acme", "data_point": "fte", "role_row": "", "value": "120",
                    "status": "Fail (hard)", "score": "90", "check": "CORE-03", "outcome": "fail",
                    "reason": "quote not in the source text"})
        w.writerow({"company_id": "acme", "data_point": "pay_currency", "role_row": "", "value": "US$",
                    "status": "Pass", "score": "100", "check": "CORE-03", "outcome": "pass", "reason": ""})

    fresh = {s.row.data_point: s for s in oc.run(run, NoSources(), dict(oc.DEFAULT_RANGES))[0]}
    assert fresh["fte"].status == "Pass"                        # CORE-03 n/a: unchecked here
    kept = {s.row.data_point: s for s in oc.rescore(run, checks, NoSources(), dict(oc.DEFAULT_RANGES))[0]}
    assert kept["fte"].status == "Fail (hard)"                  # the quote check made elsewhere
    assert kept["headcount"].status == "Fail (hard)"            # the FTE's check, same quote
    cur = next(x for x in kept["pay_currency"].results if x.check == "CORE-03")
    assert cur.outcome == "pass" and kept["pay_currency"].status == "Pass"   # "US$" now "USD"


def test_the_dashboard_takes_severity_and_requirement_from_the_workbook(tmp_path, monkeypatch):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps([{"d": "sector_code"}, {"d": "lei"}]))
    reqs = tmp_path / "reqs.json"
    reqs.write_text(json.dumps({"fields": [{"d": "sector_code", "req": "Optional", "sev": "Medium",
                                            "why": "old"}, {"d": "lei", "req": "Optional", "sev": "Low"}]}))
    ranks = tmp_path / "ranks.json"
    ranks.write_text(json.dumps({"fields": [{"d": "sector_code", "rank": 10, "sev": "High",
                                             "req": "Required"}, {"d": "lei", "rank": 31}]}))
    monkeypatch.setattr(dashboard, "FIELDS_LIST", fields)
    monkeypatch.setattr(dashboard, "FIELD_REQUIREMENTS", reqs)
    monkeypatch.setattr(dashboard, "BENCHMARK_RANK", ranks)
    got = {f["d"]: f for f in dashboard.fields_list()}
    assert (got["sector_code"]["sev"], got["sector_code"]["req"], got["sector_code"]["rank"]) == ("High", "Required", 10)
    assert got["sector_code"]["why"] == "old"                  # kept where the workbook gives none
    assert (got["lei"]["sev"], got["lei"]["rank"]) == ("Low", 31)


def _origin(cover="Geschäftsbericht 2025", n=60):
    from extractor.scraper import Page
    pages = [Page(1, cover)] + [Page(i, "text") for i in range(2, n + 1)]
    return dp.Origin("pdf", "https://x.com/gb-2025.pdf", "Annual report (PDF)", "PARSE", "", pages, {})


def test_a_report_without_figures_still_gives_its_year():
    result = {"fiscal_year": "2025", "period_end_date": "2025-12-31", "revenue": {}, "total_assets": {}}
    got = {f.data_point: f for f in dp.from_result(result, _origin())}
    assert got["fiscal_year"].value == "2025" and got["fiscal_year"].source == "Annual report (PDF)"
    assert got["fiscal_year_end"].value == "2025-12-31" and "reporting_currency" not in got


def test_a_missing_fiscal_year_comes_from_the_year_end_or_the_title():
    result = {"fiscal_year": None, "period_end_date": "2026-03-31"}
    f = dp.year_of_report(result, _origin(), [])[0]
    assert (f.value, f.method) == ("2025/26", "DERIVED") and result["fiscal_year"] == "2025/26"
    result = {"fiscal_year": None, "period_end_date": None}
    f = dp.year_of_report(result, _origin(), [])[0]
    assert f.value == "2025" and "title" in f.note
    assert dp.year_of_report({"fiscal_year": None}, _origin("Contents"), []) == []
    assert dp.year_of_report({"fiscal_year": "2024"}, _origin(), []) == []


def test_a_filings_search_url_gives_the_lei_not_a_report(tmp_path):
    p = tmp_path / "in.csv"
    p.write_text("company_id,company_name,country,annual_report_url\n"
                 "k2a,K2A,SE,https://filings.xbrl.org/api/filings?filter[entity.identifier]=549300Q62J8QZJ5TGJ71\n"
                 "sed,SED,NO,https://filings.xbrl.org/api/filings?filter%5Bentity.identifier%5D=213800ED88L967PGFK25\n",
                 encoding="utf-8")
    k2a, sed = dp.read_targets(p)
    assert k2a.company.lei == "549300Q62J8QZJ5TGJ71" and k2a.annual_report_url is None
    assert sed.company.lei == "213800ED88L967PGFK25"


def test_a_figure_in_a_table_drawn_cell_by_cell_is_found_in_its_own_cell():
    from extractor.validate import lone_cell
    page = ("<!-- Start of picture text -->\nFixed  Performance<br>compensation based<br>"
            "<!-- End of picture text -->\n\nRemuneration of the Management Board in thousand euro\n\n"
            "<!-- Start of picture text -->\n1,186.8<br>"
            "<!-- End of picture text -->\n\n<!-- Start of picture text -->\n452.2<br><!-- End of picture text -->")
    texts = [(152, "Notes"), (153, page)]
    assert lone_cell("Fixed compensation 1,186.8", 1186.8, texts) == ("1,186.8<br><!-- End of picture text -->", 153)
    assert lone_cell("Variable pay 1,186.8", 1186.8, texts) is None          # words not on the page
    assert lone_cell("Fixed compensation 1,186.8", 1186.8, texts + [(160, "1,186.8")]) is None   # twice
    assert lone_cell("Fixed compensation 1,186.8", 1186.8, [(9, "Fixed compensation 1,186.8 was paid")]) is None
    origin_pages = [dp.Page(152, "Notes"), dp.Page(153, page)]
    o = dp.Origin("pdf", "https://x.com/ar.pdf", "Annual report (PDF)", "PARSE", "", origin_pages, {})
    endpoint, conf, where, quote = o.where("Fixed compensation 1,186.8", None, 1186.8)
    assert conf == "B" and endpoint.endswith("#page=153") and dp.LONE_CELL in where
    assert oc.Row({"note": where}).quote[0] == quote
