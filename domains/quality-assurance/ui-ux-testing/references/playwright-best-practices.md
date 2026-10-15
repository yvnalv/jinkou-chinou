# Playwright Best Practices for UI/UX Testing

This reference guides the implementation of reliable, deterministic, and maintainable browser automation suites with Playwright (TypeScript/JavaScript and Python).

---

## 1. The Resilient Locator Ladder

Never locate elements by brittle CSS class hashes (`.css-19z2x3`), dynamic IDs (`#button-83921`), or absolute XPaths (`/html/body/div[2]/div/button`). Always climb the Resilient Locator Ladder:

```text
Level 1: Accessible Role & Name  --> page.getByRole('button', { name: 'Confirm Purchase' })
Level 2: Form Label               --> page.getByLabel('Work Email Address')
Level 3: Placeholder / Text       --> page.getByPlaceholder('Enter your password') / page.getByText('Success!')
Level 4: Explicit Test ID         --> page.getByTestId('order-summary-card')
Level 5: Semantic CSS (Last Resort)-> page.locator('article[data-status="active"]')
```

### Locator Rules
* **Prefer User-Facing Semantics**: Locators should reflect how assistive technology and real humans perceive the screen (`getByRole`, `getByLabel`). If a test fails because a button's accessible name changed, that is a legitimate UX regression.
* **Filter with Sub-Locators**: Scope searches to containers instead of writing complex chained CSS:
  ```typescript
  const cartItem = page.getByRole('listitem').filter({ hasText: 'Wireless Headphones' });
  await cartItem.getByRole('button', { name: 'Remove' }).click();
  ```
* **Avoid Chained `.first()` or `.nth()` Without Cause**: If multiple elements match, refine the parent scope or use explicit distinguishing labels rather than arbitrarily selecting the first element.

---

## 2. Web-First Auto-Waiting vs. Hardcoded Delays

**Hardcoded delays (`page.waitForTimeout(5000)`, `sleep(5)`) are strictly banned.** They cause flaky builds on slow CI machines and waste time on fast local runners.

### Auto-Waiting Primitives
Playwright automatically waits for an element to be actionable (visible, stable, enabled, editable, receiving events) before performing actions:
* `await locator.click()` waits for attached, visible, stable animations, enabled, and clickable.
* `await locator.fill('text')` waits for visible, enabled, and editable.

### Web-First Assertions
Always use web-first assertions with built-in polling:
```typescript
// CORRECT: Polls until the condition passes or timeout is reached (default 5s)
await expect(page.getByRole('alert')).toBeVisible();
await expect(page.getByTestId('cart-count')).toHaveText('3');
await expect(page.getByRole('button', { name: 'Submit' })).toBeDisabled();

// WRONG: Non-retrying synchronous assertion; race condition prone!
const isVisible = await page.getByRole('alert').isVisible();
expect(isVisible).toBe(true);
```

---

## 3. Page Object Model (POM) & Component Fixtures

Encapsulate DOM structure inside reusable Page Objects or Component Objects to ensure UI redesigns only require updates in a single file.

### Structure Example (TypeScript)
```typescript
import { type Page, type Locator, expect } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly shippingAddressInput: Locator;
  readonly placeOrderButton: Locator;
  readonly orderConfirmationAlert: Locator;

  constructor(page: Page) {
    this.page = page;
    this.shippingAddressInput = page.getByLabel('Shipping Address');
    this.placeOrderButton = page.getByRole('button', { name: 'Place Order' });
    this.orderConfirmationAlert = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/checkout');
    await expect(this.shippingAddressInput).toBeVisible();
  }

  async submitOrder(address: string) {
    await this.shippingAddressInput.fill(address);
    await this.placeOrderButton.click();
  }

  async expectOrderSuccessful() {
    await expect(this.orderConfirmationAlert).toContainText(/order placed successfully/i);
  }
}
```

---

## 4. Network Interception & State Mocking

UI/UX tests should test interface states (loading, error, edge cases) without relying on unreliable third-party backends or live payment gateways.

### Mocking API Responses with `page.route()`
```typescript
// Test 500 Server Error UI state
test('displays error toast when checkout API fails', async ({ page }) => {
  await page.route('**/api/v1/checkout', route => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Payment gateway timeout' }),
    });
  });

  const checkout = new CheckoutPage(page);
  await checkout.goto();
  await checkout.submitOrder('123 Main St');

  // Verify UI displays friendly error toast instead of crashing
  await expect(page.getByRole('alert')).toHaveText(/payment gateway timeout/i);
  await expect(page.getByRole('button', { name: 'Retry Payment' })).toBeVisible();
});
```

### Simulating Slow Connections / Loading Skeletons
```typescript
test('displays skeleton loader during slow data fetch', async ({ page }) => {
  await page.route('**/api/v1/products', async route => {
    await new Promise(resolve => setTimeout(resolve, 2000)); // Delay response
    await route.continue();
  });

  await page.goto('/catalog');
  await expect(page.getByTestId('product-skeleton-loader')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Featured Products' })).toBeVisible();
});
```

---

## 5. Artifacts and Debugging Flakiness

Configure Playwright to capture deep diagnostic artifacts automatically on failure:
* **Trace Viewer**: Contains DOM snapshots, action logs, network waterfalls, and console logs.
* **Screenshots on Failure**: Instant visual snapshot of the viewport at the exact moment of error.
* **Video on Failure**: Step-by-step recording of user interactions leading up to the failure.

In `playwright.config.ts`:
```typescript
use: {
  trace: 'retain-on-failure',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```
View captured traces using:
```bash
npx playwright show-trace test-results/failed-test/trace.zip
```
