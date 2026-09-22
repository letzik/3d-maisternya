## The idea of the block

The model has lived entirely inside Blender so far. Block 7 is about the last step, which often fails precisely because it seems a formality: **a correct export**. A model that looks perfect in Blender can arrive in another application a hundred times smaller, turned on its side or with black faces instead of color. The cause is always one of three: **transforms, scale, normals**.

::: idea The checklist is shared, the format isn’t
Some prepare a model for Unity or Unreal (a future game portfolio), others for their own AR showcase in [[block:8|block 8]] (web, GLB). The checklist is the same, the file format differs by target.
:::

## Session 17 — three things that break an export

**A live illustration:** a model deliberately left unprepared (transforms not applied), right after being imported into a test environment, looks deformed or the wrong size. This is what will happen to your model if you skip the checklist.

**1. [[term:apply-transform|Apply Transform]].** Object → Apply → All Transforms. There is the “visible” size and rotation of an object and its real internal data (Scale, Rotation) shown in the N-panel. If you don’t apply them, the receiving engine can interpret these numbers its own way, and the object will “drift”.

**2. Units and scale.** The key fact of 2026: Blender 5.x is metric by default (**1 unit = 1 meter**), while Unreal Engine counts in centimeters. A cube with a side of “1” in Blender is a meter: roughly a person’s height, not a house and not a button. If it looks wrong by eye, that’s the signal to check the scale before exporting.

**3. Names.** Meaningful names for objects and materials instead of `Cube.004`.

**Practice: the checklist on your own object.** Go through your model: Apply Transform; check the scale (does the object look a reasonable size next to a standard 1-meter cube); check the names.

::: challenge
Work out how the N-panel shows Dimensions in real units (meters/centimeters) and compare your object with the real size of the thing you imagined: a sword shouldn’t be as tall as a house.
:::

## Session 18 — normals and the format for your target

**Why can a model look fine in Blender but “go black” in places after export?** Because of [[term:normals|normals]]. Turn on Overlay → Normals or Face Orientation (blue/red coloring of faces): a face that “looks” the wrong way simply disappears or goes black after export into an engine with backface culling. The quick fix is Recalculate Normals ([[key:Shift+N]]).

**The format for your target:**

| Format | When | Why |
|---|---|---|
| **[[term:glb|GLB]]** | the web, your own AR showcase ([[block:8|block 8]]), Godot | compact, opens reliably right in the browser |
| **[[term:fbx|FBX]]** | Unity, Unreal Engine | the most proven format for exactly these engines |

Both formats “pack” geometry, materials and (if needed) a rig with animation into one file. The choice depends not on the model’s quality but on where it goes next.

**Practice: exporting.** Pick your target (an engine or the web/AR showcase) and export your object in the matching format, after going through the whole checklist from session 17. Aiming at block 8? Save a `.glb` file right away: you’ll need it in the next session.

::: checkpoint
Your own object is exported in a format for a specific target and verified (re-imported into Blender or opened in a simple GLB viewer): scale and normals are intact.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| After import the model looks “stretched” or deformed | A non-uniform scale (different Scale in X/Y/Z) wasn’t applied before export | Apply → All Transforms; check the N-panel: Scale must be `1.0` on all axes |
| The model’s color is lost: everything is grey after export | Only Viewport Display Color was used, not a real [[term:material|material]] (Principled BSDF with a Base Color) | Make sure the object has a full material with a filled Base Color, not only a visual color in the viewport |
| Faces partly go black or disappear after import | The normals of some faces “look” the wrong way | Face Orientation overlay → find the red faces → select them and press [[key:Shift+N]] (Recalculate Normals) |

## Before the session

- Blender 5.2 LTS and your object from block 6.
- A simple online or local GLB viewer to check exported files: any quick way to open a `.glb` and see the result is enough.
- Aiming at the [[block:8|AR showcase]]? Save the `.glb` version of your object right now.
- A useful 2026 pipeline checklist is on the [[page:resources]] page.
