#!/usr/bin/env python3
"""Snap caption cue starts to Whisper word timings on the final voiceover.

align_voiceover.py places cues by pauses and syllables (exact at pauses, approximate mid-phrase).
This pass moves a cue's start to the Whisper timestamp of its first word when Whisper heard
that word within --window seconds of the estimate, then keeps cues ordered and non-overlapping.

Usage: python scripts/refine_captions.py --captions vo-out/captions.json --words vo/final-16k.words.json [--window 0.8]
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
a = ap.parse_args()

cues = json.load(open(a.captions, encoding="utf-8"))
words = [w for w in json.load(open(a.words, encoding="utf-8")) if norm(w["text"]) and not w["text"].startswith("[")]
moved = []
for c in cues:
    first = norm(c["text"].split()[0])
    cands = [w for w in words if norm(w["text"]) == first and abs(w["start"] - c["start"]) <= a.window]
    if cands:
        best = min(cands, key=lambda w: abs(w["start"] - c["start"]))
        if abs(best["start"] - c["start"]) >= 0.05:
            moved.append({"id": c["id"], "from": c["start"], "to": round(best["start"], 2)})
            c["start"] = round(best["start"], 2)
for i, c in enumerate(cues):
    nxt = cues[i + 1]["start"] if i + 1 < len(cues) else None
    if nxt is not None:
        c["end"] = round(min(max(c["end"], c["start"] + 0.4), nxt), 2)
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
