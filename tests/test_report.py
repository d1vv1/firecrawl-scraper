"""Fill-rate report."""

import json

from extractor import report
from extractor.batch import Company


def _result(status="ok", revenue=1.0, assets=1.0, fy="2025"):
    return {"status": status, "fiscal_year": fy, "lei": "L", "website": "https://x",
            "revenue": {"value": revenue}, "total_assets": {"value": assets},
            "revenue_model": {"categories": ["product_sales"], "description": "x"},
            "business_structure": {"segments": ["A"], "legal_form": "AB", "is_listed": True}}


def test_fill_rate_counts_per_segment(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "CACHE_DIR", tmp_path)
    cs = [Company("a", "A AB", "SE"), Company("b", "B AB", "SE"), Company("c", "C ASA", "NO"),
          Company("d", "D Oyj", "FI")]
    (tmp_path / "a.json").write_text(json.dumps(_result()))
    (tmp_path / "b.json").write_text(json.dumps(_result(status="needs_review", assets=None, fy="2019")))
    (tmp_path / "c.error.json").write_text(json.dumps({"error_type": "ReportNotFoundError"}))
    # d has no file: pending, not a miss
    md = report.build_report(cs, output_dir=tmp_path)
    rows = {line.split(" | ")[0].strip("| "): line for line in md.splitlines() if line.startswith("|")}
    assert "| Processed so far | 2 / 2 (100.0%) | 0 / 1 (0.0%) | 1 / 1 (100.0%) | **3 / 4 (75.0%)** |" in md
    assert rows["Revenue"].endswith("**2 / 3 (66.7%)** |")
    assert rows["Revenue, verified (all checks pass)"].endswith("**1 / 3 (33.3%)** |")
    assert rows["Total assets"].endswith("**1 / 3 (33.3%)** |")
    assert rows["Report is recent (FY within 2 years)"].endswith("**1 / 3 (33.3%)** |")
    assert "| SE | FI | NO |" in md
