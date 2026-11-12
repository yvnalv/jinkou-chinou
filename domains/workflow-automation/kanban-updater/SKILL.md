---
name: kanban-updater
description: Writes daily technical English work logs (End-of-Day remarks) for Exact Synergy Kanban cards from local git activity, card history and user notes, scored against the team's EoD SOP, and tracks EoD points. Three modes, always offered first. Work Log writes the remark text only. Work Log + Fill also opens each card in Synergy with Playwright and types the remark into Remarks - Workflow with Synergy's timestamp, then leaves the window for the user to save (it never saves). Points Summary reports weekly and historical EoD points from the user's Synergy remarks. Runs on a weekday schedule via Windows Task Scheduler, starting with today's work candidates to pick from. Accepts DevOps work item numbers (#7111) or Synergy request numbers (00.046.493). Use for a work log, EoD or standup update, Kanban remarks, filling Synergy cards, EoD points, or the kanban schedule. Not for Jira, Azure Boards, or commit messages.
metadata:
  version: 3.0.1
---

# Kanban Updater

Turn the day's real work (git activity, card history, the user's notes) into one natural, high-scoring work log per Exact Synergy Kanban card, optionally type those logs into the cards' **Remarks: Workflow** field (never saving), and keep score of the EoD points they earn.

```text
(Scheduled: candidates → pick cards) → Ask mode → Scope → Git evidence → Card history → Draft → Self-audit → Fill → hand over
                                                    └→ Points Summary: period → report → rate new entries → tables
```

## When to Use

* Writing today's work log / EoD remark / standup update for one or more Synergy cards, and optionally filling them in without saving.
* The weekday 17:20 scheduled run (prompt starts with `/kanban-updater scheduled run`).
* Checking EoD points for this week or past weeks.
* Setting up `config.json`, Playwright, the Edge profile, or the Windows schedule.

Do not use it for: Jira, GitHub Projects or Azure Boards, writing commit messages, changing a card's status, or anything that saves in Synergy on the user's behalf.

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/eod-scoring.md` | Every draft and every quality rating: the scoring SOP, the 5–8 sentence narrative style, the gold-standard example, and the mandatory self-audit (§5). |
| `references/synergy-automation.md` | Running `find`, `history`, `candidates`, `entries` or `fill`: matching rules, board paging, timestamp mechanics, plan file format, sessions, failure table. |
| `references/schedule-and-points.md` | The scheduled run (candidate table, selection question), Points Summary (period question, rating loop, report tables), and managing the Windows task. |
| `references/configuration.md` | Creating or editing `config.json`: environments, local/live switch, credentials, repos, start time, schedule, browser. |
| `references/tickets.md` | Old ticket-to-GUID hints and Synergy URL templates. |
| `assets/config.template.json` | Template copied to `%USERPROFILE%\.config\kanban-updater\config.json` by `kanban_config.py --init`. |
| `scripts/kanban_config.py` | Settings: `python <skill-dir>/scripts/kanban_config.py --show [--env NAME]` (password masked), `--init` (create or migrate), `--path`. |
| `scripts/git_activity.py` | Git evidence by day and work item: `python <skill-dir>/scripts/git_activity.py --repo PATH [--repo PATH] [--since DATE] [--until DATE] [--author X \| --all-authors]`. Read-only. |
| `scripts/synergy_fill.py` | Synergy automation: `python <skill-dir>/scripts/synergy_fill.py [--env NAME] check \| find NUMBER... \| history TARGET... [--days N] \| candidates [--date DATE] [--max-history N] \| entries --since DATE --until DATE \| fill --plan PLAN.json`. Never saves. |
| `scripts/points.py` | EoD points: `python <skill-dir>/scripts/points.py report [--weeks N \| --since DATE --until DATE]`, `rate --file RATINGS.json`, `ledger`. |
| `scripts/schedule.py` | Windows task: `python <skill-dir>/scripts/schedule.py sync \| status \| run \| remove \| launch [--dry-run]`. |
| `scripts/setup_environment.py` | Prerequisites: `python <skill-dir>/scripts/setup_environment.py [--check \| --install \| --init-config \| --link-profiles \| --get-person-id] [--json]`. |
| `scripts/setup.bat` | One-click Windows setup: Playwright, profile links, `config.json`, schedule sync, diagnostics: `<skill-dir>/scripts/setup.bat`. |

---

## Scheduled run (prompt starts with "/kanban-updater scheduled run")

The Windows task opens Claude Code at the configured time (default Mon–Fri 17:20). Then:

1. `synergy_fill.py candidates` → today's work items from git (commits today, uncommitted files edited today on a work-item branch) plus your active cards, ranked, each with "logged today" and "last log".
2. Show the full numbered candidate table, then ask **in one question round** (details in `references/schedule-and-points.md`):
   * **Which cards** (multi-select): "All recommended (N)" plus the top 3 recommended cards; other numbers typed under *Other* (`1,4,5`).
   * **Mode**: the three options of Step 0.
3. Continue from Step 1 with the chosen cards and mode. Ambiguous or "no card found" work items: ask for the right card before drafting.
4. If nothing has activity today, say so, show your active cards anyway, and let the user pick or skip.

## Step 0 — Always ask the mode first

Before any other work (outside the scheduled run, where it is asked together with the card choice), ask one question (AskUserQuestion when available):

| Option | Meaning |
|---|---|
| **Work Log** | Write the remark text only. Read-only lookups in Synergy are allowed for history; nothing is typed into Synergy. |
| **Work Log + Fill** | Write the remarks, get approval, then type them into each card's Remarks: Workflow in a visible Edge window. The user presses Save. |
| **Points Summary** | Report EoD points for a period from your saved Synergy remarks (see "Points Summary" below). |

Mark the option the request points to as recommended, but still ask. In the same round, ask anything from Step 1 the request does not answer.

## Step 1 — Scope the day

* **Cards**: work item (`#7111`) or request numbers (`00.046.493`, `46493`). If none were given, propose candidates (`synergy_fill.py candidates`) and let the user pick.
* **Date**: today unless the user says otherwise. Never present back-dated work as today's.
* **Repositories**: from the request, the working directory, or `work_log.repos` in `config.json` (wildcards allowed).
* **Notes**: meetings, debugging help, blockers. Use them verbatim as facts.

## Step 2 — Git evidence

1. `scripts/git_activity.py` for the repos and date (add `--since` a few days back for continuity). It groups commits by day and work item and lists uncommitted files with the day they were last modified.
2. For each card, take that day's commits for its work item plus uncommitted work edited that day on its branch. Read the diffs (`git show <sha>`, `git diff`) for what you will describe; subjects alone are not evidence.
3. `unlinked` commits: ask which card they belong to, or leave them out.
4. Read-only: never commit, stash, reset, or switch branches.

## Step 3 — Card lookup and history (read-only)

1. Missing `config.json`: offer `kanban_config.py --init`, then continue. Without it, mark history "not checked".
2. `synergy_fill.py find <numbers...>`: `unique` → use it; `ambiguous` → **always ask which card** (request number, description, status, owner); `not_found` → ask for the request number.
3. `synergy_fill.py history <request_id...> --days 14`.
4. `auth_required` or a profile lock: stop and follow `references/synergy-automation.md` §6. Never invent credentials or ask for a password in chat.

## Step 4 — Draft one remark per card

Follow `references/eod-scoring.md` §4: one paragraph of **5–8 sentences** (problem and why → existing behavior and chosen solution → edge cases → obstacles and resolution → verification → next step), **never the card's own number**, plain developer tone, every claim backed by evidence, continuing the card's last entry without repeating it.

## Step 5 — Self-audit, then present

Run the inspection and scoring audit (`references/eod-scoring.md` §5) and revise until it passes. Present each card's remark with its audit table. **Work Log mode ends here.**

## Step 6 — Fill (Work Log + Fill only)

1. **Approval gate**: the user approves or edits each remark; fill only approved text, character for character.
2. **Pre-flight**: `synergy_fill.py check`; on failure `setup_environment.py --check`.
3. **Plan**: `[{"query", "request_id", "message"}, ...]` as JSON in the scratchpad (never in a repository).
4. **Fill**: `synergy_fill.py fill --plan <file>` → visible Edge window, one tab per card, Synergy timestamp (Enter, or the Timestamp button as fallback), text typed and verified, window left open.
5. **Report** one row per card (status, timestamp text, reason) and say plainly: **nothing was saved; review each tab and press Save yourself**.
6. **Verify** after the user saves: `history` for those cards.

## Points Summary

1. Ask the period first: **This week**, **Last 4 weeks**, or a custom range.
2. `points.py report` for that period (it reads your own remarks on your cards, read-only).
3. For every item in `unscored`, rate quality 0.5–3.0 with `references/eod-scoring.md` §1.C, write `[{"key", "quality", "note"}]` to the scratchpad, run `points.py rate --file`, then `report` again. Ratings are stored once in the ledger.
4. Present the weekly table and trend (`references/schedule-and-points.md` §3), with caveats: timeliness uses the timestamp time, Waiting uses the current status, unverified start time.

---

## Rules

* **Ask the mode every time** (in the scheduled run, together with the card choice). Never draft or browse before it is answered.
* **Never save.** Never click Save, Approve/In-Progress, Reject, Realize, Process, Delete or Close, never change a status. Saving is always the user's own click, even if asked mid-run.
* **Ambiguity means ask**: several cards for one number, unlinked commits, "no card found". Never pick for the user.
* **Append, never replace**; **approved text only**, into the confirmed `request_id`.
* **Writing rules always apply**: 5–8 sentence prose, no self ticket number, plain tone, truthful grounding, self-audit before presenting.
* **Honest points**: rate quality by the SOP rubric only; never inflate, and never suggest moving a card or padding text to gain points.
* **Browser discipline**: fill runs in a visible window; reads run headless or in the open automation window. Locate controls by Synergy's stable IDs and handlers, wait on page state, never fixed sleeps.
* **Login walls stop the run.** Point the user to `config.json` or a one-time sign-in.
* **Secrets stay in `config.json`.** Never print, echo, or commit the password; `kanban_config.py --show` masks it. The file lives outside every repository.
* **Non-destructive**: never kill Edge or close tabs the automation did not open.
* **No blind retries**: check `history` and open tabs before re-filling a card.
* **Schedule changes go through config**: edit `schedule` in `config.json`, then `schedule.py sync`. Never edit the Windows task by hand.

## Definition of Done

* **Work Log**: mode asked; each chosen card has a grounded 5–8 sentence remark with its audit table; ambiguities resolved by the user; history status stated.
* **Work Log + Fill**: the above, plus approval, `fill` result per card, the window left open with nothing saved, and the user told to press Save.
* **Points Summary**: period asked; every task entry in the period rated or explicitly pending; weekly totals, bonus, penalty and average per day shown with caveats.
* **Scheduled run**: candidates shown, the user's card and mode choice honored, then the chosen mode's definition of done.
