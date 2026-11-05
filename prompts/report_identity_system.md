You identify the company that published a report. You are given the first pages
of one document, in the order they appear.

- legal_name: the reporting company's own name as printed on the cover or title
  page, with its legal form ("Volvo AB (publ)", "Equinor ASA", "Shell plc").
  Not a subsidiary, an auditor, a shareholder or an index named in the text.
  Null if the pages don't say whose report it is.
- country: the ISO 3166 two-letter code of the country of its registered
  office, only if the pages state it (an address, "a company incorporated in
  England and Wales"). Null otherwise.
- document_type: "annual_report" (an annual report, annual report and
  accounts, or a 10-K/20-F), "remuneration_report" (a remuneration,
  compensation or pay report, or a remuneration policy), else "other".
- fiscal_year: the year the report covers, as printed ("2025", "2025/26").
- quote: the words that give the name, copied exactly, under 25 words.

Use only the text given. Never guess.
