"""Run files and checks of the role-based pay extractor (pay_roles_output.py), and gap-fill
(pay_roles.py --mode gapfill), with the same fakes as test_pay_roles.py."""

import csv
import json

import pytest

from extractor import pay_roles as pr, pay_roles_output as out
from tests.test_pay_roles import cell, env, line  # noqa: F401 - env is a fixture


def doc(lines, status="ok", mode="all", roles=None):
    return {"company_id": "c1", "company_name": "Acme AB", "country": "SE", "status": status,
            "run_mode": mode, "roles": roles or [], "fiscal_year": "2025",
            "period_end": "2025-12-31", "source_file": "SE_Acme.pdf", "match_type": "lei",
            "chunk_pages": {"1": [4, 5]}, "lines": lines}


def item(ln, detail="ceo", code="ceo", source="auto", pid="p1", **mapping):
    return {"pay_line_id": pid, "line": ln, "quote_check": {},
            "mapping": {"role_detail": detail, "role_code": code, "cdp_role_id": "",
                        "mapping_source": source, "mapping_confidence": "high", **mapping}}


def kinds(findings):
    return sorted(f.kind for f in findings)


class TestChecks:
    def test_total_that_does_not_add_up(self):
        ln = line("CEO", 1000)
        ln["pension"] = cell(200)
        ln["total"] = cell(1500)
        f = [x for x in out.check_company(doc([item(ln)])) if x.kind == "total_mismatch"]
        assert f and f[0].gap and "without LTI 1200" in f[0].detail

    def test_total_that_adds_up_with_lti_or_rounding(self):
        ln = line("CEO", 1000)
        ln["lti_vested"] = {**cell(500), "form": "shares"}
        ln["total"] = cell(1500)
        assert "total_mismatch" not in kinds(out.check_company(doc([item(ln)])))
        ln2 = line("CEO", 1000)
        ln2["total"] = cell(1001)                     # 1 printed unit of rounding
        assert "total_mismatch" not in kinds(out.check_company(doc([item(ln2)])))

    def test_completeness_follows_the_when_rules(self):
        ceo = item(line("CEO", 10))
        found = kinds(out.check_company(doc([ceo])))
        assert found.count("completeness") == 3      # chair, CFO/group, board members
        chair = item(line("Ordförande", 1), "board_chair", "board_chair", pid="p2")
        group = item(line("Övriga", 5, aggregate=True), "executive_management_group",
                     "executive_team_aggregate", pid="p3")
        board = item(line("Styrelsen", 4, aggregate=True), "board_group", "board_aggregate",
                     pid="p4")
        assert "completeness" not in kinds(out.check_company(doc([ceo, chair, group, board])))
        # a by-role request for the CEO only is not short of a chair
        assert "completeness" not in kinds(out.check_company(doc([ceo], mode="role",
                                                                  roles=["ceo"])))

    def test_unit_and_currency_warnings(self):
        ln = line("CFO", 2_500_000)                   # 2.5 billion in a tkr table?
        ln["pension"] = {**cell(10), "currency_printed": "EUR"}
        k = kinds(out.check_company(doc([item(ln, "cfo", "cfo")])))
        assert "unit_scale" in k and "currency_mix" in k
        small = line("CEO", 950)
        small["base_salary"]["unit"] = "units"
        assert "unit_scale" in kinds(out.check_company(doc([item(small)])))

    def test_roles_periods_quotes_duplicates(self):
        sugg = item(line("Head of Sustainability", 5), "exco_member", "other_executive",
                    "suggestion", pid="p1")
        unm = item(line("Senior adviser", 5), "", "", "unmapped", pid="p2")
        former = item(line("Former CEO", 5), pid="p3", title_part_year=True)
        dup = item(line("Former CEO", 6), pid="p4")
        badq = item(line("CFO", 7), "cfo", "cfo", pid="p5")
        badq["quote_check"] = {"base_salary": False}
        k = kinds(out.check_company(doc([sugg, unm, former, dup, badq])))
        for kind in ("role_suggestion", "role_unmapped", "period_check", "duplicate_line",
                     "quote_not_found"):
            assert kind in k

    def test_empty_core_for_an_individual_executive(self):
        f = [x for x in out.check_company(doc([item(line("CFO"), "cfo", "cfo")]))
             if x.kind == "empty_core"]
        assert f and f[0].field == "base_salary" and f[0].gap


class TestRows:
    def test_fact_row_is_verbatim(self):
        ln = line("Verkställande direktör", 12400, name="Anna")
        ln["sti_target"] = {k: None for k in ("value", "printed", "form", "unit_printed",
                                               "currency_printed", "quote", "chunk_id")}
        ln["sti_target"].update(value=60, form="pct_of_base", printed="60%")
        row = out.fact_row(doc([]), item(ln), "run1", ["total_mismatch"])
        assert row["base_salary"] == "12400" and row["units"] == "tkr"
        assert row["pay_currency"] == "SEK" and row["fiscal_year"] == 2025
        assert (row["sti_target_value"], row["sti_target_basis"]) == ("60", "pct_of_base")
        assert row["token_salary"] is False and row["review_flags"] == "total_mismatch"

    def test_token_salary(self):
        ln = line("CEO", 1)
        ln["base_salary"]["unit"] = "units"
        assert out.fact_row(doc([]), item(ln), "r", [])["token_salary"] is True

    def test_evidence_row_has_page_and_destination(self):
        ln = line("CEO", 12400)
        ln["pension_allowance"] = cell(300)
        rows = {r["field"]: r for r in out.evidence_rows(doc([]), item(ln))}
        assert rows["base_salary"]["page"] == "4,5" and rows["base_salary"]["goes_to"] == "base_salary"
        assert rows["pension_allowance"]["goes_to"] == "evidence only"
        assert rows["base_salary"]["printed"] == "12 400"

    @pytest.mark.parametrize("fy, end, want", [("2025", "2025-12-31", 2025),
                                               ("2024/25", "2025-03-31", 2025),
                                               ("2024/25", None, 2025), (None, None, None)])
    def test_fiscal_year(self, fy, end, want):
        assert out.fiscal_year_int(fy, end) == want

    def test_quote_grades(self):
        # the wrapped label's two parts have another column's cell between them
        chunks = {1: "|Ellen Trane Nørby,|Board|\n|formand|1.098.035|900.000|\n|Pension|300|",
                  2: "| Bonus | 50 |"}
        assert out.quote_grade("formand|1.098.035", "1.098.035", 1, chunks) == "exact"
        # a wrapped label joined by the AI: the figure and most words are there
        assert out.quote_grade("Ellen Trane Nørby, formand|1.098.035", "1.098.035", 1,
                               chunks) == "close"
        # the figure is not in the quote's chunk
        assert out.quote_grade("Ellen Trane Nørby, formand|2.000.000", "2.000.000", 1,
                               chunks) == "missing"
        assert out.quote_grade(None, "1", 1, chunks) is None

    def test_comparison_year(self):
        assert out.comparison_year("Benedicte|g||2024|138|||**138**", 2025)
        assert not out.comparison_year("Anna|2025|550|2024|535", 2025)
        assert not out.comparison_year("Grundlön|12 400", 2025)

    def test_comparison_year_is_flagged(self):
        ln = line("Board member")
        ln["base_salary"] = cell(138, quote="Grieg||2024|138")
        f = [x for x in out.check_company(doc([item(ln, "non_executive_director",
                                                       "board_member")]))
             if x.kind == "comparison_year"]
        assert f and f[0].gap and "2024" in f[0].detail

    def test_quote_found(self):
        chunks = {1: "| Grundlön | 12 400 |\n| Pension | 300 |"}
        assert out.quote_found("Grundlön|12 400", 1, chunks) is True
        assert out.quote_found("Grundlön 12400", 2, chunks) is True        # any chunk
        assert out.quote_found("Bonus|900", 1, chunks) is False
        assert out.quote_found(None, 1, chunks) is None


class TestRunFiles:
    def test_run_writes_the_three_csvs(self, env):
        pr.main(["--mode", "all", "--only", "acme-a", "--run-id", "o1"] + env["args"])
        d = env["tmp"] / "runs" / "o1"
        with (d / "fact_pay_line.csv").open(encoding="utf-8-sig") as fh:
            facts = list(csv.DictReader(fh))
        assert len(facts) == 4 and facts[0]["base_salary"] == "12400"
        assert facts[0]["role_code"] == "ceo" and facts[0]["run_id"] == "o1"
        with (d / "evidence.csv").open(encoding="utf-8-sig") as fh:
            ev = list(csv.DictReader(fh))
        assert {r["quote_found"] for r in ev} == {"exact"}
        with (d / "role_review.csv").open(encoding="utf-8-sig") as fh:
            review = {r["kind"] for r in csv.DictReader(fh)}
        assert {"role_suggestion", "role_unmapped", "completeness"} <= review
        run = json.loads((d / "run.json").read_text(encoding="utf-8"))
        assert run["files"]["lines"] == 4

    def test_gapfill_asks_only_flagged_cells_and_keeps_the_old_value(self, env, monkeypatch):
        pr.main(["--mode", "all", "--only", "acme-a", "--run-id", "g0"] + env["args"])
        first = env["tmp"] / "runs" / "g0" / "companies" / "acme-a.json"
        saved = json.loads(first.read_text(encoding="utf-8"))
        saved["lines"][0]["line"]["total"] = cell(99999, quote="Totalt|20 000")   # will not add up
        first.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
        n = len(env["calls"])
        rc = pr.main(["--mode", "gapfill", "--from-run", "g0", "--run-id", "g1"] + env["args"])
        assert rc == 0 and len(env["calls"]) == n + 1
        call = env["calls"][-1]
        assert call["schema"] == "GapAnswer" and "Cells to check:" in call["user"]
        assert "| total |" in call["user"] and "| base_salary |" in call["user"]
        assert "### total" in call["system"] and "### pension\n" not in call["system"]
        new = json.loads((env["tmp"] / "runs" / "g1" / "companies" / "acme-a.json")
                         .read_text(encoding="utf-8"))
        total = new["lines"][0]["line"]["total"]
        assert total["value"] == 99 and total["previous"]["value"] == 99999
        assert new["gapfill"]["of_run"] == "g0" and new["gapfill"]["changed"] >= 1
        assert json.loads(first.read_text(encoding="utf-8"))["lines"][0]["line"]["total"]["value"] == 99999
        with (env["tmp"] / "runs" / "g1" / "evidence.csv").open(encoding="utf-8-sig") as fh:
            ev = [r for r in csv.DictReader(fh) if r["field"] == "total"]
        assert ev[0]["previous_value"] == "99999" and ev[0]["note"].startswith("rechecked")

    def test_gapfill_dry_run_counts_cells(self, env, capsys):
        pr.main(["--mode", "all", "--only", "acme-a", "--run-id", "g2"] + env["args"])
        n = len(env["calls"])
        assert pr.main(["--mode", "gapfill", "--from-run", "g2", "--dry-run"] + env["args"]) == 0
        assert len(env["calls"]) == n
