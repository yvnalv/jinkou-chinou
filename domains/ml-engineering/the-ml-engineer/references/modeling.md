# Modeling

Choosing, training, and tuning models for each problem type, with reproducible experiments. Library capabilities change; check current documentation before relying on version-specific features (facts here verified 2026-09-11).

## Contents

1. The model ladder
2. Tabular classification and regression
3. Time series forecasting
4. Deep learning for text and images
5. Recommendation and ranking
6. Anomaly detection
7. Imbalanced data
8. Hyperparameter tuning
9. Experiment tracking and reproducibility

---

## 1. The model ladder

Climb only when the eval shows the rung below is not enough:

```text
baseline (rule, prior, naive) → linear / logistic → gradient-boosted trees → deep learning or foundation models
```

* Every candidate is compared with the baselines under the **same split and metric**.
* Complexity costs: training and serving infrastructure, latency, explainability, maintenance, and failure modes. Prefer the simplest model within the noise of the best one.
* Tune baselines reasonably too; beating an untuned baseline proves little.

## 2. Tabular classification and regression

* **Gradient-boosted trees** (LightGBM, XGBoost, CatBoost, scikit-learn's HistGradientBoosting) are the default for medium to large tabular data: strong accuracy, native missing-value and categorical handling, fast training and microsecond inference, no GPU.
* **Linear and logistic models** are strong baselines, easy to explain and calibrate, and sometimes win on small or very noisy data (keep them in the comparison).
* **Tabular foundation models** (for example TabPFN-2.5 and TabICLv2) now outperform tuned boosting on **small datasets (roughly under 10,000 rows)** without tuning, at the cost of GPU inference and row limits. Try them for small-data problems; check licence and deployment constraints.
* Deep tabular networks rarely beat boosting on typical business data; use them when you need end-to-end learning with text or image inputs, or very large data with rich interactions.
* Use monotonic constraints where domain logic demands them (price up → demand not up), and early stopping on a validation fold.

## 3. Time series forecasting

* **Validate with rolling-origin (backtesting) evaluation:** several forecast origins, fixed horizon, no future data in features. Report error per horizon step.
* **Baselines first:** naive, seasonal naive, and simple exponential smoothing; they are hard to beat on short or noisy series.
* **Statistical models** (ETS, ARIMA, Theta; for example via statsforecast) per series; **global ML models** (boosting on lag, calendar, and covariate features) across many series; **deep models** (N-BEATS/N-HiTS, TFT) for large related collections.
* **Time series foundation models** (for example Chronos-2 and TimesFM-2.5) give strong zero-shot forecasts, including covariates in newer versions; benchmark them against tuned statistical baselines on your data, because classical methods remain competitive on some frequencies.
* Metrics: MAE and RMSE per series scale, scaled errors (MASE) or relative MAE versus seasonal naive to compare across series, and pinball loss / coverage for **probabilistic forecasts** (quantiles), which most planning decisions need.
* Handle hierarchies (store → region → total) with reconciliation when decisions happen at several levels.

## 4. Deep learning for text and images

* **Start from pretrained models** (transfer learning): fine-tune a pretrained transformer for text or a pretrained CNN/ViT backbone for images; training from scratch is rarely justified.
* Compare with cheaper options: embeddings plus a linear or boosting classifier; for text, a prompted foundation model (zero- or few-shot) may be enough, and a fine-tuned small model often wins on cost and latency at volume.
* PyTorch is the default framework; use the ecosystem's trainers (Hugging Face Transformers, timm, PyTorch Lightning) rather than hand-written loops when they fit.
* Training hygiene: fixed seeds, validation-based early stopping, learning-rate schedules, mixed precision on GPU, augmentation on training data only, and checkpointing.
* Check label noise and class balance first; data quality usually matters more than architecture.

## 5. Recommendation and ranking

* **Multi-stage architecture:** candidate retrieval (popularity, co-occurrence, two-tower embedding models with approximate nearest-neighbor search) → ranking model (gradient boosting or a neural ranker on user, item, and context features) → re-ranking for business rules, diversity, and freshness.
* **Implicit feedback** (clicks, views, purchases) is biased by what was shown; account for position and exposure bias, and include negatives sensibly.
* **Offline metrics:** recall@k for retrieval; NDCG@k, MAP, MRR for ranking; plus coverage, novelty, and diversity. Use **time-based splits** (train on the past, evaluate on the next period's interactions).
* Offline gains don't always transfer; confirm with an **online A/B test** on the business metric.
* Cold start: content features and popularity fallbacks for new users and items.

## 6. Anomaly detection

* Clarify the goal: known fraud patterns with labels (then it's supervised classification, usually better) versus unknown anomalies without labels.
* Unsupervised methods: robust statistics (median and MAD, seasonal decomposition residuals) for single metrics; Isolation Forest, local outlier factor, or autoencoders for multivariate data (libraries such as PyOD collect many).
* Thresholds come from the **alert budget** (how many alerts people can review) and the cost of misses, not from a default score cutoff.
* Evaluate with whatever labels exist (confirmed incidents, analyst feedback) using precision at the alert budget; build a feedback loop so reviewed alerts become labels.

## 7. Imbalanced data

* Use metrics that reflect the minority class: PR AUC, recall at a fixed precision or alert rate, cost-weighted metrics. Accuracy is misleading.
* Prefer **class weights** or proper thresholding over resampling; if resampling, do it inside the training folds only, never on validation or test data.
* Calibrate probabilities after any reweighting or resampling if scores will be used as probabilities.
* Choose the operating threshold on validation data from the cost of errors (`scripts/model_report.py --cost-fp --cost-fn`).

## 8. Hyperparameter tuning

* Tune **after** the data, features, and split are right; tuning rarely fixes bad data.
* Use random search or Bayesian optimization (for example Optuna) with a fixed budget, inside cross-validation on the training data only (nested CV for small data).
* Tune the few parameters that matter (for boosting: learning rate with early stopping, tree depth or leaves, minimum samples per leaf, regularization, subsampling).
* Report the CV spread; a gain smaller than the fold-to-fold standard deviation is noise.

## 9. Experiment tracking and reproducibility

* Track every run: code version (git commit), data version or hash, parameters, metrics per fold, environment, and artifacts. **MLflow** is the default when the project has nothing; MLflow 3 treats models as first-class logged models with lineage to runs, data, and evaluations.
* Fix random seeds, pin dependency versions (lock files), and record hardware for deep learning.
* Keep an experiment log in plain language: hypothesis, change, result, decision. It prevents repeating failed ideas.
* `assets/train_pipeline.template.py` implements locked test set, correct CV scheme, baselines, metadata, and optional MLflow logging.
