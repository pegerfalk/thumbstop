# Audio

Inherited from `/brag` (MIT) and re-weighted for voiceover. The order of
importance is fixed: **voice > SFX > music**. Nothing may mask a word.

All SFX are CC0 (Kenney.nl + an OpenGameArt keypress set) and ship with the
skill. Music does **not** ship with the skill (see "Music" below): the
`-music` export uses a track the user supplies or has downloaded once.

## Tracks

- **Voice** (with `--voice` only, `assets/voiceover.wav`): its own track,
  full level, starts at 0, already processed (`process_voice.py`, −14 LUFS).
- **SFX**: their own tracks, one track per overlapping sound.
- **Music**: its own track, switchable off alone, because step 5 renders a
  `-nomusic` export from the same composition. Trending audio is added in the
  app on top of `-nomusic`.

Without a voice the music is the main sound, not a bed: play it near full
level (≈ 0.9; measured 2026-09-24: brag's 0.38 left a voiceless export at
−23.9 LUFS, far below a feed's −14) and let SFX mark the cuts and text
arrivals. Brag's "never above 0.5" applies only under a voice. The `-nomusic`
export then carries only SFX: it is meant for adding a trending sound in the
app.

## Levels (craft defaults, inherited from brag and adjusted)

| Layer | Level | Notes |
|---|---|---|
| Voice | 1.0 | Never automated down. |
| Music under the voice | 0.12–0.15 | brag's duck level; one flat level for the whole voiced part (or the hyperframes-audio carve), never a hand-drawn dip per sentence. |
| Music before the first word / after the last | 0.30–0.40 | Only in gaps longer than ~0.8 s and in the tail; never above 0.5. |
| SFX under the voice | 0.40–0.60 | Prefer placing SFX in the gaps between sentences. |
| Clip sound (footage's own audio) | 0.30–0.40 | When the material carries its own SFX bed, keep it under the voice and add nothing on top. |
| SFX in gaps / on the payoff | 0.55–0.85 | Softer for calm profiles. |

## SFX posture

Fewer than brag. A voiced video already has a rhythm; SFX mark **real motion**
only: a card landing, a page turning, a cut on the payoff. Typical density:
one cue per beat at most, three to six in a 30 s video. No typing sounds under
speech. When the real material already carries its own SFX bed (product
renders often do), prefer that bed and add nothing on top of it.

Always consult `assets/sfx/sfx-analysis.md` (it is the complete list,
including files the tables below leave out) and prefer low/medium
high-frequency-risk files: bright, clicky sounds fight the consonants of the
voice.

## Asset paths

Copy only what is used into the composition; reference it relative to
`composition/`. Never use absolute paths.

```bash
mkdir -p <out>/composition/assets/sfx/<family> <out>/composition/assets/music
cp <skill-dir>/assets/sfx/<family>/<file> <out>/composition/assets/sfx/<family>/
cp "<music track>" <out>/composition/assets/music/
```

## SFX library — approved files

The family SFX (casino, impact, interface, ui) live directly under `sfx/`; the individual keypress set lives in `sfx/keyboard/`.

Read `sfx-analysis.md` before choosing files — it lists safer picks by use case and flags files with high-frequency risk. Prefer low/medium HF risk for polished and repeated moments; reserve high-risk files for tiny isolated accents or chaotic tones.

### `keyboard/` — Individual keypress sounds

32 CC0 single keypress WAV files (`keypress-001.wav` through `keypress-032.wav`). Each is a distinct key sound at a slightly different velocity and character. Use these for per-character typing animations — randomize across the set so repeated characters don't sound robotic.

**Source:** [Keyboard Soundpack #1](https://opengameart.org/content/keyboard-soundpack-1-typing-and-single-keystrokes) by unicae_games — CC0

### `interface/` — UI sounds

| Files | Character | Use for |
|---|---|---|
| `click_001–005.ogg` | Sharp, precise | Button tap, CTA, any tap action |
| `glitch_002.ogg`, `glitch_004.ogg` | Digital distortion | Tech/AI moment, chaotic accent |
| `error_005–006.ogg` | Negative buzz | Comedic fail, wrong answer |
| `switch_001–002.ogg`, `switch_004–007.ogg` | Toggle switch | Feature switching on, binary state |
| `drop_001–003.ogg` | Soft drop | Element landing, gentle placement |
| `bong_001.ogg` | Deep bell | Dramatic announcement — use sparingly |
| `select_008.ogg` | Selection click | Navigation, item focus |

### `impact/` — Impact sounds

More physical and cinematic. Excellent for big moments and transitions.

| Files | Character | Use for |
|---|---|---|
| `impactSoft_medium_000–004.ogg` | Medium soft thud | Major reveal, hard transition — safest family |
| `impactSoft_heavy_000–004.ogg` | Heavy soft thud | Comedic bonk, weight, silly moment |
| `impactBell_heavy_000.ogg`, `_003.ogg`, `_004.ogg` | Deep resonant bell | Cinematic reveal, logo slam, dramatic moment |
| `impactPunch_heavy_000–004.ogg` | Heavy punch | Aggressive beat, chaotic tone |
| `impactPunch_medium_000–004.ogg` | Medium punch | Impact emphasis |
| `impactWood_light_000–004.ogg` | Light wood knock | Warm, organic tap |
| `impactWood_medium_000–004.ogg` | Wood knock | Warmer accent |
| `impactWood_heavy_000–004.ogg` | Heavy wood hit | Cinematic weight |
| `impactPlank_medium_000–004.ogg` | Plank slap | Comic physical moment |
| `impactPlate_heavy_000–004.ogg` | Metal plate slam | Big hit, aggressive |
| `impactPlate_light_000–004.ogg` | Light metal plate | Notification, crisp accent |
| `impactPlate_medium_000–004.ogg` | Medium plate | Mid-weight accent |
| `impactTin_medium_000–004.ogg` | Tin can hit | Quirky, lo-fi moment |
| `impactGeneric_light_000–004.ogg` | Generic light hit | Versatile small accent |
| `impactMetal_medium_000–004.ogg` | Metal tap | Medium accent |
| `impactMetal_heavy_000.ogg`, `_002.ogg`, `_004.ogg` | Heavy metal clang | Aggressive hit |
| `impactMetal_light_002–003.ogg` | Light metal ping | Small notification |
| `impactGlass_light_001–003.ogg` | Light glass clink | Sparkle, delicate achievement |
| `impactGlass_medium_000.ogg`, `_002.ogg`, `_004.ogg` | Glass tap | Mid-weight accent |
| `impactGlass_heavy_002.ogg` | Glass shatter | Chaotic hit |
| `impactMining_001.ogg` | Mining strike | Industrial, heavy |

### `casino/` — Card and chip sounds

Specific but great for swipe/deal/stack moments.

| Files | Character | Use for |
|---|---|---|
| `card-slide-1–8.ogg` | Card sliding | Swipe action, content sliding in |
| `card-place-1–4.ogg` | Card placement | Item landing, card appearing |
| `card-fan-1–2.ogg` | Cards fanning | Multiple items appearing in sequence |
| `card-shove-1–4.ogg` | Card shoved | Forceful card motion |
| `card-shuffle.ogg` | Shuffle | Transition with motion |
| `chip-lay-1–3.ogg` | Chip placed | Metric placed/confirmed |
| `chips-stack-1–6.ogg` | Chips stacking | Counter incrementing, stacking animation |
| `chips-collide-1–4.ogg` | Chips clinking | Celebratory, success with weight |
| `chips-handle-1–4.ogg`, `chips-handle-6.ogg` | Chips handled | Casual chip movement |
| `dice-shake-1–3.ogg` | Dice shaking | Build-up, anticipation |
| `dice-grab-1–2.ogg` | Dice grabbed | Pick up, quick action |
| `dice-throw-1–3.ogg` | Dice thrown | Chaotic/random moment |
| `die-throw-1–4.ogg` | Single die thrown | Lighter random accent |
| `cards-pack-open-1–2.ogg` | Pack opening | Reveal, product launch moment |

### `ui/` — Clicks and switches

| Files | Character | Use for |
|---|---|---|
| `click1–5.ogg` | Various click tones | Button tap, cleaner than interface clicks |
| `mouseclick1.ogg` | Mouse click | Simulated cursor interaction |
| `rollover1–2.ogg`, `rollover4–5.ogg` | Hover/rollover | Subtle hover feedback, very soft accent |
| `switch1–38.ogg` (most variants) | Switch variants | Toggle, mode change — pick by character |

---

## Moment → sound heuristics

Use these as examples for Hyperframes, not a fixed recipe. Sound should reinforce the edit, not call attention to itself.

| Moment type | Good sound families | Notes |
|---|---|---|
| Sequential cards/items opening | `casino/card-slide-*`, `casino/card-place-*`, `casino/card-fan-*`, `interface/drop_*` | Match the gesture. A card stack uses card sounds; a soft product grid can use drop sounds. For dense sequences, accent the first, last, or rhythmically important items only. |
| Big reveal / payoff | `impact/impactBell_heavy_000`, `_003`, or `_004`, `impact/impactSoft_medium_*`, `interface/bong_001` | One short announcement-style cue when the reveal lands. Keep it brief. |
| Text popping / typed copy | `keyboard/keypress-*.wav` (randomized), `interface/drop_*` | For per-character typing animations, pick a random file from `keyboard/` for each character. For soft label pop-ins, use `drop_001` or `drop_002`. Thin out or skip when copy is dense. |
| Simulated user action | `interface/click_*`, `interface/select_008`, `interface/switch_*`, `ui/mouseclick1`, `ui/switch*` | Use interaction sounds when the video shows a cursor, tap, button, toggle, swipe, or selection. Match the visible action. |
| Success / completion | `impact/impactBell_heavy_000`, `_003`, or `_004`, `casino/chips-collide-*` | Positive accent for approvals, matches, metrics, completed flows, or final CTAs. |
| Chaotic or comedic beat | `interface/glitch_002`, `interface/glitch_004`, `interface/error_005–006`, `impact/impactPunch_heavy_*`, `casino/dice-throw-*` | Reserve louder or weirder cues for tones that can handle them. |

When in doubt, pick fewer cues with better timing. Prefer a coherent sonic palette for the whole video over a grab bag of cute sounds.

---

## Timing rules

These rules apply when Hyperframes is implementing the composition and the motion timings are known:

- Align SFX to the **start** of the animation, not the end
- Entry pop: 0.0–0.1s before the element's first visible frame
- Transition: at the transition start time
- Success ding: at the moment the metric/stat is fully visible
- For staggered elements: usually accent the first, final, or strongest beat; only score every item when that rhythm is intentional and still feels clean

- Under the voice: land SFX in the gap after a word, not on a stressed syllable.

Composition notation:
```
Beat 3 — "The scene keeps going, past every edge." — 6.15–10.17 s
  sheet grows sideways at 6.20 s   →  (material's own paper-slide bed carries it)
  hard cut to the full page 9.90 s →  SFX: impact/impactSoft_medium_001 at 9.88 s, 0.45
```

---

## Music

### Where the track comes from

In this order:
1. `--music <file>`: the user's own track (they are responsible for its licence).
2. A downloaded ende.app track (below) in `~/.cache/thumbstop/music/` or
   `<skill-dir>/assets/music/`.
3. None: render only `-nomusic` and tell the user how to add music.

The recommended tracks are five "Happy Beats & Business Moves" pieces by
Sascha Ende, **CC BY 4.0 with attribution optional**, commercial use including
ads and TikTok allowed (`assets/music/LICENSE-music.md`). ende.app hands out
files through its own download page (daily limits apply), so the skill never
scrapes it; the user downloads a track once from its song page, keeps the file
name below, and every later run finds it.

| File name to keep | Song page | Length | Tempo | Character |
|---|---|---|---|---|
| `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` | [song 12866](https://ende.app/en/song/12866-happy-beats-business-moves-vol-1) | 2:44 | 120.2 BPM | Full upbeat, most energetic |
| `happy-beats-business-moves-vol-9-by-ende-dot-app.mp3` | [song 12874](https://ende.app/en/song/12874-happy-beats-business-moves-vol-9) | 1:54 | 114.8 BPM | Mid-energy, laid-back |
| `happy-beats-business-moves-vol-10-by-ende-dot-app.mp3` | [song 12875](https://ende.app/en/song/12875-happy-beats-business-moves-vol-10) | 1:00 | 110.0 BPM | Compact, punchy |
| `happy-beats-business-moves-vol-11-by-ende-dot-app.mp3` | [song 12876](https://ende.app/en/song/12876-happy-beats-business-moves-vol-11) | 1:28 | 114.8 BPM | Warm, business-like |
| `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` | [song 12881](https://ende.app/en/song/12881-happy-beats-business-moves-vol-12) | 1:58 | 110.0 BPM | Steady and clean (calm projects) |

Choose by the project's pace: calm projects take vol-12 or vol-11. The track
must be longer than the video; start it at a musical phrase, not mid-bar (the
cue file's beat grid shows where). Credit line when used (optional, cheap
insurance): "Music: Happy Beats & Business Moves Vol. N by Sascha Ende,
ende.app (CC BY 4.0)".

### Ducking

A flat duck under the whole voice is the baseline: a `data-automation` volume
lane on the music `<audio>` at 0.12–0.15 while the voice runs, 0.3–0.4 before
the first word and in the tail, fading out at the end. The hyperframes-audio
voiceover carve is better when the project can install `@hyperframes/core`
locally (`npm i -D @hyperframes/core` in the composition); ask before
installing anything.

### Beat sync (optional, light)

A voiced video is timed by the voice, not the music. Use cues only to nudge
**cuts that already fall between sentences** onto a nearby beat (±0.10 s),
and at most one payoff moment onto a strong cue (±0.15 s). Never move a
voice-timed beat to hit the music.

Cue sources, richest first:
1. Bundled presets: `<skill-dir>/assets/music/cues/<track-stem>.music-cues.json`
   (full track) and `.md` (first 25 s summary).
2. `npx hyperframes beats <out>/composition` (no Python) — beat grid with
   per-beat strength.
3. `analyze_music_cues.py` via `uv run --project <skill-dir>/scripts` —
   pulls librosa etc. from PyPI into a local venv; that is an install, so ask
   the user first.

### Licence in practice

- Never register a track with YouTube Content ID, Meta Rights Manager or any
  similar system (the author's explicit no-go).
- A wrongful claim: dispute it citing https://ende.app/en/standard-license,
  and fall back to the `-nomusic` export.
- Credit is optional; when there is room, the post text may carry
  "Music: <track> by Sascha Ende, ende.app (CC BY 4.0)".
- Boosted as an ad: use `-nomusic` (Meta advises against licensed music in ads).
