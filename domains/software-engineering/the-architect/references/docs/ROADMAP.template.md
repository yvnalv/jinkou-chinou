# ROADMAP — AIAgent Chat External API

Phased delivery. **Phase 0 (this work item) is documentation only.** Each phase is
gated by the previous one and by the open questions in `PRD.md` §8.

---

## Phase 0 — Design & documentation ✅ (current)

- Analyze the codebase; confirm framework, flows, orchestrator, config.
- Produce the docs in this folder.
- **Exit:** product owner approves the design and answers `PRD.md` §8.

## Phase 1 — External API skeleton + auth (no orchestration yet)

- Decide and create the new project (recommended: **`GLMSys.AIPlus.Agent.Server.External`**;
  alternatives `…ExternalApi`, `…WebApi`). It **references** `Shared`,
  `Server.Prompts`, `Server.Service`; it does **not** modify them.
- Add `GLMSysAIPlusAgentExternalAPI.ashx` (`IHttpHandler`) under `Setup\docs\` with
  sub-path/action routing for the four endpoints.
- Implement `ExternalApiKeyValidator` (parameterized lookup on
  `GLMSysCIConnections`, `SoftwareID=999`, `Active=1`) → customer identity.
- Enforce `Authorization: Bearer` on every request; fail closed; standard JSON
  error envelope.
- `POST /ai/chat` returns a stubbed echo to prove transport + auth end-to-end.
- **Exit:** valid key → 200 stub; invalid/missing key → 401; verified with the
  `test-key-001` row.

## Phase 2 — Chat orchestration (final replies only)

- Implement `ExternalAgentOrchestrator` by **composition**: reuse
  `AgentChatService.Step`, `Server.Prompts.*PromptBuilder`, `IntentClassifier`,
  `IntentToolFilter`, JWT services, security filter.
- `POST /ai/chat` runs one or more Steps and returns a final assistant reply when
  the provider needs no customer tool.
- Run **server-handled** tools (`search_documentation`) in-process.
- Meter usage to `GLMSysCILLMUsage`.
- **Exit:** non-tool prompts return correct replies via the external API; usage
  rows written; `Server.Service`/`Server.Prompts` unchanged.

## Phase 3 — Customer-side tool handoff (suspend/resume)

- Implement conversation state (recommended: server-side tables — see `DATABASE.md`).
- `POST /ai/chat` returns structured `tool_calls` and **suspends** (persists state).
- `POST /ai/tool-result` resumes: append tool result(s), continue Stepping until a
  final reply / another tool call / `[AGENT_DONE]`.
- Guarantee correct `tool_call_id` binding across the HTTP boundary.
- **Exit:** full round trip works for read/create/update/delete and navigate tools.

## Phase 4 — Conversation management + isolation + quota

- `GET /ai/conversation/{id}` and `POST /ai/reset` scoped to the authenticated key.
- Per-customer isolation on every state/query row; idle-conversation expiry.
- Per-key rate limit / quota enforced before the provider call.
- **Exit:** isolation and quota verified; conversation lifecycle complete.

## Phase 5 — Customer Local Agent contract + sample

- Document the Local Agent contract (map `tool_calls` → `IAgentToolExecutor.Execute`
  → `tool` result message).
- Provide a minimal reference Local Agent (can reuse existing executors).
- **Exit:** a customer can integrate end-to-end against the documented contract.

## Phase 6 (deferred) — Inheritance refactor for DRY

- Refactor `SecuredAgentOrchestrator` into `protected virtual` seams (prepare /
  step / dispatch-tool) and make `ExternalAgentOrchestrator : SecuredAgentOrchestrator`
  override only tool dispatch. **Only after the internal flow is confirmed stable.**
- **Exit:** loop-control duplication removed; both flows share one orchestrator base.

## Phase 7 (optional) — Hardening

- Hash stored API keys; rotate the JWT secret out of code into a vault/secure
  setting; structured audit logging; optional streaming responses.

## Phase 8 (future) — UX & cost enhancements

- **Persist `conversationId` client-side** (`sessionStorage`/`localStorage`) so a chat room
  survives page reloads/navigation (today it is in-memory only).
- **Chat history sidebar** (ChatGPT/Claude-style): list a user's past rooms and reopen them.
  Foundation already exists (one row per room + `GET /ai/conversation/{id}`); needs a per-user
  scope column (`ResourceID`) on `GLMSysAIPlusAgentConversation`, a list endpoint, a title
  (derive from first user message), and the sidebar UI (render user/assistant text only).
- **Token/cost reduction:** trim history to last N turns on the external flow (the internal
  flow has `TrimConversationHistory`); leverage prompt caching. Per-conversation cost is already
  trackable via `GLMSysCILLMUsage.ConversationId`.
- **Widget JS cache-busting:** append `?v=<version>` to the chat-engine script include
  (`AIAgentHelper.cs`/`PortalExtension.cs`) so JS updates reach users without a hard refresh.

---

## Dependency graph

```
Phase 0 ─▶ Phase 1 ─▶ Phase 2 ─▶ Phase 3 ─▶ Phase 4 ─▶ Phase 5
                                     └────────────────────────────▶ Phase 6 (deferred)
                                                                     Phase 7 (optional)
```

## Tracking note

A prior memory claimed external-API artifacts already existed
(`GLMSysAIPlusAgentExternalAPI.ashx`, `GLMSysAIPlusLocalAgentHandler.aspx`,
`LLMUsageService.cs`). **They are absent from the current branch** — treat all
phases as green-field that reuse existing assemblies.
