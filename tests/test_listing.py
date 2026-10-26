"""Exchange data points from FIRDS, the MIC list and OpenFIGI (no network)."""

import pytest

from extractor import listing

MICS = {
    "XSTO": {"operating": "XSTO", "name": "NASDAQ STOCKHOLM AB", "category": "RMKT", "country": "SE"},
    "DSTO": {"operating": "XSTO", "name": "NASDAQ STOCKHOLM AB - NORDIC@MID", "category": "RMKT", "country": "SE"},
    "FNSE": {"operating": "XSTO", "name": "FIRST NORTH SWEDEN", "category": "MLTF", "country": "SE"},
    "XLON": {"operating": "XLON", "name": "LONDON STOCK EXCHANGE", "category": "RMKT", "country": "GB"},
    "XAMS": {"operating": "XAMS", "name": "EURONEXT - EURONEXT AMSTERDAM", "category": "RMKT", "country": "NL"},
    "XCSE": {"operating": "XCSE", "name": "NASDAQ COPENHAGEN A/S", "category": "RMKT", "country": "DK"},
}


def rec(isin, mic, start, end=None, issuer="Yes", name=""):
    return {"isin": isin, "mic": mic, "mrkt_issr_trdng_rqst_flag": issuer, "gnr_full_name": name,
            "mrkt_trdng_start_date": start + "T00:00:00Z",
            **({"mrkt_trdng_trmination_date": end + "T00:00:00Z"} if end else {})}


@pytest.fixture
def offline(monkeypatch):
    monkeypatch.setattr(listing, "_mics", MICS)
    figi = {}
    monkeypatch.setattr(listing, "openfigi", lambda isin, exch: figi.get((isin, exch), []))
    return figi


def test_home_listing_with_two_share_classes_and_a_closed_london_line(offline, monkeypatch):
    docs = [rec("SE0000115420", "XSTO", "1998-03-12", name="VOLVO A"),
            rec("SE0000115446", "XSTO", "1998-03-12", name="VOLVO B"),
            rec("SE0000115446", "DSTO", "1998-03-12"),
            rec("SE0000115446", "XLON", "2008-01-10", end="2017-11-17"),
            rec("SE0000115446", "XAMS", "2019-01-01", issuer="No")]
    monkeypatch.setattr(listing, "firds_shares", lambda lei: docs)
    offline[("SE0000115446", "SS")] = [{"ticker": "VOLVB", "marketSector": "Equity"}]
    got = {f.data_point: f for f in listing.listing_values("LEI", "SE")}
    assert got["isin"].value == "SE0000115420; SE0000115446" and got["isin"].confidence == "A"
    assert got["exchange"].value == "Nasdaq Stockholm" and "regulated market" in got["exchange"].note
    assert got["listing_status"].value == "listed"
    assert got["ticker"].value == "VOLVB"          # the class with the most venue records
    assert "listing_date" not in got                # 1998: before FIRDS dates can be trusted
    assert "exchange_segment" not in got            # a regulated market: segment left to documents


def test_recent_mtf_listing_gives_segment_and_a_c_graded_date(offline, monkeypatch):
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [
        rec("SE0010323311", "FNSE", "2017-10-12"), rec("SE0010323311", "XSTO", "2017-10-12")])
    got = {f.data_point: f for f in listing.listing_values("LEI", "SE")}
    assert got["exchange_segment"].value == "First North Sweden"
    assert got["listing_date"].value == "2017-10-12" and got["listing_date"].confidence == "C"


def test_placeholder_dates_and_new_isins_are_not_listing_dates(offline, monkeypatch):
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [
        rec("DK0062498333", "XCSE", "2023-09-13"),
        rec("DK0060534915", "XCSE", "1998-10-24", end="2023-09-12")])
    got = {f.data_point: f for f in listing.listing_values("LEI", "DK")}
    assert got["isin"].value == "DK0062498333"      # the old ISIN's line is closed
    assert "listing_date" not in got                # the company traded long before 2023
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [rec("DK0010218429", "XCSE", "2016-01-01")])
    assert "listing_date" not in {f.data_point for f in listing.listing_values("LEI", "DK")}


def test_uk_company_gets_its_london_listing_from_openfigi(offline, monkeypatch):
    # London lines end at Brexit in FIRDS; Shell's live FIRDS listing is Amsterdam.
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [
        rec("GB00BP6MXD84", "XAMS", "2022-01-31"),
        rec("GB00BP6MXD84", "XLON", "2022-01-31", end="2020-12-31")])
    offline[("GB00BP6MXD84", "LN")] = [{"ticker": "SHEL", "marketSector": "Equity"}]
    got = {f.data_point: f for f in listing.listing_values("LEI", "GB")}
    assert got["exchange"].value == "London Stock Exchange" and got["ticker"].value == "SHEL"
    assert got["isin"].value == "GB00BP6MXD84" and got["isin"].source == "OpenFIGI"


def test_uk_isin_from_gleif_and_london_ticker_slash_dropped(offline, monkeypatch):
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [])
    offline[("GB00BJTNFH41", "LN")] = [{"ticker": "AO/", "marketSector": "Equity"}]
    got = {f.data_point: f for f in listing.listing_values("LEI", "GB", ["XS1234567890", "GB00BJTNFH41"])}
    assert got["ticker"].value == "AO" and got["isin"].value == "GB00BJTNFH41"


def test_no_records_gives_nothing(offline, monkeypatch):
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [rec("NO0010", "XLON", "2010-01-01", issuer="No")])
    assert listing.listing_values("LEI", "NO") == []
    assert listing.listing_values(None, "NO") == []


def test_ticker_keeps_the_exchange_spelling_from_a_document():
    from extractor import datapoints as dp
    from extractor.apis import Found
    figi = Found("ticker", "VOLVB", source="OpenFIGI", method="API", confidence="B")
    doc = Found("ticker", "VOLV B", source="Annual report (PDF)", method="PARSE", confidence="B")
    adr = Found("ticker", "NVO", source="Share information (web page)", method="SCRAPE", confidence="B")
    assert dp.best([figi, doc])["ticker"].value == "VOLV B"
    novo = dp.best([Found("ticker", "NOVOB", source="OpenFIGI", method="API", confidence="B"), adr])
    assert novo["ticker"].value == "NOVOB" and "other source says NVO" in novo["ticker"].note
