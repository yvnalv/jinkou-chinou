# Responsive Viewport Matrix & Mobile Emulation

Responsive UI/UX testing verifies that applications function smoothly, maintain visual appeal, and prevent layout breakage across screen sizes and input modalities.

---

## 1. Standard Viewport Tier Matrix

Test suites must cover these 5 core breakpoint tiers:

| Tier | Device Representative | Viewport (W x H) | User Agent / Features | Playwright Preset |
|---|---|---|---|---|
| **Large Desktop** | Standard 1080p Monitor | `1440 x 900` | Mouse, hover enabled | `Desktop Chrome` |
| **Standard Desktop** | Laptop Screen | `1280 x 800` | Mouse, hover enabled | `Desktop Firefox` |
| **Tablet Portrait** | iPad Pro / Air | `768 x 1024` | Touch enabled, `hasTouch: true` | `iPad Pro 11` |
| **Modern Phone** | iPhone 14 / 15 / 16 | `390 x 844` | Mobile Safari, DPR 3, Touch | `iPhone 14` |
| **Compact Phone** | Android (Pixel / Galaxy) | `360 x 800` | Mobile Chrome, DPR 2.6, Touch | `Pixel 7` |

---

## 2. Automated Detection of Responsive Layout Deficiencies

### A. Horizontal Overflow Detection (No Unwanted Scrollbars)
One of the most frequent mobile UX bugs is unintended horizontal overflow caused by fixed-width containers or unconstrained images.

```typescript
test('page has no horizontal overflow on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');

  const hasHorizontalScrollbar = await page.evaluate(() => {
    return document.documentElement.scrollWidth > window.innerWidth;
  });

  expect(hasHorizontalScrollbar).toBe(false);
});
```

### B. Hamburger Navigation vs. Desktop Navbar
Verify responsive components transform cleanly between mobile and desktop:

```typescript
test('nav transforms from desktop links to mobile drawer at 768px breakpoint', async ({ page }) => {
  // 1. Desktop Check
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('/');
  await expect(page.getByRole('navigation').getByRole('link', { name: 'Pricing' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Open Menu' })).toBeHidden();

  // 2. Mobile Check
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.getByRole('navigation').getByRole('link', { name: 'Pricing' })).toBeHidden();
  const hamburgerBtn = page.getByRole('button', { name: 'Open Menu' });
  await expect(hamburgerBtn).toBeVisible();

  // Open drawer
  await hamburgerBtn.click();
  await expect(page.getByRole('dialog', { name: 'Navigation Menu' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Pricing' })).toBeVisible();
});
```

### C. Minimum Touch Target Sizing (WCAG 2.5.8 - Target Size Minimum)
Interactive mobile elements (buttons, links, checkboxes) must be at least `24x24px` (WCAG AA) and ideally `44x44px` (Apple HIG / Android Material):

```typescript
test('interactive controls meet minimum touch target size on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/checkout');

  const buttons = page.getByRole('button');
  const count = await buttons.count();

  for (let i = 0; i < count; i++) {
    const btn = buttons.nth(i);
    if (await btn.isVisible()) {
      const box = await btn.boundingBox();
      if (box) {
        expect(box.width).toBeGreaterThanOrEqual(24);
        expect(box.height).toBeGreaterThanOrEqual(24);
      }
    }
  }
});
```

---

## 3. Emulating Touch & Hover Modes

Mobile devices do not have true hover states (`:hover`). Hover-dependent navigation patterns (e.g. drop-down menus opening only on mouse hover) fail on touchscreens.

In `playwright.config.ts`, device presets automatically configure touch emulation:
```typescript
use: {
  hasTouch: true, // Emulates touch events (touchstart, touchend)
  isMobile: true, // Enables mobile browser behaviors
}
```
In test scripts:
```typescript
// Simulates touchscreen tap
await page.getByRole('button', { name: 'Actions' }).tap();
```
