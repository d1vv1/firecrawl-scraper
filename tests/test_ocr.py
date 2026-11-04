"""Scanned PDFs read from page images (extractor/ocr.py, issue 6)."""

import pymupdf
import pytest

from extractor import ocr
from extractor.scraper import NeedsOCRError


def _scan(path, pages):
    doc = pymupdf.open()
    for _ in range(pages):
        doc.new_page()
    doc.save(path)
    return path


def test_pages_are_read_in_batches_and_cached(tmp_path, monkeypatch):
    monkeypatch.setattr(ocr, "CACHE_DIR", tmp_path)
    calls = []

    def fake(numbers, pngs):
        calls.append(len(pngs))
        return ocr.PageTexts(pages=[ocr.PageText(page=n, text=f"text {n}") for n in numbers])
    monkeypatch.setattr(ocr, "_ask", fake)
    pdf = _scan(tmp_path / "s.pdf", 6)
    pages = ocr.pdf_pages(pdf)
    assert [p.number for p in pages] == [1, 2, 3, 4, 5, 6]
    assert pages[4].text == "text 5" and sorted(calls) == [2, 4]
    ocr.pdf_pages(pdf)
    assert len(calls) == 2                       # the second read comes from the cache


def test_renumbered_pages_keep_their_order(tmp_path, monkeypatch):
    monkeypatch.setattr(ocr, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(ocr, "_ask", lambda numbers, pngs: ocr.PageTexts(
        pages=[ocr.PageText(page=i + 1, text=f"p{i}") for i in range(len(pngs))]))
    pages = ocr._read(5, [b"a", b"b"], tmp_path / "c.json")
    assert [(p.number, p.text) for p in pages] == [(5, "p0"), (6, "p1")]


def test_off_or_too_long(tmp_path, monkeypatch):
    pdf = _scan(tmp_path / "s.pdf", 3)
    monkeypatch.setattr(ocr, "ENABLED", False)
    with pytest.raises(NeedsOCRError):
        ocr.pdf_pages(pdf)
    monkeypatch.setattr(ocr, "ENABLED", True)
    monkeypatch.setattr(ocr, "MAX_PAGES", 2)
    with pytest.raises(NeedsOCRError):
        ocr.pdf_pages(pdf)


def test_a_failing_batch_is_read_page_by_page(tmp_path, monkeypatch):
    monkeypatch.setattr(ocr, "_ask", lambda numbers, pngs: (_ for _ in ()).throw(TimeoutError())
                        if len(pngs) > 1 or numbers == [6] else
                        ocr.PageTexts(pages=[ocr.PageText(page=numbers[0], text=f"t{numbers[0]}")]))
    pages = ocr._read(5, [b"a", b"b", b"c"], tmp_path / "c.json")
    assert [(p.number, p.text) for p in pages] == [(5, "t5"), (6, ""), (7, "t7")]
    assert not (tmp_path / "c_6.json").exists()        # the failed page is tried again next run
