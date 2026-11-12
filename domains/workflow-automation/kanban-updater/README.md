# kanban-updater

Writes daily technical English work logs for Exact Synergy Kanban cards from git activity, card history and your notes, scored against the team's EoD SOP. It can type them into each card's **Remarks: Workflow** field with Synergy's timestamp (leaving the cards unsaved for you), report your weekly EoD points, and start itself every weekday at 17:20.

Domain: `workflow-automation` · Type: `specialized` · Version: `3.0.0`

---

## When to use

Invoke with `/kanban-updater`, or ask for things like:

* *"Write my work log for #7111 and #7094 for today."*
* *"EoD update for the cards I worked on today, and fill them in Synergy."*
* *"What are my EoD points this week?"*

Every run starts by asking the mode:

| Mode | What happens |
|---|---|
| **Work Log** | Drafts one remark per card; reads history read-only to avoid repeats. Types nothing into Synergy. |
| **Work Log + Fill** | Drafts, you approve, then a visible Edge window opens one tab per card with the remark typed after Synergy's timestamp. **You press Save.** |
| **Points Summary** | Asks the period (this week, last 4 weeks, custom), then shows per-day and per-week EoD points, bonus, penalty and trend from your saved remarks. |

Cards: DevOps work item (`#7111`) or Synergy request number (`46493`, `00.046.493`). A number matching several cards always makes the skill ask.

### Scheduled run

Every weekday at 17:20 (configurable) Windows Task Scheduler opens Claude Code in Windows Terminal with `/kanban-updater scheduled run ...`. It lists today's candidates (work items in today's commits and edited files, plus your active cards, with "logged today" and "last log"), and asks in one round which cards (one, several, or all) and which mode.

Not for Jira, GitHub Projects, Azure Boards, commit messages, or status changes.

---

## Setup

1. **One-click**: `setup-kanban.bat` in the repository root (or `scripts\setup.bat`): installs Playwright, links the shared Edge profile, creates `config.json`, registers the schedule, runs diagnostics.
2. **Settings**: everything in one file outside the repo, `%USERPROFILE%\.config\kanban-updater\config.json`:
   ```json
   {
     "active_environment": "local",
     "environments": {
       "local": { "base_url": "http://localhost/synergy_505", "person_id": "1", "username": "", "password": "" },
       "live":  { "base_url": "https://synergy.glmsystems.com", "person_id": "...", "username": "DOMAIN\\name", "password": "..." }
     },
     "work_log": { "repos": ["D:\work\505\*"], "start_time": "09:00" },
     "schedule": { "enabled": true, "days": ["Mon","Tue","Wed","Thu","Fri"], "time": "17:20" }
   }
   ```
   Backslashes are doubled in JSON. Going live = `"active_environment": "live"`. Full key list: [references/configuration.md](references/configuration.md).
3. **Schedule**: after changing `schedule`, run `python scripts/schedule.py sync`; `status` shows the next run, `run` starts it now.
4. **Check**: `python scripts/synergy_fill.py check` should report `"kanban_board": "reachable"` and your PersonID.

The password sits in plain text in that file and is never printed by the scripts (`kanban_config.py --show` masks it).

---

## Structure

```text
kanban-updater/
├── SKILL.md                             # Modes, scheduled run, workflow, rules, definition of done
├── README.md                            # This file
├── config/
│   └── skill.yaml                       # Manifest and policy summary
├── assets/
│   └── config.template.json             # Template for %USERPROFILE%\.config\kanban-updater\config.json
├── scripts/
│   ├── kanban_config.py                 # Read / create / migrate config.json (password masked)
│   ├── git_activity.py                  # Read-only git evidence by day and work item
│   ├── synergy_fill.py                  # check | find | history | candidates | entries | fill (never saves)
│   ├── points.py                        # EoD points report, quality ratings ledger
│   ├── schedule.py                      # Windows Task Scheduler: sync | status | run | remove | launch
│   ├── setup_environment.py             # Prerequisite diagnostics and installer
│   └── setup.bat                        # One-click Windows setup
├── references/
│   ├── eod-scoring.md                   # EoD SOP, writing style, mandatory self-audit
│   ├── synergy-automation.md            # Lookup, paging, history, fill mechanics, sessions, failures
│   ├── schedule-and-points.md           # Scheduled run, candidate selection, points computation
│   ├── configuration.md                 # config.json keys, local/live, PersonID, Edge profile
│   └── tickets.md                       # Old ticket hints and URL templates
└── evals/
    └── evals.json                       # Trigger and behavior cases
```

---

## Changelog

### 3.0.0 — 2026-11-12

- Settings moved back to one `config.json` (`assets/config.template.json`, `scripts/kanban_config.py`) with environments, repos (wildcards), start time, schedule and browser; `synergy.md` and the flat 1.x file migrate automatically. Removed `scripts/synergy_config.py` and `assets/synergy-config.template.md`.
- Added the third mode **Points Summary** (`scripts/points.py`): per-day and per-week points, weekly bonus, repetition penalty, Waiting and weekend exclusions; quality rated once by Claude and kept in `points-ledger.json`.
- Added the weekday schedule (`scripts/schedule.py`): Windows Task Scheduler opens Claude Code (PATH or the VS Code extension's bundled binary) at the configured time with a scheduled-run prompt.
- Added `synergy_fill.py candidates` (today's work items from git plus your active cards, ranked, with logged-today and last-log) and `entries` (your remarks for points); the scheduled run asks cards (multi-select, "All") and mode in one round.
- Card search now pages through the board (action 5), so matches are no longer cut at 5 cards per column; PersonID and login name are detected from the board.
- `git_activity.py`: recognises `user/user-story/#7310` branches and reports uncommitted files by the day they were modified.
- New reference `references/schedule-and-points.md`; rewrote `references/configuration.md`.

### 2.0.0 — 2026-11-12

- Replaced the five modes with two, asked at the start of every run: **Work Log** and **Work Log + Fill**.
- Added `scripts/synergy_fill.py`: `check`, `find` (work item or request number, asks on multiple matches), `history` (Workflow remarks grouped by day) and `fill` (types into Remarks: Workflow with Synergy's auto-timestamp, or the Timestamp button as fallback; never saves; leaves the visible window open).
- Added `scripts/git_activity.py`: read-only git evidence grouped by day and work item, for several cards per run.
- Added the single settings file `synergy.md` (`assets/synergy-config.template.md`, `scripts/synergy_config.py`) holding local and live URLs, PersonID, credentials and browser options; the 1.x `config.json` values migrate into the live block.
- Added the mandatory self-audit (inspection against card history + EoD scoring) to every work log (`references/eod-scoring.md` §5).
- Merged `references/browser-recovery.md` into the new `references/synergy-automation.md`; rewrote `references/configuration.md`.
- Removed the save-and-transition mode, the separate inspection, scoring-audit and setup modes, and the `--set-person-id` / `--set-credentials` options (edit `synergy.md` instead).
- Windows integrated authentication via `--auth-server-allowlist`, so the local portal needs no stored credentials.

### 1.1.0 — 2026-11-09

- Updated work log synthesis to enforce a cohesive 5–8 sentence human narrative prose paragraph instead of bullet-point lists.
- Enforced rule omitting the current ticket/work item number from remark text (only mentioning external dependency work item IDs).
- Added gold-standard narrative reference example and updated EoD Quality scoring rubric.

### 1.0.0 — 2026-10-01

- Recreated skill under `workflow-automation` domain following `jinkou-chinou` Skill Standard.
- Added `scripts/setup_environment.py` and `scripts/setup.bat` for automated Playwright diagnostics, installation, and PersonID configuration.
- Formulated 5 distinct operational modes with Mode A (Draft-Only) as the safe default.
- Added comprehensive documentation for PersonID resolution and Edge session isolation.
- Created `evals/evals.json` trigger test suite.
