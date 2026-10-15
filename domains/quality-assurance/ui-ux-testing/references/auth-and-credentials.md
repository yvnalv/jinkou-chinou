# Authentication, Credentials & Environment Safety

This reference defines how `/ui-ux-testing` handles protected user interfaces, login barriers, credential management, and git security.

---

## 1. The Authentication Detection Gate

When running an initial smoke check, visual snapshot, or E2E flow, the agent must check if the target view is behind an authentication wall:

### Detection Signals
* **URL Redirect**: The page automatically redirects to paths containing `/login`, `/signin`, `/auth`, or `/sso`.
* **HTTP Status**: Response headers indicate `401 Unauthorized` or `403 Forbidden`.
* **DOM Signatures**: The rendered page contains password inputs (`input[type="password"]`), SSO provider buttons ("Sign in with Google", "SAML SSO"), or session expiry modals.

### Mandatory Agent Action
> [!IMPORTANT]
> If an unexpected login screen or auth wall is detected during execution, **do NOT fail silently or invent dummy credentials**.
> 
> Immediately ask the user:
> 1. *"The page at `[URL]` redirected to a login screen. Does this test suite require authenticated access?"*
> 2. *"Where should I locate or create your `.env` file (e.g. `.env.test`) to safely store the required test credentials (`TEST_USER_EMAIL`, `TEST_USER_PASSWORD`)?"*

---

## 2. Environment Variables & `.gitignore` Safety

**Never hardcode credentials, passwords, API keys, or session tokens in test files or repository code.**

### A. The `.env` Configuration Pattern
Always load credentials from a dedicated test environment file using `dotenv`:
* Recommended file name: `.env.test` or `.env.local`
* Example structure:
  ```env
  BASE_URL=https://staging.example.com
  TEST_USER_EMAIL=qa-automation@example.com
  TEST_USER_PASSWORD=YourSecureTestPassword123!
  ```

### B. Mandatory `.gitignore` Verification
Before creating or referencing any `.env` file, inspect the project's `.gitignore`. If git is used and the `.env` file or auth tokens are not ignored, append them immediately:

```gitignore
# Authentication & Test Secrets
.env
.env.*
!.env.example
!.env.test.example
playwright/.auth/
test-results/
```

---

## 3. Playwright `storageState`: Log In Once, Reuse Everywhere

Logging in through the UI on every single test is slow and causes flakiness. Instead, use Playwright's native **Project Dependencies & `storageState`** architecture.

### How It Works
1. A single **`auth.setup.ts`** runs before any tests.
2. It logs in via the UI using `.env` credentials, saves cookies and local storage tokens to `playwright/.auth/user.json`.
3. All subsequent test suites automatically start with pre-authenticated browser contexts, bypassing the login form entirely!

### Playwright Config (`playwright.config.ts`)
```typescript
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

// Load test environment variables
dotenv.config({ path: path.resolve(__dirname, '.env.test') });

export default defineConfig({
  projects: [
    // 1. Setup project: logs in and saves storageState
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    // 2. Main test projects depend on setup
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use saved storage state
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'mobile-iphone',
      use: {
        ...devices['iPhone 14'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### Setup Spec (`tests/auth.setup.ts`)
```typescript
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate user session', async ({ page }) => {
  const email = process.env.TEST_USER_EMAIL;
  const password = process.env.TEST_USER_PASSWORD;
  const baseUrl = process.env.BASE_URL || 'http://localhost:3000';

  if (!email || !password) {
    throw new Error('Missing TEST_USER_EMAIL or TEST_USER_PASSWORD in .env.test');
  }

  await page.goto(`${baseUrl}/login`);
  await page.getByLabel(/email/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /sign in|log in/i }).click();

  // Wait for redirect away from login page confirming success
  await page.waitForURL(url => !url.pathname.includes('/login'));

  // Save authenticated cookies & storage to disk
  await page.context().storageState({ path: authFile });
});
```

---

## 4. Testing Multi-Role Authentication

If the UI behaves differently for different user roles (e.g. `Admin` vs. `Customer`), save multiple storage states:
* `playwright/.auth/admin.json`
* `playwright/.auth/customer.json`

Assign the appropriate `storageState` to specific test files or projects.
