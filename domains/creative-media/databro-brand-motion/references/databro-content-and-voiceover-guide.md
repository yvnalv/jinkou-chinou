# Databro Studio (`@databroid`) — Content Generation, Voiceover, CC & Prompting Guide

This guide documents how to plan, script, voice, prompt, and customize Databro Studio (`@databroid`) videos using `/databro-brand-motion`.

---

## 1. Interactive Topic & Content Discovery (Always Ask First)

Whenever `/databro-brand-motion` is invoked without a complete topic and step breakdown, ask the user:
1. **What Content Archetype are we making?**
   - **A. Step-by-Step Technical Tutorial** (e.g., *"Cara Install Lokal LLM Menggunakan Ollama"* — Hook Emblem -> Tool Card -> Browser/Installer/Terminal steps with `#D92D20` red callouts -> Live Demo).
   - **B. Product / Feature Launch Reel** (e.g., *"Databro Cloud 2.0"* — Hook Emblem -> 3 Benchmark/CLI Highlights -> Emblem CTA).
   - **C. Data Science / AI Concept Explainer** (e.g., *"RAG vs Fine-Tuning dalam 60 Detik"*).
   - **D. Tool / Library Listicle** (e.g., *"3 Python Library Wajib Buat Data Engineer"*).
2. **What is the Topic & Target Duration?** (`15s`, `30s`, `60s`, or `90s`).
3. **Which Aspect Ratio Preset (`DATABRO_CANVAS_PRESETS`)?** (`'9:16'` TikTok/Reels default, `'4:5'` IG Feed, `'1:1'` Square, or `'16:9'` YouTube).
4. **Voiceover Mode**:
   - **A. Synced Closed Captions + TikTok SFX + BGM** (ready for voiceover or standalone reel).
   - **B. Cloned Databro Talent Voiceover** generated from `assets/brand-kit/audio/voiceover/talent-samples/`.

---

## 2. Closed Captions (CC) Rules for `@databroid`

1. **Exact Fixed Position (`Y = 1480px` on `1080×1920`)**:
   - Handled automatically by [`DatabroCaptions`](../assets/DatabroCaptions.starter.tsx) inside [`DatabroBaseCanvas`](../assets/DatabroBaseCanvas.starter.tsx).
   - Never place `<DatabroCaptions />` inside individual scenes; keep it on the root `<DatabroBaseCanvas />` so it never moves during slide transitions.
2. **2-to-4 Words Per Phrase in ALL-CAPS**:
   - Break Indonesian or English narration into natural 2-to-4 word uppercase chunks:
     - Good: `"BRO TAHU NGGAK"`, `"SIH KALAU KALIAN"`, `"BISA INSTALL MODEL"`, `"DI LAPTOP KAMU"`
     - Bad: `"Bro tahu nggak sih kalau kalian bisa install model LLM langsung di laptop kamu sendiri?"` (too long, wraps to 3+ lines).
3. **Zero Vertical Bounce**:
   - Phrases switch via a `3-frame` opacity cross-fade at `Y = 1480px` with zero `translateY` movement.

---

## 3. TikTok Sound Effects (SFX) & CapCut Transitions Mapping

Every Databro composition passes a `soundCues: DatabroSoundCue[]` array to `<DatabroBaseCanvas soundCues={soundCues}>`:

| Visual Event in `@databroid` Video | SFX Key (`assets/brand-kit/audio/sfx/`) | CapCut Transition / Spring |
| :--- | :--- | :--- |
| Hook typewriter characters (`█` cursor) | `keyboard-typing` (`durationInFrames: 24`) | Character slice interpolation |
| `#F2EBE1` cream emblem circle + 4-point sparkle pop | `pop-up` | `spring` (`damping: 15, stiffness: 240, mass: 0.8`) |
| Giant `#BFFF72` lime keyword reveal (`Ollama` / `Databro`) | `pop-up` | `spring` (`damping: 15, stiffness: 240, mass: 0.8`) |
| Slide / scene change or card implode-out | `whoosh-transition` | `<TransitionSeries.Transition>` (`10 frames`) |
| Clicking a button or pressing Enter in terminal | `mouse-click` | Cursor scale pulse (`1.0 -> 0.85 -> 1.0`) |
| Terminal / installer progress bar filling (`0% -> 100%`) | `progress-ticks` | Clamped linear/bezier width interpolation |
| `#D92D20` red rectangle locking onto output | `callout-ding` | `spring` scale/opacity lock (`8 frames`) |

---

## 4. Modifying or Duplicating the Databro Base Content Canvas

Because background color, top-left logo lockup, centered stage, and fixed Closed Captions are defined once in [`assets/databro.brand.starter.ts`](../assets/databro.brand.starter.ts) and [`assets/DatabroBaseCanvas.starter.tsx`](../assets/DatabroBaseCanvas.starter.tsx):

```tsx
import { DatabroBaseCanvas } from './DatabroBaseCanvas';
import { customizeDatabroCanvas } from './databro.brand';

// 1. Default 9:16 TikTok / Reels Canvas (Logo at 100,108 | CC locked at Y=1480)
<DatabroBaseCanvas aspectRatio="9:16" captions={captions} soundCues={soundCues}>
  {/* <TransitionSeries> scenes here */}
</DatabroBaseCanvas>

// 2. Duplicate onto 4:5 Instagram Portrait Feed or customize coordinates in 1 line:
const customCanvas = customizeDatabroCanvas('9:16', {
  closedCaption: { y: 1480, fontSize: 40 },
});
```

---

## 5. Prompt Examples for `/databro-brand-motion`

- **Tutorial Prompt**:
  > `/databro-brand-motion Buat video TikTok 60 detik tentang "Cara Setup PostgreSQL + pgvector pakai Docker dalam 2 Menit" dengan gaya @databroid: hook typewriter + emblem circle, lanjut step terminal Command Prompt dengan kotak merah #D92D20, transisi CapCut, SFX TikTok, dan CC rata tengah di posisi tetap Y=1480px.`
- **Launch / Highlight Prompt**:
  > `/databro-brand-motion Create a 15-second launch reel for "Databro SQL Copilot" showing 3 CLI steps on the Databro Base Content Canvas with TikTok SFX and CapCut smooth transitions.`

