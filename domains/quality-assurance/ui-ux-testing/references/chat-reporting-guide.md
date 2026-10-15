# Chat Reporting Guide & Standard Output Formatting

Whenever `/ui-ux-testing` executes tests, evaluates results, or completes a mode, it must format its response in the chat using this consistent, structured, table-driven layout.

---

## 1. Standard Chat Response Structure

Every chat report consists of 6 structured sections:

```text
1. Header & Executive Verdict (Target, Engine, Viewports, Overall Status Badge)
2. Execution Metrics Table (Summary of Functional, Visual, a11y, and Responsive checks)
3. Visual Regression Diffs (Table of changed snapshots, tolerances, and diff ratios)
4. Accessibility Violations (Grouped by Critical, Serious, Moderate, Minor with fix hints)
5. UX State & Responsive Checks (Overflow checks, double-submit, empty states)
6. Next Actions & Artifact Confirmation Prompt
```

---

## 2. Example Chat Output Template

### 🎯 Test Run Summary: [Application / Feature Name]

* **Target URL / Scope**: `https://staging.example.com/checkout` (or local dev server)
* **Testing Engine**: Playwright (`@playwright/test` v1.48+ / Chromium, Firefox, WebKit)
* **Viewports Tested**: Desktop (`1280x800`), Tablet (`768x1024`), Mobile (`390x844`)
* **Execution Time**: `14.2s`
* **Overall Verdict**: **`PASS WITH A11Y WARNINGS`** (or `PASSED` / `FAILED - REGRESSION DETECTED`)

---

### 📊 Execution Metrics

| Test Category | Suite / Flow | Total | Passed | Failed | Flaky | Duration | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Functional E2E** | Cart & Checkout Journey | 8 | 8 | 0 | 0 | 5.1s | ✅ PASS |
| **Visual Regression** | Multi-Viewport Snapshot Matrix | 6 | 5 | 1 | 0 | 4.3s | ❌ DIFF |
| **Accessibility (a11y)** | Axe-core WCAG 2.1/2.2 AA | 4 scans | 3 clean | 1 | 0 | 2.6s | ⚠️ WARN |
| **Responsive & UX** | Overflow, Touch Targets, Double-Click | 5 | 5 | 0 | 0 | 2.2s | ✅ PASS |
| **Total** | | **23** | **21** | **2** | **0** | **14.2s** | **ACTION REQ** |

---

### 🖼️ Visual Regression Diffs

| Snapshot File | Viewport | Max Diff Allowed | Actual Diff | Masked Selectors | Result |
|---|---|:---:|:---:|---|:---:|
| `checkout-hero-desktop.png` | `1280x800` | `1.0%` | `0.00%` | `.live-timestamp` | ✅ Match |
| `order-summary-mobile.png` | `390x844` | `1.0%` | **`2.45%`** | `None` | ❌ Unmatched |

> **Visual Diff Diagnosis**: On `390x844`, the coupon code input wrapped below the "Apply" button, causing a 24px vertical shift in the order summary card.

---

### ♿ Accessibility (a11y) Violations

| Severity | Rule ID | Target Selector | WCAG Criterion | Recommended Remediation |
|---|---|---|---|---|
| **Serious** | `color-contrast` | `button.btn-secondary` | WCAG 1.4.3 (Contrast Min) | Increase text contrast from 3.2:1 to at least 4.5:1 (change `#888` to `#595959`). |
| **Moderate** | `link-name` | `a.footer-social-icon` | WCAG 2.4.4 (Link Purpose) | Add `aria-label="Visit our Twitter profile"` to the icon-only anchor. |

---

### 📱 Responsive & UX Edge Cases

* [x] **Horizontal Scrollbar Check**: Zero unwanted horizontal overflow on mobile (`390px` and `360px`).
* [x] **Double-Click Prevention**: Place Order button successfully disables on click during pending API request.
* [x] **Empty State**: Cart empty state renders illustration, helpful message, and "Start Shopping" CTA.
* [x] **Touch Targets**: All interactive mobile buttons exceed minimum size `44x44px`.

---

## 3. Mandatory File Placement Confirmation Rule

> [!IMPORTANT]
> **Always ask the user where to save the generated test report `.md` file BEFORE writing it to disk.**
> Never write `.md` reports silently to arbitrary locations.

When completing a test run or test plan, provide the proposed default file path and prompt the user:

> *"I have prepared the complete Markdown test report with detailed assertion logs, visual diff breakdowns, and Axe-core JSON violations.*
>
> *Where would you like me to save the dedicated report file?*
> *(Recommended default: `tests/reports/ui_ux_test_report.md` or `docs/testing/UI_UX_TEST_REPORT.md`)*"
