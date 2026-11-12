#!/usr/bin/env python3
"""
Notion Content Planner Sync Helper for yvnalvworks.
Transforms a yvnalvworks content idea into Notion properties schema for the
'📆 yvnalvworks Content Planner' database.
"""

import argparse
import json
import os
import sys

DEFAULT_DATABASE_ID = "5a915afd-b3c1-8274-836c-87fe398765ee"
PARENT_PAGE_ID = "23715afd-b3c1-8005-a71d-d220cf1c636f"


def build_notion_properties(data: dict) -> dict:
    platform = data.get("platform", "Instagram")
    post_type = data.get("postType", "Post")

    prefix = "(Post)"
    if "Reels" in post_type or "Video" in platform:
        prefix = "(Video)"
        post_type = "Reels"
    elif "Article" in post_type or "Blog" in platform:
        prefix = "(Article)"
        post_type = "Article"

    page_title = f"{prefix} {data['title']}"

    # Category mapping
    pillar = data.get("pillar", "AI Engineering")
    cat = "Education"
    if "Vision" in pillar:
        cat = "Study Case"
    elif "Architecture" in pillar:
        cat = "Insights"
    elif "MLOps" in pillar:
        cat = "Tutorial"

    props = {
        "Name": page_title,
        "Platform": "Instagram" if "Instagram" in platform else ("Linkedin" if "LinkedIn" in platform else "Website"),
        "Post Type": post_type,
        "Category": cat,
        "Status": data.get("status", "Idea 💡"),
    }

    if "date" in data:
        props["date:Publication Date:start"] = data["date"]

    if "link" in data:
        props["Link"] = data["link"]

    return props


def main():
    parser = argparse.ArgumentParser(description="Build Notion payload for yvnalvworks Content Planner")
    parser.add_argument("input_json", help="Path to content idea JSON file")
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"Error: input file '{args.input_json}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    props = build_notion_properties(data)
    print(json.dumps(props, indent=2))


if __name__ == "__main__":
    main()
