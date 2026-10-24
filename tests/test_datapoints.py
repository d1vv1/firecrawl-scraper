"""Data-point rows: where values come from, which value wins, and the CSV format."""

from pathlib import Path

from extractor import datapoints as dp
from extractor.apis import Found
from extractor.batch import Company
from extractor.schemas import DataPointFacts
from extractor.scraper import Page
from extractor.sections import Chunk

ROOT = Path(__file__).resolve().parent.parent


def _origin(kind="pdf"):
    pages = [Page(1, "Contents"), Page(7, "Net sales|3|2,326.2|1,827.3"),
             Page(8, "The CEO's pension is defined contribution, 25 percent of base salary.")]
    chunks = {0: Chunk(0, "Net sales|3|2,326.2|1,827.3\nThe CEO's pension is defined contribution, "
                          "25 percent of base salary.", [7, 8])}
    return dp.Origin(kind, "https://x.com/ar.pdf", "Annual report (PDF)", "PARSE",
                     "2026-10-19T00:00:00+00:00", pages, chunks)


def test_columns_match_the_requested_format():
    assert dp.COLUMNS == ["company_id", "company_name", "segment", "country", "lei", "grain",
                          "role_row", "data_point", "value", "unit", "period_end", "source",
                          "endpoint", "method", "retrieved_at", "confidence", "note"]


def test_pdf_value_gets_the_page_of_its_quote():
    endpoint, conf, note = _origin().where("pension is defined contribution, 25 percent", 0)
    assert endpoint == "https://x.com/ar.pdf#page=8"
    assert conf == "B"
    assert note.startswith("PDF page 8:")


def test_quote_with_wrong_chunk_id_is_still_found():
    loc = dp.locate("Net sales|3|2,326.2", 99, _origin().chunks, _origin().pages)
    assert loc == dp.Located(7, True)


def test_quote_not_in_the_source_is_confidence_c():
    endpoint, conf, note = _origin().where("Revenue rose to 9,999", 0)
    assert conf == "C" and "not found verbatim" in note


def test_html_report_links_to_the_quote_text():
    endpoint, conf, _ = _origin("xhtml").where("pension is defined contribution, 25 percent", 0)
    assert endpoint.startswith("https://x.com/ar.pdf#:~:text=pension%20is%20defined")
    # table rows never match a rendered page: no fragment
    assert dp.text_fragment("https://x.com/a", "Net sales|3|2,326.2") == "https://x.com/a"


def test_exact_source_beats_ai_and_differences_are_noted():
    vals = [Found("headcount", 470, source="Annual report (PDF)", method="PARSE", confidence="B"),
            Found("headcount", 512, source="Brønnøysund", method="API", confidence="A"),
            Found("isin", "SE0015657788", method="SCRAPE", confidence="C")]
    chosen = dp.best(vals)
    assert chosen["headcount"].value == 512
    assert "other source says 470" in chosen["headcount"].note
    assert chosen["isin"].method == "SCRAPE"


def test_every_data_point_gets_a_row_with_a_reason():
    c = Company("x-1", "X AB", "SE", "nordic_uk_unlisted")
    chosen = {"listing_status": Found("listing_status", "unlisted", method="PARSE", confidence="B")}
    rows = dp.finish(dp.Target(c), chosen, ["Annual report (PDF)"], None)
    assert [r.data_point for r in rows] == dp.NAMES
    by = {r.data_point: r for r in rows}
    assert by["market_cap_band"].note.startswith("not applicable")       # unlisted
    assert by["ticker"].note.startswith("not applicable")
    assert by["cik"].note.startswith("not applicable")
    assert by["revenue"].note == "not found in: Annual report (PDF)"
    assert by["lei"].note.startswith("not found: only an official API")    # no API ran
    assert by["sector_code"].note.startswith("not found: only an official API")


def test_an_isin_makes_the_company_listed():
    c = Company("x-1", "X AB", "SE")
    chosen = {"isin": Found("isin", "SE0015657788", method="PARSE", confidence="B", note="p. 34")}
    rows = {r.data_point: r for r in dp.finish(dp.Target(c), chosen, [], None)}
    assert rows["isin"].confidence == "B"
    assert rows["listing_status"].value == "listed"       # has an ISIN of its own shares


def _facts(**over) -> DataPointFacts:
    none_t = {"value": None, "quote": None, "chunk_id": None}
    none_n = {"value": None, "unit": None, "currency": None, "period_end": None, "quote": None,
              "chunk_id": None}
    none_h = {"name": None, "holder_type": None, "stake_pct": None, "quote": None, "chunk_id": None}
    none_b = {"items": [], "unit": None, "currency": None, "basis": None, "quote": None,
              "chunk_id": None}
    d = {k: none_n for k in ("revenue", "total_assets", "fte", "headcount", "shares_outstanding")}
    d |= {k: none_t for k in ("legal_name", "business_id", "country_code", "other_names",
                              "ultimate_parent", "head_office_city", "website", "ticker", "isin",
                              "exchange", "exchange_segment", "listing_date", "is_listed",
                              "sub_sector", "fiscal_year_end", "reporting_currency",
                              "accounting_basis", "pension_type", "benefits",
                              "shareholding_requirement")}
    d |= {"controlling_owner": none_h, "major_shareholders": [], "revenue_by_country": none_b,
          "staff_by_country": none_b, "revenue_by_segment": none_b, "staff_by_segment": none_b,
          "ebitda": {"value": None, "unit": None, "currency": None, "measure": None,
                     "company_defined": None, "label_in_report": None, "quote": None,
                     "chunk_id": None},
          "share_price": {"value": None, "currency": None, "date": None, "quote": None,
                          "chunk_id": None}}
    return DataPointFacts.model_validate(d | over)


def test_owner_facts_map_to_golden_categories():
    owner = {"name": "EQT X", "holder_type": "private_equity", "stake_pct": 62.0,
             "quote": "Net sales|3|2,326.2", "chunk_id": 0}
    found = {f.data_point: f for f in dp.from_facts(_facts(controlling_owner=owner), _origin())}
    assert found["controlling_owner"].value == "private_equity"
    assert found["ownership_type"].value == "pe_backed"
    assert found["pe_stake_5pct"].value == "yes"
    assert found["controlling_owner_name"].value == "EQT X"


def test_facts_without_a_quote_are_dropped():
    fact = {"value": "Stockholm", "quote": None, "chunk_id": None}
    assert dp.from_facts(_facts(head_office_city=fact), _origin()) == []


def test_money_from_the_report_is_in_full_units():
    rev = {"value": 2326.2, "unit": "millions", "currency": "SEK", "period_end": "2024-12-31",
           "quote": "Net sales|3|2,326.2", "chunk_id": 0}
    f = dp.from_facts(_facts(revenue=rev), _origin())[0]
    assert (f.value, f.unit, f.endpoint) == (2326200000.0, "SEK", "https://x.com/ar.pdf#page=7")
    assert dp.fmt_number(f.value) == "2326200000"


def test_identity_facts_come_from_documents():
    q = {"quote": "The CEO's pension is defined contribution", "chunk_id": 0}
    found = {f.data_point: f for f in dp.from_facts(_facts(
        business_id={"value": "556720-8851", **q}, country_code={"value": "se", **q},
        ultimate_parent={"value": "Parent Oy", **q}), _origin())}
    assert found["business_id"].value == "556720-8851"
    assert found["country_code"].value == "SE"
    assert found["ultimate_parent"].value == "Parent Oy"


def _doc(url, kind, text, label="remuneration", year=2025):
    from extractor.documents import DOC_TYPES, Document
    return Document(url, DOC_TYPES[label], kind, [Page(1, "Intro"), Page(4, text)], year,
                    "2026-10-20T00:00:00+00:00")


def test_bundle_places_each_value_in_its_own_document():
    rem = dp.doc_origin(_doc("https://x.com/rem-2025.pdf", "pdf",
                             "The CEO's pension is defined contribution, 30 percent of salary."), 0)
    share = dp.doc_origin(_doc("https://x.com/the-share", "web",
                               "The ISIN code of the share is SE0015657788.", "share", None),
                          len(rem.chunks))
    pension = {"value": "defined contribution, 30%",
               "quote": "pension is defined contribution, 30 percent", "chunk_id": 0}
    isin = {"value": "SE0015657788", "quote": "ISIN code of the share is SE0015657788",
            "chunk_id": 0}                                      # wrong chunk id
    found = {f.data_point: f for f in dp.from_facts(_facts(pension_type=pension, isin=isin),
                                                     dp.Bundle([rem, share]))}
    p, i = found["pension_type"], found["isin"]
    assert (p.endpoint, p.source, p.method, p.confidence) == (
        "https://x.com/rem-2025.pdf#page=4", "Remuneration report (PDF)", "PARSE", "B")
    assert "document dated 2025" in p.note
    assert i.endpoint.startswith("https://x.com/the-share#:~:text=")
    assert (i.source, i.method, i.confidence) == ("Share information (web page)", "SCRAPE", "B")


def test_gap_list_skips_listed_only_points_for_unlisted_companies():
    chosen = {"listing_status": Found("listing_status", "unlisted", method="PARSE", confidence="B")}
    gaps = dp.gap_list(chosen)
    assert "pension_type" not in gaps and "isin" not in gaps
    assert "fte" in gaps and "business_id" in gaps
    assert "lei" not in gaps and "market_cap_band" not in gaps
    assert dp.wanted_fields(["controlling_owner_name", "ownership_type", "listing_status"]) == [
        "controlling_owner", "is_listed"]


def test_golden_sample_reads_one_target_per_company():
    targets = dp.read_targets(ROOT / "data" / "golden_test_sample_5_per_segment_country_all.csv")
    ids = [t.company.company_id for t in targets]
    assert len(ids) == len(set(ids)) == 196
    none_country = [t for t in targets if t.company.segment == "other_unlisted_or_unknown"
                    and t.company.country is None]
    assert none_country                                   # "(none)" means unknown


def test_build_value_uses_the_golden_unit():
    golden = {"unit": "millions", "currency": "SEK"}
    assert dp.build_value(golden, {"value": "2326200000", "unit": "SEK"}) == "2326.2"
    assert dp.build_value({"unit": ""}, {"value": "listed", "unit": ""}) == "listed"


def test_protocol_company_fields_from_the_report():
    q = {"quote": "Net sales|3|2,326.2", "chunk_id": 0}
    found = {f.data_point: f for f in dp.from_facts(_facts(
        ebitda={"value": 412.5, "unit": "millions", "currency": "SEK", "measure": "adjusted_ebitda",
                "company_defined": True, "label_in_report": "Adjusted EBITDA", **q},
        share_price={"value": 54.2, "currency": "SEK", "date": "2025-12-30", **q},
        website={"value": "https://www.Acme.se/investors", **q},
        major_shareholders=[{"name": "EQT X", "holder_type": "private_equity", "stake_pct": 30.0, **q},
                            {"name": "Fund Y", "holder_type": "institutional_investor",
                             "stake_pct": 4.0, **q}],
        revenue_by_segment={"items": [{"segment": "Cloud", "value": 100.0},
                                      {"segment": "Devices", "value": 50.0}],
                            "unit": "millions", "currency": "SEK", "basis": "external revenue", **q}),
        _origin())}
    assert found["ebitda"].value == 412_500_000 and "company-defined" in found["ebitda"].note
    assert (found["share_price"].value, found["share_price"].unit) == (54.2, "SEK")
    assert found["website"].value == "acme.se"
    assert found["largest_holders"].value == "EQT X 30%; Fund Y 4%"
    assert found["pe_stake_5pct"].value == "yes"
    assert found["revenue_by_segment"].value == "Cloud: 100; Devices: 50"


def test_market_cap_band_is_derived_in_eur_only():
    shares = Found("shares_outstanding", 100_000_000, unit="shares", source="AR", confidence="B")
    eur = Found("share_price", 12.0, unit="EUR", source="AR", confidence="B")
    band, why = dp.market_cap_band({"shares_outstanding": shares, "share_price": eur})
    assert band.value == "large" and band.method == "DERIVED" and why == ""
    band, why = dp.market_cap_band({"shares_outstanding": shares,
                                    "share_price": Found("share_price", 12.0, unit="SEK")})
    assert band is None and "exchange rate" in why
    assert dp.market_cap_band({})[1] == "not derived: no shares outstanding and share price"


def _amount(v=None, unit="thousands", cur="EUR", quote=None, includes=None):
    return {"value": v, "unit": unit if v is not None else None, "currency": cur if v is not None else None,
            "includes": includes, "quote": quote, "chunk_id": 0 if quote else None}


def _role(title, executive=True, aggregate=False, name=None, **pay):
    none_p = {"value": None, "quote": None, "chunk_id": None}
    d = {"role_title": title, "person_name": name, "executive": executive, "is_aggregate": aggregate,
         "quote": "Net sales|3|2,326.2", "chunk_id": 0,
         "aggregate_headcount": {"value": None, "excludes": None, "quote": None, "chunk_id": None},
         }
    d |= {k: _amount() for k in ("base_salary", "sti_paid", "benefits", "pension",
                                 "pension_allowance", "total")}
    d |= {k: _amount() | {"form": None} for k in ("lti_vested", "lti_granted")}
    d |= {k: none_p | {"form": None, "currency": None, "unit": None}
          for k in ("sti_target", "sti_max", "lti_target", "lti_max")}
    return d | pay


def _pay(roles):
    from extractor.schemas import RemunerationFacts
    none_t = {"value": None, "quote": None, "chunk_id": None}
    return RemunerationFacts.model_validate({"fiscal_year": "2025", "roles": roles,
                                             "pension_type": none_t, "benefits": none_t,
                                             "shareholding_requirement": none_t})


def test_role_rows_for_executives_and_one_row_for_the_board():
    from extractor import pay
    q = "Net sales|3|2,326.2"
    facts = _pay([
        _role("CEO", base_salary=_amount(1000, quote=q), sti_paid=_amount(400, quote=q),
              lti_vested=_amount(300, quote=q) | {"form": "shares"},
              lti_granted=_amount(450, quote=q) | {"form": "shares"},
              benefits=_amount(50, quote=q), pension=_amount(200, quote=q, includes="social security"),
              total=_amount(2000, quote=q),
              sti_target={"value": 50.0, "form": "pct_of_max", "currency": None, "unit": None,
                          "quote": q, "chunk_id": 0},
              sti_max={"value": 120.0, "form": "pct_of_base", "currency": None, "unit": None,
                       "quote": q, "chunk_id": 0}),
        _role("Board of directors (non-executive)", executive=False, aggregate=True)])
    rows = pay.role_found(facts, _origin(), period_end="2025-12-31")
    ceo = {f.data_point: f for f in rows if f.role_row == "CEO"}
    assert [f.data_point for f in rows if f.role_row == "CEO"] == pay.ROLE_POINTS
    assert ceo["base_salary"].value == 1_000_000 and ceo["base_salary"].unit == "EUR"
    assert ceo["base_salary"].endpoint == "https://x.com/ar.pdf#page=7"
    assert ceo["pay_currency"].value == "EUR" and "thousands" in ceo["pay_currency"].note
    assert ceo["lti_vested"].value == 300_000 and "form: shares" in ceo["lti_vested"].note
    assert ceo["lti_granted"].value == 450_000
    assert (ceo["sti_target"].value, ceo["sti_target"].unit, ceo["sti_target"].method) == (
        60.0, "% of base salary", "DERIVED")                  # 50% of a 120% maximum
    assert ceo["sti_max"].unit == "% of base salary"
    assert "includes social security" in ceo["pension_contribution"].note
    assert ceo["aggregate_headcount"].note == "not applicable: one person"
    assert ceo["lti_target"].value is None
    assert all(f.grain == "role" for f in rows)
    # 1000 + 400 + 300 + 50 + 200 = 1950 vs 2000 stated: -2.5%, over the 2% tolerance
    assert "-2.5% against the stated total" in ceo["total_remuneration"].note
    board = [f for f in rows if f.role_row.startswith("Board")]
    assert [(f.data_point, f.value) for f in board] == [("role_disclosure", "aggregate")]


def test_duplicate_titles_get_the_name_and_policy_fills_targets():
    from extractor import pay
    q = "Net sales|3|2,326.2"
    roles = _pay([_role("Member of the Management Board", name="A. Meier"),
                  _role("Member of the Management Board", name="B. Weber")])
    assert pay.role_names(roles.roles) == ["Member of the Management Board (A. Meier)",
                                           "Member of the Management Board (B. Weber)"]
    policy = _pay([_role("Management Board", sti_max={"value": 150.0, "form": "pct_of_base",
                                                      "currency": None, "unit": None,
                                                      "quote": q, "chunk_id": 0})])
    rows = pay.role_found(roles, _origin(), policy, _origin())
    got = [f for f in rows if f.data_point == "sti_max" and f.value == 150.0]
    assert len(got) == 2 and "from the remuneration policy" in got[0].note


def test_board_members_become_one_row_and_pages_without_figures_are_rejected():
    from extractor import pay
    facts = _pay([_role("Supervisory Board", executive=False, name="A"),
                  _role("Supervisory Board", executive=False, name="B"),
                  _role("CEO")])
    roles = pay.merge_board(facts.roles)
    assert [r.role_title for r in roles] == ["Board (non-executive)", "CEO"]
    assert roles[0].is_aggregate is False                     # disclosed one by one
    assert not pay.has_pay(facts)                             # the CEO has no figures
    q = "Net sales|3|2,326.2"
    assert pay.has_pay(_pay([_role("CEO", total=_amount(900, quote=q))]))


def test_a_report_pdf_beats_a_page_about_it():
    from extractor.documents import DOC_TYPES, Candidate, _rank
    rem = DOC_TYPES["remuneration"]
    page = Candidate("https://acme.com/governance/remuneration", rem, 2, None, False, 0)
    pdf = Candidate("https://acme.com/files/annual-report-2025-remuneration-report.pdf", rem, 2,
                    2025, True, 0)
    assert _rank(pdf, 2025) > _rank(page, 2025)


def test_old_or_undated_figures_from_fallback_documents_are_graded_c():
    f = Found("ebitda", 16e6, confidence="B", note='web page: "EBIT of CHF 16.0 million"')
    dp.year_check(f, 2025)
    assert f.confidence == "C" and "undated" in f.note
    g = Found("ebitda", 6.8e6, confidence="B", note="PDF page 3; document dated 2025")
    dp.year_check(g, 2025)
    assert g.confidence == "B"
    assert dp.same_company("Kendrion N.V.", "Kendrion NV") and not dp.same_company("Metall Zug AG", "Komax Holding AG")


def test_run_budget_reserves_the_worst_case_of_running_companies(tmp_path, monkeypatch):
    monkeypatch.setattr(Company, "result_path", property(lambda self: tmp_path / f"{self.company_id}.json"))
    monkeypatch.setattr(Company, "error_path", property(lambda self: tmp_path / f"{self.company_id}.err"))
    opts = {"docs": True, "doc_credits": 10, "pipeline_credits": 6, "retry_failed": False}
    new, cached = dp.Target(Company("n", "New AB", "SE")), dp.Target(Company("c", "Cached AB", "SE"))
    (tmp_path / "c.json").write_text("{}")
    assert dp.worst_case(new, opts) == 16 and dp.worst_case(cached, opts) == 10
    b = dp.Budget(30, spent=5)
    assert b.allows(new, opts, [])                       # 5 + 16 <= 30
    assert not b.allows(new, opts, [cached])             # 5 + 10 + 16 > 30
    assert b.allows(cached, opts, [cached])              # 5 + 10 + 10 <= 30
    assert dp.Budget(None).allows(new, opts, [new] * 9)


def test_a_report_from_another_country_is_graded_c():
    vals = [Found("country_code", "NL", source="Annual report (PDF)", confidence="B"),
            Found("revenue", 1.2e9, source="Annual report (PDF)", method="PARSE", confidence="B"),
            Found("revenue", 7.9e10, source="ESEF filing", method="XBRL", confidence="A")]
    dp.identity_check(vals, "DE", ["Siemens AG"], "Annual report (PDF)")
    assert [v.confidence for v in vals] == ["C", "C", "A"]
    assert "possibly another company's report" in vals[1].note
    ok = [Found("country_code", "DE", source="Annual report (PDF)", confidence="B")]
    dp.identity_check(ok, "DE", ["Siemens AG"], "Annual report (PDF)")
    assert ok[0].confidence == "B"


def test_a_report_by_another_legal_entity_is_graded_c():
    sub = [Found("legal_name", "Siemens Financieringsmaatschappij N.V.", source="AR", confidence="B")]
    dp.identity_check(sub, None, ["Siemens AG", "Siemens Aktiengesellschaft"], "AR")
    assert sub[0].confidence == "C" and "Financieringsmaatschappij" in sub[0].note
    for report, ours in [("Yubico AB (publ)", "Yubico AB"), ("Leonardo S.p.a.", "Leonardo SpA"),
                         ("CTT – Correios de Portugal, S.A.", "CTT - Correios de Portugal SA"),
                         ("Siemens Aktiengesellschaft", "Siemens AG"),
                         ("H & M Hennes & Mauritz AB", "Hennes & Mauritz AB"),
                         ("Komax Holding AG", "Komax Holding AG")]:
        f = [Found("legal_name", report, source="AR", confidence="B")]
        dp.identity_check(f, None, [ours], "AR")
        assert f[0].confidence == "B", report
    trade = [Found("legal_name", "Nokian Renkaat Oyj", source="AR", confidence="B")]
    dp.identity_check(trade, None, ["Nokian Tyres plc", "Nokian Renkaat Oyj"], "AR")   # LEI name
    assert trade[0].confidence == "B"


def test_ifrs_revenue_with_the_broader_line_noted():
    result = {"revenue": {"value": 1128843214, "value_full": 1128843214, "unit": "units",
                          "currency": "EUR", "method": "xbrl_tag",
                          "xbrl_concept": "ifrs-full:RevenueFromContractsWithCustomers"},
              "filing": {"type": "esef", "report_url": "https://f/x.xhtml",
                         "revenue_and_operating_income": 1292435282.0},
              "period_end_date": "2025-12-31", "fiscal_year": "2025"}
    rev = next(f for f in dp.from_result(result, None) if f.data_point == "revenue")
    assert rev.value == 1128843214 and "revenue and operating income 1292435282" in rev.note


def test_api_values_come_first_and_documents_fill_the_rest(monkeypatch):
    from extractor import apis
    gleif = [Found("lei", "529900UID9PCQXLG9479", source="GLEIF", method="API", confidence="A"),
             Found("head_office_city", "Dierikon", source="GLEIF", method="API", confidence="A"),
             Found("_gleif_isins", "CH0010702154", source="GLEIF ISIN map", method="API")]
    monkeypatch.setattr(apis, "gleif_values", lambda lei: gleif)
    monkeypatch.setattr(apis, "registry_values", lambda country, number, name=None: [])
    t = dp.Target(Company("komax", "Komax Holding AG", "CH"))
    values, answered, isins = dp.from_apis(t, None, {"lei": "529900UID9PCQXLG9479", "country": "CH"})
    assert answered == ["GLEIF"] and isins == ["CH0010702154"]
    doc = Found("head_office_city", "Luzern", source="Annual report (PDF)", method="PARSE", confidence="B")
    isin = Found("isin", "CH0010702154", source="Annual report (PDF)", method="PARSE", confidence="B")
    chosen = dp.best(values + [doc, isin])
    assert chosen["head_office_city"].value == "Dierikon"
    assert "other source says Luzern" in chosen["head_office_city"].note
    rows = {r.data_point: r for r in dp.finish(t, chosen, answered, None, isins)}
    assert rows["lei"].value == "529900UID9PCQXLG9479"
    assert rows["isin"].confidence == "A" and "GLEIF ISIN map" in rows["isin"].note


def test_aggregate_rows_from_the_annual_report_complete_a_ceo_only_report(monkeypatch):
    from extractor import pay
    q = "Net sales|3|2,326.2"
    report_pay = _pay([_role("CEO", base_salary=_amount(1000, quote=q))])
    ar_pay = _pay([_role("VD och koncernchef", base_salary=_amount(1000, quote=q)),
                   _role("Other members of group management", aggregate=True,
                         base_salary=_amount(9000, quote=q))])
    monkeypatch.setattr(pay, "ask_pay", lambda *a, **k: ar_pay)
    ar = _origin()
    rem = dp.Origin("pdf", "https://x.com/rem.pdf", "Remuneration report (PDF)", "PARSE", "", ar.pages,
                    ar.chunks)
    read = []
    rows = dp._aggregates_from_report("X", report_pay, rem, ar, "k", "2025-12-31", read)
    assert {r.role_row for r in rows} == {"Other members of group management"}   # not the CEO again
    assert read == ["Annual report (PDF)"]


def test_targets_keep_their_stated_form():
    from extractor import pay
    q = "Net sales|3|2,326.2"
    facts = _pay([_role("CEO", base_salary=_amount(1000, quote=q),
                        sti_max={"value": 6.0, "form": "months_of_salary", "currency": None,
                                 "unit": None, "quote": q, "chunk_id": 0},
                        lti_max={"value": 2.0, "form": "amount", "currency": "EUR",
                                 "unit": "millions", "quote": q, "chunk_id": 0})])
    rows = {f.data_point: f for f in pay.role_found(facts, _origin()) if f.role_row == "CEO"}
    assert (rows["sti_max"].value, rows["sti_max"].unit, rows["sti_max"].method) == (
        50.0, "% of base salary", "DERIVED")                     # 6 months = half a year
    assert "stated as 6 months of salary" in rows["sti_max"].note
    assert (rows["lti_max"].value, rows["lti_max"].unit) == (2_000_000, "EUR")


def test_pay_from_an_older_year_is_skipped_and_uk_reads_the_annual_report_first(monkeypatch):
    from extractor import pay
    q = "Net sales|3|2,326.2"
    old = _pay([_role("CEO", total=_amount(8.6, unit="millions", quote=q))])
    old = old.model_copy(update={"fiscal_year": "2024"})
    new = _pay([_role("CEO", base_salary=_amount(1600, quote=q))])
    asked = []

    def fake_ask(name, url, chunks, what, key):
        asked.append(url)
        return old if "roadshow" in url else new
    monkeypatch.setattr(pay, "ask_pay", fake_ask)
    ar = _origin()

    class Lib:
        def __init__(self):
            self.n = 0

        def find(self, key, search=False):
            from extractor.documents import DOC_TYPES, Document
            self.n += 1
            if key == "remuneration" and self.n == 1:
                return Document("https://shell.com/remuneration-roadshow-q1-2025.pdf",
                                DOC_TYPES["remuneration"], "pdf", ar.pages, 2025, "")
            return None
    roles, _, read = dp.from_pay("Shell", "shell", Lib(), ar, "k", "2025-12-31", "SE", 2025)
    assert asked[0].endswith("roadshow-q1-2025.pdf") and asked[-1] == ar.url   # skipped, then AR
    assert any(r.data_point == "base_salary" and r.value == 1_000_000 * 1.6 for r in roles)
    asked.clear()
    dp.from_pay("Shell", "shell", Lib(), ar, "k", "2025-12-31", "GB", 2025)
    assert asked[0] == ar.url                                    # UK: the annual report first


def test_fiscal_years_are_read_by_their_end():
    assert dp.fiscal_end_year("2025") == 2025
    assert dp.fiscal_end_year("2025/26") == 2026
    assert dp.fiscal_end_year("FY 2025-2026") == 2026
    assert dp.fiscal_end_year(None) is None


def test_supplied_report_urls_are_read_from_the_input(tmp_path):
    p = tmp_path / "in.csv"
    p.write_text("company_id,company_name,country,annual_report_url,remuneration_report_url\n"
                 "eq,Equinor ASA,NO,https://cdn.example.com/files/9b3e.pdf?2025-annual-report.pdf,\n",
                 encoding="utf-8")
    t = dp.read_targets(p)[0]
    assert t.annual_report_url.startswith("https://cdn.example.com/") and t.remuneration_report_url is None


def test_a_supplied_document_is_read_first_and_skips_the_year_check(monkeypatch):
    from extractor import pay
    q = "Net sales|3|2,326.2"
    old_year = _pay([_role("CEO", base_salary=_amount(1142, quote=q))]).model_copy(
        update={"fiscal_year": "2024"})
    asked = []
    monkeypatch.setattr(pay, "ask_pay", lambda name, url, *a: asked.append(url) or old_year)
    ar = _origin()
    from extractor.documents import DOC_TYPES, Document
    monkeypatch.setattr(dp, "supplied_doc", lambda slug, url, label, lib: Document(
        url, DOC_TYPES["remuneration"], "pdf", ar.pages, 2025, ""))
    roles, _, _ = dp.from_pay("Equinor", "eq", None, ar, "k", "", "NO", 2025,
                              (("https://cdn.example.com/x.pdf", "Annual report"),))
    assert asked[0] == "https://cdn.example.com/x.pdf"          # first, and accepted as given
    assert any(r.data_point == "base_salary" and r.value == 1_142_000 for r in roles)


def test_a_salary_addition_in_lieu_of_pension_counts_as_pension():
    from extractor import pay
    q = "Net sales|3|2,326.2"
    facts = _pay([_role("EVP Exploration", pension=_amount(30, quote=q),
                        pension_allowance=_amount(93, quote=q))])
    rows = {f.data_point: f for f in pay.role_found(facts, _origin())}
    p = rows["pension_contribution"]
    assert (p.value, p.method) == (123_000, "DERIVED") and "salary addition in lieu" in p.note

