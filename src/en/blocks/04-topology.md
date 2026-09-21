## The idea of the block

Until now the “done or not” judgment was purely visual: it looks as intended — so it’s done. Block 4 introduces a second criterion, invisible in a screenshot: **will this mesh survive movement?** A model can look perfect and yet break as soon as someone tries to bend it in a game or an animation, because inside the form there is a [[term:topology|topology]] with a random number of corners and triangular “fans” where a smooth bend should be.

The [[ex:clean-mesh|“Clean Mesh”]] trainer is exactly about this: three meshes that look the same, one bend, and only one deforms predictably. Start with it: [[app:clean-mesh|open the trainer]].

::: idea Through simple shapes, not abstract theory
Everything is explained on circles and rectangles → loops. Every concept is immediately checked on a real bend or joint.
:::

## Session 8 — why quads matter

Imagine your character has to raise an arm, or your car has to open a door. Are you sure the mesh at the bend will cope? Most people haven’t thought about it, and that’s fine: today is exactly about this.

**Quad, triangle or n-gon.** The same form can be made of different faces:

| Face type | What it gives | The problem if it’s not where it should be |
|---|---|---|
| **[[term:quad|Quad]]** (4 corners) | supports Loop Cut, easier UVs, predictable deformation | — (this is the goal) |
| **Triangle** | sometimes unavoidable (a cone’s tip, an edge) | a pile of triangles in a row = a [[term:pole|pole]]: a point where too many edges meet; deforms badly |
| **[[term:ngon|N-gon]]** (5+ corners) | quickly closes a big flat area | doesn’t support Subdivision and Loop Cut predictably, especially in a bend zone |

**[[term:edge-flow|Edge flow]].** Edge loops should run **around** a joint, like rings around a finger, not through it.

**The [[term:matcap|MatCap]] check.** In Viewport Shading → Solid pick a reflective MatCap instead of the flat material. On a bad, uneven mesh reflections “swim” and distort unevenly, on a clean one they lie smoothly. It’s a quick visual test you can do at any stage of the work.

**Practice: diagnose your own object.** Turn on MatCap on your object from [[block:3|block 3]] and find problem zones: poles, n-gons, abrupt changes in mesh density. For now only **find and mark** them; fixing everything in one session isn’t required. Having several problem zones is normal: today’s goal is learning to see.

::: challenge
Try to rebuild one of the problem zones by hand with clean loops (Loop Cut + connecting vertices manually), without waiting for the automatic tools of the next session.
:::

## Session 9 — retopology and the polygon budget

**Why can’t you simply press Subdivide on a bad mesh and get a clean model?** Because [[term:subdivision|Subdivision]] amplifies the existing topology rather than fixing it: a bad mesh becomes a “smooth bad mesh”.

**[[term:retopology|Retopology]]** is building a new clean mesh over the old form, using circles and rectangles as basic “islands” of topology joined by predictable loops. Helpers:

- **[[term:shrinkwrap|Shrinkwrap]]** pulls the new clean mesh onto the surface of the old form;
- **[[term:decimate|Decimate]]** quickly simplifies a mesh that is too heavy — a rough start, not a substitute for manual retopology.

**The polygon budget and [[term:lod|LOD thinking]].** Are all parts of a model equally important for the polygon count? A character’s face, or a detail the camera sees up close, deserves more polygons than a sole or an inner, invisible part. Different levels of detail for different parts or distances is LOD thinking.

**Practice.** Rebuild the problem zones of your object — by hand or with Shrinkwrap/Decimate where it makes sense. You don’t have to rebuild the whole model: fixing the zones where movement will really happen (joints, hinges) is enough; the rest may stay as it is.

::: checkpoint
Your object from block 3, checked and retopologized for predictable deformation: a clean mesh exactly where it matters. Show the “before” and “after” of the MatCap check.
:::

::: challenge
The same model with a deliberately reduced polygon budget: remove detail where it doesn’t affect the silhouette or function.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| MatCap shows no difference: the mesh looks equally “smooth” | The viewport is still in ordinary Solid mode with the standard material instead of a reflective MatCap | Viewport Shading → Solid → in the settings pick a reflective (metal or clay) MatCap instead of the flat one |
| Decimate makes the model equally rough everywhere | One overall simplification percentage was applied to the whole object regardless of important areas | Use Decimate with a Vertex Group (protect the important zones with weight) or simplify in parts by hand |
| After retopology with Shrinkwrap the new mesh “pokes through” or doesn’t sit on the old surface | Shrinkwrap targets the wrong shape, or the modifier order is mixed up | Check that Shrinkwrap targets the original (old) object and sits above Mirror/Subdivision in the stack |

## Before the session

- Blender 5.2 LTS; your object from block 3.
- Open [[app:clean-mesh|“Clean Mesh”]] and play a few rounds: the best warm-up.
