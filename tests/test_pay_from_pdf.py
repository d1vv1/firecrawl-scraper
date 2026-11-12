"""One PDF in, pay rows out (extractor/pay_from_pdf.py), with the pay route stubbed."""

import csv

import pymupdf

from extractor import pay_from_pdf as pf
from extractor.apis import Found


def _pdf(path):
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_textbox(pymupdf.Rect(72, 72, 520, 760),
                        "Remuneration report. " + "The CEO received a base salary. " * 40)
    doc.save(path)
    return path


def test_one_pdf_gives_pay_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(pf, "CACHE_DIR", tmp_path / "cache")
    seen = {}

    def fake_from_pay(name, slug, lib, report, report_key, period_end):
        seen.update(name=name, lib=lib, source=report.source, url=report.url, pdf=report.pdf)
        return ([Found("base_salary", 1_242_000, unit="USD", period_end=period_end, grain="role",
                       role_row="CEO", confidence="B", method="PARSE", source=report.source,
                       endpoint=report.url + "#page=1")],
                [Found("pension_type", "defined contribution", confidence="B", method="PARSE")],
                [report.source])
    monkeypatch.setattr(pf, "from_pay", fake_from_pay)
    pdf = _pdf(tmp_path / "rem.pdf")
    out = tmp_path / "pay.csv"
    assert pf.main([str(pdf), "--company", "Acme AB", "--period-end", "2025-12-31",
                    "--out", str(out)]) == 0
    assert seen["name"] == "Acme AB" and seen["lib"] is None and seen["pdf"] == pdf
    assert seen["source"] == "rem.pdf (PDF)" and seen["url"].startswith("file:///")
    rows = list(csv.DictReader(out.open(encoding="utf-8-sig")))
    assert [(r["role_row"], r["data_point"], r["value"]) for r in rows] == [
        ("CEO", "base_salary", "1242000"), ("", "pension_type", "defined contribution")]
    assert rows[0]["period_end"] == "2025-12-31" and rows[0]["company"] == "Acme AB"
    assert rows[1]["period_end"] == "2025-12-31"             # the pay term: the pay year's
    assert list((tmp_path / "cache").glob("pdf_*.md"))       # the text is cached


def test_no_pay_found_exits_2(tmp_path, monkeypatch):
    monkeypatch.setattr(pf, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pf, "from_pay", lambda *a: ([], [], []))
    assert pf.main([str(_pdf(tmp_path / "x.pdf")), "--out", str(tmp_path / "o.csv")]) == 2
    assert pf.main([str(tmp_path / "missing.pdf")]) == 1
