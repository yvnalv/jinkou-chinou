#!/usr/bin/env python3
"""
Playwright-based 4:5 Slide Renderer for yvnalvworks Carousels.
Reads a carousel specification JSON file and renders pixel-perfect 1080x1350 PNG slides.
"""

import argparse
import json
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: 'playwright' is required. Run 'pip install playwright && playwright install chromium'", file=sys.stderr)
    sys.exit(1)


def render_carousel(spec_path: str, output_dir: str):
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    slides = spec.get("slides", [])
    total_slides = len(slides)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350, "device_scale_factor": 2})

        for idx, slide in enumerate(slides, start=1):
            slide_html = slide.get("html", "")
            page.set_content(slide_html, wait_until="networkidle")
            out_file = os.path.join(output_dir, f"{idx:02d}.png")
            page.screenshot(path=out_file)
            print(f"Rendered slide {idx:02d}/{total_slides:02d} -> {out_file}")

        browser.close()
    print("All slides rendered successfully.")


def main():
    parser = argparse.ArgumentParser(description="Render yvnalvworks 4:5 carousel slides")
    parser.add_argument("spec", help="Path to carousel-spec.json")
    parser.add_argument("--out", "-o", default="./slides", help="Output directory for rendered PNGs")
    args = parser.parse_args()

    if not os.path.exists(args.spec):
        print(f"Error: spec file '{args.spec}' not found.", file=sys.stderr)
        sys.exit(1)

    render_carousel(args.spec, args.out)


if __name__ == "__main__":
    main()
