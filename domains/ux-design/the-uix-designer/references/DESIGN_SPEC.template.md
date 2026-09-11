# Design Spec — <feature or flow>

Hand-off document for developers. The prototype shows how it looks; this spec says how it behaves.

| | |
|---|---|
| Prototype | <path to design/prototype/…html or Figma link> |
| Requirements | <UX-001, UX-002 … from UX_BRIEF.md> |
| Platforms | <web breakpoints / iOS / Android / desktop> |
| Design system | <tokens file, component library, version> |
| Status | <Draft / Ready for build> |

## 1. Summary

<What the user can do after this ships, in two or three sentences.>

## 2. Screens

| Screen | Purpose | Primary action | Entry points | Exit points |
|---|---|---|---|---|
| <name> | <purpose> | <action> | <from> | <to> |

## 3. States per Screen

| Screen | Default | Loading | Empty | Error | Other (offline, permission, overflow) |
|---|---|---|---|---|---|
| <name> | <description or screenshot ref> | <skeleton / spinner> | <message + action> | <message + recovery> | <…> |

## 4. Interactions and Behavior

| Element | Trigger | Result | Notes |
|---|---|---|---|
| <button, row, field> | <click, keyboard, gesture, timer> | <what happens, including focus and URL changes> | <validation, optimistic update, undo> |

## 5. Responsive and Platform Behavior

| Width / platform | Layout changes |
|---|---|
| ≥ 1024px | <…> |
| 640–1023px | <…> |
| < 640px | <…> |
| iOS / Android specifics | <navigation pattern, gestures, sheets> |

## 6. Content

| Location | Text | Notes |
|---|---|---|
| <button, heading, empty state, error> | <exact copy> | <max length, pluralization, variables> |

Glossary: <term = definition>.

## 7. Accessibility

- Landmarks and heading outline: <h1 …, h2 …>
- Focus order and focus management: <where focus goes after actions, dialogs, route changes>
- Keyboard: <shortcuts, arrow-key widgets and their ARIA pattern>
- Announcements: <status messages via role="status" / aria-live>
- Names for icon-only controls: <list>
- Reduced motion behavior: <…>
- Contrast: <all pairs checked with design_tokens.py; results>

## 8. Tokens and Components

| Component | Variant / size | Tokens | New or existing |
|---|---|---|---|
| <Button> | <primary / md> | <color.action.primary, space.4> | <existing> |

New tokens or components (need design-system approval): <list, with reason>.

## 9. Analytics and Success Measurement

<Events to track, tied to the brief's metrics.>

## 10. Open Questions

- <question — owner>

## 11. Verification

- [ ] `audit_html.py` on the prototype: <result>
- [ ] Contrast check: <result>
- [ ] Screenshots reviewed at <widths> in <themes>: <location>
- [ ] Keyboard pass: <done / not possible here>
- [ ] Not verified: <screen readers, real devices, …>
