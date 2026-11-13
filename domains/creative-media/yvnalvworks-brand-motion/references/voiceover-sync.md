# Voiceover Sync (recorded voice to reel)

How a reel goes from estimated timings to Yovan's real voice. First used on "The AI Engineering Workflow" (2026-11-12): five takes, 1.2x, median caption error about 0.1 s after refinement. The tools ship in `assets/reel-starter/scripts/`.

## 1. Recording convention

- One take per scene, in scene order, recorded from the teleprompter guide (iPhone, 48 kHz is fine).
- Files land in the reel's OneDrive folder under `voiceover/`, usually `Recording (N).m4a`. Gaps in numbering are normal (discarded takes); very short, near-silent files are false starts.
- Never edit or delete the originals. All outputs are new files.

## 2. Match takes to scenes

1. Convert each take to 16 kHz mono WAV inside the reel project (`vo/`), using the bundled ffmpeg (`node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe`; there is no system ffmpeg on PATH).
2. `npm run transcribe -- vo/<take>-16k.wav ...` (whisper.cpp 1.5.5, `small.en`, local). Use the transcript only to confirm **which scene each take is** and **what was actually said**. Its word timestamps are rough.
3. Compare each transcript with the scene's `spoken` line. Whisper mishears jargon ("evils" for evals, "sip" for ship); treat those as the script. Flag real wording changes (an added or swapped word) to Yovan and update the caption only if he confirms.

## 3. Speed

Ask the speed if it was not given; Yovan's preference so far is **1.2x** (natural pace about 135 WPM becomes about 160, a normal reels pace). `atempo` keeps the pitch. Keep the final reel inside 40 to 60 seconds.

## 4. Align, join, speed up

```text
npm run align -- --reel "<reel folder>/reel.json" --takes "<scene 1 take>" ... --speed 1.2 --out vo-out
```

What it does, and why it is accurate:

- Pauses (`silencedetect`, -38 dB, 0.25 s) split each take into speech segments; blips under 0.3 s are ignored.
- The scene's script is split into phrases at `, . : ? !`. A natural read pauses at punctuation, so segments and phrases line up one to one (too many segments: the closest pair merges; too few: phrases are grouped by dynamic programming on syllable counts).
- Words inside a segment are spread by syllables, giving each caption cue a start and end.
- Takes are trimmed (0.12 s before speech, 0.18 s after), joined with a 0.25 s lead-in and 0.45 s gaps, loudness-normalized to -16 LUFS, and sped up.

Outputs: `vo-out/voiceover.wav`, `captions.json`, `captions.srt`, `alignment.json` (trim points and segments per take). Read `alignment.json`: each take's segment count should equal its phrase count.

## 5. Refine

```text
ffmpeg -i vo-out/voiceover.wav -ar 16000 -ac 1 vo/final-16k.wav
npm run transcribe -- vo/final-16k.wav
npm run refine -- --captions vo-out/captions.json --words vo/final-16k.words.json
```

Cues that start mid-phrase snap to Whisper's time for their first word (within 0.8 s). Cues that start after a pause are already exact. Report the median difference before and after.

Higher-accuracy option when available on this machine: MMS forced alignment (`torchaudio.functional.forced_align` with the `MahmoudAshraf/mms-300m-1130-forced-aligner` model from Hugging Face) gives about 0.06 s word timing. The fbaipublicfiles download of `MMS_FA` fails on certificate errors; use the Hugging Face mirror.

## 6. Render and deliver

1. Copy `vo-out/voiceover.wav` to `public/`, `vo-out/captions.json` to `src/data/`, set `VOICEOVER_FILE = 'voiceover.wav'` in `src/voiceover.ts`. Every animation beat follows the new cue times automatically.
2. Typecheck, render both versions (captions and clean, both with voice), and check the audio stream exists (`ffprobe`).
3. Sample a frame at every beat: faster pacing gives animations less time, so confirm each one finishes before its panel leaves.
4. Copy into the reel folder: both MP4s, `voiceover/voiceover-final-<speed>x.wav`, `voiceover/alignment.json`, and the aligned `captions.srt` / `captions.json` (replacing the estimates). Mark `reel.json` `video.voiceover.captionsAligned: true` so `build_reel_package.py` will not overwrite them.

## Gotchas

- The bundled ffmpeg has `loudnorm`, `atempo`, `silencedetect`, but not `highpass`, `acompressor`, or `dynaudnorm`.
- Run Python with Windows paths (`D:/...`). A Git Bash path like `/d/...` becomes `D:\d\...` in Windows Python and silently writes to the wrong folder.
- `installWhisperCpp` 1.6.2 hangs on Windows; use 1.5.5. Check model downloads finished (`small` is about 487 MB).
