# Databro Studio (`@databroid`)  :  Brand Assets & Guidelines Checklist

Use this interactive checklist to audit, track, and update all Databro brand assets. Click on any file link to open or edit it directly, or click on folder links to drop new files.

---

## 1. Brand Guidelines, Colors & Token Spec

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`databro.tokens.json`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/guidelines/databro.tokens.json) | **Machine-Readable Brand Tokens**: Stores hex codes (`#111111`, `#BFFF72`, `#F2EBE1`, `#D92D20`), font stack, and preset layout geometry for `9:16`, `4:5`, `1:1`, and `16:9`. | Update hex codes or margins if brand colors change. |
| [x] | [`databro.brand.starter.ts`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/databro.brand.starter.ts) | **TypeScript Brand Module**: Remotion token export (`databroBrand`), spring physics (`bouncy`, `snappy`), and `DATABRO_CANVAS_PRESETS`. | Mirror any hex code or layout coordinate changes made in `databro.tokens.json`. |
| [x] | [`databro-brand-guidelines.md`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/references/databro-brand-guidelines.md) | **Official Brand Motion Guidelines**: Written guide on color usage, safe zones, persistent chrome vs. transitioning stage, and scene archetypes. | Update if design standards or aspect ratio coordinates are revised. |
| [ ] | [`assets/brand-kit/guidelines/pdfs/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/guidelines/pdfs/) | **Official Brand Book PDF Directory**: Storage for official agency brand book PDFs. | Drop official PDF brand guidelines here (e.g. `databro-brand-book-2026.pdf`). |

---

## 2. Persona, Tone of Voice & Script Rules

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`databro-persona.md`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/persona/databro-persona.md) | **Persona & Scriptwriting Rules**: Tone of voice, audience, strict pronoun guardrails (**"Kamu/Anda"**, strictly no "Lo/Gue"), opening hooks, transitions, and sign-offs. | Adjust tone, add new signature catchphrases, or update target audience. |
| [x] | [`databro-content-and-voiceover-guide.md`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/references/databro-content-and-voiceover-guide.md) | **Content Generation Guide**: Content archetypes (tutorials, launches, listicles), Closed Caption synchronization, and prompt templates. | Update prompt templates or scene timing rules. |

---

## 3. Logos & Avatars

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`databro-avatar.jpg`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/databro-avatar.jpg) | **Persistent Top-Left Avatar**: Circular `#F2EBE1` illustrated Databro avatar rendered at `(100px, 108px)` (`64×64px`). | Replace with official circular avatar icon if artwork updates. |
| [x] | [`Databro-Logo.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/Databro-Logo.png) | **Horizontal Logo Wordmark**: Full Databro logo for horizontal video titles or outro screens. | Replace with official high-resolution transparent `.png` or `.svg`. |
| [x] | [`DATABRO-01-rev-yvnalv-(Circle).png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(Circle).png) | **Circular Brand Badge**: High-res circular Databro badge revision. | Primary round badge asset for end screens and callouts. |
| [x] | [`DATABRO-01-rev-yvnalv-(White)-Landscape.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White)-Landscape.png) | **Landscape White Logo**: Horizontal white wordmark for dark headers. | Used in wide 16:9 compositions or YouTube thumbnails. |
| [x] | [`DATABRO-01-rev-yvnalv-(White).png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/DATABRO-01-rev-yvnalv-(White).png) | **Standard White Logo**: High-res Databro white mark revision. | Used across dark cards and intro/outro frames. |
| [ ] | [`assets/brand-kit/logos/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/logos/) | **Logo Assets Directory**: Storage for all brand logos, watermarks, and icons. | Drop new `.svg` vector files or transparent `.png` logos here. |

---

## 4. Typography & Custom Fonts

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | Display Font: `Plus Jakarta Sans` | Loaded via Google Fonts (`weights: 400, 600, 700, 800, 900`). Used for headlines, UI, and captions. | Configured in `databro.brand.starter.ts`. |
| [x] | Mono Font: `JetBrains Mono` | Loaded via Google Fonts (`weights: 400, 500, 700`). Used for code, terminal, and tags. | Configured in `databro.brand.starter.ts`. |
| [ ] | [`assets/brand-kit/fonts/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/fonts/) | **Local Font Directory**: For custom proprietary brand fonts (`.woff2`, `.ttf`, `.otf`). | Drop custom font files here if Databro uses proprietary typography. |

---

## 5. UI Canvas Components (Standard Base Content Canvas)

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`DatabroBaseCanvas.starter.tsx`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/DatabroBaseCanvas.starter.tsx) | **Master Canvas Wrapper**: Persistent `#111111` canvas, persistent logo, fixed `Y=1480px` CC, centered `<TransitionSeries>` stage, and audio bus. | Edit to adjust master canvas layering, stage margins, or default BGM volume. |
| [x] | [`DatabroLogoLockup.starter.tsx`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/DatabroLogoLockup.starter.tsx) | **Top-Left Lockup**: Renders avatar + `Databro` / `Belajar Data Science`. Animates only once at frame 0..12. | Edit to change lockup text, avatar size, or font styling. |
| [x] | [`DatabroCaptions.starter.tsx`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/DatabroCaptions.starter.tsx) | **Fixed Closed Captions**: Locked at `Y = 1480px`, cardless ALL-CAPS `#FFFFFF` ExtraBold chunks with 3-frame crossfade. | Edit to modify caption font size, position, or crossfade duration. |

---

## 6. Graphics, UI Badges & Visual References

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`1.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/1.png), [`2.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/2.png), [`3.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/3.png) | **Numbered Step Badges**: Graphic assets for tutorial steps. | Replace with custom illustrated badges. |
| [x] | [`(Reels) Computer Vision (3).png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/%28Reels%29%20Computer%20Vision%20%283%29.png) | **Reels CV Graphic Reference**: Layout benchmark for visual AI posts. | Reference slide for computer vision tutorials. |
| [x] | [`Table.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Table.png) | **Data Table Graphic**: Reference graphic for database/table scenes. | Replace with brand-styled table illustrations. |
| [x] | [`output.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/output.png), [`output 2.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/output%202.png) | **Terminal Output Graphics**: Reference graphics for terminal output scenes. | Replace with real CLI screenshots or terminal frames. |
| [x] | [`Screenshot 2026-04-25 135828.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Screenshot%202026-04-25%20135828.png) | **UI Reference Screenshot 1**: Benchmark slide layout. | Visual reference for cards and badges. |
| [x] | [`Screenshot 2026-04-25 135852.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Screenshot%202026-04-25%20135852.png) | **UI Reference Screenshot 2**: Benchmark slide layout. | Visual reference for cards and badges. |
| [x] | [`Screenshot 2026-04-25 135944.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Screenshot%202026-04-25%20135944.png) | **UI Reference Screenshot 3**: Benchmark slide layout. | Visual reference for cards and badges. |
| [x] | [`Screenshot 2026-04-25 140023.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Screenshot%202026-04-25%20140023.png) | **UI Reference Screenshot 4**: Benchmark slide layout. | Visual reference for cards and badges. |
| [x] | [`Screenshot 2026-04-25 140040.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Screenshot%202026-04-25%20140040.png) | **UI Reference Screenshot 5**: Benchmark slide layout. | Visual reference for cards and badges. |
| [x] | [`Untitled design.png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Untitled%20design.png), [`Untitled design (1).png`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/Untitled%20design%20%281%29.png) | **Slide Design Assets**: Canvas reference templates. | Background and layout references. |
| [ ] | [`assets/brand-kit/graphics/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/graphics/) | **Graphics Directory**: Storage for reusable icons, badges, stickers, and mascots. | Drop new SVG/PNG graphic elements here. |
| [ ] | [`assets/brand-kit/references/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/references/) | **References Directory**: Storage for benchmark `.mp4` videos and layout screenshots. | Drop past TikTok videos or Figma layout screenshots here. |

---

## 7. TikTok Sound Effects (SFX) & Ambient BGM

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`keyboard-typing.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/keyboard-typing.wav) | **Typing SFX**: Mechanical keyboard typing for typewriter hooks & CLI commands. | Replace with preferred keyboard SFX (`48kHz mono WAV`). |
| [x] | [`pop-up.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/pop-up.wav) | **Bubble Pop SFX**: Synced to `#F2EBE1` cream emblem circle and card spring entries. | Replace with preferred pop SFX. |
| [x] | [`whoosh-transition.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/whoosh-transition.wav) | **Air Whoosh SFX**: Synced to CapCut slide & zoom transitions between scenes. | Replace with preferred whoosh SFX. |
| [x] | [`mouse-click.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/mouse-click.wav) | **UI Click SFX**: Crisp mouse click when buttons highlight or commands trigger. | Replace with preferred click SFX. |
| [x] | [`progress-ticks.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/progress-ticks.wav) | **Progress Ticks SFX**: Rapid digital ticking while progress bars fill. | Replace with preferred ticking SFX. |
| [x] | [`callout-ding.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/sfx/callout-ding.wav) | **Callout Chime SFX**: Harmonic chime when `#D92D20` red callout rectangle locks onto key output. | Replace with preferred notification chime SFX. |
| [x] | [`bgm-ambient.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/bgm/bgm-ambient.wav) | **Ambient BGM Loop**: Warm lo-fi ambient synth pad loop (mixed at `0.07` under voiceover). | Replace with preferred background music track. |

---

## 8. Voiceover Talent Samples & Cloning Config

| Status | Asset / File | Description & Required Specs | Action When Updating |
| :---: | :--- | :--- | :--- |
| [x] | [`VOICE_RECORDING_GUIDE.md`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md) | **Recording Guide & 5-Block Script**: Acoustic specs (`48kHz 24-bit mono WAV`), mic setup, and calibration script. | Read to record the talent voiceover samples. |
| [x] | [`Gang Haji Nasim 12.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2012.m4a) | **Raw Voice Take 12**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 13.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2013.m4a) | **Raw Voice Take 13**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 14.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2014.m4a) | **Raw Voice Take 14**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 15.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2015.m4a) | **Raw Voice Take 15**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 16.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2016.m4a) | **Raw Voice Take 16**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 17.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2017.m4a) | **Raw Voice Take 17**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`Gang Haji Nasim 18.m4a`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/Gang%20Haji%20Nasim%2018.m4a) | **Raw Voice Take 18**: Uploaded talent voice sample. | Ready for audio conversion & cloning. |
| [x] | [`databro-talent-master-calibration.wav`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.wav) | **Master Uncompressed Calibration Audio**: Concat of all 7 takes, `48,000 Hz, 16-bit Mono PCM`, 03:18.45 duration (19 MB). | Source reference file for voice cloning & acoustic calibration. |
| [x] | [`databro-talent-master-calibration.mp3`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3) | **Master Compressed Reference Audio**: High-bitrate 192kbps MP3 reference (4.7 MB). | Fast upload for cloud-based voice cloning APIs (ElevenLabs/Cartesia). |
| [ ] | [`assets/brand-kit/audio/voiceover/talent-samples/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/) | **Talent Audio Storage Directory**: Directory holding raw talent voice samples. | Drop new recordings here anytime. |
| [x] | [`assets/brand-kit/audio/voiceover/generated/`](file:///d:/yvnalv/AI%20Skills/jinkou-chinou/domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/generated/) | **Generated Episodes Audio**: Output directory for rendered episode voiceovers and word-level timestamp JSONs. | Populated during video generation. |

---

## 9. Sampled Exact Brand Color Tokens (From Authentic Assets)

| Color Name | Hex Code | Source Asset Sampled | Purpose in Databro Videos |
| :--- | :--- | :--- | :--- |
| **Matte Charcoal Base** | `#111111` / `#191A1B` | `DatabroBaseCanvas`, Code Cards | Static solid canvas background & IDE code containers |
| **Warm Cream Brand Accent** | `#F0ECE2` / `#E6DBCF` | `(Reels) Computer Vision`, `1.png` | Circular emblem pop, step badges, brand text |
| **Signature Electric Lime** | `#BFFF72` | `databroBrand.colors` | Keyword kinetic typography highlight & success states |
| **Data Teal / Cyan** | `#03DAC6` | `Untitled design (1).png` | Scatter plot points, neural network nodes, vector data |
| **Dark IDE Card Surface** | `#191A1B` | `Screenshot 2026-04-25 135828.png` | Code editor surface (`1px solid #2C2D2E` border) |
| **Dataframe Table Body** | `#1F1F1E` | `Table.png` | Tabular data preview background |
| **Dataframe Table Header** | `#262624` | `Table.png` | Tabular data column header row |
| **Dataframe Row Divider** | `#3B3B39` | `Table.png` | Subtle horizontal lines separating records |
| **High-Contrast Data Off-White** | `#FAF9F5` | `Table.png` | Readable table cell text and numerical data |
| **Warning / Gotcha Red** | `#D92D20` | `databroBrand.colors` | Rectangular callout box for bugs, errors, and pitfalls |

---

## 10. How to Verify & Synchronize After Updates

Whenever you update, add, or replace any file from this checklist:
1. **Validate integrity**:
   ```cmd
   python tools/skills.py validate
   ```
2. **Propagate to all 8 AI agents** (Antigravity, Cursor IDE, Claude Code, Copilot, ChatGPT, Codex, Cline, CAgent):
   ```cmd
   .\sync-skills.bat --no-pause
   ```
