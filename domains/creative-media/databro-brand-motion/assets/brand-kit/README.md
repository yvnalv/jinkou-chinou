# Databro Studio (`@databroid`) — Brand Kit & Asset Storage Directory

This folder (`assets/brand-kit/`) is the **single source of truth** for all Databro Studio visual, typographic, graphic, reference, and audio assets. Every brand motion skill in `jinkou-chinou` uses this exact folder structure so you can drop in or update files without touching scene code.

---

## Where to Store Each Asset Type

| Folder Path | What to Store Here | Supported Formats | Pre-Populated Default Files |
| :--- | :--- | :--- | :--- |
| **`persona/`** | Brand persona, target audience profile, Indonesian + English code-switching rules, hooks, and scriptwriting tone. | `.md`, `.pdf`, `.json` | [`persona/databro-persona.md`](persona/databro-persona.md) |
| **`guidelines/`** | Color hex tokens, typography stack, Base Content Canvas geometry presets (`9:16`, `4:5`, `1:1`, `16:9`), and official Brand Book PDFs (`guidelines/pdfs/`). | `.json`, `.ts`, `.pdf`, `.md` | [`guidelines/databro.tokens.json`](guidelines/databro.tokens.json) |
| **`fonts/`** | Custom brand font files loaded via `staticFile()` or `@remotion/google-fonts`. | `.ttf`, `.otf`, `.woff2` | [`fonts/README.md`](fonts/README.md) (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`) |
| **`logos/`** | Official brand avatars, primary/secondary wordmarks, and icon marks. | `.svg`, `.png`, `.jpg`, `.webp` | [`logos/databro-avatar.jpg`](logos/databro-avatar.jpg) |
| **`graphics/emblems/`** | Hero line-art icons and badges placed inside the `#F0ECE2` warm cream emblem circle. | `.svg`, `.png` | [`graphics/emblems/README.md`](graphics/emblems/README.md) |
| **`graphics/ui-frames/`** | Reusable terminal, browser, or installer window templates and chrome assets. | `.svg`, `.png`, `.tsx` | [`graphics/ui-frames/README.md`](graphics/ui-frames/README.md) |
| **`graphics/overlays/`** | Sparkle accents, custom cursors, and `#D92D20` red callout frames. | `.svg`, `.png` | [`graphics/overlays/README.md`](graphics/overlays/README.md) |
| **`references/videos/`** | Real reference TikTok / Reels `.mp4` videos for motion/timing benchmarking. | `.mp4`, `.mov`, `.webm` | [`references/videos/README.md`](references/videos/README.md) |
| **`references/designs/`** | Figma exports, static slide mockups, and keyframe screenshots. | `.png`, `.jpg`, `.svg`, `.pdf` | [`references/designs/README.md`](references/designs/README.md) |
| **`audio/sfx/`** | TikTok / CapCut sound effects triggered frame-accurately in Remotion. | `.wav`, `.mp3` | `keyboard-typing.wav`, `pop-up.wav`, `whoosh-transition.wav`, `mouse-click.wav`, `progress-ticks.wav`, `callout-ding.wav` |
| **`audio/bgm/`** | Low-volume (`-22 dBFS`) background music loops. | `.wav`, `.mp3` | `bgm-ambient.wav` |
| **`audio/voiceover/talent-samples/`** | Raw dry recordings of the Databro voice talent used for AI voice cloning. | `.wav` (`48kHz 24-bit Mono`) | [`VOICE_RECORDING_GUIDE.md`](audio/voiceover/talent-samples/VOICE_RECORDING_GUIDE.md) |
| **`audio/voiceover/generated/`** | Synthesized per-video voiceover tracks and word-level timestamp JSON files. | `.wav`, `.mp3`, `.json` | [`audio/voiceover/generated/README.md`](audio/voiceover/generated/README.md) |

---

## How Assets Sync into a Remotion Project

When building or updating a Remotion project with `/databro-brand-motion`, copy `assets/brand-kit/` into the Remotion project's `public/brand-kit/` directory:

```powershell
Copy-Item -Recurse -Force "domains/creative-media/databro-brand-motion/assets/brand-kit" "<remotion-project>/public/brand-kit"
```

All components inside [`DatabroBaseCanvas.starter.tsx`](../DatabroBaseCanvas.starter.tsx) automatically resolve logos, SFX, BGM, and voiceovers from `staticFile('brand-kit/...')`.
