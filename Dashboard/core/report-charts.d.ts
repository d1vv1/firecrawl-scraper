// Types for report-charts.js (shared SVG chart builders). Each returns an SVG string.
export interface Item { label: string; value: number; color?: string; sub?: string }
export function esc(s: any): string;
export function bars(items: Item[], o?: { max?: number; suffix?: string }): string;
export function hbars(items: Item[], o?: { max?: number; suffix?: string }): string;
export function stacked(cats: string[], series: { name: string; color: string; values: number[] }[]): string;
export function stackedH(rows: Record<string, any>[], series: { key: string; name: string; color: string }[]): string;
export function pie(items: Item[]): string;
export function line(points: { label: string; short: string; checks: number; found: number }[], target?: number): string;
export function legend(items: { label: string; color: string }[]): string;
