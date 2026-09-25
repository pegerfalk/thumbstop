#!/usr/bin/env bash
# Fail if any text in the composition enters a platform UI zone.
#
# The common (strictest) safe box for TikTok + Instagram Reels + Facebook
# Reels on 1080x1920, verified 2026-09-23 (references/platforms.md):
#   x 120-960, y 270-1248, and x <= 780 below y 840 (TikTok action column).
#
# `hyperframes check --caption-zone` audits one band per run (a repeated flag
# keeps only the last — tested on 0.8.65), so this runs check once per band.
# It audits every text element, clipped or hidden ones included. The only
# allowed waiver is `data-layout-allow-caption-zone` on the outermost
# container of recreated product imagery (step-4-compose.md); overlay text
# (captions, keywords, CTA copy) is never waived.
#
# Usage: safezone_check.sh <composition-dir> [seek-fractions]
#   seek-fractions: comma list of 0-1 timeline fractions to sample
#   (default: every 5 %). Captions change fast; sample densely.
set -uo pipefail

dir="${1:?usage: safezone_check.sh <composition-dir> [seek-fractions]}"
seek="${2:-.02,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,.99}"

bands=(
  "top|x0=0;y0=0;x1=1;y1=.1406"
  "bottom|x0=0;y0=.65;x1=1;y1=1"
  "left|x0=0;y0=0;x1=.1111;y1=1"
  "right|x0=.8889;y0=0;x1=1;y1=1"
  "tiktok-actions|x0=.7222;y0=.4375;x1=1;y1=1"
)

hits=0
for band in "${bands[@]}"; do
  name="${band%%|*}"
  geom="${band#*|}"
  out=$(npx hyperframes check "$dir" --no-contrast \
        --caption-zone "${geom};severity=error;seek=${seek}" 2>&1)
  found=$(grep "caption_zone_collision" <<<"$out" | sed "s/caption_zone_collision/[$name]/")
  if [[ -n "$found" ]]; then
    echo "$found"
    hits=$((hits + $(grep -c . <<<"$found")))
  fi
done

if (( hits > 0 )); then
  echo "safe zone: $hits text collision(s) — move the text inside x 120-960, y 270-1248 (x <= 780 below y 840)"
  exit 1
fi
echo "safe zone: clean (5 bands, seek=${seek})"
