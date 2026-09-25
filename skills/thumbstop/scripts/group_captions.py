#!/usr/bin/env python3
"""Group aligned words into caption groups.

Caption policy (what), not caption rendering (how): turns `words.json`
(from align_captions.py) into `caption-groups.json`, which the composition
renders one group at a time with the active word highlighted.

Rules:
- A phrase ends at sentence or clause punctuation (. , ? ! : ;) or a pause
  of >= --pause seconds.
- A phrase is split into balanced groups of at most 3 words (4 -> 2+2,
  5 -> 3+2, 7 -> 3+2+2), so no word is orphaned at a sentence end.
- A group longer than --max-chars characters is halved, so it fits on one
  line in the caption band; a lone short word left over joins a neighbour.
- A group ends at the next group's start, or 0.35 s after its last word.

Usage: group_captions.py --words words.json --out caption-groups.json
Output: [{start, end, words: [{text, start}]}]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PUNCT = ".,?!:;"


def phrases(words: list[dict], pause: float) -> list[list[dict]]:
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or w["text"].rstrip("\"'”’)")[-1:] in PUNCT or nxt["start"] - w["end"] >= pause:
            out.append(cur)
            cur = []
    return out


def split(phrase: list[dict], max_chars: int) -> list[list[dict]]:
    n = len(phrase)
    k = math.ceil(n / 3)
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    groups, i = [], 0
    for s in sizes:
        chunk = phrase[i:i + s]
        i += s
        if len(" ".join(w["text"] for w in chunk)) > max_chars and len(chunk) > 1:
            h = len(chunk) // 2
            groups += [chunk[:h], chunk[h:]]
        else:
            groups.append(chunk)
    return groups


def text(g: list[dict]) -> str:
    return " ".join(w["text"] for w in g)


def absorb_orphans(groups: list[list[dict]], max_chars: int) -> list[list[dict]]:
    """A lone short word ("a", "the", "and") flashes by unreadably: move it to
    the start of the next group if that still fits, else to the end of the
    previous one, never across a sentence end."""
    out = [list(g) for g in groups]
    i = 0
    while i < len(out):
        g = out[i]
        if len(g) == 1 and len(g[0]["text"]) <= 4 and len(out) > 1:
            nxt = out[i + 1] if i + 1 < len(out) else None
            prv = out[i - 1] if i > 0 else None
            if nxt and not g[0]["text"].rstrip("\"'”’)")[-1:] in ".?!" \
                    and len(text(g + nxt)) <= max_chars + 2:
                out[i + 1] = g + nxt
                del out[i]
                continue
            if prv and not prv[-1]["text"].rstrip("\"'”’)")[-1:] in ".?!" \
                    and len(text(prv + g)) <= max_chars + 2:
                out[i - 1] = prv + g
                del out[i]
                continue
        i += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--words", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--pause", type=float, default=0.5)
    ap.add_argument("--max-chars", type=int, default=18)
    ap.add_argument("--tail", type=float, default=0.35)
    args = ap.parse_args()

    words = json.loads(args.words.read_text(encoding="utf-8"))
    if not words:
        print("no words", file=sys.stderr)
        return 1
    groups = [g for p in phrases(words, args.pause) for g in split(p, args.max_chars)]
    groups = absorb_orphans(groups, args.max_chars)
    out = []
    for gi, g in enumerate(groups):
        nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else None
        end = g[-1]["end"] + args.tail
        if nxt is not None:
            end = min(end, nxt)
        out.append({"start": round(g[0]["start"], 3), "end": round(end, 3),
                    "words": [{"text": w["text"], "start": round(w["start"], 3)} for w in g]})
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    short = sum(1 for g in out if g["end"] - g["start"] < 0.3)
    print(f"{len(out)} groups from {len(words)} words; {short} shorter than 0.3 s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
