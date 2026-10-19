"""Read tagged figures from an inline-XBRL (iXBRL) document.

UK accounts filed at Companies House are XHTML pages with the figures tagged in
place (<ix:nonFraction name="core:TurnoverRevenue" contextRef=... scale="3">1,234</...>).
This reads those tags with the stdlib HTML parser (tolerant of entities and markup
that a strict XML parser rejects).
"""

import datetime as dt
import re
from html.parser import HTMLParser

from .esef import TaggedFigure

# Local concept names, any taxonomy (FRC "core", old "uk-gaap", IFRS).
REVENUE = ["TurnoverRevenue", "TurnoverGrossOperatingRevenue", "Revenue",
           "RevenueFromContractsWithCustomers"]
TOTAL_ASSETS = ["Assets", "TotalAssets"]
FIXED_ASSETS = ["FixedAssets", "NoncurrentAssets"]
CURRENT_ASSETS = ["CurrentAssets"]
EQUITY_AND_LIABILITIES = ["EquityAndLiabilities", "LiabilitiesAndEquity"]
EMPLOYEES = ["AverageNumberEmployeesDuringPeriod", "AverageNumberOfEmployees"]


class _Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.contexts: dict[str, dict] = {}
        self.units: dict[str, str] = {}
        self.facts: list[dict] = []
        self._ctx = None              # context being read
        self._field = None            # startdate / enddate / instant / explicitmember / measure
        self._member_dim = None
        self._unit = None
        self._fact = None             # open ix:nonfraction
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        local = tag.rsplit(":", 1)[-1]
        if local == "context":
            self._ctx = {"id": a.get("id"), "members": [], "dates": {}}
        elif self._ctx is not None and local in ("startdate", "enddate", "instant"):
            self._field, self._buf = local, ""
        elif self._ctx is not None and local == "explicitmember":
            self._field, self._buf, self._member_dim = "member", "", a.get("dimension")
        elif local == "unit":
            self._unit = a.get("id")
        elif self._unit is not None and local == "measure":
            self._field, self._buf = "measure", ""
        elif tag == "ix:nonfraction":
            if self._fact is None:
                self._fact = {**a, "text": ""}
                self._depth = 1
            else:
                self._depth += 1

    def handle_endtag(self, tag):
        local = tag.rsplit(":", 1)[-1]
        if self._field and local in ("startdate", "enddate", "instant"):
            self._ctx["dates"][local] = self._buf.strip()
            self._field = None
        elif self._field == "member" and local == "explicitmember":
            self._ctx["members"].append((self._member_dim or "", self._buf.strip()))
            self._field = None
        elif self._field == "measure" and local == "measure":
            self.units[self._unit] = self._buf.strip().split(":")[-1].upper()
            self._field = None
        elif local == "context" and self._ctx is not None:
            self.contexts[self._ctx["id"]] = self._ctx
            self._ctx = None
        elif local == "unit":
            self._unit = None
        elif tag == "ix:nonfraction" and self._fact is not None:
            self._depth -= 1
            if self._depth == 0:
                self.facts.append(self._fact)
                self._fact = None

    def handle_data(self, data):
        if self._field:
            self._buf += data
        if self._fact is not None:
            self._fact["text"] += data


def _number(fact: dict) -> float | None:
    """The fact's value: its text read with its format, times 10**scale, signed."""
    text = fact["text"].strip()
    fmt = (fact.get("format") or "").lower()
    if not text or "zero" in fmt or re.fullmatch(r"[-–—]+", text):
        value = 0.0
    else:
        if "comma" in fmt and "decimal" in fmt:          # 1.234,5
            text = text.replace(".", "").replace(" ", "").replace(",", ".")
        else:                                            # 1,234.5
            text = text.replace(",", "").replace(" ", "")
        text = re.sub(r"[^\d.]", "", text)
        if not text:
            return None
        try:
            value = float(text)
        except ValueError:
            return None
    value *= 10 ** int(fact.get("scale") or 0)
    return -value if fact.get("sign") == "-" else value


def _scope(members: list[tuple[str, str]], has_group: bool) -> str | None:
    """Group vs company figures from the context's dimensions; None for other
    breakdowns (segments, classes of shares...)."""
    if not members:
        return "parent_only" if has_group else "consolidated"
    names = [m.rsplit(":", 1)[-1].lower() for _, m in members]
    if all("consolidated" in n or ("group" in n and "company" not in n) for n in names):
        return "consolidated"
    if all(any(w in n for w in ("company", "entity", "parent", "separate", "solo")) for n in names):
        return "parent_only"
    return None


def _days(start: str, end: str) -> int:
    return (dt.date.fromisoformat(end[:10]) - dt.date.fromisoformat(start[:10])).days


def ixbrl_facts(html: str, period_end: str) -> tuple[dict[str, TaggedFigure], int | None]:
    """Revenue (the year ending period_end), total assets and total equity and
    liabilities (at period_end), and the average number of employees. Group figures
    win over the company's. UK balance sheets have no total-assets line: then total
    assets = fixed assets + current assets (both tagged)."""
    p = _Collector()
    p.feed(html)
    has_group = any(_scope([m], False) == "consolidated"
                    for c in p.contexts.values() for m in c["members"])
    found: dict[str, tuple[int, TaggedFigure]] = {}
    employees = None
    for f in p.facts:
        name = (f.get("name") or "").rsplit(":", 1)[-1]
        ctx = p.contexts.get(f.get("contextref"))
        if not ctx:
            continue
        dates = ctx["dates"]
        end = dates.get("enddate") or dates.get("instant")
        if not end or end[:10] != period_end[:10]:
            continue
        scope = _scope(ctx["members"], has_group)
        if scope is None:
            continue
        value = _number(f)
        if value is None:
            continue
        if name in EMPLOYEES:
            employees = employees or int(value)
            continue
        duration = "startdate" in dates
        for key, names, wants_duration in (("revenue", REVENUE, True),
                                           ("total_assets", TOTAL_ASSETS, False),
                                           ("fixed", FIXED_ASSETS, False),
                                           ("current", CURRENT_ASSETS, False),
                                           ("total_equity_and_liabilities", EQUITY_AND_LIABILITIES, False)):
            if name not in names or duration != wants_duration:
                continue
            if duration and not 300 <= _days(dates["startdate"], end) <= 400:
                continue                       # a quarter, or a long first period
            period = f"{dates['startdate'][:10]}/{end[:10]}" if duration else end[:10]
            prefix = (f.get("name") or name).split(":", 1)[0] if ":" in (f.get("name") or "") else ""
            fig = TaggedFigure(value, p.units.get(f.get("unitref"), "GBP"),
                               f"{prefix}:{name}" if prefix else name, period, scope)
            rank = (scope == "consolidated") * 2 + (name == names[0])
            if key not in found or rank > found[key][0]:
                found[key] = (rank, fig)
    out = {k: f for k, (_, f) in found.items() if k not in ("fixed", "current")}
    if "total_assets" not in out and "fixed" in found and "current" in found:
        fixed, current = found["fixed"][1], found["current"][1]
        if fixed.scope == current.scope and fixed.currency == current.currency:
            out["total_assets"] = TaggedFigure(fixed.value + current.value, fixed.currency,
                                               f"{fixed.concept} + {current.concept}",
                                               fixed.period, fixed.scope)
    return out, employees
