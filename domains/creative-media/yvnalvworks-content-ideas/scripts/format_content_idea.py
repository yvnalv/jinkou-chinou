#!/usr/bin/env python3
"""
Format and validate a yvnalvworks content idea into the five story beats.
Enforces completeness, valid citations, English only, and zero em-dashes.
JSON keys keep their original names: hookStatement = the moment, industryTension = the problem,
architecturalFramework = the turn, goldenRule = the lesson, takeawayAndCta = the next step.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime


MAX_COVER_LINE_CHARS = 18


def validate_cover_headline(headline: str) -> list[str]:
    """Check a cover headline against references/cover-headline-patterns.md."""
    errors = []
    opens, closes = headline.count("[["), headline.count("]]")
    if opens != closes:
        errors.append("coverHeadline: unbalanced [[ ]] highlight markers.")
    elif opens != 1:
        errors.append(f"coverHeadline: needs exactly one [[highlight]] phrase, found {opens}.")
    lines = [ln.strip() for ln in headline.replace("[[", "").replace("]]", "").split("\n")]
    if any(not ln for ln in lines):
        errors.append("coverHeadline: contains an empty line.")
    if not 3 <= len(lines) <= 4:
        errors.append(f"coverHeadline: use 3 to 4 hand-broken lines (\\n), found {len(lines)}.")
    for ln in lines:
        if len(ln) > MAX_COVER_LINE_CHARS:
            errors.append(f"coverHeadline: line '{ln}' is {len(ln)} characters; max is {MAX_COVER_LINE_CHARS}.")
    if headline.rstrip().endswith((".", "!", "?", ":")):
        errors.append("coverHeadline: no trailing punctuation.")
    return errors


def validate_and_format(data: dict) -> tuple[str, list[str]]:
    errors = []

    required_fields = [
        "title",
        "pillar",
        "platform",
        "hookStatement",
        "industryTension",
        "architecturalFramework",
        "goldenRule",
        "takeawayAndCta",
        "evidenceSources",
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: '{field}'")

    raw_text = json.dumps(data)
    if "—" in raw_text or "–" in raw_text:
        errors.append("Banned character detected: Em-dash (—) or en-dash (–) found. Use colons, parentheses, or clean separate sentences.")

    # Validate English only
    indonesian_words = [" yang ", " dan ", " di ", " ini ", " untuk ", " dengan ", " tidak "]
    for w in indonesian_words:
        if w in raw_text.lower():
            errors.append(f"Non-English word detected ('{w.strip()}'). yvnalvworks content must be in English.")
            break

    is_carousel = "carousel" in str(data.get("platform", "")).lower()
    cover = data.get("coverHeadline", "")
    if is_carousel and not cover:
        errors.append("Missing required field for carousels: 'coverHeadline' (see references/cover-headline-patterns.md)")
    elif cover:
        errors.extend(validate_cover_headline(cover))

    sources = data.get("evidenceSources", [])
    if not sources:
        errors.append("Evidence sources missing: every yvnalvworks content idea must cite verified papers, docs, or benchmarks.")

    if errors:
        return "", errors

    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    cover_block = ""
    if cover:
        cover_lines, in_hl = [], False
        for raw in cover.split("\n"):
            line = ("[[" if in_hl else "") + raw
            in_hl = line.count("[[") > line.count("]]")
            line += "]]" if in_hl else ""
            cover_lines.append(line.replace("[[", "**").replace("]]", "**"))
        cover_block = "**Cover headline:**\n\n" + "\n".join(f"> {ln}  " for ln in cover_lines) + "\n\n"

    md = f"""# {data['title']}

- **Pillar**: {data['pillar']}
- **Platform**: {data['platform']}
- **Date**: {date_str}
- **Author**: Yovan Alvianto (@yvnalvworks)
- **Status**: {data.get('status', 'Idea 💡')}

---

## 1. Cover + The Moment
{cover_block}**Hook (caption and reel opener):** {data['hookStatement']}

## 2. The Problem
{data['industryTension']}

## 3. The Turn (How It Actually Works)
{data['architecturalFramework']}

## 4. The Lesson
{data['goldenRule']}

## 5. The Next Step & CTA
{data['takeawayAndCta']}

---

## Verified Evidence Sources
"""
    for src in sources:
        md += f"- {src}\n"

    return md, []


def main():
    # Status values carry emoji; Windows consoles and pipes default to cp1252.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Format and validate a yvnalvworks content idea")
    parser.add_argument("input_json", help="Path to content idea JSON file")
    parser.add_argument("--out", "-o", help="Path to write output markdown")
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"Error: input file '{args.input_json}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    md, errors = validate_and_format(data)
    if errors:
        print("Validation failed with errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Formatted content idea written to: {args.out}")
    else:
        print(md)


if __name__ == "__main__":
    main()
