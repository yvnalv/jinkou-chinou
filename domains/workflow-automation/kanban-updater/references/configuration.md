# Configuration: the `config.json` Settings File

Every URL, PersonID, credential, repository, start time, schedule and browser setting lives in **one JSON file outside every repository**:

```text
%USERPROFILE%\.config\kanban-updater\config.json
```

The environment variable `KANBAN_UPDATER_CONFIG` points to a different file. The file holds a password in plain text: never copy it into a skill folder, a repository, or a chat message. Next to it live two data files the scripts write: `points-ledger.json` (quality ratings) and `schedule.log`.

---

## 1. Create or migrate

```powershell
python <skill-dir>/scripts/kanban_config.py --init
```

* No file: copies `assets/config.template.json`.
* An older `synergy.md` (2.0) in the same folder: its values are moved into `config.json`, and `synergy.md` is deleted after they read back identically.
* A flat 1.x `config.json` (`person_id`, `username`, `password` at top level): those values move into `environments.live`.
* Already current: nothing changes.

Check what the scripts will use (password masked):

```powershell
python <skill-dir>/scripts/kanban_config.py --show
python <skill-dir>/scripts/kanban_config.py --show --env live
```

## 2. Format

```json
{
  "active_environment": "local",
  "environments": {
    "local": { "base_url": "http://localhost/synergy_505", "person_id": "1",
               "username": "", "password": "", "date_format": "dd-mm-yyyy" },
    "live":  { "base_url": "https://synergy.glmsystems.com", "person_id": "...",
               "username": "DOMAIN\\name", "password": "...", "date_format": "dd-mm-yyyy" }
  },
  "work_log": { "repos": ["D:\\work\\505\\*"], "start_time": "09:00" },
  "schedule": { "enabled": true, "days": ["Mon","Tue","Wed","Thu","Fri"], "time": "17:20",
                "working_dir": "D:\\work\\505", "task_name": "kanban-updater EoD" },
  "browser":  { "profile": "%USERPROFILE%\\.gemini\\playwright-edge-profile", "cdp_port": 9333,
                "slow_mo": 100, "timeout_seconds": 45 }
}
```

JSON rules that bite:

* **Backslashes are doubled**: `DOMAIN\\name`, `D:\\work\\505`. A single `\` is a syntax error (the scripts point at the line and say so).
* A `"` inside a password is written `\"`.
* No comments and no trailing commas.

| Key | Meaning |
|---|---|
| `active_environment` | Which entry of `environments` is used. Switch `local` → `live` after testing. |
| `environments.<name>.base_url` | Portal root without `/docs`. |
| `person_id` | Your resource ID. Needed for your active cards (candidates) and points. `synergy_fill.py check` detects it from the board and tells you the value to set. |
| `username`, `password` | Optional. Empty = Windows login or the saved browser session. |
| `date_format` | How Synergy prints timestamp dates for you: `dd-mm-yyyy`, `mm-dd-yyyy` or `yyyy-mm-dd`. |
| `work_log.repos` | Repository paths. Wildcards (`D:\\work\\505\\*`) expand to every git repository they match. |
| `work_log.start_time` | Official start time (HH:MM). Timeliness deadline = start + 9 h; grace hour after that. |
| `schedule.*` | See `references/schedule-and-points.md` §1. After editing, run `schedule.py sync`. |
| `browser.profile` | Dedicated Edge profile. `%USERPROFILE%` is expanded. |
| `browser.cdp_port` | Local port of the visible automation window. |
| `browser.slow_mo` | Milliseconds between fill actions (watchable); 0 disables. |
| `browser.timeout_seconds` | Page timeout. |

More environments (for example `"local_504"`) can be added and selected by name.

## 3. Local first, then live

1. Test with `"active_environment": "local"` (Windows login, no credentials).
2. Fill `environments.live` and change one value: `"active_environment": "live"`.
3. `python <skill-dir>/scripts/synergy_fill.py check` confirms login, Kanban access and your PersonID on live.

## 4. Finding your PersonID by hand

Right-click your name (top-right in Synergy) → **Open in new tab** → the number after `HRMResourceCard.aspx?ID=`. A normal click opens the profile in an iframe and hides the URL. `SYNERGY_PERSON_ID` (environment variable) overrides the file for `setup_environment.py`.

## 5. Browser profile and session sharing

The automation uses its own Edge profile. `setup_environment.py --link-profiles` links the same physical profile into each AI tool folder (`.gemini` is the master; `.claude`, `.copilot`, `.agents`, `.codex`, `.cline`, `.cagent`, `.antigravity-ide` are directory junctions), so one sign-in serves every tool. Junctions need no administrator rights.

For a sign-in credentials cannot answer (single sign-on), sign in once in the visible window `fill` opens, or open the profile yourself and close it afterwards (a window opened without the automation port locks the profile for the scripts):

```cmd
start msedge.exe --user-data-dir="%USERPROFILE%\.gemini\playwright-edge-profile" https://synergy.glmsystems.com
```
