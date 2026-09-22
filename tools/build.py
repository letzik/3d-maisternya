#!/usr/bin/env python3
"""Static site builder for the "3D-Майстерня" / "3D Workshop" learning resource.

    python3 tools/build.py            # rebuild uk/ en/ + search index + sitemap
    python3 tools/build.py --check    # build and run consistency checks only

Sources:  src/site.yml  src/blocks.yml  src/exercises.yml  src/glossary.yml
          src/<lang>/*.md   src/<lang>/blocks/*.md   src/<lang>/exercises/*.md
Output:   uk/  en/  assets/search-<lang>.json  index.html  404.html  sitemap.xml  robots.txt

The two languages are built from one structure, so every page exists in both languages and
the language switch always opens the same page in the other language. Requires only PyYAML.
"""
import html
import json
import posixpath
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
LANGS = ("uk", "en")
OTHER = {"uk": "en", "en": "uk"}


def load_yaml(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


CFG = load_yaml(SRC / "site.yml")
BLOCKS = load_yaml(SRC / "blocks.yml")["blocks"]
EXS = load_yaml(SRC / "exercises.yml")["exercises"]
GLOSS = load_yaml(SRC / "glossary.yml")["terms"]
UI = CFG["ui"]
HOME = CFG["home"]
SITE_URL = CFG["site_url"].rstrip("/") + "/"
REPO_URL = CFG["repo_url"]
BUILD_DATE = date.today().isoformat()

ERRORS = []


def err(msg):
    ERRORS.append(msg)
    print("ERROR:", msg, file=sys.stderr)


# ----------------------------------------------------------------------------- icons
def svg(inner, cls="ico", size=24, sw=1.7):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{inner}</svg>')


ICON_PATHS = {
    "cube": '<path d="M12 3 4 7.5v9L12 21l8-4.5v-9L12 3Z"/><path d="M4 7.5 12 12l8-4.5M12 12v9"/>',
    "knife": '<path d="M12 3 4 7.5v9L12 21l8-4.5v-9L12 3Z"/><path d="M2.5 15.5 21.5 8.5" stroke-dasharray="2 2.4"/>',
    "reference": '<rect x="3" y="5" width="18" height="14" rx="1.6"/><path d="M6 16c1.6-4.4 3.6-6 6-6s4.4 1.6 6 6"/><path d="M6 16h12"/><circle cx="9" cy="16.6" r="1"/><circle cx="15" cy="16.6" r="1"/>',
    "mesh": '<path d="M4 6c5-1.3 11-1.3 16 0M4 11c5 1.3 11 1.3 16 0M4 16.5c5 3 11 3 16 0"/><path d="M4 6c1.2 4 1.2 6.6 0 10.5M9.5 5.2c.9 4.6.9 9.6 0 13.3M14.5 5.2c-.9 4.6-.9 9.6 0 13.3M20 6c-1.2 4-1.2 6.6 0 10.5"/>',
    "character": '<circle cx="12" cy="5.5" r="2.7"/><path d="M8.4 10.5h7.2v6H8.4z"/><path d="M9.6 16.5V21M14.4 16.5V21M8.4 11.6 5 15.5M15.6 11.6 19 15.5"/>',
    "bones": '<circle cx="5.5" cy="18.5" r="2"/><circle cx="12" cy="11" r="2"/><circle cx="18.5" cy="4.5" r="2"/><path d="M6.9 17 10.6 12.6M13.4 9.4 17.1 5.9"/>',
    "export": '<path d="M12 3 4 7.5v9L12 21l8-4.5"/><path d="M4 7.5 12 12l3-1.7M12 12v9"/><path d="M15.5 5.5h6M18.5 2.5l3 3-3 3"/>',
    "ar": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.2"/><path d="M12 7.6 9.2 9.2v3.2L12 14l2.8-1.6V9.2L12 7.6Z"/><path d="M9.2 9.2 12 10.8l2.8-1.6M12 10.8V14"/><path d="M10.5 18.5h3"/>',
    "portfolio": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/><path d="m12 11.4 1.2 2.4 2.6.4-1.9 1.8.5 2.6-2.4-1.3-2.4 1.3.5-2.6-1.9-1.8 2.6-.4L12 11.4Z"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M18.7 5.3l-1.6 1.6M6.9 17.1l-1.6 1.6"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/>',
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "download": '<path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M5 19.5h14"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "bolt": '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6l1-8Z"/>',
    "flag": '<path d="M5 21V4M5 5h11l-2 3.5 2 3.5H5"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V16h5v-.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3Z"/>',
    "warn": '<path d="M12 3.5 2.5 20h19L12 3.5Z"/><path d="M12 10v4.5M12 17.4v.1"/>',
    "note": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.4 4 5.6 4 9s-1.4 6.6-4 9c-2.6-2.4-4-5.6-4-9s1.4-6.6 4-9Z"/>',
    "github": '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
}


def icon(name, cls="ico", size=24):
    return svg(ICON_PATHS[name], cls=cls, size=size)


LOGO = ('<svg class="logo" viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" focusable="false">'
        '<path d="M16 3 4 9.8v12.4L16 29l12-6.8V9.8L16 3Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M4 9.8 16 16.6l12-6.8M16 16.6V29" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M16 3v13.6L4 9.8Z" fill="var(--accent)" stroke="none" opacity=".9"/></svg>')

# ----------------------------------------------------------------------------- utilities
UK_TR = {"а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e", "є": "ie", "ж": "zh", "з": "z",
         "и": "y", "і": "i", "ї": "i", "й": "i", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
         "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
         "щ": "shch", "ь": "", "ю": "iu", "я": "ia", "'": "", "’": "", "ʼ": ""}
UK_ORDER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    out = "".join(UK_TR.get(ch, ch) for ch in text)
    out = re.sub(r"[^a-z0-9]+", "-", out).strip("-")
    return out or "section"


def esc(s):
    return html.escape(str(s), quote=True)


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def rel(frm, to):
    """Relative URL between two site-root-relative paths ('uk/a.html' -> 'en/b.html')."""
    start = posixpath.dirname(frm) or "."
    r = posixpath.relpath(to.split("#")[0].split("?")[0] or ".", start)
    tail = to[len(to.split("#")[0].split("?")[0]):]
    if to.endswith("/") and not r.endswith("/"):
        r += "/"
    return r + tail


def root_prefix(path):
    depth = path.count("/")
    return "../" * depth


def split_front(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, flags=re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def uk_sort_key(s):
    s = s.lower()
    return [UK_ORDER.index(c) + 1000 if c in UK_ORDER else ord(c) for c in s]


# ----------------------------------------------------------------------------- page registry
PAGES = {}       # (lang, key) -> {"path", "title"}
USAGE = {}       # (lang, term_id) -> [page keys that link to it]
SEARCH = {lang: [] for lang in LANGS}

BLOCK_BY_NUM = {b["num"]: b for b in BLOCKS}
EX_BY_SLUG = {e["slug"]: e for e in EXS}


def reg(lang, key, path, title):
    PAGES[(lang, key)] = {"path": path, "title": title}


def top_md(lang, name):
    return SRC / lang / f"{name}.md"


def register_pages():
    for lang in LANGS:
        for name in ("start", "program", "resources", "about", "exercises"):
            p = top_md(lang, name)
            if not p.exists():
                err(f"missing {p.relative_to(ROOT)}")
                continue
            fm, _ = split_front(p.read_text(encoding="utf-8"))
            path = f"{lang}/exercises/index.html" if name == "exercises" else f"{lang}/{name}.html"
            reg(lang, name, path, fm.get("title", name))
        reg(lang, "home", f"{lang}/index.html", UI[lang]["site_name"])
        reg(lang, "glossary", f"{lang}/glossary.html", UI[lang]["nav_glossary"])
        for b in BLOCKS:
            reg(lang, f"block:{b['num']}", f"{lang}/blocks/{b['slug']}.html", b["title"][lang])
        for e in EXS:
            reg(lang, f"ex:{e['slug']}", f"{lang}/exercises/{e['slug']}.html", e["title"][lang])


# ----------------------------------------------------------------------------- markdown
class Md:
    def __init__(self, lang, path, page_key):
        self.lang = lang
        self.path = path              # site-root-relative path of the page being rendered
        self.page_key = page_key
        self.headings = []            # (id, text) of h2
        self.seen_ids = set()
        self.terms = []               # ordered, unique term ids linked from this page

    # -- inline
    def key_html(self, combo):
        parts = [p.strip() for p in combo.split("+")]
        return "+".join(f"<kbd>{esc(p)}</kbd>" for p in parts).replace("+", '<span class="kbd-plus">+</span>')

    def directive(self, m):
        body = m.group(1)
        kind, _, arg = body.partition(":")
        arg, _, shown = arg.partition("|")
        kind, arg, shown = kind.strip(), arg.strip(), shown.strip()
        lang = self.lang
        if kind == "key":
            return self.key_html(arg)
        if kind == "term":
            if arg not in GLOSS:
                err(f"{self.path}: unknown term '{arg}'")
                return esc(shown or arg)
            if arg not in self.terms:
                self.terms.append(arg)
            label = shown or GLOSS[arg][lang]["term"]
            href = rel(self.path, f"{lang}/glossary.html#term-{arg}")
            return f'<a class="term" href="{href}" data-term="{arg}">{label}</a>'
        if kind == "block":
            try:
                num = int(arg)
                page = PAGES[(lang, f"block:{num}")]
            except (ValueError, KeyError):
                err(f"{self.path}: unknown block '{arg}'")
                return esc(shown or arg)
            label = shown or f"{UI[lang]['block_word']} {num}"
            return f'<a class="xref" href="{rel(self.path, page["path"])}" title="{esc(page["title"])}">{label}</a>'
        if kind == "ex":
            page = PAGES.get((lang, f"ex:{arg}"))
            if not page:
                err(f"{self.path}: unknown exercise '{arg}'")
                return esc(shown or arg)
            label = shown or page["title"]
            return f'<a class="xref" href="{rel(self.path, page["path"])}">{label}</a>'
        if kind == "page":
            page = PAGES.get((lang, arg))
            if not page:
                err(f"{self.path}: unknown page '{arg}'")
                return esc(shown or arg)
            label = shown or page["title"]
            return f'<a class="xref" href="{rel(self.path, page["path"])}">{label}</a>'
        if kind == "app":
            e = EX_BY_SLUG.get(arg)
            if not e:
                err(f"{self.path}: unknown app '{arg}'")
                return esc(shown or arg)
            target = e["app"].replace("{lang}", lang)
            sep = "" if e["kind"] == "template" else f"?lang={lang}"
            return f'<a class="xref" href="{rel(self.path, target)}{sep}">{shown or e["title"][lang]}</a>'
        err(f"{self.path}: unknown directive [[{body}]]")
        return esc(body)

    def link(self, m):
        text, url = m.group(1), m.group(2)
        url = url.replace("{root}", root_prefix(self.path)).replace("{lang}", self.lang)
        ext = re.match(r"https?://", url)
        if ext:
            return (f'<a class="ext" href="{esc(url)}" target="_blank" rel="noopener">{text}'
                    f'<span class="ext-ico">{icon("external", "ico ico-sm", 14)}</span></a>')
        return f'<a href="{esc(url)}">{text}</a>'

    def inline(self, s):
        codes = []

        def stash(m):
            codes.append(m.group(1))
            return f"\x00C{len(codes) - 1}\x00"

        s = re.sub(r"`([^`]+)`", stash, s)
        s = html.escape(s, quote=False)
        s = re.sub(r"\[\[([^\]]+)\]\]", self.directive, s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", self.link, s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
        s = re.sub(r"\x00C(\d+)\x00", lambda m: "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>", s)
        return s

    # -- blocks
    def heading_id(self, text):
        base = slugify(text)
        cand, n = base, 2
        while cand in self.seen_ids:
            cand = f"{base}-{n}"
            n += 1
        self.seen_ids.add(cand)
        return cand

    def table(self, rows):
        def cells(line):
            line = line.strip()
            if line.startswith("|"):
                line = line[1:]
            if line.endswith("|"):
                line = line[:-1]
            # pipes inside [[directive|alias]] and `code` are not column separators
            line = re.sub(r"\[\[[^\]]*\]\]|`[^`]*`", lambda m: m.group(0).replace("|", "\x01"), line)
            return [c.replace("\x01", "|").strip() for c in re.split(r"(?<!\\)\|", line)]

        head = cells(rows[0])
        body = [cells(r) for r in rows[2:]]
        labels = [strip_tags(self.inline(h)) for h in head]
        out = ['<div class="table-wrap"><table>', "<thead><tr>" + "".join(f"<th>{self.inline(h)}</th>" for h in head) + "</tr></thead><tbody>"]
        for r in body:
            tds = []
            for i, c in enumerate(r):
                lab = esc(labels[i]) if i < len(labels) else ""
                tds.append(f'<td data-label="{lab}">{self.inline(c.replace(chr(92) + "|", "|"))}</td>')
            out.append("<tr>" + "".join(tds) + "</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    def lst(self, lines):
        """Render a (possibly nested) list. lines: raw lines beginning with a list marker."""
        marker = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
        base_indent = len(marker.match(lines[0]).group(1))
        ordered = bool(re.match(r"\d+\.", marker.match(lines[0]).group(2)))
        items = []
        for ln in lines:
            m = marker.match(ln)
            if m and len(m.group(1)) == base_indent:
                items.append([m.group(3)])
            elif items:
                items[-1].append(ln)
        tag = "ol" if ordered else "ul"
        out = [f"<{tag}>"]
        for it in items:
            head = it[0]
            rest = it[1:]
            sub = [r for r in rest if marker.match(r)]
            cont = [r.strip() for r in rest if not marker.match(r) and r.strip()]
            txt = self.inline(" ".join([head] + cont))
            li = f"<li>{txt}"
            if sub:
                li += self.lst(sub)
            li += "</li>"
            out.append(li)
        out.append(f"</{tag}>")
        return "".join(out)

    def callout(self, kind, title, inner):
        names = {"tip": ("bulb", "callout_tip"), "warn": ("warn", "callout_warn"),
                 "checkpoint": ("flag", "callout_checkpoint"), "challenge": ("bolt", "callout_challenge"),
                 "note": ("note", "callout_note"), "idea": ("bulb", "callout_idea")}
        if kind not in names:
            err(f"{self.path}: unknown callout '{kind}'")
            kind = "note"
        ic, key = names[kind]
        label = title or UI[self.lang][key]
        return (f'<aside class="callout callout--{kind}"><div class="callout__head">{icon(ic, "ico", 20)}'
                f'<span>{self.inline(label)}</span></div><div class="callout__body">{self.blocks(inner)}</div></aside>')

    def blocks(self, text):
        lines = text.split("\n")
        i, out = 0, []
        list_re = re.compile(r"^(\s*)([-*]|\d+\.)\s+")
        while i < len(lines):
            ln = lines[i]
            if not ln.strip():
                i += 1
                continue
            m = re.match(r"^```(\w*)\s*$", ln)
            if m:
                j = i + 1
                buf = []
                while j < len(lines) and not lines[j].startswith("```"):
                    buf.append(lines[j])
                    j += 1
                code = html.escape("\n".join(buf), quote=False)
                out.append(f'<div class="codeblock"><button class="copy-btn" type="button" data-copy data-copied="{esc(UI[self.lang]["copied"])}">{esc(UI[self.lang]["copy"])}</button>'
                           f'<pre><code>{code}</code></pre></div>')
                i = j + 1
                continue
            m = re.match(r"^:::\s*(\w+)\s*(.*)$", ln)
            if m:
                depth, j, buf = 1, i + 1, []
                while j < len(lines):
                    if re.match(r"^:::\s*\w+", lines[j]):
                        depth += 1
                    elif lines[j].strip() == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    buf.append(lines[j])
                    j += 1
                out.append(self.callout(m.group(1), m.group(2).strip(), "\n".join(buf)))
                i = j + 1
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)(?:\s*\{#([\w-]+)\})?\s*$", ln)
            if m:
                level, text_, hid = len(m.group(1)), m.group(2), m.group(3)
                inner = self.inline(text_)
                hid = hid or self.heading_id(text_)
                if level == 2:
                    self.headings.append((hid, strip_tags(inner)))
                out.append(f'<h{level} id="{hid}"><a class="anchor" href="#{hid}" aria-label="link">#</a>{inner}</h{level}>')
                i += 1
                continue
            if re.match(r"^(-{3,}|\*{3,})\s*$", ln):
                out.append("<hr>")
                i += 1
                continue
            if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
                j = i
                buf = []
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    buf.append(lines[j])
                    j += 1
                out.append(self.table(buf))
                i = j
                continue
            if ln.startswith(">"):
                j, buf = i, []
                while j < len(lines) and lines[j].startswith(">"):
                    buf.append(re.sub(r"^>\s?", "", lines[j]))
                    j += 1
                out.append(f"<blockquote>{self.blocks(chr(10).join(buf))}</blockquote>")
                i = j
                continue
            if list_re.match(ln):
                j, buf = i, []
                while j < len(lines) and (list_re.match(lines[j]) or (lines[j].startswith("  ") and lines[j].strip())):
                    buf.append(lines[j])
                    j += 1
                out.append(self.lst(buf))
                i = j
                continue
            if ln.lstrip().startswith("<"):
                j, buf = i, []
                while j < len(lines) and lines[j].strip():
                    buf.append(lines[j])
                    j += 1
                raw = "\n".join(buf)
                raw = raw.replace("{root}", root_prefix(self.path)).replace("{lang}", self.lang)
                out.append(raw)
                i = j
                continue
            j, buf = i, []
            while j < len(lines) and lines[j].strip() and not re.match(r"^(#{1,6}\s|```|:::|>|\||-{3,}\s*$)", lines[j]) \
                    and not list_re.match(lines[j]):
                buf.append(lines[j].strip())
                j += 1
            out.append(f"<p>{self.inline(' '.join(buf))}</p>")
            i = j
        return "\n".join(out)


# ----------------------------------------------------------------------------- layout
def hreflang_links(lang, path):
    other_path = re.sub(r"^" + lang + "/", OTHER[lang] + "/", path)
    out = []
    for lg, p in ((lang, path), (OTHER[lang], other_path)):
        out.append(f'<link rel="alternate" hreflang="{lg}" href="{SITE_URL}{p}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}">')
    return "\n".join(out), other_path


def nav_html(lang, path):
    u = UI[lang]

    def a(key, label, cls="nav__link"):
        cur = ' aria-current="page"' if PAGES[(lang, key)]["path"] == path else ""
        return f'<a class="{cls}" href="{rel(path, PAGES[(lang, key)]["path"])}"{cur}>{label}</a>'

    in_blocks = path.startswith(f"{lang}/blocks/")
    drop = "".join(
        f'<a class="dd__item" href="{rel(path, PAGES[(lang, "block:" + str(b["num"]))]["path"])}"'
        f'{" aria-current=page" if PAGES[(lang, "block:" + str(b["num"]))]["path"] == path else ""}>'
        f'<span class="dd__num">{b["num"]}</span><span>{esc(b["title"][lang])}</span></a>' for b in BLOCKS)
    return (
        f'<nav class="nav" id="site-nav" aria-label="{esc(u["menu"])}">'
        f'{a("start", u["nav_start"])}{a("program", u["nav_program"])}'
        f'<div class="dd"><button class="nav__link dd__btn{" is-current" if in_blocks else ""}" type="button" aria-expanded="false" aria-controls="dd-blocks">'
        f'{u["nav_blocks"]}{icon("chevron", "ico ico-sm", 14)}</button>'
        f'<div class="dd__panel" id="dd-blocks">{drop}</div></div>'
        f'{a("exercises", u["nav_exercises"])}{a("glossary", u["nav_glossary"])}{a("resources", u["nav_resources"])}{a("about", u["nav_about"])}'
        f'</nav>')


def header_html(lang, path):
    u = UI[lang]
    home = rel(path, f"{lang}/index.html")
    _, other_path = hreflang_links(lang, path)
    sw = (f'<div class="langsw" role="group" aria-label="Language">'
          f'<a class="langsw__opt{" is-on" if lang == "uk" else ""}" href="{rel(path, re.sub("^" + lang + "/", "uk/", path))}" hreflang="uk" lang="uk"'
          f'{" aria-current=true" if lang == "uk" else ""}>UA</a>'
          f'<a class="langsw__opt{" is-on" if lang == "en" else ""}" href="{rel(path, re.sub("^" + lang + "/", "en/", path))}" hreflang="en" lang="en"'
          f'{" aria-current=true" if lang == "en" else ""}>EN</a></div>')
    return (
        f'<header class="site-header"><div class="site-header__in">'
        f'<a class="brand" href="{home}">{LOGO}<span class="brand__t"><b>{esc(u["site_name"])}</b><small>{esc(u["site_sub"])}</small></span></a>'
        f'{nav_html(lang, path)}'
        f'<div class="tools">'
        f'<button class="iconbtn" type="button" data-search-open aria-label="{esc(u["search"])}" title="{esc(u["search"])}">{icon("search")}</button>'
        f'<button class="iconbtn" type="button" data-theme-toggle aria-label="{esc(u["theme_toggle"])}" title="{esc(u["theme_toggle"])}">'
        f'<span class="i-sun">{icon("sun")}</span><span class="i-moon">{icon("moon")}</span></button>'
        f'{sw}'
        f'<button class="iconbtn nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false" aria-label="{esc(u["menu"])}">'
        f'<span class="i-open">{icon("menu")}</span><span class="i-shut">{icon("close")}</span></button>'
        f'</div></div></header>')


def footer_html(lang, path):
    u = UI[lang]

    def a(key, label):
        return f'<li><a href="{rel(path, PAGES[(lang, key)]["path"])}">{label}</a></li>'

    return (
        f'<footer class="site-footer"><div class="site-footer__in">'
        f'<div><p class="foot-brand">{LOGO}<b>{esc(u["site_name"])}</b></p><p class="foot-org">{esc(u["footer_org"])}</p>'
        f'<p class="foot-note">{esc(u["footer_note"])}</p></div>'
        f'<div><p class="foot-h">{esc(u["footer_learn"])}</p><ul>{a("start", u["nav_start"])}{a("program", u["nav_program"])}'
        f'{a("exercises", u["nav_exercises"])}{a("glossary", u["nav_glossary"])}</ul></div>'
        f'<div><p class="foot-h">{esc(u["footer_about_title"])}</p><ul>{a("resources", u["nav_resources"])}{a("about", u["nav_about"])}'
        f'<li><a class="ext" href="{esc(REPO_URL)}" target="_blank" rel="noopener">{icon("github", "ico ico-sm", 16)} {esc(u["footer_repo"])}</a></li></ul></div>'
        f'</div><p class="site-footer__c">© 2026 {esc(u["site_name"])}</p></footer>')


def search_dialog(lang):
    u = UI[lang]
    return (f'<div class="search" id="search" role="dialog" aria-modal="true" aria-label="{esc(u["search"])}" hidden>'
            f'<div class="search__box"><div class="search__row">{icon("search")}'
            f'<input id="search-input" type="search" autocomplete="off" placeholder="{esc(u["search_placeholder"])}" aria-label="{esc(u["search"])}">'
            f'<button class="iconbtn" type="button" data-search-close aria-label="Close">{icon("close")}</button></div>'
            f'<ul class="search__results" id="search-results"></ul>'
            f'<p class="search__hint" data-none="{esc(u["search_none"])}" data-default="{esc(u["search_hint"])}">{esc(u["search_hint"])}</p></div></div>')


THEME_INIT = ("<script>(function(){try{var t=localStorage.getItem('3dm-theme');"
              "if(!t){t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}"
              "document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','dark')}})()</script>")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700'
         '&family=Oswald:wght@500;600;700&display=swap">')


def breadcrumbs(lang, path, trail):
    u = UI[lang]
    items = [f'<li><a href="{rel(path, f"{lang}/index.html")}">{esc(u["breadcrumb_home"])}</a></li>']
    for label, key in trail:
        if key:
            items.append(f'<li><a href="{rel(path, PAGES[(lang, key)]["path"])}">{esc(label)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def toc_html(lang, headings):
    if len(headings) < 2:
        return ""
    lis = "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in headings)
    return (f'<aside class="toc-rail"><details class="toc" data-toc><summary>{esc(UI[lang]["on_this_page"])}</summary>'
            f'<ol>{lis}</ol></details></aside>')


def sidebar_blocks(lang, path):
    u = UI[lang]
    lis = []
    for b in BLOCKS:
        p = PAGES[(lang, f"block:{b['num']}")]["path"]
        cur = ' aria-current="page"' if p == path else ""
        lis.append(f'<li><a class="side__link{" is-current" if p == path else ""}" href="{rel(path, p)}"{cur}>'
                   f'<span class="side__num">{b["num"]}</span><span class="side__t">{esc(b["title"][lang])}</span>'
                   f'<span class="side__check" data-check="{b["num"]}">{icon("check", "ico", 16)}</span></a></li>')
    return (f'<nav class="side" aria-label="{esc(u["all_blocks"])}"><p class="side__title">{esc(u["all_blocks"])}</p>'
            f'<ol class="side__list">{"".join(lis)}</ol>'
            f'<div class="progress" data-progress data-total="{len(BLOCKS)}" data-text="{esc(u["progress_of"])}">'
            f'<p class="progress__label">{esc(u["progress_label"])}</p>'
            f'<div class="progress__bar"><span></span></div><p class="progress__n"></p></div></nav>')


def sidebar_exercises(lang, path):
    lis = []
    for e in EXS:
        p = PAGES[(lang, f"ex:{e['slug']}")]["path"]
        lis.append(f'<li><a class="side__link{" is-current" if p == path else ""}" href="{rel(path, p)}"'
                   f'{" aria-current=page" if p == path else ""}><span class="side__num">{icon(e["icon"], "ico", 18)}</span>'
                   f'<span class="side__t">{esc(e["title"][lang])}</span></a></li>')
    return (f'<nav class="side" aria-label="{esc(UI[lang]["nav_exercises"])}"><p class="side__title">{esc(UI[lang]["nav_exercises"])}</p>'
            f'<ol class="side__list">{"".join(lis)}</ol></nav>')


def page_shell(lang, path, title, description, main, *, sidebar="", toc="", crumbs="", body_class="", wide=False):
    u = UI[lang]
    root = root_prefix(path)
    hl, _ = hreflang_links(lang, path)
    full_title = title if path == f"{lang}/index.html" else f"{title} · {u['site_name']}"
    classes = ["layout"]
    if wide:
        classes.append("layout--wide")
    if sidebar:
        classes.append("layout--side")
    elif toc:
        classes.append("layout--toc")
    if sidebar and toc:
        classes.append("has-toc")
    grid = " ".join(classes)
    head = (
        f'<!doctype html><html lang="{u["html_lang"]}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{esc(full_title)}</title><meta name="description" content="{esc(description)}">'
        f'<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(description)}">'
        f'<meta property="og:type" content="website"><meta property="og:url" content="{SITE_URL}{path}">'
        f'<meta name="theme-color" content="#161826">{hl}'
        f'<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">'
        f'{THEME_INIT}{FONTS}<link rel="stylesheet" href="{root}assets/css/site.css"></head>')
    body = (
        f'<body class="{body_class}" data-root="{root}" data-lang="{lang}" data-path="{path}">'
        f'<a class="skip" href="#main">{esc(u["skip"])}</a>{header_html(lang, path)}'
        f'<div class="{grid}">{sidebar}<main id="main" class="main">{crumbs}{main}</main>{toc}</div>'
        f'{footer_html(lang, path)}{search_dialog(lang)}'
        f'<script src="{root}assets/js/site.js" defer></script></body></html>')
    return head + body


def write(path, content):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def add_search(lang, path, title, headings, main_html):
    SEARCH[lang].append({"t": title, "u": path, "h": [h[1] for h in headings], "x": strip_tags(main_html)[:2400]})


# ----------------------------------------------------------------------------- page builders
def cards_blocks(lang, path):
    u = UI[lang]
    out = []
    for b in BLOCKS:
        p = PAGES[(lang, f"block:{b['num']}")]["path"]
        out.append(
            f'<a class="bcard" href="{rel(path, p)}" data-block="{b["num"]}">'
            f'<span class="bcard__top"><span class="bcard__num">{b["num"]:02d}</span>{icon(b["icon"], "ico bcard__ico", 40)}</span>'
            f'<span class="bcard__t">{esc(b["title"][lang])}</span>'
            f'<span class="bcard__d">{esc(b["tagline"][lang])}</span>'
            f'<span class="bcard__meta"><span>{icon("clock", "ico ico-sm", 15)} {b["sessions"]} {u["sessions_word"]}</span>'
            f'<span class="bcard__done" data-check="{b["num"]}">{icon("check", "ico ico-sm", 15)}</span></span></a>')
    return f'<div class="bgrid">{"".join(out)}</div>'


def cards_exercises(lang, path, only=None):
    u = UI[lang]
    out = []
    for e in EXS:
        if only is not None and e["slug"] not in only:
            continue
        p = PAGES[(lang, f"ex:{e['slug']}")]["path"]
        kind = u["kind_trainer"] if e["kind"] == "trainer" else u["kind_template"]
        blocks_txt = ", ".join(f"{u['block_word']} {n}" for n in e["blocks"])
        out.append(
            f'<a class="xcard" href="{rel(path, p)}"><span class="xcard__top">{icon(e["icon"], "ico", 30)}'
            f'<span class="tag">{esc(kind)}</span></span><span class="xcard__t">{esc(e["title"][lang])}</span>'
            f'<span class="xcard__d">{esc(e["tagline"][lang])}</span>'
            f'<span class="xcard__m">{esc(e["topic"][lang])} · {esc(blocks_txt)}</span></a>')
    return f'<div class="xgrid">{"".join(out)}</div>'


def build_home(lang):
    u, h = UI[lang], HOME[lang]
    path = f"{lang}/index.html"
    start = rel(path, PAGES[(lang, "start")]["path"])
    prog = rel(path, PAGES[(lang, "program")]["path"])
    idea = "".join(f'<div class="idea"><span class="idea__n">{i["n"]}</span><h3>{esc(i["t"])}</h3><p>{esc(i["d"])}</p></div>' for i in h["idea"])
    need = "".join(f'<li><b>{esc(n["t"])}</b><span>{esc(n["d"])}</span></li>' for n in h["need"])
    main = (
        f'<section class="hero"><div class="hero__stripes" aria-hidden="true"></div>'
        f'<p class="eyebrow">{esc(h["eyebrow"])}</p>'
        f'<h1 class="hero__t">{esc(h["title"])}<br><span>{esc(h["title2"])}</span></h1>'
        f'<p class="lede">{esc(h["lede"])}</p>'
        f'<div class="hero__cta"><a class="btn btn--primary" href="{start}">{esc(h["cta_start"])}{icon("arrow-right", "ico", 20)}</a>'
        f'<a class="btn" href="{prog}">{esc(h["cta_program"])}</a></div>'
        f'<p class="hero__note">{icon("globe", "ico ico-sm", 16)} {esc(h["languages_note"])}</p></section>'
        f'<section class="sec"><h2>{esc(h["idea_title"])}</h2><div class="ideas">{idea}</div></section>'
        f'<section class="sec"><div class="sec__head"><h2>{esc(h["map_title"])}</h2>'
        f'<div class="progress progress--inline" data-progress data-total="{len(BLOCKS)}" data-text="{esc(u["progress_of"])}">'
        f'<div class="progress__bar"><span></span></div><p class="progress__n"></p></div></div>'
        f'<p class="sec__lede">{esc(h["map_lede"])}</p>{cards_blocks(lang, path)}</section>'
        f'<section class="sec"><h2>{esc(h["ex_title"])}</h2><p class="sec__lede">{esc(h["ex_lede"])}</p>{cards_exercises(lang, path)}</section>'
        f'<section class="sec"><h2>{esc(h["need_title"])}</h2><ul class="need">{need}</ul>'
        f'<p><a class="btn" href="{esc(CFG["blender_url"])}" target="_blank" rel="noopener">{esc(h["need_blender"])}{icon("external", "ico ico-sm", 16)}</a></p></section>')
    desc = h["lede"]
    add_search(lang, path, u["site_name"], [], main)
    write(path, page_shell(lang, path, u["site_name"], desc, main, body_class="page-home", wide=True))


def build_simple(lang, name, *, crumb_trail=None, toc=True):
    """start / program / resources / about — plain markdown pages."""
    p = top_md(lang, name)
    fm, body = split_front(p.read_text(encoding="utf-8"))
    path = PAGES[(lang, name)]["path"]
    md = Md(lang, path, name)
    content = md.blocks(body)
    if name == "program":
        content = content.replace("<!--BLOCKS_TABLE-->", program_table(lang, path)).replace("<!--BLOCK_CARDS-->", cards_blocks(lang, path))
    eyebrow = f'<p class="eyebrow">{esc(fm["eyebrow"])}</p>' if fm.get("eyebrow") else ""
    main = f'<article class="prose-page">{eyebrow}<h1>{esc(fm["title"])}</h1>' + (f'<p class="lede">{md.inline(fm["lede"])}</p>' if fm.get("lede") else "") + f'<div class="prose">{content}</div>' + pager_simple(lang, name, path) + '</article>'
    for t in md.terms:
        USAGE.setdefault((lang, t), []).append(name)
    trail = [(fm["title"], None)]
    add_search(lang, path, fm["title"], md.headings, main)
    write(path, page_shell(lang, path, fm["title"], fm.get("description", fm.get("lede", "")), main,
                           crumbs=breadcrumbs(lang, path, trail), toc=toc_html(lang, md.headings) if toc else ""))


def pager_simple(lang, name, path):
    u = UI[lang]
    nxt = {"start": ("block:1", u["next_intro"]), "program": ("start", None)}.get(name)
    if not nxt or not nxt[1]:
        return ""
    page = PAGES[(lang, nxt[0])]
    return (f'<nav class="pager pager--one"><a class="pager__a pager__a--next" href="{rel(path, page["path"])}">'
            f'<small>{esc(nxt[1])}</small><b>{esc(page["title"])}</b>{icon("arrow-right", "ico", 22)}</a></nav>')


def program_table(lang, path):
    u = UI[lang]
    rows = []
    for b in BLOCKS:
        p = PAGES[(lang, f"block:{b['num']}")]["path"]
        rows.append(
            f'<tr><td data-label="#">{b["num"]}</td>'
            f'<td data-label="{esc(u["block_word"])}"><a href="{rel(path, p)}">{esc(b["title"][lang])}</a></td>'
            f'<td data-label="{esc(u["sessions_word"])}">{b["sessions"]}</td>'
            f'<td data-label="{esc(u["checkpoint_label"])}">{esc(b["checkpoint"][lang])}</td>'
            f'<td data-label="{esc(u["challenge_label"])}">{esc(b["challenge"][lang])}</td></tr>')
    head = f'<th>#</th><th>{esc(u["block_word"])}</th><th>{esc(u["sessions_word"])}</th><th>{esc(u["checkpoint_label"])}</th><th>{esc(u["challenge_label"])}</th>'
    return f'<div class="table-wrap"><table class="table--program"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def build_block(lang, b):
    u = UI[lang]
    key = f"block:{b['num']}"
    path = PAGES[(lang, key)]["path"]
    src = SRC / lang / "blocks" / f"{b['slug']}.md"
    if not src.exists():
        err(f"missing {src.relative_to(ROOT)}")
        return
    fm, body = split_front(src.read_text(encoding="utf-8"))
    md = Md(lang, path, key)
    content = md.blocks(body)
    n = b["num"]
    idx = BLOCKS.index(b)
    prev_b = BLOCKS[idx - 1] if idx > 0 else None
    next_b = BLOCKS[idx + 1] if idx < len(BLOCKS) - 1 else None
    hero = (
        f'<header class="bhero"><span class="bhero__num" aria-hidden="true">{n:02d}</span>'
        f'<div class="bhero__ico">{icon(b["icon"], "ico", 56)}</div>'
        f'<p class="eyebrow">// {esc(u["block_word"])} {n} {esc(u["of"])} {len(BLOCKS)} · {esc(u["sessions_word"])} {esc(b["range"])}</p>'
        f'<h1>{esc(b["title"][lang])}</h1><p class="lede">{esc(b["tagline"][lang])}</p>'
        f'<dl class="facts"><div><dt>{icon("clock", "ico ico-sm", 16)} {esc(u["time_label"])}</dt><dd>{b["sessions"]} {esc(u["sessions_word"])} · {esc(u["hours_each"])}</dd></div>'
        f'<div><dt>{icon("flag", "ico ico-sm", 16)} {esc(u["checkpoint_label"])}</dt><dd>{esc(b["checkpoint"][lang])}</dd></div>'
        f'<div><dt>{icon("bolt", "ico ico-sm", 16)} {esc(u["challenge_label"])}</dt><dd>{esc(b["challenge"][lang])}</dd></div></dl></header>')
    # related
    rel_parts = []
    if b["exercises"]:
        rel_parts.append(f'<section class="related__sec"><h2>{esc(u["practice_this"])}</h2>{cards_exercises(lang, path, only=b["exercises"])}</section>')
    if md.terms:
        chips = "".join(f'<a class="chip" href="{rel(path, f"{lang}/glossary.html#term-{t}")}">{GLOSS[t][lang]["term"]}</a>' for t in md.terms)
        rel_parts.append(f'<section class="related__sec"><h2>{esc(u["terms_here"])}</h2><div class="chips">{chips}</div></section>')
    if b["further"]:
        lis = "".join(f'<li><a class="ext" href="{esc(f["url"])}" target="_blank" rel="noopener">{esc(f["title"])}'
                      f'<span class="ext-ico">{icon("external", "ico ico-sm", 14)}</span></a> — {esc(f["note"][lang])}</li>' for f in b["further"])
        rel_parts.append(f'<section class="related__sec"><h2>{esc(u["further"])}</h2><ul class="links">{lis}</ul></section>')
    done = (f'<div class="donebar"><button class="btn btn--done" type="button" data-done="{n}" data-on="{esc(u["marked_done"])}" '
            f'data-off="{esc(u["mark_done"])}">{icon("check", "ico", 20)}<span>{esc(u["mark_done"])}</span></button></div>')

    def pg(bb, cls, label, arrow):
        if not bb:
            return f'<span class="pager__a pager__a--empty {cls}"></span>'
        pp = PAGES[(lang, f"block:{bb['num']}")]["path"]
        inner = (f'{icon("arrow-left", "ico", 22)}<span><small>{esc(label)} · {bb["num"]}</small><b>{esc(bb["title"][lang])}</b></span>'
                 if arrow == "l" else
                 f'<span><small>{esc(label)} · {bb["num"]}</small><b>{esc(bb["title"][lang])}</b></span>{icon("arrow-right", "ico", 22)}')
        return f'<a class="pager__a {cls}" href="{rel(path, pp)}">{inner}</a>'

    pager = f'<nav class="pager" aria-label="Pager">{pg(prev_b, "pager__a--prev", u["prev"], "l")}{pg(next_b, "pager__a--next", u["next"], "r")}</nav>'
    main = (f'<article class="block">{hero}<div class="prose">{content}</div>{done}'
            f'<div class="related">{"".join(rel_parts)}</div>{pager}</article>')
    for t in md.terms:
        USAGE.setdefault((lang, t), []).append(key)
    trail = [(PAGES[(lang, "program")]["title"], "program"), (f'{u["block_word"]} {n}', None)]
    add_search(lang, path, f'{u["block_word"]} {n}. {b["title"][lang]}', md.headings, main)
    write(path, page_shell(lang, path, f'{u["block_word"]} {n}. {b["title"][lang]}', b["tagline"][lang], main,
                           sidebar=sidebar_blocks(lang, path), toc=toc_html(lang, md.headings), crumbs=breadcrumbs(lang, path, trail)))


def build_exercises_hub(lang):
    u = UI[lang]
    path = PAGES[(lang, "exercises")]["path"]
    fm, body = split_front(top_md(lang, "exercises").read_text(encoding="utf-8"))
    md = Md(lang, path, "exercises")
    intro = md.blocks(body)
    main = (f'<article class="prose-page"><p class="eyebrow">{esc(fm.get("eyebrow", ""))}</p><h1>{esc(fm["title"])}</h1>'
            f'<p class="lede">{md.inline(fm["lede"])}</p><div class="prose">{intro}</div>{cards_exercises(lang, path)}</article>')
    for t in md.terms:
        USAGE.setdefault((lang, t), []).append("exercises")
    add_search(lang, path, fm["title"], md.headings, main)
    write(path, page_shell(lang, path, fm["title"], fm.get("description", fm["lede"]), main,
                           crumbs=breadcrumbs(lang, path, [(fm["title"], None)])))


def build_exercise(lang, e):
    u = UI[lang]
    key = f"ex:{e['slug']}"
    path = PAGES[(lang, key)]["path"]
    src = SRC / lang / "exercises" / f"{e['slug']}.md"
    if not src.exists():
        err(f"missing {src.relative_to(ROOT)}")
        return
    fm, body = split_front(src.read_text(encoding="utf-8"))
    md = Md(lang, path, key)
    content = md.blocks(body)
    target = e["app"].replace("{lang}", lang)
    href = rel(path, target) + ("" if e["kind"] == "template" else f"?lang={lang}")
    btns = f'<a class="btn btn--primary" href="{href}" target="_blank" rel="noopener">{esc(u["open_exercise"] if e["kind"] == "trainer" else u["open_template"])}{icon("arrow-right", "ico", 20)}</a>'
    if e["kind"] == "template":
        btns += f'<a class="btn" href="{href}" download>{icon("download", "ico", 18)}{esc(u["download_template"])}</a>'
    blocks_links = "".join(f'<a class="chip" href="{rel(path, PAGES[(lang, f"block:{n}")]["path"])}">{u["block_word"]} {n} — {esc(BLOCK_BY_NUM[n]["title"][lang])}</a>' for n in e["blocks"])
    kind = u["kind_trainer"] if e["kind"] == "trainer" else u["kind_template"]
    main = (f'<article class="block ex"><header class="bhero bhero--ex"><div class="bhero__ico">{icon(e["icon"], "ico", 56)}</div>'
            f'<p class="eyebrow">// {esc(kind)} · {esc(e["topic"][lang])}</p><h1>{esc(e["title"][lang])}</h1>'
            f'<p class="lede">{esc(e["tagline"][lang])}</p><div class="hero__cta">{btns}</div></header>'
            f'<div class="prose">{content}</div>'
            f'<div class="related"><section class="related__sec"><h2>{esc(u["supports_blocks"])}</h2><div class="chips chips--wide">{blocks_links}</div></section></div>'
            f'<nav class="pager pager--one"><a class="pager__a pager__a--prev" href="{rel(path, PAGES[(lang, "exercises")]["path"])}">{icon("arrow-left", "ico", 22)}<span><small>{esc(u["back_to_exercises"])}</small></span></a></nav></article>')
    for t in md.terms:
        USAGE.setdefault((lang, t), []).append(key)
    trail = [(PAGES[(lang, "exercises")]["title"], "exercises"), (e["title"][lang], None)]
    add_search(lang, path, e["title"][lang], md.headings, main)
    write(path, page_shell(lang, path, e["title"][lang], e["tagline"][lang], main, sidebar=sidebar_exercises(lang, path),
                           toc=toc_html(lang, md.headings), crumbs=breadcrumbs(lang, path, trail)))


def build_glossary(lang):
    u = UI[lang]
    path = PAGES[(lang, "glossary")]["path"]
    terms = sorted(GLOSS.items(), key=lambda kv: uk_sort_key(kv[1][lang]["term"]) if lang == "uk" else kv[1][lang]["term"].lower())
    md = Md(lang, path, "glossary")
    letters = []
    seen_letters = []
    blocks_html = []
    for tid, t in terms:
        letter = t[lang]["term"][0].upper()
        if letter not in seen_letters:
            seen_letters.append(letter)
        used = USAGE.get((lang, tid), [])
        used_links = []
        for k in dict.fromkeys(used):
            pg = PAGES[(lang, k)]
            label = f'{u["block_word"]} {k.split(":")[1]}' if k.startswith("block:") else pg["title"]
            used_links.append(f'<a class="chip chip--sm" href="{rel(path, pg["path"])}">{esc(label)}</a>')
        see = "".join(f'<a class="chip chip--sm" href="#term-{s}">{GLOSS[s][lang]["term"]}</a>' for s in t.get("see", []) if s in GLOSS)
        blocks_html.append(
            f'<div class="term-entry" id="term-{tid}" data-letter="{letter}"><h3>{t[lang]["term"]}</h3><p>{md.inline(t[lang]["def"])}</p>'
            f'<div class="term-meta">'
            f'{"<p><b>" + esc(u["used_in"]) + ":</b> " + "".join(used_links) + "</p>" if used_links else ""}'
            f'{"<p><b>" + esc(u["term_see"]) + ":</b> " + see + "</p>" if see else ""}</div></div>')
    letters_html = "".join(f'<a href="#letter-{i}">{l}</a>' for i, l in enumerate(seen_letters))
    # insert letter anchors
    out, last = [], None
    for html_block, (tid, t) in zip(blocks_html, terms):
        letter = t[lang]["term"][0].upper()
        if letter != last:
            out.append(f'<h2 class="letter" id="letter-{seen_letters.index(letter)}">{letter}</h2>')
            last = letter
        out.append(html_block)
    title = u["nav_glossary"]
    intro = {"uk": "Короткі визначення всіх термінів, що зустрічаються на занятях. Кожен термін у текстах блоків веде сюди, а тут — назад до блоків, де він використаний.",
             "en": "Short definitions of every term used in the sessions. Each term in a block text links here, and each entry links back to the blocks where it appears."}[lang]
    main = (f'<article class="prose-page"><p class="eyebrow">// {esc(u["glossary_intro_count"].format(n=len(terms)))}</p><h1>{esc(title)}</h1>'
            f'<p class="lede">{esc(intro)}</p><nav class="letters" aria-label="{esc(u["letters"])}"><span>{esc(u["letters"])}:</span>{letters_html}</nav>'
            f'<div class="glossary">{"".join(out)}</div></article>')
    add_search(lang, path, title, [], main)
    for tid, t in terms:
        SEARCH[lang].append({"t": t[lang]["term"], "u": f"{path}#term-{tid}", "h": [], "x": strip_tags(md.inline(t[lang]["def"]))})
    write(path, page_shell(lang, path, title, intro, main, crumbs=breadcrumbs(lang, path, [(title, None)]), body_class="page-glossary"))


def build_root():
    langs_js = "['" + "','".join(LANGS) + "']"
    links = "".join(f'<a class="btn" href="{lg}/" hreflang="{lg}">{UI[lg]["lang_name"]}</a>' for lg in LANGS)
    write("index.html",
          f'<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
          f'<title>{esc(UI["uk"]["site_name"])} · {esc(UI["en"]["site_name"])}</title>'
          f'<meta name="description" content="{esc(HOME["uk"]["lede"])}"><meta name="theme-color" content="#161826">'
          f'<link rel="alternate" hreflang="uk" href="{SITE_URL}uk/"><link rel="alternate" hreflang="en" href="{SITE_URL}en/">'
          f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}"><link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">'
          f'{THEME_INIT}{FONTS}<link rel="stylesheet" href="assets/css/site.css">'
          f'<noscript><style>.gate__wait{{display:none}}</style></noscript>'
          f'<script>(function(){{try{{var s=localStorage.getItem("3dm-lang");var l=(navigator.languages&&navigator.languages[0])||navigator.language||"uk";'
          f'var t=s||((l+"").toLowerCase().indexOf("en")===0?"en":"uk");if({langs_js}.indexOf(t)<0)t="uk";location.replace(t+"/"+location.search+location.hash)}}catch(e){{}}}})()</script>'
          f'</head><body class="gate"><main class="gate__in">{LOGO}<h1>{esc(UI["uk"]["site_name"])} <span>/</span> {esc(UI["en"]["site_name"])}</h1>'
          f'<p class="gate__wait">…</p><div class="hero__cta">{links}</div></main></body></html>')
    write("404.html",
          f'<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
          f'<title>404 · {esc(UI["uk"]["site_name"])}</title><meta name="robots" content="noindex">{THEME_INIT}{FONTS}'
          f'<link rel="stylesheet" href="{SITE_URL}assets/css/site.css"></head><body class="gate"><main class="gate__in">{LOGO}<h1>404</h1>'
          f'<p>{esc(UI["uk"]["not_found_text"])}</p><p>{esc(UI["en"]["not_found_text"])}</p>'
          f'<div class="hero__cta"><a class="btn btn--primary" href="{SITE_URL}uk/">{esc(UI["uk"]["not_found_home"])}</a>'
          f'<a class="btn" href="{SITE_URL}en/">{esc(UI["en"]["not_found_home"])}</a></div></main></body></html>')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
    write(".nojekyll", "")
    urls = []
    for (lang, key), pg in PAGES.items():
        other = re.sub(r"^" + lang + "/", OTHER[lang] + "/", pg["path"])
        urls.append(
            f'<url><loc>{SITE_URL}{pg["path"]}</loc><lastmod>{BUILD_DATE}</lastmod>'
            f'<xhtml:link rel="alternate" hreflang="{lang}" href="{SITE_URL}{pg["path"]}"/>'
            f'<xhtml:link rel="alternate" hreflang="{OTHER[lang]}" href="{SITE_URL}{other}"/></url>')
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                         'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(urls) + "</urlset>")


def build_all():
    for lang in LANGS:
        shutil.rmtree(ROOT / lang, ignore_errors=True)
    register_pages()
    for lang in LANGS:
        build_home(lang)
        for name in ("start", "program", "resources", "about"):
            build_simple(lang, name)
        for b in BLOCKS:
            build_block(lang, b)
        build_exercises_hub(lang)
        for e in EXS:
            build_exercise(lang, e)
    for lang in LANGS:          # glossary last: it needs the usage map
        build_glossary(lang)
        write(f"assets/search-{lang}.json", json.dumps(SEARCH[lang], ensure_ascii=False, separators=(",", ":")))
    build_root()


def check():
    """Consistency checks: language parity, internal links, anchors, missing assets."""
    files = {}
    for lang in LANGS:
        files[lang] = sorted(str(p.relative_to(ROOT / lang)) for p in (ROOT / lang).rglob("*.html"))
    if files["uk"] != files["en"]:
        err(f"language parity broken: only-uk={set(files['uk']) - set(files['en'])} only-en={set(files['en']) - set(files['uk'])}")
    ids_cache = {}

    def ids_of(fp):
        if fp not in ids_cache:
            ids_cache[fp] = set(re.findall(r'\sid="([^"]+)"', fp.read_text(encoding="utf-8")))
        return ids_cache[fp]

    bad = 0
    for fp in list((ROOT / "uk").rglob("*.html")) + list((ROOT / "en").rglob("*.html")):
        text = fp.read_text(encoding="utf-8")
        text = re.sub(r"<(pre|code)\b.*?</\1>", "", text, flags=re.S)   # code samples are not links
        visible = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", text, flags=re.S)))
        for m in re.finditer(r"\[\[|\]\]|\*\*|\{#", visible):
            err(f"{fp.relative_to(ROOT)}: unrendered markdown near '{visible[max(0, m.start() - 30):m.end() + 30].strip()}'")
            bad += 1
            break
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if re.match(r"^(https?:|mailto:|#|data:|javascript:)", url):
                if url.startswith("#") and len(url) > 1 and url[1:] not in ids_of(fp):
                    err(f"{fp.relative_to(ROOT)}: missing anchor {url}")
                    bad += 1
                continue
            base, _, frag = url.partition("#")
            base = base.split("?")[0]
            if not base:
                continue
            target = (fp.parent / base).resolve()
            if not target.exists():
                err(f"{fp.relative_to(ROOT)}: broken link {url}")
                bad += 1
            elif frag and target.suffix == ".html" and frag not in ids_of(target):
                err(f"{fp.relative_to(ROOT)}: missing anchor {url}")
                bad += 1
    print(f"checked {sum(len(v) for v in files.values())} pages, {bad} link problems")


if __name__ == "__main__":
    build_all()
    check()
    n = sum(1 for _ in (ROOT / "uk").rglob("*.html"))
    print(f"built {n} pages per language")
    sys.exit(1 if ERRORS else 0)
