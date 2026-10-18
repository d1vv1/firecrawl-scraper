"""LEI lookup and website routing (no network: GLEIF/Wikidata/Firecrawl are faked)."""

import pytest

from extractor import pipeline
from extractor.lei import normalize_legal_name, pick_match
from extractor.website import WebsiteResult, country_adjustment
from extractor.wikidata import choose_website


def _item(lei, name, country="GB", status="ACTIVE", reg="ISSUED", other_names=()):
    return {"id": lei, "attributes": {
        "entity": {"legalName": {"name": name}, "otherNames": [{"name": n} for n in other_names],
                   "legalAddress": {"country": country}, "jurisdiction": country,
                   "legalForm": {"id": "B6ES"}, "status": status, "registeredAs": "00041424"},
        "registration": {"status": reg}}}


# GLEIF's name filter is a contains-search: this is what "Unilever PLC" really returns.
GLEIF_UNILEVER = [
    _item("549300MKFYEKVRWML317", "UNILEVER PLC"),
    _item("549300SWZPWJ6VCGG628", "UNILEVER GHANA PLC", "GH"),
    _item("029200448B5I1F8B5I87", "UNILEVER NIGERIA PLC", "NG"),
    _item("254900B2CN1A29DKM974", "Unilever PLC ADRhedged(TM)", "US"),
    _item("213800L6OOJFDAPTIP96", "UNILEVER PLC SHARE INCENTIVE PLAN"),
]


@pytest.mark.parametrize("a,b", [
    ("Unilever PLC", "UNILEVER PLC"),
    ("Unilever P.L.C.", "UNILEVER PLC"),
    ("Unilever Public Limited Company", "UNILEVER PLC"),
    ("Koninklijke Philips N.V.", "KONINKLIJKE PHILIPS NV"),
    ("Marks & Spencer Group plc", "MARKS AND SPENCER GROUP P.L.C."),
])
def test_normalize_legal_name_equal(a, b):
    assert normalize_legal_name(a) == normalize_legal_name(b)


def test_normalize_keeps_legal_form_distinct():
    assert normalize_legal_name("Unilever PLC") != normalize_legal_name("Unilever N.V.")


def test_pick_match_exact_name_only():
    res = pick_match("Unilever PLC", GLEIF_UNILEVER)
    assert res.record.lei == "549300MKFYEKVRWML317"
    assert res.record.country == "GB"
    assert [c["name_match"] for c in res.candidates].count("exact") == 1


def test_pick_match_none():
    res = pick_match("Unilever Holdings Ltd", GLEIF_UNILEVER)
    assert res.record is None and "no GLEIF record" in res.reason


def test_pick_match_prefers_active_then_ambiguous():
    items = [_item("A", "ACME LTD", "GB", status="INACTIVE"), _item("B", "ACME LTD", "IE")]
    assert pick_match("Acme Limited", items).record.lei == "B"
    items = [_item("A", "ACME LTD", "GB"), _item("B", "ACME LTD", "IE")]
    res = pick_match("Acme Limited", items)
    assert res.record is None and res.reason.startswith("ambiguous")


def test_pick_match_uses_other_names():
    items = [_item("X", "SOCIETE ACME SA", "FR", other_names=["Acme SA"])]
    assert pick_match("Acme SA", items).record.lei == "X"


def test_choose_website():
    assert choose_website(["https://unilever.com"], "unilever") == "https://unilever.com"
    urls = ["https://www.example.org/", "https://www.unilever.com/brands/", "https://en.wikipedia.org/x"]
    assert choose_website(urls, "unilever") == "https://www.unilever.com"
    assert choose_website(["https://en.wikipedia.org/wiki/Unilever"], "unilever") is None


def test_country_adjustment():
    assert country_adjustment("unilever.co.uk", "GB") > 0
    assert country_adjustment("unilever.de", "DE") > 0
    assert country_adjustment("unilever.com.bd", "GB") < 0
    assert country_adjustment("unilever.com", "GB") == 0
    assert country_adjustment("unilever.co.uk", None) == 0


# --- step 2 routing -------------------------------------------------------------

LEI_REC = {"lei": "549300MKFYEKVRWML317", "legal_name": "UNILEVER PLC", "country": "GB"}


class _Calls:
    def __init__(self, monkeypatch, wikidata_site):
        self.wikidata, self.search = [], []

        def fake_wikidata(lei, clean, country=None):
            self.wikidata.append(lei)
            return (wikidata_site, "wikidata Q157062") if wikidata_site else (None, "no item")

        def fake_search(name, fc, country=None):
            self.search.append(country)
            return WebsiteResult("https://www.unilever.com", "unilever.com", 1.0, [])

        monkeypatch.setattr(pipeline, "website_for_lei", fake_wikidata)
        monkeypatch.setattr(pipeline, "find_website", fake_search)
        monkeypatch.setattr(pipeline, "website_for_name", lambda clean, country: (None, "no match"))


def test_lei_and_wikidata_hit_skips_firecrawl(monkeypatch):
    calls = _Calls(monkeypatch, "https://unilever.com")
    r = pipeline.find_official_website("Unilever PLC", fc=None, lei_record=LEI_REC)
    assert r["website"] == "https://unilever.com" and r["website_source"] == "wikidata"
    assert calls.search == []


def test_lei_but_wikidata_miss_searches_with_country(monkeypatch):
    calls = _Calls(monkeypatch, None)
    r = pipeline.find_official_website("Unilever PLC", fc=None, lei_record=LEI_REC)
    assert r["website_source"] == "search+lei"
    assert calls.wikidata == [LEI_REC["lei"]] and calls.search == ["GB"]


def test_no_lei_searches_by_name_only(monkeypatch):
    calls = _Calls(monkeypatch, "https://unilever.com")
    r = pipeline.find_official_website("Unilever PLC", fc=None, lei_record=None)
    assert r["website_source"] == "search"
    assert calls.wikidata == [] and calls.search == [None]


def test_choose_website_rank_and_country():
    philips = [("normal", "https://usa.philips.com"), ("preferred", "https://philips.com"),
               ("normal", "https://philips.nl")]
    assert choose_website(philips, "koninklijke philips", "NL") == "https://philips.com"
    siemens = [("normal", "http://www.siemens.com.mx"), ("normal", "https://www.siemens.com/")]
    assert choose_website(siemens, "siemens", "DE") == "https://www.siemens.com"


@pytest.mark.parametrize("listed,gleif,level", [
    ("Volvo AB", "Aktiebolaget Volvo", "exact"),
    ("AB Volvo (publ)", "Aktiebolaget Volvo", "exact"),
    ("Atlas Copco AB", "ATLAS COPCO AKTIEBOLAG", "exact"),
    ("Orsted A/S", "ØRSTED A/S", "exact"),
    ("Novo Nordisk A/S", "NOVO NORDISK A/S", "exact"),
    ("Sampo plc", "Sampo Oyj", "exact"),
    ("Nordea Bank Oyj", "Nordea Bank Abp", "exact"),
    ("Equinor", "EQUINOR ASA", "exact"),                 # no form given: compatible
    ("Hennes & Mauritz AB", "H & M Hennes & Mauritz AB", "partial"),
    ("Volvo AB", "Volvo Car AB", None),                  # extra words after = other company
    ("Equinor ASA", "EQUINOR ASSET MANAGEMENT AS", None),  # ASA vs AS
    ("Unilever PLC", "UNILEVER N.V.", None),
])
def test_match_level_nordic_forms(listed, gleif, level):
    from extractor.lei import match_level
    assert match_level(listed, gleif) == level


def test_partial_prefers_closest_and_exact_beats_partial():
    items = [_item("HM", "H & M Hennes & Mauritz AB", "SE"),
             _item("GBC", "H & M Hennes & Mauritz GBC AB", "SE")]
    assert pick_match("Hennes & Mauritz AB", items, "SE").record.lei == "HM"
    items = [_item("CAR", "Volvo Car AB", "SE"), _item("VOLVO", "Aktiebolaget Volvo", "SE")]
    res = pick_match("Volvo AB", items, "SE")
    assert res.record.lei == "VOLVO" and res.reason == "exact name match"


def test_country_prefers_home_registration():
    items = [_item("SE1", "ACME AB", "SE"), _item("NO1", "ACME AB", "NO")]
    assert pick_match("Acme AB", items, "NO").record.lei == "NO1"
    assert pick_match("Acme AB", items, None).record is None      # ambiguous without country


def test_search_text_strips_forms():
    from extractor.lei import search_text
    assert search_text("AB Volvo (publ)") == "Volvo"
    assert search_text("Hennes & Mauritz AB") == "Hennes & Mauritz"
    assert search_text("Novo Nordisk A/S") == "Novo Nordisk"
    assert search_text("Atlas Copco Aktiebolag") == "Atlas Copco"


def test_choose_website_prefers_english_tagged_and_generic_tld():
    equinor = [("normal", "https://equinor.com", True), ("normal", "https://equinor.no", False),
               ("normal", "https://equinor.jp/en", True), ("normal", "https://equinor.ar", False)]
    assert choose_website(equinor, "equinor", "NO") == "https://equinor.com"
    # untagged: generic .com beats the home-country TLD
    assert choose_website(["https://acme.se", "https://acme.com"], "acme", "SE") == "https://acme.com"
    assert choose_website(["https://acme.se", "https://acme.de"], "acme", "SE") == "https://acme.se"


class _FC:
    pass


def test_wikidata_site_without_report_falls_back_to_search(monkeypatch, tmp_path):
    from extractor.report_finder import ReportNotFoundError, ReportResult
    monkeypatch.setattr(pipeline, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pipeline, "website_for_lei", lambda lei, clean, country=None:
                        ("https://www2.hm.com", "wikidata Q188326"))
    monkeypatch.setattr(pipeline, "find_website", lambda name, fc, country=None:
                        WebsiteResult("https://hmgroup.com", "hmgroup.com", 0.8, []))
    tried = []

    def fake_find_report(site, fc, country=None, **kwargs):
        tried.append(site)
        if "hm.com" in site and "hmgroup" not in site:
            raise ReportNotFoundError("nothing on the shop site")
        return ReportResult("https://hmgroup.com/annual-report-2025.pdf", 2025, True, [])
    monkeypatch.setattr(pipeline, "find_report", fake_find_report)
    found = pipeline.discover("Hennes & Mauritz AB", "h-m", _FC(), None, None, False,
                              {"lei": "X", "country": "SE"}, "SE")
    assert tried == ["https://www2.hm.com", "https://hmgroup.com"]
    assert found["website"] == "https://hmgroup.com"
    assert found["report_url"].endswith("annual-report-2025.pdf")


@pytest.mark.parametrize("listed,gleif,level", [
    ("Metsä Board Corporation", "Metsä Board Oyj", "exact"),
    ("Nokia Corporation", "Nokia Oyj", "exact"),
    ("Otello Corp ASA", "OTELLO CORPORATION ASA", "exact"),
    ("Bakkafrost P/F", "P/F Bakkafrost", "exact"),
    ("Neste Corporation", "NESTE ASSET MANAGEMENT AS", None),
])
def test_corporation_is_a_weak_form(listed, gleif, level):
    from extractor.lei import match_level
    assert match_level(listed, gleif) == level


def test_current_legal_name_beats_former_name():
    items = [_item("WITH", "WithSecure Oy", "FI", other_names=["F-Secure Oyj", "WithSecure Oyj"]),
             _item("NEW", "F-Secure Oyj", "FI", other_names=["F-Secure Corporation"])]
    assert pick_match("F-Secure Oyj", items, "FI").record.lei == "NEW"
    items = [_item("DAN", "ASETEK DANMARK A/S", "DK", other_names=["ASETEK A/S"]),
             _item("ASE", "ASETEK A/S", "DK")]
    assert pick_match("Asetek A/S", items, "DK").record.lei == "ASE"


def test_wikidata_name_search_is_used_before_paid_search(monkeypatch):
    calls = _Calls(monkeypatch, None)                         # LEI not on Wikidata
    monkeypatch.setattr(pipeline, "website_for_name", lambda clean, country:
                        ("https://www.medivir.com", "wikidata name search Q10579256 (Medivir)")
                        if country == "SE" else (None, "no match"))
    r = pipeline.find_official_website("Medivir AB", fc=None, lei_record=LEI_REC | {"country": "SE"},
                                       country="SE")
    assert r["website_source"] == "wikidata-name" and calls.search == []


def test_name_search_miss_falls_through_to_paid_search(monkeypatch):
    calls = _Calls(monkeypatch, None)
    monkeypatch.setattr(pipeline, "website_for_name", lambda clean, country: (None, "no match"))
    r = pipeline.find_official_website("Unilever PLC", fc=None, lei_record=LEI_REC)
    assert r["website_source"] == "search+lei" and calls.search == ["GB"]
