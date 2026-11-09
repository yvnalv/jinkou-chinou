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

## 2. Tone & Pronoun Guardrails (Strict Rule: "Kamu/Anda", Never "Lo")

* **NEVER USE "Lo" / "Lu" / "Gue"**: They are strictly banned across all Databro scripts and captions.
* **Always use "Kamu"** as the default friendly second-person pronoun (*"model ML kamu"*, *"laptop kamu"*, *"biar kamu gak bingung"*). Use **"Anda"** for enterprise/formal contexts, and **"Kalian"** for addressing the community.
* **Always use "Kita"** as the collaborative first-person pronoun (*"Yuk kita coba"*, *"Kita cek di terminal"*).
* **"Bro"** is an energetic brand greeting and closing punctuation (*"Bro, tahu nggak sih..."*, *"Belajar bareng Databro!"*), NOT a replacement for the pronoun "lo".

---

## 3. Closed Captions (CC) Rules for `@databroid`

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

## 4. TikTok Sound Effects (SFX) & CapCut Transitions Mapping

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

## 5. Modifying or Duplicating the Databro Base Content Canvas

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

## 6. Databro Content Archetype & Style Decision Matrix

The skill intelligently selects the motion, stage layout, and graphic assets based on the topic:

| Content Topic / Type | Archetype (`DATABRO_ARCHETYPES`) | Stage Layout & Core Assets | Opening Hook Style | Reference Tone |
| :--- | :--- | :--- | :--- | :--- |
| **Python, Pandas, SQL, Scikit-Learn, Git, Train-Test-Split** | `code-walkthrough` (`60s`) | Dark IDE code cards (`#191A1B`), Table preview (`Table.png`), step badges (`1.png`, `2.png`, `3.png`), terminal output (`output.png`). | **Code Shock / Failed Run** or **Step Roadmap** | Hands-on mentor ("Yuk kita pisahin X dan y...") |
| **Transformer, Backprop, Attention, Vector DB, Loss Functions** | `concept-theory` (`45s`) | `@aibutsimple`-inspired 2D vector animated diagrams, scatter plot trendline (`Untitled design (1).png`), kinetic keywords (`#BFFF72`). | **The Paradox / Counter-Intuitive Question** | Deep technical simplifier ("Kenapa akurasi 99% bisa nipu kamu?") |
| **Data Career Paths, Tech Stack 2026, Salary Insights, AI News** | `opinion-editorial` (`30s-45s`) | Kinetic typography, high-impact statistic badges, quote callouts, Databro landscape logo. | **The Bold Statement / Career Myth** | Provocative & encouraging ("Jangan belajar Python sebelum tahu ini...") |
| **Databro Cloud 2.0, New Features, Free Templates** | `launch-showcase` (`15s-30s`) | 3D UI perspective tilt cards, lime `#BFFF72` ambient glow, metric speedometers. | **Dynamic Metric / Speedometer** | High-energy community builder |

---

## 7. Opening Hook Varieties (Eliminating Visual Monotony)

Never use the exact same opening layout consecutively. Rotate between 4 distinct visual hooks:

1. **Variant 1 — The Paradox Headline (`paradox-headline`)**:
   - Giant bold question scales in at center (`damping: 14, stiffness: 140`).
   - Signature keyword lights up in `#BFFF72` Lime.
   - Ideal for conceptual AI and myth-busting topics.
2. **Variant 2 — The Code Shock / Diagnostic Error (`code-shock`)**:
   - Starts with a dark IDE card showing a high score (e.g. `Accuracy: 99%`) immediately flashing a `#D92D20` red border (`DEPLOY ERROR: OVERFITTING`).
   - Drives instant curiosity for debugging tutorials.
3. **Variant 3 — The Visual Data Spring (`visual-data`)**:
   - Begins directly with a styled dataframe (`Table.png`) or scatter plot (`Untitled design (1).png`) springing into the center stage.
   - Ideal for data wrangling, EDA, and statistical modeling reels.
4. **Variant 4 — The 3-Step Roadmap Card (`step-roadmap`)**:
   - Displays the numbered badges (`1.png`, `2.png`, `3.png`) in a clean horizontal roadmap before zooming into step 1.
   - Ideal for structured tutorials and actionable checklists.

---

## 8. Official Voice Cloning Pipeline & Script Execution

The official Databro Indonesian talent recordings have been merged into master reference files:
- **Master Reference WAV**: `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.wav` (`48 kHz, Mono, 16-bit PCM`, ~3m18s).
- **Master Reference MP3**: `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3` (`192 kbps`).

### How Voiceover is Synthesized:
1. **With ElevenLabs / Cartesia**:
   - Set `ELEVENLABS_API_KEY`. The script uploads the master MP3 to synthesize speech with the authentic talent tone, timbre, and intonation.
2. **Offline Calibrated Fallback**:
   - Runs `edge-tts` with `id-ID-ArdiNeural` calibrated at `rate="+0%"` (135 WPM) and `pitch="+0Hz"`, utilizing a phonetic lexicon for ML terms.

---

## 9. Prompt Examples for `/databro-brand-motion`

- **Tutorial Prompt**:
  > `/databro-brand-motion Buat video TikTok 60 detik tentang "Cara Setup PostgreSQL + pgvector pakai Docker dalam 2 Menit" dengan archetype code-walkthrough: opening code-shock, step terminal Command Prompt dengan kotak merah #D92D20, transisi CapCut, SFX TikTok, dan CC rata tengah di posisi tetap Y=1480px.`
- **Concept Theory Prompt (aibutsimple synthesis)**:
  > `/databro-brand-motion Buat video 45 detik tentang "Kenapa Cosine Similarity Dipakai di Vector Search?" dengan archetype concept-theory: opening paradox-headline, 2D vector diagrams ala aibutsimple, scatter points teal #03DAC6, dan closed captions terkunci di Y=1480px.`
- **Launch / Highlight Prompt**:
  > `/databro-brand-motion Create a 15-second launch reel for "Databro SQL Copilot" showing 3 CLI steps on the Databro Base Content Canvas with TikTok SFX and CapCut smooth transitions.`

