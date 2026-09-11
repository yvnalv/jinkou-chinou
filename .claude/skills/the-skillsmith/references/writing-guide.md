# Writing Guide

How to write skill content that Claude picks up at the right moment and follows well.

## Contents

1. The description
2. What goes where
3. Degrees of freedom
4. Encoding expertise
5. Writing style
6. Scripts
7. Evals
8. Anti-patterns

---

## 1. The description

The description is the only part of a skill Claude sees before deciding to load it, and it is what `/` autocomplete shows. Formula:

```text
[What it does: concrete verbs + objects + result]
[Use when: the phrases, file types, and situations a user would actually mention]
[Not for: the nearest neighbouring tasks that should go elsewhere]
```

**Good:**

> Systematic exploratory data analysis (EDA) of a tabular dataset such as a CSV, Excel, Parquet or JSON file, a DataFrame, or a SQL result. Profiles structure, data quality, distributions, relationships, and target leakage, then writes an evidence-backed EDA report with a cleaning plan. Use when the user shares a dataset and asks what is in it, wants to explore, profile, audit or sanity-check data, or before modeling. Not for dashboards, pipelines, or training models.

**Bad:**

> Helps with data analysis.

It is too vague to trigger reliably, and it names no file types, verbs, or boundaries.

Rules:

* Third person, present tense ("Profiles…", "Creates…").
* Front-load the words users type: tool names, file extensions, task names, synonyms ("profile", "explore", "audit").
* 300–800 characters is typical; the hard limit is 1024.
* No `<` or `>`. If the text contains `: ` or starts with a special character, wrap it in double quotes (the scaffolder does this for you).
* Keep the catalog summary in `config/skill.yaml` separate: that is one short human sentence, not trigger text.

## 2. What goes where

| Content | Location | Why |
|---|---|---|
| Workflow, modes, rules that always apply, definition of done, the index of bundled files | `SKILL.md` | Loaded on every use, so keep it essential and under ~500 lines |
| Long checklists, domain knowledge, per-variant details (per stack, per format) | `references/*.md` | Loaded only when a step needs it |
| Output skeletons | `references/*.template.md` | Consistent deliverables |
| Deterministic, repetitive, or error-prone work (parsing, profiling, validation, conversions) | `scripts/*.py` | Reliable and cheaper than having Claude rewrite the code every time |
| Files copied into the output (boilerplate, images, sample configs) | `assets/` | Never read into context |
| Manifest plus a machine-readable policy summary | `config/skill.yaml` | Tooling and quick reference |
| Human-facing overview and changelog | `README.md` | Claude does not need it |

Each reference must be reachable: a row in Bundled Resources **and** a mention at the workflow step where it is used.

## 3. Degrees of freedom

Match how prescriptive the instructions are to how fragile the task is:

| Task | Freedom | Write |
|---|---|---|
| Fragile, exact, or destructive (migrations, file formats, validation) | Low | Exact commands, scripts, required order, stop conditions |
| Structured with a known good pattern (reports, reviews) | Medium | Templates, checklists, defaults that can be adapted |
| Judgment-heavy (analysis, design, writing) | High | Principles, heuristics, trade-off tables, examples |

Do not script judgment, and do not leave fragile operations to judgment.

## 4. Encoding expertise

A skill earns its place by capturing what an expert does that a capable generalist forgets:

* **Gates:** conditions that must hold before moving on ("no modeling before a leakage review").
* **Checklists:** the complete set of things to check, so nothing depends on memory.
* **Failure modes:** known traps, with how to detect and avoid each one.
* **Decision tables:** "if X, do Y" for the common forks.
* **Definition of done:** observable conditions, not "the task is complete".
* **What to ask first:** the few questions whose answers change the approach.

**Core (persona) skills** hold domain-wide principles, modes, and judgment: how this kind of expert thinks. **Specialized skills** hold one concrete workflow with its tools and outputs. A specialized skill copies the handful of core rules it depends on (for example "raw data is read-only") rather than referring to the core skill.

## 5. Writing style

* Imperative voice: "Run the profiler", not "The profiler should be run".
* Explain *why* when a rule is not self-evident; Claude applies rules better when it knows their purpose.
* Concrete thresholds and examples beat adjectives ("more than 5% missing", not "a lot of missing values").
* Tables for decisions and mappings; numbered lists for sequences; bullets for sets.
* Reserve emphasis (bold, "never") for the real hard rules. When everything is emphasized, nothing is.
* One term per concept throughout the skill.
* Paths are relative to the skill folder; script commands use `python <skill-dir>/scripts/<name>.py`.

## 6. Scripts

* Use `argparse` with a module docstring and examples, so `--help` is useful.
* For output Claude consumes: JSON, with `--out FILE` plus a short printed summary for large results.
* Exit code 0 on success and non-zero with a clear message on failure.
* Never modify inputs. Write only to the paths given. No network calls unless that is the purpose.
* Check third-party imports at the top and exit with an install hint; list them under `requires`.
* Test on realistic **and** messy data: missing values, wrong types, odd encodings, empty files, large files. Keep the test data out of the skill unless it belongs in `assets/` as an example.
* Mask personal data by default when output may include raw values.

## 7. Evals

* Write prompts the way the owner would really type them: short, informal, with file names.
* Vary the phrasing across cases; do not repeat the description's wording.
* Negative cases should be **near misses** (similar domain, different job), not obviously unrelated requests.
* Expected behaviors must be observable in a transcript: "runs X before Y", "reports counts with percentages", "asks for approval before Z".
* Update the evals whenever triggers or behavior change.

## 8. Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Vague description | Apply the formula in section 1 |
| `SKILL.md` as an encyclopedia | Move detail into references and keep an index |
| A reference that is never mentioned | Add it to Bundled Resources and to the workflow step |
| A skill depending on another skill's files | Copy what is needed; set `extends` for documentation only |
| Restating `SKILL_STANDARD.md` inside skills | Domain skills follow the standard; they do not quote it |
| Empty `scripts/` or `assets/` folders, filler sections | Remove them; proportional skills are better |
| Asking the user fifteen questions at once | Rounds of three to four, highest impact first |
| Scripts that dump huge unstructured output | JSON to a file plus a summary |
| Placeholder text left behind | The validator blocks `TODO(skillsmith)`; replace every one |
