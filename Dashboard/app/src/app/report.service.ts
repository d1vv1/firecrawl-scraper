import { Injectable, computed, signal } from '@angular/core';
import * as Core from '../../../core/report-core.js';
import type { Filters, Model, ReportData, Value } from '../../../core/report-core.js';

/** Holds the report model and filters. All logic comes from the shared core (SPEC.md section 2). */
@Injectable({ providedIn: 'root' })
export class ReportService {
  readonly C = Core;
  readonly loaded = signal(false);
  readonly error = signal('');
  readonly filters = signal<Filters>({ ...Core.EMPTY_FILTERS });
  /** Bumped whenever model.recs or model.hist change in place (import, reset). */
  readonly version = signal(0);
  model!: Model;
  schema: any = null;

  readonly view = computed<Value[]>(() => {
    this.version();
    return this.loaded() ? Core.filterValues(this.model.recs, this.filters()) : [];
  });
  readonly kpis = computed(() => (this.loaded() ? Core.kpis(this.model, this.view()) : []));
  readonly titles = computed(() => (this.loaded() ? Core.titles(this.model, this.view()) : ({} as Record<string, string>)));
  readonly options = computed(() => {
    this.version();
    return this.loaded() ? Core.filterOptions(this.model) : null;
  });

  async load(base = '') {
    try {
      const [data, schema] = await Promise.all([
        fetch(base + 'report.json').then((r) => r.json()),
        fetch(base + 'allshares_import_schema.json').then((r) => r.json())
      ]);
      this.init(data, schema);
    } catch (e: any) {
      this.error.set('Could not load report.json. Run python -m extractor.dashboard <run>_datapoints.csv first. ' + (e?.message || ''));
    }
  }

  init(data: ReportData, schema: any) {
    this.model = Core.createModel(data);
    this.schema = schema;
    this.loaded.set(true);
    this.version.update((v) => v + 1);
  }

  setFilter<K extends keyof Filters>(key: K, value: Filters[K]) {
    this.filters.update((f) => ({ ...f, [key]: value }));
  }
  clearFilters() {
    this.filters.set({ ...Core.EMPTY_FILTERS });
  }
  touch() {
    this.version.update((v) => v + 1);
  }
}
