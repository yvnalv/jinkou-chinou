# Testing Strategy

How to choose, write, and run tests so that a green result really means the project works. `SKILL.md` has the mandatory rules (Honest Green, baseline, full suite, traceability, evidence); this file has the detail. Stack-specific frameworks and commands are in `stack-profiles.md`.

Contents:

1. Test Levels — What to Test Where
2. From Acceptance Criteria to Tests
3. Writing Good Tests
4. Test Data
5. External Dependencies
6. Baseline, Full Suite, and Evidence
7. Pre-existing Failures and Flaky Tests
8. Continuous Integration
9. Coverage
10. When Automation Is Not Possible

---

## 1. Test Levels — What to Test Where

| Level | Use it for | Amount |
|---|---|---|
| Unit | Business rules, calculations, validation, state transitions, pure logic | Many, fast |
| Integration | Data access against a real or containerized database, ORM mappings, migrations, message handling, framework wiring (dependency injection, middleware, authentication) | Some |
| Contract / API | Request and response shapes between client and server or between services; the public API of a library | One set per boundary |
| End-to-end / UI | A few critical user journeys through the real stack | Few, slow |
| Characterization | Capturing current behavior before a refactor or migration (Mode D) | As needed for the affected area |
| Specialized | Performance / load, security (for example authorization bypass), accessibility, data quality | Only when a requirement or known risk calls for it |

Guidance:

- Prove each rule at the lowest level that can prove it, then confirm the wiring with fewer higher-level tests.
- Test authorization explicitly for both the allowed and the denied case.
- Every bug fix gets a regression test at the level where the bug lived.
- Prefer the frameworks and helpers the repository already uses. Do not introduce a new test framework when an existing one works.

---

## 2. From Acceptance Criteria to Tests

Every `AC-xxx` must map to at least one automated test, or to a documented manual check when automation is impossible (section 10).

- **Given / When / Then maps to Arrange / Act / Assert.** The "then" clause is what the test asserts.
- **Make the link visible.** Name the test after the behavior, and reference the AC id in the test name or a short comment where the codebase conventions allow it, for example `AC-003 rejects a booking that overlaps an existing one`.
- **Cover the stated failure expectations** and the important edge cases from the PRD, not only the success path.
- **Keep the traceability table in `IMPLEMENTATION_PLAN.md` current:**

| AC | Phase | Test(s) | Level | Status |
|---|---|---|---|---|
| AC-001 | 1 | `BookingServiceTests.Rejects_overlapping_booking` | Unit | Passing |
| AC-002 | 2 | `BookingApiTests.Post_booking_returns_409_on_conflict` | Integration | Passing |
| AC-003 | 3 | Manual check M-1 (payment sandbox unavailable) | Manual | Pending |

Example:

```text
AC-004: Given a valid receipt, when the user submits it, the system extracts the
supported line items and presents them for confirmation without creating a
finalized split automatically.

Tests:
- ReceiptParserTests.Extracts_supported_line_items            (unit)
- SubmitReceiptTests.Returns_items_for_confirmation            (integration)
- SubmitReceiptTests.Does_not_create_split_before_confirmation (integration)
```

---

## 3. Writing Good Tests

- **See it fail first, for the right reason.** Run the new test before the fix or feature exists, or temporarily break the code, and confirm it fails with the expected message. A test that has never failed may be testing nothing.
- **Test behavior through public interfaces**, not private implementation details. A refactor that preserves behavior should not break tests.
- **One behavior per test**, with clear arrange / act / assert steps and a descriptive name.
- **Deterministic.** Control time, randomness, generated IDs, ordering, locale, and time zone. Do not use sleeps for synchronization. Do not depend on test order or shared mutable state.
- **Meaningful assertions.** Check the actual outcome (returned values, persisted state, emitted events, error type and message), not merely "no exception was thrown".
- **Follow the repository's conventions** for test location, naming, fixtures, and helpers.

---

## 4. Test Data

- Build minimal, explicit data inside the test, or with builders / factories. Avoid large shared fixtures that hide what matters.
- Never use production data or real credentials. Use synthetic data; if realistic data is essential, it must be anonymized and approved.
- Each test sets up and cleans up its own data (rolled-back transactions, fresh containers, temporary directories).

---

## 5. External Dependencies

| Dependency | Preferred approach in tests |
|---|---|
| Database | A real engine in a container (Testcontainers, docker compose) or the project's established test database. Use in-memory substitutes only when their behavior is close enough for what is being tested. |
| Third-party HTTP APIs | Fakes or stubs at the HTTP boundary (for example WireMock, MSW, respx, httpmock), plus a small number of optional tests against the provider's sandbox. |
| Message brokers / queues | A containerized broker or the framework's in-process test harness. |
| Time, randomness, IDs | An injectable clock or generator. |
| File system | Temporary directories. |
| Payments, email, SMS, push | Provider test mode or fakes. Never send real messages or real charges. |

Mock boundaries you do not own. Never mock the code under test.

Tests that need infrastructure (a database container, a broker) may be grouped so they can run separately, but they are still required when the phase needs them. If they could not run in the current environment, report that explicitly.

---

## 6. Baseline, Full Suite, and Evidence

### Baseline

Before changing any code in a phase, build and run the full relevant test suite and record the result:

```text
Baseline — commit abc1234
Command: dotnet test
Result:  412 passed, 3 failed, 5 skipped
Failing: OrdersTests.Export_csv_includes_totals (pre-existing)
         ...
```

If the baseline is already red, report it before starting and agree with the user how to treat the pre-existing failures.

### Full Relevant Suite

- Normal repositories: the entire test suite, plus the lint and type-check steps the repository's CI runs.
- Very large repositories and monorepos: the affected packages plus their dependents. State that scope explicitly in the evidence.
- New tests alone are never enough to call a phase green.

### Final Run and Comparison

Run the same commands again at the end of the phase and compare:

- every test that passed at baseline still passes,
- all new tests pass,
- the skipped count has not increased (unless explicitly approved),
- pre-existing failures are still listed, never presented as passing.

### Evidence Format

Record this in the phase's **Test Evidence** section and in the phase report:

```text
Baseline: dotnet test → 412 passed, 3 failed (pre-existing), 5 skipped
Final:    dotnet test → 421 passed, 3 failed (same pre-existing), 5 skipped
New tests: 9 (all seen failing before implementation)
Acceptance criteria covered: AC-001, AC-002 (automated); AC-003 (manual check M-1)
Not run: payment sandbox tests (no sandbox credentials in this environment)
```

---

## 7. Pre-existing Failures and Flaky Tests

- **Pre-existing failures:** report them at baseline. Do not hide them, and do not silently fix unrelated failures outside the phase's scope. Ask whether to fix them as a separate phase.
- **A test that starts failing after your change** is a real regression until proven otherwise.
- **Suspected flaky test:** re-run it (for example three times) and report the evidence. Fix the root cause if it is in scope. Quarantining a flaky test requires explicit approval and a tracking note. Never quarantine a test that fails because of your change.

---

## 8. Continuous Integration

- Find the CI configuration (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`, …).
- Make sure new tests are picked up by the command CI runs: the right project or folder, the naming pattern the runner discovers, and no excluded test category.
- Run the same commands CI runs locally where possible.
- Never change CI to skip tests, allow failures, or lower thresholds.
- **No CI yet:** recommend a minimal pipeline (restore → build → test). For a new project, propose it as a Phase 1 deliverable. Adding CI to an existing project needs the user's approval.

---

## 9. Coverage

- Coverage is a signal, not a goal. Never write assertion-free tests to raise a percentage.
- Respect existing coverage thresholds and never lower them.
- New and changed code should be covered by meaningful tests.
- Typical tools: coverlet (.NET), JaCoCo (JVM), coverage.py / pytest-cov (Python), c8 / istanbul / `vitest --coverage` (JavaScript / TypeScript), `go test -cover` (Go), `cargo llvm-cov` (Rust).

---

## 10. When Automation Is Not Possible

Examples: physical devices or hardware, visual or gameplay feel, a third-party service with no sandbox.

- Write a manual check with an id (`M-1`), exact steps, and the expected result, and reference the AC it verifies.
- Automate everything around it that can be automated.
- In the phase report, state clearly which acceptance criteria are verified automatically, which manually, and which remain unverified.
