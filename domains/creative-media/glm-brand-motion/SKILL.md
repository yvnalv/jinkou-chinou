---
name: glm-brand-motion
description: "GLM Systems (glmsystems.com) specialized brand motion skill extending the-motion-designer. Applies GLM's isolated visual identity and Standard Base Content Canvas (GlmBaseCanvas) for Remotion videos across 16:9, 4:5, 9:16, and 1:1: #003A40 Emerald, #CDFF70 Lime, #F1F0FA Cool White, Poppins typography, official GLM Bird logo lockups and Flippy mascot animations, fixed Closed Captions, and enterprise B2B SaaS Remotion compositions. Use when the user selects the GLM brand in the-motion-designer or invokes /glm-brand-motion. Never mix with Databro or other brands."
metadata:
  version: 0.1.0
---

# GLM Brand Motion : GLM Systems (`glmsystems.com`) Visual Identity and Base Content Canvas

Specialized brand skill extending **`the-motion-designer`** exclusively for **GLM Systems (`glmsystems.com`)**.

This skill isolates all GLM Systems brand guidelines, colors, typography, vector logo lockups, sound effects, Flippy AI agent assets, and **Standard Base Content Canvas** presets (`16:9`, `4:5`, `9:16`, `1:1`) so they never contaminate `the-motion-designer` or any other brand skill (such as `databro-brand-motion`).

```text
Confirm Topic & Archetype -> Mount <GlmBaseCanvas> (Persistent Logo + Fixed Y=920px CC + SFX) -> Build <TransitionSeries> Scenes (React Icons + Emerald/Lime Cards) -> Calibrate Enterprise Voiceover (135 WPM) -> Validate & Render
```

## When to Use

* Generating LinkedIn B2B announcements, YouTube product walkthroughs, or in-app feature explainers for **GLM Systems (`glmsystems.com`)**.
* Introducing or animating **Flippy**, the AI assistant embedded in Exact Globe+ and Exact Synergy.
* Building high-contrast ERP workflow, sales order management, stock verification, or Synergy Kanban motion graphics.
* When the user selects **GLM** during Step 1 of `the-motion-designer`'s Pre-Generation Option Wizard or invokes `/glm-brand-motion`.

Do not use it for: Databro Studio (`@databroid`) projects (use `databro-brand-motion`) or generic, brand-agnostic video generation (use `the-motion-designer`).

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `assets/GlmBaseCanvas.starter.tsx` | Standard 5-layer Base Content Canvas preset component across aspect ratios. |
| `assets/GlmCaptions.starter.tsx` | Fixed Y Closed Captions component locked at Y = 920px (16:9) or Y = 1140px (4:5). |
| `assets/GlmLogoLockup.starter.tsx` | Persistent top-left GLM bird logo lockup animating once at frame 0..12. |
| `assets/glm.brand.starter.ts` | Isolated TypeScript brand tokens, color palette, and canvas geometry presets. |
| `assets/brand-kit/README.md` | Directory overview for the GLM Systems brand kit assets. |
| `assets/brand-kit/audio/bgm/bgm-ambient.wav` | Royalty-free warm ambient synth pad background music loop. |
| `assets/brand-kit/audio/sfx/callout-ding.wav` | Subtle harmonic chime SFX for highlight callouts and card arrivals. |
| `assets/brand-kit/audio/sfx/keyboard-typing.wav` | Mechanical typing SFX for terminal prompts and typewriter text. |
| `assets/brand-kit/audio/sfx/mouse-click.wav` | Crisp UI mouse click SFX for button triggers and user actions. |
| `assets/brand-kit/audio/sfx/pop-up.wav` | Clean UI pop SFX for modal windows and badge entries. |
| `assets/brand-kit/audio/sfx/progress-ticks.wav` | Digital tick SFX for loading bars and metric counters. |
| `assets/brand-kit/audio/sfx/whoosh-transition.wav` | Smooth air whoosh SFX for slide and whip transitions. |
| `assets/brand-kit/graphics/README.md` | Directory documentation for product interface screenshots. |
| `assets/brand-kit/graphics/email.png` | Flippy drafted email action popup screenshot. |
| `assets/brand-kit/graphics/menu.png` | Exact Globe+ purchase and sales menu screen. |
| `assets/brand-kit/graphics/sales.png` | Exact Globe+ sales orders table screen. |
| `assets/brand-kit/graphics/stock.png` | Exact Globe+ warehouse stock verification screen. |
| `assets/brand-kit/guidelines/glm.tokens.json` | Machine-readable color hex tokens, typography, and canvas presets. |
| `assets/brand-kit/logos/GLM-BIRD-Color.svg` | Official dual lime birds brandmark vector SVG. |
| `assets/brand-kit/logos/GLM-black-Text-Color-Bird.svg` | Official horizontal lockup vector SVG (dark wordmark with lime bird). |
| `assets/brand-kit/logos/README.md` | Vector logos directory overview and clear-space rules. |
| `assets/brand-kit/persona/README.md` | Directory overview for GLM brand voice and persona. |
| `assets/brand-kit/persona/glm-persona.md` | B2B enterprise persona, Flippy agent narrative, and tone guidelines. |
| `assets/brand-kit/references/README.md` | Directory documentation for campaign references. |
| `assets/brand-kit/references/flippy-video-script.md` | Authentic Flippy launch video production script and storyboard. |
| `references/glm-brand-assets-checklist.md` | Actionable tracking checklist for all GLM brand kit assets. |
| `references/glm-brand-guidelines.md` | Visual identity spec, color palette, typography, and React Icons rules. |
| `references/glm-content-and-voiceover-guide.md` | Content archetypes, pacing standards, and voiceover guidelines. |

## Workflow

1. **Confirm Topic, Archetype, and Platform**: Determine if creating Archetype A (Flippy launch), Archetype B (Synergy workflow demo), or Archetype C (feature release). Default to `16:9` widescreen for LinkedIn/YouTube or `4:5` portrait for mobile feeds.
2. **Mount `<GlmBaseCanvas />`**: Place the 5-layer canvas shell at the root composition level. Never place logo lockups or captions inside transitioning slide children.
3. **Build Slide Scenes in `<TransitionSeries>`**: Create high-contrast cards (`#FFFFFF` surfaces on `#F1F0FA` Cool White) with `#003A40` Emerald headers and `#CDFF70` Lime accents.
4. **Use React Icons exclusively**: Source all UI and status icons from `react-icons/lu` (`LuBot`, `LuBuilding2`, `LuShieldCheck`, `LuWorkflow`, `LuDatabase`).
5. **Integrate Real Product Screens and Mascot**: Incorporate bundled UI screens (`menu.png`, `sales.png`, `stock.png`, `email.png`) and position Flippy perching on callout badges.
6. **Enforce Breathing Room and Timing**: Ensure 0.4s/word reading pace, minimum 2.0s card visibility, 10-frame post-transition settle delay, and 14-frame tail silence buffer.
7. **Verify Zero Em-Dashes**: Scan all headlines, body text, code snippets, and Closed Captions to ensure zero em-dashes (`—`).

## Operating Modes

### Mode A : Storyboard and Safe-Zone Spec
* Generate a structured scene-by-scene script adhering to GLM reading time standards (0.4s/word, min 2.0s per card).
* Define the primary aspect ratio (`16:9` widescreen `1920x1080` default; `4:5` portrait `1080x1350`).
* Map safe zones: Top-left logo at `(72px, 54px)`, top-right `glmsystems.com` at `(72px, 54px)`, and captions locked at `Y = 920px` (`16:9`).

### Mode B : Remotion Component Build
* Implement compositions using `GlmBaseCanvas.starter.tsx` and `glm.brand.starter.ts`.
* Use `<TransitionSeries>` with smooth 12-frame transitions (`slide`, `fade`).
* Style elevated cards with `#FFFFFF` background, `#E5E7EB` border, and `#111827` Charcoal text.

### Mode C : Timing Repair and Breathing Room
* Eliminate rushed transitions. Enforce 10-frame settle delay after each transition before voiceover audio starts.
* Enforce 12-14 frame silence buffer after voiceover ends before the next slide transitions.
* Set a 24-frame outro hold before video termination.

### Mode D : Brand Guidelines Audit
* Validate colors against `assets/brand-kit/guidelines/glm.tokens.json`:
  - Primary Canvas: `#F1F0FA` Cool White (or full-bleed `#003A40` Emerald for hero beats).
  - Accent Lime: `#CDFF70`.
  - Accent Emerald: `#003A40`.
  - Headline Text: `#111827`.
* Scan for banned elements: Flag any em-dashes (`—`), non-React vector icons, or unauthorized gradients.

### Mode E : Multi-Platform Export
* Export across aspect ratios by switching `aspectRatio="16:9" | "4:5" | "9:16" | "1:1"` on `<GlmBaseCanvas />`.
* Render using Remotion CLI with H.264 MP4 output.

## GLM Signature Rules

### 1. Always Ask for Content Archetype and Topic First
* Before generating a new GLM video (unless specified by the user), confirm the **Content Archetype** (`references/glm-content-and-voiceover-guide.md`):
  1. **Archetype A : "Flippy" AI Agent Launch and Explainer** (45-65s: Problem tension in Exact Globe+, Flippy arrives, data context demo, action confirmation, trust anchor).
  2. **Archetype B : Exact Synergy Workflow Solution Demo** (30-45s: Automated task routing, Kanban efficiency, zero manual entry).
  3. **Archetype C : B2B Feature Release Stinger** (15-30s: Fast announcement of new ERP connector or AI capability).

### 2. Always Build on `<GlmBaseCanvas />` (Persistent Chrome vs. Transitioning Stage)
* **Never place `<GlmLogoLockup />` or `<GlmCaptions />` inside individual transitioning scenes.**
* Mount [`GlmBaseCanvas.starter.tsx`](assets/GlmBaseCanvas.starter.tsx) at the root level:
  - **Layer 0 (Canvas)**: Solid `#F1F0FA` Cool White (or `#003A40` Emerald for hero cards) stays static.
  - **Layer 1 (Center Stage)**: Centered `contentStage` (`top: 140, bottom: 160, left: 100, right: 100` on `16:9`) hosts `<TransitionSeries>`.
  - **Layer 2A (Top-Left Lockup)**: Anchored at **`top: 54px, left: 72px`** on `16:9` (`GlmLogoLockup`). Animates only on `frame 0..12` and remains stationary.
  - **Layer 2B (Top-Right Website)**: Anchored at **`top: 54px, right: 72px`** (`glmsystems.com` in `#003A40`, `22px` Bold).
  - **Layer 3 (Fixed Closed Captions)**: Locked at **`Y = 920px`** on `16:9` (or `Y = 1140px` on `4:5`). Displays cardless ALL-CAPS `#111827` (or `#F1F0FA` on dark) phrases with zero vertical movement.
  - **Layer 4 (Audio, BGM and SFX)**: Controls `bgm-ambient.wav` and synchronized SFX cues (`pop-up.wav`, `whoosh-transition.wav`, `keyboard-typing.wav`, `mouse-click.wav`, `callout-ding.wav`).

### 3. Vector Icons Standard : React Icons as Single Source of Truth
* **Strict Ban**: Never use generic AI clipart, emojis, or arbitrary SVG doodles.
* **Standard**: Exclusively use **React Icons** (`react-icons` package: `react-icons/lu` Lucide, `react-icons/tb` Tabler, `react-icons/fi` Feather).
* Standard GLM Icons:
  - ERP & Architecture: `LuBuilding2` / `LuDatabase`
  - Flippy & AI Automation: `LuBot` / `LuSparkles`
  - Enterprise Security & Trust: `LuShieldCheck` / `LuLock`
  - Workflow & Synergy: `LuWorkflow` / `LuLayers`
  - Action & Email: `LuMail` / `LuSend` / `LuCheckCircle`
  - Navigation & Arrows: `LuArrowRight` / `LuSearch`

### 4. Absolute Ban on Em-Dashes (`—`) Across Writing and Closed Captions
* **Strict Rule**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in video titles, slides, code comments, Closed Captions, or scripts.
* Use colons (`:`), arrows (`->`), hyphens (`-`), or clean whitespace instead (e.g., `Meet Flippy : Your AI agent inside Exact Globe+`, `ERP Automation -> Real-time sync`).

### 5. Reading Pacing Rules (GLM Minimum Time Standard)
* **Per Spoken / Written Word**: Minimum `0.4 seconds` per word.
* **Per Text Block Entry**: Minimum `0.5 seconds` initial eye landing buffer.
* **Minimum per Text Card**: **`2.0 seconds`** minimum on-screen visibility.
* **Stillness Buffer after Motion**: **`2.0 seconds`** visual stillness before scene transition.
* **Outro Endcard**: **`2.5 seconds`** minimum hold for GLM logo and website URL.

### 6. Audio-Visual Transition Timing and Breathing Room
* **Post-Transition Settle Buffer (Head Delay = `10-12 frames`)**:
  - Visual slide enters and completes transition.
  - Visual stillness buffer runs for `10-12 frames` (~0.35s).
  - Speech begins only *after* the incoming slide settles.
* **Pre-Transition Speech Silence Buffer (Tail Delay = `12-14 frames`)**:
  - Voiceover finishes speaking.
  - Scene holds in quiet stillness for `12-14 frames` (~0.40s) before the next transition starts.
* **Outro Tail Hold (`24 frames`)**:
  - Hold for 24 frames after speech ends before terminating the video.

### 7. Authentic GLM Color Palette and Zero Gradients
* **Canvas Backdrop**: `#F1F0FA` (Cool White) for standard scenes; `#003A40` (Emerald) for high-impact hero moments.
* **Signature Accent**: `#CDFF70` (Lime Green) for the GLM bird mark and interactive keyword callouts.
* **Deep Architectural Accent**: `#003A40` (Emerald) for badges, dark cards, and high-contrast text blocks.
* **Surface Card**: `#FFFFFF` (Pure White) with `#E5E7EB` subtle border and `16px` border-radius.
* **Typography**: Poppins (Display and Headings) and Geist/Inter for clean body copy.

### 8. Enterprise B2B Voiceover Calibration
* Voice Profile: `en-US-AndrewNeural` or `en-GB-RyanNeural` (calm, authoritative, executive cadence) for global content; `nl-NL-MaartenNeural` for Dutch enterprise campaigns.
* Cadence: Normal speaking pace (`rate="+0%"` to `"-2%"`, ~130-140 WPM).

---

## Definition of Done

* Composition wraps scenes in `<GlmBaseCanvas />` using `glmBrand` tokens (`#F1F0FA`, `#003A40`, `#CDFF70`, `#FFFFFF`, `#111827`) with zero gradients and zero cross-brand leakage.
* Top-left GLM logo lockup (`top: 54px, left: 72px` on `16:9`) and top-right `glmsystems.com` are persistent outside the transition stage.
* Closed Captions are locked at `Y = 920px` (`16:9`) or `Y = 1140px` (`4:5`) in cardless ALL-CAPS text with zero vertical bounce and zero em-dashes.
* All icons are exclusively sourced from **React Icons** (`react-icons/lu`, `react-icons/tb`, `react-icons/fi`).
* Timing enforces 0.4s/word reading pace, minimum 2.0s card visibility, 10-frame post-transition settle delay, and 14-frame tail silence buffer.
* Video adheres to Flippy AI Agent narrative guidelines ("Works within your rights. Never around them.").
* `python tools/skills.py validate glm-brand-motion` passes with `0 errors, 0 warnings`.
