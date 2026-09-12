# the-ml-engineer

End-to-end ML engineering persona for predictive models: problem framing, data collection and labeling, validation, EDA for modeling, feature engineering, training and tuning, rigorous evaluation, deployment, and MLOps monitoring and retraining. It covers tabular classification and regression, time series forecasting, deep learning for text and images, recommendation, and anomaly detection, and it is built to catch the usual killers of ML projects: leakage, wrong splits, and over-optimistic evaluation.

Domain: `ml-engineering` · Type: `core`

## When to use

Invoke with `/the-ml-engineer`, or let Claude pick it up automatically when you ask for things like:

- "Build a churn model for our subscription data, end to end." (A → B → C → D → E)
- "We need a weekly demand forecast per store." (A → E, forecasting)
- "Our fraud model scores 0.99 AUC in validation — is that real?" (F, leakage)
- "Accuracy dropped since last month; find out why." (F, drift)
- "Put this scikit-learn model behind an API with monitoring." (E)

| Mode | For | Output |
|---|---|---|
| A — Frame & Design | Decision, label, prediction time, metrics, baseline, feasibility | `docs/ml/ML_DESIGN.md` |
| B — Data | Point-in-time training table, labeling, validation, EDA, production-like split | Data pipeline, leakage report |
| C — Build & Train | Features, baselines, model ladder, tuning, tracking | Training pipeline, tracked runs |
| D — Evaluate | Intervals, calibration, thresholds, slices, fairness, error analysis | Model report, model card |
| E — Deploy & Operate | Packaging, serving, registry, rollout, monitoring, retraining | Service or batch job, drift reports, readiness review |
| F — Diagnose & Fix | Suspicious scores, production drops | Root cause, fix, updated model card |

Gates: **Leakage** (before trusting a score), **Evaluation** (before deployment), **Deployment** (before production traffic).

### Scripts and templates on their own

```text
python scripts/leakage_check.py --train train.csv --test test.csv --target churned --id customer_id --time event_date
python scripts/model_report.py preds.csv --task binary --y-true y_true --y-score y_score --cost-fp 1 --cost-fn 5 --slices plan
python scripts/drift_report.py --reference train.csv --current predictions.jsonl --columns tenure,plan,spend
python assets/train_pipeline.template.py --data churn.csv --target churned --task classification --split time --time-col event_date --out models/churn
MODEL_DIR=models/churn uvicorn serve:app        # after copying serve_api.template.py next to train.py as serve.py
```

Requirements: Python 3.10+, pandas, numpy; scikit-learn for the training template and adversarial validation; FastAPI + uvicorn for serving; MLflow optional.

## Structure

```text
the-ml-engineer/
├── SKILL.md                                  # lifecycle modes, principles, gates, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml                            # manifest + machine-readable policy
├── references/
│   ├── problem-framing.md                    # decision → task, label and prediction time, metrics, baselines
│   ├── data.md                               # collection, labeling, validation, versioning, EDA, splits, leakage
│   ├── features.md                           # pipelines, train-serving parity, preprocessing, feature patterns
│   ├── modeling.md                           # model ladder; tabular, forecasting, DL, recsys, anomaly; tuning; tracking
│   ├── evaluation.md                         # metrics, honest validation, CIs, calibration, thresholds, slices
│   ├── deployment-mlops.md                   # packaging, serving, registry, CI/CD/CT, monitoring, retraining
│   ├── responsible-ml.md                     # fairness, explainability, privacy, EU AI Act timeline
│   ├── ML_DESIGN.template.md
│   ├── MODEL_CARD.template.md
│   └── ML_READINESS.template.md
├── scripts/
│   ├── leakage_check.py                      # split and leakage checks, adversarial validation
│   ├── model_report.py                       # metrics with CIs, calibration, thresholds, slices
│   └── drift_report.py                       # schema, data quality, PSI/KS drift, prediction drift
├── assets/
│   ├── train_pipeline.template.py            # locked test set, right CV, baselines, metadata, optional MLflow
│   └── serve_api.template.py                 # FastAPI serving with shared features and prediction log
└── evals/
    └── evals.json
```

Research basis (verified 2026-09-11): leakage taxonomy and model info sheets (Kapoor & Narayanan), MLflow 3 (models as first-class logged models), tabular foundation models (TabPFN-2.5, TabICLv2) versus gradient boosting on small data, time series foundation models (Chronos-2, TimesFM-2.5) versus statistical baselines, current MLOps monitoring practice (feature and prediction drift before labels mature, gated retraining), multi-stage recommender practice, and the EU AI Act timeline after the May 2026 Digital Omnibus agreement.

## Changelog

### 0.1.1 — 2026-09-12

- Scope wording: camera and video systems now point to the new `computer-vision` domain (`the-cv-engineer`). No behavior change.

### 0.1.0 — 2026-09-11

- Initial version: six modes across the ML lifecycle, Leakage, Evaluation, and Deployment gates, seven references, three templates, three scripts (leakage check, model report verified against scikit-learn, drift report), and training and serving templates tested end to end.
