# Product Discovery

Detailed guidance for Product Discovery in Modes A and B. `SKILL.md` has the rules; this file has the discovery areas, the full PRD Discovery Coverage Gate checklist, gap handling, and the Discovery Summary format.

Contents:

1. Starting Discovery
2. The Ten Discovery Areas
3. Mapping Discovery to the PRD
4. PRD Discovery Coverage Gate
5. Gap Resolution and Question Selection
6. Discovery Completion
7. Discovery Summary

---

## 1. Starting Discovery

### Application Identity

When starting a new application, establish:

- application name (a working name is fine if no final name exists),
- short description / idea,
- problem being solved,
- primary target users.

For an existing project, infer the application identity from the repository where possible. Do not ask questions that repository inspection can answer.

### First Round — New Project

If invoked with only a rough idea, begin approximately with:

1. What is the application name?
2. In one or two sentences, what should this application do?
3. Who are the main users?
4. What is the primary end-to-end business flow?
5. Are there any fixed technical constraints or required technologies?

Adapt the questions to information already available.

### Every Round

1. Normalize the newly discovered requirements.
2. Run the Coverage Gate (section 4) mentally.
3. Identify the highest-impact missing areas.
4. Ask only the next relevant questions — about 3–6 related questions per round.
5. Continue until no Critical Gap remains.

### Existing Project

Run the Coverage Gate against repository-discovered information, existing documentation, the current conversation, and the user's requested change. Ask only unresolved product or business questions that materially affect implementation.

---

## 2. The Ten Discovery Areas

Ask only questions that materially affect product requirements, business flow, domain model, architecture, integration, security, data, or implementation scope. Use answers already available from the conversation, existing documentation, repository inspection, or known constraints, and never ask for known information again.

Discovery questions are adaptive, not a rigid questionnaire. The goal is enough information for the PRD, not a fixed number of questions.

### 2.1 Product Goal

Understand:

- What problem is being solved?
- Why should the application or feature exist?
- What value does it provide?
- What does successful behavior look like?

Identify where useful: primary goals, secondary goals, non-goals.

### 2.2 Users and Actors

Identify meaningful actors, for example Customer, Admin, Staff, Manager, Moderator, Vendor, Developer, External System. Do not invent roles without evidence.

For each relevant actor determine what they can do, what they cannot do, what they own, and what permissions they require.

Normalize actor capabilities discovered in conversation into Functional Requirements. Do not force the user to restate them in formal requirement language.

User statement:

```text
Admin can upload invoices, assign them to departments,
approve or reject them, and reopen completed invoices.
```

May produce:

```text
FR-001 Admin can upload an invoice.
FR-002 Admin can assign an invoice to a department.
FR-003 Admin can approve an invoice.
FR-004 Admin can reject an invoice.
FR-005 Admin can reopen an eligible invoice.
```

### 2.3 End-to-End Business Flow

Understand the main workflow, for example:

```text
User Action
→ System Processing
→ Validation
→ Other Actor / External System
→ State Change
→ Completion
```

Discover where relevant: entry point, normal flow, alternate flow, approval, rejection, cancellation, retry, re-open, timeout, expiration, failure, and completion.

The main user journey must be understandable from beginning to end.

### 2.4 Business Rules

Extract important rules explicitly, for example: ownership, approval, concurrency, limits, pricing, eligibility, duplicate prevention, locking, expiration, scheduling, state transitions, refunds, cancellation.

Do not leave important rules buried in casual discussion. Convert meaningful decisions into explicit requirements.

### 2.5 Data and Domain

Identify important domain concepts and, where relevant, their purpose, ownership, major fields, relationships, lifecycle, state / status, and deletion behavior.

Discovery should understand the domain. It does not need to design every database column prematurely.

### 2.6 Integrations

Identify required external systems, for example: payment gateway, email, WhatsApp, SMS, calendar, maps, AI provider, ERP, accounting, file storage, third-party API, webhook.

For each relevant integration determine:

- why it exists,
- whether it is mandatory,
- incoming / outgoing data,
- authentication expectations,
- failure behavior.

### 2.7 Authentication and Authorization

Determine where relevant: whether login is required, registration behavior, anonymous access, user roles, permissions, session requirements, service-to-service authentication, external identity providers.

Do not automatically select JWT, OAuth, cookies, API keys, or another mechanism unless required. Architecture decides the mechanism.

### 2.8 Application Surface

Identify required surfaces, for example: web application, backend API, mobile application, admin portal, public website, internal dashboard, desktop application, background worker, CLI.

Also identify whether the system is internal, public, B2B, B2C, or mixed.

### 2.9 Technical Constraints

Classify each technical decision:

- **Hard constraint** — must be followed. Examples: required framework version, hosting limitation, legacy runtime, required database, company standard.
- **Preference** — preferred but negotiable.
- **Open decision** — may be decided during architecture planning.

Never silently convert a preference into a hard constraint.

### 2.10 Definition of Success

Ask or infer:

- What result must the user be able to achieve?
- What behavior proves the feature works correctly?
- What outcome would make the user consider the feature complete?
- What failure conditions must explicitly not occur?

Translate the findings into testable Acceptance Criteria.

Avoid criteria such as:

```text
The feature should work properly.
```

Prefer observable criteria such as:

```text
Given a valid receipt,
when the user submits the receipt,
the system extracts the supported line items and presents them
for confirmation without creating a finalized split automatically.
```

---

## 3. Mapping Discovery to the PRD

| Discovery Area | PRD Destination |
|---|---|
| Application name and purpose | Product Overview |
| Problem being solved | Problem Statement |
| Main users and roles | Users / Actors |
| End-to-end flow | User Journeys |
| Actor capabilities | Functional Requirements |
| Domain and workflow rules | Business Rules |
| Failure, retry, cancel, reopen, conflict | Edge Cases |
| External systems | Integration Requirements |
| Hard constraints and limitations | Constraints |
| Observable successful behavior | Acceptance Criteria |

This mapping is conceptual. Do not force an answer into one section when it naturally affects several.

---

## 4. PRD Discovery Coverage Gate

A mandatory self-check before declaring Product Discovery complete. Discovery is complete when the important requirement areas are sufficiently understood, not because several questions have been answered.

Only applicable items need to be covered. Mark irrelevant areas N/A internally rather than inventing content.

### 1. Product Overview

- [ ] Application or feature name is known, or a working name exists. (For an existing feature, the application name may come from repository discovery.)
- [ ] Application / feature purpose is understood.
- [ ] High-level product description can be stated clearly.

### 2. Problem Statement

- [ ] The problem being solved is understood.
- [ ] The reason the application / feature is needed is understood.
- [ ] The difference between current state and desired state is clear. For existing applications, distinguish **Current Behavior** from **Expected Behavior**.

### 3. Users / Actors

- [ ] Main users / actors are identified.
- [ ] Relevant roles are understood.
- [ ] Important ownership boundaries are understood.
- [ ] Important permissions are understood where applicable.

Do not invent actors to fill this section.

### 4. User Journeys

- [ ] Main end-to-end flow is understood.
- [ ] Entry point is known.
- [ ] Primary successful completion path is known.
- [ ] Important alternate paths are known where relevant.

A minor UI interaction needs its own journey only if it materially affects behavior.

### 5. Functional Requirements

- [ ] The meaningful capabilities required from the system are understood.
- [ ] Important actor actions can be translated into Functional Requirements.
- [ ] Required system-generated behavior is captured.
- [ ] Existing functionality that must remain unchanged is identified where relevant.

Do not require the user to write `FR-xxx` requirements. Infer them from natural conversation where possible.

### 6. Business Rules

Verify the applicable rules:

- [ ] ownership
- [ ] permissions
- [ ] approval
- [ ] limits
- [ ] state transitions
- [ ] eligibility
- [ ] duplicate prevention
- [ ] locking
- [ ] concurrency
- [ ] pricing
- [ ] expiration
- [ ] scheduling
- [ ] cancellation
- [ ] other domain-specific rules

### 7. Edge Cases

Verify important behavior for the applicable cases:

- [ ] invalid input
- [ ] failure
- [ ] cancellation
- [ ] retry
- [ ] re-open
- [ ] expiration
- [ ] timeout
- [ ] duplicate action
- [ ] conflicting updates
- [ ] concurrency
- [ ] unavailable dependency
- [ ] permission failure

Not every product needs every edge case. Prioritize those that can materially change business behavior, architecture, data integrity, security, or user outcomes.

### 8. Integration Requirements

- [ ] Required external systems are known.
- [ ] The purpose of each important integration is understood.
- [ ] Relevant incoming / outgoing data is understood.
- [ ] Critical failure behavior is understood.
- [ ] Mandatory and optional integrations are distinguished.

If no external integration exists, mark this area N/A.

### 9. Constraints

- [ ] Hard technical constraints are known.
- [ ] Product constraints are known where relevant.
- [ ] Legacy compatibility requirements are known.
- [ ] Required technology choices are distinguished from preferences.
- [ ] Open architecture decisions remain explicitly open.

Do not silently convert an unknown into an assumption when the answer could materially affect implementation.

### 10. Acceptance Criteria

- [ ] Successful behavior is observable.
- [ ] Important outcomes are testable.
- [ ] Critical failure expectations are defined where appropriate.
- [ ] Acceptance criteria can later guide automated or manual verification.

Acceptance criteria describe behavior, not implementation details, unless the implementation itself is a required constraint.

---

## 5. Gap Resolution and Question Selection

After running the Coverage Gate, classify the missing information.

### Critical Gap

Missing information that can materially affect business flow, architecture, data model, integration, security, permissions, or implementation scope.

Examples: unclear ownership, unclear payment behavior, unclear approval rules, unclear state transitions, an unknown mandatory integration, an ambiguous authentication requirement.

**Continue Discovery** with focused questions.

### Non-Critical Gap

Missing information that can safely be deferred.

Examples: exact button wording, decorative UI styling, minor visual preferences, low-impact copywriting, implementation details architecture can decide later.

Do not block PRD generation. Record it as an assumption, open question, preference, or future decision.

### Question Selection

Do not dump all unresolved questions at once. Ask the highest-impact ones first, about 3–6 related questions per round, in this priority:

```text
1. Main Business Flow
2. Actors / Ownership / Permissions
3. Critical Business Rules
4. Data Integrity / State Transitions
5. External Integrations
6. Authentication / Security
7. Technical Hard Constraints
8. Acceptance / Success Behavior
9. Lower-impact UX Details
```

---

## 6. Discovery Completion

Discovery must NOT be considered complete because:

- a fixed number of questions were asked,
- the user answered one long message,
- the application sounds simple,
- or the AI believes it can infer the rest.

Discovery may be considered complete when:

```text
Applicable PRD Coverage
        ↓
Critical Gaps Resolved
        ↓
Remaining Unknowns Are Non-Critical
        ↓
Requirements Sufficient
```

The key criterion:

> No known unresolved ambiguity should remain that is reasonably likely to cause major product, architecture, security, data, integration, or implementation rework.

### Required Understanding

For a new application:

- application name
- product purpose
- problem statement
- main actors and their capabilities
- main business flow
- important business rules
- relevant edge cases
- main domain concepts
- integrations
- authentication expectations
- technical hard constraints
- major non-functional expectations
- testable success criteria
- important unresolved risks

For an existing project, also:

- relevant repository inspected,
- existing architecture understood,
- existing application flow understood,
- relevant existing components identified,
- existing safe patterns identified,
- interface contracts reviewed where applicable,
- `PROJECT_GUIDE.md` generated or refreshed.

Minor UI details do not need to block Discovery.

---

## 7. Discovery Summary

Before proceeding from Discovery, summarize under these headings:

```markdown
## Application
Name:
Description:

## Problem Statement
## Product Goals
## Non-Goals
## Users / Actors
## Actor Capabilities
## Main Business Flow
## Business Rules
## Important Edge Cases
## Main Domain Concepts
## Integrations
## Authentication / Authorization
## Application Surfaces

## Technical Constraints
### Hard Constraints
### Preferences
### Open Decisions

## Acceptance / Success Criteria

<!-- Existing applications only -->
## Existing Architecture Summary
## Relevant Existing Components
## Reusable Components
## Known Technical Risks
## Potential Compatibility Constraints

## Open Questions
```
