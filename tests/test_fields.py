"""Collecting only some data points (issue 16): --fields, run_required, merging rows."""

import json

import pytest

from extractor import datapoints as dp
from extractor import fields as sel
from extractor.batch import Company
from extractor.pay import ROLE_POINTS


def _row(name, value="", grain="company", role="", version="1", note=""):
    return {"company_id": "x", "company_name": "X", "segment": "", "country": "SE", "lei": "",
            "grain": grain, "role_row": role, "data_point": name, "value": value, "unit": "",
            "period_end": "", "source": "src" if value else "", "endpoint": "",
            "method": "PARSE" if value else "", "retrieved_at": "", "confidence": "B" if value else "",
            "note": note, "scraper_version": version}


def test_company_points_match_the_data_points():
    assert list(sel.COMPANY_POINTS) == dp.DATA_POINTS


def test_fields_are_names_or_groups_and_derived_values_bring_their_inputs():
    assert sel.parse(None) is None and sel.parse("all") is None
    assert sel.parse("revenue, headcount") == {"revenue", "headcount"}
    assert sel.parse("market_cap_band") == {"market_cap_band", "shares_outstanding", "share_price"}
    assert sel.parse("sector_code") == {"sector_code", "sub_sector"}
    pay = sel.parse("pay")
    assert set(ROLE_POINTS) <= pay and {"pension_type", "benefits"} <= pay and "revenue" not in pay
    company = sel.parse("company")
    assert "revenue" in company and "base_salary" not in company and "pension_type" not in company
    with pytest.raises(ValueError, match="unknown field 'revenu'"):
        sel.parse("revenu")


def test_run_required_follows_the_tracker():
    assert sel.from_run_required("Pay Data") == sel.parse("pay")
    assert sel.from_run_required("company  data") == sel.parse("company")
    assert sel.from_run_required("Company and Pay Data") is None
    assert sel.from_run_required("") is None
    # both given: what both ask for
    assert sel.combine(sel.parse("headcount,base_salary"), sel.parse("pay")) == {"base_salary"}
    assert sel.combine(sel.parse("headcount"), sel.parse("pay")) == frozenset()
    assert sel.combine(None, sel.parse("pay")) == sel.parse("pay")


def test_steps_follow_the_fields():
    api_only = sel.parse("isin,ticker,lei")
    assert not sel.needs_report(api_only) and not sel.needs_pay(api_only)
    assert not sel.needs_documents(api_only)
    assert sel.needs_report(sel.parse("pay")) and sel.needs_pay(sel.parse("pay"))
    assert not sel.needs_pay(sel.parse("company"))
    assert sel.needs_report(None) and sel.needs_pay(None) and sel.needs_documents(None)


def test_plan_skips_the_report_search_for_api_fields(tmp_path, monkeypatch):
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.company_id}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.company_id}.err"))
    opts = {"docs": True, "doc_credits": 10, "pipeline_credits": 6, "retry_failed": False}
    t = dp.Target(Company("n", "New AB", "SE"))
    assert dp.worst_case(t, opts) == 16
    t.fields = sel.parse("isin,ticker")
    assert dp.worst_case(t, opts) == 0
    assert [s for s, _ in dp.plan(t, opts)] == ["official APIs"]
    t.fields = sel.parse("pay")
    assert "executive pay" in [s for s, _ in dp.plan(t, opts)] and dp.worst_case(t, opts) == 16
    (tmp_path / "n.json").write_text(json.dumps({"fiscal_year": "2025"}))
    assert dp.worst_case(t, opts) == 10            # the report found before is reused


def test_merge_replaces_only_the_chosen_company_fields():
    old = [_row("revenue", "100", version="3"), _row("headcount", "50", version="3"),
           _row("role_disclosure", "individual", "role", "CEO", "3"),
           _row("base_salary", "1000", "role", "CEO", "3")]
    new = [_row("revenue", "", version="4", note="not found in: x"), _row("headcount", "60", version="4"),
           _row("ebitda", "7", version="4"),
           _row("role_disclosure", "", "role", "", "4", "not collected")]
    rows = {r["data_point"]: r for r in sel.merge(old, new, sel.parse("headcount"))}
    assert rows["headcount"]["value"] == "60" and rows["headcount"]["scraper_version"] == "4"
    assert rows["revenue"]["value"] == "100" and rows["revenue"]["scraper_version"] == "3"
    assert rows["ebitda"]["value"] == "" and rows["ebitda"]["note"].startswith(sel.NOT_COLLECTED)
    assert rows["base_salary"]["value"] == "1000"                   # pay rows kept
    assert sel.merge(old, new, None) == new


def test_merge_of_role_fields():
    old = [_row("role_disclosure", "individual", "role", "CEO"), _row("base_salary", "1000", "role", "CEO"),
           _row("lti_target", "", "role", "CEO"), _row("role_disclosure", "individual", "role", "CFO")]
    new = [_row("role_disclosure", "individual", "role", "CEO"), _row("base_salary", "1100", "role", "CEO"),
           _row("lti_target", "50", "role", "CEO")]
    rows = sel.merge(old, new, sel.parse("lti_target"))
    ceo = {r["data_point"]: r["value"] for r in rows if r["role_row"] == "CEO"}
    assert ceo == {"role_disclosure": "individual", "base_salary": "1000", "lti_target": "50"}
    assert any(r["role_row"] == "CFO" for r in rows)
    whole = sel.merge(old, new, sel.parse("pay"))
    assert [r for r in whole if r["grain"] == "role"] == new        # the whole block


def test_missing_lists_the_fields_without_a_value():
    rows = [_row("revenue", "100"), _row("headcount", "")]
    assert sel.missing(rows, frozenset({"revenue", "headcount", "lti_target"})) == ["headcount", "lti_target"]


def test_fields_top_up_only_companies_missing_them(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(dp, "DP_DIR", tmp_path / "dp")
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.company_id}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.company_id}.err"))
    (tmp_path / "dp").mkdir()
    (tmp_path / "dp" / "a.json").write_text(json.dumps([_row("headcount", "50")]))
    (tmp_path / "dp" / "b.json").write_text(json.dumps([_row("headcount", "")]))
    (tmp_path / "dp" / "c.json").write_text(json.dumps([_row("headcount", "")]))
    csv = tmp_path / "in.csv"
    csv.write_text("company_id,company_name,country,run_required\n"
                   "a,A AB,SE,Company Data\nb,B AB,SE,Company and Pay Data\nc,C AB,SE,Pay Data\n",
                   encoding="utf-8")
    assert dp.main([str(csv), "--fields", "headcount", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "] b B AB: fields headcount" in out and "] a A AB" not in out
    assert "1 companies skipped" in out                     # c needs pay only
    assert dp.main([str(csv), "--dry-run"]) == 0            # done before: nothing to do
    assert "Dry run: 0 companies" in capsys.readouterr().out
    assert dp.main([str(csv), "--dry-run", "--redo"]) == 0
    out = capsys.readouterr().out
    assert "c C AB: fields pay (run_required: Pay Data)" in out
    assert "a A AB: fields company" in out
    assert dp.main([str(csv), "--dry-run", "--redo", "--ignore-run-required"]) == 0
    assert "c C AB: fields all" in capsys.readouterr().out


def test_save_rows_merges_into_the_saved_file(tmp_path, monkeypatch):
    monkeypatch.setattr(dp, "DP_DIR", tmp_path)
    t = dp.Target(Company("x", "X AB", "SE"))
    dp.dp_path(t.company).write_text(json.dumps([_row("revenue", "100"), _row("headcount", "50")]))
    t.fields = sel.parse("headcount")
    dp.save_rows(t, [_row("revenue", ""), _row("headcount", "60")])
    saved = {r["data_point"]: r["value"] for r in json.loads(dp.dp_path(t.company).read_text())}
    assert saved == {"revenue": "100", "headcount": "60"}
