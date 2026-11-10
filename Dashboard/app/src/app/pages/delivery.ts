import { Component, computed, inject, signal } from '@angular/core';
import { Chart } from '../chart';
import * as G from '../chart';
import { download } from '../download';
import { ReportService } from '../report.service';

// Delivery pages (SPEC 6.4): the FY2025 gap-fill stand-up view. All numbers come from Core.delivery.

function pctColor(p: number | null, good: number) {
  return p == null ? '#888888' : p >= good ? '#009988' : p >= good - 20 ? '#EE7733' : '#CC3311';
}

/** Shared by the five pages: the delivery model for the current Country filter. */
function useDelivery() {
  const r = inject(ReportService);
  return { r, C: r.C, x: computed(() => { r.version(); return r.C.delivery(r.model, r.filters().country); }) };
}

const ERR = `@if (!x().ok) {<div class="attn alert alert-danger" role="alert">{{ x().error }}</div>}`;

// ------------------------------------------------------------------ Stand-up
@Component({
  selector: 'app-standup',
  imports: [Chart],
  template: `${ERR}
    @if (x().ok) {
      @let d = x();
      @let k = d.kpis;
      <div class="title">{{ d.titles.standup }}</div>
      <div class="sub">FY{{ d.fy }} gap-fill. Delivery data built {{ d.built }}; deadline {{ d.deadline }}; exceptions sign-off {{ d.acceptance }}. {{ d.country ? 'Country filter: ' + d.country + ' (other filters do not apply to these pages).' : 'Only the Country filter applies to these pages.' }}</div>
      <div class="kmini">
        <div><b>{{ C.fmt(k.remaining) }} <small>of {{ C.fmt(d.plan.baseline_remaining) }}</small></b><span>{{ k.behind > 0 ? 'Remaining: ' + C.fmt(k.behind) + ' behind plan' : 'Remaining: on or ahead of plan' }}</span></div>
        <div><b>{{ C.fmt(k.done) }}</b><span>Done (of {{ C.fmt(k.companies) }} required)</span></div>
        <div><b>{{ C.fmt(k.extracted) }}</b><span>Extracted so far</span></div>
        <div><b>{{ C.fmt(k.workLeft) }}</b><span>Working days left{{ k.needed == null ? '' : ' · need ' + C.fmt(k.needed) + '/day (plan ' + d.plan.daily_target + ')' }}</span></div>
        <div><b>{{ k.passPct == null ? '–' : k.passPct + '%' }}</b><span>Rules pass rate ({{ C.fmt(k.passN) }} of {{ C.fmt(k.valuesN) }} values; line {{ line() }}%)</span></div>
        <div><b>{{ C.fmt(k.discOpen) }}</b><span>Discovery open (of {{ C.fmt(k.discN) }})</span></div>
        <div><b>{{ C.fmt(k.exc) }}</b><span>Exceptions ({{ C.fmt(k.excYes) }} accepted)</span></div>
      </div>
      <div class="vis card"><h3>Status funnel by regional batch</h3>
        <div class="hint">Companies that reached each stage, in order, with the share of the batch's required companies. The outlined cell in each column is the biggest drop: where that batch is stuck.</div>
        <div class="tbl"><table class="table table-sm table-hover">
          <thead><tr><th>Stage</th>@for (f of d.funnel; track f.name) {<th class="n">{{ f.name }}</th>}</tr></thead>
          <tbody>
            @for (s of d.stages; track s; let i = $index) {
              <tr><td>{{ s }}</td>@for (f of d.funnel; track f.name) {
                <td class="n" [class.stuck]="i === f.stuck" [attr.title]="i === f.stuck ? 'Stuck here: ' + C.fmt(f.drop) + ' companies waiting' : null"><span class="pctbar"><i [style.width.%]="f.pcts[i]" style="background:#0077BB"></i></span>{{ C.fmt(f.counts[i]) }} <span class="hint">{{ f.pcts[i] }}%</span></td>}</tr>
            }
            <tr><td class="hint">Stuck at</td>@for (f of d.funnel; track f.name) {<td class="n hint">{{ f.stuck > 0 && f.counts[0] ? d.stages[f.stuck] : '–' }}</td>}</tr>
          </tbody></table></div></div>
      <div class="grid">
        <div class="vis card"><h3>{{ passTitle() }}</h3><app-chart [options]="passChart()" [height]="hh(passItems().length)" />
          <div class="legend"><span><i style="background:#0077BB"></i>Automated rules</span><span><i style="background:#EE7733"></i>Spot-check sample</span></div></div>
        <div class="vis card"><h3>Pass rate by batch against the {{ line() }}% line</h3>
          <div class="hint">Automated rules = values with status Pass of the values scored. Spot-check = sampled values judged correct. Rules low but sample fine points to the rules; both low points to extraction.</div>
          <div class="tbl"><table class="table table-sm table-hover">
            <thead><tr><th>Batch</th><th class="n">Values scored</th><th class="n">Rules pass %</th><th class="n">Review</th><th class="n">Fail</th><th class="n">Sampled</th><th class="n">Spot-check pass %</th><th>Reading</th></tr></thead>
            <tbody>@for (b of d.passByBatch; track b.b) {
              <tr><td>{{ b.b }}</td><td class="n">{{ C.fmt(b.n) }}</td>
                <td class="n">@if (b.rules != null) {<span class="pctbar"><i [style.width.%]="b.rules" [style.background]="color(b.rules)"></i></span>{{ b.rules }}%} @else {–}</td>
                <td class="n">{{ C.fmt(b.review) }}</td><td class="n">{{ C.fmt(b.fail) }}</td><td class="n">{{ C.fmt(b.spotN) }}</td>
                <td class="n">@if (b.spot != null) {<span class="pctbar"><i [style.width.%]="b.spot" [style.background]="color(b.spot)"></i></span>{{ b.spot }}%} @else {–}</td>
                <td>@switch (reading(b)) {
                  @case ('none') {<span class="hint">not extracted yet</span>}
                  @case ('rulesOkNoSample') {<span class="yes">Rules at the line</span> · no sample yet}
                  @case ('rulesLowNoSample') {<span class="no">Rules below the line</span> · no sample yet}
                  @case ('both') {<span class="yes">Both at the line</span>}
                  @case ('rules') {<span class="no">Rules problem</span> (sample fine)}
                  @case ('extraction') {<span class="no">Extraction problem</span> (both low)}
                  @default {<span class="no">Rules miss errors</span> the sample finds}
                }</td></tr>
            }</tbody></table></div></div>
      </div>
      <div class="grid">
        <div class="vis card"><h3>{{ d.failures.length ? 'Top failure: ' + d.failures[0].cat + ' (' + C.fmt(d.failures[0].companies) + ' companies)' : 'Failure patterns' }}</h3>
          <app-chart [options]="failChart()" [height]="hh(d.failures.length)" /></div>
        <div class="vis card">
          <div class="bar">
            <div class="opt" style="flex:1 1 220px"><label class="form-label">Work list: reason</label>
              <select class="form-select form-select-sm" (change)="cat.set($any($event.target).value)">
                <option value="">All reasons</option>
                @for (f of d.failures; track f.cat) {<option [value]="f.cat" [selected]="cat() === f.cat">{{ f.cat }} ({{ f.companies }})</option>}
              </select></div>
            <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export CSV</button>
          </div>
          <div class="tbl tall"><table class="table table-sm table-hover">
            <thead><tr><th>Company</th><th>Country</th><th>Batch</th><th>Reason</th><th class="n">Count</th><th>Example</th></tr></thead>
            <tbody>@for (f of failList().slice(0, 500); track f.id + f.cat) {
              <tr><td>{{ f.o }}</td><td>{{ f.c }}</td><td>{{ f.b }}</td><td>{{ f.cat }}</td><td class="n">{{ C.fmt(f.n) }}</td><td class="iss">{{ f.ex }}</td></tr>
            } @empty {<tr><td colspan="6">No failures for this selection.</td></tr>}</tbody></table></div></div>
      </div>
    }`
})
export class Standup {
  private readonly u = useDelivery();
  readonly C = this.u.C;
  readonly x = this.u.x;
  readonly cat = signal('');
  readonly hh = G.hHeight;
  readonly line = computed(() => (this.x().ok ? Math.round(this.x().plan.pass_line * 100) : 95));
  readonly passItems = computed(() => {
    const d = this.x(), items: G.Item[] = [];
    if (!d.ok) return items;
    d.passByBatch.forEach((b: any) => {
      if (b.rules != null) items.push({ label: b.b + ' · rules', value: b.rules, color: '#0077BB', sub: b.rules >= this.line() ? 'at the line' : 'below' });
      if (b.spot != null) items.push({ label: b.b + ' · spot-check', value: b.spot, color: '#EE7733', sub: b.spot >= this.line() ? 'at the line' : 'below' });
    });
    return items;
  });
  readonly passChart = computed(() => G.hbars(this.passItems(), { max: 100, suffix: '%' }));
  readonly passTitle = computed(() => {
    const d = this.x();
    if (!d.ok || !this.passItems().length) return 'Validation pass rate by batch';
    const ran = d.passByBatch.filter((b: any) => b.rules != null);
    return `${ran.filter((b: any) => b.rules < this.line()).length} of ${ran.length} extracted batches are below the ${this.line()}% line on the automated rules`;
  });
  readonly failChart = computed(() => (this.x().ok ? G.hbars(this.x().failures.map((f: any) => ({ label: f.cat, value: f.companies,
    color: /Wrong|Missing/.test(f.cat) ? '#CC3311' : '#0077BB', sub: this.C.fmt(f.values) + ' values' }))) : null));
  readonly failList = computed(() => (this.x().ok ? this.x().failRows.filter((f: any) => !this.cat() || f.cat === this.cat()) : []));
  color(p: number | null) { return pctColor(p, this.line()); }
  reading(b: any) {
    const line = this.line();
    if (b.rules == null) return 'none';
    if (b.spot == null) return b.rules >= line ? 'rulesOkNoSample' : 'rulesLowNoSample';
    return b.rules >= line && b.spot >= line ? 'both' : b.rules < line && b.spot >= line ? 'rules' : b.rules < line ? 'extraction' : 'sample';
  }
  exportCsv() { download(this.C.deliveryFailCSV(this.failList()), 'allshares_failure_patterns.csv'); }
}

// ------------------------------------------------------------------ Throughput
@Component({
  selector: 'app-throughput',
  imports: [Chart],
  template: `${ERR}
    @if (x().ok) {
      @let d = x();
      @let k = d.kpis;
      <div class="title">{{ d.titles.throughput }}</div>
      <div class="sub">{{ C.fmt(d.plan.baseline_remaining) }} companies on {{ d.baselineDate }}, due {{ d.deadline }} at {{ d.plan.daily_target }} a working day. {{ d.burn.text }} The burn-down covers every batch; the Country filter does not apply to it.</div>
      <div class="kmini">
        <div><b>{{ C.fmt(k.remaining) }}</b><span>Remaining today</span></div>
        <div><b>{{ C.fmt(k.planNow) }}</b><span>Plan for today</span></div>
        <div><b>{{ (k.behind > 0 ? '+' : '') + C.fmt(k.behind) }}</b><span>{{ k.behind > 0 ? 'Behind plan' : 'Against plan (0 or less = on track)' }}</span></div>
        <div><b>{{ C.fmt(k.workLeft) }}</b><span>Working days left</span></div>
        <div><b>{{ k.needed == null ? '–' : C.fmt(k.needed) }}</b><span>Needed per working day</span></div>
        <div><b>{{ d.burn.proj ? d.burn.projShort : '–' }}</b><span>Projected finish</span></div>
      </div>
      <div class="vis card"><h3>Remaining companies against plan</h3><app-chart [options]="chart()" [height]="260" /></div>
      <div class="vis card"><h3>Batches against plan</h3>
        <div class="hint">Expected by today = the batch's companies spread evenly over its working days. Behind = done below 90% of expected, so slippage shows from day two.</div>
        <div class="tbl"><table class="table table-sm table-hover">
          <thead><tr><th>Batch</th><th>Window</th><th class="n">Day</th><th class="n">To do</th><th class="n">Needs per day</th><th class="n">Expected by today</th><th class="n">Done</th><th>Status</th></tr></thead>
          <tbody>@for (b of d.batchPlan; track b.b) {
            <tr><td>{{ b.b }}</td><td>{{ b.window }}</td><td class="n">{{ b.day ? b.day + ' of ' + b.len : '–' }}</td><td class="n">{{ C.fmt(b.todo) }}</td><td class="n">{{ C.fmt(b.perDay) }}</td>
              <td class="n">{{ b.expected == null ? '–' : C.fmt(b.expected) }}</td><td class="n">{{ C.fmt(b.done) }}</td>
              <td>@if (b.cls) {<span [class]="b.cls === 'good' ? 'yes' : 'no'">{{ b.status }}</span>} @else {<span class="hint">{{ b.status }}</span>}</td></tr>
          }</tbody></table></div></div>
    }`
})
export class Throughput {
  private readonly u = useDelivery();
  readonly C = this.u.C;
  readonly x = this.u.x;
  readonly chart = computed(() => (this.x().ok ? G.burn(this.x().burn.days, this.x().plan.deadline) : null));
}

// ------------------------------------------------------------------ Discovery queue
@Component({
  selector: 'app-discovery',
  imports: [Chart],
  template: `${ERR}
    @if (x().ok) {
      @let dq = x().discovery;
      <div class="title">{{ x().titles.discovery }}</div>
      <div class="sub">Companies whose document or data source is still to find (tracker Find Required). Owner, status and next step come from accuracy/inputs/delivery/discovery.csv; the next step defaults from the need.</div>
      <div class="kmini">
        <div><b>{{ C.fmt(dq.rows.length) }}</b><span>In the queue</span></div>
        @for (c of dq.counts; track c.key) {<div><b>{{ C.fmt(c.n) }}</b><span>{{ c.label }}</span></div>}
        <div><b>{{ dq.rows.length ? C.pct(dq.resolved, dq.rows.length) + '%' : '–' }}</b><span>Resolved (found or not available)</span></div>
      </div>
      <div class="grid">
        <div class="vis card"><h3>Queue by status</h3><app-chart [options]="chart()" /></div>
        <div class="vis card"><h3>Queue by need</h3><div class="tbl"><table class="table table-sm table-hover">
          <thead><tr><th>Need</th><th class="n">Companies</th></tr></thead>
          <tbody>@for (n of dq.byNeed; track n.need) {<tr><td>{{ n.need }}</td><td class="n">{{ C.fmt(n.n) }}</td></tr>}</tbody></table></div></div>
      </div>
      <div class="vis card">
        <div class="bar">
          <div class="opt" style="flex:1 1 220px"><label class="form-label">Search</label><input class="form-control form-control-sm" type="search" placeholder="Company, owner or country" [value]="q()" (input)="q.set($any($event.target).value)"></div>
          <div class="opt"><label class="form-label">Status</label><select class="form-select form-select-sm" (change)="st.set($any($event.target).value)">
            <option value="">All statuses</option>@for (s of C.DISC_STATES; track s[0]) {<option [value]="s[0]">{{ s[1] }}</option>}</select></div>
          <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export CSV</button>
        </div>
        <div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Company</th><th>Country</th><th>Batch</th><th>Need</th><th>Next step</th><th>Owner</th><th>Status</th><th>Updated</th></tr></thead>
          <tbody>@for (r of list(); track r.id) {
            <tr><td>{{ r.o }}</td><td>{{ r.c }}</td><td>{{ r.b }}</td><td>{{ r.need }}</td><td>{{ r.next }}</td><td>@if (r.owner) {{{ r.owner }}} @else {<span class="hint">Unassigned</span>}</td>
              <td><span class="chip" style="background:#f3f2f1" [style.border-left]="'4px solid ' + state(r.status)[2]">{{ state(r.status)[1] }}</span></td><td>{{ r.updated }}</td></tr>
          } @empty {<tr><td colspan="8">No companies match.</td></tr>}</tbody></table></div>
      </div>
    }`
})
export class Discovery {
  private readonly u = useDelivery();
  readonly C = this.u.C;
  readonly x = this.u.x;
  readonly q = signal('');
  readonly st = signal('');
  readonly chart = computed(() => (this.x().ok ? G.bars(this.x().discovery.counts.map((c: any) => ({ label: c.label, value: c.n, color: c.color }))) : null));
  readonly list = computed(() => {
    if (!this.x().ok) return [];
    const q = this.q().trim().toLowerCase(), st = this.st();
    return this.x().discovery.rows.filter((r: any) => (!st || this.C.discState(r.status) === st) && (!q || (r.o + ' ' + r.owner + ' ' + r.c + ' ' + r.b).toLowerCase().includes(q)));
  });
  state(s: string) { return this.C.DISC_STATES.find((d) => d[0] === this.C.discState(s)) || ['', s, '#888888']; }
  exportCsv() { download(this.C.discoveryCSV(this.list()), 'allshares_discovery_queue.csv'); }
}

// ------------------------------------------------------------------ Exceptions
@Component({
  selector: 'app-exceptions',
  template: `${ERR}
    @if (x().ok) {
      @let ex = x().exceptions;
      <div class="title">{{ x().titles.exceptions }}</div>
      <div class="sub">Each company with no FY{{ x().fy }} report, a document still missing, or a wrong document, with the reason. This is the list Allshares formally accepts on {{ x().acceptance }}. Record acceptance in accuracy/inputs/delivery/exceptions.csv. {{ x().country ? 'Country filter: ' + x().country + '.' : '' }}</div>
      <div class="kmini">
        <div><b>{{ C.fmt(ex.rows.length) }}</b><span>Exceptions</span></div>
        @for (c of ex.byCat; track c.cat) {<div><b>{{ C.fmt(c.n) }} <small>{{ C.fmt(c.yes) }} accepted</small></b><span>{{ c.cat }}</span></div>}
      </div>
      <div class="vis card">
        <div class="bar">
          <div class="opt" style="flex:1 1 220px"><label class="form-label">Search</label><input class="form-control form-control-sm" type="search" placeholder="Company or reason" [value]="q()" (input)="q.set($any($event.target).value)"></div>
          <div class="opt"><label class="form-label">Category</label><select class="form-select form-select-sm" (change)="cat.set($any($event.target).value)">
            <option value="">All categories</option>@for (c of ex.byCat; track c.cat) {<option [value]="c.cat">{{ c.cat }}</option>}</select></div>
          <button class="btn btn-outline-primary btn-sm" (click)="exportCsv()">Export for Allshares</button>
        </div>
        <div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Company</th><th>Country</th><th>Batch</th><th>Category</th><th>Reason</th><th>Source</th><th>Allshares</th></tr></thead>
          <tbody>@for (e of list(); track e.id + e.cat) {
            <tr><td>{{ e.o }}</td><td>{{ e.c }}</td><td>{{ e.b }}</td><td>{{ e.cat }}</td><td class="iss">{{ e.reason }}@if (e.note) { <i>({{ e.note }})</i>}</td><td class="hint">{{ e.source }}</td>
              <td>@switch (e.accepted) { @case ('yes') {<span class="yes">Accepted</span>} @case ('no') {<span class="no">Rejected</span>} @default {<span class="hint">Pending</span>} }</td></tr>
          } @empty {<tr><td colspan="7">No exceptions match.</td></tr>}</tbody></table></div>
      </div>
    }`
})
export class Exceptions {
  private readonly u = useDelivery();
  readonly C = this.u.C;
  readonly x = this.u.x;
  readonly q = signal('');
  readonly cat = signal('');
  readonly list = computed(() => {
    if (!this.x().ok) return [];
    const q = this.q().trim().toLowerCase(), cat = this.cat();
    return this.x().exceptions.rows.filter((e: any) => (!cat || e.cat === cat) && (!q || (e.o + ' ' + e.reason + ' ' + e.c + ' ' + e.b).toLowerCase().includes(q)));
  });
  exportCsv() { download(this.C.exceptionsCSV(this.list()), 'allshares_FY2025_exceptions.csv'); }
}

// ------------------------------------------------------------------ Pipeline health
@Component({
  selector: 'app-health',
  imports: [Chart],
  template: `${ERR}
    @if (x().ok) {
      @let h = x().health;
      <div class="title">{{ x().titles.health }}</div>
      <div class="sub">Scheduled runs, failed runs and Firecrawl credit use, so a broken run or a credit shortfall does not quietly stop a batch. Runs and credits come from the per-company run outputs; scheduled runs from accuracy/inputs/delivery/scheduled_runs.csv.</div>
      <div class="kmini">
        <div><b>{{ C.fmt(h.runs) }}</b><span>Company runs{{ h.span ? ' (' + h.span + ')' : '' }}</span></div>
        <div><b>{{ C.fmt(h.failed) }} <small>{{ h.failedPct == null ? '–' : h.failedPct + '%' }}</small></b><span>Failed runs</span></div>
        <div><b>{{ C.fmt(h.scheduled.length) }}</b><span>{{ h.scheduled.length ? C.fmt(h.missed) + ' scheduled runs missed' : 'Scheduled runs (none recorded)' }}</span></div>
        <div><b>{{ C.fmt(h.used) }}</b><span>Firecrawl credits used</span></div>
        <div><b>{{ C.fmt(h.perRun) }}</b><span>Credits per company run</span></div>
        <div><b>{{ C.fmt(h.need) }}</b><span>Credits needed for the remaining {{ C.fmt(x().kpis.remaining) }}</span></div>
        <div><b>{{ h.balance == null ? '–' : C.fmt(h.balance) }}</b><span>{{ h.balance == null ? 'Credit balance (set it in accuracy/inputs/delivery.json)' : h.short ? 'Credit balance: short by ' + C.fmt(h.need - h.balance) : 'Credit balance: covers what is needed' }}</span></div>
      </div>
      <div class="grid">
        <div class="vis card"><h3>Company runs per day</h3><app-chart [options]="runChart()" />
          <div class="legend"><span><i style="background:#0077BB"></i>Completed</span><span><i style="background:#CC3311"></i>Failed</span></div></div>
        <div class="vis card"><h3>Firecrawl credits per day</h3><app-chart [options]="creditChart()" /></div>
      </div>
      <div class="grid">
        <div class="vis card"><h3>Scheduled runs</h3><div class="tbl"><table class="table table-sm table-hover">
          <thead><tr><th>Run</th><th>Batch</th><th>Scheduled</th><th>Started</th><th>Status</th><th class="n">Companies</th><th class="n">Credits</th></tr></thead>
          <tbody>@for (s of h.scheduled; track $index) {
            <tr><td>{{ s.run }}</td><td>{{ s.b }}</td><td>{{ s.at }}</td><td>{{ s.started }}</td><td>@if (s.bad) {<span class="no">{{ s.status }}</span>} @else {{{ s.status }}}</td><td class="n">{{ s.companies }}</td><td class="n">{{ s.credits }}</td></tr>
          } @empty {<tr><td colspan="7">No scheduled runs recorded. Add one row per planned run to accuracy/inputs/delivery/scheduled_runs.csv; a run past its time with no start is flagged as missed.</td></tr>}</tbody></table></div></div>
        <div class="vis card"><h3>Failed runs</h3><div class="tbl tall"><table class="table table-sm table-hover">
          <thead><tr><th>Company</th><th>Date</th><th>Error</th></tr></thead>
          <tbody>@for (f of h.failedRuns; track $index) {<tr><td>{{ f.name }}</td><td>{{ f.date }}</td><td class="iss">{{ f.error }}</td></tr>}
          @empty {<tr><td colspan="3">No failed runs.</td></tr>}</tbody></table></div></div>
      </div>
    }`
})
export class Health {
  private readonly u = useDelivery();
  readonly C = this.u.C;
  readonly x = this.u.x;
  readonly runChart = computed(() => {
    if (!this.x().ok) return null;
    const days = this.x().health.days;
    return G.stacked(days.map((d: any) => d.short), [{ name: 'Completed', color: '#0077BB', values: days.map((d: any) => d.ok) },
      { name: 'Failed', color: '#CC3311', values: days.map((d: any) => d.failed) }]);
  });
  readonly creditChart = computed(() => (this.x().ok ? G.bars(this.x().health.days.map((d: any) => ({ label: d.short, value: Math.round(d.credits), color: '#009988' }))) : null));
}
