"""Pay tables read by a table library, not by the AI (docs/pay_table_plan.md).

The pay AI call reads a pay table from markdown that the PDF conversion can get wrong
(two columns merged into one cell, "96<br>23"), and it also decides which columns make
up which field; both vary from run to run (docs/known_issues.md, issues 2 and 5). Here
the two jobs are split:

  1. READ    Camelot (stream mode) reads the grid of each page that looks like a pay
             table (pay.table_pages). No AI.
  2. MAP     One small AI call per grid, cached by the grid: which rows are the
             report year's executive rows, and which columns make up which field
             (prompts/pay_columns_system.md holds the rules). It gives row and column
             numbers only, never figures.
  3. ADD UP  Code adds the mapped cells of each row and applies the unit.
  4. CHECK   The parts must add up to the table's own total column (2%); a row that
             doesn't keeps the AI's figures.

The rows are then matched to the roles the pay AI call found (by name, title or base
salary), and their amounts replace the AI's; titles, targets and maximums still come
from the AI call. With no PDF, no table, or no match, nothing changes.
"""

import hashlib
import json
import logging
import os
import re
import warnings
from dataclasses import dataclass
from pathlib import Path

from . import llm
from .config import CACHE_DIR
from .schemas import ColumnMap, LtiAmount, PayAmount, RemunerationFacts, RolePay
from .sections import Chunk

log = logging.getLogger(__name__)

ENABLED = os.getenv("PAY_TABLES", "1").lower() not in ("0", "false", "no")
MAX_TABLE_PAGES = 6              # pages read with Camelot per document, at most
MIN_FIGURES = 12                 # a grid with fewer figure cells is not a pay table
MAX_GRID_ROWS = 80               # longer grids are prose read as columns
PAGE_CHARS = 4_000               # of the page's text, shown with the grid for its caption
TOTAL_TOLERANCE = 0.02           # as pay.TOTAL_TOLERANCE
AMOUNT_FIELDS = ("base_salary", "sti_paid", "lti_vested", "lti_granted", "benefits", "pension",
                 "pension_allowance")
# A figure cell: "1,242", "1 242", "(12)", "-", "–", "4.5"; not "73% / 27%" or a year.
_FIGURE = re.compile(r"\(?-?\d{1,3}(?:[ ,.  ']\d{3})*(?:[.,]\d+)?\)?|[-–—]")
_YEAR = re.compile(r"(19|20)\d{2}(/\d{2,4})?")


@dataclass
class Grid:
    page: int
    cells: list[list[str]]

    def width(self) -> int:
        return max(len(r) for r in self.cells)

    def first_figure_row(self) -> int:
        """The first row with two or more figures: the rows above it are headers."""
        return next((i for i, r in enumerate(self.cells) if sum(map(is_figure, r)) >= 2),
                    len(self.cells))

    def text(self) -> str:
        """The grid as numbered rows and columns, then each column's header words joined,
        for the mapping call and its cache."""
        width = self.width()
        lines = ["row | " + " | ".join(f"c{i}" for i in range(width))]
        lines += [f"r{i} | " + " | ".join(r) for i, r in enumerate(self.cells)]
        first = self.first_figure_row()
        lines += ["", "Header words above the first row of figures, per column (a header cell "
                      "can sit one column off):"]
        lines += [f"c{i}: {_header(self, i, first)}" for i in range(width)]
        return "\n".join(lines)


def is_figure(cell: str) -> bool:
    c = cell.strip()
    return bool(c) and bool(_FIGURE.fullmatch(c)) and not _YEAR.fullmatch(c)


def parse_figure(cell: str) -> float | None:
    """'1,242' -> 1242, '1 242' -> 1242, '(12)' -> -12, '-' -> 0, '4.5' -> 4.5; else None."""
    c = cell.strip().replace(" ", " ").replace(" ", " ")
    if c in ("-", "–", "—", "-,"):
        return 0.0
    if not is_figure(c.rstrip(",")):
        return None
    neg = c.startswith("(") or c.startswith("-")
    c = c.strip("()-").replace("'", "").replace(" ", "")
    # a separator followed by exactly three digits groups thousands; else it is decimal
    c = re.sub(r"[.,](?=\d{3}(?:[.,]|$))", "", c).replace(",", ".")
    try:
        v = float(c)
    except ValueError:
        return None
    return -v if neg else v


def clean(cells: list[list[str]]) -> list[list[str]]:
    """Cells on one line, empty rows and columns dropped."""
    rows = [[" ".join(c.split()) for c in r] for r in cells]
    rows = [r for r in rows if any(r)]
    keep = [i for i in range(max((len(r) for r in rows), default=0))
            if any(i < len(r) and r[i] for r in rows)]
    return [[r[i] if i < len(r) else "" for i in keep] for r in rows]


def read_grids(pdf: Path, pages: list[int]) -> list[Grid]:
    """Camelot's stream-mode grids of these pages that hold enough figures to be a pay
    table. Stream mode finds columns from the gaps between text, so it also turns prose
    columns into "tables": those have few figures and are dropped here."""
    try:
        import camelot
    except ImportError:
        log.warning("Pay tables: camelot is not installed; using the AI's reading only")
        return []
    out = []
    for page in pages:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tables = camelot.read_pdf(str(pdf), pages=str(page), flavor="stream")
        except Exception as e:  # noqa: BLE001 - a page Camelot can't read keeps the AI's reading
            log.warning("Pay tables: Camelot failed on page %d of %s: %s", page, pdf.name,
                        str(e)[:150])
            continue
        for t in tables:
            cells = clean(t.df.values.tolist())
            figures = sum(is_figure(c) for r in cells for c in r)
            if (figures >= MIN_FIGURES and len(cells) <= MAX_GRID_ROWS
                    and max((len(r) for r in cells), default=0) >= 3):
                out.append(Grid(page, cells))
    return out


def map_columns(grid: Grid, name: str, page_text: str = "") -> ColumnMap:
    """The mapping call, cached by the grid, the page and the prompt: the same table gets
    the same mapping on every run, and the cache file can be read and corrected."""
    prompt = llm.load_prompt("pay_columns_system")
    text = grid.text()
    page = page_text[:PAGE_CHARS]
    key = hashlib.sha1(f"{prompt}\n{text}\n{page}".encode()).hexdigest()[:16]
    path = CACHE_DIR / f"paytable_{key}.json"
    if path.exists():
        return ColumnMap.model_validate(json.loads(path.read_text(encoding="utf-8"))["map"])
    user = (f"Company: {name}\n\nPDF page {grid.page} as text, for the table's caption, year "
            f"and unit (its tables may be garbled here):\n\n{page}\n\nThe table, by row and "
            f"column number:\n\n{text}")
    m = llm.call_llm(prompt, user, ColumnMap)
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps({"page": grid.page, "grid": text, "model": llm.model_name(),
                                "map": m.model_dump()}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    return m


@dataclass
class TableRow:
    label: str                  # the person or role as printed
    page: int
    cells: dict[str, list[str]]  # field -> the printed cells added up
    values: dict[str, float]     # field -> the sum, as printed (unit not applied)
    total: float | None
    headers: dict[str, str]      # field -> "Other fees + Fringe benefits"


def _header(grid: Grid, col: int, upto: int) -> str:
    """A column's header: its non-figure cells above the first data row."""
    parts = [r[col] for r in grid.cells[:upto] if col < len(r) and r[col] and not is_figure(r[col])]
    return " ".join(parts)


def mapping_problem(m: ColumnMap, width: int) -> str | None:
    """Why a mapping can't be used, or None. Each column counts once, and the total is
    what the parts are checked against: a mapping without one is not used."""
    if not m.is_pay_table or not m.rows:
        return "not a pay table"
    used = [c for f in AMOUNT_FIELDS + ("other_in_total",) for c in getattr(m, f)]
    used += [m.total] if m.total is not None else []
    if len(used) != len(set(used)):
        return "a column is mapped to two fields (often a table with people as columns)"
    if any(not 0 <= c < width for c in used):
        return "a column number is outside the table"
    if not m.base_salary:
        return "no base salary column"
    if m.total is None:
        return "no total column to check the parts against"
    return None


def table_rows(grid: Grid, m: ColumnMap) -> list[TableRow]:
    """The mapped rows whose parts add up to the table's own total."""
    width = grid.width()
    problem = mapping_problem(m, width)
    if problem:
        if m.is_pay_table:
            log.info("Pay tables: table on page %d not used: %s", grid.page, problem)
        return []
    first = grid.first_figure_row()
    out = []
    for r in m.rows:
        if not 0 <= r.row < len(grid.cells):
            continue
        row = grid.cells[r.row] + [""] * (width - len(grid.cells[r.row]))
        cells, values, headers = {}, {}, {}
        for field in AMOUNT_FIELDS:
            cols = [c for c in getattr(m, field) if 0 <= c < width]
            got = [(c, parse_figure(row[c])) for c in cols]
            if not cols or any(v is None for _, v in got):
                continue                    # a mapped cell is empty or not a figure
            cells[field] = [row[c] for c in cols]
            values[field] = sum(v for _, v in got)
            headers[field] = " + ".join(_header(grid, c, first) or f"column {c}" for c in cols)
        total = parse_figure(row[m.total])
        other = [parse_figure(row[c]) or 0 for c in m.other_in_total]
        if "base_salary" not in values or total is None:
            log.info("Pay tables: page %d row %d (%s) skipped: no base salary or total figure",
                     grid.page, r.row, r.label[:40])
            continue
        if not adds_up(values, total, other):
            log.info("Pay tables: page %d row %d (%s) skipped: parts don't add up to the total",
                     grid.page, r.row, r.label[:40])
            continue
        cells["total"] = [row[m.total]]
        values["total"] = total
        headers["total"] = _header(grid, m.total, first) or f"column {m.total}"
        out.append(TableRow(r.label, grid.page, cells, values, total, headers))
    return out


def adds_up(values: dict[str, float], total: float, other: list[float]) -> bool:
    """The parts against the total, with the LTI the total includes: vested, granted,
    both or none (as pay.check_total)."""
    base = sum(v for k, v in values.items() if not k.startswith("lti_")) + sum(other)
    v, g = values.get("lti_vested", 0), values.get("lti_granted", 0)
    best = min(abs(base + lti - total) for lti in (0, v, g, v + g))
    return best <= TOTAL_TOLERANCE * abs(total) or (total == 0 and best == 0)


def _words(t: str) -> set[str]:
    return {w for w in re.findall(r"[a-zà-ÿ0-9]+", (t or "").lower()) if len(w) > 1}


def match(role: RolePay, rows: list[TableRow]) -> TableRow | None:
    """The table row of a role found by the AI: its person's name in the row label,
    else its title, else the one row with the same base salary as printed."""
    def only(found):
        return found[0] if len(found) == 1 else None
    if role.person_name:
        name = _words(role.person_name)
        if got := only([r for r in rows if name and name <= _words(r.label)]):
            return got
    title = _words(role.role_title)
    if got := only([r for r in rows if title and title <= _words(r.label)]):
        return got
    base = role.base_salary.value
    if base is not None:
        return only([r for r in rows if abs(r.values["base_salary"] - base) < 0.5])
    return None


def chunk_of(page: int, chunks: list[Chunk]) -> int | None:
    return next((c.id for c in chunks if page in c.pages), None)


def apply(facts: RemunerationFacts, rows: list[TableRow], unit, currency: str | None,
          chunks: list[Chunk], done: set[int]) -> RemunerationFacts:
    """The facts with each matched executive role's amounts taken from its table row.
    Roles in `done` (taken from an earlier table) are left alone; changed ones are added."""
    roles, used = [], set()
    for i, role in enumerate(facts.roles):
        row = (match(role, [r for r in rows if id(r) not in used])
               if role.executive and i not in done else None)
        if row is None:
            roles.append(role)
            continue
        used.add(id(row))
        done.add(i)
        cid = chunk_of(row.page, chunks)
        cur = currency or next((getattr(role, f).currency for f in ("total", "base_salary")
                                if getattr(role, f).currency), None)
        update = {}
        for field, value in row.values.items():
            quote = " | ".join([row.label] + row.cells[field])
            parts = row.headers[field]
            includes = f"table: {parts}" if "+" in parts else None
            if field.startswith("lti_"):
                old: LtiAmount = getattr(role, field)
                update[field] = LtiAmount(value=value, unit=unit, currency=cur,
                                          form=old.form or "other", includes=includes,
                                          quote=quote, chunk_id=cid)
            else:
                update[field] = PayAmount(value=value, unit=unit, currency=cur, includes=includes,
                                          quote=quote, chunk_id=cid)
        # a field the table doesn't map keeps the AI's figure; the LTI pair is one choice
        if "lti_vested" in update or "lti_granted" in update:
            for f in ("lti_vested", "lti_granted"):
                if f not in update:
                    update[f] = LtiAmount(value=None, unit=None, currency=None, form=None,
                                          includes=None, quote=None, chunk_id=None)
        if "pension" in update and "pension_allowance" not in update:
            update["pension_allowance"] = PayAmount(value=None, unit=None, currency=None,
                                                    includes=None, quote=None, chunk_id=None)
        roles.append(role.model_copy(update=update))
    return facts.model_copy(update={"roles": roles})


def from_tables(name: str, facts: RemunerationFacts, pdf: Path | None, chunks: list[Chunk],
                page_text: dict[int, str]) -> RemunerationFacts:
    """The pay AI call's facts with the amounts of every role found in a checked table
    row replaced by the table's figures. Unchanged without a PDF or a usable table."""
    from .pay import table_pages
    if not ENABLED or not pdf or not Path(pdf).exists():
        return facts
    pages = table_pages(chunks, page_text, MAX_TABLE_PAGES)
    if not pages:
        return facts
    from .datapoints import fiscal_end_year
    year = fiscal_end_year(facts.fiscal_year)
    done: set[int] = set()
    for grid in read_grids(Path(pdf), pages):
        try:
            m = map_columns(grid, name, page_text.get(grid.page, ""))
        except Exception as e:  # noqa: BLE001 - a failed mapping keeps the AI's reading
            log.warning("Pay tables: mapping page %d failed: %s", grid.page, str(e)[:150])
            continue
        if year and m.year and fiscal_end_year(m.year) != year:
            # Equinor prints last year's table on the next page
            log.info("Pay tables: table on page %d is for %s, the pay is for %s; not used",
                     grid.page, m.year, facts.fiscal_year)
            continue
        rows = table_rows(grid, m)
        if not rows:
            continue
        before = len(done)
        facts = apply(facts, rows, m.unit, m.currency, chunks, done)
        if len(done) > before:
            log.info("Pay tables: %d role(s) from the table on PDF page %d", len(done) - before,
                     grid.page)
    if not done:
        log.info("Pay tables: no table row matched a role; the AI's figures stay")
    return facts
