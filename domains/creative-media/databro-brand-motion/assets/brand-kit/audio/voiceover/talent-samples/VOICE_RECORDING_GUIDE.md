# Databro Talent Voice Recording & AI Voiceover Cloning Guide

> **Storage Directory**: Drop all raw talent `.wav` recordings directly into this folder:  
> [`domains/creative-media/databro-brand-motion/assets/brand-kit/audio/voiceover/talent-samples/`](./)

---

## 1. Recording Format & Acoustic Checklist

| Parameter | Required Specification | Recommended Setting |
| :--- | :--- | :--- |
| **File Format** | Uncompressed `.wav` (`PCM`) | `.wav` (DO NOT use compressed `.mp3` or `.m4a` for reference samples) |
| **Sample Rate** | **`48,000 Hz`** (or `44,100 Hz`) | `48 kHz` |
| **Bit Depth** | **`24-bit`** (or `16-bit`) | `24-bit PCM` |
| **Channels** | **Mono** (`1 channel`) | Mono (if recorded in stereo, export as mono) |
| **Peak Level** | **`-6 dBFS` to `-3 dBFS`** | Leave `3-6 dB` of headroom, never clip (`0 dBFS`) |
| **Noise Floor** | Below **`-55 dBFS`** | Quiet bedroom/studio, AC/fan turned off, curtains closed |
| **Mic Distance** | **`15-20 cm`** from mouth | Slightly off-axis (45°) with a pop filter to prevent plosives (*P, B, T*) |
| **Audio Processing** | **100% DRY VOCAL** | **No BGM, no reverb, no heavy noise reduction, no compressor** |

---

## 2. Tone & Persona Guidelines (`@databroid`)

* **Pronoun Guardrail**: **ALWAYS use `"Kamu"` (or `"Anda"` for enterprise) and `"Kita"` / `"Kalian"`. NEVER use `"Lo"` / `"Lu"` / `"Gue"`.**
* **Energy Level**: Friendly, energetic, knowledgeable senior tech mentor talking to a smart friend at a coffee shop. Not stiff like a Wikipedia article, but not chaotic or screaming.
* **Speed**: **Normal conversational pace (~130-145 words per minute)**. Clear articulation, not rushed.
* **English Tech Terms**: Pronounce technical words with standard global developer phonetics (`Python`, `Scikit-Learn`, `API`, `RAG`, `Pipeline`, `Vector Database`, `Docker`, `Uptime SLA`, `Overfitting`, `JSON`), smoothly integrated into natural Indonesian.

---

## 3. Calibration Recording Script (Read in 1 Take or 5 Separate Files)

Read each block below with natural conversational energy. Pause for **1.5 seconds** between blocks:

### Block 1  :  Energetic Hook & Opening (`~20s`  :  save as `databro-talent-ref-hook.wav`)
> *"Bro, tahu nggak sih kalau kamu bisa install dan jalanin model AI canggih langsung di laptop kamu sendiri tanpa ribet? Nah, di video ini kita bakal setup semuanya dari nol dalam waktu kurang dari dua menit. Yuk, kita mulai!"*

### Block 2  :  Tutorial & Instructional Walkthrough (`~30s`  :  save as `databro-talent-ref-tutorial.wav`)
> *"Langkah pertama, buka browser kamu lalu cari halaman download resmi di website-nya. Kemudian klik tombol Download for Windows, lalu tunggu prosesnya selesai. Setelah itu, buka file dot exe yang sudah kamu download, lalu klik Install dan tunggu sampai progress barnya penuh."*

### Block 3  :  Technical Python Code & Data Science (`~35s`  :  save as `databro-talent-ref-code.wav`)
> *"Sekarang kita masuk ke Python. Pertama, pisahkan fitur X dan target y menggunakan Pandas. Kemudian panggil fungsi train test split dari Scikit-Learn. Set test size nol koma dua, dan wajib pasang random state empat puluh dua biar hasil split data kamu selalu konsisten dan reproducible."*

### Block 4  :  Metrics, Numbers & Enterprise SLA (`~30s`  :  save as `databro-talent-ref-metrics.wav`)
> *"Kalau kita cek performanya di terminal, kecepatan query database naik sepuluh kali lipat dari empat koma dua detik jadi nol koma empat dua detik. Ditambah lagi, ada jaminan sembilan puluh sembilan koma sembilan sembilan persen Uptime SLA untuk PostgreSQL, BigQuery, dan model Llama tiga."*

### Block 5  :  Outro, Community Advice & CTA (`~20s`  :  save as `databro-talent-ref-outro.wav`)
> *"Dengan tiga langkah tadi, model machine learning kamu dijamin jauh lebih valid di production dan bebas data leakage. Save video ini biar kamu gak lupa, dan follow Databro buat belajar Data Science bareng, bro!"*

---

## 4. Recommended Target File Names to Save Here

Once recorded, save your files directly into this directory:

1. **`databro-talent-ref-30s.wav`** *(30-45 seconds: combined Block 1 + Block 3)*  
   👉 Used for fast zero-shot local voice cloning (`F5-TTS`, `CosyVoice 2`, `Fish Speech`).
2. **`databro-talent-full-calibration.wav`** *(90-150 seconds: all 5 blocks)*  
   👉 Used for ElevenLabs Instant Voice Cloning (IVC) or Cartesia neural model training.

---

## 5. Official Merged Master Calibration Audio

The human talent takes (`Gang Haji Nasim 12.m4a` through `Gang Haji Nasim 18.m4a`) have been processed and merged into the official Databro reference audio:

- **Master PCM WAV**: [`databro-talent-master-calibration.wav`](databro-talent-master-calibration.wav)  
  *Specs:* `48,000 Hz, 16-bit Mono PCM, 768 kb/s, 03:18.45 duration (19,051,726 bytes)*
- **Master High-Bitrate MP3**: [`databro-talent-master-calibration.mp3`](databro-talent-master-calibration.mp3)  
  *Specs:* `192 kbps, 48,000 Hz, Mono, 03:18.45 duration (4,764,140 bytes)*

---

## 6. How the Databro Voice Cloning Pipeline Operates

1. **Online Instant Voice Cloning (ElevenLabs / Cartesia)**:
   - Provide `ELEVENLABS_API_KEY` in your environment.
   - Clone the talent once from `databro-talent-master-calibration.mp3` (ElevenLabs Voices -> Instant Voice Clone) and set `DATABRO_VOICE_ID` to the new voice ID.
   - Run the skill's `assets/generate_databro_cloned_vo.starter.py` (Stability: 0.60, Similarity: 0.82). It never falls back to a stock voice.
2. **Offline Calibrated Fallback (Edge-TTS `id-ID-ArdiNeural`)**:
   - If no external API key is set, the pipeline automatically uses Microsoft Edge-TTS with phonetic calibration (`rate="-2%"`, `pitch="-4Hz"`, ~135 WPM), mapping English ML jargon to Indonesian tech developer phonetics.
3. **Word-Level Captions Synchronization**:
   - Closed Captions are locked at `Y = 1480px` in 2-4 word uppercase chunks synchronized with the synthesized speech audio boundaries.
