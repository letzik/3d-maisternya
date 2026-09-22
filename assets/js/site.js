/* 3D-Майстерня / 3D Workshop — small progressive enhancements. Everything works without JS
   except search, theme toggle and the local progress tracker. No tracking, no external requests. */
(function () {
  "use strict";
  var d = document, body = d.body;
  var root = body.getAttribute("data-root") || "";
  var lang = body.getAttribute("data-lang") || "uk";

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  function each(sel, fn, ctx) { [].forEach.call((ctx || d).querySelectorAll(sel), fn); }

  /* language memory (used by the root gateway page and the exercises) */
  store("3dm-lang", lang);

  /* theme */
  var THEME_COLORS = { dark: "#161826", light: "#f5f6fb" };
  var themeBtn = d.querySelector("[data-theme-toggle]");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = d.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    d.documentElement.setAttribute("data-theme", next);
    store("3dm-theme", next);
    var meta = d.getElementById("theme-color-meta");
    if (meta) meta.setAttribute("content", THEME_COLORS[next]);
  });

  /* mobile menu + blocks dropdown */
  var navBtn = d.querySelector("[data-nav-toggle]");
  if (navBtn) navBtn.addEventListener("click", function () {
    var open = body.classList.toggle("nav-open");
    navBtn.setAttribute("aria-expanded", String(open));
  });
  var dd = d.querySelector(".dd"), ddBtn = dd && dd.querySelector(".dd__btn");
  function closeDd() { if (dd) { dd.classList.remove("open"); ddBtn.setAttribute("aria-expanded", "false"); } }
  if (ddBtn) ddBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = dd.classList.toggle("open");
    ddBtn.setAttribute("aria-expanded", String(open));
  });
  d.addEventListener("click", function (e) { if (dd && !dd.contains(e.target)) closeDd(); });

  /* table of contents: open on wide screens, highlight the current section */
  var toc = d.querySelector("[data-toc]");
  if (toc) {
    var mq = window.matchMedia("(min-width: 1181px)");
    var sync = function () { toc.open = mq.matches; };
    sync();
    if (mq.addEventListener) mq.addEventListener("change", sync);
    var links = [].slice.call(toc.querySelectorAll("a"));
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (l) { l.classList.remove("is-active"); });
          if (byId[en.target.id]) byId[en.target.id].classList.add("is-active");
        });
      }, { rootMargin: "-80px 0px -68% 0px" });
      links.forEach(function (a) { var h = d.getElementById(a.getAttribute("href").slice(1)); if (h) io.observe(h); });
    }
  }

  /* copy buttons on code blocks */
  d.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    var code = b.parentNode.querySelector("pre");
    var done = function () {
      var old = b.textContent;
      b.textContent = b.getAttribute("data-copied") || "✓";
      setTimeout(function () { b.textContent = old; }, 1600);
    };
    if (navigator.clipboard && code) navigator.clipboard.writeText(code.innerText).then(done, function () {});
  });

  /* local progress: which block checkpoints are done (stays in this browser only) */
  var KEY = "3dm-done";
  function getDone() { try { return JSON.parse(store(KEY) || "[]"); } catch (e) { return []; } }
  function paint() {
    var done = getDone();
    each("[data-check]", function (el) { el.classList.toggle("is-done", done.indexOf(+el.getAttribute("data-check")) >= 0); });
    each(".bcard", function (c) { c.classList.toggle("is-done", done.indexOf(+c.getAttribute("data-block")) >= 0); });
    each("[data-progress]", function (p) {
      var total = +p.getAttribute("data-total");
      var n = done.filter(function (x) { return x >= 1 && x <= total; }).length;
      var bar = p.querySelector(".progress__bar span");
      if (bar) bar.style.width = (n / total * 100) + "%";
      var t = p.querySelector(".progress__n");
      if (t) t.textContent = (p.getAttribute("data-text") || "").replace("{n}", n).replace("{total}", total);
    });
    each("[data-done]", function (b) {
      var on = done.indexOf(+b.getAttribute("data-done")) >= 0;
      b.classList.toggle("is-done", on);
      b.setAttribute("aria-pressed", String(on));
      b.querySelector("span").textContent = b.getAttribute(on ? "data-on" : "data-off");
    });
  }
  d.addEventListener("click", function (e) {
    var b = e.target.closest("[data-done]");
    if (!b) return;
    var n = +b.getAttribute("data-done"), done = getDone(), i = done.indexOf(n);
    if (i >= 0) done.splice(i, 1); else done.push(n);
    store(KEY, JSON.stringify(done));
    paint();
  });
  paint();

  /* search: a small client-side index built by tools/build.py */
  var box = d.getElementById("search"), input = d.getElementById("search-input"), list = d.getElementById("search-results");
  var hint = box && box.querySelector(".search__hint");
  var index = null, loading = false, sel = -1;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function mark(text, terms) {
    var out = esc(text);
    terms.forEach(function (w) {
      if (!w) return;
      out = out.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
    });
    return out;
  }
  function load() {
    if (index || loading || !box) return;
    loading = true;
    fetch(root + "assets/search-" + lang + ".json").then(function (r) { return r.json(); })
      .then(function (j) { index = j; run(); }).catch(function () { loading = false; });
  }
  function openSearch() {
    if (!box) return;
    box.hidden = false; input.value = ""; list.innerHTML = ""; sel = -1; body.style.overflow = "hidden";
    if (hint) hint.textContent = hint.getAttribute("data-default") || (hint.setAttribute("data-default", hint.textContent), hint.textContent);
    input.focus(); load();
  }
  function closeSearch() { if (box && !box.hidden) { box.hidden = true; body.style.overflow = ""; } }
  function run() {
    if (!index) return;
    var q = input.value.trim().toLowerCase();
    if (!q) { list.innerHTML = ""; return; }
    var terms = q.split(/\s+/), scored = [];
    index.forEach(function (p) {
      var t = p.t.toLowerCase(), h = (p.h || []).join(" ").toLowerCase(), x = p.x.toLowerCase(), s = 0, ok = true;
      terms.forEach(function (w) {
        var k = 0;
        if (t.indexOf(w) >= 0) k += 10;
        if (h.indexOf(w) >= 0) k += 4;
        if (x.indexOf(w) >= 0) k += 1;
        if (!k) ok = false;
        s += k;
      });
      if (ok) scored.push([s, p]);
    });
    scored.sort(function (a, b) { return b[0] - a[0]; });
    if (!scored.length) { list.innerHTML = ""; if (hint) hint.textContent = hint.getAttribute("data-none"); return; }
    if (hint) hint.textContent = hint.getAttribute("data-default");
    list.innerHTML = scored.slice(0, 8).map(function (r) {
      var p = r[1], x = p.x, pos = x.toLowerCase().indexOf(terms[0]);
      var from = Math.max(0, pos - 50), snip = (from ? "… " : "") + x.slice(from, from + 130) + (x.length > from + 130 ? " …" : "");
      return '<li><a href="' + esc(root + p.u) + '"><b>' + mark(p.t, terms) + "</b><span>" + mark(snip, terms) + "</span></a></li>";
    }).join("");
    sel = -1;
  }
  each("[data-search-open]", function (b) { b.addEventListener("click", openSearch); });
  each("[data-search-close]", function (b) { b.addEventListener("click", closeSearch); });
  if (box) {
    box.addEventListener("click", function (e) { if (e.target === box) closeSearch(); });
    input.addEventListener("input", run);
    input.addEventListener("keydown", function (e) {
      var items = [].slice.call(list.querySelectorAll("a"));
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!items.length) return;
        sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
        items.forEach(function (a, i) { a.classList.toggle("is-sel", i === sel); });
        items[sel].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter") {
        var a = items[sel >= 0 ? sel : 0];
        if (a) location.href = a.href;
      }
    });
  }
  d.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeDd(); closeSearch(); body.classList.remove("nav-open"); }
    var typing = /^(input|textarea|select)$/i.test((e.target.tagName || ""));
    if (!typing && (e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k"))) { e.preventDefault(); openSearch(); }
  });
})();
