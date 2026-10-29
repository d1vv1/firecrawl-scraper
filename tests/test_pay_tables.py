"""Pay tables read by Camelot and mapped by a small AI call (docs/pay_table_plan.md)."""

from extractor import pay_tables as pt
from extractor.schemas import (ColumnMap, LtiAmount, MappedRow, PayAmount, PayTarget,
                               RemunerationFacts, RoleHeadcount, RolePay, TextFact)
from extractor.sections import Chunk
from extractor.validate import quote_in_text

# Equinor 2025, page 15, as Camelot reads it (stream mode).
EQUINOR = [
    ["", "", "Fixed remuneration", "", "", "Variable remuneration", "", "", "", "", "", ""],
    ["", "", "Fees", "", "", "One-year variable", "Multi-year variable", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "Proportion"],
    ["Members of the corporate executive", "", "", "", "", "", "", "", "", "", "", "of fixed and"],
    ["committee", "", "Fixed salary", "", "", "", "", "", "Extraordinary", "", "Total", "variable"],
    ["(figures in USD thousand)", "Base salary", "addition", "Other fees", "Fringe benefits", "AVP",
     "LTI", "SSP", "items", "Pension expense", "remuneration", "remuneration"],
    ["Anders Opedal", "1,242", "224", "96", "23", "292", "306", "0", "0", "30", "2,213", "73% / 27%"],
    ["Geir Tungesvik", "479", "86", "143", "9", "101", "118", "4", "0", "24", "965", "77% / 23%"],
    ["Philippe François Mathieu", "516", "93", "103", "53", "113", "126", "9", "0", "30", "1,043",
     "76% / 24%"],
]
EQUINOR_MAP = dict(is_pay_table=True, year="2025", unit="thousands", currency="USD",
                   rows=[MappedRow(row=6, label="Anders Opedal"),
                         MappedRow(row=7, label="Geir Tungesvik"),
                         MappedRow(row=8, label="Philippe François Mathieu")],
                   base_salary=[1], sti_paid=[5], lti_vested=[], lti_granted=[6, 7],
                   benefits=[3, 4], pension=[9], pension_allowance=[2], other_in_total=[8],
                   total=10)


def _map(**kw) -> ColumnMap:
    return ColumnMap(**{**EQUINOR_MAP, **kw})


def _amount(value=None, quote=None):
    return PayAmount(value=value, unit="thousands" if value is not None else None,
                     currency="USD" if value is not None else None, includes=None,
                     quote=quote, chunk_id=0 if quote else None)


def _lti(value=None):
    return LtiAmount(value=value, unit=None, currency=None, form="shares" if value else None,
                     includes=None, quote="q" if value else None, chunk_id=None)


def _target():
    return PayTarget(value=None, form=None, currency=None, unit=None, quote=None, chunk_id=None)


def _role(title, name=None, base=None, benefits=None, executive=True):
    return RolePay(role_title=title, person_name=name, executive=executive, is_aggregate=False,
                   quote=None, chunk_id=None,
                   aggregate_headcount=RoleHeadcount(value=None, excludes=None, quote=None,
                                                     chunk_id=None),
                   base_salary=_amount(base, "q" if base else None), sti_paid=_amount(),
                   lti_vested=_lti(), lti_granted=_lti(5), benefits=_amount(benefits, "q"),
                   pension=_amount(), pension_allowance=_amount(), total=_amount(),
                   sti_target=_target(), sti_max=_target(), lti_target=_target(),
                   lti_max=_target())


def _facts(*roles, year="2025"):
    none = TextFact(value=None, quote=None, chunk_id=None)
    return RemunerationFacts(fiscal_year=year, roles=list(roles), pension_type=none,
                             benefits=none, shareholding_requirement=none)


def test_parse_figure():
    assert pt.parse_figure("1,242") == 1242
    assert pt.parse_figure("1 242") == 1242
    assert pt.parse_figure("1.242") == 1242
    assert pt.parse_figure("7.1") == 7.1
    assert pt.parse_figure("(12)") == -12
    assert pt.parse_figure("-") == 0 and pt.parse_figure("–") == 0
    assert pt.parse_figure("73% / 27%") is None
    assert pt.parse_figure("Anders") is None
    assert pt.parse_figure("") is None


def test_years_are_not_figures():
    assert not pt.is_figure("2025") and not pt.is_figure("2025/26")
    assert pt.is_figure("2,213") and pt.is_figure("-")


def test_clean_drops_empty_rows_and_columns_and_joins_lines():
    assert pt.clean([["a\nb", "", "1"], ["", "", ""], ["c", "", "2"]]) == [["a b", "1"], ["c", "2"]]


def test_grid_text_gives_each_column_its_joined_header():
    text = pt.Grid(15, EQUINOR).text()
    assert "r6 | Anders Opedal | 1,242" in text
    assert "c2: Fixed remuneration Fees Fixed salary addition" in text
    assert "c10: Total remuneration" in text


def test_table_rows_add_up_the_mapped_columns():
    rows = pt.table_rows(pt.Grid(15, EQUINOR), _map())
    ceo = rows[0]
    assert ceo.label == "Anders Opedal"
    assert ceo.values == {"base_salary": 1242, "sti_paid": 292, "lti_granted": 306,
                          "benefits": 119, "pension": 30, "pension_allowance": 224, "total": 2213}
    assert ceo.headers["benefits"] == "Other fees + Fringe benefits"
    assert ceo.cells["benefits"] == ["96", "23"]
    assert rows[2].values["lti_granted"] == 135                     # LTI 126 + SSP 9


def test_a_row_whose_parts_miss_the_total_is_dropped():
    # "Fringe benefits" left out: Mathieu's parts are 53 short of 1,043 (5%); the CEO's
    # 23 of 2,213 is within the 2% tolerance, so a small column can slip through
    rows = pt.table_rows(pt.Grid(15, EQUINOR), _map(benefits=[3]))
    assert [r.label for r in rows] == ["Anders Opedal", "Geir Tungesvik"]


def test_mapping_problems():
    assert pt.mapping_problem(_map(is_pay_table=False), 12) == "not a pay table"
    assert "two fields" in pt.mapping_problem(_map(sti_paid=[1]), 12)   # people as columns
    assert "no total" in pt.mapping_problem(_map(total=None), 12)
    assert "outside" in pt.mapping_problem(_map(pension=[30]), 12)
    assert pt.mapping_problem(_map(), 12) is None


def test_the_quote_of_a_summed_field_is_found_in_a_merged_markdown_row():
    # pymupdf4llm merged "Other fees" and "Fringe benefits" into one cell
    page = ("| Members | Base salary | Fixed salary addition | Other fees Fringe benefits | AVP |\n"
            "|---|---|---|---|---|\n"
            "| Anders Opedal | 1,242 | 224 | 96<br>23 | 292 | 306 | 0 | 0 | 30 | 2,213 |")
    ceo = pt.table_rows(pt.Grid(15, EQUINOR), _map())[0]
    quote = " | ".join([ceo.label] + ceo.cells["benefits"])
    assert quote_in_text(quote, page)


def test_apply_replaces_the_matched_roles_amounts():
    rows = pt.table_rows(pt.Grid(15, EQUINOR), _map())
    facts = _facts(_role("President and CEO", base=1242, benefits=343),     # by base salary
                   _role("EVP Projects", name="Geir Tungesvik"),            # by name
                   _role("Board (non-executive)", executive=False))
    done = set()
    out = pt.apply(facts, rows, "thousands", "USD", [Chunk(4, "", [15])], done)
    ceo, evp, board = out.roles
    assert done == {0, 1}
    assert ceo.benefits.value == 119 and ceo.benefits.includes == "table: Other fees + Fringe benefits"
    assert ceo.benefits.quote == "Anders Opedal | 96 | 23" and ceo.benefits.chunk_id == 4
    assert ceo.pension_allowance.value == 224 and ceo.total.value == 2213
    assert ceo.lti_granted.value == 306 and ceo.lti_granted.form == "shares"
    assert ceo.role_title == "President and CEO"                           # the AI's title stays
    assert evp.base_salary.value == 479
    assert board == facts.roles[2]


def test_a_role_matched_by_an_earlier_table_is_left_alone():
    rows = pt.table_rows(pt.Grid(15, EQUINOR), _map())
    facts = _facts(_role("CEO", name="Anders Opedal", benefits=1))
    out = pt.apply(facts, rows, "thousands", "USD", [], {0})
    assert out.roles[0].benefits.value == 1


def test_no_match_when_two_rows_fit():
    rows = pt.table_rows(pt.Grid(15, EQUINOR), _map())
    assert pt.match(_role("EVP"), rows) is None                  # no name, title or base
    assert pt.match(_role("EVP", base=479), rows).label == "Geir Tungesvik"


def test_from_tables_skips_a_table_for_another_year(tmp_path, monkeypatch):
    pdf = tmp_path / "rem.pdf"
    pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(pt, "read_grids", lambda p, pages: [pt.Grid(16, EQUINOR), pt.Grid(15, EQUINOR)])
    maps = {16: _map(year="2024"), 15: _map()}
    monkeypatch.setattr(pt, "map_columns", lambda g, name, text="": maps[g.page])
    monkeypatch.setattr("extractor.pay.table_pages", lambda chunks, text, n=4: [15, 16])
    facts = _facts(_role("CEO", name="Anders Opedal", benefits=343))
    out = pt.from_tables("Equinor ASA", facts, pdf, [Chunk(0, "", [15, 16])], {})
    assert out.roles[0].benefits.value == 119
    assert pt.from_tables("Equinor ASA", facts, None, [], {}) is facts      # no PDF


def test_from_tables_can_be_switched_off(tmp_path, monkeypatch):
    pdf = tmp_path / "rem.pdf"
    pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(pt, "ENABLED", False)
    facts = _facts(_role("CEO"))
    assert pt.from_tables("X", facts, pdf, [], {}) is facts
