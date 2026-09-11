# Accessibility

Accessibility is the baseline of every design and build in this skill, not a feature. Target **WCAG 2.2 Level AA** unless the user sets a stricter bar.

Facts in section 5 were verified on 2026-09-11. Laws and standards change: re-check official sources before stating a deadline or legal requirement, and never present this as legal advice.

## Contents

1. Design-time rules
2. WCAG 2.2 AA checklist
3. Native apps
4. Testing method
5. Standards and legal landscape
6. ARIA rules

---

## 1. Design-time rules

These prevent most failures before any audit:

* **Contrast:** body text 4.5:1; large text (≥ 24px regular or ≥ 18.66px bold) 3:1; UI component boundaries, focus indicators, and meaningful graphics 3:1 against adjacent colors. Check token pairs with `scripts/design_tokens.py contrast`.
* **Never color alone:** pair color with text, an icon, a pattern, or position (errors, status badges, chart series, required fields).
* **Visible focus on everything interactive**, at least as clear as a 2px outline with 3:1 contrast, and never hidden under sticky headers, cookie banners, or chat widgets (2.4.11).
* **Targets at least 24 × 24 CSS px** (2.5.8), or spaced so a 24px circle around each does not overlap another. Design for 44 × 44 pt (iOS) and 48 × 48 dp (Android) on touch.
* **Every input has a visible label** (placeholder is not a label), help text before the field, and errors that say what went wrong and how to fix it, linked with `aria-describedby`.
* **Structure is semantic:** one `h1`, headings in order, landmarks (`header`, `nav`, `main`, `footer`), lists as lists, data tables with header cells.
* **Reflow:** works at 320 CSS px wide and at 400% zoom without two-dimensional scrolling (except for data tables, maps, and diagrams).
* **Motion:** respect `prefers-reduced-motion`; nothing flashes more than three times per second; auto-moving content can be paused.
* **Alternatives:** meaningful images get alt text that serves the same purpose; decorative ones get `alt=""`; video gets captions; audio gets transcripts.
* **No cognitive tests to log in** (3.3.8): allow password managers and paste, offer passkeys, magic links, or OAuth; no puzzle CAPTCHAs without an alternative.
* **Don't make people re-enter** information they already gave in the same process (3.3.7).
* **Consistent help** (3.2.6): contact or help links in the same place on every page.
* **Dragging has a single-pointer alternative** (2.5.7): reorder with buttons or menus, sliders with input fields.

## 2. WCAG 2.2 AA checklist

Level A and AA success criteria, grouped for review. The criterion number goes in every audit finding.

**Perceivable**

| SC | Check |
|---|---|
| 1.1.1 Non-text Content | Images, icons, and controls have text alternatives; decorative images are hidden from assistive technology |
| 1.2.1–1.2.5 Time-based Media | Captions for video (prerecorded and live), transcripts for audio, audio description for video |
| 1.3.1 Info and Relationships | Headings, lists, tables, labels, and groups are in the markup, not only visual |
| 1.3.2 Meaningful Sequence | DOM order matches reading order |
| 1.3.3 Sensory Characteristics | Instructions don't rely only on shape, position, or sound ("click the round button on the right") |
| 1.3.4 Orientation | Works in portrait and landscape |
| 1.3.5 Identify Input Purpose | Personal-data fields have `autocomplete` values |
| 1.4.1 Use of Color | Color is not the only way information is conveyed |
| 1.4.2 Audio Control | Auto-playing audio over 3 seconds can be stopped |
| 1.4.3 Contrast (Minimum) | 4.5:1 text, 3:1 large text |
| 1.4.4 Resize Text | Text scales to 200% without loss of content or function |
| 1.4.5 Images of Text | Real text instead of text baked into images |
| 1.4.10 Reflow | No horizontal scrolling at 320 CSS px |
| 1.4.11 Non-text Contrast | 3:1 for component boundaries, states, focus rings, and informative graphics |
| 1.4.12 Text Spacing | Layout survives line-height 1.5, paragraph spacing 2×, letter spacing 0.12em, word spacing 0.16em |
| 1.4.13 Content on Hover or Focus | Tooltips and popovers are dismissible (Esc), hoverable, and persistent |

**Operable**

| SC | Check |
|---|---|
| 2.1.1 Keyboard | Everything works with the keyboard alone |
| 2.1.2 No Keyboard Trap | Focus can always move away (modals trap on purpose but close with Esc) |
| 2.1.4 Character Key Shortcuts | Single-key shortcuts can be turned off or remapped |
| 2.2.1 Timing Adjustable | Time limits can be extended or turned off (session timeout warnings) |
| 2.2.2 Pause, Stop, Hide | Carousels, tickers, and animations over 5 seconds can be paused |
| 2.3.1 Three Flashes | No flashing more than three times per second |
| 2.4.1 Bypass Blocks | Skip link or landmarks |
| 2.4.2 Page Titled | Unique, descriptive titles (and route changes update the title in single-page apps) |
| 2.4.3 Focus Order | Logical order; focus moves into dialogs and returns to the trigger afterwards |
| 2.4.4 Link Purpose (In Context) | Link text says where it goes |
| 2.4.5 Multiple Ways | Search, sitemap, or navigation to reach pages |
| 2.4.6 Headings and Labels | Descriptive headings and labels |
| 2.4.7 Focus Visible | Always a visible focus indicator |
| 2.4.11 Focus Not Obscured (Minimum) | A focused element is not entirely hidden by author content |
| 2.5.1 Pointer Gestures | Multi-point or path gestures have single-pointer alternatives |
| 2.5.2 Pointer Cancellation | Actions fire on up-event, or can be aborted |
| 2.5.3 Label in Name | The accessible name contains the visible label text |
| 2.5.4 Motion Actuation | Shake or tilt actions have alternatives and can be turned off |
| 2.5.7 Dragging Movements | Dragging has a single-pointer alternative |
| 2.5.8 Target Size (Minimum) | 24 × 24 CSS px, or enough spacing |

**Understandable**

| SC | Check |
|---|---|
| 3.1.1 / 3.1.2 Language | `lang` on the page and on passages in other languages |
| 3.2.1 / 3.2.2 On Focus / On Input | Focus or input alone does not trigger a change of context |
| 3.2.3 / 3.2.4 Consistency | Same navigation order and same names for the same functions |
| 3.2.6 Consistent Help | Help mechanisms in a consistent place |
| 3.3.1 Error Identification | Errors are identified in text |
| 3.3.2 Labels or Instructions | Labels and required formats are given up front |
| 3.3.3 Error Suggestion | Errors suggest a fix when one is known |
| 3.3.4 Error Prevention | Legal, financial, or data-changing submissions can be reviewed, corrected, or reversed |
| 3.3.7 Redundant Entry | Previously entered information is auto-filled or selectable |
| 3.3.8 Accessible Authentication (Minimum) | No cognitive function test without an alternative or assistance |

**Robust**

| SC | Check |
|---|---|
| 4.1.2 Name, Role, Value | Custom controls expose name, role, and state (expanded, selected, checked) |
| 4.1.3 Status Messages | Status updates (saved, 3 results, error) are announced without moving focus (`role="status"`, `aria-live`) |

(4.1.1 Parsing was removed in WCAG 2.2.)

## 3. Native apps

WCAG applies to app content through EN 301 549 and WCAG2ICT, plus platform expectations:

| Topic | iOS | Android |
|---|---|---|
| Screen reader | VoiceOver: set `accessibilityLabel`, traits, and hints; logical element order | TalkBack: `contentDescription`, `Modifier.semantics`, headings, merged descendants |
| Text scaling | Dynamic Type through all sizes, including accessibility sizes; layouts reflow | Font scaling up to 200%; use `sp` for text; nothing clipped or truncated |
| Targets | 44 × 44 pt | 48 × 48 dp |
| Motion and transparency | Respect Reduce Motion, Reduce Transparency, and Increase Contrast (important with Liquid Glass) | Respect "Remove animations"; test high-contrast text |
| Color | Support Dark Mode and Increase Contrast | Support dark theme; don't depend on dynamic color for meaning |

## 4. Testing method

Automated tools find only a minority of real barriers; a pass is never proof of accessibility.

1. **Automated:** `scripts/audit_html.py` for static markup, then axe-core (browser extension, `@axe-core/playwright`, `jest-axe`) or Lighthouse on the rendered page.
2. **Keyboard-only pass:** Tab, Shift+Tab, Enter, Space, arrows, and Esc through every flow. Check focus order, visibility, traps, and what happens after dialogs close.
3. **Zoom and reflow:** 200% text zoom, 400% page zoom, 320px width (`scripts/screenshot.py --widths 320`), and the text-spacing overrides from 1.4.12.
4. **Screen reader smoke test:** NVDA with Chrome or Firefox on Windows, VoiceOver with Safari on macOS or iOS, and TalkBack on Android. Check names, roles, states, headings, and live announcements for the main flow.
5. **Preferences:** dark mode, reduced motion, Windows forced colors (high contrast), and a color-blindness simulation for charts and status colors.
6. **Record** what you could not test (for example no screen reader in this environment) and list it as unverified.

## 5. Standards and legal landscape (verified 2026-09-11)

| Standard or law | Status |
|---|---|
| WCAG 2.2 | W3C Recommendation since October 2023; the current target |
| WCAG 3.0 | Working Draft (latest March 2026); final Recommendation not expected before 2028. Do not use it, or its APCA contrast method, as a compliance measure. APCA can be a secondary readability hint only |
| European Accessibility Act | Enforceable since 28 June 2025 for many consumer products and services sold in the EU (e-commerce, banking, transport, e-books, telecoms, and more), including by non-EU companies. Existing services have transition periods until 2030 |
| EN 301 549 | The harmonised technical standard. v3.2.1 is based on WCAG 2.1 AA. v4.1.1 (published 2 September 2026) references WCAG 2.2 AA; it gives presumption of conformity once cited in the EU Official Journal, expected around late 2026 |
| US ADA Title II (state and local government) | WCAG 2.1 AA required. In April 2026 the DOJ extended the deadlines to 26 April 2027 (population of 50,000 or more) and 26 April 2028 (smaller entities) |
| US ADA Title III (private businesses) | No technical regulation, but lawsuits and settlements use WCAG 2.1 or 2.2 AA as the yardstick |
| US Section 508 | Federal ICT; WCAG 2.0 AA through the 2017 refresh |

Other jurisdictions (UK public sector regulations, Canada, Australia, Japan, Indonesia, and others) have their own rules. Ask where the product is sold or used, and check official sources.

## 6. ARIA rules

1. **Use native HTML first.** `<button>`, `<a href>`, `<input>`, `<select>`, `<details>`, and `<dialog>` come with keyboard support and semantics for free.
2. **Don't change native semantics** (`<h2 role="button">`); wrap or restructure instead.
3. **Every custom interactive control must be keyboard operable** and follow the ARIA Authoring Practices pattern for its role (tabs, menu, combobox, disclosure, dialog, listbox).
4. **Don't hide focusable elements** with `aria-hidden="true"`; use `inert` for inactive regions.
5. **Every interactive element needs an accessible name.**
6. **State must be exposed:** `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`, `aria-current`, `aria-invalid`.
7. **Live regions exist before content is injected into them**; keep announcements short and polite unless urgent.

No ARIA is better than bad ARIA: incorrect roles make things worse than plain markup.
