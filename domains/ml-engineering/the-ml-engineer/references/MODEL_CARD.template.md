# Model Card — <model name> v<version>

| | |
|---|---|
| Owner | <team, contact> |
| Model type | <e.g. gradient-boosted trees, scikit-learn pipeline> |
| Registered as | <registry name / alias, artifact path> |
| Training code | <repository @ commit> |
| Training data | <dataset name and version / hash, period covered> |
| Date | <date> |

## Intended Use

- **Decision supported:** <…>
- **Users:** <who consumes the predictions>
- **Out of scope:** <uses the model must not be used for>

## Data

- Population and period: <…>
- Label definition and maturity: <…>
- Preprocessing and features: <summary; feature list in metadata.json>
- Known data issues and biases: <…>

## Evaluation

Split: <out-of-time / grouped / random>, test period <…>, <n> rows.

| Metric | Baseline | Model (95% CI) | Target |
|---|---|---|---|
| <primary> | <…> | <…> | <…> |
| <operating point> | <…> | <…> | <…> |
| Calibration (ECE) | — | <…> | <≤ 0.05> |

Operating threshold: <value>, chosen by <cost / capacity / precision target> on validation data.

### Performance by Slice

| Slice | n | Metric | Gap vs overall |
|---|---|---|---|
| <segment = value> | <…> | <…> | <…> |

### Fairness

<Groups assessed, metrics, findings, mitigations, and the fairness definition chosen with its rationale.>

## Limitations and Risks

- <known failure modes, populations with little data, sensitivity to drift, feedback loops>

## Monitoring and Maintenance

- Monitored: <data quality, feature and prediction drift, performance when labels mature>
- Retraining: <schedule / trigger>; last retrained <date>
- Rollback: <previous version / fallback rule>

## Change Log

- v<version> (<date>): <what changed and why>
