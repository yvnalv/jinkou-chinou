# Security, Safety, and Compliance

Threats specific to LLM applications and agents, the controls that work, and the regulatory landscape. Facts in sections 1 and 7 were verified on 2026-09-11; laws and lists change, so re-check official sources, and treat this as engineering guidance, not legal advice.

## Contents

1. Threat lists (OWASP)
2. Prompt injection
3. The lethal trifecta
4. Architectural defenses for agents
5. Output handling and data protection
6. Guardrails and red teaming
7. Regulation
8. Security review checklist

---

## 1. Threat lists (OWASP)

**OWASP Top 10 for LLM Applications (2025):** LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Supply Chain · LLM04 Data and Model Poisoning · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM08 Vector and Embedding Weaknesses · LLM09 Misinformation · LLM10 Unbounded Consumption.

**OWASP Top 10 for Agentic Applications (2026, published December 2025):** ASI01 Agent Goal Hijack · ASI02 Tool Misuse and Exploitation · ASI03 Agent Identity and Privilege Abuse · ASI04 Agentic Supply Chain Compromise · ASI05 Unexpected Code Execution · ASI06 Memory and Context Poisoning · ASI07 Insecure Inter-Agent Communication · ASI08 Cascading Agent Failures · ASI09 Human-Agent Trust Exploitation · ASI10 Rogue Agents.

Use these IDs in reviews (`AI_REVIEW.md`) so findings map to a shared vocabulary.

## 2. Prompt injection

* **Direct:** the user types instructions to override the system ("ignore previous instructions…").
* **Indirect:** instructions hidden in content the model reads: web pages, emails, documents, retrieved chunks, tool results, image text, MCP tool descriptions, other agents' messages.

There is **no reliable detector-only defense**; adaptive attackers bypass input filters and classifier guardrails. Treat injection as inevitable and **limit what a successful injection can do**. Filters and instruction hierarchy still help as one layer.

## 3. The lethal trifecta

An agent is exploitable for data theft when it combines all three:

1. **Access to private data** (user files, emails, databases, credentials)
2. **Exposure to untrusted content** (web, email, documents, tickets, third-party tools)
3. **A way to communicate externally** (HTTP requests, sending email, creating links or images that load URLs, writing to shared places)

Design so that no single agent context has all three, or put a human approval or deterministic policy check on the external channel. Rendering model output as Markdown with images or links is itself an exfiltration channel (data in URL parameters).

## 4. Architectural defenses for agents

| Pattern | Idea |
|---|---|
| Least privilege | Minimal tools, scopes, and data per task; short-lived, narrowly scoped credentials; no shared admin tokens |
| Plan-then-execute | Fix the plan (which tools, which targets) before reading untrusted content, so injected text cannot add new actions |
| Dual model / quarantine | A privileged model plans and acts but never sees untrusted text; a quarantined model processes untrusted text and returns only constrained values (enums, IDs, structured fields) |
| Policy engine outside the model | The model proposes actions; deterministic code checks them against rules (allowed recipients, domains, amounts) before execution (the idea behind CaMeL-style designs) |
| Action allow-lists | Outbound network only to allow-listed domains; no arbitrary URL fetches with user data |
| Human approval | Required for irreversible or externally visible actions (`references/agents-and-tools.md` section 6) |
| Sandboxing | Code execution in isolated containers with no secrets, no network by default, resource limits, and disposable state |
| Provenance tracking | Mark which data came from untrusted sources and block it from flowing into sensitive sinks |

## 5. Output handling and data protection

* **Model output is untrusted input** to the rest of the system. Never pass it unescaped into HTML (XSS), SQL, shell commands, file paths, `eval`, templates, or URLs. Validate against schemas and allow-lists.
* **Secrets:** never put credentials in prompts, tool descriptions, or logs; the model can reveal anything in its context. System prompts are not secret either; don't rely on them for security.
* **Personal data:** minimize what is sent; redact in logs and traces; honor retention limits; check provider data-use and residency terms.
* **Misinformation:** ground answers in sources, show citations, add uncertainty and "not found" behavior, and require human review for high-stakes outputs (medical, legal, financial).
* **Unbounded consumption:** rate limits per user, max tokens, max agent steps, cost budgets and alerts, and protection against prompts designed to cause long outputs or loops.
* **Supply chain:** pin model versions and SDKs; review third-party MCP servers, plugins, datasets, and open-weights models (provenance, licence, known issues).

## 6. Guardrails and red teaming

* **Input guardrails:** topic scope, abuse, and injection classifiers as a first filter, not a guarantee.
* **Output guardrails:** schema validation, policy checks (no promises the business can't keep), PII detection, grounding checks, and moderation where required.
* **Refusal and escalation paths** designed as product features: polite scope limits, handoff to humans.
* **Red teaming:** before launch and after major changes, attempt direct and indirect injection, data exfiltration through tools and rendered links, jailbreaks of scope rules, excessive-agency scenarios, and cost abuse. Turn successful attacks into eval cases with a `must-pass` tag.

## 7. Regulation

**EU AI Act** (status after the Digital Omnibus provisional agreement of May 2026):

| Obligation | Applies from |
|---|---|
| Prohibited practices (Article 5) | 2 February 2025 |
| General-purpose AI model provider obligations | 2 August 2025 |
| Transparency duties (Article 50: tell people they are interacting with AI, disclose deepfakes and AI-generated text published on matters of public interest) | 2 August 2026 |
| Machine-readable marking of synthetic content (Article 50(2)) | 2 December 2026 |
| High-risk systems in Annex III (for example employment, credit, education, essential services) | 2 December 2027 (postponed from August 2026) |
| High-risk systems in Annex I (product-safety legislation) | 2 August 2028 |

Practical engineering consequences: disclose AI interaction in chatbots and assistants, label or mark AI-generated content where required, and if the use case may be high-risk, involve legal counsel early (risk management, data governance, logging, human oversight, accuracy and robustness documentation).

Elsewhere: sector rules (finance, health, employment), privacy law (GDPR and equivalents) for personal data in prompts, logs, and training data, and frameworks such as the NIST AI Risk Management Framework and its generative AI profile, or ISO/IEC 42001 for AI management systems. Ask where the product is used and check current law.

## 8. Security review checklist

- [ ] Trifecta check: no agent context combines private data, untrusted content, and an external channel without a policy or approval gate.
- [ ] Tools are least-privilege, scoped per task, with strict schemas and validated inputs.
- [ ] Irreversible and externally visible actions require human approval.
- [ ] Model output is escaped or validated before reaching HTML, SQL, shell, files, or URLs; Markdown image and link rendering is controlled.
- [ ] Retrieval enforces the end user's permissions; the index is protected against poisoning and cross-tenant leakage.
- [ ] No secrets in prompts, tool descriptions, or logs; personal data minimized and redacted.
- [ ] Rate limits, token caps, step caps, and cost alerts are in place.
- [ ] Third-party models, SDKs, MCP servers, and datasets are pinned and reviewed.
- [ ] Red-team cases exist in the eval with a `must-pass` tag.
- [ ] Transparency and labelling duties that apply to the product are implemented.
