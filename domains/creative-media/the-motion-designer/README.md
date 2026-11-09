# the-motion-designer

Programmatic motion graphics, social media video, kinetic typography, animated infographics, and frame-accurate React video engineering powered by Remotion (`remotion-dev/remotion`).

## Quick Facts

| Field | Value |
| --- | --- |
| Domain | `creative-media` |
| Type | `core` |
| Version | `0.2.0` |
| Owner | `@yvnalv` |
| Tags | `creative-media`, `remotion`, `motion-graphics`, `video-production`, `animation`, `social-media`, `react` |

## When to use

- Designing and building programmatic videos, reels, shorts, stories, product launch teasers, kinetic typography, lower-thirds, or animated data charts in React + TypeScript with Remotion.
- Selecting and isolating brand guidelines (`BrandTheme` tokens, fonts, palettes, logos, and spring physics) across multiple brands (e.g., GLM, Databro, or custom brand folders) without cross-brand leakage.
- Enforcing platform-specific UI Safe Zones and Closed Caption (CC) placement for Instagram (Reels `9:16` + `4:5` Home Feed crop, Stories, `4:5` Feed, `1:1`), TikTok, YouTube (Shorts & `16:9`), LinkedIn, Facebook, and X.
- Exporting MP4 (`h264`/`h265`), WebM (`vp8`/`vp9`), transparent ProRes 4444 overlays (`prores --prores-profile=4444 --image-format=png`), GIFs, single stills (`npx remotion still`), PNG/JPEG frame sequences (`--sequence`), and audio masters.
- Auditing and repairing flickering Remotion compositions caused by CSS transitions, `@keyframes`, raw `<img>`/`<video>` tags, or mismatched `@remotion/*` package versions.

## Structure

```text
the-motion-designer/
├── SKILL.md                                        # Persona, 4-step Pre-Generation Wizard, modes, & guardrails
├── README.md                                       # Human overview & changelog
├── config/
│   └── skill.yaml                                  # Machine metadata & version manifest
├── references/
│   ├── remotion-core-api.md                        # Verified Remotion v4.x hooks, components, & determinism rules
│   ├── packages-and-capabilities.md                # Official @remotion/* ecosystem packages & licensing
│   ├── social-media-safe-zones.md                  # Platform aspect ratios & pixel-exact UI/CC safe-zone insets
│   ├── export-formats-and-codecs.md                # CLI render commands, codecs, alpha transparency, & still exports
│   ├── motion-styles-and-choreography.md           # 8 motion style archetypes, spring presets, & pacing templates
│   ├── brand-system-architecture.md                # BrandTheme contract & multi-brand skill isolation pattern
│   └── STORYBOARD_SPEC.template.md                 # Frame-by-frame storyboard specification template
├── scripts/
│   └── validate_remotion_project.py                # CLI auditor for CSS transitions, timers, raw tags, & version parity
├── assets/
│   ├── brand-tokens.starter.ts                     # Strict TypeScript BrandTheme interface & neutral fallback theme
│   ├── SafeZoneOverlay.starter.tsx                 # Toggleable platform UI safe-zone & CC guide overlay component
│   ├── Root.starter.tsx                            # Multi-ratio Remotion <Composition> & <Still> registration starter
│   └── SceneTemplate.starter.tsx                   # Frame-deterministic scene starter using spring() & interpolate()
└── evals/
    └── evals.json                                  # Trigger & non-trigger evaluation suite
```

## Changelog

### 0.2.0 — 2026-11-09

- Enforced symmetric horizontal and vertical centering (`left === right`) for the main content container and Closed Captions (CC) so layouts are always dead-center on the canvas while clearing right-side social UI buttons.
- Added persistent fixed Top-Left Brand Logo and Top-Right Icon/Status Header bar rule across compositions.
- Adopted `the-uix-designer` anti-AI craft standards: banned all CSS gradients (`linear-gradient`, `radial-gradient`, gradient text) and blurry glow orbs in favor of flat, solid WCAG AA semantic color tokens; banned em-dashes (`—`), `//` badge prefixes, arrow/dingbat characters, and emoji icons in favor of sentence-case copy and geometric `<svg>` icons.
- Upgraded `scripts/validate_remotion_project.py` to automatically flag CSS gradients, blurry glow filters, em-dashes, `//` label prefixes, and emoji/dingbat icons.

### 0.1.0 — 2026-11-09

- Initial release of `the-motion-designer` under the `creative-media` domain.
- Added mandatory 4-Step Pre-Generation Discovery Wizard (Brand Profile, Deliverable & Export Format, Motion Style, Platform & UI Safe-Zone Preset).
- Added pixel-exact Social Media UI Safe Zones and Closed Caption (CC) protection across Instagram, TikTok, YouTube, LinkedIn, Facebook, and X.
- Added multi-brand isolation architecture (`BrandTheme` TypeScript contract) enabling brand-specific child skills (`extends: the-motion-designer`) with zero cross-brand leakage.
- Bundled Remotion v4.x reference documentation, starter `.ts`/`.tsx` templates, and `validate_remotion_project.py` determinism auditor.
