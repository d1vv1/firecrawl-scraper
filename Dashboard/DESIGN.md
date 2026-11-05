# Allshares Part 1 accuracy dashboard: design

Companion to `SPEC.md` (what the dashboard does). This file covers how it looks and behaves.
The Angular app and the single-file HTML follow the same design.

## 1. Principles

1. **Findings first.** Every page title and chart title is a computed sentence that states what the data
   shows ("Only 49% of values are found; 1,409 are empty"), not a label ("Overview").
2. **Red means a problem.** Red is used only for failures, hard fails and empty values. Nothing decorative
   is red.
3. **One question per visual.** Each chart answers one question. If a chart needs a paragraph to explain,
   use a table.
4. **Drill down, don't scroll.** Summary at the top, detail one click away (field → values,
   company → values → gate reasons).
5. **Same numbers everywhere.** A count shown on two pages comes from the same core function.

## 2. Layout

```
┌───────────────────────────────────────────────────────────────────────┐
│ Top bar (48px, dark): title · tabs (scroll on overflow) · values count│  sticky
├───────────────────────────────────────────────────────────────────────┤
│ Filters: Country · Source · Data type · Field group · Company · Status│  sticky
├───────────────────────────────────────────────────────────────────────┤
│ KPI strip: 10 cards, auto-fit min 118px                               │  sticky
├───────────────────────────────────────────────────────────────────────┤
│ Page title (finding)                                                  │
│ Subtitle (scope, what is counted)                                     │
│ [Callout when there is something to act on]                           │
│ ┌──────────── chart ───────────┐ ┌──────────── chart ───────────┐     │  grid: auto-fit min 300px
│ └──────────────────────────────┘ └──────────────────────────────┘     │
│ ┌───────────────────────── table (max 340px, scrolls) ─────────────┐  │
│ └──────────────────────────────────────────────────────────────────┘  │
│ Footer: source · data date · imports applied · values in view         │
└───────────────────────────────────────────────────────────────────────┘
```

- Page padding 16px 18px; 16px side gutter at phone width; no horizontal page scroll (tables scroll
  inside their own box).
- Gap between cards and panels: 12–14px.

## 3. Tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | #f3f2f1 | Page background |
| `--card` | #ffffff | Panels, cards, tables |
| `--ink` | #252423 | Body text |
| `--soft` | #605e5c | Secondary text, axis labels |
| `--faint` | #8a8886 | Hints, footer, gridline labels |
| `--line` | #e1dfdd | Borders, gridlines |
| `--dark` | #201f1e | Top bar |
| `--brand` | #0077BB | Active tab, links, buttons, primary series |

### Data palette (colour-blind safe, max 5 per chart)

| Colour | Hex | Meaning |
|---|---|---|
| Blue | #0077BB | Primary series; Review |
| Orange | #EE7733 | Partial; soft fail; Fail (soft) |
| Teal | #009988 | Found; Pass |
| Red | #CC3311 | Not found; hard fail; Fail (hard) |
| Grey | #888888 | Incomplete; not run; n under 10 |

Gate result mapping: PASS teal, FAIL red on hard gates and orange on soft gates, NOT RUN grey.

Status mapping is fixed across pages: Pass teal, Review blue, Incomplete grey, Fail orange,
Fail (hard) red. Value status: found teal, partial orange, not found red.

### Type

- Font: "Segoe UI", system-ui, Arial, sans-serif. Base 13px / 1.45.
- Page title 20px semibold; panel title 14px semibold; KPI value 19px semibold; table 12px;
  hints 11px. Numbers in tables use tabular figures, right aligned.

## 4. Components

The Angular app builds these from Bootstrap 5.3 (CSS only); the Bootstrap class used is in brackets.
`app/src/bootstrap-theme.css` maps Bootstrap's primary, success, warning, danger and secondary colours to
the data palette above and keeps the 13px base size. The single-file HTML draws the same components
with `core/report.css`.

| Component | Spec |
|---|---|
| **Tab** | (`navbar` + `nav nav-underline`) Text link, 3px bottom border in `--brand` when selected, `aria-selected`. Tabs scroll horizontally on narrow screens. |
| **Filter** | (`form-label` + `form-select form-select-sm`) Label (12px uppercase, `--soft`) over a native `select`, min width 160px. Changing a filter refreshes every page. A "Clear filters" link appears when any filter is set. |
| **KPI card** | (`card`) White, 3px top border coloured by state (teal good, orange watch, red problem, blue neutral). Value, label, one comparison line ("+1.2 pts vs tracker", "target 95%"). |
| **Panel** | (`card`) White, 1px `--line` border, 2px radius, light shadow, 10–12px padding, title row. |
| **Callout** | (`alert alert-danger` / `alert-warning`) 4px left border. Red for "most attention needed", orange for data notes (e.g. duplicate company IDs). |
| **Table** | (`table table-sm table-hover`) Sticky header, 6px 8px cells, zebra-free, hover row tint. Clickable rows show a pointer and a "›" in the last cell; Enter or click opens the detail. Sortable headers show ▲/▼. |
| **Search box** | (`form-control form-control-sm`) Above long tables (Fields, Companies, detail values). Filters as you type. |
| **Status chip** | (`badge rounded-pill`) Small rounded label with the status colour as background tint and text colour; used in detail tables. |
| **Drill-down panel** | Opens below the list on the same page with a "← Back to list" link; the selected item stays highlighted. |
| **Breadcrumb** | (`breadcrumb`, divider "›") Validation steps levels: Validation steps › gate › field. |
| **Button** | (`btn btn-primary` for primary actions, `btn btn-outline-primary` otherwise, `btn btn-link` for links) Outline in `--brand`; disabled at 45% opacity. Primary actions: Import valid rows, Export CSV. Reset is secondary. |

## 5. Charts

- Library: Apache ECharts (SVG renderer) in the Angular app; built-in SVG builders in the single-file HTML.
  Same colours, order and labels in both.
- SVG only, fixed height about 230px (horizontal bar charts with 12 rows use 332px). Category labels on
  horizontal bars are truncated at 142px with the full name in the tooltip.
- Gridlines `--line`, axis labels 10px `--faint`, data labels 10–11px.
- Every bar, slice and point has a `<title>` tooltip with label and exact value.
- Bar charts start at zero. Percent charts run 0–100.
- Pie: at most 5 slices, legend with percentages; use only for part-of-whole.
- Stacked bars: status order bottom to top Pass, Review, Incomplete, Fail, Fail (hard).
- Trend: two lines (checks passing blue, found teal), points labelled "Tracker", "#1", "#2", …; a dashed
  grey line at the 95% target.
- Empty state: "No data for this selection" centred in `--faint`.

## 6. Page compositions

| Page | Row 1 | Row 2 | Row 3 |
|---|---|---|---|
| Overview | Companies by country (bars) · Value status (pie) | Country summary (table) | |
| Pay vs company | Status by data type (stacked) · Share of values (pie) | By country (table) | |
| Countries | Status by country (stacked) · Companies by country (h-bars) | Country × data type (table) | |
| Fields | Callout: worst field | Score status by field, top 12 (stacked h-bars) | Fields table → field drill-down |
| Empty fields | Top 12 empty fields (h-bars, red) · Empty by data type (pie) | By field (table) | By company (table → Companies) |
| Companies | Companies table | Drill-down: header, status pie, fails by gate (h-bars), values table | |
| Failures | Callout: most attention | Fails by check · Hard vs soft · Fail rate by module · Fail rate by field | Fails by field (table) |
| Validation steps | Pass rate by family (bars) | Steps table grouped by family → step: fails by field (h-bars) · reasons · fields table → field: values table | Breadcrumb "Steps › CORE-02 › revenue" at each level |
| Ranges | Range options panel | n per range row (h-bars; grey when n < 10) | Ranges table, Export CSV |
| Trend | Trend line | Schema checks by import (table) | |
| Metric register | Register table, Export CSV | | |
| Import | 1. Choose file · preview · apply · reset | 2. Errors | Schema columns · Protocol field IDs · full JSON |

## 7. Wording

- Plain English, sentence case, no jargon in titles. Gate IDs shown with their names ("NUM-09 Valuation
  basis stated").
- Counts with thousands separators (en-GB). Percentages rounded to whole numbers on charts, one decimal in
  KPI comparisons.
- Provisional or unapproved content always carries its label (see SPEC section 9).

## 8. Accessibility

- Text contrast at least 4.5:1 on white; status never shown by colour alone (chips carry the word).
- Tabs use `role="tablist"`/`role="tab"`; charts `role="img"` with a text summary in the title.
- All interactive rows reachable by keyboard (`tabindex="0"`, Enter opens).

## 9. Responsive

- ≥ 1100px: two charts per row. 700–1100px: charts wrap by the 300px auto-fit grid. < 700px: one column,
  filters wrap, KPI cards two per row, tables scroll inside their panel.
