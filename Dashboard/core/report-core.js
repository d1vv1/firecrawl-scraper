/* Allshares Part 1 dashboard core. Front-end logic shared by the Angular app and the single-file HTML:
   filters, aggregations, import validation and upsert, ranges, metrics, computed titles and the
   Delivery pages (funnel, pass rate by batch, failure patterns, burn-down, discovery, exceptions, health).
   No gate rules here: gate results come from the Python engine through report.json (SPEC section 5). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ReportCore = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var PAL = ["#0077BB", "#EE7733", "#009988", "#CC3311", "#888888"];
  var VSTAT = [["found", "Found", "#009988"], ["partial", "Partial", "#EE7733"], ["not_found", "Not found", "#CC3311"]];
  var SSTAT = [["P", "Pass", "#009988"], ["R", "Review", "#0077BB"], ["I", "Incomplete", "#888888"],
               ["F", "Fail", "#EE7733"], ["H", "Fail (hard)", "#CC3311"]];
  var SNAME = {}; SSTAT.forEach(function (s) { SNAME[s[0]] = s[1]; });
  var COUNTRIES = ["SE", "NO", "DK", "FI"];
  var GROUPS = ["Required fields", "Allowed values", "Role row", "Value when found", "Unit when numeric", "Data point when ambiguous"];
  var RANGE_FIELDS = ["aggregate_headcount", "base_salary", "benefits_value", "ebitda", "fte", "headcount", "lti_granted",
    "lti_max", "lti_target", "lti_vested", "pension_contribution", "revenue", "share_price", "shares_outstanding",
    "sti_max", "sti_paid", "sti_target", "total_assets", "total_remuneration"];
  var ISO_4217 = ["SEK", "NOK", "DKK", "EUR", "USD", "GBP", "CHF", "ISK", "PLN", "CAD", "AUD", "JPY", "CNY"];

  function pct(a, b) { return b ? Math.round(a / b * 100) : 0; }
  function pct1(a, b) { return b ? Math.round(a / b * 1000) / 10 : 0; }
  function lc(s) { return String(s || "").trim().toLowerCase(); }
  function fmt(n) { return n == null || n === "" ? "–" : Number(n).toLocaleString("en-GB", {maximumFractionDigits: 2}); }
  function num(s) {
    var t = String(s == null ? "" : s).trim().replace(/−/g, "-").replace(/ /g, "");
    return /^-?\d+(\.\d+)?$/.test(t) ? parseFloat(t) : null;
  }
  function clone(v) { var o = {}; for (var k in v) o[k] = v[k]; return o; }
  function companyKey(v) { return v.ck || (v.c + "|" + v.o); }
  // What the KPI deltas compare with: the previous run, or this run itself on a first build.
  function vsLabel(model) { return model.data.baseline.label === "This run" ? "this run" : "previous run"; }

  // ---------------------------------------------------------------- model
  function createModel(data) {
    var fidToDp = {}, dpMeta = {}, names = {};
    data.values.forEach(function (v) {
      (fidToDp[v.f] = fidToDp[v.f] || {})[v.d] = 1;
      if (!dpMeta[v.d]) dpMeta[v.d] = {d: v.d, f: v.f, k: v.k, m: v.m, g: v.g, p: v.p};
      if (!names[companyKey(v)]) names[companyKey(v)] = {key: companyKey(v), name: v.o, country: v.c};
    });
    Object.keys(fidToDp).forEach(function (f) { fidToDp[f] = Object.keys(fidToDp[f]); });
    return {
      data: data,
      recs: data.values.map(clone),
      hist: firstHist(data),
      histBase: firstHist(data).length,
      impCount: 0,
      fidToDp: fidToDp,
      dpMeta: dpMeta,
      companyNames: names
    };
  }
  // The baseline (the previous run), then this run when the two differ; imports add points after them.
  function firstHist(data) {
    var b = data.baseline, m = data.meta, h = [{label: b.label, checks: b.checksPct, found: b.foundPct, n: null, groups: null}];
    if (m.checksPct != null && b.label !== "This run") h.push({label: "This run (" + m.tracker + ")", checks: m.checksPct, found: m.foundPct, n: null, groups: null});
    return h;
  }
  function resetModel(model) {
    model.recs = model.data.values.map(clone);
    model.hist = firstHist(model.data);
    model.impCount = 0;
  }

  // ---------------------------------------------------------------- filters
  var EMPTY_FILTERS = {country: "", source: "all", dtype: "all", cat: "", company: "", status: "", fill: ""};
  // Value filter: filled = found or partial, empty = not found (not-applicable values are in neither).
  var FILL_OPTIONS = [["", "All values"], ["filled", "Filled (found or partial)"], ["empty", "Empty (not found)"]];
  function filterValues(recs, f) {
    f = f || EMPTY_FILTERS;
    return recs.filter(function (v) {
      if (f.country && v.c !== f.country) return false;
      if (f.source && f.source !== "all" && v.s !== f.source) return false;
      if (f.dtype === "pay" && !v.p) return false;
      if (f.dtype === "company" && v.p) return false;
      if (f.cat && v.k !== f.cat) return false;
      if (f.company && companyKey(v) !== f.company) return false;
      if (f.fill === "filled" && v.st !== "found" && v.st !== "partial") return false;
      if (f.fill === "empty" && v.st !== "not_found") return false;
      if (f.status) {
        if (f.status === "not_scored") { if (v.sc || v.st === "not_found") return false; }
        else if (f.status === "empty") { if (v.st !== "not_found") return false; }
        else if (v.sc !== f.status) return false;
      }
      return true;
    });
  }
  function filterOptions(model) {
    var cats = {}, cos = {};
    model.recs.forEach(function (v) { cats[v.k] = 1; cos[companyKey(v)] = v.o + " (" + v.c + ")"; });
    return {
      countries: (model.data.meta.countries || COUNTRIES).slice(),
      categories: Object.keys(cats).sort(),
      companies: Object.keys(cos).map(function (k) { return {key: k, label: cos[k]}; })
        .sort(function (a, b) { return a.label.localeCompare(b.label); }),
      statuses: SSTAT.map(function (s) { return {key: s[0], label: s[1]}; })
        .concat([{key: "empty", label: "Empty (not found)"}, {key: "not_scored", label: "Not scored (imported)"}])
    };
  }
  function anyFilter(f) {
    return !!(f.country || (f.source && f.source !== "all") || (f.dtype && f.dtype !== "all") || f.cat || f.company || f.status || f.fill);
  }

  // ---------------------------------------------------------------- counts
  function statusCounts(vs) {
    var o = {found: 0, partial: 0, not_found: 0, not_applicable: 0};
    vs.forEach(function (v) { o[v.st] = (o[v.st] || 0) + 1; });
    return o;
  }
  function scoreCounts(vs) {
    var o = {P: 0, R: 0, I: 0, F: 0, H: 0, scored: 0, notScored: 0, scoreSum: 0};
    vs.forEach(function (v) {
      if (v.sc) { o[v.sc]++; o.scored++; o.scoreSum += v.sp || 0; }
      else if (v.st !== "not_found") o.notScored++;
    });
    o.avg = o.scored ? Math.round(o.scoreSum / o.scored) : null;
    return o;
  }
  // Found % is over the values that apply: a not-applicable value (a group headcount on one
  // person's row, an SEC number for a company not filed there) is neither found nor missing.
  function applicable(s, n) { return n - (s.not_applicable || 0); }
  function foundPct(vs, one) { var s = statusCounts(vs), a = applicable(s, vs.length); return one ? pct1(s.found, a) : pct(s.found, a); }
  function companiesOf(vs) { var m = {}; vs.forEach(function (v) { m[companyKey(v)] = 1; }); return Object.keys(m).length; }
  function countriesOf(vs) { var m = {}; vs.forEach(function (v) { m[v.c] = 1; }); return COUNTRIES.filter(function (c) { return m[c]; }).concat(Object.keys(m).filter(function (c) { return COUNTRIES.indexOf(c) < 0; }).sort()); }
  function companyCountBy(vs, key) {
    var m = {};
    vs.forEach(function (v) { (m[v[key]] = m[v[key]] || {})[companyKey(v)] = 1; });
    var o = {}; Object.keys(m).forEach(function (k) { o[k] = Object.keys(m[k]).length; }); return o;
  }
  function gates(model, v) {
    if (!v.gr) return [];
    var d = model.data;
    return v.gr.map(function (g) {
      var id = d.gateIds[g[0]];
      return {gate: id, name: d.gates[id][0], sev: d.gates[id][1], res: g[1], reason: g[2] >= 0 ? d.reasons[g[2]] : ""};
    });
  }

  // ---------------------------------------------------------------- page aggregations
  function overview(vs) {
    var byC = companyCountBy(vs, "c");
    return {
      st: statusCounts(vs), n: vs.length, companies: companiesOf(vs),
      byCountryCompanies: countriesOf(vs).map(function (c) { return {c: c, n: byC[c] || 0}; }),
      rows: countriesOf(vs).map(function (c) {
        var cv = vs.filter(function (v) { return v.c === c; }), s = statusCounts(cv);
        return {c: c, companies: companiesOf(cv), n: cv.length, found: s.found, partial: s.partial, nf: s.not_found, foundPct: pct(s.found, applicable(s, cv.length))};
      })
    };
  }
  function payComp(vs) {
    var co = vs.filter(function (v) { return !v.p; }), pa = vs.filter(function (v) { return v.p; });
    return {
      co: co.length, pa: pa.length, sc: statusCounts(co), sp: statusCounts(pa),
      rows: countriesOf(vs).map(function (c) {
        var cc = co.filter(function (v) { return v.c === c; }), pp = pa.filter(function (v) { return v.c === c; });
        return {c: c, co: cc.length, coFound: foundPct(cc), pa: pp.length, paFound: foundPct(pp)};
      })
    };
  }
  function countriesPage(vs) {
    var cs = countriesOf(vs), byC = companyCountBy(vs, "c"), rows = [];
    cs.forEach(function (c) {
      ["Company data", "Pay data"].forEach(function (lbl) {
        var sub = vs.filter(function (v) { return v.c === c && ((lbl === "Pay data") === !!v.p); }), s = statusCounts(sub);
        rows.push({c: c, type: lbl, n: sub.length, found: s.found, partial: s.partial, nf: s.not_found});
      });
    });
    return {
      countries: cs,
      series: VSTAT.map(function (x) { return {name: x[1], color: x[2], values: cs.map(function (c) { return vs.filter(function (v) { return v.c === c && v.st === x[0]; }).length; })}; }),
      companies: cs.map(function (c) { return {c: c, n: byC[c] || 0}; }),
      rows: rows
    };
  }

  function gateStats(model, vs) {
    var runs = 0, fail = 0, nr = 0, hard = 0, soft = 0, perCheck = {}, mods = {}, fields = {};
    vs.forEach(function (v) {
      if (!v.gr) return;
      var fx = fields[v.d] || (fields[v.d] = {name: v.d, cat: v.k, mod: v.m, runs: 0, fail: 0, nr: 0, hard: 0});
      var mx = mods[v.m] || (mods[v.m] = {name: v.m, runs: 0, fail: 0, nr: 0});
      gates(model, v).forEach(function (g) {
        var p = perCheck[g.gate] || (perCheck[g.gate] = {id: g.gate, name: g.name, sev: g.sev, runs: 0, pass: 0, fail: 0, nr: 0});
        runs++; p.runs++; fx.runs++; mx.runs++;
        if (g.res === "F") { fail++; p.fail++; fx.fail++; mx.fail++; if (g.sev === "Hard") { hard++; fx.hard++; } else soft++; }
        else if (g.res === "N") { nr++; p.nr++; fx.nr++; mx.nr++; }
        else p.pass++;
      });
    });
    var checks = Object.keys(perCheck).map(function (k) { return perCheck[k]; }).sort(function (a, b) { return b.fail - a.fail || a.id.localeCompare(b.id); });
    var fl = Object.keys(fields).map(function (k) { var x = fields[k]; x.rate = pct(x.fail, x.runs - x.nr); return x; });
    var ranked = fl.filter(function (x) { return x.runs - x.nr >= 10; }).sort(function (a, b) { return b.rate - a.rate || b.fail - a.fail; });
    var modules = Object.keys(mods).map(function (k) { var x = mods[k]; x.rate = pct(x.fail, x.runs - x.nr); return x; });
    var topHard = checks.filter(function (x) { return x.sev === "Hard" && x.fail > 0; })[0] || null;
    return {runs: runs, fail: fail, nr: nr, pass: runs - fail - nr, hard: hard, soft: soft, checks: checks,
            fields: fl.sort(function (a, b) { return b.fail - a.fail; }), ranked: ranked, modules: modules,
            topHard: topHard, topField: ranked[0] || null,
            checksPct: pct1(runs - fail - nr, runs - nr)};
  }

  function fieldTable(model, vs) {
    var m = {};
    vs.forEach(function (v) {
      var x = m[v.d] || (m[v.d] = {d: v.d, f: v.f, k: v.k, m: v.m, g: v.g, rows: 0, found: 0, partial: 0, nf: 0,
                                    P: 0, R: 0, I: 0, F: 0, H: 0, scored: 0, scoreSum: 0, companies: {}, emptyCos: {}});
      x.rows++;
      if (v.st === "found") x.found++; else if (v.st === "partial") x.partial++; else if (v.st === "not_found") { x.nf++; x.emptyCos[companyKey(v)] = 1; }
      if (v.sc) { x[v.sc]++; x.scored++; x.scoreSum += v.sp || 0; }
      x.companies[companyKey(v)] = 1;
    });
    return Object.keys(m).map(function (k) {
      var x = m[k];
      x.passPct = pct(x.P, x.scored); x.avg = x.scored ? Math.round(x.scoreSum / x.scored) : null;
      x.nCompanies = Object.keys(x.companies).length; x.nEmptyCos = Object.keys(x.emptyCos).length;
      x.problems = x.F + x.H;
      delete x.companies; delete x.emptyCos; delete x.scoreSum;
      return x;
    }).sort(function (a, b) { return b.problems - a.problems || b.H - a.H || a.d.localeCompare(b.d); });
  }
  function fieldDetail(model, vs, dp) {
    var rows = vs.filter(function (v) { return v.d === dp; });
    return {
      dp: dp, meta: model.dpMeta[dp] || {},
      values: rows.filter(function (v) { return v.st !== "not_found" && v.st !== "not_applicable"; }).map(function (v) { return valueRow(model, v); }),
      empty: rows.filter(function (v) { return v.st === "not_found"; }).map(function (v) { return {key: companyKey(v), o: v.o, c: v.c, r: v.r, note: v.nt || ""}; })
    };
  }
  function valueRow(model, v) {
    var gs = gates(model, v);
    return {key: companyKey(v), o: v.o, c: v.c, id: v.id, d: v.d, f: v.f, k: v.k, r: v.r, v: v.v, u: v.u, pe: v.pe || "",
            me: v.me || "", so: v.so || "", ep: v.ep || "", nt: v.nt || "", st: v.st, sc: v.sc || "", scName: v.sc ? SNAME[v.sc] : (v.st === "not_found" ? "Empty" : "Not scored"),
            sp: v.sp == null ? null : v.sp, s: v.s,
            issues: gs.filter(function (g) { return g.res !== "P"; }).map(function (g) {
              return {gate: g.gate, sev: g.sev, res: g.res === "F" ? "fail" : "not run", reason: g.reason};
            })};
  }

  function emptyTables(model, vs) {
    var empty = vs.filter(function (v) { return v.st === "not_found"; });
    var byField = {}, byCo = {};
    vs.forEach(function (v) {
      var f = byField[v.d] || (byField[v.d] = {d: v.d, k: v.k, g: v.g, p: v.p, rows: 0, empty: 0, cos: {}});
      f.rows++;
      var c = byCo[companyKey(v)] || (byCo[companyKey(v)] = {key: companyKey(v), o: v.o, c: v.c, rows: 0, empty: 0, fields: {}});
      c.rows++;
      if (v.st === "not_found") { f.empty++; f.cos[companyKey(v)] = 1; c.empty++; c.fields[v.d] = 1; }
    });
    var fields = Object.keys(byField).map(function (k) { var x = byField[k]; x.pct = pct(x.empty, x.rows); x.companies = Object.keys(x.cos).length; delete x.cos; return x; })
      .filter(function (x) { return x.empty > 0; }).sort(function (a, b) { return b.empty - a.empty || a.d.localeCompare(b.d); });
    var cos = Object.keys(byCo).map(function (k) { var x = byCo[k]; x.pct = pct(x.empty, x.rows); x.fieldList = Object.keys(x.fields).sort(); delete x.fields; return x; })
      .sort(function (a, b) { return b.empty - a.empty || a.o.localeCompare(b.o); });
    var pay = empty.filter(function (v) { return v.p; }).length;
    return {n: empty.length, rows: vs.length, fields: fields, companies: cos, affected: cos.filter(function (c) { return c.empty; }).length,
            byType: [{label: "Company data", value: empty.length - pay, color: "#0077BB"}, {label: "Pay data", value: pay, color: "#EE7733"}]};
  }

  function companyTable(model, vs) {
    var m = {};
    vs.forEach(function (v) {
      var k = companyKey(v);
      var x = m[k] || (m[k] = {key: k, o: v.o, c: v.c, ids: {}, rows: 0, found: 0, partial: 0, nf: 0, na: 0, P: 0, R: 0, I: 0, F: 0, H: 0, scored: 0, scoreSum: 0});
      x.ids[v.id] = 1; x.rows++;
      if (v.st === "found") x.found++; else if (v.st === "partial") x.partial++; else if (v.st === "not_found") x.nf++; else if (v.st === "not_applicable") x.na++;
      if (v.sc) { x[v.sc]++; x.scored++; x.scoreSum += v.sp || 0; }
    });
    return Object.keys(m).map(function (k) {
      var x = m[k]; x.idList = Object.keys(x.ids).sort(); delete x.ids;
      x.avg = x.scored ? Math.round(x.scoreSum / x.scored) : null; delete x.scoreSum;
      x.foundPct = pct(x.found, x.rows - x.na);
      return x;
    }).sort(function (a, b) { return a.c.localeCompare(b.c) || a.o.localeCompare(b.o); });
  }
  function companyDetail(model, vs, key, mode) {
    var all = vs.filter(function (v) { return companyKey(v) === key; });
    if (!all.length) return null;
    var ids = {}; all.forEach(function (v) { ids[v.id] = 1; });
    var dup = (model.data.meta.duplicates || []).filter(function (d) { return d.lei === key; })[0] || null;
    var gs = gateStats(model, all);
    var rows = all;
    if (mode === "problems") rows = all.filter(function (v) { return v.sc === "H" || v.sc === "F" || v.sc === "I" || v.sc === "R"; });
    if (mode === "empty") rows = all.filter(function (v) { return v.st === "not_found"; });
    return {
      key: key, name: all[0].o, country: all[0].c, lei: /^[A-Z0-9]{20}$/.test(key) ? key : "", ids: Object.keys(ids).sort(),
      duplicate: dup, st: statusCounts(all), sc: scoreCounts(all), gates: gs,
      values: rows.slice().sort(function (a, b) { return a.k.localeCompare(b.k) || a.d.localeCompare(b.d) || (a.r || "").localeCompare(b.r || ""); })
        .map(function (v) { return valueRow(model, v); })
    };
  }

  // ---------------------------------------------------------------- validation steps (SPEC 6.3, 7a)
  var FAMILIES = [["CORE", "Core checks"], ["COD", "Codes and lists"], ["NUM", "Numbers"],
                  ["DES", "Descriptive claims"], ["DER", "Derived values"], ["XF", "Cross-field"]];
  var RESULT_NAME = {P: "PASS", F: "FAIL", N: "NOT RUN"};
  function familyOf(gate) { return gate.split("-")[0]; }
  function tally(o, res) { o.runs++; if (res === "P") o.pass++; else if (res === "F") o.fail++; else o.nr++; }
  function rates(o) { o.passPct = pct1(o.pass, o.runs - o.nr); o.failRate = pct(o.fail, o.runs - o.nr); return o; }
  function topReason(reasons) {
    var best = null; Object.keys(reasons).forEach(function (k) { if (!best || reasons[k] > reasons[best]) best = k; });
    return best ? {text: best, n: reasons[best]} : null;
  }
  // Level 1: every gate that ran, in family order, plus totals per family.
  function validationSteps(model, vs) {
    var order = model.data.gateIds, steps = {}, fams = {};
    FAMILIES.forEach(function (f) { fams[f[0]] = {key: f[0], name: f[1], runs: 0, pass: 0, fail: 0, nr: 0, steps: 0}; });
    vs.forEach(function (v) {
      if (!v.gr) return;
      v.gr.forEach(function (g) {
        var id = order[g[0]];
        var s = steps[id] || (steps[id] = {id: id, name: model.data.gates[id][0], sev: model.data.gates[id][1], family: familyOf(id),
                                            runs: 0, pass: 0, fail: 0, nr: 0, fieldSet: {}, reasons: {}});
        tally(s, g[1]); s.fieldSet[v.d] = 1;
        if (g[2] >= 0) { var t = model.data.reasons[g[2]]; s.reasons[t] = (s.reasons[t] || 0) + 1; }
        tally(fams[familyOf(id)], g[1]);
      });
    });
    var list = order.filter(function (id) { return steps[id]; }).map(function (id) {
      var s = steps[id]; s.fields = Object.keys(s.fieldSet).length; s.top = topReason(s.reasons);
      delete s.fieldSet; delete s.reasons; return rates(s);
    });
    list.forEach(function (s) { fams[s.family].steps++; });
    var families = FAMILIES.map(function (f) { return rates(fams[f[0]]); }).filter(function (f) { return f.runs; });
    var clean = list.filter(function (s) { return !s.fail; }).length, worst = list.slice().sort(function (a, b) { return b.fail - a.fail; })[0];
    return {steps: list, families: families,
            title: list.length ? clean + " of " + list.length + " validation steps have no fails" + (worst && worst.fail ? "; " + worst.id + " (" + worst.name + ") fails most: " + fmt(worst.fail) : "") : "No scored values in this selection"};
  }
  // Level 2: one gate, by field and by reason.
  function stepDetail(model, vs, gate) {
    var gi = model.data.gateIds.indexOf(gate);
    if (gi < 0) return null;
    var fields = {}, reasons = {}, tot = {runs: 0, pass: 0, fail: 0, nr: 0};
    vs.forEach(function (v) {
      if (!v.gr) return;
      v.gr.forEach(function (g) {
        if (g[0] !== gi) return;
        var f = fields[v.d] || (fields[v.d] = {d: v.d, f: v.f, k: v.k, runs: 0, pass: 0, fail: 0, nr: 0});
        tally(f, g[1]); tally(tot, g[1]);
        if (g[2] >= 0) {
          var key = g[1] + "|" + model.data.reasons[g[2]];
          var r = reasons[key] || (reasons[key] = {res: RESULT_NAME[g[1]], text: model.data.reasons[g[2]], n: 0, fields: {}});
          r.n++; r.fields[v.d] = 1;
        }
      });
    });
    var meta = model.data.gates[gate];
    return {id: gate, name: meta[0], sev: meta[1], family: (FAMILIES.filter(function (f) { return f[0] === familyOf(gate); })[0] || [, ""])[1],
            counts: rates(tot),
            fields: Object.keys(fields).map(function (k) { return rates(fields[k]); }).sort(function (a, b) { return b.fail - a.fail || b.nr - a.nr || a.d.localeCompare(b.d); }),
            reasons: Object.keys(reasons).map(function (k) { var r = reasons[k]; r.fieldList = Object.keys(r.fields).sort(); delete r.fields; return r; })
              .sort(function (a, b) { return b.n - a.n; })};
  }
  // Level 3: one gate on one field, value by value. mode: all | F | N | P
  function stepFieldValues(model, vs, gate, dp, mode) {
    var gi = model.data.gateIds.indexOf(gate), out = [];
    vs.forEach(function (v) {
      if (v.d !== dp || !v.gr) return;
      v.gr.forEach(function (g) {
        if (g[0] !== gi || (mode && mode !== "all" && g[1] !== mode)) return;
        out.push({key: companyKey(v), o: v.o, c: v.c, id: v.id, r: v.r, v: v.v, u: v.u, pe: v.pe || "", res: g[1], resName: RESULT_NAME[g[1]],
                  reason: g[2] >= 0 ? model.data.reasons[g[2]] : "", sc: v.sc || "", scName: v.sc ? SNAME[v.sc] : "Not scored", sp: v.sp == null ? null : v.sp});
      });
    });
    var rank = {F: 0, N: 1, P: 2};
    return out.sort(function (a, b) { return rank[a.res] - rank[b.res] || a.o.localeCompare(b.o) || (a.r || "").localeCompare(b.r || ""); });
  }

  // ---------------------------------------------------------------- ranges
  function percentile(sorted, p) {
    if (!sorted.length) return null;
    var k = (sorted.length - 1) * p, lo = Math.floor(k), hi = Math.ceil(k);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (k - lo);
  }
  function rangeUnit(u) { return (u === "" || u === "instruments") ? "unknown" : u; }
  var RANGE_DEFAULTS = {field: "", unit: "", grain: "", method: "", include: "all", excludeZeros: false,
                        excludeUnknownUnits: false, low: 5, high: 95, minN: 1, byCountry: false};
  function ranges(vs, opts) {
    var o = {}; for (var k in RANGE_DEFAULTS) o[k] = RANGE_DEFAULTS[k];
    for (var j in (opts || {})) if (opts[j] !== undefined) o[j] = opts[j];
    var lo = Math.max(0, Math.min(100, Number(o.low))) / 100, hi = Math.max(0, Math.min(100, Number(o.high))) / 100;
    if (lo > hi) { var t = lo; lo = hi; hi = t; }
    var groups = {};
    vs.forEach(function (v) {
      if (RANGE_FIELDS.indexOf(v.d) < 0 || v.st === "not_found") return;
      var n = num(v.v); if (n === null) return;
      var unit = rangeUnit(v.u);
      if (o.field && v.d !== o.field) return;
      if (o.unit && unit !== o.unit) return;
      if (o.grain && v.g !== o.grain) return;
      if (o.method && v.me !== o.method) return;
      if (o.include === "nohard" && v.sc === "H") return;
      if (o.include === "passreview" && v.sc !== "P" && v.sc !== "R") return;
      if (o.excludeZeros && n === 0) return;
      var nonIso = unit === "unknown" || (/^[A-Z]{3,5}$/.test(unit) && ISO_4217.indexOf(unit) < 0);
      if (o.excludeUnknownUnits && nonIso) return;
      var key = v.d + "|" + unit + (o.byCountry ? "|" + v.c : "");
      var g = groups[key] || (groups[key] = {d: v.d, unit: unit, c: o.byCountry ? v.c : "", vals: [], cos: {}});
      g.vals.push(n); g.cos[companyKey(v)] = 1;
    });
    var rows = Object.keys(groups).sort().map(function (k) {
      var g = groups[k], s = g.vals.slice().sort(function (a, b) { return a - b; }), med = percentile(s, 0.5), cav = [];
      if (s.some(function (x) { return x === 0; })) cav.push("zero values present (check not found vs true zero)");
      if (g.d === "ebitda") cav.push("losses expected; negatives are valid");
      if (med > 0 && s[s.length - 1] > 100 * med) cav.push("max is over 100x median: possible unit error");
      if (g.unit === "unknown") cav.push("currency not recorded");
      if (g.unit === "EURO") cav.push("non-ISO unit label");
      if (s.length < 10) cav.push("n under 10: indicative only");
      return {d: g.d, unit: g.unit, c: g.c, n: s.length, companies: Object.keys(g.cos).length, min: s[0],
              low: percentile(s, lo), median: med, high: percentile(s, hi), max: s[s.length - 1], caveat: cav.join("; ")};
    }).filter(function (r) { return r.n >= (Number(o.minN) || 1); });
    return {opts: o, lowLabel: Math.round(lo * 100), highLabel: Math.round(hi * 100), rows: rows};
  }
  function rangeOptions(vs) {
    var units = {}, methods = {};
    vs.forEach(function (v) { if (RANGE_FIELDS.indexOf(v.d) >= 0 && num(v.v) !== null) { units[rangeUnit(v.u)] = 1; if (v.me) methods[v.me] = 1; } });
    return {fields: RANGE_FIELDS.slice(), units: Object.keys(units).sort(), methods: Object.keys(methods).sort()};
  }

  // ---------------------------------------------------------------- reports and sources (SPEC 6.3, 12)
  // Source group of a value, from its source name: the same three groups as the Source List sheet of
  // allshares_fields_list.xlsx. Annual report filings (ESEF, SEC 20-F / 10-K, Companies House accounts)
  // count as the annual report; anything naming a remuneration report or policy as the remuneration report.
  var SRC_GROUPS = [["annual", "Annual report"], ["rem", "Remuneration report"], ["other", "Other sources"]];
  function sourceGroup(so) {
    var s = lc(so);
    if (!s) return "";
    if (/remunerat/.test(s)) return "rem";
    if (/annual report|esef|20-f|10-k|companies house filing/.test(s)) return "annual";
    return "other";
  }
  function srcGroupName(g) { var x = SRC_GROUPS.filter(function (s) { return s[0] === g; })[0]; return x ? x[1] : ""; }
  function isUrl(u) { return /^https?:\/\//i.test(String(u || "")); }
  function docUrl(u) { return String(u || "").split("#")[0]; }
  function hostOf(u) { var m = /^https?:\/\/([^\/?#]+)/i.exec(String(u || "")); return m ? m[1].replace(/^www\./, "") : ""; }
  function newCo(v) {
    return {key: companyKey(v), o: v.o, c: v.c, ids: {}, dps: {}, dpFilled: {}, rows: 0, na: 0, found: 0, partial: 0, nf: 0,
            scored: 0, P: 0, runs: 0, pass: 0, n: {annual: 0, rem: 0, other: 0}, links: {annual: {}, rem: {}, other: {}}};
  }
  // One row per company: whether an annual / remuneration report was used, its links, and coverage KPIs.
  function sources(model, vs) {
    var m = {};
    vs.forEach(function (v) {
      var x = m[companyKey(v)] || (m[companyKey(v)] = newCo(v));
      x.ids[v.id] = 1; x.dps[v.d] = 1; x.rows++;
      if (v.st === "found") x.found++; else if (v.st === "partial") x.partial++; else if (v.st === "not_found") x.nf++; else if (v.st === "not_applicable") x.na++;
      if (v.st === "found" || v.st === "partial") x.dpFilled[v.d] = 1;
      if (v.sc) { x.scored++; if (v.sc === "P") x.P++; }
      (v.gr || []).forEach(function (g) { if (g[1] !== "N") { x.runs++; if (g[1] === "P") x.pass++; } });
      var grp = sourceGroup(v.so);
      if (!grp) return;
      x.n[grp]++;
      if (isUrl(v.ep)) {
        var doc = docUrl(v.ep);   // one link per document: page anchors and text fragments are dropped
        var l = x.links[grp][doc] || (x.links[grp][doc] = {url: doc, label: v.so, host: hostOf(doc), n: 0});
        l.n++;
      }
    });
    var rows = Object.keys(m).map(function (k) {
      var x = m[k];
      x.idList = Object.keys(x.ids).sort(); x.fields = Object.keys(x.dps).length; x.fieldsFilled = Object.keys(x.dpFilled).length;
      x.fieldsEmpty = x.fields - x.fieldsFilled; x.values = x.rows - x.na;
      x.foundPct = pct(x.found, x.values); x.filledPct = pct(x.found + x.partial, x.values);
      x.passPct = x.scored ? pct(x.P, x.scored) : null; x.checksPct = x.runs ? pct1(x.pass, x.runs) : null;
      SRC_GROUPS.forEach(function (g) {
        var ls = x.links[g[0]];
        x.links[g[0]] = Object.keys(ls).map(function (u) { return ls[u]; }).sort(function (a, b) { return b.n - a.n || a.url.localeCompare(b.url); });
      });
      x.hasAnnual = x.n.annual > 0; x.hasRem = x.n.rem > 0;
      x.reports = x.hasAnnual && x.hasRem ? "Both" : x.hasAnnual ? "Annual only" : x.hasRem ? "Remuneration only" : "Neither";
      delete x.ids; delete x.dps; delete x.dpFilled;
      return x;
    }).sort(function (a, b) { return a.c.localeCompare(b.c) || a.o.localeCompare(b.o); });
    function tot(list) {
      var t = {companies: list.length, annual: 0, rem: 0, both: 0, neither: 0};
      list.forEach(function (x) { if (x.hasAnnual) t.annual++; if (x.hasRem) t.rem++; if (x.hasAnnual && x.hasRem) t.both++; if (!x.hasAnnual && !x.hasRem) t.neither++; });
      t.annualPct = pct(t.annual, t.companies); t.remPct = pct(t.rem, t.companies); t.bothPct = pct(t.both, t.companies); t.neitherPct = pct(t.neither, t.companies);
      return t;
    }
    var byCountry = countriesOf(vs).map(function (c) { var t = tot(rows.filter(function (x) { return x.c === c; })); t.c = c; return t; });
    var t = tot(rows);
    return {rows: rows, totals: t, byCountry: byCountry,
            title: rows.length ? "Annual report found for " + t.annual + " of " + t.companies + " companies (" + t.annualPct + "%); remuneration report for " + t.rem + " (" + t.remPct + "%)" : "No companies in this selection"};
  }

  // ---------------------------------------------------------------- not-found matrix (Pay vs company, SPEC 6.3)
  // Rows: data type > field group > field. Columns: countries. Cell: values not found of the values that apply.
  function notFoundMatrix(vs) {
    var cs = countriesOf(vs), types = {};
    function node(id, label, level, sel) { return {id: id, label: label, level: level, sel: sel, rows: 0, nf: 0, cos: {}, dcos: {}, acos: {}, byC: {}, kids: {}}; }
    function add(n, v) {
      n.rows++;
      var ck = companyKey(v);
      n.acos[ck] = 1;
      if (v.st === "found" || v.st === "partial") n.dcos[ck] = 1;
      var c = n.byC[v.c] || (n.byC[v.c] = {rows: 0, nf: 0});
      c.rows++;
      if (v.st === "not_found") { n.nf++; c.nf++; n.cos[ck] = 1; }
    }
    vs.forEach(function (v) {
      if (v.st === "not_applicable") return;
      var tk = v.p ? "pay" : "company", p = v.p ? 1 : 0;
      var t = types[tk] || (types[tk] = node("t:" + tk, v.p ? "Pay data" : "Company data", 0, {p: p}));
      var k = t.kids[v.k] || (t.kids[v.k] = node("k:" + tk + "|" + v.k, v.k, 1, {p: p, k: v.k}));
      var d = k.kids[v.d] || (k.kids[v.d] = node("d:" + v.d, v.d, 2, {p: p, k: v.k, d: v.d}));
      add(t, v); add(k, v); add(d, v);
    });
    function fin(n) {
      n.pct = pct(n.nf, n.rows); n.companies = Object.keys(n.cos).length; n.withData = Object.keys(n.dcos).length; n.cosAll = Object.keys(n.acos).length;
      delete n.cos; delete n.dcos; delete n.acos;
      cs.forEach(function (c) { var x = n.byC[c]; if (x) x.pct = pct(x.nf, x.rows); });
      n.children = Object.keys(n.kids).map(function (k) { return fin(n.kids[k]); }).sort(function (a, b) { return b.nf - a.nf || a.label.localeCompare(b.label); });
      delete n.kids;
      return n;
    }
    var tree = ["company", "pay"].filter(function (k) { return types[k]; }).map(function (k) { return fin(types[k]); });
    var all = node("all", "All values", -1, {}); delete all.kids;
    vs.forEach(function (v) { if (v.st !== "not_applicable") add(all, v); });
    all.rows = 0; all.nf = 0; all.byC = {};   // add() only collects the companies; the counts come from the tree
    tree.forEach(function (t) {
      all.rows += t.rows; all.nf += t.nf;
      cs.forEach(function (c) { var x = t.byC[c]; if (!x) return; var a = all.byC[c] || (all.byC[c] = {rows: 0, nf: 0}); a.rows += x.rows; a.nf += x.nf; });
    });
    all.pct = pct(all.nf, all.rows); all.companies = Object.keys(all.cos).length; all.withData = Object.keys(all.dcos).length;
    all.cosAll = Object.keys(all.acos).length; delete all.cos; delete all.dcos; delete all.acos; delete all.id; delete all.label; delete all.level; delete all.sel;
    cs.forEach(function (c) { if (all.byC[c]) all.byC[c].pct = pct(all.byC[c].nf, all.byC[c].rows); });
    var fields = [];
    tree.forEach(function (t) { t.children.forEach(function (k) { fields = fields.concat(k.children); }); });
    var top = fields.slice().sort(function (a, b) { return b.nf - a.nf; })[0];
    return {countries: cs, tree: tree, total: all,
            title: all.nf ? fmt(all.nf) + " values not found (" + all.pct + "%)" + (top && top.nf ? "; " + top.label + " is missing most often (" + fmt(top.nf) + ")" : "") : "Nothing missing in this selection"};
  }
  // The not-found values behind one matrix cell. sel: {p, k, d, c}; any may be left out.
  function notFoundValues(vs, sel) {
    sel = sel || {};
    return vs.filter(function (v) {
      return v.st === "not_found" && (sel.p == null || (v.p ? 1 : 0) === sel.p) && (!sel.k || v.k === sel.k) && (!sel.d || v.d === sel.d) && (!sel.c || v.c === sel.c);
    }).map(function (v) { return {key: companyKey(v), o: v.o, c: v.c, id: v.id, r: v.r, d: v.d, f: v.f, k: v.k, type: v.p ? "Pay data" : "Company data", note: v.nt || ""}; })
      .sort(function (a, b) { return a.o.localeCompare(b.o) || a.d.localeCompare(b.d) || (a.r || "").localeCompare(b.r || ""); });
  }

  // ---------------------------------------------------------------- field coverage (SPEC 6.3, 13)
  // One row per field of the protocol field list (Company Data and Pay Data sheets of
  // allshares_fields_list.xlsx, carried in report.json as fieldList): found and validation by field,
  // with the average across the fields of each group and sheet.
  function fieldList(model) {
    var fl = model.data.fieldList || [];
    if (fl.length) return fl;
    return Object.keys(model.dpMeta).sort().map(function (d, i) {
      var x = model.dpMeta[d];
      return {sheet: x.p ? "Pay Data" : "Company Data", n: i + 1, d: d, f: x.f, k: x.k, g: x.g, what: "", checks: []};
    });
  }
  function fieldCoverage(model, vs) {
    var m = {};
    vs.forEach(function (v) {
      var x = m[v.d] || (m[v.d] = {rows: 0, na: 0, found: 0, partial: 0, nf: 0, cos: {}, filledCos: {}, scored: 0, P: 0, H: 0, scoreSum: 0, runs: 0, pass: 0, fail: 0});
      x.rows++; x.cos[companyKey(v)] = 1;
      if (v.st === "found") x.found++; else if (v.st === "partial") x.partial++; else if (v.st === "not_found") x.nf++; else if (v.st === "not_applicable") x.na++;
      if (v.st === "found" || v.st === "partial") x.filledCos[companyKey(v)] = 1;
      if (v.sc) { x.scored++; x.scoreSum += v.sp || 0; if (v.sc === "P") x.P++; if (v.sc === "H") x.H++; }
      (v.gr || []).forEach(function (g) { if (g[1] === "P") { x.runs++; x.pass++; } else if (g[1] === "F") { x.runs++; x.fail++; } });
    });
    var sheets = {}, order = [];
    fieldList(model).forEach(function (f) {
      var x = m[f.d];
      var r = {sheet: f.sheet, n: f.n, d: f.d, f: f.f, k: f.k, g: f.g, what: f.what || "", checks: f.checks || [], inView: !!x,
               req: f.req || "", reqClass: reqClass(f.req), sev: f.sev || "", fill50: f.fill50 == null ? null : f.fill50, milestone: f.milestone || "", why: f.why || "",
               rows: 0, found: 0, partial: 0, nf: 0, companies: 0, filledCos: 0, foundPct: null, filledPct: null, checkRuns: 0, checkFail: 0,
               checkPct: null, scored: 0, P: 0, H: 0, passPct: null, avg: null};
      if (x) {
        var a = x.rows - x.na;
        r.rows = a; r.found = x.found; r.partial = x.partial; r.nf = x.nf;
        r.companies = Object.keys(x.cos).length; r.filledCos = Object.keys(x.filledCos).length;
        r.foundPct = a ? pct1(x.found, a) : null; r.filledPct = a ? pct1(x.found + x.partial, a) : null;
        r.checkRuns = x.runs; r.checkFail = x.fail; r.checkPct = x.runs ? pct1(x.pass, x.runs) : null;
        r.scored = x.scored; r.P = x.P; r.H = x.H; r.passPct = x.scored ? pct1(x.P, x.scored) : null;
        r.avg = x.scored ? Math.round(x.scoreSum / x.scored) : null;
      }
      var s = sheets[f.sheet];
      if (!s) { s = sheets[f.sheet] = {name: f.sheet, fields: [], cats: {}, catOrder: []}; order.push(f.sheet); }
      if (!s.cats[f.k]) { s.cats[f.k] = {k: f.k, fields: []}; s.catOrder.push(f.k); }
      s.cats[f.k].fields.push(r); s.fields.push(r);
    });
    function avg(list, key) {
      var xs = list.filter(function (r) { return r[key] != null; });
      return xs.length ? Math.round(xs.reduce(function (a, r) { return a + r[key]; }, 0) / xs.length * 10) / 10 : null;
    }
    function summary(o, list) {
      o.nFields = list.length; o.inView = list.filter(function (r) { return r.inView; }).length;
      o.avgFound = avg(list, "foundPct"); o.avgFilled = avg(list, "filledPct"); o.avgCheck = avg(list, "checkPct"); o.avgPass = avg(list, "passPct");
      o.alwaysFound = list.filter(function (r) { return r.filledPct === 100; }).length;
      o.neverFound = list.filter(function (r) { return r.inView && r.rows && !r.found && !r.partial; }).length;
      return o;
    }
    var out = order.map(function (n) {
      var s = sheets[n];
      s.cats = s.catOrder.map(function (k) { return summary(s.cats[k], s.cats[k].fields); });
      delete s.catOrder;
      return summary(s, s.fields);
    });
    var all = summary({name: "All fields"}, out.reduce(function (a, s) { return a.concat(s.fields); }, []));
    return {sheets: out, all: all,
            title: all.inView ? "On average a field is found " + all.avgFound + "% of the time and passes " + (all.avgCheck == null ? "–" : all.avgCheck + "%") + " of its checks (" + all.inView + " fields)" : "No fields in this selection"};
  }

  // ---------------------------------------------------------------- Company Data and Pay Data pages (SPEC 6.3, 15)
  // The field review (requirement, severity, fill in the 50-company review, why) next to this run's
  // found and validation results, for one sheet of the field list.
  var SEVERITIES = ["High", "Medium", "Low", "Never used"];
  var REQ_CLASSES = [["required", "Required"], ["conditional", "Required (conditional)"], ["optional", "Optional"]];
  function reqClass(req) {
    var s = lc(req);
    if (!s) return "";
    if (s === "required") return "required";
    if (s.indexOf("required") === 0) return "conditional";
    return "optional";
  }
  function dataPage(model, vs, sheet) {
    var fc = fieldCoverage(model, vs), s = fc.sheets.filter(function (x) { return x.name === sheet; })[0];
    var fields = s ? s.fields : [], cos = companiesOf(vs);
    fields.forEach(function (r) { r.filledCosPct = cos ? pct(r.filledCos, cos) : null; r.fill50Pct = r.fill50 == null ? null : r.fill50 * 2; });
    function mean(list, key) {
      var xs = list.filter(function (r) { return r[key] != null; });
      return xs.length ? Math.round(xs.reduce(function (a, r) { return a + r[key]; }, 0) / xs.length * 10) / 10 : null;
    }
    function group(list) { return {n: list.length, avgFound: mean(list, "foundPct"), avgFilled: mean(list, "filledPct"), avgCheck: mean(list, "checkPct"), avgPass: mean(list, "passPct")}; }
    var must = fields.filter(function (r) { return r.reqClass === "required" || r.reqClass === "conditional"; });
    var bySev = SEVERITIES.map(function (v) { var g = group(fields.filter(function (r) { return r.sev === v; })); g.sev = v; return g; }).filter(function (g) { return g.n; });
    var byReq = REQ_CLASSES.map(function (c) { var g = group(fields.filter(function (r) { return r.reqClass === c[0]; })); g.key = c[0]; g.label = c[1]; return g; }).filter(function (g) { return g.n; });
    var gaps = fields.filter(function (r) { return r.sev === "High" && r.filledPct != null && r.filledPct < 80; }).sort(function (a, b) { return a.filledPct - b.filledPct; });
    var milestones = {};
    fields.forEach(function (r) { if (r.milestone) (milestones[r.milestone] = milestones[r.milestone] || []).push(r); });
    var label = sheet === "Pay Data" ? "pay" : "company";
    var mg = group(must);
    return {sheet: sheet, fields: fields, companies: cos, required: mg, all: group(fields), bySev: bySev, byReq: byReq, gaps: gaps,
            neverUsed: fields.filter(function (r) { return r.sev === "Never used"; }).length,
            milestones: Object.keys(milestones).map(function (k) { var g = group(milestones[k]); g.name = k; return g; }),
            title: fields.length ? "Required " + label + " fields are filled " + (mg.avgFilled == null ? "–" : mg.avgFilled + "%") + " of the time on average; " +
              (gaps.length ? gaps.length + " high-severity " + (gaps.length === 1 ? "field is" : "fields are") + " under 80%: " + gaps.slice(0, 4).map(function (r) { return r.d; }).join(", ") + (gaps.length > 4 ? "…" : "")
                           : "every high-severity field is at 80% or more") : "No fields in this selection"};
  }
  function dataPageCSV(dp) {
    var pay = dp.sheet === "Pay Data";
    return toCSV(["n", "data_point", "field_id", "field_group", "requirement", "severity"].concat(pay ? ["milestone_1_dec"] : [])
      .concat(["fill_of_50_review", "companies_with_value", "companies", "found_pct", "filled_pct", "check_pass_pct", "values_pass_pct", "why"]),
      dp.fields.map(function (r) {
        return [r.n, r.d, r.f, r.k, r.req, r.sev].concat(pay ? [r.milestone] : []).concat([r.fill50 == null ? "" : r.fill50, r.filledCos, dp.companies,
          r.foundPct == null ? "" : r.foundPct, r.filledPct == null ? "" : r.filledPct, r.checkPct == null ? "" : r.checkPct, r.passPct == null ? "" : r.passPct, r.why]);
      }), true);
  }

  // ---------------------------------------------------------------- export for Claude (SPEC 6.3, 14)
  // compact: value columns without URL and note, values cut at 200 characters (about a third of the size).
  var EXPORT_DEFAULTS = {summary: true, sources: true, coverage: true, notFound: true, values: "filled", compact: true, notes: true, maxValues: 0};
  function filterText(f, model) {
    var parts = [];
    f = f || EMPTY_FILTERS;
    if (f.country) parts.push("country " + f.country);
    if (f.source && f.source !== "all") parts.push(f.source === "T" ? "this run only" : "imported only");
    if (f.dtype && f.dtype !== "all") parts.push(f.dtype + " data");
    if (f.cat) parts.push("field group " + f.cat);
    if (f.company) parts.push("company " + ((model.companyNames[f.company] || {}).name || f.company));
    if (f.status) parts.push("score status " + (SNAME[f.status] || f.status));
    if (f.fill) parts.push(f.fill === "filled" ? "filled values only" : "empty values only");
    return parts.length ? parts.join(", ") : "none (all values)";
  }
  function csvBlock(title, intro, csv) {
    var FENCE = "```";
    return "## " + title + "\n\n" + (intro ? intro + "\n\n" : "") + FENCE + "csv\n" + csv.replace(/\r\n$/, "").replace(/\r\n/g, "\n") + "\n" + FENCE + "\n";
  }
  function exportValues(vs, mode) {
    return vs.filter(function (v) {
      if (mode === "filled") return v.st === "found" || v.st === "partial";
      if (mode === "empty") return v.st === "not_found";
      return mode === "all";
    });
  }
  function valuesCSV(model, list, compact) {
    var head = ["company", "country", "company_key", "company_id", "data_type", "field_group", "field_id", "data_point", "role", "value", "unit",
                "period_end", "value_status", "score_status", "score", "source", "source_group", "url", "failed_checks", "note"];
    if (compact) head = head.filter(function (h) { return h !== "url" && h !== "note" && h !== "company_id"; });
    return toCSV(head, list.map(function (v) {
      var fails = gates(model, v).filter(function (g) { return g.res === "F"; }).map(function (g) { return compact ? g.gate : g.gate + (g.reason ? ": " + g.reason : ""); }).join(" | ");
      var val = compact && String(v.v).length > 200 ? String(v.v).slice(0, 200) + "…" : v.v;
      var row = {company: v.o, country: v.c, company_key: companyKey(v), company_id: v.id, data_type: v.p ? "pay" : "company", field_group: v.k, field_id: v.f,
                 data_point: v.d, role: v.r, value: val, unit: v.u, period_end: v.pe || "", value_status: v.st, score_status: v.sc ? SNAME[v.sc] : "",
                 score: v.sp == null ? "" : v.sp, source: v.so || "", source_group: srcGroupName(sourceGroup(v.so)), url: v.ep || "", failed_checks: fails, note: v.nt || ""};
      return head.map(function (h) { return row[h]; });
    }));
  }
  function sourcesCSV(rows) {
    function urls(l) { return l.map(function (u) { return u.url; }).join(" | "); }
    return toCSV(["company", "country", "company_key", "annual_report_found", "remuneration_report_found", "annual_report_links", "remuneration_report_links", "other_source_links",
                  "protocol_fields", "fields_filled", "fields_empty", "values", "found", "partial", "not_found", "found_pct",
                  "values_from_annual_report", "values_from_remuneration_report", "values_from_other_sources", "values_pass_pct", "checks_pass_pct"],
      rows.map(function (x) {
        return [x.o, x.c, x.key, x.hasAnnual ? "yes" : "no", x.hasRem ? "yes" : "no", urls(x.links.annual), urls(x.links.rem), urls(x.links.other),
                x.fields, x.fieldsFilled, x.fieldsEmpty, x.values, x.found, x.partial, x.nf, x.foundPct, x.n.annual, x.n.rem, x.n.other,
                x.passPct == null ? "" : x.passPct, x.checksPct == null ? "" : x.checksPct];
      }));
  }
  function coverageCSV(fc) {
    var rows = [];
    fc.sheets.forEach(function (sh) {
      sh.fields.forEach(function (r) {
        rows.push([sh.name, r.k, r.n, r.d, r.f, r.g, r.req, r.sev, r.milestone, r.fill50 == null ? "" : r.fill50, r.why, r.what, r.rows, r.found, r.partial, r.nf, r.foundPct == null ? "" : r.foundPct, r.filledPct == null ? "" : r.filledPct,
                   r.filledCos, r.companies, r.checkRuns, r.checkFail, r.checkPct == null ? "" : r.checkPct, r.passPct == null ? "" : r.passPct, r.avg == null ? "" : r.avg, r.checks.join(" ")]);
      });
    });
    return toCSV(["sheet", "field_group", "n", "data_point", "field_id", "grain", "requirement", "severity", "milestone_1_dec", "fill_of_50_review", "why", "what_it_is", "values", "found", "partial", "not_found", "found_pct", "filled_pct",
                  "companies_with_value", "companies", "checks_run", "checks_failed", "check_pass_pct", "values_pass_pct", "avg_score", "checks_applied"], rows);
  }
  function notFoundCSV(nm) {
    var rows = [];
    nm.tree.forEach(function (t) { t.children.forEach(function (k) { k.children.forEach(function (d) {
      rows.push([t.label, k.label, d.label, d.rows, d.nf, d.pct, d.companies, d.withData].concat(nm.countries.map(function (c) { var x = d.byC[c]; return x ? x.nf + "/" + x.rows : ""; })));
    }); }); });
    return toCSV(["data_type", "field_group", "data_point", "values", "not_found", "not_found_pct", "companies_missing", "companies_with_data"].concat(nm.countries), rows);
  }
  // Markdown with CSV blocks, ready to paste or upload to Claude. ctx: {filters, notes, page, now}.
  function claudeExport(model, vs, opts, ctx) {
    var o = {};
    for (var k in EXPORT_DEFAULTS) o[k] = EXPORT_DEFAULTS[k];
    for (var j in (opts || {})) if (opts[j] !== undefined) o[j] = opts[j];
    ctx = ctx || {};
    var meta = model.data.meta, out = [];
    out.push("# Allshares Part 1 accuracy data: export for analysis\n");
    out.push("- Run: " + meta.tracker + ", data as of " + meta.asOf + " (" + fmt(meta.rows) + " rows, " + meta.companies + " companies; countries " + (meta.countries || []).join(", ") + ")");
    out.push("- Exported: " + (ctx.now || new Date().toISOString().slice(0, 16).replace("T", " ")) + (ctx.page ? ", from the " + ctx.page + " page" : ""));
    out.push("- Filters: " + filterText(ctx.filters, model) + ". Values in view: " + fmt(vs.length) + ".");
    out.push("- Value status: found (value, with unit and period where needed), partial (value, but unit or period missing), not_found (blank), not_applicable.");
    out.push("- Score status per value: Pass >= " + meta.thresholds.pass + ", Review >= " + meta.thresholds.review + ", else Fail; a failed hard check makes it Fail (hard). failed_checks lists CHECK: reason.");
    out.push("- Source group: Annual report (incl. ESEF filings, SEC 20-F / 10-K, Companies House accounts), Remuneration report (report or policy), Other sources (registers, APIs, web pages, other documents).\n");
    if (o.notes && ctx.notes && String(ctx.notes).trim()) out.push("## My notes\n\n" + String(ctx.notes).trim() + "\n");
    var src = (o.summary || o.sources) ? sources(model, vs) : null;
    if (o.summary) {
      out.push("## Summary\n");
      kpis(model, vs).forEach(function (x) { if (x.key !== "imports") out.push("- " + x.l + ": " + x.v + " (" + x.d + ")"); });
      var t = src.totals;
      out.push("- Annual report found: " + t.annual + " of " + t.companies + " companies (" + t.annualPct + "%); remuneration report: " + t.rem + " (" + t.remPct + "%); both: " + t.both + "; neither: " + t.neither);
      out.push("");
    }
    if (o.sources) out.push(csvBlock("Companies: reports found, links and coverage",
      "One row per company (by LEI). Links are the documents values were read from. protocol_fields = fields in the protocol list for this company; fields_filled = those with a value.", sourcesCSV(src.rows)));
    if (o.coverage) {
      var fc = fieldCoverage(model, vs);
      out.push(csvBlock("Field coverage and validation by field", "Protocol field list (Company Data and Pay Data sheets). " + fc.title + ".", coverageCSV(fc)));
    }
    if (o.notFound) {
      var nm = notFoundMatrix(vs);
      out.push(csvBlock("Not found by field and country", nm.title + ". Country cells: not found / values.", notFoundCSV(nm)));
    }
    if (o.values && o.values !== "none") {
      var list = exportValues(vs, o.values), cut = o.maxValues > 0 && list.length > o.maxValues;
      out.push(csvBlock("Values (" + (o.values === "filled" ? "filled only" : o.values === "empty" ? "empty only" : "all") + ")",
        fmt(list.length) + " values" + (cut ? "; the first " + fmt(o.maxValues) + " are included" : "") + (o.compact ? "; compact: no URL or note columns, failed_checks lists check IDs, values cut at 200 characters" : "") + ".",
        valuesCSV(model, cut ? list.slice(0, o.maxValues) : list, o.compact)));
    }
    return out.join("\n");
  }

  // ---------------------------------------------------------------- KPIs, metrics, titles
  function kpis(model, vs) {
    var st = statusCounts(vs), sc = scoreCounts(vs), gs = gateStats(model, vs), n = vs.length, base = model.data.baseline;
    var last = model.hist[model.hist.length - 1];
    var foundPct = pct1(st.found, applicable(st, n)), dFound = Math.round((foundPct - base.foundPct) * 10) / 10;
    var dChecks = Math.round((gs.checksPct - base.checksPct) * 10) / 10;
    var t = model.data.meta.target;
    function sign(x) { return (x >= 0 ? "+" : "") + x.toFixed(1); }
    return [
      {key: "companies", v: companiesOf(vs), l: "Companies (distinct LEI)", cls: "", d: "of " + model.data.meta.companies + " (" + model.data.meta.companyIds + " IDs) in this run"},
      {key: "countries", v: countriesOf(vs).length, l: "Countries", cls: "", d: (model.data.meta.countries || COUNTRIES).join(", ") + " in this run"},
      {key: "values", v: fmt(n), l: "Values in view", cls: "", d: "this run: " + fmt(model.data.values.length)},
      {key: "found", v: pct(st.found, applicable(st, n)) + "%", l: "Found", cls: foundPct >= 90 ? "g" : foundPct >= 75 ? "a" : "r", d: sign(dFound) + " pts vs " + vsLabel(model)},
      {key: "partial", v: fmt(st.partial), l: "Partial", cls: "a", d: pct(st.partial, n) + "% of values"},
      {key: "notfound", v: fmt(st.not_found), l: "Not found", cls: "r", d: pct(st.not_found, n) + "% of values"},
      {key: "checks", v: gs.runs ? gs.checksPct + "%" : "–", l: "Checks passing", cls: gs.checksPct >= t ? "g" : gs.checksPct >= 80 ? "a" : "r", d: "target " + t + "% · " + (gs.runs ? sign(dChecks) + " pts vs " + vsLabel(model) : "no scored values")},
      {key: "pass", v: sc.scored ? pct(sc.P, sc.scored) + "%" : "–", l: "Values passing", cls: "", d: fmt(sc.P) + " of " + fmt(sc.scored) + " scored values"},
      {key: "hard", v: fmt(gs.hard), l: "Hard fails", cls: gs.hard ? "r" : "g", d: fmt(sc.H) + " values blocked"},
      {key: "imports", v: model.impCount, l: "Imports applied", cls: "", d: model.impCount ? "latest schema pass " + last.checks + "%" : "none yet"}
    ];
  }

  function metrics(model, vs) {
    var st = statusCounts(vs), sc = scoreCounts(vs), gs = gateStats(model, vs), n = vs.length, base = model.data.baseline;
    var asOf = model.data.meta.asOf, built = model.data.meta.built, NA = "not assigned", NS = "not set";
    function trend(cur, b) { if (cur == null) return "–"; var d = Math.round((cur - b) * 10) / 10; return d === 0 ? "level with " + vsLabel(model) : (d > 0 ? "up " : "down ") + Math.abs(d) + " pts vs " + vsLabel(model); }
    var last = model.hist[model.hist.length - 1];
    return [
      ["M01", "Checks passing", "Accuracy", "Scoring engine (gates)", "PASS / (PASS + FAIL) over gates run on values in view", pct1(gs.pass, gs.runs - gs.nr), model.data.meta.target, trend(pct1(gs.pass, gs.runs - gs.nr), base.checksPct)],
      ["M02", "Found %", "Coverage", "Run / imports", "Values with status found / values in view that apply", pct1(st.found, applicable(st, n)), NS, trend(pct1(st.found, applicable(st, n)), base.foundPct)],
      ["M03", "Values passing", "Accuracy", "Scoring engine (status)", "Values with status Pass / scored values", pct1(sc.P, sc.scored), NS, "–"],
      ["M04", "Values blocked by a hard fail", "Accuracy", "Scoring engine (status)", "Values with status Fail (hard)", sc.H, NS, "–"],
      ["M05", "Hard gate fails", "Accuracy", "Scoring engine (gates)", "Count of FAIL on hard gates", gs.hard, NS, "–"],
      ["M06", "Gates not run", "Completeness", "Scoring engine (gates)", "NOT RUN / gates applicable", pct1(gs.nr, gs.runs), NS, "–"],
      ["M07", "Empty values", "Coverage", "Run / imports", "Values with status not_found", st.not_found, NS, "–"],
      ["M08", "Companies covered", "Coverage", "Run / imports", "Distinct companies (by LEI) in view", companiesOf(vs), NS, "–"],
      ["M09", "Imports applied", "Operations", "Import page", "Imports applied this session", model.impCount, NS, "–"],
      ["M10", "Latest import schema pass", "Operations", "Import page", "Rows passing every schema check / rows in the latest file", model.impCount ? last.checks : null, NS, "–"]
    ].map(function (r) {
      return {id: r[0], metric: r[1], category: r[2], module: r[3], formula: r[4], period: "Run of " + asOf,
              value: r[5], target: r[6], trend: r[7], owner: NA, updated: built};
    });
  }

  function titles(model, vs, extra) {
    var st = statusCounts(vs), n = vs.length, pc = payComp(vs), gs = gateStats(model, vs);
    var cs = countriesOf(vs).map(function (c) { var cv = vs.filter(function (v) { return v.c === c; }); return {c: c, p: foundPct(cv)}; }).sort(function (a, b) { return b.p - a.p; });
    var ft = fieldTable(model, vs), et = emptyTables(model, vs), last = model.hist[model.hist.length - 1];
    var allPass = ft.filter(function (x) { return x.scored && x.P === x.scored; }).length;
    var worst = ft[0];
    var hist = model.hist;
    return {
      overview: "Only " + pct(st.found, applicable(st, n)) + "% of values are found; " + fmt(st.not_found) + " are empty",
      paycomp: "Company data is found " + pct(pc.sc.found, applicable(pc.sc, pc.co)) + "% of the time; pay data " + pct(pc.sp.found, applicable(pc.sp, pc.pa)) + "%",
      countries: cs.length ? "Best found rate: " + cs[0].c + " (" + cs[0].p + "%); lowest: " + cs[cs.length - 1].c + " (" + cs[cs.length - 1].p + "%)" : "No data for this selection",
      fields: ft.length ? allPass + " of " + ft.length + " fields pass on every scored value" + (worst && worst.problems ? "; most failures: " + worst.d + " (" + fmt(worst.problems) + ")" : "") : "No data for this selection",
      empty: et.fields.length ? fmt(et.n) + " values are empty; " + et.fields[0].d + " is empty for " + et.fields[0].companies + " " + (et.fields[0].companies === 1 ? "company" : "companies") : "No empty values in this selection",
      companies: "",
      failures: gs.runs ? fmt(gs.fail) + " gate fails, " + fmt(gs.hard) + " of them hard" + (gs.topHard ? "; " + gs.topHard.id + " fails most" : "") : "No scored values in this selection",
      trend: "Checks passing: " + hist[0].checks + "% at the baseline, " + last.checks + "% " + (hist.length > model.histBase ? "after " + (hist.length - model.histBase) + " import" + (hist.length - model.histBase === 1 ? "" : "s") : "in this run"),
      footer: "Source: " + model.data.meta.tracker + " (" + fmt(model.data.meta.rows) + " rows, " + fmt(model.data.meta.filled) + " filled values, " +
        model.data.meta.companies + " companies from " + model.data.meta.companyIds + " IDs" + dupText(model) + "). Data as of " + model.data.meta.asOf +
        ". Imports applied: " + model.impCount + ". Values in view: " + fmt(n) + "."
    };
  }
  function dupText(model) {
    var d = model.data.meta.duplicates || [];
    return d.length ? "; " + d.map(function (x) { return x.ids.join(" and "); }).join(", ") + " share one LEI" : "";
  }
  function attention(model, vs) {
    var gs = gateStats(model, vs);
    if (!gs.topHard) return {text: "No hard fails in this selection.", gate: null};
    return {gate: gs.topHard.id,
            text: "Most attention needed: " + gs.topHard.id + " (" + gs.topHard.name + ") with " + fmt(gs.topHard.fail) + " hard fails" +
                  (gs.topField ? ", and " + gs.topField.name + " fails " + gs.topField.rate + "% of its checks" : "") + "."};
  }

  // ---------------------------------------------------------------- import
  function parseCSV(text) {
    var rows = [], row = [], cur = "", q = false, i = 0;
    while (i < text.length) {
      var ch = text[i];
      if (q) { if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += ch; }
      else if (ch === '"') q = true;
      else if (ch === ",") { row.push(cur); cur = ""; }
      else if (ch === "\n" || ch === "\r") { if (ch === "\r" && text[i + 1] === "\n") i++; row.push(cur); rows.push(row); row = []; cur = ""; }
      else cur += ch;
      i++;
    }
    if (cur.length || row.length) { row.push(cur); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ""; }); });
  }
  function leiValid(s) {
    if (!/^[A-Z0-9]{18}[0-9]{2}$/.test(s)) return false;
    var d = "";
    for (var i = 0; i < s.length; i++) d += parseInt(s[i], 36).toString();
    var r = 0;
    for (var j = 0; j < d.length; j++) r = (r * 10 + (d.charCodeAt(j) - 48)) % 97;
    return r === 1;
  }
  function groupOf(col) {
    if (col === "role_row") return "Role row";
    if (col === "value") return "Value when found";
    if (col === "unit") return "Unit when numeric";
    if (col === "data_point") return "Data point when ambiguous";
    if (["country", "size", "grain", "status", "field_id", "source_type", "currency", "lei"].indexOf(col) >= 0) return "Allowed values";
    return "Required fields";
  }
  function validate(S, text) {
    var rows = parseCSV(String(text).replace(/^﻿/, ""));
    var errs = [], good = [], gFail = {}, badRows = {};
    if (!rows.length) return {errs: [{row: 0, col: "", msg: "File is empty"}], good: [], rows: 0, gFail: {}, badCount: 0};
    var header = rows[0].map(function (h) { return h.trim(); });
    var cols = S.columns, byName = {};
    cols.forEach(function (c) { byName[c.name] = c; });
    cols.filter(function (c) { return c.required; }).forEach(function (c) {
      if (header.indexOf(c.name) < 0) errs.push({row: 0, col: c.name, msg: "Required column missing"});
    });
    header.forEach(function (h) { if (h && !byName[h]) errs.push({row: 0, col: h, msg: "Unknown column (ignored)", warn: true}); });
    var idx = {}; header.forEach(function (h, i) { idx[h] = i; });
    var set = function (arr) { var o = {}; arr.forEach(function (x) { o[x] = 1; }); return o; };
    var numeric = set(S.numeric_field_ids), pay = set(S.pay_field_ids), ambiguous = set(S.ambiguous_field_ids);
    var countries = byName.country.allowed;
    for (var r = 1; r < rows.length; r++) {
      var row = rows[r], rowErr = [];
      var get = function (n) { var i = idx[n]; return i === undefined ? "" : (row[i] || "").trim(); };
      cols.forEach(function (c) { if (c.required && !get(c.name)) rowErr.push({row: r + 1, col: c.name, msg: "Required value empty"}); });
      // The schema spells the UK "UK", the collector ISO "GB": both are accepted, and stored as GB.
      var country = get("country"); if (country === "UK") country = "GB";
      if (country && countries.indexOf(country) < 0 && !(country === "GB" && countries.indexOf("UK") >= 0)) rowErr.push({row: r + 1, col: "country", msg: "Not an allowed country code: " + country});
      var size = get("size"); if (size && ["large", "small_mid"].indexOf(size) < 0) rowErr.push({row: r + 1, col: "size", msg: "Must be large or small_mid"});
      var grain = get("grain"); if (grain && ["company", "role"].indexOf(grain) < 0) rowErr.push({row: r + 1, col: "grain", msg: "Must be company or role"});
      if (grain === "role" && !get("role_row")) rowErr.push({row: r + 1, col: "role_row", msg: "Required when grain is role"});
      var fid = get("field_id"); if (fid && !S.field_ids[fid]) rowErr.push({row: r + 1, col: "field_id", msg: "Not a protocol field ID: " + fid});
      if (fid && ambiguous[fid] && !get("data_point")) rowErr.push({row: r + 1, col: "data_point", msg: "Required: field ID " + fid + " covers more than one field"});
      var st = get("status"); if (st && ["found", "partial", "not_found", "not_applicable"].indexOf(st) < 0) rowErr.push({row: r + 1, col: "status", msg: "Must be found, partial, not_found or not_applicable"});
      if ((st === "found" || st === "partial") && !get("value")) rowErr.push({row: r + 1, col: "value", msg: "Required when status is " + st});
      if (get("value") && numeric[fid] && !get("unit")) rowErr.push({row: r + 1, col: "unit", msg: "Unit required for numeric field " + fid});
      var sct = get("source_type"); if (sct && ["api", "filed_document", "web", "derived"].indexOf(sct) < 0) rowErr.push({row: r + 1, col: "source_type", msg: "Not an allowed source type"});
      var cur = get("currency"); if (cur && !/^[A-Z]{3}$/.test(cur)) rowErr.push({row: r + 1, col: "currency", msg: "Must be an ISO 4217 code"});
      var lei = get("lei"); if (lei && !leiValid(lei)) rowErr.push({row: r + 1, col: "lei", msg: "Not a valid ISO 17442 LEI"});
      if (rowErr.length) {
        errs = errs.concat(rowErr);
        rowErr.forEach(function (e) { var g = groupOf(e.col); (gFail[g] = gFail[g] || {})[e.row] = 1; badRows[e.row] = 1; });
        continue;
      }
      good.push({line: r + 1, c: country, o: get("company"), lei: lei, g: grain, p: pay[fid] ? 1 : 0, k: S.field_ids[fid],
                 m: pay[fid] ? "Pay and role" : "Company and ownership", f: fid, r: get("role_row"), d: get("data_point"),
                 v: get("value"), u: get("unit"), st: st});
    }
    return {errs: errs, good: good, rows: rows.length - 1, gFail: gFail, badCount: Object.keys(badRows).length};
  }

  // Upsert (SPEC section 7): company by LEI when known, else name + country; record by field ID + role row + data_point.
  function applyImport(model, recs, rows) {
    var nameIdx = {}, leiIdx = {}, byKey = {};
    recs.forEach(function (v) {
      var ck = companyKey(v), nk = v.c + "|" + lc(v.o);
      if (!nameIdx[nk]) nameIdx[nk] = ck;
      if (/^[A-Z0-9]{20}$/.test(ck)) leiIdx[ck] = ck;
      var key = ck + "|" + v.f + "|" + (v.r || "");
      (byKey[key] = byKey[key] || []).push(v);
    });
    var cnt = {added: 0, updated: 0, same: 0, ambiguous: 0, dupes: 0}, errs = [], seen = {};
    rows.forEach(function (row) {
      var nk = row.c + "|" + lc(row.o), ck = (row.lei && leiIdx[row.lei]) || nameIdx[nk];
      if (!ck) { ck = row.lei || ("I|" + row.c + "|" + row.o.trim()); nameIdx[nk] = ck; if (row.lei) leiIdx[row.lei] = ck; }
      var key = ck + "|" + row.f + "|" + (row.r || ""), sk = key + "|" + (row.d || "");
      if (seen[sk]) cnt.dupes++;
      seen[sk] = 1;
      var cands = byKey[key] || [], target = null;
      if (row.d) target = cands.filter(function (x) { return x.d === row.d; })[0] || null;
      else if (cands.length === 1) target = cands[0];
      else if (cands.length > 1) { cnt.ambiguous++; errs.push({row: row.line, col: "data_point", msg: "Several fields share field ID " + row.f + " for this company. Add data_point."}); return; }
      if (target) {
        var changed = target.v !== row.v || target.st !== row.st || (target.u || "") !== (row.u || "");
        if (changed) {
          target.v = row.v; target.u = row.u; target.st = row.st; target.s = "I";
          delete target.sc; delete target.sp; delete target.gr;
          cnt.updated++;
        } else cnt.same++;
      } else {
        var dps = model.fidToDp[row.f] || [];
        var rec = {s: "I", c: row.c, o: row.o.trim(), ck: ck, g: row.g, p: row.p, k: (model.dpMeta[row.d || dps[0]] || {}).k || row.k,
                   m: (model.dpMeta[row.d || dps[0]] || {}).m || row.m, f: row.f, r: row.r || "", d: row.d || (dps.length === 1 ? dps[0] : row.k),
                   st: row.st, v: row.v, u: row.u || "", id: ck};
        recs.push(rec);
        (byKey[key] = byKey[key] || []).push(rec);
        cnt.added++;
      }
    });
    return {counts: cnt, errs: errs};
  }
  function previewImport(model, S, text, fileName) {
    var v = validate(S, text);
    var preview = applyImport(model, model.recs.map(clone), v.good);
    return {good: v.good, errs: v.errs, rows: v.rows, preview: preview, gFail: v.gFail, badCount: v.badCount, file: fileName || "file"};
  }
  function commitImport(model, pending) {
    var res = applyImport(model, model.recs, pending.good);
    model.impCount++;
    var n = pending.rows || 0, pass = n ? Math.round((n - pending.badCount) / n * 100) : 0;
    var fileFound = pending.good.length ? pct(pending.good.filter(function (x) { return x.st === "found"; }).length, pending.good.length) : 0;
    var groups = {};
    GROUPS.forEach(function (g) { var bad = pending.gFail[g] ? Object.keys(pending.gFail[g]).length : 0; groups[g] = n ? Math.round((n - bad) / n * 100) : 100; });
    model.hist.push({label: "Import " + model.impCount + " (" + pending.file + ")", checks: pass,
                     found: foundPct(model.recs, true), fileFound: fileFound, n: n, groups: groups});
    return res;
  }

  function toCSV(header, rows, bom) {
    function q(x) { var s = x == null ? "" : String(x); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
    return (bom ? "﻿" : "") + [header].concat(rows).map(function (r) { return r.map(q).join(","); }).join("\r\n") + "\r\n";
  }
  function rangesCSV(res) {
    return toCSV(["Field", "Unit / currency"].concat(res.opts.byCountry ? ["Country"] : []).concat(["Values (n)", "Companies", "Min", res.lowLabel + "th percentile", "Median", res.highLabel + "th percentile", "Max", "Status", "Data caveat"]),
      res.rows.map(function (r) { return [r.d, r.unit].concat(res.opts.byCountry ? [r.c] : []).concat([r.n, r.companies, r.min, r.low, r.median, r.high, r.max, "Provisional: sample only, Allshares to approve", r.caveat]); }), true);
  }
  function metricsCSV(ms) {
    return toCSV(["Metric", "Category", "Source Module", "Formula or Method", "Period", "Value", "Target", "Trend", "Owner", "Last Updated", "Metric ID"],
      ms.map(function (m) { return [m.metric, m.category, m.module, m.formula, m.period, m.value, m.target, m.trend, m.owner, m.updated, m.id]; }), true);
  }

  // ---------------------------------------------------------------- delivery (SPEC 6.4)
  // Dates are YYYY-MM-DD strings; a working day is Monday to Friday when plan.working_days_only.
  function dP(s) { var a = s.split("-").map(Number); return new Date(Date.UTC(a[0], a[1] - 1, a[2])); }
  function dAdd(s, n) { var d = dP(s); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function dWork(plan, s) { var w = dP(s).getUTCDay(); return !plan.working_days_only || (w !== 0 && w !== 6); }
  function dWorkdays(plan, a, b) { var n = 0; for (var d = dAdd(a, 1); d <= b; d = dAdd(d, 1)) if (dWork(plan, d)) n++; return n; } // (a, b]
  function dShort(s) { return s ? dP(s).toLocaleDateString("en-GB", {day: "numeric", month: "short", timeZone: "UTC"}) : "–"; }
  var DISC_STATES = [["found", "Found", "#009988"], ["in progress", "In progress", "#0077BB"], ["open", "Open", "#888888"], ["not available", "Not available", "#CC3311"]];
  function discState(s) { s = lc(s); return s === "not published" ? "not available" : s === "done" ? "found" : s; }

  function delivery(model, country, today) {
    var D = model.data.delivery;
    if (!D || D.error || !D.companies) return {ok: false, error: (D && D.error) || "No delivery data in report.json. Rebuild with python -m extractor.dashboard --rerender."};
    var plan = D.plan, last = D.stages.length - 1;
    function inC(x) { return !country || x.c === country; }
    var all = D.companies, cs = all.filter(inC);
    var asOf = today || new Date().toISOString().slice(0, 10);
    if (asOf < plan.baseline_date) asOf = plan.baseline_date;

    // burn-down: always the whole backlog (the plan is for all companies)
    var doneAfter = all.filter(function (c) { return c.done && c.done > plan.baseline_date; });
    function remainingOn(d) { return plan.baseline_remaining - doneAfter.filter(function (c) { return c.done <= d; }).length; }
    function planOn(d) { return Math.max(0, plan.baseline_remaining - plan.daily_target * dWorkdays(plan, plan.baseline_date, d)); }
    var remainingNow = remainingOn(asOf), workLeft = Math.max(0, dWorkdays(plan, asOf, plan.deadline));
    var back = asOf, wd = 0;
    while (wd < 3 && back > plan.baseline_date) { if (dWork(plan, back)) wd++; back = dAdd(back, -1); }
    var pace = wd ? doneAfter.filter(function (c) { return c.done > back && c.done <= asOf; }).length / wd : 0, proj = null;
    if (pace > 0) { var left = remainingNow, d0 = asOf; while (left > 0 && d0 < dAdd(plan.deadline, 120)) { d0 = dAdd(d0, 1); if (dWork(plan, d0)) left -= pace; } proj = d0; }
    var end = [plan.deadline, proj || plan.deadline, asOf].sort().pop(), days = [];
    for (var d = plan.baseline_date; d <= end; d = dAdd(d, 1))
      days.push({d: d, short: dShort(d), plan: planOn(d), actual: d <= asOf ? remainingOn(d) : null,
                 proj: proj && d >= asOf && d <= proj ? Math.max(0, Math.round(remainingNow - pace * dWorkdays(plan, asOf, d))) : null,
                 doneThatDay: doneAfter.filter(function (c) { return c.done === d; }).length, work: dWork(plan, d)});
    var burnText = proj ? "At the last " + wd + " working days' pace (" + Math.round(pace) + "/day) the backlog clears on " + dShort(proj) + (proj > plan.deadline ? ", after the deadline." : ".")
                        : "No company has reached Done since " + dShort(plan.baseline_date) + ", so there is no pace to project yet.";
    var batchPlan = plan.batches.map(function (b) {
      var bc = all.filter(function (c) { return c.b === b.name; });
      var todo = bc.filter(function (c) { return !(c.done && c.done <= plan.baseline_date); }).length;
      var done = bc.filter(function (c) { return c.done && c.done > plan.baseline_date && c.done <= asOf; }).length;
      var len = Math.max(1, dWorkdays(plan, dAdd(b.start, -1), b.end));
      var el = asOf < b.start ? 0 : Math.min(len, dWorkdays(plan, dAdd(b.start, -1), asOf));
      var exp = Math.round(todo * el / len), status, cls;
      if (!el) { status = "Not started"; cls = ""; }
      else if (done >= todo) { status = "Complete"; cls = "good"; }
      else if (done >= exp * 0.9) { status = "On track"; cls = "good"; }
      else { status = "Behind by " + fmt(exp - done); cls = "bad"; }
      return {b: b.name, start: b.start, end: b.end, window: dShort(b.start) + " – " + dShort(b.end), todo: todo, perDay: Math.round(todo / len),
              day: el, len: len, expected: el ? exp : null, done: done, status: status, cls: cls};
    });

    // funnel: stages x (all batches, each batch); the biggest drop is the stuck stage
    var cols = [{name: "All batches", list: cs}].concat(D.batches.map(function (b) { return {name: b, list: cs.filter(function (c) { return c.b === b; })}; }));
    var funnel = cols.map(function (col) {
      var counts = D.stages.map(function (_, i) { return col.list.filter(function (c) { return c.stage >= i; }).length; });
      var stuck = -1, drop = 0;
      for (var i = 1; i < counts.length; i++) if (counts[i - 1] - counts[i] > drop) { drop = counts[i - 1] - counts[i]; stuck = i; }
      return {name: col.name, counts: counts, pcts: counts.map(function (n) { return pct(n, counts[0]); }), stuck: stuck, drop: drop};
    });

    // pass rate by batch: automated rules (values with status Pass) and the spot-check sample
    var passByBatch = D.batches.map(function (b) {
      var v = {n: 0, pass: 0, review: 0, fail: 0}, s = {n: 0, pass: 0};
      cs.forEach(function (c) { if (c.b !== b) return; v.n += c.v.n; v.pass += c.v.pass; v.review += c.v.review; v.fail += c.v.fail; if (c.spot) { s.n += c.spot.n; s.pass += c.spot.pass; } });
      if (!country && D.spotByBatch[b]) s = D.spotByBatch[b];
      return {b: b, n: v.n, pass: v.pass, review: v.review, fail: v.fail, rules: v.n ? pct1(v.pass, v.n) : null, spotN: s.n, spotPass: s.pass, spot: s.n ? pct1(s.pass, s.n) : null};
    });
    var tv = cs.reduce(function (a, c) { a.n += c.v.n; a.pass += c.v.pass; return a; }, {n: 0, pass: 0});

    // failure patterns: companies affected per reason, and the work list
    var cats = {}, failRows = [];
    cs.forEach(function (c) { Object.keys(c.fc).forEach(function (k) {
      cats[k] = cats[k] || {cat: k, companies: 0, values: 0}; cats[k].companies++; cats[k].values += c.fc[k];
      failRows.push({id: c.id, o: c.o, c: c.c, b: c.b, cat: k, n: c.fc[k], ex: (c.fx || {})[k] || ""});
    }); });
    var failures = Object.keys(cats).map(function (k) { return cats[k]; }).sort(function (a, b) { return b.companies - a.companies || a.cat.localeCompare(b.cat); });
    failRows.sort(function (a, b) { return b.n - a.n || a.o.localeCompare(b.o); });

    // discovery queue and exceptions
    var drows = D.discovery.filter(inC), dcount = {}, byNeed = {};
    drows.forEach(function (x) { var s = discState(x.status); dcount[s] = (dcount[s] || 0) + 1; byNeed[x.need] = (byNeed[x.need] || 0) + 1; });
    var resolved = (dcount.found || 0) + (dcount["not available"] || 0);
    var erows = D.exceptions.filter(inC), ecat = {};
    erows.forEach(function (e) { var x = ecat[e.cat] = ecat[e.cat] || {cat: e.cat, n: 0, yes: 0}; x.n++; if (e.accepted === "yes") x.yes++; });
    var excYes = erows.filter(function (e) { return e.accepted === "yes"; }).length;

    // pipeline health
    var countryOf = {}; all.forEach(function (c) { countryOf[c.id] = c.c; });
    var runs = D.runs.filter(function (r) { return !country || countryOf[r.id] === country; });
    var rdays = {}, used = 0;
    runs.forEach(function (r) {
      used += r.credits; if (!r.date) return;
      var x = rdays[r.date] = rdays[r.date] || {d: r.date, short: dShort(r.date), ok: 0, failed: 0, credits: 0};
      x[r.status === "failed" ? "failed" : "ok"]++; x.credits += r.credits;
    });
    var hd = Object.keys(rdays).sort(), hdays = [];
    if (hd.length) for (var x = hd[0]; x <= hd[hd.length - 1]; x = dAdd(x, 1)) hdays.push(rdays[x] || {d: x, short: dShort(x), ok: 0, failed: 0, credits: 0});
    var failedRuns = runs.filter(function (r) { return r.status === "failed"; });
    var perRun = runs.length ? used / runs.length : 0, need = Math.round(perRun * remainingNow);
    var fc = D.firecrawl || {}, balance = null;
    if (fc.credit_balance != null) balance = fc.credit_balance - D.runs.filter(function (r) { return r.date && (!fc.balance_as_of || r.date > fc.balance_as_of); }).reduce(function (a, r) { return a + r.credits; }, 0);
    var nowIso = new Date().toISOString();
    var sched = (D.scheduled || []).map(function (s) {
      var missed = !!(s.scheduled_for && s.scheduled_for < nowIso && !s.started_at && !/done|ok|success|running/i.test(s.status || ""));
      return {run: s.run_id, b: s.batch, at: s.scheduled_for, started: s.started_at, finished: s.finished_at, status: missed ? "Missed" : (s.status || "scheduled"),
              bad: missed || /fail|error/i.test(s.status || ""), companies: s.companies, credits: s.credits_used, note: s.note};
    });

    var stuckAll = funnel[0].stuck > 0 ? D.stages[funnel[0].stuck] : "";
    var behind = remainingNow - planOn(asOf);
    return {
      ok: true, plan: plan, stages: D.stages, batches: D.batches, asOf: asOf, built: D.built, fy: D.fiscalYear, country: country || "",
      deadline: dShort(plan.deadline), acceptance: dShort(plan.exceptions_acceptance_date), baselineDate: dShort(plan.baseline_date),
      kpis: {companies: cs.length, remaining: remainingNow, planNow: planOn(asOf), behind: behind, done: cs.filter(function (c) { return c.stage === last; }).length,
             extracted: cs.filter(function (c) { return c.stage >= 2; }).length, workLeft: workLeft, needed: workLeft ? Math.round(remainingNow / workLeft) : null,
             passPct: tv.n ? pct1(tv.pass, tv.n) : null, passN: tv.pass, valuesN: tv.n, discOpen: drows.length - resolved, discN: drows.length,
             exc: erows.length, excYes: excYes},
      funnel: funnel, passByBatch: passByBatch, failures: failures, failRows: failRows,
      burn: {days: days, proj: proj, projShort: dShort(proj), pace: pace, wd: wd, text: burnText, remainingNow: remainingNow}, batchPlan: batchPlan,
      discovery: {rows: drows, counts: DISC_STATES.map(function (s) { return {key: s[0], label: s[1], color: s[2], n: dcount[s[0]] || 0}; }),
                  byNeed: Object.keys(byNeed).map(function (k) { return {need: k, n: byNeed[k]}; }), resolved: resolved,
                  owners: D.discovery.some(function (x) { return x.owner; })},
      exceptions: {rows: erows, byCat: Object.keys(ecat).map(function (k) { return ecat[k]; }).sort(function (a, b) { return b.n - a.n; })},
      health: {runs: runs.length, failed: failedRuns.length, failedPct: runs.length ? pct(failedRuns.length, runs.length) : null, failedRuns: failedRuns,
               used: Math.round(used), perRun: Math.round(perRun * 10) / 10, need: need, balance: balance, short: balance != null && balance < need,
               days: hdays, scheduled: sched, missed: sched.filter(function (s) { return s.status === "Missed"; }).length,
               span: hd.length ? dShort(hd[0]) + " – " + dShort(hd[hd.length - 1]) : ""},
      titles: {
        standup: (stuckAll ? fmt(funnel[0].drop) + " of " + fmt(funnel[0].counts[0]) + " required companies are waiting at " + stuckAll : "Status of " + fmt(funnel[0].counts[0]) + " required companies") + (country ? " (" + country + ")" : ""),
        throughput: fmt(remainingNow) + " of " + fmt(plan.baseline_remaining) + " companies remaining, " + (behind > 0 ? fmt(behind) + " behind plan" : "on or ahead of plan") + "; due " + dShort(plan.deadline),
        discovery: fmt(drows.length - resolved) + " of " + fmt(drows.length) + " companies still need a document or data source",
        exceptions: fmt(erows.length) + " exceptions for Allshares to accept on " + dShort(plan.exceptions_acceptance_date) + " (" + fmt(excYes) + " accepted)",
        health: fmt(failedRuns.length) + " of " + fmt(runs.length) + " company runs failed; " + fmt(Math.round(used)) + " Firecrawl credits used"
      }
    };
  }
  function deliveryFailCSV(rows) {
    return toCSV(["Company", "Company ID", "Country", "Batch", "Reason", "Count", "Example"], rows.map(function (r) { return [r.o, r.id, r.c, r.b, r.cat, r.n, r.ex]; }), true);
  }
  function exceptionsCSV(rows) {
    return toCSV(["Company", "Company ID", "Country", "Batch", "Category", "Reason", "Source", "Accepted by Allshares", "Note"],
      rows.map(function (e) { return [e.o, e.id, e.c, e.b, e.cat, e.reason, e.source, e.accepted, e.note]; }), true);
  }
  function discoveryCSV(rows) {
    return toCSV(["Company", "Company ID", "Country", "Batch", "Need", "Next step", "Owner", "Status", "Updated", "Note"],
      rows.map(function (x) { return [x.o, x.id, x.c, x.b, x.need, x.next, x.owner, discState(x.status), x.updated, x.note]; }), true);
  }

  return {
    PAL: PAL, VSTAT: VSTAT, SSTAT: SSTAT, SNAME: SNAME, COUNTRIES: COUNTRIES, GROUPS: GROUPS, RANGE_FIELDS: RANGE_FIELDS,
    EMPTY_FILTERS: EMPTY_FILTERS, RANGE_DEFAULTS: RANGE_DEFAULTS, FILL_OPTIONS: FILL_OPTIONS, SRC_GROUPS: SRC_GROUPS, EXPORT_DEFAULTS: EXPORT_DEFAULTS,
    sourceGroup: sourceGroup, sources: sources, notFoundMatrix: notFoundMatrix, notFoundValues: notFoundValues,
    fieldList: fieldList, fieldCoverage: fieldCoverage, claudeExport: claudeExport, valuesCSV: valuesCSV, exportValues: exportValues, filterText: filterText,
    SEVERITIES: SEVERITIES, REQ_CLASSES: REQ_CLASSES, reqClass: reqClass, dataPage: dataPage, dataPageCSV: dataPageCSV,
    sourcesCSV: sourcesCSV, coverageCSV: coverageCSV, notFoundCSV: notFoundCSV, srcGroupName: srcGroupName,
    pct: pct, pct1: pct1, fmt: fmt, num: num, companyKey: companyKey,
    createModel: createModel, resetModel: resetModel, filterValues: filterValues, filterOptions: filterOptions, anyFilter: anyFilter,
    statusCounts: statusCounts, scoreCounts: scoreCounts, companiesOf: companiesOf, countriesOf: countriesOf, gates: gates,
    overview: overview, payComp: payComp, countriesPage: countriesPage, gateStats: gateStats,
    fieldTable: fieldTable, fieldDetail: fieldDetail, emptyTables: emptyTables, companyTable: companyTable, companyDetail: companyDetail,
    FAMILIES: FAMILIES, validationSteps: validationSteps, stepDetail: stepDetail, stepFieldValues: stepFieldValues,
    percentile: percentile, ranges: ranges, rangeOptions: rangeOptions,
    kpis: kpis, metrics: metrics, titles: titles, attention: attention,
    parseCSV: parseCSV, leiValid: leiValid, validate: validate, applyImport: applyImport, previewImport: previewImport, commitImport: commitImport,
    toCSV: toCSV, rangesCSV: rangesCSV, metricsCSV: metricsCSV,
    DISC_STATES: DISC_STATES, discState: discState, delivery: delivery, deliveryFailCSV: deliveryFailCSV,
    exceptionsCSV: exceptionsCSV, discoveryCSV: discoveryCSV
  };
});
