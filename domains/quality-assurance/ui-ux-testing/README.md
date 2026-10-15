# ui-ux-testing

Automated UI/UX testing persona for web applications. Plans, writes, and executes resilient end-to-end browser tests using Playwright (primary) and Selenium (secondary), covering critical user journeys, visual regression testing (pixel diffs, snapshot baselines, dynamic masking), automated WCAG 2.1/2.2 AA accessibility audits with `axe-core`, UX edge-case state matrices (empty, loading, error, form validation), responsive multi-viewport testing (mobile, tablet, desktop), and authentication detection with `.env.test` credential safety and Playwright `storageState` session caching.

## When to Use

Invoke this skill whenever you need to build, run, or debug automated browser tests with a focus on visual and user experience quality:

* `/ui-ux-testing` — Activate the automated UI/UX testing persona.
* *"Write Playwright tests for our checkout page with visual regression and WCAG AA accessibility checks."*
* *"Set up automated responsive testing across mobile (390px) and desktop viewports to catch layout shifts."*
* *"Test our user dashboard behind authentication using .env credentials and storageState session caching."*
* *"Audit this web app for accessibility violations and provide a structured report with remediation steps."*
* *"Fix our flaky E2E tests by eliminating hardcoded sleeps and replacing fragile XPath selectors."*

## Structure

```text
ui-ux-testing/
├── SKILL.md                                 # Core workflow, modes, anti-flakiness rules, and DoD
├── README.md                                # Human overview, quick start, and changelog
├── config/
│   └── skill.yaml                           # Machine-readable manifest (extends: the-tester)
├── references/
│   ├── playwright-best-practices.md         # Resilient locators ladder, auto-waiting, POM, traces, network mocking
│   ├── auth-and-credentials.md              # Auth wall detection, .env.test setup, gitignore safety, storageState
│   ├── visual-regression.md                 # toHaveScreenshot(), masking dynamic tokens, animation freezing, baseline workflows
│   ├── accessibility-testing.md             # @axe-core/playwright, WCAG 2.1/2.2 AA tags, dynamic state scans, keyboard traps
│   ├── ux-scenario-matrix.md                # Edge states: loading skeletons, empty states, error toasts, slow network
│   ├── responsive-viewport-matrix.md        # Mobile (360/390px), tablet (768px), desktop (1280px), touch emulation
│   ├── selenium-fallback.md                 # Selenium WebDriver integration guide for legacy environments
│   ├── chat-reporting-guide.md              # Standardized markdown tables, metrics breakdown, and verdict badges
│   ├── UI_UX_TEST_PLAN.template.md          # Mode A: Scoping and planning a test suite before coding
│   └── UI_UX_TEST_REPORT.template.md        # Mode C: Dedicated persistent Markdown test results report template
├── assets/
│   ├── playwright.config.starter.ts         # TypeScript starter config with dotenv, multi-device viewports, and visual rules
│   ├── playwright.config.starter.py         # Python pytest-playwright starter config with viewport fixtures
│   ├── env.test.example                     # Starter template for .env.test credentials
│   ├── auth.setup.starter.ts                # One-time login setup script saving playwright/.auth/user.json storageState
│   ├── axe-fixture.starter.ts               # Reusable TypeScript fixture for Playwright AxeBuilder audits
│   ├── axe_fixture_starter.py               # Reusable Python fixture for axe-core accessibility auditing
│   └── sample-pom.starter.ts                # Reference Page Object Model with getByRole and getByLabel locators
├── scripts/
│   └── ui_test_helper.py                    # Verification script: validates Playwright configs and formats axe JSON
└── evals/
    └── evals.json                           # Trigger and non-trigger test cases with expected behaviors
```

## Changelog

### 0.1.0 — 2026-10-15
* Initial release of `ui-ux-testing` extending `the-tester`.
* Five operational modes: Test Matrix & Mapping (A), Suite Implementation (B), Visual & Accessibility Audit (C), Flakiness Repair (D), and Quick Sweep (E).
* Golden rules: Resilient Locator Ladder, Zero `sleep()` Guarantee, Interactive a11y Sweeps, Deterministic Visual Snapshots.
* Authentication Wall Detection & Credential Safety Gate: prompts on unexpected login walls, manages `.env.test`, enforces `.gitignore` secret exclusion, and implements Playwright `storageState` one-time login caching.
* Standardized chat response tables and mandatory report file placement confirmation gate.
* Multi-device viewport matrix (desktop, tablet, modern phone, compact Android) and horizontal overflow checks.
* Python standard-library CLI helper `scripts/ui_test_helper.py` for config validation and Axe-core JSON formatting.
* Starter assets for TypeScript and Python Playwright configurations, `env.test.example`, `auth.setup.starter.ts`, and AxeBuilder fixtures.
