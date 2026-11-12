# yvnalvworks-content-ideas

Researches, validates, and structures evidence-backed technical content ideas for **yvnalvworks** across AI Engineering, Computer Vision, Edge Systems, and High-Performance Software Engineering in 100% Technical English.

## When to use

* Use when drafting technical carousel or reels content ideas for `@yvnalvworks` or `yvnalvworks.com`.
* Use when planning engineering breakdowns, evals architectures, edge AI pipelines, or MLOps systems.
* Use when preparing teleprompter voiceover guides and 2-4 word ALL-CAPS SRT closed captions for Yovan's manual voice recording.
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
│   └── yvnalvworks-voice-and-tone-guide.md  # Tone constraints and em-dash ban
├── scripts/
│   ├── format_content_idea.py               # Markdown validator and formatter
│   └── sync_notion_planner.py               # Notion payload constructor
└── assets/
    └── content-idea.starter.json            # Reference starter JSON payload
```

## Changelog

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
