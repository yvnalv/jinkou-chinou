# AI Plus Agent — External AI Agent API

Design documentation for the work item **"AIAgent Chat External API with Secure
Customer API Key and Customer-side Tool Execution."**

> **Implemented & in production.** The external API is built and deployed (project
> `GLMSys.AIPlus.Agent.Server.External` in the `AIPlusAgentServerInternal` repo under
> `Addons\505`). These documents are the **design of record** — keep them in sync with the
> code and log every change in `CHANGELOG.md` (newest on top). Some deeper docs still describe
> the pre-refactor `503` / `GLMSysCIConnections` naming; cross-check against the code.

---

## What this is

AI Plus Agent is a natural-language chat assistant addon for **Exact Synergy
Enterprise 503+** (C#, **.NET Framework 4.7**, all class-library DLLs), powered by
Azure OpenAI. It lets users look up, create, update, delete, navigate, and email
Synergy/Globe records in plain language, gated by their Synergy entity rights.

This work item adds a **production external API** so customer apps talk to *our*
GLM-hosted AI service instead of running the AI orchestration in-process on their
own server — while **keeping tool execution on the customer side** (only the
customer can reach the customer database).

## The two flows

**Today (internal / direct) — stays for testing:**

```
Chat widget (JS)
  → GLMSysAIPlusAgentClientCallBack.aspx   (customer server, in-process)
      → SecuredAgentOrchestrator → AgentChatService → Azure OpenAI   (customer's own keys)
      → tool executor runs locally (customer DB)
  → reply
```

**Target (external API):**

```
Customer App / Chat widget
  → [X-API-Key: <key>]  POST /ai/chat   → GLM Server External API (.ashx)
      → validate API key  (GLMSysAIPlusProviderConnections, SoftwareID=999)
      → orchestrate: AgentChatService.Step → AI provider (GLM's keys, never exposed)
  ← assistant reply  OR  structured tool_calls
  → Customer Local Agent executes tool(s) locally against customer Synergy/DB
  → POST /ai/tool-result  → server feeds results back to AI provider
  ← next assistant reply / another tool_call / [AGENT_DONE]
```

The server **orchestrates the conversation**; the customer **executes the tools**.

## Endpoints (see `docs/API_SPEC.md`)

| Method & path | Purpose |
|---|---|
| `POST /ai/chat` | Send user message; get final reply **or** tool-call instructions. |
| `POST /ai/tool-result` | Return locally-executed tool results; get next assistant turn. |
| `GET  /ai/conversation/{id}` | Fetch conversation history for the authenticated key. |
| `POST /ai/reset` | Reset the conversation/session for the authenticated key. |

Hosted as a single `.ashx` handler (e.g. `GLMSysAIPlusAgentExternalAPI.ashx`) that
routes by sub-path/action — not an `.aspx` page (no WebForms lifecycle/NTLM/viewstate
issues). See `docs/ARCHITECTURE.md`.

## Authentication

Every request carries the API key in **`X-API-Key: <api-key>`** (canonical — survives IIS
Windows Auth, which clobbers `Authorization`), with **`Authorization: Bearer <api-key>`** accepted
as a fallback. The key format is `glm_live_`/`glm_test_` + 22-char + 32-char base62 (see
`docs/AUTH_TOKEN_TYPE.md`). The server validates it against the **`GLMSysAIPlusProviderConnections`**
row with **`SoftwareID = 999`**, `Active = 1`, and non-expired `ExpiryDate` — matching by the
indexed `KeyID` then a constant-time decrypt-and-compare — and derives the customer identity
**from that row**, never from the request body. Example row:

```
ID:        72AEDC9B-ECFF-4EF0-89F3-DA1113D623F7
SoftwareID: 999
KeyID:     <22-char base62 lookup id>
APIKey:    <Exact.Core.Crypt-encrypted glm_live_… key>
Active:    1
Product:   synergy            (or 'globe')
```

→ client sends `X-API-Key: glm_live_<keyid><secret>`. The legacy `test-key-001` placeholder is
**not** a valid key and is rejected.

## Reuse principle

The external orchestrator **reuses** the existing public LLM core
(`AgentChatService.Step`), prompt builders (`Server.Prompts`), intent classifier,
security filter, and JWT services. It only adds: HTTP transport, API-key auth,
conversation state, and the **suspend/resume** loop needed to hand tool execution
back to the customer. `Server.Prompts` and `Server.Service` are **not modified** in
this work item. See `CLAUDE.md` §5.

## Document index

| File | Contents |
|---|---|
| `CLAUDE.md` | Assistant/engineer brief: facts, reuse contract, guardrails. |
| `CHANGELOG.md` | Running change log (newest first). **Update on every change.** |
| `docs/PRD.md` | Goals, scope, requirements, open questions. |
| `docs/ROADMAP.md` | Phased delivery plan. |
| `docs/ARCHITECTURE.md` | Current vs. target architecture, orchestrator design, flows. |
| `docs/DATABASE.md` | `GLMSysCIConnections`, `SoftwareID=999`, proposed conversation/usage tables. |
| `docs/API_SPEC.md` | Endpoint contracts, request/response JSON, errors. |
| `docs/CODING_STANDARDS.md` | .NET 4.7 conventions, security guardrails. |
| `docs/TESTING.md` | Test strategy and scenarios. |
| `docs/DEPLOYMENT.md` | Build, deploy, IIS/AppPool, config. |
| `docs/CONTRIBUTING.md` | Branching, PRs, review checklist. |

## Status

- ✅ Codebase analyzed; framework + flows confirmed.
- ✅ Design documented (this folder).
- ✅ Implementation **shipped & in production** — external API, API-key lifecycle
  (`GLMSysAIPlusProviderConnections`), license-driven key issuance, product routing
  (Synergy / Globe+), async orchestration (#6949).
- ♻️ ConnectIt **AIAgent** provider **retired (2026-08-26)** — key comes from
  `GLMSysAIPlusProviderConnections`, not a ConnectIt `999` connection; other ConnectIt use
  (AzureOpenAI LLM, customer CRUD, usage logging) stays. See `CHANGELOG.md`.
- ⚠️ Open production issue: `Initializing the Environment here is not allowed` on
  server-to-server calls — see `docs/Major Refactoring References/07-KNOWN-ISSUES.md` §A
  and `CHANGELOG.md` (2026-08-26).
