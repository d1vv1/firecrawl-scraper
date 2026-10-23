"""The validation scorer: number parsing, units and code comparisons."""

from extractor import protocol_score as ps


def test_numbers_and_units():
    assert ps.numbers("580,945 (net sales 574,203)") == [580945.0, 574203.0]
    assert ps.scale_of("thousands") == 1e3 and ps.scale_of("EUR m millions") == 1e6


def test_compare_numbers_and_codes():
    theirs = {"value": "640,849", "unit": "thousands"}
    assert ps.compare("C13", theirs, [{"value": "640849000"}]) == "match"
    assert ps.compare("C13", theirs, [{"value": "1"}]) == "differs"
    assert ps.compare("C04", {"value": "CH0010702154", "unit": ""},
                      [{"value": "CH0010702154"}]) == "match"
    assert ps.compare("C03", {"value": "FN 78543f", "unit": ""}, [{"value": "FN 78543 f"}]) == "match"
    assert ps.compare("C11", {"value": "anything", "unit": ""}, [{"value": "x"}]) == "found"


def test_space_separators_and_identifiers_inside_text():
    assert ps.numbers("6 228 784 092") == [6228784092.0]
    assert ps.compare("C03", {"value": "NIF A31065618 (IARC cover A-31065618); GLEIF RA000533", "unit": ""},
                      [{"value": "A-31.065.618"}]) == "match"
    assert ps.compare("C03", {"value": "00881841001 (registeredAt RA000407)", "unit": ""},
                      [{"value": "00881841001"}]) == "match"
    assert ps.compare("C08", {"value": "Incorporated LU; HQ Betzdorf", "unit": ""},
                      [{"value": "LU"}]) == "match"
