"""Company registries: the accounts every company files by law, free to read.

Private companies rarely put annual reports on their websites, but they must file
their accounts with the national registry. Two registries are open without a key:

  Norway   Brønnøysund (Regnskapsregisteret): the filed accounts as JSON (revenue,
           total assets, equity and liabilities), group (KONSERN) and company-only
           (SELSKAP), last three years. The company profile (Enhetsregisteret: legal
           form, industry, activity) is the text for the descriptive facts.
  Denmark  Erhvervsstyrelsen (offentliggørelser): every filed annual report, as XBRL
           (the figures) and inline-XBRL / PDF (the text).

The company is found by its registration number (from its LEI record) or, in Norway,
by an exact legal-name match. Never by "first search result": "Hurtigruten" finds a
small property company before the cruise group.

  UK       Companies House (needs a free LIVE API key, COMPANIES_HOUSE_API_KEY): the
           latest filed accounts, as iXBRL (tagged figures + text) or PDF (text; the
           AI reads the figures).

Sweden (Bolagsverket) needs an organisation account; not built yet.
"""

import datetime as dt
import gzip
import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .esef import TaggedFigure
from .ixbrl import ixbrl_facts
from .lei import match_level

log = logging.getLogger(__name__)

BRREG_ACCOUNTS = "https://data.brreg.no/regnskapsregisteret/regnskap/{orgnr}"
BRREG_ENTITY = "https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}"
BRREG_SEARCH = "https://data.brreg.no/enhetsregisteret/api/enheter"
VIRK_SEARCH = "http://distribution.virk.dk/offentliggoerelser/_search"
CH_API = "https://api.company-information.service.gov.uk"
REGISTRIES = {"NO": "brreg", "DK": "virk", "GB": "companies_house"}
_MIN_INTERVAL_S = 0.3
_last_call = 0.0


@dataclass
class RegistryFiling:
    registry: str              # "brreg" (Norway) or "virk" (Denmark)
    country: str
    org_number: str
    company: str               # the registry's name for the company
    form: str                  # what was filed, in words
    filing_id: str
    period_end: str            # YYYY-MM-DD
    report_url: str            # the filed accounts (JSON / XBRL)
    figures: dict[str, TaggedFigure] = field(default_factory=dict)
    text_url: str | None = None        # the readable report (DK: .xhtml or .pdf)
    profile_text: str | None = None    # NO: company profile, the text source
    employees: int | None = None
    language: str = "en"               # registry text is used as is (no website)
    viewer_url: str | None = None
    package_url: str | None = None
    lei: str | None = None

    @property
    def fiscal_year(self) -> str:
        return self.period_end[:4]

    @property
    def identifier(self) -> str:
        label = {"NO": "org. no.", "DK": "CVR", "GB": "company no."}.get(self.country, "reg. no.")
        return f"{label} {self.org_number}"

    def as_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "RegistryFiling":
        figs = {k: TaggedFigure(**v) for k, v in (d.get("figures") or {}).items()}
        return RegistryFiling(**{**d, "figures": figs})


class RegistryUnavailable(Exception):
    pass


@retry(retry=retry_if_exception_type((httpx.TransportError, RegistryUnavailable)),
       stop=stop_after_attempt(4), wait=wait_exponential(min=2, max=30), reraise=True)
def _request(method: str, url: str, **kw) -> httpx.Response:
    global _last_call
    pause = _MIN_INTERVAL_S - (time.monotonic() - _last_call)
    if pause > 0:
        time.sleep(pause)
    _last_call = time.monotonic()
    headers = {"User-Agent": "annual-report-extractor/0.1", **kw.pop("headers", {})}
    # httpx drops the auth header when a redirect leaves the host (Companies House
    # documents redirect to Amazon S3, which must not get it).
    r = httpx.request(method, url, timeout=120, follow_redirects=True, headers=headers, **kw)
    if r.status_code == 429 or r.status_code >= 500:
        raise RegistryUnavailable(f"HTTP {r.status_code} for {url}")
    return r


def _body(r: httpx.Response) -> bytes:
    """virk.dk serves some files gzip-compressed without saying so."""
    raw = r.content
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def org_number(lei_record: dict | None) -> str | None:
    """The registration number from the LEI record ("916 359 667" -> "916359667")."""
    reg = (lei_record or {}).get("registered_as") or ""
    digits = re.sub(r"\D", "", reg)
    return digits or None


# --- Norway -----------------------------------------------------------------------

def _no_find_orgnr(legal_name: str) -> tuple[str | None, str]:
    r = _request("GET", BRREG_SEARCH, params={"navn": legal_name, "size": 50})
    if r.status_code != 200:
        return None, f"Brønnøysund name search failed (HTTP {r.status_code})"
    units = (r.json().get("_embedded") or {}).get("enheter") or []
    exact = {u["organisasjonsnummer"]: u["navn"] for u in units
             if not u.get("slettedato") and match_level(legal_name, u["navn"]) == "exact"}
    if len(exact) == 1:
        orgnr, name = next(iter(exact.items()))
        return orgnr, f"exact name match in Brønnøysund ({name})"
    if len(exact) > 1:
        return None, f"ambiguous: {len(exact)} Norwegian companies named like {legal_name!r}"
    return None, "no Norwegian company with exactly this name"


def _get(d: dict, *path):
    for p in path:
        d = (d or {}).get(p)
    return d


def _no_profile(entity: dict) -> str:
    """The company profile as text for the descriptive facts (no report needed)."""
    lines = [f"Company: {entity.get('navn')}",
             f"Organisation number: {entity.get('organisasjonsnummer')}",
             f"Legal form: {_get(entity, 'organisasjonsform', 'beskrivelse')} "
             f"({_get(entity, 'organisasjonsform', 'kode')})",
             f"Industry (NACE {_get(entity, 'naeringskode1', 'kode')}): "
             f"{_get(entity, 'naeringskode1', 'beskrivelse')}"]
    if entity.get("aktivitet"):
        lines.append("Business activity: " + " ".join(entity["aktivitet"]))
    if entity.get("vedtektsfestetFormaal"):
        lines.append("Purpose (articles of association): " + " ".join(entity["vedtektsfestetFormaal"]))
    if entity.get("antallAnsatte") is not None:
        lines.append(f"Number of employees: {entity['antallAnsatte']}")
    if entity.get("hjemmeside"):
        lines.append(f"Website: {entity['hjemmeside']}")
    if entity.get("overordnetEnhet"):
        lines.append(f"Parent unit (organisation number): {entity['overordnetEnhet']}")
    city = _get(entity, "forretningsadresse", "poststed")
    if city:
        lines.append(f"Business address: {city}, Norway")
    return "\n".join(lines)


def _no_filing(orgnr: str, lei: str | None) -> tuple["RegistryFiling | None", str]:
    r = _request("GET", BRREG_ACCOUNTS.format(orgnr=orgnr))
    if r.status_code == 404 or not r.content.strip():
        return None, f"no accounts filed in Brønnøysund for {orgnr}"
    r.raise_for_status()
    accounts = r.json()
    if not accounts:
        return None, f"no accounts filed in Brønnøysund for {orgnr}"
    latest = max(a["regnskapsperiode"]["tilDato"] for a in accounts)
    of_year = {a["regnskapstype"]: a for a in accounts if a["regnskapsperiode"]["tilDato"] == latest}
    acc = of_year.get("KONSERN") or of_year.get("SELSKAP") or next(iter(of_year.values()))
    if acc["regnskapstype"] == "KONSERN":
        scope = "consolidated"
    else:   # company-only accounts: the whole business unless it is a parent company
        scope = "parent_only" if _get(acc, "virksomhet", "morselskap") else "consolidated"
    period = acc["regnskapsperiode"]
    currency = acc.get("valuta") or "NOK"
    figures = {}
    # Revenue = sales revenue (salgsinntekter), as the golden values use; total
    # operating income also holds other income (Flokk: 831m sales, 941m in total).
    income = _get(acc, "resultatregnskapResultat", "driftsresultat", "driftsinntekter") or {}
    sales = income.get("salgsinntekter")
    revenue, revenue_concept = ((sales, "brreg:salgsinntekter") if sales is not None
                                else (income.get("sumDriftsinntekter"), "brreg:sumDriftsinntekter"))
    for key, value, concept, duration in (
            ("revenue", revenue, revenue_concept, True),
            ("total_assets", _get(acc, "eiendeler", "sumEiendeler"), "brreg:sumEiendeler", False),
            ("total_equity_and_liabilities", _get(acc, "egenkapitalGjeld", "sumEgenkapitalGjeld"),
             "brreg:sumEgenkapitalGjeld", False)):
        if value is not None:
            figures[key] = TaggedFigure(float(value), currency, concept,
                                        f"{period['fraDato']}/{period['tilDato']}" if duration
                                        else period["tilDato"], scope)
    entity_r = _request("GET", BRREG_ENTITY.format(orgnr=orgnr))
    entity = entity_r.json() if entity_r.status_code == 200 else {"organisasjonsnummer": orgnr}
    kind = "group" if acc["regnskapstype"] == "KONSERN" else "company"
    filing = RegistryFiling(
        registry="brreg", country="NO", org_number=orgnr, company=entity.get("navn") or "",
        form=f"Annual accounts ({kind}), Brønnøysund Register Centre",
        filing_id=str(acc.get("journalnr") or acc.get("id")), period_end=period["tilDato"],
        report_url=BRREG_ACCOUNTS.format(orgnr=orgnr), figures=figures,
        profile_text=_no_profile(entity), employees=entity.get("antallAnsatte"),
        viewer_url=f"https://virksomhet.brreg.no/nb/oppslag/enheter/{orgnr}", lei=lei)
    return filing, f"Brønnøysund {kind} accounts FY{filing.fiscal_year}"


# --- Denmark ----------------------------------------------------------------------

REVENUE_CONCEPTS = ["Revenue", "RevenueFromContractsWithCustomers"]
ASSETS_CONCEPTS = ["Assets"]
EQ_LIAB_CONCEPTS = ["LiabilitiesAndEquity", "EquityAndLiabilities"]


def xbrl_facts(xml: bytes, start: str, end: str) -> tuple[dict[str, TaggedFigure], int | None]:
    """Revenue (the year start..end), total assets and total liabilities and equity
    (at end) from an XBRL instance. Group figures (ConsolidatedMember) win over the
    parent company's; in Danish GAAP files without a group, the undimensioned figures
    are the company's whole business. Also the average number of employees."""
    root = ET.fromstring(xml)
    contexts, units = {}, {}
    has_group = False
    for el in root.iter():
        local = el.tag.rsplit("}", 1)[-1]
        if local == "context":
            members = [m.text or "" for m in el.iter() if m.tag.endswith("explicitMember")]
            dates = {p.tag.rsplit("}", 1)[-1]: (p.text or "").strip() for p in el.iter()
                     if p.tag.rsplit("}", 1)[-1] in ("startDate", "endDate", "instant")}
            contexts[el.get("id")] = (members, dates)
            has_group |= any(m.endswith("ConsolidatedMember") for m in members)
        elif local == "unit":
            measure = next((m.text for m in el.iter() if m.tag.endswith("measure")), "") or ""
            units[el.get("id")] = measure.split(":")[-1].upper()

    def scope_of(members: list[str], ifrs: bool) -> str | None:
        if not members:
            # ESEF (IFRS) facts without a dimension are the group's; in Danish GAAP the
            # undimensioned figures are the parent's when group figures also exist.
            return "consolidated" if ifrs or not has_group else "parent_only"
        if members == ["cmn:ConsolidatedMember"] or all(m.endswith("ConsolidatedMember") for m in members):
            return "consolidated"
        if all(m.endswith("SoloMember") for m in members):
            return "parent_only"
        return None                       # other breakdowns (segments, ...)

    best: dict[str, tuple[int, TaggedFigure]] = {}
    employees = None
    for el in root.iter():
        ctx = el.get("contextRef")
        if not ctx or ctx not in contexts or not (el.text or "").strip():
            continue
        uri, local = el.tag[1:].split("}", 1) if el.tag.startswith("{") else ("", el.tag)
        members, dates = contexts[ctx]
        if local == "AverageNumberOfEmployees" and dates.get("endDate") == end and not members:
            try:
                employees = int(float(el.text))
            except ValueError:
                pass
            continue
        for key, names, duration in (("revenue", REVENUE_CONCEPTS, True),
                                     ("total_assets", ASSETS_CONCEPTS, False),
                                     ("total_equity_and_liabilities", EQ_LIAB_CONCEPTS, False)):
            if local not in names:
                continue
            if duration and not (dates.get("startDate") == start and dates.get("endDate") == end):
                continue
            if not duration and dates.get("instant") != end:
                continue
            ifrs = "ifrs" in uri
            scope = scope_of(members, ifrs)
            if scope is None:
                continue
            try:
                value = float(el.text.strip())
            except ValueError:
                continue
            prefix = "ifrs-full" if ifrs else "fsa"
            fig = TaggedFigure(value, units.get(el.get("unitRef"), "DKK"), f"{prefix}:{local}",
                               f"{start}/{end}" if duration else end, scope)
            rank = (scope == "consolidated") * 2 + (local == names[0])
            if key not in best or rank > best[key][0]:
                best[key] = (rank, fig)
    return {k: f for k, (_, f) in best.items()}, employees


def _dk_filing(cvr: str, lei: str | None) -> tuple["RegistryFiling | None", str]:
    query = {"size": 10,
             "query": {"bool": {"must": [{"term": {"cvrNummer": int(cvr)}},
                                         {"term": {"offentliggoerelsestype": "regnskab"}}]}},
             "sort": [{"regnskab.regnskabsperiode.slutDato": {"order": "desc"}}]}
    r = _request("POST", VIRK_SEARCH, json=query)
    r.raise_for_status()
    for hit in r.json().get("hits", {}).get("hits", []):
        src = hit["_source"]
        docs = src.get("dokumenter") or []
        if not any(d["dokumentType"].startswith("AARSRAPPORT") for d in docs):
            continue                       # half-year and other reports
        period = src["regnskab"]["regnskabsperiode"]
        start, end = period["startDato"][:10], period["slutDato"][:10]
        # Listed companies: the IFRS figures are in the ESEF file, the other file only
        # holds Danish metadata (auditor, address). Read the ESEF file first.
        xml_docs = [d["dokumentUrl"] for d in sorted(docs, key=lambda d: d["dokumentType"] != "AARSRAPPORT_ESEF")
                    if d["dokumentMimeType"] == "application/xml"
                    and d["dokumentType"] in ("AARSRAPPORT", "AARSRAPPORT_ESEF")]
        text_doc = (next((d["dokumentUrl"] for d in docs if d["dokumentType"] == "AARSRAPPORT"
                          and d["dokumentMimeType"] == "application/xhtml+xml"), None)
                    or next((d["dokumentUrl"] for d in docs if d["dokumentType"] == "AARSRAPPORT"
                             and d["dokumentMimeType"] == "application/pdf"), None))
        figures, employees, name = {}, None, ""
        for url in xml_docs:
            body = _body(_request("GET", url))
            facts, emp = xbrl_facts(body, start, end)
            for k, v in facts.items():
                figures.setdefault(k, v)
            employees = employees or emp
            m = re.search(rb"NameOfReportingEntity[^>]*>([^<]+)<", body)
            name = name or (m.group(1).decode("utf-8", "replace").strip() if m else "")
        if not figures and not text_doc:
            return None, f"CVR {cvr}: the latest annual report (FY{end[:4]}) has no XBRL or text"
        filing = RegistryFiling(
            registry="virk", country="DK", org_number=cvr, company=name,
            form="Annual report, Danish Business Authority", filing_id=hit["_id"],
            period_end=end, report_url=xml_docs[0] if xml_docs else text_doc,
            figures=figures, text_url=text_doc, employees=employees,
            viewer_url=f"https://datacvr.virk.dk/enhed/virksomhed/{cvr}", lei=lei)
        return filing, f"Danish Business Authority annual report FY{filing.fiscal_year}"
    return None, f"CVR {cvr}: no annual report filed"


# --- entry point ------------------------------------------------------------------

# --- UK ---------------------------------------------------------------------------

def ch_key() -> str | None:
    from .config import load_settings
    load_settings()
    return (os.getenv("COMPANIES_HOUSE_API_KEY") or "").strip() or None


def available(home: str | None) -> bool:
    """Can this registry be used now? (The UK needs an API key.)"""
    return home in REGISTRIES and (home != "GB" or bool(ch_key()))


def _ch(path_or_url: str, **kw) -> httpx.Response:
    url = path_or_url if path_or_url.startswith("http") else CH_API + path_or_url
    r = _request("GET", url, auth=(ch_key() or "", ""), **kw)
    if r.status_code == 401:
        raise RegistryUnavailable("Companies House refused the API key (a test-environment "
                                  "key? It must be a LIVE REST key)")
    return r


def gb_number(lei_record: dict | None) -> str | None:
    """Company number from the LEI record: 8 characters, zero-padded ("445790" ->
    "00445790"); Scottish/NI numbers keep their prefix ("SC177553")."""
    reg = re.sub(r"[^A-Za-z0-9]", "", (lei_record or {}).get("registered_as") or "").upper()
    if not reg:
        return None
    return reg.zfill(8) if reg.isdigit() else reg


def _gb_find_number(legal_name: str) -> tuple[str | None, str]:
    r = _ch("/search/companies", params={"q": legal_name, "items_per_page": 50})
    if r.status_code != 200:
        return None, f"Companies House search failed (HTTP {r.status_code})"
    items = r.json().get("items") or []
    exact = {i["company_number"]: i["title"] for i in items
             if i.get("company_status") == "active" and match_level(legal_name, i["title"]) == "exact"}
    if len(exact) == 1:
        number, title = next(iter(exact.items()))
        return number, f"exact name match at Companies House ({title})"
    if len(exact) > 1:
        return None, f"ambiguous: {len(exact)} active UK companies named like {legal_name!r}"
    return None, "no active UK company with exactly this name"


def _gb_filing(number: str, lei: str | None) -> tuple["RegistryFiling | None", str]:
    r = _ch(f"/company/{number}/filing-history", params={"category": "accounts", "items_per_page": 25})
    if r.status_code == 404:
        return None, f"company {number} not found at Companies House"
    r.raise_for_status()
    items = [i for i in r.json().get("items") or []
             if (i.get("description_values") or {}).get("made_up_date")
             and (i.get("links") or {}).get("document_metadata")
             and "dormant" not in (i.get("description") or "")]
    if not items:
        return None, f"company {number}: no accounts filed"
    latest = max(items, key=lambda i: i["description_values"]["made_up_date"])
    period_end = latest["description_values"]["made_up_date"]
    kind = (latest.get("description") or "accounts").replace("accounts-with-accounts-type-", "")
    meta_r = _ch(latest["links"]["document_metadata"])
    meta_r.raise_for_status()
    meta = meta_r.json()
    resources = meta.get("resources") or {}
    content_url = (meta.get("links") or {}).get("document")
    if not content_url:
        return None, f"company {number}: the {period_end} accounts have no downloadable document"
    figures, employees = {}, None
    if "application/xhtml+xml" in resources:
        doc = _ch(content_url, headers={"Accept": "application/xhtml+xml"})
        doc.raise_for_status()
        figures, employees = ixbrl_facts(doc.text, period_end)
        text_kind = "ixbrl"
    elif "application/pdf" in resources:
        text_kind = "pdf"
    else:
        return None, f"company {number}: the {period_end} accounts are in an unsupported format"
    profile = _ch(f"/company/{number}")
    name = profile.json().get("company_name", "") if profile.status_code == 200 else ""
    filing = RegistryFiling(
        registry="companies_house", country="GB", org_number=number, company=name,
        form=f"Annual accounts ({kind}), Companies House", filing_id=latest.get("transaction_id", ""),
        period_end=period_end, report_url=content_url, figures=figures,
        text_url=content_url if text_kind == "ixbrl" else content_url + "#pdf", employees=employees,
        viewer_url=f"https://find-and-update.company-information.service.gov.uk/company/{number}/filing-history",
        lei=lei)
    return filing, (f"Companies House {kind} accounts made up to {period_end} "
                    f"({'tagged iXBRL' if text_kind == 'ixbrl' else 'PDF only: the AI reads the figures'})")


def find_filing(legal_name: str, country: str | None,
                lei_record: dict | None) -> tuple["RegistryFiling | None", str]:
    """(filing, reason): the latest accounts filed in the company's home registry."""
    home = (lei_record or {}).get("country") or country
    if home not in REGISTRIES:
        return None, f"no open registry for {home}"
    if not available(home):
        return None, "no COMPANIES_HOUSE_API_KEY in .env"
    same_country = (lei_record or {}).get("country") == home
    number = (gb_number(lei_record) if home == "GB" else org_number(lei_record)) if same_country else None
    how = "registration number from the LEI record"
    if not number and home == "NO":
        number, how = _no_find_orgnr(legal_name)
    elif not number and home == "GB":
        number, how = _gb_find_number(legal_name)
    if not number:
        return None, how if home in ("NO", "GB") else "no CVR number (no LEI record) for this Danish company"
    get = {"NO": _no_filing, "DK": _dk_filing, "GB": _gb_filing}[home]
    filing, why = get(number, (lei_record or {}).get("lei"))
    return filing, f"{why} ({how})"


def download_text(filing: RegistryFiling) -> tuple[str, bytes | str]:
    """("html" | "pdf" | "text", content) for the descriptive facts."""
    if filing.profile_text:
        return "text", filing.profile_text
    if filing.registry == "companies_house":
        pdf = filing.text_url.endswith("#pdf")
        r = _ch(filing.text_url.removesuffix("#pdf"),
                headers={"Accept": "application/pdf" if pdf else "application/xhtml+xml"})
    else:
        r = _request("GET", filing.text_url)
    r.raise_for_status()
    body = _body(r)
    if body[:4] == b"%PDF":
        return "pdf", body
    return "html", body.decode("utf-8", "replace")
