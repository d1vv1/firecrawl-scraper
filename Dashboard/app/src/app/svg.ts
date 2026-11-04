import { Component, input } from '@angular/core';

/** Legend row for a chart. */
@Component({
  selector: 'app-legend',
  template: `<div class="legend">@for (i of items(); track i.label) {<span><i [style.background]="i.color"></i>{{ i.label }}</span>}</div>`
})
export class Legend {
  readonly items = input<{ label: string; color: string }[]>([]);
}

/** Score status chip. */
@Component({
  selector: 'app-chip',
  template: `<span class="chip badge rounded-pill" [class]="'chip badge rounded-pill ' + (sc() || (name() === 'Empty' ? 'E' : 'X'))">{{ name() }}</span>`
})
export class Chip {
  readonly sc = input<string>('');
  readonly name = input<string>('');
}
