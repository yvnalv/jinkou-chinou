# Evaluation

Proving a model is good enough for its decision: the right metric, honest validation, uncertainty, calibration, thresholds, slices, error analysis, and online confirmation. `scripts/model_report.py` computes the offline report.

## Contents

1. Choosing metrics
2. Honest validation
3. Uncertainty
4. Calibration
5. Thresholds and costs
6. Slices and fairness checks
7. Error analysis
8. Robustness
9. Online evaluation
10. Acceptance criteria

---

## 1. Choosing metrics

| Task | Ranking / quality | At the operating point | Probabilistic |
|---|---|---|---|
| Binary classification | ROC AUC; **PR AUC** when positives are rare | Precision, recall, F1, or cost at the chosen threshold; recall at a fixed alert rate | Log loss, Brier score, calibration error (ECE) |
| Multiclass | Macro F1 (classes equally important), weighted F1 | Per-class precision and recall; confusion matrix | Log loss |
| Regression | MAE (robust, interpretable), RMSE (penalizes large errors), R² | Share of predictions within a business tolerance | Prediction intervals and their coverage |
| Forecasting | MAE / RMSE per horizon, MASE or relative MAE vs seasonal naive | Error on the aggregated level where decisions happen | Quantile (pinball) loss, interval coverage |
| Ranking / recommendation | NDCG@k, MAP, MRR, recall@k | Business metric in A/B test | — |
| Anomaly detection | Precision at alert budget | Alerts per day, time to detection | — |

Report MAPE only when targets are far from zero; otherwise use sMAPE or scaled errors. Always report the baseline's score next to the model's.

## 2. Honest validation

* Use the split that mirrors production (`references/data.md` section 6): out-of-time for future predictions, grouped for repeated entities.
* Select models and hyperparameters on validation folds; evaluate **once** on the locked test set.
* Check for leakage before celebrating (`scripts/leakage_check.py`); a surprisingly high score is more often a leak than a breakthrough.
* Evaluate on the population and time period the model will serve; recent data is the best proxy for the near future.

## 3. Uncertainty

* Report **confidence intervals** (bootstrap over test rows; `model_report.py` does this) and CV mean ± standard deviation.
* When comparing two models, use **paired** comparisons on the same rows or folds; a difference inside the noise is not an improvement.
* For small test sets, intervals are wide; say so rather than overstating results.

## 4. Calibration

* If predicted scores are used as probabilities (expected value, risk tiers, thresholds that must mean something), check calibration: reliability table and **expected calibration error**.
* Recalibrate on validation data (isotonic regression for enough data, Platt / sigmoid scaling for small data) and verify on test.
* Class weighting, resampling, and many boosting settings distort calibration; always recheck after them.

## 5. Thresholds and costs

* The default 0.5 threshold is rarely right. Choose it from the decision: the cost of a false positive versus a false negative, a capacity limit (only 200 cases per day can be reviewed), or a required precision.
* Select thresholds on **validation** data and confirm on test. `model_report.py --cost-fp 1 --cost-fn 5` reports the cost-optimal threshold.
* Show stakeholders the trade-off (precision–recall curve, cost per threshold), not a single number.

## 6. Slices and fairness checks

* Evaluate per segment that matters: region, product, customer tier, device, new versus existing users, and protected attributes where legally appropriate to measure (`model_report.py --slices`).
* Large gaps between slices are findings: data coverage problems, different base rates, or real unfairness (`references/responsible-ml.md`).
* Check small but important slices separately; averages hide them.

## 7. Error analysis

* Read the worst errors: highest-confidence mistakes, largest residuals, systematic misses per slice.
* Group errors into causes (label noise, missing feature, rare case, data bug, genuinely unpredictable) and count them; fix the biggest actionable cause.
* Look for patterns in residuals versus features and time (seasonality not captured, drift).

## 8. Robustness

* Stress tests: missing features at serving time, unseen categories, out-of-range values, noisy inputs.
* Stability: performance across time periods (backtesting windows) and across CV folds.
* For deep learning: evaluate under realistic corruptions (blur, lighting, typos) when relevant.

## 9. Online evaluation

* Offline metrics are a proxy. Confirm with a **controlled online test**: A/B test or champion–challenger on the business metric and guardrails, with a pre-defined duration and sample size.
* **Shadow mode** first for risky models: score live traffic without acting, compare with the current system.
* Keep a small **holdout** group without model-driven actions to measure long-term effect and to keep collecting unbiased labels.

## 10. Acceptance criteria

Before deployment, all must hold (record them in the model card, `references/MODEL_CARD.template.md`):

- [ ] Beats the baseline on the primary metric by more than the uncertainty, on the locked test set with the production-like split.
- [ ] Meets the agreed bar on the operating-point metric and guardrails.
- [ ] Calibrated if scores are used as probabilities.
- [ ] No unacceptable slice gaps; fairness review done where people are affected.
- [ ] Leakage check clean, or remaining findings explained.
- [ ] Error analysis done; known limitations documented.
