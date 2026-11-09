# Remotion Export Formats, Codecs & Render Commands

This reference provides the exact, verified CLI commands (`npx remotion render` and `npx remotion still`) and programmatic options for every output format supported by Remotion v4.x.

---

## 1. Quick Export Format Matrix

| Deliverable Type | File Extension | `--codec` | Extra Required Flags | Supports Alpha (Transparency)? | Best For |
|---|---|---|---|---|---|
| **Standard Social / Web Video** | `.mp4` | `h264` *(default)* | `--crf=18` *(high quality)* | No | Instagram, TikTok, YouTube, LinkedIn, Facebook, X |
| **High-Efficiency MP4** | `.mp4` | `h265` | `--crf=22` | No | Smaller file size for Apple/modern devices |
| **Web Video (Opaque)** | `.webm` | `vp8` or `vp9` | `--crf=20` | No | Lightweight web embeds |
| **Web Video (Transparent Overlay)** | `.webm` | `vp9` | `--image-format=png --pixel-format=yuva420p` | **Yes** | Transparent web animations & browser overlays |
| **Pro Video / Alpha Overlay** | `.mov` | `prores` | `--prores-profile=4444 --image-format=png --pixel-format=yuva444p10le` | **Yes** | Lower-thirds, stingers, Premiere / DaVinci / Final Cut |
| **Animated Loop** | `.gif` | `gif` | `--every-nth-frame=2` *(optional size reduction)* | Yes (1-bit) | GitHub READMEs, documentation, Slack/Teams |
| **Lossless Frame Sequence** | `folder/element-0001.png` | *(none)* | `--sequence --image-format=png` | **Yes** | VFX compositing pipelines |
| **Single Still Frame (Lossless)** | `.png` | *(still CLI)* | `npx remotion still --image-format=png` | **Yes** | Thumbnails, UI cards, transparent badges |
| **Single Still Frame (Web/Social)** | `.webp` / `.jpeg` | *(still CLI)* | `npx remotion still --image-format=webp` | Yes (`webp`) | Fast-loading OpenGraph cards & social banners |
| **Vector / Printable Slide** | `.pdf` | *(still CLI)* | `npx remotion still --image-format=pdf` | N/A | Printable slide decks, one-pagers, posters |
| **Audio Track Only** | `.wav` / `.mp3` / `.aac` | `wav` / `mp3` / `aac` | None | N/A | Exporting mixed voiceover + SFX audio stems |

---

## 2. Exact CLI Render Commands

### A. High-Quality Social Media MP4 (`H.264`)
```bash
npx remotion render src/index.ts <CompositionId> out/video.mp4 --codec=h264 --crf=18
```
* `--crf=18` produces visually lossless H.264 output (default is `23`; lower = higher quality).

### B. Transparent Motion Overlay — Apple ProRes 4444 (`.mov`)
Use when exporting lower-thirds, logo stingers, or floating UI badges to layer over footage in Premiere Pro, DaVinci Resolve, CapCut, or Final Cut:
```bash
npx remotion render src/index.ts <CompositionId> out/overlay.mov \
  --codec=prores \
  --prores-profile=4444 \
  --image-format=png \
  --pixel-format=yuva444p10le
```
* Ensure your Remotion composition root does **not** set an opaque background color (`backgroundColor: 'transparent'`).

### C. Transparent Web Video — WebM Alpha (`VP9`)
```bash
npx remotion render src/index.ts <CompositionId> out/overlay.webm \
  --codec=vp9 \
  --image-format=png \
  --pixel-format=yuva420p
```

### D. Animated GIF Loop (for Docs & READMEs)
```bash
npx remotion render src/index.ts <CompositionId> out/demo.gif --codec=gif
```
* Tip: For smaller GIF file sizes on 60fps compositions, pass `--every-nth-frame=2` (renders at 30fps) or `--scale=0.75`.

### E. PNG Frame Sequence
```bash
npx remotion render src/index.ts <CompositionId> out/frames --sequence --image-format=png
```

### F. Single Still Image or PDF Slide (`npx remotion still`)
```bash
# High-DPI PNG (2x retina scale)
npx remotion still src/index.ts <CompositionId> out/thumbnail.png --frame=45 --image-format=png --scale=2

# WebP Banner
npx remotion still src/index.ts <CompositionId> out/banner.webp --frame=0 --image-format=webp

# Printable PDF Document / Slide
npx remotion still src/index.ts <CompositionId> out/slide.pdf --frame=0 --image-format=pdf
```

### G. Passing Custom Brand / Content Props via CLI (`--props`)
You can override any Zod/React prop at render time using a JSON string or a path to a `.json` file:
```bash
npx remotion render src/index.ts MainPromo out/glm-reel.mp4 \
  --props='./props/glm-launch.json'
```

