"""The dashboard's data (extractor/dashboard.py): report.json from the output checks."""

import csv
import json

from extractor import dashboard
from extractor import output_checks as oc

COLUMNS = ["company_id", "company_name", "segment", "country", "lei", "grain", "role_row", "data_point",
           "value", "unit", "period_end", "source", "endpoint", "method", "retrieved_at", "confidence", "note"]
LEI = "549300HX9MRFY47AH564"


def _csv(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({"company_id": "T1", "company_name": "Acme AB", "country": "SE", "lei": LEI,
                        "grain": "company", "endpoint": "https://example.com/ar.pdf#page=3",
                        "method": "PARSE", **r})
    return path


ROWS = [
    {"data_point": "legal_name", "value": "Acme AB", "method": "API", "endpoint": "https://api.gleif.org/x"},
    {"data_point": "revenue", "value": "1000000", "unit": "SEK", "period_end": "2025-12-31",
     "note": 'printed 1000 thousands; PDF page 3: "Net sales 1,000"'},
    {"data_point": "headcount", "value": "12.5", "period_end": "2025-12-31",
     "note": 'PDF page 3: "Employees 12.5"'},                            # not whole: NUM-05 hard fail
    {"data_point": "ebitda", "value": ""},
    {"grain": "role", "role_row": "CEO", "data_point": "base_salary", "value": "500000", "unit": "SEK",
     "note": 'printed 500 thousands; PDF page 3: "CEO | 500"'},          # no period: partial
]


def _build(tmp_path, monkeypatch, rows=ROWS):
    monkeypatch.setattr(oc, "Sources", lambda cache, results: type("S", (), {"pages": lambda s, e: None})())
    out = tmp_path / "Dashboard"
    html = dashboard.build(_csv(tmp_path / "run_datapoints.csv", rows), out=out)
    return json.loads((out / "report.json").read_text(encoding="utf-8")), html


def test_report_json_follows_the_spec(tmp_path, monkeypatch):
    data, html = _build(tmp_path, monkeypatch)
    m = data["meta"]
    assert (m["tracker"], m["rows"], m["filled"], m["companies"], m["countries"]) == \
        ("run_datapoints.csv", 5, 4, 1, ["SE"])
    assert data["gateIds"] == [oc.CHECK_ID[fn] for fn, _, _ in oc.CHECKS]
    assert data["gates"]["NUM-05"] == ["Counts are whole numbers", "Hard"]
    by = {v["d"]: v for v in data["values"]}
    assert by["legal_name"]["ck"] == LEI and by["legal_name"]["f"] == "C01"
    assert by["headcount"]["sc"] == "H"
    gi = data["gateIds"].index("NUM-05")
    assert [gi, "F"] == by["headcount"]["gr"][[g[0] for g in by["headcount"]["gr"]].index(gi)][:2]
    assert by["revenue"]["st"] == "found" and by["base_salary"]["st"] == "partial"
    assert by["ebitda"]["st"] == "not_found" and "gr" not in by["ebitda"]
    assert all(g[1] in ("P", "F") for v in data["values"] if "gr" in v for g in v["gr"])   # n/a left out
    assert data["baseline"]["label"] == "This run"
    page = html.read_text(encoding="utf-8")
    assert "var DATA = " in page and "/*__DATA__*/" not in page and "/*__CORE__*/" not in page
    assert (tmp_path / "run_datapoints_checks.md").exists()


def test_not_applicable_is_neither_found_nor_missing(tmp_path, monkeypatch):
    rows = ROWS + [{"grain": "role", "role_row": "CEO", "data_point": "aggregate_headcount",
                    "note": "not applicable: one person"}]
    data, _ = _build(tmp_path, monkeypatch, rows)
    by = {v["d"]: v for v in data["values"]}
    assert by["aggregate_headcount"]["st"] == "not_applicable"
    found = sum(v["st"] == "found" for v in data["values"])
    assert data["meta"]["foundPct"] == round(100 * found / (len(rows) - 1), 1)


def test_the_previous_run_becomes_the_baseline(tmp_path, monkeypatch):
    first, _ = _build(tmp_path, monkeypatch, ROWS[:2])
    second, _ = _build(tmp_path, monkeypatch)
    assert second["baseline"]["checksPct"] == first["meta"]["checksPct"]
    assert second["baseline"]["label"].startswith("Previous run (run_datapoints.csv")


def test_several_runs_show_as_one_with_their_saved_checks(tmp_path, monkeypatch):
    first, _ = _build(tmp_path, monkeypatch)    # scores run_datapoints.csv and saves its checks
    other = [dict(r, company_id="T2") for r in ROWS]
    b = tmp_path / "b_datapoints.csv"
    with b.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in other:
            w.writerow({"company_name": "Beta AB", "country": "NO", "grain": "company",
                        "endpoint": "https://example.com/b.pdf#page=3", "method": "PARSE", **r})
    s, _ = oc.run(b, oc.Sources(None, None), dict(oc.DEFAULT_RANGES))
    oc.write_csv(s, tmp_path / "b_datapoints_checks.csv")
    monkeypatch.setattr(oc, "run", lambda *a: (_ for _ in ()).throw(AssertionError("scored again")))
    out = tmp_path / "Dashboard"
    dashboard.build([tmp_path / "run_datapoints.csv", b], out=out, saved_checks=True)
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    m = data["meta"]
    assert (m["tracker"], m["companyIds"], m["rows"], m["filled"]) == \
        ("run_datapoints.csv + b_datapoints.csv", 2, 10, 8)
    assert m["checksPct"] == first["meta"]["checksPct"]   # same values, same saved outcomes
    by = {(v["id"], v["d"]): v for v in data["values"]}
    assert by[("T2", "headcount")]["sc"] == "H" and by[("T1", "headcount")]["sc"] == "H"


def test_a_field_the_tracker_did_not_ask_for_is_not_counted_as_not_found():
    from extractor import dashboard
    from extractor import output_checks as oc
    f = {"field_id": "", "category": "Financials"}
    skipped = oc.Row({"value": "", "note": "not collected: this run asked only for pay"})
    missing = oc.Row({"value": "", "note": "not found in: Annual report (PDF)"})
    assert dashboard.value_status(skipped, f) == "not_applicable"
    assert dashboard.value_status(missing, f) == "not_found"
