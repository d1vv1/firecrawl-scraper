import { Component, computed, inject, input, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { Chart } from '../chart';
import * as G from '../chart';
import { ReportService } from '../report.service';
import { Chip, Legend } from '../svg';

type Sort = { k: string; dir: number };
function sortBy<T extends Record<string, any>>(arr: T[], s: Sort): T[] {
  return arr.slice().sort((a, b) => {
    let x = a[s.k], y = b[s.k];
    if (x == null) x = -1;
    if (y == null) y = -1;
    return (typeof x === 'string' ? x.localeCompare(y) : x - y) * s.dir;
  });
}
function nextSort(s: Sort, k: string): Sort {
  return { k, dir: s.k === k ? -s.dir : /^(d|f|k|o|c)$/.test(k) ? 1 : -1 };
}

/** Failed / not-run gates of one value. */
@Component({
  selector: 'app-issues',
  template: `@for (i of items(); track i.gate) {<div class="iss"><b>{{ i.gate }}</b> {{ i.sev === 'Hard' ? 'hard ' : '' }}{{ i.res }}@if (i.reason) {: {{ i.reason }}}</div>}`
})
export class Issues {
  readonly items = input<any[]>([]);
}

@Component({
  selector: 'app-fields',
  imports: [Chart, Legend, Chip, Issues, RouterLink],
  template: `
    <div class="title">{{ r.titles()['fields'] }}</div>
    <div class="sub">Each data point: how many values were found, and how its scored values came out. Click a field to see every value.</div>
    <div class="vis card"><h3>{{ chartTitle() }}</h3><app-chart [options]="chart()" [height]="332" /><app-legend [items]="leg" /></div>
    <div class="vis card">
      <div class="bar"><div class="opt" style="flex:1 1 240px"><label class="form-label">Search fields</label><input class="form-control form-control-sm" type="search" placeholder="Field, ID or group" [value]="q()" (input)="q.set($any($event.target).value)"></div></div>
      <div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr>
          @for (h of heads; track h[0]) {<th [class.n]="h[2]" (click)="sort.set(next(h[0]))">{{ h[1] }}{{ sort().k === h[0] ? (sort().dir > 0 ? ' ▲' : ' ▼') : '' }}</th>}<th></th>
        </tr></thead>
        <tbody>
          @for (x of list(); track x.d) {
            <tr class="click" [class.sel]="dp() === x.d" tabindex="0" [routerLink]="['/fields', x.d]">
              <td>{{ x.d }}</td><td>{{ x.f }}</td><td>{{ x.k }}</td><td class="n">{{ C.fmt(x.rows) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td>
              <td class="n">{{ C.fmt(x.P) }}</td><td class="n">{{ C.fmt(x.R) }}</td><td class="n">{{ C.fmt(x.I) }}</td><td class="n">{{ C.fmt(x.F) }}</td><td class="n">{{ C.fmt(x.H) }}</td>
              <td class="n">{{ x.scored ? x.passPct + '%' : '–' }}</td><td class="n">{{ x.avg ?? '–' }}</td><td>›</td></tr>
          } @empty {<tr><td colspan="15">No data for this selection.</td></tr>}
        </tbody></table></div>
    </div>
    @if (detail(); as d) {
      <div class="vis card">
        <div class="back"><a class="btn btn-link btn-sm" routerLink="/fields">← Close field</a></div>
        <h3>{{ d.dp }} ({{ d.meta.f }}, {{ d.meta.k }}): {{ C.fmt(d.values.length) }} values, {{ C.fmt(d.empty.length) }} empty</h3>
        <div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Company</th><th>Country</th><th>Role</th><th>Value</th><th>Unit</th><th>Period</th><th>Status</th><th class="n">Score</th><th>Failed / not run gates</th></tr></thead>
          <tbody>@for (v of d.values; track $index) {
            <tr class="click" tabindex="0" [routerLink]="['/companies', v.key]"><td>{{ v.o }}</td><td>{{ v.c }}</td><td>{{ v.r }}</td><td>{{ v.v.slice(0, 120) }}</td><td>{{ v.u }}</td><td>{{ v.pe }}</td>
              <td><app-chip [sc]="v.sc" [name]="v.scName" /></td><td class="n">{{ v.sp ?? '–' }}</td><td><app-issues [items]="v.issues" /></td></tr>
          }</tbody></table></div>
        @if (d.empty.length) {
          <h3 style="margin-top:12px">Empty for</h3>
          <div class="tbl"><table class="table table-sm table-hover"><thead><tr><th>Company</th><th>Country</th><th>Role</th><th>Note</th></tr></thead>
            <tbody>@for (e of d.empty; track $index) {<tr class="click" tabindex="0" [routerLink]="['/companies', e.key]"><td>{{ e.o }}</td><td>{{ e.c }}</td><td>{{ e.r }}</td><td>{{ e.note }}</td></tr>}</tbody></table></div>
        }
      </div>
    }`
})
export class Fields {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly dp = input<string>('');
  readonly q = signal('');
  readonly sort = signal<Sort>({ k: 'problems', dir: -1 });
  readonly next = (k: string) => nextSort(this.sort(), k);
  readonly heads: [string, string, boolean][] = [['d', 'Field', false], ['f', 'ID', false], ['k', 'Group', false], ['rows', 'Rows', true], ['found', 'Found', true], ['partial', 'Partial', true],
    ['nf', 'Not found', true], ['P', 'Pass', true], ['R', 'Review', true], ['I', 'Incomplete', true], ['F', 'Fail', true], ['H', 'Fail (hard)', true], ['passPct', 'Pass %', true], ['avg', 'Avg score', true]];
  readonly leg = this.C.SSTAT.map((s) => ({ label: s[1], color: s[2] }));
  readonly table = computed(() => this.C.fieldTable(this.r.model, this.r.view()));
  readonly list = computed(() => {
    const q = this.q().trim().toLowerCase();
    return sortBy(this.table().filter((x) => !q || (x.d + ' ' + x.f + ' ' + x.k).toLowerCase().includes(q)), this.sort());
  });
  readonly top = computed(() => this.table().filter((x) => x.scored).slice(0, 12));
  readonly chartTitle = computed(() => { const t = this.top()[0]; return t && t.problems ? `${t.d} has the most failing values (${this.C.fmt(t.problems)}); top 12 fields by failures` : 'Score status by field'; });
  readonly chart = computed(() => {
    const series = this.C.SSTAT.map((s) => ({ key: s[0], name: s[1], color: s[2] }));
    return G.stackedH(this.top().map((x) => { const o: any = { label: x.d }; series.forEach((s) => (o[s.key] = x[s.key])); return o; }), series);
  });
  readonly detail = computed(() => (this.dp() ? this.C.fieldDetail(this.r.model, this.r.view(), this.dp()) : null));
}

@Component({
  selector: 'app-empty',
  imports: [Chart, RouterLink],
  template: `
    @let e = data();
    <div class="title">{{ r.titles()['empty'] }}</div>
    <div class="sub">Values with no result in any source tried (status not_found). {{ C.fmt(e.n) }} empty values across {{ e.fields.length }} fields and {{ e.affected }} companies. Click a company to open it.</div>
    <div class="grid">
      <div class="vis card"><h3>{{ e.fields.length ? 'Fields empty most often: ' + e.fields[0].d + ' leads with ' + C.fmt(e.fields[0].empty) : 'Fields empty most often' }}</h3><app-chart [options]="chTop()" [height]="332" /></div>
      <div class="vis card"><h3>Empty values by data type</h3><app-chart [options]="chType()" /></div>
    </div>
    <div class="vis card"><h3>Empty by field</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Field</th><th>Group</th><th>Grain</th><th class="n">Rows</th><th class="n">Empty</th><th class="n">Empty %</th><th class="n">Companies with it empty</th></tr></thead>
      <tbody>@for (x of e.fields; track x.d) {<tr class="click" tabindex="0" [routerLink]="['/fields', x.d]"><td>{{ x.d }}</td><td>{{ x.k }}</td><td>{{ x.g }}</td><td class="n">{{ C.fmt(x.rows) }}</td><td class="n">{{ C.fmt(x.empty) }}</td><td class="n">{{ x.pct }}%</td><td class="n">{{ x.companies }}</td></tr>}
      @empty {<tr><td colspan="7">No empty values in this selection.</td></tr>}</tbody></table></div></div>
    <div class="vis card"><h3>Empty by company</h3><div class="tbl"><table class="table table-sm table-hover">
      <thead><tr><th>Company</th><th>Country</th><th class="n">Rows</th><th class="n">Empty</th><th class="n">Empty %</th><th>Empty fields</th><th></th></tr></thead>
      <tbody>@for (c of withEmpty(); track c.key) {<tr class="click" tabindex="0" [routerLink]="['/companies', c.key]"><td>{{ c.o }}</td><td>{{ c.c }}</td><td class="n">{{ C.fmt(c.rows) }}</td><td class="n">{{ C.fmt(c.empty) }}</td><td class="n">{{ c.pct }}%</td><td class="iss">{{ c.fieldList.join(', ') }}</td><td>›</td></tr>}
      @empty {<tr><td colspan="7">No empty values in this selection.</td></tr>}</tbody></table></div></div>`
})
export class Empty {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly data = computed(() => this.C.emptyTables(this.r.model, this.r.view()));
  readonly withEmpty = computed(() => this.data().companies.filter((c: any) => c.empty));
  readonly chTop = computed(() => G.hbars(this.data().fields.slice(0, 12).map((x: any) => ({ label: x.d, value: x.empty, color: '#CC3311', sub: x.pct + '%' }))));
  readonly chType = computed(() => G.pie(this.data().byType));
}

@Component({
  selector: 'app-companies',
  imports: [Chart, Chip, Issues, RouterLink],
  template: `
    @if (!key()) {
      <div class="title">{{ listTitle() }}</div>
      <div class="sub">One row per company, counted by LEI. Click a company to drill into its values and gate results.</div>
      <div class="vis card">
        <div class="bar"><div class="opt" style="flex:1 1 240px"><label class="form-label">Search companies</label><input class="form-control form-control-sm" type="search" placeholder="Name, ID or LEI" [value]="q()" (input)="q.set($any($event.target).value)"></div></div>
        <div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr>@for (h of heads; track h[0]) {<th [class.n]="h[2]" (click)="h[0] && sort.set(next(h[0]))">{{ h[1] }}{{ sort().k === h[0] ? (sort().dir > 0 ? ' ▲' : ' ▼') : '' }}</th>}<th></th></tr></thead>
          <tbody>@for (x of list(); track x.key) {
            <tr class="click" tabindex="0" [routerLink]="['/companies', x.key]"><td>{{ x.o }}</td><td>{{ x.c }}</td><td class="mono">{{ x.idList.join(', ') }}</td><td class="n">{{ C.fmt(x.rows) }}</td><td class="n">{{ C.fmt(x.found) }}</td><td class="n">{{ C.fmt(x.partial) }}</td><td class="n">{{ C.fmt(x.nf) }}</td>
              <td class="n">{{ C.fmt(x.P) }}</td><td class="n">{{ C.fmt(x.R) }}</td><td class="n">{{ C.fmt(x.I) }}</td><td class="n">{{ C.fmt(x.F) }}</td><td class="n">{{ C.fmt(x.H) }}</td><td class="n">{{ x.avg ?? '–' }}</td><td>›</td></tr>
          } @empty {<tr><td colspan="14">No companies in this selection.</td></tr>}</tbody></table></div>
      </div>
    } @else {
      <div class="back"><a class="btn btn-link btn-sm" routerLink="/companies">← Back to companies</a></div>
      @if (detail(); as d) {
        <div class="title">{{ d.name }}: {{ C.fmt(d.sc.P) }} of {{ C.fmt(d.sc.scored) }} scored values pass, {{ C.fmt(d.sc.H) }} blocked by a hard fail</div>
        <div class="sub">{{ d.country }} · IDs {{ d.ids.join(', ') }}@if (d.lei) { · LEI <span class="mono">{{ d.lei }}</span>} · {{ C.fmt(d.st.found) }} found, {{ C.fmt(d.st.partial) }} partial, {{ C.fmt(d.st.not_found) }} empty</div>
        @if (d.duplicate) {<div class="attn info alert alert-warning">Same company under IDs {{ d.duplicate.ids.join(' and ') }} (one LEI). Rows for both IDs are shown.</div>}
        <div class="grid">
          <div class="vis card"><h3>Scored values by status ({{ C.fmt(d.st.not_found) }} empty values not scored)</h3><app-chart [options]="pie()" /></div>
          <div class="vis card"><h3>{{ fails().length ? 'Failing gates: ' + fails()[0].id + ' fails most (' + fails()[0].fail + ')' : 'No failing gates' }}</h3><app-chart [options]="failChart()" [height]="332" /></div>
        </div>
        <div class="vis card">
          <div class="bar"><div class="opt"><label class="form-label">Show</label>
            <select class="form-select form-select-sm" (change)="mode.set($any($event.target).value)">
              <option value="all" [selected]="mode() === 'all'">All values</option><option value="problems" [selected]="mode() === 'problems'">Problems only</option><option value="empty" [selected]="mode() === 'empty'">Empty only</option>
            </select></div></div>
          <div class="tbl tall"><table class="table table-sm table-hover">
            <thead><tr><th>Group</th><th>Field</th>@if (d.ids.length > 1) {<th>ID</th>}<th>Role</th><th>Value</th><th>Unit</th><th>Period</th><th>Method</th><th>Status</th><th class="n">Score</th><th>Failed / not run gates</th><th>Source</th></tr></thead>
            <tbody>@for (v of d.values; track $index) {
              <tr><td>{{ v.k }}</td><td>{{ v.d }} <span class="hint">{{ v.f }}</span></td>@if (d.ids.length > 1) {<td class="mono">{{ v.id }}</td>}<td>{{ v.r }}</td><td>{{ v.v.slice(0, 160) }}</td><td>{{ v.u }}</td><td>{{ v.pe }}</td><td>{{ v.me }}</td>
                <td><app-chip [sc]="v.sc" [name]="v.scName" /></td><td class="n">{{ v.sp ?? '–' }}</td>
                <td><app-issues [items]="v.issues" />@if (v.st === 'not_found' && v.nt) {<div class="iss">{{ v.nt }}</div>}</td>
                <td>{{ v.so }}@if (isUrl(v.ep)) { <a [href]="v.ep" target="_blank" rel="noopener noreferrer">locator</a>}</td></tr>
            } @empty {<tr><td colspan="12">No values for this view.</td></tr>}</tbody></table></div>
        </div>
      } @else {
        <div class="vis card">This company has no values in the current filters.</div>
      }
    }`
})
export class Companies {
  readonly r = inject(ReportService);
  readonly router = inject(Router);
  readonly C = this.r.C;
  readonly key = input<string>('');
  readonly q = signal('');
  readonly mode = signal('all');
  readonly sort = signal<Sort>({ k: 'c', dir: 1 });
  readonly next = (k: string) => nextSort(this.sort(), k);
  readonly heads: [string, string, boolean][] = [['o', 'Company', false], ['c', 'Country', false], ['', 'IDs', false], ['rows', 'Rows', true], ['found', 'Found', true], ['partial', 'Partial', true], ['nf', 'Not found', true],
    ['P', 'Pass', true], ['R', 'Review', true], ['I', 'Incomplete', true], ['F', 'Fail', true], ['H', 'Fail (hard)', true], ['avg', 'Avg score', true]];
  readonly table = computed(() => this.C.companyTable(this.r.model, this.r.view()));
  readonly list = computed(() => {
    const q = this.q().trim().toLowerCase();
    return sortBy(this.table().filter((x) => !q || (x.o + ' ' + x.key + ' ' + x.idList.join(' ')).toLowerCase().includes(q)), this.sort());
  });
  readonly listTitle = computed(() => {
    const l = this.table(), w = l.slice().sort((a, b) => b.H - a.H)[0];
    return l.length ? `${l.length} companies in view` + (w && w.H ? `; ${w.o} has the most hard fails (${w.H})` : '') : 'No companies in this selection';
  });
  readonly detail = computed(() => (this.key() ? this.C.companyDetail(this.r.model, this.r.view(), this.key(), this.mode()) : null));
  readonly pie = computed(() => { const d = this.detail(); return d ? G.pie(this.C.SSTAT.map((s) => ({ label: s[1], value: d.sc[s[0]], color: s[2] }))) : null; });
  readonly fails = computed(() => (this.detail()?.gates.checks || []).filter((c: any) => c.fail).slice(0, 12));
  readonly failChart = computed(() => G.hbars(this.fails().map((c: any) => ({ label: c.id + ' ' + c.name, value: c.fail, color: c.sev === 'Hard' ? '#CC3311' : '#EE7733', sub: c.sev }))));
  isUrl(s: string) {
    return /^https?:\/\//.test(s || '');
  }
}
