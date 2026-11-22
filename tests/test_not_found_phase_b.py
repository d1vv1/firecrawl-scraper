"""Phase B of docs/not_found_reduction_plan.md: extraction rules and the decided values
(D1, D4) they rest on."""

from extractor import datapoints as dp
from tests.test_before_dach import _row

MISSING = "not found in: GLEIF, Annual report (PDF), Remuneration report (PDF)"


def _by(rows):
    return {r["data_point"]: r for r in rows}


def _role(name, value, note="", role="CEO"):
    r = _row("a", name, value, "role", role,
             note or ("" if value else "not found in: Remuneration report (PDF)"))
    if value:
        r.update(unit="EUR", source="Remuneration report (PDF)", endpoint="https://x/rr.pdf#page=12",
                 period_end="2025-12-31")
    return r


# --- D4: a part folded into another amount ---------------------------------------------------

def test_a_pension_folded_into_benefits_is_included_not_missing():
    rows = [_role("base_salary", "500000"), _role("benefits_value", "80000", note="includes pension"),
            _role("pension_contribution", ""), _role("total_remuneration", "900000")]
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["note"] == "not applicable: included in benefits_value (pension)"


def test_the_total_including_everything_folds_nothing(monkeypatch):
    rows = [_role("base_salary", "500000"), _role("pension_contribution", ""),
            _role("total_remuneration", "900000", note="includes pension and benefits")]
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["note"].startswith("not found")
    monkeypatch.setenv("RULES_OFF", "included_in_other")
    rows = [_role("benefits_value", "1", note="includes pension"), _role("pension_contribution", "")]
    dp.refresh(rows)
    assert rows[1]["note"].startswith("not found")


# --- B2: no shareholding rule in a remuneration report read --------------------------------------

def _company(note=MISSING):
    return [_row("a", "shareholding_requirement", "", note=note), _role("base_salary", "500000")]


def test_no_shareholding_rule_in_the_remuneration_report_read_is_none():
    rows = _company()
    dp.refresh(rows)
    sr = rows[0]
    assert sr["value"] == "None" and sr["confidence"] == "C" and sr["method"] == "DERIVED"
    assert sr["endpoint"] == "https://x/rr.pdf" and sr["source"] == "Remuneration report (PDF)"
    assert sr["note"].startswith("derived: no shareholding requirement in the remuneration report read")


def test_no_none_without_a_remuneration_report_read(monkeypatch):
    # searched in the annual report only
    rows = _company("not found in: GLEIF, Annual report (PDF)")
    dp.refresh(rows)
    assert rows[0]["value"] == ""
    # the pay came from the annual report, not a remuneration report
    rows = _company()
    rows[1]["source"] = "Annual report (PDF)"
    dp.refresh(rows)
    assert rows[0]["value"] == ""
    monkeypatch.setenv("RULES_OFF", "none_if_absent")
    rows = _company()
    dp.refresh(rows)
    assert rows[0]["value"] == ""
