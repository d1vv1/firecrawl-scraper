import { AfterViewInit, Component, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';
import * as UI from '../../../core/report-ui.js';
import { ReportService } from './report.service';

export const PAGES = [
  { path: 'overview', label: 'Overview' },
  { path: 'sources', label: 'Reports & sources' },
  { path: 'codata', label: 'Company data' },
  { path: 'paydata', label: 'Pay data' },
  { path: 'paycomp', label: 'Pay vs company' },
  { path: 'notfound', label: 'Not found' },
  { path: 'countries', label: 'Countries' },
  { path: 'fields', label: 'Fields' },
  { path: 'coverage', label: 'Field coverage' },
  { path: 'empty', label: 'Empty fields' },
  { path: 'companies', label: 'Companies' },
  { path: 'failures', label: 'Failures' },
  { path: 'steps', label: 'Validation steps' },
  { path: 'ranges', label: 'Ranges' },
  { path: 'trend', label: 'Trend' },
  { path: 'metrics', label: 'Metric register' },
  { path: 'standup', label: 'Stand-up' },
  { path: 'throughput', label: 'Throughput' },
  { path: 'discovery', label: 'Discovery queue' },
  { path: 'exceptions', label: 'Exceptions' },
  { path: 'health', label: 'Pipeline health' },
  { path: 'export', label: 'Export for Claude' },
  { path: 'import', label: 'Import data' }
];

/** The top bar: Overview on its own, the other pages in menus (SPEC 6.1). */
const GROUPS: [string, string[]][] = [
  ['Overview', ['overview']],
  ['Coverage', ['codata', 'paydata', 'coverage', 'fields', 'empty', 'notfound']],
  ['Companies', ['companies', 'sources', 'countries', 'paycomp']],
  ['Checks', ['failures', 'steps', 'ranges', 'trend', 'metrics']],
  ['Delivery', ['standup', 'throughput', 'discovery', 'exceptions', 'health']],
  ['Data', ['export', 'import']]
];
export const NAV = GROUPS.map(([label, paths]) => ({ label, pages: paths.map((p) => PAGES.find((x) => x.path === p)!) }));

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html'
})
export class App implements AfterViewInit {
  readonly r = inject(ReportService);
  readonly router = inject(Router);
  readonly pages = PAGES;
  readonly nav = NAV;
  /** The current route, to mark the group of the open page and name that page on its button. */
  readonly url = signal('');

  constructor() {
    this.r.load();
    this.router.events.pipe(filter((e) => e instanceof NavigationEnd)).subscribe(() => this.url.set(this.router.url));
  }
  current(g: (typeof NAV)[number]) {
    const u = this.url();
    return g.pages.find((p) => u === '/' + p.path || u.startsWith('/' + p.path + '/')) || null;
  }
  /** Every table sorts on a header click; the notes bar sits on the right edge (core/report-ui.js). */
  ngAfterViewInit() {
    UI.sortable(document.body);
    const nav = document.querySelector('.navgroups');
    if (nav) UI.navMenus(nav);
    UI.mountNotes({
      context: () => {
        const p = PAGES.find((x) => this.router.url.startsWith('/' + x.path));
        return (p ? p.label : this.router.url) + (this.r.loaded() ? ' · filters: ' + this.r.C.filterText(this.r.filters(), this.r.model) : '');
      },
      onChange: (t) => this.r.notes.set(t)
    });
  }
  imported() {
    this.r.version();
    return this.r.loaded() ? this.r.model.recs.filter((v) => v.s === 'I').length : 0;
  }
  on(key: 'country' | 'source' | 'dtype' | 'cat' | 'company' | 'status' | 'fill', ev: Event) {
    this.r.setFilter(key, (ev.target as HTMLSelectElement).value);
  }
}
