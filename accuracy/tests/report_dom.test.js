// Runs the built single-file report in a minimal DOM stub and checks KPIs, filters, pages,
// failures attention, ranges, import preview / apply / reset and trend.
//   node accuracy/tests/report_dom.test.js [path/to/allshares_report.html]
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const ROOT = path.join(__dirname, "..");
const HTML = process.argv[2] || path.join(ROOT, "out", "allshares_report.html");
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

test("KPIs at tracker baseline", () => {
  assert.strictEqual(kcard("companies").v, "49");
  assert.match(kcard("companies").d, /49 \(50 IDs\)/);
  assert.strictEqual(kcard("values").v, "3,993");
  assert.strictEqual(kcard("found").v, "49%");
  assert.strictEqual(kcard("checks").v, "92.2%");
  assert.match(kcard("checks").d, /target 95%/);
  assert.match(kcard("checks").d, /\+0\.0 pts vs tracker/);
  assert.strictEqual(kcard("hard").v, "438");
  assert.strictEqual(kcard("notfound").v, "1,409");
});
test("overview title and duplicate note", () => {
  assert.match($("ovTitle").textContent, /^Only 49% of values are found; 1,409 are empty$/);
  assert.match($("dupNote").textContent, /T0668 and T0671 share one LEI/);
  assert.match($("ftr").textContent, /49 companies from 50 IDs/);
});
test("country filter narrows every count", () => {
  R.setFilter("country", "FI");
  const fiValues = R.model.recs.filter((v) => v.c === "FI").length;
  assert.strictEqual(kcard("values").v, fiValues.toLocaleString("en-GB"));
  assert.ok(Number(kcard("companies").v) < 49);
  R.setFilter("country", "");
  assert.strictEqual(kcard("values").v, "3,993");
});
test("data type and status filters", () => {
  R.setFilter("dtype", "pay");
  const pay = R.model.recs.filter((v) => v.p).length;
  assert.strictEqual(kcard("values").v, pay.toLocaleString("en-GB"));
  R.setFilter("dtype", "all");
  R.setFilter("status", "H");
  assert.strictEqual(kcard("values").v, "404");
  R.setFilter("status", "");
});
test("failures page: most attention callout names the hard check with most fails", () => {
  R.show("failures");
  assert.match($("attn").textContent, /^Most attention needed: CORE-02 \(Snippet re-parses to same value\) with 208 hard fails/);
  assert.match($("flTitle").textContent, /1,287 gate fails, 438 of them hard/);
  assert.ok(count($("chChecks").innerHTML, /<rect/g) === 12);
  R.setFilter("country", "DK");
  assert.doesNotMatch($("attn").textContent, /with 208 hard fails/);
  R.setFilter("country", "");
});
test("fields page lists 55 fields and drills into one", () => {
  R.show("fields");
  assert.strictEqual(count($("fdTable").innerHTML, /data-field=/g), 55);
  R.openField("exchange");
  assert.match($("fdDetail").innerHTML, /exchange \(C05, Listing and market\): 50 values, 0 empty/);
  assert.match($("fdDetail").innerHTML, /COD-01<\/b> hard fail: stored as exchange name/);
});
test("empty fields page", () => {
  R.show("empty");
  assert.match($("emTitle").textContent, /^1,409 values are empty; /);
  assert.ok(count($("emFields").innerHTML, /<tr>/g) > 10);
});
test("companies page: 49 companies and drill-down with duplicate note", () => {
  R.show("companies");
  assert.strictEqual(count($("coTable").innerHTML, /data-co=/g), 49);
  R.openCompany("549300HX9MRFY47AH564");
  assert.match($("coDetail").innerHTML, /IDs T0668, T0671/);
  assert.match($("coDetail").innerHTML, /Same company under IDs T0668 and T0671/);
  assert.strictEqual($("coList").style.display, "none");
});
test("ranges page matches the Python ranges workbook at default options", () => {
  R.show("ranges");
  const py = JSON.parse(fs.readFileSync(path.join(ROOT, "out", "ranges_default.json"), "utf8"));
  const js = window.ReportCore.ranges(R.model.recs, {});
  assert.strictEqual(js.rows.length, py.length);
  js.rows.forEach((r, i) => {
    const p = py[i];
    assert.deepStrictEqual([r.d, r.unit, r.n, r.companies], [p[0], p[1], p[2], p[3]]);
    [r.min, r.low, r.median, r.high, r.max].forEach((x, j) => assert.ok(Math.abs(x - p[4 + j]) <= 1e-6 * Math.max(1, Math.abs(x)), r.d + " " + r.unit));
  });
  assert.strictEqual(count($("rgBody").innerHTML, /<tr>/g), py.length);
  R.setRanges({ field: "base_salary", low: 10, high: 90, byCountry: true });
  assert.match($("rgHead").innerHTML, /10th percentile.*90th percentile/);
  assert.match($("rgHead").innerHTML, /<th>Country<\/th>/);
  assert.ok(!/fte/.test($("rgBody").innerHTML));
  R.setRanges(Object.assign({}, window.ReportCore.RANGE_DEFAULTS));
});
test("validation steps: steps, one step, one step on one field", () => {
  R.openStep("", "");
  const body = () => $("stBody").innerHTML;
  assert.match(body(), /17 of 33 validation steps have no fails; CORE-04 \(As-of or period date present\) fails most: 621/);
  assert.strictEqual(count(body(), /class="group"/g), 6);
  assert.strictEqual(count(body(), /tr class="click" tabindex="0" data-step=/g), 33);
  R.openStep("NUM-09", "");
  assert.match(body(), /NUM-09 Valuation basis stated \(grant, face, realised\): 92 fails, 0 not run, across 4 fields/);
  assert.match(body(), /data-stepfield="lti_granted"/);
  R.openStep("NUM-09", "lti_granted");
  assert.match(body(), /NUM-09 on lti_granted: 49 of 49 values fail, 0 not run/);
  assert.strictEqual(count(body(), /data-co=/g), 49);
  R.setStepMode("P");
  assert.match(body(), /No values for this view/);
  R.setFilter("country", "SE");
  R.openStep("NUM-09", "lti_granted");
  assert.ok(count(body(), /data-co=/g) < 49);
  R.setFilter("country", "");
});
test("metric register", () => {
  R.show("metrics");
  assert.strictEqual(count($("mtBody").innerHTML, /<tr>/g), 10);
  assert.match($("mtBody").innerHTML, /Checks passing/);
});

// Import: one update, one unchanged, one added, one duplicate, one ambiguous, one invalid.
const syd = R.model.recs.find((v) => v.d === "legal_name" && v.id === "T0002");
const lei = syd.ck, sydOriginal = syd.v;
const head = "country,company,lei,size,grain,field_id,role_row,data_point,status,value,unit,currency,fiscal_year,source_type,source_name,url,location,language,minutes,notes";
const csv = [head,
  `DK,Any Name,${lei},large,company,C01,,legal_name,found,Illustrative example name,,,2025,api,GLEIF API,https://example.org,,,,`,
  `DK,${syd.o},,large,company,C02,,lei,found,${lei},,,2025,api,GLEIF API,https://example.org,,,,`,
  "SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,,,2025,web,Website,https://example.org,,,,",
  "SE,Illustrative Example AB,,small_mid,company,C09,,website,found,example.org,,,2025,web,Website,https://example.org,,,,",
  `DK,${syd.o},,large,company,C05,,,found,XCSE,,,2025,api,FIRDS,https://example.org,,,,`,
  "SE,Bad Row AB,,huge,company,C99,,,found,,,,2025,web,x,,,,,"].join("\n");

test("import preview counts", () => {
  R.show("import");
  const p = R.previewText(csv, "results_test.csv");
  assert.strictEqual(p.rows, 6);
  assert.strictEqual(p.good.length, 4, "C05 without data_point fails validation; bad row fails");
  const c = p.preview.counts;
  // The duplicate row matches the record its first copy added, so it also counts as unchanged.
  assert.deepStrictEqual([c.added, c.updated, c.same, c.dupes, c.ambiguous], [1, 1, 2, 1, 0]);
  assert.match($("impReport").innerHTML, /<b>1<\/b> added, <b>1<\/b> updated, <b>2<\/b> unchanged, <b>1<\/b> duplicate/);
  assert.match($("errTable").innerHTML, /Required: field ID C05 covers more than one field/);
  assert.strictEqual($("impGo").disabled, false);
  assert.strictEqual(R.model.recs.length, 3993, "preview does not change data");
});
test("ambiguous match without data_point is rejected at upsert", () => {
  const C = window.ReportCore, M = R.model;
  const res = C.applyImport(M, M.recs.map((v) => Object.assign({}, v)), [{ line: 2, c: "DK", o: syd.o, lei: "", g: "company", p: 0, k: "x", m: "x", f: "C01", r: "", d: "", v: "x", u: "", st: "found" }]);
  assert.strictEqual(res.counts.ambiguous, 1);
  assert.match(res.errs[0].msg, /Add data_point/);
});
test("apply import, trend and source filter", () => {
  R.applyPending();
  assert.strictEqual(R.model.recs.length, 3994);
  assert.strictEqual(R.model.impCount, 1);
  assert.strictEqual(kcard("imports").v, "1");
  const upd = R.model.recs.find((v) => v.d === "legal_name" && v.id === "T0002");
  assert.strictEqual(upd.v, "Illustrative example name");
  assert.strictEqual(upd.s, "I");
  assert.ok(!upd.gr && !upd.sc, "updated value is no longer gate-scored");
  R.show("trend");
  assert.match($("trTitle").textContent, /92.2% at the tracker, \d+% after 1 import$/);
  assert.strictEqual(count($("trBody").innerHTML, /<tr>/g), 2);
  R.setFilter("source", "I");
  assert.strictEqual(kcard("values").v, "2");
  R.setFilter("source", "all");
});
test("reset restores tracker values", () => {
  R.resetAll();
  assert.strictEqual(R.model.recs.length, 3993);
  assert.strictEqual(R.model.hist.length, 1);
  assert.strictEqual(kcard("imports").v, "0");
  assert.strictEqual(R.model.recs.find((v) => v.d === "legal_name" && v.id === "T0002").v, sydOriginal);
});

console.log(`\n${passed} tests passed (${path.relative(process.cwd(), HTML)})`);
