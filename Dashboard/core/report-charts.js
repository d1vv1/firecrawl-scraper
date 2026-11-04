/* SVG chart builders shared by the Angular app and the single-file HTML (DESIGN.md section 5).
   Each returns an SVG string. Fixed height about 230px; colours come from the caller (max 5 per chart). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ReportCharts = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  var GRID = "#e1dfdd", FAINT = "#8a8886", SOFT = "#605e5c", INK = "#252423";

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function fmt(n) { return Number(n).toLocaleString("en-GB"); }
  function empty(w, h) { return '<svg viewBox="0 0 ' + w + ' ' + h + '" role="img"><text x="' + w / 2 + '" y="' + h / 2 + '" text-anchor="middle" fill="' + FAINT + '" font-size="12">No data for this selection</text></svg>'; }
  function axis(s, W, pad, base, max, suffix) {
    for (var t = 0; t <= 4; t++) {
      var y = base - (base - 20) * t / 4;
      s += '<line x1="' + pad + '" x2="' + (W - 6) + '" y1="' + y + '" y2="' + y + '" stroke="' + GRID + '"/><text x="' + (pad - 6) + '" y="' + (y + 4) + '" text-anchor="end" font-size="10" fill="' + FAINT + '">' + fmt(Math.round(max * t / 4)) + (suffix || "") + '</text>';
    }
    return s;
  }

  function bars(items, o) {
    o = o || {};
    var W = 520, H = 230, pad = 40, base = H - 34;
    if (!items.length) return empty(W, H);
    var max = o.max || Math.max(1, Math.max.apply(null, items.map(function (i) { return i.value; })));
    var bw = (W - pad - 10) / items.length, suf = o.suffix || "";
    var s = axis('<svg viewBox="0 0 ' + W + ' ' + H + '" role="img">', W, pad, base, max, suf);
    items.forEach(function (it, i) {
      var h = (base - 20) * it.value / max, x = pad + i * bw + bw * 0.18, w = bw * 0.64;
      s += '<rect x="' + x + '" y="' + (base - h) + '" width="' + w + '" height="' + h + '" fill="' + (it.color || "#0077BB") + '"><title>' + esc(it.label) + ': ' + fmt(it.value) + suf + '</title></rect>';
      s += '<text x="' + (x + w / 2) + '" y="' + (base - h - 4) + '" text-anchor="middle" font-size="10" fill="' + INK + '">' + fmt(it.value) + suf + '</text>';
      s += '<text x="' + (x + w / 2) + '" y="' + (base + 14) + '" text-anchor="middle" font-size="11" fill="' + SOFT + '">' + esc(it.label) + '</text>';
    });
    return s + '</svg>';
  }

  function hbars(items, o) {
    o = o || {};
    var W = 520, rowH = 22, lab = 230;
    if (!items.length) return empty(W, 230);
    var H = Math.max(60, items.length * rowH + 12);
    var max = o.max || Math.max(1, Math.max.apply(null, items.map(function (i) { return i.value; })));
    var suf = o.suffix || "";
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" style="height:' + H + 'px">';
    items.forEach(function (it, i) {
      var y = 6 + i * rowH, w = (W - lab - 70) * it.value / max;
      s += '<text x="' + (lab - 6) + '" y="' + (y + 14) + '" text-anchor="end" font-size="11" fill="' + INK + '">' + esc(String(it.label).slice(0, 38)) + '</text>';
      s += '<rect x="' + lab + '" y="' + (y + 3) + '" width="' + Math.max(w, 1) + '" height="' + (rowH - 8) + '" fill="' + (it.color || "#0077BB") + '"><title>' + esc(it.label) + ': ' + fmt(it.value) + suf + '</title></rect>';
      s += '<text x="' + (lab + Math.max(w, 1) + 5) + '" y="' + (y + 14) + '" font-size="11" fill="' + SOFT + '">' + fmt(it.value) + suf + (it.sub ? ' (' + esc(it.sub) + ')' : '') + '</text>';
    });
    return s + '</svg>';
  }

  function stacked(cats, series) {
    var W = 520, H = 230, pad = 40, base = H - 34;
    if (!cats.length) return empty(W, H);
    var totals = cats.map(function (_, i) { return series.reduce(function (a, se) { return a + se.values[i]; }, 0); });
    var max = Math.max(1, Math.max.apply(null, totals)), bw = (W - pad - 10) / cats.length;
    var s = axis('<svg viewBox="0 0 ' + W + ' ' + H + '" role="img">', W, pad, base, max);
    cats.forEach(function (c, i) {
      var acc = 0, x = pad + i * bw + bw * 0.18, w = bw * 0.64;
      series.forEach(function (se) {
        var v = se.values[i], h = (base - 20) * v / max;
        if (h > 0) s += '<rect x="' + x + '" y="' + (base - acc - h) + '" width="' + w + '" height="' + h + '" fill="' + se.color + '"><title>' + esc(c) + ' · ' + esc(se.name) + ': ' + fmt(v) + '</title></rect>';
        acc += h;
      });
      s += '<text x="' + (x + w / 2) + '" y="' + (base + 14) + '" text-anchor="middle" font-size="11" fill="' + SOFT + '">' + esc(c) + '</text>';
    });
    return s + '</svg>';
  }

  // Horizontal 100% stacked bars (one row per item; series share of the row total).
  function stackedH(rows, series) {
    var W = 520, rowH = 22, lab = 170;
    if (!rows.length) return empty(W, 230);
    var H = rows.length * rowH + 12, s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" style="height:' + H + 'px">';
    rows.forEach(function (r, i) {
      var y = 6 + i * rowH, tot = series.reduce(function (a, se) { return a + (r[se.key] || 0); }, 0), x = lab;
      s += '<text x="' + (lab - 6) + '" y="' + (y + 14) + '" text-anchor="end" font-size="11" fill="' + INK + '">' + esc(r.label) + '</text>';
      series.forEach(function (se) {
        var v = r[se.key] || 0, w = tot ? (W - lab - 40) * v / tot : 0;
        if (w > 0) s += '<rect x="' + x + '" y="' + (y + 3) + '" width="' + w + '" height="' + (rowH - 8) + '" fill="' + se.color + '"><title>' + esc(r.label) + ' · ' + esc(se.name) + ': ' + fmt(v) + ' (' + Math.round(v / tot * 100) + '%)</title></rect>';
        x += w;
      });
      s += '<text x="' + (x + 4) + '" y="' + (y + 14) + '" font-size="10" fill="' + SOFT + '">' + fmt(tot) + '</text>';
    });
    return s + '</svg>';
  }

  function pie(items) {
    var total = items.reduce(function (a, i) { return a + i.value; }, 0);
    if (!total) return empty(320, 230);
    var s = '<svg viewBox="0 0 340 230" role="img">', cx = 110, cy = 115, r = 95, a0 = -Math.PI / 2;
    items.forEach(function (it) {
      if (!it.value) return;
      var frac = it.value / total, a1 = a0 + frac * 2 * Math.PI;
      if (frac >= 0.9999) { s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + it.color + '"><title>' + esc(it.label) + ': ' + fmt(it.value) + '</title></circle>'; a0 = a1; return; }
      var x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0), x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
      s += '<path d="M' + cx + ',' + cy + ' L' + x0 + ',' + y0 + ' A' + r + ',' + r + ' 0 ' + (frac > 0.5 ? 1 : 0) + ',1 ' + x1 + ',' + y1 + ' Z" fill="' + it.color + '"><title>' + esc(it.label) + ': ' + fmt(it.value) + ' (' + Math.round(frac * 100) + '%)</title></path>';
      a0 = a1;
    });
    var ly = 30;
    items.forEach(function (it) {
      s += '<rect x="228" y="' + ly + '" width="10" height="10" fill="' + it.color + '"/><text x="244" y="' + (ly + 9) + '" font-size="11" fill="' + INK + '">' + esc(it.label) + ' ' + Math.round(it.value / total * 100) + '%</text>';
      ly += 20;
    });
    return s + '</svg>';
  }

  function line(points, target) {
    var W = 520, H = 230, pl = 40, pb = 30, pt = 10, pr = 14;
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img">';
    [0, 25, 50, 75, 100].forEach(function (t) {
      var y = pt + (H - pt - pb) * (1 - t / 100);
      s += '<line x1="' + pl + '" x2="' + (W - pr) + '" y1="' + y + '" y2="' + y + '" stroke="' + GRID + '"/><text x="' + (pl - 6) + '" y="' + (y + 4) + '" text-anchor="end" font-size="10" fill="' + FAINT + '">' + t + '%</text>';
    });
    if (target != null) {
      var ty = pt + (H - pt - pb) * (1 - target / 100);
      s += '<line x1="' + pl + '" x2="' + (W - pr) + '" y1="' + ty + '" y2="' + ty + '" stroke="#888888" stroke-dasharray="5 4"><title>Target ' + target + '%</title></line><text x="' + (W - pr) + '" y="' + (ty - 4) + '" text-anchor="end" font-size="10" fill="#888888">target ' + target + '%</text>';
    }
    var n = points.length, step = n > 1 ? (W - pl - pr) / (n - 1) : 0;
    function xy(i, val) { return [pl + (n > 1 ? i * step : (W - pl - pr) / 2), pt + (H - pt - pb) * (1 - val / 100)]; }
    [["checks", "#0077BB"], ["found", "#009988"]].forEach(function (ser) {
      var pts = points.map(function (p, i) { return xy(i, p[ser[0]]); });
      s += '<polyline fill="none" stroke="' + ser[1] + '" stroke-width="2.4" points="' + pts.map(function (p) { return p[0] + "," + p[1]; }).join(" ") + '"/>';
      pts.forEach(function (p, i) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="3.5" fill="' + ser[1] + '"><title>' + esc(points[i].label) + ': ' + points[i][ser[0]] + '%</title></circle>'; });
    });
    points.forEach(function (p, i) { s += '<text x="' + xy(i, 0)[0] + '" y="' + (H - 10) + '" text-anchor="middle" font-size="10" fill="' + SOFT + '">' + esc(p.short) + '</text>'; });
    return s + '</svg>';
  }

  function legend(items) {
    return items.map(function (i) { return '<span><i style="background:' + i.color + '"></i>' + esc(i.label) + '</span>'; }).join("");
  }

  return {esc: esc, bars: bars, hbars: hbars, stacked: stacked, stackedH: stackedH, pie: pie, line: line, legend: legend};
});
