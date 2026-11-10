# GLM Systems (glmsystems.com) : Brand Motion Guidelines and Base Canvas Spec

> **Source References**: 
> 1. Official GLM Systems Brand Refresh (*"GLM's new logo and colour scheme"*).
> 2. GLM Corporate Website (`glmsystems.com`) and B2B LinkedIn campaign assets.
> 3. Official Vector SVG Brandmarks (`GLM-BIRD-Color.svg`, `GLM-black-Text-Color-Bird.svg`).
> 
> **Brand Isolation Rule**: These tokens, components, and layout rules apply **exclusively** when the user selects the **GLM** brand in `the-motion-designer` or invokes `/glm-brand-motion`. Never mix these tokens into `the-motion-designer` or other brand profiles (such as Databro).

---

## 1. Full Color Palette (100% Solid Flat Colors : Zero Gradients)

Sampled directly from authentic GLM Systems brand assets:

| Token Name | Hex Code | Visual Role and Usage in GLM Assets |
| :--- | :--- | :--- |
| **`backgroundPrimary`** | `#F1F0FA` | **Cool White** : Clean, spacious lilac-white canvas (`RGB(241, 240, 250)`). Used as the primary background for clean enterprise motion. |
| **`backgroundSecondary`** | `#003A40` | **Emerald** : Deep, technological blue-green (`RGB(0, 58, 64)`). Represents trust and deep software architecture; used for high-contrast cards and full-bleed hero scenes. |
| **`backgroundCard`** | `#FFFFFF` | **Pure White** : Elevated card surface on `#F1F0FA` backdrop (`borderRadius: 16px to 20px`). |
| **`accentPrimary` / `accentLime`** | `#CDFF70` | **Signature GLM Lime** : Electric lime green (`RGB(205, 255, 112)`). Represents energy and AI innovation; fills the GLM dual birds and highlights interactive keywords. |
| **`accentSecondary` / `accentEmerald`**| `#003A40` | **Signature GLM Emerald** : High-contrast partner to Lime. Used for text, badges, and dark callout blocks. |
| **`textPrimary`** | `#111827` | **Dark Charcoal** : Primary headline and body text on Cool White surfaces. |
| **`textSecondary`** | `#4B5563` | **Muted Slate Gray** : Secondary descriptions and ERP metadata. |
| **`textOnDark`** | `#F1F0FA` | **Cool White Text** : High-contrast text on `#003A40` Emerald backgrounds. |
| **`borderSubtle`** | `#E5E7EB` | Subtle 1.5px card border on Cool White backgrounds. |
| **`semanticSuccess`** | `#10B981` | Emerald green for verified data entries and automated tasks. |
| **`semanticWarning`** | `#F59E0B` | Amber for review requests and pending approvals. |
| **`semanticDanger`** | `#EF4444` | Red for inventory stockout warnings and validation errors. |

---

## 2. Vector Icons Standard : React Icons as Single Source of Truth

* **Strict Prohibition**: Never use AI-generated emojis, generic flat AI clipart, or arbitrary doodles.
* **Source of Truth**: Use [React Icons](https://react-icons.github.io/react-icons/) exclusively for all UI and vector icons across Remotion compositions:
  - **`react-icons/lu` (Lucide Icons, Primary Standard)**: `LuBuilding2`, `LuDatabase`, `LuBot`, `LuSparkles`, `LuCheckCircle`, `LuSearch`, `LuMail`, `LuSend`, `LuWorkflow`, `LuLayers`, `LuShieldCheck`, `LuArrowRight`.
  - **`react-icons/tb` (Tabler Icons)**: `TbRobot`, `TbBinaryTree`, `TbArrowsSplit`, `TbDatabase`.
  - **`react-icons/fi` (Feather Icons)**: `FiCheck`, `FiFileText`, `FiSend`.
* **Styling**: Render icons using crisp vector strokes, sized proportionally (`size={32}` to `size={54}`), colored in GLM brand tokens (`#003A40`, `#CDFF70`, `#111827`).

---

## 3. Punctuation Guardrail : Absolute Ban on Em-Dashes (`—`)

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

## 4. Reading Pacing Rules (GLM Minimum Time Standard)

Enterprise software animations require calibrated reading time:

| In-Video Element | Minimum Required On-Screen Time |
| :--- | :--- |
| **Per Spoken / Written Word** | `0.4 seconds` per word |
| **Per New Text Block Entry** | `0.5 seconds` initial eye landing buffer |
| **Minimum per Text Card** | **`2.0 seconds`** minimum visibility |
| **Stillness Buffer after Motion** | **`2.0 seconds`** visual stillness before scene transition |
| **Outro Endcard** | **`2.5 seconds`** minimum hold for GLM logo and website |

---

## 5. Standard GLM Base Content Canvas (`GlmBaseCanvas`)

Every GLM video is built on `GlmBaseCanvas.starter.tsx` and `GLM_CANVAS_PRESETS`.

### Persistent Root Layers vs. Transitioning Stage

| Layer | Component / Element | Position on `16:9` (`1920x1080`) | Transition Rule |
| :--- | :--- | :--- | :--- |
| **Layer 0: Canvas** | `#F1F0FA` Cool White (or `#003A40` Emerald) | `0, 0, 1920x1080` | **Persistent** : never transitions. |
| **Layer 1: Center Stage** | `<TransitionSeries>` host | `top: 140, bottom: 160, left: 100, right: 100` | **Transitioning** : hosts scene slides with smooth transitions. |
| **Layer 2A: Top-Left Lockup** | `GlmLogoLockup` | **`top: 54px, left: 72px`** (`160px` width) | **Persistent** : animates in once at `frame 0..12`, stays stationary. |
| **Layer 2B: Top-Right Website** | `glmsystems.com` | **`top: 54px, right: 72px`** (`#003A40`, `22px` Bold) | **Persistent** : subtle, anchored brand URL. |
| **Layer 3: Closed Captions** | `GlmCaptions` | Locked at **`Y = 920px`** (`left: 200, right: 200`) | **Persistent** : locked at Y = 920px with zero vertical bounce. |
| **Layer 4: Audio and SFX** | `<Audio />` + `<Sequence>` | Root audio bus | Plays ambient BGM (`bgm-ambient.wav`) and synced SFX cues. |

### Multi-Platform Aspect Ratio Presets (`GLM_CANVAS_PRESETS`)

| Aspect Ratio | Resolution | Top-Left Logo `(left, top)` | Top-Right Website `(right, top)` | Centered Stage `(top, bottom, left, right)` | Fixed Closed Caption `Y` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`16:9`** (LinkedIn / YouTube Widescreen) | `1920x1080` | `(72px, 54px)` | `(72px, 54px)` | `top: 140, bottom: 160, left: 100, right: 100` | **`Y = 920px`** (`34px` ExtraBold) |
| **`4:5`** (LinkedIn / Instagram Portrait) | `1080x1350` | `(72px, 64px)` | `(72px, 64px)` | `top: 160, bottom: 240, left: 72, right: 72` | **`Y = 1140px`** (`32px` ExtraBold) |
| **`9:16`** (Shorts / Reels / Vertical) | `1080x1920` | `(84px, 96px)` | `(84px, 96px)` | `top: 220, bottom: 440, left: 84, right: 84` | **`Y = 1480px`** (`36px` ExtraBold) |
| **`1:1`** (Square Feed) | `1080x1080` | `(60px, 48px)` | `(60px, 48px)` | `top: 130, bottom: 180, left: 60, right: 60` | **`Y = 910px`** (`30px` ExtraBold) |
