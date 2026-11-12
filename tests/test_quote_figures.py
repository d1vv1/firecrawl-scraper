"""Values the quote check failed though the quote holds them (12 Nov 2026): nothing
stated in words, counts in words, decimal commas, a pre-scaled figure, a total less
the CEO; and pay "amounts" that are only percentages."""

from extractor import output_checks as oc
from extractor.extract import printed_figure
from extractor.pay import percent_only
from extractor.validate import figure_in_quote, number_words, states_none


def _row(name, value, note, unit="GBP", role=""):
    return oc.Row({"data_point": name, "value": value, "note": note, "unit": unit,
                   "role_row": role, "method": "PARSE"})


def _core02(row):
    return oc.core_02(row, oc.Ctx(None, dict(oc.DEFAULT_RANGES)))


def test_a_zero_stated_in_words_is_in_its_quote():
    for q in ("No bonuses were paid for the 2025 Financial Year.",
              "Im Geschäftsjahr 2025 waren keine Mitarbeiter beschäftigt.",
              "I 2025 ble det ikke foretatt tildeling av egenkapitalbevis.",
              "As the performance targets were not met, the awards will lapse in full.",
              "Employees | nil | nil"):
        assert states_none(q), q
        assert _core02(_row("sti_paid", "0", f'report text: "{q}"', unit="")).outcome == "pass"
    assert not states_none("The bonus was paid in March.")
    assert _core02(_row("sti_paid", "0", 'report text: "The bonus was paid in March."')).outcome == "fail"


def test_counts_written_as_words():
    assert figure_in_quote(3, "We had three employees as of December 31, 2025.")
    assert figure_in_quote(2, "aber für kein Vorstandsmitglied zwei Prozent übersteigen soll")
    assert not figure_in_quote(2, "The board appointed her to the role")       # not Norwegian "to"
    assert not figure_in_quote(1, "one of the directors")                      # articles: not for 1
    assert 5 in number_words("employed five salaried staff")


def test_decimal_commas_and_swiss_separators():
    assert figure_in_quote(2.14, "Kurs am letzten Handelstag € 2,14")
    assert figure_in_quote(42.3, "Nebenleistungen|41,0|6,7|33,6|3,8|42,3|7,5")
    assert figure_in_quote(1905326, "Total assets 1′905′326")
    assert figure_in_quote(98064, "**Geschäftsleitung Total**|**98‘064**|**20‘000**")
    assert figure_in_quote(1234, "Revenue 1,234")                              # still thousands


def test_cells_grouped_with_spaces_add_up():
    assert figure_in_quote(182000, "Markus Ehrle, CEO | 154 000 | 28 000")


def test_a_figure_the_ai_had_already_scaled():
    # the AI gave 180000 with the table's "thousands": the value is right, printed 180
    assert printed_figure(180000, "thousands", "Annual bonus £000 180") == 180
    assert printed_figure(180, "thousands", "Annual bonus £000 180") == 180
    row = _row("sti_paid", "180000", 'printed 180000 thousands; report text: "Annual bonus £000 180"')
    assert row.printed == (180, 1e3) and _core02(row).outcome == "pass"


def test_other_members_as_the_total_less_the_ceo():
    q = "Base salary|8,097.1|1,800.0|8,285.1|1,700.0|"
    assert _core02(_row("base_salary", "6297100", f'printed 6297.1 thousands; report text: "{q}"',
                        role="Other members of Global Executive Committee")).outcome == "pass"
    assert _core02(_row("base_salary", "6297100", f'printed 6297.1 thousands; report text: "{q}"',
                        role="CEO")).outcome == "fail"
    # a near miss by chance (435 - 173 = 262, not 261) is no difference
    q = "Rest of the Committee 5|806|435|157|36|225|173|101|1 933"
    assert _core02(_row("lti_granted", "261000", f'printed 261 thousands; report text: "{q}"',
                        role="Rest of the Committee")).outcome == "fail"


def test_a_zero_amount_needs_no_currency():
    row = _row("pension_contribution", "0", 'report text: "No pension contributions were made."', unit="")
    ctx = oc.Ctx(None, dict(oc.DEFAULT_RANGES), [row, _row("base_salary", "100", "", unit="GBP")])
    assert oc.num_01(row, ctx).outcome == "n/a" and oc.num_12(row, ctx).outcome == "n/a"
    assert oc.num_01(_row("base_salary", "5", "", unit=""), ctx).outcome == "fail"


def test_a_percentage_is_not_a_pay_amount():
    assert percent_only(200, "Up to 200% of base salary at allocation.")
    assert percent_only(60, "Bonus achieved 60%")
    assert percent_only(5, "On 1 July 2025, Aaron Izzard was granted a VCP award of 5 per cent")
    assert not percent_only(200, "LTIP 200 (2024: 180)")
    assert not percent_only(60, "Bonus 60 | 60% of maximum")                  # also printed bare
