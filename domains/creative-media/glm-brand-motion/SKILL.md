---
name: glm-brand-motion
description: "GLM Systems (glmsystems.com) specialized brand motion skill extending the-motion-designer. Applies GLM's isolated visual identity and Standard Base Content Canvas (GlmBaseCanvas) for Remotion videos across 16:9, 4:5, 9:16, and 1:1: Lime #CDFF70, Emerald #003A40, Stone Grey #444547, and Cool White #F2F0FA, Poppins typography, official GLM Bird logo lockups and Flippy mascot animations, fixed Closed Captions, and enterprise B2B SaaS Remotion compositions. Use when the user selects the GLM brand in the-motion-designer or invokes /glm-brand-motion. Never mix with Databro or other brands."
metadata:
  version: 0.3.0
---

# GLM Brand Motion : GLM Systems (`glmsystems.com`) Visual Identity and Base Content Canvas

Specialized brand skill extending **`the-motion-designer`** exclusively for **GLM Systems (`glmsystems.com`)**.

This skill isolates all GLM Systems brand guidelines, colors, typography, vector logo lockups, sound effects, Flippy AI agent assets, product knowledge for **AI Plus Agent (Globe+ and Synergy)**, and **Standard Base Content Canvas** presets (`16:9`, `4:5`, `9:16`, `1:1`) so they never contaminate `the-motion-designer` or any other brand skill (such as `databro-brand-motion`).

```text
Present Script First -> User Approval -> Mount <GlmBaseCanvas> -> Build <TransitionSeries> (React Icons + Emerald/Lime/Stone Grey) -> Sync Audio Bed & SFX (~116-120 BPM) -> Validate & Render
```

## When to Use

* Generating LinkedIn B2B announcements, YouTube product walkthroughs, or in-app feature explainers for **GLM Systems (`glmsystems.com`)**.
* Introducing or animating **Flippy**, the AI assistant embedded in Exact Globe+ and Exact Synergy.
* Explaining core AI Plus Agent capabilities: Stock Depletion Forecasts, Screen-to-Stock verification, Recode master data renaming, Excel bulk mapping, or Role 501 security.
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
| `references/products/README.md` | Product knowledge directory overview for GLM enterprise add-ons. |
| `references/products/ai-plus-agent-globeplus.md` | Deep specification for Flippy inside Exact Globe+ (ERP). |
| `references/products/ai-plus-agent-synergy.md` | Deep specification for Flippy inside Exact Synergy (Workflow/CRM). |

## Workflow

1. **Script-First Production Gate ("Eerst het script, dan pas bouwen")**:
   - Write and present the complete scene-by-scene script before writing Remotion code (`references/glm-content-and-voiceover-guide.md`).
   - Detail exact on-screen copy, visual movement in one line, and scene start/end timings.
   - Enforce reading times: 0.4s/word, min 2.0s per card, 2.0s post-motion stillness buffer.
   - **Require explicit user approval** before proceeding to code.
2. **Mount `<GlmBaseCanvas />`**: Place the 5-layer canvas shell at the root composition level. Never place logo lockups or captions inside transitioning slide children. Default to `16:9` widescreen for LinkedIn/YouTube or `4:5` portrait for mobile feeds.
3. **Build Slide Scenes in `<TransitionSeries>`**: Create high-contrast cards (`#FFFFFF` surfaces on `#F2F0FA` Cool White) with `#003A40` Emerald headers, `#444547` Stone Grey text, and `#CDFF70` Lime accents.
4. **Use React Icons exclusively**: Source all UI and status icons from `react-icons/lu` (`LuBot`, `LuBuilding2`, `LuShieldCheck`, `LuWorkflow`, `LuDatabase`).
5. **Integrate Real Product Screens and Mascot**: Incorporate bundled UI screens (`menu.png`, `sales.png`, `stock.png`, `email.png`) and position Flippy perching on callout badges. Reference product docs (`references/products/`).
6. **Synchronize Audio Bed & SFX**:
   - Musical character: **Zakelijk, upbeat, gegrond** (~116-120 BPM, calm harmony, active rhythm, FM-Rhodes stabs).
   - Sync tight SFX: `pop` (40ms blip, -8dB), `swoosh` (0.28s noise sweep, -15dB), `ticks` (table waterfall, -18dB), `stijg` (progress bars, -14dB), `ping` (max 2 per video, -14dB).
7. **Ensure Audio-Independent Comprehension**: Verify that all questions, metrics, and takeaways are 100% readable from on-screen graphics with sound muted (LinkedIn standard).
8. **Verify Zero Em-Dashes & Verified Citations**: Ensure zero em-dashes (`—`) across all text, and verify that any statistics have source citations.

## Operating Modes

### Mode A : Storyboard and Safe-Zone Spec
* Generate a structured scene-by-scene script adhering to GLM reading time standards (0.4s/word, min 2.0s per card).
* Define the primary aspect ratio (`16:9` widescreen `1920x1080` default; `4:5` portrait `1080x1350`).
* Map safe zones: Top-left logo at `(72px, 54px)`, top-right `glmsystems.com` at `(72px, 54px)`, and captions locked at `Y = 920px` (`16:9`).

### Mode B : Remotion Component Build
* Implement compositions using `GlmBaseCanvas.starter.tsx` and `glm.brand.starter.ts`.
* Use `<TransitionSeries>` with smooth 12-frame transitions (`slide`, `fade`).
* Style elevated cards with `#FFFFFF` background, `#E5E7EB` border, and `#444547` Stone Grey text.

### Mode C : Timing Repair and Breathing Room
* Eliminate rushed transitions. Enforce 10-frame settle delay after each transition before voiceover audio starts.
* Enforce 12-14 frame silence buffer after voiceover ends before the next slide transitions.
* Set a 24-frame outro hold before video termination.

### Mode D : Brand Guidelines Audit
* Validate colors against `assets/brand-kit/guidelines/glm.tokens.json`:
  - Primary Canvas: `#F2F0FA` Cool White (or full-bleed `#003A40` Emerald for hero beats).
  - Primary Accent Lime: `#CDFF70` (RGB: 205, 255, 112).
  - Signature Emerald: `#003A40` (RGB: 0, 58, 64).
  - Headline & Body Text: `#444547` Stone Grey (RGB: 68, 69, 71).
* Scan for banned elements: Flag any em-dashes (`—`), non-React vector icons, or unauthorized gradients.

### Mode E : Multi-Platform Export
* Export across aspect ratios by switching `aspectRatio="16:9" | "4:5" | "9:16" | "1:1"` on `<GlmBaseCanvas />`.
* Render using Remotion CLI with H.264 MP4 output.

## GLM Signature Rules

### 1. Script-First Approval Gate ("Eerst het script, dan pas bouwen")
* Never jump straight into code for a new video. Always write the scene-by-scene script first with timings, motion descriptions, and full copy. Await user sign-off before rendering.

### 2. Single Idea Per Video & Open with Tension
* Every video focuses on one clear operational improvement.
* Always open with user tension/friction (*"Still clicking through menus to find one sales order?"*), not with the solution.
* Split conclusion: Present the core memorable takeaway on its own scene first, followed by a clean static endcard.

### 3. Always Build on `<GlmBaseCanvas />` (Persistent Chrome vs. Transitioning Stage)
* **Never place `<GlmLogoLockup />` or `<GlmCaptions />` inside individual transitioning scenes.**
* Mount [`GlmBaseCanvas.starter.tsx`](assets/GlmBaseCanvas.starter.tsx) at the root level:
  - **Layer 0 (Canvas)**: Solid `#F2F0FA` Cool White (or `#003A40` Emerald for hero cards) stays static.
  - **Layer 1 (Center Stage)**: Centered `contentStage` (`top: 140, bottom: 160, left: 100, right: 100` on `16:9`) hosts `<TransitionSeries>`.
  - **Layer 2A (Top-Left Lockup)**: Anchored at **`top: 54px, left: 72px`** on `16:9` (`GlmLogoLockup`). Animates only on `frame 0..12` and remains stationary.
  - **Layer 2B (Top-Right Website)**: Anchored at **`top: 54px, right: 72px`** (`glmsystems.com` in `#003A40`, `22px` Bold).
  - **Layer 3 (Fixed Closed Captions)**: Locked at **`Y = 920px`** on `16:9` (or `Y = 1140px` on `4:5`). Displays cardless ALL-CAPS `#444547` (or `#F2F0FA` on dark) phrases with zero vertical movement.
  - **Layer 4 (Audio, BGM and SFX)**: Controls `bgm-ambient.wav` and synchronized SFX cues (`pop-up.wav`, `whoosh-transition.wav`, `keyboard-typing.wav`, `mouse-click.wav`, `callout-ding.wav`).

### 4. Vector Icons Standard : React Icons as Single Source of Truth
* **Strict Ban**: Never use generic AI clipart, emojis, or arbitrary SVG doodles.
* **Standard**: Exclusively use **React Icons** (`react-icons` package: `react-icons/lu` Lucide, `react-icons/tb` Tabler, `react-icons/fi` Feather).
* Standard GLM Icons:
  - ERP & Architecture: `LuBuilding2` / `LuDatabase`
  - Flippy & AI Automation: `LuBot` / `LuSparkles`
  - Enterprise Security & Trust: `LuShieldCheck` / `LuLock`
  - Workflow & Synergy: `LuWorkflow` / `LuLayers`
  - Action & Email: `LuMail` / `LuSend` / `LuCheckCircle`
  - Navigation & Arrows: `LuArrowRight` / `LuSearch`

### 5. Absolute Ban on Em-Dashes (`—`) Across Writing and Closed Captions
* **Strict Rule**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in video titles, slides, code comments, Closed Captions, or scripts.
* Use colons (`:`), arrows (`->`), hyphens (`-`), or clean whitespace instead (e.g., `Meet Flippy : Your AI assistant embedded in Exact Globe+`, `ERP Automation -> Real-time sync`).

### 6. Reading Pacing Rules (GLM Minimum Time Standard)
* **Per Spoken / Written Word**: Minimum `0.4 seconds` per word.
* **Per Text Block Entry**: Minimum `0.5 seconds` initial eye landing buffer.
* **Minimum per Text Card**: **`2.0 seconds`** minimum on-screen visibility.
* **Stillness Buffer after Motion**: **`2.0 seconds`** visual stillness before scene transition.
* **Outro Endcard**: **`2.5 seconds`** minimum hold for GLM logo and website URL.

### 7. Official Brand Colors (Source of Truth)
* **Lime (Primary)**: `#CDFF70` | RGB: `205, 255, 112` (energy, motion, AI innovation, dual birds logo).
* **Emerald**: `#003A40` | RGB: `0, 58, 64` (trust, technological depth, badges, hero cards).
* **Stone Grey**: `#444547` | RGB: `68, 69, 71` (primary text, headlines, subtle borders).
* **Cool White**: `#F2F0FA` | RGB: `242, 240, 250` (spacious canvas background).
* **Pure White**: `#FFFFFF` (elevated card surface).

### 8. Audio Brand Identity (Zakelijk, Upbeat, Gegrond)
* **BGM Character**: Professional, driving, grounded (~116-120 BPM). No dreamy or sleepy ambient beds; calm harmonies with active rhythmic drive.
* **SFX Precision**: Place SFX at the exact visual landing frame (`pop` for cards, `swoosh` for slides, `ticks` for tables, `stijg` for counters, max 2 `ping` accents per video).

### 9. Product Knowledge Specialization
* Reference [`references/products/ai-plus-agent-globeplus.md`](references/products/ai-plus-agent-globeplus.md) for Exact Globe+ features: Role 501 permissions, 5 layout modes, 10 feature pillars (stock depletion horizon, screen reader, recode, transaction confirmation, Excel import).
* Reference [`references/products/ai-plus-agent-synergy.md`](references/products/ai-plus-agent-synergy.md) for Exact Synergy features: Request automation (leave, tasks, approvals), CRM accounts, colleague search, quotation lines, document summarization, voice input, slash commands.

---

## Definition of Done

* Scene-by-scene script presented and approved before writing Remotion code.
* Composition wraps scenes in `<GlmBaseCanvas />` using `glmBrand` tokens (`#CDFF70`, `#003A40`, `#444547`, `#F2F0FA`, `#FFFFFF`) with zero gradients and zero cross-brand leakage.
* Top-left GLM logo lockup (`top: 54px, left: 72px` on `16:9`) and top-right `glmsystems.com` are persistent outside the transition stage.
* Closed Captions are locked at `Y = 920px` (`16:9`) or `Y = 1140px` (`4:5`) in cardless ALL-CAPS text with zero vertical bounce and zero em-dashes.
* All icons are exclusively sourced from **React Icons** (`react-icons/lu`, `react-icons/tb`, `react-icons/fi`).
* Timing enforces 0.4s/word reading pace, minimum 2.0s card visibility, 10-frame post-transition settle delay, and 14-frame tail silence buffer.
* Video is 100% understandable on mute for LinkedIn viewers.
* `python tools/skills.py validate glm-brand-motion` passes with `0 errors, 0 warnings`.
