#!/usr/bin/env python3
"""Read, validate and create the single kanban-updater settings file (config.json).

Location: %USERPROFILE%\\.config\\kanban-updater\\config.json   (override: KANBAN_UPDATER_CONFIG)

Usage:
  python kanban_config.py --show [--env NAME]      resolved settings as JSON (password masked)
  python kanban_config.py --init                   create config.json from the template; migrates an
                                                   older synergy.md or flat 1.x config.json in place
  python kanban_config.py --path                   print the settings file path

Standard library only.
"""

from __future__ import annotations

import argparse
import copy
import glob
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "config.template.json"
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

DEFAULTS = {
    "browser": {"profile": "%USERPROFILE%\\.gemini\\playwright-edge-profile", "cdp_port": 9333,
                "slow_mo": 100, "timeout_seconds": 45},
    "work_log": {"repos": [], "start_time": "09:00"},
    "schedule": {"enabled": False, "days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "17:20",
                 "working_dir": "", "task_name": "kanban-updater EoD"},
}


class ConfigError(Exception):
    """Settings file missing or invalid; the message says how to fix it."""


def user_home() -> Path:
    up = os.environ.get("USERPROFILE", "").strip()
    return Path(up) if up else Path.home()


def config_path() -> Path:
    override = os.environ.get("KANBAN_UPDATER_CONFIG", "").strip()
    if override:
        return Path(os.path.expandvars(override)).expanduser()
    return user_home() / ".config" / "kanban-updater" / "config.json"


def config_dir() -> Path:
    return config_path().parent


def legacy_markdown_path() -> Path:
    return config_dir() / "synergy.md"


def expand(value: str) -> str:
    return os.path.expandvars(str(value).replace("%USERPROFILE%", str(user_home())))


def expand_repos(patterns: list[str]) -> list[str]:
    """Expand wildcard entries (D:\\work\\505\\*) to the git repositories they match."""
    out: list[str] = []
    for pattern in patterns:
        p = expand(pattern).strip()
        if not p:
            continue
        matches = sorted(glob.glob(p)) if any(ch in p for ch in "*?[") else [p]
        for m in matches:
            if any(ch in p for ch in "*?[") and not (Path(m) / ".git").exists():
                continue
            if m not in out:
                out.append(m)
    return out


def _read_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        hint = ""
        line = text.splitlines()[exc.lineno - 1] if 0 < exc.lineno <= len(text.splitlines()) else ""
        if "\\" in line:
            hint = " Backslashes must be doubled in JSON (DOMAIN\\\\name, D:\\\\path)."
        raise ConfigError(f"{path} is not valid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}.{hint}") from None
    if not isinstance(data, dict):
        raise ConfigError(f"{path} must contain a JSON object.")
    return data


def _time_ok(value: str) -> bool:
    return bool(re.fullmatch(r"([01]?\d|2[0-3]):[0-5]\d", str(value).strip()))


def load_config(path: Path | None = None, env_override: str | None = None) -> dict:
    """Load config.json and resolve the active environment. Raises ConfigError with a fix hint."""
    path = path or config_path()
    if not path.is_file():
        raise ConfigError(f"Settings file not found: {path}. Create it with: python {Path(__file__).resolve()} --init")
    data = _read_json(path)
    if "environments" not in data:
        raise ConfigError(f"{path} uses the old flat format. Run: python {Path(__file__).resolve()} --init (migrates it).")

    envs = data.get("environments") or {}
    env_name = (env_override or data.get("active_environment") or "").strip().lower()
    envs_lc = {k.lower(): v for k, v in envs.items()}
    if not env_name:
        raise ConfigError(f"Set \"active_environment\" in {path} (one of: {', '.join(envs)}).")
    if env_name not in envs_lc:
        raise ConfigError(f"Environment '{env_name}' is not under \"environments\" in {path} (found: {', '.join(envs)}).")
    env = envs_lc[env_name] or {}

    base_url = str(env.get("base_url", "")).strip().rstrip("/")
    parsed = urlparse(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ConfigError(f"\"base_url\" of '{env_name}' must look like http(s)://host/path, got '{base_url}'.")

    browser = {**DEFAULTS["browser"], **(data.get("browser") or {})}
    work_log = {**DEFAULTS["work_log"], **(data.get("work_log") or {})}
    schedule = {**DEFAULTS["schedule"], **(data.get("schedule") or {})}
    try:
        cdp_port, slow_mo, timeout_s = int(browser["cdp_port"]), int(browser["slow_mo"]), int(browser["timeout_seconds"])
    except (TypeError, ValueError):
        raise ConfigError("\"cdp_port\", \"slow_mo\" and \"timeout_seconds\" must be whole numbers.") from None
    if work_log.get("start_time") and not _time_ok(work_log["start_time"]):
        raise ConfigError("\"work_log.start_time\" must be HH:MM, for example \"09:00\".")
    if not _time_ok(schedule.get("time", "")):
        raise ConfigError("\"schedule.time\" must be HH:MM, for example \"17:20\".")
    days = [str(d)[:3].title() for d in (schedule.get("days") or [])]
    bad = [d for d in days if d not in WEEKDAYS]
    if bad or not days:
        raise ConfigError(f"\"schedule.days\" must list days like [\"Mon\", \"Tue\"], got {schedule.get('days')}.")
    repos_raw = work_log.get("repos") or []
    if isinstance(repos_raw, str):
        repos_raw = [r for r in repos_raw.split(",")]

    username = str(env.get("username", "") or "")
    password = str(env.get("password", "") or "")
    return {
        "config_file": str(path),
        "config_dir": str(path.parent),
        "environment": env_name,
        "environments": list(envs),
        "base_url": base_url,
        "docs_url": base_url + "/docs",
        "host": parsed.hostname,
        "person_id": str(env.get("person_id") or "").strip() or None,
        "credentials": {"username": username, "password": password} if username and password else None,
        "date_format": str(env.get("date_format") or "dd-mm-yyyy").lower(),
        "browser": {"profile": expand(browser["profile"]), "cdp_port": cdp_port, "slow_mo": slow_mo,
                    "timeout_ms": timeout_s * 1000},
        "work_log": {"repo_patterns": list(repos_raw), "repos": expand_repos(repos_raw),
                     "start_time": str(work_log.get("start_time") or "") or None},
        "schedule": {"enabled": bool(schedule.get("enabled")), "days": days, "time": schedule["time"].strip(),
                     "working_dir": expand(schedule.get("working_dir") or ""),
                     "task_name": str(schedule.get("task_name") or DEFAULTS["schedule"]["task_name"])},
    }


def public_view(cfg: dict) -> dict:
    """Settings safe to print: the password is never shown."""
    out = {k: v for k, v in cfg.items() if k != "credentials"}
    creds = cfg.get("credentials")
    out["auth"] = ({"mode": "credentials", "username": creds["username"], "password": "set"}
                   if creds else {"mode": "windows-login-or-session"})
    return out


# ------------------------------------------------------------------ migration from older formats

_HEADING = re.compile(r"^\s*#{2,6}\s+(.+?)\s*#*\s*$")
_LINE = re.compile(r"^\s*(?:[-*]\s+)?([a-z][a-z0-9_]*)\s*:\s?(.*?)\s*$")


def _parse_synergy_md(text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    current = None
    for line in text.splitlines():
        h = _HEADING.match(line)
        if h:
            current = re.sub(r"[^a-z0-9]+", "_", h.group(1).lower()).strip("_")
            sections.setdefault(current, {})
            continue
        m = _LINE.match(line)
        if current and m:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "`'\"":
                v = v[1:-1]
            sections[current][m.group(1)] = v
    return sections


def _from_markdown(md: dict, base: dict) -> dict:
    out = copy.deepcopy(base)
    reserved = {"active", "browser", "work_log"}
    out["active_environment"] = md.get("active", {}).get("environment", out["active_environment"]).lower()
    for name, values in md.items():
        if name in reserved:
            continue
        env = out["environments"].setdefault(name, {"base_url": "", "person_id": "", "username": "",
                                                     "password": "", "date_format": "dd-mm-yyyy"})
        for k in ("base_url", "person_id", "username", "password", "date_format"):
            if values.get(k):
                env[k] = values[k]
    b = md.get("browser", {})
    for k, cast in (("profile", str), ("cdp_port", int), ("slow_mo", int), ("timeout_seconds", int)):
        if b.get(k):
            try:
                out["browser"][k] = cast(b[k])
            except ValueError:
                pass
    w = md.get("work_log", {})
    if w.get("repos"):
        out["work_log"]["repos"] = [r.strip() for r in w["repos"].split(",") if r.strip()]
    if w.get("start_time"):
        out["work_log"]["start_time"] = w["start_time"]
    return out


def _from_flat_json(flat: dict, base: dict) -> dict:
    out = copy.deepcopy(base)
    live = out["environments"]["live"]
    for k in ("person_id", "username", "password"):
        if flat.get(k):
            live[k] = str(flat[k]).strip()
    return out


def init_config() -> dict:
    """Create config.json from the template, carrying over values from synergy.md or a flat 1.x config.json."""
    path = config_path()
    result: dict = {"config_file": str(path)}
    existing = None
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            raise ConfigError(f"{path} exists but is not valid JSON; fix or remove it first.") from None
        if isinstance(existing, dict) and "environments" in existing:
            result.update(status="exists", note="config.json is already in the current format; nothing changed.")
            return result

    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    sources = []
    if isinstance(existing, dict) and existing:
        data = _from_flat_json(existing, data)
        sources.append("flat config.json (person_id, username, password -> live)")
    md_path = legacy_markdown_path()
    if md_path.is_file():
        data = _from_markdown(_parse_synergy_md(md_path.read_text(encoding="utf-8-sig")), data)
        sources.append(f"{md_path.name}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    load_config(path)  # must read back cleanly
    result.update(status="created" if existing is None else "migrated", migrated_from=sources)
    if md_path.is_file():
        md = _parse_synergy_md(md_path.read_text(encoding="utf-8-sig"))
        same = all(
            data["environments"].get(env, {}).get(k, "") == v
            for env, values in md.items() if env not in {"active", "browser", "work_log"}
            for k, v in values.items() if k in ("base_url", "person_id", "username", "password") and v
        )
        if same:
            md_path.unlink()
            result["removed"] = str(md_path)
        else:
            result["kept"] = f"{md_path} (values did not read back identically)"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="kanban-updater settings (config.json) helper.")
    parser.add_argument("--show", action="store_true", help="print resolved settings as JSON (password masked)")
    parser.add_argument("--env", help="resolve this environment instead of the active one")
    parser.add_argument("--init", action="store_true", help="create or migrate config.json")
    parser.add_argument("--path", action="store_true", help="print the settings file path")
    args = parser.parse_args()
    try:
        if args.path:
            print(config_path())
            return 0
        if args.init:
            print(json.dumps(init_config(), indent=2))
            return 0
        print(json.dumps({"status": "ok", **public_view(load_config(env_override=args.env))}, indent=2))
        return 0
    except ConfigError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
