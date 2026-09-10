---
name: the-architect
description: Discover new or existing applications, generate product requirements, understand existing codebases, maintain PROJECT_GUIDE.md, define architecture, and produce implementation-ready phased plans before coding. Scales from bug fixes and small changes to new products, refactors, framework upgrades, and migrations, across any language or stack.
metadata:
  version: 1.3.0
---

# The Architect — Application Foundation

Turn an idea or change request into a sufficiently understood, documented, architecture-aware, and implementation-ready plan, then implement it in verified phases.

Use it for new applications and products, features in existing applications, bug fixes and small changes, refactors / upgrades / migrations, and preparing an existing project for AI-assisted development.

It is language- and stack-agnostic. This file is the general process and the rules that always apply. Detailed and stack-specific guidance lives in `references/`; open a file when the current step needs it.

```text
Understand → Discover → Document → Architect → Scope → Implement → Test → Verify → Continue
```

Never jump directly from a rough idea into large-scale implementation.

---

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/product-discovery.md` | Running Product Discovery (Modes A, B): first-round questions, the ten discovery areas, the full PRD Coverage Gate checklist, gap handling, required understanding, and the Discovery Summary format. |
| `references/codebase-discovery.md` | Inspecting an existing repository (Modes B, D; targeted in C) and writing `PROJECT_GUIDE.md`: step-by-step discovery, scoping, contract checks, and what each guide section must contain. |
| `references/stack-profiles.md` | Detecting stacks and choosing inventory categories, verification commands, test frameworks, and `.gitignore` entries (web, mobile, desktop, data/ML, infrastructure, library/CLI, systems/embedded, games). |
| `references/testing-strategy.md` | Planning or writing tests: test levels, acceptance-criteria traceability, good-test rules, test data, external dependencies, baseline and evidence format, flaky and pre-existing failures, CI, coverage, manual checks. |
| `references/PRD.template.md` | Writing a full PRD for a new application. |
| `references/FEATURE_PRD.template.md` | Writing a feature-scoped PRD for an existing application. |
| `references/MIGRATION_BRIEF.template.md` | Writing the Mode D brief (replaces the PRD). |
| `references/ARCHITECTURE.template.md` | Writing or updating `ARCHITECTURE.md`. |
| `references/IMPLEMENTATION_PLAN.template.md` | Writing `IMPLEMENTATION_PLAN.md`. |
| `references/PHASE.template.md` | Writing an individual `phases/PHASE_NN.md`. |
| `references/PROJECT_GUIDE.template.md` | Creating or refreshing `PROJECT_GUIDE.md`. |
| `scripts/scan_repo.py` | First step of codebase discovery: `python <skill-dir>/scripts/scan_repo.py <repo_path> [--summary]`. Prints JSON with file categories, key project files, and detected sub-projects. Reads no file contents and does not replace reading the code. |
| `scripts/validate_artifacts.py` | After writing planning files: `python <skill-dir>/scripts/validate_artifacts.py <project_path> --mode new\|feature\|migration`. Checks required files and sections, checks that every `AC-xxx` is traced into the plan, and flags obvious secret leakage. Not needed in Mode C. |
| `config/skill.yaml` | Machine-readable summary of this policy. |

Use the templates as the starting structure. Fill them from real discovery; never leave invented placeholder content.

---

## Operating Modes

### Choose the Lightest Safe Mode

| Request | Mode |
|---|---|
| No application exists yet | A — New Project |
| New capability or substantial behavior change in an existing system | B — Existing Project |
| Bug fix or small, well-understood change | C — Small Change |
| Behavior-preserving restructuring, framework or runtime upgrade, platform or data migration | D — Refactor / Upgrade / Migration |

Process must stay proportional to risk, just as architecture stays proportional to complexity.

Escalate to a heavier mode as soon as a change turns out to be larger than it looked, for example when it touches a database schema, a public contract, authentication or authorization, payments, or more than a few modules. Tell the user when you escalate and why.

If the user explicitly asks for a lighter or heavier mode, follow the request, but state any significant risk of the lighter choice once.

### Mode A — New Project

Use when the application does not exist yet.

```text
Idea → Product Discovery → PRD.md → ARCHITECTURE.md → IMPLEMENTATION_PLAN.md → Phased Execution
```

### Mode B — Existing Project

Use when a repository exists and the user wants a new feature or a substantial change, or when another developer or AI agent needs to understand the application before working on it.

```text
Request → Codebase Discovery → PROJECT_GUIDE.md → Feature Discovery → PRD.md (feature-scoped)
        → Architecture Impact → IMPLEMENTATION_PLAN.md → Phased Execution
```

`PROJECT_GUIDE.md` is mandatory in this mode. Do not plan substantial implementation before the relevant code has been inspected.

### Mode C — Small Change / Bug Fix

Use when the change is small, local, and well understood: a bug fix, a copy or configuration tweak, a minor UI change, or a contained behavior adjustment.

```text
Request → Targeted Inspection → Short Plan (in chat) → Implement + Test → Verify
```

* Skip full Product Discovery, `PRD.md`, `ARCHITECTURE.md`, and `IMPLEMENTATION_PLAN.md`.
* Still inspect the relevant code, and read `PROJECT_GUIDE.md` if it exists.
* For a bug: reproduce or locate the failure and find the root cause first. Prefer a regression test that fails before the fix and passes after it.
* Before editing, state a short plan: the cause or target behavior, the files to change, the test to add, and how the change will be verified.
* Ask questions only when the expected behavior is genuinely unclear.
* All Execution Rules below still apply.
* Update `PROJECT_GUIDE.md` only if the change materially affects what it documents.

### Mode D — Refactor / Upgrade / Migration

Use when the goal is to change *how* the system is built while keeping *what* it does: restructuring, framework or runtime upgrades (for example .NET Framework → .NET 8, AngularJS → Angular, Python 2 → 3), database or platform migration, monolith decomposition, or dependency modernization.

```text
Request → Codebase Discovery → PROJECT_GUIDE.md → MIGRATION_BRIEF.md → Safety Net
        → ARCHITECTURE.md (current → target) → IMPLEMENTATION_PLAN.md (incremental, reversible) → Phased Execution
```

`MIGRATION_BRIEF.md` replaces `PRD.md`. It records the current and target state, behavior to preserve, explicitly allowed behavior changes, compatibility requirements, safety net, migration strategy, cutover plan, rollback plan, and risks.

* **Behavior preservation is the primary requirement.** Any behavior change must be listed as allowed in the brief.
* **Build the safety net first.** Before changing structure, add characterization tests that capture the current behavior of the affected area, especially where coverage is thin. This is Phase 1.
* **Prefer incremental, reversible steps** (strangler pattern, adapters, feature flags, parallel run, expand-then-contract schema changes). A big-bang step needs a stated reason and explicit approval.
* **Keep the system buildable and releasable after every phase** where practical.
* **Every phase needs a rollback path.** Schema and data changes need a tested down-migration or a restore / backfill plan.
* **Do not mix feature work into a migration** unless the user asks; plan it as separate phases.
* **Use official upgrade guides and release notes.** Do not rely on memory for version-specific breaking changes.

---

## Core Principles

1. **Understand before coding.** Discovery exists to prevent incorrect business logic, incorrect data models, unclear ownership, architecture rework, broken integrations, duplicated functionality, unnecessary refactoring, and security mistakes.
2. **Business before technical implementation.** Understand why the feature exists, who uses it, the business flow and rules, ownership, state transitions, and external dependencies before choosing implementation details.
3. **The repository is the source of truth.** Never assume architecture, framework, folder structure, names, database patterns, coding conventions, API contracts, business flows, reusable components, or integrations; inspect them. Documentation is guidance. The current repository and verified runtime behavior are the final authority.
4. **Do not overengineer.** Keep architecture proportional to complexity. Do not add abstraction layers, microservices, queues, caching, CQRS, event buses, repositories, mapping layers, or infrastructure just because they are considered enterprise patterns. Every major technical decision must solve an actual requirement.

---

## Product Discovery (Modes A and B)

Details: `references/product-discovery.md`. If invoked with only a rough idea, start with the first-round questions there.

* Discovery is adaptive, not a questionnaire. Ask only questions that materially affect requirements, business flow, domain model, architecture, integration, security, data, or scope.
* Ask about 3–6 related questions per round, highest impact first: business flow → actors / ownership / permissions → critical business rules → data integrity / state → integrations → authentication / security → hard constraints → acceptance behavior → lower-impact UX.
* Never ask what the conversation, existing documentation, or the repository already answers, and never ask for the same information twice.
* Cover the ten discovery areas where applicable: product goal, users and actors, end-to-end flow, business rules, data and domain, integrations, authentication and authorization, application surface, technical constraints (hard constraint vs preference vs open decision), and definition of success.
* Turn what the user says into Functional Requirements, Business Rules, and testable Acceptance Criteria yourself. Do not make the user write `FR-xxx`.
* Never silently turn a preference into a hard constraint, or an unknown into an assumption, when it could materially affect implementation.

**PRD Discovery Coverage Gate (mandatory).** Before leaving Discovery, run the full checklist in `references/product-discovery.md` across the ten PRD areas, marking inapplicable ones N/A. Then classify what is missing:

* **Critical gap** (could change business flow, architecture, data model, integration, security, permissions, or scope): continue Discovery with focused questions.
* **Non-critical gap** (wording, styling, details architecture can decide): record it as an assumption, open question, preference, or future decision, and do not block the PRD.

Discovery is **not** complete because a number of questions were asked, the user wrote one long message, the app sounds simple, or you believe you can infer the rest. It is complete when:

> No known unresolved ambiguity remains that is reasonably likely to cause major product, architecture, security, data, integration, or implementation rework.

Before moving on, write the Discovery Summary (format in `references/product-discovery.md`).

---

## Codebase Discovery (Modes B and D; targeted in C)

Details: `references/codebase-discovery.md` and `references/stack-profiles.md`.

Do not ask the user to describe what the code can tell you. In order:

1. **Map the repository** with `scripts/scan_repo.py`.
2. **Detect every stack** (one repository may hold a .NET API, a React app, a Flutter app, and Terraform) and load the matching stack profiles. If none match, derive the details from the stack's own conventions and say so. Verify versions from project files, not filenames or user descriptions.
3. **Inventory components mechanically** using the profile's categories. Do not inspect a handful of files and assume the rest.
4. **Cross-check interface contracts** wherever two parts communicate: client ↔ API, service ↔ service, library ↔ consumers, application ↔ schema, configuration ↔ infrastructure. Do not assume they are synchronized because both sides compile.
5. **Reconstruct the architecture that actually exists.** Keep *Existing Architecture*, *Observed Issues*, and *Possible Improvements* separate. Never document an ideal architecture as though it exists.
6. **Discover established code style and patterns** so new work stays consistent with the safe ones.
7. **Trace the important application and business flows**, not only the technical structure.
8. **Create or refresh `PROJECT_GUIDE.md`.**

**Large repositories, monorepos, and multi-repo systems:** always produce a project map first, then inventory in depth only the affected packages plus their direct dependencies and dependents (use `scan_repo.py --summary` on big repositories). For inaccessible repositories or services, record the assumed contract as an assumption or open question, and ask for access or specifications when it matters. State which areas were not inspected in depth. Never present a partial inventory as complete.

---

## PROJECT_GUIDE.md

The authoritative human-and-AI-readable map of the current project, so future developers and AI agents do not have to rediscover it. Put it in the project root unless the repository already has an established documentation location. Write it in clear English. Use `references/PROJECT_GUIDE.template.md`; `references/codebase-discovery.md` describes what each section must contain:

1. Executive Summary & Tech Stack Map
2. End-to-End Architecture & Layering
3. Established Code Style & Existing Patterns
4. Application Flow & Business Capabilities
5. Comprehensive Mechanized Inventories (from real inspection; never invent or silently omit major components)
6. AI Assistant & Developer Contribution Rules
7. Risk Matrix & Modernization Recommendations (current state kept separate from recommendation)

Never silently modernize the repository while documenting it. Keep the guide current: update it whenever implementation materially changes the architecture, major modules, important flows, API contracts, integrations, conventions, build process, or testing strategy.

---

## Security Rule — Zero Credential Leakage

Never expose secret values (passwords, API keys, access or refresh tokens, client secrets, private keys, database credentials, sensitive connection-string values) in any planning file (`PROJECT_GUIDE.md`, `PRD.md`, `MIGRATION_BRIEF.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, phase files) or in chat summaries.

Document configuration key names only, for example `ConnectionStrings:DefaultConnection`, `OpenAI:ApiKey`, `Jwt:SigningKey`. If a value must be represented, write `[REDACTED]`.

---

## Requirements Document

After Discovery passes the Coverage Gate, write the requirements document. It describes **what** the product should do and **why**, without locking in low-level implementation details.

* **Mode A:** `PRD.md` from `references/PRD.template.md`.
* **Mode B:** a feature-scoped `PRD.md` from `references/FEATURE_PRD.template.md`. Do not rewrite the whole application's requirements.
* **Mode D:** `MIGRATION_BRIEF.md` from `references/MIGRATION_BRIEF.template.md`.

Use identifiers where useful (`FR-001`, `BR-001`). Acceptance criteria **must** use `AC-001`-style identifiers so each one can be traced to a test, and must be observable and testable ("Given …, when …, then …"), never "the feature should work properly".

---

## Architecture

When the requirements are stable, create or update `ARCHITECTURE.md` from `references/ARCHITECTURE.template.md`. It answers **how** the required behavior will be implemented, and consciously addresses the template's concerns where relevant: frontend, backend, module and domain boundaries, persistence, authentication and authorization, integrations, API contracts, validation and error handling, logging and observability, configuration, concurrency and background processing, storage and caching, deployment, testing, and security.

For an existing system, do not redesign the whole application. Run an **architecture impact analysis**: does the change need no architecture change, an extension of existing modules, a new module, a new persistence model, a new API, new frontend state, a new integration, a new background process, or a genuine architecture modification? Prefer extending the existing architecture cleanly over introducing a parallel one.

---

## Code Efficiency & Safety Gate

Existing code is not correct just because it exists. If the work would copy or extend an obviously unsafe or inefficient pattern (SQL string concatenation, credential exposure, dangerous dynamic execution, memory leaks, unsafe singleton state, redundant API calls, severe N+1 data access, raw exception leakage, unsafe concurrency, duplicated expensive processing, uncontrolled resource use), stop before reproducing it:

```text
Detect problem → Explain existing pattern → Explain risk → Propose cleaner alternative
→ Explain compatibility impact → Get explicit approval → Implement chosen approach
```

Do not perform unrelated modernization automatically.

---

## Implementation Plan

Create `IMPLEMENTATION_PLAN.md` from `references/IMPLEMENTATION_PLAN.template.md` with about 3–5 phases: the fewest that keep the work understandable, bounded, independently verifiable, testable, and recoverable. Avoid both giant all-in-one phases and needless micro-phases.

The plan must include an **Acceptance Criteria Coverage** table mapping every `AC-xxx` to the phase and the test(s) that prove it.

**Source hierarchy for existing projects:** current repository → `PROJECT_GUIDE.md` (current reality) → `PRD.md` / `MIGRATION_BRIEF.md` (required behavior) → `ARCHITECTURE.md` (chosen approach) → `IMPLEMENTATION_PLAN.md` (how to move safely from current to expected state). The repository has the highest authority.

**Every phase must contain** (see `references/PHASE.template.md`):

| Section | Content |
|---|---|
| Phase Objective | What the phase achieves |
| Current State | What exists before the phase, taken from inspected code and `PROJECT_GUIDE.md` |
| Expected State | What exists after the phase |
| Reference Files | Files to read; read-only unless also listed as targets |
| Target Files | Files or directories that may be created, modified, or deleted |
| Existing Patterns to Follow | Discovered conventions that apply |
| Requirements | Business and technical requirements for this phase |
| Acceptance Criteria Covered | The `AC-xxx` this phase proves, and the test for each |
| Constraints | Rules the coding agent must respect |
| Deliverables | Concrete expected output |
| Tests | Required automated tests, with the level chosen per `references/testing-strategy.md` (unit, integration, contract, end-to-end, …) |
| Verification | Build / test / run commands or their stack equivalents |
| Test Evidence | Filled in during execution: baseline and final commands with passed / failed / skipped counts |
| Rollback / Recovery | How to undo the phase after release. Required when it changes schema, data, public contracts, configuration, or deployment; otherwise reverting its commits is enough |

---

## Execution Rules (all modes)

### Codebase Execution

Before modifying code in each phase:

1. Inspect the workspace.
2. Read the relevant `PROJECT_GUIDE.md` and architecture sections.
3. Re-read the immediate target and reference files, and inspect relevant dependencies.
4. Verify current assumptions against the repository.
5. Implement the minimum coherent change.
6. Add or update tests.
7. Build, run the tests, diagnose failures, fix, and repeat until green.

Never invent classes, functions, endpoints, schema, files, configuration, or behavior.

### Existing Pattern Preservation

Follow established patterns when they are safe, reasonably maintainable, and compatible with the requirements. Preserve naming, project structure, dependency direction, coding style, API conventions, state-management and data-access patterns, and existing public behavior. Do not refactor unrelated code without a requirement or explicit approval.

### Testing

Testing is part of implementation, not a final optional phase. Details: `references/testing-strategy.md`.

* **Every meaningful phase includes automated tests** for its changes, covering business rules, success and failure paths, authorization, state transitions, integration boundaries, and regressions as relevant, at the level chosen per `references/testing-strategy.md`.
* **Every acceptance criterion is proven.** Each `AC-xxx` maps to at least one automated test, or to a documented manual check when automation is truly impossible. Keep the plan's coverage table current.
* **See each new test fail first**, for the right reason (before the fix or feature exists, or by temporarily breaking the code), so it cannot pass trivially.
* **CI runs the tests.** If the repository has a CI pipeline, make sure the new tests run in it and do not break it. If it has none, recommend one; for a new project, propose a minimal pipeline (restore → build → test) in Phase 1.
* **No test infrastructure?** Do not silently skip testing, and do not introduce a large framework unasked. Report it, and propose the lightest conventional setup for the stack (see `references/stack-profiles.md`) as the first phase or a Phase 0. If the user declines, agree on the best alternative (a verification script, type-checking, linting, or documented manual checks) and record it in each phase's Verification section.
* **Stack-appropriate verification.** "Build" and "test" mean the stack's equivalent: compiling, type-checking, linting, `terraform validate` / `plan`, executing notebooks, building a mobile app for a simulator, and so on. Prefer the commands the repository already uses.

### Green Build Policy

Generated code is not finished code. **Green means the build passes and the full relevant test suite passes**, not only the new tests.

1. **Baseline first.** Before changing code in a phase, build and run the existing suite, and record the commands and the passed / failed / skipped counts, including the names of failing tests. If the baseline is already red, report it before starting and agree how to treat the pre-existing failures.
2. **Loop until green:** restore dependencies → build → run the full relevant suite (plus the lint and type-check steps CI runs) → diagnose → fix → retry. In very large repositories, run the affected packages plus their dependents, and state that scope.
3. **Compare with the baseline.** Every test that passed at baseline must still pass, all new tests must pass, and the skipped count must not grow without approval. Pre-existing failures stay reported; never present them as passing.
4. **Never declare a phase complete** while required builds or tests fail.
5. If a check needs something unavailable (a device, real hardware, a cloud account, an external service, production-like data), say so explicitly and list what remains to be verified.

### Honest Green — Never Fake a Passing Result

A green result must mean the software works. To reach green:

* Do not delete, skip, disable, or comment out tests (`skip`, `xit`, `@Disabled`, `[Fact(Skip = …)]`, `pytest.mark.skip`, `t.Skip()`, …).
* Do not weaken assertions, widen tolerances, loosen matchers, or replace real checks with trivially true ones.
* Do not change an existing test's expected behavior unless a requirement changed. When one did, name the requirement and state the change in the phase report.
* Do not mock or stub the code under test, or hard-code outputs to satisfy a test.
* Do not exclude tests from the run, lower coverage thresholds, mark failures as allowed, or bypass hooks and CI checks (for example `--no-verify`).
* Do not catch and swallow errors in production code just to make a test pass.

If a test looks wrong, flaky, or impossible to satisfy, stop and report it with evidence instead of working around it. Quarantining a flaky test needs explicit approval and a tracking note.

### Version Control Rules

Commits belong to the human developer.

* Do not add AI agents, assistants, or tools as commit authors or contributors.
* Do not add `Co-Authored-By:` trailers for any AI agent (Claude, Copilot, Cursor, or similar), and do not add "Generated with …" or similar AI attribution lines to commit messages or pull request descriptions.
* Do not change `git config user.name` or `user.email`, and do not use `--author` to impersonate or add another identity.
* Do not commit, push, or open pull requests unless the user explicitly asks.
* Write commit messages that describe the change, not the tool that produced it.

**.gitignore:** before the first commit in a new project, and before adding build tooling, dependencies, or configuration to an existing one:

1. Check for a `.gitignore` at the repository root, and in sub-project roots for monorepos.
2. Make sure it covers dependency folders, build output, local environment and secret files (`.env`, `.env.*` except committed examples such as `.env.example`, `*.pem`, `*.key`, `*.pfx`, `appsettings.*.local.json`, `secrets.json`), IDE and OS files, caches / logs / coverage output, and personal AI-tool files such as `.claude/settings.local.json`. The matching stack profile lists typical entries.
3. New project: create `.gitignore` as a Phase 1 deliverable.
4. Existing project: only append missing entries. Do not reorder or rewrite the file, and do not remove entries without approval.
5. If a file that should be ignored is already tracked (for example a committed `.env`), report it. Do not rewrite git history or run `git rm --cached` without explicit approval.

Planning files (`PROJECT_GUIDE.md`, `PRD.md`, `MIGRATION_BRIEF.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `phases/`) are project documentation and should be committed unless the user says otherwise.

### Phase Gate

Do not run through all phases automatically. After each phase:

* summarize the changes,
* report **test evidence**: the exact commands run, passed / failed / skipped counts compared with the baseline, the new tests added, and which acceptance criteria are now covered (automatically or manually) and which remain unverified,
* report known remaining issues and anything that could not be run,
* update relevant documentation,
* stop at the phase boundary.

Continue only when instructed.

---

## Definition of Ready

| Mode | Ready for implementation when |
|---|---|
| A — New Project | Discovery passes the Coverage Gate; purpose, actors, business flow, functional capabilities, business rules, important edge cases, and constraints are understood; acceptance criteria are testable and traced to planned tests; the PRD, architecture, and implementation plan exist. |
| B — Existing Project | Relevant code is inspected; `PROJECT_GUIDE.md` exists or is refreshed; Discovery passes the Coverage Gate; current and expected behavior are defined; impacted and reusable components are identified; business rules and edge cases are known; architecture impact is understood; acceptance criteria are testable and traced to planned tests; phases are scoped. |
| C — Small Change | Relevant code is inspected; the root cause or target behavior is clear; the test or verification step is known. |
| D — Refactor / Upgrade / Migration | `PROJECT_GUIDE.md` exists or is refreshed; `MIGRATION_BRIEF.md` defines preserved behavior and allowed behavior changes; the safety-net approach is agreed; breaking changes in the target versions are checked against official guides; every phase has a rollback path. |

## Definition of Done

A phase is complete (not merely generated) when:

* requirements are implemented and the expected behavior works,
* architecture boundaries and safe existing conventions are respected,
* every acceptance criterion in scope has a passing test, or a documented manual check where automation is impossible,
* the build and the full relevant test suite pass, with no regression against the baseline,
* no test was deleted, skipped, or weakened to get there (Honest Green),
* test evidence has been reported,
* important interface contracts (client/server, service/service, public API) remain valid,
* documentation is updated where materially affected,
* secrets, build output, and dependency folders are covered by `.gitignore` and not committed,
* no known critical error is hidden.

---

## Artifacts by Mode

| Mode | Files (project root, or the repository's existing documentation location) |
|---|---|
| A — New Project | `PRD.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `phases/PHASE_NN.md` |
| B — Existing Project | `PROJECT_GUIDE.md`, `PRD.md` (feature-scoped), `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `phases/PHASE_NN.md` |
| C — Small Change | None; the short plan lives in the conversation |
| D — Refactor / Upgrade / Migration | `PROJECT_GUIDE.md`, `MIGRATION_BRIEF.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `phases/PHASE_01.md` (safety net), `phases/PHASE_02.md`, … |

Follow the repository's existing documentation structure rather than forcing unnecessary restructuring.

---

The goal is disciplined AI-assisted development: understand reality first, define desired behavior second, verify requirement coverage third, plan the transition fourth, and code only after all four are sufficiently clear.
