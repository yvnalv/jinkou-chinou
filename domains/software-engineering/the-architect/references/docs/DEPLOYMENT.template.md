# DEPLOYMENT — AIAgent Chat External API

How the external API is built, deployed, and configured on the **GLM server**. It
mirrors the existing addon's deploy model (DLLs → Synergy `BIN`, web files →
`docs\`), adding one `.ashx` and (optionally) new tables.

---

## 0. Dev/test topology (two Synergy installations on localhost)

The external API is developed and tested with **two separate Synergy Enterprise 503
installations** on the same machine — one acting as the **GLM server** (hosts the
external API), the other as the **external customer app** (executes tools locally).
This mirrors production where the two are different servers.

| Role | Install folder | Portal URL | App / DB |
|---|---|---|---|
| **GLM server** (hosts external API) | `C:\Exact Synergy Enterprise 503` | `http://localhost/Synergy_503/docs/Portal.aspx` | `Synergy_503` |
| **External customer app** (Local Agent / tool execution) | `C:\Exact Synergy Enterprise 503_ClientAIPlusAgent` | `http://localhost/Synergy_503_ClientAIPlusAgent/docs/Portal.aspx` | `Synergy_503_ClientAIPlusAgent` |

Consequences for this work item:

- The external API endpoint is deployed to the **GLM server** install:
  `C:\Exact Synergy Enterprise 503\docs\GLMSysAIPlusAgentExternalAPI.ashx`, reachable at
  **`http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx`**.
  This matches the seeded `GLMSysCIConnections` (`SoftwareID=999`) `APIUri`.
- The new DLL (`GLMSys.AIPlus.Agent.Server.External.dll`) and the reused server
  assemblies (`Server.Service`, `Server.Prompts`, `Shared`) must be in the **GLM
  server** install's `BIN\` (the post-build copies to `C:\Exact Synergy Enterprise 503\BIN\`).
- `GLMSysCIConnections` rows for the API (`SoftwareID=999` customer key,
  `SoftwareID=AzureOpenAI` provider creds) live in the **GLM server** DB
  (`Synergy_503`).
- The **customer app** (`...503_ClientAIPlusAgent`) calls the GLM server's `.ashx`
  with `Authorization: Bearer <key>` and executes tools against **its own** DB
  (`Synergy_503_ClientAIPlusAgent`). The GLM server never touches the customer DB.
- The environment-acquisition seam (`GlmServerEnvironmentProvider`) must yield an
  `Exact.Core.Environment` bound to the **GLM server** install (`Synergy_503`).

> Note: a previous, separate external-AI-Agent attempt exists outside the repo. Per
> the owner's instruction it is **not** used as a reference here; ignore those old
> files (ask the owner before touching them).

---

## 0c. Prerequisites — ConnectIt on the customer Synergy (REQUIRED for CRUD)

> **ConnectIt must be installed on every customer Synergy that runs the AI agent.**
> The agent performs all CRUD (create/update/delete) through the `GLMSys.CI` (ConnectIt)
> provider, which on write routes through Synergy's OData endpoint
> (`services/Exact.Entity.Rest.svc/`). That server-side write pipeline requires ConnectIt
> to be **installed and registered** on the customer Synergy so it can resolve the
> `GLMSys.CI.Data.Connection`.

- **Symptom when missing:** reads work (search/metadata/list), but create/update/delete fail
  with `InternalServerError` →
  `Unable to cast object of type 'Exact.Services.MetaModel.Entity.Data.MetadataEntity' to type 'GLMSys.CI.Data.Connection'`.
  This affects **both** the internal `.aspx` callback and the external `.ashx` callback —
  it is an install/registration issue, not an AI-agent code issue.
- **Fix:** install ConnectIt on the customer Synergy exactly as on the GLM server, then CRUD works.
- **Verified 2026-06-04:** installing ConnectIt on `Synergy_503_ClientAIPlusAgent` made
  "create kanban request" succeed end-to-end through the external flow.

## 0d. The AIAgent ConnectIt provider (`GLMSys.CI.AIAgent.Provider`)

> **⚠️ DEPRECATED / RETIRED (2026-08-26) — retained for history.** The external API **no longer
> depends on this provider**. The customer API key is provisioned by the license-driven flow into
> **`GLMSysAIPlusProviderConnections`** (`SoftwareID=999`), which the validator reads directly, so the
> ConnectIt-managed `GLMSysCIConnections` 999 connection and its "Test connection" are not required.
> You do **not** need to deploy `GLMSys.CI.AIAgent.Provider.dll` or create a `ProviderName="AIAgent"`
> row. `GET /ai/ping` remains as a manual health probe. This section is kept for reference to the old
> setup. (Scope: only the *AIAgent* provider is retired — the AzureOpenAI LLM provider and customer
> CRUD providers still use ConnectIt. See CHANGELOG 2026-08-26.)

So the `SoftwareID=999` connection can be **created and "Test connection"-ed via the Synergy
Provider/Connections UI** (not hand-inserted by SQL), the AI Agent is registered as a ConnectIt
provider. Synergy loads a provider's implementation by reflection from `GLMSysCISoftwares.ProviderName`
(`assembly = "GLMSys.CI." + ProviderName + ".Provider"`), so two things must line up:

- **`GLMSysCISoftwares` row** with **`ProviderName = "AIAgent"`** (API-key connection type;
  `APIUri` + `APIKey` fields visible). Currently created via the Provider UI; a repeatable seed
  script is a deferred follow-up.
- **`GLMSys.CI.AIAgent.Provider.dll`** deployed to the **customer** Synergy `bin\` (where Test
  connection runs) — and to the GLM `bin\` if AIAgent connections are also created there. (The
  ConnectIt project post-build copies to `C:\Exact Synergy Enterprise 503\BIN\`; copy to the
  customer bin too.) Missing DLL → *"Could not load file or assembly 'GLMSys.CI.AIAgent.Provider'"*.

**Test connection** calls the GLM API's **`GET /ai/ping`** route (added in `Server.External`) with
the API key + Windows default credentials (`UseDefaultCredentials = true` inside the compiled
provider): `200` = reachable + key accepted, `401` = key rejected. This means ping requires either
a domain pool identity on the customer IIS or anonymous auth enabled on the GLM handler path — see
§4 and §2b-credentials below.
The provider is **connection-only** — chat itself flows through the `.ashx` (`/ai/chat`, …), not
ConnectIt entity CRUD. See `docs/API_SPEC.md` §5a.

---

## 1. Build model (existing, reused)

- Each project is a .NET Framework 4.7 class library built in Visual Studio /
  MSBuild against DLL references in `C:\Exact Synergy Enterprise 503\bin\`.
- Post-build event copies the output DLL to `C:\Exact Synergy Enterprise 503\BIN\`:
  `copy "$(TargetPath)" "C:\Exact Synergy Enterprise 503\BIN\" /Y`.
- Web assets (`.aspx`, `.ashx`, `.js`, `.css`, images) live under `Setup\docs\` and
  are deployed to the Synergy site's `docs\` folder.

The new project (`GLMSys.AIPlus.Agent.Server.External`) follows the same pattern:
its DLL copies to `BIN\`; its `GLMSysAIPlusAgentExternalAPI.ashx` deploys to `docs\`.

---

## 2. Artifacts to deploy — full manifest (GLM server vs customer app)

The external flow spans **two** Synergy installs. The GLM server hosts the API and runs
the LLM; the customer app hosts the widget and executes tools locally. Below is exactly
what each side needs (this is the external-API setup on top of a normal AI Plus Agent install).

### 2a. GLM server (`Synergy_503`) — hosts the external API + runs the LLM

**DLLs → `…\Synergy_503\bin\`**
| DLL | Purpose |
|---|---|
| `GLMSys.AIPlus.Agent.Server.External.dll` | the API handler (`.ashx` class) + orchestrator (NEW project) |
| `GLMSys.AIPlus.Agent.Server.Service.dll` | chat service, intent classifier, capabilities builder, etc. |
| `GLMSys.AIPlus.Agent.Server.Prompts.dll` | prompt builders + tool definitions |
| `GLMSys.AIPlus.Agent.ExactGlobe.Server.dll` | **Globe product only** — Globe system prompt + tool definitions (`GlobePromptAssembler`, embedded resources). From the **AIPlusAgentEG** repo; self-contained (references only stock DLLs, no extra companion files). Required whenever any `999` key has `Product='globe'`. See §2c and `GLOBE_PROFILE_POINTER.md`. |
| `GLMSys.AIPlus.Agent.Shared.dll` | entity registry, locale loader, JWT, template registry |
| `GLMSys.CI.*` (ConnectIt) + AzureOpenAI provider | the LLM call runs here |

**Web files → `…\Synergy_503\docs\`**
| File | Purpose |
|---|---|
| `GLMSysAIPlusAgentExternalAPI.ashx` | the API endpoint (WebHandler → `ExternalAgentApiHandler`) |
| `GLMSysAIPlusAgentLocale_{EN,DE,ES,FR,NL}.json` | **required** — capabilities/help/template-list detection |
| `GLMSysAIPlusAgentTemplates_{EN,…}.json` | template locale labels (template-list / template-query) |

**Database (`Synergy_503`)**
- `GLMSysAIPlusAgentConversation` table — run `Setup\sql\GLMSysAIPlusAgent.sql` (idempotent).
- `GLMSysCIConnections`: the **AzureOpenAI** row (LLM creds) **and** the **SoftwareID=999** row(s)
  holding the customer API key, `Active=1`.
- **ConnectIt installed** (needed for the AzureOpenAI provider).

**IIS / config**
- IIS auth for the `.ashx`: **currently must be Windows auth with a mapped Synergy service-account
  app pool** — the intended Anonymous + key-only mode is **not yet viable** (env-init throws; see §A1
  reality-check below and `07-KNOWN-ISSUES.md` §A1). Dev works via the `X-API-Key` header over the
  logged-in session.
- AppPool identity = a **mapped Synergy resource** with DB-config access (an unmapped account drops to
  the broken anonymous env construction — see §A1).
- ⚠️ JWT secret is still hardcoded `"MySecret"` — pre-prod hardening TODO.

### 2b. Customer app (`Synergy_503_ClientAIPlusAgent`) — executes tools + hosts the widget

**DLLs → `…\bin\`**
| DLL | Purpose |
|---|---|
| `GLMSys.AIPlus.Agent.Client.Core.dll` | executors base, `EntityRecordService`, `ChatResponseEnricher`, `AgentLogger` |
| `GLMSys.AIPlus.Agent.Client.dll` | domain executors incl. `GeneralToolExecutor` |
| `GLMSys.AIPlus.Agent.Client.PageExtension.dll` | widget injection / `AIAgentHelper` |
| `GLMSys.AIPlus.Agent.Shared.dll` | shared registry/helpers |
| ⭐ **ConnectIt — fully INSTALLED** | **REQUIRED for all CRUD** (see §0c). Not just the DLLs — the registration. |

**Web files → `…\docs\`**
| File | Purpose |
|---|---|
| `GLMSysAIPlusAgentExternalCallback.ashx` | the widget→GLM bridge (calls the GLM API, executes tool_calls locally) |
| `GLMSysAIPlusAgentChatEngine.js` (+ widget CSS/assets) | chat widget (incl. conversationId threading) |
| `GLMSysAIPlusAgentClientCallBack.aspx` | still used for non-chat actions (apply / drilldown / email) |

**Bin (`…\bin\`)**
- ~~`GLMSys.CI.AIAgent.Provider.dll` — the ConnectIt AIAgent provider~~ **(retired 2026-08-26 — no
  longer required; see §0d).** The key comes from `GLMSysAIPlusProviderConnections`, not a ConnectIt
  connection. (ConnectIt itself is still required on the customer for CRUD — this only drops the
  *AIAgent* provider DLL.)

**Database (`Synergy_503_ClientAIPlusAgent`)**
- ~~`GLMSysCISoftwares` row with `ProviderName="AIAgent"`~~ **(retired 2026-08-26 — no longer required;
  see §0d).** Historically this backed the `SoftwareID=999` connection in the Connections UI with
  `VisibleFieldUserName=1`/`VisibleFieldPassword=1`. The license-driven `GLMSysAIPlusProviderConnections`
  row replaces it.
- `GLMSysCIConnections` **SoftwareID=999** row: `APIUri` = the GLM `…GLMSysAIPlusAgentExternalAPI.ashx`
  endpoint, `APIKey` = the key (**must match** the GLM server's 999 key), `Active=1`.

**§2b-credentials. Windows credentials on the SoftwareID=999 row (optional)**

When the customer-side IIS app pool runs as `ApplicationPoolIdentity` (no domain account), the
bridge's `UseDefaultCredentials` has no network credentials and NTLM to the GLM server fails.
Set these two fields on the 999 connection row via the Connections UI to supply explicit credentials:

| Field | Value | Notes |
|---|---|---|
| `UserName` | `domain\username` (e.g. `radium\Client`) | Parsed as `domain\user` automatically |
| `Password` | account password | Encrypted at rest; decrypted by `TryGetExternalApi` the same way as `APIKey` |

Leave both empty to skip Windows auth (API key only) — works when GLM server allows anonymous auth.
The `GLMSysCISoftwares` row must have `VisibleFieldUserName=1` and `VisibleFieldPassword=1` (already
set on the client DB) for these fields to appear in the Connections UI.
- `GLMSysAIPlusLog` + `GLMSysAIPlusFieldMismatch` tables — created by `Setup\sql\GLMSysAIPlusAgent.sql`
  (diagnostic logging; best-effort, agent works without them).
- ConnectIt's own config (ExactSynergy self-connection, entity registrations) from its install.

**Config / setting — `GLMSysAIPlusAgentUseExternalApi`**
- Controls whether the widget's chat routes to the **external** callback (`'1'`) or the **internal**
  callback (`'0'`/absent). All non-chat widget actions always use the internal callback.
- Stored in **`BacoSettings`**: `SettingType=0, SettingGroup='AIPlus', SettingName='GLMSysAIPlusAgentUseExternalApi',
  StringValue='1', Division=0`. **`Division` must be `0`** (global) — a `NULL` Division is not matched.
- **Seeded by the install script** (`Setup\sql\GLMSysAIPlusAgent.sql`, default `'0'`). To enable, flip the
  **"Use External API" toggle** on the **Agent Settings page** (`GLMSysAIPlusAgentSettings.aspx` → *API Routing*
  card; admin-only), or set `StringValue='1'` directly (the script also has an inline `UPDATE` snippet).
- **Toggle is gated on the external connection.** The toggle is disabled (greyed, forced OFF, with a note)
  unless a `GLMSysCIConnections` row with `SoftwareID=999` **exists** (existence only — inactive/misconfigured
  still counts; see §0d). `save_settings` also coerces the value to `0` when no 999 row exists, so a stored
  `1` self-heals if the connection is later removed.
- The Settings page writes the value through the internal callback's `save_settings` action, which writes
  **the `BacoSettings` table directly** (`UPDATE`, `INSERT` if no row) — `env.set_Setting` alone only updates
  the per-session cache and would leave the table (and therefore routing) unchanged. `get_settings` likewise
  reads the value with a **direct `BacoSettings` query**, so the toggle reflects the live row even after an
  `iisreset` (a per-session `env.get_Setting` snapshot would show a stale value).
- `AIAgentHelper.ResolveExternalChatUrl` reads this **directly from `BacoSettings`** (not `env.get_Setting`),
  so a value changed by SQL or the toggle takes effect without a re-login.
- **No page reload needed (dynamic routing).** The chat engine resolves the route **lazily at the start of
  each conversation** via the internal callback's **`get_route`** action (`ensureChatRoute` in
  `GLMSysAIPlusAgentChatEngine.js`), then keeps it fixed for that conversation (thread continuity) and
  re-resolves on **New chat**. So toggling the setting applies on the next conversation — no refresh. The
  page-rendered `_aiAgentConfig.chatUrl` is now only the initial fallback if `get_route` fails.
- Resolution is centralized in `AIAgentHelper.BuildConfigScript`, so **all** widget paths honor it
  (portal widget, standalone chat page, and per-record page extensions).

### 2b-note. Widget JS caching (operational gotcha)
`GLMSysAIPlusAgentChatEngine.js` is injected with **no cache-busting** query string
(`~/docs/GLMSysAIPlusAgentChatEngine.js` in `AIAgentHelper.cs` / `PortalExtension.cs`). After
deploying a new JS, **browsers keep serving the cached copy** until a hard refresh (Ctrl+F5).
When verifying a widget change, hard-refresh first (or check DevTools → Sources that the new file
is loaded). Recommended future improvement: append `?v=<build/version>` so updates propagate
automatically.

### 2c. The three things people miss
1. **The SoftwareID=999 API key must match on BOTH databases** (customer sends it; GLM validates it).
2. **ConnectIt must be installed on the customer Synergy** — without it, reads work but every
   write throws `Unable to cast MetadataEntity → GLMSys.CI.Data.Connection` (see §0c).
3. **Globe keys need `GLMSys.AIPlus.Agent.ExactGlobe.Server.dll` in the GLM `bin`.** This repo's
   post-build copies **only** `Server.External.dll`; the Globe overlay DLL comes from the
   **AIPlusAgentEG** build and must be deployed separately (it *is* listed in the setup manifest
   `Custom.GLMSys.AIPlus.Agent.Server.Internal.xml`, so a full package install includes it — a
   partial/manual DLL copy can miss it). It loads lazily, so a **Synergy-only** server runs fine
   without it; but any `Product='globe'` key fails `/ai/chat` with a **502** until it is present.
   *(Verified on production 2026-08-13: Synergy chat worked, Globe chat 502'd; copying the Globe
   DLL into the Synergy `bin` fixed Globe immediately.)*

### 2d. End-to-end flow
```
Widget
  → GLMSysAIPlusAgentExternalCallback.ashx   (customer: bridge)
    → GLMSysAIPlusAgentExternalAPI.ashx       (GLM: runs the LLM, returns tool_calls)
  ← tool_calls
  → GeneralToolExecutor.Execute(...)          (customer: executes locally, needs ConnectIt)
    → POST /ai/tool-result                     (GLM: continues the loop)
  ← final reply  → widget
```

---

## 3. Configuration on the GLM server

`GLMSysCIConnections` rows required:

| `SoftwareID` | `Active` | Purpose | Notes |
|---|---|---|---|
| `AzureOpenAI` (enum) | 1 | GLM's AI-provider credentials | Used by `AgentChatService`; **never exposed** |
| `999` | 1 | Customer API key | One per customer (issue `APIKey`); `APIUri` = the `.ashx` URL |

- `999` must be registered in `GLMSysCISoftwares` (per the work-item note).
- Issue/rotate keys by inserting/updating the `999` row's `APIKey`; disable with
  `Active=0`.
- `GLMSysAIPlusAgentBaseModel` setting (read by `AgentChatService.ResolveBaseModel`)
  selects the model; default `gpt-4.1-mini`.
- JWT secret: replace `GetJwtSecretKey()`'s hardcoded `"MySecret"` with a secure
  source before external rollout (`PRD.md` §8.4).

Usage metering uses the existing `GLMSysCILLMUsage` table (search page
`GLMSysCILLMUsageSearch.aspx`).

---

## 4. IIS / hosting — the auth caveat (important)

The current internal callback is an `.aspx` that relies on the **logged-in Synergy
session** (Windows/forms auth). The external API authenticates by **Bearer key**
and must be reachable by external customer apps **without** a Synergy login.

Risks and handling (also `ARCHITECTURE.md` R4):

- If the Synergy site enforces site-wide Windows/NTLM auth, the `.ashx` may be
  challenged **before** our handler runs → 401 regardless of the Bearer key.
- **Mitigation:** host the handler on a path/application configured for **Anonymous
  Authentication** (Bearer enforced inside `ProcessRequest`), or a dedicated
  IIS application/site pointing at the same `bin`. Confirm with infrastructure.
- `.ashx` (`IHttpHandler`) avoids WebForms viewstate/lifecycle entirely, which is
  why it is preferred over `.aspx` for this endpoint.

> **⚠️ Reality check (2026-08-26) — Anonymous is NOT yet viable server-side.** The "Anonymous
> Authentication + Bearer-inside-`ProcessRequest`" mitigation above is the *target*, but it does **not**
> work with the current code: with no Synergy session, `GetEnvironment()` falls through to
> `new Exact.Core.Environment(… AllowAnonymousDatabaseConnection)`, which **throws
> `Initializing the Environment here is not allowed`** inside the web request. Until that tier-3 env
> construction is fixed (startup `EnvironmentFactory`, or the sanctioned Exact request-scoped/anonymous
> accessor), the **only working config is Windows auth + a mapped Synergy service-account app pool**.
> Full matrix and fix direction: **`07-KNOWN-ISSUES.md` §A1 + §A**.

### AppPool identity

- The handler initializes an `Exact.Core.Environment` to read
  `GLMSysCIConnections`/`GLMSysCILLMUsage` and call the provider. The AppPool
  identity must be able to read/decrypt the GLM server's Synergy DB config (the same
  class of issue seen historically with `DefaultAppPool` vs. a privileged Windows
  account). Use an AppPool identity with the required DB-config access.
- **Current requirement (see §A1):** that identity must be a **mapped Synergy resource** so
  `Environment.Current()` returns non-null — an unmapped account (even a privileged one) drops to the
  broken anonymous construction and fails.

### Customer-side AppPool identity and outbound Windows auth

The customer bridge (`GLMSysAIPlusAgentExternalCallback.ashx`) makes server-to-server
HTTP calls to the GLM API. The auth layer has two independent options — pick one:

| Option | How | When to use |
|---|---|---|
| **Explicit credentials** | Fill `UserName`/`Password` on the 999 connection row (see §2b-credentials) | Customer pool runs as `ApplicationPoolIdentity` |
| **Domain pool identity** | Set the customer app pool to a domain service account (e.g. `radium\Client`) | Simpler; no credential row needed |
| **Anonymous GLM handler** | Enable anonymous auth on the GLM `…ExternalAPI.ashx` path | Removes the IIS-level gate entirely; API key is the only auth |

Note (**historical — AIAgent provider retired 2026-08-26, §0d**): the ConnectIt **"Test connection"**
ping was made by the compiled `GLMSys.CI.AIAgent.Provider.dll`, which used `UseDefaultCredentials`
internally — explicit credentials on the 999 row did **not** help it, so under `ApplicationPoolIdentity`
that button needed anonymous auth on the GLM handler. With the provider retired there is no
"Test connection"; `GET /ai/ping` is now a manual probe. (The `ApplicationPoolIdentity` / Windows-auth
considerations for the **chat** bridge itself still apply — see §0d rows above and 07-KNOWN-ISSUES §A2.)

---

## 5. TLS & network

- Production endpoints must be **HTTPS only**.
- Restrict inbound to expected customer networks where feasible; rate-limit per key.
- Do not log API keys or full conversation content.

---

## 6. Deploy procedure (per release)

1. Build the solution (Release) on a machine with the Synergy `bin` references.
2. Confirm the new DLL copied to `BIN\`; copy the `.ashx` to the site `docs\`. **If any customer
   uses a Globe key**, also confirm `GLMSys.AIPlus.Agent.ExactGlobe.Server.dll` (from AIPlusAgentEG)
   is in `BIN\` — the post-build does not copy it (see §2c).
3. Apply guarded SQL (new tables) to the GLM Synergy DB if Phase 3+.
4. Ensure `GLMSysCIConnections` has the `AzureOpenAI` row and at least one `999`
   row (`test-key-001` for dev).
5. Configure IIS auth for the handler path (anonymous + Bearer).
6. Smoke test: `POST /ai/chat` with `Bearer test-key-001` → 200; invalid key → 401.
7. Regression: run the internal `.aspx` widget flow.

---

## 7. Rollback

- The feature is additive: remove/disable the `.ashx` and set the `999` row
  `Active=0` to take the external API offline. The internal flow is unaffected.
- New tables can remain (unused) or be dropped; no impact on existing addon tables.

---

## 8. Environments summary

| Setting | Dev | Prod |
|---|---|---|
| GLM server (API host) | `Synergy_503` — `http://localhost/Synergy_503/docs/` | GLM production server |
| Customer app | `Synergy_503_ClientAIPlusAgent` — `http://localhost/Synergy_503_ClientAIPlusAgent/docs/` | customer server |
| API endpoint | `http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx` | `https://<glm-host>/.../GLMSysAIPlusAgentExternalAPI.ashx` |
| API key | `test-key-001` (`999` row) | issued per customer |
| Model | `GLMSysAIPlusAgentBaseModel` or default | per setting |
| TLS | optional (localhost) | required |
| AppPool | dev account | account with DB-config access |
