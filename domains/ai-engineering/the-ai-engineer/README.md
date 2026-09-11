# the-ai-engineer

Provider-neutral AI engineering persona: design, build, evaluate, and harden features built on large language models and other foundation models — prompts, structured outputs, RAG, agents, tools and MCP servers, evals, guardrails, and LLMOps. It chooses the simplest approach that works, proves every change with evals, and treats untrusted content and model output as hostile until checked.

Domain: `ai-engineering` · Type: `core`

## When to use

Invoke with `/the-ai-engineer`, or let Claude pick it up automatically when you ask for things like:

- "Should we use RAG or just put the handbook in the prompt for our HR assistant?" (Mode A)
- "Build a support bot that answers from our docs and can look up order status." (Mode B)
- "Our summarizer got worse after the prompt change — prove it and fix it." (Mode C)
- "Review our email agent for prompt-injection risks before launch." (Mode D)
- "Our LLM bill doubled this month, find out why." (Mode D)
- "The extractor sometimes returns invalid JSON." (Mode E)

| Mode | For | Output |
|---|---|---|
| A — Design | Feasibility, approach ladder, models, budgets, risks | `docs/ai/AI_DESIGN.md` |
| B — Build | Prompts, structured outputs, tools, RAG, agents, MCP, with evals from day one | Code, prompt templates, eval cases, baseline run |
| C — Evaluate & Improve | Error analysis, datasets, graders, judge calibration, paired comparisons | `evals/`, `runs/`, `docs/ai/EVAL_REPORT.md` |
| D — Harden & Review | OWASP LLM + Agentic Top 10, reliability, cost, observability, compliance | `docs/ai/AI_REVIEW.md` |
| E — Quick Fix | Small fixes, each with a regression case | Fix + regression case |

Gates: **Approach** (climb the ladder only with evidence), **Eval** (no change ships without a measured comparison), **Agent Safety** (lethal-trifecta check, least privilege, human approval, caps).

### Scripts on their own

```text
python scripts/eval_runner.py validate --dataset evals/cases.jsonl
python scripts/eval_runner.py run --dataset evals/cases.jsonl --oracle --out runs/oracle
python scripts/eval_runner.py run --dataset evals/cases.jsonl --target-py app.bot:answer --reps 3 --out runs/v1
python scripts/eval_runner.py compare --baseline runs/v1 --candidate runs/v2 --fail-on-regression --must-pass-tag must-pass
python scripts/usage_report.py logs/calls.jsonl --prices prices.json --group route
```

Both scripts use only the Python standard library and never call a model provider themselves: the system under test and any LLM judge are plugged in by you, so they work with every provider.

## Structure

```text
the-ai-engineer/
├── SKILL.md                                  # modes, principles, gates, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml                            # manifest + machine-readable policy
├── references/
│   ├── system-design.md                      # feasibility, approach ladder, patterns, model selection, budgets
│   ├── prompting-and-context.md              # context engineering, prompts, structured outputs, caching layout
│   ├── rag.md                                # ingestion, hybrid search, reranking, permissions, RAG evals
│   ├── agents-and-tools.md                   # tool design, agent loops, MCP (2026-07-28), A2A, human approval
│   ├── evals.md                              # error analysis, datasets, graders, judges, statistics, CI
│   ├── security-and-safety.md                # OWASP LLM/Agentic Top 10, injection, lethal trifecta, EU AI Act
│   ├── production.md                         # reliability, cost levers, OTel GenAI tracing, rollouts, monitoring
│   ├── fine-tuning.md                        # when to fine-tune/distill, methods, data, serving open weights
│   ├── AI_DESIGN.template.md
│   ├── EVAL_REPORT.template.md
│   └── AI_REVIEW.template.md
├── scripts/
│   ├── eval_runner.py                        # provider-neutral eval harness: run, grade, compare, CI gate
│   └── usage_report.py                       # cost / cache / latency / error report from call logs
├── assets/
│   ├── eval_cases.example.jsonl              # example dataset covering the grader types
│   └── llm_judge.template.py                 # binary LLM judge with calibration
└── evals/
    └── evals.json
```

Research basis (verified 2026-09-11): MCP specification 2026-07-28 and the Agentic AI Foundation (MCP, AGENTS.md, and since August 2026 A2A 1.0), OWASP Top 10 for LLM Applications 2025 and for Agentic Applications 2026, the EU AI Act timeline after the May 2026 Digital Omnibus agreement, OpenTelemetry GenAI semantic conventions (Development status), prompt-injection design patterns (lethal trifecta, plan-then-execute, CaMeL-style policy engines), current RAG practice (hybrid search, reranking, contextual chunks), eval practice (error analysis, binary graders, judge calibration), and fine-tuning guidance (prompt → RAG → fine-tune → distill).

## Changelog

### 0.1.0 — 2026-09-11

- Initial version: five modes (design, build, evaluate and improve, harden and review, quick fix), Approach, Eval, and Agent Safety gates, eight references, three templates, a provider-neutral eval runner (12 grader types, error separation, Wilson and paired bootstrap intervals, CI gate), a usage and cost analyzer, an example dataset, and a calibratable LLM-judge template.
