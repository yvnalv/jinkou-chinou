# Databro Studio (`@databroid`) — Brand Motion Guidelines & Base Canvas Spec

> **Source Reference**: Extracted from [`@databroid` TikTok (`https://www.tiktok.com/@databroid/video/7633480140214897927`)](https://www.tiktok.com/@databroid/video/7633480140214897927) — *"Databro / Belajar Data Science"*.
> **Brand Isolation Rule**: These tokens, components, and layout rules apply **exclusively** when the user selects the **Databro** brand in `the-motion-designer` or invokes `/databro-brand-motion`. Never mix these tokens into `the-motion-designer` or other brands.

---

## 1. Color Palette (100% Solid Flat Colors — Zero Gradients)

| Token Name | Hex Code | Usage in `@databroid` Videos |
| :--- | :--- | :--- |
| **`backgroundPrimary`** | `#111111` | Full-bleed solid matte charcoal canvas (`RGB(17, 17, 17)`). No gradients, no grid lines, no glow orbs. |
| **`backgroundElevated`** | `#0C0C0C` | Pure terminal window interior background (`Command Prompt` body). |
| **`terminalChrome`** | `#1F1F1F` | Windows Terminal top tab bar (`Command Prompt` tab header). |
| **`textPrimary`** | `#FFFFFF` | Primary headline text, `Databro` brand title, and Closed Captions (CC). |
| **`textSecondary`** | `#B3B3B3` | Sub-label (`Belajar Data Science`) and muted terminal metadata. |
| **`accentPrimary` (Databro Lime)** | `#BFFF72` | Signature Databro lime green (`RGB(191, 255, 114)`). Used for giant display keywords (`Ollama`, `Databro`) and highlighted action terms (`Ketik "Download Ollama"`). |
| **`accentSecondary` (Warm Cream)** | `#F2EBE1` | Signature warm cream circle (`RGB(242, 235, 225)`) used for the avatar circle and central hero emblem circles. |
| **`emblemInk`** | `#111111` | Bold black line-art icon and uppercase label inside the `#F2EBE1` warm cream circle. |
| **`calloutRed`** | `#D92D20` | Solid `3px` red rectangular callout border (`borderRadius: 6px`) highlighting key terminal output or buttons. |

---

## 2. Standard Databro Base Content Canvas (`DatabroBaseCanvas`)

Every Databro video is built on [`assets/DatabroBaseCanvas.starter.tsx`](../assets/DatabroBaseCanvas.starter.tsx) and [`assets/databro.brand.starter.ts`](../assets/databro.brand.starter.ts) (`DATABRO_CANVAS_PRESETS`).

### Persistent Root Layers vs. Transitioning Stage

| Layer | Component / Element | Position on `9:16` (`1080×1920`) | Transition Rule |
| :--- | :--- | :--- | :--- |
| **Layer 0: Canvas** | `#111111` Matte Charcoal | `0, 0, 1080×1920` | **Persistent** — never transitions. |
| **Layer 1: Center Stage** | `<TransitionSeries>` host | `top: 250, bottom: 490, left: 90, right: 90` | **Transitioning** — ONLY this layer runs CapCut smooth transitions (`pop-scale`, `camera-zoom-pan`, `whip-slide`, `implode-out`). |
| **Layer 2: Top-Left Lockup** | [`DatabroLogoLockup`](../assets/DatabroLogoLockup.starter.tsx) | **`top: 108px, left: 100px`** (`64×64px` avatar) | **Persistent** — animates in **only once at `frame 0..12`** of the video, then stays **100% stationary** across all slide transitions. |
| **Layer 3: Closed Captions** | [`DatabroCaptions`](../assets/DatabroCaptions.starter.tsx) | Locked at **`Y = 1480px`** (`left: 110, right: 110`) | **Persistent** — locked at `Y = 1480px` throughout the entire video (`3-frame` opacity cross-fade, **zero vertical movement**). |
| **Layer 4: Audio & SFX** | `<Audio />` + `<Sequence>` | Root audio bus | Plays `bgm-ambient.wav` (`volume: 0.14`), `voiceover.wav`, and frame-accurate TikTok SFX cues. |

### Multi-Platform Aspect Ratio Presets (`DATABRO_CANVAS_PRESETS`)

To duplicate or adapt a Databro video to another platform, pass `aspectRatio="4:5" | "1:1" | "16:9"` to `<DatabroBaseCanvas />` or call `customizeDatabroCanvas()`:

| Aspect Ratio | Resolution | Top-Left Logo `(left, top)` | Centered Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` |
| :--- | :--- | :--- | :--- | :--- |
| **`9:16`** (TikTok / Reels / Shorts) | `1080×1920` | `(100px, 108px)` | `top: 250, bottom: 490, left: 90, right: 90` | **`Y = 1480px`** (`38px` ExtraBold) |
| **`4:5`** (IG / LinkedIn Portrait) | `1080×1350` | `(84px, 72px)` | `top: 180, bottom: 260, left: 84, right: 84` | **`Y = 1140px`** (`34px` ExtraBold) |
| **`1:1`** (Square Feed) | `1080×1080` | `(72px, 56px)` | `top: 150, bottom: 210, left: 72, right: 72` | **`Y = 910px`** (`32px` ExtraBold) |
| **`16:9`** (YouTube / Landscape) | `1920×1080` | `(96px, 64px)` | `top: 160, bottom: 200, left: 140, right: 140` | **`Y = 920px`** (`36px` ExtraBold) |

---

## 3. Authentic `@databroid` Scene Archetypes & Choreography

### Archetype A — Typewriter + Warm Cream Emblem Hook (`00:00–00:08`)
1. **Beat 1 (`frame 0..24`)**: Only the persistent top-left `Databro` lockup, centered white typewriter text with solid block cursor (`█`) + `sfx: 'keyboard-typing'`, and bottom caption at `Y = 1480px` are visible.
2. **Beat 2 (`frame 24..90`)**: Center `#F2EBE1` warm cream circle (`380–400px`) springs in (`scale: 0 -> 1` with `bouncy` spring + `sfx: 'pop-up'`) with 4-point white sparkle burst on the right, followed `4 frames` later by the giant `#BFFF72` lime green keyword (`108–124px` ExtraBold) popping in above `Y = 1480px`.

### Archetype B — Terminal / Browser Step with Camera Zoom & Red Callout
1. **Action Instruction Header**: Centered above the window, `44–50px` Bold `#FFFFFF`, with quoted action keywords in `#BFFF72` lime green (e.g., `Ketik "Download Ollama"` or `1. Run SQL Queries "10x Faster"`).
2. **Window Entry & Camera Zoom**: Window pops in (`sfx: 'pop-up'`), commands type in with `sfx: 'keyboard-typing'`, progress bar fills with `sfx: 'progress-ticks'`, and the camera smoothly zooms (`scale: 1 -> 1.18`) toward the `#D92D20` red callout rectangle (`sfx: 'callout-ding'`).

---

## 4. Brand Kit Storage (`assets/brand-kit/`)

All Databro brand files live in [`assets/brand-kit/README.md`](../assets/brand-kit/README.md):
- Token JSON: [`assets/brand-kit/guidelines/databro.tokens.json`](../assets/brand-kit/guidelines/databro.tokens.json)
- PDF Guidelines: [`assets/brand-kit/guidelines/pdfs/README.md`](../assets/brand-kit/guidelines/pdfs/README.md)
- Fonts: [`assets/brand-kit/fonts/README.md`](../assets/brand-kit/fonts/README.md)
- Logos & Avatar: [`assets/brand-kit/logos/databro-avatar.jpg`](../assets/brand-kit/logos/databro-avatar.jpg) and [`assets/brand-kit/logos/README.md`](../assets/brand-kit/logos/README.md)
- Graphics (Emblems, UI Frames, Overlays): [`assets/brand-kit/graphics/README.md`](../assets/brand-kit/graphics/README.md)
- Reference Videos & Designs: [`assets/brand-kit/references/README.md`](../assets/brand-kit/references/README.md)
- TikTok SFX (`keyboard-typing.wav`, `pop-up.wav`, `whoosh-transition.wav`, `mouse-click.wav`, `progress-ticks.wav`, `callout-ding.wav`) & BGM (`bgm-ambient.wav`): `assets/brand-kit/audio/sfx/` and `assets/brand-kit/audio/bgm/`
- Talent Voice Recording Guide & Generated Voiceovers: [`assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md`](../assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md) and [`assets/brand-kit/audio/voiceover/generated/README.md`](../assets/brand-kit/audio/voiceover/generated/README.md)
