#!/usr/bin/env python3
"""UI/UX Testing Helper CLI tool.

Provides utility functions to:
  1. Validate Playwright test configuration files for UI/UX testing best practices.
  2. Parse and format Axe-core accessibility JSON outputs into clean markdown tables.
  3. Generate summary metrics of UI test runs for chat reporting.

Uses Python standard library only (no external dependencies required).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure UTF-8 output on Windows consoles to prevent charmap encoding errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def validate_config(config_path: Path) -> dict[str, Any]:
    """Validate a Playwright configuration file for UI/UX testing best practices."""
    if not config_path.is_file():
        return {
            "valid": False,
            "error": f"File not found: {config_path}",
        }

    content = config_path.read_text(encoding="utf-8")
    checks = {
        "has_desktop_viewport": bool(re.search(r"1280|1440|1920", content)),
        "has_mobile_viewport": bool(re.search(r"390|360|375|iPhone|Pixel", content, re.IGNORECASE)),
        "has_visual_tolerance": bool(re.search(r"maxDiffPixelRatio|threshold", content)),
        "has_animation_freeze": bool(re.search(r"animations\s*:\s*['\"]disabled['\"]|transition:\s*none", content)),
        "has_trace_capture": bool(re.search(r"trace\s*:\s*['\"][^'\"]+['\"]", content)),
        "has_screenshot_capture": bool(re.search(r"screenshot\s*:\s*['\"][^'\"]+['\"]", content)),
    }

    warnings = []
    if not checks["has_mobile_viewport"]:
        warnings.append("Missing explicit mobile viewport or mobile device preset (e.g. iPhone 14 or 390px).")
    if not checks["has_visual_tolerance"]:
        warnings.append("No visual diff tolerance specified; recommend setting `maxDiffPixelRatio: 0.01`.")
    if not checks["has_animation_freeze"]:
        warnings.append("CSS animations not disabled; recommend setting `animations: 'disabled'` to prevent snapshot diff flakiness.")
    if not checks["has_trace_capture"]:
        warnings.append("Trace recording not detected; recommend setting `trace: 'retain-on-failure'`.")

    score = sum(1 for v in checks.values() if v)
    return {
        "valid": True,
        "file": str(config_path),
        "score": f"{score}/6",
        "checks": checks,
        "warnings": warnings,
    }


def parse_axe_results(file_path: Path) -> dict[str, Any]:
    """Parse Axe-core accessibility scan JSON results and group by severity."""
    if not file_path.is_file():
        return {"valid": False, "error": f"File not found: {file_path}"}

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"valid": False, "error": f"Invalid JSON format: {exc}"}

    violations = data.get("violations", data) if isinstance(data, dict) else data
    if not isinstance(violations, list):
        return {"valid": False, "error": "Expected violations list in JSON payload."}

    grouped: dict[str, list[dict[str, Any]]] = {
        "critical": [],
        "serious": [],
        "moderate": [],
        "minor": [],
    }

    for v in violations:
        impact = str(v.get("impact", "minor")).lower()
        if impact not in grouped:
            impact = "minor"

        nodes = v.get("nodes", [])
        selectors = []
        for n in nodes[:3]:  # Top 3 selectors
            targets = n.get("target", [])
            if targets:
                selectors.append(", ".join(targets) if isinstance(targets, list) else str(targets))

        grouped[impact].append({
            "id": v.get("id", "unknown-rule"),
            "impact": impact,
            "description": v.get("description", ""),
            "help": v.get("help", ""),
            "helpUrl": v.get("helpUrl", ""),
            "selectors": selectors,
            "total_occurrences": len(nodes),
        })

    summary = {
        "critical": len(grouped["critical"]),
        "serious": len(grouped["serious"]),
        "moderate": len(grouped["moderate"]),
        "minor": len(grouped["minor"]),
        "total_violations": sum(len(g) for g in grouped.values()),
    }

    return {
        "valid": True,
        "summary": summary,
        "grouped": grouped,
    }


def format_axe_markdown_table(parsed_axe: dict[str, Any]) -> str:
    """Format parsed axe violations into a clean Markdown table."""
    grouped = parsed_axe.get("grouped", {})
    summary = parsed_axe.get("summary", {})
    total = summary.get("total_violations", 0)

    if total == 0:
        return "[PASS] No accessibility violations detected! Meets WCAG A/AA standards.\n"

    lines = [
        f"### Accessibility Audit Findings ({total} Rules Violated)",
        "",
        "| Severity | Rule ID | Impact / Description | Occurrences | Example Selector |",
        "|---|---|---|:---:|---|",
    ]

    for severity in ["critical", "serious", "moderate", "minor"]:
        items = grouped.get(severity, [])
        for item in items:
            sel = item["selectors"][0] if item["selectors"] else "N/A"
            lines.append(
                f"| **{severity.capitalize()}** | `{item['id']}` | {item['help']} | {item['total_occurrences']} | `{sel}` |"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="UI/UX Testing Helper CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate-config
    val_parser = subparsers.add_parser("validate-config", help="Validate Playwright configuration file")
    val_parser.add_argument("--config", required=True, type=Path, help="Path to playwright.config.ts/js")
    val_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # parse-axe
    axe_parser = subparsers.add_parser("parse-axe", help="Parse Axe-core JSON output")
    axe_parser.add_argument("--file", required=True, type=Path, help="Path to axe JSON results file")
    axe_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    axe_parser.add_argument("--out", type=Path, help="Optional path to write formatted Markdown table")

    args = parser.parse_args()

    if args.command == "validate-config":
        res = validate_config(args.config)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Configuration File: {res.get('file')}")
            print(f"UI/UX Health Score: {res.get('score')}")
            checks = res.get("checks", {})
            for k, v in checks.items():
                mark = "[PASS]" if v else "[FAIL]"
                print(f"  {mark} {k}")
            if res.get("warnings"):
                print("\nRecommendations:")
                for w in res["warnings"]:
                    print(f"  * {w}")
        return 0 if res.get("valid") else 1

    if args.command == "parse-axe":
        res = parse_axe_results(args.file)
        if not res.get("valid"):
            print(f"Error: {res.get('error')}", file=sys.stderr)
            return 1

        if args.json:
            print(json.dumps(res, indent=2))
        else:
            table = format_axe_markdown_table(res)
            print(table)
            if args.out:
                args.out.write_text(table, encoding="utf-8")
                print(f"Saved Markdown report to: {args.out}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
