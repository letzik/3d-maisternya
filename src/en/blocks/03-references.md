## The idea of the block

Until now you built forms “from your head” — from imagination and memory of your own idea. That works well for simple, familiar things, but has a limit: as soon as the idea gets harder (a specific car model, a character with clear proportions, a building of a certain style), memory and your eye let you down — proportions “drift”, symmetry “by eye” turns out not to be so symmetrical.

The answer is not “more talent” but a concrete technique: **a [[term:reference|reference image]] right in the viewport**. This is what professional modelers do: they don’t invent proportions but check them against a real image, like an artist checks against a live model.

::: idea You choose the object
A car, a weapon, a character, a building, a creature — anything with a clear front and side view. You find or prepare the image yourself. It continues the principle of self-expression, now tied to real proportions.
:::

## Session 6 — the reference and a blockout along the outline

**What makes a good reference?** We discuss it in pairs, and the summary is:

- a view **strictly from the side and strictly from the front** (not in perspective and not at an angle), otherwise proportions get distorted when laid over an [[term:orthographic|orthographic view]];
- the same relative width and height of the object in both images, so you don’t fit the scale “by eye”;
- enough resolution to see the details you plan to model.

Look for technical drawings and blueprint images for machines and reference sites for characters. No perfect “front + side” pair? Even a single view will do if the object is fairly symmetrical.

**Importing into the [[term:viewport|viewport]].** Reference/Background Images puts the image on a separate orthographic plane tied to a specific view (Front/Side). Adjust the transparency (Opacity) so you can see through it to the mesh you’re building. **A typical mistake** is a forgotten scale: the reference and the future model must be of comparable size from the very start.

**Practice: a blockout along the outline.** Import your own reference and start a [[term:blockout|blockout]] with the same tools from blocks 1–2 (Mirror, Extrude, Inset, Bevel, Loop Cut, Knife), but check every step against the image’s outline, not against imagination. Big shapes first (the silhouette of the whole), details afterwards.

::: challenge
If the reference has complex asymmetry or a mechanism, start thinking about how to split the model into parts using Boolean and Merge from [[block:2]].
:::

## Session 7 — detailing from the reference

**How do you notice that proportions have drifted before the model is nearly done?** Regularly switch the view to Front/Side and compare with the reference at the same angle. Measure relative sizes (“the cabin is half the length of the body”), not absolute numbers.

Bring your object to a detailed state: add the elements the reference shows and the blockout doesn’t reproduce yet (protrusions, holes, small forms), using the whole toolkit of blocks 1–2.

::: checkpoint
Your own object (a car, weapon, character, building — your choice), modeled from a reference: a blockout and detailing. When you show it, put your screen next to the reference image so the correspondence itself is visible.
:::

::: challenge
An object with more complex symmetry or a mechanism, or your own drawn reference instead of a found photo: this tests whether your grasp of proportions no longer depends on a ready-made image.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| The model comes out stretched or squashed compared with the reference | The front and side images were imported at different scales relative to each other | Before you start, compare the object’s relative width/height in both images: they must be proportionally the same |
| The reference isn’t visible in the viewport, or the mesh doesn’t show through it | The Opacity is too low, or Front/Side were swapped on import | Raise the Opacity in the settings of the Empty holding the image; check which axis the image is tied to |
| Proportions imperceptibly “drift” while you work | You have no habit of regularly checking against the reference: it’s easy to get carried away detailing one area | Every 10–15 minutes switch the view to Front/Side and compare the silhouette with the reference |

## Before the session

- **Choose your own reference a week before session 6.** Don’t spend session time searching from scratch.
- For example, a car blueprint in four views is a typical example of a perfect reference.
- The file with your object and progress from block 2.
