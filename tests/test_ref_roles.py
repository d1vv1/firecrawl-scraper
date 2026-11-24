"""The role workbook and title mapper (extractor/ref_roles.py). Runs on small workbooks
written here; the last class checks the real ref_roles.xlsx when it is there (skipped
otherwise)."""

import openpyxl
import pytest

from extractor import ref_roles
from extractor.ref_roles import RefRolesError, norm

ROLES = [("ceo", "Y"), ("deputy_ceo", "Y"), ("cfo", "Y"), ("coo", "N"), ("other_executive", "N"),
         ("board_chair", "Y"), ("board_vice_chair", "Y"), ("board_member", "Y")]
DETAILS = [  # role_detail, required, role_code, cdp_role_id
    ("ceo", "Y", "ceo", "R001"), ("deputy_ceo", "Y", "deputy_ceo", "R327"), ("cfo", "Y", "cfo", "R002"),
    ("coo", "N", "coo", "R004"), ("exco_member", "Y", "other_executive", "R338"),
    ("cto", "N", "other_executive", "R003"), ("board_chair", "Y", "board_chair", ""),
    ("board_vice_chair", "Y", "board_vice_chair", ""), ("non_executive_director", "Y", "board_member", ""),
    ("supervisory_board_member", "Y", "board_member", "")]
TITLES = [  # role_detail, title, lang, match, status, country
    ("ceo", "CEO", "en", "abbrev", "agreed", ""),
    ("ceo", "Chief Executive Officer", "en", "phrase", "agreed", ""),
    ("ceo", "Group Chief Executive Officer", "en", "phrase", "agreed", ""),
    ("ceo", "VD", "sv", "abbrev", "agreed", "SE"),
    ("ceo", "Verkställande direktör", "sv", "phrase", "agreed", ""),
    ("ceo", "Toimitusjohtaja", "fi", "phrase", "agreed", ""),
    ("ceo", "Administrerende direktør", "da", "phrase", "agreed", ""),
    ("ceo", "Διευθύνων Σύμβουλος", "el", "phrase", "agreed", ""),
    ("deputy_ceo", "Vice VD", "sv", "phrase", "agreed", ""),
    ("deputy_ceo", "Deputy CEO", "en", "phrase", "agreed", ""),
    ("cfo", "CFO", "en", "abbrev", "agreed", ""),
    ("cfo", "Finanzvorstand", "de", "phrase", "proposed", ""),
    ("coo", "COO", "en", "abbrev", "agreed", ""),
    ("exco_member", "Member of the Management Board", "en", "phrase", "agreed", ""),
    ("cto", "Chief Technology Officer", "en", "phrase", "agreed", ""),
    ("board_chair", "Chairman", "en", "phrase", "agreed", ""),
    ("board_chair", "Chairman of the Board", "en", "phrase", "agreed", ""),
    ("board_chair", "Styrelseordförande", "sv", "phrase", "agreed", ""),
    ("board_vice_chair", "Vice Chairman", "en", "phrase", "agreed", ""),
    ("non_executive_director", "Board member", "en", "phrase", "agreed", ""),
    ("supervisory_board_member", "Mitglied des Aufsichtsrats", "de", "phrase", "agreed", ""),
]
EXCLUSIONS = [("Former", "en", "part_year"), ("Tidigare", "sv", "part_year"),
              ("Ehemalige", "de", "part_year"), ("Acting", "en", "flag"), ("Tf.", "sv", "flag")]


def write(path, roles=ROLES, details=DETAILS, titles=TITLES, exclusions=EXCLUSIONS, version=True):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "roles"
    ws.append(["code", "label", "role_level", "role_group", "meaning", "is_ceo", "sort_order",
               "required", "active"])
    for code, req in roles:
        ws.append([code, code, "E1", "board" if code.startswith("board") else "executive",
                   "", "N", 1, req, "Y"])
    ws = wb.create_sheet("role_details")
    ws.append(["role_detail", "label", "group", "required", "when_rule", "role_code", "cdp_role_id",
               "cdp_role_title", "note"])
    for d, req, code, cdp in details:
        ws.append([d, d, "", req, "", code, cdp, "", ""])
    ws = wb.create_sheet("titles")
    ws.append(["role_detail", "role_code", "title", "lang", "country", "match", "status", "note"])
    for d, title, lang, match, status, country in titles:
        ws.append([d, None, title, lang, country, match, status, None])
    ws = wb.create_sheet("exclusions")
    ws.append(["phrase", "lang", "effect", "note"])
    for row in exclusions:
        ws.append(list(row) + [None])
    for name, codes in (("disclosure", ["individual", "aggregate"]),
                        ("period_coverage", ["full_year", "left_in_year"])):
        ws = wb.create_sheet(name)
        ws.append(["code", "label", "meaning", "status", "list_source"])
        for c in codes:
            ws.append([c, c, "", "In use", ""])
    ws = wb.create_sheet("version")
    ws.append(["version", "date", "agreed_by"])
    if version:
        ws.append(["0.1-test", "2026-11-24", ""])
    wb.save(path)
    return path


@pytest.fixture()
def ref(tmp_path):
    return ref_roles.load(write(tmp_path / "ref_roles.xlsx"))


def code(ref, text, country=None):
    m = ref.match(text, country)
    return m.role_detail if m else None


class TestMatch:
    def test_longer_title_wins(self, ref):
        assert code(ref, "Vice VD") == "deputy_ceo"
        assert code(ref, "Deputy CEO") == "deputy_ceo"
        assert ref.match("Group Chief Executive Officer").title == "Group Chief Executive Officer"
        assert ref.match("Chairman of the Board").title == "Chairman of the Board"

    def test_first_title_wins_when_they_overlap(self, ref):
        # "Vice Chairman" and "Chairman of the Board" overlap; the one that starts first wins
        assert code(ref, "Vice Chairman of the Board") == "board_vice_chair"

    def test_abbreviations_are_whole_words_in_capitals(self, ref):
        assert code(ref, "Cooperation manager") is None
        assert code(ref, "COO") == "coo"
        assert code(ref, "Group COO") == "coo"
        assert code(ref, "Ceo") is None                  # not the abbreviation
        assert code(ref, "VDAX index") is None

    def test_case_accents_and_punctuation_ignored(self, ref):
        assert code(ref, "VERKSTALLANDE direktör") == "ceo"
        assert code(ref, "verkställande-direktör") == "ceo"
        assert code(ref, "Administrerende Direktør") == "ceo"   # ø kept, case ignored
        assert code(ref, "ΔΙΕΥΘΎΝΩΝ ΣΎΜΒΟΥΛΟΣ") == "ceo"        # Greek, tonos ignored

    def test_country_bound_title(self, ref):
        assert code(ref, "VD", "SE") == "ceo"
        assert code(ref, "VD", "DE") is None
        assert code(ref, "VD") == "ceo"                  # no country given: allowed

    def test_word_boundaries(self, ref):
        assert code(ref, "Chairmanship committee") is None
        assert code(ref, "Mitglied des Aufsichtsratsausschusses") is None

    def test_former_is_part_year_and_still_matched(self, ref):
        m = ref.match("Former CEO (until April 2025)")
        assert (m.role_detail, m.part_year, m.exclusions) == ("ceo", True, ["Former"])
        m = ref.match("Tidigare verkställande direktör")
        assert (m.role_detail, m.part_year) == ("ceo", True)
        m = ref.match("Ehemalige Mitglied des Aufsichtsrats")
        assert (m.role_detail, m.part_year) == ("supervisory_board_member", True)

    def test_acting_is_flagged_not_part_year(self, ref):
        m = ref.match("Acting CFO")
        assert (m.role_detail, m.part_year, m.flags) == ("cfo", False, ["acting"])
        assert ref.match("Tf. VD").flags == ["tf"]

    def test_brackets_only_when_the_rest_has_nothing(self, ref):
        assert code(ref, "CFO (Chairman of the Board from June)") == "cfo"
        assert code(ref, "Jane Doe (CFO)") == "cfo"

    def test_confidence_and_cdp_id(self, ref):
        m = ref.match("Chief Executive Officer")
        assert (m.confidence, m.source, m.cdp_role_id, m.role_code) == ("high", "auto", "R001", "ceo")
        assert ref.match("Finanzvorstand").confidence == "medium"        # proposed title
        assert ref.match("Chief Technology Officer").role_code == "other_executive"

    def test_no_match(self, ref):
        assert ref.match("Head of Investor Relations") is None
        assert ref.match("") is None
        assert ref.match("   ") is None


class TestLists:
    def test_required_optional_select(self, ref):
        assert "coo" in ref.optional() and "cto" in ref.optional()
        assert "ceo" in ref.required() and "coo" not in ref.required()
        assert ref.select("required") == ref.required()
        assert ref.select("ceo,board_member") == ["ceo", "non_executive_director",
                                                  "supervisory_board_member"]
        with pytest.raises(RefRolesError):
            ref.select("chief_wizard")

    def test_titles_for(self, ref):
        got = ref.titles_for(["ceo"], {"sv", "en"})
        assert "Verkställande direktör" in got["ceo"] and "Toimitusjohtaja" not in got["ceo"]

    def test_version_has_file_hash(self, ref):
        label, digest = ref.version.split("+")
        assert label == "0.1-test" and len(digest) == 8


class TestValidation:
    def problems(self, tmp_path, **kw):
        with pytest.raises(RefRolesError) as e:
            ref_roles.load(write(tmp_path / "bad.xlsx", **kw))
        return str(e.value)

    def test_title_under_two_roles(self, tmp_path):
        msg = self.problems(tmp_path, titles=TITLES + [("cfo", "chief executive officer", "en",
                                                        "phrase", "agreed", "")])
        assert "same title as 'Chief Executive Officer' under ceo" in msg

    def test_unknown_language_match_status(self, tmp_path):
        msg = self.problems(tmp_path, titles=[("ceo", "CEO", "xx", "regex", "maybe", "")])
        assert "lang 'xx'" in msg and "match 'regex'" in msg and "status 'maybe'" in msg

    def test_blank_title_and_unknown_detail(self, tmp_path):
        msg = self.problems(tmp_path, titles=[("ceo", "", "en", "phrase", "agreed", ""),
                                              ("chief_wizard", "Wizard", "en", "phrase", "agreed", "")])
        assert "blank title" in msg and "unknown role_detail 'chief_wizard'" in msg

    def test_unknown_role_code_and_bad_required(self, tmp_path):
        msg = self.problems(tmp_path, details=DETAILS + [("x", "maybe", "nope", "")])
        assert "unknown role_code 'nope'" in msg and "required must be Y or N" in msg

    def test_bad_exclusion_effect(self, tmp_path):
        msg = self.problems(tmp_path, exclusions=[("Former", "en", "drop")])
        assert "effect 'drop'" in msg

    def test_every_problem_is_listed(self, tmp_path):
        msg = self.problems(tmp_path, titles=[("ceo", "", "en", "phrase", "agreed", ""),
                                              ("ceo", "CEO", "xx", "phrase", "agreed", "")])
        assert "2 problem(s)" in msg

    def test_missing_file(self, tmp_path):
        with pytest.raises(RefRolesError, match="no role workbook"):
            ref_roles.load(tmp_path / "none.xlsx")


def test_norm():
    assert norm("  Vorsitzender des Aufsichtsrats ") == "vorsitzender des aufsichtsrats"
    assert norm("Président-directeur général") == "president directeur general"
    assert norm("Adm. direktør") == "adm direktør"


@pytest.fixture(scope="module")
def real():
    return ref_roles.load(ref_roles.DEFAULT_XLSX)


@pytest.mark.skipif(not ref_roles.DEFAULT_XLSX.is_file(), reason="real ref_roles.xlsx not found")
class TestRealWorkbook:
    def test_every_title_maps_to_its_own_role(self, real):
        wrong = []
        for t in real.titles:
            m = real.match(t.title, t.country or None)
            if not m or m.role_detail != t.role_detail:
                wrong.append(f"{t.title!r}: {t.role_detail} -> {m and m.role_detail}")
        assert not wrong, "\n".join(wrong)

    def test_one_title_per_language(self, real):
        by_lang = {}
        for t in real.titles:
            by_lang.setdefault(t.lang, t)
        for lang, t in by_lang.items():
            assert real.match(t.title, t.country or None).role_detail == t.role_detail, lang

    @pytest.mark.parametrize("printed, detail, part_year", [
        ("Verkställande direktör och koncernchef", "ceo", False),
        ("Tidigare VD (till och med 31 mars 2025)", "ceo", True),
        ("Styrelseordförande", "board_chair", False),
        ("Vice styrelseordförande", "board_vice_chair", False),
        ("Arbetstagarrepresentant", "employee_representative", False),
        ("Övriga ledande befattningshavare (7 personer)", "executive_management_group", False),
        ("Konsernsjef", "ceo", False),
        ("Styreleder", "board_chair", False),
        ("Hallituksen puheenjohtaja", "board_chair", False),
        ("Bestyrelsesformand", "board_chair", False),
        ("Former Chief Financial Officer", "cfo", True),
    ])
    def test_nordic_titles(self, real, printed, detail, part_year):
        m = real.match(printed)
        assert m and (m.role_detail, m.part_year) == (detail, part_year)
