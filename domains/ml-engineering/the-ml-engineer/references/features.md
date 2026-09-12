# Preprocessing and Feature Engineering

Turning raw data into model inputs that are correct at prediction time, identical in training and serving, and actually useful.

## Contents

1. Pipelines and train-serving parity
2. Preprocessing by type
3. Feature engineering patterns
4. Time series features
5. Text, images, and embeddings
6. Feature selection
7. Feature stores

---

## 1. Pipelines and train-serving parity

* Put every fitted transformation (imputation, encoding, scaling, target encoding) in a **pipeline object** (scikit-learn `Pipeline` / `ColumnTransformer`, or the framework's equivalent) that is fitted on the training fold only and saved with the model.
* Use **one feature-engineering function** for training and serving (`assets/serve_api.template.py` imports it from the training module). Re-implementing features in another language or service is the classic source of **train-serving skew**.
* Log serving inputs and compare them with training data (`scripts/drift_report.py --columns <features>`).
* Make feature code deterministic and point-in-time correct (no "current" lookups when building historical rows).

## 2. Preprocessing by type

| Data | Default | Notes |
|---|---|---|
| Numeric, missing values | Median imputation plus a missing-indicator column | Tree boosting models handle missing values natively; don't impute for them unless needed |
| Numeric, scale | Standardize for linear models, neural networks, distance-based models | Trees don't need scaling |
| Numeric, skewed | Log or Box-Cox / Yeo-Johnson for linear models | Keep the raw value for trees |
| Numeric, outliers | Investigate first; cap (winsorize) only with a reason | Never drop outliers from the test set to look better |
| Categorical, low cardinality | One-hot (linear), native categorical support (boosting) | `handle_unknown` for unseen categories at serving time |
| Categorical, high cardinality | Target encoding **computed out-of-fold**, frequency encoding, hashing, or learned embeddings | In-fold target encoding leaks the label |
| Booleans stored as text | Map explicitly (yes/no, Y/N, 1/0) | Check for mixed representations |
| Dates | Extract parts (day of week, month, hour, holiday flags), elapsed time since events | Never feed raw timestamps that encode row order |
| IDs | Drop as features | Use them for grouping and joins only |

## 3. Feature engineering patterns

* **Aggregates over windows** relative to prediction time: counts, sums, averages, recency, and trends over the last 7, 30, 90 days (for example "tickets in the last 30 days", "days since last login").
* **Ratios and interactions** with domain meaning (spend per visit, utilization = balance / limit).
* **Behavioral change:** current window versus a previous window (a drop in activity often predicts churn).
* **Entity context:** statistics of the group an entity belongs to (store-level averages), computed without the target row.
* **Domain rules as features:** existing business rules and heuristic scores are strong inputs and good baselines.

Always check: is this feature computable at prediction time in production, from the same source, with the same delay?

## 4. Time series features

* Lags (y at t−1, t−7, t−364), rolling statistics over past windows only (shift before rolling), calendar features, holidays and events (including local holidays), promotions, and price.
* For global models across many series, include series identifiers or static attributes and scale per series.
* Features must respect the **forecast horizon**: to forecast 14 days ahead, only lags of 14 days or more are available at forecast time (or use recursive / direct multi-horizon strategies deliberately).

## 5. Text, images, and embeddings

* **Pretrained embeddings** (from text or image foundation models) as features are a strong, cheap baseline for tabular models that include text or images.
* For text: normalize consistently; for classic models, TF-IDF with n-grams remains a solid baseline.
* For images: resize and normalize as the pretrained backbone expects; augment only the training data.
* Record the embedding model and version; changing it changes every feature.

## 6. Feature selection

* Prefer domain reasoning and ablation (does removing a group of features hurt the CV score?) over automated selection on the full dataset.
* Any automated selection runs **inside** the CV loop.
* Remove features that are unavailable, unstable, or legally sensitive at serving time even if they help offline.
* Permutation importance on validation data (not impurity-based importance) and SHAP values help explain which features matter; they are not causal.

## 7. Feature stores

Consider a feature store (for example Feast, or a platform's built-in store) when several models share features, when you need point-in-time correct training sets and low-latency online serving of the same features, or when feature computation is expensive. For one model with batch scoring, a well-tested feature module and versioned tables are enough.
