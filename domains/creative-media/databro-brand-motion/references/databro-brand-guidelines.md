# Databro Studio (@databroid / @databro.id) : Brand Motion Guidelines and Base Canvas Spec

> **Source References**: 
> 1. Extracted from official Databro Studio TikTok carousel slides (Train, Validation, Test Split series).
> 2. Official TikTok video reels: "Databro / Belajar Data Science".
> 3. Talent Master Calibration Audio: `databro-talent-master-calibration.wav` (measured F0 = 86 Hz).
> 
> **Brand Isolation Rule**: These tokens, components, and layout rules apply **exclusively** when the user selects the **Databro** brand in `the-motion-designer` or invokes `/databro-brand-motion`. Never mix these tokens into `the-motion-designer` or other brands.

---

## 1. Full Color Palette (100% Solid Flat Colors : Zero Gradients)

Pixel-sampled (most frequent exact pixel values) from the 13 official carousel slides in `assets/brand-kit/references/` (`Train/Val/Test Split`, `Korelasi vs Kausalitas`). These are the canonical values in `databro.tokens.json` and `databroBrand.colors`.

| Token Name | Hex Code | Visual Role and Usage in Databro Assets |
| :--- | :--- | :--- |
| **`backgroundPrimary`** | `#121212` | Full-bleed solid matte charcoal canvas. Zero gradients, zero noise, zero ambient glow orbs. |
| **`backgroundElevated`** | `#1E1E1E` | Card surface (not present in the slides; use sparingly). |
| **`backgroundCodeCard`** | `#24292E` | GitHub Dark code card surface (`borderRadius: 16px to 20px`). |
| **`textPrimary`** | `#FFFFFF` | Body text, sublines (*"model kamu akurasinya 98%..."*), table cells, and Closed Captions. |
| **`textBrand`** | `#F2EFEB` | `Databro` wordmark, `Belajar Data Science` tagline, and the top-right `@databro.id` handle (italic). |
| **`textSecondary`** | `#CCCCCC` | Muted labels and diagram strokes. |
| **`accentLavender`** | `#BB86FC` | **Signature question and headline purple.** Carousel headlines: *"Pernah ngga...."*, *"Apa itu Train/Val/Test Split?"*, *"Implementasi pakai Python"*. The only purple in the palette; validation-set visuals use it too. |
| **`accentCyan`** | `#03DAC6` | **Training and good-metric teal.** 70% training bar, `Training Accuracy -> 98%`, table header fill. |
| **`accentPrimary` / `accentLime`** | `#C1FF72` | **Signature Databro lime.** Brain circuit icon, `#1: Training Set` subheads, test-set metrics, `Takeaway quote:` label. |
| **`accentCoralRed`** | `#FF5757` | **Pitfall coral.** `Real-world Accuracy -> 62%`, overfitting alerts, error diagnostics. |
| **`calloutRed`** | `#D92D20` | Solid 3px red rectangular callout border (`borderRadius: 6px`) on terminal output or buttons (tutorial reels; not in the carousels). |
| **`emblemCircleFill`** | `#F0ECE2` | Warm cream circle behind the avatar and hero emblems. |
| **`emblemCircleInk`** | `#121212` | Bold black line-art icon inside the cream circle. |
| **`tableHeaderFill` / `tableHeaderInk`** | `#03DAC6` / `#121212` | Table header row: teal fill, bold charcoal text. Body cells are transparent with 2px `#FFFFFF` outlines and white text. |
| **`quoteBar` / `quoteText`** | `#CCCCCC` / `#CED3DA` | Takeaway quote: serif text with a 4px left bar, under a lime `Takeaway quote:` label. |

`accentViolet` is kept only as a deprecated alias of `#BB86FC` so older compositions still compile.

### Code Syntax Highlighting Palette (GitHub Dark, `background: #24292E`)
- **Keywords (`from`, `import`, `def`)**: `#F97583`
- **Arguments (`test_size=`, `random_state=`)**: `#FFAB70`
- **Numbers (`0.30`, `42`)**: `#79B8FF`
- **Comments (`# Step 1: Split train vs temp`)**: `#6A737D`
- **Variables, functions, and code text (`X_train`, `train_test_split`)**: `#E1E4E8`

### Data Table Screenshot Palette (`graphics/Table.png`)
A notebook-style dataframe preview, separate from the teal-header carousel table: body `#1F1F1E`, header `#262624`, row divider `#3B3B39`, cell text `#FAF9F5`.

### Slide Layout (from the carousels)
- Content is **left-aligned** on a shared left edge: lavender headline (about 56px ExtraBold), white subline directly under it (about 32px Regular), then the visual block, then lime subheads with white body text.
- Generous empty space; no boxes behind headlines; flat fills only.
- In video, keep this left alignment inside `contentStage`. Center only hero moments (emblem pop, giant lime keyword, final CTA).

---

## 2. Vector Icons Standard : React Icons as Single Source of Truth

* **Strict Prohibition**: Never use AI-generated emojis, generic flat AI clipart, or arbitrary raster doodles.
* **Source of Truth**: Use [React Icons](https://react-icons.github.io/react-icons/) exclusively for all UI and vector icons across Remotion compositions:
  - **`react-icons/lu` (Lucide Icons, Primary Standard)**: `LuBrain`, `LuDatabase`, `LuCodeXml`, `LuTerminal`, `LuCheck`, `LuTriangleAlert`, `LuCircleAlert`, `LuSplit`, `LuSparkles`, `LuBookOpen`, `LuLayers`, `LuWorkflow`, `LuServer`, `LuGauge`.
  - **`react-icons/tb` (Tabler Icons)**: `TbBrain`, `TbCode`, `TbArrowsSplit`, `TbRobot`, `TbDatabase`.
  - **`react-icons/fi` (Feather Icons)**: `FiDatabase`, `FiTerminal`, `FiCheckCircle`.
  - **`react-icons/fa6` (FontAwesome 6)**: `FaBrain`, `FaPython`.
* **Version check**: Names verified against `react-icons@5.7.0`. Lucide renames icons between releases (`LuCode2`, `LuAlertTriangle`, `LuAlertCircle` no longer exist), so confirm any other name with `grep "const LuName:" node_modules/react-icons/lu/index.d.ts`.
* **Styling**: Always render icons using crisp vector strokes, sized proportionally (`size={48}` to `size={64}`), colored in Databro brand tokens (`#C1FF72`, `#03DAC6`, `#BB86FC`, `#FFFFFF`).

---

## 3. Punctuation Guardrail : Absolute Ban on Em-Dashes (`—`)

* **Rule**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in:
  - Video titles, scene headlines, or question openers
  - Closed Captions text
  - Slide body text and takeaways
  - Code comments and terminal logs
  - Voiceover synthesis scripts
* **Replacement**: Use clean punctuation:
  - Arrows: `->` (e.g., `Training Accuracy -> 98%`)
  - Colons: `:` (e.g., `Pilar 1: Standar Operasional`)
  - Hyphens: `-` (e.g., `train-test-split`)
  - Clean spacing or parentheses

---

## 4. Voiceover Talent Calibration and Conversational Indonesian Tone

* **Acoustic Profiling**:
  - The talent master calibration audio (`databro-talent-master-calibration.wav`) has a measured fundamental frequency $F_0$ of **86 to 90 Hz** (grounded, warm baritone).
  - Normal speaking speed: **130 to 140 WPM**.
* **Offline Edge-TTS Calibration**:
  - Voice: `id-ID-ArdiNeural`
  - Pitch: **`-4Hz`** to lower the default high-pitched announcer timbre into the talent's natural baritone range.
  - Rate: **`-2%`** for relaxed, articulate delivery.
* **Conversational Wording (Eliminating Robotic AI Starch)**:
  - Natural opening hooks: *"Pernah ngga.... model kamu akurasinya 98%... tapi pas dicoba di data baru, langsung jelek?"*
  - Natural transitions: *"Nah, ini yang namanya overfitting."*, *"Simpelnya gini, bro."*
  - Authentic enthusiast sign-off: *"Code-nya simpel banget, bro!"*, *"Save video ini dan follow Databro buat belajar AI bareng, bro!"*
  - Pronoun guardrails: Always use **`"Kamu"`** and **`"Kita"`**. Never use `"Lo"` or `"Gue"`.

---

## 5. Standard Databro Base Content Canvas (`DatabroBaseCanvas`)

Every Databro video is built on `DatabroBaseCanvas` and `DATABRO_CANVAS_PRESETS`.

### Persistent Root Layers vs. Transitioning Stage

| Layer | Component / Element | Position on `9:16` (`1080x1920`) | Transition Rule |
| :--- | :--- | :--- | :--- |
| **Layer 0: Canvas** | `#121212` Matte Charcoal | `0, 0, 1080x1920` | **Persistent** : never transitions. |
| **Layer 1: Content Stage** | `<TransitionSeries>` host | `top: 250, bottom: 490, left: 90, right: 90` | **Transitioning** : ONLY this layer runs CapCut smooth transitions (`pop-scale`, `camera-zoom-pan`, `whip-slide`, `implode-out`). Scene content is left-aligned. |
| **Layer 2A: Top-Left Lockup** | `DatabroLogoLockup` | **`top: 108px, left: 100px`** (`64x64px` avatar) | **Persistent** : animates in **only once at `frame 0..12`** of the video, then stays **100% stationary** across all slide transitions. |
| **Layer 2B: Top-Right Handle** | `DatabroSocialHandle` | **`top: 108px, right: 100px`** (`#F2EFEB`, `24px` Regular italic) | **Persistent** : fades in at `frame 0..10`, then anchored throughout the video. |
| **Layer 3: Closed Captions** | `DatabroCaptions` | Locked at **`Y = 1480px`** (`left: 110, right: 110`) | **Persistent** : locked at `Y = 1480px` throughout the entire video (`3-frame` opacity cross-fade, **zero vertical movement**). |
| **Layer 4: Audio and SFX** | `<Audio />` + `<Sequence>` | Root audio bus | Plays `bgm-ambient.wav` (`volume: 0.08`), `voiceover.wav`, and frame-accurate TikTok SFX cues. |

### Multi-Platform Aspect Ratio Presets (`DATABRO_CANVAS_PRESETS`)

| Aspect Ratio | Resolution | Top-Left Logo `(left, top)` | Top-Right Handle `(right, top)` | Content Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`9:16`** (TikTok / Reels / Shorts) | `1080x1920` | `(100px, 108px)` | `(100px, 108px)` | `top: 250, bottom: 490, left: 90, right: 90` | **`Y = 1480px`** (`38px` ExtraBold) |
| **`4:5`** (IG / LinkedIn Portrait) | `1080x1350` | `(84px, 72px)` | `(84px, 72px)` | `top: 180, bottom: 260, left: 84, right: 84` | **`Y = 1140px`** (`34px` ExtraBold) |
| **`1:1`** (Square Feed) | `1080x1080` | `(72px, 56px)` | `(72px, 56px)` | `top: 150, bottom: 210, left: 72, right: 72` | **`Y = 910px`** (`32px` ExtraBold) |
| **`16:9`** (YouTube / Landscape) | `1920x1080` | `(96px, 64px)` | `(96px, 64px)` | `top: 160, bottom: 200, left: 140, right: 140` | **`Y = 920px`** (`36px` ExtraBold) |

---

## 6. Audio-Visual Transition Timing Buffer Rules

1. **Post-Transition Settle Buffer (`HeadDelay = 10 to 12 frames`)**:
   - Visual slide enters and completes transition.
   - Settle buffer runs in visual stillness.
   - Voiceover speech begins at `frame 10..12`.
2. **Pre-Transition Speech Silence Buffer (`TailDelay = 12 to 14 frames`)**:
   - Voiceover completes speech.
   - Scene holds in quiet stillness for 12 to 14 frames.
   - Next transition begins smoothly without clipping words.
3. **Outro Hold (`24 frames`)**:
   - Outro holds for 24 frames before video terminates.
