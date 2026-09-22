## The idea of the block

The five tools of block 1 are deliberately limited — so the first session is guaranteed to give a result. But they have a limit: all they can make are forms symmetrical about one axis, with details that “stick out”. Block 2 lifts that limit with three new tools:

- **[[term:knife|Knife]]** — cut the mesh freely, not only with loops across the form;
- **[[term:subdivision|Subdivision Surface]]** — smooth an angular form into an organic one in a controlled way;
- **[[term:boolean|Boolean]] and [[term:merge|Merge]]** — join separate parts into one model instead of only building on from one piece.

::: warn Subdivision Surface is not a “beauty button”
It is a tool that **amplifies what is already built into the topology** (the number and placement of loops). On an angular, uneven mesh it gives an angular, uneven “smooth” form. We come back to this in [[block:4]].
:::

::: idea A guiding principle: break the complex into parts
Behind [[term:merge|Merge]] and [[term:boolean|Boolean]] is a strategy that becomes critical in [[block:5]]: **a complex idea is not built as one solid piece**. You split it into logical parts (for a character — head, torso, limbs, weapon; for a car — body, wheels, interior details), work on each as its own object and assemble them only at the end. That makes it easier to keep everything in your head and to fix one part without risking the whole model.
:::

The through-line example of this block is **the same ship** as in block 1, not a new object. That is deliberate: real modeling work rarely stops at the first blockout — it comes back to an already-finished object again and again, adding a new layer of detail with new tools each time. Below is what the block-1 ship becomes after sessions 4 and 5: an uneven seam on the hull ([[term:knife|Knife]]), a dome on the stern, built separately and smoothed ([[term:subdivision|Subdivision Surface]]), a vent hole cut with [[term:boolean|Boolean]], and the dome itself attached to the hull with [[term:merge|Merge]].

<div class="fig-pair">
  <figure><img src="{root}assets/img/b1/b1-pislya.webp" alt="The ship at the end of block 1 — five colors, no extra hull detail yet" loading="lazy"><figcaption>Before — the ship at the end of block 1</figcaption></figure>
  <figure><img src="{root}assets/img/b2/b2-pislya.webp" alt="The same ship after block 2 — a vent hole, an attached dome, a seam on the hull" loading="lazy"><figcaption>After — sessions 4–5 of this block</figcaption></figure>
</div>

## Session 4 — Knife and Subdivision Surface

| Tool | What it does | Example |
|---|---|---|
| [[term:knife|Knife]] [[key:K]] | cuts the mesh along any line right across the model’s surface | an uneven hull-panel seam across the fuselage |
| [[term:subdivision|Subdivision Surface]] (modifier) | smooths an angular “cage” into an organic form | an angular block dome → a smooth streamlined dome |

<div class="tanim-grid">
  <div class="tanim">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <rect x="20" y="20" width="60" height="60" fill="none" stroke="var(--line)" stroke-width="3"/>
      <path class="ta-knife-line" d="M22 30 L78 74" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>
    </svg>
    <b>Knife</b>
    <span class="tanim-key"><kbd>K</kbd></span>
  </div>
  <div class="tanim">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <polygon class="ta-bevel-sharp" points="30,30 70,30 70,70 30,70" fill="none" stroke="var(--accent)" stroke-width="3"/>
      <circle class="ta-bevel-chamfer" cx="50" cy="50" r="26" fill="none" stroke="var(--accent)" stroke-width="3"/>
    </svg>
    <b>Subdivision</b>
    <span class="tanim-key">modifier</span>
  </div>
</div>

**Knife** ([[key:K]]) cuts the mesh along any line you draw with the mouse right across the model’s surface. Unlike Loop Cut, the line doesn’t have to be a straight loop around the whole form. With it you can cut an uneven seam, a hull panel, a scar, a triangular dent.

**Subdivision Surface** adds smoothness. Look at two contrasting examples:

- an organic creature or a character’s head: an angular blockout → a smooth form with one modifier;
- a spaceship hull with crisp engineered edges: here smoothness “eats” the design, so Subdivision isn’t needed.

Control the smoothing level (Levels Viewport / Render) and keep the effect **as a modifier** — then you can keep editing the rough “cage” instead of “baking” the result into the geometry right away.

### Each tool a bit closer up

- **[[term:knife|Knife]] ([[key:K]]).** Click to add points of the cut line one by one; [[key:Enter]] or a double click finishes the cut. By default the line “snaps” to existing edges — to cut freely, without snapping, hold [[key:C]]. If the cut needs to go all the way through the form, not just the side facing the camera, press [[key:X]] while cutting to turn on Cut Through.
- **[[term:subdivision|Subdivision Surface]].** Modifier Properties (the wrench icon) → Add Modifier → Generate → Subdivision Surface. Two level fields: **Viewport** (how much you see while working — keep it small, 1–2, or the viewport starts to lag) and **Render** (how much is computed in the final frame — here you can go higher). Protect edges that must stay sharp either with an extra loop right next to them (Loop Cut), or by setting an **Edge Crease** right on the edge ([[key:Shift+E]], drag with the mouse) — the extremes 0 and 1 mean “ordinary edge” and “fully rigid, Subdivision leaves it alone”.

### A worked example: two new layers on the same ship

Continuing the same ship. Both of this session’s tools show up clearly on two separate spots on the model — that makes it easier to see the effect of each one on its own before mixing them.

**A hull seam — Knife.** On the top face of the fuselage (the same one where a Loop Cut ran in block 1), draw a Knife cut on the diagonal — not straight along the loop, but at an angle, like a real hull-panel seam that isn’t afraid of looking “imperfect”. The cut line by itself gives no visible relief yet — Knife only adds an edge to the mesh. To actually make the seam read on the silhouette, there’s one more step: in Edit Mode select the new cut vertices and nudge them down a little ([[key:G]] → [[key:Z]] → a small negative number) — now there’s a height difference on either side of the seam, not just a line on a flat face, and light reacts to it.

<figure class="fig">
  <img src="{root}assets/img/b2/b2-knife.webp" alt="A cube block with a diagonal Knife cut, the cut vertices nudged down slightly — a clear diagonal seam runs across the top and down the front face" loading="lazy">
  <figcaption>Knife only adds an edge by itself; the visible seam appears once you move its vertices</figcaption>
</figure>

::: warn A cut with no relief is invisible
The most typical beginner trap with Knife: draw a line and expect a visible detail. The line by itself is just a new edge on a flat face; as long as both halves stay in the same plane, a chamfer or Bevel on that edge won’t change anything either — there’s no angle to round off. Visibility only comes from a difference in height, rotation or angle — moving vertices, an Extrude, or a similar deformation along the new edge.
:::

**A dome — Subdivision Surface.** Instead of cutting a dome straight into the hull, make it a **separate object** — a direct bridge to session 5, where separate objects are exactly what get joined together. The starting shape is a cube, turned through Inset and Extrude (tools you already know from block 1) into a stepped block, like a small ziggurat. On its own it’s angular:

<div class="fig-pair">
  <figure><img src="{root}assets/img/b2/b2-subdiv-before.webp" alt="A stepped, angular block dome shape, built from a cube with Inset and Extrude" loading="lazy"><figcaption>Before — the bare “cage” from Inset and Extrude</figcaption></figure>
  <figure><img src="{root}assets/img/b2/b2-subdiv-after.webp" alt="The same block after Subdivision Surface — a smooth streamlined dome with no sharp corners" loading="lazy"><figcaption>After — Subdivision Surface, the same block</figcaption></figure>
</div>

One modifier, and the same object, with the same proportions, suddenly looks like a cast part instead of a pile of cubes. That’s exactly the point of the warning at the start of the block: the “after” shape isn’t magic — it’s a direct continuation of the “before” shape; whatever is built into the angular cage (where exactly the Insets are, how the steps are arranged) decides where the smoothed surface flows.

::: challenge
Apply Subdivision Surface selectively — to part of the model only. To do that, keep edges sharp where they must stay sharp: with extra supporting loops or Edge Crease.
:::

## Session 5 — Boolean, Merge and assembling from parts

| Tool | What it does | Example |
|---|---|---|
| [[term:boolean|Boolean]] (modifier) | cuts out or adds volume in the shape of another object | a cylinder cuts a round vent hole in a hull side |
| [[term:merge|Merge]] [[key:Ctrl+J]] / [[key:M]] | joins separate objects into one, then welds the vertices at the seam | the dome from session 4 gets attached to the hull |

<div class="tanim-grid">
  <div class="tanim">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <rect x="22" y="22" width="56" height="56" fill="none" stroke="var(--line)" stroke-width="3"/>
      <circle class="ta-inset-r" cx="50" cy="50" r="20" fill="var(--accent)" opacity=".55"/>
      <circle class="ta-bevel-chamfer" cx="50" cy="50" r="14" fill="var(--panel)" stroke="var(--accent)" stroke-width="2"/>
    </svg>
    <b>Boolean</b>
    <span class="tanim-key">modifier</span>
  </div>
  <div class="tanim">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <circle class="ta-merge-l" cx="34" cy="50" r="14" fill="var(--accent)" opacity=".85"/>
      <circle class="ta-merge-r" cx="66" cy="50" r="14" fill="var(--accent)" opacity=".85"/>
    </svg>
    <b>Merge</b>
    <span class="tanim-key"><kbd>Ctrl</kbd><kbd>J</kbd></span>
  </div>
</div>

Ask yourself: **is there a part of my model that’s easier to make separately and attach than to pull out of the same solid form?** A wheel, a tower, a barrel, a handle — and the dome you just built in session 4 — that is the topic of the session.

- **Merge** — two separate actions that are easy to mix up. First, **Object → Join** ([[key:Ctrl+J]]) in Object Mode: select the part, then, holding [[key:Shift]], the main object; whichever you click last becomes the “main” one and absorbs the rest into one mesh. After that, the part and the hull are already one object, but doubled-up vertices can be left where they meet. The second step is, in Edit Mode, select everything ([[key:A]]) and **M → By Distance**: vertices lying closer than a set threshold get merged into one.
- **Boolean** (a modifier) cuts out or adds volume in the shape of another object: for example, a cylinder “cuts” a round hole in a body. More powerful but more fragile: it often leaves a messy mesh. Treat it as a tool “for a quick result”, not the standard workflow.

::: warn Don’t forget Apply Transform
The most typical beginner problem is a forgotten [[term:apply-transform|Apply Transform]] before Boolean or Merge. Objects “drift” or deform if transforms aren’t applied.
:::

### Each tool a bit closer up

- **[[term:boolean|Boolean]].** Modifier Properties → Add Modifier → Generate → Boolean → Operation: **Difference** cuts (the “knife” object removes everything it overlaps), **Union** merges both volumes into one with no internal walls, **Intersect** keeps only the shared part. The **Object** field is the “knife” itself: pick the helper object (a cylinder, a sphere) you’re cutting with. The **Solver** field: **Exact** is slower but more reliable — make it the default; **Fast** is quicker but more often leaves broken geometry on complex intersections. After you Apply the modifier the helper “knife” object isn’t needed anymore — hide it ([[key:H]]) or delete it, it no longer affects the result.
- **[[term:merge|Merge]].** The [[key:M]] menu has a few options: **At Center** collapses the selected vertices to one point — the exact midpoint between them; **At Last** collapses them to the position of the last-selected vertex (handy when you need to keep exactly that position); **By Distance** automatically welds every pair of vertices closer than a set threshold, without you having to select pairs by hand. For the seam between two objects you just joined, **By Distance** is usually the fastest and most reliable choice.

### A worked example: a vent and a dome on the same ship

**A vent hole — Boolean.** Add a cylinder on the side of the hull, oriented across the hull plating — this is the future “knife”. A Boolean modifier on the hull: Operation → Difference, Object → the cylinder you just added, Solver → Exact. The viewport immediately shows a round hole wherever the cylinder crosses the plating. Once the shape and position look right, Apply the modifier to bake the hole into the hull’s geometry, and the “knife” cylinder can be hidden or deleted.

**Attaching the dome — Merge.** Slide the dome from session 4 (already carrying its own Subdivision Surface) up against the stern, flush with the hull. Select the dome first, then, holding [[key:Shift]], the ship itself — the last click decides which object is “main” and absorbs the rest. [[key:Ctrl+J]] joins them into one object. In Edit Mode select everything ([[key:A]]) and **M → By Distance** to weld the vertices where the dome touches the hull — skip this step and the seam stays two separate, barely-overlapping meshes, which shows up as a thin gap on close inspection, or as a problem later, in [[block:7]] (export).

<figure class="fig">
  <img src="{root}assets/img/b2/b2-pislya.webp" alt="The ship after block 2: a Boolean vent hole in the hull, a dome on the stern attached with Merge, a Knife seam on the hull" loading="lazy">
  <figcaption>All three techniques from sessions 4–5 on one ship: the seam, the hole, the attached dome</figcaption>
</figure>

::: checkpoint
The same object from block 1, refined and assembled from several parts: the difference is visible between “before” (one solid blockout) and “after” (an assembled model where at least one part is a separate object attached with Merge, and at least one hole or protrusion comes from Boolean).
:::

::: challenge
The same model with a moving part (a lid, a door, a rotating turret) prepared as a separate object with its own pivot ([[term:origin|origin]]). This looks ahead to [[block:6]] (rigging).
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| The Knife cut is in the mesh, but nothing looks different | The cut line sits in the same plane as the rest of the face — there’s no angle to see or to chamfer | Select the new cut vertices and move them (Extrude or [[key:G]] along an axis) — visibility comes from a height or angle difference, not from the cut existing |
| Subdivision Surface inflates or squeezes a form where it should be sharp | There are no supporting loops near the edge that must stay crisp | Add another Loop Cut right next to the edge, or set an Edge Crease on it |
| After Boolean the model has holes or stray faces | The objects intersect ambiguously, or transforms weren’t applied beforehand | Object → Apply → All Transforms on both objects before Boolean; try another Solver (Exact) in the modifier |
| [[key:M]] doesn’t offer to join two different objects | The Merge menu only works on vertices inside ONE object in Edit Mode — two separate objects need Object → Join first | First [[key:Ctrl+J]] in Object Mode, and only then go into Edit Mode for M → By Distance |
| Merge by Distance doesn’t join vertices that look like they’re in one spot | The distance threshold is too small, or the vertices really are slightly apart | Increase the distance in the Merge by Distance field, or select the vertices by hand and join them with M → At Center |

## Before the session

- The file with your object from block 1 (saved and accessible: from the cloud or a flash drive) — sessions 4 and 5 continue that same file, not a fresh start.
- Think about which part of your model is worth making separately: that is the main question of session 5.
