import { Routes } from '@angular/router';
import { Companies, Empty, Fields } from './pages/drill';
import { Countries, Failures, Metrics, Overview, PayComp, Trend } from './pages/summary';
import { Steps } from './pages/steps';
import { Import, Ranges } from './pages/tools';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'overview' },
  { path: 'overview', component: Overview, title: 'Overview · Allshares accuracy' },
  { path: 'paycomp', component: PayComp, title: 'Pay vs company · Allshares accuracy' },
  { path: 'countries', component: Countries, title: 'Countries · Allshares accuracy' },
  { path: 'fields', component: Fields, title: 'Fields · Allshares accuracy' },
  { path: 'fields/:dp', component: Fields, title: 'Field detail · Allshares accuracy' },
  { path: 'empty', component: Empty, title: 'Empty fields · Allshares accuracy' },
  { path: 'companies', component: Companies, title: 'Companies · Allshares accuracy' },
  { path: 'companies/:key', component: Companies, title: 'Company detail · Allshares accuracy' },
  { path: 'failures', component: Failures, title: 'Failures · Allshares accuracy' },
  { path: 'steps', component: Steps, title: 'Validation steps · Allshares accuracy' },
  { path: 'steps/:gate', component: Steps, title: 'Validation step · Allshares accuracy' },
  { path: 'steps/:gate/:dp', component: Steps, title: 'Validation step by field · Allshares accuracy' },
  { path: 'ranges', component: Ranges, title: 'Ranges · Allshares accuracy' },
  { path: 'trend', component: Trend, title: 'Trend · Allshares accuracy' },
  { path: 'metrics', component: Metrics, title: 'Metric register · Allshares accuracy' },
  { path: 'import', component: Import, title: 'Import data · Allshares accuracy' },
  { path: '**', redirectTo: 'overview' }
];
