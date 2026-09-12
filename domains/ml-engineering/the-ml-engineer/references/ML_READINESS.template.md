# ML Production Readiness Review — <model / system>

| | |
|---|---|
| Scope | <model version, pipelines, services reviewed> |
| Inputs | <code, data, metadata, eval reports, leakage and drift reports, dashboards> |
| Date | <date> |

## 1. Summary

<Ready / Ready with conditions / Not ready — with the main reasons.>

## 2. Checklist

Mark each item Pass / Fail / N/A with evidence.

**Data**

- [ ] Data sources documented with owners; validation checks fail the pipeline on violations
- [ ] Features are point-in-time correct and available at prediction time (reviewed with a domain expert)
- [ ] `leakage_check.py` clean or findings explained
- [ ] Training data versioned; personal data minimized and access-controlled

**Model**

- [ ] Beats the baseline beyond uncertainty on a production-like, locked test set
- [ ] Operating threshold chosen from costs or capacity on validation data
- [ ] Calibrated if scores are used as probabilities
- [ ] Slice and fairness analysis done; gaps acceptable and documented
- [ ] Reproducible from code commit + data version + config + seed; experiment tracked
- [ ] Model card complete

**Serving**

- [ ] Whole pipeline packaged with signature and pinned dependencies
- [ ] Same feature code in training and serving; parity checked on a sample
- [ ] Input validation, timeouts, and a fallback when the model is unavailable
- [ ] Load-tested for latency and throughput (online) or run time (batch)
- [ ] Predictions logged with model version (no raw personal data unless allowed)

**Operations**

- [ ] Monitoring: service health, data quality, feature and prediction drift, performance when labels mature
- [ ] Alerts with owners and runbook; rollback tested
- [ ] Retraining trigger and promotion gate defined; feedback-loop holdout if actions affect labels
- [ ] Regulatory and responsible-ML review done where people are affected

## 3. Findings

| ID | Severity | Area | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|
| RDY-001 | <High> | <data / model / serving / operations / compliance> | <…> | <file:line, report, metric> | <…> |

## 4. Conditions for Launch

1. <must be fixed before launch>

## 5. Not Verified

- <what could not be checked and why>
