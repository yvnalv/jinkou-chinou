# the-skillsmith

Repo-local meta skill that creates, extends, changes, audits, and imports skills so the whole jinkou-chinou collection follows `SKILL_STANDARD.md`. It lives in `.claude/skills/`, so Claude Code and the VS Code extension load it automatically whenever you work inside this repository. It is never installed globally or packaged for claude.ai.

Domain: `meta` · Type: `core`

## When to use

Invoke with `/the-skillsmith` inside this repository, or just ask:

- "Create a new skill for time-series forecasting in data-science."
- "Start a new domain for personal finance with a core persona."
- "Add a Flutter section to the-architect's stack profiles."
- "Bump exploratory-data-analysis: add support for SQL tables."
- "Audit the-architect against the standard."
- "Import this skill I found into the collection."

| Mode | For |
|---|---|
| A — New skill | A skill that does not exist yet, possibly in a new domain |
| B — Extend with a reference | Extra knowledge for an existing skill's workflow |
| C — Change | Edits, version bump, changelog, review of extending skills |
| D — Audit / Upgrade / Import | Findings first, then upgrade after approval |

## Structure

```text
the-skillsmith/
├── SKILL.md                     # modes, workflow, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml               # manifest + machine-readable policy
├── references/
│   ├── writing-guide.md         # description formula, what goes where, style, scripts, evals, anti-patterns
│   └── review-checklist.md      # quality review beyond the validator
└── evals/
    └── evals.json
```

It relies on the repository's `SKILL_STANDARD.md`, `tools/skills.py`, and `tools/templates/`.

## Changelog

### 0.1.0 — 2026-09-10

- Initial version: four modes (new, extend, change, audit/upgrade/import), writing guide, and review checklist.
