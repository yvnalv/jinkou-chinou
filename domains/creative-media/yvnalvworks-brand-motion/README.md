# yvnalvworks-brand-motion

yvnalvworks (`@yvnalvworks` / `yvnalvworks.com`) specialized brand motion and visual design skill extending `the-motion-designer`.

## When to use

* Use when rendering 4:5 Instagram carousel slides for yvnalvworks.
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
│   ├── lucide-icon-spec.md                  # Lucide SVG standards and concept mappings
│   ├── yvnalvworks-brand-assets-checklist.md# Brand kit asset checklist
│   └── yvnalvworks-brand-guidelines.md      # Color tokens, typography, and rules
├── scripts/
│   └── render_carousel.py                   # Playwright-based 1080x1350 slide renderer
└── assets/
    ├── YvnalvworksBaseCanvas.starter.tsx    # Remotion stage wrapper component
    └── brand-kit/
        ├── guidelines/
        │   └── yvnalvworks.tokens.json      # Machine-readable design tokens
        └── logos/
            ├── yovan-avatar.png             # Circular profile avatar
            └── yvnalvworks-logo-transparent.png # Transparent wordmark logo
```

## Changelog

### 0.1.0 — 2026-11-12
* Initial specialized release for yvnalvworks brand motion and slide rendering.
* Integrated Inter typography, Matte Charcoal #121212 canvas, Electric Lime #C1FF72 accents, and Lucide SVG specifications.
* Added automated Playwright 4:5 carousel renderer and Remotion base canvas starter.
