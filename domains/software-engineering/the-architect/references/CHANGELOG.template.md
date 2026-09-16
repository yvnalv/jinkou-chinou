# CHANGELOG — AI Plus Agent External API

Running log of changes for the **AIAgent Chat External API** work item. **Newest
entry on top** (reverse-chronological).

> **Update rule:** add an entry here on **every** change — design decisions, doc
> edits, code, schema, deployment, blockers. Do not land a PR or finalize a design
> change without a corresponding CHANGELOG entry. See `docs/CONTRIBUTING.md` §0.

## Entry template (copy for each change)

```
## YYYY-MM-DD HH:MM (+TZ) — <short title>
- **What:** what changed (files/areas touched, decision made).
- **Why:** the reason / trigger.
- **How to resolve / how applied:** steps taken, or how to act on it.
- **Status:** Done | In progress | Proposed | Reverted.
- **Currently blocking:** what this blocks or is blocked by (or "None").
- **Refs:** related docs/§, PR/WI, files.
```

---

## 2026-09-08 (+07:00) — ROOT CAUSE: `IsDefault` overloaded -> server cannot reach any LLM (`502 provider_error`); new doc `DESIGN_DEFECTS.md`
- **What:** Identified why the GLM server returns `502 provider_error` after the environment problem was resolved.
  `AgentChatService.ResolveProviderConnectionId()` selects the server's **LLM provider** with
  `WHERE IsDefault = 1 AND Active = 1` and **no `SoftwareID` filter**. The same table also holds the customer
  **API-key** rows (`SoftwareID = 999`), and `ProcessSetDefaultProvider` clears `IsDefault` from every other row
  when any provider is made default. Marking the 999 "Customer Credentials" provider as default - the documented
  way to enable external routing - therefore **un-defaults Azure OpenAI**, and the server resolves its "LLM" to a
  customer-key row whose `APIUri` is the Synergy web host.
- **Observed (Synergy_505 as GLM server):** `999 GLM Systems International Ltd IsDefault=True` /
  `65 Azure OpenAI IsDefault=False`.
- **Failure signature:** auth + environment + key validation + orchestrator construction all succeed, then the
  provider call throws inside the try at `ExternalAgentApiHandler.cs:193` -> `502 provider_error`, and **no row is
  written to `GLMSysCILLMUsage`** because Azure is never called. That absent usage row is the cheapest way to tell
  a provider *misconfiguration* from an Azure-side failure (bad deployment name, rate limit), which logs first.
- **Immediate remediation (no deploy):** move `IsDefault` back to the Azure OpenAI row.
- **Recommended fix:** (1) `ResolveProviderConnectionId()` excludes customer-key rows (allow-list of LLM
  `SoftwareID`s); (2) `ProcessSetDefaultProvider` stops touching `IsDefault` for `SoftwareID = 999` - external
  routing already has its own switch, `GLMSysAIPlusAgentUseExternalApi`, so the flag carries no meaning there.
  Neither needs a schema change.
- **New doc:** `docs/DESIGN_DEFECTS.md` - D1 the overloaded flag; D2 one table holding two entity kinds (with an
  audit list of six unfiltered query sites); D3 six related same-class defects (licensing Preserve re-enabling a
  revoked key, unticking Agent not revoking, the lost `Active` filter, non-deterministic `TOP 1`, the swallowed
  `502` exception, `DecryptApiKey` returning ciphertext as a password); D4 remediation order; D5 the design
  principle.
- **Status:** Root cause identified + documented. Fixes proposed, **not yet applied**.
- **Currently blocking:** production chat until `IsDefault` is corrected on `srv01`.
- **Refs:** `AgentChatService.cs` ~L203/L221, `GLMSysAIPlusAgentClientCallBack.aspx` ~L3490,
  `ExternalAgentApiHandler.cs:193-206`, `docs/DESIGN_DEFECTS.md`, `docs/TROUBLESHOOTING.md`.

## 2026-09-03 (+07:00) — New doc `TROUBLESHOOTING.md` (41-row failure matrix, end to end)
- **What:** Added `docs/TROUBLESHOOTING.md` — every known failure along the external chat path with
  **failure / symptom / how to confirm / where to debug (project + file + line) / fix**, grouped by hop:
  route selection, customer config read, NTLM, environment construction, API-key validation,
  orchestration + response handling, deployment.
- **Why:** the same failures kept being re-diagnosed from scratch, and several produce *identical*
  outward symptoms (one HTML 500) despite completely different causes and fixes.
- **Key content:**
  - **§0 triage** — four questions that cut the matrix down fast. The decisive one: an **HTML** error page
    means the failure is *before* `ProcessRequest`, so nothing inside the handler can affect it; a **JSON**
    error means the handler ran.
  - **§4 environment block** — rows 17-22 have **no debuggable line**; they fire in Exact's `Session_OnStart`
    (`global.asax:57`). Breaking at `GlmServerEnvironmentProvider.cs:11` and seeing it *not hit* is itself
    the diagnostic. Includes the six-breakpoint environment debug set.
  - **§7** — the `humres` identity query with the known-good reference row (local `Client`, `res_id 284983`),
    the duplicate-999 query, and the DLL SHA256 table (all AIPlus DLLs are stamped `1.0.0.0`, so verify by
    size + hash, never version).
- **Test result recorded:** `blocked = 1` on the caller's `humres` row is **not** a failure mode — verified
  2026-09-03, still returns `{"status":"ok"}`. The `AllowBlockedUsers` hypothesis is eliminated.
- **Verification anchor:** `AIPlusAgentServerInternal` @ `6054d82` + the uncommitted `GetEnvironment()`
  rewrite; `AIPlusAgent` @ `fa08193`; Synergy 505, `Exact.Core 5.0.0.737`. Line numbers are anchors, not
  addresses — search the quoted symbol if they drift.
- **Status:** Done.
- **Refs:** `docs/TROUBLESHOOTING.md`, `docs/ENV_INIT_AND_AUTH.md`, `07-KNOWN-ISSUES.md` §A/§A1,
  `DEPLOYMENT.md` §2.

## 2026-09-02 (+07:00) — API-key rejection changed from `401` to `403` (status-code collision with IIS Windows auth)
- **What:** `ExternalAgentApiHandler.ProcessRequest` now answers **`403` / `forbidden`** instead of `401` / `unauthorized`
  for both API-key failures: missing key, and invalid/inactive key. `API_SPEC.md` updated (§ auth, /ai/ping, error table).
- **Why:** the endpoint sits behind IIS **Windows authentication**, which owns `401`. Returning `401` from the
  application for a *different* reason collides with it:
  - a browser that has just completed NTLM sees a second `401` and **re-prompts for Windows credentials**, so a valid
    login looks rejected (observed 2026-09-02 on `…/Synergy_505_ClientABCD/docs/GLMSysAIPlusAgentExternalAPI.ashx`);
  - .NET clients (`HttpWebRequest`/`HttpClient` with `NetworkCredential` — both the Synergy bridge's `CallExternal`
    and the Globe `ExternalTransport`) treat `401` as an auth challenge and **retry the NTLM handshake** pointlessly;
  - in logs a transport auth failure and an API-key failure become indistinguishable.
  Transport auth has already succeeded by the time the key is checked, so "authenticated but not permitted" (`403`)
  is the accurate status.
- **Client impact — none.** Verified before changing: `CallExternal` catches `WebException`, reads the body and parses
  the JSON envelope without branching on status; the Globe transport only checks `IsSuccessStatusCode` and reports
  `(int)StatusCode` + the extracted message. No consumer switches on the `error.code` string either, so the code was
  aligned to `forbidden` alongside the status.
- **Also clarified (not a bug):** a keyless request **never reaches environment acquisition** — the key-presence check
  at the top of `ProcessRequest` returns first. So browser probes without `X-API-Key` say nothing about the env problem;
  they must carry the key to exercise `GetEnvironment()`.
- **Build:** `GLMSys.AIPlus.Agent.Server.External.dll` 52224 bytes, SHA256 `B1FFB6D2415F8289D459F1D6F679A49DE44144F7BB43D5D9565D69285405765B`.
- **Status:** Implemented + builds clean locally. Not deployed.
- **Refs:** `ExternalAgentApiHandler.cs` (`ProcessRequest`), `ApiResponseWriter.Codes.Forbidden`, `API_SPEC.md`,
  `docs/ENV_INIT_AND_AUTH.md` §1.

## 2026-09-02 (+07:00) — Env acquisition rebuilt to Exact's shipped in-request pattern; new doc `ENV_INIT_AND_AUTH.md`
- **What:** Rewrote `GlmServerEnvironmentProvider.GetEnvironment()` to the standard Exact ships in
  `docs\EGNUtilities.ashx`: `EnvironmentFactory` -> `Environment.Current()` -> `new Environment(HttpContext.Current)`,
  **each tier in its own try/catch**, with the background constructor
  (`ProcessOptions.AllowAnonymousDatabaseConnection`) reached **only when `HttpContext.Current == null`** — where it is
  legal. When every applicable tier fails it throws `InvalidOperationException` carrying a per-tier reason list
  (`current: … | httpcontext: …`), which the handler renders as a JSON 500; tiers are also traced as `AIAGENT-ENV <tier>: <reason>`.
- **Also:** removed the hard-coded `"Synergy_503"` fallback in `ResolveDbConfigName()`. Order is now
  `DbConfigName` -> **`GLMSysAIPlusAgentDbConfig` appSetting** (new) -> `Request.ApplicationPath` ->
  **`HostingEnvironment.ApplicationVirtualPath`** (new; works off-request, which is the only place tier 4 runs) ->
  **null**. It never guesses — a wrong `/DBCONFIG` silently points the API at another database. Note the old
  `HttpContext` branch was dead code there: that method only ran when `HttpContext.Current` was null, so it always
  returned `"Synergy_503"`.
- **Why:** `07-KNOWN-ISSUES.md` §A root cause — the background constructor is illegal while `HttpContext.Current != null`
  (`Initializing the Environment here is not allowed`). The 2026-08-27 fix was **never committed or deployed**; it existed
  only as an uncommitted working-copy edit (now `stash@{0}` in `AIPlusAgentServerInternal`).
- **New evidence (local repro, 2026-09-02):**
  - `Environment.Current()` is **not** a passive getter — it calls `new Environment(HttpContext)` internally
    (stack: `..ctor(HttpContext) +1681` <- `Current() +415`). So inserting that constructor as an extra tier is **not**
    a second chance when `Current()` throws — a correction to the 2026-08-27 plan.
  - With the handler declaring `IRequiresSessionState`, a cookie-less caller makes ASP.NET create a session per call,
    firing Exact's `Session_OnStart` (`global.asax:57`) during **`AcquireRequestState`** — so env construction happens
    **before** `ProcessRequest` and the handler's try/catch can never turn it into a JSON 500. That also explains the
    production yellow page's single reset frame at `ProcessRequest +0`.
  - Reproduced locally under Anonymous IIS auth: `ArgumentNullException "g"` from `Session_OnStart` -> `Environment.Current()`.
    Under NTLM with a mapped account the same endpoint returns `200` in ~34 ms.
  - Production facts confirmed: IIS **Windows auth, anonymous disabled** (incognito gets a browser credentials popup);
    the app is **root-hosted** (`Server Error in '/' Application`), so `Request.ApplicationPath` is `"/"` and the
    `GLMSysAIPlusAgentDbConfig` appSetting is **mandatory** there; `customErrors` is **`Off`** (verbose stack traces
    served to customers).
  - `EGNUtilities.ashx` succeeds on production only because its callers are browsers with a Synergy session, and because
    it **never calls the background constructor** — not because it does anything the API cannot.
- **New doc:** `docs/ENV_INIT_AND_AUTH.md` — the three auth layers, what the message really means, the EGNUtilities
  reference standard, and the two open design questions: (§6) whether the handler should keep `IRequiresSessionState`
  — recommendation **no**, it is not an auth mechanism and `context.Session` is never read; (§7) whether an encrypted
  Windows password in the customer DB is acceptable — encryption at rest is reversible by design and the real issue is
  that the secret grants an **OS identity on shared production infrastructure**, versus an API key that grants one
  revocable thing.
- **Build:** `GLMSys.AIPlus.Agent.Server.External.dll` 52224 bytes, SHA256 `20D3A3540AF21372B9B27986EE893696C93945B55DBFEEB0F329EAA33D0CD811`.
- **Status:** Implemented + builds clean locally. **Not deployed.** Blocked on the two probes below.
- **Currently blocking / next:** (1) hash the DLL deployed on `srv01` against `C1B03F42…` / `D6A5C94F…`; (2) probe
  `EGNUtilities.ashx?Security=1` with **NTLM as the customer's service account** — `<security>` means an environment is
  obtainable for that identity, `<message>` means it is not and the account needs mapping as a Synergy resource
  (a fix needing **no code**). Do both before deploying.
- **Refs:** `GlmServerEnvironmentProvider.cs`, `ExternalAgentApiHandler.cs`, `docs/ENV_INIT_AND_AUTH.md`,
  `07-KNOWN-ISSUES.md` §A/§A1/§A2, CHANGELOG 2026-08-26 / 2026-08-27.

## 2026-08-27 (+07:00) — FIX (root cause): `Initializing the Environment here is not allowed` — wrong Environment constructor inside a web request
- **What:** Fixed `GlmServerEnvironmentProvider.GetEnvironment()` (`GLMSys.AIPlus.Agent.Server.External`). Added a tier
  between `Environment.Current()` and the anonymous fallback: when there is **no** ambient session but an
  **HttpContext exists**, build the environment with **`new Exact.Core.Environment(HttpContext.Current)`** — the
  framework-sanctioned **in-request** constructor. The previous fallback used the **background** constructor
  `new Environment("name", "/DBCONFIG:", ProcessOptions.AllowAnonymousDatabaseConnection)`, which Exact **forbids while
  HttpContext.Current != null** → that is the exact source of `Initializing the Environment here is not allowed`.
- **Root cause (confirmed):** the endpoint is a server-to-server, API-key-authenticated call that carries **no Synergy
  session**, so tier-2 `Environment.Current()` is null and it fell to the background constructor **inside a web request**.
  It only ever "worked" when a **warm** `Environment.Current()` from a prior logged-in request happened to be on the same
  worker thread — hence the non-determinism (worked in dev / when a session was warm; failed on cold threads / after an
  app-pool recycle / on pure server-to-server production calls).
- **Evidence for the fix:** Exact's own code uses this exact pattern —
  `GLMSys.Services.NotificationModel/BSubscriber.Initialize` (505/Core): `Current()` → else `new Environment(HttpContext.Current)`
  → else (no HttpContext) the background constructor. Our provider was skipping the middle branch.
- **Effect:** env acquisition is now **deterministic and sessionless** — no Synergy login required, works on cold threads
  and across recycles, and under either Anonymous or Windows IIS auth. This is the **intended** anonymous/key-only design.
- **Local build:** rebuilt `GLMSys.AIPlus.Agent.Server.External.dll` — 50176 bytes, SHA256 `C1B03F424A9DCA4FDFBA1D1A3156EF8657615786916433857F4CE85796D12C3C`
  (prior deployed build was `D6A5C94F78412EDBD7234AD126D2E251BB1FA18C8AF063C215C6E4E3483E3BB7`). Post-build copied to the local
  `…505\bin`. **Note:** all AIPlus DLLs are stamped `1.0.0.0`, so verify deploys by **size + SHA256**, not version.
- **Deploy + verify:** copy the new DLL to `srv01` `…505\bin`, recycle the app pool, then `GET /ai/ping` **immediately after
  `Restart-WebAppPool`** (cold thread, no session) — previously errored, must now return `200`. Test under both Windows and
  Anonymous auth. (For future server-side debugging, also copy the `.pdb`; the post-build copies the DLL only.)
- **Fallback (if `new Environment(HttpContext.Current)` still requires a user):** construct the anonymous env **off the
  request thread** (`Task.Run(...).GetAwaiter().GetResult()`, where `HttpContext.Current` is null so the guard doesn't fire) —
  same file/method, two-line change.
- **Status:** Implemented + builds clean locally. **Not yet deployed/verified on `srv01`.**
- **Scope:** fixes the env error only. The separate **chat-only 502** (proxy timeout / async #6949) is a different issue.
- **Refs:** `GlmServerEnvironmentProvider.cs` (`GetEnvironment`), `BSubscriber.vb` (reference pattern), `07-KNOWN-ISSUES.md` §A/§A1.

## 2026-08-26 (+07:00) — Analysis: can the GLM server accept BOTH Anonymous and Windows IIS auth? (dual-mode)
- **Question:** does the current architecture connect successfully under **either** Anonymous **or** Windows
  (NTLM) auth on the GLM `.ashx` — and does the logic handle both?
- **Finding — three independent layers:** (1) IIS transport auth (Anonymous vs Windows), (2) Environment
  acquisition in `GlmServerEnvironmentProvider.GetEnvironment()`, (3) API-key check (`X-API-Key`). Layer 3 is
  **mode-independent** (runs the same either way).
- **Client bridge handles both ✅:** `CallExternal` attaches a `NetworkCredential` only when the 999 row has
  `UserName`/`Password`; otherwise it sends none → works against Windows *or* Anonymous IIS.
- **GLM server env acquisition handles only ONE ❌:** `GetEnvironment()` is a 3-tier fallback
  (`EnvironmentFactory` → `Environment.Current()` → `new Exact.Core.Environment(… AllowAnonymousDatabaseConnection)`).
  Tier 3 **throws `Initializing the Environment here is not allowed`** inside a web request. So:
  **Anonymous → fails** (tier 3); **Windows auth → works only if the account is a mapped Synergy resource**
  yielding a non-null `Environment.Current()` (tier 2). Plain/unmapped Windows auth (e.g. `LAME1035`) falls to
  tier 3 and fails — the production symptom. (`IRequiresSessionState` can even trip `Session_Start` before the handler.)
- **To make both modes work — fix tier 3:** set `GlmServerEnvironmentProvider.EnvironmentFactory` at app
  startup, **or** replace `new Environment(...)` with the sanctioned Exact request-scoped/anonymous accessor.
  Then **Anonymous IIS + key-only** becomes the clean recommended mode; until then, only **Windows auth +
  mapped Synergy service-account pool** works.
- **Also confirmed this session:** the customer bridge (`GLMSysAIPlusAgentExternalCallback.ashx`,
  `TryGetExternalApi`) reads the key from **`GLMSysAIPlusProviderConnections`** (`SoftwareID=999`), decrypts it,
  and has **no** `GLMSysCIConnections` / `CI.AIAgent` references — the AIAgent-provider repoint is complete in code.
- **Status:** Analyzed; documented. **No code change yet** — owner to supply the target auth conditions before the tier-3 fix.
- **Refs:** `07-KNOWN-ISSUES.md` §A1 (matrix) + §A; `GlmServerEnvironmentProvider.GetEnvironment`,
  `ExternalAgentApiHandler` (`IRequiresSessionState`), `GLMSysAIPlusAgentExternalCallback.ashx` (`CallExternal`/`TryGetExternalApi`).

## 2026-08-26 (+07:00) — Decision: retire the ConnectIt **AIAgent** provider dependency for the external API
- **What:** The external AI Agent API **no longer depends on the ConnectIt `GLMSys.CI.AIAgent.Provider`**
  or on a ConnectIt-managed `GLMSysCIConnections` `SoftwareID=999` connection created/tested via the
  Synergy Provider/Connections UI. The customer API key is provisioned by the **license-driven flow**
  into **`GLMSysAIPlusProviderConnections`** (`SoftwareID=999`, materialized on license apply — see the
  2026-07-16 §14 entry), which the validator reads directly. So the `AIAgent` provider — whose only jobs
  were letting that connection be *created* and *"Test connection"-ed* in the UI — is redundant.
- **Scope (narrow, by owner decision):** this removes **only** the `AIAgent`-provider dependency of *this*
  project (the external API). **Other ConnectIt usage is unchanged** — the GLM server still calls Azure
  OpenAI through `GLMSys.CI.AzureOpenAI.Provider`, customer-side CRUD still routes through `GLMSys.CI.*`
  providers (ConnectIt remains a customer prerequisite for tool execution), and token usage still logs to
  `GLMSysCILLMUsage`.
- **Effect on setup:**
  - `GLMSys.CI.AIAgent.Provider.dll` is **no longer a required deploy artifact**, and no `GLMSysCISoftwares`
    row with `ProviderName="AIAgent"` / ConnectIt `999` connection needs to be created for the API to work.
  - The ConnectIt **"Test connection"** button path is retired. **`GET /ai/ping` remains** as a generic
    health/auth probe you can hit manually (curl/browser with `X-API-Key`) — it is no longer *for* the
    AIAgent provider.
- **Docs:** marked the AIAgent-provider sections **deprecated (retained for history)** rather than deleted —
  `API_SPEC.md` §5a, `DEPLOYMENT.md` §0d + manifest, `QA_TEST_PLAN.md` §0/§3.4/§4, `07-KNOWN-ISSUES.md` §H.
  The historical CHANGELOG entries (2026-06-10 "ConnectIt AIAgent provider + `/ai/ping`", etc.) are left intact.
- **Status:** Decision recorded; docs updated. Code/deploy cleanup (drop the DLL from the deploy list) to
  follow in `AIPlusAgentServerInternal` / customer packaging as convenient — the API already works without it.
- **Refs:** `AIPlus-Agent-API-Key-License-Integration-Plan.md` §15 (parked item "retire `GLMSys.CI.AIAgent.Provider`");
  `ExternalApiKeyValidator.cs` (reads `GLMSysAIPlusProviderConnections`); `ExternalAgentApiHandler.cs` (`/ai/ping`).

## 2026-08-26 (+07:00) — Investigation: production `Initializing the Environment here is not allowed` (env-init on a server-to-server call)
- **Symptom:** On the GLM production server (`srv01`, IIS app `Synergy`, `/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/ping`),
  an authenticated request returned the ASP.NET "yellow page" `System.Exception: Initializing the Environment here is not allowed`
  thrown at `ExternalAgentApiHandler.ProcessRequest` (`+0`, no inner frames). Intermittent ("not each time" — Event ID 3005, occurrence 5).
  The probe used the **old** `X-Api-Key: test-key-001`.
- **What surfaced it (auth side):** the Windows account the customer authenticates with (`LAME1035`) had an **expired password**
  (Security log `0xC000006E` / sub `0xC0000071` = *password expired*) → NTLM to the Synergy IIS site failed **at IIS**, so requests
  never reached the handler. After the customer **recreated the account with the same password**, NTLM succeeded (`Error Code 0x0`),
  requests reached `ProcessRequest`, and the environment-init failure became visible. **The account fix did not cause the bug — it unmasked it.**
- **Root cause (same as `07-KNOWN-ISSUES.md` §A, new message string):** for a server-to-server call there is no Synergy session, so
  `GlmServerEnvironmentProvider.GetEnvironment()` finds `Environment.Current() == null` and falls to
  `new Exact.Core.Environment("GLMSysAIPlusAgentExternalAPI", "/DBCONFIG:…", ProcessOptions.AllowAnonymousDatabaseConnection)` — which the
  Exact framework **forbids inside a web request** (throws `Initializing the Environment here is not allowed`; the pre-505 build threw
  `ArgumentNullException "g"` from the same anonymous path). Intermittency = `Current()` occasionally returns a leftover ambient environment
  from a prior Synergy request on the same worker thread.
- **`test-key-001` is a red herring for THIS error:** `GetEnvironment()` runs **before** `Validate()`, so the request dies at env-acquisition
  regardless of key validity; a real `glm_live_…` key fails identically on this path. (Accepted key format is unchanged —
  `glm_live_`/`glm_test_` + 22 + 32 base62; `test-key-001` is rejected by `ParseKeyId` anyway.)
- **Yellow page vs. the handler's JSON 500:** the source wraps `GetEnvironment()` in try/catch that should return a JSON `500`. That it didn't
  points to either **version drift** (deployed `Server.External.dll` older than source — check file version on `srv01`) or the exception being
  raised in the `IRequiresSessionState` session/env setup around the handler. **Verify the deployed assembly first.**
- **Remediation options (discussion, not yet applied):** (1) use the sanctioned Exact accessor for a request-scoped/anonymous env instead of
  `new Environment(...)`; (2) set `GlmServerEnvironmentProvider.EnvironmentFactory` at app startup (the provider already prefers a host-supplied
  factory); (3) run the endpoint under **Anonymous** IIS auth + key-only (removes both the NTLM header clobber and the expired-password failure);
  (4) set the service account password to never-expire / gMSA. A durable fix combines {1 or 2} with 3. See §A for the standing mapped-user requirement.
- **Status:** Investigated; root cause identified. **No code change applied** — remediation pending owner decision.
- **Currently blocking:** the customer's server-to-server `/ai/*` calls on `srv01` until env-init is fixed or the pool runs as a mapped Synergy user.
- **Refs:** `GlmServerEnvironmentProvider.cs` (`GetEnvironment`), `ExternalAgentApiHandler.cs` (`ProcessRequest`/`ExtractApiKey`),
  `ExternalApiKeyValidator.cs`/`ExternalApiKeyGenerator.cs` (key format); `07-KNOWN-ISSUES.md` §A/§A2.

## 2026-08-26 (+07:00) — External AI Agent orchestration converted to async/await (#6949)
- **What:** The external orchestration call surface is now **async**. `IExternalOrchestrator.PrepareUserTurn` and `RunLoop` return
  `Task<StepOutcome>`; both `ExternalAgentOrchestrator` and `GlobeExternalOrchestrator` implement them async. The synchronous `.ashx`
  entry point bridges via `HandleChat(...)/HandleToolResult(...)` (`private async Task`) invoked as `.GetAwaiter().GetResult()` from
  `ProcessRequest`, and `await …ConfigureAwait(false)` on the orchestration calls.
- **Why:** WI #6949 — make the LLM/tool-loop I/O path non-blocking and align the external orchestrator's shape with async provider calls.
- **Convention note:** this **supersedes**, for the external orchestration path only, the older "no `async/await` in the `.ashx` request path"
  guardrail in `CLAUDE.md` §8. The customer-side `.aspx`/callback and the synchronous `Exact.Data`/`EDLConnection` DB access remain synchronous.
- **Status:** Done (commit `f7f1cb5`, branch merged to `master`).
- **Refs:** `IExternalOrchestrator.cs`, `ExternalAgentOrchestrator.cs`, `GlobeExternalOrchestrator.cs`, `ExternalAgentApiHandler.cs`
  (`HandleChat`/`HandleToolResult`/`ProcessRequest`).

## 2026-08-13 (+07:00) — Fix: Globe `/ai/chat` 502 on production = Globe overlay DLL missing from GLM `bin`
- **Symptom:** On production, an authenticated `POST /ai/chat` returned a proper reply for
  **Synergy** keys but an **IIS gateway 502** ("Web server received an invalid response…") for
  **Globe** keys. `GET /ai/ping` and auth were fine for both — so it was isolated to the Globe
  chat path, not auth/endpoint/Azure (Synergy proved the LLM call works).
- **Root cause:** `GLMSys.AIPlus.Agent.ExactGlobe.Server.dll` (the AIPlusAgentEG overlay that
  `GlobeExternalOrchestrator` → `GlobePromptAssembler` binds to) was **not present in the GLM
  server's `bin`**. This repo's post-build copies only `Server.External.dll`; the Globe DLL is a
  separate build output and had not been deployed. Synergy keys never touch that DLL (lazy load),
  so they were unaffected.
- **How resolved:** copied `GLMSys.AIPlus.Agent.ExactGlobe.Server.dll` into the Synergy server
  `bin`. Globe `/ai/chat` worked immediately. The DLL is self-contained (references only stock
  `Newtonsoft.Json`/`System.Net.Http`; its Globe prompts + tool JSON are **embedded resources**),
  so no companion files were needed.
- **Also (doc fixes):** added the Globe DLL to `DEPLOYMENT.md` §2a manifest + a new §2c item #3 and
  §6 step 2 note; corrected `GLOBE_PROFILE_POINTER.md` (the shipped design uses a compiled Globe
  overlay assembly with embedded resources via `IExternalOrchestrator`/`GlobeExternalOrchestrator`
  — **not** the never-implemented data-driven `~/docs/agent-profiles/<product>/` profile seam);
  added `07-KNOWN-ISSUES.md` §D. The setup manifest `Custom.GLMSys.AIPlus.Agent.Server.Internal.xml`
  already lists the DLL (added in `d02b380`), so a full package install includes it — the gap was a
  partial/manual DLL deploy.
- **Status:** Done (verified on production).
- **Currently blocking:** None.
- **Refs:** `GlobeExternalOrchestrator.cs`, `ExternalAgentApiHandler.HandleChat`/`ResolveProduct`,
  `GLMSys.AIPlus.Agent.Server.External.csproj` (Globe `HintPath` + post-build), WI #6892.

## 2026-07-22 (+07:00) — Rotate confirm → native Synergy dialog; add Revoke / Re-enable buttons
- **What:**
  - **Rotate confirm** now uses Synergy's own dialog (`SysShowModalPopup(SysConfirmUrl(5,'0',<msg>), … SysDialog.returnValue …)`) with the custom rotation warning, instead of the browser `confirm()` ("localhost says"). Matches the WorkflowPlus custom-message pattern.
  - **Revoke API Key** button — immediate on click (status flip, no re-issue): sets `Active=0` + stamps `RevokedDate`/`Revoker` on the customer's central `GLMSysAIPlusProviderConnections` row → the validator returns 401 on the next call. Visible only when a key exists **and** is active.
  - **Re-enable API Key** button — reverses it (`Active=1`, clears `RevokedDate`/`Revoker`, same key). Visible only when the key is revoked.
  - The masked Preserve display now shows status: `KeyID … ****last4 (active|REVOKED)`.
- **Also:** fixed the `DBNull → String` error on Rotate→Add (VB `AppendSetValue(..., DBNull.Value)` → `Nothing`, matching the C# store's `null`); removed the temporary stack-trace diagnostic added to hunt it.
- **How it works:** revoke/re-enable are driven by `hfAgentRevoke`/`hfAgentReenable` flags (set client-side via the confirm), handled in `RefreshAgentApiKeyField` (OnPreRender) which flips the row then re-reads state. Enforcement is central-only (unchanged validator); the customer's local row is irrelevant to the 401.
- **Status:** Done; builds clean. Deploy `GLMSysGenerateAddOnLicense.aspx` (docs) + rebuilt `GLMSys.License.Page.dll` (bin); copy the `.vb` back to CoreInternal.
- **Refs:** `GenerateAddOnLicense.vb` (`RefreshAgentApiKeyField`, `RevokeAgentConnection`, `ReenableAgentConnection`); `GLMSysGenerateAddOnLicense.aspx` (Rotate/Revoke/Re-enable buttons). Closes the §15 "operator Disable/Revoke now" item.

## 2026-07-22 (+07:00) — Fix (ROOT CAUSE): VB byte-shift truncated license values >= 256 chars
- **Symptom:** the AIPlus license row rendered with the End date/Users cut off (`ENDDATE:31-`); short add-on rows were fine. Persisted through multiple decode rewrites, IIS resets, and rebuilds.
- **False trails (now understood):** the stored value was always complete (proved by decrypting the real value → full 357 chars) and the decrypt/read was fine on the server (a diagnostic showed `raw=361` decrypted bytes). The earlier "single-`Read` truncation" theory was wrong — `CryptoStream` read fully.
- **Actual root cause:** in `Decode`, the 4-byte length prefix was reassembled as `length(0) Or (length(1) << 8) Or …`. In **VB.NET the `<<` operator masks the shift count to the left operand's bit width**, so `Byte << 8` shifts by `8 And 7 = 0` — the high bytes never shift in and `len` collapses to the **low byte**. `357 & 0xFF = 101`, so any value **≥ 256 chars** decoded to 101 chars. Other add-ons were always < 256 chars, so it never showed until the AIPlus **API-key embed** pushed the value to 357. (`Encode` was correct — `text.Length` is an `Integer`, so its shifts aren't masked; and the C# customer-side decoder is unaffected — C# promotes `byte` to `int` before shifting.)
- **Fix:** cast each byte to `Integer` **before** shifting: `CInt(length(0)) Or (CInt(length(1)) << 8) Or …`. Applied in both repos' `GenerateAddOnLicense.vb`. (Kept the `CopyTo`-based full-stream decrypt from the prior step; removed the temp `[b64=…]`/`DecodeRawByteCount` diagnostics.)
- **Note on the debugging loop:** the deploys *were* landing (the diagnostic proved the new binary ran); the bug was in the code, not staleness. The `raw`/`txt` diagnostic is what finally isolated it.
- **Status:** Done; builds clean. Redeploy `GLMSys.License.Page.dll` + recycle.
- **Refs:** `GenerateAddOnLicense.vb` `Decode` (len reconstruction).

## 2026-07-16 (+07:00) — Fix: "Index was outside the bounds of the array" removing the AIPlus license
- **Symptom:** removing the AIPlus row from the license list threw *Index was outside the bounds of the array*; other add-ons removed fine.
- **Root cause:** `RemoveLicenseKeyFromCustomXml` pre-sizes `customerLicensesNew` to `count-1`, assuming exactly one item matches `RemoveAddOn` and is dropped. The AIPlus row's remove ✕ built `RemoveAddOn` from the **decoded** `ADDON:` — which was **empty** (the `Decode` truncation bug) — so **nothing matched**, all `count` items were kept, and the write overran the `count-1` array.
- **Fix (`GenerateAddOnLicense.vb`):** (1) `RemoveLicenseKeyFromCustomXml` now collects kept licenses in a `List(Of CustomerLicense)` → never overruns regardless of how many match; (2) the list's remove ✕ now sources `RemoveAddOn` from the **intact `CustomerLicense.AddOn` XML property** (falls back to the decoded value), so removal works even if the encoded value was truncated/corrupted.
- **Status:** Done; builds clean. Redeploy `GLMSys.License.Page.dll` + recycle.
- **Refs:** `GenerateAddOnLicense.vb` (`RemoveLicenseKeyFromCustomXml`, `ListLicensesGetData` remove cell).

## 2026-07-16 (+07:00) — Fix: license `Decode` truncated longer (AIPlus) values → blank license row
- **Symptom:** after saving/re-saving an AIPlus license, its row in the generator's license list rendered **blank** (name cut to "GLM S", no Addon/Features/dates), while WordMergePlus/WorkflowPlus rows were fine.
- **Root cause:** both `Decode` (VB, `GenerateAddOnLicense.vb`) and `DecodeLicenseValue` (C#, `GLMSysLicenseUpdateCallBack.aspx`) read the decrypted `CryptoStream` with a **single `Read()`**, which may return fewer bytes than requested. Short add-on values fit one read; the **AIPlus value is longer** (embedded `KEYID/APIURI/APIEXPIRY/CUSTOMERID`, plus `APIKEY` on Issue), so it decoded **truncated** → `GetValueFromLicense` found no `ADDON:`/`FEATURES:`.
- **Fix:** read the crypto stream to completion (`ReadStreamFully`/`ReadFully` loops) and clamp the length to bytes actually read. Short values unchanged.
- **No data loss:** the bug was read-side only; `Encode` stored the full ciphertext, so existing rows decode correctly after the rebuilt DLL is deployed. **Caveat:** the **Re-new** path (decode→modify→re-encode) on the buggy build could have truncated-and-re-saved an AIPlus license permanently — re-issue via **Add** if any AIPlus license was renewed on the old build.
- **Status:** Done; license-page project builds clean. Redeploy `GLMSys.License.Page.dll` (central) + `GLMSysLicenseUpdateCallBack.aspx` (customer).
- **Refs:** `GenerateAddOnLicense.vb` (`Decode`, `ReadStreamFully`); `GLMSysLicenseUpdateCallBack.aspx` (`DecodeLicenseValue`, `ReadFully`).

## 2026-07-16 (+07:00) — License-driven Agent API key: issuance + Issue/Preserve/Rotate lifecycle (§14)
- **What:** The AIPlus license now issues the Agent API key when the **"Agent"** feature is ticked, carries it inside the license, and the customer materializes it on license apply — so the key is provisioned without hand-inserting a row. Then reworked the key lifecycle to the industry-standard **Issue / Preserve / Rotate** model (supersedes the initial rotate-on-resave behaviour).
- **Foundation (earlier this session):**
  - **License generator** (`GLMSys.License.Page\GenerateAddOnLicense.vb`, CoreInternal; working copy builds in the 505 repo): VB port of the secure key generator (matches `ExternalApiKeyGenerator` format `glm_live_`+22+32 base62); the disabled **Agent API Key** field appears when the Agent checkbox is ticked (checkbox id is the **numeric** enum → `cbAIPlus4`, not `cbAIPlusAgent`); on Add it upserts the central `GLMSysAIPlusProviderConnections` row (`SoftwareID=999`, keyed by new **`CustomerID`** = `cmp_wwn`) with the `Exact.Core.Crypt`-encrypted key, and embeds the key material in the (RC2-encoded) license value.
  - **Generator page** (`GLMSysGenerateAddOnLicense.aspx`): the disabled field + hidden carrier.
  - **Customer apply** (`505\Core\Setup\docs\GLMSysLicenseUpdateCallBack.aspx`): on **Continue & Apply**, decodes the license segments and upserts the **local** `GLMSysAIPlusProviderConnections` row, **re-encrypting** `APIKey` with the customer's own connection (ciphertext never copied across DBs — robust whether `Exact.Core.Crypt` is shared- or DB-scoped).
  - **Schema** (`505\AIPlusAgentServerInternal\Setup\sql\GLMSysAIPlusAgentServerInternal.sql`): added idempotent **`CustomerID nvarchar(64)`** column.
- **§14 lifecycle rework (this change):**
  - **Issue** (no key yet) → generate + store + embed. **Preserve** (key exists) → no regen/redisplay; only extend `ExpiryDate`/`Active`; embed identity + expiry but **no** `APIKEY`. **Rotate** (explicit **"Rotate API Key"** button) → new key overwrites the row.
  - **`ExpiryDate` = license end date** (was +1yr) so auth tracks the subscription; **Renew (Action 5)** now extends the central row + carries the new `APIEXPIRY`, key preserved.
  - Field shows the plaintext (disabled) on Issue/Rotate, **masked** `KeyID/Last4` on Preserve. Detection reads the central row by `CustomerID`.
  - Customer apply split: `APIKEY` present → key+expiry; absent but `KEYID` present → expiry/active only (key preserved).
  - Expiry enforcement stays **purely central** — the validator already returns 401 on expired/inactive keys (`ExternalApiKeyValidator` unchanged); the customer just relays the 401.
- **Why:** WI — the AIPlus license should provision the Agent key so customers don't register it manually; and rotating a working key on every save (the first cut) breaks live integrations, so we moved to create-once / rotate-explicitly / disable-by-status.
- **Status:** Implemented; license-page project **builds clean**. Not yet runtime-verified for the §14 flows. Debug `agentKeySync` field kept in the customer callback for testing — **remove before production**.
- **Currently blocking:** None. **Parked (§15):** (1) repoint the **AIAgent 999** connection reads from `GLMSysCIConnections` → `GLMSysAIPlusProviderConnections` (`GLMSysAIPlusAgentExternalCallback.ashx` ~L274, `GLMSysAIPlusAgentClientCallBack.aspx` ~L2094/L2180, settings note ~L419) + add UserName/Password to the settings page; (2) retire `GLMSys.CI.AIAgent.Provider`; (3) optional operator "Disable/Revoke now" button. **Deploy:** rebuilt `GLMSys.License.Page.dll` + `GLMSysGenerateAddOnLicense.aspx` (central), `GLMSysLicenseUpdateCallBack.aspx` (customer), SQL on both DBs; copy the `.vb` back to CoreInternal.
- **Refs:** `AIPlus-Agent-API-Key-License-Integration-Plan.md` §14/§15; `GenerateAddOnLicense.vb`, `GLMSysGenerateAddOnLicense.aspx`, `GLMSysLicenseUpdateCallBack.aspx`, `GLMSysAIPlusAgentServerInternal.sql`; `Server.External\ExternalApiKeyValidator.cs` (unchanged).

## 2026-06-24 (+07:00) — Fix: explicit Windows credentials in customer bridge (ApplicationPoolIdentity support)
- **What:** Two related issues found during real-case setup with `ApplicationPoolIdentity` on the customer IIS app pool.
- **Issue 1 — Customer account request type visibility:**
  - `ResolveRequestTypeName` queries `AbsenceTypes` via `env.Connection`, which is scoped to the
    logged-in Synergy user. Customer-type accounts only see request types their user group is granted
    access to — so a customer account with no access to e.g. "kanban" gets 0 rows → AI replies with
    "I encountered an issue accessing the metadata for kanban requests."
  - **Resolved in Synergy configuration** (grant the customer account / user group access to the
    relevant request type in Workflow → Request Types). No code change needed.
- **Issue 2 — `ApplicationPoolIdentity` breaks outbound HTTP calls from customer bridge:**
  - `CallExternal` used `req.UseDefaultCredentials = true`, which sends the IIS app pool's Windows
    credentials via NTLM for every outbound call to the GLM API.
  - With a domain account pool identity (`radium\Client`): NTLM succeeds ✓
  - With `ApplicationPoolIdentity` (`IIS AppPool\DefaultAppPool`): this is a virtual machine-local
    account with **no network/domain credentials** → NTLM handshake fails against the GLM server's
    IIS → HTTP 500 on `/ai/ping` and 502 from the chat widget.
  - **Fix (`GLMSysAIPlusAgentExternalCallback.ashx`):**
    1. `TryGetExternalApi` now also SELECTs `UserName, Password` from `GLMSysCIConnections`
       (SoftwareID=999) and decrypts `Password` via the same `DecryptApiKey` helper used for `APIKey`.
    2. `CallExternal` signature extended with optional `windowsUser`/`windowsPassword`; when both are
       provided it uses `new NetworkCredential(user, password, domain)` instead of `UseDefaultCredentials`.
       `domain\username` format in `UserName` is automatically parsed.
    3. `UseDefaultCredentials = true` removed entirely — no fallback to pool identity.
  - **To activate:** fill in `UserName` (`domain\username`, e.g. `radium\Client`) and `Password` on
    the SoftwareID=999 row via the Connections UI (`VisibleFieldUserName` and `VisibleFieldPassword`
    are already `1` in `GLMSysCISoftwares` on the client database).
  - **Leave empty** to skip Windows auth and rely on API key only — works when the GLM server's IIS
    allows anonymous auth on the handler.
  - **Ping caveat:** the test connection ping (`/ai/ping`) is made by `GLMSys.CI.AIAgent.Provider.dll`
    (compiled ConnectIt provider), which also uses `UseDefaultCredentials` internally and cannot use
    these explicit credentials. Ping still requires either a domain pool identity OR anonymous auth on
    the GLM server's handler path.
- **Why:** Real-case deployment scenario where the customer-side app pool must use `ApplicationPoolIdentity`
  (no dedicated domain service account).
- **Status:** Done. Committed `43f35fb` on `yovan/user-story/#6421`.
- **Refs:** `Setup/docs/GLMSysAIPlusAgentExternalCallback.ashx` (`TryGetExternalApi`, `CallExternal`);
  `docs/DEPLOYMENT.md` §0d, §2b, §4; `docs/Major Refactoring References/07-KNOWN-ISSUES.md` §A.

## 2026-06-18 (+07:00) — Fix: external chat bubble rendered the raw JSON envelope (resultText ReferenceError)
- **Symptom:** on the **external** flow only, a query like "show top 5 kanban request" rendered the
  chat bubble as the **raw response envelope** — `{"status":200,"data":{"reply":"Top 5 Kanban
  Requests",…,"directDisplayData":"<the table HTML>"}}` — with the table rendered *inside* the literal
  JSON (JSON text top + a real table in the middle + `"}}` at the bottom). Internal chat was fine.
- **Misleading trails ruled out first (all verified):** deployed `.ashx`/`.js` were byte-identical to
  the repo; the **Network response was already clean** (`data.reply = "Top 5 Kanban Requests"`); the
  new JS *was* running (`appendAIAgentDirectDisplay.toString().indexOf('Caption guard')` → `290`);
  no missing/duplicate render functions; the GLM conversation DB had **0** envelope-polluted threads.
  So it was neither cache, nor a stale deploy, nor a bad server response.
- **Root cause (found via a temp diagnostic in the chat handler's `catch`):**
  `GLMSysAIPlusAgentChatEngine.js` `renderToolCallBadge` **read an undeclared `resultText`**
  (assigned only inside the `|||RESULT|||` branch at ~line 596, but read unconditionally at ~line 611).
  Reading a never-declared identifier throws `ReferenceError` in **all** modes (only *assignment* to one
  is the silent-global case — the file is non-strict, which misled the first analysis). The throw
  propagated to the chat handler's `try/catch`, whose fallback did
  `appendAIAgentMessage('assistant', xhr.responseText)` → `div.innerHTML = marked.parse(text)` →
  the envelope's embedded `directDisplayData` HTML rendered inline while the surrounding JSON showed as
  text. **External-only because** external tool-call badges (`ChatResponseEnricher.BuildToolCallBadge`)
  are `label|||argsJson` with **no `|||RESULT|||` segment**, so `resultText` was never assigned →
  ReferenceError; internal badges carry a result segment, so it was always defined there.
- **Fix (`GLMSysAIPlusAgentChatEngine.js`):** (1) declare `var resultText = null;` at the top of
  `renderToolCallBadge`; (2) **harden the handler `catch`** so a render error never dumps the raw JSON
  envelope into the bubble — it now falls back to `response.data.reply` and `console.error`s the
  exception. Syntax-checked (`node --check`), deployed to repo + customer `docs` + GLM `docs` (all three
  copies identical).
- **Status:** Done. Crash fixed; external table now renders as caption + table like internal.
- **Refs:** `Setup/docs/GLMSysAIPlusAgentChatEngine.js` (`renderToolCallBadge`, chat `onreadystatechange`
  catch); see also `docs/Major Refactoring References/07-KNOWN-ISSUES.md` §F.

## 2026-06-18 (+07:00) — Investigation: external "different columns/links" is prompt + data, not a code regression
- **Report:** the external chat's Request table showed an **empty HID** column and **no entity links**,
  while the internal chat showed the request number (`00.008.827`) and clickable Description/Request Type.
- **Verified the external code is byte-faithful to the proven `#6421` build (`f01b300`):**
  `ExternalAgentOrchestrator.cs` differs by **only** the `using Shared`→`Core` line; the whole
  `Server.External` project differs only in **auth** (`ExternalApiKeyValidator` decrypt-compare) and the
  new **`/ai/ping`** route; `GLMSysAIPlusAgentExternalCallback.ashx` differs only by the `DecryptApiKey`
  helper. Nothing in orchestration, prompting, tool execution, or table rendering diverged — the external
  flow reuses the **same** `GeneralToolExecutor`, `GeneralAgentPromptBuilder`, and `DataQueryHelper` as
  internal.
- **Actual cause (from the stored thread, ground truth):** the **shared** system prompt
  (`Server.Prompts.GeneralAgentPromptBuilder`, unchanged, used by *both* flows) explicitly orders
  *"REQUEST ENTITY DISPLAY RULES — ALWAYS include HID … NEVER select RequestID"* and *"Use HID instead of
  RequestNumber."* The LLM obeyed and selected `HID`. The link only renders on a column with a value, and
  **`HID` is empty in the customer DB's AI-created kanban records** but populated in the GLM `Synergy_503`
  DB (`00.008.827`). Same prompt + executor + renderer both sides; internal merely *looks* richer because
  its rows have numbers.
- **Conclusion:** not a bridge/parity bug. Open verification: confirm in the customer Synergy request
  screen whether those records actually have a request number (blank → pure data; populated-but-blank-in-chat
  → executor HID-resolution against the customer DB, a separate item). The two compared screenshots were
  also **different databases / different record sets**.
- **Refs:** `EntityRegistry.cs` (Request `LinkDisplayField=RequestNumber`), `DataQueryHelper.cs`
  (link requires `pageInfo`+`idVal`), `Server.Prompts` system prompt; `Server.External` diff vs `f01b300`.

## 2026-06-10 (+07:00) — Docs: QA test plan (setup → chat question)
- **What:** Added `docs/QA_TEST_PLAN.md` — a QA/acceptance script covering the **whole external-API
  path end to end**: binaries/web-files/ConnectIt/AzureOpenAI preconditions, the AIAgent provider +
  `SoftwareID=999` connection provisioning, provider **Test connection** (`/ai/ping`), the **Use
  External API** toggle (gate + persist), and **asking the chat widget a question** answered via the
  external API — with a Pass/Fail results table, troubleshooting matrix, and sign-off.
- **Why:** QA needs a single ordered checklist from a clean environment to a working chat question;
  complements the developer smoke test in `TESTING.md` §0 (references DEPLOYMENT/API_SPEC/DATABASE,
  doesn't duplicate).
- **Refs:** `docs/QA_TEST_PLAN.md`; cross-linked from `docs/TESTING.md` §0.

## 2026-06-10 (+07:00) — Fix: API-key auth must compare on the DECRYPTED key (Test connection 401)
- **Symptom:** the ConnectIt AIAgent provider's **Test connection** failed **401 "API key was
  rejected"** on the client side, even though the **chat widget worked** with the same connection.
- **Root cause:** the Connections UI **encrypts `APIKey` at rest** (`ConnectionMaintPage` →
  `Crypt.Encrypt` on save), but the validator compared the **raw column** to the bearer
  (`WHERE c.APIKey = @bearer`). The two client paths sent **different representations** of the key:
  chat (`TryGetExternalApi`) sent the **raw (encrypted)** column — which matched the GLM's raw column
  *only because both DBs are on the same dev machine / same cipher* — while the provider probe sent the
  **decrypted** `Connection.APIKey`, which never equals the encrypted column → 401. Encryption is
  non-deterministic, so the bearer can't be matched in SQL at all. (Also a **latent prod bug**: across
  two machines the encrypted blobs differ for the same key, so chat itself would 401.)
- **Fix (all paths agree on PLAINTEXT):**
  - `ExternalApiKeyValidator`: fetch active `SoftwareID=999` rows; match the bearer against each key's
    **decrypted** value (fallback to raw for plaintext/SQL-seeded keys). Replaces the SQL `APIKey` predicate.
  - `GLMSysAIPlusAgentExternalCallback.ashx` `TryGetExternalApi`: **decrypt** the stored key before
    sending it as `X-API-Key` (new `DecryptApiKey` helper; decrypt → fallback to raw). Feeds both
    `/ai/chat` and `/ai/tool-result`.
  - Provider probe already sends the decrypted `Connection.APIKey` (Synergy decrypts on load) — unchanged.
- **Why correct + cross-machine safe:** both installs decrypt to the **same plaintext** regardless of
  per-machine cipher → Test connection and chat both match.
- **Server-side Test connection 500** (GLM app probing its own loopback `.ashx`, no session → 3b env
  throws) is **out of scope by owner decision**: the server-side 999 row is API-key-only (no `APIUri`),
  so it isn't ping-tested — it just serves as the key registry the validator reads.
- **Build/deploy:** `Server.External.dll` → GLM `503\BIN`; updated `.ashx` → customer
  `…503_ClientAIPlusAgent\docs`. Committed (AIPlusAgent #6703).
- **Refs:** `Server.External\ExternalApiKeyValidator.cs`; `GLMSysAIPlusAgentExternalCallback.ashx`
  (`TryGetExternalApi`/`DecryptApiKey`); `docs/API_SPEC.md` §1; `docs/DATABASE.md` §1.3.

## 2026-06-10 (+07:00) — ConnectIt AIAgent provider (SoftwareID 999) + `/ai/ping` health route
- **What:** Made the AI Agent external API a *real* ConnectIt provider so the `SoftwareID=999`
  connection can be created **and "Test connection"-ed via the Synergy Provider/Connections UI**,
  instead of hand-inserting the `GLMSysCIConnections` row by SQL.
- **Root cause of the prior error** (`Could not load file or assembly 'GLMSys.CI.AIAgent.Provider'`):
  Synergy resolves a provider implementation by reflection from `GLMSysCISoftwares.ProviderName` —
  `assembly = "GLMSys.CI." + ProviderName + ".Provider"`, then loads `{asm}.Connection`,
  `{asm}.EntityService`, `{asm}.ConnectionMaintPage` (`GLMSys.CI.Provider\Helper.cs:89-93`,
  `EntityService.cs:44`, `ConnectionMaintPage.cs:405-415`). `ProviderName="AIAgent"` with no such DLL → load failure.
- **New project (ConnectIt repo): `GLMSys.CI.AIAgent.Provider`** (mirrors the minimal AzureOpenAI
  provider; GUID `405CA35A-607E-478E-9BE9-B44631E1F4CD`; added to `ConnectIt.sln`; post-build → `503\BIN`):
  - `Connection : REST.Provider.Connection` — overrides `Connect()` so a **connection test** probes
    `GET {APIUri}/ai/ping` with `X-API-Key` + `UseDefaultCredentials` (passes IIS Windows auth, like the
    Local Agent callback) instead of the stock REST entity-GET test (the agent endpoint is the custom
    `.ashx`, not a generic REST entity API). `200`→ok, `401`→key rejected, else/unreachable→`ConnectionException`.
  - `EntityService : REST.Provider.EntityService` — minimal (two constructors); all entity behaviour
    inherited (the provider is connection-only; chat runs through the `.ashx`, not ConnectIt CRUD).
- **New route (AIPlusAgent repo, `Server.External`): `GET /ai/ping`** in `ExternalAgentApiHandler`
  returns `200 {"status":"ok"}` **after** the existing key auth (so a valid key → 200, missing/invalid → 401).
- **Build/deploy:** both built green via MSBuild. `GLMSys.CI.AIAgent.Provider.dll` → GLM `503\BIN` (post-build)
  **and** copied to the customer bin `…503_ClientAIPlusAgent\bin` (where Test connection runs).
  `Server.External.dll` → `503\BIN`.
- **Status:** Built + deployed; **not yet runtime-verified** — owner to recycle both apps, confirm the
  `GLMSysCISoftwares` row has `ProviderName="AIAgent"` (API-key type, APIUri+APIKey visible), then click
  **Test connection** on the 999 connection.
- **Two repos = two commits:** provider in ConnectIt; ping route in AIPlusAgent (#6703).
- **Deferred (owner decision):** repeatable `GLMSysCISoftwares` + 999-connection **seed script** (UI-created for now).
- **Refs:** `ConnectIt\GLMSys.CI.AIAgent.Provider\{Connection,EntityService}.cs`, `ConnectIt.sln`;
  `Server.External\ExternalAgentApiHandler.cs`; `docs/API_SPEC.md` §5a.

## 2026-06-10 (+07:00) — Gate "Use External API" toggle on a SoftwareID=999 connection row (WI #6703)
- **What:** The Settings toggle is now **disabled/greyed only when no `GLMSysCIConnections` row with
  `SoftwareID=999` exists** on the customer DB — so an admin can't route chat to an external API that
  isn't configured. **Existence only** (no `Active`/`APIUri`/`APIKey` usability checks): if a 999 row
  exists (even if inactive/misconfigured) the toggle stays usable — that's the owner's rule.
- **`get_settings`:** returns `externalApiExists` = `SELECT TOP 1 ID FROM GLMSysCIConnections WHERE SoftwareID=999`.
- **`save_settings`:** **coerces `useExternalApi` to 0** when no 999 row exists, so a previously-stored `1`
  self-heals once the connection is removed and a crafted request can't enable external with no endpoint.
- **Settings page:** when `externalApiExists` is false the toggle is `disabled`, **forced OFF**, and shows a
  "not configured (SoftwareID=999)" info note; `toggleUseExternalApi` no-ops while disabled. (Older server
  responses without the flag are treated as enabled, so nothing breaks.)
- **Also fixed:** mangled API-Routing-card markup that shipped in the prior commit (`< div` / `</ div >` /
  `< button` and the button-group opening tag) which broke the card's HTML rendering.
- **Routing left as-is** (per owner): `get_route`/`ResolveExternalChatUrl` unchanged — a 999 row that exists
  but is misconfigured + external enabled surfaces the external callback's existing "not configured" error.
- **Status:** Done (uncommitted at time of writing). No DLL/build change (runtime-compiled `.aspx`).
- **Refs:** `Setup\docs\{GLMSysAIPlusAgentSettings.aspx, GLMSysAIPlusAgentClientCallBack.aspx}`.

## 2026-06-09 (+07:00) — "Use External API" settings toggle + no-refresh dynamic routing (WI #6703)
- **What:** Exposed `GLMSysAIPlusAgentUseExternalApi` in the **Agent Settings UI** and made the
  internal⇄external chat route switch **without a page refresh**. (Branch `yovan/user-story/#6703`.)
  - **Settings page (`GLMSysAIPlusAgentSettings.aspx`):** new *API Routing* card with a **"Use External
    API"** toggle, mirroring the *Debugging Options* toggle pattern (Vue `settings`/`originalSettings`,
    `toggleUseExternalApi()`, `updateToggleState`, and load/save/reset wiring).
  - **Callback `get_settings`/`save_settings` (`GLMSysAIPlusAgentClientCallBack.aspx`):** read & persist
    the setting (`BacoSettings`, `SettingGroup='AIPlus'`, `ValueType=0`; `1`=external, `0`=internal).
  - **New `get_route` action** on the internal callback: returns the live `chatUrl` from the setting
    (direct `BacoSettings` read; no admin gate — only the routing URL is exposed, page-level AIPlus
    license check still applies). Used by the widget to resolve the route at conversation start.
  - **Chat engine (`GLMSysAIPlusAgentChatEngine.js`):** `sendAIAgentMessage` now wraps
    `_doSendAIAgentMessage` via `ensureChatRoute()` — resolves the route **lazily on the first message of
    each conversation**, reuses it for the rest of the conversation (thread continuity), and re-resolves on
    **New chat** (`_aiAgentRouteResolved` reset alongside `_aiAgentConversationId`).
- **Two bugs found & fixed during this WI:**
  - **Save didn't persist:** the direct `BacoSettings` write ran only in the `set_Setting` `catch`, but
    `set_Setting` updates the session cache **without throwing**, so the row never changed. Now the table is
    written unconditionally (`UPDATE`, `INSERT` only when no row affected); `set_Setting` kept best-effort
    for cache coherence. Critical here because the router reads the **table**, not the cache.
  - **Stale toggle after `iisreset`:** `get_settings` read via `env.get_Setting` (per-session snapshot) and
    showed OFF while `StringValue='1'`. Switched to a **direct `BacoSettings` query**, matching
    `ResolveExternalChatUrl`, so toggle and routing share one live source of truth.
- **Why:** WI #6703 — let admins flip internal/external routing from the UI (no SQL), applied live.
- **How to resolve / how applied:** edits to the three `Setup\docs\` files; committed by owner. No DLL/build
  change (runtime-compiled `.aspx` + static `.js`). Updated `docs/DEPLOYMENT.md` §2b accordingly.
- **Status:** Done (code committed). Deploy the 3 `docs\` files to the live `docs` folder; one hard refresh
  to pick up the new chat-engine JS (the known no-cache-busting gotcha, §2b-note), then toggle applies with
  no further refresh.
- **Currently blocking:** None. (Pre-existing: `toolsDebug`/`baseModel` saves still use the old
  write-only-on-exception pattern → likely persist to the session cache only; offered to fix for consistency,
  not done.)
- **Refs:** `Setup\docs\{GLMSysAIPlusAgentSettings.aspx, GLMSysAIPlusAgentClientCallBack.aspx,
  GLMSysAIPlusAgentChatEngine.js}`; `AIAgentHelper.ResolveExternalChatUrl`; `docs/DEPLOYMENT.md` §2b.

## 2026-06-08 (+07:00) — Fix: tool_calls thread imbalance ("must be followed by tool messages")
- **Symptom:** after several questions, the widget intermittently errored:
  "An assistant message with 'tool_calls' must be followed by tool messages responding to each
  'tool_call_id'…".
- **Cause:** specific to conversationId threading — the server-side stored thread keeps
  `tool_calls`/`tool` messages across turns. If a tool loop is abandoned (customer hits its max
  tool rounds, errors, or the user sends a NEW question mid-loop), a dangling `assistant(tool_calls)`
  with no matching `tool` responses stays in the persisted thread; the next LLM `Step` sends it and
  the provider rejects it. (The old replay-text approach never carried tool messages, so it couldn't happen.)
- **Fix:** `ExternalAgentOrchestrator.RunLoop` now calls `EnsureToolCallBalance(thread)` before any LLM
  `Step` — removes assistant messages whose `tool_calls` aren't all answered + orphan `tool` messages.
  Mutates in place, so the persisted thread self-heals (broken conversations recover on the next turn).
  Built/deployed Server.External.dll → GLM, recycled.

## 2026-06-08 (+07:00) — Fix (root cause): read UseExternalApi directly from BacoSettings
- After centralizing the toggle (below), it STILL routed internal with the setting = '1'.
  Browser diagnostics on `_aiAgentConfig` proved: env non-null, the new DLL loaded, and
  `get_Setting(0,"GLMSysAIPlusAgentToolsDebug")` returned `"1"` — but BOTH
  `get_Setting(0, …UseExternalApi)` and `get_Setting(SettingType.General, …UseExternalApi)`
  returned `(null)`, even after the row was made byte-identical to ToolsDebug (Division=0 etc.)
  and after iisreset.
- **Root cause:** `env.get_Setting` serves a **per-session snapshot** of settings (taken at login).
  `ToolsDebug` existed at login (cached); `UseExternalApi` was **SQL-inserted during the session**,
  so `get_Setting` never sees it — and `iisreset` doesn't help because the user's session persists.
  A fresh install is fine, but a setting added to a running system is invisible to `get_Setting`.
- **Fix:** `AIAgentHelper.ResolveExternalChatUrl` now reads `BacoSettings` **directly** via
  `env.Connection` (QueryBuilder, `SingleValue` on `StringValue WHERE SettingName=…`), so the
  live value is always honored — works immediately after a SQL change, no re-login. Also future-
  proofs the upcoming Settings UI toggle.
- Verified: `_aiAgentConfig.chatUrl = "GLMSysAIPlusAgentExternalCallback.ashx"`. Diagnostics removed,
  clean `Client.PageExtension.dll` deployed to both bins.

## 2026-06-05 (+07:00) — Fix: UseExternalApi setting ignored by some widget paths (centralized)
- **Bug:** with `GLMSysAIPlusAgentUseExternalApi='1'`, chat still went to the internal callback.
  The `UseExternalApi → chatUrl` logic lived ONLY in `AIAgentHelper.RegisterAll` (page-extension
  path). But config is built by **three** paths, and the other two never read the setting:
  `PortalExtension` (global portal widget) and `AgentChatPageExtension` (standalone chat page) —
  both call `BuildConfigScript(...)` directly → always `callbackUrl` (internal).
- **Fix (centralized, removes the duplication):** the toggle is now resolved in ONE place —
  `BuildConfigScript` gained an `env` param and calls the shared `AIAgentHelper.ResolveExternalChatUrl(env)`
  to inject `chatUrl` when the setting is "1". The per-caller chatUrl blocks were removed; all three
  callers just pass `env`. Single source of truth → every injection path honours the toggle.
- Built/deployed `Client.PageExtension.dll` → both bins, recycled. SettingGroup is `'AIPlus'` in the
  SQL (matches live rows). New uncommitted files for the AIPlusAgent commit: `AIAgentHelper.cs`,
  `PortalExtension.cs`, `AgentChatPageExtension.cs`.

## 2026-06-05 (+07:00) — Install script completeness (Setup\sql\GLMSysAIPlusAgent.sql)
- Added the **`GLMSysAIPlusAgentUseExternalApi`** setting (BacoSettings, idempotent, default `'0'` =
  internal callback; `'1'` routes the widget chat to the external API). This is the toggle
  `AIAgentHelper` reads to set `chatUrl`; it didn't exist before, so a fresh page always fell back
  to the internal callback (the external route had only been forced via a console override).
- Folded in **`GLMSysAIPlusLog`** + **`GLMSysAIPlusFieldMismatch`** table creates (previously only in
  the dev-only `Client.Core\Scripts\GLMSysAIPlus.sql`, which isn't run by Setup — that's why
  `GLMSysAIPlusLog` was missing on the customer DB and had to be created by hand).
- Net: a new install now gets all addon tables (ScheduledTask, ActionToken, Conversation, Log,
  FieldMismatch) + settings (ToolsDebug, UseExternalApi) from one script — no manual steps.
  (GLMSysCILLMUsage + the SoftwareID=999 connection row remain ConnectIt/per-customer config.)

## 2026-06-05 (+07:00) — Per-conversation LLM usage tracking (GLMSysCILLMUsage.ConversationId)
- **Goal:** correlate token usage to a chat conversation so cost can be tracked per room.
- **No schema change needed** — `GLMSysCILLMUsage` already has `ConversationId UNIQUEIDENTIFIER NULL`
  + `SessionId NVARCHAR(100) NULL` (designed as optional correlation ids) + an index on ConversationId.
- **Approach (ambient seam):** the LLM-usage insert is deep in the generic ConnectIt AzureOpenAI
  provider; the conversationId lives in the AI-agent handler. Threading a param through the generic
  LLM abstraction would be invasive, so we use `env.Cache`:
  - `ConnectIt/GLMSys.CI.AzureOpenAI.Provider/EntityService.cs` — at the usage insert, reads
    `env.Cache["GLMSysCILLMUsageConversationId"]` / `["GLMSysCILLMUsageSessionId"]` and
    `AppendField`s them (best-effort; NULL when absent → all non-agent LLM use unchanged).
  - `Server.External/ExternalAgentApiHandler.cs` — sets those cache keys (conv.Id / conv.SessionId)
    before orchestration in `HandleChat` + `HandleToolResult`, clears them in `finally` (so they
    can't leak to unrelated LLM calls in a session env).
- Per-turn there are multiple usage rows (intent classification + main reply + tool rounds), all
  carrying the same ConversationId → `SUM(...) GROUP BY ConversationId` gives per-room cost.
  Short-circuit turns (capabilities/farewell/template-list/template-query) log nothing (no LLM).
- Both changes GLM-side; customer untouched. Built/deployed (AzureOpenAI provider + Server.External → GLM), recycled.

## 2026-06-05 (+07:00) — Widget conversationId threading (one chat room = one server thread)
- **Widget (`GLMSysAIPlusAgentChatEngine.js`):** track `_aiAgentConversationId`; in **external mode**
  (chatUrl set) send `{ message, conversationId }` instead of the full history; capture
  `data.conversationId` from each reply; clear on "New chat". Internal flow stays full-history
  (stateless). `_aiAgentMessages` still kept for rendering.
- **Result:** one chat room = ONE `GLMSysAIPlusAgentConversation` row, updated in place each turn
  (no more orphan row per message); GLM keeps the thread server-side. Verified: same conversationId
  across turns in the browser, single DB row.
- **Limitation (by design, for now):** the id is in-memory only → a page reload/navigation starts a
  new room. True "resume after reload" (and the future history sidebar) needs persisting the id in
  `sessionStorage`/`localStorage`. Deferred.
- ⚠️ **Cache caveat (cost us a debugging round):** the chat-engine JS is included with **no
  cache-busting** (`~/docs/GLMSysAIPlusAgentChatEngine.js`), so browsers serve the stale file until a
  hard refresh. Consider adding a `?v=<version>` in `AIAgentHelper.cs`/`PortalExtension.cs` so JS
  updates reach users automatically. Deferred.

## 2026-06-04 (+07:00) — External chat parity Batch 2: template-query form trigger (parity COMPLETE)
- **GLM (`ExternalAgentOrchestrator.PrepareUserTurn`):** added Step 4a — `TemplateQueryMatcher.Match`
  (reused) returns `SecuredAgentOrchestrator.TemplateQueryMarker + id` when a template matches.
  Not appended to the stored thread (it's a marker the callback consumes). Stores `_locale` for the matcher.
- **Customer (`GLMSysAIPlusAgentExternalCallback.ashx`):** detects the `[TEMPLATE_QUERY]<id>` reply and
  executes the template locally via `GeneralToolExecutor.ExecuteTemplateQuery` (mirrors the internal
  `.aspx` callback) → the form's table HTML flows out via `PendingDirectDisplayData`.
- Built/deployed (Server.External → GLM; callback → customer), recycled both.
- **Parity now complete** (Batch 1 + 2): capabilities, intent-aware prompt + tool filtering,
  farewell, template-list, previous-entity merge, template-query — all reuse the shared/internal
  building blocks (no duplication; internal SecuredAgentOrchestrator behavior unchanged, only
  4 helpers + the template marker made public).

## 2026-06-04 (+07:00) — Docs: full two-sided deployment manifest
- Expanded `docs/DEPLOYMENT.md` §2 into a complete file/setup manifest split by side:
  §2a GLM server (DLLs, locale/template JSON, conversation table, AzureOpenAI + SoftwareID=999,
  IIS/auth), §2b customer app (Client DLLs, callback `.ashx`, chat-engine JS, matching 999 key,
  `GLMSysAIPlusLog`, `GLMSysAIPlusAgentUseExternalApi=1`, **ConnectIt installed**), §2c the two
  common gotchas (matching 999 key + ConnectIt install), §2d the end-to-end flow diagram.

## 2026-06-04 16:20 (+07:00) — CRUD RESOLVED: ConnectIt prerequisite on the customer Synergy
- **Root cause (finally pinpointed):** the external-flow create cast
  (`Unable to cast MetadataEntity → GLMSys.CI.Data.Connection`) was **not** a code bug.
  Ground-truth diagnostics (full provider-result dump) showed create routes through the
  **OData path** (`Exact.Services.REST.DataServiceUpdateProvider.SaveChanges` →
  `System.Data.Services.DataService`) to the customer's own `Exact.Entity.Rest.svc`, and the
  cast is thrown **server-side** there by a ConnectIt write hook that couldn't resolve the
  `Connection`. Proof: identical failure via BOTH the internal `.aspx` and external `.ashx`
  callbacks on the customer install, while the GLM install (Synergy_503) created fine.
- **Fix:** **install ConnectIt on the customer Synergy** (`Synergy_503_ClientAIPlusAgent`).
  After install, create/update/delete work through both callbacks. Reads worked before because
  they don't hit the server-side write hook.
- **Therefore: ConnectIt is a deployment PREREQUISITE on every customer Synergy** that runs the
  AI agent (the agent uses the `GLMSys.CI` provider for all CRUD). Documented in `docs/DEPLOYMENT.md`.
- **Diagnostics removed (this was investigation scaffolding, now reverted):**
  - AIPlusAgent `EntityRecordService.cs`: `[DIAGV2]`/`[THROWN]`/`[RETURNED]` markers, widened
    `SanitizeErrorResponse`, full-result dump, raw `LogWarning` — all reverted.
  - External callback `.ashx`: temp `toolDebug` field — removed.
  - ConnectIt `ConnectionLink.cs` & `Helper.cs` cache guards + `[CU-CATCH]`/`[ES-CREATE-CATCH]`
    catch dumps — all reverted to baseline (they were never the fix).
  - Rebuilt baseline DLLs and redeployed (CI → GLM bin; `Client.Core` → both; clean `.ashx`),
    recycled both apps. Repos clean (AIPlusAgent fully; ConnectIt only the AzureOpenAI csproj).
- **Created `GLMSysAIPlusLog` table on the customer DB** (ran `Client.Core/Scripts/GLMSysAIPlus.sql`)
  — the app expects it for diagnostic logging; was missing. Kept (harmless, useful).
- **Note (re multi-turn memory):** the widget sends the full accumulated `_aiAgentMessages`
  history every turn, so cross-turn memory already works via replay (both flows). Threading the
  server-side `conversationId` is an OPTIONAL optimization (send new-message-only + id), deferred —
  naively adding it while still replaying history would duplicate the stored thread.

## 2026-06-03 17:17 (+07:00) — Pre-commit cleanup: revert unproven ConnectIt guards, drop temp debug code
- **Reverted the ConnectIt cache guards** (`GLMSys.CI.Data\ConnectionLink.cs`,
  `GLMSys.CI.Provider\Helper.cs`) back to baseline. They were a hypothesis for the
  external-flow create cast but a re-test still failed with the identical
  "MetadataEntity → Connection" error, so they fixed nothing. With CRUD parked, we
  don't commit speculative changes to the shared CI framework. Rebuilt + redeployed
  the baseline `GLMSys.CI.Data.dll` / `GLMSys.CI.Provider.dll` to both bins.
  **`GLMSysAIPlusAgentExternalCallback.ashx` create remains BROKEN/OPEN** — to be
  diagnosed properly when CRUD is resumed (next step: capture the FULL provider stack
  by temporarily raising `SanitizeErrorResponse` maxLength, since the real cast site is
  inside the repository `bc.Update()` path, not Helper.GetConnection).
- **Kept** `GLMSys.CI.AzureOpenAI.Provider.csproj` (501→503 HintPaths): not env-specific
  noise — this project uniquely pointed at a stale 501 install while every other ConnectIt
  project references 503; the mismatch caused the `BuildCreateUpdateUri` chat crash. The
  edit aligns it with the repo standard.
- **Removed the temp `toolDebug` field** from the external callback (declaration + populate
  + response field). It was CRUD-diagnosis scaffolding; re-add targeted logging when CRUD
  resumes. Deployed the cleaned `.ashx` to the customer docs.
- **Removed redundant code** in `ExternalAgentOrchestrator`: `BuildInitialThread` no longer
  builds a throwaway system prompt (PrepareUserTurn sets it per turn), and the now-unused
  private `BuildSystemPrompt(request)` was deleted. Rebuilt + redeployed Server.External.dll.
- **Status:** repos clean for commit — AIPlusAgent = chat parity + widget integration;
  ConnectIt = AzureOpenAI csproj only. Build green, no warnings.

## 2026-06-03 16:47 (+07:00) — Chat-response parity: external flow reuses the server-side pre-LLM pipeline
- **Problem:** external-flow replies were plainer than the internal server-side flow.
  E.g. "what can you do" returned generic LLM prose instead of the rich
  "Hello **{name}** — I'm your AI assistant…" capabilities card. Cause: the internal
  `SecuredAgentOrchestrator` runs a pre-LLM pipeline (capabilities/help template →
  intent classification → FULL intent-aware system prompt → intent-filtered tools)
  before any LLM call; `ExternalAgentOrchestrator` skipped all of it and passed
  all-nulls to `BuildSystemPrompt`, so the prompt lacked the formatting/section guidance.
- **Approach (owner-chosen): reuse the shared builders from the external project** — NOT a
  refactor of the working internal orchestrator (zero regression risk). All response LOGIC
  stays in the shared `public` classes; only the small sequencing lives in External.
- **Changes (Server.External only; Server.Service/Prompts untouched):**
  - `ExternalAgentOrchestrator.PrepareUserTurn(thread, request)` — new per-turn pre-LLM step:
    (1) `IntentClassifier.IsHelpQuery` → `AgentCapabilitiesBuilder.Build(context, null, userName, false)`
        short-circuit (identical capabilities card + `[SUGGESTED_PROMPTS]`); (2) `ClassifyWithEntity`
        → intents/entities/provider; (3) `GeneralAgentPromptBuilder.BuildSystemPrompt(intents,
        userMessage, detectedEntities, askUser, userContext, false)` set as thread[0] (rebuilt
        each user turn); (4) caches intents/provider.
  - `RunLoop` now `BuildTurnTools()` = `IntentToolFilter` on the General catalog (mirrors internal
    Step 6); on `/ai/tool-result` resume (no classification) it offers the full catalog.
  - `DocsFolder`/`LanguageCode` props + lazy locale-aware `IntentClassifier` (locale JSON loaded
    from the GLM `~/docs/` via `AgentLocaleLoader`, same files the internal flow uses).
  - Handler `HandleChat`: sets `DocsFolder = Server.MapPath("~/docs/")` + `LanguageCode`, calls
    `PrepareUserTurn` first (short-circuit → return; else RunLoop). `ExternalChatRequest` +`language`.
- **Reuse vs duplicate:** capabilities text, classifier, prompt sections, tool defs, intent
  filter = all the SAME shared classes. Only the if-sequence is in External (unavoidable — the
  external loop is resumable across HTTP, the internal is in-process).
- **Deferred (parity gaps, noted):** template-query marker (Step 4a), page-context shortcut (4a2),
  terminal-farewell (4b1), template-list chips (4b2), previous-entity merge + security entity
  fallback, last-active-entity hint. None affect the reported capabilities/formatting issue.
- **Status:** built (EXIT 0) + deployed `GLMSys.AIPlus.Agent.Server.External.dll` → GLM bin
  (auto-recycle). Owner to re-test "what can you do" via the widget/external callback.
- **Refs:** `Server.External\ExternalAgentOrchestrator.cs`, `ExternalAgentApiHandler.cs`,
  `ExternalChatRequest.cs`; reused `Server.Service\{AgentCapabilitiesBuilder,IntentClassifier,IntentToolFilter}`.

## 2026-06-03 15:53 (+07:00) — Fix (real root cause): external-flow create cast was in ConnectionLink
- **The 11:51 Helper.cs guard did NOT fix create** — re-test returned the identical
  "Unable to cast MetadataEntity to GLMSys.CI.Data.Connection". Diagnosis: the error is
  returned as an `EntityResult` error from inside the ExactSynergy provider's repository
  `CreateUpdate` catch (so it surfaces via `EntityRecordService.cs:172` "create failed: …"),
  and `AgentToolHelper.SanitizeErrorResponse` truncates to 300 chars, hiding the stack.
  That means the cast happens **during `bc.Update()`** (a ConnectIt component loads connection
  links on create), not in `Helper.GetConnection`.
- **Real culprit:** `GLMSys.CI.Data\ConnectionLink.cs:53/59` did a blind
  `(GLMSys.CI.Data.Connection)env.Cache["GLMSysCIConnection"+id]` and only fell back to
  `Helper.GetConnection` when the cached value was `== null`. A *poisoned* cache entry
  (a MetadataEntity, left under that key in the no-page .ashx context) is not null → the
  cast throws. The Helper guard never helped because ConnectionLink reads **different**
  connection IDs that the Helper path never re-cached.
- **Fix:** ConnectionLink.cs:53/59 now use `as GLMSys.CI.Data.Connection` (wrong-type or
  missing entry → null → rebuild via Helper.GetConnection, which re-caches a valid
  Connection). Also hardened `Helper.DisconnectAll` (Helper.cs:143) with the same `as` cast.
  Rebuilt `GLMSys.CI.Data.dll` + `GLMSys.CI.Provider.dll` → both bins.
- **Why .aspx worked but .ashx didn't:** the internal callback runs the full Synergy Page
  lifecycle which initialises the MetaModel cache cleanly; the .ashx skips it, so MetaModel
  caches a MetadataEntity under a key that collides with `GLMSysCIConnection+id`.
- **Status:** deployed; owner to re-test create from the customer widget.
- **Refs:** `ConnectIt\GLMSys.CI.Data\ConnectionLink.cs`, `ConnectIt\GLMSys.CI.Provider\Helper.cs`,
  `GLMSys.AIPlus.Agent.Client.Core\EntityRecordService.cs:172`.

## 2026-06-03 11:51 (+07:00) — Fix: external-flow create (CI cache guard) + "[shown]" tables
- **Create failure root cause (diagnosed via temp toolDebug):** `create_record` returned
  "Unable to cast 'Exact.Services.MetaModel.Entity.Data.MetadataEntity' to
  'GLMSys.CI.Data.Connection'." Traced to `GLMSys.CI.Provider.Helper.GetConnection`
  (Helper.cs:52): `env.Cache["GLMSysCIConnection"+connectionId]` held a MetadataEntity, not
  a Connection — an env.Cache collision in the no-page (.ashx) context (the in-process
  metamodel poisons the key). Reads worked (cache populated first); create read it back poisoned.
  **Fix (ConnectIt):** changed the cache check from `!= null` to `is GLMSys.CI.Data.Connection`
  so a poisoned entry is ignored and the Connection is rebuilt + re-cached. Robust for all
  providers; only changes the previously-crashing path. Rebuilt `GLMSys.CI.Provider.dll` →
  both bins. (Owner-approved CI framework change.)
- **"[shown]" placeholder tables:** the external flow sent `[DIRECT_DISPLAY]` tool results
  back to the LLM, which then narrated "Description: [shown] …". The internal orchestrator
  short-circuits direct-display (no final LLM call). **Fix:** external callback now
  short-circuits — when all tool results in a batch start with `[DIRECT_DISPLAY]`, it stops
  the loop (skips /ai/tool-result) and surfaces `PendingDirectDisplayCaption` +
  `PendingDirectDisplayData` (table) — matching the internal UX. Deployed.
- **Status:** deployed (bin change auto-recycles both apps); owner to re-test create + table.
- **Refs:** `ConnectIt\GLMSys.CI.Provider\Helper.cs`; `GLMSysAIPlusAgentExternalCallback.ashx`.

## 2026-06-03 11:28 (+07:00) — Phase 5c: rich tool-call badges in the external flow
- **What:** The widget worked through the external callback (tables render, links resolve),
  but the debug **tool-call badges** showed only the bare name (`Tool called: create_record`)
  instead of the internal flow's rich `get_entity_metadata (Exact Synergy - Synergy: Request)|||{args}`.
- **Fix:** Added `BuildToolCallLabel` + `ExtractRequestTypeFilterValue` + `BuildToolCallBadge`
  to the shared `ChatResponseEnricher` (mirrors `SecuredAgentOrchestrator.BuildToolCallLabel`
  + the callback's provider injection). External callback now adds
  `ChatResponseEnricher.BuildToolCallBadge(name, args)` per tool call, and respects the
  `GLMSysAIPlusAgentToolsDebug` setting (clears badges when off) — parity with internal.
  Kept a separate bare-name list for `ExtractUpdatedRecord`'s gate.
- **How applied:** rebuilt `Client.Core` (badge helpers) → deployed to both bins; deployed
  the external callback. Bin change auto-recycles the customer app (badges appear next chat).
- **Status:** badge parity done; re-test the widget.
- **Also noted (separate, to investigate):** "create new kanban request" returned
  "I encountered an error…" — a create_record failure in the external flow (the tool ran
  but errored). Needs the tool result text to diagnose (likely a field/arg issue).
- **Refs:** `ChatResponseEnricher.cs`; `GLMSysAIPlusAgentExternalCallback.ashx`.

## 2026-06-03 11:09 (+07:00) — Phase 5c (A): renamed external callback + chat-only widget routing
- **Renamed** `GLMSysAIPlusLocalAgentHandler.ashx` → **`GLMSysAIPlusAgentExternalCallback.ashx`**
  (class + directive; repo + customer docs). Old customer copy left (unused; sandbox blocks delete).
- **Option A wired (chat-only, opt-in, reversible):**
  - `AIAgentHelper.RegisterAll`: when Synergy setting **`GLMSysAIPlusAgentUseExternalApi = 1`**,
    emits `chatUrl: 'GLMSysAIPlusAgentExternalCallback.ashx'` into `_aiAgentConfig`.
  - Chat-engine JS `sendAIAgentMessage`: chat posts to `_aiAgentConfig.chatUrl || callbackUrl`
    (only the chat send; `apply`/`autocomplete` stay on the internal callback).
  - Built `PageExtension`; deployed DLL → customer bin; chat-engine JS → customer docs.
- **Net:** with the setting on, the customer widget's CHAT goes through the external API
  (GLM-orchestrated, customer-executed tools) with rich parity (tables/nav/updatedRecord);
  everything else stays on the internal callback. Off (default) = unchanged behavior.
- **Status:** deployed; owner to test the widget against the external callback.
- **Deferred (fast-follow):** email enrichers (table-in-email + action-link) — plain email
  already flows; only table-embedded / action-link emails are degraded until ported. Then
  graduate to B (full drop-in).
- **Refs:** `AIAgentHelper.cs`, `GLMSysAIPlusAgentChatEngine.js`, `GLMSysAIPlusAgentExternalCallback.ashx`.

## 2026-06-03 10:35 (+07:00) — Phase 5c: shared ChatResponseEnricher + Local Agent parity (part 2)
- **What:** Created `GLMSys.AIPlus.Agent.Client.Core.ChatResponseEnricher` — the shared
  post-processing helper used by BOTH the internal callback and the customer Local Agent
  (owner's choice: shared helper, no duplication). Moved `ExtractSuggestedPrompts` and
  `ExtractUpdatedRecord` (verbatim) into it.
  - Callback (`GLMSysAIPlusAgentClientCallBack.aspx`): Steps 7/8 now call
    `ChatResponseEnricher.*` (the inline copies are superseded — flagged for removal).
  - Local Agent (`GLMSysAIPlusLocalAgentHandler.ashx`): accumulates the assistant
    tool_calls + tool-result turns into a loop messages array and now returns
    `updatedRecord` (same-record refresh) and `suggestedPrompts` (no-op until the help
    short-circuit is added) via the shared helper — on top of `directDisplayData` +
    `navigateUrl` from part 1.
- **How applied:** Built `Client.Core` (helper compiles), deployed `Client.Core.dll` to
  BOTH bins (server post-build + copy to customer); deployed the Local Agent. The
  callback's helper switch is in the repo but **not yet pushed to the deployed callbacks**
  (it works either way; deploy with the normal process) to avoid overwriting production
  callbacks now.
- **Status:** Local Agent chat parity now covers tables, navigation, same-record refresh,
  suggested prompts (wired). **Remaining for full parity: the EMAIL flow** — pre-LLM
  `[EMAIL_TABLE_CONTEXT]` injection (customer-side, before /ai/chat) + post-`[EMAIL_PREVIEW]`
  processing (table HTML, entity→URL links, action-link token via ActionTokenService).
  That's the last piece before repointing the widget.
- **Refs:** `ChatResponseEnricher.cs`; `GLMSysAIPlusLocalAgentHandler.ashx`;
  callback Steps 7/8.

## 2026-06-03 10:14 (+07:00) — Phase 5c (option B): Local Agent enrichment, part 1
- **Decision:** owner chose **full UX parity** (enrich the Local Agent to reproduce the
  callback's rich chat output, then repoint the widget) — not a minimal repoint.
- **What (part 1):** Local Agent now also accepts the widget's chat shape
  (`{action:"chat", messages:[full history]}`) and **surfaces the executor's rich
  side-effects** in the response (since it runs the real `GeneralToolExecutor`):
  `directDisplayData` (HTML table) and `navigateUrl` (auto-open) — the two most visible
  features. Falls back to `PendingDirectDisplayCaption` for the reply when the model
  returns no text but a table exists.
- **Status:** deployed to the customer app.
- **Remaining for full parity (with a design fork):**
  - `suggestedPrompts` — only emitted by the help/capabilities short-circuit, which the
    external orchestrator doesn't run (low effort if we add that short-circuit).
  - `updatedRecord` — same-record page refresh after update/create (moderate).
  - **`[EMAIL_PREVIEW]` injection — the big one** (table HTML + entity-link resolution +
    action-link token via ActionTokenService; ~150 lines inline in the callback).
  - FORK: duplicate these inline in the `.ashx` (high duplication, esp. email) **vs**
    extract the callback's post-processing into a **shared helper** both call (less
    duplication; a safe refactor of the callback). Recommend shared helper for email.
- **Then:** repoint widget chat to the Local Agent (AIAgentHelper `chatUrl` + chat-engine
  JS), keeping non-chat actions (apply/autocomplete/settings/templates/drilldown) on the
  internal callback.
- **Refs:** `GLMSysAIPlusLocalAgentHandler.ashx`; callback `ProcessChat` post-processing.

## 2026-06-02 21:40 (+07:00) — ✅ Phase 5b VERIFIED with REAL DATA (full pipeline)
- **What:** The Customer Local Agent works end-to-end against the real customer DB.
  - "List 3 accounts" → 3 **real** accounts with real `entity://Account/<guid>` links;
    `toolCallsExecuted: [query_entity_data, query_entity_data]`.
  - "How many open requests do I have?" → ran `get_entity_metadata`, then asked which
    request type (real General-agent resolution) — correct behavior.
- **Switched Local Agent from `.aspx` to `.ashx`:** the `Page.Base` `.aspx` returned
  Synergy's framework "System Error" page on a direct JSON POST (pre-`Page_Load`
  lifecycle/security; my try/catch never ran). Rewrote as `GLMSysAIPlusLocalAgentHandler.ashx`
  (`IHttpHandler, IRequiresSessionState`, env via `Environment.Current()`) — same pattern
  as the external API handler. Works. (The dead `.aspx` remains in the customer docs only
  because the sandbox blocked deleting under `C:\Exact…`; harmless, nothing calls it — can
  be removed manually.)
- **Proven chain:** customer `.ashx` → external GLM API (server-to-server, 3b constructed
  env, X-API-Key) → tool_calls → real local execution (GeneralToolExecutor + live
  SynergyEntityRightsProvider, option A) → /ai/tool-result → final reply w/ real data.
- **Status:** Phase 5b DONE & verified. The full work-item flow (server orchestrates,
  customer executes tools, real data) is proven.
- **Next:** Phase 5c — point the chat widget at the Local Agent so the UI uses the external
  API. Then Phase 4 (quota/expiry); production cross-machine needs anonymous IIS auth.
- **Refs:** `GLMSysAIPlusLocalAgentHandler.ashx`.

## 2026-06-02 21:24 (+07:00) — ✅ 3b VERIFIED + Phase 5b: Customer Local Agent
- **3b verified:** PowerShell `-UseDefaultCredentials` (Windows-auth, NO Synergy session) →
  HTTP 200 + real reply. The constructed-env path works; the AppPool identity already has
  Synergy config access (no IIS identity change needed). Removed the temp debug detail;
  clean DLL rebuilt/deployed.
- **Phase 5b — Customer Local Agent:** new `Setup\docs\GLMSysAIPlusLocalAgentHandler.aspx`
  (deployed to the **customer** app `...503_ClientAIPlusAgent\docs`). Self-contained `.aspx`
  (reuses the already-deployed client DLLs — no new DLL to push). It:
  1. reads the external API URL+key from the customer's `GLMSysCIConnections` SoftwareID=999;
  2. POSTs `/ai/chat` to the GLM API server-to-server (`HttpWebRequest`,
     `UseDefaultCredentials` + `X-API-Key`), passing user identity (env.ResourceID + humres name);
  3. executes returned `tool_calls` **locally** via `GeneralToolExecutor` with live
     `SynergyEntityRightsProvider` rights (option A — customer enforces);
  4. POSTs `/ai/tool-result`, loops to a final reply; returns `{reply, conversationId,
     toolCallsExecuted}` to the widget.
- **Why:** Phase 5 — turns the proven loop into real tool execution against the customer DB.
- **Status:** deployed; owner to test from a logged-in customer session (new `.aspx` compiles
  on first hit — no iisreset needed customer-side; server already has working 3b loaded).
- **Scope/next:** General context only for now (other contexts reuse the same pattern);
  Phase 5c = repoint the chat widget to this Local Agent. Production cross-machine needs
  anonymous IIS auth (localhost server-to-server works via Windows auth).
- **Refs:** `GLMSysAIPlusLocalAgentHandler.aspx`; `docs/ARCHITECTURE.md` §2.2; `docs/API_SPEC.md`.

## 2026-06-02 21:09 (+07:00) — Option 3b: construct env without a session (anonymous)
- **What:** Implemented `GlmServerEnvironmentProvider`'s integration point to build an
  `Exact.Core.Environment` for no-session (server-to-server) requests:
  `new Exact.Core.Environment("GLMSysAIPlusAgentExternalAPI", "/DBCONFIG:<vdir>",
  ProcessOptions.AllowAnonymousDatabaseConnection)`. Order: EnvironmentFactory →
  Environment.Current() (3c dev/browser) → constructed (3b). `<vdir>` resolves from
  `DbConfigName` override, else the request ApplicationPath (e.g. "/Synergy_503" →
  "Synergy_503"), else "Synergy_503" (case-sensitive, must match the IIS vdir).
- **How signature was obtained:** reflected the real `Exact.Core.dll` — confirmed ctor
  `(string ProcessName, string CommandLine, ProcessOptions Options)` and the
  `ProcessOptions.AllowAnonymousDatabaseConnection` value. (Also saw a direct
  `(Server, Database, Integrated, SQLUser, SQLPass, DBMS, localRoot)` ctor as a future
  alternative that avoids config decryption.) Incidentally found the prior env-init
  debug notes under Project Brief\Misc\Old — used only to confirm the AppPool root cause
  (not the code); no old code reused.
- **Known prerequisite (server config, not code):** the IIS AppPool identity for the
  Synergy_503 site must be a privileged Windows account that can read/decrypt the Synergy
  connection config (like Exact.Process.exe). The restricted DefaultAppPool throws
  `ArgumentNullException "g"`. Anonymous IIS auth is also needed for truly credential-less
  callers (the 3b path can be tested first via Windows-auth, no Synergy session).
- **Status:** Built + deployed (21:09, with a TEMP debug detail on the env-acquisition
  catch). Owner to iisreset + test the 3b path (PowerShell -UseDefaultCredentials =
  Windows-auth, no Synergy session → forces constructed env).
- **Refs:** `GlmServerEnvironmentProvider.cs`; `docs/DEPLOYMENT.md` §4; `docs/ARCHITECTURE.md` R4.

## 2026-06-02 20:59 (+07:00) — Phase 5a: user-context in prompt; surfaced 3b dependency
- **What:** External API `/ai/chat` now accepts optional end-user identity
  `{ "user": { "resourceId": N, "fullName": "..." } }`; `ExternalAgentOrchestrator`
  injects it as a `UserContext` into the system prompt (via the existing
  `GeneralAgentPromptBuilder.BuildSystemPrompt(..., userContext)` overload). Fixes
  `CURRENT USER: Unknown` for new conversations. Built + deployed (20:59).
- **Why:** Prereq for "me/my" resolution and for the Local Agent (Phase 5b).
- **KEY REALIZATION (blocks 5b):** the real Customer Local Agent calls the GLM external
  API **server-to-server** (customer app -> GLM `.ashx`), so there is **no Synergy_503
  session** on that call. Option **3c** (`Environment.Current()`) only worked because we
  tested from a browser logged into Synergy_503. For the Local Agent / real production,
  the external API must run **anonymously** → we need **option 3b** (construct
  `Exact.Core.Environment` without a session) + **anonymous IIS auth** on the `.ashx`.
  3c stays as the dev/test shortcut.
- **Status:** 5a done (verifiable now via console with a `user` field, 3c). 5b (Local
  Agent) is **gated on 3b**.
- **Next:** implement option 3b (constructed env via `GlmServerEnvironmentProvider`'s
  EnvironmentFactory or integration point) + enable anonymous IIS auth for the handler;
  then build the Local Agent.
- **Refs:** `ExternalChatRequest.cs`, `ExternalAgentOrchestrator.cs`; `docs/ARCHITECTURE.md` R4;
  `docs/DEPLOYMENT.md` §4.

## 2026-06-02 20:51 (+07:00) — ✅ Phase 3 part 2 VERIFIED (full tool loop, both sessions)
- **What:** End-to-end tool loop confirmed with a stub customer executor, from BOTH a
  Synergy_503 session and the customer-app browser session.
  - Server-side run: chat → tool_calls(get_entity_metadata) → tool-result →
    tool_calls(read_records) → tool-result → tool_calls(get_entity_metadata) → final reply
    (3 rounds).
  - Customer-side run: chat → tool_calls(get_entity_metadata) → tool-result →
    tool_calls(query_entity_data) → tool-result → final reply ("You have 3 open requests").
  Confirms: tool_calls returned by /ai/chat, /ai/tool-result resumes, conversation state
  binds tool_call_ids across HTTP calls, multi-round loops terminate.
- **Known gap (not a bug):** the system prompt shows `CURRENT USER: Unknown` — the external
  orchestrator doesn't inject the end-user identity yet, so "how many requests do I have"
  can't resolve "I". This is the deferred customer-context input (PRD §8.3 / decision #3) —
  resolve in Phase 5 (pass user identity from the customer, or from env under option 3c).
- **Status:** Phase 3 (parts 1 & 2) DONE & verified. The external API now fully orchestrates
  server-side with customer-side tool execution.
- **Next:** Phase 5 (real customer Local Agent: map tool_calls → IAgentToolExecutor; +
  user-context injection; repoint widget); Phase 4 (quota/idle-expiry). Production-anonymous
  still needs option 3b + anonymous IIS auth.
- **Refs:** ROADMAP Phases 4/5; `docs/API_SPEC.md` §3,§7.

## 2026-06-02 20:41 (+07:00) — Phase 3 part 2: tool offering + /ai/tool-result (option A)
- **What:** The external API now offers tools and runs the customer-side tool loop.
  - `ExternalAgentOrchestrator`: replaced `RunStep` with `RunLoop` + `StepOutcome`.
    RunLoop offers the context tool defs (General set), runs `AgentChatService.Step`;
    on tool_calls it appends the assistant tool_calls message, executes **server-handled**
    tools in-process (`search_documentation` via `DocumentationGroundingService`, looped),
    and returns any **customer** tool calls for local execution. **Option A:** no
    server-side entity-rights filtering — the customer enforces rights on execution.
  - `ExternalAgentApiHandler`: `/ai/chat` now returns either a final reply or an assistant
    `tool_calls` message (sets conversation Status=awaiting_tool_result). Implemented
    `/ai/tool-result`: load (scoped to customer) → 409 if not awaiting → append the
    customer's `tool` messages (not sanitised) → resume `RunLoop` → return next
    reply/tool_calls. Added `BuildChatResponse`; removed the unused `NotImplemented` helper.
- **Why:** ROADMAP Phase 3 — the core handoff: server orchestrates, customer executes tools.
- **How to resolve / how applied:** Built (EXIT=0), deployed to 503 BIN (20:41). No changes
  to Server.Service/Server.Prompts (RunLoop composes Step + GeneralAgentPromptBuilder +
  DocumentationGroundingService).
- **Status:** Code done & deployed; **owner to iisreset + run the tool-loop test** (with a
  stub customer executor in the console — real executor is Phase 5).
- **Currently blocking / next:** real customer Local Agent (Phase 5) to execute tools for
  real; entity-rights filtering stays customer-side (option A); non-General contexts +
  Globe tools later.
- **Refs:** `ExternalAgentOrchestrator.cs`, `ExternalAgentApiHandler.cs`; `docs/API_SPEC.md` §3,§7.

## 2026-06-02 20:27 (+07:00) — ✅ Phase 3 part 1 VERIFIED (server-side memory) + Load fix
- **What:** Multi-turn memory works end-to-end. T1 created a conversation; T2 (sending only
  the `conversationId`, not the history) correctly replied **"Your name is Yovan"**;
  `GET /ai/conversation/{id}` returned the stored thread (`status:"active"`); `/ai/reset`
  closes it. So Create + Load + Save + history + reset all function.
- **Fix applied during verification:** `ConversationStore.Load` threw "Specified cast is
  not valid" on `(Guid)rows[0,0]` — EDL returns `uniqueidentifier` in a form that won't
  hard-unbox to Guid here. Changed to parse via `Guid.TryParse(Convert.ToString(...))` and
  read the result with `as object[,]`. (Earlier same session: fixed the `DBNull` SessionID
  insert error.) Removed the temporary debug text from both catch blocks.
- **Why:** Confirms the conversation store (the Phase 3 foundation the tool handoff needs).
- **How verified:** logged-in Synergy_503 console, multi-turn fetch with `X-API-Key`.
- **Status:** Phase 3 part 1 DONE & verified. Clean (debug-free) DLL deployed 20:27 —
  needs one iisreset to load.
- **Currently blocking / next:** Phase 3 part 2 — offer tools + return `tool_calls` +
  implement `/ai/tool-result` continuation (currently 501), plus the entity-rights
  filtering decision.
- **Refs:** `ConversationStore.cs`; `docs/API_SPEC.md` §2–5.

## 2026-06-02 19:56 (+07:00) — Fix: conversation insert failed on DBNull SessionID
- **What:** `/ai/chat` returned 500 "Could not persist the conversation." Real error
  (via temp debug): `Conversion from type 'DBNull' to type 'String' is not valid.`
- **Why:** `ConversationStore.Create` passed `DBNull` for the **`SessionID` (uniqueidentifier)**
  column; the EDL `InsertBuilder` can't stringify `DBNull` for a uniqueidentifier (it's
  fine for nvarchar/int, which is why `ScheduledTaskService` never hit it). T1 sent no
  `sessionId`.
- **How to resolve / how applied:** Omit the `SessionID` field entirely when there's no
  valid GUID (nullable column → defaults to NULL); only `AppendField` when a real session
  GUID is present. Removed the unused `ToGuidOrNull` helper and the temporary debug text.
  Rebuilt + deployed (19:56). The `GLMSysAIPlusAgentConversation` table was confirmed to
  exist in `Synergy_503` with the correct schema.
- **Status:** Fixed; awaiting owner iisreset + multi-turn retest.
- **Refs:** `ConversationStore.cs`.

## 2026-06-02 18:43 (+07:00) — Phase 3 (part 1): server-side conversation memory
- **What:** Added server-side conversation state so chat is stateful and the LLM loop can
  continue across turns (foundation for the /ai/tool-result handoff). Decision (confirmed
  with owner): **new table `GLMSysAIPlusAgentConversation`** (AI-Agent-owned, Messages as a
  JSON blob); `GLMSysCILLMUsage` left untouched (it already auto-logs usage). Rationale:
  Azure OpenAI Chat Completions is stateless (no conversation id in the response), so the
  AI Agent must own the ConversationId and store the thread.
  - `Setup\sql\GLMSysAIPlusAgent.sql`: idempotent CREATE TABLE (ID=ConversationId,
    CustomerConnectionID isolation key, SessionID, Context, Messages nvarchar(max),
    Status, Created, Modified) + index.
  - `ConversationStore.cs` (+ `ConversationRecord`): Load/Create/Save/Reset via
    InsertBuilder/UpdateBuilder/QueryBuilder + conn.Exec; every op scoped by
    CustomerConnectionID.
  - `ExternalChatRequest`: added optional `sessionId` (conversationId already supported).
  - `ExternalAgentOrchestrator`: split into `BuildInitialThread` (system prompt + msgs)
    and `RunStep` (one LLM turn, appends assistant reply) — replaces RunChatReply.
  - `ExternalAgentApiHandler`: `/ai/chat` now stateful (new → build+store; existing →
    load by id scoped to customer, append turn, save). Implemented `/ai/conversation/{id}`
    (returns stored thread, 404 if not owned) and `/ai/reset` (closes the conversation).
- **Why:** ROADMAP Phase 3 foundation; tool handoff depends on remembering the thread.
- **How to resolve / how applied:** Built (EXIT=0), DLL deployed to 503 BIN (18:42).
  `Server.Service`/`Server.Prompts`/`GLMSysCILLMUsage` unchanged.
- **Status:** Code done & deployed. **Owner must run the CREATE TABLE on the Synergy_503
  DB, then iisreset + retest** (multi-turn memory).
- **Currently blocking / next:** Tool offering + `/ai/tool-result` continuation is the
  next increment (`/ai/tool-result` still returns 501 until then). Security/entity-rights
  filtering decision comes with tool offering.
- **Refs:** `docs/DATABASE.md` §4; `docs/API_SPEC.md` §2–5.

## 2026-06-02 18:06 (+07:00) — ✅ Phases 1–2 VERIFIED LIVE (external API chat works)
- **What:** First successful end-to-end call to the deployed external API. From a
  logged-in `Synergy_503` console: `POST .../GLMSysAIPlusAgentExternalAPI.ashx/ai/chat`
  with `X-API-Key: test-key-001` → **HTTP 200** with
  `{"conversationId":"…","messages":[{"role":"assistant","content":"I am your AI assistant…"}]}`.
- **Why:** Validates Phase 1 (transport + API-key auth + routing) and Phase 2
  (orchestration: prompt builder + AgentChatService.Step → Azure OpenAI → reply).
- **How verified:** browser console fetch from the logged-in Synergy_503 tab (option 3c
  session). Confirms: X-API-Key auth, GLMSysCIConnections SoftwareID=999 validation,
  `Environment.Current()` returned a valid env (3c works — **3b not needed for dev**),
  AzureOpenAI provider call succeeded (BuildCreateUpdateUri fix held).
- **Status:** Phase 2 DONE & verified. Ready to start Phase 3.
- **Currently blocking:** None for Phases 1–2. Note for production: true anonymous
  (no-session) access still needs option 3b + anonymous IIS auth (deferred); usage
  metering still deferred.
- **Refs:** `docs/ROADMAP.md` Phase 3; `docs/TESTING.md` §0.

## 2026-06-02 17:40 (+07:00) — Fixed LLM-call crash (stale Azure OpenAI CI provider)
- **What:** Chat (internal widget AND would-be external API) failed with
  `MissingMethodException: GLMSys.CI.REST.Provider.EntityService.BuildCreateUpdateUri(Boolean, Object)`.
  Root cause: in current ConnectIt source the method is **3-param**
  `BuildCreateUpdateUri(bool, object, JObject=null)`, and `GLMSys.CI.AzureOpenAI.Provider`
  overrides/calls the 3-param base — but the **deployed `GLMSys.CI.AzureOpenAI.Provider.dll`
  was stale (5/25)**, compiled when it was 2-param, so its IL called a 2-param overload
  absent from the freshly-rebuilt (6/2) 3-param `REST.Provider.dll`.
- **Why it was stale:** `GLMSys.CI.AzureOpenAI.Provider.csproj` was the **only** ConnectIt
  project referencing `C:\Exact Synergy Enterprise 501\bin\` (which doesn't exist on this
  machine) for Exact.Core/Data/Newtonsoft — all 39 sibling projects use `503`. So it alone
  failed to rebuild during the framework rebuild and stayed at the old 2-param version.
- **How to resolve / how applied:** Edited that csproj's 3 HintPaths `501` → `503`
  (aligning it with every sibling), then rebuilt it (ConnectIt uses ProjectReference, so
  CI.Data/CI.Provider/REST.Provider rebuilt too). Post-build deployed a **matched** set to
  `C:\Exact Synergy Enterprise 503\BIN\` (AzureOpenAI.Provider + REST.Provider both 6/2 17:39).
  **File changed is OUTSIDE the AIPlusAgent repo** (ConnectIt framework).
- **Status:** Fixed; **owner to iisreset + retest** (internal widget "hi" and/or the external
  API console fetch — both share this LLM path).
- **Currently blocking:** None known for the LLM call. If a new `MissingMethod` appears, it
  means another deployed CI DLL is stale vs. source → rebuild that provider the same way.
- **Refs:** `ConnectIt\GLMSys.CI.AzureOpenAI.Provider\EntityService.cs` (L578),
  `ConnectIt\GLMSys.CI.REST.Provider\EntityService.cs` (L3326).

## 2026-06-02 14:43 (+07:00) — Documented quick manual smoke test
- **What:** Added `docs/TESTING.md` §0 "Quick manual smoke test (deployed external API)"
  — prerequisites (iisreset, `999`+`AzureOpenAI` rows, logged-in `Synergy_503`),
  the `X-API-Key` auth note, ready-to-paste browser-console `fetch` snippets for the 4
  cases, and a result-interpretation table (200 ✅ / 401 / 500→3b / 502 provider).
- **Why:** Owner ready to test; needed concrete, repeatable steps for the current 3c
  (session-based) build.
- **How to resolve / how applied:** Doc-only.
- **Status:** Done. Awaiting owner's iisreset + test result.
- **Currently blocking:** A 500 result would confirm `Environment.Current()` is null in
  the `.ashx` → triggers option 3b (constructed env).
- **Refs:** `docs/TESTING.md` §0.

## 2026-06-02 14:26 (+07:00) — Fixed whole-solution build (missing PdfPig in bin)
- **What:** Full-solution rebuild was failing with errors that looked like code bugs
  (`RequestTypeToolExecutor.EnforceEntityRights` "not marked virtual",
  `UseBusinessComponent*`/`GetCreateKeyProperties` "no suitable method to override",
  ExactGlobe `DirectQueryConfig` "no parameter named virtualFields"). Diagnosed as
  **cascade symptoms**, not bugs.
- **Why:** Root cause = `UglyToad.PdfPig*.dll` (PdfPig 0.1.14) **missing from**
  `C:\Exact Synergy Enterprise 503\bin\` (the csproj HintPath target), present only in
  `packages\PdfPig.0.1.14\`. So `Client.Core` failed (`CS0103 'UglyToad'`), produced no
  fresh DLL, and every dependent project compiled against the **stale `Client.Core.dll`**
  → the override/param mismatches. Compounded by projects using **file references**
  (HintPath→bin) instead of project references, so a parallel/whole-solution build
  compiles against stale bin DLLs.
- **How to resolve / how applied:** Copied the 7 `UglyToad.PdfPig*.dll` (the **net462**
  lib — NuGet-correct for a net47 project) into `C:\Exact Synergy Enterprise 503\bin\`,
  then rebuilt **in dependency order** (Shared → Suggestion → VectorSearch → Client.Core
  → Server.Prompts → Client → Client.RPA → Client.ExactGlobe → Scheduler → Server.Service
  → PageExtension → Server.External). Result: **all 12 OK**.
- **Status:** Done. Whole solution builds; all DLLs in bin now consistent with source.
- **Currently blocking:** None for build. Note: PdfPig DLLs are also a **runtime**
  dependency (PDF text extraction) and must ship to each server/client bin.
- **Recommendation (not done):** convert the inter-project file references to
  **ProjectReference** so VS/MSBuild always builds in correct order and avoids the
  stale-bin race. Larger change touching all csproj — propose before doing.
- **Refs:** `Client.Core\DocumentTextExtractor.cs` (UglyToad usage); per-project csproj
  HintPaths.

## 2026-06-02 14:14 (+07:00) — Deployed my handler; added X-API-Key auth; test handoff
- **What:** (1) Overwrote the old live `.ashx` with my one-liner
  (`→ GLMSys.AIPlus.Agent.Server.External.ExternalAgentApiHandler`) and redeployed
  `External.dll` to `C:\Exact Synergy Enterprise 503\BIN\`. (2) Handler now implements
  `IRequiresSessionState` and the env seam falls back to `Exact.Core.Environment.Current()`
  (option 3c) for session-based testing. (3) Added **`X-API-Key`** header support
  (checked before `Authorization: Bearer`).
- **Why:** Live probe proved my handler runs and `PathInfo` routing works, but behind
  IIS **Windows Auth** the NTLM handshake **overwrites `Authorization`**, so the Bearer
  token was lost (handler returned 401 "missing key"). `X-API-Key` dodges this — the
  same workaround the prior attempt used.
- **How to resolve / how applied:** Edited `ExternalAgentApiHandler` (ExtractApiKey:
  X-API-Key → Authorization) + `GlmServerEnvironmentProvider` (Current() fallback);
  rebuilt **only** `Server.External` (rebuilding `Server.Service` from current source
  fails — stale `Shared.dll` in BIN missing `AgentDelegationRouter`; not needed, the
  deployed DLLs already provide the members used). Updated `docs/API_SPEC.md` auth.
- **Status:** Deployed; **owner to iisreset + refresh (slow laptop) and test via
  browser/widget**.
- **Currently blocking / notes:** Option 3c needs the request to carry a Synergy
  session for `Environment.Current()` to return non-null; if it returns null even with
  a session in an `.ashx`, we move to 3b (constructed env). Anonymous IIS auth (#2)
  intentionally NOT enabled yet — it would remove the session 3c relies on; it belongs
  with the 3b production path. `Server.Service` in BIN still carries old external types
  (harmless now the old `.ashx` is replaced).
- **Refs:** `docs/API_SPEC.md` §1; `docs/ARCHITECTURE.md` §4.5; ROADMAP Phase 2/3.

## 2026-06-02 13:38 (+07:00) — Live probe of deployed endpoint (test findings)
- **What:** Probed `http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx`.
  Findings: (1) anonymous POST → **IIS 401** with `WWW-Authenticate: Negotiate,NTLM`
  (HTML) — the `docs/` path enforces **Windows Authentication**, so anonymous Bearer
  requests never reach the handler; (2) with Windows creds → `{"status":401,"error":
  "Unauthorized."}` — that envelope is the **old** attempt's, i.e. the deployed
  `.ashx` (`C:\Exact Synergy Enterprise 503\docs\GLMSysAIPlusAgentExternalAPI.ashx`)
  is the previous-attempt handler (inline class `GLMSysAIPlusAgentExternalAPIHandler`,
  uses `Exact.Core.Environment.Current()` → needs a Synergy session), and the
  `Server.Service.dll` in `BIN` still carries the old `ExternalAgentOrchestrator`.
- **Why:** Owner asked to test; needed to know the real deployed state.
- **How to resolve / how applied:** Diagnosis only — no files overwritten (old `.ashx`
  left untouched pending owner approval, per the "ask first about old files" rule).
- **Status:** Done (diagnosis). End-to-end test **blocked**.
- **Currently blocking (3 items):**
  1. **IIS auth** — `docs/` requires Windows auth; anonymous Bearer is rejected by IIS
     before our code runs. Need Anonymous Authentication on the `.ashx` (or a dedicated
     anonymous path/app).
  2. **Stale deployment** — live `.ashx` + `Server.Service.dll` are the old attempt;
     must deploy my one-line `.ashx` (→ `GLMSys.AIPlus.Agent.Server.External.ExternalAgentApiHandler`)
     and the current `Server.Service`/`Server.Prompts` builds. (Old `.ashx` overwrite
     needs owner OK.)
  3. **Env seam for anonymous** — anonymous = no Synergy session, so
     `Environment.Current()` is null. Must supply env via
     `GlmServerEnvironmentProvider.EnvironmentFactory` or a constructed
     `Exact.Core.Environment` (needs an AppPool identity able to read the `Synergy_503`
     DB config). This is the core unsolved problem from the prior attempt.
- **Refs:** `docs/ARCHITECTURE.md` R4; `docs/DEPLOYMENT.md` §4; `CLAUDE.md` §0.

## 2026-06-02 13:14 (+07:00) — Phase 2: real chat orchestration (final replies)
- **What:** Added real `/ai/chat` orchestration to `GLMSys.AIPlus.Agent.Server.External`,
  reusing the existing LLM core with **no** `Server.Service`/`Server.Prompts` changes.
  New/changed files:
  - `ExternalChatRequest.cs` — parses bare-array or object body (`context`/`messages`/
    `conversationId`); `context` defaults to `General`.
  - `ExternalAgentOrchestrator.cs` — composes `GeneralAgentPromptBuilder.BuildSystemPrompt()`
    + `AgentChatService.SanitizeMessages` + `AgentChatService.Step(messages, [])` and
    returns the assistant's final reply. Phase 2 offers **no tools** (General tools are
    all customer-side; no server-handled tool in General), so Step yields a direct reply.
  - `ExternalAgentApiHandler.cs` — replaced the Phase 1 stub with `HandleChat(...)` that
    runs the orchestrator and returns the API_SPEC chat shape; provider failures → 502
    `provider_error` (no internal details leaked). Removed now-unused parsing helpers.
  - `.csproj` — included the two new files.
- **Why:** ROADMAP Phase 2 — prove the external orchestration path
  (API → env → AgentChatService.Step → Azure OpenAI → reply) end-to-end.
- **How to resolve / how applied:** Rebuilt with MSBuild (Debug/AnyCPU) — **succeeded**;
  DLL post-built to `C:\Exact Synergy Enterprise 503\BIN\`. Empty-tools Step is an
  established path (SecuredAgentOrchestrator uses it for summarisation-only calls).
- **Status:** Done (code) / **pending server verification** (needs env seam wired —
  same blocker as Phase 1; also requires an active `AzureOpenAI` row in the `Synergy_503`
  `GLMSysCIConnections`).
- **Currently blocking / deferred to Phase 3 (by design, coupled):** customer-side tool
  offering + entity-rights filtering, server-side conversation state, and the
  `/ai/tool-result` continuation. Also deferred: usage metering to `GLMSysCILLMUsage`
  (blocked — `ChatStepResult` does not surface token counts and `Server.Service` must
  not be modified this WI; needs a token-usage surface or the table insert schema).
  Non-General contexts currently fall back to the General prompt.
- **Refs:** `docs/ROADMAP.md` Phase 2/3; `docs/ARCHITECTURE.md` §4.2; `docs/API_SPEC.md` §2.

## 2026-06-02 13:08 (+07:00) — Documented dev/test topology (two Synergy installs)
- **What:** Recorded the dev topology: **GLM server** install
  `C:\Exact Synergy Enterprise 503` (`http://localhost/Synergy_503/docs/Portal.aspx`,
  hosts the external API) and **external customer app** install
  `C:\Exact Synergy Enterprise 503_ClientAIPlusAgent`
  (`http://localhost/Synergy_503_ClientAIPlusAgent/docs/Portal.aspx`, executes tools).
  Concrete API endpoint:
  `http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx`.
- **Why:** Owner provided the real folders/URLs; needed for deploy + testing and to
  ground the `SoftwareID=999` `APIUri`.
- **How to resolve / how applied:** Added `docs/DEPLOYMENT.md` §0 (topology table +
  consequences) and updated §8 environments; made `docs/API_SPEC.md` base URL
  concrete; added a pointer in `CLAUDE.md` §1.
- **Status:** Done.
- **Currently blocking:** None. (Also noted: a prior external-AI-Agent attempt exists
  outside the repo and is **not** used as reference per owner instruction.)
- **Refs:** `docs/DEPLOYMENT.md` §0/§8; `docs/API_SPEC.md` §1; `CLAUDE.md` §1.

## 2026-06-02 13:02 (+07:00) — Phase 1: external API skeleton + auth + chat stub
- **What:** Created the new project **`GLMSys.AIPlus.Agent.Server.External`** (.NET 4.7
  class library) in `d:\yvnalv\Projects\Addons\AIPlusAgent` and added it to
  `GLMSys.AIPlus.Agent.sln`. New files:
  - `IAgentEnvironmentProvider.cs` + `GlmServerEnvironmentProvider.cs` — the single,
    swappable environment-acquisition seam (settable `EnvironmentFactory` for
    host/test wiring; explicit INTEGRATION POINT otherwise).
  - `ExternalApiKeyValidator.cs` + `CustomerContext.cs` — parameterized Bearer-key
    lookup on `GLMSysCIConnections` (`SoftwareID=999 AND APIKey=@key AND Active=1`);
    customer identity = matched row `ID`; fail-closed.
  - `ApiResponseWriter.cs` — JSON success + standard error envelope
    (`{ "error": { "code", "message" } }`).
  - `ExternalAgentApiHandler.cs` — `IHttpHandler`; Bearer auth on **every** request;
    routes `ai/chat` (Phase 1 stub), `ai/tool-result`/`ai/conversation/{id}`/`ai/reset`
    (→ `not_implemented`, still behind auth), unknown → 404, method checks → 405.
  - `Setup\docs\GLMSysAIPlusAgentExternalAPI.ashx` — thin WebHandler pointing to the
    compiled handler class.
- **Why:** ROADMAP Phase 1 — prove transport + API-key auth end-to-end before wiring
  orchestration.
- **How to resolve / how applied:** Built with MSBuild (Debug/AnyCPU) — **succeeded**;
  post-build copied the DLL to `C:\Exact Synergy Enterprise 503\BIN\`. Reused the
  existing `ConnectionHelper`/`QueryBuilder` patterns; did **not** modify
  `Server.Prompts` or `Server.Service`.
- **Status:** Done (code) / **pending server verification**.
- **Currently blocking:** Live verification of the exit criteria (valid key → 200
  stub; invalid/missing → 401) requires the environment-acquisition seam to be wired
  on the GLM server: set `GlmServerEnvironmentProvider.EnvironmentFactory` at app
  startup **or** implement its INTEGRATION POINT, plus enable Anonymous Auth on the
  handler path and use an AppPool identity that can read the Synergy DB config
  (`docs/DEPLOYMENT.md` §4). Until then `/ai/chat` with a valid key returns 500
  (`server_error`) and the auth-rejection path (missing/malformed header → 401)
  works without env.
- **Refs:** `docs/ROADMAP.md` Phase 1; `docs/API_SPEC.md`; `docs/ARCHITECTURE.md`
  §4.5; `docs/DEPLOYMENT.md` §4.

## 2026-06-02 12:45 (+07:00) — Open questions resolved; decisions locked
- **What:** Recorded the product owner's answers to `docs/PRD.md` §8 and updated all
  affected docs. (1) Conversation state = **server-side store**; (2) keep
  `SoftwareID=999` as-is, multi-customer keys deferred to a future WI;
  (3) customer-context = **existing approach** (rights→JWT + logged-in user's
  menu/page access, sent in request); (4) JWT **kept as-is** for now;
  (5) `.ashx` = **anonymous, Bearer-only**; (6) project name =
  **`GLMSys.AIPlus.Agent.Server.External`**.
- **Why:** Unblock Phase 1 by removing design ambiguity.
- **How to resolve / how applied:** Updated `docs/PRD.md` §8 (Open questions →
  Resolved decisions), `CLAUDE.md` §9, `docs/CONTRIBUTING.md` decision log,
  `docs/ARCHITECTURE.md` §4.4, `docs/DATABASE.md` §4, `docs/API_SPEC.md` header;
  mirrored to project memory.
- **Status:** Done.
- **Currently blocking:** Nothing blocked. Remaining non-blocking defaults: usage
  metering per call (per-key quota later), non-streaming v1.
- **Refs:** `docs/PRD.md` §8; `docs/CONTRIBUTING.md` §6.

## 2026-06-02 (earlier) — Initial design documentation created
- **What:** Authored the full documentation set for the external API:
  `CLAUDE.md`, `README.md`, and `docs/`: `PRD.md`, `ROADMAP.md`, `ARCHITECTURE.md`,
  `DATABASE.md`, `API_SPEC.md`, `CODING_STANDARDS.md`, `TESTING.md`,
  `DEPLOYMENT.md`, `CONTRIBUTING.md` (all were previously empty).
- **Why:** Documentation-first work item: design the external API (customer-side
  tool execution + Bearer key via `SoftwareID=999`) before any code.
- **How to resolve / how applied:** Analyzed the codebase
  (`d:\yvnalv\Projects\Addons\AIPlusAgent`); confirmed framework, current flow,
  orchestrator design, config usage; wrote the design of record. Reuse strategy:
  `ExternalAgentOrchestrator` composes the public `AgentChatService.Step` + prompt
  builders + classifiers; `Server.Prompts`/`Server.Service` untouched.
- **Status:** Done.
- **Currently blocking:** (at the time) the §8 open questions — since resolved by the
  entry above.
- **Refs:** entire `Project Docs/` folder.

## 2026-06-02 (analysis finding) — Prior memory corrected: external API artifacts absent
- **What:** Verified that `GLMSysAIPlusAgentExternalAPI.ashx`,
  `GLMSysAIPlusLocalAgentHandler.aspx`, and `LLMUsageService.cs` — claimed by an
  older note as already implemented — **do not exist** in the current branch (HEAD).
- **Why:** Avoid building on a false premise; the external API is green-field.
- **How to resolve / how applied:** File search across the repo confirmed absence;
  treated the external API as a fresh build that reuses existing assemblies; project
  memory corrected.
- **Status:** Done (informational).
- **Currently blocking:** None.
- **Refs:** `CLAUDE.md` §0; `docs/ROADMAP.md` "Tracking note".

---

## Confirmed baseline (reference, not a change)
- Framework: **.NET Framework 4.7**; all class-library DLLs; HTTP today via
  WebForms `.aspx`; no `.ashx` exists yet.
- Current flow is internal/direct: chat widget → `GLMSysAIPlusAgentClientCallBack.aspx`
  (customer server, in-process) → `SecuredAgentOrchestrator` → `AgentChatService.Step`
  → Azure OpenAI (customer's own credentials); tool execution local.
- **No production code written for the external API yet.** Next: Phase 1
  (`ROADMAP.md`).
