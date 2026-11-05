import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import data from '../../public/report.json';
import schema from '../../public/allshares_import_schema.json';
import { routes } from './app.routes';
import { Companies, Fields } from './pages/drill';
import { Failures, Overview, Trend } from './pages/summary';
import { Steps } from './pages/steps';
import { Import, Ranges } from './pages/tools';
import { ReportService } from './report.service';

// report.json is whatever run was built last (python -m extractor.dashboard), so the expected
// numbers come from the data itself.
const D = data as any;
const N: number = D.values.length;
const fmtN = (x: number) => x.toLocaleString('en-GB');
const empty = D.values.filter((v: any) => v.st === 'not_found').length;
const foundPct = Math.round((D.values.filter((v: any) => v.st === 'found').length / N) * 100);

function setup() {
  TestBed.configureTestingModule({ providers: [provideRouter(routes)] });
  const r = TestBed.inject(ReportService);
  r.init(structuredClone(data) as any, schema);
  return r;
}
function render<T>(cmp: new (...a: any[]) => T, inputs: Record<string, any> = {}) {
  const f = TestBed.createComponent(cmp);
  Object.entries(inputs).forEach(([k, v]) => f.componentRef.setInput(k, v));
  f.detectChanges();
  return f.nativeElement as HTMLElement;
}
const kpi = (r: ReportService, key: string) => r.kpis().find((k) => k.key === key)!;

describe('Allshares dashboard (Angular)', () => {
  it('KPIs match the run', () => {
    const r = setup();
    expect(kpi(r, 'companies').v).toBe(D.meta.companies);
    expect(kpi(r, 'values').v).toBe(fmtN(N));
    expect(kpi(r, 'checks').v).toBe(D.meta.checksPct + '%');
    expect(r.titles()['footer']).toContain(`${D.meta.companies} companies from ${D.meta.companyIds} IDs`);
  });

  it('filters narrow the view', () => {
    const r = setup();
    const c = D.values[0].c;
    r.setFilter('country', c);
    expect(r.view().every((v) => v.c === c)).toBe(true);
    r.setFilter('status', 'H');
    expect(r.view().every((v) => v.sc === 'H')).toBe(true);
    r.clearFilters();
    expect(r.view().length).toBe(N);
  });

  it('overview states the finding', () => {
    setup();
    const el = render(Overview);
    expect(el.querySelector('.title')!.textContent).toBe(`Only ${foundPct}% of values are found; ${fmtN(empty)} are empty`);
  });

  it('failures page names the hard check that needs most attention', () => {
    const r = setup();
    const top = (r.C as any).gateStats(r.model, r.model.recs).topHard;
    const el = render(Failures);
    if (top) expect(el.querySelector('.attn')!.textContent).toMatch(new RegExp('^Most attention needed: ' + top.id));
  });

  it('fields page lists every field and opens a field', () => {
    setup();
    const ex = D.values.filter((v: any) => v.d === 'exchange');
    const el = render(Fields, { dp: 'exchange' });
    expect(el.querySelectorAll('tbody tr.click').length).toBeGreaterThanOrEqual(new Set(D.values.map((v: any) => v.d)).size);
    expect(el.textContent).toContain(`exchange (C05, Listing and market): ${ex.length} values`);
  });

  it('company drill-down shows the company IDs', () => {
    setup();
    const co = D.values.find((v: any) => v.d === 'legal_name');
    const el = render(Companies, { key: co.ck });
    expect(el.textContent).toContain('IDs ' + co.id);
  });

  it('ranges page responds to options', () => {
    setup();
    const f = TestBed.createComponent(Ranges);
    f.detectChanges();
    expect(f.nativeElement.querySelector('.title').textContent).toMatch(/^\d+ range rows from [\d,]+ values/);
    f.componentInstance.set('field', 'base_salary');
    f.componentInstance.set('low', 10);
    f.detectChanges();
    expect(f.nativeElement.textContent).toContain('10th percentile');
    expect(f.componentInstance.result().rows.every((x: any) => x.d === 'base_salary')).toBe(true);
  });

  it('validation steps drill from steps to a step to one field', () => {
    const r = setup();
    const s = r.C.validationSteps(r.model, r.model.recs);
    let el = render(Steps);
    expect(el.querySelectorAll('tr.group').length).toBe(s.families.length);
    const top = s.steps.slice().sort((a: any, b: any) => b.fail - a.fail)[0];
    el = render(Steps, { gate: top.id });
    expect(el.querySelector('.title')!.textContent).toContain(`${top.id} ${top.name}: ${top.fail} fails`);
    const field = r.C.stepDetail(r.model, r.model.recs, top.id).fields[0];
    el = render(Steps, { gate: top.id, dp: field.d });
    expect(el.querySelector('.title')!.textContent).toBe(`${top.id} on ${field.d}: ${field.fail} of ${field.runs} values fail, 0 not run`);
    expect([...el.querySelectorAll('.breadcrumb-item')].map((x) => x.textContent!.trim())).toEqual(['Validation steps', top.id, field.d]);
  });

  it('import preview, apply and reset; trend follows', () => {
    const r = setup();
    // the import schema spells the UK "UK", the data "GB": use a company elsewhere
    const co = r.model.recs.find((v) => v.d === 'legal_name' && v.ck !== v.id && v.c !== 'GB')!;
    const base = r.model.hist.length;
    const csv = 'country,company,lei,size,grain,field_id,role_row,data_point,status,value,unit\n' +
      `${co.c},Any Name,${co.ck},large,company,C01,,legal_name,found,Illustrative example name,\n` +
      'SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,\n' +
      `${co.c},${co.o},,large,company,C05,,,found,XCSE,\n`;
    const f = TestBed.createComponent(Import);
    f.detectChanges();
    f.componentInstance.preview(csv, 'results_test.csv');
    f.detectChanges();
    const p = f.componentInstance.pending();
    expect([p.preview.counts.added, p.preview.counts.updated]).toEqual([1, 1]);
    expect(f.nativeElement.textContent).toContain('Required: field ID C05 covers more than one field');
    f.componentInstance.apply();
    expect(r.model.recs.length).toBe(N + 1);
    expect(kpi(r, 'imports').v).toBe(1);
    const t = render(Trend);
    expect(t.querySelector('.title')!.textContent).toMatch(/after 1 import$/);
    f.componentInstance.reset();
    expect(r.model.recs.length).toBe(N);
    expect(r.model.hist.length).toBe(base);
  });
});
