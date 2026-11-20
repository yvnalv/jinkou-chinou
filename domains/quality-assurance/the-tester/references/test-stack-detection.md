# Test Stack Detection

Before writing tests, you must determine the appropriate testing stack for the current project. **Always prefer established patterns.** If the project already uses a testing framework, adopt it. If not, select the most standard tool based on the ecosystem.

## Language and Ecosystem Defaults

If no testing framework is detected, use the following standard defaults based on the dominant language or framework in the repository:

### JavaScript / TypeScript
* **Unit/Integration:** `Jest` (standard for React/Node), `Vitest` (standard for Vite/Vue projects), or `Mocha` + `Chai`.
* **Component Testing:** `@testing-library/react` (or angular/vue), `Enzyme` (legacy).
* **End-to-End (E2E):** `Playwright` (recommended for modern TS/JS E2E), `Cypress`, or `Selenium`.

### Python
* **Unit/Integration:** `pytest` (strongly preferred for its rich assertion ecosystem and fixtures) or `unittest` (built-in, if already used).
* **E2E / Browser:** `Playwright for Python`, `Selenium`, or `Robot Framework`.

### Java / Kotlin
* **Unit/Integration:** `JUnit 5` (Jupiter), `TestNG`.
* **Mocking:** `Mockito`, `MockK`.
* **E2E:** `Selenium WebDriver`, `Selenide`, `Playwright for Java`.

### C# / .NET
* **Unit/Integration:** `xUnit.net` (default for modern .NET Core), `NUnit`, `MSTest`.
* **Mocking:** `Moq`, `NSubstitute`.
* **E2E:** `Playwright for .NET`, `Selenium`.

### Go
* **Unit/Integration:** `testing` (the built-in standard library package).
* **Mocking:** `gomock`, `testify` (for rich assertions).

### Ruby
* **Unit/Integration:** `RSpec` (strongly preferred in Rails ecosystems), `Minitest`.
* **E2E:** `Capybara` with `Selenium`.

## How to Detect Existing Stacks

Do not guess. Look for the following artifacts to determine the existing test setup:

1. **Package Managers:** `package.json` (JS), `requirements.txt` / `Pipfile` / `pyproject.toml` (Python), `pom.xml` / `build.gradle` (Java), `*.csproj` (C#), `go.mod` (Go).
2. **Test Directories:** Folders named `tests/`, `__tests__/`, `spec/`, or `t/`.
3. **Test Filename Conventions:** Files ending in `_test.py`, `.spec.ts`, `.test.js`, or starting with `Test*.java`.
4. **CI/CD Pipelines:** Inspect `.github/workflows/`, `.gitlab-ci.yml`, or `Jenkinsfile` for existing test execution commands.

## Automated Dependency & Browser Binary Bootstrap

Before executing any test suite, verify that the chosen test runner and (for E2E tests) browser binaries exist. If missing, install them automatically:

* **Node.js / TypeScript (Playwright E2E):**
  ```bash
  # If node/npx is missing on Windows:
  winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
  # Install Playwright test runner and Chromium binaries:
  npm install -D @playwright/test @axe-core/playwright dotenv
  npx playwright install chromium
  ```
* **Node.js / TypeScript (Vitest / Jest Unit & Integration):**
  ```bash
  npm install -D vitest
  # or
  npm install -D jest @types/jest ts-jest
  ```
* **Python (PyTest + Playwright E2E):**
  ```bash
  python -m pip install pytest playwright pytest-playwright axe-playwright-python
  python -m playwright install chromium
  ```
* **Python (PyTest Unit & Integration):**
  ```bash
  python -m pip install pytest pytest-cov
  ```

