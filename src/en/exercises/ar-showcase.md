## What it is

A ready-made page with the [[term:model-viewer|model-viewer]] web component. You drop in your own [[term:glb|GLB]] model and publish the page — it rotates in the browser and, on a phone, opens in [[term:ar|augmented reality]] with one tap. We’ll use the same starting point for the portfolio page in [[block:9|block 9]].

## How to use it

1. **Download the template** and put your file next to it named `model.glb` (or change `src="…"` in the code to your own filename).
2. Replace the text in `alt="…"`: briefly describe the model for people who can’t see the image.
3. Replace the “Project name” and description placeholders under the viewport with yours: what the project is, the hardest part, what you learned.
4. **Publish the page** (for example on [[term:github-pages|GitHub Pages]]). On a local file the AR button won’t work: you need a real `https://…` link.
5. Make a [[term:qr-code|QR code]] for the published address and scan it with your phone.

## The minimal code

Everything needed for viewing and AR is a few lines of HTML:

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer/dist/model-viewer.min.js"></script>

<model-viewer
  src="model.glb"
  alt="A short description of the model"
  camera-controls
  auto-rotate
  ar
  ar-modes="webxr scene-viewer quick-look"
  shadow-intensity="1">
</model-viewer>
```

The template already contains this code, the styling and a demo model, so the page works right away — before you swap in your own.

## Before you publish

::: checkpoint Checklist
- **Scale and [[term:apply-transform|Apply Transform]]** are checked ([[block:7]]): the model doesn’t look too big or too small in AR.
- **[[term:normals|Normals]] are recalculated:** no black or missing faces.
- **The page is published** (not a local file) — otherwise the AR button won’t appear on the phone.
:::

::: warn
Generate the QR code **only after publishing**, for the final `https://…` address. A code pointing to `localhost` or a local file leads nowhere.
:::
