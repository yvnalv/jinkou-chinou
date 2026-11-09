#!/usr/bin/env python3
"""Validate a Remotion project or component file for determinism, version parity, and safe-zone compliance.

Checks performed:
  1. Banned non-deterministic CSS animations (`transition:`, `@keyframes`, Tailwind `animate-*`).
  2. Banned non-deterministic JS timers (`setTimeout`, `setInterval`, `requestAnimationFrame`).
  3. Raw HTML `<img` or `<video` tags inside `.tsx`/`.jsx` files instead of `<Img`, `<Video`, `<OffthreadVideo`, or `@remotion/media`.
  4. Unclamped `interpolate(...)` calls missing `extrapolateLeft` or `extrapolateRight`.
  5. `package.json` Remotion package version parity (`remotion` and all `@remotion/*` packages must match exact versions without `^` or `~` drift).

Usage:
  python validate_remotion_project.py --path ./my-remotion-video
  python validate_remotion_project.py --path ./src/SceneTemplate.tsx --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List


@dataclass
class Finding:
    severity: str  # "ERROR" or "WARNING"
    rule: str
    file: str
    line: int
    message: str


CSS_TRANSITION_RE = re.compile(
    r"(?:\btransition\s*:|\btransitionProperty\s*:|\btransitionDuration\s*:)",
)
CSS_KEYFRAMES_RE = re.compile(r"@keyframes\b")
TAILWIND_ANIMATE_RE = re.compile(
    r"\banimate-(?:spin|ping|pulse|bounce|none)\b"
)
TIMER_RE = re.compile(
    r"\b(?:setTimeout|setInterval|requestAnimationFrame)\s*\("
)
RAW_IMG_TAG_RE = re.compile(r"<img\b")
RAW_VIDEO_TAG_RE = re.compile(r"<video\b")
INTERPOLATE_CALL_RE = re.compile(r"\binterpolate\s*\(\s*[^)\s]")

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "coverage"}
CODE_EXTENSIONS = {".tsx", ".ts", ".jsx", ".js", ".css"}


def scan_code_file(path: Path, root: Path) -> List[Finding]:
    findings: List[Finding] = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        findings.append(
            Finding(
                severity="ERROR",
                rule="file-read-error",
                file=str(path),
                line=1,
                message=f"Could not read file: {exc}",
            )
        )
        return findings

    rel_path = str(path.relative_to(root)) if path != root else path.name
    lines = content.splitlines()
    ext = path.suffix.lower()

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        if CSS_TRANSITION_RE.search(line):
            findings.append(
                Finding(
                    severity="ERROR",
                    rule="no-css-transition",
                    file=rel_path,
                    line=idx,
                    message="CSS transitions cause flickering in headless Remotion renders. Drive animations via useCurrentFrame() + spring()/interpolate().",
                )
            )

        if CSS_KEYFRAMES_RE.search(line):
            findings.append(
                Finding(
                    severity="ERROR",
                    rule="no-css-keyframes",
                    file=rel_path,
                    line=idx,
                    message="CSS @keyframes are not synchronized with Remotion's frame clock. Use useCurrentFrame() instead.",
                )
            )

        if TAILWIND_ANIMATE_RE.search(line):
            findings.append(
                Finding(
                    severity="ERROR",
                    rule="no-tailwind-animate",
                    file=rel_path,
                    line=idx,
                    message="Tailwind animate-* classes rely on CSS keyframes and break frame-accurate rendering.",
                )
            )

        if ext in {".tsx", ".ts", ".jsx", ".js"}:
            if TIMER_RE.search(line):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule="no-wallclock-timers",
                        file=rel_path,
                        line=idx,
                        message="Wall-clock timers (setTimeout/setInterval/requestAnimationFrame) break deterministic rendering. Derive state from useCurrentFrame().",
                    )
                )

        if ext in {".tsx", ".jsx"}:
            if RAW_IMG_TAG_RE.search(line):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule="no-raw-img-tag",
                        file=rel_path,
                        line=idx,
                        message="Raw <img> tag detected. Use <Img> from 'remotion' so frame rendering waits for image decode.",
                    )
                )
            if RAW_VIDEO_TAG_RE.search(line):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule="no-raw-video-tag",
                        file=rel_path,
                        line=idx,
                        message="Raw <video> tag detected. Use <OffthreadVideo> from 'remotion' or <Video> from '@remotion/media'.",
                    )
                )

    # Check multi-line interpolate(...) calls for extrapolateRight / extrapolateLeft
    if ext in {".tsx", ".ts", ".jsx", ".js"}:
        for match in INTERPOLATE_CALL_RE.finditer(content):
            start_pos = match.start()
            line_num = content.count("\n", 0, start_pos) + 1
            line_str = lines[line_num - 1].strip() if line_num <= len(lines) else ""
            if line_str.startswith("//") or line_str.startswith("/*") or line_str.startswith("*"):
                continue
            # Inspect a window of 450 characters after `interpolate(`
            window = content[start_pos : start_pos + 450]
            if "extrapolateRight" not in window and "extrapolateLeft" not in window:
                findings.append(
                    Finding(
                        severity="WARNING",
                        rule="unclamped-interpolate",
                        file=rel_path,
                        line=line_num,
                        message="interpolate() call does not specify extrapolateLeft or extrapolateRight. Pass extrapolateRight: 'clamp' unless unbounded extrapolation is intentional.",
                    )
                )

    return findings


def check_package_json(pkg_path: Path, root: Path) -> List[Finding]:
    findings: List[Finding] = []
    rel_path = str(pkg_path.relative_to(root)) if pkg_path != root else pkg_path.name
    try:
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(
            Finding(
                severity="ERROR",
                rule="invalid-package-json",
                file=rel_path,
                line=1,
                message=f"Failed to parse package.json: {exc}",
            )
        )
        return findings

    deps = {}
    for section in ("dependencies", "devDependencies"):
        section_dict = data.get(section, {})
        if isinstance(section_dict, dict):
            deps.update(section_dict)

    remotion_pkgs = {
        k: v
        for k, v in deps.items()
        if k == "remotion" or k.startswith("@remotion/")
    }
    if not remotion_pkgs:
        return findings

    normalized_versions = set()
    for pkg_name, ver_spec in remotion_pkgs.items():
        if not isinstance(ver_spec, str):
            continue
        if ver_spec.startswith("^") or ver_spec.startswith("~"):
            findings.append(
                Finding(
                    severity="WARNING",
                    rule="unpinned-remotion-version",
                    file=rel_path,
                    line=1,
                    message=f"Package '{pkg_name}' uses range specifier '{ver_spec}'. Pin exact versions across all Remotion packages to prevent version mismatch crashes.",
                )
            )
        normalized_versions.add(ver_spec.lstrip("^~"))

    if len(normalized_versions) > 1:
        versions_summary = ", ".join(f"{k}={v}" for k, v in sorted(remotion_pkgs.items()))
        findings.append(
            Finding(
                severity="ERROR",
                rule="remotion-version-mismatch",
                file=rel_path,
                line=1,
                message=f"Mismatched Remotion package versions detected ({versions_summary}). All 'remotion' and '@remotion/*' packages must use the exact same version.",
            )
        )

    return findings


def validate_target(target_path: Path) -> List[Finding]:
    findings: List[Finding] = []
    if not target_path.exists():
        findings.append(
            Finding(
                severity="ERROR",
                rule="path-not-found",
                file=str(target_path),
                line=1,
                message=f"Target path does not exist: {target_path}",
            )
        )
        return findings

    if target_path.is_file():
        if target_path.name == "package.json":
            findings.extend(check_package_json(target_path, target_path.parent))
        elif target_path.suffix.lower() in CODE_EXTENSIONS:
            findings.extend(scan_code_file(target_path, target_path.parent))
        return findings

    pkg_json = target_path / "package.json"
    if pkg_json.is_file():
        findings.extend(check_package_json(pkg_json, target_path))

    for file_path in sorted(target_path.rglob("*")):
        if any(part in SKIP_DIRS for part in file_path.parts):
            continue
        if file_path.is_file() and file_path.suffix.lower() in CODE_EXTENSIONS:
            findings.extend(scan_code_file(file_path, target_path))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Remotion components and projects for deterministic rendering and version parity."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to a Remotion project directory or a single .tsx/.ts/.css file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit validation findings as JSON.",
    )
    args = parser.parse_args()

    target = Path(args.path).resolve()
    findings = validate_target(target)
    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARNING"]

    if args.json:
        print(
            json.dumps(
                {
                    "target": str(target),
                    "error_count": len(errors),
                    "warning_count": len(warnings),
                    "passed": len(errors) == 0,
                    "findings": [asdict(f) for f in findings],
                },
                indent=2,
            )
        )
    else:
        print(f"Remotion Determinism & Parity Audit: {target}")
        print("=" * 68)
        if not findings:
            print("PASS: 0 errors, 0 warnings. All inspected files follow Remotion rules.")
        else:
            for item in findings:
                print(
                    f"[{item.severity}] {item.file}:{item.line} ({item.rule}) -> {item.message}"
                )
            print("-" * 68)
            print(
                f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)."
            )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
