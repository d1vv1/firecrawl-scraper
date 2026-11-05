"""The HTML / iXBRL report converter (extractor/xhtml_text.py), on hand-made markup shaped
like the filings it was fixed for (AO World, Bang & Olufsen, Novo Nordisk)."""

from extractor.xhtml_text import html_to_text, private_glyphs

POS = 'style="position: absolute; top: {}px"'


def test_positioned_boxes_are_lines_so_table_rows_stay_apart():
    # AO World's staff note: every row a positioned <span>, no tags between rows
    html = ("<div><span {}>Sales, marketing and distribution<span> </span>2,884<span> </span>3,133</span>"
            "<span {}>Directors (Executive and Non-Executive)<span> </span>8<span> </span>7</span>"
            "<span {}>2,892<span> </span>3,140</span></div>").format(POS.format(10), POS.format(20), POS.format(30))
    lines = html_to_text(html).splitlines()
    assert lines == ["Sales, marketing and distribution 2,884 3,133",
                     "Directors (Executive and Non-Executive) 8 7", "2,892 3,140"]


def test_a_private_ligature_glyph_becomes_its_letters():
    fi = "\ue61f"                                    # AO World's "fi"
    text = (f"The {fi}nancial statements. Our pro{fi}t grew. The bene{fi}ts are clear. "
            "Financial review. Profit for the year. Employee benefits.")
    assert private_glyphs(text).startswith("The financial statements. Our profit grew. The benefits")


def test_a_shifted_private_font_is_decoded_with_the_documents_own_words():
    def shift(s, off):
        return "".join(chr(ord(c) + off) for c in s)
    # Bang & Olufsen: letters at +0xE5E3, digits in a second font (U+E8DC is "0")
    letters = shift("Strategy and outlook Remuneration report Financial review", 0xE5E3)
    years = "/".join(shift(y, 0xE8DC - 0x30) for y in ("2025", "26")) + " " + \
        " ".join(shift(y, 0xE8DC - 0x30) for y in ("2024", "2026"))
    plain = "Strategy. Outlook. Remuneration report. Financial review. "
    out = private_glyphs(plain + letters + " " + years)
    assert out.endswith("Strategy and outlook Remuneration report Financial review 2025/26 2024 2026")


def test_an_unknown_private_glyph_is_dropped():
    assert private_glyphs("Icon \uf06f here and there") == "Icon   here and there"


def test_a_shortened_row_of_a_drawn_table_is_found():
    from extractor.validate import quote_in_text
    text = "Total £ Executive Directors\nJohn Roberts FY26 557,080 49,232 22,000 628,312 461,262 920,971\n"
    assert quote_in_text("John Roberts FY26 461,262", text) == "loose"        # cells skipped, in order
    assert quote_in_text("John Roberts 461,262 FY26", text) is None            # not in order
    assert quote_in_text("Executive Directors 461,262", text) is None          # across lines
