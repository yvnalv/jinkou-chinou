# Historical Ticket Lookup Hints

These mappings serve as reference lookup hints from previous configurations. They have not been verified live. Always resolve and confirm the actual card on the current user's board before writing. Historical mappings are never a current-state guarantee.

## Known Ticket References

| Ticket / Subject | Request Number | Known Request GUID |
|---|---|---|
| `#7111` | `00.046.493` | `bd709722-464a-4bcb-b461-c6988b579d57` |
| `Daily Tasks` | `00.046.420` | `7a63397c-8492-422f-9f28-c1fcc1622ece` |
| `PTT Problem` | `00.033.010` | `054740d5-db8a-42a2-bd17-68a43019c029` |
| `#7094` | `00.046.377` | `380b0580-8122-4410-94ed-3a4e0061d409` |
| `#7093` | `00.046.371` | `feef4025-972f-4b9d-845c-5c153c6a763a` |
| `#7084` | `00.046.343` | `82c20c25-0565-42db-bf96-3311d9c1204b` |

## Exact Synergy URL Templates

```text
https://synergy.glmsystems.com/docs/HRMResourceCard.aspx?ID=<PersonID>
https://synergy.glmsystems.com/docs/GLMSysKanbanBoard.aspx?personid=<PersonID>
https://synergy.glmsystems.com/docs/WflRequest.aspx?RequestID=<GUID>
```

### Route Notes

* `<PersonID>`: Identifier of the employee resource. Must be resolved before opening the Kanban board.
* `<GUID>`: The specific workflow request ID (`RequestID`), extracted from the ticket link on the Kanban board.
* Directory listing on `https://synergy.glmsystems.com/docs/` often returns HTTP 403 Forbidden by design; specific `.aspx` endpoints function normally.
