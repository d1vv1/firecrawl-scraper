"""Industry code from the business description (extractor/sector.py, issue 7)."""

from extractor import sector
from extractor.apis import Found
from extractor.schemas import SectorPick


def test_the_nace_list_is_complete():
    levels = [level for level, _ in sector.taxonomy().values()]
    assert (levels.count("section"), levels.count("division"), levels.count("group"),
            levels.count("class")) == (21, 88, 272, 615)       # NACE Rev. 2
    assert sector.classes()["70.10"] == "Activities of head offices"


def test_register_codes_that_describe_the_parent():
    assert sector.describes_parent("SIC (UK) 70100")
    assert sector.describes_parent("SIC (UK) 70100; 74990")         # AO World
    assert sector.describes_parent("TOL/NACE 70100")                # Nokia
    assert not sector.describes_parent("SIC (UK) 70100; 47910")     # also a trading code
    assert not sector.describes_parent("NACE 06.100")
    assert sector.describes_parent("SIC 6719") and not sector.describes_parent("SIC 7010")


def test_register_agreement_is_by_nace_class():
    assert sector.nace_class("47910") == "47.91"
    assert sector.agrees("06.10", Found("sector_code", "NACE 06.100"))
    assert sector.agrees("47.71", Found("sector_code", "TOL/NACE 47712"))
    assert not sector.agrees("47.71", Found("sector_code", "SIC 5651"))   # US SIC: another scheme


def _chosen(**extra):
    d = {"sub_sector": Found("sub_sector", "Shell is an international energy company",
                             source="ESEF filing", endpoint="https://f", method="PARSE",
                             confidence="B"),
         "sector_code": Found("sector_code", "SIC (UK) 70100", source="Companies House",
                              method="API", confidence="A")}
    return d | extra


def test_classified_from_the_description(monkeypatch):
    seen = {}

    def fake(name, description, segments):
        seen.update(name=name, segments=segments)
        return SectorPick(code="06.10", basis="international energy company")
    monkeypatch.setattr(sector, "classify", fake)
    segs = Found("revenue_by_segment", "Integrated Gas: 38457; Upstream: 5105")
    f = sector.from_description(_chosen(revenue_by_segment=segs), "Shell PLC")
    assert f.value == "NACE 06.10" and f.method == "DERIVED" and f.confidence == "B"
    assert f.source == "ESEF filing" and f.endpoint == "https://f"
    assert f.note.startswith("derived: NACE Rev. 2 class 06.10 (Extraction of crude petroleum)")
    assert "SIC (UK) 70100 (Companies House) describes the parent company" in f.note
    assert seen["segments"] == ["Integrated Gas", "Upstream"]       # names only, no revenue


def test_no_class_when_vague_or_not_in_the_list(monkeypatch):
    monkeypatch.setattr(sector, "classify", lambda *a: SectorPick(code=None, basis=""))
    assert sector.from_description(_chosen(), "X") is None
    monkeypatch.setattr(sector, "classify", lambda *a: SectorPick(code="99.99", basis="x"))
    assert sector.from_description(_chosen(), "X") is None           # not a NACE class
    assert sector.from_description({}, "X") is None                  # no description


def test_section_name_is_the_nace_section_of_a_sector_code():
    from extractor import sector
    assert sector.section_name("NACE 28.99") == "Manufacturing"
    assert sector.section_name("NACE 64.20") == "Financial and insurance activities"
    assert sector.section_name("TOL/NACE 46900").startswith("Wholesale and retail trade")
    assert sector.section_name("SIC (UK) 70100") == ""     # another scheme
    assert sector.section_name("") == ""


def test_segment_is_the_industry_and_the_input_tier_moves_to_tier():
    from extractor.datapoints import segment_from_sector
    old = [{"grain": "company", "data_point": "sector_code", "value": "NACE 41.10", "segment": "Tier 2"},
           {"grain": "role", "data_point": "base_salary", "value": "1", "segment": "Tier 2"}]
    segment_from_sector(old)
    assert [(r["segment"], r["tier"]) for r in old] == [("Construction", "Tier 2")] * 2
    segment_from_sector(old)                                # saved again: unchanged
    assert [(r["segment"], r["tier"]) for r in old] == [("Construction", "Tier 2")] * 2
    new = [{"grain": "company", "data_point": "sector_code", "value": "", "segment": "", "tier": "Tier 1"}]
    segment_from_sector(new)
    assert (new[0]["segment"], new[0]["tier"]) == ("", "Tier 1")
