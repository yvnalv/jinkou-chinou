#!/usr/bin/env python3
"""
Format and validate a Databro content idea into the standard 8-part markdown schema.
Enforces technical completeness, valid citations, and zero em-dashes. Video ideas
(Reels / TikTok / Shorts / YouTube) must also carry a `cover` plan
{"headline", "limeKeyword", "hook", "visual"} and a storytelling `script`
[{"beat", "voiceover", "visual"}] whose first sentence (the hook) is at most 9 words.
Every idea is also linted for AI-ish writing (stacked short sentences, colon reveals,
stock phrases); findings are reported as `styleWarnings` and should be zero before handover.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

VIDEO_PATTERN = re.compile(r"\b(video|reels?|tiktok|shorts|youtube)\b", re.IGNORECASE)
COVER_FIELDS = ("headline", "limeKeyword", "hook", "visual")


def is_video_idea(data: dict) -> bool:
    text = f"{data.get('platform', '')} {data.get('formatType', '')}"
    return bool(VIDEO_PATTERN.search(text))


def validate_cover(data: dict) -> list[str]:
    """A video idea needs a complete cover plan; the lime keyword must sit inside the headline."""
    if not is_video_idea(data):
        return []
    cover = data.get("cover")
    if not isinstance(cover, dict):
        return ["Missing 'cover': every Reels / TikTok / Shorts / YouTube idea needs a cover plan "
                "{headline, limeKeyword, hook, visual}."]
    errors = [f"Missing cover field: 'cover.{f}'" for f in COVER_FIELDS if not str(cover.get(f, "")).strip()]
    kw, headline = str(cover.get("limeKeyword", "")), str(cover.get("headline", ""))
    if kw and headline and kw.lower() not in headline.lower():
        errors.append(f"cover.limeKeyword '{kw}' must appear inside cover.headline '{headline}'.")
    return errors


# --- Storytelling checks --------------------------------------------------------------

HOOK_MAX_WORDS = 9
SPOKEN_WPM = 125  # measured Databro talent pace: 123 wpm including natural pauses (2026-11-12 reel)
VO_SPEED = 1.2  # creator preference: the recorded voice is sped up 1.2x in the final reel (about 148 wpm)
STORY_BEATS = ("hook", "setup", "discovery", "payoff", "takeaway", "cta")
STOCK_PHRASES = (
    "di era digital", "mari kita bahas", "tahukah kamu", "semoga bermanfaat", "game changer",
    "revolusioner", "rahasia", "bukan cuma", "bukan hanya", "tidak hanya",
)
SENTENCE_SPLIT = re.compile(r"(?<=[.?!])\s+")


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT.split(str(text).strip()) if s.strip()]


def word_count(text: str) -> int:
    return len(re.findall(r"[0-9A-Za-zÀ-ɏ'-]+", str(text)))


def validate_script(data: dict) -> list[str]:
    """A video idea needs a storytelling script whose hook fits in 2 to 3 seconds."""
    if not is_video_idea(data):
        return []
    script = data.get("script")
    if not isinstance(script, list) or not script:
        return ["Missing 'script': every Reels / TikTok / Shorts / YouTube idea needs a storytelling script "
                "[{beat, voiceover, visual}] that opens with a hook."]
    errors = []
    for i, scene in enumerate(script, 1):
        if not isinstance(scene, dict) or not str(scene.get("voiceover", "")).strip():
            errors.append(f"script[{i}] needs a non-empty 'voiceover'.")
        elif str(scene.get("beat", "")).lower() not in STORY_BEATS:
            errors.append(f"script[{i}].beat must be one of {', '.join(STORY_BEATS)}.")
    if errors:
        return errors
    if str(script[0].get("beat", "")).lower() != "hook":
        errors.append("script[1] must be the 'hook' beat.")
    first = sentences(script[0]["voiceover"])[0]
    if word_count(first) > HOOK_MAX_WORDS:
        errors.append(f"Hook too long: '{first}' has {word_count(first)} words; the first sentence must be "
                      f"{HOOK_MAX_WORDS} words or fewer (2 to 3 seconds).")
    return errors


def style_warnings(data: dict) -> list[str]:
    """Flag writing that sounds generated instead of told (see the voice guide, section 2.4)."""
    warnings = []
    fields = {k: data.get(k, "") for k in ("subtitle", "backgroundHook", "realWorldCase", "closingCta")}
    if isinstance(data.get("script"), list):
        fields["script"] = " ".join(str(s.get("voiceover", "")) for s in data["script"] if isinstance(s, dict))
    for name, text in fields.items():
        sents = sentences(text)
        low = str(text).lower()
        run = 0
        for s in sents:
            run = run + 1 if word_count(s) <= 5 else 0
            if run == 3:
                warnings.append(f"{name}: three or more short sentences in a row (stiff rhythm) near '{s}'.")
        for phrase in STOCK_PHRASES:
            if phrase in low:
                warnings.append(f"{name}: stock phrase '{phrase}'.")
        colon_sents = [s for s in sents if ":" in s]
        if len(colon_sents) > 1:
            warnings.append(f"{name}: {len(colon_sents)} sentences use a colon reveal or dictated list "
                            f"(e.g. '{colon_sents[0]}'); tell it as a flowing sentence.")
        if re.search(r"\bpertama\b", low) and re.search(r"\bkedua\b", low):
            warnings.append(f"{name}: mechanical 'pertama ... kedua ...' enumeration; narrate it as a flow.")
        if low.count("simpelnya gini") > 1:
            warnings.append(f"{name}: 'simpelnya gini' used more than once.")
        if sum(1 for s in sents if s.lower().startswith("nah")) > 1:
            warnings.append(f"{name}: more than one sentence starts with 'Nah'.")
    if isinstance(data.get("script"), list) and data["script"]:
        body = [s for s in sentences(fields["script"])][1:]
        if body:
            avg = sum(word_count(s) for s in body) / len(body)
            if avg < 9:
                warnings.append(f"script: average sentence is {avg:.1f} words (choppy); aim for 10 to 22.")
        first = sentences(data["script"][0].get("voiceover", ""))
        if first and re.search(r"\badalah\b", first[0].lower()):
            warnings.append("script: the hook reads like a definition; open with a question or surprise instead.")
        secs = word_count(fields["script"]) / SPOKEN_WPM * 60 / VO_SPEED
        if not 40 <= secs <= 90:
            warnings.append(f"script: final reel about {secs:.0f} s ({SPOKEN_WPM} wpm recorded, {VO_SPEED}x speed); reels work best at 45 to 90 s.")
    return warnings


def recording_seconds(data: dict) -> float | None:
    """Estimated length of the raw recording at the creator's natural pace."""
    if not isinstance(data.get("script"), list):
        return None
    words = sum(word_count(s.get("voiceover", "")) for s in data["script"] if isinstance(s, dict))
    return round(words / SPOKEN_WPM * 60, 1)


def script_seconds(data: dict) -> float | None:
    """Estimated voiced length of the final reel (recording sped up VO_SPEED)."""
    rec = recording_seconds(data)
    return None if rec is None else round(rec / VO_SPEED, 1)


def validate_and_format(data: dict) -> tuple[str, list[str]]:
    errors = []

    required_fields = [
        "title",
        "subtitle",
        "category",
        "platform",
        "backgroundHook",
        "bridgingExplanation",
        "realWorldCase",
        "actionableSolution",
        "summaryPullQuote",
        "closingCta",
        "evidenceSources",
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: '{field}'")

    # Em-dash check across entire JSON dump
    raw_text = json.dumps(data)
    if "—" in raw_text or "–" in raw_text:
        errors.append("Banned character detected: Em-dash (—) or en-dash (–) found in content. Use colons, hyphens (-), or parentheses instead.")

    # Databro pronoun check: strictly banned lu/lo/loe/gue
    banned_match = re.search(r'\b(lu|lo|loe|gue)\b', raw_text, re.IGNORECASE)
    if banned_match:
        errors.append(f"Banned pronoun detected: '{banned_match.group(0)}' found in content. Databro persona strictly requires 'kamu' (or 'anda'/'kalian'). 'Bro' is permitted only as a greeting.")

    errors.extend(validate_cover(data))
    errors.extend(validate_script(data))

    # Source check
    sources = data.get("evidenceSources", [])
    if not sources:
        errors.append("Evidence sources missing: every Databro content idea must have verified source links or 'Source: Evergreen fundamentals'.")

    if errors:
        return "", errors

    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    status_str = data.get("status", "Idea 💡")
    format_type = data.get("formatType", "Carousel (8-part)")

    # Build bridging explanation section
    bridging = data["bridgingExplanation"]
    bridging_md = ""
    if isinstance(bridging, dict):
        bridging_md += f"{bridging.get('summary', '')}\n\n"
        comparison = bridging.get("comparison", [])
        if comparison:
            bridging_md += "| Element | Cara Kerja | Catatan |\n|---|---|---|\n"
            for row in comparison:
                elem = row.get("element", "")
                how = row.get("howItWorks", "")
                note = row.get("limitation", row.get("note", ""))
                bridging_md += f"| {elem} | {how} | {note} |\n"
    else:
        bridging_md = str(bridging)

    # Build actionable solution section
    actionable = data["actionableSolution"]
    actionable_md = ""
    if isinstance(actionable, dict):
        desc = actionable.get("description", "")
        code = actionable.get("code", "")
        actionable_md += f"{desc}\n\n"
        if code:
            actionable_md += f"```python\n{code}\n```"
    else:
        actionable_md = str(actionable)

    # Build sources section
    sources_md = ""
    for s in sources:
        if isinstance(s, dict):
            title = s.get("title", "Source")
            url = s.get("url", "")
            note = s.get("note", "")
            note_str = f" - {note}" if note else ""
            if url:
                sources_md += f"- [{title}]({url}){note_str}\n"
            else:
                sources_md += f"- {title}{note_str}\n"
        else:
            sources_md += f"- {s}\n"

    cover_md = ""
    if is_video_idea(data):
        c = data["cover"]
        cover_md = (
            "## Cover (video)\n"
            f"- **Headline**: {c['headline']}\n"
            f"- **Lime keyword**: {c['limeKeyword']}\n"
            f"- **Hook**: {c['hook']}\n"
            f"- **Key visual**: {c['visual']}\n\n---\n\n"
        )
        rows = "\n".join(
            f"| {i} | {s.get('beat', '')} | {s.get('voiceover', '')} | {s.get('visual', '')} |"
            for i, s in enumerate(data["script"], 1)
        )
        cover_md += (
            f"## Script (video, about {script_seconds(data)} s in the final reel: {SPOKEN_WPM} wpm recorded, sped up {VO_SPEED}x)\n"
            "| # | Beat | Voiceover | Visual |\n|---|---|---|---|\n"
            f"{rows}\n\n---\n\n"
        )

    md = f"""# [{data['platform']}] {data['title']}

> {data['subtitle']}

**Category**: {data['category']}  
**Target Platform**: {data['platform']}  
**Tone & Audience**: Casual Indonesian ("bro" tone) - Data practitioners & learners  
**Date**: {date_str}  
**Status**: {status_str}  
**Format Type**: {format_type}  

---

## 1. Title / Headline
{data['title']}

## 2. Subtitle / Framing Question
{data['subtitle']}

## 3. Background & Relatable Friction (Hook)
{data['backgroundHook']}

## 4. Bridging Explanation & Core Concept
{bridging_md.strip()}

## 5. Real-World Case Study & Benchmark Numbers
{data['realWorldCase']}

## 6. Actionable Solution / Future Knowledge
{actionable_md.strip()}

## 7. Summary Pull-Quote
> "{data['summaryPullQuote']}"

## 8. Closing Call-to-Action (CTA)
{data['closingCta']}

---

{cover_md}## Evidence & Verified Sources
{sources_md.strip()}
"""
    return md, []


def main():
    parser = argparse.ArgumentParser(description="Format and validate a Databro content idea.")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON content idea file")
    parser.add_argument("--output", "-o", help="Path to output markdown file (optional)")
    parser.add_argument("--json", action="store_true", help="Print result in machine-readable JSON format")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        res = {"status": "error", "message": f"Input file not found: {args.input}"}
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Error: {res['message']}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            res = {"status": "error", "message": f"Invalid JSON format: {e}"}
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"Error: {res['message']}", file=sys.stderr)
            sys.exit(1)

    md_output, errors = validate_and_format(data)

    if errors:
        res = {"status": "validation_failed", "errors": errors}
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("Validation Errors:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    out_path = args.output
    if not out_path:
        date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        out_path = f"content-idea-{date_str}.md"

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_output)

    res = {
        "status": "ok",
        "output_path": os.path.abspath(out_path),
        "title": data["title"],
        "category": data["category"],
        "platform": data["platform"],
        "word_count": len(md_output.split()),
        "sources_count": len(data.get("evidenceSources", [])),
        "has_cover": "cover" in data and is_video_idea(data),
        "script_seconds": script_seconds(data),
        "recording_seconds": recording_seconds(data),
        "styleWarnings": style_warnings(data),
    }

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Successfully formatted Databro content idea -> {out_path}")
        for w in res["styleWarnings"]:
            print(f"  style warning: {w}")


if __name__ == "__main__":
    main()

