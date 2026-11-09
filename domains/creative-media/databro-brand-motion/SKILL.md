---
name: databro-brand-motion
description: "Databro Studio (@databroid) specialized brand motion skill extending the-motion-designer. Applies Databro's isolated visual identity for Remotion videos: #111111 solid matte charcoal canvas, #BFFF72 lime green and #F2EBE1 warm cream accents, fixed top-left Databro avatar with Belajar Data Science sub-label (no top-right box), typewriter block-cursor hooks, center-locked cardless stage with #F2EBE1 cream emblem circles or terminal/UI frames with #D92D20 red callout boxes, and cardless 2-to-4 word uppercase ExtraBold white Closed Captions. Use when the user selects the Databro brand in the-motion-designer or invokes /databro-brand-motion. Never mix with GLM or other brands."
metadata:
  version: 0.1.0
---

# Databro Brand Motion — `@databroid` Visual Identity for Remotion

Specialized brand skill extending **`the-motion-designer`** exclusively for **Databro Studio (`@databroid` — "Belajar Data Science")**.

This skill isolates all Databro brand guidelines, colors, typography, logo lockups, and scene choreography patterns so they never contaminate `the-motion-designer` or any other brand skill (such as `GLM`).

```text
Load Databro Tokens (#111111, #BFFF72, #F2EBE1) → Lock Top-Left Avatar Header → Center Cardless Stage → Render Cardless 2-4 Word Uppercase CC
```

## When to Use

* Generating TikTok, Instagram Reels, YouTube Shorts, or educational data science / AI motion videos for **Databro Studio (`@databroid`)**.
* When the user selects **Databro** during Step 1 of `the-motion-designer`'s Pre-Generation Option Wizard.

Do not use it for: any non-Databro brand (such as GLM or neutral client projects).

## Bundled Resources

Paths are relative to this skill's base directory.

| File | Open it when |
|---|---|
| `references/databro-brand-guidelines.md` | Reviewing Databro Studio's exact color hexes (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), typography, scene templates, and Closed Caption rules. |
| `assets/databro-avatar.jpg` | Copying the official Databro Studio circular illustrated portrait into a Remotion project's `public/databro-avatar.jpg`. |
| `assets/databro.brand.starter.ts` | Importing Databro's isolated TypeScript tokens (`DATABRO_BRAND`) into a Remotion project. |
| `assets/DatabroLogoLockup.starter.tsx` | Rendering the fixed top-left Databro avatar + `Databro` / `Belajar Data Science` lockup component. |
| `assets/DatabroCaptions.starter.tsx` | Rendering Databro's signature cardless, 2-to-4 word ALL-CAPS ExtraBold white Closed Captions (`Y: 1180–1260px`). |

---

## Databro Signature Visual Rules (Overrides Default Generic SaaS Cards)

### 1. Solid Matte `#111111` Canvas & Cardless Minimalist Stage
* **Canvas Background**: Always solid **`#111111`** (Matte Charcoal Black).
* **No Generic Dark-Blue SaaS Dashboard Cards**: Do not wrap scenes in `#131B2E` slate boxes or multi-column metric grids. Elements float directly on the `#111111` canvas, vertically and horizontally centered (`X = 540px`).
* **Exact Brand Palette (Zero Gradients)**:
  * **Canvas**: `#111111`
  * **Primary Accent (Databro Lime Green)**: `#BFFF72`
  * **Badge / Emblem Circle Surface (Warm Cream)**: `#F2EBE1`
  * **Primary Text**: `#FFFFFF`
  * **Sub-label Text**: `#B3B3B3`
  * **UI / Terminal Callout Box Stroke**: `#D92D20` (`3px` solid red rectangle highlighting key output or buttons)

### 2. Fixed Top-Left Brand Lockup (No Top-Right Box)
* Anchor [`DatabroLogoLockup.starter.tsx`](assets/DatabroLogoLockup.starter.tsx) at **top-left (`left: 88px, top: 220px` on `1080×1920`)**:
  * **Left**: `68×68px` circular Databro avatar (`staticFile('databro-avatar.jpg')`, `#F2EBE1` cream background).
  * **Right (Stacked)**:
    * **`Databro`** (`38px`, Bold `700`, `#FFFFFF`, tight tracking `-0.02em`)
    * **`Belajar Data Science`** (`19px`, Regular `400`, `#B3B3B3`)
* **Never place a top-right step counter or icon box** on Databro videos—keep the top-right completely clean, matching `@databroid`'s real videos.

### 3. The Two Signature Databro Scene Archetypes
Every scene in a Databro video uses one of two centered visual archetypes inside the safe stage (`X: 140..940px`, `Y: 420..1120px`, horizontally and vertically centered):

1. **Archetype A — Emblem Hook / Outro Scene (`00:00–00:08` style)**:
   * **Top Hook Text**: Centered white title (`#FFFFFF`, `50–56px`, SemiBold `600`, 1–2 lines) that types in with a **solid white block cursor (`█`)**.
   * **Center Cream Circle**: A `400×400px` solid **`#F2EBE1` Warm Cream Circle** (`borderRadius: '50%'`) centered at `X = 540px`, containing a bold minimalist black (`#111111`, `strokeWidth: 4–6px`) line-art icon/illustration and optional bold uppercase black label inside the bottom of the circle.
   * **Giant Lime Display Keyword**: Directly below the circle, a giant **`#BFFF72` Lime Green** display title (`104–120px`, ExtraBold `800`) that pops in with a snappy spring.
2. **Archetype B — Terminal / Window Action Scene (`00:16–01:20` style)**:
   * **Top Instruction Line**: Centered above the window (`40–44px`, Bold `700`), combining `#FFFFFF` action verb + **`#BFFF72` Lime Green** target phrase (e.g., `Query jalan ` + `#BFFF72` `"10x Lebih Cepat"` or `Run queries ` + `#BFFF72` `"10x Faster"`).
   * **Centered Window / Command Prompt Frame**: A clean, realistic dark terminal (`#0C0C0C` body with `#1F1F1F` title bar: `Command Prompt` tab + `+` and window controls) or clean app frame centered horizontally and vertically at `X = 540px`.
   * **Typewriter Command + Red `#D92D20` Callout Box**: Commands type in character-by-character via `useCurrentFrame()`, followed by the output highlighted inside a crisp **`3px solid #D92D20` red rectangle** so the viewer's eye immediately locks onto the result.

### 4. Cardless 2–4 Word Uppercase Closed Captions (`DatabroCaptions`)
* Unlike generic pill captions, Databro's Closed Captions ([`DatabroCaptions.starter.tsx`](assets/DatabroCaptions.starter.tsx)) have:
  * **Zero background box / zero border** (pure floating text on `#111111`).
  * **Short 2-to-4 word chunks** switching in sync with the voiceover cadence.
  * **ALL-CAPS, ExtraBold (`800`–`900`), `#FFFFFF`**, `36–40px`, centered horizontally (`X = 540px`) at **`Y: 1180–1260px`** (safely above TikTok & Instagram Reels bottom captions and clear of the right-side engagement buttons).

---

## Definition of Done

* `DATABRO_BRAND` tokens (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`) are used with zero CSS gradients and zero cross-brand leakage.
* Top-left `Databro / Belajar Data Science` lockup with `databro-avatar.jpg` is fixed in position, with no top-right clutter.
* Scenes use Databro's centered Emblem Circle or Terminal/UI Callout archetypes rather than generic SaaS dashboard cards.
* Closed Captions render as cardless 2–4 word ALL-CAPS `#FFFFFF` chunks at `Y: 1180–1260px`.
* `validate_remotion_project.py` from `the-motion-designer` passes with `0 errors`.
