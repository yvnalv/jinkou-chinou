# Voiceover Generation, Closed Captions (CC), Sound Effects (SFX) & CapCut Transitions Guide

This guide documents how to produce synced voiceovers using a human talent's recorded voice, position Closed Captions (CC) at a fixed coordinate, trigger TikTok/CapCut sound effects, and choreograph smooth transitions in Remotion.

---

## 1. Closed Captions (CC) Guidelines

### Fixed-Position Rule
Closed Captions MUST be rendered at the root level inside [`BaseContentCanvas`](../assets/BaseContentCanvas.starter.tsx) (outside `<TransitionSeries>`) and locked at a **fixed Y coordinate** for the entire video:
- **`9:16` Vertical (`1080×1920`)**: **`Y = 1480px`** (`440px` above the bottom edge, `X = 540px` horizontally centered, `left: 110px, right: 110px`).
  - Why `Y = 1480px`? It sits cleanly below center-stage emblem titles (`Y = 1230–1380px`) and terminal windows (`Y = 550–1320px`) while staying above the TikTok/Instagram Reels username and caption overlay (`Y = 1540–1920px`).
- **`4:5` Portrait (`1080×1350`)**: **`Y = 1140px`** (`left: 96px, right: 96px`).
- **`1:1` Square (`1080×1080`)**: **`Y = 910px`** (`left: 84px, right: 84px`).
- **`16:9` Landscape (`1920×1080`)**: **`Y = 920px`** (`left: 240px, right: 240px`).

### Chunking & Transition Rules
1. **2-to-4 Words Per Chunk**: Break the voiceover script into short, punchy 2-to-4 word phrases (`"BRO TAHU NGGAK"`, `"SIH KALAU KALIAN"`, `"MEET DATABRO CLOUD"`). Never stack more than 1–2 short lines.
2. **Zero Vertical Bounce**: Captions must NEVER slide up/down when switching phrases or when scenes transition. Use a `3-frame` opacity cross-fade (`0.25 -> 1.0 -> 0.25`) locked at the exact `Y` coordinate.
3. **Typography**:
   - **TikTok / CapCut Cardless Mode (`cardlessCaptions: true`)**: `38px` (`9:16`), Weight `800` (ExtraBold), ALL-CAPS (`textTransform: 'uppercase'`), `#FFFFFF` solid white, no pill box.
   - **Boxed Mode (`cardlessCaptions: false`)**: Solid flat dark container (`padding: 12px 24px`, `borderRadius: 12px`), no backdrop blur.

---

## 2. TikTok / CapCut Sound Effects (SFX) System

Every brand skill stores its sound effects inside `assets/brand-kit/audio/sfx/`.

### Standard 6-SFX Pack + Ambient BGM
You can generate a clean, royalty-free `.wav` pack for any brand using [`scripts/generate_default_sfx.py`](../scripts/generate_default_sfx.py):

```bash
python domains/creative-media/the-motion-designer/scripts/generate_default_sfx.py \
  --out domains/creative-media/<brand>-brand-motion/assets/brand-kit/audio
```

| SFX Key | File Path (`assets/brand-kit/audio/...`) | When to Trigger (`SoundCueItem`) | Recommended Volume |
| :--- | :--- | :--- | :--- |
| **`keyboard-typing`** | `sfx/keyboard-typing.wav` | Synced to typewriter hook text or terminal CLI command typing (`durationInFrames` matched to typing duration) | `0.50 – 0.60` |
| **`pop-up`** | `sfx/pop-up.wav` | Exact frame when an emblem circle, badge, or UI window springs onto the canvas | `0.55 – 0.65` |
| **`whoosh-transition`** | `sfx/whoosh-transition.wav` | Exact start frame of a `<TransitionSeries>` slide/whip transition or camera zoom-in | `0.45 – 0.55` |
| **`mouse-click`** | `sfx/mouse-click.wav` | Exact frame when a cursor clicks a button or submits a terminal command | `0.60` |
| **`progress-ticks`** | `sfx/progress-ticks.wav` | Start frame of a terminal or installer progress bar filling (`0% -> 100%`) | `0.40 – 0.50` |
| **`callout-ding`** | `sfx/callout-ding.wav` | Exact frame when a red callout rectangle (`#D92D20`) or highlight locks around key output | `0.50` |
| **`bgm-ambient`** | `bgm/bgm-ambient.wav` | Continuous background synth pad loop (`bgmVolume: 0.12` to `0.15`, ~`-22 dBFS` under voiceover) | `0.12 – 0.15` |

### Dropping Custom TikTok / CapCut SFX
To use your own `.wav` or `.mp3` files from CapCut or TikTok, drop them into `assets/brand-kit/audio/sfx/` (either replacing the standard names above or referencing `'brand-kit/audio/sfx/my-custom-sound.mp3'` in `soundCues`).

---

## 3. Smooth CapCut / TikTok Transitions Choreography

Because `<BaseContentCanvas>` keeps the background, top-left brand logo, and bottom closed captions stationary at the root level, `<TransitionSeries>` inside the center stage produces seamless CapCut-style transitions:

1. **Pop-Scale Spring Entry (`damping: 16, stiffness: 240, mass: 0.8`)**:
   - Elements scale from `0.0 -> 1.0` (with subtle `4%` CapCut overshoot) synced with `sfx: 'pop-up'`.
2. **Smooth Camera Zoom & Pan (`CameraFocusRig`)**:
   - When showing a browser or terminal window, start at `scale(1) translate(0px, 0px)` for the first `15 frames`, then interpolate using a fast spring (`damping: 20, stiffness: 170`) to `scale(1.25) translate(targetX, targetY)` to focus on the active command or red callout box, paired with `sfx: 'whoosh-transition'`.
3. **Whip-Slide / Push Transition (`@remotion/transitions`)**:
   - Use `TransitionSeries.Transition` with `slide({ direction: 'from-right' })` or `slide({ direction: 'from-bottom' })` and `springTiming({ config: { damping: 18, stiffness: 220 }, durationInFrames: 10 })` paired with `sfx: 'whoosh-transition'`.
4. **Implode / Crumple Exit (`scale: 1 -> 0` over final `8 frames`)**:
   - Before the next step begins, scale the active card down to `0` at center (`interpolate(frame, [end - 8, end], [1, 0])`) so the stage clears cleanly.

---

## 4. Generating Voiceover from Recorded Talent Audio

### Step 1: Record the Talent's Reference Audio (`assets/brand-kit/audio/voiceover/talent-samples/`)
- **File Format**: Uncompressed `.wav`, `48 kHz` (or `44.1 kHz`), `24-bit` (or `16-bit`), **Mono**.
- **Acoustic Environment**: Quiet carpeted room, microphone `15–20 cm` from mouth with pop filter, peak level between **`-6 dBFS` and `-3 dBFS`**.
- **No Processing**: Do **not** add background music, reverb, echo, or aggressive noise-gate clipping.
- **Duration**:
  - **`20–30 seconds` (`talent-ref-30s.wav`)**: Ideal for zero-shot local models (**F5-TTS**, **CosyVoice 2**, **Fish Speech 1.5**).
  - **`90–180 seconds` (`talent-full-calibration.wav`)**: Ideal for **ElevenLabs Instant Voice Cloning (IVC)** to capture full pitch range and bilingual code-switching.

### Step 2: Calibration Script for the Talent to Read

#### Option A — Indonesian + English Tech Code-Switching (`@databroid` Style)
> **1. Hook & Excitement (Upbeat, conversational "Bro" energy):**
> *"Bro, tahu nggak sih kalau sekarang kalian bisa jalanin model AI dan query jutaan baris data langsung di cloud dalam hitungan detik? Nah, di video kali ini kita bakal bahas tuntas cara setup-nya dalam waktu kurang dari dua menit. Yuk, kita mulai!"*
>
> **2. Technical Walkthrough (Clear step-by-step pacing, natural English tech pronunciation):**
> *"Pertama, buka browser kalian lalu masuk ke dashboard resmi. Di sini kita bisa langsung konekin database PostgreSQL, MySQL, atau BigQuery tanpa perlu bikin file konfigurasi YAML manual. Coba buka Command Prompt, lalu ketik perintahnya dan tekan Enter."*
>
> **3. Numbers, Metrics & Acronyms (Crisp articulation of numbers & acronyms):**
> *"Lihat hasilnya: kecepatan query naik sepuluh kali lipat dari empat koma dua detik jadi nol koma empat dua detik, dengan jaminan sembilan puluh sembilan koma sembilan sembilan persen Uptime SLA. Semua pipeline ETL, API endpoint, dan model LLM kayak Llama tiga, Claude, atau Gemini langsung siap dipakai."*
>
> **4. Call to Action (Warm, energetic sign-off):**
> *"Kalau semuanya sudah beres, sistem kalian sekarang udah jalan otomatis secara real-time. Langsung aja cobain sekarang juga, semoga bermanfaat bro!"*

#### Option B — English Technical Creator Style
> **1. Hook & Excitement:**
> *"Wait—did you know you can run local AI models and query a billion rows of data in under half a second right from your terminal? In this video, I'll show you how to set the whole thing up in less than two minutes. Let's dive in."*
>
> **2. Technical Walkthrough:**
> *"First, open your browser and grab the official CLI installer. Once it's installed, open Command Prompt or your terminal, connect your PostgreSQL or Lakehouse cluster with a single command, and hit Enter—zero YAML configuration required."*
>
> **3. Numbers, Metrics & Acronyms:**
> *"Check out that benchmark: query latency drops tenfold from 4.20 seconds down to 0.42 seconds, backed by a 99.99% multi-region Uptime SLA. Your ETL pipelines, vector indexes, and LLM endpoints for Llama 3, Claude, and Gemini are live."*
>
> **4. Call to Action:**
> *"And that's it—your real-time data pipeline is ready for production. Try it free today, and follow for more engineering tutorials!"*

### Step 3: Voice Synthesis + Automatic Word/Phrase Timestamp Alignment
1. **Generate the Voiceover `.wav`**:
   - **ElevenLabs API**: Call `POST /v1/text-to-speech/{voice_id}/with-timestamps` (`model_id: "eleven_multilingual_v2"`), saving the audio to `assets/brand-kit/audio/voiceover/generated/voiceover.wav` and character/word timestamps to `timestamps.json`.
   - **Local Zero-Shot (F5-TTS / CosyVoice 2 / Fish Speech)**: Pass `talent-samples/talent-ref-30s.wav` + script text to output `generated/voiceover.wav`, then run `faster-whisper` (`word_timestamps=True`) to produce `generated/timestamps.json`.
2. **Convert Timestamps to Remotion `CaptionPhraseCue[]`**:
   - Group every `2–4 words` from `timestamps.json` and convert seconds to frames (`Math.round(seconds * fps)`), passing the resulting array directly into `<BaseContentCanvas captions={captions} voiceoverSrc="brand-kit/audio/voiceover/generated/voiceover.wav" />`.

