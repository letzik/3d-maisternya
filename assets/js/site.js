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
    var next = -1; for (var k = 0; k < 10; k++) { if (done.indexOf(k) < 0) { next = k; break; } }
    each(".bcard", function (c) { var b = +c.getAttribute("data-block"); c.classList.toggle("is-done", done.indexOf(b) >= 0); c.classList.toggle("is-next", done.length > 0 && b === next); });
    each("[data-segs] i", function (s, i) { s.classList.toggle("is-done", done.indexOf(i) >= 0); s.classList.toggle("is-next", i === next); });
    var cont = d.querySelector("[data-continue]");
    if (cont) {
      var back = done.length > 0;
      cont.hidden = !back;
      each("[data-new]", function (x) { x.hidden = back; });
      each("[data-continue-first]", function (x) { x.hidden = !back; });
      var link = cont.querySelector("[data-cont-link]"), hrefs = JSON.parse(cont.getAttribute("data-hrefs") || "[]");
      if (link) {
        if (next < 0) { link.href = cont.getAttribute("data-all-href"); link.querySelector("span").textContent = cont.getAttribute("data-all"); }
        else { link.href = hrefs[next]; link.querySelector("span").textContent = cont.getAttribute("data-label") + " " + (next < 10 ? "0" : "") + next; }
      }
    }
    each("[data-progress]", function (p) {
      var total = +p.getAttribute("data-total");
      var n = done.filter(function (x) { return x >= 0 && x < total; }).length;
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
    lastFocus = d.activeElement;
    box.hidden = false; input.value = ""; list.innerHTML = ""; sel = -1; body.style.overflow = "hidden";
    if (hint) hint.textContent = hint.getAttribute("data-default") || (hint.setAttribute("data-default", hint.textContent), hint.textContent);
    input.focus(); load();
  }
  var lastFocus = null;
  function closeSearch() { if (box && !box.hidden) { box.hidden = true; body.style.overflow = ""; if (lastFocus && lastFocus.focus) lastFocus.focus(); } }
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


/* v2 · motion and feedback. Pointer effects only on fine pointers; nothing runs under reduced motion. */
(function () {
  "use strict";
  var d = document, reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  function each(sel, fn) { [].forEach.call(d.querySelectorAll(sel), fn); }

  /* hero: one object per visit */
  var objs = d.querySelectorAll(".hero__obj");
  if (objs.length > 1) {
    var pick = Math.floor(Math.random() * objs.length);
    [].forEach.call(objs, function (o, i) { o.hidden = i !== pick; });
  }

  /* idea 01: cycle viewport modes (Object → Wireframe → X-ray → Subdivision) */
  each("[data-vp-cycle]", function (box) {
    var modes = JSON.parse(box.getAttribute("data-vp-cycle")), img = box.querySelector("img"), cap = box.querySelector(".idea__mode"), i = 0;
    modes.forEach(function (m) { var p = new Image(); p.src = m[0]; });
    if (reduce) return;
    var timer = null, io = new IntersectionObserver(function (en) {
      if (en[0].isIntersecting && !timer) timer = setInterval(function () { i = (i + 1) % modes.length; img.src = modes[i][0]; cap.textContent = modes[i][1]; }, 2200);
      else if (!en[0].isIntersecting && timer) { clearInterval(timer); timer = null; }
    });
    io.observe(box);
  });

  if (reduce) return;

  /* primary button ripple from the pointer */
  d.addEventListener("pointerdown", function (e) {
    var b = e.target.closest(".btn--primary");
    if (!b) return;
    var r = b.getBoundingClientRect(), s = d.createElement("span");
    s.className = "ripple";
    var size = Math.max(r.width, r.height) * 2.4;
    s.style.cssText = "left:" + (e.clientX - r.left) + "px;top:" + (e.clientY - r.top) + "px;width:" + size + "px;height:" + size + "px";
    b.appendChild(s);
    setTimeout(function () { s.remove(); }, 600);
  });

  /* theme toggle: a short light sweep across the page */
  var tt = d.querySelector("[data-theme-toggle]");
  if (tt) tt.addEventListener("click", function () {
    var light = d.documentElement.getAttribute("data-theme") === "light", s = d.createElement("div");
    s.className = "theme-sweep";
    s.style.background = light ? "radial-gradient(60vmax 60vmax at 85% 0%, rgba(255,236,170,.45), transparent 60%)" : "radial-gradient(60vmax 60vmax at 10% 0%, rgba(138,222,110,.18), transparent 60%)";
    d.body.appendChild(s);
    setTimeout(function () { s.remove(); }, 950);
  });

  if (!fine) return;

  /* card tilt: max 5°, number sits in front */
  each(".bcard, .xcard", function (c) {
    var raf = 0;
    c.addEventListener("pointermove", function (e) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 2 - 1, y = (e.clientY - r.top) / r.height * 2 - 1;
        c.style.transform = "perspective(700px) rotateX(" + (-y * 5).toFixed(2) + "deg) rotateY(" + (x * 5).toFixed(2) + "deg) translateY(-3px)";
      });
    });
    c.addEventListener("pointerleave", function () { c.style.transform = ""; });
  });

  /* hero parallax: glow and object move against the pointer, up to 14px */
  each("[data-parallax]", function (el) {
    var raf = 0;
    el.addEventListener("pointermove", function (e) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 2 - 1, y = (e.clientY - r.top) / r.height * 2 - 1;
        el.style.setProperty("--px1", "translate(" + (x * 5.6).toFixed(1) + "px," + (y * 5.6).toFixed(1) + "px)");
        el.style.setProperty("--px2", "translate(" + (-x * 14).toFixed(1) + "px," + (-y * 14).toFixed(1) + "px)");
      });
    });
    el.addEventListener("pointerleave", function () { el.style.removeProperty("--px1"); el.style.removeProperty("--px2"); });
  });
})();
