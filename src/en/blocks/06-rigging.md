## The idea of the block

“Rigging” sounds like a separate profession that takes years to study — and at depth, it is. But to bring one specific object to life with a simple motion loop you don’t need animation theory; you need **one repeatable sequence of actions** that you can go through for the first time in 15 minutes and repeat on your own object a second time, already deliberately. This is Grant Abbitt’s technique: a [[term:rigify|Rigify]] meta-rig → fitting the bones → generating the final rig → Automatic Weights → cleaning up the bone layers.

::: idea Rig for a specific movement
Rigging is preparation for a movement you already imagine (session 13 of block 5 asked about it). Don’t rig “just in case”: rig for a specific pose or loop.
:::

## Session 15 — Rigify: the meta-rig and generation

First remind yourself of the planned movement from [[block:5|block 5]]. Then six steps you go through on your own object:

| Step | Action | Why |
|---|---|---|
| **1** | Enable the Rigify add-on (Edit → Preferences → Add-ons) | gives ready-made “meta-rig” templates: you don’t build every bone by hand |
| **2** | Add a meta-rig that matches the object’s form (human, a simple biped or your own simple [[term:armature|armature]] of a few bones) | a starting frame that you then fit to the model |
| **3** | Move the meta-rig’s bones so they line up with the model’s joints (elbows, knees, hinges) | bones must lie inside the mesh exactly where bending happens |
| **4** | Generate the final rig (the Generate Rig button) | Rigify turns the meta-rig into a full control system with controllers |
| **5** | Bind the model to the rig via [[term:parent|Parent]] with Automatic Weights ([[key:Ctrl+P]]) | Blender itself works out which part of the mesh moves with which bone |
| **6** | Hide the extra bone layers (Bone Layers) | leave visible only the controllers you’ll really use |

**Practice.** Add the simplest meta-rig that matches the intended movement (not necessarily a full human skeleton: a few bones are often enough) and go through steps 3–5 on your object from block 5.

::: challenge
Understand the bone-layer structure and tidy up on your own (step 6), without waiting for help.
:::

## Session 16 — the motion loop and cleaning the weights

**Diagnostics.** Move the controllers and look for places where the mesh deforms wrongly. Typically: an elbow “pokes through” the sleeve, a shoulder caves in. **Automatic Weights got it wrong — what now?** [[term:weight-paint|Weight Paint]]: paint by hand which part of the mesh really belongs to which bone, at least in the worst spot. It’s a “quick patch” for one obvious defect, not a full course.

**The motion loop.** Set a few [[term:keyframe|keyframes]] (Insert Keyframe) for a simple loop: a walk, a part spinning, a door opening, depending on your idea. The goal is not a complex animation but **one convincing, looping movement**.

::: checkpoint
Your block 5 object, animated with a simple loop (walk, spin, open) through a rig you built yourself. Show 20–30 seconds of video or screen.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| The rig moves but the model doesn’t | The object is linked to the rig with a plain Parent without Automatic Weights (an Armature modifier with no weights) | Select the mesh first, then the rig (last) and repeat [[key:Ctrl+P]] → With Automatic Weights |
| Automatic Weights gave an obviously wrong skew: part of the mesh follows the wrong bone | The distance-based estimate errs where bones are close to each other | Weight Paint on the specific problem area: paint the right weight instead of redoing the whole rig |
| The meta-rig won’t generate or gives an error | The meta-rig bones were left in the default position, not fitted to the specific object’s mesh | Go back to step 3 (fitting the bones): Generate Rig works only after the bones are placed precisely along the form |

## Before the session

- Blender 5.2 LTS **with the Rigify add-on enabled** (check in advance).
- Save the rig as a separate version file (`_rig.blend`) apart from the unrigged model: if something goes wrong, you can start rigging again.
- Your object from block 5 and, possibly, an already planned hierarchy of parts.
