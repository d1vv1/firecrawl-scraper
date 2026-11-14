"""No test asks the AI: a call that reaches llm.call_llm is refused, as when the model
refuses (the optional second looks, requote and the targets question, then keep the values
as they were; a test that needs an answer gives a fake one)."""

import pytest

from extractor import llm


@pytest.fixture(autouse=True)
def no_ai_calls(request, monkeypatch):
    if request.node.fspath.basename == "test_live.py":
        return

    def refuse(*a, **k):
        raise llm.LLMRefusalError("no AI calls in tests: give the test a fake answer")
    monkeypatch.setattr(llm, "call_llm", refuse)
