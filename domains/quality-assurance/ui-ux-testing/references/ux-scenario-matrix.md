# The Comprehensive UX Scenario Matrix

Automated UI/UX testing must go far beyond happy-path clicks. This matrix defines the comprehensive set of user states, edge cases, and failure modes every robust UI suite must verify.

---

## 1. The Core UX State Matrix

Every key view or interactive component must be tested across the 6 UX States:

```text
1. Loading / Skeleton State   --> Are skeletons visible? Are buttons disabled to prevent double-submit?
2. Empty State                 --> Clear illustration, helpful explanation, actionable CTA present?
3. Partial / Default State     --> Standard populated view with clean visual hierarchy.
4. Error State (Inline/Toast)  --> Clear message, non-technical explanation, retry action available.
5. Success / Completed State   --> Positive confirmation, status badge, next-step guidance.
6. Offline / Degraded State    --> Graceful warning banner, no unhandled blank white screen.
```

---

## 2. Concrete Test Patterns for UX Scenarios

### A. Preventing Double-Submission & Button Disabling
Users frequently double-click buttons when responses take time. Automated tests must verify the action button is disabled immediately upon clicking:

```typescript
test('submit button disables immediately to prevent double-charging', async ({ page }) => {
  await page.route('**/api/v1/charge', async route => {
    // Artificial 1 second delay
    await new Promise(r => setTimeout(r, 1000));
    await route.fulfill({ status: 200, body: JSON.stringify({ ok: true }) });
  });

  const payButton = page.getByRole('button', { name: 'Pay $49.00' });
  await payButton.click();

  // Button must be disabled immediately while pending
  await expect(payButton).toBeDisabled();
  // Spinner or loading indicator must be present
  await expect(page.getByTestId('spinner')).toBeVisible();

  // Once completed, navigates or displays success
  await expect(page.getByRole('heading', { name: 'Payment Confirmed' })).toBeVisible();
});
```

### B. Empty State Verification
When a user searches for non-existent items or views an empty dashboard, verify the empty state CTA:
```typescript
test('displays friendly empty state with action when search yields no items', async ({ page }) => {
  await page.goto('/products');
  await page.getByPlaceholder('Search products...').fill('non-existent-xyz-product-999');
  await page.keyboard.press('Enter');

  // Verify empty state container
  const emptyState = page.getByTestId('empty-state');
  await expect(emptyState).toBeVisible();
  await expect(emptyState.getByRole('heading')).toHaveText(/no products found/i);
  await expect(emptyState.getByText(/try checking for spelling errors/i)).toBeVisible();

  // Verify clear filters CTA works
  const clearBtn = emptyState.getByRole('button', { name: 'Clear Filters' });
  await expect(clearBtn).toBeVisible();
  await clearBtn.click();
  await expect(page.getByRole('listitem').first()).toBeVisible();
});
```

### C. Network Loss & Offline Recovery
Verify the application does not crash when the network drops:
```typescript
test('warns user when network connectivity is lost', async ({ page, context }) => {
  await page.goto('/document/edit/123');
  await expect(page.getByRole('textbox')).toBeVisible();

  // Simulate going offline
  await context.setOffline(true);

  // Trigger auto-save or action
  await page.getByRole('textbox').fill('Updated offline notes');

  // Offline banner must appear
  await expect(page.getByRole('status')).toHaveText(/you are currently offline/i);

  // Restore connection
  await context.setOffline(false);
  await expect(page.getByRole('status')).toHaveText(/changes saved/i);
});
```

### D. Form Validation & Edge Case Inputs
Test forms against messy user inputs:
* **Trailing Whitespace**: Does the email input auto-trim `' user@domain.com '`?
* **Pasted Content with Line Breaks**: Does pasting into a single-line input strip newlines?
* **Maximum Length**: Does typing 500 characters in a 100-character field truncate or display a clean counter?
* **XSS / Special Characters**: Does submitting `<script>alert(1)</script>` or `Robert'); DROP TABLE Users;--` render as plain escaped text without breaking layout or executing?

```typescript
test('handles edge-case input values gracefully', async ({ page }) => {
  await page.goto('/contact');
  const nameInput = page.getByLabel('Your Name');

  // Test special characters & HTML entities
  const messyName = '<script> & "quotes" & accents: éàç';
  await nameInput.fill(messyName);
  await page.getByRole('button', { name: 'Submit' }).click();

  // Ensure output is safely rendered as text
  await expect(page.getByTestId('submitted-name')).toHaveText(messyName);
});
```

### E. Session Timeout & Auth Redirection
Verify that expired auth tokens preserve user context:
```typescript
test('redirects expired session to login and preserves return URL', async ({ page }) => {
  await page.route('**/api/v1/user/profile', route => {
    route.fulfill({ status: 401, body: JSON.stringify({ error: 'Unauthorized' }) });
  });

  await page.goto('/settings/security');

  // Must redirect to login with redirect query param
  await expect(page).toHaveURL(/\/login\?redirect=%2Fsettings%2Fsecurity/);
  await expect(page.getByRole('alert')).toHaveText(/session has expired/i);
});
```
