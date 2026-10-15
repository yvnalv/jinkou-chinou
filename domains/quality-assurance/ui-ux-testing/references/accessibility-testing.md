# Automated Accessibility (a11y) Testing with Axe-Core and Playwright

Automated accessibility testing scans the rendered DOM in real browser runtime to catch WCAG compliance defects before they reach production.

---

## 1. Setup & Core Integration

Playwright integrates natively with Deque's industry-standard `axe-core` via `@axe-core/playwright` (TypeScript/JavaScript) and `axe-core-python` (Python).

### Installation
```bash
# TypeScript / JavaScript
npm install --save-dev @axe-core/playwright

# Python
pip install axe-core-python
```

### Basic Audit Spec (TypeScript)
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Compliance (WCAG 2.1/2.2 AA)', () => {
  test('landing page contains no detectable a11y violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
```

---

## 2. Interactive State Auditing (The Core Rule)

**Never test only static initial page loads.** Over 60% of real-world accessibility bugs occur *after* user interaction—when dialogs open, error toasts trigger, or dropdowns expand.

### Pattern: Audit After Every Major State Transition
```typescript
test('modal dialog maintains accessibility compliance when open', async ({ page }) => {
  await page.goto('/settings');

  // Trigger modal
  await page.getByRole('button', { name: 'Delete Account' }).click();
  const dialog = page.getByRole('dialog', { name: 'Confirm Deletion' });
  await expect(dialog).toBeVisible();

  // Audit specifically within the open dialog container
  const modalA11y = await new AxeBuilder({ page })
    .include('div[role="dialog"]')
    .analyze();

  expect(modalA11y.violations).toEqual([]);
});

test('form validation errors meet WCAG standards', async ({ page }) => {
  await page.goto('/signup');

  // Submit empty form to trigger validation errors
  await page.getByRole('button', { name: 'Create Account' }).click();
  await expect(page.getByText('Email is required')).toBeVisible();

  // Audit error state
  const errorA11y = await new AxeBuilder({ page })
    .include('form#signup-form')
    .analyze();

  expect(errorA11y.violations).toEqual([]);
});
```

---

## 3. Scoping & Handling Third-Party Widgets

If third-party widgets (e.g. Google Maps, Chatbots, embedded YouTube iframes) contain third-party accessibility issues out of your team's control, scope the scan or exclude the third-party container:

```typescript
const results = await new AxeBuilder({ page })
  .include('#main-content')
  .exclude('.embedded-intercom-chat')
  .exclude('#cookie-banner-vendor')
  .analyze();
```

---

## 4. Keyboard Navigation & Focus Trapping

Automated tools like `axe-core` catch static DOM defects (color contrast, missing labels, duplicate IDs, missing ARIA). However, interactive keyboard flows must be asserted explicitly in your test suite:

### A. Focus Trapping in Modals
When a modal opens, keyboard `Tab` must cycle exclusively within the modal and never leak to the background page:
```typescript
test('modal traps keyboard focus', async ({ page }) => {
  await page.goto('/dashboard');
  await page.getByRole('button', { name: 'Open Filter' }).click();

  const modal = page.getByRole('dialog');
  await expect(modal).toBeVisible();

  // Verify initial focus is inside modal
  await expect(modal.getByRole('button', { name: 'Close' })).toBeFocused();

  // Press Tab through all modal controls
  await page.keyboard.press('Tab');
  await expect(modal.getByLabel('Category')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(modal.getByRole('button', { name: 'Apply Filters' })).toBeFocused();

  // Tabbing past the last control must loop back to the first control
  await page.keyboard.press('Tab');
  await expect(modal.getByRole('button', { name: 'Close' })).toBeFocused();

  // Escape key must dismiss dialog and return focus to triggering element
  await page.keyboard.press('Escape');
  await expect(modal).toBeHidden();
  await expect(page.getByRole('button', { name: 'Open Filter' })).toBeFocused();
});
```

### B. Skip Link Verification
Every page must provide a functional "Skip to main content" link for keyboard users:
```typescript
test('skip link bypasses navigation', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');

  const skipLink = page.getByRole('link', { name: /skip to (main )?content/i });
  await expect(skipLink).toBeFocused();

  await page.keyboard.press('Enter');
  await expect(page.locator('main')).toBeFocused();
});
```

---

## 5. Violation Severity Tiers & Remediation Format

Group Axe-core violations into 4 severity tiers:

| Severity | Impact on User | Example Defect | Fix Requirement |
|---|---|---|---|
| **Critical** | Blocks screen reader users completely | Missing `alt` on image link, untrapped modal focus, broken ARIA role | Block CI build immediately |
| **Serious** | Significant barrier; user may fail task | Form input without `<label>` or `aria-label`, duplicate `id` | Block CI build immediately |
| **Moderate** | Causes confusion or difficulty | Contrast ratio below 4.5:1 on body text, skipped heading levels (`h1` to `h3`) | Fix in sprint backlog |
| **Minor** | Subtle annoyance or warning | Missing landmark region, redundant title attribute | Fix in hygiene cycle |

---

## 6. Attaching Detailed a11y Reports to Playwright Test Artifacts

When an accessibility test fails in CI, print a clean summary and attach the raw JSON payload to the test report:

```typescript
test('accessible checkout flow', async ({ page }, testInfo) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page }).analyze();

  if (results.violations.length > 0) {
    // Attach JSON report for debugging
    await testInfo.attach('axe-violations.json', {
      body: JSON.stringify(results.violations, null, 2),
      contentType: 'application/json',
    });
  }

  expect(results.violations).toEqual([]);
});
```
