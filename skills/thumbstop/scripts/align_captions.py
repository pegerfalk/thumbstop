#!/usr/bin/env python3
"""Put the script's words on the voiceover's clock.

Kokoro gives no word timings, so the voiceover is transcribed afterwards
(`npx hyperframes transcribe`). The transcript's *timing* is good, but its
*spelling* is whisper's guess ("Pacaman", "center"). Captions must
show the script's spelling, so this aligns the display script to the
transcript and keeps only the times.

Measured on Kokoro + whisper small.en (Hyperframes 0.8.65, 2026-09-23):
word STARTS match real silence boundaries within ~0.05 s; word ENDS stretch
across pauses by up to ~0.6 s. So every end is clamped to the next word's
start, and, when the wav is given, to the start of any silence it runs into.
Whisper can also drift late (a start inside a measured silence); with the wav,
such words are pulled back into the speech around them.

Stdlib only (ffmpeg is used for silence detection when --wav is passed).

Usage:
  align_captions.py --script script.txt --transcript transcript.json \
      --wav voiceover.wav --out words.json [--sentences sentences.json] \
      [--must-match "BrandName,ProductName"]

Exit code 2 when fewer than --min-match of the script words matched the
transcript by text, or when any --must-match word (brand and product names)
was heard as something else: the voice probably said it wrong. Listen, then
fix the TTS spelling (never the display script).
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

# Spelling pairs whisper normalizes differently from our scripts. Compared
# after normalization, so both sides are lowercase ASCII letters/digits.
EQUIVALENT = {
    "centre": "center",
    "colour": "color",
    "favourite": "favorite",
    "grey": "gray",
}


# Whisper writes small numbers as digits ("8"), scripts often as words.
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def normalize(word: str) -> str:
    ascii_word = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    token = re.sub(r"[^a-z0-9]", "", ascii_word.lower())
    if token.isdigit() and int(token) < len(NUMBER_WORDS):
        token = NUMBER_WORDS[int(token)]
    return EQUIVALENT.get(token, token)


def ends_clause(word: str) -> bool:
    return bool(re.search(r"[.!?,;:]['\"”’)]*$", word))


def silences(wav: Path, noise_db: float, min_s: float) -> list[tuple[float, float]]:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
         f"silencedetect=n={noise_db}dB:d={min_s}", "-f", "null", "-"],
        capture_output=True, text=True, check=False,
    )
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", proc.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", proc.stderr)]
    return list(zip(starts, ends))


def align(script_words: list[str], transcript: list[dict]) -> tuple[list[dict], list[tuple[str, str]]]:
    a = [normalize(w) for w in script_words]
    b = [normalize(w["text"]) for w in transcript]
    times: list[tuple[float, float] | None] = [None] * len(script_words)
    mismatches: list[tuple[str, str]] = []
    attach_next: list[tuple[int, float]] = []
    attach_prev: list[tuple[int, float]] = []

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                t = transcript[j1 + k]
                times[i1 + k] = (float(t["start"]), float(t["end"]))
        elif tag == "replace":
            # Spread the transcript span evenly over the script span.
            span_start = float(transcript[j1]["start"])
            span_end = float(transcript[j2 - 1]["end"])
            n = i2 - i1
            for k in range(n):
                s = span_start + (span_end - span_start) * k / n
                e = span_start + (span_end - span_start) * (k + 1) / n
                times[i1 + k] = (s, e)
            # Same letters, different word split ("AcmeStudio" vs
            # "Acme Studio"): a spelling choice, not a mishearing.
            if "".join(a[i1:i2]) == "".join(b[j1:j2]):
                continue
            mismatches.append((" ".join(script_words[i1:i2]),
                               " ".join(t["text"] for t in transcript[j1:j2])))
        elif tag == "delete":
            mismatches.append((" ".join(script_words[i1:i2]), "<not heard>"))
        elif tag == "insert":
            # Heard but not in the screen script: the TTS text said one screen
            # token as several words ("/thumbstop" -> "slash thumbstop"). The
            # extra words belong to the next script word (or the previous one
            # at the very end), so that word starts where they start.
            if i1 < len(script_words):
                pending_start = float(transcript[j1]["start"])
                attach_next.append((i1, pending_start))
            elif i1 > 0:
                attach_prev.append((i1 - 1, float(transcript[j2 - 1]["end"])))

    for i, s in attach_next:
        if times[i]:
            times[i] = (min(s, times[i][0]), times[i][1])
    for i, e in attach_prev:
        if times[i]:
            times[i] = (times[i][0], max(e, times[i][1]))

    # Script words the voice never said get squeezed between their neighbours.
    for i, t in enumerate(times):
        if t is None:
            prev_end = next((times[k][1] for k in range(i - 1, -1, -1) if times[k]), 0.0)
            nxt = next((times[k][0] for k in range(i + 1, len(times)) if times[k]), prev_end)
            times[i] = (prev_end, max(prev_end, nxt))

    words = [{"id": f"w{i}", "text": w, "start": round(s, 3), "end": round(e, 3)}
             for i, (w, (s, e)) in enumerate(zip(script_words, times))]
    return words, mismatches


def snap_to_speech(words: list[dict], quiet: list[tuple[float, float]]) -> int:
    """Pull words whisper placed inside a measured silence back into speech.

    Whisper sometimes drifts late (seen on Kokoro: "cards out." started 0.4 s
    after the voice had gone quiet). A word whose start falls inside a silence
    belongs to one side of it: punctuation decides first (a clause-final word
    before, a word after a clause end after), then the nearer side, and word
    order is kept. Words before the silence compress their speech run so it
    ends where the silence starts; words after it start where it ends. Returns
    the number of words moved.
    """
    moved = 0
    for q_start, q_end in quiet:
        inside = [i for i, w in enumerate(words) if q_start + 0.03 < w["start"] < q_end - 0.03]
        if not inside:
            continue
        # Decide in speaking order. Punctuation first: a clause-final word was
        # said before the pause, a word after a clause end starts after it.
        # Once one word is placed after the pause, every later one follows.
        before, after = [], []
        for i in inside:
            if after:
                after.append(i)
            elif ends_clause(words[i]["text"]):
                before.append(i)
            elif i > 0 and ends_clause(words[i - 1]["text"]):
                after.append(i)
            elif words[i]["start"] - q_start < q_end - words[i]["start"]:
                before.append(i)
            else:
                after.append(i)
        if after:
            nxt = after[-1] + 1
            limit = words[nxt]["start"] if nxt < len(words) else q_end + 0.2 * len(after)
            step = max(0.0, min(0.2, (limit - q_end) / (len(after) + 1)))
            for k, i in enumerate(after):
                words[i]["start"] = round(q_end + k * step, 3)
                moved += 1
        if not before:
            continue
        last = max(before)
        # The speech run: back to the previous silence (or the first word).
        prev_end = max((qe for qs, qe in quiet if qe <= q_start), default=0.0)
        first = next(i for i, w in enumerate(words) if w["start"] >= prev_end - 0.05)
        t0, t1 = words[first]["start"], words[last]["start"]
        tail = max(0.15, 0.07 * len(normalize(words[last]["text"])))
        target_last = max(t0, q_start - tail)
        if t1 <= t0:
            continue
        scale = (target_last - t0) / (t1 - t0)
        for i in range(first, last + 1):
            new = round(t0 + (words[i]["start"] - t0) * scale, 3)
            if abs(new - words[i]["start"]) > 0.001:
                moved += 1
            words[i]["start"] = new
    return moved


def clamp_ends(words: list[dict], quiet: list[tuple[float, float]]) -> None:
    for i, w in enumerate(words):
        end = w["end"]
        if i + 1 < len(words):
            end = min(end, words[i + 1]["start"])
        for q_start, _ in quiet:
            if w["start"] < q_start < end:
                end = q_start
        w["end"] = round(max(end, w["start"] + 0.05), 3)


def sentences(words: list[dict]) -> list[dict]:
    out, current = [], []
    for w in words:
        current.append(w)
        if re.search(r"[.!?]['\"”’)]*$", w["text"]):
            out.append(current)
            current = []
    if current:
        out.append(current)
    return [{"id": f"s{i}", "text": " ".join(w["text"] for w in s),
             "start": s[0]["start"], "end": s[-1]["end"],
             "first_word": s[0]["id"], "last_word": s[-1]["id"]}
            for i, s in enumerate(out)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--script", required=True, type=Path, help="display script (screen spelling)")
    ap.add_argument("--transcript", required=True, type=Path, help="hyperframes transcribe output")
    ap.add_argument("--wav", type=Path, help="voiceover, for silence-based end clamping")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--sentences", type=Path, help="also write sentence timings here")
    ap.add_argument("--min-match", type=float, default=0.9)
    ap.add_argument("--must-match", default="",
                    help="comma list of words that must be heard exactly (brand names)")
    ap.add_argument("--silence-db", type=float, default=-40.0)
    ap.add_argument("--silence-min", type=float, default=0.12)
    args = ap.parse_args()

    script_words = args.script.read_text(encoding="utf-8").split()
    raw = json.loads(args.transcript.read_text(encoding="utf-8"))
    transcript = [w for w in (raw if isinstance(raw, list) else raw.get("words", []))
                  if normalize(w.get("text", ""))]
    if not script_words or not transcript:
        print("empty script or transcript", file=sys.stderr)
        return 1

    words, mismatches = align(script_words, transcript)
    quiet = silences(args.wav, args.silence_db, args.silence_min) if args.wav else []
    moved = snap_to_speech(words, quiet)
    for i in range(1, len(words)):  # starts never go backwards
        if words[i]["start"] < words[i - 1]["start"]:
            words[i]["start"] = round(words[i - 1]["start"] + 0.01, 3)
    clamp_ends(words, quiet)

    args.out.write_text(json.dumps(words, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.sentences:
        args.sentences.write_text(json.dumps(sentences(words), indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8")

    unmatched = sum(len(s.split()) for s, _ in mismatches if s != "<not in script>")
    ratio = 1 - unmatched / len(script_words)
    print(f"{len(words)} words, {ratio:.0%} matched by text, "
          f"voice {words[0]['start']:.2f}-{words[-1]['end']:.2f}s, "
          f"{moved} word start(s) pulled out of silences")
    for script_side, heard in mismatches:
        print(f"  script {script_side!r} <- heard {heard!r}")
    failed = False
    if ratio < args.min_match:
        print(f"match below {args.min_match:.0%}: listen to the voiceover before continuing",
              file=sys.stderr)
        failed = True
    must = {normalize(w) for w in args.must_match.split(",") if normalize(w)}
    for script_side, heard in mismatches:
        wrong = must & {normalize(w) for w in script_side.split()}
        if wrong:
            print(f"must-match word(s) {sorted(wrong)} heard as {heard!r}: listen, then respell "
                  f"them in the TTS text", file=sys.stderr)
            failed = True
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
