# Skill Standard

The rules every skill in **jinkou-chinou** follows. This file is the single source of truth: `CLAUDE.md`, the `the-skillsmith` skill, and `tools/skills.py validate` all enforce what is written here. If they ever disagree, this file wins — fix the others.

To create or change a skill, use `/the-skillsmith` inside this repository. It walks through these rules for you.

---

## 1. Principles

1. **One shape, trimmed per skill.** Every skill has the same anatomy (section 5). Optional folders exist only when the skill needs them — never as empty placeholders.
2. **Self-contained.** An installed skill is copied or linked on its own into `~/.claude/skills/<name>/` or uploaded alone to claude.ai. It must work without reading any other skill or any file outside its own folder.
3. **Progressive disclosure.** `SKILL.md` holds the workflow and the rules that always apply. Detail lives in `references/` and is opened only when a step needs it. Deterministic work lives in `scripts/`.
4. **Portable.** Skills must work in Claude Code (CLI), the Claude Code VS Code extension, and claude.ai. Use only portable frontmatter (section 6.1).
5. **Proportional.** A skill is as large as its job. A small specialized skill can be `SKILL.md` + `README.md` + `config/skill.yaml`.
6. **Personal use.** Skills are written for one owner. Prefer directness over generality, but never hard-code secrets, credentials, or personal data.

---

## 2. Repository Layout

```text
jinkou-chinou/
├── README.md                    # overview + generated skill catalog
├── CLAUDE.md                    # instructions for AI agents working in this repo
├── SKILL_STANDARD.md            # this file
├── .claude/skills/              # repo-local meta skills (active only inside this repo)
│   └── the-skillsmith/
├── tools/
│   ├── skills.py                # list | validate | new | catalog | install | uninstall | package
│   └── templates/               # skeleton files used by `skills.py new`
└── domains/
    └── <domain>/
        ├── README.md            # domain scope + generated skill list
        ├── the-<persona>/       # optional core skill for the domain
        └── <specialized-skill>/ # any number of specialized skills
```

Skills are organized by domain in the repository but installed **flat** into `~/.claude/skills/<name>/`, because Claude Code only discovers skills one level deep. That is why skill names must be globally unique (section 4).

---

## 3. Domains

A **domain** is a field of expertise that one expert persona could plausibly master: `software-engineering`, `data-science`, `writing`, `finance`, `cooking`, `law`, … The repository is meant to grow to cover any field; domains are added when the first skill for them is created.

* Domain folder names are kebab-case nouns describing the field, specific enough to be unambiguous across all human knowledge (`software-engineering`, not `engineering`).
* Every domain folder has a `README.md` with a one-paragraph scope statement and the generated skill list (between `<!-- skills:start -->` and `<!-- skills:end -->`).
* A domain has **at most one core skill** (the persona) and **any number of specialized skills**. A core skill is not required before specialized skills can exist.
* Split a domain only when it clearly holds two different kinds of expert (for example `data-science` vs `data-engineering`). Do not nest domains.
* `meta` is reserved for repo-local skills in `.claude/skills/` that maintain this repository.

---

## 4. Skill Types and Naming

| Type | What it is | Name rule | Example |
|---|---|---|---|
| `core` | The domain's broad persona: its general workflow, principles, and judgment | `the-<persona>` | `the-architect`, `the-data-scientist` |
| `specialized` | One focused task, technique, or sub-field inside a domain | descriptive, **no** `the-` prefix | `exploratory-data-analysis`, `time-series-forecasting` |

Rules for every name:

* kebab-case: lowercase letters, digits, and single hyphens; at most 64 characters.
* Must not contain `claude` or `anthropic` (reserved on claude.ai).
* Must equal the skill's folder name, `name` in `SKILL.md`, and `name` in `config/skill.yaml`.
* Must be unique across the whole repository, across all domains.
* The name is the slash command: `the-architect` is invoked as `/the-architect`. Prefer names that are clear when typed.

### 4.1 Specialized skills — new skill or reference file?

| The specialization… | Do this |
|---|---|
| is extra knowledge for the **same workflow** (a new stack, a new data format, one more checklist) | Add a file to the existing skill's `references/` and list it in its Bundled Resources table. |
| has its **own trigger, workflow, or output** (a user would ask for it by name) | Create a specialized skill in the same domain. |

A specialized skill may declare `extends: <core-skill>` in `config/skill.yaml` when it builds on a core skill's workflow. `extends` is documentation and a review trigger, not a runtime import: the specialized skill must still copy in any rule from the core skill that it depends on (principle 2). When a core skill's version changes, review every skill that extends it.

---

## 5. Skill Anatomy

```text
<skill-name>/
├── SKILL.md              # required — what Claude loads
├── README.md             # required — for the human owner
├── config/
│   └── skill.yaml        # required — machine-readable manifest
├── references/           # optional — docs and templates loaded on demand
├── scripts/              # optional — deterministic helpers
├── assets/               # optional — files used in the output, not read into context
└── evals/
    └── evals.json        # recommended — trigger and behavior test cases
```

Nothing else belongs at the top level of a skill folder.

---

## 6. `SKILL.md`

### 6.1 Frontmatter

Only these keys are allowed, so the skill uploads cleanly to claude.ai and works in Claude Code:

```yaml
---
name: exploratory-data-analysis
description: One paragraph saying what the skill does and exactly when to use it.
metadata:
  version: 1.0.0
---
```

Also allowed when genuinely needed: `license`, `allowed-tools`, `compatibility`. Do not use Claude Code–only keys (`argument-hint`, `disable-model-invocation`, `model`, …); they break portability.

### 6.2 The `description`

The description is what makes Claude pick the skill (and what `/` autocomplete shows). It is the most important line in the skill.

* Say **what it does** and **when to use it**, including the words a user would actually type (file types, task names, synonyms).
* Say when **not** to use it if a neighbouring skill could be confused with it.
* Third person, present tense. At most 1024 characters. No `<` or `>` characters.
* See `.claude/skills/the-skillsmith/references/writing-guide.md` for examples.

### 6.3 Body

Recommended outline (drop sections that do not apply):

1. `# Title` and a two- or three-sentence purpose.
2. **When to use / when not to use.**
3. **Bundled Resources** — a table listing *every* file in `references/`, `scripts/`, and `assets/` with "open it when …". Paths are relative to the skill folder.
4. **Workflow** — numbered steps or modes.
5. **Rules** — the constraints that always apply.
6. **Definition of Done** — how Claude knows the task is finished.

Limits and style:

* Keep `SKILL.md` under ~500 lines. Move detail to `references/` before it grows past that.
* Write instructions in the imperative, and explain *why* a rule exists when the reason is not obvious.
* Every path mentioned under `references/`, `scripts/`, or `assets/` must exist, and every file in those folders must be mentioned.
* Never include secret values, credentials, or real personal data.

---

## 7. `config/skill.yaml`

The machine-readable manifest. Claude Code builds the `/` command from `SKILL.md` frontmatter; `skill.yaml` is what the repository tooling reads to validate, catalog, install, and package skills, and it can also hold a machine-readable summary of the skill's policy.

Required header (top-level keys, in this order):

```yaml
name: exploratory-data-analysis     # = folder name = SKILL.md name
version: 1.0.0                      # = SKILL.md metadata.version (semver)
description: >                      # one short human sentence for the catalog
  Systematic profiling of a new dataset before cleaning or modeling.
domain: data-science                # = parent domain folder ("meta" for .claude/skills)
type: specialized                   # core | specialized
```

Optional header keys:

```yaml
extends: the-data-scientist         # specialized only; must name an existing core skill
requires:                           # runtime dependencies of scripts/
  - python>=3.10
  - pandas
tags: [eda, profiling]              # free-form, for search
```

Everything after the header is free-form, skill-specific policy (workflow steps, gates, limits), as in `the-architect`. The tooling only parses the top-level header keys, so keep them as plain scalars or simple `- item` lists.

---

## 8. `references/`

* One topic per file, kebab-case names: `eda-checklist.md`, `stack-profiles.md`.
* Output templates are named `UPPER_SNAKE.template.md`: `EDA_REPORT.template.md`, `PRD.template.md`.
* A reference longer than ~300 lines starts with a short table of contents.
* References may point to other files inside the same skill, never outside it.

## 9. `scripts/`

* Python 3.10+. Prefer the standard library. Third-party packages must be listed under `requires` in `skill.yaml`, and the script must fail with a clear install hint if one is missing.
* Every script supports `--help`, takes paths as arguments, and prints machine-readable output (JSON) when its result is consumed by Claude.
* Scripts never modify input data, never write outside the paths they are given, and never make network calls unless that is their stated purpose.
* Each script is documented in the Bundled Resources table with its exact command line: `python <skill-dir>/scripts/<script>.py <args>`.
* Test every script on a realistic input before committing it.

## 10. `assets/`

Files that end up in the output (images, boilerplate code, fonts, sample configs). They are copied or referenced, not read into context. List each one in Bundled Resources.

## 11. `evals/evals.json`

Recommended for every skill; required before a skill reaches version 1.0.0 if it has scripts. A JSON list of cases:

```json
[
  {
    "id": "csv-first-look",
    "prompt": "I just got sales_2025.csv, what's in it?",
    "should_trigger": true,
    "expected_behavior": [
      "Runs scripts/profile_data.py before writing conclusions",
      "Reports missing values with counts and percentages"
    ]
  },
  {
    "id": "not-for-dashboards",
    "prompt": "Build me a Grafana dashboard for these metrics",
    "should_trigger": false
  }
]
```

Include at least two `should_trigger: true` cases and one `should_trigger: false` case. Use them to check the description after every change.

## 12. `README.md` (of a skill)

For the human owner, not for Claude. Required sections:

* `# <name>` and a one-paragraph summary.
* `## When to use` — typical requests, and how to invoke it (`/<name>`).
* `## Structure` — the folder tree with a line per file.
* `## Changelog` — newest first, one entry per version: `### 1.1.0 — 2026-09-10` followed by bullet points.

---

## 13. Versioning

Semantic versioning, kept identical in `SKILL.md` (`metadata.version`) and `config/skill.yaml` (`version`):

* **patch** — wording fixes, clarifications, typo fixes in references.
* **minor** — new reference, new script, new mode or step, stricter but compatible rules.
* **major** — changed workflow, removed or renamed files, changed output format.

Every version bump gets a Changelog entry. New skills start at `0.1.0` while they are being shaped and move to `1.0.0` once they have been used on real work and have evals.

---

## 14. Tooling

All commands run from the repository root and need only Python 3.10+:

| Command | Does |
|---|---|
| `python tools/skills.py list` | List every skill with domain, type, and version |
| `python tools/skills.py validate [names…]` | Check skills against this standard (exit code 1 on errors) |
| `python tools/skills.py new <domain>/<name> --type core\|specialized [--extends X] [--with references,scripts,assets]` | Scaffold a new skill (and the domain folder if needed) |
| `python tools/skills.py catalog [--check]` | Regenerate the catalog in `README.md` and each domain `README.md` |
| `python tools/skills.py install [names…\|--all] [--mode link\|copy]` | Install into `~/.claude/skills/` (link = edits in the repo apply immediately) |
| `python tools/skills.py uninstall <names…>` | Remove skills this tool installed; never touches anything else |
| `python tools/skills.py package [names…\|--all]` | Build `dist/<name>.zip` for upload to claude.ai |

Meta skills in `.claude/skills/` are validated and cataloged but never installed or packaged; they only make sense inside this repository.

---

## 15. Checklist Before Committing a Skill

- [ ] Name follows section 4 and matches folder, `SKILL.md`, and `skill.yaml`.
- [ ] Description says what and when, with real trigger words; ≤ 1024 chars; no angle brackets.
- [ ] Every bundled file is listed in `SKILL.md`, and every listed file exists.
- [ ] Scripts run on a realistic input; dependencies are declared in `requires`.
- [ ] `evals/evals.json` covers trigger and non-trigger cases.
- [ ] Version bumped in both places, with a Changelog entry.
- [ ] `python tools/skills.py validate` passes with no errors.
- [ ] `python tools/skills.py catalog` has been run.
- [ ] No secrets, credentials, or real personal data anywhere in the skill.
