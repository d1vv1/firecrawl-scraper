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
  it('KPIs match the tracker baseline', () => {
    const r = setup();
    expect(kpi(r, 'companies').v).toBe(49);
    expect(kpi(r, 'values').v).toBe('3,993');
    expect(kpi(r, 'checks').v).toBe('92.2%');
    expect(kpi(r, 'hard').v).toBe('438');
    expect(r.titles()['footer']).toContain('49 companies from 50 IDs');
  });

  it('filters narrow the view', () => {
    const r = setup();
    r.setFilter('country', 'FI');
    expect(r.view().every((v) => v.c === 'FI')).toBe(true);
    r.setFilter('status', 'H');
    expect(r.view().every((v) => v.sc === 'H')).toBe(true);
    r.clearFilters();
    expect(r.view().length).toBe(3993);
  });

  it('overview states the finding and the duplicate company', () => {
    setup();
    const el = render(Overview);
    expect(el.querySelector('.title')!.textContent).toBe('Only 49% of values are found; 1,409 are empty');
    expect(el.textContent).toContain('T0668 and T0671 share one LEI');
  });

  it('failures page names the hard check that needs most attention', () => {
    setup();
    const el = render(Failures);
    expect(el.querySelector('.attn')!.textContent).toMatch(/^Most attention needed: CORE-02 .* with 208 hard fails/);
  });

  it('fields page lists 55 fields and opens a field', () => {
    setup();
    const el = render(Fields, { dp: 'exchange' });
    expect(el.querySelectorAll('tbody tr.click').length).toBeGreaterThanOrEqual(55);
    expect(el.textContent).toContain('exchange (C05, Listing and market): 50 values, 0 empty');
  });

  it('company drill-down shows the duplicate IDs', () => {
    setup();
    const el = render(Companies, { key: '549300HX9MRFY47AH564' });
    expect(el.textContent).toContain('IDs T0668, T0671');
    expect(el.textContent).toContain('Same company under IDs T0668 and T0671');
  });

  it('ranges page computes 67 provisional rows and responds to options', () => {
    setup();
    const f = TestBed.createComponent(Ranges);
    f.detectChanges();
    expect(f.nativeElement.querySelector('.title').textContent).toMatch(/^67 range rows from 1,011 values/);
    f.componentInstance.set('field', 'base_salary');
    f.componentInstance.set('low', 10);
    f.detectChanges();
    expect(f.nativeElement.textContent).toContain('10th percentile');
    expect(f.componentInstance.result().rows.every((x: any) => x.d === 'base_salary')).toBe(true);
  });

  it('validation steps drill from steps to a step to one field', () => {
    setup();
    let el = render(Steps);
    expect(el.querySelector('.title')!.textContent).toMatch(/^17 of 33 validation steps have no fails/);
    expect(el.querySelectorAll('tr.group').length).toBe(6);
    el = render(Steps, { gate: 'NUM-09' });
    expect(el.querySelector('.title')!.textContent).toContain('NUM-09 Valuation basis stated (grant, face, realised): 92 fails');
    el = render(Steps, { gate: 'NUM-09', dp: 'lti_granted' });
    expect(el.querySelector('.title')!.textContent).toBe('NUM-09 on lti_granted: 49 of 49 values fail, 0 not run');
    expect([...el.querySelectorAll('.breadcrumb-item')].map((x) => x.textContent!.trim())).toEqual(['Validation steps', 'NUM-09', 'lti_granted']);
    expect(el.querySelector('table')!.classList).toContain('table');
  });

  it('import preview, apply and reset; trend follows', () => {
    const r = setup();
    const lei = r.model.recs.find((v) => v.id === 'T0002' && v.d === 'legal_name')!.ck;
    const csv = 'country,company,lei,size,grain,field_id,role_row,data_point,status,value,unit\n' +
      `DK,Any Name,${lei},large,company,C01,,legal_name,found,Illustrative example name,\n` +
      'SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,\n' +
      'DK,Sydbank AS,,large,company,C05,,,found,XCSE,\n';
    const f = TestBed.createComponent(Import);
    f.detectChanges();
    f.componentInstance.preview(csv, 'results_test.csv');
    f.detectChanges();
    const p = f.componentInstance.pending();
    expect([p.preview.counts.added, p.preview.counts.updated]).toEqual([1, 1]);
    expect(f.nativeElement.textContent).toContain('Required: field ID C05 covers more than one field');
    f.componentInstance.apply();
    expect(r.model.recs.length).toBe(3994);
    expect(kpi(r, 'imports').v).toBe(1);
    const t = render(Trend);
    expect(t.querySelector('.title')!.textContent).toMatch(/after 1 import$/);
    f.componentInstance.reset();
    expect(r.model.recs.length).toBe(3993);
    expect(r.model.hist.length).toBe(1);
  });
});
