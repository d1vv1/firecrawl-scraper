// Runs the built single-file report in a minimal DOM stub and checks KPIs, filters, pages,
// failures attention, ranges, import preview / apply / reset and trend.
//   node accuracy/tests/report_dom.test.js [path/to/allshares_report.html]
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const ROOT = path.join(__dirname, "..");
const HTML = process.argv[2] || path.join(ROOT, "..", "Dashboard", "allshares_report.html");
const html = fs.readFileSync(HTML, "utf8");

// ---- DOM stub -------------------------------------------------------------------------
function el(id, attrs) {
  const handlers = {};
  const classes = new Set((attrs.class || "").split(/\s+/).filter(Boolean));
  return {
    id, attrs, handlers, innerHTML: "", textContent: "", value: attrs.value || "", checked: false, disabled: "disabled" in attrs,
    style: {}, files: [], parentNode: null,
    classList: { toggle: (c, on) => (on === undefined ? (classes.has(c) ? classes.delete(c) : classes.add(c)) : on ? classes.add(c) : classes.delete(c)),
                 contains: (c) => classes.has(c), add: (c) => classes.add(c), remove: (c) => classes.delete(c) },
    hasClass: (c) => classes.has(c),
    addEventListener(t, fn) { (handlers[t] = handlers[t] || []).push(fn); },
    fire(t, ev) { (handlers[t] || []).forEach((fn) => fn.call(this, ev || { target: this })); },
    setAttribute(k, v) { attrs[k] = String(v); }, getAttribute(k) { return k in attrs ? attrs[k] : null; },
    insertAdjacentHTML(_, s) { this.innerHTML += s; }
  };
}
const byId = {}, tabs = [], pages = [];
const tagRe = /<(\w+)([^>]*)>/g;
let m;
while ((m = tagRe.exec(html.split("<script>\n/*")[0] + html.slice(html.indexOf("<body>"), html.lastIndexOf("<script>"))))) {
  const attrs = {};
  m[2].replace(/([\w-]+)(?:="([^"]*)")?/g, (_, k, v) => { attrs[k] = v === undefined ? "" : v; });
  const e = el(attrs.id || "", attrs);
  if (attrs.id && !byId[attrs.id]) byId[attrs.id] = e;
  if ((attrs.class || "").split(" ").includes("tab")) tabs.push(e);
  if ((attrs.class || "").split(" ").includes("page")) pages.push(byId[attrs.id] || e);
}
const document = {
  getElementById: (id) => byId[id] || (byId[id] = el(id, {})),
  querySelectorAll: (sel) => (sel === ".tab" ? tabs : sel === ".page" ? pages : []),
  querySelector: (sel) => (sel === ".page.on" ? pages.find((p) => p.hasClass("on")) : null)
};
const window = {};
const ctx = vm.createContext({ window, document, console, FileReader: function () {}, self: window, encodeURIComponent, JSON, Math, Object, Array, String, Number, RegExp, Date });
ctx.self = window;

const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((x) => x[1]);
scripts.forEach((s) => vm.runInContext(s.replace(/\bwindow\.(\w+)\s*=/g, "window.$1 = this.$1 ="), ctx));
const R = window.__REPORT;
assert.ok(R, "report API exposed");
const $ = (id) => document.getElementById(id);
const count = (s, re) => (s.match(re) || []).length;
let passed = 0;
function test(name, fn) { fn(); passed++; console.log("ok -", name); }

// ---- tests ------------------------------------------------------------------------------
const kcard = (k) => { const mm = $("kstrip").innerHTML.match(new RegExp('data-k="' + k + '"><div class="v">([^<]*)</div><div class="l">[^<]*</div><div class="d">([^<]*)</div>')); return mm ? { v: mm[1], d: mm[2] } : null; };

// The report holds whatever run was built last (python -m extractor.dashboard), so the
// expected numbers come from its own data.
const D = R.model.data, N = D.values.length, fmtN = (x) => x.toLocaleString("en-GB");
const empty = D.values.filter((v) => v.st === "not_found").length;
const foundPct = Math.round(D.values.filter((v) => v.st === "found").length / N * 100);
const hardGates = D.values.filter((v) => v.gr).reduce((a, v) => a + v.gr.filter((g) => g[1] === "F" && D.gates[D.gateIds[g[0]]][1] === "Hard").length, 0);
const countries = [...new Set(D.values.map((v) => v.c))];
const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

test("KPIs match the run", () => {
  assert.strictEqual(kcard("companies").v, String(D.meta.companies));
  assert.match(kcard("companies").d, new RegExp(D.meta.companies + " \\(" + D.meta.companyIds + " IDs\\) in this run"));
  assert.strictEqual(kcard("values").v, fmtN(N));
  assert.strictEqual(kcard("found").v, foundPct + "%");
  assert.strictEqual(kcard("checks").v, D.meta.checksPct + "%");
  assert.match(kcard("checks").d, /target 95%/);
  assert.match(kcard("checks").d, /pts vs (this|previous) run/);
  assert.strictEqual(kcard("hard").v, String(hardGates));
  assert.strictEqual(kcard("notfound").v, fmtN(empty));
});
test("overview title and footer", () => {
  assert.match($("ovTitle").textContent, new RegExp("^Only " + foundPct + "% of values are found; " + fmtN(empty) + " are empty$"));
  assert.match($("ftr").textContent, new RegExp(D.meta.companies + " companies from " + D.meta.companyIds + " IDs"));
  assert.match($("ftr").textContent, new RegExp("Source: " + esc(D.meta.tracker)));
});
test("country filter narrows every count", () => {
  const c = countries[0];
  R.setFilter("country", c);
  assert.strictEqual(kcard("values").v, fmtN(R.model.recs.filter((v) => v.c === c).length));
  assert.ok(Number(kcard("companies").v) <= D.meta.companies);
  R.setFilter("country", "");
  assert.strictEqual(kcard("values").v, fmtN(N));
});
test("data type and status filters", () => {
  R.setFilter("dtype", "pay");
  assert.strictEqual(kcard("values").v, fmtN(R.model.recs.filter((v) => v.p).length));
  R.setFilter("dtype", "all");
  R.setFilter("status", "H");
  assert.strictEqual(kcard("values").v, fmtN(R.model.recs.filter((v) => v.sc === "H").length));
  R.setFilter("status", "");
});
test("failures page: most attention callout names the hard check with most fails", () => {
  R.show("failures");
  const gs = window.ReportCore.gateStats(R.model, R.model.recs);
  if (gs.topHard) assert.match($("attn").textContent, new RegExp("^Most attention needed: " + gs.topHard.id));
  assert.match($("flTitle").textContent, new RegExp(fmtN(gs.fail) + " gate fails, " + gs.hard + " of them hard"));
});
test("fields page lists every field and drills into one", () => {
  R.show("fields");
  assert.strictEqual(count($("fdTable").innerHTML, /data-field=/g), new Set(D.values.map((v) => v.d)).size);
  const ex = D.values.filter((v) => v.d === "exchange");
  R.openField("exchange");
  assert.match($("fdDetail").innerHTML, new RegExp("exchange \\(C05, Listing and market\\): " + ex.length + " values, " +
    ex.filter((v) => v.st === "not_found").length + " empty"));
});
test("empty fields page", () => {
  R.show("empty");
  assert.match($("emTitle").textContent, new RegExp("^" + fmtN(empty) + " values are empty; "));
});
test("companies page and drill-down", () => {
  R.show("companies");
  assert.strictEqual(count($("coTable").innerHTML, /data-co=/g), D.meta.companies);
  const co = D.values.find((v) => v.d === "legal_name");
  R.openCompany(co.ck);
  assert.match($("coDetail").innerHTML, new RegExp("IDs " + co.id));
  assert.strictEqual($("coList").style.display, "none");
});
test("ranges page responds to options", () => {
  R.show("ranges");
  assert.strictEqual(count($("rgBody").innerHTML, /<tr>/g), window.ReportCore.ranges(R.model.recs, {}).rows.length);
  R.setRanges({ field: "base_salary", low: 10, high: 90, byCountry: true });
  assert.match($("rgHead").innerHTML, /10th percentile.*90th percentile/);
  assert.match($("rgHead").innerHTML, /<th>Country<\/th>/);
  assert.ok(!/fte/.test($("rgBody").innerHTML));
  R.setRanges(Object.assign({}, window.ReportCore.RANGE_DEFAULTS));
});
test("validation steps: steps, one step, one step on one field", () => {
  const C = window.ReportCore, s = C.validationSteps(R.model, R.model.recs);
  const body = () => $("stBody").innerHTML;
  R.openStep("", "");
  assert.strictEqual(count(body(), /class="group"/g), s.families.length);
  assert.strictEqual(count(body(), /tr class="click" tabindex="0" data-step=/g), s.steps.length);
  const top = s.steps.slice().sort((a, b) => b.fail - a.fail)[0];
  R.openStep(top.id, "");
  assert.match(body(), new RegExp(top.id + " .*: " + top.fail + " fails, 0 not run"));
  const field = C.stepDetail(R.model, R.model.recs, top.id).fields[0];
  R.openStep(top.id, field.d);
  assert.match(body(), new RegExp(top.id + " on " + field.d + ": " + field.fail + " of " + field.runs + " values fail"));
});
test("metric register", () => {
  R.show("metrics");
  assert.strictEqual(count($("mtBody").innerHTML, /<tr>/g), 10);
  assert.match($("mtBody").innerHTML, /Checks passing/);
});

// Import: one update, one unchanged, one added, one duplicate, two invalid.
const co = R.model.recs.find((v) => v.d === "legal_name" && v.ck !== v.id);
const lei = co.ck, coOriginal = co.v, histBase = R.model.histBase;
const head = "country,company,lei,size,grain,field_id,role_row,data_point,status,value,unit,currency,fiscal_year,source_type,source_name,url,location,language,minutes,notes";
const csv = [head,
  `${co.c},Any Name,${lei},large,company,C01,,legal_name,found,Illustrative example name,,,2025,api,GLEIF API,https://example.org,,,,`,
  `${co.c},${co.o},,large,company,C02,,lei,found,${lei},,,2025,api,GLEIF API,https://example.org,,,,`,
  "SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,,,2025,web,Website,https://example.org,,,,",
  "SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,,,2025,web,Website,https://example.org,,,,",
  `${co.c},${co.o},,large,company,C05,,,found,XCSE,,,2025,api,FIRDS,https://example.org,,,,`,
  "SE,Bad Row AB,,huge,company,C99,,,found,,,,2025,web,x,,,,,"].join("\n");

test("import preview counts", () => {
  R.show("import");
  const p = R.previewText(csv, "results_test.csv");
  assert.strictEqual(p.rows, 6);
  assert.strictEqual(p.good.length, 4, "C05 without data_point fails validation; bad row fails");
  const c = p.preview.counts;
  // The duplicate row matches the record its first copy added, so it also counts as unchanged.
  assert.deepStrictEqual([c.added, c.updated, c.same, c.dupes, c.ambiguous], [1, 1, 2, 1, 0]);
  assert.match($("errTable").innerHTML, /Required: field ID C05 covers more than one field/);
  assert.strictEqual($("impGo").disabled, false);
  assert.strictEqual(R.model.recs.length, N, "preview does not change data");
});
test("apply import, trend and source filter", () => {
  R.applyPending();
  assert.strictEqual(R.model.recs.length, N + 1);
  assert.strictEqual(kcard("imports").v, "1");
  const upd = R.model.recs.find((v) => v.d === "legal_name" && v.ck === lei);
  assert.strictEqual(upd.v, "Illustrative example name");
  assert.ok(!upd.gr && !upd.sc, "updated value is no longer gate-scored");
  R.show("trend");
  assert.match($("trTitle").textContent, /% at the baseline, [\d.]+% after 1 import$/);
  assert.strictEqual(count($("trBody").innerHTML, /<tr>/g), histBase + 1);
  R.setFilter("source", "I");
  assert.strictEqual(kcard("values").v, "2");
  R.setFilter("source", "all");
});
test("reset restores the run's values", () => {
  R.resetAll();
  assert.strictEqual(R.model.recs.length, N);
  assert.strictEqual(R.model.hist.length, histBase);
  assert.strictEqual(kcard("imports").v, "0");
  assert.strictEqual(R.model.recs.find((v) => v.d === "legal_name" && v.ck === lei).v, coOriginal);
});

console.log(`\n${passed} tests passed (${path.relative(process.cwd(), HTML)})`);
