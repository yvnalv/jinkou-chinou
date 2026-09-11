# Design Systems

How to create, extend, and implement a design system: tokens, components, documentation, and code (Mode C).

## Contents

1. Inventory before inventing
2. Design tokens (DTCG 2025.10)
3. Components
4. Implementing in code
5. Governance and change
6. Definition of done

---

## 1. Inventory before inventing

In an existing product, never design a system from scratch before you know what exists:

1. **Find the sources:** token files, theme config (Tailwind config, CSS custom properties, SCSS variables, `Theme.kt`, asset catalogs), component libraries (shadcn/ui, MUI, Radix, Material, SwiftUI views), Storybook, Figma libraries (with the Figma connector: `get_variable_defs`, `search_design_system`).
2. **Measure real usage:** grep the code for hard-coded colors, font sizes, spacing, radii, and z-indexes. Count distinct values; 40 grays usually means 6 are needed.
3. **List components and their variants,** noting duplicates (three button implementations) and inconsistencies.
4. **Record accessibility failures** in existing patterns; do not copy them into the system.
5. Propose a consolidation plan (keep, merge, deprecate) before changing anything.

## 2. Design tokens (DTCG 2025.10)

The W3C Design Tokens Community Group format reached its first stable version, **2025.10**, in October 2025. Style Dictionary v4 and Figma Variables exports support it. Use it as the source of truth and generate platform code from it.

**Structure:**

```json
{
  "color": {
    "$type": "color",
    "palette": {
      "blue": {
        "600": { "$value": { "colorSpace": "srgb", "components": [0.145, 0.388, 0.922], "hex": "#2563eb" } }
      }
    },
    "action": {
      "primary": { "$value": "{color.palette.blue.600}", "$description": "Primary buttons and links" }
    }
  },
  "space": {
    "$type": "dimension",
    "4": { "$value": { "value": 1, "unit": "rem" } }
  }
}
```

* A **token** has `$value`; a **group** does not. `$type` is inherited from the closest group.
* **Aliases** use `{group.token}`; property-level references use `{"$ref": "#/json/pointer"}`. No circular references.
* Names must not start with `$` or contain `{`, `}`, or `.`.
* **Types:** color (object with `colorSpace`, `components`, optional `alpha` and `hex`), dimension (`{"value", "unit"}` with px or rem), duration (ms or s), fontFamily, fontWeight, number, cubicBezier, strokeStyle, and composites (border, transition, shadow, gradient, typography).
* **Themes and modes** (light/dark, brands, density): keep the base file plus override files that change only semantic tokens (the DTCG Resolver Module formalizes this). `scripts/design_tokens.py css base.json --dark dark.json` emits both.

**Three tiers:**

| Tier | Example | Rule |
|---|---|---|
| Primitive (palette) | `color.palette.blue.600`, `space.4` | Raw values; never used directly in components |
| Semantic | `color.text.default`, `color.action.primary`, `color.feedback.danger-text` | Meaning; the layer themes override |
| Component (optional) | `button.primary.background` | Only when a component needs to diverge from semantics |

**Naming:** category → property → variant → state (`color.action.primary-hover`). Name by role, not by value (`text.muted`, not `gray-600`).

**Validation loop:**

```text
python <skill-dir>/scripts/design_tokens.py validate tokens/base.tokens.json tokens/dark.tokens.json
python <skill-dir>/scripts/design_tokens.py contrast --tokens tokens/base.tokens.json --fg "color.text.*" --bg "color.bg.*"
python <skill-dir>/scripts/design_tokens.py contrast --tokens tokens/base.tokens.json tokens/dark.tokens.json --fg "color.text.*" --bg "color.bg.*"
python <skill-dir>/scripts/design_tokens.py css tokens/base.tokens.json --dark tokens/dark.tokens.json --out src/styles/tokens.css
```

Also check the pairs that are not text on background: `on-primary` on `action.primary`, feedback text on feedback backgrounds, `border.strong` and `focus` against surfaces (`--target 3`).

`assets/tokens.starter.json` and `assets/tokens.starter.dark.json` are a complete starting set that passes these checks; replace the palette and typefaces with the product's direction.

## 3. Components

Specify each component with `references/COMPONENT_SPEC.template.md`:

* **Purpose and when not to use it** (point to the alternative).
* **Anatomy:** named parts.
* **Variants** (primary, secondary, ghost, danger) and **sizes**, only as many as real use needs.
* **States:** default, hover, focus-visible, active, disabled, loading, selected, error, read-only.
* **Behavior:** keyboard interaction (following the ARIA Authoring Practices pattern), responsive behavior, and overflow and truncation rules.
* **Accessibility:** role, accessible name source, states exposed, focus management.
* **Content guidelines:** label length, capitalization, and tone.
* **Tokens used**, and the code API (props, slots, events).
* **Do and don't** examples.

Build order that pays off first: foundations (tokens, type, icons) → primitives (button, link, input, select, checkbox, radio, switch) → feedback (alert, toast, badge, spinner, skeleton) → containers (card, dialog, sheet, tabs, accordion, popover, tooltip) → navigation (nav bar, sidebar, breadcrumbs, pagination) → data (table, list, empty state) → patterns (forms, filters, search).

## 4. Implementing in code

Follow the project's existing stack and conventions. Inspect before writing:

| Stack | Tokens land in | Notes |
|---|---|---|
| Plain CSS or any framework | CSS custom properties (`tokens.css`) | Output of `design_tokens.py css`; themes via `prefers-color-scheme` and `[data-theme]` |
| Tailwind CSS | Theme variables mapped to the CSS custom properties (for Tailwind v4, the `@theme` directive; for v3, `tailwind.config`) | Check the installed major version before editing |
| React component libraries (shadcn/ui, Radix, MUI) | The library's theme or CSS variables | Extend the library's components; don't fork them |
| iOS (SwiftUI) | Asset catalog colors plus a `Theme` type | Generated with Style Dictionary or hand-mapped from tokens |
| Android (Compose) | `MaterialTheme` color scheme, typography, shapes | Map semantic tokens to Material roles |
| Flutter | `ThemeData` and `ThemeExtension` | |

Engineering rules when changing product code:

* Inspect the codebase first: existing components, styling approach, folder structure, lint rules, and tests.
* Reuse and extend existing components; do not add a new UI library or a parallel styling system without explicit approval.
* Replace hard-coded values with tokens as you touch code, but do not refactor unrelated screens unasked.
* Build accessibility into the component (semantics, keyboard, focus, ARIA state), then prove it: the project's unit tests, plus `jest-axe` or `@axe-core/playwright` if available, plus a keyboard pass.
* Show every state: Storybook stories when the project uses Storybook, otherwise a demo page.
* Run the project's own build, lint, type-check, and tests until they pass. Never skip, delete, or weaken tests to get green.

## 5. Governance and change

* **Single source of truth:** tokens in the repository; Figma variables and code are generated from, or synced with, them.
* **Versioning:** semantic versioning for the system; breaking changes (renamed tokens, removed variants) get a migration note and a deprecation period (`$deprecated` in tokens).
* **Contribution:** a new component or variant needs a demonstrated need in at least two places, a spec, accessibility review, and documentation.
* **Documentation lives next to code** (README or Storybook docs), with usage guidance, not only prop tables.

## 6. Definition of done

* Tokens validate, all declared pairs pass contrast in every theme, and CSS or platform output is generated, not hand-edited.
* Each new or changed component has a spec, every state implemented, keyboard and screen-reader semantics, and a story or demo.
* The project build, lint, and tests pass; accessibility checks ran and their results are reported.
* The inventory, decisions, and any deprecations are documented.
