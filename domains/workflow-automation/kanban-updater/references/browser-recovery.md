# Browser Recovery and Playwright Diagnostics

This reference specifies how `kanban-updater` handles browser sessions, transient errors, and persistent state verification.

---

## 1. Non-Destructive Operation Rules

1. **Zero Forced Process Termination**:
   * **Never** use `taskkill`, `Stop-Process`, or PID-targeted kills on Microsoft Edge.
   * Terminating a browser can destroy open tabs, active user sessions, and unsaved work.
2. **Profile Lock Detection**:
   * If `%USERPROFILE%\.gemini\playwright-edge-profile` is locked (`ProcessSingleton` lock file), fail gracefully.
   * Log the condition and notify the user to either close the automated browser tab or attach via CDP.
3. **CDP Window Preservation**:
   * When attaching via `connect_over_cdp()`, **never** call `browser.close()`.
   * Only close specific tabs (`page.close()`) instantiated by this automation.

---

## 2. Structured Error Logging

Every failure during browser automation must be recorded in this concise, standardized format:

```text
[<DD/MM/YYYY HH:mm:ss TZ> | attempt <N> | <stage>]
Error: <ErrorClass / Message / HTTP Status>
Write attempted: <yes | no>
Next: <Planned recovery action>
```

### Example
```text
[01/10/2026 13:40:15 GMT+07 | attempt 2 | navigate board]
Error: net::ERR_CONNECTION_TIMED_OUT
Write attempted: no
Next: Check Synergy portal reachability and verify VPN connection status.
```

---

## 3. Failure Mode Diagnostic Table

| Symptom / Error | Root Cause | Evidence-Based Recovery Action |
|---|---|---|
| `EBUSY / ProcessSingleton` | Automation profile is currently opened by another process | Check running processes. Do not kill. Ask user to close the profile window or use CDP. |
| `ERR_INVALID_AUTH_CREDENTIALS` or login redirect | Expired session in automation profile | Notify user that interactive login is required in the automation profile. |
| `HTTP 403 Forbidden` on `/docs/` | Directory browsing is disabled on IIS | Do not fail; test the concrete `.aspx` route (`GLMSysKanbanBoard.aspx` / `WflRequest.aspx`). |
| `Timeout 30000ms` on board render | Network latency or slow Synergy SQL backend | Retry navigation once with explicit 45s timeout. Inspect frames for error banners. |
| Target card not found in DOM | Card in different column, filtered, or paginated | Inspect board filters, click "Show All", or verify ticket number against search box. |
| Selector not found (`#txtRemarks`) | Frame hierarchy or dynamic control ID shift | Inspect frame tree (`page.frames`); locate control by `name` or input role rather than ID alone. |

---

## 4. Safe Read vs. Write Retries

* **Before a Write**: Read retries are safe. If card inspection times out, re-opening the page or reloading is idempotent.
* **After a Possible Write**:
  * If a timeout occurs during `#btnSave` or `#btnApprove` submission, **NEVER immediately retry the write action**.
  * Immediately perform a **read-only reload** of `WflRequest.aspx?RequestID=<GUID>`.
  * Inspect existing remarks to verify if the new update was already persisted.
  * Only execute a second write if fresh evidence proves the first write failed and the card state remains unchanged.
