"""SEC EDGAR route (no network: SEC-shaped sample data)."""

from extractor import edgar

FACTS = {"facts": {"us-gaap": {
    "Revenues": {"units": {"USD": [
        {"start": "2024-01-01", "end": "2024-12-31", "val": 45042700000, "accn": "0000059478-25-000067", "form": "10-K"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 65179000000, "accn": "0000059478-26-000013", "form": "10-K"},
        {"start": "2025-10-01", "end": "2025-12-31", "val": 19000000000, "accn": "0000059478-26-000013", "form": "10-K"},
        {"start": "2024-01-01", "end": "2024-12-31", "val": 45042700000, "accn": "0000059478-26-000013", "form": "10-K"}]}},
    "Assets": {"units": {"USD": [
        {"end": "2025-12-31", "val": 101500000000, "accn": "0000059478-26-000013", "form": "10-K"},
        {"end": "2024-12-31", "val": 78700000000, "accn": "0000059478-26-000013", "form": "10-K"}]}},
    "LiabilitiesAndStockholdersEquity": {"units": {"USD": [
        {"end": "2025-12-31", "val": 101500000000, "accn": "0000059478-26-000013", "form": "10-K"}]}},
}}}


def test_tagged_figures_from_the_chosen_filing_only():
    figs = edgar.tagged_figures(FACTS, "0000059478-26-000013", "2025-12-31")
    assert figs["revenue"].value == 65179000000          # full year, not the Q4 figure
    assert figs["revenue"].period == "2025-01-01/2025-12-31"
    assert figs["revenue"].currency == "USD" and figs["revenue"].concept == "us-gaap:Revenues"
    assert figs["total_assets"].value == 101500000000
    assert figs["total_equity_and_liabilities"].value == 101500000000


def test_ifrs_filers_and_other_currencies():
    facts = {"facts": {"ifrs-full": {"Revenue": {"units": {"EUR": [
        {"start": "2025-01-01", "end": "2025-12-31", "val": 1.0e9, "accn": "A", "form": "20-F"}]}}}}}
    figs = edgar.tagged_figures(facts, "A", "2025-12-31")
    assert figs["revenue"].currency == "EUR" and figs["revenue"].concept == "ifrs-full:Revenue"


def test_find_cik_matches_names_like_the_lei_lookup(monkeypatch):
    rows = [{"cik_str": 59478, "ticker": "LLY", "title": "ELI LILLY & Co"},
            {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
            {"cik_str": 1, "ticker": "X", "title": "Willis Towers Watson plc"}]
    monkeypatch.setattr(edgar, "_tickers", lambda: rows)
    assert edgar.find_cik("ELI LILLY AND COMPANY")[0] == 59478
    assert edgar.find_cik("Apple Inc.")[0] == 320193
    assert edgar.find_cik("Willis Towers Watson Public Limited Company")[0] == 1
    assert edgar.find_cik("Unknown Widgets Inc")[0] is None


def test_missing_contact_is_a_clear_error(monkeypatch):
    import pytest
    monkeypatch.setattr(edgar, "load_settings", lambda: None)
    monkeypatch.delenv("SEC_CONTACT", raising=False)
    with pytest.raises(edgar.SecContactMissing, match="SEC_CONTACT"):
        edgar._headers()
