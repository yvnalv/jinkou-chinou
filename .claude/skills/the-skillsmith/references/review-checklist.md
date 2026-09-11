# Review Checklist

Quality checks that `tools/skills.py validate` cannot do. Use it before finishing any mode, and as the core of a Mode D audit. Report findings as: item, evidence, proposed fix.

## Trigger and scope

- [ ] The description says what, when, and not-for, using words a user would really type.
- [ ] Every eval prompt with `should_trigger: true` clearly matches the description; every near miss clearly does not.
- [ ] No other skill in the repository has an overlapping description. Run `python tools/skills.py list --json` and compare.
- [ ] The name works as a slash command: clear, not too long, and no confusable neighbour.

## Placement

- [ ] The domain is the right field of expertise; a new domain is not a near-duplicate of an existing one.
- [ ] The type is right: a core skill is a broad persona, a specialized skill is one focused job.
- [ ] `extends` is set only where the specialized skill really builds on the core skill's workflow.
- [ ] It would not be better as a reference inside an existing skill (standard section 4.1).

## Content quality

- [ ] The workflow is complete from start to finish, including what to do when inputs are missing or wrong.
- [ ] It captures real expertise (gates, checklists, failure modes), not generic advice Claude already follows.
- [ ] Rules are justified where the reason is not obvious, and emphasis is reserved for true hard rules.
- [ ] The definition of done is observable.
- [ ] `SKILL.md` stays lean; detail lives in references, each referenced at the step where it is needed.
- [ ] Terminology is consistent across `SKILL.md`, references, `skill.yaml` policy, and README.
- [ ] Facts that go stale (versions, prices, APIs, regulations) are flagged for verification rather than stated as permanent truth.

## Self-containment and portability

- [ ] No paths outside the skill folder and no references to other skills' files (meta skills are exempt).
- [ ] Only portable frontmatter keys (`name`, `description`, `metadata`, plus `license`, `allowed-tools`, `compatibility` when needed).
- [ ] Scripts run without network access and with common dependencies, so they also work in the claude.ai sandbox; heavier dependencies are optional and degrade gracefully.
- [ ] Commands use `python <skill-dir>/scripts/...` so they work wherever the skill is installed.

## Scripts

- [ ] Each script was run on realistic and messy input during this session, and the output was checked.
- [ ] `--help` is accurate; errors are clear; the exit code is non-zero on failure.
- [ ] Inputs are never modified; outputs go only where asked.
- [ ] Dependencies are declared in `requires` and checked with an install hint.

## Safety

- [ ] Destructive or irreversible actions are gated behind explicit user approval.
- [ ] No secrets, credentials, or real personal data anywhere, including evals and examples.
- [ ] Personal data in outputs is masked by default when relevant.

## Housekeeping

- [ ] The README structure tree matches the real files.
- [ ] The version is bumped in both places, with a dated changelog entry.
- [ ] `python tools/skills.py catalog` has been run and `validate` shows no errors.
