# kanban-updater

Draft evidence-based technical English work updates from Git and user notes, or update requested Exact Synergy Kanban cards using isolated Playwright automation.

Domain: `workflow-automation` · Type: `specialized` · Version: `1.0.0`

---

## When to use

Invoke with `/kanban-updater`, or let your agent activate it when asking to:

* *"Draft my EoD remarks based on my commits today for ticket #7111."*
* *"Summarize what changed on this branch and format it for our standup."*
* *"Inspect the current remarks and status of ticket #7094 on Synergy."*
* *"Submit my drafted remarks to card #7111 and move it to In-Progress."*
* *"Audit my EoD update score for this week according to the SOP."*
* *"Setup the Playwright environment and set my PersonID."*

Do not use for Jira, GitHub Projects, general git commits, or backend coding tasks.

---

## Getting Started

### 1. Prerequisites and Setup
The skill includes a deterministic helper tool to verify or install required browser automation dependencies without modifying personal browser profiles:

```powershell
# Diagnostic check
python domains/workflow-automation/kanban-updater/scripts/setup_environment.py --check

# Automatic installation (installs playwright package and chromium binaries)
python domains/workflow-automation/kanban-updater/scripts/setup_environment.py --install
```

### 2. Setting Your `<PersonID>`
Exact Synergy routes personal Kanban boards using the employee's `PersonID`. Each team member has a unique ID:

#### Finding Your PersonID
1. Navigate to `https://synergy.glmsystems.com/` in your browser.
2. In the top-right header, right-click your name link and select **Open in new tab**.
3. In the new tab's URL bar, find the parameter:
   `https://synergy.glmsystems.com/docs/HRMResourceCard.aspx?ID=12345`
4. The number following `?ID=` is your `PersonID`.

#### Configuring Your PersonID
You can set your `PersonID` in any of the following ways (highest to lowest priority):

1. **Directly in the Prompt**:
   ```text
   /kanban-updater #7111 for PersonID 12345
   ```
2. **Local User Configuration** (Recommended, persists across sessions):
   ```powershell
   python domains/workflow-automation/kanban-updater/scripts/setup_environment.py --set-person-id 12345
   ```
   *(Saves to `~/.config/kanban-updater/config.json`, keeping personal IDs out of Git).*
3. **Environment Variable**:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('SYNERGY_PERSON_ID', '12345', 'User')
   ```
4. **Live Auto-Discovery**:
   If unconfigured, the skill automatically discovers your ID by inspecting the top-right name link in a new tab during an active Synergy session.

---

## Operating Modes

| Mode | Trigger Example | Actions & Safeguards |
|---|---|---|
| **Mode A — Draft-Only** *(Default)* | `"Draft my standup from today's commits"` | Inspects git log/diffs, formats EoD SOP remarks. **Zero browser access.** |
| **Mode B — Card Inspection** | `"Check ticket #7111 on Synergy"` | Launches headless Edge, navigates to board, reads status and remarks. |
| **Mode C — Append & Transition** | `"Submit update to #7111 and mark In-Progress"` | Preserves history, appends remarks, transitions status, verifies persistence. |
| **Mode D — EoD Scoring Audit** | `"Calculate my EoD score for this week"` | Evaluates remarks against consistency, timeliness, and quality criteria. |
| **Mode E — Environment Setup** | `"Setup Playwright environment"` | Runs `setup_environment.py` diagnostics, installer, and config helper. |

---

## Structure

```text
kanban-updater/
├── SKILL.md                          # Main skill instructions, trigger description, modes, and rules
├── README.md                         # Human owner documentation, setup guide, and changelog
├── config/
│   └── skill.yaml                    # Machine-readable manifest and operational policy
├── scripts/
│   └── setup_environment.py          # Dependency installer and PersonID configuration tool
├── references/
│   ├── configuration.md              # PersonID discovery, environment variables, Edge profiles
│   ├── tickets.md                    # Historical ticket lookup hints and Synergy URL templates
│   ├── eod-scoring.md                # End-of-Day scoring SOP and evidence-based remark templates
│   └── browser-recovery.md           # Playwright session management and failure recovery protocols
└── evals/
    └── evals.json                    # Trigger and behavior test cases
```

---

## Changelog

### 1.0.0 — 2026-10-01

- Recreated skill under `workflow-automation` domain following `jinkou-chinou` Skill Standard.
- Added `scripts/setup_environment.py` for automated Playwright diagnostics, installation, and PersonID configuration.
- Formulated 5 distinct operational modes with Mode A (Draft-Only) as the safe default.
- Added comprehensive documentation for PersonID resolution and Edge session isolation.
- Created `evals/evals.json` trigger test suite.
