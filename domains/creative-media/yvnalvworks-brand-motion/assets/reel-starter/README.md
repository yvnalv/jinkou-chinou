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

## Render

```text
npm run typecheck
npm run render        # out/reel-captions.mp4
npm run render:clean  # out/reel-clean.mp4
```

Copy both MP4s into the reel's OneDrive folder. After the voiceover is recorded and `captions.json` re-timed, run `REEL_DIR="<reel folder>" npm run sync` and render again; every beat follows the new timing.
