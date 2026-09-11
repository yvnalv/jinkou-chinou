# Implementation Plan

## Source Hierarchy

For existing projects:

```text
Current Repository
↓
PROJECT_GUIDE.md
↓
PRD.md / Feature Requirements / MIGRATION_BRIEF.md
↓
ARCHITECTURE.md
↓
IMPLEMENTATION_PLAN.md
```

## Acceptance Criteria Coverage

> Every AC-xxx from the requirements document must appear here with the test(s) that prove it. Use a manual check id (M-1, …) only when automation is truly impossible.

| AC | Phase | Test(s) | Level | Status |
|---|---|---|---|---|
| AC-001 | 1 | | Unit / Integration / Contract / E2E / Manual | Planned |

## Test Commands

> The commands that define "green" for this project, taken from the repository or CI. See stack-profiles.md and testing-strategy.md.

```text
# restore / install
# build
# full test suite
# lint / type-check (if CI runs them)
```

---

## Phase 1 — [Name]

### Phase Objective

### Current State

### Expected State

### Reference Files
> Read-only unless also listed as targets.
- 

### Target Files
- 

### Existing Patterns to Follow
- 

### Requirements
- 

### Acceptance Criteria Covered
- AC-xxx → test name

### Constraints
- 

### Deliverables
- 

### Tests
> Level per testing-strategy.md. Each test must be seen failing before it passes.
- 

### Verification
```text
# build command (or stack equivalent)
# full relevant test suite
```

### Rollback / Recovery
> Required when the phase changes schema, data, public contracts, configuration, or deployment. Otherwise: "Revert the phase's commits."

---

## Phase 2 — [Name]

### Phase Objective

### Current State

### Expected State

### Reference Files
- 

### Target Files
- 

### Existing Patterns to Follow
- 

### Requirements
- 

### Acceptance Criteria Covered
- 

### Constraints
- 

### Deliverables
- 

### Tests
- 

### Verification

### Rollback / Recovery

---

## Phase 3 — [Name]

### Phase Objective

### Current State

### Expected State

### Reference Files
- 

### Target Files
- 

### Existing Patterns to Follow
- 

### Requirements
- 

### Acceptance Criteria Covered
- 

### Constraints
- 

### Deliverables
- 

### Tests
- 

### Verification

### Rollback / Recovery
