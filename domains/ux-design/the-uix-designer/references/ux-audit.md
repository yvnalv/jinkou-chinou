# UX and UI Audit Method

How to review an existing interface (Mode D) and produce `UX_AUDIT.md` from `references/UX_AUDIT.template.md`.

## Contents

1. Scope and inputs
2. The passes
3. Usability heuristics with concrete checks
4. Severity and priority
5. Evidence and writing findings
6. Definition of done

---

## 1. Scope and inputs

Agree first:

* **What:** which flows, screens, and platforms (for example "checkout on mobile web and iOS").
* **Against what:** usability heuristics, WCAG 2.2 AA, the product's design system, platform guidelines, and the stated user goals.
* **Inputs available:** live URL, local build, source code, screenshots, Figma files (with the connector), analytics, or support tickets.
* **Depth:** a quick scan (top issues in an hour's worth of review) or a full audit.

Walk the flows as a user with a concrete goal, not screen by screen in isolation.

## 2. The passes

| Pass | How | Tools |
|---|---|---|
| Heuristic evaluation | Walk each flow against the ten heuristics below | Screenshots, the live UI |
| Accessibility | WCAG 2.2 AA checklist in `references/accessibility.md`; automated then manual | `scripts/audit_html.py`, axe or Lighthouse if available, keyboard pass, zoom and reflow screenshots |
| Visual consistency | Tokens versus hard-coded values, component variants, spacing rhythm, type scale, iconography | grep the code, `scripts/design_tokens.py contrast` |
| Content | Clarity, terminology consistency, error messages, empty states, localization readiness | Read every string in the flow |
| Platform conventions | Navigation, gestures, controls, and back behavior as the platform expects | `references/platforms.md` |
| Performance perception | Layout shifts, slow feedback, missing loading states | Browser dev tools or Lighthouse if available |
| Ethics | Dark patterns, consent, cancellation, pricing transparency | `references/interaction-patterns.md` section 10 |

## 3. Usability heuristics with concrete checks

Jakob Nielsen's ten heuristics, turned into things you can check:

| # | Heuristic | Look for |
|---|---|---|
| H1 | Visibility of system status | Loading, saving, and progress feedback; current location; data freshness |
| H2 | Match with the real world | Users' language, familiar concepts, logical order, local formats for dates and money |
| H3 | User control and freedom | Undo, cancel, back, exit from flows, draft saving, easy dismissal |
| H4 | Consistency and standards | Same words and patterns for the same things; platform conventions |
| H5 | Error prevention | Constraints, good defaults, confirmation for destructive actions, inline validation |
| H6 | Recognition rather than recall | Visible options, recent items, examples in fields, no memorizing between screens |
| H7 | Flexibility and efficiency | Shortcuts, bulk actions, saved filters, sensible defaults for experts and novices |
| H8 | Aesthetic and minimalist design | Only relevant content; clear hierarchy; no noise competing with primary actions |
| H9 | Help users recognize, diagnose, and recover from errors | Plain-language errors with a cause and a fix; preserved input |
| H10 | Help and documentation | Contextual help where needed; searchable help; consistent help location (WCAG 3.2.6) |

## 4. Severity and priority

Severity (Nielsen's 0–4 scale, adapted):

| Severity | Meaning |
|---|---|
| 4 — Critical | Blocks a task, loses data or money, excludes users of assistive technology, or creates legal risk. Fix before release |
| 3 — Major | Causes frequent errors, abandonment, or significant delay. Fix soon |
| 2 — Minor | Causes friction or confusion but users recover. Schedule |
| 1 — Cosmetic | Polish; fix when touching the area |
| 0 — Not a problem | Noted disagreement or preference |

Any WCAG 2.2 Level A or AA failure on a core flow is at least Major; failures that block access entirely are Critical.

Priority combines severity with **frequency** (how many users and how often) and **effort** (quick win, medium, large). Present quick wins with high severity first.

## 5. Evidence and writing findings

Every finding needs:

* **ID** (`AUD-001`), **title**, **severity**, **heuristic or WCAG criterion**, and **location** (URL and screen, or `file:line`, or a Figma frame).
* **Evidence:** screenshot reference, selector, the exact text, or a measured value (for example "contrast 3.2:1, needs 4.5:1").
* **Impact:** who is affected and how.
* **Recommendation:** specific and actionable, ideally with the design-system token or component to use.

Also record **what works well**; it tells the team what to keep.

Be precise about confidence: separate what you observed from what you infer, and list the checks you could not perform (screen readers, real devices, analytics).

Do not fix anything during the audit unless the user asks. Offer a prioritized plan, and implement it afterwards in Mode B, C, or E.

## 6. Definition of done

* Scope, inputs, and standards are stated.
* All agreed passes are done or explicitly skipped with a reason.
* Every finding has evidence, severity, a criterion, and a recommendation.
* Findings are prioritized, with quick wins identified.
* Unverified areas are listed.
