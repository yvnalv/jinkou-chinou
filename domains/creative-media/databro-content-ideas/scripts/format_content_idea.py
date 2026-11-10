#!/usr/bin/env python3
"""
Format and validate a Databro content idea into the standard 8-part markdown schema.
Enforces technical completeness, valid citations, and zero em-dashes.
"""

import argparse
import json
import os
import sys
from datetime import datetime


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

## Evidence & Verified Sources
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
    }

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Successfully formatted Databro content idea -> {out_path}")


if __name__ == "__main__":
    main()

