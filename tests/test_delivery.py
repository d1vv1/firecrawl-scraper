"""The Delivery pages' data (extractor/delivery.py, Dashboard/SPEC.md 6.4)."""

import csv
import json

import openpyxl

from extractor import delivery

HEAD = ["Company Name", "Country", "Region", "Tier", "ISIN", "LEI", "Pipeline Run", "Run required",
        "Find Required", "Company Data", "Company URL", "Remuneration Files", "Link", "Date",
        "Annual Reports", "Annual Link", "Date", "Pay Extracted ", "Company Data Extracted ", "Remarks"]


def _tracker(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Companies"
    ws.append(HEAD)
    for name, region, run, req, find, status in rows:
        ws.append([name, "SE", region, "Tier 1", None, None, run, req, find, None, None, None, None, None,
                   None, None, None, None, None, f"Status: {status}"])
    wb.save(path)


def _csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def _setup(tmp_path, monkeypatch, spot=None):
    monkeypatch.setattr(delivery, "PROJECT_ROOT", tmp_path)
    _tracker(tmp_path / "tracker.xlsx", [
        ("Alpha AB", "Nordics", "required", "Company Data", "NA", "Pay document held"),      # extracted, clean
        ("Beta AB", "Nordics", "required", "Company Data", "NA", "Pay document held"),       # extracted, fails
        ("Gamma AB", "Nordics", "required", "Company Data", "OpenAPI", "Still to find"),     # discovery
        ("Delta AB", "Nordics", "skip", "NA", "NA", "FY2025 not published yet"),             # exception only
    ])
    (tmp_path / "out").mkdir()
    (tmp_path / "in").mkdir()
    _csv(tmp_path / "out" / "run_datapoints.csv", ["company_id", "data_point", "value", "retrieved_at"],
         [["alpha-ab", "revenue", "10", "2026-11-10T08:00:00"], ["beta-ab", "revenue", "", "2026-11-10T08:00:00"]])
    _csv(tmp_path / "out" / "run_datapoints_checks.csv",
         ["company_id", "data_point", "role_row", "value", "status", "check", "outcome", "reason"],
         [["alpha-ab", "revenue", "", "10", "Pass", "CORE-01", "pass", ""],
          ["beta-ab", "revenue", "", "x", "Fail (hard)", "NUM-01", "fail", "unit 'kroner' is not ISO 4217"]])
    (tmp_path / "out" / "beta-ab.json").write_text(json.dumps(
        {"company_id": "beta-ab", "input_name": "Beta AB", "status": "ok", "fiscal_year": "2023",
         "extracted_at": "2026-11-10T09:00:00+00:00", "firecrawl_credits_used": 4}), encoding="utf-8")
    (tmp_path / "out" / "gamma-ab.error.json").write_text(json.dumps(
        {"company_id": "gamma-ab", "error_type": "ReportNotFoundError", "error": "none", "at": "2026-11-10T10:00:00+00:00",
         "firecrawl_credits_used": "2"}), encoding="utf-8")
    _csv(tmp_path / "in" / "spot_checks.csv", ["company_id", "batch", "data_point", "role_row", "reviewer", "checked_on", "result", "reason"],
         spot or [])
    _csv(tmp_path / "in" / "discovery.csv", ["company_id", "status", "next_step", "owner", "updated_on", "note"],
         [["Gamma AB", "in progress", "", "Divyanshu", "2026-11-10", ""]])
    cfg = {"fiscal_year": "2025",
           "sources": {"tracker": "tracker.xlsx", "datapoints_globs": ["out/*_datapoints.csv"],
                       "checks_globs": ["out/*_datapoints_checks.csv"], "run_outputs_dir": "out", "inputs_dir": "in"},
           "plan": {"baseline_remaining": 3, "baseline_date": "2026-11-09", "deadline": "2026-11-27", "daily_target": 1,
                    "working_days_only": True, "exceptions_acceptance_date": "2026-12-01", "pass_line": 0.95,
                    "batches": [{"name": "Nordics", "start": "2026-11-10", "end": "2026-11-12"}]},
           "required_fields": {"Company Data": ["revenue"]},
           "failure_categories": {"CORE-04": "Fiscal year not confirmed (no period end)"},
           "currency_reason_patterns": ["ISO 4217"],
           "firecrawl": {"credit_balance": None}}
    (tmp_path / "delivery.json").write_text(json.dumps(cfg), encoding="utf-8")
    return delivery.build(tmp_path / "delivery.json")


def test_stages_failures_discovery_exceptions(tmp_path, monkeypatch):
    d = _setup(tmp_path, monkeypatch)
    co = {c["id"]: c for c in d["companies"]}
    assert set(co) == {"alpha-ab", "beta-ab", "gamma-ab"}                       # skip rows are not required
    assert co["alpha-ab"]["stage"] == 4                                         # rules passed, not spot-checked
    assert co["beta-ab"]["stage"] == 2                                          # extracted, revenue empty
    assert co["gamma-ab"]["stage"] == 0                                         # document still to find
    assert co["beta-ab"]["fc"] == {"Wrong currency": 1, "Missing field": 1, "Wrong document": 1}
    assert co["beta-ab"]["fx"]["Wrong document"] == "Run read the FY2023 report, not FY2025"
    assert d["discovery"] == [{"id": "gamma-ab", "o": "Gamma AB", "c": "SE", "b": "Nordics", "need": "OpenAPI",
                               "next": "Open API: fetch company data", "owner": "Divyanshu", "status": "in progress",
                               "updated": "2026-11-10", "note": ""}]
    cats = {(e["id"], e["cat"]) for e in d["exceptions"]}
    assert cats == {("delta-ab", "No FY2025 report"), ("gamma-ab", "Document missing"), ("beta-ab", "Wrong document")}
    assert [(r["id"], r["status"], r["credits"]) for r in d["runs"]] == [("beta-ab", "ok", 4.0), ("gamma-ab", "failed", 2.0)]


def test_spot_check_clears_the_batch(tmp_path, monkeypatch):
    d = _setup(tmp_path, monkeypatch, spot=[["Alpha AB", "", "revenue", "", "QA", "2026-11-11", "pass", ""]])
    alpha = next(c for c in d["companies"] if c["id"] == "alpha-ab")
    assert alpha["stage"] == 6 and alpha["done"] == "2026-11-11"
    assert d["spotByBatch"]["Nordics"] == {"n": 1, "pass": 1, "last": "2026-11-11"}


def test_missing_tracker_does_not_raise(tmp_path, monkeypatch):
    monkeypatch.setattr(delivery, "PROJECT_ROOT", tmp_path)
    (tmp_path / "delivery.json").write_text(json.dumps({"sources": {"tracker": "nope.xlsx"}}), encoding="utf-8")
    assert "error" in delivery.build(tmp_path / "delivery.json")
