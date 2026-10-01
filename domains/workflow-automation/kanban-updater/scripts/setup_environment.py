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


KNOWN_AI_DIRECTORIES: list[tuple[str, str]] = [
    (".gemini", "Gemini / Antigravity"),
    (".claude", "Claude Code"),
    (".copilot", "GitHub Copilot"),
    (".agents", "OpenAI / Agent Skills (ChatGPT)"),
    (".codex", "OpenAI Codex"),
    (".cline", "Cline"),
    (".cagent", "CAgent"),
    (".antigravity-ide", "Antigravity IDE"),
]


def get_user_home() -> Path:
    """Return current user's home directory (resolves %USERPROFILE% on Windows)."""
    userprofile = os.environ.get("USERPROFILE")
    if userprofile and userprofile.strip():
        return Path(userprofile.strip())
    return Path.home()


def get_config_dir() -> Path:
    """Return local user config directory (~/.config/kanban-updater)."""
    home = get_user_home()
    config_dir = home / ".config" / "kanban-updater"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    return get_config_dir() / "config.json"


def get_default_profile_dir() -> Path:
    """Return dedicated Edge automation profile directory."""
    env_profile = os.environ.get("PLAYWRIGHT_EDGE_PROFILE")
    if env_profile and env_profile.strip():
        return Path(env_profile.strip())
    home = get_user_home()
    return home / ".gemini" / "playwright-edge-profile"


def ensure_profile_junctions(master_dir: Path | None = None) -> dict[str, dict]:
    """Ensure all detected AI agent directories have a directory junction pointing to the master profile.

    On Windows, directory junctions (NTFS reparse points) require NO administrator
    elevation and allow all AI assistants (.gemini, .claude, .copilot, .agents, .codex, etc.)
    to share the exact same physical Edge profile and authenticated session.
    """
    if master_dir is None:
        master_dir = get_default_profile_dir()
    master_dir.mkdir(parents=True, exist_ok=True)
    master_str = str(master_dir.resolve())

    home = get_user_home()
    results: dict[str, dict] = {}

    for folder_name, agent_label in KNOWN_AI_DIRECTORIES:
        agent_dir = home / folder_name
        if not agent_dir.exists():
            continue

        target_profile = agent_dir / "playwright-edge-profile"
        status_info = {
            "agent": agent_label,
            "directory": str(agent_dir),
            "profile_path": str(target_profile),
            "status": "unknown",
        }

        # If this is the master folder itself
        if str(target_profile.absolute()).lower() == str(master_dir.absolute()).lower():
            status_info["status"] = "master"
            results[folder_name] = status_info
            continue

        # Check if junction/symlink already exists
        if target_profile.exists():
            try:
                link_target = os.readlink(str(target_profile))
                status_info["status"] = "already_linked"
                status_info["target"] = link_target
                results[folder_name] = status_info
                continue
            except (OSError, ValueError):
                # Exists as a regular directory
                if target_profile.is_dir() and not any(target_profile.iterdir()):
                    try:
                        target_profile.rmdir()
                    except OSError:
                        status_info["status"] = "empty_dir_cannot_rm"
                        results[folder_name] = status_info
                        continue
                else:
                    status_info["status"] = "existing_folder"
                    results[folder_name] = status_info
                    continue

        # Create junction on Windows or symlink on POSIX
        try:
            if sys.platform == "win32":
                created = False
                try:
                    import _winapi
                    _winapi.CreateJunction(master_str, str(target_profile))
                    created = True
                except Exception:
                    pass

                if not created:
                    cmd_ret = subprocess.run(
                        ["cmd", "/c", "mklink", "/J", str(target_profile), master_str],
                        capture_output=True,
                        text=True,
                    )
                    created = (cmd_ret.returncode == 0)

                status_info["status"] = "created" if created else "error"
            else:
                target_profile.symlink_to(master_dir, target_is_directory=True)
                status_info["status"] = "created"
        except Exception as e:
            status_info["status"] = f"error: {e}"

        results[folder_name] = status_info

    return results


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


def ensure_edge_execution_policy() -> bool:
    """Ensure that msedge.exe is not blocked by Windows RUNASADMIN compatibility flags.

    If HKLM or system policies set ~ RUNASADMIN on msedge.exe, programmatic execution via
    CreateProcess (Playwright / Node.js child_process / Python subprocess) fails with
    WinError 740 (Elevation Required) or EACCES. Setting ~ RUNASINVOKER in HKCU safely
    overrides this for the current user without requiring Administrator elevation.
    """
    if sys.platform != "win32":
        return True
    try:
        import winreg
        exe_path = find_edge_executable()
        if not exe_path:
            return True
        reg_path = r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, exe_path, 0, winreg.REG_SZ, "~ RUNASINVOKER")
        return True
    except Exception:
        return False


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
    ensure_edge_execution_policy()
    profile_dir = get_default_profile_dir()
    profile_exists = profile_dir.is_dir()
    profile_locked = False
    if profile_exists:
        lock_markers = ["SingletonLock", "lockfile", "SingletonCookie"]
        for marker in lock_markers:
            if (profile_dir / marker).exists():
                profile_locked = True
                break

    ai_links = ensure_profile_junctions(profile_dir)
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
            "ai_links": ai_links,
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
    """Install playwright and ensure profile directory exists across all AI agent folders."""
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

    # 3. Create profile directory and link to all AI folders
    print("Preparing shared Edge profile and linking across all AI agent folders...")
    ensure_edge_execution_policy()
    profile_dir = get_default_profile_dir()
    profile_dir.mkdir(parents=True, exist_ok=True)
    junctions = ensure_profile_junctions(profile_dir)
    results["profile_dir"] = {
        "path": str(profile_dir),
        "created": profile_dir.is_dir(),
        "junctions": junctions,
    }

    results["status"] = "success"
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Environment setup and diagnostic tool for kanban-updater."
    )
    parser.add_argument("--check", action="store_true", help="Run environment diagnostics (default)")
    parser.add_argument("--install", action="store_true", help="Install playwright package, browsers, and link profiles")
    parser.add_argument("--link-profiles", action="store_true", help="Create or verify profile junctions across all AI folders")
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

    if args.link_profiles:
        profile_dir = get_default_profile_dir()
        links = ensure_profile_junctions(profile_dir)
        if args.json:
            print(json.dumps({"master": str(profile_dir), "ai_profiles": links}, indent=2))
        else:
            print(f"Master Profile: {profile_dir}")
            print("\nShared AI Agent Profiles:")
            for folder, info in links.items():
                st = info.get("status", "unknown")
                ag = info.get("agent", folder)
                pth = info.get("profile_path", "")
                if st == "master":
                    print(f"  [MASTER]       {ag:32} -> {pth}")
                elif st in ("already_linked", "created"):
                    print(f"  [LINKED]       {ag:32} -> {pth}")
                else:
                    print(f"  [{st.upper():12}] {ag:32} -> {pth}")
        return 0

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
        if "ai_links" in diag["profile"] and diag["profile"]["ai_links"]:
            print("  Shared AI Agent Profiles:")
            for folder, info in diag["profile"]["ai_links"].items():
                st = info.get("status", "unknown")
                ag = info.get("agent", folder)
                if st == "master":
                    print(f"    - {ag:32} [MASTER PROFILE]")
                elif st in ("already_linked", "created"):
                    print(f"    - {ag:32} [LINKED]")
                else:
                    print(f"    - {ag:32} [{st.upper()}]")
        print(f"Synergy Connectivity: {'Online' if diag['synergy']['reachable'] else 'Unreachable / Timeout'}")
        print(f"PersonID: {diag['person_id']['value'] or '<not set>'} (source: {diag['person_id']['source']})")
        if diag['status'] != "ready":
            print("\nRun with --install to install missing dependencies, or set PersonID with --set-person-id <ID>.")

    return 0 if diag["status"] == "ready" else 0


if __name__ == "__main__":
    sys.exit(main())
