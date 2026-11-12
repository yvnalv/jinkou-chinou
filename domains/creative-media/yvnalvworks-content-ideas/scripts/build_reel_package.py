#!/usr/bin/env python3
"""Build a yvnalvworks reel package from one reel JSON file.

Writes, into --out (default: the JSON file's folder):
  reels-script.txt, teleprompter-voiceover-guide.txt, captions.srt, captions.json, content-spec.json

Every caption cue is checked against the spoken words (same words, same order), the
storytelling caption rules (sentence case, 3 to 6 words, max 32 characters, no trailing
period), and the em/en dash ban. Timing is estimated from words per minute; re-time
captions.srt to the real voiceover after recording.

Usage:
  python build_reel_package.py <reel.json> [--out <dir>]

See assets/reel.starter.json for the input format. Prints a JSON summary; exits 1 on rule errors.
"""
import argparse
import json
import os
import re
import sys

MIN_WORDS, MAX_WORDS, MAX_CHARS = 3, 6, 32
MIN_CUE, SENTENCE_PAUSE = 1.0, 0.3


def norm(text):
    return re.sub(r"[^\w'\- ]", " ", text.lower()).split()


def ts(t, srt=True):
    ms = int(round(t * 1000))
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"00:{m:02d}:{s:02d},{ms:03d}" if srt else f"{m:02d}:{s:02d}.{ms // 100}"


def validate(reel):
    errors = []
    for key in ("title", "date", "scenes", "sources"):
        if not reel.get(key):
            errors.append(f"missing '{key}'")
    for sc in reel.get("scenes", []):
        name = sc.get("name", "?")
        cues = sc.get("cues", [])
        if norm(sc.get("spoken", "")) != norm(" ".join(c[0] for c in cues)):
            errors.append(f"{name}: cues do not match the spoken words")
        for text, _ in cues:
            n = len(text.split())
            if not MIN_WORDS <= n <= MAX_WORDS or len(text) > MAX_CHARS:
                errors.append(f"{name}: cue '{text}' has {n} words / {len(text)} chars (need {MIN_WORDS}-{MAX_WORDS} words, max {MAX_CHARS})")
            if text.isupper() or text.rstrip().endswith("."):
                errors.append(f"{name}: cue '{text}' must be sentence case with no trailing period")
    if "—" in json.dumps(reel, ensure_ascii=False) or "–" in json.dumps(reel, ensure_ascii=False):
        errors.append("em or en dash found; use commas, colons, or a new sentence")
    return errors


def build(reel, out):
    wpm = reel.get("wpm", 140)
    spw = 60 / wpm
    scenes = reel["scenes"]
    t, cues = 0.0, []
    for si, sc in enumerate(scenes, 1):
        sc["start"] = t
        for text, end_sentence in sc["cues"]:
            dur = max(MIN_CUE, len(text.split()) * spw)
            cues.append({"id": len(cues) + 1, "scene": si, "start": round(t, 2), "end": round(t + dur, 2), "text": text})
            t += dur + (SENTENCE_PAUSE if end_sentence else 0)
        sc["end"] = cues[-1]["end"]
    total = cues[-1]["end"]
    words = sum(len(sc["spoken"].split()) for sc in scenes)
    os.makedirs(out, exist_ok=True)

    def write(name, text):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)

    write("captions.srt", "".join(f"{c['id']}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n" for c in cues))
    write("captions.json", "[\n" + ",\n".join("  " + json.dumps({k: c[k] for k in ("id", "start", "end", "text")}, ensure_ascii=False) for c in cues) + "\n]\n")

    title = reel["title"]
    bar, line = "=" * 80, "-" * 80
    g = [bar, "YVNALVWORKS VOICE RECORDING TELEPROMPTER & CLOSED CAPTION GUIDE", bar,
         f"Topic       : {title}",
         "Platform    : Instagram Reels / TikTok / YouTube Shorts (9:16)",
         f"Pacing      : Warm and conversational, like telling a friend (~{wpm} WPM)",
         f"Target Time : ~{round(total)} seconds ({words} words)",
         "Language    : English, friendly storytelling",
         "Voiceover   : Manual recording by Yovan (iPhone, 48 kHz). No AI voice.", bar, "",
         "[HOW TO RECORD]",
         "1. Read the FULL READ-THROUGH out loud once. It should sound like you're telling a story,",
         "   not reading a list. If a line feels stiff in your mouth, say it your way.",
         "2. Let sentences flow into each other. Small pauses at commas, a breath at each period.",
         "3. Lean lightly on the word marked *LIKE THIS* in each scene.",
         "4. Smile on the first line. The hook is a moment the viewer recognizes.",
         f"5. Caption timings are estimates at ~{wpm} WPM. After recording, re-time captions.srt to your",
         "   audio (CapCut: import SRT, drag cue edges), or send the audio back for re-alignment.", "",
         line, "FULL READ-THROUGH", line]
    g += [sc["spoken"] for sc in scenes] + [""]
    for si, sc in enumerate(scenes, 1):
        g += [line, f"SCENE {si} ({ts(sc['start'], False)} - {ts(sc['end'], False)}) | {sc['name'].upper()}", line,
              "SPOKEN LINE:", f"\"{sc['spoken']}\"", "", f"EMPHASIS: {sc.get('emphasis', '')}", "",
              "CLOSED CAPTIONS (ON-SCREEN):"]
        g += [f"[{ts(c['start'], False)} - {ts(c['end'], False)}] {c['text']}" for c in cues if c["scene"] == si]
        g.append("")
    write("teleprompter-voiceover-guide.txt", "\n".join(g))

    s = [f"# REELS SCRIPT: {title}", f"Story: {reel.get('story', '')}",
         "Platform: Instagram Reels / TikTok / YouTube Shorts (9:16)", f"Duration: ~{round(total)} seconds ({words} words)",
         "Voice: Friendly, conversational storytelling"]
    if reel.get("companion"):
        s.append(f"Companion post: {reel['companion']}")
    s += ["", "---", ""]
    for si, sc in enumerate(scenes, 1):
        s += [f"[SCENE {si}: {ts(sc['start'], False)} - {ts(sc['end'], False)}] {sc['name']}",
              f"On-screen: {sc.get('onscreen', '')}", f"Audio: \"{sc['spoken']}\"", f"Visual: {sc.get('visual', '')}", ""]
    s += ["---", "", f"EVIDENCE SOURCES (verified {reel['date']})"]
    s += [f"{i}. {src}" for i, src in enumerate(reel["sources"], 1)] + [""]
    write("reels-script.txt", "\n".join(s))

    spec = {
        "title": f"(Video) {title}", "category": reel.get("category", "AI Engineering"), "platform": "Instagram", "postType": "Reels",
        "aspectRatio": "9:16", "resolution": {"width": 1080, "height": 1920}, "durationSeconds": round(total, 1),
        "date": reel["date"], "status": reel.get("status", "Idea 💡"), "articleRef": reel.get("link", "https://www.yvnalvworks.com/projects"),
        "brandTokens": {"background": "assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png (never a flat fill)",
                        "fontPrimary": "Poppins", "fontMono": "JetBrains Mono", "textHeadline": "#FFFFFF",
                        "textBody": "#F0ECE2", "textSecondary": "#8E8E93", "accentLime": "#C1FF72", "cardDark": "#18181b"},
        "voiceover": {"mode": "manual", "talent": "Yovan Alvianto", "guideFile": "teleprompter-voiceover-guide.txt",
                      "subtitlesSrt": "captions.srt", "subtitlesJson": "captions.json",
                      "timingNote": f"Estimated at {wpm} WPM; re-time to the recorded audio"},
        "captionStyle": {"case": "sentence", "wordsPerCue": f"{MIN_WORDS}-{MAX_WORDS}", "maxCharsPerCue": MAX_CHARS,
                         "font": "Poppins 600, white, one line", "ccLockedY": 1480},
        "scenes": [{"scene": i, "name": sc["name"], "duration": f"{ts(sc['start'], False)} - {ts(sc['end'], False)}",
                    "onscreen": sc.get("onscreen", ""), "visual": sc.get("visual", ""), "lucideIcons": sc.get("icons", []), "ccLockedY": 1480}
                   for i, sc in enumerate(scenes, 1)],
    }
    write("content-spec.json", json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    return {"out": out, "cues": len(cues), "words": words, "durationSeconds": round(total, 1),
            "inTarget": 40 <= total <= 60}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Build a yvnalvworks reel package (script, teleprompter, captions, spec) from reel JSON")
    ap.add_argument("reel_json", help="Path to reel JSON (see assets/reel.starter.json)")
    ap.add_argument("--out", "-o", help="Output folder (default: the JSON file's folder)")
    args = ap.parse_args()
    if not os.path.exists(args.reel_json):
        print(f"Error: '{args.reel_json}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(args.reel_json, encoding="utf-8") as f:
        reel = json.load(f)
    errors = validate(reel)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    out = args.out or os.path.dirname(os.path.abspath(args.reel_json))
    print(json.dumps(build(reel, out), indent=2))


if __name__ == "__main__":
    main()
