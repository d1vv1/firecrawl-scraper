"""Phase A of docs/not_found_reduction_plan.md: rules over the saved rows that fill a gap
the data already settles (GLEIF exceptions, ownership from the holder list, a zero part of
a stated total, the pay currency, a zero total, pence and cents share prices)."""

from extractor import apis
from extractor import datapoints as dp
from extractor.apis import Found
from tests.test_before_dach import _row

MISSING = "not found in: GLEIF, Annual report (PDF)"


def _by(rows):
    return {r["data_point"]: r for r in rows}


def _role(name, value, unit="EUR", role="CEO"):
    r = _row("a", name, value, "role", role, "" if value else "not found in: Remuneration report (PDF)")
    r["unit"] = unit if value else ""
    return r


# --- A1: GLEIF ------------------------------------------------------------------------------

def _gleif(monkeypatch, parent, reason):
    def fake(path, params=None):
        if path.endswith("/ultimate-parent"):
            return parent
        if path.endswith("reporting-exception"):
            return {"data": {"attributes": {"reason": reason}}} if reason else None
    monkeypatch.setattr(apis, "_gleif", fake)


def test_non_consolidating_fills_the_ultimate_parent_unless_switched_off(monkeypatch):
    _gleif(monkeypatch, None, "NON_CONSOLIDATING")
    monkeypatch.setenv("RULES_OFF", "gleif_non_consolidating")
    f = apis.gleif_parent("X" * 20)
    assert f.value is None and f.note == "reporting exception: NON_CONSOLIDATING"
    monkeypatch.setenv("RULES_OFF", "zero_from_total")
    f = apis.gleif_parent("X" * 20)
    assert f.value == apis.NO_CONSOLIDATING_PARENT and f.confidence == "A"
    _gleif(monkeypatch, None, "NON_PUBLIC")
    assert apis.gleif_parent("X" * 20).value is None
    _gleif(monkeypatch, None, "NATURAL_PERSONS")
    assert apis.gleif_parent("X" * 20).value == "none (top of group)"
    _gleif(monkeypatch, {"data": {"id": "P" * 20, "attributes": {"entity": {"legalName": {"name": "Parent AG"}}}}},
           None)
    assert apis.gleif_parent("X" * 20).value == "Parent AG"


def test_refresh_asks_gleif_for_an_empty_ultimate_parent_only_when_told_to():
    rows = [_row("a", "lei", "X" * 20), _row("a", "ultimate_parent", "", note=MISSING),
            _row("a", "controlling_owner", "", note=MISSING)]
    asked = []

    def lookup(lei):
        asked.append(lei)
        return Found("ultimate_parent", apis.NO_CONSOLIDATING_PARENT, source="GLEIF level 2",
                     method="API", confidence="A", note="reporting exception: NON_CONSOLIDATING")
    dp.refresh(rows)
    assert not asked and _by(rows)["ultimate_parent"]["value"] == ""
    dp.refresh(rows, lookup)
    by = _by(rows)
    assert by["ultimate_parent"]["value"] == apis.NO_CONSOLIDATING_PARENT
    assert by["ultimate_parent"]["source"] == "GLEIF level 2"
    # never read as "no controlling owner"
    assert by["controlling_owner"]["value"] == "" and by["controlling_owner"]["note"] == MISSING


def test_an_exception_without_a_value_leaves_its_reason_in_the_note():
    rows = [_row("a", "lei", "X" * 20), _row("a", "ultimate_parent", "", note=MISSING)]
    dp.refresh(rows, lambda lei: Found("ultimate_parent", None, note="reporting exception: NON_PUBLIC"))
    up = _by(rows)["ultimate_parent"]
    assert up["value"] == "" and up["note"] == MISSING + "; GLEIF reporting exception: NON_PUBLIC"


# --- A2: ownership from largest_holders --------------------------------------------------------

def _owners(holders):
    lh = _row("a", "largest_holders", holders, note='4 holder(s) as listed; PDF page 9: "..."')
    lh.update(source="Annual report (PDF)", endpoint="https://x/ar.pdf#page=9", confidence="B",
              period_end="2025-12-31")
    return [lh, *(_row("a", k, "", note=MISSING) for k in
                  ("controlling_owner", "controlling_owner_name", "ownership_type", "pe_stake_5pct"))]


def test_no_holder_of_20_percent_is_widely_held_with_no_owner_to_name():
    rows = _owners("BlackRock, Inc. 7.13%; FMR LLC 4.9%; Norges Bank 2.99%")
    dp.refresh(rows)
    by = _by(rows)
    assert by["controlling_owner"]["value"] == "none"
    assert by["ownership_type"]["value"] == "widely_held"
    assert by["ownership_type"]["method"] == "DERIVED"
    assert by["ownership_type"]["endpoint"] == "https://x/ar.pdf#page=9"
    assert "BlackRock, Inc. 7.13%" in by["ownership_type"]["note"]
    assert by["controlling_owner_name"]["note"] == dp.NO_CONTROLLING_OWNER
    assert by["pe_stake_5pct"]["value"] == ""        # a 7% holder: its type is unknown


def test_groups_of_holders_are_not_holders():
    # "Institutional 60.19%" is many holders: the largest single one is 12.59%
    rows = _owners("Institutional 60.19%; Sparkassen Beteiligungs GmbH 12.59%; Erste Foundation 6.08%; "
                   "Retail 5.63%")
    dp.refresh(rows)
    assert _by(rows)["ownership_type"]["value"] == "widely_held"


def test_a_holder_of_20_percent_or_more_is_named_but_not_typed():
    rows = _owners("Marwyn Investment Management LLP 59.11%; Nicholas E Gardner 12.45%")
    dp.refresh(rows)
    by = _by(rows)
    assert by["controlling_owner_name"]["value"] == "Marwyn Investment Management LLP"
    assert by["controlling_owner"]["value"] == "" and by["ownership_type"]["value"] == ""


def test_every_stake_under_5_percent_means_no_pe_stake():
    rows = _owners("Schroders plc 4.99%; Mawer Investment Management Ltd. 4.99%; Norges Bank 2.98%")
    dp.refresh(rows)
    assert _by(rows)["pe_stake_5pct"]["value"] == "no"


def test_one_holder_or_no_stakes_settles_nothing():
    for holders in ("Rob Perrins 3.172%", "Folketrygdfondet; Regin Jacobsen; Oddvør M. Jacobsen"):
        rows = _owners(holders)
        dp.refresh(rows)
        assert all(r["value"] == "" for r in rows[1:]), holders


def test_a_value_already_read_is_kept():
    rows = _owners("BlackRock 7%; FMR 5%")
    rows[1].update(value="family", note="")
    rows[3].update(value="family_owned", note="")
    dp.refresh(rows)
    assert _by(rows)["controlling_owner"]["value"] == "family"
    assert _by(rows)["ownership_type"]["value"] == "family_owned"


# --- A3: a part of the total that must be 0 ----------------------------------------------------

def _pay(**amounts):
    rows = [_role(k, v) for k, v in amounts.items()]
    have = set(amounts)
    rows += [_role(k, "") for k in ("benefits_value", "pension_contribution", "sti_paid",
                                    "lti_vested", "lti_granted") if k not in have]
    return rows


def test_benefits_and_pension_are_0_when_the_total_is_the_other_parts(monkeypatch):
    rows = _pay(base_salary="500000", sti_paid="200000", lti_vested="100000", total_remuneration="800000")
    dp.refresh(rows)
    by = _by(rows)
    for k in ("benefits_value", "pension_contribution"):
        assert by[k]["value"] == "0" and by[k]["method"] == "DERIVED" and by[k]["unit"] == "EUR"
        assert "the stated total 800,000 = base_salary 500,000 + sti_paid 200,000 + lti_vested 100,000" \
            in by[k]["note"]


def test_no_zero_when_the_total_holds_more_or_the_rule_is_off(monkeypatch):
    rows = _pay(base_salary="500000", sti_paid="200000", total_remuneration="710000")   # 1.4% more
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["value"] == ""
    monkeypatch.setenv("RULES_OFF", "zero_from_total")
    rows = _pay(base_salary="500000", sti_paid="200000", total_remuneration="700000")
    dp.refresh(rows)
    assert _by(rows)["pension_contribution"]["value"] == ""


# --- A4: pay currency ------------------------------------------------------------------------

def test_an_empty_pay_currency_is_the_currency_of_the_roles_amounts():
    rows = [_role("pay_currency", "", role="CEO"), _role("base_salary", "100", "CHF", role="CEO"),
            _role("pay_currency", "", role="Other members"),
            _role("pay_currency", "CHF", "", role="CFO")]
    rows[-1]["unit"] = ""
    dp.refresh(rows)
    ceo, other = rows[0], rows[2]
    assert ceo["value"] == "CHF" and ceo["note"] == "derived: the currency of the role's amounts"
    assert other["value"] == "CHF" and "other roles" in other["note"]


def test_mixed_currencies_settle_nothing():
    rows = [_role("pay_currency", ""), _role("base_salary", "100", "CHF"), _role("sti_paid", "5", "EUR")]
    dp.refresh(rows)
    assert rows[0]["value"] == ""


# --- A5: a role paid nothing ----------------------------------------------------------------

def test_a_stated_total_of_0_makes_the_empty_amounts_not_applicable():
    rows = _pay(total_remuneration="0")
    dp.refresh(rows)
    assert all(r["note"].startswith("not applicable: no pay for the year")
               for r in rows if r["data_point"] != "total_remuneration")


# --- A6: share prices in pence and cents, and the market-cap band ---------------------------------

def test_hundredths_of_a_currency():
    assert dp.price_in_hundredths("GBp") == "GBP" and dp.price_in_hundredths("pence") == "GBP"
    assert dp.price_in_hundredths("p") == "GBP" and dp.price_in_hundredths("USD cents") == "USD"
    assert dp.price_in_hundredths("GBP") is None and dp.price_in_hundredths("EUR") is None


def _price(value, unit, note=""):
    r = _row("a", "share_price", value, note=note)
    r.update(unit=unit, period_end="2025-12-31")
    return r


def test_a_price_in_cents_becomes_its_currency_and_the_band_follows(monkeypatch):
    monkeypatch.setattr(dp.fx, "eur_rate", lambda cur, date: (1.1, "2025-12-31"))
    shares = _row("a", "shares_outstanding", "353000000")
    band = _row("a", "market_cap_band", "", note="not derived: market cap 43,164,209,095 USD cents; "
                                                 "no ECB euro rate for USD cents on 2025-12-31")
    rows = [shares, _price("122.1", "USD cents"), band]
    dp.refresh(rows)
    assert rows[1]["value"] == "1.221" and rows[1]["unit"] == "USD"
    assert rows[1]["note"].endswith("printed 122.1 USD cents")
    assert band["value"] and band["method"] == "DERIVED"


def test_a_price_the_page_prints_in_cents_is_divided_once():
    rows = [_price("2325", "ZAR", note='web page: "Last price | 2325 ZAR cents"')]
    dp.refresh(rows)
    dp.refresh(rows)
    assert rows[0]["value"] == "23.25" and rows[0]["unit"] == "ZAR"


def test_no_band_from_a_price_over_a_year_from_the_year_end():
    chosen = {"shares_outstanding": Found("shares_outstanding", 5_800_000_000),
              "share_price": Found("share_price", 1.4065, unit="EUR", period_end="2023-12-31"),
              "fiscal_year_end": Found("fiscal_year_end", "2025-12-31")}
    band, why = dp.market_cap_band(chosen)
    assert band is None and "over a year" in why
