# yvnalvworks Reel Starter (Remotion)

A ready-to-run 9:16 Remotion project that matches the published yvnalvworks reel style. Read `references/reels-motion-system.md` (in this skill) before building scenes.

## Set up a new reel

1. Copy this folder to `D:\yvnalv\AI Skills\remotion-demos\<reel-name>\` (never inside OneDrive: `node_modules` must not sync).
2. Copy the brand assets into `public/`:
   - `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png`
   - `assets/brand-kit/logos/yovan-avatar-color.png`
3. Copy the reel's `captions.json` (from `/yvnalvworks-content-ideas`, `build_reel_package.py`) into `src/data/captions.json`.
4. `npm install`, then `npm run studio` to preview.

## Files

| File | Role |
|---|---|
| `src/theme.ts` | Fonts (Poppins, JetBrains Mono), color tokens, centered layout constants |
| `src/timing.ts` | `at(id)` / `until(id)` cue frames, `pop`, `ease`, `span`, `mix`, `rand` |
| `src/components/Base.tsx` | Background, TopLockup, Captions, Wipe, AppTile, Tag |
| `src/components/Patterns.tsx` | Panel, StepHeading, PhoneFrame, LineChart, Meter, StepRail, EndCard, morph |
| `src/Reel.tsx` | Example reel (three scenes + end card); replace the scenes |
| `src/Root.tsx` | Two compositions: `YvnalvworksReel` (captions) and `YvnalvworksReelClean` |
| `src/voiceover.ts` | `VOICEOVER_FILE`: null (silent) or the aligned voiceover in `public/` |
| `scripts/transcribe.mjs` | whisper.cpp (local) transcript + word times per WAV -> `<name>.words.json` |
| `scripts/align_voiceover.py` | Joins takes, speeds up, times captions from pauses + syllables -> `vo-out/` |
| `scripts/refine_captions.py` | Snaps cue starts to Whisper word times on the final audio |

## Voiceover (after Yovan records)

Full guide: `references/voiceover-sync.md` in this skill.

```text
# 1. Check what each take says (one take per scene; skip false starts)
npm run transcribe -- vo/take1-16k.wav vo/take2-16k.wav ...   # 16 kHz mono WAV copies of the takes
# 2. Join, speed up, and time the captions to the real audio
npm run align -- --reel "<reel folder>/reel.json" --takes "<take scene 1>" "<take scene 2>" ... --speed 1.2 --out vo-out
# 3. Snap mid-phrase cues to Whisper word times on the final audio
npm run transcribe -- vo/final-16k.wav
npm run refine -- --captions vo-out/captions.json --words vo/final-16k.words.json
```

Then copy `vo-out/voiceover.wav` to `public/`, `vo-out/captions.json` to `src/data/`, set `VOICEOVER_FILE = 'voiceover.wav'` in `src/voiceover.ts`, and render.

## Render

```text
npm run typecheck
npm run render        # out/reel-captions.mp4
npm run render:clean  # out/reel-clean.mp4
```

Copy both MP4s into the reel's OneDrive folder. After the voiceover is recorded and `captions.json` re-timed, run `REEL_DIR="<reel folder>" npm run sync` and render again; every beat follows the new timing.
