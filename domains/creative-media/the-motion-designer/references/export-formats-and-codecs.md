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

---

## 3. Editable NLE & Canvas Export Package (CapCut & Canva)

When users want to continue editing, modifying colors, or restyling animations inside **CapCut** or **Canva**, rendering a single flattened `.mp4` file is insufficient because text, audio, and color fills are permanently baked into pixels.

To enable seamless post-editing in CapCut and Canva, the motion designer exports a **5-Layer Editable Asset Package**:

```
out/editable-editing-pack/
├── subtitles/
│   └── captions.srt                # Standard SubRip subtitles for live font/style editing
├── audio-stems/
│   ├── voiceover-stem.wav          # Clean voiceover track (unmixed)
│   ├── music-bed-stem.wav          # Clean background music track
│   ├── sfx-stem.wav                # Synchronized UI sound effects track
│   └── full-mix.mp3                # Complete reference mix
├── vector-assets/                  # Native SVG vectors with changeable color layers
│   ├── mascot-character.svg        # Clean vector paths (Canva surfaces color swatches)
│   ├── icons/                      # Individual Lucide/React icon vector SVGs
│   └── ui-components/              # Badges, prompt chips, and speech balloons
├── transparent-overlays/           # Alpha video tracks for CapCut overlays
│   └── mascot-overlay.mov          # Apple ProRes 4444 with alpha channel
└── scene-clips/                    # Modular video clips per scene
    ├── scene01.mp4
    ├── scene02.mp4
    └── ...
```

### CapCut Continuation Workflow

1. **Video & Overlay Import**:
   - Create a new project in CapCut (16:9 or 9:16).
   - Drag modular `scene-clips/` onto the main video track.
   - Drag `transparent-overlays/mascot-overlay.mov` onto an upper track. Because it is encoded with ProRes 4444 (`yuva444p10le`), CapCut recognizes the alpha channel automatically with zero green screen keying.
2. **Audio Stems Mixing**:
   - Drag `voiceover-stem.wav` to Audio Track 1.
   - Drag `music-bed-stem.wav` to Audio Track 2 and set CapCut's "Auto-Ducking" or lower volume to -18dB.
   - Drag `sfx-stem.wav` to Audio Track 3.
3. **Editable Subtitles**:
   - Navigate to **Text > Local Captions > Import `.srt`**.
   - Select `subtitles/captions.srt`.
   - CapCut instantly populates an editable subtitle timeline track. Select all captions to change font type, font size, stroke color, glow, or apply CapCut animated text presets in one click.

### Canva Video Continuation Workflow

1. **Changeable Color Vector Assets (`.svg`)**:
   - Canva parses SVG vector files with distinct `fill="..."` and `stroke="..."` attributes (up to 5 solid colors) and **displays color swatches in the top toolbar**.
   - In Canva, navigate to **Uploads > Upload files** and select the SVGs from `vector-assets/`.
   - Place an SVG (e.g. Mascot, Card, or Icon) on any video page. Click the element: Canva's top toolbar displays the color boxes, allowing users to swap brand colors in real time.
2. **Modular Scene Video Pages**:
   - Add a page in Canva Video for each scene.
   - Drag each clip from `scene-clips/` onto its corresponding Canva page.
3. **Captions & Audio**:
   - Upload `voiceover-stem.wav` and `music-bed-stem.wav` to Canva's Audio tab.
   - Upload `subtitles/captions.srt` to attach synchronized captions across pages.

