"""The second look at quotes that are not in the text (extractor/requote.py). No network:
the AI call is replaced."""
import pytest

from extractor import datapoints as dp, requote
from extractor.schemas import NumberFact, TextFact
from extractor.scraper import Page
from pydantic import BaseModel

TEXT = ("## Key figures\n\n|Number of employees|64,938|62,035|\n|EBITDA|3,124|2,465|\n\n"
        "The company is domiciled in Herzogenaurach, Germany.")


class Facts(BaseModel):
    headcount: NumberFact
    head_office_city: TextFact
    people: list[TextFact]


def _number(value, quote, chunk_id=0):
    return NumberFact(value=value, unit="units", currency=None, period_end=None, quote=quote,
                      chunk_id=chunk_id)


def _facts(headcount_quote="Employees at year end: 64,938", city_quote="domiciled in Herzogenaurach"):
    return Facts(headcount=_number(64938, headcount_quote),
                 head_office_city=TextFact(value="Herzogenaurach", quote=city_quote, chunk_id=0),
                 people=[])


@pytest.fixture
def origin():
    return dp.Origin("pdf", "https://x/report.pdf", "Annual report (PDF)", "PARSE", "",
                     [Page(1, TEXT)], {0: dp.Chunk(0, TEXT, [1])})


@pytest.fixture
def answers(monkeypatch, tmp_path):
    """The AI's answers, by item id; the calls made are kept in .calls."""
    monkeypatch.setattr(requote, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(requote, "ON", True)
    given: dict[int, tuple] = {}
    calls = []

    def call_llm(system, user, schema, images=None):
        calls.append(user)
        return requote.Requotes(items=[requote.Requote(id=i, quote=q, chunk_id=c)
                                       for i, (q, c) in given.items()])
    monkeypatch.setattr(requote.llm, "call_llm", call_llm)
    given_calls = type("Answers", (), {"given": given, "calls": calls})
    return given_calls


def test_a_quote_not_in_the_text_gets_the_passage_as_printed(origin, answers):
    facts = _facts()
    answers.given[0] = ("|Number of employees|64,938|62,035|", 0)
    assert requote.repair(facts, origin, "adidas AG", "k") == 1
    assert facts.headcount.quote == "|Number of employees|64,938|62,035|"
    assert '"quote_given": "Employees at year end: 64,938"' in answers.calls[0]
    assert "domiciled in Herzogenaurach" not in answers.calls[0].split("Items:")[1]   # sound: not asked


def test_a_new_quote_is_used_only_when_it_is_in_the_text_and_prints_the_figure(origin, answers):
    facts = _facts()
    answers.given[0] = ("Total staff worldwide: 64,938 persons", 0)        # not in the text
    assert requote.repair(facts, origin, "adidas AG", "k") == 0
    answers.given[0] = ("|EBITDA|3,124|2,465|", 0)                         # in the text, another figure
    assert requote.repair(facts, origin, "adidas AG", "k2") == 0
    answers.given[0] = ("64,938", 0)                                       # the figure alone
    assert requote.repair(facts, origin, "adidas AG", "k3") == 0
    assert facts.headcount.quote == "Employees at year end: 64,938"        # as it was


def test_sound_quotes_cost_no_call(origin, answers):
    facts = _facts(headcount_quote="|Number of employees|64,938|62,035|")
    assert requote.repair(facts, origin, "adidas AG", "k") == 0
    assert answers.calls == []


def test_the_answer_is_cached_by_what_was_asked(origin, answers):
    answers.given[0] = ("|Number of employees|64,938|62,035|", 0)
    requote.repair(_facts(), origin, "adidas AG", "k")
    facts = _facts()
    assert requote.repair(facts, origin, "adidas AG", "k") == 1
    assert len(answers.calls) == 1
    requote.repair(_facts(headcount_quote="64,938 staff in total"), origin, "adidas AG", "k")
    assert len(answers.calls) == 2                                          # another quote: asked again


def test_a_failed_call_keeps_the_values(origin, answers, monkeypatch):
    import openai

    def fail(*a, **k):
        raise openai.OpenAIError("boom")
    monkeypatch.setattr(requote.llm, "call_llm", fail)
    facts = _facts()
    assert requote.repair(facts, origin, "adidas AG", "k") == 0
    assert facts.headcount.quote == "Employees at year end: 64,938"


def test_switched_off(origin, answers, monkeypatch):
    monkeypatch.setattr(requote, "ON", False)
    assert requote.repair(_facts(), origin, "adidas AG", "k") == 0 and answers.calls == []


def test_the_chunks_shown_are_the_cited_one_and_those_printing_the_figure(answers):
    chunks = {0: dp.Chunk(0, "Our people make the difference every day.", [1]),
              1: dp.Chunk(1, "Remuneration of the board in thousands", [2]),
              2: dp.Chunk(2, TEXT, [3])}
    origin = dp.Origin("pdf", "u", "Annual report (PDF)", "PARSE", "",
                       [Page(i + 1, c.text) for i, c in chunks.items()], chunks)
    facts = _facts(city_quote="domiciled in Herzogenaurach")
    facts.headcount.chunk_id = 0                                            # the wrong chunk cited
    facts.headcount.quote = "64,938 people make the difference"
    answers.given[0] = ("|Number of employees|64,938|62,035|", 2)
    assert requote.repair(facts, origin, "adidas AG", "k") == 1
    assert facts.headcount.chunk_id == 2
    assert '<chunk id="0">' in answers.calls[0] and '<chunk id="2">' in answers.calls[0]
    assert '<chunk id="1">' not in answers.calls[0]


def test_roles_are_named_in_the_label():
    from extractor.schemas import RemunerationFacts
    fields = RemunerationFacts.model_fields
    assert "roles" in fields
    labels = [label for label, _ in requote.quoted(Facts(
        headcount=_number(1, "q"), head_office_city=TextFact(value="x", quote="q", chunk_id=0),
        people=[TextFact(value="a", quote="q", chunk_id=0)]))]
    assert labels == ["headcount", "head_office_city", "people[0]"]
