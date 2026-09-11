# the-architect

Planning-first skill for application discovery, requirements, architecture, project documentation, and phased implementation. It turns an idea or change request into an understood, documented, implementation-ready plan, then implements it in verified phases.

Domain: `software-engineering` · Type: `core`

## When to use

Invoke with `/the-architect`, or let Claude pick it up automatically when you ask for things like:

- "I want to build an app that …" (new product → PRD, architecture, phased plan)
- "Add feature X to this repo" (codebase discovery → `PROJECT_GUIDE.md` → feature PRD → plan)
- "Fix this bug" or a small contained change (lightweight mode, plan in chat)
- "Upgrade this project from .NET Framework to .NET 8" / "migrate to …" (migration brief, safety net, reversible phases)
- "Document this codebase so another developer or AI can work on it"

### Modes

| Mode | Use for | Planning files |
|---|---|---|
| A — New Project | No application exists yet | PRD, ARCHITECTURE, IMPLEMENTATION_PLAN, phases |
| B — Existing Project | New feature or substantial change | + PROJECT_GUIDE |
| C — Small Change | Bug fixes, small contained changes | None (short plan in chat) |
| D — Refactor / Upgrade / Migration | Same behavior, different implementation | PROJECT_GUIDE, MIGRATION_BRIEF, ARCHITECTURE, IMPLEMENTATION_PLAN with rollback, phases |

Version control rules: commits are authored by the human developer only (no AI
co-author trailers or attribution lines), nothing is committed unless asked, and
a stack-appropriate `.gitignore` is required before the first commit.

## Structure

```text
the-architect/
├── SKILL.md                                 # compact, stack-agnostic core loaded every run
├── README.md
├── config/
│   └── skill.yaml                           # manifest + machine-readable workflow policy
├── references/
│   ├── product-discovery.md                 # discovery rounds, PRD Coverage Gate, Discovery Summary
│   ├── codebase-discovery.md                # existing-repo discovery and PROJECT_GUIDE contents
│   ├── stack-profiles.md                    # per-stack inventories, commands, test frameworks, .gitignore
│   ├── testing-strategy.md                  # test levels, AC traceability, baseline and evidence
│   ├── PRD.template.md
│   ├── FEATURE_PRD.template.md
│   ├── MIGRATION_BRIEF.template.md          # replaces the PRD in Mode D
│   ├── ARCHITECTURE.template.md
│   ├── IMPLEMENTATION_PLAN.template.md
│   ├── PROJECT_GUIDE.template.md
│   └── PHASE.template.md
├── scripts/
│   ├── scan_repo.py                         # mechanical repo inventory + sub-project map
│   └── validate_artifacts.py                # required sections, AC→test traceability, secret leakage
└── evals/
    └── evals.json                           # trigger and behavior test cases
```

- `scripts/scan_repo.py`: `python scripts/scan_repo.py <repo_path> [--summary]`
- `scripts/validate_artifacts.py`: `python scripts/validate_artifacts.py <project_path> --mode new|feature|migration`

## Changelog

### 1.3.0 — 2026-09-10

- Imported into the jinkou-chinou repository under `domains/software-engineering/`.
- Added the standard manifest header (`domain`, `type`, `requires`, `tags`) to `config/skill.yaml` and `evals/evals.json`. No change to the skill's behavior.
