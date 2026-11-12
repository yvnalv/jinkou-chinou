# Scheduled Run and Points Summary

How the weekday schedule starts a work-log session, how the candidate list and selection question look, and how EoD points are computed and presented.

---

## 1. The Windows task

`scripts/schedule.py` manages one Windows Task Scheduler task (default name `kanban-updater EoD`) from the `schedule` block of `config.json`:

```json
"schedule": { "enabled": true, "days": ["Mon","Tue","Wed","Thu","Fri"], "time": "17:20",
              "working_dir": "D:\\work\\505", "task_name": "kanban-updater EoD" }
```

| Command | Effect |
|---|---|
| `python <skill-dir>/scripts/schedule.py sync` | Create or update the task from config (removes it when `enabled` is false). Run after every edit of `schedule`. |
| `python <skill-dir>/scripts/schedule.py status` | State, next and last run, and `in_sync_with_config`. |
| `python <skill-dir>/scripts/schedule.py run` | Start it now, exactly as the trigger would. |
| `python <skill-dir>/scripts/schedule.py launch --dry-run` | Show what it would open without opening anything. |
| `python <skill-dir>/scripts/schedule.py remove` | Delete the task. |

What the task does: runs `pythonw.exe <installed skill>/scripts/schedule.py launch`, which:

1. finds Claude Code: `claude` on PATH, else the newest `claude.exe` bundled with the VS Code extension (`%USERPROFILE%\.vscode\extensions\anthropic.claude-code-*\resources\native-binary\`), so extension updates need no change;
2. writes `%USERPROFILE%\.config\kanban-updater\launch.cmd` (Claude Code + the prompt `/kanban-updater scheduled run for <date>: ...`) and opens Windows Terminal (or `cmd` when it is missing) in `working_dir` running only that file. The prompt never passes through Windows Terminal, which re-parses quoted arguments and breaks them. If Claude Code exits with an error, the window stays open with a message;
3. appends a line to `%USERPROFILE%\.config\kanban-updater\schedule.log`.

Task settings: runs only while the user is signed in (interactive), starts as soon as possible after a missed time (sleep, shutdown), works on battery, limited rights. A Claude Code session cannot be started for a signed-out user; that run is skipped, and the next weekday runs normally.

## 2. Candidates and the selection question

`python <skill-dir>/scripts/synergy_fill.py candidates [--date YYYY-MM-DD] [--max-history 12]`:

* **git**: for each repo in `work_log.repos`, work items from that day's commits (message `#7111`, branch `feature/7111-x` or `user/user-story/#7111`) and from uncommitted files **edited that day** on a work-item branch. Older uncommitted files do not count.
* **cards**: each work item is searched on the board (`find` rules); unmatched ones appear as "(no card found)". Your own active cards (owner = your PersonID, status not Realized/Rejected/Processed/Completed) are added.
* **rank** = commits × 3 + edited files × 0.5 (max 5) + 1 if it is your active card. History is read for the top N: `logged_today`, `last_entry_date`, `last_entry_excerpt`.
* `recommended` = has a card, not yet logged today, and has activity or is your active card.

Present the table first, numbered by rank:

```text
| # | Request | Work item | Description | Status | Today's evidence | Logged today | Last log |
| 1 | 00.046.493 | #7111 | License expiry in Flippy | In-Progress | 3 commits (AIPlusAgentEG), 4 files | no | 11-11 |
| 2 | 00.046.377 | #7094 | ... | In-Progress | my active card | no | 10-11 |
```

Then one AskUserQuestion round with two questions:

1. **Cards** (`multiSelect: true`, at most 4 options): `All recommended (N)` first, then the top 3 recommended cards (`#1 00.046.493 #7111`, with the description as the option text). The table above stays the reference; the user types other rank numbers under *Other* (`1,4,5`).
2. **Mode**: Work Log / Work Log + Fill / Points Summary.

With 3 or fewer candidates, list each one plus `All (N)`. With none, say there is no activity today and offer the active cards or skipping.

## 3. Points Summary

### Period question

Ask first: **This week** (`points.py report`), **Last 4 weeks** (`--weeks 4`), or **Custom** (`--since --until`).

### What is computed (`references/eod-scoring.md` §1–3)

| Part | Rule in `points.py` |
|---|---|
| Task entry | One per card per weekday: all of your remarks on that card that day together. Weekend entries are excluded. |
| Consistency | +1.0 per weekday task entry. |
| Timeliness | First remark time vs `start_time` + 9 h: ≤ → 1.0, within the next hour → 0.5, later → 0. No `start_time` → unverified. |
| Quality | 0.5–3.0 from the ledger; new task entries come back in `unscored`. |
| Task score | 1.0 + timeliness + quality, at most 5.0. |
| Weekly bonus | +2.0 when all five weekdays have a task entry; "pending" while the week can still make it. |
| Repetition penalty | −5.0 when the same card has ≥ 95% similar remarks on 3 consecutive workdays (Fri → Mon counts as consecutive). |
| Waiting | Cards whose **current** status is Waiting are excluded (past status is not available). |

### Rating loop

1. `report` lists `unscored` items with `key`, card, date and full text.
2. Rate each with the §1.C rubric (+0.5 each: problem and approach, validation, obstacles, next step, natural prose; minimal text 0.5, short vague text 1.0; cap 3.0). Write `[{"key": "...", "quality": 2.5, "note": "why"}]` to the scratchpad.
3. `points.py rate --file <ratings.json>`, then `report` again.

Ratings and seen cards live in `%USERPROFILE%\.config\kanban-updater\points-ledger.json`, so past weeks keep their scores even after a card leaves your board. The ledger holds no credentials.

### Presenting

Per week, newest first:

```text
### Week of 10 Nov 2026 (in progress)
| Day | Tasks | Score |
| Mon 10-11 | 2 | 9.0 |
| Tue 11-11 | 1 | 4.5 |
...
Task scores 22.5 · Bonus pending (3/5, 2 days left) · Penalty 0 · Final 22.5 · Avg/day 7.5
```

Then a trend table (week, update days, final score, average per day), the excluded entries with reasons, and the caveats: timeliness uses the timestamp time (when typing started), not the save time; Waiting uses the current status; the board's saved view filters can hide cards.
