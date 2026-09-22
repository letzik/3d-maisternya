## What it trains

The ability to see, before any animation, **whether a mesh will survive movement**. A model can look perfect and still break the moment you bend it. The exercise illustrates the topic of [[block:4]] with a moving picture instead of a static slide.

## How it works

You see three panels that **bend by the same angle at the same moment**. The form is the same everywhere; only the rows of loops on it differ. Pick the one whose mesh deforms predictably.

| What you’ll see | Why |
|---|---|
| **Even loops exactly in the bend zone** — clean quads | this is the right answer: a [[term:quad|quad]] mesh and [[term:edge-flow|edge flow]] around the bend |
| **Just as many loops as the correct mesh — only in the wrong place** | dense on the flat stretches, only three right in the bend: the count isn’t the problem, the placement is |
| **A triangular fan [[term:pole|pole]] exactly in the bend zone** | the worst possible place for a pole: the mesh “twists” unpredictably |

## What we take from it

- A beautiful shape is no guarantee: check the mesh on a real bend.
- **What matters here is not how many loops you have, but where they are.** The second option has exactly as many loops as the correct one — they just sit where the surface is already flat, not where it bends.
- Edge loops should run **around** a joint, like rings around a finger, not through it.
- A quick by-eye test in Blender is [[term:matcap|MatCap]]: on a bad mesh the reflections “swim”.

In the session we go through 2–3 rounds together out loud, and then everyone diagnoses their own object from [[block:3|block 3]].

::: note
Your score and streak are stored only in your browser. You can change the language with the UA/EN buttons in the exercise’s top corner.
:::
