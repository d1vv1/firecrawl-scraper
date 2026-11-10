/* Allshares dashboard UI helpers shared by the Angular app and the single-file HTML (SPEC 6.1):
   - sortable(root): every table under root sorts by a click on its column header (again to reverse).
   - notes: the notes bar, kept in this browser (localStorage) and added to the export for Claude.
   DOM only; no data logic (that is report-core.js). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ReportUI = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // ---------------------------------------------------------------- sortable tables
  // A header with data-sort, or a table with class "nosort", keeps its own sorting. The sort is kept by
  // table (its section id and header texts), so it survives a re-render of the rows or of the table.
  // Rows of class "group" split a table into blocks sorted one by one; a single-cell "no data" row stays put.
  var state = {};
  function headRow(t) { return t.tHead && t.tHead.rows.length ? t.tHead.rows[t.tHead.rows.length - 1] : null; }
  function tableKey(t) {
    var sec = t.closest ? t.closest("[id]") : null, hr = headRow(t);
    var heads = [].map.call(hr ? hr.cells : [], function (c) { return c.getAttribute("data-label") || c.textContent.trim(); });
    return (sec ? sec.id : "") + "|" + heads.join("|");
  }
  function cellValue(td) {
    if (!td) return null;
    var a = td.getAttribute("data-v"), t = (a != null ? a : td.textContent).trim();
    if (t === "" || t === "–" || t === "-") return null;
    var n = t.replace(/[,\s %]/g, "").replace(/−/g, "-");
    if (/^-?\d+(\.\d+)?$/.test(n)) return parseFloat(n);
    var f = /^(-?\d+(\.\d+)?)\s*(of|\/)/.exec(t.replace(/,/g, ""));   // "12 of 40", "3/10"
    if (f) return parseFloat(f[1]);
    return t.toLowerCase();
  }
  function compare(a, b, dir) {
    if (a === b) return 0;
    if (a === null) return 1;                 // blanks last either way
    if (b === null) return -1;
    if (typeof a === "number" && typeof b === "number") return (a - b) * dir;
    if (typeof a === "number") return -1;
    if (typeof b === "number") return 1;
    return a.localeCompare(b) * dir;
  }
  function isStatic(r) { return r.classList.contains("group") || (r.cells.length === 1 && r.cells[0].colSpan > 1) || r.classList.contains("nosort"); }
  function sortTable(t, st) {
    var tb = t.tBodies[0];
    if (!tb || !t.tHead) return;
    var rows = [].slice.call(tb.rows);
    if (rows.length < 2) return;
    var blocks = [[]];
    rows.forEach(function (r) { if (r.classList.contains("group")) blocks.push([r]); else blocks[blocks.length - 1].push(r); });
    var order = [];
    blocks.forEach(function (b) {
      var fixed = b.filter(isStatic), movable = b.filter(function (r) { return !isStatic(r); });
      var keyed = movable.map(function (r, i) { return {r: r, i: i, v: cellValue(r.cells[st.col])}; });
      keyed.sort(function (x, y) { return compare(x.v, y.v, st.dir) || x.i - y.i; });
      b.filter(function (r) { return r.classList.contains("group"); }).forEach(function (r) { order.push(r); });
      keyed.forEach(function (k) { order.push(k.r); });
      fixed.filter(function (r) { return !r.classList.contains("group"); }).forEach(function (r) { order.push(r); });
    });
    if (order.every(function (r, i) { return r === rows[i]; })) return;
    var after = rows[rows.length - 1].nextSibling;   // keep rows before any framework anchor node
    order.forEach(function (r) { tb.insertBefore(r, after); });
  }
  function markHeads(t, st) {
    var hr = headRow(t);
    if (!hr) return;
    [].forEach.call(hr.cells, function (c, i) {
      if (c.hasAttribute("data-sort")) return;
      if (st && i === st.col) c.setAttribute("aria-sort", st.dir > 0 ? "ascending" : "descending"); else c.removeAttribute("aria-sort");
    });
  }
  function applyAll(rootEl) {
    [].forEach.call(rootEl.querySelectorAll("table"), function (t) {
      if (t.classList.contains("nosort") || !headRow(t)) return;
      var st = state[tableKey(t)];
      markHeads(t, st);
      if (st) sortTable(t, st);
    });
  }
  function sortable(rootEl) {
    if (!rootEl || !rootEl.addEventListener || rootEl.__sortable) return;
    rootEl.__sortable = true;
    function onHead(e) {
      var th = e.target.closest ? e.target.closest("thead th") : null;
      if (!th || th.hasAttribute("data-sort") || !th.textContent.trim()) return;
      var t = th.closest("table");
      if (!t || t.classList.contains("nosort") || !rootEl.contains(t)) return;
      var row = th.parentNode, col = [].indexOf.call(row.cells, th), key = tableKey(t), st = state[key];
      if (st && st.col === col) st.dir = -st.dir;
      else {
        var first = null;
        [].some.call(t.tBodies[0] ? t.tBodies[0].rows : [], function (r) { if (isStatic(r)) return false; first = cellValue(r.cells[col]); return first !== null; });
        st = state[key] = {col: col, dir: typeof first === "number" ? -1 : 1};   // numbers: largest first
      }
      markHeads(t, st);
      sortTable(t, st);
    }
    rootEl.addEventListener("click", onHead);
    rootEl.addEventListener("keydown", function (e) { if (e.key === "Enter" && e.target.tagName === "TH") onHead(e); });
    // Re-apply after any re-render (new rows, a new table, an Angular update).
    var pending = false;
    if (typeof MutationObserver === "function") {
      new MutationObserver(function () {
        if (pending) return;
        pending = true;
        setTimeout(function () { pending = false; applyAll(rootEl); }, 0);
      }).observe(rootEl, {childList: true, subtree: true});
    }
    applyAll(rootEl);
  }

  // ---------------------------------------------------------------- grouped navigation menus
  // .navgrp > .navbtn + .navmenu: a click on the button opens its menu (and closes the others); choosing
  // an item, clicking elsewhere or Escape closes it; arrow keys move between items.
  function navMenus(rootEl) {
    if (!rootEl || !rootEl.addEventListener || rootEl.__navMenus) return;
    rootEl.__navMenus = true;
    function closeAll(except) {
      [].forEach.call(rootEl.querySelectorAll(".navgrp"), function (g) {
        if (g === except) return;
        var m = g.querySelector(".navmenu"), b = g.querySelector(".navbtn");
        if (m) m.hidden = true;
        if (b) b.setAttribute("aria-expanded", "false");
      });
    }
    function items(g) { return [].slice.call(g.querySelectorAll(".navmenu > *")); }
    rootEl.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest(".navbtn") : null;
      if (btn) {
        var g = btn.closest(".navgrp"), m = g.querySelector(".navmenu"), open = m.hidden;
        closeAll(g);
        m.hidden = !open; btn.setAttribute("aria-expanded", String(open));
        return;
      }
      if (e.target.closest && e.target.closest(".navmenu")) closeAll();
    });
    rootEl.addEventListener("keydown", function (e) {
      var g = e.target.closest ? e.target.closest(".navgrp") : null;
      if (!g) return;
      var m = g.querySelector(".navmenu"), list = items(g), i = list.indexOf(e.target);
      if (e.key === "Escape") { closeAll(); g.querySelector(".navbtn").focus(); }
      else if (e.key === "ArrowDown") {
        e.preventDefault();
        if (m.hidden) { closeAll(g); m.hidden = false; g.querySelector(".navbtn").setAttribute("aria-expanded", "true"); }
        (list[i + 1] || list[0]).focus();
      } else if (e.key === "ArrowUp" && i >= 0) { e.preventDefault(); (list[i - 1] || list[list.length - 1]).focus(); }
    });
    document.addEventListener("click", function (e) { if (!rootEl.contains(e.target)) closeAll(); });
  }

  // ---------------------------------------------------------------- notes bar
  var NOTES_KEY = "allshares-dashboard-notes";
  function getNotes() { try { return localStorage.getItem(NOTES_KEY) || ""; } catch (e) { return ""; } }
  function setNotes(t) { try { localStorage.setItem(NOTES_KEY, t); return true; } catch (e) { return false; } }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]; }); }
  function saveFile(text, name) {
    var url = URL.createObjectURL(new Blob([text], {type: "text/plain;charset=utf-8"}));
    var a = document.createElement("a"); a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return fallbackCopy(text); });
    return Promise.resolve(fallbackCopy(text));
  }
  function fallbackCopy(text) {
    var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    ta.remove(); return ok;
  }
  // context(): a one-line description of the current page and filters, added by "Add current view".
  function mountNotes(opts) {
    opts = opts || {};
    if (typeof document === "undefined" || !document.body || document.getElementById("notesBar")) return null;
    var wrap = document.createElement("div");
    wrap.innerHTML =
      '<button type="button" class="notes-tab" id="notesTab" aria-controls="notesBar" aria-expanded="false">Notes</button>' +
      '<aside class="notes-bar" id="notesBar" aria-label="My notes" hidden>' +
      '<div class="notes-head"><b>My notes</b><span class="notes-saved" id="notesSaved"></span><button type="button" class="linkbtn" id="notesClose" aria-label="Close notes">Close ✕</button></div>' +
      '<textarea id="notesText" spellcheck="true" placeholder="Write notes as you review. They are kept in this browser and included in the export for Claude."></textarea>' +
      '<div class="notes-actions"><button type="button" class="btn" id="notesCtx">Add current view</button><button type="button" class="btn" id="notesCopy">Copy</button>' +
      '<button type="button" class="btn" id="notesSave">Download .txt</button><button type="button" class="linkbtn" id="notesClear">Clear</button></div>' +
      '<div class="notes-hint">Saved in this browser only (not shared, not in the report file).</div></aside>';
    while (wrap.firstChild) document.body.appendChild(wrap.firstChild);
    var bar = document.getElementById("notesBar"), tab = document.getElementById("notesTab"), ta = document.getElementById("notesText"), saved = document.getElementById("notesSaved");
    ta.value = getNotes();
    function status(t) { saved.textContent = t; }
    function count() { tab.textContent = ta.value.trim() ? "Notes •" : "Notes"; }
    function open(on) { bar.hidden = !on; tab.setAttribute("aria-expanded", String(on)); document.body.classList.toggle("notes-open", on); if (on) ta.focus(); }
    var timer = null;
    ta.addEventListener("input", function () {
      clearTimeout(timer); status("…"); count();
      timer = setTimeout(function () { status(setNotes(ta.value) ? "Saved" : "Not saved: browser storage is off"); if (opts.onChange) opts.onChange(ta.value); }, 400);
    });
    tab.addEventListener("click", function () { open(bar.hidden); });
    document.getElementById("notesClose").addEventListener("click", function () { open(false); });
    document.getElementById("notesCtx").addEventListener("click", function () {
      var line = "[" + new Date().toISOString().slice(0, 16).replace("T", " ") + (opts.context ? " · " + opts.context() : "") + "]\n";
      ta.value = (ta.value && !/\n$/.test(ta.value) ? ta.value + "\n\n" : ta.value) + line;
      ta.dispatchEvent(new Event("input")); ta.focus();
    });
    document.getElementById("notesCopy").addEventListener("click", function () { copyText(ta.value).then(function (ok) { status(ok ? "Copied" : "Copy failed"); }); });
    document.getElementById("notesSave").addEventListener("click", function () { saveFile(ta.value, "allshares_notes.txt"); });
    document.getElementById("notesClear").addEventListener("click", function () {
      if (ta.value && !confirm("Clear all notes? This cannot be undone.")) return;
      ta.value = ""; ta.dispatchEvent(new Event("input"));
    });
    count();
    return {open: open, get: function () { return ta.value; }};
  }

  return {sortable: sortable, navMenus: navMenus, cellValue: cellValue, getNotes: getNotes, setNotes: setNotes, mountNotes: mountNotes,
          copyText: copyText, saveFile: saveFile, esc: esc};
});
