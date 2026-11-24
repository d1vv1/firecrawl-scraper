"""The legal source rules, measured only (extractor/source_impact.py)."""

from extractor import source_impact as si
from tests.test_before_dach import _row


class NoBucket:
    def origin(self, endpoint):
        return None


class OneBucketFile:
    def __init__(self, f):
        self.f = f

    def origin(self, endpoint):
        return self.f if "storage.cloud.google.com" in endpoint else None


def _v(name, value="1", **kw):
    return _row("a", name, value) | {"company_name": "A", "country": "IT"} | kw


def test_a_value_from_a_blocked_host_is_marked_with_where_to_read_it_again():
    v = si.classify(_v("base_salary", source="Remuneration report (PDF)",
                       endpoint="https://www.emarketstorage.it/x/report.pdf#page=4"), NoBucket())
    assert v["rules"] == "blocked host" and v["blocked_host_group"] == "news site"
    assert v["host"] == "www.emarketstorage.it" and "company's own website" in v["replacement_source"]
    assert si.classify(_v("revenue", endpoint="https://www.acme.it/ar.pdf#page=2"), NoBucket())["rules"] == ""


def test_identifiers_only_from_the_allowed_sources():
    rule = lambda **kw: si.classify(_v(**kw), NoBucket())["rules"]
    assert rule(name="ticker", source="OpenFIGI") == "identifier: OpenFIGI only for FIGI"
    assert rule(name="isin", source="ESMA FIRDS").startswith("identifier: ISIN")
    assert rule(name="isin", source="GLEIF") == ""
    assert rule(name="exchange", source="ESMA FIRDS") == ""
    assert rule(name="listing_status", source="Share information (web page)").startswith("identifier: exchange")


def test_a_bucket_file_is_judged_by_where_it_came_from():
    ep = "https://storage.cloud.google.com/bkt/uk/a/fy2025/x.pdf#page=3"
    from_q4 = OneBucketFile({"source_url": "https://s28.q4cdn.com/1/x.pdf", "found_on_page": ""})
    v = si.classify(_v("revenue", endpoint=ep), from_q4)
    assert v["host"] == "s28.q4cdn.com" and "blocked host" in v["rules"] and v["via_bucket"]
    unknown = si.classify(_v("revenue", endpoint=ep), OneBucketFile({}))
    assert unknown["rules"] == "bucket file: original URL not recorded"


def test_a_file_on_a_cms_host_needs_its_linking_page():
    v = si.classify(_v("revenue", endpoint="https://assets.ctfassets.net/abc/ar.pdf#page=9"), NoBucket())
    assert v["rules"] == "referrer missing (file host)"


def test_robots_tdm_and_ai_txt_verdicts():
    info = {"robots": "User-agent: *\nDisallow: /private/\n\nUser-agent: GPTBot\nDisallow: /\n",
            "tdmrep": [{"location": "/reports/*", "tdm-reservation": 1}], "ai_txt": "User-agent: *\nDisallow: /\n"}
    star, fc, named = si.robots_verdict(info, "https://x.com/private/a.pdf")
    assert star and fc and named == ["GPTBot"]
    assert si.robots_verdict(info, "https://x.com/ir/a.pdf")[:2] == (False, False)
    assert si.tdm_reserved(info, "https://x.com/reports/ar.pdf") and not si.tdm_reserved(info, "https://x.com/ir/a.pdf")
    assert si.ai_txt_disallows(info, "https://x.com/ir/a.pdf")
