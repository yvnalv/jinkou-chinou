import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

// Load credentials and environment variables from .env.test (or .env)
dotenv.config({ path: path.resolve(__dirname, '.env.test') });

/**
 * Production-ready Playwright Configuration Starter for UI/UX Testing.
 * Includes:
 *   - Authentication setup with storageState reuse
 *   - Multi-device viewports (desktop, tablet, mobile)
 *   - Visual regression tolerances & animation freezing
 *   - Diagnostic trace & screenshot capture on failure
 */
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01, // 1% pixel diff allowance for font anti-aliasing
      threshold: 0.2,          // Pixel color difference threshold
      animations: 'disabled',  // Automatically freeze CSS animations/transitions
    },
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Optional: Authentication setup project (uncomment if testing behind login)
    // {
    //   name: 'setup',
    //   testMatch: /.*\.setup\.ts/,
    // },
    {
      name: 'desktop-chrome',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 800 },
        // storageState: 'playwright/.auth/user.json', // Enable when using auth setup
      },
      // dependencies: ['setup'], // Enable when using auth setup
    },
    {
      name: 'desktop-firefox',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      name: 'tablet-safari',
      use: {
        ...devices['iPad Pro 11'],
        viewport: { width: 768, height: 1024 },
      },
    },
    {
      name: 'mobile-iphone',
      use: {
        ...devices['iPhone 14'],
        viewport: { width: 390, height: 844 },
      },
    },
    {
      name: 'mobile-android',
      use: {
        ...devices['Pixel 7'],
        viewport: { width: 360, height: 800 },
      },
    },
  ],
});
