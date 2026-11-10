"""Step 7: check the extraction against the source text and basic sanity rules."""

import datetime as dt
import re
from dataclasses import asdict, dataclass

from .extract import Extraction, full_value
from .schemas import UNIT_MULTIPLIERS, MoneyFigure
from .config import clean_name, fold
from .sections import Chunk, strip_markup

# Active ISO 4217 currency codes.
ISO_4217 = set("""
AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BRL
BSD BTN BWP BYN BZD CAD CDF CHF CLP CNY COP CRC CUP CVE CZK DJF DKK DOP DZD EGP
ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HTG HUF IDR ILS INR
IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL
LYD MAD MDL MGA MKD MMK MNT MOP MRU MUR MVR MWK MXN MYR MZN NAD NGN NIO NOK NPR
NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD
SHP SLE SOS SRD SSP STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX
USD UYU UZS VES VND VUV WST XAF XCD XCG XOF XPF YER ZAR ZMW ZWG
""".split())

# How reports write a currency, to its ISO 4217 code. "kroner" is Danish or Norwegian:
# the company's country decides.
CURRENCY_ALIASES = {
    "US$": "USD", "$US": "USD", "USD$": "USD", "$": "USD", "US DOLLARS": "USD",
    "CA$": "CAD", "C$": "CAD", "A$": "AUD", "AU$": "AUD", "NZ$": "NZD", "HK$": "HKD",
    "S$": "SGD", "€": "EUR", "EURO": "EUR", "EUROS": "EUR", "£": "GBP", "STG": "GBP",
    "SFR": "CHF", "SFR.": "CHF", "FR.": "CHF", "KRONOR": "SEK", "SKR": "SEK",
    "NKR": "NOK", "DKR": "DKK", "¥": "JPY",
}
KRONER = {"DK": "DKK", "NO": "NOK", "FO": "DKK", "GL": "DKK"}


def iso_currency(text: str, country: str = "") -> str:
    """The ISO 4217 code for a currency as a report writes it ("US$" -> "USD"); a code,
    or anything not recognised, comes back unchanged."""
    t = (text or "").strip()
    if t.upper() in ISO_4217:
        return t.upper()
    if t.lower() in ("kroner", "kr", "kr."):
        return KRONER.get(country, t)
    return CURRENCY_ALIASES.get(t.upper(), t)


BALANCE_TOLERANCE = 0.005
MAX_FISCAL_YEAR_AGE = 3
_GAP_TOKENS = 3   # loose quote match: max extra tokens between quote tokens


@dataclass
class Check:
    name: str
    target: str
    result: str        # "pass" | "fail" | "skipped"
    detail: str = ""


# --- text normalization ----------------------------------------------------------

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")
_QUOTES = {ord("‘"): "'", ord("’"): "'", ord("“"): '"', ord("”"): '"'}
_SPACES = dict.fromkeys(map(ord, "     "), " ")


def normalize(text: str) -> str:
    """Lowercase, strip markdown/table markup, unify dashes/quotes/spaces, drop
    thousand separators (1,234 / 1.234 / 1 234 -> 1234), collapse whitespace."""
    # Only thin/no-break spaces count as thousand separators; a normal space
    # between digits usually separates table cells ("Turnover 2 50,503"). Swiss
    # reports group with an apostrophe ("414'843").
    t = re.sub(r"(?<=\d)['’,.   ](?=\d{3}(?!\d))", "", strip_markup(text))
    t = t.translate(_DASHES).translate(_QUOTES).translate(_SPACES).lower()
    # Dot leaders in US-style tables ("Net sales . . . . . $ 5,219,376") carry no
    # meaning, and the AI rarely copies their exact number.
    t = re.sub(r"(?:\.\s*){3,}", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:\.[0-9]+)?|[^\sa-z0-9]", text)


def quote_in_text(quote: str, source: str) -> str | None:
    """Return "exact" if the normalized quote is a substring of the normalized
    source, "loose" if its tokens appear in order with at most _GAP_TOKENS extra
    tokens between each (e.g. a table's Notes column), else None."""
    # Edge punctuation doesn't count: a quote cut mid-sentence often gains a "."
    q, s = normalize(quote).strip(" .,;:\"'"), normalize(source)
    if not q:
        return None
    if q in s:
        return "exact"
    qt = [t for t in _tokens(q) if t.isalnum() or "." in t]
    st = _tokens(s)
    if not qt:
        return None
    for start in (i for i, t in enumerate(st) if t == qt[0]):
        pos, ok = start, True
        for tok in qt[1:]:
            window = st[pos + 1: pos + 2 + _GAP_TOKENS]
            if tok not in window:
                ok = False
                break
            pos = pos + 1 + window.index(tok)
        if ok:
            return "loose"
    if len(qt) >= 2 and any(t[0].isdigit() for t in qt) and _in_one_row(qt, source):
        return "loose"
    if _ELLIPSIS.search(quote) and _parts_nearby(quote, s):
        return "loose"
    # A label wrapped over table cells is cut at the cell edges, sometimes mid-word
    # ("Executive V|ice President", Bang & Olufsen) and sometimes between words
    # ("(until|14-05-26)"): without spaces the two read alike. Long quotes only.
    qc, sc = re.sub(r"\s+", "", q), re.sub(r"\s+", "", s)
    if len(qc) >= _COMPACT_MIN and qc in sc:
        return "loose"
    if _rows_in_order(qt, source):
        return "loose"
    return None


_COMPACT_MIN = 40       # characters of a quote compared without spaces, at least


_ROWS_APART = 3   # lines between two pieces of a quote taken from several table rows, at most


def _rows_in_order(qt: list[str], source: str) -> bool:
    """A quote the AI took from several rows of a table, skipping columns: "Personnel by
    countries: 31 Dec 2025 Finland 1,409 Sweden 120" from a heading, a column header
    "31 Dec 2025 31 Dec 2024 Change" and the rows "Finland 1,409 1,444 -35" and
    "Sweden 120 122 -2" (Digia). The quote is cut into pieces where a word follows a
    figure (a new row's label); each piece is in one line of the source, in order with
    any gaps, the lines in order and at most _ROWS_APART apart. So a label never pairs
    with a figure from another full row, and a wrong figure still fails."""
    pieces, cur = [], []
    for t in qt:
        if cur and not t[0].isdigit() and cur[-1][0].isdigit():
            pieces.append(cur)
            cur = []
        cur.append(t)
    pieces.append(cur)
    if len(pieces) < 2 or not any(t[0].isdigit() for t in qt):
        return False
    lines = [_tokens(normalize(l)) for l in source.splitlines() if l.strip()]
    # a heading line (no figures) reads on into the row below it
    lines = [(lines[i - 1] if i and not any(t[0].isdigit() for t in lines[i - 1]) else []) + toks
             for i, toks in enumerate(lines)]

    def match(piece, line, pos):   # end position of piece in lines[line] from pos, or -1
        for tok in piece:
            try:
                pos = lines[line].index(tok, pos) + 1
            except ValueError:
                return -1
        return pos

    def rest(k, line, pos):        # pieces k.. placed from (line, pos) onwards
        if k == len(pieces):
            return True
        for ln in range(line, min(line + _ROWS_APART + 1, len(lines))):
            end = match(pieces[k], ln, pos if ln == line else 0)
            if end >= 0 and rest(k + 1, ln, end):
                return True
        return False

    first = pieces[0][0]
    return any(rest(0, i, 0) for i, toks in enumerate(lines) if first in toks)
_ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")
_PARTS_SPAN = 400          # characters of normalized text between two quoted parts, at most


def _parts_nearby(quote: str, s: str) -> bool:
    """A quote that leaves words out with "..." ("Short-term incentives may, for ...
    other Executives, a maximum of 80%"): each part in the normalized source, in order,
    each starting at most _PARTS_SPAN characters after the one before."""
    parts = [normalize(p).strip(" .,;:\"'") for p in _ELLIPSIS.split(quote)]
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return False
    for start in (m.start() for m in re.finditer(re.escape(parts[0]), s)):
        pos, ok = start + len(parts[0]), True
        for p in parts[1:]:
            i = s.find(p, pos)
            if i < 0 or i - pos > _PARTS_SPAN:
                ok = False
                break
            pos = i + len(p)
        if ok:
            return True
    return False


def numbers_in(text: str) -> list[float]:
    """Figures in a quote, thousands separators removed: '1,242 | 96<br>23' -> [1242, 96, 23].
    Space-grouped figures count both whole and in parts ("1 057 875" -> 1057875, 1, 57, 875),
    and a lone dash is a zero."""
    t = normalize(text)
    found = re.findall(r"\d+(?:\.\d+)?", t)
    found += [g.replace(" ", "") for g in re.findall(r"\d{1,3}(?: \d{3})+(?:\.\d+)?", t)]
    out = [float(x) for x in found]
    if re.search(r"(^|[\s|])[-–—](?=$|[\s|])", t):
        out.append(0.0)
    return out


def figure_in_quote(figure: float, quote: str, scaled: bool = False) -> bool:
    """The figure appears in the quote as one number, or as the sum of the quote's few
    cells (a table row "Anders Opedal | 96 | 23" for 119). `scaled`: the figure may also be
    printed in thousands, millions or billions ("(000s) 5 582 534" for 5,582,534,000)."""
    nums = numbers_in(quote or "")
    # a table cell that is one number grouped with plain spaces ("|22 868|", Volvo):
    # elsewhere a space between digits separates cells, so only a whole cell counts
    nums += [float(c.replace(" ", "")) for c in (x.strip() for x in (quote or "").split("|"))
             if re.fullmatch(r"\d{1,3}(?: \d{3})+", c)]
    wanted = [abs(figure) / k for k in ((1, 1e3, 1e6, 1e9) if scaled else (1,))]
    sums = ([sum(nums)] if 1 < len(nums) <= 4 else []) + ([sum(nums[1:])] if 1 < len(nums) <= 5 else [])
    return any(abs(abs(n) - w) <= max(0.005 * w, 1e-9) for n in nums + sums for w in wanted)


_FIGURE = re.compile(r"\d[\d,.]*\d|\d")


def _in_one_row(qt: list[str], source: str) -> bool:
    """The quote's tokens in order, with any gaps, within one table row of the source,
    or two neighbouring rows (converted tables can put a person's name on one line and
    their figures on the next). A quote read off a page image keeps the label and the
    figure but drops the other columns: "Salary|352 625|38 %" from the row
    "Salary|1 410 500|38 %|...|352 625|38 %". A drawn table converted from HTML has no
    "|": a line with three figures or more is a row too ("John Roberts FY26 461,262"
    from "John Roberts FY26 557,080 49,232 22,000 628,312 461,262 ...", AO World)."""
    lines = [l for l in source.splitlines() if "|" in l or len(_FIGURE.findall(l)) >= 3]
    for i in range(len(lines)):
        # the next row joins only a label row: one whose cells are mostly empty
        row = lines[i].strip()
        cells = [c.strip() for c in row[row.startswith("|"):len(row) - row.endswith("|")].split("|")]
        label_row = sum(not c for c in cells) >= len(cells) / 2
        if label_row:
            # a long name overflows into the next cells, cut mid-word: "Executive Vic|e
            # President, Chief Financial Offic|er" (Bang & Olufsen): join the pieces
            row = re.sub(r"(?<=[^\s|*])\**\|\**(?=[^\s|*])", "", row)
        lt, pos = _tokens(normalize(" ".join([row] + lines[i + 1:i + 2] if label_row else [row]))), 0
        for tok in qt:
            try:
                pos = lt.index(tok, pos) + 1
            except ValueError:
                break
        else:
            return True
    return False


# Scale words printed next to a number ("$37.4 billion", "SEK 1.2bn", "393 MSEK").
_SCALE_WORDS = {
    **dict.fromkeys(["thousand", "thousands", "tkr", "tsek", "tnok", "tdkk", "teur", "tusd",
                     "tusen", "tuhatta", "tausend", "tsd"], 1e3),
    **dict.fromkeys(["million", "millions", "mn", "mln", "m", "mio", "mill", "milj", "miljoner",
                     "millioner", "miljoonaa", "msek", "mnok", "mdkk", "meur", "musd", "mkr"], 1e6),
    **dict.fromkeys(["billion", "billions", "bn", "mrd", "mdr", "mdkr", "mia", "miljarder",
                     "milliarder", "miljardia", "milliarden", "bsek", "bnok"], 1e9),
}
_NUM_GROUPS = re.compile(r"\d+(?:\.\d+)?(?: \d+(?:\.\d+)?)*")


def _quote_numbers(quote: str) -> list[tuple[float, int, float | None]]:
    """(number, decimals printed, scale word multiplier or None) for each number in
    the quote. Handles decimal commas ("2 473,7", "393,4") and, since a plain space
    can both group thousands ("19 889") and separate table cells ("5 | 136 425 |
    133 795"), every run of 3-digit groups inside a space-separated sequence."""
    norm = normalize(quote)                                   # 1,234 / 1.234 -> 1234
    norm = re.sub(r"(?<=\d),(?=\d)", ".", norm)               # decimal comma
    out = []
    for m in _NUM_GROUPS.finditer(norm):
        parts = m.group().split(" ")
        tail = norm[m.end():]
        for i, first in enumerate(parts):
            cands = [first]
            if re.fullmatch(r"\d{1,3}", first):
                for j in range(i + 1, len(parts)):
                    if not re.fullmatch(r"\d{3}(?:\.\d+)?", parts[j]):
                        break
                    cands.append("".join(parts[i:j + 1]))
                    if "." in parts[j]:
                        break
            for k, c in enumerate(cands):
                last = i + k == len(parts) - 1 or (k == 0 and i == len(parts) - 1)
                word = re.match(r"\s?([a-zäöåæø]+)", tail) if last else None
                scale = _SCALE_WORDS.get(word.group(1)) if word else None
                decimals = len(c.split(".")[1]) if "." in c else 0
                out.append((float(c), decimals, scale))
    return out


def match_value(value: float, quote: str, unit: str | None = None) -> str | None:
    """How the value appears in the quote: "exact" (the printed number, ignoring
    sign/brackets), "scaled" (same amount in other words: 37,400 millions vs "$37.4
    billion", within the quote's rounding), or None."""
    full = abs(value) * UNIT_MULTIPLIERS.get(unit or "units", 1)
    for num, decimals, scale in _quote_numbers(quote):
        if abs(num - abs(value)) < 1e-9 * max(1.0, abs(value)):
            return "exact"
        if scale and unit and abs(num * scale - full) <= 0.5 * 10 ** -decimals * scale + 1e-6 * full:
            return "scaled"
    return None


def value_in_quote(value: float, quote: str, unit: str | None = None) -> bool:
    """True if a number in the quote equals the value (see match_value)."""
    return match_value(value, quote, unit) is not None


def prescaled_value(fig: MoneyFigure) -> float | None:
    """The printed number when the model already multiplied by the unit: value
    906,943,000 with unit "thousands" and quote "906,943" (Bulk Infrastructure)."""
    mult = UNIT_MULTIPLIERS.get(fig.unit or "units", 1)
    if fig.value is None or not fig.quote or mult == 1:
        return None
    printed = fig.value / mult
    for num, _, _ in _quote_numbers(fig.quote):
        if abs(num - abs(printed)) < 1e-9 * max(1.0, abs(printed)):
            return printed
    return None


def latest_year(fiscal_year: str | None) -> int | None:
    """'2025' -> 2025, '2024/25' -> 2025, 'FY2024-2025' -> 2025."""
    if not fiscal_year:
        return None
    m = re.findall(r"(?:19|20)\d{2}", fiscal_year)
    if not m:
        return None
    year = int(m[-1])
    tail = re.search(r"(?:19|20)\d{2}\s*[/-]\s*(\d{2})(?!\d)", fiscal_year)
    if tail:
        year = max(year, (year // 100) * 100 + int(tail.group(1)))
    return year


# --- checks ------------------------------------------------------------------------

def _source_for(chunk_id: int | None, chunks: list[Chunk]) -> tuple[str, str]:
    by_id = {c.id: c for c in chunks}
    if chunk_id in by_id:
        return by_id[chunk_id].text, f"chunk {chunk_id}"
    return "\n".join(c.text for c in chunks), f"all chunks (chunk_id {chunk_id} not sent)"


def check_quote(target: str, quote: str | None, chunk_id: int | None,
                chunks: list[Chunk]) -> Check:
    if not quote:
        return Check("quote", target, "skipped", "no quote")
    source, where = _source_for(chunk_id, chunks)
    mode = quote_in_text(quote, source)
    if mode:
        return Check("quote", target, "pass", f"{mode} match in {where}")
    # The model sometimes cites the wrong chunk id: accept an exact match elsewhere.
    for c in chunks:
        if c.id != chunk_id and quote_in_text(quote, c.text) == "exact":
            return Check("quote", target, "pass",
                         f"exact match in chunk {c.id} (model cited chunk {chunk_id})")
    # The model sometimes joins several real passages with "...": check each piece.
    pieces = [p for p in re.split(r"\.{3}|…", quote) if len(p.split()) >= 3]
    if len(pieces) > 1 and all(quote_in_text(p, source) for p in pieces):
        return Check("quote", target, "pass",
                     f"fragments match in {where} ({len(pieces)} passages joined with '...')")
    shown = quote if len(quote) <= 200 else quote[:200] + "…"
    return Check("quote", target, "fail",
                 f"quote not found in {where}: probable hallucination. Quote: {shown!r}")


def check_value_in_quote(target: str, fig: MoneyFigure) -> Check:
    if fig.value is None or not fig.quote:
        return Check("value_in_quote", target, "skipped", "no value or quote")
    how = match_value(fig.value, fig.quote, fig.unit)
    if how:
        return Check("value_in_quote", target, "pass",
                     "" if how == "exact" else f"same amount as printed in other units ({how})")
    printed = prescaled_value(fig)
    if printed is not None:
        old = fig.value
        fig.value = printed            # corrected in place: the output uses this value
        return Check("value_in_quote", target, "pass",
                     f"corrected {old:g} -> {printed:g} {fig.unit}: the model had already "
                     f"multiplied the printed number by the unit")
    return Check("value_in_quote", target, "fail", f"{fig.value:g} not in quote {fig.quote!r}")


def check_scope(target: str, fig: MoneyFigure) -> Check:
    if fig.value is None:
        return Check("scope", target, "skipped", "no value")
    if fig.scope == "consolidated":
        return Check("scope", target, "pass")
    return Check("scope", target, "fail", f"scope is {fig.scope!r}, not consolidated")


def check_balance(total_assets: MoneyFigure, total_eq_liab: MoneyFigure) -> Check:
    a = full_value(total_assets.value, total_assets.unit)
    b = full_value(total_eq_liab.value, total_eq_liab.unit)
    if a is None or b is None:
        return Check("balance", "total_assets", "skipped",
                     "total assets or total equity and liabilities missing")
    if total_assets.currency != total_eq_liab.currency:
        return Check("balance", "total_assets", "fail", "currencies differ")
    diff = abs(a - b) / max(abs(a), abs(b), 1e-9)
    ok = diff <= BALANCE_TOLERANCE
    return Check("balance", "total_assets", "pass" if ok else "fail",
                 f"assets {a:,.0f} vs equity+liabilities {b:,.0f} ({diff:.2%} apart)")


def check_sanity(target: str, fig: MoneyFigure) -> Check:
    if fig.value is None:
        return Check("sanity", target, "skipped", "no value")
    problems = []
    if fig.value <= 0:
        problems.append(f"value {fig.value:g} is not > 0")
    if (fig.currency or "").upper() not in ISO_4217:
        problems.append(f"currency {fig.currency!r} is not an ISO 4217 code")
    if fig.unit is None:
        problems.append("unit missing")
    return Check("sanity", target, "fail" if problems else "pass", "; ".join(problems))


def check_fiscal_year(fiscal_year: str | None, today: dt.date | None = None) -> Check:
    today = today or dt.date.today()
    year = latest_year(fiscal_year)
    if year is None:
        return Check("sanity", "fiscal_year", "fail", f"fiscal year {fiscal_year!r} not parseable")
    ok = today.year - MAX_FISCAL_YEAR_AGE <= year <= today.year
    return Check("sanity", "fiscal_year", "pass" if ok else "fail",
                 f"{fiscal_year} (latest year {year}, today {today.year})")


def run_checks(ex: Extraction) -> list[Check]:
    fin, qual = ex.financials, ex.qualitative
    checks: list[Check] = []
    money = {"revenue": fin.revenue, "total_assets": fin.total_assets,
             "total_equity_and_liabilities": fin.total_equity_and_liabilities}
    for name, fig in money.items():
        if name in ex.tagged:
            # Read from the filing's XBRL tag: the filing itself is the source.
            detail = f"read from XBRL tag {ex.tagged[name]} in the filing"
            checks.append(Check("quote", name, "pass", detail))
            checks.append(Check("value_in_quote", name, "pass", detail))
        else:
            checks.append(check_quote(name, fig.quote, fig.chunk_id, ex.financial_chunks))
            checks.append(check_value_in_quote(name, fig))
        if name != "total_equity_and_liabilities":
            checks.append(check_scope(name, fig))
            checks.append(check_sanity(name, fig))
    checks.append(check_balance(fin.total_assets, fin.total_equity_and_liabilities))
    checks.append(check_fiscal_year(fin.fiscal_year))
    if qual is not None:
        checks.append(check_quote("revenue_model", qual.revenue_model.quote,
                                  qual.revenue_model.chunk_id, ex.qualitative_chunks))
        checks.append(check_quote("business_structure", qual.business_structure.quote,
                                  qual.business_structure.chunk_id, ex.qualitative_chunks))
    return checks


# Checks on the descriptive fields only produce warnings: the status is about the
# financial figures (a reworded revenue-model sentence shouldn't hide a correct revenue).
DESCRIPTIVE_TARGETS = {"revenue_model", "business_structure"}


def overall_status(ex: Extraction, checks: list[Check]) -> str:
    fin = ex.financials
    if fin.revenue.value is None and fin.total_assets.value is None:
        return "not_found"
    blocking = [c for c in checks if c.target not in DESCRIPTIVE_TARGETS]
    return "needs_review" if any(c.result == "fail" for c in blocking) else "ok"


def warnings_for(checks: list[Check]) -> list[str]:
    return [f"{c.target}: {c.detail}" for c in checks if c.result == "fail"
            and (c.name == "scope" or c.target in DESCRIPTIVE_TARGETS)]


# --- entity check: is this report about the right company? ---------------------------

# Reporting currencies we expect per country (plus EUR and USD, which anyone may use).
HOME_CURRENCY = {
    "SE": "SEK", "NO": "NOK", "DK": "DKK", "FI": "EUR", "IS": "ISK", "FO": "DKK",
    "GB": "GBP", "CH": "CHF", "US": "USD", "BM": "USD", "KY": "USD", "PL": "PLN",
    "CA": "CAD", "AU": "AUD", "JP": "JPY", "CN": "CNY", "IN": "INR", "SG": "SGD",
    "HK": "HKD", "IL": "ILS", "CZ": "CZK", "HU": "HUF", "RO": "RON", "BG": "BGN",
}
ENTITY_FRONT_PAGES = 20   # covers are often images, so look past them


def _compact(text: str) -> str:
    # No digraph collapsing here: it would shrink "AAK" to "ak".
    return re.sub(r"[^a-z0-9]", "", fold(text, collapse_digraphs=False))


def check_entity(listed_name: str, gleif_name: str | None, countries: list[str | None],
                 currency: str | None, front_text: str) -> list[Check]:
    """Catch reports about the wrong company (e.g. ABB India Limited's report for ABB
    Ltd): the company's name must appear in the report's first pages, and the
    reporting currency must fit the company's countries."""
    checks = []
    names = [n for n in {clean_name(listed_name), clean_name(gleif_name or "")} if n]
    front = _compact(front_text)
    found = any(len(_compact(n)) >= 3 and _compact(n) in front for n in names)
    checks.append(Check("entity", "company_name", "pass" if found else "fail",
                        "" if found else f"none of {names} appears in the report's first "
                                         f"{ENTITY_FRONT_PAGES} pages: possibly another company's report"))
    if currency:
        allowed = {"EUR", "USD"} | {HOME_CURRENCY[c] for c in countries if c in HOME_CURRENCY}
        ok = currency.upper() in allowed or not any(c in HOME_CURRENCY for c in countries)
        checks.append(Check("entity", "currency", "pass" if ok else "fail",
                            "" if ok else f"reported in {currency}, expected one of "
                                          f"{sorted(allowed)}: possibly a subsidiary's report"))
    else:
        checks.append(Check("entity", "currency", "skipped", "no currency extracted"))
    return checks


def checks_as_dicts(checks: list[Check]) -> list[dict]:
    return [asdict(c) for c in checks]
