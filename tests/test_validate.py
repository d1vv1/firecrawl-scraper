"""Quote and figure matching (extractor/validate.py) for the forms seen in the Nordic/UK run."""

from extractor.validate import figure_in_quote, quote_in_text


def test_a_quote_that_leaves_words_out_is_found_when_its_parts_are_close():
    src = ("Short-term incentives may, for the CEO, amount to a maximum of 100% and for other "
           "Executives, a maximum of 80% of the base salary.")
    assert quote_in_text("Short-term incentives may, for ... other Executives, a maximum of 80%", src)
    assert not quote_in_text("Short-term incentives may, for ... other Executives, a maximum of 90%", src)
    far = "Short-term incentives may. " + "Unrelated words here. " * 40 + "a maximum of 80%"
    assert not quote_in_text("Short-term incentives may ... a maximum of 80%", far)


def test_a_cell_grouped_with_plain_spaces_is_one_figure():
    row = "Martin Lundstedt, President and CEO|2025|22 868|425|9 125|"
    assert figure_in_quote(22868, row) and figure_in_quote(22_868_000, row, scaled=True)
    assert not figure_in_quote(250503, "Turnover 2 50,503")          # cells, not one figure


def test_a_label_wrapped_over_table_cells_is_found():
    src = ("|**Line Køhler Ljungdahl, Executive V**|**ice President, Chief Corporate C**|**ommercial Officer (until**"
           "|**14-05-26). Garden**|**leave from 15-05**|**-26 to 30-06-27.******||||||||\n"
           "||**2025/26**|3,078|315|369|336|1,924|-|6,023|\n")
    q = ("Line Køhler Ljungdahl, Executive Vice President, Chief Corporate Commercial Officer (until 14-05-26). "
         "Garden leave from 15-05-26 to 30-06-27.******|2025/26|3,078|315|369")
    assert quote_in_text(q, src) and not quote_in_text(q.replace("3,078", "3,079"), src)
