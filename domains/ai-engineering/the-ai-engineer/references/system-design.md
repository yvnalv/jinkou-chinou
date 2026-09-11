# AI System Design

How to decide whether and how to build an AI feature: feasibility, the approach ladder, architecture patterns, model selection, budgets, and data. The output is `AI_DESIGN.md` from `references/AI_DESIGN.template.md`.

## Contents

1. Feasibility
2. The approach ladder
3. Workflow and agent patterns
4. Model selection
5. Cost and latency budgets
6. Data, privacy, and compliance inputs
7. Failure design
8. Provider neutrality without over-abstraction

---

## 1. Feasibility

Answer these before choosing any technology:

| Question | Why it matters |
|---|---|
| What exact task, for whom, with what inputs and outputs? | Vague tasks produce vague systems and unmeasurable quality |
| What does a correct output look like, and who can judge it? | No success definition means no eval, which means no way to ship safely |
| What does a wrong output cost (annoyance, money, safety, legal)? | Sets the quality bar, the need for human review, and the guardrails |
| Is a non-AI solution good enough (rules, search, a form, a template)? | Deterministic code is cheaper, faster, and testable; use AI where language or judgment is really needed |
| Is there data to ground answers, and can the system access it with the right permissions? | Most enterprise failures are missing or stale context, not model weakness |
| Volume, latency, and budget per request? | Rules out designs early (an agent loop cannot answer in 300ms) |
| Where can data go (retention, residency, confidentiality, licences)? | Rules out providers or deployment models |

Build a small **prototype on 10–20 real examples** before committing to an architecture. It reveals feasibility faster than any document.

## 2. The approach ladder

Start at the lowest rung that could work and move up only when an eval shows the current rung falls short (the Approach Gate):

| Rung | Use when | Typical cost of adoption |
|---|---|---|
| 1. Single call with a good prompt | Classification, extraction, rewriting, summarization, Q&A over provided text | Lowest; easy to evaluate |
| 2. Structured output / tool call | The result feeds code: JSON with a schema, function arguments | Low; use the provider's schema-constrained mode |
| 3. Workflow (code-orchestrated steps) | The task decomposes into known steps (see section 3) | Moderate; each step testable |
| 4. Retrieval (RAG) | Answers depend on private, large, or changing knowledge | Moderate to high; needs an ingestion pipeline and retrieval evals (`references/rag.md`) |
| 5. Agent (model-directed tool loop) | Open-ended, multi-step tasks whose steps cannot be fixed in advance | High: cost, latency, unpredictability, security surface (`references/agents-and-tools.md`) |
| 6. Fine-tuning or distillation | Prompting and retrieval are at their ceiling on form, cost, or latency | High: data, training, and maintenance (`references/fine-tuning.md`) |

Rungs combine (a workflow with a retrieval step and one structured-output call), but each addition must earn its place. Long context windows often make "put the whole document in the prompt" a valid alternative to rung 4 for small, stable corpora.

## 3. Workflow and agent patterns

Workflows keep control in code; agents give control to the model. Prefer workflows whenever the path is predictable.

| Pattern | Shape | Use when |
|---|---|---|
| Prompt chaining | Step A → check → step B | Fixed subtasks; add programmatic checks between steps |
| Routing | Classify, then send to a specialized prompt or model | Distinct input types need different handling or cost tiers |
| Parallelization | Split into independent parts, or run several attempts and vote | Independent subtasks; confidence through agreement |
| Orchestrator–workers | A model plans subtasks at runtime; workers execute | Subtasks cannot be known in advance (for example, which files to change) |
| Evaluator–optimizer | Generate → critique against criteria → revise | Clear criteria and measurable improvement from iteration |
| Autonomous agent | Loop: model chooses a tool, observes, repeats until done | Open-ended tasks with an environment that gives real feedback (tests, searches, APIs) |

Build an agent only if **all four** hold: the task is complex and hard to specify step by step; its value justifies higher cost and latency; models are demonstrably capable at it (prototype first); and errors can be caught and recovered (tests, review, rollback, human approval).

## 4. Model selection

Choose models with an eval, not by reputation or leaderboard rank.

1. **Shortlist** by hard constraints: modalities (text, images, audio, PDFs), context window, output length, tool calling and structured-output support, languages, data residency and retention terms, deployment (hosted API, cloud marketplace, self-hosted open weights), and licence for open-weights models.
2. **Check current facts in the provider's documentation or models API** at design time: model names, context limits, prices, rate limits, and deprecation dates change often. Never hard-code them from memory; record the date you checked.
3. **Run the same eval** on the shortlist with production-like prompts and settings. Compare quality, cost per completed task, and latency (p50 and p95) together.
4. **Prefer the simplest configuration that meets the bar.** Try the strongest model with lower reasoning effort (where the provider offers such a setting) before building a multi-model cascade; one model means simpler caching, fewer failure modes, and easier maintenance.
5. **Reasoning ("thinking") models** help with multi-step logic, coding, and agentic work, and add latency and cost; test whether a routine route really benefits.
6. **Plan for change:** keep model names in configuration, pin versions where the provider offers snapshots, subscribe to deprecation notices, and keep the eval runnable so a migration is a measured change.

## 5. Cost and latency budgets

Estimate before building, then measure (`scripts/usage_report.py`):

```text
cost per task = Σ over calls ( uncached_input × input_price + cached_input × cache_price
                               + output × output_price )
calls per task = 1 for a single call; N for a workflow; variable (cap it) for an agent
```

* Output tokens usually cost several times more than input tokens, and dominate latency.
* Agents multiply cost by the number of turns and re-send growing context each turn; cap steps and budgets.
* **Latency levers:** smaller or faster model on a route that tolerates it, lower reasoning effort, shorter outputs, streaming for perceived speed, parallel calls, caching of stable prefixes, and precomputation (batch jobs for anything not interactive).
* Judge cost **per completed task**: a cheaper call that needs retries or extra turns is not cheaper.

## 6. Data, privacy, and compliance inputs

* Classify the data the system will see (public, internal, confidential, personal, special categories) and decide what may be sent to which provider.
* Check the provider's data retention, training-use, and residency terms, and whether zero-retention or regional processing is available and required.
* Minimize: send only the fields the task needs; redact identifiers where possible.
* Permissions: retrieval and tools must enforce the **end user's** access rights, not the service account's.
* Regulatory triggers (for example transparency duties for AI-generated content or chatbots, high-risk uses such as hiring or credit) are in `references/security-and-safety.md` section 7.

## 7. Failure design

Design what happens when the model is wrong, slow, down, or refuses:

| Failure | Design response |
|---|---|
| Wrong or low-confidence output | Validation (schema, rules), grounding checks, a "not sure" path, human review for high-stakes outputs |
| Refusal or safety block | Detect it explicitly; show a helpful message; don't retry blindly |
| Timeout, rate limit, provider outage | Timeouts, retries with jittered backoff, fallback model or provider, graceful degradation (cached answer, non-AI path) |
| Truncated output (length limit) | Detect the stop reason; raise the limit or continue; never parse truncated JSON as complete |
| Cost runaway (agent loops) | Step, token, and money caps; alerts |

## 8. Provider neutrality without over-abstraction

* Use each provider's **official SDK** directly by default; SDKs handle retries, streaming, types, and new features.
* Add a **thin adapter** (one module with `generate()`, `stream()`, `embed()`) only when the product really needs to switch or mix providers. Keep provider-specific features (caching controls, reasoning settings, server-side tools) reachable, not hidden behind the lowest common denominator.
* Follow the framework the project already uses (LangChain, LlamaIndex, Vercel AI SDK, and others); don't introduce a framework for a single call.
* Keep prompts, tool schemas, and eval datasets provider-neutral so they move with you.
