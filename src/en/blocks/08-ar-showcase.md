## The idea of the block

Last year “VR” in the club’s program meant a conditional item “if the equipment is available”, dependent on whether there was a headset in the room. This year it is replaced by a concrete, always-available result: **augmented reality straight from your phone**, no app and no special hardware — just a link or a QR code.

The technical basis is the [[term:model-viewer|model-viewer]] web component (developed by Google): you put a [[term:glb|GLB]] model into an ordinary web page, and on a phone AR mode opens with one tap: Quick Look on iOS, Scene Viewer on Android. That’s how furniture stores offer to “see how this chair will look in your room”.

::: idea This is a personal thing
The result of the block is not an abstract demonstration of a technology but **your own** model, made with **your own** hands, in augmented reality on **your own** phone.
:::

## Session 19 — model-viewer and the first launch

A page with `<model-viewer>` is a few lines of HTML, not a program: a web page with a GLB file and a “View in AR” button. The component detects the visitor’s device and picks the right way to show it: Quick Look for iPhone, Scene Viewer for Android, an ordinary rotating view for a computer.

**Practice: your own page with a model.** Take the `.glb` file from [[block:7|block 7]] and drop it into the ready-made template: the [[ex:ar-showcase|AR showcase template]]. In pairs if there aren’t enough laptops. The goal of the session is to see your model in the browser and rotate it with the mouse. AR mode on the phone comes next time, once the page is published and available by link: **AR needs a real internet address**, not just a file on your computer.

::: challenge
Choose the angle and lighting (`auto-rotate`, `camera-orbit`) so the model “shows itself” from its best side as soon as the page opens.
:::

## Session 20 — AR on the phone

**Warm-up.** Make sure the page from last time is **published** ([[term:github-pages|GitHub Pages]]) and reachable by link, not just a local file: this is a necessary condition for AR.

**The QR code.** Make a [[term:qr-code|QR code]] for your own link (any free generator will do): a convenient way to pass the address to a phone quickly without retyping a long URL. Scan it, press the AR button and place the model “on the table” in the room, walking around it with the camera.

::: checkpoint
Your own model opens in AR via a link or QR code: shown live, with the model “on the table” through the phone’s camera. At the end, take turns placing your models on a shared table.
:::

## Common problems

| Problem | Why it happened | The fix |
|---|---|---|
| The AR button doesn’t appear even on a supported phone | The page isn’t published yet (a local file), or the `<model-viewer>` lacks the `ar`/`ar-modes` attribute | Check that the link opens from the internet (`https`), not from a file on the computer; compare the attributes with the template |
| In AR the model looks huge or tiny compared with real space | The scale wasn’t checked in [[block:7|block 7]] | Go back to the N-panel in Blender, check the real Dimensions and re-export |
| The QR code doesn’t scan or leads to an empty page | The QR was generated for a local address (`localhost` or a file), not for the published link | Generate the QR only after publishing, for the final `https://…` URL |

## Before the session

- **The `.glb` from block 7** and access to a place to publish (for example, GitHub Pages).
- **A phone** (iOS or Android) with some charge: this is the block’s “equipment”, and everybody already has it.
- Any free QR generator.
- The template is on the [[ex:ar-showcase]] page.
