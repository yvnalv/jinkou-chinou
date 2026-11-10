#!/usr/bin/env python3
"""
Notion Content Planner Sync Helper for Databro.
Transforms a Databro content idea into Notion block schema or dispatches it
to the '📆 Databro Content Planner' database.
"""

import argparse
import json
import os
import sys

DEFAULT_DATABASE_ID = "23e15afd-b3c1-81b6-8bdc-000bba4d54c4"
DEFAULT_ASSIGNEE_ID = "9021b873-2895-42d9-b8ec-44eb292dbae1"


def build_notion_payload(data: dict, database_id: str = DEFAULT_DATABASE_ID, assignee_id: str = DEFAULT_ASSIGNEE_ID) -> dict:
    platform = data.get("platform", "Instagram Carousel")
    format_type = data.get("formatType", "Carousel (8-part)")

    # Format title prefix
    prefix = "(Post)"
    if "Video" in platform or "Reels" in format_type or "TikTok" in platform:
        prefix = "(Video)"
    elif "Article" in platform or "Blog" in format_type:
        prefix = "(Article)"
    elif "Thread" in platform or "X" in platform or "Twitter" in platform:
        prefix = "(Thread)"

    page_title = f"{prefix} {data['title']}"

    # Map category to Notion select options: Education, Tutorial, Study Case, Insights, Article, Carousel, Casual, Professional
    cat_str = data.get("category", "")
    if "Tutorial" in cat_str or "How-To" in cat_str:
        notion_cat = "Tutorial"
    elif "Dataset" in cat_str or "Case" in cat_str or "Domain" in cat_str:
        notion_cat = "Study Case"
    elif "News" in cat_str or "Trends" in cat_str or "RAG" in cat_str:
        notion_cat = "Insights"
    else:
        notion_cat = "Education"

    # Map platform option
    if "Instagram" in platform:
        notion_platform = "Instagram"
    elif "LinkedIn" in platform:
        notion_platform = "Linkedin"
    elif "TikTok" in platform:
        notion_platform = "TikTok"
    elif "X" in platform or "Twitter" in platform:
        notion_platform = "Tweet"
    else:
        notion_platform = "Instagram"

    post_type = "Post" if prefix == "(Post)" else prefix.strip("()")

    # Construct Children Blocks
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Framing & Background"}}]
            }
        },
        {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": data.get("subtitle", "")}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": data.get("backgroundHook", "")}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Core Concept Breakdown"}}]
            }
        }
    ]

    bridging = data.get("bridgingExplanation", {})
    if isinstance(bridging, dict):
        summary_text = bridging.get("summary", "")
        if summary_text:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": summary_text}}]
                }
            })
    else:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": str(bridging)}}]
            }
        })

    children.extend([
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Real-World Case Study"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": data.get("realWorldCase", "")}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Actionable Takeaway"}}]
            }
        }
    ])

    actionable = data.get("actionableSolution", {})
    if isinstance(actionable, dict):
        desc = actionable.get("description", "")
        if desc:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": desc}}]
                }
            })
        code = actionable.get("code", "")
        if code:
            children.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": code}}],
                    "language": "python"
                }
            })
    else:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": str(actionable)}}]
            }
        })

    children.extend([
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Summary Insight"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": data.get("summaryPullQuote", "")}}],
                "icon": {"type": "emoji", "emoji": "💡"}
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"CTA: {data.get('closingCta', '')}"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Evidence & Sources"}}]
            }
        }
    ])

    for s in data.get("evidenceSources", []):
        if isinstance(s, dict):
            t = s.get("title", "Source Link")
            u = s.get("url", "")
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": t, "link": {"url": u} if u else None}}
                    ]
                }
            })
        else:
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": str(s)}}]
                }
            })

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": page_title}}]
            },
            "Status": {
                "select": {"name": "Idea 💡"}
            },
            "Platform": {
                "select": {"name": notion_platform}
            },
            "Post Type": {
                "select": {"name": post_type}
            },
            "Category": {
                "select": {"name": notion_cat}
            },
            "Assign": {
                "people": [{"id": assignee_id}]
            }
        },
        "children": children
    }
    return payload


def main():
    parser = argparse.ArgumentParser(description="Sync or build Notion payload for Databro content planner.")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON content idea file")
    parser.add_argument("--dry-run", action="store_true", help="Print payload schema without making network API calls")
    parser.add_argument("--output-payload", "-o", help="Save the compiled Notion API payload JSON to file")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = build_notion_payload(data)

    if args.output_payload:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_payload)), exist_ok=True)
        with open(args.output_payload, "w", encoding="utf-8") as pf:
            json.dump(payload, pf, indent=2)
        print(f"Saved Notion API payload to {args.output_payload}")

    if args.dry_run or not args.output_payload:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

