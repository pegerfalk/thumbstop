# Step 5: Preview, render, deliver

## 1. Preview (only with `--preview`)

```bash
cd <out>/composition && npx hyperframes preview --background
```

Give the user the Studio URL and say what to look at: the first second, the
payoff beat, caption readability. Wait for a go or for changes. Changes to
words go back to step 2 (both strings) and re-run step 3; changes to picture
or sound stay in step 4. Stop the preview (`--stop`) before rendering.
Without `--preview`, go straight to rendering.

## 2. Render both exports

Render the music version, then add `data-hidden` to the music `<audio>` and
render again. Nothing else may differ. With no music track available, render
only `-nomusic` and say so in the report.

```bash
cd <out>/composition
npx hyperframes render --quality high --output ../<slug>-music.mp4
# add data-hidden to the music <audio>
npx hyperframes render --quality high --output ../<slug>-nomusic.mp4
# remove data-hidden again, so the composition stays the music version
```

Verify the switch worked: the two files' audio must differ, and `-nomusic`
must be silent between sentences apart from clip sound/SFX
(`ffmpeg -i <file> -af volumedetect -f null -` on a pause range).

Use `--quality draft` only for iteration renders, never for delivery.

## 3. Verify the files

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,channels \
  -show_entries format=duration -of compact <out>/<slug>-music.mp4
```

Both files: H.264 1080×1920 at 30/1, AAC stereo, the same duration (±0.1 s
after the audio pass). Listen to the first 3 s and the last 3 s of each: the voice is clear
over the bed in `-music`, and `-nomusic` has no music at all. Peaks stay
below −1 dBFS (`ffmpeg -i <file> -af volumedetect -f null -`).

## 4. Cover and frame 0

The cover is the first thing anyone sees: the profile grid, the paused feed,
link previews. Pick the **settled** frame of the cover beat named in the
brief: text fully in, nothing mid-transition, product sharp. Title inside
y 240–1680 (Instagram's 3:4 grid crop).

```bash
cd <out>
ffmpeg -ss <t> -i <slug>-music.mp4 -frames:v 1 -q:v 2 cover.jpg
```

Then bake `cover.jpg` into frame 0 of **both** exports (only the first
frame's pixels change; the method is inherited from `/brag`) and, in the same
pass, normalise the audio to **−14 LUFS**, where the platforms play it back:

```bash
for f in <slug>-music <slug>-nomusic; do
  AF="loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.8:level=disabled"   # every export with continuous sound
  # a voiceless -nomusic export is SFX only: keep its levels (AF="anull"),
  # normalising near-silence would blow the hits up
  ffmpeg -y -i $f.mp4 -i cover.jpg \
    -filter_complex "[0:v][1:v]overlay=0:0:enable='eq(n,0)'[v];[0:a]$AF,aresample=48000[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart $f.final.mp4 && mv $f.final.mp4 $f.mp4
done
```

Check each export with `ffmpeg -i <file> -af ebur128 -f null -`: −14 ±1.5
LUFS for everything with continuous sound, and peaks below −1 dBFS
(`loudnorm` alone can still leave 0.0 dB sample peaks after AAC; the limiter
catches them). A voiceless `-nomusic` export is SFX only and lands far lower
(around −27 LUFS) by design; that is not a failed normalisation.

The audio pass can make an export slightly longer than the other (AAC
padding). If the two durations differ by more than 0.1 s, re-mux the longer
one with `-t <composition duration> -c:v copy`.

Re-run the ffprobe check afterwards.

## 5. Segments (only with `--segments`)

Some feeds seem to favour posts assembled in-app. With `--segments`, cut
`<slug>-nomusic.mp4` into **three** clips at beat boundaries near the thirds,
where both of these hold: the picture has a hard cut, and `words.json` has a
gap of at least 0.15 s (never cut inside a word). Re-encode each clip
(frame-accurate), write them to `<out>/segments/<slug>-1.mp4` … `-3.mp4`, and
list the cut times in the plan.

## 6. Post texts

Write `tiktok.txt`, `instagram.txt`, `facebook.txt`. Each has the caption
ready to paste, then an **upload checklist** that is not pasted. The caption
is written in the channel's **post-text language** (profile), which may differ
from the voice: write it natively in that language, never as a word-for-word
translation of the script. The checklist stays in English. Facts come
from `references/platforms.md` (verified, dated).

```
<caption: 1–3 short lines. The hook restated as something a viewer would
send to a friend.>

<the channel's required disclosures (profile), one plain line: facts, not
apologies. Channel `none`: the profile's always-true subset.>

<the channel's CTA / post-text ending, verbatim from the profile>

<hashtags: 3–5, specific to the subject. Instagram: never more than 5.>

---
Upload checklist (do not paste)
- File: <slug>-nomusic.mp4 (add trending audio in the app) or <slug>-music.mp4
- Cover: upload cover.jpg
- AI label: ON with --voice (synthetic voiceover); without a voice not required
  (see platforms.md)
- <TikTok only> Content disclosure → Your brand: ON (promoting own business)
- <Instagram only> Cover cannot be changed after posting; hashtags max 5
- <Facebook only> Can be shared from Instagram at creation ("Also share on…")
- If boosted as an ad: use <slug>-nomusic.mp4
- <if -music is used> Music credit: the credit line from audio.md for the track used
```

Caption rules: no em-dash rhythm, no emoji walls (one is allowed where it
carries meaning), no generic hype words, no claim that is not in the
provenance table.

## 7. Final structure

```
<out>/
  <slug>-nomusic.mp4   <slug>-music.mp4   cover.jpg
  tiktok.txt   instagram.txt   facebook.txt
  thumbstop-plan.md   composition-brief.md
  material/   voice/   composition/   [segments/]
```

## Open the video

When the files are verified, open the finished video in the user's default
player, so the first thing they get is the video itself: `<slug>-music.mp4`,
or `<slug>-nomusic.mp4` when there is no music export.

```bash
open <out>/<slug>-music.mp4                  # macOS
xdg-open <out>/<slug>-music.mp4              # Linux
cmd.exe /c start "" <out>\<slug>-music.mp4   # Windows
```

Opening is local only: it never uploads or shares anything. If there is no
desktop to open it on (a remote or cloud session, SSH, CI), skip it and give
the full path instead.

## Telling the user

- Where the videos and the cover are, and the length; say which one was
  opened.
- One sentence each: the angle it chose and why, the hook, the payoff.
- What it could not do (no music track found, a claim it cut for lack of a
  source, material it could not use) — plainly.
- The loudness of each export; for a voiceless `-nomusic` export, say that
  its low level (SFX only, about −27 LUFS) is intended.
- The upload checklist's switches: AI label on everywhere when the video has
  the synthetic voice; TikTok content disclosure on when the video promotes the
  user's own business.
- Offer re-rolls: the other two hooks, another format, a shorter cut,
  another caption style, another voice.

Never upload, schedule or post. The user publishes.
