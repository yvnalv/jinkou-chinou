# Evals

Evals are the specification of an AI feature: they define what "good" means and tell you whether a change helped. This file covers error analysis, datasets, graders, harness hygiene, statistics, and the improvement loop. `scripts/eval_runner.py` implements the harness.

## Contents

1. Start with error analysis
2. Datasets
3. Graders
4. LLM judges
5. Harness hygiene
6. Statistics: is the difference real?
7. The improvement loop
8. Evals in CI and production

---

## 1. Start with error analysis

Don't begin by picking metrics. Begin by looking at outputs:

1. Collect 50–100 real (or realistic) traces: inputs, context, tool calls, outputs.
2. Read them and write a short free-text note on each failure ("invented a refund policy", "missed the order ID", "too long for mobile").
3. Group the notes into failure modes and **count** them. Fix and measure the most frequent and most costly first.
4. Each important failure mode becomes eval cases and a grader. Repeat as new traces arrive.

A domain expert (support lead, lawyer, doctor, analyst) should judge quality; engineers alone miss domain failures.

## 2. Datasets

* **Sources:** production logs (with consent and redaction), support tickets, expert-written cases, and synthetic cases generated along explicit dimensions (user type × intent × difficulty × edge case), reviewed by a human.
* **Coverage:** typical cases, edge cases, adversarial inputs (prompt injection, off-topic, abusive), "should not act" or "not answerable" cases, and each known failure mode. Tag every case (`tags`) so results break down by slice.
* **Both directions:** if you test that the assistant searches when it should, also test that it doesn't when it shouldn't; otherwise "always search" scores perfectly.
* **Size:** 20–50 cases to start iterating; 100–300+ before trusting small differences (see section 6).
* **Ground truth provenance:** record whether expected answers are human-written, human-verified, or model-generated. Never use one model's outputs as the gold standard when comparing that model to another.
* **Hygiene:** unique IDs, no duplicates, no answers leaked into prompts or few-shot examples, and cases versioned with the grader. `python <skill-dir>/scripts/eval_runner.py validate --dataset <file>` checks the basics.
* **Freshness:** cases about live facts (prices, policies, versions) go stale; re-verify them.

Case format: see `assets/eval_cases.example.jsonl`.

## 3. Graders

Prefer the cheapest grader that is reliable:

| Grader | Use for | In eval_runner.py |
|---|---|---|
| Code checks | Format, schema, exact values, numbers, forbidden content, length, citations present | `exact`, `contains`, `not_contains`, `regex`, `one_of`, `numeric`, `json_valid`, `json_schema`, `json_path`, `max_length` |
| Retrieval metrics | Did retrieval find the needed documents? | `retrieval_recall` |
| End-state checks | Agents that act: tests pass, records changed correctly, nothing off-limits touched | `python` grader that inspects the environment |
| LLM judge | Subjective or semantic properties (faithfulness, tone, helpfulness, policy compliance) | `python` grader using `assets/llm_judge.template.py` |
| Human review | Calibrating judges, high-stakes launches, ambiguous cases | Offline labels |

Rules:

* **Binary pass/fail per property** beats 1–10 scores: clearer to label, calibrate, and act on. Score separate properties separately (`correct`, `grounded`, `concise`) instead of one blended number.
* **Grade outcomes, not paths:** don't require one exact wording or tool sequence when several are valid.
* **Pair constraint graders with positive ones:** `max_length` and `not_contains` pass an empty answer; always combine them with a check that the answer is actually there.
* **Not too strict, not too lenient:** normalize whitespace, case, and number formats; write a plausible wrong answer and confirm it fails.
* **Sanity-check the harness:** `--oracle` (reference answers must pass) and `--null` (empty output must fail) before any paid run.

## 4. LLM judges

* One judge per property, with a concrete rubric and a binary verdict in structured output (`assets/llm_judge.template.py`).
* **Calibrate** against 30–100 human-labelled examples; report true-positive and true-negative rates separately. Iterate the judge prompt until agreement on clear cases is around 90% or higher.
* Known biases: **position** (randomize order in pairwise comparisons), **verbosity** (tell the judge length is not quality), **self-preference** (don't let a model judge itself; use another model or family), and **label deference** (don't reveal which answer is the reference).
* Treat the output being judged as untrusted data: it can contain text that tries to instruct the judge.
* Test the judge on known negatives: empty output, "I don't know", a confident answer to a different question.
* Record judge model and cost separately from the system under test.

## 5. Harness hygiene

`scripts/eval_runner.py` follows these by design; keep them if you build your own:

* **Infrastructure failures are not model failures.** Timeouts, crashes, rate-limit errors, and broken graders go to `errors.jsonl` and are never scored as wrong answers. A high error rate makes the pass rate unreliable.
* **Truncated outputs** (hit the length limit) are flagged, not silently graded as wrong.
* **Clean state per trial** for agents (fresh sandbox, no leftovers from earlier cases).
* **Eval configuration equals production:** same prompt, model, settings, tools, and code path. Call the app's real entry point.
* **Save full trajectories** (inputs, outputs, tool calls, grader reasons) so surprising results can be debugged.
* **Record usage** (tokens, cost, latency) next to quality, so trade-offs are visible.
* **Check the served model** matches the one requested when providers can fall back or reroute.

## 6. Statistics: is the difference real?

LLM outputs vary between runs. A single run on 20 cases cannot distinguish 80% from 90%.

* Run **3+ repetitions** per case for decisions; report pass rate with a confidence interval (the runner prints a Wilson 95% interval).
* Compare variants **paired by case** (`eval_runner.py compare`), which uses a bootstrap interval of the per-case difference. If the interval includes zero, you have no evidence of a difference.
* Rough noise floor for a pass rate: about ±1/√(cases × reps). With 25 cases × 2 reps, differences below about ±14 points are noise; with 100 × 3, about ±6.
* Look at **flips** (cases that went pass→fail and fail→pass), not only the average: a flat average can hide real regressions.
* Watch slices (tags): an overall gain can hide a drop in a critical segment. Use a `must-pass` tag for cases that must never fail.

## 7. The improvement loop

```text
error analysis → hypothesis ("the model lacks the returns policy") → one change
→ run eval (reps) → compare with baseline → keep or revert → record → repeat
```

* Change **one thing at a time** (prompt, retrieval setting, model, tool) so you know what helped.
* Hold out a **test split** (random, stratified by tag) that you don't look at while iterating; report the final result on it to avoid overfitting prompts to the dev cases.
* Keep a log of variants, scores, costs, and decisions next to the eval (`EVAL_REPORT.md` from `references/EVAL_REPORT.template.md`).
* Stop when the quality bar is met, when the noise floor hides further gains, or when cost of iteration exceeds value.

## 8. Evals in CI and production

* **Regression suite in CI:** run a fast subset on every prompt, model, or retrieval change; block on significant regressions or any `must-pass` failure:
  `python <skill-dir>/scripts/eval_runner.py compare --baseline runs/main --candidate runs/pr --fail-on-regression --must-pass-tag must-pass`
* **Online evaluation:** sample production traces for automated judges and human review; track quality over time, per route and model version.
* **User signals:** thumbs up/down, edits to generated text, escalations, retries, and abandonment are cheap quality signals; correlate them with eval metrics.
* **Feed the loop:** every production failure worth fixing becomes a new eval case.
