"""The golden-sample scorer (extractor/pay_roles_score.py), on a run made with the fakes of
test_pay_roles.py."""

import csv
import json

import pytest

from extractor import pay_roles as pr, pay_roles_score as sc
from tests.test_pay_roles import env  # noqa: F401 - fixture

GOLD_COLS = ["company_id", "role_title", "person_name", "role_detail", "role_code",
             "role_disclosure", "period_coverage", "base_salary", "total_remuneration", "page",
             "note"]


def golden(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=GOLD_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


@pytest.mark.parametrize("text, want", [
    ("12 400", 12400), ("12 400", 12400), ("1,050", 1050), ("1.234,5", 1234.5),
    ("1,234.5", 1234.5), ("1.234", 1234), ("0.376", 0.376), ("1,5", 1.5), ("(250)", -250),
    ("-250", -250), ("−250", -250), ("60%", 60), ("", None), (None, None), ("n/a", None)])
def test_number(text, want):
    assert sc.number(text) == want


class TestScore:
    def run(self, env):
        pr.main(["--mode", "all", "--only", "acme-a", "--run-id", "s1"] + env["args"])
        return env["tmp"] / "runs" / "s1"

    def test_all_pass(self, env):
        run_dir = self.run(env)
        g = golden(env["tmp"] / "g.csv", [
            {"company_id": "acme-a", "role_title": "Verkställande direktör", "person_name": "Anna A",
             "role_detail": "ceo", "role_code": "ceo", "role_disclosure": "individual",
             "period_coverage": "full_year", "base_salary": "12 400", "page": "1"},
            {"company_id": "acme-a", "role_title": "Tidigare VD", "person_name": "Bo B",
             "role_detail": "ceo", "role_code": "ceo", "base_salary": "3100"}])
        result, cells = sc.score(run_dir, g, sc.ref_roles.load(env["xlsx"]))
        r = result["rates"]
        assert r["required_recall"] == 1 and r["role_code"] == 1 and r["exact"] == 1
        assert r["wrong"] == 0
        assert result["counts"]["extra"] == 0
        assert {c["result"] for c in cells} == {"exact"}

    def test_wrong_missing_and_not_found(self, env):
        run_dir = self.run(env)
        g = golden(env["tmp"] / "g.csv", [
            {"company_id": "acme-a", "role_title": "VD", "person_name": "Anna A",
             "role_detail": "ceo", "role_code": "ceo", "base_salary": "12 500",
             "total_remuneration": "20 000"},
            {"company_id": "acme-a", "role_title": "Styrelseordförande", "person_name": "Eva E",
             "role_detail": "board_chair", "role_code": "board_chair", "base_salary": "900"}])
        result, cells = sc.score(run_dir, g, sc.ref_roles.load(env["xlsx"]))
        n = result["counts"]
        assert (n["wrong"], n["missing"], n["exact"]) == (1, 2, 0)
        assert result["rates"]["required_recall"] == 0.5          # the chair was not found
        assert cells[0]["result"] == "wrong" and cells[0]["golden"] == "12 500"
        assert any(c["run_role_title"] == "(not found)" for c in cells)
        assert not result["all_passed"]

    def test_pairing_prefers_the_person(self):
        run = [{"line": {"person_name": "Bo B", "printed_title": "CEO"}, "mapping": {"role_detail": "ceo"}},
               {"line": {"person_name": "Anna A", "printed_title": "CEO"}, "mapping": {"role_detail": "ceo"}}]
        pairs = sc.pair([{"person_name": "anna a", "role_detail": "ceo"}], run)
        assert pairs[0][1]["line"]["person_name"] == "Anna A"

    def test_cli_writes_files_and_exit_code(self, env, capsys):
        run_dir = self.run(env)
        g = golden(env["tmp"] / "g.csv", [
            {"company_id": "acme-a", "role_title": "VD", "person_name": "Anna A",
             "role_detail": "ceo", "role_code": "ceo", "base_salary": "12400"}])
        rc = sc.main(["--run", "s1", "--golden", str(g), "--ref-roles", str(env["xlsx"])])
        out = capsys.readouterr().out
        assert "required-role recall" in out and "FAIL  completeness" in out
        assert rc == 2                                          # completeness fails: no chair
        assert (run_dir / "score_cells.csv").exists()
        assert json.loads((run_dir / "score.json").read_text(encoding="utf-8"))["passed"]["exact"]
        assert sc.main(["--run", "nope", "--golden", str(g)]) == 1
