---
name: databro-brand-motion
description: "Databro Studio (@databroid) specialized brand motion skill extending the-motion-designer. Applies Databro's isolated visual identity and Standard Base Content Canvas (DatabroBaseCanvas) for Remotion videos across 9:16, 4:5, 1:1, and 16:9: #111111 solid matte charcoal canvas, #BFFF72 lime green and #F2EBE1 warm cream accents, persistent top-left Databro avatar lockup at (100px, 108px) that animates only on video start, fixed Closed Captions locked at Y=1480px, CapCut smooth transitions, and TikTok SFX/voiceover brand-kit assets. Use when the user selects the Databro brand in the-motion-designer or invokes /databro-brand-motion. Never mix with GLM or other brands."
metadata:
  version: 0.2.0
---

# Databro Brand Motion — `@databroid` Visual Identity & Base Content Canvas

Specialized brand skill extending **`the-motion-designer`** exclusively for **Databro Studio (`@databroid` — "Belajar Data Science")**.

This skill isolates all Databro brand guidelines, colors, typography, logo lockups, sound effects, voiceover samples, and **Standard Base Content Canvas** presets (`9:16`, `4:5`, `1:1`, `16:9`) so they never contaminate `the-motion-designer` or any other brand skill (such as `GLM`).

```text
Confirm Topic & Archetype → Mount <DatabroBaseCanvas> (Persistent Logo + Fixed Y=1480px CC + SFX) → Build <TransitionSeries> Scenes → Validate & Render
```

## When to Use

* Generating TikTok, Instagram Reels, YouTube Shorts, `4:5` Feed, or `16:9` educational data science / AI motion videos for **Databro Studio (`@databroid`)**.
* When the user selects **Databro** during Step 1 of `the-motion-designer`'s Pre-Generation Option Wizard or invokes `/databro-brand-motion`.

Do not use it for: any non-Databro brand (such as GLM or neutral client projects).

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/databro-brand-assets-checklist.md` | Tracking, reviewing, or updating any Databro brand asset (tokens, logos, custom fonts, SFX, BGM, voiceover samples, persona). |
| `references/databro-brand-guidelines.md` | Reviewing Databro Studio's exact color hexes (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), `DATABRO_CANVAS_PRESETS`, persistent layer architecture, and scene archetypes. |
| `references/databro-content-and-voiceover-guide.md` | Prompting `/databro-brand-motion`, structuring tutorial/launch scripts, locking Closed Captions at `Y = 1480px`, mapping TikTok SFX cues, and duplicating the Base Content Canvas across aspect ratios. |
| `assets/brand-kit/README.md` | Inspecting or adding files to the standardized Databro Brand Kit folder (`persona/`, `guidelines/`, `fonts/`, `logos/`, `graphics/`, `references/`, `audio/sfx/`, `audio/bgm/`, `audio/voiceover/`). |
| `assets/brand-kit/persona/README.md` | Storage directory guide for Databro brand persona and tone-of-voice documents. |
| `assets/brand-kit/persona/databro-persona.md` | Databro Studio (`@databroid`) brand persona, Indonesian + English code-switching rules, hook patterns, and audience profile. |
| `assets/brand-kit/guidelines/databro.tokens.json` | Machine-readable Databro color hex tokens, typography stack, and `baseCanvasPresets` (`9:16`, `4:5`, `1:1`, `16:9`). |
| `assets/brand-kit/guidelines/pdfs/README.md` | Storage directory for official Databro Brand Book PDFs. |
| `assets/brand-kit/fonts/README.md` | Storage directory for Databro font files (`.ttf`, `.otf`, `.woff2`). |
| `assets/brand-kit/logos/README.md` | Storage directory guide for Databro logos and avatars. |
| `assets/brand-kit/logos/databro-avatar.jpg` | Official circular warm cream (`#F2EBE1`) illustrated Databro avatar inside `brand-kit/logos/`. |
| `assets/brand-kit/logos/Databro-Logo.png` | Official horizontal Databro logo wordmark. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png` | High-res circular Databro badge revision. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White)-Landscape.png` | High-res landscape Databro white mark revision. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White).png` | High-res Databro white mark revision. |
| `assets/brand-kit/graphics/README.md` | Storage directory for Databro emblem icons, terminal frames, and callout overlays. |
| `assets/brand-kit/graphics/(Reels) Computer Vision (3).png` | Databro Computer Vision slide graphic reference. |
| `assets/brand-kit/graphics/1.png` | Numbered step 1 badge graphic. |
| `assets/brand-kit/graphics/2.png` | Numbered step 2 badge graphic. |
| `assets/brand-kit/graphics/3.png` | Numbered step 3 badge graphic. |
| `assets/brand-kit/graphics/output.png` | Terminal CLI output card reference 1. |
| `assets/brand-kit/graphics/output 2.png` | Terminal CLI output card reference 2. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135828.png` | UI slide reference screenshot 1. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135852.png` | UI slide reference screenshot 2. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135944.png` | UI slide reference screenshot 3. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 140023.png` | UI slide reference screenshot 4. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 140040.png` | UI slide reference screenshot 5. |
| `assets/brand-kit/graphics/Table.png` | Reference data table illustration. |
| `assets/brand-kit/graphics/Untitled design.png` | Slide layout design asset 1. |
| `assets/brand-kit/graphics/Untitled design (1).png` | Slide layout design asset 2. |
| `assets/brand-kit/references/README.md` | Storage directory for reference `@databroid` TikTok `.mp4` videos and `.png`/`.svg` slide designs. |
| `assets/brand-kit/audio/sfx/keyboard-typing.wav` | Mechanical keyboard typing SFX synced to typewriter hooks and terminal commands. |
| `assets/brand-kit/audio/sfx/pop-up.wav` | CapCut bubble pop SFX synced to `#F2EBE1` cream emblem circle and window entries. |
| `assets/brand-kit/audio/sfx/whoosh-transition.wav` | Smooth air whoosh SFX synced to `<TransitionSeries>` slide/zoom transitions. |
| `assets/brand-kit/audio/sfx/mouse-click.wav` | Crisp UI mouse click SFX for button clicks and command execution. |
| `assets/brand-kit/audio/sfx/progress-ticks.wav` | Rapid digital tick SFX while terminal or installer progress bars fill. |
| `assets/brand-kit/audio/sfx/callout-ding.wav` | Subtle harmonic chime SFX when the `#D92D20` red callout rectangle locks onto output. |
| `assets/brand-kit/audio/bgm/bgm-ambient.wav` | Warm `-22 dBFS` ambient synth pad background loop. |
| `assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md` | Databro talent voice recording guide, `48kHz 24-bit Mono WAV` specs, and Indonesian/English calibration script. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 12.m4a` | Databro talent raw reference recording take 12. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 13.m4a` | Databro talent raw reference recording take 13. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 14.m4a` | Databro talent raw reference recording take 14. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 15.m4a` | Databro talent raw reference recording take 15. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 16.m4a` | Databro talent raw reference recording take 16. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 17.m4a` | Databro talent raw reference recording take 17. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 18.m4a` | Databro talent raw reference recording take 18. |
| `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.wav` | Merged master uncompressed 48kHz mono PCM talent reference audio (03:18.45). |
| `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3` | Merged master 192kbps MP3 calibration audio for cloud voice cloning. |
| `assets/brand-kit/audio/voiceover/generated/README.md` | Output directory for cloned voiceover `.wav` tracks and word-level `timestamps.json` files. |
| `assets/databro-avatar.jpg` | Official circular warm cream (`#F2EBE1`) illustrated Databro avatar. |
| `assets/databro.brand.starter.ts` | Importing Databro's isolated TypeScript tokens (`databroBrand`), `DATABRO_CANVAS_PRESETS` (`'9:16'`, `'4:5'`, `'1:1'`, `'16:9'`), and `customizeDatabroCanvas()` helper. |
| `assets/DatabroBaseCanvas.starter.tsx` | Wrapping any Databro video in the 5-layer Standard Base Content Canvas (persistent `#111111` backdrop, persistent top-left logo, fixed `Y = 1480px` CC, `<TransitionSeries>` center stage, and `<Audio>` SFX/BGM/VO bus). |
| `assets/DatabroLogoLockup.starter.tsx` | Rendering the persistent top-left Databro avatar + `Databro` / `Belajar Data Science` lockup (`top: 108px, left: 100px` on `9:16`). |
| `assets/DatabroCaptions.starter.tsx` | Rendering Databro's cardless 2-to-4 word ALL-CAPS ExtraBold white Closed Captions locked at `Y = 1480px` (`9:16`). |
| `assets/generate_databro_cloned_vo.starter.py` | Turnkey voiceover generator supporting ElevenLabs IVC with master calibration audio and offline edge-tts fallback. |

---

## Databro Signature Rules

### 1. Always Ask for Content Archetype & Topic First
* Before generating a new Databro video (unless the user already specified the topic and steps), ask which **Content Archetype** and **Topic** to research and build (`references/databro-content-and-voiceover-guide.md`):
  1. **Step-by-Step Technical Tutorial** (e.g., *"Cara Install Lokal LLM Menggunakan Ollama"*)
  2. **Product / Feature Launch Reel**
  3. **Data Science / AI Concept Explainer**
  4. **Tool / Library Listicle**

### 2. Always Build on `<DatabroBaseCanvas />` (Persistent Chrome vs. Transitioning Stage)
* **Never place `<DatabroLogoLockup />` or `<DatabroCaptions />` inside individual transitioning scenes.**
* Mount [`DatabroBaseCanvas.starter.tsx`](assets/DatabroBaseCanvas.starter.tsx) at the Root Composition level so:
  - **Layer 0 (Canvas)**: Solid `#111111` matte charcoal background stays static.
  - **Layer 1 (Center Stage)**: Symmetric centered `contentStage` (`top: 250, bottom: 490, left: 90, right: 90` on `9:16`) hosts `<TransitionSeries>` with smooth CapCut transitions (`pop-scale`, `camera-zoom-pan`, `whip-slide`, `implode-out`).
  - **Layer 2 (Top-Left Brand Lockup)**: Anchored at **`top: 108px, left: 100px`** (`64×64px` avatar + `Databro` / `Belajar Data Science`). Animates in **only once at `frame 0..12`** of the video and stays **100% stationary** across all slide transitions. Top-right stays completely empty.
  - **Layer 3 (Fixed Closed Captions)**: Locked at **`Y = 1480px`** (`bottom: 400px` on `1080×1920`, `X = 540px` centered). Displays cardless 2-to-4 word ALL-CAPS `#FFFFFF` (`38px` ExtraBold) phrases that switch via a `3-frame` opacity cross-fade with **zero vertical movement**.
  - **Layer 4 (Audio, BGM & TikTok SFX)**: Triggers `keyboard-typing.wav`, `pop-up.wav`, `whoosh-transition.wav`, `mouse-click.wav`, `progress-ticks.wav`, `callout-ding.wav`, and `bgm-ambient.wav` from `brand-kit/audio/`.

### 3. Modifying or Duplicating the Base Content Canvas Across Platforms
* To adapt any Databro video to Instagram Portrait Feed (`'4:5'`), Square (`'1:1'`), or YouTube (`'16:9'`), pass `aspectRatio="4:5" | "1:1" | "16:9"` to `<DatabroBaseCanvas />` or call `customizeDatabroCanvas()` in [`assets/databro.brand.starter.ts`](assets/databro.brand.starter.ts).

### 4. Authentic `@databroid` Scene Archetypes
1. **Archetype A — Typewriter + Warm Cream Emblem Hook (`00:00–00:08` style)**:
   - Starts with **only** the top-left `Databro` lockup, centered white typewriter text (`█` block cursor + `sfx: 'keyboard-typing'`), and bottom caption at `Y = 1480px`.
   - Once typing completes, the `380–400px` **`#F2EBE1` Warm Cream Circle** pops in at center (`sfx: 'pop-up'`) with bold `#111111` line-art icon + 4-point white sparkle burst, followed `4 frames` later by the giant **`#BFFF72` Lime Green** keyword (`108–124px` ExtraBold) right above `Y = 1480px`.
2. **Archetype B — Terminal / Browser Step with Camera Zoom & `#D92D20` Red Callout**:
   - Centered instruction line (`#FFFFFF` verb + `#BFFF72` quoted highlight) above a realistic Windows Terminal (`Command Prompt`, `#0C0C0C` body, `#1F1F1F` tab bar) or browser frame.
   - Commands type in (`sfx: 'keyboard-typing'`), progress bars fill (`sfx: 'progress-ticks'`), camera smoothly zooms into the active area (`sfx: 'whoosh-transition'`), and a **`3px solid #D92D20` red rectangle** locks onto the result (`sfx: 'callout-ding'`).

### 5. Tone of Voice & Pronoun Guardrails ("Kamu/Anda", Never "Lo")
* **Strictly Prohibited**: Never use `"Lo"` / `"Lu"` / `"Loe"` or `"Gue"`.
* **Second-Person Address**: Always use **`"Kamu"`** as the friendly tech-mentor default (*"model ML kamu"*, *"laptop kamu"*, *"biar kamu gak bingung"*), or **`"Anda"`** for formal/enterprise SLA contexts.
* **First-Person Address**: Always use **`"Kita"`** for inclusive tutorial walkthroughs (*"Yuk kita coba"*, *"Kita cek di terminal"*).
* **The "Bro" Salutation**: `"Bro"` is preserved as an energetic brand greeting and closing punctuation (*"Bro, tahu nggak sih..."*, *"Belajar bareng Databro!"*), but never use it as a pronoun substitute for `"lo"`.

### 6. Content Archetype & Style Decision Matrix (Topic-Driven Visual Style)
* The skill must intelligently select the stage layout and visual asset kit according to the topic:
  1. **Code & Tool Walkthrough (`code-walkthrough`)**: For Python, SQL, Git, Pandas, Scikit-Learn. Uses Dark IDE cards (`#191A1B`), Table previews (`assets/brand-kit/graphics/Table.png`), terminal output (`assets/brand-kit/graphics/output.png`), and step badges (`assets/brand-kit/graphics/1.png`, `2.png`, `3.png`).
  2. **Concept & Mental Model (`concept-theory`)**: For Transformer attention, vector databases, neural network theory. Synthesizes `@aibutsimple` dynamic 2D vector diagrams, scatter plot trendlines (`assets/brand-kit/graphics/Untitled design (1).png`), and kinetic keyword highlighting (`#BFFF72`).
  3. **Opinion & Career Editorial (`opinion-editorial`)**: For AI industry news, career guides, tech stack comparisons. Uses kinetic typography, bold metric callouts, and official Databro brandmarks.
  4. **Product Launch (`launch-showcase`)**: For Databro Cloud tools and template announcements. Uses 3D perspective tilt cards and lime `#BFFF72` ambient glow.

### 7. Opening Hook Varieties (Eliminating Visual Monotony)
* Never repeat the exact same opening sequence. Rotate between 4 distinct hook templates:
  - **The Paradox Headline (`paradox-headline`)**: High-contrast question scaling in with `#BFFF72` highlight.
  - **The Code Shock (`code-shock`)**: High accuracy score flashing into a `#D92D20` red overfitting diagnostic.
  - **The Visual Data Spring (`visual-data`)**: Dataframe table or scatter plot springing into the center stage.
  - **The Step Roadmap (`step-roadmap`)**: Numbered step badge roadmap before diving into step 1.

### 8. Cloned Talent Voiceover Pipeline
* Voiceover synthesis utilizes the merged master reference audio:
  - Online IVC: Upload `databro-talent-master-calibration.mp3` or `.wav` via ElevenLabs/Cartesia.
  - Offline Fallback: `edge-tts` (`id-ID-ArdiNeural`) calibrated at normal speaking speed (`rate="+0%"`, ~135 WPM), pitch `+0Hz`, with phonetic pre-processing for English ML terminology.

---

## Definition of Done

* Composition wraps scenes in `<DatabroBaseCanvas />` using `databroBrand` tokens (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`) with zero CSS gradients and zero cross-brand leakage.
* Top-left `Databro / Belajar Data Science` lockup (`top: 108px, left: 100px` on `9:16`) animates only at `frame 0..12` and never transitions between slides.
* Closed Captions are locked at `Y = 1480px` (`9:16`) in cardless 2–4 word ALL-CAPS `#FFFFFF` chunks with zero vertical bounce.
* CapCut smooth transitions and TikTok SFX cues (`keyboard-typing`, `pop-up`, `whoosh-transition`, `mouse-click`, `progress-ticks`, `callout-ding`) are wired.
* `validate_remotion_project.py` from `the-motion-designer` passes with `0 errors`.
