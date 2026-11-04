import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ReportService } from './report.service';

export const PAGES = [
  { path: 'overview', label: 'Overview' },
  { path: 'paycomp', label: 'Pay vs company' },
  { path: 'countries', label: 'Countries' },
  { path: 'fields', label: 'Fields' },
  { path: 'empty', label: 'Empty fields' },
  { path: 'companies', label: 'Companies' },
  { path: 'failures', label: 'Failures' },
  { path: 'steps', label: 'Validation steps' },
  { path: 'ranges', label: 'Ranges' },
  { path: 'trend', label: 'Trend' },
  { path: 'metrics', label: 'Metric register' },
  { path: 'import', label: 'Import data' }
];

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html'
})
export class App {
  readonly r = inject(ReportService);
  readonly pages = PAGES;

  constructor() {
    this.r.load();
  }
  imported() {
    this.r.version();
    return this.r.loaded() ? this.r.model.recs.filter((v) => v.s === 'I').length : 0;
  }
  on(key: 'country' | 'source' | 'dtype' | 'cat' | 'company' | 'status', ev: Event) {
    this.r.setFilter(key, (ev.target as HTMLSelectElement).value);
  }
}
