# Step 1: Inspect the project

Read the project in the working directory and work out, on your own, what
the video should say, what it can truthfully claim, and what it can show.
The result is `<out>/profile.md` (the project profile) plus working notes.
Nothing is written for the viewer yet.

## Create the output directory

```bash
mkdir -p <out>/material <out>/voice
```

## Reuse an earlier profile

Before reading anything, look for a profile from an earlier run:

1. `--profile <path>` if given.
2. `./thumbstop-profile.md` (a user-maintained profile at the project root).
3. The newest `thumbstop-output/*/profile.md`.

If one exists, start from it: keep its recorded decisions (voice, caption
style, pronunciation fixes, channel CTA) and re-read only its sources to
refresh facts. Otherwise build a new one from the reading below.

## What to read

In priority order. Stop early once the rubric can be answered from sources.

1. **README and docs**: what the project is, who it is for, the claims it
   makes, "how it works" and "usage" sections, links to where people buy,
   download or sign up.
2. **Business or product briefs**: files named like `BRIEF`, `PRODUCT`,
   `ABOUT`, `pitch`, `strategy`, marketing copy in `config/` or `content/`.
   These are usually the best source of true claims and the owner's own wording.
3. **The site or app itself**: `index.html`, pages, routes and components.
   Take the hero headline, tagline, section headings, CTA text, pricing copy.
   Find the **flow of using the product**: entry → key action → result.
4. **Styles**: CSS custom properties (`:root`), Tailwind config, theme
   files. Take background, text and accent colours, display and body fonts.
5. **Manifests**: `package.json`, `pyproject.toml`, app store metadata (name,
   description, keywords).
6. **Media inventory**: find every image and video the project owns
   (`public/`, `assets/`, `static/`, `media/`, `docs/`, render or export
   folders). For each video: `ffprobe` duration, size, fps, codec, rotation,
   whether it has audio. For images: size. Note what each one shows, and
   whether it is **raw material** (footage, renders, photos, recordings) or a
   **finished video** the owner has edited or posted. Burned-in text in a
   clip matters later (it can collide with captions). For a look inside a clip,
   extract a few frames with `ffmpeg -ss <t> -frames:v 1`; do not rely on the
   `drawtext` filter for labelled contact sheets (common ffmpeg builds, e.g.
   Homebrew's, ship without it).
7. **Existing marketing output**: earlier videos, social posts, ad copy, so
   the video matches decisions the owner already made (taste, tone, what is
   never shown).

Also look for the owner's own taste rules: `CLAUDE.md`, `AGENTS.md`, style
guides, "do not" lists. Treat them as binding.

## Skip

Build output (`dist/`, `.next/`, `build/`), dependencies, lock files, tests,
`.git/`, and anything secret: `.env*`, `*.pem`, `*.key`, credential files,
anything under `secrets/` or `credentials/`, local databases with personal
data. If a data source is needed for a count (customers, items sold), read it
read-only and record the query, never personal rows.

## The rubric

Answer all ten in working notes before step 2.

```
1. What is it?          One sentence a stranger understands.
2. Who is scrolling?    The viewer this is for and what they already know.
3. The one idea         The single thing this video lands. With a --brief,
                        the brief decides; without one, pick the strongest
                        claim the sources support.
4. Format               explainer / process / story / listicle / objection /
                        showcase (formats.md). --format wins; otherwise pick.
5. Channel              Where the viewer acts (shop, app store, site, sign-up),
                        with its CTA and any required disclosures. `none` for
                        a brand video. One channel per video.
6. The payoff           The moment the video exists for.
7. Sourced facts        Every claim the video might make, each with its
                        source (file:line, URL, or query + date). For
                        counts, get the whole-project totals too, not just
                        the featured item's: with sales data, units sold,
                        orders and distinct buyer countries (aggregates
                        only), each named by what it counts.
8. Real material        What will be on screen (tiers below). A product
                        shown as "the one you can buy" is checked against
                        the channel's own listing image, not a draft or a
                        second version.
9. Length               Target seconds inside the format's range.
10. Must not appear     Secrets, personal data, unreleased things, third-party
                        material the project does not own the rights to.
```

## Real material: the four tiers

Every video shows the real product. Use the highest tier the project allows,
and mix tiers freely across beats:

1. **The project's own media**: raw footage, screen recordings, renders,
   photos. Strongest, because it is the thing itself. Check that it matches
   the channel (never show a digital product as a physical one, or the
   reverse). **Not the owner's finished videos**: an edited or published
   video is the owner's own work, and re-cutting it is not making one. Use
   it only when the profile says `Re-cut finished videos: yes` (the default is
   no); otherwise build the video yourself from the raw material and tiers
   2–4.
2. **The product recreated in HTML from its source**: the landing hero, the
   key screen, the result view, the dashboard, built from the project's real
   markup, copy and styles. Simulate the key action (a tap, a swipe, a typed
   query, a result appearing). This is brag's core technique and works for
   any app or site.
3. **The concept animated**: when there is no UI to show, animate the idea
   with the project's own images, words and colours.
4. **Text-forward**: when the copy is the product, let the copy be the visual:
   big type, the project's fonts, minimal chrome.

Never fill a beat with abstract shapes, stock-looking decoration or generic
motion graphics. At most one beat per video may be graphic-only.

## Write the profile

Write `<out>/profile.md` using the structure in
[profile-template.md](profile-template.md). Every fact has its source. Fill
the Voice section from what you read:

- **Pronunciation risks**: brand and product names, accented letters
  (Kokoro reads accents badly: `Pokémon` → say `Pokemon`), acronyms, numbers
  with units. List a respelling for each one you expect trouble with.
- **Must-match words**: the brand and product names, for `align_captions.py`.

## Provenance table

Start it now; it goes into `thumbstop-plan.md` in step 2. Every spoken claim
and every on-screen claim needs a row:

```markdown
| Claim (as said/shown) | Source | Checked |
|---|---|---|
| "Ships in two days" | docs/shipping.md:12 "Orders ship within 2 business days" | 2026-09-24 |
```

- Pull numbers fresh at run time. A number from an earlier video, plan or
  memory is not a source.
- Prefer the project's own wording; paraphrase only for rhythm.
- A claim that is true for one channel and false for another (digital vs
  physical, one market vs another) is recorded with its channel.

## Copy the material

Copy (never link) what the video will show into `<out>/material/`, keeping
original names. Not into `composition/` yet: `hyperframes init` in step 4
refuses a non-empty directory. Never modify the originals.

- **Phone footage is transcoded now**: iPhone clips are often HEVC 4K with a
  rotation flag (a display matrix of −90°), which renders sideways or slowly.
  Make working copies in `material/`: H.264, rotation applied, 1080×1920 (or
  the clip's own orientation at 1080 on the short side).
- **Remote assets are downloaded now**: images a page loads from a URL
  (CDNs, Unsplash) and web fonts (Google Fonts: fetch the CSS, then the
  `.woff2` files for the Latin subset). A render may not fetch anything.
- **Look at every image you will use.** Alt text and file names describe what
  someone meant to put there, not what is there; describe the real image in
  the profile.

## Rule: nothing secret leaves this step

Everything read here can end up in a public video. Never carry secrets, API
keys, tokens, internal hostnames or URLs, customer names, e-mail addresses,
order ids or other personal data into the profile, plan, composition, video or
post texts. If the product's real UI shows such data, substitute neutral
stand-ins and say so in the plan.
