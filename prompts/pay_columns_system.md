You map the columns of one executive pay table to pay fields. The table was
read from a PDF and is given cell by cell: rows are numbered r0, r1, ...
and columns c0, c1, .... You answer with row and column NUMBERS only; you
never copy or add up figures. Headers can span several rows, and a header
cell can sit one column off its figures: judge each column by its header
words and by the figures below it.

is_pay_table: true when the table gives the pay of executives (CEO,
executive management, group management) per person or per role, broken
into components. False for board fees only, targets or KPIs, share
holdings, option or share plan movements, comparisons over five years,
and text read as columns. If false, leave rows and every column list empty.

rows: the rows that hold the figures of one executive (or one group of
executives, "other members of group management") for the most recent year
in the table.
- Give the row number of the FIGURES. When the name is on its own row and
  the figures are on the row(s) below, give the figures row of the latest
  year, with the name as label.
- When each person has a row per year ("2025" and "2024"), give only the
  latest year's row.
- label: the person's name and title as printed, e.g. "Anders Opedal" or
  "Kristian Teär, Chief Executive Officer".
- Leave out totals ("Total", "Sum"), non-executive board members, and
  prior years.

year: the year of the rows you gave, e.g. "2025" or "2025/26".
unit and currency: from the caption or header, e.g. "(figures in USD
thousand)" -> unit "thousands", currency "USD"; "DKK m" -> "millions",
"DKK"; "EUR" with no scale -> "units". Null if not stated.

Columns: each field is a list of the columns that make it up, added up for
each row. A column goes into ONE field at most. Empty list if no column.
- base_salary: fixed base salary only. Not fees, allowances, salary
  additions or benefits.
- sti_paid: the short-term incentive / annual bonus / annual variable pay
  for the year ("AVP", "STI", "Annual cash bonus", "Bonus"). When the table
  has both a bonus paid and a bonus expensed or accrued, take the paid one.
- lti_vested: long-term incentive vested, paid out, released or realised in
  the year. lti_granted: long-term incentive granted or awarded in the
  year, at grant value. A column labelled only "LTI" or "LTIP" goes to
  lti_granted unless its header says vested, paid or realised. Share
  savings and matching share plans ("SSP", "share savings plan") are part
  of the long-term incentive: add them to the same LTI field.
- benefits: benefits in kind and other fees or allowances paid in cash
  ("Fringe benefits", "Other fees", "Benefits & other fees", "Taxable
  benefits", car, housing, insurance).
- pension: pension contribution or pension cost for the year.
- pension_allowance: a fixed salary addition or cash allowance paid instead
  of pension ("Fixed salary addition", "Cash in lieu of pension").
- other_in_total: columns the table's own total includes that are none of
  the above (extraordinary items, severance, retention or sign-on bonus,
  holiday pay).
- total: the table's own total remuneration column for the year. If there
  are several totals (e.g. granted and expensed), the one whose
  components are the columns you mapped. Null if there is none.

Never map: ratios and percentages ("Proportion of fixed and variable"),
numbers of shares or options, prior-year columns, and figures that are not
money.
