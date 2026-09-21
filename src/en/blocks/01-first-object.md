## The idea of the block

At the introductory session you already did two things: you said what you want to learn to make and you put together a rough [[term:silhouette|silhouette]] of that idea from [[term:primitive|primitives]]. Block 1 is the bridge from “a pile of cubes and balls” to a first object you actually want to show: **colored, detailed, made in a single evening**.

The technique is borrowed from game-asset blockout practice (the Imphenzia channel): **five tools + the [[term:mirror|Mirror]] modifier + face colors without [[term:uv|UV unwrapping]]**. This minimal set is no accident: these five actions cover almost everything a beginner needs for a blockout, and skipping UV unwrapping removes the step where everybody usually gets stuck. You see a colored result right away, not a grey blank.

::: idea The object should be symmetrical
A vehicle, a weapon, a ship, a building, a creature in a calm pose — anything with a common axis. Symmetry doesn’t narrow your choice: it gives you [[term:mirror|Mirror]] — instantly doubled detail for half the work. This is exactly what lets you finish in a single session.
:::

The key skill of the block is **recognizing the right tool from the shape of the task** instead of hunting through menus at random.

## Session 2 — the five tools

Take your silhouette from the introductory session (or, if your idea has changed, start a new blockout — it takes a few minutes).

| Tool | What it does | Example |
|---|---|---|
| [[term:extrude|Extrude]] [[key:E]] | pulls a face or an edge out into new geometry | pull a ship’s nose out of a starting cube |
| [[term:inset|Inset]] [[key:I]] | creates a smaller face inside the selected one | an inset for a porthole before pushing it in |
| [[term:bevel|Bevel]] [[key:Ctrl+B]] | chamfers a sharp edge, removes the “plastic” look | round the corners of a hull |
| [[term:loop-cut|Loop Cut]] [[key:Ctrl+R]] | adds a loop of edges across a form | cut a wing so you can pull out an aileron later |
| [[term:mirror|Mirror]] (modifier) | mirrors one half across an axis | turn it on first — and forget about it |

A working order that goes well:

1. **Turn on Mirror first** (if the object isn’t symmetrical yet, check it now — it’s the cheapest thing to fix at the start). From then on edit only one half: the other repeats every move.
2. **Extrude and Inset** — add the protrusions that separate the silhouette from “just a cube”: a cockpit, a barrel, an ear, a tower.
3. **Bevel** — go over the sharp corners at the end, when you’re happy with the form.
4. **Loop Cut** — add 1–2 loops where you need detail inside a big flat area. No more: this is a blockout, not the final model.

::: challenge
A second object with more complex symmetry (not a simple mirror axis but, say, a rotational one: a wheel, a tower) or the same model with an extra moving part — a lid or a door. You’ll need it in [[block:2]].
:::

## Session 3 — color without painting

In a “grown-up” workflow there would be a separate, tedious stage here: unfold the model into a flat pattern, like an apple’s peel, and paint a texture on it. Today we **skip that stage entirely**. Beautiful doesn’t always mean complicated.

**Two ways**, both without a single click on a [[term:uv|UV map]]:

- **A material per face.** In Edit Mode select faces → create a new [[term:material|material]] → press Assign.
- **[[term:vertex-paint|Vertex Paint]].** Paint straight onto vertices or faces.

To see color in the viewport, switch the display to **Material Preview** (the sphere button at the top right).

**The palette principle:** 4–6 colors for the whole object is already enough. Fewer and the object looks monotonous, more and it’s hard to keep it coherent. Contrast between neighboring faces matters more than the number of shades. And the rule “**one part — one color**”: don’t mix shades within a single functional part.

::: checkpoint
A finished, colored, symmetrical object — your first showpiece of the year. Save it and your intermediate versions as separate files (`_step1.blend`, `_step2.blend`): you’ll need them if you miss a session or want to go back to an earlier version.
:::

::: challenge
Pick a palette for a mood or a material and explain why you chose these colors. For example, “rusty metal” — muted brown-orange shades with dark accents in the recesses; “neon toy” — bright saturated colors without midtones.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| Mirror doesn’t give symmetry: the other half appears in the wrong place or not at all | The object isn’t centered on its [[term:origin|origin]], or the wrong axis (X/Y/Z) is chosen in the modifier | Object → Set Origin → Origin to Geometry, then check the axis in the Mirror modifier itself |
| After Extrude/Inset part of the form “caves in” or is turned inside out | You pulled or inset in the wrong direction | Undo ([[key:Ctrl+Z]]) and repeat, watching the direction of the blue gizmo arrow before you confirm |
| The color you assigned to a face doesn’t show in the viewport | The viewport is in Solid mode rather than Material Preview, or the faces weren’t selected before Assign | Switch the viewport to Material Preview; make sure the faces are selected before you press Assign |

## Before the session

- Blender 5.2 LTS installed (free, runs on any PC).
- The hotkey list for the five tools (the table above) — print it or keep it in front of you: nobody has to memorize it the first time.
- Your notes about your idea from the introductory session, if you kept them.
- Practice in [[ex:see-shapes|“See the Shape”]]: it warms up the eye before a blockout.
