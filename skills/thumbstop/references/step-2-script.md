# Step 2: Hook, script, storyboard

Write `<out>/thumbstop-plan.md`: the contract every later step obeys. It
specifies what the viewer hears, reads and sees, and in what order. It does
not prescribe Hyperframes implementation.

## 1. Hook first

Read `references/hooks.md`. Write **three** hook options, from at least two
different hook types. Each option has all three layers:

```
Hook A — <type>
  Hook line:             "…"          (no voice: the big line on frame 0, 2–7 words)
  Voice (first words):  "…"          (with --voice only)
  Screen text:           "…"          (with --voice: ≤ 5 words, not the voice's words)
  First frame:           what is on screen at t = 0 and why it breaks the feed
```

The first frame is not a title card. It is product, motion or contrast.

Without a voice the hook is two layers plus a sound: the first frame and the
hook line (which now carries the words), and a soft hit on frame 0.

**Pick one** unless `--hook` or `--review` decides. Score each option:

- Does the first frame alone stop a scroll (motion, contrast, the product
  doing its most surprising thing)?
- Is the promise specific to this project (would it work for any product? then
  it loses)?
- Is it fully sourced (a hook claim needs a provenance row)?
- Does the video deliver it by the payoff beat?
- Is the screen text different from the voice line?

Take the highest; on a tie, the one whose first frame is strongest. Keep the
other two in the plan: they are the first re-roll to offer.

## 2. The screen story (no voice, the default)

Without a voice, the on-screen text *is* the script. Write it as a sequence of
**text beats**, one line per beat, each a line worth stopping for:

- 2–7 words per beat; one idea per beat. A number, a name or a verb beats an
  adjective.
- Big: the line is the headline of its frame (in-feed viewing: ≥ 90 px), set
  in the project's display type, inside the safe box.
- Each beat holds for its reading floor (step 3): about 0.3 s per word, at
  least 0.8 s; the hook at least 1.5 s.
- Mark how the line builds: `/` between the phrases that land one at a time
  (1–4 per line, split where a reader would pause), and `*…*` around the one
  key phrase that gets the accent, if any. `Emotionally / available /
  *stallion.*` lands in three events and an accent; `He's 8.` lands in one.
- Vary the lengths: some one-phrase punches, some three-phrase builds. A run
  of same-shaped lines reads as a slideshow.
- The words and the picture work together: the line says what the picture
  alone cannot (the claim, the number, the turn), the picture proves it.
- Budget: a 25 s video fits about 8–11 beats. Too many beats means cut
  beats, never shorter holds.

The storyboard (section 5) is keyed to these beats.

## 3. Word budget (with `--voice`)

Speech rate is measured, not guessed (Kokoro via Hyperframes, 2026-09-24,
after `process_voice.py`, which tightens the pauses):

| Voice | Speed | Words per second |
|---|---|---|
| `af_heart` (default with `--voice`) | 1.1 | 3.4 |
| `am_michael` | 1.1 | ≈ 3.2 |
| `am_fenrir`, `am_puck` | 1.1 | ≈ 4 (fast) |
| other voices | | generate one sentence first and measure |

Budget = target seconds × rate × 0.95. A 30 s `af_heart` video ≈ **95 words**.
Over budget → cut words, never speed the voice up further.

## 4. Two strings (with `--voice`)

The script is written twice, word for word the same except spelling:

- **Screen text** (`<out>/voice/script.txt`): correct spelling, punctuation
  and capitals. Captions are made from this.
- **TTS text** (`<out>/voice/script-tts.txt`): the same words spelled for
  Kokoro. Apply the profile's pronunciation list. Accented letters are a known
  trap: Kokoro read `Pokémon` wrong in every voice tested and `Pokemon` right.
  Numbers: if Kokoro reads a figure wrong, spell it as it should be said,
  hyphenated into one token (`$7.50` → `seven-fifty`), and keep the screen
  string as the viewer should read it.

The two files must have the **same number of words in the same order**; the
aligner maps one to the other word by word. If a respelling needs two words
("Poke mon"), hyphenate it instead ("Poke-mon"). A name written as one word on
screen but said as two ("AcmeStudio") is hyphenated in the TTS text
("Acme-Studio"); the aligner accepts the different word split.

## 5. Script rules

- The first sentence is the hook's voice line. It lands in the first second.
- Short sentences. One clause each where possible; Kokoro reads long
  sentences flat.
- Concrete over adjectives: a number, a named thing, a visible action.
- **Show the number that flexes.** A stranger reads a number in half a
  second with no context, so it must be both big and plain about what it
  counts. A count for one item (`38 sold` on one mug) reads as small, and the
  viewer can't tell what it counts. Use the biggest true total that fits the
  claim: the whole shop, catalogue or user base (`1,200+ mugs sold`), and keep
  the per-item count as a supporting detail at most. If the only true number
  is small, cut it and prove the point another way (a review, the result on
  screen).
  - **Say what it counts.** Units, orders, buyers and "times" are different
    numbers: a sum of quantities is units, not orders. The word in the line
    matches what the source counts.
  - **Round down, with a "+".** A live count keeps moving between render and
    post: `1,200+` for 1,243 stays true; `1,243` may not. Never round up.
  - **The scope matches the picture.** A shop-wide number over one product
    reads as that product's number. Show the whole range (pull back to the
    catalogue, a fan of products) when the number is the shop's; show the
    product when the number is the product's.
  - A strong shop-level number makes a good **proof close** (formats.md):
    the total and its reach, then the price or the call to action.
- With `--voice`, the voice never reads the on-screen text; screen text names
  the keyword. Without a voice, every line must make sense read alone, in
  order, with the sound off.
- No hedges in the voice ("might", "kind of", "we think"). Required
  disclosures go to the post texts (step 5), not the script.
- End on the format's ending (formats.md): a loop back into the first frame,
  or one soft call to action. Never both, never "link in bio" as the last word
  of the voice.
- Banned: generic SaaS language, em-dash rhythm, emoji, "hey guys",
  "in this video", "let's dive in", "game-changer".
- Watch the wording traps the profile lists (e.g. never call a derivative work
  the original's "own" art; never say a physical product is a download).

## 6. Storyboard in beats

Beats are keyed to **text beats** (no voice) or **script sentences** (with
`--voice`), not seconds. Seconds are estimates until step 3 measures them.

```markdown
### Beat 2 — "Most people never see this part of the process."
- Sentence: s1 (est. 2.3–5.6 s)
- On screen: <real material + what it does>
- Screen text: "this part" (keyword, held ≥ 0.8 s settled)
- Events: <phrase landings, accent, re-frames, product events — about every second beat>
- SFX intent: <what the sound does, or none>
- Transition: <hard cut / match / soft> → Beat 3
```

Rules:
- No beat stands still: with no voice, list its events (step 3 A); with
  `--voice`, a beat longer than 3 s needs a cut or re-frame inside it.
- The payoff beat gets the most screen time after the hook.
- Every beat names its real material or says "graphic: <what>" — and at most
  one graphic-only beat per video.
- Screen text: 1–5 words, inside the safe box, never covering the captions.

## 7. Captions (with `--voice`; policy, not implementation)

State in the plan:
- Chunk size: 1–3 words per caption group (formats may tighten to 1–2).
- Active word highlighted.
- Caption band position: inside the safe box. Centred captions must sit above
  y 840 (the TikTok action column starts there); captions below y 840 must
  fit x 120–780. The profile may already record a choice.
- Caption style: `--captions`, else the profile's, else `editorial`
  (step-4-compose.md describes the three styles).

## 8. Post-text drafts

Draft one caption line per platform now (step 5 finishes them), in the
channel's post-text language: the hook restated as a line a viewer would send
to a friend, not a summary. A draft is only the caption's opening line;
disclosures, the CTA and hashtags are added in step 5, so their absence here
is not a defect.

## 9. Verify the claims

Before the stop, check every claim in the script, hooks, screen text and
post-text drafts against its source. If the `truth-checker` agent
is available (it ships with the Thumbstop plugin as `thumbstop:truth-checker`),
run it on `thumbstop-plan.md` with the profile's path; otherwise do the same
check yourself: each claim VERIFIED, or rewritten until it is. A claim that
is true for another channel than the video's is wrong here.

## thumbstop-plan.md structure

```markdown
# Thumbstop plan: <slug>

## The one idea
## Viewer
## Format: <format> — target <n> s — voice: none | <id> @ <speed>
## Hooks
(A, B, C, with scores — chosen: X)
## Script
### Screen story (no voice) — one line per beat, `/` phrases, `*accent*`
### Screen text + TTS text (with --voice)
Words: <n> / budget <n> — est. <n> s
## Storyboard
(beats)
## Captions
## Visual identity (from the profile)
## Audio direction (references/audio.md)
## Provenance
(table from step 1 — every spoken or shown claim)
## Channel: <id or none> — CTA and disclosures from the profile
## Post-text drafts
```

## With `--review`, and on a first run

Stop before the voice: show the three hooks (with first-frame descriptions and
scores), the full screen-text script, the word count, the estimated length,
and the material list: what will be on screen, and what was left out and why
(e.g. the owner's finished videos). Record the answers in the profile
(`Re-cut finished videos`, proof numbers, taste) so the next run needs no stop.
Ask which hook, and whether the script is approved. Apply edits to **both**
strings and re-verify changed claims. Without `--review` (and after the first
run), continue straight to step 3.
