#!/usr/bin/env python3
"""UI/UX Testing Helper CLI tool.

Provides utility functions to:
  1. Check and auto-install required automation testing dependencies (Node.js/npx, Python Playwright,
     pytest-playwright, axe-playwright-python, @playwright/test, @axe-core/playwright, and Chromium binaries).
  2. Validate Playwright test configuration files for UI/UX testing best practices.
  3. Parse and format Axe-core accessibility JSON outputs into clean markdown tables.

Uses Python standard library only (no external dependencies required to run this helper).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
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


def get_playwright_browsers_dir() -> Path:
    """Return the platform-specific Playwright browser cache directory."""
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if env_path and env_path.strip() and env_path.strip() != "0":
        return Path(env_path.strip())
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(local_app_data) / "ms-playwright"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "ms-playwright"
    return Path.home() / ".cache" / "ms-playwright"


def ensure_windows_browser_invoker_policy() -> list[str]:
    """Ensure Chrome/Edge executables on Windows are not blocked by RUNASADMIN elevation flags."""
    applied: list[str] = []
    if sys.platform != "win32":
        return applied
    try:
        import winreg
        candidates = [
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / r"Microsoft\Edge\Application\msedge.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / r"Microsoft\Edge\Application\msedge.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / r"Google\Chrome\Application\chrome.exe",
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / r"Google\Chrome\Application\chrome.exe",
        ]
        reg_path = r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            for exe in candidates:
                if exe.is_file():
                    winreg.SetValueEx(key, str(exe), 0, winreg.REG_SZ, "~ RUNASINVOKER")
                    applied.append(str(exe))
    except Exception:
        pass
    return applied


def resolve_node_tools() -> tuple[str | None, str | None, str | None]:
    """Find node, npx, and npm even if winget just installed Node.js and PATH is not refreshed yet."""
    if sys.platform == "win32":
        candidate_dirs = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "nodejs",
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "nodejs",
            Path(os.environ.get("LocalAppData", "")) / "Programs" / "nodejs",
            Path(os.environ.get("AppData", "")) / "npm",
        ]
        current_path = os.environ.get("PATH", "")
        for d in candidate_dirs:
            if d.is_dir() and str(d).lower() not in current_path.lower():
                os.environ["PATH"] = f"{d}{os.pathsep}{os.environ.get('PATH', '')}"

    node_bin = shutil.which("node")
    npx_bin = shutil.which("npx")
    npm_bin = shutil.which("npm")
    return node_bin, npx_bin, npm_bin


def verify_python_playwright_chromium(py_exe: str) -> tuple[bool, str | None]:
    """Ask Playwright directly whether its exact required Chromium executable exists on disk."""
    code = (
        "import os, sys\n"
        "try:\n"
        "    from playwright.sync_api import sync_playwright\n"
        "    with sync_playwright() as p:\n"
        "        exe = p.chromium.executable_path\n"
        "        print(exe)\n"
        "        sys.exit(0 if os.path.isfile(exe) else 2)\n"
        "except Exception as e:\n"
        "    print(str(e))\n"
        "    sys.exit(1)\n"
    )
    try:
        proc = subprocess.run(
            [py_exe, "-c", code],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )
        out = (proc.stdout or "").strip().splitlines()
        exe_path = out[-1].strip() if out else None
        return proc.returncode == 0, exe_path
    except Exception as exc:
        return False, str(exc)


def detect_project_python(cwd: Path) -> list[str]:
    """Return [sys.executable] plus any local project virtualenv Python if different."""
    executables = [sys.executable]
    candidates = [
        cwd / ".venv" / "Scripts" / "python.exe",
        cwd / "venv" / "Scripts" / "python.exe",
        cwd / ".venv" / "bin" / "python",
        cwd / "venv" / "bin" / "python",
    ]
    seen = {str(Path(sys.executable).resolve()).lower()}
    for c in candidates:
        if c.is_file():
            resolved = str(c.resolve()).lower()
            if resolved not in seen:
                seen.add(resolved)
                executables.append(str(c))
    return executables


def check_environment(project_dir: Path | None = None) -> dict[str, Any]:
    """Inspect installed Node.js, Python packages, and exact Playwright Chromium binary revision."""
    cwd = (project_dir or Path.cwd()).resolve()
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    node_bin, npx_bin, npm_bin = resolve_node_tools()
    node_version = None
    if node_bin:
        try:
            proc = subprocess.run([node_bin, "-v"], capture_output=True, text=True, timeout=5)
            if proc.returncode == 0:
                node_version = proc.stdout.strip()
        except Exception:
            pass

    py_packages: dict[str, bool] = {}
    for pkg, mod in [
        ("playwright", "playwright"),
        ("pytest", "pytest"),
        ("pytest-playwright", "pytest_playwright"),
        ("axe-playwright-python", "axe_playwright_python"),
    ]:
        try:
            __import__(mod)
            py_packages[pkg] = True
        except ImportError:
            py_packages[pkg] = False

    browsers_dir = get_playwright_browsers_dir()
    chromium_dirs: list[str] = []
    headless_shell_dirs: list[str] = []
    if browsers_dir.is_dir():
        for child in sorted(browsers_dir.iterdir()):
            if child.is_dir():
                if child.name.startswith("chromium-"):
                    chromium_dirs.append(child.name)
                elif child.name.startswith("chromium_headless_shell-"):
                    headless_shell_dirs.append(child.name)

    exact_chromium_ok = False
    exact_chromium_exe = None
    if py_packages.get("playwright"):
        exact_chromium_ok, exact_chromium_exe = verify_python_playwright_chromium(sys.executable)

    has_package_json = (cwd / "package.json").is_file()
    node_packages = {
        "@playwright/test": (cwd / "node_modules" / "@playwright" / "test").is_dir(),
        "@axe-core/playwright": (cwd / "node_modules" / "@axe-core" / "playwright").is_dir(),
        "dotenv": (cwd / "node_modules" / "dotenv").is_dir(),
    }

    binaries_ready = bool(chromium_dirs and headless_shell_dirs and exact_chromium_ok)
    python_ready = all(py_packages.values()) and binaries_ready
    node_ready = bool(node_bin and npx_bin) and binaries_ready and (not has_package_json or all(node_packages.values()))

    missing: list[str] = []
    if not node_bin or not npx_bin:
        missing.append("node/npx")
    for pkg, ok in py_packages.items():
        if not ok:
            missing.append(f"python:{pkg}")
    if has_package_json:
        for pkg, ok in node_packages.items():
            if not ok:
                missing.append(f"npm:{pkg}")
    if not binaries_ready:
        missing.append("playwright-browsers:chromium")

    return {
        "status": "ready" if (python_ready and (not has_package_json or node_ready)) else "missing_dependencies",
        "project_dir": str(cwd),
        "python": {
            "executable": sys.executable,
            "project_pythons": detect_project_python(cwd),
            "version": py_ver,
            "packages": py_packages,
            "ready": python_ready,
        },
        "node": {
            "found": bool(node_bin and npx_bin),
            "node_path": node_bin,
            "npx_path": npx_bin,
            "npm_path": npm_bin,
            "version": node_version,
            "has_package_json": has_package_json,
            "packages": node_packages,
            "ready": node_ready,
        },
        "browsers": {
            "cache_dir": str(browsers_dir),
            "chromium": chromium_dirs,
            "chromium_headless_shell": headless_shell_dirs,
            "exact_chromium_executable": exact_chromium_exe,
            "exact_revision_verified": exact_chromium_ok,
            "ready": binaries_ready,
        },
        "missing": missing,
    }


def install_dependencies(stack: str = "auto", project_dir: Path | None = None) -> dict[str, Any]:
    """Automatically install missing Python/Node Playwright dependencies and Chromium binaries."""
    cwd = (project_dir or Path.cwd()).resolve()
    before = check_environment(cwd)
    steps: list[dict[str, Any]] = []

    def run_step(name: str, cmd: list[str], workdir: Path | None = None) -> dict[str, Any]:
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(workdir or cwd),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            step_res = {
                "step": name,
                "command": " ".join(cmd),
                "returncode": proc.returncode,
                "stdout": (proc.stdout or "")[-600:].strip(),
                "stderr": (proc.stderr or "")[-600:].strip(),
            }
        except Exception as exc:
            step_res = {
                "step": name,
                "command": " ".join(cmd),
                "returncode": 1,
                "error": str(exc),
            }
        steps.append(step_res)
        return step_res

    has_pkg_json = before["node"]["has_package_json"]
    install_py = stack in ("auto", "python", "both")
    install_node = stack in ("node", "both") or (stack == "auto" and has_pkg_json)

    # 1. Ensure Node.js on Windows if missing, then refresh PATH in-process
    if (not before["node"]["found"]) and sys.platform == "win32":
        winget = shutil.which("winget")
        if winget:
            run_step(
                "winget_install_node_lts",
                [
                    winget,
                    "install",
                    "OpenJS.NodeJS.LTS",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
            )
            resolve_node_tools()

    # 2. Install missing Python packages across active Python and any project .venv
    if install_py:
        req_py_pkgs = ["playwright", "pytest", "pytest-playwright", "axe-playwright-python"]
        for py_exe in detect_project_python(cwd):
            missing_py = (
                [pkg for pkg, ok in before["python"]["packages"].items() if not ok]
                if py_exe == sys.executable
                else req_py_pkgs
            )
            if missing_py:
                res = run_step(
                    f"pip_install_playwright_packages ({Path(py_exe).parent.name})",
                    [py_exe, "-m", "pip", "install", *missing_py],
                )
                if res.get("returncode") != 0:
                    run_step("ensurepip_bootstrap", [py_exe, "-m", "ensurepip", "--upgrade"])
                    run_step(
                        f"pip_install_retry ({Path(py_exe).parent.name})",
                        [py_exe, "-m", "pip", "install", *missing_py],
                    )

    # 3. Install missing Node packages if package.json exists (or initialize if --stack node/both)
    _, npx_bin, npm_bin = resolve_node_tools()
    if install_node and npm_bin:
        if not has_pkg_json and stack in ("node", "both"):
            run_step("npm_init_y", [npm_bin, "init", "-y"], workdir=cwd)
            has_pkg_json = (cwd / "package.json").is_file()
        if has_pkg_json:
            missing_npm = [pkg for pkg, ok in before["node"]["packages"].items() if not ok]
            if missing_npm:
                run_step(
                    "npm_install_playwright_packages",
                    [npm_bin, "install", "-D", *missing_npm],
                    workdir=cwd,
                )

    # 4. Install Playwright Chromium browser binaries if missing or revision mismatch
    current_env = check_environment(cwd)
    if not current_env["browsers"]["ready"]:
        for py_exe in detect_project_python(cwd):
            run_step(
                f"python_playwright_install_chromium ({Path(py_exe).parent.name})",
                [py_exe, "-m", "playwright", "install", "chromium"],
            )
        if npx_bin and has_pkg_json:
            run_step(
                "npx_playwright_install_chromium",
                [npx_bin, "playwright", "install", "chromium"],
                workdir=cwd,
            )

    # 5. Apply Windows RUNASINVOKER policy for smooth browser spawning
    invoker_applied = ensure_windows_browser_invoker_policy()
    after = check_environment(cwd)
    return {
        "status": after["status"],
        "steps": steps,
        "windows_invoker_applied": invoker_applied,
        "environment": after,
    }


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

    # check-env
    chk_parser = subparsers.add_parser(
        "check-env",
        help="Check installed Node.js, Python Playwright/Axe packages, and Chromium binaries",
    )
    chk_parser.add_argument("--project-dir", type=Path, default=Path.cwd(), help="Project directory to inspect")
    chk_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # install-deps
    inst_parser = subparsers.add_parser(
        "install-deps",
        help="Auto-install missing Playwright, pytest-playwright, Axe-core, and Chromium browser binaries",
    )
    inst_parser.add_argument(
        "--stack",
        choices=["auto", "python", "node", "both"],
        default="auto",
        help="Target stack to install dependencies for (default: auto)",
    )
    inst_parser.add_argument("--project-dir", type=Path, default=Path.cwd(), help="Project directory for npm install")
    inst_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

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

    if args.command == "check-env":
        res = check_environment(args.project_dir)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Environment Status: {res['status'].upper()}")
            print(f"Python ({res['python']['version']}): {res['python']['packages']}")
            print(f"Node.js ({res['node']['version'] or 'not found'}): found={res['node']['found']}")
            print(f"Playwright Browsers ({res['browsers']['cache_dir']}): ready={res['browsers']['ready']}")
            if res["missing"]:
                print(f"Missing: {', '.join(res['missing'])}")
        return 0

    if args.command == "install-deps":
        res = install_dependencies(stack=args.stack, project_dir=args.project_dir)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Dependency Bootstrap Status: {res['status'].upper()}")
            for step in res["steps"]:
                print(f"  - [{step['step']}] exit={step['returncode']} ({step['command']})")
            if res["environment"]["missing"]:
                print(f"Still Missing: {', '.join(res['environment']['missing'])}")
        return 0 if res["status"] == "ready" else 1

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
