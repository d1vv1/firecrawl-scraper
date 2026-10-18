"""Live end-to-end run. Uses Firecrawl credits and the LLM. Run with: pytest -m live"""

import pytest

from extractor.pipeline import run


@pytest.mark.live
def test_unilever_end_to_end():
    r = run("Unilever PLC")
    assert r["status"] == "ok", r["checks"]
    assert r["revenue"]["currency"] == "EUR"
    assert r["revenue"]["scope"] == "consolidated"
    assert r["total_assets"]["value_full"] > 1e10
    assert r["revenue_model"]["categories"]
    assert r["business_structure"]["segments"]

    # Second run must come entirely from cache: no Firecrawl calls, no downloads.
    again = run("Unilever PLC")
    assert again["firecrawl_credits_used"] == 0
    assert again["debug"]["cache_used"] == {"discovery": True, "report": True}
