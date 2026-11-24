"""The role-based pay runner (extractor/pay_roles.py), with the reports folder, the report
text and the AI all faked: no files outside tmp_path are read or written, and no AI is asked."""

import csv
import json
import logging

import pytest

from extractor import pay_roles as pr, ref_roles, report_library as rl
from extractor.datapoints import Origin
from extractor.pay_roles_schema import CORE_FIELDS, FIELDS
from extractor.scraper import Page
from extractor.sections import Chunk
from tests.test_ref_roles import write


def report(name, country="SE", path=None, fmt="pdf"):
    return rl.Report(company=name, country=country, region="Nordics", report_type="Remuneration",
                     format=fmt, file_name=f"{country}_{name}_FY2025_Remuneration.pdf",
                     path=path or f"C:/reports/{country}_{name}.pdf", lei=None,
                     cdp_company_id=None, period_end="2025-12-31", drive_link=None,
                     in_scope_28Oct="yes")


def cell(value=None, quote=None):
    c = {k: None for k in FIELDS["base_salary"].cell.model_fields}
    if value is not None:
        c.update(value=value, printed=f"{value:,.0f}".replace(",", " "), unit_printed="tkr",
                 unit="thousands", currency_printed="SEK", quote=quote or f"Grundlön|{value}",
                 chunk_id=1)
    return c


def line(title, base=None, suggested=None, name=None, aggregate=False):
    out = {"printed_title": title, "person_name": name, "is_aggregate": aggregate,
           "aggregate_headcount": 7 if aggregate else None, "aggregate_excludes": None,
           "role_disclosure": "aggregate" if aggregate else "individual",
           "period_coverage": "full_year", "months_in_role": None, "period_quote": None,
           "suggested_role_detail": suggested, "suggested_cdp_role_id": None,
           "suggestion_reason": None, "quote": title, "chunk_id": 1}
    for f in CORE_FIELDS:
        out[f] = {k: None for k in FIELDS[f].cell.model_fields}
    out["base_salary"] = cell(base)
    return out


ANSWER = {"fiscal_year": "2025", "period_end": "2025-12-31", "lines": [
    line("Verkställande direktör", 12400, suggested="ceo", name="Anna A"),
    line("Tidigare VD (till 31 mars)", 3100, suggested="ceo", name="Bo B"),
    line("Head of Group Sustainability", 2900, suggested="exco_member", name="Cy C"),
    line("Senior adviser", 800, suggested=None, name="Di D"),
]}


def gap_cells(user):
    """The fake AI's gap-fill answer: every asked cell found again as 99, quoted from the text."""
    out = []
    for ln in user.split("Cells to check:")[1].split("\n\n")[0].strip().splitlines():
        ref, title, field = [p.strip() for p in ln[len("- line_ref "):].split("|")][:3]
        out.append({"line_ref": ref, "field": field, "found": True, "value": 99, "printed": "99",
                    "unit_printed": "tkr", "unit": "thousands", "currency_printed": "SEK",
                    "form": None, "includes": None, "quote": "Totalt|20 000", "chunk_id": 1,
                    "not_found_reason": None})
    return out


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """A fake reports folder, report text and AI; runs and cache in tmp_path."""
    xlsx = write(tmp_path / "ref_roles.xlsx")
    calls = []

    def call_llm(system, user, schema, images=None):
        calls.append({"system": system, "user": user, "schema": schema.__name__})
        logging.getLogger("extractor.llm").info("LLM %s: %d prompt + %d completion tokens",
                                                schema.__name__, 1000, 200)
        if schema.__name__ == "GapAnswer":
            return schema.model_validate({"cells": gap_cells(user)})
        return schema.model_validate(ANSWER)

    def read_origin(rep):
        pages = [Page(1, "Ersättning till ledande befattningshavare\nVD|12 400\n"
                         "Grundlön|12400\nGrundlön|3100\nGrundlön|2900\nGrundlön|800\n"
                         "Totalt|20 000")]
        chunks = {1: Chunk(1, pages[0].text, [1])}
        return Origin("pdf", "file:///x.pdf", "x.pdf (PDF)", "PARSE", "now", pages, chunks), "k"

    reports = {"Acme AB": report("Acme"), "Acme B": report("Acme"),     # same PDF: share lines
               "Nordbolag AB": report("Nordbolag")}

    def local_reports(lib, name, country, lei):
        if name == "Noreport Oy":
            return {"Annual": rl.Report(**{**report("Noreport", "FI").__dict__,
                                           "report_type": "Annual", "file_name": "FI_ann.pdf"})}, "name-exact"
        return ({"Remuneration": reports[name]}, "name-exact") if name in reports else ({}, "")

    monkeypatch.setattr(pr.llm, "call_llm", call_llm)
    monkeypatch.setattr(pr.llm, "model_name", lambda: "fake-model")
    monkeypatch.setattr(pr, "read_origin", read_origin)
    monkeypatch.setattr(pr.rl, "local_reports", local_reports)
    monkeypatch.setattr(pr.rl, "default_root", lambda: str(tmp_path))
    monkeypatch.setattr(pr.rl, "ReportRetriever", lambda root: object())
    monkeypatch.setattr(pr, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(pr, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(pr, "load_cdp_roles", lambda repo, ref: [("R011", "Chief Strategy Officer")])
    companies = tmp_path / "companies.csv"
    with companies.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["company_id", "company_name", "country", "lei", "run_required"])
        for row in [("acme-a", "Acme AB", "SE", "", "Pay Data"), ("acme-b", "Acme B", "SE", "", ""),
                    ("nord", "Nordbolag AB", "SE", "", "Company Data"),
                    ("nore", "Noreport Oy", "FI", "", "Pay Data"),
                    ("dk1", "Dansk A/S", "DK", "", "Pay Data")]:
            w.writerow(row)
    base = ["--companies", str(companies), "--ref-roles", str(xlsx), "--images", "off"]
    return {"tmp": tmp_path, "calls": calls, "args": base, "xlsx": xlsx}


def summary(env, run_id):
    with (env["tmp"] / "runs" / run_id / "summary.csv").open(encoding="utf-8-sig") as fh:
        return {r["company_id"]: r for r in csv.DictReader(fh)}


class TestRun:
    def test_role_run_end_to_end(self, env):
        rc = pr.main(["--mode", "role", "--roles", "required", "--countries", "SE,FI",
                      "--run-id", "r1"] + env["args"])
        assert rc == 0
        s = summary(env, "r1")
        assert set(s) == {"acme-a", "acme-b", "nord", "nore"}           # DK filtered out
        assert s["acme-a"]["status"] == "ok" and s["acme-a"]["lines"] == "4"
        assert s["acme-b"]["status"] == "duplicate_of:acme-a"
        assert s["nore"]["status"] == "no_local_report"
        assert s["nore"]["note"] == "annual_only:FI_ann.pdf"
        assert s["acme-a"]["prompt_tokens"] == "1000" and s["acme-a"]["cached"] == "False"
        # acme-a and nord: two AI calls; the duplicate and the missing one ask nothing
        assert len(env["calls"]) == 2
        assert "Roles to extract:" in env["calls"][0]["user"]
        assert "- R011: Chief Strategy Officer" in env["calls"][0]["user"]
        run = json.loads((env["tmp"] / "runs" / "r1" / "run.json").read_text(encoding="utf-8"))
        assert run["mode"] == "role" and run["ref_roles_version"].startswith("0.1-test+")
        assert run["statuses"] == {"ok": 2, "duplicate_of": 1, "no_local_report": 1}

    def test_lines_are_mapped_in_code_first(self, env):
        pr.main(["--mode", "all", "--only", "acme-a", "--run-id", "r2"] + env["args"])
        saved = json.loads((env["tmp"] / "runs" / "r2" / "companies" / "acme-a.json")
                           .read_text(encoding="utf-8"))
        m = {x["line"]["printed_title"]: x["mapping"] for x in saved["lines"]}
        assert m["Verkställande direktör"]["mapping_source"] == "auto"
        assert m["Verkställande direktör"]["cdp_role_id"] == "R001"
        former = m["Tidigare VD (till 31 mars)"]
        assert (former["role_detail"], former["title_part_year"]) == ("ceo", True)
        assert (m["Head of Group Sustainability"]["mapping_source"],
                m["Head of Group Sustainability"]["mapping_confidence"]) == ("suggestion", "medium")
        assert m["Senior adviser"]["mapping_source"] == "unmapped"
        assert saved["lines"][0]["line"]["base_salary"]["printed"] == "12 400"   # verbatim
        assert saved["report"]["file_name"] == "SE_Acme_FY2025_Remuneration.pdf"

    def test_resume_skips_done_companies_and_cache_skips_the_ai(self, env):
        args = ["--mode", "all", "--countries", "SE", "--run-id", "r3"] + env["args"]
        pr.main(args)
        n = len(env["calls"])
        pr.main(args)                                   # resume: everything done
        assert len(env["calls"]) == n
        pr.main(args + ["--force"])                     # forced: same requests, from the cache
        assert len(env["calls"]) == n
        assert summary(env, "r3")["acme-a"]["cached"] == "True"

    def test_dry_run_asks_nothing_and_writes_nothing(self, env, capsys, monkeypatch):
        from extractor import ocr
        monkeypatch.setattr(ocr, "ENABLED", True)
        rc = pr.main(["--mode", "role", "--countries", "SE", "--dry-run"] + env["args"])
        assert rc == 0 and env["calls"] == []
        assert ocr.ENABLED is False                     # scans are reported, not read by the AI
        assert not (env["tmp"] / "runs").exists()
        assert "estimated prompt tokens" in capsys.readouterr().out

    def test_by_field_asks_only_those_fields(self, env):
        global ANSWER
        pr.main(["--mode", "field", "--fields", "base_salary", "--only", "nord",
                 "--run-id", "r4"] + env["args"])
        assert "### base_salary" in env["calls"][0]["system"]
        assert "### pension" not in env["calls"][0]["system"]

    def test_a_failing_company_does_not_stop_the_run(self, env, monkeypatch):
        def boom(rep):
            raise RuntimeError("unreadable PDF")
        monkeypatch.setattr(pr, "read_origin", boom)
        rc = pr.main(["--mode", "all", "--countries", "SE", "--run-id", "r5"] + env["args"])
        assert rc == 1
        s = summary(env, "r5")
        assert s["acme-a"]["status"] == "error" and "unreadable PDF" in s["acme-a"]["note"]
        assert (env["tmp"] / "runs" / "r5" / "companies" / "acme-a.error.json").exists()

    def test_bad_requests(self, env, capsys):
        assert pr.main(["--mode", "field"] + env["args"]) == 1             # no fields
        assert pr.main(["--mode", "role", "--roles", "wizard"] + env["args"]) == 1
        assert pr.main(["--mode", "gapfill"] + env["args"]) == 1           # needs --from-run
        assert pr.main(["--mode", "gapfill", "--from-run", "nope"] + env["args"]) == 1


class TestMapRole:
    @pytest.fixture()
    def ref(self, tmp_path):
        return ref_roles.load(write(tmp_path / "ref_roles.xlsx"))

    def test_workbook_title_beats_the_suggestion(self, ref):
        m = pr.map_role(ref, line("Group CFO", suggested="ceo"), "SE", set())
        assert (m["role_detail"], m["mapping_source"], m["note"]) == ("cfo", "auto", "AI suggested ceo")

    def test_cdp_role_only_from_the_list_given(self, ref):
        ln = line("Chief Strategy Officer")
        ln["suggested_cdp_role_id"] = "R011"
        assert pr.map_role(ref, ln, "SE", {"R011"})["cdp_role_id"] == "R011"
        assert pr.map_role(ref, ln, "SE", set())["mapping_source"] == "unmapped"

    def test_unknown_suggestion_is_unmapped(self, ref):
        m = pr.map_role(ref, line("Chief Wizard", suggested="wizard"), "SE", set())
        assert m["mapping_source"] == "unmapped" and "wizard" in m["note"]


def test_blank_company_ids_get_a_stable_fallback(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text("company_id,company_name,country,lei\n,Stora Enso A,SE,\n,Stora Enso R,SE,\n"
                 "x1,Acme,SE,\n", encoding="utf-8")
    ids = [c.company_id for c in pr.read_companies(p, set(), set(), 0)]
    assert ids == ["noid-stora-enso-a-se", "noid-stora-enso-r-se", "x1"]
    # one id on two rows: share lines of one company ("SEB A", "SEB C"), read once
    p.write_text("company_id,company_name,country,lei\nseb,SEB A,SE,\nseb,SEB C,SE,\n",
                 encoding="utf-8")
    (seb,) = pr.read_companies(p, set(), set(), 0)
    assert (seb.company_name, seb.also_listed_as) == ("SEB A", ["SEB C"])


def test_pay_line_id_is_stable():
    a = pr.pay_line_id("c1", "2025", {"printed_title": "VD ", "person_name": "Anna"})
    assert a == pr.pay_line_id("c1", "2025", {"printed_title": "vd", "person_name": "anna"})
    assert a != pr.pay_line_id("c1", "2024", {"printed_title": "VD", "person_name": "Anna"})
