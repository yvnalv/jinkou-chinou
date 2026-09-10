# the-architect Claude Skill Package

This package contains the `the-architect` skill together with reference
templates, helper scripts, and YAML configuration.

## Structure

```text
the-architect/
├── SKILL.md
├── config/
│   └── skill.yaml
├── references/
│   ├── product-discovery.md
│   ├── codebase-discovery.md
│   ├── stack-profiles.md
│   ├── testing-strategy.md
│   ├── PRD.template.md
│   ├── FEATURE_PRD.template.md
│   ├── MIGRATION_BRIEF.template.md
│   ├── ARCHITECTURE.template.md
│   ├── IMPLEMENTATION_PLAN.template.md
│   ├── PROJECT_GUIDE.template.md
│   └── PHASE.template.md
├── scripts/
│   ├── scan_repo.py
│   └── validate_artifacts.py
└── README.md
```

## Intended use

- `SKILL.md`: the compact, stack-agnostic core Claude loads every time the skill runs: modes, principles, and the rules that always apply. Its "Bundled Resources" section tells Claude when to open each file below.
- `references/product-discovery.md`: full Product Discovery guidance, the PRD Coverage Gate checklist, and the Discovery Summary format.
- `references/codebase-discovery.md`: step-by-step existing-repository discovery and the required `PROJECT_GUIDE.md` contents.
- `references/stack-profiles.md`: specialized knowledge per kind of system (web backend, web frontend, mobile, desktop, data/ML, infrastructure, library/CLI, systems/embedded, game).
- `references/testing-strategy.md`: test levels, acceptance-criteria traceability, baseline and evidence format, flaky and pre-existing failures, CI, coverage.
- `references/*.template.md`: artifact templates. `MIGRATION_BRIEF` replaces the PRD for refactors, upgrades, and migrations.
- `scripts/scan_repo.py`: first-pass mechanical repository inventory with a sub-project map (`python scripts/scan_repo.py <repo_path> [--summary]`).
- `scripts/validate_artifacts.py`: checks planning artifacts for required files and sections, acceptance-criteria-to-test traceability, and obvious secret leakage (`python scripts/validate_artifacts.py <project_path> --mode new|feature|migration`).
- `config/skill.yaml`: machine-readable workflow policy.

## Modes

| Mode | Use for | Planning files |
|---|---|---|
| A — New Project | No application exists yet | PRD, ARCHITECTURE, IMPLEMENTATION_PLAN, phases |
| B — Existing Project | New feature or substantial change | + PROJECT_GUIDE |
| C — Small Change | Bug fixes, small contained changes | None (short plan in chat) |
| D — Refactor / Upgrade / Migration | Same behavior, different implementation | PROJECT_GUIDE, MIGRATION_BRIEF, ARCHITECTURE, IMPLEMENTATION_PLAN with rollback, phases |

Version control rules: commits are authored by the human developer only (no AI
co-author trailers or attribution lines), nothing is committed unless asked, and
a stack-appropriate `.gitignore` is required before the first commit.
