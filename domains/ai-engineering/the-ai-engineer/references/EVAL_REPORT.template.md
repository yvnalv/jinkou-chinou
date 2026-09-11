# Eval Report — <feature name>

| | |
|---|---|
| Dataset | <path>, <n> cases, version <sha / date> |
| Graders | <list; judge model and calibration result> |
| Harness | `eval_runner.py`, <reps> reps, oracle and null checks <passed / failed> |
| Date | <date> |

## 1. Summary

<Current quality versus the target, the decision this report supports, and the recommendation.>

## 2. Error Analysis

| Failure mode | Count (of n traces) | Example case | Status |
|---|---|---|---|
| <e.g. invents refund exceptions> | <12 / 80> | <id> | <fixed in v3 / open> |

## 3. Dataset

- Sources: <production traces (redacted) / expert-written / synthetic + reviewed>
- Tags and counts: <policy 40, extraction 25, adversarial 15, not-answerable 10, …>
- Ground truth provenance: <human-written / human-verified / model-generated (which model)>
- Must-pass cases: <n, what they cover>

## 4. Judge Calibration (if any)

| Judge | Human-labelled cases | Agreement | True-positive rate | True-negative rate |
|---|---|---|---|---|
| <faithfulness> | <50> | <0.92> | <0.94> | <0.89> |

## 5. Results

| Variant | Change | Pass rate (95% CI) | vs baseline (paired CI) | Cost per task | p95 latency | Decision |
|---|---|---|---|---|---|---|
| v1 (baseline) | — | <62% (55–69%)> | — | <…> | <…> | — |
| v2 | <one change> | <…> | <+8 pts (+3 to +13) → better> | <…> | <…> | <keep / revert> |

Regressions and flips worth noting: <case ids and reasons>.

By tag: <slices that moved, especially must-pass and safety cases>.

## 6. Held-out Test Result

<Final variant on the untouched test split, with CI.>

## 7. Limitations

<Noise floor, coverage gaps, stale cases, harness errors, anything not measured.>

## 8. Next Steps

- <next failure mode to address, cases to add, CI gate to enable>
