# Motion Storyboard & Frame Specification: [Project / Video Title]

**Brand Profile:** [e.g. GLM / Databro / Custom Folder / Neutral]  
**Deliverable Type:** [e.g. MP4 Video (H.264) / ProRes 4444 Alpha Overlay / GIF Loop / Still PNG]  
**Motion Style:** [e.g. SaaS UI Walkthrough / Kinetic Typography / Enterprise Explainer / Data Infographic]  
**Target Platform & Preset:** [e.g. Instagram Reels (`9:16`, `1080×1920`) / Universal Vertical / YouTube `16:9`]  
**Frame Rate & Total Duration:** `[30 or 60] fps` · `[N] seconds` (`[TotalFrames] frames`)  

---

## 1. Brand Token & Asset Mapping

| Token / Asset | Value / Path | Source Verification |
|---|---|---|
| **Primary Background** | `[#HEX]` | `[Brand Guidelines / User Confirmed]` |
| **Primary / Secondary Accent** | `[#HEX / #HEX]` | `[Brand Guidelines / User Confirmed]` |
| **Heading / Body Font** | `[Font Name / Weight]` | `[Google Fonts / staticFile()]` |
| **Brand Logo File** | `staticFile('[brands/name/logo.svg]')` | `[Verified in public/]` |
| **Spring Physics Personality** | `[snappy / smooth / bouncy / heavy]` | `[Motion Style Preset]` |

---

## 2. Platform UI Safe-Zone Configuration

* **Canvas Resolution**: `[Width] × [Height] px`
* **Protected Dead Zones**:
  * **Top Inset**: `[e.g. 285 px]` *(Clear of status bar / platform header)*
  * **Bottom Inset**: `[e.g. 672 px]` *(Clear of username, caption, audio marquee, scrubber)*
  * **Left / Right Insets**: `Left [60 px]` / `Right [120–192 px]` *(Clear of Like/Comment/Repost/Share buttons)*
* **Safe Content Bounding Box**: `X: [60..888 px]`, `Y: [288..1040 px]`
* **Closed Caption (CC) Safe Band**: `X: [60..888 px]`, `Y: [1040..1220 px]` *(Guaranteed visible in 9:16 and 4:5 feed crop)*

---

## 3. Scene-by-Scene Frame Budget & Choreography

> **Transition Overlap Note**: Total Composition Frames $= \sum \text{Scene Frames} - \sum \text{Transition Frames} = [\text{TotalFrames}]$.

| Scene # | Scene ID & Purpose | Duration (s / frames) | Global Frame Range | Visual Choreography (`useCurrentFrame()`) | On-Screen Copy / Subtitle (CC) | Transition Out |
|---|---|---:|---:|---|---|---|
| **01** | `HookScene` — Opening Hook | `3.0s` (`90f`) | `0 – 89` | `[e.g. Brand badge pops at 0f; headline springs up at 5f (snappy); UI card tilts in at 15f]` | `"[Exact headline / voiceover line 1]"` | `slide('from-bottom')` (`15f`) |
| **02** | `FeatureScene` — Core Demo | `4.5s` (`135f`) | `75 – 209` | `[e.g. Camera zooms 1.0->1.3x to button at 20f; cursor clicks at 45f; result toast springs in at 52f]` | `"[Exact feature callout / voiceover line 2]"` | `fade()` (`15f`) |
| **03** | `OutroCtaScene` — Call to Action | `3.5s` (`105f`) | `195 – 299` | `[e.g. Logo centers with spring; CTA pill pulses subtly via Math.sin(frame/8); URL reveals]` | `"[Exact CTA text & URL]"` | None (Hold final `30f`) |

---

## 4. Verification & Export Plan

1. **Studio Preview Command**: `npx remotion studio` *(with `showSafeZoneGuide: true` to inspect UI margins)*
2. **Validator Check**: `python <skill-dir>/scripts/validate_remotion_project.py --path .`
3. **Final Render Command**:
   ```bash
   npx remotion render src/index.ts [CompositionId] out/[filename].[ext] --codec=[h264|prores|vp9|gif]
   ```

