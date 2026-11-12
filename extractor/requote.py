"""A second look at quotes that are not in the text.

The AI gives every value a quote, and a value whose quote is not found word for word
(or does not print its figure) is graded C: on 12 November 2026 that was most of the
1,122 hard fails of the combined file. Most of those quotes are real text in the wrong
shape: cells of a table pieced together, a sentence shortened or reworded. Here the AI
is shown each such value again, with only the part of the document where it should be
(the chunk it cited and the chunks that best match the quote and print the figure), and
asked for the passage as printed. A new quote is used only when it is in the text and
prints the figure; otherwise the value stays as it was (graded C). Nothing is added
and no value is changed: only the quote and its chunk.

One call per document read, cached by its content. REQUOTE=0 turns it off.
"""

import hashlib
import json
import logging
import os
import re
from typing import Iterator, Optional

import openai
from pydantic import BaseModel

from . import llm
from .config import CACHE_DIR, fold
from .sections import Chunk
from .validate import figure_in_quote

log = logging.getLogger(__name__)

ON = os.getenv("REQUOTE", "1").lower() not in ("0", "false", "no")
MAX_ITEMS = 25          # values looked at again per call (a call per document)
NEAR_CHUNKS = 2         # chunks shown per value besides the one it cited
MAX_WORDS = 60_000      # of text per call
_LABEL = re.compile(r"[^\W\d_]{3,}")   # a word: a figure on its own is no source


class Requote(BaseModel):
    id: int
    quote: Optional[str]
    chunk_id: Optional[int]


class Requotes(BaseModel):
    items: list[Requote]


def quoted(obj, path: str = "", who: str = "") -> Iterator[tuple[str, BaseModel]]:
    """Every part of the AI's answer that carries a quote, with a label saying which
    ("roles[1] (CFO, Jane Doe) base_salary")."""
    if isinstance(obj, BaseModel):
        fields = type(obj).model_fields
        title = getattr(obj, "role_title", None)
        if title:
            who = f" ({', '.join(x for x in (title, getattr(obj, 'person_name', None)) if x)})"
            path += who
        if "quote" in fields and "chunk_id" in fields:
            yield path, obj
        for name in fields:
            yield from quoted(getattr(obj, name), f"{path} {name}".strip(), who)
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from quoted(x, f"{path}[{i}]", who)


def shown(obj: BaseModel) -> str:
    """The value as the AI gave it, for the second look."""
    for attr in ("value", "name", "role_title"):
        v = getattr(obj, attr, None)
        if v not in (None, ""):
            return f"{v:g}" if isinstance(v, float) else str(v)
    items = getattr(obj, "items", None) or []
    return "; ".join(f"{getattr(i, 'country', None) or getattr(i, 'segment', '')}: {i.value:g}"
                     for i in items)


def figure_of(obj: BaseModel) -> float | None:
    v = getattr(obj, "value", None)
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def sound(obj: BaseModel, origin, quote: str | None = None, chunk_id: int | None = None) -> str | None:
    """The quote as datapoints places it (the source row, when it stands in for a quote
    pieced together), if it is in the text and prints the value's figure; else None.
    A figure of 0 needs no print: tables show it as a dash."""
    figure = figure_of(obj)
    placed = origin.place(quote or obj.quote, chunk_id if quote else obj.chunk_id, figure)
    ok = placed[2] == "B" and (not figure or figure_in_quote(figure, placed[4]))
    return placed[4] if ok else None


def all_chunks(origin) -> dict[int, Chunk]:
    """The chunks of a document, or of several read together (datapoints.Bundle)."""
    out: dict[int, Chunk] = {}
    for o in getattr(origin, "origins", None) or [origin]:
        out |= o.chunks
    return out


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{4,}", fold(text).lower()))


def near(obj: BaseModel, chunks: dict[int, Chunk], folded: dict[int, set[str]]) -> list[int]:
    """The chunks to show for a value: the one it cited, and the NEAR_CHUNKS others that
    share the most words with its quote, those printing its figure first."""
    figure, words = figure_of(obj), _words(obj.quote or "")
    scored = []
    for cid, c in chunks.items():
        if cid == obj.chunk_id:
            continue
        score = len(words & folded[cid]) + (1000 if figure and figure_in_quote(figure, c.text) else 0)
        if score:
            scored.append((-score, cid))
    best = [cid for _, cid in sorted(scored)[:NEAR_CHUNKS]]
    return ([obj.chunk_id] if obj.chunk_id in chunks else []) + best


def repair(facts: BaseModel, origin, name: str, cache_key: str) -> int:
    """Give the values of `facts` whose quote is not sound a quote that is, in place.
    `origin`: the document (datapoints.Origin or Bundle) the facts were read from.
    Returns how many quotes were replaced."""
    if not ON or origin is None:
        return 0
    failing = [(label, obj) for label, obj in quoted(facts)
               if obj.quote and shown(obj) and not sound(obj, origin)]
    if not failing:
        return 0
    if len(failing) > MAX_ITEMS:
        log.info("Second look: %d quotes not in the text, the first %d looked at",
                 len(failing), MAX_ITEMS)
        failing = failing[:MAX_ITEMS]
    chunks = all_chunks(origin)
    folded = {cid: _words(c.text) for cid, c in chunks.items()}
    show: dict[int, Chunk] = {}
    words = 0
    wanted = [near(obj, chunks, folded) for _, obj in failing]
    for rank in range(NEAR_CHUNKS + 1):         # every value's first chunk before any second
        for cids in wanted:
            cid = cids[rank] if rank < len(cids) else None
            if cid is not None and cid not in show and words + chunks[cid].words <= MAX_WORDS:
                show[cid] = chunks[cid]
                words += chunks[cid].words
    if not show:
        return 0
    body = "\n\n".join(f'<chunk id="{cid}">\n{show[cid].text.strip()}\n</chunk>' for cid in sorted(show))
    items = [{"id": i, "field": label, "value": shown(obj), "quote_given": obj.quote,
              "chunk_id_given": obj.chunk_id} for i, (label, obj) in enumerate(failing)]
    user = (f"Company legal name: {name}\n\nParts of the text (tables are in markdown):\n\n{body}"
            f"\n\nItems:\n{json.dumps(items, ensure_ascii=False, indent=1)}")
    answer = _ask(user, cache_key)
    if answer is None:
        return 0
    done = 0
    for r in answer.items:
        if not r.quote or not 0 <= r.id < len(failing):
            continue
        label, obj = failing[r.id]
        found = sound(obj, origin, r.quote, r.chunk_id)
        if found and (figure_of(obj) is None or _LABEL.search(found)):
            log.debug("Second look: %s: %r -> %r", label, obj.quote, found)
            obj.quote, obj.chunk_id = found, r.chunk_id
            done += 1
    log.info("Second look: %d of %d quotes not in the text replaced by the passage as printed",
             done, len(failing))
    return done


def _ask(user: str, cache_key: str) -> Requotes | None:
    """The call, cached by everything it was given. None when the AI gave no answer:
    the values then stay as they were."""
    prompt = llm.load_prompt("quote_repair_system")
    digest = hashlib.sha1((prompt + user).encode()).hexdigest()
    path = CACHE_DIR / f"{cache_key}_requote_llm.json"
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        if saved.get("digest") == digest:
            return Requotes.model_validate(saved["answer"])
    try:
        answer = llm.call_llm(prompt, user, Requotes)
    except llm.StructuredOutputsUnsupportedError:
        raise
    except (openai.OpenAIError, llm.LLMRefusalError) as e:
        log.warning("Second look at the quotes failed (%s); values kept as they were",
                    str(e)[:150])
        return None
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"digest": digest, "model": llm.model_name(),
                                "answer": answer.model_dump()}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    return answer
