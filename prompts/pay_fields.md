<!-- One section per pay field. The prompt builder (extractor/pay_roles_prompts.py) copies
only the sections a request asks for into the system prompt, under "## Pay fields". A section
starts at its "### <field>" heading and ends at the next one. Keep the headings exactly equal
to the field names in extractor/pay_roles_schema.py FIELDS. -->

### base_salary
The fixed base salary for the year. For a board member, chair or other
non-executive: the board fee (the basic fee for sitting on the board,
including the chair's or vice chair's fee); committee fees go to
`committee_fees`. Leave out benefits, holiday-pay adjustments, allowances
and salary additions (e.g. a fixed salary addition paid instead of
pension): those belong to benefits or pension_allowance, or nowhere. Only
if the table gives no separate base figure, give the combined one and name
what it includes in `includes`.

### committee_fees
For a board member: the fees for board committee work (audit,
remuneration, nomination or other committee), as one printed figure. If
the table gives one column per committee and no total, give null and say
so in `includes`; never add them up.

### meeting_fees
For a board member: fees paid per board or committee meeting attended
(Finnish "kokouspalkkiot", Swedish "mötesarvode"), as one printed figure;
null if the table has none.

### benefits
The value of other benefits for the year (car, insurance, housing,
benefits in kind), as printed.

### pension
The pension contribution or cost for the year, as printed.

### pension_allowance
A fixed salary addition or allowance paid instead of (or in compensation
for) pension, when the table shows it as its own column (Norway: "fixed
salary addition"). Never add it to pension or base salary. A column called
only "Pension" is pension, not pension_allowance, even when paid in cash.

### sti_paid
The short-term incentive / annual bonus for the year, as the table gives
it in one figure, whether paid in cash or deferred into shares. Where the
table gives the year's bonus in two columns, a cash part and a deferred
part ("Annual bonus – cash", "Annual bonus – deferred"), sti_paid is the
cash column and sti_deferred the deferred one. Never add them.

### sti_deferred
The part of the year's annual bonus that is deferred (into shares, or cash
paid later), only when the table shows it as its own column next to the
cash part, as an amount of money; say in `includes` how it is deferred.
Null when the bonus is one figure, also when a note says how much of that
one figure is deferred: that amount is already in sti_paid. Not a
long-term incentive, and not an earlier year's deferred bonus vesting now.

### lti_vested
The long-term incentive that vested, was paid out or was exercised for the
year (the value realised). If the report gives only one LTI figure, put it
where its label says (vested/paid/realised -> lti_vested;
granted/awarded/allocated -> lti_granted). `form`: "cash", "shares",
"options", "number_of_instruments" (a number of shares or options, not
money: then `unit` "units" and `currency_printed` null),
"accounting_expense" (IFRS 2 cost) or "other".

### lti_granted
The long-term incentive granted (awarded) in the year, at its grant value
as printed. Reports often give both vested and granted: fill both. `form`
as for lti_vested.

### other_pay
A component the table puts into the total that is none of the fields
above (e.g. travel allowance, sign-on or severance pay, a holiday-pay
adjustment, "other remuneration"), as one printed figure; say in
`includes` what it is. If there are several such columns and no subtotal,
give the largest and name the others in `includes`; never add them.

### total
The total remuneration as the company states it. Never add it up yourself;
null if the table has no total. If the table gives two totals for the
same person, one with long-term incentives at their initial grant (award)
value and one at their value at vesting, give the one at grant value and
name the other, with its figure, in `includes`.

### sti_target
The target short-term incentive opportunity for this role, in the form the
report or policy states it. `form`: "pct_of_base" (target bonus 60% of base
salary -> 60), "pct_of_max" (target is half of the maximum -> 50),
"pct_of_target", "months_of_salary" (6 months' salary -> 6), "amount"
(money: with unit_printed and currency_printed), "number_of_shares", or
"other". Give the number as stated; never convert one form into another.
This is the opportunity the policy sets, not the outcome: "STIP outcome
24.4% of maximum" is a result, not a target. Null if not stated.

### sti_max
The maximum short-term incentive opportunity, as for sti_target
("maximum bonus 200% of target" -> 200, pct_of_target).

### lti_target
The target long-term incentive opportunity (award level at target), as for
sti_target ("annual award of 100% of base salary" -> 100, pct_of_base).
"Vested at 62%" is a result, not a target.

### lti_max
The maximum long-term incentive opportunity, as for sti_target.
