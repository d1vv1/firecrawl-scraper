"""Batch runner: CSV parsing, resume/skip rules, error handling (pipeline mocked)."""

import json

import pytest

from extractor import batch
from extractor.config import ConfigError


@pytest.fixture
def out(tmp_path, monkeypatch):
    monkeypatch.setattr(batch, "OUTPUT_DIR", tmp_path)
    return tmp_path


def _csv(tmp_path, text, name="c.csv", encoding="utf-8"):
    p = tmp_path / name
    p.write_bytes(text.encode(encoding))
    return p


def test_reads_comma_csv(tmp_path):
    p = _csv(tmp_path, "company_id,company_name,country_code\n1,Volvo AB,SE\n2,Ørsted A/S,dk\n")
    cs = batch.read_companies(p)
    assert [(c.company_id, c.name, c.country) for c in cs] == [("1", "Volvo AB", "SE"),
                                                               ("2", "Ørsted A/S", "DK")]


def test_reads_excel_semicolon_csv_with_bom_and_aliases(tmp_path):
    p = _csv(tmp_path, "ID;Name;Country\n10;Hennes & Mauritz AB;SE\n;;\n", encoding="utf-8-sig")
    cs = batch.read_companies(p)
    assert len(cs) == 1 and cs[0].name == "Hennes & Mauritz AB" and cs[0].country == "SE"


@pytest.mark.parametrize("text,msg", [
    ("company_id,company_name\n1,A\n1,B\n", "duplicate"),
    ("company_id,company_name,country_code\n1,A,SWE\n", "2-letter"),
    ("company_id,company_name\n,A\n", "required"),
    ("id,foo\n1,A\n", "company_name"),
])
def test_rejects_bad_csv(tmp_path, text, msg):
    with pytest.raises(ValueError, match=msg):
        batch.read_companies(_csv(tmp_path, text))


class _Args:
    force = retry_failed = False
    max_credits = None


def _fake_run(outcomes):
    """outcomes: company name -> 'ok' | exception instance. Writes result files like run()."""
    calls = []

    def fake(name, company_id, country, fc, use_cache, lei=None):
        calls.append(company_id)
        fc.credits.add("map", "x", 2)
        o = outcomes[name]
        if isinstance(o, Exception):
            raise o
        result = {"status": o, "lei": "LEI1", "revenue": {"value": 1.0, "unit": "millions",
                  "currency": "EUR", "value_full": 1e6}, "checks": [], "firecrawl_credits_used": 2}
        (batch.OUTPUT_DIR / f"{batch.slugify(company_id)}.json").write_text(json.dumps(result))
        return result
    return fake, calls


def test_batch_records_errors_and_continues(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,Good AB\nB,Bad AB\nC,Fine AB\n"))
    fake, calls = _fake_run({"Good AB": "ok", "Bad AB": RuntimeError("boom"), "Fine AB": "needs_review"})
    monkeypatch.setattr(batch, "run", fake)
    assert batch.run_batch(cs, _Args()) == 0
    assert calls == ["A", "B", "C"]
    err = json.loads((out / "b.error.json").read_text())
    assert err["error_type"] == "RuntimeError" and err["firecrawl_credits_used"] == 2
    rows = (out / "summary.csv").read_text(encoding="utf-8-sig").splitlines()
    assert rows[1].startswith("A,Good AB,,ok") and ",error," in rows[2] and "needs_review" in rows[3]

    # Re-run: done and failed companies are skipped, so nothing is called again.
    fake2, calls2 = _fake_run({})
    monkeypatch.setattr(batch, "run", fake2)
    batch.run_batch(cs, _Args())
    assert calls2 == []

    # --retry-failed only retries the failure.
    fake3, calls3 = _fake_run({"Bad AB": "ok"})
    monkeypatch.setattr(batch, "run", fake3)
    args = _Args(); args.retry_failed = True
    batch.run_batch(cs, args)
    assert calls3 == ["B"] and not (out / "b.error.json").exists()


def test_batch_stops_on_fatal_error(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\n"))
    fake, calls = _fake_run({"One AB": ConfigError("no key"), "Two AB": "ok"})
    monkeypatch.setattr(batch, "run", fake)
    assert batch.run_batch(cs, _Args()) == 2
    assert calls == ["A"]
    assert not (out / "a.error.json").exists()     # fatal errors aren't the company's fault


def test_batch_respects_max_credits(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\nC,Three AB\n"))
    fake, calls = _fake_run({"One AB": "ok", "Two AB": "ok", "Three AB": "ok"})
    monkeypatch.setattr(batch, "run", fake)
    args = _Args(); args.max_credits = 9        # each run spends 2; worst case = per-company cap 6
    batch.run_batch(cs, args)
    assert calls == ["A", "B"]                  # 0+6, 2+6 <= 9 run; 4+6 > 9 stops before C


@pytest.mark.parametrize("broken,fixed", [
    ("HuhtamÃ¤ki Oyj", "Huhtamäki Oyj"),
    ("IndustrivÃ¤rden AB", "Industrivärden AB"),
    ("Ã…landsbanken", "Ålandsbanken"),
    ("LÃ¥n og Spar Bank", "Lån og Spar Bank"),
    ("ByggmÃ¤stare Anders J AhlstrÃ¶m Holding AB (publ)", "Byggmästare Anders J Ahlström Holding AB (publ)"),
    ("Ørsted A/S", "Ørsted A/S"),          # already correct: unchanged
    ("AAK AB", "AAK AB"),
])
def test_fix_mojibake(broken, fixed):
    assert batch.fix_mojibake(broken) == fixed


def test_summary_write_survives_locked_file(out, monkeypatch, tmp_path):
    from pathlib import Path
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\n"))
    monkeypatch.setattr(batch.time, "sleep", lambda s: None)
    monkeypatch.setattr(Path, "replace", lambda self, target: (_ for _ in ()).throw(PermissionError("locked")))
    batch.write_summary(cs, out / "summary.csv")          # must not raise


def test_is_network_error_walks_the_exception_chain():
    import socket
    try:
        try:
            raise socket.gaierror(11001, "getaddrinfo failed")
        except socket.gaierror:
            raise AttributeError("'NoneType' object has no attribute 'status_code'")  # SDK bug
    except AttributeError as e:
        assert batch.is_network_error(e)
    assert not batch.is_network_error(ValueError("bad pdf"))


def test_network_outage_waits_and_retries_same_company(out, monkeypatch, tmp_path):
    import socket
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\n"))
    attempts = []

    def flaky(name, company_id, country, fc, use_cache, lei=None):
        attempts.append(company_id)
        if company_id == "A" and attempts.count("A") == 1:
            raise socket.gaierror(11001, "getaddrinfo failed")
        result = {"status": "ok", "checks": [], "firecrawl_credits_used": 0}
        (batch.OUTPUT_DIR / f"{batch.slugify(company_id)}.json").write_text(json.dumps(result))
        return result
    waits = []
    monkeypatch.setattr(batch, "run", flaky)
    monkeypatch.setattr(batch, "internet_up", lambda: False)
    monkeypatch.setattr(batch, "wait_for_internet", lambda *a, **k: waits.append(1) or True)
    assert batch.run_batch(cs, _Args()) == 0
    assert attempts == ["A", "A", "B"] and waits == [1]
    assert not (out / "a.error.json").exists()         # an outage is not the company's failure


def test_long_outage_stops_the_batch(out, monkeypatch, tmp_path):
    import socket
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\n"))
    calls = []

    def down(name, company_id, country, fc, use_cache, lei=None):
        calls.append(company_id)
        raise socket.gaierror(11001, "getaddrinfo failed")
    monkeypatch.setattr(batch, "run", down)
    monkeypatch.setattr(batch, "internet_up", lambda: False)
    monkeypatch.setattr(batch, "wait_for_internet", lambda *a, **k: False)
    assert batch.run_batch(cs, _Args()) == 3
    assert calls == ["A"]


def test_old_network_failures_are_retried_automatically(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\n"))
    (out / "a.error.json").write_text(json.dumps({"error_type": "AttributeError",
                                                  "error": "'NoneType' object has no attribute 'status_code'"}))
    (out / "b.error.json").write_text(json.dumps({"error_type": "ValueError", "error": "bad pdf"}))
    fake, calls = _fake_run({"One AB": "ok", "Two AB": "ok"})
    monkeypatch.setattr(batch, "run", fake)
    batch.run_batch(cs, _Args())
    assert calls == ["A"]                                # B's real failure is still skipped


def test_connection_error_with_internet_up_is_a_normal_failure(out, monkeypatch, tmp_path):
    """A bad certificate on one site is not an outage: record it and move on."""
    import httpx
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,One AB\nB,Two AB\n"))
    calls = []

    def ssl_fail(name, company_id, country, fc, use_cache, lei=None):
        calls.append(company_id)
        if company_id == "A":
            raise httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED]")
        result = {"status": "ok", "checks": [], "firecrawl_credits_used": 0}
        (batch.OUTPUT_DIR / f"{batch.slugify(company_id)}.json").write_text(json.dumps(result))
        return result
    monkeypatch.setattr(batch, "run", ssl_fail)
    monkeypatch.setattr(batch, "internet_up", lambda: True)
    monkeypatch.setattr(batch, "wait_for_internet", lambda *a, **k: pytest.fail("should not wait"))
    batch.run_batch(cs, _Args())
    assert calls == ["A", "B"] and (out / "a.error.json").exists()


def test_refresh_keeps_good_cached_report_and_drops_stale_one(out, monkeypatch, tmp_path):
    monkeypatch.setattr(batch, "CACHE_DIR", tmp_path)
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name,country_code\n"
                                             "GOOD,Good AB,SE\nOLD,Old AB,SE\nOCR,Scan AB,SE\n"))
    good, old, ocr = cs
    (tmp_path / "good_discovery.json").write_text(json.dumps(
        {"report_url": "https://good.se/annual-report-2025.pdf"}))
    (tmp_path / "old_discovery.json").write_text(json.dumps(
        {"report_url": "https://old.se/annual-report-2014.pdf"}))
    for c in (good, old):
        c.result_path.write_text("{}")
    ocr.error_path.write_text(json.dumps({"error_type": "NeedsOCRError"}))
    (tmp_path / "ocr_discovery.json").write_text(json.dumps(
        {"report_url": "https://scan.se/annual-report-2025.pdf", "report_alternatives": []}))

    assert batch.prepare_refresh(good) == "re-checking with the cached report"
    assert (tmp_path / "good_discovery.json").exists() and not good.result_path.exists()
    assert batch.prepare_refresh(old) == "finding the report again"
    assert not (tmp_path / "old_discovery.json").exists()
    assert batch.prepare_refresh(ocr) is None and ocr.error_path.exists()


def test_reads_segment_and_lei_columns(tmp_path):
    p = _csv(tmp_path, "company_id,company_name,country_code,segment,lei\n"
                       "a,1&1 AG,DE,europe_uk_listed,5299003VKVDCUPSS5X23\n"
                       "b,Some Co,,other_unlisted_or_unknown,\n")
    a, b = batch.read_companies(p)
    assert (a.segment, a.lei) == ("europe_uk_listed", "5299003VKVDCUPSS5X23")
    assert (b.segment, b.lei, b.country) == ("other_unlisted_or_unknown", None, None)
    with pytest.raises(ValueError, match="20-character"):
        batch.read_companies(_csv(tmp_path, "company_id,company_name,lei\nx,X,ABC\n", "bad.csv"))


def test_lei_from_csv_is_passed_to_the_pipeline(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name,lei\nA,One AB,5299003VKVDCUPSS5X23\n"))
    seen = {}

    def fake(name, company_id, country, fc, use_cache, lei=None):
        seen["lei"] = lei
        raise ValueError("stop")
    monkeypatch.setattr(batch, "run", fake)
    batch.run_batch(cs, _Args())
    assert seen["lei"] == "5299003VKVDCUPSS5X23"


def _threads(n):
    from concurrent.futures import ThreadPoolExecutor
    return lambda: ThreadPoolExecutor(max_workers=n)


def test_workers_run_companies_at_the_same_time(out, monkeypatch, tmp_path):
    import threading
    import time as _time
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\n" +
                                   "".join(f"C{i},Co {i} AB\n" for i in range(6))))
    active, peak, lock = [0], [0], threading.Lock()

    def slow(name, company_id, country, fc, use_cache, lei=None):
        with lock:
            active[0] += 1
            peak[0] = max(peak[0], active[0])
        _time.sleep(0.2)
        with lock:
            active[0] -= 1
        (batch.OUTPUT_DIR / f"{batch.slugify(company_id)}.json").write_text(
            json.dumps({"status": "ok", "checks": [], "firecrawl_credits_used": 0}))
        return {"status": "ok"}
    monkeypatch.setattr(batch, "run", slow)
    args = _Args(); args.workers = 3; args.executor_factory = _threads(3)
    assert batch.run_batch(cs, args) == 0
    assert peak[0] == 3                  # three companies were running at the same moment
    assert all((out / f"{batch.slugify(c.company_id)}.json").exists() for c in cs)


def test_workers_reserve_credits_for_running_companies(out, monkeypatch, tmp_path):
    """With a cap of 13 and 6 per company, only 2 may run at once and the 3rd waits
    until the spend is known; nothing ever starts that could break the cap."""
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\nA,A AB\nB,B AB\nC,C AB\n"))
    fake, calls = _fake_run({"A AB": "ok", "B AB": "ok", "C AB": "ok"})   # each spends 2
    monkeypatch.setattr(batch, "run", fake)
    args = _Args(); args.workers = 3; args.executor_factory = _threads(3); args.max_credits = 13
    batch.run_batch(cs, args)
    assert sorted(calls) == ["A", "B"] or sorted(calls) == ["A", "B", "C"]
    # A and B reserve 12; after both finish, 4 spent + 6 for C = 10 <= 13, so C runs too
    assert sorted(calls) == ["A", "B", "C"]


def test_fatal_error_stops_new_work_with_workers(out, monkeypatch, tmp_path):
    cs = batch.read_companies(_csv(tmp_path, "company_id,company_name\n" +
                                   "".join(f"C{i},Co {i} AB\n" for i in range(5))))

    def fatal(name, company_id, country, fc, use_cache, lei=None):
        raise ConfigError("no key")
    monkeypatch.setattr(batch, "run", fatal)
    args = _Args(); args.workers = 2; args.executor_factory = _threads(2)
    assert batch.run_batch(cs, args) == 2


def test_refresh_restores_companies_that_did_not_run(tmp_path, monkeypatch):
    # The credit limit stopped a --refresh run before these companies started: their
    # old results must come back (Oct 2026: 18 Nordic results were lost this way).
    from extractor import batch
    out, cache = tmp_path / "out", tmp_path / "cache"
    out.mkdir(); cache.mkdir()
    monkeypatch.setattr(batch, "OUTPUT_DIR", out)
    monkeypatch.setattr(batch, "CACHE_DIR", cache)
    monkeypatch.setattr(batch, "REFRESH_BACKUP", out / "_refresh_backup")
    monkeypatch.setattr(batch, "_cached_report_still_good", lambda c: False)
    c = batch.Company("x", "X AB", "SE")
    c.result_path.write_text('{"status": "needs_review"}')
    (cache / f"{c.slug}_discovery.json").write_text("{}")
    assert batch.prepare_refresh(c) == "finding the report again"
    assert not c.result_path.exists() and not (cache / f"{c.slug}_discovery.json").exists()
    assert batch.restore_refresh(c)
    assert c.result_path.read_text() == '{"status": "needs_review"}'
    assert (cache / f"{c.slug}_discovery.json").exists()
