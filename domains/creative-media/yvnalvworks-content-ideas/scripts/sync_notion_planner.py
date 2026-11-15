#!/usr/bin/env python3
"""
Notion Content Planner Sync Helper for yvnalvworks.
Transforms a yvnalvworks content idea (or reel.json) into Notion properties for the
'📆 yvnalvworks Content Planner' database. Prints the properties as JSON, and with
--markdown also writes a Markdown handoff file (database, properties table, optional page
body) for another agent or tool that has Notion access to create the page.
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


def build_handoff_markdown(props: dict, body: str = "") -> str:
    lines = [
        f"# Notion handoff: {props['Name']}",
        "",
        f"Create one page in the **📆 yvnalvworks Content Planner** database (`{DEFAULT_DATABASE_ID}`) "
        "with these properties, then paste the page content below it.",
        "",
        "| Property | Value |",
        "|---|---|",
    ]
    for key, value in props.items():
        label = "Publication Date (start)" if key == "date:Publication Date:start" else key
        lines.append(f"| {label} | {str(value).replace('|', '/')} |")
    if body.strip():
        lines += ["", "## Page content", "", body.strip()]
    return "\n".join(lines) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Build Notion payload for yvnalvworks Content Planner")
    parser.add_argument("input_json", help="Path to content idea JSON file (or reel.json)")
    parser.add_argument("--markdown", help="Also write a Markdown handoff file to this path")
    parser.add_argument("--body", help="Markdown file to include as the page content in the handoff")
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"Error: input file '{args.input_json}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    props = build_notion_properties(data)
    if args.markdown:
        body = ""
        if args.body:
            with open(args.body, "r", encoding="utf-8") as f:
                body = f.read()
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(build_handoff_markdown(props, body))
    print(json.dumps(props, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
