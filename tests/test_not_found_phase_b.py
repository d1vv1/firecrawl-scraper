"""Phase B of docs/not_found_reduction_plan.md: extraction rules and the decided values
(D1, D4) they rest on."""

from extractor import datapoints as dp
from tests.test_before_dach import _row

MISSING = "not found in: GLEIF, Annual report (PDF), Remuneration report (PDF)"


def _by(rows):
    return {r["data_point"]: r for r in rows}


def _role(name, value, note="", role="CEO"):
    r = _row("a", name, value, "role", role,
             note or ("" if value else "not found in: Remuneration report (PDF)"))
    if value:
        r.update(unit="EUR", source="Remuneration report (PDF)", endpoint="https://x/rr.pdf#page=12",
                 period_end="2025-12-31")
    return r


# --- D4: a part folded into another amount ---------------------------------------------------

def test_a_pension_folded_into_benefits_is_included_not_missing():
    rows = [_role("base_salary", "500000"), _role("benefits_value", "80000", note="includes pension"),
            _role("pension_contribution", ""), _role("total_remuneration", "900000")]
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["note"] == "not applicable: included in benefits_value (pension)"


def test_the_total_including_everything_folds_nothing(monkeypatch):
    rows = [_role("base_salary", "500000"), _role("pension_contribution", ""),
            _role("total_remuneration", "900000", note="includes pension and benefits")]
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["note"].startswith("not found")
    monkeypatch.setenv("RULES_OFF", "included_in_other")
    rows = [_role("benefits_value", "1", note="includes pension"), _role("pension_contribution", "")]
    dp.refresh(rows)
    assert rows[1]["note"].startswith("not found")


# --- B2: no shareholding rule in a remuneration report read --------------------------------------

def _company(note=MISSING):
    return [_row("a", "shareholding_requirement", "", note=note), _role("base_salary", "500000")]


def test_no_shareholding_rule_in_the_remuneration_report_read_is_none():
    rows = _company()
    dp.refresh(rows)
    sr = rows[0]
    assert sr["value"] == "None" and sr["confidence"] == "C" and sr["method"] == "DERIVED"
    assert sr["endpoint"] == "https://x/rr.pdf" and sr["source"] == "Remuneration report (PDF)"
    assert sr["note"].startswith("derived: no shareholding requirement in the remuneration report read")


def test_no_none_without_a_remuneration_report_read(monkeypatch):
    # searched in the annual report only
    rows = _company("not found in: GLEIF, Annual report (PDF)")
    dp.refresh(rows)
    assert rows[0]["value"] == ""
    # the pay came from the annual report, not a remuneration report
    rows = _company()
    rows[1]["source"] = "Annual report (PDF)"
    dp.refresh(rows)
    assert rows[0]["value"] == ""
    monkeypatch.setenv("RULES_OFF", "none_if_absent")
    rows = _company()
    dp.refresh(rows)
    assert rows[0]["value"] == ""


# --- B3, B4: EBITDA, shares and the parent from ESEF tags -----------------------------------------

from extractor import esef  # noqa: E402

FY = "2025-12-31"


def _facts(*items):
    """ESEF facts: (concept, value, unit, period)."""
    return {str(i): {"value": v, "dimensions": {"concept": c, "unit": u, "period": p, "entity": "x"}}
            for i, (c, v, u, p) in enumerate(items)}


YEAR = "2025-01-01T00:00:00/2026-01-01T00:00:00"


def test_extension_ebitda_operating_profit_and_shares_are_read_for_the_year():
    got = esef.extra_figures(_facts(
        ("acme:Ebitda", "48829000", "iso4217:EUR", YEAR),
        ("acme:DepreciationRecognisedInProfitOrLossEbitda", "-19127000", "iso4217:EUR", YEAR),
        ("ifrs-full:ProfitLossFromOperatingActivities", "29702000", "iso4217:EUR", YEAR),
        ("ifrs-full:ProfitLossFromOperatingActivities", "1", "iso4217:EUR",
         "2024-01-01T00:00:00/2025-01-01T00:00:00"),
        ("ifrs-full:NumberOfSharesIssued", "16862067", "xbrli:shares", "2026-01-01T00:00:00"),
        ("ifrs-full:NameOfUltimateParentOfEntity", "<p>Acme Holding SA</p>", None, YEAR)), FY)
    assert got["ebitda"].value == 48829000 and got["ebitda"].concept == "acme:Ebitda"
    assert got["operating_profit"].value == 29702000
    assert got[esef.SHARES_ISSUED_CONCEPT].value == 16862067
    assert got["ifrs-full:NameOfUltimateParentOfEntity"][0] == "Acme Holding SA"


def _x(**kw):
    return esef.ExtraFigures(period_end=FY, report_url="https://filings.xbrl.org/r.xhtml", viewer_url=None, **kw)


def _gaps(legal="Acme Plc"):
    return [_row("a", "lei", "L" * 20), _row("a", "fiscal_year_end", FY), _row("a", "legal_name", legal),
            *(_row("a", k, "", note="not found in: ESEF filing (filings.xbrl.org)")
              for k in ("ebitda", "shares_outstanding", "ultimate_parent"))]


def test_gaps_filled_from_the_tags_with_operating_profit_named_as_such():
    rows = _gaps()
    x = _x(operating_profit=esef.TaggedFigure(29702000, "EUR", esef.OPERATING_PROFIT_CONCEPT, "y"),
           shares=esef.TaggedFigure(16862067, "shares", esef.SHARES_ISSUED_CONCEPT, FY),
           parent=("Acme Plc", "ifrs-full:NameOfUltimateParentOfEntity"))
    dp.refresh(rows, esef_extras=lambda lei, fye: x)
    by = _by(rows)
    assert by["ebitda"]["value"] == "29702000" and by["ebitda"]["unit"] == "EUR"
    assert by["ebitda"]["note"].startswith("operating profit (no EBITDA tagged")
    assert by["ebitda"]["method"] == "XBRL" and by["ebitda"]["confidence"] == "A"
    assert by["shares_outstanding"]["value"] == "16862067"
    assert "shares issued" in by["shares_outstanding"]["note"]
    assert by["ultimate_parent"]["value"] == "none (top of group)"


def test_a_value_already_read_is_not_replaced_and_nothing_is_asked_without_gaps():
    rows = _gaps()
    for r in rows[3:]:
        r.update(value="1", note="")
    asked = []
    dp.refresh(rows, esef_extras=lambda lei, fye: asked.append(lei))
    assert not asked and [r["value"] for r in rows[3:]] == ["1", "1", "1"]


# --- B6: an empty answer asked once more of the stronger model ---------------------------------

from extractor import llm  # noqa: E402
from extractor.schemas import DataPointFacts  # noqa: E402
from extractor.sections import Chunk  # noqa: E402


def _empty_facts(**over):
    def blank(name):
        f = DataPointFacts.model_fields[name]
        ann = f.annotation
        if getattr(ann, "__origin__", None) is list:
            return []
        return {k: ([] if k == "items" else None) for k in ann.model_fields}
    d = {k: blank(k) for k in DataPointFacts.model_fields}
    d.update(over)
    return DataPointFacts.model_validate(d)


def test_an_empty_financial_answer_is_asked_of_the_fallback_model(monkeypatch, tmp_path):
    monkeypatch.setattr(dp, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(llm, "fallback_model", lambda: "google/gemini-2.5-pro")
    monkeypatch.setattr(llm, "model_name", lambda: "google/gemini-2.5-flash")
    found = _empty_facts(revenue={"value": 120.5, "unit": "millions", "currency": "EUR",
                                  "period_end": None, "quote": "Revenue 120.5", "chunk_id": 1})
    asked = []

    def fake(system, user, schema, images=None, model=None):
        asked.append(model)
        return found if model else _empty_facts()
    monkeypatch.setattr(llm, "call_llm", fake)
    chunks = [Chunk(1, "Revenue 120.5")]
    facts = dp.ask("Acme", "https://x/ar.pdf", chunks, "the annual report", "acme_ar")
    assert asked == [None, "google/gemini-2.5-pro"] and facts.revenue.value == 120.5
    saved = (tmp_path / "acme_ar_datapoints_llm.json").read_text(encoding="utf-8")
    assert '"model": "google/gemini-2.5-pro"' in saved and '"fallback_tried": true' in saved
    # cached: not asked again
    asked.clear()
    dp.ask("Acme", "https://x/ar.pdf", chunks, "the annual report", "acme_ar")
    assert asked == []


def test_no_retry_when_the_answer_has_figures_or_none_is_configured(monkeypatch, tmp_path):
    monkeypatch.setattr(dp, "CACHE_DIR", tmp_path)
    asked = []
    monkeypatch.setattr(llm, "call_llm", lambda *a, model=None, **k: asked.append(model) or _empty_facts())
    monkeypatch.setattr(llm, "fallback_model", lambda: None)
    monkeypatch.setattr(llm, "model_name", lambda: "m")
    chunks = [Chunk(1, "text")]
    dp.ask("Acme", "u", chunks, "w", "k1")
    assert asked == [None]


# --- B7: a member paid nothing in the year (GB single-figure rows of dashes) ----------------------

def test_a_row_of_dashes_is_no_pay_for_the_year():
    assert dp.all_dashes("Jon Lewis 8,10 2025 – – – – – – – – –")
    assert dp.all_dashes("Jack Clarke\ufffd|2025|\ufffd|\ufffd|\ufffd|\ufffd")
    assert not dp.all_dashes("C Chadwick | 120,000 | 20,000 | - | - | -")
    assert not dp.all_dashes("Jeremy Suddards, former Chief Executive Officer")
    rows = [_row("a", "role_disclosure", "individual", "role", "Former CEO",
                 'executive; report text: "Jon Lewis 8,10 2025 – – – – – – – – –"'),
            *(_role(k, "", role="Former CEO") for k in ("base_salary", "total_remuneration", "pension_contribution"))]
    dp.refresh(rows)
    assert all(r["note"] == "not applicable: no pay for the year (the table row is all dashes)"
               for r in rows[1:])


def test_a_failing_fallback_model_leaves_the_first_answer(monkeypatch, tmp_path):
    monkeypatch.setattr(dp, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(llm, "model_name", lambda: "flash")
    monkeypatch.setattr(llm, "fallback_model", lambda: "pro-x")
    monkeypatch.setattr(llm, "_broken_fallbacks", set())

    def fake(system, user, schema, images=None, model=None):
        if model:   # an empty answer from the stronger model: a miss for this question only
            raise llm.LLMRefusalError("No parsed output returned (finish_reason=stop).")
        return _empty_facts()
    monkeypatch.setattr(llm, "call_llm", fake)
    facts = dp.ask("Acme", "u", [Chunk(1, "t")], "w", "k2")
    assert facts.revenue.value is None and "pro-x" not in llm._broken_fallbacks

    def rejected(system, user, schema, images=None, model=None):
        if model:   # a model or schema the project rejects: not asked again in this run
            raise llm.StructuredOutputsUnsupportedError("rejected")
        return _empty_facts()
    monkeypatch.setattr(llm, "call_llm", rejected)
    facts = dp.ask("Acme", "u", [Chunk(1, "t")], "w", "k3")
    assert facts.revenue.value is None and "pro-x" in llm._broken_fallbacks
