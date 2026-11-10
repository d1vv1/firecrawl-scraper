// Unit tests for the shared core. node Dashboard/core/report-core.test.js
"use strict";
const assert = require("assert");
const path = require("path");
const C = require("./report-core.js");

const data = require(path.join(__dirname, "..", "report.json"));
const schema = require(path.join(__dirname, "..", "allshares_import_schema.json"));
let n = 0;
function test(name, fn) { fn(); n++; console.log("ok -", name); }

test("percentile matches Excel PERCENTILE.INC", () => {
  const s = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  assert.strictEqual(C.percentile(s, 0.05), 1.45);
  assert.strictEqual(C.percentile(s, 0.5), 5.5);
  assert.strictEqual(C.percentile([7], 0.95), 7);
});
test("LEI check digits (ISO 17442)", () => {
  assert.ok(C.leiValid("549300HX9MRFY47AH564"));
  assert.ok(!C.leiValid("549300HX9MRFY47AH565"));
  assert.ok(!C.leiValid("short"));
});
// The data is whatever run was built last (python -m extractor.dashboard), so the tests check
// that the core's numbers agree with the data, not fixed counts.
const scored = data.values.filter((v) => v.gr);
test("model counts companies by key (LEI, else ID)", () => {
  const M = C.createModel(data);
  assert.strictEqual(C.companiesOf(M.recs), data.meta.companies);
  assert.strictEqual(new Set(M.recs.map((v) => v.id)).size, data.meta.companyIds);
  assert.strictEqual(C.gateStats(M, M.recs).checksPct, data.meta.checksPct);
});
test("gate and status totals match the data", () => {
  const M = C.createModel(data), g = C.gateStats(M, M.recs);
  const res = scored.flatMap((v) => v.gr.map((x) => x[1]));
  assert.deepStrictEqual([g.pass, g.fail, g.nr], ["P", "F", "N"].map((r) => res.filter((x) => x === r).length));
  const sc = C.scoreCounts(M.recs);
  ["P", "R", "F", "H"].forEach((k) => assert.strictEqual(sc[k], scored.filter((v) => v.sc === k).length, k));
  assert.strictEqual(sc.scored, data.meta.filled);
});
test("baseline: this run, then the previous run when there is one", () => {
  const M = C.createModel(data);
  assert.strictEqual(M.hist.length, M.histBase);
  assert.strictEqual(M.hist[0].checks, data.baseline.checksPct);
  const first = C.createModel(Object.assign({}, data, { baseline: { checksPct: 1, foundPct: 2, label: "This run" } }));
  assert.strictEqual(first.hist.length, 1);
  const second = C.createModel(Object.assign({}, data, { baseline: { checksPct: 1, foundPct: 2, label: "Previous run (x)" } }));
  assert.deepStrictEqual(second.hist.map((h) => h.checks), [1, data.meta.checksPct]);
  assert.match(C.kpis(second, second.recs).find((k) => k.key === "checks").d, /pts vs previous run/);
});
test("upsert: LEI first, then name + country; ambiguous without data_point", () => {
  const M = C.createModel(data);
  const co = M.recs.find((v) => v.d === "legal_name" && v.ck !== v.id);
  const base = { g: "company", p: 0, k: "x", m: "x", r: "", u: "", st: "found" };
  const res = C.applyImport(M, M.recs.map((v) => Object.assign({}, v)), [
    Object.assign({ line: 2, c: co.c, o: "Other Name", lei: co.ck, f: "C01", d: "legal_name", v: "Illustrative" }, base),
    Object.assign({ line: 3, c: co.c, o: co.o.toUpperCase(), lei: "", f: "C02", d: "lei", v: co.ck }, base),
    Object.assign({ line: 4, c: co.c, o: co.o, lei: "", f: "C01", d: "", v: "x" }, base),
    Object.assign({ line: 5, c: "SE", o: "Illustrative AB", lei: "", f: "C09", d: "", v: "example.org" }, base)
  ]);
  assert.deepStrictEqual(res.counts, { added: 1, updated: 1, same: 1, ambiguous: 1, dupes: 0 });
});
test("the UK as UK or GB: both valid, both match the run's GB company", () => {
  const M = C.createModel(data);
  const gb = M.recs.find((v) => v.d === "legal_name" && v.c === "GB");
  if (!gb) return;
  const csv = "country,company,size,grain,field_id,role_row,data_point,status,value,unit\n" +
    ["UK", "GB"].map((c) => `${c},${gb.o},large,company,C09,,website,found,example.org,`).join("\n") + "\n";
  const p = C.previewImport(M, schema, csv, "uk.csv");
  assert.deepStrictEqual(p.errs, []);
  assert.ok(p.good.every((r) => r.c === "GB"));
  const res = C.applyImport(M, M.recs.map((v) => Object.assign({}, v)), p.good);
  assert.strictEqual(res.counts.added, 0, "matched the existing company, not added as a new one");
});
test("validation: schema rules", () => {
  const M = C.createModel(data);
  const csv = "country,company,size,grain,field_id,role_row,data_point,status,value,unit,lei\n" +
    "XX,A,large,role,C05,,,found,,,BADLEI\n";
  const p = C.previewImport(M, schema, csv, "f.csv");
  const msgs = p.errs.map((e) => e.col + ": " + e.msg).join("\n");
  ["country: Not an allowed", "role_row: Required when grain is role", "data_point: Required", "value: Required when status is found", "lei: Not a valid"].forEach((m) => assert.ok(msgs.includes(m), m));
});
test("ranges options", () => {
  const M = C.createModel(data);
  const all = C.ranges(M.recs, {});
  assert.ok(all.rows.length > 0);
  const nz = C.ranges(M.recs, { excludeZeros: true, minN: 10 });
  assert.ok(nz.rows.every((r) => r.n >= 10 && r.min !== 0));
  const by = C.ranges(M.recs, { byCountry: true, field: "revenue" });
  assert.ok(by.rows.every((r) => r.d === "revenue" && r.c));
});
test("validation steps reconcile with gate totals and drill down", () => {
  const M = C.createModel(data), s = C.validationSteps(M, M.recs), g = C.gateStats(M, M.recs);
  const ran = new Set(scored.flatMap((v) => v.gr.map((x) => data.gateIds[x[0]])));
  assert.strictEqual(s.steps.length, ran.size);
  const order = ["CORE", "COD", "NUM", "DES", "DER", "XF"], keys = s.families.map((f) => f.key);
  assert.deepStrictEqual(keys, order.filter((k) => keys.includes(k)));
  const t = s.steps.reduce((a, x) => [a[0] + x.pass, a[1] + x.fail, a[2] + x.nr], [0, 0, 0]);
  assert.deepStrictEqual(t, [g.pass, g.fail, g.nr]);
  const top = s.steps.slice().sort((a, b) => b.fail - a.fail)[0];
  if (top.fail) {
    const d = C.stepDetail(M, M.recs, top.id);
    assert.deepStrictEqual([d.counts.runs, d.counts.fail], [top.runs, top.fail]);
    assert.strictEqual(d.fields.reduce((a, f) => a + f.runs, 0), top.runs);
    const field = d.fields.find((f) => f.fail);
    const v = C.stepFieldValues(M, M.recs, top.id, field.d, "F");
    assert.strictEqual(v.length, field.fail);
    assert.ok(v.every((x) => x.res === "F"));
  }
  assert.strictEqual(C.stepDetail(M, M.recs, "NOPE-01"), null);
});
test("metrics CSV has a BOM and 11 columns", () => {
  const M = C.createModel(data), csv = C.metricsCSV(C.metrics(M, M.recs));
  assert.strictEqual(csv.charCodeAt(0), 0xfeff);
  assert.strictEqual(csv.split("\r\n")[0].split(",").length, 11);
});
// ---- Delivery (SPEC 6.4): a small synthetic backlog, so the dates and counts are fixed
function dModel(companies, extra) {
  return C.createModel(Object.assign({}, data, {delivery: Object.assign({
    built: "2026-11-09", fiscalYear: "2025", stages: ["Required", "Document found", "Extracted", "Required fields 100%", "Rules passed", "Spot-checked", "Done"],
    batches: ["A", "B"], spotByBatch: {}, firecrawl: {credit_balance: 10, balance_as_of: "2026-11-09"}, scheduled: [],
    plan: {baseline_remaining: 4, baseline_date: "2026-11-09", deadline: "2026-11-13", daily_target: 1, working_days_only: true,
           exceptions_acceptance_date: "2026-12-01", pass_line: 0.95,
           batches: [{name: "A", start: "2026-11-10", end: "2026-11-11"}, {name: "B", start: "2026-11-12", end: "2026-11-13"}]},
    companies: companies, discovery: [{id: "d", o: "D", c: "SE", b: "B", need: "OpenAPI", next: "x", owner: "", status: "found"}],
    exceptions: [{id: "d", o: "D", c: "SE", b: "B", cat: "Document missing", reason: "r", source: "Tracker", accepted: "yes", note: ""}],
    runs: [{id: "a", name: "A", date: "2026-11-10", status: "ok", credits: 3}, {id: "b", name: "B", date: "2026-11-11", status: "failed", credits: 1, error: "e"}]
  }, extra || {})}));
}
const co = (id, b, stage, done, c, fc) => ({id: id, o: id.toUpperCase(), c: c || "SE", b: b, stage: stage, done: done || "", v: {n: 10, pass: 9, review: 0, fail: 1}, spot: null, fc: fc || {}, fx: {}});
test("delivery: funnel, stuck stage, burn-down and batch slippage", () => {
  const M = dModel([co("a", "A", 6, "2026-11-10"), co("b", "A", 2, "", "NO", {"Wrong currency": 2}), co("c", "B", 1), co("e", "B", 0)]);
  const x = C.delivery(M, "", "2026-11-11");
  assert.ok(x.ok);
  assert.deepStrictEqual(x.funnel[0].counts, [4, 3, 2, 1, 1, 1, 1]);
  assert.strictEqual(x.stages[x.funnel[0].stuck], "Document found");
  assert.deepStrictEqual([x.kpis.remaining, x.kpis.planNow, x.kpis.behind], [3, 2, 1]);
  assert.strictEqual(x.burn.days.find((d) => d.d === "2026-11-10").actual, 3);
  const a = x.batchPlan[0];
  assert.deepStrictEqual([a.todo, a.day, a.expected, a.done, a.status], [2, 2, 2, 1, "Behind by 1"]);
  assert.strictEqual(x.batchPlan[1].status, "Not started");
  assert.deepStrictEqual(x.failures, [{cat: "Wrong currency", companies: 1, values: 2}]);
  assert.strictEqual(x.passByBatch[0].rules, 90);
  assert.deepStrictEqual([x.discovery.resolved, x.exceptions.byCat[0].yes], [1, 1]);
  assert.deepStrictEqual([x.health.runs, x.health.failed, x.health.used, x.health.balance], [2, 1, 4, 6]);
  assert.strictEqual(C.delivery(M, "NO", "2026-11-11").kpis.companies, 1);
  assert.ok(C.exceptionsCSV(x.exceptions.rows).startsWith("﻿Company,"));
});
test("delivery: missing data gives an error, not a crash", () => {
  const M = C.createModel(Object.assign({}, data, {delivery: {error: "Delivery data not built: no tracker"}}));
  assert.deepStrictEqual(C.delivery(M), {ok: false, error: "Delivery data not built: no tracker"});
});
if (data.delivery && data.delivery.companies) test("delivery from report.json: funnel starts at the required companies", () => {
  const x = C.delivery(C.createModel(data));
  assert.strictEqual(x.funnel[0].counts[0], data.delivery.companies.length);
  assert.strictEqual(x.discovery.rows.length, data.delivery.discovery.length);
});

console.log(`\n${n} tests passed`);
