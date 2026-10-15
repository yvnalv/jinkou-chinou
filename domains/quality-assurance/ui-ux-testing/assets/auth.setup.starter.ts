import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

/**
 * Authentication Setup Script
 * Executes once before test projects run, performs UI sign-in using .env credentials,
 * and saves authentication cookies/tokens to `playwright/.auth/user.json`.
 */
setup('authenticate test user', async ({ page }) => {
  const email = process.env.TEST_USER_EMAIL;
  const password = process.env.TEST_USER_PASSWORD;
  const baseUrl = process.env.BASE_URL || 'http://localhost:3000';

  if (!email || !password) {
    throw new Error(
      'Authentication credentials missing! Please configure TEST_USER_EMAIL and TEST_USER_PASSWORD in your .env.test file.'
    );
  }

  await page.goto(`${baseUrl}/login`);

  // Resilient locators for login inputs
  await page.getByLabel(/email|username/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /sign in|log in|submit/i }).click();

  // Verify successful login by waiting for redirect away from auth page
  await page.waitForURL(url => !url.pathname.includes('/login') && !url.pathname.includes('/signin'));

  // Save session state to disk for reuse across all tests
  await page.context().storageState({ path: authFile });
});
