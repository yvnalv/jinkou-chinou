# Visual Design

Craft rules for layout, typography, color, iconography, imagery, and motion, plus how to create a distinctive visual direction instead of a generic one.

## Contents

1. Visual direction (avoid generic AI aesthetics)
2. Hierarchy and layout
3. Spacing
4. Typography
5. Color
6. Dark mode
7. Iconography and imagery
8. Motion
9. Review checklist

---

## 1. Visual direction

When an existing brand or design system exists, **follow it**; distinctiveness then comes from craft, not novelty. When there is none, set a deliberate direction before drawing screens.

AI-generated interfaces converge on the same safe look: default system or Inter-style type, purple-to-blue gradients on white, evenly spread timid palettes, rounded cards everywhere, emoji as icons, and the same hero-plus-three-cards layout. Avoid that sameness:

1. **Derive the direction from the brief:** audience, product personality (for example calm and clinical, playful, premium, technical, editorial), and context of use. Write three to five adjectives and one sentence of intent.
2. **Offer two contrasting directions** for new products, each with a type pairing, palette, shape language (radius, borders), density, imagery style, and motion character, plus a mini sample screen. Let the user choose.
3. **Typography carries identity:** pick typefaces with character that suit the personality, and pair with contrast (a display face with a neutral text face, serif with sans, sans with mono). Use real size jumps for hierarchy (display sizes can be 2.5–4× body size), not timid 1.2× steps everywhere.
4. **Commit to a palette:** one or two dominant colors with sharp accents beat evenly spread pastel sets. Define it as tokens and use it consistently.
5. **Atmosphere:** backgrounds can have depth (subtle gradients, texture, patterns, layered surfaces) where the product personality supports it; plain surfaces are fine for dense tools.
6. **Be context-appropriate:** a banking dashboard and a festival site should not look alike. Novel visuals never override usability, platform conventions, or accessibility.

Use only fonts, icons, and images with licenses that allow the use (SIL Open Font License and similar, Google Fonts, Material Symbols, Lucide, Phosphor, or the client's licensed assets). Never imitate another company's brand identity.

## 2. Hierarchy and layout

* **One primary action per screen or section**; secondary actions are visually quieter; destructive actions are distinct and never the default.
* **Hierarchy through size, weight, color, spacing, and position**, in that order of strength. If everything is bold, nothing is.
* **Scanning patterns:** F-pattern for text-heavy and list pages, Z-pattern for sparse landing layouts; put key information top and left for left-to-right languages (mirror for right-to-left).
* **Gestalt:** proximity groups related items (more space between groups than within them); alignment creates order; similarity signals same function; enclosure (cards, panels) only when grouping by space is not enough.
* **Grids:** 12 columns on large screens, 8 on tablets, 4 on phones, with consistent gutters from the spacing scale. Let content, not device names, decide breakpoints.
* **Line length:** 45–75 characters for running text (`max-width` around 60–70ch).
* **Density** is a deliberate choice: comfortable for consumer and occasional use, compact for expert and data-heavy tools (optionally user-selectable).

## 3. Spacing

* Use a **4px base scale** (4, 8, 12, 16, 24, 32, 48, 64 …) from tokens only; no one-off values.
* Space inside a component is smaller than space between components; space between sections is larger still.
* Consistent padding in all components of the same type (all cards, all table cells).

## 4. Typography

| Aspect | Guideline |
|---|---|
| Base size | 16px for body text on the web (never below 14px for UI text; 12px only for rare metadata) |
| Scale | Modular scale (for example 1.25 major third, or 1.333 perfect fourth for more drama), defined as tokens |
| Line height | 1.4–1.6 for body text, 1.1–1.3 for headings |
| Weights | Two or three weights per family; avoid faux bold and faux italic |
| Numbers | Tabular figures in tables and dashboards (`font-variant-numeric: tabular-nums`) |
| Case | Sentence case for UI labels and headings (easier to read and translate) |
| Loading | `font-display: swap`, subset where possible, a metric-compatible fallback stack, and at most two or three font files on the critical path |
| Localization | Check the chosen fonts cover every target script (for example Latin extended, Cyrillic, Arabic, CJK) |

## 5. Color

* **Roles, not raw colors:** define semantic tokens (background canvas/surface/subtle, text default/muted/accent, border default/strong, action primary/hover/on-primary, focus, feedback danger/success/warning/info) that point to palette primitives.
* **OKLCH for building scales:** equal lightness steps look equally different, which makes accessible scales predictable. Provide sRGB hex fallbacks.
* **Contrast** (WCAG 2.2): 4.5:1 for text, 3:1 for large text, and 3:1 for UI boundaries, focus indicators, and meaningful graphics. Check every semantic pair in both themes with `scripts/design_tokens.py contrast`.
* **Status colors** always come with an icon or text; red and green alone fail for many color-blind users.
* **Brand colors that fail contrast** get an accessible variant for text and small UI (keep the original for large areas and decoration).
* **Charts:** a categorical palette of distinguishable hues, ordered consistently; sequential and diverging palettes for magnitude; test with color-blindness simulation.

## 6. Dark mode

* Design it as a theme with its own semantic token values, not an inverted light theme.
* Use dark grays (not pure black) for large surfaces; show elevation with lighter surfaces rather than shadows.
* Desaturate and lighten accent colors; saturated colors vibrate on dark backgrounds.
* Recheck every contrast pair; muted text is where dark themes usually fail.
* Respect the OS preference (`prefers-color-scheme`) and let users override it; remember the choice.

## 7. Iconography and imagery

* One icon family, one stroke weight, one size grid (16, 20, 24px). Icons without text need an accessible name and should be universally understood (search, close, menu). Otherwise add a label.
* Never use emoji as UI icons.
* Images: purposeful and relevant (not generic stock), consistent in style, with aspect ratios reserved (`width`/`height` or `aspect-ratio`) to prevent layout shift, and responsive sources (`srcset`, modern formats).
* Illustrations and empty-state art match the visual direction and never carry information that is not also in text.

## 8. Motion

| Use | Duration | Easing |
|---|---|---|
| Micro-interactions (hover, press, toggle) | 100–150ms | Standard |
| Small transitions (menus, tooltips, expanding panels) | 150–250ms | Decelerate on enter, accelerate on exit |
| Large transitions (page, modal, sheet) | 250–400ms | Emphasized |

* Motion explains change (where something came from, what caused it); it is never decoration that delays the user.
* One orchestrated entrance beats many scattered animations.
* Animate `transform` and `opacity` only, for smooth performance.
* Always provide a `prefers-reduced-motion` alternative (instant or fade), and never flash.

## 9. Review checklist

- [ ] The direction fits the brief and is described in words the user agreed to.
- [ ] Every value (color, space, type, radius, shadow, duration) comes from tokens.
- [ ] Clear primary action and hierarchy on every screen; a squint test shows the right emphasis.
- [ ] Type scale, line length, and line height are within the ranges above.
- [ ] All contrast pairs pass in both themes.
- [ ] Icons are consistent and named; no emoji icons; images have reserved space.
- [ ] Motion has purpose and a reduced-motion alternative.
- [ ] Fonts, icons, and images are licensed for the use.
