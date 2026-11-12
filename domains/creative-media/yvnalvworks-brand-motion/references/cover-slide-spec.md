# yvnalvworks Cover Slide Spec (4:5)

Measured from the two published reference covers in `assets/reference-covers/`. Every carousel cover (slide 1) follows this spec so the feed reads as one series. Open the reference images and compare side by side before handing over a render.

| Reference file | Headline | Pattern |
|---|---|---|
| `assets/reference-covers/cover-ref-listicle-ai-updates.jpg` | 3 AI Updates / Every Builder / **Should Know** / in April 2026 | Numbered listicle, highlight on the promise |
| `assets/reference-covers/cover-ref-should-know-maf.jpg` | What AI Engineers / Should Know / About **Microsoft / Agent Framework** | Audience question, highlight on the subject |

## 1. Canvas

* 1080 x 1350 (4:5), exported at 2x (2160 x 2700).
* Background: `assets/brand-kit/backgrounds/yvnalvworks-grain-bg.png`, scaled with `cover`. It is a `#121212` base with fine light speckle grain and soft lighter haze in the top-left and bottom-right. **Never replace it with a flat color fill**; `#121212` is only the fallback color behind the image.
* Nothing else on the cover: no slide counter, no footer, no domain watermark, no swipe cue, no icons, no logo wordmark.

## 2. Layout

The lockup and headline form one block. Text inside the block is **left-aligned**; the block as a whole is **centered optically**:

| Property | Value |
|---|---|
| Block width | Shrinks to the longest headline line, max 860px |
| Horizontal position | Centered, nudged ~20px left of true center |
| Vertical position | Centered, nudged ~55px above true center (block spans roughly y 360 to 880) |
| Side margin | Never below 100px |

## 3. Author lockup (above the headline)

| Element | Spec |
|---|---|
| Avatar | `assets/brand-kit/logos/yovan-avatar-color.png`, 66px circle, no border |
| Gap avatar to text | 10px |
| Name | `yvnalvworks`, Poppins 600, 24px, `#FFFFFF` |
| Handle | `@yvnalvworks`, Poppins 400, 21px, `#F0ECE2` (Warm Ivory) |
| Gap lockup to headline | ~46px (lockup bottom to headline box top) |

## 4. Headline

| Property | Value |
|---|---|
| Font | Poppins 700 (Bold) |
| Size | 96px |
| Line height | 1.02 (about 98px line pitch) |
| Tracking | -0.04em |
| Case | Title Case |
| Base color | `#FFFFFF` |
| Highlight | `#C1FF72` Electric Lime on exactly **one** phrase |
| Lines | 3 to 4, each 2 to 3 words; break lines by hand |

Line width: about 17 characters of Poppins Bold fill the 860px measure ("What AI Engineers" is 836px), but wide letters overflow sooner: "Should Know About" (17 characters) does not fit. Break as "Should Know / About [[Subject]]", as in the reference. The renderer warns when a hand-broken line wraps.

Highlight rule: light up either the **promise** ("Should Know") or the **subject** ("Microsoft Agent Framework"), never both, never a single filler word. Keep the highlighted phrase on its own line(s) where possible; the auto-wrap can split it awkwardly, so always pass explicit line breaks.

Headline copy patterns (written by `/yvnalvworks-content-ideas`):

* `What [Audience] Should Know About [[Subject]]`
* `[N] [Topic] Every [Audience] [[Should Know]] in [Month Year]`
* `[N] [Things] [Audience] [[Should Read]]` (resource roundups)

## 5. Rendering

Use the `cover` slide type in `scripts/render_carousel.py`; it encodes every value above:

```json
{"slides": [
  {"type": "cover", "headline": "What AI Engineers\nShould Know\nAbout [[Microsoft\nAgent Framework]]"}
]}
```

`\n` is a line break; `[[...]]` is the lime highlight and may span a break.

## 6. Reel and video cover (9:16)

**Every reel or video ships with a cover.** It is the same cover as the feed: lockup and headline only, same type scale, same highlight rule, on the grain background, at 1080 x 1920.

- The block is optically centered in the 9:16 frame, so it stays inside both profile-grid crops (centered 4:5, y 285 to 1635, and centered 3:4, y 240 to 1680). Nothing important goes outside y 285 to 1635.
- No captions, icons, play buttons, or frame grabs on the cover.
- Render it with `"format": "reel"`; output `reel-cover.png` (2160 x 3840 at 2x) into the reel folder next to the MP4s:

```json
{"format": "reel", "slides": [
  {"type": "cover", "headline": "6 Steps Every\nAI Builder\n[[Should Know]]", "file": "reel-cover.png"}
]}
```

`/yvnalvworks-content-ideas` writes this file as `cover-spec.json` from the reel's `coverHeadline`, so normally you only run `python <skill-dir>/scripts/render_carousel.py <reel-folder>/cover-spec.json --out <reel-folder>`.

## 7. Outside inspiration (not bundled)

The owner also shared another creator's listicle cover (blue gradient, 3D clay icons, third-party company logos, "With Links" pill, "Swipe next" footer). It is kept as copy inspiration only and is not bundled, because it carries another person's name, photo, and trademarked logos.

* **Borrow:** the value-promise headline ("... You Should Read") and the idea of stating the bonus in the copy ("With Links", "With Code").
* **Do not borrow:** blue or purple gradients, 3D clay illustrations, brand logos, pill badges, header year stamps, or footer swipe bars. They break the yvnalvworks matte grain aesthetic.

## 8. Cover review checklist

- [ ] Grain background image present (not a flat fill).
- [ ] Lockup: color avatar, white name, ivory handle, above the headline.
- [ ] Headline Poppins Bold 96px, -0.04em, left-aligned, 3 to 4 hand-broken lines.
- [ ] Exactly one lime phrase.
- [ ] Block optically centered; nothing else on the slide.
- [ ] Side-by-side comparison with a reference cover shows the same scale and position.
- [ ] Reel cover: 1080 x 1920 (2x export), block inside the centered 4:5 crop, saved as `reel-cover.png` next to the MP4s.
