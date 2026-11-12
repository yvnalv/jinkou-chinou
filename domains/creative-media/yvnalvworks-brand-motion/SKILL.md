---
name: yvnalvworks-brand-motion
description: "yvnalvworks (@yvnalvworks / yvnalvworks.com) specialized brand motion skill extending the-motion-designer. Applies yvnalvworks' signature technical aesthetic: Matte Charcoal #121212 canvas, Warm Ivory Cream #F0ECE2 text, Electric Lime #C1FF72 punchline highlights, Lucide 2px monoline SVG vector icons, Inter typography, and locked Y=1480px captions. Use when creating content for yvnalvworks or invoking /yvnalvworks-brand-motion."
metadata:
  version: 0.1.0
---

# yvnalvworks Brand Motion: Visual Identity and Canvas Engine

Specialized brand motion and visual design skill extending **`the-motion-designer`** exclusively for **yvnalvworks (Yovan Alvianto : yvnalvworks.com / `@yvnalvworks`)**.

This skill isolates all yvnalvworks visual guidelines, typography, color tokens, Lucide monoline vectors, Remotion canvases, and automated 4:5 carousel slide renderers so they never mix with other brands (such as Databro or GLM).

> [!WARNING]
> **CRITICAL GATE (No Unrequested Visual Generation):**
> Do not generate slide images, videos, or Canva designs without prior confirmation from the user.
> Always review the narrative arc, slide copy, or video script with the user before executing rendering scripts.

---

## When to Use

* When designing or rendering 4:5 Instagram carousel slides for `@yvnalvworks`.
* When authoring Remotion programmatic video compositions (9:16 or 16:9) using `YvnalvworksBaseCanvas`.
* When formatting Lucide 2px monoline SVG vectors and high-contrast technical diagrams.
* When exporting video subtitles or slide decks to `D:\yvnalv\Onedrive\04. yvnalvworks\Contents\`.
* Invoke via slash command: `/yvnalvworks-brand-motion`.

## When NOT to Use

* Do not use for Databro Studio content (use `/databro-brand-motion` instead).
* Do not use for GLM Systems enterprise marketing (use `/glm-brand-motion` instead).
* Do not use for early topic ideation or research before copy is drafted (use `/yvnalvworks-content-ideas` first).

---

## Bundled Resources

| Path | Purpose & When to Load |
|---|---|
| `references/yvnalvworks-brand-guidelines.md` | Core color tokens, typography rules, and prohibition of AI gradients. |
| `references/yvnalvworks-brand-assets-checklist.md` | Verification checklist for logos, avatars, tokens, and storage locations. |
| `references/lucide-icon-spec.md` | Technical SVG rules and concept-to-icon mapping for Lucide vectors. |
| `scripts/render_carousel.py` | Playwright-based deterministic CLI renderer for 1080x1350 PNG slides (`python scripts/render_carousel.py <spec.json> --out <dir>`). |
| `assets/brand-kit/guidelines/yvnalvworks.tokens.json` | Machine-readable design tokens for canvas, text, borders, and safe zones. |
| `assets/brand-kit/logos/yvnalvworks-logo-transparent.png` | Official high-resolution transparent wordmark logo. |
| `assets/brand-kit/logos/yovan-avatar.png` | Official circular headshot avatar for top-left slide lockups. |
| `assets/YvnalvworksBaseCanvas.starter.tsx` | Reusable Remotion canvas wrapper component for 9:16 and 4:5 stages. |

---

## Visual Design Standard

1. **Canvas**: Deep Matte Charcoal (`#121212`). Pure black (`#000000`) is avoided to reduce ocular fatigue.
2. **Typography**:
   - `Inter` with tight tracking (`-0.035em`) for headlines.
   - Weights: 800 (ExtraBold) for main statements, 600 (SemiBold) for subheadings, 400 (Regular) for body.
   - `JetBrains Mono` or `Geist Mono` for slide counters (`01 / 05`), code blocks, and metrics.
3. **Accent Highlights**:
   - `Electric Lime` (`#C1FF72`) applied sparingly on punchlines and as solid backgrounds for framework cards.
4. **Lucide Monoline Icons**:
   - Strict 2px stroke width, rounded caps, rounded joins, zero fills, 24x24 viewBox.
5. **Reels Safe Zones (9:16)**:
   - Header safe area: 0 - 150px
   - Bottom interaction safe area: 1640 - 1920px
   - Right action strip: 960 - 1080px
   - Closed Captions locked at: Center Y = 1480px

---

## Definition of Done

A task run of `yvnalvworks-brand-motion` is complete when:
1. Concept and copy were confirmed with the user prior to visual rendering.
2. Design complies with yvnalvworks tokens (Inter font, #121212 canvas, #C1FF72 accents).
3. All icons follow authentic Lucide 2px monoline SVG specifications.
4. Rendered slides or videos were output to the designated directory and visually inspected.
