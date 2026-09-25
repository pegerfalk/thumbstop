# Platforms

Verified platform facts for TikTok, Instagram Reels and Facebook Reels.
Sources are listed at the end of this file. **Checked 2026-09-23.** Platform
rules move: re-verify anything older than six months before relying on it.

Labels: ✓ official source · ≈ secondary only · ? no source found.

## The common safe box (1080×1920)

| Platform | Top | Bottom | Sides | Action column |
|---|---|---|---|---|
| TikTok ✓ | 240 px | 660 px | 120 px | 180 px wide (x 780–960) from y 840 down |
| Instagram Reels ✓ | 14 % (269 px) | 35 % (672 px) | 6 % (65 px) | — |
| Facebook Reels ✓ | 14 % | 35 % | 6 % | — |

**Keep all text and key detail inside x 120–960, y 270–1248, and x ≤ 780
below y 840.** `scripts/safezone_check.sh` enforces it.
Sources: TikTok In-Feed safe-zone template (ads spec page, updated June 2026);
Meta Ads Guide Reels: "leaving at least 14% of the top, 35% of the bottom, and
6% on each side of your asset free from text, logos, or other important
creative elements". These are the ad templates; organic UI is similar, but
there is no official organic spec (?).

## File

- ✓ 1080×1920, 30 fps, H.264, AAC stereo ≥ 128 kbps, MP4 works on all three.
  Instagram: 9:16 allowed, ≥ 30 fps, ≥ 720 px. Meta ads recommend 1440×2560
  (ads only). TikTok API: 23–60 fps, ≤ 4 GB.
- ✓ Facebook Reels takes the same file as-is.

## Length

- ✓ TikTok: 21–34 s recommended for In-Feed ads (2022 one-pager, the only
  official figure). Ads up to 10 min.
- ✓ Instagram: Reels up to 20 min, but "Reels over 3 minutes won't be
  recommended to new audiences." → **never over 3 min.**
- ✓ Facebook Reels: no length limit.

## Hook and captions

- ✓ TikTok: "Prioritize your hook in the first 6 seconds", "Introduce your
  content proposition in the first 3 seconds", "Use captions or text overlays"
  at "5-10 words per second", keep content "within the UI safe zone".
- ✓ Meta: "nail the hook within the first few seconds". Reels "have sound on
  by default". Captions "optional, but recommended".
- There is no official source for "most people watch muted". Captions are for
  accessibility and as a second hook layer.

## AI labels (synthetic voice)

- ✓ Meta (Instagram + Facebook): label required for "realistic-sounding audio
  that was digitally created or altered". Explicit example: "A reel narrated
  with a realistic AI-generated voiceover". Penalties possible.
- ✓ TikTok Community Guidelines (effective 24 Sep 2026): generic TTS that is
  not "a recognizable voice of a known individual" is exempt. The TikTok
  Support page is stricter ("label all AI-generated content that contains
  realistic … audio"), and "Turning on the AI-generated content setting won't
  affect the distribution of your video."
- **Rule: with `--voice`, AI label ON on all three platforms.** Kokoro writes
  no C2PA data, so nothing is auto-labelled.
- Without a voice the video contains no synthetic voice and no AI-generated
  realistic imagery (it is rendered from the project's own copy, UI and
  media), so no label is required. If the project's own media is itself
  AI-generated and realistic, label it anyway.

## Commercial disclosure

- ✓ TikTok: "If you're promoting a product, brand, or business, you must use
  TikTok's content disclosure setting." → **Content disclosure → Your brand:
  ON** for every video about the user's own business.
- ? Meta: branded-content tools are for partnerships; no requirement found
  for a business promoting itself.

## Hashtags and captions

- ✓ Instagram: "You can use up to 5 tags on a post." → **max 5.**
- ? TikTok: no official hashtag guidance; caption limit 4,000 characters is
  secondary only (≈). Ad captions take no hashtags.
- ? Facebook: no official hashtag guidance.
- Craft default: 3–5 specific hashtags everywhere.

## Cover

- ✓ Instagram: choose a frame or upload; **cannot be changed after
  posting**. ≈ Profile grid is 3:4 since Jan 2025 → keep the cover title
  inside y 240–1680.
- ≈ TikTok: pick a frame or upload, add cover text.
- ? Facebook Reels: no official organic cover spec.
- Thumbstop bakes the cover as frame 0 (so every auto-thumbnail is right)
  and ships `cover.jpg` for upload.

## Cross-posting and ads

- ✓ Instagram → Facebook: "Also share on…" at creation, mobile app only.
- ✓ Meta Ads Guide advises against licensed music in ads → boost the
  `-nomusic` export.

## Sources (checked 2026-09-23)

- TikTok In-Feed ad template (safe zone, 720×1280 × 1.5), updated June 2026:
  https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads
- Meta Ads Guide, Instagram Reels ("leaving at least 14% of the top, 35% of
  the bottom, and 6% on each side of your asset free from text"); Facebook
  Reels uses the same text:
  https://www.facebook.com/business/ads-guide/update/video/instagram-reels
- TikTok creative best practices ("Introduce your content proposition in the
  first 3 seconds"): https://ads.tiktok.com/help/article/creative-best-practices
- Meta, "The science of the hook" (15 Dec 2025):
  https://www.facebook.com/business/news/the-science-of-the-hook-how-to-supercharge-your-reels-performance
- Meta, Reels ads ("Reels have sound on by default"):
  https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- TikTok SMB Top Tips ("21-34 seconds is the recommended length for In-Feed
  advertising"): https://ads.tiktok.com/business/library/Top_Tips_One_Pager_SMB.pdf
- TikTok Community Guidelines, integrity and authenticity (AI-generated
  content, TTS narration):
  https://www.tiktok.com/community-guidelines/en/integrity-authenticity
- TikTok FAQ, AI-generated content label:
  https://www.tiktok.com/support/faq_detail?id=7636670084747893268
