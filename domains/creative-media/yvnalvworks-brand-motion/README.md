# yvnalvworks-brand-motion

yvnalvworks (`@yvnalvworks` / `yvnalvworks.com`) specialized brand motion and visual design skill extending `the-motion-designer`.

## When to use

* Use when rendering 4:5 Instagram carousel covers and slides for yvnalvworks that match the published reference covers.
* Use when generating Remotion programmatic video compositions with `YvnalvworksBaseCanvas`.
* Use when creating Lucide-based technical architecture diagrams and poster typography slides.
* Use when preparing social-media safe vertical motion graphics.
* Invoke via slash command: `/yvnalvworks-brand-motion`.

## Structure

```
yvnalvworks-brand-motion/
├── SKILL.md                                 # Core agent instructions and gates
├── README.md                                # Human documentation and changelog
├── config/
│   └── skill.yaml                           # Machine-readable manifest and policies
├── evals/
│   └── evals.json                           # Trigger and behavior eval test cases
├── references/
│   ├── cover-slide-spec.md                  # Measured cover layout, lockup, headline scale, checklist
│   ├── lucide-icon-spec.md                  # Lucide SVG standards and concept mappings
│   ├── yvnalvworks-brand-assets-checklist.md# Brand kit asset checklist
│   └── yvnalvworks-brand-guidelines.md      # Background, color tokens, typography, and rules
├── scripts/
│   └── render_carousel.py                   # Playwright 4:5 renderer (cover + html slides, grain bg)
└── assets/
    ├── YvnalvworksBaseCanvas.starter.tsx    # Remotion stage wrapper component
    ├── reference-covers/
    │   ├── cover-ref-listicle-ai-updates.jpg# Published listicle cover
    │   └── cover-ref-should-know-maf.jpg    # Published "Should Know About" cover
    └── brand-kit/
        ├── backgrounds/
        │   └── yvnalvworks-grain-bg.png     # Matte charcoal grain background (every slide)
        ├── guidelines/
        │   └── yvnalvworks.tokens.json      # Machine-readable design tokens
        └── logos/
            ├── yovan-avatar-color.png       # Color avatar for the cover lockup
            ├── yovan-avatar.png             # Grayscale 1080px headshot
            └── yvnalvworks-logo-transparent.png # Transparent wordmark logo
```

## Changelog

### 0.2.1 — 2026-11-12
* `render_carousel.py` warns (exit 1) when a hand-broken cover line is too wide and wraps; found on the first real carousel, where "Should Know About" overflowed.
* Cover spec documents the line-width limit and the "Should Know / About [[Subject]]" break.

### 0.2.0 — 2026-11-12
* Added the published reference covers, the measured `references/cover-slide-spec.md`, and the color avatar for the cover lockup.
* Background is now the grain image `yvnalvworks-grain-bg.png` on every slide and frame; flat `#121212` fills are no longer allowed.
* Typography changed from Inter to Poppins (headlines 700, -0.04em, line height 1.02), matching the published covers. This changes rendered output.
* `render_carousel.py`: new `cover` slide type, fragment slides wrapped in the brand shell, `{{BG}}`/`{{AVATAR}}`/`{{FONTS}}` tokens, `--scale`, JSON output, font-load check; fixed `device_scale_factor` being passed inside the viewport.
* Tokens, Remotion starter, guidelines, and assets checklist updated to match.

### 0.1.0 — 2026-11-12
* Initial specialized release for yvnalvworks brand motion and slide rendering.
* Integrated Inter typography, Matte Charcoal #121212 canvas, Electric Lime #C1FF72 accents, and Lucide SVG specifications.
* Added automated Playwright 4:5 carousel renderer and Remotion base canvas starter.
