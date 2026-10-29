# Plan: reading executive pay tables reliably

*26 October 2026. Status: **built 29 October 2026** (`extractor/pay_tables.py`, `prompts/pay_columns_system.md`, `tests/test_pay_tables.py`); results and what changed from this plan are in `docs/known_issues.md`, issue 2. Related: issues 2 (merged table columns) and 5 (run-to-run variation).*

**Changed from the plan while building it:**
- The mapping call sees the whole small grid with row and column numbers, not just the header row. Real tables spread headers over several rows and put names on their own row, and code can't find the header and data rows reliably. Code adds each column's joined header words and the page text (for the caption, year and unit).
- The table route doesn't replace the pay AI call. That call still runs and gives role titles, targets, maxima and company terms; the table replaces only the amounts of the roles it matches.
- A table needs a total column. Without one nothing checks the mapping, so it isn't used.
- Results: 118, 120 and 120 of 148 over three fresh runs. That is close to the same score every time, but just under the 121 target; the spread left is Bang & Olufsen, whose table has no total column.

## In short

Today one AI call does two jobs at once:

1. it **reads** the pay table (which number sits in which column), and
2. it **decides what the columns mean** for our fields (is "Other fees" part of benefits?).

It does both badly from run to run. We split the work: a table library reads the table with no AI; the AI answers only one small question ("which columns make up which of our fields?"); then plain code adds up the numbers. Every number then comes straight from the printed table, and the one judgement left is small, reviewable and repeatable.

## Background: what this part of the pipeline does

For each listed company we collect executive pay **per role**: CEO, CFO, other executives. For each role we fill 14 fields: base salary, bonus paid (STI), long-term incentive (LTI), benefits, pension, total and others (see `pay.ROLE_POINTS`, protocol fields R01–R11).

The numbers come from the company's **remuneration report**, usually a PDF, which has one or more pay tables like this (Equinor 2025, page 15, USD thousand):

| Member | Base salary | Fixed salary addition | Other fees | Fringe benefits | AVP | LTI | SSP | Extraordinary items | Pension expense | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Anders Opedal | 1,242 | 224 | 96 | 23 | 292 | 306 | 0 | 0 | 30 | 2,213 |
| Irene Rummelhoff | 543 | 98 | 59 | 11 | 121 | 134 | 0 | 0 | 32 | 997 |

**How it works today** (`extractor/pay.py`, `ask_pay`; called from `datapoints.from_pay`):

1. The PDF is converted to text with **pymupdf4llm**, which writes tables as markdown (`| a | b | c |`).
2. The pages about pay are picked by keywords, up to about 12,000 words.
3. **One Gemini call** gets that text and returns every role with every field filled in, plus a short quote for each value.
4. We search for the quote in the text to prove the value and find its page (`#page=15`). Found: grade B. Not found: grade C.
5. Code converts units ("USD thousand" × 1,000) and checks that the parts add up to the stated total (2% tolerance).

## The problem

A PDF has no real tables in it, only pieces of text placed at x/y positions on the page. Anything that turns a PDF into a table has to **guess** where the columns are. On top of that, the report's columns never match our fields one to one. So two different things go wrong.

### Problem A: reading (which number is in which column)

When columns are close together or headers span several lines, pymupdf4llm guesses wrong. Equinor's row comes out as:

```
| Anders Opedal | 1,242 | 224 | 96<br>23 | 292 | 306 | 0 | 0 | 30 | 2,213 |
```

"Other fees" (96) and "Fringe benefits" (23) are merged into one cell, so every column after it is off by one. The AI sometimes untangles this and sometimes doesn't.

### Problem B: interpretation (which columns make up our field)

Even with a perfect table, someone has to decide:

| Our field | Equinor columns that belong to it | Why it's a judgement |
|---|---|---|
| benefits | Other fees **+** Fringe benefits | Is a car allowance a "benefit" or a "fee"? |
| pension | Pension expense **+** Fixed salary addition | The addition is paid *instead of* pension |
| LTI | LTI **+** SSP (share savings plan) | Is a share savings match long-term pay? |
| STI | AVP (annual variable pay) | The name differs per company |

Today the AI makes these decisions again, from scratch, on every run, and doesn't always decide the same way.

### Evidence (all on Equinor's table, scored against the printed figures, 91 per run)

| What the AI was given | 5 runs | What went wrong |
|---|---|---|
| Today's markdown only | 67, 91, 91, 67, 84 | both A and B |
| Markdown + correct table from **Camelot** | 86, 91, 86, 73, 86 | only B: SSP left out of LTI, "Other fees" left out of benefits |
| Markdown + **image** of the page | 91, 91, 91, 91, 91 | none on one page, but full 10-company runs swung 109–121 depending on the instruction wording |

Across all 10 test companies, the golden pay match moved from **98 to 121 of 148 on identical input**, depending only on what the AI happened to answer.

**Conclusion:** fixing the reading (Camelot, images) is not enough. As long as the AI also decides the meaning of columns in the same call, results stay unstable.

## The plan: split reading from interpretation

```
 PDF page with a pay table
        │
        ▼
 1. READ      Camelot extracts the grid: headers, rows, numbers         no AI, deterministic
        │
        ▼
 2. MAP       Gemini sees ONLY the header row and answers:              small AI call, saved
              "which columns make up which of our fields?"              and reviewable
        │
        ▼
 3. ADD UP    Code takes each person's row and adds the mapped          no AI
              columns, applies the unit, writes the role rows
        │
        ▼
 4. CHECK     Parts vs total (2%); the quote is the row itself,         no AI
              so every value is grade B with its page
```

If any step fails (no table found, the mapping doesn't fit, the numbers don't add up), we **fall back to today's method** for that document. Nothing is lost.

### Step 1: read the table (no AI)

- **Tool:** Camelot, `flavor="stream"`. It finds columns from the gaps between text; "lattice" mode needs ruled lines, and these tables have none. Tested on Equinor: all 12 columns right, 0.2 s per page. New dependencies: `camelot-py` and `opencv-python-headless`. An alternative worth a quick test is PyMuPDF's built-in `page.find_tables()`, which needs no new dependency.
- **Which pages:** the pages the pay step already selects that look like pay tables (many numbers, pay words). `pay.table_pages` does this today.
- **Clean-up:**
  - **Multi-line headers.** Camelot puts "Fixed salary" and "addition" on two rows; join the header rows above the first data row, column by column.
  - **Name on one row, figures on the next.** Join a name row (mostly empty cells) to the row below it, as Bang & Olufsen's report does.
  - **Two years in one table** ("2025" and "2024" rows per person, as at Bang & Olufsen and Volvo). Keep the report year's rows only.
  - **Two tables side by side on one page.** Camelot joins them into one wide table; the mapping step must be told this can happen.
- **Output:** a small structure per table: header list, rows (label + cells), page number, and the unit if printed ("figures in USD thousand").

### Step 2: map the columns (one small AI call per table)

The AI gets only the headers, one example row and the table's caption, e.g.:

```
Table: "Remuneration of the corporate executive committee for the reported financial year 2025
        (figures in USD thousand)"
Columns: 0 Member | 1 Base salary | 2 Fixed salary addition | 3 Other fees | 4 Fringe benefits |
         5 AVP | 6 LTI | 7 SSP | 8 Extraordinary items | 9 Pension expense | 10 Total remuneration |
         11 Proportion of fixed and variable
Example row: Anders Opedal | 1,242 | 224 | 96 | 23 | 292 | 306 | 0 | 0 | 30 | 2,213 | 73% / 27%
```

It answers in a fixed schema:

```json
{
  "name_column": 0,
  "unit": "thousands", "currency": "USD", "year": "2025",
  "fields": {
    "base_salary":       [1],
    "pension_allowance": [2],
    "benefits":          [3, 4],
    "sti_paid":          [5],
    "lti_granted":       [6, 7],
    "pension":           [9],
    "total":             [10]
  },
  "ignored": {"8": "extraordinary items, 0", "11": "a ratio, not an amount"}
}
```

- **Written rules in the prompt** decide the judgement calls the same way every time. These are the client's definitions (issue 10). Until the client confirms, we use what the golden file implies:
  - **Benefits:** benefits in kind, allowances and "other fees" count as benefits.
  - **Pension:** cash paid in lieu of pension counts as pension.
  - **LTI:** share savings and matching plans count as LTI.
  - **STI:** any annual bonus or variable pay is STI.
  - **Never mapped:** ratios, percentages and share counts.
- **Saved per table** (cache key: the header text). The same headers give the same mapping on every run, and a person can read and correct it in the cache file.
- **Small:** a few hundred tokens instead of about 30,000 per pay call today.

### Step 3: add up (code)

For each data row: field value = sum of its mapped cells, parsed as numbers (handling "1,242", "1 242", "1.242", "–" and "0"), times the unit (thousand → × 1,000). Role title and person name come from the name column; the existing title logic (`pay.role_found`) decides the role.

### Step 4: check and quote (code)

- **Total check:** the mapped parts must add up to the table's own total column, within 2%. If they don't, the mapping is probably wrong, so drop it and fall back to today's method for this document.
- **Quote:** the person's row as printed, so the quote lookup finds it on that page and the value gets grade B.
- **Method label:** `PARSE`, with a note such as "table on page 15; benefits = Other fees + Fringe benefits", so a reviewer sees exactly which columns were added.

### What stays as it is

- Finding the remuneration report, SEC exhibits, the year check, the remuneration policy for targets, aggregates from the annual report: all unchanged (`datapoints.from_pay`).
- **Targets and maxima** ("STI target 125% of salary") usually sit in prose, not tables, so they keep coming from today's AI read.
- **Fallback:** pay given only in sentences, scanned tables, or a table that fails step 1 or 4 goes through today's AI call (`pay.ask_pay`). Optionally with the page image (`PAY_PAGE_IMAGES=1`, built and off by default).

## Where the code goes

| Change | File |
|---|---|
| Find and clean the table (Camelot, header join, name-row join, year filter) | new `extractor/pay_tables.py` |
| Mapping prompt | new `prompts/pay_columns_system.md` |
| Mapping schema (`ColumnMap`) | `extractor/schemas.py` |
| Add up rows into `RolePay` objects, then reuse `pay.role_found` | `extractor/pay_tables.py` |
| Try the table route first, fall back to `ask_pay` | `extractor/datapoints.py`, inside `from_pay` |
| Tests: Equinor, Bang & Olufsen and Volvo table layouts as fixtures; mapping rules; fallbacks | new `tests/test_pay_tables.py` |

## How we'll know it works

1. **Unit tests** on saved table layouts (no network, no AI).
2. **Golden check** on the 10 Nordic/UK companies: `output/golden_uk_nordics_check.md`. Today it scores 98–121 of 148 depending on the run.
3. **Three fresh runs** of the same 10 companies. Success means:
   - the score is the **same all three times** (the main goal), and
   - it's **at least 121**, the best today's method has managed.
4. **Coverage count:** how many of the companies' pay tables went through the table route vs the fallback. If most fall back, the route isn't worth its complexity.

## Effort and risks

- **About one day** to build and test on the 10 companies, plus half a day if PyMuPDF `find_tables()` is compared with Camelot.
- **Risk: tables Camelot can't split** (very tight columns, rotated pages). The fallback covers them; the coverage count tells us how common they are.
- **Risk: wrong mapping applied consistently.** A wrong rule is now wrong *every* time, not sometimes. That's easier to spot and fix (one rule, visible in the note and the cache), but it has to be reviewed. The total check catches many such errors.
- **Risk: every company's pay data changes once**, when the new route replaces old answers. Expected; the golden check is the safety net.

## Open questions for the client

1. Do **share savings / matching plans** count as LTI?
2. Do **"other fees"** and cash allowances count as benefits?
3. Does a **cash payment in lieu of pension** count as pension?
4. **Base salary:** salary alone, or salary plus benefits (issue 10)?

Until they answer, we use yes for 1–3 (what their golden file implies, e.g. Equinor's LTI = LTI + SSP) and salary alone for 4 (the client's earlier decision, although BioArctic's golden figure includes benefits).
