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
test("model counts companies by LEI", () => {
  const M = C.createModel(data);
  assert.strictEqual(C.companiesOf(M.recs), 49);
  assert.strictEqual(new Set(M.recs.map((v) => v.id)).size, 50);
  assert.strictEqual(C.gateStats(M, M.recs).checksPct, 92.2);
});
test("baseline gate totals", () => {
  const M = C.createModel(data), g = C.gateStats(M, M.recs);
  assert.deepStrictEqual([g.pass, g.fail, g.nr, g.hard], [15311, 1287, 2433, 438]);
  const sc = C.scoreCounts(M.recs);
  assert.deepStrictEqual([sc.P, sc.R, sc.F, sc.H, sc.I], [683, 493, 8, 404, 996]);
});
test("upsert: LEI first, then name + country; ambiguous without data_point", () => {
  const M = C.createModel(data);
  const syd = M.recs.find((v) => v.id === "T0002" && v.d === "legal_name");
  const base = { g: "company", p: 0, k: "x", m: "x", r: "", u: "", st: "found" };
  const res = C.applyImport(M, M.recs.map((v) => Object.assign({}, v)), [
    Object.assign({ line: 2, c: "DK", o: "Other Name", lei: syd.ck, f: "C01", d: "legal_name", v: "Illustrative" }, base),
    Object.assign({ line: 3, c: "DK", o: syd.o.toUpperCase(), lei: "", f: "C02", d: "", v: syd.ck }, base),
    Object.assign({ line: 4, c: "DK", o: syd.o, lei: "", f: "C01", d: "", v: "x" }, base),
    Object.assign({ line: 5, c: "SE", o: "Illustrative AB", lei: "", f: "C09", d: "", v: "example.org" }, base)
  ]);
  assert.deepStrictEqual(res.counts, { added: 1, updated: 1, same: 1, ambiguous: 1, dupes: 0 });
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
  assert.strictEqual(all.rows.length, 67);
  const nz = C.ranges(M.recs, { excludeZeros: true, minN: 10 });
  assert.ok(nz.rows.every((r) => r.n >= 10 && r.min !== 0));
  const fi = C.ranges(M.recs, { byCountry: true, field: "revenue" });
  assert.ok(fi.rows.every((r) => r.d === "revenue" && r.c));
});
test("validation steps reconcile with gate totals and drill down", () => {
  const M = C.createModel(data), s = C.validationSteps(M, M.recs);
  assert.strictEqual(s.steps.length, 33);
  assert.deepStrictEqual(s.families.map((f) => f.key), ["CORE", "COD", "NUM", "DES", "DER", "XF"]);
  const t = s.steps.reduce((a, x) => [a[0] + x.pass, a[1] + x.fail, a[2] + x.nr], [0, 0, 0]);
  assert.deepStrictEqual(t, [15311, 1287, 2433]);
  const d = C.stepDetail(M, M.recs, "NUM-09");
  assert.deepStrictEqual([d.counts.runs, d.counts.fail, d.sev], [92, 92, "Hard"]);
  assert.strictEqual(d.fields.reduce((a, f) => a + f.runs, 0), 92);
  const v = C.stepFieldValues(M, M.recs, "NUM-09", "lti_granted", "F");
  assert.strictEqual(v.length, 49);
  assert.ok(v.every((x) => x.res === "F" && x.reason));
  assert.strictEqual(C.stepDetail(M, M.recs, "NOPE-01"), null);
});
test("metrics CSV has a BOM and 11 columns", () => {
  const M = C.createModel(data), csv = C.metricsCSV(C.metrics(M, M.recs));
  assert.strictEqual(csv.charCodeAt(0), 0xfeff);
  assert.strictEqual(csv.split("\r\n")[0].split(",").length, 11);
});
console.log(`\n${n} tests passed`);
