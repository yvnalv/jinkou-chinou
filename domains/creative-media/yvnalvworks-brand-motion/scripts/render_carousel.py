#!/usr/bin/env python3
"""
Playwright-based slide and cover renderer for yvnalvworks carousels and reels.

Reads a spec JSON and renders 4:5 carousel slides (1080x1350) or a 9:16 reel
cover (1080x1920), exported at --scale (default 2x). Every slide sits on the brand grain background
(assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png), never a flat fill.

Spec format:
{
  "format": "feed",            // "feed" (4:5, default) or "reel" (9:16 reel/video cover)
  "slides": [
    {"type": "cover", "headline": "What AI Engineers\\nShould Know\\nAbout [[Microsoft\\nAgent Framework]]", "file": "cover.png"},
    {"type": "html", "html": "<div class='h2'>Body slide fragment</div>"},
    {"type": "html", "html": "<!doctype html><html>... full document ...</html>"}
  ]
}

Cover headline markup: "\\n" forces a line break, [[...]] marks the Electric
Lime highlight (may span line breaks). Without "\\n" the headline wraps
automatically inside the 860px measure.

HTML slides: a fragment (no <html> tag) is wrapped in the brand shell (grain
background, Poppins, 80px padding). A full document is rendered as-is after
token substitution: {{BG}} = grain background data URI, {{AVATAR}} = color
avatar data URI, {{FONTS}} = Google Fonts <link> tags.

Optional per-slide "file" sets the output name (default 01.png, 02.png, ...).
A reel cover uses the same lockup and headline as the feed cover, centered so it
survives the profile-grid crop (3:4 and 4:5 centered crops).

Prints a JSON summary to stdout.
"""

import argparse
import base64
import html as html_lib
import json
import os
import re
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: 'playwright' is required. Run 'pip install playwright && playwright install chromium'", file=sys.stderr)
    sys.exit(1)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG_PATH = os.path.join(SKILL_DIR, "assets", "brand-kit", "backgrounds", "yvnalvworks-grain-bg.png")
AVATAR_PATH = os.path.join(SKILL_DIR, "assets", "brand-kit", "logos", "yovan-avatar-color.png")

# format -> (width, height, cover stage padding)
FORMATS = {
    "feed": (1080, 1350, "0 40px 108px 0"),
    "reel": (1080, 1920, "0 40px 140px 0"),
}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700'
    '&family=JetBrains+Mono:wght@500&display=block" rel="stylesheet">'
)

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;overflow:hidden}
body{background:#121212 url({{BG}}) center/cover no-repeat;color:#F0ECE2;
  font-family:'Poppins',sans-serif;-webkit-font-smoothing:antialiased}
.hl{color:#C1FF72}
.mono{font-family:'JetBrains Mono',monospace;font-weight:500}
"""

COVER_CSS = """
.stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:__PAD__}
.block{display:flex;flex-direction:column;align-items:flex-start;max-width:860px}
.lockup{display:flex;align-items:center;gap:10px;margin-bottom:46px}
.lockup img{width:66px;height:66px;border-radius:50%;display:block}
.lockup .name{font-weight:600;font-size:24px;line-height:1.2;color:#FFFFFF;letter-spacing:-0.01em}
.lockup .handle{font-weight:400;font-size:21px;line-height:1.2;color:#F0ECE2}
.headline{font-weight:700;font-size:96px;line-height:1.02;letter-spacing:-0.04em;color:#FFFFFF;text-align:left}
"""

SHELL_CSS = """
.shell{position:absolute;inset:0;padding:80px;display:flex;flex-direction:column}
"""


def data_uri(path: str, mime: str) -> str:
    if not os.path.exists(path):
        print(f"Error: brand asset missing: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")


def headline_html(text: str) -> str:
    if text.count("[[") != text.count("]]"):
        raise ValueError("Unbalanced [[ ]] highlight markers in headline")
    escaped = html_lib.escape(text.strip())
    escaped = escaped.replace("[[", '<span class="hl">').replace("]]", "</span>")
    return escaped.replace("\n", "<br>")


def build_cover(slide: dict) -> str:
    headline = slide.get("headline", "")
    if not headline.strip():
        raise ValueError("Cover slide needs a non-empty 'headline'")
    name = html_lib.escape(slide.get("name", "yvnalvworks"))
    handle = html_lib.escape(slide.get("handle", "@yvnalvworks"))
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{BASE_CSS}{COVER_CSS}</style></head><body>
<div class="stage"><div class="block">
  <div class="lockup"><img src="{{{{AVATAR}}}}" alt="">
    <div><div class="name">{name}</div><div class="handle">{handle}</div></div></div>
  <div class="headline">{headline_html(headline)}</div>
</div></div></body></html>"""


def build_html(slide: dict) -> str:
    content = slide.get("html", "")
    if re.search(r"<html[\s>]", content, re.IGNORECASE):
        return content
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{BASE_CSS}{SHELL_CSS}</style></head><body><div class="shell">{content}</div></body></html>"""


def substitute(doc: str, tokens: dict, fmt: str = "feed") -> str:
    w, h, pad = FORMATS[fmt]
    doc = doc.replace("__W__", str(w)).replace("__H__", str(h)).replace("__PAD__", pad)
    for key, value in tokens.items():
        doc = doc.replace("{{" + key + "}}", value)
    return doc


def render_carousel(spec_path: str, output_dir: str, scale: float, fmt_override: str | None = None) -> dict:
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    fmt = fmt_override or spec.get("format", "feed")
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format '{fmt}' (use 'feed' or 'reel')")
    width, height, _ = FORMATS[fmt]
    slides = spec.get("slides", [])
    if not slides:
        raise ValueError("Spec has no 'slides'")

    tokens = {
        "BG": data_uri(BG_PATH, "image/png"),
        "AVATAR": data_uri(AVATAR_PATH, "image/png"),
        "FONTS": FONTS,
    }
    os.makedirs(output_dir, exist_ok=True)
    rendered = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
        for idx, slide in enumerate(slides, start=1):
            kind = slide.get("type", "html")
            if kind == "cover":
                doc = build_cover(slide)
            elif kind == "html":
                doc = build_html(slide)
            else:
                raise ValueError(f"Slide {idx}: unknown type '{kind}' (use 'cover' or 'html')")
            page.set_content(substitute(doc, tokens, fmt), wait_until="networkidle")
            fonts_ok = page.evaluate(
                "async () => { await document.fonts.ready; return document.fonts.check(\"700 96px Poppins\"); }"
            )
            out_file = os.path.join(output_dir, slide.get("file") or f"{idx:02d}.png")
            page.screenshot(path=out_file)
            entry = {"slide": idx, "type": kind, "file": out_file, "poppinsLoaded": fonts_ok}
            if kind == "cover":
                # A line wider than the 860px measure wraps silently; compare rendered vs intended lines.
                entry["headlineLines"] = page.evaluate(
                    "() => { const h = document.querySelector('.headline');"
                    " return Math.round(h.getBoundingClientRect().height / (96 * 1.02)); }"
                )
                entry["intendedLines"] = slide["headline"].strip().count("\n") + 1
            rendered.append(entry)
        browser.close()

    warnings = [
        f"Slide {r['slide']}: Poppins did not load (offline?); output used a fallback font"
        for r in rendered if not r["poppinsLoaded"]
    ]
    warnings += [
        f"Slide {r['slide']}: cover headline renders as {r['headlineLines']} lines but has "
        f"{r['intendedLines']} hand-broken lines; a line is too wide for the 860px measure, shorten or re-break it"
        for r in rendered
        if r["type"] == "cover" and r["intendedLines"] > 1 and r["headlineLines"] != r["intendedLines"]
    ]
    return {"format": fmt, "slides": rendered, "pixelSize": [int(width * scale), int(height * scale)], "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description="Render yvnalvworks 4:5 carousel slides or a 9:16 reel cover on the brand grain background")
    parser.add_argument("spec", help="Path to carousel spec JSON")
    parser.add_argument("--out", "-o", default="./slides", help="Output directory for rendered PNGs")
    parser.add_argument("--scale", type=float, default=2.0, help="Device scale factor (2 = 2x export)")
    parser.add_argument("--format", choices=sorted(FORMATS), help="Override the spec format: feed (4:5) or reel (9:16 cover)")
    args = parser.parse_args()

    if not os.path.exists(args.spec):
        print(f"Error: spec file '{args.spec}' not found.", file=sys.stderr)
        sys.exit(1)
    try:
        result = render_carousel(args.spec, args.out, args.scale, args.format)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["warnings"] else 0)


if __name__ == "__main__":
    main()
