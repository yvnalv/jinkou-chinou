# UI/UX Test Plan: [Application / Feature Name]

**Document Version:** 1.0.0  
**Target Environment:** [e.g. Staging / Local Dev / Production]  
**Primary Engine:** Playwright [or Selenium]  
**Author:** AI Quality Assurance Engineer (`/ui-ux-testing`)  
**Date:** [YYYY-MM-DD]  

---

## 1. Executive Summary & Objectives
* **Feature Scope:** [Brief description of the screens, user journeys, or components under test]
* **Test Goals:**
  * Verify end-to-end user journeys using user-centric locators (`getByRole`).
  * Enforce visual regression baselines across desktop, tablet, and mobile viewports.
  * Audit accessibility compliance against WCAG 2.1 & 2.2 Level A/AA using `axe-core`.
  * Validate UX states (loading skeletons, empty states, error toasts, offline recovery).

---

## 2. Test Architecture & Environment Matrix

### A. Viewport & Device Matrix
| Tier | Viewport (W x H) | Device Emulation | Browsers |
|---|---|---|---|
| Desktop | `1280 x 800` | Standard Desktop | Chromium, Firefox, WebKit |
| Tablet | `768 x 1024` | iPad Pro 11 | WebKit |
| Mobile Phone | `390 x 844` | iPhone 14 | Mobile Safari (WebKit) |
| Compact Android | `360 x 800` | Pixel 7 | Mobile Chrome (Chromium) |

### B. Anti-Flakiness Rules
* **Auto-Waiting**: Rely exclusively on web-first assertions (`expect(locator).toBeVisible()`). Zero `sleep()` delays.
* **Animation Freezing**: Apply global CSS rule disabling animations and transitions during visual checks.
* **Dynamic Masking**: Mask live timestamps, randomized IDs, and live avatar images.

---

## 3. Critical User Journeys (E2E)

### Journey 1: [e.g. Checkout Flow with Coupon Code]
* **Preconditions:** [e.g. User logged in, 1 item in cart]
* **Steps:**
  1. Navigate to `/cart` and verify line items.
  2. Input coupon code `SAVE20` and click "Apply".
  3. Verify discount line item updates immediately with accessible text.
  4. Proceed to `/checkout`, fill shipping info, and submit.
* **Expected Assertions:**
  * Order confirmation badge rendered.
  * Order number generated and visible.

---

## 4. Visual Regression Snapshot Targets

| Snapshot ID | Target Element / Page | Viewports | Masked Selectors | Max Diff Ratio |
|---|---|---|---|:---:|
| `checkout-initial` | Full page (`fullPage: true`) | Desktop, Mobile | `.live-timestamp` | `0.01` (1%) |
| `order-summary-card` | Container `[data-testid="order-summary"]` | Desktop, Tablet | None | `0.005` (0.5%) |

---

## 5. Accessibility (a11y) Audit Plan

* **Standard Tags**: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`.
* **State Checkpoints**:
  1. Initial page load.
  2. Address selection modal open (verify focus trap and escape key).
  3. Inline validation error trigger (verify `aria-describedby` and color contrast).

---

## 6. Deliverables & Execution Commands
* Test Specs: `tests/e2e/[feature].spec.ts`
* Page Objects: `tests/e2e/pages/[Feature]Page.ts`
* Run Command: `npx playwright test tests/e2e/[feature].spec.ts`
* Update Snapshots: `npx playwright test tests/e2e/[feature].spec.ts --update-snapshots`
