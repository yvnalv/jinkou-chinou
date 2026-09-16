# CODING_STANDARDS — AI Plus Agent External API

Conventions and guardrails for external-API code. These match the existing
codebase; deviations should be justified in the PR.

---

## 1. Platform

- **.NET Framework 4.7** only. No ASP.NET Core, no .NET 5+, no `System.Text.Json`.
- Classic (non-SDK) `.csproj`, `OutputType=Library`. Add the new project in the
  same style as the existing ones (DLL references via `HintPath` into
  `C:\Exact Synergy Enterprise 503\bin\`, `Private=False` for Synergy/CI assemblies).
- HTTP endpoint = **`.ashx` `IHttpHandler`**, not `.aspx`. Synchronous
  `ProcessRequest(HttpContext)`.
- JSON via **`Newtonsoft.Json`** (`JObject`/`JArray`); serialize on the wire with
  `Formatting.None`.
- Language features: stay within what the bundled C# compiler for the existing
  projects accepts (the codebase uses classic C#: explicit types, no records, no
  top-level statements, no `init`-only setters). Match surrounding code.

## 2. Project & naming

- New project (recommended): **`GLMSys.AIPlus.Agent.Server.External`**. It
  **references** `Shared`, `Server.Prompts`, `Server.Service`; it must **not**
  modify them.
- Namespaces mirror folder/assembly names (`GLMSys.AIPlus.Agent.Server.External`).
- Post-build event copies the DLL to `C:\Exact Synergy Enterprise 503\BIN\` (same
  pattern as every other project).
- File/class names: `ExternalAgentOrchestrator`, `ExternalApiKeyValidator`,
  `ExternalChatRequest`/`Response`, `ConversationStore`, etc.

## 3. Reuse rules (DRY — the central guardrail)

- **Reuse, never re-implement** `AgentChatService.Step` (the LLM round-trip) and the
  `Server.Prompts.*PromptBuilder` builders, `IntentClassifier`, `IntentToolFilter`,
  `JwtTokenService`, `JwtEntityRightsProvider`, `EntityRegistry`, `ConnectionHelper`.
- New code is limited to: HTTP transport, API-key auth, conversation state, the
  suspend/resume loop, request/response contracts, usage metering.
- Do **not** copy the body of `SecuredAgentOrchestrator.ProcessChat`. If a pure
  helper there is genuinely needed, the DRY path is the Phase-2 `protected virtual`
  refactor (deferred) — not a copy-paste.

## 4. Security

- **API key required** on every request; validate against `GLMSysCIConnections`
  (`SoftwareID=999`, `Active=1`) with a **parameterized** query. Fail closed.
- **Never trust** `customerId` from body/header; derive identity from the validated
  row only.
- **Scope every query and state row** by the customer connection id (multi-tenant
  isolation).
- **Never expose** AI-provider keys or internal details (no stack traces, SQL,
  provider payloads) in responses; use the standard error envelope.
- **Parameterize all SQL** via `QueryBuilder.AppendWhere(col, value)`. No string
  concatenation of request input.
- **Do not log** API keys or full conversation content; redact secrets.
- Replace the hardcoded JWT secret (`GetJwtSecretKey()` → `"MySecret"`) with a
  secure source before any external rollout (`PRD.md` §8.4).
- TLS only in production.

## 5. Error handling

- Catch at the handler boundary; map to the documented HTTP code + JSON envelope
  (`API_SPEC.md` §6).
- Distinguish `UnauthorizedAccessException` → 401/403 (the existing callback already
  does this) from generic exceptions → 500 with a generic message.
- Honor the existing content-filter handling in `AgentChatService` — surface the
  friendly message, not a 5xx, where possible.

## 6. Data access

- Use `Exact.Data.QueryBuilder` + `EDLConnection` + `EDLQueryOptions`
  (`SingleValue`/`SingleRow`) exactly as `ConnectionHelper` and the orchestrator do.
- The external API runs with the **GLM server's** `Exact.Core.Environment` —
  it can read `GLMSysCIConnections`/`GLMSysCILLMUsage` and call the provider, but
  **must not** assume access to any customer DB.

## 7. JSON / message conventions

- Message objects: `role`, `content`, `tool_calls`, `tool_call_id`, `name` — the
  OpenAI shape already used internally.
- Preserve provider `tool_calls` **verbatim** (ids unchanged) when returning to the
  customer and when persisting.
- Run `AgentChatService.SanitizeMessages` semantics where client-supplied history is
  accepted, to strip malformed/leaked tool plumbing (reuse the existing public
  method).

## 8. Comments & style

- Comment **why**, not what — match the dense rationale style in
  `SecuredAgentOrchestrator.cs` (e.g. explain short-circuits, security decisions,
  token-saving choices).
- XML `<summary>` on public types/methods, as in the existing assemblies.
- Keep methods focused; prefer small private helpers over deep nesting (mirrors the
  existing `ResolveExecutor`/`ProcessChat` decomposition).

## 9. Backward compatibility

- Do not touch `Server.Prompts` or `Server.Service` source in this work item.
- Do not change the internal `.aspx` callback behavior.
- Additive only: new project, new `.ashx`, new tables (guarded/idempotent SQL).

## 10. Definition of done (per change)

- Compiles against the Synergy `bin` references; DLL copies to the Synergy `BIN`.
- API-key auth enforced and tested (valid/invalid/inactive/missing).
- No provider keys/internal details in any response.
- SQL parameterized; queries scoped by customer.
- Internal flow regression-checked.
- Docs in this folder updated if contracts changed.
- **`CHANGELOG.md` entry added** (newest on top) — mandatory on every change
  (`CONTRIBUTING.md` §0).
