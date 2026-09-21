## The idea of the block

This is the biggest project of the half-year. Unlike the previous blocks, **there is no new toolset here**: everything you need (five tools, detailing, references, topology) you already have from blocks 1–4. The leader’s role shifts from “show a new technique” to coaching and pacing.

You choose **your own idea from day one** — a character, a weapon or a prop: what you named at the introductory session, or changed since — and bring it to a presentable state. The path follows Grant Abbitt’s structure: **[[term:silhouette|silhouette]] from simple shapes → detailing → texture palette → a basic hierarchy for a pose**. The same path smaller objects already took in blocks 1–3, only now on the most ambitious idea of the year.

::: idea Everyone’s pace is their own
The question you’ll be asked in every session is always the same: “What shapes is this made of, and what is still missing?” If needed, you’ll be reminded of a specific tool from earlier blocks rather than shown a new one.
:::

::: idea Break down → work on the parts → assemble at the end
The flagship project is the first truly complex model of the year, and the principle from [[block:2]] becomes here a survival strategy for the project. Before you build the silhouette as one object, split your idea into **3–5 logical parts** (preferably on paper). Each part is a separate object: you can detail it, fix it or even redo it from scratch without risking the rest. Assembly through [[term:merge|Merge]], [[term:boolean|Boolean]] or [[term:parent|Parent]] is the last step, not the first.
:::

## Session 10 — the silhouette

First everyone names their idea or confirms the one they had. If the idea has grown into something too big for five sessions, narrow the scope, not the topic: not “less of a character” but “today this detail, not the whole set of armor”.

**Split the idea into parts right away:** name on paper or out loud 3–5 parts (a character: head, torso, arms, legs, a weapon or accessory; a car: body, wheels, cabin). This is the plan you’ll build by.

**Practice.** With the same tools from block 1 (Mirror, Extrude, Inset, Bevel, Loop Cut) make a rough [[term:silhouette|silhouette]] of the whole idea **part by part as separate objects**, with no detailing. The goal is not a single detail but the **proportions of the whole**, visible at a glance. A test: if you stopped work right now, does the idea read from the silhouette?

Don’t merge the parts into one solid object today: that’s the task of session 13, when all parts are already detailed and colored.

## Session 11 — detailing

Remind yourself of the plan: what part of the previous silhouette will become which detail. Then, with the tools of blocks 1–2 ([[term:knife|Knife]], [[term:subdivision|Subdivision Surface]], [[term:boolean|Boolean]]/[[term:merge|Merge]]) and, if needed, the [[term:reference|references]] from [[block:3|block 3]], bring the silhouette to a recognizable, detailed object.

Remember [[block:4|topology]]: detailing in zones of future movement (elbows, hinges, doors) — with clean loops right away, not “however it comes out”. In pairs, show your neighbor what you added and get one piece of advice.

## Session 12 — the texture palette

Return to the technique of color without UV unwrapping from [[block:1|block 1]] (per-face [[term:material|materials]] or [[term:vertex-paint|Vertex Paint]]). Now color the finished detailed model **deliberately, with a concrete mood or material in mind**: the same “rusty metal vs neon toy” principle, applied to the main project.

::: challenge
Micro-contrast: not one solid color over a big area but small accents (wear, highlights, a detail of another shade) that make the object “readable” from afar.
:::

## Session 13 — a hierarchy for the pose

What exactly in your object should move, even if you can’t animate it yet? This prepares the ground for [[block:6|rigging]].

Join the separate parts of the model into a parent-child structure ([[term:parent|Parent]], [[key:Ctrl+P]]): then a moving part (a character’s arm, a door, a turret) rotates about the right point ([[term:origin|origin]]) and not an arbitrary one.

::: checkpoint
A finished, presentable object — the portfolio piece of the first half of the year. Fix the shortcomings of detailing and color, set up the hierarchy for the planned moving part or pose.
:::

::: challenge
A simple pose or expression (for characters) or a functional moving part (for props and weapons): a “manual” test of what [[block:6|block 6]] will do systematically through a rig.
:::

## Session 14 — the final show-and-tell (if needed)

An extra session for those who need time: an open workshop and, at the end, a proper show. Everyone presents the finished object for 1–2 minutes: shows their screen, tells about the idea and the hardest part. It is the first “real” presentation of the year, so the questions from other participants are friendly and honest. Compare your screenshots with the silhouette from session 10 — and you’ll see your own journey.

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| The idea is too ambitious: clearly can’t be finished in 4–5 sessions | The idea wasn’t narrowed to a manageable size at the kickoff of session 10 | Narrow not the topic but the scope: one detail instead of a full set; a simpler silhouette that can be finished in [[block:9|block 9]] |
| The silhouette reads as “a pile of cubes”, not the intended idea | Too many primitives of the same size, no single dominant shape | Return to the silhouette: deliberately enlarge or stretch one key shape so it’s recognized at once |
| Stuck on one small detail and not moving on | No sense of a “deadline” for the intermediate step | The session’s checkpoint matters more than perfecting one detail: save a version, move on, return later |

## Before the session

- No new tools to prepare. The main thing is your idea and being ready to explain it clearly.
- Keep intermediate versions (`_silhouette.blend`, `_details.blend`, `_color.blend`): over 4–5 sessions this is especially valuable for comparing progress.
