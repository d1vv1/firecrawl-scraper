import { Component, computed, inject, input, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import * as UI from '../../../../core/report-ui.js';
import { Chart } from '../chart';
import * as G from '../chart';
import { download } from '../download';
import { ReportService } from '../report.service';

/** Links to the documents one company's values were read from (first two, the rest folded). */
@Component({
  selector: 'app-links',
  template: `@if (items().length) {<div class="links">
      @for (l of items().slice(0, 2); track l.url) {<a [href]="l.url" target="_blank" rel="noopener noreferrer" [title]="l.url">{{ l.label }} · {{ l.host }} ({{ l.n }})</a>}
      @if (items().length > 2) {<details><summary>+{{ items().length - 2 }} more</summary>
        @for (l of items().slice(2); track l.url) {<a [href]="l.url" target="_blank" rel="noopener noreferrer" [title]="l.url">{{ l.label }} · {{ l.host }} ({{ l.n }})</a>}</details>}
    </div>} @else {<span class="hint">–</span>}`
})
export class Links {
  readonly items = input<any[]>([]);
}

function pctColor(p: number, good: number) {
  return p >= good ? '#009988' : p >= good - 20 ? '#EE7733' : '#CC3311';
}

// ------------------------------------------------------------------ Reports and sources (SPEC 6.3, 12)
@Component({
  selector: 'app-sources',
  imports: [Chart, Links, RouterLink],
  template: `
    @let s = data();
    @let t = s.totals;
    <div class="title">{{ s.title }}</div>
    <div class="sub">For each company: whether values were read from its annual report and from its remuneration report, links to those documents and to other sources, and how many protocol fields were filled. A report counts as found when at least one value in view was read from it. Annual report includes ESEF filings, SEC 20-F / 10-K and Companies House accounts; remuneration report includes the remuneration policy.</div>
    <div class="kmini">
      <div><b>{{ t.companies }}</b><span>Companies in view</span></div>
      <div><b>{{ t.annual }} <small>({{ t.annualPct }}%)</small></b><span>Annual report found</span></div>
      <div><b>{{ t.rem }} <small>({{ t.remPct }}%)</small></b><span>Remuneration report found</span></div>
      <div><b>{{ t.both }} <small>({{ t.bothPct }}%)</small></b><span>Both found</span></div>
      <div><b>{{ t.neither }} <small>({{ t.neitherPct }}%)</small></b><span>Neither found</span></div>
      <div><b>{{ avgFilled() }}%</b><span>Protocol fields filled (average per company)</span></div>
    </div>
    <div class="grid">
      <div class="vis card"><h3>{{ t.companies ? t.neither + ' of ' + t.companies + ' companies have neither report in view' : 'Companies by reports found' }}</h3><app-chart [options]="chart()" /></div>
      <div class="vis card"><h3>Reports found by country</h3><div class="tbl"><table class="table table-sm table-hover">
        <thead><tr><th>Country</th><th class="n">Companies</th><th class="n">Annual report</th><th class="n">Annual %</th><th class="n">Remuneration report</th><th class="n">Remuneration %</th><th class="n">Both</th><th class="n">Neither</th></tr></thead>
        <tbody>@for (r of s.byCountry; track r.c) {<tr><td>{{ r.c }}</td><td class="n">{{ r.companies }}</td><td class="n">{{ r.annual }}</td><td class="n">{{ r.annualPct }}%</td><td class="n">{{ r.rem }}</td><td class="n">{{ r.remPct }}%</td><td class="n">{{ r.both }}</td><td class="n">{{ r.neither }}</td></tr>}
        @empty {<tr><td colspan="8">No data for this selection.</td></tr>}</tbody></table></div></div>
    </div>
    <div class="vis card">
      <div class="bar">
        <div class="opt" style="flex:1 1 220px"><label class="form-label">Search companies</label><input class="form-control form-control-sm" type="search" placeholder="Name, ID or LEI" [value]="q()" (input)="q.set($any($event.target).value)"></div>
        <div class="opt"><label class="form-label">Annual report</label><select class="form-select form-select-sm" (change)="fa.set($any($event.target).value)"><option value="">All</option><option value="yes">Found</option><option value="no">Not found</option></select></div>
        <div class="opt"><label class="form-label">Remuneration report</label><select class="form-select form-select-sm" (change)="fr.set($any($event.target).value)"><option value="">All</option><option value="yes">Found</option><option value="no">Not found</option></select></div>
        <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export CSV</button>
      </div>
      <div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr><th>Company</th><th>Country</th><th>Annual report</th><th>Annual report links</th><th>Remuneration report</th><th>Remuneration report links</th><th>Other source links</th><th class="n">Protocol fields</th><th class="n">Fields filled</th><th class="n">Fields empty</th><th class="n">Values</th><th class="n">Found</th><th class="n">Partial</th><th class="n">Not found</th><th class="n">Found %</th><th class="n">From annual report</th><th class="n">From remuneration report</th><th class="n">From other sources</th><th class="n">Values pass %</th><th class="n">Checks pass %</th></tr></thead>
        <tbody>@for (x of list(); track x.key) {
          <tr><td><a [routerLink]="['/companies', x.key]" title="Open company">{{ x.o }}</a></td><td>{{ x.c }}</td>
            <td>@if (x.hasAnnual) {<span class="yes">Found</span>} @else {<span class="no">Not found</span>}</td><td><app-links [items]="x.links.annual" /></td>
            <td>@if (x.hasRem) {<span class="yes">Found</span>} @else {<span class="no">Not found</span>}</td><td><app-links [items]="x.links.rem" /></td><td><app-links [items]="x.links.other" /></td>
            <td class="n">{{ x.fields }}</td><td class="n">{{ x.fieldsFilled }}</td><td class="n">{{ x.fieldsEmpty }}</td><td class="n">{{ C.fmt(x.values) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td><td class="n">{{ x.foundPct }}%</td>
            <td class="n">{{ C.fmt(x.n.annual) }}</td><td class="n">{{ C.fmt(x.n.rem) }}</td><td class="n">{{ C.fmt(x.n.other) }}</td><td class="n">{{ x.passPct == null ? '–' : x.passPct + '%' }}</td><td class="n">{{ x.checksPct == null ? '–' : x.checksPct + '%' }}</td></tr>
        } @empty {<tr><td colspan="20">No companies match.</td></tr>}</tbody></table></div>
    </div>`
})
export class Sources {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly q = signal('');
  readonly fa = signal('');
  readonly fr = signal('');
  readonly data = computed(() => this.C.sources(this.r.model, this.r.view()));
  readonly list = computed(() => {
    const q = this.q().trim().toLowerCase(), fa = this.fa(), fr = this.fr();
    return this.data().rows.filter((x: any) => (!q || (x.o + ' ' + x.key + ' ' + x.idList.join(' ')).toLowerCase().includes(q)) &&
      (!fa || (fa === 'yes') === x.hasAnnual) && (!fr || (fr === 'yes') === x.hasRem));
  });
  readonly avgFilled = computed(() => {
    const rows = this.data().rows;
    return rows.length ? Math.round((rows.reduce((a: number, x: any) => a + (x.fields ? x.fieldsFilled / x.fields : 0), 0) / rows.length) * 100) : 0;
  });
  readonly chart = computed(() => {
    const t = this.data().totals;
    return G.bars([{ label: 'Annual report', value: t.annual, color: '#0077BB' }, { label: 'Remuneration', value: t.rem, color: '#EE7733' },
      { label: 'Both', value: t.both, color: '#009988' }, { label: 'Neither', value: t.neither, color: '#CC3311' }]);
  });
  exportCsv() {
    download(this.C.sourcesCSV(this.list()), 'allshares_reports_and_sources.csv');
  }
}

// ------------------------------------------------------------------ Field coverage (SPEC 6.3, 13)
@Component({
  selector: 'app-coverage',
  imports: [Chart],
  template: `
    @let fc = data();
    <div class="title">{{ fc.title }}</div>
    <div class="sub">Every field of the protocol field list (allshares_fields_list.xlsx, sheets Company Data and Pay Data). Found % = found values of the values that apply; filled % adds partial values. Check pass % = PASS of the checks run on the field (PASS + FAIL); values pass % = values with status Pass of the scored values. Averages count each field once. Click a field to see its values.</div>
    <div class="kmini">
      @for (s of fc.sheets; track s.name) {<div><b>{{ s.avgFound ?? '–' }}% <small>found</small></b><span>{{ s.name }}: average over {{ s.inView }} fields</span></div>}
      @for (s of fc.sheets; track s.name) {<div><b>{{ s.avgCheck ?? '–' }}% <small>checks pass</small></b><span>{{ s.name }}: values pass {{ s.avgPass ?? '–' }}%</span></div>}
      <div><b>{{ fc.all.neverFound }}</b><span>Fields never found in view</span></div>
      <div><b>{{ fc.all.alwaysFound }}</b><span>Fields always filled</span></div>
    </div>
    <div class="grid">
      <div class="vis card"><h3>{{ lowF().length ? 'Found % by field: ' + lowF()[0].d + ' is lowest (' + lowF()[0].foundPct + '%); lowest 15' : 'Found % by field' }}</h3><app-chart [options]="chFound()" [height]="380" /></div>
      <div class="vis card"><h3>{{ lowC().length ? 'Check pass % by field: ' + lowC()[0].d + ' is lowest (' + lowC()[0].checkPct + '%); lowest 15' : 'Check pass % by field' }}</h3><app-chart [options]="chCheck()" [height]="380" /></div>
    </div>
    <div class="vis card">
      <div class="bar">
        <div class="opt" style="flex:1 1 220px"><label class="form-label">Search fields</label><input class="form-control form-control-sm" type="search" placeholder="Field, ID, group or description" [value]="q()" (input)="q.set($any($event.target).value)"></div>
        <div class="opt"><label class="form-label">Sheet</label><select class="form-select form-select-sm" (change)="sheet.set($any($event.target).value)"><option value="">Company and pay</option><option value="Company Data">Company Data</option><option value="Pay Data">Pay Data</option></select></div>
        <label><input type="checkbox" class="form-check-input" [checked]="grouped()" (change)="grouped.set($any($event.target).checked)"> Group by field group</label>
        <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export CSV</button>
      </div>
      <div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr><th class="n">#</th><th>Field</th><th>ID</th><th>Group</th><th>Grain</th><th>What it is</th><th class="n">Values</th><th class="n">Found</th><th class="n">Partial</th><th class="n">Not found</th><th class="n">Found %</th><th class="n">Filled %</th><th class="n">Companies with value</th><th class="n">Checks run</th><th class="n">Checks failed</th><th class="n">Check pass %</th><th class="n">Values pass %</th><th class="n">Avg score</th><th>Checks applied</th></tr></thead>
        <tbody>
          @for (row of rows(); track row.key) {
            @if (row.group; as g) {
              <tr class="group"><td colspan="19"><b>{{ g.sheet }} › {{ g.k }}</b> · {{ g.nFields }} {{ g.nFields === 1 ? 'field' : 'fields' }} · average found {{ g.avgFound ?? '–' }}% · checks pass {{ g.avgCheck ?? '–' }}% · values pass {{ g.avgPass ?? '–' }}%</td></tr>
            } @else {
              @let x = row.f;
              <tr class="click" tabindex="0" (click)="open(x.d)" (keydown.enter)="open(x.d)">
                <td class="n">{{ x.n }}</td><td>{{ x.d }}</td><td>{{ x.f }}</td><td>{{ x.k }}</td><td>{{ x.g }}</td><td class="iss">{{ x.what }}</td>
                <td class="n">{{ C.fmt(x.rows) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td>
                <td class="n">@if (x.foundPct != null) {<span class="pctbar"><i [style.width.%]="x.foundPct" [style.background]="color(x.foundPct, 90)"></i></span>{{ x.foundPct }}%} @else {–}</td>
                <td class="n">@if (x.filledPct != null) {<span class="pctbar"><i [style.width.%]="x.filledPct" [style.background]="color(x.filledPct, 90)"></i></span>{{ x.filledPct }}%} @else {–}</td>
                <td class="n">{{ C.fmt(x.filledCos) }} <span class="hint">of {{ C.fmt(x.companies) }}</span></td><td class="n">{{ C.fmt(x.checkRuns) }}</td><td class="n">{{ C.fmt(x.checkFail) }}</td>
                <td class="n">@if (x.checkPct != null) {<span class="pctbar"><i [style.width.%]="x.checkPct" [style.background]="color(x.checkPct, 95)"></i></span>{{ x.checkPct }}%} @else {–}</td>
                <td class="n">@if (x.passPct != null) {<span class="pctbar"><i [style.width.%]="x.passPct" [style.background]="color(x.passPct, 95)"></i></span>{{ x.passPct }}%} @else {–}</td>
                <td class="n">{{ x.avg ?? '–' }}</td><td class="iss mono">{{ x.checks.join(', ') }}</td></tr>
            }
          } @empty {<tr><td colspan="19">No fields match.</td></tr>}
        </tbody></table></div>
    </div>`
})
export class Coverage {
  readonly r = inject(ReportService);
  readonly router = inject(Router);
  readonly C = this.r.C;
  readonly q = signal('');
  readonly sheet = signal('');
  readonly grouped = signal(true);
  readonly color = pctColor;
  readonly data = computed(() => this.C.fieldCoverage(this.r.model, this.r.view()));
  readonly all = computed(() => this.data().sheets.reduce((a: any[], s: any) => a.concat(s.fields), []));
  readonly lowF = computed(() => this.all().filter((x: any) => x.foundPct != null).sort((a: any, b: any) => a.foundPct - b.foundPct).slice(0, 15));
  readonly lowC = computed(() => this.all().filter((x: any) => x.checkPct != null).sort((a: any, b: any) => a.checkPct - b.checkPct).slice(0, 15));
  readonly chFound = computed(() => G.hbars(this.lowF().map((x: any) => ({ label: x.d, value: x.foundPct, color: x.foundPct < 50 ? '#CC3311' : x.foundPct < 80 ? '#EE7733' : '#009988', sub: this.C.fmt(x.found) + '/' + this.C.fmt(x.rows) })), { max: 100, suffix: '%' }));
  readonly chCheck = computed(() => G.hbars(this.lowC().map((x: any) => ({ label: x.d, value: x.checkPct, color: x.checkPct < 80 ? '#CC3311' : x.checkPct < 95 ? '#EE7733' : '#009988', sub: this.C.fmt(x.checkFail) + ' fails' })), { max: 100, suffix: '%' }));
  readonly rows = computed(() => {
    const q = this.q().trim().toLowerCase(), sh = this.sheet(), out: any[] = [];
    const match = (x: any) => (!sh || x.sheet === sh) && (!q || (x.d + ' ' + x.f + ' ' + x.k + ' ' + x.what).toLowerCase().includes(q));
    this.data().sheets.forEach((s: any) => {
      if (sh && s.name !== sh) return;
      if (this.grouped()) s.cats.forEach((k: any) => {
        const fs = k.fields.filter(match);
        if (!fs.length) return;
        out.push({ key: 'g:' + s.name + k.k, group: { ...k, sheet: s.name } });
        fs.forEach((f: any) => out.push({ key: f.d, f }));
      });
      else s.fields.filter(match).forEach((f: any) => out.push({ key: f.d, f }));
    });
    return out;
  });
  open(dp: string) {
    this.router.navigate(['/fields', dp]);
  }
  exportCsv() {
    download(this.C.coverageCSV(this.data()), 'allshares_field_coverage.csv');
  }
}

// ------------------------------------------------------------------ Not-found matrix (Pay vs company, SPEC 6.3)
type Sel = { p?: number | null; k?: string; d?: string; c?: string };
@Component({
  selector: 'app-nf-matrix',
  imports: [RouterLink],
  template: `
    @let m = data();
    <div class="vis card"><h3>By data type, field group, field and country</h3>
      <div class="sub">Rows: data type › field group › field (▸ opens a level). Cells: values not found of the values that apply; the colour is the share missing. Click any cell to list the companies behind it; click a header to sort.</div>
      <div class="bar">
        <div class="opt"><label class="form-label">Cells show</label><select class="form-select form-select-sm" (change)="show.set($any($event.target).value)"><option value="n">Not found (count)</option><option value="pct">Not found %</option></select></div>
        <button class="btn btn-outline-primary btn-sm" (click)="setAll(true)">Open all</button><button class="btn btn-outline-primary btn-sm" (click)="setAll(false)">Close all</button>
      </div>
      <div class="tbl tall"><table class="table table-sm matrix">
        <thead><tr>
          @for (h of heads(); track h[0]; let i = $index) {<th [attr.data-sort]="h[0]" [class.n]="i > 0" tabindex="0" [attr.aria-sort]="sort().k === h[0] ? (sort().dir > 0 ? 'ascending' : 'descending') : null" (click)="sortBy(h[0])" (keydown.enter)="sortBy(h[0])">{{ h[1] }}</th>}
        </tr></thead>
        <tbody>
          @if (m.tree.length) {
            <tr class="l0"><td><span class="tog"></span>All values</td><td class="n">–</td>
              <td [class]="'cell ' + heat(m.total.pct) + (isSel({}, '') ? ' on' : '')" tabindex="0" (click)="pick({}, '')" (keydown.enter)="pick({}, '')">{{ cellText(m.total) }}@if (show() === 'n') {<small>/ {{ C.fmt(m.total.rows) }}</small>}</td>
              <td class="n">{{ m.total.pct }}%</td><td class="n">{{ C.fmt(m.total.companies) }}</td><td class="n" [title]="wdTitle(m.total)">{{ C.fmt(m.total.withData) }}@if (show() === 'n') {<small>/ {{ C.fmt(m.total.cosAll) }}</small>}</td>
              @for (c of m.countries; track c) {@let x = m.total.byC[c];
                @if (x && x.rows) {<td [class]="'cell ' + heat(x.pct) + (isSel({}, c) ? ' on' : '')" tabindex="0" (click)="pick({}, c)" (keydown.enter)="pick({}, c)">{{ cellText(x) }}@if (show() === 'n') {<small>/ {{ C.fmt(x.rows) }}</small>}</td>} @else {<td class="n">–</td>}}
            </tr>
          }
          @for (n of flat(); track n.id) {
            <tr [class]="'l' + n.level">
              <td>@if (n.level < 2) {<button class="tog" [attr.aria-expanded]="isOpen(n)" (click)="toggle(n)">{{ isOpen(n) ? '▾' : '▸' }}</button>} @else {<span class="tog"></span>}
                @if (n.level === 2) {<a [routerLink]="['/fields', n.label]" title="Open this field">{{ n.label }}</a>} @else {<span>{{ n.label }}</span> <span class="hint">({{ n.children.length }})</span>}</td>
              @if (n.level === 2) {<td class="n" [title]="n.rank == null ? 'Not ranked in the benchmarking field list' : 'Benchmarking rank ' + n.rank + ' (1 = most critical)'">{{ n.rank ?? '–' }}</td>} @else {<td class="n hint" [title]="n.rank == null ? '' : 'Best-ranked field in this row: ' + n.rank">@if (n.rank != null) {top {{ n.rank }}} @else {–}</td>}
              <td [class]="'cell ' + heat(n.pct) + (isSel(n.sel, '') ? ' on' : '')" tabindex="0" [title]="C.fmt(n.nf) + ' of ' + C.fmt(n.rows) + ' values not found (' + n.pct + '%)'" (click)="pick(n.sel, '')" (keydown.enter)="pick(n.sel, '')">{{ cellText(n) }}@if (show() === 'n') {<small>/ {{ C.fmt(n.rows) }}</small>}</td>
              <td class="n">{{ n.pct }}%</td><td class="n">{{ C.fmt(n.companies) }}</td><td class="n" [title]="wdTitle(n)">{{ C.fmt(n.withData) }}@if (show() === 'n') {<small>/ {{ C.fmt(n.cosAll) }}</small>}</td>
              @for (c of m.countries; track c) {@let x = n.byC[c];
                @if (x && x.rows) {<td [class]="'cell ' + heat(x.pct) + (isSel(n.sel, c) ? ' on' : '')" tabindex="0" [title]="C.fmt(x.nf) + ' of ' + C.fmt(x.rows) + ' values not found (' + x.pct + '%)'" (click)="pick(n.sel, c)" (keydown.enter)="pick(n.sel, c)">{{ cellText(x) }}@if (show() === 'n') {<small>/ {{ C.fmt(x.rows) }}</small>}</td>} @else {<td class="n">–</td>}}
            </tr>
          } @empty {<tr><td [attr.colspan]="6 + m.countries.length">Nothing missing in this selection.</td></tr>}
        </tbody></table></div>
    </div>
    @if (sel(); as s) {
      <div class="vis card">
        <div class="back"><button class="btn btn-link btn-sm" (click)="sel.set(null)">← Close list</button></div>
        <h3>Not found: {{ selLabel() }}: {{ C.fmt(detail().length) }} values at {{ C.fmt(detailCos()) }} companies</h3>
        <div class="sub">Click a company to open it.</div>
        <div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Company</th><th>Country</th><th>Data type</th><th>Group</th><th>Field</th><th>ID</th><th>Role</th><th>Note</th></tr></thead>
          <tbody>@for (x of detail().slice(0, 3000); track $index) {
            <tr class="click" tabindex="0" [routerLink]="['/companies', x.key]"><td>{{ x.o }}</td><td>{{ x.c }}</td><td>{{ x.type }}</td><td>{{ x.k }}</td><td>{{ x.d }}</td><td>{{ x.f }}</td><td>{{ x.r }}</td><td class="iss">{{ x.note }}</td></tr>
          } @empty {<tr><td colspan="8">Nothing missing here.</td></tr>}</tbody></table></div>
        @if (detail().length > 3000) {<div class="note">First 3,000 of {{ C.fmt(detail().length) }} shown. Narrow the filters or use Export for Claude for all of them.</div>}
      </div>
    }`
})
export class NotFoundMatrix {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly show = signal<'n' | 'pct'>('n');
  readonly sort = signal<{ k: string; dir: number }>({ k: '', dir: -1 });
  readonly open = signal<Record<string, boolean>>({});
  readonly sel = signal<(Sel & { c: string }) | null>(null);
  readonly data = computed(() => this.C.notFoundMatrix(this.r.view(), this.r.loaded() ? this.C.fieldRanks(this.r.model) : {}));
  readonly heads = computed(() => [['label', 'Data type › group › field'], ['rank', 'Rank'], ['nf', 'Not found'], ['pct', 'Not found %'], ['companies', 'Companies missing'], ['withData', 'Companies with data']]
    .concat(this.data().countries.map((c) => [c, c])));
  readonly flat = computed(() => {
    const out: any[] = [], s = this.sort(), show = this.show();
    const key = (n: any) => (s.k === 'label' ? n.label.toLowerCase() : s.k === 'rank' ? (n.rank == null ? 1e9 * s.dir : n.rank) : s.k === 'nf' || s.k === 'pct' || s.k === 'companies' || s.k === 'withData' ? n[s.k] : n.byC[s.k] ? (show === 'pct' ? n.byC[s.k].pct : n.byC[s.k].nf) : -1);
    const order = (l: any[]) => (s.k ? l.slice().sort((a, b) => { const x = key(a), y = key(b); return (typeof x === 'string' ? x.localeCompare(y) : x - y) * s.dir; }) : l);
    const walk = (n: any) => { out.push(n); if (this.isOpen(n)) order(n.children).forEach(walk); };
    order(this.data().tree).forEach(walk);
    return out;
  });
  readonly detail = computed(() => { const s = this.sel(); return s ? this.C.notFoundValues(this.r.view(), s) : []; });
  readonly detailCos = computed(() => new Set(this.detail().map((x: any) => x.key)).size);
  readonly selLabel = computed(() => {
    const s = this.sel();
    return s ? [s.p == null ? '' : s.p ? 'Pay data' : 'Company data', s.k, s.d, s.c].filter(Boolean).join(' · ') || 'All values' : '';
  });
  wdTitle(n: any) {
    return this.C.fmt(n.withData) + ' of ' + this.C.fmt(n.cosAll) + ' companies have at least one value found or partial here';
  }
  heat(p: number) {
    return p <= 0 ? 'heat0' : p < 25 ? 'heat1' : p < 50 ? 'heat2' : p < 75 ? 'heat3' : 'heat4';
  }
  cellText(x: any) {
    return this.show() === 'pct' ? x.pct + '%' : this.C.fmt(x.nf);
  }
  isOpen(n: any) {
    const o = this.open()[n.id];
    return o != null ? o : n.level === 0;
  }
  toggle(n: any) {
    this.open.update((o) => ({ ...o, [n.id]: !this.isOpen(n) }));
  }
  setAll(on: boolean) {
    const o: Record<string, boolean> = {};
    this.data().tree.forEach((t: any) => { o[t.id] = on; t.children.forEach((k: any) => (o[k.id] = on)); });
    this.open.set(o);
  }
  sortBy(k: string) {
    this.sort.update((s) => ({ k, dir: s.k === k ? -s.dir : k === 'label' || k === 'rank' ? 1 : -1 }));
  }
  private same(a: Sel, b: Sel) {
    return (a.p ?? null) === (b.p ?? null) && (a.k || '') === (b.k || '') && (a.d || '') === (b.d || '');
  }
  isSel(s: Sel, c: string) {
    const cur = this.sel();
    return !!cur && this.same(cur, s) && (cur.c || '') === c;
  }
  pick(s: Sel, c: string) {
    this.sel.set(this.isSel(s, c) ? null : { ...s, c });
  }
}

// ------------------------------------------------------------------ Not found page (SPEC 6.3, 2a)
@Component({
  selector: 'app-notfound',
  imports: [NotFoundMatrix],
  template: `
    @let m = data();
    <div class="title">What was not found: {{ m.title }}</div>
    <div class="sub">Every value with no result in any source tried, by data type, field group, field and country. Not-applicable values are left out.</div>
    <div class="kmini">
      <div><b>{{ C.fmt(m.total.nf) }} <small>({{ m.total.pct }}%)</small></b><span>Values not found</span></div>
      @for (t of m.tree; track t.id) {<div><b>{{ C.fmt(t.nf) }} <small>({{ t.pct }}%)</small></b><span>{{ t.label }} not found</span></div>}
      <div><b>{{ C.fmt(missingCos()) }} <small>of {{ C.fmt(cos()) }}</small></b><span>Companies with something missing</span></div>
    </div>
    <app-nf-matrix />`
})
export class NotFoundPage {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly data = computed(() => this.C.notFoundMatrix(this.r.view()));
  readonly cos = computed(() => this.C.companiesOf(this.r.view()));
  readonly missingCos = computed(() => new Set(this.r.view().filter((v) => v.st === 'not_found').map((v) => this.C.companyKey(v))).size);
}

// ------------------------------------------------------------------ Company data / Pay data (SPEC 6.3, 15)
const SEV_CHIP: Record<string, string> = { High: 'H', Medium: 'F', Low: 'R', 'Never used': 'X' };
const SEV_COLOR: Record<string, string> = { High: '#CC3311', Medium: '#EE7733', Low: '#0077BB', 'Never used': '#888888' };
@Component({
  selector: 'app-datafields',
  imports: [Chart],
  template: `
    @let d = data();
    <div class="title">{{ d.title }}</div>
    <div class="sub">The {{ pay() ? 'pay' : 'company' }} fields of the protocol: how much each one matters (requirement, severity{{ pay() ? ', 1 Dec milestone' : '' }} and why, from the field review, with its fill in the 50-company review sample) next to how this run did (companies with a value, filled %, found %, checks). Filled = found or partial. Averages count each field once. Click a field to see its values.</div>
    <div class="kmini">
      <div><b>{{ d.all.n }}</b><span>Fields in the protocol</span></div>
      <div><b>{{ d.required.n }} <small>· {{ p(d.required.avgFilled) }} filled</small></b><span>Required fields (incl. conditional)</span></div>
      <div><b>{{ p(high()?.avgFilled) }}</b><span>High severity: filled on average</span></div>
      <div><b>{{ p(d.required.avgCheck) }}</b><span>Required fields: checks pass</span></div>
      <div><b>{{ d.gaps.length }}</b><span>High-severity fields under 80% filled</span></div>
      @if (pay()) {@for (m of d.milestones; track m.name) {<div><b>{{ p(m.avgFilled) }}</b><span>1 Dec {{ m.name }}: filled on average ({{ m.n }} fields)</span></div>}}
      @else {<div><b>{{ d.neverUsed }}</b><span>Fields never used in analysis</span></div>}
      <div><b>{{ d.companies }}</b><span>Companies in view</span></div>
    </div>
    <div class="grid">
      <div class="vis card"><h3>{{ req().length ? 'Required fields by filled %: ' + req()[0].d + ' is lowest (' + req()[0].filledPct + '%)' : 'Required fields by filled %' }}</h3>
        <app-chart [options]="chart()" [height]="380" />
        <div class="legend">@for (s of sevs; track s) {<span><i [style.background]="color[s]"></i>{{ s }} severity</span>}</div></div>
      <div class="vis card"><h3>By requirement, severity{{ pay() ? ' and milestone' : '' }} (average across fields)</h3><div class="tbl"><table class="table table-sm table-hover">
        <thead><tr><th>Group</th><th class="n">Fields</th><th class="n">Filled %</th><th class="n">Found %</th><th class="n">Check pass %</th><th class="n">Values pass %</th></tr></thead>
        <tbody>@for (g of groups(); track g[0]) {<tr><td>{{ g[0] }}</td><td class="n">{{ g[1].n }}</td><td class="n">{{ p(g[1].avgFilled) }}</td><td class="n">{{ p(g[1].avgFound) }}</td><td class="n">{{ p(g[1].avgCheck) }}</td><td class="n">{{ p(g[1].avgPass) }}</td></tr>}</tbody></table></div></div>
    </div>
    <div class="vis card">
      <div class="bar">
        <div class="opt" style="flex:1 1 220px"><label class="form-label">Search fields</label><input class="form-control form-control-sm" type="search" placeholder="Field, ID, group or why" [value]="q()" (input)="q.set($any($event.target).value)"></div>
        <div class="opt"><label class="form-label">Requirement</label><select class="form-select form-select-sm" (change)="fr.set($any($event.target).value)"><option value="">All</option>@for (c of C.REQ_CLASSES; track c[0]) {<option [value]="c[0]">{{ c[1] }}</option>}</select></div>
        <div class="opt"><label class="form-label">Severity</label><select class="form-select form-select-sm" (change)="fs.set($any($event.target).value)"><option value="">All</option>@for (s of C.SEVERITIES; track s) {<option [value]="s">{{ s }}</option>}</select></div>
        @if (pay()) {<div class="opt"><label class="form-label">1 Dec milestone</label><select class="form-select form-select-sm" (change)="fm.set($any($event.target).value)"><option value="">All</option><option value="In scope">In scope</option><option value="Deferred">Deferred</option></select></div>}
        <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export CSV</button>
      </div>
      <div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr><th class="n">#</th><th>Field</th><th>ID</th><th>Group</th><th>Requirement</th><th>Severity</th>@if (pay()) {<th>1 Dec milestone</th>}<th class="n">Fill (of 50) review</th><th class="n">Companies with value</th><th class="n">Filled %</th><th class="n">Found %</th><th class="n">Check pass %</th><th class="n">Values pass %</th><th>Why</th></tr></thead>
        <tbody>@for (x of list(); track x.d) {
          <tr class="click" tabindex="0" (click)="open(x.d)" (keydown.enter)="open(x.d)">
            <td class="n">{{ x.n }}</td><td>{{ x.d }}</td><td>{{ x.f }}</td><td>{{ x.k }}</td><td>{{ x.req }}</td>
            <td [attr.data-v]="x.sev ? C.SEVERITIES.length - C.SEVERITIES.indexOf(x.sev) : ''">@if (x.sev) {<span [class]="'chip ' + (chip[x.sev] || 'X')">{{ x.sev }}</span>}</td>
            @if (pay()) {<td>{{ x.milestone }}</td>}
            <td class="n">{{ x.fill50 ?? '–' }}</td><td class="n">{{ C.fmt(x.filledCos) }} <span class="hint">of {{ C.fmt(d.companies) }}</span></td>
            @for (k of pcts; track k[0]) {<td class="n">@if (x[k[0]] != null) {<span class="pctbar"><i [style.width.%]="x[k[0]]" [style.background]="barColor(x[k[0]], k[1])"></i></span>{{ x[k[0]] }}%} @else {–}</td>}
            <td class="iss">{{ x.why }}</td></tr>
        } @empty {<tr><td colspan="14">No fields match.</td></tr>}</tbody></table></div>
    </div>`
})
export class DataFields {
  readonly r = inject(ReportService);
  readonly router = inject(Router);
  readonly C = this.r.C;
  /** "Company Data" or "Pay Data", from the route's data. */
  readonly sheet = input<string>('Company Data');
  readonly q = signal('');
  readonly fr = signal('');
  readonly fs = signal('');
  readonly fm = signal('');
  readonly chip = SEV_CHIP;
  readonly color = SEV_COLOR;
  readonly sevs = this.C.SEVERITIES.slice(0, 3);
  readonly pcts: [string, number][] = [['filledPct', 90], ['foundPct', 90], ['checkPct', 95], ['passPct', 95]];
  readonly barColor = pctColor;
  readonly pay = computed(() => this.sheet() === 'Pay Data');
  readonly data = computed(() => this.C.dataPage(this.r.model, this.r.view(), this.sheet()));
  readonly high = computed(() => this.data().bySev.find((g: any) => g.sev === 'High'));
  readonly req = computed(() => this.data().fields.filter((x: any) => (x.reqClass === 'required' || x.reqClass === 'conditional') && x.filledPct != null)
    .sort((a: any, b: any) => a.filledPct - b.filledPct));
  readonly chart = computed(() => G.hbars(this.req().slice(0, 15).map((x: any) => ({ label: x.d, value: x.filledPct, color: SEV_COLOR[x.sev] || '#888888', sub: x.sev })), { max: 100, suffix: '%' }));
  readonly groups = computed(() => {
    const d = this.data();
    return d.byReq.map((g: any) => [g.label, g]).concat(d.bySev.map((g: any) => [g.sev + ' severity', g]))
      .concat(this.pay() ? d.milestones.map((g: any) => ['1 Dec: ' + g.name, g]) : []);
  });
  readonly list = computed(() => {
    const q = this.q().trim().toLowerCase(), fr = this.fr(), fs = this.fs(), fm = this.fm();
    return this.data().fields.filter((x: any) => (!q || (x.d + ' ' + x.f + ' ' + x.k + ' ' + x.why + ' ' + x.req).toLowerCase().includes(q)) &&
      (!fr || x.reqClass === fr) && (!fs || x.sev === fs) && (!fm || x.milestone === fm));
  });
  p(x: number | null | undefined) {
    return x == null ? '–' : x + '%';
  }
  open(dp: string) {
    this.router.navigate(['/fields', dp]);
  }
  exportCsv() {
    download(this.C.dataPageCSV(this.data()), this.pay() ? 'allshares_pay_data_fields.csv' : 'allshares_company_data_fields.csv');
  }
}

// ------------------------------------------------------------------ Export for Claude (SPEC 6.3, 14)
@Component({
  selector: 'app-export',
  template: `
    <div class="export">
      <div class="title">Export for Claude: the data in the current filters, ready to paste or upload</div>
      <div class="sub">Markdown with CSV tables and a short legend, so Claude can read it without the dashboard. Global filters apply. Paste small exports into a chat; download large ones and upload the file.</div>
      <div class="vis card">
        <div class="checks">
          @for (o of parts; track o[0]) {<label><input type="checkbox" class="form-check-input" [checked]="opts()[o[0]]" (change)="set(o[0], $any($event.target).checked)"> {{ o[1] }}</label>}
        </div>
        <div class="bar">
          <div class="opt"><label class="form-label">Values</label><select class="form-select form-select-sm" (change)="set('values', $any($event.target).value)">
            @for (v of valueModes; track v[0]) {<option [value]="v[0]" [selected]="opts().values === v[0]">{{ v[1] }}</option>}</select></div>
          <div class="opt" style="flex-basis:120px"><label class="form-label">Max value rows</label><input class="form-control form-control-sm" type="number" min="0" title="0 = all" [value]="opts().maxValues" (change)="set('maxValues', +$any($event.target).value || 0)"></div>
          <label><input type="checkbox" class="form-check-input" [checked]="opts().compact" (change)="set('compact', $any($event.target).checked)"> Compact values (no URL and note columns)</label>
        </div>
        <div class="sizeinfo">{{ C.fmt(text().length) }} characters, about {{ C.fmt(tokens()) }} tokens.
          @if (tokens() > 150000) {<b>Large: download the .md file and upload it to Claude</b>, or set Values to “No value rows” to paste.} @else {Small enough to paste into a chat.}</div>
        <div class="bar"><button class="btn btn-primary btn-sm" (click)="copy()">Copy to clipboard</button><button class="btn btn-outline-primary btn-sm" (click)="save()">Download .md</button>
          <button class="btn btn-outline-primary btn-sm" (click)="saveCsv()">Download values CSV (all columns)</button><span class="hint">{{ status() }}</span></div>
        <textarea readonly aria-label="Export preview" [value]="preview()"></textarea>
        <div class="note">Filters: {{ C.filterText(r.filters(), r.model) }}. Notes are taken from the Notes bar (right edge).</div>
      </div>
    </div>`
})
export class ExportPage {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly parts: [string, string][] = [['summary', 'Summary KPIs'], ['sources', 'Companies: reports, links and coverage'], ['coverage', 'Field coverage'], ['notFound', 'Not found by field and country'], ['notes', 'My notes']];
  readonly valueModes: [string, string][] = [['none', 'No value rows'], ['filled', 'Filled values'], ['empty', 'Empty values'], ['all', 'All values']];
  readonly opts = signal<any>({ ...this.C.EXPORT_DEFAULTS });
  readonly status = signal('');
  readonly text = computed(() => this.C.claudeExport(this.r.model, this.r.view(), this.opts(), { filters: this.r.filters(), notes: this.r.notes() }));
  readonly tokens = computed(() => Math.round(this.text().length / 4));
  readonly preview = computed(() => { const t = this.text(), L = 60000; return t.length > L ? t.slice(0, L) + '\n\n… preview cut at ' + this.C.fmt(L) + ' characters. Copy and Download include everything.' : t; });
  set(k: string, v: any) {
    this.opts.update((o: any) => ({ ...o, [k]: v }));
  }
  private stamp() {
    return new Date().toISOString().slice(0, 10);
  }
  copy() {
    UI.copyText(this.text()).then((ok) => this.status.set(ok ? 'Copied ' + this.C.fmt(this.text().length) + ' characters.' : 'Copy failed: use Download instead.'));
  }
  save() {
    download(this.text(), 'allshares_export_' + this.stamp() + '.md', 'text/markdown;charset=utf-8');
  }
  saveCsv() {
    const mode = this.opts().values;
    download(this.C.valuesCSV(this.r.model, this.C.exportValues(this.r.view(), mode === 'none' ? 'all' : mode), false), 'allshares_values_' + this.stamp() + '.csv');
  }
}
