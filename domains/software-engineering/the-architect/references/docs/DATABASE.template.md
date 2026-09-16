# DATABASE — AIAgent Chat External API

Covers the existing configuration/usage tables the external API depends on, and the
**proposed** new tables for conversation state. New tables are proposals pending the
state-ownership decision in `PRD.md` §8.

> All access uses `Exact.Data.QueryBuilder` + `EDLConnection` with **parameters**.
> Never concatenate request input into SQL.

---

## 1. `GLMSysCIConnections` (existing — ConnectIt framework)

The central connection/config table. Created and owned by the GLMSys ConnectIt
framework (not by this addon's `Setup\sql\GLMSysAIPlusAgent.sql`). Rows are keyed by
`SoftwareID` (see `GLMSysCISoftwares`) and an `Active` flag.

Columns referenced by existing code (`ConnectionHelper.cs`, `AIAgentHelper.cs`,
`AgentChatService.cs`, `SecuredAgentOrchestrator.cs`):

| Column | Type (observed) | Use |
|---|---|---|
| `ID` | GUID | Connection id; **doubles as the customer/account identifier** for the API-key row. |
| `SoftwareID` | int | Discriminates product/provider. `AzureOpenAI`, `ExactGlobe`, … (enum `GLMSys.CI.Data.Application.Software`); **`999` = external AI Agent API**. |
| `Active` | bit | `1` = usable. Disable a key/connection by setting `0`. |
| `APIUri` | nvarchar | Endpoint URL (for the `999` row, the `.ashx` URL). |
| `APIKey` | nvarchar | Bearer key (for the `999` row, the customer's API key). **Encrypted at rest** when saved via the Connections UI (`Exact.Core.Crypt`); validated/sent by its **decrypted** value (§1.3). |
| `UserName` | nvarchar | Optional **Synergy credential** for outbound HTTP auth from the customer bridge (the code's `windowsUser` naming is a misnomer — it's a Synergy login, not a Windows/domain account). Stored as `domain\username` (e.g. `radium\Client`). Read by `TryGetExternalApi`; used to build `NetworkCredential` in `CallExternal`. Leave NULL for API-key-only auth. |
| `Password` | nvarchar | Optional **Synergy credential** password (pair with `UserName`; code's `windowsPassword`). **Encrypted at rest** the same way as `APIKey`; decrypted by `DecryptApiKey` before use. |
| `SQLServerName` | nvarchar | Used for Globe launch config. |
| `SQLDatabaseName` | nvarchar | Used for Globe launch config. |

> Additional columns exist (framework-managed). Confirm the exact column that
> stores the **customer/account** linkage for multi-customer key issuance
> (`PRD.md` §8.2) before implementation.

### 1.1 Roles of `SoftwareID` rows for this feature (on the GLM server)

| `SoftwareID` | Meaning | Who reads it |
|---|---|---|
| `AzureOpenAI` (enum) | GLM's AI-provider credentials | `AgentChatService` (server only) — **never exposed** |
| `999` | External API customer key(s) | `ExternalApiKeyValidator` on each request |
| `ExactGlobe` (enum) | Globe connection (customer side) | customer-side executors/help |

### 1.2 Example `999` row

```
ID:        72AEDC9B-ECFF-4EF0-89F3-DA1113D623F7
SoftwareID: 999
Active:    1
APIUri:    http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx
APIKey:    test-key-001
```

### 1.3 API-key validation (decrypt-compare — NOT SQL equality)

> **Updated (2026-07):** the validator was repointed to **`GLMSysAIPlusProviderConnections`**
> with a `KeyID` **indexed lookup** + constant-time compare + `Active`/`ExpiryDate` enforcement
> + `LastUsedDate` stamp (see `API_KEY_GENERATION_PLAN.md` §0/§11). The O(n) scan-and-decrypt
> below is the **superseded legacy** behaviour, kept for history.

> **Updated (2026-07-22) — license-driven provisioning:** `GLMSysAIPlusProviderConnections` gained a
> **`CustomerID nvarchar(64)`** column (= Synergy `cmp_wwn`) so the AIPlus **license generator** can
> upsert the customer's `999` row when the "Agent" feature is licensed. The license carries the key
> material (RC2-encoded) and the customer's license-apply materializes/refreshes its own row
> (re-encrypting `APIKey` with its own `conn`). Key lifecycle is driven from the license page:
> **Issue** (first Add), **Preserve** (re-save, key untouched), **Rotate** (new key), **Revoke**
> (`Active=0` + `RevokedDate`/`Revoker`, immediate), **Re-enable** (`Active=1`). Enforcement is
> unchanged (this validator). Full detail: `../AIPlus-Agent-API-Key-License-Integration-Plan.md`.

`APIKey` is **encrypted at rest** when a connection is saved via the Synergy Connections
UI (`ConnectionMaintPage` → `Exact.Core.Crypt.Encrypt`), and encryption is
**non-deterministic**, so the key **cannot** be matched with `WHERE c.APIKey = @key`.
The validator fetches the active `999` rows and compares the (plaintext) bearer to each
key's **decrypted** value — with a fallback to the raw value for plaintext/SQL-seeded keys:

```csharp
var qb = new QueryBuilder(conn);
qb.AppendSelect("c.ID, c.APIKey");
qb.AppendFrom("GLMSysCIConnections c");
qb.AppendWhere("c.SoftwareID", 999);   // const int ExternalAgentApiSoftwareId = 999
qb.AppendWhere("c.Active", 1);

object[,] rows = conn.Query(qb) as object[,];
foreach (row) {
    string stored = rows[i, 1];
    string dec = try { Crypt.Decrypt(stored, conn) } catch { null }; // plaintext key → throws
    if (bearer == stored || (dec != null && bearer == dec))          // match decrypted OR raw
        return rows[i, 0]; // ID = customer identity
}
```

No match → reject (`401`). Match → customer identity = `ID`.

> **Senders must transmit the plaintext key.** The Local-Agent callback
> (`GLMSysAIPlusAgentExternalCallback.ashx` → `TryGetExternalApi`) decrypts the stored
> `APIKey` before sending it as `X-API-Key`; the provider Test-connection probe sends
> `Connection.APIKey`, which Synergy already decrypts on load. Comparing on the **decrypted**
> value is also what makes auth work **across machines** (different machine ciphers, same plaintext).

> **Note:** `999` is not a named member of `GLMSys.CI.Data.Application.Software`;
> use the literal/`const`. `ConnectionHelper.GetConnectionId(conn, softwareId)`
> takes an int but only matches `SoftwareID`+`Active` and returns the id — the
> external validator needs the additional `APIKey` predicate, so add a dedicated
> method rather than reusing `GetConnectionId`.

---

## 2. `GLMSysCILLMUsage` (existing — metering)

Token-usage table already present, with a search page
`Setup\docs\GLMSysCILLMUsageSearch.aspx`. Columns include `SoftwareID`, `Prompt`,
`Response`, `ResponseJson`, `Model`, `PromptTokens`, `CompletionTokens`, `CachedTokens`,
`Creator`, `Created`, and — designed as optional correlation ids —
**`ConversationId UNIQUEIDENTIFIER NULL`** and **`SessionId NVARCHAR(100) NULL`**
(with an index on `ConversationId`). Defined in `ConnectIt\Setup\sql\GLMSysCI148To149.sql`.

- The ConnectIt **AzureOpenAI provider** writes **one row per provider call** (so a single
  chat turn produces several: intent classification + main reply + each tool round).
- **Per-conversation correlation (implemented 2026-06-05):** the provider stamps
  `ConversationId` (and `SessionId`) on each row by reading
  `env.Cache["GLMSysCILLMUsageConversationId"]` / `["GLMSysCILLMUsageSessionId"]`. The external
  API handler (`ExternalAgentApiHandler`) sets those keys to `conv.Id` / `conv.SessionId` before
  orchestration and clears them in `finally`. `ConversationId` matches
  `GLMSysAIPlusAgentConversation.ID`, so cost per room =
  `SUM(PromptTokens+CompletionTokens) WHERE ConversationId = @id`. Best-effort: non-agent LLM
  calls leave the columns NULL (unchanged).
- `ChatStepResult` (in `Server.Service`) does **not** expose token counts, and is not edited —
  the usage row (incl. tokens) is written entirely inside the provider, so no `Server.Service`
  change is needed for metering.

---

## 3. `Setup\sql\GLMSysAIPlusAgent.sql` (existing addon tables)

This addon's own SQL currently creates:

- `GLMSysAIPlusAgentScheduledTask` — Scheduler (Hangfire) recurring tasks.
- `GLMSysAIPlusActionToken` — HMAC-signed, single-use action-link tokens (email
  actions); `SoftwareID` default 6 (Globe) per its comment.

It does **not** create `GLMSysCIConnections` or `GLMSysCILLMUsage` (framework
tables). New external-API tables (below) should be added here behind existence
checks, following the same idempotent pattern used by the existing script.

---

## 4. Conversation state tables (Phase 3) — DECIDED

Server-side state is the **confirmed** model (decision 2026-06-02, `PRD.md` §8.1).
These tables are created on the **GLM** Synergy DB. Names follow the addon prefix
convention.

### 4.1 `GLMSysAIPlusAgentConversation`

| Column | Type | Notes |
|---|---|---|
| `ID` | uniqueidentifier | Conversation id (returned to the client; used by `/ai/conversation/{id}`). |
| `CustomerConnectionID` | uniqueidentifier | FK → `GLMSysCIConnections.ID` of the validated `999` key. **Isolation key.** |
| `Context` | nvarchar(64) | Agent context (e.g. `General`, `WflRequest`). |
| `Status` | tinyint | e.g. 0=active, 1=awaiting tool result, 2=closed. |
| `CreatedUtc` | datetime | Creation time. |
| `LastActivityUtc` | datetime | For idle expiry. |

### 4.2 `GLMSysAIPlusAgentConversationMessage`

| Column | Type | Notes |
|---|---|---|
| `ID` | uniqueidentifier | PK. |
| `ConversationID` | uniqueidentifier | FK → conversation. |
| `Seq` | int | Order within the conversation. |
| `Role` | nvarchar(16) | `system` / `user` / `assistant` / `tool`. |
| `Content` | nvarchar(max) | Message content (may be null for tool-call assistant turns). |
| `ToolCallsJson` | nvarchar(max) | Raw `tool_calls` JSON for assistant turns (preserves `id`s). |
| `ToolCallID` | nvarchar(128) | For `tool` messages — binds result to the call. |
| `Name` | nvarchar(128) | Tool/function name for `tool` messages. |
| `CreatedUtc` | datetime | Timestamp. |

**Why persist the raw `tool_calls` and `tool_call_id`:** the provider requires that
each `tool` result reference the exact `tool_call_id` from the assistant turn that
requested it. Because that boundary now spans two HTTP requests
(`/ai/chat` → `/ai/tool-result`), the server must store the assistant `tool_calls`
turn so the resumed turn binds correctly. (In the internal flow this lives only in
the in-memory `messages` array within one `ProcessChat` call.)

### 4.2a AS IMPLEMENTED (2026-06) — single table + JSON thread

The shipped implementation uses **one** table, not the two above: the full thread is
stored as a JSON blob on the conversation row (the separate
`GLMSysAIPlusAgentConversationMessage` table in §4.2 was **not** built). Actual columns of
`GLMSysAIPlusAgentConversation` (see `Setup\sql\GLMSysAIPlusAgent.sql`):

| Column | Type | Notes |
|---|---|---|
| `ID` | uniqueidentifier | conversation id (a "chat room") |
| `CustomerConnectionID` | uniqueidentifier | isolation key (the validated `999` row) |
| `SessionID` | uniqueidentifier NULL | optional browser/widget session |
| `Context` | nvarchar | agent context |
| `Messages` | nvarchar(max) | **the full thread as JSON** (system + user + assistant + raw `tool_calls` + tool results) — preserves the `tool_call_id` binding across the `/ai/chat`→`/ai/tool-result` boundary |
| `Status` | tinyint | 0 active, 1 awaiting_tool_result, 2 closed |
| `Created` / `Modified` | datetime | timestamps |

**One chat room = one row, threaded by the widget (2026-06-05):** the widget holds the
`conversationId` from the first reply and sends it on every subsequent message in the same room
(external mode), so the row is **updated in place** (`Messages` grows, `Modified` advances) instead
of creating a new row per message. "New chat" drops the id → a new room. The id is currently
**in-memory only** (a page reload starts a new room); persisting it in `sessionStorage`/`localStorage`
is the prerequisite for a future "resume / chat history" UI (see `ROADMAP.md`).

**Thread integrity (2026-06):** because `Messages` keeps `tool_calls`/`tool` across turns, an
abandoned tool loop can leave a dangling `assistant(tool_calls)` with no matching `tool` responses.
`ExternalAgentOrchestrator.RunLoop` calls `EnsureToolCallBalance` before every LLM `Step` — it drops
unanswered `assistant(tool_calls)` and orphan `tool` messages so the provider never sees an unbalanced
thread, and rewrites `Messages` in place so existing broken rows self-heal on the next turn (see
ARCHITECTURE.md R13). The provider requires every assistant `tool_calls` to be followed by a `tool`
message for each `tool_call_id`.

### 4.3 Indexes & isolation

- Index `GLMSysAIPlusAgentConversation(CustomerConnectionID, LastActivityUtc)`.
- Index `GLMSysAIPlusAgentConversationMessage(ConversationID, Seq)`.
- **Every** read/write filters by `CustomerConnectionID` derived from the validated
  key — never by a client-supplied id alone. A `GET /ai/conversation/{id}` for a
  conversation owned by another customer returns `404`/`403`, never the data.

### 4.4 Rejected alternative: client-holds-history

Not chosen. (It would need no new tables, but the client would have to faithfully
round-trip assistant `tool_calls` messages and `/ai/conversation/{id}` / `/ai/reset`
would be trivial/no-ops.) Kept here only as rationale; see `ARCHITECTURE.md` §4.4.

---

## 5. Data-handling guardrails

- Parameterize all SQL (`QueryBuilder.AppendWhere(col, value)`).
- API keys: never log; compare via parameterized query; consider hashing at rest
  (Phase 7).
- Conversation content may contain customer business data — store only on the GLM
  server with the same protection as other customer data; honor retention/expiry.
- Scope every query by the validated customer connection id (multi-tenant safety).
