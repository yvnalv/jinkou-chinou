# CONTRIBUTING — AI Plus Agent External API

Working agreements for the external-API work item. Read `CLAUDE.md` and
`ARCHITECTURE.md` first.

---

## 0. Always update the CHANGELOG (mandatory)

**Every change must add an entry to [`../CHANGELOG.md`](../CHANGELOG.md)** —
design decisions, doc edits, code, schema, deployment steps, and blockers. Newest
entry on top. Use the template at the top of that file (timestamp, **What**,
**Why**, **How to resolve / how applied**, **Status**, **Currently blocking**,
**Refs**). No PR is complete and no design change is "done" without its CHANGELOG
entry.

## 1. Golden rules

1. **Documentation phase is active — do not write production code** until the design
   here is approved and `PRD.md` §8 open questions are answered.
2. **Do not modify** `GLMSys.AIPlus.Agent.Server.Prompts` or
   `GLMSys.AIPlus.Agent.Server.Service` in this work item.
3. **Do not break** the internal `.aspx` callback flow.
4. **Reuse, don't duplicate** — `AgentChatService.Step` + prompt builders are the
   wheel; the new project only adds transport/auth/state/glue.
5. **Tool execution stays customer-side**; the GLM server never needs the customer
   DB (except server-handled `search_documentation`).
6. **Security guardrails are non-negotiable** — API key required, identity from the
   validated `999` row, parameterized SQL, no key/internal leakage. See
   `CODING_STANDARDS.md` §4.

---

## 2. Repository facts

- Code: `d:\yvnalv\Projects\Addons\AIPlusAgent`.
- Docs (this folder): `D:\yvnalv\Projects\Project Brief\AIPlusAgent\Project Docs`.
- Main solution: `GLMSys.AIPlus.Agent.sln`. Dev solution with external sources:
  `GLMSys.AIPlus.Agent.Other.sln`.
- Remote: Azure DevOps (`glmsystemssource.visualstudio.com/AIPlusAgent`).
- Main branch: `master`.
- Do **not** modify `Setup\` files unless explicitly asked (existing project
  convention) — except adding the new `.ashx`/SQL for this feature, when approved.

---

## 3. Branching & commits

- Branch from `master`: `feature/external-api-<phase>-<short-desc>`.
- Small, focused commits referencing the work item / PR number (match existing
  history style: `Merged PR ####: #<id> - <summary>`).
- Keep `Server.Prompts`/`Server.Service` out of the diff (guardrail #2).

---

## 4. Pull requests

Each PR must state:

- Which **phase** (`ROADMAP.md`) it implements.
- That `Server.Prompts`/`Server.Service` source is untouched.
- Auth test results (valid/invalid/inactive/missing key).
- Internal-flow regression result.
- Any contract change → corresponding update to `API_SPEC.md` / `DATABASE.md`.

### Review checklist

- [ ] Targets .NET Framework 4.7; builds against Synergy `bin`; DLL copies to `BIN\`.
- [ ] Endpoint is `.ashx`; Bearer auth enforced; fails closed.
- [ ] Customer identity derived from validated `999` row; body `customerId` ignored.
- [ ] All SQL parameterized; queries scoped by customer connection id.
- [ ] No AI-provider keys / internal details in responses or logs.
- [ ] `AgentChatService.Step` + prompt builders reused (no copied loop logic).
- [ ] Tool execution remains customer-side; only `search_documentation` server-side.
- [ ] `tool_call_id` binding preserved across `/ai/chat` → `/ai/tool-result`.
- [ ] Internal `.aspx` flow regression-checked.
- [ ] Docs updated if contracts/behavior changed.
- [ ] **`CHANGELOG.md` entry added** (newest on top) — see §0.

---

## 5. Definition of done

A change is done when it meets `CODING_STANDARDS.md` §10, passes the relevant
`TESTING.md` phase exit criteria, and the internal flow regression is green.

---

## 6. Decision log

| Date | Decision | Rationale |
|---|---|---|
| 2026-06-02 | **Conversation state = server-side store** (new tables) | `PRD.md` §8.1; enables `/ai/conversation/{id}` + `/ai/reset` and tool_call_id binding |
| 2026-06-02 | **Keep `SoftwareID=999` as-is**; multi-customer keys deferred to a future WI | `PRD.md` §8.2 |
| 2026-06-02 | **Customer-context = existing approach** (rights→JWT + logged-in user's menu/page access, sent in request) | `PRD.md` §8.3 |
| 2026-06-02 | **JWT kept as-is for now** (`"MySecret"` = pre-prod hardening TODO, unchanged this WI) | `PRD.md` §8.4 |
| 2026-06-02 | **`.ashx` is anonymous, Bearer-only** | `PRD.md` §8.5 |
| 2026-06-02 | **Project name = `GLMSys.AIPlus.Agent.Server.External`** | `PRD.md` §8.6 |

---

## 7. Communication

- Surface blockers from `PRD.md` §8 early; they gate Phases 1–4.
- If reality contradicts these docs (e.g. a `GLMSysCIConnections` column differs),
  update the doc in the same PR and note it in the decision log.
