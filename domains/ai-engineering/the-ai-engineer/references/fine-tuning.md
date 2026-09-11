# Fine-Tuning and Distillation (light ML)

When adapting model weights is worth it, how to do it without fooling yourself, and how to serve the result. Classic predictive modeling on tabular data belongs to data science, not here.

## Contents

1. When (and when not)
2. Methods
3. Data
4. Evaluation
5. Hosted versus self-hosted
6. Serving open-weights models
7. Checklist

---

## 1. When (and when not)

Follow the ladder: **prompt → retrieval → fine-tune → distill**. Fine-tuning is for **form, not facts**.

| Good reasons | Bad reasons |
|---|---|
| A consistent output format, style, tone, or schema that prompting can't hold reliably | Teaching facts that change (use retrieval) |
| Distilling a large model's behavior on a narrow task into a smaller, cheaper, faster model | "The prompt is long" (try caching and trimming first) |
| Domain language or classification behavior with many labelled examples | No eval exists yet (you won't know if it helped) |
| Latency or cost targets a hosted frontier model can't meet at the required volume | Hoping to fix bad retrieval or bad data |
| Running on-device or fully on-premises for data or connectivity reasons | Chasing a leaderboard number |

Before fine-tuning, have: a working prompt-based baseline, an eval showing where it falls short, and enough good examples of the desired behavior.

## 2. Methods

| Method | What it does | Typical use |
|---|---|---|
| Supervised fine-tuning (SFT) | Learn from input → ideal-output pairs | Format, style, task behavior |
| Parameter-efficient fine-tuning (LoRA, QLoRA) | Train small adapter weights on a frozen base model | The practical default for open-weights models; cheap to train, swap, and store |
| Preference optimization (DPO and related methods) | Learn from pairs of preferred versus rejected outputs | Tone, helpfulness, safety behaviors that are easier to compare than to write |
| Reinforcement fine-tuning with graders | Optimize against a programmatic or model-based reward | Tasks with checkable answers (math, code, extraction); offered by some hosted providers |
| Distillation | Generate training data with a strong model, verify it, train a smaller model | Cost and latency reduction on a narrow, stable task |

Check which methods your provider or framework supports today; offerings change often.

## 3. Data

* **Quality over quantity:** hundreds to a few thousand excellent, diverse examples usually beat large noisy sets.
* Make examples look exactly like production inputs (same prompt template, same context format).
* Cover edge cases, refusals, and "not enough information" behavior, or the tuned model will lose them.
* Deduplicate; remove personal data unless you have a lawful basis; check licences of any source data, including model-generated data (some provider terms restrict using outputs to train competing models).
* **Hold out an eval set** that never enters training, split by topic or time where leakage is possible.
* For distillation, verify teacher outputs (code checks, judges, human spot checks) before training on them.

## 4. Evaluation

* Compare the tuned model against the **prompt-only baseline** on the same held-out eval with repetitions (`scripts/eval_runner.py compare`).
* Check for **regressions** outside the target task: general instruction following, safety and refusal behavior, other languages.
* Watch for overfitting: training loss falling while held-out quality stalls or drops.
* Record the base model version, data version, hyperparameters, and eval results for every trained artifact.

## 5. Hosted versus self-hosted

| Hosted fine-tuning (provider API) | Self-hosted (open weights) |
|---|---|
| Little infrastructure; provider-managed serving | Full control over data, weights, and deployment |
| Limited to the provider's supported models and methods | Any open model; any method |
| Data goes to the provider (check terms) | Needs GPUs, MLOps, security patching, and on-call |
| Tuned model tied to the provider and base-model lifecycle | Licence terms of the base model apply (commercial use, attribution, acceptable-use rules) |

## 6. Serving open-weights models

* Use a dedicated inference server (for example vLLM, SGLang, TGI, llama.cpp, or a managed endpoint) rather than a naive loop; they provide batching, paged attention, streaming, and OpenAI-style or provider-style APIs.
* Choose quantization (8-bit, 4-bit) by measuring quality loss on the eval, not by default.
* Capacity-plan for peak concurrency and context length; measure time to first token and tokens per second under load.
* Apply the same guardrails, tracing, and eval gates as for hosted models (`references/production.md`).

## 7. Checklist

- [ ] A prompt-only (and retrieval) baseline was measured, and the gap is documented.
- [ ] Training and eval data are clean, representative, licensed, and separated.
- [ ] The tuned model beats the baseline on the held-out eval by more than the noise floor, with no safety or general-capability regressions.
- [ ] Artifacts are versioned with base model, data, and settings; rollback to the baseline is possible.
- [ ] Serving, monitoring, and a retraining trigger (data drift, base-model deprecation) are planned.
