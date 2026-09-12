# Data: Collection, Labeling, Validation, Splits, Leakage, EDA

Getting trustworthy data into the pipeline and splitting it so evaluation reflects production.

## Contents

1. Data collection
2. Labeling
3. Data validation and contracts
4. Versioning and lineage
5. EDA for modeling
6. Splitting strategies
7. Leakage
8. Privacy

---

## 1. Data collection

* **Start from the prediction-time snapshot:** for each training row, reconstruct features exactly as they were at prediction time (point-in-time joins against event timestamps, slowly changing dimensions, feature-store time travel). Using today's value of a customer attribute for a row from last year leaks the future.
* **Sampling:** match the population the model will score. Beware survivorship (only customers who stayed), selection (only approved loans have repayment labels), and convenience samples.
* **Rare outcomes:** collect enough positives; consider targeted collection or longer history rather than synthetic oversampling.
* **Coverage:** all segments, regions, devices, languages, and seasons the model will see.
* **Document sources:** owner, refresh cadence, known issues, and consent or licence for use.

## 2. Labeling

* Write **annotation guidelines** with definitions, edge cases, and examples; pilot them and revise.
* Measure **agreement** between annotators (for example Cohen's or Krippendorff's kappa) on an overlap set; low agreement means the task or guideline is unclear, not that annotators are careless.
* **Gold questions** and spot checks to monitor quality; adjudicate disagreements.
* Cheaper labels: **weak supervision** (rules, heuristics, existing systems as noisy labellers), **active learning** (label the examples the model is least sure about), **model-assisted labeling** (a model or LLM pre-labels, humans correct). Always verify a sample by hand.
* Record label provenance (who or what labelled, when, with which guideline version).
* Delayed or censored labels (churn, fraud chargebacks, loan defaults) need a defined maturity window; don't label rows whose window is still open.

## 3. Data validation and contracts

Validate data at every boundary (ingestion, feature pipeline, training input, serving input):

| Check | Examples |
|---|---|
| Schema | Columns present, types, allowed categories |
| Completeness | Missing rates within expected bounds; row counts within expected range |
| Validity | Ranges (age 0–120), formats, referential integrity |
| Uniqueness | Keys unique at the stated grain |
| Freshness | Latest timestamp within the expected delay |
| Distribution | Drift versus a reference window (`scripts/drift_report.py`) |

Implement as code (pandera, Great Expectations, dbt tests, or plain assertions) that **fails the pipeline** on violation. Agree data contracts with upstream owners so schema changes are announced, not discovered.

For a first look at an unfamiliar dataset, a deep profiling pass (such as the exploratory-data-analysis skill) is a good start.

## 4. Versioning and lineage

* Version datasets (DVC, lakeFS, Delta or Iceberg time travel, or immutable dated snapshots) and record the version or hash with every trained model (`assets/train_pipeline.template.py` stores a data hash).
* Keep the code that produced each dataset; a model must be reproducible from code + data version + configuration + seed.

## 5. EDA for modeling

Beyond general data profiling, answer modeling questions:

- [ ] **Grain and keys:** one row per what? Duplicates? Repeated entities (customers, patients, devices)?
- [ ] **Target:** distribution, class balance, missing labels, how it changes over time and by segment.
- [ ] **Time:** coverage, seasonality, trend, structural breaks (policy changes, new products, tracking changes).
- [ ] **Feature availability:** for each feature, when is it known? Anything recorded after prediction time is a leak.
- [ ] **Signal:** univariate relationships with the target; suspiciously perfect predictors (`scripts/leakage_check.py`).
- [ ] **Missingness:** patterns, and whether "missing" itself predicts the target.
- [ ] **Train versus future:** does the most recent period look like the training period?

Do EDA on the training portion when possible, so decisions don't peek at the test set.

## 6. Splitting strategies

The split must mimic how the model will be used:

| Situation | Split | CV scheme |
|---|---|---|
| Independent rows, no time effect | Random (stratified for classification) | (Stratified) K-fold |
| Repeated entities (customers, patients, users, stores) | Group split: an entity is only in train or only in test | GroupKFold |
| Predicting the future (churn next month, demand, credit) | Out-of-time: train on the past, test on a later period | Forward-chaining (TimeSeriesSplit), with a gap equal to the label window |
| Both entity and time effects | Out-of-time and unseen entities (or the one that matches production) | Grouped forward-chaining |
| Tiny data | Repeated (stratified) K-fold with nested CV for tuning | — |

Rules:

* **Lock the test set** before modeling; use it once, at the end. Tune on validation folds only.
* Use a **gap** between train and test periods at least as long as the label window, so training labels don't overlap test features.
* Keep preprocessing inside the CV loop (fit on the training fold only) with pipelines.
* Report the split used; a random-split score for a temporal problem is not evidence the model works.

## 7. Leakage

Leakage makes validation scores look better than production performance. Common types (after Kapoor & Narayanan's taxonomy):

| Type | Example | Guard |
|---|---|---|
| No clean train/test separation | Preprocessing or feature selection fitted on all data; duplicates across splits | Pipelines fitted per fold; dedupe; `leakage_check.py` |
| Target leakage | A feature derived from the outcome or recorded after it ("account_closed_flag", "refund_issued") | Check feature timestamps against prediction time |
| Temporal leakage | Random split for a forecasting problem; future rows in training | Out-of-time split with a gap |
| Entity leakage | The same customer in train and test | Group split |
| Illegitimate features | Proxies not available in production (manual review outcome, IDs encoding time) | Feature availability review with domain experts |
| Test-set reuse | Tuning or selecting models on the test set | Locked test set; nested CV |
| Sampling bias | Test set drawn from a different population than production | Match production sampling |

Run `python <skill-dir>/scripts/leakage_check.py --train <train> --test <test> --target <y> [--id ..] [--time ..]` on every new dataset and split. It catches the mechanical cases; the availability-at-prediction-time review needs domain knowledge.

## 8. Privacy

* Collect and keep only the data the model needs; pseudonymize IDs; restrict access.
* Check the legal basis and consent for using personal data for model training, and retention limits.
* Watch for sensitive attributes and their proxies (postcode, name, language) even when you don't use them directly; you may still need them to *measure* fairness (`references/responsible-ml.md`).
* Never place raw personal data in notebooks, reports, or model artifacts shared beyond the need.
