# Agents, Tools, and MCP

How to design tools, build agent loops that finish reliably, use MCP and agent-to-agent protocols, and keep humans in control. Protocol facts verified on 2026-09-11; check the current specifications before relying on version details.

## Contents

1. Workflow or agent?
2. Tool design
3. The agent loop
4. Context management for long runs
5. Multi-agent systems
6. Human-in-the-loop
7. MCP (Model Context Protocol)
8. Agent-to-agent (A2A)
9. Testing agents

---

## 1. Workflow or agent?

Default to a workflow (code decides the steps). Choose an agent only when the task is open-ended **and** valuable **and** models can do it **and** mistakes are recoverable (`references/system-design.md` section 3). Many "agents" are better as a router plus two or three fixed workflows.

## 2. Tool design

Tools are the agent's interface to the world; their design drives quality more than prompt wording.

* **Few, well-scoped tools** that match real tasks (`search_orders`, `get_order`, `refund_order`), not a thin wrapper over every API endpoint.
* **Names and descriptions written for the model:** what the tool does, when to use it and when not to, what each parameter means with formats and examples, and what it returns. Unambiguous parameter names (`customer_email`, not `id`).
* **Strict schemas:** required fields, enums, `additionalProperties: false`; use the provider's strict tool mode where available.
* **Token-efficient results:** return the fields the model needs, with pagination, filtering, and a concise/detailed switch. Return stable IDs so the model can follow up.
* **Helpful errors:** return an error result the model can act on ("No order found for A-1042; did you mean A-1024?"), not a stack trace. Mark failed calls as errors rather than dropping them.
* **Idempotent and safe by default:** reads are free; writes are explicit, idempotent where possible (idempotency keys), and scoped to the least privilege.
* **Dedicated tools over a generic shell** for anything that needs a security check, approval, audit, staleness check, or special UI; a shell or code-execution tool gives breadth but only an opaque command string to your harness.
* **Parallel calls:** when the model requests several independent tools at once, run them concurrently and return all results together.

## 3. The agent loop

```text
while not done:
    response = model(context, tools)
    if response is final answer: done
    for each tool call: check policy → (ask human if required) → execute with timeout → append result
    enforce budgets: max steps, max tokens or cost, wall-clock time
```

* **Explicit stop conditions:** a final-answer state, step and cost caps, and a "cannot complete" path the model is told it may take.
* **Give the full task up front:** goal, constraints, definition of done, and available resources; agents do better with a complete brief than with drip-fed instructions.
* **Ground in the environment:** tests, linters, search results, and API responses are real feedback; design tasks so the agent can check its own work.
* **Checkpoints and resumability** for long tasks: persist state, make steps idempotent, and log every call.
* Prefer the provider's or framework's maintained tool-loop helpers over hand-written loops when they fit; hand-write when you need full control.

## 4. Context management for long runs

| Technique | Use when |
|---|---|
| Clearing old tool results | Long runs accumulate large, no-longer-needed outputs |
| Summarization / compaction | The conversation approaches the context limit |
| External memory (files, a store) | Facts must persist across sessions or sub-agents |
| Sub-agents with their own context | A subtask needs lots of reading; return only a condensed result to the parent |
| Code execution to filter data | Large intermediate data should be processed in code, not read token by token |
| On-demand tool loading | Hundreds of tools exist, but only a few matter per task |

Keep caching in mind: changing tools, models, or the system prompt mid-session invalidates cached prefixes.

## 5. Multi-agent systems

Multiple agents help when work **fans out** (research many sources, process many files) or when separate contexts prevent one loop from drowning in reading. They also multiply cost, latency, and failure modes (cascading errors, conflicting actions, insecure agent-to-agent messages).

* Start with one agent; split only when an eval or trace shows a real benefit.
* Give each sub-agent a precise task, output format, and budget; the orchestrator verifies results rather than trusting them.
* Treat messages from other agents as untrusted input, with the same controls as user input.

## 6. Human-in-the-loop

Require explicit human approval for actions that are **irreversible, costly, externally visible, or security-relevant**: sending messages or emails, payments, deleting data, changing permissions, deploying, and posting publicly.

* Show the exact action and parameters in the approval request, not a paraphrase or the agent's persuasive summary; a confident explanation can talk people into unsafe approvals (OWASP ASI09, human-agent trust exploitation).
* Avoid approval fatigue: approve only what matters, batch low-risk actions, and never let a flood of requests train people to click "yes".
* Allow edit-before-approve, and log who approved what.
* Autonomy can grow per action type as evals and production evidence justify it.

## 7. MCP (Model Context Protocol)

MCP is the open standard for connecting AI applications (hosts and clients) to tools, resources, and prompts exposed by servers. Since December 2025 it is governed under the Linux Foundation's Agentic AI Foundation. The current specification version is **2026-07-28**, which made the protocol core stateless (remote servers behave like ordinary HTTP services), added multi-round-trip requests, header-based routing, cacheable list results, hardened authorization, and a formal extensions framework.

* **Build an MCP server** when several AI clients (IDEs, chat apps, agents) should reach the same capability, or when you publish an integration for others. For a single app's internal tools, native tool calling is simpler.
* Use an **official MCP SDK** (Tier 1 SDKs track the spec) rather than implementing the protocol by hand.
* **Design MCP tools with the same rules as section 2**: good descriptions, strict schemas, compact results.
* **Security:** authenticate remote servers (the spec's OAuth-based authorization), scope tokens to least privilege, validate all inputs, rate-limit, and log. Treat third-party MCP servers as supply-chain dependencies: review, pin versions, and watch for tool descriptions that contain injected instructions ("tool poisoning") or change after approval.
* Keep **tool counts manageable** per client; many servers each with many tools overwhelm context unless the client loads tools on demand.

## 8. Agent-to-agent (A2A)

A2A is the open protocol for agents built by different parties to delegate tasks to each other (discovery through agent cards, task lifecycle, streaming updates). Its first stable version (1.0) shipped in March 2026, and it moved into the Agentic AI Foundation in August 2026. Rule of thumb: **MCP is how an agent uses tools; A2A is how an agent works with someone else's agent.** Use A2A only when you actually integrate with independent agents; inside one system, function calls or queues are simpler.

## 9. Testing agents

* **Grade the end state**, not the transcript: run tasks in a disposable environment and check what changed (tests pass, records correct, nothing off-limits touched).
* Track trajectory metrics: steps, tool calls, errors, cost, and time per task, plus the rate of unnecessary or unsafe calls.
* Include cases where the right move is to **not** act, to ask for clarification, or to stop.
* Run several repetitions: agents are stochastic, and one success proves little.
* Replay real production traces as regression cases.
