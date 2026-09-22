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

## Session 4 — Knife and Subdivision Surface

**Knife** ([[key:K]]) cuts the mesh along any line you draw with the mouse right across the model’s surface. Unlike Loop Cut, the line doesn’t have to be a straight loop around the whole form. With it you can cut an uneven seam, a hull panel, a scar, a triangular dent.

**Subdivision Surface** adds smoothness. Look at two contrasting examples:

- an organic creature or a character’s head: an angular blockout → a smooth form with one modifier;
- a spaceship hull with crisp engineered edges: here smoothness “eats” the design, so Subdivision isn’t needed.

Control the smoothing level (Levels Viewport / Render) and keep the effect **as a modifier** — then you can keep editing the rough “cage” instead of “baking” the result into the geometry right away.

**Practice:** apply Knife and, if needed, Subdivision Surface to your object from block 1 — add a detail the old five tools couldn’t make (an uneven cutout, an organic smooth area). Don’t put Subdivision on the whole object at once: try it on one part first and compare “before” and “after”.

::: challenge
Apply Subdivision Surface selectively — to part of the model only. To do that, keep edges sharp where they must stay sharp: with extra supporting loops or Edge Crease.
:::

## Session 5 — Boolean, Merge and assembling from parts

Ask yourself: **is there a part of my model that’s easier to make separately and attach than to pull out of the same solid form?** A wheel, a tower, a barrel, a handle — that is the topic of the session.

- **Merge** ([[key:M]] → At Center / By Distance) joins separate objects or vertices into one mesh. A simple, reliable way for most cases: make the wheel separately, slide it up to the body, merge.
- **Boolean** (a modifier) cuts out or adds volume in the shape of another object: for example, a cylinder “cuts” a round hole in a body. More powerful but more fragile: it often leaves a messy mesh. Treat it as a tool “for a quick result”, not the standard workflow.

::: warn Don’t forget Apply Transform
The most typical beginner problem is a forgotten [[term:apply-transform|Apply Transform]] before Boolean or Merge. Objects “drift” or deform if transforms aren’t applied.
:::

::: checkpoint
Your object from block 1, refined and assembled from several parts: the difference between “before” (one solid blockout) and “after” (an assembled model with details of different kinds) is visible.
:::

::: challenge
The same model with a moving part (a lid, a door, a rotating turret) prepared as a separate object with its own pivot ([[term:origin|origin]]). This looks ahead to [[block:6]] (rigging).
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| Subdivision Surface inflates or squeezes a form where it should be sharp | There are no supporting loops near the edge that must stay crisp | Add another Loop Cut right next to the edge, or set an Edge Crease on it |
| After Boolean the model has holes or stray faces | The objects intersect ambiguously, or transforms weren’t applied beforehand | Object → Apply → All Transforms on both objects before Boolean; try another Solver (Exact) in the modifier |
| Merge by Distance doesn’t join vertices that look like they’re in one spot | The distance threshold is too small, or the vertices really are slightly apart | Increase the distance in the Merge by Distance field, or select the vertices by hand and join them with `M → At Center` |

## Before the session

- The file with your object from block 1 (saved and accessible: from the cloud or a flash drive).
- Think about which part of your model is worth making separately: that is the main question of session 5.
