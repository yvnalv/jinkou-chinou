# Platform Format Specifications: yvnalvworks

## 1. Instagram Feed Carousel
- **Aspect Ratio**: 4:5 vertical portrait
- **Resolution**: 1080 x 1350 px
- **Slide Count**: 5 to 10 slides that follow the five story beats (moment, problem, turn, lesson, next step); a beat can span more than one slide
- **Copy**: Flowing, friendly sentences per `references/yvnalvworks-voice-and-tone-guide.md`; 1 to 3 sentences of body per slide
- **Safe Margins**: 80px left/right, 80px top/bottom
- **Visual Style**: Matte charcoal grain background image (never a flat fill), Poppins typography (Bold headlines), white headlines with Warm Ivory (`#F0ECE2`) secondary text, one Electric Lime (`#C1FF72`) punchline phrase per slide, and solid framework cards with dark inner containers.
- **Cover (Slide 1)**: Avatar with `yvnalvworks` / `@yvnalvworks` lockup above a 3 to 4 line headline; nothing else on the slide. Copy rules: `references/cover-headline-patterns.md`.

## 2. Instagram Reels / Short-form Video
- **Aspect Ratio**: 9:16 vertical video
- **Resolution**: 1080 x 1920 px
- **Target Duration**: as long as the story needs and under 3 minutes (most land around 45 to 90 seconds); about 140 words per minute, relaxed conversation. Never pad a story to fill time, and never cut a payoff to hit a number.
- **Structure**: Hook 0 to 3 s (first sentence 8 words or fewer, visual from frame 0), Setup 3 to 12 s, Discovery 12 to 40 s, Payoff (answers the hook), Takeaway + CTA in the last 10 seconds; longer stories stretch the discovery, not the hook.
- **Safe Zones**:
  - Top header safe zone: 0 - 150px
  - Bottom actions safe zone: 1640 - 1920px
  - Right interaction strip: 960 - 1080px
  - Closed Captions locked position: Center Y = 1480px
- **Cover (required)**: Every reel or video gets a 9:16 cover with the same lockup and headline style as the feed cover (`coverHeadline` in `reel.json`, rules in `references/cover-headline-patterns.md`). Rendered by `/yvnalvworks-brand-motion` as `reel-cover.png`.
- **Visual Plan**: One concrete animated visual per story beat (mockup, breaking chart, step rail, app-style Lucide tiles, transformation, end card), timed to its caption cue. Illustrative numbers are tagged `illustrative`; no third-party logos. Production style: `/yvnalvworks-brand-motion` reels motion system.
- **Package**: `reel.json` → `scripts/build_reel_package.py` → script, teleprompter guide, `captions.srt`, `captions.json`, `content-spec.json`, `cover-spec.json`; plus `caption.txt`.
- **Captions Format**: Exact voiceover words in sentence case (not ALL CAPS), one cue per breath group: 3 to 9 words and at most 48 characters, shown on up to two lines, broken at commas and breath points, never splitting a phrase that belongs together, no trailing periods. High contrast.

## 3. LinkedIn Article / Technical Post
- **Format**: Structured Markdown with bullet points, code blocks, and primary source links
- **Tone**: A friendly senior engineer telling the story of a real problem, with honest trade-offs and sources.
