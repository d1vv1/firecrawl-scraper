// Types for report-ui.js (sortable tables and the notes bar).
export function sortable(root: Element): void;
export function navMenus(root: Element): void;
export function cellValue(td: Element | null): number | string | null;
export function getNotes(): string;
export function setNotes(text: string): boolean;
export function mountNotes(opts?: { context?: () => string; onChange?: (text: string) => void }): { open: (on: boolean) => void; get: () => string } | null;
export function copyText(text: string): Promise<boolean>;
export function saveFile(text: string, name: string): void;
export function esc(s: any): string;
