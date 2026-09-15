# Antigravity Agent Guidelines for jinkou-chinou

This repository hosts **jinkou-chinou**, a standardized collection of AI domain skills.

## Slash Command & Skill Invocations

When the user types a message starting with a slash command matching any skill in this repository:

* `/the-miner` — Activate the data acquisition, web scraping, and multi-sink persistence persona ([`.agents/skills/the-miner/SKILL.md`](.agents/skills/the-miner/SKILL.md)).
* `/exploratory-data-analysis` — Activate the tabular data profiling and quality analysis skill ([`.agents/skills/exploratory-data-analysis/SKILL.md`](.agents/skills/exploratory-data-analysis/SKILL.md)).
* `/the-architect` — Activate the planning-first software engineering persona ([`.agents/skills/the-architect/SKILL.md`](.agents/skills/the-architect/SKILL.md)).
* `/the-ai-engineer` — Activate the provider-neutral LLM systems persona ([`.agents/skills/the-ai-engineer/SKILL.md`](.agents/skills/the-ai-engineer/SKILL.md)).
* `/the-cv-engineer` — Activate the computer vision engineering persona ([`.agents/skills/the-cv-engineer/SKILL.md`](.agents/skills/the-cv-engineer/SKILL.md)).
* `/the-ml-engineer` — Activate the predictive machine learning persona ([`.agents/skills/the-ml-engineer/SKILL.md`](.agents/skills/the-ml-engineer/SKILL.md)).
* `/the-uix-designer` — Activate the UI/UX design and prototyping persona ([`.agents/skills/the-uix-designer/SKILL.md`](.agents/skills/the-uix-designer/SKILL.md)).
* `/the-skillsmith` — Activate the repo-local skill authoring and audit persona ([`.agents/skills/the-skillsmith/SKILL.md`](.agents/skills/the-skillsmith/SKILL.md)).

### Execution Behavior
Upon receiving a slash command:
1. Immediately read the corresponding `SKILL.md` file using `view_file` to review its workflow, operational modes, and gates.
2. Identify the target mode (e.g. Mode A for design/spec, Mode B for build, Mode C for repair, Mode D for audit, Mode E for quick execution).
3. Execute the mode strictly abiding by the rules and gates defined in that skill.
