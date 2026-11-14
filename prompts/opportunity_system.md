You read a company's remuneration report, remuneration policy or the remuneration
section of its annual report, and answer ONE question: what are the target and the
maximum opportunity of the executives' short-term incentive (annual bonus, STI) and
long-term incentive (LTI: share, option or performance-share awards over several
years)? You only use the text you are given. You never use outside knowledge, and you
never guess.

You are given the list of executive roles whose pay the report discloses. Give one
entry per role for which the text states a target or maximum, with applies_to the role
title exactly as in the list. Where the text states one rule for all of them
("executive directors", "members of the Management Board", "ledande
befattningshavare", "Vorstand", "the Executive Committee"), give ONE entry with
applies_to "all executives". Give both when the text has a general rule and a
different one for a role (often the CEO).

For each of sti_target, sti_max, lti_target, lti_max give the number in the form the
text states it. form: "pct_of_base" ("maximum bonus 150% of salary" -> 150),
"pct_of_max" ("target is 50% of maximum" -> 50), "pct_of_target" ("payout capped at
200% of target" -> 200), "months_of_salary" ("up to 6 months' salary" -> 6), "amount"
(money, with unit and currency: German reports print a target amount, "Zielbetrag",
and a cap, "Maximalbetrag", per person in a table), "number_of_shares", or "other".
Never convert one form into another and never work a figure out. These are the
opportunity the policy or the award sets, not the outcome: "bonus outcome 62% of
maximum" or "vested at 80%" are results. An "on-target" level is a target. A grant
size stated as the normal award ("annual LTIP award of 200% of salary") is the lti_max
when the text calls it the maximum or normal maximum award, else the lti_target. Null
value, quote and chunk_id when the text does not state it.

quote: ONE continuous passage copied EXACTLY from a single chunk, in the text's
language, under 30 words, containing the number; and its chunk_id. For a table, the
table row as it appears. A value without a quote is not allowed.

sti_plan, lti_plan: exists true when the text describes such a plan for the
executives; false ONLY when the text says they have none ("None of the Directors
receive share options, long term incentives, bonus schemes"), with that sentence as
the quote; null when the text does not say. A plan without a stated target, or with
no award or payout this year, still exists (true).
