#!/usr/bin/env python3
"""Screenshot an HTML file or URL at several widths, colour schemes, and prototype states.

Uses a locally installed Chromium-based browser (Chrome, Edge, Chromium, Brave)
in headless mode with a throwaway profile, so it never touches the user's
browser profile. Look at every image: static lint cannot see overlapping
elements, horizontal overflow, clipped text, or states that render together.

States and themes are passed in the URL hash (#state=empty&theme=dark), which
the the-uix-designer prototype starter understands. Other pages simply ignore
the hash; the colour scheme is also forced through the browser.

Examples:
  python screenshot.py design/prototype/index.html
  python screenshot.py design/prototype/index.html --widths 1280,390 --schemes light,dark --states default,empty,error
  python screenshot.py http://localhost:5173/settings --widths 1440,768,375 --height 1400 --out design/shots

Exit codes: 0 ok, 1 some screenshots failed, 3 no browser found (then review in a browser by hand).
Standard library only.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

MIN_WINDOW_WIDTH = 500  # Chromium's minimum headless window width

CANDIDATES = {
    "win32": [
        r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        r"%LocalAppData%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
    ],
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ],
    "linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser"],
}
SCHEME_SETTING = {"dark": "0", "light": "1"}  # Blink preferredColorScheme values


def find_browser(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() or shutil.which(explicit) else None
    env = os.environ.get("CHROME_PATH") or os.environ.get("BROWSER_PATH")
    if env and (Path(env).exists() or shutil.which(env)):
        return env
    platform = "win32" if sys.platform.startswith("win") else "darwin" if sys.platform == "darwin" else "linux"
    for candidate in CANDIDATES[platform]:
        expanded = os.path.expandvars(candidate)
        if Path(expanded).exists():
            return expanded
        found = shutil.which(expanded)
        if found:
            return found
    return None


def to_url(target: str) -> str:
    if "://" in target:
        return target
    path = Path(target).resolve()
    if not path.is_file():
        sys.exit(f"error: file not found: {target}")
    return path.as_uri()


def _unfilter(line: bytearray, prev: bytearray, ftype: int, bpp: int) -> None:
    for i in range(len(line)):
        a = line[i - bpp] if i >= bpp else 0
        b = prev[i]
        if ftype == 1:
            line[i] = (line[i] + a) & 0xFF
        elif ftype == 2:
            line[i] = (line[i] + b) & 0xFF
        elif ftype == 3:
            line[i] = (line[i] + ((a + b) >> 1)) & 0xFF
        elif ftype == 4:
            c = prev[i - bpp] if i >= bpp else 0
            p = a + b - c
            pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
            line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 0xFF


def crop_png_width(path: Path, width: int) -> bool:
    """Crop an 8-bit RGB/RGBA PNG to the given width (standard library only)."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    pos, chunks = 8, []
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunks.append((data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]))
        pos += 12 + length
    w, h, depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", chunks[0][1])
    if depth != 8 or color_type not in (2, 6) or interlace or width >= w:
        return width >= w
    bpp = 3 if color_type == 2 else 4
    raw = zlib.decompress(b"".join(body for kind, body in chunks if kind == b"IDAT"))
    stride, prev, out, i = w * bpp, bytearray(w * bpp), bytearray(), 0
    for _ in range(h):
        ftype, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        _unfilter(line, prev, ftype, bpp)
        prev = line
        out += b"\x00" + line[:width * bpp]

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, h, 8, color_type, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(out), 6)) + chunk(b"IEND", b""))
    return True


def shoot(browser: str, url: str, out: Path, width: int, height: int, scheme: str, profile: str, timeout: int) -> bool:
    target, window_width = url, width
    if width < MIN_WINDOW_WIDTH:
        # Chromium will not make a window narrower than ~500px, so a 390px request would silently lay the
        # page out at 500px. Load it in an iframe of the exact width instead, then crop the image.
        wrapper = Path(profile) / f"frame-{width}x{height}.html"
        wrapper.write_text(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>frame</title>"
            "<style>html,body{margin:0}iframe{display:block;border:0;"
            f"width:{width}px;height:{height}px}}</style></head><body>"
            f"<iframe title=\"page\" src=\"{html.escape(url, quote=True)}\"></iframe></body></html>",
            encoding="utf-8",
        )
        target, window_width = wrapper.as_uri(), MIN_WINDOW_WIDTH
    args = [
        browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
        "--no-default-browser-check", "--disable-extensions", "--allow-file-access-from-files",
        f"--user-data-dir={profile}", f"--window-size={window_width},{height}", f"--screenshot={out}",
        "--virtual-time-budget=2000", f"--blink-settings=preferredColorScheme={SCHEME_SETTING[scheme]}", target,
    ]
    try:
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return False
    if not (out.is_file() and out.stat().st_size > 0):
        return False
    return crop_png_width(out, width) if width < MIN_WINDOW_WIDTH else True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for examples.")
    parser.add_argument("target", help="HTML file path or http(s) URL")
    parser.add_argument("--widths", default="1280,768,390", help="comma list of viewport widths (default 1280,768,390)")
    parser.add_argument("--height", type=int, default=1000, help="viewport height; screenshots capture the viewport only")
    parser.add_argument("--schemes", default="light,dark", help="comma list: light,dark")
    parser.add_argument("--states", default="", help="comma list of prototype states passed as #state=...")
    parser.add_argument("--out", default="design/screenshots", help="output directory (default design/screenshots)")
    parser.add_argument("--browser", help="path to a Chromium-based browser executable")
    parser.add_argument("--timeout", type=int, default=60, help="seconds per screenshot")
    args = parser.parse_args(argv)

    browser = find_browser(args.browser)
    if not browser:
        print("No Chromium-based browser found (Chrome, Edge, Chromium, Brave). Pass --browser or set CHROME_PATH, "
              "or review the page in a browser by hand.", file=sys.stderr)
        return 3
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    schemes = [s.strip() for s in args.schemes.split(",") if s.strip()]
    bad = [s for s in schemes if s not in SCHEME_SETTING]
    if bad:
        sys.exit(f"error: unknown scheme(s): {', '.join(bad)}")
    states = [s.strip() for s in args.states.split(",") if s.strip()] or [None]
    base_url = to_url(args.target).split("#")[0]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(base_url.rstrip("/").split("/")[-1] or "page").stem or "page"

    results, failures = [], 0
    with tempfile.TemporaryDirectory(prefix="uix-shot-") as profile:
        for state in states:
            for scheme in schemes:
                for width in widths:
                    params = [f"theme={scheme}"] + ([f"state={state}"] if state else [])
                    url = f"{base_url}#{'&'.join(params)}"
                    name = "-".join(filter(None, [stem, state, scheme, f"{width}w"])) + ".png"
                    path = out_dir / name
                    ok = shoot(browser, url, path, width, args.height, scheme, profile, args.timeout)
                    failures += 0 if ok else 1
                    results.append({"file": str(path), "width": width, "scheme": scheme, "state": state, "ok": ok})
                    print(f"{'ok  ' if ok else 'FAIL'} {path}")
    (out_dir / "screenshots.json").write_text(json.dumps({"browser": browser, "screenshots": results}, indent=2),
                                             encoding="utf-8")
    print(f"\n{len(results) - failures}/{len(results)} screenshot(s) written to {out_dir} "
          f"(index: screenshots.json). Open and review each one.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
