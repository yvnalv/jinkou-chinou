# Interaction Patterns

Proven patterns for the parts of an interface that most often go wrong, plus UX writing, AI features, and dark patterns to refuse.

## Contents

1. The state matrix
2. Forms
3. Navigation and wayfinding
4. Tables, lists, search, and filters
5. Feedback: loading, notifications, errors
6. Dialogs, sheets, and destructive actions
7. Onboarding and empty states
8. UX writing
9. AI features
10. Dark patterns (never design these)

---

## 1. The state matrix

Design every state a screen or component can be in. Missing states are the most common gap between a mockup and a shippable UI.

| State | Questions |
|---|---|
| Default / ideal | Realistic content, not the happy best case only |
| Loading | Skeleton for layout-stable content, spinner only for short unknown waits, progress for long known work; keep the layout from jumping |
| Empty (first use) | Explain what goes here and give the first action |
| Empty (no results) | Say nothing matched, show the query and active filters, offer to clear or broaden |
| Partial / sparse | One item, very few items |
| Overflow | Long names, 10,000 rows, long translations (German and Finnish can be 30–40% longer), large numbers, many tags |
| Error | What happened, whether data is safe, and what to do next; keep user input |
| Offline / slow | What still works, what is queued, how sync is shown |
| Permission / role | Hidden versus disabled versus explained ("Only admins can …") |
| Success / confirmation | Visible, specific, and non-blocking where possible |
| Interaction states | Hover, focus-visible, active/pressed, selected, disabled, read-only, dragging |

## 2. Forms

* **Ask less:** remove, defer, or infer every field you can. Each field costs completion.
* **One column**, fields in a logical order, related fields grouped with `fieldset` and `legend`.
* **Labels above fields**, always visible; help text between label and field; mark optional fields (or required ones, consistently) in text, not only with an asterisk color.
* **Right input types and attributes:** `type="email|tel|url|number|date"`, `inputmode`, `autocomplete` (1.3.5), and sensible `maxlength`. Don't use number inputs for IDs, card numbers, or postal codes.
* **Field width hints at expected length** (short for postal code, wide for address).
* **Validation:** validate on blur or submit, not on every keystroke (except for helpful live checks like password rules). On submit, show an error summary at the top linked to each field, move focus to it, and mark fields with `aria-invalid` plus a text message linked by `aria-describedby`.
* **Error messages** say what is wrong and how to fix it: "Enter a date after 1 January 2026", not "Invalid input".
* **Never clear the form** on error. Preserve input across navigation and sessions for long forms.
* **Buttons** say what they do ("Create account", "Pay $42.00"), not "Submit". Disable a submit button only with a visible reason; prefer allowing submit and showing errors.
* **Long forms:** a multi-step flow with progress ("Step 2 of 4"), a review step before commit (3.3.4), and save-and-continue-later.
* **Authentication:** allow paste and password managers, show-password toggles, passkeys or magic links, no security questions, no puzzle CAPTCHA without an alternative (3.3.8).

## 3. Navigation and wayfinding

* Users should always know **where they are** (current item highlighted with `aria-current`, page title, breadcrumbs for deep hierarchies), **where they can go**, and **how to get back**.
* Keep primary navigation to about seven or fewer top-level items; group the rest.
* Don't hide primary navigation behind a hamburger on large screens.
* Deep links work: every meaningful state (filters, tabs, selected item) has a URL on the web.
* Back behaves as users expect, including browser back in single-page apps and Android predictive back.
* Search is prominent when content is large or users know what they want.

## 4. Tables, lists, search, and filters

* **Tables:** left-align text, right-align numbers (tabular figures), consistent units in the header, sticky header for long tables, sortable columns with a visible sort indicator (`aria-sort`), row actions revealed consistently, selection with a clear count and bulk actions, and a responsive strategy (priority columns, horizontal scroll inside a labelled region, or rows turning into cards).
* **Pagination vs infinite scroll vs "load more":** pagination for goal-directed finding and comparing; "load more" for browsing with a reachable footer; infinite scroll only for feeds.
* **Filters:** show active filters as removable chips with a "clear all"; show result counts; apply instantly for few results, with an Apply button on mobile sheets or slow queries; never lose filters on back.
* **Search:** forgiving (typos, synonyms), suggestions while typing, recent searches, highlighted matches, and a helpful no-results state.

## 5. Feedback: loading, notifications, errors

| Response time | Feedback |
|---|---|
| Under 100ms | Feels instant; no indicator |
| 100ms – 1s | Subtle state change (button pressed, inline spinner) |
| 1 – 10s | Skeleton or spinner, with the action disabled against double-submits |
| Over 10s | Progress with an estimate, allow background work and cancel |

* **Optimistic UI** for low-risk actions (like, reorder), with rollback and a message on failure.
* **Notification hierarchy:** inline message (about a field or section) → toast (brief, non-critical, auto-dismissing only if there is no action and it stays long enough to read; announced with `role="status"`) → banner (persistent, page-level) → modal (only when the user must decide now).
* **Undo beats confirmation** for reversible actions ("Message deleted. Undo").
* **Errors** never blame the user, never expose stack traces or codes alone, and always offer a next step (retry, contact, go back).

## 6. Dialogs, sheets, and destructive actions

* Use a modal only for a focused task or a decision that blocks progress. Use native `<dialog>` or a proven accessible component: focus moves in, Tab is trapped inside, Esc closes, focus returns to the trigger, and the background is inert.
* Title the dialog with the question or task; buttons name the actions ("Delete project", "Keep project"), not "OK" and "Cancel".
* **Destructive actions:** explain consequences with specifics ("Deletes 14 files permanently"), make the destructive button visually distinct but not the default focus, and for high-impact deletes ask the user to type the name. Prefer soft delete with undo.
* On mobile, prefer bottom sheets for short choices and full-screen views for long tasks.

## 7. Onboarding and empty states

* Get users to first value fast; defer account creation and settings where possible.
* Teach in context (empty states, inline tips, sample data) rather than with multi-screen tours people skip.
* Empty states have three parts: what this area is for, why it is empty, and the primary action to fill it.

## 8. UX writing

* **Clear, concise, useful:** front-load the key word, use the users' vocabulary, and one idea per sentence.
* **Sentence case**, active voice, second person ("You can …"), and numerals ("3 items").
* **Consistent terms:** one name per concept across the product (not "project" here and "workspace" there). Keep a small glossary in the design spec.
* **Labels are verbs for actions, nouns for places.**
* **Plan for localization:** avoid concatenated strings, leave room for expansion, handle plurals and gender with ICU message format, and use locale-aware dates, numbers, currencies, and names. Support right-to-left layouts when needed.
* **Tone** follows the product personality, but never at the cost of clarity, and never jokes in error messages about lost money or data.

## 9. AI features

When the interface includes AI output or agents:

* **Set expectations:** say what the AI can and cannot do; label AI-generated content.
* **Show sources and confidence** where it matters, so users can verify.
* **Keep the human in control:** preview before applying, easy edit, undo, and explicit confirmation for consequential or irreversible actions (sending, purchasing, deleting).
* **Design for failure:** wrong answers, refusals, slow responses (stream and allow stop), and a clear way to recover or get human help.
* **Transparency about data:** what is used, stored, or shared; opt-outs where required.
* **Evaluate with many inputs,** not one impressive demo; variability is part of the design problem.

## 10. Dark patterns (never design these)

Refuse these even when asked; propose an honest alternative that meets the business goal. Several are illegal in some jurisdictions (for example under EU consumer and digital services rules and US FTC enforcement).

| Pattern | Example | Honest alternative |
|---|---|---|
| Confirmshaming | "No thanks, I don't like saving money" | Neutral decline text |
| Roach motel | Easy sign-up, cancellation only by phone | Cancel in the same channel and number of steps |
| Hidden costs / drip pricing | Fees revealed at the last step | Total price shown early |
| Sneak into basket / pre-checked add-ons | Insurance added by default | Unchecked opt-in |
| Forced continuity | Trial silently converts to paid | Reminder before charging, easy cancel |
| Fake urgency or scarcity | Fake countdowns, "only 2 left" when untrue | Real, verifiable information only |
| Disguised ads | Ads styled as content or download buttons | Clearly labelled sponsored content |
| Nagging | Repeated prompts after a "no" | Respect the choice, ask again rarely |
| Privacy zuckering / consent tricks | "Accept all" prominent, reject hidden | Equal prominence for accept and reject |
| Trick questions | Double negatives in opt-outs | Plain, positive wording |
| Obstruction | Making data export or account deletion hard | Self-service in settings |
