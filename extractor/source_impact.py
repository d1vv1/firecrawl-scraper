"""What the legal source rules (24 Nov 2026) would touch in a datapoints CSV. Nothing is
enforced: the values stay as they are; this only measures.

    python -m extractor.source_impact [output/fy2025_runs_datapoints.csv]
        [--out output/source_rules_impact.xlsx] [--no-web]

The rules, as legal sent them:
- blocked hosts: no value from these, in any download path (BLOCKED_HOSTS);
- exchanges are no longer "official" sources (EXCHANGE_HOSTS: the blocked ones and the rest);
- identifiers: only the FIGI code from OpenFIGI; ISIN from GLEIF's ISIN-to-LEI file;
  exchange and listing status from ESMA FIRDS or the annual report;
- the document URL on every value, plus the company page that links to it when the file
  sits on a web host (CMS_HOSTS: Contentful, Cloudinary, Storyblok and similar);
- before each download, robots.txt and the text-and-data-mining opt-outs (TDM-Rep header,
  /.well-known/tdmrep.json, /ai.txt) are respected.

A value read from a CDP bucket file is judged by where the file came from: the bucket's
metadata.json gives its `source_url` and the page that linked it (`found_on_page`).

The web checks (robots.txt, tdmrep.json, ai.txt once per host; a HEAD per document for the
TDM-Rep header) are cached in cache/source_impact/; --no-web skips them.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlparse

from . import gcs, source_policy
from .config import CACHE_DIR, OUTPUT_DIR
from .rerun_list import PRIORITY

COMBINED = OUTPUT_DIR / "fy2025_runs_datapoints.csv"
OUT = OUTPUT_DIR / "source_rules_impact.xlsx"
WEB_CACHE = CACHE_DIR / "source_impact"

BLOCKED_HOSTS = {
    # stock exchanges
    "oslobors.no": "stock exchange", "euronext.com": "stock exchange",
    "nasdaq.com": "stock exchange", "jse.co.za": "stock exchange",
    # news sites (legal's heading; the Italian two are authorised storage mechanisms,
    # the others regulated-news distributors)
    "emarketstorage.it": "news site", "1info.it": "news site", "eqs.com": "news site",
    "q4cdn.com": "news site", "investorweb": "news site", "mfn.se": "news site",
    "cision.com": "news site", "hauptversammlung.de": "news site",
    # file host
    "cdn.sanity.io": "PDF host",
}
# Exchanges that are not blocked but are no longer "official" (routing in CDP's web_sources.toml)
EXCHANGE_HOSTS = ("nasdaqomxnordic.com", "londonstockexchange.com", "six-group.com",
                  "borsaitaliana.it", "boerse-frankfurt.de", "deutsche-boerse.com",
                  "athexgroup.gr", "athens.euronext.com", "bolsasymercados.es", "bmerf.es",
                  "wienerborse.at", "spotlightstockmarket.com", "ngm.se", "omxnordic.com",
                  "ise.ie", "luxse.com", "bourse.lu")
# File hosts where the company page that links the file must be recorded
CMS_HOSTS = {"ctfassets.net": "Contentful", "contentful.com": "Contentful",
             "cloudinary.com": "Cloudinary", "storyblok.com": "Storyblok",
             "sanity.io": "Sanity", "website-files.com": "Webflow", "prismic.io": "Prismic",
             "imgix.net": "imgix", "hubspotusercontent": "HubSpot", "hubfs": "HubSpot",
             "amazonaws.com": "Amazon S3", "cloudfront.net": "CloudFront",
             "blob.core.windows.net": "Azure Blob", "azureedge.net": "Azure CDN",
             "googleapis.com": "Google Cloud Storage", "cdn.shopify.com": "Shopify",
             "squarespace-cdn.com": "Squarespace", "wixstatic.com": "Wix",
             "datocms-assets.com": "DatoCMS", "b-cdn.net": "Bunny CDN", "kxcdn.com": "KeyCDN"}
# Our values from data APIs: robots.txt is for crawlers, not for these; listed for completeness
API_HOSTS = ("api.gleif.org", "registers.esma.europa.eu", "api.openfigi.com", "data.sec.gov",
             "document-api.company-information.service.gov.uk", "api.company-information.service.gov.uk",
             "data.brreg.no", "api.prh.fi", "efts.sec.gov", "www.sec.gov", "filings.xbrl.org",
             "api3.oslo.oslobors.no", "ir-api.eqs.com", "storage.cloud.google.com")
NOT_A_FILING_ARCHIVE = "filings.xbrl.org"     # XBRL International's index: not national, not the company's
IDENTIFIER_FIELDS = {"isin", "exchange", "listing_status", "ticker", "cik", "exchange_segment",
                     "listing_date", "figi"}
# AI crawlers named in robots.txt: a sign of a text-and-data-mining opt-out
AI_BOTS = ("GPTBot", "CCBot", "ClaudeBot", "anthropic-ai", "Google-Extended", "PerplexityBot",
           "Bytespider", "Applebot-Extended", "FirecrawlAgent", "cohere-ai", "omgilibot")
UA = "Mozilla/5.0 (compatible; data-source-check/1.0)"
FIRECRAWL_UA = "FirecrawlAgent"

COLUMNS = ["company_id", "company_name", "country", "data_point", "role_row", "priority_field",
           "value", "source", "method", "document_url", "referrer_url", "host", "via_bucket",
           "rules", "blocked_host_group", "what_happens", "replacement_source"]


def _under(host: str, domains) -> str | None:
    host = host.lower()
    for d in domains:
        if host == d or host.endswith("." + d) or (("." not in d) and d in host):
            return d
    return None


class Bucket:
    """Bucket object path (bucket/a/b.pdf, unquoted) -> its source_url and found_on_page."""

    def __init__(self):
        self.by_path: dict[str, dict] = {}
        self._memo: dict[str, dict | None] = {}
        for rec in gcs.records():
            folder = rec.get("_folder", "")
            for f in rec.get("files") or []:
                name = f.get("file_name") or ""
                fy = f.get("fiscal_year") or ""
                for p in (f"{gcs.BUCKET}/{gcs.PREFIX}/{folder}/{fy}/{name}",
                          f"{gcs.BUCKET}/{gcs.PREFIX}/{folder}/{name}"):
                    self.by_path[p.replace("//", "/")] = f

    def origin(self, endpoint: str) -> dict | None:
        url = endpoint.split("#")[0]
        if url not in self._memo:
            self._memo[url] = self._origin(url)
        return self._memo[url]

    def _origin(self, url: str) -> dict | None:
        m = re.match(r"^file:/{2,3}.*?/cache/gcs/objects/(.+)$", url, re.I)
        rest = m.group(1) if m else (url[len(gcs.BROWSER):] if url.startswith(gcs.BROWSER) else
                                     url[5:] if url.startswith("gs://") else None)
        if rest is None:
            return None
        rest = unquote(rest)
        hit = self.by_path.get(rest)
        if hit is None:                      # folder layout differs: match on the file name
            name = rest.rsplit("/", 1)[-1]
            folder = rest.rsplit("/", 2)[0]
            hit = next((f for p, f in self.by_path.items() if p.endswith("/" + name)
                        and p.startswith(folder.rsplit("/", 1)[0])), None)
        return hit or {}


# --- the web checks ---------------------------------------------------------------------

class Web:
    def __init__(self, cache: Path = WEB_CACHE, workers: int = 16):
        import requests
        self.requests = requests
        self.cache = cache
        self.cache.mkdir(parents=True, exist_ok=True)
        self.workers = workers
        self.hosts = self._load("hosts.json")
        self.docs = self._load("documents.json")
        self.lock = threading.Lock()

    def _load(self, name):
        p = self.cache / name
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def save(self):
        for name, d in (("hosts.json", self.hosts), ("documents.json", self.docs)):
            (self.cache / name).write_text(json.dumps(d, ensure_ascii=False, indent=0), encoding="utf-8")

    def _get(self, url, method="GET"):
        try:
            r = self.requests.request(method, url, headers={"User-Agent": UA}, timeout=12,
                                      allow_redirects=True, stream=method == "GET")
            body = ""
            if method == "GET" and r.status_code == 200:
                body = r.raw.read(400_000, decode_content=True).decode("utf-8", "replace")
            r.close()
            return r.status_code, r.headers, body
        except Exception as e:              # noqa: BLE001 - a host that does not answer
            return None, {}, type(e).__name__

    def host(self, scheme_host: str) -> dict:
        if scheme_host in self.hosts:
            return self.hosts[scheme_host]
        out = {}
        st, _, body = self._get(scheme_host + "/robots.txt")
        out["robots_status"] = st
        out["robots"] = body if st == 200 and "<html" not in body[:300].lower() else ""
        st, _, body = self._get(scheme_host + "/.well-known/tdmrep.json")
        tdm = None
        if st == 200:
            try:
                tdm = json.loads(body)
            except ValueError:
                tdm = None
        out["tdmrep"] = tdm
        st, _, body = self._get(scheme_host + "/ai.txt")
        out["ai_txt"] = body[:4000] if st == 200 and "<html" not in body[:300].lower() else ""
        with self.lock:
            self.hosts[scheme_host] = out
        return out

    def doc(self, url: str) -> dict:
        if url in self.docs:
            return self.docs[url]
        st, headers, _ = self._get(url, "HEAD")
        out = {"status": st, "tdm_reservation": headers.get("tdm-reservation", ""),
               "tdm_policy": headers.get("tdm-policy", ""),
               "x_robots": headers.get("x-robots-tag", "")}
        with self.lock:
            self.docs[url] = out
        return out

    def run(self, hosts: list[str], docs: list[str]) -> None:
        todo_h = [h for h in hosts if h not in self.hosts]
        todo_d = [d for d in docs if d not in self.docs]
        print(f"web checks: {len(todo_h)} hosts, {len(todo_d)} documents to ask", flush=True)
        with ThreadPoolExecutor(self.workers) as ex:
            for i, _ in enumerate(ex.map(self.host, todo_h), 1):
                if i % 100 == 0:
                    print(f"  hosts {i}/{len(todo_h)}", flush=True)
                    self.save()
        self.save()
        # documents: one request at a time per host, hosts in parallel
        per = defaultdict(list)
        for d in todo_d:
            per[urlparse(d).netloc].append(d)

        def one_host(urls):
            for u in urls:
                self.doc(u)
                time.sleep(0.2)
        with ThreadPoolExecutor(self.workers) as ex:
            list(ex.map(one_host, per.values()))
        self.save()


def _groups(text: str) -> list[tuple[list[str], list[tuple[bool, str]]]]:
    """robots.txt -> [(user agents, [(allow, path pattern)])], consecutive User-agent lines
    sharing one group (RFC 9309)."""
    groups, agents, rules, last = [], [], [], ""
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, val = (x.strip() for x in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if last != "user-agent" and agents:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(val.lower())
        elif key in ("allow", "disallow") and agents:
            if val or key == "allow":
                rules.append((key == "allow", val))
        last = key
    if agents:
        groups.append((agents, rules))
    return groups


def _pattern(path: str) -> re.Pattern:
    end = path.endswith("$")
    body = re.escape(path[:-1] if end else path).replace(r"\*", ".*")
    return re.compile(body + ("$" if end else ""))


def robots_allows(text: str, agent: str, url: str) -> bool:
    """RFC 9309 / Google matching: the group naming the agent (else "*"), the longest
    matching rule wins, Allow on a tie; * and $ in paths."""
    p = urlparse(url)
    path = (p.path or "/") + (f"?{p.query}" if p.query else "")
    groups = _groups(text)
    a = agent.lower()
    mine = [r for ags, r in groups if any(x != "*" and x in a for x in ags)]
    if not mine:
        mine = [r for ags, r in groups if "*" in ags]
    best = None                      # (length, allow)
    for rules in mine:
        for allow, pat in rules:
            if not pat:
                continue
            if _pattern(pat).match(path):
                key = (len(pat), allow)
                if best is None or key > best:
                    best = key
    return best is None or best[1]


def robots_verdict(info: dict, url: str) -> tuple[bool, bool, list[str]]:
    """(blocked for every crawler "*", blocked for FirecrawlAgent, AI bots named as disallowed)."""
    text = info.get("robots") or ""
    if not text:
        return False, False, []
    star = not robots_allows(text, "*", url)
    fc = not robots_allows(text, FIRECRAWL_UA, url)
    named = [bot for bot in AI_BOTS
             if re.search(rf"(?im)^\s*user-agent:\s*{re.escape(bot)}\s*$", text)
             and not robots_allows(text, bot, url)]
    return star, fc, named


def tdm_reserved(info: dict, url: str) -> bool:
    """tdmrep.json: a rule whose location covers the URL's path with tdm-reservation 1."""
    rules = info.get("tdmrep")
    if not isinstance(rules, list):
        return False
    path = urlparse(url).path or "/"
    for r in rules:
        if not isinstance(r, dict):
            continue
        loc = str(r.get("location", "/"))
        pat = "^" + re.escape(loc).replace(r"\*", ".*")
        if re.match(pat, path) and str(r.get("tdm-reservation", "0")) == "1":
            return True
    return False


def ai_txt_disallows(info: dict, url: str) -> bool:
    text = info.get("ai_txt") or ""
    if not text:
        return False
    return not robots_allows(text, "*", url)


# --- the report ---------------------------------------------------------------------------

def classify(r: dict, bucket: Bucket) -> dict | None:
    if not r["value"]:
        return None
    endpoint = r["endpoint"] or ""
    doc = endpoint.split("#")[0]
    referrer, via_bucket = "", ""
    origin = bucket.origin(endpoint) if endpoint else None
    rules, what, repl = [], [], []
    if origin is not None:
        via_bucket = gcs.browser_url(doc)
        doc = origin.get("source_url") or ""
        referrer = origin.get("found_on_page") or ""
        if not doc:
            rules.append("bucket file: original URL not recorded")
            what.append("read from a CDP bucket file whose metadata has no source_url: "
                        "the document URL legal asks for is unknown")
            repl.append("the bucket's source_url for the file (ask the bucket's owners)")
    host = urlparse(doc).netloc.lower() if doc.startswith("http") else ""
    group = ""
    blocked = _under(host, BLOCKED_HOSTS) if host else None
    if blocked:
        group = BLOCKED_HOSTS[blocked]
        rules.append("blocked host")
        what.append(f"value from a blocked host ({blocked}): not promoted; re-read elsewhere")
        repl.append("company's own website or the national filing archive")
    exch = _under(host, EXCHANGE_HOSTS) if host and not blocked else None
    if exch or (r["source"] in ("Nasdaq Nordic", "Euronext") and not blocked):
        rules.append("exchange no longer official")
        what.append("exchange page: no longer an official source (routing changes in CDP)")
        repl.append("annual report, or ESMA FIRDS for exchange and listing status")
    dp_ = r["data_point"]
    if r["source"] == "OpenFIGI" and dp_ != "figi":
        rules.append("identifier: OpenFIGI only for FIGI")
        what.append(f"{dp_} from OpenFIGI: only the FIGI code may come from OpenFIGI")
        repl.append("annual report" if dp_ in ("ticker", "exchange_segment", "listing_date")
                    else "ESMA FIRDS or the annual report")
    elif dp_ == "isin" and r["source"] not in ("GLEIF",):
        rules.append("identifier: ISIN only from GLEIF")
        what.append(f"ISIN from {r['source'] or 'unknown'}: must come from GLEIF's ISIN-to-LEI file")
        repl.append("GLEIF ISIN-to-LEI file")
    elif dp_ in ("exchange", "listing_status") and not source_policy.identifier_allowed(dp_, r["source"]):
        rules.append("identifier: exchange/listing from FIRDS or annual report")
        what.append(f"{dp_} from {r['source'] or 'unknown'}: must come from ESMA FIRDS or the annual report")
        repl.append("ESMA FIRDS or the annual report")
    cms = _under(host, CMS_HOSTS) if host else None
    if cms and not referrer:
        rules.append("referrer missing (file host)")
        what.append(f"file on {CMS_HOSTS[cms]}: the company page that links it is not recorded")
        repl.append("same document; record the linking company page")
    if host == NOT_A_FILING_ARCHIVE or host.endswith("." + NOT_A_FILING_ARCHIVE):
        rules.append("question: filings.xbrl.org")
        what.append("filings.xbrl.org is neither the company's site nor a national archive: ask legal")
        repl.append("national OAM / filing archive copy of the same ESEF file")
    if not rules:
        rules.append("")
    return {"company_id": r["company_id"], "company_name": r["company_name"], "country": r["country"],
            "data_point": dp_, "role_row": r["role_row"], "priority_field": "yes" if dp_ in PRIORITY else "",
            "value": r["value"][:300], "source": r["source"], "method": r["method"],
            "document_url": doc or via_bucket or endpoint, "referrer_url": referrer, "host": host,
            "via_bucket": via_bucket, "rules": "; ".join(x for x in rules if x),
            "blocked_host_group": group, "what_happens": "; ".join(what),
            "replacement_source": "; ".join(dict.fromkeys(repl))}


def build(src: Path = COMBINED, out: Path = OUT, web: bool = True) -> dict:
    with open(src, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    bucket = Bucket()
    vals = [x for x in (classify(r, bucket) for r in rows) if x]
    # robots / TDM per document (not for the APIs)
    if web:
        docs = sorted({v["document_url"] for v in vals if v["document_url"].startswith("http")
                       and not _under(v["host"], API_HOSTS)})
        hosts = sorted({f"{urlparse(d).scheme}://{urlparse(d).netloc}" for d in docs})
        w = Web()
        w.run(hosts, docs)
        for v in vals:
            d = v["document_url"]
            if not d.startswith("http") or _under(v["host"], API_HOSTS):
                continue
            hinfo = w.hosts.get(f"{urlparse(d).scheme}://{urlparse(d).netloc}", {})
            dinfo = w.docs.get(d, {})
            star, fc, named = robots_verdict(hinfo, d)
            extra = []
            if star:
                extra.append("robots.txt disallows all crawlers")
            elif fc:
                extra.append("robots.txt disallows FirecrawlAgent")
            if tdm_reserved(hinfo, d) or str(dinfo.get("tdm_reservation", "")).strip() == "1":
                extra.append("TDM reservation (TDM-Rep)")
            if ai_txt_disallows(hinfo, d):
                extra.append("ai.txt disallows")
            if extra:
                v["rules"] = "; ".join(x for x in (v["rules"], *extra) if x)
                v["what_happens"] = "; ".join(x for x in (v["what_happens"],
                                              "download would be skipped and logged: " + ", ".join(extra)) if x)
                v["replacement_source"] = v["replacement_source"] or "another copy of the document whose host allows it"
            if named:
                v["ai_bots_disallowed"] = ", ".join(named)
            if "noai" in str(dinfo.get("x_robots", "")).lower():
                v["other_opt_out"] = f"X-Robots-Tag: {dinfo['x_robots']} (not on legal's list)"
    affected = [v for v in vals if v["rules"]]
    write_xlsx(out, vals, affected, src, web)
    csv_out = out.with_name(out.stem + "_values.csv")
    with open(csv_out, "w", encoding="utf-8-sig", newline="") as fh:
        w_ = csv.DictWriter(fh, fieldnames=COLUMNS + ["ai_bots_disallowed", "other_opt_out"], extrasaction="ignore")
        w_.writeheader()
        w_.writerows(affected)
    return {"values": len(vals), "affected": len(affected), "xlsx": out, "csv": csv_out}


def _main_rule(rules: str) -> list[str]:
    return [x.strip() for x in rules.split(";") if x.strip()]


def write_xlsx(out: Path, vals: list[dict], affected: list[dict], src: Path, web: bool) -> None:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE7F0")

    def sheet(title, header, rows, widths=None):
        ws = wb.create_sheet(title)
        ws.append(header)
        for c in ws[1]:
            c.font, c.fill = bold, head
        for r in rows:
            ws.append(r)
        ws.freeze_panes = "A2"
        if rows:
            ws.auto_filter.ref = ws.dimensions
        for i, w in enumerate(widths or [], 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        return ws

    total = len(vals)
    companies = {v["company_id"] for v in vals}
    prio = [v for v in vals if v["priority_field"]]
    hard = [v for v in affected if any(x in v["rules"] for x in
            ("blocked host", "identifier:", "robots.txt disallows all", "TDM reservation", "ai.txt"))]
    ws = wb.active
    ws.title = "Summary"
    lines = [
        ["Legal source rules: what they would touch (not enforced)"],
        [f"File: {src.name}; {total:,} values, {len(companies):,} companies; "
         f"web checks {'done' if web else 'skipped'}"],
        [],
        ["Rule", "Values", "% of all values", "Priority-field values", "Companies", "Effect"],
    ]
    effect = {
        "blocked host": "not promoted: re-read from the company's site or national archive",
        "exchange no longer official": "routing only (CDP); value stays if the page is allowed",
        "identifier: OpenFIGI only for FIGI": "re-source from FIRDS or the annual report",
        "identifier: ISIN only from GLEIF": "re-source from GLEIF's ISIN-to-LEI file",
        "identifier: exchange/listing from FIRDS or annual report": "re-source from FIRDS or the annual report",
        "referrer missing (file host)": "value stays; the linking company page must be added",
        "robots.txt disallows all crawlers": "download skipped: value lost unless another copy is allowed",
        "robots.txt disallows FirecrawlAgent": "download skipped for our crawler",
        "TDM reservation (TDM-Rep)": "download skipped: value lost unless another copy is allowed",
        "ai.txt disallows": "download skipped",
        "bucket file: original URL not recorded": "value stays; its document URL must be found (bucket metadata)",
        "question: filings.xbrl.org": "not in legal's list: confirm it counts as a filing archive",
    }
    per_rule = defaultdict(list)
    for v in affected:
        for x in _main_rule(v["rules"]):
            per_rule[x].append(v)
    for rule in effect:
        vs = per_rule.get(rule, [])
        lines.append([rule, len(vs), round(100 * len(vs) / max(total, 1), 2),
                      sum(1 for v in vs if v["priority_field"]), len({v["company_id"] for v in vs}),
                      effect[rule]])
    lines += [[],
              ["Any rule (excluding the filings.xbrl.org question)",
               sum(1 for v in affected if set(_main_rule(v["rules"])) - {"question: filings.xbrl.org"})],
              ["Values that would be lost or must be re-sourced (blocked host, identifier rule, "
               "robots/TDM/ai.txt block)", len(hard), round(100 * len(hard) / max(total, 1), 2),
               sum(1 for v in hard if v["priority_field"]), len({v["company_id"] for v in hard})],
              ["All values", total, 100, len(prio), len(companies)]]
    for line in lines:
        ws.append(line)
    ws["A1"].font = Font(bold=True, size=13)
    for c in ws[4]:
        c.font, c.fill = bold, head
    for i, w in enumerate([58, 10, 14, 20, 11, 70], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # by host
    by_host = defaultdict(list)
    for v in affected:
        by_host[v["host"] or "(no host)"].append(v)
    sheet("By host", ["host", "values", "priority-field values", "companies", "rules", "fields (top 5)"],
          [[h, len(vs), sum(1 for v in vs if v["priority_field"]), len({v["company_id"] for v in vs}),
            "; ".join(sorted({x for v in vs for x in _main_rule(v["rules"])})),
            ", ".join(f"{k} {n}" for k, n in Counter(v["data_point"] for v in vs).most_common(5))]
           for h, vs in sorted(by_host.items(), key=lambda x: -len(x[1]))],
          [38, 9, 18, 11, 60, 60])

    # by field
    by_field = defaultdict(lambda: Counter())
    filled = Counter(v["data_point"] for v in vals)
    for v in hard:
        by_field[v["data_point"]]["hard"] += 1
    for v in affected:
        by_field[v["data_point"]]["any"] += 1
    sheet("By field", ["data_point", "priority", "values filled now", "lost or re-sourced",
                       "% of the field", "any rule"],
          [[f, "yes" if f in PRIORITY else "", filled[f], c["hard"],
            round(100 * c["hard"] / max(filled[f], 1), 1), c["any"]]
           for f, c in sorted(by_field.items(), key=lambda x: -x[1]["hard"])],
          [28, 9, 16, 18, 14, 10])

    # by company
    by_co = defaultdict(list)
    for v in hard:
        by_co[(v["company_id"], v["company_name"], v["country"])].append(v)
    sheet("By company", ["company_id", "company", "country", "values lost or re-sourced",
                         "priority-field values", "hosts"],
          [[k[0], k[1], k[2], len(vs), sum(1 for v in vs if v["priority_field"]),
            ", ".join(sorted({v["host"] for v in vs if v["host"]}))]
           for k, vs in sorted(by_co.items(), key=lambda x: -len(x[1]))],
          [40, 40, 8, 22, 20, 60])

    # the values (legal's columns first)
    sheet("Values", COLUMNS + ["ai_bots_disallowed", "other_opt_out"],
          [[v.get(c, "") for c in COLUMNS + ["ai_bots_disallowed", "other_opt_out"]] for v in affected],
          [30, 30, 7, 24, 18, 8, 30, 26, 9, 60, 40, 28, 30, 40, 14, 60, 40, 20])
    wb.save(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.source_impact", description=__doc__.split("\n\n")[0])
    p.add_argument("csv", nargs="?", type=Path, default=COMBINED)
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--no-web", action="store_true", help="Skip robots.txt / TDM / ai.txt checks")
    a = p.parse_args(argv)
    res = build(a.csv, a.out, web=not a.no_web)
    print(f"{res['affected']:,} of {res['values']:,} values touched by a rule -> {res['xlsx']} and {res['csv']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
