# Databro Studio (@databroid / @databro.id) : Brand Motion Guidelines and Base Canvas Spec

> **Source References**: 
> 1. Extracted from official Databro Studio TikTok carousel slides (Train, Validation, Test Split series).
> 2. Official TikTok video reels: "Databro / Belajar Data Science".
> 3. Talent Master Calibration Audio: `databro-talent-master-calibration.wav` (measured F0 = 86 Hz).
> 
> **Brand Isolation Rule**: These tokens, components, and layout rules apply **exclusively** when the user selects the **Databro** brand in `the-motion-designer` or invokes `/databro-brand-motion`. Never mix these tokens into `the-motion-designer` or other brands.

---

## 1. Full Color Palette (100% Solid Flat Colors : Zero Gradients)

Sampled directly from authentic Databro Studio carousel and video assets:

| Token Name | Hex Code | Visual Role and Usage in Databro Assets |
| :--- | :--- | :--- |
| **`backgroundPrimary`** | `#121212` | Full-bleed solid matte charcoal black canvas (`RGB(18, 18, 18)`). Zero gradients, zero noise, zero ambient glow orbs. |
| **`backgroundElevated`** | `#1E1E1E` | Card surface and table body background. |
| **`backgroundCodeCard`** | `#24292D` | Dark slate blue-gray surface for IDE and code cards (`borderRadius: 16px to 20px`). |
| **`textPrimary`** | `#FAF9F5` | Warm cream primary text, `Databro` brand title, and takeaway quotes (`RGB(250, 249, 245)`). |
| **`textSecondary`** | `#A3A3A3` | Sub-label (`Belajar Data Science`), top-right `@databro.id`, and section subheaders. |
| **`accentLavender`** | `#B487EC` | **Signature Question and Headline Purple** (`RGB(180, 135, 236)`). Used for carousel headlines: *"Pernah ngga....*, *"Apa itu Train/Val/Test Split?"*, *"Kenapa pakai ratio 70 / 15 / 15?"*, *"Implementasi pakai Python"*. |
| **`accentCyan`** | `#02DAC5` | **High-Performance and Training Teal** (`RGB(2, 218, 197)`). Used for 70% Training set bar, `Training Accuracy -> 98%`, and Table Header background. |
| **`accentPrimary` / `accentLime`** | `#BFFF72` / `#BEF96E` | **Signature Databro Lime Green** (`RGB(190, 249, 110)`). Used for 15% Test set bar, Brain circuit icon, `#1: Training Set` badge, and `Takeaway quote:` label. |
| **`accentViolet`** | `#B684F3` | **Validation Purple** (`RGB(182, 132, 243)`). Used for 15% Validation set bar and cylinder middle slice. |
| **`accentCoralRed`** | `#E95F62` | **Warning and Pitfall Coral Red** (`RGB(233, 95, 98)`). Used for `Real-world Accuracy -> 62%`, overfitting alerts, and error diagnostics. |
| **`calloutRed`** | `#D92D20` | Solid 3px red rectangular callout border (`borderRadius: 6px`) highlighting key terminal output or buttons. |
| **`emblemCircleFill`** | `#F0ECE2` | Warm cream circle (`RGB(240, 236, 226)`) used for the top-left avatar background and central hero emblem circles. |
| **`emblemCircleInk`** | `#121212` | Bold black line-art icon inside the `#F0ECE2` warm cream circle. |

### Code Syntax Highlighting Palette (`background: #24292D`)
- **Keywords (`from`, `import`, `def`)**: `#C27182` (soft rose / salmon pink)
- **Parameters and Numbers (`test_size=0.30`, `random_state=42`)**: `#D28251` (warm orange)
- **Code Comments (`# Step 1: Split train vs temp`)**: `#62676C` (muted slate gray)
- **Variables and Code Text (`X_train, y_train`)**: `#FAF9F5` (warm cream)

---

## 2. Vector Icons Standard : React Icons as Single Source of Truth

* **Strict Prohibition**: Never use AI-generated emojis, generic flat AI clipart, or arbitrary raster doodles.
* **Source of Truth**: Use [React Icons](https://react-icons.github.io/react-icons/) exclusively for all UI and vector icons across Remotion compositions:
  - **`react-icons/lu` (Lucide Icons, Primary Standard)**: `LuBrain`, `LuDatabase`, `LuCode2`, `LuCheck`, `LuAlertTriangle`, `LuSplit`, `LuSparkles`, `LuBookOpen`, `LuLayers`, `LuWorkflow`, `LuServer`, `LuGauge`.
  - **`react-icons/tb` (Tabler Icons)**: `TbBrain`, `TbCode`, `TbArrowsSplit`, `TbRobot`, `TbDatabase`.
  - **`react-icons/fi` (Feather Icons)**: `FiDatabase`, `FiTerminal`, `FiCheckCircle`.
  - **`react-icons/fa6` (FontAwesome 6)**: `FaBrain`, `FaPython`.
* **Styling**: Always render icons using crisp vector strokes, sized proportionally (`size={48}` to `size={64}`), colored in Databro brand tokens (`#BFFF72`, `#02DAC5`, `#B487EC`, `#FAF9F5`).

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
  - Pitch: **`-4Hz`** (or `-5Hz`) to lower the default high-pitched announcer timbre into the talent's natural baritone range.
  - Rate: **`-2%`** to **`+0%`** for relaxed, articulate delivery.
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
| **Layer 1: Center Stage** | `<TransitionSeries>` host | `top: 250, bottom: 490, left: 90, right: 90` | **Transitioning** : ONLY this layer runs CapCut smooth transitions (`pop-scale`, `camera-zoom-pan`, `whip-slide`, `implode-out`). |
| **Layer 2A: Top-Left Lockup** | `DatabroLogoLockup` | **`top: 108px, left: 100px`** (`64x64px` avatar) | **Persistent** : animates in **only once at `frame 0..12`** of the video, then stays **100% stationary** across all slide transitions. |
| **Layer 2B: Top-Right Handle** | `@databro.id` | **`top: 108px, right: 100px`** (`#A3A3A3`, `24px` Regular) | **Persistent** : subtle, anchored throughout the video. |
| **Layer 3: Closed Captions** | `DatabroCaptions` | Locked at **`Y = 1480px`** (`left: 110, right: 110`) | **Persistent** : locked at `Y = 1480px` throughout the entire video (`3-frame` opacity cross-fade, **zero vertical movement**). |
| **Layer 4: Audio and SFX** | `<Audio />` + `<Sequence>` | Root audio bus | Plays `bgm-ambient.wav` (`volume: 0.14`), `voiceover.wav`, and frame-accurate TikTok SFX cues. |

### Multi-Platform Aspect Ratio Presets (`DATABRO_CANVAS_PRESETS`)

| Aspect Ratio | Resolution | Top-Left Logo `(left, top)` | Top-Right Handle `(right, top)` | Centered Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` |
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
