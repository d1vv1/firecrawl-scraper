"""Issue 19 (DACH Set 2): German report search, names, fixed-pay-only roles, merges that
keep the better block."""

import datetime as dt

from extractor import combine
from extractor import datapoints as dp
from extractor import report_finder as rf
from tests.test_before_dach import CHECK_COLS, _check, _read, _row, _write
from tests.test_run_fixes import FakeFC

YEAR = dt.date.today().year - 1


class SearchByQuery(FakeFC):
    """Search results by a word in the query."""

    def __init__(self, maps, by_word):
        super().__init__(maps)
        self.by_word = by_word

    def search(self, query, limit):
        super().search(query, limit)
        return next((r for w, r in self.by_word.items() if w in query), [])


def test_a_dach_report_found_only_by_its_german_name():
    pdf = f"https://www.albis-leasing.de/files/geschaeftsbericht-{YEAR}.pdf"
    fc = SearchByQuery([["https://www.albis-leasing.de/leasing"]] * 5,
                       {"Geschäftsbericht": [{"url": pdf, "title": f"GESCHÄFTS- BERICHT {YEAR}"}]})
    r = rf.find_report("https://www.albis-leasing.de", fc, country="DE", company_name="ALBIS LEASING AG O.N.")
    assert r.url == pdf
    searches = [c for c in fc.calls if c.startswith("search:")]
    assert searches == [f"search:albis leasing annual report {YEAR} pdf",
                        f"search:albis leasing Geschäftsbericht {YEAR}"]


def test_no_german_search_outside_dach_or_when_the_english_one_finds_it():
    assert rf.search_languages("SE") == ["en"]
    assert rf.search_languages("CH") == rf.search_languages(None, "AT") == ["en", "de"]
    pdf = f"https://www.x-ag.de/annual-report-{YEAR}.pdf"
    fc = SearchByQuery([["https://www.x-ag.de/a"]] * 5, {"annual report": [{"url": pdf, "title": "x"}]})
    rf.find_report("https://www.x-ag.de", fc, country="DE", company_name="X AG")
    assert not any("Geschäftsbericht" in c for c in fc.calls)


def test_hyphenated_titles_and_names_of_companies_being_wound_up():
    c = rf.search_result_candidate({"url": "https://xozalbisassets.blob.core.windows.net/live/file/2d0b.pdf",
                                    "title": f"GESCHÄFTS- BERICHT {YEAR}"}, frozenset())
    assert c.kept and c.is_pdf and c.year == YEAR
    assert rf.search_name("TISCON AG i.A.") == "tiscon"
    assert rf.search_name("Muster AG in Liquidation") == "muster"


def test_place_words_a_domain_leaves_out():
    assert rf.own_document("https://www.edisunpower.com/en/investors/annual-reports",
                           "Edisun Power Europe AG", None)
    assert rf.name_tokens("Swiss Re AG") == {"swiss"}         # nothing else left: kept
    assert not rf.own_document("https://www.power.com/annual-report.pdf", "Edisun Power Europe AG", None)


def _role(name, value, note=""):
    return _row("a", name, value, "role", "Vorstand", note or ("" if value else "not found in: Remuneration report (PDF)"))


def test_a_role_paid_only_fixed_pay_has_no_variable_pay_rather_than_none_found():
    rows = [_role("base_salary", "72000"), _role("total_remuneration", "72000"),
            *[_role(k, "") for k in dp.VARIABLE_PAY], _role("benefits_value", "")]
    dp.refresh(rows)
    by = {r["data_point"]: r for r in rows}
    assert all(by[k]["note"] == dp.NO_VARIABLE_PAY for k in dp.VARIABLE_PAY)
    assert by["benefits_value"]["note"].startswith("not found")


def test_variable_pay_is_still_missing_when_the_total_holds_more_than_fixed_pay():
    rows = [_role("base_salary", "350000"), _role("benefits_value", "39000"),
            _role("total_remuneration", "565000"), *[_role(k, "") for k in dp.VARIABLE_PAY]]
    dp.refresh(rows)
    assert all(r["note"].startswith("not found") for r in rows if r["data_point"] in dp.VARIABLE_PAY)
    # a bonus figure read: the others stay "not found" too
    rows = [_role("base_salary", "100"), _role("total_remuneration", "100"), _role("sti_paid", "0"),
            _role("lti_max", "")]
    dp.refresh(rows)
    assert rows[-1]["note"].startswith("not found")


def test_combine_keeps_the_old_pay_when_a_run_got_far_fewer_values(tmp_path):
    into, run = tmp_path / "all.csv", tmp_path / "run.csv"
    old_pay = [_row("a", f"p{i}", str(i + 1), "role", "CEO") for i in range(10)]
    _write(into, [_row("a", "revenue", "100"), *old_pay], dp.COLUMNS)
    _write(tmp_path / "all_checks.csv", [_check("a", "p0", "1", role="CEO")], CHECK_COLS)
    _write(run, [_row("a", "revenue", "110"), _row("a", "p0", "1", "role", "Vorstand"),
                 _row("a", "p1", "", "role", "Vorstand")], dp.COLUMNS)
    _write(tmp_path / "run_checks.csv", [_check("a", "revenue", "110"),
                                        _check("a", "p0", "1", role="Vorstand")], CHECK_COLS)
    stats = combine.combine([run], into)
    rows = _read(into)
    assert [(r["data_point"], r["value"]) for r in rows if r["grain"] == "company"] == [("revenue", "110")]
    assert {r["role_row"] for r in rows if r["grain"] == "role"} == {"CEO"}
    assert len([r for r in rows if r["grain"] == "role"]) == 10
    assert stats["worse"] == ["a (role)"]
    checks = _read(tmp_path / "all_checks.csv")
    assert {(c["data_point"], c["role_row"]) for c in checks} == {("revenue", ""), ("p0", "CEO")}
    # --take-newer replaces it
    _write(into, [_row("a", "revenue", "100"), *old_pay], dp.COLUMNS)
    combine.combine([run], into, keep_better=False)
    assert {r["role_row"] for r in _read(into) if r["grain"] == "role"} == {"Vorstand"}


def test_a_pay_only_run_is_not_taken_for_a_failed_run_of_the_company_facts():
    from extractor.fields import NOT_COLLECTED
    old = [_row("a", f"f{i}", str(i + 1)) for i in range(10)]
    new = [_row("a", f"f{i}", note=NOT_COLLECTED + "pay") for i in range(9)] + [_row("a", "f9", "99")]
    assert combine.worse_blocks(old, new) == set()
    rows, kept = combine.merge_company(old, new)
    assert [r["value"] for r in rows] == [str(i + 1) for i in range(9)] + ["99"]


def test_the_annual_reports_listing_page_is_opened_with_the_fetch_reserve():
    listing = "https://www.edisunpower.com/en/investors/annual-reports"
    pdf = f"https://www.edisunpower.com/files/annual-report-{YEAR}.pdf"

    class Capped(FakeFC):
        max_credits = 4

        @property
        def credits(self):
            return type("M", (), {"total": self.spent})()

    fc = Capped(maps=[[listing]] * 5, scrape_links=[pdf])
    r = rf.find_report("https://www.edisunpower.com", fc, country="SE", company_name="Edisun Power Europe AG")
    assert r.url == pdf and fc.calls[-1] == f"scrape:{listing}"
