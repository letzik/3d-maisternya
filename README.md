# 3D-Майстерня · 3D Workshop

**Навчальний ресурс клубу «3D-Майстерня»** — двомовний (українська / English) сайт: програма року, дев’ять блоків, інтерактивні вправи, словник термінів із перехресними посиланнями, шаблон AR-вітрини.
**The learning resource of the “3D Workshop” club** — a bilingual (Ukrainian / English) site: the year’s program, nine blocks, interactive exercises, a glossary with cross-references and an AR showcase template.

🌐 https://letzik.github.io/3d-maisternya/

---

## Українською

### Як це влаштовано
Сайт — звичайні статичні HTML-сторінки для GitHub Pages. Їх **генерує** невеликий скрипт `tools/build.py` з текстів у теці `src/`, тому обидві мови завжди мають однакову структуру: кожна сторінка існує в `uk/` і `en/`, а перемикач мови відкриває ту саму сторінку іншою мовою.

```
src/site.yml         рядки інтерфейсу (UK/EN) і тексти головної
src/blocks.yml       дані дев’яти блоків (назви, чекпоінти, виклики, посилання)
src/exercises.yml    вправи й шаблони
src/glossary.yml     словник термінів (обидві мови в одному файлі)
src/uk/, src/en/     тексти сторінок у Markdown (start, program, about, resources, blocks/, exercises/)
tools/build.py       генератор сайту (потрібні лише Python 3 і PyYAML)
apps/                інтерактивні вправи (Three.js): see-shapes, clean-mesh
templates/           шаблони AR-вітрини (uk / en)
assets/              стилі, скрипти, іконки, індекс пошуку
uk/  en/  ...        ЗГЕНЕРОВАНІ сторінки — не редагуйте вручну
```

### Як змінити текст
1. Відредагуйте потрібний `.md` у `src/uk/…` і **відповідний** у `src/en/…`.
2. Запустіть `python3 tools/build.py` — він перебудує сайт і перевірить усі посилання, паритет мов і «недорендерений» Markdown.
3. Закомітьте зміни (разом із згенерованими `uk/` та `en/`) і надішліть у GitHub — Pages оновиться сам.

### Перехресні посилання в текстах
`[[term:mirror]]` — посилання на термін словника (у словнику автоматично з’явиться «Використано в…»); `[[block:4]]` — на блок; `[[ex:clean-mesh]]` — на сторінку вправи; `[[app:clean-mesh]]` — на саму вправу; `[[page:program]]` — на сторінку; `[[key:Ctrl+B]]` — клавіші. Вставка `|` задає власний підпис: `[[term:mirror|дзеркало]]`. Виноски: `::: tip`, `::: warn`, `::: checkpoint`, `::: challenge`, `::: idea`, `::: note` … `:::`.

### Приватність
Без реєстрації, без аналітики й відстеження. Прогрес («чекпоінт виконано») і рахунок у вправах зберігаються лише в `localStorage` браузера. Посилання-запрошення до Telegram-групи та розклад свідомо **не** публікуються на сайті.

---

## English

### How it works
The site is plain static HTML for GitHub Pages. It is **generated** by a small script, `tools/build.py`, from the texts in `src/`, so both languages always share one structure: every page exists in `uk/` and `en/`, and the language switch opens the same page in the other language.

### Changing text
1. Edit the `.md` file in `src/en/…` **and** its counterpart in `src/uk/…`.
2. Run `python3 tools/build.py` — it rebuilds the site and checks every link, language parity and unrendered Markdown.
3. Commit the changes (including the generated `uk/` and `en/`) and push — Pages updates by itself.

### Cross-references in texts
`[[term:mirror]]` links to a glossary term (the glossary entry then automatically lists “Used in…”); `[[block:4]]` — a block; `[[ex:clean-mesh]]` — an exercise page; `[[app:clean-mesh]]` — the exercise itself; `[[page:program]]` — a page; `[[key:Ctrl+B]]` — keyboard keys. Add `|text` for a custom label. Callouts: `::: tip`, `::: warn`, `::: checkpoint`, `::: challenge`, `::: idea`, `::: note` … `:::`.

### Privacy
No sign-up, no analytics, no tracking. Progress (“checkpoint done”) and exercise scores live only in the browser’s `localStorage`. The Telegram group invitation link and the schedule are deliberately **not** published on the site.
