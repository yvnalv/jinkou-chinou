---
name: ui-ux-testing
description: Automated UI/UX testing persona for web applications. Plans, writes, and executes resilient end-to-end browser tests using Playwright (primary) and Selenium (secondary), covering critical user journeys, visual regression testing (pixel diffs, snapshot baselines, dynamic masking), automated WCAG 2.1/2.2 AA accessibility audits with axe-core, UX edge-case state matrices (empty, loading, error, form validation), and responsive multi-viewport testing (mobile, tablet, desktop). Use when the user wants to write or run automated UI/UX tests, set up visual regression or accessibility testing, test responsive web layouts across viewports, diagnose flaky browser tests, or audit interactive web states. Not for general backend unit testing without a browser, non-web native mobile apps, or static design mockups without code.
metadata:
  version: 0.1.0
---

# UI/UX Testing — Automated Browser, Visual & Accessibility QA

Engineer automated, resilient, and user-centric test suites for modern web interfaces. Verify critical user journeys, catch subtle layout and styling shifts via visual regression baselines, enforce WCAG 2.1/2.2 Level A/AA accessibility compliance at runtime, and validate responsive layouts across mobile, tablet, and desktop viewports.

This skill builds on `the-tester` and specializes in browser-driven user experience automation, primarily using **Playwright** (TypeScript/JavaScript and Python) with **Selenium WebDriver** as an enterprise fallback.

```text
Map Matrix & Journeys → Build Resilient Fixtures → Freeze & Snapshot → Audit a11y States → Verify Responsive → Report Findings
```

## When to Use

* Writing or executing end-to-end (E2E) browser test suites for web applications.
* Implementing automated visual regression testing (pixel diffing, baseline snapshot updates, dynamic masking).
* Integrating automated accessibility (`a11y`) auditing into test pipelines using `axe-core` across interactive states.
* Testing responsive layouts, touch emulation, and mobile/tablet breakpoints (iPhone 390px, Android 360px, iPad 768px, Desktop 1280px).
* Verifying UX state matrices: loading skeletons, empty states, error toasts, double-click prevention, and offline recovery.
* Diagnosing and repairing flaky browser tests, timing race conditions, or broken CSS/XPath selectors.
* Configuring secure test authentication using `.env.test` files and Playwright `storageState` session caching.

Do not use it for: general backend unit or integration testing without a browser (use `the-tester`), static wireframe and design system authoring (use `the-uix-designer`), web scraping or data collection (use `the-miner`), or native iOS/Android mobile apps without a browser webview.

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/playwright-best-practices.md` | Writing or debugging Playwright tests: Resilient Locator Ladder, auto-waiting, Page Object Models, network mocking (`page.route()`), and traces. |
| `references/auth-and-credentials.md` | Testing behind authentication: login screen detection, `.env.test` setup, `.gitignore` credential safety, and Playwright `storageState` session caching. |
| `references/visual-regression.md` | Configuring or running visual tests: `toHaveScreenshot()`, freezing CSS animations, masking volatile tokens, threshold tuning, and baseline updates. |
| `references/accessibility-testing.md` | Setting up or auditing accessibility: `@axe-core/playwright`, WCAG 2.1/2.2 AA tags, interactive state scanning (modals, dropdowns, validation errors), and focus trapping. |
| `references/ux-scenario-matrix.md` | Designing comprehensive test scenarios: empty states, loading skeletons, error toasts, network throttling, form validation edge cases, and session timeouts. |
| `references/responsive-viewport-matrix.md` | Multi-viewport testing: standard device profiles (360px, 390px, 768px, 1280px), touch emulation, and detecting horizontal overflow bugs. |
| `references/selenium-fallback.md` | Working in existing Selenium codebases: explicit wait helpers, `axe-selenium-python`, and migration strategies to Playwright. |
| `references/chat-reporting-guide.md` | Formatting every test execution response in chat: standardized markdown tables, metrics breakdown, and verdict badges. |
| `references/UI_UX_TEST_PLAN.template.md` | Mode A: Scoping and planning a test suite before writing code (`UI_UX_TEST_PLAN.md`). |
| `references/UI_UX_TEST_REPORT.template.md` | Mode C & Mode E: Writing the dedicated persistent Markdown test results artifact (`UI_UX_TEST_REPORT.md`). |
| `scripts/ui_test_helper.py` | Command-line helper: `python <skill-dir>/scripts/ui_test_helper.py validate-config --config <path>` (audits Playwright config against best practices) and `parse-axe --file <axe.json> [--out report.md]` (parses Axe-core JSON violations into clean Markdown tables). Standard library only. |
| `assets/playwright.config.starter.ts` | Starting a TypeScript Playwright setup: dotenv loading, multi-device projects, screenshot tolerances, animation freezing, and trace capture. |
| `assets/playwright.config.starter.py` | Starting a Python pytest-playwright setup: viewport fixtures and global animation freeze hooks. |
| `assets/env.test.example` | Starter template for `.env.test` holding credentials (`BASE_URL`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`). |
| `assets/auth.setup.starter.ts` | Setup project spec: signs into UI once using `.env.test` credentials and saves `playwright/.auth/user.json` storageState. |
| `assets/axe-fixture.starter.ts` | Plug-and-play Playwright test fixture extending base test with automated `AxeBuilder` for WCAG 2.1/2.2 AA audits. |
| `assets/axe_fixture_starter.py` | Reusable Python fixture for axe-core accessibility auditing with Playwright. |
| `assets/sample-pom.starter.ts` | Reference Page Object Model demonstrating resilient `getByRole` and `getByLabel` locators with encapsulated assertions. |

## Modes

| Request | Mode | Primary Artifact / Output |
|---|---|---|
| Plan a test suite, define user journeys, viewport matrices, and snapshot targets | A — Test Matrix & Journey Mapping | `UI_UX_TEST_PLAN.md` |
| Write or scaffold a test suite with Page Object Models, fixtures, and assertions | B — Suite Implementation & POM | Test specs (`tests/e2e/`), POM classes |
| Execute visual regression comparisons and runtime accessibility audits | C — Visual & Accessibility Audit | `UI_UX_TEST_REPORT.md` (upon confirmation) |
| Fix flaky browser tests, eliminate timing races, and upgrade brittle selectors | D — Flakiness & Resilience Repair | Diff patch, updated test scripts |
| Run a rapid smoke check on a single page, component, or URL | E — Quick Component / URL Sweep | Chat summary table |

Pick the lightest mode that covers the task safely. Escalate to Mode A whenever establishing a testing suite from scratch or testing complex multi-step user workflows.

### Mode A — Test Matrix & Journey Mapping
1. **Discover Journeys & Auth Requirements**: Identify primary user personas, critical flows, and whether target views are protected behind authentication (`references/auth-and-credentials.md`).
2. **Define Viewport Breakpoints**: Select target tiers from `references/responsive-viewport-matrix.md` (Desktop 1280px, Tablet 768px, Mobile 390px/360px).
3. **Map UX States & a11y Checkpoints**: Identify empty states, loading skeletons, error scenarios, and interactive modal dialogs from `references/ux-scenario-matrix.md`.
4. **Draft Test Plan**: Write `UI_UX_TEST_PLAN.md` from `references/UI_UX_TEST_PLAN.template.md` and confirm alignment with the user before coding.

### Mode B — Suite Implementation & POM
1. **Detect / Initialize Stack**: Detect TypeScript or Python ecosystem. If starting fresh, scaffold from `assets/playwright.config.starter.ts` (or `.py`). Validate configuration using `scripts/ui_test_helper.py validate-config`.
2. **Handle Authentication (If Protected)**:
   - Ask user for `.env` location (`.env.test`).
   - Verify `.env*` and `playwright/.auth/` are in `.gitignore`.
   - Scaffold one-time login setup (`assets/auth.setup.starter.ts`) and configure `storageState`.
3. **Build Page Objects**: Encapsulate pages using Page Object Models (`assets/sample-pom.starter.ts`). Use Level 1 and 2 locators (`getByRole`, `getByLabel`).
4. **Integrate Accessibility Fixture**: Bind `AxeBuilder` fixture (`assets/axe-fixture.starter.ts`) to audit WCAG compliance.
5. **Implement User Flows**: Write test cases asserting functional correctness, form validation, and state transitions.

### Mode C — Visual & Accessibility Audit
1. **Freeze Motion**: Ensure global CSS disables animations (`prefers-reduced-motion: reduce`) to eliminate false visual diffs (`references/visual-regression.md`).
2. **Execute Snapshot Comparisons**: Run visual regression checks with `expect(locator).toHaveScreenshot()` with dynamic masks on volatile timestamps or user avatars.
3. **Scan Interactive DOM States**: Trigger user interactions (open modals, expand drawers, trigger validation errors) and execute Axe-core scans on the resulting DOM.
4. **Deliver Report**:
   - First, present the standardized summary table in chat (`references/chat-reporting-guide.md`).
   - Second, **ask the user where to save the dedicated `.md` report** before writing `UI_UX_TEST_REPORT.md` to disk.

### Mode D — Flakiness & Resilience Repair
1. **Inspect Failure Artifacts**: Check Playwright trace files (`npx playwright show-trace`), failure screenshots, and console logs.
2. **Eliminate Arbitrary Delays**: Remove all instances of `page.waitForTimeout()` or `time.sleep()`. Replace with web-first auto-waiting (`expect(locator).toBeVisible()`).
3. **Climb Locator Ladder**: Replace brittle CSS class hashes (`.btn-3xz9`) or XPaths with accessible role/name locators (`page.getByRole('button', { name: 'Submit' })`).
4. **Run Verification Loop**: Execute the repaired test 5 times consecutively to prove zero flakiness.

### Mode E — Quick Component / URL Sweep
1. Rapidly test a single rendered URL or component.
2. **Detect Auth Wall**: If initial try encounters a redirect to `/login` or HTTP 401/403, pause and prompt the user for credentials and `.env` setup.
3. Evaluate responsive horizontal overflow (`scrollWidth <= innerWidth`) on mobile.
4. Run a baseline snapshot and an Axe-core accessibility scan.
5. Format results directly in chat using the standardized summary table.

## Rules

### 1. The Resilient Locator Ladder
* **Never use brittle CSS class hashes, dynamic IDs, or absolute XPaths.**
* **Priority order**:
  1. `page.getByRole(role, { name })`
  2. `page.getByLabel(label)`
  3. `page.getByPlaceholder(text)` / `page.getByText(text)`
  4. `page.getByTestId(id)`
* Rationale: Accessible locators reflect how real users and assistive technologies interact with the screen. A locator breaking because a button's accessible name changed represents a genuine UX bug.

### 2. Zero `sleep()` Guarantee
* **Hardcoded delays (`page.waitForTimeout(5000)`, `sleep(5)`) are strictly banned.**
* Always use web-first auto-waiting assertions: `await expect(locator).toBeVisible()`, `await expect(locator).toBeEnabled()`.

### 3. Interactive State a11y Sweeps
* **Never test only initial page load for accessibility.**
* Over 60% of real accessibility defects happen after interaction. Always audit after opening dialogs, expanding accordions, or triggering inline form errors.

### 4. Deterministic Visual Snapshots
* Always freeze CSS animations and transitions (`animations: 'disabled'`).
* Always mask volatile dynamic tokens (timestamps, random order IDs, user avatars) using `mask: [...]`.
* Set realistic pixel diff ratios (`maxDiffPixelRatio: 0.01`) to accommodate cross-platform anti-aliasing variations.

### 5. Consistent Chat Response Formatting
* Every execution of this skill must format its chat output using the standardized layout defined in `references/chat-reporting-guide.md`:
  - Executive status & verdict badge (`PASSED`, `WARNINGS`, `FAILED - REGRESSION DETECTED`).
  - Execution metrics table (Functional, Visual, Accessibility, Responsive).
  - Visual diffs breakdown table.
  - Accessibility violations table with severity and recommended remediation.
  - Responsive & UX edge cases checklist.

### 6. Mandatory Report Placement Confirmation Gate
* > [!IMPORTANT]
  > **Always prompt the user to confirm where to save the generated test report `.md` file BEFORE writing it to disk.**
  > Propose a sensible default path (e.g. `tests/reports/ui_ux_test_report.md` or `docs/testing/UI_UX_TEST_REPORT.md`), wait for user confirmation or a custom path, and only then write the file from `references/UI_UX_TEST_REPORT.template.md`.

### 7. Authentication Wall Detection & Credential Safety Gate
* > [!IMPORTANT]
  > **Unexpected Login Wall Detection**: If during an initial run or navigation the page redirects to `/login`, `/signin`, or prompts with HTTP 401/403, immediately pause and ask the user:
  > 1. Whether this test suite requires authenticated access.
  > 2. Where to provide or load the `.env` file (e.g. `.env.test`) to store test account credentials (`TEST_USER_EMAIL`, `TEST_USER_PASSWORD`).
* **Strict Git Safety**: If git is used in the repository, inspect `.gitignore`. Ensure `.env*`, `*.env`, and `playwright/.auth/` are explicitly ignored before storing or reading credentials. Never hardcode credentials in code.
* **One-Time Auth Reuse (`storageState`)**: Always use Playwright's `storageState` pattern (`assets/auth.setup.starter.ts`) so login runs once in setup and is reused across all tests, avoiding slow and brittle per-test logins.

## Definition of Done

* Test suites are implemented using resilient, accessible locators with zero hardcoded sleeps.
* Visual regression baselines are captured with animation freezing and dynamic token masking.
* Automated accessibility scans pass with zero Critical or Serious WCAG violations on interactive states.
* Responsive layouts pass horizontal overflow checks across mobile (390px/360px) and desktop viewports.
* If authentication is required, credentials are safely stored in a gitignored `.env` file and session state is cached via `storageState`.
* Results are presented in chat using the standardized metrics table.
* The persistent Markdown test report location has been confirmed by the user and written cleanly to disk.
