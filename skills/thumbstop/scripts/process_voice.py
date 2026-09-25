#!/usr/bin/env python3
"""Make a raw Kokoro take sound like a social voiceover, and keep the timing.

Kokoro reads evenly and leaves ~0.5 s of air between sentences; in a feed that
air is where people swipe away. This script:

  1. tightens pauses: every silence longer than --max-pause is cut down to
     --keep-pause (half kept at each side, so no word is clipped)
  2. removes rumble (high-pass 80 Hz)
  3. compresses (3:1 from -20 dB) so the voice sits close and even
  4. adds presence (+3 dB around 3.5 kHz) for phone speakers
  5. normalises loudness to -14 LUFS, true peak -1.5 dB

Whisper times a take with no air in it badly (measured 2026-09-24: three
sentences collapsed into 0.2 s), so transcription and alignment run on the
RAW take, and this script moves every word and sentence time by exactly what
it cut (--remap). Order in step 3: tts -> transcribe raw -> align raw ->
process_voice.py --remap words.json sentences.json -> group_captions.py.

Stdlib only (plus ffmpeg).

Usage:
  process_voice.py --raw raw.wav --out voiceover.wav \
      --remap voice/words.json voice/sentences.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def silences(path: Path, noise_db: float, min_s: float) -> list[tuple[float, float]]:
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                           f"silencedetect=n={noise_db}dB:d={min_s}", "-f", "null", "-"],
                          capture_output=True, text=True, check=False)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", proc.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", proc.stderr)]
    return list(zip(starts, ends))


def keep_segments(total: float, quiet: list[tuple[float, float]], keep: float) -> list[tuple[float, float]]:
    """Intervals of the raw take that survive. Each long silence keeps keep/2
    at its start and keep/2 at its end; leading/trailing silence keeps keep."""
    half = keep / 2
    cuts = []
    for s, e in quiet:
        if s <= 0.001:                      # leading silence: keep `half` before the voice
            cuts.append((0.0, max(0.0, e - half)))
        elif e >= total - 0.001:            # trailing silence
            cuts.append((min(total, s + half), total))
        else:
            cuts.append((s + half, e - half))
    segs, cursor = [], 0.0
    for a, b in sorted(cuts):
        if b - a <= 0.001:
            continue
        if a > cursor:
            segs.append((cursor, a))
        cursor = max(cursor, b)
    if cursor < total:
        segs.append((cursor, total))
    return segs


def make_map(segs: list[tuple[float, float]]):
    def remap(t: float) -> float:
        acc = 0.0
        for a, b in segs:
            if t < a:                       # inside a cut: snap to the cut point
                return round(acc, 3)
            if t <= b:
                return round(acc + (t - a), 3)
            acc += b - a
        return round(acc, 3)
    return remap


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--remap", nargs="*", type=Path, default=[],
                    help="JSON files with start/end fields to move onto the new timeline (in place)")
    ap.add_argument("--max-pause", type=float, default=0.2)
    ap.add_argument("--keep-pause", type=float, default=0.12)
    ap.add_argument("--silence-db", type=float, default=-40.0)
    args = ap.parse_args()

    total = duration(args.raw)
    quiet = silences(args.raw, args.silence_db, args.max_pause)
    segs = keep_segments(total, quiet, args.keep_pause)
    select = "+".join(f"between(t,{a:.4f},{b:.4f})" for a, b in segs)
    chain = (f"aselect='{select}',asetpts=N/SR/TB,"
             "highpass=f=80,"
             "acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
             "equalizer=f=3500:t=q:w=1:g=3,"
             "loudnorm=I=-14:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(args.raw), "-af", chain,
                    "-ar", "48000", str(args.out)], check=True)

    remap = make_map(segs)
    for path in args.remap:
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data:
            for key in ("start", "end"):
                if key in item:
                    item[key] = remap(float(item[key]))
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    new_total = duration(args.out)
    cut = total - sum(b - a for a, b in segs)
    print(f"processed voice: {total:.2f} s -> {new_total:.2f} s "
          f"({len(quiet)} pauses tightened, {cut:.2f} s of air removed, -14 LUFS); "
          f"remapped {len(args.remap)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
