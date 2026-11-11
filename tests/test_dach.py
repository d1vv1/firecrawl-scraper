"""DACH: the report found by a web search, German and French keywords."""

import datetime as dt

from extractor import report_finder as rf
from extractor.sections import Chunk, select_chunks
from tests.test_run_fixes import FakeFC

YEAR = dt.date.today().year - 1


def test_only_the_companys_own_documents_count():
    own = rf.own_document
    assert own("https://report.adidas-group.com/2025/en/annual-report-adidas-ar25.pdf", "ADIDAS AG NA O.N.", "https://www.adidas.com")
    assert own("https://www.bellfoodgroup.com/en/investors/annual-report", "Bell Food Group AG", "http://www.bell.ch")
    assert not own("https://www.bellfg.com.au/bfg-2025-annual-report/", "Bell Food Group AG", "http://www.bell.ch")
    assert not own("https://www.datocms-assets.com/1/brickworks_fy25_annual_report.pdf", "BKW AG", "https://www.bkw.ch")
    assert own("https://www.bcj.ch/fr/Rapport-de-gestion-2025.html", "Banque Cantonale du Jura SA", "https://www.bcj.ch")
    assert not own("https://www.bcv.ch/rapports/rapport-annuel-2025.pdf", "Banque Cantonale du Jura SA", "https://www.bcj.ch")
    assert own("https://a.storyblok.com/f/2/x/e5/32845-essentra-ar2025-interactive.pdf", "Essentra plc", "https://www.essentraplc.com")
    assert not own("https://companiesmarketcap.com/bkw-ag/annual-reports/", "BKW AG", "https://www.bkw.ch")
    assert not own("https://investor.asml.com/annual-reports/2025/downloads", "ASMALLWORLD AG", "http://www.asmallworld.com")
    assert not own("https://www.advantech.com/en-us/investor/annual-report", "Adval Tech Holding AG", "https://www.advaltech.com")


def test_search_results_are_judged_by_title_when_the_url_misleads():
    allowed = rf.allowed_place_words("Arbonia AG", ["CH"])
    arbonia = rf.search_result_candidate({
        "url": "https://www.arbonia.com/fileadmin/05_Investoren/Gesch%C3%A4fts-_und_Halbjahresberichte/Arbonia_Annual_Report_2025.pdf",
        "title": "Annual report - Arbonia"}, allowed)
    assert arbonia.kept and arbonia.is_pdf and arbonia.year == 2025
    bucher = rf.search_result_candidate({
        "url": "https://www.bucherindustries.com/index.php?eID=dumpFile&t=f&f=4706&token=8", "title": "Financial report 2025"}, frozenset())
    assert bucher.kept and bucher.is_pdf and bucher.year == 2025
    essentra = rf.search_result_candidate({
        "url": "https://a.storyblok.com/f/2/x/e5/32845-essentra-ar2025-interactive.pdf",
        "title": "UNLOCKING OPPORTUNITIES THROUGH EVERY ..."}, frozenset())
    assert essentra.kept and essentra.year == 2025
    semi = rf.search_result_candidate({"url": "https://a.storyblok.com/f/1/x/15/advaltech_hjb26_en_final.pdf",
                                       "title": "Semi-Annual Report"}, frozenset())
    assert not semi.kept


def test_the_downloads_page_of_an_online_report_is_scraped_for_the_pdf():
    results = [{"url": "https://report.bystronic.com/", "title": "Bystronic - Annual Report 2025"},
               {"url": "https://report.bystronic.com/2025/downloads", "title": "Downloads"},
               {"url": "https://ir.bystronic.com/en/publications/financial-reports", "title": "Financial reports"}]
    cands = [rf.search_result_candidate(r, frozenset()) for r in results]
    assert rf.downloads_page(results, cands) == "https://report.bystronic.com/2025/downloads"


def test_a_report_the_site_map_never_reaches_is_found_by_a_web_search():
    pdf = f"https://report.adidas-group.com/{YEAR}/en/_assets/downloads/annual-report-adidas-ar{str(YEAR)[2:]}.pdf"
    fc = FakeFC(maps=[["https://www.adidas.com/us/adiclub"]] * 5,
                search_results=[{"url": pdf, "title": f"annual report {YEAR} - pdf"},
                                {"url": "https://www.annualreports.com/Company/adidas-ag", "title": "Adidas AG"}])
    r = rf.find_report("https://www.adidas.com", fc, country="DE", company_name="ADIDAS AG NA O.N.")
    assert r.url == pdf
    assert fc.calls[:2] == ["map:annual report", "search:adidas annual report %d pdf" % YEAR]
    assert not any(c.startswith("scrape:") for c in fc.calls)      # found: no page guessed


def test_without_a_website_the_report_is_searched_for_by_name():
    pdf = f"https://www.apgsga.ch/files/geschaeftsbericht-{YEAR}.pdf"
    fc = FakeFC(maps=[], search_results=[{"url": pdf, "title": f"Geschäftsbericht {YEAR}"},
                                         {"url": f"https://www.bcv.ch/annual-report-{YEAR}.pdf", "title": "x"}])
    r = rf.find_report(None, fc, country="CH", company_name="APG SGA SA")
    assert r.url == pdf and not any(c.startswith("map:") for c in fc.calls)
    import pytest
    with pytest.raises(rf.ReportNotFoundError):
        rf.find_report(None, FakeFC(maps=[]), country="CH", company_name="APG SGA SA")


def test_german_and_french_reports_get_the_right_excerpts():
    chunks = [Chunk(0, "Die Bilanz zeigt Vorräte und Forderungen. " * 20, [1]),
              Chunk(1, "Mitarbeitende: Per 31. Dezember beschäftigte die Gruppe 4'512 Mitarbeitende "
                       "(Vollzeitstellen 4'100). Personalaufwand stieg.", [2]),
              Chunk(2, "Le nombre de collaborateurs s'élevait à 1 234 (équivalents plein temps 1 100).", [3])]
    picked = {c.id for c in select_chunks(chunks, "employees", 200)}
    assert {1, 2} <= picked


def test_the_reports_own_domain_becomes_the_website(tmp_path, monkeypatch):
    from extractor import pipeline
    monkeypatch.setattr(pipeline, "CACHE_DIR", tmp_path)
    pdf = f"https://report.adidas-group.com/{YEAR}/en/annual-report-adidas.pdf"
    monkeypatch.setattr(pipeline, "find_report", lambda *a, **k: rf.ReportResult(pdf, YEAR, True, [], []))
    found = pipeline.discover("ADIDAS AG", "adidas", None, "https://www.adidas.com", None, False)
    assert found["website"] == "https://www.adidas-group.com" and found["report_url"] == pdf
    cdn = "https://a.storyblok.com/f/1/x/e5/essentra-ar2025.pdf"
    monkeypatch.setattr(pipeline, "find_report", lambda *a, **k: rf.ReportResult(cdn, YEAR, True, [], []))
    found = pipeline.discover("Essentra plc", "essentra", None, "https://www.essentraplc.com", None, False)
    assert found["website"] == "https://www.essentraplc.com"           # never a file server


def test_german_listing_lines_are_not_part_of_the_name():
    from extractor.config import without_share_class as w
    assert w("STABILUS SE INH. EO-,01") == "STABILUS SE"
    assert w("DRAEGERWERK ST.A.O.N.") == "DRAEGERWERK"
    assert w("BAYWA AG VINK.NA. O.N.") == "BAYWA AG"
    assert w("MUENCH.RUECKVERSICHERUNGS GESELLSCHAFT.VNA O.N.") == "MUENCH.RUECKVERSICHERUNGS GESELLSCHAFT"
    assert w("PROCREDIT HOLDING AG NA EO 5") == "PROCREDIT HOLDING AG"
    assert w("DT.TELEKOM AG NA") == "DT.TELEKOM AG"
    assert w("FAIR VALUE REIT-AG INH.ON") == "FAIR VALUE REIT-AG"
    for keep in ("Stamm AG", "Nestle SA", "Banque Cantonale du Jura SA", "SF Urban Properties AG"):
        assert w(keep) == keep


def test_the_tracker_saved_as_utf8_csv_is_read_as_it_is(tmp_path, monkeypatch):
    from pathlib import Path
    from extractor import datapoints as dp
    monkeypatch.setattr(dp, "known_ids", lambda: {"DE000BAY0017": "bayer-ag-old-id"})
    p = tmp_path / "set2.csv"
    p.write_text("﻿Company Name,Country,Region,Tier,ISIN,LEI,Pipeline Run,Run required,Find Required,"
                 "Company Data,Company URL,Remuneration Files,Link,Date,Annual Reports,Annual Link,Date2,"
                 "Additional Files_1,Link3,Date4\n"
                 "SOFTING AG O.N.,DE,DACH,Tier 2,DE0005178008,,required,Company Data,OpenAPI,YES,"
                 "https://investor.softing.com,YES,https://investor.softing.com/rem-2025.pdf,,NO,,,,,\n"
                 "BAYER AG NA O.N.,DE,DACH,Tier 2,DE000BAY0017,,required,Pay Data,NA,NO,,NO,,,YES,"
                 "https://www.bayer.com/ar-2025.pdf,,Remuneration report,https://www.bayer.com/rem-2025.pdf,\n",
                 encoding="utf-8")
    softing, bayer = dp.read_targets(Path(p))
    assert softing.company.company_id.startswith("softing-ag-") and softing.isin == "DE0005178008"
    assert softing.company.website == "https://investor.softing.com" and softing.run_required == "Company Data"
    assert softing.remuneration_report_url.endswith("rem-2025.pdf") and softing.company.segment == "Tier 2"
    assert bayer.company.company_id == "bayer-ag-old-id"                 # reused: no duplicate
    assert bayer.annual_report_url.endswith("ar-2025.pdf")
    assert bayer.remuneration_report_url.endswith("bayer.com/rem-2025.pdf")   # from Link3
