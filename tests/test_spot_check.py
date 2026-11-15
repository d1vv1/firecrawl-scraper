"""The spot-check sheet: a sample of a run's companies, one line per value to check by hand."""

import csv

from extractor import spot_check as sc


def _rows():
    rows = []
    for i in range(40):
        cid, country = f"c{i:02d}", ("GB", "DE", "CH", "NO")[i % 4]
        base = {"company_id": cid, "company_name": cid.upper(), "country": country, "unit": "",
                "period_end": "2025-12-31", "source": "Annual report (PDF)", "endpoint": "",
                "confidence": "B"}
        rows.append({**base, "grain": "company", "role_row": "", "data_point": "revenue",
                     "value": "100", "note": 'PDF page 3: "Revenue 100"'})
        rows.append({**base, "grain": "company", "role_row": "", "data_point": "sec_cik",
                     "value": "", "note": "not applicable: not an SEC registrant"})
        rows.append({**base, "grain": "company", "role_row": "", "data_point": "headcount",
                     "value": "", "note": "not found in: Annual report (PDF)"})
        for k in ("base_salary", "sti_paid", "lti_granted"):
            rows.append({**base, "grain": "role", "role_row": "CEO", "data_point": k,
                         "value": "" if i < 10 else "5", "note": "not found in: x" if i < 10 else "q"})
    return rows


def test_the_sample_mixes_countries_and_takes_companies_with_little_pay_data():
    rows = _rows()
    ids = sc.sample(rows, 0.2, seed=1)
    assert len(ids) == 8 and ids == sc.sample(rows, 0.2, seed=1) and ids != sc.sample(rows, 0.2, seed=2)
    country = {r["company_id"]: r["country"] for r in rows}
    assert {country[c] for c in ids} == {"GB", "DE", "CH", "NO"}
    assert sum(1 for c in ids if c < "c10") >= 2            # the ten with no pay values
    assert len(sc.sample(rows[:6], 0.1)) == 1               # never an empty sample


def test_the_sheet_has_a_line_per_value_asked_for(tmp_path):
    rows = _rows()
    lines = sc.sheet(rows, ["c00", "c11"], {("c11", "CEO", "base_salary"): "Fail (hard)"}, skip=("sti", "lti"))
    assert [(r["company_id"], r["data_point"]) for r in lines] == [
        ("c00", "revenue"), ("c00", "headcount"), ("c00", "base_salary"),
        ("c11", "revenue"), ("c11", "headcount"), ("c11", "base_salary")]
    assert lines[-1]["checks"] == "Fail (hard)" and lines[0]["result"] == ""
    run = tmp_path / "run_datapoints.csv"
    with open(run, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    assert sc.main([str(run)]) == 0
    with open(tmp_path / "run_datapoints_spot_check.csv", encoding="utf-8-sig", newline="") as fh:
        out = list(csv.DictReader(fh))
    assert len({r["company_id"] for r in out}) == 4 and list(out[0]) == sc.COLUMNS
