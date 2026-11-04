"""Industry code from the business description (docs/known_issues.md, issue 7).

Registers give an industry code only in the Nordics and the UK, and for a listed group
they code the parent company: Companies House gives Shell plc and AO World plc "70100
activities of head offices". The client's route: derive the sector from the business
description, which the report gives for nearly every company (97% in their review).

One small AI call picks a class from the taxonomy for the description (with the
segment names, if known); code checks that the code is in the list. The taxonomy is
NACE Rev. 2 (data/nace_rev2.tsv, Eurostat's list) until the client's own arrives: set
SECTOR_TAXONOMY to its file (tab- or comma-separated: code, optional level, name) and
SECTOR_SCHEME to the name written before each code.
"""

import csv
import hashlib
import json
import logging
import os
import re
from functools import lru_cache
from pathlib import Path

from . import llm
from .config import CACHE_DIR, PROJECT_ROOT
from .schemas import SectorPick

log = logging.getLogger(__name__)

TAXONOMY_FILE = Path(os.getenv("SECTOR_TAXONOMY") or PROJECT_ROOT / "data" / "nace_rev2.tsv")
SCHEME = os.getenv("SECTOR_SCHEME", "NACE")       # the value reads "NACE 47.91"
SCHEME_NAME = {"NACE": "NACE Rev. 2"}.get(SCHEME, SCHEME)
# Register codes for a company that only holds or manages the group (NACE 64.20 holding
# companies, 70.10 head offices; UK SIC 74990 non-trading, 99999 dormant; US SIC 6719).
PARENT_CODES = re.compile(r"^(6420|7010|74990|99999)")
US_PARENT_CODES = {"6719"}


@lru_cache(maxsize=1)
def taxonomy() -> dict[str, tuple[str, str]]:
    """code -> (level, name). Without a level column every code is a class."""
    text = TAXONOMY_FILE.read_text(encoding="utf-8-sig")
    rows = list(csv.reader(text.splitlines(), delimiter="\t" if "\t" in text else ","))
    head = [h.strip().lower() for h in rows[0]]
    at = {k: head.index(k) for k in ("code", "level", "name") if k in head}
    return {r[at["code"]].strip(): (r[at["level"]].strip() if "level" in at else "class",
                                    r[at["name"]].strip())
            for r in rows[1:] if r and r[at["code"]].strip()}


def classes() -> dict[str, str]:
    """The most detailed level: code -> name."""
    return {c: name for c, (level, name) in taxonomy().items() if level == "class"}


def system_prompt() -> str:
    lines = "\n".join(f"{c}\t{name}" for c, name in classes().items())
    return llm.load_prompt("sector_system").replace("{taxonomy}", lines)


def classify(name: str, description: str, segments: list[str]) -> SectorPick:
    """The AI's class for one description, cached by the inputs, prompt and taxonomy."""
    system = system_prompt()
    user = (f"Company: {name}\nWhat it does: {description}\n"
            + (f"Business segments: {'; '.join(segments)}\n" if segments else ""))
    key = hashlib.sha1((system + user).encode()).hexdigest()[:16]
    path = CACHE_DIR / f"sector_{key}.json"
    if path.exists():
        return SectorPick.model_validate(json.loads(path.read_text(encoding="utf-8"))["pick"])
    pick = llm.call_llm(system, user, SectorPick)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"user": user, "model": llm.model_name(), "pick": pick.model_dump()},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return pick


def register_codes(value: str) -> list[str]:
    """The code digits of a register value: "SIC (UK) 70100; 74990" -> ["70100", "74990"],
    "NACE 06.100" -> ["06100"]."""
    return [c.replace(".", "") for c in re.findall(r"\d[\d.]*\d", value)]


def describes_parent(value: str) -> bool:
    """Every code of the register value is a holding, head-office or non-trading code."""
    codes = register_codes(value)
    us = value.startswith("SIC ") and not value.startswith("SIC (UK)")
    return bool(codes) and all(c in US_PARENT_CODES if us else PARENT_CODES.match(c)
                               for c in codes)


def nace_class(digits: str) -> str:
    """"47910" or "4791" -> "47.91" (UK SIC 2007 and TOL 2008 add a fifth digit to NACE)."""
    return f"{digits[:2]}.{digits[2:4]}"


def register_note(register) -> str:
    """What the register's own code says next to the classification."""
    if register is None:
        return ""
    v = str(register.value)
    if describes_parent(v):
        return (f"register code {v} ({register.source}) describes the parent company, "
                f"not the business")
    return f"register code {v} ({register.source})"


def agrees(code: str, register) -> bool:
    """The register's code is the same NACE class (US SIC is another scheme)."""
    v = str(getattr(register, "value", "") or "")
    if SCHEME != "NACE" or not v or (v.startswith("SIC ") and not v.startswith("SIC (UK)")):
        return False
    return any(len(d) >= 4 and nace_class(d) == code for d in register_codes(v))


def segment_names(found) -> list[str]:
    """"Trucks: 319700; Buses: 23395" -> ["Trucks", "Buses"]. Names only: revenue
    misleads (an energy group's trading revenue dwarfs its production)."""
    if found is None:
        return []
    return [p.rsplit(":", 1)[0].strip() for p in str(found.value).split(";") if ":" in p][:8]


def from_description(chosen: dict, name: str):
    """The sector_code Found classified from the chosen sub_sector, or None (no
    description, or the AI found it too vague). Graded like the description it rests
    on; the register's own code is kept in the note."""
    from .apis import Found
    desc = chosen.get("sub_sector")
    if desc is None or not str(desc.value or "").strip():
        return None
    try:
        pick = classify(name, str(desc.value), segment_names(chosen.get("revenue_by_segment")))
    except Exception as e:  # noqa: BLE001 - the register code (if any) stays
        log.warning("Sector classification failed: %s", str(e)[:150])
        return None
    code = (pick.code or "").strip()
    if code not in classes():
        if code:
            log.warning("Sector classification gave %r, which is not a class of %s", code,
                        TAXONOMY_FILE.name)
        return None
    register = chosen.get("sector_code")
    reg = register_note(register)
    if register is not None and agrees(code, register):
        reg += ", the same class"
    basis = (pick.basis or "").strip()
    note = "; ".join(x for x in (
        f"derived: {SCHEME_NAME} class {code} ({classes()[code]}) from the business description"
        + (f' ("{basis}")' if basis else ""), reg) if x)
    return Found("sector_code", f"{SCHEME} {code}", source=desc.source, endpoint=desc.endpoint,
                 method="DERIVED", confidence=desc.confidence, note=note,
                 retrieved_at=desc.retrieved_at)
