"""Report-URL filters on real European/Nordic file names (collected from IR pages)."""

import pytest

from extractor.report_finder import classify, fold, pick_best, search_terms

ATLAS = ("https://www.atlascopcogroup.com/content/dam/atlas-copco/group/documents/investors/"
         "financial-publications/english/20250320-annual-report-2024-incl-sustainability-report"
         "-and-corporate-governance-report-copy-of-the-official-ESEF-format.pdf")
NOVO = "https://www.novonordisk.com/content/dam/nncorp/global/en/investors/irmaterial/annual_report/2026/"


def best(urls):
    return pick_best([classify(u) for u in urls]).url


def test_fold_transliterations():
    assert fold("Årsrapport") == fold("aarsrapport") == fold("arsrapport")
    assert fold("Geschäftsbericht") == fold("geschaeftsbericht")
    assert fold("Bæredygtighed") == fold("baeredygtighed")
    assert fold("Tilinpäätös") == fold("tilinpaatos")


@pytest.mark.parametrize("url", [
    ATLAS,
    "https://x.se/media/ars-och-hallbarhetsredovisning-2024.pdf",
    "https://x.se/media/Års- och hållbarhetsredovisning 2024.pdf",
    "https://x.com/annual-and-sustainability-report-2024.pdf",
    "https://x.se/rapporter/arsredovisning-2024.pdf",
    "https://x.no/rapporter/aarsrapport-2024.pdf",
    "https://x.dk/investor/%C3%A5rsrapport-2024.pdf",              # årsrapport, URL-encoded
    "https://x.fi/sijoittajat/vuosikertomus-2024.pdf",
    "https://x.fi/en/KONE Financial Statements 2025.pdf",
    "https://x.is/fjarfestar/arsskyrsla-2024.pdf",
    "https://x.de/berichte/Geschaeftsbericht_2024_EN.pdf",
    "https://imagepool.1und1.ag/v2/download/berichte/GB_1u1_2025_ENG.pdf",
    "https://x.nl/jaarverslag-2024.pdf",
])
def test_keeps_european_annual_reports(url):
    assert classify(url).kept, classify(url).reason


@pytest.mark.parametrize("url", [
    "https://x.se/rapporter/delarsrapport-q3-2025.pdf",
    "https://x.se/rapporter/delårsrapport-januari-september-2025.pdf",
    "https://x.se/bokslutskommunike-2025.pdf",
    "https://x.se/hallbarhetsredovisning-2024.pdf",
    "https://x.se/bolagsstyrningsrapport-2024.pdf",
    "https://x.no/kvartalsrapport-2025.pdf",
    "https://x.dk/halvaarsrapport-2025.pdf",
    "https://x.fi/osavuosikatsaus-q2-2025.pdf",
    "https://x.fi/tilinpaatostiedote-2025.pdf",
    "https://x.fi/en/KONE Financial Statement Bulletin 2023.pdf",
    "https://imagepool.1und1.ag/v2/download/berichte/1und1-AG_GB-2024_Jahresabschluss.pdf",
    "https://imagepool.1und1.ag/v2/download/berichte/1und1-AG_H1-2026_EN.pdf",
    "https://imagepool.1und1.ag/v2/download/berichte/1u1_Quartalsbericht_Q1_26_en.pdf",
    NOVO + "novo-nordisk-tax-report-2025.pdf",
    NOVO + "novo-nordisk-remuneration-report-2025.pdf",
    NOVO + "novo-nordisk-corporate-governance-report-2025.pdf",
    "https://x.com/sustainability-annual-report-2024.pdf",
    "https://x.com/en/gb/annual-report-2024-esg-supplement.pdf",
])
def test_excludes_non_annual_documents(url):
    assert not classify(url).kept


def test_gb_only_counts_in_file_name_next_to_year():
    assert not classify("https://x.com/gb/en/investors/results-2024.pdf").kept
    assert classify("https://x.com/gb/en/investors/annual-report-2024.pdf").kept


def test_english_beats_native_same_year():
    assert best(["https://imagepool.1und1.ag/v2/download/berichte/GB_1u1_2025_DEU.pdf",
                 "https://imagepool.1und1.ag/v2/download/berichte/GB_1u1_2025_ENG.pdf"]
                ).endswith("ENG.pdf")
    assert best(["https://x.se/sv/arsredovisning-2024.pdf",
                 "https://x.se/en/annual-report-2024.pdf"]).endswith("/en/annual-report-2024.pdf")


def test_newer_year_still_wins_over_language():
    # Out of scope language, but a 2-year-old English report is worse; we log a warning.
    assert best(["https://x.se/sv/arsredovisning-2025.pdf",
                 "https://x.se/en/annual-report-2023.pdf"]).endswith("2025.pdf")


def test_file_name_keyword_beats_folder_keyword():
    assert best([NOVO + "novo-nordisk-annual-report-2025.pdf",
                 NOVO + "novo-nordisk-form-20-f-2025.pdf"]).endswith("annual-report-2025.pdf")
    assert classify(NOVO + "novo-nordisk-annual-report-2025.pdf").year == 2025


def test_search_terms_use_lei_country():
    assert search_terms("SE") == ["annual report", "årsredovisning", "integrated report", "investors"]
    assert search_terms("GB") == ["annual report", "integrated report", "investors"]
    assert search_terms(None) == ["annual report", "integrated report", "investors"]
