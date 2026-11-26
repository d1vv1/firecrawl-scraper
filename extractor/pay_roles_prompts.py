"""The prompts of the role-based pay extractor (pay_roles.py), built per request.

The system prompt is the shared base (prompts/pay_base_system.md), the mode's own part
(prompts/pay_mode_<mode>.md) and the definitions of the pay fields asked for (sections of
prompts/pay_fields.md), so a by-field request never shows the AI a field nobody asked for.

The roles and their titles are never written into the .md files: they come from the role
workbook (ref_roles.py) into the user message, in the report's languages plus English. A
by-role request lists the wanted roles, then the other roles' titles that look like them
("Vice VD" when the CEO's "VD" is wanted), so the AI leaves those out.

Modes:
  field    every line, only the named fields
  role     only the named roles (e.g. the required ones), every core field
  all      every line, every core field
  gapfill  only listed cells of lines found before
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from pydantic import BaseModel

from . import llm
from .pay_roles_schema import CORE_FIELDS, FIELDS, GapAnswer, answer_model, check_fields
from .ref_roles import RefRoles, norm

MODES = ("field", "role", "all", "gapfill")

# The languages a country's reports are written in; English is always added.
LANGS_BY_COUNTRY = {
    "SE": {"sv"}, "NO": {"nb"}, "DK": {"da"}, "FI": {"fi", "sv"}, "IS": {"is"},
    "DE": {"de"}, "AT": {"de"}, "CH": {"de", "fr", "it"}, "LI": {"de"}, "LU": {"fr", "de"},
    "NL": {"nl"}, "BE": {"nl", "fr"}, "FR": {"fr"}, "IT": {"it"}, "ES": {"es"},
    "PT": {"pt"}, "GR": {"el"}, "CY": {"el"}, "GB": set(), "IE": set(),
}
OTHER_TITLES_PER_ROLE = 6       # "Not these roles": at most this many titles per other role

# A wanted "member" role takes every person of its group: the required "Executive Committee
# Member (each)" is every executive, so a COO or a CTO is wanted too, and "Non-executive
# Director (each)" is every board member, committee chairs included. The optional roles only
# name them more precisely. Cross-check lines (role_level X) are not people and stay out.
CATCH_ALL = {"other_executive": "executive", "board_member": "board"}


@dataclass(frozen=True)
class Gap:
    """One cell a gap-fill request asks about."""
    line_ref: str
    printed_title: str
    field: str
    page: int | None
    reason: str


def langs_for(country: str | None) -> set[str]:
    return {"en"} | LANGS_BY_COUNTRY.get((country or "").upper(), set())


def field_sections() -> dict[str, str]:
    """prompts/pay_fields.md, one text per field. Its headings must be exactly FIELDS."""
    text = re.sub(r"<!--.*?-->", "", llm.load_prompt("pay_fields"), flags=re.S)
    parts = re.split(r"^### +(\w+)\s*$", text, flags=re.M)
    sections = {name: body.strip() for name, body in zip(parts[1::2], parts[2::2])}
    if set(sections) != set(FIELDS):
        missing, extra = set(FIELDS) - set(sections), set(sections) - set(FIELDS)
        raise ValueError(f"prompts/pay_fields.md does not match FIELDS: missing "
                         f"{sorted(missing)}, unknown {sorted(extra)}")
    return sections


def fields_for(mode: str, fields: list[str] | None = None,
               gaps: list[Gap] | None = None) -> list[str]:
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; one of {', '.join(MODES)}")
    if mode == "field":
        if not fields:
            raise ValueError("mode 'field' needs the fields to ask for")
        return check_fields(fields)
    if mode == "gapfill":
        if not gaps:
            raise ValueError("mode 'gapfill' needs the cells to check")
        return check_fields(sorted({g.field for g in gaps}))
    return list(CORE_FIELDS)


def system_prompt(mode: str, fields: list[str]) -> str:
    sections = field_sections()
    body = "\n\n".join(f"### {f}\n{sections[f]}" for f in check_fields(fields))
    return "\n\n".join([llm.load_prompt("pay_base_system").strip(),
                        llm.load_prompt(f"pay_mode_{mode}").strip(),
                        "## Pay fields\n\n" + body]) + "\n"


def answer_schema(mode: str, fields: list[str]) -> type[BaseModel]:
    return GapAnswer if mode == "gapfill" else answer_model(fields)


# --- the user message --------------------------------------------------------------------

def _role_line(ref: RefRoles, detail: str, titles: list[str]) -> str:
    row = ref.details[detail]
    meaning = ref.roles.get(row["role_code"], {}).get("meaning", "")
    parts = [f"- {detail}: {row.get('label') or detail}"]
    if meaning:
        parts.append(f"  Meaning: {meaning}")
    if row.get("when_rule"):
        parts.append(f"  When: {row['when_rule']}")
    parts.append("  Titles: " + ("; ".join(titles) if titles else
                                 "(none listed: recognise it by its label and meaning)"))
    return "\n".join(parts)


def covered(ref: RefRoles, selected: list[str]) -> dict[str, str]:
    """Roles not asked for by name that a wanted member role takes in (see CATCH_ALL):
    role_detail -> the wanted role_detail it is counted under."""
    out: dict[str, str] = {}
    for d in selected:
        group = CATCH_ALL.get(ref.details[d]["role_code"])
        if not group:
            continue
        for other, row in ref.details.items():
            role = ref.roles.get(row["role_code"], {})
            if (other not in selected and other not in out and role.get("role_group") == group
                    and role.get("role_level") != "X"):
                out[other] = d
    return out


def roles_block(ref: RefRoles, selected: list[str], country: str | None) -> str:
    """"Roles to extract" and "Not these roles" for a by-role request."""
    langs = langs_for(country)
    under = covered(ref, selected)
    selected = list(selected) + list(under)
    wanted = ref.titles_for(selected, langs)
    out = ["Roles to extract:"]
    for d in selected:
        line = _role_line(ref, d, wanted[d])
        if d in under:
            line += f"\n  Wanted as one of: {under[d]}"
        out.append(line)
    # other roles whose titles look like a wanted one: always listed, whatever the cap
    keys = [norm(t) for d in selected for t in wanted[d]]
    others = [d for d in ref.details if d not in selected]
    other_titles = ref.titles_for(others, langs)
    lines = []
    for d in others:
        alike = [t for t in other_titles[d]
                 if any(re.search(r"(?<!\w)" + re.escape(k) + r"(?!\w)", norm(t)) for k in keys)]
        rest = [t for t in other_titles[d] if t not in alike]
        shown = alike + rest[:max(0, OTHER_TITLES_PER_ROLE - len(alike))]
        if shown:
            lines.append(f"- {d}: " + "; ".join(shown))
    if lines:
        out += ["", "Not these roles (leave their lines out):"] + lines
    return "\n".join(out)


def classify_block(ref: RefRoles, cdp_roles: list[tuple[str, str]] | None = None) -> str:
    """The role_details a line can be suggested as, and the CDP roles for lines none fits."""
    out = ["Roles to classify lines into (role_detail: label):"]
    out += [f"- {d}: {row.get('label') or d}" for d, row in ref.details.items()]
    if cdp_roles:
        out += ["", "CDP roles, only for a line none of the roles above fits (id: title):"]
        out += [f"- {i}: {t}" for i, t in cdp_roles]
    return "\n".join(out)


def gaps_block(gaps: list[Gap]) -> str:
    out = ["Cells to check:"]
    for g in gaps:
        page = f"page {g.page}" if g.page else "page unknown"
        out.append(f"- line_ref {g.line_ref} | {g.printed_title} | {g.field} | {page} | {g.reason}")
    return "\n".join(out)


def chunks_block(chunks) -> str:
    return "\n\n".join(f'<chunk id="{c.id}">\n{c.text.strip()}\n</chunk>' for c in chunks)


def user_message(mode: str, *, company: str, source: str, what: str, chunks, ref: RefRoles,
                 country: str | None = None, selected: list[str] | None = None,
                 cdp_roles: list[tuple[str, str]] | None = None,
                 gaps: list[Gap] | None = None) -> str:
    head = [f"Company legal name: {company}"]
    if country:
        head.append(f"Country: {country.upper()}")
    head.append(f"Source: {source}")
    blocks = ["\n".join(head)]
    if mode == "role":
        if not selected:
            raise ValueError("mode 'role' needs the roles to extract")
        blocks.append(roles_block(ref, selected, country))
    if mode == "gapfill":
        blocks.append(gaps_block(gaps or []))
    blocks.append(classify_block(ref, cdp_roles))
    blocks.append(f"Excerpts from {what} (tables are in markdown):\n\n{chunks_block(chunks)}")
    return "\n\n".join(blocks)


DEFAULT_MODEL = "google/gemini-2.5-flash"


def request_key(system: str, user: str, ref_version: str, model: str | None = None) -> str:
    """The cache key of one AI request: the prompt, the message (which holds the chunks and
    the role lists), the role workbook's version and, for a model other than the default,
    the model (a pro run must not reuse a flash answer; flash keys stay as they were)."""
    h = hashlib.sha1()
    parts = (system, user, ref_version) + ((model,) if model and model != DEFAULT_MODEL else ())
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:20]
