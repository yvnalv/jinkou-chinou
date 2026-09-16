# TROUBLESHOOTING — External AI Agent API: failure / symptom / confirm / debug / fix

Complete failure matrix for the external AI Agent chat path, from the widget through the
customer bridge to the GLM server and back. Companion to `ENV_INIT_AND_AUTH.md` (why the
environment fails), `DEPLOYMENT.md` §2 (what to deploy) and `07-KNOWN-ISSUES.md` §A.

> **Verified against:** `AIPlusAgentServerInternal` @ `6054d82` + the uncommitted
> `GetEnvironment()` rewrite; `AIPlusAgent` @ `fa08193`; Synergy 505, `Exact.Core 5.0.0.737`.
> **Line numbers move.** Treat them as anchors, not addresses — search the quoted symbol if a
> line no longer matches.

**Project legend:** **[SI]** `AIPlusAgentServerInternal` · **[AP]** `AIPlusAgent` ·
**[EG]** `AIPlusAgentEG` · **[SV]** `AIPlusAgentServer` · **[EX]** Exact framework (no source)

---

## 0. Triage in four questions

Answer these in order; each one eliminates whole sections below.

| Question | How | If… |
|---|---|---|
| 1. Did the request reach the handler? | Break at **[SI]** `GlmServerEnvironmentProvider.cs:11`. Or: is the error page **HTML** (pre-handler) or **JSON** (in-handler)? | Not reached → **§4 rows 17-22** only |
| 2. Which identity arrived? | IIS log `cs-username` column | blank → §3 row 14; unexpected account → §2 rows 5, 9 |
| 3. Is the deployed build current? | SHA256 of `GLMSys.AIPlus.Agent.Server.External.dll` vs §7 | stale → §4 row 21 |
| 4. Does that identity map to a Synergy resource *on the GLM server*? | `humres` query in §7 | no → §4 rows 17-20 |

**HTML error page ⇒ the failure is before `ProcessRequest`, and no change inside the handler
can affect it.** That single distinction is the fastest cut through this document.

---

## 1. Route selection (customer side)

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 1 | `GLMSysAIPlusAgentUseExternalApi` ≠ `'1'` | Chat runs locally; `{"useExternalApi":false,"chatUrl":""}` | `SELECT * FROM BacoSettings WHERE SettingName='GLMSysAIPlusAgentUseExternalApi'` | **[AP]** `ClientCallBack.aspx:2144-2168` `ProcessGetRoute`; break **:2156**, watch `useExternal` | Set `StringValue='1'` |
| 2 | Duplicate setting rows (`'AIPlus'` + `'general'`) | Readers disagree; `SingleValue` picks arbitrarily | Same query returns >1 row | **[AP]** `ClientCallBack.aspx:2153-2156` (filters `SettingGroup='General'`) vs `AIAgentHelper.cs:138` (name only) | Delete the stray row; fix the installer's `IF NOT EXISTS` group vs `INSERT` group mismatch |
| 3 | `env.set_Setting` silently no-ops | Provider set default but flag stays `'0'` | Row unchanged after the action | **[AP]** `ClientCallBack.aspx:3510` / **:3542**; step over, then re-query | Move the raw SQL fallback out of `catch`; verify by read-back |

---

## 2. Customer reads its own config (bridge / Globe)

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 4 | No `SoftwareID=999` row | `"External AI Agent API is not configured"` 500 | `SELECT COUNT(*) FROM GLMSysAIPlusProviderConnections WHERE SoftwareID=999` | **[AP]** `ExternalCallback.ashx:85` guard; `:262` `TryGetExternalApi` returns false | Issue a key via the admin callback |
| 5 | **2+ `SoftwareID=999` rows** | Settings "Test connection" → **400**; chat intermittently uses wrong key/credentials | Count > 1 | **[AP]** `ExternalCallback.ashx:273-276` (`TOP 1`, **no `ORDER BY`**) — inspect `row[0..3]`; **and** `ClientCallBack.aspx:4035-4040` — watch `Rows.Count` / `Rows[0]` | Remove stale rows; add `ORDER BY` + `Active=1`; filter the test path by `providerId` |
| 6 | `APIUri` wrong or has a scheme/path already | Connection refused, wrong host | Inspect the value | **[AP]** `ExternalCallback.ashx:282` — watch `apiUri` after `+ "/docs/…ashx"` | Store the **base URL only** |
| 7 | `APIKey` fails to decrypt | `403 invalid or inactive API key` | Compare `Last4` with the issued key | **[AP]** `ExternalCallback.ashx:299-303` `DecryptApiKey` — compare input vs output | Re-issue and store via the Settings page, never raw SQL |
| 8 | `Password` fails to decrypt | `401` at IIS; repeated failed logons → lockout | Windows Security log `4625` | **[AP]** same `:299-303`; watch `windowsPassword` at `:291` | Fix `catch { return storedKey; }` to fail loudly |
| 9 | **Globe `GLMSysGlobeAgentUsername`/`Password` blank** | `UseDefaultCredentials` sends the *workstation* account | `SELECT SettingName, StringValue FROM BacoSettings WHERE SettingName LIKE 'GLMSysGlobeAgent%'` | **[EG]** `ExternalTransport.cs:190-201` `ApplyCredentials` — break **:197**; config at `GlobeConnectionConfigReader.cs:133-143` | Populate the settings. **Globe does not read the 999 row** |
| 10 | Client DB restored/moved | Every decrypt returns garbage | Several 401/403 appear at once after a restore | **[AP]** same decrypt points | Re-enter key and password through the UI (`Crypt` is keyed to the connection) |

---

## 3. NTLM to the GLM server

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 11 | Proxy/CDN strips `Authorization: Negotiate` | `401`, never reaches ASP.NET | IIS log `401 2 5`; no ASP.NET event | **Not debuggable in code** — IIS + Security logs | Bypass the proxy, or move to anonymous + key-only |
| 12 | **Password expired / locked / disabled** | `401.2` | Security log `0xC000006E`, sub `0xC0000071` | **Not code** — Windows Security log | Reset; never-expires or gMSA |
| 13 | Domain-qualified vs bare mismatch | `DOMAIN\user` → 401, bare works (or vice versa) | Test both forms | **[AP]** `ExternalCallback.ashx:335-338` — watch the `domain`/`user` split | Send the form the server accepts |
| 14 | Anonymous auth unexpectedly enabled | Request arrives with no identity → dies in §4 | `appcmd list config "<site>/docs" /section:anonymousAuthentication` | **Not code** — IIS config | Choose the mode deliberately |
| 15 | Loopback check (same-machine tests) | 401 with correct credentials over IP | Works via `localhost`, fails via IP | **Not code** | Test through `localhost` |
| 16 | Host unreachable / firewall | Timeout, `WebException` | `Test-NetConnection` | **[AP]** `ExternalCallback.ashx:355-370` catch — watch `wex.Message` | Network / firewall |

---

## 4. Environment construction ⭐ *(where the production error lives)*

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 17 | **No `humres.usr_id` row on the GLM server** | **HTML** 500 before `ProcessRequest`; locally `ArgumentNullException "g"` | `humres` query in §7, run on **the GLM server's DB** | **[EX] not debuggable** — fires in `global.asax:57` → `Session_OnStart`. Use Event Viewer **ASP.NET 1309**. Break **[SI]** `GlmServerEnvironmentProvider.cs:11`; **if it never hits, you are here** | Create the Synergy resource — **no code, no deploy** |
| 18 | `usr_id` domain-qualified or space-padded | As 17 | `SELECT '[' + usr_id + ']'` | Same as 17 | Store the **bare** account name |
| 19 | `ldatuitdienst` past / `ldatindienst` future | As 17 | Same query | Same as 17 | Correct the dates |
| 20 | `UserLicenseType = 0` | As 17 | Same query | Same as 17 | Assign a licence |
| 21 | **Old DLL → background ctor inside a request** | `"Initializing the Environment here is not allowed"` at `ProcessRequest +0` | SHA256 vs §7 | **[SI]** `GlmServerEnvironmentProvider.cs:49` (tier 4). In the current build this is unreachable while `ctx != null` — break **:28** and watch `ctx` | Deploy the current build |
| 22 | Cold start after deploy / app-pool recycle | `EDLTimeoutException … Query = bacoGetTerms`; 35-57 s then 500 | Event 1309; IIS `time-taken` spike | **[EX] not debuggable** — event log only | Warm-up request; AlwaysRunning + Application Initialization |
| 23 | `/DBCONFIG` unresolvable (root-hosted `'/'`) | Tier 4 skipped with an explicit message | Response body / trace | **[SI]** `GlmServerEnvironmentProvider.cs:97` `ResolveDbConfigName` — step all four branches | `<add key="GLMSysAIPlusAgentDbConfig" value="…" />` |
| — | `blocked = 1` | **Not a failure.** Tested 2026-09-03: still returns `{"status":"ok"}` | — | — | — |

**Environment breakpoint set** — **[SI]** `GlmServerEnvironmentProvider.cs`:

| Line | Watch | Meaning |
|---|---|---|
| **11** | *(hit or not)* | Not hit ⇒ died in `Session_OnStart` (rows 17-22) |
| **24** | `current` | Tier 2 — the session environment |
| **28** | `ctx` | Must be non-null in a web request |
| **32** | `inRequest` | Tier 3 — the in-request constructor |
| **62** | `failure` | All tiers failed; this string is the whole story |
| **66 / 80** | `inner.GetType().Name`, `inner.Message` | Per-tier exception, otherwise swallowed |

Also enable **Debug → Exception Settings → CLR Exceptions → `System.Exception`** (break when
thrown) — Exact's guard is a plain `System.Exception` and `Attempt` swallows it.

---

## 5. API key validation

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 24 | `KeyID` not found | `403 "Invalid or inactive API key"` | Compare `KeyID`/`Last4` on both sides | **[SI]** `ExternalApiKeyValidator.cs:24` (`keyId`), `:30-33` (query) — watch `rows` | Re-issue |
| 25 | `Active=0` or `ExpiryDate` passed | Same | Server-side 999 row | **[SI]** `ExternalApiKeyValidator.cs:62` | Reactivate / extend |
| 26 | Key re-issued on the server | Customer's stored copy stops matching | `Last4` differs | **[SI]** `:54` `Crypt.Decrypt`, `:59` `FixedTimeEquals` | Re-distribute after every re-issue |
| 27 | Malformed key (e.g. `test-key-001`) | `403` — `ParseKeyId` rejects | Format: `glm_live_`/`glm_test_` + 22 + 32 base62 | **[SI]** `ExternalApiKeyGenerator.ParseKeyId` via `:24` | Use a real key |

---

## 6. Routing, orchestration, response

| # | Failure | Symptom | Confirm | Where to debug | Fix |
|---|---|---|---|---|---|
| 28 | Product mismatch | Synergy prompts for a Globe caller | `Product` column / `X-Product` header | **[SI]** `ExternalAgentApiHandler.cs:500` `ResolveProduct`; branch at `:141` | Set `Product='globe'` |
| 29 | **`ExactGlobe.Server.dll` missing from GLM `bin`** | Globe `/ai/chat` → 502/500 | File listing | **[SI]** `ExternalAgentApiHandler.cs:141-148` — `new GlobeExternalOrchestrator` throws `FileNotFoundException` | Deploy from **[EG]**; the External post-build copies **only** its own DLL |
| 30 | Locale JSONs missing from `docs\` | Capabilities/intent pipeline degrades | `GLMSysAIPlusAgentLocale_*.json` present? | **[SI]** `:203` `PrepareUserTurn`; `ResolveDocsFolder` | Deploy all five locales |
| 31 | `GLMSysAIPlusAgentConversation` missing | 500 `"Could not persist the conversation"` | Table exists? | **[SI]** `:225-226` `store.Create` / `store.Save` | Run the setup SQL |
| 32 | **`.aspx` newer than `Server.Service.dll`** | `CS1061 … no definition for 'SelectedProvider'` compile page | Compilation-error page names the line | **[AP]** `ClientCallBack.aspx:1077` vs **[SV]** `SecuredAgentOrchestrator.cs:40` | Deploy the matched DLL set |
| 33 | AzureOpenAI / ConnectIt misconfigured | `502 provider_error` | `GLMSysCIConnections` row | **[SI]** `:205` `RunLoop`; catch at `:207` — inspect the swallowed exception | Fix the connection/model |
| 34 | Long LLM call vs `executionTimeout=550` | Request aborted mid-chat | IIS `time-taken` | **[SI]** `:87` / `:92` `.GetAwaiter().GetResult()` | Raise the timeout or shorten the loop |
| 35 | No `TrySkipIisCustomErrors` | JSON error bodies replaced by IIS HTML | Body is markup on any non-2xx | **[SI]** `ApiResponseWriter.cs:24-27` — compare with `ApiKeyCallBack.ashx` `WriteRaw` | Add the line |
| 36 | `customErrors mode="Off"` on production | Full stack traces served to customers | The error page's own footer says so | **Not code** — `web.config` | Set `RemoteOnly` |
| 37 | 401 for a missing API key | Browser re-prompts; .NET clients retry NTLM | Double credentials popup | **[SI]** `ExternalAgentApiHandler.cs:35-42` | **Fixed 2026-09-03** — now `403` |
| 38 | `xhr.timeout = 10000` on the settings page | "Request timed out" on a cold compile | First hit after a recycle | **[AP]** `general.js:61` and the `provider.js` equivalents | Raise it, or warm up first |
| 39 | Stale DLLs in one install only | Works in one app, fails in another | Hash-compare both `bin` folders | **Not code** — file compare | Deploy the full matched set |
| 40 | App-domain restart window | 502 / timeouts for ~1 min after any DLL copy | IIS `time-taken` spike | **Not code** | Warm-up request after deploy |
| 41 | PDB not deployed | Breakpoints stay hollow | VS Modules window | **Not code** | Copy the `.pdb` next to the DLL |

---

## 7. Reference queries & hashes

**Identity mapping — run on the GLM server's database:**

```sql
SELECT res_id, '[' + usr_id + ']' AS usr_id, blocked, UserLicenseType,
       LTRIM(RTRIM(UserGroup)) AS UserGroup, ldatindienst, ldatuitdienst,
       Division, cmp_wwn, LTRIM(RTRIM(fullname)) AS fullname
FROM humres
WHERE LTRIM(RTRIM(usr_id)) = '<the Windows account name>';
```

Known-good reference row (local `Client`, `res_id 284983`): `blocked=0`,
`ldatuitdienst=NULL`, `UserLicenseType=100`, `UserGroup='Baco'`, `Division=602`.

**Duplicate provider rows — customer database:**

```sql
SELECT ID, Description, APIUri, LTRIM(RTRIM(Username)) AS Username,
       Last4, KeyID, Active, IsDefault, Created, Product
FROM GLMSysAIPlusProviderConnections WHERE SoftwareID = 999 ORDER BY Created;
```

**Build identity — `GLMSys.AIPlus.Agent.Server.External.dll`:**

| Build | SHA256 (first 16) | Size |
|---|---|---|
| 2026-09-03 current (EGNUtilities tiers + 403) | `B1FFB6D2415F8289` | 52224 |
| 2026-09-03 EGNUtilities tiers | `20D3A3540AF21372` | 52224 |
| 2026-08-27 fix — **never committed or deployed** | `C1B03F424A9DCA4F` | 50176 |
| prior deployed | `D6A5C94F78412EDB` | — |

All AIPlus DLLs are stamped `1.0.0.0`, so **verify deploys by size + SHA256, never by version**.

---

## 8. What this document cannot tell you

Rows 17-20 and 22 fire inside Exact's `Session_OnStart`, before any first-party code runs.
There is no breakpoint that helps. The **Event Viewer ASP.NET 1309 entry** is the only
instrument, and it carries the untruncated stack plus `User:` and `Is authenticated:` for the
failing request. When production behaviour and local behaviour disagree, that entry has
settled it every time.
