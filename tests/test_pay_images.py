"""Pay-table pages shown to the AI as images (issue 2: merged table columns)."""

import json

import pymupdf

from extractor import llm, pay
from extractor.schemas import RemunerationFacts
from extractor.sections import Chunk

TABLE = ("| Name | Base salary | Fixed salary addition | Other fees | Fringe benefits | AVP | LTI | "
         "Pension expense | Total remuneration |\n"
         + "\n".join(f"| Person {i} | 1,242 | 224 | 96 | 23 | 292 | 306 | 30 | 2,213 |" for i in range(6)))
PROSE = "The remuneration policy was approved by the general meeting in 2024. " * 20


def test_table_pages_picks_pages_with_many_numbers_and_pay_words():
    text = {1: PROSE, 2: TABLE, 3: "Revenue 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21",
            4: TABLE + "\n" + TABLE}
    chunks = [Chunk(0, "", [1, 2]), Chunk(1, "", [3, 4])]
    assert pay.table_pages(chunks, text) == [2, 4]
    assert pay.table_pages(chunks, text, n=1) == [4]           # the strongest
    assert pay.table_pages([Chunk(0, "", [1, 3])], text) == []  # no pay table


def _pdf(tmp_path, pages):
    doc = pymupdf.open()
    for t in pages:
        doc.new_page().insert_text((50, 72), t[:200])
    path = tmp_path / "rem.pdf"
    doc.save(path)
    return path


def test_ask_pay_attaches_table_pages_and_caches_by_them(tmp_path, monkeypatch):
    monkeypatch.setattr(pay, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pay, "PAGE_IMAGES", True)
    monkeypatch.setattr(llm, "load_prompt", lambda name: "system")
    pdf = _pdf(tmp_path, ["intro", "table"])
    calls = []

    def fake_call(system, user, schema, images=None):
        calls.append((user, images))
        none_t = {"value": None, "quote": None, "chunk_id": None}
        return RemunerationFacts.model_validate({"fiscal_year": "2025", "roles": [],
                                                 "pension_type": none_t, "benefits": none_t,
                                                 "shareholding_requirement": none_t})
    monkeypatch.setattr(llm, "call_llm", fake_call)
    chunks = [Chunk(0, "intro", [1]), Chunk(1, TABLE, [2])]
    pages = {1: PROSE, 2: TABLE}
    pay.ask_pay("X", "u", chunks, "the report", "x", pdf, pages)
    user, images = calls[-1]
    assert len(images) == 1 and images[0][:4] == b"\x89PNG"
    assert "PDF pages 2" in user and "read each figure from its own column" in user
    saved = json.loads((tmp_path / "x_pay_llm.json").read_text(encoding="utf-8"))
    assert saved["image_pages"] == [2]
    pay.ask_pay("X", "u", chunks, "the report", "x", pdf, pages)   # cached
    assert len(calls) == 1
    pay.ask_pay("X", "u", chunks, "the report", "x")                # no PDF: asked again
    assert len(calls) == 2 and calls[-1][1] is None


def test_user_content_carries_png_images():
    assert llm._user_content("text", None) == "text"
    content = llm._user_content("text", [b"\x89PNGdata"])
    assert content[0] == {"type": "text", "text": "text"}
    assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")


def test_page_images_are_off_by_default(tmp_path, monkeypatch):
    monkeypatch.setattr(pay, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(llm, "load_prompt", lambda name: "system")
    seen = []
    none_t = {"value": None, "quote": None, "chunk_id": None}
    monkeypatch.setattr(llm, "call_llm", lambda s, u, schema, images=None: seen.append(images) or
                        RemunerationFacts.model_validate({"fiscal_year": "2025", "roles": [],
                                                          "pension_type": none_t, "benefits": none_t,
                                                          "shareholding_requirement": none_t}))
    pdf = _pdf(tmp_path, ["intro", "table"])
    monkeypatch.setattr(pay, "PAGE_IMAGES", False)
    pay.ask_pay("X", "u", [Chunk(1, TABLE, [2])], "the report", "y", pdf, {2: TABLE})
    assert seen == [None]
