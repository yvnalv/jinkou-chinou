#!/usr/bin/env python3
"""
Format and validate a yvnalvworks technical content idea into the standard 5-part schema.
Enforces technical completeness, valid citations, 100% Technical English, and zero em-dashes.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime


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
            errors.append(f"Non-English word detected ('{w.strip()}'). yvnalvworks content must be 100% Technical English.")
            break

    sources = data.get("evidenceSources", [])
    if not sources:
        errors.append("Evidence sources missing: every yvnalvworks content idea must cite verified papers, docs, or benchmarks.")

    if errors:
        return "", errors

    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    md = f"""# {data['title']}

- **Pillar**: {data['pillar']}
- **Platform**: {data['platform']}
- **Date**: {date_str}
- **Author**: Yovan Alvianto (@yvnalvworks)
- **Status**: {data.get('status', 'Idea 💡')}

---

## 1. Bold Statement Hook
{data['hookStatement']}

## 2. Industry Tension / Anti-Pattern
{data['industryTension']}

## 3. Architectural Framework
{data['architecturalFramework']}

## 4. Golden Rule / Engineering Law
{data['goldenRule']}

## 5. Takeaway & Portfolio CTA
{data['takeawayAndCta']}

---

## Verified Evidence Sources
"""
    for src in sources:
        md += f"- {src}\n"

    return md, []


def main():
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
