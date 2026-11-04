import { Component, ElementRef, OnDestroy, afterNextRender, effect, input } from '@angular/core';
import * as echarts from 'echarts/core';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import { GridComponent, LegendComponent, MarkLineComponent, TooltipComponent } from 'echarts/components';
import { SVGRenderer } from 'echarts/renderers';
import type { EChartsCoreOption } from 'echarts/core';

echarts.use([BarChart, LineChart, PieChart, GridComponent, LegendComponent, TooltipComponent, MarkLineComponent, SVGRenderer]);

/** ECharts host, SVG renderer (DESIGN.md section 5: SVG charts, fixed height). */
@Component({
  selector: 'app-chart',
  template: `<div class="echart" [style.height.px]="height()" role="img" [attr.aria-label]="label()"></div>`
})
export class Chart implements OnDestroy {
  readonly options = input<EChartsCoreOption | null>(null);
  readonly height = input(230);
  readonly label = input('chart');
  private chart: echarts.ECharts | null = null;
  private ro: ResizeObserver | null = null;

  constructor(private readonly host: ElementRef<HTMLElement>) {
    afterNextRender(() => {
      const el = this.host.nativeElement.querySelector('.echart') as HTMLElement;
      this.chart = echarts.init(el, null, { renderer: 'svg' });
      if (this.options()) this.chart.setOption(this.options()!, true);
      if (typeof ResizeObserver !== 'undefined') {
        this.ro = new ResizeObserver(() => this.chart?.resize());
        this.ro.observe(el);
      }
    });
    effect(() => {
      const o = this.options(), h = this.height();
      if (this.chart && o) {
        this.chart.setOption(o, true);
        this.chart.resize({ height: h });
      }
    });
  }
  ngOnDestroy() {
    this.ro?.disconnect();
    this.chart?.dispose();
  }
}

// ---------------------------------------------------------------- option builders
export interface Item { label: string; value: number; color?: string; sub?: string }
const INK = '#252423', SOFT = '#605e5c', GRID = '#e1dfdd', FAINT = '#8a8886';
const FONT = { fontFamily: '"Segoe UI", system-ui, Arial, sans-serif' };
const nf = (n: number) => Number(n).toLocaleString('en-GB', { maximumFractionDigits: 1 });
const base = { textStyle: FONT, animation: false, tooltip: { trigger: 'item' as const, confine: true } };
const axisCommon = { axisLine: { lineStyle: { color: GRID } }, axisTick: { show: false }, axisLabel: { color: SOFT, fontSize: 11 }, splitLine: { lineStyle: { color: GRID } } };
const empty = { ...base, title: { text: 'No data for this selection', left: 'center', top: 'middle', textStyle: { color: FAINT, fontSize: 12, fontWeight: 'normal' as const } } };

/** Rows needed by a horizontal chart, for the host height (22px per row, DESIGN.md). */
export const hHeight = (n: number) => Math.max(80, n * 26 + 20);

export function bars(items: Item[], o: { max?: number; suffix?: string } = {}): EChartsCoreOption {
  if (!items.length) return empty;
  const suf = o.suffix || '';
  return {
    ...base, grid: { left: 44, right: 10, top: 20, bottom: 28 },
    xAxis: { type: 'category', data: items.map((i) => i.label), ...axisCommon, splitLine: { show: false } },
    yAxis: { type: 'value', max: o.max, ...axisCommon, axisLabel: { color: FAINT, fontSize: 10, formatter: (v: number) => nf(v) + suf } },
    series: [{ type: 'bar', barWidth: '60%', data: items.map((i) => ({ value: i.value, name: i.label, itemStyle: { color: i.color || '#0077BB' } })),
      label: { show: true, position: 'top', color: INK, fontSize: 10, formatter: (p: any) => nf(p.value) + suf },
      tooltip: { valueFormatter: (v: any) => nf(v) + suf } }]
  };
}

export function hbars(items: Item[], o: { max?: number; suffix?: string } = {}): EChartsCoreOption {
  if (!items.length) return empty;
  const suf = o.suffix || '';
  const rows = items.slice().reverse();
  return {
    ...base, grid: { left: 150, right: 84, top: 6, bottom: 6 },
    xAxis: { type: 'value', max: o.max, show: false },
    yAxis: { type: 'category', data: rows.map((i) => i.label), ...axisCommon,
      axisLabel: { color: INK, fontSize: 11, width: 142, overflow: 'truncate' } },
    series: [{ type: 'bar', barMaxWidth: 16, data: rows.map((i) => ({ value: i.value, name: i.label, itemStyle: { color: i.color || '#0077BB' }, sub: i.sub })),
      label: { show: true, position: 'right', color: SOFT, fontSize: 11, formatter: (p: any) => nf(p.value) + suf + (p.data.sub ? ' (' + p.data.sub + ')' : '') },
      tooltip: { valueFormatter: (v: any) => nf(v) + suf } }]
  };
}

export function stacked(cats: string[], series: { name: string; color: string; values: number[] }[]): EChartsCoreOption {
  if (!cats.length) return empty;
  return {
    ...base, tooltip: { trigger: 'axis', confine: true }, grid: { left: 48, right: 10, top: 16, bottom: 28 },
    xAxis: { type: 'category', data: cats, ...axisCommon, splitLine: { show: false } },
    yAxis: { type: 'value', ...axisCommon, axisLabel: { color: FAINT, fontSize: 10, formatter: (v: number) => nf(v) } },
    series: series.map((s) => ({ type: 'bar', name: s.name, stack: 'all', barWidth: '60%', data: s.values, itemStyle: { color: s.color } }))
  };
}

/** Horizontal 100% stacked bars; each row is one item, segments are its share by series. */
export function stackedH(rows: Record<string, any>[], series: { key: string; name: string; color: string }[]): EChartsCoreOption {
  if (!rows.length) return empty;
  const r = rows.slice().reverse();
  const tot = r.map((x) => series.reduce((a, s) => a + (x[s.key] || 0), 0));
  return {
    ...base, tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, confine: true,
      formatter: (ps: any[]) => ps[0].name + '<br>' + ps.map((p) => `${p.marker}${p.seriesName}: ${nf(p.data.n)} (${Math.round(p.value)}%)`).join('<br>') },
    grid: { left: 150, right: 16, top: 6, bottom: 6 },
    xAxis: { type: 'value', max: 100, show: false },
    yAxis: { type: 'category', data: r.map((x) => x['label']), ...axisCommon, axisLabel: { color: INK, fontSize: 11, width: 142, overflow: 'truncate' } },
    series: series.map((s) => ({ type: 'bar', name: s.name, stack: 'all', barMaxWidth: 16, itemStyle: { color: s.color },
      data: r.map((x, i) => ({ value: tot[i] ? ((x[s.key] || 0) / tot[i]) * 100 : 0, n: x[s.key] || 0 })) }))
  };
}

export function pie(items: Item[]): EChartsCoreOption {
  const shown = items.filter((i) => i.value);
  if (!shown.length) return empty;
  return {
    ...base,
    legend: { orient: 'vertical', right: 8, top: 'middle', textStyle: { color: INK, fontSize: 11 },
      formatter: (name: string) => { const t = shown.reduce((a, i) => a + i.value, 0), it = shown.find((i) => i.label === name)!; return `${name} ${Math.round((it.value / t) * 100)}%`; } },
    series: [{ type: 'pie', radius: '82%', center: ['32%', '50%'], label: { show: false },
      data: shown.map((i) => ({ name: i.label, value: i.value, itemStyle: { color: i.color } })),
      tooltip: { formatter: (p: any) => `${p.marker}${p.name}: ${nf(p.value)} (${Math.round(p.percent)}%)` } }]
  };
}

export function line(points: { label: string; short: string; checks: number; found: number }[], target?: number): EChartsCoreOption {
  const mk = (key: 'checks' | 'found', name: string, color: string, withTarget: boolean) => ({
    type: 'line', name, data: points.map((p) => p[key]), symbolSize: 7, lineStyle: { width: 2.4, color }, itemStyle: { color },
    markLine: withTarget && target != null ? { symbol: 'none', silent: true, lineStyle: { color: '#888888', type: 'dashed' },
      label: { formatter: 'target ' + target + '%', color: '#888888', fontSize: 10 }, data: [{ yAxis: target }] } : undefined
  });
  return {
    ...base, tooltip: { trigger: 'axis', confine: true, valueFormatter: (v: any) => v + '%' },
    grid: { left: 44, right: 60, top: 14, bottom: 28 },
    xAxis: { type: 'category', data: points.map((p) => p.short), boundaryGap: points.length < 2, ...axisCommon, splitLine: { show: false } },
    yAxis: { type: 'value', min: 0, max: 100, ...axisCommon, axisLabel: { color: FAINT, fontSize: 10, formatter: '{value}%' } },
    series: [mk('checks', 'Checks passing %', '#0077BB', true), mk('found', 'Found %', '#009988', false)]
  };
}
