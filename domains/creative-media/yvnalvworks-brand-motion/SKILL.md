---
name: yvnalvworks-brand-motion
description: "yvnalvworks (@yvnalvworks / yvnalvworks.com) specialized brand motion skill extending the-motion-designer. Applies yvnalvworks' signature technical aesthetic: matte charcoal grain background image (never a flat fill), Poppins Bold headlines with Warm Ivory #F0ECE2 and white text, one Electric Lime #C1FF72 punchline phrase, the avatar plus name and handle lockup above the headline on covers, Lucide 2px monoline SVG icons, and locked Y=1480px captions. Renders 4:5 carousel covers and slides that match the published reference covers, a 9:16 cover for every reel or video, and caption-timed 9:16 Remotion reels where every story beat gets an animated visual (product mockups, charts, step rails, app-style icon tiles, loops) built from the bundled reel starter, then synced to Yovan's recorded voiceover (takes joined, sped up, captions re-timed). Use when creating carousels, covers, slides, or videos for yvnalvworks or invoking /yvnalvworks-brand-motion."
metadata:
  version: 0.7.1
---

# yvnalvworks Brand Motion: Visual Identity and Canvas Engine

Specialized brand motion and visual design skill extending **`the-motion-designer`** exclusively for **yvnalvworks (Yovan Alvianto : yvnalvworks.com / `@yvnalvworks`)**.

This skill isolates all yvnalvworks visual guidelines, typography, color tokens, the grain background, reference covers, Lucide monoline vectors, Remotion canvases, and automated 4:5 carousel slide renderers so they never mix with other brands (such as Databro or GLM).

> [!WARNING]
> **CRITICAL GATE (No Unrequested Visual Generation):**
> Do not generate slide images, videos, or Canva designs without prior confirmation from the user.
> Always review the narrative arc, slide copy, or video script with the user before executing rendering scripts.

---

## When to Use

* When designing or rendering 4:5 Instagram carousel slides and covers for `@yvnalvworks`.
* When producing 9:16 Remotion reels from a reel script and `captions.json`, starting from `assets/reel-starter/`.
* When formatting Lucide 2px monoline SVG vectors and high-contrast technical diagrams.
* When exporting video subtitles or slide decks to `D:\yvnalv\Onedrive\04. yvnalvworks\Contents\`.
* Invoke via slash command: `/yvnalvworks-brand-motion`.

## When NOT to Use

* Do not use for Databro Studio content (use `/databro-brand-motion` instead).
* Do not use for GLM Systems enterprise marketing (use `/glm-brand-motion` instead).
* Do not use for early topic ideation or research before copy is drafted (use `/yvnalvworks-content-ideas` first).

---

## Bundled Resources

| Path | Purpose & When to Load |
|---|---|
| `references/cover-slide-spec.md` | Open for every carousel cover: measured layout, lockup, headline type scale, highlight rule, and review checklist. |
| `references/yvnalvworks-brand-guidelines.md` | Core color tokens, background rule, Poppins typography, and prohibited visuals. |
| `references/yvnalvworks-brand-assets-checklist.md` | Verification checklist for background, avatars, logos, tokens, reference covers, and storage locations. |
| `references/lucide-icon-spec.md` | Technical SVG rules and concept-to-icon mapping for Lucide vectors. |
| `scripts/render_carousel.py` | Playwright renderer on the grain background: 4:5 slides (2160x2700 PNG) or, with `"format": "reel"` (or `--format reel`), the 9:16 reel/video cover (2160x3840 PNG): `python <skill-dir>/scripts/render_carousel.py <spec.json> --out <dir> [--scale 2] [--format feed\|reel]`. A slide's optional `file` sets the output name. `cover` slides take a `headline` (`\n` breaks, `[[...]]` lime); `html` slides take a fragment (wrapped in the brand shell) or a full document with `{{BG}}`, `{{AVATAR}}`, `{{FONTS}}` tokens. Prints JSON; exits 1 if Poppins failed to load or a hand-broken cover line overflowed the 860px measure and wrapped. |
| `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png` | The background of every slide and video frame (matte charcoal grain). Never substitute a flat fill. |
| `assets/reference-covers/cover-ref-listicle-ai-updates.jpg` | Published listicle cover. Compare renders against it. |
| `assets/reference-covers/cover-ref-should-know-maf.jpg` | Published "What X Should Know About Y" cover. Compare renders against it. |
| `assets/brand-kit/guidelines/yvnalvworks.tokens.json` | Machine-readable design tokens: colors, background, typography, cover layout, safe zones. |
| `assets/brand-kit/logos/yovan-avatar-color.png` | Color avatar used in the cover lockup (66px circle). |
| `assets/brand-kit/logos/yovan-avatar.png` | Grayscale 1080px headshot for large placements. |
| `assets/brand-kit/logos/yvnalvworks-logo-transparent.png` | Official transparent wordmark logo. |
| `references/voiceover-sync.md` | Open when Yovan has recorded the voiceover: match takes to scenes, speed (default 1.2x), align, refine, render with voice, deliver. |
| `references/reels-motion-system.md` | Open for every reel: centered layout, caption-driven timing, story beat to visual patterns, motion rules, color meaning, icons, captions, deliverables and QA. |
| `assets/reel-starter/README.md` | How to copy the starter into `D:\yvnalv\AI Skills\remotion-demos\<reel-name>\`, add brand assets and captions, and render. |
| `assets/reel-starter/package.json` | Pinned Remotion 4.0.542, lucide-react 0.460.0, React 18; `sync`, `studio`, `typecheck`, `render`, `render:clean` scripts. |
| `assets/reel-starter/tsconfig.json` | TypeScript config (JSON imports enabled). |
| `assets/reel-starter/remotion.config.ts` | JPEG frames at quality 95, overwrite output. |
| `assets/reel-starter/src/index.ts` | Registers the root. |
| `assets/reel-starter/src/Root.tsx` | Two compositions: `YvnalvworksReel` (captions) and `YvnalvworksReelClean`. |
| `assets/reel-starter/src/Reel.tsx` | Example three-scene reel plus end card; replace the scenes, keep the structure. |
| `assets/reel-starter/src/theme.ts` | Poppins and JetBrains Mono loading, color tokens, centered layout constants (center x 540, content x 120 to 960, captions y 1480). |
| `assets/reel-starter/src/timing.ts` | Caption-keyed timing: `at(id)`, `until(id)`, `pop`, `ease`, `span`, `mix`, `rand`. |
| `assets/reel-starter/src/components/Base.tsx` | Background, TopLockup, Captions, Wipe, AppTile, Tag. |
| `assets/reel-starter/src/components/Patterns.tsx` | Panel, StepHeading, PhoneFrame, LineChart, Meter, StepRail, EndCard, morph. |
| `assets/reel-starter/src/voiceover.ts` | `VOICEOVER_FILE`: null renders silent; set to the aligned file in `public/` to add the voice. |
| `assets/reel-starter/scripts/transcribe.mjs` | whisper.cpp 1.5.5 `small.en` (local): transcript and rough word times per WAV, to confirm which take is which scene and what was said. |
| `assets/reel-starter/scripts/align_voiceover.py` | Joins the takes, normalizes loudness, applies the speed, and times every caption from pauses and syllables. |
| `assets/reel-starter/scripts/refine_captions.py` | Snaps mid-phrase cue starts to Whisper word times on the final audio. |
| `assets/reel-starter/src/data/captions.json` | Example captions (from the content-ideas reel starter); replace with the reel's real captions. |

---

## Visual Design Standard

1. **Background**: the grain image `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png` scaled with `cover` on every slide and frame. `#121212` is only the fallback behind it, never the visible background.
2. **Typography**:
   - `Poppins` for headlines, lockup, and body. Headlines 700 Bold, tracking `-0.04em`, line height `1.02`; subheadings 600; body 400.
   - `JetBrains Mono` or `Geist Mono` (500) for slide counters (`01 / 05`), code blocks, and metrics.
3. **Color**: headlines `#FFFFFF`, handle and body `#F0ECE2` Warm Ivory, secondary `#8E8E93`, muted `#71717A`.
4. **Accent Highlight**: `Electric Lime` (`#C1FF72`) on exactly one punchline phrase per slide, and as solid backgrounds for framework cards.
5. **Cover (slide 1, and every reel or video)**: color avatar + `yvnalvworks` / `@yvnalvworks` lockup above a 96px Poppins Bold headline of 3 to 4 hand-broken lines, left-aligned text in an optically centered block, nothing else on the slide. Reels and videos always get the same cover at 9:16 (`reel-cover.png`). Full spec: `references/cover-slide-spec.md`.
6. **Copy on slides**: Render copy as the flowing sentences delivered by `/yvnalvworks-content-ideas`. Never chop body copy into fragment bullets or ALL CAPS labels; give sentences room to breathe (body 28 to 32px, line height 1.45).
7. **Lucide Monoline Icons**: strict 2px stroke width, rounded caps, rounded joins, zero fills, 24x24 viewBox.
8. **Reels Safe Zones (9:16)**:
   - Header safe area: 0 - 150px
   - Bottom interaction safe area: 1640 - 1920px
   - Right action strip: 960 - 1080px
   - Closed Captions locked at: Center Y = 1480px
   - Caption style: sentence case breath groups (3 to 9 words, max 48 characters, up to two lines) from the script, Poppins 600, white, no ALL CAPS
   - Hook: the hook visual is on screen from frame 0 (no fade-in or logo intro), and one hero object travels through the story instead of a deck of titled panels (`references/reels-motion-system.md`, section 1b)

---

## Workflow

1. **Confirm copy.** Get the approved slide copy or script (usually from `/yvnalvworks-content-ideas`). For the cover, confirm the headline line breaks and the single lime phrase.
2. **Build the spec.** Slide 1 is a `cover` slide. Body slides are `html` fragments that use Poppins, Lucide icons, and the lime accent; the renderer puts them on the grain background.
3. **Render** with `scripts/render_carousel.py` to the agreed folder under `D:\yvnalv\Onedrive\04. yvnalvworks\Contents\`. If the JSON reports a Poppins warning, fix connectivity and re-render; do not ship fallback fonts. If it reports a cover overflow warning, re-break the headline (for example "Should Know / About [[Subject]]") and re-render.
4. **Compare.** View the rendered cover next to a file in `assets/reference-covers/` and walk the checklist in `references/cover-slide-spec.md`. Fix any drift in scale, position, background, or highlight before handing over.
5. **Reels.** Open `references/reels-motion-system.md`. Copy `assets/reel-starter/` to `D:\yvnalv\AI Skills\remotion-demos\<reel-name>\` (see its README), put the reel's `captions.json` in `src/data/`, and plan one animated visual per story beat keyed to its caption cue with `at(id)`. Keep content centered on x 540, typecheck, render both versions (captions and clean), render the 9:16 cover from the reel's `cover-spec.json` (`reel-cover.png`), sample a frame from every scene and check centering, safe zones, and overlaps, then copy both MP4s next to the cover in the reel's OneDrive folder.
6. **Voiceover.** When the recording arrives, follow `references/voiceover-sync.md`: confirm each take's scene and wording, apply the speed (ask; Yovan's default is 1.2x), align and refine the captions, set `VOICEOVER_FILE`, re-render both versions with voice, check every beat still finishes in time, and deliver the final audio and aligned captions.

---

## Definition of Done

A task run of `yvnalvworks-brand-motion` is complete when:
1. Concept and copy were confirmed with the user prior to visual rendering.
2. Every slide or frame sits on the grain background image, not a flat fill.
3. Design complies with yvnalvworks tokens (Poppins type, white and Warm Ivory text, one #C1FF72 phrase).
4. The cover matches the reference covers in layout, lockup, and type scale.
5. All icons follow authentic Lucide 2px monoline SVG specifications.
6. Reels: every story beat has an animated visual keyed to its caption, content is centered on x 540, charts carry an `illustrative` tag, no third-party logos, and both MP4s (captions and clean) plus `reel-cover.png` are in the reel folder.
7. Voiced reels: captions are aligned to the real audio (report the median timing error), both MP4s carry the voice, and the final audio plus aligned captions are in the reel folder.
8. Rendered slides or videos were output to the designated directory and visually inspected.
