"""Collecting only some data points (issue 16): `--fields` and the input's `run_required`.

A selection is a set of data point names (company grain: datapoints.DATA_POINTS; role
grain: pay.ROLE_POINTS), or None for every data point. It decides which steps a company
needs (`needs_*`), and how the run's rows are merged into the company's saved rows: the
selected data points are replaced, every other row stays as it was (`merge`).
"""

from .pay import ROLE_POINTS

# Company-level pay terms: read with the executive pay (pay.company_terms).
PAY_TERMS = ("pension_type", "benefits", "shareholding_requirement")

# Kept in step with datapoints.DATA_POINTS (a test checks it); not imported from there,
# which imports this module.
COMPANY_POINTS = (
    "legal_name", "other_names", "lei", "business_id", "cik", "isin", "ticker", "exchange",
    "exchange_segment", "listing_status", "listing_date", "country_code", "head_office_city",
    "website", "sector_code", "sub_sector", "revenue", "total_assets", "ebitda", "fiscal_year",
    "fiscal_year_end", "reporting_currency", "accounting_basis", "headcount", "fte",
    "shares_outstanding", "share_price", "market_cap_band", "largest_holders",
    "controlling_owner", "controlling_owner_name", "ownership_type", "pe_stake_5pct",
    "ultimate_parent", "revenue_by_segment", "staff_by_segment", "revenue_by_country",
    "staff_by_country", *PAY_TERMS)

GROUPS: dict[str, tuple[str, ...]] = {
    # with the fiscal year the pay is for: its end dates the pay rows
    "pay": (*ROLE_POINTS, *PAY_TERMS, "fiscal_year", "fiscal_year_end"),
    "company": tuple(n for n in COMPANY_POINTS if n not in PAY_TERMS),
    "ownership": ("largest_holders", "controlling_owner", "controlling_owner_name",
                  "ownership_type", "pe_stake_5pct", "ultimate_parent"),
    "listing": ("isin", "ticker", "exchange", "exchange_segment", "listing_status",
                "listing_date", "shares_outstanding", "share_price", "market_cap_band", "cik"),
    "financials": ("revenue", "total_assets", "ebitda", "fiscal_year", "fiscal_year_end",
                   "reporting_currency", "accounting_basis", "revenue_by_segment",
                   "revenue_by_country"),
    "staff": ("headcount", "fte", "staff_by_country", "staff_by_segment"),
}

# Values worked out from others: collected (and saved) together with what they rest on.
DEPENDS = {"market_cap_band": ("shares_outstanding", "share_price"),
           "sector_code": ("sub_sector",)}

# What the official APIs give (GLEIF, FIRDS and OpenFIGI, the registers, SEC EDGAR).
# A selection of only these needs no annual report: no report search, no report AI pass.
# Not here: listing_date (FIRDS's date is graded C, a document's wins), sector_code (the
# register's code describes the holding company: the business description decides),
# and what only some registers give (headcount, owners, shares).
API_FIELDS = frozenset({"lei", "legal_name", "other_names", "business_id", "cik", "isin",
                        "ticker", "exchange", "exchange_segment", "listing_status",
                        "country_code", "head_office_city"})

# The tracker's run_required column -> the group it asks for (None: everything).
RUN_REQUIRED = {"pay data": "pay", "company data": "company"}

NOT_COLLECTED = "not collected: this run asked only for "


def parse(text: str | None) -> frozenset[str] | None:
    """'revenue,headcount' or 'pay' (groups and names mixed) -> the data point names;
    None or '' or 'all' -> None (every data point). Unknown names raise ValueError."""
    if not text or text.strip().lower() == "all":
        return None
    out: set[str] = set()
    every = set(COMPANY_POINTS) | set(ROLE_POINTS)
    for word in (w.strip().lower() for w in text.split(",")):
        if not word:
            continue
        if word in GROUPS:
            out |= set(GROUPS[word])
        elif word in every:
            out.add(word)
        else:
            raise ValueError(f"unknown field {word!r}: use a data point name or one of the "
                             f"groups {', '.join(GROUPS)}")
    return expand(frozenset(out)) if out else None


def expand(sel: frozenset[str] | None) -> frozenset[str] | None:
    if sel is None:
        return None
    return sel | {d for name in sel for d in DEPENDS.get(name, ())}


def from_run_required(value: str | None) -> frozenset[str] | None:
    """'Pay Data' -> the pay fields, 'Company Data' -> the company fields, anything else
    ('Company and Pay Data', empty) -> None (every data point)."""
    group = RUN_REQUIRED.get(" ".join((value or "").lower().split()))
    return expand(frozenset(GROUPS[group])) if group else None


def combine(cli: frozenset[str] | None, required: frozenset[str] | None) -> frozenset[str] | None:
    """--fields and run_required together: what both ask for (None means no limit)."""
    if cli is None:
        return required
    if required is None:
        return cli
    return cli & required


def wants(sel: frozenset[str] | None, name: str) -> bool:
    return sel is None or name in sel


def needs_pay(sel: frozenset[str] | None) -> bool:
    """The pay step: for the role fields and the pay terms (not the fiscal year, which
    the report gives)."""
    return sel is None or bool(sel & {*ROLE_POINTS, *PAY_TERMS})


def needs_report(sel: frozenset[str] | None) -> bool:
    """The annual report is needed unless every field asked for comes from an API. Pay
    needs it too: its fiscal year end dates the pay rows, and it is a pay source."""
    return sel is None or bool(sel - API_FIELDS)


def needs_documents(sel: frozenset[str] | None) -> bool:
    """The company's website documents (Firecrawl): for pay (the remuneration report
    search) and for the document fallback of fields no API gives."""
    return sel is None or needs_pay(sel) or bool(sel - API_FIELDS)


def label(sel: frozenset[str] | None) -> str:
    """'pay', 'company', or the names, for notes and the console."""
    if sel is None:
        return "all"
    groups = [g for g in ("pay", "company") if expand(frozenset(GROUPS[g])) == sel]
    return groups[0] if groups else ", ".join(sorted(sel))


def missing(rows: list[dict], sel: frozenset[str]) -> list[str]:
    """The selected data points without a value in a company's saved rows."""
    have = {r["data_point"] for r in rows if r.get("value") not in (None, "")}
    return sorted(n for n in sel if n not in have)


def merge(old: list[dict], new: list[dict], sel: frozenset[str] | None) -> list[dict]:
    """The company's rows after a run limited to `sel`: the selected data points from the
    run, every other row as saved before (with its own scraper version). A data point
    neither selected nor saved before gets an empty row that says it wasn't collected.
    Role rows: the whole block is replaced when every role field is selected; otherwise
    the selected fields are replaced per role, other roles' and fields' rows kept."""
    if sel is None:
        return new
    why = NOT_COLLECTED + label(sel)

    def blank(r: dict) -> dict:
        return r | {"value": "", "unit": "", "period_end": "", "source": "", "endpoint": "",
                    "method": "", "retrieved_at": "", "confidence": "", "note": why}

    old_co = {r["data_point"]: r for r in old if r["grain"] == "company"}
    out = []
    for r in (r for r in new if r["grain"] == "company"):
        name = r["data_point"]
        out.append(r if name in sel else old_co.get(name) or blank(r))
    role_sel = sel & set(ROLE_POINTS)
    old_roles = [r for r in old if r["grain"] == "role"]
    new_roles = [r for r in new if r["grain"] == "role"]
    if role_sel == set(ROLE_POINTS):
        roles = new_roles
    elif not role_sel:
        roles = old_roles or [blank(r) for r in new_roles if r["data_point"] == "role_disclosure"][:1]
    else:
        kept = [r for r in old_roles if r["data_point"] not in role_sel]
        added = [r for r in new_roles if r["data_point"] in role_sel and r["role_row"]]
        order = list(dict.fromkeys(r["role_row"] for r in kept + added))
        rank = {n: i for i, n in enumerate(ROLE_POINTS)}
        roles = sorted(kept + added, key=lambda r: (order.index(r["role_row"]),
                                                    rank.get(r["data_point"], 99)))
        if not roles:
            roles = [blank(r) for r in new_roles if r["data_point"] == "role_disclosure"][:1]
    return out + roles
