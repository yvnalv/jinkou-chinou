---
name: yvnalvworks-brand-motion
description: "yvnalvworks (@yvnalvworks / yvnalvworks.com) specialized brand motion skill extending the-motion-designer. Applies yvnalvworks' signature technical aesthetic: matte charcoal grain background image (never a flat fill), Poppins Bold headlines with Warm Ivory #F0ECE2 and white text, one Electric Lime #C1FF72 punchline phrase, the avatar plus name and handle lockup above the headline on covers, Lucide 2px monoline SVG icons, and locked Y=1480px captions. Renders 4:5 carousel covers and slides that match the published reference covers, and Remotion videos. Use when creating carousels, covers, slides, or videos for yvnalvworks or invoking /yvnalvworks-brand-motion."
metadata:
  version: 0.2.1
---

# yvnalvworks Brand Motion: Visual Identity and Canvas Engine

Specialized brand motion and visual design skill extending **`the-motion-designer`** exclusively for **yvnalvworks (Yovan Alvianto : yvnalvworks.com / `@yvnalvworks`)**.

This skill isolates all yvnalvworks visual guidelines, typography, color tokens, the grain background, reference covers, Lucide monoline vectors, Remotion canvases, and automated 4:5 carousel slide renderers so they never mix with other brands (such as Databro or GLM).

> [!WARNING]
> **CRITICAL GATE (No Unrequested Visual Generation):**
> Do not generate slide images, videos, or Canva designs without prior confirmation from the user.
> Always review the narrative arc, slide copy, or video script with the user before executing rendering scripts.

---

## When to Use

* When designing or rendering 4:5 Instagram carousel slides and covers for `@yvnalvworks`.
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
| `references/cover-slide-spec.md` | Open for every carousel cover: measured layout, lockup, headline type scale, highlight rule, and review checklist. |
| `references/yvnalvworks-brand-guidelines.md` | Core color tokens, background rule, Poppins typography, and prohibited visuals. |
| `references/yvnalvworks-brand-assets-checklist.md` | Verification checklist for background, avatars, logos, tokens, reference covers, and storage locations. |
| `references/lucide-icon-spec.md` | Technical SVG rules and concept-to-icon mapping for Lucide vectors. |
| `scripts/render_carousel.py` | Playwright renderer for 4:5 slides on the grain background, exported 2160x2700 PNG: `python <skill-dir>/scripts/render_carousel.py <spec.json> --out <dir> [--scale 2]`. `cover` slides take a `headline` (`\n` breaks, `[[...]]` lime); `html` slides take a fragment (wrapped in the brand shell) or a full document with `{{BG}}`, `{{AVATAR}}`, `{{FONTS}}` tokens. Prints JSON; exits 1 if Poppins failed to load or a hand-broken cover line overflowed the 860px measure and wrapped. |
| `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png` | The background of every slide and video frame (matte charcoal grain). Never substitute a flat fill. |
| `assets/reference-covers/cover-ref-listicle-ai-updates.jpg` | Published listicle cover. Compare renders against it. |
| `assets/reference-covers/cover-ref-should-know-maf.jpg` | Published "What X Should Know About Y" cover. Compare renders against it. |
| `assets/brand-kit/guidelines/yvnalvworks.tokens.json` | Machine-readable design tokens: colors, background, typography, cover layout, safe zones. |
| `assets/brand-kit/logos/yovan-avatar-color.png` | Color avatar used in the cover lockup (66px circle). |
| `assets/brand-kit/logos/yovan-avatar.png` | Grayscale 1080px headshot for large placements. |
| `assets/brand-kit/logos/yvnalvworks-logo-transparent.png` | Official transparent wordmark logo. |
| `assets/YvnalvworksBaseCanvas.starter.tsx` | Reusable Remotion canvas wrapper with the grain background and Poppins for 9:16 and 4:5 stages. |

---

## Visual Design Standard

1. **Background**: the grain image `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png` scaled with `cover` on every slide and frame. `#121212` is only the fallback behind it, never the visible background.
2. **Typography**:
   - `Poppins` for headlines, lockup, and body. Headlines 700 Bold, tracking `-0.04em`, line height `1.02`; subheadings 600; body 400.
   - `JetBrains Mono` or `Geist Mono` (500) for slide counters (`01 / 05`), code blocks, and metrics.
3. **Color**: headlines `#FFFFFF`, handle and body `#F0ECE2` Warm Ivory, secondary `#8E8E93`, muted `#71717A`.
4. **Accent Highlight**: `Electric Lime` (`#C1FF72`) on exactly one punchline phrase per slide, and as solid backgrounds for framework cards.
5. **Cover (slide 1)**: color avatar + `yvnalvworks` / `@yvnalvworks` lockup above a 96px Poppins Bold headline of 3 to 4 hand-broken lines, left-aligned text in an optically centered block, nothing else on the slide. Full spec: `references/cover-slide-spec.md`.
6. **Lucide Monoline Icons**: strict 2px stroke width, rounded caps, rounded joins, zero fills, 24x24 viewBox.
7. **Reels Safe Zones (9:16)**:
   - Header safe area: 0 - 150px
   - Bottom interaction safe area: 1640 - 1920px
   - Right action strip: 960 - 1080px
   - Closed Captions locked at: Center Y = 1480px

---

## Workflow

1. **Confirm copy.** Get the approved slide copy or script (usually from `/yvnalvworks-content-ideas`). For the cover, confirm the headline line breaks and the single lime phrase.
2. **Build the spec.** Slide 1 is a `cover` slide. Body slides are `html` fragments that use Poppins, Lucide icons, and the lime accent; the renderer puts them on the grain background.
3. **Render** with `scripts/render_carousel.py` to the agreed folder under `D:\yvnalv\Onedrive\04. yvnalvworks\Contents\`. If the JSON reports a Poppins warning, fix connectivity and re-render; do not ship fallback fonts. If it reports a cover overflow warning, re-break the headline (for example "Should Know / About [[Subject]]") and re-render.
4. **Compare.** View the rendered cover next to a file in `assets/reference-covers/` and walk the checklist in `references/cover-slide-spec.md`. Fix any drift in scale, position, background, or highlight before handing over.
5. **Video.** For Remotion, start from `assets/YvnalvworksBaseCanvas.starter.tsx` (grain background, Poppins) and keep captions at Y=1480px.

---

## Definition of Done

A task run of `yvnalvworks-brand-motion` is complete when:
1. Concept and copy were confirmed with the user prior to visual rendering.
2. Every slide or frame sits on the grain background image, not a flat fill.
3. Design complies with yvnalvworks tokens (Poppins type, white and Warm Ivory text, one #C1FF72 phrase).
4. The cover matches the reference covers in layout, lockup, and type scale.
5. All icons follow authentic Lucide 2px monoline SVG specifications.
6. Rendered slides or videos were output to the designated directory and visually inspected.
