---
name: kanban-updater
description: Drafts evidence-based technical English work updates and End-of-Day (EoD) remarks from local Git repositories and user notes, or inspects and updates Exact Synergy Kanban cards using isolated Playwright automation. Use when drafting standup or EoD reports, checking ticket status in Synergy, appending remarks, or transitioning card status. Not for Jira, GitHub Projects, or non-Synergy issue tracking.
metadata:
  version: 1.0.0
---

# Kanban Updater

Synthesize verified Git changes and user notes into professional, high-scoring technical English work remarks, and optionally inspect or update personal Exact Synergy Kanban cards via dedicated Playwright browser automation.

```text
Resolve Intent & Scope → Extract Git Evidence → Synthesize Remarks (EoD SOP) → [Optional: Browser Automation] → Verify Persistence
```

## When to Use

* Drafting daily standup or End-of-Day (EoD) updates from local Git commits, diffs, and notes.
* Scoring or auditing work remarks against the team's EoD scoring SOP.
* Inspecting live ticket status, recent history, or available actions on Exact Synergy boards.
* Appending verified remarks to an Exact Synergy workflow request while preserving prior history.
* Moving cards across workflow states (e.g., Open to In-Progress / Approve) on personal Kanban boards.
* Setting up Playwright dependencies, Edge browser profile, or user `PersonID`.

Do not use it for: managing Jira or GitHub Projects boards, general git commit authoring, writing production feature code, or bypassing corporate authentication barriers.

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/configuration.md` | Setting up or discovering `PersonID`, configuring environment variables (`SYNERGY_PERSON_ID`), managing user config, or setting up Edge profiles and CDP. |
| `references/eod-scoring.md` | Drafting or auditing task remarks according to the End-of-Day scoring SOP (consistency, timeliness, quality, bonus/penalty, and label templates). |
| `references/tickets.md` | Looking up historical ticket mappings, request GUIDs, or Exact Synergy route templates (`HRMResourceCard`, `GLMSysKanbanBoard`, `WflRequest`). |
| `references/browser-recovery.md` | Diagnosing Playwright connection failures, handling profile locks, managing timeouts, formatting structured error logs, or executing safe write retries. |
| `scripts/setup_environment.py` | Checking prerequisites or auto-installing Playwright and configuring PersonID: `python <skill-dir>/scripts/setup_environment.py [--check|--install|--set-person-id ID|--json]`. |
| `scripts/setup.bat` | Interactive Windows batch automation to install Playwright, configure PersonID, and run health diagnostics: `<skill-dir>/scripts/setup.bat`. |

---

## Operating Modes

Choose the lightest safe mode covering the user's intent. **Default to Mode A whenever submission is not explicitly requested.**

| Request | Mode | Browser Action | Output |
|---|---|---|---|
| Draft standup or EoD remarks; summarize commits; prepare wording | **A — Draft-Only** | None (Safe) | Formatted technical English remarks |
| Check card status, read history, view board columns | **B — Card Inspection** | Read-Only | Card details, current status, recent remarks |
| Submit remarks to card; mark In-Progress or Approve | **C — Append & Transition** | Write + Read Verification | Verified submission report with card URL |
| Audit EoD score; check timeliness, quality, or weekly bonus | **D — EoD Scoring Audit** | None / Inspection | Itemized score report against SOP |
| Check dependencies; install Playwright; configure PersonID | **E — Environment Setup** | Diagnostic / Pip | Diagnostic health report / Config status |

### Mode A — Draft-Only (Default)

1. **Establish Scope**: Identify target repository, active branch, reporting period (default: current day in user's timezone), and user notes.
2. **Extract Git Evidence**: Run non-destructive Git commands (`git status --short`, `git log --since=...`, `git diff --stat`, `git diff`, `git diff --cached`). Never commit, stash, or reset working trees.
3. **Synthesize Remarks**: Combine Git evidence with notes using the EoD SOP format (`references/eod-scoring.md`). Every claim must map to a patch, commit, or note. Do not invent collaborators, root causes, tests, or deployments.
4. **Present Draft**: Output the formatted remarks. Stop here without launching a browser unless submission was explicitly commanded.

### Mode B — Card Inspection

1. **Check Prerequisites**: Ensure Playwright is available via `scripts/setup_environment.py --check`.
2. **Resolve PersonID**: Check prompt, `SYNERGY_PERSON_ID` env var, `~/.config/kanban-updater/config.json`, or perform live discovery (`references/configuration.md`).
3. **Connect Session**: Launch Edge persistent context (`channel="msedge"`, `headless=True`, `chromium_sandbox=False`, profile `%USERPROFILE%\.gemini\playwright-edge-profile` or any linked agent directory such as `%USERPROFILE%\.claude\playwright-edge-profile`) or connect via CDP endpoint if available.
4. **Locate Ticket**: Navigate to `GLMSysKanbanBoard.aspx?personid=<PersonID>`. Search ticket number/title; extract request link GUID.
5. **Inspect & Report**: Open `WflRequest.aspx?RequestID=<GUID>`. Read current status, requester, and recent remarks. Close tab and report findings.

### Mode C — Append Remarks & Transition

1. **Verify Draft & Target**: Confirm exact remarks and target card GUID before writing.
2. **Open Request**: Open `WflRequest.aspx?RequestID=<GUID>` in the authenticated context.
3. **Preserve History**: Inspect `#txtRemarks`. If editable history exists, read the entire existing string and append the new remark separated by two newlines (`\n\n`). If Synergy auto-stamps remarks, enter only the new content.
4. **Apply Transition (Optional)**: If status transition was requested (e.g. Open to In-Progress), verify available action buttons (`#btnApprove`, `#btnSave`) and click the verified control.
5. **Verify Persistence**: Re-navigate to the request URL. Confirm new remark is visible, prior remarks remain intact, and status matches the requested state.
6. **Report**: Return verified completion report with the direct card link. If submission failed, log structured error (`references/browser-recovery.md`) and output ready-to-copy remarks. Never blindly retry a write without reading first.

### Mode D — EoD Scoring Audit

1. Collect task remarks and submission timestamps.
2. Audit consistency (+1.0 weekday), timeliness (+1.0 on time, +0.5 grace), and quality (2.0-3.0 for progress, validation, blockers, and next steps) per `references/eod-scoring.md`.
3. Calculate final score and average per day; highlight penalties (repetition) or bonuses (5-day streak).

### Mode E — Environment Setup

1. Execute `<skill-dir>/scripts/setup.bat` (on Windows) or run `python <skill-dir>/scripts/setup_environment.py --install`.
2. Configure PersonID if requested via `--set-person-id <ID>`.
3. Report component readiness (Python, Playwright, Edge, Profile, Synergy connectivity).

---

## Rules

* **Default to Draft**: Never access Synergy or execute browser writes when the user asks for wording, drafts, or summaries. Submission requires unambiguous user intent.
* **Non-Destructive Browser Operations**: Never use `taskkill`, `Stop-Process`, or force-close user browsers. If the automation profile is locked, report the condition and instruct the user to close the conflicting tab or use CDP.
* **Top-Right Profile New-Tab Rule**: When auto-discovering `PersonID` in Synergy, always open the top-right name link in a new tab. Clicking inside the portal traps navigation in an iframe without exposing the URL parameter.
* **Preserve History**: Never overwrite existing remarks in `#txtRemarks`. Always append new entries to existing text.
* **Truthful Grounding**: Never invent collaborator names, deployment events, clean builds, or root causes. Distinguish implemented changes from pending validation.
* **Safe Write Retries**: If a timeout occurs after clicking save or approve, always execute a read-only page refresh to check if the update persisted before attempting any retry.

---

## Definition of Done

* **Mode A**: Factual technical English remarks delivered to the user with zero browser execution.
* **Mode B**: Live ticket details, status, and recent history extracted and presented.
* **Mode C**: Remarks confirmed persisted on the live request card, history verified intact, status transition confirmed, and direct URL provided.
* **Mode D**: Transparent mathematical score breakdown delivered with evidence citations.
* **Mode E**: Environment diagnostics verified clean (`status: ready`) or dependencies successfully installed.
