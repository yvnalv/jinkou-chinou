# TESTING — AIAgent Chat External API

How to verify the external API without breaking the internal/direct flow. The repo
has no unit-test project today, so testing is primarily **manual / integration via
HTTP** plus targeted harnesses. Add an xUnit/NUnit project only if approved (it must
also target .NET Framework 4.7).

---

> **QA / acceptance testing:** for the full ordered path from a clean environment
> (provisioning → provider Test connection → settings toggle → asking a chat question),
> use [`QA_TEST_PLAN.md`](QA_TEST_PLAN.md). The section below is the quick developer probe.

## 0. Quick manual smoke test (deployed external API)

Validates the deployed endpoint end‑to‑end. Current build uses **option 3c** (env from
the Synergy session), so the test must run **with a logged‑in Synergy session** on the
GLM server install (`Synergy_503`).

### Prerequisites
1. **Recycle** so the new DLL + `.ashx` load: run `iisreset` (or recycle the app pool).
   First request after this is slow (cold start) — give it time.
2. Confirm `GLMSysCIConnections` on `Synergy_503` has the **`SoftwareID=999`** row
   (`APIKey=test-key-001`, `Active=1`) and an active **`AzureOpenAI`** row.
3. Log in to the GLM server in a browser: `http://localhost/Synergy_503/docs/Portal.aspx`.

### Auth header
The `docs/` path is behind IIS **Windows Authentication**, which overwrites
`Authorization`. **Send the key as `X-API-Key`** (a header NTLM does not touch).
`Authorization: Bearer` only works on the future anonymous path.

### Run it (browser console — carries the session)
On the logged‑in Synergy page press **F12 → Console** and paste:

```js
// (1) valid key + chat  -> expect HTTP 200 + an assistant reply
(async () => {
  const r = await fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/chat', {
    method:'POST',
    headers:{ 'X-API-Key':'test-key-001', 'Content-Type':'application/json' },
    body: JSON.stringify([{ role:'user', content:'Hello, who are you? One short sentence.' }])
  });
  console.log('CHAT', r.status, await r.text());
})();

// (2) no key      -> expect 401 unauthorized
fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/chat',
  {method:'POST', headers:{'Content-Type':'application/json'}, body:'[]'})
  .then(r=>console.log('NO-KEY', r.status));

// (3) bad key     -> expect 401
fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/chat',
  {method:'POST', headers:{'X-API-Key':'wrong','Content-Type':'application/json'}, body:'[]'})
  .then(r=>console.log('BAD-KEY', r.status));

// (4) tool-result -> expect 501 not_implemented (Phase 3)
fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/tool-result',
  {method:'POST', headers:{'X-API-Key':'test-key-001','Content-Type':'application/json'}, body:'[]'})
  .then(async r=>console.log('TOOL-RESULT', r.status, await r.text()));
```

(If `/ai/chat` path routing misbehaves on your IIS, replace it with
`...GLMSysAIPlusAgentExternalAPI.ashx?action=chat`.)

### Interpreting the result of (1)
| Result | Meaning / next step |
|---|---|
| **200** + `{"conversationId":...,"messages":[{"role":"assistant","content":"…"}]}` | ✅ Phases 1–2 work end‑to‑end. |
| **401** `unauthorized` | key not sent as `X-API-Key`, or wrong/inactive `999` row. |
| **500** `server_error` | `Environment.Current()` returned null (the `.ashx` got no session) → move to **option 3b** (constructed env). |
| **502** `provider_error` | reached Azure OpenAI but the call failed → check the `AzureOpenAI` row / model / network on `Synergy_503`. |

### Notes
- The **chat widget still uses the internal flow** (`GLMSysAIPlusAgentClientCallBack.aspx`),
  not this API — repointing it is Phase 5. Use the console `fetch` above to exercise the
  external API directly.
- Anonymous IIS auth stays **off** for now (it would remove the session 3c relies on).

---

## 1. Test principles

- **Never regress the internal flow.** After any change, confirm the chat widget →
  `GLMSysAIPlusAgentClientCallBack.aspx` path still works.
- Test the **auth boundary** first and hardest — it is the security perimeter.
- Test the **suspend/resume** boundary (`/ai/chat` → `/ai/tool-result`) for correct
  `tool_call_id` binding.
- Use the seeded `SoftwareID=999` row (`APIKey=test-key-001`) on a dev GLM server.

---

## 2. Environments

| Env | Purpose | Notes |
|---|---|---|
| Dev GLM server | Host the `.ashx`; has `GLMSysCIConnections` with `SoftwareID=999` + `AzureOpenAI` rows | `C:\Exact Synergy Enterprise 503` per dev convention |
| Dev customer (or simulated) | Executes tools locally; or use a script that echoes tool results | Tool execution stays customer-side |
| Internal baseline | The existing `.aspx` flow | Regression reference |

---

## 3. Authentication tests (highest priority)

| Case | Request | Expected |
|---|---|---|
| Valid key | `Authorization: Bearer test-key-001` | 200, normal processing |
| Missing header | no `Authorization` | 401 `unauthorized` |
| Malformed header | `Authorization: test-key-001` (no `Bearer`) | 401 |
| Unknown key | `Bearer not-a-key` | 401 (no disclosure) |
| Inactive key | row with `Active=0` | 401 |
| Wrong `SoftwareID` | key from a non-999 row | 401 |
| Body `customerId` spoof | valid key + `"customerId":"other"` in body | identity from key only; body ignored |
| Cross-customer conversation | valid key A requests conversation owned by B | 404/403, no data |

---

## 4. Chat flow tests (`POST /ai/chat`)

| Case | Expected |
|---|---|
| Simple Q&A (no tool) | `messages:[{role:assistant, content:"..."}]` |
| Help/capabilities prompt | capabilities reply (pure short-circuit, no customer DB) |
| Prompt requiring a tool | `assistant.content=null` + `tool_calls[...]` returned verbatim |
| `search_documentation` triggered | handled server-side; **not** returned as a customer tool |
| Unknown `context` | 400 `bad_request` |
| Empty `messages` | 400 |

---

## 5. Tool-result flow tests (`POST /ai/tool-result`)

| Case | Expected |
|---|---|
| Single tool result | next assistant turn (reply / next tool / `[AGENT_DONE]`) |
| Multiple tool results in one batch | all pending ids answered → continues |
| Missing a pending `tool_call_id` | 400/409 (must answer all) |
| Wrong/unknown `tool_call_id` | 409 `conflict` |
| Result triggers another tool call | new `tool_calls` returned |
| Mutation success | reply ends with `[AGENT_DONE]` (mutation short-circuit parity) |
| Resume after app-pool recycle | state restored from store; binding intact (server-side state) |
| **Abandoned tool loop, then a NEW `/ai/chat`** (don't post the pending `/ai/tool-result`, send a new user question instead) | next turn responds normally — **no** provider 400 "tool_calls must be followed by tool messages…". `RunLoop` balances the thread (`EnsureToolCallBalance`); the dangling `assistant(tool_calls)` is dropped and the stored thread self-heals. (Regression for ARCHITECTURE.md R13.) |

**Binding check:** assert each `tool` result's `tool_call_id` matches an id from the
immediately preceding assistant `tool_calls` turn, across the HTTP boundary.

---

## 6. Conversation management tests

| Endpoint | Case | Expected |
|---|---|---|
| `GET /ai/conversation/{id}` | own conversation | history returned |
| `GET /ai/conversation/{id}` | other customer's id | 404/403 |
| `POST /ai/reset` | own conversation | cleared; idempotent on repeat |
| Idle expiry | conversation untouched past TTL | expired/closed; new turn starts fresh |

---

## 7. Isolation & quota tests

- Two customers (two `999` rows) run concurrent conversations → no cross-leak in
  state, history, or replies.
- Quota: exceed the per-key limit → 429 `quota_exceeded`; usage rows present in
  `GLMSysCILLMUsage`.
- Every conversation/state query is scoped by `CustomerConnectionID`.

---

## 8. Security / data-leak tests

- No response contains an AI-provider key, connection string, SQL, or stack trace.
- Invalid JSON → 400 with generic message (no internal detail).
- API keys never appear in logs.
- Content-filter prompt → friendly assistant message (not a 5xx), per
  `AgentChatService.IsContentFilterError`.

---

## 9. Regression (internal flow)

- Run a representative set through the chat widget (General lookup, create, update,
  delete, navigate, email, RuleMaint, WflRequest) against
  `GLMSysAIPlusAgentClientCallBack.aspx`.
- Confirm `Server.Prompts` / `Server.Service` binaries are unchanged (no source
  edits this WI).

---

## 10. Tooling

- Manual HTTP: `curl`, Postman, or a small C# console harness using `HttpClient`
  (target net47).
- Example:

```bash
curl -X POST https://glm-dev/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/chat \
  -H "Authorization: Bearer test-key-001" \
  -H "Content-Type: application/json" \
  -d '[{"role":"user","content":"help"}]'
```

- For provider-dependent assertions, prefer prompts with deterministic
  short-circuits (help, template list, farewell) to reduce LLM nondeterminism in CI.

---

## 11. Exit criteria per phase

- **Phase 1:** all auth tests pass; stub chat returns 200 for a valid key.
- **Phase 2:** non-tool prompts return correct replies; usage rows written.
- **Phase 3:** full round-trip tool tests pass with correct binding.
- **Phase 4:** conversation mgmt + isolation + quota tests pass.
- **All phases:** internal-flow regression green.
