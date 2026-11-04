import { Component, computed, inject, signal } from '@angular/core';
import { Chart } from '../chart';
import * as G from '../chart';
import { download } from '../download';
import { ReportService } from '../report.service';


@Component({
  selector: 'app-ranges',
  imports: [Chart],
  template: `
    @let o = opts();
    @let res = result();
    <div class="title">{{ title() }}</div>
    <div class="sub">Provisional ranges from the sample: NOT Allshares-approved and not used in scoring (NUM-04 stays NOT RUN). Linear-interpolation percentiles, as Excel PERCENTILE.INC. Global filters apply.</div>
    <div class="vis card"><h3>Range options</h3>
      <div class="bar">
        <div class="opt"><label class="form-label">Field</label><select class="form-select form-select-sm" (change)="set('field', val($event))"><option value="">All fields</option>@for (f of choices().fields; track f) {<option [value]="f" [selected]="o.field === f">{{ f }}</option>}</select></div>
        <div class="opt"><label class="form-label">Unit / currency</label><select class="form-select form-select-sm" (change)="set('unit', val($event))"><option value="">All units</option>@for (u of choices().units; track u) {<option [value]="u" [selected]="o.unit === u">{{ u }}</option>}</select></div>
        <div class="opt"><label class="form-label">Grain</label><select class="form-select form-select-sm" (change)="set('grain', val($event))"><option value="" [selected]="!o.grain">All</option><option value="company" [selected]="o.grain === 'company'">Company</option><option value="role" [selected]="o.grain === 'role'">Role</option></select></div>
        <div class="opt"><label class="form-label">Method</label><select class="form-select form-select-sm" (change)="set('method', val($event))"><option value="">All methods</option>@for (m of choices().methods; track m) {<option [value]="m" [selected]="o.method === m">{{ m }}</option>}</select></div>
        <div class="opt"><label class="form-label">Include values</label><select class="form-select form-select-sm" (change)="set('include', val($event))"><option value="all" [selected]="o.include === 'all'">All found values</option><option value="nohard" [selected]="o.include === 'nohard'">Exclude hard fails</option><option value="passreview" [selected]="o.include === 'passreview'">Pass and Review only</option></select></div>
        <div class="opt" style="flex-basis:90px"><label class="form-label">Low pct</label><input class="form-control form-control-sm" type="number" min="0" max="100" [value]="o.low" (change)="set('low', +val($event))"></div>
        <div class="opt" style="flex-basis:90px"><label class="form-label">High pct</label><input class="form-control form-control-sm" type="number" min="0" max="100" [value]="o.high" (change)="set('high', +val($event))"></div>
        <div class="opt" style="flex-basis:90px"><label class="form-label">Min n</label><input class="form-control form-control-sm" type="number" min="1" [value]="o.minN" (change)="set('minN', +val($event) || 1)"></div>
      </div>
      <div class="bar">
        <label class="form-check-label"><input class="form-check-input me-1" type="checkbox" [checked]="o.excludeZeros" (change)="set('excludeZeros', chk($event))"> Exclude zeros</label>
        <label class="form-check-label"><input class="form-check-input me-1" type="checkbox" [checked]="o.excludeUnknownUnits" (change)="set('excludeUnknownUnits', chk($event))"> Exclude unknown or non-ISO units</label>
        <label class="form-check-label"><input class="form-check-input me-1" type="checkbox" [checked]="o.byCountry" (change)="set('byCountry', chk($event))"> Split by country</label>
        <button class="btn btn-outline-secondary btn-sm" (click)="reset()">Reset options</button>
        <button class="btn btn-primary btn-sm" (click)="exportCsv()">Export CSV</button>
      </div>
    </div>
    <div class="vis card"><h3>Values per range row (top 12; grey when n is under 10)</h3><app-chart [options]="chart()" [height]="332" /></div>
    <div class="vis card"><div class="tbl tall"><table class="table table-sm table-hover">
      <thead><tr><th>Field</th><th>Unit / currency</th>@if (o.byCountry) {<th>Country</th>}<th class="n">Values (n)</th><th class="n">Companies</th><th class="n">Min</th><th class="n">{{ res.lowLabel }}th percentile</th><th class="n">Median</th><th class="n">{{ res.highLabel }}th percentile</th><th class="n">Max</th><th>Data caveat</th></tr></thead>
      <tbody>@for (x of res.rows; track $index) {<tr><td>{{ x.d }}</td><td>{{ x.unit }}</td>@if (o.byCountry) {<td>{{ x.c }}</td>}<td class="n">{{ x.n }}</td><td class="n">{{ x.companies }}</td><td class="n">{{ C.fmt(x.min) }}</td><td class="n">{{ C.fmt(x.low) }}</td><td class="n">{{ C.fmt(x.median) }}</td><td class="n">{{ C.fmt(x.high) }}</td><td class="n">{{ C.fmt(x.max) }}</td><td class="iss">{{ x.caveat }}</td></tr>}
      @empty {<tr><td colspan="11">No numeric values for these options.</td></tr>}</tbody></table></div></div>`
})
export class Ranges {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly opts = signal<any>({ ...this.C.RANGE_DEFAULTS });
  readonly choices = computed(() => this.C.rangeOptions(this.r.view()));
  readonly result = computed(() => this.C.ranges(this.r.view(), this.opts()));
  readonly title = computed(() => {
    const rows = this.result().rows, small = rows.filter((x: any) => x.n < 10).length;
    return rows.length ? `${rows.length} range rows from ${this.C.fmt(rows.reduce((a: number, x: any) => a + x.n, 0))} values; ${small} have n under 10 (indicative only)` : 'No numeric values for these options';
  });
  readonly chart = computed(() => G.hbars(this.result().rows.slice().sort((a: any, b: any) => b.n - a.n).slice(0, 12)
    .map((x: any) => ({ label: x.d + ' · ' + x.unit + (x.c ? ' · ' + x.c : ''), value: x.n, color: x.n < 10 ? '#888888' : '#0077BB' }))));
  val(e: Event) { return (e.target as HTMLInputElement).value; }
  chk(e: Event) { return (e.target as HTMLInputElement).checked; }
  set(k: string, v: any) { this.opts.update((o) => ({ ...o, [k]: v })); }
  reset() { this.opts.set({ ...this.C.RANGE_DEFAULTS }); }
  exportCsv() { download(this.C.rangesCSV(this.result()), 'allshares_provisional_ranges.csv'); }
}

@Component({
  selector: 'app-import',
  template: `
    <div class="title">Import data</div>
    <div class="sub">Load a results CSV in the schema below. A company is matched by LEI when given and known, otherwise by name and country; then by field ID, role row and data point. Reset restores the tracker values. Imports stay in this browser session.</div>
    <div class="vis card">
      <h3>1. Choose a file</h3>
      <input class="form-control form-control-sm" type="file" accept=".csv,text/csv" (change)="pick($event)" #file>
      <div style="margin-top:8px"><button class="btn btn-link btn-sm mono" (click)="template()">Download blank template</button></div>
      @if (pending(); as p) {
        <div style="margin-top:10px">
          <div>Rows in file: <b>{{ p.rows }}</b>. Valid rows: <b>{{ p.good.length }}</b>.</div>
          <div style="margin-top:6px">If imported: <b>{{ p.preview.counts.added }}</b> added, <b>{{ p.preview.counts.updated }}</b> updated, <b>{{ p.preview.counts.same }}</b> unchanged, <b>{{ p.preview.counts.dupes }}</b> duplicate rows in file (last row wins), <b>{{ p.preview.counts.ambiguous }}</b> ambiguous (need data_point).</div>
          @if (hardErrors().length) {<div class="err" style="margin-top:6px">Rows with errors are skipped. Fix the file to import them.</div>} @else {<div class="ok" style="margin-top:6px">File matches the schema.</div>}
        </div>
      }
      @if (applied()) {<div class="ok" style="margin-top:8px">{{ applied() }}</div>}
      <div style="margin-top:10px">
        <button class="btn btn-primary btn-sm" [disabled]="!pending()?.good.length" (click)="apply()">Import valid rows</button>
        <button class="btn btn-outline-secondary btn-sm" (click)="reset(file)">Reset to tracker values</button>
      </div>
    </div>
    <div class="vis card"><h3>2. Errors (first 50)</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Row</th><th>Column</th><th>Problem</th></tr></thead>
      <tbody>@for (e of errors().slice(0, 50); track $index) {<tr><td>{{ e.row || 'header' }}</td><td>{{ e.col }}</td><td [class]="e.warn ? 'ok' : 'err'">{{ e.msg }}</td></tr>}
      @empty {<tr><td colspan="3" class="ok">{{ pending() ? 'No errors.' : 'No file loaded.' }}</td></tr>}</tbody></table></div></div>
    <div class="grid">
      <div class="vis card"><h3>Schema columns</h3><div class="tbl"><table class="table table-sm table-hover"><thead><tr><th>Column</th><th>Required</th><th>Allowed / notes</th></tr></thead>
        <tbody>@for (c of S.columns; track c.name) {<tr><td class="mono">{{ c.name }}</td><td>{{ c.required ? 'Yes' : 'No' }}</td><td>{{ c.allowed ? c.allowed.join(', ') : c.description }}</td></tr>}</tbody></table></div></div>
      <div class="vis card"><h3>Protocol field IDs</h3><div class="tbl"><table class="table table-sm table-hover"><thead><tr><th>ID</th><th>Field</th></tr></thead>
        <tbody>@for (k of ids; track k) {<tr><td>{{ k }}</td><td>{{ S.field_ids[k] }}@if (S.ambiguous_field_ids.includes(k)) { <span class="hint">(needs data_point)</span>}</td></tr>}</tbody></table></div></div>
    </div>
    <details class="vis card"><summary style="cursor:pointer;font-weight:600">Full schema (JSON)</summary><pre class="mono" style="white-space:pre-wrap;max-height:360px;overflow:auto">{{ json }}</pre></details>`
})
export class Import {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly S = this.r.schema;
  readonly ids = Object.keys(this.S.field_ids);
  readonly json = JSON.stringify(this.S, null, 2);
  readonly pending = signal<any>(null);
  readonly applied = signal('');
  readonly errors = computed(() => { const p = this.pending(); return p ? p.errs.concat(p.preview.errs) : []; });
  readonly hardErrors = computed(() => this.errors().filter((e: any) => !e.warn));

  pick(ev: Event) {
    const f = (ev.target as HTMLInputElement).files?.[0];
    if (!f) return;
    f.text().then((t) => this.preview(t, f.name));
  }
  preview(text: string, name: string) {
    this.applied.set('');
    this.pending.set(this.C.previewImport(this.r.model, this.S, text, name));
  }
  apply() {
    const p = this.pending();
    if (!p || !p.good.length) return;
    const c = this.C.commitImport(this.r.model, p).counts;
    this.pending.set(null);
    this.applied.set(`Import applied: ${c.added} added, ${c.updated} updated, ${c.same} unchanged. Source = Imported and all pages now use the new values.`);
    this.r.touch();
  }
  reset(file?: HTMLInputElement) {
    this.C.resetModel(this.r.model);
    this.pending.set(null);
    this.applied.set('Reset to tracker values. All imports removed.');
    if (file) file.value = '';
    this.r.touch();
  }
  template() {
    download(this.S.columns.map((c: any) => c.name).join(',') + '\n', 'allshares_results_template.csv');
  }
}
