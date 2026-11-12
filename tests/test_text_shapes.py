"""Text shapes that kept real quotes from matching the source. Found 12 November 2026 in
the quotes the second look (extractor/requote.py) returned unchanged: the passage was in
the report, the matcher did not see it."""
from extractor.validate import figure_in_quote, quote_in_text


def test_the_converters_picture_text_marks_are_not_the_reports_text():
    # in 609 of 2,768 cached texts; Villeroy & Boch's report is drawn as pictures throughout
    text = ("Group is a leading ceramic manufacturer. <!-- End of picture text -->\n"
            "<!-- Start of picture text -->\nComprehensive lifestyle provider,")
    assert quote_in_text("ceramic manufacturer. Comprehensive lifestyle provider", text)
    assert quote_in_text("Prime Standard", "Prime <!-- End of picture text --> Standard of Deutsche Börse")


def test_a_full_stop_without_a_character_code():
    assert quote_in_text("EBITDA 45.5 148.4 193.9", "|EBITDA|45�5|148�4|193�9|")
    assert figure_in_quote(45.5, "|EBITDA|45�5|148�4|")
    assert quote_in_text("Company's website www.verbio.de",
                         "the Company's website www�verbio�de� VERBIO Annual Report")


def test_a_footnote_mark_reads_the_same_however_written():
    row = "|Other compensation<sup>4</sup>|72|32|"
    assert quote_in_text("Other compensation4|72|32", row)
    assert quote_in_text("Other compensation⁴ 72 32", row)
    # after a figure it stays apart: 1,234 with note 2 is not 12,342
    assert figure_in_quote(1234, "Revenue 1,234² 1,100")
    assert not figure_in_quote(12342, "Revenue 1,234² 1,100")
    assert figure_in_quote(1234, "|Revenue|1,234<sup>2</sup>|")


def test_a_word_broken_at_a_line_end():
    text = "in Germany, with the remain-\ning 9,572 employed outside Germany"
    assert quote_in_text("with the remaining 9,572 employed outside Germany", text)
    assert not quote_in_text("the remaining 9,573 employed", text)
