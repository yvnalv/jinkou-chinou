# yvnalvworks Reels Motion System (9:16)

How yvnalvworks reels look and move. Distilled from the published "The AI Engineering Workflow" reel (2026-11-12), which the owner approved as the reference style. Build every reel from `assets/reel-starter/` and this file.

## 1. The idea in one line

Every spoken story beat gets **one concrete, animated visual metaphor**, timed to the caption cue that says it. The viewer should understand the story with the sound off.

## 2. Layout (1080 x 1920)

| Zone | Rule |
|---|---|
| Header safe area | y 0 to 150: nothing |
| Author lockup | Top-left at x 60, y 168: 54px color avatar, `yvnalvworks` (600, 24px, white), `@yvnalvworks` (400, 19px, ivory). Hidden on the end card. |
| Content | **Centered on x = 540** with mirrored margins: content stays inside x 120 to 960. Text inside a block stays left-aligned; the block itself is centered. Never shift content off-center to dodge the action strip; mirror the margin instead. |
| Stage | y 300 to about 1380 |
| Captions | Pill centered on x 540 and y 1480, inside x 120 to 960 |
| Bottom | y 1640 to 1920: nothing |

Check centering on every review: draw a vertical line at x 540 over sampled frames.

## 3. Timing: captions drive everything

- `captions.json` (from `/yvnalvworks-content-ideas` `build_reel_package.py`) is the single timeline. Every beat starts at `at(cueId)` in `src/timing.ts`.
- When the voiceover is recorded and the captions re-timed, `npm run sync` and re-render; the animation follows the voice.
- Reels run 40 to 60 seconds; the composition adds about 2 seconds of tail for the end card.

## 4. Story beat to visual

| Beat | Visual pattern (starter component) | Example from the reference reel |
|---|---|---|
| The moment | A product mockup the viewer recognizes: `PhoneFrame` with app tiles, a chat, a prompt box, a button press, a cursor | Pick "Model 5 NEW", type a prompt, press "Ship it", rocket launches |
| The problem | A state that visibly breaks: `LineChart` crash in red, red-bordered wrong answer, user icons crowding in, a short shake | Bot says "Refunds are free, forever!", quality drops 94% to 41% |
| The turn | Lime `Wipe`, then a structure appears: `StepRail` drawing in, a short "kicker + big line" heading | "Six steps, one loop." |
| Steps / framework | One `Panel` per step with a `StepHeading` ("STEP 03 / 06") and one illustration each: checklist ticks, a test runner (spinner then pass/fail), typing text, items flowing along a curve, scattered dots converging, `AppTile` row, live chart | Evals, prompt, retrieval, fine-tuning, guardrails/caching/monitoring |
| Progress | A `Meter` that climbs as the story improves the system | "Evals passing 3/6 to 6/6" |
| The lesson | A transformation, not a slide: nodes `morph` from rail to straight line to loop, an item travels back along the loop, a lime badge confirms | Failure rides the ring into Evals, "+1 new test" |
| Next step + CTA | `EndCard` on the last cue: large avatar, handle, lime "Follow for more", domain | |

## 5. Motion rules

- Springs for things that appear (`pop`, damping 12 to 16); eased 10 to 16 frame fades and slides for panels (`Panel`: slide 70px in from the right, 40px out to the left).
- Stagger groups by 3 to 6 frames. Never animate more than two things at once on a single beat.
- One hard transition style: the lime `Wipe`, used once at the turn (act change). Everything else crossfades.
- Hold each finished state for at least 1 second before the next beat replaces it.

## 6. Color and meaning

| Color | Meaning in motion |
|---|---|
| Electric Lime `#C1FF72` | Good, active, done, the one highlighted phrase |
| Danger `#EF4444` | Failure, wrong answer, crash, problem factors |
| Ivory `#F0ECE2` / White | Neutral content and text |
| Muted `#71717A` | Pending, inactive, labels |

Every chart, score, or number that is not real data carries the mono tag `illustrative`.

## 7. Icons and app tiles

- Lucide only (`lucide-react` 0.460.0), stroke width 2, no fills.
- "App icons" are `AppTile`s: a rounded card tile with a Lucide glyph and a label. **Never** use OpenAI, Anthropic, Google, or other third-party logos.

## 8. Captions

Sentence case, natural phrases of 3 to 6 words (max 32 characters), Poppins 600 46px white on a dark pill (`rgba(18,18,18,0.78)`, 1px `#27272a` border), centered at y 1480, popping in per cue.

## 9. Deliverables and QA

1. Project lives in `D:\yvnalv\AI Skills\remotion-demos\<reel-name>\` (not OneDrive).
2. `npm run typecheck`, then render both: `npm run render` (captions) and `npm run render:clean` (no captions, for CapCut).
3. **Render the cover.** Every reel ships with `reel-cover.png` (9:16, same lockup and headline as the feed cover): `python <skill-dir>/scripts/render_carousel.py <reel-folder>/cover-spec.json --out <reel-folder>`. See `references/cover-slide-spec.md`, section 6.
4. Extract a frame from every scene (`npx remotion ffmpeg -ss <sec> -i <mp4> -frames:v 1 ...`) and check: grain background, centering on x 540, nothing in the right strip or header, captions readable, no overlaps.
5. Copy both MP4s into the reel's OneDrive folder next to the cover, script, guide, captions, and `reel.json`.
