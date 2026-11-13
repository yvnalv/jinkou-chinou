#!/usr/bin/env python3
"""Build a yvnalvworks reel package from one reel JSON file.

Writes, into --out (default: the JSON file's folder):
  reels-script.txt, teleprompter-voiceover-guide.txt, captions.srt, captions.json, content-spec.json,
  cover-spec.json (render the reel cover with /yvnalvworks-brand-motion render_carousel.py)

Every reel needs a cover: `coverHeadline` follows the same rules as carousel covers
(3 to 4 lines, max 18 characters per line, exactly one [[highlight]]).

Every caption cue is checked against the spoken words (same words, same order), the
storytelling caption rules (sentence case, 3 to 9 words, max 48 characters, no trailing
period), and the em/en dash ban. The hook rule is enforced: the first sentence of scene 1
is 8 words or fewer (about 3 seconds once sped up 1.2x). A style lint warns about AI-ish writing: stacked
short sentences and stock phrases (see references/yvnalvworks-voice-and-tone-guide.md). Timing is estimated from words per minute; re-time
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from format_content_idea import validate_cover_headline  # noqa: E402  (same skill)

MIN_WORDS, MAX_WORDS, MAX_CHARS = 3, 9, 48
HOOK_MAX_WORDS = 8  # about 3 s at the 1.2x delivery
SHORT_SENTENCE = 7  # words
MIN_CUE, SENTENCE_PAUSE = 1.0, 0.3


def norm(text):
    return re.sub(r"[^\w'\- ]", " ", text.lower()).split()


def ts(t, srt=True):
    ms = int(round(t * 1000))
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"00:{m:02d}:{s:02d},{ms:03d}" if srt else f"{m:02d}:{s:02d}.{ms // 100}"


STOCK_PHRASES = [
    "here's the thing", "let's dive", "dive in", "let that sink in", "buckle up", "game changer", "game-changer",
    "unlock", "in today's world", "the secret", "spoiler", "it's not just", "in short", "did you know",
    "in this video", "today we'll", "hi guys",
]


def sentences(text):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x.strip()]


def style_warnings(reel):
    """Warnings (not errors) for AI-ish writing: stacked short sentences and stock phrases."""
    warns = []
    allsent = []
    for sc in reel.get("scenes", []):
        sents = sentences(sc.get("spoken", ""))
        allsent += sents
        run = 0
        for x in sents:
            run = run + 1 if len(x.split()) < SHORT_SENTENCE else 0
            if run == 2:
                warns.append(f"{sc.get('name', '?')}: two short sentences in a row ('{x}'); merge into one flowing sentence")
        low = sc.get("spoken", "").lower()
        for ph in STOCK_PHRASES:
            if ph in low:
                warns.append(f"{sc.get('name', '?')}: stock phrase '{ph}' sounds generated; say it plainly")
    body = allsent[1:]  # the hook may be short
    if body:
        short = sum(1 for x in body if len(x.split()) < SHORT_SENTENCE)
        avg = sum(len(x.split()) for x in body) / len(body)
        if short / len(body) > 0.3:
            warns.append(f"{short} of {len(body)} sentences are under {SHORT_SENTENCE} words; the script will sound choppy")
        if avg < 11:
            warns.append(f"average sentence is {avg:.1f} words; aim for 12 to 22 so it flows like speech")
    return warns


def validate(reel):
    errors = []
    for key in ("title", "date", "scenes", "sources"):
        if not reel.get(key):
            errors.append(f"missing '{key}'")
    if not reel.get("coverHeadline"):
        errors.append("missing 'coverHeadline': every reel needs a cover (see references/cover-headline-patterns.md)")
    else:
        errors.extend(validate_cover_headline(reel["coverHeadline"]))
    scenes = reel.get("scenes", [])
    if scenes:
        first = sentences(scenes[0].get("spoken", ""))
        if first and len(first[0].split()) > HOOK_MAX_WORDS:
            errors.append(f"hook: the first sentence has {len(first[0].split())} words; the hook must land in 2 to 3 seconds ({HOOK_MAX_WORDS} words or fewer)")
    for sc in scenes:
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
         "   Record ONE TAKE PER SCENE, in order, into the reel folder's voiceover/ subfolder,",
         "   with a short natural pause at every comma and period (the sync uses those pauses).",
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
    spec["cover"] = {"file": "reel-cover.png", "headline": reel["coverHeadline"], "spec": "cover-spec.json"}
    write("content-spec.json", json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    cover_spec = {"format": "reel", "slides": [{"type": "cover", "headline": reel["coverHeadline"], "file": "reel-cover.png"}]}
    write("cover-spec.json", json.dumps(cover_spec, indent=2, ensure_ascii=False) + "\n")
    hook = sentences(scenes[0]["spoken"])[0]
    return {"out": out, "cues": len(cues), "words": words, "durationSeconds": round(total, 1),
            "inTarget": 30 <= total < 180, "hook": hook, "hookSeconds": round(len(hook.split()) * spw, 1),
            "styleWarnings": style_warnings(reel)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Build a yvnalvworks reel package (script, teleprompter, captions, spec) from reel JSON")
    ap.add_argument("reel_json", help="Path to reel JSON (see assets/reel.starter.json)")
    ap.add_argument("--out", "-o", help="Output folder (default: the JSON file's folder)")
    ap.add_argument("--force-captions", action="store_true", help="Overwrite captions even if they are aligned to a recorded voiceover")
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
    aligned = reel.get("video", {}).get("voiceover", {}).get("captionsAligned")
    keep = {}
    if aligned and not args.force_captions:
        for name in ("captions.srt", "captions.json"):
            p = os.path.join(out, name)
            if os.path.exists(p):
                keep[name] = open(p, encoding="utf-8").read()
    result = build(reel, out)
    for name, text in keep.items():  # restore captions aligned to the real voiceover
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)
    if keep:
        result["captionsKept"] = "aligned to the recorded voiceover (use --force-captions to overwrite)"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
