# QA TEST PLAN — External AI Agent API (setup → chat question)

> **⚠️ Update 2026-08-26 — the ConnectIt AIAgent provider is retired (keep steps for history).**
> The API key is now provisioned via the license-driven `GLMSysAIPlusProviderConnections` flow, so the
> steps below that **provision the `AIAgent` provider / `GLMSysCISoftwares` row / ConnectIt `999`
> connection** and use the provider **"Test connection"** button (§0d prerequisites, §3.1/§3.4, §4/TC-1,
> and the matching troubleshooting rows) are **no longer applicable** — skip them. To verify auth
> instead, hit **`GET /ai/ping`** manually with `X-API-Key` (see §TC-3). Everything else (Use-External-API
> toggle, widget chat) is unchanged. Steps retained for historical reference. See CHANGELOG 2026-08-26.

A step-by-step QA script that walks the **whole external-API path from a clean
environment to a working chat question**: ~~provisioning the ConnectIt **AIAgent**
provider and the `SoftwareID=999` connection, the provider **Test connection**~~ *(retired — see banner)*, the
**Use External API** settings toggle, and finally **asking the chat widget a question**
that is answered through the external API.

This is the **QA / acceptance** companion to the developer smoke test in
[`TESTING.md`](TESTING.md) §0. Deep mechanics live in
[`DEPLOYMENT.md`](DEPLOYMENT.md), [`API_SPEC.md`](API_SPEC.md), and
[`DATABASE.md`](DATABASE.md) — this doc references them rather than repeating them.

> **How to use:** run the sections **in order** (each builds on the previous). Record
> Pass/Fail in the results table at the end. Stop at the first failure and use
> §8 Troubleshooting before continuing.

---

## 1. What you are testing (scope)

| In scope | Out of scope |
|---|---|
| Provider/connection provisioning via the Synergy UI | Internal/direct chat flow (`GLMSysAIPlusAgentClientCallBack.aspx`) |
| Provider **Test connection** (`/ai/ping`) | Azure OpenAI model quality / answer correctness |
| **Use External API** toggle (enable/disable/gate) | Load/performance, multi-customer key management |
| Chat widget question answered **via the external API** | Email/action-link flows |

**End state to prove:** with *Use External API* ON, a question typed in the chat
widget is answered by the GLM-hosted external API, with the customer side executing
any tools.

---

## 2. Environment / topology (dev)

Two Synergy installs on the same machine:

| Role | Install folder | App / DB | Portal |
|---|---|---|---|
| **GLM server** (hosts the API + the LLM call) | `C:\Exact Synergy Enterprise 503` | `Synergy_503` | `http://localhost/Synergy_503/docs/Portal.aspx` |
| **Customer app** (runs the widget, executes tools) | `C:\Exact Synergy Enterprise 503_ClientAIPlusAgent` | `Synergy_503_ClientAIPlusAgent` | `http://localhost/Synergy_503_ClientAIPlusAgent/docs/Portal.aspx` |

**External API endpoint (on the GLM server):**
`http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx`

Dev API key: **`test-key-001`** (development only).

---

## 3. Preconditions / setup (do once, verify each)

> Tick each box. References point at the authoritative section.

### 3.1 Binaries deployed
- [ ] **GLM `…503\BIN`** has `GLMSys.AIPlus.Agent.Server.External.dll` and the reused
      server DLLs (`Server.Service`, `Server.Prompts`, `Shared`, ConnectIt + AzureOpenAI provider).
- [ ] **GLM `…503\BIN`** and **customer `…503_ClientAIPlusAgent\bin`** both have
      **`GLMSys.CI.AIAgent.Provider.dll`** (so the provider loads in the Connections UI — see DEPLOYMENT §0d).
- [ ] **Customer bin** has the AI Plus client DLLs (`Client.Core`, `Client`, `PageExtension`, …).

### 3.2 Web files deployed
- [ ] **GLM `…503\docs`**: `GLMSysAIPlusAgentExternalAPI.ashx`.
- [ ] **Customer `…503_ClientAIPlusAgent\docs`**: `GLMSysAIPlusAgentExternalCallback.ashx`,
      `GLMSysAIPlusAgentClientCallBack.aspx`, `GLMSysAIPlusAgentSettings.aspx`,
      `GLMSysAIPlusAgentChatEngine.js` (+ widget CSS/assets).

### 3.3 ConnectIt + LLM
- [ ] **ConnectIt installed & registered** on **both** installs (required for CRUD — DEPLOYMENT §0c).
- [ ] **GLM** `GLMSysCIConnections` has an **active `AzureOpenAI`** row (LLM creds) — the LLM call runs on the GLM server only.

### 3.4 AIAgent provider definition (`GLMSysCISoftwares`)
- [ ] On **both** installs a software row exists with **`ProviderName = "AIAgent"`**
      (API-key connection type; `APIUri` + `APIKey` fields visible). Created via the
      Synergy **Provider** menu. (Mechanism: DEPLOYMENT §0d.)

### 3.5 `GLMSysCIConnections` `SoftwareID=999` rows
- [ ] **GLM (`Synergy_503`)** — **key registry** row: `APIKey = test-key-001`, `Active = 1`.
      Owner convention: **no `APIUri`** on the GLM side (it only holds the key the validator reads).
- [ ] **Customer (`Synergy_503_ClientAIPlusAgent`)** — **caller** row: `APIUri =`
      `http://localhost/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx`,
      `APIKey = test-key-001` (**must match** the GLM key), `Active = 1`.

> **Note on the key:** when saved via the UI the `APIKey` is **encrypted at rest**; the
> system compares/sends the **decrypted** value, so the GLM and customer keys must be the
> **same plaintext** (`test-key-001`). See DATABASE §1.3.

### 3.6 Recycle
- [ ] `iisreset` (or recycle both app pools) so new DLLs/`.ashx` load. The **first**
      request after a recycle is slow (cold start) — allow time.

**Section pass criteria:** every box ticked.

---

## 4. TEST — Provider "Test connection"

### TC-1 · Client-side connection test (the real one)
1. Log in to the **customer** portal → **Connections** → open the **AIAgent** (999) connection.
2. Confirm `APIUri` = the GLM `…GLMSysAIPlusAgentExternalAPI.ashx` and `APIKey` = `test-key-001`.
3. Click **Test connection**.

**Expected:** ✅ success ("connection successful"). Internally the provider does
`GET {APIUri}/ai/ping` with the key; the GLM API returns `200`. (API_SPEC §5a.)

| Result | Meaning |
|---|---|
| ✅ Success | Endpoint reachable + key accepted. Proceed. |
| ❌ `Authentication failed (401)` | Key mismatch — the decrypted customer key ≠ GLM's decrypted `999` key. See §8. |
| ❌ `returned HTTP 500` | GLM env-init failed (see §8); usually a recycle/identity issue. |
| ❌ `Could not reach …` | Wrong `APIUri`, endpoint down, or GLM app not recycled. |
| ❌ `Could not load … 'GLMSys.CI.AIAgent.Provider'` | Provider DLL missing from the customer bin (§3.1 / DEPLOYMENT §0d). |

### TC-2 · Server-side connection (key registry) — informational
- The GLM-side `999` row is **API-key-only (no `APIUri`)**, so **Test connection there is
  not applicable** — clicking it shows *"API URI is not configured"*. That is **expected**;
  the GLM row only supplies the key the validator reads.

### TC-3 · (Optional) Direct `/ai/ping` probe
On a logged-in **GLM** browser tab, **F12 → Console**:
```js
fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/ping',
  { headers:{ 'X-API-Key':'test-key-001' } })
  .then(async r => console.log('PING', r.status, await r.text()));   // expect 200 {"status":"ok"}

fetch('/Synergy_503/docs/GLMSysAIPlusAgentExternalAPI.ashx/ai/ping',
  { headers:{ 'X-API-Key':'wrong' } })
  .then(r => console.log('PING-BAD', r.status));                     // expect 401
```

---

## 5. TEST — "Use External API" settings toggle

Open the **customer** portal → **AI Plus → Agent Settings**
(`GLMSysAIPlusAgentSettings.aspx`) → **API Routing** card.

### TC-4 · Toggle is gated on the `999` connection
- [ ] **With** a `SoftwareID=999` row present (it is, from §3.5): the **Use External API**
      toggle is **enabled** (clickable).
- [ ] (Negative, optional) Temporarily set the customer `999` row `Active`/remove it and
      reload: the toggle is **disabled/greyed**, shows OFF, with the *"not configured
      (SoftwareID=999)"* note. **Restore the row afterwards.**

### TC-5 · Enable + persist
1. Switch **Use External API** → **ON**.
2. Click **Save Settings** → expect "Settings saved successfully".
3. Reload the page → the toggle is still **ON** (value persisted in `BacoSettings`).

**Expected:** `GLMSysAIPlusAgentUseExternalApi` = `1`. (If no `999` row existed, Save would
coerce it back to `0` — that's the gate, DEPLOYMENT §2b.)

---

## 6. TEST — Ask the chat question (the goal)

### TC-6 · Chat answered via the external API
1. In the **customer** portal (any page with the widget, e.g. the Portal), open the
   **AI Plus chat** widget (floating button).
2. Click **New chat** (ensures the route is resolved fresh).
3. Type a simple question and send, e.g.:
   > `Hello, who are you? One short sentence.`
4. Wait for the reply (first call after a recycle is slow).

**Expected:** ✅ a coherent assistant reply appears in the widget.

### TC-7 · Confirm it really used the external API (not internal)
Pick **one**:
- **Network tab (F12 → Network):** the chat request goes to
  **`GLMSysAIPlusAgentExternalCallback.ashx`** (external), **not**
  `GLMSysAIPlusAgentClientCallBack.aspx` (internal).
- **DB:** a new row appears in **`GLMSysAIPlusAgentConversation`** on the GLM DB
  (`Synergy_503`), and **`GLMSysCILLMUsage`** gets usage rows for the turn.

### TC-8 · (Optional) Multi-turn + a tool question
1. Follow up **without** reopening: `What did I just ask you?` → it should remember (server-side conversation).
2. Ask something that needs data, e.g. `How many open requests do I have?` →
   the GLM API returns tool calls, the **customer side executes them**, and a
   data-grounded answer comes back. (Tool loop: API_SPEC §3, §7.)

### TC-9 · No-refresh routing (regression)
- With the widget already open from a session where the toggle was OFF, flipping the
  toggle **ON** and starting a **New chat** should route to the external API **without a
  full page reload** (route is resolved per conversation). (DEPLOYMENT §2b.)

---

## 7. Results summary (fill in)

| # | Test | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 3 | Preconditions | all boxes ticked | | |
| TC-1 | Client Test connection | success (200 `/ai/ping`) | | |
| TC-3 | `/ai/ping` probe (opt) | 200 ok / 401 bad | | |
| TC-4 | Toggle gate | enabled w/ 999, disabled w/o | | |
| TC-5 | Toggle save/persist | `…UseExternalApi=1`, persists | | |
| TC-6 | Chat question | assistant reply | | |
| TC-7 | Routed externally | external callback / DB rows | | |
| TC-8 | Multi-turn + tool (opt) | remembers + data answer | | |
| TC-9 | No-refresh routing (opt) | applies on next New chat | | |

---

## 8. Troubleshooting (symptom → cause → action)

| Symptom | Likely cause | Action |
|---|---|---|
| Test connection: **401 "API key was rejected"** | Customer key ≠ GLM key (different plaintext), or GLM `999` row inactive | Make both `999` `APIKey` the **same plaintext** (`test-key-001`), `Active=1`; recycle GLM. (DATABASE §1.3) |
| Test connection: **HTTP 500** for `/ai/ping` | GLM couldn't build an environment (no session, env-init) | Recycle GLM; ensure the API-key-only GLM row needs no ping. For server-side row it's N/A (TC-2). |
| **"Could not load … 'GLMSys.CI.AIAgent.Provider'"** | Provider DLL not in that app's `bin` | Deploy `GLMSys.CI.AIAgent.Provider.dll` to the bin; recycle. (DEPLOYMENT §0d) |
| Toggle is **greyed/disabled** | No `SoftwareID=999` row on the customer DB | Create the customer `999` connection (§3.5). |
| Chat returns an **error / no reply** | LLM creds, or env on GLM, or key | Check GLM `AzureOpenAI` row; run TC-3 ping; check `GLMSysCILLMUsage`. |
| Chat works but **uses the internal callback** | Toggle OFF, or widget not re-routed | Set toggle ON + **New chat** (TC-9); confirm in Network tab. |
| Create/update **fails** in a tool answer | ConnectIt not installed on the customer | Install/register ConnectIt on the customer Synergy. (DEPLOYMENT §0c) |

---

## 9. Sign-off

| Field | Value |
|---|---|
| Build / commit (AIPlusAgent) | |
| Build / commit (ConnectIt) | |
| Environment | dev (`Synergy_503` + `Synergy_503_ClientAIPlusAgent`) |
| Tester | |
| Date | |
| Result | Pass / Fail |
