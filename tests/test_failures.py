from extractor.failures import Failure, classify, failures, write


def row(note, value="", dp="revenue", grain="company", role_row=""):
    return {"company_id": "x", "company_name": "X AB", "country": "SE", "grain": grain,
            "role_row": role_row, "data_point": dp, "value": value, "note": note}


def test_a_value_is_no_failure():
    assert classify(row("anything", value="100")) is None


def test_notes_map_to_codes():
    cases = {
        "not collected: this run asked only for pay": Failure.NOT_COLLECTED,
        "not applicable: the company is not listed": Failure.NOT_APPLICABLE,
        "remuneration report not searched: Firecrawl is out of credits": Failure.CREDITS_EXHAUSTED,
        "not derived: no share price": Failure.DERIVATION_INPUT_MISSING,
        "not derived: market cap 121 SEK; the EUR band needs the year-end exchange rate (API step)":
            Failure.FX_RATE_MISSING,
        "not found: only an official API gives it (API step off or no LEI)": Failure.NO_IDENTIFIER,
        "no remuneration report found": Failure.REMUNERATION_REPORT_NOT_FOUND,
        "no source reached (route failed: WebsiteNotFoundError: Best website match x)":
            Failure.WEBSITE_NOT_FOUND,
        "not found in: GLEIF, ESMA FIRDS (annual-report route failed: ReportNotFoundError: none)":
            Failure.REPORT_NOT_FOUND,
        "not found in: GLEIF, company documents (none usable found)": Failure.DOCUMENTS_NOT_FOUND,
        "not found in: GLEIF, company documents (skipped: Firecrawl is out of credits)":
            Failure.CREDITS_EXHAUSTED,
        "not found in: GLEIF, Annual report (PDF), Legal notice (web page)": Failure.NOT_DISCLOSED,
        'stated only as 150% ("Maximum opportunity 150% of salary"), not as an amount':
            Failure.STATED_IN_OTHER_FORM,
        "": Failure.UNKNOWN,
    }
    for note, code in cases.items():
        assert classify(row(note)) is code, note


def test_pay_without_a_remuneration_report_says_so():
    assert classify(row("not found in: ESEF filing (filings.xbrl.org)", dp="benefits_value",
                        grain="role", role_row="CEO")) is Failure.REMUNERATION_REPORT_NOT_READ
    assert classify(row("not found in: Remuneration report (PDF)", dp="benefits_value",
                        grain="role", role_row="CEO")) is Failure.NOT_DISCLOSED


def test_old_report_is_flagged_and_report_written(tmp_path):
    rows = [row("the year the figures are for", value="2023", dp="fiscal_year"),
            row("not derived: no share price", dp="market_cap_band"),
            row("not collected: this run asked only for pay", dp="headcount")]
    codes = [f["failure_code"] for f in failures(rows, year=2025)]
    assert codes == ["WRONG_YEAR_REPORT", "DERIVATION_INPUT_MISSING", "NOT_COLLECTED"]
    run = tmp_path / "nordics_datapoints.csv"
    csv_path, md_path, fails = write(rows, run)
    assert csv_path.name == "nordics_failures.csv" and md_path.exists()
    assert "DERIVATION_INPUT_MISSING" in md_path.read_text(encoding="utf-8")
