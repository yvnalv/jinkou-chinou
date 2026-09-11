# AI Feature Review — <feature name>

| | |
|---|---|
| Scope | <feature, routes, agents, code paths reviewed> |
| Standards | OWASP LLM Top 10 (2025), OWASP Agentic Top 10 (2026), `production.md` readiness checklist, <regulations in scope> |
| Inputs | <code, prompts, tool definitions, traces, eval results, usage logs> |
| Date | <date> |

## 1. Summary

<Overall state, the biggest risks, and the most valuable fixes.>

| Severity | Count |
|---|---|
| Critical | <n> |
| High | <n> |
| Medium | <n> |
| Low | <n> |

## 2. Architecture as Reviewed

<Short description or diagram: models, prompts, retrieval, tools, permissions, data flows, external channels.>

Lethal trifecta: private data <yes/no> · untrusted content <yes/no> · external channel <yes/no> → <safe / gated by … / exposed>.

## 3. Findings

| ID | Severity | Area | Reference | Location | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|---|---|
| REV-001 | <Critical> | <security / quality / reliability / cost / compliance> | <LLM01, ASI02, readiness item> | <file:line, route, tool> | <what is wrong> | <trace id, test, measurement> | <specific fix> |

## 4. Quality and Evals

<Does an eval exist, is it sound (oracle/null, reps, CI), what does it show, what is missing?>

## 5. Cost and Performance

<From usage_report.py: cost per task, cache hit rate, p95 latency, error rate; the top savings levers.>

## 6. Prioritized Plan

1. **Now:** <critical and high findings>
2. **Next:** <…>
3. **Later:** <…>

## 7. Not Verified

- <areas not reviewed, tests not possible, missing access>
