"""The pay tables of a report read with Camelot (the old route, pay_tables.py), to check and
correct the figures the role-based pay extractor's AI call read (pay_roles.py).

The AI reads the report as markdown, whose tables the PDF conversion can damage (wrapped row
labels, tables cut in two, merged columns). Camelot reads a table by the position of its
columns instead. Per company:
  1. READ   the pay-table pages (pay.table_pages, plus the pages the AI's figures came from)
            with Camelot (pay_tables.read_grids). No AI.
  2. MAP    one small cached AI call per grid gives row and column numbers, never figures:
            executive tables with the old route's own call (pay_tables.map_columns,
            prompts/pay_columns_system.md, unchanged); a grid that is not an executive table
            goes to the board-table call (prompts/pay_columns_board_system.md).
  3. MATCH  each mapped row to one line of the AI's answer: same person, else same title,
            else the same base salary or board fee.
  4. CHECK  field by field, for fields that are ONE table column (decided 25 Nov 2026):
              agree           the AI read the same printed figure;
              table_replaced  they differ, the row's parts add up to its total and the
                              AI's quote is NOT found in the text: the table's figure is
                              used, verbatim, and the AI's kept as "previous";
              table_differs   they differ but the AI's quote is found: the AI's figure
                              stays and the table's goes to the review file (Southern
                              Europe prints several tables per person);
              table_blank     the table has "-" or 0 where the AI read a figure: the AI's
                              figure stays;
              (the same printed figure read with another separator counts as agree)
              table_added     the AI has no figure and the table has one (row adds up);
              ai_consistent   they differ, but the AI's own line adds up to the same total
                              (a table split another way, Stora Enso's cash and shares):
                              the AI's figure stays;
              in_other_field  the AI has the table's figure under another field: not added
                              twice;
              table_not_used  the table row's parts don't reach its total (read or mapped
                              wrong): it can't judge the AI, whose figure stays;
              multi_column    the field is several columns (committee fees per committee,
                              bonus cash + deferred): never added up, the AI's figure stays.
Lines no table row matches keep the AI's reading. Nothing changes without a PDF or Camelot.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from . import llm, pay, pay_tables
from .config import CACHE_DIR
from .schemas import MappedRow, Unit

log = logging.getLogger(__name__)

MAX_PAGES = 8
TOLERANCE = pay_tables.TOTAL_TOLERANCE
# old route's executive fields -> pay_roles fields
EXEC_FIELDS = {"base_salary": "base_salary", "sti_paid": "sti_paid", "lti_vested": "lti_vested",
               "lti_granted": "lti_granted", "benefits": "benefits", "pension": "pension",
               "pension_allowance": "pension_allowance", "other_in_total": "other_pay"}
BOARD_FIELDS = {"board_fee": "base_salary", "committee_fees": "committee_fees",
                "meeting_fees": "meeting_fees", "pension": "pension", "other_pay": "other_pay"}


class BoardColumnMap(BaseModel):
    """Which rows and columns of a board fee table make up which field. No defaults:
    structured outputs in strict mode need every field."""
    is_board_table: bool
    year: Optional[str]
    unit: Optional[Unit]
    currency: Optional[str]
    rows: list[MappedRow]
    board_fee: list[int]
    committee_fees: list[int]
    meeting_fees: list[int]
    pension: list[int]
    other_pay: list[int]
    total: Optional[int]


@dataclass
class TableRow:
    kind: str                         # executive | board
    label: str
    page: int
    cells: dict[str, list[str]]       # pay_roles field -> the printed cells of its columns
    total: str | None                 # the printed total cell
    adds_up: bool
    unit: str | None = None
    currency: str | None = None
    used: bool = field(default=False, compare=False)


def map_board(grid: pay_tables.Grid, name: str, page_text: str = "") -> BoardColumnMap:
    """The board mapping call, cached like pay_tables.map_columns."""
    prompt = llm.load_prompt("pay_columns_board_system")
    text = grid.text()
    page = page_text[:pay_tables.PAGE_CHARS]
    key = hashlib.sha1(f"{prompt}\n{text}\n{page}".encode()).hexdigest()[:16]
    path = CACHE_DIR / f"boardtable_{key}.json"
    if path.exists():
        return BoardColumnMap.model_validate(json.loads(path.read_text(encoding="utf-8"))["map"])
    user = (f"Company: {name}\n\nPDF page {grid.page} as text, for the table's caption, year "
            f"and unit (its tables may be garbled here):\n\n{page}\n\nThe table, by row and "
            f"column number:\n\n{text}")
    m = llm.call_llm(prompt, user, BoardColumnMap)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"page": grid.page, "grid": text, "model": llm.model_name(),
                                "map": m.model_dump()}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    return m


def _year_ok(map_year: str | None, fiscal_year: str | None) -> bool:
    from .datapoints import fiscal_end_year
    want, got = fiscal_end_year(fiscal_year), fiscal_end_year(map_year)
    return not (want and got and want != got)


def _rows(grid: pay_tables.Grid, m, fields: dict[str, str], kind: str) -> list[TableRow]:
    width = grid.width()
    cols_used = [c for f in fields for c in getattr(m, f)] + ([m.total] if m.total is not None else [])
    if len(cols_used) != len(set(cols_used)) or any(not 0 <= c < width for c in cols_used):
        log.info("Pay tables: %s table on page %d not used: columns overlap or out of range",
                 kind, grid.page)
        return []
    out = []
    for r in m.rows:
        if not 0 <= r.row < len(grid.cells):
            continue
        row = grid.cells[r.row] + [""] * (width - len(grid.cells[r.row]))
        cells = {fields[f]: [row[c] for c in getattr(m, f)] for f in fields if getattr(m, f)}
        total = row[m.total] if m.total is not None else None
        out.append(TableRow(kind, r.label, grid.page, cells, total,
                            _adds_up(cells, total, kind), m.unit, m.currency))
    return out


def _adds_up(cells: dict[str, list[str]], total: str | None, kind: str) -> bool:
    t = pay_tables.parse_figure(total or "")
    if t is None:
        return False
    values = {f: sum(pay_tables.parse_figure(c) or 0 for c in cs) for f, cs in cells.items()}
    if kind == "executive":
        other = [values.pop("other_pay")] if "other_pay" in values else []
        return pay_tables.adds_up(values, t, other)
    s = sum(values.values())
    return abs(s - t) <= TOLERANCE * abs(t) or (t == 0 and s == 0)


def read_rows(name: str, fiscal_year: str | None, pdf: Path, pages: list[int],
              page_text: dict[int, str]) -> list[TableRow]:
    """Every mapped executive and board row of these pages' tables, for the pay year."""
    out: list[TableRow] = []
    for grid in pay_tables.read_grids(Path(pdf), pages):
        text = page_text.get(grid.page, "")
        try:
            m = pay_tables.map_columns(grid, name, text)
            if m.is_pay_table and m.rows:
                if _year_ok(m.year, fiscal_year):
                    out += _rows(grid, m, EXEC_FIELDS, "executive")
                continue
            b = map_board(grid, name, text)
        except Exception as e:  # noqa: BLE001 - a failed mapping keeps the AI's reading
            log.warning("Pay tables: mapping page %d failed: %s", grid.page, str(e)[:150])
            continue
        if b.is_board_table and b.rows and _year_ok(b.year, fiscal_year):
            out += _rows(grid, b, BOARD_FIELDS, "board")
    return out


def _words(text: str | None) -> set[str]:
    return {w for w in re.findall(r"[^\W\d_]+", (text or "").casefold()) if len(w) > 1}


def match(line: dict, rows: list[TableRow]) -> TableRow | None:
    """The unused table row of one AI line. A line with a person's name is matched by that
    name only: board members often have the same fee, so a fee or a shared title would pick
    another person (in the Nordic pilot, Janne Moltke-Leth's line took Gitte Poulsen's row).
    A line without a name: the same title, else (executive tables only) the same base
    salary as printed."""
    free = [r for r in rows if not r.used]

    def only(found):
        return found[0] if len(found) == 1 else None
    name = _words(line.get("person_name"))
    if name:
        return only([r for r in free if name <= _words(r.label)])
    for text in (line.get("row_label"), line.get("printed_title")):
        words = _words(text)
        if words and (got := only([r for r in free if _words(r.label) == words])):
            return got
    base = (line.get("base_salary") or {}).get("value") if isinstance(line.get("base_salary"), dict) else None
    if base is not None:
        return only([r for r in free if r.kind == "executive"
                     and len(r.cells.get("base_salary", [])) == 1
                     and pay_tables.parse_figure(r.cells["base_salary"][0]) == base])
    return None


def _digits(text: str | None) -> str:
    return re.sub(r"\D", "", text or "")


def _same(a: float | None, b: float | None) -> bool:
    return a is not None and b is not None and abs(a - b) <= 1e-6 * max(1.0, abs(a))


def _consistent(line: dict, table_total: float | None) -> bool:
    """The AI's parts add up to its total, and that total is the table row's."""
    from .pay_roles_output import TOTAL_PARTS
    total = line.get("total") if isinstance(line.get("total"), dict) else None
    if not total or total.get("value") is None or table_total is None:
        return False
    if not _same(total["value"], table_total):
        return False
    parts = [line[f]["value"] for f in TOTAL_PARTS
             if isinstance(line.get(f), dict) and line[f].get("value") is not None]
    if not parts:
        return False
    base = sum(parts)
    ltis = [0.0] + [line[f]["value"] for f in ("lti_vested", "lti_granted")
                    if isinstance(line.get(f), dict) and line[f].get("value") is not None]
    t = total["value"]
    return any(abs(base + x - t) <= max(1.0, TOLERANCE * abs(t)) for x in ltis)


def compare(item: dict, row: TableRow, page_text: str) -> dict[str, str]:
    """Check one AI line against its table row, changing the line as the rules say.
    Returns field -> status."""
    line = item["line"]
    status: dict[str, str] = {}
    fields = dict(row.cells)
    if row.total is not None:
        fields["total"] = [row.total]
    existing = [c for c in line.values() if isinstance(c, dict) and c.get("value") is not None]
    unit_printed = next((c.get("unit_printed") for c in existing if c.get("unit_printed")), None)
    currency = next((c.get("currency_printed") for c in existing if c.get("currency_printed")),
                    row.currency)
    # the AI's own line already adds up to the table's total: its reading is consistent, so
    # a table that splits the pay another way (Stora Enso: cash and shares, not fee and
    # committee) does not overrule it
    consistent = _consistent(line, pay_tables.parse_figure(row.total or ""))
    quotes = item.get("quote_check") or {}
    item.pop("table_figures", None)
    for f, cells in fields.items():
        if len(cells) != 1:
            status[f] = "multi_column"
            continue
        printed = cells[0]
        tv = pay_tables.parse_figure(printed)
        old = line.get(f) if isinstance(line.get(f), dict) else None
        ai = old.get("value") if old else None
        if tv is None:
            continue
        if ai is None and tv == 0:
            continue                                  # "-" in the table, nothing read: agree
        if _same(ai, tv):
            status[f] = "agree"
            continue
        if ai is not None and _digits((old or {}).get("printed")) == _digits(printed) != "":
            # the same printed figure read with another separator (Italian "228.000"): agree
            status[f] = "agree"
            continue
        if ai not in (None, 0) and tv == 0:
            # "-" or 0 in the table where the AI read a figure (National Bank of Greece): a
            # blank cell never overwrites a figure
            status[f] = "table_blank"
            continue
        if not row.adds_up:
            # a row whose mapped parts don't reach its total was read or mapped wrong (ISS:
            # the clean "1,437 + 719 + 76 = 2,232" row mapped to other columns): it can't
            # judge the AI, so it is noted and not used
            if ai is not None:
                status[f] = "table_not_used"
            continue
        if consistent:
            status[f] = "ai_consistent"
            continue
        if ai is not None and quotes.get(f) in ("exact", "close"):
            # the AI's figure is in the text: reports print several tables per person (Italian
            # Tabella 1 and 3B, the Spanish CNMV tables), so a different figure in another
            # table is a disagreement to review, not a correction (decided 25 Nov 2026)
            status[f] = "table_differs"
            item.setdefault("table_figures", {})[f] = printed
            continue
        if ai is None and any(_same(c.get("value"), tv) for k, c in line.items()
                              if k != f and isinstance(c, dict)):
            # the AI has this figure under another field (Metsä's TyEL pension, mapped by
            # the table as "other"): adding it here would count it twice
            status[f] = "in_other_field"
            continue
        new = {k: (old or {}).get(k) for k in ("unit", "includes", "form")}
        new.update(value=tv, printed=printed,
                   unit_printed=(old or {}).get("unit_printed") or unit_printed,
                   unit=(old or {}).get("unit") or row.unit,
                   currency_printed=(old or {}).get("currency_printed") or currency,
                   quote=pay_tables.row_quote(row.label, [printed], page_text),
                   chunk_id=(old or {}).get("chunk_id"),
                   previous=({k: old.get(k) for k in ("value", "printed", "quote")} if old
                             else None),
                   table_note=f"Camelot, PDF page {row.page}, row '{row.label[:60]}'")
        line[f] = {k: v for k, v in new.items() if k != "form" or "form" in (old or {})}
        status[f] = "table_replaced" if ai is not None else "table_added"
    item["table_check"] = status
    item["table_row"] = {"kind": row.kind, "page": row.page, "label": row.label,
                         "adds_up": row.adds_up}
    return status


def check_lines(name: str, fiscal_year: str | None, lines: list[dict], origin, chunks,
                chunk_pages: dict[str, list[int]] | None = None) -> dict[str, int]:
    """Read the report's pay tables and check every AI line against them, in place."""
    if not pay_tables.ENABLED or not origin.pdf or not Path(origin.pdf).exists():
        return {}
    texts = origin.page_text()
    pages = set(pay.table_pages(chunks, texts, pay_tables.MAX_TABLE_PAGES))
    for item in lines:                       # the pages the AI's figures came from
        for c in item["line"].values():
            if isinstance(c, dict) and c.get("chunk_id") is not None and chunk_pages:
                pages.update(chunk_pages.get(str(c["chunk_id"]), [])[:2])
    pages = sorted(pages)[:MAX_PAGES] if len(pages) > MAX_PAGES else sorted(pages)
    rows = read_rows(name, fiscal_year, Path(origin.pdf), pages, texts)
    counts: dict[str, int] = {"table_rows": len(rows), "lines_matched": 0}
    for item in lines:
        if item["mapping"].get("excluded"):
            continue
        row = match(item["line"], rows)
        if not row:
            continue
        row.used = True
        counts["lines_matched"] += 1
        for s in compare(item, row, texts.get(row.page, "")).values():
            counts[s] = counts.get(s, 0) + 1
    return counts
