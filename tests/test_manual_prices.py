"""Phase C: year-end share prices entered by hand (extractor/manual_prices.py)."""

import csv

from extractor import combine
from extractor import datapoints as dp
from extractor import manual_prices as mp
from tests.test_before_dach import _read, _row, _write

MISSING = "not found in: Annual report (PDF)"
BAND_MISSING = "not derived: no share price"


def _company(cid, price="", fye="2025-12-31", shares="10000000"):
    return [_row(cid, "share_price", price, note="" if price else MISSING),
            _row(cid, "fiscal_year_end", fye), _row(cid, "shares_outstanding", shares),
            _row(cid, "isin", "GRS000000001"), _row(cid, "market_cap_band", note=BAND_MISSING)]


def _fill(sheet, **values):
    rows = _read(sheet)
    for r in rows:
        r.update(values.get(r["company_id"], {}))
    _write(sheet, rows, mp.INFO + mp.FILL)


def test_the_sheet_lists_companies_with_no_price_and_keeps_what_was_filled_in(tmp_path):
    into, sheet = tmp_path / "all.csv", tmp_path / "sheet.csv"
    _write(into, _company("a") + _company("b", "4.2") + _company("c"), dp.COLUMNS)
    assert mp.build(into, sheet) == (2, 0 + 2)
    rows = _read(sheet)
    assert [r["company_id"] for r in rows] == ["a", "c"]
    assert rows[0]["isin"] == "GRS000000001" and "on or before 2025-12-31" in rows[0]["price_wanted"]
    _fill(sheet, a={"share_price": "1.5"})
    assert mp.build(into, sheet) == (2, 0)
    assert _read(sheet)[0]["share_price"] == "1.5"


def test_a_filled_price_is_loaded_and_gives_the_band(tmp_path):
    into, sheet = tmp_path / "all.csv", tmp_path / "sheet.csv"
    _write(into, _company("a") + _company("b"), dp.COLUMNS)
    mp.build(into, sheet)
    _fill(sheet, a={"share_price": "20", "currency": "EUR", "price_date": "2025-12-30",
                    "source_url": "https://www.a.gr/investors/share", "entered_by": "DM"})
    stats = mp.load(sheet, into)
    assert stats["loaded"] == ["a"] and not stats["refused"]
    by = {(r["company_id"], r["data_point"]): r for r in _read(into)}
    p = by[("a", "share_price")]
    assert (p["value"], p["unit"], p["period_end"], p["method"], p["confidence"]) == (
        "20", "EUR", "2025-12-30", "MANUAL", "B")
    assert p["endpoint"] == "https://www.a.gr/investors/share" and "by DM" in p["note"]
    band = by[("a", "market_cap_band")]
    assert band["value"] == "mid" and band["method"] == "DERIVED"     # 10m x 20 EUR = 200m
    assert by[("b", "market_cap_band")]["value"] == ""


def test_rows_that_fail_the_checks_are_refused():
    fye = "2025-12-31"
    ok = {"share_price": "1,234.5", "currency": "EUR", "price_date": "2025-12-30",
          "source_url": "https://x.com/share"}
    assert mp.check(ok, fye)[0]["value"] == "1234.5"
    assert mp.check(ok | {"share_price": "12,5"}, fye)[0]["value"] == "12.5"
    for bad, why in (({"share_price": "-1"}, "positive"), ({"currency": "euro"}, "ISO 4217"),
                     ({"price_date": "2026-01-02"}, "after the fiscal year end"),
                     ({"price_date": "2025-10-01"}, "more than 31 days"),
                     ({"price_date": "30/12/2025"}, "YYYY-MM-DD"), ({"source_url": "a.com"}, "http")):
        new, reason = mp.check(ok | bad, fye)
        assert new is None and why in reason, bad
    assert "older report" in mp.check(ok | {"price_date": "2024-12-30"}, "2024-12-31")[1]
    assert mp.check(ok, "")[0] and "not in FY2025" in mp.check(ok | {"price_date": "2024-12-30"}, "")[1]
    assert mp.price_wanted("2023-12-31").startswith("skip")
    pence, _ = mp.check(ok | {"share_price": "140.65", "currency": "GBp"}, fye)
    assert (pence["value"], pence["unit"]) == ("1.4065", "GBP") and "pence" in pence["note"]


def test_a_price_a_run_read_is_not_replaced_without_asking(tmp_path):
    into, sheet = tmp_path / "all.csv", tmp_path / "sheet.csv"
    _write(into, _company("a"), dp.COLUMNS)
    mp.build(into, sheet)
    rows = _read(into)
    rows[0].update(value="3", source="Annual report (PDF)", method="PARSE", note="")
    _write(into, rows, dp.COLUMNS)
    _fill(sheet, a={"share_price": "20", "currency": "EUR", "price_date": "2025-12-30",
                    "source_url": "https://www.a.gr/share"})
    stats = mp.load(sheet, into)
    assert stats["skipped"] and _read(into)[0]["value"] == "3"


def test_a_later_run_that_finds_no_price_keeps_the_one_entered_by_hand():
    old = [_row("a", "share_price", "20") | {"method": "MANUAL"}, _row("a", "revenue", "1")]
    new = [_row("a", "share_price", note=MISSING), _row("a", "revenue", "2")]
    rows, kept = combine.merge_company(old, new)
    assert [r["value"] for r in rows] == ["20", "2"]
    # a run that reads a price itself replaces it
    new[0]["value"] = "21"
    rows, _ = combine.merge_company(old, new)
    assert rows[0]["value"] == "21"


def test_a_rerun_that_misses_a_fact_keeps_the_old_value_unless_the_report_was_anothers():
    fye = _row("a", "fiscal_year_end", "2025-12-31")
    old = [_row("a", "revenue", "100") | {"period_end": "2025-12-31"},
           _row("a", "ebitda", "9") | {"period_end": "2024-12-31"}, fye]
    new = [_row("a", "revenue", note="not found in: Annual report (PDF)"),
           _row("a", "ebitda", note="not found in: Annual report (PDF)"), fye]
    rows, kept = combine.merge_company(old, new, keep_better=False)
    # revenue stays; the 2024 EBITDA is from another year and goes
    assert [r["value"] for r in rows] == ["100", "", "2025-12-31"]
    other = [r | {"note": "not found: the annual report was not read (OtherCompanysReport: ...)"}
             for r in new[:2]] + [fye]
    rows, _ = combine.merge_company(old, other, keep_better=False)
    assert [r["value"] for r in rows[:2]] == ["", ""]
