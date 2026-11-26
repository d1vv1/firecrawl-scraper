"""Prompts and answer models of the role-based pay extractor (pay_roles_prompts.py,
pay_roles_schema.py). No AI calls: only what is sent and what shape the answer must have."""

from types import SimpleNamespace

import pytest
from openai.lib._pydantic import to_strict_json_schema

from extractor import llm, pay_roles_prompts as pp, ref_roles
from extractor.pay_roles_schema import CORE_FIELDS, FIELDS, GapAnswer, answer_model
from tests.test_ref_roles import write

CHUNKS = [SimpleNamespace(id=1, text="Ersättning till VD|2025\nGrundlön|12 400"),
          SimpleNamespace(id=2, text="Styrelseordförande|1 200")]


@pytest.fixture()
def ref(tmp_path):
    return ref_roles.load(write(tmp_path / "ref_roles.xlsx"))


class TestSystemPrompt:
    def test_field_file_matches_the_schema(self):
        assert list(pp.field_sections()) == list(FIELDS)

    def test_field_mode_shows_only_the_fields_asked_for(self):
        s = pp.system_prompt("field", ["sti_paid", "base_salary"])
        assert "### base_salary" in s and "### sti_paid" in s
        assert "### pension" not in s and "### lti_vested" not in s
        assert s.index("### base_salary") < s.index("### sti_paid")      # schema order

    @pytest.mark.parametrize("mode", pp.MODES)
    def test_every_mode_has_base_and_its_own_part(self, mode):
        s = pp.system_prompt(mode, ["base_salary"])
        assert s.startswith(llm.load_prompt("pay_base_system").strip()[:60])
        assert llm.load_prompt(f"pay_mode_{mode}").strip() in s

    def test_board_pay_is_in_scope(self):
        base = llm.load_prompt("pay_base_system")
        assert "Executives AND the" in base and "board are both in scope" in base
        assert "leave all their pay fields null" not in base      # the old prompt's rule

    def test_role_lists_are_not_written_into_the_prompts(self):
        for name in ("pay_base_system", "pay_fields", "pay_mode_role", "pay_mode_all",
                     "pay_mode_field", "pay_mode_gapfill"):
            text = llm.load_prompt(name)
            assert "Toimitusjohtaja" not in text and "Bestyrelsesformand" not in text, name

    def test_fields_for(self):
        assert pp.fields_for("all") == CORE_FIELDS
        assert pp.fields_for("role") == CORE_FIELDS
        assert pp.fields_for("field", ["total", "base_salary"]) == ["base_salary", "total"]
        gaps = [pp.Gap("a1", "VD", "pension", 4, "empty"), pp.Gap("a1", "VD", "total", 4, "sum")]
        assert pp.fields_for("gapfill", gaps=gaps) == ["pension", "total"]
        with pytest.raises(ValueError):
            pp.fields_for("field")
        with pytest.raises(ValueError):
            pp.fields_for("field", ["bonus"])
        with pytest.raises(ValueError):
            pp.fields_for("guess")


class TestAnswerModels:
    def test_an_absent_field_is_null(self):
        line = answer_model(["base_salary", "total"]).model_fields["lines"].annotation.__args__[0]
        empty = {k: None for k in line.model_fields}
        empty.update(printed_title="CEO", is_aggregate=False, role_disclosure="individual",
                     period_coverage="full_year")
        assert line.model_validate(empty).base_salary is None

    def test_prompt_warns_about_damaged_tables(self):
        base = llm.load_prompt("pay_base_system")
        assert "How the text was made" in base and "cut into two tables" in base
        assert "never the\n  person's name" in base or "never the person's name" in base
        assert "as rows" in base                        # comparison year as rows

    def test_by_field_model_has_only_those_fields(self):
        line = answer_model(["base_salary"]).model_fields["lines"].annotation.__args__[0]
        assert "base_salary" in line.model_fields and "pension" not in line.model_fields
        assert "printed_title" in line.model_fields and "period_coverage" in line.model_fields

    @pytest.mark.parametrize("model", [answer_model(CORE_FIELDS), answer_model(["total"]),
                                       GapAnswer])
    def test_strict_structured_output_schema(self, model):
        schema = to_strict_json_schema(model)          # what llm.call_llm sends; raises if invalid
        assert schema["additionalProperties"] is False

    def test_every_field_says_where_it_goes(self):
        assert FIELDS["total"].columns == ("total_remuneration",)
        assert FIELDS["sti_target"].columns == ("sti_target_value", "sti_target_basis")
        assert FIELDS["pension_allowance"].columns == ()          # evidence file only


class TestUserMessage:
    def test_role_mode_lists_wanted_roles_in_the_report_languages(self, ref):
        msg = pp.user_message("role", company="Acme AB", source="SE_Acme.pdf",
                              what="the remuneration report", chunks=CHUNKS, ref=ref,
                              country="SE", selected=["ceo"])
        wanted = msg.split("Roles to extract:")[1].split("Not these roles")[0]
        assert "Verkställande direktör" in wanted and "Chief Executive Officer" in wanted
        assert "Toimitusjohtaja" not in wanted                      # Finnish, not for SE
        others = msg.split("Not these roles")[1].split("Roles to classify")[0]
        assert "Vice VD" in others                                  # looks like the CEO's VD
        assert '<chunk id="1">' in msg and "Country: SE" in msg

    def test_member_roles_take_in_their_whole_group(self, ref):
        # the required "Executive Committee Member (each)" is every executive: a CTO is wanted
        msg = pp.roles_block(ref, ["exco_member"], "SE")
        wanted = msg.split("Not these roles")[0]
        assert "- cto:" in wanted and "Wanted as one of: exco_member" in wanted
        assert "- coo:" in wanted                       # its own role code, same group
        assert "- board_chair" not in wanted            # other group
        assert pp.covered(ref, ["ceo"]) == {}           # a named role takes nobody else in

    def test_former_and_untitled_roles_are_described(self, ref, tmp_path):
        msg = pp.roles_block(ref, ["supervisory_board_member", "cto"], "SE")
        assert "Mitglied des Aufsichtsrats" not in msg.split("Not these")[0]   # German, not SE
        assert "(none listed" in msg

    def test_classify_list_and_cdp_roles(self, ref):
        msg = pp.user_message("all", company="Acme AB", source="x.pdf", what="the report",
                              chunks=CHUNKS, ref=ref, cdp_roles=[("R011", "Chief Strategy Officer")])
        assert "- cto: cto" in msg and "- R011: Chief Strategy Officer" in msg
        assert "Roles to extract" not in msg

    def test_role_mode_needs_roles(self, ref):
        with pytest.raises(ValueError):
            pp.user_message("role", company="A", source="s", what="w", chunks=CHUNKS, ref=ref)

    def test_gapfill_lists_the_cells(self, ref):
        msg = pp.user_message("gapfill", company="A", source="s", what="w", chunks=CHUNKS, ref=ref,
                              gaps=[pp.Gap("l7", "VD", "pension", 12, "empty")])
        assert "- line_ref l7 | VD | pension | page 12 | empty" in msg

    def test_request_key_changes_with_the_workbook_version(self):
        assert pp.request_key("s", "u", "v1") != pp.request_key("s", "u", "v2")
        assert pp.request_key("s", "u", "v1") == pp.request_key("s", "u", "v1")

    def test_langs(self):
        assert pp.langs_for("fi") == {"en", "fi", "sv"}
        assert pp.langs_for("GB") == {"en"}
        assert pp.langs_for(None) == {"en"}


def test_request_key_keeps_flash_keys_and_separates_other_models():
    from extractor import pay_roles_prompts as pp
    base = pp.request_key("s", "u", "v")
    assert pp.request_key("s", "u", "v", "google/gemini-2.5-flash") == base
    assert pp.request_key("s", "u", "v", "google/gemini-3.1-pro-preview") != base
