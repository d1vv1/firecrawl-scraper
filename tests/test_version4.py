"""Scraper version 4 (14 Nov 2026): the AI reads the whole pay document, and is asked a
second, narrow question about the STI and LTI targets and maximums."""

from types import SimpleNamespace

import openai

from extractor import datapoints as dp
from extractor import pay
from extractor.schemas import Opportunities, PlanFact
from extractor.scraper import Page
from extractor.sections import Chunk

from .test_datapoints import _amount, _pay, _role, _t

Q = "Net sales|3|2,326.2"
NONE_T = {"value": None, "form": None, "currency": None, "unit": None, "quote": None, "chunk_id": None}
NO_ANSWER = {"exists": None, "quote": None, "chunk_id": None}


def _opp(*items, sti=NO_ANSWER, lti=NO_ANSWER) -> Opportunities:
    full = [{"applies_to": who, **{k: NONE_T for k in pay.TARGETS}, **targets} for who, targets in items]
    return Opportunities.model_validate({"items": full, "sti_plan": sti, "lti_plan": lti})


def test_targets_come_from_the_roles_own_entry_then_from_the_rule_for_all():
    facts = _pay([_role("CEO", sti_max=_t(100.0, "pct_of_base", Q)), _role("CFO"),
                  _role("Board (non-executive)", executive=False)])
    opp = _opp(("CEO", {"sti_max": _t(175.0, "pct_of_base", Q), "lti_max": _t(200.0, "pct_of_base", Q)}),
               ("all executives", {"sti_target": _t(50.0, "pct_of_max", Q),
                                   "lti_max": _t(150.0, "pct_of_base", Q)}))
    assert pay.apply_opportunities(facts, opp) == 4
    ceo, cfo, board = facts.roles
    assert ceo.sti_max.value == 100                       # the main answer's figure stays
    assert ceo.lti_max.value == 200 and ceo.sti_target.value == 50
    assert cfo.lti_max.value == 150 and cfo.sti_target.value == 50 and cfo.sti_max.value is None
    assert board.sti_target.value is None                 # not an executive


def test_the_rule_for_all_executives_is_not_a_former_executives():
    facts = _pay([_role("Finance"), _role("Former Board of Management member"),
                  _role("Ehemaliges Vorstandsmitglied")])
    pay.apply_opportunities(facts, _opp(("all executives", {"sti_max": _t(150.0, "pct_of_base", Q)})))
    assert [r.sti_max.value for r in facts.roles] == [150, None, None]


def test_two_roles_with_one_title_are_matched_by_the_name_the_output_gives_them():
    facts = _pay([_role("CFO", name="Ann"), _role("CFO", name="Bo")])
    assert pay.executive_titles(facts) == ["CFO (Ann)", "CFO (Bo)"]
    pay.apply_opportunities(facts, _opp(("CFO (Bo)", {"sti_max": _t(150.0, "pct_of_base", Q)})))
    assert facts.roles[0].sti_max.value is None and facts.roles[1].sti_max.value == 150


def test_the_plan_answers_of_the_two_questions():
    none = {"exists": False, "quote": "None of the Directors receive bonus schemes.", "chunk_id": 0}
    yes = {"exists": True, "quote": "The annual bonus", "chunk_id": 0}
    facts = _pay([_role("CEO", base_salary=_amount(100, quote=Q))])
    pay.apply_opportunities(facts, _opp(sti=none, lti=yes))
    assert facts.sti_plan.exists is False and facts.lti_plan.exists is True
    assert pay.plans_absent(facts) == {"sti": none["quote"]}
    # a plan the main answer saw stays; one it said is absent exists when the other saw it
    pay.apply_opportunities(facts, _opp(sti=yes, lti=none))
    assert facts.sti_plan.exists is True and facts.lti_plan.exists is True


def test_no_plan_is_not_believed_against_a_bonus_paid_or_a_target_stated():
    none = {"exists": False, "quote": "Das Vergütungssystem legt keine Zielvergütung fest.", "chunk_id": 0}
    paid = _pay([_role("Vorstand", sti_paid=_amount(40, quote=Q))])
    paid.sti_plan = paid.lti_plan = PlanFact.model_validate(none)
    assert pay.plans_absent(paid) == {"lti": none["quote"]}
    target = _pay([_role("Vorstand", lti_max=_t(100.0, "pct_of_base", Q))])
    target.sti_plan = target.lti_plan = PlanFact.model_validate(none)
    assert pay.plans_absent(target) == {"sti": none["quote"]}


def _long_origin():
    """A 'report' longer than both picks: 40 chunks of 1,000 words."""
    chunks = {i: Chunk(i, ("remuneration salary " if i == 3 else "word ") * 500, [i + 1]) for i in range(40)}
    pages = [Page(i + 1, c.text) for i, c in chunks.items()]
    return dp.Origin("pdf", "https://x.com/ar.pdf", "Annual report (PDF)", "PARSE", "", pages, chunks)


def test_the_ai_reads_the_whole_pay_document_and_the_targets_question_fills_in(monkeypatch):
    asked = {}
    facts = _pay([_role("CEO", base_salary=_amount(1000, quote=Q))])

    def ask_pay(name, url, chunks, *a, **k):
        asked["pay"] = len(chunks)
        return facts

    def ask_opp(name, url, chunks, roles, what, key):
        asked["opp"] = (len(chunks), roles)
        return _opp(("all executives", {"sti_max": _t(150.0, "pct_of_base", Q)}))
    monkeypatch.setattr(pay, "ask_pay", ask_pay)
    monkeypatch.setattr(pay, "ask_opportunities", ask_opp)
    roles, _, _ = dp.from_pay("X", "x", None, _long_origin(), "k", "2025-12-31")
    assert asked == {"pay": 40, "opp": (40, ["CEO"])}
    by = {r.data_point: r for r in roles if r.role_row == "CEO"}
    assert by["sti_max"].value == 150 and by["sti_max"].unit == "% of base salary"


def test_an_answer_that_runs_out_of_length_is_asked_again_about_the_pick(monkeypatch):
    sizes = []

    def ask_pay(name, url, chunks, *a, **k):
        sizes.append(len(chunks))
        if len(chunks) == 40:
            raise openai.LengthFinishReasonError(completion=SimpleNamespace(usage=None))
        return _pay([_role("CEO", base_salary=_amount(1000, quote=Q))])
    monkeypatch.setattr(pay, "ask_pay", ask_pay)
    monkeypatch.setattr(pay, "ask_opportunities", lambda *a, **k: _opp())
    roles, _, _ = dp.from_pay("X", "x", None, _long_origin(), "k", "2025-12-31")
    assert sizes[0] == 40 and len(sizes) == 2 and sizes[1] < 40
    assert any(r.data_point == "base_salary" and r.value for r in roles)
