# yvnalvworks-content-ideas

Researches, validates, and structures evidence-backed technical content ideas for **yvnalvworks** across AI Engineering, Computer Vision, Edge Systems, and High-Performance Software Engineering, told as friendly, easy-to-follow stories that stay technically accurate.

## When to use

* Use when drafting technical carousel or reels content ideas for `@yvnalvworks` or `yvnalvworks.com`.
* Use when planning engineering breakdowns, evals architectures, edge AI pipelines, or MLOps systems.
* Use when preparing conversational reel scripts, teleprompter voiceover guides, sentence-case closed captions, and post captions for Yovan's manual voice recording.
* Use when synchronizing approved ideas to the `📆 yvnalvworks Content Planner` database in Notion.
* Invoke via slash command: `/yvnalvworks-content-ideas`.

## Structure

```
yvnalvworks-content-ideas/
├── SKILL.md                                 # Core agent instructions and gates
├── README.md                                # Human documentation and changelog
├── config/
│   └── skill.yaml                           # Machine-readable manifest and policies
├── evals/
│   └── evals.json                           # Trigger and behavior eval test cases
├── references/
│   ├── CONTENT_IDEA.template.md             # Markdown outline template
│   ├── cover-headline-patterns.md           # Cover headline formulas from published covers
│   ├── platform-format-specs.md             # Resolution and safe zone specifications
│   ├── yvnalvworks-content-pillars.md       # Scope of 4 core engineering pillars
│   └── yvnalvworks-voice-and-tone-guide.md  # Storytelling voice, story beats, caption rules
├── scripts/
│   ├── build_reel_package.py                # reel.json -> script, teleprompter, captions, spec
│   ├── format_content_idea.py               # Markdown validator and formatter
│   └── sync_notion_planner.py               # Notion payload constructor
└── assets/
    ├── content-idea.starter.json            # Reference starter JSON payload
    └── reel.starter.json                    # Reference reel.json for build_reel_package.py
```

## Changelog

### 0.6.0 — 2026-11-13
* Teleprompter guide asks for one take per scene with natural pauses, matching the brand-motion voiceover sync.
* `build_reel_package.py` keeps captions already aligned to a recorded voiceover (`--force-captions` to overwrite).

### 0.5.0 — 2026-11-12
* Every reel or video gets a cover: `reel.json` requires a `coverHeadline` (same formulas and rules as carousel covers), and `build_reel_package.py` validates it and writes `cover-spec.json` for the 9:16 cover render in `/yvnalvworks-brand-motion`.

### 0.4.0 — 2026-11-12
* New `scripts/build_reel_package.py` and `assets/reel.starter.json`: one `reel.json` generates the reel script, teleprompter guide, `captions.srt`, `captions.json`, and `content-spec.json`, and enforces the caption rules (matches spoken words, sentence case, 3 to 6 words, 32 characters, no dashes). Tested on the published AI Engineering Workflow reel (byte-identical captions and guide) and on broken inputs.
* Reels now carry a visual plan per scene: one concrete animated metaphor per story beat, matching the brand-motion reels motion system.

### 0.3.0 — 2026-11-12
* New voice: friendly, flowing storytelling instead of terse "technical English". Rewrote `references/yvnalvworks-voice-and-tone-guide.md` with the five story beats (moment, problem, turn, lesson, next step), sentence rules, and before/after examples.
* The 5-part arc (hook, anti-pattern, framework, golden rule, CTA) is now the five story beats; JSON keys are unchanged, so existing ideas still validate.
* Closed captions change from 2-4 word ALL CAPS chunks to sentence-case natural phrases (3 to 6 words, max 32 characters).
* Reels target 40 to 60 seconds at about 140 WPM; carousels run 5 to 10 slides.
* Template, platform specs, cover headline notes, formatter headings, manifest, and evals updated to match.

### 0.2.1 — 2026-11-12
* Cover headline rules: the 18-character limit is a ceiling; "Should Know About" never fits on one line, so break it as "Should Know / About [[Subject]]".

### 0.2.0 — 2026-11-12
* Added `references/cover-headline-patterns.md` from the published covers: "What X Should Know About Y", numbered "Should Know" listicles, "Should Read" roundups, and one `[[lime]]` highlight phrase.
* Slide 1 is now the cover headline; the bold-statement hook moves to the caption and reel opener.
* `format_content_idea.py` requires and validates `coverHeadline` for carousels (3 to 4 lines, max 18 characters per line, exactly one highlight) and prints it in the outline.
* Platform specs updated to the grain background and Poppins typography.

### 0.1.0 — 2026-11-12
* Initial specialized release for yvnalvworks technical content research.
* Integrated 5-part narrative arc, Lucide icon pairings, and zero em-dash policy.
* Integrated manual voiceover teleprompter formatting and Notion planner database synchronization.
