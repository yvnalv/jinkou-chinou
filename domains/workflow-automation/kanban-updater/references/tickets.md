# Historical Ticket Lookup Hints

These mappings are lookup hints from earlier runs on the live portal. They are not verified and never replace `synergy_fill.py find`: always resolve the card live and let the user confirm it before filling.

## Known Ticket References

| Ticket / Subject | Request Number | Known Request GUID |
|---|---|---|
| `#7111` | `00.046.493` | `bd709722-464a-4bcb-b461-c6988b579d57` |
| `Daily Tasks` | `00.046.420` | `7a63397c-8492-422f-9f28-c1fcc1622ece` |
| `#6364` | `00.035.372` | `9bebfaec-9a4b-49c3-a57c-44e5611b4ce5` |
| `PTT Problem` | `00.033.010` | `054740d5-db8a-42a2-bd17-68a43019c029` |
| `#7094` | `00.046.377` | `380b0580-8122-4410-94ed-3a4e0061d409` |
| `#7093` | `00.046.371` | `feef4025-972f-4b9d-845c-5c153c6a763a` |
| `#7084` | `00.046.343` | `82c20c25-0565-42db-bf96-3311d9c1204b` |

## Exact Synergy URL Templates

`<base_url>` is the active environment's `base_url` from `config.json` (for example `http://localhost/synergy_505` or `https://synergy.glmsystems.com`).

```text
<base_url>/docs/HRMResourceCard.aspx?ID=<PersonID>
<base_url>/docs/GLMSysKanbanBoard.aspx?PersonId=<PersonID>
<base_url>/docs/WflRequest.aspx?BCAction=1&ID=%7b<GUID>%7d
```

### Route Notes

* `<PersonID>`: the employee resource ID. Optional for the board; `synergy_fill.py find` searches without it.
* `<GUID>`: the workflow request ID (`requestId` in `find` results). The request number shown on cards (`00.046.493`) is the HID, not the GUID.
* A request page opened this way is the same page the board shows in its popup dialog, so Save behaves the same.
* Directory listing on `<base_url>/docs/` returns HTTP 403 by design; the `.aspx` pages work normally.
