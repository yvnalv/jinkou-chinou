# Standard Base Content Canvas & Brand-Kit Architecture

Every motion video produced by `the-motion-designer` or any extending brand skill (such as `databro-brand-motion`, `glm-brand-motion`, etc.) is built on a single reusable **Standard Base Content Canvas** ([`assets/BaseContentCanvas.starter.tsx`](../assets/BaseContentCanvas.starter.tsx) + [`assets/canvas-presets.starter.ts`](../assets/canvas-presets.starter.ts)).

Instead of rebuilding background colors, logo positions, closed caption coordinates, and safe-zone containers inside every scene, you configure or duplicate the **Base Content Canvas** once per brand or aspect ratio.

---

## 1. The 5-Layer Persistent vs. Transitioning Architecture

A common mistake in programmatic video is placing the brand logo or closed captions *inside* individual scenes—causing the logo and captions to slide, fade, or jump every time a scene transitions.

The **Standard Base Content Canvas** solves this by separating **Persistent Root Layers** from the **Transitioning Center Stage**:

```text
<BaseContentCanvas aspectRatio="9:16" brand={brand} captions={captions} soundCues={soundCues}>
│
├── Layer 0: Solid Flat Canvas Background (Persistent — never transitions)
│
├── Layer 1: Symmetric Centered Stage (top/bottom/left/right safe box, left === right)
│   └── <TransitionSeries> (ONLY this center stage transitions via CapCut slide/zoom/pop)
│       ├── <Scene01 />
│       ├── <Scene02 />
│       └── <Scene03 />
│
├── Layer 2: Fixed Top-Left Brand Lockup (Persistent — animates ONLY at frame 0..12, then stays static)
│   └── (Optional Fixed Top-Right Icon Slot)
│
├── Layer 3: Fixed Closed Captions (Persistent — locked at fixed Y coordinate with 0px vertical movement)
│
└── Layer 4: Audio & SFX Engine (<Audio /> for BGM, Voiceover, and frame-accurate TikTok SFX cues)
```

---

## 2. Standard Base Canvas Geometry Presets Across Platforms

Defined in [`assets/canvas-presets.starter.ts`](../assets/canvas-presets.starter.ts):

| Preset Key | Resolution | Target Platforms | Top-Left Logo `(left, top)` | Centered Content Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` (`left, right`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`9:16`** | `1080×1920` | TikTok, IG Reels, Stories, YouTube Shorts, FB Reels | `(100px, 108px)` | `top: 250, bottom: 490, left: 90, right: 90` | **`Y = 1480px`** (`left: 110, right: 110`) |
| **`4:5`** | `1080×1350` | Instagram Feed Portrait, LinkedIn Vertical, FB Feed | `(84px, 72px)` | `top: 180, bottom: 260, left: 84, right: 84` | **`Y = 1140px`** (`left: 96, right: 96`) |
| **`1:1`** | `1080×1080` | Instagram Square, LinkedIn Square, X Square | `(72px, 56px)` | `top: 150, bottom: 210, left: 72, right: 72` | **`Y = 910px`** (`left: 84, right: 84`) |
| **`16:9`** | `1920×1080` | YouTube 16:9, LinkedIn Landscape, X Video, Web Hero | `(96px, 64px)` | `top: 160, bottom: 200, left: 140, right: 140` | **`Y = 920px`** (`left: 240, right: 240`) |

### How to Modify or Duplicate a Base Canvas Preset

Use `customizeCanvasPreset()` from [`assets/canvas-presets.starter.ts`](../assets/canvas-presets.starter.ts) to create a brand-specific or platform-specific variant without touching scene files:

```ts
import { customizeCanvasPreset } from './canvas-presets.starter';

// Example: Customize the 9:16 preset for a brand that wants a top-right badge enabled
export const MY_BRAND_9x16_CANVAS = customizeCanvasPreset('9:16', {
  logoTopLeft: { top: 108, left: 100 },
  logoTopRight: { enabled: true, top: 108, right: 100 },
  contentStage: { top: 260, bottom: 490, left: 90, right: 90 },
  closedCaption: { y: 1480, fontSize: 38, maxWordsPerChunk: 4 },
});
```

---

## 3. Standardized `assets/brand-kit/` Folder Structure

Every brand motion skill (`domains/creative-media/<brand>-brand-motion/`) stores all brand assets inside a standardized **`assets/brand-kit/`** folder so users always know where to drop colors, fonts, logos, design references, sound effects, and voiceover samples:

```text
domains/creative-media/<brand>-brand-motion/
└── assets/
    ├── brand-kit/
    │   ├── README.md                     # Quick-start inventory of where to place every brand file
    │   ├── persona/                      # Brand persona, target audience, tone of voice & script rules
    │   │   ├── README.md
    │   │   └── <brand>-persona.md
    │   ├── guidelines/
    │   │   ├── brand.tokens.json         # Machine-readable hex codes, font names, canvas presets
    │   │   ├── <brand>.brand.starter.ts  # TypeScript BrandTheme & BaseCanvasLayoutSpec
    │   │   └── pdfs/                     # Drop official Brand Guideline PDFs here
    │   ├── fonts/                        # Drop .ttf / .otf / .woff2 font files here
    │   ├── logos/                        # Drop .svg / .png / .jpg logo & avatar files here
    │   ├── graphics/
    │   │   ├── emblems/                  # Center emblem badges & icons (.svg, .png)
    │   │   ├── ui-frames/                # Terminal, browser, or mobile frame templates
    │   │   └── overlays/                 # Sparkles, callouts, cursors
    │   ├── references/
    │   │   ├── videos/                   # Drop reference TikTok / Reels .mp4 videos here
    │   │   └── designs/                  # Drop Figma / .png / .svg slide mockups here
    │   └── audio/
    │       ├── sfx/                      # TikTok / CapCut sound effects (.wav / .mp3)
    │       │   ├── keyboard-typing.wav
    │       │   ├── pop-up.wav
    │       │   ├── whoosh-transition.wav
    │       │   ├── mouse-click.wav
    │       │   ├── progress-ticks.wav
    │       │   └── callout-ding.wav
    │       ├── bgm/                      # Background music loops (.wav / .mp3)
    │       │   └── bgm-ambient.wav
    │       └── voiceover/
    │           ├── talent-samples/       # Drop recorded talent voice samples (.wav) here
    │           │   └── VOICE_RECORDING_GUIDE.md
    │           └── generated/            # Cloned voiceover audio (.wav) + word timestamps (.json)
    └── components/
        └── <Brand>BaseCanvas.starter.tsx # Pre-wired BaseContentCanvas for this brand
```
