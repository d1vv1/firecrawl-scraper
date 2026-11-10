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
const applicable = D.values.filter((v) => v.st !== "not_applicable").length;   // found % is over these
const foundPct = Math.round(D.values.filter((v) => v.st === "found").length / applicable * 100);
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
  assert.strictEqual(kcard("hard").v, fmtN(hardGates));
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
  assert.match($("flTitle").textContent, new RegExp(fmtN(gs.fail) + " gate fails, " + fmtN(gs.hard) + " of them hard"));
});
test("fields page lists every field and drills into one", () => {
  R.show("fields");
  assert.strictEqual(count($("fdTable").innerHTML, /data-field=/g), new Set(D.values.map((v) => v.d)).size);
  const ex = D.values.filter((v) => v.d === "exchange");
  R.openField("exchange");
  assert.match($("fdDetail").innerHTML, new RegExp("exchange \\(C05, Listing and market\\): " + ex.filter((v) => v.st !== "not_found" && v.st !== "not_applicable").length + " values, " +
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
  assert.match(body(), new RegExp(top.id + " .*: " + fmtN(top.fail) + " fails, 0 not run"));
  const field = C.stepDetail(R.model, R.model.recs, top.id).fields[0];
  R.openStep(top.id, field.d);
  assert.match(body(), new RegExp(top.id + " on " + field.d + ": " + fmtN(field.fail) + " of " + fmtN(field.runs) + " values fail"));
});
test("values filter: filled and empty", () => {
  R.setFilter("fill", "filled");
  assert.strictEqual(kcard("values").v, fmtN(D.values.filter((v) => v.st === "found" || v.st === "partial").length));
  R.setFilter("fill", "empty");
  assert.strictEqual(kcard("values").v, fmtN(empty));
  R.setFilter("fill", "");
});
test("reports and sources page: one row per company, report found or not", () => {
  const s = window.ReportCore.sources(R.model, R.model.recs);
  R.show("sources");
  assert.strictEqual(count($("srTable").innerHTML, /data-co=/g), D.meta.companies);
  assert.match($("srTitle").textContent, new RegExp("^Annual report found for " + s.totals.annual + " of " + D.meta.companies + " companies"));
  assert.strictEqual(count($("srTable").innerHTML, /class="yes">Found/g), s.totals.annual + s.totals.rem);
  const withRem = s.rows.find((x) => x.hasRem);
  if (withRem) assert.ok($("srTable").innerHTML.includes(withRem.links.rem[0].url.replace(/&/g, "&amp;")), "remuneration report link shown");
});
test("company data and pay data pages: field review next to the run", () => {
  const C = window.ReportCore;
  for (const [p, px, sheet] of [["codata", "cd", "Company Data"], ["paydata", "pd", "Pay Data"]]) {
    R.show(p);
    const d = C.dataPage(R.model, R.model.recs, sheet);
    assert.strictEqual($(px + "Title").textContent, d.title);
    assert.strictEqual(count($(px + "Table").innerHTML, /data-field=/g), (D.fieldList || []).filter((f) => f.sheet === sheet).length);
    if ((D.fieldList || []).some((f) => f.why)) assert.match($(px + "Table").innerHTML, /class="chip H">High</);
  }
  assert.match($("pdHead").innerHTML, /1 Dec milestone/);
  assert.ok(!/1 Dec milestone/.test($("cdHead").innerHTML));
});
test("not-found page: matrix and drill-down", () => {
  R.show("notfound");
  const m = window.ReportCore.notFoundMatrix(R.model.recs);
  assert.match($("nfTitle").textContent, new RegExp(fmtN(m.total.nf) + " values not found"));
  assert.ok($("nfBody").innerHTML.includes('data-nftog="t:pay"'));
  // Companies with data: at least one value found or partial, per row (10 Nov 2026)
  const pay = m.tree.find((t) => t.sel.p === 1);
  const filled = D.values.filter((v) => v.p && (v.st === "found" || v.st === "partial"));
  if (pay) assert.ok((pay.withData > 0) === (filled.length > 0) && pay.withData <= pay.cosAll, "pay withData");
  assert.strictEqual(m.total.rows, D.values.filter((v) => v.st !== "not_applicable").length);
  assert.ok($("nfHead").innerHTML.includes("Companies with data"));
  // Rank: benchmarking rank from fieldList; group rows carry their best field's rank
  const ranks = window.ReportCore.fieldRanks(R.model);
  const rm = window.ReportCore.notFoundMatrix(R.model.recs, ranks);
  rm.tree.forEach((t) => t.children.forEach((k) => {
    k.children.forEach((d) => assert.strictEqual(d.rank, ranks[d.label] == null ? null : ranks[d.label]));
    const best = Math.min(...k.children.filter((d) => d.rank != null).map((d) => d.rank));
    assert.strictEqual(k.rank, isFinite(best) ? best : null);
  }));
  assert.ok($("nfHead").innerHTML.includes('data-sort="rank"'));
  assert.ok($("nfBody").innerHTML.includes("companies have at least one value found or partial here"));
  R.selectNotFound({ p: 1, k: "", d: "", c: countries[0] });
  const n = D.values.filter((v) => v.p && v.c === countries[0] && v.st === "not_found").length;
  assert.match($("nfDetail").innerHTML, new RegExp("Pay data · " + countries[0] + ": " + fmtN(n) + " values"));
  R.selectNotFound(null);
});
test("field coverage page uses the protocol field list", () => {
  R.show("coverage");
  assert.strictEqual(count($("cvTable").innerHTML, /data-field=/g), (D.fieldList || []).length || new Set(D.values.map((v) => v.d)).size);
  assert.match($("cvTitle").textContent, /^On average a field is found [\d.]+% of the time/);
});
test("export for Claude", () => {
  ["exSummary", "exSources", "exCoverage", "exNotFound", "exNotes", "exCompact"].forEach((id) => ($(id).checked = true));   // the stub ignores HTML "checked"
  $("exValues").value = "filled";
  R.show("export");
  const t = R.exportText();
  assert.match(t, /^# Allshares Part 1 accuracy data: export for analysis/);
  assert.match(t, /## Companies: reports found, links and coverage/);
  assert.match(t, /## Field coverage and validation by field/);
  assert.match(t, /## Not found by field and country/);
  assert.match(t, /## Values \(filled only\)/);
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

test("delivery pages render from the core's numbers", () => {
  const x = R.delivery();
  if (!x.ok) { R.show("standup"); assert.match($("suErr").innerHTML, /attn/); return; }
  R.show("standup");
  assert.strictEqual($("suTitle").textContent, x.titles.standup);
  assert.strictEqual(count($("suFunnel").innerHTML, /<tr>/g), x.stages.length + 1);
  assert.strictEqual(count($("suFunnel").innerHTML, /class="n stuck"/g), x.funnel.filter((f) => f.stuck > 0).length);
  R.show("throughput");
  assert.strictEqual($("tpTitle").textContent, x.titles.throughput);
  assert.strictEqual(count($("tpBatches").innerHTML, /<tr>/g), x.batchPlan.length);
  R.show("discovery");
  assert.strictEqual(count($("dqTable").innerHTML, /<tr>/g), x.discovery.rows.length || 1);
  R.show("exceptions");
  assert.strictEqual($("xcTitle").textContent, x.titles.exceptions);
  assert.strictEqual(count($("xcTable").innerHTML, /<tr>/g), x.exceptions.rows.length || 1);
  R.show("health");
  assert.strictEqual($("phTitle").textContent, x.titles.health);
  R.show("overview");
});

console.log(`\n${passed} tests passed (${path.relative(process.cwd(), HTML)})`);
