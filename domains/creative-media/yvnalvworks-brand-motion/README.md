# yvnalvworks-brand-motion

yvnalvworks (`@yvnalvworks` / `yvnalvworks.com`) specialized brand motion and visual design skill extending `the-motion-designer`.

## When to use

* Use when rendering 4:5 Instagram carousel covers and slides for yvnalvworks that match the published reference covers.
* Use when producing 9:16 Remotion reels with animated, caption-timed storytelling visuals from `assets/reel-starter/`.
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
│   ├── reels-motion-system.md               # Reel layout, timing, beat-to-visual patterns, motion, QA
│   ├── lucide-icon-spec.md                  # Lucide SVG standards and concept mappings
│   ├── yvnalvworks-brand-assets-checklist.md# Brand kit asset checklist
│   └── yvnalvworks-brand-guidelines.md      # Background, color tokens, typography, and rules
├── scripts/
│   └── render_carousel.py                   # Playwright 4:5 renderer (cover + html slides, grain bg)
└── assets/
    ├── reel-starter/                        # Ready-to-run Remotion reel project
    │   ├── README.md                        # Setup, files, render steps
    │   ├── package.json                     # Pinned Remotion + lucide-react
    │   ├── tsconfig.json
    │   ├── remotion.config.ts
    │   └── src/
    │       ├── index.ts, Root.tsx, Reel.tsx # Entry, two compositions, example reel
    │       ├── theme.ts, timing.ts          # Tokens + centered layout, caption-keyed timing
    │       ├── components/Base.tsx          # Background, lockup, captions, wipe, app tile, tag
    │       ├── components/Patterns.tsx      # Panel, heading, phone, chart, meter, rail, end card
    │       └── data/captions.json           # Example captions
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

### 0.4.0 — 2026-11-12
* Reels system from the approved "The AI Engineering Workflow" reel: `references/reels-motion-system.md` (centered layout on x 540, caption-keyed timing, one animated visual per story beat, motion rules, color meaning, captions, QA).
* New `assets/reel-starter/`: a typechecked, render-tested Remotion project with Base and Patterns components (PhoneFrame, LineChart, Meter, StepRail, AppTile, Wipe, EndCard, morph) and two compositions (captions and clean).
* Removed `assets/YvnalvworksBaseCanvas.starter.tsx`; it conflicted with the reel system (off-center margins, ALL CAPS footer).
* Tokens gain reels layout, caption style, and motion colors.

### 0.3.0 — 2026-11-12
* Storytelling copy: slides render the flowing sentences from `/yvnalvworks-content-ideas`; no fragment bullets or ALL CAPS labels.
* Reels captions are sentence-case natural phrases (3 to 6 words, max 32 characters), Poppins 600, white, one line, at Y=1480px.

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
