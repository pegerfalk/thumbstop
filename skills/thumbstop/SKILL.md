---
name: thumbstop
description: Turn the current project into a short vertical video that stops the scroll — for TikTok, Instagram Reels and Facebook Reels. Reads the project directly (code, docs, media), finds the one idea worth saying, and builds a hook-first video from the project's own words and visuals; with --voice it also narrates it (local Kokoro voice) with word-timed captions. Renders exports with and without music, a cover and post texts per platform. Use when someone says "/thumbstop", "make a TikTok/reel about this", "explain this in a video", or wants a social video for their product. Built on Hyperframes; never publishes anything.
---

# /thumbstop

A short vertical video that stops the thumb in the first second and lands one
idea, readable on every platform's UI. By default it has **no voice**: the
on-screen text and the pictures carry it, so both have to stop the scroll on
their own. With `--voice` it **talks**: a punchy local voiceover with
word-timed captions. Fork of `/brag` (MIT, Shunit Haviv Hakimi), rebuilt for
vertical social video.

`/thumbstop` owns **what**: the angle, hook, script, storyboard, the truth of
every claim, the voice, caption policy, safe zones and delivery. Hyperframes
owns **how**: composition structure, animation, caption rendering, mixing and
render. Never write GSAP snippets or HTML templates into this skill or its
briefs; the brief describes, Hyperframes implements.

## Invocation dispatch

Parse the whole invocation first. Everything that is not a flag is the
**brief** (optional). With no brief, `/thumbstop` decides the angle itself
from what it reads, the way `/brag` does.

```
/thumbstop
/thumbstop what makes the export feature different
/thumbstop --format listicle three things people get wrong about X
/thumbstop --format objection "why not just use the free version?" --hook doing-it-wrong
/thumbstop --voice
/thumbstop --voice am_michael --captions pill
```

| Option | Values | Default |
|---|---|---|
| `--format` | `explainer`, `process`, `story`, `listicle`, `objection`, `showcase` | inferred |
| `--hook` | a hook type from `references/hooks.md` | best of three, chosen in step 2 |
| `--duration` | seconds (hard max 180) | per format |
| `--channel` | where the viewer acts (e.g. `webshop`, `app-store`), or `none` | inferred from the project |
| `--voice` | flag, or a Kokoro English voice id: add a voiceover | **off** (no voice); bare `--voice` = `af_heart` |
| `--speed` | Kokoro speed multiplier (with `--voice`) | `1.1` |
| `--captions` | `editorial`, `pill`, `outline` (with `--voice`) | the profile's, else `editorial` |
| `--music` | path to an audio file for the music export | a bundled-cue track if downloaded (see `references/audio.md`) |
| `--profile` | path to a project profile | reuse `thumbstop-profile.md` or the last run's |
| `--no-sfx` | flag | SFX on |
| `--segments` | flag: also cut the render into 3 clips at hard cuts | off |
| `--review` | flag: stop after the script and let the user pick the hook | off; **on for a first run** (no profile yet) |
| `--no-review` | flag: skip the first-run stop | off |
| `--preview` | flag: stop at the preview before rendering | off |

By default a run has **no stops**: it goes from reading the project to the
finished files, then reports what it made and offers re-rolls. The one
exception is a **first run** in a project (step 1 finds no profile): it stops
once after step 2 to show the three hooks, the script and the material list,
because a wrong guess about what may be used or claimed throws the whole run
away. Later runs reuse the profile and go straight through. `--no-review`
skips the first-run stop.

## Output

`thumbstop-output/<YYYY-MM-DD>-<slug>/` in the working directory; if it
exists, suffix `-2`, `-3`.

```
<slug>-nomusic.mp4    SFX (+ voice with --voice); add trending audio in the app
<slug>-music.mp4      the same + a music bed (only when a track is available)
cover.jpg             the poster, also baked in as frame 0 of the exports
tiktok.txt · instagram.txt · facebook.txt
profile.md            what was learned about the project (reused next run)
thumbstop-plan.md · composition-brief.md · material/ · voice/ · composition/
segments/             only with --segments
```

## Skill directory

`<skill-dir>` is the directory holding this file (printed as "Base directory
for this skill" when it loads). Assets live in `<skill-dir>/assets/`, scripts
in `<skill-dir>/scripts/`. Never guess an install path.

## Requirements

Node 22+ with `npx hyperframes` (always the latest release), `ffmpeg`, and
Python 3 (the scripts are stdlib only). Kokoro and whisper models are fetched
by Hyperframes on first use. Check with `npx hyperframes doctor`.

---

## Step 1 — Inspect the project

**Read:** [references/step-1-inspect.md](references/step-1-inspect.md),
[references/profile-template.md](references/profile-template.md),
[references/formats.md](references/formats.md).

Read the project the way `/brag` does, plus its media and its owner's taste
rules. Decide the one idea, the format and the channel; collect only
**sourced** facts; choose the real material.

**Gate:** `<out>/profile.md` exists, the 10-question rubric is answered, every
fact has a source, the material is copied into `<out>/material/`.

## Step 2 — Hook, script, storyboard

**Read:** [references/step-2-script.md](references/step-2-script.md),
[references/hooks.md](references/hooks.md).

Hook first: write three, pick the strongest by the rules in hooks.md. Then the
script: without a voice, the **screen story** (the sequence of on-screen text
beats, each short enough to read at a glance); with `--voice`, the spoken
script in two strings (screen text and TTS text). Then the storyboard in
beats. Verify every claim. Write `<out>/thumbstop-plan.md`.

With `--review`, and on a first run: stop here, show the three hooks, the
script and the material list (what will be shown, and what was left out and
why), and let the user choose and edit.

**Gate:** the plan exists, the script fits the word budget, every claim is
verified against its source.

## Step 3 — Timing

**Read:** [references/step-3-timing.md](references/step-3-timing.md).

Without a voice, reading time sets the clock: each text beat holds for its
reading floor, the music's beat grid nudges the cuts. With `--voice`: Kokoro
TTS → transcribe the raw take → `align_captions.py` → `process_voice.py`
(tight pauses, punch, −14 LUFS, word times remapped) → `group_captions.py`;
the voice sets the pace.

**Gate:** a measured beat table in the plan that
`<skill-dir>/scripts/check_timing.py <out>/thumbstop-plan.md` passes (no voice). With `--voice` also
`voice/words.json`, `sentences.json`, `caption-groups.json`, the aligner exits
0 (brand words heard right) and the first word starts within 0.15 s.

## Step 4 — Compose

**Read:** the Hyperframes domain skills `hyperframes-core`,
`hyperframes-animation`, `hyperframes-creative`, `hyperframes-keyframes`,
`hyperframes-studio`, `hyperframes-audio`, `hyperframes-cli`, and the captions
guide in `media-use`. `/thumbstop` is its own workflow: do not enter the
`hyperframes` entry-point intent interview or route into one of its workflows.
**Read:** [references/step-4-compose.md](references/step-4-compose.md),
[references/platforms.md](references/platforms.md),
[references/audio.md](references/audio.md).

Write `<out>/composition-brief.md`, then build `<out>/composition/` with
Hyperframes: 1080×1920 at 30 fps; screen text, SFX and music (and with
`--voice`: voice and captions) on separate tracks.

**Gate:** `npx hyperframes check` passes with zero errors and zero contrast
warnings on text, `<skill-dir>/scripts/safezone_check.sh <out>/composition` is
clean, and key frames have been looked at (snapshot).

## Step 5 — Deliver

**Read:** [references/step-5-deliver.md](references/step-5-deliver.md).

Render the exports, pick the cover, bake it in as frame 0, write the three
post texts with their upload checklists, then open the finished video for the
user. With `--preview`: start the preview first and wait for a go.

**Gate:** the exports pass `ffprobe` (1080×1920, 30 fps, H.264 + AAC), the
cover is frame 0, three texts are written, the video is open (or its path
given when there is no desktop).

---

## Laws

These hold for every format. Formats and hooks adapt everything else.

**Thumb-stop first.** In the first second the layers land together: an image
that breaks the feed's pattern, words on screen, and a sound (the voice's
first word with `--voice`; otherwise a hit on the first cut). No logo, no
intro, no "hey guys". The product or its visual promise is on screen by 1.5 s.

**One idea.** One video, one claim, one payoff. The rest is another video.

**The words are the spine.** Script before visuals. Without a voice, the screen
story is the script: every beat is a line worth stopping for, big enough to
read at a glance and held long enough to read. With `--voice`, the voice sets
the timing and screen text is a keyword or number that adds to it, never the
same words at the same moment.

**Never a still frame.** Something changes about every second beat: a phrase
lands, a key word is marked, the camera re-frames, the product does
something. Without a voice, lines build phrase by phrase on the music and the
camera drifts through every hold; with one, the words drive the cuts. Pace
comes from motion, never from pulling text off before it can be read.

**Readable everywhere.** Captions and screen text stay inside the common safe
box (x 120–960, y 270–1248; x ≤ 780 below y 840); recreated product imagery
may cross it, but what the voice points at is framed inside it. A text line holds at least
its reading floor: ~0.8 s for a short label, ~0.3 s per word for a sentence.
Text meets WCAG contrast against whatever sits behind it.

**Show the real thing.** Every video shows the real product (step 1's four
tiers), and the material matches the channel. No abstract filler, no
stock-looking decoration. The owner's finished videos (edited, published,
already a post) are their work, not material: never re-cut them unless the
profile says so.

**True or cut.** Every number and claim traces to a source in the plan. Never
invent or round up a figure. Of the true numbers, show the one that flexes:
the biggest total that fits (the whole shop's sales, not one item's), with its
unit written out (units, orders, buyers: whatever the source counts), rounded
down with a "+" when it is a live count. A number's scope matches the picture:
a shop-wide number over the whole range, a product's number over the product. Selling copy lifts strengths and carries no
self-inflicted hedges; required disclosures live in the post texts and the
platform settings, not in the voice.

**No defaults.** No generic SaaS language ("streamline", "unlock", "elevate"),
no purple-to-blue gradients, gradient text, emoji headlines, glassmorphism,
three-icon rows, or em-dash-riddled copy. The palette and type come from the
project's own identity. Recreated scenes default to light and airy: white or
pale grounds, soft layered shadows, rounded corners, pale empty states (never
a black hole); dark grounds only when the project's own identity is dark.

**Drafts only.** Render files and write texts. Never upload, schedule or post.
