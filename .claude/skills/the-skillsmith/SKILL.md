---
name: the-skillsmith
description: Creates, extends, changes, reviews, and upgrades skills in the jinkou-chinou skill repository so that every skill follows SKILL_STANDARD.md. Use when working in this repository and the user wants a new skill, a new domain, a specialized skill inside a domain, a change or version bump to an existing skill, an audit of a skill against the standard, or to import an outside skill into the collection. Not for running the skills themselves.
metadata:
  version: 0.1.0
---

# The Skillsmith

Forge skills for the jinkou-chinou collection: understand what the skill must do, place it in the right domain with the right type and name, build it from the standard skeleton, fill it with real expertise, test it, and leave the repository valid and cataloged.

This is a repo-local meta skill (domain `meta`). Unlike domain skills, it works with files outside its own folder:

| Repository file | Role |
|---|---|
| `SKILL_STANDARD.md` | The rules. Always authoritative, including over this skill. |
| `tools/skills.py` | `list`, `validate`, `new`, `catalog`, `install`, `uninstall`, `package` |
| `tools/templates/` | Skeleton files used by `skills.py new` |
| `domains/<domain>/<skill>/` | Existing skills: use them as examples of the house style |

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/writing-guide.md` | Writing or revising any skill content: the description formula with examples, what belongs in `SKILL.md` versus references versus scripts, degrees of freedom, how to encode expertise, script and eval guidance, anti-patterns. |
| `references/review-checklist.md` | Reviewing a skill before finishing (every mode), and in Mode D audits: the quality checks the validator cannot do. |

## Modes

| Request | Mode |
|---|---|
| A skill that does not exist yet (possibly in a new domain) | A — New skill |
| Knowledge that extends an existing skill's workflow | B — Extend with a reference |
| Change the behavior, content, or files of an existing skill | C — Change |
| Check a skill against the standard, fix it up, or import an outside skill | D — Audit / Upgrade / Import |

Always start by reading `SKILL_STANDARD.md` in full; it may have changed since this skill was written. Then run `python tools/skills.py list` to see what exists.

### Mode A — New skill

1. **Understand the job.** Ask in rounds of at most four questions, skipping anything the conversation already answers:
   * What does the skill produce (files, code, an answer, a decision), and for whom?
   * Three realistic requests that should trigger it, in the user's own words, and one or two similar requests that should not.
   * What does an expert in this field do that a capable generalist forgets? Gates, checklists, failure modes, quality bars. This is the value of the skill; dig for it.
   * Does it need deterministic helpers (scripts), output templates, or reference knowledge? Any dependency limits for claude.ai?
2. **Check for overlap.** If an existing skill already covers the workflow, switch to Mode B or C and say why.
3. **Propose placement, and get confirmation before scaffolding:**
   * **Domain:** an existing one, or a new kebab-case field name that is unambiguous across all knowledge (standard section 3).
   * **Type:** `core` is the domain's single persona, named `the-<persona>`. `specialized` is one focused job with a descriptive name and no `the-`.
   * **extends:** set it only when the domain's core skill exists and this skill builds on its workflow.
   * **Name:** it is the slash command, so it must be clear when typed, unique across the repository, and 64 characters or fewer.
   * **Folders:** only the optional ones the skill will really use.
4. **Scaffold:**
   `python tools/skills.py new <domain>/<name> --type <core|specialized> [--extends <core-skill>] [--with references,scripts,assets] --summary "<one sentence>" --description "<trigger description>"`
5. **Write the content** following `references/writing-guide.md`:
   * `SKILL.md`: the description first, then purpose, when to use, Bundled Resources (every file), workflow, rules, and definition of done. Keep it under about 500 lines.
   * `references/`: one topic per file; output templates named `UPPER_SNAKE.template.md`.
   * `scripts/`: write them, then **run them on realistic and messy input** and fix what breaks. Declare dependencies under `requires`.
   * `evals/evals.json`: at least two should-trigger cases and one near-miss should-not-trigger case, with observable expected behaviors.
   * `README.md`: when to use, a structure tree that matches the real files, and the changelog.
   * `config/skill.yaml`: the header, plus an optional policy summary that agrees with `SKILL.md`.
   * For a new domain: the scope paragraph in `domains/<domain>/README.md`.
   * For a specialized skill that extends a core skill: copy in the core rules it depends on. It must work alone.
6. **Verify:** `python tools/skills.py catalog`, then `python tools/skills.py validate`. Fix every error, and fix or explain every warning.
7. **Review** with `references/review-checklist.md`. Read each eval prompt against the description and workflow: would it trigger, and would it produce the expected behavior?
8. **Install and hand over:** `python tools/skills.py install <name>` links it into `~/.claude/skills/`, so edits in the repository apply immediately and `/<name>` works in new sessions. For claude.ai, run `python tools/skills.py package <name>` and upload `dist/<name>.zip`.
9. **Report** the files created, the placement decisions, the validation result, what was actually tested, and any open questions.

### Mode B — Extend with a reference

Use when the new knowledge serves the same workflow as an existing skill (a new stack, format, or checklist).

1. Add the file under the skill's `references/` (or `assets/`) and add a row to its Bundled Resources table saying when to open it.
2. Mention it at the workflow step where it is needed.
3. Minor version bump, following Mode C steps 3–6.

### Mode C — Change an existing skill

1. Read the skill's `SKILL.md`, `README.md`, and `config/skill.yaml` before editing.
2. Make the change. Move detail into references rather than growing `SKILL.md`.
3. Bump the version in **both** `SKILL.md` and `config/skill.yaml` (patch: wording; minor: new file, step, or rule; major: changed workflow or output). Add a dated changelog entry and update the README structure tree.
4. Update `evals/evals.json` when triggers or behavior changed.
5. If a **core** skill changed, find every skill that extends it (`python tools/skills.py list`) and check whether the rules they copied are still correct.
6. Run `catalog` and `validate`.

### Mode D — Audit, upgrade, or import

1. Run `python tools/skills.py validate <name>` and work through `references/review-checklist.md`.
2. Report the findings (validator errors, gaps against the standard, quality problems) and a proposed plan **before** changing anything.
3. After approval, upgrade the skill: patch bump for structure-only fixes, minor or major when content changes.
4. **Importing an outside skill:** place it in the right domain; rename it to follow the naming rules; remove non-portable frontmatter keys; add `config/skill.yaml`, `README.md`, and evals; make it self-contained; start the changelog with the import.

## Rules

* **The standard is the authority.** If this skill and `SKILL_STANDARD.md` disagree, follow the standard and tell the user this skill needs updating.
* **Never change a rule silently.** When the user wants a different rule, update `SKILL_STANDARD.md` first, then the validator in `tools/skills.py`, the templates, and this skill, all in the same change.
* **Domain skills stay self-contained.** They never refer to files outside their own folder, and never to another skill's files.
* **Do not invent expertise.** When a skill encodes knowledge you are unsure about (regulations, version-specific tools, medical or legal specifics), say so, ask, or check official sources.
* **Proportional skills.** No empty folders, filler references, or ceremonial sections. A specialized skill can be just `SKILL.md`, `README.md`, and `config/skill.yaml`.
* **Test for real.** Never claim a script works without running it. Report which paths were not tested.
* **No secrets or personal data** in any skill file, example, or eval.
* **Version control:** do not commit or push unless the user asks. Commit messages describe the change, with no AI attribution or co-author trailers.

## Definition of Done

* `python tools/skills.py validate` reports no errors, and remaining warnings are explained to the user.
* The catalog in `README.md` and the domain README is regenerated.
* Every script has been run on realistic input.
* Evals exist and were checked against the description.
* The user knows the slash command, the install command, and the claude.ai package command, plus anything left untested or open.
