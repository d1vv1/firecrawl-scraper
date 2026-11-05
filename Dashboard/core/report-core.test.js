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
console.log(`\n${n} tests passed`);
