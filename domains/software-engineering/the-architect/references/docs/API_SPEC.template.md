# API_SPEC — AIAgent Chat External API

External HTTP API hosted on the **GLM server** as a single `.ashx` handler
(`GLMSysAIPlusAgentExternalAPI.ashx`) that routes by sub-path/action. All requests
and responses are JSON (`Content-Type: application/json`). The endpoint is
**anonymous, Bearer-only** (no Synergy/NTLM login). Conversation state is
**server-side** (confirmed; `PRD.md` §8), so `conversationId` is server-issued.

> Message objects follow the OpenAI chat-completions shape already used internally
> by `AgentChatService` / `SecuredAgentOrchestrator` (`role`, `content`,
> `tool_calls`, `tool_call_id`, `name`). This keeps parity with the existing LLM
> core and the customer-side `IAgentToolExecutor` contract.

---

## 1. Authentication

> **Updated (2026-07):** validation now runs against **`GLMSysAIPlusProviderConnections`**
> (AIPlus-owned), not `GLMSysCIConnections`. The presented key's `KeyID` segment drives a
> single **indexed lookup**, then the stored key is decrypted and **constant-time compared**,
> with `Active = 1` and `ExpiryDate` enforced and `LastUsedDate` stamped. The
> scan-all-and-decrypt description below is the **superseded legacy** behaviour. See
> `API_KEY_GENERATION_PLAN.md` §0/§11 and `API_KEY_TESTING_GUIDE.md` §8.

Every endpoint requires the customer API key in **one of**:

```
X-API-Key: <api-key>            (preferred when the endpoint is behind IIS Windows Auth)
Authorization: Bearer <api-key> (anonymous production path)
```

> **Why `X-API-Key`:** when the `.ashx` sits behind IIS Windows Authentication, the
> NTLM/Negotiate handshake **overwrites the `Authorization` header**, destroying a
> Bearer token. A custom header the handshake does not touch is required in that mode.
> The handler checks `X-API-Key` first, then `Authorization: Bearer`. On the anonymous
> production path either works.

- Validated against `GLMSysCIConnections` (`SoftwareID = 999`, `Active = 1`). The key is
  **compared on its decrypted value**, not by SQL equality: when a connection is saved via
  the Synergy Connections UI the `APIKey` column is **encrypted at rest** (`Exact.Core.Crypt`)
  and encryption is non-deterministic, so the validator fetches the active `999` rows and
  matches the bearer against each key's **decrypted** value (falling back to the raw value
  for plaintext/SQL-seeded keys). The bearer is always the **plaintext** key. See `DATABASE.md` §1.3.
- The customer/Local-Agent side must therefore **send the plaintext key** — the callback
  (`GLMSysAIPlusAgentExternalCallback.ashx` → `TryGetExternalApi`) decrypts the stored
  `APIKey` before putting it in `X-API-Key`. This also makes auth work **across machines**:
  two installs encrypt with different machine keys but decrypt to the same plaintext.
- Customer identity is derived from the matched row's `ID`. **A `customerId` in the
  body or any other header is ignored.**
- Missing/malformed header → `403`. Valid format but unknown/inactive key → `403`.
  (**403, not 401** — the endpoint sits behind IIS Windows authentication, which owns `401`.
  Answering the API-key check with `401` makes browsers re-prompt for Windows credentials and
  .NET clients retry the NTLM handshake. Changed 2026-09-02.)
  Authenticated but not permitted for the target resource (e.g. another customer's
  conversation) → `403`.
- Fail closed on any auth error; never reveal whether a key "exists but is inactive"
  vs. "does not exist".

### Base path

```
POST  /ai/chat
POST  /ai/tool-result
GET   /ai/conversation/{id}
POST  /ai/reset
GET   /ai/ping
```

Routed inside `ProcessRequest(HttpContext)` by the trailing path segment
(`Request.PathInfo`, e.g. `.../GLMSysAIPlusAgentExternalAPI.ashx/ai/chat`); an
`?action=` query / body value is accepted as a fallback.

**Dev base URL (GLM server install `Synergy_503`):**

```
http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx
```

So `POST /ai/chat` in dev is:
`http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/chat`.
The customer app (install `Synergy_503_ClientAIPlusAgent`) calls this URL with the
Bearer key. See `DEPLOYMENT.md` §0 for the two-installation topology.

---

## 2. `POST /ai/chat`

Send a user message; receive a final assistant reply **or** structured tool-call
instructions for the customer to execute locally.

### Request

Headers: `Authorization: Bearer <key>`, `Content-Type: application/json`.

Body — the messages array (final element is the new user turn). A
`conversationId` is included once the server has issued one (server-side state
model); omit it on the first turn.

```json
{
  "conversationId": null,
  "context": "General",
  "messages": [
    { "role": "user", "content": "Delete all free fields" }
  ]
}
```

Minimal form (spec example) — the bare messages array is also accepted:

```json
[
  { "role": "user", "content": "Delete all free fields" }
]
```

> `context` selects the prompt/tool set (`General`, `WflRequest`, `RuleMaint`,
> `QuotationMaint`, `BusinessComponent`, `DocView`, …), mirroring the internal
> callback. Defaults to `General` if omitted. Customer-context inputs (rights/JWT,
> user name, Globe availability, page context) are passed per `PRD.md` §8.3 once
> that decision is made.

### Response — normal assistant reply

```json
{
  "conversationId": "0f6e...",
  "messages": [
    { "role": "assistant", "content": "Done. There were no free fields to delete." }
  ]
}
```

### Response — tool call(s) for the customer to execute

```json
{
  "conversationId": "0f6e...",
  "messages": [
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_xxx",
          "type": "function",
          "function": {
            "name": "DeleteFreeFields",
            "arguments": "{ \"entity_name\": \"FreeField\" }"
          }
        }
      ]
    }
  ]
}
```

- `tool_calls` are returned **verbatim** from the provider (ids preserved).
- The server has persisted the conversation up to and including this assistant turn
  and is now **awaiting** `/ai/tool-result`.
- `function.arguments` is a JSON **string** (provider convention), passed straight
  to `IAgentToolExecutor.Execute(name, argumentsJson, connectionId, entityId)` on
  the customer side.

> The bare-array response form from the spec
> (`[ { "role":"assistant", ... } ]`) is also supported; the object form adds
> `conversationId` for the stateful model.

---

## 3. `POST /ai/tool-result`

Return the result(s) of locally-executed tool call(s); receive the next assistant
turn.

### Request

```json
{
  "conversationId": "0f6e...",
  "messages": [
    {
      "role": "tool",
      "tool_call_id": "call_xxx",
      "name": "DeleteFreeFields",
      "content": "{ \"success\": true, \"deletedCount\": 10 }"
    }
  ]
}
```

- One `tool` message **per** `tool_call_id` returned by the preceding `/ai/chat`
  (or previous `/ai/tool-result`). All pending ids in a batch must be answered.
- `content` is the executor's result string (the same string `IAgentToolExecutor.Execute`
  returns internally).

### Behavior

1. Validate key → customer; load the conversation; verify it is awaiting these exact
   `tool_call_id`s for this customer.
2. Append the `tool` message(s); run `AgentChatService.Step` again.
3. Repeat for any **server-handled** tools in-process; if the provider requests more
   **customer** tools, return them (as in `/ai/chat`).

### Response

Same shape as `/ai/chat`: a final assistant reply, or another `tool_calls` batch, or
a terminal reply containing `[AGENT_DONE]`:

```json
{
  "conversationId": "0f6e...",
  "messages": [
    { "role": "assistant", "content": "Deleted 10 free fields. [AGENT_DONE]" }
  ]
}
```

> `[AGENT_DONE]` is the existing terminal marker emitted by the orchestrator's
> mutation/terminal short-circuits; clients should treat it as "turn complete".

---

## 4. `GET /ai/conversation/{id}`

Return the conversation history for the authenticated key/customer.

### Response

```json
{
  "conversationId": "0f6e...",
  "context": "General",
  "status": "active",
  "messages": [
    { "role": "user", "content": "Delete all free fields" },
    { "role": "assistant", "content": "Deleted 10 free fields. [AGENT_DONE]" }
  ]
}
```

- Returns only conversations owned by the authenticated customer
  (`CustomerConnectionID` match). Another customer's id → `404` (do not disclose
  existence).
- Internal `system` messages and raw tool plumbing may be summarized/omitted from
  the external view (decision in implementation).

---

## 5. `POST /ai/reset`

Reset/clear the conversation/session for the authenticated key/customer.

### Request

```json
{ "conversationId": "0f6e..." }
```

Omit `conversationId` to reset the customer's default/current session (semantics
finalized with the state decision).

### Response

```json
{ "status": "reset", "conversationId": "0f6e..." }
```

- Closes/clears server-side state for that conversation. Idempotent.

---

## 5a. `GET /ai/ping`

Lightweight health + auth probe: confirms the endpoint is reachable and the API key is
accepted, without exercising chat. Call it manually with `X-API-Key` (curl / browser
console) — `200 {"status":"ok"}` on a valid key, `403` otherwise.

> **Deprecated caller (retained for history):** ping was originally added for the ConnectIt
> **AIAgent** provider (`GLMSys.CI.AIAgent.Provider`, SoftwareID 999) **"Test connection"**
> button. That provider dependency is **retired** (2026-08-26) — the API key is now provisioned
> via the license-driven `GLMSysAIPlusProviderConnections` flow, so no ConnectIt AIAgent
> connection/Test-connection is involved. The route itself stays as a generic health check.
> The paragraph below describes the old provider behaviour and is kept for reference only.

### Request

No body. The API key is sent the usual way (`X-API-Key: <key>`, or
`Authorization: Bearer <key>`). Authentication runs **before** routing, so a
missing/invalid key is rejected with `403` exactly as for the other routes.

### Response

```json
{ "status": "ok" }
```

- `200` with the above body when the key is valid (and reachable).
- `403` (error envelope) when the key is missing/invalid/inactive.
- `405` if called with a method other than `GET`.

The provider's `Connection.Connect()` issues this probe with
`UseDefaultCredentials` (to pass IIS Windows auth on the GLM server, mirroring the
customer Local Agent callback) and treats `200` as success, `403` as "key
rejected", and anything else/unreachable as a connection failure.

---

## 6. Error envelope

Non-2xx responses use a consistent JSON shape; never leak stack traces, SQL, or
provider details.

```json
{
  "error": {
    "code": "forbidden",
    "message": "Invalid or missing API key."
  }
}
```

| HTTP | `code` | When |
|---|---|---|
| 400 | `bad_request` | Malformed JSON, missing `messages`, unanswered `tool_call_id`s, unknown `context`. |
| 403 | `forbidden` | Missing/invalid/inactive API key. (Was `401`/`unauthorized` before 2026-09-02.) |
| 403 | `forbidden` | Authenticated but not allowed (e.g. another customer's conversation). |
| 404 | `not_found` | Conversation id not owned by this customer / does not exist. |
| 409 | `conflict` | Conversation not awaiting tool results / wrong lifecycle state. |
| 429 | `quota_exceeded` | Rate limit or token quota exceeded for this key. |
| 500 | `server_error` | Unexpected server error (generic message only). |
| 502 | `provider_error` | AI provider call failed (content filter handled gracefully — see below). |

> Azure OpenAI **content-filter** rejections are already mapped to a friendly
> message by `AgentChatService.ExtractReplyText` / `IsContentFilterError`; surface
> that friendly text as a normal assistant reply rather than a 5xx where possible.

---

## 7. Tool-call contract (customer side)

For each returned tool call, the customer Local Agent:

1. Reads `function.name` and `function.arguments` (JSON string).
2. Calls the existing executor:
   `result = IAgentToolExecutor.Execute(name, argumentsJson, connectionId, entityId)`.
3. Returns `{ "role":"tool", "tool_call_id": <id>, "name": <name>, "content": result }`
   to `/ai/tool-result`.

The function names match the existing tool JSON in `Server.Prompts\Tools\*.json`
(e.g. `read_records`, `create_record`, `update_record`, `delete_record`,
`query_entity_data`, `get_entity_metadata`, `navigate_to`, plus context-specific
tools). **`search_documentation` is handled on the server and never returned.**

---

## 8. Worked example — full round trip

```
1) POST /ai/chat
   Authorization: Bearer test-key-001
   [ { "role":"user", "content":"Delete free field 'Legacy Code'" } ]

   → 200
   { "conversationId":"0f6e...",
     "messages":[ { "role":"assistant","content":null,
       "tool_calls":[ { "id":"call_1","type":"function",
         "function":{ "name":"delete_record",
           "arguments":"{\"entity_name\":\"FreeField\",\"record_id\":\"123\"}" } } ] } ] }

2) (customer executes delete_record locally → "Deleted FreeField 123 successfully.")

   POST /ai/tool-result
   Authorization: Bearer test-key-001
   { "conversationId":"0f6e...",
     "messages":[ { "role":"tool","tool_call_id":"call_1",
       "name":"delete_record","content":"Deleted FreeField 123 successfully." } ] }

   → 200
   { "conversationId":"0f6e...",
     "messages":[ { "role":"assistant",
       "content":"Deleted free field 'Legacy Code'. [AGENT_DONE]" } ] }
```
