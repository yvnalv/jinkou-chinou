#!/usr/bin/env python3
"""Windows Task Scheduler integration: open a Claude Code session for the daily work log.

The task runs `schedule.py launch` at the time and days in config.json ("schedule"). `launch` finds
the Claude Code binary (the `claude` command, or the newest one bundled with the VS Code
extension) and opens it in Windows Terminal with the kanban-updater scheduled-run prompt.
The task runs only while you are signed in to Windows, and catches up after sleep.

Usage:
  python schedule.py sync      create/update the task from config.json (removes it when disabled)
  python schedule.py status    task state, next run, and whether it matches config.json
  python schedule.py run       start the task now (same as the scheduled trigger)
  python schedule.py remove    delete the task
  python schedule.py launch [--dry-run]   what the task executes; --dry-run only prints the command

Windows only. Standard library only. Prints JSON.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kanban_config import ConfigError, config_dir, load_config, user_home  # noqa: E402

DAY_NAMES = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
             "Sat": "Saturday", "Sun": "Sunday"}


def emit(obj: dict, code: int = 0) -> int:
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    return code


def ps_quote(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def powershell(script: str) -> subprocess.CompletedProcess:
    # -EncodedCommand keeps multi-line statements intact (stdin input is parsed line by line).
    encoded = base64.b64encode(("$ErrorActionPreference = 'Stop'\n" + script).encode("utf-16-le")).decode("ascii")
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                           "-EncodedCommand", encoded],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def script_path() -> Path:
    """Prefer the installed skill path, which survives repository moves."""
    installed = user_home() / ".claude" / "skills" / "kanban-updater" / "scripts" / "schedule.py"
    return installed if installed.is_file() else Path(__file__).absolute()


def pythonw() -> str:
    exe = Path(sys.executable)
    candidate = exe.with_name("pythonw.exe")
    return str(candidate if candidate.is_file() else exe)


def log(line: str) -> None:
    try:
        with open(config_dir() / "schedule.log", "a", encoding="utf-8") as f:
            f.write(f"{dt.datetime.now().isoformat(timespec='seconds')} {line}\n")
    except OSError:
        pass


def _version_key(path: str) -> tuple:
    m = re.search(r"claude-code-(\d+(?:\.\d+)*)", path)
    return tuple(int(x) for x in m.group(1).split(".")) if m else (0,)


def find_claude() -> tuple[str | None, str]:
    on_path = shutil.which("claude")
    if on_path:
        return on_path, "PATH"
    pattern = str(user_home() / ".vscode" / "extensions" / "anthropic.claude-code-*" / "resources" / "native-binary" / "claude.exe")
    found = sorted(glob.glob(pattern), key=_version_key)
    if found:
        return found[-1], "vscode-extension"
    return None, "not found"


def launch_command(cfg: dict) -> tuple[list[str] | None, dict]:
    claude, source = find_claude()
    info = {"claude": claude, "claude_source": source}
    if not claude:
        return None, {**info, "error": "Claude Code binary not found (no `claude` on PATH and no VS Code extension)."}
    workdir = cfg["schedule"]["working_dir"] or (cfg["work_log"]["repos"][0] if cfg["work_log"]["repos"] else str(user_home()))
    if not Path(workdir).is_dir():
        workdir = str(user_home())
    today = dt.date.today().strftime("%A %d %B %Y")
    prompt = (f"/kanban-updater scheduled run for {today}: list today's work candidates, "
              "let me pick the cards and the mode, then continue the workflow")
    info["working_dir"] = workdir
    info["prompt"] = prompt
    wt = shutil.which("wt") or shutil.which("wt.exe")
    if wt:
        cmd = [wt, "-w", "new", "--title", "kanban-updater EoD", "-d", workdir, claude, prompt]
        info["terminal"] = "Windows Terminal"
    else:
        cmd = ["cmd.exe", "/c", "start", "kanban-updater EoD", "/d", workdir, claude, prompt]
        info["terminal"] = "cmd"
    return cmd, info


def cmd_launch(cfg: dict, dry_run: bool) -> int:
    cmd, info = launch_command(cfg)
    if not cmd:
        log(f"launch failed: {info['error']}")
        return emit({"status": "error", **info}, 1)
    if dry_run:
        return emit({"status": "dry-run", "command": cmd, **info})
    flags = 0x00000008 | 0x00000200 if sys.platform == "win32" else 0  # DETACHED_PROCESS | NEW_PROCESS_GROUP
    subprocess.Popen(cmd, cwd=info["working_dir"], creationflags=flags, close_fds=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log(f"launched {info['terminal']} in {info['working_dir']} with {info['claude']}")
    return emit({"status": "launched", **info})


def task_info(name: str) -> dict | None:
    r = powershell(f"""
$t = Get-ScheduledTask -TaskName {ps_quote(name)} -ErrorAction SilentlyContinue
if (-not $t) {{ 'null'; exit 0 }}
$i = $t | Get-ScheduledTaskInfo
$tr = $t.Triggers | Select-Object -First 1
[pscustomobject]@{{
  state = [string]$t.State
  next_run = if ($i.NextRunTime) {{ $i.NextRunTime.ToString('yyyy-MM-dd HH:mm') }} else {{ $null }}
  last_run = if ($i.LastRunTime -and $i.LastRunTime.Year -gt 2000) {{ $i.LastRunTime.ToString('yyyy-MM-dd HH:mm') }} else {{ $null }}
  last_result = $i.LastTaskResult
  time = if ($tr.StartBoundary) {{ ([datetime]$tr.StartBoundary).ToString('HH:mm') }} else {{ $null }}
  days = [int]$tr.DaysOfWeek
  action = (($t.Actions | Select-Object -First 1).Execute + ' ' + ($t.Actions | Select-Object -First 1).Arguments)
}} | ConvertTo-Json -Compress
""")
    out = (r.stdout or "").strip()
    if r.returncode != 0 or not out or out == "null":
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


DAY_BITS = {"Sun": 1, "Mon": 2, "Tue": 4, "Wed": 8, "Thu": 16, "Fri": 32, "Sat": 64}


def cmd_sync(cfg: dict) -> int:
    s = cfg["schedule"]
    name = s["task_name"]
    if not s["enabled"]:
        powershell(f"Unregister-ScheduledTask -TaskName {ps_quote(name)} -Confirm:$false -ErrorAction SilentlyContinue")
        return emit({"status": "disabled", "task": name, "note": "schedule.enabled is false; task removed if it existed"})
    days = ",".join(DAY_NAMES[d] for d in s["days"])
    args = f'"{script_path()}" launch'
    r = powershell(f"""
$action  = New-ScheduledTaskAction -Execute {ps_quote(pythonw())} -Argument {ps_quote(args)} -WorkingDirectory {ps_quote(str(script_path().parent))}
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {days} -At {ps_quote(s['time'])}
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$principal = New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName {ps_quote(name)} -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'Opens Claude Code for the kanban-updater daily work log (config.json: schedule).' -Force | Out-Null
'ok'
""")
    if "ok" not in (r.stdout or ""):
        return emit({"status": "error", "error": (r.stderr or r.stdout or "").strip()[:600]}, 1)
    return emit({"status": "synced", "task": name, "days": s["days"], "time": s["time"], **(task_info(name) or {})})


def cmd_status(cfg: dict) -> int:
    s = cfg["schedule"]
    info = task_info(s["task_name"])
    claude, source = find_claude()
    if not info:
        return emit({"status": "not_scheduled", "task": s["task_name"], "config": s, "claude": claude,
                     "hint": "run: python schedule.py sync"})
    want_bits = sum(DAY_BITS[d] for d in s["days"])
    in_sync = info.get("time") == s["time"] and info.get("days") == want_bits and s["enabled"]
    return emit({"status": "scheduled", "task": s["task_name"], "in_sync_with_config": in_sync, "config": s,
                 "claude": claude, "claude_source": source, **info,
                 **({} if in_sync else {"hint": "config.json and the task differ: run python schedule.py sync"})})


def cmd_run(cfg: dict) -> int:
    name = cfg["schedule"]["task_name"]
    if not task_info(name):
        return emit({"status": "error", "error": f"task '{name}' does not exist; run sync first"}, 1)
    r = powershell(f"Start-ScheduledTask -TaskName {ps_quote(name)}; 'ok'")
    ok = "ok" in (r.stdout or "")
    return emit({"status": "started" if ok else "error", "task": name, "error": None if ok else (r.stderr or "").strip()[:400]},
                0 if ok else 1)


def cmd_remove(cfg: dict) -> int:
    name = cfg["schedule"]["task_name"]
    powershell(f"Unregister-ScheduledTask -TaskName {ps_quote(name)} -Confirm:$false -ErrorAction SilentlyContinue")
    return emit({"status": "removed" if not task_info(name) else "error", "task": name})


def main() -> int:
    parser = argparse.ArgumentParser(description="Windows Task Scheduler integration for kanban-updater.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("sync", "status", "run", "remove"):
        sub.add_parser(name)
    lp = sub.add_parser("launch")
    lp.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if sys.platform != "win32":
        return emit({"status": "error", "error": "Windows only"}, 1)
    try:
        cfg = load_config()
    except ConfigError as exc:
        log(f"config error: {exc}")
        return emit({"status": "error", "error": str(exc)}, 1)
    if args.command == "launch":
        return cmd_launch(cfg, args.dry_run)
    return {"sync": cmd_sync, "status": cmd_status, "run": cmd_run, "remove": cmd_remove}[args.command](cfg)


if __name__ == "__main__":
    sys.exit(main())
