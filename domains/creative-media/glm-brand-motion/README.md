# glm-brand-motion

GLM Systems (`glmsystems.com`) specialized brand motion graphics and video production skill extending `the-motion-designer` with official Lime (`#CDFF70`), Emerald (`#003A40`), Stone Grey (`#444547`), and Cool White (`#F2F0FA`) tokens, Poppins typography, Flippy AI Agent narrative assets, product knowledge for AI Plus Agent (Globe+ and Synergy), and the `GlmBaseCanvas` 5-layer Remotion architecture.

Domain: `creative-media` · Type: `specialized` · Extends: `the-motion-designer`

## When to use

Invoke with `/glm-brand-motion`, or let Claude activate it automatically when you ask for:

- Creating LinkedIn B2B announcement or product demo videos (`16:9` or `4:5`) for **GLM Systems** (`glmsystems.com`).
- Introducing or explaining **Flippy**, the AI assistant embedded in Exact Globe+ and Exact Synergy.
- Producing YouTube product walk-throughs or feature release stingers with GLM brand styling.
- Converting ERP, workflow automation, or Synergy Kanban procedures into clean, high-contrast B2B motion sequences.
- Explaining specific AI Plus Agent features: Stock Depletion Forecasts, Screen-to-Stock verification, Recode master data renaming, Excel bulk mapping, or Role 501 security.
- Auditing or refactoring Remotion projects to adhere to official GLM brand tokens (Lime `#CDFF70`, Emerald `#003A40`, Stone Grey `#444547`, Cool White `#F2F0FA`), safe-zones, audio identity, and breathing room pacing.

Do not use this skill for Databro Studio (`@databroid`) projects (use `databro-brand-motion`) or generic, brand-agnostic motion design (use `the-motion-designer`).

## Structure

```text
glm-brand-motion/
├── SKILL.md                                        # Master skill instructions, modes, and signature rules
├── README.md                                       # Overview, structure, and changelog
├── config/
│   └── skill.yaml                                  # Manifest extending the-motion-designer (v0.3.0)
├── evals/
│   └── evals.json                                  # Triggering and regression test cases
├── references/
│   ├── glm-brand-assets-checklist.md               # Actionable asset verification checklist
│   ├── glm-brand-guidelines.md                     # Visual identity spec, colors, typography, React Icons
│   ├── glm-content-and-voiceover-guide.md          # Content archetypes, pacing, and Closed Captions
│   └── products/
│       ├── README.md                               # Product knowledge directory overview
│       ├── ai-plus-agent-globeplus.md              # Deep spec for Flippy in Exact Globe+
│       └── ai-plus-agent-synergy.md                # Deep spec for Flippy in Exact Synergy
└── assets/
    ├── glm.brand.starter.ts                        # TypeScript brand tokens, color palette, and canvas geometry
    ├── GlmBaseCanvas.starter.tsx                   # 5-layer Base Content Canvas preset across 16:9, 4:5, 9:16, 1:1
    ├── GlmCaptions.starter.tsx                     # Fixed Y coordinate Closed Captions component
    ├── GlmLogoLockup.starter.tsx                   # Animated persistent top-left GLM bird logo lockup
    └── brand-kit/
        ├── README.md                               # Brand kit asset documentation
        ├── audio/
        │   ├── bgm/
        │   │   └── bgm-ambient.wav                 # Royalty-free warm ambient background loop
        │   └── sfx/
        │       ├── callout-ding.wav                # Harmonic ding SFX for highlight callouts
        │       ├── keyboard-typing.wav             # Mechanical typing SFX for text and code
        │       ├── mouse-click.wav                 # Crisp UI mouse click SFX
        │       ├── pop-up.wav                      # UI bubble pop entry SFX
        │       ├── progress-ticks.wav              # Digital tick SFX for loading bars
        │       └── whoosh-transition.wav           # Smooth air whoosh transition SFX
        ├── graphics/
        │   ├── README.md                           # Graphics documentation
        │   ├── email.png                           # Flippy drafted email popup screenshot
        │   ├── menu.png                            # Exact Globe+ purchase/sales menu screenshot
        │   ├── sales.png                           # Exact Globe+ sales orders table screenshot
        │   └── stock.png                           # Exact Globe+ warehouse stock verification screenshot
        ├── guidelines/
        │   └── glm.tokens.json                     # Machine-readable color and layout tokens
        ├── logos/
        │   ├── README.md                           # Vector logos documentation
        │   ├── GLM-BIRD-Color.svg                  # Official dual lime birds brandmark SVG
        │   └── GLM-black-Text-Color-Bird.svg       # Official horizontal lockup SVG (Wordmark + Lime Bird)
        ├── persona/
        │   ├── README.md                           # Persona documentation
        │   └── glm-persona.md                      # B2B enterprise persona, tone, and Flippy arc
        └── references/
            ├── README.md                           # Campaign references documentation
            └── flippy-video-script.md              # Official Flippy launch video production script
```

## Changelog

### 0.3.0 — 2026-11-10

- Updated exact official GLM brand color codes and RGB values: Lime `#CDFF70` (RGB: 205, 255, 112), Emerald `#003A40` (RGB: 0, 58, 64), Stone Grey `#444547` (RGB: 68, 69, 71), and Cool White `#F2F0FA` (RGB: 242, 240, 250).
- Calibrated primary typography and text tokens to Stone Grey (`#444547`) across all Remotion components, captions, and token sets.

### 0.2.0 — 2026-11-10

- Integrated authentic GLM brand assets and guidelines from `C:\Users\yvnal\Downloads\glm-video-skill`.
- Added dedicated product knowledge specifications for **AI Plus Agent for Exact Globe+** (`references/products/ai-plus-agent-globeplus.md`) and **AI Plus Agent for Exact Synergy** (`references/products/ai-plus-agent-synergy.md`) directly from `docs.glmsystems.com`.
- Codified GLM audio brand identity: **Zakelijk, upbeat, gegrond** (~116-120 BPM, calm harmony, active groove, stabs over arpeggios, tight audible SFX).
- Enforced production rules: "Script-First, User Sign-Off Before Rendering", single idea per video, verified citation captions, and 100% audio-independent comprehension on mute.

### 0.1.0 — 2026-11-10

- Initial release of `glm-brand-motion` extending `the-motion-designer`.
- Isolated GLM Systems brand tokens: Emerald (`#003A40`), Lime (`#CDFF70`), Cool White (`#F2F0FA`), and Stone Grey (`#444547`).
- Bundled official vector SVG brandmarks (`GLM-BIRD-Color.svg`, `GLM-black-Text-Color-Bird.svg`) and UI screenshots (`menu.png`, `sales.png`, `stock.png`, `email.png`).
- Standardized `GlmBaseCanvas.starter.tsx` across `16:9`, `4:5`, `9:16`, and `1:1` aspect ratios with persistent chrome and fixed Y Closed Captions.
- Enforced React Icons (`react-icons/lu`) as vector source of truth, absolute ban on em-dashes (`—`), and calibrated reading time (0.4s/word, min 2.0s per card, 10-frame settle buffer).
- Bundled royalty-free ambient BGM and 6 synthesized UI sound effects.
