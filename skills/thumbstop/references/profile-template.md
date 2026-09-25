# Project profile template

The profile holds everything project-specific: where the truth lives, what
real material exists, what the brand looks like, how the voice must pronounce
names, and what each channel requires. The skill itself names no project.

**Step 1 writes it** to `<out>/profile.md` by reading the project. Later runs
reuse the newest one, so decisions made once (voice, caption style,
pronunciation fixes, CTA) stick. A user may also keep a hand-edited copy at the
project root as `thumbstop-profile.md`; that one wins.

A section that does not apply says so explicitly ("none"), so a run never has
to guess.

---

```markdown
# Project profile: <name>

Written <YYYY-MM-DD> from <which files>. When this profile and the project's
own files disagree, the files win: re-read them and update this profile.
Read-only: <yes/no — may /thumbstop write into the project's folders?>

## What it is
<Two or three sentences a stranger understands. The one-line pitch verbatim,
with its source.>

## Sources of truth
| What | Where | Notes |
|---|---|---|
| Product facts, prices | <file / table / URL> | <how fresh it must be> |
| Counts (customers, items, sales…) | <file / query> | re-query at run time; record the whole-project total, not just per item |
| The product as sold | <the channel's own listing image / URL> | what "the one you can buy" looks like |
| Brand voice and look | <file> | |

Staleness rule: <e.g. counts older than 30 days are re-queried or dropped>.

## Channels
Where a viewer can buy or act. Each video names one channel, or `none`
(brand/awareness video). Disclosures, CTA and prices come from the channel.

### <channel id, e.g. webshop>
- What the viewer gets: <digital download / physical item / service / app>
- Price source: <file + section>, currency <XXX>
- CTA (verbatim): "<…>"
- Required disclosures (post text, one plain line): "<…>"
- Post-text ending: "<e.g. 'Link in bio.'>"
- Post-text language: <e.g. English> (the voice language is set under Voice;
  they may differ)

### none (brand/awareness)
- Disclosures: <the subset that is always true>
- CTA: <soft, or none>

## Proof numbers
The shop- or project-level numbers a video may flex, re-queried every run.
| Number | What it counts | Query / source | Last value | Date |
|---|---|---|---|---|
| <e.g. units sold> | <units / orders / buyers / countries> | <read-only query> | <value> | <YYYY-MM-DD> |

Shown rounded down with a "+" (a live count must stay true until it is posted).

## Real material ("the real thing")
Re-cut finished videos: <no (default) / yes> — the owner's edited or posted
videos are never material unless this says yes.

| Material | Where | Use |
|---|---|---|
| <raw footage / renders / screenshots / scans> | <path> | <what it is good for> |

How to check it: <ffprobe notes, known audio beds, loop/resolve behaviour>.

## Taste already decided
<Bullet list of decisions the owner has made, with dates. Pace, look,
what must always / never be shown.>

## Visual identity
- Colours: <hex values and what each is for>
- Fonts: <display / body, or "not recorded — propose 2–3 on the first run">
- Look: <one line>
- Not used: <anything in the brand kit that collides with the No-defaults law>

## Caption style
<`editorial` (default) · `pill` · `outline` — see step-4-compose.md — plus any
project-specific adjustment, e.g. marker colour when the accent fails contrast
on white.>

## Voice
- Voice: off by default; with `--voice`: <Kokoro id> @ <speed> (default
  `af_heart` @ 1.1, processed by `process_voice.py`)
- Pronunciation (TTS text only): <word → respelling, why>
- Must-match words (align_captions.py): <comma list of brand/product names>

## Hook seeds and example briefs
<Optional. Project-specific hook lines (each with its source) and briefs that
suit each format. Claims here are re-checked at run time.>

## Hashtags
<Starting sets per topic; at most 5 per post (Instagram's limit).>

## Third-party rights
<Whose IP may appear (logos, characters, product photos), who decides.>

## Must not appear
<Secrets, personal data, internal systems, unreleased items…>
```
