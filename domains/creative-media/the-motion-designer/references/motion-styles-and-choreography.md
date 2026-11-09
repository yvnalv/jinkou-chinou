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

---

## 4. Anti-AI Visual & Copy Craft Rules (`the-uix-designer` Standard)

To prevent generated videos from looking generic or "AI-generated", strictly enforce these craft rules derived from `the-uix-designer`:

1. **Solid Flat Semantic Colors Only (Zero Gradients & Zero Blurry Orbs)**:
   * **Never use `linear-gradient`, `radial-gradient`, `conic-gradient`, gradient text (`WebkitBackgroundClip: 'text'`), or blurry background glow orbs (`filter: 'blur(...)'`).**
   * Build hierarchy through **solid surface elevation**: a dark slate canvas (`#0B0F17`), a lighter solid surface card (`#131B2E`), a crisp `1px` solid border (`#1E293B`), high-contrast primary text (`#F8FAFC`), muted secondary text (`#94A3B8`), and 1–2 solid accent colors (`#0EA5E9`, `#10B981`) that pass WCAG 2.2 AA contrast.
2. **Center-Locked Main Container + Fixed Top-Left / Top-Right Header**:
   * Anchor the **Brand Logo / Wordmark at top-left** and the **Scene Icon / Step Indicator at top-right** in a fixed header bar inside the safe zone.
   * Keep the **main content container vertically and horizontally centered** (`left === right`, `display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'`).
3. **Human UX Writing & Sentence Case (Zero AI Punctuation Slop)**:
   * **Sentence case** for all headings, badges, labels, and captions (`"10x faster query speed"`, not `"HIGHLIGHT 01 // VECTORIZED ENGINE"`).
   * **Banned punctuation & symbols**: Never use em-dashes (`—`), double-slash coder labels (`//`), arrow characters (`→`), middle-dot chains (`·`), or emoji/dingbat icons (`✓`, `✨`, `🚀`, `⚡`, `🔥`).
   * **Geometric SVG Icons Only**: When an icon is needed (such as the top-right header icon or status check), render a clean inline `<svg>` path (`width={20} height={20} strokeWidth={2} fill="none"`) on a `4px` grid.
4. **4px / 8px Spacing Scale & Tabular Numbers**:
   * Use spacing tokens strictly from `4, 8, 12, 16, 24, 32, 48, 64px` and always set `fontVariantNumeric: 'tabular-nums'` on animated numbers.

