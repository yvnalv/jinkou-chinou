# Platforms

Platform-specific guidance for web, iOS, Android, desktop, and dashboards. Platform design systems evolve every year: facts marked with a year were verified on 2026-09-11. Check the official guideline (Apple Human Interface Guidelines, Material Design, Fluent 2) before relying on version-specific details.

## Contents

1. Web (responsive)
2. iOS and iPadOS
3. Android
4. Desktop applications
5. Dashboards and data-dense apps
6. Cross-platform products

---

## 1. Web (responsive)

* **Mobile-first CSS**, with breakpoints set where the content breaks (typical ranges: under 640px, 640–1024px, over 1024px). Use **container queries** for components that live in different widths.
* **Fluid type and space** with `clamp()` within limits; never shrink body text below 16px on phones.
* **Input modes:** design for touch, mouse, keyboard, and pen. Use `@media (hover: hover)` and `(pointer: coarse)` rather than guessing by width; no hover-only functionality.
* **Viewport:** `<meta name="viewport" content="width=device-width, initial-scale=1">`, never blocking zoom; handle safe areas (`env(safe-area-inset-*)`) and the mobile browser's dynamic toolbars (`dvh` units).
* **Performance is UX** (Core Web Vitals, "good" thresholds): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1. Reserve space for images and embeds, lazy-load below the fold, keep JavaScript lean, and show skeletons rather than shifting layouts.
* **Progressive enhancement:** core content and actions work before JavaScript finishes; forms are real forms.
* **Browser features worth using:** `<dialog>`, the Popover API, `:focus-visible`, `:has()`, `color-scheme`, `prefers-reduced-motion`, `prefers-color-scheme`, and `forced-colors`. Check support against the project's browser targets.

## 2. iOS and iPadOS

* Follow the **Human Interface Guidelines** and use native SwiftUI or UIKit components wherever possible; they carry platform behavior, accessibility, and future visual updates.
* **Liquid Glass (2025 design language, iOS 26 and later):** translucent material reserved for the navigation and control layer floating above content (tab bars, toolbars, sheets). Let system components apply it; don't stack glass on glass; keep content legible on solid layers; respect Reduce Transparency and Increase Contrast.
* **Navigation:** tab bar for top-level sections (three to five), navigation stack with a back button for hierarchy, sheets for focused tasks, and sidebars on iPad.
* **Targets** at least 44 × 44 pt; **Dynamic Type** supported at all sizes including accessibility sizes; the SF system font unless the brand requires otherwise.
* **Safe areas**, the Dynamic Island, and the home indicator must never hide content or controls.
* **Gestures** follow platform conventions (swipe back from the edge, pull to refresh, swipe actions in lists) and always have visible alternatives.
* **System integration:** share sheet, haptics used sparingly and meaningfully, permission prompts with a pre-explanation of why.

## 3. Android

* Follow **Material Design 3**. **Material 3 Expressive** (introduced 2025) extends it with emphasized typography, shape morphing, motion physics, and new or refreshed components (button groups, split buttons, toolbars, loading indicators, FAB menus). Use Jetpack Compose Material 3 components.
* **Adaptive layouts by window size class** (compact, medium, expanded and larger): navigation bar on compact, navigation rail on medium, navigation drawer or rail on expanded; list-detail and supporting-pane layouts on large screens and foldables.
* **Targets** at least 48 × 48 dp; text in `sp` so it scales (up to 200%); edge-to-edge drawing with correct insets.
* **Dynamic color** (from the wallpaper) can theme the app, but the brand and meaning must survive it; semantic colors (error) stay fixed.
* **Predictive back** gesture support; system back always behaves predictably.
* **Material symbols** and motion tokens for consistency with the platform.

## 4. Desktop applications

* Respect the host platform: **Fluent 2** on Windows, the **macOS Human Interface Guidelines** on Mac. Cross-platform shells (Electron, Tauri, Flutter desktop) should still use native menus, shortcuts, and window behavior.
* **Keyboard first:** full keyboard navigation, discoverable shortcuts (shown in menus and tooltips), standard shortcuts (Ctrl/Cmd+S, Z, F, comma for settings), and a command palette for power users.
* **Menus:** menu bar on macOS and in classic Windows apps; context menus on right-click matching the visible actions.
* **Windows:** resizable with sensible minimum sizes, remembered size and position, multi-window support where it helps, and high-DPI and multi-monitor support.
* **Density:** higher than mobile, with compact controls (but targets still at least 24px), hover states, tooltips with shortcut hints, and multi-select with Shift and Ctrl/Cmd.
* **Drag and drop** with clear drop targets and keyboard alternatives.
* **System features:** follow the OS light/dark theme and accent color, native notifications, file dialogs, and accessibility APIs (UI Automation on Windows, NSAccessibility on macOS).

## 5. Dashboards and data-dense apps

Start from the decisions the dashboard supports, not from the available data.

* **Define the audience and question first:** executive (monitor a few KPIs, lots of white space), operational (spot and act on exceptions, high density), or analytical (explore, filter, drill down).
* **Layout:** the most important KPIs top-left; group related metrics; progressive disclosure from overview to detail to record. Five to nine primary elements per view.
* **KPI cards:** value, unit, comparison (versus target or previous period, with direction and whether up is good), time range, and a sparkline if trend matters.
* **Chart choice:** line for trends over time, bar for comparing categories, stacked bar for part-to-whole over few categories, scatter for relationships, heatmap for two-dimensional density, and tables when exact values matter. Avoid pie charts with more than three slices, 3D, and dual axes.
* **Honest charts:** bar axes start at zero, consistent scales across compared charts, labelled units and time zones, annotated anomalies, and visible data freshness ("Updated 5 min ago").
* **Color:** neutral by default; reserve strong color for status and highlights; categorical palettes that are distinguishable for color-blind users; the same series keeps the same color everywhere.
* **Tables:** sticky headers, frozen first column, right-aligned tabular numbers, sort and filter, column choice, density toggle, and export.
* **Filters and time ranges** are global and visible, persist in the URL, and show their effect.
* **States:** loading per widget (don't block the whole page), no data, partial data, stale data, errors per widget, and permission-limited data.
* **Accessibility for charts:** text summaries of key insights, data available as a table, patterns or direct labels in addition to color, and keyboard access to tooltips.

## 6. Cross-platform products

* Share **the design language** (tokens, voice, iconography, information architecture), not identical screens.
* Adapt **components and navigation** to each platform's conventions; users trust what feels native.
* Keep **core flows and terminology** identical across platforms so people can switch devices.
* Tokens with platform transforms (for example with Style Dictionary) keep web, iOS, Android, and Flutter in sync.
