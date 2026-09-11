# CLAUDE.md

This repository is **jinkou-chinou** (人工知能, "artificial intelligence"): a personal collection of AI skills for Claude Code, the Claude Code VS Code extension, and claude.ai, organized by domain of expertise.

## Rules for working here

1. **`SKILL_STANDARD.md` is the law.** Every skill follows it. Read it before creating or changing any skill.
2. **Use `/the-skillsmith`** (in `.claude/skills/the-skillsmith/`) to create, extend, change, audit, or import skills. It walks through the standard step by step.
3. **Never hand-edit the catalog blocks** between `<!-- catalog:start/end -->` in `README.md` or `<!-- skills:start/end -->` in domain READMEs. Run `python tools/skills.py catalog`.
4. **Validate before finishing:** `python tools/skills.py validate` must report 0 errors.
5. **Domain skills are self-contained.** A skill never refers to files outside its own folder or to another skill's files.
6. **Version every change** to a skill: bump `metadata.version` in `SKILL.md` and `version` in `config/skill.yaml` together, and add a dated entry to the skill's README changelog.
7. **Changing a rule** means updating `SKILL_STANDARD.md`, the validator in `tools/skills.py`, `tools/templates/`, and `the-skillsmith` together, in one change.

## Layout

```text
SKILL_STANDARD.md                 rules (single source of truth)
README.md                         overview + generated catalog
.claude/skills/the-skillsmith/    repo-local meta skill for authoring skills
tools/skills.py                   list | validate | new | catalog | install | uninstall | package
tools/templates/                  skeletons used by `skills.py new`
domains/<domain>/<skill>/         the skills, grouped by field of expertise
```

## Commands

```text
python tools/skills.py list
python tools/skills.py validate [names...]
python tools/skills.py new <domain>/<name> --type core|specialized [--extends X] [--with references,scripts,assets]
python tools/skills.py catalog [--check]
python tools/skills.py install <names...>|--all [--mode link|copy]    # into ~/.claude/skills
python tools/skills.py package <names...>|--all                      # dist/<name>.zip for claude.ai
```

## Environment

Windows machine; Python 3.10+ on PATH as `python`. `tools/skills.py` is standard-library only. Skill scripts may need extra packages; each skill lists them under `requires` in `config/skill.yaml`.

## Version control

Commit or push only when asked. Commit messages describe the change; no AI co-author trailers or attribution lines. `dist/`, `__pycache__/` and local settings are ignored.
