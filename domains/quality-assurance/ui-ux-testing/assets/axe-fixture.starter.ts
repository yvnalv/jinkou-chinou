import { test as base } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Custom Playwright test fixture extending base test with a pre-configured AxeBuilder.
 * Audits against WCAG 2.1 & 2.2 Level A/AA standards.
 */
type AxeFixture = {
  makeAxeBuilder: () => AxeBuilder;
};

export const test = base.extend<AxeFixture>({
  makeAxeBuilder: async ({ page }, use) => {
    const makeAxeBuilder = () =>
      new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']);
    await use(makeAxeBuilder);
  },
});

export { expect } from '@playwright/test';
