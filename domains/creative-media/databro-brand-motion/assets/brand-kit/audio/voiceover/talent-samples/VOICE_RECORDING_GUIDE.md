# Databro Talent Voice Recording & AI Voiceover Cloning Guide

Place raw dry voice recordings of the Databro talent inside this directory (`assets/brand-kit/audio/voiceover/talent-samples/`).

---

## 1. Recording Format & Acoustic Checklist

| Parameter | Required Specification |
| :--- | :--- |
| **File Format** | Uncompressed `.wav` (`PCM`) |
| **Sample Rate & Bit Depth** | `48,000 Hz` (or `44,100 Hz`), `24-bit` (or `16-bit`) |
| **Channels** | **Mono** (`1 channel`) |
| **Peak Level** | **`-6 dBFS` to `-3 dBFS`** (never clipping `0 dBFS`) |
| **Noise Floor** | Below **`-55 dBFS`** (quiet bedroom/studio, AC/fan turned off, `15–20 cm` from mic with pop filter) |
| **Audio Effects** | **None** — raw dry vocal only (no background music, no room reverb, no heavy noise gate) |
| **Recommended File Names** | `databro-talent-ref-30s.wav` (for local zero-shot cloning) and `databro-talent-full-calibration.wav` (`90–180s` for ElevenLabs IVC) |

---

## 2. Exact Calibration Script to Record (`@databroid` Tone)

Have the Databro talent read the 4 blocks below naturally in one take (pausing `1.5 seconds` between blocks). This captures `@databroid`'s signature friendly *"Bro"* energy, instructional clarity, and Indonesian + English technical code-switching:

### Block 1 — Hook & Upbeat Opening (`~20 seconds` — Save as `databro-talent-ref-30s.wav`)
> *"Bro, tahu nggak sih kalau kalian bisa install dan jalanin model LLM langsung di laptop atau cloud kalian sendiri tanpa ribet? Nah, video ini bakal bantu kamu setup semuanya dari nol dalam waktu kurang dari dua menit. Yuk, kita mulai!"*

### Block 2 — Step-by-Step Browser & Installer Walkthrough (`~30 seconds`)
> *"Pertama, buka browser kalian lalu cari halaman download resmi di website-nya. Kemudian klik tombol Download for Windows, lalu tunggu sampai proses download selesai—waktunya tergantung kecepatan internet kalian. Setelah selesai, buka file dot exe yang sudah didownload, lalu klik Install."*

### Block 3 — Terminal CLI, Numbers & Technical Acronyms (`~35 seconds`)
> *"Kalau sudah, kita cek apakah sudah terinstall dengan benar. Buka Command Prompt atau terminal kalian, lalu ketik `ollama --version` atau `databro query --vectorized`. Lihat hasilnya: kecepatan query naik sepuluh kali lipat dari empat koma dua detik jadi nol koma empat dua detik, dengan jaminan sembilan puluh sembilan koma sembilan sembilan persen Uptime SLA di PostgreSQL, BigQuery, dan model Llama tiga delapan B."*

### Block 4 — Real-Time Demo & Sign-Off CTA (`~25 seconds`)
> *"Kalau semuanya sudah beres, sekarang model AI dan pipeline data kamu udah siap dipakai kayak ChatGPT, Claude, atau Gemini. Ini bisa jadi solusi banget buat workflow data science kamu. Langsung aja cobain sekarang juga, semoga bermanfaat bro!"*

---

## 3. How Voiceover + Closed Captions Are Generated from Your Recording

1. **Voice Synthesis**:
   - **ElevenLabs (`eleven_multilingual_v2`)**: Upload `databro-talent-full-calibration.wav` to create an Instant Voice Clone, then call `/v1/text-to-speech/{voice_id}/with-timestamps` to generate both `../generated/voiceover.wav` and `../generated/timestamps.json`.
   - **Local Zero-Shot (`F5-TTS` / `CosyVoice 2` / `Fish Speech 1.5`)**: Use `databro-talent-ref-30s.wav` as the reference audio prompt to synthesize `../generated/voiceover.wav`, then run `faster-whisper` (`word_timestamps=True`) to produce `../generated/timestamps.json`.
2. **Automatic Closed Caption Sync (`Y = 1480px`)**:
   - Word timestamps are grouped into `2–4 word` uppercase phrases (`CaptionPhraseCue[]`) and passed into `<DatabroBaseCanvas captions={captions} voiceoverSrc="brand-kit/audio/voiceover/generated/voiceover.wav" />`.

