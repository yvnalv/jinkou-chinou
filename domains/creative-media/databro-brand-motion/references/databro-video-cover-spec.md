# Databro Video Cover Spec

Every Databro Reels, TikTok, Shorts, or other video deliverable ships with a dedicated **cover image**. Platforms show the cover in the profile grid, the feed preview, and share sheets. A frame grabbed from the video (mid-animation, with a burned-in caption) looks unfinished there, so the cover is designed on purpose.

## 1. Deliverable

| Video aspect ratio | Cover size | Notes |
|---|---|---|
| `9:16` (Reels / TikTok / Shorts) | `1080x1920` | Default. |
| `4:5` (feed video) | `1080x1350` | |
| `1:1` | `1080x1080` | |
| `16:9` (YouTube) | `1920x1080` | Also export `1280x720` when it is a YouTube thumbnail. |

* Build the cover as its own Remotion composition in the same project as the video (for example `<VideoId>Cover`, 31 frames, same width and height as the video) so it uses the same fonts, tokens, and lockup.
* Render frame 30, after the lockup's frame 0..12 intro has settled:
  `npx remotion still src/index.ts <VideoId>Cover out/cover.png --frame=30`
* Deliver `cover.png` next to the video files, list it in the content spec (`cover` field), and mention it in the reels script header.
* Plan the cover in the storyboard step (headline, hook, key visual) and show it to the user together with the scene plan.

## 2. Layout (9:16)

| Layer | Spec |
|---|---|
| Canvas | Solid `#121212`. No gradients, no glow. |
| Lockup + handle | `DatabroLogoLockup` top-left and `DatabroSocialHandle` top-right, same positions as the video. |
| Captions | None. A cover never shows Closed Captions. |
| Content column | `padding: 0 100px`, vertically centered, `gap` 48 to 56 px, left-aligned. |
| Headline | Plus Jakarta Sans 800, 120 to 132 px, line height about 1.02, `#BB86FC` lavender, with exactly **one** `#C1FF72` lime keyword (the topic term). At most 3 lines; at 128 px a line holds about 11 to 12 characters within 880 px. |
| Hook line | Inter 400, 44 to 46 px, `#FFFFFF`, at most 2 lines. Bold the question part. |
| Key visual | One visual taken from the video's core idea: the explanatory diagram, a code card, a metric, or a versus split. React Icons only. Never the avatar-only outro. |

### Safe area

Keep the headline, hook, and key visual inside **Y 380 to 1500** and **X 100 to 980**:

* The Instagram profile grid crops 9:16 covers to 3:4 (`1080x1440`, about Y 240 to 1680).
* The 4:5 feed preview shows about Y 285 to 1635.
* TikTok and Reels overlay buttons on the right rail and text at the bottom of the full-screen view.

For other ratios, keep 100 px side margins and keep content clear of the top lockup band.

## 3. Cover types

Pick the type that matches the video's opening hook.

| Type | Best for | Layout |
|---|---|---|
| **Question** | `concept-theory`, `opinion-editorial` | Optional cream emblem (`#F0ECE2`, 180 px) with a React Icon plus 1 or 2 mono tag chips; giant lavender question with the lime keyword; white hook line. |
| **Diagram** | Process or flow explainers | Question headline, hook line, then a compact version of the video's key diagram (for example two pipeline rows). |
| **Versus** | Comparisons (`A vs B`) | Short lavender headline; two halves, each with icon, big word (teal / lime), and a one-line meaning, split by a 3 px `#2E2E2E` divider; white closing line. |
| **Code card** | `code-walkthrough`, code-shock openings | Coral `#FF5757` warning line with `LuTriangleAlert`; headline; GitHub Dark code card (`#24292E`) with a 4 px `#D92D20` callout outline. |

One cover is the default deliverable. Offer 2 or 3 variants (one per type) only when the user asks or the hook is unclear.

## 4. Rules

* Same brand rules as the video: flat colors, React Icons only, zero em-dashes and en-dashes, "kamu/kita" (never "lo/gue").
* The cover text matches the video's topic and the first line of the post caption. The hook may paraphrase the script.
* The cover must make sense without sound and without the video.

## 5. Checklist

- [ ] `cover.png` rendered at the video's size from a dedicated cover composition (frame 30).
- [ ] Lavender headline with exactly one lime keyword, white hook, one key visual from the video.
- [ ] No captions on the cover; lockup and handle present.
- [ ] Viewed both full frame and the 3:4 crop (`crop=1080:1440:0:240`); nothing important is cut.
- [ ] Saved next to the video files and listed in the content spec.
