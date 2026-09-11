# Prompting and Context Engineering

How to write prompts and assemble context that produce reliable behavior, across providers.

## Contents

1. Context engineering
2. Prompt structure
3. Writing instructions
4. Examples (few-shot)
5. Structured outputs
6. Reasoning models
7. Caching-friendly layout
8. Long context
9. Prompt management
10. Anti-patterns

---

## 1. Context engineering

The model only knows what is in its context window. Most quality problems are **context problems**: missing facts, irrelevant noise, stale data, or instructions buried in the middle. Design the whole context, not only the prompt:

| Layer | Question |
|---|---|
| Instructions | What role, task, rules, and output format? |
| Knowledge | Which retrieved documents or data, how many, in what order? |
| Tools | Which tools are available *for this task*, with what descriptions? |
| Memory and state | What from earlier turns or sessions is relevant, summarized how? |
| User input | Clearly delimited and treated as data |

Principles:

* **Smallest set of high-signal tokens** that gets the job done. More context is not better; irrelevant context lowers accuracy and raises cost.
* **Retrieve then rerank then trim** instead of dumping everything in.
* **Scope tools per task or sub-agent**; loading every tool into every call wastes tokens and confuses tool choice. Use on-demand tool discovery when the tool set is large.
* **Compress long histories** (summaries, clearing old tool results) and keep durable facts in explicit memory.
* Measure context: token count per section, cache hit rate, and cost per task.

## 2. Prompt structure

A reliable default order:

```text
[System / developer instructions]   role, goal, audience, rules, output format, tool-use guidance
[Reference material]                documents, data, examples, in clearly labelled sections
[Conversation / task input]         the user's request, delimited
```

* Use **clear section delimiters** (headings or XML-style tags such as `<context>`, `<documents>`, `<user_request>`) so instructions and data don't blur. Tell the model which sections are untrusted data.
* Put the most important instructions at the start of the system prompt; for very long contexts, restate the key question after the documents.
* Give the **why** behind rules ("Answers are read aloud by a voice assistant, so avoid lists and markdown") — models generalize better from reasons than from bare commands.

## 3. Writing instructions

* Be specific about the task, audience, length, tone, and format, and about what to do when information is missing ("If the context doesn't contain the answer, say so and suggest contacting support").
* Say what to do, not only what not to do.
* Define terms and decision criteria explicitly (what counts as "urgent").
* Current capable models follow instructions closely: ALL-CAPS warnings and repeated "MUST" are rarely needed and can cause over-application. Use emphasis only for true hard rules.
* Keep one source of truth: the same rule stated twice in different words invites inconsistency.
* For customer-facing assistants, specify scope and refusal behavior, escalation paths, and what the assistant must never claim (prices, legal or medical advice) unless grounded in provided data.

## 4. Examples (few-shot)

* A few diverse, realistic examples teach format and judgment faster than paragraphs of rules.
* Cover edge cases and the "no answer" case, not only happy paths.
* Label examples clearly as examples so they aren't mistaken for the current input.
* Never copy eval cases into prompts (that leaks answers into the eval).

## 5. Structured outputs

When code consumes the output, use the provider's **schema-constrained output or strict tool-call mode** where available (JSON Schema enforced during generation), rather than asking for JSON in prose and hoping:

* Define a JSON Schema with `required` fields, `additionalProperties: false`, enums for categorical values, and descriptions for each field.
* Include an explicit way to express uncertainty or absence (`"answer": null`, `"confidence"`, `"reason_if_unknown"`), so the model isn't forced to invent values.
* Still **validate** on receipt (schema plus business rules), and handle refusals and truncation before parsing.
* Put reasoning fields before answer fields if you want the model to think first in the output, or rely on the provider's reasoning feature instead.
* Parse with a JSON parser, never with string matching; escaping differs between models.

## 6. Reasoning models

Models with built-in reasoning ("thinking") modes:

* Give them the goal, constraints, and success criteria; avoid prescribing every step, which can reduce quality.
* Use the provider's reasoning-effort or budget control to trade quality against latency and cost per route, and measure it with the eval.
* Don't parse or display raw reasoning as if it were reliable; many providers summarize or hide it.

## 7. Caching-friendly layout

Most providers offer **prompt (prefix) caching**: a repeated identical prefix is billed at a discount and processed faster. Details and controls differ by provider; the layout rules are universal:

* **Stable first, volatile last:** tool definitions and system prompt (frozen), then reference documents that repeat, then the conversation, then the new user message.
* Any byte change in the prefix (a timestamp, a per-user name, reordered tool list, unsorted JSON) breaks the cache for everything after it.
* Keep tool lists and their order deterministic; don't switch models mid-session if caching matters (caches are per model).
* Verify with the provider's reported cached-token counts (`scripts/usage_report.py` shows the hit rate).

## 8. Long context

* Large context windows allow whole documents, but accuracy can drop for facts buried in the middle and cost grows linearly. Test retrieval-in-context with your data rather than assuming.
* Put documents before the question, label each document (title, source, date), and ask for quotes or citations to ground answers.
* For very large corpora, retrieval (`references/rag.md`) is still cheaper, fresher, and permission-aware.

## 9. Prompt management

* Prompts are code: store them in the repository (templates with variables), review changes, and **version** them.
* Every prompt change runs the eval (`scripts/eval_runner.py compare`) before release.
* Log the prompt version and model with every call, so production traces map to the exact configuration.
* Keep secrets and personal data out of prompt templates.

## 10. Anti-patterns

| Anti-pattern | Better |
|---|---|
| Stuffing all documents and all tools into every call | Retrieve, rerank, and scope tools per task |
| Vague instructions ("be helpful and accurate") | Concrete criteria, format, and fallback behavior |
| Asking for JSON in prose and regex-parsing it | Schema-constrained output plus validation |
| Tuning a prompt on three examples by eye | Error analysis on real traces and an eval with variance |
| Timestamps or user IDs at the top of the system prompt | Put volatile data at the end to keep the cache |
| Prompt text copied between models without re-testing | Re-run the eval per model; prompts don't transfer perfectly |
| Instructions that fight each other or repeat | One clear statement per rule, with its reason |
