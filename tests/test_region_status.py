import openpyxl

from extractor import region_status as rs


def test_workbook_rows_merge_and_paths(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Country", "Region", "Company Name", "Company ID", "GCS path Annual Report",
               "GCS path Remuneration (if there)", "Other reports", "LEI", "FY"])
    ws.append(["Sweden", "Nordics", "Elekta AB", "elekta-ab-1a2b3c4d", None, None, None, None, "FY2026"])
    ws.append(["Sweden", "Nordics", "Elekta AB", "elekta-ab-1a2b3c4d", "gs://b/uploads/x/fy2025/a.pdf",
               "Inside annual report", None, None, "FY2025"])
    ws.append(["Denmark", "Nordics", "Jeudan A/S", None,
               "(not in GCS yet) nordics/dk/listed/jeudan--jeudan/fy2025/", None, None, None, "FY2025"])
    p = tmp_path / "list.xlsx"
    wb.save(p)
    cos = rs.read_workbook(p)
    assert len(cos) == 2
    elekta = cos[0]
    assert elekta["fy"] == "FY2025" and elekta["country_code"] == "SE"
    assert rs._paths(elekta["ar"]) == (["gs://b/uploads/x/fy2025/a.pdf"], [])
    assert rs._paths(cos[1]["ar"])[1]                         # staged, not in GCS yet


def test_conditional_fields_are_not_required():
    assert rs.is_required("Required")
    assert rs.is_required("Required (one of headcount/fte)")
    assert not rs.is_required("Required if LTI plan exists")
    assert not rs.is_required("Optional")
