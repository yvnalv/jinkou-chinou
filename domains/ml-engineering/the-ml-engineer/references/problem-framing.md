# Problem Framing

Turning a business need into a well-posed ML problem, or deciding that ML is the wrong tool. The output is `ML_DESIGN.md` from `references/ML_DESIGN.template.md`.

## Contents

1. Is ML the right tool?
2. From decision to prediction
3. Label and prediction time
4. Metrics: business, model, guardrail
5. Baselines
6. Feasibility and costs
7. Framing questions

---

## 1. Is ML the right tool?

Use ML when all of these hold:

* There is a **repeated decision** that a prediction would improve (not a one-off analysis).
* The pattern is **too complex for rules** a person could write, or rules exist but are costly to maintain.
* **Historical examples with outcomes** exist or can be collected, and they reflect the future.
* **Errors are tolerable** or can be caught (human review, thresholds, fallbacks).
* The value of better decisions **exceeds** the cost of building, serving, and maintaining a model.

Otherwise prefer rules, heuristics, SQL, a lookup table, optimization, or a one-off statistical analysis. For language-heavy tasks (text understanding, generation, extraction), compare with foundation-model approaches (an AI-engineering skill such as the-ai-engineer covers those).

## 2. From decision to prediction

Write the chain explicitly:

```text
Decision:   Which customers get a retention offer this week?
Action:     Send an offer to the top N by predicted risk × expected value
Prediction: P(customer cancels within the next 30 days | data known today)
Unit:       One row per active customer per weekly scoring date
Task type:  Binary classification (ranked), with calibrated probabilities
```

Common task types: binary or multiclass classification, regression, ranking or recommendation, time series forecasting, anomaly detection, clustering or segmentation (usually exploratory), and uplift modeling (when the decision is whom to *treat*, predict the treatment effect, not the outcome).

## 3. Label and prediction time

Most serious ML bugs come from getting time wrong.

* **Prediction time (t₀):** the moment the model is called in production. Every feature must be computable from data available **before t₀**, as it existed then (point-in-time correctness).
* **Label window:** the outcome period after t₀ (for example "cancels in the next 30 days"). Rows whose window has not finished cannot be labelled yet.
* **Label definition:** precise and agreed with the business ("cancellation = account closed or no payment for 45 days"). Ambiguous labels cap achievable quality.
* **Feedback loops:** once the model drives actions (offers, fraud blocks), future labels are affected by its own decisions; plan for holdout groups or exploration.

## 4. Metrics: business, model, guardrail

| Level | Example | Role |
|---|---|---|
| Business | Retained revenue, fraud losses, forecast-driven stockouts | What success means; measured online or in an A/B test |
| Model (offline) | PR AUC, recall at 5% alert rate, MAE, NDCG@10 | Chosen so improvements move the business metric |
| Guardrail | Complaint rate, false-positive rate per segment, latency, fairness gaps | Must not get worse |

Pick one **primary offline metric** that matches the decision (for a top-N offer, precision or value at N beats overall accuracy), plus secondary and guardrail metrics. Define the **acceptance bar** before training.

## 5. Baselines

Always measure simple baselines first; they set the bar and catch pipeline bugs:

| Task | Baselines |
|---|---|
| Classification | Majority class or prior; a business rule already in use; logistic regression |
| Regression | Mean or median; last value; linear model |
| Forecasting | Naive (last value), seasonal naive (same period last cycle), moving average |
| Recommendation | Most popular items (overall or per segment); recently viewed |
| Anomaly detection | Simple thresholds or z-scores on key metrics |

A complex model that barely beats a good baseline is usually not worth its maintenance cost.

## 6. Feasibility and costs

* **Data:** enough labelled examples (especially of the rare class), coverage of the segments that matter, and history for the patterns (seasonality needs several cycles).
* **Signal:** a quick model on available features. If a strong model can't beat the baseline, more tuning rarely helps; better data or features might.
* **Cost of errors:** false positives versus false negatives in money or harm; this sets thresholds and the need for review.
* **Operational constraints:** batch or real-time, latency budget, where features come from at serving time, retraining cadence, and who owns the model.
* **Risk and regulation:** decisions about people (credit, hiring, insurance, health) carry fairness, explainability, and legal duties (`references/responsible-ml.md`).

## 7. Framing questions

Ask in rounds of three to five, highest impact first:

1. What decision will the prediction change, who acts on it, and how often?
2. What exactly is the outcome (label), and when is it known?
3. When is the model called, and what data exists at that moment?
4. What do errors cost, in which direction?
5. What is done today (the baseline), and how good is it?
6. How much labelled history is there, and does the past represent the future?
7. Batch or real-time? Latency and volume?
8. Are there constraints on data use, explainability, or fairness?
