# Motion Styles, Spring Physics & Choreography Guide

Great motion design feels intentional, physical, and rhythmic rather than linear or mechanical. Use these presets and choreography rules when implementing scenes in Remotion.

---

## 1. Standard Spring Physics Presets (`SpringConfig`)

Never use raw linear interpolation (`interpolate(frame, [0, 30], [0, 100])`) for UI movement or scale reveals unless animating a progress bar or constant-speed marquee. Use `spring()` with one of these four physical personalities:

| Preset Name | `config` Values | Visual Feel | Best Used For |
|---|---|---|---|
| **`snappy`** | `{ damping: 18, stiffness: 220, mass: 0.8 }` | Crisp, responsive, minimal overshoot | SaaS UI cards, cursor clicks, badge pops, kinetic typography words |
| **`smooth`** | `{ damping: 200, stiffness: 100, mass: 1.0 }` | Critically damped (zero bounce), silky deceleration | Camera pans/zooms, enterprise explainer slides, modal entrances |
| **`bouncy`** | `{ damping: 11, stiffness: 160, mass: 0.9 }` | Playful elastic overshoot | Social media hooks, stickers, celebratory checkmarks, consumer promos |
| **`heavy`** | `{ damping: 26, stiffness: 90, mass: 1.8 }` | Weighty, cinematic inertia | 3D device rotations, full-screen hero reveals, large data charts |

---

## 2. The 5 Core Video / Motion Styles

### Style 1: SaaS UI & Product Walkthrough
* **Visual Language**: Elevated glass/card containers (`borderRadius: 16–24px`), subtle multi-layer shadows, crisp `1px` borders (`rgba(255,255,255,0.12)`), and focused UI spotlighting.
* **Camera Rig Pattern**: Wrap the UI mockup in a parent camera container that smoothly scales (`1.0 -> 1.35`) and translates (`translateX`, `translateY`) using the `smooth` spring preset to focus on the active button or form field right before a simulated cursor clicks it.
* **Stagger Rule**: Stagger list items or dashboard metric cards by `4` to `6` frames (`delay: index * 5`).

### Style 2: Kinetic Typography & Social Reel
* **Visual Language**: Bold display typography (`72px–110px` on `1080p`), high contrast, fast cuts (`45–75` frames per phrase), and word-by-word spring entrances (`translateY: 40 -> 0` + `opacity: 0 -> 1`).
* **Hook Rule**: The first **15 frames (0.5 seconds)** must already display the visual hook or headline motion—never leave frames `0–15` completely blank on social media feeds!

### Style 3: Enterprise / Corporate Explainer
* **Visual Language**: Structured grid layouts, generous whitespace, brand lower-thirds, step numbers (`01`, `02`, `03`), and clean `<TransitionSeries>` wipes or slides (`15–20` frames).
* **Pacing**: Allow `90–150` frames (`3–5 seconds`) per concept so viewers can read technical labels comfortably.

### Style 4: Data Storytelling & Infographics
* **Visual Language**: Animated number counters (`Math.round(interpolate(...))` formatted with `.toLocaleString()`), SVG path line charts (`evolvePath()`), and staggered bar growth.
* **Label Rule**: Animate the bar/line first (`delay: 0`), then pop the final value badge at the peak (`delay: 18`).

### Style 5: 3D & Shader Motion
* **Visual Language**: `<ThreeCanvas>` 3D device/logo rotations driven by `useCurrentFrame()`, or `@remotion/skia` gradient mesh / blur shaders.
* **Lighting**: Always include ambient + directional/spot lights so 3D materials have clean specular highlights.

---

## 3. Choreography & Timing Checklist

1. **Frame-0 Thumbnail Readiness**: Many platforms use Frame `0` (or the first 0.5s) as the default feed preview if no custom cover is uploaded. Ensure Frame `0` has a styled background and visible brand/hook element (or start the main title spring at `from: 0.85, to: 1` on Frame `0`).
2. **Overlapping Action (Follow-Through)**: Never animate `opacity`, `translateY`, and `scale` of a card, its title, its subtitle, and its CTA button on the exact same frame. Stagger them by `3–5` frames (`card: 0f`, `title: 4f`, `subtitle: 8f`, `cta: 12f`).
3. **Exit Before Transition**: Keep elements stable for at least `20–30` frames (`~0.7–1.0s`) after their entrance finishes so the viewer's eye can read them before the next `<TransitionSeries.Transition>` begins.

