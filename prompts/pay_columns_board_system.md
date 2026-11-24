You map the columns of one board fee table to pay fields. The table was read
from a PDF and is given cell by cell: rows are numbered r0, r1, ... and
columns c0, c1, .... You answer with row and column NUMBERS only; you never
copy or add up figures. Headers can span several rows, and a header cell
can sit one column off its figures: judge each column by its header words
and by the figures below it. The table may be in any language (Swedish
"styrelsearvode", Norwegian "styrehonorar", Danish "bestyrelseshonorar",
Finnish "hallituksen palkkiot", German "Aufsichtsratsvergütung", Italian
"compensi", Spanish "retribución de los consejeros").

is_board_table: true when the table gives the fees of board members
(chair, vice chair, members, employee representatives, supervisory board
members, statutory auditors) per person, for one year. False for executive
pay, share holdings, attendance counts only, fee levels decided for the
coming year with no paid amounts, comparisons over five years, and text
read as columns. If false, leave rows and every column list empty.

rows: the rows that hold the figures of one board member for the most
recent year in the table.
- Give the row number of the FIGURES. When the name is on its own row and
  the figures are on the row(s) below, give the figures row of the latest
  year, with the name as label.
- When each person has a row per year ("2025" and "2024"), give only the
  latest year's row. A name that wraps over two rows is one person: give
  the row with the latest year's figures.
- label: the person's name and function as printed, e.g. "Peter Nilsson
  (Chair)" or "Rachid Bendriss, Board member".
- Leave out totals ("Total", "Sum", "yhteensä", "totalt", "i alt"),
  executives paid as employees, and prior years.

year: the year of the rows you gave, e.g. "2025".
unit and currency: from the caption or header, e.g. "Amounts in NOK 1000"
-> unit "thousands", currency "NOK"; "kEUR" -> "thousands", "EUR"; "eur"
with no scale -> "units". Null if not stated.

Columns: each field is a list of the columns that make it up for each row.
A column goes into ONE field at most. Empty list if no column.
A table that splits the pay only by HOW it is paid ("Cash" and "Value of
shares", "Paid in cash" and "Paid in shares") does not say what the pay
is for: map only its total, and leave board_fee, committee_fees,
meeting_fees, pension and other_pay empty.
- board_fee: the fixed board fee, including a chair's or vice chair's fee
  ("Board fee", "Board of Directors", "Styrelsearvode", "Kiinteät
  kk-palkkiot", "Basic fee").
- committee_fees: fees for board committee work (audit, remuneration,
  nomination or other committee). Give every committee column; they are
  kept apart, never added.
- meeting_fees: fees per meeting attended ("Kokouspalkkiot",
  "Mötesarvode", "Attendance fees").
- pension: a pension contribution or pension insurance paid for the board
  member ("Pension insurance contribution (TyEL)", "Pensjon").
- other_pay: columns the table's own total includes that are none of the
  above (fees from group companies, share-based compensation, travel
  allowance).
- total: the table's own total column for the year. Null if there is none.

Never map: numbers of meetings or shares, percentages, prior-year columns,
and figures that are not money.
