import { Component, computed, inject, input, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Chart } from '../chart';
import * as G from '../chart';
import { ReportService } from '../report.service';
import { Chip } from '../svg';

/** Gate result chip: PASS teal, FAIL red (hard) or orange (soft), NOT RUN grey. */
@Component({
  selector: 'app-result',
  template: `<span class="chip badge rounded-pill" [class]="'chip badge rounded-pill ' + (res() === 'P' ? 'P' : res() === 'N' ? 'I' : sev() === 'Hard' ? 'H' : 'F')">{{ res() === 'P' ? 'PASS' : res() === 'N' ? 'NOT RUN' : 'FAIL' }}</span>`
})
export class Result {
  readonly res = input('');
  readonly sev = input('');
}

@Component({
  selector: 'app-steps',
  imports: [Chart, Chip, Result, RouterLink],
  template: `
    <nav aria-label="breadcrumb"><ol class="breadcrumb crumbs">
      @if (gate()) {<li class="breadcrumb-item"><a routerLink="/steps">Validation steps</a></li>} @else {<li class="breadcrumb-item active" aria-current="page">Validation steps</li>}
      @if (gate() && dp()) {<li class="breadcrumb-item"><a [routerLink]="['/steps', gate()]">{{ gate() }}</a></li>} @else if (gate()) {<li class="breadcrumb-item active" aria-current="page">{{ gate() }}</li>}
      @if (dp()) {<li class="breadcrumb-item active" aria-current="page">{{ dp() }}</li>}
    </ol></nav>

    @if (!gate()) {
      @let s = steps();
      <div class="title">{{ s.title }}</div>
      <div class="sub">Each gate is one validation step. Steps run in families, from core checks on every value to cross-field checks. Pass rate counts run checks only (NOT RUN excluded). Click a step to see which fields it runs on.</div>
      <div class="vis card"><h3>{{ famTitle() }}</h3><app-chart [options]="famChart()" /></div>
      <div class="vis card"><div class="tbl tall"><table class="table table-sm table-hover">
        <thead><tr><th>Step</th><th>Check</th><th>Type</th><th class="n">Fields</th><th class="n">Runs</th><th class="n">PASS</th><th class="n">FAIL</th><th class="n">NOT RUN</th><th class="n">Pass rate</th><th>Most common reason</th><th></th></tr></thead>
        <tbody>
          @for (f of s.families; track f.key) {
            <tr class="group"><td colspan="11"><b>{{ f.name }}</b> · {{ f.steps }} {{ f.steps === 1 ? 'step' : 'steps' }} · {{ C.fmt(f.fail) }} {{ f.fail === 1 ? 'fail' : 'fails' }} · {{ f.runs - f.nr ? f.passPct + '% pass' : 'not run' }}</td></tr>
            @for (x of byFamily()[f.key]; track x.id) {
              <tr class="click" tabindex="0" [routerLink]="['/steps', x.id]">
                <td class="mono">{{ x.id }}</td><td>{{ x.name }}</td><td>{{ x.sev }}</td><td class="n">{{ x.fields }}</td><td class="n">{{ C.fmt(x.runs) }}</td>
                <td class="n">{{ C.fmt(x.pass) }}</td><td class="n">{{ C.fmt(x.fail) }}</td><td class="n">{{ C.fmt(x.nr) }}</td>
                <td class="n">{{ x.runs - x.nr ? x.passPct + '%' : '–' }}</td><td class="iss">{{ x.top ? x.top.text + ' (' + C.fmt(x.top.n) + ')' : '' }}</td><td>›</td></tr>
            }
          } @empty {<tr><td colspan="11">No scored values in this selection.</td></tr>}
        </tbody></table></div></div>
    } @else if (detail(); as d) {
      @if (!dp()) {
        <div class="title">{{ d.id }} {{ d.name }}: {{ C.fmt(d.counts.fail) }} fails, {{ C.fmt(d.counts.nr) }} not run, across {{ d.fields.length }} fields</div>
        <div class="sub">{{ d.family }} · {{ d.sev }} gate{{ d.sev === 'Hard' ? ': a FAIL blocks the value (Fail (hard))' : ': a FAIL lowers the score' }} · {{ C.fmt(d.counts.runs) }} runs, {{ d.counts.runs - d.counts.nr ? d.counts.passPct + '% of run checks pass' : 'none run' }}.</div>
        <div class="grid">
          <div class="vis card"><h3>{{ d.fields[0]?.fail ? 'Fails by field: ' + d.fields[0].d + ' fails most (' + d.fields[0].fail + ')' : 'No fails for this step' }}</h3><app-chart [options]="fieldChart()" [height]="332" /></div>
          <div class="vis card"><h3>Why values fail or are not run</h3><div class="tbl"><table class="table table-sm table-hover">
            <thead><tr><th>Result</th><th>Reason</th><th class="n">Values</th><th>Fields</th></tr></thead>
            <tbody>@for (r of d.reasons; track r.res + r.text) {<tr><td><app-result [res]="r.res[0] === 'P' ? 'P' : r.res[0] === 'F' ? 'F' : 'N'" [sev]="d.sev" /></td><td>{{ r.text }}</td><td class="n">{{ C.fmt(r.n) }}</td><td class="iss">{{ r.fieldList.join(', ') }}</td></tr>}
            @empty {<tr><td colspan="4" class="ok">Every value passes this step.</td></tr>}</tbody></table></div></div>
        </div>
        <div class="vis card"><h3>Fields this step runs on (click a field for its values)</h3><div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Field</th><th>ID</th><th>Group</th><th class="n">Runs</th><th class="n">PASS</th><th class="n">FAIL</th><th class="n">NOT RUN</th><th class="n">Fail rate</th><th></th></tr></thead>
          <tbody>@for (f of d.fields; track f.d) {
            <tr class="click" tabindex="0" [routerLink]="['/steps', d.id, f.d]"><td>{{ f.d }}</td><td>{{ f.f }}</td><td>{{ f.k }}</td><td class="n">{{ C.fmt(f.runs) }}</td><td class="n">{{ C.fmt(f.pass) }}</td><td class="n">{{ C.fmt(f.fail) }}</td><td class="n">{{ C.fmt(f.nr) }}</td><td class="n">{{ f.runs - f.nr ? f.failRate + '%' : '–' }}</td><td>›</td></tr>
          }</tbody></table></div></div>
      } @else {
        @let fc = fieldCounts();
        <div class="title">{{ d.id }} on {{ dp() }}: {{ C.fmt(fc.fail) }} of {{ C.fmt(fc.runs) }} values fail, {{ C.fmt(fc.nr) }} not run</div>
        <div class="sub">{{ d.id }} {{ d.name }} ({{ d.sev }}). Every value of {{ dp() }} this step checked. Click a company to open it.</div>
        <div class="vis card">
          <div class="bar"><div class="opt"><label class="form-label">Show</label>
            <select class="form-select form-select-sm" (change)="mode.set($any($event.target).value)">
              <option value="all" [selected]="mode() === 'all'">All results</option><option value="F" [selected]="mode() === 'F'">FAIL only</option>
              <option value="N" [selected]="mode() === 'N'">NOT RUN only</option><option value="P" [selected]="mode() === 'P'">PASS only</option>
            </select></div></div>
          <div class="tbl tall"><table class="table table-sm table-hover">
            <thead><tr><th>Company</th><th>Country</th><th>Role</th><th>Value</th><th>Unit</th><th>Period</th><th>Result</th><th>Reason</th><th>Value status</th><th class="n">Score</th></tr></thead>
            <tbody>@for (v of values(); track $index) {
              <tr class="click" tabindex="0" [routerLink]="['/companies', v.key]"><td>{{ v.o }}</td><td>{{ v.c }}</td><td>{{ v.r }}</td><td>{{ v.v.slice(0, 120) }}</td><td>{{ v.u }}</td><td>{{ v.pe }}</td>
                <td><app-result [res]="v.res" [sev]="d.sev" /></td><td class="iss">{{ v.reason }}</td><td><app-chip [sc]="v.sc" [name]="v.scName" /></td><td class="n">{{ v.sp ?? '–' }}</td></tr>
            } @empty {<tr><td colspan="10">No values for this view.</td></tr>}</tbody></table></div>
        </div>
      }
    } @else {
      <div class="vis card">Unknown step {{ gate() }}.</div>
    }`
})
export class Steps {
  readonly r = inject(ReportService);
  readonly C = this.r.C;
  readonly gate = input<string>('');
  readonly dp = input<string>('');
  readonly mode = signal('all');
  readonly steps = computed(() => this.C.validationSteps(this.r.model, this.r.view()));
  readonly byFamily = computed(() => {
    const o: Record<string, any[]> = {};
    this.steps().steps.forEach((s) => (o[s.family] = o[s.family] || []).push(s));
    return o;
  });
  readonly famTitle = computed(() => {
    const f = this.steps().families.filter((x) => x.runs - x.nr).sort((a, b) => a.passPct - b.passPct)[0];
    return f ? `Pass rate by family: ${f.name} is lowest at ${f.passPct}%` : 'Pass rate by family';
  });
  readonly famChart = computed(() => G.bars(this.steps().families.map((f) => ({ label: f.name, value: f.passPct, color: f.passPct >= 95 ? '#009988' : f.passPct >= 80 ? '#0077BB' : '#CC3311' })), { max: 100, suffix: '%' }));
  readonly detail = computed(() => (this.gate() ? this.C.stepDetail(this.r.model, this.r.view(), this.gate()) : null));
  readonly fieldChart = computed(() => {
    const d = this.detail();
    return G.hbars((d?.fields || []).filter((f: any) => f.fail).slice(0, 12).map((f: any) => ({ label: f.d, value: f.fail, color: d.sev === 'Hard' ? '#CC3311' : '#EE7733', sub: f.failRate + '%' })));
  });
  readonly values = computed(() => (this.gate() && this.dp() ? this.C.stepFieldValues(this.r.model, this.r.view(), this.gate(), this.dp(), this.mode()) : []));
  readonly fieldCounts = computed(() => (this.detail()?.fields || []).find((f: any) => f.d === this.dp()) || { runs: 0, fail: 0, nr: 0 });
}
