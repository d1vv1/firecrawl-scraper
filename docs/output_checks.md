# Output checks

*3 November 2026. Script: `extractor/output_checks.py`, tests: `tests/test_output_checks.py`.*

`docs/allshares_part1_validation.html` scored 50 companies against a set of checks ("Part 1 gates"), but it is a page of results with no script behind it. These checks are now code. Run them on any data-point CSV:

```
python -m extractor.output_checks output/nordic_uk_10_datapoints.csv
python -m extractor.output_checks run.csv --out output/run_checks --ranges ranges.json
```

This writes `<name>_checks.md`, the report, and `<name>_checks.csv`, with one row per value and check. The check IDs follow the HTML page so the results can be compared.

## What changed from the HTML page

| On the page | Here |
|---|---|
| A check that couldn't run made the value "Incomplete" (39% of values) | It is "n/a" with a reason and doesn't count. Plausible ranges have defaults (`DEFAULT_RANGES`); `--ranges` replaces them when Allshares sends its own |
| "Snippet not found" taken from the run's own grade | The quote is looked up again in the cached source document, on the linked page |
| Every value needs an as-of date (621 fails, including LEIs and names) | Only values that hold for a date or period: money, counts, breakdowns, owners, pay |
| Every LTI value failed: "form: shares" is not grant, face or realised | `lti_granted` is a grant value, `lti_vested` a realised one, and an IFRS 2 expense says so in the note (the client's golden file uses the expensed figure when that is all a report gives) |
| Exchange must be stored as a MIC code | The name stays (the protocol asks for the exchange); it must resolve to an ISO 10383 MIC, which is given in the note |
| Percentages in STI 0–100 | "% of maximum" 0–100, "% of base salary" 0–1000 (a bonus maximum of 200% of salary is normal) |
| Total vs parts within 1%, a hard fail | 2% (protocol R11), with the LTI the total includes. Parts above the total are a hard fail (XF-01): a figure misread or counted twice. A total above its parts is soft (XF-02): usually pay outside the fields, such as a one-off |
| Blank values ignored | Fill rate per field and per pay field in the report |
| Annualisation and performance-period checks | Not run: the output has no such fields |

A value's status is "Fail (hard)" if a hard check fails. Otherwise its score is the checks passed divided by the checks applied: Pass at 95% or more, Review at 80% or more, else Fail.

## The checks

| ID | Hard | What it checks |
|---|---|---|
| CORE-01 | yes | An endpoint URL; a PDF link opens at a page (`#page=N`) |
| CORE-02 | yes | The value can be read off its quote. A figure appears as printed, as a sum of the quoted cells, or scaled ("(000s)"); a name or date appears in it. Not for classifications such as owner type |
| CORE-03 | yes | The quote is in the cached source text, on the linked page (or the page before it) |
| CORE-04 | | Dated values have a `period_end` |
| CORE-05 | | Numbers are numbers, dates are dates, breakdowns read "name: number; …" |
| COD-01 | yes | ISO 3166 country, ISO 4217 currency, ISO 10383 exchange, the closed sets (listing status, owner type, ownership type, PE stake, role disclosure, cap band), target units, a NACE code in the NACE Rev. 2 list |
| COD-02 | | The industry code names its scheme (NACE, SIC…) |
| COD-03 | yes | LEI (ISO 17442) and ISIN check digits |
| COD-06 | yes | Fiscal year end and listing date are valid dates |
| NUM-01 | yes | Money has an ISO currency |
| NUM-02 | | A scaled figure keeps the number and unit as printed |
| NUM-04 | | Magnitude in a plausible range |
| NUM-05 | yes | Counts are whole numbers |
| NUM-06 | yes | Stakes and "% of maximum" 0–100, "% of base salary" 0–1000 |
| NUM-07 | yes | Holdings add up to 100% or less |
| NUM-08 | | A breakdown adds up to revenue or headcount within 5% |
| NUM-09 | | An LTI amount says what it measures: granted, vested, or expensed (IFRS 2) |
| NUM-11 | | STI paid is not above its maximum (as % of base salary) |
| NUM-12 | | A role's amounts share one currency and period |
| NUM-13 | | FTE not above headcount (+10%) |
| DER-03 | yes | A derived value recalculates from the inputs in its note |
| DER-06 | | A derived value shows its formula |
| XF-01 | yes | The parts are not more than the stated total (2%) |
| XF-02 | | The stated total equals its parts within 2% |

Limits:
- The quotes in the output notes are cut at 160 characters. A figure past the cut can't be checked against the quote (CORE-02 is n/a then), and only the start of the quote is looked up (CORE-03).
- CORE-03 needs the run's cache (`--cache`, `--results`). Without it the check is n/a, unless the run itself flagged the quote as not found.

## Results: Nordic/UK test set, 5 November 2026 (run 21, saved results refreshed)

726 filled values: **683 Pass (94%), 12 Review, 1 Fail, 30 Fail (hard)**. No source was asked again. Six more values: the market-cap band for the six non-EUR companies with a share price, now converted at the ECB rate (BioArctic, Equinor, Novo Nordisk, Shell, Volvo large; Bang & Olufsen mid). Pay terms and ownership facts read without a date now carry one (the pay year, the report's year end, or the day a web page was read), which also passes CORE-04. Company-field fill rate: 82%. On the dashboard, found rose from 67% to 75% (35 values are not applicable, such as a group headcount on one person's row, and no longer count as missing) and partial values fell from 44 to 3.

## Results: Nordic/UK test set, 4 November 2026 (run 21)

720 filled values: **672 Pass (93%), 17 Review, 1 Fail, 30 Fail (hard)**. Golden pay unchanged at 120 of 148. The new sector codes (issue 7) pass COD-01/02. The extra hard fails come from AI answers that changed between runs, not from the new code: the changed description prompt made the report pass ask every field again. Shell's EBITDA and owner quotes, AO World's listing date, and a third Bang & Olufsen executive whose parts exceed the total (its bonus definition, issue 10) are new. Nokia's shares-outstanding quote and the Volvo pay quotes were already flagged.

## Results: Nordic/UK test set, 3 November 2026

10 companies, 716 filled values (`output/nordic_uk_10_checks.md`): **675 Pass (94%), 14 Review, 1 Fail, 26 Fail (hard)**. Fill rate of the company fields: 80%.

The quote check agrees with the run's own grading. Every value the run graded B because its quote was found passes CORE-03, and the 21 quotes that fail are all values the run itself graded C.

The first run of the checks found 46 hard fails among 710 values. Fixed since (`docs/known_issues.md`, issue 12):
- **A target in another unit.** "200% of target" is now its own form, turned into % of base salary in code.
- **Figures the AI worked out.** The prompts forbid them, and code grades a figure that isn't in its quote C. Code now subtracts treasury shares itself.
- **Bad breakdowns and websites.** Percentages aren't given as breakdowns, and a website must be in its quote.
- **Names cut across table cells.** Quotes with such names are now found.
- **Two checks were wrong.** An expensed LTI is the client's own basis, and a total above its parts is noted rather than failed.

Fixed in the output while building the checks:
- **Period ends.** A dated value from the annual report (EBITDA, breakdowns, shareholders and owners) takes the report's period end when the AI gave no other date. Pay-currency rows have their period too.
- **Exchanges.** An exchange name read from a document carries its MIC in the note ("MIC XSTO"). First North and other growth markets resolve by the company's country.
- **Pay notes.** Large figures were printed in scientific notation ("printed 1.05788e+06"), losing digits. They are now written in full.
