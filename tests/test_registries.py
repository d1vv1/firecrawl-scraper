"""Company registries (Norway, Denmark): offline tests with recorded shapes."""

import httpx

from extractor import registries
from extractor.registries import RegistryFiling, find_filing, org_number, xbrl_facts

DK_XBRL = b"""<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance"
  xmlns:xbrldi="http://xbrl.org/2006/xbrldi" xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
  xmlns:fsa="http://xbrl.dcca.dk/fsa" xmlns:gsd="http://xbrl.dcca.dk/gsd">
 <xbrli:context id="y"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:context id="yg"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="cmn:ConsolidatedSoloDimension">cmn:ConsolidatedMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:context id="e"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
 <xbrli:context id="eg"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="cmn:ConsolidatedSoloDimension">cmn:ConsolidatedMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
 <xbrli:context id="prev"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2024-01-01</xbrli:startDate><xbrli:endDate>2024-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:unit id="DKK"><xbrli:measure>iso4217:DKK</xbrli:measure></xbrli:unit>
 <fsa:Revenue contextRef="prev" unitRef="DKK" decimals="-3">900000</fsa:Revenue>
 <fsa:Revenue contextRef="y" unitRef="DKK" decimals="-3">1000000</fsa:Revenue>
 <fsa:Revenue contextRef="yg" unitRef="DKK" decimals="-3">1500000</fsa:Revenue>
 <fsa:Assets contextRef="e" unitRef="DKK" decimals="-3">2000000</fsa:Assets>
 <fsa:Assets contextRef="eg" unitRef="DKK" decimals="-3">2600000</fsa:Assets>
 <fsa:LiabilitiesAndEquity contextRef="eg" unitRef="DKK" decimals="-3">2600000</fsa:LiabilitiesAndEquity>
 <fsa:AverageNumberOfEmployees contextRef="y" decimals="0">42</fsa:AverageNumberOfEmployees>
</xbrli:xbrl>"""


def test_danish_xbrl_prefers_group_figures_for_the_year():
    figs, employees = xbrl_facts(DK_XBRL, "2025-01-01", "2025-12-31")
    assert figs["revenue"].value == 1_500_000 and figs["revenue"].scope == "consolidated"
    assert figs["revenue"].concept == "fsa:Revenue" and figs["revenue"].currency == "DKK"
    assert figs["total_assets"].value == 2_600_000
    assert figs["total_equity_and_liabilities"].value == 2_600_000
    assert employees == 42


def test_danish_xbrl_without_group_is_the_whole_company():
    no_group = DK_XBRL.replace(b'contextRef="yg"', b'contextRef="none"').replace(
        b'contextRef="eg"', b'contextRef="none"')
    # still has ConsolidatedMember contexts declared, but no facts use them: drop them too
    no_group = no_group.replace(b"cmn:ConsolidatedMember", b"cmn:SomethingElse")
    figs, _ = xbrl_facts(no_group, "2025-01-01", "2025-12-31")
    assert figs["revenue"].value == 1_000_000 and figs["revenue"].scope == "consolidated"


def test_org_number_from_lei_record():
    assert org_number({"registered_as": "916 359 667"}) == "916359667"
    assert org_number({"registered_as": None}) is None


BRREG_ACCOUNTS = [
    {"id": 1, "journalnr": "J1", "regnskapstype": "SELSKAP",
     "virksomhet": {"organisasjonsnummer": "912007782", "morselskap": True},
     "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"}, "valuta": "NOK",
     "resultatregnskapResultat": {"driftsresultat": {"driftsinntekter": {"sumDriftsinntekter": 10.0}}},
     "eiendeler": {"sumEiendeler": 20.0}, "egenkapitalGjeld": {"sumEgenkapitalGjeld": 20.0}},
    {"id": 2, "journalnr": "J2", "regnskapstype": "KONSERN",
     "virksomhet": {"organisasjonsnummer": "912007782", "morselskap": True},
     "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"}, "valuta": "NOK",
     "resultatregnskapResultat": {"driftsresultat": {"driftsinntekter": {"salgsinntekter": 4400000000.0,
                                                                         "sumDriftsinntekter": 4446534000.0}}},
     "eiendeler": {"sumEiendeler": 3281210000.0}, "egenkapitalGjeld": {"sumEgenkapitalGjeld": 3281209000.0}},
    {"id": 3, "journalnr": "J0", "regnskapstype": "KONSERN",
     "virksomhet": {"organisasjonsnummer": "912007782", "morselskap": True},
     "regnskapsperiode": {"fraDato": "2024-01-01", "tilDato": "2024-12-31"}, "valuta": "NOK",
     "eiendeler": {"sumEiendeler": 1.0}, "egenkapitalGjeld": {"sumEgenkapitalGjeld": 1.0}},
]
BRREG_ENTITY = {"organisasjonsnummer": "912007782", "navn": "GLAMOX AS",
                "organisasjonsform": {"kode": "AS", "beskrivelse": "Aksjeselskap"},
                "naeringskode1": {"kode": "27.400", "beskrivelse": "Produksjon av belysningsutstyr"},
                "antallAnsatte": 484, "aktivitet": ["Produksjon og salg av belysning."]}


def _fake_request(responses):
    def fake(method, url, **kw):
        for key, body in responses.items():
            if key in url:
                return httpx.Response(200, json=body, request=httpx.Request(method, url))
        return httpx.Response(404, request=httpx.Request(method, url))
    return fake


def test_norway_latest_group_accounts(monkeypatch):
    monkeypatch.setattr(registries, "_request", _fake_request({
        "regnskapsregisteret": BRREG_ACCOUNTS, "enhetsregisteret/api/enheter/": BRREG_ENTITY}))
    filing, why = find_filing("Glamox", "NO", {"lei": "L", "country": "NO", "registered_as": "912007782"})
    assert filing.fiscal_year == "2025" and "group" in why and "LEI record" in why
    # sales revenue, not total operating income (the golden values use sales revenue)
    assert filing.figures["revenue"].value == 4400000000 and filing.figures["revenue"].scope == "consolidated"
    assert filing.figures["revenue"].concept == "brreg:salgsinntekter"
    assert filing.figures["revenue"].period == "2025-01-01/2025-12-31"
    assert filing.employees == 484 and "Produksjon og salg av belysning" in filing.profile_text
    assert filing.identifier == "org. no. 912007782"
    assert RegistryFiling.from_dict(filing.as_dict()) == filing


def test_norway_company_accounts_of_a_parent_are_parent_only(monkeypatch):
    only_company = [a for a in BRREG_ACCOUNTS if a["regnskapstype"] == "SELSKAP"]
    monkeypatch.setattr(registries, "_request", _fake_request({
        "regnskapsregisteret": only_company, "enhetsregisteret/api/enheter/": BRREG_ENTITY}))
    filing, _ = find_filing("Glamox", "NO", {"lei": "L", "country": "NO", "registered_as": "912007782"})
    assert filing.figures["revenue"].scope == "parent_only"


def test_norway_name_search_needs_one_exact_match(monkeypatch):
    search = {"_embedded": {"enheter": [{"organisasjonsnummer": "1", "navn": "HURTIGRUTEN EIENDOM AS"},
                                        {"organisasjonsnummer": "2", "navn": "BRUBAKKEN AS"},
                                        {"organisasjonsnummer": "3", "navn": "BRUBAKKEN AS"}]}}
    monkeypatch.setattr(registries, "_request", _fake_request({"enhetsregisteret/api/enheter": search}))
    assert find_filing("Hurtigruten", "NO", None)[0] is None
    filing, why = find_filing("Brubakken", "NO", None)
    assert filing is None and "ambiguous" in why


def test_no_registry_for_other_countries():
    assert find_filing("Volvo AB", "SE", None) == (None, "no open registry for SE")


def test_uk_needs_a_key(monkeypatch):
    monkeypatch.setattr(registries, "ch_key", lambda: None)
    assert not registries.available("GB") and registries.available("NO")
    assert find_filing("Tesco PLC", "GB", None) == (None, "no COMPANIES_HOUSE_API_KEY in .env")


def test_uk_company_number_from_lei():
    from extractor.registries import gb_number
    assert gb_number({"registered_as": "445790"}) == "00445790"
    assert gb_number({"registered_as": "SC177553"}) == "SC177553"
    assert gb_number({"registered_as": None}) is None


UK_IXBRL = """<html xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"><body>
<div style="display:none"><ix:header><ix:resources>
 <xbrli:context id="cy"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:context id="cy-grp"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="bus:GroupCompanyDataDimension">bus:ConsolidatedGroupCompanyDataMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:context id="end-grp"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="bus:GroupCompanyDataDimension">bus:ConsolidatedGroupCompanyDataMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
 <xbrli:context id="prev"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2024-01-01</xbrli:startDate><xbrli:endDate>2024-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:unit id="GBP"><xbrli:measure>iso4217:GBP</xbrli:measure></xbrli:unit>
</ix:resources></ix:header></div>
<p>Turnover <ix:nonFraction name="core:TurnoverRevenue" contextRef="cy" unitRef="GBP" scale="3" decimals="-3" format="ixt:num-dot-decimal">9,000</ix:nonFraction>
 group <ix:nonFraction name="core:TurnoverRevenue" contextRef="cy-grp" unitRef="GBP" scale="3" decimals="-3" format="ixt:num-dot-decimal"><b>12,345</b></ix:nonFraction>
 last year <ix:nonFraction name="core:TurnoverRevenue" contextRef="prev" unitRef="GBP" scale="3" format="ixt:num-dot-decimal">8,000</ix:nonFraction></p>
<p>Fixed <ix:nonFraction name="core:FixedAssets" contextRef="end-grp" unitRef="GBP" scale="3" format="ixt:num-dot-decimal">4,000</ix:nonFraction>
 Current <ix:nonFraction name="core:CurrentAssets" contextRef="end-grp" unitRef="GBP" scale="3" format="ixt:num-dot-decimal">6,500</ix:nonFraction>
 Employees <ix:nonFraction name="core:AverageNumberEmployeesDuringPeriod" contextRef="cy" unitRef="pure" format="ixt:num-dot-decimal">120</ix:nonFraction>
 Loss <ix:nonFraction name="core:ProfitLoss" contextRef="cy" unitRef="GBP" sign="-" format="ixt:num-dot-decimal">50</ix:nonFraction></p>
</body></html>"""


def test_uk_ixbrl_group_turnover_and_computed_total_assets():
    from extractor.ixbrl import ixbrl_facts
    figs, employees = ixbrl_facts(UK_IXBRL, "2025-12-31")
    assert figs["revenue"].value == 12_345_000 and figs["revenue"].scope == "consolidated"
    assert figs["revenue"].concept == "core:TurnoverRevenue" and figs["revenue"].currency == "GBP"
    # UK balance sheets have no total-assets line: fixed + current
    assert figs["total_assets"].value == 10_500_000
    assert figs["total_assets"].concept == "core:FixedAssets + core:CurrentAssets"
    assert "total_equity_and_liabilities" not in figs
    assert employees == 120


def test_psc_bands_and_the_protocol_controlling_owner(monkeypatch):
    from extractor import apis
    assert apis.psc_band({"natures_of_control": ["ownership-of-shares-25-to-50-percent"]}) == 25
    assert apis.psc_band({"natures_of_control": ["voting-rights-75-to-100-percent",
                                                 "ownership-of-shares-50-to-75-percent"]}) == 75
    assert apis.psc_band({"natures_of_control": ["significant-influence-or-control"]}) == 0
    responses = {
        "/company/SC205718": {"company_number": "SC205718", "company_name": "TWMA GROUP LIMITED",
                              "type": "ltd", "sic_codes": ["70100"],
                              "registered_office_address": {"locality": "Aberdeen"}},
        "/company/SC205718/persons-with-significant-control": {"items": [
            {"name": "Bp Inv3 Bidco Limited", "kind": "corporate-entity-person-with-significant-control",
             "natures_of_control": ["ownership-of-shares-25-to-50-percent"]}]},
    }
    monkeypatch.setattr(apis, "_cached", lambda url, fetch: responses.get(
        url.replace(apis.registries.CH_API, "")))
    monkeypatch.setattr(apis.registries, "ch_key", lambda: "key")
    got = {f.data_point: f for f in apis.companies_house_values("SC205718")}
    assert got["controlling_owner_name"].value == "Bp Inv3 Bidco Limited"   # 25%+ counts (20% rule)
    assert got["controlling_owner"].value == "corporate"
    assert "ultimate_parent" not in got                                      # under 50%: not the parent
