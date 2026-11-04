"""The output checks (extractor/output_checks.py): each check on hand-made rows."""

import csv

from extractor import output_checks as oc


def _row(**kw) -> oc.Row:
    d = {"company_id": "acme", "grain": "company", "role_row": "", "data_point": "", "value": "",
         "unit": "", "period_end": "", "source": "", "endpoint": "https://example.com/r.pdf#page=3",
         "method": "PARSE", "confidence": "B", "note": ""}
    d.update(kw)
    return oc.Row(d)


class NoSources:
    def pages(self, endpoint):
        return None


def _ctx(*rows, sources=None):
    return oc.Ctx(sources or NoSources(), dict(oc.DEFAULT_RANGES), list(rows))


def test_quote_and_printed_figure_are_read_from_the_note():
    r = _row(note='printed 1242 thousands; PDF page 15: "Anders Opedal | 1,242"; equals the parts')
    assert r.quote == ("Anders Opedal | 1,242", 15)
    assert r.printed == (1242, 1000)
    old = _row(note='printed 1.05788e+06 units; PDF page 7: "Salary|1 057 875"')
    assert old.printed == (1057880, 1)


def test_core_02_value_in_quote():
    ctx = _ctx()
    base = _row(data_point="base_salary", value="1242000",
                note='printed 1242 thousands; PDF page 15: "Anders Opedal | 1,242"')
    assert oc.core_02(base, ctx).outcome == "pass"
    summed = _row(data_point="benefits_value", value="119000",
                  note='printed 119 thousands; PDF page 15: "Anders Opedal | 96 | 23"')
    assert oc.core_02(summed, ctx).outcome == "pass"
    spaced = _row(data_point="base_salary", value="1057875",
                  note='printed 1057875 units; PDF page 7: "Salary|1 057 875"')
    assert oc.core_02(spaced, ctx).outcome == "pass"
    shares = _row(data_point="shares_outstanding", value="5582534000",
                  note='PDF page 183: "Number of shares, (000s) 5 582 534"')
    assert oc.core_02(shares, ctx).outcome == "pass"
    wrong = _row(data_point="sti_max", value="100", unit="% of base salary",
                 note='report text: "CEO – 300% of salary"')
    assert oc.core_02(wrong, ctx).outcome == "fail"
    dash = _row(data_point="lti_vested", value="0", note='printed 0 units; PDF page 7: "Long-term incentive|—"')
    assert oc.core_02(dash, ctx).outcome == "pass"


def test_core_02_dates_names_and_what_it_skips():
    ctx = _ctx()
    date = _row(data_point="listing_date", value="2005-07-20",
                note='web page: "On July 20, 2005 the unification of Royal Dutch"')
    assert oc.core_02(date, ctx).outcome == "pass"
    invented = _row(data_point="listing_date", value="1935-01-02", note='web page: "Listed since 1935"')
    assert oc.core_02(invented, ctx).outcome == "fail"
    parent = _row(data_point="ultimate_parent", value="AB Volvo (publ)",
                  note='PDF page 30: "The ultimate parent of the Group is AB Volvo"')
    assert oc.core_02(parent, ctx).outcome == "pass"
    assert oc.core_02(_row(data_point="controlling_owner", value="state"), ctx).outcome == "n/a"
    assert oc.core_02(_row(data_point="lei", value="X", method="API"), ctx).outcome == "n/a"
    clipped = _row(data_point="benefits_value", value="559723",
                   note='printed 559723 units; PDF page 7: "other benefits including relocation…"')
    assert oc.core_02(clipped, ctx).outcome == "n/a"


def test_core_03_looks_the_quote_up_on_the_linked_page():
    class Src:
        def pages(self, endpoint):
            return {14: "Introduction", 15: "| Anders Opedal | 1,242 | 224 |"}
    ctx = _ctx(sources=Src())
    good = _row(data_point="base_salary", value="1242000", note='PDF page 15: "Anders Opedal | 1,242"')
    assert oc.core_03(good, ctx).outcome == "pass"
    misplaced = _row(data_point="base_salary", value="1242000", note='PDF page 30: "Anders Opedal | 1,242"')
    assert "page 15" in oc.core_03(misplaced, ctx).reason
    absent = _row(data_point="base_salary", value="1", note='PDF page 15: "Irene Rummelhoff | 543"')
    assert oc.core_03(absent, ctx).outcome == "fail"
    unknown = _row(data_point="base_salary", value="1", note='PDF page 15: "x"')
    assert oc.core_03(unknown, _ctx()).outcome == "n/a"                  # source not cached
    graded_c = _row(data_point="fte", note='report text: "x" (quote not found verbatim)')
    assert oc.core_03(graded_c, _ctx()).outcome == "fail"


def test_period_needed_only_for_dated_fields():
    ctx = _ctx()
    assert oc.core_04(_row(data_point="ebitda", value="1"), ctx).outcome == "fail"
    assert oc.core_04(_row(data_point="ebitda", value="1", period_end="2025-12-31"), ctx).outcome == "pass"
    assert oc.core_04(_row(data_point="legal_name", value="Acme"), ctx).outcome == "n/a"


def test_identifier_check_digits():
    assert oc.lei_ok("OW6OFBNCKXC4US5C7523") and not oc.lei_ok("OW6OFBNCKXC4US5C7524")
    assert oc.isin_ok("NO0010096985") and not oc.isin_ok("NO0010096986")
    assert oc.isin_ok("US0378331005")


def test_codes_and_closed_sets():
    ctx = _ctx()
    assert oc.cod_01(_row(data_point="country_code", value="NO"), ctx).outcome == "pass"
    assert oc.cod_01(_row(data_point="country_code", value="UK"), ctx).outcome == "fail"
    assert oc.cod_01(_row(data_point="pay_currency", value="NOK"), ctx).outcome == "pass"
    assert oc.cod_01(_row(data_point="ownership_type", value="widely_held"), ctx).outcome == "pass"
    assert oc.cod_01(_row(data_point="listing_status", value="maybe"), ctx).outcome == "fail"
    assert oc.cod_01(_row(data_point="exchange", value="Oslo Børs", note="MIC XOSL"), ctx).outcome == "pass"


def test_percentages_and_holdings():
    ctx = _ctx()
    assert oc.num_06(_row(data_point="sti_max", value="200", unit="% of maximum"), ctx).outcome == "fail"
    assert oc.num_06(_row(data_point="sti_max", value="200", unit="% of base salary"), ctx).outcome == "pass"
    over = _row(data_point="largest_holders", value="A 60%; B 50%")
    assert oc.num_07(over, ctx).outcome == "fail"
    assert oc.num_06(over, ctx).outcome == "pass"


def _role(field, value, unit="USD", role="CEO", note=""):
    return _row(grain="role", role_row=role, data_point=field, value=value, unit=unit,
                period_end="2025-12-31", note=note)


def test_total_against_its_parts():
    parts = [_role("base_salary", "1242"), _role("sti_paid", "292"), _role("benefits_value", "119"),
             _role("pension_contribution", "254"), _role("lti_granted", "306")]
    total = _role("total_remuneration", "2213")
    assert oc.xf_01(total, _ctx(*parts, total)).outcome == "pass"
    assert oc.xf_02(total, _ctx(*parts, total)).outcome == "pass"
    # parts above the total: a figure misread or counted twice
    wrong = _role("total_remuneration", "1500")
    assert oc.xf_01(wrong, _ctx(*parts, wrong)).outcome == "fail"
    # total above the parts: pay outside the fields (BioArctic's one-off 3,004); noted
    t = _role("total_remuneration", "5217")
    assert oc.xf_01(t, _ctx(*parts, t)).outcome == "pass"
    assert oc.xf_02(t, _ctx(*parts, t)).outcome == "fail"


def test_an_expensed_lti_states_its_basis():
    expensed = _role("lti_vested", "1650000", note="printed 1650 thousands; form: accounting expense")
    assert oc.num_09(expensed, _ctx()).outcome == "pass"


def test_sti_paid_above_its_maximum():
    rows = [_role("base_salary", "1000"), _role("sti_max", "50", unit="% of base salary")]
    paid = _role("sti_paid", "800")
    assert oc.num_11(paid, _ctx(*rows, paid)).outcome == "fail"
    fine = _role("sti_paid", "400")
    assert oc.num_11(fine, _ctx(*rows, fine)).outcome == "pass"


def test_derived_values_recalculate():
    ctx = _ctx()
    pension = _role("pension_contribution", "254000", note="derived: pension 30,000 + salary addition "
                    "in lieu of pension 224,000; printed 30 thousands")
    pension.d["method"] = "DERIVED"
    assert oc.der_03(pension, ctx).outcome == "pass"
    pension.d["value"] = "250000"
    assert oc.der_03(pension, ctx).outcome == "fail"


def test_a_check_that_cannot_run_never_lowers_the_status():
    r = _row(data_point="legal_name", value="Acme AB", method="API",
             endpoint="https://api.gleif.org/api/v1/lei-records/X", note="")
    s = oc.score_row(r, _ctx(r))
    assert s.status == "Pass" and not s.hard_failed


def test_end_to_end_report(tmp_path):
    path = tmp_path / "run.csv"
    rows = [_row(data_point="lei", value="OW6OFBNCKXC4US5C7523", method="API",
                 endpoint="https://api.gleif.org/x").d,
            _row(data_point="fte").d]                                       # blank: not scored
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    scored, all_rows = oc.run(path, NoSources(), dict(oc.DEFAULT_RANGES))
    assert [s.status for s in scored] == ["Pass"]
    text = oc.report(scored, all_rows, "run.csv")
    assert "1 of 2 filled" in text and "| CORE-01 |" in text


def test_sector_code_must_be_in_the_taxonomy():
    ctx = _ctx()
    assert oc.cod_01(_row(data_point="sector_code", value="NACE 47.91"), ctx).outcome == "pass"
    assert oc.cod_01(_row(data_point="sector_code", value="NACE 47.98"), ctx).outcome == "fail"
    assert oc.cod_01(_row(data_point="sector_code", value="SIC (UK) 70100"), ctx).outcome == "pass"
