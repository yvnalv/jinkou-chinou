# PHASE_[NN] — [Name]

## Phase Objective

## Current State

## Expected State

## Reference Files

## Target Files

## Existing Patterns to Follow

## Requirements

## Acceptance Criteria Covered
| AC | Test(s) | Level |
|---|---|---|

## Constraints

## Deliverables

## Tests
> Level per testing-strategy.md. Each new test must be seen failing, for the right reason, before it passes.

## Verification
```text
# build command (or stack equivalent)
# full relevant test suite
```

## Rollback / Recovery
> Required when this phase changes schema, data, public contracts, configuration, or deployment. Otherwise: "Revert the phase's commits."

## Test Evidence
> Filled in during execution. Never present pre-existing failures as passing.

```text
Baseline: <command> → <passed> passed, <failed> failed, <skipped> skipped
          Failing at baseline: <names, or none>
Final:    <command> → <passed> passed, <failed> failed, <skipped> skipped
New tests: <count> (all seen failing before implementation)
Acceptance criteria covered: <AC ids automated> / <AC ids manual, with check ids>
Not run / not verifiable here: <what and why, or none>
```

## Completion Gate
- [ ] Implementation complete
- [ ] Baseline recorded before changes
- [ ] New tests added, each seen failing first
- [ ] Every acceptance criterion in this phase has a passing test (or a documented manual check)
- [ ] Full relevant test suite passes, with no regression against the baseline
- [ ] No test deleted, skipped, disabled, or weakened to get green
- [ ] Build passes (plus lint / type-check if CI runs them)
- [ ] New tests run in CI (if the project has CI)
- [ ] Contracts verified
- [ ] Rollback path defined (if schema, data, contracts, configuration, or deployment changed)
- [ ] Documentation updated if materially affected
- [ ] Test evidence reported
- [ ] No known critical issue hidden
