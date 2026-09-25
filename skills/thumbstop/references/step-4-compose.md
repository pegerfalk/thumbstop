# Step 4: Compose

Write `<out>/composition-brief.md`, then build `<out>/composition/` with the
Hyperframes domain skills. The brief is the boundary: product, copy, claims,
timing, safe zones, caption policy and audio intent come from Thumbstop;
composition structure, animation, caption rendering and mixing are decided
with Hyperframes' current guidance. Do not paste markup from this skill.

## Scaffold

`init` refuses a non-empty directory, so scaffold first, without touching
anything outside `<out>`:

```bash
cd <out> && HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init composition \
  --example blank --resolution portrait --non-interactive
mkdir -p composition/assets
cp -R material/. composition/assets/
# with --voice only:
cp voice/voiceover.wav voice/caption-groups.json composition/assets/
```

Then copy the planned SFX and music as `audio.md` shows.
`HYPERFRAMES_SKIP_SKILLS=1` stops `init` from updating the user's globally
installed Hyperframes skills; that is the user's call, not a side effect.

## Structure (Hyperframes Studio conventions)

- Every scene or overlay group with nested markup is a sub-composition:
  one for the screen-text keywords (`data-track-kind="graphics"`), one for the
  captions (`data-track-kind="captions"`), one per recreated UI scene.
- Media (`<video>`, `<audio>`) may sit at the root with their own timing.
  Video is muted; each clip's own sound, if kept, is a separate `<audio>` with
  the same `data-start` / `data-duration` / `data-media-start`.
- One element kind per track: video, graphics, captions, voice, clip sound,
  music, SFX.

## Material handling

- **Own footage (tier 1)**: trim with `data-media-start`; hard cuts on beat
  boundaries. If a clip has **burned-in text** (labels, subtitles, UI chrome),
  it will fight the captions: punch the clip in on a non-timed wrapper
  (static scale, anchored so the text leaves the frame) or crop it; never let
  two texts speak at once.
- **The default look of recreated scenes (tiers 2–3) is light and airy**:
  white or pale grounds, soft layered shadows, rounded corners, generous
  space; an empty slot or pocket is pale with a dashed outline, never a black
  hole. Use a dark ground only when the project's own identity is dark (its
  site or app is dark).
- **Recreated UI (tier 2)**: rebuild from the project's real markup, copy and
  CSS variables at video scale (in-feed viewing: body ≥ 32 px, headlines
  ≥ 90 px). Simulate the key action the storyboard names (cursor, tap, typing,
  result appearing). Replace any personal data with neutral stand-ins.
- **Concept / text-forward (tiers 3–4)**: the project's own words, images,
  fonts and colours only.
- **The project's own fonts** are embedded with `@font-face` from the
  `.woff2` files step 1 downloaded (inside each sub-composition's
  `<template>`), so the recreated UI and the captions use the real type.
- **Overlay sub-compositions** (keywords, captions) have a transparent root:
  an opaque root background on a layer that spans the whole video hides every
  scene beneath it (`check` reports it as `text_occluded`).
- **De-emphasise with colour, not opacity**, when text stays on screen (the
  losing options, past items): a half-transparent card drops its text below
  WCAG contrast.
- **Layouts that reach below y 840 are at most 660 px wide** (x 120–780), with
  `box-sizing: border-box` so padding does not push them into the TikTok
  button column.
- **Initial states** (the hook's camera framing, hidden rows, off-screen
  sheets) are set outside the timeline: a timeline `set` at 0 does not render
  on frame 0, so the first frame would show the un-framed state. `lint` warns
  about it; treat the warning as an error. The pattern that passes both
  `lint` and `check`: set the hook's state when the composition is built;
  give any element that is tweened from-to more than once a baseline on the
  timeline at 0; and let later from-to tweens not render their start state
  until they begin (GSAP: `immediateRender: false`).
- **Per-beat state lives on the timeline.** Anything that differs between
  beats (stacking order, visibility, transform origin, perspective) is set on
  the timeline at the beat that needs it, never once at build time. A
  build-time change meant for the last beat applies to every earlier beat too
  (e.g. a z-index that puts a page behind another for the whole video).
- **3D moves stay flat**: a page turn or card flip uses a weak perspective
  (around 5000 px), so the imagery does not swing out into the text zone.
- A background that must extend a clip's edges matches the clip's own edge
  colour (sample it), never a generic fill.

## Screen story (no voice, the default)

The text beats from the plan are the words of the video. One text beat on
screen at a time (a kicker line above it is allowed), timed by the measured
beat table.

- **Type**: the project's display face (embedded), bold, ≥ 90 px for the
  line, ≥ 48 px for a kicker. Sentence case or the project's own casing; no
  all-caps paragraphs.
- **Place**: inside the safe box. Lines wider than 660 px sit above y 840;
  anything reaching below y 840 stays within x 120–780. Pick one text zone
  for the whole video (e.g. the upper third over the product, or a band just
  above y 840) so the eye learns where to read.
- **Contrast**: on a photo or footage, give the line its own ground (a card,
  a solid band or a scrim strong enough for WCAG AA), never text straight on a
  busy image.
- **Build, don't place**: a line arrives phrase by phrase at the event times
  in the plan's timing table. The line's layout is fixed from the start (the
  later phrases hold their place, invisible), so nothing reflows. The ground
  (card, band) fits what has landed and grows with each phrase: a big card
  with one word on it reads as broken, worst on frame 0. On a flat, calm
  background a line may have no ground at all. Each phrase enters fast
  (0.25–0.35 s) with a small rise and a slight overshoot; a phrase that is
  already on screen does not move again.
- **Fit the text, space the lines**: every line and its ground are only as
  wide as their text (`width: fit-content`), so the breathing scale never
  pushes a full-width block into the side bands. Lines stacked as separate
  blocks sit at least 1.25 × the font size apart, or `check` reports
  `content_overlap`.
- **Accent**: the marked key phrase gets a marker in the project's accent
  colour behind it (the same contrast rule as the caption highlight: the text
  on the marker meets WCAG AA), landing one beat after the line is complete.
  Only the one phrase; never colour whole lines.
- **Never static**: while a line holds, its ground breathes slowly (a scale
  drift of 2–3 % over the hold) and the product under it keeps moving
  (camera drift, push or pan). Out fast (≤ 0.15 s) or on a cut.
- **The product answers the words**: when a line names something the product
  shows (a filter, a price, a distance, a badge), that element does its thing
  on the same beat: pops in, fills, pulses, gets tapped. The video's events
  come from the product, not from decoration.
- **Keywords**: none beyond the beats; the beat line is the keyword.

## Captions (with `--voice`)

Source: `assets/caption-groups.json` from step 3. Render the groups as given:
one group on screen at a time, the active word highlighted from its `start`,
a hard kill at the group's `end`. Do not regroup or respell.

Three styles; `--captions`, else the profile's, else `editorial`. All three
sit inside the safe box. Fonts are ones Hyperframes bundles (render offline,
deterministic): pick the pair that fits the project's identity, or the
project's own font if it is embedded with `@font-face`.

| Style | Look | Place |
|---|---|---|
| `editorial` (default) | Condensed bold uppercase (e.g. Oswald 700, ~70 px) in the project's dark colour on a white card (small radius, soft shadow); active word marked | Left-aligned, x 120–780, **bottom-anchored at y ≈ 1230** so a second line grows upward, never into the bottom UI band |
| `pill` | Heavy geometric sans (e.g. Montserrat 900, ~60 px) in white on a pill in the project's dark colour; active word in the accent | Centred at the top of the safe box (y ≈ 300) |
| `outline` | Heavy display (e.g. Archivo Black, ~76 px) in white with a thick dark stroke; active word in the accent | Centred, above y 840 (y ≈ 700) |

**Active-word highlight must pass contrast.** Many brand accents (orange,
yellow, light green) fail against white (an orange #f5a623 on white is
2.0:1). Then mark the active word with an accent **background** behind the
dark text instead of accent-coloured text. `check` reports contrast per word;
zero contrast warnings on text is part of the gate.

**Screen-text keywords** (with `--voice`: the hook's screen text and later
keyword chips):
bold uppercase chip in the accent on the project's dark colour, placed where
the caption style is not (editorial: top-left of the safe box; pill: low-left;
outline: top-centre). A keyword never shows the same words the voice or the
caption is saying at that moment; a brand name appears after the voice has
said it, in the tail.

## composition-brief.md

```markdown
# Hyperframes composition brief: <slug>

## Objective
A <n>-second vertical <format> video for TikTok / Instagram Reels / Facebook
Reels that lands one idea: "<the one idea>".

## Output
- Composition: `composition/`
- Canvas: 1080×1920, 30 fps. Duration: <voice end + tail> s.
- Renders: `<slug>-nomusic.mp4` and (when a track exists) `<slug>-music.mp4`
  from this composition. The music bed is one `<audio>` that is switched off
  alone with `data-hidden` for the -nomusic render.

## Clock
No voice: the measured beat table (reading floors). With `--voice`:
`assets/voiceover.wav` at 0, volume 1, its own track; the `<audio>`
`data-duration` equals the file's length.

| Beat | Start | End | On screen (material + source range, or recreated scene) | Text |
|---|---|---|---|---|

## Text
No voice: screen-story lines — font <font>, size, zone, ground, colours,
accent marker colour; the phrase and accent times per line from the plan's
timing table.
With `--voice`: captions from `assets/caption-groups.json`; style <style>;
font <font>; colours <dark>/<white>/<accent>; highlight <text colour | marker>.

## Safe box (hard constraint for overlay text)
x 120–960, y 270–1248; below y 840 only x ≤ 780. Captions, keywords and
overlay copy never carry `data-layout-allow-caption-zone`; only the container
of recreated product imagery (the UI mock the camera moves over) may, and the
detail the voice points at is framed inside the box.

## First frame and cover
- t = 0 fully composed: image, the hook line, a sound (the voice's first word
  ≤ 0.15 s with `--voice`, else an SFX hit).
- Cover: <beat + moment>, settled, no caption on screen, title inside
  y 240–1680.

## Material
<files, what each shows, ranges; burned-in text and how it is hidden;
recreated scenes and their source files>

## Visual identity
<colours, fonts, look from the profile>. Avoid purple-blue gradients,
gradient text, emoji, glassmorphism, coloured card borders, three-icon rows,
Inter-only typography, grain on gradients.

## Motion
No voice: an event about every second beat (phrase, accent, re-frame or
product event), camera drift through every hold, the events list from the
timing table. With `--voice`: pattern break ≤ 3 s, camera moves on the words
the voice points at. Both: overlays in fast (0.2–0.35 s); reading floors
label ~0.8 s, sentence ~0.3 s per word. Pace per the profile's taste.

## Audio
No voice: music <file or none> as the bed · SFX on the cuts and text arrivals
· clip sound <level>. With `--voice`: voice 1.0 · music ducked under it
(audio.md) · SFX <posture>.
```

## Build and check

1. Load the Hyperframes domain skills listed in `SKILL.md` step 4 and build.
2. `npx hyperframes lint` until clean (structure warnings included).
3. The gate:

```bash
cd <out>/composition && npx hyperframes check
<skill-dir>/scripts/safezone_check.sh <out>/composition
```

`safezone_check.sh` runs `check --caption-zone` once per forbidden band (top,
bottom, left, right, TikTok action column; `--caption-zone` audits one band per
run) and fails on any text inside one. It audits every text element in the
DOM, including product UI text inside a recreated screen, text that is clipped
or off-screen, and text at opacity 0. So:

- Overlay text (captions, keywords, headlines, CTA copy): fix by moving it.
  Never waive.
- Recreated product imagery (a phone or browser mock, a card, a dashboard) is
  a picture of the product: its incidental text may pass through a band while
  the camera moves. Put `data-layout-allow-caption-zone` on that imagery's
  **outermost container only**, and check in the snapshots that whatever the
  voice points at (a name, a price, a button) sits inside the safe box when it
  is mentioned.

4. **Look at it.** `npx hyperframes snapshot composition --at <t1,…>` at the
   hook (0 and ~1 s), every beat's midpoint, the longest caption group and the
   tail. Check: first frame complete, no two texts overlapping or saying the
   same thing, captions on one line, burned-in text hidden, the product
   readable. Fix and re-run the gate. **After any edit, re-snapshot every
   beat's midpoint and both ends of every transition**, not only the beat you
   changed: a change in one place (a stacking order, a shared class) can break
   another beat.

## Self-review

- [ ] No voice: every text beat is big, on its own ground, built phrase by
      phrase on the beat and holds both reading floors (step 3 A); nothing on screen stands still for more than ~2 beats. With `--voice`: captions come from `caption-groups.json`
      unchanged; one caption track.
- [ ] t = 0 carries image + hook line + sound.
- [ ] Every beat shows its planned material; at most one graphic-only beat.
- [ ] Anything that differs by beat is set on the timeline at that beat; the
      last round of snapshots covered every beat, not just the last edit.
- [ ] Recreated scenes are light and airy unless the project's identity is dark;
      no black empty states.
- [ ] No keyword repeats what the voice/caption says at that moment.
- [ ] Music is one `<audio>` that can be hidden alone.
- [ ] `check`: zero errors, zero text-contrast warnings; `safezone_check.sh`
      clean (the only waiver: the recreated-imagery container); snapshots
      looked at.
