"""Text of a scanned PDF, read by the AI from page images.

Some filings have no text layer: a UK subsidiary files its parent's consolidated
accounts on paper, and Companies House serves the scan (TWMA Group, docs/known_issues.md
issue 6). Each page is rendered to an image and the model copies its text, a few pages
per call; the pages are cached, so a re-run costs nothing. The text is then read like
any report's. OCR=0 turns this off (the scanned PDF is then skipped, as before).
"""

import hashlib
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydantic import BaseModel
from tenacity import stop_after_attempt

from . import llm
from .config import CACHE_DIR
from .scraper import NeedsOCRError, Page

log = logging.getLogger(__name__)

ENABLED = os.getenv("OCR", "1").lower() not in ("0", "false", "no")
MAX_PAGES = 120                # longer scans are skipped: a report, not one set of accounts
PAGES_PER_CALL = 4
DPI = 120
WORKERS = 4


class PageText(BaseModel):
    page: int
    text: str


class PageTexts(BaseModel):
    pages: list[PageText]


def _images(pdf_path: Path) -> list[bytes]:
    import pymupdf
    with pymupdf.open(pdf_path) as doc:
        if doc.page_count > MAX_PAGES:
            raise NeedsOCRError(f"Scanned PDF of {doc.page_count} pages (> {MAX_PAGES}): not read")
        return [p.get_pixmap(dpi=DPI, colorspace=pymupdf.csGRAY).tobytes("png") for p in doc]


def _ask(numbers: list[int], pngs: list[bytes]) -> PageTexts:
    # Two tries, not the usual eight: a call that times out has usually started
    # repeating itself, and the pages are then read one at a time instead.
    call = llm.call_llm.retry_with(stop=stop_after_attempt(2))
    return call(llm.load_prompt("ocr_system"),
                f"The images are pages {', '.join(map(str, numbers))}, in this order.",
                PageTexts, images=pngs)


def _read(first: int, pngs: list[bytes], cache: Path) -> list[Page]:
    """Pages first .. first+len(pngs)-1 (1-based), from the cache or one AI call. A
    failing call is split into one call per page; a page that still fails is left
    empty (not cached), so the rest of the document is still read."""
    if cache.exists():
        return [Page(p["number"], p["text"]) for p in json.loads(cache.read_text(encoding="utf-8"))]
    numbers = list(range(first, first + len(pngs)))
    try:
        got = _ask(numbers, pngs)
    except Exception as e:  # noqa: BLE001 - timeouts, refusals, bad output
        if len(pngs) == 1:
            log.warning("Scanned page %d not read: %s", first, str(e)[:120])
            return [Page(first, "")]
        log.warning("Scanned pages %d-%d: %s; reading them one at a time",
                    numbers[0], numbers[-1], str(e)[:120])
        return [p for i, png in enumerate(pngs)
                for p in _read(first + i, [png], cache.with_name(f"{cache.stem}_{first + i}.json"))]
    texts = {p.page: p.text for p in got.pages}
    if set(texts) != set(numbers) and len(got.pages) == len(numbers):
        texts = dict(zip(numbers, (p.text for p in got.pages)))   # renumbered: keep the order
    pages = [Page(n, texts.get(n, "")) for n in numbers]
    cache.write_text(json.dumps([{"number": p.number, "text": p.text} for p in pages],
                                ensure_ascii=False), encoding="utf-8")
    return pages


def pdf_pages(pdf_path: Path) -> list[Page]:
    """The scanned PDF's pages as text (markdown tables), read by the AI."""
    if not ENABLED:
        raise NeedsOCRError("The PDF is scanned and OCR is off (OCR=0)")
    pngs = _images(pdf_path)
    key = hashlib.sha1(pdf_path.read_bytes() + llm.load_prompt("ocr_system").encode()).hexdigest()[:16]
    CACHE_DIR.mkdir(exist_ok=True)
    batches = [(i + 1, pngs[i:i + PAGES_PER_CALL]) for i in range(0, len(pngs), PAGES_PER_CALL)]
    log.info("Scanned PDF: the AI reads %d page images (%d calls)", len(pngs), len(batches))
    with ThreadPoolExecutor(WORKERS) as pool:
        parts = list(pool.map(lambda b: _read(b[0], b[1], CACHE_DIR / f"ocr_{key}_{b[0]}.json"),
                              batches))
    return [p for part in parts for p in part]
