## This request: check some cells

An earlier reading of this document left some cells empty or doubtful. The
message lists them under "Cells to check", one per line, each with its
`line_ref`, the line's printed title, the field, the page where the line
was found, and why it is asked again (empty, the parts do not add up to the
stated total, a different currency, unclear role).

Answer every listed cell, and nothing else, in `cells`: the same `line_ref`
and `field`, `found` true with the value as printed (rules above, and the
field's definition below), or `found` false with `not_found_reason` saying
what the text shows instead ("the table gives no pension column", "the
CFO's pay is only in the group total"). Look on the given page first, then
in the rest of the text. `form` is the LTI form or target form for those
fields, else null. Never fill a cell by working it out from other cells.
