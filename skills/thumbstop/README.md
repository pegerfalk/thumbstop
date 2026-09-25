# skills/thumbstop/

The `/thumbstop` skill: reads the current project and turns it into a
vertical video for TikTok, Instagram Reels and Facebook Reels (no voice by
default; `--voice` adds a punchy voiceover with captions).
Start at `SKILL.md`.

| Path | What |
|---|---|
| `SKILL.md` | Dispatch, flags, the five steps with gates, the laws |
| `references/step-1-inspect.md` … `step-5-deliver.md` (step 3: `step-3-timing.md`) | One file per step |
| `references/formats.md` | explainer, process, story, listicle, objection, showcase |
| `references/hooks.md` | The seven hook types, with worked examples |
| `references/platforms.md` | Verified platform facts (2026-09-23), safe box |
| `references/audio.md` | Levels with and without a voice, SFX library, music + licence practice |
| `references/profile-template.md` | The project profile step 1 writes (and later runs reuse) |
| `scripts/align_captions.py` | Script words onto the transcript's clock (stdlib) |
| `scripts/group_captions.py` | Words into 1–3-word caption groups (stdlib) |
| `scripts/process_voice.py` | Tight pauses, compression, presence, −14 LUFS for the voiceover (ffmpeg) |
| `scripts/safezone_check.sh` | `hyperframes check` once per forbidden UI band |
| `scripts/analyze_music_cues.py` | Music cue analysis, inherited from brag (needs `uv`) |
| `assets/sfx/` | CC0 SFX from brag, with `sfx-analysis.md` |
| `assets/music/` | Cue presets + `LICENSE-music.md` for the recommended tracks (audio not shipped) |

Everything project-specific is learned at run time and written to the run's
`profile.md`; the skill itself names no project.

Requirements: Node (for `npx hyperframes`, always the latest release),
ffmpeg, Python 3 (stdlib only for the Thumbstop scripts). Kokoro and whisper
models are fetched by Hyperframes on first use.

Fork of [`/brag`](https://github.com/latent-spaces/brag) 0.3.0 (MIT) by Shunit
Haviv Hakimi. Built on [Hyperframes](https://hyperframes.heygen.com/).
