# databro-brand-motion

Specialized brand motion skill for **Databro Studio (`@databroid` — "Belajar Data Science")**, extending `the-motion-designer`.

## Quick Facts

| Field | Value |
| --- | --- |
| Domain | `creative-media` |
| Type | `specialized` (`extends: the-motion-designer`) |
| Version | `0.2.0` |
| Owner | `@yvnalv` |
| Tags | `databro`, `remotion`, `motion-graphics`, `brand-guidelines`, `tiktok`, `reels`, `data-science` |

## When to use

- Creating TikTok, Instagram Reels, YouTube Shorts, `4:5` Feed, or `16:9` motion videos for **Databro Studio (`@databroid`)**.
- Applying Databro's isolated visual identity and **Standard Base Content Canvas** (`DatabroBaseCanvas`: `#111111` matte charcoal canvas, `#BFFF72` lime green, `#F2EBE1` warm cream circle badges, `#D92D20` red UI/terminal callouts, persistent top-left `Databro / Belajar Data Science` avatar lockup at `100px, 108px`, fixed Closed Captions locked at `Y = 1480px`, CapCut transitions, and TikTok SFX/voiceover brand-kit assets).

## Structure

```text
databro-brand-motion/
├── SKILL.md                                         # Databro visual identity, Base Canvas & choreography rules
├── README.md                                        # Human overview & changelog
├── config/
│   └── skill.yaml                                   # Metadata (type: specialized, extends: the-motion-designer)
├── references/
│   ├── databro-brand-guidelines.md                  # Sampled @databroid hex palette, Base Canvas presets & archetypes
│   └── databro-content-and-voiceover-guide.md       # Prompting, voiceover cloning, fixed CC & SFX choreography guide
├── assets/
│   ├── brand-kit/                                   # Standardized brand asset storage folder
│   │   ├── README.md                                # Inventory of where to drop every brand file
│   │   ├── persona/                                 # databro-persona.md (tone, audience & script rules)
│   │   ├── guidelines/                              # databro.tokens.json & pdfs/
│   │   ├── fonts/                                   # Drop .ttf / .otf / .woff2 font files here
│   │   ├── logos/                                   # databro-avatar.jpg & brand logos
│   │   ├── graphics/                                # emblems/, ui-frames/, overlays/
│   │   ├── references/                              # Reference videos/ (.mp4) & designs/ (.png, .svg)
│   │   └── audio/                                   # sfx/ (6 TikTok .wav files), bgm/, voiceover/talent-samples/
│   ├── databro-avatar.jpg                           # Official Databro Studio circular creator avatar
│   ├── databro.brand.starter.ts                     # Isolated databroBrand tokens & DATABRO_CANVAS_PRESETS
│   ├── DatabroBaseCanvas.starter.tsx                # 5-layer reusable Databro Base Content Canvas
│   ├── DatabroLogoLockup.starter.tsx                # Persistent top-left avatar + Databro / Belajar Data Science lockup
│   └── DatabroCaptions.starter.tsx                  # Cardless 2-to-4 word ALL-CAPS white CC locked at Y=1480px
└── evals/
    └── evals.json                                   # Trigger & non-trigger evaluation suite
```

## Changelog

### 0.2.0 — 2026-11-09

- Added the standardized `assets/brand-kit/` folder hierarchy (`guidelines/`, `fonts/`, `logos/`, `graphics/`, `references/`, `audio/sfx/`, `audio/bgm/`, `audio/voiceover/talent-samples/`, `audio/voiceover/generated/`) with pre-populated TikTok `.wav` SFX (`keyboard-typing`, `pop-up`, `whoosh-transition`, `mouse-click`, `progress-ticks`, `callout-ding`) and ambient BGM.
- Added `assets/DatabroBaseCanvas.starter.tsx` and multi-platform `DATABRO_CANVAS_PRESETS` (`'9:16'`, `'4:5'`, `'1:1'`, `'16:9'`) in `assets/databro.brand.starter.ts` so the top-left `Databro` lockup (`top: 108px, left: 100px` on `9:16`) animates only once at `frame 0..12` and Closed Captions stay locked at `Y = 1480px` with zero vertical bounce across CapCut scene transitions.
- Added `references/databro-content-and-voiceover-guide.md` and `assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md` detailing talent voice recording specs, Indonesian/English calibration scripts, AI voice cloning, and prompt templates.

### 0.1.0 — 2026-11-09

- Initial release of `databro-brand-motion` extending `the-motion-designer`.
- Extracted Databro Studio (`@databroid`) brand tokens (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), top-left avatar lockup (`databro-avatar.jpg` + `Databro / Belajar Data Science`), centered Emblem Circle and Command Prompt Callout scene archetypes, and cardless 2–4 word uppercase Closed Captions.
