# ML Design — <model / use case>

| | |
|---|---|
| Status | <Draft / Agreed> |
| Owner | <who decides and maintains> |
| Date | <date> |

## 1. Decision and Value

- **Decision the model supports:** <who acts, how often, on what>
- **Current approach (baseline):** <rule, manual process, none> and its performance
- **Value of improvement:** <money, time, risk reduced>
- **Why ML (and not rules):** <reason>

## 2. ML Task

| | |
|---|---|
| Task type | <binary classification / regression / forecasting / ranking / anomaly detection / …> |
| Unit of prediction | <one row per … per scoring date> |
| Prediction time (t₀) | <when the model is called> |
| Label | <precise definition> |
| Label window and maturity | <e.g. outcome within 30 days after t₀; labels final after 45 days> |

## 3. Metrics and Acceptance Bar

| Level | Metric | Baseline | Target |
|---|---|---|---|
| Business | <…> | <…> | <…> |
| Primary offline | <e.g. PR AUC on out-of-time test> | <…> | <…> |
| Operating point | <e.g. recall at 5% alert rate, or cost at chosen threshold> | <…> | <…> |
| Guardrails | <slice gaps, latency, calibration> | <…> | <…> |

Cost of errors: false positive <…>, false negative <…>.

## 4. Data

| Source | Owner | Grain | History | Refresh | Point-in-time available? | Notes |
|---|---|---|---|---|---|---|
| <table / API> | <team> | <…> | <from … to …> | <daily> | <yes / no> | <quality issues, consent> |

Labeling plan (if needed): <guidelines, annotators, agreement target, volume>.

## 5. Features

| Feature group | Examples | Available at t₀ from | Risk (leakage, sensitivity) |
|---|---|---|---|
| <behavior, last 30 days> | <tickets_30d, logins_30d> | <event tables, as of t₀> | <…> |

## 6. Validation Plan

- Split: <out-of-time / grouped / random> because <…>; gap: <…>
- CV scheme: <…>; locked test period: <…>
- Leakage review: `leakage_check.py` plus feature-availability review with <domain expert>

## 7. Modeling Plan

Baselines: <…>. Candidates: <…>. Tuning budget: <…>. Tracking: <MLflow experiment name>.

## 8. Deployment and Operations

| | |
|---|---|
| Serving | <batch daily / online API / streaming> |
| Latency and volume | <p95 target, requests per second or rows per run> |
| Consumers | <system or team using predictions> |
| Monitoring | <data quality, drift, performance when labels mature; alert owners> |
| Retraining | <schedule / trigger; comparison with production model> |
| Rollback | <previous model / rule-based fallback> |

## 9. Risks and Responsible ML

<People affected, fairness groups and metrics, explainability needs, privacy, regulatory category (e.g. EU AI Act Annex III?), feedback loops, misuse.>

## 10. Open Questions

| # | Question | Impact | Owner | Status |
|---|---|---|---|---|
| 1 | <…> | <…> | <…> | <open> |
