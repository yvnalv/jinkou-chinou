# databro-brand-motion

Specialized brand motion skill for **Databro Studio (`@databroid` — "Belajar Data Science")**, extending `the-motion-designer`.

## Quick Facts

| Field | Value |
| --- | --- |
| Domain | `creative-media` |
| Type | `specialized` (`extends: the-motion-designer`) |
| Version | `0.4.1` |
| Owner | `@yvnalv` |
| Tags | `databro`, `remotion`, `motion-graphics`, `brand-guidelines`, `tiktok`, `reels`, `data-science` |

## When to use

- Creating TikTok, Instagram Reels, YouTube Shorts, `4:5` Feed, or `16:9` motion videos for **Databro Studio (`@databroid`)**.
- Applying Databro's isolated visual identity and **Standard Base Content Canvas** (`DatabroBaseCanvas`: `#121212` matte charcoal canvas, white text, `#BB86FC` lavender headlines, `#03DAC6` teal and `#C1FF72` lime accents, `#F0ECE2` cream emblem circles, `#D92D20` terminal callouts, left-aligned slide layouts, persistent top-left `Databro / Belajar Data Science` lockup and top-right `@databro.id`, fixed Closed Captions locked at `Y = 1480px`, CapCut transitions, and TikTok SFX/voiceover brand-kit assets).
- Invoke with `/databro-brand-motion`, or pick Databro in `the-motion-designer`.

## Structure

```text
databro-brand-motion/
├── SKILL.md                                         # Databro visual identity, Base Canvas & choreography rules
├── README.md                                        # Human overview & changelog
├── config/
│   └── skill.yaml                                   # Metadata (type: specialized, extends: the-motion-designer)
├── references/
│   ├── databro-brand-assets-checklist.md            # Tracking checklist for every brand kit asset
│   ├── databro-brand-guidelines.md                  # Pixel-sampled palette, slide layout, icons, Base Canvas presets
│   └── databro-content-and-voiceover-guide.md       # Archetypes, hooks, voiceover pipeline, fixed CC & SFX choreography
├── assets/
│   ├── brand-kit/                                   # Standardized brand asset storage folder
│   │   ├── README.md                                # Inventory of where to drop every brand file
│   │   ├── persona/                                 # databro-persona.md (tone, audience & script rules)
│   │   ├── guidelines/                              # databro.tokens.json & pdfs/
│   │   ├── fonts/                                   # Drop .ttf / .otf / .woff2 font files here
│   │   ├── logos/                                   # databro-avatar.jpg & brand logos
│   │   ├── graphics/                                # Step badges, table/terminal/scatter references, slide screenshots
│   │   ├── references/                              # Official carousel slides (color and layout source of truth)
│   │   └── audio/                                   # sfx/ (6 TikTok .wav files), bgm/, voiceover/talent-samples/ + generated/
│   ├── databro-avatar.jpg                           # Official Databro Studio circular creator avatar
│   ├── databro.brand.starter.ts                     # Isolated databroBrand tokens & DATABRO_CANVAS_PRESETS
│   ├── DatabroBaseCanvas.starter.tsx                # 5-layer reusable Databro Base Content Canvas
│   ├── DatabroLogoLockup.starter.tsx                # Top-left avatar lockup + top-right @databro.id handle
│   ├── DatabroCaptions.starter.tsx                  # Cardless 2-to-4 word ALL-CAPS white CC locked at Y=1480px
│   └── generate_databro_cloned_vo.starter.py        # Per-scene voiceover (cloned or Edge-TTS) + caption timings JSON
└── evals/
    └── evals.json                                   # Trigger & non-trigger evaluation suite
```

## Changelog

### 0.4.1 - 2026-11-10

- Voiceover generator: a sentence-ending word after a full 4-word caption chunk now borrows the previous chunk's last word instead of joining the next sentence (fixes chunks like `SKILL. SIMPELNYA GINI, BRO`). Only sentence endings (`.?!`) block the borrow; breath commas do not. Found while producing the "Apa itu Skill dalam Agentic AI?" video.

### 0.4.0 - 2026-11-10

- Re-sampled every brand color from the 13 official carousel slides and made them canonical across SKILL.md, references, `databro.tokens.json`, and `databro.brand.starter.ts`: lavender `#BB86FC` (was `#B487EC`), teal `#03DAC6` (was `#02DAC5`), lime `#C1FF72` (was `#BFFF72` / `#BEF96E`), coral `#FF5757` (was `#E95F62`), body text and captions `#FFFFFF` (was `#FAF9F5`), wordmark and handle cream `#F2EFEB` (was `#A3A3A3`), emblem cream `#F0ECE2` (was `#F2EBE1` in places), canvas `#121212` (was `#111111` in places).
- Replaced the guessed code-card palette with the GitHub Dark values seen on the slides (`#24292E`, `#F97583`, `#FFAB70`, `#79B8FF`, `#6A737D`, `#E1E4E8`). Dropped the separate validation violet; `accentViolet` is now a deprecated alias of the lavender. Added table, quote, and `textBrand` tokens.
- `DatabroBaseCanvas` now actually renders the top-right `@databro.id` handle (new `DatabroSocialHandle`), and lays scenes out left-aligned like the carousels instead of centered.
- Unified the content archetypes into five keys used everywhere: `code-walkthrough`, `concept-theory`, `tool-listicle` (new), `launch-showcase`, `opinion-editorial`.
- Fixed React Icons names that no longer exist (`LuCode2` -> `LuCodeXml`, `LuAlertTriangle` -> `LuTriangleAlert`, `LuAlertCircle` -> `LuCircleAlert`), verified against `react-icons@5.7.0`, and added a name check rule.
- Settled conflicting values: Edge-TTS `pitch -4Hz`, `rate -2%`; BGM volume `0.08`; outro hold 24 frames; mono font `JetBrains Mono` first.
- Rewrote the voiceover generator: CLI with `--help`, standard-library ElevenLabs call that requires a cloned `DATABRO_VOICE_ID` (no silent stock voice), and Edge-TTS word timings that produce ready 2-4 word caption chunks in the original spelling.
- Removed the dependency on another skill's validator file from the Definition of Done; converted absolute `file:///` links in the checklist to relative links; removed the launch-reel "ambient glow" that contradicted the no-glow rule.

### 0.3.0 (2026-11-09)

- Mandated React Icons (`react-icons/lu`, `tb`, `fi`, `fa6`) as strict source of truth for vector icons, banning AI clipart and emojis.
- Implemented absolute ban on em-dashes across all writing, video text, and Closed Captions.
- Calibrated baritone voiceover matching authentic human talent master audio (measured F0 = 86 Hz, pitch: -4Hz, rate: -2%).
- Extracted exact brand color hex codes from authentic Databro carousel slides: `#121212` matte charcoal, `#FAF9F5` warm cream, `#B487EC` lavender question headers, `#02DAC5` cyan, and `#24292D` code card.
- Added persistent top-right `@databro.id` handle to the Standard Base Content Canvas.

### 0.2.0 — 2026-11-09

- Added the standardized `assets/brand-kit/` folder hierarchy (`guidelines/`, `fonts/`, `logos/`, `graphics/`, `references/`, `audio/sfx/`, `audio/bgm/`, `audio/voiceover/talent-samples/`, `audio/voiceover/generated/`) with pre-populated TikTok `.wav` SFX (`keyboard-typing`, `pop-up`, `whoosh-transition`, `mouse-click`, `progress-ticks`, `callout-ding`) and ambient BGM.
- Added `assets/DatabroBaseCanvas.starter.tsx` and multi-platform `DATABRO_CANVAS_PRESETS` (`'9:16'`, `'4:5'`, `'1:1'`, `'16:9'`) in `assets/databro.brand.starter.ts` so the top-left `Databro` lockup (`top: 108px, left: 100px` on `9:16`) animates only once at `frame 0..12` and Closed Captions stay locked at `Y = 1480px` with zero vertical bounce across CapCut scene transitions.
- Added `references/databro-content-and-voiceover-guide.md` and `assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md` detailing talent voice recording specs, Indonesian/English calibration scripts, AI voice cloning, and prompt templates.

### 0.1.0 — 2026-11-09

- Initial release of `databro-brand-motion` extending `the-motion-designer`.
- Extracted Databro Studio (`@databroid`) brand tokens (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), top-left avatar lockup (`databro-avatar.jpg` + `Databro / Belajar Data Science`), centered Emblem Circle and Command Prompt Callout scene archetypes, and cardless 2–4 word uppercase Closed Captions.
