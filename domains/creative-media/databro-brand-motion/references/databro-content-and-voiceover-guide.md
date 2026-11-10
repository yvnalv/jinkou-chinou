# Databro Studio (`@databroid`)  :  Content Generation, Voiceover, CC & Prompting Guide

This guide documents how to plan, script, voice, prompt, and customize Databro Studio (`@databroid`) videos using `/databro-brand-motion`.

---

## 1. Interactive Topic & Content Discovery (Always Ask First)

Whenever `/databro-brand-motion` is invoked without a complete topic and step breakdown, ask the user:
1. **What Content Archetype are we making?** (keys match `DATABRO_ARCHETYPES` in `assets/databro.brand.starter.ts`)
   - **1. Step-by-Step Technical Tutorial** (`code-walkthrough`, e.g. *"Cara Install Lokal LLM Menggunakan Ollama"*: Hook -> Tool Card -> Browser/Installer/Terminal steps with `#D92D20` red callouts -> Live Demo).
   - **2. Data Science / AI Concept Explainer** (`concept-theory`, e.g. *"RAG vs Fine-Tuning dalam 60 Detik"*).
   - **3. Tool / Library Listicle** (`tool-listicle`, e.g. *"3 Python Library Wajib Buat Data Engineer"*).
   - **4. Product / Feature Launch Reel** (`launch-showcase`, e.g. *"Databro Cloud 2.0"*: Hook Emblem -> 3 Benchmark/CLI Highlights -> Emblem CTA).
   - **5. Career / Opinion Editorial** (`opinion-editorial`, e.g. *"Jangan belajar Python sebelum tahu ini..."*).
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
| `#F0ECE2` cream emblem circle + 4-point sparkle pop | `pop-up` | `spring` (`damping: 15, stiffness: 240, mass: 0.8`) |
| Giant `#C1FF72` lime keyword reveal (`Ollama` / `Databro`) | `pop-up` | `spring` (`damping: 15, stiffness: 240, mass: 0.8`) |
| Slide / scene change or card implode-out | `whoosh-transition` | `<TransitionSeries.Transition>` (`10 frames`) |
| Clicking a button or pressing Enter in terminal | `mouse-click` | Cursor scale pulse (`1.0 -> 0.85 -> 1.0`) |
| Terminal / installer progress bar filling (`0% -> 100%`) | `progress-ticks` | Clamped linear/bezier width interpolation |
| `#D92D20` red rectangle locking onto output | `callout-ding` | `spring` scale/opacity lock (`8 frames`) |

---

## 5. Audio-Visual Transition Alignment & Breathing Room Rules (Preventing Voice Skipping)

To prevent voiceover cutoffs or collisions during `<TransitionSeries.Transition>` changes:

1. **Audio Drives Sequence Duration (Never Clamp Speech)**:
   $$\text{SequenceDuration} = \text{HeadDelay} + \text{AudioDuration} + \text{TailDelay}$$
2. **Head Delay (`10-12 frames`, ~0.35s)**:
   - Always enforce a `10-12 frame` breathing room *after* the transition settles before the talent starts speaking.
   - Allows the incoming title/badge to visually settle and lets the `whoosh-transition` SFX decay without muffling speech.
3. **Tail Delay (`12-14 frames`, ~0.40s)**:
   - Always enforce a `12-14 frame` silence buffer *after* speech ends before the next transition begins.
   - Transitions must **never** cut into active speech.
4. **Outro Hold (`24 frames`, ~0.80s)**:
   - Hold on the final screen after speech ends so the CTA and Databro landscape logo resonate.
5. **Captions Bounding**:
   - Closed Captions must strictly live within `[vo_start, vo_end]`, never bleeding into transition overlap regions.

---

## 6. Modifying or Duplicating the Databro Base Content Canvas

Because background color, top-left logo lockup, top-right handle, content stage, and fixed Closed Captions are defined once in [`assets/databro.brand.starter.ts`](../assets/databro.brand.starter.ts) and [`assets/DatabroBaseCanvas.starter.tsx`](../assets/DatabroBaseCanvas.starter.tsx):

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

## 7. Databro Content Archetype & Style Decision Matrix

The skill intelligently selects the motion, stage layout, and graphic assets based on the topic:

| Content Topic / Type | Archetype (`DATABRO_ARCHETYPES`) | Stage Layout & Core Assets | Opening Hook Style | Reference Tone |
| :--- | :--- | :--- | :--- | :--- |
| **Python, Pandas, SQL, Scikit-Learn, Git, Train-Test-Split** | `code-walkthrough` (`60s`) | GitHub Dark code cards (`#24292E`), Table preview (`Table.png`), step badges (`1.png`, `2.png`, `3.png`), terminal output (`output.png`). | **Code Shock / Failed Run** or **Step Roadmap** | Hands-on mentor ("Yuk kita pisahin X dan y...") |
| **Transformer, Backprop, Attention, Vector DB, Loss Functions** | `concept-theory` (`45s`) | `@aibutsimple`-inspired 2D vector animated diagrams, scatter plot trendline (`Untitled design (1).png`), kinetic keywords (`#C1FF72`). | **The Paradox / Counter-Intuitive Question** | Deep technical simplifier ("Kenapa akurasi 99% bisa nipu kamu?") |
| **Python libraries, CLI tools, VS Code extensions, AI tools roundups** | `tool-listicle` (`45s`) | Step badges (`1.png`, `2.png`, `3.png`), one React Icon per item, one-line verdict per item, optional mini code card. | **Step Roadmap** | Practical recommender ("Yang pertama, wajib banget buat kamu...") |
| **Data Career Paths, Tech Stack 2026, Salary Insights, AI News** | `opinion-editorial` (`30s-45s`) | Kinetic typography, high-impact statistic badges, quote callouts, Databro landscape logo. | **The Bold Statement / Career Myth** | Provocative & encouraging ("Jangan belajar Python sebelum tahu ini...") |
| **Databro Cloud 2.0, New Features, Free Templates** | `launch-showcase` (`15s-30s`) | 3D UI perspective tilt cards, flat lime `#C1FF72` metric badges (no glow), metric speedometers. | **Dynamic Metric / Speedometer** | High-energy community builder |

---

## 8. Opening Hook Varieties (Eliminating Visual Monotony)

Never use the exact same opening layout consecutively. Rotate between 4 distinct visual hooks:

1. **Variant 1  :  The Paradox Headline (`paradox-headline`)**:
   - Giant bold question scales in at center (`damping: 14, stiffness: 140`).
   - Signature keyword lights up in `#C1FF72` Lime.
   - Ideal for conceptual AI and myth-busting topics.
2. **Variant 2  :  The Code Shock / Diagnostic Error (`code-shock`)**:
   - Starts with a dark IDE card showing a high score (e.g. `Accuracy: 99%`) immediately flashing a `#D92D20` red border (`DEPLOY ERROR: OVERFITTING`).
   - Drives instant curiosity for debugging tutorials.
3. **Variant 3  :  The Visual Data Spring (`visual-data`)**:
   - Begins directly with a styled dataframe (`Table.png`) or scatter plot (`Untitled design (1).png`) springing into the content stage.
   - Ideal for data wrangling, EDA, and statistical modeling reels.
4. **Variant 4  :  The 3-Step Roadmap Card (`step-roadmap`)**:
   - Displays the numbered badges (`1.png`, `2.png`, `3.png`) in a clean horizontal roadmap before zooming into step 1.
   - Ideal for structured tutorials and actionable checklists.

---

## 9. Official Voice Cloning Pipeline & Script Execution

The official Databro Indonesian talent recordings have been merged into master reference files:
- **Master Reference WAV**: `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.wav` (`48 kHz, Mono, 16-bit PCM`, ~3m18s).
- **Master Reference MP3**: `assets/brand-kit/audio/voiceover/talent-samples/databro-talent-master-calibration.mp3` (`192 kbps`).

### How Voiceover is Synthesized:
Run `assets/generate_databro_cloned_vo.starter.py` from this skill folder (it only reads and writes the paths you pass) and generate **one clip per scene**:

```bash
python <skill-dir>/assets/generate_databro_cloned_vo.starter.py --text-file vo/scene-01.txt --out public/vo/scene-01.mp3 --fps 30
```

1. **Cloned talent voice (ElevenLabs)**: clone the talent once from the master MP3 (ElevenLabs Voices -> Instant Voice Clone), then set `ELEVENLABS_API_KEY` and `DATABRO_VOICE_ID`. With `--engine auto` (default) the cloned voice is used when both are set. It never falls back to a stock voice. It returns audio only, without word timings.
2. **Offline calibrated fallback (Edge-TTS)**: `id-ID-ArdiNeural`, `pitch="-4Hz"`, `rate="-2%"`, with a phonetic lexicon for ML terms. Writes `scene-01.json` with `speechEndFrame`, word timings, and ready caption chunks (`{text, startFrame, endFrame}` in the original spelling, 2-4 words, ALL CAPS, relative to the clip start).
3. **Wire it up**: scene duration = head delay (10-12) + `speechEndFrame` + tail delay (12-14). Offset each clip's captions by the scene's start frame plus the head delay before passing them to `<DatabroBaseCanvas captions={...} />`.

---

## 10. Prompt Examples for `/databro-brand-motion`

- **Tutorial Prompt**:
  > `/databro-brand-motion Buat video TikTok 60 detik tentang "Cara Setup PostgreSQL + pgvector pakai Docker dalam 2 Menit" dengan archetype code-walkthrough: opening code-shock, step terminal Command Prompt dengan kotak merah #D92D20, transisi CapCut, SFX TikTok, dan CC rata tengah di posisi tetap Y=1480px.`
- **Concept Theory Prompt (aibutsimple synthesis)**:
  > `/databro-brand-motion Buat video 45 detik tentang "Kenapa Cosine Similarity Dipakai di Vector Search?" dengan archetype concept-theory: opening paradox-headline, 2D vector diagrams ala aibutsimple, scatter points teal #03DAC6, dan closed captions terkunci di Y=1480px.`
- **Launch / Highlight Prompt**:
  > `/databro-brand-motion Create a 15-second launch reel for "Databro SQL Copilot" showing 3 CLI steps on the Databro Base Content Canvas with TikTok SFX and CapCut smooth transitions.`

