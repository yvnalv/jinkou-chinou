# Synergy Automation (Work Log + Fill)

How `scripts/synergy_fill.py` finds cards, reads remark history, and types the work log into Exact Synergy, plus what to do when it fails. Verified against Exact Synergy Enterprise 505 with the GLMSys Kanban add-on.

---

## 1. Commands

All commands print one JSON object and read every setting from `config.json` (`references/configuration.md`).

| Command | Browser | Writes? | Use |
|---|---|---|---|
| `python <skill-dir>/scripts/synergy_fill.py check` | headless (or the open automation window) | no | Pre-flight: settings, Edge profile, login, Kanban board reachable. |
| `python <skill-dir>/scripts/synergy_fill.py find 7111 00.046.493` | same | no | Resolve numbers to cards. |
| `python <skill-dir>/scripts/synergy_fill.py history <GUID-or-number> [--days 30] [--today YYYY-MM-DD]` | same | no | Read Workflow remark history, grouped by day. |
| `python <skill-dir>/scripts/synergy_fill.py candidates [--date YYYY-MM-DD]` | same | no | Today's work items for the scheduled run (`references/schedule-and-points.md` §2). |
| `python <skill-dir>/scripts/synergy_fill.py entries --since DATE --until DATE` | same | no | Your own remarks on your cards; input for `points.py`. |
| `python <skill-dir>/scripts/synergy_fill.py fill --plan <plan.json>` | **visible** Edge window | types into the field, **never saves** | Fill one tab per card and hand the window to the user. |

Add `--env live` (before the command) to run one command against another environment without editing the file.

### Plan file for `fill`

Write it to the scratchpad, never into a repository:

```json
[
  {"query": "#7111", "request_id": "bd709722-464a-4bcb-b461-c6988b579d57", "message": "<approved work log text>"},
  {"query": "00.046.377", "request_id": "380b0580-8122-4410-94ed-3a4e0061d409", "message": "<approved work log text>"}
]
```

`request_id` must come from a `find` result the user confirmed. `message` is exactly the text the user approved.

---

## 2. Finding a card (`find`)

* The script opens `GLMSysKanbanBoard.aspx` and calls the board's own paging callback from inside the page, so it uses the browser's login: `GLMSysKanbanBoardCallback.aspx`, `action=5`, `requestType` (each Kanban request type), `sourceName=Status`, `selectedPage=1,2,…` until a page comes back empty, header `X-Requested-With: XMLHttpRequest`. Each page holds up to 5 cards per status column, so paging returns every match. The server matches `searchText` against the request number (HID) **or** the description, using SQL `LIKE '%n%'`.
* `filterPerson` limits results to card **owners** (`EmpId`). Empty filters fall back to the user's saved board view, so a card hidden by a saved board filter can be missed; clear the filter on the board if a known card is not found.
* `whoami`: the login name comes from `kanbanApp.loginPersonName`; the PersonID from `config.json`, or from the board's person list (`kanbanApp.requestPerson`, loaded after the first callback).
* The script then keeps only real matches:
  * `request_number`: the card's HID equals the number. `00.046.493` is treated as a request number only.
  * `work_item_in_description`: the number appears as a whole token in the description (`#7111`, `PBI 7111`, `(7111)`). It does not match inside `17111` or a version like `v7111.2`.
* `decision`:
  * `unique`: exactly one card. Use it.
  * `ambiguous`: more than one card. **Always ask the user which card** (show request number, description, status, owner). Never pick one yourself.
  * `not_found`: say so and ask for the request number.
* The search is not limited to your PersonID: cards you work on may be owned by someone else. The result shows `owner` and `assigned`.

## 3. Reading history (`history`)

* Opens `WflRequest.aspx?BCAction=1&ID={GUID}` and reads the `WorkflowComments` textarea. When the request type shows earlier remarks in a frozen field instead, it also reads `WorkflowCommentsFreeze` and the "Remarks: Workflow" row text, and uses the longest.
* Entries are split on Synergy timestamps: `[Full Name dd-mm-yyyy hh:mm (GMT +07:00)]`. The date order comes from `date_format` in the settings file.
* Output per card: `by_date` (entries inside the `--days` window, newest day first), `today_logged`, `last_entry_date`, `recent_texts` (last 5 entries), `field_editable`, and `auto_timestamp` (`on`/`off`, the user's `SYSWorkflow_AutoTimeStamp` setting).
* Use it to: skip or confirm a card already logged today, keep the new remark from repeating earlier ones (the repetition penalty in `references/eod-scoring.md`), and continue the story where the last entry stopped.

## 4. Filling (`fill`)

For each card, in its own tab:

1. Open the request page and confirm `textarea#WorkflowComments` exists and is editable. Otherwise the card is `skipped` with the reason.
2. Click the field and press `Ctrl+End`, so the new entry goes after all existing history.
3. Press **Enter**. With auto-timestamp on, Synergy's keydown handler inserts the stamp at the caret (with a leading newline when the field already has text), and the Enter puts the message on its own line.
4. No stamp appeared (auto-timestamp off): undo the plain newline, click the field's **Timestamp** button (`button[onclick*="SysSetTimestamp('WorkflowComments')"]`, a `type="button"`, so no postback), then press Enter.
5. Insert the message text and verify that the field now equals the old content + stamp + message.

Why typing instead of `fill()`: Playwright's `fill()` sends no key events, so Synergy would never add its timestamp.

After the last card the script **disconnects and leaves the Edge window open**. It is now an ordinary browser window: the user reviews each tab and presses **Save** (or closes the tab to discard). Native dialogs work normally because nothing is attached any more.

Result statuses: `filled`, `skipped` (field missing or read-only, or the card is already open in the automation window), `error` (reason given). The top-level `saved` is always `false`.

### What fill never does

* Never clicks Save, Approve/In-Progress, Reject, Realize, Process, Delete, Close, or any button other than the field's Timestamp button.
* Never replaces existing text: it only appends at the end.
* Never re-fills a card whose tab is still open from an earlier run (it would stack two stamps). The user saves or closes that tab first.

---

## 5. Browser sessions

* **Profile**: one dedicated Edge profile (`browser.profile` in `config.json`), shared with other AI tools through directory junctions.
* **Automation window**: `fill` starts Edge with that profile and `--remote-debugging-port=<cdp_port>` (default 9333), detached from the script. Later commands (`find`, `history`, `check`) attach to that window if it is open, open their own tab, and close it again. This avoids profile-lock errors while the user is still reviewing.
* **Headless**: when no automation window is open, read-only commands launch headless Edge with the profile.
* **Login**: every launch passes `--auth-server-allowlist=<host>`, so Edge answers Windows (NTLM/Negotiate) challenges with the signed-in Windows account. If `username`/`password` are set, headless runs pass them as `http_credentials`, and the visible window answers auth challenges with them over CDP. The visible-window credential path has not been verified against the live portal yet; if a native login prompt appears, the user types the credentials once.
* **Port exposure**: while the automation window is open, any local process can control it through the port. Tell the user to close the window when they are done.

---

## 6. Failure handling

### Non-destructive rules

* Never kill Edge (`taskkill`, `Stop-Process`). Ask the user to close the conflicting window.
* Never close a tab you did not open. Read-only commands close only their own tab.
* Never retry `fill` blindly. Run `history` for the card first: if the remark is already saved, or the tab is still open, do not fill again.

### Error log format

Report every failure in this format, then the recovery step:

```text
[<DD/MM/YYYY HH:mm:ss TZ> | attempt <N> | <stage>]
Error: <error / HTTP status>
Write attempted: <no | typed, not saved>
Next: <planned recovery action>
```

### Diagnostic table

| Symptom | Cause | Recovery |
|---|---|---|
| `Settings file not found` | No `config.json` yet | `python <skill-dir>/scripts/kanban_config.py --init`, then fill it in. |
| `is not valid JSON ... Backslashes must be doubled` | Single `\` in a path or in `DOMAIN\name` | Write `\\` in the file (`DOMAIN\\name`). |
| `PersonID unknown` | `person_id` empty for the environment | Run `check`; it prints the detected value to put in `config.json`. |
| `auth_required` / HTTP 401 | Not signed in for that host | Fill `username`/`password` for the environment in `config.json`, or sign in once in the automation window. |
| `automation profile is open in another Edge window` | Profile opened without the automation port | Ask the user to close that window. Do not kill it. |
| `automation port did not open` | Same as above, seen while launching `fill` | Same. |
| `non-JSON response` from `find` | Session expired or the Kanban role is missing | Run `check`; open the board manually to see the message. |
| `decision: not_found` | Number not on the board, or hidden by a saved board filter | Ask for the request number (`00.046.493`); clear board filters. |
| `skipped: read-only` | The workflow step does not allow editing Workflow remarks for this user | Report it; the user adds the remark by hand. |
| `Timestamp button did not insert a timestamp` | Unusual request type layout | Report it; nothing was typed. |
| `Timeout` on page load | Slow portal or VPN | Retry once (read-only commands are safe to retry); check VPN. |
| WinError 740 when launching Edge | `RUNASADMIN` compatibility flag on msedge.exe | Run `python <skill-dir>/scripts/setup_environment.py --check` (sets `RUNASINVOKER` for the user). |
