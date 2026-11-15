# What the run could not find: nordics_targeted_framery.csv

16 missing values in 1 of 1 companies (built 15 Nov 2026). Not asked for and not applicable rows are counted but are not failures.

## By reason

| Code | Reason | Values | Companies | What to do |
|---|---|---:|---:|---|
| `REMUNERATION_REPORT_NOT_READ` | Pay field: only the annual report was read | 10 | 1 | Supply the remuneration report in `remuneration_report_url` and re-run the field |
| `NOT_DISCLOSED` | Not stated in the documents read | 6 | 1 | Review: the documents were read and do not state it; re-run only with a new source |
| `NOT_APPLICABLE` | Does not apply | 2 | 1 | - |

## By field

| Field | Missing | Top reasons |
|---|---:|---|
| lti_granted | 2 | NOT_DISCLOSED 1, REMUNERATION_REPORT_NOT_READ 1 |
| lti_target | 2 | NOT_DISCLOSED 1, REMUNERATION_REPORT_NOT_READ 1 |
| benefits_value | 2 | NOT_DISCLOSED 1, REMUNERATION_REPORT_NOT_READ 1 |
| pension_contribution | 2 | NOT_DISCLOSED 1, REMUNERATION_REPORT_NOT_READ 1 |
| staff_by_segment | 1 | NOT_DISCLOSED 1 |
| lti_vested | 1 | NOT_DISCLOSED 1 |
| aggregate_headcount | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| sti_paid | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| sti_target | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| sti_max | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| lti_max | 1 | REMUNERATION_REPORT_NOT_READ 1 |
| total_remuneration | 1 | REMUNERATION_REPORT_NOT_READ 1 |

## By company

| Company | Missing | Fields (reason) |
|---|---:|---|
| Framery Group (`framery-group`) | 16 | NOT_DISCLOSED: benefits_value, lti_granted, lti_target, lti_vested, pension_contribution, staff_by_segment; REMUNERATION_REPORT_NOT_READ: aggregate_headcount, benefits_value, lti_granted, lti_max, lti_target, pension_contribution, sti_max, sti_paid, sti_target, total_remuneration |
