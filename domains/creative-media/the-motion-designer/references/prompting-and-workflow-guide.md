# How to Use, Prompt & Generate Content with `the-motion-designer`

This guide explains how to use `the-motion-designer` and its isolated brand skills (such as `databro-brand-motion`) to plan, script, voice, animate, and render social media motion graphics with Remotion.

---

## 1. End-to-End Content Generation Workflow

```text
[Step 1: Discovery & Topic Intake]
   Choose Brand Skill + Content Archetype + Platform Aspect Ratio ('9:16', '4:5', '1:1', '16:9')
          │
          ▼
[Step 2: Mode A — Storyboard & Audio Spec (STORYBOARD_SPEC.md)]
   Define frame budget, voiceover script, 2-4 word CC chunks (locked at Y=1480px),
   CapCut transitions, and TikTok SFX cue frames. (Requires User Approval Gate)
          │
          ▼
[Step 3: Mode B — Scaffold on Standard Base Content Canvas]
   Copy brand-kit assets (logos, fonts, SFX, voiceover) into public/brand-kit/.
   Mount <BaseContentCanvas> at root and build center-stage scenes inside <TransitionSeries>.
          │
          ▼
[Step 4: Mode C & D — Determinism Audit & Render]
   Run validate_remotion_project.py (0 errors) -> Render preview stills & final MP4/WebM/ProRes.
```

---

## 2. Content Archetypes Supported

When starting a new video, specify which **Content Archetype** you want to generate:

1. **Step-by-Step Technical Tutorial (e.g., `@databroid` TikTok Style)**
   - **Structure**: Typewriter Hook + Emblem Circle (`00:00–00:08`) -> Tool/Model Intro Card (`00:08–00:14`) -> Numbered Browser / Installer / Command Prompt Steps with Zoom-In & Red Callout Boxes (`#D92D20`) -> Final Working Demo & CTA.
2. **Product / Feature Launch Reel (`15s–30s`)**
   - **Structure**: Problem/Hook -> 3 Key Highlights with live terminal benchmarks or UI frames -> Emblem CTA Outro.
3. **Data Science / Engineering Concept Explainer (`30s–60s`)**
   - **Structure**: Visual Hook Question -> Architecture / Pipeline Diagram Comparison -> Code/CLI Proof -> Key Takeaway Summary.
4. **Fast Listicle / Tool Roundup (`15s–45s`)**
   - **Structure**: Hook ("3 Tools Every Data Engineer Needs") -> Tool 1 Emblem + Demo -> Tool 2 Emblem + Demo -> Tool 3 Emblem + Demo -> Save/Follow CTA.

---

## 3. Copy-Paste Prompt Templates

### Template A — Step-by-Step Tutorial Video (`@databroid` TikTok Style)
```text
/databro-brand-motion Create a [30-second / 60-second] TikTok & Instagram Reels (9:16, 1080x1920, 30fps) tutorial video on:
Topic: "[Insert Topic, e.g., Cara Install Lokal LLM Menggunakan Ollama]"
Steps to show on screen:
1. [Step 1, e.g., Search & Download installer from official website with red callout box]
2. [Step 2, e.g., Run installer progress bar to 100%]
3. [Step 3, e.g., Open Command Prompt and verify version with red callout box]
4. [Step 4, e.g., Run the model and show live chat response]
Use the Databro Base Content Canvas with fixed top-left Databro logo (no transition between slides), fixed Closed Captions at Y=1480px, CapCut smooth zoom/pop transitions, and TikTok SFX (keyboard typing, pop-up, whoosh, mouse click, progress ticks, callout ding).
```

### Template B — Product / Feature Launch Reel
```text
/the-motion-designer Create a 15-second vertical launch video (9:16, 30fps) using the [Databro / Custom] brand profile for "[Product Name]" highlighting:
1. "[Highlight 1 + Metric/Command]"
2. "[Highlight 2 + Metric/Command]"
3. "[Highlight 3 + Metric/Command]"
Use the Standard Base Content Canvas with persistent top-left logo, fixed bottom Closed Captions, CapCut transitions, and TikTok sound effects.
```

### Template C — Multi-Platform Aspect Ratio Duplication
```text
/the-motion-designer Duplicate the existing [CompositionName] video onto the '4:5' (1080x1350 Instagram Feed) and '16:9' (1920x1080 YouTube) Base Content Canvas presets so the top-left logo, centered stage, and fixed Closed Captions adapt automatically, then render all 3 formats.
```

---

## 4. How to Customize a Brand's Base Content Canvas

If you ever want to adjust a brand's background color, logo coordinates, or closed caption position across **every** video at once:

1. Open `domains/creative-media/<brand>-brand-motion/assets/brand-kit/guidelines/<brand>.brand.starter.ts` (or `src/brands/<brand>.brand.ts` in your Remotion project).
2. Edit `canvasPresets['9:16']` (or `'4:5'`, `'1:1'`, `'16:9'`):
   - `logoTopLeft: { top: 108, left: 100 }` — moves the persistent top-left brand lockup.
   - `closedCaption: { y: 1480, fontSize: 38 }` — moves the locked Closed Caption line.
   - `contentStage: { top: 250, bottom: 490, left: 90, right: 90 }` — resizes the symmetric centered stage where `<TransitionSeries>` slides render.
3. Because every scene renders inside `<BaseContentCanvas>`, all scenes inherit the updated coordinates immediately with zero per-scene edits.

