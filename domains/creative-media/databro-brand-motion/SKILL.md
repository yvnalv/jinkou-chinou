---
name: databro-brand-motion
description: "Databro Studio (@databroid / @databro.id) specialized brand motion skill extending the-motion-designer. Applies Databro's isolated visual identity and Standard Base Content Canvas (DatabroBaseCanvas) for Remotion videos across 9:16, 4:5, 1:1, and 16:9: #121212 matte charcoal canvas, white body text, #BB86FC lavender question headlines, #03DAC6 teal and #C1FF72 lime accents, left-aligned slide layouts, React Icons (react-icons/lu) as strict vector source of truth, persistent top-left Databro avatar lockup and top-right @databro.id, fixed Closed Captions locked at Y=1480px, absolute ban on em-dashes, CapCut smooth transitions with 10-frame settle delay, and calibrated baritone voiceover with synced caption timings. Covers tutorials, concept explainers, tool listicles, launch reels, and career opinion videos. Use when the user selects the Databro brand in the-motion-designer or invokes /databro-brand-motion. Never mix with GLM or other brands."
metadata:
  version: 0.4.2
---

# Databro Brand Motion : `@databroid` Visual Identity and Base Content Canvas

Specialized brand skill extending **`the-motion-designer`** exclusively for **Databro Studio (`@databroid` / `@databro.id` : "Belajar Data Science")**.

This skill isolates all Databro brand guidelines, colors, typography, logo lockups, sound effects, voiceover samples, and **Standard Base Content Canvas** presets (`9:16`, `4:5`, `1:1`, `16:9`) so they never contaminate `the-motion-designer` or any other brand skill (such as `GLM`).

> [!WARNING]
> **CRITICAL GATE (Jangan Generate Design Image/Video Tanpa Diminta):**
> **Jangan buat atau generate design konten image jika tidak diminta, atau tanya terlebih dahulu.**
> Selalu susun konsep, storyboard, atau script teks terlebih dahulu dan konfirmasikan ke user sebelum merender slide image, Canva design, atau video Remotion.

```text
Confirm Topic & Archetype -> Plan Storyboard/Script -> Review with User -> Mount <DatabroBaseCanvas> -> Render
```

---

## Databro Mission & Brand Foundations

Databro adalah platform edukasi dan eksplorasi data science untuk membantu masyarakat Indonesia memahami data, teknologi, dan AI secara praktis, aplikatif, dan relatable.

### 5 Project Principles in Motion Design
1. **Simplicity First**: Layout panggung harus bersih dan langsung dipahami dalam 3 detik pertama.
2. **Data-Driven**: Tampilkan data, kurva, atau metrik riil (bukan grafik fiktif).
3. **Practical Use Case**: Visualisasikan studi kasus nyata (fintech, e-commerce, terminal output asli).
4. **Educational Value**: Setiap scene memberikan satu insight konkret yang bernilai.
5. **Visual Clarity**: Visualisasi data harus tajam, elegan, flat matte, dan bebas dari elemen dekorasi neon/glowing berlebihan.

### Audience : The Full Spectrum Rule
Setiap video atau slide Databro dikonsumsi bersamaan oleh pemula dan engineer senior:
- **Pendekatan visual ramah**: Tidak mengintimidasi, teks hook relatable, istilah teknis didefinisikan dengan bahasa sederhana.
- **Kedalaman teknis terjaga**: Kode yang ditampilkan adalah kode valid, arsitektur yang digambarkan sesuai standar industri, dan metrik akurat.
- **Editorial Constraint**: Dilarang keras memakai berita duka/tragedi/isu emosional negatif sebagai hook motion video. Gunakan hook positif atau netral yang terhubung organik ke data science.

---

## When to Use

* Generating TikTok, Instagram Reels, YouTube Shorts, `4:5` Feed, or `16:9` educational data science / AI motion videos for **Databro Studio (`@databroid`)**.
* When the user selects **Databro** during Step 1 of `the-motion-designer`'s Pre-Generation Option Wizard or invokes `/databro-brand-motion`.

Do not use it for: any non-Databro brand (such as GLM or neutral client projects), or generating designs without user request.

---

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
| `assets/brand-kit/references/Slide1-Cover.png` | Reference slide 1 Cover from authentic Berkson Fallacy carousel. |
| `assets/brand-kit/references/Slide2-Hook.png` | Reference slide 2 Hook and table comparison. |
| `assets/brand-kit/references/Slide3-Konsep.png` | Reference slide 3 DAG collider diagram. |
| `assets/brand-kit/references/Slide4-Bukti.png` | Reference slide 4 Simulation scatter plots. |
| `assets/brand-kit/references/Slide5-KasusML.png` | Reference slide 5 Machine learning application scatter plot. |
| `assets/brand-kit/references/Slide6-Kode.png` | Reference slide 6 Clean Python implementation code card. |
| `assets/brand-kit/references/Slide7-Takeaway.png` | Reference slide 7 3-point checklist and takeaway quote. |
| `assets/brand-kit/references/Slide8-CTA.png` | Reference slide 8 Closing emblem call to action. |
| `assets/databro-avatar.jpg` | Official circular warm cream illustrated avatar asset. |
| `assets/databro.brand.starter.ts` | Isolated TypeScript brand tokens, color palette, and canvas presets. |
| `assets/generate_databro_cloned_vo.starter.py` | Generating each scene voiceover and caption timings. |
| `references/databro-brand-assets-checklist.md` | Actionable tracking checklist for all Databro brand kit assets. |
| `references/databro-brand-guidelines.md` | Full brand guidelines, extracted color palette, and React Icons rules. |
| `references/databro-content-and-voiceover-guide.md` | Content archetypes, pacing, and Closed Caption guidelines. |
| `scripts/render_carousel.py` | Python script for rendering authentic Databro carousels via matplotlib. |
| `scripts/render_carousel_v2.py` | Updated Python script for rendering authentic Databro carousels. |

---

## Databro Signature Rules

### 1. Mandatory Upfront Gate (Ask Before Design / Render)
* **Never generate still images, carousels, or video renders automatically.**
* Always present the topic, content archetype, and storyboard plan to the user first.

### 2. Always Ask for Content Archetype and Topic First
* Confirm which **Content Archetype** to build:
  - **1. Step-by-Step Technical Tutorial** (`code-walkthrough`, `60s`)
  - **2. Data Science / AI Concept Explainer** (`concept-theory`, `45s`)
  - **3. Tool / Library Listicle** (`tool-listicle`, `45s`)
  - **4. Product / Feature Launch Reel** (`launch-showcase`, `15s`)
  - **5. Career / Opinion Editorial** (`opinion-editorial`, `30s`)
* Confirm duration, aspect ratio (`9:16`, `4:5`, `1:1`, `16:9`), and voiceover mode.

### 3. Always Build on `<DatabroBaseCanvas />`
* Never place lockups or captions inside individual transitioning scenes.
* Mount [`DatabroBaseCanvas.starter.tsx`](assets/DatabroBaseCanvas.starter.tsx) at Root level:
  - **Layer 0 (Canvas)**: Solid `#121212` matte charcoal background stays static (no gradients, no glow).
  - **Layer 1 (Content Stage)**: Hosts `<TransitionSeries>` with CapCut transitions. Left-aligned content: `#BB86FC` question headline, white subline, clean visual.
  - **Layer 2A (Top-Left Lockup)**: Anchored at `top: 108px, left: 100px` (`64x64px` avatar + `Databro / Belajar Data Science` in `#F2EFEB`). Animates once at `frame 0..12`.
  - **Layer 2B (Top-Right Handle)**: Anchored at `top: 108px, right: 100px` (`@databro.id` in `#F2EFEB`, `24px` Regular italic).
  - **Layer 3 (Fixed Captions)**: Locked at **`Y = 1480px`** (`9:16`, 2-4 word ALL-CAPS `#FFFFFF` chunks, zero vertical bounce).
  - **Layer 4 (Audio & SFX)**: Plays BGM and timed SFX cues.

### 4. Vector Icons Standard : React Icons Exclusively
* Strictly ban AI-generated clipart, 3D cartoon emojis, or arbitrary SVG doodles.
* Exclusively use **React Icons** (`react-icons/lu`, `react-icons/tb`, `react-icons/fi`).

### 5. Absolute Ban on Em-Dashes
* Strictly zero em-dashes (`—`) or en-dashes (`–`) anywhere in titles, slides, code comments, Closed Captions, or scripts. Use colons (`:`), arrows (`->`), or hyphens (`-`).

### 6. Tone of Voice and Pronoun Guardrails ("Kamu/Kita", Never "Lo")
* **Strictly Prohibited**: NEVER use `"Lo"`, `"Lu"`, `"Loe"`, or `"Gue"`.
* **Required Address**: Always use **`"Kamu"`** (default learner), **`"Anda"`** (enterprise), and **`"Kita"`** (collaborative).
* **The "Bro" Salutation**: Energetic brand greeting and sign-off (*"Simpelnya gini, bro!"*), paired with `"kamu"`.

### 7. Voiceover Talent Pitch Calibration
* Master audio calibration fundamental frequency $F_0 \approx 86\text{--}90$ Hz (warm baritone).
* Edge-TTS: Voice `id-ID-ArdiNeural`, pitch `"-4Hz"`, rate `"-2%"`.
* Buffer rules: Head Delay = 10-12 frames, Tail Delay = 12-14 frames, Outro Hold = 24 frames.

---

## Definition of Done

* Storyboard/script was presented to and approved by the user before rendering.
* Content adheres to the Full Spectrum rule and positive/neutral editorial constraints.
* Composition wraps scenes in `<DatabroBaseCanvas />` using `databroBrand` tokens (`#121212`, `#FFFFFF`, `#BB86FC`, `#03DAC6`, `#C1FF72`, `#FF5757`, `#24292E`) with zero CSS gradients and zero glows.
* Left-aligned stage layout, fixed top-left lockup, top-right handle, and fixed Closed Captions at Y=1480px.
* Vector icons from React Icons only.
* Zero em-dashes across all text.
* The project type-checks (`npx tsc --noEmit`) and still images render accurately.
