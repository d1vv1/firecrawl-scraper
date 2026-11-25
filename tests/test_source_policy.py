"""Legal's source rules before each download and on identifiers (extractor/source_policy.py)."""

import csv

import pytest

from extractor import listing, scraper
from extractor import source_policy as sp
from tests.test_listing import offline, rec  # noqa: F401 - fixture


class FakeWeb:
    def __init__(self, hosts=None, docs=None):
        self.hosts, self.docs = hosts or {}, docs or {}

    def host(self, h):
        return self.hosts.get(h, {"robots_status": 404, "robots": "", "tdmrep": None, "ai_txt": ""})

    def doc(self, u):
        return self.docs.get(u, {})


@pytest.fixture
def policy(monkeypatch, tmp_path):
    def setup(mode, web=None, bucket=None):
        monkeypatch.setenv("LEGAL_SOURCE_RULES", {"enforce": "true", "off": "false"}.get(mode, mode))
        monkeypatch.setattr(sp, "LOG", tmp_path / "log.csv")
        monkeypatch.setattr(sp, "_web_checks", lambda: web or FakeWeb())
        monkeypatch.setattr(sp, "_bucket_origin", lambda url: (bucket or {}).get(url))
        return tmp_path / "log.csv"
    return setup


def _log(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if path.exists() else []


def test_report_mode_logs_a_blocked_download_but_lets_it_through(policy):
    log = policy("report")
    sp.gate("https://www.emarketstorage.it/x/report.pdf")          # no exception
    (row,) = _log(log)
    assert row["action"] == "would skip" and row["rule"] == "blocked host" and row["detail"] == "emarketstorage.it"


def test_enforce_skips_a_blocked_host_before_any_request(policy, monkeypatch):
    log = policy("enforce")
    monkeypatch.setattr(scraper, "_httpx_get", lambda url: pytest.fail("downloaded"))
    with pytest.raises(scraper.DownloadError) as e:
        scraper.download("https://s28.q4cdn.com/1/files/ar2025.pdf")
    assert isinstance(e.value, sp.SourceBlocked) and e.value.rule == "blocked host"
    assert _log(log)[0]["action"] == "skipped"


def test_false_or_unset_works_as_before(policy, monkeypatch):
    log = policy("off")
    sp.gate("https://live.euronext.com/x.pdf")
    assert sp.allows_candidate("https://live.euronext.com/x.pdf")
    assert sp.keep_identifier("ticker", "OpenFIGI", "X")
    monkeypatch.delenv("LEGAL_SOURCE_RULES")
    assert sp.mode() == "off"
    assert not log.exists()


def test_robots_tdm_and_ai_txt(policy):
    web = FakeWeb({
        "https://a.com": {"robots_status": 200, "robots": "User-agent: *\nDisallow: /private/\n"
                                                         "User-agent: FirecrawlAgent\nDisallow: /\n"},
        "https://down.com": {"robots_status": 503, "robots": ""},
        "https://ai.com": {"robots_status": 404, "ai_txt": "User-agent: *\nDisallow: /\n"},
        "https://tdm.com": {"robots_status": 404, "tdmrep": [{"location": "/*", "tdm-reservation": 1}]},
    }, docs={"https://h.com/ar.pdf": {"tdm_reservation": "1"}})
    policy("enforce", web)
    assert sp.check("https://a.com/private/ar.pdf").rule == "robots.txt"
    assert sp.check("https://a.com/ir/ar.pdf").allowed                       # direct download
    assert sp.check("https://a.com/ir/ar.pdf", sp.FIRECRAWL).detail == "disallows FirecrawlAgent"
    assert sp.check("https://down.com/ar.pdf").rule == "robots.txt unreachable"
    assert sp.check("https://ai.com/ar.pdf").rule == "ai.txt"
    assert sp.check("https://tdm.com/ar.pdf").rule == "TDM reservation"
    assert sp.check("https://h.com/ar.pdf").detail == "TDM-Rep header"
    assert sp.check("https://api.gleif.org/api/v1/lei-records/X").allowed     # an API: no robots


def test_filings_xbrl_org_allowed_until_legal_answers(policy, monkeypatch):
    policy("enforce")
    url = "https://filings.xbrl.org/LEI/2025-12-31/ESEF/IT/0/r/reports/r.xhtml"
    assert sp.check(url).allowed
    monkeypatch.setenv("SOURCE_POLICY_XBRL", "block")
    assert sp.check(url).rule == "filings.xbrl.org"


def test_a_bucket_file_is_judged_by_its_original_address(policy):
    f = "file:///C:/x/cache/gcs/objects/bkt/it/acme/fy2025/ar.pdf"
    policy("enforce", bucket={f: {"source_url": "https://www.1info.it/doc/ar.pdf"}})
    v = sp.check(f)
    assert not v.allowed and "1info.it" in v.detail
    assert not sp.allows_candidate(f) and not sp.allows_candidate("https://www.eqs.com/x.pdf")
    assert sp.allows_candidate("https://www.acme.it/ar.pdf")


def test_candidates_are_only_filtered_when_enforcing(policy):
    policy("report")
    assert sp.allows_candidate("https://www.eqs.com/x.pdf")


def test_identifier_sources(policy):
    ok = sp.identifier_allowed
    assert ok("figi", "OpenFIGI") and not ok("ticker", "OpenFIGI") and not ok("isin", "OpenFIGI")
    assert ok("isin", "GLEIF") and not ok("isin", "ESMA FIRDS")
    assert ok("exchange", "ESMA FIRDS") and ok("listing_status", "Annual report (PDF)")
    assert not ok("listing_status", "Share information (web page)")
    assert not ok("exchange_segment", "Nasdaq Nordic") and ok("exchange_segment", "ESMA FIRDS")
    log = policy("enforce")
    assert not sp.keep_identifier("ticker", "OpenFIGI", "VOLVB")
    assert sp.keep_identifier("revenue", "OpenFIGI", "1")                     # not an identifier
    assert _log(log)[0]["action"] == "dropped"


def test_enforced_listing_values_take_isin_from_gleif_and_skip_openfigi(offline, policy, monkeypatch):  # noqa: F811
    policy("enforce")
    monkeypatch.setattr(listing, "firds_shares", lambda lei: [
        rec("SE0000115420", "XSTO", "1998-03-12", name="VOLVO A"),
        rec("SE0000115446", "XSTO", "1998-03-12", name="VOLVO B")])
    monkeypatch.setattr(listing, "openfigi", lambda isin, exch: pytest.fail("OpenFIGI asked"))
    got = {f.data_point: f for f in listing.listing_values("LEI", "SE", ["SE0000115446", "XS123"])}
    assert got["isin"].value == "SE0000115446" and got["isin"].source == "GLEIF"
    assert "/isins" in got["isin"].endpoint
    assert got["exchange"].source == "ESMA FIRDS" and got["listing_status"].value == "listed"
    assert "ticker" not in got
    assert listing.listing_values("LEI", "GB", ["GB00B"]) == []           # home outside FIRDS
