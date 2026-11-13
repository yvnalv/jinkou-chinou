#!/usr/bin/env python3
"""Assemble recorded voiceover takes, speed them up, and re-time the captions to the real audio.

One take per scene, in scene order. For each take:
  1. Detect pauses (ffmpeg silencedetect) to get speech segments; drop blips under 0.3 s.
  2. Split the scene's script into phrases at , . : ? ! and match phrases to segments
     (merge the closest segments if there are too many; group phrases with dynamic
     programming if there are too few, using syllable counts as expected length).
  3. Spread each segment's words by syllables -> word timings -> caption cue timings.
Then trim, join (lead-in + gaps), normalize loudness (-16 LUFS), and apply atempo.

Usage:
  python scripts/align_voiceover.py --reel <reel.json> --takes t1.m4a t2.m4a ... --speed 1.2 --out vo-out
Writes: <out>/voiceover.wav, captions.json, captions.srt, alignment.json
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FFMPEG = os.path.join(HERE, "..", "node_modules", "@remotion", "compositor-win32-x64-msvc", "ffmpeg.exe")
MIN_SEG = 0.3      # ignore speech blips shorter than this (clicks, breaths)
PAD_IN, PAD_OUT = 0.12, 0.18
LEAD, GAP = 0.25, 0.45   # seconds at 1x: before the first take, between takes


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"):
        n -= 1
    return max(1, n)


def ff(*args, capture=False):
    r = subprocess.run([FFMPEG, "-hide_banner", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-800:])
    return r.stderr


def duration(path):
    out = ff("-i", path, "-f", "null", "-")
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", out)
    h, mnt, s = m[-1]
    return int(h) * 3600 + int(mnt) * 60 + float(s)


def speech_segments(path):
    # Analyse a mono downmix; pair each silence_start with the next silence_end in event order.
    out = ff("-i", path, "-af", "aformat=channel_layouts=mono,silencedetect=noise=-38dB:d=0.25", "-f", "null", "-")
    total = duration(path)
    sil, cur = [], None
    for kind, val in re.findall(r"silence_(start|end): (-?[\d.]+)", out):
        if kind == "start":
            cur = max(0.0, float(val))
        elif cur is not None:
            sil.append((cur, float(val)))
            cur = None
    if cur is not None:
        sil.append((cur, total))
    segs, t = [], 0.0
    for s, e in sil:
        if s - t > 0:
            segs.append([t, s])
        t = e
    if total - t > 0:
        segs.append([t, total])
    return [s for s in segs if s[1] - s[0] >= MIN_SEG], total


def phrases(spoken):
    parts = re.findall(r"[^,.:?!]+[,.:?!]?", spoken)
    return [p.strip().split() for p in parts if p.strip()]


def group_phrases(ph, segs):
    """Assign consecutive phrase groups to segments (len(ph) >= len(segs)) minimizing duration mismatch."""
    syl = [sum(syllables(w) for w in p) for p in ph]
    rate = sum(s[1] - s[0] for s in segs) / sum(syl)
    n, m = len(ph), len(segs)
    INF = float("inf")
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for k in range(j - 1, i):
                if best[k][j - 1] == INF:
                    continue
                exp = sum(syl[k:i]) * rate
                got = segs[j - 1][1] - segs[j - 1][0]
                cost = best[k][j - 1] + (exp - got) ** 2
                if cost < best[i][j]:
                    best[i][j], back[i][j] = cost, k
    groups, i = [], n
    for j in range(m, 0, -1):
        k = back[i][j]
        groups.append([w for p in ph[k:i] for w in p])
        i = k
    return groups[::-1]


def align_take(path, spoken):
    segs, total = speech_segments(path)
    ph = phrases(spoken)
    while len(segs) > len(ph):  # a pause inside a phrase: merge the closest pair
        gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]
        i = gaps.index(min(gaps))
        segs[i:i + 2] = [[segs[i][0], segs[i + 1][1]]]
    groups = group_phrases(ph, segs)
    words = []
    for (s, e), ws in zip(segs, groups):
        syl = [syllables(w) for w in ws]
        t, step = s, (e - s) / sum(syl)
        for w, n in zip(ws, syl):
            words.append({"word": w, "start": t, "end": t + n * step})
            t += n * step
    return {"segments": segs, "words": words, "trim": [max(0, segs[0][0] - PAD_IN), min(total, segs[-1][1] + PAD_OUT)]}


def ts(t):
    ms = int(round(t * 1000))
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"00:{m:02d}:{s:02d},{ms:03d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reel", required=True)
    ap.add_argument("--takes", nargs="+", required=True, help="one recording per scene, in scene order")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    reel = json.load(open(a.reel, encoding="utf-8"))
    scenes = reel["scenes"]
    if len(a.takes) != len(scenes):
        sys.exit(f"Error: {len(a.takes)} takes for {len(scenes)} scenes")
    os.makedirs(a.out, exist_ok=True)

    cues, report, parts, offset = [], [], [], LEAD
    for sc, take in zip(scenes, a.takes):
        al = align_take(take, sc["spoken"])
        t0, t1 = al["trim"]
        words = al["words"]
        wi = 0
        for text, _ in sc["cues"]:
            n = len(text.split())
            ws = words[wi:wi + n]
            wi += n
            cues.append({"text": text, "start": (offset + ws[0]["start"] - t0) / a.speed, "end": (offset + ws[-1]["end"] - t0) / a.speed})
        report.append({"scene": sc["name"], "take": os.path.basename(take), "trim": [round(t0, 2), round(t1, 2)],
                       "segments": [[round(s, 2), round(e, 2)] for s, e in al["segments"]]})
        parts.append((take, t0, t1))
        offset += (t1 - t0) + GAP

    # Audio: trim each take, pad, concat, clean, speed.
    inputs, filters = [], []
    for i, (take, t0, t1) in enumerate(parts):
        inputs += ["-i", take]
        pad = LEAD if i == 0 else 0
        filters.append(f"[{i}:a]atrim={t0:.3f}:{t1:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=mono,"
                       f"adelay={int(pad * 1000)},apad=pad_dur={GAP if i < len(parts) - 1 else 0.6}[a{i}]")
    chain = "".join(f"[a{i}]" for i in range(len(parts)))
    filters.append(f"{chain}concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,atempo={a.speed},aformat=sample_rates=48000:channel_layouts=stereo[out]")
    wav = os.path.join(a.out, "voiceover.wav")
    ff("-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-c:a", "pcm_s16le", wav)
    total = duration(wav)

    out_cues = [{"id": i + 1, "start": round(c["start"], 2), "end": round(c["end"], 2), "text": c["text"]} for i, c in enumerate(cues)]
    with open(os.path.join(a.out, "captions.json"), "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in out_cues) + "\n]\n")
    with open(os.path.join(a.out, "captions.srt"), "w", encoding="utf-8") as f:
        f.write("".join(f"{c['id']}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n" for c in out_cues))
    with open(os.path.join(a.out, "alignment.json"), "w", encoding="utf-8") as f:
        json.dump({"speed": a.speed, "audioSeconds": round(total, 2), "takes": report}, f, indent=2)
    print(json.dumps({"audio": wav, "audioSeconds": round(total, 2), "cues": len(out_cues), "lastCueEnd": out_cues[-1]["end"], "speed": a.speed}, indent=2))


if __name__ == "__main__":
    main()
