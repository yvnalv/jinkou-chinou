# Component — <Name>

| | |
|---|---|
| Status | <Proposed / Stable / Deprecated> |
| Code | <path to component> |
| Figma | <link, if any> |
| ARIA pattern | <e.g. Disclosure, Tabs, Dialog (Modal), Combobox — or "native element"> |

## Purpose

<What it is for.> **Don't use it for:** <cases, and which component to use instead>.

## Anatomy

<Named parts: container, label, icon, helper text, …>

## Variants and Sizes

| Variant | Use when |
|---|---|
| <primary> | <the main action of a view> |

| Size | Height | Use when |
|---|---|---|
| <md> | <44px / token> | <default> |

## States

| State | Visual | Behavior |
|---|---|---|
| Default | | |
| Hover | | |
| Focus-visible | <ring token, offset> | |
| Active / pressed | | |
| Disabled | <how it looks, and why it is disabled is explained nearby> | Not focusable / focusable with aria-disabled |
| Loading | | <announces, prevents double action> |
| Error / invalid | | |
| Selected / checked | | |

## Behavior

- Keyboard: <Tab, Enter, Space, arrows, Esc, Home/End>
- Pointer and touch: <target size, gestures>
- Responsive: <how it adapts>
- Overflow: <truncation, wrapping, max lines, tooltip for full text>

## Accessibility

- Role: <native element or role>
- Accessible name from: <visible label / aria-label / aria-labelledby>
- States exposed: <aria-expanded, aria-pressed, aria-invalid, …>
- Focus management: <…>
- Announcements: <…>

## Content Guidelines

<Label length, capitalization, verb-first for actions, examples.>

## Tokens

| Property | Token |
|---|---|
| Background | <color.action.primary> |
| Text | <color.action.on-primary> |
| Padding | <space.5> |
| Radius | <radius.md> |

## API

| Prop / slot / event | Type | Default | Description |
|---|---|---|---|
| <variant> | <"primary" \| "secondary"> | <"primary"> | |

## Do and Don't

- **Do:** <…>
- **Don't:** <…>

## Changelog

- <version — change>
