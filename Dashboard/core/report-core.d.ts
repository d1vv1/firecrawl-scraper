// Types for report-core.js (shared dashboard logic). Shapes follow SPEC.md section 5.
export interface Value {
  s: 'T' | 'I'; c: string; o: string; ck: string; id: string; g: string; r: string; p: 0 | 1;
  k: string; m: string; f: string; d: string; v: string; u: string; st: string;
  pe?: string; me?: string; so?: string; ep?: string; nt?: string; sc?: string; sp?: number; gr?: [number, string, number][];
}
export interface ReportData {
  meta: { tracker: string; asOf: string; built: string; rows: number; filled: number; dataPoints: number;
          companyIds: number; companies: number; duplicates: { lei: string; ids: string[] }[];
          thresholds: { pass: number; review: number }; target: number;
          countries?: string[]; checksPct?: number; foundPct?: number };
  gates: Record<string, [string, string]>; gateIds: string[]; reasons: string[]; values: Value[];
  baseline: { checksPct: number; foundPct: number; label: string };
}
export interface HistPoint { label: string; checks: number; found: number; fileFound?: number; n: number | null; groups: Record<string, number> | null }
export interface Model { data: ReportData; recs: Value[]; hist: HistPoint[]; histBase: number; impCount: number; fidToDp: Record<string, string[]>; dpMeta: Record<string, any> }
export interface Filters { country: string; source: string; dtype: string; cat: string; company: string; status: string }
export interface Kpi { key: string; v: string | number; l: string; cls: string; d: string }

export const PAL: string[];
export const VSTAT: [string, string, string][];
export const SSTAT: [string, string, string][];
export const SNAME: Record<string, string>;
export const COUNTRIES: string[];
export const GROUPS: string[];
export const RANGE_FIELDS: string[];
export const EMPTY_FILTERS: Filters;
export const RANGE_DEFAULTS: any;
export function pct(a: number, b: number): number;
export function pct1(a: number, b: number): number;
export function fmt(n: any): string;
export function num(s: any): number | null;
export function companyKey(v: Value): string;
export function createModel(data: ReportData): Model;
export function resetModel(model: Model): void;
export function filterValues(recs: Value[], f: Filters): Value[];
export function filterOptions(model: Model): { countries: string[]; categories: string[]; companies: { key: string; label: string }[]; statuses: { key: string; label: string }[] };
export function anyFilter(f: Filters): boolean;
export function statusCounts(vs: Value[]): Record<string, number>;
export function scoreCounts(vs: Value[]): any;
export function companiesOf(vs: Value[]): number;
export function countriesOf(vs: Value[]): string[];
export function gates(model: Model, v: Value): any[];
export function overview(vs: Value[]): any;
export function payComp(vs: Value[]): any;
export function countriesPage(vs: Value[]): any;
export function gateStats(model: Model, vs: Value[]): any;
export function fieldTable(model: Model, vs: Value[]): any[];
export function fieldDetail(model: Model, vs: Value[], dp: string): any;
export function emptyTables(model: Model, vs: Value[]): any;
export function companyTable(model: Model, vs: Value[]): any[];
export function companyDetail(model: Model, vs: Value[], key: string, mode: string): any;
export const FAMILIES: [string, string][];
export function validationSteps(model: Model, vs: Value[]): { steps: any[]; families: any[]; title: string };
export function stepDetail(model: Model, vs: Value[], gate: string): any;
export function stepFieldValues(model: Model, vs: Value[], gate: string, dp: string, mode?: string): any[];
export function percentile(sorted: number[], p: number): number | null;
export function ranges(vs: Value[], opts: any): any;
export function rangeOptions(vs: Value[]): { fields: string[]; units: string[]; methods: string[] };
export function kpis(model: Model, vs: Value[]): Kpi[];
export function metrics(model: Model, vs: Value[]): any[];
export function titles(model: Model, vs: Value[], extra?: any): Record<string, string>;
export function attention(model: Model, vs: Value[]): { text: string; gate: string | null };
export function parseCSV(text: string): string[][];
export function leiValid(s: string): boolean;
export function validate(schema: any, text: string): any;
export function applyImport(model: Model, recs: Value[], rows: any[]): any;
export function previewImport(model: Model, schema: any, text: string, fileName?: string): any;
export function commitImport(model: Model, pending: any): any;
export function toCSV(header: string[], rows: any[][], bom?: boolean): string;
export function rangesCSV(res: any): string;
export function metricsCSV(ms: any[]): string;
