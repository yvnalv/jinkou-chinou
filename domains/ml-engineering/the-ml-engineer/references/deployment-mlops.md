# Deployment and MLOps

Shipping models safely and keeping them good: packaging, serving patterns, registry and promotion, CI/CD and continuous training, monitoring, and retraining.

## Contents

1. MLOps maturity
2. Packaging
3. Serving patterns
4. Registry and promotion
5. CI/CD and continuous training
6. Monitoring
7. Retraining
8. Operations

---

## 1. MLOps maturity

Grow automation with need; don't build a platform for one model.

| Level | Characteristics | Good for |
|---|---|---|
| 0 — Manual | Notebook training, manual export, manual deployment | Proofs of concept only |
| 1 — Reproducible pipeline | Training pipeline as code, versioned data and models, tracked experiments, automated evaluation, scripted deployment | Most first production models |
| 2 — Automated CT and CD | Scheduled or triggered retraining, automatic validation gates, registry-driven deployment, monitoring with alerts | Many models, frequent change, high stakes |

## 2. Packaging

* Save the **whole pipeline** (preprocessing + model) as one artifact, plus metadata: feature list and types, training data version, metrics, library versions, and the training code commit (`assets/train_pipeline.template.py` writes `model.joblib` + `metadata.json`).
* Record an **input/output signature** (MLflow model signatures do this) and validate requests against it.
* Pin dependencies; build a container image for serving; for portability or low-latency inference consider exported formats (ONNX, TorchScript), verified to give identical predictions on a sample.
* Security: only load model files you produced or trust (pickle-based formats execute code on load).

## 3. Serving patterns

| Pattern | Use when | Notes |
|---|---|---|
| Batch scoring | Predictions needed on a schedule (daily churn scores, weekly forecasts) | Simplest and cheapest; write scores to a table; most business models should start here |
| Online API | Predictions needed per request with low latency (fraud at checkout, recommendations on page load) | FastAPI/BentoML for a service, KServe/Seldon/Ray Serve or a cloud endpoint at scale; features must be available online |
| Streaming | Continuous events with near-real-time decisions | Stream processor calls the model or embeds it; watch ordering and late data |
| Edge / on-device | Offline use, privacy, or latency on the device | Quantized or distilled models; update strategy for deployed models |

Online services (`assets/serve_api.template.py`): validate input, apply the shared feature code, return the model version, log inputs and outputs for monitoring (without raw personal data unless allowed), expose health and metadata endpoints, and set timeouts. Load-test for latency percentiles and throughput before launch.

## 4. Registry and promotion

* Register every candidate with its metrics, data version, and lineage (MLflow Model Registry or the platform's registry).
* Promote through stages or aliases (for example candidate → staging → production) only after automated checks pass and an owner approves.
* Keep the previous production model deployable for **instant rollback**.

## 5. CI/CD and continuous training

* **CI** on code changes: unit tests for feature functions (including point-in-time logic), data validation tests, a small training run, and the leakage check.
* **CT (continuous training)** pipeline: pull fresh data → validate → train → evaluate against the current production model on the same recent test window → register if better by a margin and all guardrails pass.
* **CD**: deploy from the registry with shadow or canary rollout, automatic rollback on error or metric regression.
* Everything as code: pipelines, infrastructure, and configuration versioned in the repository.

## 6. Monitoring

Monitor at four levels, because labels often arrive late:

| Level | What | How |
|---|---|---|
| Service | Latency, errors, throughput, resource use | Standard service monitoring |
| Data quality | Schema, missing rates, ranges, freshness of inputs | Validation checks on live inputs |
| Drift (proxy) | Feature drift and **prediction drift** versus the training window | `scripts/drift_report.py` on the prediction log (PSI, KS, unseen categories) |
| Performance | Actual metric once labels mature, per slice | `scripts/model_report.py` on logged predictions joined with outcomes |

* Drift is an early warning, not proof of degradation; some drift is harmless. Investigate, and confirm with labelled performance.
* Watch prediction distribution and action rates (alerts per day, offers sent); sudden changes often mean an upstream data problem.
* Alert thresholds are agreed with owners; every alert has a runbook entry.

## 7. Retraining

* Triggers: a schedule matched to how fast the world changes (weekly, monthly), significant drift, or a measured performance drop.
* Always compare the retrained model with the current one on the **same recent window** before promoting; retraining can make things worse (bad new data, label delays).
* Guard against **feedback loops**: when the model's actions shape future labels (blocked transactions never get labels), keep a random holdout or exploration traffic.
* Keep training data windows deliberate (all history versus recent window versus weighted) and documented.

## 8. Operations

* Owners, on-call, and a runbook: how to roll back, how to disable the model and fall back to rules, whom to call about upstream data.
* Cost tracking: training compute, serving infrastructure, and labeling.
* Documentation stays current: model card, `ML_DESIGN.md`, and the readiness review (`references/ML_READINESS.template.md`).
* Decommission models that no longer earn their keep.
