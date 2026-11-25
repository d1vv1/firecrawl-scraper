"""Camelot's pay tables against the AI's lines (extractor/pay_roles_tables.py), with the
grids and the column-mapping calls faked: no PDF is read and no AI is asked."""

import pytest

from extractor import pay_roles_tables as pt, pay_tables
from extractor.datapoints import Origin
from extractor.schemas import ColumnMap, MappedRow
from extractor.scraper import Page
from tests.test_pay_roles import cell, line

EXEC_GRID = pay_tables.Grid(3, [
    ["Name", "Role", "Base salary", "Benefits", "Pension", "Bonus", "Total"],
    ["Margrethe Hauge", "CEO", "3,616", "162", "108", "1,569", "5,455"],
    ["Anders Engelsen", "CFO", "2,062", "114", "103", "304", "2,583"],
    ["Ola Nordmann", "COO", "2,004", "51", "108", "250", "9,999"],      # does not add up
])
BOARD_GRID = pay_tables.Grid(2, [
    ["Name", "Board fee", "Audit", "Remuneration", "Total"],
    ["Peter Nilsson (Chair)", "146.0", "-", "16.2", "162.2"],
    ["Viveka Ekberg", "48.7", "32.4", "-", "81.1"],
])
EXEC_MAP = ColumnMap(is_pay_table=True, year="2025", unit="thousands", currency="NOK",
                     rows=[MappedRow(row=1, label="Margrethe Hauge CEO"),
                           MappedRow(row=2, label="Anders Engelsen CFO"),
                           MappedRow(row=3, label="Ola Nordmann COO")],
                     base_salary=[2], sti_paid=[5], lti_vested=[], lti_granted=[], benefits=[3],
                     pension=[4], pension_allowance=[], other_in_total=[], total=6)
NOT_EXEC = ColumnMap(is_pay_table=False, year=None, unit=None, currency=None, rows=[],
                     base_salary=[], sti_paid=[], lti_vested=[], lti_granted=[], benefits=[],
                     pension=[], pension_allowance=[], other_in_total=[], total=None)
BOARD_MAP = pt.BoardColumnMap(is_board_table=True, year="2025", unit="thousands",
                              currency="EUR",
                              rows=[MappedRow(row=1, label="Peter Nilsson (Chair)"),
                                    MappedRow(row=2, label="Viveka Ekberg")],
                              board_fee=[1], committee_fees=[2, 3], meeting_fees=[],
                              pension=[], other_pay=[], total=4)


@pytest.fixture()
def fake(monkeypatch, tmp_path):
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(pt.pay_tables, "read_grids", lambda p, pages: [EXEC_GRID, BOARD_GRID])
    monkeypatch.setattr(pt.pay_tables, "map_columns",
                        lambda g, n, t="": EXEC_MAP if g is EXEC_GRID else NOT_EXEC)
    monkeypatch.setattr(pt, "map_board", lambda g, n, t="": BOARD_MAP)
    monkeypatch.setattr(pt.pay, "table_pages", lambda chunks, texts, n=4: [2, 3])
    return Origin("pdf", "u", "s", "PARSE", "now", [Page(2, ""), Page(3, "")], {}, pdf=pdf)


def it(title, name, base=None, **cells):
    ln = line(title, base, name=name)
    for f, v in cells.items():
        ln[f] = cell(v)
    return {"pay_line_id": name, "line": ln, "mapping": {"role_detail": "x"}, "quote_check": {}}


def test_agree_replace_add_and_rows_that_do_not_add_up(fake):
    ceo = it("CEO", "Margrethe Hauge", 3616, benefits=162, pension=108, sti_paid=1569,
             total=5455)
    cfo = it("CFO", "Anders Engelsen", 2026, benefits=114, total=2583)        # misread base
    coo = it("COO", "Ola Nordmann", 2000, total=9999)                         # misread base
    counts = pt.check_lines("Goodtech", "2025", [ceo, cfo, coo], fake, [])
    assert set(ceo["table_check"].values()) == {"agree"}
    assert cfo["table_check"]["base_salary"] == "table_replaced"
    b = cfo["line"]["base_salary"]
    assert (b["value"], b["printed"], b["previous"]["value"]) == (2062, "2,062", 2026)
    assert cfo["table_check"]["pension"] == "table_added" and cfo["line"]["pension"]["value"] == 103
    assert cfo["line"]["pension"]["unit_printed"] == "tkr"            # from the line's cells
    assert coo["table_check"]["base_salary"] == "table_not_used"         # row 3 doesn't add up
    assert coo["line"]["base_salary"]["value"] == 2000
    assert counts["lines_matched"] == 3 and counts["table_replaced"] == 1


def test_board_table_and_committee_columns_kept_apart(fake):
    chair = it("Chair", "Peter Nilsson", 146.0, total=162.2)
    member = it("Board member", "Viveka Ekberg", 48.7, total=81.1)
    pt.check_lines("Nilfisk", "2025", [chair, member], fake, [])
    assert chair["table_check"]["base_salary"] == "agree"
    assert chair["table_check"]["committee_fees"] == "multi_column"
    assert "committee_fees" not in chair["line"] or chair["line"]["committee_fees"]["value"] is None
    assert chair["table_row"]["kind"] == "board"


def test_a_figure_the_ai_has_elsewhere_is_not_added_twice(fake, monkeypatch):
    with_other = BOARD_MAP.model_copy(update={"committee_fees": [], "other_pay": [3]})
    monkeypatch.setattr(pt, "map_board", lambda g, n, t="": with_other)
    chair = it("Chair", "Peter Nilsson", 146.0, pension=16.2)   # AI: pension, no total read
    pt.check_lines("Nilfisk", "2025", [chair], fake, [])
    assert chair["table_check"]["other_pay"] == "in_other_field"
    assert not (chair["line"].get("other_pay") or {}).get("value")


def test_a_line_that_adds_up_is_not_overruled(fake, monkeypatch):
    # Stora Enso: the table splits by payment form (cash 145 / shares 89 = 234); the AI read
    # the board fee 222 and committee fee 12 = 234. Same total, AI consistent: keep the AI.
    grid = pay_tables.Grid(5, [["Name", "Cash", "Value of shares", "Total"],
                               ["Kari Jordan, Chair", "145", "89", "234"]])
    m = pt.BoardColumnMap(is_board_table=True, year="2025", unit="thousands", currency="EUR",
                          rows=[MappedRow(row=1, label="Kari Jordan, Chair")], board_fee=[1],
                          committee_fees=[], meeting_fees=[], pension=[], other_pay=[2],
                          total=3)
    monkeypatch.setattr(pt.pay_tables, "read_grids", lambda p, pages: [grid])
    monkeypatch.setattr(pt.pay_tables, "map_columns", lambda g, n, t="": NOT_EXEC)
    monkeypatch.setattr(pt, "map_board", lambda g, n, t="": m)
    chair = it("Chair", "Kari Jordan", 222, committee_fees=12, total=234)
    pt.check_lines("Stora Enso", "2025", [chair], fake, [])
    assert chair["table_check"]["base_salary"] == "ai_consistent"
    assert chair["line"]["base_salary"]["value"] == 222
    assert chair["table_check"]["total"] == "agree"


def test_comparison_year_table_is_not_used(fake, monkeypatch):
    old_year = EXEC_MAP.model_copy(update={"year": "2024"})
    monkeypatch.setattr(pt.pay_tables, "map_columns",
                        lambda g, n, t="": old_year if g is EXEC_GRID else NOT_EXEC)
    ceo = it("CEO", "Margrethe Hauge", 1, total=5455)
    pt.check_lines("Goodtech", "2025", [ceo], fake, [])
    assert "table_check" not in ceo


def test_no_pdf_changes_nothing():
    origin = Origin("pdf", "u", "s", "PARSE", "now", [], {}, pdf=None)
    assert pt.check_lines("A", "2025", [it("CEO", "A B", 1)], origin, []) == {}


def test_match_by_name_then_title_then_base():
    rows = [pt.TableRow("executive", "Margrethe Hauge, CEO", 3, {"base_salary": ["3,616"]},
                        "5,455", True),
            pt.TableRow("executive", "CFO", 3, {"base_salary": ["2,062"]}, "2,583", True)]
    assert pt.match({"person_name": "Margrethe Hauge"}, rows) is rows[0]
    assert pt.match({"printed_title": "CFO"}, rows) is rows[1]
    assert pt.match({"base_salary": {"value": 2062.0}}, rows) is rows[1]
    rows[1].used = True
    assert pt.match({"printed_title": "CFO"}, rows) is None


def test_a_named_line_never_takes_another_persons_row():
    # same board fee for two members (Sydbank): the name decides, never the fee
    rows = [pt.TableRow("board", "Gitte Poulsen", 7, {"base_salary": ["408.009"]}, "633.454", True)]
    line = {"person_name": "Janne Moltke-Leth", "printed_title": "Bestyrelsesmedlem",
            "base_salary": {"value": 408009.0}}
    assert pt.match(line, rows) is None
    assert pt.match({"base_salary": {"value": 408.009}}, rows) is None     # board: no fee match


def test_same_printed_figure_and_blank_table_cells_keep_the_ai(fake, monkeypatch):
    # B&C Speakers: "228.000" on both sides, read as two numbers; National Bank of Greece:
    # "-" in the table where the AI read the chair's fee
    grid = pay_tables.Grid(4, [["Name", "Board fee", "Total"],
                               ["Lorenzo Coppini", "228.000", "228.000"],
                               ["Gikas Hardouvelis", "–", "–"]])
    m = pt.BoardColumnMap(is_board_table=True, year="2025", unit="units", currency="EUR",
                          rows=[MappedRow(row=1, label="Lorenzo Coppini"),
                                MappedRow(row=2, label="Gikas Hardouvelis")],
                          board_fee=[1], committee_fees=[], meeting_fees=[], pension=[],
                          other_pay=[], total=2)
    monkeypatch.setattr(pt.pay_tables, "read_grids", lambda p, pages: [grid])
    monkeypatch.setattr(pt.pay_tables, "map_columns", lambda g, n, t="": NOT_EXEC)
    monkeypatch.setattr(pt, "map_board", lambda g, n, t="": m)
    a = it("Amministratore", "Lorenzo Coppini", 228000)
    a["line"]["base_salary"]["printed"] = "228.000"
    b = it("BoD Chair", "Gikas Hardouvelis", 379500)
    pt.check_lines("B&C", "2025", [a, b], fake, [])
    assert a["table_check"]["base_salary"] == "agree"
    assert b["table_check"]["base_salary"] == "table_blank"
    assert b["line"]["base_salary"]["value"] == 379500


def test_a_figure_whose_quote_is_found_is_not_replaced(fake):
    # Iren: the AI's total is in the text; another table's smaller total is only noted
    cfo = it("CFO", "Anders Engelsen", 2026, benefits=114, total=2583)
    cfo["quote_check"] = {"base_salary": "close"}
    pt.check_lines("Goodtech", "2025", [cfo], fake, [])
    assert cfo["table_check"]["base_salary"] == "table_differs"
    assert cfo["line"]["base_salary"]["value"] == 2026
    assert cfo["table_figures"]["base_salary"] == "2,062"
