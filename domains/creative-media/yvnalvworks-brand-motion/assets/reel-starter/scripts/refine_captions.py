#!/usr/bin/env python3
"""Snap caption cue starts to Whisper word timings on the final voiceover.

align_voiceover.py places cues by pauses and syllables (exact at pauses, approximate mid-phrase).
This pass moves a cue's start to the Whisper timestamp of its first two words (matched as a pair)
when Whisper heard them within --window seconds of the estimate and after the previous cue, then keeps cues ordered and non-overlapping.

Usage: python scripts/refine_captions.py --captions vo-out/captions.json --words vo/final-16k.words.json [--window 0.8] [--far-window 3.0]
Rewrites captions.json and captions.srt next to it. Prints a JSON report.
"""
import argparse
import json
import os
import re


def norm(t):
    return re.sub(r"[^a-z]", "", t.lower())


def ts(t):
    ms = int(round(t * 1000))
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"00:{m:02d}:{s:02d},{ms:03d}"


ap = argparse.ArgumentParser()
ap.add_argument("--captions", required=True)
ap.add_argument("--words", required=True)
ap.add_argument("--window", type=float, default=0.8)
ap.add_argument("--far-window", type=float, default=3.0)
a = ap.parse_args()

cues = json.load(open(a.captions, encoding="utf-8"))
words = [w for w in json.load(open(a.words, encoding="utf-8")) if norm(w["text"]) and not w["text"].startswith("[")]
moved = []
prev_start = -1.0
for c in cues:
    # Match the cue's first two words as a pair (a lone "you" or "the" matches the wrong place),
    # and never move a cue before the previous cue: keeps the timeline ordered.
    cw = [norm(x) for x in c["text"].split()]
    cands = []
    for i, w in enumerate(words):
        if norm(w["text"]) != cw[0]:
            continue
        if len(cw) > 1 and (i + 1 >= len(words) or norm(words[i + 1]["text"]) != cw[1]):
            continue
        if abs(w["start"] - c["start"]) <= a.far_window and w["start"] > prev_start + 0.2:
            cands.append(w)
    near = [w for w in cands if abs(w["start"] - c["start"]) <= a.window]
    # Within --window: take the nearest. Beyond it (a phrase said in one breath can throw the
    # pause-based estimate off by seconds): only when the two-word match is unique up to --far-window.
    pick = near or (cands if len(cands) == 1 else [])
    if pick:
        best = min(pick, key=lambda w: abs(w["start"] - c["start"]))
        if abs(best["start"] - c["start"]) >= 0.05:
            moved.append({"id": c["id"], "from": c["start"], "to": round(best["start"], 2)})
            c["start"] = round(best["start"], 2)
    prev_start = c["start"]
for i in range(1, len(cues)):  # keep the timeline ordered even where an estimate was not refined
    if cues[i]["start"] < cues[i - 1]["start"] + 0.3:
        cues[i]["start"] = round(cues[i - 1]["start"] + 0.3, 2)
for i, c in enumerate(cues):
    nxt = cues[i + 1]["start"] if i + 1 < len(cues) else None
    if nxt is not None:
        # End = where Whisper heard the cue's last word (first match after the cue starts). Hold the cue
        # until the next one unless a real pause (over 0.6 s) follows that word.
        last = norm(c["text"].split()[-1])
        lw = [w for w in words if norm(w["text"]) == last and c["start"] <= w["start"] < nxt]
        spoken_end = lw[0]["end"] if lw else c["end"]
        end = spoken_end if nxt - spoken_end > 0.6 else nxt - 0.03
        c["end"] = round(min(max(end, c["start"] + 0.4), nxt), 2)
    else:
        c["end"] = round(max(c["end"], c["start"] + 0.4), 2)
    assert c["start"] < c["end"], c
    if i:
        assert cues[i - 1]["start"] <= c["start"], (cues[i - 1], c)

with open(a.captions, "w", encoding="utf-8") as f:
    f.write("[\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in cues) + "\n]\n")
with open(os.path.join(os.path.dirname(a.captions), "captions.srt"), "w", encoding="utf-8") as f:
    f.write("".join(f"{c['id']}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n" for c in cues))
print(json.dumps({"moved": moved, "cues": len(cues)}, indent=1))
