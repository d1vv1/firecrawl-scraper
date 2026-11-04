import { Component, computed, inject } from '@angular/core';
import { Chart } from '../chart';
import * as G from '../chart';
import { ReportService } from '../report.service';
import { Legend } from '../svg';
import { download } from '../download';

@Component({
  selector: 'app-overview',
  imports: [Chart, Legend],
  template: `
    @let o = data();
    <div class="title">{{ r.titles()['overview'] }}</div>
    <div class="sub">{{ C.fmt(o.n) }} values from {{ o.companies }} companies in the current filters.</div>
    @if (dup()) {<div class="attn info alert alert-warning">{{ dup() }}</div>}
    <div class="grid">
      <div class="vis card"><h3>Companies run by country</h3><app-chart [options]="chCompanies()" /></div>
      <div class="vis card"><h3>Value status</h3><app-chart [options]="chStatus()" /><app-legend [items]="statusLegend()" /></div>
    </div>
    <div class="vis card"><h3>Country summary</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Country</th><th class="n">Companies</th><th class="n">Values</th><th class="n">Found</th><th class="n">Partial</th><th class="n">Not found</th><th class="n">Found %</th></tr></thead>
      <tbody>@for (x of o.rows; track x.c) {<tr><td>{{ x.c }}</td><td class="n">{{ x.companies }}</td><td class="n">{{ C.fmt(x.n) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td><td class="n">{{ x.foundPct }}%</td></tr>}
      @empty {<tr><td colspan="7">No data for this selection.</td></tr>}</tbody></table></div></div>`
})
export class Overview {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly data = computed(() => this.C.overview(this.r.view()));
  readonly statusLegend = computed(() => this.C.VSTAT.map((x) => ({ label: x[1], color: x[2], value: this.data().st[x[0]] })));
  readonly chCompanies = computed(() => G.bars(this.data().byCountryCompanies.map((x: any, i: number) => ({ label: x.c, value: x.n, color: this.C.PAL[i % 5] }))));
  readonly chStatus = computed(() => G.pie(this.statusLegend()));
  readonly dup = computed(() => {
    const m = this.r.model.data.meta, d = m.duplicates[0];
    return d ? `Data note: the tracker has ${m.companyIds} company IDs, but ${d.ids.join(' and ')} share one LEI (${d.lei}), so they count as one company: ${m.companies} companies. Rows for both IDs remain in the values.` : '';
  });
}
@Component({
  selector: 'app-paycomp',
  imports: [Chart, Legend],
  template: `
    <div class="title">{{ r.titles()['paycomp'] }}</div>
    <div class="sub">Pay data: policy, role and all pay fields. Company data: identity, listing, financials, workforce, ownership, segments.</div>
    <div class="grid">
      <div class="vis card"><h3>Status by data type</h3><app-chart [options]="chPC()" /><app-legend [items]="leg" /></div>
      <div class="vis card"><h3>Share of values</h3><app-chart [options]="chPie()" /></div>
    </div>
    <div class="vis card"><h3>Pay vs company by country</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Country</th><th class="n">Company values</th><th class="n">Company found %</th><th class="n">Pay values</th><th class="n">Pay found %</th></tr></thead>
      <tbody>@for (x of data().rows; track x.c) {<tr><td>{{ x.c }}</td><td class="n">{{ C.fmt(x.co) }}</td><td class="n">{{ x.coFound }}%</td><td class="n">{{ C.fmt(x.pa) }}</td><td class="n">{{ x.paFound }}%</td></tr>}</tbody></table></div></div>`
})
export class PayComp {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly leg = this.C.VSTAT.map((x) => ({ label: x[1], color: x[2] }));
  readonly data = computed(() => this.C.payComp(this.r.view()));
  readonly chPC = computed(() => { const p = this.data(); return G.stacked(['Company data', 'Pay data'], this.C.VSTAT.map((x) => ({ name: x[1], color: x[2], values: [p.sc[x[0]], p.sp[x[0]]] }))); });
  readonly chPie = computed(() => G.pie([{ label: 'Company data', value: this.data().co, color: '#0077BB' }, { label: 'Pay data', value: this.data().pa, color: '#EE7733' }]));
}

@Component({
  selector: 'app-countries',
  imports: [Chart, Legend],
  template: `
    <div class="title">{{ r.titles()['countries'] }}</div>
    <div class="sub">Status of values by country, with the companies run in each.</div>
    <div class="grid">
      <div class="vis card"><h3>Status by country</h3><app-chart [options]="chStatus()" /><app-legend [items]="leg" /></div>
      <div class="vis card"><h3>Companies by country</h3><app-chart [options]="chCo()" /></div>
    </div>
    <div class="vis card"><h3>Detail by country and data type</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Country</th><th>Data type</th><th class="n">Values</th><th class="n">Found</th><th class="n">Partial</th><th class="n">Not found</th></tr></thead>
      <tbody>@for (x of data().rows; track x.c + x.type) {<tr><td>{{ x.c }}</td><td>{{ x.type }}</td><td class="n">{{ C.fmt(x.n) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td></tr>}</tbody></table></div></div>`
})
export class Countries {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly leg = this.C.VSTAT.map((x) => ({ label: x[1], color: x[2] }));
  readonly data = computed(() => this.C.countriesPage(this.r.view()));
  readonly chStatus = computed(() => G.stacked(this.data().countries, this.data().series));
  readonly chCo = computed(() => G.hbars(this.data().companies.map((x: any, i: number) => ({ label: x.c, value: x.n, color: this.C.PAL[i % 5], sub: 'companies' }))));
}

@Component({
  selector: 'app-failures',
  imports: [Chart],
  template: `
    @let g = data();
    <div class="title">{{ r.titles()['failures'] }}</div>
    <div class="sub">Gate results from the scoring run, for the values in view. Imported values are not gate-scored.</div>
    <div class="attn alert alert-danger">{{ attention() }}</div>
    <div class="grid">
      <div class="vis card"><h3>Fails by check (top 12)</h3><app-chart [options]="chChecks()" [height]="332" />
        <div class="legend"><span><i style="background:#CC3311"></i>Hard</span><span><i style="background:#EE7733"></i>Soft</span></div></div>
      <div class="vis card"><h3>Hard vs soft fails</h3><app-chart [options]="chSev()" /></div>
      <div class="vis card"><h3>Fail rate by module (% of run checks)</h3><app-chart [options]="chModule()" /></div>
      <div class="vis card"><h3>Fail rate by field (top 12)</h3><app-chart [options]="chField()" [height]="332" /></div>
    </div>
    <div class="vis card"><h3>Fails by field</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Field</th><th>Group</th><th class="n">Runs</th><th class="n">Fail</th><th class="n">Hard fail</th><th class="n">Not run</th><th class="n">Fail rate</th></tr></thead>
      <tbody>@for (x of g.fields; track x.name) {<tr><td>{{ x.name }}</td><td>{{ x.cat }}</td><td class="n">{{ C.fmt(x.runs) }}</td><td class="n">{{ C.fmt(x.fail) }}</td><td class="n">{{ C.fmt(x.hard) }}</td><td class="n">{{ C.fmt(x.nr) }}</td><td class="n">{{ x.rate }}%</td></tr>}
      @empty {<tr><td colspan="7">No scored values in this selection.</td></tr>}</tbody></table></div></div>`
})
export class Failures {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly data = computed(() => this.C.gateStats(this.r.model, this.r.view()));
  readonly attention = computed(() => this.C.attention(this.r.model, this.r.view()).text);
  readonly chChecks = computed(() => G.hbars(this.data().checks.filter((x: any) => x.fail).slice(0, 12).map((x: any) => ({ label: x.id + ' ' + x.name, value: x.fail, color: x.sev === 'Hard' ? '#CC3311' : '#EE7733', sub: x.sev }))));
  readonly chSev = computed(() => G.pie([{ label: 'Hard', value: this.data().hard, color: '#CC3311' }, { label: 'Soft', value: this.data().soft, color: '#EE7733' }]));
  readonly chModule = computed(() => G.bars(this.data().modules.map((m: any, i: number) => ({ label: m.name.replace('Company and ownership', 'Company & own.').replace('Reference data', 'Reference'), value: m.rate, color: this.C.PAL[i % 5] })), { max: 100, suffix: '%' }));
  readonly chField = computed(() => G.hbars(this.data().ranked.slice(0, 12).map((x: any) => ({ label: x.name, value: x.rate, color: '#CC3311', sub: x.fail + ' fails' })), { max: 100, suffix: '%' }));
}

@Component({
  selector: 'app-trend',
  imports: [Chart, Legend],
  template: `
    <div class="title">{{ r.titles()['trend'] }}</div>
    <div class="sub">Checks passing and found %, from the tracker baseline and after each import. Tracker: share of run checks that passed. Imports: share of rows passing every schema check; found % is across all values after the import.</div>
    <div class="vis card"><h3>Trend</h3><app-chart [options]="chart()" /><app-legend [items]="leg()" /></div>
    <div class="vis card"><h3>Schema checks by import (% of rows passing)</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Import</th><th class="n">Rows</th><th class="n">Checks passing</th><th class="n">Found % (all values)</th><th class="n">Found % (file)</th>@for (g of C.GROUPS; track g) {<th class="n">{{ g }}</th>}</tr></thead>
      <tbody>@for (p of hist(); track $index) {<tr><td>{{ $index === 0 ? 'Tracker (baseline)' : p.label }}</td><td class="n">{{ p.n == null ? '–' : C.fmt(p.n) }}</td><td class="n"><b>{{ p.checks }}%</b></td><td class="n">{{ p.found }}%</td><td class="n">{{ p.fileFound == null ? '–' : p.fileFound + '%' }}</td>
        @for (g of C.GROUPS; track g) {<td class="n">{{ p.groups?.[g] == null ? '–' : p.groups![g] + '%' }}</td>}</tr>}</tbody></table></div>
      <div class="note">Import checks are the schema rules run on each file. Gate checks are not run on imports yet.</div></div>`
})
export class Trend {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly hist = computed(() => { this.r.version(); return this.r.model.hist.slice(); });
  readonly chart = computed(() => G.line(this.hist().map((p, i) => ({ label: p.label, short: i === 0 ? 'Tracker' : '#' + i, checks: p.checks, found: p.found })), this.r.model.data.meta.target));
  readonly leg = computed(() => [{ label: 'Checks passing %', color: '#0077BB' }, { label: 'Found %', color: '#009988' }, { label: 'Target ' + this.r.model.data.meta.target + '%', color: '#888888' }]);
}

@Component({
  selector: 'app-metrics',
  template: `
    <div class="title">Metric register: what each KPI measures and where it comes from</div>
    <div class="sub">Live for the current filters. Targets are shown only where agreed; owners are not assigned until Allshares names them.</div>
    <div class="vis card"><div style="margin-bottom:8px"><button class="btn btn-primary btn-sm" (click)="exportCsv()">Export CSV</button></div>
      <div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr><th>Metric</th><th>Category</th><th>Source module</th><th>Formula or method</th><th>Period</th><th class="n">Value</th><th class="n">Target</th><th>Trend</th><th>Owner</th><th>Last updated</th><th>Metric ID</th></tr></thead>
        <tbody>@for (m of rows(); track m.id) {<tr><td><b>{{ m.metric }}</b></td><td>{{ m.category }}</td><td>{{ m.module }}</td><td>{{ m.formula }}</td><td>{{ m.period }}</td><td class="n">{{ m.value == null ? '–' : C.fmt(m.value) }}</td><td class="n">{{ m.target }}</td><td>{{ m.trend }}</td><td>{{ m.owner }}</td><td>{{ m.updated }}</td><td class="mono">{{ m.id }}</td></tr>}</tbody>
      </table></div></div>`
})
export class Metrics {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly rows = computed(() => this.C.metrics(this.r.model, this.r.view()));
  exportCsv() {
    download(this.C.metricsCSV(this.rows()), 'allshares_metric_register.csv');
  }
}
