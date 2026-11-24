## This request: only some roles

The message lists, under "Roles to extract", the roles this request is
about: each with its meaning and the titles reports use for it, in the
report's languages and English. Give a line only for a person or group in
one of those roles, with every pay field defined below. Leave out every
other line.

Roles are often hard to find in pay tables:
- Read every row label of every pay table, and the page images where they
  are attached; a role's row may use a title not in the list, an
  abbreviation, or only a person's name with the function given elsewhere
  (a heading, a footnote, the board or management presentation). Use the
  text's own words to tie a name to its function.
- One table often mixes roles (the CEO and the other executives; the chair
  and the members). Give each wanted row; skip the others.
- A former holder of a wanted role (left or joined during the year) is
  wanted too: the same role, part of the year.
- If the text says a wanted role exists but does not give its pay
  separately (e.g. the CFO's pay is in the group management total), give a
  line with role_disclosure "not_disclosed", all pay fields null and the
  sentence that says so as the quote.

The message also lists, under "Not these roles", titles of other roles that
look similar ("Vice VD" is a deputy CEO, not the CEO; "Vice Chair" is not
the chair). A line in one of those roles is left out.

`suggested_role_detail` is still given for every line you return.
