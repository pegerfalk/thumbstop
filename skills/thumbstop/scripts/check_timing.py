#!/usr/bin/env python3
"""Check the measured timing table in a thumbstop-plan.md (step 3, no voice).

Reads the table under "## Timing" whose header has Beat / Screen text / Words /
Events / Settled / Out / Beats columns, and checks the arithmetic a hand-written
table gets wrong:

  - Words matches the screen text (phrase marks `/` and accent `*` ignored)
  - line floor:        Out - first event >= max(0.8, 0.3 x words)
  - last-phrase floor: Out - Settled     >= max(0.8, 0.3 x words in the last phrase)
  - hook (first row):  Out - first event >= 1.5
  - no line longer than 6 beats
  - no gap between consecutive events (whole table) longer than ~2 beats;
    the tail after the last event is a settled hold and is not counted

The beat length comes from "<n> BPM" in the plan, else 120 BPM (step 3 rule 7).
Rows whose Words cell is not a number (an end card) are checked for gaps only.

Usage: check_timing.py <thumbstop-plan.md> [--bpm N]
Exit 0 when every check passes, 1 otherwise. Standard library only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NUM = re.compile(r"\d+(?:\.\d+)?")
WORD = re.compile(r"[\w'’.,:%$€£-]*\w[\w'’.,:%$€£-]*")


def words(text: str) -> int:
    return len(WORD.findall(text.replace("*", " ").replace("/", " ")))


def table(plan: str) -> list[list[str]]:
    lines = plan.splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 7 and cells[0].startswith("beat") and "events" in " ".join(cells):
            rows = []
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    sys.exit("no timing table found (header: | Beat | Screen text | Words | Events (s) | Settled | Out | Beats |)")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    plan = Path(args[0]).read_text()
    bpm = float(args[args.index("--bpm") + 1]) if "--bpm" in args else None
    if bpm is None:
        m = re.search(r"(\d+(?:\.\d+)?)\s*BPM", plan)
        bpm = float(m.group(1)) if m else 120.0
    beat = 60.0 / bpm
    max_gap = 2 * beat + 0.10

    fails, events_all = [], []
    for n, row in enumerate(table(plan)):
        if len(row) < 7:
            continue
        name, text, wcell, ecell, scell, ocell, bcell = row[:7]
        evs = [float(x) for x in NUM.findall(ecell)]
        out = float(NUM.findall(ocell)[0]) if NUM.findall(ocell) else None
        events_all += evs + ([out] if out is not None else [])
        if not evs or out is None:
            fails.append(f"{name}: no events or no Out time")
            continue
        first = min(evs)
        if NUM.fullmatch(bcell.strip() or "x") and float(bcell) > 6:
            fails.append(f"{name}: {bcell} beats (max 6)")
        if not wcell.strip().isdigit():
            continue
        w, counted = int(wcell), words(text)
        if w != counted:
            fails.append(f"{name}: Words says {w}, the screen text has {counted}")
        floor = max(0.8, 0.3 * counted)
        if out - first < floor - 1e-6:
            fails.append(f"{name}: line on screen {out - first:.2f} s, floor {floor:.2f} s")
        if n == 0 and out - first < 1.5 - 1e-6:
            fails.append(f"{name}: hook holds {out - first:.2f} s, needs 1.5 s")
        settled = float(NUM.findall(scell)[0]) if NUM.findall(scell) else first
        last = words(text.split("/")[-1])
        lfloor = max(0.8, 0.3 * last)
        if out - settled < lfloor - 1e-6:
            fails.append(f"{name}: last phrase holds {out - settled:.2f} s, floor {lfloor:.2f} s")

    # The end is a settled hold (the tail rule, 0.8-1.5 s), not a gap between events.
    rows_out = [float(NUM.findall(r[5])[0]) for r in table(plan) if len(r) >= 7 and NUM.findall(r[5])]
    if rows_out and max(rows_out) in events_all:
        events_all = [t for t in events_all if t != max(rows_out)]
    pts = sorted(set(events_all))
    for a, b in zip(pts, pts[1:]):
        if b - a > max_gap:
            fails.append(f"gap {a:.2f} -> {b:.2f} s ({b - a:.2f} s, max ~2 beats = {max_gap:.2f} s at {bpm:g} BPM)")

    for f in fails:
        print("FAIL", f)
    print(f"timing: {'OK' if not fails else f'{len(fails)} problem(s)'} "
          f"({len(pts)} event times, {bpm:g} BPM)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
