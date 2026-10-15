# Visual Regression Testing with Playwright

Visual regression testing captures pixel-by-pixel screenshots of rendered pages or components and compares them against verified baseline images to detect unintended style shifts, broken layouts, or visual regressions.

---

## 1. Native Visual Comparisons

Playwright provides built-in visual assertions via `expect(page).toHaveScreenshot()` and `expect(locator).toHaveScreenshot()`.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Marketing Homepage Visual Integrity', () => {
  test('matches full desktop baseline snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Compare whole page
    await expect(page).toHaveScreenshot('homepage-desktop.png', {
      fullPage: true,
      maxDiffPixelRatio: 0.01, // 1% pixel diff allowance for anti-aliasing
    });
  });

  test('matches isolated pricing card component snapshot', async ({ page }) => {
    await page.goto('/pricing');
    const proTierCard = page.getByTestId('pricing-card-pro');

    // Compare isolated component
    await expect(proTierCard).toHaveScreenshot('pricing-card-pro.png');
  });
});
```

---

## 2. Eliminating Flakiness in Visual Tests

Visual tests are sensitive to sub-pixel rendering, font smoothing, and dynamic content. Follow these rules to keep visual tests deterministic.

### A. Freeze Animations, Transitions, and Carousels
CSS transitions, pulsing badges, and auto-advancing carousels cause intermittent screenshot diffs. Freeze them before taking snapshots:

```typescript
// Inject CSS to eliminate all animations and transitions
await page.addStyleTag({
  content: `
    *, *::before, *::after {
      transition: none !important;
      animation: none !important;
      caret-color: transparent !important;
    }
  `,
});
```
Or use Playwright's built-in `animations: 'disabled'` option:
```typescript
await expect(page).toHaveScreenshot('dashboard.png', {
  animations: 'disabled',
});
```

### B. Mask Volatile and Dynamic Elements
Always mask elements containing dynamic data (e.g. timestamps, live avatars, randomized banner ads, user IDs):

```typescript
await expect(page).toHaveScreenshot('user-profile.png', {
  mask: [
    page.getByTestId('live-timestamp'),
    page.getByTestId('user-avatar'),
    page.locator('.dynamic-advertisement'),
  ],
  maskColor: '#808080', // Renders solid gray box over dynamic elements
});
```

### C. Wait for Web Fonts and Images to Stabilize
Never take a snapshot before web fonts are loaded:
```typescript
await page.evaluate(async () => {
  await document.fonts.ready;
});
```
And ensure all images are decoded:
```typescript
await page.evaluate(async () => {
  const images = Array.from(document.querySelectorAll('img'));
  await Promise.all(
    images
      .filter(img => !img.complete)
      .map(img => new Promise(resolve => {
        img.onload = img.onerror = resolve;
      }))
  );
});
```

---

## 3. Tolerance Tuning (`threshold` vs. `maxDiffPixelRatio`)

Configure tolerance to absorb anti-aliasing variations without missing actual UI regressions:

```typescript
await expect(locator).toHaveScreenshot('button.png', {
  threshold: 0.2,          // Pixel color difference threshold (0.0 to 1.0; 0.2 is default)
  maxDiffPixels: 50,       // Max acceptable number of different pixels
  maxDiffPixelRatio: 0.01, // Max acceptable percentage of changed pixels (1%)
});
```

* **`threshold`**: Controls how different an individual pixel's color can be before it is considered changed (RGB color distance).
* **`maxDiffPixelRatio`**: Controls what fraction of the total screenshot pixels can be different before the test fails. Set to `0.01` (1%) or `0.005` (0.5%) for robust cross-environment testing.

---

## 4. Multi-Viewport Snapshot Matrix

Visual regression tests should run across standard device profiles:

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'desktop-chrome',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } },
    },
    {
      name: 'tablet-safari',
      use: { ...devices['iPad Pro 11'], viewport: { width: 768, height: 1024 } },
    },
    {
      name: 'mobile-iphone',
      use: { ...devices['iPhone 14'], viewport: { width: 390, height: 844 } },
    },
  ],
});
```
Playwright automatically stores snapshots in platform- and browser-specific directories:
```text
tests/e2e/homepage.spec.ts-snapshots/
├── homepage-desktop-chrome-win32.png
├── homepage-tablet-safari-win32.png
└── homepage-mobile-iphone-win32.png
```

---

## 5. Baseline Lifecycle & CI Management

1. **Initial Baseline Generation**: When creating a new test, running `npx playwright test` generates baseline screenshots if none exist.
2. **Reviewing Changes**: When UI changes are intentional, view the generated visual diff in the HTML report:
   ```bash
   npx playwright show-report
   ```
3. **Updating Baselines**: Update baseline snapshots in Git when changes are approved:
   ```bash
   npx playwright test --update-snapshots
   ```
4. **CI Consistency**: Because OS font rendering varies (Windows ClearType vs. Linux FreeType vs. macOS Quartz), run visual regression tests inside a standardized Docker container matching the CI runner environment (`mcr.microsoft.com/playwright`).
