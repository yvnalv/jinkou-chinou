# Configuration and PersonID Setup

This guide explains how `kanban-updater` identifies the employee (`PersonID`), accesses Exact Synergy, and isolates its Playwright browser session.

---

## 1. What is PersonID?

In Exact Synergy Enterprise, every employee has a unique resource record identified by an integer or numeric ID known as the **PersonID**. The personal Kanban board is routed via this ID:

```text
https://synergy.glmsystems.com/docs/GLMSysKanbanBoard.aspx?personid=<PersonID>
```

Without a valid `PersonID`, the automation cannot open the employee's personal board.

---

## 2. How to Find Your PersonID

Follow these steps to find your personal ID in Exact Synergy:

1. Open your browser and navigate to the Synergy portal: `https://synergy.glmsystems.com/`.
2. Ensure you are logged in with your enterprise credentials.
3. Look at the **top-right header** where your full name is displayed.
4. **Important**: Right-click your name link and choose **Open in new tab** (or inspect its URL).
   * *Why in a new tab?* Clicking the link normally inside the portal opens the profile inside a nested iframe, keeping the address bar on the generic portal URL.
5. In the newly opened tab, inspect the URL in the browser address bar:
   ```text
   https://synergy.glmsystems.com/docs/HRMResourceCard.aspx?ID=12345
   ```
6. The numeric value following `?ID=` (e.g. `12345`) is your **PersonID**.

---

## 3. PersonID Resolution Hierarchy

The skill checks for `PersonID` in this exact order:

```text
1. CLI Argument / Prompt:    /kanban-updater for person 12345
2. Environment Variable:     SYNERGY_PERSON_ID
3. Local User Config File:   ~/.config/kanban-updater/config.json
4. Live Auto-Discovery:      Opens logged-in name link in new tab via Playwright
```

### Option A: Local Config File (Recommended for Persistence)
Run the bundled setup script to store your PersonID locally:
```powershell
python scripts/setup_environment.py --set-person-id 12345
```
This saves to `~/.config/kanban-updater/config.json` (on Windows: `%USERPROFILE%\.config\kanban-updater\config.json`):
```json
{
  "person_id": "12345",
  "updated_at": "2026-10-01T13:30:00Z"
}
```
*Note: This file is located in your user profile, keeping credentials and personal IDs completely isolated from Git version control.*

### Option B: User Environment Variable
Set the variable in PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('SYNERGY_PERSON_ID', '12345', 'User')
```
Or in CMD:
```cmd
setx SYNERGY_PERSON_ID 12345
```

### Option C: Live Auto-Discovery
If no config or variable is set, the skill connects to your active Synergy session, locates your user link at the top-right header, opens it in a new tab, extracts the `ID` parameter from `HRMResourceCard.aspx?ID=...`, and uses it for the current run.

---

## 4. Browser Profiles and Session Isolation

### Dedicated Automation Profile
To avoid session conflicts with your daily Microsoft Edge browsing, the skill defaults to an isolated user data directory:
```text
%USERPROFILE%\.gemini\playwright-edge-profile
```
* **First-time Login**: If headless mode fails due to missing SSO/cookies in this profile, launch the setup script or Edge once interactively with this profile to complete login.
* **Non-Destructive Guarantee**: The automation **never** kills existing Edge processes (`taskkill`, `Stop-Process`). If the profile is locked, it reports an error and falls back to safe read/draft mode.

### Attaching via Chrome DevTools Protocol (CDP)
If you already have a running Edge session with Synergy open, you can start Edge with a remote debugging port:
```powershell
msedge.exe --remote-debugging-port=9222
```
And pass CDP connection in the prompt or environment:
```powershell
$env:SYNERGY_CDP_ENDPOINT = "http://localhost:9222"
```
Playwright will connect via `connect_over_cdp()`, reusing your live authenticated session without creating lock conflicts.
