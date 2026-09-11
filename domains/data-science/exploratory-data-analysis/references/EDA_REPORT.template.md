# EDA Report — <dataset name>

| | |
|---|---|
| Source | <system or person that provided it; how it was extracted> |
| File(s) | <path, format, size, sheet if Excel> |
| Shape | <rows> rows × <columns> columns <(sample: method and size, if sampled)> |
| Grain | One row = <entity/event> |
| Time coverage | <first> to <last> <(time zone)> |
| Analysed on | <date> by <who>, with `eda/eda.py` (Python <version>, pandas <version>) |

## 1. Summary

**Readiness:** <Ready | Ready after cleaning | Not fit for purpose> — <one-sentence reason>.

- <Most important finding, with evidence>
- <Second finding>
- <Third finding>
- <Biggest data-quality risk>
- <Recommended next step>

## 2. Context and Questions

<Purpose of the analysis, the decision it supports, the target (if any), assumptions made where context was missing.>

## 3. Dataset Overview

- **Keys:** <candidate key(s); duplicate rows and duplicate IDs with counts>
- **Column kinds:** <n numeric, n categorical, n datetime, …>
- **Compared with expectations:** <row count, columns, and coverage versus the data dictionary or stated expectations>

## 4. Data Dictionary

| Column | Kind | Meaning | Missing | Unique | Notes |
|---|---|---|---|---|---|
| <name> | <numeric / categorical / datetime / boolean / identifier / text> | <what it represents, unit> | <n (%)> | <n> | <quality issue IDs, type fixes, personal data flag> |

## 5. Data Quality Issues

| ID | Severity | Column(s) | Issue | Evidence | Proposed action |
|---|---|---|---|---|---|
| DQ-001 | <High / Medium / Low> | <column> | <what is wrong> | <counts with denominators> | <action> |

## 6. Variable Findings

<Key distributions and what they mean. Reference figures:>

![<alt text>](figures/02_numeric_distributions.png)
*<One-line takeaway.>*

## 7. Relationships and Target

<Strongest relationships with their measures and n; redundant columns; segment and time patterns. With a target: balance or distribution, top associations.>

## 8. Leakage and Bias Risks

| Feature or aspect | Risk | Evidence | Recommendation |
|---|---|---|---|
| <feature> | <leakage / selection bias / drift / …> | <measure, timing argument> | <exclude / verify timing / …> |

## 9. Hypotheses to Test

- <Hypothesis — why it is plausible, and how to test it. Not a conclusion.>

## 10. Recommended Cleaning Plan

Awaiting approval. Nothing below has been applied.

| Step | Issue | Action | Rows affected | Rationale | Reversible? |
|---|---|---|---|---|---|
| 1 | DQ-001 | <action> | <n (%)> | <why> | <yes / no> |

## 11. Next Steps

- <For example: apply the approved cleaning plan and re-profile; feature engineering; baseline model with a time-based split; request the data dictionary for columns X and Y.>

## Appendix: Reproduction

```text
python <skill-dir>/scripts/profile_data.py <file> --out eda/profile.json <options>
python eda/eda.py
```

- Random seed: <seed>
- Figures: <list of files in eda/figures/>
- Sections omitted: <none, or which and why>
