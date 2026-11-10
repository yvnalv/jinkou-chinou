# GLM Systems (glmsystems.com) : Brand Motion Guidelines and Base Canvas Spec

> **Official Brand Colors (Source of Truth)**:
> - **Lime (Primary)**: `#CDFF70` | RGB: `205, 255, 112`
> - **Emerald**: `#003A40` | RGB: `0, 58, 64`
> - **Stone Grey**: `#444547` | RGB: `68, 69, 71`
> - **Cool White**: `#F2F0FA` | RGB: `242, 240, 250`
> 
> **Source References**: 
> 1. Official GLM Systems Brand Color Codes & Guidelines.
> 2. GLM Corporate Website (`glmsystems.com`) and B2B LinkedIn campaign assets.
> 3. Official Vector SVG Brandmarks (`GLM-BIRD-Color.svg`, `GLM-black-Text-Color-Bird.svg`).
> 4. GLM Audio Branding & Synthesized Sound System (`muziek-profiel.md`, `muziek-kennis.md`).
> 5. GLM Systems Official Documentation (`docs.glmsystems.com/aiplusagent/`).
> 
> **Brand Isolation Rule**: These tokens, components, and layout rules apply **exclusively** when the user selects the **GLM** brand in `the-motion-designer` or invokes `/glm-brand-motion`. Never mix these tokens into `the-motion-designer` or other brand profiles (such as Databro).

---

## 1. Official Color Palette (100% Solid Flat Colors : Zero Gradients)

Sampled directly from authentic GLM Systems brand standards:

| Token Name | Hex Code | RGB | Visual Role and Usage in GLM Assets |
| :--- | :--- | :--- | :--- |
| **`accentPrimary` / `lime`** | **`#CDFF70`** | `205, 255, 112` | **Signature GLM Lime (Primary)** : Electric lime green representing energy, motion, and AI innovation; fills the GLM dual birds and highlights interactive keywords. |
| **`backgroundSecondary` / `emerald`** | **`#003A40`** | `0, 58, 64` | **Signature GLM Emerald** : Deep, technological blue-green representing enterprise trust and software architecture; used for high-contrast cards and hero scenes. |
| **`textPrimary` / `stoneGrey`** | **`#444547`** | `68, 69, 71` | **Official Stone Grey** : Primary headline and body typography on Cool White surfaces; also used for subtle structural elements. |
| **`backgroundPrimary` / `coolWhite`** | **`#F2F0FA`** | `242, 240, 250` | **Official Cool White** : Spacious, clean lilac-white canvas backdrop for enterprise motion graphics. |
| **`backgroundCard`** | `#FFFFFF` | `255, 255, 255` | **Pure White** : Elevated card surface on `#F2F0FA` backdrop (`borderRadius: 16px to 20px`). |
| **`textSecondary`** | `#666666` | `102, 102, 102` | **Muted Grey** : Secondary descriptions, timestamps, and ERP metadata. |
| **`textOnDark`** | `#F2F0FA` | `242, 240, 250` | **Cool White Text** : High-contrast text on `#003A40` Emerald backgrounds. |
| **`borderSubtle`** | `#E5E7EB` | `229, 231, 235` | Subtle 1.5px card border on Cool White backgrounds. |
| **`semanticSuccess`** | `#10B981` | `16, 185, 129` | Emerald green for verified data entries and automated tasks. |
| **`semanticWarning`** | `#F59E0B` | `245, 158, 11` | Amber for review requests and pending approvals. |
| **`semanticDanger`** | `#EF4444` | `239, 68, 68` | Red for inventory stockout warnings and validation errors. |

---

## 2. Visual Language & Geometric Staging

* **Spacious Whitespace**: Generous margins, clean paddings, and uncluttered typography.
* **Architectural Corner Chevrons**: Subtle diagonal cuts in Emerald (`#003A40`, top-left) and Lime (`#CDFF70`, bottom-right) framing the 1920x1080 canvas:
  - Top-Left: `clip-path: polygon(0 0, 160px 0, 356px 190px, 0 563px)`
  - Bottom-Right: `clip-path: polygon(1920px 741px, 1528px 1012px, 1572px 1080px, 1920px 1080px)`
  - Dynamic scaling: `0.55x` during content scenes for maximum stage breathing room; `1.0x` on the final Outro End Card.
* **Editorial Highlighter Underlay (`.hl`)**: Strategic keywords in headlines feature an electric Lime underlay bar rendered behind letter descenders:
  ```css
  background: linear-gradient(transparent 58%, #CDFF70 58%, #CDFF70 92%, transparent 92%);
  padding: 0 0.08em;
  ```
* **Double-Shadow Card Elevation**: UI software mockups and demo cards float with crisp definition:
  - Outline: `0 2px 0 3px #003A40` (solid Emerald perimeter border)
  - Diffusion: `0 40px 80px rgba(0, 37, 41, 0.22)` (soft deep elevation)
* **Asymmetric Prompt Chips**: Prompt showcase pills use a modern speech-tag silhouette with tightened bottom-right corner (`border-radius: 46px 46px 10px 46px`), filled in `#CDFF70` Lime with `#100E0D` dark typography.
* **Typography Hierarchy**:
  - Hero Numbers, Big Headlines & Eyebrows: **Geist** (`font-weight: 700 / 800`, letter-spacing `-0.03em`).
  - Eyebrow Badges: **Geist 700**, uppercase, `letter-spacing: 0.16em`, with 16px circular badge (Lime core, 3px Emerald outline).
  - Body, Subtitles & ERP Metadata: **Poppins** (`font-weight: 400 / 500 / 600`).
* **Living Mascot Dynamics (Flippy)**:
  - Vector SVG mascot with independent wing group pivoting around `(245, 281)`.
  - Flight physics: 4.5 Hz fast wing flap cycle with vertical banking tilt proportional to velocity (`clamp(vy / 60, -14, 14)`).
  - Idle stance: 0.6 Hz gentle breathing wave with periodic casual flap.
  - Interactive choreography: Flippy swoops into frame, moves to the bottom corner during UI demonstrations, and physically delivers prompt chips.
* **Audio-Independent Comprehension**: LinkedIn feeds play videos without sound by default. Every beat, question, and takeaway must be 100% readable from on-screen graphics alone.
* **Verified Citations**: When citing performance metrics, time savings, or financial counts, always include verified source captions in-scene.

---

## 3. Vector Icons Standard : React Icons as Single Source of Truth

* **Strict Prohibition**: Never use AI-generated emojis, generic flat AI clipart, or arbitrary doodles.
* **Source of Truth**: Use [React Icons](https://react-icons.github.io/react-icons/) exclusively for all UI and vector icons across Remotion compositions:
  - **`react-icons/lu` (Lucide Icons, Primary Standard)**: `LuBuilding2`, `LuDatabase`, `LuBot`, `LuSparkles`, `LuCheckCircle`, `LuSearch`, `LuMail`, `LuSend`, `LuWorkflow`, `LuLayers`, `LuShieldCheck`, `LuArrowRight`.
  - **`react-icons/tb` (Tabler Icons)**: `TbRobot`, `TbBinaryTree`, `TbArrowsSplit`, `TbDatabase`.
  - **`react-icons/fi` (Feather Icons)**: `FiCheck`, `FiFileText`, `FiSend`.
* **Styling**: Render icons using crisp vector strokes, sized proportionally (`size={32}` to `size={54}`), colored in GLM brand tokens (`#003A40`, `#CDFF70`, `#444547`).

---

## 4. Punctuation Guardrail : Absolute Ban on Em-Dashes (`—`)

* **Rule**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in:
  - Video titles, scene headlines, or question openers
  - Closed Captions text
  - Slide body text and takeaways
  - Code comments and UI metadata
  - Voiceover synthesis scripts
* **Replacement**: Use clean punctuation:
  - Colons: `:` (e.g., `Scene 1 : The Tension`)
  - Arrows: `->` (e.g., `Exact Globe+ -> Sales Orders`)
  - Hyphens: `-` (e.g., `B2B-first`)
  - Clean spacing or parentheses

---

## 5. Audio Brand Identity (The Voice of the Brand in Sound)

Extracted from GLM's audio brand architecture (`muziek-profiel.md`):

* **Character**: **Zakelijk, upbeat, gegrond** (confident, forward, never floating or meditative).
* **Tempo**: `116 to 120 BPM`. Upbeat without rushing.
* **Harmonic Structure**: Calm harmony with an active rhythmic groove. Avoid dreamy ambient beds or repetitive bells ("gongs").
* **Sound Effects Calibration**:
  - `pop`: Tight 40ms blip with hard click when data cards or badges appear (-8dB).
  - `swoosh`: 0.28s rising air sweep on headline/card entrances (-15dB).
  - `ticks`: Cascading clicks for multi-item table loads (-18dB).
  - `stijg` (rise): Ascending pitch on progress bars and counters (-14dB).
  - `ping`: Crisp glass ping on send confirmation or release alerts (-14dB, maximum 2 per video).

---

## 6. Reading Pacing Rules (GLM Minimum Time Standard)

Enterprise software animations require calibrated reading time:

| In-Video Element | Minimum Required On-Screen Time |
| :--- | :--- |
| **Per Spoken / Written Word** | `0.4 seconds` per word |
| **Per New Text Block Entry** | `0.5 seconds` initial eye landing buffer |
| **Minimum per Text Card** | **`2.0 seconds`** minimum visibility |
| **Stillness Buffer after Motion** | **`2.0 seconds`** visual stillness before scene transition |
| **Outro Endcard** | **`2.5 seconds`** minimum hold for GLM logo and website |

---

## 7. Standard GLM Base Content Canvas (`GlmBaseCanvas`)

Every GLM video is built on `GlmBaseCanvas.starter.tsx` and `GLM_CANVAS_PRESETS`.

### Persistent Root Layers vs. Transitioning Stage

| Layer | Component / Element | Position on `16:9` (`1920x1080`) | Transition Rule |
| :--- | :--- | :--- | :--- |
| **Layer 0: Canvas** | `#F2F0FA` Cool White (or `#003A40` Emerald) | `0, 0, 1920x1080` | **Persistent** : never transitions. |
| **Layer 0B: Corner Chevrons** | `GLM_MOTION_PREFERENCES.chevrons` | Top-Left Emerald + Bottom-Right Lime | **Persistent Architectural Framing** : scales to `0.55x` in content, `1.0x` on end card. |
| **Layer 1: Center Stage** | `<TransitionSeries>` host | `top: 140, bottom: 160, left: 100, right: 100` | **Transitioning** : hosts scene slides with smooth transitions. |
| **Layer 2A: Top-Left Lockup** | `GlmLogoLockup` | `top: 54px, left: 72px` (`160px` width) | **Optional** : used for static formats; omitted when Corner Chevrons + Flippy Mascot are active. |
| **Layer 2B: Top-Right Website** | `glmsystems.com` | `top: 54px, right: 72px` (`#003A40`, `22px` Bold) | **Optional** : subtle anchored brand URL on static slides. |
| **Layer 3: Closed Captions** | `GlmCaptions` | Locked at **`Y = 920px`** (`left: 200, right: 200`) | **Persistent** : locked at Y = 920px with zero vertical bounce. |
| **Layer 4: Audio and SFX** | `<Audio />` + `<Sequence>` | Root audio bus | Plays ambient BGM (`bgm-ambient.wav`) and synced SFX cues. |

### Multi-Platform Aspect Ratio Presets (`GLM_CANVAS_PRESETS`)

| Aspect Ratio | Resolution | Top-Left Logo `(left, top)` | Top-Right Website `(right, top)` | Centered Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`16:9`** (LinkedIn / YouTube Widescreen) | `1920x1080` | `(72px, 54px)` | `(72px, 54px)` | `top: 140, bottom: 160, left: 100, right: 100` | **`Y = 920px`** (`34px` ExtraBold) |
| **`4:5`** (LinkedIn / Instagram Portrait) | `1080x1350` | `(72px, 64px)` | `(72px, 64px)` | `top: 160, bottom: 240, left: 72, right: 72` | **`Y = 1140px`** (`32px` ExtraBold) |
| **`9:16`** (Shorts / Reels / Vertical) | `1080x1920` | `(84px, 96px)` | `(84px, 96px)` | `top: 220, bottom: 440, left: 84, right: 84` | **`Y = 1480px`** (`36px` ExtraBold) |
| **`1:1`** (Square Feed) | `1080x1080` | `(60px, 48px)` | `(60px, 48px)` | `top: 130, bottom: 180, left: 60, right: 60` | **`Y = 910px`** (`30px` ExtraBold) |
