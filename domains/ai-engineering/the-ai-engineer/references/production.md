# Production: Reliability, Cost, Observability, Operations

Running AI features in production: handling failures, controlling cost and latency, tracing, rollouts, and model lifecycle.

## Contents

1. Reliability
2. Cost and latency optimization
3. Observability
4. Releases and model lifecycle
5. Monitoring quality in production
6. Production readiness checklist

---

## 1. Reliability

| Concern | Practice |
|---|---|
| Timeouts | Set explicit client timeouts; stream long generations so connections stay alive and users see progress |
| Retries | Retry rate limits (429), overload, 5xx, and connection errors with exponential backoff and jitter, capped attempts; don't retry invalid requests (4xx) or safety refusals |
| Idempotency | Make downstream side effects idempotent (idempotency keys), because retries and agent loops repeat calls |
| Fallbacks | A secondary model or provider for outages, tested with the same eval; graceful degradation (cached answer, simpler non-AI path, "try again later") |
| Stop reasons | Always inspect why generation stopped: normal end, length limit (truncated), tool call, refusal, content filter. Never treat a truncated or refused response as a normal answer |
| Validation | Schema-validate structured outputs; repair or retry once on invalid output, then fail safely |
| Rate limits and quotas | Queue and smooth traffic; per-user limits; request higher limits before launch |
| Circuit breakers | Stop calling a failing dependency for a while instead of piling on retries |
| Long-running work | Background jobs with persisted state, progress, and resumability instead of one long HTTP request |

Use the SDK's built-in retry and timeout settings where they exist rather than wrapping another retry layer around them (double retries multiply load).

## 2. Cost and latency optimization

Measure first (`python <skill-dir>/scripts/usage_report.py <logs> --prices <prices.json>`), then apply levers roughly in this order: free wins before quality trade-offs.

**Free or nearly free:**

1. **Prompt caching:** stable prefixes first (`references/prompting-and-context.md` section 7); confirm the cache hit rate rises.
2. **Input hygiene:** remove unused instructions, redundant examples, oversized retrieved context, and bloated tool results; scope tools per task.
3. **Output hygiene:** ask for the length and format you need; stop sequences; structured outputs instead of prose plus JSON.
4. **Batch APIs** for anything not interactive (evaluations, backfills, nightly jobs): providers commonly discount batch processing substantially in exchange for delayed results.
5. **Loop hygiene** for agents: fewer, better tools; code execution to filter large intermediate data; step caps.

**Trade-offs (verify with the eval):**

6. Lower reasoning effort or a smaller thinking budget on routes that don't need it.
7. A smaller or cheaper model on a specific route (classification, extraction), proven by the eval.
8. Routing or cascades (cheap model first, escalate on low confidence): more moving parts, split caches, and harder debugging; only when measurement shows a clear win over one well-tuned model.
9. Fine-tuning or distillation for high-volume, narrow tasks (`references/fine-tuning.md`).

Report cost **per completed task** and per user or tenant; set budgets and alerts.

Pricing reminder: providers price input, output, cached reads, cache writes, and batch differently, and **report cached tokens differently** (some include them in input tokens, some report them separately). Take prices and field semantics from the provider's current documentation.

## 3. Observability

Trace every model call, tool call, and retrieval step as spans in one trace per user request or agent task.

* Use **OpenTelemetry GenAI semantic conventions** where your stack supports them (attributes such as `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`). They are still in **Development** status (as of 2026), so names can change; pin the convention version and use the dual-emission opt-in when migrating.
* Record per call: model requested and served, prompt or template version, parameters, token usage including cached tokens, latency (time to first token and total), stop reason, errors, retries, tool calls with their results' size, and cost.
* **Content logging:** full prompts and outputs are invaluable for error analysis but may contain personal or confidential data. Redact, restrict access, sample, and apply retention limits; make content capture a configuration switch.
* Link traces to user feedback and to eval results so a bad answer can be traced to its exact configuration and context.
* Dashboards: volume, error rate, refusal rate, p50/p95 latency, cost per task, cache hit rate, tool error rates, and quality metrics from online evals, per route and model version.

## 4. Releases and model lifecycle

* **Configuration, not code:** model names, parameters, and prompt versions live in versioned configuration.
* **Gate every change** (prompt, model, retrieval setting, tool) on the eval, then roll out gradually: shadow traffic (new version runs silently alongside the old) → canary (small percentage) → full rollout, with fast rollback.
* **A/B tests** for product metrics when offline evals can't capture user value; decide the metric and duration before starting.
* **Model deprecations:** providers retire models on published schedules. Track notices, keep the eval runnable, and treat a model migration as a measured change (prompts often need re-tuning for new models).
* **Pin** SDK versions and model snapshots where available; test upgrades like any dependency.
* **Documentation:** keep `AI_DESIGN.md`, the eval report, and known limitations current for the team and for compliance.

## 5. Monitoring quality in production

* Sample traces daily or weekly for LLM-judge scoring and human review; compare against the offline eval to detect drift.
* Track implicit signals: regenerations, edits, copy events, escalations to humans, abandonment, complaints.
* Watch input drift: new topics, languages, document types, or user segments the eval doesn't cover.
* Alert on sudden changes in refusal rate, output length, tool error rate, or cost per task (often the first sign of a provider-side change or a prompt regression).
* Every confirmed production failure becomes an eval case.

## 6. Production readiness checklist

- [ ] Eval suite with a baseline, a regression gate in CI, and `must-pass` safety cases.
- [ ] Timeouts, retries with jitter, idempotent side effects, fallbacks, and stop-reason handling.
- [ ] Structured outputs validated; refusals and truncation handled explicitly.
- [ ] Rate limits, token and step caps, cost budgets, and alerts.
- [ ] Tracing with model, prompt version, tokens, latency, cost, and errors; content logging redacted and access-controlled.
- [ ] Security review done (`references/security-and-safety.md` section 8).
- [ ] Rollout plan with shadow or canary and rollback; model and prompt versions in configuration.
- [ ] Owners, runbook, and a plan for model deprecations.
- [ ] Transparency and user-facing disclosures in place where required.
