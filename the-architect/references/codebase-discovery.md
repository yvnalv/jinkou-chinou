# Codebase Discovery

Detailed guidance for inspecting an existing repository (Modes B and D, and the targeted inspection in Mode C) and for writing `PROJECT_GUIDE.md`. Use it with `stack-profiles.md`, which supplies the stack-specific inventory categories and commands.

The purpose is to understand what already exists before deciding what should change.

Contents:

1. Order of Work
2. Stack Detection
3. Mechanized Inventory and Scoping
4. Interface / Contract Cross-Check
5. Architecture Reconstruction
6. Code Style and Existing Patterns
7. Application and Business Flow
8. PROJECT_GUIDE.md — Required Structure
9. PROJECT_GUIDE.md — Maintenance

---

## 1. Order of Work

Do not begin by asking the user to describe information the code can answer.

1. Inspect the repository structure. Start with `scripts/scan_repo.py`.
2. Detect every stack and load the matching profiles from `stack-profiles.md`.
3. Inventory the relevant components, scoped as in section 3.
4. Reconstruct the architecture.
5. Discover coding patterns.
6. Trace the major application flows.
7. Cross-check interface contracts where applicable.
8. Create or refresh `PROJECT_GUIDE.md`.

Then combine repository knowledge with the requested change, and run the PRD Discovery Coverage Gate (`product-discovery.md`) against repository-discovered information, existing documentation, the current conversation, and the request. Ask only unresolved product or business questions that materially affect implementation.

In Mode C, do only as much of steps 1–7 as the affected area needs.

---

## 2. Stack Detection

Identify the actual technology stack. A repository may contain several, for example a .NET API, a React web app, a Flutter mobile app, and Terraform. Identify each one and where it lives.

Identify where possible:

- framework and runtime versions,
- package managers,
- important libraries,
- build tooling,
- frontend and backend technology,
- persistence,
- deployment-related technologies.

Verify from project files and implementation. Do not rely only on filenames or user descriptions.

If no profile in `stack-profiles.md` matches, derive the inventory categories and verification commands from the stack's own conventions and say so.

---

## 3. Mechanized Inventory and Scoping

When repository tools are available, inspect the project mechanically. Do not inspect a handful of representative files and assume the rest.

Inventory important source components using the categories from the matching stack profile(s). For a typical web system that means endpoints, services, data access, entities, DTOs, validators, middleware, authentication, background jobs, integrations, and configuration key names on the backend; and pages, components, routes, state, API clients, and build configuration on the frontend.

### Large Repositories, Monorepos, and Multi-Repo Systems

A complete file-by-file inventory is not always practical.

- **Monorepo:** first build a project map of every app and package and its role (`scan_repo.py` lists detected sub-projects). Then inventory in depth only the packages the request touches, plus their direct dependencies and dependents.
- **Large repository:** always produce the top-level map. Go deep on the affected area, and state explicitly which areas were not inspected in depth. Use `scan_repo.py --summary` to avoid a huge file listing.
- **Multi-repo / microservices:** list the repositories and services that take part in the affected flow and inspect what is accessible. For anything inaccessible, record the assumed contract as an explicit assumption or open question, and ask for access or specifications when it materially affects the work.
- Never present a partial inventory as complete.

---

## 4. Interface / Contract Cross-Check

Wherever two parts of the system communicate, inspect both sides where accessible. Typical pairs:

- web or mobile client ↔ backend API,
- service ↔ service (HTTP, gRPC, queues, events),
- library or SDK public API ↔ its consumers,
- application ↔ database schema and migrations,
- application configuration ↔ infrastructure-as-code and deployment settings.

For client ↔ server pairs, map client calls to server endpoints where practical.

Check for:

- client calls with no matching server endpoint,
- apparently unused server routes,
- route mismatches,
- HTTP method mismatches,
- request payload mismatches,
- response shape assumptions,
- authentication assumptions,
- inconsistent error handling,
- duplicate API abstractions,
- schema or message-format drift between producers and consumers.

Do not assume contracts are synchronized merely because both sides compile.

---

## 5. Architecture Reconstruction

Reconstruct the architecture that actually exists. Identify:

- layers, modules, feature boundaries, and domain boundaries,
- shared libraries and dependency direction,
- persistence boundaries and external integration boundaries,
- frontend / backend communication,
- background processing,
- cross-cutting concerns.

Keep three things separate:

- **Existing Architecture** — what exists now.
- **Observed Issues** — problems detected in the current architecture.
- **Possible Improvements** — optional future recommendations.

Never document an ideal architecture as though it currently exists.

---

## 6. Code Style and Existing Patterns

Inspect where relevant: naming conventions, directory structure, class organization, async behavior, dependency management, service patterns, repository patterns, database access, validation, error handling, logging, DTO usage, API style, frontend component style, state management, API invocation, configuration patterns, and testing style.

Future implementation should stay consistent with safe established patterns unless a change is explicitly justified.

---

## 7. Application and Business Flow

Do not document only technical structure. Understand how the application behaves: major capabilities, important user flows, business workflows, important rules, state transitions, approval flows, ownership, and external-system interactions.

Where useful, trace a flow end to end:

```text
User Action
    ↓
Frontend
    ↓
API / Request
    ↓
Controller / Endpoint
    ↓
Service / Application Logic
    ↓
Domain / Business Logic
    ↓
Persistence / Integration
    ↓
Response
    ↓
Frontend State / UI
```

Adapt the layers to the stack, for example *trigger → pipeline step → dataset → consumer* for a data system, or *command → library call → output* for a CLI. Use Mermaid diagrams where they materially improve understanding.

---

## 8. PROJECT_GUIDE.md — Required Structure

`PROJECT_GUIDE.md` is the authoritative human-and-AI-readable map of the current project, so future developers and AI coding agents do not need to rediscover the application blindly. Prefer the project root unless the repository already has an established documentation location. It MUST be written in clear English. Start from `PROJECT_GUIDE.template.md`.

### 1. Executive Summary & Tech Stack Map

Application purpose; each stack or sub-project (location, language, runtime, framework); persistence; major libraries; external integrations; runtime / deployment context.

### 2. End-to-End Architecture & Layering

Layers, modules, dependency relationships, domain boundaries, frontend / backend communication, persistence flow, external integrations. Include Mermaid diagrams when useful.

### 3. Established Code Style & Existing Patterns

Patterns future contributors should follow, for example naming, directories, service structure, repository usage, error handling, validation, asynchronous behavior, state management, frontend component style, API calling conventions.

### 4. Application Flow & Business Capabilities

Important product capabilities, user journeys, business flows, major state transitions, important business rules.

### 5. Comprehensive Mechanized Inventories

An inventory for each stack or sub-project, using the categories from `stack-profiles.md`; for monorepos, a project map first. Inventories must come from actual repository inspection. Do not silently invent or omit major components, and state which areas were not inspected in depth.

### 6. AI Assistant & Developer Contribution Rules

How future contributors should work in the repository: architecture boundaries, dependency direction, patterns to preserve, reusable components, sensitive areas, files or modules requiring extra care, test expectations, build commands, verification requirements, and git rules (human authorship only, no AI co-author trailers or attribution lines, `.gitignore` coverage).

### 7. Risk Matrix & Modernization Recommendations

Observed risks, documented separately from current behavior. Possible areas: security, performance, reliability, maintainability, architectural coupling, outdated dependencies, duplicate logic, data access, interface contracts, testing gaps.

Clearly distinguish **Current State** from **Recommendation**. Never silently modernize the repository while documenting it.

---

## 9. PROJECT_GUIDE.md — Maintenance

`PROJECT_GUIDE.md` is not a one-time artifact. Update it when implementation materially changes architecture, major modules, important application flows, API contracts, external integrations, developer conventions, the build process, or testing strategy.

Do not knowingly let it drift from repository reality.
