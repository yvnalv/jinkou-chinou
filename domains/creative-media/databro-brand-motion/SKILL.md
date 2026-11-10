---
name: databro-brand-motion
description: "Databro Studio (@databroid / @databro.id) specialized brand motion skill extending the-motion-designer. Applies Databro's isolated visual identity and Standard Base Content Canvas (DatabroBaseCanvas) for Remotion videos across 9:16, 4:5, 1:1, and 16:9: #121212 matte charcoal canvas, white body text, #BB86FC lavender question headlines, #03DAC6 teal and #C1FF72 lime accents, left-aligned slide layouts, React Icons (react-icons/lu) as strict vector source of truth, persistent top-left Databro avatar lockup and top-right @databro.id, fixed Closed Captions locked at Y=1480px, absolute ban on em-dashes, CapCut smooth transitions with 10-frame settle delay, and calibrated baritone voiceover with synced caption timings. Covers tutorials, concept explainers, tool listicles, launch reels, and career opinion videos. Use when the user selects the Databro brand in the-motion-designer or invokes /databro-brand-motion. Never mix with GLM or other brands."
metadata:
  version: 0.4.0
---

# Databro Brand Motion : `@databroid` Visual Identity and Base Content Canvas

Specialized brand skill extending **`the-motion-designer`** exclusively for **Databro Studio (`@databroid` / `@databro.id` : "Belajar Data Science")**.

This skill isolates all Databro brand guidelines, colors, typography, logo lockups, sound effects, voiceover samples, and **Standard Base Content Canvas** presets (`9:16`, `4:5`, `1:1`, `16:9`) so they never contaminate `the-motion-designer` or any other brand skill (such as `GLM`).

```text
Confirm Topic & Archetype -> Mount <DatabroBaseCanvas> (Persistent Logo + Fixed Y=1480px CC + SFX) -> Generate Per-Scene Voiceover + Caption Timings (pitch -4Hz) -> Build Left-Aligned <TransitionSeries> Scenes (React Icons + #BB86FC Lavender Headlines) -> Validate & Render
```

## When to Use

* Generating TikTok, Instagram Reels, YouTube Shorts, `4:5` Feed, or `16:9` educational data science / AI motion videos for **Databro Studio (`@databroid`)**.
* When the user selects **Databro** during Step 1 of `the-motion-designer`'s Pre-Generation Option Wizard or invokes `/databro-brand-motion`.

Do not use it for: any non-Databro brand (such as GLM or neutral client projects).

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `assets/DatabroBaseCanvas.starter.tsx` | Standard 5-layer Base Content Canvas preset component across aspect ratios. |
| `assets/DatabroCaptions.starter.tsx` | Cardless ALL-CAPS Closed Captions locked at Y = 1480px on 9:16. |
| `assets/DatabroLogoLockup.starter.tsx` | Persistent top-left Databro avatar lockup animating only on frame 0..12. |
| `assets/brand-kit/README.md` | Directory overview for the standardized Databro brand kit assets. |
| `assets/brand-kit/audio/bgm/bgm-ambient.wav` | Warm ambient synth pad background music loop. |
| `assets/brand-kit/audio/sfx/callout-ding.wav` | Subtle harmonic chime SFX for red callout borders. |
| `assets/brand-kit/audio/sfx/keyboard-typing.wav` | Mechanical keyboard typing SFX for typewriter text and code. |
| `assets/brand-kit/audio/sfx/mouse-click.wav` | Crisp UI mouse click SFX for buttons and interactions. |
| `assets/brand-kit/audio/sfx/pop-up.wav` | CapCut bubble pop SFX for cream emblems and window entries. |
| `assets/brand-kit/audio/sfx/progress-ticks.wav` | Rapid digital tick SFX while progress bars fill. |
| `assets/brand-kit/audio/sfx/whoosh-transition.wav` | Smooth air whoosh SFX for slide and zoom transitions. |
| `assets/brand-kit/audio/voiceover/generated/README.md` | Output directory for generated voiceover audio and timestamp files. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 12.m4a` | Raw talent reference voice recording take 12. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 13.m4a` | Raw talent reference voice recording take 13. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 14.m4a` | Raw talent reference voice recording take 14. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 15.m4a` | Raw talent reference voice recording take 15. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 16.m4a` | Raw talent reference voice recording take 16. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 17.m4a` | Raw talent reference voice recording take 17. |
| `assets/brand-kit/audio/voiceover/talent-samples/Gang Haji Nasim 18.m4a` | Raw talent reference voice recording take 18. |
| `assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md` | Talent voice recording instructions, F0 = 86Hz specs, and calibration scripts. |
| `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3` | Merged 192kbps MP3 calibration audio for cloud voice cloning. |
| `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.wav` | Master uncompressed 48kHz mono PCM talent reference audio (03:18.45). |
| `assets/brand-kit/fonts/README.md` | Directory for custom brand typography files (.ttf, .otf, .woff2). |
| `assets/brand-kit/graphics/(Reels) Computer Vision (3).png` | Reference graphic slide for Computer Vision topics. |
| `assets/brand-kit/graphics/1.png` | Numbered step 1 badge icon graphic. |
| `assets/brand-kit/graphics/2.png` | Numbered step 2 badge icon graphic. |
| `assets/brand-kit/graphics/3.png` | Numbered step 3 badge icon graphic. |
| `assets/brand-kit/graphics/README.md` | Storage directory for emblems, step badges, and frame overlays. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135828.png` | Slide reference screenshot 1. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135852.png` | Slide reference screenshot 2. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 135944.png` | Slide reference screenshot 3. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 140023.png` | Slide reference screenshot 4. |
| `assets/brand-kit/graphics/Screenshot 2026-04-25 140040.png` | Slide reference screenshot 5. |
| `assets/brand-kit/graphics/Table.png` | Reference data table illustration graphic. |
| `assets/brand-kit/graphics/Untitled design (1).png` | Scatter plot and regression trendline design asset. |
| `assets/brand-kit/graphics/Untitled design.png` | Slide graphic layout reference asset. |
| `assets/brand-kit/graphics/output 2.png` | Terminal CLI output card reference 2. |
| `assets/brand-kit/graphics/output.png` | Terminal CLI output card reference 1. |
| `assets/brand-kit/guidelines/databro.tokens.json` | Machine-readable color hex tokens, typography, and canvas presets. |
| `assets/brand-kit/guidelines/pdfs/README.md` | Storage directory for brand book PDF documents. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png` | High-resolution circular Databro emblem mark. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White)-Landscape.png` | High-resolution landscape white Databro wordmark. |
| `assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White).png` | High-resolution white Databro brandmark. |
| `assets/brand-kit/logos/Databro-Logo.png` | Horizontal Databro brandmark logo. |
| `assets/brand-kit/logos/README.md` | Directory for official Databro logos and brandmarks. |
| `assets/brand-kit/logos/databro-avatar.jpg` | Official circular warm cream illustrated Databro avatar. |
| `assets/brand-kit/persona/README.md` | Directory for brand persona and tone documentation. |
| `assets/brand-kit/persona/databro-persona.md` | Official Databro Studio brand voice, persona, and wording rules. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/1.png` | Reference carousel slide 1 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/2.png` | Reference carousel slide 2 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/3.png` | Reference carousel slide 3 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/4.png` | Reference carousel slide 4 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/5.png` | Reference carousel slide 5 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/6.png` | Reference carousel slide 6 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) Korelasi vs Kasualitas/7.png` | Reference carousel slide 7 for Korelasi vs Kausalitas. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/1.png` | Reference carousel slide 1 for Train/Val/Test Split. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/2.png` | Reference carousel slide 2 for Train/Val/Test Split. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/3.png` | Reference carousel slide 3 for Train/Val/Test Split. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/4.png` | Reference carousel slide 4 for Train/Val/Test Split. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/5.png` | Reference carousel slide 5 for Train/Val/Test Split. |
| `assets/brand-kit/references/(Post) TrainValidationTest Set/6.png` | Reference carousel slide 6 for Train/Val/Test Split. |
| `assets/brand-kit/references/README.md` | Storage directory for reference video and graphic design assets. |
| `assets/databro-avatar.jpg` | Official circular warm cream illustrated avatar asset. |
| `assets/databro.brand.starter.ts` | Isolated TypeScript brand tokens, color palette, and canvas presets. |
| `assets/generate_databro_cloned_vo.starter.py` | Generating each scene's voiceover: `python <skill-dir>/assets/generate_databro_cloned_vo.starter.py --text-file <scene.txt> --out public/vo/<scene>.mp3 [--fps 30] [--engine auto\|edge\|elevenlabs]`. Writes `<scene>.json` with `speechEndFrame` and ready `captions` (`{text, startFrame, endFrame}`, relative to clip start). Needs `pip install edge-tts`; the cloned voice needs `ELEVENLABS_API_KEY` plus `DATABRO_VOICE_ID`. |
| `references/databro-brand-assets-checklist.md` | Actionable tracking checklist for all Databro brand kit assets. |
| `references/databro-brand-guidelines.md` | Full brand guidelines, extracted color palette, and React Icons rules. |
| `references/databro-content-and-voiceover-guide.md` | Content archetypes, pacing, and Closed Caption guidelines. |

---

## Databro Signature Rules

### 1. Always Ask for Content Archetype and Topic First
* Before generating a new Databro video (unless the user already specified the topic and steps), ask which **Content Archetype** and **Topic** to research and build (`references/databro-content-and-voiceover-guide.md`):

  | # | Archetype | Key in `DATABRO_ARCHETYPES` | Default length | Example |
  |---|---|---|---|---|
  | 1 | Step-by-Step Technical Tutorial | `code-walkthrough` | 60s | *"Cara Install Lokal LLM Menggunakan Ollama"* |
  | 2 | Data Science / AI Concept Explainer | `concept-theory` | 45s | *"RAG vs Fine-Tuning dalam 60 Detik"* |
  | 3 | Tool / Library Listicle | `tool-listicle` | 45s | *"3 Python Library Wajib Buat Data Engineer"* |
  | 4 | Product / Feature Launch Reel | `launch-showcase` | 15s | *"Databro SQL Copilot"* |
  | 5 | Career / Opinion Editorial | `opinion-editorial` | 30s | *"Jangan belajar Python sebelum tahu ini"* |

* Also confirm length, aspect ratio, and voiceover mode (cloned talent, Edge-TTS fallback, or captions + SFX only).

### 2. Always Build on `<DatabroBaseCanvas />` (Persistent Chrome vs. Transitioning Stage)
* **Never place `<DatabroLogoLockup />`, `<DatabroSocialHandle />`, or `<DatabroCaptions />` inside individual transitioning scenes.**
* Mount [`DatabroBaseCanvas.starter.tsx`](assets/DatabroBaseCanvas.starter.tsx) at the Root Composition level so:
  - **Layer 0 (Canvas)**: Solid `#121212` matte charcoal background stays static.
  - **Layer 1 (Content Stage)**: `contentStage` box (`top: 250, bottom: 490, left: 90, right: 90` on `9:16`) hosts `<TransitionSeries>` with smooth CapCut transitions (`pop-scale`, `camera-zoom-pan`, `whip-slide`, `implode-out`). Scenes are **left-aligned like the carousel slides**: `#BB86FC` question headline, white subline under it, then the visual (diagram, table, code card). Center only hero moments: emblem pop, giant lime keyword, final CTA.
  - **Layer 2A (Top-Left Brand Lockup)**: Anchored at **`top: 108px, left: 100px`** (`64x64px` avatar + `Databro` / `Belajar Data Science` in cream `#F2EFEB`). Animates in **only once at `frame 0..12`** of the video and stays **100% stationary** across all slide transitions.
  - **Layer 2B (Top-Right Social Handle)**: `<DatabroSocialHandle />`, anchored at **`top: 108px, right: 100px`** (`@databro.id` in cream `#F2EFEB`, `24px` Regular italic, centered on the avatar row). Fades in at `frame 0..10`, then stays **100% stationary**.
  - **Layer 3 (Fixed Closed Captions)**: Locked at **`Y = 1480px`** (`1080x1920`, centered horizontally). Displays cardless 2-to-4 word ALL-CAPS white `#FFFFFF` (`38px` ExtraBold) phrases that switch via a `3-frame` opacity cross-fade with **zero vertical movement**.
  - **Layer 4 (Audio, BGM and TikTok SFX)**: Triggers `keyboard-typing.wav`, `pop-up.wav`, `whoosh-transition.wav`, `mouse-click.wav`, `progress-ticks.wav`, `callout-ding.wav`, and `bgm-ambient.wav` from `brand-kit/audio/`.

### 3. Modifying or Duplicating the Base Content Canvas Across Platforms
* To adapt any Databro video to Instagram Portrait Feed (`'4:5'`), Square (`'1:1'`), or YouTube (`'16:9'`), pass `aspectRatio="4:5" | "1:1" | "16:9"` to `<DatabroBaseCanvas />` or call `customizeDatabroCanvas()` in [`assets/databro.brand.starter.ts`](assets/databro.brand.starter.ts).

### 4. Vector Icons Standard : React Icons as Single Source of Truth
* **Strict Ban**: Never use generic AI-generated clipart, emojis, or arbitrary SVG doodles.
* **Standard**: Exclusively use **React Icons** (`react-icons` package: `react-icons/lu` Lucide, `react-icons/tb` Tabler, `react-icons/fi` Feather, `react-icons/fa6` FontAwesome).
* Standard Databro Icons (names verified against `react-icons@5.7.0`):
  - Brain / AI: `LuBrain` / `TbBrain`
  - Database / Storage: `LuDatabase` / `FiDatabase`
  - Code / Terminal: `LuCodeXml` / `LuTerminal` / `TbCode` / `FiTerminal`
  - Split / Branch: `LuSplit` / `TbArrowsSplit`
  - Quality / Check: `LuCheck` / `LuSparkles`
  - Alert / Warning: `LuTriangleAlert` / `LuCircleAlert`
  - Workflow / Steps: `LuWorkflow` / `LuLayers`
* Lucide renames icons between releases (the old `LuCode2`, `LuAlertTriangle`, and `LuAlertCircle` no longer exist). Before using a name not listed here, confirm it exists in the installed version: `grep "const LuName:" node_modules/react-icons/lu/index.d.ts`.

### 5. Absolute Ban on Em-Dashes (`—`) Across Writing and Closed Captions
* **Strict Rule**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in video titles, slides, code comments, Closed Captions, or scripts.
* Use colons (`:`), arrows (`->`), hyphens (`-`), or clean whitespace instead (e.g., `Training Accuracy -> 98%`, `Pilar 1: SOP Terstruktur`).

### 6. Tone of Voice and Pronoun Guardrails ("Kamu/Anda", Never "Lo")
* **Strictly Prohibited**: Never use `"Lo"` / `"Lu"` / `"Loe"` or `"Gue"`.
* **Second-Person Address**: Always use **`"Kamu"`** as the friendly tech-mentor default (*"model ML kamu"*, *"laptop kamu"*, *"biar kamu gak bingung"*), or **`"Anda"`** for formal/enterprise SLA contexts.
* **First-Person Address**: Always use **`"Kita"`** for inclusive tutorial walkthroughs (*"Yuk kita coba"*, *"Kita cek di terminal"*).
* **The "Bro" Salutation**: `"Bro"` is preserved as an energetic brand greeting and closing punctuation (*"Code-nya simpel banget, bro!"*, *"Belajar AI bareng Databro, bro!"*), but never use it as a pronoun substitute for `"lo"`.

### 7. Conversational Databro Wording Patterns
* Eliminate robotic, stiff textbook prose. Use authentic Databro patterns:
  - Opening questions: *"Pernah ngga.... model kamu akurasinya 98%... tapi pas dicoba di data baru, langsung jelek?"*
  - Diagnostic transitions: *"Nah, ini yang namanya overfitting."*, *"Simpelnya gini, bro."*
  - Code enthusiasm: *"Code-nya simpel banget, bro!"*
  - Important takeaways: *"Yang penting: ..."*, *"Takeaway quote: '...' "*
  - Spelling nuances: Use *"ngga"* (informal spoken Indonesian), short sentence pauses (`....` or `...`).

### 8. Authentic Color Palette and Lavender Question Headers
Values are pixel-sampled from the official carousel slides in `assets/brand-kit/references/`. Use the `databroBrand.colors` tokens, never ad-hoc hex values.
* **Canvas Backdrop**: `#121212` (matte charcoal).
* **Body Text, Sublines, Captions**: `#FFFFFF`. **Wordmark and `@databro.id`**: cream `#F2EFEB`.
* **Question Headlines**: **`#BB86FC`** (Lavender) for question headers and topic prompts. It is the only purple; validation-set visuals use it too.
* **Performance / Training Accents**: **`#03DAC6`** (Teal) for training statistics, good metrics (`98%`), and table header fills (with `#121212` header text and white cell outlines).
* **Signature Lime**: **`#C1FF72`** for `#1:` style subheads, the brain circuit icon, test-set metrics, and the `Takeaway quote:` label.
* **Pitfall Accents**: **`#FF5757`** (Coral) for bad metrics (`62%`) and warnings.
* **Emblem Circle**: cream `#F0ECE2` fill with `#121212` line-art ink.
* **Code Card**: GitHub Dark, `#24292E` with `#F97583` keywords, `#FFAB70` arguments, `#79B8FF` numbers, `#6A737D` comments, `#E1E4E8` code text.
* **Takeaway Quote**: serif text in `#CED3DA` with a `#CCCCCC` left bar.

### 9. Voiceover Talent Pitch Calibration (Matching Authentic Master Audio)
* **Master Calibration Sample**: The talent audio in `databro-talent-master-calibration.wav` has a measured fundamental frequency $F_0 \approx 86\text{--}90$ Hz (warm, grounded, articulate baritone).
* **Offline Edge-TTS Engine**:
  - Voice: `id-ID-ArdiNeural`
  - Pitch: **`-4Hz`** to lower the pitch into the talent's natural baritone register.
  - Rate: **`-2%`** (130-140 WPM) for natural cadence.
* **Online Cloned Voice (ElevenLabs)**: Clone the talent **once** from `databro-talent-master-calibration.mp3` (ElevenLabs Voices -> Instant Voice Clone), then set `ELEVENLABS_API_KEY` and `DATABRO_VOICE_ID`. The generator never substitutes a stock voice. It produces no word timings, so time captions from the audio or use the Edge-TTS engine for timing.
* **Captions from timings**: Offset each clip's `captions` by its scene's start frame plus the head delay, then pass them to `<DatabroBaseCanvas captions={...} />`. Scene length = head delay + `speechEndFrame` + tail delay.

### 10. Audio-Visual Transition Alignment and Breathing Room Rules
* **Never truncate or clamp audio to fit arbitrary scene lengths**:
  $$\text{Sequence Duration} = \text{HeadDelay} + \text{AudioDuration} + \text{TailDelay}$$
* **Post-Transition Settle Buffer (Head Delay = `10-12 frames`)**:
  - Visual slide enters and completes transition.
  - Visual stillness buffer runs for `10-12 frames` (~0.35s).
  - Speech begins only *after* the incoming slide settles and the whoosh SFX finishes.
* **Pre-Transition Speech Silence Buffer (Tail Delay = `12-14 frames`)**:
  - Voiceover finishes speaking.
  - Scene holds in quiet stillness for `12-14 frames` (~0.40s) before the next transition starts.
* **Outro Tail Hold (`24 frames`)**:
  - Hold for 24 frames after speech ends before terminating the video.

---

## Definition of Done

* Composition wraps scenes in `<DatabroBaseCanvas />` using `databroBrand` tokens (`#121212`, `#FFFFFF`, `#BB86FC`, `#03DAC6`, `#C1FF72`, `#FF5757`, `#24292E`) with zero CSS gradients, zero glows, and zero cross-brand leakage.
* Scenes are left-aligned (lavender headline, white subline, visual), with centering reserved for hero moments.
* Top-left `Databro / Belajar Data Science` lockup (`top: 108px, left: 100px` on `9:16`) and top-right `@databro.id` (`top: 108px, right: 100px`) animate only at `frame 0..12` and never transition between slides.
* Closed Captions are locked at `Y = 1480px` (`9:16`) in cardless 2-4 word ALL-CAPS `#FFFFFF` chunks with zero vertical bounce and zero em-dashes.
* All icons are exclusively sourced from **React Icons**, and every icon name exists in the installed `react-icons` version.
* Voiceover is calibrated to the talent baritone pitch (`pitch="-4Hz"`, `rate="-2%"`) with conversational phrasing, and no scene cuts into speech.
* The project type-checks (`npx tsc --noEmit`) and a still of every scene renders (`npx remotion still`). If `the-motion-designer` is installed, its project validation also passes.
