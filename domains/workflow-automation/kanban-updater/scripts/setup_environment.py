#!/usr/bin/env python3
"""Environment and dependency setup tool for kanban-updater.

Diagnoses prerequisites, installs required Python dependencies (Playwright),
prepares dedicated browser automation profiles, and manages local PersonID
configuration.

Usage:
  python setup_environment.py [--check] [--json]
  python setup_environment.py --install
  python setup_environment.py --set-person-id <ID>
  python setup_environment.py --get-person-id
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path


def get_config_dir() -> Path:
    """Return local user config directory (~/.config/kanban-updater)."""
    home = Path.home()
    config_dir = home / ".config" / "kanban-updater"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    return get_config_dir() / "config.json"


def get_default_profile_dir() -> Path:
    """Return dedicated Edge automation profile directory."""
    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        base = Path(userprofile)
    else:
        base = Path.home()
    return base / ".gemini" / "playwright-edge-profile"


def find_edge_executable() -> str | None:
    """Check standard locations for Microsoft Edge executable."""
    found = shutil.which("msedge")
    if found:
        return found
    candidates = [
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / r"Microsoft\Edge\Application\msedge.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / r"Microsoft\Edge\Application\msedge.exe",
        Path(os.environ.get("LocalAppData", "")) / r"Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return None


def resolve_person_id(override: str | None = None) -> tuple[str | None, str]:
    """Resolve PersonID from argument, environment variable, or config file."""
    if override:
        return override.strip(), "argument"
    env_id = os.environ.get("SYNERGY_PERSON_ID")
    if env_id and env_id.strip():
        return env_id.strip(), "environment (SYNERGY_PERSON_ID)"
    config_file = get_config_file()
    if config_file.is_file():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                val = data.get("person_id")
                if val:
                    return str(val).strip(), f"config_file ({config_file})"
        except Exception:
            pass
    return None, "none"


def check_synergy_connectivity(host: str = "synergy.glmsystems.com", timeout: float = 3.0) -> bool:
    """Check if Synergy portal host is reachable."""
    try:
        sock = socket.create_connection((host, 443), timeout=timeout)
        sock.close()
        return True
    except (socket.timeout, OSError):
        return False


def run_diagnostics(person_id_override: str | None = None) -> dict:
    """Run non-destructive diagnostics and return health dict."""
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 10)

    # Check playwright package
    playwright_installed = False
    playwright_version = None
    try:
        import playwright
        playwright_installed = True
        playwright_version = getattr(playwright, "__version__", "installed")
    except ImportError:
        pass

    edge_path = find_edge_executable()
    profile_dir = get_default_profile_dir()
    profile_exists = profile_dir.is_dir()
    profile_locked = False
    if profile_exists:
        lock_markers = ["SingletonLock", "lockfile", "SingletonCookie"]
        for marker in lock_markers:
            if (profile_dir / marker).exists():
                profile_locked = True
                break

    synergy_online = check_synergy_connectivity()
    person_id, person_source = resolve_person_id(person_id_override)

    all_ready = py_ok and playwright_installed and (edge_path is not None) and not profile_locked

    return {
        "status": "ready" if all_ready else "needs_setup",
        "python": {
            "version": py_version,
            "compatible": py_ok,
            "executable": sys.executable,
        },
        "playwright": {
            "installed": playwright_installed,
            "version": playwright_version,
        },
        "edge": {
            "found": edge_path is not None,
            "path": edge_path,
        },
        "profile": {
            "path": str(profile_dir),
            "exists": profile_exists,
            "locked": profile_locked,
        },
        "synergy": {
            "portal_host": "synergy.glmsystems.com",
            "reachable": synergy_online,
        },
        "person_id": {
            "value": person_id,
            "source": person_source,
            "configured": person_id is not None,
        },
    }


def set_person_id(new_id: str) -> dict:
    """Store PersonID into ~/.config/kanban-updater/config.json."""
    cleaned = new_id.strip()
    if not cleaned:
        raise ValueError("PersonID cannot be empty.")
    config_file = get_config_file()
    payload = {
        "person_id": cleaned,
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return {
        "status": "success",
        "person_id": cleaned,
        "config_file": str(config_file),
    }


def install_dependencies() -> dict:
    """Install playwright and ensure profile directory exists."""
    results = {}
    # 1. pip install playwright
    print("Installing playwright via pip...")
    cmd_pip = [sys.executable, "-m", "pip", "install", "playwright"]
    proc = subprocess.run(cmd_pip, capture_output=True, text=True)
    results["pip_install"] = {
        "returncode": proc.returncode,
        "stdout": proc.stdout[-500:] if proc.stdout else "",
        "stderr": proc.stderr[-500:] if proc.stderr else "",
    }
    if proc.returncode != 0:
        results["status"] = "failed"
        return results

    # 2. playwright install chromium (fallback browser)
    print("Ensuring browser binaries (playwright install chromium)...")
    cmd_pw = [sys.executable, "-m", "playwright", "install", "chromium"]
    proc_pw = subprocess.run(cmd_pw, capture_output=True, text=True)
    results["playwright_browser_install"] = {
        "returncode": proc_pw.returncode,
        "stdout": proc_pw.stdout[-500:] if proc_pw.stdout else "",
    }

    # 3. Create profile directory
    profile_dir = get_default_profile_dir()
    profile_dir.mkdir(parents=True, exist_ok=True)
    results["profile_dir"] = {
        "path": str(profile_dir),
        "created": profile_dir.is_dir(),
    }

    results["status"] = "success"
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Environment setup and diagnostic tool for kanban-updater."
    )
    parser.add_argument("--check", action="store_true", help="Run environment diagnostics (default)")
    parser.add_argument("--install", action="store_true", help="Install playwright package and browsers")
    parser.add_argument("--set-person-id", metavar="ID", help="Save PersonID to local config")
    parser.add_argument("--get-person-id", action="store_true", help="Display resolved PersonID")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    if args.set_person_id:
        try:
            res = set_person_id(args.set_person_id)
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"[OK] PersonID set to '{res['person_id']}' in {res['config_file']}")
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to save PersonID: {e}", file=sys.stderr)
            return 1

    if args.get_person_id:
        person_id, source = resolve_person_id()
        out = {"person_id": person_id, "source": source}
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            print(f"PersonID: {person_id or '<not set>'} (source: {source})")
        return 0 if person_id else 1

    if args.install:
        res = install_dependencies()
        diag = run_diagnostics()
        combined = {"install": res, "diagnostics": diag}
        if args.json:
            print(json.dumps(combined, indent=2))
        else:
            if res.get("status") == "success":
                print("\n[OK] Playwright and environment prepared successfully.")
            else:
                print("\n[FAILED] Setup encountered an error. Check JSON report.", file=sys.stderr)
        return 0 if res.get("status") == "success" else 1

    # Default action: check
    diag = run_diagnostics()
    if args.json or not sys.stdout.isatty():
        print(json.dumps(diag, indent=2))
    else:
        print("=== kanban-updater Environment Diagnostics ===")
        print(f"Overall Status: {diag['status']}")
        print(f"Python: {diag['python']['version']} (compatible: {diag['python']['compatible']})")
        print(f"Playwright: {'Installed (' + str(diag['playwright']['version']) + ')' if diag['playwright']['installed'] else 'NOT INSTALLED'}")
        print(f"Edge Channel: {'Found at ' + str(diag['edge']['path']) if diag['edge']['found'] else 'NOT FOUND'}")
        print(f"Automation Profile: {diag['profile']['path']} (exists: {diag['profile']['exists']}, locked: {diag['profile']['locked']})")
        print(f"Synergy Connectivity: {'Online' if diag['synergy']['reachable'] else 'Unreachable / Timeout'}")
        print(f"PersonID: {diag['person_id']['value'] or '<not set>'} (source: {diag['person_id']['source']})")
        if diag['status'] != "ready":
            print("\nRun with --install to install missing dependencies, or set PersonID with --set-person-id <ID>.")

    return 0 if diag["status"] == "ready" else 0


if __name__ == "__main__":
    sys.exit(main())
