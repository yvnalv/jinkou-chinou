# Databro Studio (`@databroid`) Brand Motion Guidelines

Extracted from Databro Studio's official TikTok (`@databroid` / *"Help people to make the right data-driven decision"*). Keep this brand completely isolated from `the-motion-designer` core defaults and other brand skills.

---

## 1. Brand Identity & Fixed Top-Left Lockup

* **Brand Name**: `Databro`
* **Sub-label**: `Belajar Data Science`
* **Avatar Mark**: `assets/databro-avatar.jpg` — Circular warm cream (`#F2EBE1`) badge featuring the black-and-cream illustrated Databro creator portrait.
* **Header Placement (`1080 × 1920` Vertical Canvas)**:
  * **Position**: Fixed at `left: 88px`, `top: 220px` (sits cleanly below the OS status bar and remains visible in both `9:16` full-screen and `4:5` feed preview).
  * **Layout**: Horizontal flex row (`gap: 18px`, `alignItems: 'center'`):
    * Avatar: `68 × 68 px` circle (`borderRadius: '50%'`).
    * Text Stack:
      * Line 1: `Databro` (`fontSize: 38px`, `fontWeight: 700`, `color: '#FFFFFF'`, `lineHeight: 1.05`).
      * Line 2: `Belajar Data Science` (`fontSize: 19px`, `fontWeight: 400`, `color: '#B3B3B3'`, `lineHeight: 1.2`).
  * **Top-Right Rule**: Leave the top-right corner completely empty. Do not add step counters or grid icons.

---

## 2. Color Palette (100% Solid Flat Hex Tokens)

| Role | Hex | Usage |
|---|---|---|
| **Canvas Background** | `#111111` | Full-bleed matte charcoal-black canvas across all scenes. Never use gradients or glow orbs. |
| **Primary Accent (Databro Lime)** | `#BFFF72` | Hero display keywords (`Ollama`, `Databro 2.0`), highlighted action words in instruction headers (`Ketik "Download Ollama"`). |
| **Emblem Circle / Badge Cream** | `#F2EBE1` | Central `400×400px` circular emblem badge in hook/outro scenes; matches the avatar background. |
| **Primary Text** | `#FFFFFF` | Hook titles, instruction prefixes, terminal text, and bottom ALL-CAPS Closed Captions. |
| **Secondary Sub-label Text** | `#B3B3B3` | `Belajar Data Science` subtitle and terminal prompt metadata. |
| **Callout Highlight Box** | `#D92D20` | Solid `3px` red rectangular border highlighting key terminal outputs or UI buttons. |
| **Terminal Chrome** | `#1F1F1F` / `#0A0A0A` | Windows Terminal / Command Prompt tab bar (`#1F1F1F`) and console body (`#0A0A0A`). |

---

## 3. Typography & Hierarchy

* **Display & UI Font**: `"Plus Jakarta Sans"`, `"Poppins"`, or `"Inter"` (clean geometric sans-serif).
* **Terminal / Code Font**: `"JetBrains Mono"` or `"Consolas"`, `monospace`.
* **Size Scale (`1080 × 1920` Canvas)**:
  * **Hero Lime Display Word**: `104px – 120px`, `fontWeight: 800`, `color: '#BFFF72'`, `letterSpacing: '-0.03em'`.
  * **Opening Hook Title**: `50px – 56px`, `fontWeight: 600`, `color: '#FFFFFF'`, `lineHeight: 1.22`, centered, with a solid white block cursor (`width: 24px, height: 52px, backgroundColor: '#FFFFFF'`) during the typewriter reveal.
  * **Scene Instruction Header**: `40px – 44px`, `fontWeight: 700`, centered above the terminal/window (`#FFFFFF` verb + `#BFFF72` highlighted target).
  * **Closed Captions (CC)**: `36px – 40px`, `fontWeight: 800`, `textTransform: 'uppercase'`, `color: '#FFFFFF'`, `letterSpacing: '0.01em'`, centered at `Y: 1180–1260px` with **no background box**.

---

## 4. Scene Choreography Patterns

1. **Hook / Emblem Scene**:
   * Frames `0–25`: Opening title types in at the top of the center stage (`Y ≈ 480px`) with a white block cursor (`█`).
   * Frame `18`: Central `#F2EBE1` Warm Cream Circle (`400 × 400 px`) + giant `#BFFF72` Lime Green keyword below it pop in with a snappy spring, accompanied by small decorative 4-point star/dot accents on the right edge of the circle.
2. **Terminal / Action Step Scene**:
   * Top of center stage (`Y ≈ 500px`): Instruction line (`#FFFFFF` + `#BFFF72`).
   * Center of stage (`Y ≈ 580–1060px`): Centered Windows Terminal (`Command Prompt`) window (`width: 820px`, centered at `X = 540px`).
   * Command types in (`C:\Users\databro> ...`), output appears, and a crisp **`3px solid #D92D20` red rectangle** springs in around the key output line to direct viewer attention.
3. **Closed Captions (CC)**:
   * Positioned at `Y: 1180px` (`X = 540px` centered). Displays 2–4 words at a time in bold uppercase white text (`#FFFFFF`) without any pill or card background.

