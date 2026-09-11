---
name: exploratory-data-analysis
description: Systematic exploratory data analysis (EDA) of a tabular dataset such as a CSV, Excel, Parquet or JSON file, a DataFrame, or a SQL result. Profiles structure and grain, data quality (missing values, duplicates, outliers, wrong types, inconsistent categories, disguised nulls, personal data), distributions, relationships, and target leakage, then writes an evidence-backed EDA report with a cleaning plan. Use when the user shares a dataset and asks what is in it, wants to explore, profile, understand, audit or sanity-check data, or before cleaning, feature engineering, or modeling. Not for building dashboards, production pipelines, or training models.
metadata:
  version: 0.1.0
---

# Exploratory Data Analysis

Turn an unfamiliar dataset into a documented understanding: what one row means, what every column holds, what is wrong with the data, what patterns and risks exist, and what must be fixed before anyone models or reports on it. The result is an `EDA_REPORT.md`, supporting figures, a reproducible script, and a cleaning plan the user approves before anything is changed.

## When to Use

* "What's in this file?", "explore / profile / understand this data", "check this export for problems".
* Before cleaning, feature engineering, statistical testing, or modeling on data that has not been examined yet.
* Auditing data quality of a delivery from another team or system.

Do not use it for: dashboards and recurring reports, building production pipelines, or training and tuning models. Recommend those as next steps instead.

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `scripts/profile_data.py` | Step 2, the first mechanical pass: `python <skill-dir>/scripts/profile_data.py <file> --out eda/profile.json [--target COL] [--sheet NAME] [--sample N] [--dayfirst] [--raw-na]`. Prints a summary and writes a JSON profile: shape, duplicates, candidate keys, per-column kind and statistics, high correlations, target associations, and a ranked issue list. Masks suspected personal data. Needs pandas and numpy (pyarrow for Parquet, openpyxl for Excel). Run with `--help` for every option. |
| `references/eda-checklist.md` | Steps 3–6: the full checks per data-quality dimension and per column kind, missing-data and outlier analysis, relationships, time-based data, target and leakage checks, common pitfalls, and the cleaning-plan format. |
| `references/visualization-guide.md` | Whenever you create a chart: which chart answers which question, the standard EDA figure set, style rules, and plotting code conventions. |
| `references/EDA_REPORT.template.md` | Step 7: the structure of `EDA_REPORT.md`. |

## Workflow

### 0. Frame the analysis

Find out, from the conversation or by asking at most three short questions:

* **Purpose** — the decision or question the data should support.
* **Grain** — what one row represents (a customer, an order, a sensor reading per minute).
* **Target** — the outcome column, if the data is headed for modeling.
* **Context** — a data dictionary, the source system, the expected row count or time range.

If the user just says "explore this", do not block: proceed, state your assumptions, and revisit them when the data contradicts them.

### 1. Set up safely

* Treat the raw file as read-only. Load it into memory; never edit, overwrite, or re-save it.
* Put outputs in an `eda/` folder next to the data, or where the user asks: `eda/EDA_REPORT.md`, `eda/profile.json`, `eda/figures/`, and `eda/eda.py` (or a notebook if the project uses notebooks).
* Check the file size first. Above about 1 GB or 5 million rows, profile a random sample (`--sample`) and say so; compute exact counts on the full data where it is cheap.
* If the data is a DataFrame in a notebook or a SQL result, export it to Parquet or CSV for the script, or run the equivalent checks in code.

### 2. Run the mechanical profile

Run `scripts/profile_data.py` with `--out eda/profile.json` (add `--target` when there is an outcome column). Read the printed summary, then open the JSON for the columns that need detail. The profile is a starting point: it tells you where to look, not what to conclude.

If the script reports ambiguous dates, rerun with or without `--dayfirst` and compare. If NA-like tokens might be real values (for example `NA` for North America), rerun with `--raw-na`.

### 3. Validate structure and grain

* Confirm what one row is. Check candidate keys and duplicate IDs. Explain exact duplicate rows (true duplicates, or legitimate repeated events).
* Compare columns, types, row counts, and time coverage with the data dictionary or with what the user expects.
* List every type that must be fixed on load: numbers or dates stored as text, codes with leading zeros, booleans stored as words.

### 4. Assess data quality

Work through the quality dimensions and the checks for each column kind in `references/eda-checklist.md`. Give each issue an ID (`DQ-001`), a severity, evidence with counts, and a proposed action. Do not fix anything yet.

### 5. Understand each variable

Describe distributions: centre, spread, skew, and modes for numeric columns; frequencies and rare levels for categorical ones; coverage and gaps for dates. Plot only what answers a question (see `references/visualization-guide.md`).

### 6. Explore relationships

* Pairwise relationships between the important variables, and redundant or derived columns.
* With a target: class balance or distribution, the strongest associations, and a **leakage review** of every feature that is suspiciously predictive or recorded after the outcome.
* Segments and time: how key metrics differ across groups and periods, and whether the data drifts over time.

State every relationship as an association with its measure and sample size, never as a cause.

### 7. Write the report and the reproducible script

Fill `references/EDA_REPORT.template.md` into `eda/EDA_REPORT.md`. Every number in the report must come from `eda/eda.py` (or the notebook), which reruns the analysis from the raw file with fixed random seeds. Save figures to `eda/figures/` and reference them from the report.

Scale the report to the job: a quick look at a small file needs the summary, data dictionary, issues, and next steps. Say which sections you left out.

### 8. Present and wait

In chat, give: the readiness verdict (ready / ready after cleaning / not fit for purpose), the three to five most important findings, the high-severity issues, and the proposed cleaning plan. Ask for approval before applying any cleaning step.

## Rules

* **Raw data is read-only.** Cleaning is a plan first (issue, action, rows affected, rationale). Apply it only after approval, in code that is saved with the analysis, never by hand-editing data.
* **Evidence with denominators.** Write "148 of 2,010 rows (7.4%)", not "some rows". Name the statistic used, and say whether it comes from a sample.
* **Separate observation, hypothesis, and recommendation.** Associations are not effects; a hypothesis needs a test before it becomes a finding.
* **Characterize missing data before treating it.** How much, where, co-missing patterns, relation to time or the target, and disguised forms (sentinels such as -1 or 999, "N/A", empty strings, zeros that mean unknown).
* **Investigate outliers; never delete them automatically.** Separate impossible values (errors) from rare but real extremes.
* **Hunt for leakage** whenever a target exists: features known only after the outcome, near-perfect associations, IDs or timestamps that encode the label, and duplicates spanning future train and test splits.
* **Protect personal data.** Do not print raw personal values in chat, reports, or figures. Report counts and masked examples, and keep the script's masking unless the user explicitly needs the values.
* **Every chart answers a question.** No automatic walls of plots.
* **Stay in scope.** Do not train models or build pipelines here; recommend them as next steps.

## Definition of Done

* The profile has been run, and every column has a kind, a description, and its quality status in the data dictionary.
* Grain and keys are confirmed or explicitly flagged as uncertain.
* Every high-severity issue has evidence and a proposed action.
* With a target: its balance or distribution is described and leakage has been reviewed.
* `EDA_REPORT.md`, the figures, and the reproducible script are saved, and the report's numbers match the script's output.
* No raw personal data appears in any output.
* The user has seen the summary and the cleaning plan, and nothing has been changed without approval.
