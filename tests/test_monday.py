"""Monday table: sample picking and golden comparison."""

import json

from extractor import monday
from extractor.batch import Company


def _g(field, value, year="2025", currency="EUR", unit="millions"):
    return {"field": field, "value": str(value), "unit": unit, "currency": currency,
            "year": year, "fiscal_year": year}


def test_compare_money_rounding_year_and_currency():
    ours = {"value_full": 19_889_000_000, "currency": "EUR"}
    assert monday.compare_money(ours, [_g("revenue", 19889)], "2025")[0] == "confirmed"
    assert monday.compare_money(ours, [_g("revenue", 19889.4)], "2025")[0] == "confirmed"
    assert monday.compare_money(ours, [_g("revenue", 21000)], "2025")[0] == "differs"
    out, why = monday.compare_money(ours, [_g("revenue", 19889, year="2024")], "2025")
    assert out == "skipped" and "golden year 2024" in why
    assert monday.compare_money(ours, [_g("revenue", 19889, currency="USD")], "2025")[0] == "skipped"
    assert monday.compare_money(ours, [], "2025") == ("skipped", "no golden value")


def test_pick_sample_is_stratified_scorable_first_and_repeatable():
    golden = {f"n{i}": {"lei": [{}]} for i in range(10)}
    golden |= {f"s{i}": {"revenue": [{}]} for i in range(3)}
    cs = ([Company(f"n{i}", "N", "SE", "nordic_listed") for i in range(10)]
          + [Company(f"s{i}", "S", "SE", "nordic_listed") for i in range(3)]
          + [Company("x", "X", "SE", "nordic_listed")]                       # not in golden
          + [Company("o1", "O", "US", "other_unlisted_or_unknown")])         # scrape route
    golden["o1"] = {"revenue": [{}]}
    a = monday.pick_sample(cs, golden, 5)
    assert len(a) == 5 and {c.company_id for c in a[:3]} == {"s0", "s1", "s2"}
    assert all(c.segment == "nordic_listed" for c in a)
    assert [c.company_id for c in a] == [c.company_id for c in monday.pick_sample(cs, golden, 5)]


def test_build_table_rows(tmp_path):
    cs = [Company("a", "A Oyj", "FI", "nordic_listed"), Company("b", "B AB", "SE", "nordic_listed"),
          Company("c", "C AB", "SE", "nordic_listed")]
    res = {"company_id": "a", "fiscal_year": "2025", "data_source": "esef",
           "revenue": {"value_full": 1e9, "currency": "EUR", "method": "xbrl_tag"},
           "total_assets": {"value_full": None},
           "revenue_model": {"categories": ["product_sales"]},
           "business_structure": {"segments": ["X"]},
           "checks": [{"name": "quote", "target": "revenue_model", "result": "pass"},
                      {"name": "quote", "target": "business_structure", "result": "fail"}]}
    (tmp_path / "a.json").write_text(json.dumps(res))
    (tmp_path / "b.error.json").write_text("{}")
    golden = {"a": {"revenue": [_g("revenue", 1000)]}}
    rows = {(r["field"], r["segment"]): r for r in monday.build_table(cs, golden, tmp_path)}
    rev = rows[("revenue", "nordic_listed")]
    assert (rev["companies_tested"], rev["found"], rev["checked"], rev["confirmed"]) == (2, 1, 1, 1)
    assert rev["coverage_pct"] == "50.0" and "1 read from XBRL tags" in rev["notes"]
    assert rows[("business_structure", "nordic_listed")]["confirmed"] == 0
    assert rows[("employees_fte", "nordic_listed")]["recommendation"] == "NOT_TESTED"
