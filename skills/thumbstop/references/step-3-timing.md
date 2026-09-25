# Step 3: Timing

Turn the storyboard into a measured beat table. Two modes:

- **No voice (default):** reading time is the clock.
- **`--voice`:** the processed voiceover is the clock.

## A. No voice: the music is the clock, reading time is the floor

Without a voice nothing on screen moves at the speed of speech, so the video
has to make that rhythm itself. A line that lands whole and then stands still
for three seconds reads as a slide; the same line built phrase by phrase on
the beat reads as someone talking. Every text beat is therefore split into
**events**, and events, not whole lines, are what get timed.

1. **Reading floors, two of them**: the line is on screen (first phrase to
   out) for at least `max(0.8 s, 0.3 s × words)`, and its **last** phrase
   holds at least `max(0.8 s, 0.3 s × its words)` settled before the line
   leaves. Earlier phrases are read while the rest arrives, the way captions
   are read while a voice talks. A number or a one-word punch line may sit at
   the 0.8 s floor.
2. **Phrases on the beat**: split each line into 1–4 phrases at its natural
   breaks (the ones the script marks with `/`, see step 2) and give each its
   own landing time on the music grid, one or two beats apart. The line's
   card or ground arrives with its first phrase.
3. **Accent a beat later**: a line with a key phrase (marked `*…*` in the
   plan) gets one more event: a marker on that phrase one beat after the
   line is complete. At most one accent per line; not every line has one.
4. **Varied lengths**: mix 2-, 4- and 6-beat lines. Short punch lines take 2
   beats; a line never sits longer than 6 beats. Three lines of the same
   length in a row is a metronome: change one.
5. **Something moves every ~2 beats** (~1–1.2 s at 100–120 BPM): a phrase
   lands, the accent lands, the camera re-frames, or the product does
   something (a UI element pops in, a row fills, a counter ticks). The camera
   never stands still between events: a slow drift or push runs through
   every hold. A beat longer than 3 s without an event is a failure.
6. **Hook**: the hook's first phrase and a sound are on screen at frame 0,
   and the complete hook line holds at least 1.5 s, measured from its first
   phrase.
7. **No music track**: use a 0.5 s grid (120 BPM) as the clock anyway, so
   events keep the same rhythm the SFX will follow.
8. **Music**: events sit on the track's beat grid within ±0.10 s; the payoff
   lands on a strong cue within ±0.15 s. Never shorten a reading floor to
   hit a beat: move the line out a beat later instead.
9. **Sound on frame 0**: the hook's arrival gets a soft hit (SFX), so the
   first second has sound even without music. Product events (a row, a tap,
   a match) get their small SFX on the same frame.
10. **Tail**: 0.8–1.5 s settled hold on the last beat (or the loop seam). The
    closing card builds on the beat too (headline, then the action, then the
    badges), and its last element is settled at least 0.8 s before the end.

Write the table into `thumbstop-plan.md` under `## Timing (measured)`:

```markdown
| Beat | Screen text (phrases / accent) | Words | Events (s) | Settled | Out | Beats |
|---|---|---|---|---|---|---|
| 1 Hook | "Emotionally / available / *stallion.*" | 3 | 0.00, 0.56, 1.09, accent 1.64 | 1.09 | 2.19 | 4 |
| 2 | "He's 8." | 2 | 2.19 | 2.19 | 3.27 | 2 |
```

`Settled` is when the last phrase has landed. Check each row:
`Out − first event ≥ line floor` and `Out − Settled ≥ last-phrase floor`; beats vary; no gap of more than
~2 beats between consecutive events across the whole table (camera moves
count; list them under the table).

Then run the arithmetic check; hand-counted words and floors slip:

```bash
python3 <skill-dir>/scripts/check_timing.py <out>/thumbstop-plan.md
```

It checks each row's word count against the screen text, both reading
floors, the hook's 1.5 s, the 6-beat maximum and every gap between events,
using the BPM named in the plan (else 120). Fix the table until it exits 0.

The total must land inside the format's range; too long means too many or too
wordy beats: cut, never speed up.

## B. With `--voice`: the voice is the clock

Facts behind this step (measured 2026-09-23 on Hyperframes 0.8.65):
Kokoro returns audio only, no word timings. `hyperframes transcribe`
(whisper `small.en`) gives per-word `start`/`end`; starts sit within ~0.05 s
of the real silence boundaries, ends stretch across pauses by up to ~0.6 s.
Whisper's spelling is a guess ("Pacaman", "center"), so captions take their
words from the script and only their times from the transcript.

### 1. Generate

```bash
npx hyperframes tts <out>/voice/script-tts.txt \
  --voice <voice> --speed <speed> \
  --output <out>/voice/raw.wav --json
```

Write the raw take to `<out>/voice/raw.wav`. Default
voice `af_heart` (Kokoro's best-rated voice), speed `1.1`. Any English Kokoro
id works (`af_*`, `am_*`, `bf_*`, `bm_*`), including ones `tts --list` does
not show. Always use `npx hyperframes` unpinned (latest release).

### 2. Transcribe the raw take

```bash
npx hyperframes transcribe <out>/voice/raw.wav \
  -d <out>/voice -l en --json
```

Always the **raw** take: whisper times a take whose pauses have been
tightened badly (measured 2026-09-24: three sentences collapsed into 0.2 s).

This writes `<out>/voice/transcript.json`. Use `small.en` (the default) for
English voices. Read the transcript once: nonsense words or a word count far
from the script mean the voice went wrong, not the transcriber.

### 3. Align (on the raw take)

```bash
python3 <skill-dir>/scripts/align_captions.py \
  --script <out>/voice/script.txt \
  --transcript <out>/voice/transcript.json \
  --wav <out>/voice/raw.wav \
  --out <out>/voice/words.json \
  --sentences <out>/voice/sentences.json \
  --must-match "<the profile's must-match words>"
```

`words.json` is `[{id, text, start, end}]` in the Hyperframes transcript
shape, with the screen spelling. `sentences.json` gives each sentence's start
and end.

Exit codes:
- `0` — go on.
- `2` — a brand word was heard as something else, or under 90 % of the words
  matched. **Listen to the wav.** If the voice really said it wrong, respell
  the word in `script-tts.txt` only (hyphens, phonetic spelling), regenerate,
  re-run. Add a working respelling to the profile's pronunciation list. If the
  voice was right and whisper misheard, say so and continue.

With `--wav`, the aligner also pulls words whisper placed inside a measured
silence back into the speech around them (whisper can drift ~0.4 s late at a
sentence end) and reports how many it moved.

### 4. Make it punchy, keep the timing

```bash
python3 <skill-dir>/scripts/process_voice.py \
  --raw <out>/voice/raw.wav --out <out>/voice/voiceover.wav \
  --remap <out>/voice/words.json <out>/voice/sentences.json
```

Raw Kokoro reads evenly and leaves ~0.5 s of air between sentences. The
script cuts every pause over 0.2 s down to 0.12 s, compresses, adds presence
and sets −14 LUFS, then moves every word and sentence time by exactly what it
cut. From here on `voiceover.wav` and the remapped JSON are the clock.
Measured 2026-09-24: `af_heart` @ 1.1 went from 23.6 s to 21.0 s for 71 words
(≈ 3.4 words/s).

### 5. Group the captions

```bash
python3 <skill-dir>/scripts/group_captions.py \
  --words <out>/voice/words.json --out <out>/voice/caption-groups.json
```

Groups of 1–3 words, split at punctuation and pauses, balanced so no word is
orphaned, at most 18 characters so a group stays on one line in the caption
band. The composition renders these groups as they are; it does not regroup.

### 6. Check the take

- First word starts ≤ 0.15 s. Kokoro starts at ~0.05 s; more means leading
  silence to trim.
- Total length is inside the format's range. Too long: cut script words and
  regenerate (step 2's budget was off). Never raise `--speed` to fit.
- No sentence runs over ~4 s. Longer sentences read flat; split them.

### 7. Beat durations

Each storyboard beat is keyed to sentences; its duration now comes from
`sentences.json`:

- A beat starts at its first sentence's `start` (the hook beat starts at 0).
- A beat ends where the next beat starts; the last beat ends at the voice's
  last `end` plus the tail from the format (0.8–1.5 s hold, or the loop
  seam).
- Visual cuts may lead the voice by up to 0.1 s; never lag it.

Write the measured beat table into `thumbstop-plan.md` under
`## Timing (measured)`, replacing the estimates:

```markdown
| Beat | Sentences | Start | End | Duration |
|---|---|---|---|---|
| 1 Hook | s0 | 0.00 | 2.33 | 2.33 |
```

## Gate

- No voice: the measured beat table is in the plan; every text beat meets its
  reading floor; the total fits the format.
- With `--voice`: `voice/raw.wav`, `voiceover.wav` (processed, remapped), `transcript.json`, `words.json`, `sentences.json`,
  `caption-groups.json` exist.
- The aligner exited 0, or its exit 2 was listened to and explained.
  The measured timing table is in the plan and sums to the voice length plus
  the tail.
