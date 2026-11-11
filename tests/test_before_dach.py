"""Before the DACH runs: merging runs safely, unlocked PDFs, input checks, code changes."""

import csv
from pathlib import Path

from extractor import combine
from extractor import datapoints as dp
from extractor.batch import Company
from extractor.fields import NOT_COLLECTED

CHECK_COLS = ["company_id", "data_point", "role_row", "value", "status", "score", "check", "outcome", "reason"]


def _row(cid, name, value="", grain="company", role="", note=""):
    return {c: "" for c in dp.COLUMNS} | {"company_id": cid, "grain": grain, "role_row": role,
                                          "data_point": name, "value": value, "note": note}


def _check(cid, name, value, outcome="pass", role=""):
    return {"company_id": cid, "data_point": name, "role_row": role, "value": value, "status": "Pass",
            "score": "100", "check": "CORE-03", "outcome": outcome, "reason": ""}


def _write(path: Path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _read(path: Path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def test_combine_replaces_companies_in_place_and_keeps_what_a_run_did_not_collect(tmp_path):
    into, run = tmp_path / "all_datapoints.csv", tmp_path / "run_datapoints.csv"
    _write(into, [_row("a", "revenue", "100"), _row("a", "headcount", "50"),
                  _row("a", "base_salary", "9", "role", "CEO"),
                  _row("b", "revenue", "7")], dp.COLUMNS)
    _write(tmp_path / "all_datapoints_checks.csv", [_check("a", "revenue", "100", "fail"),
                                                   _check("a", "headcount", "50"),
                                                   _check("b", "revenue", "7")], CHECK_COLS)
    # a pay-only run of a: its company rows weren't collected, except headcount
    _write(run, [_row("a", "revenue", note=NOT_COLLECTED + "pay"), _row("a", "headcount", "60"),
                 _row("a", "base_salary", "10", "role", "CEO"), _row("c", "revenue", "3")], dp.COLUMNS)
    _write(tmp_path / "run_datapoints_checks.csv", [_check("a", "headcount", "60"),
                                                   _check("c", "revenue", "3")], CHECK_COLS)
    stats = combine.combine([run], into)
    assert stats == {"replaced": 1, "added": 1, "kept": 1}
    rows = _read(into)
    assert [(r["company_id"], r["data_point"], r["value"]) for r in rows] == [
        ("a", "revenue", "100"), ("a", "headcount", "60"), ("a", "base_salary", "10"),
        ("b", "revenue", "7"), ("c", "revenue", "3")]
    checks = {(c["company_id"], c["data_point"]): c for c in _read(tmp_path / "all_datapoints_checks.csv")}
    assert checks[("a", "revenue")]["outcome"] == "fail"          # kept with its value
    assert checks[("a", "headcount")]["value"] == "60"            # the run's
    assert ("c", "revenue") in checks and ("b", "revenue") in checks


def test_combine_keeps_the_old_pay_rows_when_a_run_collected_no_pay(tmp_path):
    into, run = tmp_path / "all.csv", tmp_path / "run.csv"
    _write(into, [_row("a", "revenue", "100"), _row("a", "base_salary", "9", "role", "CEO")], dp.COLUMNS)
    _write(run, [_row("a", "revenue", "110"),
                 _row("a", "role_disclosure", grain="role", note=NOT_COLLECTED + "company")], dp.COLUMNS)
    combine.combine([run], into)
    assert [(r["data_point"], r["value"]) for r in _read(into)] == [("revenue", "110"), ("base_salary", "9")]


def test_a_copy_protected_pdf_is_read_from_an_unlocked_copy(tmp_path):
    import pymupdf
    from extractor import pay_tables
    pdf = tmp_path / "locked.pdf"
    doc = pymupdf.open()
    doc.new_page().insert_text((72, 72), "Base salary 1,000")
    doc.save(pdf, encryption=pymupdf.PDF_ENCRYPT_AES_256, owner_pw="owner", user_pw="",
             permissions=pymupdf.PDF_PERM_PRINT)
    out = pay_tables.unlocked(pdf)
    assert out and out.exists()
    with pymupdf.open(out) as copy:
        assert not copy.is_encrypted and "Base salary" in copy[0].get_text()
    assert pay_tables.unlocked(pdf) == out                      # made once


def test_input_problems_flag_login_links_and_companies_found_by_name_only():
    t = dp.Target(Company("x", "X AG", "CH"), annual_report_url="https://drive.google.com/file/d/1/view")
    assert any("needs a login (drive.google.com)" in p for p in dp.input_problems(t))
    assert any("no LEI and no ISIN" in p for p in dp.input_problems(t))
    ok = dp.Target(Company("y", "Y AG", "CH", lei="529900ABCDEFGHIJKL12"),
                   annual_report_url="https://y.ch/geschaeftsbericht-2025.pdf")
    assert dp.input_problems(ok) == []


def test_a_change_to_the_code_during_a_run_is_reported(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(dp, "code_fingerprint", lambda: "after")
    assert dp.warn_if_code_changed("before") == "after"
    assert "changed while this run is going" in capsys.readouterr().out
    assert dp.warn_if_code_changed("after") == "after"
    assert capsys.readouterr().out == ""


def test_gleif_waits_as_long_as_it_is_told_on_too_many_requests(monkeypatch):
    import httpx
    from extractor import lei
    calls, slept = [], []
    monkeypatch.setattr(lei, "_MIN_INTERVAL_S", 0)
    monkeypatch.setattr(lei._get.retry, "sleep", lambda s: slept.append(s))

    def fake_get(url, params=None, headers=None, timeout=None):
        calls.append(url)
        req = httpx.Request("GET", url)
        if len(calls) < 3:
            return httpx.Response(429, headers={"retry-after": "40"}, request=req)
        return httpx.Response(200, json={"data": []}, request=req)
    monkeypatch.setattr(lei.httpx, "get", fake_get)
    assert lei.fetch_by_lei("529900ABCDEFGHIJKL12") is None
    assert len(calls) == 3 and slept == [41, 41]
